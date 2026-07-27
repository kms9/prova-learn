# check-instructional-interaction 示例

> 下列为**设计夹具**（`fixture_type=simulated_fixture`），不是真实观察结果。它们演示独立质量检查的输入（被检 S6 信封的教学工件）与输出（`quality_check_result`），并附来源追溯。G6 判定工件质量，不宣布学习者掌握。eval 执行时不注入执行器提示。

## 示例 A（通过）— 复核多列索引顺序的渐隐教学工件

**被检输入**：`.agents/skills/run-instructional-interaction/references/example.md` 示例 A 的 S6 信封（`run_id=run-pg-multicol-0001`，`artifact_id=spt-pg-multicol-0001`）。来源：`docs/chat_log/七步个性化学习SOP正反例与研究依据.md` §S6 正向例子 1；端到端案例 `docs/chat_log/七步个性化学习SOP贯穿案例-PostgreSQL查询优化.md` §S6。

**复核输出 `quality_check_result`（校验通过 `quality-check-result.schema.json`）**

```json
{
  "schema_version": "1.0.0",
  "check_id": "qc-spt-pg-multicol-0001",
  "stage_id": "S6",
  "gate_id": "G6",
  "checked_envelope_ref": { "run_id": "run-pg-multicol-0001", "stage_id": "S6", "artifact_id": "spt-pg-multicol-0001" },
  "structural_validation": { "handoff_valid": true, "artifact_valid": true, "errors": [] },
  "dimension_results": [
    { "dimension": "内容正确性与可追溯性", "evidence": ["content_quality_status.state=correct", "explanations[].evidence_refs 各≥1（e-pg-doc-multicolumn/skipscan）"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "对目标和学习者的适配", "evidence": ["session_goal 与 current_node.exit_criteria 对齐", "匹配 N10 学习者前沿"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "认知层级", "evidence": ["explanations 覆盖 understand/apply/analyze", "activities 含 create"], "score": 4, "threshold": 2, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "例子代表性", "evidence": ["examples.positive/negative/boundary/common_misconceptions 均非空"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "支架质量", "evidence": ["hint_ladder 逐级 light→medium→strong 含 fading_condition", "scaffolding_fade_strategy.terminal_support=on_demand"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "答案泄露控制", "evidence": ["independent_transfer.answer_leakage_control=提交前不公布顺序", "completion_problem 隐去关键两步"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "学习者主动性", "evidence": ["interaction_events evt-3 无提示独立给出顺序与沙箱验证步骤", "candidate_mastery_evidence 非空 status=candidate"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "交付可用性", "evidence": ["content 全字段完整，可被 S7 直接消费"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null }
  ],
  "verdict": "pass",
  "route_to": "S7",
  "confirmation_check": { "mode_required": "inform", "status": "acknowledged", "blocking": false },
  "evidence_summary": "内容与 PostgreSQL 18 多列索引文档一致且每条解释有来源；分层解释覆盖多认知层级；正反例+边界+误解齐全；提示逐级且不泄露最终顺序；存在真实独立迁移证据与候选掌握证据（candidate，非掌握宣告）；工件字段完整；放行 S7。G6 通过不等于宣布掌握——延迟保持与边界稳定性留待 G7。",
  "checked_at": "2026-07-26T12:00:00Z"
}
```

## 示例 B（不通过）— 复核“长篇讲义 + 即时答案”

**被检输入**：`.agents/skills/run-instructional-interaction/references/example.md` 示例 B 的反向信封（`positive_artifact=null`：系统连续输出 5000 字索引理论、每题后立即公布答案、学习者仅回复“懂了”，无独立作答、无提示层级、无迁移证据）。来源：`docs/chat_log/七步个性化学习SOP正反例与研究依据.md` §S6 反向例子。

**复核输出 `quality_check_result`**

```json
{
  "schema_version": "1.0.0",
  "check_id": "qc-spt-handout-revise",
  "stage_id": "S6",
  "gate_id": "G6",
  "checked_envelope_ref": { "run_id": "run-handout-revise", "stage_id": "S6", "artifact_id": null },
  "structural_validation": { "handoff_valid": true, "artifact_valid": false, "errors": ["positive_artifact 为 null，无法通过 session-package-and-trace.schema.json"] },
  "dimension_results": [
    { "dimension": "内容正确性与可追溯性", "evidence": ["positive_artifact 缺失，无法核对 evidence_refs 与 content_quality_status"], "score": false, "threshold": true, "passed": false, "failure_action": "revise_here", "route_to": "S6", "notes": "工件未产出，无法确认内容来源可追溯" },
    { "dimension": "支架质量", "evidence": ["无 hint_ladder / scaffolding_fade_strategy / feedback_rules"], "score": false, "threshold": true, "passed": false, "failure_action": "revise_here", "route_to": "S6", "notes": "长篇讲义替代了支架，无逐级提示与撤架条件" },
    { "dimension": "答案泄露控制", "evidence": ["每题后立即显示标准答案"], "score": false, "threshold": true, "passed": false, "failure_action": "revise_here", "route_to": "S6", "notes": "无法区分“会做”与“看懂”" },
    { "dimension": "学习者主动性", "evidence": ["仅 learner 回复“懂了”，无 interaction_events、无 candidate_mastery_evidence"], "score": false, "threshold": true, "passed": false, "failure_action": "revise_here", "route_to": "S6", "notes": "“懂了”不是 learner_behavior 证据，不得代写" },
    { "dimension": "交付可用性", "evidence": ["positive_artifact=null，content 全字段缺失"], "score": false, "threshold": true, "passed": false, "failure_action": "revise_here", "route_to": "S6", "notes": "工件不可被 S7 消费" }
  ],
  "verdict": "revise_here",
  "route_to": "S6",
  "confirmation_check": { "mode_required": "inform", "status": "acknowledged", "blocking": false },
  "evidence_summary": "工件未产出（positive_artifact=null）；答案在提交前即时公布构成泄露；无支架、无独立作答、仅“懂了”不构成 learner_behavior 证据；不得进入 S7 宣称掌握。缺陷均可在 S6 修复，故 revise_here 留在 S6。",
  "checked_at": "2026-07-26T12:05:00Z"
}
```
