# `.agents` 运行规则：项目级 LLM Wiki

本文件适用于 `.agents/` 下的所有 Skill、质量检查和共享合同。它补充并在冲突处覆盖仓库根 `AGENTS.md`。

## 1. 统一工作区优先

执行任何 S1–S7 Skill 前，必须先读取：

1. `.agents/project-workspace-contract.md`
2. `.agents/stage-delivery-manifest.json`
3. 当前项目 `workspace/<project-slug>/INDEX.md`
4. 当前项目 `project-state.json`
5. 当前 conversation 与目标阶段的 `INDEX.md`

若项目尚不存在，只有 S1 可以创建项目根。S2–S7 缺项目上下文时必须返回 S1 或要求定位现有项目，不得临时生成孤立工件。

## 2. 覆盖旧三工件规则

现有 S3–S7 `SKILL.md` 中“Markdown → 单体 JSON envelope → HTML”为主要交付的规则进入兼容期，按以下方式解释：

- Markdown 内容迁入项目 Wiki 的阶段页面；
- JSON Schema 继续约束机器快照、JSONL 原子记录或兼容导出；
- HTML 是可选派生视图，不再是每次阶段交互的强制写入；
- 只生成单体 JSON 而未更新项目 Wiki、conversation 和项目状态，视为交付不完整；
- 旧 envelope 可作为导出，但不能取代阶段目录与项目索引。

## 3. 每次交互必须留痕

每次产生以下任一结果时，都必须创建或更新项目 conversation：

- 用户补充目标、约束、材料或确认；
- Agent 执行研究、诊断、规划、教学、测评或重规划；
- 使用工具得到影响结论的结果；
- Gate、路由或项目状态发生变化；
- 学习者产生可用于诊断或掌握判断的行为。

conversation 至少包含 `transcript.md`、`events.jsonl` 和 `summary.md`。不能只把最终 JSON 保存为“交互记录”。

## 4. 当前页、事件与快照

- 当前 Wiki 页面可以更新，但必须通过事件和 `supersedes` 追溯旧版本。
- `events.jsonl`、阶段原子日志和学习者模型事件只追加。
- `project-state.json` 是可覆盖的派生快照，更新时必须检查 `expected_project_revision`。
- 自由文本工作笔记不能自动升级为已确认事实。

## 5. 阶段完成条件

一个阶段完成至少要求：

```text
项目根存在
+ 当前 conversation 已记录
+ 阶段必需 Wiki/JSONL 文件齐全
+ 稳定 ID 和跨文件引用可解析
+ 阶段 Gate 通过
+ verification 通过
+ project-state.json 已更新
+ 根 INDEX.md/timeline.md 已同步
```

旧文件存在、单体 JSON Schema 通过、自然语言声称“完成”均不能单独证明阶段完成。

## 6. 兼容迁移

读取旧 `runs/<run-id>/` 时保持只读。需要继续学习流程时先按项目工作区合同完成迁移，再在新结构写入后续交互。不得一半写旧 run、一半写新项目阶段目录而不留下迁移事件和明确主入口。

## 7. 质量检查

独立质量检查必须同时检查：

- 阶段业务量规；
- 项目工作区结构；
- conversation 留痕；
- 当前页与事件追溯；
- 项目 revision 与阶段版本；
- 根索引、阶段索引和机器快照一致性。

质量检查只读、只判，不得替阶段 Skill 修改项目 Wiki。
