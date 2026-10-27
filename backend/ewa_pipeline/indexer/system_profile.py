"""Build a short "ID card" (SystemProfile) of the SAP system from an EWA report.

Plain HTML parsing only, no AI. Works on compact HTML produced by
``convert_html_to_compact_html``. Sources are tried in priority order and an
earlier source wins; later ones only fill blanks:

  1. cover paragraph (only present when the cover text survives as one paragraph)
  2. landscape tables (Product, Databases, Host Overview, Transport Landscape)
  3. Hardware Capacity "Analysis Start" / "Analysis End" (period)
  4. headings such as "Performance Indicators for TP1" (SID)
"""
from __future__ import annotations

import logging
import re
from collections import Counter

from bs4 import BeautifulSoup, Tag

from ewa_pipeline.indexer.sap_summary import _rows, _text
from ewa_pipeline.report.schemas import SystemProfile

logger = logging.getLogger(__name__)

_SID_RE = re.compile(r"Alert Service Report\s+([A-Z][A-Z0-9]{2})\b")
_ROLE_RE = re.compile(r"\b(Productive|Production|Test|Development|Quality)\b")
_INSTALL_RE = re.compile(r"Installation No\.\s+(\d{10,})\s+(\d{10})")
_DATE_RE = re.compile(r"\b(\d{2})\.(\d{2})\.(\d{4})\b")
_HEADING_SID_RE = re.compile(r"\bfor ([A-Z][A-Z0-9]{2})$")
_NOT_A_SID = {"SAP", "ABAP", "JAVA"}
_ROLE_NAMES = {
    "productive": "Production",
    "production": "Production",
    "test": "Test",
    "development": "Development",
    "quality": "Quality",
}
_MAX_PROMPT_CHARS = 600


def _iso(text: str) -> str:
    match = _DATE_RE.fullmatch((text or "").strip())
    return f"{match.group(3)}-{match.group(2)}-{match.group(1)}" if match else ""


def _role(text: str) -> str:
    return _ROLE_NAMES.get((text or "").strip().lower(), "")


def _find_table(soup: BeautifulSoup, *headers: str) -> list[list[str]] | None:
    """Return the rows of the first table whose first row holds all ``headers``."""
    for table in soup.find_all("table"):
        rows = _rows(table)
        if rows and all(h in rows[0] for h in headers):
            return rows
    return None


def _column(rows: list[list[str]], name: str) -> list[str]:
    index = rows[0].index(name)
    return [r[index] if index < len(r) else "" for r in rows[1:]]


class _Builder:
    def __init__(self) -> None:
        self.profile = SystemProfile()

    def set(self, field: str, value: str, source: str) -> None:
        value = (value or "").strip()
        if value and not getattr(self.profile, field):
            setattr(self.profile, field, value)
            self.profile.sources[field] = source


def _from_cover(soup: BeautifulSoup, b: _Builder) -> None:
    for p in soup.find_all("p"):
        text = _text(p)
        sid = _SID_RE.search(text)
        if not sid:
            continue
        b.set("sid", sid.group(1), "cover")
        role = _ROLE_RE.search(text)
        if role:
            b.set("system_role", _role(role.group(1)), "cover")
        install = _INSTALL_RE.search(text)
        if install:
            # Cover order is "Session No." then "Installation No." (13 digits, 10 digits).
            b.set("session_number", install.group(1), "cover")
            b.set("installation_number", install.group(2), "cover")
        head = text.split("EarlyWatch", 1)[0] if "EarlyWatch" in text else text
        dates = _DATE_RE.findall(head)
        if len(dates) >= 2:
            b.set("period_start", _iso(".".join(dates[-2])), "cover")
            b.set("period_end", _iso(".".join(dates[-1])), "cover")
        return


def _heading_sid(soup: BeautifulSoup) -> str:
    counts: Counter[str] = Counter()
    for h in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        match = _HEADING_SID_RE.search(_text(h))
        if match and match.group(1) not in _NOT_A_SID:
            counts[match.group(1)] += 1
    return counts.most_common(1)[0][0] if counts else ""


def _from_landscape(soup: BeautifulSoup, b: _Builder, sid: str) -> None:
    rows = _find_table(soup, "SAP Product", "Product Version")
    if rows and len(rows) > 1:
        row = next((r for r in rows[1:] if sid and r[0].startswith(sid)), rows[1])
        row = (row + ["", "", ""])[:3]
        b.set("product", row[1], "landscape:Product")
        b.set("product_version", row[2], "landscape:Product")

    rows = _find_table(soup, "Database System", "Database Version", "DB ID")
    if rows and len(rows) > 1:
        row = next((r for r in rows[1:] if sid and r[0].startswith(sid)), rows[1])
        row = (row + [""] * 4)[:4]
        b.set("database", row[1], "landscape:Database")
        b.set("database_version", row[2], "landscape:Database")
        b.set("db_id", row[3], "landscape:Database")

    rows = _find_table(soup, "Host", "Operating System")
    if rows:
        systems = Counter(v for v in _column(rows, "Operating System") if v)
        if systems:
            b.set("os", systems.most_common(1)[0][0], "landscape:Host Overview")

    rows = _find_table(soup, "System Role", "System ID", "Installation Number")
    if rows and sid:
        role_i = rows[0].index("System Role")
        sid_i = rows[0].index("System ID")
        inst_i = rows[0].index("Installation Number")
        for r in rows[1:]:
            r = r + [""] * (len(rows[0]) - len(r))
            if r[sid_i] == sid:
                b.set("system_role", _role(r[role_i]), "landscape:Transport Landscape")
                b.set("installation_number", r[inst_i], "landscape:Transport Landscape")
                break


def _from_hardware_capacity(soup: BeautifulSoup, b: _Builder) -> None:
    rows = _find_table(soup, "Analysis Start", "Analysis End")
    if not rows:
        return
    starts = sorted(d for d in map(_iso, _column(rows, "Analysis Start")) if d)
    ends = sorted(d for d in map(_iso, _column(rows, "Analysis End")) if d)
    if starts:
        b.set("period_start", starts[0], "hardware_capacity")
    if ends:
        b.set("period_end", ends[-1], "hardware_capacity")


def extract_system_profile(compact_html: str) -> SystemProfile:
    """Return an "ID card" of the system described by the report.

    Missing values stay "". ``sources`` says where each filled field came from
    ("cover", "landscape:Product", "landscape:Database", "landscape:Host Overview",
    "landscape:Transport Landscape", "hardware_capacity", "headings").
    Dates are YYYY-MM-DD. This function never raises.
    """
    try:
        soup = BeautifulSoup(compact_html or "", "html.parser")
        b = _Builder()
        _from_cover(soup, b)
        # The SID is needed to pick the right landscape row, so look it up
        # from headings if the cover did not give it (recorded as "headings").
        sid = b.profile.sid or _heading_sid(soup)
        _from_landscape(soup, b, sid)
        _from_hardware_capacity(soup, b)
        b.set("sid", sid, "headings")
        return b.profile
    except Exception:  # noqa: BLE001 - must never break the pipeline
        logger.exception("Could not build the system profile")
        return SystemProfile()


def profile_to_prompt_text(profile: SystemProfile) -> str:
    """Short plain-text summary of the profile for the analyst prompts (< 600 chars)."""
    p = profile
    parts = [
        ("System ID", p.sid),
        ("Role", p.system_role),
        ("Installation number", p.installation_number),
        ("Product", " ".join(x for x in (p.product, p.product_version) if x)),
        ("Database", " ".join(x for x in (p.database, p.database_version) if x)),
        ("DB ID", p.db_id),
        ("Operating system", p.os),
        ("Analysis period", f"{p.period_start} to {p.period_end}" if p.period_start and p.period_end
         else p.period_start or p.period_end),
    ]
    text = "\n".join(f"{label}: {value}" for label, value in parts if value)
    return text[:_MAX_PROMPT_CHARS]
