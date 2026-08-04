---
name: al-s6-run-instructional-interaction
description: 在统一项目级 LLM Wiki 中执行 S6 教学内容与真实交互。业务规则读取 `.agents/stage-profiles.json#S6`；缺 G2–G5 时阻断并路由，前置通过后在 sessions/<session-id> 分离材料、原文、提示、事件和候选证据。
---

# S6 教学内容与真实交互

读取共享项目合同、独立调用合同、runtime contract、manifest/profile S6，以及项目根、project-state、conversation、S6 阶段和当前 session。

## 独立调用

- 无项目：route S1。
- G2/G3/G4/G5 缺失、计划未确认或版本失效：blocked，route 最早缺失阶段。
- 前置通过但学习者尚未作答：`pending → S6`，不得代写。
- 只有讲义或“懂了”不构成行为证据。

## 正常执行

按 profile 创建真实 session，分离 session brief、materials、interaction、events、evidence 和 reflection；按 S5 策略执行解释、示范、对比、提示、撤架、反馈与独立迁移。计划提示不等于实际提示。

只有内容、交互、候选证据、conversation、revision、ID、索引和 verification 全部通过，才能 `G6=pass → S7`。G6 只放行验证，不宣布掌握。
