"""Document chat uses the explicit Portal CHAT_MODEL setting with mocked model I/O."""
import asyncio
import os
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi import HTTPException
from routers.chat_router import ChatRequest, chat_with_document


class ChatModelTests(unittest.TestCase):
    def environment(self, **extra):
        return {"AZURE_OPENAI_API_KEY": "synthetic-not-a-key",
                "AZURE_OPENAI_ENDPOINT": "https://example.openai.azure.com/",
                "CHAT_REASONING_EFFORT": "medium", **extra}

    def request(self):
        return ChatRequest(message="Explain the synthetic metric", fileName="", documentContent="Synthetic metric 42.")

    def test_chat_uses_its_own_model_independently_of_analysis_or_legacy_names(self):
        env = self.environment(CHAT_MODEL=" chosen-chat ", ORCHESTRATOR_MODEL="analysis-planner",
                               V2_ORCHESTRATOR_MODEL="obsolete-chat")
        with patch.dict(os.environ, env, clear=True), patch("routers.chat_router.load_dotenv"), \
                patch("openai.AzureOpenAI") as client:
            client.return_value.responses.create.return_value = SimpleNamespace(output_text="Synthetic reply", usage=None)
            result = asyncio.run(chat_with_document(self.request(), _user={}))
        self.assertEqual(result, {"response": "Synthetic reply"})
        self.assertEqual(client.return_value.responses.create.call_args.kwargs["model"], "chosen-chat")
        self.assertEqual(client.return_value.responses.create.call_args.kwargs["reasoning"], {"effort": "medium"})

    def test_missing_chat_model_fails_before_model_call_even_when_legacy_name_exists(self):
        for value in ("", "   "):
            with self.subTest(value=value), patch.dict(os.environ, self.environment(CHAT_MODEL=value,
                    V2_ORCHESTRATOR_MODEL="obsolete-chat"), clear=True), patch("routers.chat_router.load_dotenv"), \
                    patch("openai.AzureOpenAI") as client:
                with self.assertRaises(HTTPException) as error:
                    asyncio.run(chat_with_document(self.request(), _user={}))
                self.assertIn("CHAT_MODEL", error.exception.detail)
                client.assert_not_called()

    def claude_environment(self, **extra):
        values = {"CHAT_PROVIDER": "foundry_claude", "CHAT_MODEL": "claude-chat",
                  "AZURE_ANTHROPIC_ENDPOINT": "https://example.services.ai.azure.com/anthropic",
                  "AZURE_ANTHROPIC_API_KEY": "synthetic-not-a-key", **extra}
        return self.environment(**values)

    def run_claude(self, history, **extra):
        request = ChatRequest(message="Explain the synthetic metric", fileName="",
                              documentContent="Synthetic metric 42.", chatHistory=history)
        reply = SimpleNamespace(
            content=[SimpleNamespace(type="thinking", thinking="hidden"),
                     SimpleNamespace(type="text", text="Claude reply")],
            usage=SimpleNamespace(input_tokens=5, output_tokens=7),
        )
        env = self.claude_environment(**extra)
        with patch.dict(os.environ, env, clear=True), patch("routers.chat_router.load_dotenv"), \
                patch("anthropic.AnthropicFoundry") as client, patch("openai.AzureOpenAI") as azure:
            client.return_value.messages.create.return_value = reply
            result = asyncio.run(chat_with_document(request, _user={}))
        azure.assert_not_called()
        return result, client

    def test_claude_provider_returns_text_blocks_and_maps_effort(self):
        history = [{"text": "old answer", "isUser": False}, {"text": "first", "isUser": True},
                   {"text": "second", "isUser": True}, {"text": "", "isUser": False},
                   {"text": "reply", "isUser": False}]
        result, client = self.run_claude(history)
        self.assertEqual(result, {"response": "Claude reply"})
        self.assertEqual(client.call_args.kwargs["base_url"], "https://example.services.ai.azure.com/anthropic")
        kwargs = client.return_value.messages.create.call_args.kwargs
        self.assertEqual(kwargs["model"], "claude-chat")
        self.assertIn("Synthetic metric 42.", kwargs["system"])
        self.assertIsInstance(kwargs["max_tokens"], int)
        self.assertEqual(kwargs["messages"], [
            {"role": "user", "content": "first\n\nsecond"},
            {"role": "assistant", "content": "reply"},
            {"role": "user", "content": "Explain the synthetic metric"},
        ])
        self.assertEqual(kwargs["thinking"], {"type": "adaptive"})
        self.assertEqual(kwargs["output_config"], {"effort": "medium"})

    def test_claude_provider_turns_thinking_off_for_none_effort(self):
        _, client = self.run_claude([], CHAT_REASONING_EFFORT="none")
        kwargs = client.return_value.messages.create.call_args.kwargs
        self.assertEqual(kwargs["thinking"], {"type": "disabled"})
        self.assertEqual(kwargs["output_config"], {"effort": "low"})

    def test_claude_provider_needs_its_own_environment_variables(self):
        env = self.claude_environment(AZURE_ANTHROPIC_API_KEY="")
        with patch.dict(os.environ, env, clear=True), patch("routers.chat_router.load_dotenv"), \
                patch("anthropic.AnthropicFoundry") as client:
            with self.assertRaises(HTTPException) as error:
                asyncio.run(chat_with_document(self.request(), _user={}))
        self.assertEqual(error.exception.status_code, 500)
        self.assertIn("Claude (Azure AI Foundry)", error.exception.detail)
        client.assert_not_called()

    def test_unknown_chat_provider_is_rejected(self):
        env = self.environment(CHAT_MODEL="chosen-chat", CHAT_PROVIDER="somewhere-else")
        with patch.dict(os.environ, env, clear=True), patch("routers.chat_router.load_dotenv"):
            with self.assertRaises(HTTPException) as error:
                asyncio.run(chat_with_document(self.request(), _user={}))
        self.assertEqual(error.exception.status_code, 500)
        self.assertIn("CHAT_PROVIDER", error.exception.detail)

    def test_empty_chat_provider_still_uses_azure_openai(self):
        env = self.environment(CHAT_MODEL="chosen-chat", CHAT_PROVIDER="  ")
        with patch.dict(os.environ, env, clear=True), patch("routers.chat_router.load_dotenv"), \
                patch("openai.AzureOpenAI") as client:
            client.return_value.responses.create.return_value = SimpleNamespace(output_text="Synthetic reply", usage=None)
            result = asyncio.run(chat_with_document(self.request(), _user={}))
        self.assertEqual(result, {"response": "Synthetic reply"})


if __name__ == "__main__":
    unittest.main()
