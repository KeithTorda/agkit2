---
name: verify
description: "/verify — Proves code works by running it: build, tests, checklist gates, a runtime request or render, and an error path, reported with evidence. Use after a change, before claiming done, or when the user asks whether something works."
version: 2.0.0
---

# /verify

**Input:** the text after `/verify` says what to verify; if empty, verify the changes made in this session.
**Agent:** read `C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/agents/test-engineer.md`.
**Skills:** `@[skills/verify-changes]` (method, evidence report), `@[skills/lint-and-validate]`.

## Steps

1. **Identify** what changed: files, behavior, the original requirement (`git status`, `git diff`).
2. **Choose the method** from the table in `verify-changes`: bug fix → reproduce; feature → run it; refactor → existing tests; API → call it; UI → render it.
3. **Run the gates.**
   - Fast gate: `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/checklist.py .`
   - Release gate (before deploy, app running): `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/verify_all.py . --url <url>`
   - Required checks pass before "done"; advisory findings are reported. The required-vs-advisory split and the auto-fix policy are the global `code-rules` rule's.
4. **Execute** the change-specific checks: build, tests, a request or render, and at least one error path.
5. **Report** with real command output. Flag anything that could not be executed.

## Output

```markdown
## Verification Report
### Changes verified
- <file or behavior>: pass | fail
### Evidence
- Build: `<command>` → <result>
- Tests: `<command>` → <n>/<n> passed
- Checklist: required pass | fail; advisory <n> findings
- Runtime: `<command>` → <observed output>
- Error path: <input> → <observed>
### Not verified
- <needs manual testing and why>
```

## Rules

- "It should work" is not verification. Run it.
- Do not summarize output you did not see in this session.

## Verification

- Every pass line cites a command that ran here.
- Required checks pass, or the report says exactly what still fails.
