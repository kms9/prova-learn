# 主控路由与下一步合同

> 适用对象：`al-orchestrate-personalized-learning`。本页只定义控制面；阶段业务以 manifest、profile 和目标 Skill 为准。

## 1. 阶段 Skill 映射

每次调用都从 `.agents/stage-delivery-manifest.json` 重新核对以下映射：

| 阶段 | Skill | 事实所有权 |
|---|---|---|
| S1 | `al-s1-create-goal-success-contract` | 学习目标、场景、成功证据、范围、约束、目标实质变化 |
| S2 | `al-s2-create-domain-evidence-landscape` | 领域研究、六源取证、逐题回答、来源冲突与刷新 |
| S3 | `al-s3-build-capability-concept-graph` | 能力层级、学习单元、原子节点、先修、测评和追溯 |
| S4 | `al-s4-diagnose-learner-frontier` | 学习者真实行为、误概念、提示依赖、迁移与学习前沿 |
| S5 | `al-s5-plan-learning-sessions` | 学习路径、策略政策、会话、日程、复习和计划确认 |
| S6 | `al-s6-run-instructional-interaction` | 教学材料、真实互动、提示反馈、行为事件和候选证据 |
| S7 | `al-s7-verify-mastery-and-replan` | 多维掌握验证、模型更新、归因、复测和重规划 |

主控不是 S0，不拥有业务 Gate，也不产生独立学习阶段目录。

## 2. 意图选择优先级

按第一条已确定规则选择；不要把关键词票数当路由算法。

| 优先级 | 条件 | 选择 |
|---|---|---|
| 1 | 新学习项目；目标结果、真实场景、成功证据、领域边界发生实质变化 | S1 |
| 2 | 用户明确说 S1–S7 或点名某个阶段 Skill | 对应阶段 |
| 3 | 用户说继续、下一步、接着做、按当前状态推进 | 已验证 `project-state.route_to` |
| 4 | 纯查询进度、缺口、为什么被阻断、现在该做什么 | read_only |
| 5 | 用户请求阶段业务但未点名阶段 | 按事实所有者映射 |

只有措辞润色、展示方式或非实质约束补充不自动构成目标实质变化。若补充内容会改变目标能力、验收、范围或版本，则由 S1 处理。

## 3. 常见自然语言映射

| 用户意图示例 | 首选阶段 | 判定说明 |
|---|---|---|
| “我想学会……”“帮我定义学到什么程度” | S1 | 先校准目标和成功证据 |
| “这个领域要研究什么”“找权威资料回答这些问题” | S2 | 领域证据事实 |
| “拆知识点”“构建能力图/先修关系/测评节点” | S3 | 稳定结构建模 |
| “我应该从哪里开始”“测测我的水平/误区” | S4 | 基于真实行为定位前沿 |
| “给我排学习路径/课程/策略/复习计划” | S5 | 学习者条件下的计划 |
| “开始教我”“出练习并根据回答反馈” | S6 | 真实教学交互 |
| “我掌握了吗”“复测/更新模型/重新规划” | S7 | 多维验证与归因 |

同一请求包含“研究后拆图”时，选择 S2；只有 G2 通过后才可 S3。同一请求包含“诊断后规划”时，选择 S4；只有 G4 通过后才可 S5。用户明确要求完整流程时可进入 `guided_flow`，但仍逐门核验。

## 4. 项目与前置决策

| 项目状态 | single_stage | guided_flow |
|---|---|---|
| 缺项目，目标为 S1 | 执行 S1 | 从 S1 开始 |
| 缺项目，目标为 S2–S7 | 执行目标阶段的 `project_missing → S1` 独立语义 | 从 S1 开始 |
| 旧 run | 迁移后重读，再执行一次目标阶段 | 迁移后从最早未完成阶段推进 |
| 项目存在但前置缺失/失效 | 由目标阶段写 blocked 事务并 route 最早前置 | 从最早缺失/失效阶段开始 |
| revision 冲突 | 停止、重读、报告冲突 | 停止，不自动重试覆盖 |
| 前置通过 | 执行目标阶段一次 | 执行并逐阶段复核 |

项目选择优先级：用户显式项目路径 > 当前目录唯一有效项目 > 唯一旧 run > missing。多个候选项目的写入请求必须澄清。

## 5. 允许继续与强制停顿

只有同时满足下列条件才允许 `guided_flow` 继续：

- 本阶段状态为 `completed`；
- 本阶段业务 Gate 与 verification 均通过；
- 项目 revision、根/阶段索引、timeline 和 conversation 一致；
- `route_to` 是 manifest 允许的下游阶段；
- 下一阶段所需的真实输入已存在；
- 没有待确认、高风险选择或来源阻断。

下列状态一律停顿并转成具体用户动作：

| 状态 | 必须告诉用户 |
|---|---|
| S1 pending | 目标能力、验收、范围、约束中待确认的原问题 |
| S1/S2 research_blocked | 哪个真实来源/联网动作未执行及恢复条件 |
| S2 blocked/partial | 未回答的 RQ、缺失证据通道或冲突 |
| S3 revise_here | 断裂追溯、孤儿节点、环或缺评估的修复范围 |
| S4 pending | 要学习者实际完成的诊断题或迁移任务 |
| S5 pending | 需确认的路径、节奏、策略或会话合同 |
| S6 pending | 当前教学活动和要学习者亲自提交的回答 |
| S7 pending | 需要补测、迁移或延迟保持的任务与时间条件 |
| S7 return_upstream | 主归因、最早污染阶段和被失效的下游范围 |
| version_conflict | 预期/实际 revision 与重新加载要求 |
| complete | GOAL_ACHIEVED、最终验收和保持证据入口 |

## 6. 委托后最小核验

不要仅搜索字符串。至少交叉读取：

1. `project-state.json` 的 `project_revision`、`status`、`current_stage`、`route_to`、`last_conversation_id` 和 `stage_status`；
2. 项目根 `INDEX.md` 与 `timeline.md`；
3. 本阶段 `INDEX.md`、`gate.md`、`verification.md`；
4. 本次 conversation 的 `INDEX.md`、`transcript.md`、`events.jsonl` 和 `summary.md`；
5. manifest 的必需文件与前置定义。

满足以下证据等级再选择表述：

| 证据 | 可报告表述 |
|---|---|
| 阶段事务与 Gate/verification 全部可核验 | “阶段已完成，route_to=…” |
| 前置通过但等待真实输入 | “阶段 pending，等待…” |
| 前置失败且业务未执行 | “阶段 blocked，恢复路由为…” |
| 只有子 Skill 自述或部分文件 | “未能核验完成；缺少…” |
| 没有发生目标阶段事务 | “已选择但未执行” |

## 7. 下一步提示格式

下一步必须是用户可直接完成的一条动作，优先使用下面的形式：

```text
请直接回答：<具体问题或活动>。我会继续通过 $al-orchestrate-personalized-learning 处理。
```

或：

```text
请确认：<列出有实质影响的选项/合同摘要>。确认后继续由 $al-orchestrate-personalized-learning 推进。
```

或：

```text
下一步将由 $al-orchestrate-personalized-learning 路由到 Sx，目标是 <具体产物/决策>。
```

不要把“请调用 `$al-sN-...`”作为面向用户的默认下一步。子 Skill 名可以作为本次执行证据展示，但用户入口保持主控。
