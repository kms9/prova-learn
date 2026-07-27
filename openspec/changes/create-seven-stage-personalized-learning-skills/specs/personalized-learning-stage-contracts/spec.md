## ADDED Requirements

### Requirement: Exactly seven repo-local stage skills
The implementation SHALL create exactly the seven named stage skills in `.agents/skills/` and SHALL NOT create an eighth top-level stage or orchestration skill in this change.

#### Scenario: Stage package inventory is complete
- **WHEN** the final skill inventory is inspected
- **THEN** it contains one folder for each S1–S7 name declared in the design and no additional stage folder

### Requirement: Self-contained skill packages
Each stage skill SHALL contain `SKILL.md`, `agents/openai.yaml`, a stage contract reference, the common handoff JSON Schema, the stage artifact JSON Schema, and stage eval definitions.

#### Scenario: One stage is evaluated in isolation
- **WHEN** an evaluator is given only one stage skill folder and its declared source fixtures
- **THEN** the folder contains the instructions and contracts required to validate its own input, output, quality verdict, and route

### Requirement: Common handoff envelope
Every stage SHALL emit an envelope with schema/run/stage identity, input validation, gaps, assumptions, confirmation, evidence, processing record, named positive artifact, rubric results, verdict, route, traceability, and creation time.

#### Scenario: Valid handoff is emitted
- **WHEN** a stage completes its positive flow and quality evaluation
- **THEN** its result validates against the common handoff schema and identifies the stage-specific artifact schema

#### Scenario: Required input is invalid
- **WHEN** an input has the wrong artifact type, unsupported schema version, stale critical evidence, or a failed upstream gate
- **THEN** the stage emits a failed input validation and a deterministic upstream route without fabricating a positive artifact

### Requirement: Confirmation state machine
The skills MUST implement mandatory, conditional, and inform confirmation modes with recorded trigger, question, response, status, time, and changed assumptions; required confirmation SHALL block advancement.

#### Scenario: Mandatory confirmation is pending
- **WHEN** S1 or S5 has not received the required user decision
- **THEN** the relevant gate cannot pass and the output records `pending`

#### Scenario: Conditional risk escalates
- **WHEN** a conditional stage detects high risk, material disagreement, or multiple consequential options
- **THEN** confirmation escalates to mandatory and advancement pauses

### Requirement: Stage-specific gates and deterministic routes
Each skill SHALL evaluate its named artifact with a stage-specific rubric and emit `pass`, `revise_here`, or `return_upstream` with an allowed `route_to`.

#### Scenario: Artifact fails locally repairable criteria
- **WHEN** the evidence shows a defect owned by the current stage
- **THEN** the skill emits `revise_here` and routes to the same stage

#### Scenario: Upstream pollution is discovered
- **WHEN** the artifact defect originates in an earlier goal, source, graph, diagnostic, or plan
- **THEN** the skill emits `return_upstream`, identifies the earliest polluted stage, and records the invalidated downstream scope

### Requirement: Explicit unknown and blocked states
The skills SHALL preserve unknown, evidence-insufficient, research-blocked, not-executed, and version-conflict states and SHALL NOT coerce them to pass.

#### Scenario: Evidence is absent
- **WHEN** a required evidence class was not collected
- **THEN** the output records the applicable blocked or insufficient state and the affected gate fails

### Requirement: Evidence provenance taxonomy
Every evidence record SHALL distinguish `model_hypothesis`, `market_signal`, `external_evidence`, `user_provided_unverified`, and `learner_behavior`; a quality gate SHALL NOT count a model hypothesis or unverified user claim as external evidence.

#### Scenario: Model knowledge proposes a domain claim
- **WHEN** an agent uses existing model knowledge to form a hypothesis or query
- **THEN** the record is labeled `model_hypothesis` and cannot satisfy G1/G2 until verified by admissible external evidence

### Requirement: Operational rubric result
Every rubric entry SHALL contain a dimension, evidence-reference array, numeric-or-boolean score, matching-type threshold, passed boolean, and—when failed—a `revise_here` or `return_upstream` action with `route_to`.

#### Scenario: A rubric dimension fails
- **WHEN** the observed score does not meet the declared threshold
- **THEN** the entry identifies its evidence, marks `passed=false`, and supplies a deterministic failure action and route

### Requirement: Safe invocation without usable upstream state
Every stage SHALL define safe behavior for missing input, empty evidence, stale input, and unable-to-confirm state and SHALL NOT fabricate an upstream artifact.

#### Scenario: S2-S7 is invoked without a required upstream artifact
- **WHEN** the required named artifact is absent
- **THEN** input validation fails and the skill routes to the earliest stage that can create or refresh it

#### Scenario: Required confirmation cannot be obtained
- **WHEN** a mandatory or escalated confirmation remains unresolved
- **THEN** the stage remains pending and its gate cannot pass

### Requirement: Guarded quick-tier merges
Quick-tier execution MAY merge S2+S3 or S4+S5 only under accepted allow conditions and SHALL still emit both named artifacts and pass both gates sequentially.

#### Scenario: S2 and S3 may merge
- **WHEN** the domain is mature, single-paradigm, low-risk, and source quality is materially uniform
- **THEN** one execution may produce both artifacts but G2 must pass before G3 is evaluated

#### Scenario: S2 and S3 merge is prohibited
- **WHEN** the domain has competing paradigms, active disagreement, uneven source reliability, rapidly changing evidence, or high-risk decisions
- **THEN** S2 and S3 execute separately

#### Scenario: S4 and S5 may merge
- **WHEN** the learner is confirmed zero-baseline, the graph has a clear start, the path is nearly linear, and an incorrect start is low-cost
- **THEN** one execution may produce both artifacts but G4 must pass before G5 is evaluated

#### Scenario: S4 and S5 merge is prohibited
- **WHEN** prior knowledge is unknown, learner evidence conflicts, adaptive skipping or high-stakes placement is required, or multiple frontiers exist
- **THEN** S4 and S5 execute separately

### Requirement: Research-tier pending gates
A research-tier run SHALL identify required independent expert review and longitudinal delayed retesting and SHALL record them as pending or not-executed until evidence exists.

#### Scenario: External expert review has not run
- **WHEN** a run is labeled research-tier and its declared expert gate has no evidence
- **THEN** the run cannot claim research-tier completion

### Requirement: Eval traceability and discrimination
Each stage SHALL define two positive evals and one negative or blocked eval derived from the reviewed example corpus, with source section, prompt, expected behavior, and machine-checkable assertions.

#### Scenario: Eval corpus is audited
- **WHEN** all stage eval files are inspected
- **THEN** 21 stage evals map to the seven reviewed stage sections and include both PostgreSQL/fraction-style and cross-domain behavior without treating simulated results as observed facts

### Requirement: Skill Creator compatible eval evidence
Each skill SHALL store cases in `evals/evals.json`; every case SHALL be run with and without the skill, graded to the installed schema, aggregated to a per-skill benchmark, and rendered to a static review file.

#### Scenario: One stage benchmark is complete
- **WHEN** all three stage cases have completed both configurations
- **THEN** six grading results, timing evidence, `benchmark.json`, `benchmark.md`, and a non-empty `review.html` exist with actual route provenance

### Requirement: End-to-end handoff audits
The PostgreSQL and senior subject-content reviewer fixtures SHALL each exercise S1→S2→S3→S4→S5→S6→S7, and the audit set SHALL include an S7→S5→S6→S7 remediation loop.

#### Scenario: Full-chain handoff passes
- **WHEN** a simulated end-to-end fixture is audited
- **THEN** every transition preserves compatible schema/version, traceability, gate ownership, and an allowed route while labeling all simulated values as fixtures

#### Scenario: Remediation loop passes
- **WHEN** S7 attributes a partial-mastery failure to strategy or sequence
- **THEN** the trace returns to S5, produces an updated S6 interaction, re-enters S7, and retains prior evidence and model-version history

### Requirement: Concrete worked example coverage
Each stage skill SHALL include at least one concrete, source-traceable worked example that shows input facts, an abbreviated named stage artifact, gate verdict, and route without claiming that simulated results were observed.

#### Scenario: Isolated skill example is inspected
- **WHEN** an evaluator opens `references/example.md` in any one of the seven skill folders
- **THEN** it can identify the example source section, stage-specific artifact shape, expected quality verdict, and deterministic route

### Requirement: Validation and external evidence
Completion SHALL require successful local skill validation, JSON/schema checks, OpenSpec validation, a comparative `dclaude` benchmark, two independent structured final skill-eval session passes, and a mutual findings cross-check. The default final routes SHALL be `dclaude` and `gclaude`. When dclaude fails before inference with a provider/route error, empty `modelUsage`, and no parseable inner verdict, an explicitly user-authorized fresh gclaude session MAY replace that unavailable final retry. The fallback SHALL use a distinct session and prompt, declare `fallback_for=dclaude`, preserve the original dclaude failure, and SHALL NOT be represented as dclaude or as provider diversity. Both accepted final outer or route records SHALL have non-empty `modelUsage`, and both inner results SHALL parse as JSON with no unresolved blocking or major finding.

#### Scenario: Static validation passes but eval has not run
- **WHEN** `quick_validate.py` succeeds but the comparative benchmark, either accepted final session, parseable route result, or mutual cross-check is absent or failing
- **THEN** the change remains incomplete

#### Scenario: dclaude final retry fails before inference
- **WHEN** dclaude returns a provider/route error with empty `modelUsage` and no inner verdict, and the user explicitly authorizes gclaude fallback
- **THEN** the original failure remains auditable and a fresh, separately evidenced gclaude session may satisfy the unavailable final-session slot only when it declares `fallback_for=dclaude` and passes mutual findings cross-check with the original successful gclaude session

### Requirement: Error-first audit log
Every material failure SHALL be written to the durable error ledger before remediation, retaining symptom, diagnosis, fix, status, and revalidation evidence.

#### Scenario: A validator fails
- **WHEN** a skill, schema, OpenSpec, alias, or eval command returns a material error
- **THEN** an OPEN ledger entry exists before the related fix is applied and is later updated rather than deleted
