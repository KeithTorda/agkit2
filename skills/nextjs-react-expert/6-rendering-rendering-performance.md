# Rendering, hydration and motion

Trace the actual browser cost before changing markup, hiding content or adding compositing layers. Preserve focus, semantics and the intended visual result.

## Rule 6.1: Animate the appropriate layer

Transforms/opacity often avoid expensive layout, but acceleration depends on browser, element and paint workload. SVG can support accelerated behavior; wrapping every SVG does not guarantee GPU acceleration. Profile the real effect and avoid unnecessary wrappers/layers or blanket `will-change`.

## Rule 6.2: Large content needs an appropriate strategy

`content-visibility` can defer offscreen rendering when browser support and accessibility behavior fit. Give a suitable intrinsic size where needed and check find-in-page, focus, print and layout jumps. It does not eliminate network/data/DOM cost. Virtualization can help large interactive collections but must preserve navigation, focus, semantics and variable-height behavior.

## Rule 6.3: Keep render work pure

Static JSX can be hoisted when it simplifies a proven hot path, but do not move values that depend on props/context or create shared mutable elements. A supported compiler may already optimize the case. Readability and identity semantics matter more than hoisting every element.

## Rule 6.4: Optimize vector assets without visible damage

Remove unnecessary metadata/precision through the project's asset pipeline when useful. Precision depends on viewBox, size and geometry; a universal one-decimal rule can distort artwork. Compare the actual rendered icon/illustration after optimization and preserve accessible names where needed.

## Rule 6.5: Align server and initial client output

Hydration mismatches often come from browser-only state, time/randomness, invalid nesting, locale or external DOM changes. Fix the cause and choose an explicit initial-state strategy. Prefer a server-known preference or a supported framework theme/init mechanism for flicker-sensitive UI.

An inline pre-hydration script may be appropriate in an established solution, but requires CSP/nonces, safe serialization and agreement with framework ownership. Do not inject unescaped storage values or manipulate arbitrary React DOM as a universal fix.

## Rule 6.6: Suppress only a known limited mismatch

Use framework-supported hydration suppression only for a narrow intentionally varying value whose consequences are understood. It does not repair a broken tree or establish correct content. Do not silence a broad mismatch or console error to pass a visual check.

## Rule 6.7: Hidden state has a lifecycle

CSS hiding, unmounting, tabs and supported React visibility APIs differ in effect, memory and focus behavior. APIs such as Activity require the installed React version and intended lifecycle semantics. Do not add a version upgrade solely to keep a small panel mounted. Ensure hidden interactive content is not accidentally focusable/read as active content.

## Rule 6.8: Render conditions explicitly

Avoid accidental numeric text from expressions such as `count && <List />` when zero should render nothing. Use `count > 0` or another explicit condition. Preserve meaningful zero values when zero is the correct UI, rather than treating every falsy value as missing.

## Rule 6.9: Pending state belongs to the operation

Use transition/action pending APIs when supported and semantically appropriate; ordinary request state may still be correct. A transition is not an automatic replacement for every loading flag or error handler. Guard duplicate submissions and show relevant pending/error/empty/success states.

## Check rendered behavior

Inspect relevant widths, keyboard focus, reduced motion, loading content and hydration/runtime errors. Compare the same interaction trace for performance claims. A smoother animation cannot justify missing content, inaccessible controls or weakened state correctness.
