# Plan 1 — Quick wins: richer findings + SAP vs us

Goal: a reader can see what the report literally says vs what the AI concluded, how confident it is, what SAP itself rated, and which sections are verified healthy. Old saved analyses must keep loading.

Words: "payload" = saved `{base}_workbook_payload.json`. "Pure function" = inputs in, outputs out, no AI or storage.

## Facts this plan relies on (verified 2026-10-27)

- Tests: from `backend/`, `python -m pytest -q tests` (77 passed). Pattern for end-to-end with fake AI: `tests/test_grouped_web_pipeline.py`.
- Two HTML shapes:
  - Word "Save as HTML" (`samples/COREX_TP1_05_2026_files_html/COREX_TP1_05_2026.htm`): numbered headings; ratings `<span data-rating="red">[RED]</span>`; cover page is images only (no SID/installation/period text).
  - Word 2003 XML `.doc` (real upload path; `samples/compare/lo_test/BSW_S4P_05_2026.xml`): unnumbered headings; bare `[RED]`; first table row becomes `<th>`; cover text survives as one flattened paragraph in a tree node titled "Overview" (`html_tree_builder.py` ~70-83).
- Service Summary: `<p>Alert Overview</p>` + table; `<p>Check Overview</p>` + 4-col table (Topic Rating / Topic / Subtopic Rating / Subtopic).
  - COREX: 11 alerts (4 RED, 7 YELLOW); 8 topics (1R/3Y/4G); 38 subtopics (4R/10Y/24G).
  - BSW: 10 alerts (4R/6Y); 12 topics (1R/8Y/3G); 55 subtopics (3R/15Y/37G).
- Title matching SAP check → section (strip leading numbers, one trailing ` *`, SID; lowercase): unmatched 14/46 (COREX), 14/67 (BSW).
- Landscape: product/release/DB in both samples; role + installation number only in BSW "Transport Landscape". Period fallback: Hardware Capacity "Analysis Start/End".
- Upload form already stores blob metadata `customer_name, system_id, start_date, report_date` (`routers/storage_router.py` ~245-252).
- Excel Exec Summary uses `COUNTA(sheet!A3:A9999)` / `COUNTIF(sheet!B3:B9999,…)` → **section sheets must keep ID in col A, Severity in col B; add columns at the end only.**
- Section and finding IDs are counters → not usable across runs.
- Analysts receive their job via `route_sections` (`Send`); they don't see shared state.
- Cross-reference and synthesis dump full findings → any new field costs input tokens twice.
- Do not reuse `samples/extract_alert_overview.py` / `clean_alert_overview.py` (raw XML, lose colours).

## Steps

### 1.1 Add optional fields to each finding — tier-sonnet
- **Files:** `backend/ewa_pipeline/report/schemas.py`, new `backend/tests/test_schema_compat.py`.
- **Change:** add to `Finding`, each with `Field(description=...)` (descriptions guide the AI):
  - `confidence: Literal["High","Medium","Low"] | None = None`
  - `confidence_reason: str = ""`
  - `to_confirm: str = ""` (one concrete check)
  - `risk_types: list[Literal["Security","Availability","Performance","Compliance","Cost","Data integrity","Supportability","Operations"]] = []` (1–2, main first)
  - `subject: str = ""` (exact object from report: SQL hash, user, parameter, client, host, component)
  - `due_date: str = ""` (YYYY-MM-DD, only if report states a date)
- **Verify:** test loads a payload dict without the new fields into `AnalysisResult`, checks defaults; full pytest green.
- **Risk:** AI starts filling fields right away from descriptions — fine. Rollback = revert.

### 1.2 Prompt rules for the new fields — tier-sonnet
- **Files:** `agents/prompts.py`, `agents/orchestrator.py`.
- **Change:** `<finding_fields>` block in `DOMAIN_ANALYST_PROMPT` and `GROUPED_DOMAIN_ANALYST_PROMPT`:
  - `evidence` = verbatim quote(s) with values, units, rating icon. `description` = interpretation only.
  - Confidence: High = report's own rating/explicit value; Medium = values + skill thresholds; Low = heuristic/incomplete.
  - `to_confirm`, `risk_types`, `subject`, `due_date` as in 1.1.
  - In `cross_reference` and `synthesize`, dump findings **without** `confidence_reason`, `to_confirm`, `due_date`.
- **Verify:** pytest green; one live run on a sample — evidence quotes the report, `subject` holds e.g. SQL hash. Compare finding counts before/after.
- **Cost:** ~+80–120 output tokens/finding (~+4–8k/run); ~+250 input tokens per analyst call.

### 1.3 Excel: "All Findings" tab + new columns — tier-sonnet
- **Files:** `report/excel_generator.py`, new `tests/test_excel_generator.py`.
- **Change:**
  - New sheet "All Findings" right after Executive Summary (reserve in `used`). Columns: Finding ID, Section, Severity, Risk Type, Title, Observed (from report), Interpretation, Confidence, Why this confidence, To confirm, Impact, Action, Transactions, Effort, Priority, Due date, External Validation. Sort by severity, then section order.
  - Section sheets: rename headers Evidence → "Observed (from report)", Description → "Interpretation"; append Confidence, Risk Type, To confirm **at the end**.
  - Keep all existing tabs.
- **Verify:** test with one old-style + one new-style finding: All Findings has 2 rows; section sheet B3 is a severity; Exec Summary formulas still reference col B.

### 1.4 Read SAP's Service Summary (no AI) — tier-sonnet
- **Files:** new `backend/ewa_pipeline/indexer/sap_summary.py`; `schemas.py` (`SapAlert(rating, text)`, `SapCheck(topic, subtopic, rating, raw_title)`, `SapServiceSummary(alerts, checks)`); new `tests/test_sap_summary.py`.
- **Change:** `extract_service_summary(compact_html) -> SapServiceSummary`:
  - Find first `p/td/th/strong` with text exactly "Alert Overview" → next `<table>`. Per row (`td` and `th`): rating = first cell matching `\[(RED|YELLOW|GREEN|…)\]`; text = last non-empty cell.
  - "Check Overview": skip row with "Topic Rating". Cell 1 non-empty → topic row (rating cell 0). Cell 3 non-empty → subtopic of current topic (rating cell 2).
  - Strip only one trailing `" *"`. Missing → empty lists, never raise.
- **Verify:** unit tests on inline snippets of both shapes; integration tests on both samples hitting the counts above (skip if sample missing). BSW: copy the `.xml` to a temp `.doc`, run `convert_doc_to_html` + `convert_html_to_compact_html`. COREX: `convert_html_to_compact_html` on the `.htm`.

### 1.5 System profile parser (start of the ID card) — tier-sonnet
- **Files:** new `backend/ewa_pipeline/indexer/system_profile.py`; `schemas.py` (`SystemProfile`); new `tests/test_system_profile.py`.
- **Fields:** `sid, installation_number, session_number, product, product_version, database, database_version, db_id, os, system_role, period_start, period_end, sources: dict[str,str]`.
- **Sources in priority order:**
  - (a) Cover paragraph: SID `Alert Service Report\s+([A-Z][A-Z0-9]{2})\b`; status word Productive|Production|Test|Development|Quality → role; `Installation No\.\s+(\d{10,})\s+(\d{10})` → second number; last two `dd.mm.yyyy` before "EarlyWatch" → period.
  - (b) Landscape tables by header name (Product/Version; Database System/Version/DB ID; Host Overview OS; Transport Landscape row for SID → role + installation number).
  - (c) Hardware Capacity Analysis Start/End → period.
  - (d) Headings "… for TP1" → most common 3-char SID. Missing stays "".
- **Verify:** BSW → S4P, 0021220331, Production, SAP S/4HANA 2023, HANA 2.00.079.05, H4P, 2026-04-27..2026-05-03. COREX → TP1, no installation, no role, SAP NetWeaver 7.4, HANA 2.00.088.00, 2026-04-27..2026-05-03.

### 1.6 Give every analyst the profile; save profile + SAP summary in the result — tier-sonnet
- **Files:** `agents/orchestrator.py`, `agents/runner.py`, `services/pipeline.py`, `report/schemas.py`, `agents/prompts.py`.
- **Change:**
  - `AnalysisResult.system_profile: SystemProfile | None = None`, `sap_summary: SapServiceSummary | None = None`.
  - `run_pipeline` reads the compact HTML (`_prepare_doc_input` / `_prepare_html_input` return the path used); calls 1.4 + 1.5; passes a short profile text (<600 chars) into `run_analysis` → `EwaAnalysisState["system_profile"]` → each job in `route_sections`.
  - Insert `<system_profile>…</system_profile>` after `<objective>` in both analyst prompts. Rule: "Use role to judge exposure. If role is empty, do not assume production."
  - Attach both objects to the result.
- **Verify:** extend `test_grouped_web_pipeline.py` so the fake analyst asserts `<system_profile>` is in its prompt.
- **Cost:** ~+150–250 input tokens per analyst call (~+5–10k input/run).

### 1.7 Reconcile with SAP (no AI) — tier-sonnet
- **Files:** new `backend/ewa_pipeline/report/reconciliation.py`; `schemas.py` (`ReconciliationRow`, `AnalysisResult.reconciliation: list[ReconciliationRow] = []`); `services/pipeline.py`; new `tests/test_reconciliation.py`.
- **Change:** `reconcile(result, sap_summary, tree, profile) -> list[ReconciliationRow]`:
  - Clean titles (as Facts; also strip SID and DB ID).
  - Our colour for a check = worst finding severity in matching section **and child sections** (D1 mapping).
  - Verdicts: Agree / We rated higher / We rated lower / Not covered (section failed/skipped, or no finding matches alert) / No detail section in report.
  - Alerts → findings by word overlap with title + evidence (Jaccard ≥ 0.3 = shared words ÷ all distinct words); keep best match + score.
  - Python-written reason: "We raised {id} ({sev}) '{title}'" / "No finding raised; section analysed" / "Section failed analysis".
  - Call in `run_pipeline` before Excel.
- **Verify:** fake result + summary + tree → one row of each verdict.
- **Risk:** reworded alerts may show "Not covered" instead of a false match — safe; 1.7b fixes.

### 1.7b (optional) AI matching for unmatched alerts — tier-sonnet
- One call on the cross-reference model: unmatched alerts + finding IDs/titles → pairs; Python keeps only real IDs. On/off flag in `ewa_pipeline/config.py`. ~3–5k in, ~1k out per run.

### 1.8 Excel: "SAP vs Us" + "Verified Healthy" tabs — tier-sonnet
- **Files:** `excel_generator.py`, `tests/test_excel_generator.py`.
- **SAP vs Us:** Source (Alert/Check), SAP Topic, SAP Item, SAP Rating, Our Section, Our Rating, Our Finding IDs, Verdict (coloured), Reason; verdict counts at top.
- **Verified Healthy:** sections with coverage = analyzed and zero findings. Columns: Section, SAP rating (if matched), Note ("SAP disagrees" when SAP is RED/YELLOW).
- Both skipped when data missing (old payloads).
- **Verify:** test checks both sheets and row counts; manual CLI `excel` on a saved result.

### 1.9 (optional) Rebuild old workbooks
- Not needed for compatibility. Covered by Plan 2 step 2.11 `--regenerate-workbooks`.
