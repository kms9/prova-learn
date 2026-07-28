# Analyzer notes — run-instructional-interaction

- **Discrimination:** with-skill mean pass rate is `1.0000`; without-skill is `0.2777`; delta is `+0.72`. Evidence-producing activity design, hint leakage control, trace capture and “G6 is not mastery” are effective separators.
- **Variance:** with-skill standard deviation is `0.0000`; without-skill is `0.4809`. The high baseline variance comes from the blocked fixture, where a generic answer can notice missing learner responses but still tends to route incorrectly.
- **Time:** with-skill mean is `119.5117s`, without-skill `57.9983s` (`+61.5s`).
- **Tokens:** actual outer `modelUsage` totals average `77,155.0` with the skill and `33,219.7` without it (`+43,935.3`). Full activities and interaction traces add material cost; compact repeated rubric narration is the main future optimization target.
- **Conclusion:** strong discrimination with explicit time/token overhead justified by trace completeness and answer-leakage controls.
