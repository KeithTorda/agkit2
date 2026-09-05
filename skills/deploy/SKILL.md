---
name: deploy
description: "/deploy — Runs pre-flight checks, builds, deploys to preview or production, verifies health, and rolls back on failure. Use when the user asks to deploy, release, ship, publish, or roll back."
version: 2.0.0
---

# /deploy

**Input:** `/deploy check` (pre-flight only), `/deploy preview`, `/deploy production`, `/deploy rollback`. Plain `/deploy` runs check, then asks which target.
**Agent:** read `C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/agents/devops-engineer.md`.
**Skills:** `@[skills/verify-changes]`; `@[skills/shell-ops]` for SSH, PM2, and Docker commands.

## Steps

1. **Pre-flight.** Release gate `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/verify_all.py . --url <url>` (required checks pass), production build succeeds, no secrets in the repo, env vars documented for the target, pending migrations listed, rollback target known (previous deployment id, image tag, or commit).
2. **Approval.** Production deploys and production rollbacks are irreversible actions — the global `universal-rules` Safety rule requires approval before them; preview deploys do not. State target, version, and migrations, then wait for the go-ahead before touching production.
3. **Backup** what the deploy changes irreversibly (database before migrations).
4. **Deploy** with the platform's own tool and watch the output.

| Platform | Deploy | Rollback |
|---|---|---|
| Vercel / Netlify | git push or `vercel --prod` | promote the previous deployment |
| Railway / Render / Fly.io | `railway up` / dashboard / `fly deploy` | previous release (dashboard or `fly releases`) |
| Docker / compose | `docker compose up -d` with a new image tag | previous image tag |
| Kubernetes | `kubectl apply` | `kubectl rollout undo` |
| VPS + PM2 | pull, build, `pm2 reload` | restore backup, `pm2 reload` |

5. **Verify** during the first minutes: health endpoint returns 200, error logs stay quiet, one key user flow works, response times are normal.
6. **Confirm or roll back.** Service down or critical errors → roll back first, debug later. Minor issues → fix forward. One rollback, not a chain of changes.

## Output

```markdown
## Deployment: <environment>
Version: <tag or commit> · Platform: <name> · Migrations: <n | none>
Pre-flight: required checks pass · build ok
URL: <url> · Health: <status> · Logs: <clean | issues>
Rollback: <previous version id> via <command>
```

On failure: the failing step, the exact error, the fix, and whether the previous version is still serving.

## Rules

- Never deploy untested code; a risky change goes to preview first.
- One change per deploy; feature flags for high-risk changes; small, frequent releases.
- Keep watching after a production deploy; do not end the turn with an unverified deploy.

## Verification

- Health check and one real request succeeded after the deploy.
- The rollback command was identified before deploying.
