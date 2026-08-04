# G4 当前评价

| Dimension | Evidence refs | Score | Threshold | Passed | Failure action | Route |
|---|---|---:|---:|---|---|---|
| 测量与目标对齐度 | `diagnostic-plan.md` 覆盖 12/12 nodes | 1 | 1 | true | none | S4 |
| 证据充分性 | 无 learner_behavior observation | 0 | 1 | false | revise_here | S4 |
| 猜对识别 | 尚无作答可比较 | 0 | 1 | false | revise_here | S4 |
| 提示依赖记录 | 尚无真实提示事件 | 0 | 1 | false | revise_here | S4 |
| 错误分类一致性 | 尚无错误/推理证据 | 0 | 1 | false | revise_here | S4 |
| 偏差控制 | 未用自评/年限覆盖行为 | 1 | 1 | true | none | S4 |
| 结论可解释性 | 无节点结论或前沿可追溯 | 0 | 1 | false | revise_here | S4 |
| 诊断素材有效性 | S2/S3 来源、任务和动态边界有效 | 1 | 1 | true | none | S4 |

- gate_id：`G4`
- gate_revision：`1`
- stage_status：`pending`
- verdict：`blocked`
- route_to：`S4`
- evaluated_by_event_id：`EVT-20260804T122400Z-s4-008`
- reason：前置和诊断设计有效，但没有真实学习者回答；G4 不通过，不生成快照，不进入 S5。

## 恢复条件

提交 D1–D4 的真实答案、理由、置信度和帮助使用情况；若证据冲突或依赖中高提示，再执行针对性复测。只有多项有效行为形成最近学习前沿后，G4 才可重新评价为 pass。
