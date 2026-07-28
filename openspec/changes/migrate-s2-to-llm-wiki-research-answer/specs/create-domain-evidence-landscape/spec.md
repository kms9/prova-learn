## MODIFIED Requirements

### Requirement: Domain evidence landscape artifact
S2 SHALL write a named `s2/` LLM Wiki stage area inside the latest G1-passed S1 run folder and SHALL use `research-answers.md` as the primary human-review artifact. S2 SHALL map every S1 `research-brief.md` priority question exactly once to a stable question and answer identifier, and every answer SHALL preserve its conclusion, answer status, claim status, knowledge status, scope boundary, supporting evidence, counterevidence or alternative explanation, observable relevance, confidence, gaps, and downstream impact. S2 SHALL NOT emit a standalone handoff JSON envelope or HTML report.

#### Scenario: S1 priority questions are available
- **WHEN** S2 consumes a G1-passed run folder whose `research-brief.md` contains priority questions
- **THEN** `s2/research-answers.md` answers each question in source order with one stable `RQ-###` and `ANS-###` mapping and no silent omission

#### Scenario: A question cannot be fully answered
- **WHEN** admissible evidence is missing, conflicting, stale, or not applicable to the confirmed scope
- **THEN** S2 records the answer as `partial` or `unanswered`, preserves the evidence gap and recovery action, and does not fabricate a complete conclusion

#### Scenario: S2 output is inspected
- **WHEN** the current S2 stage area is audited
- **THEN** it contains the nine fixed files `INDEX.md`, `research-log.md`, `sources.jsonl`, `coverage.md`, `evidence-items.jsonl`, `research-answers.md`, `answer-validation.md`, `g2-evaluation.md`, and `verification.md`, with no standalone envelope JSON, HTML, or image asset

### Requirement: G2 quality gate
S2 SHALL check actual network execution, source coverage and reliability, traceability, perspective diversity, follow-up depth, sample independence, timeliness, region fit, fact/market/inference separation, disagreement balance, gap transparency, structural saturation, maturity, and per-answer multidimensional validation. Each answer SHALL be evaluated on source coverage, provenance separation, source independence, reliability/authority, timeliness/region fit, contradiction balance, observable relevance, and boundary/gap clarity.

#### Scenario: Every critical S1 question is adequately answered
- **WHEN** the S2 nine-file stage area passes cross-file validation, every critical answer passes all eight validation dimensions, six-source coverage and saturation are sufficient, maturity is at least `L1_landscape`, and no blocking gap remains
- **THEN** `g2-evaluation.md` records all dimensions passed, `verdict=pass`, and `route_to=S3`

#### Scenario: One critical answer lacks multidimensional support
- **WHEN** a critical S1 question fails one or more material answer-validation dimensions
- **THEN** G2 emits `revise_here`, routes to S2, and identifies the exact question, failed dimension, missing evidence, and recovery query or action

### Requirement: S2 eval coverage
S2 evals SHALL cover a G1-passed technical run folder, a G1-passed learning-domain run folder that preserves evidence boundaries, and an unsupported or invalid-input case. Evals SHALL assert the nine-file S2 stage area, complete S1-question mapping, per-answer eight-dimensional validation, root-index update behavior, and fail-closed G2 routing.

#### Scenario: S2 eval definitions are present
- **WHEN** the S2 eval file is inspected
- **THEN** it contains two positive and one negative case whose expected outputs use the S2 run-folder contract and do not require a standalone JSON envelope or HTML report

## ADDED Requirements

### Requirement: S2 LLM Wiki index integration
S2 MUST update the existing run root `INDEX.md` by adding or updating a distinct S2 stage entry that points to `s2/INDEX.md` and records S2 status, G2 verdict, route, and last verification time. The update MUST preserve S1 content and G1 history.

#### Scenario: S1 root index exists
- **WHEN** S2 writes or refreshes its stage area for the same confirmed goal run
- **THEN** the root index contains separate S1 and S2 stage entries and the S2 entry resolves to the current `s2/INDEX.md`

#### Scenario: S2 is blocked
- **WHEN** online research, required evidence, or escalated confirmation is unavailable
- **THEN** the root index labels S2 as blocked or pending, points to the diagnostic S2 stage area, and leaves the S1/G1 entry unchanged

### Requirement: S1-question multidimensional answer validation
S2 MUST maintain `answer-validation.md` with one validation record per S1 answer and one result for each of the eight required dimensions. Every result MUST identify evidence references, pass/fail or insufficient status, rationale, confidence impact, and a deterministic recovery action when not passed.

#### Scenario: Market evidence conflicts with an official standard
- **WHEN** a question has current market signals that conflict with normative or primary evidence
- **THEN** provenance separation and contradiction balance preserve both sides, prevent false consensus, and condition the answer on its applicable context

#### Scenario: A copied source chain inflates apparent support
- **WHEN** multiple pages trace to one underlying source
- **THEN** source-independence validation counts the chain as one independent source and lowers confidence or blocks the answer when the sample gate is not met
