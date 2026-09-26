---
name: debug
description: "/debug - Investigates a bug systematically: reproduce, isolate, find the root cause, fix, verify, add a regression test. Use when something errors, crashes, misbehaves or a test fails and the cause is not obvious."
version: 2.5.0
---

# /debug

**Input:** the text after `/debug` is the symptom (error text, failing test, or behaviour).
**Agent:** `KIT/agents/debugger.md`.
**Read now:** `KIT/skills/systematic-debugging/SKILL.md` (the four phases). Regression test: `KIT/skills/testing-patterns/SKILL.md` when needed.

Run the four phases in order; do not jump to a fix. For an obvious cause (a typo in the stack trace line), fix it directly and say so.

## Output

```markdown
## Debug: <issue>
Symptom: <what happens> · Reproduced with: `<command>` → <output>
Root cause: <why, file:line>
Fix: <what changed and why>
Verified: `<command>` → <result> · Regression test: <path or "not added: reason">
Also checked: <same mistake elsewhere, or none found>
```

No random edits: every change follows a confirmed hypothesis. If the cause is outside the reported area, say so.
