"""Whole-workbook checks for the "minimal report" look: no fills, one font, plain view."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from openpyxl import load_workbook
from openpyxl.cell.rich_text import CellRichText

from ewa_pipeline.report.excel_generator import generate
from ewa_pipeline.report.schemas import (
    AnalysisTaskRecord, CrossReference, ReconciliationRow, SectionCoverage, SystemProfile,
)
from test_excel_generator import build_result


def full_result():
    """A result that makes every tab appear."""
    result = build_result()
    result.executive_summary = "Two things need attention."
    result.system_profile = SystemProfile(sid="PRD", product="SAP S/4HANA", product_version="2022",
                                          period_start="01.05.2026", period_end="31.05.2026")
    result.cross_references = [CrossReference(
        title="Kernel and SQL", related_findings=["F-001", "F-002"],
        correlation_description="Both slow the system.", combined_impact="Slow.",
        recommended_action="Fix both.")]
    result.coverage = [
        SectionCoverage(section_id="1", section_title="Software Configuration", analysis_task_id="T1",
                        status="analyzed"),
        SectionCoverage(section_id="4", section_title="Database", analysis_task_id="T2", status="analyzed"),
    ]
    result.analysis_tasks = [AnalysisTaskRecord(
        task_id="T1", title="Task", source_section_ids=["1"], source_content_chars=10, origin="plan")]
    result.reconciliation = [
        ReconciliationRow(source="Alert", verdict="Agree", sap_topic="Performance", sap_item="Slow SQL",
                          sap_rating="RED", our_section_id="2", our_section_title="Performance Indicators",
                          our_rating="RED", finding_ids=["F-002"]),
        ReconciliationRow(source="Check", verdict="Not covered", sap_topic="Database", sap_rating="YELLOW",
                          our_section_id="4"),
    ]
    return result


TREE = {"structure": [{"title": "Overview", "start_index": 1, "end_index": 3, "summary": "s",
                       "nodes": [{"title": "Child", "start_index": 2, "end_index": 3, "summary": "c"}]}]}


class WholeWorkbookStyleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "out.xlsx"
            generate(full_result(), path, tree=TREE)
            cls.wb = load_workbook(path, rich_text=True)

    def test_every_expected_tab_is_present(self):
        names = self.wb.sheetnames
        for name in ("How to read this workbook", "Executive Summary", "All Findings", "SAP vs SoftwareONE",
                     "No Issues Found", "Linked Issues", "Action Plan", "Document Structure",
                     "Token Usage", "Analysis Tasks", "Source Coverage"):
            self.assertIn(name, names)

    def test_no_solid_fills_anywhere(self):
        for ws in self.wb.worksheets:
            for cell in ws._cells.values():
                self.assertIn(cell.fill.fill_type, (None, ""), f"{ws.title}!{cell.coordinate}")

    def test_every_font_is_aptos_including_rich_text_runs(self):
        for ws in self.wb.worksheets:
            for cell in ws._cells.values():
                self.assertEqual(cell.font.name, "Aptos", f"{ws.title}!{cell.coordinate}")
                if isinstance(cell.value, CellRichText):
                    for part in cell.value:
                        if not isinstance(part, str):
                            self.assertEqual(part.font.rFont, "Aptos", f"{ws.title}!{cell.coordinate}")
                        else:
                            self.fail(f"plain run inside rich text at {ws.title}!{cell.coordinate}")

    def test_zoom_100_and_no_gridlines_on_every_tab(self):
        for ws in self.wb.worksheets:
            self.assertEqual(ws.sheet_view.zoomScale, 100, ws.title)
            self.assertFalse(ws.sheet_view.showGridLines, ws.title)

    def test_tables_repeat_their_header_row_when_printed(self):
        for ws in self.wb.worksheets:
            if ws.freeze_panes:
                self.assertTrue(ws.print_title_rows, ws.title)

    def test_all_tabs_print_a4_landscape_one_page_wide(self):
        for ws in self.wb.worksheets:
            self.assertEqual(ws.page_setup.orientation, "landscape", ws.title)
            self.assertEqual(int(ws.page_setup.paperSize), 9, ws.title)
            self.assertEqual(ws.page_setup.fitToWidth, 1, ws.title)


if __name__ == "__main__":
    unittest.main()
