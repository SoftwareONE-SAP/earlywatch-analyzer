"""Read SAP's own ratings from section 1 "Service Summary" of an EWA report.

Plain HTML parsing only, no AI. Works on compact HTML produced by
``convert_html_to_compact_html``.
"""
from __future__ import annotations

import logging
import re

from bs4 import BeautifulSoup, Tag

from ewa_pipeline.report.schemas import SapAlert, SapCheck, SapServiceSummary

logger = logging.getLogger(__name__)

_RATING_RE = re.compile(
    r"\[(RED|YELLOW|GREEN|BLUE|GRAY|NOT_RATED|GREEN_BAR|RED_BAR|YELLOW_BAR|GRAY_BAR|CHECK)\]"
)
_LABEL_TAGS = ["p", "td", "th", "strong"]


def _text(node: Tag) -> str:
    return re.sub(r"\s+", " ", node.get_text(" ", strip=True)).strip()


def _rating(cell_text: str) -> str:
    match = _RATING_RE.search(cell_text)
    return match.group(1) if match else ""


def _strip_marker(title: str) -> str:
    return title[:-2] if title.endswith(" *") else title


def _rows(table: Tag) -> list[list[str]]:
    return [
        [_text(c) for c in tr.find_all(["td", "th"], recursive=False)]
        for tr in table.find_all("tr")
    ]


def _table_after_label(soup: BeautifulSoup, label: str) -> Tag | None:
    for tag in soup.find_all(_LABEL_TAGS):
        if _text(tag) == label:
            return tag.find_next("table")
    return None


def _parse_alerts(table: Tag) -> list[SapAlert]:
    alerts = []
    for cells in _rows(table):
        rating = next((_rating(c) for c in cells if _rating(c)), "")
        if not rating:
            continue
        text = next((c for c in reversed(cells) if c), "")
        alerts.append(SapAlert(rating=rating, text=text))
    return alerts


def _parse_checks(table: Tag) -> list[SapCheck]:
    checks: list[SapCheck] = []
    topic = ""
    for cells in _rows(table):
        cells = (cells + [""] * 4)[:4]
        if "Topic Rating" in " ".join(cells):
            continue
        if cells[1]:
            raw = cells[1]
            topic = _strip_marker(raw)
            checks.append(SapCheck(topic=topic, subtopic="", rating=_rating(cells[0]), raw_title=raw))
        if cells[3]:
            raw = cells[3]
            checks.append(
                SapCheck(topic=topic, subtopic=_strip_marker(raw), rating=_rating(cells[2]), raw_title=raw)
            )
    return checks


def extract_service_summary(compact_html: str) -> SapServiceSummary:
    """Return SAP's Alert Overview and Check Overview as structured data.

    Alerts: one SapAlert per row that has a rating token; ``text`` is the last
    non-empty cell. Ratings are plain uppercase words ("RED"), no brackets.

    Checks: one SapCheck per topic row and one per subtopic row.
      - Topic row (cell 1 non-empty): ``subtopic=""``, ``topic`` is the topic
        title, ``rating`` comes from cell 0. It becomes the current topic.
      - Subtopic row (cell 3 non-empty): ``topic`` is the current topic,
        ``subtopic`` is the subtopic title, ``rating`` comes from cell 2.
      - A row can be both; it then yields a topic check followed by a subtopic check.
    Only one trailing " *" is stripped from ``topic``/``subtopic``;
    ``raw_title`` keeps the original text.

    Missing labels or tables give empty lists. This function never raises.
    """
    try:
        soup = BeautifulSoup(compact_html or "", "html.parser")
        alert_table = _table_after_label(soup, "Alert Overview")
        check_table = _table_after_label(soup, "Check Overview")
        return SapServiceSummary(
            alerts=_parse_alerts(alert_table) if alert_table is not None else [],
            checks=_parse_checks(check_table) if check_table is not None else [],
        )
    except Exception:  # noqa: BLE001 - must never break the pipeline
        logger.exception("Could not read the SAP Service Summary")
        return SapServiceSummary()
