---
name: remember
description: "Save or update requested project notes in .agents/memory/MEMORY.md. Use /remember or an explicit memory request; ordinary task completion does not trigger a save."
version: 2.8.2
---

# /remember

The text after the command is the requested note. If no note can be identified from context, ask what to remember. Read `KIT/skills/memory-system/SKILL.md` for scope and storage.

Confirm the project and inspect relevant existing entries. Distill the requested decision, convention, preference, reference or durable failure into a concise useful entry with its scope/reason. Preserve exact names and versions where material; avoid arbitrary character limits that destroy meaning.

Create `.agents/memory/` and its index only as part of this authorized save. Update a matching entry rather than adding contradictions; use a focused topic note only when useful detail warrants it. Do not include secrets, raw personal data or an entire transcript. Do not silently change unrelated notes or a global memory store.

Report what was saved and where. If the requested location is unwritable, state that it was not saved and provide the concise note for the user; do not claim persistence.
