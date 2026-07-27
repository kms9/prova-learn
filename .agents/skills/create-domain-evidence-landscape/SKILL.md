---
name: create-domain-evidence-landscape
description: 对已通过 G1 的学习目标执行真实联网、STORM 式多视角、多轮取证，形成可追溯的 domain_evidence_landscape，区分共识、分歧、市场信号、推断和证据缺口。只要用户需要进入个性化学习 S2、研究某领域全景、从岗位或评估样本提炼能力，或补充 S3 建图暴露的来源空白，就使用本 skill。
---

# 领域取证与认知全景（S2）

负责“依据是什么”，不负责画能力图，也不把搜索结果数量或模型记忆当成证据质量。

## 开始前

1. 读取 [stage-contract.md](references/stage-contract.md)。
2. 读取 [handoff-envelope.schema.json](references/handoff-envelope.schema.json) 和 [domain-evidence-landscape.schema.json](references/domain-evidence-landscape.schema.json)。
3. 仅为理解输出形状时读取 [example.md](references/example.md)；案例数据是设计夹具，不是真实观察。
4. 校验上游 `goal_success_contract` 已通过 G1，范围、可观察成功证据、确认和 `external_research_seed` 可用。

## 执行

1. 基于 S1 目标框定主题、地区、语言、岗位/应用场景、时间边界与研究深度。
2. 至少建立六类视角：术语/历史、理论/标准、实践/真实任务、招聘/市场能力、面试/评估证据、批评/争议/前沿。
3. 为每个视角提出核心问题、反例问题与后续追问；执行多轮联网查询，冲突或新发现必须触发后续检索，**不允许只做一次搜索**。
4. 建立来源台账与强制类别覆盖表；为六类来源记 `covered / not_applicable / gap`、理由、关键性与门禁影响。`not_applicable` 必须写明理由；找不到资料记为 `gap`。
5. 分开标记 `external_evidence`、`market_signal`、`model_hypothesis`、`user_provided_unverified`；模型知识只能作假设与查询生成器，不能当外部来源。
6. 适用时招聘研究至少覆盖 3 个当前岗位样本、2 个组织；面试/选拔至少 2 组独立样本；未达标记 `undersample gap`，不补造样本。把任务、能力、技能、工具、背景筛选分开编码。
7. 建立 claim→evidence 映射，区分 `supported / partially_supported / unsupported`，保留强反方论据、适用边界与时效；把市场信号与规范事实并列而非合并。
8. 生成 `domain_evidence_landscape`，再按 G2 量规逐项评价。

## Fail closed

- 无真实查询清单、只有模型常识或少量未审计页面时，G2 失败。
- 无联网/检索能力时输出 `research_blocked`，`status=blocked`；用户确认不能豁免外部证据门。
- 资料不存在时记为 `gap`；只有确实不适用并写明理由时才能用 `not_applicable`。
- 招聘条件不是科学事实，面试题不是能力本体，百科只作为全景入口。
- S3 建图发现来源空白时回到 S2 局部补证，不重做无关部分；目标本身改变时返回 S1。

## 输出

只输出符合两个 Schema 的 JSON 移交信封。只有联网多视角研究已实际执行并记录、强制来源类别覆盖完整、关键结论可追溯、争议未被单边伪装成共识、市场信号与事实分开、证据缺口透明且 G2 通过时，才允许 `verdict=pass`、`route_to=S3`。
