# S1 项目级 Wiki 示例

> 设计夹具，不是真实运行结果。示例用于说明目录和追溯，不可作为外部证据。

## 正向夹具：PostgreSQL 查询优化

```text
workspace/postgresql-query-optimization/
  INDEX.md
  PROJECT.md
  project-state.json
  timeline.md
  conversations/2026-08/CONV-.../
  stages/s1-goal-contract/
```

### 项目状态摘要

```json
{
  "project_revision": 4,
  "status": "active",
  "current_stage": "S2",
  "route_to": "S2",
  "active_goal_id": "GOAL-postgresql-query-optimization-v1",
  "active_goal_version": 1,
  "last_conversation_id": "CONV-20260804T040000Z-example",
  "stage_status": {
    "S1": {
      "state": "completed",
      "gate": "pass",
      "route_to": "S2",
      "revision": 3,
      "entrypoint": "stages/s1-goal-contract/INDEX.md"
    }
  }
}
```

### 当前目标

学习者在 PostgreSQL 18 沙箱中，能够独立：

1. 阅读 `EXPLAIN (ANALYZE, BUFFERS)`；
2. 区分估算与实际执行；
3. 形成诊断假设；
4. 设计索引或查询改写；
5. 在三个未见查询上验证收益与副作用。

不允许直接修改生产数据库。单纯看完材料、刷题数量或一次选择题不能通过。

### 追溯链

```text
用户原文
→ conversation transcript
→ user_confirmation event
→ GOAL-postgresql-query-optimization-v1
→ CAP-001..CAP-005
→ SRC-001..SRC-008
→ GATE-G1-3
→ project revision 4
→ route S2
```

### 关键文件

- `goal-contract.md`：当前确认目标；
- `sources.jsonl`：实际预检来源；
- `evidence-table.md`：结论与来源；
- `capabilities.jsonl`：能力和未见证据；
- `confirmation.md`：用户强制确认；
- `gate.md`：G1 逐维判定；
- `verification.md`：conversation、ID、项目版本和索引检查。

## 阻断夹具：“七天成为 AI 专家”

用户拒绝提供场景、范围和验收，并要求不联网。

项目仍然创建并记录 conversation，但状态保持：

```text
current_stage=S1
route_to=S1
G1=blocked
confirmation=pending
external_evidence=0
verification=research_blocked
```

系统不得：

- 伪造来源；
- 用模型记忆替代预检；
- 把 100 道选择题视为专家能力；
- 路由到 S2；
- 只输出一个 JSON 后声称完成。
