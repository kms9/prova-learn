# S1 阶段契约 — create-goal-success-contract（门 G1）

> 本文件治理 S1 与决策门 G1。§0 为七阶段共享规则；其余为 S1 专属。

## 0. 共享阶段契约（适用于 S1–S7）

每个阶段产出**恰好一个**移交信封（`handoff-envelope.schema.json`），并遵循统一执行形状：

```text
校验输入契约
→ 收集需求缺口
→ 执行本阶段确认策略
→ 收集可采信证据
→ 生成具名正向工件
→ 用本阶段专属量规评价
→ 给出 pass / revise_here / return_upstream 与 route_to
```

- **输入契约校验**：至少检查工件类型、schema 版本、必填字段、来源阶段、追溯与上游门状态。失败时 `input_validation.status=fail` 并路由上游，**不得伪造正向工件**。
- **确认状态机**：`mandatory`（S1/S5，未确认不得前进）、`conditional`（S2/S3/S4/S7，遇高风险/分歧/多方案升级为强制）、`inform`（S6 节点推进，告知后继续）。
- **证据来源分类**：`model_hypothesis`/`market_signal`/`external_evidence`/`user_provided_unverified`/`learner_behavior`。**门不得把 `model_hypothesis` 或 `user_provided_unverified` 计为外部证据。**
- **量规结果形状**：`{dimension, evidence[], score, threshold, passed, failure_action, route_to}`；`passed=false` 时 `failure_action` 与 `route_to` 必填。
- **显式未知/阻塞态**：`pending`/`blocked`/`unknown`/`evidence_insufficient`/`research_blocked`/`not_executed`/`version_conflict` 不得被强制为 `pass`。
- **确定性路由**：`pass` 前进；`revise_here` 同阶段重试；`return_upstream` 指向**最早**污染阶段并记录失效下游范围。S7 多归因按上游优先级路由。
- **合并守卫**：快速档仅可在满足条件时合并 S2+S3 或 S4+S5，仍须分别产出工件并依次通过两门；S1、S7 永不合并。

## 1. S1 目的

把模糊的“我想学 X”与一次有边界的强制联网预检，校准为经过外部校准、用户确认、可观察、可验收的目标契约。S1 是“目标校准—领域研究”对（S1–S2）的目标校准半边。

## 2. S1 输入契约

| 输入 | 是否必填 | 说明 |
|---|---|---|
| 学习者诉求/目标问题 | 必填 | 冷启动可模糊 |
| 目标使用场景 | 必填 | 至少一个场景或问题 |
| 既有材料 | 可选 | 须保留来源标识；未验证材料不得默认为事实 |

冷启动允许不完整；未确认推断与模型知识不得写成已确认目标。

## 3. S1 确认策略（强制）

用户确认：目标能力、成功证据、范围、地区/行业/职级、时间/资源/形式约束、排除项。`confirmation.status=pending` 时门不得通过。用户中途根本改变目标时，无论流程进行到哪，都返回 S1。

## 4. S1 强制联网预检（不可降级）

- 确认前执行，即便模型“知道”该领域。
- 至少查询：Wikipedia/百科（术语+相邻概念）、当前 JD（任务/工具/职级）、面试/实操样本、S2 可追溯的一手来源入口。
- 记录 `external_research_seed`：`search_executed`、`retrieval_date`、`queries`、`sources`（仅 `market_signal`/`external_evidence`）、`category_coverage`（每类 `covered`/`not_applicable`/`gap` + `reason` + `gate_effect`）。
- `not_applicable` 必须给出可审计理由；找不到资料记为 `gap`，不是 `not_applicable`。
- 无联网/检索能力时：`status=blocked`，G1 失败，不得用模型记忆替代预检。

## 5. S1 工件字段（`goal_success_contract.content`）

`target_problem`、`target_scene`、`terminology_corrections[]`（`original/corrected/evidence_refs`）、`observable_capabilities[]`（`capability_id/statement/observable_evidence[]`，每项≥1 可观察证据）、`final_assessment`（`tasks[]` + `unseen_or_transfer_required`）、`pass_rules[]`、`scope[]`、`exclusions[]`、`constraints{}`、`external_research_seed`、`open_questions[]`、`confirmed_items[]`（≥1）。

## 6. S1 量规（门 G1）

| 维度 | 阈值类型 | 阈值 | 证据来源 |
|---|---|---|---|
| 目标可观察性 | 每项能力≥1 可观察证据 | ≥1 | observable_capabilities.observable_evidence |
| 成功标准可判定性 | unseen_or_transfer_required | true | final_assessment |
| 场景真实性 | target_scene 非空 | true | target_scene |
| 外部现实校准度 | 有 terminology_corrections 或确认无歧义 | true | terminology_corrections |
| 强制类别覆盖 | wiki/recruiting/interview covered 或可审计 | true | external_research_seed.category_coverage |
| 边界清晰 | exclusions 非空 | ≥1 | exclusions |
| 约束完整 | 时间/形式约束存在 | true | constraints |
| 目标—验收一致 | pass_rules 与能力、验收对齐 | true | pass_rules |

G1 通过当且仅当**所有维度** `passed=true` 且 `confirmation.status=confirmed` 且无关键证据缺口阻塞目标确认。

## 7. S1 路由

| verdict | route_to | 触发 |
|---|---|---|
| `pass` | S2 | 全部 G1 维度通过 + 已确认 |
| `revise_here` | S1 | 目标/成功标准不清、术语漂移、预检未执行或仅模型总结 |
| `return_upstream` | S1 | 用户根本改变目标（S1 是最早阶段，上游返回即重回 S1） |
| `blocked` | S1 | 无联网能力或关键缺口未解决 |

## 8. S1 安全/阻塞态

- 冷启动缺输入 → 记录 `requirement_gaps`，保持 `pending`，不伪造。
- 无检索能力 → `blocked`；G1 失败；不得通过。
- 关键来源类别缺口 → 门阻塞，除非缩小范围、降低置信度并记录缺口。
- 强制确认未完成 → `pending`；G1 不得通过。
