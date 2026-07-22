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

    def test_known_openai_model_uses_fallback_pricing(self) -> None:
        tracker = CostTracker(pricing={})

        tracker.record(
            "phase0_planning",
            "gpt-5.4",
            input_tokens=34094,
            output_tokens=8570,
        )

        usage = tracker.to_dict("sample")
        breakdown = usage["breakdown"][0]

        self.assertEqual(2.5, breakdown["pricing"]["input_per_1m"])
        self.assertEqual(0.25, breakdown["pricing"]["cached_input_per_1m"])
        self.assertEqual(15.0, breakdown["pricing"]["output_per_1m"])
        self.assertGreater(breakdown["total_cost_usd"], 0)
        self.assertGreater(usage["totals"]["cost_usd"], 0)

    def test_gpt_5_6_luna_deployment_uses_family_pricing_and_cache_writes(self) -> None:
        tracker = CostTracker(pricing={})

        tracker.record(
            "phase1_domain_analysis",
            "ewa-gpt-5.6-luna-prod",
            input_tokens=1_000_000,
            output_tokens=100_000,
            cached_input_tokens=200_000,
            cache_write_tokens=100_000,
        )

        usage = tracker.to_dict("sample")
        breakdown = usage["breakdown"][0]

        self.assertEqual(1.0, breakdown["pricing"]["input_per_1m"])
        self.assertEqual(0.1, breakdown["pricing"]["cached_input_per_1m"])
        self.assertEqual(1.25, breakdown["pricing"]["cache_write_per_1m"])
        self.assertEqual(6.0, breakdown["pricing"]["output_per_1m"])
        self.assertEqual(700_000, breakdown["billable_input_tokens"])
        self.assertAlmostEqual(0.7, breakdown["input_cost_usd"])
        self.assertAlmostEqual(0.02, breakdown["cached_input_cost_usd"])
        self.assertAlmostEqual(0.125, breakdown["cache_write_cost_usd"])
        self.assertAlmostEqual(0.6, breakdown["output_cost_usd"])
        self.assertAlmostEqual(1.445, breakdown["total_cost_usd"])

    def test_exact_deployment_pricing_overrides_family_fallback(self) -> None:
        tracker = CostTracker(
            pricing={
                "ewa-gpt-5.6-luna-prod": {
                    "input_per_1m": 9.0,
                    "cached_input_per_1m": 8.0,
                    "cache_write_per_1m": 7.0,
                    "output_per_1m": 6.0,
                }
            }
        )

        tracker.record("phase", "ewa-gpt-5.6-luna-prod", 1_000_000, 0)

        self.assertEqual(9.0, tracker.to_dict()["breakdown"][0]["pricing"]["input_per_1m"])


if __name__ == "__main__":
    unittest.main()
