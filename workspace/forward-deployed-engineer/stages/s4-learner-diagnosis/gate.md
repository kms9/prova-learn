# G4 当前评价

| Dimension | Evidence refs | Score | Threshold | Passed | Failure action | Route |
|---|---|---:|---:|---|---|---|
| 测量与目标对齐度 | `diagnostic-plan.md` 第一层覆盖高信息核心簇，第二层按需探针 | 1 | 1 | true | none | S4 |
| 子项—指标—节点映射 | Q1-a…Q4 已映射 indicator、node、threshold、confounds | 1 | 1 | true | none | S4 |
| 诊断负担 | 第一层预计 8–12 分钟，允许分批提交 | 1 | 1 | true | none | S4 |
| 证据充分性 | 尚无真实 `learner_behavior` observation | 0 | 1 | false | revise_here | S4 |
| 猜对与提示识别 | 尚无作答和实际提示事件 | 0 | 1 | false | revise_here | S4 |
| 节点最小证据规则 | 尚无两项独立观察或表现+迁移/保持证据 | 0 | 1 | false | revise_here | S4 |
| 偏差与混淆控制 | 已显式区分写作、行业熟悉度、搜索/记忆和时间压力 | 1 | 1 | true | none | S4 |
| 模拟证据隔离 | 主项目未引用 `simulations/**`，未创建 synthetic observation | 1 | 1 | true | none | S4 |
| 前沿可解释性 | 尚无节点状态和最近学习前沿 | 0 | 1 | false | revise_here | S4 |
| 诊断素材有效性 | S2/S3 来源、节点和任务边界仍有效 | 1 | 1 | true | none | S4 |

- gate_id：`G4`
- gate_revision：`2`
- stage_status：`pending`
- verdict：`blocked`
- route_to：`S4`
- evaluated_by_event_id：`EVT-20260804T122400Z-s4-008`
- reason：诊断设计已升级为短筛查与自适应探针，但尚未收到真实学习者回答；不创建 learner snapshot，不进入 S5。

## 恢复条件

1. 学习者提交 Q1–Q4，可分批；
2. 原样记录回答、理由、置信度和帮助使用；
3. 以子项形成 observation；
4. 仅对冲突、关键先修不确定或可能猜对的节点追加 P1–P4；
5. 关键节点满足两项独立观察，或完整表现任务加无提示迁移/延迟复测；
6. 形成可用于 S5 的最近学习前沿，未测节点允许保持 `unknown`。
