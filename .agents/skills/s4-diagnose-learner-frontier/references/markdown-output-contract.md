# S4 完整 Markdown 文档契约

本文件规定 S4 的第一份必交工件：可审核任务设计、行为证据和学习前沿推断的完整 Markdown 文档。
建议文件名为 `<run_id>-S4-review.md`。

## 1. 三工件顺序

先写完整 Markdown 诊断报告，再把同一观察、推断和状态无损结构化为规范 JSON，校验对应关系后再由
最终 JSON 派生交互 HTML。Markdown 是首要人审文档，JSON 是机器移交规范表示，HTML 只读展示。
原始行为、诊断推断与路由决策必须在三者中保持分层。

## 2. 必须使用的文档结构

1. `# S4 学习者前沿诊断审核报告`
2. `## 1. 文档与运行信息`
3. `## 2. 上游输入、模型版本与有效性审计`
4. `## 3. 诊断目标、范围与事前判定规则`
5. `## 4. 诊断任务与覆盖设计`
6. `## 5. 学习者行为证据记录`
7. `## 6. 节点状态逐项判断`
8. `## 7. 错误类型、提示依赖与置信度校准`
9. `## 8. 最近学习前沿及候选比较`
10. `## 9. 误概念、能力缺口与迁移表现`
11. `## 10. 待复测、人工确认与恢复条件`
12. `## 11. 证据有效期与诊断限制`
13. `## 12. G4 质量评价与路由`
14. `## 13. 输出审计与 JSON 对应表`

## 3. 阶段内容与 JSON 对应

| 内容块 | 必须完整呈现 | 主要 JSON Pointer |
|---|---|---|
| 输入审计 | 目标/图谱工件、版本、学习者记录、时间和身份有效性 | `/input_contract`、`/input_validation`、`/positive_artifact/content/model_version` |
| 事前规则 | 每节点何时算掌握、未掌握或证据不足，以及复测触发 | `/processing_record`、`/confirmation` |
| 任务设计 | 解释、预测、反例、诊断、比较、迁移和置信度任务的节点覆盖 | `/processing_record`、`/positive_artifact/content/diagnosis_evidence_mapping` |
| 行为证据 | 回答、推理、提示、修正、耗时（可得时）、置信度与来源 | `/evidence_collected` |
| 节点判断 | 每节点状态及全部证据引用，不把自评直接写为掌握 | `/positive_artifact/content/node_states` |
| 依赖与校准 | 错误类型、实际提示依赖、自评和观察一致性 | `/positive_artifact/content/node_states` |
| 学习前沿 | 最近可学习节点、选择理由、证据及备选候选 | `/positive_artifact/content/learning_frontier` |
| 缺口与迁移 | 误概念、能力缺口、迁移状态和证据 | `/positive_artifact/content/misconceptions`、`/positive_artifact/content/capability_gaps`、`/positive_artifact/content/transfer_performance` |
| 后续动作 | 复测、人审、无回答/冷启动时的恢复条件 | `/positive_artifact/content/items_needing_retest_or_human_confirmation`、`/requirement_gaps` |
| 有效性 | 有效期、过期证据、适用限制和禁止外推 | `/positive_artifact/content/evidence_validity` |
| G4 与路由 | 分维量规、裁决、最早污染阶段与下一动作 | `/quality_evaluation` |

## 4. 完整性要求

- 必须逐条保留“观察到什么→如何解释→为何得到状态”的链条，不得只输出 `mastered/not_mastered` 列表。
- 明确区分答对、独立完成和迁移；提示使用必须来自真实事件，不能从计划提示阶梯反推。
- 无真实回答时仍生成完整诊断设计文档，但不得模拟学习者行为或伪造快照。
- 禁止 `TBD`、`TODO`、空证据表、默认全未掌握画像或版本 0 占位。

## 5. 输出审计

末章列出三工件路径和逐章节对应表。`node_id`、`evidence_id`、提示等级、前沿节点和状态在 Markdown
与 JSON 中必须一致；任一结论缺少可解析证据引用时，对应校验失败。

