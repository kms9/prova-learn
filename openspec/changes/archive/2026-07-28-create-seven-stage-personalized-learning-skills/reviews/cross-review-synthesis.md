# OpenSpec Explore 交叉评审综合结论

## 路由证据

| 路由 | 退出状态 | 实际模型证据 | 评审结论 |
|---|---:|---|---|
| `dclaude` | 0 | `modelUsage.deepseek-v4-pro[1m]` | `pass_with_changes`，置信度 0.72 |
| `gclaude` | 0 | 主要为 `modelUsage.glm-5.2`，少量 `glm-5.1` | `pass_with_changes`，置信度 0.83 |

结构化结果见：

- `reviews/dclaude-review.json`
- `reviews/gclaude-review.json`

## 双方一致且已接受

1. 顶层必须保持恰好七个阶段 skill；S7 在一个 skill 内顺序执行掌握验证与版本化模型更新/重规划。
2. 补齐快速档 S2+S3、S4+S5 合并的允许/禁止条件，且合并执行不能删除任何工件或质量门。
3. 将量规条目操作化为“维度—证据—分数—阈值—通过—失败动作—路由”。
4. 显式区分 `model_hypothesis`、`market_signal`、`external_evidence` 等证据来源。
5. 为所有阶段规定缺输入、空证据、过期输入和无法确认时的安全行为。
6. 把两个贯穿案例的集成审计具体化为 S1→S7 全链路，并包含 S7→S5→S6→S7 补救循环。
7. `quick_validate.py` 只证明 skill 结构/frontmatter，不等于 Schema、行为或 eval 通过。
8. S7 补齐 `load(as_of)`、不可变 `append_evidence`、版本化 `update` 和 `history` 审计协议。
9. 研究级运行未执行外部专家复核或纵向延迟复测时必须保持 pending/not-executed。

## 单方意见的处理

- 接受 `dclaude` 的 S3 双图建议：`canonical_knowledge_concept_map` 作为可选且受追溯约束的输出，不替代 `capability_concept_graph`。
- 接受 `gclaude` 的 S2 默认样本阈值建议：适用时招聘样本默认不少于 3 个岗位、2 个组织，面试/选拔不少于 2 组独立样本；不足时形成 gap 并按影响降级或阻塞。
- 保留每个 skill 的 `references/example.md`。它用于说明工件契约，不作为 eval executor 输入；任务清单增加完整性检查。

## 未采纳或调整

- 未新建 repo-local validator 脚本。原因：用户偏好在新脚本前先确认；当前可用 `quick_validate.py`、Python `json`/`jsonschema`、SHA-256 和直接引用/占位符检查完成确定性验证。
- 不把 per-case 结果写入 skill 自身的 `evals/results/`。实际安装的 Claude Skill Creator 规定运行结果位于 skill 相邻 workspace：`iteration-N/<eval-name>/{with_skill,without_skill}`，而 skill 内只保留 `evals/evals.json`。
- 不要求把真实联网结果冻结为 S1/S2 eval 的唯一答案；此类 eval 评价研究执行、证据分类、覆盖/缺口与阻塞诚实性，避免随时间漂移和答案泄漏。

## Apply 前结论

交叉评审提出的实施阻塞项已转成 design/spec/task 的可测试要求。只有 OpenSpec strict validation 与工件哈希基线通过后才进入 `openspec-apply-change`。
