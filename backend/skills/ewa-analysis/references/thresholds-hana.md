# SAP HANA Assessment Guidance

Use this reference for HANA stability and alerts, service restarts, availability,
configuration, persistence, resource consumption, row/column store, delta merge,
backup, diagnosis files, statistics server, and important-note sections.

## Assessment Rules

- Preserve the HANA alert ID, rating, affected host/service, first and last
  occurrence, frequency, and report recommendation. A repeated active alert is
  stronger evidence than an isolated historical alert.
- Evaluate service restarts against cause, service, host, timing, recurrence,
  and availability impact. Do not treat every planned restart as instability.
- For memory, distinguish allocation limit, used memory, resident memory,
  peak usage, table memory, and temporary/statement memory. Correlate with OOM
  events and workload before recommending a limit change.
- For disk and persistence, assess data, log, trace, and backup destinations
  separately. Preserve both utilization and growth horizon.
- For row-store fragmentation, use the report's estimated reclaimable memory
  and SAP recommendation; size alone does not prove reorganization is needed.
- For delta merge, examine delta size, merge duration/failures, write rate, and
  resource pressure together. Delta merge temporarily needs additional memory.
- For backup and recovery, assess recent successful data and log backups,
  failures, catalog/retention symptoms, recoverability evidence, and whether a
  restore or recovery check is documented when the section covers it. Backup
  success alone does not prove recoverability, but absence of restore-test detail
  from a backup summary does not prove that testing is missing. Create a finding
  only for explicit failed, missing, overdue, or required recoverability evidence;
  otherwise state the scope limitation without changing the section rating.
- Treat parameter recommendations, revision currency, and important SAP Notes
  as release-specific. Quote the report and require current external validation.

## Severity Guidance

- Critical: current unavailability, unrecoverable business data risk, full log
  or data volume stopping writes/startup, or repeated failures with active impact.
- High: recurring unplanned service restarts, failed backup chain, severe
  resource pressure with workload impact, or active high-priority HANA alerts.
- Medium: growth, fragmentation, configuration, monitoring, or recoverability
  evidence gaps without current business impact.
