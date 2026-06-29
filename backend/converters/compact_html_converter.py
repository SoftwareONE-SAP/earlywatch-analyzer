"""Convert EWA HTML exports into compact semantic HTML for LLM input."""

from __future__ import annotations

import html
import logging
import os
import re
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup, NavigableString, Tag

from converters.icon_classifier import (
    build_icon_map,
    classify_icon,
    detect_encoding,
)

logger = logging.getLogger(__name__)

_INLINE_TAGS = {"b", "strong", "i", "em", "a", "span", "sub", "sup", "br", "img"}
_BLOCK_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6", "p", "table", "ul", "ol", "div"}
_RATING_RE = re.compile(r"^\[(GREEN|YELLOW|RED|BLUE|GRAY|NOT_RATED|GREEN_BAR|RED_BAR|YELLOW_BAR|GRAY_BAR|CHECK)\]$")


def _resolve_image_src(src: str, html_dir: str) -> Optional[str]:
    if not src:
        return None
    resolved = os.path.normpath(os.path.join(html_dir, src))
    return resolved if os.path.isfile(resolved) else None


def _image_label(img: Tag, icon_map: dict[str, str], html_dir: str) -> str:
    src = img.get("src", "")
    fname = os.path.basename(src)
    label = icon_map.get(fname)
    if label is not None:
        return label
    resolved = _resolve_image_src(src, html_dir)
    return classify_icon(resolved) if resolved else "[IMAGE]"


def _clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _attrs(tag: Tag, names: tuple[str, ...]) -> str:
    parts = []
    for name in names:
        value = tag.get(name)
        if value:
            parts.append(f' {name}="{html.escape(str(value), quote=True)}"')
    return "".join(parts)


def _inline_html(element: Tag, icon_map: dict[str, str], html_dir: str) -> str:
    parts: list[str] = []
    for child in element.children:
        if isinstance(child, NavigableString):
            text = _clean_text(str(child))
            if text:
                parts.append(html.escape(text))
            continue
        if not isinstance(child, Tag):
            continue

        name = child.name.lower()
        if name == "br":
            parts.append("<br>")
        elif name == "img":
            label = _image_label(child, icon_map, html_dir)
            match = _RATING_RE.match(label)
            if match:
                parts.append(f'<span data-rating="{match.group(1).lower()}">{html.escape(label)}</span>')
            else:
                parts.append(html.escape(label))
        elif name in {"b", "strong"}:
            inner = _inline_html(child, icon_map, html_dir)
            if inner:
                parts.append(f"<strong>{inner}</strong>")
        elif name in {"i", "em"}:
            inner = _inline_html(child, icon_map, html_dir)
            if inner:
                parts.append(f"<em>{inner}</em>")
        elif name == "a":
            inner = _inline_html(child, icon_map, html_dir)
            href = child.get("href", "")
            if inner and href and not href.startswith("#"):
                parts.append(f'<a href="{html.escape(href, quote=True)}">{inner}</a>')
            elif inner:
                parts.append(inner)
        elif name in {"sub", "sup"}:
            inner = _inline_html(child, icon_map, html_dir)
            if inner:
                parts.append(f"<{name}>{inner}</{name}>")
        elif name == "table":
            parts.append(_table_html(child, icon_map, html_dir))
        else:
            inner = _inline_html(child, icon_map, html_dir)
            if inner:
                parts.append(inner)
    return " ".join(part for part in parts if part).strip()


def _table_html(table: Tag, icon_map: dict[str, str], html_dir: str) -> str:
    rows = []
    for tr in table.find_all("tr"):
        cells = []
        for cell in tr.find_all(["td", "th"], recursive=False):
            name = cell.name.lower()
            inner = _inline_html(cell, icon_map, html_dir)
            attrs = _attrs(cell, ("colspan", "rowspan"))
            cells.append(f"<{name}{attrs}>{inner}</{name}>")
        if cells:
            rows.append("<tr>" + "".join(cells) + "</tr>")
    return "<table>" + "".join(rows) + "</table>" if rows else ""


def _list_html(list_tag: Tag, icon_map: dict[str, str], html_dir: str) -> str:
    name = list_tag.name.lower()
    items = []
    for li in list_tag.find_all("li", recursive=False):
        inner = _inline_html(li, icon_map, html_dir)
        if inner:
            items.append(f"<li>{inner}</li>")
    return f"<{name}>" + "".join(items) + f"</{name}>" if items else ""


def _block_html(element: Tag, icon_map: dict[str, str], html_dir: str) -> list[str]:
    name = element.name.lower()
    if name in {"h1", "h2", "h3", "h4", "h5", "h6"}:
        inner = _inline_html(element, icon_map, html_dir)
        return [f"<{name}>{inner}</{name}>"] if inner else []
    if name == "table":
        table = _table_html(element, icon_map, html_dir)
        return [table] if table else []
    if name in {"ul", "ol"}:
        list_html = _list_html(element, icon_map, html_dir)
        return [list_html] if list_html else []
    if name == "p":
        inner = _inline_html(element, icon_map, html_dir)
        return [f"<p>{inner}</p>"] if inner else []

    blocks = []
    has_block_child = any(isinstance(child, Tag) and child.name.lower() in _BLOCK_TAGS for child in element.children)
    if has_block_child:
        for child in element.children:
            if isinstance(child, NavigableString):
                text = _clean_text(str(child))
                if text:
                    blocks.append(f"<p>{html.escape(text)}</p>")
            elif isinstance(child, Tag):
                blocks.extend(_block_html(child, icon_map, html_dir))
    else:
        inner = _inline_html(element, icon_map, html_dir)
        if inner:
            blocks.append(f"<p>{inner}</p>")
    return blocks


def convert_html_to_compact_html(html_path: str | Path, output_path: str | Path | None = None) -> str:
    """Return compact, semantic HTML suitable for direct LLM input."""
    html_path = Path(html_path).resolve()
    html_dir = str(html_path.parent)
    if output_path is None:
        output_path = html_path.with_name(f"{html_path.stem}.compact.html")
    else:
        output_path = Path(output_path).resolve()

    base_name = html_path.stem
    images_dir = html_path.parent / f"{base_name}_files"
    if not images_dir.is_dir():
        images_dir = html_path.parent / f"{base_name}.files"
    icon_map = build_icon_map(str(images_dir)) if images_dir.is_dir() else {}

    raw_bytes = html_path.read_bytes()
    source = raw_bytes.decode(detect_encoding(raw_bytes), errors="replace")
    soup = BeautifulSoup(source, "html.parser")
    body = soup.find("body") or soup

    blocks: list[str] = []
    for child in body.children:
        if isinstance(child, NavigableString):
            text = _clean_text(str(child))
            if text:
                blocks.append(f"<p>{html.escape(text)}</p>")
        elif isinstance(child, Tag):
            blocks.extend(_block_html(child, icon_map, html_dir))

    compact = "<article>\n" + "\n".join(blocks) + "\n</article>\n"
    output_path.write_text(compact, encoding="utf-8")
    logger.info("Wrote compact HTML to %s (%d chars)", output_path, len(compact))
    return compact
