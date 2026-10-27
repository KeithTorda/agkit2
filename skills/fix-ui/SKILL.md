---
name: fix-ui
description: "/fix-ui - Repair a visible layout or interaction defect such as clipping, overlap, misplacement, broken responsiveness or a stuck state. Use it for an existing screen, not for a new design."
version: 3.2.0
---

# /fix-ui

Correct one UI defect at the rule that owns it while keeping the approved design. Work as `KIT/agents/frontend-engineer.md` with the method in `KIT/skills/ui-repair/SKILL.md`.

## Steps

1. Identify the route, component, UI state (open menu, error, empty) and screen width where the defect appears.
2. Open the component and its parent layout files. Read the styles that apply to the broken element.
3. Walk from the element up through its ancestors. For each, note display mode, width/height limits, overflow, position, z-index and breakpoint classes.
4. Check whether the defect comes from data or state (long label, missing value, wrong flag) rather than CSS.
5. State the cause in one sentence before editing.
6. Change the owning constraint: the token, utility class, grid/flex rule or state logic. Remove wrappers and rules the fix makes unnecessary.
7. Confirm the fix still works in Light and Dark per rule-01-unified-theme-system, and at narrow and wide widths, by reading the code.
8. Run a rendered re-check only when the user asks; then use `KIT/skills/browser-verification/SKILL.md` on the reported state and neighboring widths.

## Stack notes

- Bootstrap 5.3: prefer utility classes and CSS variables (`--bs-*`) over custom overrides.
- Tailwind: fix the class list or the theme config; keep responsive prefixes consistent.
- Blade: check included partials and stacks for duplicated wrappers.
- Third-party widgets: a narrow override with a one-line reason comment is fine when the library cannot be configured.

Avoid stacking offsets, negative margins or `!important` to hide a parent problem.

## Output

Report what was wrong, the file and rule that caused it, what changed, and whether the result was seen in a browser or only reviewed in code.

## Before you finish, check

- [ ] The cause was named before the edit.
- [ ] The fix lives in the owning rule or state, not a patch on top.
- [ ] Obsolete CSS and wrappers are removed.
- [ ] The report says plainly if no browser check was run.
