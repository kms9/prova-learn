# S5 阶段契约 — plan-learning-sessions（门 G5）

> 本文件治理 S5 与决策门 G5。§0 为七阶段共享规则；其余为 S5 专属。

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

## 1. S5 目的

从已证实的学习前沿到目标能力选择最小可行子图，并把它编排为有通关标准、测评与复习锚点的学习会话。S5 是“诊断—规划”对（S4–S5）的规划半边：用计划假设替代诊断证据是本阶段最典型的失败模式。

## 2. S5 输入契约

| 输入 | 是否必填 | 说明 |
|---|---|---|
| `learner_snapshot`（G4） | 必填 | 提供已证实的学习前沿、稳定/不稳定节点与误概念 |
| `capability_concept_graph`（G3） | 必填 | 提供能力大纲、学习单元—节点关联、原子节点、先修边与评估映射 |
| `goal_success_contract`（G1） | 必填 | 提供目标能力、验收任务与边界 |
| 时间/节奏/资源/交付形式 | 必填 | 至少一组可用时间与交付形式 |

校验版本一致性与追溯关系：三者 `artifact_id`、`schema_version` 与上游门状态须对齐；S3
`learning_units`、`unit_node_mappings`、`nodes` 与 `edges` 的引用必须仍兼容。**关键学习前沿若仍为
“证据不足”，不得被当作已确定起点直接规划**——返回 S4 补测，不在 S5 用计划假设填充。

## 3. S5 确认策略（强制）

`confirmation.mode=mandatory`。用户确认的是**取舍**，不是每个内部算法细节：

- 路径概览（从前沿到目标的最小连通子图）；
- 阶段目标与优先级；
- 时间投入与节奏（每周/每天可用时间、会话时长与数量）；
- 第一个会话契约（目标、活动、预计时间、输入材料、退出标准）。

`confirmation.status=pending` 时 G5 不得通过。用户根本改变目标时返回 S1。

## 4. S5 规划规则

- 选择前沿到目标的**最小连通子图**；遵守硬先修，仅跳过有有效掌握证据的节点。
- 最小路径以原子 `nodes` 与 `edges` 为计算对象；`learning_units` 只作面向用户的可读分组。大纲父子关系、
  `scope_role` 或展示顺序不得直接转换为个性化学习顺序。
- 发现单元—节点映射悬空、核心覆盖缺失、节点粒度/语义重复、S3 版本冲突或先修不可靠时
  `return_upstream → S3`；S5 不得重写单元、节点、映射或先修边。
- 按概念类型、错误类型与认知目标**匹配教学策略**（误概念优先用对比与worked example；程序性能力优先用渐进练习与撤架；迁移目标必须有未见任务）。
- 编排讲解、练习、检索、交错、迁移与延迟复测；复习锚点须与遗忘曲线匹配（次日、第4天、一周后等）。
- 为每个节点定义**进入条件与退出标准**；退出标准须可观察、可判定，并与测评对齐。
- 时间预算覆盖所有会话与延迟复测；首个会话必须可在用户约束内独立执行。

## 5. S5 工件字段（`learning_and_session_plan.content`）

`stage_goals[]`（`goal_id/statement`）、`ordered_learning_nodes[]`（`node_id/order/selection_rationale/teaching_strategy[]/scaffolding{approach,description}/fade_conditions[]`）、`sessions[]`（`session_id/goal/activities[]/estimated_time{minutes_per_session,session_count}/input_materials[]`）、`assessment_schedule`（`immediate[]/transfer[]/delayed[]`）、`review_anchors[]`、`risks[]`（`risk_id/description/mitigation/criticality`）、`alternative_routes[]`（`trigger/adjustment`）、`exit_criteria`（`per_node[]{node_id,criteria}` + `overall[]`）。

`teaching_strategy` 枚举：`explain`/`worked_example`/`practice`/`retrieval`/`interleaving`/`transfer`/`delayed_retest`/`contrast_case`。

## 6. S5 量规（门 G5）

| 维度 | 阈值类型 | 阈值 | 证据来源 |
|---|---|---|---|
| 目标连通性 | 路径从已证实前沿连到目标 | true | ordered_learning_nodes + exit_criteria |
| 先修正确性 | 无硬先修跨越 | true | ordered_learning_nodes.order + 图谱先修边 |
| 路径最小性 | 无不可解释冗余，仅跳过有掌握证据节点 | true | selection_rationale |
| 时间可行性 | 首个会话可在约束内执行，总量不超预算 | true | sessions.estimated_time |
| 策略适配性 | 策略匹配概念/错误类型/认知目标 | true | teaching_strategy + scaffolding |
| 教学与测评对齐度 | 每节点退出标准对应可判定测评 | true | exit_criteria.per_node + assessment_schedule |
| 认知负荷 | 难度处于当前可学习范围，复习间距合理 | true | sessions + review_anchors |
| 调整空间 | 风险与替代路线可执行 | true | risks + alternative_routes |

G5 通过当且仅当**所有维度** `passed=true` 且 `confirmation.status=confirmed`。复制课程目录、视频定额或题量，无图谱/快照/退出规则者直接失败。

## 7. S5 路由

| verdict | route_to | 触发 |
|---|---|---|
| `pass` | S6 | 全部 G5 维度通过 + 强制确认完成 + 首个会话可执行 |
| `revise_here` | S5 | 时间/资源不可行、路径冗余、策略不适配、退出标准不可判定 |
| `return_upstream` | S4 | 诊断依据不稳、学习前沿证据不足或冲突 |
| `return_upstream` | S1 | 用户根本改变目标、范围或验收方式 |
| `return_upstream` | S3 | 图谱版本、学习单元—节点映射、节点粒度、先修边或评估映射错误 |

## 8. S5 安全/阻塞态

- 学习前沿证据不足 → 返回 S4，不伪造起点。
- 图谱版本、学习单元—节点映射、节点粒度或先修不可靠 → 返回 S3，不在 S5 修补。
- 时间/资源不可行 → 留在 S5 缩减或调整，不静默删除目标门或测评。
- 强制确认未完成 → `pending`；G5 不得通过。
- 快速档合并 S4+S5 时仍须先产出独立 `learner_snapshot` 并通过 G4，再产出计划并通过 G5。
