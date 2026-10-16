---
part: 33
title: Naming and project organization
covers: filenames, folders, domain terms, variables, functions, components, assets, configuration, imports, scaffolds, cleanup
---

# 33 - Naming and project organization

Read when scaffolding, naming, or cleaning a project. Favor discoverability and the repository's conventions. A folder or variable is not wrong merely because a generated project also uses it.

## Follow actual responsibilities

Use names that help a maintainer predict purpose: `calculateInvoiceTotal`, `ResidentSearch`, or `paymentWebhook` can be clearer than a vague `processData`. Short local names such as `i`, `x`, `data`, or `result` can be entirely appropriate where their scope and meaning are obvious. Do not mechanically rename every conventional term.

Use domain language consistently across UI, types, APIs, and persistence while respecting external contracts. Do not translate a real identifier or official term merely to make it stylistically uniform. Preserve names, codes, and leading zeros accurately.

Organize by features, layers, or framework routes according to the project. A small app may be flat; a large system may need deeper structure. No universal folder-depth limit applies. Avoid empty speculative hierarchies and multiple overlapping shared folders when their boundaries are unclear, but retain legitimate public APIs and package boundaries.

## Files, functions, and types

Use the existing casing, extension, and suffix conventions. Components, tests, migrations, generated files, and platform routes may have meaningful naming requirements. Classes ending in `Service`, `Manager`, or `Handler`, interface prefixes, and file names such as `index.ts` are not automatically wrong; evaluate whether they express a useful contract in this codebase.

Function names should reflect effects and results. Avoid a name that suggests pure calculation while it sends mail or writes data. Boolean names should make conditions readable. Types should describe the real model rather than a misleadingly broad abstraction. Do not rename a public interface casually because another name sounds cleaner.

Asset names should be identifiable enough for maintenance. Build hashes, camera names, and generated filenames can be valid provenance; a descriptive exported name can help when the asset is part of a permanent system. Renaming must update all references and respect caching, attribution, and generated build behavior.

## Imports and configuration

Barrel files can create a clear module boundary or cause cycles and unwanted bundle expansion. Keep them when useful and inspect actual dependency behavior. Do not require or ban them across every project.

Keep environment variable names aligned with the framework and exposure boundary. Vite's public values and Next's public values have different naming conventions; inspect the actual stack. Never put a secret under a client-exposed prefix. `.env.example` should document required values using safe placeholders, with useful source/setup context.

Multiple config files or lockfiles may belong to a monorepo or several deployable packages. Investigate ownership before deletion. Remove stale copies only after understanding their callers. Do not remove a CI workflow merely because it currently fails; fix it or report the real failure within the task's scope.

## Scaffolds and cleanup

Review starter logos, default titles, demo routes, unused widgets, placeholder text, copied policies, and obsolete deployment targets. Keep a demonstration route when it is an intentional supported feature; protect internal tools appropriately. A prototype may deliberately retain sample content if it is labeled.

Versioned duplicates such as `ButtonNewFinal.tsx` often indicate unresolved ownership; determine which file is actually used and migrate references before removing anything. Do not delete user data, unrelated files, ignored assets, or unfamiliar generated artifacts to make the tree look tidy.

## Review

Check import resolution, external contracts, route conventions, build references, environment exposure, and actual ownership before renames or deletion. Confirm the tree makes the changed responsibility easier to find. A clean-looking file list is not proof of functional correctness.
