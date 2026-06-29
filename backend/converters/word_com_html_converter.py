"""Convert Word documents to filtered HTML using Microsoft Word (Windows only)."""

from __future__ import annotations

import logging
import subprocess
import sys
import textwrap
from pathlib import Path

logger = logging.getLogger(__name__)

# wdFormatFilteredHTML
WORD_FILTERED_HTML_FORMAT = 10


class WordComNotAvailableError(RuntimeError):
    """Raised when Word COM automation is unavailable on this host."""


def is_windows() -> bool:
    return sys.platform == "win32"


def detect_word_document_kind(path: Path) -> str:
    """
    Detect the on-disk Word format.

    SAP EWA reports are often Word 2003 XML saved with a .doc extension,
    not legacy binary OLE .doc files.
    """
    with path.open("rb") as handle:
        head = handle.read(4096)
    if head.startswith(b"<?xml") or b"wordDocument" in head:
        return "word2003_xml"
    if head[:4] == b"\xd0\xcf\x11\xe0":
        return "ole_doc"
    if head[:2] == b"PK":
        return "ole_doc"
    return "unknown"


def convert_doc_to_html_word_com(
    doc_path: str | Path,
    output_dir: str | Path,
) -> Path:
    """
    Save a Word document as filtered HTML using locally installed Microsoft Word.

    This matches the manual workflow: Word -> Save As -> Web Page, Filtered.
    """
    if not is_windows():
        raise WordComNotAvailableError("Word COM conversion is only available on Windows.")

    doc_path = Path(doc_path).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    html_path = output_dir / f"{doc_path.stem}.htm"
    ps_script = textwrap.dedent(
        f"""
        $ErrorActionPreference = 'Stop'
        $docPath = '{doc_path.as_posix().replace("'", "''")}'
        $htmlPath = '{html_path.as_posix().replace("'", "''")}'
        $format = {WORD_FILTERED_HTML_FORMAT}
        $word = New-Object -ComObject Word.Application
        $word.Visible = $false
        $word.DisplayAlerts = 0
        try {{
            $doc = $word.Documents.Open($docPath)
            $doc.SaveAs2([ref]$htmlPath, [ref]$format)
            $doc.Close([ref]0)
        }} finally {{
            $word.Quit()
        }}
        """
    ).strip()

    logger.info("Converting %s to filtered HTML via Microsoft Word COM", doc_path.name)
    result = subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_script],
        capture_output=True,
        text=True,
        timeout=300,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip() or f"exit code {result.returncode}"
        raise WordComNotAvailableError(f"Word COM conversion failed: {detail}")

    if not html_path.is_file():
        # Word may write .html in some locales/versions.
        alt = html_path.with_suffix(".html")
        if alt.is_file():
            html_path = alt
        else:
            raise WordComNotAvailableError(
                f"Word COM completed but HTML was not created at {html_path}"
            )

    logger.info("Word COM HTML output: %s", html_path)
    return html_path
