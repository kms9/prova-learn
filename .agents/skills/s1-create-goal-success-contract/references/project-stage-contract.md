---
desc: "S1 项目级 Wiki 阶段合同。规定 stages/s1-goal-contract/ 的页面、JSONL、稳定 ID、conversation 追溯、项目 revision、Gate 与历史规则。"
---

# S1 项目级 Wiki 阶段合同

> 现行合同。旧 `run-folder-contract.md` 只用于迁移历史 `runs/<run-id>/`。

## 1. 目录

```text
workspace/<project-slug>/
  INDEX.md
  PROJECT.md
  project-state.json
  timeline.md
  conversations/YYYY-MM/<conversation-id>/
  stages/s1-goal-contract/
    INDEX.md
    working-notes.md
    records.jsonl
    decisions.md
    gate.md
    verification.md
    history/
    goal-contract.md
    research-brief.md
    sources.jsonl
    evidence-table.md
    coverage.md
    capabilities.jsonl
    terminology.jsonl
    confirmation.md
```

每次实质更新必须同时存在一个 conversation，并在 S1 `INDEX.md`、根 `INDEX.md` 和 `project-state.json` 中可定位。

## 2. 稳定 ID

| 对象 | 新项目 ID |
|---|---|
| 项目 | `PRJ-<slug>` |
| 会话 | `CONV-<timestamp>-<suffix>` |
| 事件 | `EVT-<timestamp>-<suffix>-<seq>` |
| 目标 | `GOAL-<slug>-v<n>` |
| 来源 | `SRC-###` |
| 能力 | `CAP-###` |
| 术语 | `TERM-###` |
| 自由结论 | `CL-###` |
| 决策 | `DEC-###` |
| Gate | `GATE-G1-<revision>` |

迁移记录可保留旧 `S001` 等 ID，但必须通过 `legacy_id` 和迁移映射追溯；迁移后新增记录一律使用新 ID。

## 3. conversation

每次 S1 事务的 conversation 必须包含：

- `transcript.md`：用户原文、Agent 回应、工具动作和结果摘要；
- `events.jsonl`：不可变结构化事件；
- `summary.md`：本次变化、未决问题和下一动作；
- `INDEX.md`：元数据和受影响页面。

至少产生：

```text
conversation_started
conversation_turn
tool_result_recorded（使用工具时）
source_added / evidence_added（新增证据时）
artifact_created / artifact_updated / artifact_superseded
user_confirmation（确认时）
gate_evaluated
route_decided
project_state_changed
conversation_closed
```

并非每次都必须产生全部事件，但任何事实或状态变化都必须有对应事件。

## 4. `goal-contract.md`

当前有效目标契约，至少包括：

```markdown
# 目标契约

> goal_id | version | status | project_revision | source_conversation | supersedes

## 目标问题
## 真实使用场景
## 可观察能力
## 最终验收
## 通过规则
## 范围
## 排除项
## 约束
## 风险与隐私
## 证据与确认
```

规则：

- 当前页只表达被接受版本；
- 实质变化前把旧版本复制到 `history/`；
- 新页写 `supersedes` 和来源事件；
- 未确认内容明确标 `proposed`，不得混入 confirmed 段。

## 5. `sources.jsonl`

每行一个来源记录：

```json
{
  "source_id": "SRC-001",
  "title": "来源标题",
  "type": "web",
  "url": "https://example.com",
  "snippet": "来源原文片段",
  "query": "检索意图",
  "retrieved_at": "2026-08-04T03:00:00Z",
  "retrieved_by": "agent",
  "provenance": "external_evidence",
  "category": "official_academic",
  "status": "accepted",
  "trust_note": "适用边界"
}
```

允许 `web/local/vector/agent_trace/expert_note`。  
`model_hypothesis` 和 `user_provided_unverified` 不得支撑 G1 pass。

## 6. `capabilities.jsonl`

```json
{
  "capability_id": "CAP-001",
  "statement": "可观察能力陈述",
  "observable_evidence": ["未见任务中的行为或产物"],
  "knowledge_type": "concept",
  "cognitive_process": "apply",
  "required_evidence_types": ["independent_application", "transfer"],
  "source_refs": ["SRC-001"],
  "goal_ref": "GOAL-example-v1",
  "created_by_event_id": "EVT-..."
}
```

每项能力至少有一个可观察证据。能力与章节、视频、题量必须区分。

## 7. `terminology.jsonl`

```json
{
  "term_id": "TERM-001",
  "original": "用户原词",
  "corrected": "当前工作定义",
  "source_refs": ["SRC-001"],
  "status": "proposed|confirmed",
  "created_by_event_id": "EVT-..."
}
```

只记录理解当前目标所必需的术语校正。

## 8. `evidence-table.md`

主表至少包含：

| Claim ID | Claim | Source refs | Support | Confidence | Applicability |
|---|---|---|---|---|---|

- `CAP-`、`TERM-`、`CL-` 可作为 Claim ID；
- 所有非常识当前结论绑定 accepted 来源；
- `unsupported`、`trace_only` 和矛盾结论进入风险区，不进入主表；
- 来源引用必须能在 `sources.jsonl` 解析。

## 9. `coverage.md`

固定六类：

- `wikipedia_encyclopedia`
- `official_academic`
- `practice_case`
- `recruiting_jd`
- `interview_selection`
- `adversarial_frontier`

每类只出现一次，字段包括：

```text
status = covered | not_applicable | gap | not_executed
reason
gate_effect
source_refs
```

`not_applicable` 必须有可审计理由；找不到资料是 `gap`。

## 10. `research-brief.md`

供 S2 直接消费：

- 当前 `goal_id` 和目标版本；
- 领域/岗位/学段边界；
- 地区、语言、时间窗口；
- 决策风险；
- 按优先级排序的研究问题；
- 来源限制；
- 六源检索种子：`job_career/books_courses/papers_research/community_web/standards_official/artifacts_validation`。

它不代表已完成 S2 研究。

## 11. `confirmation.md`

至少包括：

```text
mode=mandatory
status=pending|confirmed|rejected
questions
verbatim_responses
confirmed_items
open_questions
assumptions_changed
conversation_ref
event_ref
confirmed_at
```

用户原文保存在 conversation；本页保存结构化确认结果。

## 12. `records.jsonl`

S1 原子变更索引，不替代专属 JSONL。每条至少包含：

```json
{
  "record_id": "REC-S1-0001",
  "record_type": "source_added",
  "object_ref": "SRC-001",
  "event_ref": "EVT-...",
  "conversation_ref": "CONV-...",
  "project_revision": 3
}
```

只追加。旧记录不得原地改写。

## 13. `decisions.md`

记录：

- 选择了什么；
- 排除了什么；
- 依据哪些证据；
- 是否需要用户确认；
- 决策事件和项目版本；
- 对 S2–S7 的影响。

## 14. `gate.md`

逐维格式：

| Dimension | Evidence refs | Score | Threshold | Passed | Failure action | Route |
|---|---|---:|---|---|---|---|

G1 至少检查：

1. 目标可观察；
2. 成功标准可判定；
3. 场景真实；
4. 外部现实校准；
5. 六类覆盖；
6. 边界与排除项；
7. 约束完整；
8. 目标—能力—验收一致；
9. conversation 和事件追溯；
10. 项目版本与索引一致。

结尾必须明确：

```text
gate_id
gate_revision
verdict
route_to
evaluated_by_event_id
```

## 15. `verification.md`

确定性检查：

- 项目根文件齐全；
- conversation 四文件齐全；
- S1 文件齐全；
- JSONL 可解析；
- 稳定 ID 可解析；
- 当前页含来源 conversation/event；
- 没有占位符或空表；
- `project-state.json` revision 与事件一致；
- S1/根索引、timeline 和 route 同步；
- accepted external evidence 数量；
- 未解决 high 风险。

只有全部通过才写 `state=verified`。

## 16. `INDEX.md`

结论先行，至少展示：

- 当前目标和目标版本；
- S1 状态、G1、route；
- 当前项目 revision；
- 最近 conversation；
- 当前页面链接；
- 历史版本；
- 未决问题和下一动作。

## 17. 项目状态事务

更新前：

```text
expected_project_revision = 当前读取值
```

提交后：

```text
project_revision = expected + 1
updated_by_event_id = 本次 project_state_changed
last_conversation_id = 当前 conversation
```

G1 pass 时：

```text
S1.state=completed
S1.gate=pass
S1.route_to=S2
current_stage=S2
route_to=S2
status=active
```

pending/blocked 时保持 S1，不得生成虚假下游状态。
