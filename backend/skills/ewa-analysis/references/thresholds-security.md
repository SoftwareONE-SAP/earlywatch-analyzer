# Security and Compliance Thresholds

Use this reference for EWA sections about users, authorizations, default
passwords, RFC destinations, kernel age, support packages, and security
configuration.

| Metric | Healthy | Warning | Critical | Transactions | Notes |
| --- | --- | --- | --- | --- | --- |
| Users with SAP_ALL in production | 0 | 1-3 | > 3 | SUIM | SAP_ALL bypasses authorization checks |
| Default passwords unchanged | 0 | Any | Direct exposure | RSUSR003 | Well-known credentials are high risk |
| RFC destinations without authentication | 0 | Any | External/open exposure | SM59 | Can enable lateral movement |
| Password policy violations | 0 | Any | Widespread weak policy | RZ10, SU01 | Usually High in production |
| Kernel patch level age | < 6 months | 6-12 months | > 12 months | SM51 | Old kernels miss fixes |
| Support package age | < 12 months | 12-24 months | > 24 months | SPAM | Old SPs increase maintenance and compliance risk |
| Locked/obsolete users active | 0 | Any | Privileged obsolete users | SUIM | Review ownership and validity |

Severity guidance:

- Security findings default to High in production unless clearly informational.
- Critical requires immediate exposure, active compromise indicator, or broad
  privileged access with exploitable external paths.
- Medium can apply to patch currency issues without current exposure.
