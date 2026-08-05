---
name: al-s2-create-domain-evidence-landscape
description: 在统一项目级 LLM Wiki 中执行 S2 领域取证与逐题回答。读取已通过的目标契约，进行真实联网、多视角、多轮研究，形成可追溯回答、冲突、边界、证据等级和刷新策略。缺前置时 fail closed 并路由最早缺失阶段。
---

# S2 领域取证与逐题回答

## 1. 权威输入

读取项目工作区合同、独立调用合同、runtime contract、manifest/profile S2，以及项目根、`project-state.json`、目标版本、最近 conversation 和 `stages/s2-domain-evidence/INDEX.md`。

旧 run、单体 JSON 和 HTML 只作为兼容或迁移输入，不能作为当前主要交付。

## 2. 独立调用

- 无项目：`project_missing → S1`，不创建孤立研究工件。
- 旧 run：先迁移并重新加载。
- G1 缺失、目标版本不一致或入口不可解析：记录 blocked conversation 与 prerequisite check，route S1。
- revision 冲突：不覆盖。

## 3. 问题合同

从 S1 `research-brief.md` 编译稳定的 `RQ-*`。每个问题必须保留：

- 原始目标关系；
- 决策用途；
- 可接受回答边界；
- 需要的来源类型；
- 何种证据会推翻或降级结论。

不得为了“内容更全面”静默改写目标问题，也不得用无关知识填充六源覆盖。

## 4. 研究与来源分层

至少进行两轮真实联网；冲突、关键缺口或新概念触发追加轮次。六个通道是检索视角，不是质量分数：

- job/career；
- books/courses；
- papers/research；
- community/web；
- standards/official；
- artifacts/validation。

每个来源记录：

```text
source_id
channel
provenance
source_group / independent_group
publisher / author
authority
retrieved_at
freshness
region
status
supports / contradicts
limitations
```

同一组织、同一底稿或转载链只能算一个独立来源组。搜索摘要、百科、聚合页只作发现入口，不能自动升级为结论来源。

## 5. 高影响主张

涉及效果比例、市场增长、风险概率、政策、标准、合规或普遍性结论时：

- 优先追到 canonical、原始数据、官方文件或研究原文；
- 只找到二手转引、preliminary、供应商案例或方法不明数字时必须降级；
- 找不到原始依据时标记 `trace_only`、`unverified` 或 `accepted_with_limitations`；
- 不得因为透明写出缺口就把问题算作“未回答”，但也不得把它用于能力门或强决策。

## 6. 原子证据与逐题回答

`evidence-items.jsonl` 中每条证据应是可审计的原子主张，绑定来源、支持方向、独立来源组、适用边界和置信度。

`research-answers.md` 对每个 RQ 记录：

1. 结论；
2. 主要支持；
3. 反证与分歧；
4. 来源独立性；
5. 地区、时间和场景边界；
6. 置信度；
7. 未解决缺口；
8. 对 S3/S4/S7 的可用范围。

模型推断必须显式标记，不能与来源原文混写。

## 7. 八维校验

至少检查：

- 目标问题覆盖；
- 来源通道覆盖；
- 来源角色分离；
- 独立来源组；
- 权威性与原始性；
- 时效与地区适配；
- 冲突与反方；
- 可观察相关性和缺口透明。

六通道都有材料但独立性、权威性或目标相关性不足时，G2 仍不得通过。

## 8. G2 与路由

只有以下全部满足，才能 `G2=pass → S3`：

- 所有关键 RQ 已回答；
- 高影响主张已追源或降级；
- 来源组没有重复计数；
- 原子证据可解析；
- 争议、边界和刷新条件明确；
- conversation、revision、索引与 verification 一致。

关键答案 `partial/unanswered`、只依赖模型常识、只有转载或来源边界不清时保持 S2。

## 9. Fail closed

- 无真实联网：`research_blocked → S2`。
- S1 目标或版本失效：route S1。
- 证据缺口污染能力定义：保持 S2，不由 S3 猜测补齐。
- 用户材料和课程可以定义研究范围，但在核验前保持 `user_provided_unverified`。
- 不得把模拟学习者数据当成领域事实。

## 10. 用户回执

说明研究轮次、独立来源组、关键结论、被降级的主张、仍存缺口、G2 与下一阶段输入。不要用“搜了多少条”代替证据质量结论。
