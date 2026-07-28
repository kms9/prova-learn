---
name: al-03-build-capability-concept-graph
description: 读取同一 LLM Wiki run 中已通过 G1 的 S1 目标契约与已通过 G2 的 S2 逐题研究回答/多维校验，将其建模为可诊断的 capability_concept_graph，并按“完整 Markdown 人审文档→无损结构化 JSON→JSON 驱动的 S3 交互 HTML”交付三份工件，全程不生成独立图片。只要用户要进入个性化学习 S3、把目标与证据转成三层能力大纲、学习单元、原子知识点、映射、先修、评估与追溯，或修正既有图谱，就使用本 skill。
---

# 能力—概念图建模（S3）

负责“结构是什么”。把三层能力大纲作为图谱的层级视图，不创建第八阶段或平行
`learning_architecture` 真值源。不要在 S3 发明领域事实，也不要把课程目录或术语列表伪装成图谱。

## 独立运行时的阶段、门与依赖

- `S3` 是本 Skill 的能力—概念图建模阶段；`G3` 是 S3 图谱质量门。直接上游 `G1` 是 S1 目标契约质量门，`G2` 是 S2 领域证据质量门；这些编号不是学习理论或其他 Skill 名。
- 直接依赖一：S1 LLM Wiki run folder。G1 通过要求 S1 的 11 文件与七项机读条件通过；业务上代表目标、成功证据、范围和验收已经确定。
- 直接依赖二：同一 run 的 `s2/` 阶段区。G2 通过要求 S2 九文件、逐题映射、八维校验、真实六源研究、追溯、饱和、至少 L1 成熟度、确认、根索引和最终裁决九项机读条件全部通过，`g2-evaluation.md` 为 `verdict=pass`、`route_to=S3`。
- `G3` 通过是指层级与硬先修图无环、引用与核心覆盖完整、节点不重复且粒度一致、边可解释、关键节点可诊断、目标—节点—测评—来源全链路可追溯，最终 `verdict=pass`、`route_to=S4`。
- 本 Skill 不要求 S1/S2 Skill 目录共同安装；它消费同一 run folder 的根 `INDEX.md`、S1 根文件和 `s2/INDEX.md` 指向的九文件。裸目录、单个回答或调用者口头声称“G1/G2 已过”都不能替代门证据；缺失时 `input_validation.status=fail`，不生成正向图谱。

## 开始前

1. 读取 [stage-contract.md](references/stage-contract.md)。
2. 读取 [markdown-output-contract.md](references/markdown-output-contract.md)，按 S3 专属章节先生成完整人审文档。
3. 读取 [handoff-envelope.schema.json](references/handoff-envelope.schema.json) 和 [capability-concept-graph.schema.json](references/capability-concept-graph.schema.json)。
4. 读取 [evidence-to-learning-graph.md](references/evidence-to-learning-graph.md)，按其中的六源归一化、三层大纲、知识状态与图关系规则建模。
5. 读取 [html-visualization-contract.md](references/html-visualization-contract.md)；必须使用 [stage-report.html](assets/stage-report.html) 生成已填充的 S3 专用页面。
6. 仅在需要理解输出形状时读取 [example.md](references/example.md)；案例数据是设计夹具，不是真实观察。
7. 从根 `INDEX.md` 定位 S1 与 `s2/INDEX.md`，分别校验 G1 七项和 G2 九项条件；读取 S2 的逐题回答、八维校验、归一化原子、六源覆盖和来源，确认目标/范围/答案/来源可互相追溯。

## 执行

1. 用最终目标提出焦点问题；从可观察目标能力反推典型任务和判断，组织
   `target_capability → sub_capability → learning_unit` 组成层级。窄目标无需凑满三层，可把学习单元直接挂到
   `target_capability`，但在 `processing_record` 记录省略理由。
2. 只基于 S1 目标和 S2 已审计证据建图；先消费 S2 的统一原子项和多源覆盖矩阵，再聚类为能力领域、问题族/子能力和可教学学习单元，禁止按“招聘/书籍/论文/社区”等来源目录建大纲。
3. 将学习单元拆成唯一、可复用的原子 `nodes`；用 `unit_node_mappings` 建立多对多覆盖关系并标记
   `core | supporting | extension` 与理由，不把同一知识点复制成多个 ID。
4. 将组成层级、单元—节点覆盖、先修三类关系分开；只有 `edges` 表示学习先修。为每条边标记
   `hard | soft` 并给出理由，不从目录或展示顺序推断先修。
5. 为每个关键节点保留 `core_stable / core_practice / research_frontier / emerging_signal` 的进入理由、`stable / dynamic` 时效类型、多源证据和适用边界；社区或单一热点信号不得升级为核心节点。
6. 专家与普通岗位的差异优先建模为任务复杂度、自主性、影响范围、责任与掌握深度，不用堆叠工具关键词制造“专家节点”。
7. 为每个关键节点绑定可观察能力陈述、常见误概念、评估题（覆盖解释/应用/诊断/评估/迁移/记忆）、
   掌握门槛与补救入口。
8. 保留 `goal → role/capability → learning_unit → node → assessment → evidence/source` 的全链路追溯，并输出覆盖/缺口说明。
9. 向用户展示目标能力主干、学习单元粒度、核心关联与关键先修边界；遇明显遗漏或多种可比建模方案时
   执行条件确认，分歧会实质影响诊断或路径时升级为强制。
10. 生成 `capability_concept_graph`，再按 G3 量规逐项评价。

## Fail closed

- 缺 G1/G2 通过状态、版本不兼容或关键来源缺失时拒绝建图；`input_validation.status=fail`，不伪造正向工件。
- 事实依据不足时 `return_upstream → S2`，不在 S3 内隐式补造领域事实。
- 只有在已提供的目标、成功标准或范围存在可观察冲突时，才 `return_upstream → S1`；缺少 G1 工件本身只记为输入 prerequisite gap，不得推断为“目标矛盾”。
- 只有主题目录、无焦点问题/具名边/误概念/评估/来源时，主路由 `revise_here → S3`；若目录中的节点事实也缺少 S2 审计证据，则主路由 `return_upstream → S2`。两种情况都不进入 S4。
- 学习单元无核心知识点、映射指向未知 ID、核心节点未被覆盖、语义重复节点未归并，或把目录顺序当先修时，
  `revise_here → S3`；不得补造节点凑通过。
- 学习单元或映射依据的领域事实没有 S2 来源时 `return_upstream → S2`；目标/范围冲突时
  `return_upstream → S1`。
- S2 六源覆盖、饱和度、知识状态或时效不足以支持节点进入核心路径时 `return_upstream → S2`；不得由 S3 自行升级证据等级。
- 单元、节点、映射或先修语义实质改变时生成新 S3 工件版本，记录旧证据不可静默迁移及失效下游
  `["S4","S5","S6","S7"]`。
- 任何未通过 G3 的结果都在 `processing_record` 或 `quality_evaluation.evidence` 中显式记录失效下游范围至少为 `["S4","S5","S6","S7"]`。
- 无环性被破坏时 `revise_here → S3`，不静默删边凑通过。

## 输出

每次运行必须依次交付：完整 S3 Markdown 图谱审核报告、符合共同 Schema `1.3.0` 与正向工件 Schema
的无损结构化 JSON、由最终 JSON 填充的 S3 交互 HTML。Markdown 必须完整呈现三层大纲、学习单元、
原子节点、映射、硬/软关系、知识状态、评估、覆盖和追溯；JSON 不得删节为摘要，并须用
`document_artifact.section_mappings` 逐章对应。HTML 提供关系图、邻接表等阶段专属视图，图形始终保留
结构化等价表达。阻断时仍生成三份工件并展示真实结构缺口和
失效下游，不得显示通用文件装载器或空白占位。页面交互只用于检索、筛选、展开和浏览既有图谱，
不允许编辑图谱，也不展示 Schema、模板或 Markdown/HTML 生成状态。HTML 是本阶段唯一可视化交付；三层大纲、
关系图和知识点视图必须由内嵌规范 JSON 在页面内动态渲染。禁止调用 `imagegen`、`image_gen` 或其他
制图工具，禁止生成、引用或依赖独立的插图、知识点图片、静态图卡及 PNG/JPEG/WebP/SVG/GIF 等图片资产。
用户提到“知识点图片”或“可视化”时，默认实现为页面内可筛选、可展开、可聚焦的数据视图，不得自动
解释为制图任务。Markdown 失败写入 `document_artifact`，HTML 失败写入 `presentation_artifact`；
不得篡改 G3 门禁，但任一失败时整次阶段交付不得报告为完成。
只有层级与
硬先修子图分别无环、所有关联引用有效、每个学习单元至少有一个核心节点、目标必需节点无孤儿或无解释重复、
每条关键先修边可解释、每个目标能力可追溯到必要节点、每个关键节点均有可观察能力与评估证据且全链路
可追溯时，才允许 `verdict=pass`、`route_to=S4`。
