---
name: al-04-diagnose-learner-frontier
description: 用对齐目标与先修链的多项行为证据诊断学习者节点状态、误概念、提示依赖、迁移表现和置信度校准，并按“完整 Markdown 人审文档→无损结构化 learner_snapshot JSON→JSON 驱动的 S4 交互 HTML”交付三份工件，全程不生成独立图片。只要用户要进入个性化学习 S4、确定从哪里开始学、复测争议节点、修正既有诊断或排查“会做但讲不清”，就使用本 skill。
---

# al-s4-学习前沿诊断

从观察推断能力，不从自评、年限、偏好问卷或单题正确直接推断掌握。

## 独立运行时的阶段、门与依赖

- `S4` 是本 Skill 的学习者诊断阶段；`G4` 是 S4 学习前沿质量门。直接依赖的 `G1` 是 S1 目标契约质量门，`G3` 是 S3 能力—概念图质量门。
- `goal_success_contract` 通过 G1，表示目标、成功证据、范围与验收已经确认；机读上要求兼容 S1 信封完成、输入校验通过、工件合法、G1 全量规通过、`verdict=pass`、`route_to=S2`。
- `capability_concept_graph` 通过 G3，表示节点、先修、误概念、测评和来源追溯可用于诊断；机读上要求兼容 S3 信封完成、输入校验通过、工件合法、G3 全量规通过、`verdict=pass`、`route_to=S4`。
- `G4` 通过是指关键节点由多项、对齐且在有效期内的真实行为证据支持，识别/独立/迁移和提示依赖被区分，最近学习前沿可解释，最终 `verdict=pass`、`route_to=S5`。
- 本 Skill 可在没有 S1/S3 Skill 目录时独立运行，但必须收到上述兼容信封；裸工件或自然语言门声明保持未验证，不从中推断学习者状态。

## 开始前

1. 读取 [stage-contract.md](references/stage-contract.md)。
2. 读取 [markdown-output-contract.md](references/markdown-output-contract.md)，按 S4 专属章节先生成完整人审文档。
3. 读取 [handoff-envelope.schema.json](references/handoff-envelope.schema.json) 和 [learner-snapshot.schema.json](references/learner-snapshot.schema.json)。
4. 读取 [html-visualization-contract.md](references/html-visualization-contract.md)；必须使用 [stage-report.html](assets/stage-report.html) 生成已填充的 S4 专用页面。
5. 仅在需要理解输出形状时读取 [example.md](references/example.md)；案例数据是设计夹具，不是真实观察。
6. 确认上游 G1、G3 已通过，关键节点具有可执行诊断项；既有学习记录须带身份、时间、来源和有效期，过期证据只作线索。

## 执行

1. 先声明要推断的节点/能力以及每类证据的判定规则，再选择诊断任务。
2. 沿目标与先修链组合解释、预测、反例、诊断、比较、迁移和置信度任务；优先使用 S2/S3 已追溯的真实任务、失败案例、Benchmark 与误概念，包含无错题与隐蔽错题，避免只测口号识别。
3. 收集真实学习者回答；记录正确性、推理过程、提示层级、耗时（可得时）、置信度和错误类型。
4. 关键结论须由多项对齐观察支持；显式区分“答对”“独立会做”“能迁移”与“证据不足”。
   - `tested_mastered` 必须有同一节点在 `hint_dependency.level=none|low` 下的独立证据；只有 `medium|high|unknown` 提示记录时，最多标为 `tested_not_mastered` 或 `insufficient_evidence`，并安排撤除支架后的复测。
   - 向 S7 移交时按 `none→none`、`low→low`、`medium→moderate`、`high→high` 归一；
     `unknown` 仅在没有可用提示记录时成为 `not_executed`。
5. 学习者对结论有异议时，对争议节点追加测试；自述只用于选题，不得覆盖行为证据。
6. 检查诊断项所依赖的动态知识是否仍在有效期；社区信号只能用于生成待测误概念，不得直接当成学习者误概念或正确答案。
7. 递归定位最近可学习节点；生成 `model_version>=1` 的版本化 `learner_snapshot`，再按 G4 量规逐项评价。

## Fail closed

- 无真实学习者回答时，只产出诊断任务并保持 `pending`；不模拟回答、不伪造前沿。
- 冷启动返回 `unknown`/`insufficient_evidence`，路由到 S4 建立初始证据；首个真实快照版本从 1 开始，不得用版本 0 创建“全部未掌握”画像。
- 单题、纯自评或仅口号识别不得决定关键节点状态。
- 诊断题无法产生目标证据时返回 S3；图谱或来源缺失时返回 S2/S3。
- 诊断暴露真实任务、失败模式、评估基准或来源时效缺口时返回 S2；只是节点/评估映射错误时返回 S3。
- S4+S5 仅在确认零基础、图谱起点明确、路径近线性且任务低风险时才可合并；存在先验未知、证据冲突、多前沿或高风险决策时禁止合并。

## 输出

每次运行必须依次交付：完整 S4 Markdown 诊断审核报告、符合共同 Schema `1.3.0` 与
`learner-snapshot.schema.json` 的无损结构化 JSON、由最终 JSON 填充的 S4 交互 HTML。Markdown 必须
完整呈现事前规则、任务、原始行为、节点判断、提示/置信度、学习前沿、误概念、迁移、复测、限制与 G4；
JSON 不得删节为状态摘要，并须用 `document_artifact.section_mappings` 逐章对应。无真实回答时三份工件
必须直接展示已生成的诊断任务、事前规则和
所需记录字段，不得显示通用文件装载器或空白占位。页面交互只用于筛选、对照和展开既有诊断数据，
不接受学习者作答，也不展示 Schema、模板或 Markdown/HTML 生成状态。HTML 是本阶段唯一可视化交付；所有诊断
视图必须由内嵌规范 JSON 在页面内动态渲染。禁止调用 `imagegen`、`image_gen` 或其他制图工具，禁止
生成、引用或依赖独立的插图、知识点图片、静态图卡及 PNG/JPEG/WebP/SVG/GIF 等图片资产。用户提到
“图片”或“可视化”时，默认实现为页面内的数据视图，不得自动解释为制图任务。Markdown 失败写入
`document_artifact`，HTML 失败写入 `presentation_artifact`；不得篡改 G4 门禁，但任一失败时整次阶段交付不得报告为完成。只有学习前沿有多项、可追溯且在有效期内的
行为证据，关键结论区分了识别/独立/迁移，且 G4 全维度通过时，才允许 `verdict=pass`、`route_to=S5`。
