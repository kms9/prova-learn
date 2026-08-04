#!/usr/bin/env python3
"""Current legacy migration entrypoint with project-Wiki prerequisite finalization."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from migrate_legacy_run_impl import DEFAULT_WORKSPACE_ROOT, migrate


def finalize_prerequisite_check(project_dir: Path) -> None:
    """Add the S2 prerequisite audit required by manifest 2.1.

    The migration does not re-evaluate G1. It records whether the migrated
    project state says the inherited S1/G1 contract is consumable.
    """
    s2_dir = project_dir / "stages" / "s2-domain-evidence"
    if not (s2_dir / "INDEX.md").is_file():
        return

    state = json.loads((project_dir / "project-state.json").read_text(encoding="utf-8"))
    s1 = state.get("stage_status", {}).get("S1", {})
    entrypoint = s1.get("entrypoint")
    entry_exists = isinstance(entrypoint, str) and (project_dir / entrypoint).is_file()
    passed = s1.get("state") == "completed" and s1.get("gate") == "pass" and entry_exists
    status = "pass" if passed else "blocked"
    route = "S2" if passed else "S1"
    reason = (
        "Migrated S1 is completed, G1 is pass, and the project entrypoint resolves. "
        "This audit inherits the legacy Gate; it does not re-run S1."
        if passed
        else "Migrated S1/G1 is not consumable; S2 must not continue until S1 is repaired."
    )
    migration_map = project_dir / "_machine" / "migration-map.json"
    content = f"""# S2 前置检查（迁移继承）

- status：`{status}`
- required_stage：`S1`
- required_gate：`G1`
- actual_state：`{s1.get('state', 'not_started')}`
- actual_gate：`{s1.get('gate', 'not_evaluated')}`
- entrypoint：`{entrypoint or 'missing'}`
- entrypoint_exists：`{str(entry_exists).lower()}`
- route_to：`{route}`
- project_revision：`{state.get('project_revision')}`
- migration_map：`{migration_map.relative_to(project_dir)}`

## 判定

{reason}

## 边界

- 本文件只审计迁移后 S2 的输入合同。
- 迁移没有重新执行外部预检、确认或 G1。
- 若旧 G1 不是 pass，当前 S2 业务记录只能作为历史材料，不能被下游消费。
"""
    (s2_dir / "prerequisite-check.md").write_text(content.rstrip() + "\n", encoding="utf-8")

    if not passed:
        s2_status = state.setdefault("stage_status", {}).setdefault("S2", {})
        s2_status.update({
            "state": "blocked",
            "gate": "blocked",
            "route_to": "S1",
            "entrypoint": "stages/s2-domain-evidence/INDEX.md",
        })
        state.update({"status": "blocked", "current_stage": "S1", "route_to": "S1"})
        (project_dir / "project-state.json").write_text(
            json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("legacy_run_dir", type=Path)
    parser.add_argument("--project-slug")
    parser.add_argument("--title")
    parser.add_argument("--workspace-root", type=Path, default=DEFAULT_WORKSPACE_ROOT)
    parser.add_argument("--conversation-id")
    args = parser.parse_args()
    try:
        project_dir = migrate(args)
        finalize_prerequisite_check(project_dir)
        print(project_dir)
    except (ValueError, FileExistsError, FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
