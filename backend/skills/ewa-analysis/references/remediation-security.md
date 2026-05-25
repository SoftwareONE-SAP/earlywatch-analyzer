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
