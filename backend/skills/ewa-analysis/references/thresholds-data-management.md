# Data Volume Management Assessment

Use this reference for database size and growth, largest tables or indexes, row
and column store footprint, archiving, deletion, reorganization, compression,
housekeeping, and DVM sections.

## Assessment Rules

- Preserve current size, unit, observation period, absolute and percentage
  growth, forecast horizon, free capacity, and the largest contributing objects.
- Do not compare percentage growth without the absolute base; rapid growth of a
  small object and modest growth of a multi-terabyte object imply different risk.
- Distinguish live business data, technical/log data, temporary data, duplicates,
  and reclaimable free space.
- Treat table size as a prioritization signal, not proof that data can be deleted
  or archived.
- Assess archiving/deletion candidates against application ownership, legal hold,
  retention, residence time, audit, downstream use, and restore/read-access needs.
- Distinguish logical data reduction from physical space reclamation. Archiving,
  deletion, compression, and database reorganization are separate actions.
- Use the report's forecast and rating when supplied; generic monthly growth or
  utilization values are triage heuristics only.

## Severity Guidance

- Critical: imminent capacity exhaustion that can stop writes or availability.
- High: forecast capacity breach within the operational lead time, or growth
  materially degrading backup, recovery, maintenance, or performance.
- Medium: sustained avoidable growth, missing ownership/retention strategy, or
  measurable reduction opportunity without near-term availability risk.
