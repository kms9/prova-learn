---
name: check-goal-success-contract
description: 独立复核项目级 LLM Wiki 中 S1/G1 的目标契约、conversation、外部预检、确认、项目 revision 与路由。只读、只判，不接受旧 run 或单体 JSON 作为唯一输入。
---

# S1/G1 项目 Wiki 质量检查

读取项目根、`stages/s1-goal-contract/`、最近 conversation、project-state 和 canonical `quality-check_result` 2.0。

独立检查目标/能力/验收一致性、accepted external evidence、六类覆盖、mandatory 确认、稳定 ID、JSONL、历史、revision、Gate、verification、根/阶段 INDEX 和 timeline。G1 pass 时必须 route S2；pending/blocked 时保持 S1。

输出小型检查结果，`prerequisite_check.status=not_applicable`。不得修改项目。
