---
name: doctor
description: "/doctor - Read-only diagnosis of AGKIT2 source validation, installed version/sync, active rules, entrypoint and available local tools. Use for kit loading problems or after an install; it does not repair files or test a project UI."
version: 2.8.2
---

# Kit Health

Run `python -B "KIT/scripts/kit_doctor.py" --json` for a read-only report. Use `--source "<editable source>"` when the source is in a nondefault location and `--config-root "<test config>"` for isolated installations. Read `--help` for the current options.

The report checks structural source validity, expected installed files, managed rules, the global kit entrypoint and source/installation agreement. It notes local Python, Node, Git and PowerShell availability without printing secret values or installing tools. A missing tool matters only to work that needs it.

Interpret findings by cause: source invalidity needs a source repair; drift needs deliberate sync/install after preserving work; a missing entrypoint/rule needs installation repair; an already-loaded chat needs restart/new chat. Do not delete unrelated rules just because their names resemble a kit rule. The helper reports evidence and never applies a repair.

After a requested repair, run the appropriate source checks, use the backed-up installer, then rerun the doctor against the actual active configuration. For a healthy report, say that the kit's installation checks passed; it does not establish a generated app's appearance, security or runtime correctness.
