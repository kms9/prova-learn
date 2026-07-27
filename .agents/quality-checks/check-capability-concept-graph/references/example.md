# check-capability-concept-graph 示例

> 下列为**设计夹具**，不是真实观察结果。它们演示独立质量检查的输入（被检 S3 信封）与输出（`quality_check_result`），并附来源追溯。eval 执行时不注入执行器提示。`traceability.fixture_type` 标注为 `simulated_fixture`。

## 示例 A（通过）— 复核 PostgreSQL 查询优化能力—概念图

**被检输入**：`.agents/skills/build-capability-concept-graph/references/example.md` 示例 A 的 S3 信封（`run_id=run-pg-0003`，`artifact_id=ccg-pg-0001`）。来源：`docs/chat_log/七步个性化学习SOP正反例与研究依据.md` §S3 正向例子 1；端到端案例 `docs/chat_log/七步个性化学习SOP贯穿案例-PostgreSQL查询优化.md` §S3。

**复核输出 `quality_check_result`（校验通过 `quality-check-result.schema.json`）**

```json
{
  "schema_version": "1.0.0",
  "check_id": "qc-ccg-pg-0001",
  "stage_id": "S3",
  "gate_id": "G3",
  "checked_envelope_ref": { "run_id": "run-pg-0003", "stage_id": "S3", "artifact_id": "ccg-pg-0001" },
  "structural_validation": { "handoff_valid": true, "artifact_valid": true, "errors": [] },
  "dimension_results": [
    { "dimension": "结构无环性", "evidence": ["edges 中 hard 子图 8 节点 7 硬边，检查者自验为 DAG，无环"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "先修边可解释性", "evidence": ["每条 hard 先修边均带 rationale；soft 边亦具名说明"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "目标覆盖率", "evidence": ["cap-read-plan / cap-design-index / cap-validate-tradeoff 经 traceability.goal_refs 均可追溯到必要节点"], "score": 3, "threshold": 1, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "节点粒度一致性", "evidence": ["8 节点粒度同阶（表征/概念/过程/策略/元认知），无整章与单步混排"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "能力与概念区分度", "evidence": ["每个节点 capability_statement 可观察；concept 节点不冒充能力"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "评估题有效性", "evidence": ["每个关键节点均有 assessment_item，覆盖 explain/apply/diagnose/transfer/evaluate"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "全链路可追溯性", "evidence": ["traceability 三向 source_refs(S2)/goal_refs(S1)/assessment_refs 均非空"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null }
  ],
  "verdict": "pass",
  "route_to": "S4",
  "confirmation_check": { "mode_required": "conditional", "status": "acknowledged", "blocking": false },
  "evidence_summary": "硬先修子图自验无环、每条先修边均有理由、三个目标能力均可追溯到必要节点、关键节点均有可观察能力与评估、全链路可追溯 S1/S2；条件确认已告知；放行 S4。",
  "checked_at": "2026-07-27T12:00:00Z"
}
```

## 示例 B（不通过/返工）— 复核“把目录当图谱”

**被检输入**：`.agents/skills/build-capability-concept-graph/references/example.md` 示例 B 的阻塞信封（主题目录 `SQL 基础 → 索引 → 执行计划 → 锁 → 事务 → 分区 → 调优`，`positive_artifact=null`，无焦点问题/具名边/误概念/评估/来源）。来源：`docs/chat_log/七步个性化学习SOP正反例与研究依据.md` §S3 反向例子。

**复核输出 `quality_check_result`**

```json
{
  "schema_version": "1.0.0",
  "check_id": "qc-ccg-toc-blocked",
  "stage_id": "S3",
  "gate_id": "G3",
  "checked_envelope_ref": { "run_id": "run-toc-0003", "stage_id": "S3", "artifact_id": null },
  "structural_validation": { "handoff_valid": true, "artifact_valid": false, "errors": ["positive_artifact 为 null，无法通过 capability-concept-graph.schema.json；目录无焦点问题/具名边/误概念/评估/追溯"] },
  "dimension_results": [
    { "dimension": "结构无环性", "evidence": [], "score": false, "threshold": true, "passed": false, "failure_action": "revise_here", "route_to": "S3", "notes": "无边含 hard|soft 强度，目录式'下一章'非先修边，无法判 DAG" },
    { "dimension": "先修边可解释性", "evidence": [], "score": false, "threshold": true, "passed": false, "failure_action": "revise_here", "route_to": "S3", "notes": "无任何 rationale，无法解释先修关系" },
    { "dimension": "评估题有效性", "evidence": [], "score": false, "threshold": true, "passed": false, "failure_action": "revise_here", "route_to": "S3", "notes": "缺 assessment_items 与 mastery_thresholds，无法支持 S4 诊断" },
    { "dimension": "全链路可追溯性", "evidence": [], "score": false, "threshold": true, "passed": false, "failure_action": "revise_here", "route_to": "S3", "notes": "无 traceability，节点不可追溯 S1/S2；若节点本身无 S2 证据则升级为 return_upstream→S2" }
  ],
  "verdict": "revise_here",
  "route_to": "S3",
  "confirmation_check": { "mode_required": "conditional", "status": "pending", "blocking": false },
  "evidence_summary": "主题目录伪装成图谱：无焦点问题、无边强度与理由、无评估与掌握门槛、无追溯；硬先修子图无法判定；不放行，留在 S3 局部重修（节点无证据时升级 S2）。",
  "checked_at": "2026-07-27T12:05:00Z"
}
```
