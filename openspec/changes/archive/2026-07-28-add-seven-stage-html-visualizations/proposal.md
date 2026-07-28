## Why

七阶段 Skill 的规范 JSON 已适合机器校验和阶段移交，但缺少面向学习者、教学设计者与审查者的可离线可视化界面，导致关系、证据、门禁和路由难以快速理解。现在需要在不削弱 JSON 真值源和阶段门禁的前提下，为 S1—S7 增加可复验的 HTML 派生视图与受约束的交互草稿能力。

## What Changes

- 为每个阶段 Skill 增加可独立复制、无远程依赖的单文件 HTML 模板。
- 为 S1—S7 定义阶段专属的总览、关系视图、筛选、详情与草稿导出行为。
- 将共同移交信封从 `1.0.0` 升级为 `1.1.0`，新增必填 `presentation_artifact`，记录 HTML 的派生权威性、路径、来源和真实验证状态。
- 规定 JSON 是唯一权威工件，HTML 不得反写 JSON，本地交互只有经相应 Skill 重新处理后才可成为规范确认、计划或学习证据。
- 规定成功、待确认和阻断结果均可生成 HTML；HTML 失败不得篡改阶段业务门禁，但在明确请求 HTML 时必须作为未完成项报告。
- 增加离线、本地文件装载、DOM 注入防护、无障碍、响应式、打印和浏览器交互验收要求。
- 不引入前端框架、CDN、远程 API 或独立生成脚本。

## Capabilities

### New Capabilities

- `stage-html-visualizations`: 定义七阶段 JSON 移交信封到非权威单文件 HTML 的派生契约、阶段专属视图、交互草稿边界、安全、无障碍与验收行为。

### Modified Capabilities

无。当前 `openspec/specs/` 中没有已归档的七阶段基线能力；现有完成 change 的历史规格不作为本 change 的 delta 目标。

## Impact

- 影响 `.agents/skills/` 下七个个性化学习 Skill 的 `SKILL.md`、共同移交信封 Schema、引用文档和静态资产。
- 新增 `assets/stage-report.html` 与 `references/html-visualization-contract.md`，七个 Skill 各自携带字节一致的副本。
- 调用方在消费 `1.1.0` 移交信封时需要识别 `presentation_artifact`；旧 `1.0.0` 工件继续可被显式识别为旧版本，但不能作为 `1.1.0` 校验通过。
- 不增加运行时网络依赖、生产服务、托管站点或业务数据库。
