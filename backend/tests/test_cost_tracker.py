from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ewa_pipeline.tracking.cost_tracker import CostTracker  # noqa: E402


class CostTrackerTests(unittest.TestCase):
    def test_cached_input_tokens_are_costed_separately(self) -> None:
        tracker = CostTracker(
            pricing={
                "gpt-test": {
                    "input_per_1m": 2.0,
                    "cached_input_per_1m": 0.5,
                    "output_per_1m": 8.0,
                }
            }
        )

        tracker.record(
            "phase1_domain_analysis",
            "gpt-test",
            input_tokens=1000,
            output_tokens=200,
            cached_input_tokens=400,
        )

        usage = tracker.to_dict("sample")
        breakdown = usage["breakdown"][0]

        self.assertEqual(1000, breakdown["input_tokens"])
        self.assertEqual(400, breakdown["cached_input_tokens"])
        self.assertEqual(600, breakdown["billable_input_tokens"])
        self.assertAlmostEqual(0.0012, breakdown["input_cost_usd"])
        self.assertAlmostEqual(0.0002, breakdown["cached_input_cost_usd"])
        self.assertAlmostEqual(0.0016, breakdown["output_cost_usd"])
        self.assertAlmostEqual(0.003, breakdown["total_cost_usd"])
        self.assertEqual(400, usage["totals"]["cached_input_tokens"])
        self.assertEqual(600, usage["totals"]["billable_input_tokens"])

    def test_missing_cached_pricing_keeps_cached_cost_at_zero_and_notes_it(self) -> None:
        tracker = CostTracker(
            pricing={
                "gpt-test": {
                    "input_per_1m": 2.0,
                    "output_per_1m": 8.0,
                }
            }
        )

        tracker.record(
            "phase1_domain_analysis",
            "gpt-test",
            input_tokens=1000,
            output_tokens=0,
            cached_input_tokens=250,
        )

        usage = tracker.to_dict("sample")

        self.assertEqual(0.0, usage["breakdown"][0]["cached_input_cost_usd"])
        self.assertTrue(any("cached_input_per_1m" in note for note in usage["notes"]))


if __name__ == "__main__":
    unittest.main()
