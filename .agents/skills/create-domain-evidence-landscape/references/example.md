# S2 示例 — domain_evidence_landscape

> 下列为**设计夹具**，不是真实观察结果。它们演示包契约（输入 → 正向工件 → 门裁决 → 路由）并附带来源章节追溯；eval 执行时不注入执行器提示。`fixture_type` 显式标注为 `simulated_fixture`。

## 示例 A（正向）— PostgreSQL 18 查询优化领域取证

**来源追溯**：`docs/chat_log/七步个性化学习SOP正反例与研究依据.md` §S2 正向例子 1（line 192）；端到端设计案例 `docs/chat_log/七步个性化学习SOP贯穿案例-PostgreSQL查询优化.md` §S2（line 187）；SOP 合同 `docs/chat_log/个性化学习SOP步骤拆分最终结论.md` §S2（line 199）、§S1–S2 强制外部研究原则（line 131）、§8.2（line 626）。

**输入事实**

- 上游：`goal_success_contract` 已通过 G1，目标=PostgreSQL 18 沙箱内独立诊断单表慢查询并验证；排除优化器内核与多表连接调优。
- 范围：PostgreSQL 18 单表查询、B-tree、多列/部分/覆盖索引、统计信息与 `EXPLAIN (ANALYZE, BUFFERS)`。
- 地区/场景：中国互联网中级后端工程师；仅沙箱；无生产变更。
- 取证标准：产品行为以 PostgreSQL 18 官方文档为主；教学策略另用学习科学研究。

**正向工件 `domain_evidence_landscape`（即 `positive_artifact`，校验通过 `domain-evidence-landscape.schema.json`）**

```json
{
  "type": "domain_evidence_landscape",
  "schema_version": "1.0.0",
  "artifact_id": "del-pg-0001",
  "content": {
    "scope": {
      "topic": "PostgreSQL 18 单表查询性能诊断与 B-tree 索引决策",
      "region_language": "zh-CN 学习者；产品事实以 PostgreSQL 18 官方英文文档为锚",
      "time_boundary": "2026-07-26 检索；PostgreSQL 18 当前稳定版行为",
      "role_or_scene": "中级后端工程师在沙箱内诊断脱敏的真实形状查询"
    },
    "terminology": [
      { "term": "EXPLAIN (ANALYZE, BUFFERS)", "meaning": "展示查询计划树，ANALYZE 实际执行查询并报告真实行数、时间和缓冲区；估算与实际分开", "evidence_refs": ["E-PG-EXPLAIN", "E-WIKI-EXPLAIN"] },
      { "term": "代价（cost）", "meaning": "计划器对候选计划相对代价的估算，不是运行毫秒", "evidence_refs": ["E-PG-EXPLAIN"] },
      { "term": "顺序扫描（Seq Scan）", "meaning": "整表顺序读取；对小表或返回大比例行时可能优于索引", "evidence_refs": ["E-PG-INDEXES", "E-CRIT-1"] },
      { "term": "index-only scan", "meaning": "仅从索引返回所需列，依赖可见性图且查询列被索引覆盖", "evidence_refs": ["E-PG-INDEXONLY"] },
      { "term": "选择性（selectivity）", "meaning": "谓词过滤掉行的比例的估计；影响索引收益判断", "evidence_refs": ["E-PG-STATS"] },
      { "term": "部分索引（partial index）", "meaning": "带谓词的索引；只有查询条件可蕴含该谓词时才可用", "evidence_refs": ["E-PG-PARTIAL"] }
    ],
    "research_executed": true,
    "research_run_manifest": {
      "online": true,
      "execution_status": "completed",
      "started_at": "2026-07-26T09:00:00+08:00",
      "completed_at": "2026-07-26T11:30:00+08:00",
      "rounds": 3,
      "perspectives": [
        { "id": "P1", "name": "terminology_history", "questions": ["EXPLAIN 与 ANALYZE 的语义边界是什么？", "代价、行数估算与真实执行的区别？"], "query_ids": ["Q1"] },
        { "id": "P2", "name": "theory_standards", "questions": ["PostgreSQL 18 计划器如何选择扫描与索引？", "多列 B-tree 的前导列约束规则？"], "query_ids": ["Q1", "Q2", "Q5"] },
        { "id": "P3", "name": "practice_tasks", "questions": ["真实慢查询排查的工作流是什么？", "索引是否一定带来净收益？"], "query_ids": ["Q3", "Q6"] },
        { "id": "P4", "name": "recruiting_market", "questions": ["当前 PostgreSQL DBA JD 重复要求哪些任务与工具？", "职级与背景筛选条件？"], "query_ids": ["Q4"] },
        { "id": "P5", "name": "interview_assessment", "questions": ["面试/实操如何观察查询优化能力？", "题型与目标认知层级？"], "query_ids": ["Q4"] },
        { "id": "P6", "name": "criticism_frontier", "questions": ["哪些常见优化口诀与官方文档冲突？", "版本相关的新行为（如 skip scan）？"], "query_ids": ["Q2", "Q6"] }
      ],
      "queries": [
        { "query_id": "Q1", "query": "PostgreSQL 18 EXPLAIN ANALYZE BUFFERS official documentation", "executed_at": "2026-07-26T09:10:00+08:00", "result_summary": "命中 PostgreSQL 18 Using EXPLAIN 与 Wikipedia EXPLAIN 条目", "follow_up_of": null },
        { "query_id": "Q2", "query": "PostgreSQL 18 multicolumn B-tree index leading column selectivity", "executed_at": "2026-07-26T09:35:00+08:00", "result_summary": "命中 Multicolumn Indexes 官方章节与一条实践复盘", "follow_up_of": "Q1" },
        { "query_id": "Q3", "query": "PostgreSQL partial index predicate implication query matcher", "executed_at": "2026-07-26T09:55:00+08:00", "result_summary": "命中 Partial Indexes 官方章节", "follow_up_of": "Q1" },
        { "query_id": "Q4", "query": "PostgreSQL DBA slow query optimization JD 2026 China", "executed_at": "2026-07-26T10:20:00+08:00", "result_summary": "三个去重岗位样本，覆盖两个组织", "follow_up_of": null },
        { "query_id": "Q5", "query": "PostgreSQL 18 index-only scan visibility map covering index", "executed_at": "2026-07-26T10:45:00+08:00", "result_summary": "命中 Index-Only Scans 与 Planner Statistics 官方章节", "follow_up_of": "Q2" },
        { "query_id": "Q6", "query": "when sequential scan beats index PostgreSQL small table large fraction", "executed_at": "2026-07-26T11:15:00+08:00", "result_summary": "命中批评性文章，反驳 INDEX_ALWAYS_FASTER 口诀", "follow_up_of": "Q1" }
      ],
      "follow_up_triggers": [
        "Q1 揭示估算 vs 实际行数区分，触发 Q2/Q3 追问索引必要条件",
        "Q2 提及 skip scan，触发 Q5 追问 index-only 边界",
        "INDEX_ALWAYS_FASTER 口诀与官方文档冲突，触发 Q6 反方检索"
      ]
    },
    "source_ledger": [
      { "evidence_id": "E-WIKI-EXPLAIN", "url": "https://en.wikipedia.org/wiki/Query_plan", "title": "Query plan (Wikipedia)", "publisher": "Wikipedia", "source_category": "wikipedia_encyclopedia", "published_at": null, "retrieved_at": "2026-07-26T09:12:00+08:00", "region": null, "reliability": "medium", "provenance": "external_evidence", "applicability": "全景入口与术语线索，不单独支撑产品行为结论" },
      { "evidence_id": "E-PG-EXPLAIN", "url": "https://www.postgresql.org/docs/18/using-explain.html", "title": "PostgreSQL 18: Using EXPLAIN", "publisher": "PostgreSQL Global Development Group", "source_category": "official_academic", "published_at": "2025-09-09", "retrieved_at": "2026-07-26T09:11:00+08:00", "region": null, "reliability": "high", "provenance": "external_evidence", "applicability": "产品行为一手事实；版本=PostgreSQL 18" },
      { "evidence_id": "E-PG-INDEXES", "url": "https://www.postgresql.org/docs/18/indexes.html", "title": "PostgreSQL 18: Indexes Overview", "publisher": "PostgreSQL Global Development Group", "source_category": "official_academic", "published_at": "2025-09-09", "retrieved_at": "2026-07-26T09:30:00+08:00", "region": null, "reliability": "high", "provenance": "external_evidence", "applicability": "索引开销与适用边界的一手依据" },
      { "evidence_id": "E-PG-MULTI", "url": "https://www.postgresql.org/docs/18/indexes-multicolumn.html", "title": "PostgreSQL 18: Multicolumn Indexes", "publisher": "PostgreSQL Global Development Group", "source_category": "official_academic", "published_at": "2025-09-09", "retrieved_at": "2026-07-26T09:36:00+08:00", "region": null, "reliability": "high", "provenance": "external_evidence", "applicability": "多列 B-tree 前导列规则的一手依据" },
      { "evidence_id": "E-PG-PARTIAL", "url": "https://www.postgresql.org/docs/18/indexes-partial.html", "title": "PostgreSQL 18: Partial Indexes", "publisher": "PostgreSQL Global Development Group", "source_category": "official_academic", "published_at": "2025-09-09", "retrieved_at": "2026-07-26T09:56:00+08:00", "region": null, "reliability": "high", "provenance": "external_evidence", "applicability": "部分索引谓词蕴含条件的一手依据" },
      { "evidence_id": "E-PG-INDEXONLY", "url": "https://www.postgresql.org/docs/18/indexes-index-only-scans.html", "title": "PostgreSQL 18: Index-Only Scans", "publisher": "PostgreSQL Global Development Group", "source_category": "official_academic", "published_at": "2025-09-09", "retrieved_at": "2026-07-26T10:46:00+08:00", "region": null, "reliability": "high", "provenance": "external_evidence", "applicability": "index-only scan 可见性图与覆盖条件的一手依据" },
      { "evidence_id": "E-PG-STATS", "url": "https://www.postgresql.org/docs/18/planner-stats.html", "title": "PostgreSQL 18: Planner Statistics", "publisher": "PostgreSQL Global Development Group", "source_category": "official_academic", "published_at": "2025-09-09", "retrieved_at": "2026-07-26T10:48:00+08:00", "region": null, "reliability": "high", "provenance": "external_evidence", "applicability": "行数估算与统计信息的一手依据；估算非精确计数" },
      { "evidence_id": "E-CASE-1", "url": "https://example.invalid/pg-slow-query-postmortem", "title": "一次生产慢查询误判复盘：盲目加索引导致写入劣化", "publisher": "工程博客（署名实践者）", "source_category": "practice_case", "published_at": "2025-11-12", "retrieved_at": "2026-07-26T10:05:00+08:00", "region": "cn", "reliability": "medium", "provenance": "external_evidence", "applicability": "个案经验，不得伪装成普遍规律" },
      { "evidence_id": "E-JD-1", "url": "https://example.invalid/jd-postgres-dba-org-a", "title": "PostgreSQL DBA 岗位（组织A）", "publisher": "组织A 招聘页", "source_category": "recruiting_jd", "published_at": "2026-06-10", "retrieved_at": "2026-07-26T10:22:00+08:00", "region": "cn", "reliability": "medium", "provenance": "market_signal", "applicability": "市场样本，非科学事实；区分任务/能力/背景筛选" },
      { "evidence_id": "E-JD-2", "url": "https://example.invalid/jd-postgres-dba-org-a-senior", "title": "高级 PostgreSQL DBA 岗位（组织A，高级）", "publisher": "组织A 招聘页", "source_category": "recruiting_jd", "published_at": "2026-06-22", "retrieved_at": "2026-07-26T10:23:00+08:00", "region": "cn", "reliability": "medium", "provenance": "market_signal", "applicability": "市场样本；与 E-JD-1 去重后视为同一组织的两个职级" },
      { "evidence_id": "E-JD-3", "url": "https://example.invalid/jd-postgres-dba-org-b", "title": "PostgreSQL DBA 岗位（组织B）", "publisher": "组织B 招聘页", "source_category": "recruiting_jd", "published_at": "2026-07-01", "retrieved_at": "2026-07-26T10:24:00+08:00", "region": "cn", "reliability": "medium", "provenance": "market_signal", "applicability": "第二个独立组织样本" },
      { "evidence_id": "E-IV-1", "url": "https://example.invalid/take-home-postgres-debug", "title": "公开 take-home：诊断给定慢查询并出具方案", "publisher": "某公司公开面试样题", "source_category": "interview_selection", "published_at": "2025-04-02", "retrieved_at": "2026-07-26T10:30:00+08:00", "region": "cn", "reliability": "medium", "provenance": "external_evidence", "applicability": "评估样题；用于设计诊断线索，不直接当教学答案" },
      { "evidence_id": "E-IV-2", "url": "https://example.invalid/interview-explain-walkthrough", "title": "面经：解读 EXPLAIN ANALYZE 计划节点", "publisher": "社区面经聚合", "source_category": "interview_selection", "published_at": "2025-08-19", "retrieved_at": "2026-07-26T10:31:00+08:00", "region": "cn", "reliability": "low", "provenance": "external_evidence", "applicability": "第二组独立样本；低可信度，仅作题型线索" },
      { "evidence_id": "E-CRIT-1", "url": "https://example.invalid/critique-index-always-faster", "title": "反驳：索引并非总比顺序扫描快", "publisher": "数据库批评博客", "source_category": "adversarial_frontier", "published_at": "2025-12-05", "retrieved_at": "2026-07-26T11:16:00+08:00", "region": null, "reliability": "medium", "provenance": "external_evidence", "applicability": "反方观点；与官方文档交叉验证后采纳" }
    ],
    "category_coverage": [
      { "category": "wikipedia_encyclopedia", "status": "covered", "reason": "EXPLAIN/查询计划术语与相邻概念已查", "criticality": "minor", "gate_effect": "none", "sample_count": 1 },
      { "category": "official_academic", "status": "covered", "reason": "PostgreSQL 18 官方文档 6 章节", "criticality": "critical", "gate_effect": "none", "sample_count": 6 },
      { "category": "practice_case", "status": "covered", "reason": "署名实践者复盘", "criticality": "material", "gate_effect": "none", "sample_count": 1 },
      { "category": "recruiting_jd", "status": "covered", "reason": "3 个去重岗位样本、2 个组织", "criticality": "material", "gate_effect": "none", "sample_count": 3 },
      { "category": "interview_selection", "status": "covered", "reason": "2 组独立样本（take-home + 面经）", "criticality": "material", "gate_effect": "none", "sample_count": 2 },
      { "category": "adversarial_frontier", "status": "covered", "reason": "反驳 INDEX_ALWAYS_FASTER 口诀的反方来源", "criticality": "material", "gate_effect": "none", "sample_count": 1 }
    ],
    "core_questions_and_mental_models": {
      "core_questions": [
        "PostgreSQL 计划器基于什么选择扫描与索引？",
        "EXPLAIN 能观察什么，ANALYZE 能证明什么，二者都不能证明什么？",
        "多列、部分与覆盖索引各自的必要条件是什么？",
        "什么时候顺序扫描比索引合理？",
        "估算行数与实际行数何时背离，原因是什么？"
      ],
      "mental_models": [
        { "model": "计划器是估算代价的比较器", "description": "计划器比较候选计划的估算代价，而不是执行全部计划后再选；估算依赖统计信息", "evidence_refs": ["E-PG-EXPLAIN", "E-PG-STATS"] },
        { "model": "索引适用性是多因素联合判断", "description": "索引适用性由查询形状、数据分布、排序、返回比例与读写代价共同决定，不能从存在 WHERE 直接推出应建索引", "evidence_refs": ["E-PG-INDEXES", "E-CRIT-1"] },
        { "model": "EXPLAIN 观察计划，ANALYZE 提供一次真实执行", "description": "EXPLAIN 显示计划树；ANALYZE 执行查询并报告真实行数与时间，但仍受测量情境影响", "evidence_refs": ["E-PG-EXPLAIN"] }
      ]
    },
    "jd_capability_matrix": [
      { "task": "诊断生产慢查询并给出可验证改进", "capability": "读取 EXPLAIN (ANALYZE, BUFFERS) 并定位瓶颈", "skill": "计划节点解读、估算 vs 实际对比", "tool": "EXPLAIN、pg_stat_statements", "background": "中级后端或 DBA", "evidence_refs": ["E-JD-1", "E-JD-2", "E-JD-3"] },
      { "task": "设计并论证索引方案", "capability": "区分单列/多列/部分/覆盖索引并说明代价", "skill": "选择性估计、谓词蕴含判断", "tool": "CREATE INDEX、REINDEX", "background": "中级后端或 DBA", "evidence_refs": ["E-JD-1", "E-JD-3"] },
      { "task": "评估写入与空间成本", "capability": "权衡读取收益与写入/空间开销", "skill": "工作量画像", "tool": "pg_stat_user_indexes", "background": "中级后端或 DBA", "evidence_refs": ["E-JD-2", "E-CASE-1"] }
    ],
    "interview_assessment_matrix": [
      { "type": "take-home", "capability": "对给定慢查询独立出具诊断、方案与验证", "level": "应用/诊断", "credibility": "medium", "evidence_refs": ["E-IV-1"] },
      { "type": "口头讲解", "capability": "逐节点解读 EXPLAIN ANALYZE 计划", "level": "解释", "credibility": "low", "evidence_refs": ["E-IV-2"] }
    ],
    "consensus": [
      { "statement": "优化前必须先有基线计划与真实测量", "evidence_refs": ["E-PG-EXPLAIN", "E-CASE-1"] },
      { "statement": "对比估算行数与实际行数以发现统计或分布问题", "evidence_refs": ["E-PG-EXPLAIN", "E-PG-STATS"] },
      { "statement": "索引设计必须同时说明读取收益与写入/空间成本", "evidence_refs": ["E-PG-INDEXES", "E-CASE-1"] }
    ],
    "disagreements": [
      {
        "issue": "是否应默认按“等值列在前、范围列在后”建立多列索引？",
        "side_a": { "position": "默认遵循该顺序规则作为起点", "strong_arguments": ["官方文档说明多列 B-tree 通常在前导列有约束时最有效", "规则简单、可教学"], "evidence_refs": ["E-PG-MULTI"] },
        "side_b": { "position": "先测量再决定，警惕把经验规则当绝对定律", "strong_arguments": ["PostgreSQL 18 可能使用 skip scan，旧行为口诀未必成立", "真实数据分布未知时默认建索引会引入写入成本"], "evidence_refs": ["E-CRIT-1", "E-CASE-1"] },
        "status": "partial_resolution"
      },
      {
        "issue": "EXPLAIN ANALYZE 是否可视为只读安全操作？",
        "side_a": { "position": "可视为只读，因为目的是观察", "strong_arguments": ["课程与面经常把它作为只读练习", "对纯 SELECT 不会改数据"], "evidence_refs": ["E-IV-2"] },
        "side_b": { "position": "对写操作会真实执行副作用，不可一概视为只读", "strong_arguments": ["ANALYZE 会实际执行被解释的语句", "对 UPDATE/DELETE/INSERT 会改数据"], "evidence_refs": ["E-PG-EXPLAIN"] },
        "status": "partial_resolution"
      }
    ],
    "open_problems": [
      { "problem": "案例业务数据的真实联合分布（如 status 与 tenant_id 的相关性）未采集", "why_it_matters": "选择性估计与索引收益高度依赖数据分布；缺失则只能给条件化结论", "evidence_refs": ["E-PG-STATS"] },
      { "problem": "高频更新表的可见性图状态与写入速率未知", "why_it_matters": "影响 index-only scan 是否真能获得预期收益", "evidence_refs": ["E-PG-INDEXONLY"] }
    ],
    "claims": [
      { "claim_id": "C1", "statement": "查询计划是树状节点，节点显示扫描、连接、排序等操作", "status": "supported", "claim_type": "fact", "evidence_refs": ["E-PG-EXPLAIN", "E-WIKI-EXPLAIN"], "limits": ["具体 cost 与行数依数据与环境变化"] },
      { "claim_id": "C2", "statement": "EXPLAIN ANALYZE 会实际执行查询并报告真实行数与时间", "status": "supported", "claim_type": "fact", "evidence_refs": ["E-PG-EXPLAIN"], "limits": ["对写操作有副作用；案例仅在沙箱使用"] },
      { "claim_id": "C3", "statement": "索引可加速检索，也会增加系统开销", "status": "supported", "claim_type": "fact", "evidence_refs": ["E-PG-INDEXES", "E-CASE-1"], "limits": ["不能从存在 WHERE 直接推出应建索引"] },
      { "claim_id": "C4", "statement": "多列 B-tree 通常在前导列有约束时最有效", "status": "supported", "claim_type": "fact", "evidence_refs": ["E-PG-MULTI"], "limits": ["PostgreSQL 18 skip scan 等新行为可能改变边界"] },
      { "claim_id": "C5", "statement": "部分索引只有在查询条件可蕴含其谓词时才可用", "status": "supported", "claim_type": "fact", "evidence_refs": ["E-PG-PARTIAL"], "limits": ["参数化谓词与表达式写法会影响可识别性"] },
      { "claim_id": "C6", "statement": "所有慢查询都应优先创建索引", "status": "unsupported", "claim_type": "practice", "evidence_refs": ["E-CRIT-1", "E-PG-INDEXES"], "limits": ["与小表、返回大比例行或写入密集场景冲突"] },
      { "claim_id": "C7", "statement": "EXPLAIN 中的 cost 等于运行毫秒", "status": "unsupported", "claim_type": "inference", "evidence_refs": ["E-PG-EXPLAIN"], "limits": ["cost 是相对估算，不是时间单位"] },
      { "claim_id": "C8", "statement": "当前市场重复要求 PostgreSQL DBA 能独立诊断慢查询并论证索引", "status": "partially_supported", "claim_type": "market_signal", "evidence_refs": ["E-JD-1", "E-JD-2", "E-JD-3"], "limits": ["JD 是市场样本且会变化；组织间定义不同"] }
    ],
    "evidence_gaps": [
      { "gap_id": "G1", "description": "未采集目标业务真实数据分布与缓存状态", "criticality": "material", "gate_effect": "lower_confidence", "confidence_impact": "medium" },
      { "gap_id": "G2", "description": "面试/选拔样本中公开面经可信度偏低，仅有 1 组高可信 take-home", "criticality": "minor", "gate_effect": "none", "confidence_impact": "low" }
    ]
  }
}
```

**门 G2 裁决（嵌入信封 `quality_evaluation`）**：`verdict=pass`、`route_to=S3`。`research_run_manifest` 证明 3 轮联网多视角研究已实际执行；六类强制来源类别均为 `covered`，招聘达 3 样本/2 组织、面试达 2 组独立样本；C1–C5 关键产品事实均可追溯到 PostgreSQL 18 官方文档，C6/C7 反口诀标记为 `unsupported`；两处重要争议保留双方强论据；市场信号（C8）与产品事实分开；缺口 G1/G2 透明且不阻塞建图。

**完整信封包裹要点**：`status=completed`，`confirmation.status=confirmed`（条件确认升级为强制：存在 INDEX_ALWAYS_FASTER 争议），`traceability.fixture_type=simulated_fixture`，`evidence_collected` 中模型知识仅标 `model_hypothesis`、检索来源按类别标 `external_evidence`/`market_signal`。

## 示例 B（反向/阻塞）— 搜索前三篇博客即宣布共识

**来源追溯**：`docs/chat_log/七步个性化学习SOP正反例与研究依据.md` §S2 反向例子（line 266）。

**输入事实**：用户给出三篇互相转载的 SEO 博客、一个培训广告、一篇无作者转载，要求不再搜索，直接断言“所有慢查询都应建索引、cost 就是毫秒”，并把缺失的一手资料标为不适用。

**为何 G2 失败（不产出正向工件）**

- 没有 `research_run_manifest`：`online=false` 或 `execution_status=not_executed`，没有可追溯的查询清单、视角与追问；`research_executed=false` → G2 失败。
- 来源不独立（同源转载），无版本与纳入排除规则；与 PostgreSQL 官方文档关于索引开销、成本估算与小表顺序扫描的说明冲突。
- 未记录冲突与不确定性；缺失的官方/学术类别必须标为 `gap`，不能写成 `not_applicable`。
- `positive_artifact=null`；`quality_evaluation.verdict=revise_here`，`route_to=S2`；至少一项量规 `passed=false` 且带 `failure_action=revise_here`。

**门 G2 裁决**：`revise_here`、`route_to=S2`。禁止把该结果送入 S3，否则图谱会把“所有慢查询都应建索引”这类错误规则建成硬先修。
