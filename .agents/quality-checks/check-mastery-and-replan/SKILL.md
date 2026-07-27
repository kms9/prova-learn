---
name: check-mastery-and-replan
description: 独立质量检查 skill，用于判定 S7（verify-mastery-and-replan）的输出工件是否达到决策门 G7。只要需要独立复核一个 mastery_and_replanning_bundle 移交信封是否合格——多维掌握证据是否齐全、归因是否正确、版本化更新是否诚实、确定性路由是否被遵循——就使用本 skill。它不重新判定掌握、不重写学习者模型、不替 S7 选路由；只按 G7 量规逐维复核并给出可追溯的 pass / revise_here / return_upstream / blocked 裁决。
---

# 掌握验证与重规划质量检查（check S7 / G7）

独立复核 S7 的输出是否达标。不要替 S7 重判掌握、重写模型或选路由；只读、只判。

## 开始前

1. 读取 [check-rubric.md](references/check-rubric.md)（G7 量规 = 判定标准）。
2. 读取 [quality-check-result.schema.json](references/quality-check-result.schema.json)（本检查的输出结构；与其它 check-* 共享同一份）。
3. 取待检 S7 移交信封；按需参考阶段 skill 的契约 `.agents/skills/verify-mastery-and-replan/references/stage-contract.md` 与两份 schema（`mastery-and-replanning-bundle.schema.json`、`handoff-envelope.schema.json`）。
4. 仅在需要理解输出形状时读取 [example.md](references/example.md)；案例为设计夹具。

## 执行

1. 结构校验：待检信封能否通过 `handoff-envelope.schema.json`；其 `positive_artifact` 能否通过 `mastery-and-replanning-bundle.schema.json`（两段 `mastery_verification` + `learner_model_update_and_replan` 顺序与字段齐全，持久化操作 `load`/`append_evidence`/`update`/`history` 在位）。任一不通过即记入 `structural_validation.errors`。
2. 逐维复核 G7（见 check-rubric.md）：证据充分性、掌握规则一致性、提示影响控制、迁移与延迟证据、更新前后一致性、调整可解释性、避免单次结果过度反应。每维给出证据、评分、阈值、`passed`。
3. 多维证据复核：每个待判节点须有 `correctness`/`reasoning_quality`/`hint_dependency`/`transfer`/`confidence`/`delayed_retention` 六维证据；单题识别正确不得记为高掌握。掌握规则须在测评**之前**确定（不得用结果反推规则）。
4. 归因与路由复核：按确定性路由表核对 `attribution.primary` 与 `route.route_to`（EVIDENCE_INSUFFICIENT→S7、CONTENT_QUALITY→S6、STRATEGY_OR_SEQUENCE→S5、DIAGNOSTIC_ERROR→S4、GRAPH_ERROR→S3、SOURCE_ERROR→S2、GOAL_CHANGED→S1、NODE_MASTERED→S6、GOAL_ACHIEVED→complete）；多归因按上游优先级“目标→来源→图谱→诊断→路径→内容→证据”取最早污染源。内容质量问题（CONTENT_QUALITY→S6）不得记成学习者能力问题。
5. 版本化更新复核：`update.expected_model_version` 须与 `load.current_model_version` 比对；不一致则 `update_status=version_conflict` 且不应用补丁；无真实后端或证据不足则 `update_status=not_executed`。`not_executed`/`version_conflict`/`partial`/`not_mastered` 不得被强制为 `pass` 或“已掌握”。每个 `model_patch` 须可追溯到新证据事件 ID。
6. 确认复核：S7 为条件确认；常规节点推进 `acknowledged` 即可，但跳过节点、重大路径变更、声称 GOAL_ACHIEVED 或与学习者就掌握结论存在分歧时须升级为强制并已解，否则 `blocking=true`。
7. 复核独立性：不得把 S7 自报的 `verdict`/`route` 当作结论；按本量规独立重判。
8. 汇总：区分“工件质量”与“学习者是否掌握”——多维证据齐全、归因与路由正确、更新前后一致且版本检查诚实时，工件可通过 G7，`verdict` 与 `route_to` 仍由归因决定（NODE_MASTERED/GOAL_ACHIEVED→`pass` 前进；EVIDENCE_INSUFFICIENT→`revise_here` 留 S7；其余归因→`return_upstream` 路由对应上游阶段）。存在结构性非法或关键缺口未解时给 `blocked`。

## Fail closed

- 待检信封结构非法且无法定位工件 → `verdict=blocked`，不臆造通过。
- 单次结果被写成高掌握、`transfer`/`delayed_retention` 为 `not_executed` 却声称已掌握 → 对应维度 `passed=false`。
- 版本冲突或未执行被静默改成 `applied`/已持久化 → 对应维度 `passed=false`。
- 内容质量问题被记成学习者能力问题，或学习者未掌握被记成内容质量问题 → 调整可解释性维度 `passed=false`。
- 只能给出复核结论与路由，不得修改被检工件、不得替 S7 重判掌握、重写模型或选路由。

## 输出

只输出符合 `quality-check-result.schema.json` 的 JSON：`stage_id=S7`、`gate_id=G7`、`dimension_results[]`、`verdict`、`route_to`、`evidence_summary`、`checked_at`。每个不通过维度必须带 `failure_action` 与 `route_to`。`verdict` 编码路由决策：`pass`=前进（S6/complete）、`revise_here`=留 S7 补测、`return_upstream`=路由至最早污染上游阶段、`blocked`=结构非法或关键缺口未解。
