# G1 量规评价 — run-20260727-234421（初中数学·双师）

> verdict = `pass`；route_to = `S2`。目标=初中数学双师教培教研岗；全部维度 `passed=true` 且 `confirmation.status=confirmed`。紧时间（4–6 周）作为已知风险交 S5 排程，不阻塞 G1。

| Dimension | Evidence | Score | Threshold | Passed | Failure_action | Route |
| --- | --- | --- | --- | --- | --- | --- |
| 目标可观察性 | CAP-001..007（初中数学·双师）每项≥1可观察证据 | met | 每项≥1 | true | — | — |
| 成功标准可判定性 | 三件未见产物 + unseen_or_transfer_required=true | met | true | true | — | — |
| 场景真实性 | target_scene=初中数学双师教研岗（主讲+辅导师双端） | filled | 非空 | true | — | — |
| 外部现实校准度 | TERM-001..004 已校准（教培双师 vs 公立） | covered | 有校正 | true | — | — |
| 强制类别覆盖 | coverage.md 六类 covered | covered | 六类 | true | — | — |
| S2 研究范围可执行 | role+学段+学科+机构+地区(全国) 确认；六源种子齐 | met | 明确 | true | — | — |
| 边界清晰 | exclusions：销售/行政/公立/高中/非数学 | met | 非空 | true | — | — |
| 约束完整 | 时间≈4–6 周（更紧）、形式 markdown+产物、风险 medium-high | met | 时间/形式约束 | true | — | — |
| 目标—验收一致 | pass_rules 与三件产物验收对齐 | met | 对齐 | true | — | — |
| 外部证据真实 | sources.jsonl accepted external_evidence=15 | 15 | ≥1 | true | — | — |
| 跨文件互引可解析 | 全部 source/cap/term 引用可解析 | ok | true | true | — | — |

裁决：`verdict=pass`，`route_to=S2`。所有维度通过 + `confirmation.status=confirmed` + sources.jsonl ≥1 accepted external_evidence + 跨文件 ID 可解析。
