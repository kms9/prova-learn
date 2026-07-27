# check-rubric — S3 / 决策门 G3（能力—概念图质量判定标准）

> 本量规是 `check-capability-concept-graph` 的判定标准，与阶段 skill `build-capability-concept-graph/references/stage-contract.md` §6 保持一致。检查者独立重判，不采信被检工件自报的 `verdict`，并对硬先修子图自行验证无环。

## 判定流程

1. 结构校验：信封通过 `handoff-envelope.schema.json`；`positive_artifact` 通过 `capability-concept-graph.schema.json`。
2. 逐维判定下表（每维：证据 / 评分 / 阈值 / `passed`）。
3. 确认复核（S3 条件确认；高风险/分歧/多方案须已升级为强制并已解）。
4. 证据来源复核（节点与边的事实须可追溯到 S2 已审计来源；`model_hypothesis` 不得冒充 `external_evidence`）。
5. 汇总裁决与路由（多归因按上游优先级：目标矛盾→S1，证据空白→S2，结构问题→S3）。

## G3 维度量规

| 维度 | 阈值类型 | 通过阈值 | 证据来源（指向被检工件字段） |
|---|---|---|---|
| 结构无环性 | 硬先修子图无环 | true | `content.edges`（仅取 `prerequisite_strength=hard` 的子图，自验 DAG） |
| 先修边可解释性 | 每条关键先修边有理由；硬先修必有理由 | true | `content.edges[].rationale`（硬先修缺理由即不通过） |
| 目标覆盖率 | 每个目标能力可追溯到必要节点 | ≥1 节点/能力 | `content.target_capabilities[].capability_id` ↔ `content.traceability[].goal_refs` |
| 节点粒度一致性 | 节点粒度同阶，无“整章”与“单步”混排 | true | `content.nodes[]`（粒度、范围、抽象层级） |
| 能力与概念区分度 | 能力节点含可观察陈述，概念节点不冒充能力 | true | `content.nodes[].node_type` ↔ `content.nodes[].capability_statement` |
| 评估题有效性 | 每个关键节点有评估题且覆盖≥解释/应用/诊断/迁移之一 | true | `content.assessment_items[]`（按 `node_id` 对齐关键节点） |
| 全链路可追溯性 | 节点→来源(S2)/目标(S1)/评估均可追溯 | true | `content.traceability[]`（`source_refs`/`goal_refs`/`assessment_refs` 三向非空） |

## 通过条件（G3 pass）

当且仅当**全部**满足：

- 所有上表维度 `passed=true`；
- 硬先修子图经检查者自验为 DAG（无环），且每条硬先修边均有 `rationale`；
- 每个目标能力至少可追溯到一个必要节点，每个关键节点绑定可观察能力陈述与评估题；
- 节点与边的事实依据可追溯到 S2 已审计来源（`external_evidence`/`market_signal`），无 `model_hypothesis` 冒充外部证据；
- 确认已完成（条件确认 `acknowledged` 即可；升级为强制时须 `confirmed`/`corrected`）；
- 无 `criticality=critical` 且 `gate_effect=block` 的未决证据缺口阻塞建图。

通过 → `verdict=pass`、`route_to=S4`。

## 不通过时的路由

| 触发 | verdict | route_to |
|---|---|---|
| 粒度不一、边缺理由或不可解释、出现环、覆盖或评估缺失（结构局部可修） | revise_here | S3 |
| 事实依据不足或证据空白，需补检索/补视角/补证后再建图 | return_upstream | S2 |
| 目标、成功标准或范围本身不一致，需重签目标契约 | return_upstream | S1 |
| 输入契约缺失/版本不兼容/G1/G2 未通过且无法本地修复 | blocked | S3 |

> 多归因按上游优先级路由：目标不一致→S1，证据不足→S2，图谱结构问题→S3。每次路由记录主归因、次要归因、证据与失效下游范围（至少 S4–S7）。主题目录（无焦点问题/具名边/误概念/评估/来源）按结构缺陷归 `revise_here → S3`；若节点本身无 S2 证据则升级为 `return_upstream → S2`。

## 反模式（检查者不得犯）

- 直接采信被检工件自报 `verdict=pass` 而不逐维重判、不自验无环。
- 把 `model_hypothesis` 或 `user_provided_unverified` 计为已审计外部证据，或在图中补造领域事实凑通过。
- 硬先修子图出现环却仍给出 `pass`，或静默删边/改方向以消除环。
- 把主题目录（只有“下一章”式边、无 `rationale`/`capability_statement`/`assessment_items`/`traceability`）判为合格图。
- 修改被检工件或替 S3 重画图、补造节点与边。
