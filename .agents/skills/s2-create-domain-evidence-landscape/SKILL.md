---
name: al-s2-create-domain-evidence-landscape
description: 在统一项目级 LLM Wiki 中执行 S2 领域取证与逐题回答。业务规则读取 `.agents/stage-profiles.json#S2`，独立调用缺前置时记录 blocked conversation 并路由最早缺失阶段；不得以旧 run、单体 JSON 或 HTML 作为主要交付。
---

# S2 领域取证与逐题回答

必须读取项目工作区合同、独立调用合同、stage runtime contract、manifest 的 S2、stage profiles 的 S2，以及当前项目根、project-state、conversation 和 `stages/s2-domain-evidence/INDEX.md`。

本目录旧三工件 Schema、HTML 合同和历史 example 仅作兼容资料，不能覆盖当前合同。

## 独立调用

- 无项目：`project_missing → S1`，不创建孤立工件。
- 旧 run：先迁移并重新加载。
- S1/G1 缺失或失效：运行 `record_prerequisite_block.py --stage S2`，只写诊断事务并 route S1。
- 用户要求补齐全流程：退出 S2，调用 S1；G1 通过后重新调用 S2。
- revision 冲突：不覆盖。

## 正常执行

按照 `stage-profiles.json#S2` 执行真实联网、多视角、多轮六源研究，更新研究日志、来源、覆盖、证据项、逐题回答、八维校验、刷新策略、G2、verification 和项目 revision。

只有业务量规、conversation、版本、稳定 ID、索引和 verification 全部通过，才能 `G2=pass → S3`。无联网、关键答案 partial/unanswered 或证据边界不清时保持 S2。
