# Plain CSS and SCSS

Use the project's established stylesheet conventions. Plain CSS with custom properties, CSS modules, component-prefixed selectors, SCSS partials or a small layered entrypoint can all be maintainable. Do not require Sass, BEM, a fixed partial tree or a framework migration for a local change.

## Ownership and imports

Start with the actual import graph and winning rules. Keep global resets/base defaults narrow, shared semantic decisions in the existing token source, and component/page rules near their owners. A small site may need one file; split when responsibilities become hard to locate. Import each intended source once and investigate duplicate resets before removing them.

If cascade layers are useful, establish their order deliberately. For example:

```css
@layer reset, vendor, base, components, utilities;
@import url('./vendor.css') layer(vendor);
@layer base {
  *, *::before, *::after { box-sizing: border-box; }
}
@layer components {
  .invoice-table { width: 100%; border-collapse: collapse; }
}
```

Adapt this to actual browser/build support and import rules. Normal unlayered CSS outranks normal layered CSS; important declaration precedence reverses across layers. Layers are optional when existing scoping already gives clear ownership.

## Reuse without rigidity

Use semantic custom properties for decisions that change together. Component-prefixed naming can avoid collisions, but preserve a coherent existing convention. Scope global element styles so an embedded editor or administrative screen does not inherit a marketing reset unexpectedly.

```css
.report-panel {
  --report-panel-gap: clamp(1rem, 3vw, 2rem);
  display: grid;
  gap: var(--report-panel-gap);
  color: var(--text-primary);
  background: var(--surface-raised);
}
```

A local responsive calculation is not automatically a missing global token. Intentionally inherited variables can create section themes without duplicating a full palette. Document one-off vendor overrides when their source cannot be changed.

With SCSS, follow installed module support (`@use`/`@forward` when suitable), existing build order and framework integration. Do not rewrite an older import system during a narrow repair unless necessary. Keep nesting shallow enough that selector ownership stays clear; a fixed nesting-depth number is not the measure of quality.

After an edit search markup, script-added classes and template consumers before removing old rules. Run appropriate build/style checks and inspect the affected render, including state and responsive behavior. Source auditors are heuristics, particularly around runtime variables, themes, third-party CSS and contrast.
