# EWA Service Data Quality Remediation

Actions:

- Use `SDCCN` to inspect the exact EWA session log, collection status, timing,
  transfer status, and module/function named by the report.
- Use `ST13`/`RTCCTOOL` to validate service preparation and current collector
  prerequisites; validate any ST-PI/ST-A/PI update against current SAP guidance.
- For BW/RCA gaps, verify the corresponding extractor/data-provider chain and
  the report's cited diagnostic path.
- For CCDB gaps, inspect the managed-system configuration collection and errors
  in the applicable CCDB tooling.
- Confirm SAP backbone connectivity and that service-definition maintenance is
  current when transmission or content is missing.
- Repeat or regenerate the EWA only after the missing data has arrived; verify
  that the previously grey/omitted section now contains a complete observation
  period.

Effort: Low to Medium. Priority: Short-term, or Immediate when the blind spot
prevents validation of an active security, availability, or capacity concern.
