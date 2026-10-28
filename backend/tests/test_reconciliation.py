"""SAP vs us: compare SAP's own ratings with our findings (no AI)."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ewa_pipeline.indexer.tree_navigator import flatten_tree
from ewa_pipeline.report.reconciliation import (
    _descendants,
    _heading_paths,
    _heading_score,
    _heading_words,
    _home_section,
    _section_texts,
    _statement_ids,
    _words,
    clean_title,
    reconcile,
)
from ewa_pipeline.report.schemas import (
    AnalysisResult,
    DomainAnalysis,
    Finding,
    SapAlert,
    SapCheck,
    SapServiceSummary,
    SectionCoverage,
    SystemProfile,
)

PROFILE = SystemProfile(sid="TP1", db_id="H4P")


def finding(fid: str, severity: str, title: str = "A finding", evidence: str = "") -> Finding:
    return Finding(
        id=fid, title=title, severity=severity, description="d", evidence=evidence, impact="i",
        remediation={"action": "a", "sap_transactions": [], "effort_estimate": "Low", "priority": "Short-term"},
    )


def analysis(section_id: str, *findings: Finding) -> DomainAnalysis:
    return DomainAnalysis(
        section_title=f"S{section_id}", section_id=section_id, findings=list(findings), overall_health="Warning"
    )


def cover(section_id: str, status: str = "analyzed") -> SectionCoverage:
    return SectionCoverage(section_id=section_id, section_title=f"S{section_id}", status=status)


def node(node_id: str, title: str, children: list | None = None, text: str = "") -> dict:
    raw = {"node_id": node_id, "title": title, "nodes": children or []}
    if text:
        raw["text"] = text
    return raw


TREE = {"structure": [
    node("0001", "4 Software Configuration for TP1", [
        node("0002", "4.1 Kernel Release *"),
        node("0003", "4.2 Support Packages", [node("0004", "4.2.1 Child Details")]),
    ]),
    node("0005", "5 Database Check for H4P"),
    node("0006", "6 Broken Section"),
    node("0007", "7 Skipped Section"),
]}


def make_result(analyses: list[DomainAnalysis], coverage: list[SectionCoverage]) -> AnalysisResult:
    return AnalysisResult(
        domain_analyses=analyses, cross_references=[], executive_summary="", overall_system_health="Warning",
        top_5_priority_actions=[], token_usage={}, coverage=coverage,
    )


def check(item: str, rating: str, topic: str = "Topic") -> SapCheck:
    return SapCheck(topic=topic, subtopic=item, rating=rating, raw_title=item)


class CleanTitleTests(unittest.TestCase):
    def test_strips_number_marker_sid_and_db_id(self):
        self.assertEqual(clean_title("4.2.1  Kernel   for TP1 *", "TP1", "H4P"), "kernel for")
        self.assertEqual(clean_title("5 Database Check for H4P", "TP1", "H4P"), "database check for")
        self.assertEqual(clean_title("Kernel Release", "", ""), "kernel release")

    def test_sid_only_removed_as_whole_word(self):
        self.assertEqual(clean_title("TP10 and TP1", "TP1"), "tp10 and")

    def test_only_one_trailing_marker(self):
        self.assertEqual(clean_title("Thing * *"), "thing *")


class CheckRowTests(unittest.TestCase):
    def setUp(self):
        self.result = make_result(
            [
                analysis("0002", finding("F-1", "Medium", "Kernel is old")),
                analysis("0004", finding("F-2", "High", "Child problem"), finding("F-3", "Low")),
                analysis("0005"),
            ],
            [cover("0002"), cover("0004"), cover("0005"), cover("0006", "failed"), cover("0007", "skipped")],
        )
        self.summary = SapServiceSummary(checks=[
            check("Kernel Release *", "YELLOW"),      # Agree (Medium = YELLOW)
            check("Support Packages", "GREEN"),       # child High rolls up: We rated higher
            check("Database Check for H4P", "YELLOW"),  # no findings: We rated lower
            check("Broken Section", "RED"),           # failed
            check("Skipped Section", "RED"),          # skipped
            check("Nothing Like This", "RED"),        # no section
            check("Kernel Release", "GRAY"),          # SAP not rated
        ])
        self.rows = {r.sap_item + r.sap_rating: r for r in reconcile(self.result, self.summary, TREE, PROFILE)}

    def verdicts(self):
        return [r.verdict for r in reconcile(self.result, self.summary, TREE, PROFILE)]

    def test_all_verdicts_present(self):
        self.assertEqual(
            self.verdicts(),
            ["Agree", "We rated higher", "We rated lower", "Not covered", "Not covered",
             "No detail section in report", "SAP not rated"],
        )

    def test_child_severity_rolls_up_to_parent(self):
        row = self.rows["Support PackagesGREEN"]
        self.assertEqual(row.our_rating, "RED")
        self.assertEqual(row.our_section_id, "0003")
        self.assertEqual(row.finding_ids, ["F-2", "F-3"])
        self.assertEqual(row.reason, "We raised F-2 (High) 'Child problem' and 1 more")

    def test_reasons(self):
        self.assertEqual(self.rows["Kernel Release *YELLOW"].reason, "We raised F-1 (Medium) 'Kernel is old'")
        self.assertEqual(self.rows["Database Check for H4PYELLOW"].reason, "No finding raised; section analysed")
        self.assertEqual(self.rows["Broken SectionRED"].reason, "Section failed analysis")
        self.assertEqual(self.rows["Skipped SectionRED"].reason, "Section skipped")
        self.assertEqual(self.rows["Nothing Like ThisRED"].reason, "No matching section in report")
        self.assertEqual(self.rows["Database Check for H4PYELLOW"].our_rating, "GREEN")

    def test_old_result_without_coverage_is_not_marked_skipped(self):
        self.result.coverage = []
        rows = reconcile(self.result, self.summary, TREE, PROFILE)
        self.assertEqual(rows[3].verdict, "We rated lower")


class AlertRowTests(unittest.TestCase):
    def setUp(self):
        self.result = make_result(
            [analysis("0002", finding("F-9", "High", "Standard users retain default passwords"))],
            [cover("0002")],
        )

    def run_alert(self, text: str, rating: str = "YELLOW"):
        summary = SapServiceSummary(alerts=[SapAlert(rating=rating, text=text)])
        return reconcile(self.result, summary, TREE, PROFILE)[0]

    def test_match_above_threshold(self):
        row = self.run_alert("Standard users have default password.")
        self.assertEqual(row.source, "Alert")
        self.assertGreaterEqual(row.match_score, 0.3)
        self.assertEqual(row.finding_ids, ["F-9"])
        self.assertEqual(row.our_section_id, "0002")
        self.assertEqual(row.our_rating, "RED")
        self.assertEqual(row.verdict, "We rated higher")
        self.assertEqual(row.match_method, "Word overlap")

    def test_title_only_score_rescues_long_evidence(self):
        self.result.domain_analyses[0].findings[0].evidence = " ".join(f"word{i}" for i in range(60))
        self.assertEqual(self.run_alert("Standard users default passwords", "RED").verdict, "Agree")

    def test_below_threshold_is_not_covered(self):
        row = self.run_alert("Backup of the database has not run for a week")
        self.assertLess(row.match_score, 0.3)
        self.assertEqual(row.verdict, "Not covered")
        self.assertEqual(row.finding_ids, [])
        self.assertEqual(row.our_rating, "")
        self.assertEqual(row.match_method, "")


class DecisionAlertTests(unittest.TestCase):
    """Decision-1 scores are passed in; nothing here touches the network."""

    def setUp(self):
        self.result = make_result(
            [
                analysis("0002", finding("F-1", "High", "Standard users retain default passwords")),
                analysis("0003", finding("F-2", "Medium", "Backup catalog is not maintained"),
                         finding("F-3", "Low", "Backup catalog size is growing")),
            ],
            [cover("0002"), cover("0003")],
        )

    def run_alert(self, text, scores, rating="RED", **kwargs):
        summary = SapServiceSummary(alerts=[SapAlert(rating=rating, text=text)])
        return reconcile(self.result, summary, TREE, PROFILE, alert_scores={0: scores}, **kwargs)[0]

    def test_no_scores_is_word_overlap_only(self):
        summary = SapServiceSummary(alerts=[
            SapAlert(rating="RED", text="Standard users have default password."),
            SapAlert(rating="RED", text="Something unrelated entirely"),
        ])
        for scores in (None, {}, {1: {}}):
            rows = reconcile(self.result, summary, TREE, PROFILE, alert_scores=scores)
            self.assertEqual([r.match_method for r in rows], ["Word overlap", ""])
            self.assertEqual(rows[0].reason, "We raised F-1 (High) 'Standard users retain default passwords'")
            self.assertEqual(rows[1].reason, "No finding matches this alert")

    def test_keep_band_rescues_a_word_overlap_miss(self):
        row = self.run_alert("Backups are stale", {"F-1": 0.1, "F-2": 0.99, "F-3": 0.3})
        self.assertEqual(row.match_method, "Decision-1")
        self.assertEqual(row.finding_ids, ["F-2"])
        self.assertEqual(row.match_score, 0.99)
        self.assertEqual(row.our_section_id, "0003")
        self.assertEqual(row.our_rating, "YELLOW")
        self.assertEqual(row.verdict, "We rated lower")
        self.assertEqual(row.reason, "Decision-1 match (p=0.99): We raised F-2 (Medium) 'Backup catalog is not maintained'")

    def test_keep_band_overrides_a_wrong_word_overlap_match(self):
        row = self.run_alert("Standard users have default password.", {"F-1": 0.2, "F-2": 0.95})
        self.assertEqual((row.match_method, row.finding_ids), ("Decision-1", ["F-2"]))
        self.assertEqual(row.match_score, 0.95)

    def test_non_decision_rows_keep_word_overlap_score(self):
        cases = [
            ("Standard users have default password.", {"F-1": 0.6, "F-2": 0.1}),
            ("Backups are stale", {"F-2": 0.7}),
            ("Standard users have default password.", {"F-1": 0.2}),
        ]
        for text, scores in cases:
            row = self.run_alert(text, scores)
            plain = self.run_alert(text, {})
            self.assertEqual(row.match_score, plain.match_score)
            self.assertNotEqual(row.match_method, "Decision-1")

    def test_close_runner_up_is_noted_only(self):
        row = self.run_alert("Backups are stale", {"F-2": 0.99, "F-3": 0.97, "F-1": 0.1})
        self.assertEqual(row.finding_ids, ["F-2"])
        self.assertTrue(row.reason.endswith("; also close, please check: F-3 'Backup catalog size is growing' (p=0.97)"))
        far = self.run_alert("Backups are stale", {"F-2": 0.99, "F-3": 0.90})
        self.assertNotIn("also close", far.reason)
        low = self.run_alert("Backups are stale", {"F-2": 0.52, "F-3": 0.50}, keep=0.5, possible=0.6)
        self.assertNotIn("also close", low.reason)

    def test_possible_band_keeps_word_overlap_row(self):
        row = self.run_alert("Standard users have default password.", {"F-1": 0.6, "F-2": 0.1})
        self.assertEqual(row.match_method, "Word overlap")
        self.assertEqual(row.verdict, "Agree")
        self.assertEqual(row.reason, "We raised F-1 (High) 'Standard users retain default passwords'; "
                                     "Decision-1 possible match, please check: F-1 'Standard users retain default passwords' (p=0.60)")

    def test_possible_band_without_word_overlap_stays_not_covered(self):
        row = self.run_alert("Backups are stale", {"F-2": 0.7})
        self.assertEqual((row.verdict, row.match_method, row.finding_ids), ("Not covered", "", []))
        self.assertEqual(row.reason, "No confirmed match. Possible match, please check: "
                                     "F-2 'Backup catalog is not maintained' (p=0.70)")

    def test_below_possible_flags_a_word_overlap_match(self):
        row = self.run_alert("Standard users have default password.", {"F-1": 0.2, "F-2": 0.1})
        self.assertEqual(row.match_method, "Word overlap")
        self.assertTrue(row.reason.endswith("; Decision-1 did not confirm this match"))
        miss = self.run_alert("Backups are stale", {"F-1": 0.2})
        self.assertEqual((miss.verdict, miss.reason), ("Not covered", "No finding matches this alert"))

    def test_unknown_finding_ids_are_ignored(self):
        row = self.run_alert("Backups are stale", {"GONE": 0.99})
        self.assertEqual((row.verdict, row.match_method), ("Not covered", ""))


class HeadingHelperTests(unittest.TestCase):
    def test_parent_heading_counts(self):
        tree = {"structure": [node("0001", "Top", [node("0002", "Mid heading", [node("0003", "Leaf")])])]}
        paths = _heading_paths(tree)
        self.assertEqual(paths["0003"], ["Top", "Mid heading", "Leaf"])
        self.assertEqual(paths["0001"], ["Top"])
        words = _words("Users with critical authorizations which should not be used in production")
        score, title = _heading_score(
            words, ["Top", "Critical authorizations, which should not be used in production", "Leaf"]
        )
        self.assertEqual((score >= 3, title), (True, "Critical authorizations, which should not be used in production"))

    def test_number_prefix_and_sid_are_ignored(self):
        self.assertEqual(
            _heading_words("4.2 Kernel Patch Level for TP1", "TP1", "H4P"), {"kernel", "patch", "level"}
        )
        score, _ = _heading_score({"kernel", "patch", "level"}, ["4.2 Kernel Patch Level for TP1"], "TP1", "H4P")
        self.assertEqual(score, 3)

    def test_filler_words_alone_score_zero(self):
        alert = _words("SAP HANA database: Recommended Audit configuration is not applied.")
        self.assertEqual(_heading_score(alert, ["SAP HANA Database TP1"], "TP1", "H4P"), (0, ""))
        # Only "configuration" survives from this heading, so it is not a hit either.
        self.assertEqual(_heading_score(alert, ["SAP HANA Database Configuration"]), (0, ""))

    def test_two_shared_words_is_not_a_hit(self):
        self.assertEqual(_heading_score({"backup", "catalog"}, ["Backup catalog"]), (0, ""))

    def test_heading_only_half_in_alert_is_not_a_hit(self):
        alert = {"critical", "authorizations", "which"}
        self.assertEqual(_heading_score(alert, ["Critical authorizations which allow anything goes"]), (0, ""))


class HeadingCheckTests(unittest.TestCase):
    """The heading check re-ranks Decision-1's own scores; nothing here touches the network."""

    TREE = {"structure": [
        node("0060", "5 Users with Critical Authorizations", [
            node("0068", "5.1 Critical authorizations, which allow to do anything", [
                node("0069", "5.1.1 Super User Accounts"),
            ]),
            node("0071", "5.2 Critical authorizations, which should not be used in production", [
                node("0072", "5.2.1 Users Authorized to Change or Display all Tables"),
            ]),
        ]),
        node("0080", "6 SAP HANA Database Configuration"),
        node("0081", "7 SAP HANA Database Audit"),
    ]}
    BSW4 = ("Users with critical authorizations, which should not be used in production "
            "in other client(s) than 000")
    BSW2 = "Users with critical authorizations, which allow to do anything in client 000"

    def setUp(self):
        self.a = finding("A-1", "High", "Super User Accounts have critical authorizations")
        self.b = finding("B-1", "Medium", "Users can change or display all tables")
        self.cfg = finding("C-1", "Low", "HANA database configuration drifts")
        self.audit = finding("D-1", "High", "Audit trail is not switched on")
        self.result = make_result(
            [analysis("0069", self.a), analysis("0072", self.b), analysis("0080", self.cfg),
             analysis("0081", self.audit)],
            [cover("0069"), cover("0072"), cover("0080"), cover("0081")],
        )

    def run_alert(self, text, scores, **kwargs):
        summary = SapServiceSummary(alerts=[SapAlert(rating="RED", text=text)])
        return reconcile(self.result, summary, self.TREE, PROFILE, alert_scores={0: scores}, **kwargs)[0]

    def test_switches_to_finding_under_the_alerts_own_heading(self):
        row = self.run_alert(self.BSW4, {"A-1": 0.97, "B-1": 0.75})
        self.assertEqual(row.finding_ids, ["B-1"])
        self.assertEqual((row.match_method, row.match_score), ("Report heading", 0.75))
        self.assertEqual(row.our_section_id, "0072")
        self.assertIn("also close, please check: A-1 'Super User Accounts have critical authorizations' (p=0.97)",
                      row.reason)
        self.assertIn('heading "5.2 Critical authorizations, which should not be used in production"', row.reason)

    def test_correct_top_pick_is_kept(self):
        row = self.run_alert(self.BSW2, {"A-1": 0.97, "B-1": 0.75})
        self.assertEqual((row.finding_ids, row.match_method), (["A-1"], "Decision-1"))

    def test_weak_candidate_is_ignored(self):
        row = self.run_alert(self.BSW4, {"A-1": 0.97, "B-1": 0.40})
        self.assertEqual((row.finding_ids, row.match_method), (["A-1"], "Decision-1"))

    def test_below_keep_is_untouched(self):
        scores = {"A-1": 0.70, "B-1": 0.69}
        with_check = self.run_alert(self.BSW4, scores)
        without = self.run_alert(self.BSW4, scores, heading_check=False)
        self.assertEqual(with_check, without)
        self.assertNotEqual(with_check.match_method, "Report heading")

    def test_filler_word_heading_does_not_beat_the_top_pick(self):
        text = "SAP HANA database: Recommended Audit configuration is not applied."
        row = self.run_alert(text, {"D-1": 0.95, "C-1": 0.90})
        self.assertEqual((row.finding_ids, row.match_method), (["D-1"], "Decision-1"))

    def test_switch_off_gives_identical_rows(self):
        for text, scores in ((self.BSW4, {"A-1": 0.97, "B-1": 0.75}), (self.BSW2, {"A-1": 0.97, "B-1": 0.75})):
            off = self.run_alert(text, scores, heading_check=False)
            self.assertEqual(off.match_method, "Decision-1")
            self.assertEqual(off.finding_ids, ["A-1"])
        on = self.run_alert(self.BSW2, {"A-1": 0.97, "B-1": 0.75})
        self.assertEqual(on, self.run_alert(self.BSW2, {"A-1": 0.97, "B-1": 0.75}, heading_check=False))


class HomeSectionTests(unittest.TestCase):
    ALERT = "At least one SQL statement causes unnecessary high load on the system"
    X = "9aaf8105bdad5308ab706eea28078d28"

    def sections(self, *raw_nodes):
        nodes = []
        for top in flatten_tree({"structure": list(raw_nodes)}):
            nodes.extend(_descendants(top))
        return _section_texts(nodes)

    def test_reworded_sentence_finds_the_right_section(self):
        texts = self.sections(
            node("0115", "14 Problematic SQL Statements",
                 text=f"<p>At least one SQL statement causes unnecessary high load.</p><table><tr><td>{self.X}</td></tr></table>"),
            node("0116", "15 Backup", text="<p>The last backup ran fine.</p>"),
        )
        home = _home_section(self.ALERT, texts)
        self.assertEqual(home.id, "0115")
        self.assertEqual(_statement_ids(finding("A-1", "High", evidence=f"statement {self.X} is slow")), {self.X})

    def test_service_summary_with_the_verbatim_alert_is_skipped(self):
        texts = self.sections(
            node("0010", "2 Service Summary", text=f"<p>{self.ALERT}</p>"),
            node("0115", "14 Problematic SQL Statements", text="<p>One SQL statement causes unnecessary high load.</p>"),
        )
        self.assertEqual(_home_section(self.ALERT, texts).id, "0115")

    def test_tie_gives_no_home_section(self):
        texts = self.sections(
            node("0115", "A", text="<p>SQL statement causes unnecessary high load.</p>"),
            node("0116", "B", text="<p>SQL statement causes unnecessary high load.</p>"),
        )
        self.assertIsNone(_home_section(self.ALERT, texts))

    def test_too_few_or_too_small_a_share_of_words_gives_none(self):
        texts = self.sections(node("0115", "A", text="<p>SQL statement runs.</p>"))
        self.assertIsNone(_home_section(self.ALERT, texts))  # only 2 shared words
        long_alert = "SQL statement causes unnecessary load but also memory disk network cpu swap paging"
        texts = self.sections(node("0115", "A", text="<p>SQL statement causes unnecessary load.</p>"))
        self.assertIsNone(_home_section(long_alert, texts))  # 4 shared words, under half of the alert's

class StatementCheckTests(unittest.TestCase):
    """The statement check re-ranks Decision-1's own scores; nothing here touches the network."""

    X = "9aaf8105bdad5308ab706eea28078d28"
    Y = "d6fd1e2f3a4b5c6d7e8f9a0b1c2d3e4f"
    ALERT = "At least one SQL statement causes unnecessary high load on the system"

    def tree(self, home_text=None):
        if home_text is None:
            home_text = f"<p>One SQL statement causes unnecessary high load.</p><table><tr><td>{self.X}</td></tr></table>"
        return {"structure": [
            node("0115", "14 Problematic SQL Statements", text=home_text),
            node("0120", "15 Expensive Statements"),
            node("0130", "16 Other Statements"),
        ]}

    def setUp(self):
        self.a = finding("A-1", "High", "Statement d6fd is slow", evidence=f"statement {self.Y}")
        self.b = finding("B-1", "Medium", "Statement 9aaf is slow", evidence=f"statement {self.X}")
        self.c = finding("C-1", "Low", "SQL section overview", evidence=f"see {self.X}")
        self.result = make_result(
            [analysis("0120", self.a), analysis("0130", self.b), analysis("0115", self.c)],
            [cover("0120"), cover("0130"), cover("0115")],
        )

    def run_alert(self, scores, text=None, tree=None, **kwargs):
        summary = SapServiceSummary(alerts=[SapAlert(rating="RED", text=text or self.ALERT)])
        tree = tree or self.tree()
        return reconcile(self.result, summary, tree, PROFILE, alert_scores={0: scores}, **kwargs)[0]

    def test_switches_to_the_finding_with_the_same_statement(self):
        row = self.run_alert({"A-1": 0.98, "B-1": 0.97, "C-1": 0.01})
        self.assertEqual(row.finding_ids, ["B-1"])
        self.assertEqual((row.match_method, row.match_score), ("Same SQL statement", 0.97))
        self.assertEqual(row.our_section_id, "0130")
        self.assertIn("please check: A-1 'Statement d6fd is slow' (p=0.98)", row.reason)
        self.assertIn(self.X, row.reason)

    def test_pick_that_already_has_the_statement_is_kept(self):
        row = self.run_alert({"B-1": 0.98, "A-1": 0.50})
        self.assertEqual((row.finding_ids, row.match_method), (["B-1"], "Decision-1"))

    def test_only_carrier_below_possible_does_not_switch(self):
        row = self.run_alert({"A-1": 0.98, "B-1": 0.40, "C-1": 0.01})
        self.assertEqual((row.finding_ids, row.match_method), (["A-1"], "Decision-1"))

    def test_home_section_without_a_statement_id_does_not_switch(self):
        tree = self.tree("<p>One SQL statement causes unnecessary high load.</p>")
        row = self.run_alert({"A-1": 0.98, "B-1": 0.97}, tree=tree)
        self.assertEqual((row.finding_ids, row.match_method), (["A-1"], "Decision-1"))

    def test_word_overlap_row_is_untouched(self):
        self.a.title = "SQL statement causes unnecessary high load on the system"
        row = self.run_alert({})
        self.assertEqual((row.finding_ids, row.match_method), (["A-1"], "Word overlap"))

    def test_switch_off_gives_identical_rows(self):
        scores = {"A-1": 0.98, "B-1": 0.97}
        off = self.run_alert(scores, statement_check=False)
        self.assertEqual((off.finding_ids, off.match_method), (["A-1"], "Decision-1"))
        self.assertEqual(off, self.run_alert(scores, tree=self.tree("<p>nothing useful</p>")))

    def test_missing_text_and_odd_input_do_not_raise(self):
        scores = {"A-1": 0.98, "B-1": 0.97}
        tree = {"structure": [node("0115", "14 Problematic SQL Statements")]}
        row = self.run_alert(scores, tree=tree)
        self.assertEqual(row.match_method, "Decision-1")
        self.assertEqual(self.run_alert(scores, text=" ").match_method, "Decision-1")
        self.assertEqual(reconcile(self.result, SapServiceSummary(alerts=[SapAlert(rating="RED", text="x")]), None,
                                   None, alert_scores={0: scores})[0].match_method, "Decision-1")

class EdgeCaseTests(unittest.TestCase):
    def test_none_or_empty_summary_gives_no_rows(self):
        result = make_result([], [])
        self.assertEqual(reconcile(result, None, TREE, PROFILE), [])
        self.assertEqual(reconcile(result, SapServiceSummary(), TREE, PROFILE), [])

    def test_odd_inputs_do_not_raise(self):
        summary = SapServiceSummary(checks=[check("Kernel", "RED")], alerts=[SapAlert(rating="", text="")])
        rows = reconcile(make_result([], []), summary, None, None)
        self.assertEqual([r.verdict for r in rows], ["Not covered", "No detail section in report"])

    def test_old_payload_defaults_to_empty_reconciliation(self):
        result = AnalysisResult.model_validate({
            "domain_analyses": [], "cross_references": [], "executive_summary": "",
            "overall_system_health": "Unknown", "top_5_priority_actions": [], "token_usage": {},
        })
        self.assertEqual(result.reconciliation, [])


if __name__ == "__main__":
    unittest.main()
