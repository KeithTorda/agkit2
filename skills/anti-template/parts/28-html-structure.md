---
part: 28
title: HTML Structure
covers: div soup, nesting depth, wrapper chains, semantic elements, headings, lists, tables for data, buttons vs links, forms markup, head and meta boilerplate, inline scripts and styles, IDs, classes, data attributes, iframes, inline SVG hygiene, HTML comments, template leftovers, validation
---

# 28 — HTML Structure

Read when: writing or reviewing any HTML, JSX, Vue/Svelte template, Blade/PHP view, or email template markup.

## 28.1 Div soup and nesting

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Div for everything | Generator output with no semantic choice | Semantic element for each job: `header`, `nav`, `main`, `section`, `article`, `aside`, `footer`, `ul`, `table`, `form`, `button`, `a` |
| Nesting 8+ levels deep | Wrappers stacked for each style tweak | 3–4 levels inside a component. Move spacing and alignment to the parent's CSS (`gap`, `grid`) |
| `container` / `wrapper` / `inner` triple around one block | Template scaffolding | Single element with the needed width and padding |
| `div.row > div.col-12 > div.card > div.card-body > div.content` for a single paragraph | Bootstrap grid used for one column | `<p>` or one `<section>` with a max-width. Use the grid only for real columns |
| Every section in `div.card` | Card-everything markup | Content on the page surface; card only for a self-contained item. See part 14 |
| Wrapper added only to apply `flex` | One element could be the flex container | Put `display: flex` on the existing parent |
| Wrapper added only for margin between siblings | Spacing via extra elements | `gap` on the parent, or margin on the child |
| Empty `div`s for decoration (`<div class="blob"></div>`, `<div class="glow"></div>`, `<div class="divider"></div>`) | Decorative nodes in content markup | Remove decoration (see part 10). For a divider use `<hr>` or a border |
| Spacer elements (`<div class="h-8"></div>`, `<br><br>`) | Layout done with empty nodes | Margin or `gap` |
| React fragments around a single child, or wrapper `div` instead of a fragment | Extra node or pointless fragment | Return the child directly; use `<>…</>` only for multiple siblings |
| `<span>` wrapping every word or letter | Animation leftovers. See part 25 | Plain text |

```html
<!-- Banned -->
<div class="section-wrapper">
  <div class="container">
    <div class="inner">
      <div class="row"><div class="col-12"><div class="card"><div class="card-body">
        <div class="title">Office hours</div>
        <div class="text">Monday to Friday, 8:00 AM to 5:00 PM</div>
      </div></div></div></div>
    </div>
  </div>
</div>

<!-- Use -->
<section class="office-hours">
  <h2>Office hours</h2>
  <p>Monday to Friday, 8:00 AM to 5:00 PM</p>
</section>
```

## 28.2 Page skeleton and landmarks

Landmark requirements for screen readers are in part 27.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| No `<main>`; content sits directly in `<body>` or `#app` | Framework root with no structure | `<header>`, `<main>`, `<footer>` inside the root |
| `<header>` used for every card and section top | Misunderstood as "top bar of anything" | `<header>` for the page banner, and inside `<article>` only when it groups a title and meta |
| `<section>` without a heading | Generic wrapper under a semantic name | `<section>` only when it has a heading; otherwise `<div>` |
| `<article>` for every card | Overused | `<article>` for self-contained content that makes sense alone: a post, a news item, a product, an announcement |
| `<aside>` for a layout column | Wrong meaning | `<aside>` for tangential content (related links, sidebars on articles) |
| `<nav>` around every group of links (footer legal links, tag lists) | Too many navigation landmarks | `<nav>` for major navigation blocks: primary, breadcrumb, pagination, table of contents |
| `<footer>` missing, copyright floating in a `div` | Unstructured page end | `<footer>` with contact, legal links, copyright |
| `<body>` with 15 classes from a template | Template leftovers | Only classes that are used |

```html
<!-- Use: page skeleton -->
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <a href="/" class="site-logo"><img src="/logo.svg" alt="Barangay San Isidro, home" width="160" height="40"></a>
    <nav aria-label="Primary">…</nav>
  </header>
  <main id="main" tabindex="-1">
    <h1>Barangay clearance</h1>
    …
  </main>
  <footer class="site-footer">…</footer>
</body>
```

## 28.3 Headings and text

Heading order rules are in part 27. This covers markup choices.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `<div class="title">` / `<p class="text-2xl font-bold">` as section headings | Styled text instead of headings | `<h2>`, `<h3>` with classes for size |
| Heading level chosen by size (`<h4>` because it looks right) | Structure follows styling | Level from structure; size from CSS |
| Eyebrow text as a separate heading above the real heading (`<h6>FEATURES</h6><h2>…`) | Template eyebrow in the outline | `<p class="eyebrow">` before the `<h2>`, or drop the eyebrow. See part 05 |
| Subtitle in a second heading (`<h1>Title</h1><h2>Subtitle</h2>`) | Subtitle becomes a section | `<h1>` then `<p class="lead">` |
| `<br>` for line breaks in headings and paragraphs to control wrapping | Breaks on other widths | `text-wrap: balance` on headings; `max-width` in `ch`. See part 13 |
| `<b>` / `<strong>` on half the paragraph | Emphasis inflation. See part 02 | `<strong>` for one key fact at most per paragraph |
| `<i>` for icons (`<i class="fa fa-user">`) | Font Awesome legacy | `<svg aria-hidden="true">` or the icon component. See part 26 |
| `<i>` / `<em>` used for styling | Wrong meaning | `<em>` for stress, `<i>` for terms and foreign words (e.g. `<i lang="fil">bayanihan</i>`); CSS for style |
| `<blockquote>` for pull-quotes of your own page text | Decoration | Remove; `<blockquote>` only for quotes from a source, with `<cite>` |
| Dates as plain text in structured content | Not machine readable | `<time datetime="2025-06-05">5 June 2025</time>` |
| Addresses in `div`s | No meaning | `<address>` for contact info of the page owner or article author |
| Abbreviations unexplained (BIR, LGU, SK, DepEd) | Unclear on first use | Spell out on first use in text; `<abbr title="Bureau of Internal Revenue">BIR</abbr>` optional |
| `&nbsp;` chains for spacing | Typewriter spacing | CSS margin or gap. `&nbsp;` only to keep units together (`₱&nbsp;1,000`, `10&nbsp;kg`) |

## 28.4 Lists

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Nav links as a row of `<a>` inside a `div` | Missing list structure | `<nav><ul><li><a>` |
| Repeated cards rendered as sibling `div`s | Screen readers lose the count | `<ul>` of `<li>` cards (reset list styles) |
| Steps as `div`s with "Step 1" text | Order not encoded | `<ol>` |
| Key-value details as `div`s with bold labels | Label-value relation lost | `<dl><dt>Status</dt><dd>Approved</dd></dl>`. See part 19 |
| Feature list with emoji or checkmark characters as bullets | Characters read aloud | `<ul>` with CSS `list-style` or `::marker` |
| `<li>` outside a `<ul>`/`<ol>` | Invalid HTML | Wrap in the list |
| `<ul>` containing `<div>`s directly | Invalid HTML | Only `<li>` children (plus `<script>`/`<template>`) |
| One-item lists everywhere | Structure with no benefit | Plain element for a single item |
| Breadcrumb as a string with `>` characters | Separators read aloud | `<nav aria-label="Breadcrumb"><ol>` with CSS separators; `aria-current="page"` on the last item |

## 28.5 Tables

Table design is in part 19; table accessibility in part 27.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Tables avoided for data (CSS grid of `div`s for records) | "Tables are old" reflex | `<table>` for tabular data |
| Table used for page layout | Old template habit (common in legacy PHP and email) | CSS grid or flex. Email is the one exception, see 28.13 |
| No `<thead>` / `<tbody>` | Browser inserts `tbody`; header not marked | `<thead>` with `<th scope="col">`, `<tbody>` for rows, `<tfoot>` for totals |
| Header cells as `<td><b>` | Header not a header | `<th scope="col">` |
| Totals row styled bold in `<tbody>` | Total not marked | `<tfoot>` with `<th scope="row">Total</th>` |
| `colspan`/`rowspan` to fake layout | Breaks cell relationships | Split into separate tables, or restructure |
| Nested tables | Unreadable | Expandable row, detail panel, or separate table. See part 19 |
| Inline `width` attributes on every `<td>` | Legacy markup | `<colgroup>` or CSS on column classes |
| Action buttons inside `<th>` | Header cell used as toolbar | Actions in their own `<td>`, or above the table |
| Numbers not in a consistent cell alignment class | Right-alignment done per cell with inline style | One class on numeric columns (`class="num"`) set in CSS |

## 28.6 Buttons, links and forms markup

Behaviour rules are in parts 17, 18 and 27.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Span click handler | Not focusable | `<button type="button">` |
| `a` without `href` as a button | Not a link, not a button | `<button>` |
| `role="button"` on `div` | Rebuilding a native element badly | `<button>` |
| `<a href="#">` placeholders left in nav and footer | Dead links shipped | Real URLs, or remove the link |
| `<a href="javascript:void(0)">` | Legacy hack | `<button>` |
| `target="_blank"` on internal links | Opens tabs the user did not ask for | Same tab for internal links |
| `target="_blank"` without telling the user | Unexpected new tab | Use sparingly (external documents); add text "(opens in new tab)" or an icon with `.sr-only` text. `rel="noopener"` is default in modern browsers but harmless to keep |
| `<button>` with no `type` in a form | Submits the form | `type="submit"` or `type="button"` always explicit |
| `<form>` missing; inputs wired with JS only | Enter key does not submit; no native validation | `<form>` with `action`/`method` or an `onsubmit` handler |
| `<input>` without `name` | Value not submitted | `name` on every field |
| `<input type="text">` for email, phone, number, date | Wrong keyboard on mobile | `type="email"`, `type="tel"`, `inputmode="numeric"`, `type="date"` where suitable. See part 17 |
| `<label>` missing, or not linked with `for`/`id` | No name | `<label for>` |
| Radio/checkbox groups without `<fieldset>`/`<legend>` | Question lost | `<fieldset><legend>` |
| `novalidate` on every form with no replacement validation | Native checks removed, custom ones missing | Keep native constraints, or implement full server and client validation |
| Hidden inputs holding secrets or prices trusted by the server | Client-editable | Server computes prices and permissions; hidden inputs only for IDs and CSRF tokens |
| No CSRF token in server-rendered forms (Laravel, Django, PHP) | Security gap | `@csrf` / `{% csrf_token %}` / framework equivalent |

## 28.7 The `<head>`

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `<title>` left as "Vite + React", "React App", "Create Next App", "Document" | Template leftover | "{Page name} — {Site name}". See part 08 |
| Same `<title>` on every page | No per-page titles | Unique title per route |
| `<meta name="keywords">` stuffed with 30 terms | Ignored by search engines; SEO-spam look | Remove |
| `<meta name="author">`, `generator`, `copyright`, `revisit-after`, `rating`, `distribution` | Boilerplate from 2005 templates | Remove |
| `<meta http-equiv="X-UA-Compatible" content="IE=edge">` | IE-era leftover | Remove |
| Duplicate `<meta charset>` or `viewport` tags | Merged templates | One each, `charset` first in `<head>` |
| Viewport with `maximum-scale=1, user-scalable=no` | Blocks zoom. See part 27 | `width=device-width, initial-scale=1` |
| 20 favicon links plus `msapplication-*` and `browserconfig.xml` | Favicon-generator dump | `icon.svg`, `favicon.ico`, `apple-touch-icon`, manifest if PWA. See part 26 |
| Open Graph and Twitter tags with template values ("Your description here", `og:image` of the framework logo) | Placeholders shipped | Real values per page, or remove until known. See part 08 |
| Both `twitter:*` and `og:*` duplicating every field | Redundant | `og:*` covers most; add `twitter:card` only |
| `theme-color` set to an AI purple | Default palette leak | Token value from DESIGN.md, or remove |
| Several Google Fonts `<link>`s for families not used | Leftovers | Only the families and weights used. See part 13 |
| `preconnect` to 6 origins | Cargo-cult performance | `preconnect` only to origins used above the fold (usually 0–2) |
| `<link rel="preload">` for assets not used on the page | Wasted bandwidth, console warnings | Preload only the LCP image or critical font |
| jQuery, Bootstrap JS, Popper, AOS, Font Awesome all in `<head>` without `defer` | Render-blocking script pile | Scripts at end of body or `defer`/`type="module"`; remove unused libraries. See part 34 |
| CDN links with `@latest` or no version | Unpinned dependency | Pinned version with `integrity` hash, or local install |
| Analytics snippet with placeholder ID (`G-XXXXXXXXXX`, `UA-000000-2`) | Template leftover | Remove until a real ID exists |
| JSON-LD with invented data (fake ratings, fake address) | Fabricated structured data | Real `Organization`/`GovernmentOrganization`/`School` data only, or none |
| `<base href="/">` added without need | Breaks anchors and relative links | Remove |
| `<link rel="canonical">` pointing to localhost or the template domain | Leftover | Real canonical URL per page, or none |

```html
<!-- Banned -->
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="keywords" content="barangay, best barangay, philippines, government, services, online, portal">
<meta name="author" content="Your Name">
<title>Document</title>

<!-- Use -->
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Barangay clearance — Barangay San Isidro</title>
<meta name="description" content="Requirements, fees and office hours for barangay clearance requests.">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
```

## 28.8 Inline styles and scripts

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Inline styles (`style="margin-top: 20px; color: #333"`) | One-off overrides scattered in markup | Stylesheet class using tokens. See part 29 |
| `style` attribute used to pass dynamic values as whole declarations | Hard to theme | Set a CSS custom property inline (`style="--progress: 42%"`) and use it in CSS |
| `<style>` blocks in the middle of `<body>` | Pasted component snippets | Move to the stylesheet |
| `onclick="…"` and other inline handlers with multi-line logic | Untestable; breaks CSP | `addEventListener` in a script file, or framework event binding |
| `<script>` tags scattered through the body | Snippet-by-snippet assembly | One script entry at the end of body or `defer` in head |
| Inline `<script>` holding config with API keys | Secret exposure | Server-side secrets only; public config in a clearly named `data-` attribute or env at build time |
| `document.write` | Legacy, blocks parsing | DOM APIs |
| JSX `style={{ … }}` objects on most elements | Inline styling in React | Class names, CSS modules or the project's styling approach. See part 31 |
| Tailwind classes plus inline `style` on the same element | Two systems fighting | Pick the project's system. See part 11 |

## 28.9 IDs, classes and attributes

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| IDs everywhere (`id="hero-section"`, `id="feature-card-1"`) | Added "for styling" or by habit | IDs only for label targets, anchors, ARIA references and skip-link targets |
| Duplicate IDs (from a repeated component) | Invalid; breaks labels and ARIA | Generated unique IDs (`useId()` in React, a counter or record ID in templates) |
| Styling by ID (`#hero { … }`) | High specificity. See part 29 | Classes |
| Generic class names (`.container`, `.card`, `.title`, `.box`, `.content`) | Clash across components | Component-prefixed names (`.receipt-list__item`). See part 29 |
| Class names describing looks (`.blue-text`, `.big-margin`, `.left-box`) | Breaks on redesign | Names for purpose (`.status--paid`, `.page-intro`) |
| `data-*` attributes used as styling hooks for everything | Parallel class system | Classes for styling; `data-*` for state or JS hooks (`data-state="open"`, `data-testid` in tests) |
| `data-aos`, `data-wow-*`, `data-scroll` animation attributes | Animation library leftovers. See part 25 | Remove |
| `data-testid` on every element in production markup | Test noise | On elements tests target only; strip in production builds if the project does |
| Boolean attributes written as strings (`disabled="false"`) | `disabled="false"` still disables | Omit the attribute to turn it off |
| `autofocus` on page load for non-search pages | Skips content for screen reader users; jumps on mobile | `autofocus` only on single-purpose pages (search, sign-in) |
| `contenteditable` used as a text input | No form value, no label | `<textarea>` or `<input>` |
| `draggable="true"` on everything | Leftover from a demo | Only on draggable items |

## 28.10 HTML comments and leftovers

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| HTML comments like `<!-- Hero Section -->`, `<!-- Features Section -->`, `<!-- Footer -->` everywhere | Generator narrates its own output; the element already says it | Remove. The `<section>` class and heading name the block |
| `<!-- End of container -->`, `<!-- /.row -->` closing comments | Template habit | Remove. Keep nesting shallow instead |
| Comments explaining obvious markup (`<!-- Button to submit form -->`) | Obvious comment. See part 30 | Remove |
| `<!-- TODO: add content here -->`, `<!-- Add more items as needed -->` | Unfinished work shipped | Finish, or record it in the report and remove the comment |
| Commented-out blocks of old markup | Dead code | Delete; version control keeps history |
| Emoji in comments (`<!-- 🚀 Hero -->`) | AI tell | Remove |
| Lorem ipsum, "Your Company", "John Doe", `example@email.com`, `123 Main St` in shipped markup | Placeholder content | Real content, or flag the missing content in the report. See part 09 for PH addresses |
| `09XX-XXX-XXXX` or `+63 912 345 6789` as a live contact number | Fake phone shipped | The office's real number, or remove and flag |
| `href="https://facebook.com"` (no page) in social links | Placeholder link | Real page URL, or remove |
| Copyright year hard-coded to an old year | Stale | Current year or a range; generate server-side |
| Framework demo markup left in (Vite counter, "Edit src/App.tsx and save to reload") | Template leftover. See part 33 | Remove |

```html
<!-- Banned -->
<!-- ========== Hero Section ========== -->
<section class="hero">
  <!-- Hero Title -->
  <h1>Welcome</h1>
</section>
<!-- ========== End Hero Section ========== -->

<!-- Use -->
<section class="page-intro">
  <h1>Barangay San Isidro</h1>
</section>
```

## 28.11 Inline SVG hygiene

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Figma/Illustrator export pasted raw (`id="Layer_1"`, `data-name`, `xml:space`, `enable-background`, editor metadata) | Bloated, collides IDs across the page | Run SVGO; keep `viewBox`, paths, and `fill`/`stroke="currentColor"` |
| Fixed `width="800" height="600"` with no `viewBox` | Cannot scale | `viewBox` always; size with CSS or `width`/`height` attributes matching the intended display size |
| `viewBox` removed by an optimiser | SVG no longer scales | Keep `viewBox` (SVGO `removeViewBox: false`) |
| Hard-coded colours in icons (`fill="#6366F1"`) | Breaks theming | `currentColor` |
| Same 2 KB SVG pasted 20 times in a list | Markup bloat | Sprite with `<symbol>` and `<use href="#icon-x">`, or the icon component |
| Duplicate internal IDs (`id="gradient1"`, `id="clip0"`) across multiple inline SVGs | Gradients and clips reference the wrong element | Unique IDs per SVG (SVGO `prefixIds`), or avoid defs in icons |
| Decorative SVG without `aria-hidden="true"` | Read aloud or focusable in old browsers | `aria-hidden="true" focusable="false"` |
| Meaningful SVG without a name | Silent | `role="img"` and `aria-label`, or `<title>` with `aria-labelledby`. See part 27 |
| `<svg>` containing `<text>` for labels that should be HTML | Not translatable, not selectable | HTML text next to the SVG |
| Giant inline SVG illustrations in the HTML | Blocks parsing | External `<img src="…svg">` for large decorative art, or remove it. See part 26 |
| Blob, wave and glow SVG decorations | Template visuals. See part 10 | Remove |

```html
<!-- Banned -->
<svg id="Layer_1" data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" width="24" height="24"
  enable-background="new 0 0 24 24" xml:space="preserve"><defs><style>.cls-1{fill:#6366f1;}</style></defs>
  <path class="cls-1" d="…"/></svg>

<!-- Use -->
<svg aria-hidden="true" focusable="false" viewBox="0 0 24 24" width="20" height="20"
  fill="none" stroke="currentColor" stroke-width="1.75"><path d="…"/></svg>
```

## 28.12 Iframes and embeds

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `<iframe>` with no `title` | Screen reader says "frame" | `title="Map of Barangay San Isidro hall"` |
| Google Maps iframe on every page (footer map) | Heavy third-party load site-wide | Map on the contact page only; text address everywhere else |
| Map iframe with the template's default location (Googleplex, New York) | Placeholder shipped | Real location, or remove |
| Iframe with `frameborder`, `scrolling`, `marginheight` attributes | Obsolete attributes | CSS `border: 0`; remove obsolete attributes |
| Iframes loaded eagerly below the fold | Slow page | `loading="lazy"` |
| YouTube/Facebook embeds loaded on page load | Heavy scripts | Click-to-load thumbnail. See part 26 |
| Fixed pixel iframe sizes (`width="600" height="450"`) that overflow on mobile | Horizontal scroll | `width: 100%` with `aspect-ratio` in CSS |
| `allow="…"` list copied with every permission (camera, microphone, autoplay, clipboard-write) | Over-permissioned | Only what the embed needs |
| `sandbox` missing on third-party or user-supplied embed content | Security gap | `sandbox` with the minimum `allow-*` flags |
| Facebook Page plugin iframe as the main content of an LGU news page | Content hidden behind Facebook | Post announcements as HTML on the site; link to Facebook |

## 28.13 Email templates

Email copy is in part 08.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Web layout markup (flex, grid, `div` columns) in HTML email | Breaks in Outlook and many clients | Table-based layout with `role="presentation"` on layout tables |
| Layout tables without `role="presentation"` | Screen readers announce rows and columns | `role="presentation"` on every layout table |
| External stylesheet or `<style>` only | Stripped by many clients | Inline critical styles; keep a small `<style>` for media queries |
| Image-only email (the whole receipt or notice as one JPEG) | Blank when images are off; unreadable to screen readers | Live HTML text; images optional with alt |
| No plain-text part | Spam score; accessibility | Send a plain-text alternative with every HTML email |
| Missing `lang` and `<title>` in email HTML | Screen reader pronunciation | `<html lang="en">` or `lang="fil"`, `<title>` with the subject |

## 28.14 Framework-specific markup tells

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| JSX `<div onClick>` everywhere | Same as div buttons | `<button type="button" onClick>` |
| `className="flex flex-col"` wrapper around each child | Extra nodes for spacing | `gap` on the parent |
| `key={index}` in markup lists | See part 31 | Stable ID |
| `dangerouslySetInnerHTML` for plain text | XSS risk, pointless | Render text as children |
| Vue `v-html` / Blade `{!! !!}` on user content | XSS risk | Escaped output (`{{ }}`) |
| Next.js `<a>` inside `<Link>` (old pattern) or plain `<a>` for internal routes | Outdated or full reloads | `<Link href>` directly |
| `<img>` in Next.js where `next/image` is set up | Mixed approaches | One image approach per project |
| Bootstrap markup copied with unused attributes (`data-bs-toggle` on elements with no JS) | Dead attributes | Remove attributes with no behaviour attached |
| Blade/PHP templates echoing full HTML strings from controllers | Markup scattered in logic | Views or partials; controllers pass data only |
| Every component's root is a `<div>` | No semantic root | Root element that matches the job: `<article>`, `<li>`, `<section>`, `<form>` |

## 28.15 Validity and output checks

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Markup never validated | Unclosed tags, duplicate IDs, invalid nesting ship | Run the W3C Nu validator (`vnu`) or `html-validate` on built pages |
| Block elements inside `<p>` (`<p><div>`) | Browser splits the paragraph | Change `<p>` to `<div>` or restructure |
| Interactive content nested (`<a><button>`) | Invalid | One interactive element |
| Self-closing non-void tags in HTML (`<div />`) | JSX habit in plain HTML | Explicit closing tags in HTML; void elements (`<img>`, `<input>`, `<br>`) need no slash |
| Uppercase tags and attributes, mixed quoting | Merged sources | Lowercase tags, double quotes, consistent indentation via Prettier |
| Missing `<!doctype html>` | Quirks mode | `<!doctype html>` first line |
| Files with CRLF and LF mixed, trailing whitespace | Pasted from several sources | Formatter and `.editorconfig` |

## 28.16 Check
- [ ] No `div` or `span` does the job of `button`, `a`, `ul`, `table`, `form`, `nav`, `main`, `header` or `footer`.
- [ ] Nesting inside a component is 4 levels or fewer.
- [ ] No container/wrapper/inner chains; no wrappers added only for flex or spacing.
- [ ] No empty decorative `div`s, spacer `div`s or `<br>` spacing.
- [ ] One `<main>`, plus `<header>` and `<footer>`; `<section>` only with a heading.
- [ ] `<article>`, `<aside>`, `<nav>` used for their meaning, not layout.
- [ ] Headings are real `<h1>`–`<h6>`; one `<h1>`; subtitles and eyebrows are `<p>`.
- [ ] Repeated items are `<ul>`/`<ol>`; steps are `<ol>`; key-value data is `<dl>`.
- [ ] Data is in `<table>` with `<thead>`, `<tbody>`, `<th scope>`; no layout tables outside email.
- [ ] No `href="#"`, `javascript:void(0)` or anchor-without-href buttons.
- [ ] Every `<button>` has an explicit `type`.
- [ ] Forms use `<form>`, every field has `name` and a linked `<label>`, groups use `<fieldset>`.
- [ ] Input types match the data (`email`, `tel`, `date`, `inputmode`).
- [ ] CSRF token present in server-rendered forms.
- [ ] `<!doctype html>`, `<html lang>`, one `charset`, one viewport without zoom blocking.
- [ ] `<title>` is unique and specific per page; no "Vite + React", "Document" or "React App".
- [ ] No `meta keywords`, `author`, `generator`, `X-UA-Compatible` or other legacy meta.
- [ ] OG, analytics, canonical and JSON-LD contain real values or are absent.
- [ ] Only used fonts, scripts and preloads in `<head>`; scripts deferred; CDN versions pinned.
- [ ] No inline styles except CSS custom properties; no `<style>` or `<script>` blocks mid-body.
- [ ] No inline multi-line event handlers; no `document.write`.
- [ ] IDs only for labels, anchors and ARIA; no duplicate IDs; no ID selectors for styling.
- [ ] Class names describe purpose, not look; no generic `.card`/`.title` without a prefix.
- [ ] No animation-library `data-*` attributes left.
- [ ] No section-label comments (`<!-- Hero Section -->`), closing-tag comments or emoji comments.
- [ ] No commented-out markup, TODO comments or Lorem ipsum in shipped files.
- [ ] No placeholder names, emails, addresses, phone numbers or social URLs.
- [ ] Inline SVGs are SVGO-cleaned, keep `viewBox`, use `currentColor`, and have unique internal IDs.
- [ ] Repeated icons use a sprite or component, not pasted copies.
- [ ] Decorative SVGs are `aria-hidden`; meaningful SVGs have a name.
- [ ] Iframes have `title`, `loading="lazy"`, responsive sizing and a minimal `allow` list.
- [ ] Map embeds show the real location and appear only where needed.
- [ ] Email templates use presentation tables, inline styles, live text and a plain-text part.
- [ ] No `dangerouslySetInnerHTML`, `v-html` or `{!! !!}` on user content.
- [ ] Built pages pass the W3C Nu validator or `html-validate` with no errors.
