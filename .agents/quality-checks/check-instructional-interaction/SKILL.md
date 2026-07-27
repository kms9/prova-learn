---
name: check-instructional-interaction
description: 独立质量检查 skill，用于判定 S6（run-instructional-interaction）的输出工件 session_package_and_trace 是否达到决策门 G6（工件质量，非学习效果）。只要需要独立复核一个 S6 移交信封的教学工件是否合格、是否应该放行进入 S7，就使用本 skill。它不重新生成教学内容、不判定学习者是否掌握（掌握判定属于 G7），只按 G6 量规逐维复核并给出可追溯的 pass / revise_here / return_upstream / blocked 裁决。
---

# 教学交互质量检查（check S6 / G6）

独立复核 S6 的输出工件是否达标。不要替 S6 重做教学；只读、只判。G6 判定的是**工件质量**（内容正确性、支架、答案泄露控制、交互证据是否可被 S7 判定），**不是**学习者掌握程度——掌握判定留给 G7，本检查绝不得宣布学习者掌握。

## 开始前

1. 读取 [check-rubric.md](references/check-rubric.md)（G6 量规 = 判定标准）。
2. 读取 [quality-check-result.schema.json](../../check-goal-success-contract/references/quality-check-result.schema.json)（共享输出结构；本 skill 不自带副本）。
3. 取待检 S6 移交信封；按需参考阶段 skill 的契约 `.agents/skills/run-instructional-interaction/references/stage-contract.md` 与 `session-package-and-trace.schema.json`。
4. 仅在需要理解输出形状时读取 [example.md](references/example.md)；案例为设计夹具。

## 执行

1. 结构校验：待检信封能否通过 `handoff-envelope.schema.json`；其 `positive_artifact` 能否通过 `session-package-and-trace.schema.json`。任一不通过即记入 `structural_validation.errors`。
2. 逐维复核 G6（见 check-rubric.md）：内容正确性与可追溯性、对目标和学习者的适配、认知层级、例子代表性、支架质量、答案泄露控制、学习者主动性、交付可用性。每维给出证据、评分、阈值、`passed`。
3. 来源与泄露复核：每条 `explanations[].evidence_refs` 至少 1 条已审计来源；`model_hypothesis`/`user_provided_unverified` 不得计为内容来源；独立任务在提交前不得公布答案；提示不得代替学习者的关键推理。
4. 交互证据复核：`interaction_events[]` 须记录真实 `learner_behavior`（回答、提示层级、修正轨迹）；存在非空 `candidate_mastery_evidence`（候选，非掌握宣告）；学习者仅回复“懂了”或未作答不得代写证据。
5. 复核独立性：不得把 S6 自报的 `verdict=pass` 或学习者一句“懂了”当作结论；按本量规独立重判。
6. 汇总：所有维度 `passed=true` 且存在真实候选掌握证据 → `pass`、`route_to=S7`；否则按最早缺陷给 `revise_here`/`return_upstream`/`blocked` 与 `route_to`。

## Fail closed

- 待检信封结构非法且无法定位工件，或 `positive_artifact=null` → 不得 `pass`；视缺陷记 `revise_here`（可本阶段修复）或 `blocked`（无法继续）。
- 答案泄露、无独立作答、支架缺失或提示代替学习者推理 → 对应维度 `passed=false`，禁止进入 S7。
- 学习者未作答或仅“懂了” → 不得代写 `learner_behavior` 证据，不得生成有效掌握候选。
- 关键内容无可追溯来源 → `blocked` 或 `return_upstream`（S3/S2），不得用模型记忆替代审计证据。
- 只能给出复核结论与路由，不得修改被检工件、不得替 S6 生成新教学内容、不得宣布学习者掌握。

## 输出

只输出符合 `quality-check-result.schema.json` 的 JSON：`stage_id=S6`、`gate_id=G6`、`dimension_results[]`、`verdict`、`route_to`、`evidence_summary`、`checked_at`。每个不通过维度必须带 `failure_action` 与 `route_to`。
