from __future__ import annotations

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from langchain_anthropic import ChatAnthropic
from langchain_openai import AzureChatOpenAI
from pydantic import ValidationError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ewa_pipeline.agents.orchestrator import _tokens  # noqa: E402
from ewa_pipeline.config import Config  # noqa: E402
from ewa_pipeline.models import (  # noqa: E402
    get_cross_ref_model,
    get_orchestrator_model,
    get_subagent_model,
    get_synthesis_model,
    structured,
)
from ewa_pipeline.tracking.cost_tracker import CostTracker  # noqa: E402

ENDPOINT = "https://example.services.ai.azure.com/anthropic"
CLAUDE = {"endpoint": ENDPOINT, "api_key": "synthetic-not-a-key", "max_output_tokens": 1234}


def make_config(**extra) -> Config:
    return Config.model_validate(
        {
            "azure_openai": {
                "endpoint": "https://example.openai.azure.com",
                "api_key": "synthetic-not-a-key",
                "api_version": "2025-03-01-preview",
                "deployments": {
                    "orchestrator": "claude-opus-5-5",
                    "specialist": "claude-sonnet-5-5",
                    **extra.pop("deployments", {}),
                },
            },
            "reasoning": {"orchestrator": "high", "deep": "none", **extra.pop("reasoning", {})},
            **extra,
        }
    )


class ProviderConfigTests(unittest.TestCase):
    def test_default_config_uses_azure_openai_everywhere(self) -> None:
        config = make_config()
        for role in ("orchestrator", "specialist", "cross_reference", "synthesis"):
            self.assertEqual("azure_openai", config.provider_for(role))
        for factory in (get_orchestrator_model, get_subagent_model,
                        get_cross_ref_model, get_synthesis_model):
            self.assertIsInstance(factory(config), AzureChatOpenAI)

    def test_unset_roles_follow_the_orchestrator_provider(self) -> None:
        config = make_config(providers={"orchestrator": "foundry_claude"}, claude=CLAUDE)
        self.assertEqual("foundry_claude", config.provider_for("cross_reference"))
        self.assertEqual("foundry_claude", config.provider_for("synthesis"))
        self.assertEqual("azure_openai", config.provider_for("specialist"))

    def test_role_with_its_own_deployment_defaults_to_azure_openai(self) -> None:
        config = make_config(
            providers={"orchestrator": "foundry_claude"},
            claude=CLAUDE,
            deployments={"synthesis": "gpt-5.6-sol"},
        )
        self.assertEqual("azure_openai", config.provider_for("synthesis"))
        self.assertEqual("foundry_claude", config.provider_for("cross_reference"))

    def test_explicit_role_provider_wins(self) -> None:
        config = make_config(
            providers={"synthesis": " Foundry_Claude "},
            claude=CLAUDE,
            deployments={"synthesis": "claude-opus-5-5"},
        )
        self.assertEqual("foundry_claude", config.provider_for("synthesis"))

    def test_invalid_provider_is_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            make_config(providers={"orchestrator": "bedrock"})

    def test_claude_role_without_endpoint_or_key_is_rejected(self) -> None:
        for claude in ({}, {"endpoint": ENDPOINT}, {"api_key": "synthetic-not-a-key"}):
            with self.assertRaises(ValidationError) as caught:
                make_config(providers={"specialist": "foundry_claude"}, claude=claude)
            self.assertIn("AZURE_ANTHROPIC_ENDPOINT", str(caught.exception))
            self.assertIn("AZURE_ANTHROPIC_API_KEY", str(caught.exception))


class ClaudeFactoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = make_config(
            providers={
                "orchestrator": "foundry_claude",
                "specialist": "foundry_claude",
                "cross_reference": "foundry_claude",
                "synthesis": "foundry_claude",
            },
            claude=CLAUDE,
            reasoning={"cross_reference": "medium", "synthesis": "xhigh"},
        )

    def test_every_factory_returns_a_claude_model(self) -> None:
        for factory, name in (
            (get_orchestrator_model, "claude-opus-5-5"),
            (get_subagent_model, "claude-sonnet-5-5"),
            (get_cross_ref_model, "claude-opus-5-5"),
            (get_synthesis_model, "claude-opus-5-5"),
        ):
            model = factory(self.config)
            self.assertIsInstance(model, ChatAnthropic)
            self.assertEqual(name, model.model)
            self.assertEqual(ENDPOINT, model.anthropic_api_url)
            self.assertEqual(1234, model.max_tokens)
            self.assertEqual(self.config.max_model_retries, model.max_retries)

    def test_effort_is_passed_through_with_adaptive_thinking(self) -> None:
        orchestrator = get_orchestrator_model(self.config)
        self.assertEqual("high", orchestrator.reasoning_effort)
        self.assertEqual({"type": "adaptive"}, orchestrator.thinking)
        self.assertEqual("medium", get_cross_ref_model(self.config).reasoning_effort)
        self.assertEqual("xhigh", get_synthesis_model(self.config).reasoning_effort)

    def test_none_effort_disables_thinking(self) -> None:
        specialist = get_subagent_model(self.config)
        self.assertEqual({"type": "disabled"}, specialist.thinking)
        self.assertEqual("low", specialist.reasoning_effort)

    def test_request_timeouts(self) -> None:
        self.assertEqual(self.config.request_timeout_seconds,
                         get_subagent_model(self.config).default_request_timeout)
        config = self.config.model_copy(update={"planning_timeout_seconds": 77})
        self.assertEqual(77, get_orchestrator_model(config).default_request_timeout)

    def test_endpoint_joins_to_the_foundry_messages_path(self) -> None:
        client = get_subagent_model(self.config)._client
        self.assertEqual(ENDPOINT + "/v1/messages", str(client._prepare_url("/v1/messages")))


class StructuredOutputTests(unittest.TestCase):
    def test_non_claude_models_keep_the_original_call(self) -> None:
        model = MagicMock()
        result = structured(model, dict)
        model.with_structured_output.assert_called_once_with(dict, include_raw=True)
        self.assertIs(model.with_structured_output.return_value, result)

    def test_claude_models_use_json_schema(self) -> None:
        model = ChatAnthropic(model="claude-sonnet-5-5", base_url=ENDPOINT,
                              api_key="synthetic-not-a-key")
        with patch.object(ChatAnthropic, "with_structured_output") as mocked:
            structured(model, dict)
        mocked.assert_called_once_with(dict, include_raw=True, method="json_schema")


class ClaudeCostTests(unittest.TestCase):
    def test_claude_fallback_pricing_and_cache_maths(self) -> None:
        tracker = CostTracker(pricing={})
        tracker.record("p", "claude-opus-5-5", 1_000_000, 100_000,
                       cached_input_tokens=400_000, cache_write_tokens=100_000)
        totals = tracker.to_dict()["totals"]
        # 500k plain at 4.00, 400k cached at 0.40, 100k written at 5.00, 100k output at 20.00
        self.assertAlmostEqual(2.0 + 0.16 + 0.5 + 2.0, totals["cost_usd"], places=6)

    def test_other_claude_models_have_prices(self) -> None:
        for model, expected in (("claude-sonnet-5-5", 2.0), ("claude-haiku-5-5", 0.1)):
            tracker = CostTracker(pricing={})
            tracker.record("p", model, 1_000_000, 0)
            self.assertAlmostEqual(expected, tracker.to_dict()["totals"]["cost_usd"], places=6)


class ClaudeUsageTests(unittest.TestCase):
    def test_usage_extraction_reads_anthropic_cache_details(self) -> None:
        raw = SimpleNamespace(
            usage_metadata={
                "input_tokens": 1000,
                "output_tokens": 50,
                "input_token_details": {"cache_read": 300, "cache_creation": 200},
            }
        )
        self.assertEqual((1000, 50, 300, 200), _tokens(raw))


if __name__ == "__main__":
    unittest.main()
