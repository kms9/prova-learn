# check-rubric — S4 / 决策门 G4（学习者前沿质量判定标准）

> 本量规是 `check-learner-frontier` 的判定标准，与阶段 skill `diagnose-learner-frontier/references/stage-contract.md` §6 保持一致。检查者独立重判，不采信被检工件自报的 `verdict`。

## 判定流程

1. 结构校验：信封通过 `handoff-envelope.schema.json`；`positive_artifact` 通过 `learner-snapshot.schema.json`。
2. 逐维判定下表（每维：证据 / 评分 / 阈值 / `passed`）。
3. 行为证据复核（`learner_behavior` 为 S4 唯一可采信诊断来源）。
4. 三项区分复核（答对 / 独立 / 迁移）。
5. 冷启动/阻塞态复核（不得强制为 pass，不得产出"全部未掌握"画像）。
6. 汇总裁决与路由。

## G4 维度量规

| 维度 | 阈值类型 | 通过阈值 | 证据来源（指向被检工件字段） |
|---|---|---|---|
| 测量与目标对齐度 | 关键节点均有对齐诊断项 | true | `node_states[]` ∩ `goal_success_contract` 能力与先修链 |
| 证据充分性 | 关键结论≥2 对齐观察或显式不足 | true | `diagnosis_evidence_mapping[]`、`evidence_collected`（`provenance=learner_behavior`） |
| 猜对识别 | 区分答对/独立/迁移 | true | `node_states[].error_type`、`node_states[].hint_dependency.level`、`transfer_performance.status` |
| 提示依赖记录 | 每节点 hint_dependency 已记录 | true | `node_states[].hint_dependency{level,evidence_refs}` |
| 错误分类一致性 | error_type 与证据一致，可审计 | true | `node_states[].error_type` ↔ `evidence_collected` 行为描述 |
| 偏差控制 | 自述/年限未覆盖行为证据 | true | `confidence_calibration`、`evidence_collected`（无 `user_provided_unverified` 计为掌握） |
| 结论可解释性 | 每条结论→证据可追溯 | true | `diagnosis_evidence_mapping[]`、`learning_frontier.evidence_refs` |

## 通过条件（G4 pass）

当且仅当**全部**满足：

- 所有上表维度 `passed=true`；
- 三项区分明确：`答对`（可能猜对或只识别口号）、`独立会做`（`hint_dependency.level ∈ {none, low}` 且无关键提示）、`能迁移`（`transfer_performance.status=demonstrated` 或在未见/变式情境通过）被分别标注；答对不得覆盖独立或迁移结论；
- 学习前沿（`learning_frontier`）有在 `evidence_validity.valid_until` 内的多项 `learner_behavior` 证据支撑；
- 冷启动/证据不足节点保持 `unknown`/`insufficient_evidence`/`untested`，**未**被坍缩为"全部未掌握"画像；
- 无 `criticality=critical` 且 `gate_effect=block` 的未决证据缺口。

通过 → `verdict=pass`、`route_to=S5`。

## 不通过时的路由

| 触发 | verdict | route_to |
|---|---|---|
| 证据不足、猜对未识别、提示/置信度缺失、争议节点未复测 | revise_here | S4 |
| 诊断题无法产生目标证据、图谱节点/先修边无效 | return_upstream | S3 |
| 诊断暴露来源缺失、偏差或图谱事实错误 | return_upstream | S2 或 S3（指向最早污染阶段） |
| 无真实学习者回答；冷启动待证；关键记录失效且无法补证 | blocked | S4 |

> S4 的 `return_upstream` 指向**最早**污染阶段（S2 图谱事实错误 / S3 节点或先修边无效），并记录失效下游范围。`revise_here` 与 `blocked` 的 `route_to` 均为 S4；区别在于缺陷是"当前证据可补"（revise_here）还是"无真实回答/记录失效且无法补证"（blocked）。

## 反模式（检查者不得犯）

- 直接采信被检工件自报 `verdict=pass` 而不逐维重判。
- 把 `model_hypothesis`、`user_provided_unverified`、自评或年限计为已掌握的行为证据。
- 把单题口号识别或纯自评映射为某节点的 `tested_mastered`。
- 冷启动时生成"全部未掌握"画像，或将 `unknown`/`insufficient_evidence`/`untested` 强制为 `pass`。
- 用"答对"覆盖"独立会做"或"能迁移"结论。
- 结构非法（`positive_artifact=null`）却仍给出 `pass`。
- 修改被检工件或替 S4 生成新快照、重新诊断学习者。
