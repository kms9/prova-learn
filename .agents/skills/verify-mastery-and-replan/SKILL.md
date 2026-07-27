---
name: verify-mastery-and-replan
description: 用预先确定的掌握规则，把会话交互证据综合成节点级掌握判定与归因，再以版本检查原子地更新学习者模型并决定下一步路由。只要用户要进入个性化学习 S7、判断是否学会、更新学习者状态、安排复测或重规划路径，就使用本 skill。
---

# 掌握验证、模型更新与重规划（S7）

S7 是一个完整的反馈事务：验证结果必须被原子地写入学习者模型并产生下一动作。把“本次答对”与长期掌握分开；不要把一次选择题的正确率、单题分数或完成度当成能力。

本 skill 保持一个顶层阶段，但严格按顺序执行两个内部子流程：先 `mastery_verification`，后 `learner_model_update_and_replan`。两者在一次事务内闭环，更新引用验证产生的证据。

## 开始前

1. 读取 [stage-contract.md](references/stage-contract.md)。
2. 读取共享的 `handoff-envelope.schema.json`（位于 S1 skill 目录，勿在本 skill 复制）和 [mastery-and-replanning-bundle.schema.json](references/mastery-and-replanning-bundle.schema.json)。
3. 仅在需要理解输出形状时读取 [example.md](references/example.md)；案例数据是设计夹具，不是真实观察。
4. 校验上游：`session_package_and_trace` 已通过 G6、会话记录完整、节点掌握规则在测评前已确定、历史学习者模型版本可用，且内容质量问题没有被误读为学习者能力问题。

## 执行

### 子流程一：掌握验证（mastery_verification）

1. 对每个待判节点，分别采集并记录多维证据：正确性、推理质量、提示依赖、迁移（近/远）、置信度校准和必要的延迟保持。
2. 区分内容质量问题（S6）、教学策略/顺序问题（S5）、诊断假设冲突（S4）、图谱结构错误（S3）、来源错误（S2）与目标变更（S1），不要混作“学习者不会”。
3. 按预设规则给出每个节点的掌握判定（`mastered`/`partial`/`not_mastered`）；证据不足以满足规则时记为 `partial` 或 `not_mastered`，归因为 `EVIDENCE_INSUFFICIENT`。
4. 单题识别正确不得越级写成高掌握概率；多维证据任一关键维度缺失即不得标为已掌握。

### 子流程二：学习者模型更新与重规划（learner_model_update_and_replan）

5. 读取历史模型版本；执行基于版本的原子更新——仅当 `expected_model_version` 与当前版本匹配时才应用补丁，并保留每个受影响节点的变更前值、变更后值、证据事件 ID 和理由。
6. 版本冲突时：`update_status=version_conflict`，**不应用任何补丁**，输出重新加载指令；不得静默覆盖较新状态。
7. 无真实后端或证据被判定为不足以更新时：`update_status=not_executed`，不得声称持久化成功。
8. 按确定性归因表选择下一动作（`continue`/`remediate`/`skip`/`rediagnose`/`complete`）与 `route_to`；多归因按“目标 → 来源 → 图谱 → 诊断 → 路径 → 内容 → 证据”的上游优先级选择最早污染源。
9. 产出调整后的路径、下一会话契约，以及检索、间隔、交错与延迟复测安排。
10. 重大路径变更触发条件确认；收集学习者反思并说明掌握结论、证据、仍存缺口与调整理由。

## Fail closed

- 无独立应用、迁移或必要延迟证据时，不得标为 `mastered`；保持 `partial`/`not_mastered` 并安排补测或延迟复测。
- 版本冲突或无真实后端时，按 `version_conflict` 或 `not_executed` 诚实标注，不伪造写入成功。
- 学习者未掌握不等于 S7 工件失败：当多维证据齐全、归因与路由正确且更新前后一致时，S7 工件质量可通过，路由仍可指向上游补救。
- 目标发生实质变化时返回 S1，不在 S7 内静默改写目标或验收标准。

## 输出

只输出符合两个 Schema 的 JSON 移交信封。`positive_artifact` 必须是同时包含 `mastery_verification` 与 `learner_model_update_and_replan` 两个有序段的 `mastery_and_replanning_bundle`，且后者的每项关键变更都能追溯到前者采集的证据事件。再生成 `quality_evaluation`：只有当多维证据充分、掌握规则一致、提示影响受控、更新可追溯、调整可解释且未对单次结果过度反应时，才允许工件通过；`route_to` 严格遵循归因路由表。
