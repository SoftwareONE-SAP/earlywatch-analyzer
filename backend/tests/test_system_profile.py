from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ewa_pipeline.indexer.system_profile import (  # noqa: E402
    extract_system_profile,
    profile_to_prompt_text,
)
from ewa_pipeline.report.schemas import SystemProfile  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
COREX = REPO / "samples" / "COREX_TP1_05_2026_files_html" / "COREX_TP1_05_2026.htm"
BSW = REPO / "samples" / "compare" / "lo_test" / "BSW_S4P_05_2026.xml"

COVER = (
    "<p>SAP Alert Service Report ABC Productive SAP S/4HANA 2023 "
    "Session No. Installation No. 0010000004616 0021220331 "
    "23.04.2026 27.04.2026 03.05.2026 EarlyWatch Alert</p>"
)

LANDSCAPE = """
<h2>Performance Indicators for TP1</h2>
<h2>Checks for TP1</h2>
<h2>3.1 Maintenance for SAP</h2>
<table><tr><td>System</td><td>SAP Product</td><td>Product Version</td></tr>
<tr><td>TP100002~ABAP</td><td>SAP NetWeaver</td><td>7.4</td></tr></table>
<table><tr><td>Related System</td><td>Database System</td><td>Database Version</td><td>DB ID</td></tr>
<tr><td>TP100002~ABAP</td><td>SAP HANA Database</td><td>2.00.088.00</td><td>TP1</td></tr></table>
<table><tr><td>Host</td><td>Operating System</td></tr>
<tr><td>h1</td><td>SUSE 15</td></tr><tr><td>h2</td><td>SUSE 15</td></tr><tr><td>h3</td><td></td></tr></table>
<table><tr><td>Transport Track</td><td>System Role</td><td>System ID</td><td>Installation Number</td></tr>
<tr><td>T</td><td>Test</td><td>TQ1</td><td>0000000001</td></tr>
<tr><td>T</td><td>Production</td><td>TP1</td><td>0000000002</td></tr></table>
<table><tr><td>Server</td><td>Analysis Start</td><td>Analysis End</td></tr>
<tr><td>a</td><td>27.04.2026</td><td>03.05.2026</td></tr>
<tr><td>b</td><td>28.04.2026</td><td>02.05.2026</td></tr></table>
"""


class UnitTests(unittest.TestCase):
    def test_cover_paragraph(self):
        p = extract_system_profile(COVER)
        self.assertEqual(
            (p.sid, p.system_role, p.session_number, p.installation_number),
            ("ABC", "Production", "0010000004616", "0021220331"),
        )
        self.assertEqual((p.period_start, p.period_end), ("2026-04-27", "2026-05-03"))
        self.assertEqual(set(p.sources.values()), {"cover"})

    def test_cover_wins_over_landscape(self):
        p = extract_system_profile(COVER + LANDSCAPE)
        self.assertEqual((p.sid, p.system_role, p.installation_number), ("ABC", "Production", "0021220331"))
        self.assertEqual(p.sources["installation_number"], "cover")
        # blanks are still filled by later sources
        self.assertEqual((p.product, p.product_version), ("SAP NetWeaver", "7.4"))
        self.assertEqual(p.sources["product"], "landscape:Product")

    def test_landscape_tables(self):
        p = extract_system_profile(LANDSCAPE)
        self.assertEqual((p.database, p.database_version, p.db_id), ("SAP HANA Database", "2.00.088.00", "TP1"))
        self.assertEqual(p.os, "SUSE 15")
        self.assertEqual((p.system_role, p.installation_number), ("Production", "0000000002"))
        self.assertEqual(p.sources["system_role"], "landscape:Transport Landscape")
        self.assertEqual((p.period_start, p.period_end), ("2026-04-27", "2026-05-03"))
        self.assertEqual(p.sources["period_start"], "hardware_capacity")

    def test_headings_fallback_ignores_sap(self):
        p = extract_system_profile("<h2>Indicators for TP1</h2><h2>Checks for TP1</h2><h2>Maintenance for SAP</h2>")
        self.assertEqual(p.sid, "TP1")
        self.assertEqual(p.sources, {"sid": "headings"})

    def test_empty_input_gives_empty_profile(self):
        for html in ("", "<p>Nothing here</p>", None):
            p = extract_system_profile(html)
            self.assertEqual(p.model_dump(exclude={"sources"}), SystemProfile().model_dump(exclude={"sources"}))
            self.assertEqual(p.sources, {})

    def test_prompt_text_skips_empty_fields_and_is_short(self):
        text = profile_to_prompt_text(SystemProfile(sid="TP1", product="SAP NetWeaver", product_version="7.4"))
        self.assertEqual(text, "System ID: TP1\nProduct: SAP NetWeaver 7.4")
        self.assertEqual(profile_to_prompt_text(SystemProfile()), "")
        self.assertLessEqual(len(profile_to_prompt_text(SystemProfile(os="x" * 2000))), 600)


class SampleTests(unittest.TestCase):
    """Each sample is converted once for the whole class (the .doc path takes ~30 s)."""

    @classmethod
    def setUpClass(cls):
        from converters.compact_html_converter import convert_html_to_compact_html
        from converters.doc_html_converter import convert_doc_to_html

        cls.corex = cls.bsw = None
        with tempfile.TemporaryDirectory() as tmp:
            if COREX.is_file():
                cls.corex = extract_system_profile(
                    convert_html_to_compact_html(COREX, Path(tmp) / "corex.compact.html"))
            if BSW.is_file():
                doc = Path(tmp) / "BSW_S4P_05_2026.doc"
                shutil.copy(BSW, doc)
                html_path = convert_doc_to_html(doc, Path(tmp) / "out")
                cls.bsw = extract_system_profile(
                    convert_html_to_compact_html(html_path, Path(tmp) / "bsw.compact.html"))

    def test_corex_sample(self):
        if self.corex is None:
            self.skipTest("COREX sample missing")
        p = self.corex
        self.assertEqual((p.sid, p.installation_number, p.system_role), ("TP1", "", ""))
        self.assertEqual((p.product, p.product_version), ("SAP NetWeaver", "7.4"))
        self.assertIn("HANA", p.database)
        self.assertEqual(p.database_version, "2.00.088.00")
        self.assertEqual((p.period_start, p.period_end), ("2026-04-27", "2026-05-03"))

    def test_bsw_sample(self):
        if self.bsw is None:
            self.skipTest("BSW sample missing")
        p = self.bsw
        self.assertEqual((p.sid, p.installation_number, p.system_role), ("S4P", "0021220331", "Production"))
        self.assertEqual((p.product, p.product_version), ("SAP S/4HANA", "2023"))
        self.assertIn("HANA", p.database)
        self.assertEqual((p.database_version, p.db_id), ("2.00.079.05", "H4P"))
        self.assertEqual((p.period_start, p.period_end), ("2026-04-27", "2026-05-03"))
        self.assertLess(len(profile_to_prompt_text(p)), 600)


if __name__ == "__main__":
    unittest.main()
