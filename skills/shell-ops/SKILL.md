---
name: shell-ops
description: Write and diagnose shell commands, scripts, processes and small-server operations with correct Bash or PowerShell semantics. Use for shell/host work; inspect the real environment and scope filesystem/process changes precisely.
version: 2.8.2
---

# Shell and Host Operations

Determine the shell/version, OS, working directory, executable paths and relevant environment before translating commands. PowerShell pipelines carry objects; Bash pipelines usually carry text. Similar aliases do not guarantee identical argument or error behavior.

## Read and search precisely

Prefer `rg`/`rg --files` where installed. Quote paths and distinguish literal from wildcard paths. In PowerShell, use `-LiteralPath` when a path may contain brackets or other wildcard characters. `Select-String` does not offer a general recursive file switch: enumerate files first.

```powershell
Get-ChildItem -LiteralPath .\src -File -Recurse |
  Select-String -Pattern 'TODO' -SimpleMatch
Get-Content -LiteralPath '.\config\app.json' -Raw | ConvertFrom-Json
```

Avoid dumping environment variables, credential files or command lines containing tokens. Print presence/status or a redacted summary instead.

## Reliable execution

Use the language's actual quoting rules. `JSON.stringify()` is not shell escaping. PowerShell double-quoted strings expand variables/subexpressions; single-quoted here-strings preserve literal script bodies. Prefer structured arguments or a temporary file for complex multiline content. Do not evaluate untrusted text as code.

A native program's failure is not always a shell exception. In PowerShell check `$LASTEXITCODE` for native tools; `$ErrorActionPreference = 'Stop'` handles many cmdlet errors. In Bash, `set -euo pipefail` can help but has contextual exceptions; still handle important statuses and cleanup explicitly. Do not interpret an empty pipeline as a proven success.

Keep the project's supported interpreter/runtime; do not assume `python`, `node`, `git` or package executors resolve to the intended installation. Use explicit working directories. Avoid repurposing `$HOME`, `$home`, `$CODEX_HOME`, `$PID` or other reserved/system variables.

## Files and processes

Before recursive deletion/moving, resolve and verify the target is within the intended directory and is not the root, home or an empty expansion. Inspect symlink/reparse behavior where it matters. Use one shell end-to-end for filesystem mutations, native literal-path cmdlets on Windows, and a recoverable backup for valuable data. Do not pipe enumerated paths into another shell's delete command.

Find processes by verified PID, owner, command and listening port before stopping them. A process name alone may match unrelated work. Prefer graceful shutdown where supported, then a bounded forced stop only if justified. Start background helpers hidden on Windows unless the user needs an interactive window; record the PID/log location and cleanup ownership.

A timeout may end the wrapper without ending a child tree. Confirm process state and clean up only the process tree created for the task. Do not leave servers or watchers running accidentally.

## Small-server changes

Inspect service, reverse-proxy, firewall and deployment configuration before editing. Validate syntax with the installed tool before reloading. Keep SSH/recovery access and an understood rollback path when changing network/auth settings. Do not open ports, disable TLS validation or turn off a sandbox merely to silence an error.

Use least-privilege service identities, deliberate writable directories, secret storage and bounded restart/log policies. Check service logs, actual health endpoints and dependencies after restart. A running process is not proof the application works. Backups are useful only if restoration and retention meet the data requirement.

Report commands/results and meaningful limitations. Follow the central authorization policy for remote/destructive actions rather than creating a new permission ritual for ordinary read-only diagnostics.
