from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


# The largest focused pair (core + security threshold + security remediation)
# is just over 12K characters. Keep enough headroom to avoid cutting off safety
# guidance while remaining far below GPT-5.6 Luna's context capacity.
DEFAULT_SKILL_CONTEXT_CHARS = 16000


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


def _parse_frontmatter(raw_frontmatter: str) -> dict[str, Any]:
    metadata: dict[str, Any] = {}
    lines = raw_frontmatter.splitlines()
    index = 0

    while index < len(lines):
        line = lines[index]
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
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
            continue

        metadata[key] = value.strip("'\"")
        index += 1

    return metadata


def _split_frontmatter(raw: str) -> tuple[dict[str, Any], str]:
    if not raw.startswith("---"):
        return {}, raw.strip()

    parts = raw.split("---", 2)
    if len(parts) < 3:
        return {}, raw.strip()

    metadata = _parse_frontmatter(parts[1])
    return metadata, parts[2].strip()


def _reference_title(path: Path) -> str:
    return path.stem.replace("-", " ").replace("_", " ").title()


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
            metadata, _ = _split_frontmatter(skill_md.read_text(encoding="utf-8"))
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
            )

        return cls(root_dir=root_dir, skills=skills)

    def catalog_text(self) -> str:
        if not self._skills:
            return "No backend skills are available."

        parts: list[str] = []
        for skill in self._skills.values():
            refs = ", ".join(ref.id for ref in skill.references) or "none"
            parts.append(
                "\n".join(
                    [
                        f"- skill_name: {skill.name}",
                        f"  description: {skill.description}",
                        f"  reference_ids: {refs}",
                    ]
                )
            )
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

        selected_ids = {str(ref_id).strip() for ref_id in (reference_ids or []) if ref_id}
        reference_lookup = {ref.id: ref for ref in skill.references}

        parts: list[str] = []
        _, skill_body = _split_frontmatter(skill.path.read_text(encoding="utf-8"))
        if skill_body:
            parts.append(f"# Skill: {skill.name}\n\n{skill_body}")

        for ref_id in sorted(selected_ids):
            ref = reference_lookup.get(ref_id)
            if ref is None:
                continue
            body = ref.path.read_text(encoding="utf-8").strip()
            if body:
                parts.append(f"# Reference: {ref.id}\n\n{body}")

        context = "\n\n---\n\n".join(parts).strip()
        if not context:
            return fallback_text
        if len(context) <= max_chars:
            return context
        return context[:max_chars].rstrip() + "\n\n[Skill context truncated by backend limit.]"

    def suggest_references(self, skill_name: str | None, text: str) -> list[str]:
        skill = self._skills.get((skill_name or "").strip())
        if skill is None:
            return []

        available = {ref.id for ref in skill.references}
        lowered = text.lower()
        suggestions: list[str] = []

        mapping = {
            "thresholds-memory": [
                "memory",
                "buffer",
                "heap",
                "roll",
                "extended memory",
                "em utilization",
                "em/",
            ],
            "thresholds-database": ["database", "oracle", "sql", "db ", "tablespace"],
            "thresholds-performance": ["dialog", "workload", "response", "cpu", "swap", "hardware"],
            "thresholds-hana": [
                "hana",
                "indexserver",
                "nameserver",
                "column store",
                "row store",
                "delta merge",
                "savepoint",
            ],
            "thresholds-batch": ["batch", "background", "job", "sm37"],
            "thresholds-security": [
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
                "data admin",
                "system user",
                "listeninterface",
                "sql trace",
            ],
            "thresholds-operations": [
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
            ],
            "thresholds-continuity": [
                "availability",
                "outage",
                "restart",
                "update error",
                "number range",
                "backup",
                "recovery",
                "recoverability",
            ],
            "thresholds-integration": [
                "rfc load",
                "rfc gateway",
                "message server",
                "netweaver gateway",
                "odata",
                "/iwfnd/",
                "/iwbep/",
                "interface",
            ],
            "thresholds-lifecycle": [
                "maintenance phase",
                "support package",
                "kernel release",
                "database version",
                "operating system",
                "sqldbc",
                "important sap note",
            ],
            "thresholds-data-management": [
                "data volume",
                "dvm",
                "growth",
                "largest table",
                "archiv",
                "reorganization",
                "compression",
            ],
            "thresholds-data-quality": [
                "service data quality",
                "service readiness",
                "missing data",
                "grey rating",
                "not rated",
                "rtcctool",
                "sdccn",
                "st-pi",
                "ccdb",
            ],
            "remediation-performance": ["dialog", "workload", "response", "cpu", "swap", "hardware"],
            "remediation-memory": [
                "memory",
                "buffer",
                "heap",
                "roll",
                "extended memory",
                "em utilization",
                "em/",
            ],
            "remediation-database": ["database", "oracle", "sql", "db ", "tablespace"],
            "remediation-hana": [
                "hana",
                "indexserver",
                "nameserver",
                "column store",
                "row store",
                "delta merge",
                "savepoint",
            ],
            "remediation-batch": ["batch", "background", "job", "sm37"],
            "remediation-security": [
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
                "data admin",
                "system user",
                "listeninterface",
                "sql trace",
            ],
            "remediation-operations": [
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
            ],
            "remediation-continuity": [
                "availability",
                "outage",
                "restart",
                "update error",
                "number range",
                "backup",
                "recovery",
                "recoverability",
            ],
            "remediation-integration": [
                "rfc load",
                "rfc gateway",
                "message server",
                "netweaver gateway",
                "odata",
                "/iwfnd/",
                "/iwbep/",
                "interface",
            ],
            "remediation-lifecycle": [
                "maintenance phase",
                "support package",
                "kernel release",
                "database version",
                "operating system",
                "sqldbc",
                "important sap note",
            ],
            "remediation-data-management": [
                "data volume",
                "dvm",
                "growth",
                "largest table",
                "archiv",
                "reorganization",
                "compression",
            ],
            "remediation-data-quality": [
                "service data quality",
                "service readiness",
                "missing data",
                "grey rating",
                "not rated",
                "rtcctool",
                "sdccn",
                "st-pi",
                "ccdb",
            ],
            "correlations": ["correlation", "related", "compound", "cascade"],
        }
        for ref_id, keywords in mapping.items():
            if ref_id in available and any(keyword in lowered for keyword in keywords):
                suggestions.append(ref_id)

        # HANA-specific guidance already covers HANA availability, restart,
        # backup, and recovery sections. Avoid adding the generic continuity
        # pair for the same text so fallback loading stays focused.
        if "thresholds-hana" in suggestions:
            suggestions = [
                ref_id
                for ref_id in suggestions
                if ref_id not in {"thresholds-continuity", "remediation-continuity"}
            ]

        # A HANA security subsection should use the focused security pair rather
        # than also loading the broad HANA operations pair.
        hana_security_markers = (
            "audit trail",
            "audit policy",
            "data admin",
            "system user",
            "listeninterface",
            "sql trace",
        )
        if "thresholds-security" in suggestions and any(
            marker in lowered for marker in hana_security_markers
        ):
            suggestions = [
                ref_id
                for ref_id in suggestions
                if ref_id not in {"thresholds-hana", "remediation-hana"}
            ]

        if "core-analysis" in available:
            suggestions.insert(0, "core-analysis")

        if suggestions:
            return list(dict.fromkeys(suggestions))

        if "core-analysis" in available:
            return ["core-analysis"]
        return []
