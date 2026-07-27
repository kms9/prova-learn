# 本地确定性校验报告

日期：2026-07-27  
范围：`.agents/skills` 下七个阶段技能。  
说明：本报告证明结构、Schema、合同和设计夹具一致性；不把设计夹具当作真实学习效果，也不替代 dclaude 对照评测。

## 结构与 Skill Creator 校验

- 顶层阶段 skill 目录：`7`。
- 每个目录均有 `SKILL.md`、`agents/openai.yaml`、`references/stage-contract.md`、公共 handoff Schema、阶段 artifact Schema、`references/example.md`、`evals/evals.json`。
- Skill Creator `quick_validate.py`：七个目录均返回 `Skill is valid!`。
- `openai.yaml`：PyYAML 成功解析 `7/7`；`display_name`、25–64 字符 `short_description` 和含 `$skill-name` 的 `default_prompt` 均存在。
- SKILL 中所有直接 Markdown 文件链接均存在。

## JSON、YAML 与 Schema

- Draft 2020-12 `check_schema`：`14/14`（7 份公共 handoff + 7 份阶段 artifact）。
- 七份阶段 artifact Schema 根包装一致：`type/schema_version/artifact_id/content`。
- 七份公共 handoff Schema SHA-256 相同：
  `51695994c452893efac20338992ed5a42b66de8846e38780fade45469c337ff4`。
- 自动最小夹具 + 严格 FormatChecker：
  - 正向阶段 artifact：`7/7` 合法；
  - 删除根必填字段的反向 artifact：`7/7` 被拒绝；
  - `positive_artifact=null` 的 blocked handoff：`7/7` 合法；
  - `passed=false` 且 failure action/route 为空：被公共 handoff Schema 拒绝；
  - `input_validation.status=fail` 且正向工件非空：被公共 handoff Schema 拒绝；
  - S7 `expected_model_version=4`、loaded=5、`version_conflict/not_executed`：Schema 合法且语义断言通过。

## 示例与 eval 语料

- 七份 `references/example.md` 均含：来源追溯、输入事实、正向 artifact JSON、门裁决、`route_to`、`simulated_fixture`。
- 从示例 Markdown 抽取 `8` 个正向 artifact JSON（S7 有两个正向示例），全部通过对应阶段 Schema。
- 七份 `evals/evals.json` 均符合安装版 Claude Skill Creator 形状：
  `skill_name + evals[3]`，共 `21` 条。
- 每条 eval 均含整数 id、执行器 prompt、带 source/fixture 标签的 expected output、文件数组和 grader-only 字符串 expectations。
- 所有声明的 eval 输入文件均存在；没有把 expectation 文本、`expected_output` 或 `route_to` 直接注入执行器 prompt。

## 合同与语义守卫

- S1：`external_research_seed.search_executed` 为必填，合同明确无检索时 G1 失败且模型记忆不能替代预检。
- S2：`research_executed` 为必填，合同明确无真实联网时 G2 失败且模型知识只用于假设/查询。
- S6：阶段 Schema 没有掌握结论字段；合同明确 G6 只评价教学工件，不能宣布掌握。
- S4：`learner_snapshot` Schema 以 Draft 2020-12 `if/then` 强制 `tested_mastered` 只能搭配 `hint_dependency.level=none|low`；旧的 `high + tested_mastered` 夹具被拒绝，修复后 gclaude eval-2 工件通过 handoff/artifact 两层 Schema。
- S7：合同含 9 条完整归因→路由；Schema 路由枚举含 S1–S7/complete；多因采用“目标→来源→图谱→诊断→路径→内容→证据”上游优先级。
- S7 版本协议的 `load/append_evidence/update/history` 均为 required，`version_conflict` 在结构枚举中。
- S7 合同明确 Schema/G7 边界：跨数组同 `node_id` 的动态掌握规则由 G7 判定；冷启动不伪装为版本 0 正向事务，而是 null artifact 并返回 S4。
- 快速档 allow/deny、研究档 expert/delayed pending gate 与每阶段安全态见 `contract-guard-audit.md`。

## 集成审计

`integration-audits.json` 包含：

- PostgreSQL 查询优化 S1→S7 链；
- 资深学科内容校验老师 S1→S7 链；
- S7→S5→S6→S7 补救环。

jq 审计结果为 `true`，验证：

- 两条主链 stage/gate 顺序为 S1/G1 到 S7/G7；
- 每门 pass、确定性 route 顺序正确；
- 当前阶段输入引用上一阶段 artifact；
- 每阶段 source refs 和适用范围非空；
- 补救环顺序/路由为 `S7→S5→S6→S7` / `S5→S6→S7→S6`；
- expected/loaded model version 一致；
- 后续 history 保留上一事件；
- 第一轮主归因为 `STRATEGY_OR_SEQUENCE`，第二次 S7 为 `NODE_MASTERED`；
- 所有集成数据均显式标记为模拟夹具，未声称真实持久化或生产胜任。

## 未由本报告证明的门

- 当前外部证据已包含 21 条 eval 的 42 次 with-skill/without-skill 原始 dclaude 执行、42 份 canonical grading、七份 benchmark 和七个非空静态 review；这些证据的 route/model provenance、S4 gclaude 修复重跑和历史失败均分别保留。
- `dclaude-benchmarks/canonical-evidence-manifest.json` 明确 current canonical 层为 `eval-*/<configuration>/run-1`；`case-*`、两个 `historical-aggregate-grading.json`、原始失败 `grader_run_status.json` 与 legacy workspace 均保留但不参与当前聚合。七个 canonical workspace 均有非空 `grader-route.json`。
- 独立 S4/S7 canonical integrity 审计确认 12/12 expectation、passed flag、summary、benchmark 和 `canonical_output` 一致；三处陈旧 eval_feedback 已只做叙述修正，没有改分。
- 最终确定性回归再次通过：七个 Skill Creator 校验、14 份 Draft 2020-12 Schema、21 条 eval、42/42 exact grading、七份 benchmark/viewer、两条主链与一条补救环，以及 `openspec validate create-seven-stage-personalized-learning-skills --strict`。
- 最终 primary 与 `fallback_for=dclaude` 两个 fresh gclaude session 已交换结构化 findings 并完成互审；两份 inner JSON 均为 `verdict=pass`、blocking=0、major=0，两份 route 的实际 `modelUsage` 均非空。primary 提出的 S2 日期精度 minor 已修复并由 fallback 复验；完整裁决见 `../reviews/final-mutual-crosscheck-summary.md`。
- dclaude 推理前 HTTP 402、空 `modelUsage` 和零 token 原始证据继续保留；用户授权的 fallback 始终标为 gclaude、`fallback_for=dclaude`。两个成功会话具有 session independence，但**不声称 provider diversity**。
- 真实用户、真实持久化后端、长期学习效果或生产环境。
