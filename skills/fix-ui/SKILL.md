---
name: fix-ui
description: "/fix-ui — Diagnoses and fixes existing web UI that renders wrong (misplaced, overlapping, clipped, collapsed, or unresponsive layout): sees it in the browser, locates the parent's layout mode and computed box model, names one of eight root causes, fixes the container at the source, and re-verifies at three widths. Never an override."
version: 1.0.0
---

# /fix-ui

**Input:** the text after `/fix-ui` is the route plus the defect in the user's words (`/fix-ui /dashboard the sidebar renders under the header`). If it is empty, ask for both in one line.
**Agent:** read `C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/agents/frontend-specialist.md`.
**Skills:** `@[skills/ui-repair]` (the protocol, the eight root causes, the exemplar, `components.md`); `@[skills/browser-verification]` (render and inspect mechanics); `@[skills/css-architecture]` when CSS files change.

## Steps

1. **See before.** Open the route at the reported width (`/see`), screenshot it, and state the defect in one sentence of observation.
2. **Locate.** Find the misplaced element and its parent in the rendered DOM; dump computed layout values for the element and its ancestors (`ui-repair` §2).
3. **Name the cause.** Pick one of the eight root causes (`ui-repair` §3) and write it down before editing anything. Shell, sidebar, header, modal, dropdown, table, form, or toast: read `components.md` first.
4. **Fix at the source.** Change the container's constraint or the token in the file that owns it (`ui-repair` §4).
5. **Delete dead CSS.** Remove the rule, variant, or wrapper your fix replaced, then run `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/css_audit.py .` — a colour defect is usually a token defined twice or a `var()` nothing defines, and it must be clean before you re-render.
6. **See after.** Re-render at ~390, ~768, and ~1440 (`/see`); confirm the interaction still works. `before-<width>.png` and `after-<width>.png` land in `.agents/verify/<task-slug>/` alongside `verdict.json`; then `ui_verify.py .agents/verify/<task-slug> --require-before` must exit 0 — on a repair the before shot is the only proof the defect existed.

## Output

```markdown
## UI Repair Report
- Defect: <one sentence, as observed, at <width>>
- Root cause: <number + name> — in <file:line of the container>
- What changed: <file:line → the new constraint>
- What was deleted: <rule / variant / wrapper, or none>
- Before / after: 390 <…> · 768 <…> · 1440 <…>
- Not verified: <escape-hatch reason, or none>
```

## Rules

- Name the root cause before editing. No cause named, no edit.
- One fix, not a pile of tweaks. If it does not hold at all three widths, the cause was wrong: go back to step 3.
- No override of any kind (`code-rules` "Fix at the source"): no `!important`, inline style, wrapper div, more specific selector, or margin/`absolute` hack on the child.
- If the cause is in a shared shell or layout file, say so and fix it there: every route has the bug.
- If the render gate cannot run, say so in one line and name the reason; never skip silently.

## Verification

- The report names the route, the width the defect reproduced at, and all three widths after.
- The root cause is one of the eight, by number, with the container's file:line.
- The diff contains no override pattern and no leftover rule.
- Before and after screenshots exist for all three widths.
