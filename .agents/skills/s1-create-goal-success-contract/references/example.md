# S1 示例 — goal_success_contract run folder

> 下列为**设计夹具**，不是真实观察结果。它们演示 run folder 落盘形态（输入 → run-folder 文件 → 门裁决 → 路由）；eval 执行时不注入执行器提示。`INDEX.md` / `verification.md` 标注 `fixture_type=simulated_fixture`。

## 示例 A（正向）— 成人学习 PostgreSQL 查询优化

**来源追溯**：`docs/chat_log/七步个性化学习SOP正反例与研究依据.md` §S1 正向例子 1（line 94）；端到端案例 `docs/chat_log/七步个性化学习SOP贯穿案例-PostgreSQL查询优化.md` §S1。

**输入事实**

- 诉求："会写 SQL，但遇到 PostgreSQL 慢查询只会试着加索引。希望四周内（每周约 6 小时）能自己看执行计划并做优化。"
- 确认：PostgreSQL 18；仅沙箱；无生产变更权限；目标=诊断并提出可验证改进，非优化器内核。

**run folder**：`workspace/postgresql-query-optimization/runs/run-20260727-192733/`

`sources.jsonl`（节选，每行一条）：

```jsonl
{"source_id":"S001","type":"web","title":"PostgreSQL 18 EXPLAIN","url":"https://www.postgresql.org/docs/18/sql-explain.html","snippet":"EXPLAIN (ANALYZE, BUFFERS) 显示估算与实际执行信息…","query":"PostgreSQL 18 EXPLAIN ANALYZE","retrieved_at":"2026-07-26T10:00:00+08:00","retrieved_by":"web","provenance":"external_evidence","category":"official_academic","trust_note":"官方文档，直接标准页","status":"accepted"}
{"source_id":"S002","type":"web","title":"PostgreSQL DBA JD（样本）","url":"https://example.invalid/jd-postgres-dba","snippet":"…独立诊断慢查询、设计复合索引…","query":"PostgreSQL DBA slow query","retrieved_at":"2026-07-26T10:05:00+08:00","retrieved_by":"web","provenance":"market_signal","category":"recruiting_jd","trust_note":"招聘样本，仅作市场信号","status":"accepted"}
```

`evidence_table.md`（节选）：

| Claim ID | Claim | Source IDs | Support | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| CAP-001 | 从 EXPLAIN (ANALYZE, BUFFERS) 区分估算与实际执行信息 | S001 | supported | high | 官方文档直接支撑 |
| TERM-001 | "学会查询优化" 应收窄为 "诊断并改进单表查询性能" | S002 | partially_supported | medium | JD 样本侧证，需 S2 复核 |
| CL-001 | 目标边界=PostgreSQL 18 单表，排除优化器内核 | S001 | supported | high | 官方版本说明 |

`coverage.md`（节选）：

| Category | Status | Reason | Gate effect | Source IDs |
| --- | --- | --- | --- | --- |
| wikipedia_encyclopedia | covered | 术语与相邻概念已查 | none | — |
| official_academic | covered | PostgreSQL 18 官方文档 | none | S001 |
| recruiting_jd | covered | 岗位样本 | none | S002 |

> S2 六源映射：`official_academic`→`standards_official`；`recruiting_jd`→`job_career`；S2 须按实际来源重新核验，不按类别名升级证据等级。

`capabilities.jsonl`（节选）：

```jsonl
{"capability_id":"CAP-001","statement":"从 EXPLAIN (ANALYZE, BUFFERS) 区分估算与实际执行信息","observable_evidence":["指出基线计划估算行数与实际行数的差异"],"bloom_level":"analyze","source_ids":["S001"]}
{"capability_id":"CAP-003","statement":"设计并论证单列/多列/部分索引而非默认加索引","observable_evidence":["为 (tenant_id,status,created_at) 论证多列索引"],"bloom_level":"create","source_ids":["S001"]}
```

`goal-contract.md`（要点）：`target_problem`=独立诊断并改进 PostgreSQL 18 单表查询性能；`final_assessment.tasks`=三个未见查询的独立采集/诊断/方案/验证/回滚，`unseen_or_transfer_required=true`；`pass_rules`=三题中至少两题主瓶颈/方案/验证均正确且不执行未经确认的生产变更；`scope`/`exclusions`（优化器内核、复杂多表连接调优）/`constraints`（4 周、每周 6 小时、PG18 沙箱）。

`research-brief.md`（要点）：`role_family`=后端工程/数据库性能诊断；`target_level`=中级后端；`region`=中国互联网；`languages`=[zh-CN,en]；`time_window`=PG18 当前版本与近三年；`decision_risk`=medium；`six_source_seeds` 六类各 ≥1 条 query。

`confirmation.md`：确认问题/回答齐全，`status=confirmed`；`confirmed_items`≥1。

`g1-evaluation.md`：全维 `passed=true`；`verdict=pass`、`route_to=S2`。

`verification.md`（节选）：

```markdown
- state: verified
- source_summary: { accepted: 6, accepted_external_evidence: 4, needs_metadata: 0, rejected: 0, trace_only: 1 }
- confirmation_status: confirmed
- g1_verdict: pass / route_to: S2
- unresolved_risks: []
- files_created: [INDEX.md, sources.jsonl, evidence_table.md, coverage.md, capabilities.jsonl, terminology.jsonl, goal-contract.md, research-brief.md, confirmation.md, g1-evaluation.md, verification.md]
```

## 示例 B（反向/阻塞）— 七天成为 AI 专家

**来源追溯**：`docs/chat_log/七步个性化学习SOP正反例与研究依据.md` §S1 反向例子（line 165）。

**输入事实**：诉求"七天成为 AI 专家"；未执行联网预检，仅凭模型记忆；验收只想做 100 道选择题 80 分通过。

**为何 G1 失败（不产出 pass 的 run folder，但仍写诊断 run folder）**

- `target_problem` 无可观察定义（"专家"）；学习时长非能力；纯选择题无法验证迁移；无场景/范围/边界。
- 预检未执行：`sources.jsonl` 无 `accepted` 且 `provenance=external_evidence` 的来源 → `verification.md.state=blocked`，不进入 S2。
- `g1-evaluation.md`：至少一维 `passed=false` 且 `failure_action=revise_here`；`verdict=blocked`、`route_to=S1`。

`verification.md`（节选）：

```markdown
- state: blocked
- source_summary: { accepted: 0, accepted_external_evidence: 0, trace_only: 0 }
- confirmation_status: pending
- g1_verdict: blocked / route_to: S1
- unresolved_risks: [{ id: R001, severity: high, reason: 预检未执行且目标不可观察, action: 重新校准目标并执行联网预检 }]
```

## run folder 交付状态示例

- 每次运行写出 11 个固定命名文件（`INDEX.md`/`sources.jsonl`/`evidence_table.md`/`coverage.md`/`capabilities.jsonl`/`terminology.jsonl`/`goal-contract.md`/`research-brief.md`/`confirmation.md`/`g1-evaluation.md`/`verification.md`）。
- `pending` 或 `blocked` 也写出完整诊断 run folder，展示缺口、当前结论与恢复条件；不用空标题、`TBD`/`TODO`/示例占位。
- run folder 内不出现单体 JSON 移交信封、HTML 页面或独立图片资产；"可视化" = 数据表视图。
- 跨文件 ID 互引必须可解析；任一必需文件缺失或 G1 机读七项不满足时，本次交付不得报告为完整完成，且 G1 不得 `pass`。
