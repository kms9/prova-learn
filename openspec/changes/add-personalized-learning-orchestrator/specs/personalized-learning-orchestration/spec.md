## ADDED Requirements

### Requirement: Single orchestration entrypoint
The repository SHALL provide a repo-local `al-orchestrate-personalized-learning` Skill that accepts a user's natural-language learning request and acts as the control-plane entrypoint above exactly seven business stages. The orchestrator MUST NOT define S0/G0, own a stage artifact, or replace any S1–S7 Gate.

#### Scenario: User starts without knowing stage names
- **WHEN** a user invokes only the orchestrator and describes a learning goal in natural language
- **THEN** the orchestrator selects and invokes the applicable S1–S7 Skill without requiring the user to name that stage Skill

### Requirement: Deterministic intent routing
The orchestrator SHALL classify explicit stage requests, goal changes, continue/status requests, and semantic learning intents using a documented precedence. A new project or material goal change MUST route to S1; a continue request MUST use verified project state; a pure status request MUST remain read-only.

#### Scenario: Continue an existing project
- **WHEN** the user says to continue and one project is unambiguously selected
- **THEN** the orchestrator reads the current project state and selects its verified `route_to` rather than inferring the next stage from conversation wording alone

#### Scenario: Goal changes after later stages exist
- **WHEN** the user materially changes the target outcome, use case, success evidence, or domain boundary
- **THEN** the orchestrator routes to S1 and preserves downstream invalidation semantics

#### Scenario: Status only
- **WHEN** the user asks what has been completed and what comes next without asking to continue
- **THEN** the orchestrator reports current stage, Gate evidence and next action without invoking a mutating stage transaction

### Requirement: Authoritative project resolution
The orchestrator SHALL resolve project context in the order defined by the standalone invocation contract and MUST read the project root, `project-state.json`, current conversation pointers, manifest and stage profile before mutation. If multiple projects match and the choice affects writes, it MUST ask for clarification.

#### Scenario: Multiple candidate projects
- **WHEN** two or more project workspaces plausibly match a mutating request and the user did not identify one
- **THEN** the orchestrator pauses before stage invocation and asks the user to select the project

### Requirement: Exact stage delegation
After selecting a stage, the orchestrator SHALL load and follow that stage's current `SKILL.md` and shared contracts. It MUST NOT reproduce, weaken, or bypass the stage's research, confirmation, learner-behavior, version, artifact, Gate, or verification rules.

#### Scenario: Teaching request lacks learner prerequisites
- **WHEN** the user asks to begin teaching but the selected project's required upstream Gates are missing
- **THEN** the orchestrator preserves the selected stage's blocked behavior or, only under an explicit full-flow request, starts from the earliest missing stage

### Requirement: Bounded full-flow advancement
The orchestrator SHALL default to one stage per request. It MAY advance across stages only when the user explicitly requests a full or prerequisite-completing flow and each preceding stage is revalidated as completed with an allowed route. It MUST stop on confirmation, real learner input, consequential choice, blocked/pending state, research failure, version conflict, same-stage revision, or an upstream remediation route.

#### Scenario: Mandatory confirmation is reached
- **WHEN** guided flow reaches an unresolved S1 or S5 mandatory confirmation
- **THEN** the orchestrator stops, presents the concrete confirmation request, and does not invoke the downstream stage

#### Scenario: Mastery verification routes upstream
- **WHEN** S7 validly routes to S1–S7 for remediation instead of `complete`
- **THEN** the orchestrator stops the current automatic loop, reports the attribution and recovery stage, and waits for new user input or evidence

### Requirement: Evidence-backed post-delegation verification
After a mutating stage delegation, the orchestrator SHALL re-read the persisted project and stage evidence, including revision, stage state, Gate, `route_to`, verification and conversation linkage. It MUST report `not_executed`, `pending`, `blocked`, or an evidence gap when those facts cannot be verified.

#### Scenario: Stage claims completion without persisted evidence
- **WHEN** the delegated stage response says it completed but the expected project transaction or Gate evidence is absent
- **THEN** the orchestrator does not report completion and identifies the missing evidence

### Requirement: Actionable next-step response
Every orchestration response SHALL identify the resolved project/revision when available, understood intent, selected or executed stage, selection reason, stage/Gate state, evidence entrypoint, stop reason, required user input, and one concrete next action. The next action SHALL keep the orchestrator as the user-facing entrypoint.

#### Scenario: Stage is pending on learner behavior
- **WHEN** S4 or S6 has valid prerequisites but waits for a real learner answer
- **THEN** the response presents the exact question or activity to answer and tells the user to continue through `al-orchestrate-personalized-learning`, without fabricating a learner response
