# Analyzer notes — diagnose-learner-frontier

- **Discrimination:** after correcting two fixture-contract defects and rerunning the affected configurations, with-skill mean pass rate is `1.0000`; without-skill is `0.4444`; delta is `+0.56`.
- **Variance:** with-skill standard deviation is `0.0000`; without-skill is `0.5092`. The negative fail-closed case is deliberately easy for a capable baseline and scores 6/6, while the two positive cases retain structural and evidence-traceability discrimination.
- **Time:** with-skill mean is `150.6577s`, without-skill `65.7723s` (`+84.9s`).
- **Tokens:** canonical-route outer `modelUsage` totals average `66,935.3` with the skill and `43,517.0` without it (`+23,418.3`); eval-2 with-skill and eval-3 with/without use the successful gclaude repair-route totals, while the other three runs use their original dclaude totals.
- **Repair provenance:** original dclaude outputs and the first gclaude grading are retained. Current eval-2 with-skill and eval-3 with/without outputs are gclaude reruns because dclaude returned 402 after the contract fixes; route metadata records actual `modelUsage`. The first eval-2 rerun failed with a connection close and created no file; the successful retry passed both handoff and learner-snapshot schemas.
- **Semantic guard result:** the repaired eval-2 artifact has no `tested_mastered` node with medium/high/unknown hint dependence; repaired eval-3 with-skill has `positive_artifact=null`, `verdict=revise_here`, `route_to=S4`.
- **Conclusion:** current with-skill results are stable and correct. Final dclaude rerun/audit remains a separate external gate; gclaude evidence is not represented as dclaude.
