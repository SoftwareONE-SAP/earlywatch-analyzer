# Security and Compliance Thresholds

Use this reference for EWA sections about ABAP and HANA users, authorizations,
default passwords, audit policy, RFC and message-server exposure, HANA network
settings, kernel age, support packages, and security configuration.

| Metric | Healthy | Warning | Critical | Transactions | Notes |
| --- | --- | --- | --- | --- | --- |
| Users with SAP_ALL in production | 0 | 1-3 | > 3 | SUIM | SAP_ALL bypasses authorization checks |
| Default passwords unchanged | 0 | Any | Direct exposure | RSUSR003 | Well-known credentials are high risk |
| RFC destinations without authentication | 0 | Any | External/open exposure | SM59 | Can enable lateral movement |
| Password policy violations | 0 | Any | Widespread weak policy | RZ10, SU01 | Usually High in production |
| Kernel patch level age | < 6 months | 6-12 months | > 12 months | SM51 | Old kernels miss fixes |
| Support package age | < 12 months | 12-24 months | > 24 months | SPAM | Old SPs increase maintenance and compliance risk |
| Locked/obsolete users active | 0 | Any | Privileged obsolete users | SUIM | Review ownership and validity |

## HANA-Specific Assessment

- Preserve the report's rating and exact evidence for HANA audit status,
  applicable audit policies, password policy, SQL trace level, internal-service
  and system-replication network settings, and maintenance status.
- For the `SYSTEM` user, assess activation, validity, recent use, alternative
  named administrators, and emergency-access design. Do not recommend disabling
  the only viable administrator without a tested alternative.
- For `DATA ADMIN` and other system privileges, identify the grantee type,
  business/technical owner, direct versus role grant, and production need.
- For network/listen-interface findings, capture topology, tenant/system DB,
  replication configuration, source networks, encryption, and external
  reachability before assigning severity.
- SQL trace can expose sensitive statement or business data and create overhead;
  assess level, scope, destination, retention, and whether it is temporarily
  enabled for an active investigation.
- HANA security settings are revision- and topology-specific. Use report values
  as evidence and validate remediation in current SAP HANA security guidance.

Severity guidance:

- Security findings default to High in production unless clearly informational.
- Critical requires immediate exposure, active compromise indicator, or broad
  privileged access with exploitable external paths.
- Medium can apply to patch currency issues without current exposure.
- Missing audit, user, or network evidence is a coverage gap, not proof of secure
  configuration.
