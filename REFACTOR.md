# Backend Lazy Skill Loading Refactor

## Current Problem

The backend currently reads `backend/skills/ewa-analysis/SKILL.md` and every
markdown file under `references/`, joins them into one large string, and passes
that text into analysis prompts. That means every LLM call receives broad skill
material even when a section only needs one small part of it.

This is wasteful and makes prompt context less focused.

## Target Behavior

The backend should treat skills like a small catalog plus lazily loaded files:

1. At planning time, show the LLM only compact skill cards: skill name,
   description, and available reference IDs.
2. The planner selects the relevant skill and reference IDs for each report
   section.
3. Plain backend code validates those IDs and reads only the selected markdown
   files from disk.
4. The section analyst receives the report section plus only the selected skill
   context.

The skill loader is plain code. It is not another LLM call.

## Loader Responsibilities

- Scan `backend/skills/*/SKILL.md`.
- Parse skill frontmatter for `name` and `description`.
- List available `references/*.md` files by stable reference ID.
- Build a compact catalog for the planner without reading reference bodies.
- Validate requested skill and reference IDs.
- Load the selected skill body and selected references only when a section is
  dispatched to the domain analyst.
- Cap loaded context size so a large file cannot bloat every prompt.
- Fall back safely when the planner requests unknown skills or references.

## Migration Steps

1. Replace the eager `_load_skills()` function with a `SkillRegistry`.
2. Store only compact `skills_catalog` text in graph state.
3. Extend section planning output with `skill_name` and `reference_ids`.
4. Resolve section skill context during the domain analyst dispatch step.
5. Shorten `SKILL.md` and move detailed EWA guidance into smaller reference
   files so lazy loading materially reduces prompt size.
6. Add tests for catalog generation, lazy loading, invalid IDs, and prompt
   construction.

## Test Plan

- Verify the planner catalog lists skills and reference IDs but does not contain
  full reference body text.
- Verify selected references are loaded into section analysis context.
- Verify invalid skill or reference IDs are ignored safely.
- Verify planner prompts use the compact catalog and domain prompts use selected
  context.
- Run backend unit tests and a Python compile check after implementation.
