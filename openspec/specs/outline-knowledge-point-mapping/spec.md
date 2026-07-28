# outline-knowledge-point-mapping Specification

## Purpose
TBD - created by archiving change add-outline-knowledge-mapping-to-s3. Update Purpose after archive.
## Requirements
### Requirement: Seven-stage ownership
The system SHALL model the capability outline and its knowledge-point associations inside S3 `build-capability-concept-graph` and SHALL NOT create an eighth stage, a new stage skill, or a parallel `learning_architecture` source of truth.

#### Scenario: Outline modeling is requested
- **WHEN** a G1/G2-passed target needs a readable capability outline before diagnosis
- **THEN** S3 includes that outline in `capability_concept_graph` and evaluates it under G3

### Requirement: Capability outline levels
S3 SHALL represent target capabilities, sub-capabilities or problem families, and assessable learning units as containment levels; a narrow target MAY omit the sub-capability level only when the omission rationale is recorded and the learning unit still has a valid target-capability parent.

#### Scenario: Narrow goal does not justify three populated levels
- **WHEN** adding a synthetic sub-capability would only satisfy a numeric depth rule
- **THEN** S3 attaches the learning unit to the target capability and records why the middle level was omitted

### Requirement: Assessable learning units
Every positive S3 artifact SHALL contain `learning_units` with a stable unit ID, title, valid parent reference and level, observable outcome, goal references, source references, and a `required`, `optional`, or `extension` scope role.

#### Scenario: Learning unit is ready for mapping
- **WHEN** S3 emits an assessable learning unit
- **THEN** the unit identifies what capability it exits with and which S1 goal and S2 source support it

### Requirement: Typed many-to-many unit-node mappings
Every positive S3 artifact SHALL contain `unit_node_mappings` that connect learning units to canonical atomic nodes using `core`, `supporting`, or `extension` coverage roles and a non-empty rationale. The same node MAY map to multiple units and SHALL retain one canonical `node_id`.

#### Scenario: Cross-cutting knowledge point supports two units
- **WHEN** one atomic concept is required by two assessable learning units
- **THEN** two mappings reference the same canonical node instead of duplicating the node

### Requirement: Relationship semantics are separated
S3 MUST keep containment, unit-node coverage, and hard/soft prerequisite relations distinct. Parent/child hierarchy or display order SHALL NOT be treated as prerequisite evidence, and personalized introduce/reinforce/review ordering SHALL remain owned by S5/S6.

#### Scenario: Outline order differs from prerequisite order
- **WHEN** a unit appears earlier in the readable outline but its nodes depend on another unit's nodes
- **THEN** S3 preserves the readable containment view and records the actual prerequisite only in graph edges

### Requirement: Mapping integrity and coverage
G3 SHALL fail unless entity IDs are unique, every parent and mapping reference resolves, the containment hierarchy and hard-prerequisite subgraph are acyclic, every learning unit has at least one `core` mapping, every target-required node is covered, and unexplained duplicate core nodes are absent.

#### Scenario: Learning unit has no core node
- **WHEN** a learning unit contains only supporting or extension mappings
- **THEN** G3 emits `revise_here`, routes to S3, and blocks S4–S7

#### Scenario: Mapping points to an unknown node
- **WHEN** `unit_node_mappings` references a missing `node_id`
- **THEN** G3 records a dangling-reference failure and routes to S3 without fabricating the node

### Requirement: Provenance and version impact
Learning units and core mappings SHALL be traceable to accepted S1 goals and S2 sources. A semantic change to a unit, canonical node, mapping, or prerequisite SHALL produce a new S3 artifact version and record the affected downstream S4–S7 scope; prior learner evidence SHALL NOT silently transfer to a semantically replaced ID.

#### Scenario: Knowledge-point meaning changes
- **WHEN** a node's meaning changes rather than only its label
- **THEN** S3 creates a replacement identity/version, preserves the prior identity for audit, and marks dependent downstream artifacts stale

### Requirement: Deterministic failure ownership
S3 SHALL route goal/scope conflicts to S1, unsupported unit or node facts to S2, and local hierarchy, granularity, mapping, coverage, duplicate, or prerequisite defects to S3.

#### Scenario: Unit statement has no audited source
- **WHEN** the hierarchy is structurally valid but a required learning unit depends on an unsupported domain claim
- **THEN** S3 returns upstream to S2 and identifies the affected unit and invalidated downstream scope

### Requirement: S5 consumption boundary
S5 SHALL consume accepted learning-unit mappings only as a readable grouping over the graph, SHALL order atomic nodes from the learner frontier and prerequisite graph, and SHALL return mapping, version, granularity, or prerequisite defects to S3 instead of repairing them.

#### Scenario: Planning discovers a stale mapping
- **WHEN** the learning plan references a unit mapping from an incompatible S3 artifact version
- **THEN** S5 returns upstream to S3 and does not produce a passing G5 plan

### Requirement: Existing eval surface is extended
The S3 eval file SHALL retain two positive and one negative case while adding assertions for assessable learning units, many-to-many mappings, relation separation, coverage, and deterministic failure behavior.

#### Scenario: Directory-like pseudo-graph is evaluated
- **WHEN** the negative directory case has no assessable learning units or valid unit-node mappings
- **THEN** the case fails G3 without increasing the seven-stage total beyond 21 eval definitions

