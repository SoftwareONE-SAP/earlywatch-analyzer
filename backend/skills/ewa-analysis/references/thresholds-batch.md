# Batch Processing Thresholds

Use this reference for EWA sections about background jobs, failed jobs,
long-running jobs, background work processes, scheduler health, and batch/dialog
contention.

| Metric | Healthy | Warning | Critical | Transactions | Notes |
| --- | --- | --- | --- | --- | --- |
| Failed jobs as percent of total | < 1% | 1-5% | > 5% | SM37 | Failed jobs can mean failed business processes |
| Long-running jobs | 0 | 1-3 | > 3 | SM37 | Long jobs hold work processes and delay chains |
| Background WP utilization | < 70% | 70-90% | > 90% | SM50, SM66 | Near saturation means new jobs queue |
| Jobs delayed past scheduled start | < 5 min | 5-30 min | > 30 min | SM37 | Indicates scheduling or capacity contention |
| Cancelled critical jobs | 0 | 1 | > 1 | SM37 | Severity depends on business function |

Severity guidance:

- Critical if failed or delayed jobs stop business-critical processing.
- High if repeat failures affect finance, billing, logistics, payroll, or
  interface jobs.
- Medium for capacity pressure or cleanup needed without current business impact.
