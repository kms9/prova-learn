## Why

S2 当前把“回答 S1 已确认研究问题”包装成独立的 Markdown/JSON/HTML 三工件，重复了机器信封与页面派生工作，却没有把研究结论直接沉淀进 S1 已建立的 LLM Wiki 项目知识入口。现在需要让 S2 直接消费同一 run folder，以可追溯、多维校验的明确文档逐题回答 S1，并把阶段入口、状态和路由写回主 `INDEX.md`。

## What Changes

- **BREAKING**：S2 不再产出独立 `domain_evidence_landscape` JSON 信封、单体审核 Markdown 或交互 HTML，也不再以三工件完整性作为 S2 交付门。
- S2 仍是独立阶段 Skill；“不再独立”仅指其物理交付并入 S1 建立的 LLM Wiki run folder，不删除 S2，也不把 G2 合并进 G1。
- S2 读取最新已过 G1 的 `workspace/<project-slug>/runs/<run-id>/INDEX.md` 及其链接内容，在同一 run folder 下创建具名 `s2/` 阶段区。
- S2 以 `research-brief.md` 的 `priority_questions` 为主键，生成逐题明确回答；每个回答必须包含结论、适用边界、支持证据、反证/替代解释、跨来源校验、置信度、缺口和下游影响。
- S2 保留真实联网、STORM 多视角、多轮六源取证、来源独立性、事实/市场/推断分离、争议平衡、结构饱和、时效治理与 G2 fail-closed。
- S2 阶段区采用 LLM Wiki 文件：阶段索引、问题回答、来源台账、六源覆盖、多维校验矩阵、证据原子、G2 评价与验证记录；记录型数据可用 JSONL，面向人审的回答与审计使用 Markdown。
- 若上游 S1 run folder 存在，S2 原地更新根 `INDEX.md`，新增明确的 `S2` 阶段分区、入口、状态、G2 裁决、路由和最后核对时间；不得改写 S1/G1 历史事实。
- 阻断或未通过时仍写出诚实的 S2 阶段区和索引状态，保留未执行项、恢复条件与最早回退路由。
- S3 改为通过根 `INDEX.md` 定位当前 S2 阶段区，并按 S2 run-folder 机读条件判断 G2，而非读取 S2 JSON 信封。
- 更新 S2 Skill、阶段/输出合同、示例、eval、agent prompt、仓库导航、基础规格及受影响的共享阶段/HTML 契约。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `create-domain-evidence-landscape`：把 S2 输出从独立三工件改为同一 LLM Wiki run folder 中、逐题回答 S1 研究问题并执行多维校验的阶段文档区。
- `personalized-learning-stage-contracts`：为 S2 定义 run-folder 交付例外、G2 机读条件及 S2→S3 的索引读取契约，不再要求 S2 发出共同 JSON 信封。
- `stage-html-visualizations`：移除 S2 的强制 HTML 派生与 `evidence_landscape_workbench` 交付要求，S2 可视化回归 Markdown 表格/索引视图。

## Impact

- 主要实现：`.agents/skills/s2-create-domain-evidence-landscape/`。
- 下游消费：`.agents/skills/s3-build-capability-concept-graph/` 的 S2 输入验证。
- 仓库协议：`AGENTS.md` 中三工件范围、阶段导航、验证清单与 LLM Wiki 结构。
- 规格：`openspec/specs/create-domain-evidence-landscape/`、`personalized-learning-stage-contracts/`、`stage-html-visualizations/`。
- 示例与 eval：S2 的 `references/example.md`、`evals/evals.json`、`agents/openai.yaml`。
- 兼容性：S2 遗留 JSON Schema/HTML 模板不再是现行输出合同；历史工件仅保留为历史证据，不得作为当前 S2 完成证明。
- 前置关系：本 change 继承 `migrate-s1-to-llm-wiki-delivery` 已建立的 S1 run-folder 与根 `INDEX.md` 入口，不扩大到 S3–S7 全部输出迁移。
