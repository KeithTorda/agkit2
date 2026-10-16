---
name: seo-fundamentals
description: Improve technical discoverability and accurate page metadata, indexing, structured data and search-oriented content. Use for SEO audits or implementation; treat ranking and AI citation claims as hypotheses requiring evidence.
version: 2.8.2
---

# Search Discoverability

Identify which pages should be public and indexable, who the intended reader is and what the page actually answers. Preserve content accuracy and user value. Search ranking, rich results and AI citations cannot be guaranteed by a checklist or heuristic score.

## Technical page contract

- Important pages return meaningful content and correct HTTP statuses. Check rendered HTML when client rendering, authentication or middleware may obscure it.
- Use distinct, descriptive titles and useful descriptions. Character-count heuristics are not hard limits; quality and snippet rendering depend on content and search context.
- Use headings that express a logical content structure. A clear main heading is useful; do not manufacture sections or rewrite a valid document solely to satisfy a counter.
- Canonicals express actual preferred duplicates. Sitemap entries should be intended canonical, indexable URLs; omit private/error/redirect URLs. Keep deliberate `noindex` decisions intact.
- `robots.txt` controls crawling and is not access control. Blocking crawling can prevent a crawler from seeing `noindex`. Protect private data with authorization.
- Preserve stable URLs and redirect intentionally moved content. Meaningful removed resources may correctly return 404/410; do not redirect everything to the homepage.
- Provide accurate language/direction, useful link text and appropriate image alt text; decorative images use empty alt. Performance/mobile usability affects the experience, not a promise of ranking.

## Metadata and structured data

Follow the framework's metadata mechanism and verify actual output, including nested routes and environment-specific hosts. Avoid development origins in canonical, sitemap and share URLs. Social previews need accessible absolute assets and accurate content; inspect the target platform when exact requirements matter.

Use schema types that describe visible real content. Validate against current official schema/search-provider documentation for the requested feature. Do not invent ratings, authorship, FAQs or credentials to obtain rich results. Valid JSON-LD does not ensure rich-result eligibility.

## Content and AI-oriented discovery

Answer the reader's question clearly with supported claims, useful structure and attributable sources where appropriate. Do not force every page into FAQ/list/table patterns or keyword repetition. Author/date information belongs where truthful and relevant.

AI crawler rules, robots tokens and use policies change. When configuring a named provider, consult its current official documentation and the user's publication preferences. Distinguish training controls, search discovery and user-triggered fetch; do not copy a stale bot table or imply one directive governs all uses.

Measure coverage with actual rendered checks, indexing/search-console evidence and appropriate analytics over time. Citation-oriented readability is a content hypothesis, not a guarantee of inclusion by any AI service.

## Existing helpers

```powershell
python "KIT/skills/seo-fundamentals/scripts/seo_checker.py" .
python "KIT/skills/seo-fundamentals/scripts/geo_checker.py" .
```

`seo_checker.py` reports source-level title, description, heading, canonical, social and indexing patterns. Supports `--json`, `--verbose`, `--fail-on error|warning|never`. Its missing-title or noindex findings require rendered/context review.

`geo_checker.py` scores citation-oriented source heuristics and supports `--json`, `--verbose`, `--min-score`. Its score is advisory; do not add fabricated content or block delivery to satisfy it. Neither helper verifies live indexability, ranking, legal crawler compliance or actual AI citations.
