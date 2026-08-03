---
name: al-s6-run-instructional-interaction
description: 为已确认路径上的当前学习节点生产可追溯、分层、含正反例与渐隐支架的教学内容，并按“完整 Markdown 人审文档→无损结构化 session_package_and_trace JSON→JSON 驱动的 S6 交互 HTML”交付三份工件，全程不生成独立图片。只要用户要进入个性化学习 S6、开展学习会话、调整教学形式或修复内容质量，就使用本 skill。
---

# al-s6-教学交互执行

本阶段的完成条件是产生可解释的学习者行为证据，不是教师输出结束。G6 只评价教学工件质量，绝不宣布学习者掌握。

## 独立运行时的阶段、门与依赖

- `S6` 是本 Skill 的教学内容与真实交互阶段；`G6` 是 S6 教学工件和候选证据质量门，不是掌握门。
- 直接依赖包括：通过 G5 的 `learning_and_session_plan`、通过 G3 的 `capability_concept_graph`、通过 G2 的 `domain_evidence_landscape`、通过 G4 且仍有效的 `learner_snapshot`。G2/G3/G4/G5 分别是 S2 证据、S3 图谱、S4 诊断和 S5 计划质量门。
- 每个“已通过”都必须由对应 S2–S5 兼容信封证明：阶段完成、输入校验通过、具名工件合法、该门全部量规通过、`quality_evaluation.verdict=pass`，并路由到下一阶段；裸工件或自然语言声明不算门证据。
- `G6` 通过是指内容正确可追溯、适配目标与学习前沿、认知层级和正反/边界例完整、提示不替代推理、无答案泄露、存在真实交互与非空候选掌握证据，最终 `verdict=pass`、`route_to=S7`。它只允许 S7 开始验证，不代表学习者已经掌握。
- 本 Skill 不要求上游 Skill 目录共同安装；缺少任何直接依赖的门证据时记录 prerequisite gap，并路由到最早失效阶段。

## 开始前

1. 读取 [stage-contract.md](references/stage-contract.md)。
2. 读取 [markdown-output-contract.md](references/markdown-output-contract.md)，按 S6 专属章节先生成完整人审文档。
3. 读取 [handoff-envelope.schema.json](references/handoff-envelope.schema.json) 和 [session-package-and-trace.schema.json](references/session-package-and-trace.schema.json)。
4. 读取 [html-visualization-contract.md](references/html-visualization-contract.md)；必须使用 [stage-report.html](assets/stage-report.html) 生成已填充的 S6 专用页面。
5. 仅在需要理解输出形状时读取 [example.md](references/example.md)；案例数据是设计夹具，不是真实观察。
6. 校验当前节点属于已确认计划、硬先修通过、来源可追溯、学习者快照有效且目标与节点通关标准一致。

## 执行

1. 会话开始时执行 `inform` 确认：告知目标、约束、媒介与“过程记录用于更新学习者模型”。
2. 检查本会话目标、可用媒介、学习者当前状态、材料与例子缺口；确定本轮需要解释、示范、练习还是迁移。
3. 按证据角色选择内容：书课/标准用于稳定原理，论文用于方法与争议，岗位用于真实任务深度，案例/Benchmark/事故用于应用与失败条件，社区仅用于待验证痛点、误解和反例线索；标明来源、知识状态、时效与适用边界，模型常识不得包装为审计事实。
4. 组合分层解释、多表征、正反例、边界案例与常见误解；让抽象与具体互相连接。
5. 设计渐进练习（检索前测 → worked example → 半完成 → 对比 → 独立迁移）；难度处于当前可学习范围。
6. 先让学习者产出，再给反馈；建立逐级提示并按回答逐步撤架；提示指向形状或规则，不代替关键推理。
7. 防止答案泄露：独立任务提交前不公布答案。
8. 每个关键解释至少有权威/稳定来源或真实验证证据；动态工具做法在会话前检查时效。若社区说法与标准、论文或真实产物冲突，作为对比案例呈现，不静默定为真。
9. 完整记录交互轨迹：每次回答、实际使用的提示、修正轨迹、未解决问题与内容变化。提示阶梯只是计划；
   向 S7 移交时仅按真实事件把 `light/medium/strong` 归一为 `low/moderate/high`，未使用为 `none`，缺记录为 `not_executed`。
10. 仅在至少形成一项真实 `candidate_mastery_evidence` 时生成 G6 正向工件；再按 G6 量规逐项评价。

## Fail closed

- 关键内容无可追溯来源时返回 S2/S3 或 `blocked`，不把模型常识包装成审计事实。
- 内容依赖已过期动态证据、只有社区信号或缺少真实应用/失败边界时返回 S2 局部补证；节点归类错误时返回 S3。
- 学习者尚未作答时保持 `pending`，不要代写 `learner_behavior` 证据。
- 答案泄露或无独立作答时留在 S6 重生成；禁止进入 S7 宣称掌握。
- 内容正确但连续卡住时返回 S5 调策略，必要时返回 S4 重诊断。
- G6 只评价教学工件质量，绝不能宣布学习者掌握。

## 输出

每次运行必须依次交付：完整 S6 Markdown 教学与交互审核报告、符合共同 Schema `1.3.0` 与正向工件
Schema 的无损结构化 JSON、由最终 JSON 填充的 S6 交互 HTML。Markdown 必须完整呈现来源边界、分层解释、
正反/边界案例、活动、泄露控制、提示/反馈/撤架、真实交互、候选证据、限制、G6 与路由；JSON 不得删节
为教学提纲，并须用 `document_artifact.section_mappings` 逐章对应。输入阻断时三份工件展示缺失计划、
当前节点、真实回答和恢复顺序，不得显示
通用文件装载器或空白占位。页面交互只用于查看、切换和展开已经记录的内容、提示与交互轨迹，
不接受新作答、不产生新事件，也不展示 Schema、模板或 Markdown/HTML 生成状态。HTML 是本阶段唯一可视化交付；
教学内容、正反例、提示与轨迹视图必须由内嵌规范 JSON 在页面内动态渲染。禁止调用 `imagegen`、
`image_gen` 或其他制图工具，禁止生成、引用或依赖独立的插图、知识点图片、静态图卡及
PNG/JPEG/WebP/SVG/GIF 等图片资产。用户提到“图片”或“可视化”时，默认实现为页面内的数据视图，
不得自动解释为制图任务。Markdown 失败写入 `document_artifact`，HTML 失败写入
`presentation_artifact`；不得篡改 G6 门禁，但任一失败时整次阶段交付不得报告为完成。只有内容正确可追溯、对目标和学习者适配、难度可学习、
提示不代替关键推理、无答案泄露且产生真实候选掌握证据时，才允许 `verdict=pass`、`route_to=S7`。
