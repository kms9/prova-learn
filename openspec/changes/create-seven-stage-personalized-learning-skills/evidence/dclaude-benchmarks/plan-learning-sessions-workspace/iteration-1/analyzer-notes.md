# Analyzer notes — plan-learning-sessions

- **Discrimination:** with-skill mean pass rate is `1.0000`; without-skill is `0.5556`; delta is `+0.44`. The skill adds consistent value, but this is the weakest separation among the six completed benchmarks because baseline answers often include plausible schedules and activities.
- **Variance:** with-skill standard deviation is `0.0000`; without-skill is `0.0962`. The remaining discriminators are mandatory confirmation, decidable per-node exits, transfer/delayed review and deterministic G5 routing.
- **Time:** with-skill mean is `129.7793s`, without-skill `174.7483s` (`-45.0s`). The structured skill was faster in this small sample.
- **Tokens:** recovered directly from each executor outer `modelUsage`, the means are `76,434.3` with the skill and `70,685.0` without it (`+5,749.3`). This replaces the earlier zero-value aggregation gap.
- **Conclusion:** retain the current skill but strengthen future evals around plan adaptation and executable exit criteria, where generic baseline plans should fail.
