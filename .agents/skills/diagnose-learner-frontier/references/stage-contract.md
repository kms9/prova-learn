# S4 阶段契约 — diagnose-learner-frontier（门 G4）

> 本文件治 S4 与决策门 G4。§0 为七阶段共享规则；其余为 S4 专属。

## 0. 共享阶段契约（适用于 S1–S7）

每个阶段产出**恰好一个**移交信封（`handoff-envelope.schema.json`），并遵循统一执行形状：

```text
校验输入契约
→ 收集需求缺口
→ 执行本阶段确认策略
→ 收集可采信证据
→ 生成具名正向工件
→ 用本阶段专属量规评价
→ 给出 pass / revise_here / return_upstream 与 route_to
```

- **输入契约校验**：至少检查工件类型、schema 版本、必填字段、来源阶段、追溯与上游门状态。失败时 `input_validation.status=fail` 并路由上游，**不得伪造正向工件**。
- **确认状态机**：`mandatory`（S1/S5，未确认不得前进）、`conditional`（S2/S3/S4/S7，遇高风险/分歧/多方案升级为强制）、`inform`（S6 节点推进，告知后继续）。
- **证据来源分类**：`model_hypothesis`/`market_signal`/`external_evidence`/`user_provided_unverified`/`learner_behavior`。**门不得把 `model_hypothesis` 或 `user_provided_unverified` 计为外部证据。**
- **量规结果形状**：`{dimension, evidence[], score, threshold, passed, failure_action, route_to}`；`passed=false` 时 `failure_action` 与 `route_to` 必填。
- **显式未知/阻塞态**：`pending`/`blocked`/`unknown`/`evidence_insufficient`/`research_blocked`/`not_executed`/`version_conflict` 不得被强制为 `pass`。
- **确定性路由**：`pass` 前进；`revise_here` 同阶段重试；`return_upstream` 指向**最早**污染阶段并记录失效下游范围。S7 多归因按上游优先级路由。
- **合并守卫**：快速档仅可在满足条件时合并 S2+S3 或 S4+S5，仍须分别产出工件并依次通过两门；S1、S7 永不合并。

## 1. S4 目的

用对齐目标与先修链的行为证据，确定学习者已经能**独立**解决什么、缺口与误概念在哪里、从哪个节点开始最合适。S4 产出“最近学习前沿”，是“诊断—规划”对（S4–S5）的诊断半边。学习者模型是一等状态：S4 通过 `load`/`append_evidence`/`update`/`history` 读写版本化证据，不在此处静默覆盖既有模型。

## 2. S4 输入契约

| 输入 | 是否必填 | 说明 |
|---|---|---|
| `goal_success_contract`（G1 通过） | 必填 | 锁定目标能力与验收方式 |
| `capability_concept_graph`（G3 通过） | 必填 | 提供节点、先修边和每节点可执行诊断项 |
| 既有学习者记录 | 可选 | 须校验身份、时间、来源、有效期；过期证据只作线索，不计为已掌握 |

校验失败时 `input_validation.status=fail`：目标/图谱未过门、关键节点无诊断项或学习者记录身份/版本不一致，分别路由 S1/S3/S4，**不伪造快照**。

## 3. S4 确认策略（`conditional`）

告知诊断范围、用途和有效期；展示初步节点状态、误概念和学习前沿。学习者对结论有异议、涉及高风险分班/跳级、或自述与行为冲突时升级为强制：对**争议节点追加测试**，从不以自述直接覆盖行为证据。冷启动仅告知将采集哪些初始证据。

## 4. S4 诊断规则（基于行为证据）

- **先声明推断规则再采证**：对每个节点预先说明什么观察算“掌握/未掌握/证据不足”，避免事后调分。
- **任务覆盖**：沿目标与先修链使用解释、预测、反例、诊断、比较、迁移和置信度任务；题目集须含明显错、隐蔽错、无错和需升级题，防止只测口号识别。
- **每条观察记录**：正确性、推理过程、提示层级、耗时（可得时）、置信度、错误类型。
- **三项区分**：`答对`（可能猜对或只识别）、`独立会做`（无提示或低提示完成）、`能迁移`（未见/变式情境通过）。
- **提示—掌握不变量**：`tested_mastered` 必须有同一节点在 `hint_dependency.level=none|low` 下的独立证据；只有 `medium|high|unknown` 提示证据时不得标为 `tested_mastered`，须保持 `tested_not_mastered`/`insufficient_evidence` 并安排撤除支架后的复测。
- **递归定位前沿**：从目标节点回溯，找到最近一个证据支持“可学习但尚未掌握”的节点作为 `learning_frontier`，附证据与理由；多竞争前沿时禁止 S4+S5 合并。
- **证据归并**：自评/年限/偏好问卷只用于选题或线索，绝不直接写入“已掌握”；原始行为、推断状态与路由决策三层分离。

## 5. S4 工件字段（`learner_snapshot.content`）

`learner_id`、`model_version`（整数，基于版本原子更新）、`as_of`（诊断时间点，可选）、`node_states[]`（`node_id`/`status[tested_mastered|tested_not_mastered|insufficient_evidence|untested]`/`evidence_refs[]`/`error_type`/`hint_dependency{level,evidence_refs}`/`confidence_calibration{self_confidence,observed_alignment}`）、`learning_frontier{nearest_learnable_node_id,evidence_refs[],rationale,alternative_candidate_node_ids?}`、`misconceptions[]`（`code/description/evidence_refs[]/related_node_ids?`）、`capability_gaps[]`、`transfer_performance{status,evidence_refs[],summary?}`、`diagnosis_evidence_mapping[]`（`conclusion→evidence_refs`）、`items_needing_retest_or_human_confirmation[]`（`kind[retest|human_confirmation]`）、`evidence_validity{valid_until,stale_evidence_refs,policy?}`。

证据条目本体放在信封 `evidence_collected`（`provenance=learner_behavior`），工件用 `evidence_refs` 引用。

## 6. S4 量规（门 G4）

| 维度 | 阈值类型 | 阈值 | 证据来源 |
|---|---|---|---|
| 测量与目标对齐度 | 关键节点均有对齐诊断项 | true | node_states ∩ goal_success_contract |
| 证据充分性 | 关键结论≥2 对齐观察或显式不足 | true | diagnosis_evidence_mapping |
| 猜对识别 | 区分答对/独立/迁移 | true | node_states.error_type, transfer_performance |
| 提示依赖记录 | 每节点 hint_dependency 已记录 | true | node_states.hint_dependency |
| 错误分类一致性 | error_type 与证据一致，可审计 | true | node_states.error_type |
| 偏差控制 | 自述/年限未覆盖行为证据 | true | confidence_calibration, evidence_collected |
| 结论可解释性 | 每条结论→证据可追溯 | true | diagnosis_evidence_mapping, learning_frontier.evidence_refs |

G4 通过当且仅当**所有维度** `passed=true` 且学习前沿有在有效期内的多项行为证据。

## 7. S4 路由

| verdict | route_to | 触发 |
|---|---|---|
| `pass` | S5 | 全部 G4 维度通过，学习前沿有多项有效证据 |
| `revise_here` | S4 | 证据不足、猜对未识别、提示/置信度缺失、争议节点未复测 |
| `return_upstream` | S3 | 诊断题无法产生目标证据、图谱节点/先修边无效 |
| `return_upstream` | S2/S3 | 诊断暴露来源缺失、偏差或图谱事实错误 |
| `blocked` | S4 | 无真实学习者回答；冷启动待证；关键记录失效且无法补证 |

## 8. S4 安全/阻塞态

- 无真实回答 → 只产出诊断任务，`status=pending`，不模拟行为。
- 冷启动 → `unknown`/`insufficient_evidence`，路由 S4 建立初始证据；**不得**创建“全部未掌握”画像。
- 单题/纯自评/口号识别 → 关键节点保持 `insufficient_evidence` 或 `untested`，G4 不通过。
- 证据过期 → 移入 `evidence_validity.stale_evidence_refs`，只作线索，关键结论需复测后再生效。
- S4+S5 合并须满足：确认零基础、图谱起点明确、路径近线性、任务低风险；四者任一不满足即拆回两步。
