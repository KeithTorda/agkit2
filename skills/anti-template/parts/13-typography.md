---
part: 13
title: Typography
covers: font choice, font count, font loading, type scale, hero size, weights, line-height, line length, letter-spacing, uppercase, italics, numerals, heading hierarchy, alignment, text wrapping, orphans, links, Filipino text
---

# 13 — Typography

Read when: choosing fonts, setting a type scale, styling headings, body text, tables, prices, links, or any page where text is the main content.

## 13.1 Font choice

The same five fonts appear on almost every generated site. A default font is fine when DESIGN.md picks it. It is a tell when nobody picked it.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Inter on every project, no reason given | Default of most starter kits and AI output. The page looks like every other generated page. | Font named in DESIGN.md. If DESIGN.md has none, use the system stack (13.17) and write the choice into DESIGN.md. |
| Poppins for headings and body | Geometric round shapes, wide set, tiring at 14–16px body sizes. Very common in AI landing pages. | Poppins only if DESIGN.md names it, and only for headings. Body in a text face with a tall x-height. |
| Space Grotesk headings on a "tech" page | The standard "developer tool" look since 2021. | Headings in the same family as body, heavier weight. Change family only when DESIGN.md says so. |
| Plus Jakarta Sans, Manrope, Outfit, Sora, DM Sans picked at random | Rotating through the same Google Fonts shortlist. No link to the brand. | One family from DESIGN.md. Record the reason in one line (e.g. "school uses it in printed forms"). |
| Geist / Geist Mono copied from a Vercel template | Signals "copied from a Next.js starter". | Only when DESIGN.md names it. Remove the `next/font/google` import of Geist if unused. |
| Display or script font for body text (Pacifico, Lobster, Playfair at 14px) | Decorative faces break down at small sizes. Reads as a template theme. | Display face for one element at most (logo, page title at 32px+). Body in a text face. |
| Serif headline + sans body "editorial" combo on a POS or admin app | Borrowed from magazine templates. Wrong tone for tools. | One sans family for tools and dashboards. Serif pairing only for editorial or school publication sites, if DESIGN.md says so. |
| Monospace for non-code UI (labels, nav, prices) to look "technical" | Hacker aesthetic trope. Lower legibility, wide set. | Monospace only for code, IDs, reference numbers, OR/receipt numbers if they need fixed width. Otherwise `font-variant-numeric: tabular-nums` on the text face. |
| Handwriting font for "friendly" copy | Cute trope. Hard to read, poor glyph coverage. | Friendly tone comes from plain words (see part 03), not the font. |
| Different font per section of a landing page | Theme-builder look. No system. | One family, maybe two. Sections differ by size and weight only. |
| Font chosen that lacks ₱ (U+20B1) or ñ/Ñ | Fallback font renders the glyph in a different style and width. Visible in every price and in names like Parañaque, Dasmariñas, Peñafrancia. | Check the font file covers U+20B1, U+00D1, U+00F1 before shipping. Load the `latin-ext` subset if needed. Test the string `₱1,250.00 Parañaque Ñ`. |
| Google Fonts `<link>` with 3 families "just in case" | Leftover from generation. Loads unused files. | Load only families used on the page. Delete unused `<link>` and `@import` lines. |

## 13.2 Font count and weights loaded

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| 3+ font families on one page | No system. Original 5.1: "3+ families". | 1 family. Max 2 (one for headings, one for body) when DESIGN.md says so. Code font does not count. |
| 5–9 weights loaded (`wght@100;200;300;400;500;600;700;800;900`) | Copy-pasted Google Fonts URL. Most weights never used. | Load only weights in the scale, usually 400 and 600, maybe 700. Variable font: one file with a limited `wght` range. Perf budget: see part 34. |
| Italic files loaded but no italics used | Copied embed URL. | Drop `ital` axis unless the design uses italics. |
| Weight 100/200 for large headings | "Elegant thin" look. Fails on low-DPI Android screens and projectors. | 400 minimum for any text. Thin weights only if DESIGN.md names them and size is 40px+. |
| 4 weights in one paragraph or card (original 5.1) | Weight used as decoration. No clear emphasis. | 2 weights per block max: regular and one strong weight (600 or 700). |
| `font-weight: 800/900` on every heading | Heavy-by-default hero look. Headings shout at each other. | 600 or 700 for headings. 800+ only for one display element if DESIGN.md calls for it. |
| `font-weight: 500` body text | Medium body looks bold on Windows and blurry on low-end screens. | 400 body. 500 only for UI labels where the family's 400 is too light. |
| Faux bold / faux italic (weight or style requested but file not loaded) | Browser synthesises it. Smeared letter shapes. | Load the file for every weight/style used, or set `font-synthesis: none` and fix the CSS. |

## 13.3 Type scale

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Random sizes: 13px, 15px, 17px, 22px, 27px in one file | No scale. Every component picked its own. | One scale in tokens from DESIGN.md, e.g. `--text-xs` to `--text-3xl`. 6–8 steps total. |
| Too many steps (12+ sizes) | Hierarchy dissolves. Near-identical sizes. | 6–8 steps. Adjacent steps differ by at least 2px at body sizes. |
| Too few steps (everything 16px, headings bold only) | Flat hierarchy, hard to scan. | Distinct sizes for page title, section heading, body, small/meta. |
| Scale ratio copied from a generator (1.618 golden ratio) | Produces 68px+ headings for h1 in apps. | App UIs: ratio 1.125–1.2. Marketing: up to 1.25–1.333. Cap app headings (13.4). |
| Body text 12px or 13px (original 5.1: "12px body") | Dense-looking, hard to read on phones. | Body 16px preferred, 14px minimum for dense tables and admin UIs. 12px only for legal fine print or axis labels, never paragraphs. |
| Fluid `clamp()` on every element | Sizes drift between breakpoints, no two screens match, body shrinks below 16px on small phones. | `clamp()` for page titles and hero headings only. Body and UI text fixed in rem. |
| `clamp(3rem, 8vw, 7rem)` hero | Text scales past readability on 1440px+ and wraps to 1 word per line on phones. | Cap: `clamp(2rem, 1.5rem + 2vw, 3rem)` for marketing. See 13.4 for app pages. |
| Font sizes in px everywhere, including body | Ignores user font-size preference in some browsers. | Sizes in `rem`. Borders and hairlines may stay in px. |
| `vw`-only font sizes (`font-size: 4vw`) | Zoom does not scale it. Fails WCAG 1.4.4 resize text. | `rem` or `clamp()` with a `rem` component. |
| Small text for "cleaner look" on meta rows (11px gray) | Gray + tiny = unreadable for older users. Common on barangay and school audiences. | Meta text 13–14px min, contrast 4.5:1. Color: see part 12. |
| Label text same size as body with no other cue | Form or card has no scanning structure. | Labels 14px weight 600, or smaller size with muted token. Pick one pattern for the whole app. |

## 13.4 Hero and heading size on utility pages

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| 48px+ page title on an app page (original 5.1) | Marketing hero dropped into a tool. Wastes the first screen. | App page titles 24–32px max. Dashboard section headings 16–20px. |
| `text-6xl md:text-7xl font-extrabold tracking-tight` hero | The exact Tailwind hero string of generated landing pages. | `text-3xl` or `text-4xl`, `font-semibold`, default tracking. Larger only for a single marketing hero, per DESIGN.md. |
| Hero headline split across 3 lines with one word highlighted | Gradient or accent-colored keyword. Template signature. | One line or two. Same color for all words. Emphasis through word choice. Gradient text: see part 10. |
| Gradient headings (original 5.1) | Decoration, lower contrast, breaks on selection and in Windows high-contrast mode. | Solid text color token from DESIGN.md, e.g. `var(--color-text)`. |
| Page title larger on the login page than on the dashboard | Auth page styled as a hero. | Auth heading 20–24px: "Sign in". See part 23. |
| h1 + eyebrow + subhead + tagline stack on every page | Four text levels before content starts. | h1 and one optional line of description. No eyebrow on app pages. Eyebrow copy: see part 05. |
| Subhead at 20–24px gray paragraph under every heading | "Lead paragraph" on pages that do not need one. | Delete the subhead, or keep it at body size. |
| Hero headline over 8 words at display size | Wraps to 4 lines. | Headline 3–8 words. Detail goes to body text. |
| Section headings all the same size as h1 | No hierarchy between page and section. | h1 > h2 by one clear step (at least 4px). |
| Stat numbers at 48px on KPI tiles | "Big number" dashboard trope. | 24–32px for the key number. Secondary stats at body size. See part 22. |

## 13.5 Line height

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Body line-height under 1.4 (original 5.1) | Cramped. Hard to track lines on phones. | Body 1.5–1.6. |
| `leading-none` / `line-height: 1` on multi-line headings | Descenders and ascenders collide when the heading wraps. | Headings 1.15–1.3. Test with a 2-line wrap at 390px. |
| Same line-height for 48px heading and 14px caption | Heading looks airy, caption looks cramped. | Line-height shrinks as size grows: 1.6 body, 1.4 small headings, 1.2 large headings. |
| `line-height: 2` on body "for readability" | Lines float apart, paragraph shape breaks. | 1.5–1.6 is enough. |
| Line-height in px (`line-height: 24px`) with rem font sizes | Breaks when the user scales text. | Unitless line-height (`1.5`). |
| Table cells with body line-height 1.6 | Rows too tall, fewer rows per screen. | Table cells 1.3–1.4. Density: see part 19. |
| Buttons with line-height that shifts label off center | Label sits high or low. | Button `line-height: 1.25` or explicit height with flex centering. |

## 13.6 Line length

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Paragraphs spanning 1200px+ full width | 150+ characters per line. Eye loses its place. | `max-width: 65ch` on prose. Range 45–75ch. |
| `max-w-7xl` on an article or policy page | Container meant for grids used for reading text. | Reading column `max-width: 65ch` (about 680–720px at 16px). Layout widths: see part 14. |
| Hero subhead full width, 2 long lines | Hard to read. | `max-width: 50ch` on subheads. |
| Very short measure (25–35ch) on desktop for "elegance" | Choppy reading, too many line breaks. | 45ch minimum except in narrow cards. |
| Centered paragraph blocks over 3 lines | Ragged left edge makes each line start in a new place. | Center only 1–2 line headings and short blurbs. Body text left-aligned. |
| Long government notices and ordinances in a full-width div | Barangay and LGU sites post long text. Full width makes it unreadable. | Prose column at 65ch, headings for each section, numbered clauses kept as `<ol>`. |
| Form help text running under two-column fields full width | Help text line longer than its field. | Help text width matches its field. |

## 13.7 Letter-spacing and uppercase

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Letter-spacing on body text (original 5.1) | Slows reading. Generated to look "premium". | Body `letter-spacing: 0` (font default). |
| `tracking-tight` / `letter-spacing: -0.05em` on every heading | Tight tracking at small sizes cramps letters together. | Default tracking up to 32px. Slight negative (-0.01 to -0.02em) only on 40px+ headings if DESIGN.md says so. |
| `tracking-widest uppercase text-xs` eyebrow above every heading | Template "SECTION LABEL" signature. | Drop the eyebrow. If a label is needed, sentence case, normal tracking. |
| Uppercase everything: nav, buttons, labels, headings (original 5.1) | Shouting. Harder to read, loses word shapes. | Sentence case for headings, buttons, nav. Uppercase only for short labels (2–3 words) like table column headers or status tags, with 0.02–0.05em spacing. |
| Uppercase applied in HTML source ("SAVE CHANGES") | Screen readers may spell it out. Hard to change later. | Write sentence case in source. Use `text-transform: uppercase` in CSS if a label needs caps. |
| Uppercase long Tagalog words in labels (e.g. "PAGPAPAREHISTRO NG BOTANTE") | Long words in caps overflow buttons and tabs. | Sentence case: "Pagpaparehistro ng botante". Check width at 360px. |
| Letter-spaced uppercase buttons (`uppercase tracking-wider`) | Material Design 2016 look, dated. | Sentence case button labels, normal tracking. Button styling: see part 18. |
| Small caps faked with uppercase + smaller size | Stroke weights mismatch. | `font-variant-caps: all-small-caps` if the font supports it, or skip. |
| Negative tracking on uppercase text | Capitals collide. | Uppercase always gets 0 or positive tracking. |

## 13.8 Italics, emphasis and underline

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Italic subheads and taglines | Borrowed from editorial templates. Low contrast. | Regular style. Size and color do the work. |
| Italic for long passages (quotes, testimonials) | Harder to read in long runs. | Italic for titles of works, foreign terms, short emphasis. Quotes in regular with `<blockquote>`. |
| Bold used for emphasis 5+ times per paragraph | Nothing stands out. Bold overuse in copy: see part 02. | Bold for at most one phrase per paragraph, or none. |
| Bold + italic + underline + color on one phrase | Stacked emphasis. | One emphasis device at a time. |
| Underline on non-link text for emphasis | Users click it. | Underline only for links. |
| Pull-quotes in a dashboard (original 5.1) | Magazine device in a tool. | Delete. |
| Highlighted "marker" background behind a keyword in hero | Template trope (`bg-yellow-200` squiggle). | Plain text. |
| Hand-drawn SVG underline under a hero keyword | Template trope. | Delete the SVG. |
| `<i>` or `<b>` for styling | Semantic meaning lost. | `<em>`/`<strong>` for meaning. CSS for pure styling. HTML rules: see part 28. |

## 13.9 Numerals, prices and data text

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Proportional numerals in tables, prices, totals | Columns do not line up. Digits jump when values update. | `font-variant-numeric: tabular-nums` on tables, prices, timers, KPI numbers, receipts. |
| Old-style numerals (dropping 3, 4, 5) in data | Some fonts default to them. Look wrong in figures. | `font-variant-numeric: lining-nums tabular-nums` in data contexts. |
| Number columns left-aligned | Hard to compare magnitudes. | Right-align numbers and currency in tables. Align the header with its column. See part 19. |
| `₱` glyph from a fallback font, different weight | Missing glyph in chosen font. | Pick a font with U+20B1 (13.1). Do not fake the sign with "P" and a strikethrough. |
| "PHP 1250" or "P1250" in UI text | Looks unfinished. Formatting rules for currency: see part 04 and part 09. | Display `₱1,250.00` from a formatter. Typography only needs tabular numerals and a covered glyph. |
| Price with decimals at same size as integer on pricing cards | Heavy visual. | Decimals may be smaller, or omit `.00` on marketing prices. Keep full `.00` on receipts, invoices, BIR-related output. |
| Mixed digit fonts: prices in monospace, rest in sans | Inconsistent. | One family with tabular numerals. |
| Slashed zero forced everywhere | Code-editor look. | Slashed zero (`font-feature-settings: "zero"`) only for IDs, voucher codes, reference numbers where 0/O confusion matters. |
| Phone numbers with inconsistent spacing (09171234567, 0917-123-4567, +63 917 123 4567 on one page) | Visual noise. Formatting rules: see part 09. | One display format per app. Tabular numerals in contact tables. |
| Long reference numbers (OR no., GCash ref no., LRN, precinct no.) breaking mid-number | Hard to read back. | `white-space: nowrap` on short IDs. Group digits with thin spaces only if the format allows. |
| Timers and countdowns shifting width each second | Proportional digits. | `tabular-nums` and fixed min-width. |
| Big animated counter numbers | See part 25. | Show the number. |

## 13.10 Heading hierarchy

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Heading levels chosen by size (h4 because it looked right) | Skipped levels. Outline broken for screen readers. | Choose level by structure. Style with classes. Heading order rules: see part 27. |
| Multiple `h1` per page (logo, hero, section) | Template leftovers. | One `h1` per page: the page title. |
| Logo text as `h1` on every page | Every page has the same h1. | Logo is a link. Page title is the h1. |
| Card titles as `h2`/`h3` inside a list of 50 cards | Outline flooded. | Card titles in a list can be `h3` under a section `h2`, or plain strong text if the list has its own heading. |
| Headings that look like body text (same size, bold only) | No hierarchy. | Step up at least one scale size per level used. |
| Every heading the same weight as body with only color change | Weak hierarchy. | Weight 600+ for headings. |
| Heading with a decorative icon before it on every section | See part 26. | Plain heading text. |
| Heading followed by a divider line and big gap | Template rhythm. | Space above heading larger than space below (e.g. 32px above, 8–12px below). Layout spacing: see part 14. |
| Heading margins equal above and below | Heading floats between sections, not attached to its content. | Margin-top about 2–3x margin-bottom. |
| Emoji in headings | See part 02. | Plain text. |

## 13.11 Alignment

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Justified body text (original 5.1) | Rivers of white space, worse on narrow screens and with long Tagalog words. | `text-align: left` (start). |
| Centered everything: headings, paragraphs, lists, form labels | Landing page reflex applied to all pages. | Left-align body, lists, forms, tables. Center only short headings and single-line blurbs. Layout centering: see part 14. |
| Centered bullet lists | Bullets float at random horizontal positions. | Left-align every list. |
| Right-aligned text in LTR paragraphs for "variety" | Hard to read. | Right-align only numbers in tables. |
| Text vertically centered in tall cards with uneven content | Titles at different heights across a row. | Top-align card content. |
| Mixed alignment within one card (centered title, left body, right button) | No alignment line. | One alignment axis per component. |

## 13.12 Text wrapping, orphans, overflow

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Headings with one orphan word on the last line | Unbalanced. Visible at every width. | `text-wrap: balance` on h1–h3 and short blurbs (up to about 6 lines). |
| Paragraph last line with one short word | Minor, but common. | `text-wrap: pretty` on paragraphs. Fine to omit where unsupported. |
| `<br>` tags to force headline breaks | Breaks at other widths. | Remove `<br>`. Use `text-wrap: balance` and `max-width` in `ch`. |
| `&nbsp;` chains to prevent wraps | Overflow on phones. | `text-wrap: balance`, or `white-space: nowrap` on a short span only (e.g. `₱1,250.00`, `+63 917 123 4567`). |
| Long words or URLs overflowing cards (Tagalog compounds, emails, GCash refs) | Horizontal scroll or clipped text. | `overflow-wrap: anywhere` on user-generated content and URLs. `hyphens: auto` with correct `lang` for prose. |
| Single-line `truncate` on titles that users must read (names, addresses, product names) | Information lost, no way to see it. | Allow 2 lines with `line-clamp: 2`, show full text on the detail page, and add `title` only as a backup. Truncation rules: see part 04. |
| `line-clamp: 3` on every card description | Template sameness. | Clamp only where the full text is reachable one click away. |
| Text in fixed-height boxes (`h-12` on a label) | Clips when translated to Filipino or when user zooms. | `min-height` or no height. Fixed heights on text: see part 11. |
| Button labels that wrap to 2 lines in Filipino | Tagalog strings run 20–40% longer than English. | Test both languages at 360px. Allow wrap or shorten copy. Do not shrink the font. |
| `hyphens: auto` without `lang` | Wrong or no hyphenation. | Set `lang="en"` or `lang="fil"` on the element. See part 27. |
| Ellipsis in the middle of numbers (₱1,2…) | Wrong value shown. | Never truncate numbers. Shrink the column or wrap. |

## 13.13 Links

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Links in body text with underline removed | Link indicated only by color. Fails for color-blind users. | Underline links inside prose. `text-underline-offset: 0.15em`, `text-decoration-thickness: 1px` or `from-font`. |
| Link color same as body, bold only | Not recognisable as a link. | Link color token from DESIGN.md plus underline in prose. |
| Animated underline slide-in on every link | Decorative motion. Original 2.2: allowed on one or two nav links at most. | Static underline. Hover changes thickness or color only. |
| Gradient underline | Template decoration. | Solid underline in current color. |
| "Click here" / "Read more" link text | Copy problem. See part 03. | Link text names the target. |
| Visited style removed on content-heavy sites (notices, announcements) | Users lose track of what they read. | Keep `:visited` on article and notice lists. |
| Links styled as buttons inside paragraphs | Breaks reading flow. | Inline links as text. Buttons for actions. See part 18. |
| External link icon on every link | Visual noise. | Icon only for links that leave the site or open files (PDF). State "PDF, 1.2 MB" in text. |
| Nav links underlined permanently | Nav is a list of links; underline adds noise. | Nav links without underline, clear active state. See part 16. |

## 13.14 Font loading and rendering

Performance budgets for fonts live in part 34. This section covers what the user sees.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| No `font-display` set | Invisible text (FOIT) for up to 3s on slow PH mobile data. | `font-display: swap` for body text. `optional` for decorative faces. |
| Big layout jump when the web font swaps in (FOUT with shift) | Fallback metrics differ. Content moves. | Fallback `@font-face` with `size-adjust`, `ascent-override`, `descent-override`. Or use `next/font`, which generates these. |
| Loading fonts via `@import` inside CSS | Chains requests, slower first paint. | `<link rel="preconnect">` then `<link rel="stylesheet">`, or self-host woff2. |
| Preloading every font file | Competes with critical resources. | Preload only the body weight woff2 used above the fold. |
| TTF/OTF served to browsers | Large files. | woff2 only. |
| Icon font loaded for text rendering fixes | See part 26 and 34. | SVG icons. |
| `-webkit-font-smoothing: antialiased` on everything, including light text on light bg | Thins text on macOS. Copied from starter CSS. | Apply only on light-on-dark text if DESIGN.md wants it. Otherwise leave default. |
| `text-rendering: optimizeLegibility` on the whole body | Slow on long pages and low-end Android. | Remove, or scope to headings. |
| `font-feature-settings` blocks copied from a starter (`"cv02","cv03","cv04","cv11"`) | Inter-specific settings pasted into projects with other fonts. | Delete unless the chosen font supports them and DESIGN.md wants them. |
| Font file hosted on a third-party CDN with `@latest` | Can change or disappear. See part 34. | Self-host or pin a version. |

## 13.15 Tailwind and Bootstrap specifics

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `text-5xl font-extrabold tracking-tight lg:text-6xl` on page titles | shadcn/landing boilerplate. | `text-2xl font-semibold` for app titles. Marketing hero size from DESIGN.md. |
| `bg-clip-text text-transparent bg-gradient-to-r from-purple-600 to-pink-600` on headings | Gradient text. See part 10. | `text-[color:var(--color-text)]` or a theme color mapped to the token. |
| `text-muted-foreground text-sm` on every description, including primary content | Everything below the title fades out. | Muted only for meta and help text. Main content at normal color. |
| `uppercase tracking-widest text-xs font-semibold text-indigo-600` eyebrow | Template eyebrow. | Remove. |
| `font-mono` on numbers | Hacker look. | `tabular-nums`. |
| `leading-tight` on paragraphs | Cramped body. | `leading-relaxed` or `leading-normal` (1.5–1.625). |
| `max-w-prose` missing on article pages | Full-width text. | `max-w-prose` (65ch) on reading columns. |
| Arbitrary sizes `text-[13px]`, `text-[17px]`, `leading-[1.1]` | No scale. See part 11. | Extend `theme.fontSize` with DESIGN.md tokens. Use named sizes. |
| `prose` plugin applied to the whole app | Typography plugin styles leak into UI components. | `prose` only on rendered Markdown or article bodies. |
| Bootstrap `display-1` / `display-4` on dashboard headings | Marketing display sizes in admin. | `h4`/`fs-4` scale for admin page titles. |
| Bootstrap `lead` class on every paragraph | Oversized body. | `lead` once per page at most, under the main heading. |
| Bootstrap `text-uppercase fw-bold small` on labels everywhere | Uppercase soup. | Set label style once in Sass (`$form-label-font-weight`). |
| Overriding Bootstrap fonts with `!important` in a custom.css | Override hell. See part 29. | Set `$font-family-sans-serif`, `$font-size-base`, `$headings-font-weight` in Sass variables. |

## 13.16 Filipino and bilingual text

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Layout tuned only for English string lengths | Tagalog labels are longer ("I-save ang mga pagbabago"). Tabs, buttons and table headers overflow. | Test every fixed-width UI element with the Filipino string. Allow wrap. See 13.12. |
| Font without ñ/Ñ or with ñ from fallback | Place and family names show a mismatched glyph. | Check coverage (13.1). Load `latin-ext`. |
| Hyphenating Tagalog with English rules | `hyphens: auto` under `lang="en"` splits words wrongly. | Set `lang="fil"` on Filipino blocks. If unsure, `hyphens: manual`. |
| Bilingual page with English and Filipino in the same weight and size side by side | No reading order. | Primary language at body style. Secondary in the same size, below or in a separate column, with its own `lang`. Bilingual copy rules: see part 09. |
| Baybayin script added as decoration in headings | Cultural decoration trope. Most fonts lack the glyphs. | Only when the client provides the text and a font that covers U+1700 block. |
| Uppercase for official names of offices ("SANGGUNIANG BARANGAY NG ...") in body text | Copied from letterheads. Hard to read in paragraphs. | Title case in body text ("Sangguniang Barangay ng San Isidro"). Uppercase only in the letterhead or seal line if the client's official template uses it. |
| Official titles set in italics ("*Hon.* Juan Dela Cruz") | Template styling. | Plain text. Official-name rules: see part 09. |

## 13.17 Code: banned vs use

```css
/* Banned: generated hero and body typography */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&family=Poppins:wght@400;700&family=Space+Grotesk:wght@700&display=swap');

h1 {
  font-size: clamp(3rem, 8vw, 7rem);
  font-weight: 900;
  letter-spacing: -0.05em;
  line-height: 1;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-transform: uppercase;
}
p {
  font-size: 13px;
  line-height: 1.3;
  letter-spacing: 0.02em;
  text-align: justify;
}
.eyebrow { text-transform: uppercase; letter-spacing: 0.3em; font-size: 11px; }
```

```css
/* Use: tokens from DESIGN.md, one family, short scale */
:root {
  --font-sans: var(--brand-font, system-ui, -apple-system, "Segoe UI", Roboto, "Noto Sans", Arial, sans-serif);
  --font-mono: ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace;

  --text-sm: 0.875rem;   /* 14px */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.125rem;   /* 18px */
  --text-xl: 1.25rem;    /* 20px */
  --text-2xl: 1.5rem;    /* 24px */
  --text-3xl: 1.875rem;  /* 30px */
}

body {
  font-family: var(--font-sans);
  font-size: var(--text-base);
  line-height: 1.5;
  color: var(--color-text);
}

h1, h2, h3 {
  line-height: 1.25;
  font-weight: 600;
  text-wrap: balance;
}
h1 { font-size: var(--text-3xl); }   /* app page title, 30px max */
h2 { font-size: var(--text-xl); margin: 2rem 0 0.5rem; }

p { max-width: 65ch; text-wrap: pretty; }

.prose a { text-decoration: underline; text-underline-offset: 0.15em; }

table, .price, .total, .timer { font-variant-numeric: tabular-nums lining-nums; }
td.num, th.num { text-align: right; }

.label-caps { text-transform: uppercase; letter-spacing: 0.04em; font-size: var(--text-sm); }
```

```html
<!-- Banned: every weight, two extra families -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

<!-- Use: one family, weights in the scale, latin-ext for ñ and ₱ where the font splits subsets -->
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Brand+Font:wght@400;600&display=swap" rel="stylesheet">
```

## 13.18 Check

- [ ] Font family comes from DESIGN.md, or the system stack is used and recorded.
- [ ] No Inter/Poppins/Space Grotesk/Plus Jakarta/Geist unless DESIGN.md names it.
- [ ] 1 family, max 2. Code font excluded from the count.
- [ ] Only weights in use are loaded. No 100–900 range URLs.
- [ ] No unused font `<link>` or `@import` lines.
- [ ] The font covers ₱ (U+20B1), ñ and Ñ. Tested with `₱1,250.00 Parañaque Ñ`.
- [ ] One type scale in tokens, 6–8 steps, sizes in rem.
- [ ] No arbitrary sizes (`text-[13px]`, `font-size: 17px`) outside the scale.
- [ ] Body 16px, 14px minimum in dense UIs. No 12px paragraphs.
- [ ] App page titles 24–32px. No 48px+ headings on utility pages.
- [ ] No `font-extrabold tracking-tight` hero string on app pages.
- [ ] No gradient headings or gradient text.
- [ ] Max 2 weights per text block. Body at 400.
- [ ] No weight below 400 for text.
- [ ] Body line-height 1.5–1.6. Headings 1.15–1.3. Unitless.
- [ ] Prose width 45–75ch (`max-width: 65ch`).
- [ ] Body letter-spacing 0. Negative tracking only on 40px+ headings.
- [ ] Uppercase only on short labels. Source text in sentence case.
- [ ] No eyebrow labels above every section.
- [ ] No italic subheads or italic long passages.
- [ ] Bold used at most once per paragraph.
- [ ] Tables, prices, totals, timers use `tabular-nums`.
- [ ] Numbers right-aligned in tables. Never truncated.
- [ ] One `h1` per page. Heading levels follow structure, not size.
- [ ] Heading margin-top larger than margin-bottom.
- [ ] Body text left-aligned. No justified text.
- [ ] Centering limited to short headings and 1–2 line blurbs.
- [ ] `text-wrap: balance` on headings, `pretty` on paragraphs.
- [ ] No `<br>` or `&nbsp;` chains used to shape headlines.
- [ ] Long URLs, emails and reference numbers do not overflow at 360px.
- [ ] No fixed heights on text containers.
- [ ] Filipino strings tested in buttons, tabs and headers at 360px.
- [ ] `lang` set on Filipino blocks where hyphenation applies.
- [ ] Links in prose are underlined. No animated underline on every link.
- [ ] `font-display: swap` set. No large layout shift when the font loads.
- [ ] Fonts served as woff2, self-hosted or pinned.
- [ ] No copied `font-feature-settings` from another font.
- [ ] Bootstrap fonts set through Sass variables, not `!important` overrides.
