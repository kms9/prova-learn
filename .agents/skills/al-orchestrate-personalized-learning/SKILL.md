---
name: al-pls
description: 作为 Prova Learn 七阶段个性化学习流程的统一主控入口，理解用户的自然语言学习意图，定位项目状态，分发并执行对应的 `.agents/skills` S1–S7 Skill，核验落盘 Gate 与 route，并提示下一步行动。用户开始或改变学习目标、要求研究领域、构建能力图谱、诊断水平、制定计划、开始教学、验证掌握，或只说“继续”“下一步”“现在该做什么”且不想自己选择阶段时，使用本 Skill。
---

# 个性化学习主控

把本 Skill 当作 S1–S7 之上的薄控制面。只负责理解、选择、委托、核验和提示；不要创建 S0/G0，不要代替阶段业务，不要替阶段宣布 Gate 通过。

## 1. 每次开始前读取

按顺序完整读取：

1. `../../AGENTS.md`
2. `../../project-workspace-contract.md`
3. `../../standalone-invocation-contract.md`
4. `../../stage-runtime-contract.md`
5. `../../stage-delivery-manifest.json`
6. `../../stage-profiles.json`
7. [orchestration-contract.md](references/orchestration-contract.md)

manifest/profile 是阶段名称、路径、前置和允许路由的当前权威。参考文件与其冲突时，以 manifest/profile 为准。

## 2. 建立本次编排上下文

记录以下工作变量，不要先写入业务文件：

```text
request_kind = status | stage_work | continue | full_flow
execution_mode = read_only | single_stage | guided_flow
project = resolved | legacy | missing | ambiguous
requested_stage = S1..S7 | none
selected_stage = S1..S7 | none
expected_project_revision = integer | none
```

执行以下规则：

- 纯“查进度/下一步是什么”使用 `read_only`，不创建 conversation，不运行阶段。
- 默认使用 `single_stage`，一次只执行一个阶段。
- 只有用户明确要求“从头完成”“补齐前置”“按完整流程推进”时使用 `guided_flow`。
- 目标实质变化、新项目或新的成功证据定义优先选择 S1，即使项目当前处于后续阶段。

## 3. 定位项目

严格使用独立调用合同的解析顺序：用户显式路径 → 当前目录唯一项目 → 旧 run → 未找到。

- 若用户要新建或校准目标，允许选择 S1，由 S1 创建或更新项目。
- 若 S2–S7 的 `single_stage` 请求没有项目，仍执行该阶段的独立调用语义，保留 `project_missing → S1`，不要替它创建孤立工件。
- 若 `guided_flow` 没有项目，从 S1 开始。
- 若多个项目可能匹配且下一步会写入，先让用户选择；不要按修改时间猜测。
- 若存在旧 run，按合同先迁移并复核，不要继续写旧 run。

项目存在时读取根 `INDEX.md`、`PROJECT.md`、`project-state.json`、`last_conversation_id` 指向的会话和目标阶段入口；保存写前 `project_revision`。

## 4. 选择阶段

使用参考合同的优先级和语义表：

1. 先识别新项目或目标实质变化；命中即 S1。
2. 再识别用户显式指定的 S1–S7。
3. `continue` 从已核验的 `project-state.json.route_to` 选择，不按对话印象猜测。
4. 其他阶段工作按事实所有者映射为研究 S2、结构 S3、诊断 S4、规划 S5、教学 S6、验证/重规划 S7。
5. 同时命中多个阶段时选择最早事实所有者；若不同选择会产生实质不同写入且无法从项目证据消歧，先请求一个最小澄清。

`route_to=complete` 时不要调用阶段；展示完成证据和复习/新目标选项。

## 5. 委托阶段

选择阶段后：

1. 从 manifest 取得 `skill_name` 与 `skill_dir`。
2. 完整读取目标 `SKILL.md` 及其明确要求的共享合同和阶段 references。
3. 把用户原始意图、已解析项目路径、`expected_project_revision`、执行模式和前置检查结果交给目标阶段。
4. 严格按目标 Skill 执行业务与写入事务，如同用户直接调用它。
5. 不在主控中重写阶段工件，不用聊天摘要填补目标 Skill 未执行的步骤。

只有实际读取并执行了目标 Skill，才能说“已调用/已执行该阶段”。只完成选择但没有执行业务时，报告 `selected_not_executed`。

### single_stage

执行选定阶段一次。前置失败时保留阶段的 blocked/project_missing 结果和最早恢复路由，不静默补跑上游。

### guided_flow

若目标阶段的前置缺失或失效，从最早缺失阶段开始。每执行一个阶段，都先完成第 6 节复核；只有阶段 `completed`、Gate 通过、verification 通过且 `route_to` 允许继续时，才考虑下一阶段。

## 6. 复核落盘事实

阶段执行后重新读取，不使用写前缓存：

- 项目根 `INDEX.md` 与 `project-state.json`；
- 目标阶段 `INDEX.md`、`gate.md`、`verification.md`；
- `last_conversation_id` 对应的 conversation；
- manifest 要求的阶段入口与必需文件。

至少核对：

```text
project_revision 是否符合本次事务
conversation 是否存在且与本次请求关联
stage state = completed | pending | blocked
Gate verdict/status 与 route_to 是否一致
verification 是否通过
project-state、根 INDEX、阶段 INDEX 与 timeline 是否同步
```

无法核验时如实报告 `not_executed`、`pending`、`blocked`、`version_conflict` 或 `evidence_gap`。不要把子 Skill 自述、文件存在或裸 `route_to` 当成完成证明。

## 7. 决定是否继续

默认在一个阶段后停止。仅 `guided_flow` 可继续，并且遇到下列任一条件必须停：

- mandatory 或升级后的确认尚未完成；
- 等待真实学习者回答、练习、迁移或延迟保持；
- 需要用户在有实质后果的方案间选择；
- `pending`、`blocked`、`research_blocked`、`version_conflict` 或验证缺口；
- `route_to` 回到当前阶段或任何上游阶段；
- S7 未到 `complete`；
- 下一阶段无法由已落盘证据证明前置通过。

没有新用户输入或新证据时，不要在同一次调用中重复执行同一阶段。

## 8. 给用户下一步回执

每次结论先行，包含：

```markdown
当前结果：<已完成 / 待确认 / 待作答 / 被阻断 / 仅查询>
项目：<路径与 revision，未知则说明>
理解的意图：<一句话>
本次路由：<未调用 | Sx -> $skill-name>
依据：<项目 route / 显式请求 / 语义所有者 / 最早缺失前置>
阶段与 Gate：<state、Gx、route_to>
证据入口：<可点击或可定位的 INDEX/conversation/gate/verification>
停止原因：<为何现在不继续>
需要你提供：<具体确认、回答、材料或“无”>
下一步：<一条可立即执行的动作>
```

下一步始终继续指向 `$al-orchestrate-personalized-learning`，不要要求用户改为记忆或直接调用子 Skill。若需要回答问题，直接展示问题或活动；不得只说“请补充信息”。

## 9. 不可越过的边界

- 不把主控选择当成阶段调用成功。
- 不把模型知识当成 S1/S2 真实联网证据。
- 不替用户确认 S1/S5，不模拟 S4/S6 学习者回答。
- 不因 S7 工件通过就声称学习目标已达成；只有 `GOAL_ACHIEVED` 且最终验收与保持通过才 `complete`。
- 不在 revision 冲突时覆盖项目。
- 不调用图像生成工具，不创建独立图片或 HTML 业务交付。
- 不把 Skill 软编排描述成严格跨进程状态机；严格重试、并发锁和外部持久化需要独立 runtime/harness。
