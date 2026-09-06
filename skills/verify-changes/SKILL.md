---
name: verify-changes
description: Proves a change works by executing it (build, tests, checklist gates, a request or render, an error path) and reporting evidence, with the split between required checks and advisory findings. Use after writing or fixing code, before saying done, and for /verify.
version: 2.0.0
---

# Verify Changes

> "Code that exists" is not "code that works". Verification by execution, never by inspection or assumption.

## What counts as evidence

Evidence is output you produced, not a prediction of it: the command you ran and what it printed — an exit code, `42 passed`, an HTTP `200` with the body, the rendered screen, the message on the bad-input path. Not evidence: "it should work", "the types line up", "compiles, so it's correct", or a description of the output you expect. If you did not run it, it is unverified — say so under "Not verified".

## Protocol

1. **Identify what changed** — files, the expected behavior difference, the original bug or requirement.
2. **Pick the method.**

| Change | Verify by |
|---|---|
| Bug fix | Reproduce the original scenario → it no longer occurs |
| New feature | Run it → expected output, plus one error path |
| Refactor | Existing tests pass; behavior unchanged |
| API change | Call the endpoint → response shape and status codes |
| UI change | **Required UI-render gate** — `browser-verification` (`/see`): render it, check computed styles vs `DESIGN.md`, console/network, one interaction, breakpoints. Gate and escape hatch: `code-rules` |
| Config or build | Load the config / run the build → values applied, build succeeds |

3. **Run the gates.**

- Fast gate (every change): `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/checklist.py .`
- Release gate (before deploy, app running): `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/verify_all.py . --url <url>`

| Kind | Checks | On failure |
|---|---|---|
| Required | Security (high+), lint, type errors, tests, UI-render gate for rendered UI | Fixed before "done" |
| Advisory | UX, accessibility heuristics, SEO, GEO, mobile, API heuristics, bundle, Lighthouse | Reported with findings |

The required/advisory split and the auto-fix policy live in the global `code-rules` rule; this skill is how you run the checks and prove the result. "Done" means required checks pass and logic changes have tests.

4. **Execute the change-specific commands** — build, tests, dev server start, a `curl` or fetch, a script run with bad input.
5. **Report evidence** with the real output.

```markdown
## Verification Report
### What changed
- <files and summary>
### How it was verified
- `<exact commands>`
### Evidence
- Build: pass — <output line>
- Tests: 42/42 passing
- Checklist: required pass; advisory 3 findings (listed below)
- Runtime: server starts; `GET /api/users` → 200 with the expected JSON
- Error path: empty input → 400 with message
### Not verified
- <what needs a manual check and why>
```

## Checklist by project type

- **Web app:** build, the project's lint script, tests, dev server starts, changed pages render, no browser console errors.
- **API:** server starts, changed endpoints respond, error cases return the right status, DB queries run.
- **CLI or script:** runs without errors, expected output matches, bad input handled, help text correct.
- **Mobile:** app builds for the target platform, the changed screen renders, navigation to and from it works.

## Anti-patterns

| Avoid | Do instead |
|---|---|
| "It should work" | Run it and show the output |
| Only the happy path | Test at least one error path |
| Compiles, therefore correct | Test runtime behavior |
| Skipping checks for a "trivial" change | Run the required checks for every change; run advisory checks when the change touches their area |
| Fixing advisory findings that change design or scope without asking | Report them and ask |
