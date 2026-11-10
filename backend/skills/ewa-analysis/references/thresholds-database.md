# Database Thresholds

Use this reference for EWA sections about non-HANA database time, cache hit
ratios, growth, tablespaces, and logging (Oracle, SQL Server, DB2, MaxDB, ASE).
HANA: use `thresholds-hana`. SQL statements: use `thresholds-sql`.

| Metric | Healthy | Warning | Critical | Transactions | Notes |
| --- | --- | --- | --- | --- | --- |
| DB request time per dialog step | < 200ms | 200-400ms | > 400ms | ST03N, ST04 | User response often follows DB latency |
| Data buffer cache hit ratio | > 98% | 95-98% | < 95% | ST04, DBACOCKPIT | Low ratio means reads go to disk |
| Log buffer wait ratio | < 1% | 1-5% | > 5% | ST04 | Writes wait for log buffer |
| Database growth rate | < 5% per month | 5-10% per month | > 10% per month | DB02 | Unchecked growth creates space risk |
| Tablespace utilization | < 75% | 75-90% | > 90% | DB02 | Prefer the report's own threshold; above 90% may become urgent |

Severity guidance:

- Critical when DB bottlenecks are causing broad current transaction delays or
  imminent space exhaustion.
- High when DB request time and cache evidence align.
- Medium for growth or tablespace trends without current impact.
