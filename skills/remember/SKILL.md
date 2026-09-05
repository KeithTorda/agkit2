---
name: remember
description: "/remember — Saves a preference, convention, decision, or reference note to the project's memory at .agents/memory/MEMORY.md so later sessions reuse it. Use when the user says remember, save this, or don't forget, and after a decision worth keeping."
version: 2.0.0
---

# /remember

**Input:** the text after `/remember` is what to save. If empty, ask what to remember in one line.
**Agent:** none; no specialist persona is needed.
**Skills:** `@[skills/memory-system]` (index format, taxonomy, what not to save).

## Steps

1. Classify the note: `user`, `feedback`, `project`, or `reference` (taxonomy in `memory-system`).
2. Distill it to one line of at most 150 characters, keeping the user's exact terms for names and versions. Refuse secrets, tokens, credentials, and anything derivable from code (`package.json`, lockfiles).
3. If `<project>/.agents/memory/MEMORY.md` does not exist, create the `<project>/.agents/memory/` directory (if missing) and the file with the index skeleton from `memory-system`. Otherwise read it first.
4. Add the entry under the matching section, or replace an existing entry on the same subject instead of appending a contradiction.
5. When the note needs more than one line, put the detail in a topic file (`.agents/memory/<topic>.md`) and point the index entry at it.
6. If the index exceeds 200 lines, say so and propose merges; never delete entries without asking.
7. Confirm what was saved and where.

## Output

```
Saved to memory
Type: project
File: .agents/memory/MEMORY.md (→ project-conventions.md when a topic file was used)
Entry: [project] Use bun instead of npm for all scripts
```

## Verification

- The entry is present in `MEMORY.md`, under 150 characters, with no secrets.
- The index is still under 200 lines, or the user was warned.
