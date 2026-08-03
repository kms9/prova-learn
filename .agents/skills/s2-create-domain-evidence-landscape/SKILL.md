---
name: al-s2-create-domain-evidence-landscape
description: 读取已通过 G1 的 S1 LLM Wiki run folder，对 research-brief.md 中的问题执行真实联网、STORM 式多视角、多轮六源取证，以逐题明确回答和八维校验写入同一 run 的 s2/ 阶段区，并更新根 INDEX.md；不产出独立 JSON 信封、单体 Markdown、HTML 或图片。只要用户要进入个性化学习 S2、核验并回答 S1 研究问题、研究领域依据，或补充 S3 暴露的来源空白，就使用本 skill。
---

# al-s2-领域取证与回答

负责“对 S1 已确认的问题，证据支持什么回答”。不负责画能力图，不把搜索数量、模型记忆、招聘词频或社区热度当成事实质量。

## 阶段、门与直接依赖

- `S2` 是领域研究回答阶段；`G2` 是判断这些回答能否被 S3 消费的质量门。
- 直接依赖是最新已过 G1 的 S1 run folder，入口为
  `workspace/<project-slug>/runs/<run-id>/INDEX.md`。
- G1 必须按 S1 run-folder 七项校验：11 文件齐全、G1 全维通过且 route=S2、确认完成、verification=verified
  且无阻塞 high 风险、无占位符、跨文件引用可解析、至少一条 accepted external evidence。
- S2 读取 `research-brief.md` 的 priority questions、`goal-contract.md`、`capabilities.jsonl`、
  `sources.jsonl`、`coverage.md`、`confirmation.md`。S1 预检只提供种子，不能冒充 S2 六源研究。
- G2 通过表示：每个 S1 问题都有明确回答和八维校验，真实多轮六源研究、来源独立性、追溯、争议、饱和、
  L1 成熟度、时效、确认和九文件完整性均通过，最终 route=S3。

## 开始前

1. 完整读取 [run-folder-contract.md](references/run-folder-contract.md)。
2. 读取 [stage-contract.md](references/stage-contract.md)。
3. 读取 [six-source-information-collection.md](references/six-source-information-collection.md)。
4. 仅为理解形状时读取 [example.md](references/example.md)；示例是夹具，不是真实观察。
5. 读取最新 S1 根 `INDEX.md` 及其链接的 `research-brief.md`、`goal-contract.md`、`capabilities.jsonl`、
   `sources.jsonl`、`coverage.md`、`confirmation.md`、`g1-evaluation.md`、`verification.md`。
6. 写入根索引前再次读取当前内容；工作树或索引已变化时以当前文件为准，不机械覆盖。

## 输出位置

在同一 S1 run 下写：

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

然后只在根 `INDEX.md` 的 `## 阶段输出` 区段新增或更新 S2 行，链接 `s2/INDEX.md`，记录状态、G2、路由和最后核对时间。不得改写 S1 目标、确认、G1 或历史事实。

## 执行

1. 定位最新 S1 run，执行 G1 七项校验；失败则记录输入缺口并返回 S1，不伪造 S2 正向回答。
2. 从 `research-brief.md` 按原顺序编译 priority questions：每题分配稳定 `RQ-###` 和 `ANS-###`，
   保存问题原文与上游位置；不得合并后静默丢题。
3. 基于 S1 目标框定主题、岗位/场景、地区、语言、时间边界、研究深度、排除项和问题关键性。
4. 同时建立研究视角与六类证据通道。视角用于提问；通道固定为 `job_career`、`books_courses`、
   `papers_research`、`community_web`、`standards_official`、`artifacts_validation`，两者不得混为一类。
5. 为每个视角提出核心问题、反例问题和后续追问，执行真实联网多轮查询。至少六视角、至少两轮；
   冲突或新发现必须触发后续检索。全过程写入 `research-log.md`。
6. 将实际核验来源写入 `s2/sources.jsonl`，分开标记
   `external_evidence`、`market_signal`、`model_hypothesis`、`user_provided_unverified`；
   用 `independence_group` 合并转载链。
7. 在 `coverage.md` 审计六源覆盖、样本独立性、关键性和 gate effect。找不到资料记 `gap`；
   `not_applicable` 必须有可审计理由。
8. 把来源统一抽取为 Task/Capability/Knowledge/Skill/Evidence 及必要扩展对象，写入
   `evidence-items.jsonl`；保留来源、回答、claim/knowledge status、时效、边界和冲突引用。
9. 在 `research-answers.md` 逐题写明确回答。每题必须有 answer/claim/knowledge status、置信度、
   适用边界、支持证据、反证或替代解释、可观察相关性、缺口、恢复动作和给 S3 的输入。
10. 在 `answer-validation.md` 对每个答案执行八维校验：
    `source_coverage`、`provenance_separation`、`source_independence`、
    `reliability_authority`、`timeliness_region_fit`、`contradiction_balance`、
    `observable_relevance`、`boundary_gap_clarity`。
11. 建立多源覆盖，检查连续两轮无新增一级能力域或关键二级问题族的结构饱和，评价 L0–L4 成熟度，
    并为稳定/动态知识设置刷新策略。
12. 遇高风险、活跃分歧、多种后果显著的回答或研究范围变化时，把 S2 条件确认升级为 mandatory；
    未确认不得通过 G2。
13. 按 G2 量规写 `g2-evaluation.md`，再完成 `verification.md` 的九文件、JSONL、映射、八维、
    跨引用、根索引和反占位检查，最后写/更新 `s2/INDEX.md` 与根 `INDEX.md`。
14. 若输入来自 S7 evidence feedback，只刷新受影响问题、claim、node 和来源，保留未受影响 ID；
    目标本身改变时返回 S1。

## 每题八维校验

| 维度 | 必须回答 |
|---|---|
| source coverage | 关键结论是否有合适的多源通道支持 |
| provenance separation | 事实、标准、市场、社区、假设是否分开 |
| source independence | 转载链是否去重，样本是否独立 |
| reliability/authority | 是否追到可访问的一手或权威来源 |
| timeliness/region fit | 是否匹配时间、地区、学段、学科和目标场景 |
| contradiction balance | 是否保留反证、竞争解释和双方强论据 |
| observable relevance | 是否落到 S1 的真实任务、可观察能力或验收产物 |
| boundary/gap clarity | 是否明确边界、未知、置信度影响和下游风险 |

结果使用 `pass|fail|insufficient|not_applicable`；非 pass 必须给出 failure action 和 route。任一关键答案的关键维度失败，该题不能标 `answered`，G2 不得通过。

## Fail closed

- 无真实联网、无查询日志、只有模型常识或一次浅搜索：`research_blocked`/`revise_here → S2`。
- S1 G1 未通过、priority questions 缺失或不可解析：输入失败，route=S1。
- 缺失来源通道：写 `gap`；不得用 `not_applicable` 掩盖未找到。
- 转载 SEO、培训广告、单一 JD、单个教材目录、社区多数或论文热度不能单独建立共识。
- 招聘是市场信号，面试题是评估信号；二者不是能力或领域事实本体。
- 问题证据不足时明确回答“当前不能下结论”，使用 partial/unanswered，不补造结论。
- 未达到六源覆盖、逐题八维、结构饱和和至少 L1 成熟度，不得写 `domain_landscape_ready` 或 route=S3。
- S3 发现来源空白时只局部刷新受影响回答和证据，不推倒无关结果。

## G2 九项机读条件

1. `s2/` 九文件齐全，根索引可解析到 `s2/INDEX.md`；
2. S1 priority questions 全部且恰好映射一个 RQ/ANS；
3. 在线完成、至少六视角、至少两轮，追问触发可审计；
4. 六源状态、理由、独立样本数、gate effect 完整且无阻塞 gap；
5. 至少一条 accepted external evidence，所有答案/来源/原子/缺口引用可解析；
6. 所有关键答案八维通过，事实/市场/假设分离，争议和缺口透明；
7. 结构饱和达到，成熟度至少 L1；
8. 升级的 mandatory 确认已完成；
9. G2 全维通过、verdict=pass、route=S3，verification=verified、无阻塞 high 风险、无占位符。

## 输出

首要交付是同一 LLM Wiki 中的 `s2/research-answers.md`，辅以研究日志、来源、覆盖、原子、八维校验、
G2 和验证文件，并由 `s2/INDEX.md` 与根 `INDEX.md` 提供入口。每次运行都写完整九文件；阻断态同样写清
已知、未知、未执行、恢复条件和路由。

不得生成或要求独立 JSON 移交信封、单体 S2 Markdown、HTML 页面、通用装载器或图片资产。只有 G2 九项全部满足时，才允许报告 S2 阶段完整完成并交给 S3。
