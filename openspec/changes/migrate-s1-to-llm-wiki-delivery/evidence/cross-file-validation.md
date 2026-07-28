# Task 18 — 跨文件 ID/链接解析校验（真实 run folder 样本）

**样本**：`workspace/senior-teaching-researcher/runs/run-20260727-234421/`（初中数学·双师 教培教研岗，G1 pass）。

**校验器**：`evidence/validate-run-folder.py`（按 run-folder-contract §14 实现；非 task 22 的 eval harness 扩展，仅为一次性结构校验）。

**校验项（契约 §14）**：
1. 三份 JSONL（`sources`/`capabilities`/`terminology`）可解析。
2. `capabilities.jsonl`.source_ids、`terminology.jsonl`.evidence_refs 在 `sources.jsonl` 可解析。
3. `evidence_table.md` / `coverage.md` 中所有 `S###` 在 `sources.jsonl` 可解析。
4. `goal-contract.md` 引用的 `CAP-`/`TERM-`/`S-` 在对应 jsonl 可解析。
5. `g1-evaluation.md` 证据列引用的 `CAP-`/`TERM-`/`S-` 可解析。
6. `INDEX.md` 文件清单与实际写出文件一致。
7. `verification.md` 的 `accepted`/`accepted_external_evidence` 计数与 `sources.jsonl` 自洽。

**运行结果**：

```
RUN-FOLDER: .../workspace/senior-teaching-researcher/runs/run-20260727-234421
  note: sources=24 capabilities=7 terms=4
  note: INDEX.md lists 10 content files; actual content files=10
  note: sources accepted=24 external_evidence=15
RESULT: PASS — all cross-file IDs/links resolve, JSONL parses, INDEX matches actual files.
```

**说明**：
- `INDEX.md` 列 10 个内容文件（不含 `INDEX.md` 自身，符合索引惯例）；与实际 10 个内容文件逐一对应，无幽灵条目、无遗漏。
- `external_evidence=15` 与 `g1-evaluation.md`「外部证据真实=15」、`verification.md`「accepted_external_evidence: 15」一致。
- 无 `orphan_reference`，故按契约不进 `verification.md` 未决风险、不阻塞 G1。

**结论**：跨文件互引校验通过。样本 run folder 结构完整、ID 全部可解析。
