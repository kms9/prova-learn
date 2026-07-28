## ADDED Requirements

### Requirement: Canonical JSON and derived HTML authority
The system SHALL keep the stage handoff JSON as the sole canonical artifact and SHALL treat every generated HTML report as a derived, non-authoritative view.

#### Scenario: HTML interaction does not mutate canonical data
- **WHEN** a user filters, selects, expands, or enters data in a stage HTML report
- **THEN** the canonical handoff JSON remains unchanged and no interaction is represented as confirmed stage evidence

#### Scenario: Draft becomes eligible only after stage processing
- **WHEN** a user exports an interaction draft from HTML
- **THEN** the draft is marked unsubmitted and has no canonical effect until the corresponding stage Skill validates and records it in a new handoff

### Requirement: Versioned presentation artifact metadata
Every `1.1.0` handoff envelope SHALL contain a `presentation_artifact` object that records the HTML format, generation status, authority, source identity, interaction mode, generation time, validation facts, and reason.

#### Scenario: Generated HTML metadata
- **WHEN** an HTML report is generated successfully
- **THEN** `status` is `generated`, `path` and `generated_at` are non-null, `authority` is `derived_non_authoritative`, `interaction_mode` is `draft_export_only`, and `reason` is null

#### Scenario: Failed HTML metadata
- **WHEN** HTML generation fails
- **THEN** `status` is `failed`, `path` and `generated_at` are null, and `reason` contains a non-empty failure explanation

#### Scenario: HTML explicitly not requested
- **WHEN** the caller explicitly does not request an HTML artifact or has not authorized file output
- **THEN** `status` is `not_requested`, `path` and `generated_at` are null, and `reason` explains the boundary

#### Scenario: Validation fact was not run
- **WHEN** an HTML validation check was not executed
- **THEN** its validation value is `not_run` and is not reported as `pass`

### Requirement: Self-contained offline stage report
Each S1—S7 Skill SHALL contain a self-contained `assets/stage-report.html` that renders without a build step, remote dependency, remote request, application server, or external asset.

#### Scenario: Skill is copied independently
- **WHEN** one stage Skill directory is copied without the other six Skills
- **THEN** its HTML template and visualization contract remain available and usable

#### Scenario: Report opens offline
- **WHEN** a generated report is opened through a local file URL with the network unavailable
- **THEN** its embedded JSON, navigation, filtering, details, and draft export remain usable

#### Scenario: Template consistency
- **WHEN** the seven Skill templates are compared
- **THEN** their byte content and SHA-256 hashes are identical

### Requirement: Embedded and user-selected JSON loading
The report SHALL load an safely embedded handoff envelope by default and SHALL allow a user to replace the view with a JSON file that the user explicitly selects or drops.

#### Scenario: Embedded envelope loads
- **WHEN** the template contains a valid handoff in the `stage-data` application JSON block
- **THEN** the report renders that handoff without requiring user action

#### Scenario: User selects a valid local JSON file
- **WHEN** the user selects or drops a valid handoff JSON file
- **THEN** the report asynchronously reads, parses, and renders the selected handoff and announces success

#### Scenario: User selects invalid JSON
- **WHEN** the selected file is not valid JSON or lacks a supported stage identifier
- **THEN** the report preserves a recoverable interface, displays an accessible error, and does not fabricate stage data

### Requirement: Secure rendering of untrusted data
The report SHALL treat all handoff and draft values as untrusted data, SHALL render them only through safe DOM or SVG node APIs, and SHALL not transmit them over the network.

#### Scenario: JSON contains HTML-like content
- **WHEN** a field contains tags, event attributes, script text, or a closing script sequence
- **THEN** the value is displayed as inert text and does not create executable markup

#### Scenario: Static security inspection
- **WHEN** the report source is inspected
- **THEN** it contains no input-data path to `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, `eval`, or `Function`, and contains no fetch, XHR, WebSocket, EventSource, remote script, remote style, or remote font dependency

#### Scenario: Embedded data serialization
- **WHEN** a Skill embeds JSON into the report
- **THEN** it escapes `<`, U+2028, and U+2029 before replacing only the designated application JSON data block

### Requirement: Common report shell and accessible interaction
Every stage report SHALL provide stage and run identity, status and authority warnings, summary, stage details, evidence and traceability, quality and gates, raw JSON, routing information, keyboard-operable navigation, visible focus, responsive reflow, reduced-motion support, and text alternatives for visual encodings.

#### Scenario: Keyboard tab navigation
- **WHEN** focus is in the report tab list
- **THEN** Left Arrow, Right Arrow, Home, End, Enter, and Space operate the tabs consistently with the declared ARIA roles and selected state

#### Scenario: Visual state is not color-only
- **WHEN** a status, relation, threshold, or selection is shown
- **THEN** text, a symbol, a pattern, or a line style conveys the same distinction as color

#### Scenario: Complex visualization alternative
- **WHEN** the report displays a graph, timeline, matrix, or chart
- **THEN** the same material facts are available in a structured text list or table

#### Scenario: Narrow viewport
- **WHEN** the viewport width is 320 CSS pixels
- **THEN** primary content reflows without loss of information or functionality, except for components whose meaning inherently requires two-dimensional scrolling

### Requirement: Stage-specific visualizations
The report SHALL select a stage-specific view from `stage_id` and SHALL preserve access to unmapped fields in raw JSON.

#### Scenario: S1 goal success contract
- **WHEN** `stage_id` is `S1`
- **THEN** the report shows the target scene, observable capabilities, final assessment, pass rules, scope and exclusions, open questions, and confirmation state and can export a goal contract confirmation draft

#### Scenario: S2 domain evidence landscape
- **WHEN** `stage_id` is `S2`
- **THEN** the report shows research run history, category coverage, claim-to-source traceability, consensus, disagreements, source ledger, and evidence gaps and supports source and claim filtering

#### Scenario: S3 capability concept graph
- **WHEN** `stage_id` is `S3`
- **THEN** the report shows the capability outline, learning units, atomic nodes, unit-to-node mappings, typed graph edges, assessments, mastery thresholds, and traceability and provides both a relationship view and an adjacency-table equivalent

#### Scenario: S4 learner frontier
- **WHEN** `stage_id` is `S4`
- **THEN** the report shows node states, learning frontier, misconceptions, capability gaps, transfer performance, diagnosis evidence, and retest items and supports state and evidence-validity filtering

#### Scenario: S5 learning and session plan
- **WHEN** `stage_id` is `S5`
- **THEN** the report shows ordered learning nodes, sessions, assessment schedule, review anchors, risks, alternative routes, exit criteria, and confirmation state and can export a plan confirmation draft

#### Scenario: S6 instructional interaction
- **WHEN** `stage_id` is `S6`
- **THEN** the report shows the current node, explanations, positive and negative examples, activities, progressive hint ladder, feedback rules, interaction trace, candidate evidence, and content quality and can export an unsubmitted interaction event draft

#### Scenario: S7 mastery and replanning
- **WHEN** `stage_id` is `S7`
- **THEN** the report shows multidimensional mastery evidence, attribution, learner model changes, route rationale, review or retest plan, and applicability limits and can export a mastery review draft

### Requirement: Search, filter, detail, and raw data behavior
The report SHALL provide non-destructive search and filtering, visible result counts, on-demand entity details, an explicit empty or unknown representation, and a formatted raw JSON view.

#### Scenario: Clear filters
- **WHEN** the user clears search and filter controls
- **THEN** the complete original in-memory collection is restored without changing the source JSON

#### Scenario: Missing value
- **WHEN** an optional field is absent, null, or empty
- **THEN** the report displays an explicit missing or unavailable state and does not invent a value

#### Scenario: Raw JSON
- **WHEN** the user opens the raw JSON tab
- **THEN** the complete currently loaded envelope is available as inert formatted text and cannot be saved back over the source file

### Requirement: Constrained draft export
Every editable report interaction SHALL export only a versioned local draft containing authority, stage, run, action type, creation time, and explicit user payload.

#### Scenario: Export warning and content
- **WHEN** the user exports a draft
- **THEN** the page warns that the file is not canonical evidence and downloads a JSON object whose `authority` is `unsubmitted_user_draft`

#### Scenario: Sensitive source data is not copied implicitly
- **WHEN** the draft is created
- **THEN** it contains only identifiers required for routing and values explicitly entered or selected by the user, not an automatic copy of the source envelope

### Requirement: Business status and presentation status remain independent
HTML generation and validation SHALL NOT rewrite a stage business status, positive artifact, confirmation state, quality decision, or next-stage route.

#### Scenario: Blocked stage is visualized
- **WHEN** the handoff status is `blocked` and `positive_artifact` is null
- **THEN** the report renders the input gaps, evidence, quality result, and route with nullable positive-artifact source metadata

#### Scenario: HTML fails after stage success
- **WHEN** the stage business result succeeds but HTML generation fails
- **THEN** the stage business result remains unchanged and the task reports the presentation artifact failure separately

### Requirement: Verifiable implementation
The implementation SHALL provide reproducible evidence for OpenSpec validation, JSON Schema validation, template parity, HTML parsing, static security inspection, stage routing, and browser interactions, and SHALL identify every unrun gate.

#### Scenario: Required automated acceptance
- **WHEN** implementation is submitted as complete
- **THEN** strict OpenSpec validation, seven-stage route smoke, successful local-file loading, invalid-file recovery, keyboard tabs, filtering, details, and draft download checks have passed

#### Scenario: State variants
- **WHEN** browser acceptance is executed
- **THEN** at least one successful, one needs-confirmation, and one blocked handoff have been rendered and checked

#### Scenario: Manual accessibility gate is not run
- **WHEN** no real screen-reader or other assistive-technology session was performed
- **THEN** the final evidence explicitly states that the manual accessibility gate was not run
