---
name: al-s4-diagnose-learner-frontier
description: 在统一项目级 LLM Wiki 中执行 S4 学习者诊断与学习前沿。基于目标、图谱和真实学习行为，用短筛查与自适应探针定位节点状态、误概念、提示依赖、迁移表现和最近学习前沿。无真实回答时保持 pending，不得模拟。
---

# S4 学习者诊断与学习前沿

## 1. 权威输入

读取共享项目合同、独立调用合同、runtime contract、manifest/profile S4、目标版本、S3 节点/边/测评、项目根、最近 conversation 和 `stages/s4-learner-diagnosis/INDEX.md`。

## 2. 独立调用

- 无项目：route S1。
- G1/G3 缺失、失效或测评合同不可解析：blocked，route 最早缺失阶段。
- 前置通过但没有真实学习者回答：可以生成诊断计划，状态保持 `pending → S4`，不回退、不模拟。
- 裸学习记录先标 `user_provided_unverified`，经原文、时间和帮助使用信息核验后才能成为 observation。

## 3. 两级自适应诊断

默认采用：

### 第一层：高信息短筛查

- 目标时长约 8–12 分钟；
- 只测能够最大幅度缩小起点范围的核心节点；
- 混合使用识别、解释、反例、应用和简短迁移；
- 不要求一次覆盖全部节点；未测节点保持 `unknown`。

### 第二层：针对性探针

仅对以下情况追加：

- 首轮证据冲突；
- 关键先修不确定；
- 可能是猜对；
- 提示依赖不清；
- 复合任务无法定位失败节点；
- 需要区分近迁移和远迁移。

用户可以分批提交；阶段保持 pending，不把缺失答案判错。

## 4. 诊断计划与评分映射

`diagnostic-plan.md` 必须包含：

```text
item/sub-item → observable_indicator → node → threshold
→ independence requirement → minimum observations
→ possible confounds → remediation/retest
```

一个开放题覆盖多个节点时，必须拆成可独立评分的子项。不得依据“整题总体不错”同时把多个节点判为掌握。

证据审计、法规、论文或统计判断题应提供最小必要来源卡；目标是测来源判断，不是测是否记住某份材料或能否临时搜索。

长文本任务必须区分：领域理解、写作表达、行业熟悉度、时间压力和工具使用，避免把表达问题直接归因为知识缺口。

## 5. 行为记录

原样记录：

- 回答和关键理由；
- 子项正确性；
- 推理质量；
- 置信度；
- 是否查资料、使用 AI 或获得提示；
- 实际提示级别；
- 耗时（可得时）；
- 错误类型与可能混淆；
- 迁移表现。

observation 以子项为最小粒度，引用原始 transcript。计划中的提示不等于实际提示。

## 6. 节点状态规则

允许状态包括：

```text
unknown
insufficient_evidence
candidate_mastery
partial
tested_not_mastered
tested_mastered
stale
```

`tested_mastered` 默认必须满足：

```text
至少两项相互独立的有效观察
OR
一项完整表现任务 + 一项无提示迁移或延迟复测
```

并同时满足：

- 理由或过程达到阈值；
- 提示依赖为 none/low 且符合节点合同；
- 不存在未解释的构念混淆；
- 置信度不覆盖行为事实。

单题、单个复合回答、自评、年限、偏好问卷和“说懂了”不得产生 `tested_mastered`。证据不够时必须使用 `candidate_mastery`、`partial`、`unknown` 或 `insufficient_evidence`。

## 7. 最近学习前沿

G4 的目标不是把全部节点判定完毕，而是形成一个可用于规划的最近学习前沿。可保留未知节点，只要：

- 关键先修状态足够清楚；
- 前沿结论由真实行为支撑；
- 冲突节点进入 `retests.md`；
- S5 能区分已证实状态与未测状态；
- 不把 unknown 当作未掌握。

## 8. 模拟证据隔离

- 真实项目只接受真实 `learner_behavior`。
- 系统构造答案、fixture 和 `simulations/**` 使用 `synthetic_learner_behavior` 或明确 fixture 标记。
- 模拟证据不得写入真实 `learner-snapshot.md`、`model-events.jsonl`、active learner model 或 project-state。
- 任何真实项目引用 `simulations/**` 都视为证据污染并阻断 G4。

## 9. G4

至少检查：

1. 测量与目标对齐；
2. 子项—指标—节点映射；
3. 诊断负担合理；
4. 真实回答与来源追溯；
5. 猜对、提示和混淆控制；
6. 节点结论满足最小证据数；
7. 错误分类一致；
8. 前沿可解释；
9. 未测节点保持 unknown；
10. 模拟与真实证据隔离；
11. conversation、revision、索引和 verification 一致。

有可用前沿、关键节点证据充分且其他门通过时，才能 `G4=pass → S5`。不要求形式上的 100% 节点覆盖。

## 10. Fail closed

- 无真实回答：`pending → S4`。
- 图谱或测评不可诊断：route S3。
- 领域事实缺失：route S2。
- 单题推导多个 mastered、复合题无子项映射、模拟证据进入真实项目：G4 不通过。
- 不得把未作答编译为全部未掌握。

## 11. 用户回执

直接展示当前最小作答任务、预计时长、是否允许分批回答和帮助标记方式。完成后说明已证实节点、未知节点、前沿、误概念、复测项、G4 与下一步。
