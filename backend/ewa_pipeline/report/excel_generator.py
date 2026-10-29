"""
Deterministic Excel workbook generator for EWA analysis results.
"""

import re
from pathlib import Path

from openpyxl import Workbook
from openpyxl.cell.rich_text import CellRichText, TextBlock
from openpyxl.styles import Alignment, Border, PatternFill, Side
from openpyxl.utils import get_column_letter

from ewa_pipeline.report import excel_style as xs
from ewa_pipeline.report import reconciliation_display as rd
from ewa_pipeline.report import visual_data as vd
from ewa_pipeline.report.schemas import (
    AnalysisResult, CrossReference, DomainAnalysis, Finding,
)
from ewa_pipeline.tracking.token_tracker import TokenUsage

# ── Colours ───────────────────────────────────────────────────────────────────

_SZ     = 11          # body size

_C_LINK     = xs.LINK

_SEV_ORDER = ["Critical", "High", "Medium", "Low"]

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

# ── Sheet builders ────────────────────────────────────────────────────────────

_FINDINGS = "Findings"
_PRIORITY = "Priority Actions"


_HEALTH_DOT = {"Critical": "C00000", "Warning": "E0A000", "Healthy": "548235"}


def _text_lines(text, per_line=100) -> int:
    """Rough number of wrapped lines a text needs (merged cells do not auto-fit)."""
    return max(1, sum(max(1, -(-len(part) // per_line)) for part in str(text).split("\n")))


def _clean_action(text) -> str:
    """Drop a leading "1." / "2)" / bullet: the numbering is added by the workbook."""
    return re.sub(r"^\s*(?:\d+\s*[.)]|[-•*])\s*", "", str(text)).strip()


def _build_priority_actions(wb: Workbook, result: AnalysisResult):
    """Front tab: the overall health and the top 5 actions, each with links to the findings it names."""
    ws = wb.create_sheet(_PRIORITY)
    _apply_app_style(ws, hide_headers=True)

    # Margin columns A and I; B..G hold the merged action text, H the finding refs.
    for col, width in (("A", 2), ("B", 38), ("C", 16), ("D", 11), ("E", 11), ("F", 11),
                       ("G", 11), ("H", 16), ("I", 2)):
        ws.column_dimensions[col].width = width

    top_left = Alignment(horizontal="left", vertical="top", wrap_text=True)
    line = Border(bottom=Side(style="thin", color=xs.ROW_LINE))

    # Row 1: title, with the system id when we know it
    sid = result.system_profile.sid if result.system_profile else ""
    ws.merge_cells("B1:H1")
    c = ws["B1"]
    c.value = f"SAP EarlyWatch Alert {xs.DASH} {sid or 'Deep Analysis Report'}"
    c.font = _font(bold=True, size=16)
    c.alignment = Alignment(horizontal="left", vertical="center")
    xs.title_band(ws, 1, 1, 8)
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

    # Top 5 priority actions
    c = ws.cell(4, 2, "Top 5 priority actions")
    c.font = _font(bold=True, size=12, color=xs.NAVY)
    ws.row_dimensions[4].height = 20
    row_by_id, _ = _finding_rows(result)

    r = 5
    for i, action in enumerate(result.top_5_priority_actions, 1):
        clean = _clean_action(action)
        text = f"{i}. {clean}"
        r = _put_action_rows(ws, r, text, text, _refs_in_text(clean, result), row_by_id)

    if r == 5:
        ws.merge_cells("B5:H5")
        c = ws.cell(5, 2, "No priority actions were produced.")
        c.font = _font(color=xs.MUTED)
        c.alignment = top_left
        for col in range(2, 9):
            ws.cell(5, col).border = line
        r = 6

    # Risks that add up: findings that are best handled together
    if result.cross_references:
        r += 1
        c = ws.cell(r, 2, "Risks that add up")
        c.font = _font(bold=True, size=12, color=xs.NAVY)
        ws.row_dimensions[r].height = 20
        r += 1
        for xr in result.cross_references:
            value, text = _risk_text(xr)
            refs = list(dict.fromkeys(fid for fid in xr.related_findings if fid in row_by_id))
            r = _put_action_rows(ws, r, value, text, refs, row_by_id)

    # What we checked, and anything we could not analyse
    lines = _coverage_lines(result)
    if lines:
        r += 1
        for text, bold in lines:
            ws.merge_cells(f"B{r}:H{r}")
            c = ws.cell(r, 2, text)
            c.font = _font(bold=bold)
            c.alignment = top_left
            ws.row_dimensions[r].height = max(15, 15 * _text_lines(text, 110))
            r += 1

    _put_how_to_read(ws, r + 1, result)


def _put_how_to_read(ws, r, result: AnalysisResult) -> None:
    """Short guide at the bottom of the front tab: severity and dots legends, one line per other tab."""
    top_left = Alignment(horizontal="left", vertical="top", wrap_text=True)
    c = ws.cell(r, 2, "How to read this workbook")
    c.font = _font(bold=True, size=12, color=xs.NAVY)
    ws.row_dimensions[r].height = 20
    r += 1

    lines: list = [
        _legend("How serious a finding is:  ", [xs.severity_text(sev) for sev in _SEV_ORDER]),
        _legend("How sure we are:  ", [xs.sure_dots(level) for level in ("High", "Medium", "Low")]),
        f"{_FINDINGS} {xs.DASH} every finding in one list, worst first. Use the arrows in the header row "
        "to filter or sort. Folded columns on the right hold more detail; click the small + above the "
        "column letters to open them.",
    ]
    if result.reconciliation:
        lines.append(f"{_SAP_VS_US} {xs.DASH} SAP's own ratings next to ours, so you can see where we "
                     "agree and where a second look is worthwhile.")
    if vd.heatmap_rows(result):
        lines.append(f"{_HEATMAP} {xs.DASH} which report sections carry which kinds of risk, coloured by "
                     "the most serious finding.")
    for value in lines:
        ws.merge_cells(f"B{r}:H{r}")
        c = ws.cell(r, 2, value)
        c.font = _font()
        c.alignment = top_left
        ws.row_dimensions[r].height = max(15, 15 * _text_lines(value, 110))
        r += 1


def _coverage_lines(result: AnalysisResult) -> list[tuple[str, bool]]:
    """(text, bold) lines: how many sections we checked and found clean, and how many failed."""
    lines: list[tuple[str, bool]] = []
    checked = sum(1 for c in result.coverage if c.status == "analyzed")
    if checked:
        healthy = _healthy_sections(result)
        text = f"We checked {checked} sections, no issues in {len(healthy)} of them"
        sap_rating = vd.sap_rating_by_section(result.reconciliation)
        flagged = sum(1 for c in healthy if sap_rating.get(c.section_id) in ("RED", "YELLOW"))
        if flagged:
            text += f" (SAP rated {flagged} red/yellow; see {_SAP_VS_US})"
        lines.append((text + ".", False))
    failed = sum(1 for c in result.coverage if c.status == "failed")
    if failed:
        lines.append((f"{failed} {'section' if failed == 1 else 'sections'} could not be analysed.", True))
    return lines


def _put_action_rows(ws, r, value, height_text, refs, row_by_id) -> int:
    """Text merged across B..G, one linked finding ref per row in column H, a grey line below.

    One row per ref (at least one); returns the next free row.
    """
    top_left = Alignment(horizontal="left", vertical="top", wrap_text=True)
    k = max(1, len(refs))
    ws.merge_cells(f"B{r}:G{r + k - 1}")
    c = ws.cell(r, 2, value)
    c.font = _font()
    c.alignment = top_left
    for n, fid in enumerate(refs):
        rc = ws.cell(r + n, 8, fid)
        rc.font = _font()
        rc.alignment = top_left
        if fid in row_by_id:
            rc.hyperlink = f"#'{_FINDINGS}'!A{row_by_id[fid]}"
            rc.font = _link_font()
    for rr in range(r, r + k):
        ws.row_dimensions[rr].height = max(15, 15 * _text_lines(height_text, 95) / k)
    for col in range(2, 9):
        ws.cell(r + k - 1, col).border = Border(bottom=Side(style="thin", color=xs.ROW_LINE))
    return r + k


def _risk_text(xr: CrossReference):
    """Cell value (rich text when available) and plain text for one linked risk: title, why, what to do."""
    parts = [("", xr.title, True)]
    why = " ".join(t.strip() for t in (xr.correlation_description, xr.combined_impact) if t.strip())
    if why:
        parts.append(("Why it matters together: ", why, False))
    if xr.recommended_action.strip():
        parts.append(("What to do: ", xr.recommended_action.strip(), False))
    text = "\n".join(label + body for label, body, _ in parts)
    if not xs.RICH:
        return text, text
    blocks = []
    for n, (label, body, bold) in enumerate(parts):
        if n:
            blocks.append(TextBlock(xs._inline(xs.TEXT), "\n"))
        if label:
            blocks.append(TextBlock(xs._inline(xs.TEXT, bold=True), label))
        blocks.append(TextBlock(xs._inline(xs.TEXT, bold=bold), body))
    return CellRichText(*blocks), text


_SEV_RANK = {sev: i for i, sev in enumerate(_SEV_ORDER)}


def _findings_in_order(result: AnalysisResult) -> list[tuple[DomainAnalysis, Finding]]:
    """Every (section, finding) pair, worst severity first, then section order, then finding order."""
    rows: list[tuple] = []
    for sec_idx, da in enumerate(result.domain_analyses):
        for f_idx, f in enumerate(da.findings):
            rows.append((_SEV_RANK.get(f.severity, 9), sec_idx, f_idx, da, f))
    rows.sort(key=lambda x: x[:3])
    return [(da, f) for *_, da, f in rows]


def _finding_rows(result: AnalysisResult) -> tuple[dict[str, int], dict[str, int]]:
    """Row on the Findings tab for each finding id, and for the first finding of each section.

    Data starts at row 2. A repeated id keeps its first row.
    """
    row_by_id: dict[str, int] = {}
    first_row_by_section: dict[str, int] = {}
    for i, (da, f) in enumerate(_findings_in_order(result)):
        row_by_id.setdefault(f.id, 2 + i)
        first_row_by_section.setdefault(da.section_id, 2 + i)
    return row_by_id, first_row_by_section


def _refs_in_text(text, result: AnalysisResult) -> list[str]:
    """Finding ids mentioned in a text, in order of appearance, each once.

    "A-F001 – A-F003" (two ids of one section joined only by a dash) also brings in the
    findings between them. Anything that is not a real finding id is ignored.
    """
    position: dict[str, tuple[int, int]] = {}  # id -> (section index, finding index), first one wins
    for sec_idx, da in enumerate(result.domain_analyses):
        for f_idx, f in enumerate(da.findings):
            position.setdefault(f.id, (sec_idx, f_idx))
    if not position:
        return []

    text = str(text)
    ids = sorted(position, key=len, reverse=True)  # longest first, so a short id never cuts a long one
    pattern = re.compile(r"(?<!\w)(?:" + "|".join(re.escape(i) for i in ids) + r")(?!\w)")
    matches = list(pattern.finditer(text))

    found: list[str] = []

    def add(fid):
        if fid not in found:
            found.append(fid)

    for n, m in enumerate(matches):
        add(m.group())
        nxt = matches[n + 1] if n + 1 < len(matches) else None
        if nxt is None or text[m.end():nxt.start()].strip() not in ("–", "—", "-"):
            continue
        (sec_a, idx_a), (sec_b, idx_b) = position[m.group()], position[nxt.group()]
        if sec_a == sec_b and idx_a < idx_b:
            for f in result.domain_analyses[sec_a].findings[idx_a + 1:idx_b]:
                add(f.id)
    return found


def _build_all_findings(wb: Workbook, result: AnalysisResult):
    """One flat, filterable table of every finding, worst first. Detail columns are folded away."""
    ws = wb.create_sheet(_FINDINGS)
    _apply_app_style(ws)

    COLS = [
        "Ref.", "Severity", "Title", "What it means", "Recommended action",
        "Priority", "Effort", "How sure we are", "Section",
        # columns 10-19: grouped and collapsed
        "Risk area", "What the SAP report says", "Impact", "Why", "How to confirm",
        "SAP transactions", "Check latest SAP guidance first?", "Due date",
        "Reviewer note: why check first", "Reviewer note: search query",
    ]
    _hdr_row(ws, 1, COLS)
    ws.freeze_panes = "A2"

    rows = _findings_in_order(result)

    for i, (da, f) in enumerate(rows):
        r = 2 + i
        vals = [
            f.id, xs.severity_text(f.severity), f.title, f.description, f.remediation.action,
            f.remediation.priority, f.remediation.effort_estimate, xs.sure_dots(f.confidence),
            da.section_title,
            ", ".join(f.risk_types), f.evidence, f.impact, f.confidence_reason, f.to_confirm,
            ", ".join(f.remediation.sap_transactions), None, f.due_date,
            f.remediation.validation_reason, f.remediation.validation_query,
        ]
        for col, val in enumerate(vals, 1):
            c = ws.cell(row=r, column=col, value=val)
            c.font = _font()
        _guidance_cell(ws.cell(row=r, column=16), f.remediation.external_validation_required)

    xs.apply_table_style(ws, header=1, last_row=max(1, 1 + len(rows)), last_col=len(COLS))
    _set_widths(ws, 1, len(COLS))
    _collapse_group(ws, 10, len(COLS))


_SAP_VS_US = "SAP vs SoftwareONE"

# Results a reader should look at first: shown in bold.
_BOLD_RESULTS = {rd.RESULT_MORE, rd.RESULT_LESS, rd.RESULT_CHECK}


def _build_sap_vs_us(wb: Workbook, result: AnalysisResult):
    """SAP's own ratings next to ours: result counts on top, one row per alert/check below."""
    rows, analyses = result.reconciliation, result.domain_analyses
    ws = wb.create_sheet(_SAP_VS_US)
    _apply_app_style(ws)

    findings_by_id: dict = {}
    for da in analyses:
        for f in da.findings:
            findings_by_id.setdefault(f.id, f)
    row_by_id, _ = _finding_rows(result)
    displays = [rd.describe(row, findings_by_id) for row in rows]

    ws.cell(1, 1, _SAP_VS_US).font = _font(bold=True, size=16)
    xs.title_band(ws, 1, 1, 14)  # 14 = number of columns in the main table below
    ws.cell(2, 1, "SAP's own ratings next to ours. Bold results are worth a look. "
                  "Dots show how sure we are: "
                  f"{xs.DOT * 3} High, {xs.DOT * 2}{xs.EMPTY} Medium, {xs.DOT}{xs.EMPTY * 2} Low."
            ).font = _font(size=10, color=xs.NOTE)

    # Summary block: result counts, split by Alerts and Checks.
    counts = vd.sap_result_counts(rows, analyses)
    sum_hdr = 4
    xs.header_row(ws, sum_hdr, ["Result", None, None, "Alerts", "Checks", "Total"], numeric_cols=(4, 5, 6))
    for i, (result_name, alerts, checks) in enumerate(counts):
        r = sum_hdr + 1 + i
        ws.cell(r, 1, result_name).font = _font(bold=result_name in _BOLD_RESULTS)
        for col, val in ((4, alerts), (5, checks), (6, alerts + checks)):
            ws.cell(r, col, val).font = _font()
    sum_last = sum_hdr + len(counts)
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

    # Link (after styling): our finding -> its row on the Findings tab.
    for i, row in enumerate(rows):
        r = hdr + 1 + i
        fid = row.finding_ids[0] if row.finding_ids else None
        if fid in row_by_id and ws.cell(r, 6).value:
            ws.cell(r, 6).hyperlink = f"#'{_FINDINGS}'!A{row_by_id[fid]}"
            ws.cell(r, 6).font = _link_font()

    _set_widths(ws, hdr, len(COLS))
    _collapse_group(ws, 11, 14)


_HEATMAP = "Risk Heatmap"
_HEATMAP_GROUP_OVER = 25  # more section rows than this: fold them under one row per chapter


def _heat_fill(severity):
    colour = xs.SEVERITY_COLOURS[severity]
    return PatternFill("solid", start_color=colour, end_color=colour)


def _worst_of(severities):
    present = set(severities)
    return next((sev for sev in vd.SEVERITIES if sev in present), None)


def _legend(label, items):
    """One line: a plain label, then each item (coloured dots and a word) separated by spaces."""
    if not xs.RICH:
        return label + "   ".join(str(item) for item in items)
    blocks = [TextBlock(xs._inline(xs.NOTE), label)]
    for i, item in enumerate(items):
        if i:
            blocks.append(TextBlock(xs._inline(xs.TEXT), "    "))
        blocks.extend(item)
    return CellRichText(*blocks)


def _heat_legend():
    """One line: a coloured dot and the name for each severity."""
    return _legend("Colour = most serious finding:  ", [xs.severity_text(sev) for sev in vd.SEVERITIES])


def _add_cells(total: dict, cells: dict) -> None:
    """Add {type: (count, worst severity)} into a running total, in place."""
    for rt, (count, worst) in cells.items():
        old_count, old_worst = total.get(rt, (0, worst))
        total[rt] = (old_count + count, _worst_of([old_worst, worst]))


def _build_risk_heatmap(wb: Workbook, result: AnalysisResult) -> bool:
    """Sections down, risk types across. Number = findings, colour = most serious one.

    Returns False (no sheet) when there is nothing to show.
    """
    rows = vd.heatmap_rows(result)
    if not rows:
        return False
    types = vd.heatmap_columns(result)
    with_sap = bool(result.reconciliation)
    _, first_row_by_section = _finding_rows(result)

    ws = wb.create_sheet(_HEATMAP)
    _apply_app_style(ws)

    first_type = 3 if with_sap else 2
    findings_col = first_type + len(types)
    ncols = findings_col
    cols = ["Section"] + (["SAP rating"] if with_sap else []) + types + ["Findings"]

    ws.cell(1, 1, _HEATMAP)
    xs.title_band(ws, 1, 1, ncols)
    ws.cell(2, 1, "Number = findings of that risk type. Colour = the most serious of them. "
                  "A finding with two risk types counts in both.").font = _font(size=10, color=xs.NOTE)
    _hdr_row(ws, 3, cols)
    for col in range(first_type, ncols + 1):
        ws.cell(3, col).alignment = _align("center", "top", True)
    ws.freeze_panes = "A4"

    def put_grid(r, cells, findings, bold=False):
        for i, rt in enumerate(types):
            if rt not in cells:
                continue
            count, worst = cells[rt]
            c = ws.cell(r, first_type + i, count)
            c.font = _font(bold=True, color=xs.WHITE)
            c.fill = _heat_fill(worst)
        ws.cell(r, findings_col, findings if findings else xs.muted(xs.DASH)).font = _font(bold=bold)

    def finish_row(r):
        for col in range(1, ncols + 1):
            c = ws.cell(r, col)
            c.border = Border(bottom=Side(style="thin", color=xs.ROW_LINE))
            c.alignment = _align("center" if col >= first_type else "left", "center", wrap=(col == 1))

    # Plain list, or one folded group per chapter when the list is long.
    grouped = len(rows) > _HEATMAP_GROUP_OVER
    layout: list[tuple[str, object]] = []  # ("chapter", (title, rows)) or ("section", HeatRow)
    if grouped:
        chapters: dict = {}
        for row in rows:
            chapters.setdefault(row.chapter, []).append(row)
        for chapter in sorted(chapters, key=lambda ch: (ch[0] is None, ch[0] or 0)):
            layout.append(("chapter", (chapter[1], chapters[chapter])))
            layout.extend(("section", row) for row in chapters[chapter])
        ws.sheet_properties.outlinePr.summaryBelow = False
    else:
        layout = [("section", row) for row in rows]

    r = 3
    links: list[tuple[int, int]] = []  # (heatmap row, row on the Findings tab)
    for kind, item in layout:
        r += 1
        if kind == "chapter":
            title, members = item
            cells: dict[str, tuple[int, str]] = {}
            for m in members:
                _add_cells(cells, m.cells)
            ws.cell(r, 1, title).font = _font(bold=True)
            if with_sap:
                ratings = [m.sap_rating for m in members if m.sap_rating]
                best = min(ratings, key=lambda x: vd.RATING_ORDER[x], default=None)
                ws.cell(r, 2, xs.rating_text(best)).font = _font(bold=True)
            put_grid(r, cells, sum(m.findings for m in members), bold=True)
            finish_row(r)
            ws.row_dimensions[r].collapsed = True
            continue
        row = item
        ws.cell(r, 1, row.title).font = _font()
        if with_sap:
            ws.cell(r, 2, xs.rating_text(row.sap_rating)).font = _font()
        put_grid(r, row.cells, row.findings)
        finish_row(r)
        if row.section_id in first_row_by_section:
            links.append((r, first_row_by_section[row.section_id]))
        if grouped:
            ws.cell(r, 1).alignment = Alignment(horizontal="left", vertical="center", wrap_text=True, indent=1)
            ws.row_dimensions[r].outlineLevel = 1
            ws.row_dimensions[r].hidden = True
    for rr, findings_row in links:
        ws.cell(rr, 1).hyperlink = f"#'{_FINDINGS}'!A{findings_row}"
        ws.cell(rr, 1).font = _link_font()

    # Total row: distinct findings per type (a finding sits in one section, so section counts add up).
    r += 1
    totals: dict[str, tuple[int, str]] = {}
    for row in rows:
        _add_cells(totals, row.cells)
    ws.cell(r, 1, "Total").font = _font(bold=True)
    for i, rt in enumerate(types):
        if rt in totals:
            ws.cell(r, first_type + i, totals[rt][0]).font = _font(bold=True)
    ws.cell(r, findings_col, sum(row.findings for row in rows)).font = _font(bold=True)
    finish_row(r)
    for col in range(1, ncols + 1):
        ws.cell(r, col).border = Border(top=Side(style="thin", color=xs.NAVY),
                                        bottom=Side(style="thin", color=xs.ROW_LINE))

    ws.cell(r + 2, 1, _heat_legend())

    ws.column_dimensions["A"].width = 44
    if with_sap:
        ws.column_dimensions["B"].width = 14
    for col in range(first_type, findings_col):
        ws.column_dimensions[get_column_letter(col)].width = 14
    ws.column_dimensions[get_column_letter(findings_col)].width = 10
    return True


def _healthy_sections(result: AnalysisResult) -> list:
    """Coverage entries we analysed and found clean."""
    with_findings = {da.section_id for da in result.domain_analyses if da.findings}
    return [c for c in result.coverage
            if c.status == "analyzed" and c.section_id not in with_findings]


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

    _build_priority_actions(wb, result)
    _build_all_findings(wb, result)
    if result.reconciliation:
        _build_sap_vs_us(wb, result)
    _build_risk_heatmap(wb, result)
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

    # Open on Priority Actions (the first tab)
    wb.active = 0
    for i, ws in enumerate(wb.worksheets):
        ws.sheet_view.tabSelected = (i == 0)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(str(output_path))
