# S1 示例 — goal_success_contract

> 下列为**设计夹具**，不是真实观察结果。它们演示包契约（输入 → 正向工件 → 门裁决 → 路由）并附带来源章节追溯；eval 执行时不注入执行器提示。`fixture_type` 显式标注为 `simulated_fixture`。

## 示例 A（正向）— 成人学习 PostgreSQL 查询优化

**来源追溯**：`docs/chat_log/七步个性化学习SOP正反例与研究依据.md` §S1 正向例子 1（line 94）；端到端设计案例 `docs/chat_log/七步个性化学习SOP贯穿案例-PostgreSQL查询优化.md` §S1。

**输入事实**

- 诉求：“会写 SQL，但遇到 PostgreSQL 慢查询只会试着加索引。希望四周内（每周约6小时）能自己看执行计划并做优化。”
- 确认：PostgreSQL 18；仅沙箱；无生产变更权限；目标=诊断并提出可验证改进，非优化器内核。

**正向工件 `goal_success_contract`（即 `positive_artifact`，校验通过 `goal-success-contract.schema.json`）**

```json
{
  "type": "goal_success_contract",
  "schema_version": "1.0.0",
  "artifact_id": "gsc-pg-0001",
  "content": {
    "target_problem": "独立诊断并改进 PostgreSQL 18 中常见的单表查询性能问题",
    "target_scene": "在沙箱中对脱敏的真实形状查询做诊断、方案与验证",
    "terminology_corrections": [
      { "original": "学会查询优化", "corrected": "能诊断并改进单表查询性能", "evidence_refs": ["e-jd"] }
    ],
    "observable_capabilities": [
      { "capability_id": "cap-explain", "statement": "从 EXPLAIN (ANALYZE, BUFFERS) 区分估算与实际执行信息", "observable_evidence": ["指出基线计划估算行数与实际行数差异"] },
      { "capability_id": "cap-scan", "statement": "根据谓词、排序、选择性解释扫描方式", "observable_evidence": ["说明 Bitmap Scan 过滤大量行的原因"] },
      { "capability_id": "cap-index", "statement": "设计并论证单列/多列/部分索引而非默认加索引", "observable_evidence": ["为 (tenant_id,status,created_at) 论证多列索引"] }
    ],
    "final_assessment": {
      "tasks": ["三个未见查询的独立采集、诊断、方案、验证与回滚说明"],
      "unseen_or_transfer_required": true
    },
    "pass_rules": ["三题中至少两题主瓶颈、方案与验证均正确", "不执行未经确认的生产变更"],
    "scope": ["PostgreSQL 18 单表查询与索引", "读计划、判断统计信息、选索引并说明代价"],
    "exclusions": ["PostgreSQL 源码级优化器开发", "复杂多表连接调优"],
    "constraints": { "duration": "4周", "effort_per_period": "每周6小时", "environment": "PostgreSQL 18 沙箱" },
    "external_research_seed": {
      "search_executed": true,
      "retrieval_date": "2026-07-26",
      "queries": ["PostgreSQL 18 EXPLAIN ANALYZE", "composite index order selectivity", "PostgreSQL DBA JD slow query"],
      "sources": [
        { "evidence_id": "e-doc", "url": "https://www.postgresql.org/docs/18/sql-explain.html", "provenance": "external_evidence" },
        { "evidence_id": "e-jd", "url": "https://example.invalid/jd-postgres-dba", "provenance": "market_signal" }
      ],
      "category_coverage": [
        { "category": "wikipedia_encyclopedia", "status": "covered", "reason": "术语与相邻概念已查", "gate_effect": "none" },
        { "category": "official_academic", "status": "covered", "reason": "PostgreSQL 18 官方文档", "gate_effect": "none" },
        { "category": "recruiting_jd", "status": "covered", "reason": "3 个岗位样本", "gate_effect": "none" },
        { "category": "interview_selection", "status": "covered", "reason": "实操调试样本", "gate_effect": "none" },
        { "category": "adversarial_frontier", "status": "not_applicable", "reason": "单表索引优化非争议前沿", "gate_effect": "none" }
      ]
    },
    "open_questions": ["是否需要后续覆盖连接查询"],
    "confirmed_items": ["目标版本=PostgreSQL 18", "仅沙箱、无生产变更", "三题未见查询验收"]
  }
}
```

**门 G1 裁决（嵌入信封 `quality_evaluation`）**：`verdict=pass`、`route_to=S2`。每项能力均有可观察证据；验收任务要求未见/迁移；强制类别已覆盖；沙箱/排除边界明确；确认 `confirmed`。

**完整信封包裹要点**：`status=completed`，`confirmation.status=confirmed`，`traceability.fixture_type=simulated_fixture`，`evidence_collected` 中模型知识仅标 `model_hypothesis`、检索来源标 `external_evidence`/`market_signal`。

## 示例 B（反向/阻塞）— 七天成为 AI 专家

**来源追溯**：`docs/chat_log/七步个性化学习SOP正反例与研究依据.md` §S1 反向例子（line 165）。

**输入事实**：诉求“七天成为AI专家”；未执行联网预检，仅凭模型记忆生成。

**为何 G1 失败（不产出正向工件）**

- `target_problem` 无可观察定义（“专家”）；学习时长非能力；纯选择题无法验证迁移；无场景/范围/边界。
- `external_research_seed.search_executed=false` → 状态 `blocked`，不进入 S2。
- `positive_artifact=null`；`quality_evaluation.verdict=blocked`，`route_to=S1`；至少一项量规 `passed=false` 且带 `failure_action=revise_here`。

**门 G1 裁决**：`blocked`、`route_to=S1`。
