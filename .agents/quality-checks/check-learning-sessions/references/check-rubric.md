# check-rubric — S5 / 决策门 G5（学习会话计划质量判定标准）

> 本量规是 `check-learning-sessions` 的判定标准，与阶段 skill `plan-learning-sessions/references/stage-contract.md` §6 保持一致。检查者独立重判，不采信被检工件自报的 `verdict`。

## 判定流程

1. 结构校验：信封通过 `handoff-envelope.schema.json`；`positive_artifact` 通过 `learning-and-session-plan.schema.json`。
2. 逐维判定下表（每维：证据 / 评分 / 阈值 / `passed`）。
3. 确认复核（S5 强制确认）。
4. 证据来源复核（计划假设不得当作已证实前沿）。
5. 汇总裁决与路由。

## G5 维度量规

| 维度 | 阈值类型 | 通过阈值 | 证据来源（指向被检工件字段） |
|---|---|---|---|
| 目标连通性 | 路径从已证实前沿连到目标 | true | `content.ordered_learning_nodes` + `content.exit_criteria` |
| 先修正确性 | 无硬先修跨越 | true | `content.ordered_learning_nodes[].order` + 上游 `capability_concept_graph` 先修边 |
| 路径最小性 | 无不可解释冗余，仅跳过有掌握证据节点 | true | `content.ordered_learning_nodes[].selection_rationale` |
| 时间可行性 | 首个会话可在约束内执行，总量不超预算 | true | `content.sessions[].estimated_time` |
| 策略适配性 | 策略匹配概念/错误类型/认知目标 | true | `content.ordered_learning_nodes[].teaching_strategy` + `scaffolding` |
| 教学与测评对齐度 | 每节点退出标准对应可判定测评 | true | `content.exit_criteria.per_node[]` + `content.assessment_schedule` |
| 认知负荷 | 难度处于当前可学习范围，复习间距合理 | true | `content.sessions` + `content.review_anchors` |
| 调整空间 | 风险与替代路线可执行 | true | `content.risks` + `content.alternative_routes` |

## 通过条件（G5 pass）

当且仅当**全部**满足：

- 所有上表维度 `passed=true`；
- `confirmation.status=confirmed`（强制确认已解）；
- 起点为已证实的上游 `learner_snapshot` 学习前沿（计划假设不得替代诊断证据）；
- 首个会话可在用户时间/资源约束内独立执行；
- 无 `criticality=critical` 且 `gate_effect=block` 的未决证据缺口。

通过 → `verdict=pass`、`route_to=S6`。

## 不通过时的路由

| 触发 | verdict | route_to |
|---|---|---|
| 时间/资源不可行、路径冗余、策略不适配、退出标准不可判定 | revise_here | S5 |
| 学习前沿证据不足、冲突或诊断依据不稳 | return_upstream | S4 |
| 图谱先修边、节点粒度或评估映射错误 | return_upstream | S3 |
| 用户根本改变目标、范围或验收方式 | return_upstream | S1 |
| 缺强制确认 / `positive_artifact=null` / 关键缺口未解 | blocked | S5 |

> S5 处于“诊断—规划”对（S4–S5）的规划半边：起点不稳 → S4；图谱先修/粒度错 → S3；计划自身不达标 → 留在 S5；目标被改变 → S1。四者按最早污染阶段区分。

## 反模式（检查者不得犯）

- 直接采信被检工件自报 `verdict=pass` 而不逐维重判。
- 把计划假设（`model_hypothesis`）或 `user_provided_unverified` 当作已证实学习前沿。
- 把“课程章节/视频定额/题量”当作能力节点放行。
- 用退出标准通过替代“强制确认通过”；二者各自独立。
- 结构非法却仍给出 `pass`。
- 修改被检工件或替 S5 生成新计划。
