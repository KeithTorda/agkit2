# Client payload and module loading

Inspect production build output and the route's real network/module profile. Source import count is not bundle size. A server-only dependency, cached chunk and initial client dependency have different user costs.

## Rule 2.1: Inspect package entry points

Barrel exports can increase development graph traversal or bundle work, but do not automatically include an entire library. Tree-shaking depends on module format, side-effect metadata, bundler and actual usage. Check analyzer output before replacing every ergonomic import.

Use supported package subpaths when they reduce the measured cost and preserve public API compatibility. Do not import undocumented private files. Framework import-optimization lists/options vary by version; verify installed behavior rather than assuming a library is or is not automatically optimized.

## Rule 2.2: Load optional features deliberately

A dynamic import can defer optional code until needed. Choose a supported framework mechanism and preserve loading/error states. Confirm it creates the intended chunk and does not move essential work into a later waterfall.

```ts
async function exportWhenRequested(rows: ExportRow[]) {
  const { createExport } = await import('./export-client')
  return createExport(rows)
}
```

This illustrates an on-demand module boundary; the actual data handling, error UX and browser/runtime support still need implementation. A shared statically imported dependency may remain in the initial bundle.

## Rule 2.3: Third-party work needs a purpose

Defer analytics/chat/widgets according to product needs, consent and supported platform APIs. Do not embed an arbitrary script to improve a score. Evaluate network, CPU and privacy/credential exposure separately. When a client-only widget cannot render on the server, isolate it in an appropriate client boundary using supported configuration.

## Rule 2.4: Split heavy interaction by usage

Editors, maps, charts and media tools can be useful loading boundaries when absent from the primary task. Keep important visible content discoverable and accessible before the feature loads. Client-only rendering flags and dynamic-import APIs are version/router-specific; a server component cannot necessarily use the same options as a client module.

Do not split tiny components into many chunks without evidence; request overhead and late loading can outweigh savings. Verify repeat navigation and failed-chunk recovery as well as first load.

## Rule 2.5: Preload with a budget

Intent-based preload on focus, hover or a likely next step can reduce delay when the feature is likely to be used. It consumes bandwidth/CPU and should respect the app's device/network constraints. Do not preload every deferred feature and recreate the original cost.

## Validate the change

Compare equivalent production builds, route transfer/compressed size, executed JS and load/interaction timing. Ensure dependencies were not merely shifted to a later blocking request. Preserve module side effects and expected exports. Use `performance-profiling` for measurement and `frontend-architecture` for meaningful server/client ownership.
