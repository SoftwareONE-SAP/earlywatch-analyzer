"""Embedded base64 icons are classified like linked image files. Synthetic images only."""
from __future__ import annotations

import base64
import io
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from converters import compact_html_converter as chc  # noqa: E402
from converters.compact_html_converter import (  # noqa: E402
    _data_uri_label,
    convert_html_to_compact_html,
    count_unresolved_images,
)


def _uri(color, size=(16, 16), fmt="GIF", mime="gif") -> str:
    buf = io.BytesIO()
    Image.new("RGB", size, color).save(buf, fmt)
    return f"data:image/{mime};base64," + base64.b64encode(buf.getvalue()).decode()


def _convert(body: str) -> str:
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "r.htm"
        src.write_text(f"<html><body>{body}</body></html>", encoding="utf-8")
        return convert_html_to_compact_html(src, Path(tmp) / "r.compact.html")


class DataUriTests(unittest.TestCase):
    def test_green_and_red_icons(self):
        self.assertEqual(_data_uri_label(_uri((0, 170, 0))), "[GREEN]")
        self.assertEqual(_data_uri_label(_uri((200, 0, 0), fmt="PNG", mime="png")), "[RED]")

    def test_conversion_writes_rating_span(self):
        out = _convert(f'<p><img src="{_uri((0, 170, 0))}"> ok</p>')
        self.assertIn('data-rating="green"', out)
        self.assertNotIn("[IMAGE]", out)

    def test_garbage_base64_is_image(self):
        self.assertEqual(_data_uri_label("data:image/gif;base64,@@not-base64@@"), "[IMAGE]")
        garbage = "data:image/gif;base64," + base64.b64encode(b"not an image").decode()
        self.assertEqual(_data_uri_label(garbage), "[IMAGE]")

    def test_svg_is_image(self):
        svg = b'<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10"/>'
        self.assertEqual(_data_uri_label("data:image/svg+xml;base64," + base64.b64encode(svg).decode()), "[IMAGE]")

    def test_too_many_pixels_is_image(self):
        self.assertEqual(_data_uri_label(_uri((0, 170, 0), size=(600, 500))), "[IMAGE]")

    def test_too_many_bytes_is_image(self):
        original = chc._MAX_DATA_URI_BYTES
        chc._MAX_DATA_URI_BYTES = 10
        chc._classify_image_bytes.cache_clear()
        try:
            self.assertEqual(_data_uri_label(_uri((0, 170, 0))), "[IMAGE]")
        finally:
            chc._MAX_DATA_URI_BYTES = original
            chc._classify_image_bytes.cache_clear()


class PathTests(unittest.TestCase):
    def test_parent_folder_not_resolved(self):
        with tempfile.TemporaryDirectory() as tmp:
            inner = Path(tmp) / "inner"
            inner.mkdir()
            Image.new("RGB", (16, 16), (0, 170, 0)).save(Path(tmp) / "x.gif")
            Image.new("RGB", (16, 16), (0, 170, 0)).save(inner / "y.gif")
            self.assertIsNone(chc._resolve_image_src("../x.gif", str(inner)))
            self.assertIsNotNone(chc._resolve_image_src("y.gif", str(inner)))

    def test_count_unresolved(self):
        with tempfile.TemporaryDirectory() as tmp:
            Image.new("RGB", (16, 16), (0, 170, 0)).save(Path(tmp) / "here.gif")
            page = Path(tmp) / "r.htm"
            page.write_text(
                f'<html><body><img src="here.gif"><img src="gone.gif"><img src="../x.gif">'
                f'<img src="{_uri((0, 170, 0))}"></body></html>',
                encoding="utf-8",
            )
            self.assertEqual(count_unresolved_images(page), 2)


if __name__ == "__main__":
    unittest.main()
