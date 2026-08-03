#!/usr/bin/env python3
"""Validate the canonical Prova Learn stage-delivery contract.

This validator is intentionally deterministic. It checks repository structure,
Skill names, eval metadata, referenced schema/template assets, and optional
runtime run folders without asking an LLM to infer whether a delivery is valid.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO / ".agents" / "stage-delivery-manifest.json"
FRONTMATTER_NAME = re.compile(r"(?m)^name:\s*([^\s]+)\s*$")


class ValidationError(Exception):
    pass


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValidationError(f"missing file: {path.relative_to(REPO)}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(
            f"invalid JSON: {path.relative_to(REPO)}:{exc.lineno}:{exc.colno}: {exc.msg}"
        ) from exc


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate_manifest() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    manifest = load_json(MANIFEST_PATH)
    stages = manifest.get("stages")
    require(isinstance(stages, dict), "manifest.stages must be an object", errors)
    if not isinstance(stages, dict):
        return manifest, errors

    expected_stage_ids = [f"S{i}" for i in range(1, 8)]
    require(list(stages) == expected_stage_ids, "manifest must define S1..S7 in order", errors)

    for stage_id, cfg in stages.items():
        prefix = f"{stage_id}:"
        skill_dir = REPO / cfg.get("skill_dir", "")
        skill_md = skill_dir / "SKILL.md"
        require(skill_dir.is_dir(), f"{prefix} missing skill_dir {cfg.get('skill_dir')}", errors)
        require(skill_md.is_file(), f"{prefix} missing SKILL.md", errors)
        if skill_md.is_file():
            text = skill_md.read_text(encoding="utf-8")
            match = FRONTMATTER_NAME.search(text)
            actual_name = match.group(1) if match else None
            require(
                actual_name == cfg.get("skill_name"),
                f"{prefix} SKILL.md name={actual_name!r}, manifest={cfg.get('skill_name')!r}",
                errors,
            )

        eval_path = skill_dir / "evals" / "evals.json"
        require(eval_path.is_file(), f"{prefix} missing evals/evals.json", errors)
        if eval_path.is_file():
            evals = load_json(eval_path)
            accepted_names = {cfg.get("skill_name"), Path(cfg.get("skill_dir", "")).name}
            require(
                evals.get("skill_name") in accepted_names,
                f"{prefix} eval skill_name={evals.get('skill_name')!r} does not match {sorted(accepted_names)}",
                errors,
            )

        delivery_type = cfg.get("delivery_type")
        if delivery_type in {"run_folder", "nested_run_folder"}:
            files = cfg.get("required_files")
            require(isinstance(files, list) and files, f"{prefix} required_files must be non-empty", errors)
            require(cfg.get("entrypoint") in files, f"{prefix} entrypoint must be required", errors)
        elif delivery_type == "three_artifacts":
            artifacts = cfg.get("required_artifacts")
            require(
                artifacts == ["markdown", "json_envelope", "html_projection"],
                f"{prefix} three_artifacts contract is incomplete",
                errors,
            )
            require(bool(cfg.get("artifact_type")), f"{prefix} artifact_type is required", errors)
            for rel in (
                "references/markdown-output-contract.md",
                "references/handoff-envelope.schema.json",
                "references/html-visualization-contract.md",
                "assets/stage-report.html",
            ):
                require((skill_dir / rel).is_file(), f"{prefix} missing {rel}", errors)
        else:
            errors.append(f"{prefix} unsupported delivery_type={delivery_type!r}")

    return manifest, errors


def validate_run(manifest: dict[str, Any], run_dir: Path) -> list[str]:
    errors: list[str] = []
    stages = manifest["stages"]
    for stage_id in ("S1", "S2"):
        cfg = stages[stage_id]
        for rel in cfg["required_files"]:
            path = run_dir / rel
            require(path.is_file(), f"runtime {stage_id}: missing {path}", errors)

    for jsonl in run_dir.rglob("*.jsonl"):
        for lineno, line in enumerate(jsonl.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"runtime invalid JSONL {jsonl}:{lineno}: {exc.msg}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--run-dir",
        type=Path,
        help="Optional S1/S2 runtime run-folder to validate against the manifest.",
    )
    args = parser.parse_args()

    try:
        manifest, errors = validate_manifest()
    except ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.run_dir:
        run_dir = args.run_dir.resolve()
        if not run_dir.is_dir():
            errors.append(f"run directory does not exist: {run_dir}")
        else:
            errors.extend(validate_run(manifest, run_dir))

    if errors:
        print("delivery contract validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("delivery contract validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
