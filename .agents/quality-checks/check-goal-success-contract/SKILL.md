---
name: check-goal-success-contract
description: 独立质量检查 Skill，用于判定项目级 LLM Wiki 中的 S1 目标校准阶段是否达到 G1。它读取项目根、conversation、stages/s1-goal-contract/ 及项目状态，独立复核结构、证据、确认、版本和量规，不重新生成目标。
---

# 目标契约质量检查（S1 / G1）

本检查只读、只判。现行 S1 交付位于长期项目工作区：

```text
workspace/<project-slug>/
  INDEX.md
  PROJECT.md
  project-state.json
  conversations/...
  stages/s1-goal-contract/
```

单体 JSON envelope 或旧 `runs/<run-id>/` 只能作为兼容导出或迁移输入，不能作为当前 S1 通过证据。

## 输入

1. `.agents/project-workspace-contract.md`。
2. `.agents/stage-delivery-manifest.json` 的 `workspace` 与 `S1`。
3. 项目根 `INDEX.md`、`PROJECT.md`、`project-state.json`、`timeline.md`。
4. 产生当前 S1 版本的 conversation：`INDEX.md`、`transcript.md`、`events.jsonl`、`summary.md`。
5. `stages/s1-goal-contract/` 的共同文件和 S1 专属文件。

## 检查步骤

1. 确认 `delivery_type=project_wiki_stage`，项目根和 S1 阶段目录符合 manifest。
2. 检查 conversation 已记录本次目标补充、外部预检、用户确认和 Gate 事件；`events.jsonl` 每行合法、不可变且 ID 唯一。
3. 检查 S1 当前 Wiki 页面能追溯到 conversation、来源和稳定 ID；被替代版本已进入 `history/` 或有 `supersedes` 记录。
4. 独立复核 G1：
   - 目标可观察；
   - 成功标准可判定；
   - 场景真实且边界清晰；
   - 约束和排除项完整；
   - 目标、能力与验收任务一致；
   - 已真实执行外部预检；
   - 至少一条 accepted `external_evidence`；
   - `model_hypothesis` 与 `user_provided_unverified` 未冒充外部证据。
5. 检查强制确认已写入 `confirmation.md` 和 conversation 事件，且用户确认未被用来豁免证据门。
6. 检查 `project-state.json` 的 `project_revision`、`current_stage`、S1 状态和最近 conversation 指针与项目根索引一致。
7. 不采信 `gate.md` 自报 verdict；按量规独立重判。只有业务维度、项目结构、追溯、版本和 verification 全部通过时，才允许 `pass → S2`。

## Fail closed

- 项目根、conversation 或 S1 阶段文件缺失：`revise_here|blocked → S1`。
- 实质交互未留痕、事件被改写或跨引用断裂：G1 不得通过。
- 未执行联网预检或没有 accepted external evidence：`blocked|revise_here → S1`。
- 强制确认未完成：保持 `pending → S1`。
- 项目 revision 冲突：记录 `version_conflict`，不得覆盖当前目标版本。
- 不得修改被检项目，也不得替 S1 补造目标、来源或 conversation。

## 输出

输出符合共享 `quality-check-result.schema.json` 的 JSON：

```text
stage_id=S1
gate_id=G1
verdict=pass|revise_here|return_upstream|blocked
route_to=S1|S2
```

每个失败维度必须包含证据、`failure_action` 和 `route_to`。
