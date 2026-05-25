# Database Remediation

## High DB Request Time

Actions:

- Use `ST03N` to confirm workload impact and affected task types.
- Use `ST04` or `DBACOCKPIT` to inspect wait events, cache hit ratios, and
  expensive statements.
- Use `ST05` or SQL Monitor for suspect custom transactions.
- Tune SQL or indexes when one statement dominates elapsed time.
- Increase DB buffer/memory only when cache evidence supports sizing as root
  cause.

Effort: Medium to High. Priority: Short-term or Immediate if users are impacted.

## Space or Growth Risk

Actions:

- Use `DB02` to confirm tablespace utilization and growth trend.
- Extend tablespace or storage when utilization is near critical thresholds.
- Identify largest growing tables.
- Start an archiving plan with `SARA`/ADK where business retention permits.

Effort: Medium. Priority: Immediate if above 90% and growing; otherwise
Medium-term.
