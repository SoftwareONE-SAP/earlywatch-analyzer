"""
Deterministic Excel workbook generator for EWA analysis results.
"""

import re
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Side
from openpyxl.utils import get_column_letter

from ewa_pipeline.report import excel_style as xs
from ewa_pipeline.report import reconciliation_display as rd
from ewa_pipeline.report.schemas import (
    AnalysisResult, CrossReference, DomainAnalysis, Finding, ReconciliationRow,
)
from ewa_pipeline.tracking.token_tracker import TokenUsage

# ── Colours ───────────────────────────────────────────────────────────────────

_SZ     = 11          # body size

_C_LINK     = xs.LINK

_SEV_ORDER = ["Critical", "High", "Medium", "Low"]

# SAP's own traffic-light ratings, and the "SAP vs Us" verdict colours.
_RATING_ORDER = {"RED": 0, "YELLOW": 1, "GREEN": 2}

_NUM = '#,##0'

# ── Style helpers ─────────────────────────────────────────────────────────────

def _font(bold=False, size=xs.BODY_SIZE, color=xs.TEXT, italic=False):
    return xs.font(bold=bold, size=size, color=color, italic=italic)

def _align(h="left", v="center", wrap=False):
    return Alignment(horizontal=h, vertical=v, wrap_text=wrap)

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
    "SAP list": 11, "SAP topic": 24, "What SAP says": 40, "SAP rating": 14,
    "SoftwareONE rating": 18, "Our finding": 36, "Result": 26, "Explanation": 55,
    "Report section": 30, "Note": 45, 
    "Reviewer note: refs": 18, "Reviewer note: score": 14, "Reviewer note: matched by": 20,
    "Reviewer note: original note": 55,
    "Related findings": 45, "How they connect": 55, "Combined impact": 50,
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

def _worst_severity(findings):
    """Most serious severity among findings, or None when there are none."""
    present = {f.severity for f in findings}
    for sev in _SEV_ORDER:
        if sev in present:
            return sev
    return None

# ── Sheet builders ────────────────────────────────────────────────────────────

_HOW_TO_READ = "How to read this workbook"
_LINKED = "Linked Issues"


def _build_how_to_read(wb: Workbook, tabs: set[str]):
    """First tab: what each tab is for and what the dots mean. One wide wrapped column."""
    ws = wb.create_sheet(_HOW_TO_READ)
    _apply_app_style(ws)
    ws.column_dimensions["A"].width = 100

    lines: list = []  # (text or rich text, kind) with kind in title / note / head / body

    def add(value, kind="body"):
        lines.append((value, kind))

    add(_HOW_TO_READ, "title")
    add("A plain-English review of your SAP EarlyWatch Alert report, prepared by SoftwareONE. "
        "Read this page first.", "note")
    add("What each tab shows", "head")
    add("Executive Summary " + xs.DASH + " the overall health, the most urgent actions and the number of "
        "findings in each report section.")
    add("All Findings " + xs.DASH + " every finding in one list, worst first. Use the arrows in the "
        "header row to filter or sort.")
    if _SAP_VS_US in tabs:
        add(f"{_SAP_VS_US} " + xs.DASH + " SAP's own ratings next to ours, so you can see where we agree "
            "and where a second look is worthwhile.")
    if "No Issues Found" in tabs:
        add("No Issues Found " + xs.DASH + " report sections we checked and found clean.")
    add("Section tabs " + xs.DASH + " one tab per report section with findings: what the SAP report says, "
        "what it means and what to do about it.")
    if _LINKED in tabs:
        add(f"{_LINKED} " + xs.DASH + " findings that are connected and are best handled together.")
    add("Action Plan " + xs.DASH + " every recommended action in one list.")

    add("How serious is a finding?", "head")
    add(xs.legend_line(xs.severity_text("Critical"), "needs attention straight away."))
    add(xs.legend_line(xs.severity_text("High"), "should be fixed soon."))
    add(xs.legend_line(xs.severity_text("Medium"), "plan a fix."))
    add(xs.legend_line(xs.severity_text("Low"), "worth knowing; low urgency."))

    add("SAP's own traffic lights", "head")
    add(xs.legend_line(xs.rating_text("RED"), "SAP flags this as a problem."))
    add(xs.legend_line(xs.rating_text("YELLOW"), "SAP flags this as a warning."))
    add(xs.legend_line(xs.rating_text("GREEN"), "SAP sees no problem."))

    add("How sure are we?", "head")
    add(xs.legend_line(xs.sure_dots("High"), "the evidence is clear."))
    add(xs.legend_line(xs.sure_dots("Medium"), "likely, but worth confirming."))
    add(xs.legend_line(xs.sure_dots("Low"), "a rough match; please check by hand."))

    add("Good to know", "head")
    add("Columns called \"Reviewer note\" are folded away. Click the small + above the column letters to "
        "open them.")
    add("Some technical tabs are hidden. To see them in Excel, right-click any tab and choose Unhide.")
    add("\"Check latest SAP guidance first?\" says Yes when the advice depends on current SAP Notes or "
        "release information that you should look up before acting.")

    for r, (value, kind) in enumerate(lines, 1):
        c = ws.cell(r, 1, value)
        if kind == "title":
            c.font = _font(bold=True, size=16)
        elif kind == "note":
            c.font = _font(size=10, color=xs.NOTE)
        elif kind == "head":
            c.font = _font(bold=True)
        else:
            c.font = _font()
        c.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
        if kind == "head":
            ws.row_dimensions[r].height = 30  # room above the heading
            c.alignment = Alignment(horizontal="left", vertical="bottom", wrap_text=True)


_HEALTH_DOT = {"Critical": "C00000", "Warning": "E0A000", "Healthy": "548235"}


def _text_lines(text, per_line=100) -> int:
    """Rough number of wrapped lines a text needs (merged cells do not auto-fit)."""
    return max(1, sum(max(1, -(-len(part) // per_line)) for part in str(text).split("\n")))


def _profile_line(profile) -> str:
    """One quiet line about the analysed system, built from whatever is known."""
    if profile is None:
        return ""
    parts = []
    if profile.sid:
        parts.append(f"System {profile.sid}")
    for name, version in ((profile.product, profile.product_version),
                          (profile.database, profile.database_version)):
        text = " ".join(p for p in (name, version) if p)
        if text:
            parts.append(text)
    if profile.os:
        parts.append(profile.os)
    if profile.system_role:
        parts.append(profile.system_role)
    if profile.period_start and profile.period_end:
        parts.append(f"Period {profile.period_start} {xs.DASH} {profile.period_end}")
    elif profile.period_start or profile.period_end:
        parts.append(f"Period {profile.period_start or profile.period_end}")
    return "  ·  ".join(parts)


def _clean_action(text) -> str:
    """Drop a leading "1." / "2)" / bullet: the numbering is added by the workbook."""
    return re.sub(r"^\s*(?:\d+\s*[.)]|[-•*])\s*", "", str(text)).strip()


def _build_executive_summary(wb: Workbook, result: AnalysisResult, sheet_map: dict[str, str]):
    ws = wb.create_sheet("Executive Summary")
    _apply_app_style(ws, hide_headers=True)

    # Margin columns A and I, then fixed widths (the merged text rows do not auto-fit).
    for col, width in (("A", 2), ("B", 38), ("C", 16), ("D", 11), ("E", 11), ("F", 11),
                       ("G", 11), ("H", 11), ("I", 2)):
        ws.column_dimensions[col].width = width

    # Aggregate KPI counts
    totals = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    for da in result.domain_analyses:
        for f in da.findings:
            if f.severity in totals:
                totals[f.severity] += 1
    total_findings = sum(totals.values())

    top_left = Alignment(horizontal="left", vertical="top", wrap_text=True)

    # Row 1: title
    ws.merge_cells("B1:H1")
    c = ws["B1"]
    c.value = "SAP EarlyWatch Alert — Deep Analysis Report"
    c.font = _font(bold=True, size=16)
    c.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[1].height = 26

    # Row 2: health line (the upper-case word stays: tests and readers look for it)
    health = result.overall_system_health
    ws.merge_cells("B2:H2")
    c = ws["B2"]
    c.value = xs.dot_label(_HEALTH_DOT.get(health, xs.MUTED), str(health).upper(), size=14,
                           bold=True, prefix="Overall system health: ")
    c.font = _font(bold=True, size=14)
    c.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[2].height = 24

    r = 3
    # System profile line, when we know anything about the system
    profile = _profile_line(result.system_profile)
    if profile:
        ws.merge_cells(f"B{r}:H{r}")
        c = ws.cell(r, 2, profile)
        c.font = _font(size=10, color=xs.NOTE)
        c.alignment = top_left
        ws.row_dimensions[r].height = 15 * _text_lines(profile, 120)
        r += 1

    # Written summary
    if result.executive_summary and result.executive_summary.strip():
        r += 1
        ws.merge_cells(f"B{r}:H{r}")
        c = ws.cell(r, 2, result.executive_summary.strip())
        c.font = _font()
        c.alignment = top_left
        ws.row_dimensions[r].height = 15 * _text_lines(result.executive_summary.strip(), 100)
        r += 1

    # Key numbers: a small grey label with its dot, a big number underneath. No fills.
    r += 1
    label_row, number_row = r, r + 1
    ws.row_dimensions[label_row].height = 18
    ws.row_dimensions[number_row].height = 30
    tiles = [(4, "Total", None, total_findings)] + [
        (5 + i, sev, xs.SEVERITY_COLOURS[sev], totals[sev]) for i, sev in enumerate(_SEV_ORDER)
    ]
    for col, label, dot_colour, number in tiles:
        lc = ws.cell(label_row, col)
        lc.value = (xs.dot_label(dot_colour, label, size=10, word_colour=xs.NOTE)
                    if dot_colour else label)
        lc.font = _font(size=10, color=xs.NOTE)
        lc.alignment = Alignment(horizontal="right", vertical="bottom")
        nc = ws.cell(number_row, col, number)
        nc.font = _font(bold=True, size=20)
        nc.alignment = Alignment(horizontal="right", vertical="center")
    r = number_row + 2

    # Top 5 priority actions
    for col in range(2, 9):
        ws.cell(r, col).border = Border(bottom=Side(style="medium", color=xs.HEADER_LINE))
    c = ws.cell(r, 2, "Top 5 priority actions")
    c.font = _font(bold=True, size=12)
    ws.row_dimensions[r].height = 20
    r += 1
    for i, action in enumerate(result.top_5_priority_actions, 1):
        text = f"{i}. {_clean_action(action)}"
        ws.merge_cells(f"B{r}:H{r}")
        c = ws.cell(r, 2, text)
        c.font = _font()
        c.alignment = top_left
        for col in range(2, 9):
            ws.cell(r, col).border = Border(bottom=Side(style="thin", color=xs.ROW_LINE))
        ws.row_dimensions[r].height = 15 * _text_lines(text, 100)
        r += 1

    r += 1
    c = ws.cell(r, 2, "Findings by section")
    c.font = _font(bold=True, size=12)
    r += 1

    # Section table
    tbl_hdr_row = r
    col_headers = ["Section", "Worst severity", "Findings", "Critical", "High", "Medium", "Low"]
    xs.header_row(ws, tbl_hdr_row, col_headers, start_col=2, numeric_cols=(4, 5, 6, 7, 8))

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
    for _rank, _n, _orig, da, worst in rows:
        sname = sheet_map[da.section_id]
        ref = _sheet_ref(sname)

        lc = ws.cell(row=r, column=2, value=da.section_title)
        lc.hyperlink = f"#'{sname}'!A1"
        lc.font = _link_font()

        hc = ws.cell(row=r, column=3, value=xs.severity_text(worst) if worst else xs.muted(xs.DASH))
        hc.font = _font()

        sev_col = "B"
        data_range = f"{ref}!${sev_col}$3:${sev_col}$9999"
        ws.cell(row=r, column=4, value=f"=COUNTA({ref}!$A$3:$A$9999)")
        # Wildcard: the Severity cells read "● High" (dot + word).
        ws.cell(row=r, column=5, value=f'=COUNTIF({data_range},"*Critical")')
        ws.cell(row=r, column=6, value=f'=COUNTIF({data_range},"*High")')
        ws.cell(row=r, column=7, value=f'=COUNTIF({data_range},"*Medium")')
        ws.cell(row=r, column=8, value=f'=COUNTIF({data_range},"*Low")')

        for col in range(2, 9):
            cell = ws.cell(row=r, column=col)
            cell.border = Border(bottom=Side(style="thin", color=xs.ROW_LINE))
            cell.alignment = Alignment(horizontal="right" if col >= 4 else "left",
                                       vertical="top", wrap_text=True)
            if col >= 4:
                cell.font = _font()
        r += 1

    ws.auto_filter.ref = f"B{tbl_hdr_row}:H{max(r - 1, tbl_hdr_row)}"


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


_SAP_VS_US = "SAP vs SoftwareONE"

# Results a reader should look at first: shown in bold.
_BOLD_RESULTS = {rd.RESULT_MORE, rd.RESULT_LESS, rd.RESULT_CHECK}
_RESULT_ORDER = [rd.RESULT_AGREE, rd.RESULT_MORE, rd.RESULT_LESS, rd.RESULT_CHECK,
                 rd.RESULT_NOT_FOUND, rd.RESULT_NOT_ANALYSED, rd.RESULT_NO_DETAIL,
                 rd.RESULT_NO_RATING]


def _build_sap_vs_us(wb: Workbook, rows: list[ReconciliationRow], sheet_map: dict[str, str],
                     analyses: list[DomainAnalysis]):
    """SAP's own ratings next to ours: result counts on top, one row per alert/check below."""
    ws = wb.create_sheet(_SAP_VS_US)
    _apply_app_style(ws)

    findings_by_id: dict = {}
    finding_row: dict[str, tuple[str, int]] = {}  # finding id -> (section id, row on its sheet)
    for da in analyses:
        for i, f in enumerate(da.findings):
            findings_by_id.setdefault(f.id, f)
            finding_row.setdefault(f.id, (da.section_id, 3 + i))
    displays = [rd.describe(row, findings_by_id) for row in rows]

    ws.cell(1, 1, _SAP_VS_US).font = _font(bold=True, size=16)
    ws.cell(2, 1, "SAP's own ratings next to ours. Bold results are worth a look. "
                  "Dots show how sure we are: "
                  f"{xs.DOT * 3} High, {xs.DOT * 2}{xs.EMPTY} Medium, {xs.DOT}{xs.EMPTY * 2} Low."
            ).font = _font(size=10, color=xs.NOTE)

    # Summary block: result counts, split by Alerts and Checks.
    seen = {d.result for d in displays}
    results = [r for r in _RESULT_ORDER if r in seen] + sorted(seen - set(_RESULT_ORDER))
    sum_hdr = 4
    xs.header_row(ws, sum_hdr, ["Result", None, None, "Alerts", "Checks", "Total"], numeric_cols=(4, 5, 6))
    for i, result_name in enumerate(results):
        r = sum_hdr + 1 + i
        alerts = sum(1 for x, d in zip(rows, displays) if d.result == result_name and x.source == "Alert")
        checks = sum(1 for x, d in zip(rows, displays) if d.result == result_name and x.source == "Check")
        ws.cell(r, 1, result_name).font = _font(bold=result_name in _BOLD_RESULTS)
        for col, val in ((4, alerts), (5, checks), (6, alerts + checks)):
            ws.cell(r, col, val).font = _font()
    sum_last = sum_hdr + len(results)
    xs.apply_table_style(ws, header=sum_hdr, last_row=sum_last, last_col=6,
                         numeric_cols=(4, 5, 6), filter=False)
    for r in range(sum_hdr + 1, sum_last + 1):  # labels run across the empty cells beside them
        ws.cell(r, 1).alignment = _align(v="top")

    hdr = sum_last + 2
    COLS = ["SAP list", "SAP topic", "What SAP says", "SAP rating", "SoftwareONE rating",
            "Our finding", "Result", "How sure we are", "Explanation", "Report section",
            "Reviewer note: refs", "Reviewer note: score", "Reviewer note: matched by",
            "Reviewer note: original note"]
    _hdr_row(ws, hdr, COLS)
    ws.freeze_panes = f"A{hdr + 1}"

    for i, (row, disp) in enumerate(zip(rows, displays)):
        r = hdr + 1 + i
        fid = row.finding_ids[0] if row.finding_ids else None
        finding = findings_by_id.get(fid) if fid else None
        title = finding.title if finding is not None else ""
        if title and len(row.finding_ids) > 1:
            title += f" (+{len(row.finding_ids) - 1} more)"
        vals = [row.source, row.sap_topic, row.sap_item, xs.rating_text(row.sap_rating),
                xs.rating_text(row.our_rating), title, disp.result, xs.sure_dots(disp.how_sure),
                disp.explanation, row.our_section_title, ", ".join(row.finding_ids),
                row.match_score if row.match_score is not None else "", row.match_method,
                row.reason]
        for col, val in enumerate(vals, 1):
            ws.cell(r, col, val).font = _font()
        ws.cell(r, 7).font = _font(bold=disp.result in _BOLD_RESULTS)

    last = max(hdr, hdr + len(rows))
    xs.apply_table_style(ws, header=hdr, last_row=last, last_col=len(COLS))

    # Links (after styling): finding -> its row on the section tab, section -> top of its tab.
    for i, row in enumerate(rows):
        r = hdr + 1 + i
        fid = row.finding_ids[0] if row.finding_ids else None
        target = finding_row.get(fid) if fid else None
        if target and sheet_map.get(target[0]) and ws.cell(r, 6).value:
            ws.cell(r, 6).hyperlink = f"#'{sheet_map[target[0]]}'!A{target[1]}"
            ws.cell(r, 6).font = _link_font()
        sname = sheet_map.get(row.our_section_id)
        if sname and row.our_section_title:
            ws.cell(r, 10).hyperlink = f"#'{sname}'!A1"
            ws.cell(r, 10).font = _link_font()

    _set_widths(ws, hdr, len(COLS))
    _collapse_group(ws, 11, 14)


def _healthy_sections(result: AnalysisResult) -> list:
    """Coverage entries we analysed and found clean."""
    with_findings = {da.section_id for da in result.domain_analyses if da.findings}
    return [c for c in result.coverage
            if c.status == "analyzed" and c.section_id not in with_findings]


def _has_healthy_sections(result: AnalysisResult) -> bool:
    return bool(_healthy_sections(result))


def _build_verified_healthy(wb: Workbook, result: AnalysisResult) -> bool:
    """Sections we analysed and found clean. Returns False (no sheet) when none qualify."""
    healthy = _healthy_sections(result)
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

    for i, cov in enumerate(healthy):
        r = 2 + i
        rating = sap_rating.get(cov.section_id, "")
        flagged = rating in ("RED", "YELLOW")
        ws.cell(r, 1, cov.section_title.strip() or cov.section_id).font = _font()
        ws.cell(r, 2, xs.rating_text(rating)).font = _font()
        ws.cell(r, 3, f"SAP flagged this {xs.DASH} please review" if flagged else None).font = _font(bold=flagged)

    xs.apply_table_style(ws, header=1, last_row=1 + len(healthy), last_col=3)
    _set_widths(ws, 1, 3)
    return True

def _build_linked_issues(wb: Workbook, xrefs: list[CrossReference], analyses: list[DomainAnalysis]):
    """Findings that belong together, with their titles instead of bare reference numbers."""
    ws = wb.create_sheet(_LINKED)
    _apply_app_style(ws)

    titles = {f.id: f.title for da in analyses for f in da.findings}
    COLS = ["Title", "Related findings", "How they connect", "Combined impact", "Recommended action"]
    _hdr_row(ws, 1, COLS)
    ws.freeze_panes = "A2"

    for i, xr in enumerate(xrefs):
        r = 2 + i
        related = "\n".join(f"{fid} {titles[fid]}" if fid in titles else fid
                            for fid in xr.related_findings)
        vals = [xr.title, related, xr.correlation_description, xr.combined_impact,
                xr.recommended_action]
        for col, val in enumerate(vals, 1):
            ws.cell(row=r, column=col, value=val).font = _font()

    xs.apply_table_style(ws, header=1, last_row=1 + len(xrefs), last_col=len(COLS))
    _set_widths(ws, 1, len(COLS))


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
    ws.cell(tr + 2, 1,
        "Phase 0 tokens are not tracked — PageIndex runs via LiteLLM independently."
    ).font = _font(italic=True, color="888888")

    _autofit_columns(ws, min_width=8, max_width=40)


# ── Final pass over every tab ─────────────────────────────────────────────────

# The five front tabs get the navy tab colour; every other tab has none.
_FRONT_TABS = set(xs.FRONT_TABS)

# Technical tabs for reviewers: kept in the file, hidden from view.
_HIDDEN_TABS = {"Document Structure", "Token Usage", "Analysis Tasks", "Source Coverage"}

def _finish_sheets(wb: Workbook) -> None:
    """Tab colour policy and print setup. Freeze panes were set by each builder."""
    for ws in wb.worksheets:
        ws.sheet_properties.tabColor = xs.NAVY if ws.title in _FRONT_TABS else None
        ws.sheet_state = "hidden" if ws.title in _HIDDEN_TABS else "visible"
        freeze = ws.freeze_panes
        header_row = int("".join(ch for ch in freeze if ch.isdigit())) - 1 if freeze else None
        xs.apply_print_setup(ws, repeat_row=header_row or None)

# ── Public entry point ────────────────────────────────────────────────────────

def generate(result: AnalysisResult, output_path: Path, tree: dict | None = None) -> None:
    wb = xs.init_workbook()
    wb.remove(wb.active)

    _ILLEGAL_SHEET = str.maketrans("", "", "/\\?*[]:'")

    sheet_map: dict[str, str] = {}
    used: set[str] = {_HOW_TO_READ, "Executive Summary", "All Findings", _LINKED, "Action Plan", "Document Structure",
                      "Token Usage", "Analysis Tasks", "Source Coverage", _SAP_VS_US, "No Issues Found"}
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

    _build_how_to_read(wb, {
        _SAP_VS_US if result.reconciliation else "",
        "No Issues Found" if _has_healthy_sections(result) else "",
        _LINKED if result.cross_references else "",
    })
    _build_executive_summary(wb, result, sheet_map)
    _build_all_findings(wb, result, sheet_map)
    if result.reconciliation:
        _build_sap_vs_us(wb, result.reconciliation, sheet_map, result.domain_analyses)
    if result.coverage:
        _build_verified_healthy(wb, result)
    for da in result.domain_analyses:
        if da.section_id in sheet_map:
            _build_section_sheet(wb, da, sheet_map[da.section_id])
    if result.cross_references:
        _build_linked_issues(wb, result.cross_references, result.domain_analyses)
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

    # Open on "How to read this workbook" (the first tab)
    wb.active = 0
    for i, ws in enumerate(wb.worksheets):
        ws.sheet_view.tabSelected = (i == 0)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(str(output_path))
