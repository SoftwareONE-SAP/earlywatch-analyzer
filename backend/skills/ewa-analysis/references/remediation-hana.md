# SAP HANA Remediation

## Alerts, Restarts, and Resource Pressure

Actions:

- Use SAP HANA cockpit, `DBACOCKPIT`, or Database Explorer to confirm the exact
  alert history, service event, host, and observation window.
- Correlate with diagnosis files, OOM events, expensive statements, savepoints,
  merges, backups, and infrastructure events before assigning a root cause.
- Contain a current capacity risk through approved workload controls or space
  extension; do not change HANA parameters from a generic threshold.
- Validate any parameter or revision action against current SAP Help and the
  exact SAP Note/KBA for the installed revision.
- Verify alert clearance and behavior over a representative workload period.

Effort: Medium to High. Priority: Immediate for active availability or data
risk; otherwise Short-term.

## Backup and Recoverability

Actions:

- Confirm data and log backup history, destination availability, catalog state,
  and `backup.log`/`backint.log` errors in HANA cockpit or Database Explorer.
- Preserve the existing backup chain while investigating; do not delete catalog
  entries or backup files as a first response.
- Run supported backup-integrity and recoverability checks appropriate to the
  installed HANA release and backup tool.
- Test recovery in an isolated environment against agreed RPO/RTO; document the
  result, required media, credentials, and runbook owner.

Effort: Medium to High. Priority: Immediate for a broken backup chain or no
recoverable copy; otherwise Short-term.

## Row Store and Delta Merge

Actions:

- Confirm reclaimable row-store memory or persistent delta-merge symptoms using
  HANA tooling and the report's recommendation.
- Review write workload, merge history, memory headroom, and affected tables.
- Schedule reorganization or corrective work through change control with tested
  rollback/recovery arrangements; validate release-specific procedures first.

Effort: Medium to High. Priority: Medium-term unless active resource pressure is
causing failures.
