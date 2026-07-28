---
name: al-01-create-goal-success-contract
description: 将模糊学习诉求、职业目标或能力愿望校准为经过外部预检、可观察、可验收并由用户确认的 goal_success_contract。交付物为运行目录下的 LLM Wiki run folder（workspace/<project-slug>/runs/<run-id>/），内含固定命名文件（sources.jsonl 记录预检来源、evidence_table.md / coverage.md 汇总表、capabilities.jsonl / terminology.jsonl 记录、goal-contract.md / research-brief.md / confirmation.md / g1-evaluation.md / verification.md / INDEX.md 主索引），由状态机带 guard 控制写入、稳定 ID 跨文件互引。不再产出单体 JSON 移交信封、Markdown 单文件或 HTML 页面，也不生成独立图片。只要用户要开始新的个性化学习目标、改变既有目标、定义"学会"的证据，或需要校正岗位/领域名称，就使用本 skill。
---

# 目标与成功契约（S1）

把目标定义错误隔离在流程最前端。不要直接生成课程表，也不要把投入时长、看完材料或选择题分数当成能力。S1 把校准结果与强制预检证据落盘为一个**可被人和代理独立检索的 run folder**（LLM Wiki 方式），供 S2–S7 经 `INDEX.md` 读取。

## 概述

S1 负责"目标校准"。它把模糊诉求、一次有边界的强制联网预检和用户确认，编译为可观察、可验收的目标契约，并把**预检来源**（`sources.jsonl`）、**来源↔结论支撑**（`evidence_table.md`）、**六类覆盖**（`coverage.md`）、**能力/术语记录**（`capabilities.jsonl`/`terminology.jsonl`）、**目标契约编译稿**（`goal-contract.md`）、**S2 研究简报**（`research-brief.md`）、**确认**（`confirmation.md`）、**G1 量规**（`g1-evaluation.md`）和**终态**（`verification.md`）写入 `workspace/<project-slug>/runs/<run-id>/`，以 `INDEX.md` 为下游入口。落盘方式参照 `storm-evidence` skill 的证据治理产物。

## 引用加载

- 在写 run folder 之前，阅读 [stage-contract.md](references/stage-contract.md)（§0 共享交付模型 + S1 阶段逻辑）。
- 在创建任何 run-folder 文件之前，阅读 [run-folder-contract.md](references/run-folder-contract.md)（逐文件字段契约、稳定 ID、状态机 guard、反占位、跨文件互引校验）。
- 仅在需要理解输出形状时阅读 [example.md](references/example.md)；案例数据是设计夹具，不是真实观察。
- [goal-success-contract.schema.json](references/goal-success-contract.schema.json) 仅作**字段覆盖参考**（语义形状），不再作为产物校验器；S1 不产出 JSON 信封。
- [handoff-envelope.schema.json](references/handoff-envelope.schema.json) 为 S2–S7 共享遗留契约，S1 不再产出。

## run folder 布局

```text
<cwd>/workspace/<project-slug>/runs/<run-id>/
  INDEX.md            主索引：G1 verdict/route + 文件清单 + 运行历史指针（下游读取入口）
  sources.jsonl       预检来源记录
  evidence_table.md   来源 ↔ S1 结论 支撑表
  coverage.md         六类预检覆盖表
  capabilities.jsonl  可观察能力记录
  terminology.jsonl   术语校正记录
  goal-contract.md    目标/场景/验收/通过规则/范围/排除/约束（人审编译稿）
  research-brief.md   domain_research_brief（S2 直接消费）
  confirmation.md     确认问题/回答/状态 + 开放问题 + 已确认项
  g1-evaluation.md    G1 量规逐维表 + verdict + route
  verification.md     状态机终态 + 统计 + 未决风险 + 命令
```

- `project-slug` = 校准后目标的 kebab-case，稳定不变；根本改变目标时开新 slug。
- `run-id` = `run-YYYYMMDD-HHMMSS`；同项目多次运行并列在 `runs/`，下游按时间戳取最新 run 的 `INDEX.md`。

## 状态机

按状态机执行，不要跳过 guard（字段契约见 [run-folder-contract.md](references/run-folder-contract.md)）：

```text
idle
  -> input_validated
  -> preflight_executed
  -> sources_normalized
  -> coverage_classified
  -> capabilities_extracted
  -> evidence_table_ready
  -> goal_contract_compiled
  -> confirmation_resolved
  -> g1_evaluated
  -> risk_reviewed
  -> verified

repair loops:
  preflight_executed -> research_blocked (无联网) -> idle
  confirmation_resolved -> pending (未确认) -> 收集确认
  g1_evaluated -> revise_here -> capabilities_extracted
```

## 状态机 Guard

| 迁移 | 必须满足 |
| --- | --- |
| `idle -> input_validated` | 至少一个目标问题或使用场景；记录缺失约束，不把推断写成已确认事实。 |
| `input_validated -> preflight_executed` | 强制联网预检真实执行（百科/JD/面试样本 + 六类来源入口）；无联网能力只能进 `research_blocked`。 |
| `preflight_executed -> sources_normalized` | 每条可用来源有稳定 `source_id`、`type`、`provenance`、`category`、`retrieved_at`；模型知识标 `model_hypothesis`/`trace_only`。 |
| `sources_normalized -> coverage_classified` | `coverage.md` 六类固定类别各出现一次，记 `covered`/`not_applicable`/`gap` + `reason` + `gate_effect` + `source_ids`。 |
| `coverage_classified -> capabilities_extracted` | `capabilities.jsonl` 每项能力 ≥1 `observable_evidence`；`terminology.jsonl` 只保留理解当前目标所必需的校正。 |
| `capabilities_extracted -> evidence_table_ready` | 每条非常识 S1 结论绑定 accepted Source IDs；`unsupported`/`trace_only` 不入主表。 |
| `evidence_table_ready -> goal_contract_compiled` | `goal-contract.md` 与 `research-brief.md` 写齐目标/场景/验收/规则/范围/排除/约束与六源种子。 |
| `goal_contract_compiled -> confirmation_resolved` | 强制确认完成：目标能力、成功证据、范围、岗位/职级、地区/语言、时效、时间/资源/形式、风险、排除项；`confirmation.status=confirmed`。 |
| `confirmation_resolved -> g1_evaluated` | `g1-evaluation.md` 逐维评价，记录 evidence/score/threshold/passed/failure_action/route。 |
| `g1_evaluated -> risk_reviewed` | `verification.md` 汇总未决风险；`high` 风险未解决不得 `verified`。 |
| `risk_reviewed -> verified` | G1 全维 `passed=true` + `confirmed` + sources.jsonl ≥1 accepted external_evidence + 跨文件 ID 全可解析 + 无占位符；写 `INDEX.md`。 |

## 执行

1. 校验至少一个目标问题或使用场景；记录缺失约束，不把推断写成已确认事实。
2. 收集目标场景、受众、岗位族/目标职级、地区/行业/语言、时效窗口、时间、资源、输出形式、排除项、风险级别和最终验收方式。
3. 执行轻量外部预检：术语/别名/相邻概念；相关真实任务/岗位/实践；面试/实操/认证等可观察评估；S2 可追溯的岗位、书课、论文、社区、标准与真实产物六类来源入口。结果落 `sources.jsonl`，`provenance` 严分 `external_evidence`/`market_signal`/`model_hypothesis`。
4. `coverage.md` 记六类预检覆盖（固定类别，各一次）+ S2 六源映射说明；不按类别名自动升级证据等级。
5. 把目标反推成可观察能力阶梯（`capabilities.jsonl`，区分记忆/解释/应用/诊断/迁移/创造）和未见验收任务（`goal-contract.md`）。
6. `evidence_table.md` 绑定能力/术语/目标边界结论到 accepted 来源；`research-brief.md` 锁定领域边界与六源种子，只生成检索种子，不在 S1 宣称完成领域全景。
7. 展示术语校正、目标选项、成功证据、范围和关键假设，执行强制确认；结果落 `confirmation.md`。
8. `g1-evaluation.md` 按 G1 量规逐项评价；`verification.md` 收尾终态与未决风险；`INDEX.md` 写主索引。

用户已经否决、替换或声明无关的旧目标、旧场景和案例内容不得进入当前 run folder，也不得为了说明"不做什么"而复述。`terminology.jsonl` 只保留理解当前目标所必需的真实术语校正。

## Fail closed

- 无联网/检索能力时，`verification.md.state=blocked`，保持 G1 失败；不要用模型记忆替代预检。
- 强制确认未完成时，`confirmation.status=pending`，保持不前进；不进入 S2。
- 关键来源缺失时在 `coverage.md` 记 `gap`、在 `verification.md` 记重要性与门禁影响；"找不到"不等于 `not_applicable`。
- S1 的少量岗位或资料样本只能用于校准目标与生成查询，不得被包装成六源覆盖、领域共识或完整能力模型。
- 用户根本改变目标时重新执行 S1（开新 run），不在下游静默改写目标。
- 跨文件 ID 不可解析、必需文件缺失或存在占位符时，本次交付不得报告为完整完成，G1 不得 `pass`。

## 输出

每次运行必须写出一个完整的 run folder（11 文件，见"run folder 布局"），由状态机按 guard 推进到 `verified`：

- `sources.jsonl` / `coverage.md`：真实执行的预检来源与六类覆盖；
- `evidence_table.md`：来源↔S1 结论支撑表；
- `capabilities.jsonl` / `terminology.jsonl`：可观察能力与术语校正记录；
- `goal-contract.md`：目标/场景/验收/通过规则/范围/排除/约束人审编译稿；
- `research-brief.md`：S2 直接消费的领域研究简报；
- `confirmation.md`：强制确认结果与开放问题；
- `g1-evaluation.md`：G1 量规逐维 + verdict + route；
- `verification.md`：终态 + 统计 + 未决风险；
- `INDEX.md`：下游读取入口（结论先行 + 文件清单 + 运行历史指针）。

待确认或阻断时仍写出含真实缺口、处理记录和路由的诊断 run folder（11 文件齐全，不得用空标题/`TBD`/`TODO`/示例占位）。S1 run folder 内不得出现独立图片资产或 HTML 文件；"可视化" 默认指 `evidence_table.md`/`coverage.md`/`g1-evaluation.md` 等数据表视图。只有外部预检已执行、核心能力均有可观察证据、验收任务与目标对齐、确认完成、跨文件互引可解析时，才允许 `g1-evaluation.md.verdict=pass`、`route_to=S2`。
