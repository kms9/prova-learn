## 1. S2 输出合同迁移

- [x] 1.1 新增 S2 `references/run-folder-contract.md`，定义 `s2/` 九文件、稳定 ID、状态机、八维答案校验和 G2 九项机读条件
- [x] 1.2 重写 S2 `SKILL.md`，改为读取 S1 LLM Wiki、逐题回答并写入同一 run folder
- [x] 1.3 重写 S2 `references/stage-contract.md`，同步输入、确认、研究、输出、G2 与路由合同
- [x] 1.4 删除 S2 独立 Markdown→JSON→HTML 合同、两个 JSON Schema、HTML 模板及空目录

## 2. S2 执行与评估材料

- [x] 2.1 重写 S2 `references/example.md`，提供九文件 run-folder 正向与阻断夹具
- [x] 2.2 重写 S2 `evals/evals.json`，检查逐题映射、八维校验、根索引更新和 fail-closed
- [x] 2.3 更新 S2 `agents/openai.yaml` 默认提示为 LLM Wiki 阶段区输出

## 3. 下游与仓库协议

- [x] 3.1 更新 S3 `SKILL.md` 与 `references/stage-contract.md`，从根索引读取 S2 阶段区并校验 G2 九项条件
- [x] 3.2 更新 `AGENTS.md` 的三工件范围、阶段导航、产物合同、验证清单和 S2 run-folder 结构
- [x] 3.3 更新 OpenSpec 基础规格 `create-domain-evidence-landscape`、`personalized-learning-stage-contracts`、`stage-html-visualizations`

## 4. 验证

- [x] 4.1 静态扫描 S2 无现行独立 JSON 信封、HTML 页面或 Markdown→JSON 对应义务
- [x] 4.2 校验 S2/S3 Skill 结构、所有 JSON、相对链接及 `git diff --check`
- [x] 4.3 运行 `openspec validate --all --strict --no-interactive` 并记录规格、实现和未运行门的边界
- [x] 4.4 对 `workspace/senior-teaching-researcher` 执行只读 S1→S2 输入冒烟，不伪造 S2 研究结果
