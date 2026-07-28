## ADDED Requirements

### Requirement: S1 input and external preflight
The S1 skill SHALL accept a learner request, target problem or usage scene, constraints, and available materials; it MUST run a live external preflight on cold start or material target change before G1 can pass.

#### Scenario: Cold-start request is incomplete
- **WHEN** the learner provides a broad goal without observable success evidence, scope, or constraints
- **THEN** S1 records the gaps, performs bounded terminology/role/assessment preflight research, and requests mandatory confirmation

#### Scenario: Research is unavailable
- **WHEN** live search or browsing cannot be executed
- **THEN** S1 emits `research_blocked`, does not represent model knowledge as evidence, and keeps G1 failed

### Requirement: Goal success contract artifact
S1 SHALL produce `goal_success_contract` with target problem and scene, terminology/role correction, observable capability ladder, final assessment and pass rules, initial market or practice tasks where applicable, scope, exclusions, constraints, confirmed items, open questions, and `external_research_seed`.

#### Scenario: Goal artifact is complete
- **WHEN** external preflight evidence exists and mandatory confirmation succeeds
- **THEN** every core capability maps to observable evidence and the final assessment distinguishes recall from problem-solving ability

#### Scenario: Preflight uses model knowledge to form a query
- **WHEN** S1 proposes terminology or role hypotheses before external verification
- **THEN** the seed labels them `model_hypothesis` and labels verified job evidence separately as `market_signal` or `external_evidence`

### Requirement: G1 quality gate
S1 SHALL evaluate observability, decidability, scene realism, external calibration, required source-category coverage, boundary clarity, constraint completeness, assessment alignment, and confirmation.

#### Scenario: Seven-day expert goal uses video hours and quizzes
- **WHEN** a proposed contract defines expertise by content-consumption time and a recall-only quiz
- **THEN** G1 does not pass and S1 routes to itself with the missing observable behavior and scenario boundaries

### Requirement: S1 eval coverage
S1 evals SHALL cover an observable PostgreSQL goal, a learner-appropriate concept goal, and an unobservable “become an expert” goal.

#### Scenario: S1 eval definitions are present
- **WHEN** the S1 eval file is inspected
- **THEN** it contains two positive and one negative case traceable to the reviewed S1 examples
