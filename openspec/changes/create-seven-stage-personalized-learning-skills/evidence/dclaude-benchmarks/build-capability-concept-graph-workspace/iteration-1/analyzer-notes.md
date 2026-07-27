# Analyzer notes — build-capability-concept-graph

- **Discrimination:** with-skill mean pass rate is `1.0000`; without-skill is `0.0000`; delta is `+1.00`. Typed nodes, DAG invariants, traceability, assessment alignment and G3 routing cleanly separate the configurations.
- **Variance:** both configurations have standard deviation `0.0000`; the result is stable across PostgreSQL, fractions and blocked fixtures.
- **Time:** with-skill mean is `133.4507s`, without-skill `132.8083s` (`+0.6s`), so the quality gain has negligible observed latency cost.
- **Tokens:** actual outer `modelUsage` totals average `79,668.7` with the skill and `88,791.0` without it (`-9,122.3`). At this sample size the skill is more accurate without an observed token penalty, although baseline variance is large.
- **Conclusion:** strongest observed benefit/cost profile; preserve the graph invariants and source traceability as non-negotiable checks.
