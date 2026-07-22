# Availability and Continuity Assessment

Use this reference for collector-based availability, planned/unplanned restarts,
update errors, failed business updates, critical number ranges, data/log backups,
recovery readiness, and monitoring continuity.

## Assessment Rules

- Preserve the observation period and data source. Collector gaps reduce
  confidence and must not be interpreted as uptime.
- Separate planned maintenance from unplanned outage and report both frequency
  and business duration where available.
- For update errors, capture affected update module, transaction, user, client,
  timestamp, recurrence, and whether the business document was reposted or lost.
- For number ranges, record object/subobject, client, interval, percentage or
  forecast to exhaustion, buffering context, and business process.
- For backups, distinguish configuration, last successful data backup, log
  backup continuity, failures, retention, off-host copies, integrity checks, and
  tested recovery when those controls are in scope. Never infer RPO/RTO
  compliance unless the targets are stated.
- Treat an explicitly missing, failed, overdue, or required recovery test as a
  recoverability assurance gap, not proof that recovery will fail. Mere omission
  from a summary section is a validation question, not a finding.

## Severity Guidance

- Critical: current outage, update failures blocking postings, imminent number
  range exhaustion, or no viable recovery path for critical data.
- High: repeated unplanned outages, recurring update loss, broken log/data
  backup chain, or a near-term exhaustion forecast.
- Medium: incomplete availability collection, untested recovery, or continuity
  process drift without current impact.
