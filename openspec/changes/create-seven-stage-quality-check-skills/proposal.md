## Why

The seven stage skills (`create-seven-stage-personalized-learning-skills`) each self-report a gate verdict inside their handoff envelope. A self-reported verdict is not evidence that the artifact actually meets the gate: a stage can mislabel model memory as external evidence, skip a rubric dimension, or coerce a blocked state to `pass`. To make each stage's output independently auditable, the repository needs one standalone quality-check skill per stage that re-derives the gate verdict from the stage's own rubric, without trusting the stage's self-reported verdict and without regenerating the artifact.

## What Changes

- Create exactly seven independent repo-local quality-check skills under `.agents/quality-checks/`, one per stage S1–S7: `check-goal-success-contract` … `check-verify-mastery-and-replan`.
- Each quality-check skill is independently invocable: given a stage handoff envelope, it structurally validates the envelope and named artifact, applies that stage's gate rubric dimension by dimension, and emits a structured `quality_check_result`.
- Define one shared `quality-check-result` JSON Schema, copied byte-identically into every quality-check skill (mirrors the shared handoff-envelope pattern of the stage skills).
- Each quality-check skill embeds its stage's gate rubric (`references/check-rubric.md`) as the judging standard, kept consistent with the corresponding stage skill's `stage-contract.md`.
- Checkers MUST fail closed on structurally invalid input, MUST NOT echo the stage's self-reported verdict, MUST NOT modify the checked artifact or regenerate it, and MUST preserve blocked/insufficient states rather than coercing them to pass.
- Add three eval cases per quality-check skill (two passing-stage-output + one failing/blocked-stage-output) derived from the reviewed example corpus.

## Capabilities

### New Capabilities

- `personalized-learning-stage-quality-checks`: Seven standalone gate-checkers (one per stage), a shared quality-check-result schema, per-stage gate rubrics, independent-verdict rules, and fail-closed behavior for invalid input or unresolved blocking states.

### Modified Capabilities

None. The seven stage skills and the shared handoff envelope are owned by `create-seven-stage-personalized-learning-skills`; quality-check skills only read them.

## Impact

- New implementation roots: `.agents/quality-checks/check-<stage>/` (kept separate from `.agents/skills/` so the seven-stage inventory stays exactly seven stage skills).
- New planning/validation evidence under this OpenSpec change.
- Reads, but does not modify, `.agents/skills/<stage>/references/{handoff-envelope,<artifact>}.schema.json` and `stage-contract.md`.
- Depends on the seven stage skills being complete; no production service or learner database is modified.
