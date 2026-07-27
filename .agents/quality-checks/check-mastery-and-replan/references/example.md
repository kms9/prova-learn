# check-mastery-and-replan 示例

> 下列为**设计夹具**（`fixture_type=simulated_fixture`），不是真实观察结果，也不代表已完成真实后端持久化。它们演示独立质量检查的输入（被检 S7 信封）与输出（`quality_check_result`），并附来源追溯。eval 执行时不注入执行器提示。

> 关键约定：G7 是**掌握门**，裁决“掌握证据是否多维齐全 + 归因是否正确 + 版本化更新是否诚实 + 路由是否按确定性表”。**学习者未掌握 ≠ S7 工件失败**：多维证据齐全、归因与路由正确、版本化更新诚实时，工件可通过 G7，`verdict` 与 `route_to` 由归因决定。示例 A 即“未掌握但路由正确”的正向结果——各维 `passed=true`，但 `verdict=return_upstream`、`route_to=S5`。

## 示例 A（通过-as-正确路由）— 复核 SQL 节点未掌握但流程正确的 mastery_and_replanning_bundle

**被检输入**：`.agents/skills/verify-mastery-and-replan/references/example.md` 示例 A 的 S7 信封（`run_id=run-pg-0001`，`artifact_id=mrb-pg-n10-0001`）。来源：`docs/chat_log/七步个性化学习SOP正反例与研究依据.md` §S7 正向例子 1（line 652）；端到端案例 `docs/chat_log/七步个性化学习SOP贯穿案例-PostgreSQL查询优化.md` §S7（line 714）。

**关键判定**：直接表现含 `EVIDENCE_INSUFFICIENT`（分布迁移与延迟证据不足），但决定路由的最早污染主因是 `STRATEGY_OR_SEQUENCE`（策略未把统计信息与分布变化接入索引决策）。按确定性路由表与上游优先级，`primary=STRATEGY_OR_SEQUENCE`、`secondary=[EVIDENCE_INSUFFICIENT]` → `route_to=S5`。`expected_model_version=1` 与 `load.current_model_version=1` 一致，`update.status=proposed`、`persistence=proposed`（无真实后端，未声称已持久化）。

**复核输出 `quality_check_result`（校验通过 `quality-check-result.schema.json`）**

```json
{
  "schema_version": "1.0.0",
  "check_id": "qc-mrb-pg-n10-0001",
  "stage_id": "S7",
  "gate_id": "G7",
  "checked_envelope_ref": { "run_id": "run-pg-0001", "stage_id": "S7", "artifact_id": "mrb-pg-n10-0001" },
  "structural_validation": { "handoff_valid": true, "artifact_valid": true, "errors": [] },
  "dimension_results": [
    { "dimension": "证据充分性", "evidence": ["multicolumn_index_order 与 statistics_and_distribution_transfer 各含 correctness/reasoning_quality/hint_dependency/transfer/confidence/delayed_retention 六维", "每维带 evidence_event_ids Q1/Q2/D3"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "掌握规则一致性", "evidence": ["mastery_judgment: multicolumn_index_order=partial, statistics_and_distribution_transfer=not_mastered", "掌握规则在测评前确定；未用结果反推"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "提示影响控制", "evidence": ["Q1 hint_dependency.level=none", "Q2 hint_dependency.level=moderate 经二级提示后修正，已计入 not_mastered 判定"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "迁移与延迟证据", "evidence": ["transfer 已执行（Q2 分布迁移失败）", "delayed_retention 已执行（D3 三日延迟复测 partial/fail）"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "更新前后一致性", "evidence": ["model_patch[].evidence_event_ids 均追溯至 Q1/Q2/D3", "expected_model_version=1 == load.current_model_version=1"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "调整可解释性", "evidence": ["decision=remediate 与 primary=STRATEGY_OR_SEQUENCE 匹配", "adjusted_path 增加三种数据分布对比并纳入 ANALYZE，有 rationale"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "避免单次结果过度反应", "evidence": ["confidence=calibrated，未因 Q1 正确即升 mastered", "分布迁移未通过故 multicolumn_index_order 仅 provisional=partial"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null }
  ],
  "verdict": "return_upstream",
  "route_to": "S5",
  "confirmation_check": { "mode_required": "conditional", "status": "acknowledged", "blocking": false },
  "evidence_summary": "两节点六维证据齐全；掌握规则先于测评确定；提示依赖被计入；迁移与延迟已执行（虽未通过）；model_patch 可追溯至 Q1/Q2/D3 且版本检查一致；decision=remediate 与 primary=STRATEGY_OR_SEQUENCE 匹配，按确定性路由表与上游优先级 route_to=S5；条件确认未升级且已 acknowledged。工件通过 G7，但因路由上游 verdict=return_upstream——学习者未掌握不等于 S7 工件失败。",
  "checked_at": "2026-07-27T12:30:00Z"
}
```

> 对照（版本冲突情形）：若 `expected_model_version=1` 但 `load.current_model_version=2`，则检查者须确认 `update.status=version_conflict`、`persistence=not_executed`、`model_patch=[]`，掌握判定仍可记录但不得声称已更新；此时“更新前后一致性”维度仍 `passed=true`（诚实未执行），`verdict` 仍由归因决定。

## 示例 B（通过-as-正确路由，简）— 复核分数节点掌握并路由 S6

**被检输入**：`.agents/skills/verify-mastery-and-replan/references/example.md` 示例 B 的 S7 信封（`run_id=run-frac-0002`，`artifact_id=mrb-frac-0002`）。来源：§S7 正向例子 2（line 684）。

**关键判定**：`unit_fraction_magnitude` 与 `same_numerator_comparison` 六维证据均通过（独立解释 + 近迁移 + 表征迁移 + 功能情境 + 一周延迟）；`primary=NODE_MASTERED` → `route_to=S6`。

**复核输出 `quality_check_result`**

```json
{
  "schema_version": "1.0.0",
  "check_id": "qc-mrb-frac-0002",
  "stage_id": "S7",
  "gate_id": "G7",
  "checked_envelope_ref": { "run_id": "run-frac-0002", "stage_id": "S7", "artifact_id": "mrb-frac-0002" },
  "structural_validation": { "handoff_valid": true, "artifact_valid": true, "errors": [] },
  "dimension_results": [
    { "dimension": "证据充分性", "evidence": ["两节点各六维证据齐（F1/F2/F3/F4）"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "掌握规则一致性", "evidence": ["mastery_judgment: 两节点均为 mastered，与预设规则一致"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "提示影响控制", "evidence": ["hint_dependency.level=none（F1/F2/F3）"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "迁移与延迟证据", "evidence": ["transfer=pass（近迁移 + 表征迁移 + 功能情境）", "delayed_retention=pass（一周后独立完成）"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "更新前后一致性", "evidence": ["model_patch before=partial→after=mastered，evidence_event_ids 追溯 F1/F2/F3/F4", "expected_model_version=6 == load.current_model_version=6"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "调整可解释性", "evidence": ["decision=continue 与 primary=NODE_MASTERED 匹配", "保持计划写入 review_schedule"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null },
    { "dimension": "避免单次结果过度反应", "evidence": ["掌握由多维 + 迁移 + 延迟共同支持，非单题"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null }
  ],
  "verdict": "pass",
  "route_to": "S6",
  "confirmation_check": { "mode_required": "conditional", "status": "acknowledged", "blocking": false },
  "evidence_summary": "两节点多维证据齐全且迁移/延迟均通过；掌握判定与预设规则一致；版本检查一致且 model_patch 可追溯；decision=continue 与 NODE_MASTERED 匹配，按路由表 route_to=S6；条件确认已 acknowledged。若本节点为目标终节点且最终验收通过则归因 GOAL_ACHIEVED、route_to=complete。",
  "checked_at": "2026-07-27T12:45:00Z"
}
```

## 示例 C（不通过/留 S7 补测）— 复核“一次选择题正确即 0.95 掌握”

**被检输入**：`.agents/skills/verify-mastery-and-replan/references/example.md` 示例 C 的 S7 信封（`run_id=run-btree-single-mc`，`positive_artifact=null`，主归因 `EVIDENCE_INSUFFICIENT`，`update_status=not_executed`）。来源：§S7 反向例子（line 713）。

**关键判定**：唯一掌握证据是一道识别题“B-tree 适合等值查询吗？— 是”；模型想把掌握概率改成 0.95；`transfer`/`delayed_retention`/`reasoning_quality`/`hint_dependency` 均为 `not_executed`，`confidence=uncalibrated`。S7 正确拒绝产出正向工件并拒绝写入掌握；检查者独立确认主归因 `EVIDENCE_INSUFFICIENT`、`verdict=revise_here`、`route_to=S7`。

**复核输出 `quality_check_result`**

```json
{
  "schema_version": "1.0.0",
  "check_id": "qc-mrb-btree-single-mc",
  "stage_id": "S7",
  "gate_id": "G7",
  "checked_envelope_ref": { "run_id": "run-btree-single-mc", "stage_id": "S7", "artifact_id": null },
  "structural_validation": { "handoff_valid": true, "artifact_valid": false, "errors": ["positive_artifact 为 null，无法通过 mastery-and-replanning-bundle.schema.json"] },
  "dimension_results": [
    { "dimension": "证据充分性", "evidence": ["仅单一识别题，缺 reasoning/transfer/confidence/delayed 多维"], "score": false, "threshold": true, "passed": false, "failure_action": "revise_here", "route_to": "S7", "notes": "单题识别不得作为多维掌握证据" },
    { "dimension": "掌握规则一致性", "evidence": ["claimed_mastery_probability=0.95 无校准依据", "未记录预设掌握规则"], "score": false, "threshold": true, "passed": false, "failure_action": "revise_here", "route_to": "S7", "notes": "0.95 与 not_executed 的多维证据矛盾" },
    { "dimension": "提示影响控制", "evidence": ["hint_dependency=not_executed，未记录提示层级"], "score": false, "threshold": true, "passed": false, "failure_action": "revise_here", "route_to": "S7", "notes": "提示依赖未采集" },
    { "dimension": "迁移与延迟证据", "evidence": ["transfer=not_executed", "delayed_retention=not_executed"], "score": false, "threshold": true, "passed": false, "failure_action": "revise_here", "route_to": "S7", "notes": "必要迁移与延迟证据缺失" },
    { "dimension": "更新前后一致性", "evidence": ["update_status=not_executed，model_patch 为空（未写入掌握）", "expected 与 load 版本未冲突且未强制 applied"], "score": true, "threshold": true, "passed": true, "failure_action": null, "route_to": null, "notes": "未执行被诚实保留，未被强制为已应用" },
    { "dimension": "调整可解释性", "evidence": ["被拒绝的尝试无有效 decision/adjusted_path", "主归因 EVIDENCE_INSUFFICIENT 与 route=S7 一致"], "score": false, "threshold": true, "passed": false, "failure_action": "revise_here", "route_to": "S7", "notes": "不得在证据不足时声称掌握并跳过节点" },
    { "dimension": "避免单次结果过度反应", "evidence": ["单次识别正确即 0.95 掌握概率", "confidence=uncalibrated"], "score": false, "threshold": true, "passed": false, "failure_action": "revise_here", "route_to": "S7", "notes": "触犯避免单次结果过度反应" }
  ],
  "verdict": "revise_here",
  "route_to": "S7",
  "confirmation_check": { "mode_required": "conditional", "status": "acknowledged", "blocking": false },
  "evidence_summary": "仅单一识别题、迁移/延迟/推理/提示均为 not_executed、0.95 掌握无校准依据；S7 正确拒绝写入掌握（update_status=not_executed 诚实保留，未被强制为 applied）；主归因 EVIDENCE_INSUFFICIENT，按确定性路由表 verdict=revise_here、route_to=S7 补测；不放行，不更新为已掌握。结构性 artifact_valid=false 因 positive_artifact=null，但信封本身合法且阶段正确 fail-closed，故为 revise_here 而非 blocked。",
  "checked_at": "2026-07-27T12:55:00Z"
}
```
