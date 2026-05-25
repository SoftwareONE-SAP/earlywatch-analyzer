# Database Thresholds

Use this reference for EWA sections about DB time, cache hit ratios, expensive
SQL, growth, tablespaces, logging, and HANA/Oracle/SQL Server health.

| Metric | Healthy | Warning | Critical | Transactions | Notes |
| --- | --- | --- | --- | --- | --- |
| DB request time per dialog step | < 200ms | 200-400ms | > 400ms | ST03N, ST04 | User response often follows DB latency |
| Data buffer cache hit ratio | > 98% | 95-98% | < 95% | ST04, DBACOCKPIT | Low ratio means reads go to disk |
| Log buffer wait ratio | < 1% | 1-5% | > 5% | ST04 | Writes wait for log buffer |
| Top SQL elapsed share | No dominant SQL | > 20% one SQL | > 40% one SQL | ST05, SQLM | May indicate missing index or bad custom code |
| Database growth rate | < 5% per month | 5-10% per month | > 10% per month | DB02 | Unchecked growth creates space risk |
| Tablespace utilization | < 75% | 75-90% | > 90% | DB02 | Above 90% may become urgent |
| HANA column store memory | < 80% | 80-90% | > 90% | DBACOCKPIT | Memory pressure affects DB performance |
| HANA savepoint duration | < 30s | 30-120s | > 120s | HANA Studio, DBACOCKPIT | Long savepoints can signal I/O bottlenecks |

Severity guidance:

- Critical when DB bottlenecks are causing broad current transaction delays or
  imminent space exhaustion.
- High when DB request time and cache/SQL evidence align.
- Medium for growth, tablespace, or dominant SQL trends without current impact.
