# S2 示例 — 同一 LLM Wiki 中的问题回答与多维校验

> 以下均为 `simulated_fixture`，用于展示合同，不是真实研究结果。真实运行必须重新联网并记录查询、来源和时间。

## 示例 A：PostgreSQL 18 正向夹具

### S1 输入

最新 S1 run 已通过 G1，`research-brief.md` 含：

1. 如何用可观察产物证明能诊断单表慢查询？
2. B-tree、多列、部分和覆盖索引的适用边界是什么？
3. 哪些“索引总更快”类口诀与官方行为冲突？

S2 在同一 run 写：

```text
s2/
  INDEX.md
  research-log.md
  sources.jsonl
  coverage.md
  evidence-items.jsonl
  research-answers.md
  answer-validation.md
  g2-evaluation.md
  verification.md
```

根 `INDEX.md` 的 `## 阶段输出` 表新增：

| Stage | Entry | Status | Gate | Route | Last verified |
| --- | --- | --- | --- | --- | --- |
| S1 | 当前根索引与 S1 文件 | completed | G1 pass | S2 | fixture-time |
| S2 | S2 领域研究回答（路径 `s2/INDEX.md`） | completed | G2 pass | S3 | fixture-time |

### `research-log.md` 摘录

- online: true
- execution_status: completed
- perspectives: 6
- rounds: 3
- `Q-001`：PostgreSQL 18 `EXPLAIN (ANALYZE, BUFFERS)` 官方文档
- `Q-002`：多列/部分/覆盖索引官方边界，follow_up_of=`Q-001`
- `Q-003`：顺序扫描优于索引的反例，follow_up_of=`Q-001`
- follow-up trigger：社区口诀“索引总更快”与官方成本/适用边界冲突

### `research-answers.md` 摘录

```markdown
## RQ-001 / ANS-001

- S1 question: 如何用可观察产物证明能诊断单表慢查询？
- criticality: critical
- answer_status: answered
- claim_status: supported
- knowledge_status: consensus
- confidence: high

### 明确回答
候选人应提交基线执行计划、估算与实际行数差异解释、瓶颈定位、备选方案、
读写代价权衡和沙箱复测记录；只给“加索引”结论不能证明诊断能力。

### 支持证据
E-001, E-004, E-009

### 反证、替代解释与分歧
单次 EXPLAIN ANALYZE 受缓存和数据分布影响；对写语句还会真实执行副作用。

### 对 S3 的输入
ITEM-001 真实任务、ITEM-004 计划估算知识、ITEM-007 验证技能。
```

### `answer-validation.md` 摘录

| Answer | Dimension | Evidence | Result | Confidence impact | Failure action |
|---|---|---|---|---|---|
| ANS-001 | source_coverage | E-001,E-004,E-009 | pass | none | — |
| ANS-001 | provenance_separation | E-001,E-009 | pass | none | — |
| ANS-001 | source_independence | IG-001,IG-004 | pass | none | — |
| ANS-001 | reliability_authority | E-001,E-004 | pass | none | — |
| ANS-001 | timeliness_region_fit | E-001 | pass | none | — |
| ANS-001 | contradiction_balance | E-006,E-009 | pass | none | — |
| ANS-001 | observable_relevance | ITEM-001,ITEM-007 | pass | none | — |
| ANS-001 | boundary_gap_clarity | GAP-002 | pass | none | — |

所有 S1 问题均有一对 RQ/ANS；六源覆盖可审计，结构饱和达到，成熟度=`L1_landscape`。
`g2-evaluation.md`：全维 passed，`verdict=pass`、`route_to=S3`。`verification.md`：`state=verified`。

## 示例 B：分数学习的证据边界夹具

S1 问题包括“哪些表征有助于理解等值分数”和“常见领域误概念是否就是该学习者的误概念”。

S2 回答：

- 数轴、面积模型和比例情境属于可交叉验证的领域级教学/表征证据；
- “分母更大所以分数更大”可以记录为领域常见误概念；
- 这些来源不能证明当前学习者一定持有该误概念，个体判断必须留给 S4 的真实行为诊断；
- `observable_relevance` 关联 S1 的数轴解释、配方缩放和未见迁移题；
- 若 `job_career` 对儿童分数学习确实不适用，可使用 `not_applicable`，但必须给出目标边界理由和 gate effect，
  不能把其余找不到的通道一并写成不适用。

满足逐题八维、六源可审计、饱和和 L1 后才 route=S3。

## 示例 C：SEO 转载链阻断夹具

输入要求用三篇互相转载的 SEO 博客和培训广告直接宣布“十条规则是行业共识”，并禁止继续联网。

S2 仍写九文件诊断区：

- `research-log.md`：online=false / execution_status=blocked；
- `sources.jsonl`：三篇转载共享同一 `independence_group`，广告为 market signal；
- `coverage.md`：缺失官方、论文、真实产物等通道记 `gap`；
- `research-answers.md`：对应回答为 `unanswered` / `unsupported` / `insufficient_evidence`；
- `answer-validation.md`：source coverage、independence、authority、contradiction balance 为 fail/insufficient；
- `g2-evaluation.md`：`verdict=blocked` 或 `revise_here`，`route_to=S2`；
- `verification.md`：`state=blocked`，列出恢复查询和缺口；
- 根 `INDEX.md` 的 S2 行明确 blocked，不改写 S1/G1。

不得生成假的联网轮次、独立样本数、结构饱和、L1、JSON 信封或 HTML。

## 示例 D：S7 返回后的局部补证

若 S7 只报告 `ANS-002` 关联的基数估算资料过期：

- S2 保留未受影响的 `ANS-001`、来源和原子 ID；
- `research-log.md` 新增刷新轮次和 S7 feedback 引用；
- 只为受影响问题执行 suggested queries；
- 更新对应来源、答案、八维校验、G2 和 verification；
- 只有受影响缺口解决且 G2 重新通过才 route=S3；
- S1 目标未变，不返回 S1。
