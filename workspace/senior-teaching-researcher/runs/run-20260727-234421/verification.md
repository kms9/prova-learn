# Verification — run-20260727-234421（初中数学·双师）

- state: `verified`
- source_summary: { accepted: 24, accepted_external_evidence: 15, needs_metadata: 0, rejected: 0, trace_only: 0 }
- capability_count: 7（CAP-001..007，初中数学·双师）
- confirmation_status: `confirmed`
- g1_verdict: `pass` / route_to: `S2`
- unresolved_risks（不阻塞 G1，交下游处理）:
  - R001 | medium | 时间紧（4–6 周）覆盖 7 项能力偏紧，可能需 S5 压缩范围（优先 CAP-001/002/006） | action: 交 S5 排程
  - R002 | medium | CAP-003/004/007 单/弱来源（双师体系、辅导师培训、负责人级规划） | action: S2 补头部双师机构一手案例
  - R003 | low | 是否具备真实教研场景/数据未显式确认（默认按可用规划） | action: S5 复核，无则改用公开样本
- commands:
  - 静态校验：JSONL 可解析、跨文件 ID 解析（已自检通过）
  - S1 evals：待 `run_skill_evals.py` 支持目录评分（后续）
- files_created:
  - INDEX.md, sources.jsonl(24), evidence_table.md, coverage.md, capabilities.jsonl(7), terminology.jsonl(4), goal-contract.md, research-brief.md, confirmation.md, g1-evaluation.md, verification.md

## 结论

S1 完成：**初中数学 双师/O2O 教培教研岗** 目标契约已校准、强制确认完成、G1 `pass`、路由至 **S2**。下游经 `INDEX.md` 读取本 run folder；`research-brief.md` 为 S2 主要消费页。
