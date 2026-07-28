# S4 示例 — learner_snapshot

> 下列为**设计夹具**，不是真实观察结果。它们演示包契约（输入 → 正向工件 → 门裁决 → 路由）并附带来源章节追溯；eval 执行时不注入执行器提示，也不模拟学习者回答。`fixture_type` 显式标注为 `simulated_fixture`。

## 示例 A（正向）— 诊断 PostgreSQL 学习者

**来源追溯**：`docs/chat_log/七步个性化学习SOP正反例与研究依据.md` §S4 正向例子 1（line 398）；端到端设计案例 `docs/chat_log/七步个性化学习SOP贯穿案例-PostgreSQL查询优化.md` §S4（line 361）。

**输入事实（行为观察，证据 ID D1–D4，放入信封 `evidence_collected`，`provenance=learner_behavior`）**

- D1 解释 `EXPLAIN` 与 `EXPLAIN ANALYZE`：知道后者会实际执行，未提及对写操作的副作用/风险。
- D2 标注估算行数与实际行数差异：能指出差异，不能解释统计信息的作用。
- D3 为 `tenant_id = ? AND status = ? ORDER BY created_at DESC` 选索引：只答“把选择性最高的列放前面”。
- D4 数据分布变化后修订方案：仍沿用同一索引，不要求重新测量。
- 自述熟练度 8/10；以上为多次观察的真实行为，与自述存在偏差。

**正向工件 `learner_snapshot`（即 `positive_artifact`，校验通过 `learner-snapshot.schema.json`）**

```json
{
  "type": "learner_snapshot",
  "schema_version": "1.0.0",
  "artifact_id": "ls-pg-0001",
  "content": {
    "learner_id": "learner-demo-01",
    "model_version": 3,
    "as_of": "2026-07-26T09:30:00Z",
    "node_states": [
      {
        "node_id": "plan_tree_basics",
        "status": "tested_mastered",
        "evidence_refs": ["D1"],
        "error_type": "none",
        "hint_dependency": {"level": "none", "evidence_refs": ["D1"]},
        "confidence_calibration": {"self_confidence": null, "observed_alignment": "calibrated"}
      },
      {
        "node_id": "estimated_vs_actual_recognition",
        "status": "tested_mastered",
        "evidence_refs": ["D2"],
        "error_type": "none",
        "hint_dependency": {"level": "none", "evidence_refs": ["D2"]},
        "confidence_calibration": {"self_confidence": null, "observed_alignment": "calibrated"}
      },
      {
        "node_id": "explain_analyze_safety",
        "status": "insufficient_evidence",
        "evidence_refs": ["D1"],
        "error_type": "partial_reasoning",
        "hint_dependency": {"level": "unknown", "evidence_refs": ["D1"]},
        "confidence_calibration": {"self_confidence": null, "observed_alignment": "unknown"}
      },
      {
        "node_id": "planner_statistics_reasoning",
        "status": "tested_not_mastered",
        "evidence_refs": ["D2", "D3"],
        "error_type": "conceptual_misconception",
        "hint_dependency": {"level": "low", "evidence_refs": ["D2"]},
        "confidence_calibration": {"self_confidence": 0.85, "observed_alignment": "overconfident"}
      },
      {
        "node_id": "multicolumn_index_order",
        "status": "tested_not_mastered",
        "evidence_refs": ["D3"],
        "error_type": "conceptual_misconception",
        "hint_dependency": {"level": "high", "evidence_refs": ["D3"]},
        "confidence_calibration": {"self_confidence": 0.80, "observed_alignment": "overconfident"}
      },
      {
        "node_id": "workload_change_transfer",
        "status": "tested_not_mastered",
        "evidence_refs": ["D4"],
        "error_type": "transfer_failure",
        "hint_dependency": {"level": "high", "evidence_refs": ["D4"]},
        "confidence_calibration": {"self_confidence": null, "observed_alignment": "unknown"}
      }
    ],
    "learning_frontier": {
      "nearest_learnable_node_id": "planner_statistics_reasoning",
      "evidence_refs": ["D2", "D3"],
      "rationale": "学习者已能读计划与识别估算偏差，但把统计信息与多列顺序当成机械规则；先修统计信息与估算模型即可解锁多列索引判断",
      "alternative_candidate_node_ids": ["multicolumn_index_order"]
    },
    "misconceptions": [
      {
        "code": "SELECTIVITY_FIRST_ALWAYS",
        "description": "认为多列索引首列必须取全局选择性最高的列，忽略谓词、排序与查询形状约束",
        "evidence_refs": ["D3"],
        "related_node_ids": ["multicolumn_index_order", "planner_statistics_reasoning"]
      },
      {
        "code": "EXPLAIN_ANALYZE_READ_ONLY_ASSUMED",
        "description": "未意识到 EXPLAIN ANALYZE 实际执行可能产生的副作用或写风险",
        "evidence_refs": ["D1"],
        "related_node_ids": ["explain_analyze_safety"]
      }
    ],
    "capability_gaps": [
      {
        "node_id": "planner_statistics_reasoning",
        "description": "不能解释统计信息对估算行数与计划选择的作用",
        "evidence_refs": ["D2"]
      },
      {
        "node_id": "workload_change_transfer",
        "description": "数据分布变化后不重新测量、沿用既有索引",
        "evidence_refs": ["D4"]
      }
    ],
    "transfer_performance": {
      "status": "not_demonstrated",
      "evidence_refs": ["D4"],
      "summary": "分布变化后未迁移，沿用既有索引且不要求复测"
    },
    "diagnosis_evidence_mapping": [
      {"conclusion": "能读基础计划树并区分扫描/过滤/排序", "evidence_refs": ["D1"]},
      {"conclusion": "能识别估算行数与实际行数的差异", "evidence_refs": ["D2"]},
      {"conclusion": "不能解释统计信息对计划的作用，存在误概念", "evidence_refs": ["D2", "D3"]},
      {"conclusion": "多列索引顺序仅凭选择性机械判断", "evidence_refs": ["D3"]},
      {"conclusion": "迁移未通过：分布变化后不重新测量", "evidence_refs": ["D4"]}
    ],
    "items_needing_retest_or_human_confirmation": [
      {"node_id": "explain_analyze_safety", "kind": "retest", "reason": "仅有一次观察且未提写风险，需补测安全边界任务后再定状态"}
    ],
    "evidence_validity": {
      "valid_until": "2026-08-26T00:00:00Z",
      "stale_evidence_refs": [],
      "policy": "诊断证据 30 天内有效；过期仅作线索，关键结论需复测后再生效"
    }
  }
}
```

**门 G4 裁决（嵌入信封 `quality_evaluation`）**：`verdict=pass`、`route_to=S5`。关键结论均有多项对齐观察或显式标注证据不足；区分了识别（D1/D2 答对）、独立（hint=none）与迁移（D4 未通过）；提示依赖与置信度校准逐节点记录；自评 8/10 未覆盖行为证据（偏差控制通过）；每条结论都可回溯到 D1–D4。

**完整信封包裹要点**：`stage_id=S4`，`status=completed`，`confirmation.status=confirmed`（学习者承认常按选择性排序列，符合实际），`traceability.fixture_type=simulated_fixture`；D1–D4 放入 `evidence_collected`，`provenance=learner_behavior`，原始行为、推断状态与路由决策三层分离。

## 示例 B（反向/阻塞）— 自评 8/10 即判中高级

**来源追溯**：`docs/chat_log/七步个性化学习SOP正反例与研究依据.md` §S4 反向例子（line 464）。

**输入事实**：仅“熟练度 8/10”与一题口号式回答“索引能加速查询吗？是”；无推理、提示层级、迁移、时间或第二个观察。

**为何 G4 失败（不产出正向工件）**

- 自评未经校准；第二题只测口号识别（`error_type=recall_only`）。
- 关键节点无多项对齐观察，状态只能为 `insufficient_evidence`/`untested`；“高级”无法映射到图谱节点。
- 没有迁移、反例或错误分类证据；无法定位学习前沿。
- `positive_artifact=null`；不得把 8/10 写成任何节点的 `tested_mastered`。

**门 G4 裁决**：`verdict=revise_here`、`route_to=S4`（补采行为证据）；若诊断题本身无法产生目标证据，则 `return_upstream → S3`。冷启动保持 `unknown`/`evidence_insufficient`，**不**生成“全部未掌握”画像，路由到 S4 建立初始证据。

## 三工件交付状态示例

- 每次运行先写完整 `run-s4-S4-review.md`，再生成共同信封 `schema_version=1.3.0`，最后生成已填充的 `run-s4-S4-report.html`；
  Markdown 各章节必须通过 `document_artifact.section_mappings` 与 JSON 实质内容对应，不能把行为证据简化为节点标签。
  页面专门展示诊断任务、节点状态、学习前沿、行为证据、误概念、缺口和待复测项。
- 页面只允许筛选、对照和展开既有数据，不显示装载器、Schema/模板/Markdown/HTML 生成状态，也不接受学习者作答。
- 页面是唯一可视化交付，完全由内嵌 JSON 驱动；本次运行不调用制图工具，也不生成或引用任何独立图片资产。
- 冷启动或证据不足结果仍必须生成诊断页面；页面不得补造掌握状态。生成或验证失败时使用
  对应的 `document_artifact.status=failed` 或 `presentation_artifact.status=failed`，且本次交付不得报告为完整完成。
