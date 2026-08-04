# S2–S7 项目 Wiki 迁移与独立调用恢复规则

S2–S7 统一按“前置检查→conversation→阶段 Wiki/JSONL→Gate/verification→revision→索引”执行，旧 JSON/HTML 仅兼容导出。

## 独立调用

```text
无项目 → S1，不写孤立阶段
旧 run → 迁移
项目存在 → 检查 prerequisites
  pass → 当前阶段
  missing/invalid/stale → blocked conversation，route 最早缺失阶段
revision conflict → 不覆盖
```

默认不自动执行上游；用户明确要求补齐全流程时，编排器按 route 逐阶段调用。

## 直接前置

| 阶段 | 直接前置 |
|---|---|
| S2 | S1/G1 |
| S3 | S1/G1、S2/G2 |
| S4 | S1/G1、S3/G3 |
| S5 | S1/G1、S3/G3、S4/G4 |
| S6 | S2/G2、S3/G3、S4/G4、S5/G5 |
| S7 | S3/G3、S4/G4、S5/G5、S6/G6 |

阻断脚本递归检查传递依赖，因此全新项目独立调用 S6/S7 仍 route S1。

## blocked 与 pending

blocked=前置不满足、业务未执行；pending=前置已通过但等待真实回答、确认或延迟复测。

## 阻断事务

`record_prerequisite_block.py` 写 conversation、前置表、诊断页、blocked Gate、最早 route、revision 和索引同步，专属业务 JSONL 为空。

## 阶段交付

S2：研究回答/验证/刷新 + 来源/证据项。  
S3：能力图/学习单元/追溯 + nodes/edges/assessments。  
S4：诊断计划/快照/误概念/复测 + observations/model events。  
S5：路径/策略政策/会话/复习 + schedule。  
S6：session 导航/内容决策 + 真实交互/候选证据。  
S7：掌握证据/归因/重规划/route + mastery/model updates。

Checker 识别 completed、pending、blocked，使用 `quality_check_result` 2.0 的 project_ref 与 prerequisite_check。
