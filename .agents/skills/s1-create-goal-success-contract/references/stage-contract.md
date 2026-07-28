# S1 阶段契约 — create-goal-success-contract（门 G1）

> 本文件治理 S1 与决策门 G1。§0 为阶段共享规则（**S1 已迁移到 run-folder 目录交付**，S2–S7 暂保留三工件模型，待后续迁移）；其余为 S1 专属。

## 0. 共享阶段契约（适用于 S1–S7）

- **编号定义**：`Sx` 是第 x 个执行阶段（Stage），`Gx` 是紧随 Sx、评价该阶段工件能否被下游消费的质量决策门（Gate）。例如 `G1` 是 S1 目标契约质量门，不是学习理论、外部标准或另一个 Skill。
- **产物交付模型（S1）**：S1 不再产出单体 Markdown / JSON 移交信封 / HTML。S1 在运行目录下写一个 **run folder**（`workspace/<project-slug>/runs/<run-id>/`），内含一组**固定命名文件 + 严格字段契约**：记录型用 `.jsonl`（一行一条、稳定 ID、跨文件互引），汇总/审计型用 `.md` 表，状态机带 guard 控制写入顺序，`INDEX.md` 为下游读取入口，`verification.md` 收尾。逐文件字段契约见各阶段 `run-folder-contract.md`（S1）或对应输出契约（S2–S7）。
- **S2–S7 暂保留三工件模型**：仍产出"完整 Markdown + 规范 JSON 移交信封 + 交互 HTML"三件工件，直到各自迁移到 run-folder 交付。因此本 §0 同时描述两种模型；S1 走 run-folder，S2–S7 走三工件，分叉被显式记录而非静默。

### 0.1 S1 run-folder 交付（S1 专属生效）

- **产物清单**（见 `references/run-folder-contract.md`）：`INDEX.md`、`sources.jsonl`、`evidence_table.md`、`coverage.md`、`capabilities.jsonl`、`terminology.jsonl`、`goal-contract.md`、`research-brief.md`、`confirmation.md`、`g1-evaluation.md`、`verification.md`。
- **稳定 ID 跨文件互引**：`S001`(source)/`CAP-001`(capability)/`TERM-001`(terminology)/`CL-001`(evidence_table 结论)/`G1-*`(量规维度)；不复用已删除 ID；交付前所有跨文件引用必须可解析。
- **状态机生成顺序**（guard 见 `SKILL.md`）：`input_validated → preflight_executed → sources_normalized → coverage_classified → capabilities_extracted → evidence_table_ready → goal_contract_compiled → confirmation_resolved → g1_evaluated → risk_reviewed → verified`。
- **cross-stage 读取契约**：下游先读 `workspace/<project-slug>/runs/` 下最新 run 的 `INDEX.md`，按需读 `research-brief.md`/`sources.jsonl`/`evidence_table.md`/`coverage.md`/`goal-contract.md`/`capabilities.jsonl`；历史 run 仅供背景，不作当前输入。
- **"已通过 G1"机读校验（run-folder 版）**：1) 最新 run 含全部 11 文件；2) `g1-evaluation.md` 记 `verdict=pass`/`route_to=S2`/每维 `passed=true`；3) `confirmation.md` 记 `confirmation.status=confirmed`；4) `verification.md` 终态 `verified`、无阻塞 G1 的 high 风险；5) 无占位符；6) 跨文件 ID 全部可解析；7) `sources.jsonl` ≥1 条 `accepted` 且 `provenance=external_evidence`（预检真实执行）。

### 0.2 S2–S7 三工件交付（暂留）

每个阶段必须产出**三份内容一致、用途不同的工件**：

1. 一份按当前阶段专属结构撰写的完整 Markdown 人审文档；
2. 一份把 Markdown 全部实质内容无损结构化的规范 JSON 移交信封（`handoff-envelope.schema.json`）；
3. 一份由最终 JSON 填充的阶段专用交互 HTML。

- **三工件权威边界**：Markdown 是首要人审文档，JSON 是机器移交的规范表示，HTML 是 JSON 驱动的只读派生视图。Markdown 与 JSON 必须语义等价。
- **"已通过 Gx"机读含义（三工件版）**：消费方必须验证兼容移交信封同时满足 `stage_id=Sx`、`status=completed`、`input_validation.status=pass`、具名 `positive_artifact` 非空且通过其 Schema、全部 `quality_evaluation.rubric_results[].passed=true`、`quality_evaluation.verdict=pass`、`quality_evaluation.route_to=S{x+1}`，并满足该阶段确认规则；三工件交付还要求 `document_artifact.status=generated` 与 `presentation_artifact.status=generated`。

### 0.3 共通执行形状与门规

- **输入契约校验**：至少检查工件类型/版本、必填字段、来源阶段、追溯与上游门状态。S1 run-folder 模式下校验最新 run 的 11 文件与 G1 机读七项；S2–S7 三工件模式下校验信封字段。失败时 `input_validation.status=fail` 并路由上游，**不得伪造正向工件**。
- **确认状态机**：`mandatory`（S1/S5，未确认不得前进）、`conditional`（S2/S3/S4/S7，遇高风险/分歧/多方案升级为强制）、`inform`（S6 节点推进，告知后继续）。
- **证据来源分类**：`model_hypothesis`/`market_signal`/`external_evidence`/`user_provided_unverified`/`learner_behavior`。**门不得把 `model_hypothesis` 或 `user_provided_unverified` 计为外部证据。**
- **量规结果形状**：`{dimension, evidence[], score, threshold, passed, failure_action, route_to}`；`passed=false` 时 `failure_action` 与 `route_to` 必填。
- **显式未知/阻塞态**：`pending`/`blocked`/`unknown`/`evidence_insufficient`/`research_blocked`/`not_executed`/`version_conflict` 不得被强制为 `pass`。
- **确定性路由**：`pass` 前进；`revise_here` 同阶段重试；`return_upstream` 指向**最早**污染阶段并记录失效下游范围。S7 多归因按上游优先级路由。
- **合并守卫**：快速档仅可在满足条件时合并 S2+S3 或 S4+S5，仍须分别产出工件并依次通过两门；S1、S7 永不合并。
- **强制完整产物**：S1 每次 run 都必须写出 11 文件（`pending`/`blocked` 也写齐诊断 run folder，明确已知、未知、未执行与恢复条件）；S2–S7 每次 run 都必须产出三工件。禁止空标题、空表、`TBD`、`TODO`、示例数据占位。
- **禁止独立图片/HTML 装载器（S1）**：S1 run-folder 内不得出现独立 PNG/JPEG/WebP/SVG/GIF 图片资产或 HTML 文件；"可视化" 默认指 `evidence_table.md`/`coverage.md`/`g1-evaluation.md` 等数据表视图。
- **交付完整性**：S1 任一必需文件缺失、跨文件引用失败、或 G1 机读七项任一不满足，本次交付不得报告为完整完成；S2–S7 任一工件缺失、Markdown—JSON 对应失败或 HTML 验证失败，同样不得报告为完整完成。产物失败不篡改领域门禁本身。

## 1. S1 目的

把模糊的"我想学 X"与一次有边界的强制联网预检，校准为经过外部校准、用户确认、可观察、可验收的目标契约。S1 是"目标校准—领域研究"对（S1–S2）的目标校准半边。S1 把校准结果与预检证据落盘为一个 run folder（见 §0.1），供 S2–S7 经 `INDEX.md` 读取。

## 2. S1 输入契约

| 输入 | 是否必填 | 说明 |
|---|---|---|
| 学习者诉求/目标问题 | 必填 | 冷启动可模糊 |
| 目标使用场景 | 必填 | 至少一个场景或问题 |
| 既有材料 | 可选 | 须保留来源标识；未验证材料不得默认为事实 |

冷启动允许不完整；未确认推断与模型知识不得写成已确认目标。

## 3. S1 确认策略（强制）

用户确认：目标能力、成功证据、范围、岗位族/目标职级、地区/行业/语言、时效窗口、时间/资源/形式约束、风险级别、排除项。`confirmation.status=pending` 时门不得通过。用户中途根本改变目标时，无论流程进行到哪，都返回 S1（开新 run）。

## 4. S1 强制联网预检（不可降级）

- 确认前执行，即便模型"知道"该领域。
- 至少查询：Wikipedia/百科（术语+相邻概念）、当前 JD（任务/工具/职级）、面试/实操样本，以及 S2 可追溯的岗位、书课、论文、社区、标准、真实产物六类来源入口。
- 预检结果落盘为 `sources.jsonl`（每条来源：`source_id`/`type`/`url|file`/`snippet`/`query`/`retrieved_at`/`provenance`/`category`/`status`）与 `coverage.md`（六类覆盖表）。模型知识只标 `provenance=model_hypothesis`、`status=trace_only`；只有真实检索到的可访问来源才能 `external_evidence` 且 `accepted`。
- 预检覆盖类别固定为 `wikipedia_encyclopedia / official_academic / practice_case / recruiting_jd / interview_selection / adversarial_frontier`，六类各出现一次于 `coverage.md`，并记 `covered`/`not_applicable`/`gap` + `reason` + `gate_effect` + `source_ids`。
- `not_applicable` 必须给出可审计理由；找不到资料记为 `gap`，不是 `not_applicable`。
- 形成 `research-brief.md`（`domain_research_brief`）：领域边界、岗位族/目标职级、地区/语言、时间窗口、风险级别、重点问题、六源检索种子与来源限制。该简报只约束 S2，不代表已完成六源研究或领域全景。
- S1 预检类别与 S2 证据通道不是同一分类，必须按实际来源归属映射（映射说明写在 `coverage.md` 下方）：`wikipedia_encyclopedia` 仅作发现入口；`official_academic` 按来源进入 `books_courses`/`papers_research`/`standards_official`；`recruiting_jd` 进入 `job_career`；`practice_case`/`interview_selection` 通常进入 `artifacts_validation`，社区转述进 `community_web`；`adversarial_frontier` 按出处进入 `papers_research`/`community_web`/`artifacts_validation`。S2 必须重新核验实际来源，不得按类别名自动升级证据等级。
- 无联网/检索能力时：`verification.md.state=blocked`，G1 失败，不得用模型记忆替代预检。

## 5. S1 产物字段 → run-folder 文件映射

旧 `goal_success_contract.content` 字段落盘分布如下（字段契约详见 `run-folder-contract.md`）：

| 旧字段 | run-folder 文件 |
|---|---|
| `target_problem` / `target_scene` / `final_assessment` / `pass_rules` / `scope` / `exclusions` / `constraints` | `goal-contract.md` |
| `observable_capabilities[]` | `capabilities.jsonl`（`capability_id`/`statement`/`observable_evidence[]`/`bloom_level`/`source_ids`） |
| `terminology_corrections[]` | `terminology.jsonl`（`term_id`/`original`/`corrected`/`evidence_refs`） |
| `external_research_seed.sources` | `sources.jsonl` |
| `external_research_seed.category_coverage` | `coverage.md` |
| 来源↔结论支撑关系（来源↔能力/术语/目标边界） | `evidence_table.md` |
| `domain_research_brief`（含 `six_source_seeds`） | `research-brief.md` |
| `open_questions` / `confirmed_items` / 确认结果 | `confirmation.md` |
| G1 量规 / verdict / route | `g1-evaluation.md` |
| 终态 / 统计 / 未决风险 | `verification.md` |
| 下游读取入口 / 文件清单 / 运行历史 | `INDEX.md` |

`goal-success-contract.schema.json` 保留为**字段覆盖参考**（语义形状），不再作为产物校验器；S1 不产出 JSON 信封。`handoff-envelope.schema.json` 为 S2–S7 共享遗留契约，S1 不再产出。

## 6. S1 量规（门 G1）

| 维度 | 阈值类型 | 阈值 | 证据来源（run-folder） |
|---|---|---|---|
| 目标可观察性 | 每项能力≥1 可观察证据 | ≥1 | `capabilities.jsonl`.observable_evidence |
| 成功标准可判定性 | unseen_or_transfer_required | true | `goal-contract.md`.final_assessment |
| 场景真实性 | target_scene 非空 | true | `goal-contract.md` |
| 外部现实校准度 | 有 terminology_corrections 或确认无歧义 | true | `terminology.jsonl` |
| 强制类别覆盖 | 六类固定预检类别均有唯一状态，wiki/recruiting/interview covered 或可审计 | true | `coverage.md` |
| S2 研究范围可执行 | 目标岗位/场景、地区语言、时效和六源种子明确 | true | `research-brief.md` |
| 边界清晰 | exclusions 非空 | ≥1 | `goal-contract.md`.exclusions |
| 约束完整 | 时间/形式约束存在 | true | `goal-contract.md`.constraints |
| 目标—验收一致 | pass_rules 与能力、验收对齐 | true | `goal-contract.md`.pass_rules |
| 外部证据真实 | sources.jsonl ≥1 accepted external_evidence | ≥1 | `sources.jsonl` |
| 跨文件互引可解析 | 所有 source/cap/term/claim 引用可解析 | true | 全文件 + `verification.md` |

G1 通过当且仅当**所有维度** `passed=true` 且 `confirmation.status=confirmed` 且无关键证据缺口阻塞目标确认（对应 §0.1 机读七项）。

## 7. S1 路由

| verdict | route_to | 触发 |
|---|---|---|
| `pass` | S2 | 全部 G1 维度通过 + 已确认 + run-folder 七项机读校验通过 |
| `revise_here` | S1 | 目标/成功标准不清、术语漂移、预检未执行或仅模型总结 |
| `return_upstream` | S1 | 用户根本改变目标（S1 是最早阶段，上游返回即重回 S1，开新 run） |
| `blocked` | S1 | 无联网能力或关键缺口未解决 |

路由结果写入 `g1-evaluation.md`（`verdict`/`route_to`）与 `verification.md`。

## 8. S1 安全/阻塞态

- 冷启动缺输入 → 记 `requirement_gaps`（`confirmation.md`/`verification.md`），保持 `pending`，仍写出诊断 run folder，不伪造。
- 无检索能力 → `verification.md.state=blocked`；G1 失败；不得通过。
- 关键来源类别缺口 → 门阻塞，除非缩小范围、降低置信度并记录缺口（`coverage.md` 记 `gap`、`verification.md` 记风险）。
- 强制确认未完成 → `confirmation.status=pending`；G1 不得通过。
- 用户否决的旧目标不得作为术语校正、排除项、确认问题继续传播到当前 run folder。
