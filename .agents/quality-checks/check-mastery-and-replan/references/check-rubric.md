# check-rubric — S7 / 决策门 G7（掌握验证与重规划质量判定标准）

> 本量规是 `check-mastery-and-replan` 的判定标准，与阶段 skill `verify-mastery-and-replan/references/stage-contract.md` §6–§7 保持一致。检查者独立重判，不采信被检工件自报的 `verdict`/`route`。G7 是**掌握门**：判定“掌握证据是否多维齐全 + 归因是否正确 + 版本化更新是否诚实 + 路由是否按确定性表”，而非内容质量门（G6）。

## 判定流程

1. 结构校验：信封通过 `handoff-envelope.schema.json`；`positive_artifact` 通过 `mastery-and-replanning-bundle.schema.json`（两段 `mastery_verification` + `learner_model_update_and_replan` 顺序与字段齐全，持久化操作 `load`/`append_evidence`/`update`/`history` 在位）。
2. 逐维判定下表（每维：证据 / 评分 / 阈值 / `passed`）。
3. 多维证据与掌握规则复核（单次结果不得记为高掌握；规则须先于测评确定）。
4. 归因与路由复核（按确定性路由表与上游优先级）。
5. 版本化更新复核（版本检查；`not_executed`/`version_conflict` 不得被强制为 `applied`/已掌握）。
6. 确认复核（S7 条件确认；跳过/重大变更/GOAL_ACHIEVED 须升级为强制并已解）。
7. 汇总裁决与路由（区分工件质量与学习者是否掌握）。

## G7 维度量规

| 维度 | 阈值类型 | 通过阈值 | 证据来源（指向被检工件字段） |
|---|---|---|---|
| 证据充分性 | 每节点六维证据齐（非单次结果） | true | `content.mastery_verification.node_mastery_evidence[]`（`correctness`/`reasoning_quality`/`hint_dependency`/`transfer`/`confidence`/`delayed_retention`） |
| 掌握规则一致性 | 判定与预设掌握规则一致（规则先于测评确定） | true | `content.mastery_verification.mastery_judgment[]` ↔ 预设节点掌握规则 |
| 提示影响控制 | 提示依赖被记录并计入判定 | true | `content.mastery_verification.node_mastery_evidence[].hint_dependency`（`level`/`detail`/`evidence_event_ids`） |
| 迁移与延迟证据 | 必要的近/远迁移与延迟保持已执行 | true | `content.mastery_verification.node_mastery_evidence[].transfer` + `delayed_retention` |
| 更新前后一致性 | 每项模型变更可追溯到新证据事件 | true | `content.learner_model_update_and_replan.model_patch[].evidence_event_ids` ↔ `append_evidence[]` |
| 调整可解释性 | 决策与归因匹配、路径调整有理由 | true | `content.learner_model_update_and_replan.decision` + `adjusted_path` + `model_patch[].rationale` ↔ `content.route.attribution` |
| 避免单次结果过度反应 | 不因一次正确即高掌握 | true | `content.mastery_verification.node_mastery_evidence[].confidence` + `mastery_judgment[]` |

## 通过条件（G7 各维度 `passed=true`）

当且仅当**全部**满足：

- 所有上表维度 `passed=true`；
- 每个待判节点具备多维证据（六维），**而非单一结果**；单题识别正确归为 `EVIDENCE_INSUFFICIENT`，绝不写成高掌握；
- 掌握规则在测评**之前**确定，判定与规则一致（不得用结果反推规则）；
- 每个关键模型变更（`model_patch[]`）可追溯到本次采集的新证据事件 ID；版本化更新经版本检查（`expected_model_version == load.current_model_version`）；
- 版本化更新诚实：`update_status` 为 `not_executed`/`version_conflict` 时未被强制为 `applied`/已掌握；冲突或未执行时掌握判定仍可记录，但不得声称已更新或已掌握；
- 下一步动作（`decision`/`adjusted_path`/`route`）与主归因匹配；
- 确认策略已满足（条件确认 `acknowledged` 即可；升级情形须 `confirmed`/`corrected`）；
- 无 `criticality=critical` 且 `gate_effect=block` 的未决证据缺口。

> **工件质量 ≠ 学习者掌握**：多维证据齐全、归因与路由正确、更新前后一致且版本检查诚实时，工件通过 G7；学习者未掌握不等于 S7 工件失败。`verdict` 与 `route_to` 由归因决定（见下表），而非由“是否前进”决定。

## 确定性返工与路由表（核对 `content.route`）

| 主归因代码 | 判定条件 | `route_to` | 对应 `verdict` |
|---|---|---|---|
| `EVIDENCE_INSUFFICIENT` | 缺少独立、迁移或延迟证据，无法满足预定掌握规则 | S7 | revise_here |
| `CONTENT_QUALITY` | 内容错误、来源不可追溯、示例或题目失效 | S6 | return_upstream |
| `STRATEGY_OR_SEQUENCE` | 内容正确，但难度、支架、顺序或节奏不适配 | S5 | return_upstream |
| `DIAGNOSTIC_ERROR` | 新证据与学习前沿假设冲突，且不能由单次波动解释 | S4 | return_upstream |
| `GRAPH_ERROR` | 先修边、节点粒度或评估映射错误 | S3 | return_upstream |
| `SOURCE_ERROR` | 图谱错误来自来源缺失、偏差或冲突未处理 | S2 | return_upstream |
| `GOAL_CHANGED` | 目标、成功标准、范围或约束发生实质变化 | S1 | return_upstream |
| `NODE_MASTERED` | 达到预设门槛且没有待完成的必要延迟检查 | S6 | pass |
| `GOAL_ACHIEVED` | 最终验收任务和整体保持要求均通过 | complete | pass |

存在多个归因时，按“**目标 → 来源 → 图谱 → 诊断 → 路径 → 内容 → 证据**”的上游优先级路由——先修复最早污染源，再重新验证下游工件。每次路由必须记录主归因、次要归因、证据和失效下游范围（至少 S6 起的下游）。

## 不通过时的汇总路由

| 触发 | verdict | route_to |
|---|---|---|
| 多维证据缺失、单次结果过度反应、规则事后反推（留在 S7 可补测修复） | revise_here | S7 |
| 主归因为 `CONTENT_QUALITY`/`STRATEGY_OR_SEQUENCE`/`DIAGNOSTIC_ERROR`/`GRAPH_ERROR`/`SOURCE_ERROR`/`GOAL_CHANGED`（工件质量通过或可记录，但路由上游） | return_upstream | 按上表（S6/S5/S4/S3/S2/S1） |
| 信封结构非法 / `positive_artifact=null` 且无法判定 / 版本更新被伪造为已应用 / 关键缺口未解 | blocked | S7 |

## 反模式（检查者不得犯）

- 直接采信被检工件自报 `verdict`/`route` 而不逐维重判、不核对路由表。
- 把单次识别正确当作多维掌握证据，或把 `transfer`/`delayed_retention = not_executed` 的节点写成已掌握。
- 把 `not_executed`/`version_conflict`/`partial`/`not_mastered` 强制为 `applied`/`pass`/已掌握。
- 用结果反推掌握规则（规则须先于测评确定）。
- 把内容质量问题（CONTENT_QUALITY→S6）记成学习者能力问题，或把学习者未掌握记成内容质量问题。
- 多归因时未按上游优先级取最早污染源（例如 primary=STRATEGY_OR_SEQUENCE 却误路由到 S7 而非 S5）。
- 把“学习者未掌握”等同于“S7 工件失败”，对正确路由上游的高质量工件错误地给 `revise_here`/`blocked`。
- 修改被检工件或替 S7 重判掌握、重写模型、补造证据或选路由。
