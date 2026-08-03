---
name: al-s5-plan-learning-sessions
description: 从已证实的学习前沿选择最小连通子图并编排学习会话，并按“完整 Markdown 人审文档→无损结构化 learning_and_session_plan JSON→JSON 驱动的 S5 交互 HTML”交付三份工件，全程不生成独立图片。只要用户要进入个性化学习 S5、制定或修订学习路径与会话、调整时间投入或第一个会话契约，就使用本 skill。
---

# al-s5-学习路径规划

规划“下一步学什么以及为什么”。不要复制教材目录，不要把章节、视频或题量当成能力节点，也不要把证据不足的学习前沿当作已确定起点。

## 独立运行时的阶段、门与依赖

- `S5` 是本 Skill 的路径与会话规划阶段；`G5` 是 S5 计划质量门。直接依赖 `G1`（S1 目标契约门）、`G3`（S3 图谱门）和 `G4`（S4 学习前沿门）。
- `goal_success_contract` 的 G1 通过，表示目标、成功证据、范围和验收已确认；要求兼容 S1 信封完成、工件合法、G1 全量规通过、`verdict=pass`、`route_to=S2`。
- `capability_concept_graph` 的 G3 通过，表示节点/先修/测评/追溯可用；要求兼容 S3 信封完成、工件合法、G3 全量规通过、`verdict=pass`、`route_to=S4`。
- `learner_snapshot` 的 G4 通过，表示最近学习前沿有多项有效行为证据；要求兼容 S4 信封完成、工件合法、G4 全量规通过、`verdict=pass`、`route_to=S5`。
- `G5` 通过是指路径从已证实前沿连通到目标、遵守硬先修、节点选择有证据、会话与测评可执行、退出标准明确且用户强制确认完成，最终 `verdict=pass`、`route_to=S6`。
- 本 Skill 不依赖其他 Skill 目录，只依赖兼容的上游移交信封；裸工件或口头门声明不能证明上游通过。

## 开始前

1. 读取 [stage-contract.md](references/stage-contract.md)。
2. 读取 [markdown-output-contract.md](references/markdown-output-contract.md)，按 S5 专属章节先生成完整人审文档。
3. 读取 [handoff-envelope.schema.json](references/handoff-envelope.schema.json) 和 [learning-and-session-plan.schema.json](references/learning-and-session-plan.schema.json)。
4. 读取 [html-visualization-contract.md](references/html-visualization-contract.md)；必须使用 [stage-report.html](assets/stage-report.html) 生成已填充的 S5 专用页面。
5. 仅在需要理解输出形状时读取 [example.md](references/example.md)；案例数据是设计夹具，不是真实观察。

## 执行

1. 校验 `learner_snapshot`（G4）、`capability_concept_graph`（G3）与 `goal_success_contract`（G1）的版本、
   追溯关系与上游门状态；检查 S3 学习单元、单元—节点关联和先修图引用一致。记录缺失或过期输入，不把
   推断写成已确认事实。
2. 收集可用时间、节奏、资源、交付形式、动机与任务情境；识别计划中的依赖、风险与资源缺口。
3. 从已证实前沿到目标选择原子节点的最小连通子图；遵守硬先修，仅跳过有有效掌握证据的节点；学习单元
   只作可读分组，不从大纲父子关系或展示顺序推断学习顺序。关键前沿若仍为“证据不足”，不得当作固定起点。
4. 检查候选节点的知识状态、证据层级、时效和角色深度：默认核心路径优先 `core_stable` 与 `core_practice`；`research_frontier` 仅在目标要求时进入；仅有 `emerging_signal` 的内容进入观察/可选路线，不得冒充必修。
5. 按概念类型、错误类型、认知目标与真实任务匹配教学策略，编排讲解、worked example、练习、检索、交错、迁移与延迟复测；专家目标通过复杂度、自主性、影响范围和责任提升深度，不靠堆叠新术语。
6. 为每个节点记录纳入/排除理由、证据引用、时效和替代路线，再定义教学策略、支架与撤架条件；为每个会话定义目标、活动、预计时间与输入材料；为路径定义即时、迁移与延迟测评安排、复习锚点、风险与替代路线。
7. 为每个节点及整体路径定义可观察的通关标准。
8. 展示路径概览、阶段目标、时间投入、优先级与第一个会话契约，执行强制确认。
9. 生成 `learning_and_session_plan`，再按 G5 量规逐项评价。

## Fail closed

- 学习前沿证据不足或不稳时返回 S4；不要猜测起点。
- 图谱版本、学习单元—节点映射、节点粒度或先修关系不可靠时返回 S3；不要在 S5 改写 S3 结构。
- 核心节点只有社区/单一热点支持、动态证据已过期或知识状态未决时，返回 S2/S3；不要用“热门”替代“目标必需且有证据”。
- 目标发生变化时返回 S1，不在 S5 静默改写目标。
- 时间/资源不可行时留在 S5 缩减或调整，不静默删除目标门或测评。
- 强制确认未完成时保持 `pending`；不要进入 S6。

## 输出

每次运行必须依次交付：完整 S5 Markdown 计划审核报告、符合共同 Schema `1.3.0` 与正向工件 Schema
的无损结构化 JSON、由最终 JSON 填充的 S5 交互 HTML。Markdown 必须完整呈现输入前沿、用户约束、
路径取舍、节点理由、会话、支架/撤架、三类测评、复习、风险、退出标准、G5 与路由；JSON 不得删节为
课程表摘要，并须用 `document_artifact.section_mappings` 逐章对应。输入阻断时三份工件均展示缺失前沿、
恢复条件和返回路由，不得显示通用文件
装载器或空白占位。页面交互只用于查看、筛选和展开既有路线与会话，不接受计划确认输入，
也不展示 Schema、模板或 Markdown/HTML 生成状态。HTML 是本阶段唯一可视化交付；路线、会话和测评视图必须由
内嵌规范 JSON 在页面内动态渲染。禁止调用 `imagegen`、`image_gen` 或其他制图工具，禁止生成、引用
或依赖独立的插图、知识点图片、静态图卡及 PNG/JPEG/WebP/SVG/GIF 等图片资产。用户提到“图片”或
“可视化”时，默认实现为页面内的数据视图，不得自动解释为制图任务。Markdown 失败写入
`document_artifact`，HTML 失败写入 `presentation_artifact`；不得篡改 G5 门禁，但任一失败时整次阶段交付不得报告为完成。只有路径从已证实前沿连通到目标、无不可
解释冗余或硬先修跨越、首个会话可在约束内执行、教学与测评对齐且强制确认完成时，才允许
`verdict=pass`、`route_to=S6`。
