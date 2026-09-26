---
name: see
description: "/see - Opens the running app in the browser and reports what actually rendered: screenshot, DOM, computed styles against DESIGN.md tokens, console and network errors, one interaction, and mobile and desktop widths. Use when asked, when a page looks wrong, or at code-rules tier 1+ for a layout change while a dev server is running."
version: 2.5.0
---

# /see

A tool for looking at a real render. Use it when the user asks, when a page looks wrong, or when `code-rules` calls for it (a layout change at tier 1 or above while a dev server is running). Skip it for non-visual changes, trivial style values, or when there is no dev server or browser, and say so in the report.

**Input:** the text after `/see` is the route or URL (`/see /dashboard`). If empty, check the route affected by the most recent change; if that is unclear, ask for the route in one line.
**Agent:** work as `KIT/agents/frontend-specialist.md`.
**Skills:** `KIT/skills/browser-verification/SKILL.md` (method, what to look for, report format); `KIT/skills/design-spec/SKILL.md` when the token scale needs interpreting.

## Steps

1. **Attach.** Reuse the dev server already running; start one only if nothing is up, and wait for the ready line. Do not start a second server: a stale port serves an old build.
2. **Render.** Open the route and screenshot it. Describe what you see, not what you expect.
3. **Critique and refine** (your own UI in this task). Ask the `frontend-design` §4.0 questions against the screenshot: does the right thing win the eye, are type and spacing on the scale, does it match the chosen direction and references? Fix what fails and render again before reporting. Two passes is normal.
4. **Inspect.** Read the DOM for the region that changed and the computed colour, spacing, type and radius; compare with the `DESIGN.md` scale.
5. **Listen.** Console errors and warnings, failed network requests.
6. **Interact.** Click the primary action once. For a form, submit valid then invalid input and confirm the error state.
7. **Widths.** ~390 and ~1440 by default; add ~768 when the layout has a tablet breakpoint or the bug lives there. Check overflow, clipping, readability, touch targets.
8. **Report** in the format in `browser-verification`, findings split into must-fix and polish.

Optional evidence: save `after-<width>.png` (and `before-<width>.png` on a repair) plus `verdict.json` in `.agents/verify/<task-slug>/`, then `python "KIT/scripts/ui_verify.py" .agents/verify/<task-slug> --widths 390,1440` checks that each claimed width was really rendered. Use it for tier 2-3 work, client handoff, or when the user asks for proof.

## Rules

- When the user runs `/see` on existing UI: report first; fix only if asked or if the fix is obviously part of the current task.
- A screenshot is one part of the pass; DOM, computed styles, console and one interaction catch what it cannot.
- Must-fix findings: the route does not render, an uncaught console error, a failed data request on this route, a broken primary interaction, unreadable text. At tier 2-3 these block "done".
- Never report a width, interaction or check you did not actually run. If the browser is unavailable, say which precondition failed (`browser-verification/troubleshooting.md`).
