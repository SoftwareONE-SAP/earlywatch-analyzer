# Integration and Gateway Assessment

Use this reference for RFC load, RFC destinations, RFC Gateway and message
server security, ICM, SAP NetWeaver Gateway/OData configuration, metadata cache,
logging, error logs, cleanup jobs, and interface availability.

## Assessment Rules

- For RFC workload, capture destination/caller, synchronous or asynchronous
  type, calls, total time, time per call, data volume, errors, and the business
  interface. High volume alone is not a defect.
- Correlate high RFC time with network, remote-system response, serialization,
  work-process, queue, and application evidence before assigning cause.
- For RFC Gateway security, assess the report's findings on `reginfo`, `secinfo`,
  ACL behavior, gateway logging, SNC, and external exposure. Do not infer secure
  configuration merely because files exist.
- For message server and ICM, preserve the exact report check, parameter, error,
  certificate, endpoint, and exposure context.
- For SAP NetWeaver Gateway, distinguish hub and embedded deployment. Assess
  metadata cache, log level, error frequency, cleanup jobs, affected service,
  HTTP status, and production/test/development role.
- Avoid exposing destinations, hostnames, users, tokens, or business payloads in
  finding text beyond what is necessary for remediation ownership.

## Severity Guidance

- Critical: active externally exploitable gateway path or integration failure
  stopping a critical business process.
- High: repeated interface failures, insecure external registration/start rules,
  or user-facing OData outage.
- Medium: inefficient RFC workload, risky logging, cache/cleanup configuration,
  or incomplete monitoring without active impact.
