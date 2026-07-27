---
name: check-goal-success-contract
description: 独立质量检查 skill，用于判定 S1（create-goal-success-contract）的输出工件是否达到决策门 G1。只要需要独立复核一个 goal_success_contract 移交信封是否合格、是否应该放行进入 S2，就使用本 skill。它不重新生成目标，只按 G1 量规逐维复核并给出可追溯的 pass / revise_here / return_upstream / blocked 裁决。
---

# 目标契约质量检查（check S1 / G1）

独立复核 S1 的输出是否达标。不要替 S1 重做目标；只读、只判。

## 开始前

1. 读取 [check-rubric.md](references/check-rubric.md)（G1 量规 = 判定标准）。
2. 读取 [quality-check-result.schema.json](references/quality-check-result.schema.json)（本检查的输出结构）。
3. 取待检 S1 移交信封；按需参考阶段 skill 的契约 `.agents/skills/create-goal-success-contract/references/stage-contract.md` 与两份 schema。
4. 仅在需要理解输出形状时读取 [example.md](references/example.md)；案例为设计夹具。

## 执行

1. 结构校验：待检信封能否通过 `handoff-envelope.schema.json`；其 `positive_artifact` 能否通过 `goal-success-contract.schema.json`。任一不通过即记入 `structural_validation.errors`。
2. 逐维复核 G1（见 check-rubric.md）：目标可观察性、成功标准可判定性、场景真实性、外部现实校准度、强制来源类别覆盖、边界清晰、约束完整、目标—验收一致。每维给出证据、评分、阈值、`passed`。
3. 确认复核：S1 为强制确认；`confirmation.status` 非 `confirmed`/`guardian_and_learner_confirmed` 则 `blocking=true`。
4. 证据来源复核：`model_hypothesis` 与 `user_provided_unverified` 不得被计为外部证据；`external_research_seed.search_executed` 必须为真且类别覆盖可审计。
5. 复核独立性：不得把 S1 自报的 `verdict=pass` 当作结论；按本量规独立重判。
6. 汇总：所有维度 `passed` 且确认已解且无关键缺口 → `pass`、`route_to=S2`；否则按最早缺陷给 `revise_here`/`return_upstream`/`blocked` 与 `route_to`。

## Fail closed

- 待检信封结构非法且无法定位工件 → `verdict=blocked`，不臆造通过。
- 缺强制确认或未执行联网预检 → 不得 `pass`。
- 证据来源被错标（模型记忆伪装成外部证据）→ 对应维度 `passed=false`。
- 只能给出复核结论与路由，不得修改被检工件、不得替 S1 生成新目标。

## 输出

只输出符合 `quality-check-result.schema.json` 的 JSON：`stage_id=S1`、`gate_id=G1`、`dimension_results[]`、`verdict`、`route_to`、`evidence_summary`、`checked_at`。每个不通过维度必须带 `failure_action` 与 `route_to`。
