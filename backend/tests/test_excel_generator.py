"""The Excel workbook has an All Findings tab and keeps the section-sheet layout."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

from ewa_pipeline.report.excel_generator import generate
from ewa_pipeline.report.schemas import (
    AnalysisResult, CrossReference, DomainAnalysis, Finding, ReconciliationRow, Remediation, SectionCoverage,
    SystemProfile,
)
from ewa_pipeline.tracking.token_tracker import TokenUsage


def _remediation(action: str) -> Remediation:
    return Remediation(
        action=action,
        sap_transactions=["SPAM"],
        effort_estimate="Medium",
        priority="Short-term",
    )


def old_style_finding() -> Finding:
    """Shaped like a finding saved before the new fields existed."""
    return Finding(
        id="F-001",
        title="Kernel release out of maintenance",
        severity="Medium",
        description="The kernel is old.",
        evidence="Kernel 753 [RED]",
        impact="No security patches.",
        remediation=_remediation("Upgrade the kernel."),
    )


def new_style_finding() -> Finding:
    return Finding(
        id="F-002",
        title="Expensive SQL statement",
        severity="Critical",
        description="One statement dominates database time.",
        evidence="Statement hash 4f3a9c uses 61% of DB time",
        impact="Slow dialog response.",
        remediation=_remediation("Tune the statement."),
        confidence="High",
        confidence_reason="The report rates it RED.",
        to_confirm="Check ST04 / DBACOCKPIT.",
        risk_types=["Performance", "Cost"],
        subject="4f3a9c",
        due_date="2026-12-31",
    )


def build_result() -> AnalysisResult:
    return AnalysisResult(
        domain_analyses=[
            DomainAnalysis(
                section_title="Software Configuration",
                section_id="1",
                findings=[old_style_finding()],
                overall_health="Warning",
            ),
            DomainAnalysis(
                section_title="Performance Indicators",
                section_id="2",
                findings=[new_style_finding()],
                overall_health="Critical",
            ),
        ],
        cross_references=[],
        executive_summary="Summary.",
        overall_system_health="Critical",
        top_5_priority_actions=["Tune the statement."],
        token_usage=TokenUsage(),
    )


def _headers(ws, row: int) -> list:
    return [c.value for c in ws[row]]


class ExcelGeneratorTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        path = Path(self._tmp.name) / "out.xlsx"
        generate(build_result(), path)
        self.wb = load_workbook(path)

    def test_all_findings_follows_executive_summary(self):
        names = self.wb.sheetnames
        self.assertEqual(names[0], "How to read this workbook")
        self.assertEqual(names[1], "Executive Summary")
        self.assertEqual(names[2], "All Findings")
        for expected in ("Software Configuration", "Performance Indicators", "Action Plan", "Token Usage"):
            self.assertIn(expected, names)

    def test_all_findings_rows_sorted_by_severity(self):
        ws = self.wb["All Findings"]
        headers = _headers(ws, 1)
        self.assertEqual(headers[:3], ["Ref.", "Section", "Severity"])
        self.assertIn("What the SAP report says", headers)
        self.assertIn("What it means", headers)
        self.assertEqual(ws.max_row, 3)  # header + exactly 2 findings

        rows = [dict(zip(headers, [c.value for c in ws[r]])) for r in (2, 3)]
        self.assertEqual([r["Severity"] for r in rows], ["● Critical", "● Medium"])

        new, old = rows
        self.assertEqual(new["Ref."], "F-002")
        self.assertEqual(new["Section"], "Performance Indicators")
        self.assertEqual(new["Risk area"], "Performance, Cost")
        self.assertEqual(new["How sure we are"], "●●● High")
        self.assertEqual(new["Why"], "The report rates it RED.")
        self.assertEqual(new["How to confirm"], "Check ST04 / DBACOCKPIT.")
        self.assertEqual(new["What the SAP report says"], "Statement hash 4f3a9c uses 61% of DB time")
        self.assertEqual(new["What it means"], "One statement dominates database time.")
        self.assertEqual(new["Due date"], "2026-12-31")
        self.assertEqual(new["Check latest SAP guidance first?"], "No")

        # Old-style finding: new fields render as empty cells (or a dash for How sure).
        self.assertIn(old["Risk area"], ("", None))
        self.assertEqual(old["How sure we are"], "—")
        self.assertIn(old["How to confirm"], ("", None))
        self.assertEqual(old["What the SAP report says"], "Kernel 753 [RED]")

    def test_finding_id_links_to_section_sheet(self):
        ws = self.wb["All Findings"]
        # Same "#'Sheet'!A1" style the Executive Summary already uses.
        target = ws["A2"].hyperlink.target or ws["A2"].hyperlink.location
        self.assertEqual(target, "#'Performance Indicators'!A3")

    def test_section_sheet_layout_kept_for_summary_formulas(self):
        ws = self.wb["Software Configuration"]
        self.assertEqual(ws["A3"].value, "F-001")
        self.assertEqual(ws["B3"].value, "● Medium")
        headers = _headers(ws, 2)
        self.assertEqual(headers[:2], ["Ref.", "Severity"])
        self.assertIn("What the SAP report says", headers)
        self.assertIn("What it means", headers)
        self.assertNotIn("Evidence", headers)
        self.assertNotIn("Description", headers)
        self.assertEqual(headers[-5:-2], ["How sure we are", "Risk area", "How to confirm"])

    def test_section_sheet_shows_new_fields(self):
        ws = self.wb["Performance Indicators"]
        headers = _headers(ws, 2)
        row = dict(zip(headers, [c.value for c in ws[3]]))
        self.assertEqual(row["How sure we are"], "●●● High")
        self.assertEqual(row["Risk area"], "Performance, Cost")
        self.assertEqual(row["How to confirm"], "Check ST04 / DBACOCKPIT.")

    def test_reviewer_notes_columns_are_grouped_and_collapsed(self):
        ws = self.wb["Performance Indicators"]
        headers = _headers(ws, 2)
        for name in ("Reviewer note: why check first", "Reviewer note: search query"):
            dim = ws.column_dimensions[get_column_letter(headers.index(name) + 1)]
            self.assertTrue(dim.hidden, name)
            self.assertEqual(dim.outlineLevel, 1, name)
        plan = self.wb["Action Plan"]
        plan_headers = _headers(plan, 1)
        dim = plan.column_dimensions[get_column_letter(plan_headers.index("Reviewer note: why check first") + 1)]
        self.assertTrue(dim.hidden)
        # Severity (column B) is never hidden: the Executive Summary counts it.
        self.assertFalse(ws.column_dimensions["B"].hidden)

    def test_executive_summary_formulas_still_use_columns_a_and_b(self):
        ws = self.wb["Executive Summary"]
        formulas = [
            str(c.value) for row in ws.iter_rows() for c in row
            if isinstance(c.value, str) and c.value.startswith("=")
        ]
        self.assertTrue(any("$A$3:$A$9999" in f and "COUNTA" in f for f in formulas))
        self.assertTrue(any("B$3:$B$9999" in f or "B3:B9999" in f.replace("$", "") for f in formulas))

    def test_executive_summary_counts_use_wildcard_for_dot_severity(self):
        # Severity cells read "● High", so the COUNTIF criteria need a leading wildcard.
        ws = self.wb["Executive Summary"]
        formulas = [
            str(c.value) for row in ws.iter_rows() for c in row
            if isinstance(c.value, str) and c.value.startswith("=COUNTIF")
        ]
        for word in ("Critical", "High", "Medium", "Low"):
            self.assertTrue(any(f.endswith(f',"*{word}")') for f in formulas), word)
        self.assertFalse(any(f.endswith(',"High")') for f in formulas))

    def test_section_named_all_findings_does_not_collide(self):
        result = build_result()
        result.domain_analyses[0].section_title = "All Findings"
        path = Path(self._tmp.name) / "collide.xlsx"
        generate(result, path)
        names = load_workbook(path).sheetnames
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(names[2], "All Findings")

    def test_how_to_read_is_first_and_active(self):
        self.assertEqual(self.wb.active.title, "How to read this workbook")
        selected = [ws.title for ws in self.wb.worksheets if ws.sheet_view.tabSelected]
        self.assertEqual(selected, ["How to read this workbook"])
        ws = self.wb["How to read this workbook"]
        self.assertEqual(ws.column_dimensions["A"].width, 100)
        text = "\n".join(str(c.value) for row in ws.iter_rows() for c in row if c.value)
        for expected in ("● Critical", "● Red", "●●● High", "●○○ Low", "Reviewer note"):
            self.assertIn(expected, text)

    def test_technical_tabs_are_hidden_and_the_rest_visible(self):
        self.assertEqual(self.wb["Token Usage"].sheet_state, "hidden")
        for name in ("How to read this workbook", "Executive Summary", "All Findings",
                     "Software Configuration", "Action Plan"):
            self.assertEqual(self.wb[name].sheet_state, "visible", name)

    def test_tab_order_front_tabs_sections_then_action_plan(self):
        names = self.wb.sheetnames
        self.assertEqual(names[:3], ["How to read this workbook", "Executive Summary", "All Findings"])
        self.assertLess(names.index("Performance Indicators"), names.index("Action Plan"))
        self.assertLess(names.index("Action Plan"), names.index("Token Usage"))


def _row(source, verdict, **kw) -> ReconciliationRow:
    return ReconciliationRow(source=source, verdict=verdict, **kw)


class SapVsUsTests(unittest.TestCase):
    def _generate(self, result):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "out.xlsx"
        generate(result, path)
        return load_workbook(path)

    def test_sap_vs_us_sheet_position_rows_and_counts(self):
        result = build_result()
        result.reconciliation = [
            _row("Alert", "Agree", sap_topic="Alerts", sap_item="Kernel old", sap_rating="RED",
                 our_section_id="1", our_section_title="Software Configuration",
                 our_rating="RED", finding_ids=["F-001", "F-003"], match_score=0.97, match_method="Decision-1"),
            _row("Alert", "Not covered", sap_item="Odd alert", sap_rating="YELLOW"),
            _row("Check", "Agree", sap_topic="Performance", sap_rating="GREEN", our_rating="GREEN"),
            _row("Check", "We rated higher", sap_topic="Hardware", sap_rating="YELLOW", our_rating="RED"),
        ]
        wb = self._generate(result)
        self.assertEqual(wb.sheetnames[:4],
                         ["How to read this workbook", "Executive Summary", "All Findings", "SAP vs SoftwareONE"])
        ws = wb["SAP vs SoftwareONE"]

        counts = {ws.cell(r, 1).value: (ws.cell(r, 4).value, ws.cell(r, 5).value, ws.cell(r, 6).value)
                  for r in range(5, 9)}
        self.assertEqual(counts["Agree"], (1, 1, 2))
        self.assertEqual(counts["We rate it more serious"], (0, 1, 1))
        self.assertEqual(counts["Not found in our analysis"], (1, 0, 1))

        hdr_row = next(r for r in range(1, 15) if ws.cell(r, 1).value == "SAP list")
        headers = _headers(ws, hdr_row)
        self.assertEqual(headers[:5], ["SAP list", "SAP topic", "What SAP says", "SAP rating", "SoftwareONE rating"])
        self.assertEqual(ws.max_row - hdr_row, 4)  # one row per reconciliation row
        first = dict(zip(headers, [c.value for c in ws[hdr_row + 1]]))
        self.assertEqual(first["Result"], "Agree")
        self.assertEqual(first["SAP rating"], "● Red")
        self.assertEqual(first["SoftwareONE rating"], "● Red")
        self.assertEqual(first["How sure we are"], "●●● High")
        self.assertEqual(first["Our finding"], "Kernel release out of maintenance (+1 more)")
        target = ws.cell(hdr_row + 1, headers.index("Our finding") + 1).hyperlink
        self.assertEqual(target.target or target.location, "#'Software Configuration'!A3")
        self.assertEqual(first["Reviewer note: refs"], "F-001, F-003")
        self.assertEqual(first["Reviewer note: score"], 0.97)
        self.assertEqual(first["Reviewer note: matched by"], "Decision-1")
        self.assertEqual(ws.freeze_panes, f"A{hdr_row + 1}")

        # Bold only for the results a reader should look at; reviewer notes are collapsed.
        result_col = headers.index("Result") + 1
        self.assertFalse(ws.cell(hdr_row + 1, result_col).font.b)  # Agree
        self.assertTrue(ws.cell(hdr_row + 4, result_col).font.b)   # more serious
        for name in headers:
            if name.startswith("Reviewer note"):
                self.assertTrue(ws.column_dimensions[get_column_letter(headers.index(name) + 1)].hidden, name)

        # No solid fills and no matching jargon in anything a reader can see.
        for row in ws.iter_rows():
            for cell in row:
                self.assertIn(cell.fill.fill_type, (None, ""), cell.coordinate)
                if cell.value is not None and not ws.column_dimensions[cell.column_letter].hidden:
                    for jargon in ("Decision", "p=", "overlap"):
                        self.assertNotIn(jargon, str(cell.value), cell.coordinate)

    def test_verified_healthy_rows_and_sap_disagrees(self):
        result = build_result()  # sections "1" and "2" have findings
        result.coverage = [
            SectionCoverage(section_id="1", section_title="Software Configuration", status="analyzed"),
            SectionCoverage(section_id="3", section_title="Hardware", status="analyzed"),
            SectionCoverage(section_id="4", section_title="Database", status="analyzed"),
            SectionCoverage(section_id="5", section_title="Security", status="failed"),
        ]
        result.reconciliation = [
            _row("Check", "Not covered", sap_topic="Database", sap_rating="YELLOW", our_section_id="4"),
            _row("Check", "Agree", sap_topic="Database", sap_rating="RED", our_section_id="4"),
        ]
        wb = self._generate(result)
        ws = wb["No Issues Found"]
        self.assertEqual(ws.max_row, 3)  # header + 2 healthy sections
        flag = "SAP flagged this — please review"
        rows = {ws.cell(r, 1).value: (ws.cell(r, 2).value, ws.cell(r, 3).value) for r in (2, 3)}
        self.assertEqual(rows["Hardware"], ("—", None))  # no SAP rating: muted dash, no note
        self.assertEqual(rows["Database"], ("● Red", flag))
        self.assertEqual(sum(1 for _, n in rows.values() if n == flag), 1)
        for r in (2, 3):
            self.assertIn(ws.cell(r, 2).fill.fill_type, (None, ""))
        self.assertNotIn("disagrees", " ".join(str(c.value) for row in ws.iter_rows() for c in row))

    def test_both_sheets_ordered_when_both_present(self):
        result = build_result()
        result.coverage = [SectionCoverage(section_id="9", section_title="Clean", status="analyzed")]
        result.reconciliation = [_row("Check", "Agree", sap_rating="GREEN")]
        names = self._generate(result).sheetnames
        self.assertEqual(names[2:5], ["All Findings", "SAP vs SoftwareONE", "No Issues Found"])

    def test_old_payload_has_neither_sheet(self):
        wb = self._generate(build_result())
        self.assertNotIn("Verified Healthy", wb.sheetnames)
        self.assertNotIn("SAP vs SoftwareONE", wb.sheetnames)
        self.assertNotIn("No Issues Found", wb.sheetnames)

    def test_coverage_without_healthy_sections_skips_sheet(self):
        result = build_result()
        result.coverage = [SectionCoverage(section_id="1", section_title="Software Configuration",
                                           status="analyzed")]
        self.assertNotIn("No Issues Found", self._generate(result).sheetnames)


class MinimalReportBaseStyleTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "out.xlsx"
        generate(build_result(), path)
        self.wb = load_workbook(path)

    def test_every_tab_is_plain_100_percent_no_gridlines(self):
        for ws in self.wb.worksheets:
            self.assertEqual(ws.sheet_view.zoomScale, 100, ws.title)
            self.assertFalse(ws.sheet_view.showGridLines, ws.title)

    def test_table_headers_are_bold_without_fill(self):
        ws = self.wb["All Findings"]
        for cell in ws[1]:
            self.assertTrue(cell.font.b)
            self.assertEqual(cell.font.name, "Aptos")
            self.assertIn(cell.fill.fill_type, (None, ""))
            self.assertEqual(cell.border.bottom.style, "medium")

    def test_no_cambria_and_header_not_blue(self):
        for ws in self.wb.worksheets:
            for row in ws.iter_rows():
                for cell in row:
                    if cell.value is not None:
                        self.assertNotEqual(cell.font.name, "Cambria")
                        self.assertNotEqual(cell.fill.fgColor.rgb, "004472C4")

    def test_only_front_tabs_have_navy_tab_colour(self):
        front = {"How to read this workbook", "Executive Summary", "All Findings",
                 "SAP vs SoftwareONE", "No Issues Found"}
        for ws in self.wb.worksheets:
            colour = ws.sheet_properties.tabColor
            if ws.title in front:
                self.assertTrue(colour is not None and colour.rgb.endswith("1F3864"), ws.title)
            else:
                self.assertIsNone(colour, ws.title)

    def test_print_setup_a4_landscape_one_page_wide(self):
        ws = self.wb["All Findings"]
        self.assertEqual(ws.page_setup.orientation, "landscape")
        self.assertEqual(int(ws.page_setup.paperSize), 9)
        self.assertEqual(ws.page_setup.fitToWidth, 1)
        self.assertEqual(ws.print_title_rows, "$1:$1")
        self.assertEqual(self.wb["Performance Indicators"].print_title_rows, "$2:$2")


class LinkedIssuesTests(unittest.TestCase):
    def test_linked_issues_tab_shows_titles_not_only_refs(self):
        result = build_result()
        result.cross_references = [CrossReference(
            title="Old kernel and slow SQL", related_findings=["F-001", "F-999"],
            correlation_description="Both hurt response time.", combined_impact="Slow system.",
            recommended_action="Fix both together.")]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "out.xlsx"
            generate(result, path)
            wb = load_workbook(path)
        self.assertNotIn("Cross-References", wb.sheetnames)
        ws = wb["Linked Issues"]
        self.assertEqual([c.value for c in ws[1]][:3], ["Title", "Related findings", "How they connect"])
        self.assertEqual(ws["B2"].value, "F-001 Kernel release out of maintenance\nF-999")
        self.assertEqual(ws.sheet_view.zoomScale, 100)
        how = " ".join(str(c.value) for row in wb["How to read this workbook"].iter_rows() for c in row)
        self.assertIn("Linked Issues", how)
        self.assertNotIn("Cross-References", how)
        names = wb.sheetnames
        self.assertLess(names.index("Linked Issues"), names.index("Action Plan"))


class ExecutiveSummaryStyleTests(unittest.TestCase):
    def _sheet(self, result):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "out.xlsx"
        generate(result, path)
        return load_workbook(path)["Executive Summary"]

    def _texts(self, ws):
        return [str(c.value) for row in ws.iter_rows() for c in row if c.value is not None]

    def test_health_line_and_written_summary(self):
        result = build_result()
        result.executive_summary = "The system needs attention soon."
        ws = self._sheet(result)
        self.assertEqual(ws["B2"].value, "Overall system health: ● CRITICAL")
        self.assertIn("The system needs attention soon.", self._texts(ws))

    def test_system_profile_line(self):
        result = build_result()
        result.system_profile = SystemProfile(sid="PRD", product="SAP S/4HANA", product_version="2022",
                                              period_start="01.05.2026", period_end="31.05.2026")
        texts = self._texts(self._sheet(result))
        line = next(t for t in texts if t.startswith("System PRD"))
        self.assertIn("SAP S/4HANA 2022", line)
        self.assertIn("01.05.2026", line)

    def test_top_actions_numbered_once(self):
        result = build_result()
        result.top_5_priority_actions = ["1. Patch the kernel.", "2) Tune the statement."]
        texts = self._texts(self._sheet(result))
        self.assertIn("1. Patch the kernel.", texts)
        self.assertIn("2. Tune the statement.", texts)

    def test_kpi_tiles_have_no_fill(self):
        ws = self._sheet(build_result())
        for row in ws.iter_rows():
            for cell in row:
                self.assertIn(cell.fill.fill_type, (None, ""), cell.coordinate)


def _finding(fid: str, severity: str) -> Finding:
    return Finding(
        id=fid, title=f"Finding {fid}", severity=severity,
        description="d", evidence="e", impact="i", remediation=_remediation("Fix."),
    )


class WorstSeverityTests(unittest.TestCase):
    def _summary_rows(self, result):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "out.xlsx"
        generate(result, path)
        ws = load_workbook(path)["Executive Summary"]
        hdr = next(r for r in ws.iter_rows() if r[2].value == "Worst severity")
        rows = []
        for r in range(hdr[0].row + 1, ws.max_row + 1):
            if ws.cell(row=r, column=2).value:
                rows.append((ws.cell(row=r, column=2).value, ws.cell(row=r, column=3).value))
        return rows

    def test_worst_severity_and_sorting(self):
        result = build_result()
        # Medium-only section listed first, but labelled "Healthy" by the AI.
        result.domain_analyses = [
            DomainAnalysis(section_title="Mild", section_id="1", overall_health="Healthy",
                           findings=[_finding("M-1", "Medium"), _finding("M-2", "Low")]),
            DomainAnalysis(section_title="Serious", section_id="2", overall_health="Healthy",
                           findings=[_finding("H-1", "Low"), _finding("H-2", "High")]),
        ]
        rows = self._summary_rows(result)
        self.assertEqual([r[0] for r in rows], ["Serious", "Mild"])
        self.assertEqual([r[1] for r in rows], ["● High", "● Medium"])

    def test_ties_sorted_by_finding_count(self):
        result = build_result()
        result.domain_analyses = [
            DomainAnalysis(section_title="One", section_id="1", overall_health="Warning", findings=[_finding("A-1", "High")]),
            DomainAnalysis(section_title="Two", section_id="2", overall_health="Warning",
                           findings=[_finding("B-1", "High"), _finding("B-2", "Low")]),
        ]
        self.assertEqual([r[0] for r in self._summary_rows(result)], ["Two", "One"])


if __name__ == "__main__":
    unittest.main()
