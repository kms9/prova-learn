#!/usr/bin/env python3
"""Deterministically validate Prova Learn project-Wiki contracts and workspaces."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

REPO = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO / ".agents/stage-delivery-manifest.json"
PROFILES_PATH = REPO / ".agents/stage-profiles.json"
ORCHESTRATOR_PATH = REPO / ".agents/skills/al-orchestrate-personalized-learning/SKILL.md"
FRONTMATTER_NAME = re.compile(r"(?m)^name:\s*([^\s]+)\s*$")
EXPECTED_STAGES = [f"S{i}" for i in range(1, 8)]
LEGACY_S1_FILES = [
    "INDEX.md", "sources.jsonl", "evidence_table.md", "coverage.md",
    "capabilities.jsonl", "terminology.jsonl", "goal-contract.md",
    "research-brief.md", "confirmation.md", "g1-evaluation.md", "verification.md",
]
LEGACY_S2_FILES = [
    "s2/INDEX.md", "s2/research-log.md", "s2/sources.jsonl", "s2/coverage.md",
    "s2/evidence-items.jsonl", "s2/research-answers.md", "s2/answer-validation.md",
    "s2/g2-evaluation.md", "s2/verification.md",
]

SKILL_MARKERS: dict[str, tuple[str, ...]] = {
    "S1": ("confirmed_fields", "unconfirmed_fields", "普通“继续”"),
    "S2": ("独立来源组", "高影响主张", "trace_only"),
    "S3": ("observable_indicator", "minimum_observations", "复合任务"),
    "S4": ("8–12 分钟", "tested_mastered", "synthetic_learner_behavior"),
    "S5": ("unknown 不等于未掌握", "撤架", "mandatory"),
    "S6": ("synthetic_learner_behavior", "答案泄露", "候选证据"),
    "S7": ("GOAL_ACHIEVED", "delayed_retention", "persistence=not_executed"),
}
ORCHESTRATOR_MARKERS = (
    "普通的“继续/下一步/跑完流程”",
    "synthetic_learner_behavior",
    "至少两项相互独立的观察",
    "GOAL_ACHIEVED",
)


class ValidationError(Exception):
    pass


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValidationError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(
            f"invalid JSON: {path}:{exc.lineno}:{exc.colno}: {exc.msg}"
        ) from exc


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def unique(values: Iterable[str]) -> bool:
    values = list(values)
    return len(values) == len(set(values))


def eval_aliases(stage_id: str, cfg: dict[str, Any]) -> set[str]:
    directory = Path(cfg["skill_dir"]).name
    short = re.sub(rf"^s{stage_id[1:]}-", "", directory)
    callable_name = cfg["skill_name"]
    callable_short = re.sub(rf"^al-s{stage_id[1:]}-", "", callable_name)
    return {directory, short, callable_name, callable_short}


def iter_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from iter_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from iter_strings(item)


def is_simulation_path(path: Path) -> bool:
    return "simulations" in path.parts


def validate_jsonl(path: Path, errors: list[str], immutable: bool = False) -> None:
    if not path.is_file():
        return
    seen: set[str] = set()
    simulation = is_simulation_path(path)
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"invalid JSONL {path}:{line_no}: {exc.msg}")
            continue
        if not isinstance(item, dict):
            errors.append(f"JSONL item must be object {path}:{line_no}")
            continue
        if immutable:
            require(
                item.get("immutable") is True,
                f"event must be immutable {path}:{line_no}",
                errors,
            )
            event_id = item.get("event_id")
            require(
                isinstance(event_id, str) and bool(event_id),
                f"event_id missing {path}:{line_no}",
                errors,
            )
            if isinstance(event_id, str):
                require(
                    event_id not in seen,
                    f"duplicate event_id {event_id} in {path}",
                    errors,
                )
                seen.add(event_id)

        provenance = item.get("provenance")
        if not simulation:
            require(
                provenance != "synthetic_learner_behavior",
                f"synthetic learner evidence outside simulations {path}:{line_no}",
                errors,
            )
            strings = list(iter_strings(item))
            require(
                not any("simulations/" in value or "/simulations/" in value for value in strings),
                f"real project record references simulations {path}:{line_no}",
                errors,
            )
            require(
                not any(value == "simulated_fixture" for value in strings),
                f"fixture metadata outside simulations {path}:{line_no}",
                errors,
            )


def validate_skill_markers(
    stage_id: str, skill_md: Path, text: str, errors: list[str]
) -> None:
    for marker in SKILL_MARKERS.get(stage_id, ()):
        require(
            marker in text,
            f"{stage_id}: learning-validity marker missing in {skill_md}: {marker}",
            errors,
        )


def validate_manifest() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    manifest = load_json(MANIFEST_PATH)
    require(
        manifest.get("manifest_version") == "2.1.0",
        "manifest_version must be 2.1.0",
        errors,
    )
    workspace = manifest.get("workspace")
    require(isinstance(workspace, dict), "manifest.workspace must be object", errors)
    if isinstance(workspace, dict):
        require(
            workspace.get("delivery_type") == "project_llm_wiki",
            "workspace delivery_type invalid",
            errors,
        )
        for key in ("contract", "standalone_contract", "state_schema", "event_schema"):
            rel = workspace.get(key)
            require(
                isinstance(rel, str) and (REPO / rel).is_file(),
                f"workspace {key} missing: {rel}",
                errors,
            )
        required = workspace.get("conversation", {}).get("required_files", [])
        append_only = workspace.get("conversation", {}).get("append_only_files", [])
        require(bool(required), "conversation required files missing", errors)
        require(
            set(append_only).issubset(required),
            "append-only conversation files must be required",
            errors,
        )

    common = manifest.get("common_stage_files")
    require(isinstance(common, list) and bool(common), "common_stage_files missing", errors)
    if isinstance(common, list):
        for name in ("INDEX.md", "records.jsonl", "gate.md", "verification.md"):
            require(name in common, f"common stage file missing: {name}", errors)

    stages = manifest.get("stages")
    require(isinstance(stages, dict), "manifest.stages must be object", errors)
    if not isinstance(stages, dict):
        return manifest, errors
    require(list(stages) == EXPECTED_STAGES, "manifest must define S1..S7 in order", errors)

    require(PROFILES_PATH.is_file(), "stage-profiles.json is required", errors)
    profiles_doc = load_json(PROFILES_PATH) if PROFILES_PATH.is_file() else {}
    require(
        profiles_doc.get("schema_version") == "1.1.0",
        "stage-profiles schema_version must be 1.1.0",
        errors,
    )
    profiles = profiles_doc.get("stages", {}) if isinstance(profiles_doc, dict) else {}

    seen_dirs: list[str] = []
    for stage_id, cfg in stages.items():
        prefix = f"{stage_id}:"
        profile = profiles.get(stage_id, {}) if isinstance(profiles, dict) else {}
        require(profile.get("stage_id") == stage_id, f"{prefix} stage profile missing", errors)
        require(profile.get("gate") == cfg.get("gate"), f"{prefix} profile gate mismatch", errors)
        require(
            profile.get("stage_dir") == cfg.get("stage_dir"),
            f"{prefix} profile stage_dir mismatch",
            errors,
        )
        require(
            profile.get("prerequisites") == cfg.get("prerequisites"),
            f"{prefix} profile prerequisites mismatch",
            errors,
        )
        require(
            profile.get("required_stage_files") == cfg.get("required_stage_files"),
            f"{prefix} profile required files mismatch",
            errors,
        )
        require(
            isinstance(profile.get("business_rules"), list) and profile["business_rules"],
            f"{prefix} profile business_rules missing",
            errors,
        )
        require(
            isinstance(profile.get("fail_closed"), list) and profile["fail_closed"],
            f"{prefix} profile fail_closed missing",
            errors,
        )
        require(
            cfg.get("delivery_type") == "project_wiki_stage",
            f"{prefix} wrong delivery_type",
            errors,
        )
        stage_dir = cfg.get("stage_dir")
        require(
            isinstance(stage_dir, str) and stage_dir.startswith("stages/"),
            f"{prefix} invalid stage_dir",
            errors,
        )
        if isinstance(stage_dir, str):
            seen_dirs.append(stage_dir)

        skill_dir = REPO / cfg.get("skill_dir", "")
        skill_md = skill_dir / "SKILL.md"
        require(skill_md.is_file(), f"{prefix} missing SKILL.md", errors)
        if skill_md.is_file():
            text = skill_md.read_text(encoding="utf-8")
            match = FRONTMATTER_NAME.search(text)
            actual = match.group(1) if match else None
            require(
                actual == cfg.get("skill_name"),
                f"{prefix} skill name drift: {actual}",
                errors,
            )
            validate_skill_markers(stage_id, skill_md, text, errors)

        eval_path = skill_dir / "evals/evals.json"
        require(eval_path.is_file(), f"{prefix} missing evals", errors)
        if eval_path.is_file():
            evals = load_json(eval_path)
            require(
                evals.get("skill_name") in eval_aliases(stage_id, cfg),
                f"{prefix} eval skill_name drift",
                errors,
            )

        specific = cfg.get("required_stage_files")
        require(
            isinstance(specific, list) and bool(specific),
            f"{prefix} required_stage_files missing",
            errors,
        )
        if isinstance(common, list) and isinstance(specific, list):
            require(unique(common + specific), f"{prefix} duplicate common/specific file", errors)
            require(
                cfg.get("entrypoint") in common + specific,
                f"{prefix} entrypoint not required",
                errors,
            )

        prerequisites = cfg.get("prerequisites")
        require(isinstance(prerequisites, list), f"{prefix} prerequisites must be array", errors)
        seen_req: set[str] = set()
        if isinstance(prerequisites, list):
            for req in prerequisites:
                require(isinstance(req, dict), f"{prefix} prerequisite must be object", errors)
                if not isinstance(req, dict):
                    continue
                req_stage = req.get("stage")
                require(req_stage in EXPECTED_STAGES, f"{prefix} invalid prerequisite {req_stage}", errors)
                if req_stage in EXPECTED_STAGES:
                    require(
                        int(req_stage[1:]) < int(stage_id[1:]),
                        f"{prefix} prerequisite must be earlier",
                        errors,
                    )
                    require(
                        req_stage not in seen_req,
                        f"{prefix} duplicate prerequisite {req_stage}",
                        errors,
                    )
                    seen_req.add(req_stage)
                    require(
                        req.get("gate") == f"G{req_stage[1:]}",
                        f"{prefix} prerequisite gate mismatch",
                        errors,
                    )
                    require(
                        req.get("state") == "completed",
                        f"{prefix} prerequisite state must be completed",
                        errors,
                    )
        if stage_id == "S1":
            require(prerequisites == [], "S1 must have no prerequisites", errors)
        else:
            require(
                "prerequisite-check.md" in (specific or []),
                f"{prefix} prerequisite-check.md required",
                errors,
            )
        if stage_id in {"S3", "S4", "S5", "S6", "S7"}:
            require(
                bool(cfg.get("compatibility_exports")),
                f"{prefix} compatibility exports missing",
                errors,
            )

    require(unique(seen_dirs), "stage directories must be unique", errors)

    require(ORCHESTRATOR_PATH.is_file(), "orchestrator SKILL.md missing", errors)
    if ORCHESTRATOR_PATH.is_file():
        orchestrator = ORCHESTRATOR_PATH.read_text(encoding="utf-8")
        for marker in ORCHESTRATOR_MARKERS:
            require(
                marker in orchestrator,
                f"orchestrator learning-validity marker missing: {marker}",
                errors,
            )

    for path in (
        REPO / ".agents/AGENTS.md",
        REPO / "workspace/AGENTS.md",
        REPO / "scripts/record_prerequisite_block.py",
        REPO / ".agents/stage-runtime-contract.md",
    ):
        require(path.is_file(), f"required shared file missing: {path.relative_to(REPO)}", errors)

    return manifest, errors


def validate_project(manifest: dict[str, Any], project: Path) -> list[str]:
    errors: list[str] = []
    workspace = manifest["workspace"]
    for rel in workspace["required_files"]:
        require((project / rel).is_file(), f"project missing file: {rel}", errors)
    for rel in workspace["required_directories"]:
        require((project / rel).is_dir(), f"project missing directory: {rel}", errors)

    state_path = project / "project-state.json"
    if not state_path.is_file():
        return errors
    state = load_json(state_path)
    require(state.get("schema_version") == "1.0.0", "project state schema_version invalid", errors)
    require(
        isinstance(state.get("project_revision"), int) and state["project_revision"] >= 1,
        "project_revision invalid",
        errors,
    )
    require(state.get("current_stage") in EXPECTED_STAGES, "current_stage invalid", errors)
    require(
        state.get("route_to") in EXPECTED_STAGES + ["complete"],
        "route_to invalid",
        errors,
    )
    require(
        not any("simulations/" in value or "/simulations/" in value for value in iter_strings(state)),
        "project-state must not reference simulations",
        errors,
    )

    common = manifest["common_stage_files"]
    statuses = state.get("stage_status", {}) if isinstance(state.get("stage_status"), dict) else {}
    for stage_id, cfg in manifest["stages"].items():
        status = statuses.get(stage_id, {})
        stage_state = status.get("state", "not_started") if isinstance(status, dict) else "not_started"
        if stage_state == "not_started":
            continue
        stage_dir = project / cfg["stage_dir"]
        require(stage_dir.is_dir(), f"{stage_id} started but directory missing", errors)
        for rel in common + cfg["required_stage_files"]:
            require((stage_dir / rel).is_file(), f"{stage_id} missing stage file: {rel}", errors)
        for jsonl in stage_dir.glob("*.jsonl"):
            validate_jsonl(jsonl, errors)
        if stage_state == "completed":
            require(status.get("gate") == "pass", f"{stage_id} completed but gate != pass", errors)
            for req in cfg.get("prerequisites", []):
                req_status = statuses.get(req["stage"], {})
                require(
                    req_status.get("state") == "completed",
                    f"{stage_id}: {req['stage']} not completed",
                    errors,
                )
                require(
                    req_status.get("gate") == "pass",
                    f"{stage_id}: {req['stage']} gate not pass",
                    errors,
                )
                entry = req_status.get("entrypoint")
                require(
                    isinstance(entry, str) and (project / entry).is_file(),
                    f"{stage_id}: prerequisite entry missing",
                    errors,
                )
        if stage_state == "blocked" and stage_id != "S1":
            require(
                (stage_dir / "prerequisite-check.md").is_file(),
                f"{stage_id} blocked without prerequisite check",
                errors,
            )
            require(status.get("gate") == "blocked", f"{stage_id} blocked but gate not blocked", errors)

    root = project / "conversations"
    conversations = [p for p in root.glob("*/*") if p.is_dir()] if root.is_dir() else []
    require(bool(conversations), "project must contain conversation", errors)
    ids: set[str] = set()
    for conv in conversations:
        ids.add(conv.name)
        for rel in workspace["conversation"]["required_files"]:
            require((conv / rel).is_file(), f"conversation missing {conv / rel}", errors)
        validate_jsonl(conv / "events.jsonl", errors, immutable=True)
    require(state.get("last_conversation_id") in ids, "last_conversation_id cannot be resolved", errors)

    for jsonl in project.rglob("*.jsonl"):
        if jsonl.name == "events.jsonl" and "conversations" in jsonl.parts:
            continue
        validate_jsonl(jsonl, errors)
    return errors


def validate_legacy(run: Path) -> list[str]:
    errors: list[str] = []
    for rel in LEGACY_S1_FILES + LEGACY_S2_FILES:
        require((run / rel).is_file(), f"legacy run missing: {rel}", errors)
    for jsonl in run.rglob("*.jsonl"):
        validate_jsonl(jsonl, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", type=Path)
    parser.add_argument("--run-dir", "--legacy-run-dir", dest="legacy_run_dir", type=Path)
    args = parser.parse_args()
    try:
        manifest, errors = validate_manifest()
    except ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if args.project_dir:
        project = args.project_dir.resolve()
        errors.extend(
            validate_project(manifest, project)
            if project.is_dir()
            else [f"project directory does not exist: {project}"]
        )
    if args.legacy_run_dir:
        run = args.legacy_run_dir.resolve()
        errors.extend(
            validate_legacy(run)
            if run.is_dir()
            else [f"legacy run directory does not exist: {run}"]
        )
    if errors:
        print("delivery contract validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("delivery contract validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
