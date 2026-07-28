# Skill Benchmark: diagnose-learner-frontier

**Executor Models**: dclaude: deepseek-v4-pro[1m]; gclaude: glm-5.1, glm-5.2
**Analyzer Models**: gclaude: glm-5.1, glm-5.2
**Date**: 2026-07-26T19:40:33Z
**Evals**: 1, 2, 3 (3 runs each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 44% ± 51% | +0.56 |
| Time | 150.7s ± 65.8s | 65.8s ± 33.7s | +84.9s |
| Tokens | 66935 ± 11495 | 43517 ± 22023 | +23418 |

## Route Provenance

- Per-run route/model/canonical-output fields and actual `inputTokens+outputTokens` are embedded in `benchmark.json`.
- Detailed analysis and route limitations are recorded in `analyzer-notes.md`.


## Analyzer notes

- **Discrimination:** after correcting two fixture-contract defects and rerunning the affected configurations, with-skill mean pass rate is `1.0000`; without-skill is `0.4444`; delta is `+0.56`.
- **Variance:** with-skill standard deviation is `0.0000`; without-skill is `0.5092`. The negative fail-closed case is deliberately easy for a capable baseline and scores 6/6, while the two positive cases retain structural and evidence-traceability discrimination.
- **Time:** with-skill mean is `150.6577s`, without-skill `65.7723s` (`+84.9s`).
- **Tokens:** canonical-route outer `modelUsage` totals average `66,935.3` with the skill and `43,517.0` without it (`+23,418.3`); the three repaired S4 runs use their successful gclaude route totals and the other three use original dclaude totals.
- **Repair provenance:** original dclaude outputs and the first gclaude grading are retained. Current eval-2 with-skill and eval-3 with/without outputs are gclaude reruns because dclaude returned 402 after the contract fixes; route metadata records actual `modelUsage`. The first eval-2 rerun failed with a connection close and created no file; the successful retry passed both handoff and learner-snapshot schemas.
- **Semantic guard result:** the repaired eval-2 artifact has no `tested_mastered` node with medium/high/unknown hint dependence; repaired eval-3 with-skill has `positive_artifact=null`, `verdict=revise_here`, `route_to=S4`.
- **Conclusion:** current with-skill results are stable and correct. Final dclaude rerun/audit remains a separate external gate; gclaude evidence is not represented as dclaude.
