# Task 19 — S1 `evals.json` 跑通（blocked on harness follow-up task 22）

## 已验证（本 change 内可做）

- `evals.json` 是合法 JSON，3 个 case：
  - id=1 正向（PostgreSQL 慢查询，4 周）。
  - id=2 正向（六年级分数，监护人与学习者共同确认）。
  - id=3 负向/blocked（"七天成为 AI 专家"，拒绝补全/联网，仅模型知识 + 选择题验收）。
- `expected_output` 与 `expectations` 已全部重写为 run-folder 模型：点名 11 文件 run folder、禁止单体 JSON/HTML/图片、JSONL 稳定 ID、六类固定预检类别 + S2 六源映射、evidence_table 绑定 accepted Source ID、capabilities 每项 ≥1 可观察证据、research-brief 六源种子、goal-contract 排除项、confirmation=confirmed、g1-evaluation 逐维 + 路由 S2、verification 终态 + accepted_external_evidence>0、反占位 + 跨文件 ID 可解析。结构与 `run-folder-contract.md` 一致。

## 未跑通（blocker）

`scripts/run_skill_evals.py`（340 行）当前**不支持目录型产物评分**，两处硬编码旧单体 JSON 模型：

1. **执行器指令仍要求单体 JSON**（L39/L45）：
   - `"produce that stage's handoff envelope as a SINGLE JSON object. Think, then output ONLY the JSON (no prose)."`
   - 与 S1 run-folder 目录交付直接冲突。
2. **grader 只评捕获的文本输出**（`grade()` L102–113，`run["result_text"] = result.get("result","")` L149）：LLM judge 只看到执行器的 stdout 文本，**不读取 run folder 目录文件**，无法校验 `sources.jsonl`/`coverage.md`/`INDEX.md` 等多文件结构与跨文件互引。

## 解锁条件（= task 22，显式后续追踪，不在本 change 范围）

- 执行器指令改为"落盘 run folder 目录"。
- grader 改为读取 `workspace/<slug>/runs/<run-id>/` 目录，复用本 change 已写的结构校验（`evidence/validate-run-folder.py` + `evidence/smoke-s1-to-s2.py` 可作判分依据），再交 LLM judge 评语义期望。

## 结论

`evals.json` 本身合规且与 run-folder 契约一致；**实际跑通**依赖 `run_skill_evals.py` 扩展（task 22），属显式后续追踪。本 change 内 task 19 维持 `[ ]`（未跑通），不阻塞 S1 迁移结论。
