---
name: updatekit
description: "Check upstream AGKIT2 changes or update a clean source repository and activate it with backup/validation. Use /updatekit; --check fetches metadata but never pulls or installs."
version: 2.8.2
---

# /updatekit

Use the existing helper, preserving local customization:

```powershell
python "KIT/scripts/update_kit.py" --check
python "KIT/scripts/update_kit.py" --repo "<source repository>"
```

`--check` fetches Git metadata and compares HEAD with the selected origin branch, then returns before pull/install even when they match. It does not update source worktree files, active rules or installed plugin files. Fetch can require network access and changes Git metadata; do not describe it as entirely filesystem read-only.

Applying an update requires a clean source worktree on the selected branch and a fast-forward pull. The helper will not discard, stash or reset customizations. If local changes exist, report them and preserve/merge them within the user's scope rather than overwriting them. `--branch` defaults to main; inspect before selecting a different branch. The helper locates an adjacent source repository or the user's Desktop/agkit2; `--repo` selects another location.

The installer validates source/staging, backs up active files, activates and verifies them, restoring prior active files if activation fails. `install.ps1 -Check` validates without activation; inspect the installer's current parameters before using custom locations. Report the actual source revision/version, installation outcome and backup path from execution, not a predicted success.

For conflicting rules, drift or broken setup, use `KIT/skills/doctor/SKILL.md` to diagnose before changing configuration. Restart Antigravity/open a new chat to load changed instructions; an installed kit is not a tested generated design.
