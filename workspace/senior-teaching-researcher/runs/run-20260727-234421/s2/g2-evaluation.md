# G2 评价 — run-20260727-234421

> verdict=`revise_here`；route_to=`S2`。原因不是没有研究，而是关键问题 ANS-002 的“跨机构精确周 SOP”缺一手内部证据，且合规业务形态触发的 mandatory confirmation 尚未完成。

| dimension | evidence | score | threshold | passed | failure action | route |
| --- | --- | ---: | ---: | --- | --- | --- |
| 输入有效 | S1 validator PASS；`../g1-evaluation.md`、`../confirmation.md`、`../verification.md` | 1.0 | 1.0 | true | — | S2 research |
| 实际联网 | research-log：43 queries、3 rounds、online completed | 1.0 | 1.0 | true | — | continue |
| 多视角与追问 | 六视角；Q-029..Q-043 对周 SOP、指标和 SEC 来源追问 | 1.0 | 1.0 | true | — | continue |
| 六源覆盖 | coverage.md 固定六行均 covered | 1.0 | 1.0 | true | — | continue |
| 来源质量 | 25 accepted；官方/年报/研究为关键锚点，独立组去重 | 0.9 | 0.8 | true | — | continue |
| 问题映射 | 5 个 S1 问题各恰好一个 RQ/ANS | 1.0 | 1.0 | true | — | continue |
| 逐题八维 | 40 行齐全；ANS-002 两个关键维度 insufficient | 0.75 | 1.0 | false | 补两个当前组织的周级内部工件或具名访谈 | S2 |
| 可追溯性 | ANS/ITEM/E/GAP/Q 稳定 ID 均由 verification 静态检查解析 | 1.0 | 1.0 | true | — | continue |
| 证据边界 | market_signal、external_evidence、社区风险和推断分离 | 1.0 | 1.0 | true | — | continue |
| 争议与缺口透明 | GAP-001..GAP-003；辅导师角色冲突、因果限制和合规边界保留 | 1.0 | 1.0 | true | — | continue |
| 饱和与成熟度 | 三轮连续补证；saturation reached；L1_landscape | 1.0 | 1.0 | true | — | continue |
| 时效治理 | 稳定/动态分类、valid_through 与 review_trigger 已写 | 1.0 | 1.0 | true | — | continue |
| 条件确认 | GAP-002 实质改变产品边界，mandatory confirmation=pending | 0.0 | 1.0 | false | 用户确认业务形态及 1–2 个目标地区 | S2 |
| 根索引与九文件 | 九文件与根索引已建立，最终完整性见 verification.md | 1.0 | 1.0 | true | — | continue |

## 裁决

- `verdict=revise_here`
- `route_to=S2`
- `g2_pass=false`
- 不返回 S1：目标“初中数学双师/O2O 教培教研”未被证伪，可在 S2 内通过确认业务形态与补机构流程证据收敛。
- 不进入 S3：ANS-002 为 critical 且存在关键维度不足；mandatory confirmation 也未完成。

## 最小恢复条件

1. 用户从“获许可义务教育学科类培训 / 学习机或数字内容 / 非学科数学素养产品”中确认目标形态，并给出 1–2 个优先地区。
2. 对至少两个当前组织补到脱敏周级 SOP、版本记录、质检表/看板，或具名负责人的可审计访谈；若确实不存在统一周制，改写问题为“机构内按课次/周期的迭代机制”并由用户确认。
3. 重跑 ANS-002 的 `source_coverage`、`reliability_authority` 和 G2 确认维度；其他 E/ITEM/ANS ID 保持稳定。
