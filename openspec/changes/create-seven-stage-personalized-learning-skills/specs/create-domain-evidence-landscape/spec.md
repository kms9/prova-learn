## ADDED Requirements

### Requirement: Live multi-perspective domain research
The S2 skill MUST execute traceable multi-round internet research covering terminology/history, theory/standards, practice/tasks, recruitment/market capability where applicable, interview/assessment evidence where applicable, and criticism/frontier disagreement.

#### Scenario: A source category is unavailable
- **WHEN** required material cannot be found
- **THEN** S2 records `gap`, criticality, confidence impact, and gate effect rather than marking it `not_applicable`

#### Scenario: A source category is genuinely inapplicable
- **WHEN** the target scope makes a source category irrelevant
- **THEN** S2 may record `not_applicable` only with a reason, criticality, and gate effect

#### Scenario: Only model knowledge or shallow search exists
- **WHEN** no executed query manifest or only a few unvetted pages support the output
- **THEN** G2 fails and the skill routes to S2 for additional research

### Requirement: Domain evidence landscape artifact
S2 SHALL produce `domain_evidence_landscape` with scope, terminology, research manifest, perspectives/questions/queries, source ledger, evidence-provenance labels, category coverage, claims-to-evidence map, practice and assessment matrices where applicable, consensus, disagreements, unknowns, gaps, and confidence.

#### Scenario: Conflicting market and normative evidence exists
- **WHEN** current job samples disagree with standards or primary domain sources
- **THEN** the artifact preserves both as distinct evidence types and does not force a false consensus

#### Scenario: Default market sample size is not met
- **WHEN** applicable recruitment research has fewer than three current role samples across two organizations or interview research has fewer than two independent samples
- **THEN** S2 records an undersample gap, lowers confidence, and blocks G2 when the gap affects core capability or target definition

### Requirement: G2 quality gate
S2 SHALL check actual network execution, source coverage/reliability, traceability, perspective diversity, follow-up depth, sample independence, timeliness, region fit, fact/market/inference separation, disagreement balance, and gap transparency.

#### Scenario: Three SEO pages claim a universal rule
- **WHEN** an evidence landscape uses unversioned promotional sources to declare consensus
- **THEN** G2 emits `revise_here` and blocks transfer to S3

### Requirement: S2 eval coverage
S2 evals SHALL cover an official-versioned technical landscape, a learning-domain landscape that preserves evidence boundaries, and an unsupported blog-based consensus.

#### Scenario: S2 eval definitions are present
- **WHEN** the S2 eval file is inspected
- **THEN** it contains two positive and one negative case traceable to the reviewed S2 examples
