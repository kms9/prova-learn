# S3 示例 — capability_concept_graph

> 下列为**设计夹具**，不是真实观察结果。它们演示包契约（输入 → 正向工件 → 门裁决 → 路由）并附带来源章节追溯；eval 执行时不注入执行器提示。`traceability.fixture_type` 显式标注为 `simulated_fixture`。

## 示例 A（正向）— PostgreSQL 查询优化能力—概念图

**来源追溯**：`docs/chat_log/七步个性化学习SOP正反例与研究依据.md` §S3 正向例子 1（line 298）；端到端设计案例 `docs/chat_log/七步个性化学习SOP贯穿案例-PostgreSQL查询优化.md` §S3（line 269）。

**输入事实**

- 上游：`goal_success_contract`（artifact_id `gsc-pg-0001`，G1 通过）与 `domain_evidence_landscape`（artifact_id `del-pg-0001`，G2 通过）均存在且可追溯。
- 目标：在 PostgreSQL 18 沙箱中独立诊断单表慢查询、提出并验证索引方案；仅沙箱、无生产变更。
- 证据：执行计划节点、估算/实际行数、选择性基数、多列/部分索引、写入代价均有 S2 已审计来源。

**正向工件 `capability_concept_graph`（即 `positive_artifact`，校验通过 `capability-concept-graph.schema.json`）**

```json
{
  "type": "capability_concept_graph",
  "schema_version": "1.1.0",
  "artifact_id": "ccg-pg-0001",
  "content": {
    "focus_question": "学习者要依据什么证据选择并验证一个索引方案？",
    "goal_contract_ref": "gsc-pg-0001",
    "evidence_landscape_ref": "del-pg-0001",
    "target_capabilities": [
      {
        "capability_id": "cap-read-plan",
        "statement": "读取并解释 PostgreSQL 执行计划，定位瓶颈节点",
        "sub_capabilities": [
          { "sub_capability_id": "sub-scan-nodes", "statement": "识别 Seq/Index/Bitmap Scan 节点与过滤位置" },
          { "sub_capability_id": "sub-est-actual", "statement": "区分估算行数与实际行数并解释偏差" }
        ],
        "typical_tasks": ["对一条慢查询采集 EXPLAIN (ANALYZE, BUFFERS) 并指出瓶颈节点"]
      },
      {
        "capability_id": "cap-design-index",
        "statement": "设计并论证索引方案，而非默认加索引",
        "sub_capabilities": [
          { "sub_capability_id": "sub-multicol-order", "statement": "选择多列索引列顺序并说明扫描范围" },
          { "sub_capability_id": "sub-partial-index", "statement": "判断部分索引谓词是否被查询蕴含" }
        ],
        "typical_tasks": ["为给定查询形状提出索引方案并说明扫描范围与边界"]
      },
      {
        "capability_id": "cap-validate-tradeoff",
        "statement": "验证改进并权衡查询收益与写入/空间代价",
        "sub_capabilities": [
          { "sub_capability_id": "sub-tradeoff", "statement": "比较收益与代价并给出取舍建议" },
          { "sub_capability_id": "sub-rollback", "statement": "建立基线、复测并准备回滚" }
        ],
        "typical_tasks": ["在沙箱中复测索引改动并给出采纳/回滚建议"]
      }
    ],
    "learning_units": [
      {
        "unit_id": "unit-read-plan",
        "title": "读取执行计划并定位扫描节点",
        "parent_ref": "sub-scan-nodes",
        "parent_level": "sub_capability",
        "outcome": "能从真实 EXPLAIN 输出识别主要扫描节点、过滤位置与 Buffers 表征",
        "goal_refs": ["cap-read-plan"],
        "source_refs": ["e-doc"],
        "scope_role": "required"
      },
      {
        "unit_id": "unit-explain-estimates",
        "title": "解释估算行数与实际行数偏差",
        "parent_ref": "sub-est-actual",
        "parent_level": "sub_capability",
        "outcome": "能定位 estimated rows 与 actual rows 并解释至少一类偏差来源",
        "goal_refs": ["cap-read-plan"],
        "source_refs": ["e-doc"],
        "scope_role": "required"
      },
      {
        "unit_id": "unit-design-multicolumn",
        "title": "设计多列索引列顺序",
        "parent_ref": "sub-multicol-order",
        "parent_level": "sub_capability",
        "outcome": "能为不同谓词形状比较候选列顺序并说明扫描边界",
        "goal_refs": ["cap-design-index"],
        "source_refs": ["e-doc"],
        "scope_role": "required"
      },
      {
        "unit_id": "unit-design-partial",
        "title": "判断部分索引谓词适用性",
        "parent_ref": "sub-partial-index",
        "parent_level": "sub_capability",
        "outcome": "能判断查询谓词是否蕴含给定部分索引谓词",
        "goal_refs": ["cap-design-index"],
        "source_refs": ["e-doc"],
        "scope_role": "optional"
      },
      {
        "unit_id": "unit-evaluate-tradeoff",
        "title": "权衡索引收益与代价",
        "parent_ref": "sub-tradeoff",
        "parent_level": "sub_capability",
        "outcome": "能比较查询收益、写入和空间代价并给出采纳或拒绝建议",
        "goal_refs": ["cap-design-index", "cap-validate-tradeoff"],
        "source_refs": ["e-doc", "e-jd"],
        "scope_role": "required"
      },
      {
        "unit_id": "unit-validate-rollback",
        "title": "建立基线、复测与回滚",
        "parent_ref": "sub-rollback",
        "parent_level": "sub_capability",
        "outcome": "能在沙箱完成一次含基线、复测和回滚预案的验证",
        "goal_refs": ["cap-validate-tradeoff"],
        "source_refs": ["e-doc"],
        "scope_role": "required"
      }
    ],
    "nodes": [
      {
        "node_id": "n-explain-output",
        "node_type": "representation",
        "capability_statement": "能用 EXPLAIN (ANALYZE, BUFFERS) 文本与 Buffers 统计表征基线与改进",
        "common_misconceptions": ["只看执行时间，不记录 Buffers 命中与读盘差异"]
      },
      {
        "node_id": "n-plan-nodes",
        "node_type": "concept",
        "capability_statement": "能从 EXPLAIN 输出识别 Seq Scan / Index Scan / Bitmap Scan 等节点及过滤位置",
        "common_misconceptions": ["把 cost 字段直接当作墙钟毫秒"]
      },
      {
        "node_id": "n-est-actual",
        "node_type": "concept",
        "capability_statement": "能区分 estimated rows 与 actual rows 并解释偏差来源",
        "common_misconceptions": ["认为估算行数等于实际行数，无需对照"]
      },
      {
        "node_id": "n-selectivity",
        "node_type": "concept",
        "capability_statement": "能根据谓词解释选择性与基数估算对扫描范围的影响",
        "common_misconceptions": ["把选择性最高的列机械地放在多列索引第一位"]
      },
      {
        "node_id": "n-multicol-order",
        "node_type": "procedure",
        "capability_statement": "给定谓词与排序，比较候选列顺序并解释扫描范围与边界",
        "common_misconceptions": ["认为等值列必须按选择性排序而非等值优先"]
      },
      {
        "node_id": "n-partial-index",
        "node_type": "procedure",
        "capability_statement": "能判断查询谓词是否蕴含部分索引的谓词条件",
        "common_misconceptions": ["认为任意查询都能使用某个部分索引"]
      },
      {
        "node_id": "n-index-tradeoff",
        "node_type": "strategy",
        "capability_statement": "能权衡查询收益与写入/空间代价，决定采纳、改方案或拒绝索引",
        "common_misconceptions": ["认为索引越多越好，无需考虑写入代价"]
      },
      {
        "node_id": "n-validate-rollback",
        "node_type": "metacognition",
        "capability_statement": "能在改动前建立基线、复测并准备回滚，而非改一次即结束",
        "common_misconceptions": ["认为改完看到变快就无需复测与回滚预案"]
      }
    ],
    "unit_node_mappings": [
      { "unit_id": "unit-read-plan", "node_id": "n-explain-output", "coverage_role": "supporting", "rationale": "计划节点识别需要先能表征 EXPLAIN 与 Buffers 输出" },
      { "unit_id": "unit-read-plan", "node_id": "n-plan-nodes", "coverage_role": "core", "rationale": "识别扫描节点和过滤位置是该单元的退出能力" },
      { "unit_id": "unit-explain-estimates", "node_id": "n-est-actual", "coverage_role": "core", "rationale": "估算与实际行数偏差解释是该单元的核心判断" },
      { "unit_id": "unit-design-multicolumn", "node_id": "n-selectivity", "coverage_role": "supporting", "rationale": "比较列顺序需要理解选择性与基数如何影响扫描范围" },
      { "unit_id": "unit-design-multicolumn", "node_id": "n-multicol-order", "coverage_role": "core", "rationale": "选择并论证多列索引顺序是该单元的退出能力" },
      { "unit_id": "unit-design-partial", "node_id": "n-selectivity", "coverage_role": "supporting", "rationale": "同一选择性节点跨切支持部分索引适用性判断，不复制节点" },
      { "unit_id": "unit-design-partial", "node_id": "n-partial-index", "coverage_role": "core", "rationale": "判断谓词蕴含是该单元的核心能力" },
      { "unit_id": "unit-evaluate-tradeoff", "node_id": "n-index-tradeoff", "coverage_role": "core", "rationale": "收益与写入/空间代价权衡直接决定单元退出" },
      { "unit_id": "unit-validate-rollback", "node_id": "n-validate-rollback", "coverage_role": "core", "rationale": "基线、复测与回滚纪律是该单元的核心" }
    ],
    "edges": [
      { "from_node": "n-explain-output", "to_node": "n-plan-nodes", "prerequisite_strength": "hard", "rationale": "表征 EXPLAIN 输出是识别计划节点与过滤位置的前提" },
      { "from_node": "n-plan-nodes", "to_node": "n-est-actual", "prerequisite_strength": "hard", "rationale": "必须先识别计划节点，才能定位估算行数与实际行数" },
      { "from_node": "n-plan-nodes", "to_node": "n-selectivity", "prerequisite_strength": "hard", "rationale": "选择性估算依附于具体计划节点的谓词" },
      { "from_node": "n-est-actual", "to_node": "n-multicol-order", "prerequisite_strength": "hard", "rationale": "理解估算偏差后才能比较索引列顺序的扫描范围" },
      { "from_node": "n-selectivity", "to_node": "n-multicol-order", "prerequisite_strength": "hard", "rationale": "列顺序选择依赖选择性与基数估算" },
      { "from_node": "n-selectivity", "to_node": "n-partial-index", "prerequisite_strength": "soft", "rationale": "部分索引谓词蕴含以选择性理解为支撑，但可在主干后补学" },
      { "from_node": "n-multicol-order", "to_node": "n-index-tradeoff", "prerequisite_strength": "hard", "rationale": "比较过候选方案后才能做取舍" },
      { "from_node": "n-partial-index", "to_node": "n-index-tradeoff", "prerequisite_strength": "soft", "rationale": "部分索引是取舍的可选项之一，非必经路径" },
      { "from_node": "n-index-tradeoff", "to_node": "n-validate-rollback", "prerequisite_strength": "hard", "rationale": "决定采纳后才需要建立基线、复测与回滚纪律" }
    ],
    "assessment_items": [
      { "node_id": "n-explain-output", "item": "采集一条慢查询的 EXPLAIN (ANALYZE, BUFFERS) 并指出主扫描节点与 Buffers 命中", "cognitive_level": "apply" },
      { "node_id": "n-plan-nodes", "item": "给定 EXPLAIN 输出，指出 Seq/Index/Bitmap Scan 节点及过滤位置", "cognitive_level": "diagnose" },
      { "node_id": "n-est-actual", "item": "解释某节点 estimated rows 与 actual rows 偏差的可能原因", "cognitive_level": "explain" },
      { "node_id": "n-selectivity", "item": "对 (tenant_id, status) 谓词估计选择性并说明对扫描范围的影响", "cognitive_level": "apply" },
      { "node_id": "n-multicol-order", "item": "为三个不同谓词形状选择多列索引列顺序并说明边界", "cognitive_level": "transfer" },
      { "node_id": "n-partial-index", "item": "判断查询谓词是否蕴含给定的部分索引谓词", "cognitive_level": "diagnose" },
      { "node_id": "n-index-tradeoff", "item": "比较加索引前后查询收益与写入/空间代价并给出取舍建议", "cognitive_level": "evaluate" },
      { "node_id": "n-validate-rollback", "item": "为一次索引改动写出基线、复测与回滚步骤", "cognitive_level": "apply" }
    ],
    "mastery_thresholds": [
      { "node_id": "n-explain-output", "threshold": "独立采集并表征基线计划 2/3 正确", "requires_transfer": false },
      { "node_id": "n-plan-nodes", "threshold": "独立识别扫描节点与过滤位置 2/3 正确", "requires_transfer": false },
      { "node_id": "n-est-actual", "threshold": "能解释至少一类估算偏差来源", "requires_transfer": false },
      { "node_id": "n-selectivity", "threshold": "对两谓词给出选择性判断并排序", "requires_transfer": false },
      { "node_id": "n-multicol-order", "threshold": "三个未见谓词形状中至少两题列顺序与边界正确", "requires_transfer": true },
      { "node_id": "n-partial-index", "threshold": "能判断蕴含/不蕴含各一例", "requires_transfer": false },
      { "node_id": "n-index-tradeoff", "threshold": "给出含代价权衡的取舍建议并通过同伴复核", "requires_transfer": true },
      { "node_id": "n-validate-rollback", "threshold": "完成一次含基线、复测与回滚的端到端验证", "requires_transfer": true }
    ],
    "remediation_entries": [
      { "node_id": "n-est-actual", "trigger": "把 estimated rows 当作 actual rows", "entry": "重看 EXPLAIN 与 EXPLAIN ANALYZE 差异并重做偏差识别练习" },
      { "node_id": "n-selectivity", "trigger": "机械按选择性排序等值列", "entry": "补做等值优先 vs 选择性优先的对比练习" },
      { "node_id": "n-multicol-order", "trigger": "列顺序无理由或忽略边界", "entry": "补做三个谓词形状的边界题并写出理由" },
      { "node_id": "n-index-tradeoff", "trigger": "未说明写入或空间代价", "entry": "加入写入/空间代价测算子任务后再取舍" },
      { "node_id": "n-validate-rollback", "trigger": "未建立基线即改动或未复测", "entry": "回退到基线采集步骤并补写回滚脚本" }
    ],
    "traceability": [
      { "node_id": "n-explain-output", "source_refs": ["e-doc"], "goal_refs": ["cap-read-plan"], "assessment_refs": ["n-explain-output"] },
      { "node_id": "n-plan-nodes", "source_refs": ["e-doc"], "goal_refs": ["cap-read-plan"], "assessment_refs": ["n-plan-nodes"] },
      { "node_id": "n-est-actual", "source_refs": ["e-doc"], "goal_refs": ["cap-read-plan"], "assessment_refs": ["n-est-actual"] },
      { "node_id": "n-selectivity", "source_refs": ["e-doc"], "goal_refs": ["cap-design-index", "cap-read-plan"], "assessment_refs": ["n-selectivity"] },
      { "node_id": "n-multicol-order", "source_refs": ["e-doc"], "goal_refs": ["cap-design-index"], "assessment_refs": ["n-multicol-order"] },
      { "node_id": "n-partial-index", "source_refs": ["e-doc"], "goal_refs": ["cap-design-index"], "assessment_refs": ["n-partial-index"] },
      { "node_id": "n-index-tradeoff", "source_refs": ["e-doc", "e-jd"], "goal_refs": ["cap-validate-tradeoff", "cap-design-index"], "assessment_refs": ["n-index-tradeoff"] },
      { "node_id": "n-validate-rollback", "source_refs": ["e-doc"], "goal_refs": ["cap-validate-tradeoff"], "assessment_refs": ["n-validate-rollback"] }
    ]
  }
}
```

**门 G3 裁决（嵌入信封 `quality_evaluation`）**：`verdict=pass`、`route_to=S4`。六个学习单元均有
核心节点；关联引用全部解析；`n-selectivity` 被两个学习单元复用而未复制；组成层级和硬先修子图分别无环，
且没有把大纲顺序当作先修；每条先修边均有理由；三个目标能力均可追溯到必要节点；每个关键节点均有
可观察能力陈述、误概念、评估题与掌握门槛；学习单元/节点→来源(S2)/目标(S1)/评估全链路可追溯。

**完整信封包裹要点**：`stage_id="S3"`，`status=completed`，`confirmation.mode=conditional`、`status=acknowledged`（无实质分歧），`input_validation.status=pass`（G1/G2 通过且版本兼容），`traceability.fixture_type=simulated_fixture`，`evidence_collected` 中上游工件标为 `external_evidence`、结构推断标为 `model_hypothesis`，`processing_record` 记录“焦点问题→能力反推→节点/边→评估/掌握→追溯”各步。

## 示例 B（反向/阻塞）— 把目录当图谱

**来源追溯**：`docs/chat_log/七步个性化学习SOP正反例与研究依据.md` §S3 反向例子（line 369）。

**输入事实**：仅给出主题目录 `SQL 基础 → 索引 → 执行计划 → 锁 → 事务 → 分区 → 调优`，无焦点问题、无具名边与理由、无误概念、无评估题、无掌握门槛、无来源映射，且混入不属于目标最小路径的“锁/事务/分区”。

**为何 G3 失败（不产出正向工件）**

- 无焦点问题和可测评 `learning_units`，无法判断“能解决什么问题”；节点只是术语，无
  `capability_statement` 与 `common_misconceptions`。
- 无 `unit_node_mappings`，不能判断每个学习单元的核心知识点、跨单元复用或目标必需节点是否成为孤儿。
- 边只是“下一章”，无 `hard | soft` 强度与 `rationale`；无法判断先修关系或环。
- 无 `assessment_items`、`mastery_thresholds`、`remediation_entries`；无法支持 S4 诊断。
- `traceability` 缺失，节点不可追溯到 S1 目标或 S2 来源；若节点本身无证据则归因 `SOURCE_ERROR`。

**门 G3 裁决**：`verdict=revise_here`、`route_to=S3`（局部结构缺陷：缺焦点问题/具名边/评估/追溯）；若节点事实本身无 S2 证据支撑，则升级为 `verdict=return_upstream`、`route_to=S2`。`positive_artifact=null`，`status=blocked`，失效下游范围至少 `["S4","S5","S6","S7"]`。
