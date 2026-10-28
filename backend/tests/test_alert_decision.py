"""Live alert scorer: switched off by default, never raises, no real network."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ewa_pipeline.agents.alert_decision import CRITERIA, QUESTION, score_alerts
from ewa_pipeline.services.pipeline import _reconcile_safely
from ewa_pipeline.report.schemas import AnalysisResult, SapAlert, SapServiceSummary
from test_alert_match_trial import make_result
from test_decision_client import FakePost, FakeResponse, make_config, ok

TABLE = {"S-1": 0.97, "S-2": 0.6, "P-1": 0.1}


class RoutedPost:
    """Answers by finding id; alerts named in fail_alerts get an HTTP 500."""

    def __init__(self, table, fail_alerts=()):
        self.table, self.fail_alerts, self.calls = table, set(fail_alerts), []

    def __call__(self, url, **kwargs):
        self.calls.append(kwargs)
        state = kwargs["json"]["state"]
        if state["sap_alert"]["text"] in self.fail_alerts:
            return FakeResponse(status=500)
        return ok(self.table[state["finding"]["id"]])


class ScoreAlertsTests(unittest.TestCase):
    def setUp(self):
        data = make_result()
        self.result = AnalysisResult.model_validate(data)
        self.summary = SapServiceSummary.model_validate(data["sap_summary"])
        self.config = make_config(decision_enabled=True, decision_workers=2)

    def test_off_makes_no_call(self):
        post = RoutedPost(TABLE)
        self.assertEqual(score_alerts(self.result, self.summary, make_config(), post=post), {})
        self.assertEqual(post.calls, [])

    def test_scores_every_alert_and_finding(self):
        post = RoutedPost(TABLE)
        scores = score_alerts(self.result, self.summary, self.config, post=post)
        self.assertEqual(sorted(scores), [0, 1, 2])
        self.assertEqual(scores[0], TABLE)
        self.assertEqual(len(post.calls), 9)
        question = post.calls[0]["json"]["questions"]["answer"]
        self.assertEqual((question["instructions"], question["criteria"]), (QUESTION, CRITERIA))
        self.assertEqual(post.calls[0]["timeout"], 15.0)

    def test_alert_with_a_failed_call_is_dropped(self):
        post = RoutedPost(TABLE, fail_alerts={"User SYSTEM is active and valid."})
        scores = score_alerts(self.result, self.summary, self.config, post=post)
        self.assertEqual(sorted(scores), [0, 2])

    def test_first_alert_failing_stops_everything(self):
        post = FakePost(FakeResponse(status=500))
        self.assertEqual(score_alerts(self.result, self.summary, self.config, post=post), {})
        self.assertEqual(len(post.calls), 3)  # one alert x three findings, then stop

    def test_budget_stops_new_alerts(self):
        ticks = iter([0, 0, 1000, 1000, 1000])
        scores = score_alerts(self.result, self.summary, self.config, post=RoutedPost(TABLE),
                              clock=lambda: next(ticks))
        self.assertEqual(sorted(scores), [0])

    def test_never_raises(self):
        def boom(*args, **kwargs):
            raise RuntimeError("down")
        self.assertEqual(score_alerts(self.result, self.summary, self.config, post=boom), {})
        self.assertEqual(score_alerts(self.result, None, self.config), {})
        one_alert = SapServiceSummary(alerts=[SapAlert(rating="RED", text="x")], checks=[])
        no_findings = AnalysisResult.model_validate({**make_result(), "domain_analyses": []})
        self.assertEqual(score_alerts(no_findings, one_alert, self.config, post=RoutedPost(TABLE)), {})


class PipelineWiringTests(unittest.TestCase):
    def setUp(self):
        data = make_result()
        self.result = AnalysisResult.model_validate(data)
        self.summary = SapServiceSummary.model_validate(data["sap_summary"])

    def test_off_makes_no_scoring_call_and_matches_by_word_overlap(self):
        with patch("ewa_pipeline.agents.decision_client.requests.post") as post:
            rows = _reconcile_safely(self.result, self.summary, None, None, make_config())
        post.assert_not_called()
        self.assertEqual(len(rows), 3)
        self.assertNotIn("Decision-1", [r.match_method for r in rows])

    def test_scores_reach_reconcile_and_failures_fall_back(self):
        config = make_config(decision_enabled=True)
        with patch("ewa_pipeline.services.pipeline.score_alerts", return_value={2: {"P-1": 0.99}}):
            rows = _reconcile_safely(self.result, self.summary, None, None, config)
        self.assertEqual((rows[2].match_method, rows[2].finding_ids), ("Decision-1", ["P-1"]))
        with patch("ewa_pipeline.services.pipeline.score_alerts", side_effect=RuntimeError("boom")):
            rows = _reconcile_safely(self.result, self.summary, None, None, config)
        self.assertEqual(len(rows), 3)
        self.assertNotIn("Decision-1", [r.match_method for r in rows])


if __name__ == "__main__":
    unittest.main()
