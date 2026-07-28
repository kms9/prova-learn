# diagnose-learner-frontier Specification

## Purpose
TBD - created by archiving change create-seven-stage-personalized-learning-skills. Update Purpose after archive.
## Requirements
### Requirement: Behavior-evidence diagnosis
The S4 skill SHALL infer learner state from multiple aligned behavior tasks and SHALL record correctness, reasoning, prompt dependence, time where available, confidence, error type, and evidence validity.

#### Scenario: Learner self-rates highly
- **WHEN** self-report is not supported by behavior evidence
- **THEN** S4 uses the self-report only to guide assessment selection and does not mark graph nodes mastered

#### Scenario: Learner succeeds only with material prompting
- **WHEN** the only success evidence for a node has `prompt/hint_dependency` equal to medium, high, or unknown
- **THEN** S4 does not mark that node `tested_mastered`, preserves it as not-mastered/evidence-insufficient, and schedules an unprompted retest

### Requirement: Learner snapshot artifact
S4 SHALL produce a versioned `learner_snapshot` separating mastered, developing/not-mastered, evidence-insufficient, and stale nodes; it SHALL include misconceptions, prompt dependence, transfer, confidence calibration, learning frontier, and evidence references.

#### Scenario: No prior learner record exists
- **WHEN** the learner is a cold start
- **THEN** S4 records unknown/evidence-insufficient state and collects diagnostic evidence instead of assuming every node is not mastered

### Requirement: G4 quality gate
S4 SHALL evaluate target alignment, evidence sufficiency, guessing control, prompt-dependence recording, error classification, bias control, and explainability.

#### Scenario: One easy item is correct
- **WHEN** a single recognition item is the only evidence
- **THEN** G4 cannot establish a learning frontier and routes to S4 for additional tasks or S3 if the item is invalid

### Requirement: S4 eval coverage
S4 evals SHALL cover a technical misconception diagnosis, a conceptual misconception diagnosis, and a self-report-only false advanced classification.

#### Scenario: S4 eval definitions are present
- **WHEN** the S4 eval file is inspected
- **THEN** it contains two positive and one negative case traceable to the reviewed S4 examples

