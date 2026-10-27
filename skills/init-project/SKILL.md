---
name: init-project
description: "/init-project - Scan the current repository and create or update AGENTS.md with the project's facts (stack, commands, folders, data ownership, integrations, design system) so every new chat starts with the right context."
version: 3.2.0
---

# /init-project

Write the project's facts into `AGENTS.md` at the repo root. Antigravity loads it in every chat for this workspace, so later chats skip re-discovery.

## Steps

1. Read `package.json` / `composer.json` / `pubspec.yaml`, lockfiles, framework config, `.env.example`, `README.md`, `routes/`, `app/` or `src/`, `database/migrations` or `prisma/schema.prisma`, `DESIGN.md`, `docs/plans/`.
2. Copy `KIT/skills/init-project/AGENTS.template.md` to `AGENTS.md` (or update the existing file, keeping user-written lines).
3. Fill every section from what you actually found. Write `unknown - ask` for anything not in the repo (e.g. ERP base URL).
4. Keep it under 6,000 characters: facts and commands only, no policy (policy lives in the kit rules).
5. Show the user the filled sections that say `unknown - ask` as questions in one message.

## Before you finish, check

- [ ] Commands (dev, build, test, migrate) are copied from the real scripts.
- [ ] Data ownership lists which tables this system owns vs copies from the ERP.
- [ ] No secrets; env vars listed by name only.
