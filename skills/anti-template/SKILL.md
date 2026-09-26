---
name: anti-template
description: Reference of defaults that make copy, UI and code look generated, with what to write instead - 35 parts by topic. Use when writing visible text, designing or reviewing a page, or checking a project for template tells; read only the parts the task needs.
version: 2.5.0
---

# Anti-template guidance

These are defaults that make work look generated. Question each one against the brief. `DESIGN.md` or an explicit client request overrides any of them: if the client asks for glass, a gradient hero, glow badges or bold motion, build it well and skip the matching warning.

Firm only:
- **Accessibility** (part 27): contrast, real controls, labels, focus, keyboard, reduced motion.
- **Hype-free system copy** (parts 01-04): no hype words, no fake-excited microcopy, buttons say what they do, errors say what to do next.

Everything else is a question to ask ("does this page need it, and does it fit this audience?"), not a ban. When you keep a flagged default on purpose, say why in one line.

Parts live in `KIT/skills/anti-template/parts/`. Do not read all 35. Pick by task, read 1-4 parts.

## Pick by task
| Task | Read |
|---|---|
| Any reply, plan, report or summary you write | 07 |
| Button, label, form text, toast, confirm, loading | 03, 17 |
| Empty state, error page, onboarding, status text, dates, pesos | 04 |
| Landing, marketing, pricing, about page copy | 05, 24, 10 |
| README, docs, changelog, commit, PR, code comments, logs | 06 |
| Email, SMS, social post, SEO title, meta, OG tags | 08 |
| Anything for a PH client, LGU, barangay, school, COMELEC, POS | 09 |
| New page or component (visual) | 10, 14, and the component part below |
| Writing or reviewing CSS / Tailwind / Bootstrap classes | 11, 29 |
| Colours, dark mode | 12, 34 |
| Fonts, type scale | 13 |
| Mobile, responsive | 15 |
| Header, nav, sidebar, tabs, footer, pagination | 16 |
| Forms and inputs | 17 |
| Buttons and actions | 18 |
| Tables, lists, cards, badges, stat tiles | 19 |
| Charts | 20 |
| Modals, drawers, toasts, tooltips, spinners, skeletons | 21 |
| Dashboard, admin panel, CRUD, POS, inventory | 22 |
| Sign in, register, reset, profile, settings, billing | 23 |
| A specific page type (blog, docs, checkout, 404, precinct finder) | 24 |
| Animation | 25 |
| Icons, images, logos, favicon | 26 |
| Accessibility | 27 |
| HTML markup | 28 |
| JS / TS | 30 |
| React / Next / Vue | 31 |
| API, backend, database | 32 |
| File, folder, variable names | 33 |
| Performance, SEO, theming | 34 |
| `/review`, pre-ship check, grep for tells | 35 |

## All parts
01 words · 02 phrases and sentences · 03 microcopy core · 04 microcopy states · 05 marketing copy · 06 docs and code text · 07 agent replies · 08 email, social, meta · 09 Filipino context · 10 visual tropes · 11 CSS patterns · 12 colour · 13 typography · 14 layout and spacing · 15 responsive and mobile · 16 navigation · 17 forms and inputs · 18 buttons and actions · 19 data display · 20 charts · 21 overlays and feedback · 22 dashboards and admin · 23 auth and account · 24 page types · 25 motion · 26 icons and images · 27 accessibility · 28 HTML structure · 29 CSS architecture · 30 JS / TS · 31 React frontend · 32 backend, API, DB · 33 naming and structure · 34 performance, SEO, theming · 35 master checklist and grep patterns

File names: `parts/NN-<topic>.md` (for example `parts/09-filipino-context.md`). List the folder if unsure.

## How to read a part
- Each table row is *AI pattern → why it reads as generated → use instead*. Read "use instead" as the default when nothing in the brief points elsewhere.
- Some parts say "banned" or "never" for visual or code patterns. Outside parts 01-04 and 27, read that as "do not reach for it by reflex". A pattern the brief or `DESIGN.md` asks for is a design decision, not a tell.
- Hex values in the parts are labelled examples of common defaults (mostly Tailwind and shadcn palettes). Real colours come from `DESIGN.md`.
- The tell is usually the combination, not the single element: indigo + glass + gradient text + three equal cards + "Unlock your potential" is a template; one glass nav on a photo-led consumer site is a choice.

## Keep in mind without reading a part
1. No hype words in system copy: seamless, powerful, robust, cutting-edge, unlock, elevate, empower, leverage, delve, journey, comprehensive, intuitive (01).
2. Buttons say the action: Save, Sign in, Export. "Get started" only when it is the literal next step (03).
3. Empty state = fact + next action. Error = what failed + what to do. No "Oops" (04).
4. No emoji and no exclamation marks in system UI text, unless the brand voice in `DESIGN.md` is deliberately playful (03).
5. Decoration is a choice: glow, gradient text, glass, blobs, hover scale and entrance animations are fine when the direction calls for them and wrong when they are there because nobody chose (10, 25).
6. Colours, fonts, radii from `DESIGN.md` tokens. One accent per view unless the direction says otherwise (12).
7. "Live" only for real push updates. Otherwise "Updated 2m ago" (04).
8. Your own reply: lead with the result, no "Great question", no claim of testing you did not run (07).
