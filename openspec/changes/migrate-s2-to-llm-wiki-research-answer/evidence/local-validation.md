# S2 LLM Wiki 研究回答迁移 — 本地验证

> 日期：2026-07-28  
> change：`migrate-s2-to-llm-wiki-research-answer`  
> 范围：规格、S2/S3 Skill、静态合同与 S1→S2 只读输入冒烟  
> 不包含：真实 S2 联网研究、外部 Skill eval、S3 端到端产物、生产或长期门

## 已通过

- S2 `quick_validate.py`：pass。
- S3 `quick_validate.py`：pass。
- S2/S3 现存 JSON（eval 与 Schema）全部可由 `jq` 解析。
- S2 旧 `markdown-output-contract.md`、`html-visualization-contract.md`、两个 JSON Schema 和
  `assets/stage-report.html` 均已移除。
- S2/S3 Markdown 仓库内相对链接解析：pass；运行时 `s2/INDEX.md` 示例不伪装成仓库静态链接。
- `git diff --check -- AGENTS.md .agents/skills openspec docs`：pass。
- `openspec validate migrate-s2-to-llm-wiki-research-answer --type change --strict --no-interactive`：pass。
- 三份受影响基础 spec strict validation：pass。
  - `create-domain-evidence-landscape`
  - `personalized-learning-stage-contracts`
  - `stage-html-visualizations`

## `senior-teaching-researcher` 只读冒烟

- 输入：`workspace/senior-teaching-researcher/runs/run-20260727-234421/`。
- S1 根文件数：11。
- `research-brief.md` priority questions：5。
- G1 文件声明为 pass/route S2，verification 声明为 verified。
- 当前 `s2/` 不存在：符合“尚未执行真实 S2，不伪造阶段输出”。
- 本次冒烟没有修改 workspace。

## 未通过或未运行

- 全仓 `openspec validate --all --strict --no-interactive`：12 passed、1 failed；唯一失败是既有
  `migrate-s1-to-llm-wiki-delivery` 缺 design/specs。见错误台账 ERR-104；本次不越界修复。
- S2 外部 eval：未运行。现有 eval harness 对目录型产物的通用评分仍是既有后续项。
- 真实多轮联网、六源覆盖、逐题八维校验、结构饱和、L1 与 G2：未执行；因此
  `workspace/senior-teaching-researcher` 不能声称已完成 S2。
- S3 真实消费新 S2 九文件的端到端运行：未运行。
