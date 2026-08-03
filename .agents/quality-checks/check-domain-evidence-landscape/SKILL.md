---
name: check-domain-evidence-landscape
description: 独立质量检查 Skill，用于判定同一学习 run 下的 S2 领域取证阶段区是否达到 G2。它读取根 INDEX.md 与 s2/INDEX.md 及八个关联文件，独立复核逐题回答、六源研究、八维校验和路由，不接受旧 JSON 信封或口头通过声明。
---

# 领域证据质量检查（S2 / G2）

本检查只读、只判。现行 S2 交付是 **嵌套在 S1 run 中的九文件阶段区**，不是 `domain_evidence_landscape` JSON envelope。交付形状以 `.agents/stage-delivery-manifest.json` 的 `S2` 为唯一机器合同。

## 输入

输入必须是同一个学习 run：

```text
workspace/<project-slug>/runs/<run-id>/
  INDEX.md
  research-brief.md
  ...
  s2/
    INDEX.md
    research-log.md
    sources.jsonl
    coverage.md
    evidence-items.jsonl
    research-answers.md
    answer-validation.md
    g2-evaluation.md
    verification.md
```

S2 开始前必须先验证该 run 的 G1 仍通过，且根索引链接到 `s2/INDEX.md`。

## 检查步骤

1. 读取 `.agents/stage-delivery-manifest.json`，确认 S2 `delivery_type=nested_run_folder`。
2. 检查 `s2/` 九文件齐全、JSONL 每行可解析、无占位符，根 `INDEX.md` 的阶段输出能解析到 `s2/INDEX.md`。
3. 检查 S1 `research-brief.md` 中每个 priority question 都恰好映射一个稳定 `RQ-###` 和 `ANS-###`，不得静默合并或漏题。
4. 检查真实联网研究已执行：至少六视角、至少两轮；冲突或新发现触发的追问可在 `research-log.md` 审计。
5. 独立复核六源通道：`job_career`、`books_courses`、`papers_research`、`community_web`、`standards_official`、`artifacts_validation`。转载链按 `independence_group` 去重；找不到资料记 `gap`，不得伪装为 `not_applicable`。
6. 检查证据角色：`model_hypothesis` 和 `user_provided_unverified` 不计为外部证据；JD/面经等 `market_signal` 不得写成领域事实。
7. 对每个答案独立复核八维：来源覆盖、来源角色分离、来源独立性、可靠性/权威性、时效与地区适配、争议平衡、可观察相关性、边界与缺口清晰度。
8. 检查结构饱和、成熟度至少 L1、升级后的 mandatory 确认已完成。
9. 不采信 `g2-evaluation.md` 自报 verdict；仅当所有关键答案可消费、无阻塞 gap、`verification=verified` 且路由为 S3 时放行。

## Fail closed

- G1 失效、根索引缺失或 priority questions 不可解析：`return_upstream → S1`。
- S2 文件缺失、JSONL 非法、逐题映射断裂、研究未执行：`revise_here|blocked → S2`。
- 关键答案为 partial/unanswered，或关键八维失败：G2 不得通过。
- 不得要求或接受旧 `domain_evidence_landscape` JSON envelope 作为现行 S2 通过证据。
- 不得修改被检阶段区，也不得替 S2 新增来源或重写答案。

## 输出

输出符合共享 `quality-check-result.schema.json` 的 JSON：

```text
stage_id=S2
gate_id=G2
verdict=pass|revise_here|return_upstream|blocked
route_to=S1|S2|S3
```

每个失败维度必须包含证据、`failure_action` 和 `route_to`。
