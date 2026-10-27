"""Hierarchy-aware task grouping; source sections remain the coverage units."""
from __future__ import annotations

import re

from bs4 import BeautifulSoup

from ewa_pipeline.config import Config
from ewa_pipeline.indexer.tree_navigator import TreeNode, flatten_tree
from ewa_pipeline.report.schemas import OrchestratorPlan


# SAP's own "Service Summary" chapter holds SAP's verdicts (Alert/Check Overview).
# Python reads it exactly (indexer/sap_summary.py), so the AI must not re-analyse it.
SAP_SUMMARY_TITLE = "service summary"
SAP_SUMMARY_SKIP_REASON = "SAP Service Summary — read by Python, see SAP vs Us"


def is_sap_summary_section(node: TreeNode) -> bool:
    """True for the top-level chapter, numbered ("1 Service Summary") or not."""
    title = re.sub(r"^[\d.\s]+", "", node.title or "").strip().lower()
    return node.level == 0 and title == SAP_SUMMARY_TITLE


def prepare_sections(tree: dict, sections: list[TreeNode], content: dict[str, str]):
    metadata: dict[str, dict] = {}
    contexts: dict[str, str] = {}

    def visit(node: TreeNode, ancestors: list[str], branch: str):
        metadata[node.id] = {"parent_id": ancestors[-1] if ancestors else "",
                             "ancestor_ids": ancestors, "branch_id": branch}
        contexts[node.id] = f"{node.title}\n{BeautifulSoup(node.content, 'html.parser').get_text(' ', strip=True)}"
        for child in node.children:
            visit(child, [*ancestors, node.id], branch)

    for node in flatten_tree(tree):
        visit(node, [], node.id)
    return ([{"id": node.id, "title": node.title, "summary": node.summary,
              "content_chars": len(content[node.id]),
              **metadata.get(node.id, {"parent_id": "", "ancestor_ids": [], "branch_id": node.id})}
             for node in sections], contexts)


def parent_context(section_ids: list[str], sections: list[dict], contexts: dict[str, str], limit: int):
    """Bounded, explicitly supplementary ancestor excerpts, never owned source text."""
    lookup = {s["id"]: s for s in sections}
    candidates = []
    for sid in section_ids:
        # Prefer immediate parents over distant front matter.
        for ancestor in reversed(lookup[sid].get("ancestor_ids", [])):
            # Ancestors without an excerpt (e.g. the excluded Service Summary) are not re-injected.
            if ancestor in contexts and ancestor not in section_ids and ancestor not in candidates:
                candidates.append(ancestor)
    parts, included = [], []
    remaining = limit
    for ancestor in candidates:
        if remaining <= 0:
            break
        value = f"Ancestor {ancestor} (context excerpt only):\n{contexts.get(ancestor, '')}\n"
        parts.append(value[:remaining])
        remaining -= len(parts[-1])
        included.append(ancestor)
    return "".join(parts), included


def planning_catalogue(sections: list[dict], contexts: dict[str, str]):
    """List each source/container once; parent IDs encode the hierarchy compactly."""
    sources = {s["id"]: s for s in sections}
    parents = {}
    for section in sections:
        path = [*section.get("ancestor_ids", []), section["id"]]
        for index, sid in enumerate(path):
            parents[sid] = path[index - 1] if index else ""
    result = []
    for sid in dict.fromkeys([*contexts, *sources]):
        if sid not in parents:
            continue
        source = sources.get(sid)
        row = {"id": sid, "parent": parents[sid],
               "title": source["title"] if source else contexts[sid].split("\n", 1)[0],
               "source": source is not None}
        if source:
            row.update(chars=source.get("content_chars", 0), preview=source.get("summary", "")[:80])
        result.append(row)
    return result


def validate_plan(plan: OrchestratorPlan | None, sections_available: list[dict], config: Config | None = None):
    """Validate grouped ownership; split by budgets and backfill with hierarchy groups.

    Invalid groups are rejected as a whole. First valid owner wins. Omitted sources
    receive bounded fallback tasks, never a silent coverage exemption. A source
    larger than the source budget is retained and flagged for explicit failure.
    """
    max_sections = config.max_task_sections if config else 12
    max_chars = config.max_task_content_chars if config else 48000
    available = {s["id"]: s for s in sections_available}
    if len(available) != len(sections_available):
        raise ValueError("Source section IDs must be unique before planning")
    order = {s["id"]: i for i, s in enumerate(sections_available)}
    tasks, origins, notes = [], {}, []

    def append_group(ids, title, focus, skill, references, origin):
        current, size = [], 0

        def flush():
            if current:
                tasks.append({"section_ids": list(current), "section_title": title,
                    "analysis_focus": focus, "skill_name": skill or "ewa-analysis",
                    "reference_ids": references or [], "source_content_chars": size,
                    "oversized": size > max_chars, "task_origin": origin})

        for sid in sorted(ids, key=order.__getitem__):
            chars = available[sid].get("content_chars", 0)
            if current and (len(current) >= max_sections or size + chars > max_chars):
                flush()
                current, size = [], 0
            current.append(sid)
            size += chars
            origins[sid] = origin
        flush()

    rejected = 0
    for item in plan.tasks if plan else []:
        ids = [str(sid).strip("[]'\" ") for sid in item.section_ids]
        if (not ids or len(set(ids)) != len(ids)
                or any(sid not in available or sid in origins for sid in ids)):
            rejected += 1
            continue
        append_group(ids, item.section_title, item.analysis_focus, item.skill_name, item.reference_ids, "planner")
    if rejected:
        notes.append(f"{rejected} invalid, duplicate, or overlapping planner group(s) rejected.")

    missing = [s for s in sections_available if s["id"] not in origins]
    if missing:
        if not tasks:
            notes.append("No usable grouped plan; bounded hierarchy fallback used.")
        # Only combine adjacent uncovered sources belonging to the same root branch.
        current, branch = [], None
        for section in missing:
            next_branch = section.get("branch_id", section["id"])
            if current and next_branch != branch:
                append_group(current, available[current[0]]["title"], "Review related measurements together; retain individual source attribution.",
                             "ewa-analysis", [], "default")
                current = []
            current.append(section["id"])
            branch = next_branch
        if current:
            append_group(current, available[current[0]]["title"], "Review related measurements together; retain individual source attribution.",
                         "ewa-analysis", [], "default")
        notes.append(f"{len(missing)} omitted source section(s) assigned to hierarchy fallback; none dropped.")
    for index, task in enumerate(tasks, 1):
        task["task_id"] = f"T{index:04d}"
    oversized = sum(t["oversized"] for t in tasks)
    if oversized:
        notes.append(f"{oversized} individual source(s) exceed the source budget; recorded as failures without truncation or model calls.")
    return tasks, origins, notes
