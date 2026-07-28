#!/usr/bin/env python3
"""S1 run-folder cross-file ID/link validator (contract §14).

Scope: verification artifact for change `migrate-s1-to-llm-wiki-delivery` task 18.
This is NOT the eval-harness extension (task 22) — it is a one-off structural
checker that every stable ID referenced across the run-folder files resolves.

Usage: validate-run-folder.py <run-folder-dir>
"""
import json
import os
import re
import sys

S = re.compile(r"S\d{3}")
CAP = re.compile(r"CAP-\d{3}")
TERM = re.compile(r"TERM-\d{3}")

EXPECTED_FILES = [
    "INDEX.md", "sources.jsonl", "evidence_table.md", "coverage.md",
    "capabilities.jsonl", "terminology.jsonl", "goal-contract.md",
    "research-brief.md", "confirmation.md", "g1-evaluation.md", "verification.md",
]


def load_jsonl(path):
    rows, errs = [], []
    with open(path, encoding="utf-8") as fh:
        for i, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                errs.append(f"{os.path.basename(path)}:{i} JSON parse error: {e}")
    return rows, errs


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else "."
    problems = []
    notes = []

    # --- existence ---------------------------------------------------------
    missing = [f for f in EXPECTED_FILES if not os.path.exists(os.path.join(d, f))]
    if missing:
        problems.append(f"missing expected files: {missing}")

    # --- JSONL parse + id sets --------------------------------------------
    src_rows, e = load_jsonl(os.path.join(d, "sources.jsonl")); problems += e
    cap_rows, e = load_jsonl(os.path.join(d, "capabilities.jsonl")); problems += e
    term_rows, e = load_jsonl(os.path.join(d, "terminology.jsonl")); problems += e

    src_ids = {r["source_id"] for r in src_rows}
    cap_ids = {r["capability_id"] for r in cap_rows}
    term_ids = {r["term_id"] for r in term_rows}
    notes.append(f"sources={len(src_ids)} capabilities={len(cap_ids)} terms={len(term_ids)}")

    # --- internal JSONL source refs ---------------------------------------
    for r in cap_rows:
        for sid in r.get("source_ids", []):
            if sid not in src_ids:
                problems.append(f"capabilities.jsonl {r['capability_id']} -> orphan source {sid}")
    for r in term_rows:
        for sid in r.get("evidence_refs", []):
            if sid not in src_ids:
                problems.append(f"terminology.jsonl {r['term_id']} -> orphan source {sid}")

    # --- markdown reference resolution ------------------------------------
    def refs(path, patterns):
        if not os.path.exists(path):
            return {}
        txt = open(path, encoding="utf-8").read()
        out = {}
        for name, pat in patterns.items():
            out[name] = set(pat.findall(txt))
        return out

    et = refs(os.path.join(d, "evidence_table.md"), {"S": S, "CAP": CAP, "TERM": TERM})
    cv = refs(os.path.join(d, "coverage.md"), {"S": S})
    gc = refs(os.path.join(d, "goal-contract.md"), {"S": S, "CAP": CAP, "TERM": TERM})
    g1 = refs(os.path.join(d, "g1-evaluation.md"), {"S": S, "CAP": CAP, "TERM": TERM})

    def check(label, found, valid):
        bad = sorted(found - valid)
        if bad:
            problems.append(f"{label}: orphan refs {bad}")

    check("evidence_table.md S", et.get("S", set()), src_ids)
    check("evidence_table.md CAP", et.get("CAP", set()), cap_ids)
    check("evidence_table.md TERM", et.get("TERM", set()), term_ids)
    check("coverage.md S", cv.get("S", set()), src_ids)
    check("goal-contract.md S", gc.get("S", set()), src_ids)
    check("goal-contract.md CAP", gc.get("CAP", set()), cap_ids)
    check("goal-contract.md TERM", gc.get("TERM", set()), term_ids)
    check("g1-evaluation.md S", g1.get("S", set()), src_ids)
    check("g1-evaluation.md CAP", g1.get("CAP", set()), cap_ids)
    check("g1-evaluation.md TERM", g1.get("TERM", set()), term_ids)

    # --- INDEX.md file list vs actual -------------------------------------
    idx_path = os.path.join(d, "INDEX.md")
    if os.path.exists(idx_path):
        idx_txt = open(idx_path, encoding="utf-8").read()
        listed = set(f for f in EXPECTED_FILES if f != "INDEX.md" and re.search(rf"`?{re.escape(f)}`?", idx_txt))
        actual_content = set(f for f in os.listdir(d) if f != "INDEX.md" and not f.startswith("."))
        unlisted = sorted(actual_content - listed - {f for f in actual_content if f not in EXPECTED_FILES})
        ghost = sorted(listed - actual_content)
        # only flag expected content files
        unlisted_expected = sorted((actual_content & set(EXPECTED_FILES)) - listed)
        if unlisted_expected:
            problems.append(f"INDEX.md does not list actual content files: {unlisted_expected}")
        if ghost:
            problems.append(f"INDEX.md lists non-existent files: {ghost}")
        notes.append(f"INDEX.md lists {len(listed)} content files; actual content files={len(actual_content & set(EXPECTED_FILES))}")

    # --- verification.md self-consistency ---------------------------------
    ver_path = os.path.join(d, "verification.md")
    if os.path.exists(ver_path) and src_rows:
        ver = open(ver_path, encoding="utf-8").read()
        accepted = len([r for r in src_rows if r.get("status") == "accepted"])
        ext = len([r for r in src_rows if r.get("status") == "accepted" and r.get("provenance") == "external_evidence"])
        m = re.search(r"accepted:\s*(\d+)", ver)
        me = re.search(r"accepted_external_evidence:\s*(\d+)", ver)
        if m and int(m.group(1)) != accepted:
            problems.append(f"verification.md accepted={m.group(1)} but actual={accepted}")
        if me and int(me.group(1)) != ext:
            problems.append(f"verification.md accepted_external_evidence={me.group(1)} but actual={ext}")
        notes.append(f"sources accepted={accepted} external_evidence={ext}")

    print("RUN-FOLDER:", os.path.abspath(d))
    for n in notes:
        print("  note:", n)
    if problems:
        print("RESULT: FAIL")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("RESULT: PASS — all cross-file IDs/links resolve, JSONL parses, INDEX matches actual files.")


if __name__ == "__main__":
    main()
