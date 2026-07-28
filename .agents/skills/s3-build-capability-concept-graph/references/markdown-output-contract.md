# S3 完整 Markdown 文档契约

本文件规定 S3 的第一份必交工件：可逐层校对能力结构、知识点和关系依据的完整 Markdown 文档。建议
文件名为 `<run_id>-S3-review.md`。

## 1. 三工件顺序

先形成完整 Markdown，再将全部实质内容无损结构化为规范 JSON，校验章节与 JSON Pointer 对应后，最后
由最终 JSON 生成 S3 交互 HTML。Markdown 是首要人审文档，JSON 是机器移交规范表示，HTML 是只读展示。
三层大纲、原子节点、关系和测评不得只存在于任一单独工件。

## 2. 必须使用的文档结构

1. `# S3 能力—概念图谱审核报告`
2. `## 1. 文档与运行信息`
3. `## 2. G1/G2 输入与建模边界审计`
4. `## 3. 建模焦点与设计原则`
5. `## 4. 三层能力大纲`
6. `## 5. 学习单元详解`
7. `## 6. 原子知识与能力节点`
8. `## 7. 学习单元—节点映射`
9. `## 8. 先修、依赖与关联关系`
10. `## 9. 知识状态、角色深度与适用边界`
11. `## 10. 评估方式、阈值与补救规则`
12. `## 11. 覆盖、缺口、冲突与重复检查`
13. `## 12. 全链路追溯`
14. `## 13. G3 质量评价与路由`
15. `## 14. 输出审计与 JSON 对应表`

## 3. 阶段内容与 JSON 对应

| 内容块 | 必须完整呈现 | 主要 JSON Pointer |
|---|---|---|
| 输入审计 | G1/G2 工件、版本、门状态、证据适用性、缺失/过期项 | `/input_contract`、`/input_validation`、`/requirement_gaps` |
| 焦点 | 图谱服务的目标问题、边界、建模原则、非目标 | `/positive_artifact/content/focus_question`、`/processing_record` |
| 三层大纲 | 一级能力域、二级能力簇、三级可评估学习单元，保留父子关系与范围角色 | `/positive_artifact/content/learning_units` |
| 单元详解 | 每单元的可观察结果、目标/来源引用、适用层级和质量要求 | `/positive_artifact/content/learning_units` |
| 原子节点 | 每节点定义、类型、可观察能力、知识状态、来源、误概念与边界 | `/positive_artifact/content/nodes` |
| 单元映射 | 多对多映射、核心/支撑角色、覆盖理由 | `/positive_artifact/content/unit_node_mappings` |
| 关系 | 硬/软先修、方向、理由、证据和不存在环的验证 | `/positive_artifact/content/edges` |
| 状态与深度 | 稳定核心/实践核心/研究前沿/新兴信号，以及角色能力阶梯 | `/positive_artifact/content/knowledge_status_summary`、`/positive_artifact/content/role_capability_ladder` |
| 评估 | 节点级评估、通过阈值、失败动作、补救与再测 | `/positive_artifact/content/assessment_items`、`/positive_artifact/content/mastery_thresholds`、`/positive_artifact/content/remediation_entries` |
| 覆盖检查 | 目标覆盖、孤儿、重复、悬空引用、关键缺口和下游影响 | `/positive_artifact/content/coverage_and_gap_report` |
| 追溯 | 目标→来源原子→单元→节点→边→评估的完整链路 | `/positive_artifact/content/source_atom_mappings`、`/traceability` |
| G3 与路由 | 分维量规、结构验证、裁决和路由 | `/quality_evaluation` |

## 4. 完整性要求

- 三层大纲必须展开到可评估学习单元；不得以课程目录、章节标题或术语堆叠代替能力结构。
- 每个核心节点必须有定义、可观察表现、来源、边界和评估；每条关键关系必须说明为什么成立。
- 图形只是 HTML 中的一个阅读视图，Markdown 必须提供完整文字/表格等价表达。
- 阻断时仍完整说明已建部分、结构缺口、受影响下游和修复顺序；禁止空表、占位节点、`TBD` 或 `TODO`。

## 5. 输出审计

末章列出三工件路径和逐章节 `section_id → 标题 → JSON Pointer[] → matched/gap/not_applicable` 对应表。
节点、边、映射和评估的计数及稳定 ID 必须在 Markdown 与 JSON 中一致。
