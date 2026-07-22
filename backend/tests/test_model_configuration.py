from __future__ import annotations

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ewa_pipeline.agents.orchestrator import _tokens  # noqa: E402
from ewa_pipeline.config import Config  # noqa: E402
from ewa_pipeline.models import get_orchestrator_model, get_subagent_model  # noqa: E402


class ModelConfigurationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = Config.model_validate(
            {
                "azure_openai": {
                    "endpoint": "https://example.openai.azure.com",
                    "api_key": "test-key",
                    "api_version": "2025-03-01-preview",
                    "deployments": {
                        "orchestrator": "gpt-5.6-sol",
                        "specialist": "gpt-5.6-luna",
                        "router": "gpt-5.4-nano",
                    },
                },
                "reasoning": {"orchestrator": "medium", "deep": "low"},
            }
        )

    def test_each_pipeline_model_receives_its_configured_reasoning_effort(self) -> None:
        self.assertEqual(
            "medium",
            get_orchestrator_model(self.config).reasoning_effort,
        )
        self.assertEqual(
            "low",
            get_subagent_model(self.config).reasoning_effort,
        )

    def test_usage_extraction_includes_cache_reads_and_writes(self) -> None:
        raw = SimpleNamespace(
            usage_metadata={
                "input_tokens": 100,
                "output_tokens": 20,
                "input_token_details": {
                    "cache_read": 30,
                    "cache_write_tokens": 10,
                },
            }
        )

        self.assertEqual((100, 20, 30, 10), _tokens(raw))


if __name__ == "__main__":
    unittest.main()
