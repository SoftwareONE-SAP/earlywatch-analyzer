# EWA Core Analysis Guidance

## Workflow

1. Establish the section's scope, observation period, system role, database,
   release, and whether the data is complete enough to assess.
2. Extract all numerical values, units, percentages, dates, trends, status
   indicators, alert IDs, SAP object names, and report recommendations.
3. Apply evidence in this order: the report's explicit rating or target; a
   release-specific value quoted in the report; local skill guidance; then a
   clearly labelled heuristic.
4. Compare like with like. Preserve units and observation windows, distinguish
   average from peak and current value from trend, and do not infer a trend from
   one measurement.
5. Assess impact in business terms: user experience, availability,
   recoverability, data risk, compliance, or operational debt.
6. Create one finding per discrete issue. Link related symptoms in the
   description, but do not duplicate the same root issue across nested sections.
7. Write staged remediation: validate, contain if urgent, correct the root
   cause, and verify after a representative workload period.
8. Calibrate severity from evidence, impact, exposure, and urgency, not from
   color alone.

## Evidence Guardrails

- Treat the EWA report's own threshold and rating as authoritative for that
  report unless the section says the data is missing or stale.
- Treat skill thresholds as triage guidance, not universal SAP limits. Release,
  database, OS, workload, system role, and customer SLA can change the target.
- Never invent a parameter value, SAP Note number, maintenance deadline,
  retention period, recovery objective, or capacity target.
- Quote the metric and its context. Prefer `peak CPU 91% during 09:00-10:00`
  over `CPU is high`.
- Distinguish observed fact, report recommendation, likely cause, and proposed
  validation. Do not present a likely cause as proven.
- If the report explicitly marks data required for its assessment as missing,
  create a coverage/monitoring finding rather than declaring the component
  healthy. Do not turn every control or data point omitted from a summary into a
  finding; state it as a limitation or validation question instead.
- For configuration, security, version, sizing, deletion, reorganization, and
  recovery changes, require validation against current SAP Help or the exact
  SAP Note/KBA for the installed release before execution.

## Severity Calibration

| Severity | Use When | Timeframe |
| --- | --- | --- |
| Critical | System failure or data loss is plausible or already happening | 24-48 hours |
| High | Users, SLAs, security, or compliance are materially affected | 1-2 weeks |
| Medium | Stable but suboptimal configuration, trend, or incomplete monitoring | Next maintenance window |
| Low | Best-practice drift with no current operational impact | Next project cycle |

Rules:

- A red metric is not automatically Critical.
- Security findings default to High unless clearly informational or already
  creating immediate compromise risk.
- Missing monitoring data is usually Medium because operations cannot validate
  health.
- Do not escalate solely because a heuristic threshold is crossed. Require
  corroborating duration, trend, business impact, or report rating.
- Use Healthy only when the section has no meaningful issue or only Low findings.

## Output Expectations

Every finding needs:

- a precise title,
- specific evidence from the report,
- severity,
- business impact,
- an actionable remediation,
- relevant SAP transactions,
- effort estimate,
- priority.

Use an empty findings array when the section contains sufficient, current
evidence and no issue. Data explicitly reported as missing, stale,
contradictory, or incomplete is not evidence of health. A topic simply outside
the section's stated scope does not create a finding by itself.

Common EWA domains include system information, hardware capacity, SAP memory,
ABAP workload, database performance, batch processing, security, spool, transport
management, system logs, and dumps.
