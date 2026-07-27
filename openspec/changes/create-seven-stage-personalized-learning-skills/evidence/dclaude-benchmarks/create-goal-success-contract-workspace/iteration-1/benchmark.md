# Skill Benchmark: create-goal-success-contract

**Executor Models**: dclaude: deepseek-v4-flash, deepseek-v4-pro[1m]; dclaude: deepseek-v4-pro[1m]
**Analyzer Models**: dclaude: deepseek-v4-pro[1m]
**Date**: 2026-07-26T19:40:33Z
**Evals**: 1, 2, 3 (3 runs each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 6% ± 10% | +0.94 |
| Time | 163.0s ± 54.1s | 126.0s ± 113.6s | +37.1s |
| Tokens | 164735 ± 87028 | 69439 ± 61539 | +95296 |

## Route Provenance

- Per-run route/model/canonical-output fields and actual `inputTokens+outputTokens` are embedded in `benchmark.json`.
- Detailed analysis and route limitations are recorded in `analyzer-notes.md`.


## Analyzer notes

- **Discrimination:** with-skill mean pass rate is `1.0000`; without-skill is `0.0556`; delta is `+0.94`. The contract, research provenance, mandatory confirmation and deterministic G1 route strongly separate the configurations.
- **Variance:** with-skill standard deviation is `0.0000`; without-skill is `0.0962`. All three skill runs are stable; the small baseline variance comes from one blocked case satisfying a single generic expectation.
- **Time:** with-skill mean is `163.037s`, without-skill `125.952s` (`+37.1s`). The added time is consistent with research/contract construction rather than a faster prose answer.
- **Tokens:** actual outer `modelUsage` totals average `164,735.3` with the skill and `69,439.3` without it (`+95,296`). The prior aggregate proxy used output characters, so it understated route token use; the corrected figures show a material cost with high variance at `n=3`.
- **Conclusion:** strong, stable discrimination. Keep the blocked case because it confirms fail-closed behavior rather than only rewarding verbosity.
