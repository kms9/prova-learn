## Why

The repository has a reviewed seven-stage personalized-learning SOP and cross-domain positive, negative, and end-to-end examples, but it does not yet have executable repo-local skills that preserve each stage's input contract, named artifact, quality gate, and deterministic failure route. Converting the reviewed requirements and examples into seven independently invocable skills plus a shared contract and eval surface makes the SOP testable without collapsing evidence, structure, diagnosis, instruction, and mastery into one prompt.

## What Changes

- Create exactly seven repo-local stage skills under `.agents/skills/`, one for each S1–S7 stage.
- Keep S7 as one top-level skill while implementing mastery verification and versioned learner-model replanning as two ordered, atomic internal subflows.
- Define a shared handoff envelope, seven stage artifact schemas, confirmation-state rules, gate verdicts, error-attribution routes, and safe blocked states.
- Preserve mandatory live-research behavior for S1/S2: model knowledge may generate hypotheses and queries but cannot satisfy G1/G2 evidence requirements.
- Add stage-specific eval cases derived from the reviewed current requirements, 21 positive/negative examples, the PostgreSQL end-to-end case, and the senior subject-content reviewer end-to-end case.
- Include at least one concrete, source-traceable worked example in every stage skill so an isolated package demonstrates its expected artifact, verdict, and route.
- Require deterministic structural validation, a `dclaude` with-skill/without-skill benchmark, and two independent final skill-eval sessions with mutual findings cross-validation. The default final routes are `dclaude` and `gclaude`; when `dclaude` fails before inference with empty `modelUsage`, the user-authorized fallback is a fresh, separately evidenced `gclaude` session labeled as a fallback rather than as `dclaude`. Record every encountered error before fixing it and retain route/model provenance.
- Cross-review the proposal, design, specs, and tasks through both `dclaude` and `gclaude` in an `openspec-explore` stance before implementation.

## Capabilities

### New Capabilities

- `personalized-learning-stage-contracts`: Common handoff envelope, schema/version rules, confirmation states, gate verdicts, traceability, blocked states, and cross-stage routing.
- `create-goal-success-contract`: S1 skill for externally calibrated, user-confirmed observable goals and success evidence.
- `create-domain-evidence-landscape`: S2 skill for live, multi-perspective, source-traceable domain research and evidence-gap handling.
- `build-capability-concept-graph`: S3 skill for turning accepted goals and evidence into a traceable capability/concept/prerequisite/assessment graph.
- `diagnose-learner-frontier`: S4 skill for behavior-evidence-based learner state and learning-frontier diagnosis.
- `plan-learning-sessions`: S5 skill for a minimal, confirmed path from demonstrated frontier to target, with session and review gates.
- `run-instructional-interaction`: S6 skill for source-grounded instructional content, scaffolding, interaction traces, and candidate mastery evidence.
- `verify-mastery-and-replan`: S7 skill for multidimensional mastery judgment, deterministic attribution, versioned learner-model update, and replanning.

### Modified Capabilities

None.

## Impact

- New implementation roots: `.agents/skills/<stage-skill>/`.
- New planning and validation evidence under this OpenSpec change, including cross-review and eval reports.
- Source corpus remains in `docs/chat_log/`; no source example is rewritten as an observed real-world result.
- Depends on the local `skill-creator` initialization/validation utilities, OpenSpec CLI, and the user-configured `dclaude`/`gclaude` aliases; final-route fallback follows the explicit availability rule in the design and stage-contract spec.
- No production service, learner database, or external business system is modified; persistence is specified as a skill output contract, not provisioned as a live backend.
