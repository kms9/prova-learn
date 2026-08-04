---
name: al-s1-create-goal-success-contract
description: 在项目级 LLM Wiki 中创建或更新 S1 目标校准。它把模糊学习诉求、真实外部预检、可观察能力、验收方式和用户强制确认写入 workspace/<project-slug>/ 的项目根、conversation 与 stages/s1-goal-contract/，并以项目 revision、事件日志和 G1 路由形成可追溯事务。只要用户开始新学习项目、改变目标、定义“学会”的证据或修正领域/岗位边界，就使用本 Skill。
metadata:
  author: kms9
---

# S1 项目级目标校准

S1 负责把“想学什么”编译为一个可观察、可验收、经过外部现实校准并由用户确认的目标契约。**项目工作区是交付边界**；单个 JSON、旧 run folder 或聊天结论都不是当前项目的唯一真相。

## 1. 开始前必须读取

按顺序读取：

1. `../../project-workspace-contract.md`
2. `../../stage-delivery-manifest.json`
3. [project-stage-contract.md](references/project-stage-contract.md)
4. [stage-contract.md](references/stage-contract.md)
5. 当前项目的 `INDEX.md`、`PROJECT.md` 和 `project-state.json`（若已存在）
6. 当前或新建 conversation
7. `stages/s1-goal-contract/INDEX.md`

[run-folder-contract.md](references/run-folder-contract.md) 仅用于读取或迁移旧 `runs/<run-id>/`，不得作为新 S1 写入合同。

## 2. 项目定位

### 2.1 冷启动

若当前学习目标尚无项目：

1. 从用户明确表达的目标生成稳定 `project-slug`；slug 是技术标识，不是已确认领域结论。
2. 使用 `scripts/init_project_workspace.py` 创建 `workspace/<project-slug>/`。
3. 在初始化会话之后，为本次真实 S1 交互创建新的 conversation。
4. 不得因为项目目录已创建，就把 S1 标为完成或 G1 标为通过。

### 2.2 已有项目

若项目已存在：

1. 读取 `project-state.json.project_revision`，作为 `expected_project_revision`。
2. 校验当前 `active_goal_id`、目标版本、当前阶段和路由。
3. 用户只是补充约束、来源、确认或验收方式时，在同一项目更新 S1。
4. 用户实质改变目标时，创建新的 `GOAL-*` 版本并记录 `supersedes`；只有边界完全不同且用户明确要求时才新建项目。

### 2.3 旧 run

若只发现 `workspace/<project-slug>/runs/<run-id>/`：

1. 不得继续写旧 run。
2. 使用 `scripts/migrate_legacy_run.py` 迁移为项目 Wiki。
3. 迁移完成后重新读取项目状态，再执行本次 S1 事务。

## 3. 每次交互事务

每次用户补充、纠正或确认目标，都必须执行完整事务：

```text
读取 project-state 与根 INDEX
→ 校验 expected_project_revision
→ 创建 conversation
→ 追加用户原文、Agent 回应与工具结果摘要
→ 追加 project events
→ 更新 S1 当前 Wiki 与 JSONL
→ 独立执行 G1 和 verification
→ project_revision + 1
→ 更新 project-state、根 INDEX 与 timeline
```

版本已变化时停止写入，记录 `version_conflict`，不得最后写入者覆盖。

conversation 固定包含：

```text
conversations/YYYY-MM/<conversation-id>/
  INDEX.md
  transcript.md
  events.jsonl
  summary.md
```

原始用户回答写 `transcript.md`；结构化变化写 `events.jsonl`。不得只记录最终总结。

## 4. S1 项目阶段目录

当前 S1 只写：

```text
workspace/<project-slug>/stages/s1-goal-contract/
  INDEX.md
  working-notes.md
  records.jsonl
  decisions.md
  gate.md
  verification.md
  history/
  goal-contract.md
  research-brief.md
  sources.jsonl
  evidence-table.md
  coverage.md
  capabilities.jsonl
  terminology.jsonl
  confirmation.md
```

文件职责与字段见 [project-stage-contract.md](references/project-stage-contract.md)。

### 真相边界

- Markdown Wiki：当前被接受的目标、边界、证据解释和确认。
- JSONL：来源、能力、术语及阶段原子记录的不可变历史。
- `project-state.json`：当前版本、阶段、路由和指针。
- 兼容 JSON 导出：可选，不得替代上述三层。

## 5. S1 状态机

```text
project_located
→ conversation_started
→ input_validated
→ preflight_executed
→ sources_normalized
→ coverage_classified
→ capabilities_extracted
→ evidence_table_ready
→ goal_contract_compiled
→ confirmation_resolved
→ g1_evaluated
→ verified
→ project_committed
```

修复路由：

```text
无联网 → research_blocked → S1
确认未完成 → pending → S1
局部能力/边界问题 → revise_here → S1
版本冲突 → version_conflict → 重新读取项目
目标实质变化 → 新 GOAL 版本 → S1
```

## 6. 输入收集

至少收集并区分“用户明确事实”与“待验证推断”：

- 目标问题与真实使用场景；
- 学习者或受众；
- 领域、岗位族、目标深度或学段；
- 地区、行业、语言和时效窗口；
- 可用时间、节奏、设备、环境和资源；
- 最终验收方式；
- 风险、隐私、不可执行动作和排除项；
- 用户已有材料及其验证状态。

缺失信息写入 conversation、`working-notes.md` 和 `confirmation.md`；不得静默补成已确认事实。

## 7. 强制外部预检

冷启动、目标实质变化或关键证据过期时，必须真实联网。模型记忆只用于生成问题和查询。

预检至少覆盖：

1. 百科/术语与相邻概念；
2. 官方、教材、学术或标准来源；
3. 真实实践、案例或失败复盘；
4. 当前岗位/职业任务样本（适用时）；
5. 面试、认证、实操或公开评估样本（适用时）；
6. 反方、争议、边界或前沿来源。

来源写入 `sources.jsonl`，新项目使用 `SRC-###`。严格区分：

- `external_evidence`
- `market_signal`
- `model_hypothesis`
- `user_provided_unverified`
- `learner_behavior`

只有真实访问、可定位且接受的来源可以作为 G1 外部证据。无联网时保持 `research_blocked`，不能用用户确认豁免。

## 8. 目标编译

从用户目标和预检证据反推：

1. 可观察能力 `CAP-###`；
2. 每项能力至少一个真实行为或产物；
3. 认知层级与证据类型；
4. 至少一个未见任务、迁移任务或真实综合产物；
5. 可判定的通过规则；
6. 范围、排除项与约束；
7. S2 需要回答的优先研究问题和六源检索种子。

不得把观看时长、完成章节、刷题数量或一次选择题分数直接当成能力。

## 9. 强制确认

S1 为 `mandatory`。

向用户展示并确认：

- 目标能力；
- 成功证据与最终验收；
- 范围和排除项；
- 目标岗位/职级、学段或深度；
- 地区、语言、时效；
- 时间、资源、环境和形式；
- 高风险假设与隐私边界。

确认结果同时进入：

- conversation transcript；
- `user_confirmation` 事件；
- `confirmation.md`；
- `decisions.md`；
- `project-state.json` 的目标版本指针。

未确认时 `confirmation.status=pending`，G1 不得通过。

## 10. G1 与提交

`gate.md` 必须逐维检查：

1. 目标可观察性；
2. 成功标准可判定性；
3. 场景真实性；
4. 外部现实校准度；
5. 来源类别覆盖；
6. 边界与排除项；
7. 约束完整性；
8. 目标—能力—验收一致性；
9. conversation 与事件追溯；
10. 项目 revision 和索引一致性。

只有以下全部满足，才能：

```text
G1=pass
route_to=S2
S1.state=completed
project.current_stage=S2
project.route_to=S2
```

- 所有 G1 维度通过；
- 至少一条 accepted `external_evidence`；
- 强制确认完成；
- 所有稳定 ID 与跨文件引用可解析；
- `verification.md` 为 verified；
- conversation、项目根与阶段索引同步；
- project revision 事务成功。

## 11. Fail closed

- 无真实 conversation：交付不完整。
- 只输出 JSON 或聊天总结：交付不完整。
- 无联网预检：`research_blocked → S1`。
- 强制确认未完成：`pending → S1`。
- 版本冲突：不覆盖，重新加载。
- 旧 run 未迁移：不得继续写旧目录。
- 模型假设冒充证据、市场信号冒充事实：G1 失败。
- 占位符、空表、孤儿 ID 或根索引未更新：G1 不得通过。
- 不得模拟用户回答或代替用户确认。

## 12. 完成输出

对用户的可见回应应结论先行，说明：

- 项目路径和当前项目版本；
- 本次 conversation；
- 目标契约的核心变化；
- G1 verdict 与 route；
- 仍存在的证据缺口或确认项；
- 下一阶段入口。

不要把完整 JSON 信封粘贴到聊天中。完整事实以项目 Wiki 和事件记录为准。
