---
name: check-capability-concept-graph
description: 独立复核项目级 S3/G3 的能力图、节点、边、测评、追溯、前置和项目版本；不接受旧 capability_concept_graph envelope 作为唯一输入。
---

# S3/G3 项目 Wiki 质量检查

验证 G1/G2、prerequisite-check、conversation 和项目 revision。completed 时独立检查层级/覆盖/先修分离、硬先修无环、节点唯一性、评估有效性、来源追溯和索引一致性。

blocked 时验证最早缺失 route 和业务 not_executed，不能给 G3 pass。输出 `quality_check_result` 2.0，不修改项目。
