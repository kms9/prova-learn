---
name: al-07-verify-mastery-and-replan
description: 用预先确定的掌握规则综合节点级掌握证据，以版本检查更新学习者模型并决定路由，并按“完整 Markdown 人审文档→无损结构化 mastery_and_replanning_bundle JSON→JSON 驱动的 S7 交互 HTML”交付三份工件，全程不生成独立图片。只要用户要进入个性化学习 S7、判断是否学会、更新学习者状态、安排复测或重规划路径，就使用本 skill。
---

# 掌握验证、模型更新与重规划（S7）

S7 是一个完整的反馈事务：验证结果必须被原子地写入学习者模型并产生下一动作。把“本次答对”与长期掌握分开；不要把一次选择题的正确率、单题分数或完成度当成能力。

本 skill 保持一个顶层阶段，但严格按顺序执行两个内部子流程：先 `mastery_verification`，后 `learner_model_update_and_replan`。两者在一次事务内闭环，更新引用验证产生的证据。

## 独立运行时的阶段、门与依赖

- `S7` 是本 Skill 的掌握验证与重规划阶段；`G7` 是 S7 事务质量门，不等同于“学习者已掌握”。
- 直接依赖包括：通过 G6 的 `session_package_and_trace`、通过 G4 且可加载的历史 `learner_snapshot`、通过 G5 的当前计划，以及通过 G3 的当前图谱。G3/G4/G5/G6 分别是 S3 图谱、S4 诊断、S5 计划和 S6 教学交互质量门。
- 每个“已通过”必须由对应 S3–S6 兼容信封证明：阶段完成、输入校验通过、具名工件合法、该门全部量规通过、`quality_evaluation.verdict=pass`，并路由到下一阶段；只有文件或调用者声明不算门证据。历史快照还必须具有可用 `learner_id` 和 `model_version>=1`。
- `G7` 评价多维证据、预设掌握规则、版本事务、归因和路由是否正确。学习者未掌握时，S7 工件仍可能质量合格并正确返回上游；因此不得把“G7 工件质量合格”简写成“目标已完成”。只有 `GOAL_ACHIEVED` 且最终验收与保持要求都通过时才能 `route_to=complete`。
- 本 Skill 不要求上游 Skill 目录共同安装；缺少兼容门证据时 fail closed，返回相应阶段，不创建版本 0 或“全部未掌握”画像。

## 开始前

1. 读取 [stage-contract.md](references/stage-contract.md)。
2. 读取 [markdown-output-contract.md](references/markdown-output-contract.md)，按 S7 专属章节先生成完整人审文档。
3. 读取 [handoff-envelope.schema.json](references/handoff-envelope.schema.json) 和 [mastery-and-replanning-bundle.schema.json](references/mastery-and-replanning-bundle.schema.json)。
4. 读取 [html-visualization-contract.md](references/html-visualization-contract.md)；必须使用 [stage-report.html](assets/stage-report.html) 生成已填充的 S7 专用页面。
5. 仅在需要理解输出形状时读取 [example.md](references/example.md)；案例数据是设计夹具，不是真实观察。
6. 校验上游：`session_package_and_trace` 已通过 G6、会话记录完整、节点掌握规则在测评前已确定、历史学习者模型版本可用，且内容质量问题没有被误读为学习者能力问题。

## 执行

### 子流程一：掌握验证（mastery_verification）

1. 对每个待判节点，分别采集并记录多维证据：正确性、推理质量、提示依赖、迁移（近/远）、置信度校准和必要的延迟保持。
   提示依赖必须来自真实行为事件：S4 `none/low/medium/high` 归一为 S7 `none/low/moderate/high`，
   S6 实际 `light/medium/strong` 归一为 `low/moderate/high`；无提示为 `none`，无可用记录才为 `not_executed`。
2. 区分内容质量问题（S6）、教学策略/顺序问题（S5）、诊断假设冲突（S4）、图谱结构错误（S3）、来源错误/过期/覆盖缺口（S2）与目标变更（S1），不要混作“学习者不会”。
3. 按预设规则给出每个节点的掌握判定（`mastered`/`partial`/`not_mastered`）；证据不足以满足规则时记为 `partial` 或 `not_mastered`，归因为 `EVIDENCE_INSUFFICIENT`。
4. 单题识别正确不得越级写成高掌握概率；多维证据任一关键维度缺失即不得标为已掌握。

### 子流程二：学习者模型更新与重规划（learner_model_update_and_replan）

5. 读取历史模型版本；执行基于版本的原子更新——仅当 `expected_model_version` 与当前版本匹配时才应用补丁，并保留每个受影响节点的变更前值、变更后值、证据事件 ID 和理由。
6. 版本冲突时：`update_status=version_conflict`，**不应用任何补丁**，输出重新加载指令；不得静默覆盖较新状态。
7. 无真实后端或证据被判定为不足以更新时：`update_status=not_executed`，不得声称持久化成功。
8. 按确定性归因表选择下一动作（`continue`/`remediate`/`skip`/`rediagnose`/`complete`）与 `route_to`；多归因按“目标 → 来源 → 图谱 → 诊断 → 路径 → 内容 → 证据”的上游优先级选择最早污染源。把新暴露的来源错误、过期事实、缺失失败条件、Benchmark 偏差或新兴信号误用记录为证据反馈，列出受影响 claim/node 和复核查询，路由 S2 局部更新。
9. 产出调整后的路径、下一会话契约，以及检索、间隔、交错与延迟复测安排。
10. 重大路径变更触发条件确认；收集学习者反思并说明掌握结论、证据、仍存缺口与调整理由。

## Fail closed

- 无独立应用、迁移或必要延迟证据时，不得标为 `mastered`；保持 `partial`/`not_mastered` 并安排补测或延迟复测。
- 版本冲突或无真实后端时，按 `version_conflict` 或 `not_executed` 诚实标注，不伪造写入成功。
- 学习者未掌握不等于 S7 工件失败：当多维证据齐全、归因与路由正确且更新前后一致时，S7 工件质量可通过，路由仍可指向上游补救。
- 目标发生实质变化时返回 S1，不在 S7 内静默改写目标或验收标准。
- 来源反馈不得直接在 S7 改写领域事实或图谱；先回 S2 补证，再由 S3 重新计算受影响节点并显式失效下游工件。

## 输出

每次运行必须依次交付：完整 S7 Markdown 掌握与重规划审核报告、符合共同 Schema `1.3.0` 与正向工件
Schema 的无损结构化 JSON、由最终 JSON 填充的 S7 交互 HTML。Markdown 必须完整呈现输入/版本事务、
预设规则、六维证据、节点判断、归因、证据追加、before/after 补丁、持久化事实、路由、复测、来源反馈、
限制与 G7；JSON 不得删节为单分数或最终结论，并须用 `document_artifact.section_mappings` 逐章对应。
`positive_artifact` 必须是同时包含
`mastery_verification` 与 `learner_model_update_and_replan` 两个有序段的
`mastery_and_replanning_bundle`，且后者的每项关键变更都能追溯到前者采集的证据事件。每次运行都必须
按 HTML 派生契约另写出已填充的 S7 多维掌握证据、模型变更、归因、路由、复测与适用限制专用页面；
输入阻断时展示缺失证据、版本事务条件和恢复顺序，不得显示通用文件装载器或空白占位。页面交互只用于
筛选、对照和展开既有掌握证据与重规划结果，不执行模型更新，也不展示 Schema、模板或 Markdown/HTML 生成状态。
HTML 是本阶段唯一可视化交付；掌握证据、模型差异、路由与复测视图必须由内嵌规范 JSON 在页面内动态
渲染。禁止调用 `imagegen`、`image_gen` 或其他制图工具，禁止生成、引用或依赖独立的插图、知识点图片、
静态图卡及 PNG/JPEG/WebP/SVG/GIF 等图片资产。用户提到“图片”或“可视化”时，默认实现为页面内的
数据视图，不得自动解释为制图任务。
Markdown 失败写入 `document_artifact`，HTML 失败写入 `presentation_artifact`；不得篡改
掌握判定、持久化事实或路由，但任一失败时整次阶段交付不得报告为完成。再生成 `quality_evaluation`：只有当
多维证据充分、掌握规则一致、提示影响受控、更新可追溯、调整可解释且未对单次结果过度反应时，才允许
工件通过；`route_to` 严格遵循归因路由表。
