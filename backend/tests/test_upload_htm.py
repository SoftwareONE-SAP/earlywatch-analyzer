"""/api/upload accepts .htm/.html reports. Azure storage is mocked."""
from __future__ import annotations

import asyncio
import base64
import io
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from fastapi import HTTPException
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from routers import storage_router  # noqa: E402


def _green_uri() -> str:
    buf = io.BytesIO()
    Image.new("RGB", (16, 16), (0, 170, 0)).save(buf, "GIF")
    return "data:image/gif;base64," + base64.b64encode(buf.getvalue()).decode()


class _FakeUpload:
    def __init__(self, filename: str, content: bytes):
        self.filename = filename
        self._content = content

    async def read(self) -> bytes:
        return self._content


def _upload(filename: str, html: str):
    client = MagicMock()
    with patch.object(storage_router, "blob_service_client", client):
        result = asyncio.run(storage_router.upload_file(
            file=_FakeUpload(filename, html.encode("utf-8")),
            customer_name="ACME",
            system_id="abc",
            start_date="2026-04-27",
            end_date="2026-05-03",
            _user={},
        ))
    return result, client


class UploadHtmlTests(unittest.TestCase):
    def test_htm_and_html_are_accepted(self):
        page = f"<html><body><p>Hi <img src='{_green_uri()}'></p></body></html>"
        for name in ("ABC_030526.htm", "ABC_030526.HTML"):
            result, client = _upload(name, page)
            self.assertEqual(result["filename"], "ABC_03_May_26.html")
            self.assertNotIn("warnings", result)
            blob = client.get_blob_client.return_value.upload_blob.call_args.args[0].decode()
            self.assertIn('data-rating="green"', blob)

    def test_other_types_rejected(self):
        with patch.object(storage_router, "blob_service_client", MagicMock()):
            with self.assertRaises(HTTPException) as ctx:
                asyncio.run(storage_router.upload_file(
                    file=_FakeUpload("ABC_030526.pdf", b"x"), customer_name="A", system_id="abc",
                    start_date="2026-04-27", end_date="2026-05-03", _user={}))
        self.assertEqual(ctx.exception.status_code, 400)
        self.assertIn(".htm", ctx.exception.detail)

    def test_directory_parts_in_filename_are_ignored(self):
        result, _ = _upload("..\..\evil/ABC_030526.htm", "<html><body><p>Hi</p></body></html>")
        self.assertEqual(result["filename"], "ABC_03_May_26.html")

    def test_warning_only_when_images_missing(self):
        result, _ = _upload("ABC_030526.htm", "<html><body><img src='r_files/a.gif'><img src='r_files/b.gif'></body></html>")
        self.assertEqual(len(result["warnings"]), 1)
        self.assertIn("2 images could not be found", result["warnings"][0])
        self.assertIn("ABC_030526_files", result["warnings"][0])


if __name__ == "__main__":
    unittest.main()
