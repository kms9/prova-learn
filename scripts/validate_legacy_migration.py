#!/usr/bin/env python3
"""Validate an auditable legacy-run to project-Wiki migration."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", type=Path, required=True)
    parser.add_argument("--legacy-run-dir", type=Path, required=True)
    args = parser.parse_args()

    project = args.project_dir.resolve()
    legacy = args.legacy_run_dir.resolve()
    errors: list[str] = []

    migration_path = project / "_machine" / "migration-map.json"
    if not migration_path.is_file():
        fail(errors, f"missing migration map: {migration_path}")
    else:
        migration = load_json(migration_path)
        if migration.get("source_policy") != "read_only":
            fail(errors, "migration source_policy must be read_only")
        recorded_legacy = Path(str(migration.get("legacy_run_path", ""))).resolve()
        if recorded_legacy != legacy:
            fail(errors, f"legacy path mismatch: {recorded_legacy} != {legacy}")

        mappings = []
        for stage in ("s1", "s2"):
            value = migration.get(stage, [])
            if not isinstance(value, list):
                fail(errors, f"migration.{stage} must be an array")
                continue
            mappings.extend(value)

        if not mappings:
            fail(errors, "migration map contains no copied files")

        destination_paths: set[str] = set()
        for index, item in enumerate(mappings, 1):
            if not isinstance(item, dict):
                fail(errors, f"mapping {index} is not an object")
                continue
            source = Path(str(item.get("source_path", ""))).resolve()
            destination_rel = str(item.get("destination_path", ""))
            destination = project / destination_rel
            if destination_rel in destination_paths:
                fail(errors, f"duplicate destination mapping: {destination_rel}")
            destination_paths.add(destination_rel)
            if not source.is_file():
                fail(errors, f"source file missing after migration: {source}")
                continue
            if not destination.is_file():
                fail(errors, f"destination file missing: {destination}")
                continue
            source_hash = sha256(source)
            destination_hash = sha256(destination)
            if source_hash != item.get("source_sha256"):
                fail(errors, f"source hash mismatch: {source}")
            if destination_hash != item.get("destination_sha256"):
                fail(errors, f"destination hash mismatch: {destination}")
            if source_hash != destination_hash:
                fail(errors, f"copy is not byte-preserving: {source} -> {destination}")

    event_files = list((project / "conversations").glob("*/*/events.jsonl"))
    migrated_events: list[dict[str, Any]] = []
    for path in event_files:
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            event = json.loads(line)
            if event.get("event_type") == "artifact_migrated":
                migrated_events.append(event)
    if not any(event.get("stage_id") == "S1" for event in migrated_events):
        fail(errors, "missing S1 artifact_migrated event")
    if (legacy / "s2" / "INDEX.md").is_file() and not any(
        event.get("stage_id") == "S2" for event in migrated_events
    ):
        fail(errors, "legacy S2 exists but S2 artifact_migrated event is missing")

    state_path = project / "project-state.json"
    if not state_path.is_file():
        fail(errors, "missing project-state.json")
    else:
        state = load_json(state_path)
        if state.get("project_revision") != 2:
            fail(errors, "migration must advance the initialized project to revision 2")
        if state.get("last_conversation_id") is None:
            fail(errors, "migration state must reference the migration conversation")

    if errors:
        print("legacy migration validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("legacy migration validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
