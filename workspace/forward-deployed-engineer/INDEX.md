# 前线部署工程师课程学习

> 项目：`PRJ-forward-deployed-engineer`
> 状态：`active`
> 当前阶段：`S4`
> G1：`pass`
> G2：`pass`
> G3：`pass`
> G4：`blocked — waiting for learner behavior`
> 当前路由：`S4`
> 项目版本：`6`
> 最近更新：`2026-08-04T12:24:00Z`

## 当前结论

S1–S3 已通过。S4 冷启动诊断的 D1–D4、事前规则和 pending 三工件已经生成并验证，覆盖 12/12 节点。当前没有真实学习者作答，因此 positive learner snapshot 为空、G4 blocked、route 保持 S4；这只表示证据尚未采集，不表示用户未掌握。

## 当前入口

- [项目说明](PROJECT.md)
- [项目状态](project-state.json)
- [时间线](timeline.md)
- [S1 目标校准](stages/s1-goal-contract/INDEX.md)
- [S2 领域取证](stages/s2-domain-evidence/INDEX.md)
- [S2 逐题回答](stages/s2-domain-evidence/research-answers.md)
- [S2 研究会话](conversations/2026-08/CONV-20260804T114235Z-s2-research/INDEX.md)
- [S3 能力—概念图](stages/s3-capability-graph/INDEX.md)
- [S3 审核报告](stages/s3-capability-graph/RUN-20260804T120500Z-S3-review.md)
- [S3 交互视图](stages/s3-capability-graph/capability-graph.html)
- [S3 建图会话](conversations/2026-08/CONV-20260804T120500Z-s3-graph/INDEX.md)
- [S4 诊断入口](stages/s4-learner-diagnosis/INDEX.md)
- [D1–D4 诊断计划](stages/s4-learner-diagnosis/diagnostic-plan.md)
- [S4 只读诊断视图](stages/s4-learner-diagnosis/learner-snapshot.html)
- [当前 S4 会话](conversations/2026-08/CONV-20260804T122400Z-s4-diagnostic/INDEX.md)
- [本次 S1 会话](conversations/2026-08/CONV-20260804T111952Z-s1-scope/INDEX.md)
- [S1 确认会话](conversations/2026-08/CONV-20260804T113555Z-s1-confirm/INDEX.md)
- [初始化会话](conversations/2026-08/CONV-20260804T111911Z-c3ff1011/INDEX.md)

## 当前已确认目标

在一个未见企业 AI 场景中，独立完成一份可审查的 FDE 部署简报：识别高价值问题，定义可衡量结果，设计最小可行部署与生产风险控制，规划激活、续约、扩收和产品回流，并能说明何时不应采用 FDE 模式。

## 已确认默认约束

- 用途：工作应用深度；
- 练习：课程外模拟企业 AI 案例，不使用敏感真实客户资料；
- 节奏：每周 3 次、每次 45 分钟；无硬截止日期；
- 起点：技术与交付基础未知，由 S4 真实诊断确定；
- 验收：部署简报、答辩与跨场景迁移。

## 下一动作

用户按 [作答格式](stages/s4-learner-diagnosis/diagnostic-plan.md#作答格式) 回复 D1–D4；之后仍由 `$al-pls` 主控继续记录观察、重评 G4 并在通过后进入 S5。
