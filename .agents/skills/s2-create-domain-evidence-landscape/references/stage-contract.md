# S2 阶段契约 — S1 问题的领域研究回答（门 G2）

> 本文件治理 S2 与 G2。逐文件字段、稳定 ID、状态机和验证规则见
> [run-folder-contract.md](run-folder-contract.md)。

## 0. 阶段共享规则在 S2 的落地

- `S2` 是执行阶段；`G2` 是判断 S2 回答能否被 S3 消费的门，不是理论或另一个 Skill。
- S1 与 S2 使用同一个 `workspace/<project-slug>/runs/<run-id>/` LLM Wiki。S1 文件位于根目录，
  S2 文件位于 `s2/`，根 `INDEX.md` 注册阶段入口。
- S2 不产出共同 JSON 信封、`domain_evidence_landscape` 单体 JSON、单体审核 Markdown 或 HTML。
- 记录型材料使用 JSONL，审核/回答/索引/量规使用 Markdown；九文件全部必需。
- 证据区分 `model_hypothesis`、`market_signal`、`external_evidence`、
  `user_provided_unverified`、`learner_behavior`。前两类以外的模型假设/未核验主张不能计入外部证据。
- `pending`、`blocked`、`unknown`、`evidence_insufficient`、`research_blocked`、
  `not_executed` 不得被强制写成 pass。
- S2 是 conditional confirmation；高风险、活跃分歧、多种后果显著的回答或范围变化升级为 mandatory。
- 快速档可以连续执行 S2+S3，但必须先写完 S2 九文件并通过 G2，再评价 G3。

## 1. 目的

把 S1 已确认的研究问题变成可审计的明确回答，建立进入 S3 所需的领域事实基础。S2 回答“依据支持什么结论”，
识别真实任务、能力、知识、技能、产物、共识、分歧、误概念、边界和开放问题；S3 才组织正式能力图谱。

## 2. 输入契约

| 输入 | 必填 | 来源 |
|---|---|---|
| 最新 S1 根 `INDEX.md` | 是 | `workspace/<project-slug>/runs/<run-id>/INDEX.md` |
| 目标、范围、验收、排除项 | 是 | `goal-contract.md` |
| S1 priority questions 与六源种子 | 是 | `research-brief.md` |
| 可观察能力 | 是 | `capabilities.jsonl` |
| S1 预检来源与覆盖 | 是 | `sources.jsonl`、`coverage.md` |
| S1 确认与 G1 状态 | 是 | `confirmation.md`、`g1-evaluation.md`、`verification.md` |
| S7 evidence feedback | 否 | 局部补证时提供 |

G1 通过必须验证 S1 的七项机读条件，不能依赖一句“G1 已过”。S1 预检类别不等于 S2 六源通道，
S2 必须重新查询、核验、分类和评价实际来源。

输入无效时不得伪造回答。若 run 可安全写入，建立阻断态 `s2/` 诊断区并在根索引标明 route=S1；
若连 run 身份也无法确定，仅返回输入缺口而不创建任意目录。

## 3. 确认策略

默认 `conditional`。研究开始前可展示问题、视角、六源通道、深度与预计限制。

以下情况升级 mandatory：

- 高风险或快速变化主题；
- 重要问题存在活跃分歧或竞争范式；
- 来源限制会实质改变结论；
- 研究发现目标、成功证据或范围需要实质修改；
- 多个回答方案会明显改变 S3 结构。

未确认时保留 `pending`，G2 不通过。

## 4. 强制研究协议

- 必须真实联网；模型知识只产生假设、视角、问题和检索词。
- 至少六视角：术语历史、理论标准、实践任务、招聘市场、评估证据、批评前沿。
- 至少两轮；冲突或新发现触发追问。查询重复或结果减少不等于饱和。
- 六源通道固定为岗位、书课、论文、社区、官方标准、真实产物，各自记录状态、理由、独立数、关键性和门影响。
- 岗位适用时至少 3 个当前样本/2 个组织；面试适用时至少 2 组。不足写 undersample gap。
- 书课比较权威教材/Handbook/大学课程/认证；论文覆盖综述、代表、近三年前沿、批评或负面结果；
  社区只提供痛点、误解、失败、变通、争议和新兴信号；标准给规范边界；真实产物给成功/失败条件。
- 百科、搜索结果页和聚合页只是入口，最终结论追到可访问原始或权威来源。
- 来源统一抽取为 Task/Capability/Knowledge/Skill/Evidence 和必要扩展对象。
- 核心候选默认至少有岗位/真实任务、书课或标准、论文/产物/经验证实践三类独立支持。
- 连续两轮没有新增一级能力域或关键二级问题族，才能记结构饱和。

详细规则见 [six-source-information-collection.md](six-source-information-collection.md)。

## 5. 输出合同

S2 在同一 run 的 `s2/` 写九个文件：

| 文件 | 作用 |
|---|---|
| `INDEX.md` | S2 阶段入口、问题回答摘要、G2 和下游指引 |
| `research-log.md` | 视角、查询、轮次、追问、纳入排除和未执行项 |
| `sources.jsonl` | 实际核验来源、可靠性、独立组、时效、证据角色 |
| `coverage.md` | 六源覆盖、独立样本、多源矩阵 |
| `evidence-items.jsonl` | 归一化 Task/Capability/Knowledge/Skill/Evidence 等 |
| `research-answers.md` | 按 S1 priority questions 逐题明确回答；首要人审交付 |
| `answer-validation.md` | 每题八维校验、共识/分歧/缺口、饱和/成熟度/刷新 |
| `g2-evaluation.md` | G2 分维量规、裁决、路由 |
| `verification.md` | 九文件、映射、引用、反占位、风险和命令收尾 |

根 `INDEX.md` 必须新增或更新独立 `## 阶段输出` 表的 S2 行，链接 `s2/INDEX.md`。S1 内容和 G1 历史保持不变。

## 6. 问题回答与八维校验

每个 S1 priority question 恰好对应一个 `RQ-###` 和 `ANS-###`。每题保存问题原文、上游位置、关键性、
明确回答、answer/claim/knowledge status、置信度、边界、支持证据、反证/替代解释、可观察相关性、缺口、
恢复动作和 S3 输入。

每个答案恰好评价：

1. `source_coverage`
2. `provenance_separation`
3. `source_independence`
4. `reliability_authority`
5. `timeliness_region_fit`
6. `contradiction_balance`
7. `observable_relevance`
8. `boundary_gap_clarity`

结果为 `pass|fail|insufficient|not_applicable`，非 pass 必须给 failure action、route 和 confidence impact。
关键问题任一关键维度非 pass，则不能记 `answered`，G2 不通过。

## 7. G2 量规

| 维度 | 通过条件 | 证据 |
|---|---|---|
| 输入有效 | G1 七项通过，priority questions 可解析 | S1 根文件 |
| 实际联网 | online completed、至少两轮 | `research-log.md` |
| 多视角与追问 | 至少六视角，冲突/新发现有追问 | `research-log.md` |
| 六源覆盖 | 六行齐全、独立数和 gate effect 可审计 | `coverage.md` |
| 来源质量 | 可靠、当前、地区匹配、转载去重 | `sources.jsonl` |
| 问题映射 | 每个 S1 问题恰好一个 RQ/ANS | `research-answers.md` |
| 八维回答 | 所有关键答案八维通过 | `answer-validation.md` |
| 可追溯性 | ANS/ITEM/E/GAP 引用全部解析 | 九文件 |
| 证据边界 | 事实、市场、社区、假设分离，争议平衡 | 回答与校验 |
| 饱和与成熟度 | 饱和达到且至少 L1 | `answer-validation.md` |
| 时效治理 | 稳定/动态知识有刷新条件 | `answer-validation.md` |
| 确认 | 升级 mandatory 时已确认 | `g2-evaluation.md` |
| 交付完整性 | 九文件、根索引、无占位、verification=verified | `verification.md` |

G2 pass 还必须满足 [run-folder-contract.md](run-folder-contract.md) §15 的九项机读条件。

## 8. 路由

| verdict | route | 条件 |
|---|---|---|
| `pass` | S3 | G2 全维和九项机读条件全部通过 |
| `revise_here` | S2 | 研究浅、来源失衡、答案部分/未答、八维失败、饱和不足 |
| `return_upstream` | S1 | 目标、成功证据或范围实质失效 |
| `blocked` | S2 | 无联网或关键来源能力不可用 |

S3/S7 返回证据反馈时在 S2 局部补证，保留未受影响回答、来源和 ID；记录失效下游范围。

## 9. 安全态与完整性

- 无联网 → `research_blocked`，不能由用户确认豁免外部证据门。
- 找不到来源 → `gap`，不能伪装成 not applicable。
- SEO 转载链按一个独立组计数；广告、JD、社区或模型自述不能升级成规范事实。
- S4/S6 的学习者行为不在 S2 代写；领域常见误概念不能冒充该学习者诊断。
- 阻断也写完整九文件和根索引状态，不使用空标题、空表、TBD、TODO、示例数据占位。
- 九文件任一缺失、根索引未更新、问题遗漏、八维不全或引用失败，都不得报告完整完成或进入 S3。

## 10. 快速档与研究档

- S2+S3 只有在领域成熟、单一范式、低风险、来源质量均匀时允许连续执行；G2 必须先通过。
- 竞争范式、活跃分歧、快速变化、来源不均或高风险时分开执行。
- 研究档声明需要独立专家评审但没有证据时，记录 pending/not_executed，不声称研究档完成。
