# Measure mobile performance where it matters

Identify the reported symptom and target: startup, list scrolling, gesture responsiveness, a transition, network wait, memory or battery. Frame budgets vary by refresh rate: about 16.7 ms at 60 Hz and 8.3 ms at 120 Hz. Those arithmetic budgets do not guarantee a particular device can sustain every effect. Use representative hardware and a release/profile build where possible, with realistic data.

## Lists and images

Virtualize growing or large datasets using a supported list implementation. Existing FlatList, FlashList, native collection views or Flutter lazy builders can all be appropriate. A small fixed set in an ordinary scroll view is not inherently a bug. Third-party recycling packages have version/architecture requirements; do not force one to satisfy the kit.

Use stable item identity when records reorder or mutate. Supply known fixed layout only when it is actually fixed, accounting for text scaling and variable content. Tune list windows, batching and clipping from measured behavior; copying aggressive defaults can produce blank cells or accessibility problems.

Decode images near the required display dimensions, reserve layout space, use suitable formats/cache behavior and bounded prefetch. Native/Flutter built-in image components can be sufficient; a cache package is optional. Large decoded images can consume much more memory than compressed download size.

## Work and rendering

Profile before adding broad memoization. The React Compiler and React Native architecture are separate concerns; inspect the actual build if compiler behavior matters. Memoize measured expensive work or unstable boundaries, preserving correctness. Flutter `const` can reduce work for eligible subtrees, but does not mean a widget never participates in layout/paint or that state changes cannot affect its surroundings.

Use animation APIs compatible with the installed runtime and property. The React Native native driver supports a subset; layout or gesture needs may justify another runtime. Do not enable `useNativeDriver` for unsupported properties or assume every Reanimated property is cheap. Flutter/native rendering differs from browser compositor rules; “only transform and opacity use the GPU” is not a universal mobile rule.

Keep expensive computation, decoding and unnecessary repeated fetches away from interaction paths where possible. Scope state updates and rebuilds. Clean up subscriptions, timers, observers, controllers and queued callbacks; bound caches and retained objects.

## Network and battery

Use appropriate payloads, pagination, image variants, caching and cancellation. Avoid aggressive polling or redundant background work; push also has delivery/battery constraints. Do not run continuous offscreen decoration without a reason. Measure the actual bottleneck rather than declaring all WebSockets or animation expensive by category.

## Evidence

Capture the tool/build/device, dataset, reproduction, baseline and measured change. Inspect frame timelines, CPU/memory or network traces relevant to the symptom. Recheck the user flow after optimization; smoother scrolling with missing rows is a regression. State simulator/dev-mode limits and avoid unsupported universal startup, FPS or “never drops a frame” claims.
