# Choose technology for the constraints

Preserve a healthy existing stack, package manager, lockfile and deployment path. For a new project, respect explicit user choices and compare viable foundations against real requirements. Templates describe one option; they do not convert aesthetic references into packages.

| Decision | Evidence that matters |
|---|---|
| Static or application runtime | Content update model, dynamic data, user identity, mutations, interaction and hosting |
| Server framework | Existing team/code, language, auth, jobs, integration ecosystem, operations |
| Storage | Data relationships, transactions, search, volume, isolation, backup and deployment constraints |
| Client state | Local transient state versus shared application state versus server cache |
| Native/cross-platform | Required device APIs, platform conventions, performance, distribution and maintainers |
| Styling/components | Current design system, accessibility behavior, required customization and supported browsers |
| Background work | Work duration, retry semantics, volume, cancellation and infrastructure |

Start with fewer moving parts when they meet the requirements. A small app need not have a separate API deployment, queue, global store, monorepo, ORM, or dependency-injection layer. Conversely, do not collapse necessary trust or workload boundaries merely to keep the package count small.

Inspect actual versions and verify current official installation/migration instructions when changing a foundation. New dependencies should solve a named need and fit the runtime, peer versions, licensing and deployment constraints. Avoid opportunistic upgrades or `@latest` scaffolds over an existing app. Record meaningful choices and alternatives briefly when future maintainers need the reasoning.

Paid integrations, AI providers and identity/payment services require actual supported configuration and authorized credentials. Do not invent successful connections or store secrets in client-exposed values. A local mock should be clearly scoped and identified rather than silently becoming the product backend.
