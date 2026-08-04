#!/usr/bin/env python3
"""Initialize a long-lived Prova Learn project-level LLM Wiki workspace."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import uuid
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_WORKSPACE_ROOT = REPO / "workspace"
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def event(
    *,
    event_id: str,
    event_type: str,
    project_id: str,
    conversation_id: str,
    occurred_at: str,
    payload: dict[str, object],
    resulting_revision: int | None,
) -> dict[str, object]:
    return {
        "schema_version": "1.0.0",
        "event_id": event_id,
        "event_type": event_type,
        "project_id": project_id,
        "conversation_id": conversation_id,
        "stage_id": "S1",
        "actor": "system",
        "occurred_at": occurred_at,
        "immutable": True,
        "expected_project_revision": None,
        "resulting_project_revision": resulting_revision,
        "provenance": "system_state",
        "refs": [],
        "payload": payload,
        "redaction": {"applied": False, "reason": None},
    }


def initialize(args: argparse.Namespace) -> Path:
    if not SLUG.fullmatch(args.project_slug):
        raise ValueError("project-slug must be lowercase kebab-case")

    workspace_root = args.workspace_root.resolve()
    project_dir = workspace_root / args.project_slug
    if project_dir.exists() and any(project_dir.iterdir()):
        raise FileExistsError(f"project workspace already exists and is not empty: {project_dir}")

    now = utc_now()
    occurred_at = now.isoformat().replace("+00:00", "Z")
    stamp = now.strftime("%Y%m%dT%H%M%SZ")
    suffix = uuid.uuid4().hex[:8]
    project_id = f"PRJ-{args.project_slug}"
    goal_id = f"GOAL-{args.project_slug}-v1"
    conversation_id = args.conversation_id or f"CONV-{stamp}-{suffix}"
    event_prefix = f"EVT-{stamp}-{suffix}"
    month = now.strftime("%Y-%m")

    required_dirs = [
        "conversations",
        "stages",
        "knowledge/evidence",
        "knowledge/concepts",
        "knowledge/misconceptions",
        "knowledge/methods",
        "learner",
        "plans",
        "sessions",
        "assessments",
        "decisions",
        "attachments",
        "_machine",
        "stages/s1-goal-contract/history",
    ]
    for rel in required_dirs:
        (project_dir / rel).mkdir(parents=True, exist_ok=True)

    stage_status = {
        stage: {
            "state": "in_progress" if stage == "S1" else "not_started",
            "gate": "not_evaluated",
            "route_to": "S1" if stage == "S1" else stage,
            "revision": 0,
            "entrypoint": "stages/s1-goal-contract/INDEX.md" if stage == "S1" else None,
        }
        for stage in [f"S{i}" for i in range(1, 8)]
    }
    state = {
        "schema_version": "1.0.0",
        "project_id": project_id,
        "project_slug": args.project_slug,
        "project_revision": 1,
        "status": "initializing",
        "current_stage": "S1",
        "route_to": "S1",
        "active_goal_id": goal_id,
        "active_goal_version": 1,
        "active_learner_model_version": None,
        "active_plan_id": None,
        "active_session_id": None,
        "last_conversation_id": conversation_id,
        "stage_status": stage_status,
        "updated_at": occurred_at,
        "updated_by_event_id": f"{event_prefix}-002",
    }
    write_json(project_dir / "project-state.json", state)

    write_text(
        project_dir / "INDEX.md",
        f"""# {args.project_title}

> 项目：`{project_id}`  
> 状态：`initializing`  
> 当前阶段：`S1`  
> 当前路由：`S1`  
> 项目版本：`1`  
> 最近更新：`{occurred_at}`

## 当前结论

项目工作区已创建，但目标、成功证据和范围尚未通过 S1 校准。当前任何能力、路径或掌握结论都不得视为已成立。

## 当前入口

- [项目说明](PROJECT.md)
- [项目状态](project-state.json)
- [时间线](timeline.md)
- [S1 目标校准](stages/s1-goal-contract/INDEX.md)
- [初始化会话](conversations/{month}/{conversation_id}/INDEX.md)

## 下一动作

进入 S1，记录学习诉求、使用场景与约束，执行外部预检并完成目标确认。
""",
    )
    write_text(
        project_dir / "PROJECT.md",
        f"""# 项目说明

- project_id：`{project_id}`
- project_slug：`{args.project_slug}`
- title：{args.project_title}
- learner_id：{args.learner_id or '尚未绑定'}
- created_at：`{occurred_at}`
- status：`initializing`

## 项目边界

当前仅建立项目容器。学习目标、目标场景、时间约束、资源约束、隐私边界和最终验收均处于待收集状态，不得由初始化脚本推断。

## 数据与历史策略

- Wiki 页面记录当前被接受版本。
- JSONL 记录不可变历史。
- 当前页面发生实质变化时保留历史版本和 supersedes 引用。
- 原始学习者回答不得为了美化而改写。
""",
    )
    write_text(project_dir / "timeline.md", f"# 项目时间线\n\n- `{occurred_at}` 创建项目工作区 `{project_id}`，进入 S1。")

    conv_dir = project_dir / "conversations" / month / conversation_id
    events = [
        event(
            event_id=f"{event_prefix}-001",
            event_type="conversation_started",
            project_id=project_id,
            conversation_id=conversation_id,
            occurred_at=occurred_at,
            payload={"purpose": "initialize_project_workspace", "project_title": args.project_title},
            resulting_revision=None,
        ),
        event(
            event_id=f"{event_prefix}-002",
            event_type="project_state_changed",
            project_id=project_id,
            conversation_id=conversation_id,
            occurred_at=occurred_at,
            payload={"from": None, "to": "initializing", "current_stage": "S1"},
            resulting_revision=1,
        ),
    ]
    write_jsonl(conv_dir / "events.jsonl", events)
    write_text(
        conv_dir / "INDEX.md",
        f"""# 初始化会话

- conversation_id：`{conversation_id}`
- project_id：`{project_id}`
- stage：`S1`
- started_at：`{occurred_at}`
- status：`closed`

## 文件

- [交互记录](transcript.md)
- [事件](events.jsonl)
- [会话总结](summary.md)

## 影响

创建项目根和 S1 初始化阶段，未形成任何已确认学习结论。
""",
    )
    write_text(
        conv_dir / "transcript.md",
        f"""# 交互记录

## `{occurred_at}` system

创建项目级 LLM Wiki 工作区。该动作只建立容器和版本 1 状态，没有代替用户定义学习目标。
""",
    )
    write_text(
        conv_dir / "summary.md",
        """# 会话总结

## 已完成

- 创建项目根、项目状态和时间线。
- 创建 S1 初始化阶段目录。
- 建立第一条不可变 conversation 事件链。

## 未完成

- 尚未收集学习诉求和场景。
- 尚未执行外部预检。
- G1 尚未评价。

## 下一动作

通过 S1 开始目标校准。
""",
    )

    s1 = project_dir / "stages" / "s1-goal-contract"
    write_text(
        s1 / "INDEX.md",
        f"""# S1 目标校准

> 状态：`in_progress`  
> Gate：`not_evaluated`  
> route_to：`S1`  
> project_revision：`1`

## 当前结论

尚未获得足够输入，不能建立目标契约或进入 S2。

## 页面

- [目标契约](goal-contract.md)
- [研究简报](research-brief.md)
- [证据表](evidence-table.md)
- [覆盖检查](coverage.md)
- [确认](confirmation.md)
- [Gate](gate.md)
- [验证](verification.md)

## 来源会话

- [`{conversation_id}`](../../conversations/{month}/{conversation_id}/INDEX.md)
""",
    )
    write_text(s1 / "working-notes.md", "# 工作记录\n\n当前仅记录：项目已初始化，尚无可接受的目标假设。")
    write_jsonl(s1 / "records.jsonl", [])
    write_text(s1 / "decisions.md", "# 决策记录\n\n尚无业务决策。项目初始化不等于目标确认。")
    write_text(s1 / "gate.md", "# G1 评价\n\n- verdict：`not_evaluated`\n- route_to：`S1`\n- reason：目标、证据和确认尚未收集。")
    write_text(s1 / "verification.md", "# S1 验证\n\n- state：`initializing`\n- project_revision：`1`\n- blockers：学习诉求、外部预检、能力、验收和确认均尚未执行。")
    write_text(s1 / "goal-contract.md", f"# 目标契约\n\n- goal_id：`{goal_id}`\n- version：`1`\n- status：`pending`\n\n尚未收集目标、场景、成功证据、范围、约束和排除项。")
    write_text(s1 / "research-brief.md", "# S2 研究简报\n\n状态：`pending`。S1 尚未形成经确认的研究问题和检索边界。")
    write_jsonl(s1 / "sources.jsonl", [])
    write_text(s1 / "evidence-table.md", "# 证据表\n\n当前没有 accepted external evidence，因此没有可进入主表的结论。")
    write_text(s1 / "coverage.md", "# 预检覆盖\n\n外部预检尚未执行，所有来源类别均为 `not_executed`，G1 不得通过。")
    write_jsonl(s1 / "capabilities.jsonl", [])
    write_jsonl(s1 / "terminology.jsonl", [])
    write_text(s1 / "confirmation.md", "# 目标确认\n\n- mode：`mandatory`\n- status：`pending`\n- reason：尚未向用户展示可确认的目标契约。")
    return project_dir


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_slug", help="Stable lowercase kebab-case project slug")
    parser.add_argument("--title", dest="project_title", required=True, help="Human-readable project title")
    parser.add_argument("--learner-id", default=None)
    parser.add_argument("--conversation-id", default=None)
    parser.add_argument("--workspace-root", type=Path, default=DEFAULT_WORKSPACE_ROOT)
    args = parser.parse_args()

    try:
        project_dir = initialize(args)
    except (ValueError, FileExistsError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(project_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
