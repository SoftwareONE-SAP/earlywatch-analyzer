# Plan 2 — Run-over-run comparison

Goal: for each system, show what is New, Recurring, Fixed, Worse or Not checked since the previous report, and how long each issue has been open.

**Compares against:** the previous **saved analysis JSON** of the **same system** (same ID card), chosen by latest earlier *report period* — not upload date. No AI re-run.

**Needs from Plan 1:** 1.1/1.2 (`subject`), 1.5 (system profile). Benefits from 1.3 (All Findings tab).

## Facts this plan relies on (verified 2026-10-27)

- Blobs keyed by filename base `{SID}_{DD}_{Mon}_{YY}` built from the user-typed end date → re-uploading same SID + end date overwrites.
- `workflow_orchestrator.py` downloads `{base}.html`, runs `run_pipeline`, uploads `_workbook.xlsx`, `_workbook_payload.json`, `_v2_usage.json`. Tree is **not** uploaded on this path.
- `export_router.py` serves stored xlsx only → old analyses need workbook rebuild for new tabs (CLI `python -m ewa_pipeline excel --result … --tree …` rebuilds without AI).
- UI (`sapui5/webapp/controller/Analysis.controller.js` ~165-250) reads payload loosely → extra fields safe.
- `delete-analysis` (`storage_router.py`) deletes fixed suffixes only → won't clean history.
- Deterministic post-AI pattern to copy: `agents/provenance.py` (`enrich_domain_analysis_provenance`, called in `runner.py`).

## Statuses

| Status | Rule |
|---|---|
| Baseline | No previous run for this system |
| New | Key only in current run |
| Recurring | Key in both, severity same (or lower → note "severity lowered", D6) |
| Worse | Key in both, severity higher |
| Fixed | Key only in previous **and** its section was analysed this run |
| Not checked | Key only in previous, but section failed or is absent this run — **never reported as Fixed** |

Numeric "worse" (e.g. SQL 40% slower) is out of scope (v2).

## Steps

### 2.1 Stable key builder — tier-sonnet
- **Files:** new `backend/ewa_pipeline/report/finding_keys.py`, new `tests/test_finding_keys.py`.
- **Change:** `finding_key(section_title, finding, profile) -> str`, `KEY_VERSION = 1`.
  - Section part = cleaned title (same cleaning as 1.7).
  - 32-hex SQL hash in `subject`/title/evidence → `sql|{hash}` (global: same SQL in 15.1/15.2/15.3 collapses).
  - Else `subject` non-empty → `{section}|{subject cleaned}` (users upper, parameters lower, spaces squashed).
  - Else → `{section}|t:{sorted significant title words}` (no stop words, no numbers).
- **Verify:** tests for SQL collapse, numbering/SID stripping, differently worded titles with same subject → same key.

### 2.2 Put keys on findings — tier-sonnet
- **Files:** `schemas.py`, `services/pipeline.py`, `excel_generator.py`.
- **Change:** set keys in Python after `run_analysis` (post-processing like provenance). All Findings gets "Key" + "Also in" columns at the end.
- **Review note (main session):** `Finding` is also the AI's structured-output schema, so a plain `stable_key` field there would be shown to the AI. Keep it out of the AI schema — e.g. a subclass/wrapper used only after parsing, or a separate `{finding_id: key}` map on `AnalysisResult`. Decide at implementation; must not add AI tokens.
- **Verify:** pipeline test asserts every finding has a key.

### 2.3 Comparison engine — tier-sonnet
- **Files:** new `report/comparison.py`; `schemas.py` (`FindingChange`, `RunComparison`, `AnalysisResult.comparison: RunComparison | None = None`); new `tests/test_comparison.py`.
- **Change:** `compare(current, previous|None) -> RunComparison`. Group by key, worst severity per run. Apply the status table. Leftovers in the same section with title Jaccard ≥ 0.5 are paired before giving up.
- **Verify:** one test per status; specifically a previous finding whose section failed now → "Not checked", never "Fixed".

### 2.4 Compare inside the pipeline + CLI option — tier-sonnet
- **Files:** `services/pipeline.py` (`previous_result: AnalysisResult | None = None`), `ewa_pipeline/main.py` (`--previous PATH` on `analyze` and `excel`).
- **Change:** compare after keys, before Excel. Previous keys recomputed with 2.1, so old payloads work.
- **Verify:** fake pipeline run twice in a test; second with first as previous; assert statuses.

### 2.5 Excel output for changes — tier-sonnet
- **Files:** `excel_generator.py`, `tests/test_excel_generator.py`.
- **Change:**
  - New tab "Changes since last run": Status, Key, Title, Section, Severity now, Severity before, Note.
  - "Status" column at the end of All Findings and section sheets.
  - Exec Summary row 3 (empty spacer today): height 20, merge B3:H3, text e.g. `Since last run (27.04–03.05.2026): 3 new · 2 fixed · 1 worse · 10 recurring · 4 not checked` or `Baseline: first analysed run for this system`. Rows 4+ unchanged.
- **Verify:** test reads B3 and the new tab.

### 2.6 History store — tier-sonnet
- **Files:** new `backend/services/history_service.py`, new `tests/test_history_service.py`.
- **Blob:** `history/{system_key}.json`:
  ```
  {schema_version, key_version, system_key, sid, installation_number, customer_name,
   runs:[{base_name, period_start, period_end, analysed_at,
          findings:[{key,severity,title,section}],
          analysed_sections:[...], not_checked_sections:[...]}]}
  ```
- `system_key` = `SID|installation_number`; if missing, `SID|customer_name` lowercased (D7); sanitised for blob names.
- Pure functions: `upsert_run`, `find_previous` (latest `period_end` earlier than current), `find_duplicate` (same period, different base_name), `first_seen_and_runs_open(key)`.
- Thin blob wrapper: get/put with ETag (version stamp) check, retry once on conflict.
- **Verify:** fake in-memory storage tests incl. out-of-order uploads.

### 2.7 Complete the ID card with upload metadata — tier-sonnet
- **Files:** `indexer/system_profile.py`, `backend/workflow_orchestrator.py`.
- **Change:** read `{base}.html` blob metadata (`system_id`, `customer_name`, `start_date`, `report_date`); fill only gaps; `sources[...]="upload"`; warn if report SID ≠ form SID.
- **Verify:** unit test of the merge.

### 2.8 Wire history into the server run — tier-sonnet (production path: careful review; two failures → back to tier-opus)
- **Files:** `backend/workflow_orchestrator.py`, `backend/routers/storage_router.py` (delete-analysis).
- **Change:**
  - Before `run_pipeline`: profile from `source_content` → load history → find previous → load its payload (fall back to next earlier if missing). Duplicate period → warning.
  - Pass `previous_result` into `_run_pipeline_sync`.
  - After successful upload, while ownership check still passes: `upsert_run`.
  - delete-analysis also removes that run from history.
- **Verify:** mocked-storage test in the style of `tests/test_processing_recovery.py`. Manual: upload two months of one SID → second workbook has Changes tab; re-upload same period → duplicate warning.

### 2.9 "First seen / Open for" columns — tier-sonnet
- **Files:** `services/pipeline.py` (accept history snapshot), `report/comparison.py`, `excel_generator.py`.
- **Change:** First seen (period), Runs open, Days open on the Changes tab.
- **Verify:** test with 3 runs in fake history.

### 2.10 (optional) AI pairing for leftovers — tier-sonnet
- **Files:** `report/comparison.py`, `ewa_pipeline/config.py` (flag).
- **Change:** one call with unpaired New + unpaired previous titles from the same sections; Python validates pairs.
- **Cost:** 0 when nothing left over; typically ~2–6k in, <1k out.
- **Verify:** fake-model test.

### 2.11 Backfill script — tier-sonnet
- **Files:** new `backend/scripts/backfill_history.py`.
- **Change:** list `*_workbook_payload.json`; for each load `{base}.html` + metadata → ID card; compute keys on the fly (no AI, old payloads unchanged); build history sorted by period. Dry run by default; `--apply` writes; `--regenerate-workbooks` rebuilds `_workbook.xlsx` (tree from html → `excel_generator.generate`).
- **Verify:** dry run prints systems/runs/periods table; check by eye before `--apply`.
- **Note:** old findings lack `subject` → title-word keys → first old-vs-new comparison noisier; 2.10 helps.

### 2.12 UI one-liner — tier-sonnet
- **Files:** `sapui5/webapp/controller/Analysis.controller.js`.
- **Change:** if `payload.comparison` exists, show a `sap.m.MessageStrip` (thin info banner) with the summary line above the statistics; add `"sap/m/MessageStrip"` to `sap.ui.define`.
- **Verify:** old analysis → no banner, no errors; new analysis → banner shows.
