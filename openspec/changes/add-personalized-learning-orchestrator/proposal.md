## Why

用户目前必须理解并分别选择 S1–S7 Skill，才能启动、继续或返工个性化学习流程；这把内部阶段划分暴露成了使用前置。仓库需要一个单一入口，把自然语言意图、项目状态和 Gate 路由编译成正确的阶段调用，并在每次调用后明确告诉用户下一步需要做什么。

## What Changes

- 新增 repo-local 主控 Skill `al-orchestrate-personalized-learning`，作为 S1–S7 之上的入口与控制面，而不是第八个业务阶段。
- 定义意图到阶段的确定性路由、项目状态恢复、显式单阶段调用与“补齐全流程”两种推进策略。
- 在委托阶段前校验项目、revision、前置 Gate 和真实输入边界；阶段完成后重新读取落盘状态与 `route_to`，不以模型自述代替证据。
- 定义统一的用户回执，展示已理解意图、实际执行阶段、Gate/阻断状态、下一动作、所需用户输入和可继续调用的提示。
- 增加正向、返工和阻断 eval，并更新仓库导航，使用户只需显式调用主控 Skill。

## Capabilities

### New Capabilities

- `personalized-learning-orchestration`: 覆盖自然语言意图分发、S1–S7 阶段委托、Gate 驱动续跑、停顿条件、证据核验与下一步提示。

### Modified Capabilities

无。

## Impact

- 新增 `.agents/skills/al-orchestrate-personalized-learning/` Skill 包及 eval。
- 更新 `.agents/AGENTS.md` 和根 `AGENTS.md` 的入口与阶段导航。
- 不新增运行时服务或脚本，不改变 S1–S7 的业务合同、Gate 所有权、项目工作区 Schema 或已有工件格式。
