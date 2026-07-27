---
name: check-capability-concept-graph
description: 独立质量检查 skill，用于判定 S3（build-capability-concept-graph）的输出工件 capability_concept_graph 是否达到决策门 G3。只要需要独立复核一个 S3 移交信封是否合格、是否应该放行进入 S4，就使用本 skill。它不重新建模图谱，只按 G3 量规逐维复核并给出可追溯的 pass / revise_here / return_upstream / blocked 裁决。
---

# 能力—概念图质量检查（check S3 / G3）

独立复核 S3 的输出是否达标。不要替 S3 重建模；只读、只判。

## 开始前

1. 读取 [check-rubric.md](references/check-rubric.md)（G3 量规 = 判定标准）。
2. 读取 [quality-check-result.schema.json](../check-goal-success-contract/references/quality-check-result.schema.json)（本检查的共享输出结构）。
3. 取待检 S3 移交信封；按需参考阶段 skill 的契约 `.agents/skills/build-capability-concept-graph/references/stage-contract.md` 与两份 schema。
4. 仅在需要理解输出形状时读取 [example.md](references/example.md)；案例为设计夹具。

## 执行

1. 结构校验：待检信封能否通过 `handoff-envelope.schema.json`；其 `positive_artifact` 能否通过 `capability-concept-graph.schema.json`。任一不通过即记入 `structural_validation.errors`。
2. 逐维复核 G3（见 check-rubric.md）：结构无环性、先修边可解释性、目标覆盖率、节点粒度一致性、能力与概念区分度、评估题有效性、全链路可追溯性。每维给出证据、评分、阈值、`passed`。
3. 确认复核：S3 为条件确认；当不同建模会实质改变下游诊断题、评估证据或学习路径时，确认应已升级为 `mandatory` 且 `status` 已解，否则 `blocking=true`。
4. 证据来源复核：节点与边的事实依据必须可追溯到 S2 已审计来源；`model_hypothesis` 不得被标为 `external_evidence`；发现证据空白应路由上游而非在图中补造。
5. 复核独立性：不得把 S3 自报的 `verdict=pass` 当作结论；按本量规独立重判，硬先修子图必须自验无环。
6. 汇总：所有维度 `passed` 且确认已解且无证据缺口阻塞建图 → `pass`、`route_to=S4`；否则按主归因给 `revise_here`（结构局部可修）/`return_upstream`（证据空白→S2 或目标矛盾→S1）/`blocked`（输入契约失效）与 `route_to`。

## Fail closed

- 待检信封结构非法或 `positive_artifact` 为 null 且无法定位工件 → 至少 `verdict=revise_here`、`route_to=S3`；输入契约失效则 `blocked`，不臆造通过。
- 硬先修子图出现环，或“主题目录伪装成图谱”（无焦点问题/具名边/误概念/评估/来源）→ 不得 `pass`。
- 节点事实无 S2 证据支撑却被标为 `external_evidence` → 对应维度 `passed=false`，并按上游优先级路由。
- 只能给出复核结论与路由，不得修改被检工件、不得替 S3 重画图或补造领域事实。

## 输出

只输出符合 `quality-check-result.schema.json` 的 JSON：`stage_id=S3`、`gate_id=G3`、`dimension_results[]`、`verdict`、`route_to`、`evidence_summary`、`checked_at`。每个不通过维度必须带 `failure_action` 与 `route_to`。
