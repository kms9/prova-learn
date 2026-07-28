# 七阶段 HTML 可视化实施验收报告

> 日期：2026-07-27  
> Change：`add-seven-stage-html-visualizations`  
> 结论：自动化范围内通过

## 1. 实施范围

- 七个 Skill 的共同移交信封升级到 `1.1.0`。
- 新增必填 `presentation_artifact` 及 `generated / failed / not_requested` 条件约束。
- 七个 Skill 均新增自包含 `assets/stage-report.html`。
- 七个 Skill 均新增 `references/html-visualization-contract.md`。
- 七个 `SKILL.md` 和七个阶段案例均已同步 HTML 派生、非权威性、阻断和草稿边界。
- S1—S7 具有不同的核心视图，共享标签、筛选、详情、证据、质量、原始 JSON 与草稿外壳。

## 2. 结构与契约验证

- `openspec validate add-seven-stage-html-visualizations --strict`：通过。
- 所有受影响 JSON 文件：`jq empty` 通过。
- 共同信封 Draft 2020-12 + `FormatChecker`：
  - 合法变体：12/12 通过。
  - 故意错误变体：4/4 被拒绝。
  - 覆盖 S1—S7、`needs_confirmation`、`blocked`、`generated`、`failed`、`not_requested`。
- 最终 HTML 证据报告：8/8 可解析，嵌入信封均通过共同 Schema，元数据路径与实际文件一致。
- 七个 Skill 的 `quick_validate.py`：7/7 通过。

共同文件 SHA-256：

| 文件 | SHA-256 |
|---|---|
| `assets/stage-report.html` | `864663e02bfd3a363e74d4bd918ae60487141d01837a7ffa4a47e42485040902` |
| `references/handoff-envelope.schema.json` | `84c95ab79d3bf49ad6b22210be91d6a4e85d01f30c0844a3fd954c8ef026929b` |
| `references/html-visualization-contract.md` | `bf0e7453b9e12d8259d9fd85d0b3e6376d9737d973842badf68fb7253e107429` |

每类文件的七份副本字节一致。

## 3. 静态安全与 HTML 验证

- HTML 结构、五个 ARIA 标签和五个面板：通过。
- 页面 JavaScript `node --check`：通过。
- 危险汇点扫描：未发现 HTML 字符串注入、文档写入或动态代码执行路径。
- 网络能力扫描：未发现请求 API、远程脚本、远程样式、远程字体、`@import` 或远程 CSS URL。
- 页面包含 CSP、本地文件显式选择、`aria-live`、键盘焦点、响应式、打印和减少动态效果样式。
- S3 关系图具有邻接表等价视图；状态不只依赖颜色。

## 4. 浏览器交互验证

内置浏览器连接不可用，可用浏览器列表为空；因此使用独立临时配置的本机无头
`Chrome/150.0.7871.182` 通过 DevTools Protocol 验收最终文件，并在完成后停止该临时浏览器。

结果：

- S1—S7 专属视图路由：7/7 通过。
- S5 `needs_confirmation`：通过。
- S7 `blocked` 且 `positive_artifact=null`：诊断页面通过。
- ARIA 标签键盘右方向键切换：通过，活动标签和面板均为“阶段详情”。
- S3 搜索与筛选：`6 / 13` 命中，清除后恢复 `13 / 13`。
- 按需详情：选中 `node-cardinality` 后显示完整字段。
- 无效本地文件：显示恢复性错误，已装载 S3 保持不变。
- 有效本地文件：重新装载 S3 成功。
- 草稿下载：`authority=unsubmitted_user_draft`，
  `action_type=graph_review_draft`，未复制完整源信封。
- 320 CSS px：
  - `window.innerWidth=320`
  - 页面根 `pageHorizontalOverflow=false`
  - S3 图谱局部 `graphOverflow=true`
- 浏览器运行异常：0。
- 总结果：`overall_pass=true`。

证据：

- `browser-smoke-results.json` SHA-256：
  `d8ae40309676801e445f5e41b83119f70c914407821864a2a17cbbb030407987`
- `s3-browser.png` SHA-256：
  `30b2971fb8905cddfda04f02cce3f20b0a565c3984098fe9c07ce537d9e73e8a`
- `s3-browser-320.png` SHA-256：
  `e4db63fa2aa6fd411a8b29e4c02afc20c10c0ab014220e11d482bef161d65a04`

## 5. 错误收口

本 change 新记录并解决：

- ERR-092：Node 24 模块格式歧义。
- ERR-093：S3 图谱穿透局部容器造成根页面横向溢出。
- ERR-094：验收器把滚动条后的内容宽误当完整 320 px 视口。

三项均为 `RESOLVED`，未通过放宽业务或无障碍条件来关闭。

## 6. 未运行门禁

以下未运行，不纳入“已通过”声明：

- 真实屏幕阅读器、放大器、语音控制等辅助技术人工验收。
- Safari、Firefox、Edge 的跨浏览器人工验收。
- 数百或数千节点的大型 S3 图谱性能基准。
- 真实学习者、真实研究账户或真实生产工件的端到端生成。
- 线上托管、生产环境、预发布环境和遥测验证；这些均不在本 change 范围。

自动化结果不能替代上述门禁。
