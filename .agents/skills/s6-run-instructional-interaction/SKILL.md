---
name: al-s6-run-instructional-interaction
description: 在统一项目级 LLM Wiki 中执行 S6 教学内容与真实交互。按照已确认计划开展分步教学、练习、提示、撤架、反馈和迁移，分离材料、原始交互、事件与候选证据。缺前置或无真实作答时保持 pending。
---

# S6 教学内容与真实交互

## 1. 权威输入

读取共享项目合同、独立调用合同、runtime contract、manifest/profile S6、S2 证据、S3 节点与测评、S4 快照、S5 已确认策略和当前 session。

## 2. 独立调用

- 无项目：route S1。
- G2/G3/G4/G5 缺失、计划未确认、版本失效或快照被模拟证据污染：blocked，route 最早缺失阶段。
- 前置通过但学习者尚未作答：`pending → S6`，直接展示当前活动，不代写。
- 只有讲义、模型示范或“懂了”不构成行为证据。

## 3. Session 事务

每个真实 session 创建：

```text
sessions/<session-id>/
  INDEX.md
  session-brief.md
  materials.md
  interaction.md
  events.jsonl
  evidence.jsonl
  reflection.md
```

原始学习者输入写入 interaction/conversation；提示、反馈、修订、撤架和适配写事件；候选证据引用具体子项和原文。

## 4. 教学执行顺序

按 S5 策略执行，但默认遵守：

1. 先做简短检索、预测或独立尝试；
2. 根据暴露的缺口给必要解释；
3. 使用正例、反例、边界案例或多重表征；
4. 提供 worked example 或部分完成支架；
5. 让学习者完成有支架练习；
6. 按预定条件逐步撤架；
7. 给未见独立任务；
8. 安排迁移或延迟复测。

不需要为了形式机械执行全部活动；必须说明跳过或切换策略的证据。

## 5. 提示与答案泄露

提示使用实际等级：

```text
none → light → medium → strong → worked_example
```

- 计划中的提示不算实际提示。
- 首次尝试前不得展示标准答案或等价完整结构。
- 反馈先指出错误位置、缺失条件或冲突证据，再决定是否升级提示。
- 学习者经过提示修订正确，只能形成带提示依赖的候选证据。
- 撤架后必须有新的独立尝试，不能把原题复述当作独立迁移。

## 6. 认知负荷

- 一次会话聚焦少量目标节点；
- 控制解释长度和同时出现的表格、术语、案例数量；
- 对复杂任务使用分段呈现和渐进披露；
- 将必要难度与无关写作、界面或信息筛选负担分开；
- 学习者明显超载时缩小任务，不把未完成直接判为知识缺口。

## 7. 证据记录

每项候选证据记录：

```text
node_id
item/sub-item
observable_indicator
learner_utterance
correctness
reasoning_quality
hint_dependency
independence
transfer
confidence
time/confounds
source_event_refs
```

只有真实用户交互使用 `learner_behavior`。系统构造答案、fixture 或 `simulations/**` 必须使用 `synthetic_learner_behavior` 或明确 fixture 元数据，并且不得进入真实 session、active learner model 或 project-state。

## 8. G6

G6 评价教学和记录质量，不评价最终掌握。至少检查：

1. 输入版本与节点对齐；
2. 内容来源和边界；
3. 学习者先尝试；
4. 解释、示例和活动匹配实际缺口；
5. 实际提示记录；
6. 答案泄露受控；
7. 撤架和独立任务实际发生或明确 pending；
8. 候选证据按子项追溯；
9. 模拟与真实行为隔离；
10. conversation、revision、session、索引和 verification 一致。

完成本轮教学、存在真实学习行为且候选证据可由 S7 消费时，才能 `G6=pass → S7`。若活动尚待学习者回答，保持 `pending → S6`。

## 9. Fail closed

- 缺计划或确认：route S5。
- 快照无效：route S4。
- 内容事实缺口：按最早污染点 route S2/S3。
- 无学习者输出、直接泄露答案、没有独立任务或使用模拟答案：G6 不通过。
- 不得在 S6 写 mastered；只能写 candidate evidence。

## 10. 用户回执

每个 turn 只给当前需要完成的活动和必要材料。会话结束后说明目标节点、真实尝试、使用的提示、撤架状态、候选证据、未解决问题、G6 与下一步验证任务。
