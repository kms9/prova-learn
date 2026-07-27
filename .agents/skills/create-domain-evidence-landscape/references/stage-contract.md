# S2 阶段契约 — create-domain-evidence-landscape（门 G2）

> 本文件治理 S2 与决策门 G2。§0 为七阶段共享规则；其余为 S2 专属。

## 0. 共享阶段契约（适用于 S1–S7）

每个阶段产出**恰好一个**移交信封（`handoff-envelope.schema.json`），并遵循统一执行形状：

```text
校验输入契约
→ 收集需求缺口
→ 执行本阶段确认策略
→ 收集可采信证据
→ 生成具名正向工件
→ 用本阶段专属量规评价
→ 给出 pass / revise_here / return_upstream 与 route_to
```

- **输入契约校验**：至少检查工件类型、schema 版本、必填字段、来源阶段、追溯与上游门状态。失败时 `input_validation.status=fail` 并路由上游，**不得伪造正向工件**。
- **确认状态机**：`mandatory`（S1/S5，未确认不得前进）、`conditional`（S2/S3/S4/S7，遇高风险/分歧/多方案升级为强制）、`inform`（S6 节点推进，告知后继续）。
- **证据来源分类**：`model_hypothesis`/`market_signal`/`external_evidence`/`user_provided_unverified`/`learner_behavior`。**门不得把 `model_hypothesis` 或 `user_provided_unverified` 计为外部证据。**
- **量规结果形状**：`{dimension, evidence[], score, threshold, passed, failure_action, route_to}`；`passed=false` 时 `failure_action` 与 `route_to` 必填。
- **显式未知/阻塞态**：`pending`/`blocked`/`unknown`/`evidence_insufficient`/`research_blocked`/`not_executed`/`version_conflict` 不得被强制为 `pass`。
- **确定性路由**：`pass` 前进；`revise_here` 同阶段重试；`return_upstream` 指向**最早**污染阶段并记录失效下游范围。S7 多归因按上游优先级路由。
- **合并守卫**：快速档仅可在满足条件时合并 S2+S3 或 S4+S5，仍须分别产出工件并依次通过两门；S1、S7 永不合并。

## 1. S2 目的

建立可追溯的领域事实基础，识别共识、分歧、核心思维模型、边界与未决问题。S2 是“目标校准—领域研究”对（S1–S2）的领域研究半边，负责回答“依据是什么”，不负责画能力图，也不把搜索结果数量当成证据质量。

## 2. S2 输入契约

| 输入 | 是否必填 | 说明 |
|---|---|---|
| `goal_success_contract` | 必填 | 必须已通过 G1；含目标、可观察成功证据、范围、排除项、地区/语言、`external_research_seed` |
| 用户提供的资料 | 可选 | 须保留来源标识；未验证材料不得默认视为领域事实，只能作为线索 |

冷启动允许输入不完整；但未确认推断与模型知识不得写成已确认的领域事实。若上游 `goal_success_contract` 未通过 G1、类型/版本不符或追溯缺失，记 `input_validation.status=fail` 并路由上游，**不得伪造正向工件**。

## 3. S2 确认策略（conditional，可升级为 mandatory）

默认 `conditional`：对争议范围、来源限制、地区/岗位口径、研究深度与成本做条件确认；先展示研究视角、核心问题、必查来源类别与预期深度。

升级为 `mandatory` 的触发：高风险或前沿主题、存在活跃分歧或多个竞争范式、目标本身因取证结果需要变更、或资料质量明显不均。`confirmation.status=pending` 时门不得通过。

## 4. S2 强制联网 + STORM 多视角研究（不可降级）

- 取 STORM 研究内核：从相邻主题发现多种视角，由不同视角提出问题，检索互联网资料，让回答严格落在检索来源上并继续追问，最后策展为可追溯的结构化全景。模型自身知识只能用于提出待验证假设、视角、问题与检索词，**不能充当外部证据**。
- 默认至少覆盖六类视角：术语与历史、理论与标准、实践者与真实任务、招聘者与市场能力、面试官/评估者与可观察证据、批评者与前沿争议；可增加学习者、管理者、安全/伦理、地区文化等视角。
- 强制多轮：冲突或新发现必须触发后续查询，**不允许只做一次搜索**；记录 `rounds` 与 `follow_up_triggers`。
- 最低来源覆盖矩阵（六类）：百科、官方/学术、实践案例、招聘 JD、面试/选拔、反方/前沿，每类记 `covered / not_applicable / gap` + `reason` + `criticality` + `gate_effect`。`not_applicable` 必须给出可审计理由；找不到资料记为 `gap`，不是 `not_applicable`。
- 招聘与面试的专门加工规则：JD 去重并记录组织/地区/职级/日期，至少 3 个当前岗位样本、2 个不同组织；面试/选拔至少 2 组独立样本；未达标记 `undersample gap`，**不补造样本**。把“工作任务、工具/知识技能、可观察能力、学历/年限/证书、软性偏好”分别编码；当招聘信号与权威标准冲突时并列呈现，分别标为“市场要求”与“规范/事实依据”，不得强行合并。
- 无联网/检索能力时：`status=blocked`，`research_run_manifest.online=false`、`execution_status=blocked`，G2 失败；用户确认**不能**豁免外部证据门。

## 5. S2 工件字段（`domain_evidence_landscape.content`）

`scope`、`terminology[]`（`term/meaning/evidence_refs`）、`research_executed`（boolean，G2 要求 true）、`research_run_manifest`（`online/execution_status/started_at/rounds/perspectives[]/queries[]/follow_up_triggers`，证明已执行联网多视角研究）、`source_ledger[]`（`evidence_id/url/title/publisher/source_category/published_at/retrieved_at/region/reliability/provenance/applicability`）、`category_coverage[]`（六类覆盖状态）、`core_questions_and_mental_models`、`jd_capability_matrix[]`（`task/capability/skill/tool/background`）、`interview_assessment_matrix[]`（`type/capability/level/credibility`）、`consensus[]`、`disagreements[]`（`issue/side_a/side_b`，双方各含 `strong_arguments`）、`open_problems[]`、`claims[]`（`status=supported/partially_supported/unsupported` + `evidence_refs`）、`evidence_gaps[]`（含 `confidence_impact`）。

`source_ledger[].published_at` 保留来源实际公开的精度：允许完整日期 `YYYY-MM-DD`、年月 `YYYY-MM`、年份 `YYYY` 或未知 `null`；不得为满足 Schema 而伪造缺失的月或日。`retrieved_at` 始终使用完整 `date-time`，用于时效复核。

枚举：`provenance` ∈ {model_hypothesis, market_signal, external_evidence, user_provided_unverified, learner_behavior}；`source_category` ∈ {wikipedia_encyclopedia, official_academic, practice_case, recruiting_jd, interview_selection, adversarial_frontier}；`reliability` ∈ {high, medium, low, unknown}。

## 6. S2 量规（门 G2）

| 维度 | 阈值类型 | 阈值 | 证据来源 |
|---|---|---|---|
| 实际联网执行 | research_executed 且 online 且 execution_status=completed | true | research_run_manifest |
| 强制来源类别覆盖 | 六类均有状态且默认样本量达标或可审计 | true | category_coverage |
| 来源可靠性与时效 | 关键结论可追溯至可靠、当前来源 | true | source_ledger |
| 结论可追溯性 | 每项 claim 有 evidence_refs | true | claims.evidence_refs |
| STORM 视角与问题多样性 | perspectives≥6 且各有 questions 与 query_ids | ≥6 | research_run_manifest.perspectives |
| 后续追问深度 | rounds≥1 且冲突触发后续查询 | true | research_run_manifest.rounds/follow_up_triggers |
| 岗位/面试样本代表性 | 招聘≥3 样本/2 组织；面试≥2 组；未达标记 gap | true | jd_capability_matrix / interview_assessment_matrix |
| 时效与地区适配性 | retrieved_at、region 与目标口径一致 | true | source_ledger |
| 事实/市场信号/推断分离 | market_signal 未被写成 fact；模型假设未计为外部证据 | true | claims.claim_type + evidence_collected.provenance |
| 争议平衡 | 重要争议未被单边伪装成共识，保留双方强论据 | true | disagreements.side_a/side_b |
| 证据缺口透明度 | 缺口显式标记且含 confidence_impact | true | evidence_gaps |

G2 通过当且仅当**所有维度** `passed=true` 且 `research_executed=true` 且无关键证据缺口阻塞建图。

## 7. S2 路由

| verdict | route_to | 触发 |
|---|---|---|
| `pass` | S3 | 全部 G2 维度通过、研究已实际执行、缺口不阻塞建图 |
| `revise_here` | S2 | 研究过浅/不平衡/过期、来源类别缺失、查询仅一次、冲突未解释、样本不足 |
| `return_upstream` | S2 | 局部证据缺口（S3 建图发现来源空白时）回到 S2 局部补证，不推倒全部结果 |
| `return_upstream` | S1 | 目标本身实质改变（成功契约失效），回最早污染阶段 |
| `blocked` | S2 | 无联网能力或 `research_run_manifest.online=false` |

## 8. S2 安全/阻塞态

- 上游未通过 G1 → `input_validation.status=fail`，路由 S1，不伪造 landscape。
- 无联网/检索能力 → `status=blocked`，`research_blocked`，G2 失败，不得用模型记忆替代取证。
- 关键来源类别缺口 → 记 `gap`、`criticality`、`gate_effect`、`confidence_impact`；阻塞相应决策门；“找不到”不等于 `not_applicable`。
- 招聘条件不是科学事实，面试题不是能力本体，百科只作为全景入口——三类均不可单独支撑高风险或争议结论。
- 重大范围变化（取证中发现目标需调整）→ 回到条件确认或返回 S1，不在下游静默改写目标。

## 9. 快速档与研究档附加门

- **S2+S3 允许合并**：领域成熟、单一范式、低风险、来源质量实质均匀；合并执行仍须先输出 `domain_evidence_landscape` 并通过 G2，再输出图谱并评价 G3。
- **S2+S3 禁止合并**：竞争范式、活跃分歧、来源可靠性明显不均、证据快速变化、前沿/高风险决策任一成立时，必须分开执行。
- **研究档专家门**：若研究档声明需要独立外部专家复核，但没有实际专家证据，记录 `pending` 或 `not_executed`；允许保存初步工件，但不得声称“研究档完成”或把专家门推断为已通过。
