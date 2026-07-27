# 七阶段合同与守卫审计

日期：2026-07-27  
范围：`.agents/skills/*/references/stage-contract.md`、公共 handoff Schema、七份阶段 artifact Schema。  
夹具性质：`simulated_fixture`；本文只验证合同与确定性条件，不声称真实学习效果。

## 公共合同

- 七个技能均要求一个 `handoff-envelope.schema.json` 信封。
- 输入校验覆盖类型、Schema 版本、必填字段、来源阶段、追溯与上游门状态；Draft 2020-12 条件约束机械强制 `input_validation.status=fail` 时 `positive_artifact=null`。
- 证据来源固定为 `model_hypothesis`、`market_signal`、`external_evidence`、`user_provided_unverified`、`learner_behavior`。
- 量规条目固定含 `dimension/evidence/score/threshold/passed/failure_action/route_to`；`passed=false` 时 Schema 强制非空 `failure_action` 与确定性 `route_to`。
- `pending/blocked/unknown/evidence_insufficient/research_blocked/not_executed/version_conflict` 不得被强制为 pass。
- 路由遵循“最早污染阶段”；S7 多原因使用上游优先顺序。

## 每阶段安全态

| 阶段 | 缺失输入 | 空证据 | 过期/版本不兼容 | 无法确认 |
|---|---|---|---|---|
| S1 | 留在 S1，记录 requirement gaps | `research_blocked`，G1 失败 | 重新联网预检并重新确认 | mandatory=`pending`，G1 失败 |
| S2 | G1 工件无效则回 S1 | `research_blocked/evidence_insufficient`，留 S2 | 刷新 S1 或 S2 的最早失效证据 | conditional 升级后为 `pending`，G2 失败 |
| S3 | 缺 G1/G2 则回 S1/S2 | 领域事实证据不足回 S2 | 版本/追溯不兼容回最早上游 | 实质建模分歧未确认则留 S3 |
| S4 | 缺可执行图谱/诊断项回 S3 | 无真实学习者回答只产诊断任务，留 S4 | 过期证据标 stale 并复测 | 争议节点未确认则留 S4 |
| S5 | 缺图谱/快照回 S3/S4 | 前沿证据不足回 S4 | 三工件版本不一致回最早上游 | mandatory=`pending`，G5 失败 |
| S6 | 缺确认计划/当前节点回 S5 | 无学习者作答为 `pending`，不得造行为 | 来源/快照/计划失效回最早上游 | 高代价形式变更未确认则留 S6 |
| S7 | 缺 G6 trace/预定义掌握规则回 S6/S3 | `EVIDENCE_INSUFFICIENT`，留 S7 | `version_conflict`，不写入并要求 reload | 高风险完成/路由争议未确认则留 S7 |

### S4 提示—掌握不变量

- `tested_mastered` 必须有同一节点在 `hint_dependency.level=none|low` 下的独立证据。
- 只有 `medium/high/unknown` 提示证据时，节点保持 `tested_not_mastered`/`insufficient_evidence` 并安排撤除支架后的复测。
- 该规则同时存在于 S4 指令、阶段合同和 Draft 2020-12 artifact Schema；旧的 `high + tested_mastered` 组合会被 Schema 拒绝。

### S7 Schema 与量规边界

- Schema 强制每节点六类证据维度、事件引用、版本检查、不可变追加、更新状态与 history 结构。
- `mastered` 必须对照测评前确定的节点专属规则；由于证据和判定位于两个按 `node_id` 关联的数组，Draft 2020-12 无法可靠表达跨数组同节点关联，该语义由 G7 的证据充分性、规则一致性、迁移/延迟三项共同判定。
- 冷启动不是版本 0 的正向 S7 工件：输入门失败、公共 handoff 强制 `positive_artifact=null`，并路由 S4；因此正向 `load.current_model_version>=1` 保持有意约束。

## 快速档合并

### S2+S3

- 允许条件（必须全部满足）：领域成熟、单一范式、低风险、来源质量实质均匀。
- 禁止条件（任一成立即禁止）：竞争范式、活跃分歧、来源可靠性明显不均、证据快速变化、前沿或高风险决策。
- 即使合并，仍须先输出 `domain_evidence_landscape` 并通过 G2，之后才能输出 `capability_concept_graph` 并评价 G3。

### S4+S5

- 允许条件（必须全部满足）：确认零基础、图谱起点明确、路径近线性、错误起点代价低。
- 禁止条件（任一成立即禁止）：先验未知、行为证据冲突、自适应跳级、高风险分班、多个竞争前沿。
- 即使合并，仍须先输出 `learner_snapshot` 并通过 G4，之后才能输出 `learning_and_session_plan` 并评价 G5。

S1 与 S7 永不合并。

## 研究档待执行门

- S2：声明需要独立外部专家复核但无实际专家证据时，状态为 `pending/not_executed`，不得声称研究档完成。
- S7：需要纵向延迟复测但尚未实际运行时，状态为 `pending/not_executed`，不得从即时成功推断长期保持。

## 结论

公共合同、两类快速合并的 allow/deny 守卫、研究档两个 pending gate 和七阶段安全态均已明确；实际执行仍须由阶段工件、门结果和评测证据证明，本文不替代它们。
