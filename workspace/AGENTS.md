# `workspace/` 项目级学习工作区规则

本文件适用于 `workspace/<project-slug>/` 下全部真实学习项目。它与 `.agents/project-workspace-contract.md`、stage manifest/profile 和各阶段 `SKILL.md` 共同构成执行合同。

## 1. 项目是长期容器

- 一个目录代表一个持续学习项目，不代表一次模型运行、一个阶段或一次重试。
- 不得为每个阶段创建新项目；阶段历史写入同一项目的 conversations、stages、learner、sessions 和 assessments。
- `simulations/**` 是非门控夹具区域，不能被真实项目当作学习证据。

## 2. 每次读取顺序

任何写入前依次读取：

1. 项目 `INDEX.md`
2. `PROJECT.md`
3. `project-state.json`
4. 当前阶段 `INDEX.md`
5. `last_conversation_id` 指向的 conversation
6. 本次任务实际需要的 Wiki 页面和 JSONL

按索引按需加载，不默认把整个项目装入上下文。

## 3. 真相层

- Markdown Wiki：当前被接受的含义和人审入口。
- JSONL：不可变的来源、交互、行为、决策、掌握和模型事件。
- `project-state.json`：当前 revision、阶段、route、active IDs 与版本指针。
- JSON/HTML compatibility exports：派生视图，不拥有业务真相。

## 4. 追加与历史

只能追加：

- conversation `transcript.md`、`events.jsonl`
- 阶段 `records.jsonl`
- observations、interaction、mastery、model events
- timeline 新项目

当前 Wiki 页面可更新，但实质替换必须保存 `history/`，并记录 `supersedes` 和事件引用。

## 5. 写入事务

- 开始写入时记录 `expected_project_revision`。
- 提交前重新读取 revision；只有未变化才能提交新快照并 revision + 1。
- 冲突时保留 conversation 和 conflict event，停止更新当前页面。
- learner model 更新还要单独核对 `expected_model_version`；无真实持久化时不得生成有效新版本。

## 6. 用户原文和确认

- 用户原始回答、确认和学习行为不得为了美化而改写。
- S1/S5 的 `confirmation.md` 必须记录 `confirmed_fields`、`unconfirmed_fields`、用户原话和解释依据。
- 普通“继续”“下一步”“跑完流程”不得自动确认多个默认字段，除非上一轮明确列出并提供“接受全部默认值”选项。

## 7. 真实与模拟证据

- 真实学习行为使用 `learner_behavior`。
- 系统构造答案、测试 persona 和 fixture 使用 `synthetic_learner_behavior` 或明确 fixture 元数据。
- 真实 learner snapshot、mastery event、active model 和 project-state 不得引用 `simulations/**`。
- 不得把未作答编译为未掌握。
- 单题或单个复合回答不得直接产生多个 `tested_mastered`。

## 8. 掌握最小规则

除非节点合同要求更严格，`tested_mastered` 至少需要：

```text
两项相互独立的有效观察
OR
一项完整表现任务 + 一项无提示迁移或延迟复测
```

提示后修订、原题重做、自评、年限、一次总分或单一选择题只能形成候选证据。

## 9. 隐私

- Agent 推断、外部事实、用户材料、真实行为和模拟行为必须保持不同 provenance。
- 脱敏时保留占位 ID 和脱敏说明，不静默删除上下文。
- 敏感客户、人员、凭据、合同和内部数据不得写入项目 Wiki。

## 10. 禁止事项

- 不用单个 JSON 文件取代项目 Wiki。
- 不把 `working-notes.md` 当作确认结论。
- 不删除失败会话、被否决路径或 Gate 未通过历史。
- 不把旧 run 与新阶段目录混写而没有迁移记录。
- 不在 revision/version 冲突时强制覆盖。
- 不用 simulations、fixture 或模型代写回答推进真实 Gate。
