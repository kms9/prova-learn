# plan-learning-sessions Specification

## Purpose
TBD - created by archiving change create-seven-stage-personalized-learning-skills. Update Purpose after archive.
## Requirements
### Requirement: Frontier-to-goal planning
The S5 skill SHALL derive the smallest feasible path from evidence-backed learner frontier to the goal through the accepted graph, respecting hard prerequisites, constraints, risk, and resource availability.

#### Scenario: Frontier remains evidence-insufficient
- **WHEN** a critical starting node has no defensible diagnostic state
- **THEN** S5 returns to S4 rather than treating the node as mastered or not mastered

### Requirement: Learning and session plan artifact
S5 SHALL produce `learning_and_session_plan` with ordered nodes, selection/ranking rationale, strategies, scaffolding and fading rules, sessions, time, inputs, immediate/transfer/delayed assessments, review anchors, risks, alternatives, and node/path pass criteria.

#### Scenario: Plan is ready to start
- **WHEN** the first session is feasible within constraints and the learner confirms path, effort, priority, and first-session contract
- **THEN** G5 may pass to S6

### Requirement: G5 quality gate
S5 SHALL check goal connectivity, prerequisite correctness, path minimality, time feasibility, strategy fit, instruction/assessment alignment, cognitive load, adaptability, and mandatory confirmation.

#### Scenario: A course table of contents is copied
- **WHEN** the plan lists chapters, videos, or question counts without using the learner snapshot, graph, exits, or adaptation rules
- **THEN** G5 emits `revise_here` or returns to S4 when the frontier itself is unsupported

### Requirement: S5 eval coverage
S5 evals SHALL cover a misconception-driven technical path, a concept-learning path, and a generic content-consumption schedule.

#### Scenario: S5 eval definitions are present
- **WHEN** the S5 eval file is inspected
- **THEN** it contains two positive and one negative case traceable to the reviewed S5 examples

