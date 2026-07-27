---
name: check-learning-sessions
description: 独立质量检查 skill，用于判定 S5（plan-learning-sessions）的输出工件是否达到决策门 G5。只要需要独立复核 S5 的 learning_and_session_plan 是否达到门 G5、是否应该放行进入 S6，就使用本 skill。它不重新生成学习计划，只按 G5 量规逐维复核并给出可追溯的 pass / revise_here / return_upstream / blocked 裁决。
---

# 学习会话计划质量检查（check S5 / G5）

独立复核 S5 的输出是否达标。不要替 S5 重做计划；只读、只判。

## 开始前

1. 读取 [check-rubric.md](references/check-rubric.md)（G5 量规 = 判定标准）。
2. 读取 [quality-check-result.schema.json](references/quality-check-result.schema.json)（本检查的输出结构）。
3. 取待检 S5 移交信封；按需参考阶段 skill 的契约 `.agents/skills/plan-learning-sessions/references/stage-contract.md` 与两份 schema。
4. 仅在需要理解输出形状时读取 [example.md](references/example.md)；案例为设计夹具。

## 执行

1. 结构校验：待检信封能否通过 `handoff-envelope.schema.json`；其 `positive_artifact` 能否通过 `learning-and-session-plan.schema.json`。任一不通过即记入 `structural_validation.errors`。
2. 逐维复核 G5（见 check-rubric.md）：目标连通性、先修正确性、路径最小性、时间可行性、策略适配性、教学与测评对齐度、认知负荷、调整空间。每维给出证据、评分、阈值、`passed`。
3. 确认复核：S5 为强制确认；`confirmation.status` 非 `confirmed` 则 `blocking=true`，G5 不得通过。
4. 证据来源复核：计划假设不得被当作已证实学习前沿；`evidence_collected` 中标为 `model_hypothesis` 或 `user_provided_unverified` 的不得计为已证实诊断。
5. 复核独立性：不得把 S5 自报的 `verdict=pass` 当作结论；按本量规独立重判。
6. 汇总：所有维度 `passed` 且确认已解且无关键缺口 → `pass`、`route_to=S6`；否则按最早缺陷给 `revise_here`/`return_upstream`/`blocked` 与 `route_to`。

## Fail closed

- 待检信封结构非法且无法定位工件 → `verdict=blocked`，不臆造通过。
- 缺强制确认或起点非已证实学习前沿（用计划假设填充）→ 不得 `pass`。
- 复制课程目录、视频定额或题量，而无图谱、快照、退出规则者 → 对应维度 `passed=false`。
- 只能给出复核结论与路由，不得修改被检工件、不得替 S5 生成新计划。

## 输出

只输出符合 `quality-check-result.schema.json` 的 JSON：`stage_id=S5`、`gate_id=G5`、`dimension_results[]`、`verdict`、`route_to`、`evidence_summary`、`checked_at`。每个不通过维度必须带 `failure_action` 与 `route_to`。
