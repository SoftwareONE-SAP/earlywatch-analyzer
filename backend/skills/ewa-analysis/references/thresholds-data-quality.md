# EWA Service Data Quality Assessment

Use this reference for Service Data Quality, Service Readiness, RTCCTOOL, SDCCN,
ST-PI, missing service modules, grey/not-rated checks, missing hardware or Java
performance data, BW/RCA gaps, CCDB gaps, and SAP backbone transmission issues.

## Assessment Rules

- Capture the missing collector/module or data source, affected section/check,
  observation period, report message, and whether the rating is grey or omitted.
- State which conclusions cannot be made. Missing hardware data, for example,
  limits capacity assessment; it does not prove hardware is healthy or unhealthy.
- Distinguish collection, transfer, processing-timing, BW/RCA, CCDB, LMDB, and
  outdated collector-content causes.
- Do not infer the exact cause from a generic missing-data message. Use the
  report's function module, context, note, and diagnostic message when present.
- Repeated or broad missing data is more important than one optional metric,
  especially when it suppresses security, availability, or capacity checks.

## Severity Guidance

- High when missing data hides an active critical control area or most of the
  report is not assessable.
- Medium for material section-level blind spots or repeated collector failures.
- Low for an isolated optional metric with alternative current evidence.
