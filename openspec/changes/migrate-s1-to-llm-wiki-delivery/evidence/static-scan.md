# Task 17 — 静态扫描：S1 无残留必产出单体 JSON/HTML 义务

**对象**：`.agents/skills/s1-create-goal-success-contract/` 全部文件（除按契约保留为参考的两个 schema 文件）。

**扫描文件**：`SKILL.md`、`agents/openai.yaml`、`evals/evals.json`、`references/example.md`、`references/run-folder-contract.md`、`references/stage-contract.md`。

**方法**：grep `stage-report.html|\.html|presentation_artifact|html-visualization`、`handoff-envelope|移交信封|单体 JSON|产出 .json`、`markdown-output|单体 Markdown|审核文档`。

**结果**：通过（无任何 S1 正向单体产物义务）。

所有命中分三类，均为预期：

| 类别 | 例子 | 说明 |
| --- | --- | --- |
| 否定句（明确禁止单体产物） | `SKILL.md`3「不再产出单体 JSON 移交信封、Markdown 单文件或 HTML 页面」；`run-folder-contract.md`:7,31,77；`example.md`:93；`openai.yaml`:4 | 正确：显式禁止 |
| 正确归口到 S2–S7 三工件模型 | `stage-contract.md`:9,24,28（「三工件版」Gx 机读含义含 `presentation_artifact.status=generated`） | 正确：§0 显式分叉 S1 run-folder / S2–S7 三工件，此处描述 S2–S7 |
| 误报 | `example.md`:19 出现 `sql-explain.html` | 实为 `sources.jsonl` 示例行的真实来源 URL，非产物义务 |

**保留参考文件（按契约允许）**：
- `references/handoff-envelope.schema.json` — `SKILL.md`:20 标注「S2–S7 共享遗留契约，S1 不再产出」。
- `references/goal-success-contract.schema.json` — `stage-contract.md`:90 标注「字段覆盖参考（语义形状），不再作为产物校验器」。

**已删除确认**：无 `assets/`、无 `markdown-output-contract.md`、无 `html-visualization-contract.md`；s1 目录现存 8 个文件。
