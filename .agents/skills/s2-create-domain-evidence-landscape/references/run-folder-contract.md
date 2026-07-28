# S2 LLM Wiki run-folder 合同

> 状态：现行  
> 适用阶段：S2 `create-domain-evidence-landscape`  
> 物理范围：已通过 G1 的 `workspace/<project-slug>/runs/<run-id>/s2/`  
> 首要人审交付：`research-answers.md`

## 1. 目的与边界

S2 读取 S1 已确认的 LLM Wiki run folder，通过真实联网、STORM 式多视角、多轮六源研究，逐项回答
`research-brief.md` 的 `priority_questions`。S2 不再产出单体 `domain_evidence_landscape` JSON、
共同移交信封、单体审核 Markdown 或交互 HTML；它把阶段资料写入同一 run 的 `s2/` 子目录，并在根
`INDEX.md` 注册 S2 入口。

S2 仍是独立阶段，G2 仍是独立质量门。物理交付并入同一 Wiki 不等于把 S2 合并进 S1，也不允许改写
S1/G1 历史事实。S3 才负责能力图谱；六类来源不能直接拼成课程目录。

## 2. 固定目录

```text
workspace/<project-slug>/runs/<run-id>/
  INDEX.md
  ...S1 的 10 个内容文件保持不变...
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

- 九个 S2 文件全部必需；`pending`、`blocked`、`revise_here` 也写出诚实的九文件诊断区。
- S2 阶段区内不得出现单体 `*.json` 移交信封、HTML、PNG/JPEG/WebP/SVG/GIF 或其他独立图片。
- 记录型数据使用 JSONL；面向人审、索引和审计的数据使用 Markdown。
- 同一 S1 run 的局部补证更新现有 `s2/`，保留未受影响 ID 和结论；目标实质改变时返回 S1 新开 run。

## 3. 稳定 ID 与引用

| ID | 含义 | 首次定义文件 |
|---|---|---|
| `RQ-001` | 从 S1 priority question 编译的研究问题 | `research-answers.md` |
| `ANS-001` | 对应问题的 S2 回答 | `research-answers.md` |
| `Q-001` | 实际执行的联网查询 | `research-log.md` |
| `E-001` | S2 实际核验来源 | `sources.jsonl` |
| `ITEM-001` | 归一化证据原子 | `evidence-items.jsonl` |
| `GAP-001` | 证据或回答缺口 | `research-answers.md` / `g2-evaluation.md` |
| `G2-*` | G2 量规维度 | `g2-evaluation.md` |

S1 的 `S001`/`CAP-001`/`TERM-001` 等 ID 保持原样，不在 S2 重编号。每个引用必须解析到当前 run 内的定义；
URL、搜索结果数量或自然语言“已验证”不能代替稳定引用。

## 4. 状态机与 guard

```text
input_located
→ g1_validated
→ questions_compiled
→ research_executed
→ sources_audited
→ answers_written
→ answers_validated
→ g2_evaluated
→ verified
```

| 转移 | Guard |
|---|---|
| `input_located → g1_validated` | 最新 S1 run 的 11 文件和 G1 七项机读条件通过 |
| `g1_validated → questions_compiled` | `research-brief.md` 可解析，priority questions 非空并逐项分配 `RQ`/`ANS` |
| `questions_compiled → research_executed` | 真实在线查询已执行；至少六视角、至少两轮，冲突/新发现有追问 |
| `research_executed → sources_audited` | S2 来源写入 `sources.jsonl`，六源覆盖、可靠性、独立性和时效已审计 |
| `sources_audited → answers_written` | 每个 S1 问题都有明确 answered/partial/unanswered 回答，不静默遗漏 |
| `answers_written → answers_validated` | 每个答案完成八维校验，所有证据/缺口/原子引用可解析 |
| `answers_validated → g2_evaluated` | 饱和、成熟度、确认状态和阻塞缺口已评价 |
| `g2_evaluated → verified` | 九文件、根索引、引用、无占位符和 G2 九项条件验证完成 |

任一 guard 失败，状态停止在最早失败点，记录当前结论、未执行项、恢复动作和路由；禁止补造通过态。

## 5. `research-log.md`

必须包含：

- run、S1 输入入口、开始/结束时间、online 与 execution status；
- 至少六类研究视角：术语与历史、理论与标准、实践任务、招聘市场、评估证据、批评与前沿；
- 每个视角的核心问题、反例问题、关联 `RQ` 和实际 `Q`；
- 查询表：`query_id`、查询文本、执行时间、结果摘要、`follow_up_of`；
- 轮次摘要、冲突/新发现触发的后续追问；
- 纳入/排除规则、去重规则、未执行项与原因。

只有模型知识或计划中的查询不得写为 `execution_status=completed`。

## 6. `sources.jsonl`

每行一个来源：

```json
{"evidence_id":"E-001","type":"web","title":"...","url":"https://...","publisher":"...","source_category":"standards_official","published_at":"2026-07","retrieved_at":"2026-07-28T10:00:00+08:00","region":"cn","reliability":"high","provenance":"external_evidence","status":"accepted","query_ids":["Q-001"],"applicability":"...","independence_group":"IG-001","supports":["ANS-001","ITEM-001"]}
```

必填字段：

- `evidence_id`、`type`、`title`、`publisher`、`source_category`；
- `published_at`（实际精度或 `null`）、`retrieved_at`、`region`；
- `reliability`：`high|medium|low|unknown`；
- `provenance`：`model_hypothesis|market_signal|external_evidence|user_provided_unverified|learner_behavior`；
- `status`：`accepted|trace_only|rejected|stale`；
- `query_ids[]`、`applicability`、`independence_group`、`supports[]`；
- web 来源用 `url`，本地来源用 `file`；至少一个可解析。

转载链共享同一 `independence_group`，独立样本计数按 group 去重。模型假设和未核验用户材料不能满足外部证据门。

## 7. `coverage.md`

固定六行且各出现一次：

`job_career`、`books_courses`、`papers_research`、`community_web`、`standards_official`、
`artifacts_validation`。

每行包含 `status=covered|not_applicable|gap`、reason、criticality、独立来源数、样本数、关键 `E`、
gate effect。找不到资料是 `gap`；只有确实不适用且理由可审计时才是 `not_applicable`。

另含：

- 核心候选的多源覆盖矩阵；
- 招聘适用时至少 3 个当前样本/2 个组织，面试适用时至少 2 组；不足记 undersample gap；
- 来源独立性和转载链说明。

研究视角与证据通道是两个维度，不得混用。

## 8. `evidence-items.jsonl`

每行一个归一化对象：

```json
{"item_id":"ITEM-001","object_type":"task","canonical_label":"...","aliases":[],"source_refs":["E-001"],"answer_refs":["ANS-001"],"claim_status":"supported","knowledge_status":"consensus","freshness":{"class":"dynamic","valid_through":null,"review_trigger":"..."},"applicability":"...","conflict_refs":[]}
```

`object_type` 至少支持 `task|capability|knowledge|skill|evidence`，可扩展
`tool|practice|failure|misconception|research_question|role|source`。同义项归并但保留 aliases；
语义不同不能因名称相近而合并。

## 9. `research-answers.md`

这是 S2 首要人审交付。开头包含范围、S1 输入、问题数、回答状态摘要、当前 G2 状态和最后核对时间。

每个问题固定结构：

```markdown
## RQ-001 / ANS-001

- S1 question source: `../research-brief.md#priority_questions` 第 1 项
- S1 question: ...
- criticality: critical|material|minor
- answer_status: answered|partial|unanswered
- claim_status: supported|partially_supported|unsupported
- knowledge_status: consensus|disputed|emerging|insufficient_evidence|deprecated
- confidence: high|medium|low|unknown

### 明确回答
...

### 适用边界与不可泛化项
...

### 支持证据
...

### 反证、替代解释与分歧
...

### 对可观察任务、能力、知识、技能和产物的影响
...

### 缺口、置信度影响与恢复动作
...

### 对 S3 的输入
...
```

问题原文必须逐字保留以便映射审计。回答可以是“证据不足，当前不能下结论”，但不能空白、TBD 或用建议冒充事实。

## 10. `answer-validation.md`：八维校验

每个 `ANS` 恰好包含八个维度：

| 维度 | 核心问题 |
|---|---|
| `source_coverage` | 是否有与结论重要性相称的六源交叉支持 |
| `provenance_separation` | 事实、标准、市场、社区、模型假设是否分开 |
| `source_independence` | 转载链是否去重，样本是否独立 |
| `reliability_authority` | 关键结论是否锚定可靠一手/权威来源 |
| `timeliness_region_fit` | 时间、地区、学段、学科、岗位/场景是否匹配 |
| `contradiction_balance` | 反证、竞争解释和双方强论据是否保留 |
| `observable_relevance` | 是否关联 S1 可观察成功证据、真实任务或产物 |
| `boundary_gap_clarity` | 边界、未知、缺口、置信度和下游风险是否透明 |

表中每行记录：`answer_id`、dimension、evidence refs、`result=pass|fail|insufficient|not_applicable`、理由、
confidence impact、failure action、route。`not_applicable` 必须有可审计理由；关键维度不是用
`not_applicable` 规避门。

文末汇总：

- answered/partial/unanswered 数；
- 每题八维完整性；
- 共识、分歧、误概念与开放问题；
- 结构饱和：连续两轮无新增一级能力域或关键二级问题族；
- 成熟度：`L0_fragments|L1_landscape|L2_learning_ready|L3_decision_ready|L4_expert_reviewed`；
- 稳定/动态知识刷新策略。

## 11. `g2-evaluation.md`

逐维评价：

- 实际联网执行；
- 六源覆盖；
- 来源可靠性、独立性、时效和地区适配；
- S1 问题完整映射；
- 逐题八维校验；
- claim/来源/原子可追溯；
- 事实/市场/推断分离；
- 争议与缺口透明；
- 结构饱和与 L1 成熟度；
- 条件确认；
- 根索引与九文件完整性。

每行包含 dimension、evidence、score、threshold、passed、failure action、route。裁决：

- `pass → S3`
- `revise_here → S2`
- `return_upstream → S1`（目标/成功契约实质失效）
- `blocked → S2`（无联网或关键外部能力不可用）

## 12. `verification.md`

必须记录：

- `state=verified|failed|blocked|pending`；
- 九文件存在性、JSONL 解析、根索引链接、问题映射、八维数量、跨文件 ID、反占位扫描；
- accepted external evidence 数和独立组数；
- 六源覆盖、轮次、视角、饱和、成熟度、确认和 G2 摘要；
- unresolved risks（严重度、影响、动作）；
- 已执行命令和未运行门；
- `fixture_type=observed|simulated_fixture|mixed|not_applicable`。

点时通过不构成永久证明；动态来源必须遵守刷新条件。

## 13. `s2/INDEX.md`

结论先行，至少包含：

- run、范围、S2 状态、G2 verdict/route、最后核对、受众；
- S1 问题→答案状态表；
- 九文件清单与用途；
- 六源/成熟度/饱和度摘要；
- 关键共识、分歧、缺口；
- S3 下游读取指引；
- 局部刷新历史和未运行门。

## 14. 根 `INDEX.md` 更新

写入前必须重读当前文件。新增或更新固定区段：

```markdown
## 阶段输出

| Stage | Entry | Status | Gate | Route | Last verified |
| --- | --- | --- | --- | --- | --- |
| S1 | 当前根索引及 S1 文件 | completed | G1 pass | S2 | ... |
| S2 | S2 领域研究回答（运行时链接目标 `s2/INDEX.md`） | completed|blocked|pending | G2 pass|revise_here|blocked | S3|S2|S1 | ... |
```

- 只更新 S2 行及必要的表头，不重写 S1 的目标、确认、G1 裁决或历史说明。
- 阻断时仍链接 `s2/INDEX.md`，但不得把根状态笼统标为完成。
- 根索引中的相对链接必须解析。

## 15. 已通过 G2：九项机读条件

1. `s2/` 九文件齐全，根 `INDEX.md` 解析到 `s2/INDEX.md`；
2. S1 priority questions 全部且恰好映射一个 `RQ`/`ANS`；
3. `research-log.md` 证明 online completed、至少六视角、至少两轮、追问触发可审计；
4. 六源各有状态/理由/独立样本数/gate effect，关键通道无阻塞 gap；
5. `sources.jsonl` 至少一条 `accepted external_evidence`，所有 `E`/`ITEM`/`ANS`/`GAP` 引用可解析；
6. 所有关键答案八维校验通过，事实/市场/假设分离，争议与缺口透明；
7. 结构饱和达到，成熟度至少 `L1_landscape`；
8. 条件确认如升级 mandatory，则已确认；
9. G2 全维通过、`verdict=pass`、`route_to=S3`，`verification=verified`、无阻塞 high 风险、无占位符。

文件存在、自然语言“研究完成”或 S1 预检来源数量都不能替代九项条件。

## 16. 反占位与完整性

禁止 `TBD`、`TODO`、`待补充`、示例 URL、空表、伪造查询、伪造日期或用模型记忆冒充检索。资料确实不存在时
写 `gap`；未执行时写 `not_executed`；网络不可用时写 `research_blocked`。

任一必需文件缺失、根索引未更新、问题映射遗漏、八维不全、跨文件引用失败或 G2 九项任一不满足时，
不得报告“S2 阶段交付完整完成”或把结果送入 S3。
