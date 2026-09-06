---
name: see
description: "/see — Opens the running app in the browser and reports what actually rendered: screenshot, real DOM, computed styles against DESIGN.md tokens, console and network errors, one interaction pass, and the breakpoint matrix. Use to verify UI before calling it done, or when a page looks wrong."
version: 1.0.0
---

# /see

**Input:** the text after `/see` is the route or URL to check (`/see /dashboard`). If it is empty, check the route affected by the most recent change; if that is unclear, ask for the route in one line.
**Agent:** read `C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/agents/frontend-specialist.md`.
**Skills:** `@[skills/browser-verification]` (the protocol, what to look for, report format); `@[skills/design-spec]` when the token scale needs interpreting.

## Steps

1. **Attach.** Reuse the dev server already running; start one only if nothing is up, and wait for the ready line. Never start a second server — a stale port serves an old build.
2. **Render.** Open the route and screenshot it. Describe what you actually see, not what you expect.
2b. **Critique** (your own UI only). Apply `frontend-design` §4.0 as questions against the screenshot; fix and re-render before reporting.
3. **Inspect.** Read the rendered DOM for the region that changed, and the **computed** styles — color, spacing, type, radius — comparing each against the `DESIGN.md` token scale.
4. **Listen.** Capture console errors/warnings and failed network requests.
5. **Interact.** Click the primary action once; submit the form with valid then invalid input and confirm the error state renders.
6. **Widths.** Re-render at ~390px, ~768px, and ~1440px; check overflow, clipping, readability, and touch targets.
7. **Report** using the Visual Verification Report format in `browser-verification`, splitting required failures from advisory findings.

## Output

The Visual Verification Report, in the format defined once in `browser-verification` (target, rendered, token conformance, console/network, interaction, findings split required/advisory, not verified). Do not invent a second format.

## Rules

- When the user invoked `/see` on existing UI: report what rendered, do not fix in the same turn unless asked — findings first, then act. When you are verifying UI you built in this task: critique and refine it first (`browser-verification` §2b), then report; do not escalate your own draft.
- A screenshot alone is not verification: the DOM, computed styles, console, network, interaction, and widths are all part of the pass.
- Required failures (route does not render, uncaught console error, failed data request, broken interaction) block "done" per the UI-render gate in `code-rules`.
- If the gate cannot run (no dev server, no browser), say so in one line and name the reason — never skip silently.

## Verification

- The report names the exact URL checked and all three widths.
- Every token violation lists the computed value and the expected scale value.
- Console and network are reported explicitly, including "none".
- Required and advisory findings are separated.
