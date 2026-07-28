## Why

S1（`create-goal-success-contract`）当前按"完整 Markdown 人审文档 → 无损结构化 JSON 移交信封 → JSON 驱动 HTML"交付三件单文件工件。这套交付对人检索不友好，把目标校准结果与预检证据锁死在单体文件里，且与项目内已验证的 `storm-evidence` 式证据治理落盘方式（`sources.jsonl` / `evidence_table.md` / `coverage.md` / `verification.md`，稳定 ID 跨文件互引、状态机带 guard）不一致。

目标：把 S1 改为 **LLM Wiki / run-folder 目录交付**——在 `workspace/<project-slug>/runs/<run-id>/` 下写一组固定命名文件，记录型用 `.jsonl`、汇总/审计型用 `.md` 表，状态机带 guard、稳定 ID 跨文件互引、`INDEX.md` 为下游读取入口。下游阶段经 `INDEX.md` 读取上游，不再依赖 JSON 移交信封。

## What Changes

- **S1 不再产出**单体 Markdown 审核文档、JSON 移交信封（`handoff-envelope.schema.json` 1.3.0）或交互 HTML（`assets/stage-report.html`）。
- **S1 改为产出 run folder**（11 文件）：`INDEX.md` / `sources.jsonl` / `evidence_table.md` / `coverage.md` / `capabilities.jsonl` / `terminology.jsonl` / `goal-contract.md` / `research-brief.md` / `confirmation.md` / `g1-evaluation.md` / `verification.md`。
- 新增 `references/run-folder-contract.md`（逐文件字段契约、稳定 ID、状态机 guard、反占位、跨文件互引校验）；删除 `references/markdown-output-contract.md` 与 `references/html-visualization-contract.md`，删除 `assets/stage-report.html`（S1 副本）。
- 重写 S1 `SKILL.md`（状态机 + guard + 产物/字段契约 + 硬性规则）、`stage-contract.md`（§0 共享交付模型分叉为 S1 run-folder / S2–S7 三工件）、`example.md`、`evals/evals.json`、`agents/openai.yaml`。
- "已通过 G1"由信封字段校验改为 run-folder 机读七项校验。
- 下游 S2 输入契约改为读取 S1 run folder 入口（`…/runs/<最新>/INDEX.md`）；S3/S4/S5 输入契约加防御性说明（`goal_success_contract` 现为 run folder）。S2–S7 自身产出仍为三工件，待后续迁移。
- `AGENTS.md` §4.2 / §5 / §7 / §13 更新为反映 run-folder 交付。

## Capabilities

### Modified Capabilities

- `goal-success-contract`（S1）：交付形态从三工件改为 run-folder 目录；语义名 `goal_success_contract` 保留，物理形态变为由 `INDEX.md` 标识的 run folder。
- S2–S7 上游消费：读取 `goal_success_contract` 的方式从 JSON 信封改为 run-folder `INDEX.md`（S2 全面改写输入契约；S3/S4/S5 防御性说明）。

### Supersedes

- 本 change 的 S1 切片**取代** `add-seven-stage-html-visualizations` 对 S1 的 `presentation_artifact` + `assets/stage-report.html` + `html-visualization-contract.md` 要求（S2–S7 的 HTML 可视化不受影响，继续生效）。

## Impact

- 影响 `.agents/skills/s1-create-goal-success-contract/` 全部文件；改写 `.agents/skills/s2-create-domain-evidence-landscape/` 的输入契约与上游消费语；为 `s3/s4/s5` 的输入契约各加一行说明。
- 影响 `AGENTS.md` §4.2 / §5 / §7 / §13。
- 共享 `handoff-envelope.schema.json` 与 `goal-success-contract.schema.json` **保持字节不变**（S2–S7 仍用；S1 仅作遗留/字段参考）。
- 不引入运行时网络依赖或独立图片资产；run folder 内禁止 HTML 与图片。
- `scripts/run_skill_evals.py` 当前只能评分单个 JSON，**暂无法对 run folder 目录评分**——S1 `evals.json` 已重写期望值，但跑通需后续扩展 harness（列为后续追踪）。
- S2–S7 完整迁移到 run-folder 产出为后续 change，不在本 change 范围。
