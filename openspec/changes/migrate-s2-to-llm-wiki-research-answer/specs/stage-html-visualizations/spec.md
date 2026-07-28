## MODIFIED Requirements

### Requirement: Canonical JSON and derived HTML authority
For S3–S7, the system SHALL keep the stage handoff JSON as the sole canonical artifact and SHALL treat every generated HTML report as a derived, non-authoritative view. S1 and S2 SHALL use their LLM Wiki run-folder contracts instead and SHALL NOT generate stage HTML reports.

#### Scenario: S2 human review is requested
- **WHEN** a user reviews a current S2 run
- **THEN** the system presents the indexed Markdown and JSONL views under `s2/` without requiring canonical JSON or derived HTML

#### Scenario: Downstream HTML interaction does not mutate canonical data
- **WHEN** a user filters, selects, or expands data in an S3–S7 HTML report
- **THEN** the canonical handoff JSON remains unchanged and no interaction is represented as confirmed stage evidence

### Requirement: Versioned presentation artifact metadata
Every current S3–S7 handoff envelope SHALL contain a `presentation_artifact` object that records the HTML format, generation status, authority, source identity, interaction mode, generation time, validation facts, and reason. S1 and S2 SHALL expose delivery status through their run-folder verification files and SHALL NOT emit presentation metadata.

#### Scenario: Generated downstream HTML metadata
- **WHEN** an S3–S7 HTML report is generated successfully
- **THEN** its presentation metadata records generated status, a non-null path and time, derived authority, read-only interaction, and passing validation facts

#### Scenario: S2 completes or blocks
- **WHEN** S2 records a pass, revise, pending, or blocked result
- **THEN** `s2/verification.md` and the root index carry the delivery state and no `presentation_artifact` is required

### Requirement: Self-contained offline stage report
Each S3–S7 Skill SHALL contain a self-contained `assets/stage-report.html` that renders without a build step, remote dependency, remote request, application server, or external asset. S1 and S2 SHALL contain no current stage HTML template.

#### Scenario: S2 Skill is copied independently
- **WHEN** the S2 Skill directory is copied with a compatible G1-passed run folder
- **THEN** its run-folder contract, stage contract and examples are sufficient to write and review the S2 LLM Wiki stage area without an HTML template

#### Scenario: Downstream Skill is copied independently
- **WHEN** one S3–S7 Skill directory is copied without the other Skills
- **THEN** its HTML template and visualization contract remain available and usable

### Requirement: Stage-specific visualizations
For S3–S7, the report SHALL select a stage-specific view from `stage_id` and SHALL preserve access to unmapped fields in raw JSON. S1 and S2 SHALL use indexed Markdown/table views defined by their run-folder contracts rather than HTML view profiles.

#### Scenario: S2 domain research answers
- **WHEN** the current stage is S2
- **THEN** `s2/INDEX.md` links the research log, six-source coverage, source ledger, evidence atoms, question answers, eight-dimensional validation, G2 evaluation and verification without producing an HTML report

#### Scenario: S3 capability concept graph
- **WHEN** `stage_id` is `S3`
- **THEN** the report shows the capability outline, learning units, atomic nodes, unit-to-node mappings, typed graph edges, assessments, mastery thresholds, and traceability and provides both a relationship view and an adjacency-table equivalent

#### Scenario: S4 learner frontier
- **WHEN** `stage_id` is `S4`
- **THEN** the report shows node states, learning frontier, misconceptions, capability gaps, transfer performance, diagnosis evidence, and retest items and supports state and evidence-validity filtering

#### Scenario: S5 learning and session plan
- **WHEN** `stage_id` is `S5`
- **THEN** the report shows ordered learning nodes, sessions, assessment schedule, review anchors, risks, alternative routes, exit criteria, and confirmation state

#### Scenario: S6 instructional interaction
- **WHEN** `stage_id` is `S6`
- **THEN** the report shows the current node, explanations, positive and negative examples, activities, progressive hint ladder, feedback rules, interaction trace, candidate evidence, and content quality

#### Scenario: S7 mastery and replanning
- **WHEN** `stage_id` is `S7`
- **THEN** the report shows multidimensional mastery evidence, attribution, learner model changes, route rationale, review or retest plan, and applicability limits
