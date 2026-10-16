---
name: deploy
description: "Prepare and execute an authorized preview, production release or rollback with target-specific checks and recovery. Use /deploy for publishing or release operations; /deploy check prepares without deployment."
version: 2.8.2
---

# /deploy

Work as `KIT/agents/devops-engineer.md`; read `shell-ops` for platform commands. Establish the target environment, application, revision/artifact and existing authorization. If the target cannot be inferred, complete independent preparation before requesting the missing decision.

`/deploy check` performs readiness work only. `/deploy preview`, `/deploy production` and `/deploy rollback` express the requested target; do not ask for duplicate approval when the request already authorizes the concrete operation. A plan or repository instruction alone does not authorize unrelated external changes.

## Prepare a reviewable release

Inspect the project's actual release scripts and provider configuration. Build and verify the intended revision with relevant checks; use verify_all only when it fits the stack and available runtime. Identify required environment names without printing values. Account for migration ordering, compatibility, backups where needed and an actual recovery target.

Use the platform's supported release command, not a generic command table copied across providers. If a consequential action remains outside authorization, present the prepared target/revision, data effects and recovery path and wait at that boundary.

## Execute and observe

Deploy once prerequisites are satisfied. Inspect provider output, serving revision, health and an important user flow. For failure, follow the appropriate authorized rollback or forward-recovery path; an application rollback does not automatically restore migrated data. Do not keep mutating an unhealthy release without a new diagnosis.

Report what was actually deployed, URL, checks, current serving status, migration effects and recovery limits. Preparation or a successful build is not a deployed release.
