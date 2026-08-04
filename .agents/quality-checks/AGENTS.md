# 质量检查共同规则

本文件适用于 `.agents/quality-checks/` 下所有独立 Gate Checker，并在冲突处覆盖各 Checker 历史 `SKILL.md` 中对单体 JSON envelope 的依赖。

## 1. 统一输入

所有 Checker 必须从同一个项目工作区读取：

```text
workspace/<project-slug>/
  INDEX.md
  project-state.json
  conversations/...
  stages/<stage-dir>/...
```

阶段目录、共同文件和专属文件以 `.agents/stage-delivery-manifest.json` 为准。

## 2. 旧 envelope 的地位

- S3–S7 的历史 JSON envelope 仅是兼容导出。
- Checker 可以用对应 Schema 校验兼容导出，但不得把它当作完整阶段输入。
- 缺少项目根、conversation、阶段 Wiki、事件日志或项目状态时，即使 JSON envelope 合法也不得通过 Gate。

## 3. 每个 Gate 的共同结构检查

在业务量规之前，Checker 必须独立验证：

1. 项目根必需文件和目录存在；
2. `project-state.json` 可解析且 revision 与当前阶段页面一致；
3. 产生当前阶段版本的 conversation 四文件齐全；
4. conversation `events.jsonl` 合法、不可变、事件 ID 唯一；
5. 阶段共同文件和专属文件齐全；
6. 稳定 ID、页面链接和事件引用可解析；
7. 被替代页面有 `history/` 或 `supersedes` 追溯；
8. 项目根 `INDEX.md`、阶段 `INDEX.md`、Gate 和 route 一致；
9. 没有用工作笔记、模型假设或自报 verdict 代替可审计证据。

## 4. 只读独立性

Checker 只读、只判：

- 不修改项目 Wiki；
- 不补写 conversation；
- 不替阶段 Skill 创建缺失事件；
- 不根据被检 Gate 自报结论直接放行；
- 不通过静默修复引用或删除失败历史来凑 pass。

## 5. 输出

`quality_check_result` JSON 仍是 Checker 的机器输出，因为它是单次审计裁决，不是学习项目本体。该 JSON 必须引用被检查的项目 revision、conversation、阶段页面和证据 ID。
