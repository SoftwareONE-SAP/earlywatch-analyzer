# EWA Core Analysis Guidance

## Workflow

1. Extract all numerical values, percentages, dates, status indicators, and SAP
   object names from the section.
2. Compare each metric with the relevant domain threshold.
3. Assess impact in business terms: user experience, availability, data risk,
   compliance, or operational debt.
4. Create one finding per discrete issue. Do not bundle unrelated symptoms.
5. Write specific remediation with SAP transactions, parameters, or procedures.
6. Calibrate severity from impact and urgency, not from color alone.

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

Common EWA domains include system information, hardware capacity, SAP memory,
ABAP workload, database performance, batch processing, security, spool, transport
management, system logs, and dumps.
