# check-rubric — S1 / 决策门 G1（目标契约质量判定标准）

> 本量规是 `check-goal-success-contract` 的判定标准，与阶段 skill `create-goal-success-contract/references/stage-contract.md` §6 保持一致。检查者独立重判，不采信被检工件自报的 `verdict`。

## 判定流程

1. 结构校验：信封通过 `handoff-envelope.schema.json`；`positive_artifact` 通过 `goal-success-contract.schema.json`。
2. 逐维判定下表（每维：证据 / 评分 / 阈值 / `passed`）。
3. 确认复核（S1 强制确认）。
4. 证据来源复核（外部证据门）。
5. 汇总裁决与路由。

## G1 维度量规

| 维度 | 阈值类型 | 通过阈值 | 证据来源（指向被检工件字段） |
|---|---|---|---|
| 目标可观察性 | 每项能力≥1 可观察证据 | ≥1 | `content.observable_capabilities[].observable_evidence` |
| 成功标准可判定性 | `unseen_or_transfer_required` | true | `content.final_assessment.unseen_or_transfer_required` |
| 场景真实性 | `target_scene` 非空 | true | `content.target_scene` |
| 外部现实校准度 | 术语已校正或确认无歧义 | true | `content.terminology_corrections` + 确认记录 |
| 强制来源类别覆盖 | wiki/recruiting/interview 均 covered 或可审计 | true | `content.external_research_seed.category_coverage` |
| 边界清晰 | exclusions 非空 | ≥1 | `content.exclusions` |
| 约束完整 | 时间/形式约束存在 | true | `content.constraints` |
| 目标—验收一致 | pass_rules 与能力、验收对齐 | true | `content.pass_rules` ↔ 能力阶梯 ↔ final_assessment |

## 通过条件（G1 pass）

当且仅当**全部**满足：

- 所有上表维度 `passed=true`；
- `confirmation.status ∈ {confirmed, guardian_and_learner_confirmed}`（强制确认已解）；
- `external_research_seed.search_executed=true`，且 `sources` 仅含 `market_signal`/`external_evidence`（无 `model_hypothesis` 伪装为外部证据）；
- 无 `criticality=critical` 且 `gate_effect=block` 的未决证据缺口。

通过 → `verdict=pass`、`route_to=S2`。

## 不通过时的路由

| 触发 | verdict | route_to |
|---|---|---|
| 目标/成功标准不可观察、术语漂移、预检未执行或仅模型总结 | revise_here | S1 |
| 缺强制确认 / 缺联网预检 / 关键缺口未解 | blocked | S1 |
| 用户根本改变目标（信封或上游指示目标已变） | return_upstream | S1 |

> S1 是最早阶段，故 `return_upstream` 与 `revise_here` 的 `route_to` 均为 S1；区别在于缺陷是否源于“目标本身被改变”（return_upstream）还是“当前目标契约未达标”（revise_here）。

## 反模式（检查者不得犯）

- 直接采信被检工件自报 `verdict=pass` 而不逐维重判。
- 把 `model_hypothesis` 或 `user_provided_unverified` 计为外部证据。
- 结构非法却仍给出 `pass`。
- 修改被检工件或替 S1 生成新目标。
