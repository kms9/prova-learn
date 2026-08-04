# Prova Learn 项目级 LLM Wiki 工作区合同

> 合同版本：1.0.0  
> 适用范围：S1–S7 全阶段、独立质量检查、运行时工作区与评测工具。

## 1. 核心决定

一个学习目标对应一个长期存在的项目工作区：

```text
workspace/<project-slug>/
```

项目工作区是 S1–S7 的共同上下文、事实入口和历史容器。阶段不得再各自产生彼此孤立的单体 JSON 作为主要真相源。

统一采用三层真相：

1. **Wiki 页面（Markdown）**：表达当前被接受的目标、知识、计划、诊断、教学与掌握结论，供人和 LLM 阅读。
2. **事件日志（JSONL）**：追加记录真实发生的会话、证据、确认、决策、模型更新和路由，禁止静默改写历史。
3. **机器快照（小型 JSON）**：保存当前指针、版本和可计算状态；它由 Wiki 与事件派生，不是完整业务叙事。

大型单体 JSON envelope 退化为兼容导出，不再作为 S3–S7 的主要交付。

## 2. 项目目录

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
│   ├── evidence/
│   ├── concepts/
│   ├── misconceptions/
│   └── methods/
├── learner/
├── plans/
├── sessions/
├── assessments/
├── decisions/
├── attachments/
└── _machine/
```

### 根文件职责

- `INDEX.md`：项目主入口。结论先行，展示当前目标、当前阶段、最近会话、Gate 状态、下一动作和关键链接。
- `PROJECT.md`：项目身份、目标边界、参与者、约束、隐私与归档策略。
- `project-state.json`：当前项目版本、阶段、路由、活动目标版本、学习者模型版本和最近会话指针。
- `timeline.md`：阶段变化、关键确认、Gate、重规划和目标版本变更的时间线。

## 3. 会话记录

每次用户与 Agent 的实质交互必须进入：

```text
conversations/YYYY-MM/<conversation-id>/
  INDEX.md
  transcript.md
  events.jsonl
  summary.md
```

- `transcript.md`：按发生顺序追加记录用户输入、Agent 回应、工具动作与结果摘要。不得在后续会话中重写旧内容。
- `events.jsonl`：每行一个符合 `project-event.schema.json` 的不可变事件。
- `summary.md`：本次会话形成的结论、未决问题、更新的页面和下一动作。
- `INDEX.md`：会话元数据及指向以上文件和受影响阶段页面的链接。

对话原文与结构化事件必须区分：原文回答“发生了什么”，事件回答“哪些事实或状态因此改变”。

## 4. 稳定 ID

项目内统一使用稳定 ID：

| 对象 | 前缀 |
|---|---|
| 项目 | `PRJ-` |
| 会话 | `CONV-` |
| 目标版本 | `GOAL-` |
| 来源 | `SRC-` |
| 证据项 | `EVID-` |
| 能力 | `CAP-` |
| 学习单元 | `UNIT-` |
| 知识节点 | `NODE-` |
| 观察 | `OBS-` |
| 计划 | `PLAN-` |
| 学习会话 | `SESSION-` |
| 测评 | `ASSESS-` |
| 决策 | `DEC-` |
| Gate 评价 | `GATE-` |
| 模型事件 | `MODEL-` |

ID 创建后不得复用。对象内容发生实质变化时创建新版本或新事件，不覆盖历史含义。

## 5. 阶段目录共同合同

每个 `stages/sN-*/` 至少包含：

```text
INDEX.md
working-notes.md
records.jsonl
decisions.md
gate.md
verification.md
history/
```

- `INDEX.md`：本阶段当前有效结论、输入版本、输出页面、Gate 和路由。
- `working-notes.md`：分析过程、候选方案和未接受假设；不得被下游当作已确认事实。
- `records.jsonl`：本阶段的原子记录或状态变更。
- `decisions.md`：关键选择、被排除方案、理由、证据与确认。
- `gate.md`：逐维 Gate 评价。
- `verification.md`：文件、引用、版本、占位符和项目索引同步检查。
- `history/`：被新版本替代的阶段页面或阶段尝试。

具体阶段文件由 `.agents/stage-delivery-manifest.json` 定义。

## 6. 七阶段在项目 Wiki 中的职责

### S1 目标校准

创建项目根、项目状态和 `stages/s1-goal-contract/`。目标、成功证据、范围与研究简报进入 Wiki；预检来源、能力和术语进入 JSONL。

### S2 领域取证

在 `stages/s2-domain-evidence/` 维护研究日志、来源、原子证据、逐题回答、争议和刷新策略。S2 不另建项目或独立 run。

### S3 能力概念图

以 `capability-map.md`、`learning-units.md`、`nodes.jsonl`、`edges.jsonl`、`assessments.jsonl` 与 `traceability.md` 组织图谱。单体 `capability_concept_graph.json` 仅可作为派生导出。

### S4 学习者诊断

原始行为进入 `observations.jsonl`，当前解释进入 `learner-snapshot.md`，模型变化进入 `model-events.jsonl`。学习者自述不得覆盖行为历史。

### S5 路径与会话规划

路径、策略政策、会话安排、复习节奏和确认进入独立 Wiki 页面；可执行日程进入 JSONL。计划版本变化保留历史。

### S6 教学交互

每次真实教学会话写入 `sessions/<session-id>/`，同时关联一个项目 conversation。教学内容、交互原文、提示、反馈、行为事件和候选证据分开记录。

### S7 掌握验证与重规划

掌握证据、模型更新、复测安排、策略归因和路由进入阶段页面与事件日志。版本冲突或无持久化后端必须如实记录。

## 7. 写入事务

每次实质交互按以下顺序执行：

```text
读取 project-state.json 与 INDEX.md
→ 校验 expected_project_revision
→ 追加 transcript.md
→ 追加 events.jsonl
→ 更新受影响阶段 Wiki/records
→ 运行阶段 Gate 与 verification
→ 更新 project-state.json（revision +1）
→ 更新项目 INDEX.md 与 timeline.md
```

若项目版本已变化，停止覆盖并报告 `version_conflict`。不得通过最后写入者获胜静默覆盖其他会话。

## 8. 当前页面与历史

- Wiki 页面表达“当前被接受版本”，必须链接到产生该版本的事件和会话。
- JSONL 表达“不可变历史”，只追加，不原地修订。
- 被替代页面移入阶段 `history/`，并在新页面写 `supersedes`。
- 目标实质变化时创建新的 `GOAL-*` 版本；同一项目可继续，也可由用户决定新建项目。

## 9. JSON 的保留边界

JSON/JSONL 继续用于：

- 机器状态与版本；
- 原子记录、事件和边；
- Schema 校验；
- 可选 API 导出；
- HTML 或图形视图的数据源。

JSON 不再承担：

- 完整教学叙事；
- 长篇研究回答；
- 会话上下文；
- 人审决策说明；
- 整个阶段唯一真相。

## 10. 旧 run 兼容

现有 `workspace/<project-slug>/runs/<run-id>/` 是迁移输入，不再作为新项目的推荐写入位置。

迁移时：

1. 创建项目根文件和 `project-state.json`；
2. 把旧 run 根内容映射到 `stages/s1-goal-contract/`；
3. 把旧 `s2/` 映射到 `stages/s2-domain-evidence/`；
4. 为迁移动作创建 conversation 和 `artifact_migrated` 事件；
5. 保留旧 run 只读，不删除历史；
6. 更新项目根 `INDEX.md` 指向新位置。

## 11. Fail closed

以下任一情况不得报告项目或阶段完整完成：

- 缺项目根入口或项目状态；
- 实质交互没有 conversation 记录；
- Wiki 结论无法追溯到事件、证据或确认；
- JSONL 非法或稳定 ID 无法解析；
- 项目 revision 冲突；
- Gate 未通过却把阶段状态改为 completed；
- 只生成单体 JSON 而没有更新项目 Wiki；
- 静默覆盖旧页面或历史事件。
