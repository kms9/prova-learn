---
name: al-s3-build-capability-concept-graph
description: 在统一项目级 LLM Wiki 中执行 S3 能力—概念图建模。业务规则读取 `.agents/stage-profiles.json#S3`；缺项目或 G1/G2 时阻断并路由最早缺失阶段，不得用课程目录、裸 JSON 或旧 envelope 补造图谱。
---

# S3 能力—概念图建模

读取共享项目合同、独立调用合同、runtime contract、manifest/profile S3，以及项目根、project-state、conversation 和 `stages/s3-capability-graph/INDEX.md`。旧三工件与 HTML 仅兼容导出。

## 独立调用

- 无项目：route S1，不写孤立图谱。
- 旧 run：先迁移。
- G1/G2 缺失、失效或 entrypoint 不可解析：记录 blocked 事务，route 最早缺失阶段。
- 用户要求补齐上游时，退出 S3，逐阶段调用；不得在 S3 搜索后假装 S2 已通过。

## 正常执行

按 profile 建立能力层级、学习单元、唯一节点、先修边、测评和全链路追溯。层级、覆盖和先修分开；硬先修无环；节点事实来自已审计 S2 证据。

只有图谱业务质量、前置、conversation、revision、ID、索引和 verification 全部通过，才能 `G3=pass → S4`。主题目录、孤儿节点、环、无来源或无评估时不得通过。
