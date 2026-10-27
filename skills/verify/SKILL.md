---
name: verify
description: "/verify - Use when the user asks to verify a change, a feature or release readiness; runs the relevant checks and reports real results."
version: 3.2.0
---

# /verify

The user invoked this command, so run the checks now and report what they show. Read `KIT/skills/verify-changes/SKILL.md` for how to pick evidence and read results.

## Steps

1. Name the target: the change, feature or release the user means, and what it should do.
2. Pick evidence that could prove the claim wrong: the related tests, an API request including a denied or invalid case, a build, or a rendered page for UI work.
3. Run the project's own commands first (`npm test`, `php artisan test`, `npm run build`).
4. Use the kit runners when they fit the stack: `python "KIT/scripts/checklist.py" . --quick` for changed files, `--full` for release readiness, and `python "KIT/scripts/verify_all.py" . --url <running-url>` when a server is running.
5. Read each result's `outcome` (PASS, FAIL, INCOMPLETE, SKIPPED). An exit code of zero with skipped checks means not verified.
6. Fix defects the change introduced, within the task, then rerun the affected checks. List failures that existed before the change separately.
7. If the dev server is needed and not running, start it.

## Output

```
Target: <what was verified>
Ran: <command> -> <result>
Found: <defects fixed / still open>
Not verified: <checks that could not run, and why>
```

## Before you finish, check

- [ ] Every claim in the report matches a command that ran in this session.
- [ ] Skipped or incomplete checks are listed under "Not verified".
- [ ] New failures and pre-existing failures are reported separately.
