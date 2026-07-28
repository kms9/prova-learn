## ADDED Requirements

### Requirement: Accepted and traceable upstream inputs
The S3 skill SHALL require G1/G2-passed goal and evidence artifacts with compatible versions and SHALL route evidence gaps to S2 instead of inventing domain facts.

#### Scenario: A graph node lacks source support
- **WHEN** a critical node or relationship depends on an unsupported domain claim
- **THEN** S3 returns upstream to S2 and identifies the affected node and claim

### Requirement: Capability concept graph artifact
S3 SHALL produce `capability_concept_graph` containing goal capabilities, node types, named relationships, hard/soft/conditional prerequisites, relationship rationales, capability statements, misconceptions, assessment items, mastery rules, and traceability to goals, evidence, and final assessment.

#### Scenario: Graph supports diagnosis
- **WHEN** the artifact passes G3
- **THEN** every critical target capability maps through prerequisite nodes to observable assessment and mastery evidence

### Requirement: Optional canonical knowledge concept map
S3 MAY also produce a human-readable `canonical_knowledge_concept_map` when the target benefits from a domain-standard map distinct from the learner overlay; it SHALL remain traceable to the same accepted evidence and SHALL NOT replace the machine-actionable capability graph.

#### Scenario: Professional domain uses dual maps
- **WHEN** the stage needs both a stable domain map and an executable capability/prerequisite graph
- **THEN** the output distinguishes the canonical map from the capability graph and leaves learner-specific state to S4

### Requirement: G3 quality gate
S3 SHALL check acyclicity, explainable prerequisites, target coverage, consistent granularity, capability/concept distinction, assessment validity, readable propositions, and end-to-end traceability.

#### Scenario: A topic list is submitted as a graph
- **WHEN** the output has disconnected labels without focus question, named edges, rationale, assessments, or sources
- **THEN** G3 emits `revise_here` and blocks transfer to S4

### Requirement: S3 eval coverage
S3 evals SHALL cover a technical capability graph, a concept-learning graph, and a directory-like pseudo-graph.

#### Scenario: S3 eval definitions are present
- **WHEN** the S3 eval file is inspected
- **THEN** it contains two positive and one negative case traceable to the reviewed S3 examples
