# Security Remediation

## Excessive Privilege

Actions:

- Use `SUIM` to list users with `SAP_ALL`, `SAP_NEW`, or broad critical roles.
- Confirm business owner and production need.
- Remove broad roles and replace with least-privilege role sets.
- Lock or expire obsolete privileged users.

Effort: Medium. Priority: Immediate for unknown or shared privileged accounts.

## Default Passwords and Weak Policy

Actions:

- Use `RSUSR003` to check default passwords.
- Reset default or weak passwords immediately.
- Review password profile parameters in `RZ10` or `RZ11`.
- Enforce password length, complexity, expiration, and failed-login lockout.

Effort: Low. Priority: Immediate for default passwords in production.

## RFC Exposure

Actions:

- Use `SM59` to review RFC destinations and authentication.
- Remove anonymous or obsolete destinations.
- Rotate credentials for technical RFC users when exposure is suspected.
- Restrict authorizations and network access for RFC users.

Effort: Medium. Priority: Immediate when externally reachable or unauthenticated.

## HANA Audit, Privilege, and User Controls

Actions:

- Use HANA cockpit or Database Explorer to confirm audit status and policies,
  privileged users/roles, password policy, trace configuration, and recent
  security-relevant activity.
- Replace broad privileges such as `DATA ADMIN` with task-specific roles after
  confirming ownership, operational dependencies, and emergency access.
- Establish tested named administrator and emergency-access procedures before
  restricting or deactivating the `SYSTEM` user.
- Configure audit policy scope, target, retention, access, and alerting according
  to current SAP guidance and organizational legal/security requirements.
- Return temporary SQL trace to the approved production level after the
  investigation and protect or remove sensitive trace data under retention rules.

Effort: Medium. Priority: Immediate for unknown broad privilege or missing audit
on an exposed production system; otherwise Short-term.

## HANA Network Exposure

Actions:

- Map HANA internal-service and system-replication communication paths before
  changing listen-interface or encryption settings.
- Validate allowed source networks, segmentation, encryption, certificates, and
  replication health against the installed HANA revision and topology.
- Test connectivity and failover in a non-production environment, retain a
  rollback path, and verify all tenants/services after the controlled change.

Effort: Medium to High. Priority: Immediate for validated external exposure;
otherwise Short-term.
