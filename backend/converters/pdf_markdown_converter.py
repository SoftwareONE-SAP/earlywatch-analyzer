"""PDF to Markdown conversion using pymupdf4llm."""

from __future__ import annotations

import pymupdf4llm


def convert_pdf_to_markdown(pdf_path: str) -> str:
    """
    Convert a local PDF file to Markdown text.

    Uses pymupdf4llm page chunking to preserve section structure as much as possible.
    """
    page_chunks = pymupdf4llm.to_markdown(pdf_path, page_chunks=True)
    markdown = "\n\n".join(chunk.get("text", "") for chunk in page_chunks)
    return markdown.strip()
