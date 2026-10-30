"""Explorer page upload: best effort, never fails the run. Storage is mocked."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from azure.core.exceptions import ResourceNotFoundError
from workflow_orchestrator import EWAWorkflowOrchestrator


def _setup():
    clients = {}

    def get_blob_client(name):
        return clients.setdefault(name, Mock(name=name))

    container = Mock()
    container.get_blob_client.side_effect = get_blob_client
    service = Mock()
    service.get_container_client.return_value = container
    return service, clients


class ExplorerUploadTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.orch = EWAWorkflowOrchestrator.__new__(EWAWorkflowOrchestrator)

    async def test_uploads_explorer(self):
        service, clients = _setup()
        with patch("workflow_orchestrator.blob_service_client", service):
            names = await self.orch._upload_artifacts(
                "doc", {"workbook_bytes": b"x", "explorer_html": "<html></html>"})
        self.assertEqual(names["explorer"], "doc_explorer.html")
        kwargs = clients["doc_explorer.html"].upload_blob.call_args.kwargs
        self.assertEqual(kwargs["content_type"], "text/html; charset=utf-8")
        self.assertTrue(kwargs["overwrite"])

    async def test_missing_explorer_deletes_stale(self):
        service, clients = _setup()
        with patch("workflow_orchestrator.blob_service_client", service):
            names = await self.orch._upload_artifacts("doc", {"workbook_bytes": b"x"})
        self.assertNotIn("explorer", names)
        clients["doc_explorer.html"].delete_blob.assert_called_once()

    async def test_missing_explorer_ignores_not_found(self):
        service, clients = _setup()
        clients["doc_explorer.html"] = Mock()
        clients["doc_explorer.html"].delete_blob.side_effect = ResourceNotFoundError("gone")
        with patch("workflow_orchestrator.blob_service_client", service):
            names = await self.orch._upload_artifacts("doc", {"workbook_bytes": b"x"})
        self.assertEqual(names["workbook"], "doc_workbook.xlsx")

    async def test_explorer_upload_error_is_swallowed(self):
        service, clients = _setup()
        clients["doc_explorer.html"] = Mock()
        clients["doc_explorer.html"].upload_blob.side_effect = RuntimeError("storage down")
        with patch("workflow_orchestrator.blob_service_client", service):
            names = await self.orch._upload_artifacts(
                "doc", {"workbook_bytes": b"x", "explorer_html": "<html></html>"})
        self.assertEqual(names["workbook"], "doc_workbook.xlsx")
        clients["doc_workbook.xlsx"].upload_blob.assert_called_once()
        self.assertNotIn("explorer", names)


if __name__ == "__main__":
    unittest.main()
