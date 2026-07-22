# Software Lifecycle Assessment

Use this reference for SAP application maintenance phases, support packages,
kernel, database revision, operating system, SQL client/SQLDBC, add-on, and
important SAP Note sections.

## Assessment Rules

- Capture product/component, installed release and patch, report date, stated
  maintenance status or deadline, target level if explicitly given, and the
  report's cited SAP Note or source.
- Distinguish out of maintenance, out of date, and affected by a specific known
  issue. They have different urgency.
- Assess exposure using system role, internet/external reachability, regulatory
  needs, known defect impact stated in the report, and available compensating
  controls.
- Do not invent the latest level, deadline, compatibility, CVE applicability, or
  SAP Note. These facts are time- and release-specific.
- Treat an EWA important-note list as candidates for applicability validation,
  not automatic implementation instructions.

## Severity Guidance

- Critical requires an active exploitable or availability-threatening condition,
  not age alone.
- High: ended maintenance with material production exposure, or a report-stated
  urgent correction applicable to the installed stack.
- Medium: aging but supported software, upcoming deadline, or validation/planning
  gap without current impact.
