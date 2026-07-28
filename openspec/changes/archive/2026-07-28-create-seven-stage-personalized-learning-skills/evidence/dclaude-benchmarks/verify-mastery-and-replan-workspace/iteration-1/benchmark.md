# Skill Benchmark: verify-mastery-and-replan

**Executor Models**: dclaude: deepseek-v4-pro[1m]
**Analyzer Models**: dclaude+gclaude: deepseek-v4-pro[1m], glm-5.1, glm-5.2
**Date**: 2026-07-26T19:40:33Z
**Evals**: 1, 2, 3 (3 runs each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 44% ± 35% | +0.56 |
| Time | 105.4s ± 43.7s | 48.7s ± 28.7s | +56.7s |
| Tokens | 81199 ± 3116 | 32824 ± 1971 | +48375 |

## Route Provenance

- Per-run route/model/canonical-output fields and actual `inputTokens+outputTokens` are embedded in `benchmark.json`.
- Detailed analysis and route limitations are recorded in `analyzer-notes.md`.


## Analyzer notes

- **Discrimination:** after correcting the grader-identified contradictory attribution assertion and adjudicating the cross-route baseline disagreement, with-skill mean pass rate is `1.0000`; without-skill is `0.4444`; delta is `+0.56`.
- **Variance:** with-skill standard deviation is `0.0000`; without-skill is `0.3469`. Baseline answers sometimes notice insufficient evidence or version mismatch, but do not implement the ordered verification/update bundle, event-sourced patch or complete route protocol.
- **Time:** with-skill mean is `105.4320s`, without-skill `48.6897s` (`+56.7s`).
- **Tokens:** actual outer `modelUsage` totals average `81,199.3` with the skill and `32,824.3` without it (`+48,375`). The ordered verification/update bundle, history and routing protocol have a material token cost.
- **Contract repair provenance:** the original dclaude grader gave expectation 5 a failure while explicitly reporting that “path before evidence” made the assertion internally contradictory. The pre-fix grading is retained as `grading.before-eval-contract-fix.json`; the canonical grading changes only the exact assertion text, its supported verdict and reconciled summary.
- **Cross-route adjudication:** for eval-2 without-skill, gclaude correctly observed that expectation 2 asks for evidence-type plurality, not six-dimensional field names. F1–F4 satisfy the literal semantic assertion, so canonical grading records 2/6; the original dclaude judgment is retained as `grading.before-cross-route-adjudication.json`.
- **Conclusion:** good discrimination, with future efficiency work focused on compact event-history output rather than removing the version/attribution safeguards.
