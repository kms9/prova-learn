---
name: build-capability-concept-graph
description: 将已通过 G1 的 goal_success_contract 与已通过 G2 的 domain_evidence_landscape 建模为含三层能力大纲、可测评学习单元、原子知识点、多对多单元—节点关联、硬软先修边、误概念、评估题、掌握门槛与全链路追溯的 capability_concept_graph。只要用户要进入个性化学习 S3、把目标与证据转成可诊断的知识结构、关联大纲与知识点、修正既有图谱，或判断一份“图”是否只是目录，就使用本 skill。
---

# 能力—概念图建模（S3）

负责“结构是什么”。把三层能力大纲作为图谱的层级视图，不创建第八阶段或平行
`learning_architecture` 真值源。不要在 S3 发明领域事实，也不要把课程目录或术语列表伪装成图谱。

## 开始前

1. 读取 [stage-contract.md](references/stage-contract.md)。
2. 读取 [handoff-envelope.schema.json](references/handoff-envelope.schema.json) 和 [capability-concept-graph.schema.json](references/capability-concept-graph.schema.json)。
3. 仅在需要理解输出形状时读取 [example.md](references/example.md)；案例数据是设计夹具，不是真实观察。
4. 校验 `goal_success_contract`（G1 通过）与 `domain_evidence_landscape`（G2 通过）均存在、版本兼容且目标/范围/来源可互相追溯。

## 执行

1. 用最终目标提出焦点问题；从可观察目标能力反推典型任务和判断，组织
   `target_capability → sub_capability → learning_unit` 组成层级。窄目标无需凑满三层，可把学习单元直接挂到
   `target_capability`，但在 `processing_record` 记录省略理由。
2. 只基于 S1 目标和 S2 已审计证据建图；不在图中补造领域事实，发现证据空白时返回 S2。
3. 将学习单元拆成唯一、可复用的原子 `nodes`；用 `unit_node_mappings` 建立多对多覆盖关系并标记
   `core | supporting | extension` 与理由，不把同一知识点复制成多个 ID。
4. 将组成层级、单元—节点覆盖、先修三类关系分开；只有 `edges` 表示学习先修。为每条边标记
   `hard | soft` 并给出理由，不从目录或展示顺序推断先修。
5. 为每个关键节点绑定可观察能力陈述、常见误概念、评估题（覆盖解释/应用/诊断/评估/迁移/记忆）、
   掌握门槛与补救入口。
6. 保留 `goal → capability → learning_unit → node → assessment → evidence/source` 的全链路追溯。
7. 向用户展示目标能力主干、学习单元粒度、核心关联与关键先修边界；遇明显遗漏或多种可比建模方案时
   执行条件确认，分歧会实质影响诊断或路径时升级为强制。
8. 生成 `capability_concept_graph`，再按 G3 量规逐项评价。

## Fail closed

- 缺 G1/G2 通过状态、版本不兼容或关键来源缺失时拒绝建图；`input_validation.status=fail`，不伪造正向工件。
- 事实依据不足时 `return_upstream → S2`，不在 S3 内隐式补造领域事实。
- 只有在已提供的目标、成功标准或范围存在可观察冲突时，才 `return_upstream → S1`；缺少 G1 工件本身只记为输入 prerequisite gap，不得推断为“目标矛盾”。
- 只有主题目录、无焦点问题/具名边/误概念/评估/来源时，主路由 `revise_here → S3`；若目录中的节点事实也缺少 S2 审计证据，则主路由 `return_upstream → S2`。两种情况都不进入 S4。
- 学习单元无核心知识点、映射指向未知 ID、核心节点未被覆盖、语义重复节点未归并，或把目录顺序当先修时，
  `revise_here → S3`；不得补造节点凑通过。
- 学习单元或映射依据的领域事实没有 S2 来源时 `return_upstream → S2`；目标/范围冲突时
  `return_upstream → S1`。
- 单元、节点、映射或先修语义实质改变时生成新 S3 工件版本，记录旧证据不可静默迁移及失效下游
  `["S4","S5","S6","S7"]`。
- 任何未通过 G3 的结果都在 `processing_record` 或 `quality_evaluation.evidence` 中显式记录失效下游范围至少为 `["S4","S5","S6","S7"]`。
- 无环性被破坏时 `revise_here → S3`，不静默删边凑通过。

## 输出

只输出符合两个 Schema 的 JSON 移交信封。先生成具名正向工件，再生成 `quality_evaluation`。只有层级与
硬先修子图分别无环、所有关联引用有效、每个学习单元至少有一个核心节点、目标必需节点无孤儿或无解释重复、
每条关键先修边可解释、每个目标能力可追溯到必要节点、每个关键节点均有可观察能力与评估证据且全链路
可追溯时，才允许 `verdict=pass`、`route_to=S4`。
