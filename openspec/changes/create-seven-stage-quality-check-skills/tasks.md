## 1. Shared checker foundation

- [x] 1.1 Author the shared `quality-check-result` JSON Schema (Draft 2020-12) and copy it byte-identically into the S1 checker; lock the canonical copy under this change's evidence
- [x] 1.2 Confirm the seven stage skills are complete and their handoff + artifact schemas are stable inputs (all seven artifact schemas conform to the canonical wrapper pattern; all handoff copies SHA-256 byte-identical; every stage example validates against its artifact schema)

## 2. Implement the seven quality-check skills

- [x] 2.1 Implement `check-goal-success-contract` (S1/G1) gold reference: SKILL.md, agents/openai.yaml, references/check-rubric.md, references/quality-check-result.schema.json, references/example.md, evals/evals.json
- [x] 2.2 Implement `check-domain-evidence-landscape` (S2/G2)
- [x] 2.3 Implement `check-capability-concept-graph` (S3/G3)
- [x] 2.4 Implement `check-learner-frontier` (S4/G4)
- [x] 2.5 Implement `check-learning-sessions` (S5/G5)
- [x] 2.6 Implement `check-instructional-interaction` (S6/G6)
- [x] 2.7 Implement `check-mastery-and-replan` (S7/G7)

## 3. Validate and close

- [x] 3.1 Validate JSON, schemas (Draft 2020-12), byte-identical `quality-check-result` copies (SHA-256 unique across 7), example results vs schema, and `openspec validate` for this change (all green)
- [x] 3.2 Requirement-by-requirement completion audit: independent-verdict, shared schema, per-stage rubric, structural fail-closed, blocking-state preservation, read-only, and eval-traceability requirements all satisfied; no unresolved failures (stage-skill drift/errors tracked in the stage change's error ledger, e.g. ERR-020)
