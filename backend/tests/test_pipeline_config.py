from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ewa_pipeline.config import _build_env_config, load_config  # noqa: E402


class PipelineConfigTests(unittest.TestCase):
    def test_reasoning_efforts_are_loaded_for_orchestrator_and_deep_models(self) -> None:
        environment = {
            "AZURE_OPENAI_ENDPOINT": "https://example.openai.azure.com",
            "AZURE_OPENAI_API_KEY": "test-key",
            "V2_ORCHESTRATOR_MODEL": "gpt-5.6-sol",
            "V2_SPECIALIST_MODEL": "gpt-5.6-luna",
            "V2_ROUTER_MODEL": "gpt-5.4-nano",
            "ORCHESTRATOR_REASONING_EFFORT": "medium",
            "DEEP_REASONING_EFFORT": "low",
        }

        with patch.dict(os.environ, environment, clear=True):
            config = _build_env_config()

        self.assertEqual("medium", config.reasoning.orchestrator)
        self.assertEqual("low", config.reasoning.deep)

    def test_reasoning_efforts_are_required(self) -> None:
        environment = {
            "AZURE_OPENAI_ENDPOINT": "https://example.openai.azure.com",
            "AZURE_OPENAI_API_KEY": "test-key",
            "V2_ORCHESTRATOR_MODEL": "gpt-5.6-sol",
            "V2_SPECIALIST_MODEL": "gpt-5.6-luna",
            "V2_ROUTER_MODEL": "gpt-5.4-nano",
        }

        with patch.dict(os.environ, environment, clear=True):
            with self.assertRaisesRegex(
                FileNotFoundError,
                "ORCHESTRATOR_REASONING_EFFORT, DEEP_REASONING_EFFORT",
            ):
                _build_env_config()

    def test_config_file_still_gets_reasoning_from_environment(self) -> None:
        config_yaml = """
azure_openai:
  endpoint: https://example.openai.azure.com
  api_key: test-key
  api_version: 2025-03-01-preview
  deployments:
    orchestrator: gpt-5.6-sol
    specialist: gpt-5.6-luna
    router: gpt-5.4-nano
pricing: {}
"""
        environment = {
            "ORCHESTRATOR_REASONING_EFFORT": "high",
            "DEEP_REASONING_EFFORT": "medium",
        }

        with TemporaryDirectory() as directory:
            path = Path(directory) / "config.yaml"
            path.write_text(config_yaml, encoding="utf-8")
            with patch.dict(os.environ, environment, clear=True):
                config = load_config(path)

        self.assertEqual("high", config.reasoning.orchestrator)
        self.assertEqual("medium", config.reasoning.deep)


if __name__ == "__main__":
    unittest.main()
