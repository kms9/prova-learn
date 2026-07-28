# verify-mastery-and-replan Specification

## Purpose
TBD - created by archiving change create-seven-stage-personalized-learning-skills. Update Purpose after archive.
## Requirements
### Requirement: Multidimensional mastery verification
The S7 skill SHALL judge mastery from predefined rules and multiple relevant evidence dimensions including independence, reasoning, prompt dependence, transfer, confidence where useful, and delayed retention where required.

#### Scenario: One recognition item is correct
- **WHEN** a learner answers one recognition question correctly without transfer or retention evidence
- **THEN** S7 emits `EVIDENCE_INSUFFICIENT`, does not mark the node mastered, and routes to S7 for additional evidence

### Requirement: Ordered internal verification and replanning
S7 SHALL keep one top-level skill while executing mastery verification before learner-model update and replanning; the update SHALL reference the produced mastery evidence.

#### Scenario: Mastery is partial
- **WHEN** independent application passes but transfer evidence fails
- **THEN** the skill can produce a valid not-yet-mastered or provisional artifact, preserve uncertainty, and route to the earliest matching remediation stage

### Requirement: Versioned learner-model transaction
S7 SHALL separate raw evidence, inferred state, and routing decision; it SHALL require `learner_id`, evidence event IDs, `expected_model_version`, proposed new version, before/after values, and update reason.

#### Scenario: Model version conflicts
- **WHEN** the current model version differs from `expected_model_version`
- **THEN** no update is claimed, a version conflict is recorded, and the caller is instructed to reload and reconsider

### Requirement: Learner-model retrieval and audit protocol
S7 SHALL specify `load(learner_id, as_of)`, immutable `append_evidence(event)`, version-checked `update(expected_version, patch)`, and `history(learner_id)` as an output protocol; it SHALL return version, evidence validity, missing fields, and auditable route reasons without claiming an unexecuted backend operation.

#### Scenario: Cold-start learner is loaded
- **WHEN** no prior learner model exists
- **THEN** the protocol returns unknown/evidence-insufficient state and routes to S4 rather than interpreting no record as not mastered

#### Scenario: History is replayed
- **WHEN** an auditor requests learner-model history
- **THEN** immutable evidence events, inferred state changes, model versions, attribution, and route reasons can be reconstructed in order

### Requirement: Deterministic attribution routing
S7 SHALL implement the attribution routes `EVIDENCE_INSUFFICIENT→S7`, `CONTENT_QUALITY→S6`, `STRATEGY_OR_SEQUENCE→S5`, `DIAGNOSTIC_ERROR→S4`, `GRAPH_ERROR→S3`, `SOURCE_ERROR→S2`, `GOAL_CHANGED→S1`, `NODE_MASTERED→S6`, and `GOAL_ACHIEVED→complete`.

#### Scenario: Multiple causes exist
- **WHEN** evidence supports more than one attribution
- **THEN** the skill selects the earliest upstream pollution source as primary, records secondary causes, and identifies invalidated downstream artifacts

### Requirement: Mastery and replanning bundle artifact
S7 SHALL produce `mastery_and_replanning_bundle` with node-level evidence/verdicts, attribution, model patch or honest non-update state, route, revised plan/next session, review schedule, traceability, and applicability limits.

#### Scenario: Learner has not yet mastered but routing is correct
- **WHEN** the stage identifies a real gap and produces an evidence-aligned remediation route
- **THEN** the S7 artifact quality gate may pass even though learner mastery did not

### Requirement: G7 quality gate
S7 SHALL evaluate evidence sufficiency, rule consistency, prompt effects, transfer/retention, update consistency, route explainability, and resistance to single-result overreaction.

#### Scenario: Final simulation passes
- **WHEN** all predefined capability and retention evidence passes within a declared simulated scope
- **THEN** S7 records `GOAL_ACHIEVED` with scope limits and SHALL NOT claim real employment, production, or untested-domain readiness

### Requirement: S7 eval coverage
S7 evals SHALL cover correct partial-mastery routing, multidimensional retained mastery, and a single-item inflated mastery claim.

#### Scenario: S7 eval definitions are present
- **WHEN** the S7 eval file is inspected
- **THEN** it contains two positive and one negative case traceable to the reviewed S7 examples

