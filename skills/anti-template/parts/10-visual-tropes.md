---
part: 10
title: Visual Tropes
covers: glassmorphism, frosted headers, neon glow, gradient text, gradient borders, border beams, shimmer buttons, aurora and mesh gradients, blobs, orbs, floating shapes, grain and noise, dot and grid backgrounds, spotlight effects, sparkles, wave dividers, black "vercel-style" hero, glowing "New" pill, oversized hero, hero plus three features, alternating sections, fake browser and terminal chrome, tilted screenshots, logo marquees, bento grids, 3D tilt cards, cards in cards, identical card grids, gradient icon tiles, emoji icons, split auth pages, neumorphism, skeuomorphism, claymorphism, neo-brutalism, component-library copy-paste looks
---

# 10 — Visual Tropes

Read when: designing or reviewing any page's look, especially landing pages, heroes, marketing sections, auth pages, dashboards and portals. Pair with part 11 for the CSS behind each trope and part 12 for colour.

Guidance: DESIGN.md and the brief override this part.

The test for every trope: does it carry information, or does it only say "this was made in 2024 with a template"? If it carries nothing, remove it and let the content be the visual.

## 10.1 Surface effects

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Glassmorphism on cards, panels and modals (translucent white fill, `backdrop-filter: blur`, thin white border) | Every AI tool and UI kit defaults to it. Text contrast changes with whatever is behind | Solid surface from DESIGN.md with a 1px border, or a surface 2–4 steps different from the page. Glass only if DESIGN.md defines it |
| Frosted or blurred sticky header | Same default. Content scrolling under blur is hard to read and costly on low-end phones | Solid opaque header, `var(--color-surface)`, 1px bottom border |
| Neon glow shadows around cards, buttons, inputs (`0 0 20px` in indigo or violet) | Crypto-dashboard aesthetic. Glow means nothing | `0 1px 2px` neutral shadow or none. See part 11 |
| Glow on focus rings that replaces the outline | Looks nice, fails as a focus indicator on light backgrounds | Solid 2px outline with 2px offset. See part 27 |
| Gradient text on headlines (`background-clip: text`) | Pure decoration. Hurts readability. Among the most common AI hero tells | Solid text colour token from DESIGN.md |
| Gradient border cards (1px animated or static gradient ring around a card) | Aceternity/MagicUI signature | 1px solid border token. Highlight a chosen item with a heavier border or a label, not a rainbow |
| Animated border beam (light travelling round the card edge) | Copy-pasted component. Constant motion pulls attention from content | Static border. Remove |
| Shimmer or shine sweep across buttons | Draws the eye every 2 seconds for no reason | Plain button. Hover changes background token |
| Glowing "pulse" dot beside "Live", "Online", "Available" | Suggests real-time data that often is not | Static dot only when status is real. See part 01 for "Live" labels and part 25 for pulse |
| Grain or noise texture overlay on the whole page | Trendy film texture. Adds bytes, lowers text contrast, looks dirty on low-DPI screens | Flat surface |
| Inner glow on inputs (`inset 0 0 30px`) | Decoration on a working control | 1px border; border colour change on focus plus outline |
| Text shadow on body or headings | Blurry type. Glow text is a dated game-UI look | No text shadow. For text on images, see 10.3 on overlays |
| Coloured drop shadows matching the element colour (purple shadow under purple button) | Tailwind `shadow-indigo-500/50` signature | Neutral shadow or none |
| Everything elevated: every card, header, dropdown and table with a large soft shadow | Elevation loses meaning when all is raised | Shadow only on things that float above the page: menus, popovers, dialogs, toasts |

## 10.2 Backgrounds

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Aurora or mesh gradient hero background (blurred purple, pink and blue clouds) | The default AI landing page backdrop | Flat page background token. Content and product image carry the page |
| Blobs: absolutely positioned circles with `filter: blur(80px)` behind content | Decorative shapes with no meaning; they also leak colour into text areas | Delete. No blobs |
| Floating orbs, spheres or glass balls drifting on scroll | 3D decoration from template kits | Delete |
| Floating or overlapping decorative shapes (rings, squiggles, triangles at odd angles) | Template filler | Delete. Whitespace |
| Dot-grid or line-grid background fading out behind the hero | Vercel/Linear imitation, repeated everywhere | Plain background. A grid is fine on a canvas tool where the grid is real |
| Radial spotlight behind the headline | Stage lighting on text | Delete |
| Cursor-following spotlight or glow | Gimmick; nothing on touch devices; costs frames | Delete |
| Sparkles, stars, confetti particles in the background | Decoration signalling "magic" | Delete |
| Animated gradient background shifting colour over 15 seconds | Constant motion, GPU cost, battery drain on phones | Static flat background |
| Decorative gradients on content areas (gradient page headers in a dashboard, gradient table header) | Data screens need calm surfaces | Flat surface. One subtle gradient on a marketing hero is the maximum, and only if DESIGN.md has it |
| Wave or slanted SVG section dividers | Template rhythm device | 1px border or spacing between sections |
| Gradient horizontal rules (`<hr>` fading at both ends) | Decoration on a separator | 1px solid border token |
| Diagonal clip-path section edges | Same | Straight edges |
| Full-bleed colour sections alternating (white, gray, brand, white, dark) | Marketing template rhythm | One consistent background. Separate sections with spacing and headings |
| "Vercel-style" black hero: pure black, white headline, grid fade, gradient text, one glowing button | Copied so often it identifies the tool, not the brand | Brand palette from DESIGN.md. Light background is fine. See part 12 for pure black |
| Dark mode plus neon accents as the default look | The AI default for "modern" | DESIGN.md palette. Light mode as default unless the client asks. See part 34 |
| Background video loop behind the hero | Heavy on mobile data, distracting, hard to read over | Static image or none. See part 26 |
| Repeating pattern backgrounds (circuit boards, hexagons, topography lines) | Tech-flavoured wallpaper | Flat background |

## 10.3 Heroes and page templates

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Hero + 3 feature cards + CTA band + footer | The default AI landing page. Every page looks the same | Plan the page from the content: what the visitor needs first, second, third. See part 24 |
| Glowing "New" or "Announcing v2" pill above the hero headline, with an arrow | Copied from startup sites; usually announces nothing | Delete. Put real news in a dated changelog or news section |
| Oversized hero: `min-height: 100vh` on a tool, portal or dashboard | Pushes content below the fold | Content visible without scrolling. Utility pages start with the task |
| Hero on every page | Only the homepage needs one, if any | Interior pages start with an H1 and content |
| Huge centred headline + one-line subhead + two buttons ("Get started", "Learn more") | The shape itself is the tell | Left-aligned headline stating what it is, a short paragraph, one primary action with a literal label. See part 05 |
| Giant icon (Lucide rocket, Heroicon bolt) as the hero visual | Stand-in for a real image | Product screenshot, real photo, data preview, or nothing |
| Product screenshot tilted in 3D perspective with a glow under it | Launch-page cliché | Flat screenshot at 1:1 scale, cropped to the part that matters, 1px border |
| Fake browser chrome (three traffic-light dots, fake URL bar) around every screenshot | macOS window frame as decoration | Plain screenshot with a border. Browser frame only when the URL is the point |
| Terminal mockup with typing animation of a fake command | Developer-tool cliché, often for products with no CLI | Real command in a `<pre>` block if a CLI exists. Otherwise delete |
| Fake code editor window with syntax highlighting of made-up code | Decoration pretending to be product | Real code sample the user can copy, or nothing |
| Floating UI fragments (notification card, chart card, avatar card) scattered around the hero | Mock collage from Dribbble | One real screenshot |
| Phone mockup with a fake app screen | Implies an app that may not exist | Real screenshot in the device frame only if the app exists |
| Gradient overlay on a hero photo to make text readable | Muddy image, purple tint | Put text beside the image, or on a solid band. If text must sit on a photo, a neutral dark scrim at fixed opacity tested at 4.5:1. See part 12 |
| Transparent header over hero image | Nav readability depends on the photo | Solid header, or a guaranteed dark overlay tested for contrast |
| Stats band ("10k+ users · 99.9% uptime · 24/7 support") in big gradient numbers | Invented figures in display type | Real numbers with a source, inline in text. See part 05 |
| Logo marquee (infinite scrolling row of grayscale logos) | Motion plus fake social proof | Static row of real client logos with permission, or none. See part 26 |
| Testimonial wall in masonry cards with avatars and 5 stars | Often invented people | Real quotes with name and role, max 3. Or none |
| Pricing: 3 cards, middle one scaled up with a gradient border and "Most popular" ribbon | Every SaaS template | Plain table or cards of equal size. Mark a recommended plan with a text label if true |
| Final CTA band in brand gradient with centred "Ready to get started?" | Template closer | End with contact info or the next real step in plain layout |
| Zig-zag feature rows (image left text right, then swapped, 4 times) | Template rhythm | Consistent alignment. One column of features with screenshots at the same position |
| "How it works" with three numbered circles joined by a dashed line | Timeline decoration for three obvious steps | Numbered list `<ol>` with one line per step |
| FAQ accordion on every page | Template default | FAQ only for real questions users ask. Plain headings and paragraphs work if there are fewer than 6 |
| Split-screen auth page (illustration or gradient left, form right) | Default auth template | Centred form on a plain surface. See part 23 |
| Coming-soon page with countdown, blob and email capture | Template | One line of what is coming and a date if known |
| Full-screen loading splash with logo animation | Delays content | Render the page. See part 25 |

## 10.4 Cards and components

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Bento grid (mixed-size rounded tiles, each with an icon, title, blurb and decorative graphic) | Apple keynote copied into every template | A list or two-column layout of what the product does, with real screenshots where helpful |
| Icon + title + vague sentence cards in a 3-column grid | Filler that says nothing concrete | For tools, skip. For services, a list with specific facts: fee, time, requirement |
| Identical card grid used for stats, feeds, people and settings | Same container for different content | Table for data, list for feeds, inline text for metadata, `<dl>` for key-value. See part 19 |
| Cards inside cards (card → section card → item card) | Nesting destroys hierarchy; three sets of borders and padding | One level of card. Inside it, dividers and spacing |
| Everything in a card with a shadow | No page surface left | Content on the page surface. Cards only for items that are separate and movable. See part 14 |
| 3D tilt cards that rotate toward the cursor | Gimmick; nothing on touch; motion sickness risk | Static card. Hover changes background token |
| Hover lift and scale on every card (`translateY(-4px)`, `scale(1.05)`) | Motion that suggests the card is a button when it may not be | No transform. If the whole card is a link, change background on hover and show focus outline |
| Gradient icon tiles (icon in a rounded square filled with a gradient) | Signature of AI feature grids | Icon in text colour, or no icon |
| Different colour per card icon (blue, green, purple, orange) | Decoration by colour | One neutral icon colour. See part 12 |
| Emoji as icons (🚀 Fast, 🔒 Secure, ⚡ Powerful) | The strongest single AI tell in UI | SVG icon from the one set in use, or text only. See part 26 |
| Decorative icon on every heading | Noise | Icons only where they help scanning: nav, buttons, file types |
| Avatar stack "Join 2,000+ others" with stock faces | Fake social proof | Delete |
| Star rating rows on testimonials | Unverifiable | Delete unless from a real review platform with a link |
| Big number badges (1, 2, 3) in gradient circles for steps | Template | `<ol>` with plain numbering |
| Glowing "Popular", "New", "Hot 🔥" ribbons on corners | Retail clichés | Plain text label when true |
| Pill tags with gradient fill | Decoration on metadata | Solid neutral pill, 1px border or muted background token |
| Rounded everything at 24px+ (tables, inputs, thread lists) | Bubbly toy look on dense UIs | Radius scale from DESIGN.md. Typical: 4px inputs, 8px cards and dialogs, full pill only for chips, badges, avatars. See part 11 |
| Oversized empty-state illustrations (Undraw, isometric people) | Template filler | One line of text and an action. See part 04 and part 26 |
| Masonry layout for non-image content | Uneven reading order | List or table |
| Horizontal carousels for content that fits on screen | Hides items, adds controls | Show all, or a grid that wraps |

## 10.5 Style families that read as AI defaults

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Neumorphism (soft extruded buttons, light and dark shadows on the same colour) | 2020 trend; low contrast; controls hard to find | Flat surfaces with borders |
| Skeuomorphism (leather, paper, wood, brushed metal textures) | Fake material | Flat colour |
| Claymorphism (puffy 3D clay shapes, inner highlights, pastel) | Trend kit look | Flat illustration from the client, or none |
| Neo-brutalism by default (thick black borders, hard offset shadows, clashing flat colours, Space Grotesk) | Became a template trend itself | Use only when DESIGN.md chooses it. Otherwise the project's normal system |
| Y2K / retro chrome / cyberpunk neon for a business client | Theme instead of design | DESIGN.md palette and type |
| Dribbble-shot look: pastel gradients, oversized rounded cards, floating widgets, no real data | Built for screenshots, not use | Real content and data in the layout from the start |
| shadcn/ui default unchanged (zinc grays, `rounded-md`, Inter, subtle border, `muted-foreground` everywhere) | Recognisable at a glance as "default shadcn" | Keep the components; change tokens to DESIGN.md colours, radius, type. See part 31 |
| Aceternity UI / Magic UI copy-paste (spotlight, beams, meteors, lamp effect, sparkles text, 3D card, globe) | Effects exist to be demoed, not to serve content | Do not install these for client sites. Remove if present |
| Tailwind UI / Flowbite template untouched (same hero, same "Trusted by" row, same footer) | Recognisable template | Use the structure only if it fits; replace copy, tokens and imagery |
| Bootstrap 5 default look (primary blue buttons, jumbotron, `.card` grid, `shadow-lg`) | Default theme, nothing changed | Bootstrap themed through Sass variables to DESIGN.md. See part 29 |
| Admin template look (AdminLTE, CoreUI, Material Dashboard): coloured stat boxes with big icons, gradient sidebar | Template signature | Neutral admin: sidebar with text, compact tables, one accent. See part 22 |
| Material 2 look by default (floating action button, ripple, raised buttons) on a web app | Mobile pattern on desktop | Only when DESIGN.md chooses Material |
| Glassy dark "AI product" look (black, purple glow, chat bubble with sparkles icon) | The look of AI startups | DESIGN.md palette; sparkle icon only if the feature is actually AI and the client wants it marked |

## 10.6 Motion-driven visuals

Timing and easing live in part 25. This table lists the visual tropes only.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Parallax layers on scroll | Nausea risk, jank on mid-range phones | No parallax |
| Every section fades or slides in on scroll | Content hidden until the user scrolls; blank screenshots and print | Content renders in place |
| Typing effect in the hero headline cycling words ("Build faster / smarter / better") | Gimmick; screen readers get noise | Static headline |
| Number counters rolling up to stats | The number arrives late | Show the number |
| Marquee rows (logos, testimonials, keywords) | Constant motion | Static row or list |
| Orbiting icons around a central logo ("integrations orbit") | Decorative animation | Static list of real integrations |
| Animated globe with arcs | Implies global scale most projects do not have | Delete |
| Confetti on sign-up or payment | Celebration nobody asked for | A plain success message. See part 03 |
| Lottie animations for simple states | Heavy files for a checkmark | Static icon or text |

## 10.7 Philippine-flavoured tropes

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Philippine flag colours as a gradient hero (blue to red with a yellow sun) | Flag used as decoration | See part 09 on national symbols. DESIGN.md palette |
| Sun rays graphic behind LGU headings | Borrowed national motif | Plain heading. Seal once in the header |
| Jeepney, banig or capiz patterns as page backgrounds | Cultural texture as wallpaper | Plain background. Use cultural art only as supplied content |
| Seal as giant faded watermark | Decoration of an official mark | See part 09 |

## 10.8 Tailwind and component fingerprints

These class combinations identify generated pages on sight. Each has a plainer replacement. Detailed CSS rules are in part 11.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `bg-gradient-to-r from-purple-500 to-pink-500` (or `from-indigo-500 via-purple-500 to-pink-500`) | The Tailwind AI gradient | `bg-[var(--color-primary)]` or a theme colour from the config mapped to DESIGN.md |
| `bg-clip-text text-transparent bg-gradient-to-r ...` | Gradient text | `text-[var(--color-text)]` or theme `text-foreground` |
| `backdrop-blur-xl bg-white/10 border border-white/20` | Glassmorphism | `bg-surface border border-border` from theme tokens |
| `shadow-2xl shadow-indigo-500/50` | Coloured glow shadow | `shadow-sm` or none |
| `rounded-3xl` on cards, `rounded-full` on buttons in a data app | Bubbly defaults | Theme radius tokens: `rounded-md` / `rounded-lg` mapped to DESIGN.md |
| `hover:scale-105 transition-all duration-300` | Hover zoom | `hover:bg-surface-alt transition-colors duration-150` |
| `hover:-translate-y-1 hover:shadow-xl` | Hover lift | Background change only |
| `animate-pulse` on real content or badges | Pulse as decoration | Remove. `animate-pulse` only on skeletons shown over 500ms |
| `absolute -z-10 h-72 w-72 rounded-full bg-purple-500/30 blur-3xl` | Blob | Delete the element |
| `bg-[radial-gradient(...)]`, `bg-grid-white/[0.05]`, `[mask-image:radial-gradient(...)]` | Spotlight and grid-fade backdrops | Delete |
| `ring-1 ring-white/10` on everything in dark mode | Glass edge | `border border-border` |
| `text-5xl md:text-7xl font-extrabold tracking-tight` on every H1 | Hero type on all pages | Type scale from DESIGN.md. See part 13 |
| `inline-flex items-center rounded-full border px-3 py-1 text-sm` + "✨ New" above H1 | Glowing pill | Delete |
| Bootstrap `.jumbotron` / `.bg-gradient` / `.shadow-lg` on every card | Default theme | Themed Sass variables; `.shadow-sm` or none |

## 10.9 Code: banned and replacement

```css
/* Banned: glass card */
.card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 0 20px rgba(139, 92, 246, 0.4);
  border-radius: 24px;
}

/* Use: solid surface */
.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-card);
}
```

```css
/* Banned: aurora hero with blobs and gradient text */
.hero { background: radial-gradient(at 20% 30%, #6366f1 0, transparent 50%),
                    radial-gradient(at 80% 0%, #ec4899 0, transparent 50%), #000; }
.blob { position: absolute; width: 400px; height: 400px; border-radius: 50%;
        background: #8b5cf6; filter: blur(80px); opacity: .5; }
.hero h1 { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
           -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

/* Use: flat hero */
.hero { background: var(--color-bg); padding-block: var(--space-12); }
.hero h1 { color: var(--color-text); }
```

```html
<!-- Banned: fake window chrome and glowing pill -->
<div class="pill glow">✨ Announcing v2.0 →</div>
<div class="window">
  <div class="dots"><span></span><span></span><span></span></div>
  <img src="dashboard.png" style="transform: perspective(1000px) rotateX(12deg)">
</div>

<!-- Use: plain screenshot with caption -->
<figure class="screenshot">
  <img src="orders-list.png" width="1200" height="750"
       alt="Orders list filtered to unpaid orders, 14 rows">
  <figcaption>Unpaid orders, filtered by branch.</figcaption>
</figure>
```

```html
<!-- Banned: emoji icon feature grid -->
<div class="grid grid-cols-3 gap-8">
  <div class="rounded-3xl p-8 shadow-2xl">
    <div class="h-12 w-12 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600">🚀</div>
    <h3>Blazing Fast</h3><p>Experience unparalleled speed.</p>
  </div>
  ...
</div>

<!-- Use: a list with facts -->
<ul class="facts">
  <li><strong>Offline sales.</strong> The POS keeps selling when the internet drops and syncs when it returns.</li>
  <li><strong>BIR-ready reports.</strong> X- and Z-readings export as PDF and CSV.</li>
  <li><strong>Branch stock.</strong> Transfer items between branches with a receiving slip.</li>
</ul>
```

## 10.10 What to put in place of a trope

When a trope is removed, the space should not be refilled with another one. Use this order.

| Space left by | Fill with | Notes |
|---|---|---|
| Hero background effect | Nothing. Flat background | The headline and a real image are enough |
| Hero visual (icon, orb, globe, mockup collage) | One real screenshot, or a real photo from the client | No screenshot yet → no visual. Text-only hero is fine |
| Feature card grid | A list of specific facts, or screenshots with captions | Each item names a concrete thing: a report, a limit, a price, a time |
| Stats band | One or two real numbers in running text with a date | "Serving 14 barangays since 2021." |
| Logo marquee | Static logos with permission, or a single line "Used by …" | Or nothing |
| Testimonial wall | Up to 3 real quotes, or none | Name, role, organisation. No stock faces |
| Decorative section dividers | Spacing token and a heading | `margin-block: var(--space-12)` |
| Card shadow and glow | 1px border | Or no container at all |
| Gradient accent | One solid accent token | See part 12 |
| Animated reveal | Nothing | Content renders in place |

## 10.11 Check

- [ ] No `backdrop-filter` on cards, panels, dialogs or headers unless DESIGN.md defines glass.
- [ ] No glow shadows (`0 0 Npx` with colour) anywhere.
- [ ] No gradient text (`background-clip: text`, `text-transparent bg-clip-text`).
- [ ] No gradient borders, border beams, shimmer sweeps or animated outlines.
- [ ] No blobs, orbs, floating shapes, aurora or mesh gradient backgrounds.
- [ ] No dot-grid or line-grid backdrops, radial spotlights, cursor spotlights or sparkles.
- [ ] No grain or noise overlay.
- [ ] No wave, slant or gradient section dividers.
- [ ] No alternating full-bleed coloured sections.
- [ ] No animated gradient backgrounds, background video or parallax.
- [ ] Header is solid and opaque.
- [ ] No glowing "New" pill above the hero.
- [ ] Hero exists only where needed and does not fill 100vh on tools and portals.
- [ ] Hero visual is a real screenshot or photo, or nothing. No giant icon, no tilted mockup, no fake window chrome, no fake terminal.
- [ ] Page structure is not hero + 3 features + CTA by default.
- [ ] No stats band with invented numbers, no logo marquee, no fake testimonial wall.
- [ ] Pricing cards are equal size; no scaled "Most popular" card with gradient border.
- [ ] No bento grid unless the content really has mixed sizes.
- [ ] No 3D tilt, hover lift or hover scale on cards.
- [ ] No cards inside cards. Not everything is in a card.
- [ ] No identical card grid used for stats, feeds and people alike.
- [ ] No gradient icon tiles; icons share one neutral colour.
- [ ] No emoji used as icons.
- [ ] No decorative icon on every heading.
- [ ] Radius follows the DESIGN.md scale; no 24px+ on tables, inputs or lists.
- [ ] Shadows only on floating layers (menus, popovers, dialogs, toasts).
- [ ] Auth page is a centred form, not split-screen.
- [ ] No neumorphism, skeuomorphism, claymorphism or unrequested neo-brutalism.
- [ ] shadcn, Tailwind UI, Flowbite or Bootstrap defaults re-themed to DESIGN.md tokens.
- [ ] No Aceternity/Magic UI effect components on client sites.
- [ ] No flag gradients, sun rays, seal watermarks or cultural patterns as wallpaper.
- [ ] Every removed trope left empty space or real content, not a different trope.
