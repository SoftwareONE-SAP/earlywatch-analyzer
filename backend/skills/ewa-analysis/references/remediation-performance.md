# Performance and Workload Remediation

## Slow Dialog or Transaction Workload

Actions:

- Use `ST03N` to preserve the report period and decompose response time into CPU,
  database, wait, load/generation, enqueue, and roll components.
- Identify the affected task type, application module, transaction, user group,
  instance, and time window before choosing a remedy.
- Use `STAD` for representative single-record analysis and `ST12` or `ST05` only
  for a controlled trace of a reproducible case.
- Correct the dominant component. Do not recommend hardware scaling when the
  evidence points to SQL, locks, RFC waits, or a small set of custom programs.
- Re-measure the same workload window after the change.

Effort: Medium. Priority: Short-term, or Immediate when a critical business
process is currently failing its service objective.

## CPU, Memory, or Instance Imbalance

Actions:

- Use `ST06`/`OS07`, `ST03N`, `SM50`, and `SM66` to confirm duration, peaks,
  run-queue or paging evidence, work-process state, and instance distribution.
- Separate host saturation from one runaway process and from uneven logon-group
  or operation-mode distribution.
- Stop or reschedule a confirmed runaway workload only through the system's
  operational change process.
- Validate virtualization, OS, database, and SAP headroom before resizing.

Effort: Medium to High. Priority: Immediate for sustained saturation with user
impact; otherwise Short-term capacity planning.
