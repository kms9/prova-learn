# S2–S7 项目 Wiki 通用运行合同

> 阶段差异由 `.agents/stage-profiles.json` 定义；目录与前置由 manifest 定义。

## 权威顺序

读取项目工作区合同、独立调用合同、本合同、manifest、stage profiles、项目根和当前 conversation。各 Skill 目录旧三工件 Schema、HTML 模板和历史 example 仅为兼容资料，不得作为当前主要交付规则。

## 独立调用

```text
定位项目
├─ 无项目 → route S1，不写孤立阶段
├─ 旧 run → migrate_legacy_run.py → 重新加载
└─ 项目存在
   ├─ 前置失败 → record_prerequisite_block.py
   ├─ revision 冲突 → 不覆盖
   └─ ready → 执行业务事务
```

默认不自动运行上游。用户明确要求补齐完整流程时，编排器按 route 逐阶段调用。

## 前置检查

递归检查 manifest prerequisites 的 state、gate、entrypoint、verification、版本和失效关系。每次正常或阻断调用都写 `prerequisite-check.md`。

## 正常事务

```text
读取 expected_project_revision
→ 创建 conversation
→ 写原文、工具结果与 events
→ 更新阶段 Wiki/JSONL
→ Gate 与 verification
→ project revision +1
→ 同步根/阶段 INDEX、timeline、project-state
```

当前页实质变化前进入 `history/`，JSONL 只追加。

## 阻断事务

`record_prerequisite_block.py` 输出 blocked conversation、前置表、诊断页和最早 route；专属业务 JSONL 为空，不能消费为正向结果。

## pending

前置已通过但等待真实输入时保持 pending：S4 等待回答，S5 等待 mandatory 确认，S6 等待真实交互，S7 等待补测或延迟保持。

## 完成

前置、业务量规、conversation、阶段文件、稳定 ID、版本、verification、project-state 和索引全部通过才完成。JSON/HTML 仅可派生导出。
