---
name: plan-learning-sessions
description: 从已证实的学习前沿到目标能力选择最小连通子图，并把它编排为有通关标准、测评与复习锚点的学习会话，形成经用户强制确认的 learning_and_session_plan；可用 S3 学习单元作可读分组，但始终按原子节点与先修边排序。只要用户要进入个性化学习 S5、制定或修订学习路径与会话、调整时间投入或第一个会话契约，就使用本 skill。
---

# 路径与会话规划（S5）

规划“下一步学什么以及为什么”。不要复制教材目录，不要把章节、视频或题量当成能力节点，也不要把证据不足的学习前沿当作已确定起点。

## 开始前

1. 读取 [stage-contract.md](references/stage-contract.md)。
2. 读取 [handoff-envelope.schema.json](references/handoff-envelope.schema.json) 和 [learning-and-session-plan.schema.json](references/learning-and-session-plan.schema.json)。
3. 仅在需要理解输出形状时读取 [example.md](references/example.md)；案例数据是设计夹具，不是真实观察。

## 执行

1. 校验 `learner_snapshot`（G4）、`capability_concept_graph`（G3）与 `goal_success_contract`（G1）的版本、
   追溯关系与上游门状态；检查 S3 学习单元、单元—节点关联和先修图引用一致。记录缺失或过期输入，不把
   推断写成已确认事实。
2. 收集可用时间、节奏、资源、交付形式、动机与任务情境；识别计划中的依赖、风险与资源缺口。
3. 从已证实前沿到目标选择原子节点的最小连通子图；遵守硬先修，仅跳过有有效掌握证据的节点；学习单元
   只作可读分组，不从大纲父子关系或展示顺序推断学习顺序。关键前沿若仍为“证据不足”，不得当作固定起点。
4. 按概念类型、错误类型与认知目标匹配教学策略，编排讲解、worked example、练习、检索、交错、迁移与延迟复测。
5. 为每个节点定义教学策略、支架与撤架条件；为每个会话定义目标、活动、预计时间与输入材料；为路径定义即时、迁移与延迟测评安排、复习锚点、风险与替代路线。
6. 为每个节点及整体路径定义可观察的通关标准。
7. 展示路径概览、阶段目标、时间投入、优先级与第一个会话契约，执行强制确认。
8. 生成 `learning_and_session_plan`，再按 G5 量规逐项评价。

## Fail closed

- 学习前沿证据不足或不稳时返回 S4；不要猜测起点。
- 图谱版本、学习单元—节点映射、节点粒度或先修关系不可靠时返回 S3；不要在 S5 改写 S3 结构。
- 目标发生变化时返回 S1，不在 S5 静默改写目标。
- 时间/资源不可行时留在 S5 缩减或调整，不静默删除目标门或测评。
- 强制确认未完成时保持 `pending`；不要进入 S6。

## 输出

只输出符合两个 Schema 的 JSON 移交信封。先生成具名正向工件，再生成 `quality_evaluation`。只有路径从已证实前沿连通到目标、无不可解释冗余或硬先修跨越、首个会话可在约束内执行、教学与测评对齐且强制确认完成时，才允许 `verdict=pass`、`route_to=S6`。
