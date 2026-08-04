# S1 阶段契约 — 项目级目标校准（G1）

> 现行交付：项目级 LLM Wiki。共享规则以 `.agents/project-workspace-contract.md`、`.agents/stage-delivery-manifest.json` 和 `.agents/AGENTS.md` 为准。

## 0. 编号与责任

- `S1`：目标校准阶段。
- `G1`：判断当前目标契约能否被 S2 消费的质量门。
- S1 无上游 Gate，但必须位于一个项目工作区中。
- S1 不制定课程路径、不执行教学、不宣布学习者掌握。

## 1. 交付边界

主要交付是：

```text
workspace/<project-slug>/
  conversations/...
  stages/s1-goal-contract/...
  project-state.json
  INDEX.md
  timeline.md
```

不再以 `runs/<run-id>/` 或单体 JSON envelope 为新写入目标。旧 run 只能通过 `scripts/migrate_legacy_run.py` 迁移。

## 2. 输入

必需：

- 至少一个学习诉求、目标问题或真实使用场景；
- 当前项目或可创建项目的稳定技术标识；
- 当前 `project-state.json.project_revision`；
- 当前 conversation。

可选：

- 用户已有材料；
- 学习者或监护人约束；
- 时间、设备、环境、隐私和资源限制。

缺失项保持未知，不得补造确认。

## 3. 强制外部预检

冷启动、目标实质变化或证据过期时必须联网。至少覆盖术语、权威来源、实践/失败、职业任务、公开评估和反方/边界。

证据分类：

```text
external_evidence
market_signal
model_hypothesis
user_provided_unverified
learner_behavior
```

模型知识只能生成检索问题；无真实预检时 G1 不得通过。

## 4. 目标编译

目标契约必须包含：

- 可观察目标问题和场景；
- `CAP-*` 能力及可观察证据；
- 至少一个未见、迁移或真实综合验收；
- 可判定通过规则；
- 范围、排除项和约束；
- 高风险假设；
- S2 优先研究问题与六源检索种子。

章节、时长、题量、观看数量或一次识别题不能直接作为能力。

## 5. 强制确认

S1 默认 `mandatory`。确认对象：

- 目标能力；
- 成功证据和验收；
- 范围和排除项；
- 目标深度/岗位/学段；
- 地区、语言和时效；
- 时间、资源、环境和隐私；
- 高风险假设。

确认原文进入 conversation，结构化确认进入 `confirmation.md` 和 `user_confirmation` 事件。

## 6. 项目版本

每次 S1 实质交互：

1. 读取 `expected_project_revision`；
2. 写 conversation 和不可变事件；
3. 更新阶段 Wiki；
4. 执行 G1/verification；
5. 项目 revision 加一；
6. 同步根索引和时间线。

版本不一致时记录 `version_conflict` 并停止覆盖。

## 7. G1

G1 通过要求：

- 目标、场景、能力和验收可观察且一致；
- 来源类别覆盖满足当前风险；
- 至少一条 accepted external evidence；
- 边界、约束和排除项完整；
- mandatory 确认完成；
- conversation、事件、当前页和稳定 ID 可追溯；
- verification 通过；
- 项目状态事务成功。

通过后：

```text
G1=pass
S1.state=completed
current_stage=S2
route_to=S2
```

失败则按根因保持 S1：

```text
pending
research_blocked
revise_here
blocked
version_conflict
```

## 8. 历史与变更

- 当前 Wiki 页可更新，但旧版本必须进入 `history/`；
- 新页面写 `supersedes`、conversation 和 event；
- 目标实质变化创建新 `GOAL-*` 版本；
- 被用户否决的内容不得继续作为当前目标或为了展示反例而重复灌入当前页。

## 9. 阶段文件

逐文件合同见 [project-stage-contract.md](project-stage-contract.md)。  
旧 [run-folder-contract.md](run-folder-contract.md) 只用于迁移历史 run。

## 10. Fail closed

以下任一情况不得 route S2：

- 没有项目根；
- 没有本次 conversation；
- 只输出 JSON 或聊天文本；
- 无真实预检；
- 确认未完成；
- 项目 revision 冲突；
- 稳定 ID、事件或页面追溯断裂；
- 根索引、阶段索引和 project-state 不一致；
- 存在占位符、空表或未解决 high 风险。
