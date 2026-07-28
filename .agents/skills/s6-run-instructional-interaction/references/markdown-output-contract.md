# S6 完整 Markdown 文档契约

本文件规定 S6 的第一份必交工件：可审核教学内容、支架和真实交互证据的完整 Markdown 文档。建议
文件名为 `<run_id>-S6-review.md`。

## 1. 三工件顺序

先完成 Markdown 教学与交互记录，再将同一内容、事件和候选证据无损结构化为规范 JSON，校验对应关系
后由最终 JSON 派生交互 HTML。Markdown 是首要人审文档，JSON 是机器移交规范表示，HTML 只读展示。
教学内容、学习者作答和模型推断不得混写。

## 2. 必须使用的文档结构

1. `# S6 教学内容与交互审核报告`
2. `## 1. 文档与运行信息`
3. `## 2. 输入、当前节点与会话契约审计`
4. `## 3. 来源、知识状态与内容边界`
5. `## 4. 分层解释与多重表征`
6. `## 5. 正例、反例、边界案例与常见误解`
7. `## 6. 学习活动与答案泄露控制`
8. `## 7. 提示阶梯、反馈规则与撤架策略`
9. `## 8. 真实交互事件与修正轨迹`
10. `## 9. 候选掌握证据`
11. `## 10. 未解决问题、内容修订与适用限制`
12. `## 11. G6 质量评价与路由`
13. `## 12. 输出审计与 JSON 对应表`

## 3. 阶段内容与 JSON 对应

| 内容块 | 必须完整呈现 | 主要 JSON Pointer |
|---|---|---|
| 输入审计 | 当前计划、节点、图谱、证据全景、快照、目标和退出标准 | `/input_contract`、`/input_validation`、`/positive_artifact/content/current_node` |
| 内容来源 | 每条关键解释的来源、知识状态、时效、边界和未核验项 | `/evidence_collected`、`/positive_artifact/content/explanations` |
| 分层解释 | 不同层级、表征、认知水平及抽象—具体连接 | `/positive_artifact/content/explanations` |
| 案例 | 正例、反例、边界、常见误解和纠正路径 | `/positive_artifact/content/examples` |
| 活动 | 检索、示例、半完成、对比、独立迁移及学习者输出要求 | `/positive_artifact/content/activities` |
| 支架 | 提示步骤、强度、反馈规则、初始支架、撤架和终止条件 | `/positive_artifact/content/hint_ladder`、`/positive_artifact/content/feedback_rules`、`/positive_artifact/content/scaffolding_fade_strategy` |
| 交互轨迹 | 原始作答、实际提示、修正步骤、反馈和仍未解决项 | `/positive_artifact/content/interaction_events` |
| 候选证据 | 节点、维度、状态、证据事件和适用限制；不得提前宣布掌握 | `/positive_artifact/content/candidate_mastery_evidence` |
| 内容质量 | 审核对象、发现的错误、修订和限制 | `/positive_artifact/content/content_quality_status`、`/requirement_gaps` |
| G6 与路由 | 分维量规、候选证据门、裁决和下一动作 | `/quality_evaluation` |

## 4. 完整性要求

- 每条关键解释必须可追溯，不能用“常识”代替来源；案例必须说明为何属于正/反/边界。
- 必须区分计划提示阶梯和实际使用提示；没有学习者作答时不得生成虚构交互或掌握候选。
- 教学讲义结束不等于阶段完成，学习者说“懂了”也不是可判定证据。
- 阻断时仍完整记录可用内容、缺失输入、不可执行活动和恢复顺序；禁止 `TBD`、`TODO`、假作答或空占位。

## 5. 输出审计

末章列出三工件路径和逐章节对应表。解释、活动、事件、提示使用与候选证据的稳定 ID/顺序必须一致；
Markdown 中出现而 JSON 未结构化的作答、修正或限制会使一致性失败。

