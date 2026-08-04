# 质量检查层：项目 Wiki 与独立调用规则

Checker 以项目根、project-state、阶段 entrypoint、conversation、Wiki 与 JSONL 为输入；旧 envelope 只能补充。

先检查 manifest prerequisites：正常阶段的 `prerequisite-check.md` 必须 pass；blocked 阶段验证失败项、最早 route、conversation、revision 和空正向 JSONL；无项目时 route S1。

独立重判业务量规、前置、conversation、稳定 ID、JSONL、版本、索引、Gate 和 verification，不采信自报 verdict。

- blocked：不要求完整正向业务记录，但不能给 Gate pass；
- pending：前置通过，检查等待条件和未模拟输入；
- completed：业务与项目质量都通过。

输出 `quality_check_result` 2.0 小型 JSON；它是检查结果，不是业务真相。Checker 不修改项目。
