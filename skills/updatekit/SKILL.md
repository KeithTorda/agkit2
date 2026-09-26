---
name: updatekit
description: "/updatekit - Fetches the latest AG Kit release from GitHub (KeithTorda/agkit2), updates local repository and plugins, installs rules, and verifies validity."
version: 2.5.0
---

# /updatekit

**Input:** none (or `--check` to preview without applying).
**Agent:** none.

Fetches the latest version of AG Kit directly from GitHub (`https://github.com/KeithTorda/agkit2.git`), updates the source repository on `c:\Users\Keith\Desktop\agkit2`, syncs the Antigravity plugin and rules directories, and runs validation.

## Steps

1. **Check local git repository.**
   Ensure `c:\Users\Keith\Desktop\agkit2` is on the `main` branch.
   Run:
   ```powershell
   git -C "c:\Users\Keith\Desktop\agkit2" fetch origin main
   ```

2. **Compare commit hash.**
   Check if local `HEAD` is behind `origin/main`:
   ```powershell
   git -C "c:\Users\Keith\Desktop\agkit2" rev-parse HEAD
   git -C "c:\Users\Keith\Desktop\agkit2" rev-parse origin/main
   ```
   If identical, report that AG Kit is already at the latest commit.

3. **Pull latest changes.**
   ```powershell
   git -C "c:\Users\Keith\Desktop\agkit2" pull origin main
   ```

4. **Re-install into Antigravity.**
   Execute the installer to update plugin files and rules:
   ```powershell
   powershell -ExecutionPolicy Bypass -File "c:\Users\Keith\Desktop\agkit2\install.ps1"
   ```

5. **Validate Installation.**
   Confirm schema and rule budget:
   ```powershell
   python "KIT/scripts/validate_kit.py" "KIT" --rules "KIT/../../rules" --quiet
   ```

6. **Report outcome.**
   Output the updated version, commit hash, and reminder to restart the IDE if subagent definitions changed.
