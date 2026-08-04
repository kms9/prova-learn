---
name: check-domain-evidence-landscape
description: 独立质量检查 Skill，用于判定项目级 LLM Wiki 中的 S2 领域取证阶段是否达到 G2。它读取项目根、conversation、stages/s2-domain-evidence/ 以及 S1 当前目标，独立复核逐题回答、六源研究、八维校验、版本和路由。
---

# 领域证据质量检查（S2 / G2）

本检查只读、只判。现行 S2 交付位于：

```text
workspace/<project-slug>/stages/s2-domain-evidence/
```

S2 与 S1、conversation 和项目状态共用一个长期项目工作区，不另建独立 run。

## 输入

1. `.agents/project-workspace-contract.md`。
2. `.agents/stage-delivery-manifest.json` 的 `workspace` 与 `S2`。
3. 项目根 `INDEX.md`、`project-state.json` 和 `timeline.md`。
4. `stages/s1-goal-contract/` 当前有效目标、研究简报和 G1 结论。
5. 产生当前 S2 版本的 conversation 与不可变事件。
6. `stages/s2-domain-evidence/` 的共同文件和 S2 专属文件。

## 检查步骤

1. 确认 S1 当前版本仍通过 G1，项目状态允许进入 S2。
2. 检查 S2 阶段文件齐全、JSONL 每行可解析、稳定 ID 和跨页引用可解析。
3. 检查 conversation 记录了实际查询、工具结果、来源新增、争议发现、后续追问、确认和 Gate 事件；研究过程不能只存在于最终回答。
4. 检查 S1 `research-brief.md` 中每个 priority question 都恰好映射一个稳定 `RQ-*` 与 `ANS-*`，不得静默合并或漏题。
5. 检查真实联网研究已执行：至少六视角、至少两轮；冲突或新发现触发的追问可在 `research-log.md` 与事件日志中审计。
6. 独立复核六源通道：`job_career`、`books_courses`、`papers_research`、`community_web`、`standards_official`、`artifacts_validation`。转载链按独立组去重；找不到资料记 `gap`。
7. 检查证据角色：模型假设、用户未验证材料、市场信号和外部证据分离；JD/面经不得冒充领域事实。
8. 对每个答案独立复核八维：来源覆盖、角色分离、来源独立性、可靠性/权威性、时效与地区适配、争议平衡、可观察相关性、边界与缺口清晰度。
9. 检查结构饱和、成熟度至少 L1、刷新策略和升级后的 mandatory 确认。
10. 检查 S2 当前页面能追溯到来源、证据项、conversation 与被替代版本；`project-state.json`、阶段索引和项目根索引一致。
11. 不采信 `gate.md` 自报 verdict；仅当所有关键答案可消费、无阻塞 gap、项目结构和 verification 均通过时，才允许 `pass → S3`。

## Fail closed

- G1 失效、项目根或 S1 当前版本不可解析：`return_upstream → S1`。
- S2 文件缺失、JSONL 非法、逐题映射断裂或研究未执行：`revise_here|blocked → S2`。
- 关键答案为 partial/unanswered，或关键八维失败：G2 不得通过。
- 实质研究没有 conversation/事件记录：G2 不得通过。
- 项目 revision 冲突：记录 `version_conflict`，不得覆盖较新研究版本。
- 不得修改被检项目，也不得替 S2 新增来源、重写答案或补造研究日志。

## 输出

输出符合共享 `quality-check-result.schema.json` 的 JSON：

```text
stage_id=S2
gate_id=G2
verdict=pass|revise_here|return_upstream|blocked
route_to=S1|S2|S3
```

每个失败维度必须包含证据、`failure_action` 和 `route_to`。
