---
name: check-learner-frontier
description: 独立复核项目级 S4/G4 的真实观察、学习者快照、模型事件、误概念、复测、前置和版本；不接受旧 learner_snapshot envelope 作为唯一输入。
---

# S4/G4 项目 Wiki 质量检查

验证 G1/G3、prerequisite-check 和 conversation。completed 时独立检查真实行为、多项证据、提示依赖、置信度、迁移、时效、前沿和模型版本。

前置失败是 blocked；前置通过但等待回答是 pending。Checker 不得要求 pending 模拟回答，也不能把 blocked 判 G4 pass。输出 `quality_check_result` 2.0。
