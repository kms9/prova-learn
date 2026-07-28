# personalized-learning-stage-contracts Specification

## Purpose
TBD - created by archiving change create-seven-stage-personalized-learning-skills. Update Purpose after archive.
## Requirements
### Requirement: Exactly seven repo-local stage skills
The implementation SHALL create exactly the seven named stage skills in `.agents/skills/` and SHALL NOT create an eighth top-level stage or orchestration skill in this change.

#### Scenario: Stage package inventory is complete
- **WHEN** the final skill inventory is inspected
- **THEN** it contains one folder for each S1–S7 name declared in the design and no additional stage folder

### Requirement: Self-contained skill packages
Each stage skill SHALL contain `SKILL.md`, `agents/openai.yaml`, a stage contract reference, stage-specific output contract, and stage eval definitions. S1 and S2 SHALL use their run-folder contracts and SHALL NOT be required to include the common handoff JSON Schema or stage artifact JSON Schema; S3–S7 retain their current package requirements until separately migrated.

#### Scenario: S2 is evaluated in isolation
- **WHEN** an evaluator is given the S2 skill folder and a compatible G1-passed S1 run folder
- **THEN** the folder contains the instructions and contracts required to validate input, write the nine-file S2 stage area, update the root index, evaluate G2, and route without requiring a standalone JSON or HTML artifact

### Requirement: Common handoff envelope
S3–S7 SHALL emit the current common handoff envelope until separately migrated. S1 and S2 SHALL instead expose their current state through their LLM Wiki run-folder indexes, fixed files, stable cross-file identifiers, gate evaluations, and verification records. Consumers SHALL use the delivery model declared by the source stage rather than requiring a common envelope from S1 or S2.

#### Scenario: Valid S2 handoff is exposed
- **WHEN** S2 completes its positive flow and G2 evaluation
- **THEN** the root `INDEX.md` points to a verified `s2/INDEX.md`, the S2 nine-file contract passes, `g2-evaluation.md` records `verdict=pass` and `route_to=S3`, and no common JSON envelope is required

#### Scenario: Required S2 input is invalid
- **WHEN** the latest S1 run folder fails the G1 machine-readable conditions or its research questions cannot be resolved
- **THEN** S2 writes no fabricated positive answer, records the input failure in its diagnostic stage area when safely possible, and routes to S1

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
Quick-tier execution MAY merge the execution of S2+S3 or S4+S5 only under accepted allow conditions and SHALL still produce and validate both stages sequentially. For S2+S3, the S2 run-folder G2 conditions MUST pass before G3 is evaluated; S3 SHALL NOT require an S2 JSON envelope.

#### Scenario: S2 and S3 may merge
- **WHEN** the domain is mature, single-paradigm, low-risk, and source quality is materially uniform
- **THEN** one execution may write the S2 stage area and then produce the S3 artifact, but the S2 G2 run-folder conditions pass before G3 is evaluated

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
Each stage skill SHALL include at least one concrete, source-traceable worked example that shows input facts, its current stage-specific delivery shape, gate verdict, and route without claiming simulated results were observed. S1 and S2 examples SHALL use their LLM Wiki run-folder shapes; S3–S7 retain their current artifact examples until separately migrated.

#### Scenario: Isolated S2 example is inspected
- **WHEN** an evaluator opens S2 `references/example.md`
- **THEN** it can identify the G1-passed S1 input, the nine-file S2 stage area, representative S1-question answers and multidimensional checks, expected G2 verdict, and deterministic route

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
