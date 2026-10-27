---
name: app-builder
description: "Build new applications and substantial features by inspecting the product need, existing repository, platform and hosting constraints, then implementing a working vertical slice. Use templates selectively; existing applications keep their supported stack."
version: 2.8.3
---

# Application building

Turn the user's requested outcome into a working application, with the smallest architecture that can support its real requirements. A kit template is a starting reference, not a stack assignment based on a keyword or a visual style.

## Inspect before selecting

Read repository instructions, tracked and uncommitted work, manifests and lockfiles, scripts, configuration, entrypoints, and the nearest existing feature. Identify the actual platform, users, primary workflow, data, identity boundaries, deployment environment, and integrations. Do not scaffold over existing files or replace a healthy app to match this kit.

Visual direction follows the frontend-design note: decide unless genuinely unclear; theming per Rule 01.

Resolve missing facts only when they change a consequential decision. Hosting on shared PHP, native device access, offline transactions, sensitive records, and payment settlement can affect architecture. A generic “modern” or “professional” look does not choose a framework, provider, component package, or paid service.

## Choose a useful path

| Need | Read |
|---|---|
| Identify the deliverable and existing foundation | [project-detection.md](project-detection.md) |
| Compare technologies using concrete constraints | [tech-stack.md](tech-stack.md) |
| Start a genuinely new project | [templates/README.md](templates/README.md), then only the relevant template |
| Lay out code and safe setup | [scaffolding.md](scaffolding.md) |
| Implement within an existing application | [feature-building.md](feature-building.md) |
| Divide work across specialists when available | [agent-coordination.md](agent-coordination.md) |

## Build a complete slice

State the important assumptions and a plan proportional to the task. A small page can use a short in-chat plan; a substantial application benefits from a durable plan with acceptance conditions and dependencies. Do not require a planning command or a document for every task.

Settle interfaces that make parallel work safe: data shape, authorization, API errors, ownership of state, and the primary user flow. Implement a useful path end to end, including real persistence or explicitly identified demo behavior. Add adjacent cases that follow from the feature: validation, unauthorized access, duplicate requests, loading, empty results, and recovery where relevant.

Preserve existing package managers and supported versions. Introduce dependencies for concrete functionality, compatibility, or maintainability; inspect current official setup guidance when creating or upgrading a foundation. Never imply an integration works merely because its environment-variable names or buttons exist. Keep secrets out of source, client bundles, fixtures, and logs.

For UI, use `frontend-design` or `mobile-design`; record a new substantial visual system with `design-spec`. For an export use `document-generation`. Use backend, data, security, or deployment workflows when the requested feature needs them. Avoid loading every specialist or running every scanner for an ordinary change.

## Verify and hand off

Deliver the requested application or feature without an automatic audit/checking phase. Project checks, browser/simulator inspection and verification are manual-only under `kit-core`. Correct defects actually observed while implementing; do not turn ordinary completion into a new review task.

Run the local preview when requested; confirm the served project and route before reporting its URL. Report the working outcome, meaningful technical decisions, actual validation, setup still needed, and exact limitations. “Fresh”, “clean”, and a successful build do not mean zero defects or production readiness.
