# S7 阶段契约 — verify-mastery-and-replan（门 G7）

> 本文件治理 S7 与决策门 G7。§0 为七阶段共享规则；其余为 S7 专属。

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
- **显式未知/阻塞态**：`pending`/`blocked`/`unknown`/`evidence_insufficient`/`research_blocked`/`not_executed` 不得被强制为 `pass`。
- **确定性路由**：`pass` 前进；`revise_here` 同阶段重试；`return_upstream` 指向**最早**污染阶段并记录失效下游范围。S7 多归因按上游优先级路由。
- **合并守卫**：快速档仅可在满足条件时合并 S2+S3 或 S4+S5，仍须分别产出工件并依次通过两门；S1、S7 永不合并。
- **强制完整文档**：每次运行都必须遵守当前 skill 的 `markdown-output-contract.md`。`pending` 或 `blocked` 也要完整写明已知事实、未知项、未执行项、当前结论与恢复条件；禁止空标题、空表、`TBD`、`TODO`、示例数据或其他占位内容。
- **强制页面派生**：每次运行都必须基于最终信封生成已填充的本阶段专用 HTML；`pending` 或 `blocked` 也展示真实缺口、当前结论和恢复条件，不得使用通用装载器或空白占位。
- **只生成数据驱动页面**：HTML 是唯一可视化交付，页面视图必须由内嵌规范 JSON 动态渲染；禁止调用制图/图像生成工具，禁止生成、引用或依赖独立图片、插图、知识点图卡或其他静态图片资产。
- **只读展示边界**：页面交互仅用于切换、搜索、筛选、展开和浏览既有数据；不得接受业务输入、导出草稿，或展示 Schema、模板、Markdown/HTML 生成状态及输出说明。
- **交付完整性**：Markdown、JSON 或 HTML 任一缺失，Markdown—JSON 对应失败，或 HTML 三项验证任一失败时，均不得把本次阶段交付报告为完整完成；文档/页面失败不篡改领域门禁本身。

## 1. S7 目的

把会话交互证据综合为节点级掌握判定，区分“本次答对”与“长期掌握”，再以基于版本的原子更新写入学习者模型，并按确定性归因选择继续、补救、跳过、重诊断或完成。S7 是“掌握验证—模型更新”反馈事务的闭环。

## 2. S7 输入契约

| 输入 | 是否必填 | 说明 |
|---|---|---|
| `session_package_and_trace`（已过 G6） | 必填 | 会话记录完整，含交互事件、提示阶梯、候选掌握证据与内容质量状态 |
| 节点掌握规则 | 必填 | 必须在测评**之前**确定；不得用结果反推规则 |
| 历史 `learner_snapshot` | 必填 | 含 `learner_id` 与可用 `model_version`；冷启动返回 `unknown` 路由 S4，不在此创建全未掌握画像 |
| 当前计划与图谱 | 必填 | 用于读取节点先修、评估映射与下一节点 |
| `expected_model_version` | 必填 | 与持久层当前版本比对，决定是否应用补丁 |

冷启动缺输入或版本不可用时记录 `requirement_gaps`，保持 `pending`/`blocked`，不伪造掌握或更新。

## 3. S7 确认策略（条件）

`confirmation.mode=conditional`。常规节点推进可告知后继续；以下情形升级为强制确认：与学习者就掌握结论或证据存在分歧、重大路径变更、跳过节点、声称目标完成（`GOAL_ACHIEVED`）、或影响高风险决策的路由。学习者反思与异议可触发复核，但不得用自述直接覆盖行为证据。

## 4. S7 两个有序子流程（原子事务）

S7 保持一个顶层阶段，内部严格按顺序执行两个子流程，二者在一次反馈事务内闭环：

### 4.1 子流程一：掌握验证（`mastery_verification`）

- 对每个待判节点采集多维证据：`correctness`、`reasoning_quality`、`hint_dependency`、`transfer`（近/远）、`confidence` 校准、`delayed_retention`。
- 统一提示依赖枚举后再判定：S4 `none/low/medium/high` 映射为 S7
  `none/low/moderate/high`，S4 `unknown` 仅在无可用提示记录时映射为 `not_executed`；S6 实际发生的
  `light/medium/strong` 映射为 S7 `low/moderate/high`。S6 的提示阶梯只是计划，必须以
  `interaction_events.hints_used` 或 S4 行为事件为准；未使用提示为 `none`，缺记录才是 `not_executed`。
- 即时正确、同题重做、近迁移、远迁移和延迟保持是**不同**证据；任一关键维度缺失即不满足掌握规则。
- 区分内容质量问题、教学策略/顺序问题、诊断假设冲突、图谱结构问题、来源错误/过期/覆盖缺口与目标变更，避免把上游错误记成“学习者不会”。
- 产出 `node_mastery_evidence[]`（每节点每维带证据事件 ID）、`mastery_judgment[]`（`mastered`/`partial`/`not_mastered`）、`attribution`（primary + secondary[]）、`not_mastered_cause`。
- 单题识别正确归为 `EVIDENCE_INSUFFICIENT`，绝不写成高掌握概率。

### 4.2 子流程二：学习者模型更新与重规划（`learner_model_update_and_replan`）

1. 读取历史模型版本与证据有效期；`load(learner_id, as_of)` 返回版本、有效期和缺失字段，不把“无记录”等同于“未掌握”。
2. 将新证据作为不可变事件追加；原始学习证据、推断出的掌握状态与重规划决策分层保存。
3. 仅当 `expected_model_version` 与当前版本匹配时，应用补丁并保留每个节点变更前值、变更后值、证据事件 ID 与理由。
4. 选择决策（`continue`/`remediate`/`skip`/`rediagnose`/`complete`）、调整路径、下一会话契约与复习/延迟复测安排。
5. 保留变更前后值与决策理由以支持回滚与审计。
6. 把会话暴露的来源错误、过期事实、缺失失败条件、Benchmark 偏差或新兴信号误用记录为
   `evidence_feedback`：包含 `feedback_id/type/affected_claim_refs/affected_node_ids/evidence_event_ids/
   suggested_queries/invalidated_downstream`。该反馈只触发 S2 局部补证，不在 S7 直接改写事实。

更新段引用验证段采集的证据事件；证据不足或版本冲突时不允许把节点写成已掌握。

### 4.3 Schema 与 G7 量规的执行边界

- JSON Schema 机械强制六类证据维度、每维结果枚举、事件引用、版本事务与更新状态的结构；S4 的提示依赖规则可在同一节点对象内静态判断，因此由 Schema 直接 `if/then` 强制。
- S7 的 `mastered` 必须逐节点对照**测评前已确定的节点专属掌握规则**。证据与判定位于两个按 `node_id` 关联的数组，且不同目标对迁移/延迟阈值可以不同；Draft 2020-12 Schema 无法可靠表达跨数组同一 `node_id` 的值关联。该语义由 G7 的“证据充分性 / 掌握规则一致性 / 迁移与延迟证据”三项共同强制，不把一个全局 `contains` 误当成节点级证明。
- `load.current_model_version` 的正向工件最小值为 1 是有意约束：S7 只接受可加载的历史 `learner_snapshot`。冷启动或无版本不是版本 0 的正向事务，而是输入验证失败，公共 handoff 令 `positive_artifact=null` 并路由 S4 建立初始证据。

## 5. S7 工件字段（`mastery_and_replanning_bundle.content`）

`content` 恰好包含两个有序段，均 `additionalProperties:false`：

- `mastery_verification`：`node_mastery_evidence[]`（每项含 `node_id` + 六维证据：`correctness`/`reasoning_quality`/`hint_dependency`/`transfer`/`confidence`/`delayed_retention`，每维含 `result`/`detail`/`evidence_event_ids`）、`mastery_judgment[]`（`node_id`+`status`）、`attribution`（`primary`+`secondary[]`）、`not_mastered_cause`。
- `learner_model_update_and_replan`：`learner_id`、`expected_model_version`、`model_version`（事务后）、`model_patch[]`（`node_id`/`before`/`after`/`evidence_event_ids`/`rationale`）、`update_status`（`applied`/`version_conflict`/`not_executed`）、`decision`、`adjusted_path`、`next_session_contract`（`next_session_id`/`target_node_id`/`objective`/`required_evidence`/`hint_policy`）、`review_schedule`（`retrieval`/`spacing`/`interleaving`/`delayed_retest`）、`evidence_feedback[]`（来源异常的受影响 claim/node、证据事件、复核查询和失效下游）。

## 6. S7 量规（门 G7）

| 维度 | 阈值类型 | 阈值 | 证据来源 |
|---|---|---|---|
| 证据充分性 | 每节点多维证据齐 | true | node_mastery_evidence |
| 掌握规则一致性 | 判定与预设规则一致 | true | mastery_judgment vs 掌握规则 |
| 提示影响控制 | 提示依赖被记录并计入 | true | hint_dependency |
| 迁移与延迟证据 | 必要的迁移/延迟已执行 | true | transfer, delayed_retention |
| 更新前后一致性 | 每项变更可追溯到新证据 | true | model_patch.evidence_event_ids |
| 调整可解释性 | 决策与归因匹配、路径调整有理由 | true | decision, adjusted_path, rationale |
| 避免单次结果过度反应 | 不因一次正确即高掌握 | true | confidence, mastery_judgment |
| 来源反馈闭环 | 来源异常被记录并路由最早污染阶段，不在 S7 改写事实 | true | evidence_feedback + route |

G7 通过当且仅当**所有维度** `passed=true` 且确认策略已满足。学习者未掌握不等于 S7 工件失败：多维证据齐全、归因与路由正确、更新前后一致时，工件可通过，`route_to` 仍可指向上游补救。

## 7. S7 确定性返工与路由表

| 主归因代码 | 判定条件 | `route_to` | 动作 |
|---|---|---|---|
| `EVIDENCE_INSUFFICIENT` | 缺少独立、迁移或延迟证据，无法满足预定掌握规则 | S7 | 补测或安排延迟复测，不更新为已掌握 |
| `CONTENT_QUALITY` | 内容错误、来源不可追溯、示例或题目失效 | S6 | 修复内容并使受影响证据失效 |
| `STRATEGY_OR_SEQUENCE` | 内容正确，但难度、支架、顺序或节奏不适配 | S5 | 重选策略或调整路径 |
| `DIAGNOSTIC_ERROR` | 新证据与学习前沿假设冲突，且不能由单次波动解释 | S4 | 对争议节点重新诊断 |
| `GRAPH_ERROR` | 先修边、节点粒度或评估映射错误 | S3 | 修正模型并重新计算受影响路径 |
| `SOURCE_ERROR` | 来源缺失、偏差、过期、覆盖不足或冲突未处理 | S2 | 记录 evidence_feedback，局部补证后再进入 S3 |
| `GOAL_CHANGED` | 目标、成功标准、范围或约束发生实质变化 | S1 | 重签目标与成功契约 |
| `NODE_MASTERED` | 达到预设门槛且没有待完成的必要延迟检查 | S6 | 进入下一学习节点 |
| `GOAL_ACHIEVED` | 最终验收任务和整体保持要求均通过 | complete | 输出最终能力证据与后续保持计划 |

存在多个归因时，按“**目标 → 来源 → 图谱 → 诊断 → 路径 → 内容 → 证据**”的上游优先级路由——先修复最早污染源，再重新验证下游工件。每次路由必须记录主归因、次要归因、证据和失效范围。

`verdict` 与路由的关系：`pass` 对应前进（`NODE_MASTERED`→S6、`GOAL_ACHIEVED`→complete）；`revise_here` 对应 `EVIDENCE_INSUFFICIENT`→S7；其余归因（`CONTENT_QUALITY`/`STRATEGY_OR_SEQUENCE`/`DIAGNOSTIC_ERROR`/`GRAPH_ERROR`/`SOURCE_ERROR`/`GOAL_CHANGED`）对应 `return_upstream`。

## 8. S7 版本冲突处理

- `update(expected_version, patch)` 必须基于版本检查；`expected_model_version` 与持久层不一致时，`update_status=version_conflict`，**不应用任何补丁**，输出重新加载指令。
- 无真实后端或证据被判定为不足以更新时，`update_status=not_executed`，不得声称持久化成功。
- 冲突或未执行时，节点掌握判定仍可记录（基于已采集证据），但不得把节点写成因“已更新”而掌握。
- 冷启动无历史模型时返回 `unknown`，路由 S4 建立初始证据，不在 S7 创建全未掌握画像。

## 9. S7 安全/阻塞态

- 缺独立/迁移/必要延迟证据 → 保持 `partial`/`not_mastered`，`EVIDENCE_INSUFFICIENT`→S7 补测，不伪造掌握。
- 内容质量问题先识别为 `CONTENT_QUALITY`→S6，不得记成学习者能力问题。
- 重大路径变更或目标实质变化 → 升级为强制确认；目标变化返回 S1。
- 研究级运行缺少独立专家评审或纵向延迟复测时，相关门记为 `pending`/`not_executed`，不得由即时表现推断为完成。
- `GOAL_ACHIEVED` 必须写明适用范围（模拟/观察）与未运行门，不得宣称获得职级、生产可用或未验证领域的胜任。
