# S5 阶段契约 — plan-learning-sessions（门 G5）

> 本文件治理 S5 与决策门 G5。§0 为七阶段共享规则；其余为 S5 专属。

## 0. 共享阶段契约（适用于 S1–S7）

- **编号定义**：`Sx` 是第 x 个执行阶段（Stage），`Gx` 是紧随 Sx、评价该阶段工件能否被下游消费的质量决策门（Gate）。例如 `G1` 是 S1 目标契约质量门，不是学习理论、外部标准或另一个 Skill。
- **“已通过 Gx”的机读含义**：不能凭文件存在、自然语言声称或只看 `positive_artifact` 推断。对作为上游输入的 G1–G6，消费方必须验证兼容移交信封同时满足：`stage_id=Sx`、`status=completed`、`input_validation.status=pass`、具名 `positive_artifact` 非空且通过其 Schema、该门要求的全部 `quality_evaluation.rubric_results[].passed=true`、`quality_evaluation.verdict=pass`、`quality_evaluation.route_to=S{x+1}`，并满足该阶段确认规则；三工件交付还要求 `document_artifact.status=generated` 与 `presentation_artifact.status=generated`。上游 Skill 未与当前 Skill 一起安装时，也必须由调用方提供这些字段或先适配成兼容信封；裸工件只能记为未验证输入。

每个阶段必须产出**三份内容一致、用途不同的工件**：

1. 一份按当前阶段专属结构撰写的完整 Markdown 人审文档；
2. 一份把 Markdown 全部实质内容无损结构化的规范 JSON 移交信封（`handoff-envelope.schema.json`）；
3. 一份由最终 JSON 填充的阶段专用交互 HTML。

统一执行形状：

```text
校验输入契约
→ 收集需求缺口
→ 执行本阶段确认策略
→ 收集可采信证据
→ 先完成阶段专属 Markdown 的事实、分析、结论、量规与路由
→ 将同一内容无损结构化为具名正向工件与 JSON 移交信封
→ 校验 Markdown 章节与 JSON Pointer 的逐项对应
→ 派生并验证阶段专用 HTML
```

- **三工件权威边界**：Markdown 是首要人审文档，JSON 是机器移交的规范表示，HTML 是 JSON 驱动的只读派生视图。Markdown 与 JSON 必须语义等价，不能以“摘要 JSON”丢弃文档中的证据、边界、缺口、失败条件、异议或路由依据。
- **严格生成顺序**：先完成 Markdown 实质内容，再生成 JSON，最后生成 HTML。JSON/HTML 生成后只允许回填路径、工件标识和验证状态等机械信息；实质内容变化必须同步 Markdown 与 JSON 并重新验证。
- **输入契约校验**：至少检查工件类型、schema 版本、必填字段、来源阶段、追溯与上游门状态。失败时 `input_validation.status=fail` 并路由上游，**不得伪造正向工件**。
- **确认状态机**：`mandatory`（S1/S5，未确认不得前进）、`conditional`（S2/S3/S4/S7，遇高风险/分歧/多方案升级为强制）、`inform`（S6 节点推进，告知后继续）。
- **证据来源分类**：`model_hypothesis`/`market_signal`/`external_evidence`/`user_provided_unverified`/`learner_behavior`。**门不得把 `model_hypothesis` 或 `user_provided_unverified` 计为外部证据。**
- **量规结果形状**：`{dimension, evidence[], score, threshold, passed, failure_action, route_to}`；`passed=false` 时 `failure_action` 与 `route_to` 必填。
- **显式未知/阻塞态**：`pending`/`blocked`/`unknown`/`evidence_insufficient`/`research_blocked`/`not_executed`/`version_conflict` 不得被强制为 `pass`。
- **确定性路由**：`pass` 前进；`revise_here` 同阶段重试；`return_upstream` 指向**最早**污染阶段并记录失效下游范围。S7 多归因按上游优先级路由。
- **合并守卫**：快速档仅可在满足条件时合并 S2+S3 或 S4+S5，仍须分别产出工件并依次通过两门；S1、S7 永不合并。
- **强制完整文档**：每次运行都必须遵守当前 skill 的 `markdown-output-contract.md`。`pending` 或 `blocked` 也要完整写明已知事实、未知项、未执行项、当前结论与恢复条件；禁止空标题、空表、`TBD`、`TODO`、示例数据或其他占位内容。
- **强制页面派生**：每次运行都必须基于最终信封生成已填充的本阶段专用 HTML；`pending` 或 `blocked` 也展示真实缺口、当前结论和恢复条件，不得使用通用装载器或空白占位。
- **只生成数据驱动页面**：HTML 是唯一可视化交付，页面视图必须由内嵌规范 JSON 动态渲染；禁止调用制图/图像生成工具，禁止生成、引用或依赖独立图片、插图、知识点图卡或其他静态图片资产。
- **只读展示边界**：页面交互仅用于切换、搜索、筛选、展开和浏览既有数据；不得接受业务输入、导出草稿，或展示 Schema、模板、Markdown/HTML 生成状态及输出说明。
- **交付完整性**：Markdown、JSON 或 HTML 任一缺失，Markdown—JSON 对应失败，或 HTML 三项验证任一失败时，均不得把本次阶段交付报告为完整完成；文档/页面失败不篡改领域门禁本身。

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

> **S1 已迁移到 run-folder 目录交付**：`goal_success_contract` 不再是 JSON 信封，而是 S1 run folder（入口 `workspace/<project-slug>/runs/<最新 run>/INDEX.md`）。取目标能力/验收/边界时按 run-folder 七项校验确认 G1 通过，并从 `goal-contract.md`/`capabilities.jsonl`/`INDEX.md` 取字段；`learner_snapshot` 与 `capability_concept_graph` 仍为 JSON 信封（待后续迁移）。

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
- 核心路径优先纳入 `core_stable` 与目标所需 `core_practice`；`research_frontier` 仅在目标明确需要时进入，
  `emerging_signal` 只能进入观察/可选路线。动态证据过期、社区或单一热点被误作核心时返回 S2/S3。
- 按概念类型、错误类型与认知目标**匹配教学策略**（误概念优先用对比与worked example；程序性能力优先用渐进练习与撤架；迁移目标必须有未见任务）。
- 专家目标通过任务复杂度、自主性、影响范围、责任和验收难度增加深度，不以更多术语或工具数量替代能力等级。
- 编排讲解、练习、检索、交错、迁移与延迟复测；复习锚点须与遗忘曲线匹配（次日、第4天、一周后等）。
- 为每个节点定义**进入条件与退出标准**；退出标准须可观察、可判定，并与测评对齐。
- 时间预算覆盖所有会话与延迟复测；首个会话必须可在用户约束内独立执行。

## 5. S5 工件字段（`learning_and_session_plan.content`）

`stage_goals[]`（`goal_id/statement`）、`ordered_learning_nodes[]`（`node_id/order/selection_rationale/evidence_basis{knowledge_tier,knowledge_status,freshness,source_refs,inclusion_reason}/teaching_strategy[]/scaffolding{approach,description}/fade_conditions[]`）、`sessions[]`（`session_id/goal/activities[]/estimated_time{minutes_per_session,session_count}/input_materials[]`）、`assessment_schedule`（`immediate[]/transfer[]/delayed[]`）、`review_anchors[]`、`risks[]`（`risk_id/description/mitigation/criticality`）、`alternative_routes[]`（`trigger/adjustment`）、`exit_criteria`（`per_node[]{node_id,criteria}` + `overall[]`）。

`teaching_strategy` 枚举：`explain`/`worked_example`/`practice`/`retrieval`/`interleaving`/`transfer`/`delayed_retest`/`contrast_case`。

## 6. S5 量规（门 G5）

| 维度 | 阈值类型 | 阈值 | 证据来源 |
|---|---|---|---|
| 目标连通性 | 路径从已证实前沿连到目标 | true | ordered_learning_nodes + exit_criteria |
| 先修正确性 | 无硬先修跨越 | true | ordered_learning_nodes.order + 图谱先修边 |
| 路径最小性 | 无不可解释冗余，仅跳过有掌握证据节点 | true | selection_rationale |
| 时间可行性 | 首个会话可在约束内执行，总量不超预算 | true | sessions.estimated_time |
| 策略适配性 | 策略匹配概念/错误类型/认知目标 | true | teaching_strategy + scaffolding |
| 证据分层适配 | 核心/实践/前沿/新兴进入规则正确，动态来源在有效期 | true | ordered_learning_nodes.evidence_basis |
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
