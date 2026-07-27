# 七步个性化学习 SOP：正反例与研究依据

> 调研日期：2026-07-26（Asia/Shanghai）  
> 对应流程：[个性化学习SOP步骤拆分最终结论.md](./个性化学习SOP步骤拆分最终结论.md)  
> 配套贯穿案例：[七步个性化学习SOP贯穿案例-PostgreSQL查询优化.md](./七步个性化学习SOP贯穿案例-PostgreSQL查询优化.md)

## 1. 文档目的

本文为 S1–S7 每一步分别提供：

- 2 个正向例子；
- 1 个反向例子；
- 实际正向输出片段；
- 质量评估与通过/返工结论；
- 支持判断的研究或官方资料。

“正向例子”表示该阶段的执行和工件质量正确，不要求学习者一定在该例中通过。“反向例子”表示该工件不应向下游移交，并说明污染会如何传播。

## 2. 调研方法与边界

本次采用**结构化快速综述**，不是完整系统综述，也不声称穷尽所有学习科学文献。

### 2.1 来源优先级

1. 国家级研究报告和政府研究指南；
2. 同行评审论文及原作者/出版机构页面；
3. 大学教学研究中心；
4. 示例领域的官方产品文档；
5. 仅在发现线索时使用二手材料，不用二手材料支撑关键结论。

### 2.2 检索与筛选原则

- 记录检索主题、来源和调研日期；
- 将目标、纳入范围和排除范围预先写清；
- 区分直接证据、方法迁移和主审推断；
- 对争议、不确定性和适用边界显式降级；
- 不把 PRISMA 或 GRADE 直接声称为通用教育流程标准，只借鉴其可追溯检索、筛选和不确定性表达方法。

这些原则参考了 [PRISMA 2020 的报告清单][R3]、[Cochrane 关于检索和筛选的手册章节][R4]以及 [CDC GRADE 对偏倚、不一致、间接性、不精确和发表偏倚的区分][R5]。

### 2.3 检索覆盖

本轮检索覆盖以下主题：

- 可观察学习目标、逆向设计和目标—教学—评价对齐；
- 可追溯资料检索、纳入排除、来源偏差和证据确信度；
- 概念图、焦点问题、学习进阶和先修结构；
- assessment triangle、Evidence-Centered Design 和先验知识诊断；
- worked examples、主动检索、间隔、深层解释问题和反馈；
- 近/远迁移、延迟保持、掌握学习和知识追踪；
- PostgreSQL 18 的执行计划、统计信息及多列、部分、覆盖索引。

最终文档保留 24 项来源，其中包括国家科学院共识报告、政府研究与实践指南、同行评审论文、大学教学中心和 PostgreSQL 官方文档。这 24 项不是 24 个相互独立的效果实验，也不应被当作元分析样本量。

## 3. 跨阶段研究证据矩阵

| SOP 阶段 | 主要研究依据 | 对示例设计的直接约束 |
|---|---|---|
| S1 目标契约 | CMU 目标与评价对齐 | 目标必须以学习者可观察行为表达，验收任务必须测到同一能力 |
| S2 领域取证 | PRISMA、Cochrane、GRADE 的透明检索思想 | 记录来源、纳入排除、结论—证据映射和不确定性 |
| S3 图谱建模 | IHMC 概念图、学习进阶 | 节点之间必须有具名关系；图谱围绕焦点问题，而不是术语堆积 |
| S4 学习者诊断 | assessment triangle、ECD、How People Learn II | 认知主张、观察任务、解释规则必须闭合；不能用自述替代行为证据 |
| S5 路径规划 | 目标—评价—教学对齐、学习者先验与情境 | 只规划学习前沿到目标的必要路径；策略和测评均服务同一目标 |
| S6 内容与交互 | worked examples、检索练习、深层问题、反馈 | 先示范后渐隐，要求学习者主动提取和解释，反馈指向任务与过程 |
| S7 掌握与重规划 | 迁移、间隔、掌握学习、知识追踪 | 即时正确不等于掌握；需要提示依赖、迁移、延迟保持和可追溯更新 |

## 4. 示例通用判定格式

所有例子都按同一最小结构展示：

```yaml
input_validation: pass | fail
requirement_gaps: []
confirmation: {}
evidence_collected: []
processing: []
positive_artifact: {}
quality_evaluation:
  evidence: []
  verdict: pass | revise_here | return_upstream
  route_to: S1-S7
```

示例中的分数和学习者回答均为**设计样例数据**，不是实际实验结果。

---

## S1. 目标与成功契约

### 研究依据

[CMU Eberly Center][R1]要求学习目标以学习者为中心、可行动且可测量；其[对齐指南][R2]指出目标、教学活动和测评不一致时，测评可能只测记忆，却声称学习者已经具备分析能力。因此 S1 的关键不是把目标写得宏大，而是把“会什么”写成可观察任务。

### 正向例子 1：成人学习 PostgreSQL 查询优化

**需求与确认**

- 用户原话：“四周内学会 PostgreSQL 查询优化，每周约 6 小时。”
- 补问：目标版本、生产权限、典型查询、是否要求改 SQL、是否要求解释权衡。
- 用户确认：PostgreSQL 18；只在沙箱执行；目标是诊断查询并提出可验证改进，不是学习数据库内核源码。

**正向输出：`goal_success_contract` 摘要**

```yaml
target_problem: 独立诊断并改进 PostgreSQL 18 中常见的单表查询性能问题
observable_capabilities:
  - 从 EXPLAIN (ANALYZE, BUFFERS) 区分估算与实际执行信息
  - 根据谓词、排序、选择性和统计信息解释扫描方式
  - 设计并论证单列、多列或部分索引，而不是默认“加索引”
  - 在沙箱比较改动前后计划，并说明写入、空间和维护代价
final_assessment:
  - 三个未见查询；独立完成采集、诊断、方案、验证和回滚说明
pass_rule:
  - 三题中至少两题的主瓶颈、方案和验证均正确
  - 不执行未经确认的生产变更
constraints:
  duration: 4周
  effort: 每周6小时
  environment: PostgreSQL 18 沙箱
excluded:
  - PostgreSQL 源码级优化器开发
confirmation_status: confirmed
```

**质量评估**

- 可观察性：每项能力都有实际行为；
- 对齐性：最终任务测诊断和取舍，不只测术语；
- 安全性：明确沙箱和变更边界；
- 结论：`pass → S2`。

### 正向例子 2：六年级学生理解分数

**需求与确认**

- 初始诉求：“分数总是学不会。”
- 确认场景：三周后需要解决分数比较、等值分数和简单情境题；每天 25 分钟；不以机械通分速度作为唯一目标。

**正向输出片段**

```yaml
target_problem: 解释分数大小并在新情境中选择合理方法
observable_capabilities:
  - 在数轴上定位真分数和假分数
  - 用图示或单位分数推理比较大小
  - 解释等值分数为何数值不变
  - 解决食谱缩放和长度分配问题
assessment:
  - 比较3/5与3/7并解释
  - 将5/4放到数轴
  - 解释2/3为何等于4/6
  - 完成一个未见食谱缩放题
pass_rule:
  conceptual_items: 3/4
  transfer_item: 必须独立通过
confirmation_status: guardian_and_learner_confirmed
```

**质量评估**

- 目标同时包含表征、解释、应用和迁移；
- 与 IES 分数指南强调的数轴、大小和概念理解相符；
- 结论：`pass → S2`。

### 反向例子：七天学会 AI

**错误输出**

```yaml
goal: 七天成为AI专家
plan: 每天看两小时视频
assessment: 做100道选择题，80分通过
```

**为什么失败**

- “专家”没有可观察定义；
- 视频时长是投入，不是能力；
- 选择题无法验证建模、诊断或创造；
- 没有使用场景、范围、资源或安全边界。

**质量判定**：`return_upstream → S1`。若继续到 S2，后续无法判断该搜哪些领域；若继续到 S7，80 分也不能证明目标达成。

---

## S2. 领域取证与认知全景

### 研究依据

S2 不是要求每次都做正式系统综述，而是借鉴 [PRISMA][R3] 对信息源、检索策略、纳入排除和选择过程的透明报告，以及 [Cochrane][R4] 对检索偏差、来源范围和停止条件的要求。证据确信度需要说明偏倚、不一致、间接性和不精确，而不是把所有链接视为等价证据。[PostgreSQL 官方索引章节][R20]还明确指出索引既可能加速查询，也带来系统开销，这类边界必须进入全景。

### 正向例子 1：PostgreSQL 查询优化证据全景

**确认交互**

- 范围：PostgreSQL 18 的单表查询、B-tree、多列/部分/覆盖索引、统计信息和 `EXPLAIN`；
- 排除：跨数据库通用结论、分布式数据库和未发布的 PostgreSQL 19 行为；
- 来源规则：产品行为以 PostgreSQL 18 官方文档为主，教学策略另用学习研究。

**正向输出片段**

```yaml
scope:
  product: PostgreSQL 18
  included: [EXPLAIN, planner statistics, B-tree, multicolumn, partial, index-only]
source_ledger:
  - claim: EXPLAIN计划由树状节点组成，ANALYZE会实际执行查询
    source: PostgreSQL 18 Using EXPLAIN
    confidence: high
  - claim: 多列B-tree对前导列约束通常最有效
    source: PostgreSQL 18 Multicolumn Indexes
    confidence: high
  - claim: 部分索引只有在查询条件可蕴含其谓词时才可用
    source: PostgreSQL 18 Partial Indexes
    confidence: high
consensus:
  - 优化必须结合查询、数据分布、计划和真实测量
misconceptions:
  - 有索引就一定比顺序扫描快
  - EXPLAIN中的cost就是毫秒
unknowns:
  - 示例业务数据的真实分布与缓存状态尚未采集
```

**质量评估**

- 关键产品事实来自当前官方文档；
- 版本和排除项明确；
- “未知”没有被猜测填充；
- 结论：`pass → S3`。

### 正向例子 2：六年级分数学习证据全景

**信息收集**

- 采用美国教育科学研究院的分数教学实践指南；
- 用国家科学院关于先验知识、学习情境和评价的报告补充一般学习机制；
- 不把某个教辅账号的“口诀”当作概念学习证据。

**正向输出片段**

```yaml
core_models:
  - 分数表示一个量，不只是两个整数
  - 数轴提供统一的大小与顺序表征
  - 等值分数保持同一数值
known_misconceptions:
  - 分母越大，分数越大
  - 分子分母分别做整数运算即可
representations:
  - 实物/操作物
  - 图形
  - 数轴
  - 符号
evidence_boundary:
  - IES指南是实践指南，不是对每个学习者的诊断结果
  - 仍需S4行为证据确认具体误概念
```

**质量评估**

- 区分领域常见误解与当前学习者误解；
- 同时覆盖概念、表征和应用；
- 结论：`pass → S3`。

### 反向例子：搜索前三篇博客后宣布共识

**错误输出**

```yaml
sources:
  - SEO博客A
  - 培训广告B
  - 无作者转载C
conclusion:
  - 所有慢查询都应该创建索引
  - cost就是运行毫秒
confidence: high
```

**为什么失败**

- 没有来源筛选、版本和纳入排除规则；
- 无法追溯具体结论；
- 与 PostgreSQL 官方文档关于索引开销、成本估算和小表顺序扫描的说明冲突；
- 未记录冲突和不确定性。

**质量判定**：`revise_here → S2`。禁止把该结果送入 S3，否则图谱会把错误规则建成“硬先修”。

---

## S3. 能力—概念图建模

### 研究依据

[IHMC][R6]将概念图定义为概念和带有连接词的关系命题，并强调每张图应回答一个焦点问题。只有术语节点而没有关系，不能表达可检验的知识结构。[How People Learn II][R9]所述学习进阶则要求从较朴素到更成熟的思考方式组织节点。S3 还需把概念连接到任务和证据，而不只是画图。

### 正向例子 1：PostgreSQL 查询优化图谱

**焦点问题**：学习者要依据什么证据选择并验证一个索引方案？

**正向输出片段**

```text
读取执行计划
├─硬先修→ 区分估算 rows 与 actual rows
├─硬先修→ 识别 Seq/Index/Bitmap Scan
└─支持→ 识别 Sort、Limit 与过滤位置

解释计划选择
├─硬先修→ 选择性与基数估算
├─硬先修→ planner statistics / ANALYZE
└─支持→ 随机访问与顺序访问代价

设计索引
├─硬先修→ B-tree可支持的比较与排序
├─硬先修→ 多列索引前导列与谓词形状
├─条件先修→ 部分索引谓词蕴含
└─条件先修→ index-only scan与可见性

验证改进
├─硬先修→ 沙箱基线
├─硬先修→ EXPLAIN (ANALYZE, BUFFERS)
└─硬先修→ 查询结果等价与写入代价说明
```

每个节点同时绑定：

```yaml
node: multicolumn_btree_order
capability: 给定查询模式，解释两个候选列顺序的适用差异
assessment: 为三个不同谓词选择索引顺序并说明边界
source: PostgreSQL 18 Multicolumn Indexes
misconception: 把选择性最高的列机械放第一位
```

**质量评估**：目标可从节点追溯；边有类型和理由；概念连接到能力、题目和来源；`pass → S4`。

### 正向例子 2：分数概念图

**焦点问题**：学生如何从“份数”发展到能比较、运算并迁移分数？

```text
单位整体
└─硬先修→ 等分
   └─硬先修→ 单位分数
      ├─硬先修→ 分数大小与数轴位置
      │  ├─支持→ 同分子比较
      │  └─支持→ 同分母比较
      └─硬先修→ 等值分数
         └─硬先修→ 通分的意义
            ├─→ 异分母比较
            └─→ 异分母加减
```

节点示例：

```yaml
node: equivalent_fractions
capability: 用图形、数轴和乘法关系解释2/3=4/6
diagnostic:
  - 判断2/3与4/6是否相等并解释
  - 构造一个与3/5等值的分数
misconception: 分子分母变大意味着分数变大
```

**质量评估**：概念结构服务焦点问题；数轴和等值关系不是孤立章节；`pass → S4`。

### 反向例子：把目录当图谱

```text
SQL基础
索引
执行计划
锁
事务
分区
调优
```

**为什么失败**

- 没有焦点问题、连接词、硬/软先修或理由；
- 不知道“能解决什么问题”；
- 无评估项、误解和来源映射；
- 混入不属于目标最小路径的主题。

**质量判定**：`revise_here → S3`；若节点事实本身无证据则 `return_upstream → S2`。

---

## S4. 学习者诊断与学习前沿

### 研究依据

国家科学院的 [assessment triangle][R7]要求认知模型、观察任务和解释规则彼此一致；[Evidence-Centered Design][R8]同样强调先说明要做什么能力推断，再设计能产生证据的任务。[How People Learn II][R9]指出有效教学依赖先验知识、经验、动机和情境。由此可见，自我评分或单题正确不能直接生成学习者画像。

### 正向例子 1：诊断 PostgreSQL 学习者

**诊断任务与观察**

| 任务 | 学习者表现 | 推断 |
|---|---|---|
| 解释普通 `EXPLAIN` 与 `EXPLAIN ANALYZE` | 知道后者实际执行；未提写操作风险 | 基础通过，安全边界待补 |
| 在计划中区分估算行数与实际行数 | 能指出差异，不能解释统计信息作用 | 观察通过，解释缺口 |
| 为 `tenant_id = ? AND status = ? ORDER BY created_at DESC` 选索引 | 只说“把选择性最高的列放前面” | 多列索引模型存在误概念 |
| 给出数据分布变化后的方案 | 仍沿用同一索引，不要求重新测量 | 迁移未通过 |

**正向输出片段**

```yaml
mastered:
  - plan_tree_basics
  - estimated_vs_actual_recognition
evidence_insufficient:
  - explain_analyze_safety
not_mastered:
  - planner_statistics_reasoning
  - multicolumn_index_order
  - workload_change_transfer
learning_frontier:
  - planner_statistics_reasoning
misconception:
  code: SELECTIVITY_FIRST_ALWAYS
  evidence_ids: [D3, D4]
confidence_calibration:
  self_confidence: 0.85
  observed_level: partial
```

**质量评估**：结论来自多任务和推理过程；区分识别、解释和迁移；`pass → S5`。

### 正向例子 2：诊断分数误概念

**诊断任务**

1. 比较 `3/5` 与 `3/7` 并解释；
2. 把 `5/4` 放在数轴；
3. 判断 `2/3` 与 `4/6`；
4. 计算 `1/2 + 1/3` 并用图说明。

**观察**

- 第 1 题答 `3/7` 大，因为 7 大；
- 第 2 题放在 0 与 1 之间；
- 第 3 题用图后能说明相等；
- 第 4 题写成 `2/5`。

**正向输出**

```yaml
mastered: [equal_partition_visual, equivalent_fraction_visual]
not_mastered:
  - denominator_magnitude
  - improper_fraction_number_line
  - unlike_denominator_addition_meaning
learning_frontier: unit_fraction_and_number_line
primary_misconception: WHOLE_NUMBER_BIAS
evidence: [F1, F2, F4]
```

**质量评估**：共同错误模式有三个独立观察支持；没有因第 3 题正确就宣布整体掌握；`pass → S5`。

### 反向例子：自评 8 分即判定中高级

```yaml
question_1: 你觉得自己有多熟？
answer_1: 8/10
question_2: 索引能加速查询吗？
answer_2: 是
learner_level: advanced
```

**为什么失败**

- 自评没有经过校准；
- 第二题只测口号识别；
- 没有推理、提示、反例、迁移或错误分类；
- “高级”无法映射到图谱节点。

**质量判定**：`revise_here → S4`；诊断题无法产生目标证据时 `return_upstream → S3`。

---

## S5. 路径与会话规划

### 研究依据

[CMU 对齐指南][R2]要求目标、评价和教学活动一致；[How People Learn II][R9]强调挑战要与学习者当前能力相匹配，并利用反馈支持有意义目标。路径因此不能只是教材目录，而应由目标图谱和学习前沿共同决定。

### 正向例子 1：面向 SQL 误概念的四会话路径

**输入**：学习者已会读取基础计划，但不了解统计信息、多列索引顺序和迁移。

**正向输出**

```yaml
path:
  - session: 1
    nodes: [selectivity, row_estimation, analyze_statistics]
    why: 修复“计划器凭规则选索引”的错误模型
    exit: 能解释估算偏差并提出验证动作
  - session: 2
    nodes: [btree_order, multicolumn_leading_columns, order_by_limit]
    why: 直接处理SELECTIVITY_FIRST_ALWAYS
    exit: 三个查询模式中至少2个独立选择并论证
  - session: 3
    nodes: [partial_index, index_only_scan, maintenance_tradeoff]
    why: 扩展条件方案与代价判断
    exit: 能拒绝一个不合适索引并说明原因
  - session: 4
    nodes: [unseen_plan_diagnosis, transfer, delayed_retrieval]
    exit: 完成未见案例和一周后复测
review_anchors: [次日, 第4天, 一周后]
confirmation: confirmed
```

**质量评估**：路径从学习前沿开始；每会话有理由和退出标准；包含迁移与延迟检查；`pass → S6`。

### 正向例子 2：分数学习路径

```yaml
path:
  - session: 1
    focus: 单位整体、等分、单位分数
    representation: [实物, 图形, 数轴]
  - session: 2
    focus: 真分数与假分数的数轴位置
    retrieval: 不看图重新定位
  - session: 3
    focus: 等值分数与大小比较
    contrast: [同分子, 同分母, 既不同分子也不同分母]
  - session: 4
    focus: 异分母加法的意义
    prerequisite_gate: 等值分数与数轴必须通过
  - session: 5
    focus: 食谱与长度分配迁移题
confirmation:
  effort: 每天25分钟
  status: confirmed
```

**质量评估**：针对全数偏差；具体—表征—抽象相连；不提前教授机械通分；`pass → S6`。

### 反向例子：复制课程目录

```yaml
week_1: 看完数据库原理第1-5章
week_2: 看10个索引视频
week_3: 刷100道题
week_4: 做项目
```

**为什么失败**

- 未使用 `learner_snapshot`；
- 章节和视频不是能力节点；
- 无先修门、退出标准和调整规则；
- 100 道题可能重复同一模板，无法证明迁移。

**质量判定**：`revise_here → S5`；若根本没有有效学习前沿则 `return_upstream → S4`。

---

## S6. 内容生产与教学交互

### 研究依据

美国教育科学研究院指南建议间隔学习、交替 worked examples 与独立问题、结合抽象和具体表征、主动检索并提出深层解释问题。[Roediger 与 Karpicke][R13]发现反复测验相较反复阅读对延迟保持更有优势。[Hattie 与 Timperley][R14]则提醒反馈的效果取决于类型和给法，不能把泛泛表扬等同于有效反馈。

### 正向例子 1：多列索引的渐隐教学

**会话片段**

1. **完整示例**：给定查询谓词、排序和数据分布，教师逐步标注哪些条件能限制 B-tree 扫描范围；
2. **半完成示例**：给另一个查询，学习者补出第二、三步判断；
3. **对比任务**：比较 `(tenant_id, status, created_at)` 与 `(status, tenant_id, created_at)`；
4. **独立任务**：新查询包含范围条件和 `ORDER BY ... LIMIT`，不显示答案；
5. **反馈**：指出学习者把“全局选择性”当成唯一规则，要求回到谓词形状和前导列约束重新解释。

**正向输出片段**

```yaml
content:
  worked_example: 有完整推理，不只给CREATE INDEX
  completion_problem: 隐去关键两步
  contrast_case: 两个可运行但适用面不同的索引
  independent_problem: 未见查询，不给提示
prompt_ladder:
  - 先指出等值、范围和排序条件
  - 再判断哪些条件限制扫描区间
  - 最后才比较索引候选
interaction_trace:
  - learner_claim: 选择性最高的列必须第一
  - feedback: 指向查询形状和官方规则，不直接泄露最终顺序
```

**质量评估**：内容与官方多列索引文档一致；支架逐步撤除；独立任务能产生 S7 证据；`pass → S7`。

### 正向例子 2：分数的具体—表征—抽象交互

**会话片段**

- 用同样大小的条形比较 `1/2` 与 `1/5`；
- 学习者自己画数轴并定位；
- 撤掉图形后要求解释“分母变大时单位分数为何变小”；
- 混入 `3/5` 与 `3/7`、`2/3` 与 `3/4`，要求选择策略；
- 次日先检索解释，再看材料。

IES 分数指南明确讨论了分数大小、数轴和多种表征；IES 的学习组织指南支持抽象—具体连接与主动检索。

**正向输出**

```yaml
representations: [等长条形, 数轴, 符号]
deep_question: 当整体相同，为什么分成更多份后每份更小？
independent_task: 不用图比较3/5与3/7并解释
feedback_rule:
  task: 指出比较目标
  process: 检查单位整体与单位分数
  self_regulation: 让学习者说明下一题先检查什么
```

**质量评估**：表征之间有连接；学习者必须生成解释；反馈不代答；`pass → S7`。

### 反向例子：长篇讲义加即时答案

```text
系统连续输出5000字索引理论；
每个问题后立即显示标准答案；
学习者只回复“懂了”；
系统把会话标成完成。
```

**为什么失败**

- 没有学习者主动提取、解释和独立作答；
- 立即泄露答案，无法区分会做与看懂；
- 没有提示层级、反馈轨迹或候选掌握证据；
- 内容长度替代了教学适配。

**质量判定**：`revise_here → S6`；禁止进入 S7 宣称掌握。

---

## S7. 掌握验证、模型更新与重规划

### 研究依据

[Roediger 与 Karpicke][R13]及 [Cepeda 等人的间隔学习综述][R15]说明即时表现和延迟保持不同；[Barnett 与 Ceci][R16]指出迁移距离包含知识、时间、场景、功能、社会和形式等多个维度，不能只写“考一道新题”；[掌握学习元分析][R17]总体支持达到门槛后再推进，同时提醒时间和完成率代价；[Corbett 与 Anderson][R18]展示了根据连续行为更新技能状态的知识追踪思想。

### 正向例子 1：SQL 节点未完全掌握，但流程正确

**证据**

| 证据 | 表现 |
|---|---|
| 同结构新查询 | 独立选择合理多列索引并解释 |
| 改变数据分布 | 仍沿用原方案，未要求重新 `ANALYZE` 和测量 |
| 提示依赖 | 第一题无提示，第二题经二级提示后修正 |
| 三日延迟复测 | 能解释前导列，不能解释估算误差来源 |

**正向输出**

```yaml
mastery:
  multicolumn_index_order: provisional_mastered
  statistics_and_distribution_transfer: not_mastered
evidence_ids: [Q1, Q2, D3]
primary_attribution: STRATEGY_OR_SEQUENCE
model_update:
  misconception_SELECTIVITY_FIRST_ALWAYS: weakened
  planner_statistics_reasoning: 0.42
route_to: S5
replan:
  - 增加统计信息与数据分布的对比会话
  - 保留多列索引次日检索
```

**为什么是正向例子**

学习者没有通过全部内容，但系统正确地区分节点、保留不确定性并调整路径，没有把局部成功夸大为整体掌握。质量结论：`pass artifact; route → S5`。

### 正向例子 2：分数节点完成并进入保持计划

**证据**

- 即时：不看材料解释 `3/5 > 3/7`；
- 近迁移：比较 `4/9` 与 `4/11`；
- 表征变化：从图形转到数轴；
- 一周延迟：独立完成；
- 远一些的功能情境：在食谱缩放中正确使用分数关系。

**正向输出**

```yaml
mastery:
  unit_fraction_magnitude: mastered
  same_numerator_comparison: mastered
evidence_dimensions:
  independence: pass
  representation_transfer: pass
  context_transfer: pass
  delayed_retention: pass
model_version: 7
route_to: S6
next_node: equivalent_fractions
review_schedule: [两周后混合检索]
```

**质量评估**：多维证据支持状态更新；版本和下一节点明确；`pass → 下一节点 S6`。

### 反向例子：一次选择题正确即 95% 掌握

```yaml
item: B-tree适合等值查询吗？
answer: 是
result: correct
mastery_probability: 0.95
route_to: next_chapter
```

**为什么失败**

- 只测识别，不测解释、选择、诊断或迁移；
- 未记录猜测概率、提示和置信度；
- 没有延迟保持；
- `0.95` 没有模型、先验或校准依据；
- 状态跳变会错误跳过必要节点。

**质量判定**：`EVIDENCE_INSUFFICIENT → S7 补测`，不得更新为已掌握。

---

## 5. 从 21 个例子抽出的共性规则

1. 正向输出必须是下游可读取的具名工件，不是过程叙述。
2. 质量评估必须引用工件内证据，不能只给“很好”“完整”等结论。
3. S1 的验收任务决定下游对齐基准。
4. S2 负责证据真值和不确定性，S3 负责结构，不能互相隐式代办。
5. S4 的核心是“从观察推断能力”，不是收集偏好问卷。
6. S5 只规划从当前学习前沿到目标的必要路径。
7. S6 必须产生学习者自己的行为证据。
8. S7 的正向结果可以是“未掌握但正确路由”，不能把通过率当作流程质量。
9. 即时正确、同题重做、近迁移、远迁移和延迟保持是不同证据。
10. 反向例子若未在本阶段拦截，会以更高成本污染全部下游。

## 6. 研究来源

[R1]: https://www.cmu.edu/teaching/designteach/syllabus/newcourse/learningobjectives.html "Carnegie Mellon University: Learning Objectives"
[R2]: https://www.cmu.edu/teaching/assessment/basics/alignment.html "Carnegie Mellon University: Align Assessments, Objectives, Instructional Strategies"
[R3]: https://www.prisma-statement.org/prisma-2020-checklist "PRISMA 2020 Checklist"
[R4]: https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04 "Cochrane Handbook Chapter 4: Searching for and selecting studies"
[R5]: https://www.cdc.gov/acip-grade-handbook/hcp/chapter-7-grade-criteria-determining-certainty-in-the-evidence/index.html "CDC ACIP GRADE Handbook: Criteria determining certainty"
[R6]: https://cmap.ihmc.us/publications/researchpapers/theorycmaps/TheoryUnderlyingConceptMaps.bck-11-01-06.htm "IHMC: The Theory Underlying Concept Maps"
[R7]: https://nap.nationalacademies.org/catalog/10019/knowing-what-students-know-the-science-and-design-of-educational "National Academies: Knowing What Students Know"
[R8]: https://onlinelibrary.wiley.com/doi/10.1111/j.1745-3992.2006.00075.x "Mislevy and Haertel: Implications of Evidence-Centered Design"
[R9]: https://nap.nationalacademies.org/catalog/24783/how-people-learn-ii-learners-contexts-and-cultures "National Academies: How People Learn II"
[R10]: https://ies.ed.gov/ncee/wwc/PracticeGuide/1 "IES: Organizing Instruction and Study to Improve Student Learning"
[R11]: https://ies.ed.gov/ncee/wwc/Docs/PracticeGuide/fractions_pg_093010.pdf "IES: Developing Effective Fractions Instruction"
[R12]: https://ies.ed.gov/ncee/wwc/practiceguide/12 "IES: Using Student Achievement Data to Support Instructional Decision Making"
[R13]: https://doi.org/10.1111/j.1467-9280.2006.01693.x "Roediger and Karpicke: Test-Enhanced Learning"
[R14]: https://doi.org/10.3102/003465430298487 "Hattie and Timperley: The Power of Feedback"
[R15]: https://pubmed.ncbi.nlm.nih.gov/16719566/ "Cepeda et al.: Distributed practice review and quantitative synthesis"
[R16]: https://pubmed.ncbi.nlm.nih.gov/12081085/ "Barnett and Ceci: A taxonomy for far transfer"
[R17]: https://doi.org/10.3102/00346543060002265 "Kulik et al.: Effectiveness of Mastery Learning Programs"
[R18]: https://act-r.psy.cmu.edu/?p=14344&post_type=publications "Corbett and Anderson: Knowledge tracing"
[R19]: https://www.postgresql.org/docs/current/using-explain.html "PostgreSQL 18: Using EXPLAIN"
[R20]: https://www.postgresql.org/docs/current/indexes.html "PostgreSQL 18: Indexes"
[R21]: https://www.postgresql.org/docs/current/indexes-multicolumn.html "PostgreSQL 18: Multicolumn Indexes"
[R22]: https://www.postgresql.org/docs/current/indexes-partial.html "PostgreSQL 18: Partial Indexes"
[R23]: https://www.postgresql.org/docs/current/indexes-index-only-scans.html "PostgreSQL 18: Index-Only Scans and Covering Indexes"
[R24]: https://www.postgresql.org/docs/current/planner-stats-details.html "PostgreSQL 18: How the Planner Uses Statistics"
