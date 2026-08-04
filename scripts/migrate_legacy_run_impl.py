#!/usr/bin/env python3
"""Migrate a legacy S1/S2 run into a long-lived project-level LLM Wiki."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import sys
import uuid
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from init_project_workspace import initialize as initialize_project

REPO = Path(__file__).resolve().parents[1]
DEFAULT_WORKSPACE_ROOT = REPO / "workspace"
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ROUTES = [f"S{i}" for i in range(1, 8)] + ["complete"]
VERDICTS = ("pass", "revise_here", "return_upstream", "blocked", "pending", "not_evaluated")

S1_MAP = {
    "sources.jsonl": "sources.jsonl",
    "evidence_table.md": "evidence-table.md",
    "coverage.md": "coverage.md",
    "capabilities.jsonl": "capabilities.jsonl",
    "terminology.jsonl": "terminology.jsonl",
    "goal-contract.md": "goal-contract.md",
    "research-brief.md": "research-brief.md",
    "confirmation.md": "confirmation.md",
    "g1-evaluation.md": "gate.md",
    "verification.md": "verification.md",
}
S2_MAP = {
    "research-log.md": "research-log.md",
    "sources.jsonl": "sources.jsonl",
    "coverage.md": "coverage.md",
    "evidence-items.jsonl": "evidence-items.jsonl",
    "research-answers.md": "research-answers.md",
    "answer-validation.md": "answer-validation.md",
    "g2-evaluation.md": "gate.md",
    "verification.md": "verification.md",
}


def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def iso(value: dt.datetime) -> str:
    return value.isoformat().replace("+00:00", "Z")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def heading(path: Path) -> str | None:
    if not path.is_file():
        return None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def token(text: str, keys: tuple[str, ...], allowed: tuple[str, ...] | list[str]) -> str | None:
    choices = "|".join(re.escape(value) for value in allowed)
    for key in keys:
        for pattern in (
            rf"(?im)\b{re.escape(key)}\b\s*[：:=]\s*[`*]*({choices})",
            rf"(?im)\b{re.escape(key)}\b[^\n]{{0,24}}?[`*]({choices})[`*]",
        ):
            match = re.search(pattern, text)
            if match:
                return match.group(1)
    return None


def gate(stage_dir: Path, gate_id: str, default_route: str) -> tuple[str, str]:
    paths = [stage_dir / f"{gate_id.lower()}-evaluation.md", stage_dir / "INDEX.md"]
    text = "\n".join(path.read_text(encoding="utf-8") for path in paths if path.is_file())
    return (
        token(text, ("verdict", gate_id), VERDICTS) or "not_evaluated",
        token(text, ("route_to", "route"), ROUTES) or default_route,
    )


def state_for(verdict: str) -> str:
    return {
        "pass": "completed",
        "blocked": "blocked",
        "pending": "pending",
    }.get(verdict, "in_progress")


def copy_files(
    source_dir: Path,
    target_dir: Path,
    mapping: dict[str, str],
    project_dir: Path,
) -> list[dict[str, Any]]:
    result = []
    for source_name, target_name in mapping.items():
        source = source_dir / source_name
        if not source.is_file():
            raise FileNotFoundError(f"legacy input is missing: {source}")
        target = target_dir / target_name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        result.append(
            {
                "source_path": str(source.resolve()),
                "destination_path": str(target.relative_to(project_dir)),
                "source_sha256": sha256(source),
                "destination_sha256": sha256(target),
                "bytes": source.stat().st_size,
            }
        )
    return result


def indexed_records(run_id: str, files: list[tuple[Path, str]]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    index = 0
    for path, record_type in files:
        if not path.is_file():
            continue
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            payload = json.loads(line)
            index += 1
            legacy_id = next(
                (
                    str(payload[key])
                    for key in ("source_id", "capability_id", "term_id", "item_id", "id")
                    if isinstance(payload, dict) and payload.get(key)
                ),
                None,
            )
            records.append(
                {
                    "record_id": f"MIG-REC-{index:05d}",
                    "record_type": record_type,
                    "legacy_run_id": run_id,
                    "legacy_file": path.name,
                    "legacy_line": line_no,
                    "legacy_id": legacy_id,
                    "payload": payload,
                }
            )
    return records


def project_event(
    event_id: str,
    event_type: str,
    project_id: str,
    conversation_id: str,
    stage_id: str,
    occurred_at: str,
    refs: list[str],
    payload: dict[str, Any],
    expected_revision: int | None = 1,
    resulting_revision: int | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "event_id": event_id,
        "event_type": event_type,
        "project_id": project_id,
        "conversation_id": conversation_id,
        "stage_id": stage_id,
        "actor": "system",
        "occurred_at": occurred_at,
        "immutable": True,
        "expected_project_revision": expected_revision,
        "resulting_project_revision": resulting_revision,
        "provenance": "system_state",
        "refs": refs,
        "payload": payload,
        "redaction": {"applied": False, "reason": None},
    }


def stage_index(
    title: str,
    status: str,
    verdict: str,
    route: str,
    run_id: str,
    conversation_link: str,
    links: list[tuple[str, str]],
    history_link: str,
) -> str:
    pages = "\n".join(f"- [{label}]({path})" for label, path in links)
    return f"""# {title}

> 状态：`{status}`  
> Gate：`{verdict}`  
> route_to：`{route}`  
> migrated_from：`{run_id}`

## 当前页面

{pages}

## 来源会话

- [迁移会话]({conversation_link})

## 历史

- [旧 run 索引]({history_link})
"""


def migrate(args: argparse.Namespace) -> Path:
    legacy = args.legacy_run_dir.resolve()
    if not (legacy / "INDEX.md").is_file():
        raise FileNotFoundError(f"legacy S1 INDEX.md is missing: {legacy}")
    inferred = legacy.parent.parent.name if legacy.parent.name == "runs" else None
    slug = args.project_slug or inferred
    if not slug or not SLUG.fullmatch(slug):
        raise ValueError("provide --project-slug in lowercase kebab-case")
    title = args.title or heading(legacy / "INDEX.md") or slug
    workspace_root = args.workspace_root.resolve()
    project_dir = initialize_project(
        SimpleNamespace(
            project_slug=slug,
            project_title=title,
            learner_id=None,
            conversation_id=None,
            workspace_root=workspace_root,
        )
    )

    current_state = json.loads((project_dir / "project-state.json").read_text(encoding="utf-8"))
    if current_state["project_revision"] != 1:
        raise ValueError("initializer did not create expected project revision 1")

    now = now_utc()
    occurred_at = iso(now)
    stamp = now.strftime("%Y%m%dT%H%M%SZ")
    suffix = uuid.uuid4().hex[:8]
    conv_id = args.conversation_id or f"CONV-{stamp}-{suffix}"
    event_prefix = f"EVT-{stamp}-{suffix}"
    month = now.strftime("%Y-%m")
    project_id = current_state["project_id"]
    run_id = legacy.name
    has_s2 = (legacy / "s2" / "INDEX.md").is_file()
    g1_verdict, g1_route = gate(legacy, "G1", "S1")
    g2_verdict, g2_route = gate(legacy / "s2", "G2", "S2") if has_s2 else ("not_evaluated", "S2")

    s1 = project_dir / "stages/s1-goal-contract"
    s2 = project_dir / "stages/s2-domain-evidence"
    (s1 / "history").mkdir(parents=True, exist_ok=True)
    (s2 / "history").mkdir(parents=True, exist_ok=True)
    s1_map = copy_files(legacy, s1, S1_MAP, project_dir)
    old_s1_index = s1 / "history" / f"{run_id}-INDEX.md"
    shutil.copy2(legacy / "INDEX.md", old_s1_index)
    s1_map.append(
        {
            "source_path": str((legacy / "INDEX.md").resolve()),
            "destination_path": str(old_s1_index.relative_to(project_dir)),
            "source_sha256": sha256(legacy / "INDEX.md"),
            "destination_sha256": sha256(old_s1_index),
            "bytes": (legacy / "INDEX.md").stat().st_size,
        }
    )
    write_jsonl(
        s1 / "records.jsonl",
        indexed_records(
            run_id,
            [
                (legacy / "sources.jsonl", "legacy_source"),
                (legacy / "capabilities.jsonl", "legacy_capability"),
                (legacy / "terminology.jsonl", "legacy_terminology"),
            ],
        ),
    )
    write_text(
        s1 / "working-notes.md",
        f"""# S1 工作记录

旧 run `{run_id}` 已复制到项目 Wiki。迁移没有重新解释事实、改变证据等级或重新判定 G1。
""",
    )
    write_text(
        s1 / "decisions.md",
        f"""# S1 决策记录

## DEC-MIGRATE-S1

- legacy_run：`{legacy}`
- verdict：`{g1_verdict}`
- route_to：`{g1_route}`
- rule：旧 run 只读；后续更新只能通过项目 conversation 和 revision 事务。
""",
    )
    conv_rel = f"../../conversations/{month}/{conv_id}/INDEX.md"
    write_text(
        s1 / "INDEX.md",
        stage_index(
            "S1 目标校准",
            state_for(g1_verdict),
            g1_verdict,
            g1_route,
            run_id,
            conv_rel,
            [
                ("目标契约", "goal-contract.md"),
                ("研究简报", "research-brief.md"),
                ("来源", "sources.jsonl"),
                ("证据表", "evidence-table.md"),
                ("覆盖", "coverage.md"),
                ("能力", "capabilities.jsonl"),
                ("术语", "terminology.jsonl"),
                ("确认", "confirmation.md"),
                ("Gate", "gate.md"),
                ("验证", "verification.md"),
            ],
            f"history/{run_id}-INDEX.md",
        ),
    )

    s2_map: list[dict[str, Any]] = []
    if has_s2:
        s2_map = copy_files(legacy / "s2", s2, S2_MAP, project_dir)
        old_s2_index = s2 / "history" / f"{run_id}-s2-INDEX.md"
        shutil.copy2(legacy / "s2" / "INDEX.md", old_s2_index)
        s2_map.append(
            {
                "source_path": str((legacy / "s2" / "INDEX.md").resolve()),
                "destination_path": str(old_s2_index.relative_to(project_dir)),
                "source_sha256": sha256(legacy / "s2" / "INDEX.md"),
                "destination_sha256": sha256(old_s2_index),
                "bytes": (legacy / "s2" / "INDEX.md").stat().st_size,
            }
        )
        write_jsonl(
            s2 / "records.jsonl",
            indexed_records(
                run_id,
                [
                    (legacy / "s2" / "sources.jsonl", "legacy_source"),
                    (legacy / "s2" / "evidence-items.jsonl", "legacy_evidence_item"),
                ],
            ),
        )
        write_text(s2 / "working-notes.md", f"# S2 工作记录\n\n旧 `{run_id}/s2` 已迁移；没有重新执行研究。")
        write_text(
            s2 / "decisions.md",
            f"# S2 决策记录\n\n- verdict：`{g2_verdict}`\n- route_to：`{g2_route}`\n- migration：不补造旧缺口。",
        )
        write_text(
            s2 / "refresh-policy.md",
            """# 刷新策略

- state：`migration_review_required`
- 动态知识在下一次 S2 运行时重新核对日期、地区、标准和争议。
- 迁移不得把 partial/unanswered 自动升级为 answered。
""",
        )
        write_text(
            s2 / "INDEX.md",
            stage_index(
                "S2 领域取证",
                state_for(g2_verdict),
                g2_verdict,
                g2_route,
                f"{run_id}/s2",
                conv_rel,
                [
                    ("研究日志", "research-log.md"),
                    ("来源", "sources.jsonl"),
                    ("覆盖", "coverage.md"),
                    ("证据项", "evidence-items.jsonl"),
                    ("逐题回答", "research-answers.md"),
                    ("答案校验", "answer-validation.md"),
                    ("刷新策略", "refresh-policy.md"),
                    ("Gate", "gate.md"),
                    ("验证", "verification.md"),
                ],
                f"history/{run_id}-s2-INDEX.md",
            ),
        )

    if has_s2:
        current_stage = g2_route if g2_verdict == "pass" and g2_route.startswith("S") else "S2"
        route_to, controlling_verdict = g2_route, g2_verdict
    else:
        current_stage = "S2" if g1_verdict == "pass" else "S1"
        route_to, controlling_verdict = g1_route, g1_verdict
    project_status = "blocked" if controlling_verdict == "blocked" else "active"

    stage_status = current_state["stage_status"]
    stage_status["S1"] = {
        "state": state_for(g1_verdict),
        "gate": g1_verdict if g1_verdict in ("pass", "revise_here", "return_upstream", "blocked") else "not_evaluated",
        "route_to": g1_route,
        "revision": 1,
        "entrypoint": "stages/s1-goal-contract/INDEX.md",
    }
    if has_s2:
        stage_status["S2"] = {
            "state": state_for(g2_verdict),
            "gate": g2_verdict if g2_verdict in ("pass", "revise_here", "return_upstream", "blocked") else "not_evaluated",
            "route_to": g2_route,
            "revision": 1,
            "entrypoint": "stages/s2-domain-evidence/INDEX.md",
        }

    migration_map = {
        "schema_version": "1.0.0",
        "migration_id": f"MIG-{stamp}-{suffix}",
        "legacy_run_id": run_id,
        "legacy_run_path": str(legacy),
        "project_id": project_id,
        "project_slug": slug,
        "migrated_at": occurred_at,
        "source_policy": "read_only",
        "s1": s1_map,
        "s2": s2_map,
    }
    write_json(project_dir / "_machine/migration-map.json", migration_map)

    events = [
        project_event(
            f"{event_prefix}-001",
            "conversation_started",
            project_id,
            conv_id,
            "S1",
            occurred_at,
            [],
            {"purpose": "migrate_legacy_run", "legacy_run_id": run_id},
            expected_revision=1,
        ),
        project_event(
            f"{event_prefix}-002",
            "artifact_migrated",
            project_id,
            conv_id,
            "S1",
            occurred_at,
            ["stages/s1-goal-contract/INDEX.md", "_machine/migration-map.json"],
            {"legacy_run_id": run_id, "file_count": len(s1_map)},
            expected_revision=1,
        ),
    ]
    if has_s2:
        events.append(
            project_event(
                f"{event_prefix}-003",
                "artifact_migrated",
                project_id,
                conv_id,
                "S2",
                occurred_at,
                ["stages/s2-domain-evidence/INDEX.md", "_machine/migration-map.json"],
                {"legacy_run_id": run_id, "file_count": len(s2_map)},
                expected_revision=1,
            )
        )
    state_event = f"{event_prefix}-{'004' if has_s2 else '003'}"
    events.append(
        project_event(
            state_event,
            "project_state_changed",
            project_id,
            conv_id,
            current_stage,
            occurred_at,
            ["_machine/migration-map.json"],
            {"from_revision": 1, "to_revision": 2, "current_stage": current_stage, "route_to": route_to},
            expected_revision=1,
            resulting_revision=2,
        )
    )

    conv = project_dir / "conversations" / month / conv_id
    write_jsonl(conv / "events.jsonl", events)
    write_text(
        conv / "INDEX.md",
        f"""# 旧 run 迁移会话

- conversation_id：`{conv_id}`
- project_id：`{project_id}`
- status：`closed`

- [迁移原文](transcript.md)
- [迁移事件](events.jsonl)
- [会话总结](summary.md)
- [S1](../../../stages/s1-goal-contract/INDEX.md)
{"- [S2](../../../stages/s2-domain-evidence/INDEX.md)" if has_s2 else ""}
""",
    )
    write_text(
        conv / "transcript.md",
        f"""# 迁移原文

## `{occurred_at}` system

将旧 run `{legacy}` 复制到项目级 LLM Wiki。旧目录未被修改；迁移没有重新解释学习结论。

- S1 copied files：{len(s1_map)}
- S2 copied files：{len(s2_map)}
- route_to：`{route_to}`
""",
    )
    write_text(
        conv / "summary.md",
        f"""# 会话总结

- 已创建迁移映射与逐文件 SHA-256。
- 已写入 S1{"、S2" if has_s2 else ""} `artifact_migrated` 事件。
- G1：`{g1_verdict}` → `{g1_route}`
- G2：`{g2_verdict}` → `{g2_route}`
- 下一动作：按 `route_to={route_to}` 继续，禁止回写旧 run。
""",
    )

    state = current_state
    state.update(
        {
            "project_revision": 2,
            "status": project_status,
            "current_stage": current_stage,
            "route_to": route_to,
            "last_conversation_id": conv_id,
            "stage_status": stage_status,
            "updated_at": occurred_at,
            "updated_by_event_id": state_event,
        }
    )
    write_json(project_dir / "project-state.json", state)
    project_md = (project_dir / "PROJECT.md").read_text(encoding="utf-8").rstrip()
    write_text(
        project_dir / "PROJECT.md",
        project_md
        + f"""

## 迁移来源

- legacy_run：`{legacy}`
- legacy_policy：`read_only`
- migration_map：[`_machine/migration-map.json`](_machine/migration-map.json)
""",
    )
    timeline = (project_dir / "timeline.md").read_text(encoding="utf-8").rstrip()
    write_text(
        project_dir / "timeline.md",
        timeline
        + f"""

- `{occurred_at}` 迁移旧 run `{run_id}`，项目 revision `1 → 2`。
- `{occurred_at}` G1=`{g1_verdict}` → `{g1_route}`。
"""
        + (f"- `{occurred_at}` G2=`{g2_verdict}` → `{g2_route}`。\n" if has_s2 else ""),
    )
    write_text(
        project_dir / "decisions" / f"migration-{run_id}.md",
        f"""# 迁移决策

- migration_id：`{migration_map['migration_id']}`
- source：`{legacy}`
- source_policy：`read_only`
- map：[`../_machine/migration-map.json`](../_machine/migration-map.json)
- conversation：[`{conv_id}`](../conversations/{month}/{conv_id}/INDEX.md)
""",
    )
    write_text(
        project_dir / "INDEX.md",
        f"""# {title}

> 项目：`{project_id}`  
> 状态：`{project_status}`  
> 当前阶段：`{current_stage}`  
> 当前路由：`{route_to}`  
> 项目版本：`2`  
> 最近更新：`{occurred_at}`

## 当前结论

旧 run 已迁移为项目级 LLM Wiki。迁移没有改变旧证据等级或 Gate。

## 当前入口

- [项目说明](PROJECT.md)
- [项目状态](project-state.json)
- [时间线](timeline.md)
- [S1](stages/s1-goal-contract/INDEX.md)
{"- [S2](stages/s2-domain-evidence/INDEX.md)" if has_s2 else ""}
- [迁移会话](conversations/{month}/{conv_id}/INDEX.md)
- [迁移映射](_machine/migration-map.json)

## 下一动作

按 `route_to={route_to}` 继续；所有新交互写入项目 conversation。
""",
    )
    return project_dir


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("legacy_run_dir", type=Path)
    parser.add_argument("--project-slug")
    parser.add_argument("--title")
    parser.add_argument("--workspace-root", type=Path, default=DEFAULT_WORKSPACE_ROOT)
    parser.add_argument("--conversation-id")
    args = parser.parse_args()
    try:
        print(migrate(args))
    except (ValueError, FileExistsError, FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
