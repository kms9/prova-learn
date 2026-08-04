---
name: check-domain-evidence-landscape
description: 独立复核项目级 S2/G2，读取项目状态、S2 Wiki/JSONL、conversation、prerequisite-check、Gate 与 verification；不接受旧 domain_evidence_landscape envelope 作为唯一输入。
---

# S2/G2 项目 Wiki 质量检查

先验证 S1/G1 和 `prerequisite-check.md`。completed 时独立复核真实联网、多视角、多轮六源、逐题映射、来源独立性、八维校验、饱和、刷新策略、revision 与索引。

blocked 时只验证前置失败、最早 route、conversation、revision 和无伪正向业务记录，不能给 G2 pass。pending 与 blocked 分开。

输出 `quality_check_result` 2.0，只读、只判。
