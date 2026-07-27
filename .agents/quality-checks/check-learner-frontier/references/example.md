# check-learner-frontier 示例

> 下列为**设计夹具**（`fixture_type=simulated_fixture`），不是真实观察结果。它们演示独立质量检查的输入（被检 S4 信封）与输出（`quality_check_result`），并附来源追溯。eval 执行时不注入执行器提示，也不模拟学习者回答。

## 示例 A（通过）— 复核 PostgreSQL 学习者前沿

**被检输入**：`.agents/skills/diagnose-learner-frontier/references/example.md` 示例 A 的 S4 信封（`run_id=run-pg-0001`，`artifact_id=ls-pg-0001`）。来源：`docs/chat_log/七步个性化学习SOP正反例与研究依据.md` §S4 正向例子 1；端到端案例 `docs/chat_log/七步个性化学习SOP贯穿案例-PostgreSQL查询优化.md` §S4。

**复核输出 `quality_check_result`（校验通过 `quality-check-result.schema.json`）**

```json
{
  "schema_version": "1.0.0",
  "check_id": "qc-ls-pg-0001",
  "stage_id": "S4",
  "gate_id": "G4",
  "checked_envelope_ref": { "run_id": "run-pg-0001", "stage_id": "S4", "artifact_id": "ls-pg-0001" },
  "structural_validation": { "handoff_valid": true, "artifact_valid": true, "errors": [] },
  "dimension_results": [
    { "dimension": "测量与目标对齐度", "evidence": ["node_states 覆盖目标与先修链关键节点（plan_tree_basics / estimated_vs_actual_recognition / planner_statistics_reasoning / multicolumn_index_order / workload_change_transfer）"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "证据充分性", "evidence": ["diagnosis_evidence_mapping 关键结论由 D1–D4 多项对齐观察支撑或显式标注证据不足"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "猜对识别", "evidence": ["error_type 区分 none/partial_reasoning/conceptual_misconception/transfer_failure；hint_dependency.level 区分 none/low/high 标注独立与提示"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "提示依赖记录", "evidence": ["node_states[].hint_dependency 逐节点记录 level 与 evidence_refs（none/low/high/unknown）"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "错误分类一致性", "evidence": ["error_type 与 D1–D4 行为描述一致：D3 选择性机械判断→conceptual_misconception，D4 不复测→transfer_failure"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "偏差控制", "evidence": ["自评 8/10 未覆盖行为证据；confidence_calibration 标注 overconfident；evidence_collected 全为 learner_behavior"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "结论可解释性", "evidence": ["diagnosis_evidence_mapping 每条结论→D1–D4 可追溯；learning_frontier.evidence_refs=[D2,D3] 且 rationale 充分"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null }
  ],
  "verdict": "pass",
  "route_to": "S5",
  "confirmation_check": { "mode_required": "conditional", "status": "confirmed", "blocking": false },
  "evidence_summary": "七维度全部通过：关键节点均有对齐诊断项、关键结论有多项 learner_behavior 观察、区分答对/独立/迁移（D1/D2 答对 vs hint=none 独立 vs D4 迁移未通过）、提示与置信度逐节点记录、自评 8/10 未覆盖行为证据、每条结论可回溯 D1–D4；学习前沿 planner_statistics_reasoning 由 D2/D3 支撑且在 evidence_validity 有效期内；放行 S5。",
  "checked_at": "2026-07-26T12:00:00Z"
}
```

## 示例 B（不通过/阻塞）— 复核"自评 8/10 即判中高级"

**被检输入**：`.agents/skills/diagnose-learner-frontier/references/example.md` 示例 B 的阻塞信封（`positive_artifact=null`，仅"熟练度 8/10"自评与一题口号式回答"索引能加速查询吗？是"，无推理过程、提示层级、迁移、耗时或第二个观察）。来源：`docs/chat_log/七步个性化学习SOP正反例与研究依据.md` §S4 反向例子。

**复核输出 `quality_check_result`**

```json
{
  "schema_version": "1.0.0",
  "check_id": "qc-ls-self-rated-blocked",
  "stage_id": "S4",
  "gate_id": "G4",
  "checked_envelope_ref": { "run_id": "run-self-rated-blocked", "stage_id": "S4", "artifact_id": null },
  "structural_validation": { "handoff_valid": true, "artifact_valid": false, "errors": ["positive_artifact 为 null，无法通过 learner-snapshot.schema.json"] },
  "dimension_results": [
    { "dimension": "测量与目标对齐度", "evidence": ["无 node_states，'高级'无法映射到图谱节点"], "score": false, "threshold": true, "passed": false, "failure_action": "revise_here", "route_to": "S4", "notes": "关键节点无对齐诊断项" },
    { "dimension": "证据充分性", "evidence": ["仅一题口号识别，关键结论无≥2 对齐观察"], "score": false, "threshold": true, "passed": false, "failure_action": "revise_here", "route_to": "S4", "notes": "无多项 learner_behavior 观察" },
    { "dimension": "猜对识别", "evidence": ["error_type=recall_only，未区分答对/独立/迁移"], "score": false, "threshold": true, "passed": false, "failure_action": "revise_here", "route_to": "S4", "notes": "口号识别无法证明独立或迁移" },
    { "dimension": "提示依赖记录", "evidence": ["无 hint_dependency 记录"], "score": false, "threshold": true, "passed": false, "failure_action": "revise_here", "route_to": "S4", "notes": "提示层级完全缺失" },
    { "dimension": "偏差控制", "evidence": ["自评 8/10 未经行为校准即判中高级"], "score": false, "threshold": true, "passed": false, "failure_action": "revise_here", "route_to": "S4", "notes": "自评不得计为掌握证据" },
    { "dimension": "结论可解释性", "evidence": ["无 diagnosis_evidence_mapping，无 learning_frontier"], "score": false, "threshold": true, "passed": false, "failure_action": "revise_here", "route_to": "S4", "notes": "无法定位学习前沿" }
  ],
  "verdict": "blocked",
  "route_to": "S4",
  "confirmation_check": { "mode_required": "conditional", "status": "pending", "blocking": true },
  "evidence_summary": "positive_artifact=null 且仅自评与口号识别：无对齐诊断项、无多项行为观察、未区分答对/独立/迁移、提示与置信度缺失、自评 8/10 未校准、无法定位学习前沿；不得把 8/10 写为任何节点 tested_mastered，冷启动保持 unknown/insufficient_evidence 而非全部未掌握画像，留在 S4 补采行为证据。",
  "checked_at": "2026-07-26T12:05:00Z"
}
```
