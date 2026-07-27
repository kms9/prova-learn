# check-rubric — S6 / 决策门 G6（教学工件质量判定标准）

> 本量规是 `check-instructional-interaction` 的判定标准，与阶段 skill `run-instructional-interaction/references/stage-contract.md` §6 保持一致。检查者独立重判，不采信被检工件自报的 `verdict`，也不因学习者一句“懂了”或“内容输出结束”而通过。G6 判定**工件质量**，不宣布学习者掌握——掌握判定属于 G7。

## 判定流程

1. 结构校验：信封通过 `handoff-envelope.schema.json`；`positive_artifact` 通过 `session-package-and-trace.schema.json`。
2. 逐维判定下表（每维：证据 / 评分 / 阈值 / `passed`）。
3. 来源与泄露复核（每条解释≥1 已审计来源；独立任务提交前不公布答案）。
4. 交互证据复核（真实 `learner_behavior` 与非空候选掌握证据）。
5. 汇总裁决与路由。

## G6 维度量规

| 维度 | 阈值类型 | 通过阈值 | 证据来源（指向被检工件字段） |
|---|---|---|---|
| 内容正确性与可追溯性 | 关键内容无错误且每条解释≥1 来源 | true | `content.content_quality_status` / `content.explanations[].evidence_refs` |
| 对目标和学习者的适配 | 会话目标与节点 exit criteria 对齐且匹配学习者前沿 | true | `content.session_goal` / `content.current_node.exit_criteria` / 上游 `learner_snapshot` |
| 认知层级 | 覆盖多个认知层级且含应用及以上 | ≥2 层级 | `content.explanations[].cognitive_level` / `content.activities[].cognitive_level` |
| 例子代表性 | 正例、反例、边界与常见误解同时出现 | true | `content.examples.{positive,negative,boundary,common_misconceptions}` |
| 支架质量 | 提示阶梯逐级、有撤架条件且不代替关键推理 | true | `content.hint_ladder[]` / `content.scaffolding_fade_strategy` |
| 答案泄露控制 | 独立任务提交前不公布答案 | true | `content.activities[].answer_leakage_control` |
| 学习者主动性 | 存在独立产出且能产生可判定证据 | true | `content.interaction_events[]` / `content.candidate_mastery_evidence[]` |
| 交付可用性 | 工件字段完整、可被 S7 直接消费 | true | `content` 全字段 |

## 通过条件（G6 pass）

当且仅当**全部**满足：

- 所有上表维度 `passed=true`；
- 每条 `explanations[].evidence_refs` 至少 1 条已审计来源（`external_evidence`/`learner_behavior` 等），`model_hypothesis` 与 `user_provided_unverified` 不得计为内容来源；
- 独立任务（`requires_learner_output=true`）在提交前未公布答案，提示不代替学习者的关键推理；
- 存在真实、非空的 `candidate_mastery_evidence`（`status` 为 `candidate`/`partial`，**不是**掌握宣告）；
- `interaction_events[]` 记录了真实 `learner_behavior`（回答、提示层级、修正轨迹），学习者仅“懂了”或未作答不得计为有效证据。

通过 → `verdict=pass`、`route_to=S7`。**G6 通过只说明教学工件合格，绝不等于宣布学习者掌握**；延迟保持与边界稳定性留待 G7。

## 不通过时的路由

| 触发 | verdict | route_to |
|---|---|---|
| 内容错误、形式不合适、答案泄露或支架缺失，可在本阶段修复 | revise_here | S6 |
| 内容正确但策略/顺序/难度/节奏不适配 | return_upstream | S5 |
| 新证据与学习前沿假设冲突，需重新诊断 | return_upstream | S4 |
| 关键内容来源不可追溯或图谱节点失效 | return_upstream | S3/S2 |
| 关键来源缺失或学习者未作答且无法继续 | blocked | S6 |

> `return_upstream` 指向**最早**污染阶段并记录失效下游范围；S6 自身缺陷（答案泄露、无支架、无独立作答）取 `revise_here`/`blocked`，`route_to=S6`。

## 反模式（检查者不得犯）

- 直接采信被检工件自报 `verdict=pass` 或学习者一句“懂了”而不逐维重判。
- 把 `model_hypothesis` 或 `user_provided_unverified` 计为内容来源。
- 因“内容输出结束”或“学习者回复懂了”而判 G6 通过。
- 答案泄露、提示代替学习者推理、无独立作答却仍放行进入 S7。
- 宣布学习者“掌握”——G6 只产出候选掌握证据，掌握判定属于 G7。
- 代写 `learner_behavior` 证据或为未作答的学习者生成掌握候选。
- 结构非法（`positive_artifact=null`）却仍给出 `pass`。
- 修改被检工件或替 S6 生成新教学内容。
