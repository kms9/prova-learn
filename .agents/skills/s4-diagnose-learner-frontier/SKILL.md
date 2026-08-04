---
name: al-s4-diagnose-learner-frontier
description: 在统一项目级 LLM Wiki 中执行 S4 学习者诊断与学习前沿。业务规则读取 `.agents/stage-profiles.json#S4`；缺 G1/G3 时记录阻断事务，前置通过但没有真实回答时保持 pending，不得模拟学习者行为。
---

# S4 学习者诊断与学习前沿

读取共享项目合同、独立调用合同、runtime contract、manifest/profile S4，以及项目根、project-state、conversation 和 `stages/s4-learner-diagnosis/INDEX.md`。

## 独立调用

- 无项目：route S1。
- G1/G3 缺失或失效：blocked，route 最早缺失阶段。
- 前置已通过但无真实学习者回答：可以生成 diagnostic plan，状态保持 `pending → S4`，不回退、不模拟。
- 裸学习记录标 `user_provided_unverified`，由 S4 验证后才能成为观察。

## 正常执行

按 profile 记录事前规则、真实回答、提示、推理、错误、置信度、迁移、误概念、复测和模型事件。关键结论由多项行为支持，区分答对、独立、迁移和证据不足。

只有业务量规、conversation、revision、ID、索引和 verification 全部通过，才能 `G4=pass → S5`。单题、自评、年限或偏好问卷不得决定掌握。
