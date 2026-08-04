# `.agents` 运行规则：项目级 LLM Wiki

统一入口为 `$al-orchestrate-personalized-learning`；用户也可以直接调用 S1–S7。主控是薄控制面，不是 S0/G0 或第八阶段，不拥有业务工件和 Gate。

执行主控或 S1–S7 前读取项目工作区合同、manifest、独立调用合同、项目根、project-state、当前 conversation 与 stage profile。

- 只有 S1 可创建项目根。
- S2–S7 无项目时 route S1，不写孤立阶段。
- 旧 run 先迁移；项目存在但前置缺失时写 blocked conversation 和 `prerequisite-check.md`，route 最早缺失阶段。
- 用户明确要求补齐全流程时，编排器按 route 逐阶段调用；当前 Skill 不得补造上游。
- 主控默认一次只委托一个阶段；只有用户明确要求完整流程时才连续推进，并在确认、真实学习者输入、blocked/pending、版本冲突或上游返工 route 处停止。
- 主控委托后必须重读 project-state、conversation、Gate 与 verification；用户可见的下一步仍指向主控，不要求用户记忆子 Skill 名。
- S2–S7 旧 Markdown→JSON→HTML 三工件规则已废止为主要交付；JSON/HTML 仅兼容导出。
- 每次实质交互、工具结果、Gate、route、学习行为、迁移或冲突都必须进入 conversation。
- Wiki 是当前意义，JSONL 是不可变历史，project-state 是版本快照。
- 写入前校验 revision；冲突不覆盖。
- blocked 表示前置失败且业务未执行；pending 表示前置通过但等待本阶段真实输入。
- 完成要求前置 pass、业务 Gate、conversation、文件、ID、verification、project-state、INDEX 和 timeline 一致。
- Checker 只读、只判，同时检查业务与项目一致性。
