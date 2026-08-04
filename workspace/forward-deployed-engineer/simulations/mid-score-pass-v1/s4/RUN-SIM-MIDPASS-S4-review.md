# S4 学习者前沿诊断审核报告

## 1. 文档与运行信息

- run_id：`RUN-SIM-MIDPASS-S4`
- artifact_id：`LS-SIM-MIDPASS-v1`
- learner_id：`simulated-mid-pass-learner`
- fixture_type：`simulated_fixture`
- score：`76/100`
- status：`completed`
- G4 verdict：`pass`
- route_to：`S5`

本报告只描述虚拟学习者。主项目 revision 6 和真实 G4 blocked 状态不变。

## 2. 上游输入、模型版本与有效性审计

输入为主项目已通过 G1 的目标合同、已通过 G3 的 `CCG-forward-deployed-engineer-v1` 及 S4 诊断设计。图谱版本 `1.2.0`、共同信封 `1.3.0` 可读取，12 个节点和 ASM-001–ASM-012 引用可解析。虚拟学习者无历史模型，创建 fixture model version 1；有效期到 2026-09-03。

## 3. 诊断目标、范围与事前判定规则

诊断目标是定位最近可学习节点，不是证明终局掌握。事前规则：单题正确不判掌握；有独立理由且跨任务一致才可标记 `tested_mastered`；理由不完整标记 `tested_not_mastered` 或 `insufficient_evidence`；提示依赖、迁移和置信度分开记录。虚拟身份和非门控用途已显式披露。

## 4. 诊断任务与覆盖设计

D1 覆盖角色、适用性、产品回流和退出；D2 覆盖部署、安全、四层指标与扩缩决策；D3 覆盖工作流、价值、MVD、指标和停止；D4 覆盖医疗迁移、产品回流与来源审计。四题都记录答案、理由、置信度与帮助使用。

## 5. 学习者行为证据记录

`SIM-D1`–`SIM-D4` 对应 [虚拟答案](answer.md) 的四个回答，均为无提示首次作答；它们在虚拟身份内部标作 `learner_behavior`，同时由信封 `traceability.fixture_type=simulated_fixture` 限定，禁止外推为用户行为。四题得分分别为 20、19、18、19，总分 76。

## 6. 节点状态逐项判断

| Node | Status | Evidence | 结论 |
|---|---|---|---|
| N-001 | tested_mastered | SIM-D1 | 能区分 FDE、售前、咨询和客户特例维护 |
| N-002 | tested_mastered | SIM-D1,SIM-D4 | 能给采用、转型和退出的条件 |
| N-003 | tested_mastered | SIM-D3 | 能建立工作流、基线、owner 与失败成本 |
| N-004 | tested_not_mastered | SIM-D3,SIM-D4 | 停止条件方向正确，但阈值、样本和决策权不完整 |
| N-005 | tested_mastered | SIM-D2,SIM-D3 | 能定义真实边界、人工 handoff 与回滚 |
| N-006 | tested_not_mastered | SIM-D2,SIM-D4 | 能识别治理风险，跨域上下文 eval 仍不完整 |
| N-007 | tested_mastered | SIM-D2,SIM-D3 | 能区分技术、采用和业务证据，但 DAU 权重偏高 |
| N-008 | tested_not_mastered | SIM-D2,SIM-D3 | 扩张/停止逻辑部分成立，商业基线不足 |
| N-009 | tested_mastered | SIM-D1,SIM-D4 | 能要求重复现场信号后再回流 |
| N-010 | insufficient_evidence | SIM-D1 | 能说出退出方向，缺组织成本与交接细化 |
| N-011 | tested_mastered | SIM-D4 | 正确区分标准、岗位、厂商案例与 trace_only |
| N-012 | tested_not_mastered | SIM-D4 | 来源边界正确，独立组、刷新和远迁移审计不完整 |

## 7. 错误类型、提示依赖与置信度校准

N-004/N-008 的主要错误是 `partial_reasoning`：能提出方向，不能把 value owner、可观测阈值、窗口和 stop/go 动作组成可执行规则。N-006/N-012 是 `transfer_failure`。四题未用提示；置信度 70–82 与 76 分总体校准，D2 略偏高但没有以自评覆盖行为。

## 8. 最近学习前沿及候选比较

最近前沿为 `N-004`。其硬先修 `N-003` 已在 SIM-D3 中通过，且它直接制约后续 MVD、指标和商业闭环。备选 `N-006` 的硬先修 N-005 也已通过，但先修复 N-004 能先让“为何做、何时停”稳定，再进入“怎样安全上线”，路径更小。

## 9. 误概念、能力缺口与迁移表现

误概念 `USAGE_IMPLIES_VALUE`：曾把 DAU 当成较强价值代理；`STOP_RULE_CAN_STAY_VAGUE`：知道要停止条件，却未把阈值、窗口、owner 和动作写全。能力缺口集中于价值假设、上下文治理、扩缩决策和来源刷新。保险到医疗的远迁移为 `partial`。

## 10. 待复测、人工确认与恢复条件

需复测 N-004 的未见场景价值假设和停止条件；需在后续会话补测 N-006、N-008、N-012。此夹具的 S5 确认由虚拟身份完成，不代替真实用户确认。真实项目恢复条件仍是用户本人完成 D1–D4。

## 11. 证据有效期与诊断限制

虚拟证据只在本演练目录有效，有效至 2026-09-03。任何图谱语义变更都使其失效。不得用于招聘、真实能力认证、真实学习者画像或主项目质量门。

## 12. G4 质量评价与路由

测量对齐、证据充分、猜对识别、提示依赖、错误分类、偏差控制、结论可解释性和素材有效性八项均通过**夹具质量检查**。`verdict=pass`，`route_to=S5`。这表示 S4 夹具可被 S5 消费，不表示用户掌握。

## 13. 输出审计与 JSON 对应表

Markdown 是首要人审工件；[规范 JSON](learner_snapshot.json) 无损表达节点状态、前沿、误概念、缺口、迁移与证据；[HTML](learner-snapshot.html) 由最终 JSON 驱动。全部实质内容标注 `simulated_fixture`，不生成独立图片。
