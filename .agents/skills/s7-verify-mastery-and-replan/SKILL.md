---
name: al-s7-verify-mastery-and-replan
description: 在统一项目级 LLM Wiki 中执行 S7 掌握验证、模型更新与重规划。业务规则读取 `.agents/stage-profiles.json#S7`；缺 G3–G6 或历史模型时按最早根因路由，禁止版本 0、单题过度更新和无后端伪持久化。
---

# S7 掌握验证、模型更新与重规划

读取共享项目合同、独立调用合同、runtime contract、manifest/profile S7，以及项目根、project-state、conversation、图谱、历史快照、计划和 session。

## 独立调用

- 无项目：route S1。
- G3/G4/G5/G6 缺失或失效：blocked，route 最早缺失阶段。
- 无历史 learner snapshot/model_version<1：route S4，禁止版本 0。
- 前置通过但等待补测或延迟保持：`pending → S7`。
- revision 或 learner model version 冲突：不应用补丁。

## 正常执行

按 profile 综合正确性、推理、提示、迁移、置信度和延迟保持；记录掌握事件、版本化模型更新、策略选择/执行归因、重规划、复测和 route。

G7 评价事务质量，不等同学习者掌握。只有 GOAL_ACHIEVED 且最终验收与保持通过，才能 complete；否则按最早污染源 route S1–S7。
