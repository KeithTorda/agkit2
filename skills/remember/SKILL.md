---
name: remember
description: "/remember - Saves a preference, convention, decision, reference note or failed approach to the project's memory at .agents/memory/MEMORY.md so later sessions reuse it. Use when the user says remember, save this or don't forget, and after a decision or dead end worth keeping."
version: 2.5.0
---

# /remember

**Input:** the text after `/remember` is what to save. If empty, ask what to remember in one line.
**Agent:** none.
**Read now:** `KIT/skills/memory-system/SKILL.md` (index format, types, what not to save).

## Steps

1. Classify: `user`, `feedback`, `project`, `reference` or `failure`.
2. Distill to one line of at most 150 characters, keeping the user's exact names and versions. Refuse secrets, tokens, credentials, and facts derivable from code (`package.json`, lockfiles).
3. Open `<project>/.agents/memory/MEMORY.md`. Missing: create `.agents/memory/` and the file with the index skeleton from `memory-system`. Read-only project root: say so and stop.
4. Add the entry under its section, or replace the entry on the same subject instead of appending a contradiction.
5. More than one line of detail: put it in `.agents/memory/<topic>.md` and point the index entry at it.
6. Index over 200 lines: say so and propose merges; never delete entries without asking.

## Output

```
Saved to .agents/memory/MEMORY.md
[project] Use bun instead of npm for all scripts
```
