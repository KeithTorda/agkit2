---
name: create
description: "/create - Build a new site, app, API or tool from the user's brief through working code. Use it for a new project; use /enhance for changes to an existing one."
version: 3.2.0
---

# /create

Turn a brief into a new, working project in the requested stack.

## Steps

1. Read `KIT/skills/app-builder/SKILL.md` and only the template that matches the requested stack. Treat the template as a starting point; the user's stack and delivery format win.
2. Collect the brief from what the user already gave: audience, main task, required behavior, constraints. Ask once only about gaps that change scope, data, money or permissions (rule-02-work-style). Decide routine details yourself and state them in one line.
3. Pick planning depth: a short task list for a bounded build, `KIT/skills/plan-writing/SKILL.md` for multi-session work, or `/proplan` for a whole system. Start building once the plan exists; no separate approval round is needed.
4. If the project is a new system or an add-on, set up separate DB, outbox and versioned API first (per rule-04-system-integration).
5. Build the costly-to-change parts first: data model, auth, shared contracts, theme tokens.
6. For UI, use `KIT/skills/frontend-design/SKILL.md` (web) or `KIT/skills/mobile-design/SKILL.md` (Expo). Record the chosen direction in DESIGN.md with `KIT/skills/design-spec/SKILL.md`. Design follows rule-01-unified-theme-system and rule-07-template-grade-design.
7. Implement complete flows, including loading, empty, error and success states (rule-03-code-standards).
8. Split independent lanes with `KIT/skills/parallel-agents/SKILL.md` when delegation is available; otherwise do the roles in order yourself.
9. Start a dev server or preview only when the user asks to run or see it. Give the URL once it responds.

## Stack notes

- Next.js/React: App Router conventions of the installed version; server code for totals and permissions.
- Laravel/Blade: Form Requests, policies, migrations, Blade components.
- Bootstrap 5.3 or Tailwind: map tokens once, then use them everywhere.
- Expo: tokens and three-mode theme from rule-01; native controls.
- VPS: note Nginx/PM2 setup in the README for later `/deploy`.

## Output

Report in the rule-02 shape: what was built, how to run it, decisions, and what was not run (tests, builds, browser checks run only on request per kit-core).

## Before you finish, check

- [ ] Every requested flow works end to end in code, not as a proposal.
- [ ] README lists setup, env variable names and run commands.
- [ ] Demo data lives in one `demo-data.*` file.
- [ ] The report says plainly which checks were not run.
