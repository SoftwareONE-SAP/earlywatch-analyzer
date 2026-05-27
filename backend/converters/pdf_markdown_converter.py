"""PDF to Markdown conversion using Microsoft MarkItDown."""

from __future__ import annotations

from markitdown import MarkItDown


def convert_pdf_to_markdown(pdf_path: str) -> str:
    """
    Convert a local PDF file to Markdown text.

    Uses MarkItDown's local-file API to avoid accidental remote fetching.
    """
    converter = MarkItDown(enable_plugins=False)
    result = converter.convert_local(pdf_path)
    return (result.text_content or "").strip()
