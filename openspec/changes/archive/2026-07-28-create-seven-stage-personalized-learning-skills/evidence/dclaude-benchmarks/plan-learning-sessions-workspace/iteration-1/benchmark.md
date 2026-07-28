# Skill Benchmark: plan-learning-sessions

**Executor Models**: dclaude: deepseek-v4-pro[1m]
**Analyzer Models**: dclaude: deepseek-v4-pro[1m]
**Date**: 2026-07-26T19:40:33Z
**Evals**: 1, 2, 3 (3 runs each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 56% ± 10% | +0.44 |
| Time | 129.8s ± 58.9s | 174.7s ± 142.6s | -45.0s |
| Tokens | 76434 ± 3693 | 70685 ± 59611 | +5749 |

## Route Provenance

- Per-run route/model/canonical-output fields and actual `inputTokens+outputTokens` are embedded in `benchmark.json`.
- Detailed analysis and route limitations are recorded in `analyzer-notes.md`.


## Analyzer notes

- **Discrimination:** with-skill mean pass rate is `1.0000`; without-skill is `0.5556`; delta is `+0.44`. The skill adds consistent value, but this is the weakest separation among the six completed benchmarks because baseline answers often include plausible schedules and activities.
- **Variance:** with-skill standard deviation is `0.0000`; without-skill is `0.0962`. The remaining discriminators are mandatory confirmation, decidable per-node exits, transfer/delayed review and deterministic G5 routing.
- **Time:** with-skill mean is `129.7793s`, without-skill `174.7483s` (`-45.0s`). The structured skill was faster in this small sample.
- **Tokens:** recovered directly from each executor outer `modelUsage`, the means are `76,434.3` with the skill and `70,685.0` without it (`+5,749.3`). This replaces the earlier zero-value aggregation gap.
- **Conclusion:** retain the current skill but strengthen future evals around plan adaptation and executable exit criteria, where generic baseline plans should fail.
