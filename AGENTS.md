# Prova Learn 代理协作 Wiki

> 页面类型：仓库级运行协议与导航页  
> 适用范围：本文件所在目录及全部子目录；更深层的 `AGENTS.md` 可补充或覆盖局部规则  
> 维护语言：中文优先；路径、Schema 字段、枚举、命令和外部标识保留原文  
> 最近全面核对：2026-07-27；主控入口补充核对：2026-08-04
> 当前主线：统一主控入口、七阶段个性化学习 Skill、阶段质量门、项目级 LLM Wiki、证据驱动回路

## 1. 项目定位

本仓库把个性化学习过程实现为一个统一主控入口和七个可独立调用、可串联、可返工的阶段 Skill。主控只负责意图分发、调用、落盘复核与下一步提示，不是第八个业务阶段。系统不是一次性生成课程，而是持续执行：

```text
目标校准 → 领域取证 → 结构建模 → 学习者诊断
→ 路径规划 → 教学交互 → 掌握验证与重规划
```

每个阶段都有独立质量门。任何 `pending`、`blocked`、证据不足、研究未执行或版本冲突都必须如实保留，不能为了继续流程而伪造通过。

本仓库当前以文档、Skill 契约、JSON Schema、HTML 模板、eval 和 OpenSpec 为主要实现载体，不要套用服务端、数据库或前端应用仓库的默认假设。

## 2. 权威来源顺序

发生冲突时，按以下顺序判断：

1. 用户当前明确指令。
2. 当前路径适用的 `AGENTS.md`。
3. 当前主控 `.agents/skills/al-orchestrate-personalized-learning/SKILL.md`、七个 `.agents/skills/sN-*/SKILL.md`，以及它们明确引用的合同。
4. 当前 OpenSpec change 的 proposal、design、specs、tasks；它描述需求和变更边界，但任务勾选不等于实现或发布证明。
5. `docs/chat_log/` 中标为已实施的结论文档和研究记录。
6. `example/`、eval、benchmark、review、外部模型 JSON 等点时证据。
7. `.specstory/history/` 的原始会话记录。

特别规则：

- 用户已明确要求以后以当前 Skill 定义和命令为准。历史 OpenSpec、文档和会话中没有 `s1-`～`s7-` 前缀的旧目录名，只能作为历史引用，不得据此回退当前命名。
- `.agents/AGENTS.md`、`.agents/project-workspace-contract.md` 与 manifest/profile 已把 S1–S7 迁移到统一项目级 Wiki；本页 §7、§13 中旧 run-folder/三工件细节只作迁移背景，不得覆盖 `.agents` 下的现行合同。
- `.specstory/history/` 用于回答“为什么这样设计”和恢复决策过程，不是当前实现的直接真相。引用历史结论前必须再检查现有文件。
- `docs/chat_log/个性化学习理论与七阶段策略归属排查.md` 与 `docs/chat_log/S5基于学习者输出的学习策略检查与适配场景设计.md` 当前是“尚未实施”的设计输入；其中建议字段、策略分类或映射规则不能冒充现行 Schema 能力。
- 示例只是夹具或点时执行结果。文件存在不证明上游门已通过，也不证明整条 S1→S7 链完整。

## 3. 仓库地图

| 路径 | 角色 | 使用方式 |
|---|---|---|
| `.agents/skills/al-orchestrate-personalized-learning/` | 统一主控 Skill | 用户不想自行选择阶段，或说“继续/下一步/完整流程”时的默认入口 |
| `.agents/skills/s1-...`～`s7-...` | 七阶段现行 Skill | 由主控分发，或在明确阶段任务时直接调用 |
| `.agents/skills/*/references/` | 阶段契约、兼容合同、Schema、示例 | 按目标 `SKILL.md` 指示读取；当前主要交付以 `.agents` 项目工作区合同与 manifest/profile 为准 |
| `.agents/skills/*/assets/stage-report.html` | S3–S7 阶段专用 HTML 模板 | 由最终 JSON 填充，不作为事实来源（S1/S2 已改 run-folder 交付） |
| `.agents/skills/*/evals/evals.json` | 每阶段正向和反向/阻断 eval | Skill 变更后的行为校验输入 |
| `.codex/skills/openspec-*` | 本仓库 OpenSpec 工作流 | proposal、explore、apply、archive |
| `openspec/changes/` | 需求、设计、规格、任务与评审证据 | 先查 `openspec status`，再决定动作 |
| `docs/chat_log/` | SOP、调研、独立结论、错误台账 | 区分“现状”“建议”“尚未实施” |
| `.specstory/history/` | SpecStory 生成的会话历史 | 用 `rg` 定位决策，不整份当规格复制 |
| `example/` | 真实或夹具化阶段产物 | 先核对来源、状态、门和来源阶段的当前交付合同 |
| `scripts/run_skill_evals.py` | Skill eval 编排入口 | 先看 `--help` 或使用 `--dry-run` |

关键知识页：

- [七阶段最终 SOP](docs/chat_log/个性化学习SOP步骤拆分最终结论.md)
- [六源信息收集建议](docs/chat_log/信息收集建议.md)
- [七阶段理论职责排查](docs/chat_log/个性化学习理论与七阶段策略归属排查.md)
- [S5 策略适配场景设计](docs/chat_log/S5基于学习者输出的学习策略检查与适配场景设计.md)
- [S3 大纲—知识点关联](docs/chat_log/大纲-知识点关联.md)
- [三工件 HTML 需求](docs/chat_log/七阶段Skill输出HTML可视化与交互需求.md)
- [实施与评估错误台账](docs/chat_log/七阶段个性化学习Skill实施与评估错误记录.md)

## 4. 核心术语

### 4.1 Sx 与 Gx

- `Sx`：第 x 个执行阶段（Stage）。
- `Gx`：紧随 Sx、判断该阶段工件能否被下游消费的质量门（Gate）。
- `G1` 是 S1 目标契约质量门，不是学习理论、外部标准或另一个 Skill。
- `G7` 评价 S7 掌握判定与重规划事务的质量；G7 工件合格不自动等于学习者已掌握。只有 `GOAL_ACHIEVED` 且最终验收与保持要求通过，才能 `route_to=complete`。

“已通过 Gx”不能由文件存在、裸 `positive_artifact` 或自然语言声明推断。消费上游工件时至少验证：

```text
stage_id=Sx
+ status=completed
+ input_validation.status=pass
+ 具名 positive_artifact 非空且符合阶段 Schema
+ 全部 rubric_results[].passed=true
+ quality_evaluation.verdict=pass
+ route_to 符合阶段合同
+ 确认策略已满足
+ 交付模型满足来源阶段合同（S1 七项 / S2 九项 / S3–S7 三工件）
```

### 4.2 交付模型

S1–S7 当前共享 `workspace/<project-slug>/` 项目级 LLM Wiki：Markdown 表达当前接受含义，JSONL 保存不可变事件与原子记录，`project-state.json` 保存派生状态和版本指针。各阶段在 `stages/sN-*/` 维护入口、业务页面、Gate 与 verification；旧 run、单体 JSON envelope 和 HTML 只作迁移输入或兼容导出，不是主要真相源。完整合同以 `.agents/project-workspace-contract.md`、`.agents/stage-delivery-manifest.json` 和目标 Skill 为准。

### 4.3 证据与安全态

证据角色至少区分：

- `model_hypothesis`
- `market_signal`
- `external_evidence`
- `user_provided_unverified`
- `learner_behavior`

`model_hypothesis` 和 `user_provided_unverified` 不能被计为已验证外部证据。以下状态必须保留真实语义，不得强制改成 `pass`：

`pending`、`blocked`、`unknown`、`evidence_insufficient`、`research_blocked`、`not_executed`、`version_conflict`。

## 5. 统一主控与七阶段导航

| 阶段 / Skill | 主输入 | 具名正向工件 | 正常路由 |
|---|---|---|---|
| 主控 `$al-orchestrate-personalized-learning` | 用户自然语言意图、项目状态与 `route_to` | 阶段选择/执行复核与下一步回执；无独立业务工件 | 分发到 S1–S7 或只读状态 |
| S1 `$al-s1-create-goal-success-contract` | 学习诉求、场景、约束、外部预检 | `stages/s1-goal-contract/` 目标契约阶段区 | G1 → S2 |
| S2 `$al-s2-create-domain-evidence-landscape` | 已过 G1 的项目 Wiki 与研究简报 | `stages/s2-domain-evidence/` 研究回答阶段区 | G2 → S3 |
| S3 `$al-s3-build-capability-concept-graph` | 已过 G1/G2 的目标与证据 | `stages/s3-capability-graph/` | G3 → S4 |
| S4 `$al-s4-diagnose-learner-frontier` | 已过 G1/G3 的目标与图谱、真实行为证据 | `stages/s4-learner-diagnosis/` | G4 → S5 |
| S5 `$al-s5-plan-learning-sessions` | 已过 G1/G3/G4 的目标、图谱、学习前沿 | `stages/s5-learning-plan/` | G5 → S6 |
| S6 `$al-s6-run-instructional-interaction` | 已过 G2/G3/G4/G5 的证据、图谱、快照、计划 | `stages/s6-instruction/` 与 `sessions/<session-id>/` | G6 → S7 |
| S7 `$al-s7-verify-mastery-and-replan` | 已过 G3/G4/G5/G6 的图谱、历史快照、计划、真实交互 | `stages/s7-mastery-replan/` | G7 → S1～S7 或 complete |

### 5.1 Skill 路由触发

- 用户不确定阶段、只想调用一个入口、要求继续/下一步/完整流程：主控；主控读取项目状态并委托 S1–S7。
- 新学习目标、目标实质变化、成功证据或岗位/领域名称校准：S1。
- 领域全景、真实联网、STORM 式研究、六源取证或 S3 暴露来源空白：S2。
- 能力大纲、学习单元、原子知识点、映射、先修关系和测评图谱：S3。
- “从哪里开始学”、误概念、提示依赖、迁移表现或争议节点复测：S4。
- 学习路径、会话、时间节奏、教学策略选择和首个会话合同：S5。
- 真实教学会话、解释、正反例、支架、练习、反馈和交互轨迹：S6。
- 是否掌握、版本化更新学习者模型、延迟复测、归因和重规划：S7。

主控默认一次只执行一个阶段。只有用户明确要求补齐前置或完整流程时才按已验证 `route_to` 逐阶段推进；遇到 mandatory/升级确认、真实学习者回答、`pending`、`blocked`、版本冲突或上游返工 route 必须停止并给出具体下一步。

阶段 Skill 均须能独立理解自己的直接依赖。独立调用时以项目根、`project-state.json`、manifest 前置、阶段入口、Gate 与 verification 校验上游；缺失依赖时 fail closed 并路由到最早失效阶段。

### 5.2 确认策略

- S1、S5：`mandatory`，未确认不得前进。
- S2、S3、S4、S7：`conditional`，高风险、分歧或多方案时升级为强制确认。
- S6：`inform` 为主，但必须有真实学习者交互，不能代写学习者回答。

快速档只允许在合同条件满足时连续执行 S2+S3 或 S4+S5，而且仍要分别满足两个阶段的交付合同并依次通过两个门。S1、S7 永不合并。

## 6. 不可降级的领域规则

### 6.1 S1/S2 联网研究

冷启动、目标实质变化或关键证据过期时，S1/S2 必须真实联网。模型知识只能产生假设、视角、问题和检索词，不能代替外部证据。网络或关键来源不可用时，记录 `research_blocked` 或 `gap`，不得通过 G1/G2。

S2 使用六个强制证据通道：

1. `job_career`
2. `books_courses`
3. `papers_research`
4. `community_web`
5. `standards_official`
6. `artifacts_validation`

百科、搜索结果页和聚合页只作为入口，最终结论应追溯到可访问的原始或权威来源。研究视角用于提出问题，六源通道用于检查证据覆盖；两者不能混为一类。

### 6.2 结构、个性化与教学的边界

- S3 是稳定能力结构、学习单元、原子节点、映射和先修关系的唯一建模阶段。
- 大纲层级、展示顺序或 `scope_role` 不能直接充当个性化学习顺序。
- S4 提供真实学习者状态和策略选择信号。
- S5 是基于学习者与节点条件选择路径、教学方法、支架和复习安排的主责阶段。
- S6 执行 S5 决策并记录实际发生的交互与提示，不用计划字段冒充行为事件。
- S7 验证策略效果、区分内容/策略/诊断/图谱/来源/目标问题，并路由到最早污染阶段。

Bloom 是认知目标分类框架，不是教学方法；建构主义是理论取向；苏格拉底提问是教学方法；费曼式复述更适合作为 `teach-back`/自我解释技术。不要把理论、方法、活动、练习节奏和测评证据塞入同一个枚举，也不要把任何方法设为所有学习者的默认策略。

当前有关 S5 细粒度策略资格检查、禁用条件、方法追踪和切换规则的设计仍是候选需求。除非这些字段已同步进入当前 Skill、Schema、eval 和 OpenSpec，否则只能在分析中引用，不能声称已经实现。

### 6.3 S6/S7 真实行为

- S4/S6 不得代写学习者回答。
- S6 的提示阶梯是计划；只有实际 `interaction_events` 才能证明提示被使用。
- “学习者说懂了”、一次答对、单题得分或流畅解释都不能单独证明掌握。
- S7 必须检查正确性、推理、提示依赖、迁移、置信度校准和必要的延迟保持。
- 没有真实后端时，学习者模型更新写 `not_executed`；版本冲突时不应用补丁。

## 7. 产物与页面合同

**S1（run-folder 目录交付）**：

- 在 `workspace/<project-slug>/runs/<run-id>/` 下写一组固定命名文件（`sources.jsonl` 记录预检来源、`evidence_table.md`/`coverage.md` 汇总表、`capabilities.jsonl`/`terminology.jsonl` 记录、`goal-contract.md`/`research-brief.md`/`confirmation.md`/`g1-evaluation.md`/`verification.md` 与 `INDEX.md` 主索引）；不再产出单体 Markdown/JSON/HTML。
- 记录型用 `.jsonl`（一行一条、稳定 ID、跨文件互引），汇总/审计型用 `.md` 表；状态机带 guard 控制写入顺序，`INDEX.md` 为下游读取入口，`verification.md` 收尾。
- 下游阶段经 `INDEX.md` 读取上游 S1（按 run-folder 七项机读校验确认 G1 通过），历史 run 仅供背景。
- run folder 内不得出现独立 PNG/JPEG/WebP/SVG/GIF 图片资产或 HTML 文件；"可视化" 默认指数据表视图。
- 任一必需文件缺失、跨文件 ID 不可解析、存在占位符或 G1 机读七项不满足时，不得报告"本阶段交付完整完成"；但产物失败不篡改领域质量门本身。

**S2（同一 run 的 LLM Wiki 阶段区）**：

- 读取最新已过 G1 的根 `INDEX.md`、`research-brief.md` 及相关 S1 文件，在同一 run 的 `s2/` 写：
  `INDEX.md`、`research-log.md`、`sources.jsonl`、`coverage.md`、`evidence-items.jsonl`、
  `research-answers.md`、`answer-validation.md`、`g2-evaluation.md`、`verification.md`。
- `research-answers.md` 按 S1 priority questions 逐题明确回答；每题必须完成来源覆盖、证据角色分离、
  来源独立性、可靠性/权威性、时效/地区适配、冲突平衡、可观察相关性、边界/缺口透明八维校验。
- S2 写入前重读根 `INDEX.md`，只新增/更新 `## 阶段输出` 中的 S2 行，链接 `s2/INDEX.md`；
  不得改写 S1 目标、确认、G1 或历史事实。
- S2 不生成独立 JSON 信封、单体 S2 Markdown、HTML 或图片。阻断时仍写诚实九文件诊断区和根索引状态。
- 已通过 G2 必须满足 S2 `run-folder-contract.md` 的九项机读条件；文件存在或一句“研究完成”不算通过。

**S3–S7（三工件模型，暂留）**：

- 先写完整 Markdown，再生成无损 JSON，最后派生 HTML。
- 实质内容变化必须同步 Markdown 与 JSON，并重新生成、重新校验 HTML。
- HTML 只允许搜索、筛选、切换、展开和浏览已存在的数据，不接受业务输入，不执行模型更新。
- HTML 内嵌规范 JSON 并由其动态渲染；不得展示 Schema、模板、生成状态或通用文件装载器。
- HTML 是阶段唯一默认可视化交付。除非用户明确改变需求，禁止调用图像生成工具，禁止生成或依赖 PNG、JPEG、WebP、SVG、GIF 等独立图片资产。
- `pending` 或 `blocked` 也要生成三份诚实工件，展示缺口、当前结论、恢复条件和路由；不要用空白占位。

## 8. OpenSpec 工作流

当用户要求提出、探索、实施或归档变更时，必须使用对应仓库 Skill：

- `$openspec-propose`
- `$openspec-explore`
- `$openspec-apply-change`
- `$openspec-archive-change`

执行约定：

1. 先运行 `git status --short --branch`，识别并保留用户已有改动。
2. 使用 `openspec status --change <name>` 和相关工件判断当前状态。
3. 在 apply 前核对 proposal、design、specs、tasks 与现行 Skill 是否漂移。
4. 实施后更新任务与证据，但不因复选框已勾选就宣称 release-ready。
5. 归档前运行严格验证，并区分“规格有效”“实现完成”“真实集成通过”。

当前 `openspec/changes/` 中可能同时存在已生成全部工件但尚未归档的 change；不要把 “All artifacts complete” 误解成已经实施或已验收。

## 9. 外部模型路由

外部模型用于旁路探索、交叉评审和 Skill eval；主线程负责检查其外层 JSON、实际文件、diff 和验证结果。

### 9.1 Claude 路由

默认非交互并优先返回 JSON：

```bash
gclaude -p '<task>' --output-format json --no-session-persistence
dclaude -p '<task>' --output-format json --no-session-persistence
```

等价路由：

- `gclaude` → `claude --dangerously-skip-permissions`
- `dclaude` → `claude --settings /Users/logo/.claude/deepseek.json --dangerously-skip-permissions`

规则：

- 不用主观固定等待窗口判定失败；等待进程真实结束，以退出码、外层 JSON、日志或用户停止指令为准。
- 实际模型以外层 JSON 的 `modelUsage` 为准，不依赖模型自述。
- 若任务结果应为结构化数据，要求 `.result` 本身为 JSON，并分别校验外层和内层 JSON。
- 写文件任务以文件内容、diff 和验证产物为准，不要求模型回显全文。
- `dclaude` 因余额、路由、连接或格式问题失败时，先记录错误，再按用户授权改用 `gclaude` 重试；保留 `fallback_for=dclaude` 之类的来源说明，不能把 gclaude 结果冒充 dclaude 通过。

### 9.2 Cursor 路由

单次只读分析、解释和校验优先 `--mode ask`：

```bash
grcursor -p '<task>' --output-format json --mode ask
op46cursor -p '<task>' --output-format json --mode ask
op46tcursor -p '<task>' --output-format json --mode ask
op48cursor -p '<task>' --output-format json --mode ask
gecursor -p '<task>' --output-format json --mode ask
```

| alias | 等价命令 |
|---|---|
| `grcursor` | `agent --trust --force --model grok-4.5-xhigh` |
| `op46cursor` | `agent --trust --force --model claude-4.6-opus-high` |
| `op46tcursor` | `agent --trust --force --model claude-4.6-opus-high-thinking` |
| `op48cursor` | `agent --trust --force --model claude-opus-4-8-high-thinking` |
| `gecursor` | `agent --trust --force --model gemini-3.1-pro` |

需要确认实际模型时使用 `--output-format stream-json`，读取 `type=system`、`subtype=init` 事件的 `model` 字段。若任务结果还要求内部 JSON，解析外层 `.result` 后再次校验；CLI 失败时不要假定输出仍是合法 JSON。与 Claude 路由一样，不以主观等待时间中断任务，以最终退出码、JSON/NDJSON、日志或用户指令判断结果。

### 9.3 Alias 与 subagent 边界

- 单次验证、模型对比、外部评审或获取某一路由 JSON/NDJSON，直接调用对应 alias。
- 只有用户明确要求 subagent/委托/并行多代理，或任务能拆成互不阻塞、边界清楚的并行检查时，才使用 Codex subagent。
- 主线程下一步立即依赖结果、写入范围高度重叠或只需一次 alias 的任务，不使用 subagent。
- 若 subagent 需要走 Claude/Cursor，必须在任务中明确指定 alias；subagent 不是这些 alias 的替代品。
- 主线程始终负责核对外部结果、实际文件、diff、测试和 JSON/NDJSON 证据，再做最终汇总。

## 10. 错误、证据和重试

本项目采用 error-first 记录：

1. 遇到实质性 CLI、Schema、OpenSpec、eval、外部路由或页面验证错误，先把症状、命令、退出状态和影响追加到[错误台账](docs/chat_log/七阶段个性化学习Skill实施与评估错误记录.md)。
2. 再修复；保留原始症状，追加根因、修复和复验证据，不覆盖历史。
3. 锚点漂移、并发已修复或目标已存在时，先重新读取当前文件，不机械重复补丁。
4. 同一路由可重试；用户已允许 dclaude 异常时切换 gclaude。所有 fallback 必须保留来源与未执行门。

汇报时分开陈述：

- 当前文件事实；
- 目标设计或尚未实施建议；
- 推断；
- 已运行且通过的验证；
- 未运行、被阻断或仅点时通过的门。

## 11. 修改纪律

- 搜索文件和文本优先 `rg` / `rg --files`。
- 编辑已有或新建文本文件使用 `apply_patch`。
- 工作树可能包含用户正在进行的重命名和未提交修改；只改任务范围内文件，不恢复、覆盖、清理或提交无关变更。
- 不使用 `git reset --hard`、破坏性 checkout 或大范围删除。
- 项目专用 Skill 固定放在 `.agents/skills/<skill-dir>/`；不要默认安装到全局目录。
- 新脚本不是默认方案。优先现有命令、Schema、eval 和脚本；确需创建新脚本时先征得用户同意。
- 不手工改 `.specstory/history/` 来伪造历史；它由会话记录机制维护。
- 对需要联网的当前事实必须实际检索并保留来源；对本地仓库事实先检查文件和命令输出。

## 12. 验证清单

先运行与本次改动成比例的最小验证，再决定是否执行昂贵的外部 eval。

### 12.1 基础检查

```bash
git diff --check -- AGENTS.md .agents/skills openspec docs scripts
find .agents/skills -type f -name '*.json' -exec jq empty {} +
openspec validate --all --strict --no-interactive
```

### 12.2 主控与七个阶段 Skill 结构

```bash
for skill_dir in .agents/skills/s{1,2,3,4,5,6,7}-*; do
  python3 /Users/logo/.codex/skills/.system/skill-creator/scripts/quick_validate.py "$skill_dir"
done
python3 /Users/logo/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  .agents/skills/al-orchestrate-personalized-learning
```

`quick_validate.py` 只证明结构和 frontmatter 基本有效，不证明阶段语义、Schema 实例、HTML 视觉或真实学习效果。

### 12.3 Eval

```bash
python3 scripts/run_skill_evals.py --help
python3 scripts/run_skill_evals.py --all --route dclaude --dry-run
python3 scripts/run_skill_evals.py --all --route dclaude
```

外部 eval 前检查输出目录、现有 workspace 和当前路由可用性。不得删除或覆盖历史证据来凑出整洁结果。dclaude 失败时按第 9、10 节记录后使用 gclaude 重试，并明确哪一道原始路由门仍未通过。

### 12.4 声明完成前

- 一个主控目录和七个阶段目录的数量、角色与 Skill 名称与本页一致；主控未被当成 S0/G0。
- 项目工作区合同、manifest/profile、project-state/event Schema 与 S1–S7 阶段入口一致；兼容导出不冒充主要交付。
- 所有相对链接存在，JSON/YAML 可解析，Schema 自检与代表性实例验证通过。
- 阶段正向、反向/阻断 eval 都存在，executor prompt 未泄露 grader-only 期望。
- S1–S7 的项目根、conversation、阶段 Wiki/JSONL、Gate、verification、revision、根索引与 timeline 一致。
- S1/S2 的研究与逐题回答规则、S3–S7 的阶段专属页面/记录和所有跨文件稳定 ID 均按现行 manifest/profile 验证。
- 所有实际失败已先登记，修复后有复验证据。
- 明确列出尚未执行的浏览器视觉验收、真实账户、真实学习者、长期保持或生产级门。

## 13. LLM Wiki 维护格式

新增或重写关键文档时，使页面可被人和代理独立检索：

1. 标题后写日期、状态、范围和适用对象。
2. 开头给出结论与当前/目标边界。
3. 再写术语、输入、流程、输出、质量门、失败路由和证据来源。
4. 使用稳定的相对链接连接源文档、现行契约、Schema、eval 与错误台账。
5. 把原始证据、编译结论和历史会话分层，不把建议写成已确认决策。
6. 记录“最后核对时间”和未验证缺口；点时检查不能成为永久证明。
7. 保持本文件紧凑。仓库级与上级 `AGENTS.md` 会按层级合并，超长规则可能被截断；详细合同留在 Skill references，本页负责导航、路由和不可违背的边界。

### 13.1 S1 run-folder 标准结构（LLM Wiki 落盘方式）

S1 采用 `storm-evidence` 式证据治理落盘：一个 run folder，内含固定命名文件 + 严格字段契约，记录型 `.jsonl`、汇总/审计型 `.md`，状态机带 guard、稳定 ID 跨文件互引：

```text
<cwd>/workspace/<project-slug>/runs/<run-id>/
  INDEX.md            主索引（下游读取入口：结论先行 + 文件清单 + 运行历史指针）
  sources.jsonl       预检来源（source_id/type/url|file/snippet/query/retrieved_at/provenance/category/status）
  evidence_table.md   来源↔S1结论 支撑表（Claim→Source→support/confidence）
  coverage.md         六类预检覆盖表 + S2 六源映射说明
  capabilities.jsonl  可观察能力（capability_id/statement/observable_evidence/bloom_level/source_ids）
  terminology.jsonl   术语校正（term_id/original/corrected/evidence_refs）
  goal-contract.md    目标/场景/验收/通过规则/范围/排除/约束（人审编译稿）
  research-brief.md   domain_research_brief（S2 直接消费，含 six_source_seeds）
  confirmation.md     确认问题/回答/状态 + open_questions + confirmed_items
  g1-evaluation.md    G1 量规逐维 + verdict + route
  verification.md     状态机终态 + 统计 + 未决风险 + 命令
```

- `project-slug` = 校准后目标的 kebab-case，稳定不变；根本改变目标时开新 slug。同项目多次运行并列在 `runs/`，下游按时间戳取最新 run 的 `INDEX.md`。
- 稳定 ID（`S001`/`CAP-001`/`TERM-001`/`CL-001`/`G1-*`）跨文件互引，交付前必须全部可解析。
- "已通过 G1"（机读七项）：11 文件齐全 + `g1-evaluation` verdict=pass/route=S2/全维 passed + `confirmation` confirmed + `verification` verified 无 high 风险 + 无占位符 + 跨文件 ID 可解析 + `sources.jsonl` ≥1 accepted external_evidence。
- 逐文件字段契约与状态机 guard 详见 S1 `references/run-folder-contract.md` 与 `SKILL.md`。

### 13.2 S2 run-folder 阶段区（回答 S1 问题）

S2 不新建独立运行或三工件，而是在同一已过 G1 的 run 下追加具名阶段区：

```text
<cwd>/workspace/<project-slug>/runs/<run-id>/
  INDEX.md                 根索引；新增/更新独立 S2 阶段行
  ...S1 文件保持不变...
  s2/
    INDEX.md               S2 阶段入口、问题回答摘要、G2 与 S3 指引
    research-log.md        视角、查询、轮次、追问、纳入排除与未执行项
    sources.jsonl          S2 实际核验来源、可靠性、独立组、时效、证据角色
    coverage.md            六源覆盖、独立样本与多源矩阵
    evidence-items.jsonl   Task/Capability/Knowledge/Skill/Evidence 等原子对象
    research-answers.md    按 S1 priority questions 逐题明确回答（首要人审交付）
    answer-validation.md   每题八维校验、共识/分歧/缺口、饱和/成熟度/刷新
    g2-evaluation.md       G2 分维量规、verdict 与 route
    verification.md        九文件、映射、引用、根索引、反占位与风险收尾
```

- 稳定 ID 使用 `RQ-###`/`ANS-###`/`Q-###`/`E-###`/`ITEM-###`/`GAP-###`；S1 的
  `S###`/`CAP-###`/`TERM-###` 保持原样。
- 每个 S1 priority question 必须恰好映射一个 RQ/ANS，保留问题原文；证据不足可以明确回答
  `partial/unanswered`，不能静默遗漏或补造结论。
- 每个答案校验八维：source coverage、provenance separation、source independence、
  reliability/authority、timeliness/region fit、contradiction balance、observable relevance、
  boundary/gap clarity。
- “已通过 G2”（机读九项）：九文件+根索引链接；问题全映射；真实在线六视角至少两轮且有追问；
  六源审计无阻塞 gap；accepted external evidence 与跨引用可解析；关键答案八维通过；结构饱和且至少 L1；
  升级确认已完成；G2 全维 pass/route=S3 且 verification=verified、无阻塞 high 风险和占位符。
- 逐文件字段契约与状态机 guard 详见 S2 `references/run-folder-contract.md` 与 `SKILL.md`。
