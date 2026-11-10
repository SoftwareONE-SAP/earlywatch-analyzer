# Cross-Domain Correlation Patterns

Use this reference when correlating findings across sections or when a section
mentions symptoms that likely connect to another domain.

## Memory Pressure Chain

Extended memory near capacity plus heavy heap usage plus user context swapping
may point to insufficient extended memory allocation or memory-heavy custom
workloads. Validate these possible causes (memory settings for the kernel
release, custom program review) before changing anything.

## Database Bottleneck Cascade

High DB request time plus low cache hit ratio plus expensive SQL may point
to DB buffer undersizing, bad SQL, missing indexes, or a mix. Validate in `ST04`,
`DBACOCKPIT`, `ST05`, and SQL Monitor.

## Hardware Sizing Crisis

CPU above 85%, swap above 20%, and dialog response above 2 seconds together
may indicate resources are insufficient for the current workload, or that a
workload or configuration issue is consuming them. Validate before concluding;
options include workload redistribution, operation modes, or scaling.

## Batch Versus Dialog Contention

Background work process saturation plus dialog slowdowns during batch windows
indicates job scheduling or capacity conflict. Reschedule jobs, adjust operation
modes, or add batch capacity.

## Security Compound Risk

Old kernel, broad privileged users, and weak RFC security together may point
to neglected security maintenance. Validate this pattern against the report
evidence before concluding. If confirmed, treat it as higher priority than
isolated patch currency findings.

## Growth Trajectory Warning

Database growth above 10% per month plus tablespaces above the report's threshold plus no archiving
indicates a data lifecycle gap. Address with storage extension and archiving
strategy.
