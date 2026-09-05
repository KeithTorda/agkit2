---
name: seo-fundamentals
description: Search and AI-answer visibility for web pages - technical SEO, E-E-A-T, Core Web Vitals, structured data, and generative engine optimisation (GEO) for ChatGPT, Claude, Perplexity, and Gemini, plus AI-crawler access rules. Use when adding meta tags, sitemaps, or schema, fixing Core Web Vitals, writing content meant to rank or be cited, or configuring robots.txt for AI bots.
version: 2.0.0
---

# SEO and GEO Fundamentals

Two audiences read a page: search crawlers that rank it, and AI answer engines that quote it. They share one foundation — fast, accessible, well-structured HTML — but they reward different work, and the decisions split cleanly:

- **Technical SEO** decides whether the page can be *crawled, indexed, and deduplicated*: content in the server-rendered HTML, one canonical URL, a correct `sitemap.xml` and `robots.txt`, valid structured data. Get these wrong and nothing ranks — but on their own they earn no AI citation.
- **GEO** decides whether a passage can be *lifted and attributed*: self-contained answers, clear definitions, original data and numbers, visible author and dates, and entities a knowledge graph can consolidate. This is invisible to classic ranking, yet it is what makes ChatGPT, Claude, Perplexity, and Gemini quote you.

They rarely conflict; when they do, indexable HTML wins, because an engine cannot cite a page it cannot fetch. Ownership and the build process are in `agents/seo-specialist.md`; this skill is the shared reference for both.

## 1. Technical baseline

| Element | Rule |
|---------|------|
| Title | One per page, 50-60 characters, primary topic first, unique across the site |
| Meta description | 150-160 characters, states the benefit; not a ranking factor but drives clicks |
| Headings | One `h1`; `h2`-`h4` form a logical outline that reads as a table of contents |
| Canonical | `<link rel="canonical">` on every indexable page; self-referencing by default |
| Sitemap and robots | `sitemap.xml` listing canonical URLs; `robots.txt` only blocks what must not be indexed |
| URLs | Lowercase, hyphenated, stable; redirect (301) old URLs instead of leaving 404s |
| Images | Descriptive `alt` for meaningful images; `alt=""` is correct for decorative ones |
| Open Graph / Twitter | `og:title`, `og:description`, `og:image` (1200x630) so shares render a card |
| HTTPS, mobile | Required; mobile rendering is what Google indexes |

Next.js: use the `metadata` export or `generateMetadata()` per route, `app/sitemap.ts` and `app/robots.ts`, and `next/image` for sized, lazy images.

## 2. Core Web Vitals

| Metric | Good | Measures |
|--------|------|----------|
| LCP | under 2.5 s | Loading of the largest visible element |
| INP | under 200 ms | Responsiveness to interaction |
| CLS | under 0.1 | Visual stability |

Measure with PageSpeed Insights (field data) and Lighthouse 12 (`@[skills/performance-profiling]`); fix in the order LCP, CLS, INP. Preload the hero image and fonts, reserve space for media, and keep third-party scripts off the critical path.

## 3. Content that ranks and gets cited (E-E-A-T)

- Experience and expertise: first-hand detail, real numbers, screenshots, named author with credentials and an author page (`Person` schema).
- Authority: earn links and mentions; keep entity facts (name, address, founding date) consistent everywhere so knowledge graphs consolidate them.
- Trust: visible dates (`datePublished`, `dateModified`), sources for statistics, contact and policy pages, HTTPS.
- Structure for extraction: a two-sentence summary at the top, question-form headings, a definition where a term is introduced, comparison tables, step lists, and a short FAQ. AI engines lift self-contained passages; make each section answer one question completely.
- AI-assisted drafts are fine when a human edits, verifies, and adds original insight; raw generated text with no new information is what gets filtered.

## 4. Structured data

Use JSON-LD in the page head. Common types: `Article`/`BlogPosting` (with `author`, `datePublished`, `dateModified`), `Organization`, `Person`, `Product` (with `offers`), `FAQPage`, `HowTo`, `BreadcrumbList`. Only mark up content that is visible on the page. Validate with the Rich Results Test.

## 5. AI crawler access

Decide per bot whether you want training use, search indexing, or user-triggered fetches. Current user agents:

| Bot | Operator | Purpose |
|-----|----------|---------|
| `GPTBot` | OpenAI | Model training; block to opt out of training |
| `OAI-SearchBot` | OpenAI | ChatGPT search results and citations |
| `ChatGPT-User` | OpenAI | Fetches a page when a user asks about it |
| `ClaudeBot` | Anthropic | Crawling for training |
| `Claude-SearchBot` | Anthropic | Search index used for citations |
| `Claude-User` | Anthropic | User-initiated fetches |
| `PerplexityBot` | Perplexity | Search index and citations |
| `Perplexity-User` | Perplexity | Fetches a page when a user asks about it |
| `Google-Extended` | Google | Controls use of your content for Gemini training and grounding; `Googlebot` still handles Search and AI Overviews |

To be cited, allow the search and user-agent bots; block only the training bots if that is the policy. Example that keeps citations but opts out of training:

```text
User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: Google-Extended
Disallow: /
```

`Claude-Web` and `anthropic-ai` are legacy names; do not rely on them. Bot names change, so verify against each vendor's current documentation before finalising a policy.

## 6. Measuring

Search Console (indexing, queries, Core Web Vitals field data), analytics with UTM-tagged links for AI referrals, and periodic manual checks of how ChatGPT, Perplexity, and Gemini answer your core questions and whom they cite.

## 7. Scripts (advisory)

Both scripts are heuristic and never block a task on their own; review their findings before changing content.

- `./scripts/seo_checker.py <project>` scans HTML/JSX/TSX pages for a title, meta description, Open Graph tags, multiple `h1`s, and images without `alt`. It also flags `alt=""`; treat that as informational for decorative images.
- `./scripts/geo_checker.py <project>` scores public pages on citation readiness: single `h1`, `h2` structure, JSON-LD and recognisable schema entities, author and date on articles, and bonus points for FAQ sections, lists, tables, data-backed claims, and definition phrasing. Average score below 60 returns exit code 1.

```powershell
python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/skills/seo-fundamentals/scripts/seo_checker.py .
python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/skills/seo-fundamentals/scripts/geo_checker.py .
```
