---
name: debug
description: "Diagnose and repair errors, regressions or incorrect behavior with discriminating evidence. Use /debug when a cause is uncertain or a direct fix needs confirmation."
version: 2.8.2
---

# /debug

Use `KIT/agents/debugger.md` and `KIT/skills/systematic-debugging/SKILL.md`. The text after the command supplies the symptom; infer missing context from the current task before asking for it.

Establish expected versus observed behavior, triggering input and environment. Reproduce when practical, then trace to the first incorrect value or decision. Test hypotheses with checks that distinguish them. Fix an obvious localized cause directly; do not turn a typo into a required investigation ceremony.

When experiments fail, remove ineffective changes and reassess from new evidence. Use `problem-solving` for competing hypotheses or repeated failure. A tool/service unavailable in the environment is a limitation to diagnose, not proof of an application bug.

Verify the corrected case and a relevant neighboring success/failure path. Add a regression test when it protects meaningful behavior, following `testing-patterns`. Report the cause with source references, the change, execution evidence and what remains uncertain. Save a durable lesson only under requested or otherwise authorized project memory work.
