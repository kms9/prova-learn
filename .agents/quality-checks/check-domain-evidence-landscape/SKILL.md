---
name: check-domain-evidence-landscape
description: 独立质量检查 skill，用于判定 S2（create-domain-evidence-landscape）的输出工件是否达到决策门 G2。只要需要独立复核 S2 的 domain_evidence_landscape 移交信封是否合格、是否应该放行进入 S3，就使用本 skill。它不重新做领域研究，只按 G2 量规逐维复核并给出可追溯的 pass / revise_here / return_upstream / blocked 裁决。
---

# 领域证据全景质量检查（check S2 / G2）

独立复核 S2 的输出是否达标。不要替 S2 重做研究；只读、只判。

## 开始前

1. 读取 [check-rubric.md](references/check-rubric.md)（G2 量规 = 判定标准）。
2. 读取 [quality-check-result.schema.json](references/quality-check-result.schema.json)（本检查的输出结构；与其他 check-* 共享同一份）。
3. 取待检 S2 移交信封；按需参考阶段 skill 的契约 `.agents/skills/create-domain-evidence-landscape/references/stage-contract.md` 与三份 schema。
4. 仅在需要理解输出形状时读取 [example.md](references/example.md)；案例为设计夹具。

## 执行

1. 结构校验：待检信封能否通过 `handoff-envelope.schema.json`；其 `positive_artifact` 能否通过 `domain-evidence-landscape.schema.json`。任一不通过即记入 `structural_validation.errors`。
2. 逐维复核 G2（见 check-rubric.md）：实际联网执行、强制来源类别覆盖、来源可靠性与时效、结论可追溯性、关键主题覆盖率、STORM 视角与问题多样性、后续追问深度、岗位/面试样本代表性、时效与地区适配性、事实/市场信号/推断分离、争议平衡、证据缺口透明度。每维给出证据、评分、阈值、`passed`。
3. 强制联网复核（G2 硬门槛）：`research_run_manifest.online=true` 且 `execution_status=completed`；`online=false`/`not_executed`/`blocked` 直接失败，用户确认不能豁免。
4. 证据来源复核：`model_hypothesis` 与 `user_provided_unverified` 不得计为外部证据；`market_signal`（如 JD、面经）不得被写成 `fact`；百科只作为全景入口，不可单独支撑高风险或争议结论。
5. 复核独立性：不得把 S2 自报的 `verdict=pass` 当作结论；按本量规独立重判，特别警惕“少量同源博客即共识”“搜索结果数量当作证据质量”。
6. 汇总：所有维度 `passed` 且 `research_executed=true` 且无关键缺口阻塞建图 → `pass`、`route_to=S3`；否则按最早缺陷给 `revise_here`/`return_upstream`/`blocked` 与 `route_to`。

## Fail closed

- 待检信封结构非法且无法定位工件 → `verdict=blocked`，不臆造通过。
- 无联网能力或 `research_run_manifest.online=false` → 不得 `pass`，路由 S2。
- 把模型记忆伪装成外部证据、或把市场信号写成事实 → 对应维度 `passed=false`。
- “找不到资料”应记 `gap` 而非 `not_applicable`；同源转载博客不得计为独立来源。
- 只能给出复核结论与路由，不得修改被检工件、不得替 S2 生成新的领域证据。

## 输出

只输出符合 `quality-check-result.schema.json` 的 JSON：`stage_id=S2`、`gate_id=G2`、`dimension_results[]`、`verdict`、`route_to`、`evidence_summary`、`checked_at`。每个不通过维度必须带 `failure_action` 与 `route_to`。
