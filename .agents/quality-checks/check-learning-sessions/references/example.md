# check-learning-sessions 示例

> 下列为**设计夹具**（`fixture_type=simulated_fixture`），不是真实观察结果。它们演示独立质量检查的输入（被检 S5 信封）与输出（`quality_check_result`），并附来源追溯。eval 执行时不注入执行器提示。

## 示例 A（通过）— 复核 SQL 误概念四会话计划

**被检输入**：`.agents/skills/plan-learning-sessions/references/example.md` 示例 A 的 S5 信封（`run_id=run-pg-0001`，`artifact_id=lsp-pg-0001`）。来源：`docs/chat_log/七步个性化学习SOP正反例与研究依据.md` §S5 正向例子 1；端到端案例 `docs/chat_log/七步个性化学习SOP贯穿案例-PostgreSQL查询优化.md` §S5。

**复核输出 `quality_check_result`（校验通过 `quality-check-result.schema.json`）**

```json
{
  "schema_version": "1.0.0",
  "check_id": "qc-lsp-pg-0001",
  "stage_id": "S5",
  "gate_id": "G5",
  "checked_envelope_ref": { "run_id": "run-pg-0001", "stage_id": "S5", "artifact_id": "lsp-pg-0001" },
  "structural_validation": { "handoff_valid": true, "artifact_valid": true, "errors": [] },
  "dimension_results": [
    { "dimension": "目标连通性", "evidence": ["ordered_learning_nodes 从前沿起点 n-row-est 连到迁移目标 n-transfer", "exit_criteria.per_node 覆盖全路径"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "先修正确性", "evidence": ["n-multicol 的硬先修 n-row-est/n-stats 在 order 中先行"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "路径最小性", "evidence": ["selection_rationale 说明仅跳过已掌握的计划树入门节点"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "时间可行性", "evidence": ["sessions.estimated_time 每周两次 90 分钟 ×4 周符合每周 6 小时预算", "首个会话 s1 可独立执行"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "策略适配性", "evidence": ["SELECTIVITY_FIRST_ALWAYS 用 contrast_case + worked_example 处理", "scaffolding 半完成示例匹配程序性能力"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "教学与测评对齐度", "evidence": ["exit_criteria.per_node 与 assessment_schedule.immediate/transfer/delayed 对齐"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "认知负荷", "evidence": ["review_anchors 次日/第4天/一周后 与遗忘曲线匹配", "难度处于当前可学习范围"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "调整空间", "evidence": ["risks r-1/r-2 可执行缓解", "alternative_routes 两条可执行调整"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null }
  ],
  "verdict": "pass",
  "route_to": "S6",
  "confirmation_check": { "mode_required": "mandatory", "status": "confirmed", "blocking": false },
  "evidence_summary": "路径从已证实前沿（估算/统计模型不稳）连通到迁移目标；硬先修被遵守；策略匹配误概念类型；测评覆盖即时/迁移/延迟；首个会话 s1 在约束内可执行；强制确认已解；放行 S6。",
  "checked_at": "2026-07-26T12:00:00Z"
}
```

## 示例 B（不通过/阻塞）— 复核“复制课程目录”

**被检输入**：`.agents/skills/plan-learning-sessions/references/example.md` 示例 B 的阻塞信封（`positive_artifact=null`，无 `learner_snapshot`、无能力节点、无退出标准，`confirmation.status=pending`）。来源：§S5 反向例子（line 545）。

**复核输出 `quality_check_result`**

```json
{
  "schema_version": "1.0.0",
  "check_id": "qc-lsp-catalog-blocked",
  "stage_id": "S5",
  "gate_id": "G5",
  "checked_envelope_ref": { "run_id": "run-catalog-blocked", "stage_id": "S5", "artifact_id": null },
  "structural_validation": { "handoff_valid": true, "artifact_valid": false, "errors": ["positive_artifact 为 null，无法通过 learning-and-session-plan.schema.json"] },
  "dimension_results": [
    { "dimension": "目标连通性", "evidence": ["无 learner_snapshot，起点非已证实前沿", "章节/视频非能力节点"], "score": false, "threshold": true, "passed": false, "failure_action": "revise_here", "route_to": "S5", "notes": "复制课程目录，路径不连前沿到目标" },
    { "dimension": "先修正确性", "evidence": ["无 ordered_learning_nodes 与 selection_rationale", "无先修门"], "score": false, "threshold": true, "passed": false, "failure_action": "revise_here", "route_to": "S5", "notes": "无硬先修可言" },
    { "dimension": "路径最小性", "evidence": ["100 道题可能重复同模板，无掌握证据跳过"], "score": false, "threshold": true, "passed": false, "failure_action": "revise_here", "route_to": "S5", "notes": "题量定额非最小路径" },
    { "dimension": "教学与测评对齐度", "evidence": ["无 exit_criteria.per_node", "无延迟复测"], "score": false, "threshold": true, "passed": false, "failure_action": "revise_here", "route_to": "S5", "notes": "退出标准与测评缺失" },
    { "dimension": "策略适配性", "evidence": ["无 teaching_strategy/scaffolding", "无与误概念类型匹配"], "score": false, "threshold": true, "passed": false, "failure_action": "revise_here", "route_to": "S5", "notes": "策略与诊断脱节" }
  ],
  "verdict": "blocked",
  "route_to": "S5",
  "confirmation_check": { "mode_required": "mandatory", "status": "pending", "blocking": true },
  "evidence_summary": "复制课程目录无 learner_snapshot、无能力节点、无退出标准与测评；起点非已证实前沿；强制确认未解；不放行，留在 S5。若无任何有效学习前沿，则升级为 return_upstream 至 S4。",
  "checked_at": "2026-07-26T12:05:00Z"
}
```
