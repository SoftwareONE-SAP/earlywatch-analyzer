# Plan 3 — Fleet view (parked)

Goal: all systems on one screen — systems × domains health grid with trend, plus cross-system questions ("which systems still have HANA user SYSTEM active?", "what is due in 90 days?").

**Needs:** Plan 2 steps 2.1, 2.6, 2.8, 2.11; Plan 1 steps 1.4 (SAP topics = grid columns), 1.1/1.2 (`due_date`, `risk_types`).

**Output form:** an **Excel fleet workbook** first, downloaded with a button. It matches how the team works, Excel filters answer the cross-system questions, and it needs no new UI pages. A UI page can come later.

## Steps (minimum = 3.1–3.3)

### 3.1 Fleet snapshot builder (pure) — tier-sonnet
- **Files:** new `backend/services/fleet_service.py` + test.
- **Change:** read all `history/*.json` plus each system's latest payload `sap_summary` and `reconciliation`. Domains = SAP Check Overview topics with SID removed. Domain health = our colour from 1.7. Trend = latest vs previous (▲ worse, ▼ better, ▶ same).

### 3.2 Fleet Excel — tier-sonnet
- **Files:** new `backend/ewa_pipeline/report/fleet_excel.py`.
- **Tabs:**
  - Health Grid: systems × domains, coloured, with arrows.
  - Open Findings (all systems): SID, customer, key, title, severity, risk type, first seen, days open, due date.
  - Same Issue Across Systems: key → systems.
  - Due in 90 days: `due_date` within 90 days of today.

### 3.3 Endpoint + button — tier-sonnet
- **Files:** new `backend/routers/fleet_router.py` (register where other routers are, see `backend/ewa_main.py`); button in `sapui5/webapp/view/FileList.view.xml` + `controller/FileList.controller.js`.
- **Change:** `GET /api/fleet/export?customer=…` with `require_auth()`. Filter by customer from the start (D10 — security-sensitive).

### 3.4 Later
- Chat over fleet data.
- Rule-based reading of maintenance end dates (more reliable than AI `due_date`).
- UI grid page.
