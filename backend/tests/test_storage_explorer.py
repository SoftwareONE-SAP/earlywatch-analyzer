"""Explorer page listing, download headers and delete allowlist; storage stays offline."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi import HTTPException
from routers import storage_router


def _blob(name):
    return SimpleNamespace(name=name, last_modified=None, size=1)


class ExplorerStorageTests(unittest.IsolatedAsyncioTestCase):
    async def test_list_files_flags_explorer_per_run_and_hides_the_blob(self):
        client = Mock()
        client.get_container_client.return_value.list_blobs.return_value = [
            _blob(n) for n in (
                "A.doc", "A.html", "A_workbook.xlsx", "A_explorer.html",
                "B.doc", "B_workbook.xlsx",
            )
        ]
        state = Mock()
        state.read.return_value = SimpleNamespace(metadata={})
        with patch.object(storage_router, "blob_service_client", client), \
                patch.object(storage_router, "ProcessingStateStore", return_value=state):
            response = await storage_router.list_files(_user={})
        rows = {row["name"]: row for row in response["files"]}
        self.assertEqual(set(rows), {"A.doc", "B.doc"})
        self.assertTrue(rows["A.doc"]["explorer_available"])
        self.assertFalse(rows["B.doc"]["explorer_available"])

    async def test_download_missing_explorer_is_404(self):
        with patch.object(storage_router, "blob_service_client", Mock()), \
                patch.object(storage_router.storage_service, "get_text_content",
                             side_effect=FileNotFoundError):
            with self.assertRaises(HTTPException) as ctx:
                await storage_router.download_file("B_explorer.html", _user={})
        self.assertEqual(ctx.exception.status_code, 404)

    async def test_download_explorer_is_sandboxed(self):
        with patch.object(storage_router, "blob_service_client", Mock()), \
                patch.object(storage_router.storage_service, "get_text_content",
                             return_value="<html></html>"):
            response = await storage_router.download_file("A_explorer.html", _user={})
        self.assertIn("sandbox", response.headers["content-security-policy"])
        self.assertEqual(response.headers["x-content-type-options"], "nosniff")
        self.assertEqual(response.headers["cache-control"], "no-store")
        self.assertTrue(response.headers["content-type"].startswith("text/html"))
        self.assertTrue(response.headers["content-disposition"].startswith("inline"))

    async def test_download_other_file_has_no_csp(self):
        with patch.object(storage_router, "blob_service_client", Mock()), \
                patch.object(storage_router.storage_service, "get_bytes", return_value=b"x"):
            response = await storage_router.download_file("A_workbook.xlsx", _user={})
        self.assertNotIn("content-security-policy", response.headers)

    async def test_delete_allowlist_includes_explorer(self):
        client = Mock()
        container = client.get_container_client.return_value
        container.list_blobs.return_value = [_blob("A.doc"), _blob("A_explorer.html")]
        request = storage_router.DeleteAnalysisRequest(fileName="A.doc", baseName="A")
        with patch.object(storage_router, "blob_service_client", client):
            result = await storage_router.delete_analysis(request, _user={})
        self.assertIn("A_explorer.html", result["deleted_files"])


if __name__ == "__main__":
    unittest.main()
