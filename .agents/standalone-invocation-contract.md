# 独立 Skill 调用与前置恢复合同

> 适用范围：S2–S7。S1 负责创建项目，S2–S7 不得在没有项目和上游事实时生成孤立正向工件。

## 1. 解析顺序

1. 用户显式提供的 `workspace/<project-slug>/`；
2. 当前工作目录中唯一含 `INDEX.md` 与 `project-state.json` 的项目根；
3. 旧 `runs/<run-id>/`；
4. 以上均不存在。

结果：`ready | legacy_migration_required | project_missing | prerequisite_missing | prerequisite_invalid | prerequisite_stale | version_conflict`。

## 2. 项目缺失

S2–S7 不能创建项目根，也不能把裸文本、JSON 或单文件当作上游通过证据。

```text
status=project_missing
route_to=S1
workspace_write=none
```

只有用户明确要求从头完成整个流程时，编排器才按 S1→目标阶段逐步调用；每阶段仍独立记录 conversation、Gate 和 revision。

## 3. 旧 run

保持旧 run 只读，先运行 `scripts/migrate_legacy_run.py`，验证 migration map、SHA-256 和 `artifact_migrated` 事件，再重新检查前置。

## 4. 前置 Gate

依赖由 manifest 的 `prerequisites` 定义。检查 `state=completed`、`gate=pass`、entrypoint、Gate/verification、版本与失效关系。裸文件、口头声明或旧 envelope Schema 通过均不能替代项目 Gate。

## 5. 项目存在但前置缺失

默认不静默执行上游，也不补造结果：

```bash
python3 scripts/record_prerequisite_block.py \
  --project-dir workspace/<project-slug> \
  --stage Sx \
  --reason "<本次独立调用意图>"
```

该事务创建 conversation、`prerequisite-check.md`、blocked Gate、最早 route、revision 更新和根索引/时间线；不写正向业务记录。

用户明确要求补齐前置时，编排器退出当前阶段，按 route 调用上游；上游通过后重新调用原阶段。

## 6. 裸材料

课程目录、研究报告、图谱 JSON、学习记录或导出先保存为附件或 conversation 输入，标 `user_provided_unverified`，由所属上游验证。当前阶段不能直接升级为 Gate 事实。

## 7. 版本冲突

写入前读取 `expected_project_revision`。不一致时停止业务覆盖，记录冲突并重新加载。

## 8. blocked 与 pending

- `blocked`：前置合同不满足，当前阶段未执行；
- `pending`：前置通过，但等待本阶段真实输入，如回答、确认或延迟复测。

## 9. 用户回应

说明项目、revision、请求阶段、前置结果、最早缺失阶段、诊断 conversation、route 和恢复条件；不得只返回 JSON。
