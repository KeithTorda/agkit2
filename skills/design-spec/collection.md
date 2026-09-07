# Design reference collection — organised by who you are building for

**How to use.** Pick 1-2 entries from the section that matches your **audience and domain**, and name
what you borrow from each (grid, type treatment, nav, density, colour logic). The section you reach
for is decided by the user of the thing you are building, never by the design you have seen most.
Building a barangay portal? Section 1. A sari-sari store's POS? Section 3. A clinic booking flow?
Section 5. Section 12 — developer products — is last on purpose: reach for it only when you are
building a developer product.

**These are pointers to durable patterns, not specifications.** Products redesign. Open the one you
pick and look at it before you borrow from it; if you cannot, borrow the pattern named here and say
you did not verify. Entries marked `(slug)` have a published DESIGN.md you can fetch — see the
appendix for the URL shape.

---

## 1. Public service, government and civic

The hardest audience: people who did not choose to be here, often stressed, on a bad connection, on
an old phone. Decoration reads as untrustworthy. Plain language beats brand voice every time.

- **GOV.UK** — UK government services. The reference standard: black on white, one column, plain language, one task per page, no decoration.
- **U.S. Web Design System (USWDS)** — US federal services. Accessible component set: high contrast, large targets, error text that says how to recover.
- **Singpass / GovTech Singapore** — national digital identity. Task-first flows, minimal chrome, no marketing voice inside the service.
- **Service NSW** — Australian state services. A card per service on the home screen; plain service titles instead of department names.
- **gov.br** — Brazilian federal portal. A large service search is the primary entry, not a navigation menu.
- **UMANG / DigiLocker (India)** — national service apps at scale. Icon-and-label grid built for low-literacy users; prominent language switching.
- **eesti.ee (Estonia)** — digital-state portal. Dense service directory with "who accessed your data" surfaced as a first-class view.
- **Election and agency notice sites** — the pattern that matters: date-stamped announcement lists, one authoritative "where do I go" lookup, and results tables that stay readable when printed.

## 2. Money: wallets, banking and payments

Trust is the design problem. Users check a balance, then act. Show the number they came for first,
and never let motion or promotion sit between them and it.

- **GCash** — dominant PH wallet. Dense action grid on the home screen; every icon carries a word under it.
- **Maya** — PH wallet and bank. Card-forward hierarchy on a dark surface; balance anchors the screen, promotions sit below it.
- **BPI / BDO online banking** — PH retail banks. Conservative trust cues, form-dense, deliberately slow motion, no decoration.
- **Wise** — cross-border transfers. The fee and the rate appear before you commit; the number the user cares about is the headline.
- **Nubank** — Latin American bank. One brand colour, large type, radical simplicity in the account view.
- **Monzo** — UK bank. Plain-English transaction lines with merchant logos and a category colour per row.
- **Cash App** — consumer payments. A single giant numeric input is the entire screen.
- **Revolut** `(revolut)` — digital banking. Gradient cards as identity; accounts separated by colour.
- **Alipay / WeChat Pay** — Chinese super-apps. Service-tile density Western apps avoid, and the mini-app grid SEA super-apps inherited.

## 3. Retail, POS and merchant tools

Used standing up, one-handed, under time pressure, often in bad light, by staff trained in ten
minutes. Touch targets and contrast beat elegance. Destructive actions sit far from frequent ones.

- **Square POS** — small-merchant POS. Large touch tiles, item grid over lists, one-thumb operation.
- **Toast** — restaurant POS. High-contrast tiles readable in bad light; voids and refunds physically separated from the till flow.
- **Shopify admin (Polaris)** — merchant back office. Dense data tables inside a calm neutral shell; the data is the product.
- **Lightspeed Retail** — inventory-first retail. Search is the primary navigation, not the menu.
- **Loyverse** — small-shop POS widely used across SEA. Free-tier discipline: fewer than ten primary actions in the whole app.
- **Grab Merchant / foodpanda partner** — SEA seller apps. The order queue *is* the home screen; state colour carries the whole interface.
- **Zettle** — micro-merchant payments. Number pad first, catalogue second.
- **Odoo / Zoho (SMB modules)** — small-business ERP. A module grid as the entry point, and forms that deliberately mirror the paper process they replace.

## 4. Marketplace and commerce

Density that would read as clutter elsewhere reads as choice here. Price, rating and delivery belong
on every card. Regional expectations differ sharply — do not apply a Western minimal grid to a SEA
marketplace.

- **Shopee** — SEA marketplace. Orange saturation, urgency badges, tight cards; banner density that is normal to its users.
- **Lazada** — SEA marketplace. Category-grid entry point and stacked promotional rails.
- **Tokopedia** — Indonesian marketplace. Dense category tiles under a single strong brand colour.
- **Amazon** — global retail. Information density over beauty; every card carries price, rating and delivery date.
- **Mercado Libre** — LatAm marketplace. Trust badges sit next to the price, not in a footer.
- **Etsy** — handmade marketplace. Photography-led grid with warm neutral chrome that stays out of the way.
- **IKEA** — furniture retail. Room photography is the navigation; the product grid is subordinate to it.
- **Shopify storefronts (Dawn)** — the default modern storefront: generous product photography, minimal chrome, one accent.

## 5. Health, clinics and care

Clinical caution over delight. People arrive worried. Never make a result or an appointment time
compete with anything, and never signal state by colour alone.

- **Zocdoc** — appointment booking. The availability grid is the primary object; time slots are the product.
- **Practo** — India and SEA clinic booking. One card per doctor carrying credentials, fee and next slot together.
- **MyChart (Epic)** — patient portal. Results and appointments as plain lists; no decoration near clinical data.
- **Teladoc** — telehealth. A pre-visit checklist that exists to stop the call from failing.
- **Ada** — symptom triage. One question per screen, no progress anxiety, explicit "this is not a diagnosis".
- **Apple Health** — personal health. Trends over instantaneous numbers; the ring and graph are the identity.
- **Telehealth in the Philippines** — the pattern: Filipino-English mixed copy, and HMO or PhilHealth fields surfaced early rather than at checkout.

## 6. Education and learning

Progress is the emotional core. Show where the learner is, what is next, and nothing else.

- **Duolingo** — language learning. Streak and progress carry the product; one lesson per screen.
- **Khan Academy** — free courseware. Calm neutral reading surface with a progress bar per unit.
- **Google Classroom** — school workflow. A stream plus an assignment list; built for teachers, not for looks.
- **Quizlet** — study tool. The card flip is the entire interaction model.
- **Coursera** — higher education. The institution's logo on the course card is the trust signal.
- **School information portals** — the pattern students actually use: enrolment status, grades, and outstanding balance are the three things they came for; everything else is secondary.

## 7. Logistics, delivery and field work

A map, a status, and one action. Used outdoors, in motion, at arm's length. Glanceability beats
information richness.

- **Grab** — SEA super-app. Map-first with exactly one primary action per screen.
- **Gojek** — Indonesian super-app. Service-tile grid where every icon carries a label.
- **Lalamove** — SEA delivery. The booking form *is* the home screen, not a dashboard.
- **Parcel tracking (J&T, LBC, Ninja Van)** — the timeline is the entire page and the status word is larger than everything around it.
- **Driver and rider apps** — accept and decline targets sized to be hit without looking; nothing else competes on the screen.
- **Circuit / Onfleet** — route tools. Map and list side by side, both authoritative, neither subordinate.

## 8. Booking, travel and hospitality

Photography sells, but the calendar and the price do the work. Scarcity language is a design element
in this domain — use it honestly.

- **Airbnb** `(airbnb)` — stays marketplace. Photography-driven cards, warm rounded UI, filters as a first-class surface.
- **Booking.com** — hotel booking. Dense but legible; urgency text sits inside the card hierarchy.
- **Agoda** — SEA travel. Price-first cards with aggressive discount labelling.
- **Traveloka** — SEA travel. Multiple product types bundled behind one search bar.
- **Klook** — SEA activities. Category tiles led by photography, with local-language switching.
- **Cal.com** `(cal)` / **Calendly** — scheduling. The calendar is the whole interface; nothing competes with it.
- **OpenTable** — restaurant reservations. Time-slot chips are the primary control.

## 9. Work tools: dashboards, admin and internal

Daily users. Density is a feature; they will learn the layout. Colour is reserved for state, never
for decoration. This is the section for most app-UI work.

- **Notion** `(notion)` — workspace. Warm minimalism, serif headings, blocks instead of chrome.
- **Airtable** `(airtable)` — structured data. Colour-coded fields; the grid itself is the navigation.
- **Metabase** — analytics for non-analysts. The question comes first, the chart second.
- **Grafana / Datadog** — observability. Small multiples; colour reserved strictly for state.
- **Retool** — internal tools. Function over polish: dense forms sitting beside dense tables.
- **Salesforce Lightning** — enterprise CRM. Record page with tabs; density expected by people who live in it.
- **Intercom** `(intercom)` — customer messaging. Conversational UI patterns under a friendly, low-contrast shell.

## 10. Media, publishing and editorial

Typography is the design. Hierarchy carried from print still outperforms invented layouts.

- **The Guardian** — news. Column rhythm and headline hierarchy taken directly from print.
- **The New York Times** — news. Multi-column density under strict typographic hierarchy.
- **WIRED** `(wired)` — tech magazine. Broadsheet density, custom serif, ink-blue links.
- **The Verge** `(theverge)` — tech editorial. Acid accents over an opinionated grid.
- **Medium** — reading. The type scale and the measure are the entire design.
- **Substack** — newsletters. Author identity sits above publication chrome.
- **Philippine news portals** — the pattern: dense homepages with section rails, and election coverage that runs as a live blog rather than a static page.

## 11. Consumer social and entertainment

Content is the interface. Chrome disappears. Motion is expected here in a way it is not anywhere else
in this list.

- **Spotify** `(spotify)` — music. Vibrant accent on dark; album art drives the grid.
- **Netflix** — video. Row-based browsing where artwork *is* the navigation.
- **TikTok** — short video. Full-bleed single item with UI floating over content.
- **Instagram** — photo social. The chrome recedes until only content remains.
- **YouTube** — video. A thumbnail grid with metadata density tuned over two decades.
- **Discord** — community chat. A three-pane shell that survives extreme message density.

## 12. Developer and technical products — only when building one

**This section is last on purpose.** It is the design most written about on the internet, which makes
it the reflex answer and the wrong one for a POS, a clinic, a school portal or a government service.
Its aesthetic — dark surfaces, monospace accents, ultra-minimal chrome, gradient-on-black heroes —
signals "for engineers". Use it when your users are engineers.

- **Linear** `(linear.app)` — issue tracking for engineers. Ultra-minimal and precise; keyboard-first.
- **Stripe** `(stripe)` — payments infrastructure. Documentation and dashboard share one design language.
- **Vercel** `(vercel)` — deployment platform. Black-and-white precision, Geist.
- **Supabase** `(supabase)` — backend platform. Dark emerald, code-first.
- **Sentry** `(sentry)` — error monitoring. Data-dense dark dashboard.
- **GitHub** — code hosting. A neutral shell that survives enormous density.
- **Raycast** `(raycast)` / **Warp** `(warp)` / **Cursor** `(cursor)` — developer tools. Dark chrome with command-palette entry.

---

## Fetchable DESIGN.md files

Entries marked `(slug)` have a published DESIGN.md. The full slug list, by category, and the URL shape are in [fetchable.md](./fetchable.md) — read it only when you are authoring a `DESIGN.md` and a browsing tool is available.
