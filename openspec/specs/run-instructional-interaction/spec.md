# run-instructional-interaction Specification

## Purpose
TBD - created by archiving change create-seven-stage-personalized-learning-skills. Update Purpose after archive.
## Requirements
### Requirement: Stage-aligned instructional interaction
The S6 skill SHALL use accepted source evidence, the current plan node, learner snapshot, and predefined success criteria to produce explanation, representations, examples, contrasting cases, practice, feedback, scaffolding, and fading.

#### Scenario: Upstream content source is untraceable
- **WHEN** a critical explanation or example cannot be traced to accepted evidence
- **THEN** S6 blocks or returns upstream rather than presenting it as established fact

### Requirement: Session package and trace artifact
S6 SHALL produce `session_package_and_trace` with content/source references, activities, prompt ladder, answer-leakage controls, learner attempts, feedback, corrections, unresolved issues, interaction events, and candidate mastery evidence.

#### Scenario: Independent evidence is produced
- **WHEN** the learner completes an unshown task after scaffolding is reduced
- **THEN** the artifact records the behavior and prompt level as candidate evidence for S7

### Requirement: G6 content quality gate
S6 SHALL evaluate correctness/traceability, learner and goal fit, cognitive level, example coverage, scaffold quality, answer-leakage control, learner agency, and delivery usability; it SHALL NOT infer mastery from content quality.

#### Scenario: Long lecture exposes every answer
- **WHEN** the session consists of extensive explanation, immediate answers, and learner acknowledgment only
- **THEN** G6 emits `revise_here`, produces no valid candidate mastery claim, and blocks S7 mastery inference

### Requirement: S6 eval coverage
S6 evals SHALL cover faded worked-example instruction, multi-representation conceptual interaction, and a lecture-plus-answer anti-pattern.

#### Scenario: S6 eval definitions are present
- **WHEN** the S6 eval file is inspected
- **THEN** it contains two positive and one negative case traceable to the reviewed S6 examples

