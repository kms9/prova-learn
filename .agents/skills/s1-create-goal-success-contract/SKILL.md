---
name: al-s1-create-goal-success-contract
description: 在项目级 LLM Wiki 中创建或更新 S1 目标校准，把模糊诉求、真实场景、外部预检、可观察能力、最终验收和用户强制确认写成可追溯目标契约。新目标、目标实质变化、成功证据变化或领域边界修正时使用。
metadata:
  author: kms9
---

# S1 目标与成功契约

S1 把“想学什么”转成一个可观察、可验收、受现实证据约束并由用户明确确认的目标。项目 Wiki 是交付边界；聊天结论、旧 run 或单个 JSON 不能替代项目事实。

## 1. 读取顺序

1. `../../project-workspace-contract.md`
2. `../../standalone-invocation-contract.md`
3. `../../stage-runtime-contract.md`
4. `../../stage-delivery-manifest.json`
5. `../../stage-profiles.json#S1`
6. `references/project-stage-contract.md`
7. 当前项目根、最近 conversation 和 S1 入口

旧 `runs/<run-id>` 只能作为迁移输入，不能继续写入。

## 2. 项目与事务

- 无项目时，S1 可创建 `workspace/<project-slug>/`；slug 只是技术标识，不代表领域结论已确认。
- 已有项目时保存 `expected_project_revision`，目标实质变化创建新 `GOAL-*` 版本并记录 `supersedes`。
- 每次补充、纠正或确认都创建 conversation，原样保留用户输入，追加事件，再更新 S1、Gate、verification、根索引和 timeline。
- revision 冲突时停止提交，不允许最后写入者覆盖。

## 3. 输入与事实分层

至少区分：

- 用户明确事实；
- 用户材料但尚未验证的内容；
- 模型假设；
- 市场信号；
- 已访问的外部证据。

需要形成：目标问题、真实使用场景、学习深度、受众、地区/行业/语言/时效、可用时间与资源、隐私边界、范围、排除项、最终验收。

缺失信息保持 `unknown` 或 `pending`，不得静默补成已确认事实。

## 4. 外部预检

冷启动、目标实质变化或关键事实过期时必须真实联网。至少覆盖：

1. 术语及相邻概念；
2. 官方、标准、教材或学术来源；
3. 真实实践和失败边界；
4. 当前职业任务或场景样本（适用时）；
5. 公开评估、实操或认证样本（适用时）；
6. 反方、争议或不适用条件。

来源必须记录访问时间、来源角色、独立来源组、权威性、地区和限制。用户材料统一先标 `user_provided_unverified`；模型常识不能补成外证。

## 5. 目标编译

从场景和证据反推：

- `CAP-###` 可观察能力；
- 每项能力的真实行为或产物；
- 认知层级与证据类型；
- 至少一个未见综合任务；
- 近迁移或远迁移要求；
- 适用时的延迟保持要求；
- 可判定通过规则；
- 范围、排除项、约束与隐私；
- S2 的优先研究问题。

观看时长、章节完成、题量、一次选择题或“感觉懂了”不能直接作为成功标准。

## 6. 强制确认

S1 的确认模式为 `mandatory`。必须向用户展示将被确认的具体字段，并将结果结构化记录为：

```json
{
  "status": "pending|confirmed",
  "confirmed_fields": [],
  "unconfirmed_fields": [],
  "learner_utterance": "原始用户回复",
  "interpretation_basis": "explicit|explicit_accept_all_defaults|ambiguous"
}
```

不得把普通“继续”“下一步”“跑完流程”自动解释为接受多个默认项。

只有上一轮明确提供了一个“接受全部默认值”的选项、逐项列出字段且本轮回复直接指向该选项时，才允许 `explicit_accept_all_defaults`。即便如此，用户回执仍要重新列出实际确认字段。

确认至少覆盖：

- 目标能力和深度；
- 使用场景；
- 最终验收和通过规则；
- 范围与排除项；
- 时间、资源、语言和环境；
- 高风险假设及隐私边界。

已有明确答案不得重复询问；只询问会改变目标或验收的最少问题。

## 7. G1

G1 至少检查：

1. 目标可观察；
2. 成功标准可判定；
3. 场景真实且边界清楚；
4. 外部现实校准；
5. 来源覆盖和独立性；
6. 目标—能力—验收一致；
7. 未见任务、迁移和保持要求适配目标；
8. 范围、约束和隐私完整；
9. `confirmed_fields` 完整且无关键 `unconfirmed_fields`；
10. conversation、revision、ID、索引和 verification 一致。

只有全部通过，才允许：

```text
S1.state=completed
G1=pass
route_to=S2
```

## 8. Fail closed

- 无联网预检：`research_blocked → S1`。
- 关键确认未完成或含糊：`pending → S1`。
- 模型假设、市场信号或裸材料冒充事实：G1 失败。
- 目标只剩课程目录、章节或题量：G1 失败。
- 旧 run 未迁移、引用断裂、占位符、revision 冲突：不得通过。
- 不得模拟用户确认或学习者能力。

## 9. 用户回执

说明项目与 revision、本次 conversation、目标变化、实际 `confirmed_fields`、仍未确认字段、G1 和 route，以及一条具体下一步。不要把完整 JSON 信封粘贴到聊天中。
