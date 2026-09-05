---
name: memory-system
description: Per-project persistent memory in <project>/.agents/memory/MEMORY.md — what belongs there (decisions, conventions, gotchas), the index format, optional topic files, and how to recall without reciting. Use when the user says remember, save this, or don't forget, for /remember, and at session start when the file exists.
version: 2.0.0
---

# Memory System

> Persist the decisions, conventions, and gotchas of a project so they are never re-discovered.

## Location and lifecycle

Memory is per project, at the Antigravity workspace root: `<project>/.agents/memory/MEMORY.md`. This is the one place the kit uses an `.agents/` path — by design.

The directory does not exist until first use. `/remember` (or the first save) creates `.agents/memory/` and `MEMORY.md`; nothing else does. This needs a **writable project root** — on a read-only checkout or where the root is not writable, say so and skip the save; never fail the task over it.

Session start: if the file exists, read it once and apply what you learn silently (use bun in commands, keep answers short); if not, do nothing (the `core-protocol` rule). Recite entries only when the user asks what you remember.

## Layout

```
.agents/memory/
├── MEMORY.md                index (required, max 200 lines)
├── project-conventions.md   optional topic file
└── <topic>.md               optional; only when an entry needs detail
```

Small projects keep everything in `MEMORY.md`. Create a topic file only when a note needs more than one line; the index entry then points at it.

## Index format

- One entry per line, at most 150 characters: `- [type] summary → topic-file.md` (the pointer is optional).
- Types: `[user]` `[feedback]` `[project]` `[reference]`.
- Replace an entry when the fact changes; never append a contradiction.

```markdown
# Memory Index

## User
- [user] Windows 11, PowerShell, prefers concise answers with tables

## Project
- [project] Use bun instead of npm for all scripts
- [project] Migrations must run before seed or the FK constraint fails → project-conventions.md

## Feedback
- [feedback] Dislikes long explanations before the code

## Reference
- [reference] Staging API base URL is https://staging.example.com/api
```

Topic files start with frontmatter (`type`, `created`, `updated`) followed by short headed sections.

## What belongs — and what does not

| Type | Save | Example |
|---|---|---|
| user | Role, tools, communication style | "Senior DevOps, prefers dark mode" |
| feedback | What the user liked or disliked about output | "Too verbose; prefers tables" |
| project | Conventions, stack decisions, and gotchas | "bun, not npm; Prisma over Drizzle; seed fails unless migrated first" |
| reference | Non-secret infrastructure notes, public URLs | "Prod API hostname and port" |

| Never save | Why |
|---|---|
| Secrets, tokens, passwords, keys | Persistent and possibly shared |
| Facts derivable from code (`package.json`, lockfiles) | Read the source instead |
| Temporary debug context | Clutter |
| Code snippets | Go stale |
| Whole conversations | Memory holds distilled insights, not transcripts |

## Operations

- **Save** (`/remember`, "remember", "don't forget"): classify → distill to one line → create the directory and index if missing → add or replace the entry → confirm what was saved.
- **Recall** (session start, "what do you remember about X"): read the index; open a topic file only when its entry matches the task.
- **Search** ("do I have notes on X"): search `.agents/memory/*.md` and return matching entries with file names.
- **Prune** (index over 200 lines): warn, propose merges or an `archive/` folder; never delete without asking.

## Memory vs. plan vs. task

| Artifact | Holds | Lives |
|---|---|---|
| Memory | What you know across sessions | `.agents/memory/` |
| Plan | What you will do for this task | `docs/plans/{task-slug}.md` |
| Task | What you are doing now | Antigravity task list and Artifacts |
