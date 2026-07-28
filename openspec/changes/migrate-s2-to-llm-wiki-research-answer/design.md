## Context

S1 已迁移为 `workspace/<project-slug>/runs/<run-id>/` 下的 LLM Wiki run folder，根 `INDEX.md` 是当前项目运行的下游入口。S2 目前虽已能读取该入口，但仍把研究结果输出为独立 Markdown、共同 JSON 信封和 JSON 驱动 HTML，导致 S1 问题、S2 回答、来源审计和阶段路由分散。

本设计把 S2 的物理输出并入同一 run folder，同时保持阶段职责不变：S1 定义并确认问题，S2 通过真实联网、多视角、多轮六源研究回答问题并评价 G2，S3 才组织能力结构。

## Goals / Non-Goals

**Goals:**

- 让 S2 逐项回答 S1 `research-brief.md` 中的 `priority_questions`，而不是仅生成抽象的领域对象。
- 为每个回答提供统一、可审计的多维校验机制。
- 把 S2 阶段资料落在同一 run folder 的 `s2/` 命名空间，并更新根 `INDEX.md`。
- 保留多轮联网、六源覆盖、证据独立性、冲突追问、饱和、成熟度、时效和 G2 fail-closed。
- 让 S3 从根索引定位并验证 S2 阶段区。

**Non-Goals:**

- 不删除 S2 Skill，不合并 G1/G2，也不把 S2 变为 S1 内部步骤。
- 不在 S2 构建正式能力图谱、学习路径或教学内容。
- 不迁移 S3–S7 的自身输出。
- 不要求改写历史 run 或迁移历史 JSON/HTML 工件。
- 不新增运行脚本；验证优先使用现有 CLI、JSONL 解析和静态检查。

## Decisions

### 1. 在同一 run 下使用具名 `s2/` 阶段区

S2 写入：

```text
workspace/<project-slug>/runs/<run-id>/
  INDEX.md
  ...S1 文件保持不变...
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

选择子目录而不是把文件平铺为 `s2-*.md`，因为后续阶段可以使用相同命名空间，根索引保持紧凑，而且同名 `sources.jsonl` 的阶段语义不会混淆。选择同一 `run-id` 而不是另开 S2 run，是因为 S2 正在回答这个已确认 S1 契约；目标实质变化必须返回 S1 新开 run。

### 2. `research-answers.md` 是 S2 的首要人审交付

S2 不再以 `domain_evidence_landscape` JSON 对象为中心。`research-answers.md` 按 S1 问题顺序逐题组织，每题使用稳定 `RQ-###` / `ANS-###`，保存上游问题原文和 `research-brief.md` 锚点。每个回答至少包含：

- 明确结论；
- `answer_status=answered|partial|unanswered`；
- `claim_status=supported|partially_supported|unsupported`；
- `knowledge_status=consensus|disputed|emerging|insufficient_evidence|deprecated`；
- 适用范围与不可泛化边界；
- 支持证据和反证/替代解释；
- 可观察任务、能力、知识、技能、产物影响；
- 置信度、证据缺口和对 S3 的影响。

这样保留 S2 的证据语义，同时让人直接看到“S1 问了什么，S2 回答了什么”。

### 3. 每个答案采用八维校验

`answer-validation.md` 对每个 `ANS-###` 逐维给出证据引用、结果、理由和失败动作：

1. `source_coverage`：结论是否得到适当六源通道支持；
2. `provenance_separation`：事实、市场信号、社区信号、模型假设是否分离；
3. `source_independence`：是否去重转载链并达到适用样本独立性；
4. `reliability_authority`：关键结论是否锚定可靠、可访问的一手或权威来源；
5. `timeliness_region_fit`：时间、地区、学段、学科和场景是否匹配；
6. `contradiction_balance`：反证、竞争解释和重要分歧是否被公平保留；
7. `observable_relevance`：回答是否落到 S1 的可观察成功证据、真实任务或产物；
8. `boundary_gap_clarity`：适用边界、未知项、置信度影响和下游风险是否透明。

任一关键维度失败时，该问题不能标为完全回答；关键问题未回答时 G2 不得通过。

### 4. 研究过程与人审回答分层

- `research-log.md`：视角、问题、查询、轮次、追问触发、开始/结束时间和未执行项。
- `sources.jsonl`：S2 实际核验的来源，一行一条，使用 S2 稳定 `E-###` ID。
- `coverage.md`：六源通道状态、独立样本数、关键性、门禁影响。
- `evidence-items.jsonl`：Task/Capability/Knowledge/Skill/Evidence 及可选对象的归一化记录。
- `research-answers.md`：结论先行的逐题回答。
- `answer-validation.md`：逐答案八维校验与多源覆盖。
- `g2-evaluation.md`：阶段级量规、裁决和路由。
- `verification.md`：文件、引用、占位符、状态机和风险收尾。
- `s2/INDEX.md`：S2 阶段入口、结论摘要、文件清单和下游读取说明。

选择少量 JSONL 记录文件而不是完全 Markdown，是为了保留稳定 ID 和跨文件机读，但不再生成单体 JSON 信封或正向工件 JSON。

### 5. 根 `INDEX.md` 是跨阶段注册表，不是可变结论混写页

S2 只新增或更新根索引中的 `## 阶段输出` 区段，至少列出 S1 与 S2 的入口、状态、门、路由和最后核对时间。S1 的目标、G1 裁决和历史内容保持原样；S2 详细事实只写在 `s2/`，根索引只存指针与摘要。

如果根索引不存在或不是通过 G1 的最新 run，S2 不创建伪造的项目入口，而是写阻断诊断并返回 S1。

### 6. G2 以 run-folder 九项条件机读

S2 被下游视为通过 G2，当且仅当：

1. `s2/` 九个固定文件齐全，根 `INDEX.md` 可解析到 `s2/INDEX.md`；
2. S1 `priority_questions` 全部恰好映射一个稳定 `RQ`/`ANS`，无静默遗漏；
3. `research-log.md` 证明真实在线、多视角、至少两轮研究，并记录冲突/新发现触发的追问；
4. `coverage.md` 六个通道各有状态、理由、独立样本数和门禁影响，且关键通道无阻塞缺口；
5. `sources.jsonl` 至少一条 accepted external evidence，所有答案/原子/量规引用可解析；
6. 所有关键答案的八维校验通过，事实/市场/模型假设分离，争议和缺口透明；
7. 结构饱和达到、成熟度至少 `L1_landscape`；
8. 条件确认若升级为 mandatory，则状态已确认；
9. `g2-evaluation.md` 全维通过、`verdict=pass`、`route_to=S3`，且 `verification.md` 为 `verified`、无阻塞 high 风险、无占位符。

### 7. 删除现行 S2 独立三工件依赖

S2 当前的共同信封 Schema、`domain-evidence-landscape.schema.json`、Markdown→JSON 对应合同、HTML 派生合同和页面模板不再属于现行 Skill 包。删除这些文件比保留“仅供参考”更能避免执行器误走旧流程；字段语义被编译进新的 `run-folder-contract.md`。

历史 OpenSpec、历史工件或评审证据不删除，只标记为迁移前证据。

## Risks / Trade-offs

- [根 `INDEX.md` 被多阶段更新，可能发生锚点漂移] → 使用固定 `## 阶段输出` 标题和阶段表；写入前重读当前文件，只更新 S2 行。
- [同一 run 混合 S1 与 S2 状态，读者可能误把 G1 pass 当 G2 pass] → 根索引和 `s2/INDEX.md` 分别显示门状态，禁止使用一个笼统“完成”状态。
- [移除 JSON Schema 后机器验证能力下降] → 以固定文件清单、JSONL 字段、稳定 ID、跨文件引用和九项 G2 条件替代；eval 改为检查目录与文档契约。
- [问题回答可能退化为无来源的长文] → 每题强制八维校验、证据引用和失败动作；未通过只能 `partial/unanswered`。
- [旧 S3 仍期待 JSON 信封] → 同步修改 S3 输入合同与 eval 断言；未迁移的其他阶段只改变读取 S2 的入口，不改变自身输出。
- [历史三工件证据与新规则冲突] → 历史工件明确为迁移前点时证据，不作为当前完成证明。

## Migration Plan

1. 新增 S2 `run-folder-contract.md`，冻结九文件、稳定 ID、状态机、八维校验和 G2 九项条件。
2. 重写 S2 Skill、阶段合同、示例、eval 和 agent prompt。
3. 删除 S2 独立 JSON/HTML 输出合同、Schema 和模板。
4. 修改 S3 的 S2 输入读取与 G2 校验。
5. 更新仓库 `AGENTS.md` 和 OpenSpec 基础规格。
6. 对现有 `workspace/senior-teaching-researcher` 只做读取冒烟，不伪造或补写尚未真实执行的 S2 研究结果。
7. 运行结构、JSONL、链接、OpenSpec 严格验证；昂贵外部 eval 未运行时显式保留门。

回滚时恢复 S2 三工件文件和 S3 JSON 信封输入合同，并撤销根索引的 S2 阶段注册规则；历史 run 不需要删除。

## Open Questions

- S3–S7 后续是否全部采用相同的阶段子目录结构，由各自后续 change 决定；本 change 不预设其具体文件清单。
- 现有 eval harness 对目录型输出的完整评分仍依赖后续通用扩展；本 change 先保证 eval 定义、静态合同和代表性目录检查可审计。
