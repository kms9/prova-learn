# HTML 可视化派生契约

本契约适用于 S1—S7。完整 Markdown 是首要人审文档，规范 JSON 是机器移交的规范表示；HTML 是每次阶段运行都必须交付的、
由最终 JSON 驱动的已填充、只读、非权威阶段结果视图。

## 1. 必须读取的资源

- `references/markdown-output-contract.md`
- `references/handoff-envelope.schema.json`
- 当前阶段正向工件 Schema
- 当前阶段自己的 `assets/stage-report.html`

## 2. 强制生成

- 每次阶段运行都必须生成 HTML，不以调用方再次提出要求为前提。
- HTML 是该阶段唯一可视化交付。所有卡片、表格、时间线、关系图和知识点视图都必须由内嵌规范 JSON
  通过页面原生 HTML/CSS/JS 动态渲染。
- 禁止调用 `imagegen`、`image_gen` 或其他制图/图像生成工具；禁止生成、引用、加载或交付独立的
  PNG、JPEG、WebP、SVG、GIF、PDF 插图、知识点图片、静态图卡或其他图片资产。
- `completed`、`needs_confirmation`、`pending` 与 `blocked` 都必须有页面。
- 有正向工件时展示工件本身；无正向工件时展示真实输入缺口、当前结论、已执行处理和恢复条件。
- 不存在“不需要页面”的成功状态。无法写入、生成失败或验证失败时使用 `failed`；阶段领域门禁保持原判定，
  但本次交付不得报告为完整完成。

## 3. 生成顺序

1. 按当前阶段的 `markdown-output-contract.md` 先完成并写出完整 Markdown 实质内容。
2. 将同一内容无损结构化为符合 `1.3.0` 共同 Schema 的 JSON；填写 `document_artifact`，每个必备一级章节都要有一条指向真实 JSON Pointer 的映射。
3. 校验 Markdown 可解析、必备章节齐全、无占位符且与 JSON 语义对应；四项均通过才把
   `document_artifact.status` 标为 `generated`。
4. 为当前阶段选择固定 `view_profile`，把自己的 `assets/stage-report.html` 复制到工件目录，建议命名
   `<run_id>-<stage_id>-report.html`。
5. 将移交信封序列化为 JSON；依次把 `<`、U+2028、U+2029 转义为 `\u003c`、`\u2028`、`\u2029`。
6. 只替换模板中 `<script id="stage-data" type="application/json">{}</script>` 的 `{}`；不得改写程序脚本或生成通用装载页面。
7. 对预填充 HTML 执行解析、无障碍冒烟、交互冒烟和阶段视图核对。
8. 仅当三项验证均为 `pass` 时，把 `presentation_artifact.status` 回填为 `generated`；否则回填为 `failed`。
9. 再次嵌入最终规范信封，核对 HTML 内嵌数据与最终 JSON 逐字段一致，并重新执行共同信封校验；
   若机械回填改变 Markdown 输出审计信息，也要同步该节但不得改变实质结论。

不得为该步骤临时新增生成脚本；优先使用现有文件操作、直接文本替换能力或调用环境已有工具。

## 4. `presentation_artifact`

共同字段：

```json
{
  "format": "html",
  "status": "generated",
  "path": "run-123-S3-report.html",
  "authority": "derived_non_authoritative",
  "source": {
    "stage_id": "S3",
    "run_id": "run-123",
    "envelope_schema_version": "1.3.0",
    "artifact_id": "ccg-123",
    "artifact_schema_version": "1.1.0"
  },
  "view_profile": "capability_graph_explorer",
  "data_binding": "embedded_canonical_envelope",
  "interaction_mode": "read_only_exploration",
  "generated_at": "2026-07-27T10:00:00Z",
  "validation": {
    "html_parse": "pass",
    "accessibility_smoke": "pass",
    "interaction_smoke": "pass"
  },
  "reason": null
}
```

- `generated`：`path`、`generated_at` 非空，`reason=null`，三项验证全部为 `pass`。
- `failed`：`path=null`、`generated_at=null`，`reason` 说明失败。
- 没有正向工件时，`source.artifact_id` 与 `source.artifact_schema_version` 为 `null`。
- `view_profile` 必须与 `stage_id` 的固定映射一致。

## 5. 页面边界

- 页面打开后直接显示内嵌的最终阶段数据；不得出现文件选择器、拖放区、粘贴 JSON 区或“装载”动作。
- 页面不联网，不加载第三方资源，不上报遥测，不反写或覆盖规范 JSON。
- 页面必须在没有任何图片文件的情况下完整表达阶段信息；用户所说的“图片”“图谱”或“可视化”默认
  指页面内由数据驱动的交互视图，不得自动扩张为独立制图任务。
- 标签切换、搜索、筛选、选择、展开、图谱聚焦和提示展开都只改变阅读视图。
- 页面不接受确认、计划修改、学习者作答、提示使用或模型更新等业务输入，不导出草稿。
- 页面不向使用者展示 Schema 版本、模板信息、Markdown/HTML 生成或验证状态、字段输出说明或“为什么输出”等内部控制信息。
- 输入 JSON 视为不可信数据；不得通过 HTML 字符串注入或动态代码执行渲染。
- 图形必须有文字、列表或表格等价表达，颜色不得成为唯一信息通道。

## 6. 阶段视图映射

| 阶段 | `view_profile` | 必须适配展示的信息 |
|---|---|---|
| S1 | `goal_contract_dashboard` | 目标场景、可观察能力、终局测评、通过规则、范围/排除项、开放问题、确认结果 |
| S2 | `evidence_landscape_workbench` | 研究轮次、类别覆盖、来源台账、主张—证据、共识、分歧、证据缺口 |
| S3 | `capability_graph_explorer` | 能力大纲、学习单元、知识点、单元—节点映射、关系图与邻接表、测评、阈值、追溯 |
| S4 | `learner_frontier_diagnostic` | 诊断任务、节点状态、学习前沿、误概念、能力缺口、迁移、行为证据、待复测项 |
| S5 | `learning_plan_board` | 有序节点及其证据层级/时效/纳入理由、会话、测评计划、复习锚点、风险、备选路线、退出标准、确认结果 |
| S6 | `instructional_session_workspace` | 当前节点、解释、正反例、活动、渐进提示、反馈、既有交互轨迹、候选证据、内容质量 |
| S7 | `mastery_replan_console` | 掌握维度、证据、归因、学习者模型差异、路由、复测或复习、适用限制 |

## 7. 最低验证

- Markdown 四项验证、共同信封和正向工件 JSON Schema 全部通过。
- HTML 能被真实解析，且只存在一个 `stage-data` 数据块；其值与最终 JSON 信封一致。
- 每个阶段显示自己的标题、信息分区和固定 `view_profile`，不得回退成七阶段共用占位内容。
- 成功、待确认、阻断与无效内嵌 JSON 都能恢复性渲染；阻断页仍显示真实缺口与恢复条件。
- 页面不存在文件选择器、通用装载文案、业务输入控件、草稿导出或内部契约说明。
- 标签键盘操作、搜索/筛选、详情展开，以及阶段适用的图谱或提示浏览通过。
- 静态扫描确认无远程依赖、网络 API、危险 HTML 汇点或动态代码执行。
- 静态扫描确认无 `<img>`、`<picture>`、图片文件引用或 CSS 图片 URL；阶段工件目录不包含由本次运行
  生成的独立图片资产。
- 未运行的屏幕阅读器、真实账户、生产环境或大规模性能门禁必须显式报告。
