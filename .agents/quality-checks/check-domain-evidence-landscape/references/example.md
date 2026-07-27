# check-domain-evidence-landscape 示例

> 下列为**设计夹具**，不是真实观察结果。它们演示独立质量检查的输入（被检 S2 信封）与输出（`quality_check_result`），并附来源追溯。eval 执行时不注入执行器提示。`fixture_type` 显式标注为 `simulated_fixture`。

## 示例 A（通过）— 复核 PostgreSQL 18 领域证据全景

**被检输入**：`.agents/skills/create-domain-evidence-landscape/references/example.md` 示例 A 的 S2 信封（`run_id=run-pg-0002`，`artifact_id=del-pg-0001`，`positive_artifact=domain_evidence_landscape`）。来源：`docs/chat_log/七步个性化学习SOP正反例与研究依据.md` §S2 正向例子 1；端到端案例 `docs/chat_log/七步个性化学习SOP贯穿案例-PostgreSQL查询优化.md` §S2。

**复核输出 `quality_check_result`（校验通过 `quality-check-result.schema.json`）**

```json
{
  "schema_version": "1.0.0",
  "check_id": "qc-del-pg-0001",
  "stage_id": "S2",
  "gate_id": "G2",
  "checked_envelope_ref": { "run_id": "run-pg-0002", "stage_id": "S2", "artifact_id": "del-pg-0001" },
  "structural_validation": { "handoff_valid": true, "artifact_valid": true, "errors": [] },
  "dimension_results": [
    { "dimension": "实际联网执行", "evidence": ["research_run_manifest.online=true", "execution_status=completed", "rounds=3"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "强制来源类别覆盖", "evidence": ["category_coverage 六类均 covered", "recruiting_jd sample_count=3", "interview_selection sample_count=2"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "STORM 视角与问题多样性", "evidence": ["perspectives=6（P1–P6：术语/标准/实践/招聘/面试/批评）", "每视角含 questions 与 query_ids"], "score": 6, "threshold": 6, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "结论可追溯性", "evidence": ["claims C1–C8 均含 evidence_refs", "C1–C5 追溯至 PostgreSQL 18 官方文档"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "事实/市场信号/推断分离", "evidence": ["C8 标 claim_type=market_signal 且 partially_supported", "C7 unsupported 推断（cost≠毫秒）", "JD 来源 provenance=market_signal 未写成 fact"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "争议平衡", "evidence": ["disagreements 两条争议均含 side_a/side_b strong_arguments", "INDEX_ALWAYS_FASTER 争议保留反方"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "证据缺口透明度", "evidence": ["evidence_gaps G1/G2 含 criticality 与 confidence_impact", "无 gate_effect=block"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null }
  ],
  "verdict": "pass",
  "route_to": "S3",
  "confirmation_check": { "mode_required": "conditional", "status": "confirmed", "blocking": false },
  "evidence_summary": "3 轮联网多视角研究已实际执行；六类强制来源覆盖且招聘/面试样本达标；关键产品事实可追溯至 PostgreSQL 18 官方文档；反口诀标记 unsupported；争议保留双方强论据；市场信号与事实分离；缺口透明且不阻塞建图；放行 S3。",
  "checked_at": "2026-07-26T12:00:00Z"
}
```

## 示例 B（不通过/返工）— 复核“三篇博客即宣布共识”

**被检输入**：`.agents/skills/create-domain-evidence-landscape/references/example.md` 示例 B 的 S2 信封（`positive_artifact=null`；三篇同源转载 SEO 博客 + 培训广告；用户要求不再搜索）。来源：`docs/chat_log/七步个性化学习SOP正反例与研究依据.md` §S2 反向例子。

**复核输出 `quality_check_result`**

```json
{
  "schema_version": "1.0.0",
  "check_id": "qc-del-blog-revise",
  "stage_id": "S2",
  "gate_id": "G2",
  "checked_envelope_ref": { "run_id": "run-blog-blocked", "stage_id": "S2", "artifact_id": null },
  "structural_validation": { "handoff_valid": true, "artifact_valid": false, "errors": ["positive_artifact 为 null，无法通过 domain-evidence-landscape.schema.json"] },
  "dimension_results": [
    { "dimension": "实际联网执行", "evidence": ["research_run_manifest 缺失或 online=false", "execution_status≠completed"], "score": false, "threshold": true, "passed": false, "failure_action": "revise_here", "route_to": "S2", "notes": "无可追溯的多视角研究清单与查询" },
    { "dimension": "强制来源类别覆盖", "evidence": ["仅有三篇同源转载博客与培训广告", "official_academic/adversarial_frontier 缺失且被错标 not_applicable"], "score": false, "threshold": true, "passed": false, "failure_action": "revise_here", "route_to": "S2", "notes": "六类未覆盖；缺失类别应记 gap 而非 not_applicable" },
    { "dimension": "结论可追溯性", "evidence": ["声称“所有慢查询都应建索引”“cost 就是毫秒”无 evidence_refs"], "score": false, "threshold": true, "passed": false, "failure_action": "revise_here", "route_to": "S2", "notes": "结论与 PostgreSQL 官方文档冲突且无证据追溯" },
    { "dimension": "事实/市场信号/推断分离", "evidence": ["把同源博客与培训广告当事实", "模型推断写成已确认结论"], "score": false, "threshold": true, "passed": false, "failure_action": "revise_here", "route_to": "S2", "notes": "未分离事实/市场信号/推断" }
  ],
  "verdict": "revise_here",
  "route_to": "S2",
  "confirmation_check": { "mode_required": "conditional", "status": "acknowledged", "blocking": false },
  "evidence_summary": "未执行可追溯的联网多视角研究；来源仅同源博客且缺官方/学术类别（应记 gap）；错误规则（“所有慢查询都应建索引”“cost=毫秒”）无证据支撑且与官方文档冲突；模型推断伪装成事实；用户“不再搜索”不能豁免外部证据门；不放行，留在 S2 重做研究。",
  "checked_at": "2026-07-26T12:10:00Z"
}
```
