# Integration and Gateway Remediation

## RFC Workload and Failures

Actions:

- Use `ST03N`, `STAD`, `SM58`, `SMQ1`, `SMQ2`, and `SM59` as applicable to
  identify the caller, destination, queue, failure, and dominant time component.
- Validate the remote system and network before tuning the local system.
- Reduce excessive chatty calls through application/interface design and tested
  batching; do not increase work processes to mask a remote bottleneck.

## RFC Gateway, Message Server, and ICM

Actions:

- Use `SMGW`, `SMMS`, `SMICM`, and current SAP guidance to validate exposure,
  ACL behavior, logs, certificates, and profile settings.
- Build least-privilege `reginfo`/`secinfo` rules from observed required traffic,
  test in the appropriate logging/simulation mode, and retain rollback access.
- Validate release-specific parameter changes and schedule them through change
  control.

## SAP NetWeaver Gateway/OData

Actions:

- Use `/IWFND/ERROR_LOG` on the hub and `/IWBEP/ERROR_LOG` on the backend to
  group errors by service, code, user, and time.
- Validate metadata cache and logging configuration using the report-specified
  checks; keep production logs sufficient for diagnosis without recording
  sensitive payload data unnecessarily.
- Verify the cache cleanup job and retest the affected OData service after the
  root cause is corrected.

Effort: Medium. Priority: Immediate for a stopped critical interface or active
security exposure; otherwise Short-term.
