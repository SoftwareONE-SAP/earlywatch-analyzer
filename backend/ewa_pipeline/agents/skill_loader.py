from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


# The largest focused pair (core + security threshold + security remediation)
# is just over 12K characters. Keep enough headroom to avoid cutting off safety
# guidance while remaining far below GPT-5.6 Luna's context capacity.
DEFAULT_SKILL_CONTEXT_CHARS = 16000

# Compatibility index files. They only point at other references, so they are
# never offered to the planner and never loaded as analysis content.
COMPAT_REFERENCE_IDS = frozenset({"thresholds", "remediation-patterns"})

CORE_REFERENCE_ID = "core-analysis"
CORRELATIONS_REFERENCE_ID = "correlations"
MAX_DOMAIN_PAIRS = 2

# One keyword map for every domain. Each domain yields both
# `thresholds-<domain>` and `remediation-<domain>`. Keywords are matched as
# whole words or phrases (a trailing plural "s"/"es" is allowed), so "roll"
# does not match "payroll" and "lock" does not match "blocked".
DOMAIN_KEYWORDS: dict[str, tuple[str, ...]] = {
    "performance": (
        "dialog",
        "workload",
        "response",
        "cpu",
        "swap",
        "hardware",
        "performance",
        "transaction profile",
        "performance evaluation",
    ),
    "memory": (
        "memory",
        "buffer",
        "heap",
        "roll",
        "extended memory",
        "em utilization",
        "em/",
    ),
    "database": (
        "database",
        "db",
        "oracle",
        "sql server",
        "mssql",
        "db2",
        "maxdb",
        "sybase",
        "ase",
        "tablespace",
    ),
    "sql": (
        "sql statement",
        "statement hash",
        "top statement",
        "expensive statement",
        "expensive sql",
        "plan cache",
        "sql cache",
        "thread distribution",
        "known issue",
        "origin of sql",
        "internal sql",
        "missing index",
        "statement history",
        "correlation with index server",
        "index server resource consumption",
        "index server rescource consumption",  # typo as it appears in the report
    ),
    "hana": (
        "hana",
        "indexserver",
        "nameserver",
        "column store",
        "row store",
        "delta merge",
        "savepoint",
        "disk usage",
        "disk configuration",
        "diagnosis file",
        "statisticsserver",
        "statistics server",
        "tables and indexes",
        "parameter recommendation",
    ),
    "batch": ("batch", "background", "job", "sm37"),
    "security": (
        "security",
        "sap_all",
        "sap_new",
        "password",
        "rfc security",
        "open rfc",
        "unauthenticated rfc",
        "authorization",
        "audit trail",
        "audit policy",
        "audit",
        "auditing",
        "user system",
        "automatic login",
        "super user",
        "login/no_automatic_user_sapstar",
        "data admin",
        "system user",
        "listeninterface",
        "sql trace",
    ),
    "operations": (
        "spool",
        "temse",
        "transport",
        "stms",
        "dump",
        "st22",
        "system log",
        "sm21",
        "icm",
        "enqueue",
        "lock",
        "number of changes",
    ),
    "continuity": (
        "availability",
        "outage",
        "restart",
        "update error",
        "number range",
        "backup",
        "recovery",
        "recoverability",
    ),
    "integration": (
        "rfc",
        "rfc load",
        "rfc workload",
        "workload of rfc",
        "rfc gateway",
        "message server",
        "netweaver gateway",
        "gateway",
        "odata",
        "/iwfnd/",
        "/iwbep/",
        "interface",
    ),
    "lifecycle": (
        "maintenance phase",
        "support package",
        "kernel release",
        "database version",
        "operating system",
        "sqldbc",
        "important sap note",
        "kernel",
        "current landscape",
        "software configuration",
        "license information",
    ),
    "data-management": (
        "data volume",
        "dvm",
        "growth",
        "largest table",
        "archiving",
        "archive",
        "archived",
        "reorganization",
        "compression",
    ),
    "data-quality": (
        "service data quality",
        "service readiness",
        "missing data",
        "grey rating",
        "not rated",
        "rtcctool",
        "sdccn",
        "st-pi",
        "ccdb",
        "sdcc",
        "service data",
        "solution manager",
        "backbone",
        "service preparation",
        "managed system setup",
    ),
}

# Extra regex patterns that count as one hit for a domain.
DOMAIN_REGEXES: dict[str, tuple[str, ...]] = {
    # Section titles such as "15.1.1 Statement b61a3f9c2d7e" (hash has a digit).
    "sql": (r"\bstatement\s+(?=[0-9a-f]*\d)[0-9a-f]{6,}\b",),
    # "SAP*" ends in a non-word character, so the whole-word keyword pattern
    # cannot match it.
    "security": (r"(?<!\w)sap\*(?!\w)",),
}

# Keywords that only count when the text does NOT mention HANA.
GENERIC_DATABASE_KEYWORDS = frozenset({"database", "db"})

# Phrases blanked out of the text before one domain is matched, so they do not
# give that domain a false hit.
DOMAIN_EXCLUDED_PHRASES: dict[str, tuple[str, ...]] = {
    "integration": (
        "user interface",
        "rfc security",
        "open rfc",
        "unauthenticated rfc",
    ),
}

CORRELATION_KEYWORDS = ("correlation", "compound", "cascade")

_HANA_SECURITY_MARKERS = (
    "audit trail",
    "audit policy",
    "data admin",
    "system user",
    "listeninterface",
    "sql trace",
)


def _keyword_pattern(keyword: str) -> re.Pattern[str]:
    body = re.escape(keyword)
    # Allow a simple plural ("job" -> "jobs", "index" -> "indexes") for words.
    suffix = r"(?:e?s)?" if keyword[-1].isalnum() else ""
    return re.compile(rf"(?<!\w){body}{suffix}(?!\w)", re.IGNORECASE)


_DOMAIN_PATTERNS: dict[str, tuple[tuple[str, re.Pattern[str]], ...]] = {
    domain: tuple(
        [(keyword, _keyword_pattern(keyword)) for keyword in keywords]
        + [(rx, re.compile(rx, re.IGNORECASE)) for rx in DOMAIN_REGEXES.get(domain, ())]
    )
    for domain, keywords in DOMAIN_KEYWORDS.items()
}
_CORRELATION_PATTERNS = tuple(_keyword_pattern(keyword) for keyword in CORRELATION_KEYWORDS)
_EXCLUDED_PHRASE_PATTERNS = {
    domain: tuple(_keyword_pattern(phrase) for phrase in phrases)
    for domain, phrases in DOMAIN_EXCLUDED_PHRASES.items()
}
_HANA_PATTERN = _keyword_pattern("hana")
_HANA_SECURITY_PATTERNS = tuple(_keyword_pattern(m) for m in _HANA_SECURITY_MARKERS)

_BLOCK_RE = {
    name: re.compile(rf"<{name}>(.*?)</{name}>", re.DOTALL)
    for name in ("routing", "quick_start")
}


@dataclass(frozen=True)
class SkillReference:
    id: str
    title: str
    path: Path


@dataclass(frozen=True)
class SkillCard:
    name: str
    description: str
    path: Path
    references: tuple[SkillReference, ...]
    routing: str = ""


def _parse_frontmatter(raw_frontmatter: str) -> dict[str, Any]:
    metadata: dict[str, Any] = {}
    lines = raw_frontmatter.splitlines()
    index = 0
    last_plain_key: str | None = None

    while index < len(lines):
        line = lines[index]
        if not line.strip() or line.lstrip().startswith("#"):
            index += 1
            continue

        if line.startswith((" ", "\t")):
            # Wrapped plain value: continue the previous key.
            if last_plain_key is not None:
                metadata[last_plain_key] = f"{metadata[last_plain_key]} {line.strip()}".strip()
            index += 1
            continue

        if ":" not in line:
            index += 1
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value in {">", "|", ">-", "|-"}:
            collected: list[str] = []
            index += 1
            while index < len(lines):
                continuation = lines[index]
                if continuation and not continuation.startswith((" ", "\t")):
                    break
                collected.append(continuation.strip())
                index += 1
            metadata[key] = " ".join(part for part in collected if part).strip()
            last_plain_key = None
            continue

        metadata[key] = value.strip("'\"")
        last_plain_key = key
        index += 1

    return metadata


def _split_frontmatter(raw: str) -> tuple[dict[str, Any], str]:
    raw = raw.lstrip("﻿")
    lines = raw.splitlines()
    if not lines or lines[0].rstrip() != "---":
        return {}, raw.strip()

    for end in range(1, len(lines)):
        if lines[end].rstrip() == "---":
            metadata = _parse_frontmatter("\n".join(lines[1:end]))
            return metadata, "\n".join(lines[end + 1 :]).strip()
    return {}, raw.strip()


def _extract_block(body: str, name: str) -> str:
    match = _BLOCK_RE[name].search(body)
    return match.group(1).strip() if match else ""


def _strip_blocks(body: str, names: tuple[str, ...]) -> str:
    for name in names:
        body = _BLOCK_RE[name].sub("", body)
    return re.sub(r"\n{3,}", "\n\n", body).strip()


def _reference_title(path: Path) -> str:
    return path.stem.replace("-", " ").replace("_", " ").title()


def _domain_hits(domain: str, text: str, *, has_hana: bool) -> tuple[int, int]:
    """Return (distinct keyword hits, position of first hit) for one domain."""
    for pattern in _EXCLUDED_PHRASE_PATTERNS.get(domain, ()):
        text = pattern.sub(lambda m: " " * len(m.group(0)), text)

    hits = 0
    first = len(text) + 1
    for keyword, pattern in _DOMAIN_PATTERNS[domain]:
        if domain == "database" and has_hana and keyword in GENERIC_DATABASE_KEYWORDS:
            continue
        match = pattern.search(text)
        if match:
            hits += 1
            first = min(first, match.start())
    return hits, first


class SkillRegistry:
    def __init__(self, root_dir: Path, skills: dict[str, SkillCard]):
        self.root_dir = root_dir
        self._skills = skills

    @classmethod
    def from_dir(cls, root_dir: Path) -> "SkillRegistry":
        root_dir = Path(root_dir)
        skills: dict[str, SkillCard] = {}
        if not root_dir.exists():
            return cls(root_dir=root_dir, skills=skills)

        for skill_md in sorted(root_dir.glob("*/SKILL.md")):
            metadata, body = _split_frontmatter(skill_md.read_text(encoding="utf-8"))
            name = str(metadata.get("name") or skill_md.parent.name).strip()
            if not name:
                continue

            refs_dir = skill_md.parent / "references"
            references: list[SkillReference] = []
            if refs_dir.exists():
                for ref_path in sorted(refs_dir.glob("*.md")):
                    references.append(
                        SkillReference(
                            id=ref_path.stem,
                            title=_reference_title(ref_path),
                            path=ref_path,
                        )
                    )

            skills[name] = SkillCard(
                name=name,
                description=str(metadata.get("description") or "").strip(),
                path=skill_md,
                references=tuple(references),
                routing=_extract_block(body, "routing"),
            )

        return cls(root_dir=root_dir, skills=skills)

    def reference_ids(self, skill_name: str) -> list[str]:
        """Ids of the skill's references in file order ([] for unknown skill)."""
        skill = self._skills.get((skill_name or "").strip())
        if skill is None:
            return []
        return [ref.id for ref in skill.references]

    def catalog_text(self) -> str:
        if not self._skills:
            return "No backend skills are available."

        parts: list[str] = []
        for skill in self._skills.values():
            refs = (
                ", ".join(
                    ref.id for ref in skill.references if ref.id not in COMPAT_REFERENCE_IDS
                )
                or "none"
            )
            lines = [
                f"- skill_name: {skill.name}",
                f"  description: {skill.description}",
                f"  reference_ids: {refs}",
            ]
            if skill.routing:
                lines.append("  routing:")
                lines.extend(
                    f"    {line}" if line.strip() else ""
                    for line in skill.routing.splitlines()
                )
            parts.append("\n".join(lines))
        return "\n".join(parts)

    def resolve_context(
        self,
        skill_name: str | None,
        reference_ids: list[str] | tuple[str, ...] | None,
        *,
        fallback_text: str = "",
        max_chars: int = DEFAULT_SKILL_CONTEXT_CHARS,
    ) -> str:
        skill = self._skills.get((skill_name or "").strip())
        if skill is None:
            return fallback_text

        reference_lookup = {ref.id: ref for ref in skill.references}
        ordered_ids = self._order_reference_ids(reference_ids, reference_lookup)

        _, skill_body = _split_frontmatter(skill.path.read_text(encoding="utf-8"))
        skill_body = _strip_blocks(skill_body, ("routing", "quick_start"))
        base = f"# Skill: {skill.name}\n\n{skill_body}" if skill_body else ""

        blocks: list[tuple[str, str]] = []
        for ref_id in ordered_ids:
            body = reference_lookup[ref_id].path.read_text(encoding="utf-8").strip()
            if body:
                blocks.append((ref_id, f"# Reference: {ref_id}\n\n{body}"))

        if not base and not blocks:
            return fallback_text

        separator = "\n\n---\n\n"

        def render(kept: list[tuple[str, str]], omitted: list[str]) -> str:
            sections = ([base] if base else []) + [text for _, text in kept]
            context = separator.join(sections).strip()
            if omitted:
                note = f"[Skill context: omitted references due to size: {', '.join(omitted)}]"
                context = f"{context}\n\n{note}" if context else note
            return context

        kept = list(blocks)
        omitted: list[str] = []
        context = render(kept, omitted)
        # Drop whole references from the end; never core-analysis, never mid-text.
        while len(context) > max_chars:
            index = next(
                (i for i in range(len(kept) - 1, -1, -1) if kept[i][0] != CORE_REFERENCE_ID),
                None,
            )
            if index is None:
                break
            omitted.insert(0, kept.pop(index)[0])
            context = render(kept, omitted)
        return context

    @staticmethod
    def _order_reference_ids(
        reference_ids: list[str] | tuple[str, ...] | None,
        reference_lookup: dict[str, SkillReference],
    ) -> list[str]:
        """core-analysis, then thresholds-X/remediation-X per domain, correlations last."""
        requested: list[str] = []
        for ref_id in reference_ids or []:
            ref_id = str(ref_id).strip()
            if (
                ref_id
                and ref_id in reference_lookup
                and ref_id not in COMPAT_REFERENCE_IDS
                and ref_id not in requested
            ):
                requested.append(ref_id)

        groups: dict[str, dict[str, str]] = {}
        for ref_id in requested:
            if ref_id in {CORE_REFERENCE_ID, CORRELATIONS_REFERENCE_ID}:
                continue
            kind, _, domain = ref_id.partition("-")
            if kind in {"thresholds", "remediation"} and domain:
                groups.setdefault(domain, {})[kind] = ref_id
            else:
                groups.setdefault(ref_id, {})["other"] = ref_id

        ordered: list[str] = []
        if CORE_REFERENCE_ID in requested:
            ordered.append(CORE_REFERENCE_ID)
        for group in groups.values():
            for kind in ("thresholds", "remediation", "other"):
                if kind in group:
                    ordered.append(group[kind])
        if CORRELATIONS_REFERENCE_ID in requested:
            ordered.append(CORRELATIONS_REFERENCE_ID)
        return ordered

    def suggest_references(self, skill_name: str | None, text: str) -> list[str]:
        skill = self._skills.get((skill_name or "").strip())
        if skill is None:
            return []

        available = {ref.id for ref in skill.references} - COMPAT_REFERENCE_IDS
        has_hana = bool(_HANA_PATTERN.search(text))

        scores: dict[str, tuple[int, int]] = {}
        for domain in DOMAIN_KEYWORDS:
            if not ({f"thresholds-{domain}", f"remediation-{domain}"} & available):
                continue
            hits, first = _domain_hits(domain, text, has_hana=has_hana)
            if hits:
                scores[domain] = (hits, first)

        # Statement-level SQL sections use the SQL guides, not the generic
        # database or HANA service guides.
        if "sql" in scores:
            scores.pop("database", None)
            scores.pop("hana", None)

        # HANA-specific guidance already covers HANA availability, restart,
        # backup, and recovery sections.
        if "hana" in scores:
            scores.pop("continuity", None)

        # A HANA security subsection should use the focused security pair
        # rather than also loading the broad HANA service pair.
        if "security" in scores and any(p.search(text) for p in _HANA_SECURITY_PATTERNS):
            scores.pop("hana", None)

        ranked = sorted(scores, key=lambda d: (-scores[d][0], scores[d][1]))[:MAX_DOMAIN_PAIRS]

        suggestions: list[str] = []
        if CORE_REFERENCE_ID in available:
            suggestions.append(CORE_REFERENCE_ID)
        for domain in ranked:
            for kind in ("thresholds", "remediation"):
                ref_id = f"{kind}-{domain}"
                if ref_id in available:
                    suggestions.append(ref_id)
        if CORRELATIONS_REFERENCE_ID in available and any(
            p.search(text) for p in _CORRELATION_PATTERNS
        ):
            suggestions.append(CORRELATIONS_REFERENCE_ID)

        return suggestions
