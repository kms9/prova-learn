# S3 阶段契约 — build-capability-concept-graph（门 G3）

> 本文件治理 S3 与决策门 G3。§0 为七阶段共享规则；其余为 S3 专属。

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

## 1. S3 目的

把目标问题和领域证据转成“能力大纲—可测评学习单元—原子知识点—先修关系—掌握证据”的可计算结构。
S3 是“目标校准—领域研究”对（S1–S2）之后、学习者诊断（S4）之前的结构建模半边：它回答“稳定结构
由哪些学习单元和知识点组成，它们如何覆盖目标，以及知识点之间有什么先修关系”。三层能力大纲是
`capability_concept_graph` 的层级视图，不是独立阶段或平行工件。

## 2. S3 输入契约

| 输入 | 是否必填 | 说明 |
|---|---|---|
| `goal_success_contract` | 必填 | 必须已通过 G1；提供焦点问题来源、目标能力、范围与验收任务 |
| `domain_evidence_landscape` | 必填 | 必须已通过 G2；提供可追溯的术语、来源、claim 与证据 |
| 上游追溯一致性 | 必填 | 目标、范围与来源标识可互相追溯；版本兼容 |

冷启动证据不全时返回 S2 局部补充，不在 S3 内隐式补造领域事实；目标本身矛盾时返回 S1。`input_validation.status=fail` 时不产出正向工件。

## 3. S3 确认策略（条件确认）

向用户展示目标能力主干、学习单元粒度、核心单元—节点关联、关键边界与硬/软先修判断。对优先级、明显
遗漏或多种可比建模方案做**条件确认**；当不同建模会实质改变下游诊断题、评估证据或学习路径时，升级为
强制确认（`confirmation.mode=mandatory`）。无分歧时 `confirmation.mode=conditional`、
`status=acknowledged` 即可前进。

## 4. S3 建模规则（不可降级）

- **只基于 S1 目标和 S2 已审计证据**：从目标能力反推所需判断与任务，再反推概念、程序、策略、表征与经验模式，最后反推元认知节点。
- **先组织能力大纲，再建知识图**：`target_capability → sub_capability → learning_unit` 只表达组成。
  窄目标可把学习单元直接挂到目标能力，但必须记录省略中间层理由，不能为满足层数制造空节点。
- **学习单元—节点关联为多对多**：用 `core | supporting | extension` 表达稳定覆盖，同一原子知识点复用
  同一个 `node_id`；`introduce/reinforce/review` 等个性化顺序由 S5/S6 决定。
- **三类关系不得混用**：层级父子关系表示组成，`unit_node_mappings` 表示覆盖，`edges` 才表示学习先修；
  展示顺序不能充当先修证据。
- **不得发明领域事实**：节点与边的事实依据必须可追溯到 S2 的 claim/source；模型只可对结构做推断（`model_hypothesis`），不可把推断写成已审计事实。发现证据空白时 `return_upstream → S2`，不在图中补造。
- **先修边必须具名且可解释**：每条边标记 `hard | soft` 并给出理由；硬先修子图必须是 DAG，不得出现环或不可解释的跨越。
- **节点必须可诊断**：每个关键节点绑定可观察能力陈述、常见误概念、评估题、掌握门槛与补救入口。
- **保留全链路追溯**：`goal → capability → node → assessment → evidence/source`。
- **合并守卫**：只有领域成熟、单一范式、来源质量均匀且低风险时才允许合并 S2+S3；合并后仍须先输出并通过 G2，再生成本工件并通过 G3。

## 5. S3 工件字段（`capability_concept_graph.content`）

`focus_question`（焦点问题）、`goal_contract_ref`、`evidence_landscape_ref`、
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
