# `workspace/` 运行规则

本文件适用于全部项目级学习工作区。

## 1. 项目是长期容器

`workspace/<project-slug>/` 代表一个长期学习项目，不代表一次模型运行。不得为每个阶段、每次提示或每次重试创建新的项目目录。

## 2. 入口和读取顺序

任何写入前依次读取：

1. `INDEX.md`
2. `PROJECT.md`
3. `project-state.json`
4. 当前阶段 `INDEX.md`
5. 最近 conversation 的 `summary.md`
6. 本次任务实际需要的 Wiki 页面和 JSONL 记录

不要默认把整个项目全部装入上下文；由根索引和阶段索引按需加载。

## 3. 追加与覆盖边界

只能追加：

- `conversations/**/transcript.md`
- `conversations/**/events.jsonl`
- 阶段 `records.jsonl`
- 学习者观察、教学事件、掌握证据和模型事件 JSONL
- `timeline.md` 的新时间线项目

可以更新但必须留历史：

- `INDEX.md`
- `PROJECT.md`
- 阶段当前 Wiki 页面
- `project-state.json`
- 当前计划和学习者快照

当前页面被实质替换时，将旧版本写入对应 `history/`，并在新页面注明 `supersedes` 与事件引用。

## 4. 写入事务

写入开始时记录 `expected_project_revision`。结束时只有在当前 revision 未变化时才能提交新快照，并把 revision 加一。冲突时停止更新当前页面，保留本次 conversation 和冲突事件，等待重新加载。

## 5. 隐私与原文

- 学习者原始回答属于证据，不得为了美化而改写。
- 需要脱敏时保留占位 ID 和脱敏说明，不静默删除上下文。
- Agent 推断、外部事实、用户自述和学习者行为必须保持不同 provenance。

## 6. 禁止事项

- 不用单个 JSON 文件取代项目 Wiki。
- 不把 `working-notes.md` 当作已确认结论。
- 不删除失败会话、被否决路径或 Gate 未通过历史。
- 不把旧 run 与新阶段目录混写而没有迁移记录。
- 不在 revision 冲突时强制覆盖。
