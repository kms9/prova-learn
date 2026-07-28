## Context

The accepted seven-stage implementation assigns stable domain/capability structure to S3 and personalized ordering to S5. S3 currently has `target_capabilities`, nested `sub_capabilities`, atomic `nodes`, prerequisite `edges`, assessments, mastery rules, remediation, and traceability, but it has no explicit assessable-learning-unit layer or unit-to-node association table. The research note fills that gap with a separate `learning_architecture` stage, which would violate the exactly-seven-stage constraint and split one G3 invariant across two artifacts.

The change is repo-local and contract-oriented. There is no live database or migration engine; version and invalidation behavior must therefore be expressed as artifact protocol and fail-closed routing.

## Goals / Non-Goals

**Goals:**

- Represent the human-readable three-level capability outline inside the existing S3 artifact.
- Make learning-unit to knowledge-node relationships explicit, typed, many-to-many, and traceable.
- Keep containment, prerequisite, and personalized ordering as separate semantics.
- Add deterministic G3 checks for coverage, dangling references, duplicates, and version impact.
- Preserve exactly seven skills and the existing three-eval-per-stage baseline.

**Non-Goals:**

- Create an eighth stage, an orchestration skill, or a second `learning_architecture` source of truth.
- Require every narrow goal to fabricate exactly three populated hierarchy levels.
- Encode session-specific `introduce`, `reinforce`, or `review` order in S3.
- Rewrite historical evidence from the completed seven-stage change.
- Add a new validation script, service, database, or learner-state migration.

## Decisions

### 1. Extend the S3 artifact instead of creating another stage artifact

`capability_concept_graph` remains the only machine-actionable S3 structure. `target_capabilities` are level 1, their `sub_capabilities` are level 2, new `learning_units` are level 3, and existing typed `nodes` are atomic knowledge points. A narrow target may attach a learning unit directly to a target capability by declaring `parent_level=target_capability`.

Alternative rejected: a separate `learning_architecture` artifact and gate. It duplicates target/source identity, creates cross-artifact atomicity problems, and has no independent failure owner beyond S3.

### 2. Add `learning_units` and `unit_node_mappings`

Each `learning_unit` has a stable ID, title, parent reference/level, observable outcome, goal and source references, and `scope_role=required|optional|extension`.

Each `unit_node_mapping` has `unit_id`, `node_id`, `coverage_role=core|supporting|extension`, and a rationale. The table is many-to-many: one unit may need multiple nodes and a cross-cutting node may support multiple units.

Alternative rejected: nesting copied knowledge-point objects under each unit. That makes identity, diagnostic evidence, remediation, and version invalidation ambiguous when a node is reused.

### 3. Keep three relationship classes semantically separate

- Capability/sub-capability/learning-unit parent references express containment.
- `unit_node_mappings` express stable structural coverage.
- Existing `edges` express hard/soft prerequisite.

Display order is non-normative. Session roles and personalized order remain in S5/S6.

### 4. Make the extension a schema-versioned contract change

The S3 artifact schema advances from `1.0.0` to `1.1.0`; `learning_units` and `unit_node_mappings` are required for positive artifacts. Historical 1.0.0 fixtures remain evidence of the completed prior change but are not claimed compatible with new S3 output.

Semantic changes produce a new artifact ID/version in the surrounding handoff protocol and record invalidated S4–S7 scope. Label-only changes may retain entity IDs; semantic replacements must not silently inherit old learner evidence.

### 5. Add cross-field G3 invariants in prose and eval assertions

JSON Schema validates field shape, enums, and required values. The S3 contract and G3 rubric validate cross-reference and semantic invariants:

- unique entity IDs and valid parent/mapping references;
- no containment cycle and no hard-prerequisite cycle;
- at least one `core` mapping per learning unit;
- every target-required node covered by at least one learning unit;
- no unexplained duplicate core node;
- unit and node traceability to S1/S2;
- display hierarchy never used as prerequisite evidence.

### 6. Keep S5 as a consumer

S5 may group a plan by `learning_unit`, but it orders atomic nodes from the accepted graph and learner frontier. It returns version, mapping, granularity, or prerequisite defects to S3 and must not repair them locally.

### 7. Preserve the existing eval count

The two positive S3 cases gain outline/mapping expectations, and the existing negative directory case must also fail when it lacks assessable learning units and valid mappings. No fourth S3 eval is added, preserving the 21-case seven-stage baseline.

## Risks / Trade-offs

- **[Risk] Requiring learning units adds ceremony for narrow goals** → Allow direct attachment to a target capability with an explicit omitted-level rationale in the processing record.
- **[Risk] Schema cannot enforce all cross-reference invariants** → Put them in the G3 rubric and machine-checkable eval expectations; validate a concrete positive fixture separately.
- **[Risk] Schema 1.1.0 makes old outputs stale** → Keep historical evidence immutable and require downstream version compatibility checks for new runs.
- **[Risk] Human-readable outline order may still be mistaken for a path** → Repeat the separation in S3 and S5 Skill instructions and include it in the negative eval expectations.
- **[Risk] Duplicate data between unit and node traceability can drift** → Require unit source/goal refs for outline provenance and retain node-level `traceability` for diagnosis/assessment provenance; G3 checks their consistency.

## Migration Plan

1. Update durable requirement documents and add the new OpenSpec capability.
2. Advance the S3 schema to 1.1.0 with required learning units and mappings.
3. Update S3 instructions, stage contract, worked example, and the three existing eval definitions.
4. Clarify S5 consumption and upstream return behavior without changing its artifact schema.
5. Validate skill folders, JSON syntax, the S3 worked fixture, the three eval definitions, exact stage/eval inventory, and OpenSpec strict mode.

Rollback restores only the S3/S5 skill files and requirements changed by this change; the new OpenSpec change remains as audit history. Historical evidence from the completed change is never rewritten.

## Open Questions

None blocking.
