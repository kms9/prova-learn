# S4 阶段契约 — diagnose-learner-frontier（门 G4）

> 本文件治 S4 与决策门 G4。§0 为七阶段共享规则；其余为 S4 专属。

## 0. 共享阶段契约（适用于 S1–S7）

- **编号定义**：`Sx` 是第 x 个执行阶段（Stage），`Gx` 是紧随 Sx、评价该阶段工件能否被下游消费的质量决策门（Gate）。例如 `G1` 是 S1 目标契约质量门，不是学习理论、外部标准或另一个 Skill。
- **“已通过 Gx”的机读含义**：不能凭文件存在、自然语言声称或只看 `positive_artifact` 推断。对作为上游输入的 G1–G6，消费方必须验证兼容移交信封同时满足：`stage_id=Sx`、`status=completed`、`input_validation.status=pass`、具名 `positive_artifact` 非空且通过其 Schema、该门要求的全部 `quality_evaluation.rubric_results[].passed=true`、`quality_evaluation.verdict=pass`、`quality_evaluation.route_to=S{x+1}`，并满足该阶段确认规则；三工件交付还要求 `document_artifact.status=generated` 与 `presentation_artifact.status=generated`。上游 Skill 未与当前 Skill 一起安装时，也必须由调用方提供这些字段或先适配成兼容信封；裸工件只能记为未验证输入。

每个阶段必须产出**三份内容一致、用途不同的工件**：

1. 一份按当前阶段专属结构撰写的完整 Markdown 人审文档；
2. 一份把 Markdown 全部实质内容无损结构化的规范 JSON 移交信封（`handoff-envelope.schema.json`）；
3. 一份由最终 JSON 填充的阶段专用交互 HTML。

统一执行形状：

```text
校验输入契约
→ 收集需求缺口
→ 执行本阶段确认策略
→ 收集可采信证据
→ 先完成阶段专属 Markdown 的事实、分析、结论、量规与路由
→ 将同一内容无损结构化为具名正向工件与 JSON 移交信封
→ 校验 Markdown 章节与 JSON Pointer 的逐项对应
→ 派生并验证阶段专用 HTML
```

- **三工件权威边界**：Markdown 是首要人审文档，JSON 是机器移交的规范表示，HTML 是 JSON 驱动的只读派生视图。Markdown 与 JSON 必须语义等价，不能以“摘要 JSON”丢弃文档中的证据、边界、缺口、失败条件、异议或路由依据。
- **严格生成顺序**：先完成 Markdown 实质内容，再生成 JSON，最后生成 HTML。JSON/HTML 生成后只允许回填路径、工件标识和验证状态等机械信息；实质内容变化必须同步 Markdown 与 JSON 并重新验证。
- **输入契约校验**：至少检查工件类型、schema 版本、必填字段、来源阶段、追溯与上游门状态。失败时 `input_validation.status=fail` 并路由上游，**不得伪造正向工件**。
- **确认状态机**：`mandatory`（S1/S5，未确认不得前进）、`conditional`（S2/S3/S4/S7，遇高风险/分歧/多方案升级为强制）、`inform`（S6 节点推进，告知后继续）。
- **证据来源分类**：`model_hypothesis`/`market_signal`/`external_evidence`/`user_provided_unverified`/`learner_behavior`。**门不得把 `model_hypothesis` 或 `user_provided_unverified` 计为外部证据。**
- **量规结果形状**：`{dimension, evidence[], score, threshold, passed, failure_action, route_to}`；`passed=false` 时 `failure_action` 与 `route_to` 必填。
- **显式未知/阻塞态**：`pending`/`blocked`/`unknown`/`evidence_insufficient`/`research_blocked`/`not_executed`/`version_conflict` 不得被强制为 `pass`。
- **确定性路由**：`pass` 前进；`revise_here` 同阶段重试；`return_upstream` 指向**最早**污染阶段并记录失效下游范围。S7 多归因按上游优先级路由。
- **合并守卫**：快速档仅可在满足条件时合并 S2+S3 或 S4+S5，仍须分别产出工件并依次通过两门；S1、S7 永不合并。
- **强制完整文档**：每次运行都必须遵守当前 skill 的 `markdown-output-contract.md`。`pending` 或 `blocked` 也要完整写明已知事实、未知项、未执行项、当前结论与恢复条件；禁止空标题、空表、`TBD`、`TODO`、示例数据或其他占位内容。
- **强制页面派生**：每次运行都必须基于最终信封生成已填充的本阶段专用 HTML；`pending` 或 `blocked` 也展示真实缺口、当前结论和恢复条件，不得使用通用装载器或空白占位。
- **只生成数据驱动页面**：HTML 是唯一可视化交付，页面视图必须由内嵌规范 JSON 动态渲染；禁止调用制图/图像生成工具，禁止生成、引用或依赖独立图片、插图、知识点图卡或其他静态图片资产。
- **只读展示边界**：页面交互仅用于切换、搜索、筛选、展开和浏览既有数据；不得接受业务输入、导出草稿，或展示 Schema、模板、Markdown/HTML 生成状态及输出说明。
- **交付完整性**：Markdown、JSON 或 HTML 任一缺失，Markdown—JSON 对应失败，或 HTML 三项验证任一失败时，均不得把本次阶段交付报告为完整完成；文档/页面失败不篡改领域门禁本身。

## 1. S4 目的

用对齐目标与先修链的行为证据，确定学习者已经能**独立**解决什么、缺口与误概念在哪里、从哪个节点开始最合适。S4 产出“最近学习前沿”，是“诊断—规划”对（S4–S5）的诊断半边。学习者模型是一等状态：
S4 校验既有记录后产出 §5 定义的版本化 `learner_snapshot`；持久层可概念性地执行加载、追加证据和保留历史，
但这些不是 S4 正向工件字段。S7 才负责把新证据作为事务追加并按版本应用模型补丁；S4 不静默覆盖既有模型。

## 2. S4 输入契约

| 输入 | 是否必填 | 说明 |
|---|---|---|
| `goal_success_contract`（G1 通过） | 必填 | 锁定目标能力与验收方式 |
| `capability_concept_graph`（G3 通过） | 必填 | 提供节点、先修边和每节点可执行诊断项 |
| 既有学习者记录 | 可选 | 须校验身份、时间、来源、有效期；过期证据只作线索，不计为已掌握 |

校验失败时 `input_validation.status=fail`：目标/图谱未过门、关键节点无诊断项或学习者记录身份/版本不一致，分别路由 S1/S3/S4，**不伪造快照**。

> **S1 已迁移到 run-folder 目录交付**：`goal_success_contract` 不再是 JSON 信封，而是 S1 run folder（入口 `workspace/<project-slug>/runs/<最新 run>/INDEX.md`）。锁定目标能力与验收方式时按 run-folder 七项校验确认 G1 通过，并从 `goal-contract.md`/`capabilities.jsonl`/`INDEX.md` 取字段；`capability_concept_graph` 与 `learner_snapshot` 仍为 JSON 信封（待后续迁移）。

## 3. S4 确认策略（`conditional`）

告知诊断范围、用途和有效期；展示初步节点状态、误概念和学习前沿。学习者对结论有异议、涉及高风险分班/跳级、或自述与行为冲突时升级为强制：对**争议节点追加测试**，从不以自述直接覆盖行为证据。冷启动仅告知将采集哪些初始证据。

## 4. S4 诊断规则（基于行为证据）

- **先声明推断规则再采证**：对每个节点预先说明什么观察算“掌握/未掌握/证据不足”，避免事后调分。
- **任务覆盖**：沿目标与先修链使用解释、预测、反例、诊断、比较、迁移和置信度任务；题目集须含明显错、隐蔽错、无错和需升级题，防止只测口号识别。
- **证据角色**：优先使用 S2/S3 已追溯的真实任务、失败案例、Benchmark 与误概念设计题目；社区材料只可生成待测假设，不得直接决定正确答案或学习者状态。
- **时效检查**：诊断动态工具、法规、岗位或前沿节点前检查来源有效期；过期或缺失关键真实任务/失败条件时返回 S2，节点—测评映射本身错误时返回 S3。
- **每条观察记录**：正确性、推理过程、提示层级、耗时（可得时）、置信度、错误类型。
- **三项区分**：`答对`（可能猜对或只识别）、`独立会做`（无提示或低提示完成）、`能迁移`（未见/变式情境通过）。
- **提示—掌握不变量**：`tested_mastered` 必须有同一节点在 `hint_dependency.level=none|low` 下的独立证据；只有 `medium|high|unknown` 提示证据时不得标为 `tested_mastered`，须保持 `tested_not_mastered`/`insufficient_evidence` 并安排撤除支架后的复测。
- **提示等级跨阶段映射**：S4 诊断观察进入 S7 时，`none→none`、`low→low`、`medium→moderate`、
  `high→high`；`unknown` 只有在没有可用提示记录时映射为 `not_executed`。该映射保留的是实际行为证据，
  不得从 S6 计划的提示阶梯反推学习者已使用的提示等级。
- **递归定位前沿**：从目标节点回溯，找到最近一个证据支持“可学习但尚未掌握”的节点作为 `learning_frontier`，附证据与理由；多竞争前沿时禁止 S4+S5 合并。
- **证据归并**：自评/年限/偏好问卷只用于选题或线索，绝不直接写入“已掌握”；原始行为、推断状态与路由决策三层分离。

## 5. S4 工件字段（`learner_snapshot.content`）

`learner_id`、`model_version`（整数且 `>=1`；表示可被 S7 加载的已建立快照版本，冷启动不使用版本 0）、`as_of`（诊断时间点，可选）、`node_states[]`（`node_id`/`status[tested_mastered|tested_not_mastered|insufficient_evidence|untested]`/`evidence_refs[]`/`error_type`/`hint_dependency{level,evidence_refs}`/`confidence_calibration{self_confidence,observed_alignment}`）、`learning_frontier{nearest_learnable_node_id,evidence_refs[],rationale,alternative_candidate_node_ids?}`、`misconceptions[]`（`code/description/evidence_refs[]/related_node_ids?`）、`capability_gaps[]`、`transfer_performance{status,evidence_refs[],summary?}`、`diagnosis_evidence_mapping[]`（`conclusion→evidence_refs`）、`items_needing_retest_or_human_confirmation[]`（`kind[retest|human_confirmation]`）、`evidence_validity{valid_until,stale_evidence_refs,policy?}`。

证据条目本体放在信封 `evidence_collected`（`provenance=learner_behavior`），工件用 `evidence_refs` 引用。

## 6. S4 量规（门 G4）

| 维度 | 阈值类型 | 阈值 | 证据来源 |
|---|---|---|---|
| 测量与目标对齐度 | 关键节点均有对齐诊断项 | true | node_states ∩ goal_success_contract |
| 证据充分性 | 关键结论≥2 对齐观察或显式不足 | true | diagnosis_evidence_mapping |
| 猜对识别 | 区分答对/独立/迁移 | true | node_states.error_type, transfer_performance |
| 提示依赖记录 | 每节点 hint_dependency 已记录 | true | node_states.hint_dependency |
| 错误分类一致性 | error_type 与证据一致，可审计 | true | node_states.error_type |
| 偏差控制 | 自述/年限未覆盖行为证据 | true | confidence_calibration, evidence_collected |
| 结论可解释性 | 每条结论→证据可追溯 | true | diagnosis_evidence_mapping, learning_frontier.evidence_refs |
| 诊断素材有效性 | 真实任务/失败/Benchmark 可追溯且动态来源未过期 | true | S2/S3 source refs + evidence_validity |

G4 通过当且仅当**所有维度** `passed=true` 且学习前沿有在有效期内的多项行为证据。

## 7. S4 路由

| verdict | route_to | 触发 |
|---|---|---|
| `pass` | S5 | 全部 G4 维度通过，学习前沿有多项有效证据 |
| `revise_here` | S4 | 证据不足、猜对未识别、提示/置信度缺失、争议节点未复测 |
| `return_upstream` | S3 | 诊断题无法产生目标证据、图谱节点/先修边无效 |
| `return_upstream` | S2/S3 | 诊断暴露来源缺失、偏差或图谱事实错误 |
| `blocked` | S4 | 无真实学习者回答；冷启动待证；关键记录失效且无法补证 |

## 8. S4 安全/阻塞态

- 无真实回答 → 只产出诊断任务，`status=pending`，不模拟行为。
- 冷启动 → `unknown`/`insufficient_evidence`，路由 S4 建立初始证据；形成首个可持久化快照时版本从 1 开始，**不得**以版本 0 创建“全部未掌握”画像。
- 单题/纯自评/口号识别 → 关键节点保持 `insufficient_evidence` 或 `untested`，G4 不通过。
- 证据过期 → 移入 `evidence_validity.stale_evidence_refs`，只作线索，关键结论需复测后再生效。
- S4+S5 合并须满足：确认零基础、图谱起点明确、路径近线性、任务低风险；四者任一不满足即拆回两步。
