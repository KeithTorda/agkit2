---
name: verify-changes
description: How to prove a change works by executing it (build, tests, checklist script, a request or render, an error path) and report evidence, sized to the change's risk tier. Use for /verify, for tier 2-3 changes, and whenever you are about to say "works" or "fixed".
version: 2.5.0
---

# Verify Changes

"Code that exists" is not "code that works". Verify by running things, never by inspection alone, and run as much as the risk calls for.

## What counts as evidence

Evidence is output you produced: the command and what it printed (an exit code, `42 passed`, an HTTP `200` with the body, the rendered screen, the message on the bad-input path). Not evidence: "it should work", "the types line up", "it compiles so it is correct", or a description of expected output. If you did not run it, list it under `Not verified`.

## How much to run

The tier table in `code-rules` decides. In short:

| Tier | Change | Run |
|---|---|---|
| 0 | copy, a style value, a comment | nothing; say so |
| 1 | a component, an endpoint, a few files | the project's own lint/types/tests for touched files (`python "KIT/scripts/checklist.py" . --quick`) |
| 2 | auth, payments, permissions, migrations, data deletion, public API, shared utilities | `checklist.py . --full`, tests for the logic, `/review` on the diff |
| 3 | deploy, production data | `python "KIT/scripts/verify_all.py" . --url <url>` plus the `/deploy` steps |

Required failures (block done at tier 2-3): security high+, type errors, failing tests. Lint style, naming, CSS audit, UX/SEO heuristics are advisory: report them, fix them when cheap and in scope, ask before fixes that change design or scope.

## Pick the method

| Change | Verify by |
|---|---|
| Bug fix | Reproduce the original scenario; it no longer occurs |
| New feature | Run it; expected output, plus one error path |
| Refactor | Existing tests pass; behaviour unchanged |
| API change | Call the endpoint; response shape and status codes, including one 4xx |
| UI change | When a dev server is running and layout changed: render it (`/see`, or the `browser` built-in subagent if available in your Antigravity version) at 390 px and 1440 px, check the console, try one interaction. No server or browser: say so |
| Config or build | Load the config or run the build; values applied, build succeeds |
| Generated document | `/see-doc` |

## Per project type

- **Web app:** build, lint script, tests, dev server starts, changed pages render, no console errors.
- **API:** server starts, changed endpoints respond, error cases return the right status, queries run.
- **CLI or script:** runs, expected output, bad input handled, `--help` correct.
- **Mobile:** builds for the target platform, changed screen renders, navigation to and from it works.

## Report

```markdown
<Result in one line>
Evidence:
- Build: `npm run build` → ok
- Tests: `npm test` → 42/42 pass
- Checklist: `checklist.py . --full` → required pass; 3 advisory (listed)
- Runtime: `GET /api/users` → 200 with the expected JSON
- Error path: empty email → 400 "email required"
Not verified: <what needs a manual check and why>
```

## Anti-patterns

| Avoid | Do instead |
|---|---|
| "It should work" | Run it and show the output |
| Only the happy path | Try at least one error path |
| Compiles, therefore correct | Test runtime behaviour |
| Running the full gate on a one-line copy change | Match the checks to the tier |
| Fixing advisory findings that change design or scope without asking | Report them and ask |
