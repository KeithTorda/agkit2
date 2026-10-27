---
name: deploy
description: "/deploy - Use to prepare or perform a release, preview or rollback. `/deploy check` prepares only; `/deploy production` and `/deploy rollback` act on the named target."
version: 3.2.0
---

# /deploy

Ship one known revision to one known target with a written rollback path. Work as `KIT/agents/devops-engineer.md` and read `KIT/skills/shell-ops/SKILL.md` for shell commands.

## Steps

1. Identify the target (preview, staging, production), the server or host, and the git revision. If the target is unclear, finish the preparation and ask once.
2. Read the project's deploy scripts, CI files and server notes. Use them instead of generic commands.
3. List the env variables the release needs, by name only. Confirm they exist on the target.
4. Check migrations: are they backward-compatible with the running version, and is there a fresh database backup before any destructive change?
5. `/deploy check`: stop here and report target, revision, env status, migrations and the rollback plan.
6. Production deploys, production restores and DNS changes need the user's yes per rule-02-work-style. A `/deploy production` or `/deploy rollback` command for a named target is that yes.
7. Deploy with the project's release method, then confirm the serving revision, the health endpoint and one key user flow.
8. Restart queue workers and the outbox middleman worker so they run the new code (rule-04-system-integration).
9. On failure, roll back to the previous release. An app rollback does not undo migrations; restore data only with approval.

## Stack notes

- Laravel on VPS: `composer install --no-dev`, `php artisan migrate --force`, `config:cache`, `route:cache`, `view:cache`, `queue:restart`; Supervisor for workers, cron for `schedule:run`.
- Next.js on VPS: `next build`, then `pm2 reload <app>` behind Nginx; `NEXT_PUBLIC_*` values are fixed at build time.
- Expo: EAS build or OTA update to a production channel needs approval like any production release.

## Output

```
Deployed: <revision> to <target> at <URL>
Checks: <health, key flow - observed result>
Migrations: <ran / none, data effects>
Rollback: <command or steps>
Needs your action: <DNS, secrets, approvals>
```

## Before you finish, check

- [ ] The deployed revision and URL are confirmed from the server, not assumed from the build.
- [ ] Workers and schedulers were restarted on the new code.
- [ ] A rollback command or steps are written in the report.
- [ ] No secret values appear in the output or logs.
