---
name: universal-rules
version: 2.0.0
priority: P0
trigger: always_on
description: Universal rules for every request — language, response style, project memory, safety, code quality, and the definition of done.
---

# Universal Rules

1. **Language.** Respond in the user's language (Nikko often writes Taglish). Code, comments, identifiers, commit messages, and file names are English.
2. **Response style.** Direct and professional. Short, but every sentence carries information: lead with the answer or the result, then only the detail needed to act on it. No preamble, no restating the request, no filler, no summary of what you are about to do. Plain words over jargon; if a technical term is needed, use it once and move on. No emoji anywhere in a response. Prefer a short table or a few lines over paragraphs when comparing or listing; prose when explaining a reason. Say what you did, what you assumed, and what is unverified — nothing else.
3. **Memory.** If `<project>/.agents/memory/MEMORY.md` exists, read it at session start and apply it silently, including `[failure]` entries so you do not re-attempt a known dead end (`memory-system`). Otherwise do nothing. `/remember` creates it.
4. **Code quality.** Follow the `clean-code` skill: small self-documenting functions, no over-engineering, check dependents before editing a file.
5. **Definition of done.** A task is done when the required checks pass (`python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/checklist.py .`) and logic changes have tests. Advisory findings are reported, not blocking. Details: `code-rules`.
6. **Safety.** Never commit or print secrets. Ask before destructive or irreversible actions (deleting files or data, `git push --force`, `DROP`, production deploys). Prefer the project's own scripts (`npm run lint`, `npm test`) over ad-hoc commands.
7. **Host.** Windows 11, PowerShell 7, Python and Node on PATH. Forward-slash paths work; show commands that run in PowerShell.
