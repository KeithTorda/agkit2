---
name: fix-ui
description: "Repair an existing visual or interaction defect from observed layout/state evidence. Use /fix-ui for clipping, overlap, placement, responsiveness or similar UI failures."
version: 2.8.2
---

# /fix-ui

Use `KIT/agents/frontend-specialist.md` and `KIT/skills/ui-repair/SKILL.md`. Identify the route, state, device/width and reported defect from available context. Read the relevant component guidance only for the affected structure.

Observe the actual render when possible; otherwise distinguish source-based diagnosis from visual evidence. Inspect the element and its ancestors: layout mode, size constraints, overflow, positioning, stacking and breakpoint behavior. Consider data/state defects as well as CSS. Name the cause before accumulating fixes.

Correct the owning constraint or state transition. A narrow documented override is acceptable when upstream code cannot be configured, but do not mask an unexplained parent defect with repeated offsets or !important. Clean up rules and wrappers made obsolete by the correction.

Recheck the reported state and relevant neighboring widths/states with `browser-verification`; exercise the affected interaction. Preserve the approved direction. A repair does not need new style intake unless the user also requests a new design.

Report what was wrong, its source, the changed constraint and the actual evidence. If runtime/browser access is unavailable, state the visual limit and continue applicable source or automated checks. Before/after screenshots and ui_verify are useful evidence when the task warrants them, not proof by file existence alone.
