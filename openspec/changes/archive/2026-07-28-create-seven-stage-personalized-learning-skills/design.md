## Context

The repository contains a reviewed seven-stage SOP, 21 stage-level positive/negative examples, and two end-to-end design cases. The current conclusion is `pass_with_changes`: stage boundaries are accepted, but reliable skill implementation still requires concrete schemas, confirmation and failure states, stage-specific rubrics, deterministic routes, research evidence gates, and eval proof.

The implementation is documentation-and-contract heavy rather than service code. The deliverables are seven repo-local Codex skills under `.agents/skills/`, each initialized and validated with the installed `skill-creator` utilities. The current directory is not a Git repository, so verification must rely on OpenSpec state, file/content checks, validators, eval results, and preserved external-route JSON.

## Goals / Non-Goals

**Goals:**

- Implement exactly seven independently invocable stage skills matching S1–S7.
- Make each skill fail closed on invalid upstream artifacts, missing required confirmation, absent research evidence, stale state, or insufficient mastery evidence.
- Materialize the common handoff envelope and seven artifact types as machine-checkable JSON Schemas.
- Keep stage artifact quality separate from learner mastery and make all routes auditable.
- Use the reviewed positive/negative examples as stage eval data and both end-to-end cases as integration/generalization evidence.
- Finish only after local validation, the `dclaude` comparative benchmark, and two mutually cross-checked final skill-eval session passes whose routes and actual `modelUsage` are preserved. Prefer `dclaude` plus `gclaude`; allow a fresh gclaude fallback session only under the explicit pre-inference route-failure rule.

**Non-Goals:**

- Build a live learner database, web application, search backend, or production orchestrator.
- Claim that simulated learner results, thresholds, or cases are real observations.
- Create an eighth top-level stage skill, an orchestrator skill, or shared executable scripts.
- Create a new repository validator script when installed validators and direct deterministic checks are sufficient.
- Allow user confirmation to waive required S1/S2 external evidence.
- Treat a valid YAML frontmatter check as sufficient skill eval evidence.

## Decisions

### 1. Use exactly seven stage skill folders

The skill folders will be:

1. `create-goal-success-contract`
2. `create-domain-evidence-landscape`
3. `build-capability-concept-graph`
4. `diagnose-learner-frontier`
5. `plan-learning-sessions`
6. `run-instructional-interaction`
7. `verify-mastery-and-replan`

This preserves the accepted seven-stage runtime semantics. The alternative of creating eight physical skills by splitting S7 is rejected for this change because the user explicitly requested seven stage skills. S7 instead exposes two ordered internal sections—`mastery_verification` and `learner_model_update_and_replan`—inside one atomic output contract.

### 2. Make every skill self-contained

Each folder will contain:

- `SKILL.md`
- `agents/openai.yaml`
- `references/handoff-envelope.schema.json`
- `references/<stage-artifact>.schema.json`
- `references/stage-contract.md`
- `references/example.md`
- `evals/evals.json`

The handoff schema is duplicated identically into all seven skills and checked for byte equality. This avoids an undiscoverable pseudo-skill such as `.agents/skills/_shared` and allows an individual skill folder to be copied or evaluated in isolation. The trade-off is duplication, mitigated by a final consistency check.

Eval run outputs do not live inside the skill folder. For each skill they are written to a sibling `<skill-name>-workspace/iteration-N/<eval-name>/` tree with paired `with_skill/` and `without_skill/` runs.

### 3. Use one execution shape with stage-specific semantics

Every skill will instruct the agent to run:

```text
validate input contract
→ collect requirement gaps
→ execute the stage confirmation policy
→ collect admissible evidence
→ produce the named positive artifact
→ evaluate it with the stage rubric
→ emit pass / revise_here / return_upstream and route_to
```

The common shape does not imply a universal rubric. Each stage contract defines its own evidence, thresholds, and routes. A stage SHALL not fabricate an output merely to satisfy schema shape.

### 4. Use strict, inspectable schema contracts

Schemas use JSON Schema Draft 2020-12 and require stable IDs, schema versions, run/stage identity, input validation, confirmation state, evidence, named artifact content, rubric results, verdict, route, and traceability. Unknown evidence states remain explicit (`unknown`, `evidence_insufficient`, `research_blocked`, or equivalent); missing data is not coerced to failure or success.

Every rubric result uses the same operational shape: `dimension`, `evidence[]`, numeric-or-boolean `score`, matching-type `threshold`, `passed`, and—when failed—`failure_action` plus `route_to`.

The alternative of placing example YAML only in `SKILL.md` is rejected because it cannot mechanically validate required fields, enum values, versioning, or traceability.

### 5. Fail closed on research and evidence boundaries

S1/S2 must perform live external research for a cold start, material target change, or stale critical evidence. Model knowledge is limited to hypotheses, questions, and query generation. If browsing/search is unavailable, the stage emits `research_blocked` and fails G1/G2. `not_applicable` requires a reason; an unavailable source is a `gap`, not `not_applicable`.

Evidence provenance is explicit: `model_hypothesis`, `market_signal`, `external_evidence`, `user_provided_unverified`, and `learner_behavior`. A gate cannot count `model_hypothesis` or unverified user material as external evidence.

S3–S7 likewise reject invalid, stale, or unpassed upstream artifacts instead of silently repairing upstream facts in the current stage.

### 6. Keep S7 as one versioned feedback transaction

S7 first produces a mastery claim with multidimensional evidence and attribution. It then applies a version-checked learner-model patch and chooses a deterministic route. If `expected_model_version` conflicts, it emits a conflict and performs no update. The skill documents the persistence protocol but does not pretend to provide a live database.

### 7. Preserve guarded complexity tiers

The standard semantic contract remains seven stages. Quick execution may merge S2+S3 or S4+S5 only when the SOP allow conditions hold, and merged execution must still emit both artifacts and pass both gates sequentially. Competing paradigms, materially uneven source reliability, active disagreement, emerging/high-risk use, unknown prior knowledge, conflicting learner evidence, multiple frontiers, or high-stakes placement prohibit the corresponding merge.

Rigorous and research tiers remain seven stages. A research-tier run records when independent external expert review and longitudinal delayed retesting are required; if those gates have not actually run, the output remains pending/not-executed rather than claiming research-grade completion.

### 8. Treat reviewed examples as eval inputs, not hidden answers

Each stage receives three eval definitions derived from the reviewed 21-example corpus: two positive cases and one negative/blocked case. Eval metadata records source file, section, prompt, expected behavior, and assertions. The two end-to-end cases are used to audit cross-stage handoff and cross-domain generalization.

Expected assertions are disclosed to the grader but not injected into an executor prompt. No benchmark may count merely echoing a source example as generalization.

Each `references/example.md` contains at least one concrete worked example with
input facts, abbreviated stage output, gate verdict, route, and source-section
traceability. The worked example teaches the package contract; it is not an
observed learner result and is not injected into executor prompts during eval.

The installed Claude Skill Creator contract is:

- `evals/evals.json` in each skill with `skill_name`, integer `id`, executor `prompt`, human-readable `expected_output`, optional `files`, and grader-held `expectations`;
- paired `with_skill` and `without_skill` executions for every case;
- per-eval `eval_metadata.json`, per-run `timing.json` and `grading.json`;
- per-skill `benchmark.json`, `benchmark.md`, analyzer notes, and static `review.html`.

The two integration audits exercise both complete S1→S7 chains and at least one S7→S5→S6→S7 remediation loop. Each transition checks schema compatibility, version consistency, traceability continuity, gate ownership, allowed route, and fixture labeling.

### 9. Preserve external review, fallback, and eval provenance

`dclaude` and `gclaude` requirement reviews run in non-interactive JSON mode with no session persistence and an explicit read-only `openspec-explore` stance. The comparative with-skill/without-skill benchmark uses `dclaude`. Final skill evaluation defaults to independent `dclaude` and `gclaude` sessions, then each successful session receives the other's structured findings for a cross-check.

If `dclaude` fails before model inference with a route/provider error such as 402, 429, or 5xx, has empty `modelUsage`, and produces no parseable inner verdict, the failure is retained and logged first. With the user's explicit authorization, a fresh `gclaude` session may replace that unavailable final retry. The fallback must use a distinct session and adversarial prompt, store separate outer/inner evidence, declare `fallback_for=dclaude`, and never be represented as a successful dclaude result or as provider diversity. The original successful gclaude session and fallback gclaude session must mutually cross-check structured findings and each must finish with no blocking or major finding.

Actual route identity comes from outer JSON `modelUsage`, not model self-description. Both accepted final inner results must parse as JSON and both outer/route records must have non-empty `modelUsage`. Failures and intermediate verdicts remain in the error/review records.

`quick_validate.py` checks skill structure/frontmatter only. JSON and schema syntax are checked with the installed Python `json` and `jsonschema` modules, handoff duplication with direct SHA-256 comparison, and placeholders/references with direct repository searches. No new validator script is needed for these deterministic checks.

### 10. Record errors before fixing them

The durable error ledger is `docs/chat_log/七阶段个性化学习Skill实施与评估错误记录.md`. Every material CLI, validation, schema, eval, or route failure is appended before remediation. Resolved entries retain the original symptom and add repair plus revalidation evidence.

## Risks / Trade-offs

- **[Risk] Seven self-contained folders duplicate the common schema** → Compare all seven copies during final validation and fail on drift.
- **[Risk] Skills can become verbose by copying the SOP** → Keep `SKILL.md` procedural and place detailed contracts/schemas in one-level `references/`.
- **[Risk] S1/S2 evals may be nondeterministic because current web evidence changes** → Grade evidence discipline, coverage/status recording, and blocked behavior rather than requiring frozen current facts.
- **[Risk] Example leakage can inflate eval scores** → Use source examples as fixtures/rubrics, require transformed outputs or defect detection, and keep expected assertions out of executor prompts.
- **[Risk] S7 “atomic update” could imply a backend that does not exist** → Specify a versioned protocol and require honest `not_executed`/conflict states; do not claim persistence occurred.
- **[Risk] External routes can fail or return malformed JSON** → Retain raw output and exit status, log the failure, retry the same named route when appropriate, and use another route only under the explicit user-authorized pre-inference fallback rule with honest `fallback_for` provenance.
- **[Risk] No Git metadata makes change isolation harder to prove** → Verify an explicit expected-path manifest, OpenSpec tasks/status, file content, schemas, validators, and eval artifacts.

## Migration Plan

1. Create and cross-review all OpenSpec artifacts.
2. Initialize the seven skill folders with `skill-creator/scripts/init_skill.py`.
3. Replace templates with stage instructions, references, schemas, and eval definitions.
4. Run structure, YAML/JSON, schema, placeholder, duplicate-contract, and OpenSpec validation.
5. Run all 21 cases as paired with-skill and without-skill forward tests, grade each run, aggregate seven benchmarks, and generate static viewers.
6. Run both end-to-end handoff audits; fix and re-run failures.
7. Run independent final `dclaude` and `gclaude` skill evals over the complete evidence set. If dclaude meets the documented pre-inference failure condition, preserve that failure and run a fresh labeled gclaude fallback session. Exchange the two successful sessions' structured findings, fix actionable findings, and repeat affected sessions until both structured verdicts pass.
8. Mark OpenSpec tasks complete only after their named evidence exists.

Rollback is deletion of only the seven newly created stage skill folders and the change-specific generated evidence; the source SOP and reviewed example documents are not modified. The error ledger is retained as audit history.

## Open Questions

None blocking. The installed Claude Skill Creator's eval file and workspace contract was verified directly from its `SKILL.md` and `references/schemas.md`; cross-review changes are captured before apply.
