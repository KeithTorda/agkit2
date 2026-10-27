---
name: tailwind-patterns
description: "Implement and maintain Tailwind styling in the version actually installed. Covers version-aware setup, semantic theme mapping, responsive and state variants, class discovery, component reuse and deliberate migration without choosing the visual direction."
version: 2.8.2
---

# Tailwind in the existing project

Translate the approved design using the installed Tailwind version and the project's existing build pipeline. This skill does not select a visual style, require Tailwind, or authorize a version migration. Read the manifest, lockfile, CSS entrypoint, config, plugins and representative components before changing syntax.

## Match the version

Tailwind v3 commonly uses JavaScript configuration and `@tailwind` directives. v4 uses a CSS-first `@import "tailwindcss"` setup with theme variables and supported integration packages. Keep a working v3 project on compatible syntax unless migration is actually requested or necessary. Check official version-specific docs before a new install or configuration change.

For v4, inspect whether the project uses the Vite integration, PostCSS integration or another supported path; do not install both by habit. Legacy JavaScript configuration may coexist through supported compatibility mechanisms. Generated output/config must derive from an understandable source rather than drift independently.

## Semantic roles and local values

Reuse existing roles and agreed tokens. A v4 example, with values chosen for the actual design:

```css
@theme inline {
  --color-surface: var(--surface);
  --color-on-surface: var(--on-surface);
  --color-action: var(--action);
}
:root {
  --surface: #fbfaf7;
  --on-surface: #1a1c1e;
  --action: #194b3a;
}
```

Then `bg-surface text-on-surface` uses semantic decisions. Map font families, text size, spacing, radius and motion through supported namespaces when reuse helps. Do not reset an entire default scale just to add a token. An arbitrary value or inline custom property can be correct for a one-off, calculated layout or dynamic position; repeated numbers alone do not require a new token.

Theme scope comes from the brief and existing product. If multiple themes exist, preserve its single switch mechanism and semantic overrides. v4 can define a manual dark variant with `@custom-variant`; v3 uses its supported config. Do not add a toggle or dark palette to a single-theme task. Section contrast can inherit local semantic variables without changing the global preference.

## Layout and state

Use content-driven breakpoints and intrinsic layout. Base/unprefixed utilities are not intrinsically “phone-only”; they apply until overridden. Container queries can help reusable components adapt to their own width when supported. Use grid for two-dimensional relationships, flex for one-dimensional flow, and native layout where appropriate.

Check shrinkability (`min-w-0`/`min-h-0`), overflow boundaries, wrapping and readable content before compensating with arbitrary widths. Choose `svh`, `dvh`, ordinary viewport units or content sizing from the desired browser behavior. A viewport-height utility is not categorically wrong, but fixed height can clip real content or interact poorly with mobile browser UI.

Provide focus-visible, selected, disabled, invalid and pending states relevant to the actual control. Keep hover enhancements available to keyboard/touch equivalents. Apply `motion-reduce`/`motion-safe` or the existing motion approach without leaving essential content hidden when effects are skipped.

## Class discovery and reuse

Ensure the compiler sees complete class names. Prefer a finite mapping such as `{ success: 'text-success', error: 'text-error' }` instead of `text-${status}`. Use the installed version's source inclusion/safelist mechanism when classes originate outside normal scanning. Verify emitted CSS when a class appears to do nothing.

Extract components or variants when they express stable behavior or a reusable design contract, not when a repetition counter reaches a fixed number. Use existing conditional/merge helpers; add a class-composition package only for a concrete need. Remember that conflicting utility classes are resolved by generated CSS and variant ordering, not simply the last string in markup.

For a conflict, inspect the cascade, layers, specificity, imports and computed value. Avoid repeated `!` modifiers as unexplained patches; narrow overrides are valid when a vendor boundary genuinely requires them. See `css-architecture` for ownership.

## Deliberate migration and verification

For an authorized version migration, check browser support, plugins, theme/config compatibility, reset/default changes, class/variant changes and build integration. Use the official migration tooling appropriate to the actual versions, review its changes, and preserve a recoverable baseline. Do not copy upgrade commands blindly from this skill.

When the user asks for checks, run relevant build checks and, if requested, inspect the browser output. Compilation proves class generation, not visual quality. Report the installed version, meaningful configuration changes and actual validation when they matter to the handoff.
