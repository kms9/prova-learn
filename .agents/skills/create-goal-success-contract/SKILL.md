---
name: create-goal-success-contract
description: 将模糊学习诉求、职业目标或能力愿望校准为经过外部预检、可观察、可验收并由用户确认的 goal_success_contract。只要用户要开始新的个性化学习目标、改变既有目标、定义“学会”的证据，或需要校正岗位/领域名称，就使用本 skill。
---

# 目标与成功契约（S1）

把目标定义错误隔离在流程最前端。不要直接生成课程表，也不要把投入时长、看完材料或选择题分数当成能力。

## 开始前

1. 读取 [stage-contract.md](references/stage-contract.md)。
2. 读取 [handoff-envelope.schema.json](references/handoff-envelope.schema.json) 和 [goal-success-contract.schema.json](references/goal-success-contract.schema.json)。
3. 仅在需要理解输出形状时读取 [example.md](references/example.md)；案例数据是设计夹具，不是真实观察。

## 执行

1. 校验是否至少有一个目标问题或使用场景；记录缺失约束，不把推断写成已确认事实。
2. 收集目标场景、受众、地区/行业/职级、时间、资源、输出形式、排除项和最终验收方式。
3. 执行轻量外部预检：
   - 术语、别名和相邻概念；
   - 相关真实任务、岗位或实践；
   - 面试、实操、认证或其他可观察评估方式；
   - S2 可继续追溯的一手来源入口。
4. 把模型知识只标为 `model_hypothesis`。把招聘样本标为 `market_signal`；只有实际检索到的可访问来源才能标为 `external_evidence`。
5. 展示术语校正、目标选项、成功证据、范围和关键假设，执行强制确认。
6. 将目标反推成可观察能力阶梯和未见验收任务；区分记忆、解释、应用、诊断、迁移和创造。
7. 生成 `goal_success_contract`，再按 G1 量规逐项评价。

## Fail closed

- 无联网/检索能力时，输出 `research_blocked`，保持 G1 失败；不要用模型记忆替代预检。
- 强制确认未完成时，保持 `pending`；不要进入 S2。
- 关键来源缺失时记录 `gap`、重要性和门禁影响；“找不到”不等于 `not_applicable`。
- 用户根本改变目标时重新执行 S1，不在下游静默改写目标。

## 输出

只输出符合两个 Schema 的 JSON 移交信封。先生成具名正向工件，再生成 `quality_evaluation`。只有外部预检已执行、核心能力均有可观察证据、验收任务与目标对齐且确认完成时，才允许 `verdict=pass`、`route_to=S2`。
