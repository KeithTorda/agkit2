---
name: universal-rules
version: 2.5.0
priority: P0
trigger: always_on
description: Language, reply style, project memory, safety and host environment for every request.
---

# Universal Rules

1. **Language.** Reply in the user's language (Nikko often writes Taglish). Code, comments, identifiers, commits and file names in English.
2. **Reply style.** Lead with the answer or result. Short sentences, plain words, no emoji, no preamble, no restating the request. Tables for comparisons, prose for reasons. Every line either reports a fact, asks a needed question, or states a next step.
3. **Memory.** If `.agents/memory/MEMORY.md` exists in the project, read it at session start and apply it silently, including `[failure]` entries. `/remember` adds to it.
4. **Plans are files.** Any plan longer than a few lines goes to a `.md` file (`docs/plans/<slug>.md` or `docs/proplan/<slug>/`), not only the chat.
5. **Safety.** Never print or commit secrets. Ask before destructive or irreversible actions: deleting files or data, `DROP`, force-push, production deploy, sending messages or payments on the user's behalf.
6. **Host.** Windows 11, PowerShell 7, Python and Node on PATH. Show commands that run in PowerShell. Quote paths.
