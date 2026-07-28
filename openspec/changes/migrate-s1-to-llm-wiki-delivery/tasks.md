# Tasks — migrate-s1-to-llm-wiki-delivery

## S1 skill 改写

- [x] 新增 `s1/references/run-folder-contract.md`（11 文件逐文件字段契约、稳定 ID、状态机 guard、反占位、跨文件互引校验）
- [x] 删除 `s1/references/markdown-output-contract.md`、`s1/references/html-visualization-contract.md`、`s1/assets/stage-report.html`（并移除空 `assets/`）
- [x] 重写 `s1/references/stage-contract.md`：§0 分叉为 S1 run-folder / S2–S7 三工件；§5 字段→文件映射；§6 量规证据→文件；保留 §1–§4/§7/§8
- [x] 重写 `s1/SKILL.md`：状态机 + guard + run folder 布局 + 产物/字段契约 + 硬性规则 + Fail closed
- [x] 重写 `s1/references/example.md`：run folder 文件摘录替代 JSON 信封
- [x] 重写 `s1/evals/evals.json`：3 case 期望值改为 run-folder 校验
- [x] 重写 `s1/agents/openai.yaml`：`default_prompt` 改为 run-folder 指令
- [x] 保留不动 `s1/references/handoff-envelope.schema.json`（S2–S7 共享）与 `goal-success-contract.schema.json`（字段参考）

## 下游输入契约

- [x] `s2/references/stage-contract.md` §2：输入改为 S1 run folder 入口 + 字段→文件映射 + run-folder 七项校验
- [x] `s2/SKILL.md`：上游消费语改为读 run folder `INDEX.md`
- [x] `s3` / `s4` / `s5` 各自 `stage-contract.md` §2 加防御性 run-folder 说明

## 仓库级文档

- [x] `AGENTS.md` §4.2：加 S1 迁移说明
- [x] `AGENTS.md` §5：S1 行具名正向工件 → run folder 入口
- [x] `AGENTS.md` §7：产物合同分 S1 run-folder / S2–S7 三工件
- [x] `AGENTS.md` §13.1：新增 S1 run-folder 标准结构

## OpenSpec

- [x] 开本 change（proposal + tasks），记范围与对 `add-seven-stage-html-visualizations` 的 S1 切片取代

## 验证（待跑）

- [x] 静态扫描：S1 内无残留必产出单体 JSON/HTML 义务（schema 文件作参考保留）
- [x] 跨文件 ID/链接解析校验（用真实 run folder 样本）
- [ ] S1 `evals.json` 跑通：待 `run_skill_evals.py` 扩展为可评分 run folder 目录（后续追踪）
  - `evals.json` 本身合规且与 run-folder 契约一致（见 `evidence/evals-blocked.md`）；实际跑通被 `scripts/run_skill_evals.py` 的单体 JSON 执行器指令 + 纯文本 grader 阻塞，解锁条件 = task 22。
- [x] S1→S2 冒烟：S2 按 `INDEX.md` 读取并取出 `research-brief.md` / `sources.jsonl` / `coverage.md`

## 后续追踪（不在本 change 范围）

- [ ] S2–S7 各自迁移到 run-folder 产出
- [ ] `scripts/run_skill_evals.py` 支持目录型产物评分
- [ ] `AGENTS.md` §3 仓库地图 / §12.4 检查表对旧模型的美观性引用
- [ ] `example/初中资深教研老师/` 旧 `-S1-handoff.json` / `-S1-report.html` 加迁移前注明
