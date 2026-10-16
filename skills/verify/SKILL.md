---
name: verify
description: "Execute relevant checks and inspect requested behavior with real evidence. Use /verify for explicit verification, the current change or release readiness; report incomplete checks honestly."
version: 2.8.2
---

# /verify

Read `KIT/skills/verify-changes/SKILL.md`. Use the supplied target or identify the current task's change and its intended outcome. An explicit verification request warrants a thorough pass of that target, not unrelated tooling across every ecosystem.

Select evidence that could disprove the claim: relevant tests, config/build consumption, an endpoint request, failure/denial path, real render or generated artifact. Use project commands first. Checklist/verify_all are useful when their detected scope and prerequisites fit; inspect what they actually ran.

Run the checks, investigate failures and correct defects within the authorized task. Recheck affected behavior after fixes. Separate pre-existing failures from new regressions and unavailable prerequisites. An idle development server is setup to resolve when practical, not an automatic visual-check exemption.

Report the observed result, useful commands/actions, relevant findings and what could not be verified. Exit zero alone does not establish a pass; read outcome, verified/not_verified and per-check results as described in verify-changes.
