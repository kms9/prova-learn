---
name: check-learner-frontier
description: 独立质量检查 skill，用于判定 S4（diagnose-learner-frontier）的输出工件 learner_snapshot 是否达到决策门 G4。只要需要独立复核 S4 的 learner_snapshot 移交信封是否合格、是否应该放行进入 S5，就使用本 skill。它不重新诊断学习者，只按 G4 量规逐维复核并给出可追溯的 pass / revise_here / return_upstream / blocked 裁决。
---

# 学习者前沿质量检查（check S4 / G4）

独立复核 S4 的输出是否达标。不要替 S4 重做诊断；只读、只判。

## 开始前

1. 读取 [check-rubric.md](references/check-rubric.md)（G4 量规 = 判定标准）。
2. 读取共享 schema `quality-check-result.schema.json`（位于 `.agents/quality-checks/check-goal-success-contract/references/`，定义本检查的输出结构）。
3. 取待检 S4 移交信封；按需参考阶段 skill 的契约 `.agents/skills/diagnose-learner-frontier/references/stage-contract.md` 与 `learner-snapshot.schema.json`、`handoff-envelope.schema.json`。
4. 仅在需要理解输出形状时读取 [example.md](references/example.md)；案例为设计夹具。

## 执行

1. 结构校验：待检信封能否通过 `handoff-envelope.schema.json`；其 `positive_artifact` 能否通过 `learner-snapshot.schema.json`。任一不通过即记入 `structural_validation.errors`。
2. 逐维复核 G4（见 check-rubric.md）：测量与目标对齐度、证据充分性、猜对识别、提示依赖记录、错误分类一致性、偏差控制、结论可解释性。每维给出证据、评分、阈值、`passed`。
3. 行为证据复核：`learner_behavior` 是 S4 唯一可采信的诊断证据来源；`model_hypothesis`、`user_provided_unverified`、自评或年限不得被计为已掌握的行为证据。
4. 三项区分复核：独立确认 `答对`（可能猜对或只识别口号）、`独立会做`（`hint_dependency.level ∈ {none, low}`）、`能迁移`（未见/变式情境通过）被分别标注；答对不得覆盖独立或迁移结论。
5. 冷启动/阻塞态复核：`pending`/`blocked`/`unknown`/`insufficient_evidence`/`untested` 不得被强制为 `pass`；冷启动不得产出"全部未掌握"画像。
6. 复核独立性：不得把 S4 自报的 `verdict=pass` 当作结论；按本量规独立重判。
7. 汇总：所有维度 `passed=true` 且学习前沿有在有效期内的多项行为证据 → `pass`、`route_to=S5`；否则按最早缺陷给 `revise_here`/`return_upstream`/`blocked` 与 `route_to`。

## Fail closed

- 待检信封结构非法且无法定位工件 → `verdict=blocked`，不臆造通过。
- 无真实学习者回答、冷启动待证、或关键记录失效且无法补证 → 不得 `pass`。
- 自评/年限/单题口号识别被错标为 `tested_mastered` → 对应维度 `passed=false`。
- 只能给出复核结论与路由，不得修改被检工件、不得替 S4 生成新快照或重新诊断学习者。

## 输出

只输出符合 `quality-check-result.schema.json` 的 JSON：`stage_id=S4`、`gate_id=G4`、`dimension_results[]`、`verdict`、`route_to`、`evidence_summary`、`checked_at`。每个不通过维度必须带 `failure_action` 与 `route_to`。
