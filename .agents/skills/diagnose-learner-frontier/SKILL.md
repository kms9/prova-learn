---
name: diagnose-learner-frontier
description: 用对齐目标与先修链的多项行为证据诊断学习者节点状态、误概念、提示依赖、迁移表现和置信度校准，产出版本化 learner_snapshot 与最近学习前沿。只要用户要进入个性化学习 S4、确定从哪里开始学、复测争议节点、修正既有诊断或排查“会做但讲不清”，就使用本 skill。
---

# 学习者诊断与学习前沿（S4）

从观察推断能力，不从自评、年限、偏好问卷或单题正确直接推断掌握。

## 开始前

1. 读取 [stage-contract.md](references/stage-contract.md)。
2. 读取 [handoff-envelope.schema.json](references/handoff-envelope.schema.json) 和 [learner-snapshot.schema.json](references/learner-snapshot.schema.json)。
3. 仅在需要理解输出形状时读取 [example.md](references/example.md)；案例数据是设计夹具，不是真实观察。
4. 确认上游 G1、G3 已通过，关键节点具有可执行诊断项；既有学习记录须带身份、时间、来源和有效期，过期证据只作线索。

## 执行

1. 先声明要推断的节点/能力以及每类证据的判定规则，再选择诊断任务。
2. 沿目标与先修链组合解释、预测、反例、诊断、比较、迁移和置信度任务；包含无错题与隐蔽错题，避免只测口号识别。
3. 收集真实学习者回答；记录正确性、推理过程、提示层级、耗时（可得时）、置信度和错误类型。
4. 关键结论须由多项对齐观察支持；显式区分“答对”“独立会做”“能迁移”与“证据不足”。
   - `tested_mastered` 必须有同一节点在 `hint_dependency.level=none|low` 下的独立证据；只有 `medium|high|unknown` 提示记录时，最多标为 `tested_not_mastered` 或 `insufficient_evidence`，并安排撤除支架后的复测。
5. 学习者对结论有异议时，对争议节点追加测试；自述只用于选题，不得覆盖行为证据。
6. 递归定位最近可学习节点；生成版本化 `learner_snapshot`，再按 G4 量规逐项评价。

## Fail closed

- 无真实学习者回答时，只产出诊断任务并保持 `pending`；不模拟回答、不伪造前沿。
- 冷启动返回 `unknown`/`insufficient_evidence`，路由到 S4 建立初始证据；不得创建“全部未掌握”画像。
- 单题、纯自评或仅口号识别不得决定关键节点状态。
- 诊断题无法产生目标证据时返回 S3；图谱或来源缺失时返回 S2/S3。
- S4+S5 仅在确认零基础、图谱起点明确、路径近线性且任务低风险时才可合并；存在先验未知、证据冲突、多前沿或高风险决策时禁止合并。

## 输出

只输出符合两个 Schema 的 JSON 移交信封。先生成具名正向工件 `learner_snapshot`，再生成 `quality_evaluation`。只有学习前沿有多项、可追溯且在有效期内的行为证据，关键结论区分了识别/独立/迁移，且 G4 全维度通过时，才允许 `verdict=pass`、`route_to=S5`。
