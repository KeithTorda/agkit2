---
part: 34
title: Performance, SEO and Theming
covers: image weight, LCP, lazy loading, font payload, icon fonts, animation and utility libraries, CDN @latest, render-blocking scripts, third-party widgets, layout shift, preloaders, skeleton timing, data payloads, build and cache, performance budget for PH networks, technical SEO, titles and meta duplication, robots.txt, sitemap, canonical, structured data, indexing of staging and admin, dark mode, theme toggles, system preference, theme flash
---

# 34 — Performance, SEO and Theming

Read when: adding images, fonts, libraries or third-party scripts; preparing a public site for launch; writing `robots.txt`, sitemap or head tags; adding dark mode or a theme toggle.

Generated sites are heavy in the same ways: a 3 MB hero PNG, five font weights, Framer Motion for one fade, Font Awesome for three icons, and a spinner preloader in front of all of it. The SEO layer is copied boilerplate: one title on every page, a `keywords` meta tag, and a staging domain indexed by Google. Dark mode is either forced on or done with `filter: invert(1)`. This part lists those tells and the fix.

Related: wording of titles, meta descriptions, OG text and alt text is part 08. Font choice and FOUT styling are part 13. Mobile layout and slow-network UX are part 15. Motion design is part 25. Colour values and contrast are part 12. React data fetching is part 31. API and DB performance (N+1, indexes) is part 32.

## 34.1 Images

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Hero image as a 3–6 MB PNG or JPG at 4000px wide | Downloaded from Unsplash at full size and dropped in | Resize to the largest rendered width x 2 (usually 1600–2400px). Export AVIF or WebP at quality 60–80. Keep the hero under about 200 KB. |
| PNG for photographs | Lossless format for lossy content; 5–10x larger | JPG, WebP or AVIF for photos. PNG only for screenshots with text, or images that need exact pixels. |
| `<img>` with no `width` and `height` | Layout jumps when the image loads (CLS) | Set `width` and `height` attributes to the intrinsic ratio, or CSS `aspect-ratio`. |
| One image size for all screens | Phones download desktop images | `srcset` with 3–4 widths and a real `sizes` value. `<picture>` for art direction. |
| Hotlinked `images.unsplash.com/photo-...` with no size params, or `source.unsplash.com/random` | Full-size remote image; random image changes on reload; third-party dependency | Download, resize, self-host. Stock photo tells: see part 26. |
| `loading="lazy"` on the hero or logo | Delays the largest paint; common copy-paste on every `<img>` | No lazy loading above the fold. Add `fetchpriority="high"` to the LCP image. |
| No `loading="lazy"` on long galleries, officials lists, news grids | Page loads 40 images at once | `loading="lazy"` and `decoding="async"` on images below the first screen. |
| LCP hero as a CSS `background-image` | Browser finds it late; cannot use `srcset` or `fetchpriority` | Real `<img>` with `object-fit: cover`, or `<link rel="preload" as="image" imagesrcset=...>` if a background is required. |
| Next.js `<Image unoptimized>` everywhere, or `priority` on every image | Turns off the optimizer, or preloads everything so nothing is prioritised | Default optimizer on. `priority` on the one LCP image per page. |
| Large images inlined as base64 data URIs in CSS/JS | Blocks rendering; cannot be cached separately; bloats the bundle | Separate files. Inline only tiny icons (under about 2 KB), and SVG as markup instead of base64. |
| SVG exported from a design tool with an embedded raster (`<image href="data:image/png;base64,...">`) | "Vector" file that is a 1 MB PNG inside | Export real vectors, or use the raster directly. Run SVGO on exported SVGs. |
| Animated GIF for a demo or loader | Huge, low quality | `<video autoplay muted loop playsinline>` with MP4/WebM and a poster, or a still screenshot. |
| Background video on the homepage | Megabytes on page load; drains prepaid data | Static image. If video is required, `preload="none"`, a poster, and a play button. Video tells: see part 26. |
| Icons as 512px PNGs scaled to 24px | Wasted bytes; blurry on some screens | SVG icons from one set. |
| Every official's photo on an LGU/school site uploaded straight from a phone (4–8 MB each) | No upload pipeline | Resize on upload (server or build step) to a fixed max width, strip EXIF, convert to WebP. |
| Carousel/slider with 8 full-width slides loaded at once | 8 hero images for 1 visible slide | One static image. If a carousel is required, load slides 2+ lazily. Carousel tells: see part 10. |
| `object-fit: cover` on a 4000px image in a 64px avatar | Browser downloads 4000px to show 64px | Serve a thumbnail sized at 2x the display size. |

## 34.2 Fonts (payload)

Font choice and pairing rules are in part 13. This section covers bytes and requests.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Google Fonts URL with 5–9 weights: `wght@100;200;300;400;500;600;700;800;900` | Every weight requested "in case" | Load the 2–3 weights the CSS uses. Or one variable font file. |
| Italic axis loaded (`ital,wght@0,400;1,400;...`) with no italic in the design | Doubles font bytes | Drop italics unless body text uses them. |
| Two or three families loaded (display + body + mono) on a simple site | Template pairing plus a mono for no code | One family. Add a second only with a stated reason. See part 13. |
| `@import url('https://fonts.googleapis.com/...')` inside CSS | Chained request; blocks rendering | `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>` plus `<link rel="stylesheet">` in `<head>`, or self-host. |
| Self-hosted `.ttf` files | Uncompressed format | `.woff2` only. |
| Full character set for a Latin-only site | Extra bytes for scripts never shown | Latin subset. Keep Latin Extended if names use ñ and accented letters (common in Filipino names: Peñafrancia, Dasmariñas, Parañaque). |
| No `font-display` or `font-display: block` | Invisible text on slow networks | `font-display: swap` (or `optional` for non-critical fonts). FOUT styling: see part 13. |
| Preloading every font file | Preload competes with the LCP image | Preload only the one body weight used above the fold. |
| Variable font file plus static files of the same family | Same font downloaded twice | One or the other. |
| `next/font` configured, plus a Google Fonts `<link>` for the same family | Duplicate loading | `next/font` only. |

## 34.3 Icon fonts and icon payload

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Font Awesome full kit (CSS + webfonts, all styles) for 3–10 icons | 100+ KB of fonts for a handful of glyphs | Inline SVG or tree-shaken imports from one SVG icon set (Lucide, Heroicons, Tabler, Phosphor). Icon style rules: see part 26. |
| Material Icons / Material Symbols font loaded from Google | Icon font blocks and flashes ligature text ("shopping_cart") before load | SVG icons. If Material Symbols is required, request only the used icons with `icon_names=`. |
| `bootstrap-icons.css` plus Font Awesome plus an SVG set | Three icon systems | One set. |
| `import * as Icons from 'lucide-react'` or dynamic icon by string name from the whole set | Pulls every icon into the bundle | Named imports: `import { Trash2 } from 'lucide-react'`. |
| `react-icons` importing from 5 different sets | Mixed styles and bigger bundle | One set via named imports. |
| Emoji used as icons to avoid an icon library | Rendering differs by OS; reads as generated | SVG icons. See part 26. |

## 34.4 JavaScript and dependencies

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Framer Motion / GSAP / AOS / anime.js installed for one fade-in | 30–60 KB for an effect CSS does in 3 lines | CSS `transition` or `@keyframes`, or remove the effect. Motion rules: see part 25. |
| `animate.css` full stylesheet for one class | Whole library for one animation | Copy the one keyframe you need, or drop it. |
| Lottie player for a loading spinner or empty-state animation | Player plus JSON for decoration | CSS spinner or static SVG. |
| `canvas-confetti`, `react-confetti`, typewriter or particles libraries | Decoration libraries; each a tell on its own | Delete. See part 25. |
| three.js, tsParticles, Vanta for a hero background | Hundreds of KB and constant GPU use for a backdrop | Solid background token. See part 10. |
| `moment` | Large and in maintenance mode | `Intl.DateTimeFormat` with `'en-PH'` or `'fil-PH'`, or `date-fns`/`dayjs` if parsing is needed. |
| Full `lodash` import (`import _ from 'lodash'`) | Whole library for `debounce` | Native methods, or `import debounce from 'lodash/debounce'`. |
| jQuery added to a React/Vue app | Two DOM models | Framework code. |
| `axios` for 3 `GET` calls | Dependency for what `fetch` does | `fetch` with a 10-line wrapper, unless interceptors are needed. |
| Chart.js / Recharts / ApexCharts for one sparkline | Charting library for a 40px line | Inline SVG `<polyline>`, or a number with a delta. Chart rules: see part 20. |
| Full UI kit (MUI, Ant Design, Chakra) installed for one date picker | Kit-wide CSS and runtime for one component | Native `<input type="date">` or one focused library. |
| Bootstrap CSS and Tailwind both loaded | Two resets, two systems, conflicting utilities | One. |
| Bootstrap `bootstrap.bundle.min.js` included on a page with no JS components | Unused script on every page | Include JS only on pages that use dropdowns, modals or collapse. |
| Polyfill.io or IE polyfills | Dead browser support; polyfill.io was compromised in 2024 | Remove. Target evergreen browsers plus the Android WebView versions the client needs. |
| Client-side rendering for a static brochure or LGU info site | Blank page until JS loads; weak on low-end phones | Static HTML (Astro, Eleventy, plain HTML, or Next static export). Server components: see part 31. |
| Google Maps JS API embedded on every page for one office location | Heavy script plus billing key exposure | Static map image linking to Google Maps, or an `<iframe loading="lazy">` on the contact page only. Maps in data views: see part 20. |
| Leaflet plus a 20 MB GeoJSON of all barangays loaded at start | Whole-country boundaries for one municipality view | Simplify geometry (mapshaper), split per municipality, load on demand, or serve vector tiles. |

## 34.5 CDN, versions and supply chain

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `https://cdn.jsdelivr.net/npm/<pkg>@latest/...` or `unpkg.com/<pkg>` with no version | Site breaks silently on the next major release | Pin an exact version: `@5.3.3`. Better, install via npm and bundle. |
| CDN script without `integrity` and `crossorigin` | No tamper protection | Add SRI hash (`integrity="sha384-..."`) for every third-party CDN file. |
| Same library from two CDNs, or CDN plus npm | Loaded twice; version mismatch | One source. |
| Tailwind Play CDN (`cdn.tailwindcss.com`) in production | Development-only script that compiles CSS in the browser | Build step with the Tailwind CLI or framework plugin. |
| Babel standalone in the browser to run JSX | Compiles at runtime on every visit | Build step. |
| `"latest"` or `"*"` versions in `package.json` | Unreproducible builds | Caret ranges plus a committed lockfile. |

## 34.6 Render-blocking and third-party scripts

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `<script src>` in `<head>` without `defer`, `async` or `type="module"` | Blocks parsing | `defer` for app scripts; `async` for independent analytics. |
| Google Analytics, GTM, Meta Pixel, Hotjar and Microsoft Clarity all installed on a barangay site | Tracking stack copied from a marketing template | One analytics tool the client will read. None if nobody will. Privacy notice must match (Data Privacy Act; see part 08 for notice wording). |
| Chat widgets (Tawk.to, Crisp, Messenger chat plugin) loaded on every page at start | 200+ KB and a floating bubble on every page | Load on click from a plain "Message us" link, or link to the Facebook Page. The Facebook Customer Chat plugin was discontinued in 2024; remove it. |
| Facebook Page Plugin iframe embedded in the homepage sidebar | Heavy iframe; often blank when blocked | Link to the Page. Show recent posts server-side only if the client needs them. |
| YouTube `<iframe>` embeds on load | Loads the full player per video | Facade: thumbnail image plus play button; load the iframe on click (`lite-youtube-embed` or 20 lines of JS). |
| Social share buttons SDKs (AddThis, ShareThis) | Tracking scripts for buttons nobody uses; AddThis shut down in 2023 | Plain share links (`https://www.facebook.com/sharer/sharer.php?u=`) or the Web Share API. |
| Inline `<script>` blocks of 50+ KB in HTML | Not cached; parsed on every page | External file with a hashed name. |
| `<link rel="preload">` on 10 resources | Preload everything means nothing is prioritised | Preload only the LCP image and the critical font. |
| `<link rel="prefetch">` on every nav link | Wasted data on prepaid connections | Let the framework prefetch on hover/viewport, or none. |
| reCAPTCHA script loaded on every page | Heavy script site-wide | Load only on the form page. CAPTCHA need: see part 23. |

## 34.7 Layout shift

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Images and iframes without reserved space | Content jumps as they load | `width`/`height` or `aspect-ratio` on every media element. |
| Announcement or cookie banner injected at the top after load | Pushes the whole page down | Render it server-side in its final place, or overlay it at the bottom with fixed position and reserved space. |
| Skeleton sized differently from the loaded content | Two jumps: skeleton in, then real content | Skeleton matches final row height and count. Skeleton design: see part 21. |
| Web font swap changes line lengths a lot | Headline reflows | Fallback font metric overrides (`size-adjust`, `ascent-override`) or `next/font`, which sets them. |
| Late-loading ad or embed above content | Content moves while the user reads | Reserve the slot height, or place embeds below the main content. |
| Dynamic content inserted above what the user is reading (new rows at top of a feed) | Reading position lost | "3 new entries" button that inserts on click. |
| Buttons whose label width changes on loading ("Save" to "Saving...") | Button resizes and nearby items move | Fixed min-width or keep the label and add a spinner inside. See part 18. |

## 34.8 Perceived performance and loading states

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Full-page preloader (logo spinner, percent counter) on a landing page | Common template habit; hides a page that could render now | Remove it. Render HTML immediately. |
| Splash screen with logo animation in a web app | Delays every visit by 1–3 s | No splash. Show the app shell. |
| Skeleton shimmer on data that returns in under 500 ms | Flash of grey blocks; slower-feeling than nothing | Show nothing for the first 300–500 ms, then a skeleton or spinner. Skeleton only for loads over 500 ms. |
| Spinner for actions under 200 ms | Flicker | No indicator under 200 ms; delay the spinner by 200–300 ms. |
| Artificial delays (`setTimeout(..., 1500)`) "so it feels like it's working" | Makes the app slow on purpose | Remove. Show the result when it is ready. |
| Fake progress bar that counts to 99% | Lies about progress | Real progress (upload bytes) or an indeterminate indicator. |
| Loading the whole app before showing a static page (SPA shell for the About page) | Content waits on JS | Static render for content pages. |
| No optimistic update on a safe action (toggling a checkbox waits 800 ms) | Sluggish feel | Update the UI immediately; roll back and show an error on failure. Not for payments or votes. |

## 34.9 Data payload and fetching

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Fetch every row, then paginate and filter in the browser | Megabytes on first load; slow on low-end Android | Server-side pagination, filter and sort. Return 25–50 rows per page. Table rules: see part 19. |
| Full PSGC list (all regions to all barangays) bundled into the JS | Tens of thousands of rows in the bundle for one dropdown chain | Load provinces, then cities for the chosen province, then barangays for the chosen city, each on demand and cached. |
| Precinct or voter lookup that downloads the whole list and searches client-side | Exposes data and wastes bandwidth | Server-side search endpoint with a minimum query length and rate limit (part 32). |
| API returns full objects with 40 fields for a list that shows 4 | Wasted bytes | Select only needed columns for list endpoints. |
| Polling every 2–5 s | Battery and data drain; server load | Refetch on focus and on action, or poll at 60 s+ with "Updated 2m ago". Live labels: see part 04. Dashboard refresh: see part 22. |
| Same request fired 3 times on mount | Duplicate effects or components each fetching | Shared cache (TanStack Query, SWR, framework loader). See part 31. |
| No HTTP caching on static API data (provinces, fee tables, product categories) | Refetched every visit | `Cache-Control: public, max-age=...` with ETags, or bake into the build. |
| Uncompressed JSON responses | Easy win missed | gzip or Brotli on the server or CDN. |
| Images uploaded by users served at original size in lists | 5 MB photos in a 48px thumbnail column | Generate thumbnails on upload. |

## 34.10 Build, caching and deploy

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Development build deployed (`npm run dev` on the server, React dev mode warnings in console) | Slow and verbose; exposes internals | Production build (`npm run build`) served by a static host or `node` server. |
| `vite preview` used as the production server | Preview server is not meant for production | Static host (Netlify, Vercel, Cloudflare Pages, Nginx). |
| Assets without hashed file names, served with `no-cache` | Every visit re-downloads everything | Hashed names from the bundler with `Cache-Control: public, max-age=31536000, immutable`. HTML with `no-cache`. |
| Public source maps on a client project | Exposes source code | Upload source maps to the error tracker only, or keep them off public paths. |
| Unminified CSS/JS in production | Larger files | Bundler minification on. |
| Tailwind build without content scanning, shipping the full 3 MB stylesheet | Purge misconfigured | Correct `content` paths (v3) or source detection (v4). Check the built CSS size. |
| Bootstrap full CSS plus a 2,000-line override file | Two stylesheets fighting | Customise via Sass variables and import only used components. See part 29. |
| Service worker from a template caching everything forever | Users stuck on old versions | No service worker unless offline use is a requirement. If needed, use Workbox with a versioned cache and an update prompt. |
| No performance budget in the plan | Weight creeps up unnoticed | Write a budget in the plan and check it on each build, for example: JS under 200 KB gzip per route, LCP image under 200 KB, 2 font files. |
| Performance tested only on a fast laptop on fibre | PH users are mostly on mid-range Android over mobile data | Test with Chrome DevTools "Slow 4G" and 4x CPU throttling, and on a real budget Android phone. Mobile specifics: see part 15. |
| Lighthouse score quoted as proof ("100/100 performance") | One lab run on a fast machine | Report LCP, CLS and INP from a throttled run, and field data if available. |

## 34.11 Technical SEO: titles, meta and head

Wording rules for titles, meta descriptions, OG text and alt text are in part 08. This section covers duplication, structure and crawl settings.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Same `<title>` on every page (set once in the layout) | SPA or layout default never overridden | Unique title per page: page name first, site name last: "Enrollment Requirements — San Roque NHS". |
| Titles like "Home — Premium Community Experience" or "Home Page" | Marketing or placeholder titles | Name what the page shows: "Phorum — Community Forum". See part 08. |
| `<title>React App</title>`, "Vite + React + TS", "Create Next App" | Template default shipped | Real title. See part 33. |
| Same meta description on every page | Copied in the layout | Unique description per page, or omit it and let search engines pick text. |
| `<meta name="keywords" content="best, top, cheap, Philippines, website, ...">` | Ignored by Google for years; reads as keyword stuffing | Delete the tag. |
| Keyword-stuffed titles and headings ("Best Barangay Clearance Online Philippines Fast Barangay Clearance") | Spam pattern | One plain title. Say what the page is. |
| Hidden text or text coloured like the background for SEO | Spam; can be penalised | Delete. |
| `<meta name="robots" content="index, follow">`, `<meta name="revisit-after">`, `<meta name="rating">`, `<meta name="distribution">`, `<meta name="generator">` | Boilerplate that does nothing | Delete. Add `robots` only to say `noindex` on pages that need it. |
| `<meta name="author" content="">`, empty `og:image`, `twitter:site` for an account that does not exist | Empty or false tags | Fill with real values or remove. |
| OG image missing, or the same generic image on every page | Shared links show a blank or template card | 1200x630 image per page type (home, article, event). Text on it follows part 08. |
| Multiple `<h1>` or no `<h1>` | Heading structure broken | One `<h1>` per page. Heading rules: see part 28. |
| No `lang` or `lang="en"` on Filipino-language pages | Wrong language signals | `lang="fil"` or `lang="en-PH"` to match the content. See part 27. |
| Missing `<link rel="canonical">` where the same page is reachable by several URLs (`?ref=`, trailing slash, `www`) | Duplicate content | Canonical to the preferred URL. Redirect `www`/non-`www` and trailing slash variants with 301s. |
| Canonical pointing every page to the homepage | Copied from the layout; tells Google all pages are the homepage | Self-referencing canonical per page. |
| `hreflang` tags for `fil` and `en` when there is only one language version | Tags for pages that do not exist | Add `hreflang` only when both language versions exist and link to each other. Bilingual UI: see part 09. |

## 34.12 Crawling and indexing: robots.txt, sitemap, status codes

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `robots.txt` with `Disallow: /` shipped from staging | Whole site blocked from search | Production `robots.txt`: allow public paths, disallow `/admin`, `/api`, `/account`. Check it on launch day. |
| `<meta name="robots" content="noindex">` left in the layout after launch | Site never appears in search | Remove on production. Make it depend on an env var so it cannot leak. |
| CRA/robotstxt.org sample `robots.txt` comment kept | Template leftover | Real rules and a `Sitemap:` line. |
| Sitemap with `localhost`, `127.0.0.1`, or the staging domain in `<loc>` | Generated from the dev environment | Build the sitemap from the production base URL env var. |
| Sitemap listing admin, login, cart, thank-you and search result pages | Everything crawlable dumped in | Only public, indexable, canonical pages. |
| `<lastmod>` identical on every URL (build date) or `<priority>`/`<changefreq>` on every entry | Fake freshness; `priority` and `changefreq` are ignored by Google | Real last-modified dates, or omit `lastmod`. Drop `priority` and `changefreq`. |
| No sitemap on a site with 50+ pages (news, announcements, officials) | Deep pages found slowly | Generated sitemap, linked from `robots.txt`, submitted in Search Console. |
| Staging or preview URLs (`*.vercel.app`, `*.netlify.app`, `staging.`) indexed | Duplicate site in search results | `noindex` header or password on previews. Canonical to production. |
| Admin dashboard and internal POS pages indexable | Login screens and internal tools in search | Auth-gated routes return 401/302; add `noindex` and `Disallow` as well. |
| 404 page that returns HTTP 200 (soft 404), common in SPAs | Search engines index error pages | Real 404 status: server config or framework `notFound()`. Error page copy: see part 04. |
| Hash routing (`/#/about`) for public pages | Fragments are not separate URLs to crawlers | History routing with server fallback, or static pages. |
| Public content rendered only client-side | Crawlers and link previews see an empty shell | Server-render or pre-render public pages. |
| Redirect chains (`http` to `https` to `www` to trailing slash) | Slow and lossy | One 301 to the final URL. |

## 34.13 Structured data

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `AggregateRating` / `Review` schema with invented ratings ("4.9 from 1,200 reviews") | Fake data; violates search guidelines | Remove. Add only if real reviews exist on the page. Fake social proof: see part 05. |
| `FAQPage` schema on a page with no visible FAQ | Markup for content that is not there | Structured data must match visible content. Delete. |
| `Organization` schema with `sameAs` links to social accounts that do not exist | Copied template | Only real, active profiles. |
| `LocalBusiness` with placeholder address, `+1` phone, or `"priceRange": "$$"` on a PH business | US template values | Real address in PH format, `+63` phone, peso price range or omit. Address and phone format: see part 09. |
| Government office marked up as `Corporation` or `LocalBusiness` | Wrong type | `GovernmentOrganization` / `GovernmentOffice`; schools as `School` / `HighSchool` / `CollegeOrUniversity`. |
| `Event` schema without real dates, or for past events never removed | Stale or fake events | Real `startDate` with `+08:00` offset, location, and `eventStatus`. Remove after the event or mark completed. |
| Structured data never validated | Errors go unnoticed | Run the Rich Results Test or Schema Markup Validator before launch. |

## 34.14 Dark mode: defaults and colour

Colour token values and contrast ratios are in part 12. This section covers how the theme is chosen, stored and applied.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Dark mode by default with neon accents on a site that has no reason to be dark | Default AI look (original rule: "Dark mode + neon by default") | Use the DESIGN.md palette. Light mode is fine. Follow the user's system preference if both themes exist. |
| Pure black background (`#000`, `bg-black`) with pure white text | Harsh contrast; smearing on OLED during scroll | Dark surface token from DESIGN.md (`var(--color-bg)` in the dark set) and a softened text token (`var(--color-text)`). If DESIGN.md has no dark set, add near-black and off-white tokens there first; do not hard-code. |
| Same saturated brand colour in both themes | Vibrates on dark backgrounds; fails contrast | A dark-theme variant of each accent token in DESIGN.md. Check 4.5:1 for text, 3:1 for UI parts. |
| Shadows reused in dark mode | Invisible on dark surfaces; look like smudges | Elevation by lighter surface tokens (`var(--color-surface-2)`) and 1px borders in dark mode. |
| Dark mode that changes only the page background | Cards, inputs, tables, code blocks and modals stay light | Theme every surface through tokens. Grep for hard-coded colours (part 35). |
| `dark:` Tailwind variants sprinkled on some components only | Half the UI themed | Semantic tokens in CSS variables switched by one `.dark` or `[data-theme]` selector; components use the tokens, not `dark:` pairs. |
| Hard-coded colours in inline styles, SVGs, charts and canvas | Do not switch with the theme | `currentColor` in SVGs, CSS variables read into chart configs, re-render charts on theme change. Chart palettes: see part 20. |
| Brand logo is a black transparent PNG that disappears on dark | Logo not checked in dark mode | `logo-on-dark` asset, or an SVG with `fill="currentColor"`. |
| Photos and screenshots at full brightness on dark pages | Glare | Leave photos unchanged; optionally lower brightness slightly with a token-driven filter on decorative images only. |
| Map tiles stay light in a dark UI | Bright block in the page | Dark tile style when in dark mode, or keep the map in a bordered light panel on purpose. |
| Printed pages in dark mode | Black pages waste toner | `@media print` forces the light tokens. Receipts and certificates always print light. |

## 34.15 Dark mode: mechanics

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Dark mode made with `filter: invert(1) hue-rotate(180deg)` on `html` | Inverts photos, logos and brand colours; a known shortcut | Real dark tokens. Never invert images. |
| No `prefers-color-scheme` support; theme only via toggle, default light or dark | Ignores the OS setting | Default to system: `@media (prefers-color-scheme: dark)` sets tokens unless the user chose a theme. |
| Two-state toggle (Light/Dark) with no "System" option | Once clicked, the user cannot return to following the OS | Three options: System, Light, Dark. Default System. |
| Theme choice not saved | Resets on every visit | Save to `localStorage` (and the user profile if signed in). |
| Flash of the wrong theme on load | Theme set by JS after first paint | Inline blocking script in `<head>` that reads the saved choice and sets `data-theme` before paint; or `next-themes`; or server-render from a cookie. |
| `color-scheme` property missing | Form controls, scrollbars and autofill stay light in dark mode | `:root { color-scheme: light dark; }` and set `color-scheme: dark` on the dark theme. Add `<meta name="color-scheme" content="light dark">`. |
| `theme-color` meta fixed to one colour | Mobile browser bar mismatched in the other theme | Two `<meta name="theme-color">` tags with `media="(prefers-color-scheme: ...)"`, values from tokens. |
| Theme switcher with 6–10 themes (Ocean, Sunset, Forest, Cyberpunk) | Feature padding; each theme untested | Light and dark max (original rule). One brand. |
| Animated sun/moon toggle icon that spins, morphs or bounces | Decorative motion on a setting | Static icon or a labelled select. Motion: see part 25. |
| Theme toggle in the main nav of a government or school site | Setting given prime space | Put it in the footer or settings, or follow the system and skip the toggle. |
| Theme transition `transition: all 0.3s` on `*` when switching | Everything animates; slows the page | Switch instantly. Suppress transitions during the change. |
| Server-rendered markup uses one theme; client hydrates to another | Hydration warnings and flicker | Read the theme from a cookie on the server, or render theme-neutral markup and let CSS variables switch. |
| Emails and PDFs built with the same dark tokens | Unreadable when printed or opened in light clients | Emails and documents use a fixed light palette. Email rules: see part 08. |

## 34.16 Check

- [ ] Hero/LCP image under about 200 KB, AVIF/WebP, sized to 2x its rendered width.
- [ ] No PNG photographs.
- [ ] Every `<img>` and `<iframe>` has `width`/`height` or `aspect-ratio`.
- [ ] `srcset` and `sizes` on content images.
- [ ] No `loading="lazy"` above the fold; `fetchpriority="high"` on the LCP image.
- [ ] Below-fold images lazy-loaded.
- [ ] No hotlinked Unsplash or random-image URLs.
- [ ] No background video or GIF loaders; video uses a poster and does not preload.
- [ ] User uploads resized and thumbnailed on upload.
- [ ] Font weights loaded equal the weights used (2–3); no unused italics.
- [ ] Fonts are `.woff2`, subset, `font-display: swap`, preconnected or self-hosted.
- [ ] No icon font for a handful of icons; one SVG icon set with named imports.
- [ ] No animation, confetti, particles, typewriter or Lottie library for decoration.
- [ ] No `moment`, full `lodash`, jQuery in a framework app, or UI kit for one widget.
- [ ] No `@latest` or unversioned CDN URLs; SRI on CDN files; no Tailwind Play CDN.
- [ ] No render-blocking `<script>` in `<head>`; app scripts `defer`.
- [ ] One analytics tool at most; chat and video embeds load on click.
- [ ] No full-page preloader or splash screen.
- [ ] Skeletons only for loads over 500 ms and sized like the final content.
- [ ] No artificial delays or fake progress bars.
- [ ] Lists paginated, filtered and sorted on the server.
- [ ] PSGC and other large reference data loaded per level, not bundled whole.
- [ ] No polling faster than 60 s without a reason in the plan.
- [ ] Production build deployed with hashed assets and long cache headers.
- [ ] Performance budget written in the plan and checked.
- [ ] Tested with Slow 4G and 4x CPU throttling, and on a budget Android phone.
- [ ] Unique `<title>` and description per page; no template titles.
- [ ] No `keywords`, `revisit-after`, `generator` or empty meta tags.
- [ ] One `<h1>` per page; correct `lang`.
- [ ] Self-referencing canonical; one 301 to the final URL.
- [ ] `robots.txt` allows public pages, blocks admin/API, lists the sitemap; no `Disallow: /` in production.
- [ ] No `noindex` in production layout; previews and staging are `noindex`.
- [ ] Sitemap uses the production domain and lists only public canonical pages.
- [ ] 404s return HTTP 404; no hash routing for public pages.
- [ ] Structured data matches visible content; no fake ratings; correct PH address and `+63` phone.
- [ ] Theme follows system preference by default; System/Light/Dark options; choice saved.
- [ ] No theme flash on load; `color-scheme` set; `theme-color` per scheme.
- [ ] No `filter: invert()` dark mode; no pure black or pure white; tokens from DESIGN.md.
- [ ] Every surface, chart, SVG and logo checked in both themes.
- [ ] Light and dark only; no multi-theme picker; print and email use light.
