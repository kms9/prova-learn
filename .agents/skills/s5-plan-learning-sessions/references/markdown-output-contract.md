# S5 完整 Markdown 文档契约

本文件规定 S5 的第一份必交工件：可审核路径取舍、会话、测评和时间可行性的完整 Markdown 文档。建议
文件名为 `<run_id>-S5-review.md`。

## 1. 三工件顺序

先写完整 Markdown 计划，再将同一路径、理由和约束无损结构化为规范 JSON，校验对应关系后，由最终 JSON
派生交互 HTML。Markdown 是首要人审文档，JSON 是机器移交规范表示，HTML 是只读展示。不得先生成
简化 JSON 再用泛化文字补齐 Markdown。

## 2. 必须使用的文档结构

1. `# S5 学习路径与会话计划审核报告`
2. `## 1. 文档与运行信息`
3. `## 2. 输入、版本与学习前沿审计`
4. `## 3. 用户约束、取舍与确认结果`
5. `## 4. 路径选择原则与最小连通子图`
6. `## 5. 有序学习节点详解`
7. `## 6. 会话编排与材料`
8. `## 7. 支架、撤架与教学策略`
9. `## 8. 即时、迁移与延迟测评`
10. `## 9. 复习锚点与时间预算`
11. `## 10. 风险、备选路线与触发条件`
12. `## 11. 节点退出标准与总体完成条件`
13. `## 12. G5 质量评价与路由`
14. `## 13. 输出审计与 JSON 对应表`

## 3. 阶段内容与 JSON 对应

| 内容块 | 必须完整呈现 | 主要 JSON Pointer |
|---|---|---|
| 输入审计 | G1/G3/G4 工件、版本、门状态、前沿证据和兼容性 | `/input_contract`、`/input_validation`、`/requirement_gaps` |
| 约束与确认 | 时间、节奏、资源、形式、用户取舍、首会话确认 | `/confirmation`、`/assumptions` |
| 路径原则 | 前沿到目标的连通性、硬先修、跳过依据、最小性 | `/processing_record`、`/positive_artifact/content/ordered_learning_nodes` |
| 节点详解 | 顺序、选择理由、证据等级/状态/时效/来源、教学策略、支架和撤架条件 | `/positive_artifact/content/ordered_learning_nodes` |
| 会话 | 每次会话目标、活动、材料、时间、进入条件和预期产物 | `/positive_artifact/content/sessions` |
| 测评 | 即时、迁移、延迟测评及其节点对应 | `/positive_artifact/content/assessment_schedule` |
| 复习和预算 | 复习锚点、间隔、总时间和约束校验 | `/positive_artifact/content/review_anchors`、`/positive_artifact/content/sessions` |
| 风险与替代 | 风险、严重性、缓解、触发条件和路线调整 | `/positive_artifact/content/risks`、`/positive_artifact/content/alternative_routes` |
| 退出标准 | 每节点可观察判据和总体完成条件 | `/positive_artifact/content/exit_criteria` |
| G5 与路由 | 分维量规、确认门、裁决和下一阶段 | `/quality_evaluation` |

## 4. 完整性要求

- 不能输出课程目录式计划；每个节点都要说明“为何现在学、依据是什么、怎样教、何时撤架、如何判定退出”。
- 时间预算必须覆盖会话与延迟复测，且首个会话可直接执行。
- 前沿证据不足时完整记录返回 S4 的原因，不得用计划假设补成已确定起点。
- `pending`/`blocked` 仍产出完整计划诊断文档；禁止 `TBD`、`TODO`、空会话或占位路线。

## 5. 输出审计

末章列出三工件路径和逐章节对应表。节点顺序、时间、会话数量、测评、风险及退出标准必须在 Markdown
与 JSON 中逐项一致；删节任何失败条件或备选路线均视为对应失败。

