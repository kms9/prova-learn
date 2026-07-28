# Analyzer notes — create-goal-success-contract

- **Discrimination:** with-skill mean pass rate is `1.0000`; without-skill is `0.0556`; delta is `+0.94`. The contract, research provenance, mandatory confirmation and deterministic G1 route strongly separate the configurations.
- **Variance:** with-skill standard deviation is `0.0000`; without-skill is `0.0962`. All three skill runs are stable; the small baseline variance comes from one blocked case satisfying a single generic expectation.
- **Time:** with-skill mean is `163.037s`, without-skill `125.952s` (`+37.1s`). The added time is consistent with research/contract construction rather than a faster prose answer.
- **Tokens:** actual outer `modelUsage` totals average `164,735.3` with the skill and `69,439.3` without it (`+95,296`). The prior aggregate proxy used output characters, so it understated route token use; the corrected figures show a material cost with high variance at `n=3`.
- **Conclusion:** strong, stable discrimination. Keep the blocked case because it confirms fail-closed behavior rather than only rewarding verbosity.
