# Data Volume Management Remediation

Actions:

- Use `DB02`/`DBACOCKPIT`, HANA cockpit, DVM tooling, and application-specific
  analysis to confirm growth history and object ownership.
- Rank candidates by absolute growth, capacity horizon, business value, age,
  technical reduction potential, and operational cost.
- Agree retention and residence rules with business, legal, privacy, records,
  audit, and application owners before deletion or archiving.
- Use supported application archiving such as `SARA`/ADK when applicable; test
  archive write, delete, storage, retrieval, reconciliation, and failure recovery.
- Treat database reorganization or compression as a separate change requiring
  database-specific validation, capacity headroom, backup, outage assessment,
  and rollback/recovery planning.
- Re-measure database size, growth, backup duration, and application behavior
  after the change.

Never recommend deleting a large table directly from size evidence alone.

Effort: Medium to High. Priority: Immediate for imminent capacity exhaustion;
otherwise Medium-term governance and reduction work.
