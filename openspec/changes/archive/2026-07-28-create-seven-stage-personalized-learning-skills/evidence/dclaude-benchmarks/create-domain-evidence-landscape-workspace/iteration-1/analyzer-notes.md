# Analyzer notes — create-domain-evidence-landscape

- **Discrimination:** with-skill mean pass rate is `1.0000`; without-skill is `0.2223`; delta is `+0.78`. Executed-research evidence, category coverage, claim/source linkage and G2 routing remain discriminating.
- **Variance:** with-skill standard deviation is `0.0000`; without-skill is `0.3851`. Baseline variance is high because the negative case can satisfy generic provenance cautions while still missing gap classification and fail-closed routing.
- **Time:** with-skill mean is `320.288s`, without-skill `147.667s` (`+172.6s`). Live research and source auditing are the dominant cost.
- **Tokens:** actual outer `modelUsage` totals average `193,616.7` with the skill and `117,192.0` without it (`+76,424.7`). The accuracy gain has a material token cost; a later optimization should reduce repeated source narration without weakening the manifest or ledger.
- **Conclusion:** high quality gain with the clearest cost trade-off among the completed stages.
