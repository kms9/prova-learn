# Final route fallback approval

- Date: 2026-07-27
- User decision: when dclaude encounters the same route-level failure, gclaude may be used for the retry.
- Trigger evidenced here: dclaude returned HTTP 402 before inference, with `modelUsage={}`, zero input/output tokens, and no inner skill-eval verdict.
- Preserved failure evidence: `final-dclaude-audit.outer.json`, `final-dclaude-reaudit.outer.json`, and `final-dclaude-closure.outer.json`.
- Accepted fallback: a fresh gclaude session with a distinct adversarial prompt and separate inner/route records.
- Required provenance: the fallback record declares `fallback_for=dclaude`; it is not labeled as dclaude and does not claim provider diversity.
- Completion rule: the original successful gclaude session and the fresh fallback session each have non-empty actual `modelUsage`, parseable inner JSON, exchange structured findings, and end with no unresolved blocking or major finding.
