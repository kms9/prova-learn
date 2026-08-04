## 1. 主控 Skill 包

- [x] 1.1 使用 Skill Creator 初始化 `al-orchestrate-personalized-learning` repo-local Skill 包与界面元数据
- [x] 1.2 编写薄控制面 `SKILL.md`，实现项目解析、意图分类、阶段委托、停顿条件和落盘复核
- [x] 1.3 编写路由参考，固化 S1–S7 语义映射、选择优先级、推进模式与下一步回执合同

## 2. 评测与导航

- [x] 2.1 增加自然语言起步、继续当前 route、目标变更、前置阻断和真实输入停顿 eval
- [x] 2.2 更新 `.agents/AGENTS.md` 与根 `AGENTS.md`，把主控声明为统一入口而非第八阶段

## 3. 验证

- [x] 3.1 运行 Skill 结构校验、eval JSON 解析和定向静态语义检查
- [x] 3.2 运行 OpenSpec strict validation、`git diff --check` 并核对没有改动用户已有的 workspace 删除
