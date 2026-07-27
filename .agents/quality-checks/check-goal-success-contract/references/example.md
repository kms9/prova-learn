# check-goal-success-contract 示例

> 下列为**设计夹具**，不是真实观察结果。它们演示独立质量检查的输入（被检 S1 信封）与输出（`quality_check_result`），并附来源追溯。eval 执行时不注入执行器提示。

## 示例 A（通过）— 复核 PostgreSQL 目标契约

**被检输入**：`.agents/skills/create-goal-success-contract/references/example.md` 示例 A 的 S1 信封（`run_id=run-pg-0001`，`artifact_id=gsc-pg-0001`）。来源：`docs/chat_log/七步个性化学习SOP正反例与研究依据.md` §S1 正向例子 1。

**复核输出 `quality_check_result`（校验通过 `quality-check-result.schema.json`）**

```json
{
  "schema_version": "1.0.0",
  "check_id": "qc-gsc-pg-0001",
  "stage_id": "S1",
  "gate_id": "G1",
  "checked_envelope_ref": { "run_id": "run-pg-0001", "stage_id": "S1", "artifact_id": "gsc-pg-0001" },
  "structural_validation": { "handoff_valid": true, "artifact_valid": true, "errors": [] },
  "dimension_results": [
    { "dimension": "目标可观察性", "evidence": ["observable_capabilities.cap-explain.observable_evidence"], "score": 3, "threshold": 1, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "成功标准可判定性", "evidence": ["final_assessment.unseen_or_transfer_required=true"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "强制来源类别覆盖", "evidence": ["category_coverage wiki/recruiting/interview=covered"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "边界清晰", "evidence": ["exclusions 非空"], "score": 2, "threshold": 1, "passed": true, "failure_action": null, "route_to": null }
  ],
  "verdict": "pass",
  "route_to": "S2",
  "confirmation_check": { "mode_required": "mandatory", "status": "confirmed", "blocking": false },
  "evidence_summary": "目标可观察、验收要求未见迁移、强制联网预检已执行且类别覆盖可审计、确认已解、无关键缺口；放行 S2。",
  "checked_at": "2026-07-26T11:00:00Z"
}
```

## 示例 B（不通过/阻塞）— 复核“七天成为 AI 专家”

**被检输入**：`.agents/skills/create-goal-success-contract/references/example.md` 示例 B 的阻塞信封（`positive_artifact=null`，`search_executed=false`）。来源：§S1 反向例子。

**复核输出 `quality_check_result`**

```json
{
  "schema_version": "1.0.0",
  "check_id": "qc-gsc-ai-blocked",
  "stage_id": "S1",
  "gate_id": "G1",
  "checked_envelope_ref": { "run_id": "run-ai-blocked", "stage_id": "S1", "artifact_id": null },
  "structural_validation": { "handoff_valid": true, "artifact_valid": false, "errors": ["positive_artifact 为 null，无法通过 goal-success-contract.schema.json"] },
  "dimension_results": [
    { "dimension": "目标可观察性", "evidence": [], "score": 0, "threshold": 1, "passed": false, "failure_action": "revise_here", "route_to": "S1", "notes": "“专家”无可观察定义" },
    { "dimension": "成功标准可判定性", "evidence": [], "score": false, "threshold": true, "passed": false, "failure_action": "revise_here", "route_to": "S1", "notes": "纯选择题无法验证迁移" },
    { "dimension": "强制来源类别覆盖", "evidence": ["search_executed=false"], "score": false, "threshold": true, "passed": false, "failure_action": "revise_here", "route_to": "S1", "notes": "未执行联网预检" }
  ],
  "verdict": "blocked",
  "route_to": "S1",
  "confirmation_check": { "mode_required": "mandatory", "status": "pending", "blocking": true },
  "evidence_summary": "目标不可观察、验收无法判定迁移、未执行联网预检、强制确认未解；不放行，留在 S1。",
  "checked_at": "2026-07-26T11:05:00Z"
}
```
