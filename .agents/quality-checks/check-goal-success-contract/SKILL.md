---
name: check-goal-success-contract
description: 独立质量检查 Skill，用于判定 S1 目标校准 run folder 是否达到 G1。它读取 workspace/<project-slug>/runs/<run-id>/INDEX.md 及十个关联文件，独立复核结构、证据、确认和量规，不重新生成目标，不接受旧 JSON 信封或口头通过声明。
---

# 目标契约质量检查（S1 / G1）

本检查只读、只判。现行 S1 交付是 **11 文件 run folder**，不是 `handoff-envelope.json`。交付形状以 `.agents/stage-delivery-manifest.json` 的 `S1` 为唯一机器合同。

## 输入

输入必须是一个 S1 run 目录，入口为：

```text
workspace/<project-slug>/runs/<run-id>/INDEX.md
```

必须存在：`INDEX.md`、`sources.jsonl`、`evidence_table.md`、`coverage.md`、`capabilities.jsonl`、`terminology.jsonl`、`goal-contract.md`、`research-brief.md`、`confirmation.md`、`g1-evaluation.md`、`verification.md`。

## 检查步骤

1. 读取 `.agents/stage-delivery-manifest.json`，确认 S1 `delivery_type=run_folder`。
2. 检查 11 文件齐全、JSONL 每行可解析、无 `TBD`/`TODO`/空标题等占位符。
3. 检查所有稳定 ID 在文件间可解析，`INDEX.md` 能定位其余文件。
4. 独立复核 G1：
   - 目标可观察；
   - 成功标准可判定；
   - 场景真实且边界清晰；
   - 约束和排除项完整；
   - 目标、能力、验收任务一致；
   - 已真实执行外部预检；
   - 至少一条 accepted `external_evidence`；
   - `model_hypothesis` 与 `user_provided_unverified` 未冒充外部证据。
5. 检查强制确认：`confirmation.status=confirmed`；用户确认不能豁免证据门。
6. 不采信 `g1-evaluation.md` 自报 verdict，按量规独立重判。
7. 仅当所有维度通过、`verification` 为 verified、无阻塞 high 风险且路由为 S2 时放行。

## Fail closed

- 缺文件、JSONL 非法、跨引用断裂、存在占位符：`revise_here → S1`。
- 未执行联网预检或没有 accepted external evidence：`blocked|revise_here → S1`。
- 强制确认未完成：`pending → S1`。
- 不得要求或接受旧 `goal_success_contract` JSON envelope 作为现行 S1 通过证据。
- 不得修改被检 run folder，也不得替 S1 补造目标或来源。

## 输出

输出符合共享 `quality-check-result.schema.json` 的 JSON：

```text
stage_id=S1
gate_id=G1
verdict=pass|revise_here|return_upstream|blocked
route_to=S1|S2
```

每个失败维度必须包含证据、`failure_action` 和 `route_to`。
