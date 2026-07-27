# S6 阶段契约 — run-instructional-interaction（门 G6）

> 本文件治理 S6 与决策门 G6。§0 为七阶段共享规则；其余为 S6 专属。

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

## 1. S6 目的

为当前学习节点生产可追溯、分层、含正反例与渐隐支架的教学内容，并通过真实交互帮助学习者形成可验证、可被 S7 判定的理解和能力。S6 评价的是**教学工件质量与交互证据**，不宣布学习者是否掌握——掌握判定属于 G7。

## 2. S6 输入契约

| 输入 | 是否必填 | 说明 |
|---|---|---|
| 当前节点（`learning_and_session_plan`） | 必填 | 必须位于已确认路径，硬先修已满足 |
| 图谱节点信息（节点边、通关标准） | 必填 | 节点必须可被 S3 图谱追溯 |
| 证据全景（来源与适用边界） | 必填 | 内容必须可追溯到已审计证据 |
| `learner_snapshot` | 必填 | 仍在有效期内，描述当前可学习范围 |
| 会话目标与节点通关标准 | 必填 | 会话目标必须与节点 exit criteria 一致 |

校验失败时 `input_validation.status=fail`，路由上游并**不得伪造正向工件**；关键内容无可追溯来源返回 S2/S3，学习者状态失效返回 S4/S5。

## 3. S6 确认策略（inform 为主）

- **会话开始**：`mode=inform`，告知本会话目标、约束、可用媒介与“过程记录用于更新学习者模型”，学习者无异议记 `status=acknowledged` 后继续。
- **节点结束**：`mode=inform`，告知默认下一动作（进入 S7 掌握验证），不强制确认。
- **条件升级为 conditional**：学习者卡住、疲劳或请求改变形式（媒介/难度/支架量）时触发；高代价或不可逆调整须显式确认。

## 4. S6 教学规则

- 仅从已审计证据中选择内容；标明来源与适用边界；模型常识不得包装为审计事实。
- 生成**分层解释**与**多种表征**，并互相连接（抽象↔具体）。
- 同时给出**正例、反例、边界案例**与**常见误解**及纠正路径。
- 设计**渐进练习**：检索前测 → worked example → 半完成 → 对比 → 独立迁移；难度处于当前可学习范围。
- 建立**逐级提示阶梯**与**反馈规则**（task / process / self-regulation）；提示指向查询形状或官方规则，**不代替学习者的关键推理**。
- **先让学习者产出，再给反馈**；按回答动态撤架；没有独立作答不生成有效掌握候选。
- **防止答案泄露**：练习提交前不公布答案；区分“会做”与“看懂”。
- **完整记录交互轨迹**：每次回答、提示层级、修正轨迹、未解决问题与内容变化；记录 `learner_behavior` 证据。
- G6 通过只说明教学工件合格，**绝不**宣布学习者掌握。

## 5. S6 工件字段（`session_package_and_trace.content`）

`session_goal`、`success_conditions[]`、`current_node{node_id, exit_criteria[]}`、`explanations[]`（`explanation_id/layer/representation/statement/cognitive_level/evidence_refs[]`，每条≥1 来源追溯）、`examples{positive[]/negative[]/boundary[]/common_misconceptions[]}`、`activities[]`（`activity_id/kind/instruction/cognitive_level/requires_learner_output`，含 `exercise/question/project/simulation` 等）、`hint_ladder[]`（`step/level/prompt/fading_condition`）、`feedback_rules[]`（`rule_id/task/process/self_regulation`）、`scaffolding_fade_strategy{initial_support/fade_rule/terminal_support}`、`interaction_events[]`（`event_id/learner_response/hints_used[]/correction_trajectory[]`）、`candidate_mastery_evidence[]`（节点级 `evidence_id/node_id/dimension/status`）、`content_quality_status{state, reviewed_against, errors_found}`。`state` 取值 `correct/has_error/needs_review`；`cognitive_level` 取值 `remember/understand/apply/analyze/evaluate/create`。

## 6. S6 量规（门 G6）

| 维度 | 阈值类型 | 阈值 | 证据来源 |
|---|---|---|---|
| 内容正确性与可追溯性 | 关键内容无错误且每条解释≥1 来源 | true | content_quality_status / explanations.evidence_refs |
| 对目标和学习者的适配 | 会话目标与节点 exit criteria 对齐且匹配学习者前沿 | true | session_goal / current_node / learner_snapshot |
| 认知层级 | 覆盖多个认知层级并含应用及以上 | ≥2 层级 | explanations.cognitive_level / activities.cognitive_level |
| 例子代表性 | 正例、反例、边界与常见误解同时出现 | true | examples |
| 支架质量 | 提示阶梯逐级、有撤架条件且不代替关键推理 | true | hint_ladder / scaffolding_fade_strategy |
| 答案泄露控制 | 独立任务提交前不公布答案 | true | activities.answer_leakage_control |
| 学习者主动性 | 存在独立产出且能产生可判定证据 | true | interaction_events / candidate_mastery_evidence |
| 交付可用性 | 工件字段完整、可被 S7 直接消费 | true | content 全字段 |

G6 通过当且仅当**所有维度** `passed=true`，且存在真实 `candidate_mastery_evidence`（非空）。G6 **不得**因“内容输出结束”或“学习者回复懂了”而通过。

## 7. S6 路由

| verdict | route_to | 触发 |
|---|---|---|
| `pass` | S7 | 全部 G6 维度通过且存在真实候选掌握证据 |
| `revise_here` | S6 | 内容错误、形式不合适、答案泄露或支架缺失，可在本阶段修复 |
| `return_upstream` | S5 | 内容正确但策略/顺序/难度/节奏不适配 |
| `return_upstream` | S4 | 新证据与学习前沿假设冲突，需重新诊断 |
| `return_upstream` | S3/S2 | 关键内容来源不可追溯或图谱节点失效 |
| `blocked` | S6 | 关键来源缺失或学习者未作答且无法继续 |

## 8. S6 安全/阻塞态

- 学习者尚未作答 → 记录 `requirement_gaps`，保持 `pending`，**不得代写** `learner_behavior`。
- 关键内容无可追溯来源 → `blocked` 或 `return_upstream`；不得用模型记忆替代审计证据。
- 答案泄露或无独立作答 → `revise_here`；禁止进入 S7 宣称掌握。
- 学习者持续卡住但内容正确 → `return_upstream → S5`，必要时继续上溯至 S4。
- 长篇讲义 + 即时答案 + “懂了” → G6 失败，`positive_artifact=null`，`verdict=revise_here`。
