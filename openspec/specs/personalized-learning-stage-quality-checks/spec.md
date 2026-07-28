# personalized-learning-stage-quality-checks Specification

## Purpose
TBD - created by archiving change create-seven-stage-quality-check-skills. Update Purpose after archive.
## Requirements
### Requirement: Exactly seven standalone quality-check skills
The implementation SHALL create exactly seven quality-check skills in `.agents/quality-checks/`, one per stage S1–S7, and SHALL NOT create a stage skill, an orchestrator, or an eighth checker in this change.

#### Scenario: Quality-check inventory is complete
- **WHEN** the `.agents/quality-checks/` inventory is inspected
- **THEN** it contains exactly one `check-<stage>` folder per S1–S7 and no additional folder

### Requirement: Independently invocable per-stage checker
Each quality-check skill SHALL be runnable standalone given only a stage handoff envelope and SHALL produce a `quality_check_result` that re-derives that stage's gate verdict.

#### Scenario: One checker is run in isolation
- **WHEN** an evaluator runs one `check-<stage>` skill against that stage's envelope
- **THEN** the checker emits a result that names the stage, gate, checked artifact, per-dimension findings, verdict, and route without invoking any other stage or checker

### Requirement: Independent verdict, not echoed
A quality-check skill SHALL derive its verdict from the stage gate rubric and the checked artifact and SHALL NOT adopt the stage's self-reported `quality_evaluation.verdict` as its own conclusion.

#### Scenario: Stage self-reports pass but artifact is defective
- **WHEN** the checked envelope claims `verdict=pass` but a rubric dimension actually fails
- **THEN** the checker marks that dimension `passed=false` and emits a non-pass verdict with the matching route

### Requirement: Shared quality-check-result schema
Every quality-check skill SHALL emit a result validating against the shared `quality-check-result` JSON Schema, copied byte-identically into all seven checker folders.

#### Scenario: Checker output is machine-checkable
- **WHEN** a checker result is validated
- **THEN** it validates against the shared schema and contains `stage_id`, `gate_id`, `checked_envelope_ref`, `structural_validation`, `dimension_results[]`, `verdict`, `route_to`, and `checked_at`

### Requirement: Per-stage gate rubric as the standard
Each quality-check skill SHALL embed its stage's gate rubric in `references/check-rubric.md`, kept consistent with the corresponding stage skill's `stage-contract.md` rubric, and SHALL evaluate every declared dimension with evidence, score, threshold, and `passed`.

#### Scenario: A failing dimension carries a route
- **WHEN** a rubric dimension's score does not meet its threshold
- **THEN** the dimension result supplies `failure_action` (`revise_here`/`return_upstream`) and `route_to`

### Requirement: Structural validation and fail-closed behavior
Each quality-check skill SHALL structurally validate the checked envelope against the shared handoff schema and the named artifact against the stage artifact schema, and SHALL fail closed (emit `blocked`, no fabricated pass) when the input is structurally invalid or the artifact cannot be located.

#### Scenario: Invalid envelope is rejected
- **WHEN** the checked envelope does not validate against the handoff schema or the artifact is absent
- **THEN** the checker records the structural errors and emits `verdict=blocked` without inventing a pass

### Requirement: Preserve blocking states
A quality-check skill SHALL preserve unresolved confirmation, missing research, and evidence-insufficient states as blocking rather than coercing them to `pass`, and SHALL NOT count `model_hypothesis` or `user_provided_unverified` as admissible external evidence.

#### Scenario: Mandatory confirmation is unresolved
- **WHEN** the checked stage requires mandatory confirmation and `confirmation.status` is not resolved
- **THEN** the checker flags `confirmation_check.blocking=true` and does not emit `pass`

### Requirement: Read-only checker
A quality-check skill SHALL NOT modify the checked artifact, regenerate the stage output, or advance the run; it only reads and judges.

#### Scenario: Checker does not mutate inputs
- **WHEN** a checker runs against an envelope
- **THEN** no file or field in the checked stage skill is changed and no new stage artifact is produced

### Requirement: Quality-check eval traceability
Each quality-check skill SHALL define three eval cases (two passing-stage-output + one failing/blocked-stage-output) derived from the reviewed example corpus, with source section, prompt, expected behavior, and machine-checkable assertions.

#### Scenario: Checker eval corpus is audited
- **WHEN** all seven `check-*` eval files are inspected
- **THEN** 21 checker evals map to the seven stage sections and each case's expectations cover independent-verdict, structural validation, blocking-state preservation, and deterministic routing

