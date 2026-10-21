"""Convert Word 2003 XML .doc files to HTML."""

from __future__ import annotations

import base64
import binascii
import html
import logging
import tempfile
from pathlib import Path
from xml.etree import ElementTree as ET

from converters.icon_classifier import classify_icon

logger = logging.getLogger(__name__)


class DocConversionError(RuntimeError):
    """Raised when document conversion to HTML fails."""


WORDML_NS = "http://schemas.microsoft.com/office/word/2003/wordml"
WORDML = f"{{{WORDML_NS}}}"
WORDML_NAME = f"{WORDML}name"
WORDML_VAL = f"{WORDML}val"


def detect_word_document_kind(path: Path) -> str:
    with path.open("rb") as file:
        head = file.read(512)
    if head.startswith(b"<?xml") or b"wordDocument" in head:
        return "word2003_xml"
    return "unsupported"


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


def convert_doc_to_html(
    doc_path: str | Path,
    output_dir: str | Path | None = None,
) -> Path:
    """
    Convert a Word document to HTML.

    Routing:
      - Word 2003 XML (.doc extension): direct XML-to-HTML conversion.
      - Other .doc encodings fail without fallback conversion.
    """
    doc_path = Path(doc_path).resolve()
    if not doc_path.is_file():
        raise FileNotFoundError(f"Document not found: {doc_path}")

    suffix = doc_path.suffix.lower()
    if suffix != ".doc":
        raise ValueError(f"Expected .doc, got: {suffix}")

    if output_dir is None:
        output_dir = Path(tempfile.mkdtemp(prefix="ewa-doc-html-"))
    else:
        output_dir = Path(output_dir).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)

    kind = detect_word_document_kind(doc_path)
    logger.info("Detected Word document kind: %s (%s)", kind, doc_path.name)

    if kind != "word2003_xml":
        raise DocConversionError(
            f"Unsupported .doc format for {doc_path.name}. Only Word 2003 XML .doc files are supported."
        )

    try:
        return _convert_word2003_xml_to_html(doc_path, output_dir)
    except ET.ParseError as exc:
        raise DocConversionError(f"Word 2003 XML parsing failed for {doc_path.name}.") from exc
