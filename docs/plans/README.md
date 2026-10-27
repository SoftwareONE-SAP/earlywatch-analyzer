# EWA Analyzer — output improvement plans

Three plans, built **one small step at a time**. Each step = one commit, reviewed before the next.

| Plan | File | Status |
|---|---|---|
| 1. Quick wins: richer findings + SAP vs us | [01-quick-wins.md](01-quick-wins.md) | In progress (step 1.1) |
| 2. Run-over-run comparison | [02-run-comparison.md](02-run-comparison.md) | After Plan 1 |
| 3. Fleet view | [03-fleet-view.md](03-fleet-view.md) | Parked |

## Overall approach

**Python reads the facts, AI interprets, Python compares.**

- SAP's own ratings, the system ID card and landscape are read by plain Python parsers (no AI, no invented values).
- The AI only adds a few short fields per finding.
- Run comparison is a plain Python function over saved JSON, plus a small rebuildable history file per system.

Rejected alternatives: AI extraction of SAP ratings/ID (costly, can invent); re-running AI on old reports to compare (expensive, drifts); new "observed"/"interpretation" text fields (duplicates `evidence`/`description`).

## Order and dependencies

1.1 → 1.2 → 1.3 → 1.4 → 1.5 → 1.6 → 1.7 → 1.8 → (1.7b optional) → 2.1 … 2.12 → 3.1 … 3.3

- Plan 2 needs Plan 1 steps 1.1/1.2 (`subject` field), 1.5 (system profile = start of the ID card); benefits from 1.3 (All Findings tab).
- Plan 3 needs Plan 2 steps 2.1, 2.6, 2.8, 2.11 and Plan 1 steps 1.4, 1.1/1.2.

## Decisions (recommendation in brackets) — all accepted as recommended on 2026-10-27

- **D1** Colour mapping of our severity to SAP colours. [Critical/High = RED, Medium = YELLOW, Low/none = GREEN]
- **D2** Keep existing Excel tabs, add "All Findings". [Yes; revisit Remediation Plan later]
- **D3** Observed / Interpretation: reuse `evidence` / `description`. [Reuse]
- **D4** Risk types: Security, Availability, Performance, Compliance, Cost, Data integrity, Supportability, Operations; up to 2 per finding. [Yes]
- **D5** System role when the report has none (e.g. COREX). [Show "Unknown"; tell AI not to assume production; maybe a role dropdown on upload later]
- **D6** Severity went down between runs. [Recurring with note "severity lowered"]
- **D7** System identity without installation number. [SID + customer name, with warning]
- **D8** AI fallbacks (1.7b, 2.10). [Build after rule-based versions]
- **D9** Rebuild old workbooks via backfill script. [Yes]
- **D10** Fleet access across customers. [Filter by customer from the start — security-sensitive]

## Verification for every step

1. In a terminal at `C:\GenAI\earlywatch-analyzer\backend`: `python -m pytest -q tests` — all green (baseline 2026-10-27: 77 passed).
2. Parser steps: integration tests must hit the exact counts in [01-quick-wins.md](01-quick-wins.md) "Facts".
3. Excel steps: Executive Summary Critical/High counts still match section tabs (no `0` or `#REF!`).
4. Old-data check: `python -m ewa_pipeline excel --result <payload.json> --tree <tree.json> --output out.xlsx` still works on an existing payload.

## Risks and unknowns

1. Binary `.doc` via LibreOffice: cover text survival not tested; ID card falls back to landscape / hardware / upload form.
2. Other EWA versions/languages may change labels; parsers return empty, never break the run.
3. Chat cost: `routers/chat_router.py` pastes the whole payload into every chat prompt; new data may add ~20–40%. Consider excluding `reconciliation` and `comparison` from chat context.
4. First comparison against old analyses will be noisy (no `subject` field).
5. Trailing `*` in Check Overview probably means "details not in report" — unverified; only strip one trailing ` *` (`SAP*` is a real user name).
6. Sections SAP only prints on problems (e.g. "Kernel out of date") show as "Not checked", not "Fixed" — cautious by design.
7. Concurrent analyses of one system could clash on history; ETag check + rebuildable history cover it.
8. Token estimates are reasoned, not measured (no live run possible). Compare the Token Usage tab before/after 1.2 and 1.6.
