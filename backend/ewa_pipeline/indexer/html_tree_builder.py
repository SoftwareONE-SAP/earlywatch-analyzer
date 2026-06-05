"""Build a lightweight analysis tree from compact semantic HTML."""

from __future__ import annotations

import json
import re
from pathlib import Path

from bs4 import BeautifulSoup, Tag


def _text_snippet(html_text: str, limit: int = 180) -> str:
    text = BeautifulSoup(html_text, "html.parser").get_text(" ", strip=True)
    return re.sub(r"\s+", " ", text)[:limit]


def _node_id(index: int) -> str:
    return f"{index:04d}"


def build_document_tree_from_html(html_path: Path, output_dir: Path) -> dict:
    """
    Build a PageIndex-shaped tree from compact HTML headings.

    Node text is compact HTML, so downstream agents receive tables as HTML
    instead of lossy Markdown tables.
    """
    html_path = Path(html_path)
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
    root = soup.find("article") or soup

    nodes: list[dict] = []
    stack: list[tuple[int, dict, list[str]]] = []
    counter = 0

    def current_parts() -> list[str] | None:
        return stack[-1][2] if stack else None

    def finish_node(level: int) -> None:
        while stack and stack[-1][0] >= level:
            _, node, parts = stack.pop()
            node["text"] = "\n".join(parts).strip()
            node["summary"] = _text_snippet(node["text"])

    for child in root.children:
        if not isinstance(child, Tag):
            continue
        name = child.name.lower()
        if name in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            level = int(name[1])
            finish_node(level)
            counter += 1
            node = {
                "node_id": _node_id(counter),
                "title": child.get_text(" ", strip=True) or f"Section {_node_id(counter)}",
                "summary": "",
                "start_index": 0,
                "end_index": 0,
                "nodes": [],
                "text": "",
            }
            if stack:
                stack[-1][1]["nodes"].append(node)
            else:
                nodes.append(node)
            stack.append((level, node, [str(child)]))
            continue

        rendered = str(child).strip()
        if not rendered:
            continue
        parts = current_parts()
        if parts is None:
            counter += 1
            node = {
                "node_id": _node_id(counter),
                "title": "Overview",
                "summary": "",
                "start_index": 0,
                "end_index": 0,
                "nodes": [],
                "text": "",
            }
            nodes.append(node)
            stack.append((1, node, []))
            parts = stack[-1][2]
        parts.append(rendered)

    finish_node(0)

    result = {
        "doc_name": html_path.name,
        "structure": nodes,
        "doc_description": _text_snippet(root.get_text(" ", strip=True), 220),
    }
    tree_path = output_dir / f"{html_path.stem}_tree.json"
    tree_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    return result
