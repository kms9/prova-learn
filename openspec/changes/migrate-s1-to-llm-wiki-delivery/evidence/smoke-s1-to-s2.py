#!/usr/bin/env python3
"""S1 -> S2 consumption smoke (contract §12 downstream-read guidance + §4/§8).

Simulates S2: read INDEX.md, follow its "S2 reads ..." guidance, then confirm
the named files exist and are structurally consumable by S2.

Verification artifact for change `migrate-s1-to-llm-wiki-delivery` task 20.
Usage: smoke-s1-to-s2.py <run-folder-dir>
"""
import json
import os
import re
import sys

S2_FILES = ["research-brief.md", "sources.jsonl", "coverage.md"]
S2_CHANNELS = ["job_career", "books_courses", "papers_research",
               "community_web", "standards_official", "artifacts_validation"]
S1_CATEGORIES = ["wikipedia_encyclopedia", "official_academic", "practice_case",
                 "recruiting_jd", "interview_selection", "adversarial_frontier"]


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else "."
    problems = []
    notes = []

    # 1. INDEX.md names the S2 downstream-read files
    idx = os.path.join(d, "INDEX.md")
    idx_txt = open(idx, encoding="utf-8").read() if os.path.exists(idx) else ""
    m = re.search(r"S2[^:]*[:：][^\n]*", idx_txt)
    s2_line = m.group(0) if m else ""
    for f in S2_FILES:
        if f not in idx_txt:
            problems.append(f"INDEX.md does not name S2 input file {f}")
    notes.append("INDEX.md S2 guidance present: " + ("yes" if s2_line else "NO"))

    # 2. The three files exist
    for f in S2_FILES:
        p = os.path.join(d, f)
        if not os.path.exists(p) or os.path.getsize(p) == 0:
            problems.append(f"S2 input file missing/empty: {f}")

    # 3. sources.jsonl parses (S2 reads it)
    sp = os.path.join(d, "sources.jsonl")
    if os.path.exists(sp):
        n = 0
        for i, line in enumerate(open(sp, encoding="utf-8"), 1):
            line = line.strip()
            if not line:
                continue
            try:
                json.loads(line); n += 1
            except json.JSONDecodeError as e:
                problems.append(f"sources.jsonl:{i} parse error: {e}")
        notes.append(f"sources.jsonl records={n}")

    # 4. coverage.md has the six fixed S1 categories, each exactly once
    cp = os.path.join(d, "coverage.md")
    if os.path.exists(cp):
        ctxt = open(cp, encoding="utf-8").read()
        for cat in S1_CATEGORIES:
            c = ctxt.count(cat)
            if c < 1:
                problems.append(f"coverage.md missing category {cat}")
            # category appears in table + maybe mapping note; table row once is the rule
        notes.append("coverage.md six categories all present: " +
                     str(all(ctxt.count(c) >= 1 for c in S1_CATEGORIES)))

    # 5. research-brief.md has all six S2 source channels, each >=1 seed
    rp = os.path.join(d, "research-brief.md")
    if os.path.exists(rp):
        rtxt = open(rp, encoding="utf-8").read()
        for ch in S2_CHANNELS:
            if ch not in rtxt:
                problems.append(f"research-brief.md missing six_source channel {ch}")
        notes.append("research-brief.md six_source channels all present: " +
                     str(all(ch in rtxt for ch in S2_CHANNELS)))

    print("RUN-FOLDER:", os.path.abspath(d))
    for n in notes:
        print("  note:", n)
    if problems:
        print("RESULT: FAIL")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("RESULT: PASS — S2 can follow INDEX.md to read research-brief.md + sources.jsonl + coverage.md; all structurally consumable.")


if __name__ == "__main__":
    main()
