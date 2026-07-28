# S7 完整 Markdown 文档契约

本文件规定 S7 的第一份必交工件：可审核掌握证据、模型更新事务和重规划决定的完整 Markdown 文档。
建议文件名为 `<run_id>-S7-review.md`。

## 1. 三工件顺序

先完成 Markdown 掌握验证与重规划报告，再将同一证据、判断、补丁和路由无损结构化为规范 JSON，
校验对应关系后由最终 JSON 派生交互 HTML。Markdown 是首要人审文档，JSON 是机器移交规范表示，
HTML 是只读展示。模型更新只能由真实事务结果描述，文档或页面不得执行更新。

## 2. 必须使用的文档结构

1. `# S7 掌握验证与重规划审核报告`
2. `## 1. 文档与运行信息`
3. `## 2. 输入、历史模型与版本事务审计`
4. `## 3. 预先确定的掌握规则`
5. `## 4. 六维掌握证据`
6. `## 5. 节点级掌握判断与证据充分性`
7. `## 6. 问题归因与上游定位`
8. `## 7. 不可变证据追加与模型补丁`
9. `## 8. 版本检查、持久化结果与前后差异`
10. `## 9. 路由决定与下一会话`
11. `## 10. 复测、复习与维护计划`
12. `## 11. 来源反馈、失效下游与适用限制`
13. `## 12. G7 质量评价与最终路由`
14. `## 13. 输出审计与 JSON 对应表`

## 3. 阶段内容与 JSON 对应

| 内容块 | 必须完整呈现 | 主要 JSON Pointer |
|---|---|---|
| 输入/事务审计 | G6 工件、学习者模型、当前/期望版本、持久层可用性、缺失或冲突 | `/input_contract`、`/input_validation`、`/requirement_gaps` |
| 掌握规则 | 测评前已确定的判据、阈值、失败动作和禁止外推 | `/processing_record`、`/positive_artifact/content/mastery_verification` |
| 六维证据 | 正确性、推理、提示依赖、迁移、置信度、延迟保持；含未执行项 | `/evidence_collected`、`/positive_artifact/content/mastery_verification` |
| 节点判断 | 每节点状态、证据引用、充分/不足原因和可适用范围 | `/positive_artifact/content/mastery_verification` |
| 归因 | 主/次归因、排除理由、最早污染阶段和证据 | `/positive_artifact/content/mastery_verification/attribution`、`/positive_artifact/content/mastery_verification/not_mastered_cause` |
| 证据与补丁 | 不可变证据事件、每个补丁的 before/after、理由及引用 | `/positive_artifact/content/learner_model_update_and_replan/append_evidence`、`/positive_artifact/content/learner_model_update_and_replan/model_patch` |
| 事务结果 | 版本检查、应用/冲突/未执行、持久化事实和模型差异 | `/positive_artifact/content/learner_model_update_and_replan/update`、`/positive_artifact/content/learner_model_update_and_replan/update_status` |
| 路由/计划 | continue/remediate/retest/complete 决定、route_to、下一会话、复习计划 | `/positive_artifact/content/learner_model_update_and_replan/decision`、`/positive_artifact/content/learner_model_update_and_replan/next_session_contract`、`/positive_artifact/content/learner_model_update_and_replan/review_schedule`、`/positive_artifact/content/route` |
| 来源反馈 | 过期/错误/缺口影响的主张、节点、事件、查询和失效下游 | `/positive_artifact/content/learner_model_update_and_replan/evidence_feedback` |
| G7 与路由 | 分维量规、证据、裁决和确定性路由 | `/quality_evaluation` |

## 4. 完整性要求

- 六维证据必须逐项说明“观察、状态、证据引用、缺失和影响”，不得压缩成单一分数。
- 每个模型补丁必须显示 before/after 并引用新证据；版本冲突或无历史模型时不得声称已更新。
- 单题正确、学习者自述或页面中存在提示阶梯均不能被外推为掌握。
- 阻断/冲突也必须产出完整诊断报告和恢复顺序；禁止版本 0 占位、全未掌握假画像、`TBD` 或 `TODO`。

## 5. 输出审计

末章列出三工件路径和逐章节对应表。证据事件、节点判断、归因、补丁、版本和路由必须逐项一致；任何
Markdown 中的限制或失败事实若未进入 JSON，`json_correspondence` 必须失败。
