"""Shared look and feel for the Excel report ("minimal report" style).

Plain, quiet styling: one font, no fills in the body, thin grey row lines,
coloured dots instead of coloured cells. The only fills are a navy frame:
title bands and table header rows. Everything here is presentation only.
"""
from __future__ import annotations

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.utils.indexed_list import IndexedList

try:  # rich text needs openpyxl >= 3.1
    from openpyxl.cell.rich_text import CellRichText, TextBlock
    from openpyxl.cell.text import InlineFont

    RICH = True
except ImportError:  # pragma: no cover - old openpyxl
    RICH = False

# One-line switch: change to "Calibri" if Aptos is not wanted.
FONT_NAME = "Aptos"
BODY_SIZE = 11

TEXT = "1F1F1F"
MUTED = "808080"
NOTE = "595959"
LINK = "0563C1"
NAVY = "1F3864"
WHITE = "FFFFFF"
ROW_LINE = "D9D9D9"
EMPTY_DOT = "BFBFBF"

RATING_COLOURS = {"RED": "C00000", "YELLOW": "E0A000", "GREEN": "548235"}
SEVERITY_COLOURS = {"Critical": "C00000", "High": "E46C0A", "Medium": "E0A000", "Low": "4F81BD"}
# Chart colours for the SAP-vs-us result labels (same text as visual_data.RESULT_ORDER).
RESULT_COLOURS = {
    "Agree": "548235",
    "We rate it more serious": "E46C0A",
    "We rate it less serious": "4F81BD",
    "Please check": "E0A000",
    "Not found in our analysis": "C00000",
    "Section not analysed": "808080",
    "No detail to compare": "BFBFBF",
    "SAP gave no rating": "D9D9D9",
}
RESULT_DEFAULT_COLOUR = "BFBFBF"
SURE_LEVELS = {"High": 3, "Medium": 2, "Low": 1}

DOT = "●"        # filled circle
EMPTY = "○"      # empty circle
DASH = "—"       # em dash

# Tabs that get the navy colour (the five front tabs).
FRONT_TABS = (
    "How to read this workbook",
    "Executive Summary",
    "All Findings",
    "SAP vs SoftwareONE",
    "No Issues Found",
    "Risk Heatmap",
)


def font(bold=False, size=BODY_SIZE, color=TEXT, italic=False, underline=None) -> Font:
    """Every Font in the report goes through here so name and size are always set."""
    return Font(name=FONT_NAME, size=size, bold=bold, italic=italic, color=color, underline=underline)


def init_workbook() -> Workbook:
    """New workbook whose default font is FONT_NAME (so empty cells match too)."""
    wb = Workbook()
    # Changing only the Normal style does not work; the first stored font is the real default.
    wb._fonts = IndexedList([Font(name=FONT_NAME, size=BODY_SIZE, family=2)])
    try:
        normal = next(s for s in wb._named_styles if s.name == "Normal")
        normal.font = Font(name=FONT_NAME, size=BODY_SIZE, family=2)
    except StopIteration:  # pragma: no cover
        pass
    return wb


def _bottom(style, color) -> Border:
    return Border(bottom=Side(style=style, color=color))


def navy_fill() -> PatternFill:
    return PatternFill("solid", start_color=NAVY, end_color=NAVY)


def title_band(ws, row, first_col, last_col, size=16, bold=True, underline=None) -> None:
    """Navy band across first_col..last_col on one row; any text in it becomes white."""
    for col in range(first_col, last_col + 1):
        c = ws.cell(row=row, column=col)
        c.fill = navy_fill()
        if c.value is not None:
            c.font = font(bold=bold, size=size, color=WHITE, underline=underline)


def header_row(ws, row, values, start_col=1, numeric_cols=()) -> None:
    """Navy fill, bold white text, thin navy line underneath."""
    for i, val in enumerate(values):
        col = start_col + i
        c = ws.cell(row=row, column=col, value=val)
        c.font = font(bold=True, color=WHITE)
        c.fill = navy_fill()
        c.border = _bottom("thin", NAVY)
        c.alignment = Alignment(
            horizontal="right" if col in numeric_cols else "left", vertical="top", wrap_text=True
        )


def apply_table_style(ws, header=1, first_data=None, last_row=None, last_col=None,
                      numeric_cols=(), filter=True) -> None:
    """Thin grey line under each data row, text left, numbers right, top aligned, wrapped."""
    first_data = first_data or header + 1
    last_row = last_row or ws.max_row
    last_col = last_col or ws.max_column
    for r in range(first_data, last_row + 1):
        for col in range(1, last_col + 1):
            c = ws.cell(row=r, column=col)
            c.border = _bottom("thin", ROW_LINE)
            c.alignment = Alignment(
                horizontal="right" if col in numeric_cols else "left", vertical="top", wrap_text=True
            )
    if filter and last_row >= header:
        ws.auto_filter.ref = f"A{header}:{get_column_letter(last_col)}{last_row}"


def apply_sheet_view(ws, freeze=None, zoom=100) -> None:
    """Gridlines off, plain zoom, optional freeze pane cell such as "A2"."""
    ws.sheet_view.showGridLines = False
    ws.sheet_view.zoomScale = zoom
    if freeze:
        ws.freeze_panes = freeze


def apply_print_setup(ws, repeat_row=None, title="SAP EarlyWatch Alert analysis") -> None:
    """A4 landscape, one page wide, header row repeated, page numbers in the footer."""
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_margins.left = ws.page_margins.right = 0.5
    ws.page_margins.top = ws.page_margins.bottom = 0.75
    ws.oddHeader.center.text = title
    ws.oddFooter.left.text = "Page &P of &N"
    ws.oddFooter.right.text = "&A"
    if repeat_row:
        ws.print_title_rows = f"{repeat_row}:{repeat_row}"


# -- Rich text helpers -------------------------------------------------------

def _inline(color, bold=False, size=BODY_SIZE):
    return InlineFont(rFont=FONT_NAME, sz=size, color=color, b=bold or None)


def _dots(dot_text, dot_colour, word, word_colour=TEXT, bold=False):
    """Coloured dot(s), a space, then a plain word. Falls back to plain text."""
    if not RICH:
        return f"{dot_text} {word}"
    return CellRichText(
        TextBlock(_inline(dot_colour), dot_text),
        TextBlock(_inline(word_colour, bold=bold), f" {word}"),
    )


def rating_text(rating):
    """SAP traffic light: "● Red". Unknown or empty values come back as muted text."""
    key = (rating or "").upper()
    if key not in RATING_COLOURS:
        return muted(rating.title() if rating else DASH)
    return _dots(DOT, RATING_COLOURS[key], key.title())


def severity_text(severity):
    """Finding severity: "● High"."""
    if severity not in SEVERITY_COLOURS:
        return muted(severity or DASH)
    return _dots(DOT, SEVERITY_COLOURS[severity], severity)


def sure_dots(level):
    """How sure we are: "●●● High", "●●○ Medium", "●○○ Low"; anything else is a muted dash."""
    n = SURE_LEVELS.get(level or "")
    if n is None:
        return muted(DASH)
    if not RICH:
        return f"{DOT * n}{EMPTY * (3 - n)} {level}"
    blocks = [TextBlock(_inline(NAVY), DOT * n)]
    if n < 3:
        blocks.append(TextBlock(_inline(EMPTY_DOT), EMPTY * (3 - n)))
    blocks.append(TextBlock(_inline(TEXT), f" {level}"))
    return CellRichText(*blocks)


def dot_label(dot_colour, word, size=BODY_SIZE, word_colour=TEXT, bold=False, prefix=""):
    """Optional plain prefix, a coloured dot, then a word, all at one size. Falls back to plain text."""
    if not RICH:
        return f"{prefix}{DOT} {word}"
    blocks = []
    if prefix:
        blocks.append(TextBlock(_inline(word_colour, bold=bold, size=size), prefix))
    blocks.append(TextBlock(_inline(dot_colour, bold=bold, size=size), DOT))
    blocks.append(TextBlock(_inline(word_colour, bold=bold, size=size), f" {word}"))
    return CellRichText(*blocks)


def legend_line(label, note):
    """A dots-and-word label (from rating_text etc.) followed by a plain explanation, as one cell value."""
    if not RICH or not isinstance(label, CellRichText):
        return f"{label} {DASH} {note}"
    return CellRichText(*label, TextBlock(_inline(TEXT), f" {DASH} {note}"))


def muted(text):
    """Grey text for "nothing here" values. Rich text when available."""
    if not RICH:
        return text
    return CellRichText(TextBlock(_inline(MUTED), str(text)))
