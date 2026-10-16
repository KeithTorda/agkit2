---
part: 34
title: Performance, discovery, and themes
covers: images, fonts, bundles, dependencies, third parties, layout shift, fetching, caching, deployment, SEO, indexing, structured data, theme behavior
---

# 34 - Performance, discovery, and themes

Read when adding media, fonts, dependencies, external scripts, public metadata, or themes. Measure actual costs and follow the selected direction. Rich visuals and good performance can coexist; a blanket ban on animation or imagery is not a performance strategy.

## Assets and bundles

Choose image formats and quality from content, display size, transparency, decoding, and support. Provide responsive sources, dimensions/aspect ratios, and an appropriate loading strategy. Prioritize the actual likely LCP asset; defer below-fold images when useful. Do not lazy-load all images by reflex or preload every resource at once.

Load font families, subsets, and weights the design uses. Preserve language coverage and legible fallbacks. Compare variable and static files by real payload. Avoid unnecessary font flashes or layout shift through appropriate fallbacks, metrics, and loading strategy. There is no universal font-weight count limit.

Use suitable icon delivery. A full icon font for a few glyphs may be wasteful; an existing cached system can be a reasonable choice. Tree-shaken SVG imports, sprites, and local assets can help. Check actual output rather than assuming every package tree-shakes correctly.

Choose dependencies from required behavior, accessibility, maintainability, licensing, and bundle cost. A rich animation or 3D runtime may be justified by the chosen experience; a tiny effect may not need another library. Reuse the existing supported stack where practical. Follow the project's package policy, pin appropriate versions, and avoid shipping development CDN tooling as a production assumption.

## Rendering, data, and third parties

Reserve space for media, fonts, banners, and async regions to reduce layout shift. Loading feedback should reflect actual latency and state. Avoid an artificial preloader that hides already available content solely to showcase an effect.

Fetch needed fields and ranges, paginate large results, cache according to freshness and identity, and avoid duplicate requests. Private responses must not leak through a shared public cache. Handle stale data and retry honestly. Measure the important user flow on representative devices/networks when possible.

Third-party analytics, chat, maps, and video have cost and privacy effects. Defer or load on interaction where appropriate, without making a required feature impossible to discover. Multiple tools may serve distinct approved purposes; inspect overlap rather than enforce a fixed tool count.

## Build and deployment

Run the appropriate production build and inspect relevant warnings, asset paths, environment configuration, routes, and headers. Fingerprinted assets can use long immutable caching; HTML and private data need different policies. Avoid treating a local dev server as proof of deployment correctness. Publish or deploy only within the user's authorized scope.

## Search and sharing

Public pages need accurate titles, descriptions, canonical URLs, content, status codes, and share metadata where relevant. Avoid leaving preview hosts, starter titles, missing pages returning fake success, or accidental production `noindex` directives. Conversely, private admin and sensitive pages should not become indexable just to satisfy a marketing checklist.

A sitemap should reflect intended public canonical pages; robots rules express crawler preference and do not secure private content. Use actual authentication for protected data. Structured data must describe real content and supported types, not invented ratings, events, products, or local-business facts. Validate relevant structured data and share previews when in scope. See part 08 for wording.

## Theme behavior

Build the theme modes the user or product needs. A light-only, dark-only, mixed-section, or adaptive design can be valid. Do not add both themes or a toggle by default. A dark section within a light page is a composition choice, not necessarily a global theme change.

If multiple user themes are supported, respect an explicit choice and provide system behavior only where part of the product. Persist and apply the preference coherently, handle hydration/first paint, and verify all states and third-party surfaces. Do not invert the entire document as a shortcut; use intentional values and asset variants. Print output needs its own readable, practical treatment, especially documents and receipts.

## Review

Inspect the actual build and critical paths for transfer, loading, shift, interaction, indexing intent, and supported theme states. Report measurements and environments actually checked. A high performance score alone does not establish visual quality, accessibility, or correct business behavior.
