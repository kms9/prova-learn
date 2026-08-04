# G1 评价

| Dimension | Evidence refs | Score | Threshold | Passed | Failure action | Route |
|---|---|---:|---:|---|---|---|
| 目标可观察 | `goal-contract.md`,`CAP-001`–`CAP-006` | 1 | 1 | true | none | S2 |
| 成功标准可判定 | `goal-contract.md#最终验收`,`#通过规则` | 1 | 1 | true | none | S2 |
| 场景真实 | `confirmation.md`,`goal-contract.md#真实使用场景` | 1 | 1 | true | none | S2 |
| 外部现实校准 | `SRC-003`–`SRC-010`,`evidence-table.md` | 1 | 1 | true | none | S2 |
| 六类覆盖 | `coverage.md` | 1 | 1 | true | none | S2 |
| 边界与排除项 | `goal-contract.md#范围`,`#排除项`,`#风险与隐私` | 1 | 1 | true | none | S2 |
| 约束完整 | `goal-contract.md#约束`,`confirmation.md` | 1 | 1 | true | none | S2 |
| 目标—能力—验收一致 | `goal-contract.md`,`capabilities.jsonl` | 1 | 1 | true | none | S2 |
| conversation 和事件追溯 | `CONV-20260804T113555Z-s1-confirm`,`records.jsonl` | 1 | 1 | true | none | S2 |
| 项目版本与索引一致 | `project-state.json`,`INDEX.md`,`timeline.md` | 1 | 1 | true | none | S2 |
| mandatory 用户确认 | `confirmation.md`,`EVT-20260804T113555Z-s1-003` | 1 | 1 | true | none | S2 |

- gate_id：`G1`
- gate_revision：`2`
- verdict：`pass`
- route_to：`S2`
- evaluated_by_event_id：`EVT-20260804T113555Z-s1-005`
- reason：目标、模拟使用场景、六项能力、验收、范围、约束、外部预检、追溯与用户 mandatory 确认全部满足 G1。
