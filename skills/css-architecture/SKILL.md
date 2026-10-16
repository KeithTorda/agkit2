---
name: css-architecture
description: "Organize and repair CSS using the existing styling system, ownership boundaries, cascade, semantic tokens, component variants and responsive constraints. Applies to plain CSS, SCSS, modules and utility frameworks without requiring a migration."
version: 2.8.2
---

# Maintainable styling

Make a future change easy to locate and reason about. Follow the project's supported styling approach: plain CSS, SCSS, modules, CSS-in-JS, utilities, or a component theme can all work. Improve the affected boundary without migrating the project for a local repair.

## Find the owner

Before adding a rule, inspect the rendered element, owning component, token source, imports, and winning declarations. Identify whether the decision belongs to a semantic token, element default, reusable component/variant, layout, page, or runtime value. Shared behavior should have an understandable owner; intentional responsive and theme overrides may have multiple declarations.

Fix the cause rather than adding contradictory patches. A parent constraint, an inherited token, library configuration, or an animation may own the behavior. Co-locate rules where the project expects them. A small static page can use one stylesheet; a large application may need layers, modules, and separate theme sources generated from a common input.

## Cascade decisions

- Inspect origin, importance, cascade layers, specificity, scoping and source order before increasing specificity.
- With layers, declare intentional order before imports. Normal unlayered author CSS outranks normal layered rules; important layer precedence reverses. A blanket rule that later layers always win is inaccurate.
- Place vendor styles into a controlled layer when the build and library permit. Otherwise use its configuration, supported theme API, or a narrow documented override.
- `!important`, inline styles, descendant selectors and variants have legitimate roles. Avoid using them to conceal an unexplained conflict; choose the least fragile remedy for the real integration.

For example, a transformed ancestor can contain a dropdown beneath another stacking context. Raising the dropdown number repeatedly will not escape that context; fix the ancestor's role or use the product's overlay mechanism.

## Tokens, variants, and local values

Reuse semantic decisions that need coordinated change: surfaces, text, status, focus, spacing relationships, shape, elevation, and motion. Preserve approved materials such as gradients or glass. Do not create a universal neutral palette or a dark theme as an architecture task.

Tokenize because a value expresses a reusable decision, not merely because the same number occurs twice. A purposeful one-off, fluid calculation, inherited section role, or runtime position can remain local. Avoid redundant token sources that drift; generated platform outputs or explicit theme mappings are not automatically duplication.

Use component variants for meaningful supported differences. A layout may still legitimately constrain a child; avoid turning every local adjustment into a global variant. Prefer names and scopes that explain ownership, following existing conventions. In new plain CSS, component-prefixed naming is a useful option, not a forced BEM migration.

## Responsive and cleanup workflow

Use content-driven constraints, intrinsic sizing, grid/flex, wrapping, and suitable queries. Inspect `min-width`, `min-height`, overflow, actual containing blocks and viewport-unit behavior. `svh`, `dvh`, `%`, and content-sized layouts suit different needs; fixed heights are appropriate only when the content contract supports them.

Remove rules made obsolete by the change after searching their callers, including generated templates and script-added classes. Do not delete shared styling because one route does not use it. Keep imports, selectors, keyframes and custom properties consistent.

Run the project's relevant style/build checks and inspect the affected render with `browser-verification`. The optional `KIT/scripts/css_audit.py` and `KIT/scripts/naming_check.py` helpers provide source heuristics; read findings in context before using strict modes. Repeated declarations, inline values, or unresolved runtime variables may be intentional. Static color-pair scans cannot establish contrast over actual media or effects.

Read [plain-css.md](plain-css.md) for plain CSS/SCSS organization. Use `tailwind-patterns` for the installed Tailwind version, `ui-repair` for reproduced layout defects, and `design-spec` when documenting a substantial visual system.
