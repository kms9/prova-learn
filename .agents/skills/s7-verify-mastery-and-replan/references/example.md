# S7 示例 — mastery_and_replanning_bundle

> 下列为**设计夹具**（`fixture_type=simulated_fixture`），不是真实观察结果，也不代表已完成真实后端持久化。它们演示“验证 → 版本化更新 → 归因路由”的闭环，并附带来源章节追溯；eval 执行时不注入执行器提示。

## 示例 A（正向）— SQL 节点未完全掌握，但流程正确，按多归因上游优先级返回 S5

**来源追溯**：`docs/chat_log/七步个性化学习SOP正反例与研究依据.md` §S7 正向例子 1（line 652）；端到端设计案例 `docs/chat_log/七步个性化学习SOP贯穿案例-PostgreSQL查询优化.md` §S7（line 714，第一次掌握验证）。

**输入事实**

- 节点 `multicolumn_index_order` 与 `statistics_and_distribution_transfer`（N10 相关）；
- 证据：Q1 同结构新查询独立选择合理多列索引并解释；Q2 改变数据分布后仍沿用原方案，未要求重新 `ANALYZE`；第一题无提示、第二题经二级提示后修正；D3 三日延迟复测能解释前导列、不能解释估算误差来源；
- 掌握规则在测评前已确定；`expected_model_version=1`，加载版本也是 1；存在真实持久化后端。

**关键判定**：直接表现含 `EVIDENCE_INSUFFICIENT`（分布迁移与延迟证据不足），但决定路由的最早污染主因是 `STRATEGY_OR_SEQUENCE`（策略未把统计信息与分布变化接入索引决策）。因此 primary=`STRATEGY_OR_SEQUENCE`、secondary=`EVIDENCE_INSUFFICIENT`，按上游优先级路由 `S5`。

**正向工件 `mastery_and_replanning_bundle`（即 `positive_artifact`，校验通过 `mastery-and-replanning-bundle.schema.json`）**

```json
{
  "type": "mastery_and_replanning_bundle",
  "schema_version": "1.1.0",
  "artifact_id": "mrb-pg-n10-0001",
  "content": {
    "mastery_verification": {
      "node_mastery_evidence": [
        {
          "node_id": "multicolumn_index_order",
          "correctness": {"result": "correct", "detail": "独立为同结构新查询选择 (tenant_id,status,created_at) 多列索引", "evidence_event_ids": ["Q1"]},
          "reasoning_quality": {"result": "sound", "detail": "能解释前导列与等值谓词的对应", "evidence_event_ids": ["Q1"]},
          "hint_dependency": {"level": "none", "detail": "第一题无提示独立完成", "evidence_event_ids": ["Q1"]},
          "transfer": {"result": "partial", "detail": "同结构迁移通过；数据分布变化后仍沿用原方案", "evidence_event_ids": ["Q2"]},
          "confidence": {"result": "calibrated", "detail": "结论与多维证据一致，未夸大", "evidence_event_ids": ["Q1", "Q2", "D3"]},
          "delayed_retention": {"result": "partial", "detail": "三日延迟复测能解释前导列，不能解释估算误差来源", "evidence_event_ids": ["D3"]}
        },
        {
          "node_id": "statistics_and_distribution_transfer",
          "correctness": {"result": "incorrect", "detail": "分布显著变化后仍沿用原方案，未要求重新 ANALYZE 与测量", "evidence_event_ids": ["Q2"]},
          "reasoning_quality": {"result": "partial", "detail": "未把选择性/基数变化连接到方案更新", "evidence_event_ids": ["Q2"]},
          "hint_dependency": {"level": "moderate", "detail": "经二级提示后修正", "evidence_event_ids": ["Q2"]},
          "transfer": {"result": "fail", "detail": "数据分布迁移未通过", "evidence_event_ids": ["Q2"]},
          "confidence": {"result": "calibrated", "detail": "判定未掌握，与证据一致", "evidence_event_ids": ["Q2", "D3"]},
          "delayed_retention": {"result": "fail", "detail": "延迟复测不能解释估算误差来源", "evidence_event_ids": ["D3"]}
        }
      ],
      "mastery_judgment": [
        {"node_id": "multicolumn_index_order", "status": "partial"},
        {"node_id": "statistics_and_distribution_transfer", "status": "not_mastered"}
      ],
      "attribution": {"primary": "STRATEGY_OR_SEQUENCE", "secondary": ["EVIDENCE_INSUFFICIENT"]},
      "not_mastered_cause": "数据分布迁移与延迟保持证据不足，无法满足 statistics_and_distribution_transfer 的掌握规则；次要原因为策略未把统计信息与分布变化接入索引决策"
    },
    "learner_model_update_and_replan": {
      "load": {
        "learner_id": "learner-demo-01",
        "as_of": "2026-07-27T00:00:00Z",
        "current_model_version": 1,
        "missing_fields": [],
        "evidence_validity": "valid"
      },
      "append_evidence": [
        {"event_id": "Q1", "immutable": true, "source_evidence_ids": ["Q1"], "summary": "同结构新查询独立迁移"},
        {"event_id": "Q2", "immutable": true, "source_evidence_ids": ["Q2"], "summary": "数据分布变化迁移失败"},
        {"event_id": "D3", "immutable": true, "source_evidence_ids": ["D3"], "summary": "三日延迟复测部分通过"}
      ],
      "update": {
        "expected_model_version": 1,
        "loaded_model_version": 1,
        "proposed_model_version": 2,
        "status": "proposed",
        "before": {"model_version": 1},
        "after": {"model_version": 2, "route_to": "S5"},
        "reason": "按多维证据保留部分掌握，并将策略/序列问题路由 S5",
        "persistence": "proposed"
      },
      "history": [
        {"event_id": "h-Q1", "event_type": "evidence", "created_at": "2026-07-27T00:01:00Z", "evidence_event_ids": ["Q1"], "decision": null, "model_version": 1},
        {"event_id": "h-inference", "event_type": "state_inference", "created_at": "2026-07-27T00:02:00Z", "evidence_event_ids": ["Q1", "Q2", "D3"], "decision": "partial/not_mastered", "model_version": 1},
        {"event_id": "h-route", "event_type": "route_decision", "created_at": "2026-07-27T00:03:00Z", "evidence_event_ids": ["Q1", "Q2", "D3"], "decision": "return S5", "model_version": 1}
      ],
      "learner_id": "learner-demo-01",
      "expected_model_version": 1,
      "model_version": 2,
      "model_patch": [
        {"node_id": "multicolumn_index_order", "before": "not_mastered", "after": "partial", "evidence_event_ids": ["Q1", "D3"], "rationale": "独立应用与延迟前导列解释支持 provisional；分布迁移未通过故不升 mastered"},
        {"node_id": "misconception_SELECTIVITY_FIRST_ALWAYS", "before": "active", "after": "weakened_but_active", "evidence_event_ids": ["Q2"], "rationale": "分布变化后仍沿用原方案，但二级提示后可修正"},
        {"node_id": "planner_statistics_reasoning", "before": 0.30, "after": 0.42, "evidence_event_ids": ["D3"], "rationale": "延迟复测显示能解释前导列，但仍不能解释估算误差"}
      ],
      "update_status": "proposed",
      "decision": "remediate",
      "adjusted_path": "在 W2S2 前增加同一查询三种数据分布（5%/50%/80%）对比；把 ANALYZE 与估算偏差重新纳入检索；保留多列索引次日检索；压缩已通过的语法练习",
      "next_session_contract": {
        "next_session_id": "W2S2-R",
        "target_node_id": "statistics_and_distribution_transfer",
        "objective": "在数据分布变化下先预测计划、检查统计信息、再决定是否新增或拒绝索引",
        "required_evidence": ["分布变化下的独立方案选择", "估算与实际行数差异的解释", "一周后延迟复测"],
        "hint_policy": "先要求预测与测量，再给一级提示；不直接给最终方案"
      },
      "review_schedule": {
        "retrieval": ["multicolumn_index_order 次日检索", "前导列选择原则"],
        "spacing": "已通过语法练习间隔拉长，集中时间分配给分布对比",
        "interleaving": "把等值、排序与分布变化查询交错练习",
        "delayed_retest": {"scheduled": true, "interval_days": 7, "target_nodes": ["statistics_and_distribution_transfer"]}
      },
      "evidence_feedback": []
    },
    "route": {"attribution": "STRATEGY_OR_SEQUENCE", "route_to": "S5"},
    "applicability_limits": ["simulated_fixture", "无真实后端，版本 2 仅为提议，未持久化"]
  }
}
```

**门 G7 裁决（嵌入信封 `quality_evaluation`）**：所有量规维度 `passed=true`（多维证据齐全、判定与规则一致、提示影响受控、更新前后可追溯、决策与归因匹配、未对局部成功过度反应），工件质量通过。但因路由指向上游，`verdict=return_upstream`、`route_to=S5`。学习者未掌握不等于 S7 工件失败。

**版本冲突情形（同输入的对照）**：若 `expected_model_version=1` 但 `load.current_model_version=2`（另一会话先写入），则 `update.status=version_conflict`、`update.persistence=not_executed`、`update_status=version_conflict`、`model_patch=[]`，输出重新加载指令；掌握判定仍可记录，但不得声称已更新。

## 示例 B（正向，简）— 分数节点掌握并进入保持计划

**来源追溯**：`docs/chat_log/七步个性化学习SOP正反例与研究依据.md` §S7 正向例子 2（line 684）。

**输入事实**：F1 不看材料解释 `3/5 > 3/7`；F2 近迁移比较 `4/9` 与 `4/11`；F3 表征从图形转到数轴且一周后独立完成；F4 在食谱缩放中正确使用分数关系。`expected_model_version=6`，加载版本 6。

**正向工件 `mastery_and_replanning_bundle`（校验通过同 schema）**

```json
{
  "type": "mastery_and_replanning_bundle",
  "schema_version": "1.1.0",
  "artifact_id": "mrb-frac-0002",
  "content": {
    "mastery_verification": {
      "node_mastery_evidence": [
        {
          "node_id": "unit_fraction_magnitude",
          "correctness": {"result": "correct", "detail": "不看材料解释 3/5 > 3/7", "evidence_event_ids": ["F1"]},
          "reasoning_quality": {"result": "sound", "detail": "用分子相同、分母越大越小解释", "evidence_event_ids": ["F1"]},
          "hint_dependency": {"level": "none", "detail": "无提示独立完成", "evidence_event_ids": ["F1"]},
          "transfer": {"result": "pass", "detail": "近迁移 4/9 vs 4/11 与食谱缩放功能情境均正确", "evidence_event_ids": ["F2", "F4"]},
          "confidence": {"result": "calibrated", "detail": "多维证据一致", "evidence_event_ids": ["F1", "F2", "F3", "F4"]},
          "delayed_retention": {"result": "pass", "detail": "一周后独立完成", "evidence_event_ids": ["F3"]}
        },
        {
          "node_id": "same_numerator_comparison",
          "correctness": {"result": "correct", "detail": "比较 4/9 与 4/11 正确", "evidence_event_ids": ["F2"]},
          "reasoning_quality": {"result": "sound", "detail": "从图形转到数轴表征解释", "evidence_event_ids": ["F2", "F3"]},
          "hint_dependency": {"level": "none", "detail": "无提示独立完成", "evidence_event_ids": ["F2", "F3"]},
          "transfer": {"result": "pass", "detail": "表征迁移（图→数轴）与功能情境迁移通过", "evidence_event_ids": ["F2", "F4"]},
          "confidence": {"result": "calibrated", "detail": "结论由多表征与延迟证据支持", "evidence_event_ids": ["F1", "F2", "F3", "F4"]},
          "delayed_retention": {"result": "pass", "detail": "一周延迟独立完成", "evidence_event_ids": ["F3"]}
        }
      ],
      "mastery_judgment": [
        {"node_id": "unit_fraction_magnitude", "status": "mastered"},
        {"node_id": "same_numerator_comparison", "status": "mastered"}
      ],
      "attribution": {"primary": "NODE_MASTERED", "secondary": []},
      "not_mastered_cause": null
    },
    "learner_model_update_and_replan": {
      "load": {
        "learner_id": "learner-frac-06",
        "as_of": "2026-07-27T01:00:00Z",
        "current_model_version": 6,
        "missing_fields": [],
        "evidence_validity": "valid"
      },
      "append_evidence": [
        {"event_id": "F1", "immutable": true, "source_evidence_ids": ["F1"], "summary": "独立解释同分子分数大小"},
        {"event_id": "F2", "immutable": true, "source_evidence_ids": ["F2"], "summary": "近迁移与表征解释"},
        {"event_id": "F3", "immutable": true, "source_evidence_ids": ["F3"], "summary": "一周延迟保持"},
        {"event_id": "F4", "immutable": true, "source_evidence_ids": ["F4"], "summary": "功能情境迁移"}
      ],
      "update": {
        "expected_model_version": 6,
        "loaded_model_version": 6,
        "proposed_model_version": 7,
        "status": "proposed",
        "before": {"model_version": 6},
        "after": {"model_version": 7, "route_to": "S6"},
        "reason": "独立、迁移与延迟证据满足预定义掌握规则",
        "persistence": "proposed"
      },
      "history": [
        {"event_id": "h-F", "event_type": "evidence", "created_at": "2026-07-27T01:01:00Z", "evidence_event_ids": ["F1", "F2", "F3", "F4"], "decision": null, "model_version": 6},
        {"event_id": "h-F-inference", "event_type": "state_inference", "created_at": "2026-07-27T01:02:00Z", "evidence_event_ids": ["F1", "F2", "F3", "F4"], "decision": "mastered", "model_version": 6},
        {"event_id": "h-F-route", "event_type": "route_decision", "created_at": "2026-07-27T01:03:00Z", "evidence_event_ids": ["F1", "F2", "F3", "F4"], "decision": "continue S6", "model_version": 6}
      ],
      "learner_id": "learner-frac-06",
      "expected_model_version": 6,
      "model_version": 7,
      "model_patch": [
        {"node_id": "unit_fraction_magnitude", "before": "partial", "after": "mastered", "evidence_event_ids": ["F1", "F2", "F3", "F4"], "rationale": "独立、近/远迁移、表征迁移与一周延迟均通过"},
        {"node_id": "same_numerator_comparison", "before": "partial", "after": "mastered", "evidence_event_ids": ["F1", "F2", "F3", "F4"], "rationale": "多表征与功能情境迁移及延迟保持均通过"}
      ],
      "update_status": "proposed",
      "decision": "continue",
      "adjusted_path": "保持原计划进入下一节点 equivalent_fractions；已掌握节点转入保持队列",
      "next_session_contract": {
        "next_session_id": "W3-frac-1",
        "target_node_id": "equivalent_fractions",
        "objective": "在已掌握分数比较基础上学习等值分数与通分",
        "required_evidence": ["等值分数解释", "未见情境迁移", "一周延迟复测"],
        "hint_policy": "先独立尝试，必要时给一级表征提示"
      },
      "review_schedule": {
        "retrieval": ["unit_fraction_magnitude 与 same_numerator_comparison 混合检索"],
        "spacing": "两周后混合检索一次",
        "interleaving": "把分数比较与等值分数交错复习",
        "delayed_retest": {"scheduled": true, "interval_days": 14, "target_nodes": ["unit_fraction_magnitude", "same_numerator_comparison"]}
      },
      "evidence_feedback": []
    },
    "route": {"attribution": "NODE_MASTERED", "route_to": "S6"},
    "applicability_limits": ["simulated_fixture", "无真实后端，版本 7 仅为提议，未持久化"]
  }
}
```

**门 G7 裁决**：`verdict=pass`、`route_to=S6`（进入下一节点）；保持计划写入 `review_schedule`。若本节点为目标终节点且最终验收通过，则归因 `GOAL_ACHIEVED`、`route_to=complete`。

## 示例 C（反向）— 一次选择题正确即 0.95 掌握

**来源追溯**：`docs/chat_log/七步个性化学习SOP正反例与研究依据.md` §S7 反向例子（line 713）。

**输入事实**：唯一掌握证据是一道识别题“B-tree 适合等值查询吗？— 是”，结果正确；模型想把掌握概率改成 0.95；无推理、独立应用、迁移、提示层级或延迟证据。

**被拒绝的尝试（缩略；不作为正向工件）**

```json
{
  "attempted_evidence": "single_recognition_item",
  "item": "B-tree 适合等值查询吗？",
  "answer": "是",
  "result": "correct",
  "claimed_mastery_probability": 0.95,
  "reasoning_quality": "not_executed",
  "hint_dependency": "not_executed",
  "transfer": "not_executed",
  "delayed_retention": "not_executed",
  "confidence": "uncalibrated"
}
```

**为何 G7 失败（不产出正向工件）**

- 只测识别，不测解释、选择、诊断或迁移；`transfer`/`delayed_retention` 为 `not_executed`，证据充分性与迁移/延迟维度不通过。
- `confidence=uncalibrated`：0.95 没有模型、先验或校准依据；触犯“避免单次结果过度反应”。
- 未记录猜测概率与提示层级；状态跳变会错误跳过必要节点。
- `positive_artifact=null`；`quality_evaluation.verdict=revise_here`、`route_to=S7`；主归因 `EVIDENCE_INSUFFICIENT`，`update_status=not_executed`（不写入掌握）。

**门 G7 裁决**：`revise_here`、`route_to=S7` 补测；不得更新为已掌握。

## 三工件交付状态示例

- 每次运行先写完整 `run-s7-S7-review.md`，再生成共同信封 `schema_version=1.3.0`，最后生成已填充的 `run-s7-S7-report.html`；
  Markdown 各章节必须通过 `document_artifact.section_mappings` 与 JSON 实质内容对应，不能压缩成单一掌握分数。
  页面专门展示掌握证据、归因、模型差异、路由、复测/复习和适用限制。
- 页面只允许筛选、对照和展开既有数据，不显示装载器、Schema/模板/Markdown/HTML 生成状态，也不执行模型更新。
- 页面是唯一可视化交付，完全由内嵌 JSON 驱动；本次运行不调用制图工具，也不生成或引用任何独立图片资产。
- 证据不足或版本冲突仍必须生成诊断页面；页面不能把建议路由显示为已执行，也不能伪造模型持久化。
  生成或验证失败时使用对应的 `document_artifact.status=failed` 或 `presentation_artifact.status=failed`，且本次交付不得报告为完整完成。
