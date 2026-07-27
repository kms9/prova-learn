---
name: run-instructional-interaction
description: 为已确认路径上的当前学习节点生产可追溯、分层、含正反例与渐隐支架的教学内容，并通过真实交互记录学习者回答、提示与修正，形成 session_package_and_trace。只要用户要进入个性化学习 S6、开展一个学习会话、调整教学形式或修复内容质量，就使用本 skill。
---

# 内容生产与教学交互（S6）

本阶段的完成条件是产生可解释的学习者行为证据，不是教师输出结束。G6 只评价教学工件质量，绝不宣布学习者掌握。

## 开始前

1. 读取 [stage-contract.md](references/stage-contract.md)。
2. 读取 [handoff-envelope.schema.json](references/handoff-envelope.schema.json) 和 [session-package-and-trace.schema.json](references/session-package-and-trace.schema.json)。
3. 仅在需要理解输出形状时读取 [example.md](references/example.md)；案例数据是设计夹具，不是真实观察。
4. 校验当前节点属于已确认计划、硬先修通过、来源可追溯、学习者快照有效且目标与节点通关标准一致。

## 执行

1. 会话开始时执行 `inform` 确认：告知目标、约束、媒介与“过程记录用于更新学习者模型”。
2. 检查本会话目标、可用媒介、学习者当前状态、材料与例子缺口；确定本轮需要解释、示范、练习还是迁移。
3. 从已审计证据选择内容；标明来源与适用边界，模型常识不得包装为审计事实。
4. 组合分层解释、多表征、正反例、边界案例与常见误解；让抽象与具体互相连接。
5. 设计渐进练习（检索前测 → worked example → 半完成 → 对比 → 独立迁移）；难度处于当前可学习范围。
6. 先让学习者产出，再给反馈；建立逐级提示并按回答逐步撤架；提示指向形状或规则，不代替关键推理。
7. 防止答案泄露：独立任务提交前不公布答案。
8. 完整记录交互轨迹：每次回答、提示层级、修正轨迹、未解决问题与内容变化。
9. 生成 `session_package_and_trace`，再按 G6 量规逐项评价。

## Fail closed

- 关键内容无可追溯来源时返回 S2/S3 或 `blocked`，不把模型常识包装成审计事实。
- 学习者尚未作答时保持 `pending`，不要代写 `learner_behavior` 证据。
- 答案泄露或无独立作答时留在 S6 重生成；禁止进入 S7 宣称掌握。
- 内容正确但连续卡住时返回 S5 调策略，必要时返回 S4 重诊断。
- G6 只评价教学工件质量，绝不能宣布学习者掌握。

## 输出

只输出符合两个 Schema 的 JSON 移交信封。先生成具名正向工件，再生成 `quality_evaluation`。只有内容正确可追溯、对目标和学习者适配、难度可学习、提示不代替关键推理、无答案泄露且产生真实候选掌握证据时，才允许 `verdict=pass`、`route_to=S7`。
