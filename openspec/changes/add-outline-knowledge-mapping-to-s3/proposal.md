## Why

The current S3 contract models target capabilities, knowledge nodes, prerequisites, assessments, and traceability, but it does not machine-model the intermediate relationship between a human-readable capability outline and its atomic knowledge points. The standalone research note consequently recommends an eighth stage and a second structure artifact, which conflicts with the accepted seven-stage ownership model and would create two competing sources of truth.

## What Changes

- Keep exactly seven stages and make three-level capability outlining an internal S3 modeling view, not a new stage or skill.
- Extend `capability_concept_graph` with assessable learning units and typed many-to-many unit-to-node mappings.
- Separate hierarchy/containment semantics from hard/soft prerequisite semantics; display order must never imply prerequisite order.
- Add stable identity, source/goal traceability, coverage, dangling-reference, duplicate-node, and downstream version-impact rules.
- Extend G3 so hierarchy, mappings, graph, assessments, and traceability pass or fail atomically.
- Clarify that S5 may use learning units as readable grouping but must return structural or version defects to S3.
- Update the durable requirements, S3/S5 skill contracts, S3 schema, worked example, and existing three-case eval surface without creating a new script or an eighth skill.

## Capabilities

### New Capabilities

- `outline-knowledge-point-mapping`: Defines how S3 represents capability-outline levels, assessable learning units, atomic knowledge points, typed unit-to-node mappings, validation invariants, and the S5 consumption boundary.

### Modified Capabilities

None. There are no archived baseline specs under `openspec/specs/`; the completed seven-stage change remains an implementation baseline and is not reopened.

## Impact

- Requirements: `docs/chat_log/大纲-知识点关联.md` and `docs/chat_log/个性化学习SOP步骤拆分最终结论.md`.
- Primary implementation: `.agents/skills/build-capability-concept-graph/`.
- Boundary clarification: `.agents/skills/plan-learning-sessions/`.
- Validation: S3 JSON Schema/example/evals, S5 contract wording, skill structure validation, JSON/Schema fixture checks, and strict OpenSpec validation.
- Stage inventory remains exactly seven; no service, database, live learner state, or production deployment is added.
