---
name: debug
description: "/debug - Find and fix the root cause of an error, crash, regression or wrong behavior. Use it when the cause is unknown or a quick fix needs confirming."
version: 3.2.0
---

# /debug

Turn a reported symptom into a confirmed cause and a minimal fix. Work as `KIT/agents/debugger.md` and follow the method in `KIT/skills/systematic-debugging/SKILL.md`.

## Steps

1. Read the symptom from the text after the command. Fill gaps from the current task and the code before asking the user.
2. Write down three facts: expected behavior, observed behavior, and the input or environment that triggers it.
3. Reproduce the failure when practical (request, command, page action or failing test the user already has).
4. Trace the data or control flow back to the first wrong value or decision. Read the logs, stack trace and the code at each hop.
5. List one to three hypotheses. Check each with evidence that tells them apart (a log line, a query result, a breakpoint value).
6. If the cause is an obvious local mistake (typo, wrong field name, missing import), fix it directly and move on.
7. Fix the cause at its owning layer: service, query, migration, component state or config. Remove any experimental edits that did not help.
8. After two failed attempts, step back and use `KIT/skills/problem-solving/SKILL.md` to reframe.
9. Add a regression test only when the user asked for tests, following `KIT/skills/testing-patterns/SKILL.md`.

## Stack notes

- Laravel: check `storage/logs/laravel.log`, Form Request rules, Eloquent relations and queue failures.
- Next.js/React: separate server vs client errors; check hydration warnings and route handler responses.
- MySQL/Postgres: run `EXPLAIN` for slow queries; check constraints and nullable columns.
- VPS: read `pm2 logs`, Nginx error log and PHP-FPM log before changing code.
- A missing service or tool in this environment is an environment limit, not proof of an app bug.

## Output

Report in the rule-02-work-style shape. Include the cause with file and line, the change, what evidence confirmed it, and what is still uncertain. Mark anything not executed as "not run".

## Before you finish, check

- [ ] The cause is named with a source location, not guessed.
- [ ] The fix sits where the cause lives, with no leftover debug code.
- [ ] Failed experiments are reverted.
- [ ] Runs that did not happen are reported as "not run".
