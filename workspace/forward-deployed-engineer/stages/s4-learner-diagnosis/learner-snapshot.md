# S4 学习者快照状态

- snapshot_status：`not_created`
- learner_id：`local-learner`
- model_version：`not_established`
- as_of：`2026-08-04T12:24:00Z`
- reason：尚未收到真实学习者回答。

当前没有节点状态、最近学习前沿、误概念、能力缺口、迁移表现或置信度校准结论。不得把“未作答”编译成“全部未掌握”，也不得创建版本 0。首个可持久化快照只有在 D1–D4 产生足够真实行为证据并通过 G4 后才从 version 1 开始。

## 恢复条件

学习者按 [诊断计划](diagnostic-plan.md) 提交作答后：原样记录回答与帮助使用 → 按事前规则形成观察 → 必要时追加撤除提示的复测 → 建立首个 learner_snapshot v1 → 评价 G4。
