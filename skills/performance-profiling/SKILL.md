---
name: performance-profiling
description: Measuring and fixing web performance - Core Web Vitals targets, the baseline-identify-fix-validate loop, Lighthouse 12 audits, bundle size analysis, and DevTools runtime and memory profiling. Use when a page or app is slow, before a release, when Core Web Vitals or Lighthouse scores drop, or when deciding what to optimise first.
version: 2.0.0
---

# Performance Profiling

Measure, find the largest bottleneck, fix that one thing, measure again. Framework-specific fixes are in `@[skills/nextjs-react-expert]`; this skill is about measurement and prioritisation.

## 1. Core Web Vitals

| Metric | Good | Poor | Measures |
|--------|------|------|----------|
| LCP | < 2.5 s | > 4.0 s | Loading of the largest visible element |
| INP | < 200 ms | > 500 ms | Responsiveness to interaction |
| CLS | < 0.1 | > 0.25 | Visual stability |

Lab data (Lighthouse, local DevTools) finds problems; field data (Search Console, RUM such as Vercel Speed Insights or web-vitals reporting) tells you which ones users hit. Fix LCP first, then CLS, then INP.

INP is the hardest to chase because it fires on one specific interaction you have to catch in the act. Instrument it in the field with `web-vitals` v4+ (the `web-vitals/attribution` build): attribution names the element and the phase, so you fix the slow interaction instead of guessing from a p75 number.

```js
import { onINP } from "web-vitals/attribution";
onINP(({ value, attribution: a }) => {
  // a.interactionTarget → the element that was slow; a.interactionType → 'pointer' | 'keyboard'
  // a.inputDelay / a.processingDuration / a.presentationDelay → which phase cost the time
  // a.longAnimationFrameEntries → the long task (LoAF) that blocked the main thread
  report({ inp: value, ...a });
});
```

Reproduce it locally in the DevTools Performance panel: record, use the Interactions track to find the offending interaction, and read the long task blocking the main thread beneath it.

## 2. Loop

Measure first — let the profile name the largest cost; never optimise from a hunch.

1. Baseline: record Lighthouse scores and Web Vitals before touching code, under a throttle that matches your field data (mobile CPU 4–6×, 4G) so every number is comparable.
2. Identify: pick the single largest cost (DevTools Performance for long tasks over 50 ms, Network for blocking requests, Coverage for unused JS/CSS, Memory for growing heaps and detached DOM nodes).
3. Fix: one targeted change.
4. Validate: re-measure under the same throttle; keep the change only if the target metric moved, revert if it did not.

Common causes by symptom: slow first load means large JS or render-blocking resources; slow interactions mean heavy event handlers or main-thread work; scroll jank means layout thrashing or scroll listeners in React state; growing memory means retained references or uncleaned subscriptions.

## 3. Quick wins in priority order

Compression (Brotli) and caching headers for static assets, `next/image` or sized lazy images, route-level code splitting and dynamic imports for heavy components, preloading the LCP image and fonts, reserving space for media to stop layout shift, removing or deferring third-party scripts.

## 4. Bundle analysis

Look for one oversized dependency at the top of the chunk list, duplicated packages across chunks (dedupe, align versions), routes bundled into the main chunk (split), and unused exports (tree-shake, avoid barrel imports).

## 5. Scripts

`./scripts/lighthouse_audit.py <url>` runs the Lighthouse CLI in headless Chrome against the URL, then applies thresholds: `--min-performance 50 --min-accessibility 80 --min-best-practices 80 --min-seo 80` by default; below a threshold returns exit code 1. It reports the four category scores and LCP, CLS, INP, and TBT values as JSON. Chrome runs with its sandbox on; do not add `--no-sandbox`. The script needs the Lighthouse CLI resolvable on PATH: install it pinned to a major (`npm install -g lighthouse@12`), since a bare `npm install -g lighthouse` freezes at whatever was current the day you ran it and never updates. For a one-off audit outside the script, run the latest without installing anything: `npx lighthouse@latest <url>`.

`./scripts/bundle_analyzer.py <project>` inspects built output (`.next/static`, `dist`, `build/static`, `build/assets`, `out/_next/static`) without extra dependencies, listing JS and CSS assets with raw and gzip sizes. Defaults: warn above 250 KiB per file, fail above 750 KiB per file or 2 MiB total JS (`--file-warn-kib`, `--file-fail-kib`, `--total-js-fail-kib`, `--fail-on`). Build first; with no build output it prints a skip notice.

```powershell
python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/skills/performance-profiling/scripts/lighthouse_audit.py http://localhost:3000
python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/skills/performance-profiling/scripts/bundle_analyzer.py .
```

Both are advisory in the checklist: report findings, fix the ones that fall under the project's stated performance budget, and ask before changes that alter design or scope.

## 6. Anti-patterns

Guessing instead of profiling; micro-optimising before the largest cost is fixed; optimising code that never runs on a hot path; trusting a fast laptop over throttled CPU and 4G presets; shipping without field data.
