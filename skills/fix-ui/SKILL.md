---
name: fix-ui
description: "/fix-ui - Diagnoses and fixes existing web UI that renders wrong (misplaced, overlapping, clipped, collapsed, unresponsive): locates the parent's layout mode and computed box model, names the root cause, fixes the container at the source, and checks the result in proportion to risk. Use when a page or component that exists looks broken."
version: 2.5.0
---

# /fix-ui

**Input:** the text after `/fix-ui` is the route plus the defect in the user's words (`/fix-ui /dashboard the sidebar renders under the header`). If either is missing and you cannot infer it from the recent conversation, ask for both in one line.
**Agent:** work as `KIT/agents/frontend-specialist.md`.
**Skills:** `KIT/skills/ui-repair/SKILL.md` (the protocol, the eight root causes, `components.md`); `KIT/skills/browser-verification/SKILL.md` when a dev server is running; `KIT/skills/css-architecture/SKILL.md` when CSS files change.

## Steps

1. **Observe.** With a dev server running, open the route at the reported width (`/see`) and screenshot it. Otherwise use the user's screenshot or description and read the code. State the defect in one sentence of observation.
2. **Locate.** Find the misplaced element and its parent; read computed layout values for the element and its ancestors (`ui-repair` §2), or the same chain in source when there is no browser.
3. **Name the cause.** Pick one of the eight root causes (`ui-repair` §3), or name the other cause you found, before editing. For a shell, sidebar, header, modal, dropdown, table, form or toast, read `components.md` first.
4. **Fix at the source.** Change the container's constraint or the token in the file that owns it (`ui-repair` §4). An override only when the source is outside your control, narrow and commented.
5. **Clean up.** Delete the rule, variant or wrapper your fix replaced. For a colour defect, `python "KIT/scripts/css_audit.py" .` often names the line (a token defined twice, a `var()` nothing defines).
6. **Check.** Per the `code-rules` tier. With a dev server running: look at the broken width plus one other (~390 and ~1440; add ~768 for breakpoint bugs) and click the region's primary action once. Before/after screenshots in `.agents/verify/<task-slug>/` are useful evidence on a repair; `python "KIT/scripts/ui_verify.py" .agents/verify/<task-slug> --require-before` checks them if you saved them. No server: say so under `Not verified`.

## Output

```markdown
Fixed: <defect> at <width>. Cause: <number + name> in <file:line of the container>.
- Changed: <file:line → the new constraint>
- Deleted: <rule / variant / wrapper, or none>
- Checked: <widths looked at and what you saw, or commands run>
- Not verified: <what you did not see, or none>
```

## Rules

- Name the cause before editing. It is what keeps the fix to one change instead of a pile of tweaks.
- If the fix does not hold at a second width, the cause was probably wrong: go back to step 3.
- If the cause is in a shared shell or layout file, fix it there and say so: every route that uses it had the bug.
- Overrides (`!important`, inline style, a wrapper added only to win, a margin hack on the child) are a last resort with a one-line comment naming why, not the first move.
