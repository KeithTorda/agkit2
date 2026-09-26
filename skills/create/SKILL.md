---
name: create
description: "/create - Builds a new application end to end: up to 3 questions with defaults, a /proplan --lite offer for anything beyond a small site, DESIGN.md, template-based build, verification by risk tier, and a running dev server. Use when the user asks for a new app, site, API or project from scratch."
version: 2.5.0
---

# /create

**Input:** the text after `/create` describes the app (or names a `/plan` or `/proplan` slug to build from).
**Read now:** `KIT/skills/app-builder/SKILL.md`, then `app-builder/project-detection.md` and only the matching `templates/<name>/TEMPLATE.md`.
**Read when:** UI project → `KIT/skills/design-spec/SKILL.md`; several specialists → `KIT/skills/parallel-agents/SKILL.md`; questions needed → `KIT/skills/brainstorming/SKILL.md`.

## Steps

1. **Questions (only if blocked).** One message, at most 3, each with a recommended default: usually who uses it, the must-have features, and anything that fixes the stack (existing hosting, Laravel shop, offline need). If the request already answers them, or the user says "proceed", go with the defaults and list them as assumptions.
2. **Size it.**
   - Small site or single-purpose tool (landing page, portfolio, brochure site, a one-screen utility): write the stack and a short task list in the reply, or `docs/plans/<slug>.md` if it spans sessions (`plan-writing`).
   - Anything bigger (accounts and roles, a database with several entities, payments, admin panel, a client system): offer `/proplan --lite <idea>` first (`KIT/skills/proplan/SKILL.md`) - five docs that settle goals, data model and milestones before code. If the user declines, write a `/plan` file and continue.
   - A `/proplan` already exists: build milestone by milestone with `/orchestrate docs/proplan/<slug> M1`.
3. **DESIGN.md (UI projects).** Before any UI code, `frontend-specialist` (web) or `mobile-developer` (mobile-only) writes `DESIGN.md` at the project root with `design-spec`: the audience, style direction from the brief, tokens. The client's taste wins; `anti-template` is a list of defaults to question. Skip for API-only and CLI projects.
4. **Build.** Scaffold from the template with current stable versions, then change the expensive-to-reverse things first: data model and IDs, auth, the data-fetching boundary. Order and owners: `app-builder/agent-coordination.md`. Delegate independent parts with `invoke_subagent`; do small builds yourself.
5. **Verify by tier** (`code-rules`). A static site is tier 1: build succeeds, the project's lint and types pass, a look at 390 px and 1440 px when a browser is available. Auth, payments, permissions or data deletion make it tier 2: `python "KIT/scripts/checklist.py" . --full`, tests for that logic, `/review` on it.
6. **Run.** Start the dev server with the template's command; confirm the home route responds; report the URL and how to stop it.

## Output

```markdown
<App> is running at http://localhost:<port> (stop: Ctrl+C in its terminal)
Template: <name> · Stack: <one line> · Plan: <path or "in reply">
Files: <grouped by area or owner>
Checks: <commands> → <outcome>
Assumptions: <defaults taken>
Not verified: <what did not run>
Next: /enhance <feature>, /test, /deploy preview
```
