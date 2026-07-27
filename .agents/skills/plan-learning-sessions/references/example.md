# S5 示例 — learning_and_session_plan

> 下列为**设计夹具**，不是真实观察结果。它们演示包契约（输入 → 正向工件 → 门裁决 → 路由）并附带来源章节追溯；eval 执行时不注入执行器提示。`fixture_type` 显式标注为 `simulated_fixture`。

## 示例 A（正向）— 面向 SQL 误概念的四会话路径

**来源追溯**：`docs/chat_log/七步个性化学习SOP正反例与研究依据.md` §S5 正向例子 1（line 491）；端到端设计案例 `docs/chat_log/七步个性化学习SOP贯穿案例-PostgreSQL查询优化.md` §S5。

**输入事实**

- 上游：`goal_success_contract=gsc-pg-0001`、`capability_concept_graph` 与 `learner_snapshot=LS-001` 版本一致，G1/G3/G4 均通过。
- 学习前沿（来自 G4）：已掌握计划树读取与扫描方式；不稳节点为估算/实际差异、谓词选择性、多列索引顺序；典型误概念 `SELECTIVITY_FIRST_ALWAYS`（把“全局选择性最高列优先”当成机械规则）。
- 约束：4 周、每周约 6 小时、PostgreSQL 18 沙箱；每周两次 90 分钟交互会话；接受三个未见查询的迁移验收。
- 确认：用户确认先修复估算与统计信息模型，再学多列索引，最后扩展条件方案；首个会话契约可执行。

**正向工件 `learning_and_session_plan`（即 `positive_artifact`，校验通过 `learning-and-session-plan.schema.json`）**

```json
{
  "type": "learning_and_session_plan",
  "schema_version": "1.0.0",
  "artifact_id": "lsp-pg-0001",
  "content": {
    "stage_goals": [
      { "goal_id": "sg-1", "statement": "修复'计划器按规则选索引'的错误模型，建立估算—统计—代价的因果链" },
      { "goal_id": "sg-2", "statement": "能独立为未见查询选择并论证多列/部分/覆盖索引，包含能论证'不加索引'的情形" }
    ],
    "ordered_learning_nodes": [
      {
        "node_id": "n-row-est",
        "order": 1,
        "selection_rationale": "学习前沿起点：D1 显示学习者把估算行数当实际行数，是后续所有索引判断的基础",
        "teaching_strategy": ["explain", "worked_example", "retrieval"],
        "scaffolding": { "approach": "标注偏差", "description": "教师先在 EXPLAIN (ANALYZE, BUFFERS) 上标注估算与实际行数差异，再让学习者补标" },
        "fade_conditions": ["学习者独立指出估算偏差并提出验证动作"]
      },
      {
        "node_id": "n-stats",
        "order": 2,
        "selection_rationale": "修复统计信息缺失的错误模型；连接前沿与多列索引推理",
        "teaching_strategy": ["explain", "contrast_case"],
        "scaffolding": { "approach": "对比案例", "description": "对比统计信息新鲜与陈旧两种情形下的计划差异" },
        "fade_conditions": ["能解释何时应 ANALYZE 并说明对计划的影响"]
      },
      {
        "node_id": "n-multicol",
        "order": 3,
        "selection_rationale": "直接处理 SELECTIVITY_FIRST_ALWAYS 误概念；硬先修为 n-row-est 与 n-stats",
        "teaching_strategy": ["worked_example", "practice", "contrast_case"],
        "scaffolding": { "approach": "半完成示例", "description": "给出谓词与数据分布，学习者补出前导列判断的二、三步" },
        "fade_conditions": ["在两个未见查询中独立选择并论证多列索引顺序"]
      },
      {
        "node_id": "n-partial",
        "order": 4,
        "selection_rationale": "扩展条件方案与代价判断；跳过仅视频教学的可选节点",
        "teaching_strategy": ["practice", "transfer"],
        "scaffolding": { "approach": "边界任务", "description": "识别部分索引可用、不可用与参数化边界" },
        "fade_conditions": ["能拒绝一个不合适索引并说明代价原因"]
      },
      {
        "node_id": "n-transfer",
        "order": 5,
        "selection_rationale": "迁移到未见查询并安排延迟复测；对应最终验收任务",
        "teaching_strategy": ["transfer", "delayed_retest"],
        "scaffolding": { "approach": "无提示独立任务", "description": "三个未见查询独立采集、诊断、方案与验证" },
        "fade_conditions": ["三题中至少两题主瓶颈、方案与验证均正确"]
      }
    ],
    "sessions": [
      {
        "session_id": "s1",
        "goal": "建立估算—实际—统计信息的因果链",
        "activities": ["无材料检索：先写自己的计划选择模型", "在沙箱计划上标注估算/实际偏差", "对比统计信息新旧下的计划"],
        "estimated_time": { "minutes_per_session": 90, "session_count": 2 },
        "input_materials": ["PostgreSQL 18 EXPLAIN 文档", "脱敏 orders 查询与沙箱计划"]
      },
      {
        "session_id": "s2",
        "goal": "为多列索引选择论证前导列与排序约束",
        "activities": ["worked example：tenant_id/status/created_at 三列顺序", "半完成示例补步", "对比 (tenant_id,status,created_at) 与 (status,tenant_id,created_at)"],
        "estimated_time": { "minutes_per_session": 90, "session_count": 2 },
        "input_materials": ["PostgreSQL 多列索引文档", "带 ORDER BY ... LIMIT 的案例查询"]
      },
      {
        "session_id": "s3",
        "goal": "扩展部分/覆盖索引并判断代价",
        "activities": ["部分索引可用/不可用/参数化边界", "index-only scan 的可见性条件", "写入代价与维护权衡"],
        "estimated_time": { "minutes_per_session": 90, "session_count": 2 },
        "input_materials": ["部分索引与覆盖索引文档", "写入负载样本"]
      },
      {
        "session_id": "s4",
        "goal": "未见查询迁移与延迟复测",
        "activities": ["三个未见查询独立诊断与方案", "至少一例论证'不加索引'", "一周后对多列索引节点复测"],
        "estimated_time": { "minutes_per_session": 90, "session_count": 2 },
        "input_materials": ["三个未见脱敏查询", "回滚与验证清单"]
      }
    ],
    "assessment_schedule": {
      "immediate": ["每会话末独立完成至少一道未见小题并解释推理", "s2 末在两个查询中独立论证多列索引顺序"],
      "transfer": ["s4 三个未见查询项目：独立采集、诊断、方案、验证与回滚说明"],
      "delayed": ["一周后对 n-multicol 节点延迟复测", "最终项目前一次计划诊断延迟检查"]
    },
    "review_anchors": ["次日", "第4天", "一周后"],
    "risks": [
      { "risk_id": "r-1", "description": "学习者把'全局选择性最高列优先'当成机械规则", "mitigation": "在 s2 插入对比任务，要求回到谓词形状与前导列约束", "criticality": "high" },
      { "risk_id": "r-2", "description": "估算模型修复不牢导致 s2 跨级", "mitigation": "s1 退出标准未达则在 s2 前补一次半完成示例，不提前教授语法", "criticality": "medium" }
    ],
    "alternative_routes": [
      { "trigger": "若 s1 退出标准未达", "adjustment": "在 s2 前增加一次检索式补救，保持最小路径不变" },
      { "trigger": "若延迟复测显示多列索引节点遗忘", "adjustment": "插入一次交错复习，再进入 s4 迁移" }
    ],
    "exit_criteria": {
      "per_node": [
        { "node_id": "n-row-est", "criteria": "独立指出未见计划中的估算偏差并提出验证动作" },
        { "node_id": "n-stats", "criteria": "能解释统计信息新旧对计划的影响并判断是否需要 ANALYZE" },
        { "node_id": "n-multicol", "criteria": "在两个未见查询中独立选择并论证多列索引顺序" },
        { "node_id": "n-partial", "criteria": "能拒绝一个不合适索引并说明代价原因" },
        { "node_id": "n-transfer", "criteria": "三题中至少两题主瓶颈、方案与验证均正确" }
      ],
      "overall": ["三个未见查询中至少两题方案与验证正确", "至少出现一次能论证'不加索引'的案例", "一周后延迟复测通过"]
    }
  }
}
```

**门 G5 裁决（嵌入信封 `quality_evaluation`）**：`verdict=pass`、`route_to=S6`。路径从已证实前沿（估算/统计模型不稳）连到目标（独立诊断并改进单表查询性能）；硬先修 n-row-est/n-stats → n-multicol 被遵守；跳过的仅为已掌握的计划树入门；策略与误概念类型匹配（对比+worked example 处理 `SELECTIVITY_FIRST_ALWAYS`）；测评覆盖即时/迁移/延迟；首个会话 s1 在每周两次 90 分钟约束内可执行；强制确认 `confirmed`。

**完整信封包裹要点**：`status=completed`，`confirmation.status=confirmed`（mode=mandatory），`traceability.fixture_type=simulated_fixture`，`evidence_collected` 中计划假设标 `model_hypothesis`、上游诊断与图谱证据标 `learner_behavior`/`external_evidence`。

## 示例 B（反向/阻塞）— 复制课程目录

**来源追溯**：`docs/chat_log/七步个性化学习SOP正反例与研究依据.md` §S5 反向例子（line 545）。

**输入事实**：有人提交“第1周看完数据库原理第1-5章、第2周看10个索引视频、第3周刷100道题、第4周做项目”；无 `learner_snapshot`、无前沿证据、无节点进入/退出条件，要求立即进入教学。

**为何 G5 失败（不产出正向工件）**

- 未使用 `learner_snapshot`；起点不是已证实前沿。
- 章节与视频不是能力节点；无 `selection_rationale`、硬先修或退出标准。
- 100 道题可能重复同一模板，无法证明迁移；无延迟复测。
- 强制确认无法替代缺失证据；`confirmation.status=pending`。
- `positive_artifact=null`；`quality_evaluation.verdict=revise_here`（或无有效前沿时 `return_upstream`），至少一项量规 `passed=false` 且带 `failure_action`。

**门 G5 裁决**：`revise_here`、`route_to=S5`；若无任何有效学习前沿，则 `return_upstream`、`route_to=S4`。
