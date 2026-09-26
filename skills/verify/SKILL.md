---
name: verify
description: "/verify - Proves a change works by running it: build, tests, the checklist script, a request or render, one error path, reported with real output. On-demand deep check; use when the user asks whether something works, for tier 2-3 changes, or before a release."
version: 2.5.0
---

# /verify

**Input:** the text after `/verify` says what to verify; empty means the changes made in this session.
**Agent:** `KIT/agents/test-engineer.md`.
**Read now:** `KIT/skills/verify-changes/SKILL.md` (method table, evidence rules, report format).

## Steps

1. **Identify** what changed and what it was meant to do (`git status`, `git diff`, the request).
2. **Pick the method** from `verify-changes` (bug fix → reproduce; feature → run it; refactor → existing tests; API → call it; UI → render it).
3. **Run the checks.** When the user calls `/verify`, run the full set for the change, whatever its tier:
   - `python "KIT/scripts/checklist.py" . --full`
   - release (app running, before deploy): `python "KIT/scripts/verify_all.py" . --url <url>`
   - the change-specific commands: build, tests, a request or render, at least one error path.
4. **Report** with real output; list anything that could not run under `Not verified`.

"It should work" is not verification. Do not summarise output you did not see in this session.
