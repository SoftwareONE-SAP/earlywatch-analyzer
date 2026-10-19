"""CLI settings reach the web graph and real Responses adapter without network I/O."""
from __future__ import annotations

import json
import os
import sys
import unittest
from contextlib import ExitStack
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from openai import _base_client
from pydantic import ValidationError

from ewa_pipeline.config import Config, _build_env_config, load_config
from ewa_pipeline.models import (
    get_cross_ref_model, get_orchestrator_model, get_subagent_model, get_synthesis_model,
)
from ewa_pipeline.report.schemas import (
    CrossReferenceList, DomainAnalysis, OrchestratorPlan, SynthesisResult,
)


SETTINGS = {
    "AZURE_OPENAI_ENDPOINT": "https://example.openai.azure.com/",
    "AZURE_OPENAI_API_KEY": "synthetic-not-a-key",
    "V2_ORCHESTRATOR_MODEL": "legacy-planner",
    "V2_SPECIALIST_MODEL": "legacy-specialist",
    "V2_ROUTER_MODEL": "unchanged-router",
    "DEEP_REASONING_EFFORT": "low",
    "ORCHESTRATOR_MODEL": "gpt-6-luna",
    "SPECIALIST_MODEL": "gpt-6.1-sol",
    "ORCHESTRATOR_REASONING_EFFORT": "xhigh",
    "SPECIALIST_REASONING_EFFORT": "medium",
    "CROSS_REFERENCE_MODEL": "gpt-6.1-sol",
    "CROSS_REFERENCE_REASONING_EFFORT": "high",
    "SYNTHESIS_MODEL": "gpt-6.1-sol",
    "SYNTHESIS_REASONING_EFFORT": "high",
    "MAX_CONCURRENCY": "10",
    "REQUEST_TIMEOUT_SECONDS": "600",
    "PLANNING_TIMEOUT_SECONDS": "600",
    "MAX_TASK_SECTIONS": "12",
    "MAX_TASK_CONTENT_CHARS": "48000",
    "MAX_PARENT_CONTEXT_CHARS": "4000",
}


def configured():
    with patch.dict(os.environ, SETTINGS, clear=True):
        return _build_env_config()


class CLIAnalysisSettingsTests(unittest.TestCase):
    def test_cli_settings_override_legacy_aliases_and_keep_router(self):
        config = configured()
        self.assertEqual(config.azure_openai.deployments.orchestrator, "gpt-6-luna")
        self.assertEqual(config.azure_openai.deployments.specialist, "gpt-6.1-sol")
        self.assertEqual(config.azure_openai.deployments.router, "unchanged-router")
        self.assertEqual(config.reasoning.orchestrator, "xhigh")
        self.assertEqual(config.reasoning.deep, "medium")
        self.assertEqual(config.model_settings("cross_reference"), ("gpt-6.1-sol", "high"))
        self.assertEqual(config.model_settings("synthesis"), ("gpt-6.1-sol", "high"))
        self.assertEqual(config.max_concurrency, 10)
        self.assertEqual(config.request_timeout_seconds, 600)
        self.assertEqual(config.planning_timeout_seconds, 600)
        self.assertEqual(config.max_model_retries, 3)
        self.assertEqual(config.max_task_sections, 12)
        self.assertEqual(config.max_task_content_chars, 48000)
        self.assertEqual(config.max_parent_context_chars, 4000)

    def test_unset_downstream_settings_inherit_independently(self):
        config = configured()
        config.azure_openai.deployments.cross_reference = None
        config.reasoning.synthesis = None
        config.reasoning.cross_reference = "none"
        self.assertEqual(config.model_settings("cross_reference"), ("gpt-6-luna", "none"))
        self.assertEqual(config.model_settings("synthesis"), ("gpt-6.1-sol", "xhigh"))

    def test_blank_overrides_keep_legacy_environment_working(self):
        env = {**SETTINGS, "ORCHESTRATOR_MODEL": "", "SPECIALIST_MODEL": "",
               "SPECIALIST_REASONING_EFFORT": "", "CROSS_REFERENCE_MODEL": "",
               "CROSS_REFERENCE_REASONING_EFFORT": "", "SYNTHESIS_MODEL": "",
               "SYNTHESIS_REASONING_EFFORT": "", "MAX_CONCURRENCY": "",
               "REQUEST_TIMEOUT_SECONDS": "", "PLANNING_TIMEOUT_SECONDS": ""}
        with patch.dict(os.environ, env, clear=True):
            config = _build_env_config()
        self.assertEqual(config.azure_openai.deployments.orchestrator, "legacy-planner")
        self.assertEqual(config.azure_openai.deployments.specialist, "legacy-specialist")
        self.assertEqual(config.reasoning.deep, "low")
        self.assertEqual(config.model_settings("synthesis"), ("legacy-planner", "xhigh"))
        self.assertEqual(config.max_concurrency, 4)
        self.assertEqual(config.request_timeout_seconds, 180)
        self.assertIsNone(config.planning_timeout_seconds)

    def test_invalid_runtime_budgets_are_rejected(self):
        for key in ("MAX_CONCURRENCY", "REQUEST_TIMEOUT_SECONDS", "PLANNING_TIMEOUT_SECONDS",
                    "MAX_TASK_SECTIONS", "MAX_TASK_CONTENT_CHARS"):
            for value in ("0", "-1", "unbounded"):
                with self.subTest(key=key, value=value), patch.dict(os.environ, {**SETTINGS, key: value}, clear=True):
                    with self.assertRaises(ValidationError):
                        _build_env_config()

    def test_portal_grouping_overrides_and_zero_parent_context(self):
        with patch.dict(os.environ, {**SETTINGS, "MAX_TASK_SECTIONS": "2",
                                    "MAX_TASK_CONTENT_CHARS": "3000", "MAX_PARENT_CONTEXT_CHARS": "0"}, clear=True):
            config = _build_env_config()
        self.assertEqual((config.max_task_sections, config.max_task_content_chars, config.max_parent_context_chars),
                         (2, 3000, 0))
        with patch.dict(os.environ, {**SETTINGS, "MAX_PARENT_CONTEXT_CHARS": "-1"}, clear=True):
            with self.assertRaises(ValidationError):
                _build_env_config()

    def test_yaml_runtime_values_override_environment(self):
        config = configured()
        data = config.model_dump()
        data.update(max_concurrency=2, request_timeout_seconds=300, planning_timeout_seconds=None)
        import yaml
        with TemporaryDirectory() as directory, patch.dict(os.environ, SETTINGS, clear=True):
            path = Path(directory) / "config.yaml"
            path.write_text(yaml.safe_dump(data), encoding="utf-8")
            actual = load_config(path)
        self.assertEqual(actual.max_concurrency, 2)
        self.assertEqual(actual.request_timeout_seconds, 300)
        self.assertIsNone(actual.planning_timeout_seconds)

    def test_each_role_sends_its_deployment_reasoning_and_timeout(self):
        config = configured()
        config.planning_timeout_seconds = 900
        http = getattr(_base_client, "httpx2", None) or _base_client.httpx
        for factory, deployment, effort, timeout in (
            (get_orchestrator_model, "gpt-6-luna", "xhigh", 900),
            (get_subagent_model, "gpt-6.1-sol", "medium", 600),
            (get_cross_ref_model, "gpt-6.1-sol", "high", 600),
            (get_synthesis_model, "gpt-6.1-sol", "high", 600),
        ):
            with self.subTest(role=factory.__name__):
                requests = []

                def respond(request):
                    requests.append(request)
                    return http.Response(200, json={
                        "id": "resp_synthetic", "object": "response", "created_at": 0,
                        "status": "completed", "model": deployment,
                        "output": [{"id": "msg_synthetic", "type": "message",
                                    "status": "completed", "role": "assistant",
                                    "content": [{"type": "output_text", "annotations": [],
                                                 "text": '{"tasks": [], "planning_notes": "Synthetic only"}'}]}],
                        "usage": {"input_tokens": 10, "output_tokens": 10, "total_tokens": 20},
                        "error": None, "incomplete_details": None,
                        "parallel_tool_calls": True, "tools": [], "tool_choice": "auto",
                    })

                model = factory(config)
                self.assertEqual(model.max_retries, 3)
                model.root_client._client.close()
                model.root_client._client = http.Client(transport=http.MockTransport(respond))
                try:
                    result = model.with_structured_output(OrchestratorPlan, include_raw=True).invoke("Synthetic only")
                    self.assertIsInstance(result["parsed"], OrchestratorPlan)
                    self.assertEqual(len(requests), 1)
                    payload = json.loads(requests[0].content)
                    self.assertEqual(payload["model"], deployment)
                    self.assertEqual(payload["reasoning"], {"effort": effort})
                    self.assertNotIn("temperature", payload)
                    self.assertEqual(requests[0].extensions["timeout"]["read"], timeout)
                finally:
                    model.root_client.close()

    def test_full_graph_uses_separate_roles_and_runner_concurrency(self):
        from ewa_pipeline.agents import orchestrator, runner
        from ewa_pipeline.indexer.tree_navigator import TreeNode
        from ewa_pipeline.tracking.cost_tracker import CostTracker

        config = configured()
        registry = Mock()
        registry.catalog_text.return_value = "Synthetic skill catalog"
        registry.suggest_references.return_value = []
        registry.resolve_context.return_value = "Synthetic context"
        parsed = (
            OrchestratorPlan(tasks=[{"section_ids": ["0001"], "section_title": "Synthetic",
                                     "analysis_focus": "Review synthetic values"}]),
            DomainAnalysis(section_id="0001", section_title="Synthetic", findings=[], overall_health="Healthy"),
            CrossReferenceList(items=[]),
            SynthesisResult(executive_summary="Synthetic summary", overall_system_health="Healthy",
                            top_5_priority_actions=[]),
        )
        tracker = CostTracker({})
        with ExitStack() as stack:
            factories = []
            for name, result in zip(
                ("get_orchestrator_model", "get_subagent_model", "get_cross_ref_model", "get_synthesis_model"), parsed
            ):
                factory = stack.enter_context(patch.object(orchestrator, name))
                factory.return_value.with_structured_output.return_value.invoke.return_value = {
                    "parsed": result,
                    "raw": SimpleNamespace(usage_metadata={"input_tokens": 10, "output_tokens": 5}),
                }
                factories.append(factory)
            graph = orchestrator.build_ewa_graph(config, tracker, registry)
            wrapped = Mock(wraps=graph)
            stack.enter_context(patch.object(runner, "build_ewa_graph", return_value=wrapped))
            stack.enter_context(patch.object(runner.SkillRegistry, "from_dir", return_value=registry))
            result = runner.run_analysis(config, {"structure": []}, {},
                                         [TreeNode(id="0001", title="Synthetic", content="Synthetic values")],
                                         Path("unused-synthetic-skills"), tracker)
            for factory in factories:
                factory.assert_called_once_with(config)
        self.assertEqual(wrapped.stream.call_args.kwargs["config"], {"max_concurrency": 10})
        self.assertEqual(result.executive_summary, "Synthetic summary")
        self.assertEqual(len(result.domain_analyses), 1)
        self.assertEqual(tracker._entries["phase0_planning"].model, "gpt-6-luna")
        for phase in ("phase1_domain_analysis", "phase2_cross_reference", "phase2_synthesis"):
            self.assertEqual(tracker._entries[phase].model, "gpt-6.1-sol")
            self.assertEqual(tracker._entries[phase].calls, 1)


if __name__ == "__main__":
    unittest.main()
