## MODIFIED Requirements

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

### Requirement: Guarded quick-tier merges
Quick-tier execution MAY merge the execution of S2+S3 or S4+S5 only under accepted allow conditions and SHALL still produce and validate both stages sequentially. For S2+S3, the S2 run-folder G2 conditions MUST pass before G3 is evaluated; S3 SHALL NOT require an S2 JSON envelope.

#### Scenario: S2 and S3 may merge
- **WHEN** the domain is mature, single-paradigm, low-risk, and source quality is materially uniform
- **THEN** one execution may write the S2 stage area and then produce the S3 artifact, but the S2 G2 run-folder conditions pass before G3 is evaluated

#### Scenario: S2 and S3 merge is prohibited
- **WHEN** the domain has competing paradigms, active disagreement, uneven source reliability, rapidly changing evidence, or high-risk decisions
- **THEN** S2 and S3 execute separately

### Requirement: Concrete worked example coverage
Each stage skill SHALL include at least one concrete, source-traceable worked example that shows input facts, its current stage-specific delivery shape, gate verdict, and route without claiming simulated results were observed. S1 and S2 examples SHALL use their LLM Wiki run-folder shapes; S3–S7 retain their current artifact examples until separately migrated.

#### Scenario: Isolated S2 example is inspected
- **WHEN** an evaluator opens S2 `references/example.md`
- **THEN** it can identify the G1-passed S1 input, the nine-file S2 stage area, representative S1-question answers and multidimensional checks, expected G2 verdict, and deterministic route
