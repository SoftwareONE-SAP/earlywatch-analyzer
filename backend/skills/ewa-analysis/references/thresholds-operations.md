# Operations and Maintenance Thresholds

Use this reference for EWA sections about spool, TemSe, transports, system logs,
ABAP dumps, ICM, enqueue, locks, kernel currency, support packages, and general
Basis maintenance.

| Metric | Healthy | Warning | Critical | Transactions | Notes |
| --- | --- | --- | --- | --- | --- |
| Short dumps per day | < 10 | 10-50 | > 50 | ST22 | Repeated dump types need root cause analysis |
| New unique dump types | Stable | Increasing | Rapidly increasing | ST22 | New dump families may indicate a recent regression |
| System restarts in 30 days | 0-1 | 2-3 | > 3 | SM21 | Unexpected restarts are stability findings |
| Security-related syslog events | 0 | Any | Repeated or privileged | SM21 | Check failed logons and authorization events |
| TemSe object count | < 10,000 | 10,000-50,000 | > 50,000 | SP01 | Old spool objects consume filesystem/database space |
| Old spool/TemSe objects | < 7 days | 7-30 days | > 30 days | SP01 | Cleanup should be scheduled |
| Failed print requests | < 1% | 1-5% | > 5% | SP01 | May indicate printer or spool server issues |
| Import errors | 0 | 1-3 | > 3 | STMS | Failed imports can leave systems inconsistent |
| Import queue age | < 7 days | 7-30 days | > 30 days | STMS | Old queues indicate change-process issues |
| ICM thread utilization | < 60% | 60-80% | > 80% | SMICM | High utilization can degrade HTTP/Fiori traffic |
| ICM connection errors | 0 | < 10/day | > 10/day | SMICM | Often certificate, network, or backend issues |
| Enqueue rejects | 0 | < 10/day | > 10/day | SM12 | Rejects indicate lock table pressure or contention |
| Lock wait time | < 100ms | 100-500ms | > 500ms | SM12 | Long waits indicate blocking transactions |
| Enqueue table utilization | < 50% | 50-75% | > 75% | SM12 | Review `enque/table_size` and application locks |
| Kernel patch age | < 6 months | 6-12 months | > 12 months | SM51 | Old kernels miss fixes |
| Support package age | < 12 months | 12-24 months | > 24 months | SPAM | Old SPs increase support and compliance risk |

Severity guidance:

- Critical when operational failures stop business processing, cause repeated
  restarts, block transports, or exhaust spool/enqueue capacity.
- High when repeated errors affect users or compliance.
- Medium for cleanup, age, and trend findings without current impact.
