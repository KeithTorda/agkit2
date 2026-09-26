---
name: deploy
description: "/deploy - Pre-flight checks, build, deploy to preview or production, health verification, and rollback on failure. Tier 3 in code-rules: production needs the user's approval. Use when the user asks to deploy, release, ship, publish or roll back."
version: 2.5.0
---

# /deploy

**Input:** `/deploy check` (pre-flight only), `/deploy preview`, `/deploy production`, `/deploy rollback`. Plain `/deploy` runs check, then asks which target.
**Agent:** `KIT/agents/devops-engineer.md`.
**Read when:** SSH, PM2, Docker or Nginx commands → `KIT/skills/shell-ops/SKILL.md`.

## Steps

1. **Pre-flight.** `python "KIT/scripts/verify_all.py" . --url <url>` (required checks pass), production build succeeds, no secrets in the repo, env vars documented for the target, pending migrations listed, rollback target known (previous deployment id, image tag or commit).
2. **Approval.** Production deploys and production rollbacks need the user's go-ahead (`universal-rules`); preview deploys do not. State target, version and migrations, then wait.
3. **Backup** what the deploy changes irreversibly (the database before migrations).
4. **Deploy** with the platform's own tool and watch the output.

| Platform | Deploy | Rollback |
|---|---|---|
| Vercel / Netlify | git push or `vercel --prod` | promote the previous deployment |
| Railway / Render / Fly.io | `railway up` / dashboard / `fly deploy` | previous release (dashboard or `fly releases`) |
| Docker / compose | `docker compose up -d` with a new image tag | previous image tag |
| VPS + PM2 | pull, build, `pm2 reload <app>` | restore backup, check out previous tag, `pm2 reload` |
| Laravel on VPS | pull, `composer install --no-dev -o`, `php artisan migrate --force`, `php artisan optimize`, reload PHP-FPM or queue workers | previous release folder or tag, restore DB backup if migrations ran |
| Shared hosting (cPanel) | upload build or git deploy, run migrations from the terminal if available | re-upload the previous build |

5. **Verify** in the first minutes: health endpoint 200, error logs quiet, one key user flow works, response times normal.
6. **Confirm or roll back.** Service down or critical errors → roll back first, debug later. Minor issue → fix forward. One rollback, not a chain of changes.

## Output

```markdown
## Deployment: <environment>
Version: <tag or commit> · Platform: <name> · Migrations: <n | none>
Pre-flight: <commands> → <outcome>
URL: <url> · Health: <status> · Logs: <clean | issues>
Rollback: <previous version> via <command>
```

On failure: the failing step, the exact error, the fix, and whether the previous version is still serving.

## Rules

- Risky changes go to preview first. One change per deploy; feature flags for high-risk changes.
- Keep watching after a production deploy; do not end the turn with an unverified deploy.
