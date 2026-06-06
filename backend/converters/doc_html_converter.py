"""Convert Word .doc/.docx files to HTML (WordML, Word COM, or LibreOffice)."""

from __future__ import annotations

import base64
import binascii
import html
import logging
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from xml.etree import ElementTree as ET

from converters.html_markdown_converter import classify_icon
from converters.word_com_html_converter import (
    WordComNotAvailableError,
    convert_doc_to_html_word_com,
    detect_word_document_kind,
    is_windows,
)

logger = logging.getLogger(__name__)

DEFAULT_SOFFICE_PATHS = (
    os.environ.get("LIBREOFFICE_PATH"),
    "soffice",
    r"C:\Program Files\LibreOffice\program\soffice.exe",
    r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
    "/usr/bin/soffice",
    "/usr/bin/libreoffice",
)


class LibreOfficeNotFoundError(RuntimeError):
    """Raised when the LibreOffice/soffice binary cannot be located."""


class DocConversionError(RuntimeError):
    """Raised when document conversion to HTML fails."""


_NON_FATAL_LIBREOFFICE_WARNINGS = (
    "warning: failed to launch javaldx - java may not function correctly",
)

WORDML_NS = "http://schemas.microsoft.com/office/word/2003/wordml"
WORDML = f"{{{WORDML_NS}}}"
WORDML_NAME = f"{WORDML}name"
WORDML_VAL = f"{WORDML}val"


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _image_extension(data: bytes) -> str | None:
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    if data.startswith((b"GIF87a", b"GIF89a")):
        return ".gif"
    if data.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    return None


def _wordml_image_labels(root: ET.Element, output_dir: Path, source_stem: str) -> dict[str, str]:
    labels: dict[str, str] = {}
    assets_dir = output_dir / f"{source_stem}_files"
    for index, bin_data in enumerate(root.findall(f".//{WORDML}binData")):
        name = bin_data.attrib.get(WORDML_NAME)
        payload = "".join((bin_data.text or "").split())
        if not name or not payload:
            continue
        try:
            data = base64.b64decode(payload)
        except binascii.Error:
            continue
        extension = _image_extension(data)
        if extension is None:
            labels[name] = "[IMAGE]"
            continue
        assets_dir.mkdir(parents=True, exist_ok=True)
        image_path = assets_dir / f"wordml_image_{index}{extension}"
        image_path.write_bytes(data)
        labels[name] = classify_icon(str(image_path))
    return labels


def _wordml_text(element: ET.Element, image_labels: dict[str, str]) -> str:
    parts: list[str] = []
    for child in element.iter():
        name = _local_name(child.tag)
        if name == "t" and child.text:
            parts.append(child.text)
        elif name == "tab":
            parts.append(" ")
        elif name == "br":
            parts.append("\n")
        elif name == "imagedata":
            label = image_labels.get(child.attrib.get("src", ""))
            if label:
                parts.append(label)
    return " ".join(" ".join(parts).split())


def _wordml_paragraph_style(paragraph: ET.Element) -> str:
    style = paragraph.find(f"./{WORDML}pPr/{WORDML}pStyle")
    return style.attrib.get(WORDML_VAL, "") if style is not None else ""


def _wordml_heading_tag(style: str) -> str | None:
    normalized = style.lower().replace("_", " ")
    if "heading" not in normalized:
        return None
    for level in range(1, 7):
        if str(level) in normalized:
            return f"h{level}"
    return None


def _wordml_paragraph_html(paragraph: ET.Element, image_labels: dict[str, str]) -> str:
    text = _wordml_text(paragraph, image_labels)
    if not text:
        return ""
    tag = _wordml_heading_tag(_wordml_paragraph_style(paragraph)) or "p"
    return f"<{tag}>{html.escape(text)}</{tag}>"


def _wordml_table_html(table: ET.Element, image_labels: dict[str, str]) -> str:
    rows: list[str] = []
    for row_index, row in enumerate(table.findall(f"./{WORDML}tr")):
        cells: list[str] = []
        cell_tag = "th" if row_index == 0 else "td"
        for cell in row.findall(f"./{WORDML}tc"):
            text = _wordml_text(cell, image_labels)
            grid_span = cell.find(f"./{WORDML}tcPr/{WORDML}gridSpan")
            colspan = ""
            if grid_span is not None:
                value = grid_span.attrib.get(WORDML_VAL)
                if value and value.isdigit() and int(value) > 1:
                    colspan = f' colspan="{value}"'
            cells.append(f"<{cell_tag}{colspan}>{html.escape(text)}</{cell_tag}>")
        if cells:
            rows.append("<tr>" + "".join(cells) + "</tr>")
    return "<table>" + "".join(rows) + "</table>" if rows else ""


def _wordml_blocks(element: ET.Element, image_labels: dict[str, str]) -> list[str]:
    blocks: list[str] = []
    for child in element:
        name = _local_name(child.tag)
        if name == "p":
            block = _wordml_paragraph_html(child, image_labels)
            if block:
                blocks.append(block)
        elif name == "tbl":
            block = _wordml_table_html(child, image_labels)
            if block:
                blocks.append(block)
        else:
            blocks.extend(_wordml_blocks(child, image_labels))
    return blocks


def _convert_word2003_xml_to_html(doc_path: Path, output_dir: Path) -> Path:
    tree = ET.parse(doc_path)
    root = tree.getroot()
    image_labels = _wordml_image_labels(root, output_dir, doc_path.stem)
    body = root.find(f".//{WORDML}body")
    if body is None:
        raise DocConversionError(f"Word 2003 XML body was not found in {doc_path.name}.")

    blocks = _wordml_blocks(body, image_labels)

    if not blocks:
        raise DocConversionError(f"Word 2003 XML conversion produced no text for {doc_path.name}.")

    output_dir.mkdir(parents=True, exist_ok=True)
    html_path = output_dir / f"{doc_path.stem}.html"
    html_path.write_text("<article>\n" + "\n".join(blocks) + "\n</article>\n", encoding="utf-8")
    logger.info("Word 2003 XML HTML output: %s", html_path)
    return html_path


def find_soffice() -> str:
    """Return the first available LibreOffice binary path."""
    for candidate in DEFAULT_SOFFICE_PATHS:
        if not candidate:
            continue
        path = shutil.which(candidate) if os.path.basename(candidate) == candidate else candidate
        if path and os.path.isfile(path):
            return path
    raise LibreOfficeNotFoundError(
        "LibreOffice (soffice) was not found. Install LibreOffice and ensure soffice is on PATH, "
        "or set LIBREOFFICE_PATH to the soffice executable."
    )


def _soffice_program_dir(soffice: str) -> Path:
    return Path(soffice).resolve().parent


def _libreoffice_user_installation_uri(work_dir: Path) -> str:
    profile_dir = work_dir / "lo_profile"
    profile_dir.mkdir(parents=True, exist_ok=True)
    return "file:///" + profile_dir.as_posix()


def _discover_html_output(output_dir: Path, source_stem: str) -> Path:
    """Find the HTML file produced for a given source document."""
    html_candidates = sorted(
        list(output_dir.glob("*.htm")) + list(output_dir.glob("*.html")),
        key=lambda p: (p.name.lower() != f"{source_stem.lower()}.html", p.name),
    )
    if not html_candidates:
        raise DocConversionError(
            f"No .htm/.html output found in {output_dir} after conversion."
        )
    return html_candidates[0]


def _is_non_fatal_libreoffice_warning(detail: str) -> bool:
    normalized = detail.strip().lower()
    return any(warning in normalized for warning in _NON_FATAL_LIBREOFFICE_WARNINGS)


def discover_companion_dirs(html_path: Path) -> list[Path]:
    """Return likely image/asset directories next to an HTML export."""
    parent = html_path.parent
    stem = html_path.stem
    patterns = (
        f"{stem}_files",
        f"{stem}.files",
        f"{stem}_html_files",
    )
    found: list[Path] = []
    for name in patterns:
        candidate = parent / name
        if candidate.is_dir():
            found.append(candidate)

    for child in parent.iterdir():
        if child.is_dir() and child not in found and stem in child.name:
            found.append(child)

    return found


def _convert_with_libreoffice(
    doc_path: Path,
    output_dir: Path,
    *,
    soffice_path: str | None = None,
    timeout_seconds: int = 180,
    infilter: str | None = None,
) -> Path:
    soffice = soffice_path or find_soffice()
    program_dir = _soffice_program_dir(soffice)
    user_installation = _libreoffice_user_installation_uri(output_dir)

    cmd = [
        soffice,
        "--headless",
        "--nologo",
        "--nofirststartwizard",
        f"-env:UserInstallation={user_installation}",
    ]
    if infilter:
        cmd.append(f"--infilter={infilter}")
    cmd.extend(
        [
            "--convert-to",
            "html",
            "--outdir",
            str(output_dir),
            str(doc_path),
        ]
    )

    logger.info("Converting %s with LibreOffice (%s)", doc_path.name, soffice)
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
            cwd=str(program_dir),
        )
    except subprocess.TimeoutExpired as exc:
        raise DocConversionError(
            f"LibreOffice timed out after {timeout_seconds}s while converting {doc_path.name}"
        ) from exc

    stderr = (result.stderr or "").strip()
    stdout = (result.stdout or "").strip()
    detail = stderr or stdout or f"exit code {result.returncode}"
    html_path: Path | None = None
    try:
        html_path = _discover_html_output(output_dir, doc_path.stem)
    except DocConversionError:
        html_path = None

    if result.returncode != 0:
        if html_path is not None and _is_non_fatal_libreoffice_warning(detail):
            logger.warning(
                "LibreOffice returned %s for %s but produced HTML output anyway: %s",
                result.returncode,
                doc_path.name,
                detail,
            )
            logger.info("LibreOffice HTML output: %s", html_path)
            return html_path
        raise DocConversionError(f"LibreOffice conversion failed: {detail}")

    if html_path is None:
        raise DocConversionError(
            f"LibreOffice conversion completed but no .htm/.html output was found for {doc_path.name}."
        )
    logger.info("LibreOffice HTML output: %s", html_path)
    return html_path


def convert_doc_to_html(
    doc_path: str | Path,
    output_dir: str | Path | None = None,
    *,
    soffice_path: str | None = None,
    timeout_seconds: int = 180,
    prefer_word_com: bool = True,
) -> Path:
    """
    Convert a Word document to HTML.

    Routing:
      - Word 2003 XML (.doc/.xml extension): Microsoft Word COM on Windows (best fidelity),
        then LibreOffice with MS Word 2003 XML filter as fallback.
      - OLE .doc / .docx: LibreOffice headless.
    """
    doc_path = Path(doc_path).resolve()
    if not doc_path.is_file():
        raise FileNotFoundError(f"Document not found: {doc_path}")

    suffix = doc_path.suffix.lower()
    if suffix not in {".doc", ".docx", ".xml"}:
        raise ValueError(f"Expected .doc, .docx, or .xml, got: {suffix}")

    if output_dir is None:
        output_dir = Path(tempfile.mkdtemp(prefix="ewa-doc-html-"))
    else:
        output_dir = Path(output_dir).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)

    kind = detect_word_document_kind(doc_path)
    logger.info("Detected Word document kind: %s (%s)", kind, doc_path.name)

    if kind == "word2003_xml" and prefer_word_com and is_windows():
        try:
            return convert_doc_to_html_word_com(doc_path, output_dir)
        except WordComNotAvailableError as exc:
            logger.warning("Word COM failed, falling back to LibreOffice: %s", exc)

    if kind == "word2003_xml":
        try:
            return _convert_word2003_xml_to_html(doc_path, output_dir)
        except (ET.ParseError, DocConversionError) as exc:
            logger.warning("Word 2003 XML direct conversion failed, falling back to LibreOffice: %s", exc)
            staged = output_dir / doc_path.name
            shutil.copy2(doc_path, staged)
            return _convert_with_libreoffice(
                staged,
                output_dir,
                soffice_path=soffice_path,
                timeout_seconds=timeout_seconds,
                infilter="MS Word 2003 XML",
            )

    return _convert_with_libreoffice(
        doc_path,
        output_dir,
        soffice_path=soffice_path,
        timeout_seconds=timeout_seconds,
    )
