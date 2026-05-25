# Batch Processing Remediation

## Failed or Cancelled Jobs

Actions:

- Use `SM37` to filter failed jobs by date, user, job name, and status.
- Inspect job logs and spool output for the real failure cause.
- Identify whether the job supports a business-critical process.
- Fix authorization, variant, program, interface, or data issues before rerun.

Effort: Low to Medium. Priority: Immediate for critical business jobs.

## Batch Capacity Contention

Actions:

- Use `SM50` and `SM66` to inspect background work process saturation.
- Reschedule non-critical jobs away from dialog peak windows.
- Use operation modes to allocate background capacity by time window.
- Add dedicated batch servers if contention is structural.
- Review long-running jobs for SQL or program tuning.

Effort: Medium. Priority: Short-term when delays affect users or job chains.
