# S6 示例 — session_package_and_trace

> 下列为**设计夹具**，不是真实观察结果。它们演示包契约（输入 → 正向工件 → 门裁决 → 路由）并附带来源章节追溯；eval 执行时不注入执行器提示。`fixture_type` 显式标注为 `simulated_fixture`。

## 示例 A（正向）— 多列索引顺序的渐隐教学

**来源追溯**：`docs/chat_log/七步个性化学习SOP正反例与研究依据.md` §S6 正向例子 1（line 571）；端到端设计案例 `docs/chat_log/七步个性化学习SOP贯穿案例-PostgreSQL查询优化.md` §S6（line 549）。

**输入事实**

- 当前节点：N10 多列索引与排序；G5 已通过，计划要求先预测、再看反例、最后独立迁移。
- 学习者首次回答：“选择性最高的列永远放第一”（暴露把单列全局选择性当唯一规则）。
- 经边界反例与一级提示后修正；随后在未见等值+范围+排序查询上无提示给出正确顺序、理由和沙箱验证步骤。
- 来源：PostgreSQL 18 多列索引与 skip scan 文档。

**正向工件 `session_package_and_trace`（即 `positive_artifact`，校验通过 `session-package-and-trace.schema.json`）**

```json
{
  "type": "session_package_and_trace",
  "schema_version": "1.0.0",
  "artifact_id": "spt-pg-multicol-0001",
  "content": {
    "session_goal": "给定查询谓词、排序和数据分布，比较 (tenant_id, status, created_at) 与 (status, tenant_id, created_at) 两个多列 B-tree 候选；解释前导列约束、首个非等值条件与排序的关系；信息不足时要求测量。",
    "success_conditions": [
      "独立识别等值、范围与排序条件",
      "说明前导列由查询族而非单列全局选择性决定",
      "在未见查询上独立给出索引顺序、理由和沙箱验证步骤"
    ],
    "current_node": {
      "node_id": "N10-multi-column-index",
      "exit_criteria": ["在未见等值+范围+排序查询上独立论证索引顺序"]
    },
    "explanations": [
      {
        "explanation_id": "exp-led-column",
        "layer": "core_concept",
        "representation": "symbolic",
        "statement": "多列 B-tree 索引按声明顺序逐列约束扫描区间；前导列由目标查询族决定，而非单列全局选择性。",
        "cognitive_level": "understand",
        "evidence_refs": ["e-pg-doc-multicolumn"]
      },
      {
        "explanation_id": "exp-range-sort",
        "layer": "procedure",
        "representation": "worked_narrative",
        "statement": "等值条件之后只能再有效服务一个范围或排序列；首个非等值条件之后的列不再有效缩小区间。",
        "cognitive_level": "apply",
        "evidence_refs": ["e-pg-doc-multicolumn"]
      },
      {
        "explanation_id": "exp-skipscan-nuance",
        "layer": "edge_case",
        "representation": "multiple",
        "statement": "PostgreSQL 18 的 skip scan 缓解了部分缺前导列情形，但不等于可以忽略前导列设计；代价仍需测量。",
        "cognitive_level": "analyze",
        "evidence_refs": ["e-pg-doc-multicolumn", "e-pg-doc-skipscan"]
      }
    ],
    "examples": {
      "positive": [
        { "example_id": "ex-pos-a", "summary": "(tenant_id, status, created_at DESC) 服务 tenant 级隔离 + paid 状态等值过滤 + ORDER BY created_at LIMIT" }
      ],
      "negative": [
        { "example_id": "ex-neg-b", "summary": "(status, tenant_id, created_at DESC) 在 tenant 强隔离查询族下前导列失配，扫描区间放大" }
      ],
      "boundary": [
        { "example_id": "ex-bound-skipscan", "summary": "仅 ORDER BY created_at LIMIT、无等值前导列时，PostgreSQL 18 可能走 skip scan 但代价需测量" }
      ],
      "common_misconceptions": [
        {
          "misconception_id": "mis-global-selectivity",
          "description": "把单列全局选择性当作决定前导列的唯一规则",
          "correction_ref": "exp-led-column"
        }
      ]
    },
    "activities": [
      {
        "activity_id": "act-retrieval-pretest",
        "kind": "retrieval_pretest",
        "instruction": "不查资料，先写下选择 Seq / Index / Bitmap Scan 的判断模型",
        "cognitive_level": "understand",
        "requires_learner_output": true,
        "answer_leakage_control": "学习者先产出，再展示参考框架"
      },
      {
        "activity_id": "act-worked-example",
        "kind": "worked_example",
        "instruction": "逐步标注候选 A 与 B 各自能限制哪些扫描区间，给出完整推理而非直接 CREATE INDEX",
        "cognitive_level": "apply",
        "requires_learner_output": false
      },
      {
        "activity_id": "act-completion",
        "kind": "completion_problem",
        "instruction": "给等值+IN 列表+范围+排序查询，补出数据分布确认项与候选索引主要代价",
        "cognitive_level": "analyze",
        "requires_learner_output": true,
        "answer_leakage_control": "隐去关键两步，提交前不提供最终顺序"
      },
      {
        "activity_id": "act-contrast",
        "kind": "contrast_case",
        "instruction": "比较 (tenant_id, status, created_at) 与 (status, tenant_id, created_at) 的适用面",
        "cognitive_level": "analyze",
        "requires_learner_output": true
      },
      {
        "activity_id": "act-independent-transfer",
        "kind": "independent_transfer",
        "instruction": "对未见查询 tenant_id=42 AND created_at >= now()-interval '30 days' ORDER BY created_at DESC LIMIT 100，选择/修改/拒绝一个索引方案并写出沙箱验证步骤",
        "cognitive_level": "create",
        "requires_learner_output": true,
        "answer_leakage_control": "不提供即时答案；提交前不公布顺序"
      }
    ],
    "hint_ladder": [
      { "step": 1, "level": "light", "prompt": "指出查询中的等值、范围与排序条件分别在哪", "fading_condition": "学习者已识别三类条件后撤除" },
      { "step": 2, "level": "medium", "prompt": "判断哪些条件能限制 B-tree 扫描区间、首个范围列之后的列如何", "fading_condition": "能解释前导约束后撤除" },
      { "step": 3, "level": "strong", "prompt": "回到查询族与官方前导列规则比较候选；不直接给最终顺序", "fading_condition": "迁移题中由学习者自行触发" }
    ],
    "feedback_rules": [
      {
        "rule_id": "fb-multi-col",
        "task": "指出比较目标是否对齐目标查询族",
        "process": "检查前导列与首个非等值条件的关系，避免回到单列选择性口诀",
        "self_regulation": "让学习者说明下一题先检查什么"
      }
    ],
    "scaffolding_fade_strategy": {
      "initial_support": "worked example 完整推理 + 半完成题",
      "fade_rule": "每完成一个独立推理环节即撤一级支架",
      "terminal_support": "on_demand"
    },
    "interaction_events": [
      {
        "event_id": "evt-1",
        "learner_response": "status 全局选择性更高，所以候选 B 永远更好",
        "hints_used": ["hint_ladder.step=1"],
        "correction_trajectory": ["回到谓词形状", "确认查询族是否总是 tenant 隔离", "承认不确定数据分布"]
      },
      {
        "event_id": "evt-2",
        "learner_response": "不能只看单列选择性；需要看查询族和排序，但还不确定数据分布",
        "hints_used": ["hint_ladder.step=2"],
        "correction_trajectory": ["把需要确认的数据列为清单", "决定候选前先在沙箱测量"]
      },
      {
        "event_id": "evt-3",
        "learner_response": "在未见等值+范围+排序查询上独立给出索引顺序、理由和沙箱验证步骤",
        "hints_used": [],
        "correction_trajectory": []
      }
    ],
    "candidate_mastery_evidence": [
      { "evidence_id": "E-W2S1-1", "node_id": "N10-multi-column-index", "dimension": "independent_application", "status": "candidate", "limits": ["数据分布剧烈变化时偶尔回到单列选择性口诀"] },
      { "evidence_id": "E-W2S1-2", "node_id": "N10-multi-column-index", "dimension": "transfer", "status": "candidate", "limits": ["延迟保持待 S7 复测"] }
    ],
    "content_quality_status": {
      "state": "correct",
      "reviewed_against": ["PostgreSQL 18 多列索引文档", "PostgreSQL 18 skip scan 文档"],
      "errors_found": []
    }
  }
}
```

**门 G6 裁决（嵌入信封 `quality_evaluation`）**：`verdict=pass`、`route_to=S7`。内容与官方多列索引文档一致；分层解释有多来源；正反例+边界+误解齐全；提示逐级且不泄露最终顺序；存在真实独立迁移证据；支架按回答渐隐；工件字段完整可进入 S7。注意：G6 通过**不**等于宣布掌握——延迟保持与边界稳定性留待 S7。

**完整信封包裹要点**：`stage_id=S6`，`status=completed`，`confirmation.mode=inform`/`status=acknowledged`，`traceability.fixture_type=simulated_fixture`，`evidence_collected` 中检索来源标 `external_evidence`、学习者回答标 `learner_behavior`。

## 示例 B（反向）— 长篇讲义加即时答案

**来源追溯**：`docs/chat_log/七步个性化学习SOP正反例与研究依据.md` §S6 反向例子（line 626）。

**输入事实**：系统连续输出 5000 字索引理论；每道题后立即显示标准答案；学习者只回复“懂了”；无独立作答、无提示层级、无迁移证据。

**为何 G6 失败（不产出正向工件）**

- 答案泄露：练习后立即公布答案，无法区分“会做”与“看懂”。
- 无学习者主动性：仅“懂了”不是 `learner_behavior` 证据，不得代写。
- 无支架与反馈轨迹：缺 `hint_ladder`、`feedback_rules`、`interaction_events`、`candidate_mastery_evidence`。
- 内容长度替代了教学适配：未对齐节点 exit criteria 与学习者前沿。

**门 G6 裁决**：`positive_artifact=null`；`quality_evaluation.verdict=revise_here`，`route_to=S6`；至少“答案泄露控制”与“学习者主动性”两项 `passed=false` 且带 `failure_action=revise_here`。禁止进入 S7 宣称掌握。
