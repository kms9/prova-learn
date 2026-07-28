## 1. Requirement Baseline and Cross-Review

- [x] 1.1 Establish the durable error-first ledger and inspect the non-Git workspace boundary
- [x] 1.2 Inspect the final SOP, 21 reviewed stage examples, and two end-to-end cases as the requirement/eval corpus
- [x] 1.3 Run read-only `dclaude` and `gclaude` `openspec-explore` reviews and preserve parsed JSON plus outer `modelUsage`
- [x] 1.4 Synthesize both reviews, update proposal/design/specs/tasks for accepted findings, and record rejected findings with reasons
- [x] 1.5 Pass strict OpenSpec validation after cross-review updates and capture a pre-apply file-hash baseline

## 2. Initialize Seven Skill Packages

- [x] 2.1 Initialize `create-goal-success-contract` with `skill-creator`, references, evals, and UI metadata
- [x] 2.2 Initialize `create-domain-evidence-landscape` with `skill-creator`, references, evals, and UI metadata
- [x] 2.3 Initialize `build-capability-concept-graph` with `skill-creator`, references, evals, and UI metadata
- [x] 2.4 Initialize `diagnose-learner-frontier` with `skill-creator`, references, evals, and UI metadata
- [x] 2.5 Initialize `plan-learning-sessions` with `skill-creator`, references, evals, and UI metadata
- [x] 2.6 Initialize `run-instructional-interaction` with `skill-creator`, references, evals, and UI metadata
- [x] 2.7 Initialize `verify-mastery-and-replan` with `skill-creator`, references, evals, and UI metadata

## 3. Common Contracts and Guards

- [x] 3.1 Create the Draft 2020-12 common handoff schema and place byte-identical copies in all seven skills
- [x] 3.2 Define confirmation states, operational rubric entries, evidence provenance, blocked states, traceability, and deterministic routes in every stage contract
- [x] 3.3 Implement and verify quick-tier S2+S3 and S4+S5 merge allow/deny guards while preserving both artifacts and gates
- [x] 3.4 Implement research-tier pending gates for external expert review and longitudinal delayed retesting
- [x] 3.5 Define safe missing-input, empty-evidence, stale-input, and unable-to-confirm behavior for every stage

## 4. S1-S3 Skills

- [x] 4.1 Implement S1 instructions, `goal_success_contract` schema, G1 rubric, evidence provenance, research-blocked behavior, and mandatory confirmation
- [x] 4.2 Implement S2 instructions, `domain_evidence_landscape` schema, multi-perspective research manifest, sample/gap rules, and G2 rubric
- [x] 4.3 Implement S3 instructions, `capability_concept_graph` schema, optional canonical map, graph invariants, traceability, and G3 routing

## 5. S4-S7 Skills

- [x] 5.1 Implement S4 instructions, versioned `learner_snapshot` schema, behavior-evidence diagnosis, and G4 rubric
- [x] 5.2 Implement S5 instructions, `learning_and_session_plan` schema, mandatory path confirmation, and G5 rubric
- [x] 5.3 Implement S6 instructions, `session_package_and_trace` schema, scaffolding/answer-leakage controls, and G6 rubric
- [x] 5.4 Implement S7 instructions and `mastery_and_replanning_bundle` schema with ordered verification/update, load/append/history protocol, version conflict behavior, attribution routes, and G7 rubric

## 6. Eval Definitions and Integration Audits

- [x] 6.1 Add two positive and one negative/blocked eval to each skill in Claude Skill Creator `evals/evals.json` format
- [x] 6.2 Verify all 21 evals record source file/section, executor prompt, expected output, grader-only expectations, and fixture labeling
- [x] 6.3 Verify all seven `references/example.md` files contain input facts, abbreviated artifact, gate verdict, route, and source-section traceability
- [x] 6.4 Define PostgreSQL and senior-reviewer S1→S7 audit chains with schema/version/traceability/gate/route assertions
- [x] 6.5 Define and run at least one S7→S5→S6→S7 remediation-loop audit with retained history
- [x] 6.6 Audit eval prompts for answer leakage and ensure expected assertions are not injected into executor prompts

## 7. Deterministic Local Validation

- [x] 7.1 Run `quick_validate.py` successfully for all seven skills and verify UI metadata matches each SKILL
- [x] 7.2 Parse every `openai.yaml`, eval JSON, and JSON Schema; run Draft 2020-12 schema self-checks with installed modules
- [x] 7.3 Validate representative positive, negative, blocked, and version-conflict artifacts against each stage schema
- [x] 7.4 Verify required-file inventory, no template placeholders, and all direct reference links
- [x] 7.5 Verify SHA-256 byte identity for all seven handoff schema copies
- [x] 7.6 Verify S1/S2 cannot pass without executed research evidence and S6 artifact quality cannot imply S7 mastery
- [x] 7.7 Verify the complete S7 deterministic route table, upstream-priority multi-cause rule, and model-version conflict behavior

## 8. dclaude Benchmark, Mutual Cross-Validation, and Repair

- [x] 8.1 Run all 21 cases through `dclaude` with-skill and without-skill configurations and preserve per-run outputs, timing, exit status, and outer `modelUsage`
- [x] 8.2 Grade all 42 runs to the installed `grading.json` schema and aggregate one benchmark per skill
- [x] 8.3 Generate seven non-empty static `review.html` files and record analyzer notes on discrimination, variance, time, and token trade-offs
- [x] 8.4 Run two independent final skill-eval audits across the seven benchmarks and two integration traces with parseable inner JSON and non-empty outer `modelUsage`; prefer `dclaude` + `gclaude`, but when dclaude fails before inference preserve the failure and use the explicitly authorized fresh gclaude fallback labeled `fallback_for=dclaude`
- [x] 8.5 Give each successful final audit session the other session's structured findings, record agreements/disagreements and route limitations, and log every actionable finding before fixes
- [x] 8.6 Apply accepted fixes, rerun affected local/benchmark gates and audit sessions, and repeat until both accepted structured verdicts pass with no unresolved blocking or major finding

## 9. Final Evidence Audit

- [x] 9.1 Re-run strict OpenSpec validation and confirm all task evidence exists
- [x] 9.2 Confirm exactly seven stage skill folders, synchronized contracts, 21 eval definitions, 42 graded runs, seven benchmarks/viewers, two integration cases, and both accepted final session/cross-check records with honest fallback provenance
- [x] 9.3 Close resolved error entries with revalidation evidence and keep accepted environmental limitations explicit
