# SQL Statement Assessment

Use this reference for EWA sections on top/expensive SQL statements, SQL plan
cache, statement hashes, thread distribution, correlation coefficients, known
issues, and missing indexes. It applies to HANA and non-HANA databases
(ST04/DBACOCKPIT top SQL, SQL cache).

## Assessment Rules

- Capture statement hash/ID, total elapsed time, executions, elapsed time per
  execution, records per execution, user/origin, and the analysis window.
  Keep units; do not compare different windows.
- High total elapsed with tiny time per execution is a frequency problem
  (caller loops, chatty code). High time per execution is a single-statement
  inefficiency (plan, filter, data volume).
- Thread-state or thread-method distributions ("Thread Distribution") are
  hints, not proof. CPU, lock wait, network, I/O, or Join/Search dominance
  points to where to look next.
- CPU/memory correlation coefficients shown in the report (for example 0.31
  labelled "medium") show association, not cause.
- SAP-internal or monitoring statements (`_SYS_STATISTICS`, `_SYS_*`, SAP
  internal SQL flag, origin statistics server/monitoring) are no finding or Low.
  Raise only if SAP rates them red/yellow or lists a Known Issue; cite the
  SAP Note the report gives.
- One finding per statement hash across all "Top Statements" lists (elapsed,
  executions, memory, records). Cite the other lists as extra evidence.
- Image-only "Statement History" sections without readable numbers are not
  evidence.

## Severity Guidance

- Use the report's own rating first.
- High only when the report rates it red, or one statement dominates DB time
  and the section shows business impact.
- Medium for a recurring expensive custom statement or a Known Issue without
  shown impact.
- Low or no finding for internal/monitoring statements and isolated entries.
