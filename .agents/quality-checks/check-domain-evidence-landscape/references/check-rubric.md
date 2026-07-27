# check-rubric — S2 / 决策门 G2（领域证据全景质量判定标准）

> 本量规是 `check-domain-evidence-landscape` 的判定标准，与阶段 skill `create-domain-evidence-landscape/references/stage-contract.md` §6 保持一致。检查者独立重判，不采信被检工件自报的 `verdict`，特别警惕“少量同源博客即共识”。

## 判定流程

1. 结构校验：信封通过 `handoff-envelope.schema.json`；`positive_artifact` 通过 `domain-evidence-landscape.schema.json`。
2. 强制联网复核（G2 硬门槛）：`research_run_manifest.online=true` 且 `execution_status=completed`。
3. 逐维判定下表（每维：证据 / 评分 / 阈值 / `passed`）。
4. 证据来源复核（外部证据门）：`model_hypothesis`/`user_provided_unverified` 不计为外部证据；`market_signal` 不写成 `fact`。
5. 汇总裁决与路由。

## G2 维度量规

| 维度 | 阈值类型 | 通过阈值 | 证据来源（指向被检工件字段） |
|---|---|---|---|
| 实际联网执行 | research_executed ∧ online ∧ execution_status=completed | true | `content.research_executed` + `content.research_run_manifest` |
| 强制来源类别覆盖 | 六类均有状态；covered 或可审计的 not_applicable/gap；关键类样本量达标 | true | `content.category_coverage[]` |
| 来源可靠性与时效 | 关键结论可追溯至可靠且当前来源 | true | `content.source_ledger[].reliability/published_at/retrieved_at` |
| 结论可追溯性 | 每项 claim 至少有一条 `evidence_refs` | true | `content.claims[].evidence_refs` |
| 关键主题覆盖率 | core_questions 覆盖目标范围关键决策点且非空 | ≥1 | `content.core_questions_and_mental_models.core_questions` |
| STORM 视角与问题多样性 | perspectives≥6 且各有 questions 与 query_ids | ≥6 | `content.research_run_manifest.perspectives[]` |
| 后续追问深度 | rounds≥1 且冲突/新发现触发后续查询 | true | `content.research_run_manifest.rounds` / `follow_up_triggers` |
| 岗位/面试样本代表性 | 招聘≥3 样本/2 组织；面试≥2 组独立样本；未达标记 gap 而非忽略 | true | `content.jd_capability_matrix` + `interview_assessment_matrix` + `category_coverage` |
| 时效与地区适配性 | retrieved_at、region 与目标口径（`scope`）一致 | true | `content.source_ledger[].retrieved_at/region` ↔ `content.scope` |
| 事实/市场信号/推断分离 | market_signal 未写成 fact；模型假设未计为外部证据 | true | `content.claims[].claim_type` + 信封 `evidence_collected[].provenance` |
| 争议平衡 | 重要争议不被单边伪装成共识，`disagreements` 保留双方 strong_arguments | true | `content.disagreements[].side_a/side_b` |
| 证据缺口透明度 | 缺口显式标记且含 `confidence_impact` 与 `gate_effect` | true | `content.evidence_gaps[]` |

## 通过条件（G2 pass）

当且仅当**全部**满足：

- 所有上表维度 `passed=true`；
- `content.research_executed=true` 且 `research_run_manifest.online=true` 且 `execution_status=completed`；
- 强制来源类别覆盖中无 `criticality=critical` 且 `gate_effect=block` 的未决缺口；
- 关键产品行为 `claims` 至少可追溯至一手 `external_evidence`（`market_signal`/`model_hypothesis` 不充当一手事实）。

通过 → `verdict=pass`、`route_to=S3`。

## 不通过时的路由

| 触发 | verdict | route_to |
|---|---|---|
| 研究过浅/不平衡/过期、来源类别缺失、查询仅一次、冲突未解释、样本不足 | revise_here | S2 |
| 无联网能力或 `research_run_manifest.online=false` / `execution_status=blocked` | blocked | S2 |
| 局部证据缺口（S3 建图发现来源空白，需局部补证，不推倒全部结果） | return_upstream | S2 |
| 取证中发现目标本身实质改变（S1 成功契约失效） | return_upstream | S1 |

> `revise_here`（同阶段重做研究）与 `return_upstream → S2` 的区别：前者是当前研究未达标、就地补强；后者多见于 S3 建图阶段发现局部空白后回拉。目标被实质改变时才回最早污染阶段 S1。

## 反模式（检查者不得犯）

- 直接采信被检工件自报 `verdict=pass` 而不逐维重判。
- 把 `model_hypothesis`/`user_provided_unverified` 计为外部证据，或把 `market_signal`（JD/面经）写成产品事实。
- 把“找不到资料”记为 `not_applicable` 而非 `gap`，或用模型记忆替代缺失的一手来源。
- 把搜索结果数量当作证据质量，或把同源转载博客当作独立来源。
- 用用户确认豁免联网执行硬门槛。
- 修改被检工件或替 S2 生成新的领域证据。
