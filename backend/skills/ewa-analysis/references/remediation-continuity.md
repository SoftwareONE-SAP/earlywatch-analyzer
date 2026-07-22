# Availability and Continuity Remediation

## Availability and Restarts

Actions:

- Correlate the EWA period with `SM21`, `ST22`, `SM50`/`SM66`, host monitoring,
  database events, and approved maintenance records.
- Classify each outage as planned, application, database, OS, infrastructure, or
  unknown; assign an owner and eliminate repeated unknown causes.
- Validate alerting and collector coverage after correction.

## Update Errors and Number Ranges

Actions:

- Use `SM13` to group update failures and confirm the business-document outcome
  before any repeat processing.
- Fix the underlying application, lock, database, authorization, or capacity
  cause; rerun only through an approved business reconciliation procedure.
- Use `SNRO`/`SNUM` and the owning application transaction to confirm number-range
  consumption and forecast. Extend intervals only after checking legal,
  year-dependent, buffering, transport, and application constraints.

## Backup and Recovery Assurance

Actions:

- Confirm backup jobs, logs, destinations, retention, integrity checks, and
  alerts with the database-specific supported tools.
- Compare actual protection with approved RPO/RTO and retention requirements.
- Perform a controlled restore/recovery test and record evidence; never test by
  overwriting the production system.

Effort: Medium to High. Priority: Immediate for active business or data risk;
otherwise Short-term.
