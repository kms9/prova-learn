# 项目级 LLM Wiki 工作区与七阶段交互迁移设计

> 日期：2026-08-04  
> 状态：基础合同已实施，七阶段 Skill 正在按 S1→S7 顺序迁移  
> 目标：把“阶段单体 JSON 交付”迁移为“长期项目 Wiki + 不可变会话事件 + 机器状态快照”。

## 1. 当前问题

旧实现把阶段理解为一次模型调用：

```text
输入上游 JSON
→ 生成本阶段 Markdown/JSON/HTML
→ 用 JSON 交给下一阶段
```

这种方式适合验证单次工件，不适合长期学习项目：

- 会话原文、用户确认和工具结果没有稳定归档位置；
- 同一目标经过多次讨论后，难以知道哪个版本当前有效；
- 学习者诊断、计划、教学和掌握证据被切成彼此孤立的 JSON；
- 返工会生成新工件，但缺少统一项目时间线和 supersedes 关系；
- JSON 能表示字段，却不适合承载研究叙事、教学上下文和决策理由；
- 每次都生成完整 Markdown、JSON、HTML，成本高且容易语义漂移。

## 2. 新的系统边界

一个学习目标对应一个长期项目：

```text
workspace/<project-slug>/
```

七个阶段是在同一个项目中的七类职责，不是七个独立项目或七个孤立文件包。

统一三层真相：

| 层 | 载体 | 回答的问题 |
|---|---|---|
| 当前认知 | Markdown Wiki | 现在接受什么目标、知识、诊断、计划和结论 |
| 不可变历史 | JSONL 事件 | 发生过什么交互、证据、确认、决策和状态变化 |
| 机器状态 | 小型 JSON | 当前版本、阶段、路由和活动指针是什么 |

单体 JSON envelope 保留为兼容导出，而不是项目主真相。

## 3. 项目级目录

```text
workspace/<project-slug>/
├── INDEX.md
├── PROJECT.md
├── project-state.json
├── timeline.md
├── conversations/
├── stages/
│   ├── s1-goal-contract/
│   ├── s2-domain-evidence/
│   ├── s3-capability-graph/
│   ├── s4-learner-diagnosis/
│   ├── s5-learning-plan/
│   ├── s6-instruction/
│   └── s7-mastery-replan/
├── knowledge/
├── learner/
├── plans/
├── sessions/
├── assessments/
├── decisions/
├── attachments/
└── _machine/
```

根 `INDEX.md` 是所有 Agent 和人的第一入口，只展示当前状态和必要链接，不把全部项目内容塞入一个页面。

## 4. 每次对话如何记录

每次实质交互建立：

```text
conversations/YYYY-MM/<conversation-id>/
  INDEX.md
  transcript.md
  events.jsonl
  summary.md
```

### `transcript.md`

按顺序记录用户输入、Agent 回答、工具动作和工具结果摘要。原始学习者回答不得改写成更正确或更流畅的版本。

### `events.jsonl`

记录结构化事件，例如：

- `conversation_turn`
- `user_confirmation`
- `source_added`
- `learner_observation`
- `strategy_selected`
- `instruction_event`
- `mastery_evidence_added`
- `learner_model_updated`
- `gate_evaluated`
- `route_decided`

事件只追加，不能覆盖。

### `summary.md`

记录本次会话产生了什么结论、更新了哪些 Wiki 页面、留下什么缺口以及下一动作。

## 5. 阶段共同文件

每个阶段目录至少包含：

```text
INDEX.md
working-notes.md
records.jsonl
decisions.md
gate.md
verification.md
history/
```

`working-notes.md` 是候选分析，不是下游可直接消费的事实。当前有效结论必须进入阶段专属 Wiki 页面，并链接到来源事件。

## 6. 七阶段交互与输出

| 阶段 | 主要交互 | 当前 Wiki 输出 | JSONL / 机器记录 |
|---|---|---|---|
| S1 | 澄清目标、场景、范围、成功证据并确认 | `goal-contract.md`、`research-brief.md`、`confirmation.md` | 来源、能力、术语、确认事件 |
| S2 | 多轮研究、冲突追问、证据缺口确认 | `research-answers.md`、`answer-validation.md`、`refresh-policy.md` | 来源、证据项、查询与工具事件 |
| S3 | 展示能力结构、粒度和关键先修，处理建模分歧 | `capability-map.md`、`learning-units.md`、`traceability.md` | 节点、边、评估项 |
| S4 | 执行诊断任务、记录真实回答、处理争议节点 | `diagnostic-plan.md`、`learner-snapshot.md`、`misconceptions.md` | 观察、提示、模型事件 |
| S5 | 展示路径取舍、策略、时间和首个会话并强制确认 | `learning-path.md`、`strategy-policy.md`、`sessions.md` | 日程、策略决策、确认事件 |
| S6 | 真实教学、提问、提示、反馈、撤架和学习者输出 | 每个 `sessions/<session-id>/` 的材料、交互和反思 | 教学事件、行为证据、候选掌握证据 |
| S7 | 复测、掌握判断、版本更新、归因和重规划 | `mastery-evidence.md`、`strategy-attribution.md`、`replan.md`、`route.md` | 掌握事件、模型更新、路由事件 |

## 7. 项目写入事务

```text
读取 project-state.json
→ 校验 expected_project_revision
→ 追加 conversation 原文与事件
→ 更新阶段记录和当前 Wiki
→ 执行 Gate 与 verification
→ project_revision + 1
→ 更新项目 INDEX.md 与 timeline.md
```

如果 revision 已变化，保留本次 conversation 和冲突事件，但停止覆盖当前页面。

## 8. 当前页和历史页

- 当前 Wiki 页面表达项目目前接受的版本。
- 旧版本进入阶段 `history/`。
- 新页面声明 `supersedes`，并链接导致变化的 conversation/event。
- 目标、图谱、学习者模型和计划分别拥有自己的版本，不共用一个模糊的“最新 JSON”。

## 9. HTML 的新位置

HTML 不再是每次阶段运行的强制工件。它只在以下情况按需生成：

- 需要人审图谱或路径；
- 需要汇报；
- 需要浏览大量事件或模型差异；
- 需要导出离线报告。

HTML 只能从项目 Wiki 和机器记录派生，不得另造业务事实。

## 10. 迁移顺序

### Phase 0：统一基座

- 项目工作区合同；
- 阶段交付 manifest 2.0；
- project-state 与 project-event Schema；
- 项目初始化器；
- 项目与旧 run 的确定性验证；
- `.agents/AGENTS.md` 和 `workspace/AGENTS.md` 覆盖规则。

### Phase 1：S1、S2

- S1 从旧 run 根迁入项目 `stages/s1-*`；
- S2 从嵌套 `s2/` 迁入项目 `stages/s2-*`；
- 对话和研究过程进入 conversation；
- 提供旧 run 迁移器。

### Phase 2：S3、S4

- 图谱拆成 Wiki + nodes/edges/assessments JSONL；
- 诊断拆成原始观察、当前快照和模型事件；
- 更新 G3/G4 Checker 和 eval。

### Phase 3：S5、S6

- S5 实现结构化策略政策；
- S6 以真实 `sessions/<session-id>/` 运行；
- 明确方法执行忠实度、提示和适配事件。

### Phase 4：S7

- 掌握验证、模型事务、策略归因和重规划写入项目事件链；
- 延迟复测可跨 conversation 持续更新；
- 只有项目级目标验收通过才 `complete`。

## 11. 当前实施状态

已完成：

- 项目工作区共享合同；
- manifest 2.0；
- project-state / project-event Schema；
- 项目初始化脚本；
- 确定性验证器和 CI 入口；
- `.agents`、`workspace`、quality-checks 三层运行规则；
- S1、S2 Checker 改为读取项目 Wiki。

待完成：

- S1–S7 各自 `SKILL.md` 和阶段 reference 的逐个迁移；
- 旧 run 自动迁移脚本；
- eval runner 从单 JSON 评分迁移为工作区 diff 与事件评分；
- S3–S7 Checker 的阶段专属输入路径迁移；
- 第一个完整项目级 S1→S7 贯穿样例。
