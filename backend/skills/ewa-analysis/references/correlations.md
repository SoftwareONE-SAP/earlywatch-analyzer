# Cross-Domain Correlation Patterns

Use this reference when correlating findings across sections or when a section
mentions symptoms that likely connect to another domain.

## Memory Pressure Chain

Extended memory near capacity plus heavy heap usage plus user context swapping
usually points to insufficient extended memory allocation or memory-heavy custom
workloads. Fix the root cause through `em/initial_size_MB`, related memory
parameters, and custom program review.

## Database Bottleneck Cascade

High DB request time plus low cache hit ratio plus expensive SQL usually points
to DB buffer undersizing, bad SQL, missing indexes, or both. Validate in `ST04`,
`DBACOCKPIT`, `ST05`, and SQL Monitor.

## Hardware Sizing Crisis

CPU above 85%, swap above 20%, and dialog response above 2 seconds together
indicate the system has outgrown available resources. Consider workload
redistribution, operation modes, or infrastructure scaling.

## Batch Versus Dialog Contention

Background work process saturation plus dialog slowdowns during batch windows
indicates job scheduling or capacity conflict. Reschedule jobs, adjust operation
modes, or add batch capacity.

## Security Compound Risk

Old kernel, broad privileged users, and weak RFC security together indicate
neglected security maintenance. Treat as higher priority than isolated patch
currency findings.

## Growth Trajectory Warning

Database growth above 10% per month plus tablespaces above 80% plus no archiving
indicates a data lifecycle gap. Address with storage extension and archiving
strategy.
