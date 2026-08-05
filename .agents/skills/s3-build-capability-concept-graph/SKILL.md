---
name: al-s3-build-capability-concept-graph
description: 在统一项目级 LLM Wiki 中执行 S3 能力—概念图建模。把目标与已审计证据转成能力、学习单元、唯一节点、先修边、可诊断测评和全链路追溯。缺项目或 G1/G2 时阻断并路由最早缺失阶段。
---

# S3 能力—概念图建模

## 1. 权威输入

读取共享项目合同、独立调用合同、runtime contract、manifest/profile S3、项目根、目标版本、S2 当前入口、最近 conversation 和 `stages/s3-capability-graph/INDEX.md`。旧 envelope、HTML 或课程目录只能作兼容输入。

## 2. 独立调用

- 无项目：route S1，不写孤立图谱。
- 旧 run：先迁移。
- G1/G2 缺失、失效或入口不可解析：记录 blocked 事务，route 最早缺失阶段。
- 不得在 S3 临时搜索后假装 S2 已完成；事实缺口必须回 S2。

## 3. 建模层次

建立并保持分层：

```text
goal → capability → sub-capability → learning unit → atomic node
```

- 学习单元是可独立教学和测评的能力片段，不是课程章节。
- 原子节点只能承担一个主要判断，节点类型为 `concept|procedure|strategy|representation|metacognition`。
- 层级、覆盖、多对多支撑和先修关系分开表示。
- 硬先修必须无环，且每条边有可解释理由。
- 未被充分证据支持的内容保持 gap，不为追求图谱完整而补造。

## 4. 节点合同

每个关键节点至少包含：

- 可观察能力陈述；
- 常见误概念与可区分错误；
- 知识状态、时效和适用边界；
- 来源与独立来源组；
- 节点退出标准；
- 补救入口；
- 是否要求迁移或延迟保持。

节点粒度必须允许 S4 区分“不会该节点”和“复合题中其他部分失败”。

## 5. 测评合同

`assessments.jsonl` 的每个测评项或子项至少记录：

```text
assessment_id
item_id / sub_item_id
node_id
observable_indicator
task / stimulus
cognitive_level
threshold
independence_requirement
minimum_observations
requires_transfer
requires_delayed_retention
confounds
remediation
```

约束：

- 一个复合任务可以覆盖多个节点，但必须拆成可独立评分的子项，并建立 `sub_item → indicator → node` 映射。
- 不得只写“D1 覆盖 N-001…N-005”而没有可判定指标。
- 诊断题应允许暴露解释、预测、反例、比较、应用和迁移差异。
- 证据审计任务应提供必要的来源卡或材料，避免把记忆/搜索能力混入构念。
- 开放写作任务要标记写作表达、领域熟悉度和时间压力等潜在混淆。

## 6. 掌握证据规则

S3 只定义证据要求，不推断学习者掌握。

关键节点的默认最小规则：

```text
tested_mastered =
  至少两项相互独立的有效观察
  OR
  一项完整表现任务 + 一项无提示迁移或延迟复测
```

单题、单个复合回答、自评、年限或偏好问卷只能产生候选证据。若领域需要更严格规则，在节点或测评中提升 `minimum_observations`。

## 7. 诊断效率

S3 不要求 S4 冷启动一次覆盖全部节点。应标记：

- 高信息筛查节点；
- 可由先修或依赖关系推断但仍需复测的节点；
- 仅在首轮结果不确定时追加的探针；
- 可以保持 `unknown` 而不阻塞形成最近学习前沿的节点。

这用于支持“短筛查 → 自适应探针”，而不是一次性长考试。

## 8. 追溯

保持：

```text
goal → capability → unit → node → assessment/sub-item → indicator → evidence/source
```

所有稳定 ID 可解析；来源变化、目标版本变化或图谱修改必须记录失效范围。

## 9. G3

G3 至少检查：

1. 目标覆盖但不过度扩张；
2. 节点原子性；
3. 硬先修无环；
4. 无核心孤儿节点；
5. 每个关键节点有来源和测评；
6. 复合任务存在子项映射；
7. threshold、independence 和 `minimum_observations` 可执行；
8. 诊断可支持自适应而非强制全覆盖；
9. 追溯、conversation、revision、索引和 verification 一致。

只有全部通过，才能 `G3=pass → S4`。

## 10. Fail closed

- 只有主题目录、章节名或工具词：`revise_here → S3`。
- 来源不足：route S2。
- 目标不清：route S1。
- 环、孤儿、断链、不可评分测评或复合题无子项映射：G3 不通过。
- 不得将测评存在误写为学习者已经掌握。

## 11. 用户回执

说明能力结构、节点数、硬/软先修、诊断筛查节点、测评子项规则、主要缺口、G3 和 S4 的具体输入。
