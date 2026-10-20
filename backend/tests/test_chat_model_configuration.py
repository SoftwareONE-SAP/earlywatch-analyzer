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


if __name__ == "__main__":
    unittest.main()
