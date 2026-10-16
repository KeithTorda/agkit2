---
name: status
description: "Read-only summary of current project progress, changes and observed check results. Use /status for where work stands; /doctor diagnoses AGKIT2 installation/configuration issues."
version: 2.8.2
---

# /status

Report the current project or supplied path without editing files, installing tools or running a new verification suite. Batch independent reads where practical.

Inspect project metadata and source state. `python "KIT/scripts/session_manager.py" status <project>` provides a project snapshot when useful. Read git status/recent history if this is a repository; distinguish committed work, uncommitted changes and unknown state.

Summarize relevant plans and proplan milestones from actual checkboxes/dependencies. Name the next ready work, unresolved blockers and source artifact. A checked task is recorded progress, not proof its old verification is current.

Report checks actually observed in this session with their target and outcome; otherwise say the latest result is unavailable or historical. Use available runtime state for active workers or a dev-server URL; do not label unavailable agent state as confirmed none. Mention existing project memory only when relevant without reciting unrelated entries.

Keep the output focused on completed behavior, current work, next step and material uncertainty. Use `/verify` for new behavior checks. If the issue is the kit itself, route to `KIT/skills/doctor/SKILL.md`; do not run kit diagnostics for every ordinary project status.
