# S3 阶段契约 — build-capability-concept-graph（门 G3）

> 本文件治理 S3 与决策门 G3。§0 为七阶段共享规则；其余为 S3 专属。

## 0. 共享阶段契约（适用于 S1–S7）

- **编号定义**：`Sx` 是第 x 个执行阶段（Stage），`Gx` 是紧随 Sx、评价该阶段工件能否被下游消费的质量决策门（Gate）。例如 `G1` 是 S1 目标契约质量门，不是学习理论、外部标准或另一个 Skill。
- **“已通过 Gx”的机读含义**：不能凭文件存在或自然语言声称推断。S1 使用 11 文件与 G1 七项 run-folder 条件；S2 使用同一 run 中 `s2/` 九文件与 G2 九项条件；S3–S7 在各自迁移前仍验证兼容移交信封、具名正向工件、全量规、verdict/route、确认和三工件状态。

S3–S7 当前必须产出**三份内容一致、用途不同的工件**：

1. 一份按当前阶段专属结构撰写的完整 Markdown 人审文档；
2. 一份把 Markdown 全部实质内容无损结构化的规范 JSON 移交信封（`handoff-envelope.schema.json`）；
3. 一份由最终 JSON 填充的阶段专用交互 HTML。

S3 当前执行形状：

```text
校验输入契约
→ 收集需求缺口
→ 执行本阶段确认策略
→ 收集可采信证据
→ 先完成阶段专属 Markdown 的事实、分析、结论、量规与路由
→ 将同一内容无损结构化为具名正向工件与 JSON 移交信封
→ 校验 Markdown 章节与 JSON Pointer 的逐项对应
→ 派生并验证阶段专用 HTML
```

- **三工件权威边界**：Markdown 是首要人审文档，JSON 是机器移交的规范表示，HTML 是 JSON 驱动的只读派生视图。Markdown 与 JSON 必须语义等价，不能以“摘要 JSON”丢弃文档中的证据、边界、缺口、失败条件、异议或路由依据。
- **严格生成顺序**：先完成 Markdown 实质内容，再生成 JSON，最后生成 HTML。JSON/HTML 生成后只允许回填路径、工件标识和验证状态等机械信息；实质内容变化必须同步 Markdown 与 JSON 并重新验证。
- **输入契约校验**：S3 至少检查 S1/S2 run-folder 文件、稳定 ID、问题/回答/证据追溯与上游门状态，再检查自身输出 Schema。失败时 `input_validation.status=fail` 并路由上游，**不得伪造正向工件**。
- **确认状态机**：`mandatory`（S1/S5，未确认不得前进）、`conditional`（S2/S3/S4/S7，遇高风险/分歧/多方案升级为强制）、`inform`（S6 节点推进，告知后继续）。
- **证据来源分类**：`model_hypothesis`/`market_signal`/`external_evidence`/`user_provided_unverified`/`learner_behavior`。**门不得把 `model_hypothesis` 或 `user_provided_unverified` 计为外部证据。**
- **量规结果形状**：`{dimension, evidence[], score, threshold, passed, failure_action, route_to}`；`passed=false` 时 `failure_action` 与 `route_to` 必填。
- **显式未知/阻塞态**：`pending`/`blocked`/`unknown`/`evidence_insufficient`/`research_blocked`/`not_executed`/`version_conflict` 不得被强制为 `pass`。
- **确定性路由**：`pass` 前进；`revise_here` 同阶段重试；`return_upstream` 指向**最早**污染阶段并记录失效下游范围。S7 多归因按上游优先级路由。
- **合并守卫**：快速档仅可在满足条件时合并 S2+S3 或 S4+S5，仍须分别产出工件并依次通过两门；S1、S7 永不合并。
- **强制完整文档**：每次运行都必须遵守当前 skill 的 `markdown-output-contract.md`。`pending` 或 `blocked` 也要完整写明已知事实、未知项、未执行项、当前结论与恢复条件；禁止空标题、空表、`TBD`、`TODO`、示例数据或其他占位内容。
- **强制页面派生**：每次运行都必须基于最终信封生成已填充的本阶段专用 HTML；`pending` 或 `blocked` 也展示真实缺口、当前结论和恢复条件，不得使用通用装载器或空白占位。
- **只生成数据驱动页面**：HTML 是唯一可视化交付，页面视图必须由内嵌规范 JSON 动态渲染；禁止调用制图/图像生成工具，禁止生成、引用或依赖独立图片、插图、知识点图卡或其他静态图片资产。
- **只读展示边界**：页面交互仅用于切换、搜索、筛选、展开和浏览既有数据；不得接受业务输入、导出草稿，或展示 Schema、模板、Markdown/HTML 生成状态及输出说明。
- **交付完整性**：Markdown、JSON 或 HTML 任一缺失，Markdown—JSON 对应失败，或 HTML 三项验证任一失败时，均不得把本次阶段交付报告为完整完成；文档/页面失败不篡改领域门禁本身。

## 1. S3 目的

把目标问题和领域证据转成“能力大纲—可测评学习单元—原子知识点—先修关系—掌握证据”的可计算结构。
S3 是“目标校准—领域研究”对（S1–S2）之后、学习者诊断（S4）之前的结构建模半边：它回答“稳定结构
由哪些学习单元和知识点组成，它们如何覆盖目标，以及知识点之间有什么先修关系”。三层能力大纲是
`capability_concept_graph` 的层级视图，不是独立阶段或平行工件。六源证据到图谱的具体转换规则见
`evidence-to-learning-graph.md`。

## 2. S3 输入契约

| 输入 | 是否必填 | 说明 |
|---|---|---|
| S1 run folder | 必填 | 必须已通过 G1 七项；提供焦点问题来源、目标能力、范围与验收任务 |
| 同一 run 的 `s2/` 阶段区 | 必填 | 必须已通过 G2 九项；提供逐题研究回答、八维校验、六源覆盖、统一原子对象、结构饱和、成熟度、时效与来源 |
| 上游追溯一致性 | 必填 | 目标、范围与来源标识可互相追溯；版本兼容 |

冷启动证据不全时返回 S2 局部补充，不在 S3 内隐式补造领域事实；目标本身矛盾时返回 S1。`input_validation.status=fail` 时不产出正向工件。

> **S1/S2 已迁移到同一 LLM Wiki run**：入口为
> `workspace/<project-slug>/runs/<最新 run>/INDEX.md`。读取目标能力/范围/验收时按 S1 七项校验并取
> `goal-contract.md`/`capabilities.jsonl`；读取领域依据时由根索引进入 `s2/INDEX.md`，按 G2 九项校验并取
> `research-answers.md`、`answer-validation.md`、`evidence-items.jsonl`、`coverage.md` 和
> `sources.jsonl`。S2 不再提供 JSON 信封。

## 3. S3 确认策略（条件确认）

向用户展示目标能力主干、学习单元粒度、核心单元—节点关联、关键边界与硬/软先修判断。对优先级、明显
遗漏或多种可比建模方案做**条件确认**；当不同建模会实质改变下游诊断题、评估证据或学习路径时，升级为
强制确认（`confirmation.mode=mandatory`）。无分歧时 `confirmation.mode=conditional`、
`status=acknowledged` 即可前进。

## 4. S3 建模规则（不可降级）

- **只基于 S1 目标和 S2 已审计证据**：从目标能力反推所需判断与任务，再反推概念、程序、策略、表征与经验模式，最后反推元认知节点。
- **先归一化再组织能力大纲**：从 S2 的 `Task / Capability / Knowledge / Skill / Evidence` 与扩展对象出发，以真实问题聚类，`target_capability → sub_capability → learning_unit` 只表达组成。
  窄目标可把学习单元直接挂到目标能力，但必须记录省略中间层理由，不能为满足层数制造空节点。
- **学习单元—节点关联为多对多**：用 `core | supporting | extension` 表达稳定覆盖，同一原子知识点复用
  同一个 `node_id`；`introduce/reinforce/review` 等个性化顺序由 S5/S6 决定。
- **三类关系不得混用**：层级父子关系表示组成，`unit_node_mappings` 表示覆盖，`edges` 才表示学习先修；
  展示顺序不能充当先修证据。
- **不得发明领域事实**：节点与边的事实依据必须可追溯到 S2 的 claim/source；模型只可对结构做推断（`model_hypothesis`），不可把推断写成已审计事实。发现证据空白时 `return_upstream → S2`，不在图中补造。
- **来源不是目录**：不得以岗位、书籍、论文、社区、标准、案例作为并列章节；来源只用于证明由任务与能力聚类出的结构。
- **分层进入路径**：`core_stable` 与目标所需 `core_practice` 可进入必修；`research_frontier` 默认扩展；`emerging_signal` 默认观察；争议项保留竞争观点与适用条件。
- **岗位级别映射深度**：专家差异主要映射为自主性、复杂度、影响、责任、迁移/创造和验收难度，不复制概念或堆叠工具名。
- **先修边必须具名且可解释**：每条边标记 `hard | soft` 并给出理由；硬先修子图必须是 DAG，不得出现环或不可解释的跨越。
- **节点必须可诊断**：每个关键节点绑定可观察能力陈述、常见误概念、评估题、掌握门槛与补救入口。
- **保留全链路追溯**：`goal → capability → node → assessment → evidence/source`。
- **合并守卫**：只有领域成熟、单一范式、来源质量均匀且低风险时才允许合并 S2+S3；合并后仍须先输出并通过 G2，再生成本工件并通过 G3。

## 5. S3 工件字段（`capability_concept_graph.content`）

`focus_question`（焦点问题）、`goal_contract_ref`、`evidence_landscape_ref`、
`source_atom_mappings[]`（S2 原子项到 S3 节点/能力的映射）、`knowledge_status_summary[]`（证据层级、知识状态、时效、覆盖与边界）、`role_capability_ladder[]`、`coverage_and_gap_report`、
`target_capabilities[]`（`capability_id/statement/sub_capabilities[]/typical_tasks[]`）、
`learning_units[]`（`unit_id/title/parent_ref/parent_level[target_capability|sub_capability]/outcome/goal_refs[]/
source_refs[]/scope_role[required|optional|extension]`）、
`nodes[]`（`node_id/node_type[concept|procedure|strategy|representation|metacognition]/capability_statement/
common_misconceptions[]`）、
`unit_node_mappings[]`（`unit_id/node_id/coverage_role[core|supporting|extension]/rationale`）、
`edges[]`（`from_node/to_node/prerequisite_strength[hard|soft]/rationale`，有向边构成 DAG）、
`assessment_items[]`（`node_id/item/cognitive_level[explain|apply|diagnose|evaluate|transfer|remember]`）、
`mastery_thresholds[]`（每节点 `node_id/threshold/requires_transfer`）、
`remediation_entries[]`（`node_id/trigger/entry`）、
`traceability[]`（`node_id/source_refs[]/goal_refs[]/assessment_refs[]`，节点→来源/目标/评估）。

ID 必须唯一且引用可解析。标题小改可保留实体 ID；语义实质变化须产生替代 ID/新 S3 工件版本，保留旧身份供
审计，并记录依赖旧语义的 S4–S7 失效范围。不得把旧学习者证据静默挂到新语义。

## 6. S3 量规（门 G3）

| 维度 | 阈值类型 | 阈值 | 证据来源 |
|---|---|---|---|
| 结构无环性 | 硬先修子图无环 | true | edges（hard 子图） |
| 层级与引用完整性 | 父级引用与单元—节点引用均存在；组成层级无环 | true | target_capabilities + learning_units + unit_node_mappings |
| 学习单元核心覆盖 | 每个学习单元至少有一个 `core` 映射 | true | learning_units ↔ unit_node_mappings |
| 必需节点无孤儿 | 每个目标必需节点至少被一个学习单元覆盖 | true | nodes ↔ unit_node_mappings |
| 原子节点唯一性 | 无语义重复且未说明替代关系的核心节点 | true | nodes + processing_record |
| 先修边可解释性 | 每条关键先修边有理由；硬先修必有理由 | true | edges.rationale |
| 目标覆盖率 | 每个目标能力可追溯到必要节点 | ≥1 节点/能力 | target_capabilities ↔ traceability.goal_refs |
| 节点粒度一致性 | 节点粒度同阶，无“整章”与“单步”混排 | true | nodes |
| 能力与概念区分度 | 能力节点含可观察陈述，概念节点不冒充能力 | true | nodes.capability_statement |
| 评估题有效性 | 每个关键节点有评估题且覆盖≥解释/应用/诊断/迁移之一 | true | assessment_items |
| 全链路可追溯性 | 节点→来源(S2)/目标(S1)/评估均可追溯 | true | traceability |
| 六源归一化完整性 | S2 原子项到能力/节点映射可审计，来源未被当成目录 | true | source_atom_mappings |
| 核心进入规则 | 核心/实践/前沿/新兴状态与时效、证据覆盖一致 | true | knowledge_status_summary |
| 岗位深度建模 | 职级差异表达任务深度和责任，而非词汇数量 | true | role_capability_ladder |

G3 通过当且仅当**所有维度** `passed=true`、确认完成且无证据缺口阻塞建图。主题目录（无焦点问题/
可测评学习单元/有效关联/具名边/误概念/评估/来源）不通过 G3。

## 7. S3 路由

| verdict | route_to | 触发 |
|---|---|---|
| `pass` | S4 | 全部 G3 维度通过；目标能力均可追溯到必要节点且关键节点均有可观察能力与评估证据 |
| `revise_here` | S3 | 结构局部可修：层级/粒度不一、映射悬空、核心覆盖缺失、节点重复、把展示顺序当先修、边缺理由、出现环或评估缺失 |
| `return_upstream` | S2 | 事实依据不足或证据空白，需补检索/补视角/补证后再建图 |
| `return_upstream` | S1 | 目标、成功标准或范围本身不一致，需重签目标契约 |
| `blocked` | S3 | 输入契约缺失/版本不兼容且无法本地修复 |

存在多个归因时按上游优先级路由：目标不一致→S1，证据不足→S2，图谱结构问题→S3。每次路由记录主归因、次要归因、证据与失效下游范围（至少 S4–S7）。

这里的“目标不一致”必须有已提供目标/成功标准/范围之间的可观察冲突；**缺少 G1 工件不等于目标不一致**。对只有主题目录且 G1/G2 均缺失的输入，缺失 G1 记为 prerequisite gap，不单独触发 S1：若目录节点事实无 S2 审计证据，主路由 `return_upstream → S2`；若事实已有证据而只缺图谱结构，主路由 `revise_here → S3`。无论采用哪条主路由，都必须显式记录失效下游范围至少 `["S4","S5","S6","S7"]`。

## 8. S3 安全/阻塞态

- 上游 G1/G2 未通过或版本不兼容 → `input_validation.status=fail`，不产出正向工件。
- 证据空白 → `return_upstream → S2`，**不**在 S3 补造事实或把模型推断标为 `external_evidence`。
- 出现环 → `revise_here → S3`，不静默删边或改方向凑通过。
- 学习单元没有核心节点、关联引用悬空、目标必需节点无覆盖或节点语义重复 → `revise_here → S3`，不补造
  映射或复制节点凑通过。
- 学习单元/映射事实无 S2 依据 → `return_upstream → S2`。
- 单元、节点、映射或先修发生语义变化 → 新建 S3 工件版本并显式使受影响 S4–S7 失效。
- 目录伪装成图 → `revise_here → S3`；若节点本身无证据则 `return_upstream → S2`。
- 目标矛盾 → `return_upstream → S1`。
- S2↔S3 允许多轮局部迭代；严谨档下关键工件使用独立评审。
