## 1. Requirements and Contract Baseline

- [x] 1.1 Correct `docs/chat_log/大纲-知识点关联.md` so the outline mapping belongs to S3 rather than a new stage, and document the missing mapping/version/routing logic.
- [x] 1.2 Update `docs/chat_log/个性化学习SOP步骤拆分最终结论.md` with the S3/S5 ownership boundary and expanded G3 requirements.
- [x] 1.3 Verify the new proposal, design, and `outline-knowledge-point-mapping` spec are internally consistent and pass strict OpenSpec validation.

## 2. S3 Contract and Schema

- [x] 2.1 Update the S3 Skill workflow and fail-closed rules for capability-outline construction, atomic node reuse, typed mappings, and relation separation.
- [x] 2.2 Update the S3 stage contract with learning-unit/mapping fields, coverage and reference invariants, version impact, confirmation, and deterministic routes.
- [x] 2.3 Advance `capability-concept-graph.schema.json` to 1.1.0 and require shape-valid `learning_units` plus `unit_node_mappings`.

## 3. Examples, Evals, and S5 Boundary

- [x] 3.1 Update the S3 worked example to schema 1.1.0 with concrete learning units and many-to-many mappings that validate against the artifact schema.
- [x] 3.2 Extend the existing two positive and one negative S3 eval definitions without changing the total case count.
- [x] 3.3 Clarify in the S5 Skill and stage contract that outline units are readable groupings, graph nodes own ordering, and structural/version defects return to S3.
- [x] 3.4 Check S3/S5 `agents/openai.yaml` metadata against the updated Skill descriptions and regenerate only if stale.

## 4. Validation

- [x] 4.1 Run Skill Creator `quick_validate.py` for the changed S3 and S5 skill folders.
- [x] 4.2 Validate changed JSON files, the S3 positive worked fixture, reference integrity, exact seven-skill inventory, and unchanged 21-eval total.
- [x] 4.3 Run strict OpenSpec validation and record final status without rewriting historical evidence from completed changes.
