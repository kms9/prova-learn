---
name: al-s5-plan-learning-sessions
description: 在统一项目级 LLM Wiki 中执行 S5 路径、策略与会话规划。业务规则读取 `.agents/stage-profiles.json#S5`；缺 G1/G3/G4 时阻断并路由，前置通过后基于真实前沿输出策略政策、会话和 mandatory 确认。
---

# S5 路径、策略与会话规划

读取共享项目合同、独立调用合同、runtime contract、manifest/profile S5，以及项目根、project-state、conversation 和 `stages/s5-learning-plan/INDEX.md`。

## 独立调用

- 无项目：route S1。
- G1/G3/G4 缺失或版本失效：记录 blocked 事务，route 最早缺失阶段。
- 裸课程表不能替代图谱或学习者前沿，先作为 unverified 输入路由所属上游。
- 前置通过但路径确认未完成：`pending → S5`。

## 正常执行

按 profile 选择最小连通路径，在 `strategy-policy.md` 分层记录获得、练习、保持、验收策略及适用/禁用条件、证据和切换规则；定义会话、日程、复习和退出标准。

只有业务量规、mandatory 确认、conversation、revision、ID、索引和 verification 全部通过，才能 `G5=pass → S6`。不得猜测前沿或用章节/题量代替能力节点。
