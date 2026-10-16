---
name: memory-system
description: "Read and maintain authorized project memory for durable decisions, conventions and lessons. Use for /remember, explicit save/update requests and relevant existing project notes; ordinary work does not imply permission to write memory."
version: 2.8.2
---

# Project Memory

Project notes live at `<project>/.agents/memory/MEMORY.md`. Existing notes can supply relevant context; verify drift-prone claims against current source. Missing memory is normal and does not block a task.

## Read selectively

Read the index when it is relevant to the current work, then only matching topic notes. Give workers the relevant decisions in their brief rather than making every worker read all memory. Treat old notes as context, not authority above the user's current request or actual behavior.

## Write with authorization

Create or change memory only when the user requests it or explicitly authorizes a project workflow that includes it. A successful fix, a failed experiment or an agent suggestion alone does not authorize a save. Do not write to a global memory store when the request concerns project notes.

Keep entries concise and useful without arbitrary character/line limits. Suggested categories are `[user]`, `[feedback]`, `[project]`, `[reference]` and `[failure]`. Store a durable decision with its reason and scope; for a failure record the cause and the approach that worked. Link a focused topic file when detail warrants it.

```markdown
# Memory Index

## Project
- [project] Order IDs are generated offline; server deduplicates by client UUID.

## Failures
- [failure] The target printer lacks the browser API; use the native print adapter.
```

Update the matching entry instead of appending a contradiction. Preserve useful history when a decision changes; do not silently delete unrelated notes. Never save secrets, raw personal data, entire conversations or readily derived inventories. Avoid temporary debug state and claims not established by evidence.

Confirm what was saved and the path. If writing is unavailable, report the limitation without claiming persistence or blocking independent work.
