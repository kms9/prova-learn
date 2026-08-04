---
desc: "历史 S1 run-folder 兼容合同。仅用于读取和迁移 workspace/<project-slug>/runs/<run-id>/；新 S1 禁止继续写该结构。"
---

# 历史 S1 Run-Folder 兼容合同

该合同只服务于旧项目迁移。现行 S1 合同见：

- `../../../project-workspace-contract.md`
- [project-stage-contract.md](project-stage-contract.md)
- `scripts/migrate_legacy_run.py`

## 1. 旧目录

```text
workspace/<project-slug>/runs/<run-id>/
  INDEX.md
  sources.jsonl
  evidence_table.md
  coverage.md
  capabilities.jsonl
  terminology.jsonl
  goal-contract.md
  research-brief.md
  confirmation.md
  g1-evaluation.md
  verification.md
  s2/...
```

旧目录必须保持只读。

## 2. 迁移映射

| 旧文件 | 项目 Wiki |
|---|---|
| `INDEX.md` | `stages/s1-goal-contract/history/<run-id>-INDEX.md` |
| `sources.jsonl` | `stages/s1-goal-contract/sources.jsonl` |
| `evidence_table.md` | `stages/s1-goal-contract/evidence-table.md` |
| `coverage.md` | `stages/s1-goal-contract/coverage.md` |
| `capabilities.jsonl` | `stages/s1-goal-contract/capabilities.jsonl` |
| `terminology.jsonl` | `stages/s1-goal-contract/terminology.jsonl` |
| `goal-contract.md` | `stages/s1-goal-contract/goal-contract.md` |
| `research-brief.md` | `stages/s1-goal-contract/research-brief.md` |
| `confirmation.md` | `stages/s1-goal-contract/confirmation.md` |
| `g1-evaluation.md` | `stages/s1-goal-contract/gate.md` |
| `verification.md` | `stages/s1-goal-contract/verification.md` |
| `s2/*` | `stages/s2-domain-evidence/*` |

迁移器还必须生成：

- 项目根与 `project-state.json`；
- migration conversation；
- `artifact_migrated` 事件；
- `_machine/migration-map.json`；
- 逐文件 SHA-256；
- 阶段 `records.jsonl`、`decisions.md` 和当前 `INDEX.md`。

## 3. ID 兼容

旧来源 ID（如 `S001`）在复制文件中保持原样，以保证历史引用不失效。迁移映射和 `records.jsonl.legacy_id` 负责连接旧 ID。

迁移后新增来源使用 `SRC-###`；不得继续分配新的 `S###`。

## 4. Gate 兼容

迁移继承旧 `g1-evaluation.md` 的可审计 verdict，但**迁移动作本身不重新证明 G1**。

- 旧 G1 pass：项目可 route S2；
- 旧 G1 revise/pending/blocked：项目保持 S1；
- 无法解析 Gate：`not_evaluated → S1`。

## 5. 禁止事项

- 不得删除或改写旧 run；
- 不得把迁移当成新的外部研究；
- 不得把旧 partial/gap 自动提升；
- 不得在旧 run 和新项目 Wiki 同时继续写入；
- 不得把旧单体文件重新包装为当前唯一真相。
