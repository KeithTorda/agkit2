---
name: universal-rules
version: 2.0.0
priority: P0
trigger: always_on
description: Universal rules for every request — language, project memory, safety, code quality, and the definition of done.
---

# Universal Rules

1. **Language.** Respond in the user's language (Keith often writes Taglish). Code, comments, identifiers, commit messages, and file names are English.
2. **Memory.** If `<project>/.agents/memory/MEMORY.md` exists, read it at session start. Otherwise do nothing. `/remember` creates it.
3. **Code quality.** Follow the `clean-code` skill: small self-documenting functions, no over-engineering, check dependents before editing a file.
4. **Definition of done.** A task is done when the required checks pass (`python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/checklist.py .`) and logic changes have tests. Advisory findings are reported, not blocking. Details: `code-rules`.
5. **Safety.** Never commit or print secrets. Ask before destructive or irreversible actions (deleting files or data, `git push --force`, `DROP`, production deploys). Prefer the project's own scripts (`npm run lint`, `npm test`) over ad-hoc commands.
6. **Host.** Windows 11, PowerShell 7, Python and Node on PATH. Forward-slash paths work; show commands that run in PowerShell.
