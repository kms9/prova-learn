## 1. Shared Presentation Contract

- [x] 1.1 Upgrade the seven byte-identical handoff envelope schemas to `1.1.0` with conditional `presentation_artifact` validation
- [x] 1.2 Add a byte-identical `html-visualization-contract.md` reference to all seven Skills
- [x] 1.3 Validate generated, failed, not-requested, needs-confirmation, and blocked envelope variants against the shared schema

## 2. Offline HTML Renderer

- [x] 2.1 Build the self-contained `stage-report.html` with CSP, safe embedded JSON loading, explicit local file loading, and no remote dependencies
- [x] 2.2 Implement the common shell, accessible tabs, live status, responsive and print styles, search, filtering, details, and raw JSON
- [x] 2.3 Implement inert rendering through safe DOM and SVG APIs and add text or table alternatives for visual encodings
- [x] 2.4 Implement versioned `unsubmitted_user_draft` export without copying source envelope data implicitly

## 3. Stage-Specific Views

- [x] 3.1 Implement S1 target, capability, assessment, scope, confirmation, and confirmation-draft views
- [x] 3.2 Implement S2 research coverage, claim-source, consensus, disagreement, and evidence-gap views
- [x] 3.3 Implement S3 outline, learning-unit mapping, typed relationship graph, assessment, threshold, traceability, and adjacency views
- [x] 3.4 Implement S4 node-state, frontier, evidence, confidence, misconception, gap, and retest views
- [x] 3.5 Implement S5 route, session, assessment, review, risk, alternative-route, and confirmation-draft views
- [x] 3.6 Implement S6 lesson, example, activity, progressive hint, interaction trace, candidate evidence, and interaction-draft views
- [x] 3.7 Implement S7 mastery dimension, evidence, model difference, attribution, route, applicability, and review-draft views

## 4. Skill Integration

- [x] 4.1 Add byte-identical renderer assets to all seven Skill directories and verify their SHA-256 parity
- [x] 4.2 Update all seven `SKILL.md` files with JSON authority, HTML generation, safe embedding, failure, draft, and verification instructions
- [x] 4.3 Update stage examples or eval expectations so generated and non-generated presentation states are exercised without changing stage business semantics

## 5. Verification

- [x] 5.1 Run strict OpenSpec validation, JSON parsing, JSON Schema validation, HTML parsing, and static remote-dependency and dangerous-sink scans
- [x] 5.2 Run seven-stage browser routing checks plus successful, needs-confirmation, blocked, invalid-file, keyboard-tab, filter, detail, and draft-download interaction smoke tests
- [x] 5.3 Record reproducible verification evidence, identify unrun manual accessibility and production gates, and recalibrate every task checkbox
