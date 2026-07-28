# 六源证据到学习图谱协议

## 1. 输入门

只消费同一 LLM Wiki run 中已通过 G2 的 `s2/` 阶段区。先按 S2 九项机读条件检查根 `INDEX.md` →
`s2/INDEX.md`，再读取 `research-answers.md`、`answer-validation.md`、`evidence-items.jsonl`、
`coverage.md` 与 `sources.jsonl`。至少检查：

- 六类证据通道状态、独立样本与关键缺口；
- 统一原子对象的 ID、来源和冲突；
- 多源覆盖矩阵、结构饱和结论和成熟度；
- `consensus / disputed / emerging / insufficient_evidence / deprecated`；
- `stable / dynamic` 时效与已过期来源。
- S1 priority questions 是否全部映射且关键回答的八维校验通过。

关键一级/二级候选未达到覆盖或饱和门时返回 S2，不在 S3 自行补资料或升级证据等级。

## 2. 从原子对象生成三层能力大纲

1. 以目标问题和真实任务聚类 `Task + Capability`，形成一级能力领域。
2. 以“同一组知识共同解决什么问题”聚类为二级问题族或子能力。
3. 把可说明学习结果、可独立测评、可拆原子知识点、可声明先修且关联真实任务的对象形成三级学习单元。
4. 将 `Knowledge / Skill / Practice / Failure / Misconception` 映射到学习单元，复用规范 ID。

禁止使用“招聘要求 / 书籍知识 / 热门论文 / 社区讨论 / 标准 / 案例”作为六个并列大纲章节。
来源是证据维度，不是知识结构。

## 3. 进入核心路径的规则

- `core_stable` 默认进入必修，且应有关键任务、书课/标准和真实应用的交叉支持。
- `core_practice` 在目标任务需要且有多个真实产物或案例支持时进入必修/重点实践。
- `research_frontier` 只有目标明确要求研究或前沿能力时进入主路径，否则标为扩展。
- `emerging_signal` 进入观察或可选项；获得官方、论文或真实产物支持后才能升级。
- `disputed` 必须保留竞争观点、适用条件与评估方式，不得伪装成单一共识。
- `deprecated` 不进入当前核心路径，但可作为历史、迁移或反例节点保留。

## 4. 岗位层级的建模

普通岗位与专家岗位共享概念时，不复制一组“专家术语”。优先在同一能力上表达：

- 自主识别和定义问题的程度；
- 任务复杂度与不确定性；
- 影响范围和决策责任；
- 机制理解、迁移和创造要求；
- 风险承担、标准建立与指导他人的要求；
- 对应的掌握阈值和验收任务难度。

## 5. 图关系与追溯

层级父子只表示组成，`unit_node_mappings` 表示学习单元覆盖，`edges` 只表示学习先修。
根据需要在处理记录或等价结构中保留：

`part_of / prerequisite_of / enables / required_by / applied_in / implemented_by /
evidenced_by / assessed_by / contradicts / evolved_from / fails_when / discussed_in`。

每个核心节点至少可追溯：

`goal → role/capability → learning_unit → node → assessment → evidence/source`。

记录节点的证据层级、知识状态、时效、适用边界和覆盖缺口。动态证据过期或新的反例改变节点语义时，
返回 S2 补证；语义实质变化后生成新 S3 工件版本，并使受影响 S4–S7 工件显式失效。
