#!/usr/bin/env python3
"""Record a fail-closed project transaction for an independent stage with missing prerequisites."""
from __future__ import annotations
import argparse, datetime as dt, json, shutil, sys, uuid
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / ".agents/stage-delivery-manifest.json"
STAGES = [f"S{i}" for i in range(2, 8)]

def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")

def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows), encoding="utf-8")

def collect_requirements(manifest: dict[str, Any], stage_id: str) -> list[dict[str, Any]]:
    collected: dict[str, dict[str, Any]] = {}
    def visit(current: str) -> None:
        for req in manifest["stages"][current].get("prerequisites", []):
            visit(req["stage"])
            collected[req["stage"]] = req
    visit(stage_id)
    return [collected[k] for k in sorted(collected, key=lambda x: int(x[1:]))]

def check(project: Path, state: dict[str, Any], req: dict[str, Any]) -> dict[str, Any]:
    status = state.get("stage_status", {}).get(req["stage"], {})
    entry = status.get("entrypoint")
    entry_ok = isinstance(entry, str) and (project / entry).is_file()
    passed = status.get("state") == "completed" and status.get("gate") == "pass" and entry_ok
    reason = "ready"
    if status.get("state", "not_started") == "not_started":
        reason = "stage_not_started"
    elif status.get("gate") != "pass":
        reason = f"gate_{status.get('gate', 'not_evaluated')}"
    elif not entry_ok:
        reason = "entrypoint_missing"
    return {"stage": req["stage"], "required_gate": req["gate"],
            "actual_state": status.get("state", "not_started"),
            "actual_gate": status.get("gate", "not_evaluated"),
            "entrypoint": entry, "entrypoint_exists": entry_ok,
            "passed": passed, "reason": reason}

def event(event_id: str, event_type: str, project_id: str, conversation_id: str,
          stage_id: str, when: str, revision: int, refs: list[str],
          payload: dict[str, Any], resulting: int | None = None) -> dict[str, Any]:
    return {"schema_version": "1.0.0", "event_id": event_id, "event_type": event_type,
            "project_id": project_id, "conversation_id": conversation_id,
            "stage_id": stage_id, "actor": "system", "occurred_at": when,
            "immutable": True, "expected_project_revision": revision,
            "resulting_project_revision": resulting, "provenance": "system_state",
            "refs": refs, "payload": payload,
            "redaction": {"applied": False, "reason": None}}

def archive(stage_dir: Path, stamp: str) -> str:
    stage_dir.mkdir(parents=True, exist_ok=True)
    existing = [p for p in stage_dir.iterdir() if p.name != "history"]
    if not existing:
        (stage_dir / "history").mkdir(exist_ok=True)
        return "none"
    target = stage_dir / "history" / f"before-prerequisite-block-{stamp}"
    target.mkdir(parents=True)
    for path in existing:
        shutil.move(str(path), target / path.name)
    return str(target.name)

def record(args: argparse.Namespace) -> Path:
    project = args.project_dir.resolve()
    state_path = project / "project-state.json"
    if not state_path.is_file():
        raise FileNotFoundError("project_missing: only S1 may create a project")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    state = json.loads(state_path.read_text(encoding="utf-8"))
    revision = state["project_revision"]
    if args.expected_revision is not None and args.expected_revision != revision:
        raise ValueError(f"version_conflict: expected {args.expected_revision}, current {revision}")

    cfg = manifest["stages"][args.stage]
    checks = [check(project, state, req) for req in collect_requirements(manifest, args.stage)]
    failed = [item for item in checks if not item["passed"]]
    if not failed:
        raise ValueError(f"{args.stage} prerequisites are satisfied; do not record a block")
    route = min((x["stage"] for x in failed), key=lambda x: int(x[1:]))

    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    when = now.isoformat().replace("+00:00", "Z")
    stamp = now.strftime("%Y%m%dT%H%M%SZ")
    suffix = uuid.uuid4().hex[:8]
    conversation_id = args.conversation_id or f"CONV-{stamp}-{suffix}"
    prefix = f"EVT-{stamp}-{suffix}"
    next_revision = revision + 1
    stage_dir = project / cfg["stage_dir"]
    archived = archive(stage_dir, stamp)

    rows = ["| Stage | Required | Actual state | Actual gate | Entry | Result | Reason |",
            "|---|---|---|---|---|---|---|"]
    for item in checks:
        rows.append(f"| {item['stage']} | {item['required_gate']} | {item['actual_state']} | "
                    f"{item['actual_gate']} | {item['entrypoint'] or '—'} | "
                    f"{'pass' if item['passed'] else 'fail'} | {item['reason']} |")
    write_text(stage_dir / "prerequisite-check.md",
        f"# {args.stage} 前置检查\n\n- status：`blocked`\n- route_to：`{route}`\n"
        f"- expected_project_revision：`{revision}`\n- resulting_project_revision：`{next_revision}`\n"
        f"- reason：{args.reason}\n- archived_previous_stage：`{archived}`\n\n" +
        "\n".join(rows) + f"\n\n## 恢复条件\n\n完成并通过 `{route}`，随后重新调用 {args.stage}。")

    all_files = manifest["common_stage_files"] + cfg["required_stage_files"]
    for filename in all_files:
        path = stage_dir / filename
        if filename == "prerequisite-check.md":
            continue
        if filename.endswith(".jsonl"):
            data = []
            if filename == "records.jsonl":
                data = [{"record_id": f"REC-{args.stage}-{stamp}-{suffix}",
                         "record_type": "prerequisite_block", "requested_stage": args.stage,
                         "route_to": route, "conversation_ref": conversation_id,
                         "project_revision": next_revision,
                         "missing_prerequisites": [x["stage"] for x in failed]}]
            write_jsonl(path, data)
        elif filename == "INDEX.md":
            write_text(path, f"# {args.stage} 独立调用阻断\n\n> 状态：`blocked`  \n"
                       f"> Gate：`blocked`  \n> route_to：`{route}`  \n"
                       f"> project_revision：`{next_revision}`\n\n"
                       "业务逻辑未执行。见 [前置检查](prerequisite-check.md)。")
        elif filename == "working-notes.md":
            write_text(path, f"# 工作记录\n\n前置失败，{args.stage} 业务未执行。")
        elif filename == "decisions.md":
            write_text(path, f"# 决策记录\n\n- decision：`block_independent_invocation`\n"
                       f"- requested_stage：`{args.stage}`\n- route_to：`{route}`")
        elif filename == "gate.md":
            write_text(path, f"# {cfg['gate']} 评价\n\n- verdict：`blocked`\n- route_to：`{route}`")
        elif filename == "verification.md":
            write_text(path, f"# {args.stage} 验证\n\n- state：`blocked`\n"
                       f"- project_revision：`{next_revision}`\n- business_execution：`not_executed`")
        else:
            write_text(path, f"# {filename.removesuffix('.md').replace('-', ' ').title()}\n\n"
                       f"- state：`not_executed`\n- route_to：`{route}`")

    month = now.strftime("%Y-%m")
    conv = project / "conversations" / month / conversation_id
    stage_entry = f"{cfg['stage_dir']}/INDEX.md"
    prereq_entry = f"{cfg['stage_dir']}/prerequisite-check.md"
    events = [
        event(f"{prefix}-001", "conversation_started", state["project_id"], conversation_id,
              args.stage, when, revision, [], {"purpose": "independent_stage_invocation"}),
        event(f"{prefix}-002", "gate_evaluated", state["project_id"], conversation_id,
              args.stage, when, revision, [prereq_entry],
              {"gate": cfg["gate"], "verdict": "blocked",
               "missing_prerequisites": [x["stage"] for x in failed]}),
        event(f"{prefix}-003", "route_decided", state["project_id"], conversation_id,
              args.stage, when, revision, [prereq_entry], {"route_to": route}),
        event(f"{prefix}-004", "project_state_changed", state["project_id"], conversation_id,
              args.stage, when, revision, [stage_entry],
              {"from_revision": revision, "to_revision": next_revision,
               "current_stage": route, "route_to": route}, next_revision),
        event(f"{prefix}-005", "conversation_closed", state["project_id"], conversation_id,
              args.stage, when, revision, [stage_entry], {"status": "blocked", "route_to": route})]
    write_jsonl(conv / "events.jsonl", events)
    write_text(conv / "INDEX.md", f"# {args.stage} 独立调用前置检查\n\n"
               f"- conversation_id：`{conversation_id}`\n- status：`blocked`\n- route_to：`{route}`\n\n"
               "- [交互](transcript.md)\n- [事件](events.jsonl)\n- [总结](summary.md)\n"
               f"- [阶段](../../../{stage_entry})")
    write_text(conv / "transcript.md", f"# 交互记录\n\n## `{when}` system\n\n"
               f"独立调用 `{args.stage}`，前置失败，业务未执行。route_to=`{route}`。")
    write_text(conv / "summary.md", f"# 会话总结\n\n- requested_stage：`{args.stage}`\n"
               f"- prerequisite_result：`fail`\n- route_to：`{route}`\n"
               f"- resulting_project_revision：`{next_revision}`")

    target = state.setdefault("stage_status", {}).setdefault(args.stage, {})
    target.update({"state": "blocked", "gate": "blocked", "route_to": route,
                   "revision": int(target.get("revision", 0)) + 1,
                   "entrypoint": stage_entry})
    state.update({"project_revision": next_revision, "status": "blocked",
                  "current_stage": route, "route_to": route,
                  "last_conversation_id": conversation_id, "updated_at": when,
                  "updated_by_event_id": f"{prefix}-004"})
    write_json(state_path, state)

    timeline = (project / "timeline.md").read_text(encoding="utf-8").rstrip()
    write_text(project / "timeline.md", timeline + f"\n\n- `{when}` 独立调用 `{args.stage}` "
               f"前置失败，revision `{revision} → {next_revision}`，route `{route}`。")
    root = (project / "INDEX.md").read_text(encoding="utf-8").rstrip()
    write_text(project / "INDEX.md", root + f"\n\n## 最近一次独立调用前置阻断\n\n"
               f"- requested_stage：`{args.stage}`\n- route_to：`{route}`\n"
               f"- conversation：`conversations/{month}/{conversation_id}/INDEX.md`\n"
               f"- project_revision：`{next_revision}`")
    return project

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", type=Path, required=True)
    parser.add_argument("--stage", choices=STAGES, required=True)
    parser.add_argument("--reason", default="independent invocation")
    parser.add_argument("--conversation-id")
    parser.add_argument("--expected-revision", type=int)
    try:
        print(record(parser.parse_args()))
    except (FileNotFoundError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
