---
name: create
description: "Build a new site, application, API or tool from an accepted brief through implementation, with verification only when requested. Use /create for a new project rather than maintenance."
version: 2.8.3
---

# /create

Read `KIT/skills/app-builder/SKILL.md`, its project-detection guidance and only the template matching the actual project. A template is a starting point; preserve the requested stack and delivery format.

## Establish the brief

Use what the user already supplied: audience, primary task, required behavior and practical constraints. Resolve consequential gaps; choose routine details within scope. For new visual design, decide the direction unless it is genuinely unclear (see frontend-design).

Choose planning depth to fit the work. A bounded build can use a short task list. Use `plan-writing` for durable coordination or `proplan` when a system document set is requested or genuinely useful; do not block a build on accepting an extra planning command.

## Deliver

Establish shared contracts and the costly-to-reverse boundaries first. For UI, use frontend-design/mobile-design and record the approved direction with design-spec when helpful. Implement complete useful flows, including relevant empty, loading, error and recovery behavior. Delegate independent lanes with `parallel-agents` when available; otherwise perform the roles directly.

Deliver the implementation without an automatic audit or checking phase. Use `verify-changes` or browser verification only when requested (kit-core). Start a preview when the user asks to see/run the result; report its URL only after it is ready.

Finish with what was built, where to run/view it, material assumptions, evidence and remaining limits. Do not claim integrations or deployment that were not exercised.
