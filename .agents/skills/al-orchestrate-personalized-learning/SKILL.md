---
name: al-pls
description: 作为 Prova Learn 七阶段个性化学习流程的统一主控入口，理解自然语言学习意图，定位项目状态，选择并执行 S1–S7，复核 Gate、route、conversation、revision 和真实学习证据。用户开始或改变目标、继续项目、要求诊断、规划、教学、掌握验证或完整流程时使用。
---

# 个性化学习主控

本 Skill 是 S1–S7 之上的薄控制面，只负责理解、选择、委托、复核和向用户交付下一动作。它不是 S0/G0，不拥有阶段业务工件，也不得替阶段宣布通过。

## 1. 权威输入

每次按顺序读取：

1. `../../AGENTS.md`
2. `../../project-workspace-contract.md`
3. `../../standalone-invocation-contract.md`
4. `../../stage-runtime-contract.md`
5. `../../stage-delivery-manifest.json`
6. `../../stage-profiles.json`
7. `references/orchestration-contract.md`
8. 项目根、当前阶段入口和最近 conversation

manifest/profile 与阶段 `SKILL.md` 共同构成当前合同；任一处要求更严格时采用更严格规则。

## 2. 编排上下文

```text
request_kind = status | stage_work | continue | full_flow
execution_mode = read_only | single_stage | guided_flow
project = resolved | legacy | missing | ambiguous
requested_stage = S1..S7 | none
selected_stage = S1..S7 | none
expected_project_revision = integer | none
real_learner_input = present | absent
```

- 查询状态使用 `read_only`，不制造 conversation 或阶段工件。
- 默认 `single_stage`，一次只执行一个阶段。
- 只有用户明确要求从头完成、补齐前置或完整推进时使用 `guided_flow`。
- 新目标、目标实质变化或成功证据变化优先回 S1。

## 3. 项目定位与版本

解析顺序：用户显式项目路径 → 当前目录唯一项目 → 旧 run → 未找到。

- 只有 S1 可创建项目。
- S2–S7 无项目时保留 `project_missing → S1`，不得创建孤立阶段。
- 多项目且写入目标不唯一时，先做最小选择，不按修改时间猜。
- 旧 run 先迁移，随后重新读取项目状态。
- 写入前保存 `expected_project_revision`；写后必须重新读取，冲突时报告 `version_conflict`。

## 4. 阶段选择

优先级：

1. 新目标或目标实质变化 → S1；
2. 用户显式指定阶段；
3. “继续/下一步”使用已核验 `project-state.json.route_to`；
4. 研究事实归 S2，结构归 S3，诊断归 S4，路径归 S5，教学归 S6，掌握与重规划归 S7；
5. 多阶段冲突时选择最早事实所有者。

`route_to=complete` 时不再调用阶段，只展示最终证据、保持状态和可选的新目标。

## 5. 确认语义

不得把普通的“继续”“下一步”“跑完流程”自动解释为对多个高影响默认值的确认。

只有同时满足以下条件，才能把简短回复解释为接受默认方案：

1. 上一轮向用户展示了一个明确的“接受全部默认值”选项；
2. 已逐项列出将被确认的字段；
3. 本轮原话与该选项直接相邻且无歧义；
4. conversation 和 `confirmation.md` 记录 `confirmed_fields`、`unconfirmed_fields` 与用户原话；
5. 用户可见回执再次列出实际确认的字段。

否则保持 `pending`，只询问产生实质差异的最少问题。不得重复询问用户已经明确提供的信息。

## 6. 委托阶段

1. 从 manifest 读取目标阶段的 `skill_name`、目录和前置。
2. 完整读取目标 `SKILL.md` 及其 references。
3. 传递用户原始意图、项目路径、revision、执行模式和前置结果。
4. 严格按目标 Skill 执行业务事务。
5. 主控不得用聊天摘要补造阶段遗漏的研究、回答、确认或学习行为。

只有真正执行了阶段业务，才能报告“已执行”；只选择阶段时报告 `selected_not_executed`。

## 7. 真实学习证据边界

- S4、S6、S7 只接受真实学习者原话和实际交互作为真实 `learner_behavior`。
- `simulations/**`、fixture、系统构造答案必须标记 `synthetic_learner_behavior` 或明确的 fixture 元数据，且不得进入真实项目的 learner snapshot、mastery event、active model 或 `project-state.json`。
- 不得把“未作答”编译为“未掌握”。
- 不得把单个复合题覆盖多个节点，直接推导多个 `tested_mastered`。
- 关键节点达到 `tested_mastered`，必须满足阶段预设的多证据规则：至少两项相互独立的观察，或一项完整表现任务再加一项无提示迁移/延迟复测。否则使用 `candidate_mastery`、`partial`、`unknown` 或 `insufficient_evidence`。

## 8. guided flow 停止条件

每个阶段执行后必须复核，再决定是否继续。遇到以下任一条件立即停止：

- mandatory 或升级确认未完成；
- 等待真实学习者回答、练习、迁移或延迟保持；
- 需要用户在有实质后果的方案间选择；
- `pending`、`blocked`、`research_blocked`、`version_conflict`、`evidence_gap`；
- route 回到当前或上游阶段；
- 下一阶段前置不能由落盘事实证明；
- S7 尚未达到 `complete`。

没有新输入或新证据时，不得在同一次调用里重复跑同一阶段。

## 9. 落盘复核

阶段执行后重新读取：

- 根 `INDEX.md`、`project-state.json`、timeline；
- 阶段 `INDEX.md`、`gate.md`、`verification.md`；
- `last_conversation_id` 对应 conversation；
- manifest 必需文件；
- 学习阶段还要检查 observation/session/mastery 与真实来源边界。

至少核对：

```text
revision 事务一致
conversation 与本次请求关联
stage state / gate / route 一致
verification 通过
根索引、阶段索引、timeline 同步
真实与模拟证据未混用
掌握结论满足最小证据数和独立性
```

无法核验时如实报告 `not_executed`、`pending`、`blocked`、`version_conflict` 或 `evidence_gap`。

## 10. 用户回执

```markdown
当前结果：<已完成 / 待确认 / 待作答 / 被阻断 / 仅查询>
项目：<路径与 revision>
理解的意图：<一句话>
本次路由：<未调用 | Sx -> $skill-name>
依据：<route / 显式请求 / 事实所有者 / 最早缺失前置>
阶段与 Gate：<state、Gx、route_to>
证据入口：<INDEX / conversation / gate / verification>
停止原因：<为何不能继续>
需要你提供：<具体问题、作答或“无”>
下一步：<一条可立即执行动作>
```

下一步继续指向 `$al-pls`；需要回答时直接展示题目或活动，不只说“请补充信息”。

## 11. 不可越过的边界

- 不把阶段选择当成执行完成。
- 不把模型知识当 S1/S2 联网证据。
- 不替用户确认 S1/S5。
- 不模拟 S4/S6 的学习者回答。
- 不把 G6 或 G7 工件质量等同掌握。
- 只有最终验收、迁移与要求的保持证据均通过，才允许 `GOAL_ACHIEVED` 和 `complete`。
- 不在 revision 或 learner model version 冲突时覆盖。
- 不把软编排描述为具备外部 runtime 才能提供的强锁、严格重试或后台执行能力。
