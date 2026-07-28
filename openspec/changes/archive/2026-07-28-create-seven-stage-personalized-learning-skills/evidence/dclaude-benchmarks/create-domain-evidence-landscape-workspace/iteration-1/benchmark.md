# Skill Benchmark: create-domain-evidence-landscape

**Executor Models**: dclaude: deepseek-v4-flash, deepseek-v4-pro[1m]; dclaude: deepseek-v4-pro[1m]
**Analyzer Models**: dclaude: deepseek-v4-pro[1m]
**Date**: 2026-07-26T19:40:33Z
**Evals**: 1, 2, 3 (3 runs each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 22% ± 38% | +0.78 |
| Time | 320.3s ± 125.3s | 147.7s ± 121.2s | +172.6s |
| Tokens | 193617 ± 141076 | 117192 ± 130111 | +76425 |

## Route Provenance

- Per-run route/model/canonical-output fields and actual `inputTokens+outputTokens` are embedded in `benchmark.json`.
- Detailed analysis and route limitations are recorded in `analyzer-notes.md`.


## Analyzer notes

- **Discrimination:** with-skill mean pass rate is `1.0000`; without-skill is `0.2223`; delta is `+0.78`. Executed-research evidence, category coverage, claim/source linkage and G2 routing remain discriminating.
- **Variance:** with-skill standard deviation is `0.0000`; without-skill is `0.3851`. Baseline variance is high because the negative case can satisfy generic provenance cautions while still missing gap classification and fail-closed routing.
- **Time:** with-skill mean is `320.288s`, without-skill `147.667s` (`+172.6s`). Live research and source auditing are the dominant cost.
- **Tokens:** actual outer `modelUsage` totals average `193,616.7` with the skill and `117,192.0` without it (`+76,424.7`). The accuracy gain has a material token cost; a later optimization should reduce repeated source narration without weakening the manifest or ledger.
- **Conclusion:** high quality gain with the clearest cost trade-off among the completed stages.
