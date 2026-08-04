#!/usr/bin/env python3
"""
Independent skill-eval harness for the personalized-learning stage skills,
the orchestration entrypoint, and the check-* quality skills. Implements the §8 with-skill / without-skill
benchmark contract from openspec change create-seven-stage-personalized-learning-skills:

  <skills-root>/<skill>-workspace/iteration-N/<eval-name>/
      eval_metadata.json
      with_skill/    { run.json, timing.json, grading.json }
      without_skill/ { run.json, timing.json, grading.json }
  <skills-root>/<skill>-workspace/iteration-N/
      benchmark.json, benchmark.md, review.html

It drives the installed `claude` CLI (routes: gclaude / dclaude) non-interactively,
captures raw JSON, exit status, timing, and the OUTER modelUsage; grades each run
against the grader-held expectations with an LLM judge; and aggregates per-skill.

This is an eval RUNNER, not a validator. It exists because the installed
skill-creator ships only init/validate/yaml scripts and no eval runner.

Usage:
  python3 scripts/run_skill_evals.py --skill build-capability-concept-graph \
      --route gclaude --iteration 1 --max-turns 6
  python3 scripts/run_skill_evals.py --all --route gclaude --iteration 1
"""
import argparse, json, os, re, subprocess, sys, time, datetime, html, pathlib

REPO = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_SKILLS_ROOT = REPO / ".agents" / "skills"

ROUTES = {
    # gclaude = default claude; dclaude = deepseek-settings claude (glm route)
    "gclaude": ["/usr/local/bin/claude", "--dangerously-skip-permissions"],
    "dclaude": ["/usr/local/bin/claude", "--settings", "/Users/logo/.claude/deepseek.json", "--dangerously-skip-permissions"],
}

EXECUTOR_PREAMBLE = (
    "You are executing ONE stage of a seven-stage personalized-learning SOP and must "
    "produce that stage's handoff envelope as a SINGLE JSON object. Think, then output "
    "ONLY the JSON envelope (no prose before/after). If you cannot fully satisfy a gate, "
    "emit the honest blocked/pending state rather than fabricating a pass."
)
EXECUTOR_PREAMBLE_WITHOUT = (
    "You are executing ONE stage of a personalized-learning SOP and must produce that "
    "stage's output as a SINGLE JSON object. Think, then output ONLY the JSON (no prose)."
)
ORCHESTRATOR_PREAMBLE = (
    "You are executing the user-facing orchestration entrypoint above a seven-stage "
    "personalized-learning SOP. Interpret the request, select or invoke the correct stage, "
    "preserve all gate and real-user-input boundaries, and return a concise evidence-backed "
    "user response with the next action. Treat any project state embedded in the task as an "
    "evaluation fixture; do not claim file writes that you did not perform."
)


def now_iso():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def load_cases(skill_dir):
    raw = json.load(open(skill_dir / "evals" / "evals.json"))
    return raw.get("evals", raw.get("cases", []))


def load_skill_context(skill_dir):
    """Return the skill body (instructions + contract + schemas) for with-skill runs."""
    parts = []
    sk = skill_dir / "SKILL.md"
    if sk.exists():
        parts.append("# SKILL.md\n\n" + sk.read_text())
    sc = skill_dir / "references" / "stage-contract.md"
    if sc.exists():
        parts.append("# references/stage-contract.md\n\n" + sc.read_text())
    oc = skill_dir / "references" / "orchestration-contract.md"
    if oc.exists():
        parts.append("# references/orchestration-contract.md\n\n" + oc.read_text())
    for schema in sorted((skill_dir / "references").glob("*.schema.json")):
        parts.append(f"# references/{schema.name}\n\n```json\n{schema.read_text()}\n```")
    example = skill_dir / "references" / "example.md"
    # NOTE: example.md is intentionally NOT injected into executor prompts (anti-leakage).
    return "\n\n---\n\n".join(parts)


def run_claude(route, prompt, append_system=None, max_turns=6, timeout=600):
    """Run claude -p non-interactively; return (result_dict_or_None, exit_status, raw_stdout, elapsed)."""
    cmd = ROUTES[route][:] + ["-p", prompt, "--output-format", "json", "--max-turns", str(max_turns)]
    if append_system:
        cmd += ["--append-system-prompt", append_system]
    t0 = time.time()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, -1, "", time.time() - t0
    elapsed = time.time() - t0
    out = proc.stdout
    # claude --output-format json prints one JSON object per line events + a final result line.
    # The final result object has "type": "result".
    result = None
    for line in out.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue
        if obj.get("type") == "result":
            result = obj
    return result, proc.returncode, out, elapsed


def grade(route, executor_output, expectations, case_id, config, max_turns=4):
    """LLM judge: evaluate executor output against grader-held expectations."""
    exp_block = "\n".join(f"{i+1}. {e}" for i, e in enumerate(expectations))
    prompt = (
        "You are a STRICT grader. Given an executor's output and a list of expectations, "
        "decide for EACH expectation whether it is satisfied by the output. Be strict and "
        "evidence-based; do not infer beyond what the output shows. "
        "Output ONLY a JSON object of this exact shape:\n"
        '{"expectation_results":[{"expectation":"<verbatim>","passed":true|false,"evidence":"<short>"}],'
        '"overall_passed":true|false,"summary":"<one line>"}\n\n'
        f"EXPECTATIONS:\n{exp_block}\n\n"
        f"EXECUTOR OUTPUT:\n{executor_output}\n\n"
        "Return ONLY the JSON object."
    )
    result, exit_status, raw, elapsed = run_claude(route, prompt, max_turns=max_turns, timeout=180)
    grading = {
        "case_id": case_id, "config": config, "graded_at": now_iso(), "expectation_results": [],
        "overall_passed": False, "summary": "", "grader_elapsed_s": round(elapsed, 2),
        "grader_exit_status": exit_status,
    }
    if result:
        txt = result.get("result", "")
        grading["grader_modelUsage"] = result.get("modelUsage")
        grading["grader_cost_usd"] = result.get("total_cost_usd")
        m = re.search(r"\{.*\}", txt, re.S)
        if m:
            try:
                parsed = json.loads(m.group(0))
                grading["expectation_results"] = parsed.get("expectation_results", [])
                grading["overall_passed"] = bool(parsed.get("overall_passed", False))
                grading["summary"] = parsed.get("summary", "")
            except Exception as e:
                grading["summary"] = f"grader parse error: {e}"
        else:
            grading["summary"] = "grader returned no JSON"
    else:
        grading["summary"] = f"grader run failed (exit {exit_status})"
    return grading


def write_run_artifacts(cfg_dir, config, result, exit_status, raw, elapsed, grading):
    cfg_dir.mkdir(parents=True, exist_ok=True)
    run = {
        "config": config, "captured_at": now_iso(), "exit_status": exit_status,
        "elapsed_s": round(elapsed, 2),
    }
    if result:
        run["result_text"] = result.get("result", "")
        run["duration_ms"] = result.get("duration_ms")
        run["total_cost_usd"] = result.get("total_cost_usd")
        run["usage"] = result.get("usage")
        run["modelUsage"] = result.get("modelUsage")  # outer route/model provenance
        run["num_turns"] = result.get("num_turns")
        run["is_error"] = result.get("is_error")
    else:
        run["result_text"] = ""
        run["error"] = "no result object (timeout or crash)"
    (cfg_dir / "run.json").write_text(json.dumps(run, ensure_ascii=False, indent=2))
    timing = {
        "config": config, "elapsed_s": round(elapsed, 2),
        "duration_ms": result.get("duration_ms") if result else None,
        "api_duration_ms": result.get("duration_api_ms") if result else None,
    }
    (cfg_dir / "timing.json").write_text(json.dumps(timing, ensure_ascii=False, indent=2))
    (cfg_dir / "grading.json").write_text(json.dumps(grading, ensure_ascii=False, indent=2))
    return run


def eval_skill(skill_name, route, iteration, skills_root, max_turns, grade_turns, dry_run, out_root):
    skill_dir = skills_root / skill_name
    cases = load_cases(skill_dir)
    skill_ctx = load_skill_context(skill_dir)
    ws_root = out_root if out_root else skills_root
    ws = ws_root / f"{skill_name}-workspace" / f"iteration-{iteration}"
    ws.mkdir(parents=True, exist_ok=True)
    print(f"\n=== {skill_name} ({route}, iteration {iteration}) — {len(cases)} cases ===", flush=True)
    per_case = []
    for case in cases:
        cid = case.get("id")
        label = case.get("label")
        ename = f"eval-{cid}-{label}" if label else f"eval-{cid}"
        ename = re.sub(r"[^A-Za-z0-9._-]+", "-", ename)[:80]
        prompt = case["prompt"]
        expectations = case.get("expectations", [])
        meta = {
            "skill_name": skill_name, "case_id": cid, "eval_name": ename,
            "source": case.get("source", {}), "route": route, "iteration": iteration,
            "expectations_count": len(expectations),
        }
        (ws / ename / "eval_metadata.json").parent.mkdir(parents=True, exist_ok=True)
        (ws / ename / "eval_metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2))

        case_result = {"case_id": cid, "eval_name": ename, "expectations": expectations}
        for config in ("without_skill", "with_skill"):
            if dry_run:
                print(f"  [dry-run] {ename}/{config}", flush=True)
                continue
            sys_prompt = skill_ctx if config == "with_skill" else None
            if case.get("execution_mode") == "orchestrator":
                preamble = ORCHESTRATOR_PREAMBLE
            else:
                preamble = EXECUTOR_PREAMBLE if config == "with_skill" else EXECUTOR_PREAMBLE_WITHOUT
            full_prompt = f"{preamble}\n\nTASK:\n{prompt}"
            t0 = time.time()
            result, exit_status, raw, elapsed = run_claude(
                route, full_prompt, append_system=sys_prompt, max_turns=max_turns)
            out_text = result.get("result", "") if result else ""
            grading = grade(route, out_text, expectations, cid, config, max_turns=grade_turns)
            run = write_run_artifacts(ws / ename / config, config, result, exit_status, raw, elapsed, grading)
            n_pass = sum(1 for r in grading.get("expectation_results", []) if r.get("passed"))
            n_tot = len(grading.get("expectation_results", []))
            print(f"  {ename}/{config}: exit={exit_status} {elapsed:.0f}s pass={n_pass}/{n_tot} "
                  f"overall={grading.get('overall_passed')} cost=${run.get('total_cost_usd',0):.4f}", flush=True)
            case_result[config] = {
                "exit_status": exit_status, "elapsed_s": round(elapsed, 2),
                "overall_passed": grading.get("overall_passed"),
                "expectations_passed": n_pass, "expectations_total": n_tot,
                "cost_usd": run.get("total_cost_usd"), "modelUsage": run.get("modelUsage"),
            }
        per_case.append(case_result)
    if dry_run:
        return None
    benchmark = aggregate(skill_name, route, iteration, per_case)
    (ws / "benchmark.json").write_text(json.dumps(benchmark, ensure_ascii=False, indent=2))
    (ws / "benchmark.md").write_text(render_benchmark_md(benchmark))
    (ws / "review.html").write_text(render_review_html(benchmark, per_case, ws))
    return benchmark


def aggregate(skill_name, route, iteration, per_case):
    def summ(key):
        rows = [c[key] for c in per_case if key in c]
        return {
            "cases": len(rows),
            "overall_passed": sum(1 for r in rows if r.get("overall_passed")),
            "expectations_passed": sum(r.get("expectations_passed", 0) for r in rows),
            "expectations_total": sum(r.get("expectations_total", 0) for r in rows),
            "avg_elapsed_s": round(sum(r.get("elapsed_s", 0) for r in rows) / len(rows), 2) if rows else 0,
            "total_cost_usd": round(sum(r.get("cost_usd") or 0 for r in rows), 6),
        }
    with_s = summ("with_skill")
    without_s = summ("without_skill")
    delta_exp = with_s["expectations_passed"] - without_s["expectations_passed"]
    return {
        "skill_name": skill_name, "route": route, "iteration": iteration,
        "generated_at": now_iso(),
        "with_skill": with_s, "without_skill": without_s,
        "delta_expectations_passed": delta_exp,
        "skill_helps": delta_exp > 0,
        "cases": per_case,
    }


def render_benchmark_md(b):
    lines = [
        f"# Benchmark — {b['skill_name']} ({b['route']}, iteration {b['iteration']})",
        "",
        f"Generated: {b['generated_at']}",
        "",
        "| metric | without_skill | with_skill | Δ |",
        "|---|---|---|---|",
        f"| cases overall-passed | {b['without_skill']['overall_passed']}/{b['without_skill']['cases']} | "
        f"{b['with_skill']['overall_passed']}/{b['with_skill']['cases']} | "
        f"{b['with_skill']['overall_passed']-b['without_skill']['overall_passed']:+d} |",
        f"| expectations passed | {b['without_skill']['expectations_passed']}/{b['without_skill']['expectations_total']} | "
        f"{b['with_skill']['expectations_passed']}/{b['with_skill']['expectations_total']} | "
        f"{b['delta_expectations_passed']:+d} |",
        f"| avg elapsed (s) | {b['without_skill']['avg_elapsed_s']} | {b['with_skill']['avg_elapsed_s']} | |",
        f"| total cost (USD) | {b['without_skill']['total_cost_usd']:.4f} | {b['with_skill']['total_cost_usd']:.4f} | |",
        "",
        f"**Skill helps (more expectations pass with the skill): {b['skill_helps']}**",
        "",
        "## Per-case",
        "| case | without overall | with overall | without exp | with exp |",
        "|---|---|---|---|---|",
    ]
    for c in b["cases"]:
        wo = c.get("without_skill", {}); wi = c.get("with_skill", {})
        lines.append(f"| {c['eval_name']} | {wo.get('overall_passed')} | {wi.get('overall_passed')} | "
                     f"{wo.get('expectations_passed',0)}/{wo.get('expectations_total',0)} | "
                     f"{wi.get('expectations_passed',0)}/{wi.get('expectations_total',0)} |")
    return "\n".join(lines) + "\n"


def render_review_html(b, per_case, ws):
    rows = []
    for c in per_case:
        wo = c.get("without_skill", {}); wi = c.get("with_skill", {})
        rows.append(
            f"<tr><td>{html.escape(str(c['case_id']))}</td><td>{html.escape(c['eval_name'])}</td>"
            f"<td>{wo.get('overall_passed')}</td><td>{wi.get('overall_passed')}</td>"
            f"<td>{wo.get('expectations_passed',0)}/{wo.get('expectations_total',0)}</td>"
            f"<td>{wi.get('expectations_passed',0)}/{wi.get('expectations_total',0)}</td>"
            f"<td>{wo.get('avg_elapsed_s','-')}</td><td>{wi.get('elapsed_s','-')}</td>"
            f"<td><a href=\"{html.escape(c['eval_name'])}/with_skill/grading.json\">with</a> / "
            f"<a href=\"{html.escape(c['eval_name'])}/without_skill/grading.json\">without</a></td></tr>")
    return f"""<!doctype html><html><head><meta charset="utf-8">
<title>Eval review — {html.escape(b['skill_name'])}</title>
<style>body{{font-family:system-ui,sans-serif;margin:2rem}}table{{border-collapse:collapse}}td,th{{border:1px solid #ccc;padding:6px 10px}}h2{{margin-top:2rem}}</style>
</head><body>
<h1>Eval review — {html.escape(b['skill_name'])} ({html.escape(b['route'])}, iteration {b['iteration']})</h1>
<p>Skill helps: <b>{b['skill_helps']}</b> (Δ expectations passed = {b['delta_expectations_passed']:+d})</p>
<table><tr><th>case</th><th>eval</th><th>without overall</th><th>with overall</th>
<th>without exp</th><th>with exp</th><th>without s</th><th>with s</th><th>grading</th></tr>
{''.join(rows)}
</table></body></html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skill")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--route", choices=list(ROUTES), default="gclaude")
    ap.add_argument("--iteration", type=int, default=1)
    ap.add_argument("--skills-root", default=str(DEFAULT_SKILLS_ROOT))
    ap.add_argument("--out-root", default=None,
                    help="Where to write <skill>-workspace trees. Defaults to skills-root. "
                         "Set to a persistent evidence dir if skills-root workspaces get cleaned.")
    ap.add_argument("--max-turns", type=int, default=6)
    ap.add_argument("--grade-turns", type=int, default=4)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    skills_root = pathlib.Path(args.skills_root)
    if args.all:
        skills = [p.name for p in sorted(skills_root.iterdir())
                  if (p / "evals" / "evals.json").exists() and not p.name.endswith("-workspace")]
    elif args.skill:
        skills = args.skill.split(",")
    else:
        ap.error("provide --skill or --all")
    print(f"route={args.route} iteration={args.iteration} max_turns={args.max_turns} "
          f"grade_turns={args.grade_turns} skills={skills}", flush=True)
    out_root = pathlib.Path(args.out_root) if args.out_root else None
    if out_root:
        out_root.mkdir(parents=True, exist_ok=True)
    for s in skills:
        eval_skill(s, args.route, args.iteration, skills_root, args.max_turns, args.grade_turns, args.dry_run, out_root)


if __name__ == "__main__":
    main()
