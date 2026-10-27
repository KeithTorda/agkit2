---
name: see
description: "/see - Open the real rendered web page and inspect it against the intended design and behavior. Use it when the user wants a visual check or UI review."
version: 3.2.0
---

# /see

Look at the actual render, exercise the changed interaction and report only what was observed. Invoking /see is the user's request, so run the browser checks. Follow `KIT/skills/browser-verification/SKILL.md`.

## Steps

1. Pick the target: the route or URL given after the command, or the screen changed in the current task.
2. Reuse a running dev server, or start the project's documented one (`npm run dev`, `php artisan serve`). Confirm it serves the current code.
3. Choose widths from the project's breakpoints. New responsive screens: one mobile and one desktop width. Reported bugs: add the reported width.
4. Render each relevant state: default, loading, empty, error, open menus and dialogs.
5. Inspect hierarchy, text wrapping, spacing, contrast, overflow, focus rings and image cropping. Check Light and Dark.
6. Read the browser console and failed network requests that affect the flow.
7. Click through the main changed interaction, including one invalid input and its recovery.
8. Compare against the agreed brief and rule-07-template-grade-design, not a generic checklist.
9. If this is your own implementation task, fix observed defects and render again. If it is review-only, report findings without editing.

## Output

- Target, states and widths actually inspected.
- Observed problems, ordered by impact, with the fix or suggestion.
- Areas not inspected and why.

Screenshots or `KIT/scripts/ui_verify.py` output support a claim; a saved image alone does not prove inspection. If the browser cannot run, say what blocked it and list what stays unverified.

## Before you finish, check

- [ ] Every width, click and console result in the report was really observed.
- [ ] Both Light and Dark were looked at.
- [ ] Review-only runs left files unchanged.
- [ ] Unverified areas are listed.
