---
part: 24
title: Page Types
covers: landing page, pricing, about, contact, blog list, article, docs page, changelog, careers, portfolio, product page, cart and checkout, search results, legal pages, coming soon and waitlist, link-in-bio, event page, government and barangay homepage, school homepage, election and precinct finder
---

# 24 — Page Types

Read when: building a whole page of a known type and you need its structure, required content and the template tells to avoid.

Guidance: DESIGN.md and the brief override this part.

Marketing wording (headlines, testimonials, stats, plan names) is in part 05. Visual tropes are in part 10. Error pages and empty states are in part 04. SEO text and meta tags are in part 08. Filipino-language and government wording is in part 09. This part covers what each page type must contain and how it is structured.

## 24.1 Rules for every page type

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Every page starts with a full-height hero | Template habit | Full hero on the landing page only, and only when there is a real image or product shot. Other pages start with an H1 and content |
| 100vh hero on a utility page or tool | Content pushed below the fold | Main content visible in the first 600px on a 390x844 phone |
| Same section order on every page (hero, features, testimonials, CTA) | One template for all content | Order sections by what the visitor on that page needs first |
| Hero + 3 feature cards + CTA as the whole page | Default AI landing layout | Build from the client's real content: services, schedule, prices, location, proof |
| Lorem ipsum or "Your headline here" left in sections | Unfinished template | Real copy, or remove the section. Mark missing content with a TODO the client sees in review, not in production |
| Sections included because templates have them (Testimonials, Team, FAQ) with invented content | Filler | Include a section only when the client supplied the content |
| Final "Ready to get started?" CTA band on every page | Template ending | End with the next step specific to the page (contact details, schedule, related articles) or nothing |
| Alternating full-bleed background colors per section | Marketing rhythm tell | One page background; separate sections with spacing and headings |
| Decorative wave/blob SVG dividers between sections | Template | Spacing or a 1px border |
| Scroll-reveal animation on every section | Content hidden until scroll | Render content immediately. See part 25 |
| Page `<title>` "Home" or identical titles site-wide | SEO and tab confusion | "Page name — Site name". See part 08 |
| No H1, or several H1s | Structure broken | One H1 per page that names the page |

## 24.2 Landing page

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Glowing "New" pill above the hero headline ("✨ Introducing v2.0 →") | Launch-template trope | Remove, or a plain text link to the real announcement |
| Headline "The all-in-one platform for X" / "X reimagined" | Hype. See part 05 | Say what it is and who it is for: "Point-of-sale for hardware stores in Luzon" |
| Two CTAs "Get Started" + "Learn More" in the hero | Default pair | One primary action that names what happens: "Book a site visit", "Request a quote", "Call 0917 123 4567"; optional secondary text link |
| Hero visual: floating 3D shapes, gradient orb, abstract illustration | No information | Real product screenshot, real photo of the business, or no image |
| Fake browser/macOS window around a screenshot with traffic-light dots | Template chrome | Plain screenshot with a 1px border, cropped to the useful part |
| Logo wall of well-known brands the client never worked with | Fabricated proof | Only real clients with permission; otherwise omit |
| "Trusted by 10,000+ teams" with no source | Invented stat | Real numbers the client can back up, or omit |
| Feature grid of 6–9 icon cards with one vague sentence each | Filler | 3–5 concrete features, each with a screenshot or a specific fact |
| Bento grid of mismatched feature tiles | 2024 template trend | Simple stacked sections or a plain list |
| Testimonials carousel with stock headshots and first names only | Looks invented | Real quotes with full name, role, organization and permission; static, not a carousel |
| Pricing teaser plus FAQ plus newsletter plus CTA band stacked at the end | Every section at once | Pick the one that helps the decision; link to pricing and contact |
| Stats row ("99.9% uptime", "24/7 support", "10x faster") | Invented numbers | Only measured, sourced numbers; otherwise omit |
| Landing page with no address, phone or business hours for a local business | Missing the facts visitors want | Address with map link, phone, hours, and service area near the top or in the footer |
| Sticky "Chat with us" bubble plus cookie banner plus promo bar | Clutter on a phone screen | One contact channel, placed in the page; cookie notice only if cookies need consent |

## 24.3 Pricing page

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Three plans with the middle one scaled up, glowing and tagged "Most popular" | Template decoy layout | Equal cards or a table; mark a plan as "Most chosen" only if it is true |
| Plan names Starter / Pro / Enterprise or Basic / Premium / Ultimate | Default names | Names that describe the buyer: "1 branch", "Up to 5 branches", "Custom" |
| Monthly/annual toggle with "Save 20% 🔥" | Hype badge | Show both prices plainly: "₱999/month or ₱9,990/year (2 months free)" |
| Prices in USD, or "$" symbol for PH clients | Wrong currency | ₱ with VAT basis stated: "VAT inclusive" or "plus 12% VAT" |
| Long feature lists with checkmarks, half of them identical across plans | Padding | Show only differences in the cards; full comparison table below |
| Comparison table with 40 rows of checkmarks and "Unlimited" everywhere | Unreadable | Group rows (Sales, Inventory, Reports); use real limits ("3 users"), not "Unlimited" unless true |
| "Contact us" for every plan with no price | Hides the key fact | Show prices; "Custom" only for truly custom work, with a starting range |
| Hidden fees revealed at checkout (setup, hardware, training) | Distrust | List one-time costs on the pricing page: setup, hardware, training, SMS credits |
| FAQ with invented questions ("Is it really that easy?") | Filler | Questions customers actually ask: payment methods, contract length, refunds, data export, BIR accreditation |
| No payment method info | PH buyers look for it | "Pay by GCash, Maya, bank transfer or card." |

## 24.4 About page

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "We believe in…", "We're passionate about…" mission paragraph | Feeling statements. See part 05 | Facts: when founded, where, who runs it, what it does, for whom |
| "Our Story" with a timeline of invented milestones | Fabricated history | Real dates the client supplied, or a short paragraph |
| Team grid with stock headshots and names like "Sarah Johnson, CEO" | Invented people | Real people with permission, real photos taken on site; or no team section |
| Values grid: Innovation, Integrity, Excellence with icons | Generic | Remove, or concrete practices: "We reply to quotes within 1 working day" |
| Mission / Vision / Values blocks on a small business site | Corporate template | Keep for schools and LGUs where Mission/Vision is an official requirement; use the official text verbatim |
| Big "Join our team" CTA on a 3-person company's About page | Template | Link to careers only if there are openings |
| No address, registration details or contact on About | Missing trust facts | Business address, DTI/SEC registration where relevant, contact link |

## 24.5 Contact page

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Contact form only, no phone or address | Many PH customers prefer calling or messaging | Phone (click-to-call), email, Facebook page or Messenger link if used, address, hours, then the form |
| Form with Subject dropdown, Budget range, "How did you hear about us" | Over-collecting | Name, contact number or email, message. Add fields only when the client routes by them |
| "Get in touch — we'd love to hear from you! 💌" heading | Chatty | "Contact" |
| Embedded Google Map iframe loading on page open | Heavy on mobile data | Static map image or address with "Open in Google Maps" link; load the iframe on click |
| Map with the pin in the wrong place or generic city center | Unverified | Exact pin from the client; add landmarks: "Across Poblacion Public Market" |
| Business hours missing holidays | Visitors arrive to closed doors | Regular hours plus "Closed on regular holidays" or a holiday note |
| After submit: full-page "Thank you!" with confetti | Celebration | Inline "Message sent. We reply within 1 working day." |
| No response time stated | Uncertainty | State a real response time the client commits to |
| Phone as "+1 (555) 123-4567" | Template placeholder | Real PH number in local format: "(02) 8123 4567" or "0917 123 4567" |

## 24.6 Blog list

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Card grid with a stock or AI image per post | Visual noise, slow | Text list: title, date, 1–2 line summary; images only when the post has a real one |
| "Featured post" giant hero card | Template | Newest post first in the list |
| Category pills in 6 colors | Rainbow | Plain text categories, one neutral style |
| Author avatars from placeholder services | Fake people | Real author name; avatar only if real |
| Reading time on every post ("3 min read") | Filler on short posts | Omit, or show only for long guides |
| Infinite scroll on a blog archive | No footer, hard to return to place | Pagination or a full archive list by year |
| Newsletter box between every 3 posts | Interrupts browsing | One signup at the end of the list, only if the client sends a newsletter |
| Blog with 3 posts from 2 years ago on a live site | Looks abandoned | Hide the blog link, or show dates honestly; do not invent posts |

## 24.7 Article page

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Full-width hero image with gradient overlay and title on top | Template; title contrast unreliable | Title, date and author first; image below at content width |
| Body text wider than 90 characters per line | Hard to read | 60–75ch measure. See part 13 |
| Sticky table of contents for a 600-word post | Unneeded chrome | TOC only for long guides with 5+ H2s |
| Floating share buttons column (Facebook, X, LinkedIn, Pinterest, WhatsApp) | Clutter | One "Copy link" and the one or two networks the audience uses (Facebook, Messenger for PH) |
| "Related posts" of 3 cards with images at the end | Template | 3 text links to related posts, if they exist |
| Drop cap, pull quotes and highlighted callouts in every post | Decoration | Plain paragraphs; callout only for real warnings |
| No updated date on time-sensitive content (fees, requirements) | Stale info looks current | "Updated 12 Sep 2026" near the title |
| Comment section with no moderation plan | Spam | Omit comments, or enable with moderation |

## 24.8 Docs page

Docs wording is in part 06.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Docs site with a marketing hero ("Build faster with our docs ✨") | Wrong page type | Docs home lists sections and the quick start |
| Three-column layout with empty right rail | Wasted space | Sidebar + content; right-rail TOC only on long pages |
| Code blocks without a copy button or language label | Hard to use | Copy button, language label, commands that run |
| Callout boxes (Note, Tip, Warning, Info) on every section | Noise | Callouts only for warnings that prevent data loss or errors |
| Search box that does nothing | Fake control | Working search, or none |
| "Was this page helpful? 👍👎" on every page with no one reading the results | Theater | Omit unless someone reviews the feedback |
| No version selector when versions differ | Wrong instructions | Version selector or a clear "Docs for v2" label |

## 24.9 Changelog page

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Timeline with dots, gradient line and emoji per entry | Decoration | Dated list: version, date, grouped changes (Added, Changed, Fixed, Removed) |
| Entries like "Improved performance and fixed bugs" | Says nothing | Name the change: "Receipts print 2x faster on Epson TM-T82" (if measured), "Fixed: SC discount not applied to bundled items" |
| Marketing images for every release | Heavy | Screenshot only when UI changed |
| Changelog written as launch posts ("We're thrilled to announce…") | Hype. See part 06 | Flat statements |
| No link from the app to the changelog | Users never see it | "What's new" link in the help menu |

## 24.10 Careers page

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "Join our rockstar team!" / "We're hiring ninjas" | Hype and clichés | "Careers" or "Job openings" |
| Perks grid with icons (free snacks, ping pong, unlimited PTO) | Invented perks | Real benefits the client offers: HMO, 13th month pay, SSS/PhilHealth/Pag-IBIG, schedule, work setup |
| No salary range | Candidates skip | Salary range in ₱ per month |
| Open roles list that is empty with "No openings right now, but check back soon! 🚀" | Chatty | "No openings right now." plus how to send an application anyway, if the client accepts them |
| Application form asking for 20 fields plus a cover letter | Friction | Name, contact, CV upload (PDF, max size stated), optional note |
| Job posts with no location or work setup | Missing key facts | Location (city), onsite/hybrid/remote, schedule, employment type |

## 24.11 Portfolio

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "Hi, I'm Alex 👋 — a passionate full-stack developer crafting digital experiences" | Template bio | "Juan Reyes. Web developer in Cebu. I build booking and inventory systems for small businesses." |
| Skills section with progress bars (React 90%, CSS 85%) | Meaningless numbers | List of tools with projects that used them |
| Tech logo wall (every framework icon) | Padding | Short list of the stack actually used |
| Projects shown as cards with gradient placeholders or mockups on floating phones | No real work visible | Real screenshots, the problem, what was built, the result, live link or case study |
| Typing animation cycling job titles | Trope | Static one-line description |
| Dark theme with neon accent and particle background | Default dev-portfolio look | Theme from DESIGN.md; plain background |
| "Download CV" as the main CTA with no contact details | Dead end | Email, phone or Facebook/LinkedIn contact visible |
| Testimonials from "happy clients" with no names | Invented | Real named quotes with permission, or none |

## 24.12 E-commerce product page

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Product title with hype adjectives ("Premium Ultra-Soft Luxury Towel") | Keyword stuffing | Plain name with the attributes that matter: "Bath towel, cotton, 70 x 140 cm" |
| Price without currency or with USD | Wrong locale | "₱349.00"; sale price with the original struck through and the saving stated |
| Fake urgency ("Only 2 left! 🔥", countdown timers that reset) | Dark pattern | Real stock counts only when low and true; no fake timers |
| Fake reviews (5.0 stars, "Amazing product!!!") | Fabricated | Real reviews only; show count and distribution; no stars when there are no reviews |
| Image gallery with zoom-on-hover only | Fails on touch | Tap to open full-size images; swipe on mobile |
| "Add to cart" hidden below a long description on mobile | Key action buried | Price, variant picker, quantity and Add to cart visible in the first screen |
| Variant selectors as color circles with no labels | Unclear | Swatch plus name ("Navy"); unavailable variants marked, not hidden |
| No shipping info on the product page | Surprise at checkout | Delivery areas, fees and times: "Metro Manila 2–3 days, ₱120. Provinces 5–7 days." |
| No mention of payment options | Buyers look for COD and e-wallets | "COD, GCash, Maya, card" near the price |
| Size chart missing or in inches only | Wrong units | cm first, inches second |

## 24.13 Cart and checkout

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Cart as a slide-out drawer with upsell carousel | Distraction | Cart page (or drawer) with items, quantities, subtotal and Checkout; upsell at most one row |
| Account required before checkout | Drop-off | Guest checkout; offer account creation after the order |
| Multi-step checkout with 5 steps for a single item | Friction | One page: contact, delivery address, delivery option, payment, review |
| Address form built for US (State, ZIP) | Wrong structure | Region, province, city/municipality, barangay (dependent dropdowns from PSGC), street/house no., landmark, ZIP optional |
| Mobile number validated as 10 US digits | Rejects PH numbers | Accept 09XX / +63 formats; normalize on save |
| Payment options shown as logos only | Unclear | Radio list with labels: "GCash", "Maya", "Credit/debit card", "Cash on delivery (+₱20)" |
| Totals change at the last step (shipping, fees appear) | Distrust | Show shipping and fees as soon as the address is known |
| Promo code field as the first thing on the checkout | Sends users away to search for codes | Collapsed "Have a promo code?" link |
| "Place order" button with no final total on it | Unclear commitment | "Pay ₱1,249.00" or "Place order · ₱1,249.00 (COD)" |
| Order confirmation with confetti and "You're awesome! 🎉" | Celebration | Order number, items, total, payment status, delivery estimate, what happens next, contact for issues |
| No official receipt / invoice info for business buyers | BIR needs | Option to enter TIN and business name for the invoice |
| GCash/Maya redirect return shows "Success" before confirmation | Premature | Pending state until the provider confirms. See part 21 |

## 24.14 Search results

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Results as big image cards when the content is text | Slow to scan | Text list: title, snippet with matched words highlighted, type, date |
| No count or query echo | User unsure what ran | "12 results for 'barangay clearance'" |
| No results: illustration and "We couldn't find anything 🔍" | Chatty. See part 04 | "No results for 'brgy clerance'." plus spelling suggestion and links to common pages |
| Search that needs exact matches | Misses typos and abbreviations | Handle case, accents ("ñ"), common abbreviations (Brgy., Sto., Sta.) and simple typos |
| Search query not in the URL | Cannot share or go back | `/search?q=…` |
| Filters shown before any results exist | Premature | Show filters after results, with counts per filter |

## 24.15 Legal pages

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Privacy policy copied from a generic US template (CCPA, "California residents") | Wrong law for PH clients | Privacy notice written for the Data Privacy Act of 2012 (RA 10173): what data, why, legal basis, retention, sharing, rights, DPO contact. Have the client or their counsel review |
| Terms of service generated with placeholder "[Company Name]" left in | Unfinished | Fill every placeholder; grep for "[", "Company Name", "Lorem" |
| "Last updated" date missing or set to the build date | Untraceable | Real effective date, changed only when content changes |
| Legal page styled as a marketing page with hero and gradient | Wrong tone | Plain text page, 60–75ch, numbered headings, anchor links |
| Cookie policy on a site with no non-essential cookies, plus a consent banner | Theater | No banner when only essential cookies are used; short note in the privacy notice |
| Legal text in 12px gray | Hard to read | Same body size and color as other content |
| Legal pages written by the agent and published as final | Not legal advice | Mark as a draft for the client's review in the handover notes |

## 24.16 Coming soon and waitlist

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Countdown timer to a date nobody committed to | Fake urgency | Show a date only if confirmed; otherwise "Opening in October 2026" or no date |
| "Something amazing is coming ✨" | Says nothing | Name what is coming and for whom: "Online enrollment for SY 2027–2028 opens 1 March." |
| Waitlist with "Join 5,000+ people on the waitlist" | Invented number | No count, or the real count |
| Animated gradient background with particles | Trope | Plain page with logo, one paragraph, one form or contact line |
| "Be the first to know" signup with no privacy note | Collects emails with no terms | One line on how the email will be used and a link to the privacy notice |
| Coming soon page left live for months | Looks abandoned | Replace with a minimal real page (contact, hours, what is available now) |

## 24.17 Link-in-bio page

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Linktree clone with gradient background, glass buttons and emoji per link | Template look | Solid background, plain full-width buttons with clear text |
| 15 links in random order | Nothing stands out | 3–7 links ordered by what visitors want most (order, menu, location, contact) |
| Links named "✨ My Shop ✨", "🔥 HOT DEALS 🔥" | Emoji and caps | "Order online", "Menu and prices", "Location and hours" |
| Avatar ring with animated gradient | Instagram trope | Plain logo or photo |
| No contact or location info on a local business bio page | Missing facts | Phone, address link and hours as links |

## 24.18 Event page

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Hero with event name in gradient text and a countdown | Trope | Event name, date, time, venue and cost in plain text at the top |
| Date without day of week or timezone | Ambiguous | "Sat, 18 Oct 2026, 8:00 AM–12:00 NN (PHT)" |
| Venue as a name only | People get lost | Full address, map link, landmark, parking/commute notes |
| Speakers grid with stock photos and invented titles | Fabricated | Real speakers with confirmed names and roles, or omit until confirmed |
| Register button leads to a long form | Drop-off | Only what the organizer needs: name, contact, organization, and any required fields (e.g., school, grade level) |
| No "Add to calendar" | Forgotten events | .ics download and Google Calendar link |
| Past events still show "Register now" | Stale | After the date: "This event has ended." plus photos or materials if any |
| Schedule as a timeline graphic | Hard to read on phones | Table: time, session, speaker, room |

## 24.19 Government and barangay homepage

Official wording, seals and officials are covered in part 09. Structure rules:

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Hero carousel of 5 rotating photos with Ken Burns effect | Slow on mobile data; nobody sees slide 2+ | One static photo of the actual barangay hall or area, or none |
| "Welcome to the Official Website of Barangay X! Mabuhay! 🇵🇭" hero | Hype and forced greeting | Barangay name, municipality/city and province as the H1 area; services first |
| Services hidden below news and officials' photos | Residents come for services | Top section: most requested services with requirements, fees, hours and where to go (Barangay clearance, Certificate of indigency, Residency, Business clearance, Cedula) |
| Service pages that say "Visit the barangay hall for more information" | No real info | Requirements list, fee in ₱, processing time, office hours, person/office to see, online request link if available |
| Officials section with placeholder names ("Hon. Juan Dela Cruz") or stock photos | Fabricated officials | Real officials supplied by the client with term dates; update after elections |
| News section with invented articles | Fabricated content | Real announcements with dates, or omit until the client posts |
| Announcements as a scrolling marquee ticker | Hard to read, inaccessible | Dated list of notices, newest first; urgent notice as a persistent banner. See part 21 |
| Emergency hotlines missing or buried in the footer | Critical info hidden | Hotlines near the top: barangay, police, fire (BFP), health center, MDRRMO, with click-to-call |
| Transparency documents as image scans | Not searchable | Full disclosure policy documents as searchable PDFs with dates and titles; budget, procurement, and ordinances listed by year |
| Map embed of the whole city | Not useful | Barangay hall location with landmark and office hours |
| Facebook page feed embed as the main content | Slow, tracking, breaks when FB changes | Link to the Facebook page; post key notices on the site too |
| Language: formal deep Tagalog nobody uses, or English only | Wrong register. See part 09 | Plain Filipino or English as the client decides; key service info in both if residents need it |
| Visitor counter, "Last updated" in the footer only, weather widget | Old portal clutter | Remove counter and widget; show updated dates on each notice |

## 24.20 School homepage

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Hero "Empowering Future Leaders Through Excellence in Education" | Slogan template | School name, location, levels offered (e.g., "Kinder to Grade 12, SHS strands: STEM, ABM, HUMSS"), and school ID for DepEd schools |
| Stats row ("5,000+ students, 200+ teachers, 98% passing rate") invented | Fabricated | Real figures supplied by the school with the year, or omit |
| Enrollment info buried | The top reason parents visit | Enrollment section near the top in season: dates, requirements, fees in ₱ (private schools), steps, online form link, contact |
| Announcements carousel | Missed content | Dated list; class suspension notices as a persistent banner with scope and source |
| Faculty page with stock photos | Invented people | Real names and photos with consent, or names only |
| "Virtual tour" / 3D campus link that does not exist | Filler | Remove; add real photos of facilities if supplied |
| Mission/Vision/Core values paraphrased | Official text changed | Use the official DepEd or school text verbatim |
| Portal login ("Student Portal", "LMS") as a big hero button when no portal exists | Fake feature | Link only to systems that exist |
| No contact details for the registrar or admissions | Parents call the wrong office | Office names, phone, email, hours |

## 24.21 Election and precinct finder

Used for COMELEC-style voter lookups and campaign/LGU election info pages. Data accuracy and neutrality matter more than looks.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Hero with flag gradient, confetti and "Your Voice Matters! 🗳️" | Hype on a civic tool | Page title "Find your precinct" and the search form at the top |
| Search that requires exact full name and birthdate formats | Many misses | Fields as the source data needs them (last name, first name, birthdate, city/municipality); accept name variants and "ñ"; state the date format "DD/MM/YYYY" or use three fields |
| Results showing full voter records publicly | Data privacy exposure | Show only what the official source publishes (precinct number, polling place, address); no full addresses or birthdates of others |
| Unofficial finder that looks like an official COMELEC page (seal, "Official") | Impersonation | State the data source and date; link to the official source; use no official seals unless the site is official |
| No data date shown | Stale lists mislead voters | "Voter list as of 15 Jan 2026. Confirm with your local COMELEC office." |
| Polling place shown without a map link or landmark | Voters get lost | Address, landmark, map link, accessible entrance note if known |
| Election results page with animated counters and live-looking badges on static data | Fake real-time | "Unofficial results as of 9:40 PM, 12 May. Source: …" with a timestamp; "Live" only for pushed updates |
| Candidate lists ordered by preference or styled differently | Bias | Alphabetical by surname, same styling for all, as on the official ballot |
| Heavy page that fails under election-day traffic | Outage when it matters | Static or cached pages, small payload, rate-limited search, tested under load |
| Search results in a modal | Cannot share or print | Results on the page with a print-friendly layout |

## 24.22 Check
- [ ] Only the landing page has a hero, and only with a real image or product shot.
- [ ] Main content is visible in the first 600px on a 390px-wide phone.
- [ ] Section order fits the page's visitors, not a template.
- [ ] No section exists with invented content (testimonials, team, stats, logos, news, officials).
- [ ] No lorem ipsum, "[Company Name]", "Your headline here" or placeholder people left anywhere.
- [ ] Each page has one H1 and a unique title. See part 08.
- [ ] No "Ready to get started?" CTA band by default.
- [ ] Landing page states what the business does, for whom, where, and how to contact them.
- [ ] Screenshots are real and shown without fake browser chrome.
- [ ] Pricing shows ₱ prices with VAT basis, real limits, one-time costs and payment methods.
- [ ] "Most popular" only when true; plan names describe the buyer.
- [ ] About page is facts: founded, location, who, what; team only with real people and consent.
- [ ] Contact page lists phone, address, hours and response time before the form; map loads on demand.
- [ ] Blog list is a text list with dates; no stock images per post; no invented posts.
- [ ] Articles use 60–75ch, show published and updated dates, and skip floating share bars.
- [ ] Docs home lists sections and quick start; code blocks have copy buttons.
- [ ] Changelog is a dated list with specific changes.
- [ ] Careers list real benefits, salary ranges in ₱, location and work setup.
- [ ] Portfolio shows real projects with screenshots and outcomes; no skill bars or typing effects.
- [ ] Product pages show ₱ price, shipping, payment options and Add to cart in the first screen; no fake urgency or reviews.
- [ ] Checkout allows guest orders, uses PH address structure (region to barangay), shows full costs early, and names the total on the final button.
- [ ] GCash/Maya returns show pending until confirmed.
- [ ] Search results echo the query, show a count, and live in the URL.
- [ ] Legal pages follow RA 10173, have real effective dates, no placeholders, and are flagged for client review.
- [ ] Coming soon pages state what, for whom and a confirmed date; no fake countdowns or waitlist counts.
- [ ] Link-in-bio has 3–7 plain links, no emoji labels.
- [ ] Event pages show day, date, time with PHT, full venue, calendar links, and change after the event.
- [ ] Barangay/LGU homepages put services with requirements, fees and hours first, and hotlines near the top.
- [ ] Officials, seals and news come from the client; no placeholders.
- [ ] Notices are dated lists, not marquees or carousels.
- [ ] School homepages lead with levels offered and enrollment info; official Mission/Vision text used verbatim.
- [ ] Precinct finders state data source and date, show only published fields, are neutral, and are cached for peak load.
