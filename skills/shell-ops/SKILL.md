---
name: shell-ops
description: Shell and server cheat sheet - Bash and PowerShell 7 equivalents, safe defaults for scripts and process handling, Windows 11 host notes (PowerShell 7, PortableGit), and Linux server basics (systemd, nginx, ufw, SSH keys, backups). Use when writing or translating shell commands and scripts, running commands on the user's Windows host or a Linux server, or setting up and operating a small server.
version: 2.0.0
---

# Shell Ops

The user's workstation is Windows 11 with PowerShell 7 (`pwsh`) and PortableGit; servers are Linux with Bash. Write commands for the shell that will actually run them, and say which one you mean.

**Which shell.** Target the shell that will execute the code, not the one you happen to be typing in:

- Commands on the user's host -> PowerShell 7.
- A Linux server, a Docker/CI step, or a Dockerfile `RUN` -> Bash.
- A deploy script that runs on the Linux server is Bash even though you author it on Windows (run it through PortableGit locally, or on the server).
- Anything that has to run on both the Windows host and Linux -> write it in Python, like the kit's own scripts, not a shell script ported twice.

Do not translate a script line by line between the two: PowerShell pipes objects (`Where-Object`, `Select-Object`), Bash pipes text (`grep`, `awk`) — use each one's idioms.

## 1. Bash and PowerShell equivalents

| Task | Bash (Linux/macOS) | PowerShell 7 (Windows) |
|------|--------------------|------------------------|
| List files | `ls -la` | `Get-ChildItem -Force` (`ls` alias works) |
| Find files | `find . -name "*.ts" -type f` | `Get-ChildItem -Recurse -Filter *.ts -File` |
| Search text | `grep -rn "TODO" src/` | `Select-String -Path src\* -Pattern TODO -Recurse` |
| Show file | `cat f`, `head -n 20 f`, `tail -f log` | `Get-Content f`, `-Head 20`, `-Wait` |
| Copy / move / delete | `cp -r`, `mv`, `rm -rf` | `Copy-Item -Recurse`, `Move-Item`, `Remove-Item -Recurse -Force` |
| Env var | `echo $PATH`, `export X=1` | `$env:PATH`, `$env:X = "1"` |
| Chain on success | `a && b` | `a && b` (PowerShell 7+) |
| Pipeline | text lines | objects; use `Select-Object`, `Where-Object` |
| Processes | `ps aux \| grep node` | `Get-Process node` |
| Port in use | `ss -ltnp \| grep :3000` | `Get-NetTCPConnection -LocalPort 3000` |
| Stop a process | `kill -TERM <pid>` then `kill -9` | `Stop-Process -Id <pid>` (`-Force` last) |
| Download | `curl -fsSL URL -o file` | `Invoke-WebRequest URL -OutFile file` (or `curl.exe`) |
| JSON | `jq '.key' file.json` | `Get-Content file.json -Raw \| ConvertFrom-Json` |
| Script dir | `"$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"` | `$PSScriptRoot` |
| Null / empty check | `[ -n "$x" ]` | `if ($x)`; arrays: `if ($a -and $a.Count)` |
| Paths | `/home/user/app` | `Join-Path $env:USERPROFILE app`; forward slashes work in most tools |

## 2. Safe defaults

Three foot-guns cause most shell disasters: an unset variable, an unquoted expansion, and an ignored failure. One example, wrong then right:

```bash
# wrong: if BUILD_DIR is unset this runs `rm -rf /*`, and a failed
# build still falls through to deploy
cd $BUILD_DIR
rm -rf $BUILD_DIR/*
npm run build
deploy
```

```bash
# right
set -euo pipefail                 # an unset var, or any command failing, aborts
: "${BUILD_DIR:?set BUILD_DIR}"   # refuse to run with an empty path
cd "$BUILD_DIR"                   # quote every expansion
rm -rf "${BUILD_DIR:?}/"*         # guarded even if BUILD_DIR is later unset
npm run build && deploy           # deploy only if the build succeeds
```

Bash scripts:

```bash
#!/usr/bin/env bash
set -euo pipefail
trap 'rm -f "$tmp"' EXIT
tmp="$(mktemp)"
```

Quote every variable (`"$file"`), use `command -v tool >/dev/null` to check for tools, `${1:-default}` for defaults, `while IFS= read -r line; do ...; done < file` to read lines.

PowerShell scripts:

```powershell
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'   # fail fast; never 'Continue' in scripts
try {
    # work
} finally {
    # cleanup
}
```

Wrap each cmdlet in parentheses inside logical expressions: `if ((Test-Path a) -or (Test-Path b))`. Use ASCII-only output markers (`[OK]`, `[WARN]`) in scripts; emoji breaks in some consoles. `ConvertTo-Json -Depth 10` for nested objects. Return after `try/catch`, not inside `try`.

Processes and networking (both):

- Stop processes gracefully first (`kill -TERM`, `Stop-Process` without `-Force`); use `kill -9` only when the process ignores TERM.
- Use `ip addr` / `ip route` and `ss` on Linux; `ifconfig` and `netstat` are legacy.
- Never paste secrets into commands; read them from the environment or a secrets file with restricted permissions.
- Prefer `curl -fsSL` (fail on HTTP errors) over bare `curl`.
- Destructive file ops: dry-run first (`Remove-Item -WhatIf`; echo the glob before `rm`), never delete a path built from an unvalidated variable, and write-then-rename (`mv tmp final`) for updates that must not be seen half-written.

## 3. Windows host notes

- Run project commands from `pwsh`, not `cmd.exe`. `python` and `node` resolve from PATH; kit scripts run as `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/checklist.py .`.
- PortableGit provides `git` plus a Bash (`git-bash`) with `ssh`, `scp`, `tar`, `curl`; use it when a tool only ships Bash instructions. `sh -c` inside PowerShell needs Git's `sh.exe` on PATH.
- npm scripts run through `cmd`; a `--` is required before extra flags: `npm run build -- --debug`.
- Line endings: set `git config core.autocrlf input` for repos that deploy to Linux; keep kit files LF.
- Long paths: enable `git config core.longpaths true` if `node_modules` paths exceed 260 characters.
- Execution policy blocks unsigned `.ps1` files by default: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

## 4. Linux server basics

Process management (systemd):

```ini
# /etc/systemd/system/app.service
[Unit]
Description=App
After=network.target
[Service]
User=app
WorkingDirectory=/srv/app
EnvironmentFile=/srv/app/.env
ExecStart=/usr/bin/node server.js
Restart=on-failure
[Install]
WantedBy=multi-user.target
```

`systemctl daemon-reload && systemctl enable --now app`; logs with `journalctl -u app -f`. PM2 is acceptable for Node when you want clustering without writing units; Docker Compose when the stack has several services.

Reverse proxy (nginx): one server block per site in `/etc/nginx/sites-available/`, `proxy_pass http://127.0.0.1:3000`, set `proxy_set_header Host $host` and `X-Forwarded-*`, enable gzip, and get TLS from Let's Encrypt (`certbot --nginx`). Test with `nginx -t` before `systemctl reload nginx`.

Firewall (ufw): `ufw default deny incoming`, `ufw allow OpenSSH`, `ufw allow 80,443/tcp`, `ufw enable`. Open nothing else; database ports stay bound to localhost or a private network.

SSH: key-based only (`ssh-keygen -t ed25519`, `ssh-copy-id`), then set `PasswordAuthentication no` and `PermitRootLogin no` in `sshd_config`; run the app as a non-root user; keep `unattended-upgrades` on.

Backups: nightly database dumps (`pg_dump -Fc`) plus uploaded files to off-server storage (`restic` or `rclone` to object storage), retention of at least 7 daily and 4 weekly copies, and a restore test every month; a backup that has never been restored is not a backup.

Monitoring: a health endpoint (`/healthz` returning 200 and checking the database), an uptime monitor hitting it, error tracking (Sentry), and disk, memory, and CPU alerts. Rotate logs (`logrotate` or journald limits) and never log secrets or PII.

Troubleshooting order: is the process running (`systemctl status`), what do the logs say (`journalctl`), are resources exhausted (`df -h`, `free -m`, `top`), is the network path open (`ss -ltnp`, `curl -I localhost:3000`, DNS), are dependencies reachable (database, external APIs).

Scaling: profile before scaling; vertical first for a single instance, horizontal behind a load balancer once the app is stateless (sessions in Redis, uploads in object storage).
