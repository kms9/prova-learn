#!/usr/bin/env python3
"""Deterministically validate Prova Learn delivery contracts and workspaces.

The validator checks the repository-level project Wiki contract, stage metadata,
Skill naming, eval metadata, optional long-lived project workspaces, and legacy
S1/S2 run folders used as read-only migration inputs. It does not ask an LLM to
infer structural validity.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

REPO = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO / ".agents" / "stage-delivery-manifest.json"
FRONTMATTER_NAME = re.compile(r"(?m)^name:\s*([^\s]+)\s*$")
EXPECTED_STAGES = [f"S{i}" for i in range(1, 8)]
LEGACY_S1_FILES = [
    "INDEX.md",
    "sources.jsonl",
    "evidence_table.md",
    "coverage.md",
    "capabilities.jsonl",
    "terminology.jsonl",
    "goal-contract.md",
    "research-brief.md",
    "confirmation.md",
    "g1-evaluation.md",
    "verification.md",
]
LEGACY_S2_FILES = [
    "s2/INDEX.md",
    "s2/research-log.md",
    "s2/sources.jsonl",
    "s2/coverage.md",
    "s2/evidence-items.jsonl",
    "s2/research-answers.md",
    "s2/answer-validation.md",
    "s2/g2-evaluation.md",
    "s2/verification.md",
]


class ValidationError(Exception):
    pass


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        try:
            display = path.relative_to(REPO)
        except ValueError:
            display = path
        raise ValidationError(f"missing file: {display}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(f"invalid JSON: {path}:{exc.lineno}:{exc.colno}: {exc.msg}") from exc


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def unique(values: Iterable[str]) -> bool:
    data = list(values)
    return len(data) == len(set(data))


def eval_name_aliases(stage_id: str, cfg: dict[str, Any]) -> set[str]:
    directory_name = Path(cfg["skill_dir"]).name
    short_name = re.sub(rf"^s{stage_id[1:]}-", "", directory_name)
    callable_name = cfg["skill_name"]
    callable_short = re.sub(rf"^al-s{stage_id[1:]}-", "", callable_name)
    return {directory_name, short_name, callable_name, callable_short}


def validate_jsonl(path: Path, errors: list[str], require_immutable: bool = False) -> None:
    if not path.is_file():
        return
    seen_event_ids: set[str] = set()
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"invalid JSONL {path}:{lineno}: {exc.msg}")
            continue
        if not isinstance(item, dict):
            errors.append(f"JSONL item must be an object {path}:{lineno}")
            continue
        if require_immutable:
            require(item.get("immutable") is True, f"event must be immutable {path}:{lineno}", errors)
            event_id = item.get("event_id")
            require(isinstance(event_id, str) and event_id, f"event_id missing {path}:{lineno}", errors)
            if isinstance(event_id, str):
                require(event_id not in seen_event_ids, f"duplicate event_id {event_id} in {path}", errors)
                seen_event_ids.add(event_id)


def validate_manifest() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    manifest = load_json(MANIFEST_PATH)
    require(manifest.get("manifest_version") == "2.0.0", "manifest_version must be 2.0.0", errors)

    workspace = manifest.get("workspace")
    require(isinstance(workspace, dict), "manifest.workspace must be an object", errors)
    if isinstance(workspace, dict):
        require(workspace.get("delivery_type") == "project_llm_wiki", "workspace delivery_type must be project_llm_wiki", errors)
        for key in ("contract", "state_schema", "event_schema"):
            rel = workspace.get(key)
            require(isinstance(rel, str) and (REPO / rel).is_file(), f"workspace {key} is missing: {rel}", errors)
        files = workspace.get("required_files")
        dirs = workspace.get("required_directories")
        require(isinstance(files, list) and files, "workspace.required_files must be non-empty", errors)
        require(isinstance(dirs, list) and dirs, "workspace.required_directories must be non-empty", errors)
        conversation = workspace.get("conversation")
        require(isinstance(conversation, dict), "workspace.conversation must be an object", errors)
        if isinstance(conversation, dict):
            required = conversation.get("required_files")
            append_only = conversation.get("append_only_files")
            require(isinstance(required, list) and required, "conversation.required_files must be non-empty", errors)
            require(isinstance(append_only, list), "conversation.append_only_files must be an array", errors)
            if isinstance(required, list) and isinstance(append_only, list):
                require(set(append_only).issubset(required), "append-only conversation files must also be required", errors)

    common = manifest.get("common_stage_files")
    require(isinstance(common, list) and common, "common_stage_files must be non-empty", errors)
    if isinstance(common, list):
        require("INDEX.md" in common, "common_stage_files must include INDEX.md", errors)
        require("records.jsonl" in common, "common_stage_files must include records.jsonl", errors)
        require("gate.md" in common and "verification.md" in common, "common stage Gate files are required", errors)

    stages = manifest.get("stages")
    require(isinstance(stages, dict), "manifest.stages must be an object", errors)
    if not isinstance(stages, dict):
        return manifest, errors
    require(list(stages) == EXPECTED_STAGES, "manifest must define S1..S7 in order", errors)

    stage_dirs: list[str] = []
    for stage_id, cfg in stages.items():
        prefix = f"{stage_id}:"
        require(cfg.get("delivery_type") == "project_wiki_stage", f"{prefix} must use project_wiki_stage", errors)
        stage_dir_rel = cfg.get("stage_dir")
        require(isinstance(stage_dir_rel, str) and stage_dir_rel.startswith("stages/"), f"{prefix} invalid stage_dir", errors)
        if isinstance(stage_dir_rel, str):
            stage_dirs.append(stage_dir_rel)

        skill_dir = REPO / cfg.get("skill_dir", "")
        skill_md = skill_dir / "SKILL.md"
        require(skill_dir.is_dir(), f"{prefix} missing skill_dir {cfg.get('skill_dir')}", errors)
        require(skill_md.is_file(), f"{prefix} missing SKILL.md", errors)
        if skill_md.is_file():
            match = FRONTMATTER_NAME.search(skill_md.read_text(encoding="utf-8"))
            actual_name = match.group(1) if match else None
            require(actual_name == cfg.get("skill_name"), f"{prefix} SKILL name={actual_name!r}, manifest={cfg.get('skill_name')!r}", errors)

        eval_path = skill_dir / "evals" / "evals.json"
        require(eval_path.is_file(), f"{prefix} missing evals/evals.json", errors)
        if eval_path.is_file():
            evals = load_json(eval_path)
            accepted_names = eval_name_aliases(stage_id, cfg)
            require(evals.get("skill_name") in accepted_names, f"{prefix} eval skill_name drift: {evals.get('skill_name')!r}", errors)

        required_stage_files = cfg.get("required_stage_files")
        require(isinstance(required_stage_files, list) and required_stage_files, f"{prefix} required_stage_files must be non-empty", errors)
        if isinstance(common, list) and isinstance(required_stage_files, list):
            combined = common + required_stage_files
            require(unique(combined), f"{prefix} duplicate common/specific stage file", errors)
            require(cfg.get("entrypoint") in combined, f"{prefix} entrypoint must be required", errors)

        exports = cfg.get("compatibility_exports", [])
        require(isinstance(exports, list), f"{prefix} compatibility_exports must be an array", errors)
        if stage_id in {"S3", "S4", "S5", "S6", "S7"}:
            require(bool(exports), f"{prefix} should name legacy compatibility exports", errors)

    require(unique(stage_dirs), "stage_dir values must be unique", errors)
    require((REPO / ".agents" / "AGENTS.md").is_file(), ".agents/AGENTS.md is required", errors)
    require((REPO / "workspace" / "AGENTS.md").is_file(), "workspace/AGENTS.md is required", errors)
    return manifest, errors


def validate_project(manifest: dict[str, Any], project_dir: Path) -> list[str]:
    errors: list[str] = []
    workspace = manifest["workspace"]
    for rel in workspace["required_files"]:
        require((project_dir / rel).is_file(), f"project missing file: {rel}", errors)
    for rel in workspace["required_directories"]:
        require((project_dir / rel).is_dir(), f"project missing directory: {rel}", errors)

    state_path = project_dir / "project-state.json"
    if not state_path.is_file():
        return errors
    try:
        state = load_json(state_path)
    except ValidationError as exc:
        errors.append(str(exc))
        return errors

    require(state.get("schema_version") == "1.0.0", "project state schema_version must be 1.0.0", errors)
    require(isinstance(state.get("project_revision"), int) and state["project_revision"] >= 1, "project_revision must be >=1", errors)
    require(state.get("current_stage") in EXPECTED_STAGES, "current_stage is invalid", errors)
    require(state.get("route_to") in EXPECTED_STAGES + ["complete"], "route_to is invalid", errors)

    common = manifest["common_stage_files"]
    stage_status = state.get("stage_status", {})
    for stage_id, cfg in manifest["stages"].items():
        status = stage_status.get(stage_id, {}) if isinstance(stage_status, dict) else {}
        stage_state = status.get("state", "not_started")
        if stage_state == "not_started":
            continue
        stage_dir = project_dir / cfg["stage_dir"]
        require(stage_dir.is_dir(), f"{stage_id} started but stage directory is missing", errors)
        for rel in common + cfg["required_stage_files"]:
            require((stage_dir / rel).is_file(), f"{stage_id} missing stage file: {rel}", errors)

    conversation_root = project_dir / "conversations"
    conversation_dirs = []
    if conversation_root.is_dir():
        conversation_dirs = [p for p in conversation_root.glob("*/*") if p.is_dir()]
    require(bool(conversation_dirs), "project must contain at least one recorded conversation", errors)
    conversation_contract = workspace["conversation"]
    for conv_dir in conversation_dirs:
        for rel in conversation_contract["required_files"]:
            require((conv_dir / rel).is_file(), f"conversation missing {conv_dir / rel}", errors)
        validate_jsonl(conv_dir / "events.jsonl", errors, require_immutable=True)

    for jsonl in project_dir.rglob("*.jsonl"):
        if jsonl.name == "events.jsonl" and "conversations" in jsonl.parts:
            continue
        validate_jsonl(jsonl, errors)
    return errors


def validate_legacy_run(run_dir: Path) -> list[str]:
    errors: list[str] = []
    for rel in LEGACY_S1_FILES + LEGACY_S2_FILES:
        require((run_dir / rel).is_file(), f"legacy run missing: {rel}", errors)
    for jsonl in run_dir.rglob("*.jsonl"):
        validate_jsonl(jsonl, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", type=Path, help="Optional project-level LLM Wiki workspace to validate.")
    parser.add_argument(
        "--run-dir",
        "--legacy-run-dir",
        dest="legacy_run_dir",
        type=Path,
        help="Optional legacy S1/S2 run folder to validate as a read-only migration input.",
    )
    args = parser.parse_args()

    try:
        manifest, errors = validate_manifest()
    except ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.project_dir:
        project_dir = args.project_dir.resolve()
        if not project_dir.is_dir():
            errors.append(f"project directory does not exist: {project_dir}")
        else:
            errors.extend(validate_project(manifest, project_dir))

    if args.legacy_run_dir:
        legacy_run_dir = args.legacy_run_dir.resolve()
        if not legacy_run_dir.is_dir():
            errors.append(f"legacy run directory does not exist: {legacy_run_dir}")
        else:
            errors.extend(validate_legacy_run(legacy_run_dir))

    if errors:
        print("delivery contract validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("delivery contract validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
