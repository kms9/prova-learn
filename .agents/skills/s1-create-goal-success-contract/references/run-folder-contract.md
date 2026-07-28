---
desc: "S1 run-folder 产物契约。规定 S1 每次 run 在 workspace/<project-slug>/runs/<run-id>/ 下产出的固定命名文件、逐文件字段契约、稳定 ID 规则、状态机 guard、反占位与跨文件互引校验。本文件取代旧的 Markdown/JSON/HTML 三工件输出契约。"
---

# S1 Run-Folder 产物契约

本参考规定 `create-goal-success-contract`（S1）每次运行的**落盘产物**。S1 不再产出单体 Markdown 审核文档、JSON 移交信封或 HTML 页面；改为在运行目录下写一个 **run folder**，内含一组**固定命名文件**，每文件有严格字段契约，记录型用 `.jsonl`（一行一条、稳定 ID、跨文件互引），汇总/审计型用 `.md` 表，由状态机（见 `SKILL.md`）带 guard 控制写入顺序，最后 `verification.md` 收尾。

落盘方式参照 `storm-evidence` skill 的证据治理产物（sources/claims/evidence_table/citation_audit/verification）。

## 0. run folder 布局

```text
<cwd>/workspace/<project-slug>/runs/<run-id>/
  INDEX.md            主索引：G1 verdict/route + 文件清单 + 运行历史指针（下游读取入口）
  sources.jsonl       预检来源记录
  evidence_table.md   来源 ↔ S1 结论 支撑表
  coverage.md         六类预检覆盖表
  capabilities.jsonl  可观察能力记录
  terminology.jsonl   术语校正记录
  goal-contract.md    目标/场景/验收/通过规则/范围/排除/约束（人审编译稿）
  research-brief.md   domain_research_brief（S2 直接消费）
  confirmation.md     确认问题/回答/状态 + 开放问题 + 已确认项
  g1-evaluation.md    G1 量规逐维表 + verdict + route
  verification.md     状态机终态 + 统计 + 未决风险 + 命令
```

- `project-slug` = 校准后目标的 kebab-case，稳定不变；用户根本改变目标时开新 slug。
- `run-id` = `run-YYYYMMDD-HHMMSS`（如 `run-20260727-192733`）。
- 同一 `project-slug` 下多次 S1 运行并列在 `runs/` 下；下游按时间戳取最新 run 的 `INDEX.md` 为当前输入，历史 run 仅供背景。
- 不在本 run folder 之外另造单体 JSON、HTML、图片或通用装载器。

## 1. 稳定 ID 规则（跨文件互引基础）

| 前缀 | 含义 | 所在文件 |
| --- | --- | --- |
| `S001`、`S002`… | Source Record | `sources.jsonl` |
| `CAP-001`、`CAP-002`… | 可观察能力 | `capabilities.jsonl` |
| `TERM-001`、`TERM-002`… | 术语校正 | `terminology.jsonl` |
| `CL-001`、`CL-002`… | `evidence_table.md` 内的自由结论（目标/范围等） | `evidence_table.md` |
| `G1-target-observable` 等 | G1 量规维度 | `g1-evaluation.md` |

- ID 递增分配，**不复用已删除 ID**。
- 任何文件引用的 `source_id` / `capability_id` / `term_id` / claim ID 都必须能在对应文件中解析到记录；解析失败计为 `orphan_reference`，进 `verification.md` 未决风险，G1 不得 `pass`。

## 2. `sources.jsonl` — 预检来源记录

每行一个 JSON object（JSONL）。字段：

```json
{
  "source_id": "S001",
  "type": "web | local | vector | agent_trace | expert_note",
  "title": "来源标题",
  "url": "https://example.com/page",
  "file": "docs/example.md",
  "line_range": "12-30",
  "snippet": "来源原文或检索片段，非模型改写",
  "query": "找到该来源的检索意图",
  "retrieved_at": "2026-07-27T19:27:33+08:00",
  "retrieved_by": "agent 或检索路由名",
  "provenance": "external_evidence | market_signal | model_hypothesis | user_provided_unverified | learner_behavior",
  "category": "wikipedia_encyclopedia | official_academic | practice_case | recruiting_jd | interview_selection | adversarial_frontier",
  "trust_note": "为何可用或受限；时效来源写 as-of 风险",
  "status": "accepted | needs_metadata | rejected | trace_only"
}
```

字段规范与必填：

- `source_id`：`S001` 递增，不复用。
- `type`：复用 `storm-evidence` 枚举 `web`/`local`/`vector`/`agent_trace`/`expert_note`。`rg`/grep/文件读取归 `local`（AgentSearchRM），不得标 `vector`。
- `provenance`：S1 五分类。**只有真实检索到的可访问来源才能 `external_evidence`；模型知识只能 `model_hypothesis`；招聘样本 `market_signal`。** `model_hypothesis` 与 `user_provided_unverified` 默认 `status=trace_only`，不得作为支撑 G1 的外部证据。
- `category`：该来源喂给的 S1 六类预检类别之一（见 `coverage.md`）。
- `web` 必填 `url`/`title`/`snippet`/`query`/`retrieved_at`；`local` 必填 `file`/`line_range`/`snippet`/`query`/`retrieved_at`。
- `snippet` 必须是来源原文或检索片段，不是模型改写。
- `external_research_seed` 旧字段（`search_executed`/`retrieval_date`/`queries`）由本文件 + `coverage.md` 共同表达；不再写单体 JSON。

## 3. `evidence_table.md` — 来源 ↔ S1 结论 支撑表

Markdown 表格，把 S1 的实质结论绑定到 accepted Source Records：

| Claim ID | Claim | Source IDs | Support | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| CAP-001 | 能从 EXPLAIN (ANALYZE) 区分估算与实际执行信息 | S001, S004 | supported | high | 官方文档直接支撑 |
| TERM-001 | "学会查询优化" 应收窄为 "诊断并改进单表查询性能" | S002 | partially_supported | medium | JD 样本侧证，需 S2 复核 |
| CL-001 | 目标边界=PostgreSQL 18 单表，排除优化器内核 | S003 | supported | high | 官方版本说明 |

规则：

- `Claim ID` 复用 `CAP-`/`TERM-`/`CL-`；`CL-` 用于仅在 `goal-contract.md` 出现、未单列 jsonl 的结论（目标/范围/边界/约束）。
- 每条非常识的 S1 结论都映射到至少一条 Claim ID，并绑定至少一个 accepted Source ID。
- 中心结论倾向 ≥2 条独立来源；仅单来源时标 risk。
- `unsupported`/`contradicted`/`trace_only` 不入主表，入 "待补证据/风险" 区，且不得支撑 G1 pass。
- Source IDs 必须存在于 `sources.jsonl`。

## 4. `coverage.md` — 六类预检覆盖表

Markdown 表格，固定六类，各出现一次：

| Category | Status | Reason | Gate effect | Source IDs |
| --- | --- | --- | --- | --- |
| wikipedia_encyclopedia | covered | 术语与相邻概念已查 | none | S001 |
| official_academic | covered | PostgreSQL 18 官方文档 | none | S003 |
| practice_case | covered | 真实慢查询诊断案例 | none | S005 |
| recruiting_jd | covered | 3 个岗位样本 | none | S002, S006 |
| interview_selection | covered | 实操调试样本 | none | S007 |
| adversarial_frontier | not_applicable | 单表索引优化非争议前沿 | none | — |

规则：

- 类别固定为 `wikipedia_encyclopedia` / `official_academic` / `practice_case` / `recruiting_jd` / `interview_selection` / `adversarial_frontier`，不可改名或增删。
- `Status`：`covered` / `not_applicable` / `gap`。`not_applicable` 必须给可审计理由；"找不到资料" 记 `gap`，不是 `not_applicable`。
- `Source IDs` 指向 `sources.jsonl` 中归属该类的来源。
- **六类预检类别 ≠ S2 六源通道**，须按实际出处映射（wiki 仅作发现入口；official_academic 进 books_courses/papers_research/standards_official；recruiting_jd 进 job_career；practice_case/interview_selection 通常进 artifacts_validation，社区转述进 community_web；adversarial_frontier 按出处进 papers_research/community_web/artifacts_validation）。S2 必须按实际来源重新核验，不得按类别名自动升级证据等级。映射说明写在本表下方。

## 5. `capabilities.jsonl` — 可观察能力记录

每行一个 JSON object：

```json
{
  "capability_id": "CAP-001",
  "statement": "从 EXPLAIN (ANALYZE, BUFFERS) 区分估算与实际执行信息",
  "observable_evidence": ["指出基线计划估算行数与实际行数的差异"],
  "bloom_level": "understand | apply | analyze | diagnose | transfer | create",
  "source_ids": ["S001", "S004"]
}
```

规则：

- 每条 `observable_evidence` ≥1，且必须是可外部观察的行为/产物，不是能力名称本身。
- 区分记忆/解释/应用/诊断/迁移/创造（`bloom_level`）。
- `source_ids` 指向支撑该能力的 accepted 来源（可空，但空时须在 `evidence_table.md` 标 needs_source）。

## 6. `terminology.jsonl` — 术语校正记录

每行一个 JSON object：

```json
{
  "term_id": "TERM-001",
  "original": "学会查询优化",
  "corrected": "能诊断并改进单表查询性能",
  "evidence_refs": ["S002"]
}
```

规则：只保留理解当前目标所必需的真实术语校正；不得把被用户否决的旧目标/旧场景包装成反例继续展示。

## 7. `goal-contract.md` — 人审编译稿

Markdown 结构化文档（不是 jsonl），供人逐段校对，呈现编译后的目标契约。建议结构：

```markdown
# 目标与成功契约（run-<id>）

> 状态 | 日期 | 范围 | 受众：人审 + S2–S7

## 目标问题（target_problem）
## 目标场景（target_scene）
## 最终验收设计（final_assessment：tasks[] + unseen_or_transfer_required）
## 通过规则（pass_rules[]）
## 范围（scope[]）
## 排除项（exclusions[]）
## 约束（constraints{}：duration/effort/environment/...）
```

- 引用 `CAP-`/`TERM-`/`S-` ID 而非复述全文。
- 区分用户事实与推断；`pending`/`blocked` 也要完整写已知、未知、未执行与恢复条件。
- 禁止空标题、`TBD`/`TODO`/`待补充`/示例数据占位。

## 8. `research-brief.md` — domain_research_brief（S2 直接消费）

Markdown，约束 S2 的研究范围，不代表已完成六源研究或领域全景：

- `role_family` / `target_level` / `region` / `languages` / `time_window` / `decision_risk`
- `priority_questions[]`
- `source_constraints[]`
- `six_source_seeds`：六源通道（`job_career`/`books_courses`/`papers_research`/`community_web`/`standards_official`/`artifacts_validation`）各 ≥1 条 query seed 的表格。

## 9. `confirmation.md` — 确认与开放问题

- `confirmation`：确认问题 / 用户回答 / `status`（`confirmed` | `pending`）。
- `open_questions[]`、`confirmed_items[]`（≥1）。
- 用户根本改变目标时回到 S1；本文件只记当前目标的确认结果。

## 10. `g1-evaluation.md` — G1 量规与路由

Markdown 表格逐维评价 + 裁决：

| Dimension | Evidence | Score | Threshold | Passed | Failure_action | Route |
| --- | --- | --- | --- | --- | --- | --- |

量规维度（证据来源列指向 run-folder 文件/ID）：

| 维度 | 阈值 | 证据来源 |
| --- | --- | --- |
| 目标可观察性 | 每项能力≥1 可观察证据 | `capabilities.jsonl`.observable_evidence |
| 成功标准可判定性 | unseen_or_transfer_required | `goal-contract.md`.final_assessment |
| 场景真实性 | target_scene 非空 | `goal-contract.md` |
| 外部现实校准度 | 有 terminology 或确认无歧义 | `terminology.jsonl` |
| 强制类别覆盖 | 六类固定类别均有唯一状态，wiki/recruiting/interview covered 或可审计 | `coverage.md` |
| S2 研究范围可执行 | 岗位/场景、地区语言、时效、六源种子明确 | `research-brief.md` |
| 边界清晰 | exclusions 非空 | `goal-contract.md`.exclusions |
| 约束完整 | 时间/形式约束存在 | `goal-contract.md`.constraints |
| 目标—验收一致 | pass_rules 与能力、验收对齐 | `goal-contract.md`.pass_rules |
| 外部证据真实 | sources.jsonl ≥1 accepted external_evidence | `sources.jsonl` |

裁决：`verdict`（`pass`/`revise_here`/`return_upstream`/`blocked`）+ `route_to`（`S2`/`S1`）。G1 通过当且仅当所有维度 `passed=true` 且 `confirmation.status=confirmed` 且无关键证据缺口阻塞目标确认。

## 11. `verification.md` — 终态

```markdown
# Verification（run-<id>）

- state: verified | blocked | needs_repair | pending
- source_summary: { accepted, accepted_external_evidence, needs_metadata, rejected, trace_only }
- capability_count
- confirmation_status: confirmed | pending
- g1_verdict / route_to
- unresolved_risks: [{ id, severity, reason, action }]
- commands: [执行的 eval/校验命令]
- files_created: [本 run 实际写出的文件清单]
```

规则：`high` 未决风险未解决、或 `accepted_external_evidence=0` 时不得 `verified`/G1 pass。

## 12. `INDEX.md` — 主索引（下游读取入口）

run folder 的主入口，遵循 `AGENTS.md §13 LLM Wiki 维护格式`：

- 头部：`run-id` | 时间 | 状态(G1) | 范围 | 受众(S2–S7+人审) | 最后核对。
- **结论先行**：target_problem / target_scene / 目标边界一句话。
- **最新 G1 结论**：`verdict` / `route_to` / `confirmation.status`。
- **文件清单**：每个文件一句话用途（即本契约 §0 的清单）。
- **下游读取指引**：S2 读 `research-brief.md`+`sources.jsonl`+`coverage.md`；S3/S4/S5 读 `goal-contract.md`+`capabilities.jsonl`。
- **运行历史指针**：本项目其他 run 见同级 `../`（按时间戳取最新为本输入；历史仅供背景）。
- **稳定术语**：kebab 锚点列表。

## 13. 反占位与完整性

- 任何文件不得出现 `TBD`/`TODO`/`待补充`/空标题/空表/示例数据。
- `pending`/`blocked` 也要写齐已知、未知、未执行、当前结论与恢复条件（诊断 run folder）。
- 已被用户否决且与当前目标无关的旧目标/旧场景不得在任何文件中继续传播。

## 14. 跨文件互引校验（交付前必过）

- `evidence_table.md` / `coverage.md` / `capabilities.jsonl` / `terminology.jsonl` 中所有 `source_ids`/`evidence_refs` 在 `sources.jsonl` 可解析。
- `goal-contract.md` 引用的 `CAP-`/`TERM-` 在对应 jsonl 可解析。
- `g1-evaluation.md` 证据列指向的文件/ID 存在。
- `INDEX.md` 文件清单与实际写出文件一致。
- 任一校验失败写入 `verification.md.unresolved_risks`，G1 不得 pass，本次交付不得报告为完整完成。
