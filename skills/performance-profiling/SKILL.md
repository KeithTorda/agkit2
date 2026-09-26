---
name: performance-profiling
description: Measuring and fixing web performance - Core Web Vitals targets (LCP, INP, CLS), the baseline-identify-fix-validate loop, Lighthouse audits, bundle size analysis, and DevTools runtime and memory profiling. Use when a page or app is slow, before a release, when Core Web Vitals or Lighthouse scores drop, or when deciding what to optimise first.
version: 2.5.0
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

`./scripts/lighthouse_audit.py <url>` runs Lighthouse against a running URL (mobile emulation by default; `--desktop` for the desktop preset) and compares the four category scores with thresholds: `--min-performance 50 --min-accessibility 80 --min-best-practices 80 --min-seo 80` by default. The summary shows each score against its minimum, the lab metrics (FCP, LCP, CLS, TBT, Speed Index; INP needs real interaction, so TBT is the lab proxy) and up to ten failing audits by title; `--json` prints the same as JSON. Exit 1 when a threshold is missed or the page could not be audited. It uses `node_modules/.bin/lighthouse` or one on `PATH` and never downloads it; when Lighthouse or Chrome is missing the result is `SKIPPED ... NOT VERIFIED` with the fix, and it exits 0 - a skip is not a pass, so list it under `Not verified:`. Install pinned to a major (`npm install -g lighthouse@12`); for a one-off audit outside the script, `npx lighthouse@latest <url>`. `--chrome-flags` defaults to `--headless=new`; add `--no-sandbox` only inside a container that cannot run the sandbox. `--timeout` defaults to 180 seconds.

`./scripts/bundle_analyzer.py <project>` inspects client build output without extra dependencies: Next.js `.next/static` and `out/_next/static`, Vite/Astro `dist`, Laravel Vite `public/build`, CRA `build/static`, React Router `build/client`, Nuxt `.output/public`, SvelteKit `.svelte-kit/output/client`. Server bundles and source maps are ignored. It lists JS and CSS assets with raw and gzip sizes and totals. High: a single asset over `--file-fail-kib` (default 750 KiB raw). Medium: an asset over `--file-warn-kib` (default 250 KiB), or total client JS over `--total-js-fail-kib` (default 2048 KiB; large apps may exceed it). Exit 1 only at or above `--fail-on` (default `high`). `--json` (or `--output json`) for JSON. Build first; with no build output it prints `SKIP ... NOT VERIFIED` and exits 0.

```powershell
python "KIT/skills/performance-profiling/scripts/lighthouse_audit.py" http://localhost:3000
python "KIT/skills/performance-profiling/scripts/bundle_analyzer.py" .
```

Both are advisory: report findings, fix the ones that fall under the project's stated performance budget, and ask before changes that alter design or scope.

## 6. Anti-patterns

Guessing instead of profiling; micro-optimising before the largest cost is fixed; optimising code that never runs on a hot path; trusting a fast laptop over throttled CPU and 4G presets; shipping without field data.
