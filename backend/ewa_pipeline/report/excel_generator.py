"""
Deterministic Excel workbook generator for EWA analysis results.
"""

from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

from ewa_pipeline.report import excel_style as xs
from ewa_pipeline.report.schemas import (
    AnalysisResult, CrossReference, DomainAnalysis, Finding, ReconciliationRow,
)
from ewa_pipeline.tracking.token_tracker import TokenUsage

# ── Colours ───────────────────────────────────────────────────────────────────

_SZ     = 11          # body size

_C_LINK     = xs.LINK
_C_TITLE_BG = "1F4E79"
_C_BORDER   = "BFBFBF"

_SEV_BG = {"Critical": "C00000", "High": "ED7D31", "Medium": "FFC000", "Low": "548235"}
_SEV_ORDER = ["Critical", "High", "Medium", "Low"]
_HEALTH_BG = {"Critical": "C00000", "Warning": "ED7D31", "Healthy": "548235"}

# SAP's own traffic-light ratings, and the "SAP vs Us" verdict colours.
_RATING_BG = {"RED": "C00000", "YELLOW": "FFC000", "GREEN": "548235"}
_RATING_FG = {"RED": "FFFFFF", "YELLOW": "000000", "GREEN": "FFFFFF"}
_RATING_ORDER = {"RED": 0, "YELLOW": 1, "GREEN": 2}
_VERDICT_BG = {
    "Agree": "C6E0B4",
    "We rated higher": "FFE699",
    "We rated lower": "FFE699",
    "Not covered": "F4B084",
}
_VERDICT_DEFAULT_BG = "D9D9D9"

_NUM = '#,##0'

# ── Style helpers ─────────────────────────────────────────────────────────────

def _font(bold=False, size=xs.BODY_SIZE, color=xs.TEXT, italic=False):
    return xs.font(bold=bold, size=size, color=color, italic=italic)

def _fill(hex_color):
    return PatternFill("solid", fgColor=hex_color)

def _align(h="left", v="center", wrap=False):
    return Alignment(horizontal=h, vertical=v, wrap_text=wrap)

def _border_bottom(color=_C_BORDER):
    return Border(bottom=Side(style="thin", color=color))

def _apply_app_style(ws, *, hide_headers=False):
    """Plain view: 100% zoom, no gridlines. Freeze and print setup happen at the end of generate()."""
    xs.apply_sheet_view(ws)
    if hide_headers:
        ws.sheet_view.showRowColHeaders = False

def _hdr_row(ws, row, values, start_col=1):
    xs.header_row(ws, row, values, start_col=start_col)

def _sheet_ref(name: str) -> str:
    import re as _re
    return f"'{name}'" if _re.search(r"[^A-Za-z0-9_]", name) else name

def _autofit_columns(ws, min_width=8, max_width=55, skip_cols=()):
    """Set column widths based on longest content in each column."""
    col_widths: dict[int, float] = {}
    for row in ws.iter_rows():
        for cell in row:
            if cell.value is None or cell.column in skip_cols:
                continue
            col = cell.column
            length = min(len(str(cell.value)), max_width)
            if length > col_widths.get(col, 0):
                col_widths[col] = length
    for col, length in col_widths.items():
        ws.column_dimensions[get_column_letter(col)].width = max(min_width, length + 2)

# Column widths by header name: short 10-14, titles 30-40, long text 50-60.
_WIDTHS = {
    "Ref.": 10, "Severity": 14, "Effort": 12, "Priority": 14, "Due date": 13,
    "How sure we are": 16, "Check latest SAP guidance first?": 18,
    "SAP transactions": 20, "Risk area": 20,
    "Section": 32, "Title": 36,
    "What it means": 55, "What the SAP report says": 55, "Impact": 50,
    "Recommended action": 55, "Why": 50, "How to confirm": 50,
    "Reviewer note: why check first": 50, "Reviewer note: search query": 50,
}

def _set_widths(ws, header_row, ncols):
    """Fixed width per known header name; other columns fit their content (cap 45)."""
    known = set(range(ncols + 1, ws.max_column + 2))
    for col in range(1, ncols + 1):
        width = _WIDTHS.get(ws.cell(header_row, col).value)
        if width:
            ws.column_dimensions[get_column_letter(col)].width = width
            known.add(col)
    _autofit_columns(ws, min_width=8, max_width=45, skip_cols=known)

def _collapse_group(ws, first_col, last_col):
    """Reviewer-only columns: grouped and collapsed (click + above the sheet to open)."""
    for col in range(first_col, last_col + 1):
        dim = ws.column_dimensions[get_column_letter(col)]
        dim.outlineLevel = 1
        dim.hidden = True
    ws.column_dimensions[get_column_letter(last_col + 1)].collapsed = True

def _guidance_cell(c, required):
    """Check latest SAP guidance first?  Yes in bold, No in grey."""
    c.value = "Yes" if required else "No"
    c.font = _font(bold=True) if required else _font(color=xs.MUTED)

def _link_font():
    return xs.font(color=_C_LINK, underline="single")

def _kpi_tile(ws, top_left, bottom_right, label, value, bg, fg="FFFFFF"):
    """Card-style KPI tile across a merged cell range."""
    ws.merge_cells(f"{top_left}:{bottom_right}")
    c = ws[top_left]
    c.value = f"{label}\n{value}"
    c.fill = _fill(bg)
    c.font = xs.font(bold=True, size=18, color=fg)
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

def _worst_severity(findings):
    """Most serious severity among findings, or None when there are none."""
    present = {f.severity for f in findings}
    for sev in _SEV_ORDER:
        if sev in present:
            return sev
    return None

# ── Sheet builders ────────────────────────────────────────────────────────────

def _build_executive_summary(wb: Workbook, result: AnalysisResult, sheet_map: dict[str, str]):
    ws = wb.create_sheet("Executive Summary")
    _apply_app_style(ws, hide_headers=True)

    # Margin columns A and I
    ws.column_dimensions["A"].width = 2
    ws.column_dimensions["I"].width = 2

    # Aggregate KPI counts
    totals = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    for da in result.domain_analyses:
        for f in da.findings:
            if f.severity in totals:
                totals[f.severity] += 1
    total_findings = sum(totals.values())

    # Title band
    ws.row_dimensions[1].height = 40
    ws.merge_cells("B1:H1")
    c = ws["B1"]
    c.value = "SAP EarlyWatch Alert — Deep Analysis Report"
    c.font = xs.font(bold=True, size=18, color="FFFFFF")
    c.fill = _fill(_C_TITLE_BG)
    c.alignment = _align(h="center")

    # Health banner
    health = result.overall_system_health
    ws.row_dimensions[2].height = 28
    ws.merge_cells("B2:H2")
    c = ws["B2"]
    c.value = f"Overall System Health:  {str(health).upper()}"
    c.font = xs.font(bold=True, size=13, color="FFFFFF")
    c.fill = _fill(_HEALTH_BG.get(health, "888888"))
    c.alignment = _align(h="center")

    # Spacer
    ws.row_dimensions[3].height = 10

    # KPI tile band — rows 4-6
    ws.row_dimensions[4].height = 18
    ws.row_dimensions[5].height = 30
    ws.row_dimensions[6].height = 12

    _kpi_tile(ws, "B4", "C6", "TOTAL FINDINGS", total_findings, _C_TITLE_BG)
    _kpi_tile(ws, "D4", "D6", "CRITICAL",       totals["Critical"], _SEV_BG["Critical"])
    _kpi_tile(ws, "E4", "E6", "HIGH",           totals["High"],     _SEV_BG["High"])
    _kpi_tile(ws, "F4", "F6", "MEDIUM",         totals["Medium"],   _SEV_BG["Medium"], fg="000000")
    _kpi_tile(ws, "G4", "G6", "LOW",            totals["Low"],      _SEV_BG["Low"])

    # Spacer
    ws.row_dimensions[7].height = 10

    # Top 5 Priority Actions header
    r = 8
    c = ws.cell(row=r, column=2, value="Top 5 Priority Actions")
    c.font = xs.font(bold=True, size=13, color=_C_TITLE_BG)
    c.border = _border_bottom(_C_TITLE_BG)
    ws.merge_cells(f"B{r}:H{r}")
    for col in range(2, 9):
        ws.cell(row=r, column=col).border = _border_bottom(_C_TITLE_BG)

    r += 1
    for i, action in enumerate(result.top_5_priority_actions, 1):
        ws.cell(row=r, column=2, value=f"{i}").font = _font(bold=True, color=_C_TITLE_BG, size=12)
        ws.cell(row=r, column=2).alignment = _align(h="center", v="top")
        c = ws.cell(row=r, column=3, value=action)
        c.font = _font()
        c.alignment = _align(wrap=True, v="top")
        ws.merge_cells(f"C{r}:H{r}")
        ws.row_dimensions[r].height = 15 * max(1, -(-len(str(action)) // 90))
        r += 1

    # Spacer
    ws.row_dimensions[r].height = 10
    r += 1

    # Section table
    tbl_hdr_row = r
    col_headers = ["Section", "Worst severity", "Findings", "Critical", "High", "Medium", "Low"]
    xs.header_row(ws, tbl_hdr_row, col_headers, start_col=2, numeric_cols=(4, 5, 6, 7, 8))
    ws.auto_filter.ref = f"B{tbl_hdr_row}:H{tbl_hdr_row}"

    # Worst section first: by worst severity, then most findings, then original order.
    rows = []
    for orig, da in enumerate(result.domain_analyses):
        if da.section_id not in sheet_map:
            continue
        worst = _worst_severity(da.findings)
        rank = _SEV_ORDER.index(worst) if worst else len(_SEV_ORDER)
        rows.append((rank, -len(da.findings), orig, da, worst))
    rows.sort(key=lambda t: t[:3])

    r = tbl_hdr_row + 1
    for idx, (_rank, _n, _orig, da, worst) in enumerate(rows):
        sname = sheet_map[da.section_id]
        ref = _sheet_ref(sname)

        lc = ws.cell(row=r, column=2, value=da.section_title)
        lc.hyperlink = f"#'{sname}'!A1"
        lc.font = _link_font()

        hc = ws.cell(row=r, column=3, value=xs.severity_text(worst) if worst else xs.muted(xs.DASH))
        hc.font = _font()
        hc.alignment = _align(h="left")

        sev_col = "B"
        data_range = f"{ref}!${sev_col}$3:${sev_col}$9999"
        ws.cell(row=r, column=4, value=f"=COUNTA({ref}!$A$3:$A$9999)")
        # Wildcard: the Severity cells read "● High" (dot + word).
        ws.cell(row=r, column=5, value=f'=COUNTIF({data_range},"*Critical")')
        ws.cell(row=r, column=6, value=f'=COUNTIF({data_range},"*High")')
        ws.cell(row=r, column=7, value=f'=COUNTIF({data_range},"*Medium")')
        ws.cell(row=r, column=8, value=f'=COUNTIF({data_range},"*Low")')

        for col in range(4, 9):
            ws.cell(row=r, column=col).alignment = _align(h="right")
            ws.cell(row=r, column=col).font = _font()

        r += 1

    _autofit_columns(ws, min_width=8, max_width=45, skip_cols=(1, 9))


def _build_section_sheet(wb: Workbook, da: DomainAnalysis, sheet_name: str):
    ws = wb.create_sheet(sheet_name)
    _apply_app_style(ws)

    # Columns A (Ref.) and B (Severity) must stay first: the Executive Summary
    # counts findings with formulas over those two columns. New columns go last.
    # The last two columns are reviewer notes, grouped and collapsed.
    COLS = ["Ref.", "Severity", "Title", "What it means", "What the SAP report says",
            "Impact", "Recommended action", "SAP transactions", "Effort", "Priority",
            "Check latest SAP guidance first?", "How sure we are", "Risk area",
            "How to confirm", "Reviewer note: why check first", "Reviewer note: search query"]

    # Row 1: full-width back-link
    ws.merge_cells(f"A1:{get_column_letter(len(COLS))}1")
    bl = ws.cell(row=1, column=1, value="← Executive Summary")
    bl.hyperlink = "#'Executive Summary'!A1"
    bl.font = _link_font()
    bl.alignment = _align(h="left")

    # Row 2: column headers
    _hdr_row(ws, 2, COLS)
    ws.freeze_panes = "A3"

    for i, f in enumerate(da.findings):
        r = 3 + i
        vals = [
            f.id, xs.severity_text(f.severity), f.title, f.description, f.evidence,
            f.impact, f.remediation.action,
            ", ".join(f.remediation.sap_transactions),
            f.remediation.effort_estimate, f.remediation.priority,
            None, xs.sure_dots(f.confidence), ", ".join(f.risk_types), f.to_confirm,
            f.remediation.validation_reason, f.remediation.validation_query,
        ]
        for col, val in enumerate(vals, 1):
            c = ws.cell(row=r, column=col, value=val)
            c.font = _font()
        _guidance_cell(ws.cell(row=r, column=11), f.remediation.external_validation_required)

    xs.apply_table_style(ws, header=2, last_row=max(2, 2 + len(da.findings)), last_col=len(COLS))
    _set_widths(ws, 2, len(COLS))
    _collapse_group(ws, 15, 16)


def _build_all_findings(wb: Workbook, result: AnalysisResult, sheet_map: dict[str, str]):
    """One flat, filterable table of every finding, worst first."""
    ws = wb.create_sheet("All Findings")
    _apply_app_style(ws)

    COLS = [
        "Ref.", "Section", "Severity", "Risk area", "Title",
        "What the SAP report says", "What it means", "How sure we are",
        "Why", "How to confirm", "Impact", "Recommended action",
        "SAP transactions", "Effort", "Priority", "Due date",
        "Check latest SAP guidance first?",
    ]
    _hdr_row(ws, 1, COLS)
    ws.freeze_panes = "A2"

    _SEV_ORDER = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    rows: list[tuple] = []
    for sec_idx, da in enumerate(result.domain_analyses):
        for f_idx, f in enumerate(da.findings):
            rows.append((_SEV_ORDER.get(f.severity, 9), sec_idx, f_idx, da, f))
    rows.sort(key=lambda x: (x[0], x[1], x[2]))

    for i, (_, _, f_idx, da, f) in enumerate(rows):
        r = 2 + i
        vals = [
            f.id, da.section_title, xs.severity_text(f.severity), ", ".join(f.risk_types), f.title,
            f.evidence, f.description, xs.sure_dots(f.confidence),
            f.confidence_reason, f.to_confirm, f.impact, f.remediation.action,
            ", ".join(f.remediation.sap_transactions),
            f.remediation.effort_estimate, f.remediation.priority, f.due_date,
            None,
        ]
        for col, val in enumerate(vals, 1):
            c = ws.cell(row=r, column=col, value=val)
            c.font = _font()
        _guidance_cell(ws.cell(row=r, column=17), f.remediation.external_validation_required)

    xs.apply_table_style(ws, header=1, last_row=max(1, 1 + len(rows)), last_col=len(COLS))

    # Ref. links to the finding's row on its section sheet (after styling, which resets fonts only on borders).
    for i, (_, _, f_idx, da, f) in enumerate(rows):
        sname = sheet_map.get(da.section_id)
        if sname:
            idc = ws.cell(row=2 + i, column=1)
            idc.hyperlink = f"#'{sname}'!A{3 + f_idx}"
            idc.font = _link_font()

    _set_widths(ws, 1, len(COLS))


def _build_sap_vs_us(wb: Workbook, rows: list[ReconciliationRow], sheet_map: dict[str, str]):
    """SAP's own ratings next to ours: verdict counts on top, one row per alert/check below."""
    ws = wb.create_sheet("SAP vs Us")
    _apply_app_style(ws)

    # Summary block: verdict counts, split by Alerts and Checks.
    verdicts: list[str] = []
    for row in rows:
        if row.verdict not in verdicts:
            verdicts.append(row.verdict)
    ws.cell(1, 1, "Verdict counts").font = _font(bold=True, color=_C_TITLE_BG, size=13)
    _hdr_row(ws, 2, ["Verdict", "Alerts", "Checks", "Total"])
    for i, verdict in enumerate(verdicts):
        r = 3 + i
        alerts = sum(1 for x in rows if x.verdict == verdict and x.source == "Alert")
        checks = sum(1 for x in rows if x.verdict == verdict and x.source == "Check")
        vc = ws.cell(r, 1, verdict or "(none)")
        vc.font = _font(bold=True)
        vc.fill = _fill(_VERDICT_BG.get(verdict, _VERDICT_DEFAULT_BG))
        for col, val in ((2, alerts), (3, checks), (4, alerts + checks)):
            c = ws.cell(r, col, val)
            c.font = _font()
            c.alignment = _align(h="center")

    hdr = 3 + len(verdicts) + 1
    COLS = ["Source", "SAP Topic", "SAP Item", "SAP Rating", "Our Section", "Our Rating",
            "Our Finding IDs", "Verdict", "Reason", "Match score", "Matched by"]
    _hdr_row(ws, hdr, COLS)
    ws.freeze_panes = f"A{hdr + 1}"
    ws.auto_filter.ref = f"A{hdr}:{get_column_letter(len(COLS))}{hdr}"

    for i, row in enumerate(rows):
        r = hdr + 1 + i
        vals = [row.source, row.sap_topic, row.sap_item, row.sap_rating, row.our_section_title,
                row.our_rating, ", ".join(row.finding_ids), row.verdict, row.reason,
                row.match_score if row.match_score is not None else "", row.match_method]
        for col, val in enumerate(vals, 1):
            c = ws.cell(r, col, val)
            c.font = _font()
            c.alignment = _align(v="top", wrap=(col in (2, 3, 5, 9)))

        sname = sheet_map.get(row.our_section_id)
        if sname:
            lc = ws.cell(r, 5)
            lc.hyperlink = f"#'{sname}'!A1"
            lc.font = _font(color=_C_LINK)

        for col, rating in ((4, row.sap_rating), (6, row.our_rating)):
            if rating in _RATING_BG:
                c = ws.cell(r, col)
                c.fill = _fill(_RATING_BG[rating])
                c.font = _font(bold=True, color=_RATING_FG[rating])
                c.alignment = _align(h="center", v="top")
        vc = ws.cell(r, 8)
        vc.fill = _fill(_VERDICT_BG.get(row.verdict, _VERDICT_DEFAULT_BG))
        vc.font = _font(bold=True)

    _autofit_columns(ws, min_width=8, max_width=55)


def _build_verified_healthy(wb: Workbook, result: AnalysisResult) -> bool:
    """Sections we analysed and found clean. Returns False (no sheet) when none qualify."""
    with_findings = {da.section_id for da in result.domain_analyses if da.findings}
    healthy = [c for c in result.coverage
               if c.status == "analyzed" and c.section_id not in with_findings]
    if not healthy:
        return False

    # Worst SAP rating among Check rows that point at each section.
    sap_rating: dict[str, str] = {}
    for row in result.reconciliation:
        if row.source != "Check" or row.sap_rating not in _RATING_ORDER:
            continue
        best = sap_rating.get(row.our_section_id)
        if best is None or _RATING_ORDER[row.sap_rating] < _RATING_ORDER[best]:
            sap_rating[row.our_section_id] = row.sap_rating

    ws = wb.create_sheet("No Issues Found")
    _apply_app_style(ws)
    _hdr_row(ws, 1, ["Section", "SAP rating", "Note"])
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = "A1:C1"

    for i, cov in enumerate(healthy):
        r = 2 + i
        rating = sap_rating.get(cov.section_id, "")
        note = "SAP disagrees" if rating in ("RED", "YELLOW") else ""
        ws.cell(r, 1, f"{cov.section_id} {cov.section_title}".strip()).font = _font()
        ws.cell(r, 2, rating).font = _font()
        ws.cell(r, 3, note).font = _font(bold=bool(note))
        if rating in _RATING_BG:
            c = ws.cell(r, 2)
            c.fill = _fill(_RATING_BG[rating])
            c.font = _font(bold=True, color=_RATING_FG[rating])
            c.alignment = _align(h="center")

    _autofit_columns(ws, min_width=8, max_width=55)
    return True


def _build_cross_references(wb: Workbook, xrefs: list[CrossReference]):
    ws = wb.create_sheet("Cross-References")
    _apply_app_style(ws)

    COLS = ["Title", "Related Findings", "Correlation", "Combined Impact", "Recommended Action"]
    _hdr_row(ws, 1, COLS)
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(5)}1"

    for i, xr in enumerate(xrefs):
        r = 2 + i
        vals = [
            xr.title,
            ", ".join(xr.related_findings),
            xr.correlation_description,
            xr.combined_impact,
            xr.recommended_action,
        ]
        for col, val in enumerate(vals, 1):
            c = ws.cell(row=r, column=col, value=val)
            c.font = _font()
            c.alignment = _align(wrap=True)

    _autofit_columns(ws, min_width=10, max_width=55)


def _build_remediation_plan(wb: Workbook, analyses: list[DomainAnalysis]):
    ws = wb.create_sheet("Action Plan")
    _apply_app_style(ws)

    COLS = [
        "Ref.", "Section", "Severity", "Title", "Recommended action", "SAP transactions",
        "Effort", "Priority", "Check latest SAP guidance first?",
        "Reviewer note: why check first", "Reviewer note: search query",
    ]
    _hdr_row(ws, 1, COLS)
    ws.freeze_panes = "A2"

    _SEV_ORDER = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    rows: list[tuple] = []
    for da in analyses:
        for f in da.findings:
            rows.append((_SEV_ORDER.get(f.severity, 9), f, da.section_title))
    rows.sort(key=lambda x: x[0])

    for i, (_, f, section_title) in enumerate(rows):
        r = 2 + i
        vals = [
            f.id, section_title, xs.severity_text(f.severity), f.title,
            f.remediation.action, ", ".join(f.remediation.sap_transactions),
            f.remediation.effort_estimate, f.remediation.priority, None,
            f.remediation.validation_reason, f.remediation.validation_query,
        ]
        for col, val in enumerate(vals, 1):
            c = ws.cell(row=r, column=col, value=val)
            c.font = _font()
        _guidance_cell(ws.cell(row=r, column=9), f.remediation.external_validation_required)

    xs.apply_table_style(ws, header=1, last_row=max(1, 1 + len(rows)), last_col=len(COLS))
    _set_widths(ws, 1, len(COLS))
    _collapse_group(ws, 10, 11)


def _build_document_structure(wb: Workbook, tree: dict):
    ws = wb.create_sheet("Document Structure")
    _apply_app_style(ws)

    _hdr_row(ws, 1, ["Title", "Pages", "Summary", "Depth"])
    ws.freeze_panes = "A2"

    row = [2]

    def _walk(nodes, depth=0):
        for n in nodes:
            title = ("  " * depth) + n.get("title", "")
            ps, pe = n.get("start_index", ""), n.get("end_index", "")
            pages = f"{ps}–{pe}" if ps and pe else ""
            summary = n.get("summary", "")
            r = row[0]
            ws.cell(r, 1, title).font = _font(bold=(depth == 0))
            ws.cell(r, 2, pages).alignment = _align(h="center")
            c = ws.cell(r, 3, summary)
            c.font = _font()
            c.alignment = _align(wrap=True)
            ws.cell(r, 4, depth).font = _font()
            row[0] += 1
            _walk(n.get("nodes", []), depth + 1)

    _walk(tree.get("structure", []))
    _autofit_columns(ws, min_width=8, max_width=55)


def _build_token_usage(wb: Workbook, usage: TokenUsage):
    ws = wb.create_sheet("Token Usage")
    _apply_app_style(ws)

    _hdr_row(ws, 1, ["Phase", "Model", "Input Tokens", "Cached Input", "Cache Write", "Billable Input", "Output Tokens", "Total Tokens"])
    ws.freeze_panes = "A2"

    data_rows = [
        ("Phase 0 — Planning", usage.phase0_model, usage.phase0_input_tokens, usage.phase0_cached_input_tokens, usage.phase0_cache_write_tokens, usage.phase0_output_tokens),
        ("Phase 1 — Domain Analysis", usage.phase1_model, usage.phase1_input_tokens, usage.phase1_cached_input_tokens, usage.phase1_cache_write_tokens, usage.phase1_output_tokens),
        ("Phase 2 — Cross-Ref+Synth", usage.phase2_model, usage.phase2_input_tokens, usage.phase2_cached_input_tokens, usage.phase2_cache_write_tokens, usage.phase2_output_tokens),
    ]

    for i, (phase, model, inp, cached_inp, cache_write, out) in enumerate(data_rows):
        r = 2 + i
        ws.cell(r, 1, phase).font = _font()
        ws.cell(r, 2, model).font = _font()
        ws.cell(r, 3, inp).number_format = _NUM
        ws.cell(r, 4, cached_inp).number_format = _NUM
        ws.cell(r, 5, cache_write).number_format = _NUM
        ws.cell(r, 6, max(inp - cached_inp - cache_write, 0)).number_format = _NUM
        ws.cell(r, 7, out).number_format = _NUM
        c = ws.cell(r, 8, f"=C{r}+G{r}")
        c.number_format = _NUM
        c.font = _font()

    tr = 2 + len(data_rows)
    ws.cell(tr, 1, "TOTAL").font = _font(bold=True)
    for col, letter in ((3, "C"), (4, "D"), (5, "E"), (6, "F"), (7, "G")):
        c = ws.cell(tr, col, f"=SUM({letter}2:{letter}{tr-1})")
        c.number_format = _NUM
        c.font = _font(bold=True)
    for col in range(1, 8):
        ws.cell(tr, col).fill = _fill("BDD7EE")

    ws.cell(tr + 2, 1,
        "Phase 0 tokens are not tracked — PageIndex runs via LiteLLM independently."
    ).font = _font(italic=True, color="888888")

    _autofit_columns(ws, min_width=8, max_width=40)


# ── Final pass over every tab ─────────────────────────────────────────────────

# The five front tabs get the navy tab colour; every other tab has none.
_FRONT_TABS = set(xs.FRONT_TABS) | {"SAP vs Us"}

def _finish_sheets(wb: Workbook) -> None:
    """Tab colour policy and print setup. Freeze panes were set by each builder."""
    for ws in wb.worksheets:
        ws.sheet_properties.tabColor = xs.NAVY if ws.title in _FRONT_TABS else None
        freeze = ws.freeze_panes
        header_row = int("".join(ch for ch in freeze if ch.isdigit())) - 1 if freeze else None
        xs.apply_print_setup(ws, repeat_row=header_row or None)

# ── Public entry point ────────────────────────────────────────────────────────

def generate(result: AnalysisResult, output_path: Path, tree: dict | None = None) -> None:
    wb = xs.init_workbook()
    wb.remove(wb.active)

    _ILLEGAL_SHEET = str.maketrans("", "", "/\\?*[]:'")

    sheet_map: dict[str, str] = {}
    used: set[str] = {"Executive Summary", "All Findings", "Cross-References", "Action Plan", "Document Structure",
                      "Token Usage", "Analysis Tasks", "Source Coverage", "SAP vs Us", "No Issues Found"}
    for da in result.domain_analyses:
        if not da.findings:
            continue
        clean = da.section_title.translate(_ILLEGAL_SHEET).strip()[:31] or "Section"
        base, suffix, name = clean, 1, clean
        while name in used:
            name = f"{base[:28]}_{suffix}"
            suffix += 1
        sheet_map[da.section_id] = name
        used.add(name)

    _build_executive_summary(wb, result, sheet_map)
    _build_all_findings(wb, result, sheet_map)
    if result.reconciliation:
        _build_sap_vs_us(wb, result.reconciliation, sheet_map)
    if result.coverage:
        _build_verified_healthy(wb, result)
    for da in result.domain_analyses:
        if da.section_id in sheet_map:
            _build_section_sheet(wb, da, sheet_map[da.section_id])
    if result.cross_references:
        _build_cross_references(wb, result.cross_references)
    _build_remediation_plan(wb, result.domain_analyses)
    if tree:
        _build_document_structure(wb, tree)
    _build_token_usage(wb, result.token_usage)
    if result.analysis_tasks:
        ws = wb.create_sheet("Analysis Tasks")
        _apply_app_style(ws)
        _hdr_row(ws, 1, ["Task ID", "Title", "Owned Source IDs", "Context IDs", "Source Characters",
                         "Context Characters", "Origin", "Within Budget"])
        for row, task in enumerate(result.analysis_tasks, 2):
            values = [task.task_id, task.title, ", ".join(task.source_section_ids),
                      ", ".join(task.context_section_ids), task.source_content_chars,
                      task.context_content_chars, task.origin, "Yes" if task.within_budget else "No"]
            for col, value in enumerate(values, 1):
                cell = ws.cell(row, col, value)
                if isinstance(value, str):
                    cell.data_type = "s"
                cell.alignment = _align(wrap=True)
        ws.freeze_panes = "A2"
        _autofit_columns(ws, min_width=10, max_width=55)
    if result.coverage:
        ws = wb.create_sheet("Source Coverage")
        _apply_app_style(ws)
        _hdr_row(ws, 1, ["Source ID", "Title", "Task ID", "Status", "Reason"])
        for row, source in enumerate(result.coverage, 2):
            for col, value in enumerate([source.section_id, source.section_title, source.analysis_task_id,
                                         source.status, source.reason], 1):
                cell = ws.cell(row, col, value)
                cell.data_type = "s"
                cell.alignment = _align(wrap=True)
        ws.freeze_panes = "A2"
        _autofit_columns(ws, min_width=10, max_width=55)

    _finish_sheets(wb)

    # Open on the dashboard
    wb.active = 0

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(str(output_path))
