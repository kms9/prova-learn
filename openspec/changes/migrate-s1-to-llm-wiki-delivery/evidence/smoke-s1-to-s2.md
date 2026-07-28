# Task 20 — S1→S2 冒烟（INDEX.md 下游读取）

**样本**：`workspace/senior-teaching-researcher/runs/run-20260727-234421/`。
**校验器**：`evidence/smoke-s1-to-s2.py`（模拟 S2 经 INDEX.md 下游读取指引消费 3 文件）。

**校验项**：
1. `INDEX.md` 下游读取指引显式点名 S2 读 `research-brief.md` + `sources.jsonl` + `coverage.md`。
2. 三文件存在且非空。
3. `sources.jsonl` 可被 S2 解析。
4. `coverage.md` 含六类固定预检类别（S1 类别）。
5. `research-brief.md` 含六源通道种子（S2 通道）各 ≥1。

**运行结果**：

```
RUN-FOLDER: .../workspace/senior-teaching-researcher/runs/run-20260727-234421
  note: INDEX.md S2 guidance present: yes
  note: sources.jsonl records=24
  note: coverage.md six categories all present: True
  note: research-brief.md six_source channels all present: True
RESULT: PASS — S2 can follow INDEX.md to read research-brief.md + sources.jsonl + coverage.md; all structurally consumable.
```

**结论**：S1→S2 下游读取通路冒烟通过。S2 经 `INDEX.md` 的「下游读取指引」可定位并取出 `research-brief.md`（六源种子齐）、`sources.jsonl`（24 条可解析）、`coverage.md`（六类齐 + S2 六源映射说明），满足 run-folder-contract §12 的下游读取要求。
