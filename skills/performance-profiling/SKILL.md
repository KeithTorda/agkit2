---
name: performance-profiling
description: Diagnose and improve measured page, server, bundle, interaction or memory performance with comparable evidence. Use for real slowdowns, regressions or performance targets; avoid speculative optimization and score-only claims.
version: 2.8.2
---

# Performance Profiling

Define the user-visible problem before optimizing. Capture a representative URL/action, environment, data volume and target. Separate slow first load, server response, interaction, animation, query cost and memory growth; they need different evidence.

## Establish a comparable baseline

Use available field telemetry to identify affected users/devices and percentile behavior. Reproduce in a controlled local/lab setup with recorded browser/runtime, build mode, cache state, network/CPU conditions and test data. Development builds are not reliable production-size baselines.

Use repeated comparable runs when normal noise could obscure the effect. Report absolute measurements and variation rather than a single score. Lab tests can explain a cause; they do not prove field performance for all users.

## Investigate the dominant cost

| Symptom | Useful evidence |
|---|---|
| Slow response | Server trace, external dependency timings, query plan, cold-start/runtime profile |
| Slow visible content | Request waterfall, critical resource timing, image/font behavior, rendering trace |
| Input lag | Main-thread long tasks, component profile, handler work, layout/paint cost |
| Scroll/motion jank | Frame trace, style/layout/paint work, listener frequency, compositing evidence |
| Growing memory | Repeated-flow heap comparison, retained objects, detached nodes, listener/subscription cleanup |
| Large client payload | Production asset/route analyzer, transfer/compressed size, module ownership and actual usage |

For web experience, distinguish LCP/loading, INP/interaction and CLS/stability. Verify current definitions/thresholds from official documentation if the task requires a compliance-style target. Lighthouse's total blocking time is a diagnostic, not the same metric as field INP.

## Change a causal bottleneck

Choose a bounded change linked to evidence. Parallelize independent authorized I/O; remove accidental N+1; resize important images; defer genuinely unused widgets; reduce demonstrated render/layout work. Verify that a cache, deferred resource or concurrency change preserves freshness, isolation, accessibility and dependency capacity.

Re-measure under comparable conditions and test changed behavior. If the target does not improve, examine noise/hypothesis and keep only a separately justified change. Avoid merging unrelated optimizations that prevent attribution. Small correctness improvements need not be discarded merely because a speed claim failed.

## Existing helpers

```powershell
python "KIT/skills/performance-profiling/scripts/lighthouse_audit.py" http://localhost:3000
python "KIT/skills/performance-profiling/scripts/bundle_analyzer.py" .
```

`lighthouse_audit.py` uses installed Lighthouse/Chrome and never downloads them. Supports `--desktop`, `--json`, `--timeout`, `--chrome-flags` and `--min-performance`, `--min-accessibility`, `--min-best-practices`, `--min-seo`. Defaults are advisory kit budgets, not universal quality requirements. A missing tool produces SKIPPED/NOT VERIFIED even with exit zero. Keep the browser sandbox unless the actual environment requires otherwise.

`bundle_analyzer.py` inspects existing production client build output and reports raw/gzip assets; it is not route-level executed JS. Supports `--json`, `--output`, `--file-warn-kib`, `--file-fail-kib`, `--total-js-fail-kib`, `--fail-on`. Missing output is a skip. Choose budgets from the product/context instead of treating defaults as guarantees.

Report the bottleneck, before/after evidence, behavioral checks and material measurement limits. Never call a clean report proof that an app is fast.
