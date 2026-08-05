---
name: al-s7-verify-mastery-and-replan
description: 在统一项目级 LLM Wiki 中执行 S7 掌握验证、模型更新与重规划。综合正确性、推理、提示依赖、独立性、迁移、置信度和延迟保持，按预设规则判断节点并决定复测、补救、上游返工或完成。禁止单题过度更新和无后端伪持久化。
---

# S7 掌握验证、模型更新与重规划

## 1. 权威输入

读取共享项目合同、独立调用合同、runtime contract、manifest/profile S7、目标成功规则、S3 节点与测评、S4 历史快照、S5 计划、S6 session 和当前 learner model version。

## 2. 独立调用

- 无项目：route S1。
- G3/G4/G5/G6 缺失或失效：blocked，route 最早缺失阶段。
- 无真实历史 learner snapshot 或 `model_version<1`：route S4，禁止创建版本 0。
- 等待迁移或延迟保持：`pending → S7`。
- project revision 或 learner model version 冲突：不应用补丁。

## 3. 预设掌握规则

掌握阈值必须来自 S1/S3/S5 的事前合同，不能在看到答案后降低。默认综合：

```text
correctness
reasoning_quality
hint_dependency
independence
transfer
confidence_calibration
delayed_retention
```

`tested_mastered` 至少要求：

```text
两项相互独立的有效观察
OR
一项完整表现任务 + 一项无提示迁移或延迟复测
```

并且：

- 关键推理达到阈值；
- 提示依赖符合节点合同；
- 必需的迁移通过；
- 目标要求长期保持时，延迟保持已执行；
- 没有未解释的构念混淆或证据污染。

单题、原题重做、提示后修订、自评、年限、一次总分或 G6 通过均不能单独判掌握。

## 4. 证据状态

允许节点结果：

```text
unknown
insufficient_evidence
candidate_mastery
partial
tested_not_mastered
tested_mastered
stale
```

- 正确但使用提示：通常为 `candidate_mastery` 或 `partial`。
- 迁移失败或延迟保持未执行：不得 `tested_mastered`。
- 未掌握不是 G7 工件失败；G7 可完成一次有效判断并 route 补救。

## 5. 证据来源隔离

- 真实 mastery event 只能引用真实 learner behavior 和可追溯 session。
- `synthetic_learner_behavior`、fixture 和 `simulations/**` 不得更新真实 learner model、active version 或 project-state。
- 发现真实项目引用模拟证据时，停止模型更新并 route S4/S6 修复证据链。

## 6. 归因与最早污染点

区分：

- `SOURCE_GAP`：来源事实不可靠 → S2；
- `GRAPH_OR_ASSESSMENT_GAP`：节点或测评不可诊断 → S3；
- `DIAGNOSIS_GAP`：前沿或快照错误 → S4；
- `PLAN_GAP`：路径或策略政策错误 → S5；
- `INSTRUCTION_GAP`：方法执行、内容或提示问题 → S6；
- `EVIDENCE_INSUFFICIENT`：缺迁移、独立性或保持 → 留 S7；
- `GOAL_CHANGED`：目标或验收变化 → S1。

不要因为学习者未掌握就默认归因教学失败；依据事件定位最早污染点。

## 7. 模型更新事务

1. 读取 `expected_model_version`；
2. 追加不可变 mastery evidence/event；
3. 生成 proposed patch 和前后差异；
4. 再次核对 project revision 与 learner model version；
5. 只有真实持久化机制成功时才生成新有效版本；
6. 更新项目指针、索引和 timeline。

没有后端或写入未执行时：

```text
update.status=not_executed
persistence=not_executed
active_model_version 保持不变
```

不得把 proposed version 当作已持久化事实。

## 8. 重规划

根据判断生成明确动作：

- 低提示依赖但迁移不足：S7 无提示新场景复测；
- 概念或策略仍错误：S6 对比/反例补救；
- 路径顺序或负荷问题：S5；
- 诊断构念污染：S4；
- 图谱或来源错误：S3/S2；
- 证据过期：安排维护复测。

复测必须使用新任务，避免把记忆原答案当成能力。

## 9. GOAL_ACHIEVED

只有同时满足才允许 `route_to=complete`：

- S1 最终综合验收通过；
- 关键节点达到事前 mastery rule；
- 必需的未见迁移通过；
- 目标要求的延迟保持通过；
- 没有关键风险、证据污染或版本冲突；
- 最终模型更新和项目状态已真实持久化。

G7 工件质量通过不等于 `GOAL_ACHIEVED`。

## 10. G7

至少检查：

1. 证据维度完整；
2. 最小证据数与独立性；
3. 提示影响；
4. 迁移与保持；
5. 模拟/真实隔离；
6. 归因与最早污染点；
7. 版本检查和真实持久化；
8. 复测/重规划可执行；
9. complete 条件未被放宽；
10. conversation、revision、索引和 verification 一致。

## 11. Fail closed

- 缺真实快照或 session：route S4/S6。
- 证据不足：保持 S7 复测。
- 版本冲突或持久化不可用：不更新 active model。
- 单题、提示后答案或模拟 fixture 推导 mastered：G7 不通过。
- 未完成最终验收、迁移或保持：不得 complete。

## 12. 用户回执

说明节点判断、依据维度、实际模型版本、是否持久化、问题归因、复测或补救任务、G7 和 route。不得只给一个总分或“已学会”。
