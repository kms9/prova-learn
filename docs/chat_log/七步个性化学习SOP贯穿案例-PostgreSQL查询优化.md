# 七步个性化学习 SOP 贯穿案例：PostgreSQL 查询优化

> 案例类型：从模糊学习诉求到掌握验证与重规划的完整设计样例  
> 对应 SOP：[个性化学习SOP步骤拆分最终结论.md](./个性化学习SOP步骤拆分最终结论.md)  
> 正反例集合：[七步个性化学习SOP正反例与研究依据.md](./七步个性化学习SOP正反例与研究依据.md)

## 1. 案例边界

### 1.1 学习者初始诉求

> “我会写 SQL，但遇到 PostgreSQL 慢查询只会试着加索引。希望四周内能自己看执行计划并做优化。”

### 1.2 重要声明

- 这是用来检验 SOP 完整性的**设计案例**；
- 表规模、执行计划、学习者回答、得分和时间均为案例夹具，不是实际运行结果；
- PostgreSQL 产品行为以 2026-07-26 检索到的 PostgreSQL 18 当前官方文档为依据；
- 任何 `EXPLAIN ANALYZE`、建索引或统计信息变更都限定在沙箱中；
- 本案例不把单次变快视为普遍有效，真实优化必须在真实数据分布和工作负载上重新测量。

## 2. 案例对象

### 2.1 沙箱表

```sql
CREATE TABLE orders (
    id          bigint PRIMARY KEY,
    tenant_id   bigint NOT NULL,
    customer_id bigint NOT NULL,
    status      text NOT NULL,
    created_at  timestamptz NOT NULL,
    total       numeric(12, 2) NOT NULL
);

CREATE INDEX orders_tenant_id_idx ON orders (tenant_id);
CREATE INDEX orders_status_idx ON orders (status);
```

案例假设：

- `orders` 有约 2,000 万行；
- 数据按租户和状态分布不均匀；
- 表持续写入；
- 现有索引只有 `tenant_id` 和 `status` 两个单列索引。

### 2.2 目标查询

```sql
SELECT id, created_at, total
FROM orders
WHERE tenant_id = 42
  AND status = 'paid'
ORDER BY created_at DESC
LIMIT 50;
```

### 2.3 案例基线计划

以下是用于教学的简化计划形状，不是实际 PostgreSQL 输出：

```text
Limit
└─ Sort
   Sort Key: created_at DESC
   └─ Bitmap Heap Scan on orders
      Recheck Cond: tenant_id = 42
      Filter: status = 'paid'
      Rows Removed by Filter: many
      └─ Bitmap Index Scan on orders_tenant_id_idx
         Index Cond: tenant_id = 42
```

该计划夹具用于引出三个问题：

1. 过滤和排序发生在哪里；
2. 多列 B-tree 能否同时服务等值谓词与排序；
3. 是否值得加入 `INCLUDE`，以及持续写入对 index-only scan 的影响。

---

## S1. 目标与成功契约

### 3.1 输入契约校验

```yaml
input:
  learner_request: 会写SQL，但慢查询只会尝试加索引
  time_budget: 四周，每周约6小时
  existing_materials:
    - 一条真实业务形状的脱敏查询
validation:
  status: pass
  missing:
    - PostgreSQL版本
    - 是否有沙箱
    - 是否允许执行ANALYZE和创建索引
    - “学会”的验收形式
```

### 3.2 需求信息收集

系统补问：

1. 使用哪个 PostgreSQL 版本？
2. 目标是单表查询、连接、聚合还是全部？
3. 是否需要修改生产库？
4. 期望能执行哪些实际动作？
5. 如何证明不是照着示例复现？

学习者回答：

- PostgreSQL 18；
- 先覆盖单表查询和索引，不要求复杂连接；
- 有独立沙箱，无生产变更权限；
- 希望能读计划、判断统计信息问题、选择索引并说明代价；
- 可以接受三个未见查询的最终项目。

### 3.3 确认交互

```yaml
confirmation:
  mode: mandatory
  proposed_scope:
    included:
      - EXPLAIN与EXPLAIN ANALYZE
      - 估算行数与实际行数
      - B-tree及多列、部分、覆盖索引
      - planner statistics
      - 改动前后验证
    excluded:
      - 优化器源码
      - 复杂连接重排
      - 生产变更
  learner_response: confirmed
  status: confirmed
```

### 3.4 正向输出：`goal_success_contract`

```yaml
artifact_id: GSC-001
target_problem: 在PostgreSQL 18沙箱中独立诊断并改进常见单表慢查询
observable_capabilities:
  C1: 从计划树定位扫描、过滤、排序和Limit
  C2: 区分估算与实际数据，并判断何时检查统计信息
  C3: 根据谓词、排序和数据分布选择或拒绝索引
  C4: 解释多列、部分和覆盖索引的适用条件与代价
  C5: 在保持查询语义一致的前提下验证改动
final_assessment:
  fixture_count: 3
  conditions:
    - 查询与训练示例表面特征不同
    - 至少一个正确答案是拒绝新增索引
    - 至少一个需要识别统计信息问题
required_evidence:
  - 独立的计划标注
  - 主瓶颈与依据
  - 候选方案及拒绝方案
  - 沙箱验证设计
  - 写入、空间、维护和回滚说明
pass_rule:
  - 3个夹具中至少2个完整通过
  - C1-C5均至少有一项独立证据
  - 不把cost解释为毫秒
  - 不执行越权变更
constraints:
  duration: 4周
  effort: 每周6小时
```

### 3.5 S1 质量门

| 维度 | 结果 | 证据 |
|---|---|---|
| 可观察性 | 通过 | C1–C5 均对应实际行为 |
| 目标—评价对齐 | 通过 | 最终项目要求诊断、取舍和验证 |
| 边界 | 通过 | 限定版本、单表、沙箱和非生产 |
| 用户确认 | 通过 | 强制确认已完成 |

```yaml
quality_verdict: pass
route_to: S2
```

---

## S2. 领域取证与认知全景

### 4.1 输入契约校验

`GSC-001` 已通过 G1；版本、范围和安全边界明确。

### 4.2 取证计划

```yaml
focus_questions:
  - PostgreSQL计划器基于什么选择计划？
  - EXPLAIN能观察什么，不能证明什么？
  - 多列、部分和覆盖索引分别有哪些必要条件？
  - 什么时候顺序扫描可能比索引合理？
source_policy:
  product_behavior: PostgreSQL 18官方文档
  learning_design: 国家级研究报告、政府实践指南、同行评审论文
excluded_sources:
  - 无版本博客作为产品真值
  - 只给结论、不说明数据分布的性能截图
```

### 4.3 证据收集与结论映射

| 结论 | 证据 | 适用边界 |
|---|---|---|
| 查询计划是树，节点显示扫描、连接、排序等操作 | [PostgreSQL：Using EXPLAIN][P1] | 具体成本和行数依数据与环境变化 |
| `EXPLAIN ANALYZE` 会实际执行并报告实际行数和时间 | [PostgreSQL：Using EXPLAIN][P1] | 对写操作必须特别谨慎；案例只在沙箱使用 |
| 索引可加速检索，也会增加系统开销 | [PostgreSQL：Indexes][P2] | 不能从“存在 WHERE”直接推出“应建索引” |
| 多列 B-tree 通常在前导列有约束时最有效 | [PostgreSQL：Multicolumn Indexes][P3] | PostgreSQL 18 还可能使用 skip scan，不能把旧口诀当绝对定律 |
| 部分索引只有在查询条件可蕴含索引谓词时才可用 | [PostgreSQL：Partial Indexes][P4] | 参数化谓词和表达式写法会影响可识别性 |
| index-only scan 还依赖查询列覆盖和可见性信息 | [PostgreSQL：Index-Only Scans][P5] | 高频更新表不一定获得预期收益 |
| 统计信息为行数估算和成本计算提供原料 | [PostgreSQL：Planner Statistics][P6] | 估算不是精确计数 |
| 学习目标、测评和教学活动必须对齐 | [CMU 对齐指南][L1] | 用于课程设计，不是 PostgreSQL 产品行为证据 |
| 评估需要认知、观察、解释三者闭合 | [National Academies assessment triangle][L2] | 用于设计诊断与掌握证据 |
| 检索、间隔、worked example 与深层问题有研究支持 | [IES 学习组织指南][L3] | 应按学习者和任务调整，不机械套用 |

### 4.4 正向输出：`domain_evidence_landscape`

```yaml
artifact_id: DEL-001
domain_scope:
  version: PostgreSQL 18
  focus: 单表计划、统计信息与B-tree索引决策
core_mental_models:
  - 计划器比较候选计划的估算代价，而不是执行所有计划后再选
  - 索引适用性由查询形状、数据分布、排序、返回比例和代价共同决定
  - EXPLAIN观察计划；ANALYZE提供一次真实执行证据，但仍需考虑测量情境
consensus:
  - 优化前先有基线
  - 对比估算与实际行数
  - 索引设计必须说明读取收益与写入/空间成本
critical_distinctions:
  - estimated_rows_vs_actual_rows
  - index_condition_vs_filter
  - possible_index_only_vs_beneficial_index_only
  - product_fact_vs_case_assumption
misconceptions:
  - INDEX_ALWAYS_FASTER
  - COST_EQUALS_MILLISECONDS
  - SELECTIVITY_FIRST_ALWAYS
  - EXPLAIN_ANALYZE_IS_READ_ONLY
unknowns:
  - 案例真实缓存状态
  - status与tenant_id的联合分布
  - 写入速率和可见性图状态
```

### 4.5 S2 质量门

- 产品结论都能追溯到 PostgreSQL 18 官方文档；
- 案例假设与官方事实分开；
- 记录了 PostgreSQL 18 skip scan 等版本相关边界；
- 记录未知数据分布，没有提前承诺具体索引收益。

```yaml
quality_verdict: pass
route_to: S3
```

---

## S3. 能力—概念图建模

### 5.1 输入契约校验

- `GSC-001` 已通过 G1；
- `DEL-001` 已通过 G2；
- 所有产品节点必须关联 P1–P6 中至少一个来源；
- S3 不新增未经 S2 审计的 PostgreSQL 事实。

### 5.2 能力反推

```text
最终能力：独立诊断并验证单表查询优化
├─需要判断：计划正在做什么
├─需要判断：计划器为什么这样估算
├─需要判断：哪个候选方案与查询形状匹配
├─需要判断：改动是否真的改善目标工作负载
└─需要判断：收益是否值得写入和空间代价
```

### 5.3 正向输出：`capability_concept_graph`

```yaml
artifact_id: CCG-001
goal_contract_ref: GSC-001
evidence_landscape_ref: DEL-001
focus_question: 学习者要依据什么证据选择并验证一个索引方案？
```

```text
[C1 读取计划]
├─硬先修→ [N1 计划树与节点]
├─硬先修→ [N2 Seq/Index/Bitmap Scan]
├─硬先修→ [N3 Index Cond / Filter / Recheck]
└─硬先修→ [N4 Sort / ORDER BY / LIMIT]

[C2 解释估算]
├─硬先修→ [N5 estimated vs actual]
├─硬先修→ [N6 selectivity / cardinality]
├─硬先修→ [N7 statistics / ANALYZE]
└─支持→ [N8 cost不是墙钟毫秒]

[C3 设计或拒绝索引]
├─硬先修→ [N9 B-tree比较与排序]
├─硬先修→ [N10 多列前导约束]
├─支持→ [N11 skip scan边界]
├─条件先修→ [N12 部分索引谓词蕴含]
└─条件先修→ [N13 覆盖列与index-only条件]

[C4 验证和取舍]
├─硬先修→ [N14 基线与对照]
├─硬先修→ [N15 语义一致]
├─硬先修→ [N16 读写空间代价]
└─硬先修→ [N17 复测与回滚]
```

节点契约示例：

```yaml
node_id: N10
name: multicolumn_btree_constraints
capability_statement: 给定谓词与排序，比较候选列顺序并解释扫描范围
source_refs: [P3]
prerequisites: [N6, N9]
misconceptions: [SELECTIVITY_FIRST_ALWAYS]
assessment:
  explain: 解释前导等值列和首个非等值列如何限制扫描
  apply: 为两个查询比较索引顺序
  transfer: 数据分布或谓词形状改变后重新判断
mastery_rule:
  independent_apply: 2/3
  transfer_required: true
  max_hint_level: 1
```

### 5.4 S3 质量门

| 检查 | 结果 |
|---|---|
| 目标能力都可追溯到节点 | 通过 |
| 每条关键边有类型和理由 | 通过 |
| 每个关键节点有评估和误解 | 通过 |
| 产品事实可追溯到 S2 | 通过 |
| 图谱无循环 | 通过 |

```yaml
quality_verdict: pass
route_to: S4
```

---

## S4. 学习者诊断与学习前沿

### 6.1 输入契约校验

- 图谱 G3 已通过；
- 诊断只使用 N1–N17 中的目标节点；
- 先定义推断规则，再收集回答；
- 自述只用于选题，不直接更新为“已掌握”。

### 6.2 诊断任务

| ID | 任务 | 观察目标 |
|---|---|---|
| D1 | 解释普通 `EXPLAIN` 与 `EXPLAIN ANALYZE` 的差别 | N5、执行安全 |
| D2 | 标注案例基线计划中的扫描、过滤、排序 | N1–N4 |
| D3 | 估算 1,000 行、实际 100,000 行时下一步查什么 | N5–N7 |
| D4 | 比较 `(tenant_id,status,created_at)` 与 `(status,tenant_id,created_at)` | N9–N11 |
| D5 | 判断参数化查询能否使用某部分索引 | N12 |
| D6 | 表持续写入时，`INCLUDE` 是否必然产生 index-only scan | N13、N16 |

### 6.3 学习者行为证据

```yaml
responses:
  D1:
    result: partial
    evidence: 知道ANALYZE显示实际时间，但认为不会产生副作用
    confidence: 0.9
  D2:
    result: pass
    evidence: 正确指出Bitmap Heap Scan后过滤并在Limit前排序
    hints: 0
  D3:
    result: partial
    evidence: 建议加索引，没有先检查统计信息和分布
    hints: 1
  D4:
    result: fail
    evidence: 声称全局选择性最高的status必须放第一列
    confidence: 0.8
  D5:
    result: fail
    evidence: 未识别谓词蕴含与参数化限制
  D6:
    result: fail
    evidence: 认为只要INCLUDE查询列就一定index-only
```

### 6.4 正向输出：`learner_snapshot`

```yaml
artifact_id: LS-001
learner_id: learner-demo-01
model_version: 1
mastered:
  N1: plan_tree
  N2: scan_type_recognition
  N3: condition_vs_filter_recognition
  N4: sort_and_limit_recognition
partial:
  N5: estimated_vs_actual
  N7: statistics_and_analyze
not_mastered:
  N10: multicolumn_constraints
  N12: partial_index_implication
  N13: index_only_conditions
  N16: maintenance_tradeoff
misconceptions:
  - EXPLAIN_ANALYZE_IS_READ_ONLY
  - SELECTIVITY_FIRST_ALWAYS
  - INCLUDE_GUARANTEES_INDEX_ONLY
learning_frontier:
  - N5
  - N6
  - N7
evidence_refs: [D1, D2, D3, D4, D5, D6]
confidence_calibration:
  status: overconfident_on_index_rules
```

### 6.5 确认交互

系统展示：

> “你已经能读基础计划，但会把局部规则当成绝对规则。建议从估算、统计信息和查询形状开始，而不是从创建索引语法开始。”

学习者确认：

> “符合我的实际情况；我确实常按选择性排序列。”

### 6.6 S4 质量门

- 每个状态有行为证据；
- 区分会识别、会解释和能迁移；
- 记录提示和置信度；
- 没有因 D2 通过就跳过全部计划分析。

```yaml
quality_verdict: pass
route_to: S5
```

---

## S5. 路径与会话规划

### 7.1 输入契约校验

`LS-001`、图谱和目标版本一致；学习前沿有 D1–D6 支持。

### 7.2 路径选择原则

- 跳过已掌握的计划树入门；
- 先修复估算与统计信息模型；
- 再学习多列索引；
- 部分索引和 index-only scan 作为条件扩展；
- 每周包含检索和实际计划；
- 最终必须出现“拒绝加索引”的案例。

### 7.3 正向输出：`learning_and_session_plan`

```yaml
artifact_id: LSP-001
duration: 4周
weekly_effort: 6小时
sessions:
  - id: W1S1
    focus: [N5, N6, N7, N8]
    title: 估算、实际行数与统计信息
    exit: 能根据估算偏差选择检查和验证动作
  - id: W1S2
    focus: [N1-N8综合]
    title: 从计划树形成证据链
    exit: 不用“cost=毫秒”等错误解释
  - id: W2S1
    focus: [N9, N10, N11]
    title: B-tree、多列约束与排序
    exit: 两个未见查询中独立通过一个，另一个最多一级提示
  - id: W2S2
    focus: [N9-N11迁移]
    title: 改变谓词与数据分布后的索引决策
    exit: 能拒绝机械“选择性最高列优先”
  - id: W3S1
    focus: [N12]
    title: 部分索引与谓词蕴含
    exit: 识别可用、不可用和参数化边界
  - id: W3S2
    focus: [N13, N16]
    title: 覆盖索引、可见性和写入代价
    exit: 能说明“可能index-only”与“实际有收益”的差别
  - id: W4S1
    focus: [N14-N17]
    title: 基线、语义、验证和回滚
    exit: 完成一个完整优化实验设计
  - id: W4S2
    focus: [C1-C5]
    title: 三个未见查询的最终项目
review:
  - 每次会话开头5分钟无材料检索
  - 关键节点次日和第4天复测
  - 最终项目前一周安排一次延迟检查
```

### 7.4 强制确认

学习者确认：

- 每周两个 90 分钟交互会话；
- 其余时间用于沙箱实验和复测；
- 同意先补统计信息模型，而不是立即学习更多索引语法。

### 7.5 S5 质量门

| 维度 | 结果 |
|---|---|
| 从学习前沿到目标连通 | 通过 |
| 无明显冗余 | 通过；跳过已掌握的基础语法 |
| 教学与测评对齐 | 通过 |
| 时间可行 | 通过；总量不超过约 24 小时 |
| 用户确认 | 通过 |

```yaml
quality_verdict: pass
route_to: S6
```

---

## S6. 内容生产与教学交互

本节完整展示 W2S1“多列索引与排序”会话。

### 8.1 输入契约校验

- W1S1、W1S2 已通过；
- 学习者能区分估算和实际行数；
- N9–N11 的产品事实来自 [PostgreSQL 多列索引文档][P3]；
- 会话不要求在生产环境创建索引。

### 8.2 会话目标

> 给定查询谓词、排序和案例数据分布，学习者能比较两个多列 B-tree 候选，解释前导约束、首个非等值条件与排序的关系，并在信息不足时要求测量。

### 8.3 内容包

#### A. 无材料检索

```text
问题：计划器为什么可能对同一张表选择顺序扫描、索引扫描或Bitmap扫描？
要求：先写自己的模型，不查资料。
```

学习者回答：

> “看返回行数；返回少就索引，返回多就顺序扫描。”

系统记录：模型方向基本正确，但缺少页面访问、排序、统计估算和查询形状。

#### B. worked example

查询：

```sql
SELECT id, created_at, total
FROM orders
WHERE tenant_id = 42
  AND status = 'paid'
ORDER BY created_at DESC
LIMIT 50;
```

候选：

```sql
-- 候选A
CREATE INDEX ON orders (tenant_id, status, created_at DESC);

-- 候选B
CREATE INDEX ON orders (status, tenant_id, created_at DESC);
```

示范推理：

1. 两个等值谓词都可参与候选索引；
2. 不能脱离工作负载只比较单列“全局选择性”；
3. `tenant_id` 是否是稳定前导过滤条件，取决于目标查询族；
4. `created_at` 的索引顺序可能服务 `ORDER BY ... LIMIT`；
5. 候选必须放到沙箱中比较计划、实际行数、缓冲访问和写入代价；
6. PostgreSQL 18 的 skip scan 意味着“没约束左列就永远完全不可用”也过于绝对，但不等于可以忽略前导列设计。

#### C. 半完成例题

```sql
SELECT id, created_at
FROM orders
WHERE tenant_id = 42
  AND status IN ('paid', 'refunded')
  AND created_at >= now() - interval '7 days'
ORDER BY created_at DESC;
```

要求学习者补完：

```text
等值条件：tenant_id
多值/范围条件：____
排序要求：____
需要确认的数据分布：____
候选索引及其主要代价：____
```

#### D. 对比例题

```sql
SELECT count(*)
FROM orders
WHERE status = 'paid';
```

问题：

> “为什么已有 `orders_status_idx` 也可能不值得使用？请给出需要观察的证据，不要只回答‘选择性低’。”

#### E. 独立迁移题

```sql
SELECT id, total
FROM orders
WHERE tenant_id = 42
  AND created_at >= now() - interval '30 days'
ORDER BY created_at DESC
LIMIT 100;
```

要求：

- 选择、修改或拒绝一个索引方案；
- 说明 `status` 不在谓词后，对原候选的影响；
- 写出沙箱验证步骤；
- 不提供即时答案。

### 8.4 提示与反馈轨迹

```yaml
trace:
  - event: learner_attempt
    claim: status全局选择性更高，所以候选B永远更好
  - event: hint_level_1
    prompt: 目标查询族是否总是先按tenant_id隔离？两个等值条件后还要服务什么排序？
  - event: learner_revision
    claim: 不能只看单列选择性；需要看查询族和排序，但我还不确定数据分布
  - event: feedback
    type: process
    content: 正确。把“需要确认的数据”列出，再决定候选；不要把不确定性藏起来。
```

### 8.5 正向输出：`session_package_and_trace`

```yaml
artifact_id: SPT-001
session_id: W2S1
content_sources: [P1, P2, P3]
activities:
  - retrieval
  - worked_example
  - completion_problem
  - contrast_case
  - independent_transfer
answer_leakage: false
learner_evidence:
  completed:
    - 能识别等值、范围和排序
    - 会要求数据分布与计划证据
  unresolved:
    - 数据分布改变时仍偶尔回到单列选择性口诀
candidate_mastery_evidence: [E-W2S1-1, E-W2S1-2]
```

### 8.6 S6 工件质量门

- 产品内容与官方文档一致；
- worked example 后有渐隐和独立题；
- 反馈针对推理过程，不直接给最终答案；
- 产生了可由 S7 解释的行为证据；
- 本门只说明“教学工件合格”，不说明“学习者已掌握”。

```yaml
quality_verdict: pass
route_to: S7
```

---

## S7. 掌握验证、模型更新与重规划

本阶段不使用“本次答对”直接替代长期掌握：[检索练习研究][L4]区分即时表现与延迟保持，[间隔学习综述][L5]支持把时间间隔纳入证据，[迁移分类研究][L6]要求说明任务、时间、情境和形式改变了什么，[知识追踪研究][L7]则支持根据连续行为更新而不是覆盖学习者状态。

### 9.1 输入契约校验

- `SPT-001` 已通过 G6；
- N10 的掌握门在会话前已确定；
- 学习者模型当前版本为 1；
- 证据事件和提示层级完整。

### 9.2 第一次掌握验证

| 维度 | 任务 | 结果 |
|---|---|---|
| 独立应用 | 与示例同结构、不同列名 | 通过 |
| 对比解释 | 比较两个列顺序 | 通过，使用一级提示 |
| 变化迁移 | 移除 `status` 条件 | 通过 |
| 数据分布迁移 | `status='paid'` 占比从 5% 变为 80% | 未通过；仍沿用原方案 |
| 延迟保持 | 三天后解释前导约束 | 通过 |

### 9.3 `mastery-verifier` 输出

```yaml
artifact_id: ME-001
learner_id: learner-demo-01
node_id: N10
claim:
  status: provisional_mastered
  independent_application: pass
  transfer: partial
  delayed_retention: pass
evidence_refs:
  - E-W2S1-1
  - E-W2S1-2
  - E-W2S1-T1
hint_dependency: 1
unresolved:
  - 数据分布变化后的重新测量与方案更新
primary_attribution: STRATEGY_OR_SEQUENCE
```

这里没有把 `provisional_mastered` 写成最终掌握，因为目标 C3 需要在分布改变时重新判断。

### 9.4 `learner-model-replanner` 原子更新

```yaml
update:
  learner_id: learner-demo-01
  expected_model_version: 1
  new_model_version: 2
  changes:
    N10: provisional_mastered
    N6: partial
    N7: partial
    misconception_SELECTIVITY_FIRST_ALWAYS: weakened_but_active
  evidence_refs: [ME-001]
route:
  attribution: STRATEGY_OR_SEQUENCE
  route_to: S5
  reason: 需要把统计信息与分布变化提前连接到索引决策
replan_patch:
  - 在W2S2前增加“同一查询、三种分布”对比
  - 把ANALYZE与估算偏差重新加入检索
  - 保留W3和W4总时长，压缩已通过的语法练习
```

更新采用 `expected_model_version=1`；若已有其他会话写入版本 2，本次必须报冲突，不能静默覆盖。

### 9.5 第二次 S5→S6→S7 循环

#### 路径补丁

```yaml
session: W2S2-R
contrast:
  - distribution: paid占5%
  - distribution: paid占50%
  - distribution: paid占80%
required_action:
  - 先预测计划
  - 检查统计信息
  - 运行沙箱基线
  - 允许正确答案为“拒绝新增索引”
```

#### 学习者新证据

- 能说明分布变化可能改变返回比例和计划选择；
- 能先检查估算与实际差异，再决定是否 `ANALYZE`；
- 在高返回比例案例中拒绝“为了使用索引而强制索引”；
- 一周后仍能独立完成。

#### 第二次掌握判定

```yaml
node_updates:
  N6: mastered
  N7: mastered
  N10: mastered
misconception_SELECTIVITY_FIRST_ALWAYS: remediated
model_version: 3
route_to: S6
next_session: W3S1
```

### 9.6 最终项目

W3S1–W4S1 继续完成部分索引、index-only scan、代价、验证和回滚节点；每次会话按同一 S6→S7 小循环写入证据，学习者模型从版本 3 依次更新到版本 7。下面的最终项目以版本 7 为输入，完成后写入版本 8。

四周末给出三个未见夹具：

#### 夹具 A：等值谓词加排序和 LIMIT

学习者：

- 正确标注过滤与排序；
- 提出 `(tenant_id, status, created_at DESC)` 候选；
- 将 `INCLUDE (id,total)` 作为需要结合写入和可见性验证的可选方案，而不是默认添加；
- 给出基线、候选、语义一致和回滚检查。

结果：通过。

#### 夹具 B：少量 `pending` 订单的高频后台任务

学习者：

- 根据工作负载提出部分索引候选；
- 检查查询条件能否蕴含索引谓词；
- 指出参数化表达可能导致不能识别部分索引；
- 要求验证数据分布是否稳定。

结果：通过。

#### 夹具 C：返回大比例历史订单

学习者：

- 没有机械创建索引；
- 解释为什么顺序扫描可能合理；
- 检查估算、实际行数和缓冲访问；
- 给出“保持现状并监控”的方案。

结果：通过。

### 9.7 最终正向输出：`mastery_and_replanning_bundle`

```yaml
artifact_id: MRP-001
learner_id: learner-demo-01
model_version: 8
goal_contract_ref: GSC-001
final_evidence:
  fixture_A: pass
  fixture_B: pass
  fixture_C: pass
capabilities:
  C1: mastered
  C2: mastered
  C3: mastered
  C4: mastered
  C5: mastered
delayed_check:
  status: pass
  interval: 一周
hint_dependency: 0
goal_status: achieved
route_to: complete
maintenance_plan:
  - 两周后对新的JOIN查询只做诊断，不扩展本轮目标
  - 一个月后复测一个数据分布显著变化的案例
  - 在真实业务中仍需重新建立基线，不复用案例性能数字
traceability:
  sources: [P1, P2, P3, P4, P5, P6]
  learner_evidence: [D1-D6, ME-001, W2S2-R, fixture_A, fixture_B, fixture_C]
```

### 9.8 S7 质量门

| 检查 | 结果 |
|---|---|
| 多维证据 | 通过：独立、对比、迁移、延迟 |
| 提示影响 | 通过：最终项目无提示 |
| 更新可追溯 | 通过：状态关联证据事件 |
| 路由可解释 | 通过：第一次返回 S5，第二次继续 S6 |
| 目标验收对齐 | 通过：C1–C5 均在未见夹具中出现 |
| 防止过度概括 | 通过：明确案例数字不能迁移到真实生产 |

```yaml
quality_verdict: pass
goal_status: achieved
route_to: complete
```

---

## 10. 七步移交总表

| 阶段 | 输入 | 正向工件 | 质量门 | 本例路由 |
|---|---|---|---|---|
| S1 | 模糊诉求和约束 | `GSC-001` | 目标可观察、可验收、已确认 | S2 |
| S2 | 目标契约 | `DEL-001` | 来源可靠、版本明确、事实与假设分开 | S3 |
| S3 | 目标与证据全景 | `CCG-001` | 节点、边、任务、来源可追溯 | S4 |
| S4 | 图谱和行为回答 | `LS-001` | 多任务证据支持学习前沿 | S5 |
| S5 | 学习者快照 | `LSP-001` | 最小路径、时间可行、已确认 | S6 |
| S6 | 当前会话计划 | `SPT-001` | 内容正确、支架渐隐、产生行为证据 | S7 |
| S7 首轮 | 交互证据和模型 v1 | `ME-001` 与模型 v2 | 迁移不足但归因正确 | 返回 S5 |
| S7 次轮 | 补救证据和更新模型 | 模型 v3 | 相关节点掌握 | 下一节点 S6 |
| S7 最终 | 三个未见夹具和延迟复测 | `MRP-001`、模型 v8 | C1–C5 全部有独立证据 | 完成 |

## 11. 这个案例证明了什么

1. 七步不是写七份文档，而是建立七个不同的错误隔离与质量门。
2. S2 的官方事实与 S3 的结构推断分开后，产品版本变化可以局部重做取证和受影响节点。
3. S4 避免了“会写 SQL 等于会优化 SQL”的错误推断。
4. S5 跳过已会内容，把时间投入真实学习前沿。
5. S6 的完成条件是产生学习者行为，不是教师输出结束。
6. S7 首轮没有通过全部迁移，但这正是形成性闭环的价值：正确返回 S5，而不是判定失败或假装掌握。
7. 顶层 S7 保持一个反馈事务，物理实现仍可拆成验证器和重规划器。
8. 最终掌握结论来自未见任务、迁移、延迟和零提示，不来自单次选择题。

## 12. 来源

[P1]: https://www.postgresql.org/docs/current/using-explain.html "PostgreSQL 18: Using EXPLAIN"
[P2]: https://www.postgresql.org/docs/current/indexes.html "PostgreSQL 18: Indexes"
[P3]: https://www.postgresql.org/docs/current/indexes-multicolumn.html "PostgreSQL 18: Multicolumn Indexes"
[P4]: https://www.postgresql.org/docs/current/indexes-partial.html "PostgreSQL 18: Partial Indexes"
[P5]: https://www.postgresql.org/docs/current/indexes-index-only-scans.html "PostgreSQL 18: Index-Only Scans and Covering Indexes"
[P6]: https://www.postgresql.org/docs/current/planner-stats-details.html "PostgreSQL 18: How the Planner Uses Statistics"
[L1]: https://www.cmu.edu/teaching/assessment/basics/alignment.html "Carnegie Mellon University: Align Assessments, Objectives, Instructional Strategies"
[L2]: https://nap.nationalacademies.org/catalog/10019/knowing-what-students-know-the-science-and-design-of-educational "National Academies: Knowing What Students Know"
[L3]: https://ies.ed.gov/ncee/wwc/PracticeGuide/1 "IES: Organizing Instruction and Study to Improve Student Learning"
[L4]: https://doi.org/10.1111/j.1467-9280.2006.01693.x "Roediger and Karpicke: Test-Enhanced Learning"
[L5]: https://pubmed.ncbi.nlm.nih.gov/16719566/ "Cepeda et al.: Distributed Practice"
[L6]: https://pubmed.ncbi.nlm.nih.gov/12081085/ "Barnett and Ceci: Transfer Taxonomy"
[L7]: https://act-r.psy.cmu.edu/?p=14344&post_type=publications "Corbett and Anderson: Knowledge Tracing"
