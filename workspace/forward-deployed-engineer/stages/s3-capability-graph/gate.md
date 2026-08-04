# G3 评价

| Dimension | Evidence refs | Score | Threshold | Passed | Failure action | Route |
|---|---|---:|---:|---|---|---|
| 结构无环性 | `edges.jsonl` | 1 | 1 | true | none | S4 |
| 层级与引用完整性 | `capability-map.md`,`learning-units.md` | 1 | 1 | true | none | S4 |
| 学习单元核心覆盖 | 12 个 core mapping | 1 | 1 | true | none | S4 |
| 必需节点无孤儿 | 12/12 nodes covered | 1 | 1 | true | none | S4 |
| 原子节点唯一性 | `nodes.jsonl` | 1 | 1 | true | none | S4 |
| 先修边可解释性 | 13/13 edges 有 rationale | 1 | 1 | true | none | S4 |
| 目标覆盖率 | 6/6 CAP 各 2 nodes | 1 | 1 | true | none | S4 |
| 节点粒度一致性 | 12 个可独立测判断/工件 | 1 | 1 | true | none | S4 |
| 能力与概念区分度 | node_type + observable statement | 1 | 1 | true | none | S4 |
| 评估题有效性 | 12/12 ASM + threshold + remediation | 1 | 1 | true | none | S4 |
| 全链路可追溯性 | `traceability.md` | 1 | 1 | true | none | S4 |
| 六源归一化完整性 | 16/16 EVID mapped | 1 | 1 | true | none | S4 |
| 核心进入规则 | 12/12 status/tier/freshness | 1 | 1 | true | none | S4 |
| 岗位深度建模 | 3-level ladder | 1 | 1 | true | none | S4 |

- gate_id：`G3`
- gate_revision：`1`
- verdict：`pass`
- route_to：`S4`
- confirmation：`conditional / acknowledged`
- evaluated_by_event_id：`EVT-20260804T120500Z-s3-008`
- reason：输入有效，能力/单元/节点/先修/评估/阈值/追溯与三工件全部通过；无环、无孤儿、无证据阻断。
