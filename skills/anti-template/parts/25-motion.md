---
part: 25
title: Motion
covers: entrance animations, stagger, scroll-triggered reveals, hover lift and scale, parallax, counters, typing effect, confetti, pulse, marquee, page transitions, loading motion, durations, easings, reduced motion, Framer Motion, GSAP, AOS, Lottie
---

# 25 — Motion

Read when: adding any animation, transition, hover effect, loading indicator, scroll effect, or motion library to a page or component.

Guidance: DESIGN.md and the brief override this part.

## 25.1 Default rule

Content renders in place, at full opacity, on first paint. Motion is allowed only when it explains a change of state the user caused or needs to notice: something opened, closed, moved, was added, was removed, or is still working. If the animation would play with no user action and no state change, delete it.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Every section fades or slides in on page load | Template default from AOS, Framer Motion and "landing page" prompts; nothing changed, so nothing needs animating | Render all content immediately. No entrance animation |
| Animation added "for polish" with no stated purpose | Motion as decoration is the clearest generator tell | Write the purpose in one line (e.g. "drawer opens from the side it lives on"). No purpose, no animation |
| Motion on a utility screen (POS, admin table, form, voter lookup) | These screens are used hundreds of times a day; motion becomes delay | Zero decorative motion on tools. State-change transitions only, 150 ms max |
| Same fade-up applied to headings, paragraphs, images, buttons | One reusable `fadeInUp` wrapped around everything | Remove the wrapper component. Elements do not need individual entrances |
| Motion used to make a static page "feel alive" | A page with nothing live does not need to move | Accept a still page. Stillness reads as confident |
| Animations on first load of a government or school portal | Users on slow Android phones wait longer and see blank sections | Server-render content visible. No JS-gated reveal |

## 25.2 Entrance animations and stagger

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `opacity: 0; transform: translateY(20px)` as the initial state of sections | If JS fails or is slow, content stays invisible; common AI starter CSS | Initial state is visible. No hidden-until-animated CSS |
| Staggered children: cards appear one by one 100 ms apart | "staggerChildren: 0.1" is copied from Framer Motion docs into every grid | Render the grid at once |
| Hero headline split into words or letters that animate in | SplitText / per-word spans; a demo effect, not a reading aid | Plain text node. Screen readers also stop reading split letters as one word |
| Hero image zooms from 1.1 to 1 on load | "Ken Burns" hero, stock-template look | Static image |
| Logo animates in, then nav animates in, then hero animates in | A 1–2 second sequenced intro before the page is usable | Everything at first paint |
| Entrance delay on the primary button (`delay: 0.8`) | The one element the user needs arrives last | No delay on any interactive element, ever |
| List rows animate in every time data refetches | Re-running entrance on refresh makes a table flicker | Animate only rows that are new since last render, if at all (background tint that fades over 1–2 s) |
| Modal content staggers its fields in | Delays form input by up to a second | Modal content present when the modal is present. See part 21 |
| Mount animation on route change for every page | Each navigation feels slower than a plain link | No route-level entrance. See 25.9 |
| Animate-in on dashboard KPI tiles | Numbers users need to read now arrive late | Tiles render with values. See part 22 |

```html
<!-- Banned -->
<section class="opacity-0 translate-y-8 transition duration-700" data-aos="fade-up" data-aos-delay="200">

<!-- Use -->
<section class="features">
```

## 25.3 Scroll-triggered reveals and scroll effects

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Scroll-triggered animations everywhere (every section fades or slides in when scrolled into view) | AOS / IntersectionObserver reveal is the default "modern" add-on | Content renders immediately. No reveal on scroll |
| AOS library included (`aos.css`, `AOS.init()`) | Strong AI tell; ships 14 KB to hide content until scroll | Remove the library and all `data-aos` attributes |
| `whileInView` on every Framer Motion element | Copy-paste from examples | Remove. Keep `motion.*` only on elements with a real state change |
| GSAP ScrollTrigger pinning a section while text swaps | "Apple product page" imitation on a clinic or barangay site | Normal document flow. Put the content in a list or steps |
| Horizontal-scroll section driven by vertical scroll | Hijacks the scroll the user expects; breaks trackpads and screen readers | Normal vertical section, or a real horizontally scrollable list with visible overflow |
| Scroll-jacking (custom scroll speed, snapping whole screens) | Fights the browser; nauseating on trackpads | Native scroll. No `scroll-snap-type: y mandatory` on the page body |
| Progress bar at the top of an article that fills on scroll | Blog template feature nobody asked for | Remove. The scrollbar already shows position |
| Elements rotate or scale as the page scrolls | Decoration tied to scroll position | Static |
| Number that counts up when it scrolls into view | Double tell: scroll trigger plus counter | Print the number. See 25.6 |
| Forced smooth scroll (`html { scroll-behavior: smooth }`) site-wide | Slows every anchor jump; ignores user preference | `scroll-behavior: auto`, or smooth only inside `@media (prefers-reduced-motion: no-preference)` for in-page anchor links |
| Smooth-scroll libraries (Lenis, Locomotive Scroll) | Replace native scroll with JS; input lag on low-end phones | Remove. Native scroll |
| "Scroll down" bouncing arrow at the bottom of the hero | Tells the user something they know; loops forever | Remove. Make the next section's top edge visible above the fold |
| Bounce on scroll | Decorative, no state change | Render in place |
| Back-to-top button that animates in after 300 px | Motion plus a control most pages do not need | Remove unless page is 5000 px+. If kept, no animation. See part 16 |

## 25.4 Hover and press effects

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Hover lift on every card (`translateY(-4px)` plus bigger shadow) | Template reflex; card jumps under the cursor | Background change: `background-color: var(--color-surface-alt)` |
| Scale on hover (`transform: scale(1.05)`) | Makes layout jitter; text blurs during scale | Opacity (0.9) or background change |
| Tailwind `hover:scale-105 transition-transform` on cards, buttons, images | The single most common AI Tailwind hover | `hover:bg-surface-alt` (a colour token mapped in the Tailwind theme), or no hover on non-interactive cards |
| Tailwind `hover:-translate-y-1 hover:shadow-xl` | Same lift, different syntax | Remove both. Keep a border or background change |
| Hover effect on non-clickable cards | Suggests an action that does not exist | No hover state unless the whole card is a link or button |
| Row lift on table hover (`.row:hover { transform: translateY(-4px) }`) | Rows overlap neighbours; data tables must stay still | `.row:hover { background-color: var(--color-surface-alt); }` |
| Image zoom inside card on hover (`group-hover:scale-110`) | Stock e-commerce template tell | Static image. Hover changes the card title underline or border |
| 3D tilt on hover (vanilla-tilt, `rotateX/rotateY` following cursor) | Toy effect; also see part 10 | Remove |
| Magnetic buttons that follow the cursor | Agency-portfolio gimmick | Normal button |
| Icon inside button slides right on hover (`group-hover:translate-x-1`) | Every AI "Learn more →" button | Static icon, or no icon |
| Underline that grows from left on every nav link | Fine once; tiresome on every link | Plain `text-decoration: underline` on hover, or one or two animated links max |
| Glow or shadow that grows on hover | Neon style | Border colour change using a token |
| Rotate icon on hover (settings cog spins) | Decorative | Static |
| Hover animations that also run on touch devices | Tap triggers a sticky hover state on mobile | Wrap in `@media (hover: hover) and (pointer: fine)`; use `:active` for touch feedback |
| Press effect `active:scale-95` on every button | Copied from shadcn/UI demos | Optional on primary button only, 100 ms; or `:active` background shade |
| Hover transition longer than 200 ms | Feels laggy on repeated use | 100–150 ms for colour and background |

```css
/* Banned */
.card { transition: all 0.3s ease; }
.card:hover { transform: translateY(-4px) scale(1.02); box-shadow: 0 20px 40px rgba(0,0,0,0.2); }

/* Use */
.card-link { transition: background-color 120ms ease-out; }
@media (hover: hover) and (pointer: fine) {
  .card-link:hover { background-color: var(--color-surface-alt); }
}
.card-link:active { background-color: var(--color-surface-pressed); }
```

## 25.5 Parallax and background motion

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Parallax scrolling (background moves slower than content) | Nausea-inducing, costs frames, 2014 template look | No parallax |
| `background-attachment: fixed` hero | Breaks on iOS Safari; jank on Android | Normal background, or an `<img>` in flow |
| Mouse-move parallax on hero layers | Decoration following the cursor | Static layers |
| Animated gradient background (`background-size: 400% 400%; animation: gradient-shift 15s ease infinite`) | The signature AI hero; burns GPU on low-end phones | Flat background token. See part 11 for the CSS |
| Floating blobs that drift (`animate-blob`, keyframes moving blurred circles) | Tailwind UI and AI landing default | Remove blobs and their keyframes. See part 10 |
| Aurora / mesh gradient that shifts colour | Same, newer name | Static background token |
| Particle backgrounds (particles.js, tsParticles) | Heavy library, zero information | Remove |
| Floating 3D objects rotating in hero (Spline, three.js) | Heavy scene for decoration | Real screenshot or nothing |
| Stars twinkling, snow falling, sparkles following cursor | Decoration on a tool | Remove |
| Animated login background | Distracts on the one screen with a single task | Static solid background. See part 23 |
| Background video looping behind the hero | Data cost for PH mobile users; motion behind text | Static image or none. See part 26 |
| Rotating border beam around a card (`conic-gradient` animation) | MagicUI / Aceternity copy-paste | Static 1px border |
| Shimmer sweep across buttons | "Shimmer button" component | Solid button, no animation |

## 25.6 Counters, typing and number effects

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Counter animation (0 to 10,000+ on load or on scroll) | Stats counting up is an AI landing staple; delays the fact | Show the final number |
| Counter on a dashboard KPI | The user needs the number, not a show | Render the value. Update in place when data changes |
| Counter on peso amounts (₱0 to ₱1,250,000) | Money should never look in motion; it reads as fake | Static `₱1,250,000.00` with tabular numerals |
| Odometer / slot-machine digit rolls | Gimmick | Plain text update |
| Typing animation on hero headline | Delays the one sentence that matters; screen readers get partial text | Render the text |
| Rotating words in headline ("Build for [teams / schools / LGUs]") | Typed.js cliché | One headline stating one thing |
| Blinking cursor after hero text | Terminal cosplay | Remove |
| Text scramble / decode effect | Hacker aesthetic on a normal site | Plain text |
| Chat-style "AI is typing" dots on non-chat content | Fake liveness | Render the content |
| Streaming text for static responses | Simulates an LLM when nothing is generating | Render complete text |
| Progress rings that animate to a percentage on load | Delays reading the value | Static ring or plain "72%" |

## 25.7 Celebration, attention and looping effects

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Confetti on sign-up, form submit, payment, task done | Generator default for "success"; childish on government and business tools | Delete. Show "Saved." or "Payment received." |
| Confetti on a POS sale | Cashier sees it 300 times a day | No effect. Receipt view or "Sale complete. Change: ₱50.00" |
| Fireworks, balloons, party-popper Lottie | Same as confetti | Remove |
| Infinite pulse on badges (`animate-pulse` on "New", status dots, notification count) | Constant motion in peripheral vision; implies urgency that is not there | Static badge |
| `animate-ping` ring on a status dot | Tailwind docs demo pasted into production | Static dot with a text label |
| `animate-bounce` on an arrow, icon or CTA | Attention-grabbing loop | Static |
| Pulsing CTA button | Begging for clicks | Static button; position and label do the work |
| Wiggle / shake to draw attention to an unused feature | Nagging | Remove. Shake only on a failed PIN/OTP entry, 300 ms, once |
| Blinking "LIVE" or "HOT" label | Loops forever; often not actually live | Static label, and only if truly live. See part 04 |
| Marquee logo row scrolling infinitely | Template social proof; motion with no content | Static row of real logos, or none. See part 10 |
| Marquee news ticker on a barangay or school homepage | Hard to read, cannot be paused, fails WCAG 2.2.2 | Static list of the latest 3–5 announcements with dates |
| Scrolling testimonial carousel on autoplay | Moves while the user reads | Static list. If a carousel is required, no autoplay |
| Auto-advancing hero slider (Swiper, Slick) | LGU/school site staple; users never see slide 2 | One static hero, or a list of announcements |
| Animated emoji (waving hand) next to greeting | Double tell: greeting plus motion | No greeting. See part 22 |
| Spinning logo | Decoration | Static logo |
| Glow that "breathes" on a card or button | Neon look plus loop | Static |

Any content that moves automatically for more than 5 seconds must have a visible pause control (WCAG 2.2.2). The simpler fix is to not auto-move it.

## 25.8 Loading motion

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Spinner shown for loads under 200 ms | Flash of spinner is worse than nothing | Delay the spinner: show only if the load passes 300 ms |
| Skeleton shimmer on fast content | Shimmer on data that arrives in 100 ms reads as fake loading | Skeleton only if load passes 500 ms. See part 21 |
| Skeleton on a 200 ms dashboard load | Same | Render when ready; keep previous data visible while refetching |
| Full-page loader with logo animation before the site shows | Hides content that is already there; splash screens on websites | Remove. Server-render or show layout immediately |
| Progress bar for a single-step action | Implies stages that do not exist | Spinner in the button, or nothing |
| Fake progress bar that fills on a timer | Lies about progress | Indeterminate indicator, or real byte/step progress |
| Loading text that cycles cute messages ("Brewing coffee…", "Reticulating splines…") | Joke loader | "Loading…" or a silent spinner. See part 04 for text |
| Three bouncing dots on every async action | Chat-typing cliché | Spinner inside the triggering button, button disabled while pending |
| Lottie loading animation (bouncing cube, astronaut) | Heavy JSON file for a spinner | CSS spinner, 16–20 px, `currentColor` |
| Spinner in the middle of an empty page with no text | User cannot tell what is loading | Spinner next to the thing loading, or "Loading records…" |
| Multiple spinners on one screen at once | Each widget loads separately with its own spinner | One loading state per region; batch fetches where possible |
| Optimistic UI that animates a row in, then animates it out on failure | Bouncing rows | Show the row immediately with a pending style; on failure mark it with an inline error and a retry link |
| Spinner that keeps spinning forever on error | No timeout, no error state | Timeout at 15–30 s, then an error with a retry button |
| Slow 3G in the Philippines not considered | Heavy loaders on a 1 Mbps connection | Test with Chrome "Slow 3G" throttling; content first, script last |

```css
/* Use: spinner that only appears after 300 ms */
.spinner {
  width: 1rem; height: 1rem;
  border: 2px solid currentColor; border-right-color: transparent;
  border-radius: 9999px;
  animation: spin 700ms linear infinite, appear 0ms 300ms both;
  opacity: 0;
}
@keyframes spin { to { transform: rotate(360deg); } }
@keyframes appear { to { opacity: 1; } }
@media (prefers-reduced-motion: reduce) {
  .spinner { animation: appear 0ms 300ms both; border-right-color: currentColor; opacity: 0.6; }
}
```

With reduced motion on, a static ring alone does not say "loading". Pair it with visible or screen-reader text ("Loading records…"). A slow spin (1.5 s per turn) is also acceptable, because a loading indicator counts as essential motion.

## 25.9 Page, route and component transitions

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Page transitions (fade-out / fade-in between routes) | Each click costs 300–600 ms; `AnimatePresence` around the router | Instant route change |
| Slide transition between pages as in a native app | Web is not a native stack; back button feels wrong | Instant route change |
| View Transitions API morphing every element between pages | Newest demo effect applied to everything | Use only for one element that moves between list and detail (e.g. thumbnail to image), 200 ms, reduced-motion guarded |
| Modal scale + fade at 300 ms or longer | Slow open on every edit | Instant, or 150 ms fade. See part 21 |
| Modal springs in with overshoot (`type: "spring", bounce: 0.4`) | Bouncy toy feel | No spring on modals. Fade 150 ms or none |
| Drawer slides in at 500 ms | Blocks input for half a second | 200 ms ease-out, from the edge it lives on |
| Dropdown menu animates height from 0 | Height animation causes layout reflow and jank | Opacity 0 to 1 in 100 ms, or instant |
| Animated menu transitions in nav | Slows every navigation | Instant, 150 ms fade max. See part 16 |
| Accordion animates `height` with JS measuring | Janky on long content | Native `<details>` with no animation, or `grid-template-rows: 0fr → 1fr` at 150–200 ms |
| Tab content cross-fades on switch | Delays reading the new tab | Instant swap. Optional 2px indicator slide 150 ms |
| Toasts fly in from off-screen with bounce | Attention theft | 150 ms fade or slide of 8 px max. See part 21 |
| Layout animations (`layout` prop) on every list | Items glide around on each sort or filter | No layout animation on data lists. Optional on drag-and-drop reorder only |
| Animated route progress bar (NProgress) plus page fade plus skeleton | Three loading motions for one navigation | Pick one: a thin top bar only if navigation passes 300 ms |
| Tooltip fades in after 500 ms delay with 300 ms fade | Tooltips feel broken | 300–500 ms open delay is fine; fade 100 ms; instant close |
| Sidebar collapse animates width at 400 ms and reflows the whole page | Every table re-lays out during the animation | Instant, or 150 ms; avoid animating `width` of layout containers |

## 25.10 Durations and easings

| Change | Duration | Easing |
|---|---|---|
| Colour, background, border on hover/focus | 100–150 ms | `ease-out` |
| Button press (`:active`) | 0–100 ms | `ease-out` |
| Tooltip / popover / dropdown open | 100–150 ms | `ease-out` |
| Close / dismiss of any overlay | 100 ms, or instant | `ease-in` |
| Modal / dialog open | 0–150 ms (fade only) | `ease-out` |
| Drawer / bottom sheet open | 200–250 ms | `cubic-bezier(0.2, 0, 0, 1)` or `ease-out` |
| Accordion expand | 150–200 ms | `ease-out` |
| Toast enter | 150 ms | `ease-out` |
| Highlight of a new or changed row | 1–2 s fade of background | `linear` |
| Anything decorative | 0 ms | none |

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `transition: all 0.3s ease` on everything | Default AI CSS; animates layout properties and causes jank | Name the property: `transition: background-color 120ms ease-out`. See part 11 |
| `duration-300`, `duration-500`, `duration-700` scattered in Tailwind | Random durations per component | 2–3 duration tokens in DESIGN.md (`--duration-fast: 120ms`, `--duration-base: 200ms`) |
| `ease-in-out` on everything | Default easing; entering elements feel sluggish | `ease-out` for entering and hover, `ease-in` for exiting |
| Spring physics with bounce on UI controls | Playful overshoot on a business tool | No bounce. Critically damped if a spring is required (`bounce: 0`) |
| `cubic-bezier(0.68, -0.55, 0.265, 1.55)` (back-overshoot) | Copied from easings.net for "juice" | `ease-out` |
| Durations over 400 ms on any UI control | Users wait on every interaction | Cap UI transitions at 250 ms |
| Exit animation equal to or longer than entry | Closing feels slow | Exit shorter than entry, or instant |
| Animating `width`, `height`, `top`, `left`, `margin` | Forces layout every frame; stutters on low-end Android | Animate `opacity` and `transform` only |
| `will-change: transform` on dozens of elements | Pasted as a "performance fix"; wastes GPU memory | Remove. Add only to one element during an active animation |
| Motion values hard-coded in each component | No shared system; values drift | Motion tokens in DESIGN.md, referenced as `var(--duration-fast)` and `var(--ease-out)` |

```css
/* Use: motion tokens, defined once */
:root {
  --duration-fast: 120ms;
  --duration-base: 200ms;
  --ease-out: cubic-bezier(0.2, 0, 0, 1);
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
}
```

## 25.11 Reduced motion

`prefers-reduced-motion: reduce` must remove all non-essential motion. Essential motion is limited to: a loading indicator, a drag-and-drop item following the pointer, and a video the user started.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| No `prefers-reduced-motion` handling at all | Generated CSS ignores the setting | Add a global reduced-motion block (below) to the base stylesheet |
| Reduced-motion block that sets `animation-duration: 0.01ms` but JS animations still run | CSS-only fix; Framer Motion and GSAP ignore it | Also check in JS: `window.matchMedia('(prefers-reduced-motion: reduce)').matches`; in Framer Motion use `<MotionConfig reducedMotion="user">` or `useReducedMotion()` |
| Reduced-motion users get the same parallax and autoplay carousel | Vestibular disorders triggered | Parallax and autoplay off by default for everyone; if kept, off under reduced motion |
| Reduced motion replaces slide with a slower fade | Still motion | Instant state change under reduced motion |
| Motion that cannot be paused (marquee, carousel, looping video) | Fails WCAG 2.2.2 | Remove autoplay, or add a visible pause button that works by keyboard |
| Flashing effects more than 3 times per second | Seizure risk, WCAG 2.3.1 | Never flash. No strobe on errors or alerts |
| Smooth scroll kept under reduced motion | Scroll animation is motion | `scroll-behavior: auto` under reduced motion |
| Lottie autoplay ignoring the setting | Lottie player defaults to autoplay and loop | `autoplay={!reduced}` and `loop={false}`; show first frame when reduced |

```css
/* Use: base reduced-motion block */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

This is the one accepted `!important` use: it must beat component-level motion. See part 27 for the accessibility rule set.

## 25.12 Motion libraries

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Framer Motion (motion) installed for one fade | ~30 KB+ for something CSS does | CSS transition. Install the library only for gestures, drag, or shared layout that CSS cannot do |
| Every element is `motion.div` | Wrapping for the sake of it | Plain `div`. Keep `motion.*` on the 1–3 elements that truly animate |
| `initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}` pasted into every component | Framer Motion boilerplate; the most recognisable AI React tell | Delete the props |
| `AnimatePresence` wrapped around the whole app or router | Page transitions nobody asked for | Remove. Use it only around an element that must animate its removal |
| GSAP + ScrollTrigger on a 5-section brochure site | Heavy toolset for decoration | Remove GSAP. No scroll animation |
| AOS (Animate On Scroll) | Exists to hide content until scroll | Remove the package, CSS and all `data-aos*` attributes |
| animate.css classes (`animate__animated animate__fadeInUp`) | Bootstrap-era template tell | Remove |
| WOW.js, ScrollReveal, Sal.js | Same as AOS | Remove |
| Two or three motion libraries in one project | Each component copied from a different demo | Zero or one. CSS first |
| `tailwindcss-animate` plugin plus custom keyframes for blob, shimmer, float, glow | Plugin kept for shadcn, then abused | Keep the plugin for Radix open/close states; delete custom decorative keyframes |
| Tailwind `animate-spin` on non-loading icons (refresh icon spinning idle) | Motion that signals loading when nothing loads | Spin only while a request is pending |
| Tailwind `animate-pulse` used as a "live" effect | Pulse means "loading skeleton" in Tailwind | Static element. `animate-pulse` only on skeleton blocks, only after 500 ms |
| Bootstrap `.fade` + `.carousel-fade` + `data-bs-ride="carousel"` | Auto-cycling carousel on school/LGU homepages | Remove `data-bs-ride`; static content. See 25.7 |
| jQuery `.fadeIn()`, `.slideDown()`, `.animate()` sprinkled in legacy PHP templates | Old template motion kept during rebuild | CSS class toggle with a short transition, or instant |
| Motion library loaded from CDN with `@latest` | Unpinned, render-blocking | Remove, or pin a version and load deferred. See part 34 |

```tsx
// Banned
<motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.6, delay: i * 0.1 }} viewport={{ once: true }}>
  <FeatureCard {...f} />
</motion.div>

// Use
<FeatureCard {...f} />
```

## 25.13 Lottie, GIFs and animated illustrations

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Lottie animation in the hero (floating phone, rocket, people at laptop) | LottieFiles free-library look; 100 KB–1 MB of JSON | Real screenshot, or no visual |
| Lottie for empty states (astronaut, empty box bouncing) | Decoration on a state that needs one line of text | "No records." plus an action. See part 04 |
| Lottie for success check / error cross | A 40 KB file for a tick | Static SVG icon, or the text alone |
| Lottie on 404 page (lost astronaut, UFO) | Joke 404 cliché | "Page not found." plus links. See part 04 |
| Animated GIF as a feature illustration | Heavy, unpausable, no reduced-motion support | Static screenshot; or `<video muted playsinline controls>` with a poster, no autoplay |
| Animated SVG illustrations (SMIL, CSS keyframes inside the SVG) | Decoration that loops forever | Static SVG |
| Animated icons (Lordicon, animated Lucide) on every nav item | Icons that move on hover or load | Static icons. See part 26 |
| Autoplaying product demo video on landing | Data cost; motion while reading | Poster image with a play button; `preload="none"` |

## 25.14 Motion that is allowed

Motion is fine when it does one of these jobs. Keep the durations in 25.10.

| Job | Example | Limit |
|---|---|---|
| Show where something came from or went | Drawer slides from the right edge; toast slides 8 px up | 150–250 ms, transform + opacity only |
| Confirm a press | Button background darkens on `:active` | 0–100 ms |
| Show progress of real work | Spinner in button, upload progress bar with real bytes | Only while pending; delay spinner 300 ms |
| Point to a change the user did not cause | New row background fades from highlight token to normal over 1–2 s | Once, no loop |
| Show an error on a short code field | Single 300 ms horizontal shake on wrong PIN/OTP | Once, plus text error; none under reduced motion |
| Keep context during reorder | Dragged item follows pointer; others shift | Drag-and-drop only |
| Reveal disclosure content | Accordion or `<details>` open | 150–200 ms, or instant |

## 25.15 Philippine context

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Heavy motion on sites mostly viewed on budget Android phones over mobile data | Jank and battery drain on the actual audience | Test on a mid-range Android with 4x CPU throttle; remove anything that drops frames |
| Auto-sliding banner of barangay officials' photos | Common LGU template; faces rotate before anyone reads names | Static list of officials with names and positions |
| Scrolling marquee "WELCOME TO THE OFFICIAL WEBSITE OF BARANGAY …" | Old-school ticker; unreadable, cannot pause | Static page heading. See part 09 |
| Animated countdown to election day or enrolment deadline with ticking seconds | Seconds ticking create false urgency and constant motion | Static "Election day: 12 May 2025" or "Enrolment closes 15 June". Days-left count, updated daily, no seconds |
| Confetti or fireworks on a GCash/Maya payment confirmation | Money screens must look calm and exact | "Payment received. Ref. no. 1234 5678 9012." |
| Blinking "BAGO!" / "NEW!" label on announcements | Loops forever | Static "New" badge with a date. See part 04 |
| Animated Philippine flag waving GIF in the header | Decoration, heavy GIF | Static seal or logo, only if official. See part 26 |

## 25.16 Check
- [ ] No content starts hidden (`opacity: 0`, off-screen transform) waiting for JS to reveal it.
- [ ] No entrance animation on page load, section, card, heading or button.
- [ ] No stagger on grids or lists.
- [ ] No scroll-triggered reveal; AOS, WOW.js, ScrollReveal, animate.css removed.
- [ ] No parallax, no `background-attachment: fixed`, no scroll-jacking or smooth-scroll library.
- [ ] `scroll-behavior: smooth` absent, or guarded by `prefers-reduced-motion: no-preference`.
- [ ] No hover lift or scale on cards, rows or images; hover changes background or border only.
- [ ] Hover effects wrapped in `@media (hover: hover)`; touch uses `:active`.
- [ ] Non-clickable elements have no hover effect.
- [ ] No counter, odometer, typing, rotating-word or text-scramble effect.
- [ ] No confetti, fireworks, balloons or celebration Lottie.
- [ ] No infinite `animate-pulse`, `animate-ping` or `animate-bounce` outside skeletons and spinners.
- [ ] No marquee, autoplay carousel, auto-advancing slider or ticker; if unavoidable, a keyboard-operable pause exists.
- [ ] Nothing flashes more than 3 times per second.
- [ ] No animated gradient, drifting blobs, particles, aurora, border beam or shimmer.
- [ ] No background video behind text.
- [ ] Spinner appears only after 300 ms; skeleton only after 500 ms.
- [ ] No fake timed progress bar; progress bars show real progress.
- [ ] Loading indicators have a timeout and an error state.
- [ ] No full-page splash loader.
- [ ] No page or route transitions; route changes are instant.
- [ ] Modal opens instantly or with a 150 ms fade; no spring or overshoot.
- [ ] Drawer 200–250 ms; dropdown and tooltip 100–150 ms; close faster than open.
- [ ] No `transition: all`; each transition names its property.
- [ ] Only `opacity` and `transform` are animated; no `width`, `height`, `top`, `left`, `margin`.
- [ ] No UI transition longer than 250 ms.
- [ ] Durations and easings come from motion tokens in DESIGN.md.
- [ ] Global `prefers-reduced-motion: reduce` block present in the base CSS.
- [ ] JS-driven motion checks reduced motion (`useReducedMotion`, `MotionConfig reducedMotion="user"`, `matchMedia`).
- [ ] At most one motion library; none if CSS covers the need.
- [ ] No `motion.div` with `initial`/`whileInView` boilerplate on static content.
- [ ] No Lottie or GIF for heroes, empty states, 404s or success ticks.
- [ ] No animated icons in navigation.
- [ ] Dashboard KPIs, peso amounts and table data render as static values.
- [ ] POS, admin and form screens have zero decorative motion.
- [ ] LGU/school homepages have no auto-sliding banner, marquee ticker or waving-flag GIF.
- [ ] Page tested with Slow 3G and 4x CPU throttle; no dropped frames from motion.
