# SQL Statement Remediation

## Expensive or Frequent SQL Statements

Validate first:

- Confirm the full statement text and hash against the report.
- Review the execution plan and records returned versus scanned.
- Find the calling program, user, and origin.
- Confirm the time window; a one-off batch run is not a standing problem.

Tools: `SQLM` (SQL Monitor) to link statements to programs, `ST05` (SQL trace)
for a reproducible run, `ST04`/`DBACOCKPIT` for top SQL and SQL cache, `ST12`
for combined ABAP/SQL trace, and on HANA the SQL plan cache
(`M_SQL_PLAN_CACHE`) and the Expensive Statements trace.

Options, in order:

- Fix the calling ABAP/custom code or filters: remove loops that repeat one
  statement, add selective WHERE conditions, avoid reading unused columns.
- Add or adjust an index only after plan review confirms it will be used and
  its write cost is acceptable.
- Follow the SAP Note named in the report for a Known Issue; check it applies
  to the installed release first.
- If records scanned grow with data volume, plan archiving or data reduction.
- Do not change database parameters as a fix for a single statement.

Verify with the same statement over a representative workload period.

Effort: Medium. Priority: Short-term, or Immediate when one statement is
causing current user-facing delay.
