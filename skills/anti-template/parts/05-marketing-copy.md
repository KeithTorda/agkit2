---
part: 05
title: Marketing Copy
covers: hero headline, subhead, eyebrow text, feature blurbs, benefits, social proof, testimonials, logo walls, stats, pricing copy, plan names, FAQ, About, Team, Mission, careers, comparison tables, CTA sections, launch announcements, urgency, scarcity, trust badges, newsletter signup
---

# 05 — Marketing Copy

Read when: writing or reviewing any landing page, pricing page, About/Team/Careers page, feature section, FAQ, launch post, or any public page meant to convince someone to sign up, buy, enroll, or visit.

Guidance: DESIGN.md and the brief override this part.

Single words are banned in part 01. Phrase and rhythm tells are in part 02. Button labels in app UI are in part 03. This part covers how those tells show up in marketing sections, and what a real section says instead. Page layout for these pages is in part 24.

## 05.1 The one rule for all marketing copy

Every sentence must survive the question "Could a competitor paste this on their site unchanged?" If yes, delete it or add the fact only this client has: a place, a price, a number, a name, a date, a limit.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Copy that fits any product in the category | No fact ties it to this client | Name the product, the place, the price or the count in the first 2 lines |
| Benefit written before the fact exists | The model fills gaps with adjectives | Ask for the fact (price, hours, coverage, user count). If missing, write `[TODO: price]`, not a guess |
| Every section starts with a claim, then explains it | Pitch-deck rhythm | Start with the fact. Let the reader draw the claim |
| Copy written for "users", "businesses", "teams", "everyone" | No reader in mind | Name the reader: "sari-sari store owners in Batangas", "Grade 11 enrollees", "barangay treasurers" |
| Same length for every block (3 lines, 3 lines, 3 lines) | Generated in one pass with a template | Let length follow content. One line is fine. Twelve lines of a real process is fine |
| Copy that explains how the reader feels | Presumes emotion, sounds scripted | State what happens: "Your order ships the next business day." |
| Words from part 01 anywhere on the page | Instant AI tell | Run the part 35 grep before shipping |

## 05.2 Hero headline

The headline says what the thing is or what it does, in plain words, in 4 to 12 words. It does not describe the future, the reader's journey, or a feeling.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "The all-in-one platform for X" | Default category claim, zero information | "Inventory, sales and BIR-ready receipts for one store" |
| "Build X the modern way" | "Modern" says nothing a reader can check | Name the method: "Point-of-sale that runs offline and syncs when the internet is back" |
| "X reimagined" / "X, redefined" | Borrowed launch-keynote rhythm | Say what changed: "Enrollment forms you can fill on a phone" |
| "Ship faster with {Product}" | Speed claim with no number | "Post an order in 3 taps" or drop the claim |
| "The future of X is here" | Empty prophecy | State what exists now: "Online permit applications for Barangay San Isidro" |
| "Simple. Powerful. Beautiful." | Triad slogan, template default | One sentence with a noun and a verb |
| "Fast. Secure. Simple." / "Build. Ship. Scale." / "Create. Collaborate. Ship." | Triad slogans, see part 02 | One claim you can prove, with the number |
| "Unlock the power of X" | Banned verb, abstract object | "See this week's sales by item" |
| "Supercharge your workflow" | Banned verb, "workflow" is vague | Name the task: "Print 200 report cards in one batch" |
| "Everything you need, nothing you don't" | Template cliche | Name the three things included |
| "Where X meets Y" | Faux-poetic pairing | Say what it does |
| "X made simple" / "X made easy" | Claim anyone can make | Show the step count: "File a complaint in 2 steps" |
| "Welcome to {Product}" as the H1 | Greeting is not content | The H1 names what the page offers |
| "Imagine a world where..." | Hypothetical opener, ad voice | Describe the real current state |
| Headline in Title Case With Every Word Capitalised | Template default | Sentence case unless the client's brand guide says otherwise |
| Headline with a gradient-highlighted keyword | Visual tell, see part 10 | Solid text. Emphasis comes from the word choice |
| Two-part headline with a word swapped by a typing animation ("Built for [founders / teams / creators]") | Rotating-word effect, see part 25 | One headline for one reader |
| Headline ends with a period on one line and "for everyone." on the next | Rhythm padding | One line, one claim |
| Question headline ("Tired of manual inventory?") | Infomercial opener | Answer instead: "Count stock by scanning, not by notebook" |
| "Your journey starts here" | Banned noun "journey" | Name the first action: "Apply for a barangay clearance online" |
| LGU/school hero: "Welcome to the Official Website of the Municipality of X" | Hype plus redundancy, see part 09 | "Municipality of X" as the site name, H1 = the top task: "Pay real property tax, request documents, check announcements" |

```html
<!-- Banned -->
<h1>Revolutionize Your Business with Our All-in-One POS Solution</h1>
<p>Seamlessly manage sales, inventory, and more — all in one powerful platform.</p>

<!-- Use -->
<h1>Point-of-sale for small stores in the Philippines</h1>
<p>Ring up sales, track stock, and print BIR-registered receipts. Works offline. ₱499 a month per branch.</p>
```

## 05.3 Subhead

The subhead adds the facts the headline had no room for: price, who it is for, what is needed, where it works.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Subhead restates the headline with adjectives | Two lines, one idea | Add a new fact: price, platform, coverage, limit |
| "Seamlessly manage X, Y, and more — all in one place" | Banned adverb, "and more", em-dash aside | List the real items. Stop when the list stops |
| "Whether you're a beginner or an expert..." | "Whether you're" pattern, see part 02 | Name the one reader the page is for |
| "Designed to help you X" / "Built to X" / "Made to X" | Passive intent, not a fact | "It does X." Present tense, active |
| "Join thousands of happy customers" in the subhead | Vague social proof | Move proof to its own section with a real count and source, or delete |
| Subhead longer than 30 words | Paragraph pretending to be a subhead | Max 2 sentences, 30 words |
| Subhead with 3 comma-separated benefits ending in "and more" | Rule of three plus filler | 2 to 4 concrete items, no "and more" |
| "No credit card required" as the whole subhead | Borrowed SaaS reassurance | Use only if a card is ever required elsewhere. Put it under the button as helper text |

## 05.4 Eyebrow text and pill labels above the hero

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Glowing pill: "✨ New: AI-powered insights →" | Template eyebrow, emoji, arrow, see part 10 | No pill. If there is real news, put one plain line: "Version 2 released 3 March 2026. What changed" |
| "🚀 Now in public beta" | Emoji plus launch hype | "Beta. Some features may change." as small text near the form |
| Eyebrow repeating the section H2 ("FEATURES" above "Features that...") | Redundant label | Delete the eyebrow, or use it to carry a fact ("For stores with 1 to 5 branches") |
| Eyebrow in ALL CAPS with letter-spacing on every section | Template rhythm | Max one eyebrow per page, only when it carries information |
| "Introducing {Product} 2.0" on a site that never had 1.0 | Fake version history | No version claim on a first launch |
| "Backed by Y Combinator" when not true | Fabricated trust | Only real, verifiable backers. Otherwise nothing |
| "#1 Rated" / "Award-winning" without the award named | Unverifiable claim | Name the award, year and body, with a link, or delete |

## 05.5 Feature blurbs

Feature blocks describe one capability each: what it does, a limit or number, and where to see it. No icon + title + vague sentence cards.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Icon + two-word title + one vague sentence, repeated 3 or 6 times | Default AI feature grid | Screenshot or short list. Each item: capability, number or limit, where it lives |
| Titles like "Lightning Fast", "Rock Solid", "Secure by Default", "Built to Scale" | Adjective titles with no data | Title = the feature noun: "Offline sales", "Barcode scanning", "Daily Z-reading" |
| "Advanced analytics" | "Advanced" is unmeasurable | "Sales by item, by hour and by cashier. Export to Excel." |
| "Enterprise-grade security" | Banned adjective, no specifics | "Passwords hashed with bcrypt. Admin actions logged. Daily backups kept 30 days." |
| "Real-time sync" when it polls | False claim, see part 04 for live labels | "Syncs every 5 minutes when online" |
| "AI-powered" on a feature with no model | Buzzword stamping | Name the actual method or drop the prefix |
| "Smart" prefix (Smart Inventory, Smart Reports) | Filler adjective | Name what it computes: "Low-stock alerts at a level you set" |
| ALL CAPS feature brand names: LIGHTNING MODE, TURBO SYNC, SMART ENGINE | Invented jargon, see part 02 | Plain noun: "Offline mode", "Background sync" |
| "Seamless integration with your favourite tools" | Two banned words, no list | "Imports from Excel and CSV. Exports to Excel, PDF, and QuickBooks." |
| "Works on any device" | Untested claim | "Works in Chrome and Safari on phones and laptops. No app to install." Test it first |
| "24/7 support" from a solo developer | False promise | Real hours: "Support by email, Monday to Friday, 9am to 6pm" |
| "Unlimited everything" | Almost never true | State the real limits: "Up to 5,000 products per branch" |
| "Customizable to fit your needs" | Vague | Name what can be changed: "Your logo and TIN on every receipt" |
| "Intuitive dashboard" | If it needs the word, it is not | Show a screenshot. Delete the adjective |
| Six features when the product has three | Padding to fill the grid | Show the three. Grids do not need to be full |
| Feature list copied from a competitor's site | Same claims, wrong product | Build the list from the client's actual scope doc or code |
| Feature section headed "Why choose us?" | Rhetorical question heading | "What it does" or the feature names as headings |
| "Everything you need to succeed" as the section H2 | Filler heading | H2 = what the list contains: "Sales, stock and receipts" |
| Feature blurbs that all start with "Easily" | Adverb tic | Start with the verb: "Scan", "Print", "Export" |
| School site: "World-class education for the leaders of tomorrow" | Hype, unverifiable | Programs offered, strands, tuition range, enrollment dates, DepEd/CHED recognition number |
| LGU site: "Serving the people with excellence and integrity" | Slogan with no service in it | List of services with office, hours, requirements and fees |

```html
<!-- Banned -->
<div class="feature">
  <span class="icon">⚡</span>
  <h3>Lightning Fast</h3>
  <p>Experience blazing-fast performance that keeps up with your business.</p>
</div>

<!-- Use -->
<li>
  <h3>Offline sales</h3>
  <p>Keep selling when the internet drops. Sales upload when the connection returns. Tested with 3 days offline.</p>
</li>
```

## 05.6 Benefits and value propositions

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "Save time and money" | Every product claims it | "Closing the store takes 5 minutes instead of 40." Only if measured with the client |
| "Boost productivity by 10x" | Invented multiplier | Delete, or cite the client's own before/after with dates |
| "Focus on what matters most" | Empty, presumes reader priorities | Name the task that is removed: "No more copying sales into a notebook" |
| "Grow your business" | Generic outcome | Name a mechanism: "Customers can order from your Facebook page link" |
| "Peace of mind" | Feeling, not a fact | The fact behind it: "Backups every night. Restore any day from the last 30." |
| "Say goodbye to X. Say hello to Y." | Paired cliche | "Replaces your paper logbook." |
| "Stop wasting time on X" | Scolding opener | "X takes 2 clicks." |
| Benefit + feature pairs where benefit is always "so you can focus on growth" | Repeated template filler | Only state a benefit when it is not obvious from the feature |
| "Empowers you to take control" | Banned verb, abstract | Say what the reader can now do |
| Before/after section with invented pain points | Fabricated problem framing | Use pain points the client or real users stated. Otherwise skip the section |

## 05.7 Social proof, testimonials, reviews

Never invent a person, a quote, a rating, a review count, or a company. If the client has no testimonials, the page has no testimonial section.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Three testimonial cards from "Sarah J., CEO at TechCorp" | Invented people, invented company | Real quotes with written permission, full name, role, and business. Or no section |
| Avatars from pravatar, randomuser, Unsplash faces | Stock faces, see part 26 | Real photo supplied by the person, or initials, or no photo |
| Five gold stars on every testimonial | Fabricated rating | Stars only when pulled from a real review source, with link and count |
| "4.9/5 from 2,000+ reviews" | Invented aggregate | Real rating, real source (Google, Facebook page), date checked. Or delete |
| "Loved by thousands" / "Trusted by teams worldwide" | Vague social proof | Real count with scope: "Used in 32 stores since 2024" |
| "Join 10,000+ teams already using X" | Invented number, bandwagon | Real number with date, or delete |
| Quotes that all praise the same adjective ("so intuitive", "game-changer") | Model voice, not human voice | Real quotes keep typos and specific details. Do not polish them into marketing |
| Quote that reads like the feature list ("The real-time analytics and seamless integrations transformed our workflow") | Nobody talks like this | If supplied quotes sound like this, ask the client for the original words |
| Testimonial carousel auto-rotating every 3s | Motion tell, hides content | Static list. Show 1 to 3 |
| "As seen in" with Forbes, TechCrunch logos | Fabricated press | Only real coverage, linked to the article |
| Filipino site with only foreign-sounding names ("Emily Carter, Austin TX") | Template placeholder never replaced | Real local customers, or no section |
| Placeholder names like "Juan Dela Cruz" shipped live | Sample data left in | Replace before launch or remove the block |
| Case study cards with invented percentages ("Increased sales by 300%") | Fabricated statistic | Real case study with client approval, or nothing |
| "Our customers say" H2 with one testimonial | Section built around the template, not the content | Put the one quote inline near the relevant feature |
| Tagalog testimonial that is clearly machine-translated | See part 09 | Use the customer's own words in the language they wrote |

## 05.8 Logo walls

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "Trusted by leading companies" + 6 grey logos (Google, Microsoft, Airbnb, Stripe) | Fake logo wall, legal risk | Only clients who agreed in writing. Otherwise no wall |
| Logos made up by the model ("Acme", "Globex", "Initech", "Umbrella") | Placeholder never replaced | Remove before launch |
| Infinite marquee of logos | Template motion, see part 10 and 25 | Static row, 3 to 8 logos, wraps on mobile |
| Logos of tools used ("Built with React, Tailwind, Vercel") shown as clients | Misleading | A "Built with" line belongs in the footer or README, not in social proof |
| LGU/school logo wall of "partners" (DepEd, DICT, DOH) without an actual agreement | Implies endorsement | Only list agencies with a real MOA or program, with the program name |
| Grayscale logos that turn color on hover | Template interaction | Plain logos at one consistent height (e.g. 32px). No hover effect |

## 05.9 Stats and numbers

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "10x faster", "3x more productive" | Invented multipliers | A measured number with the baseline: "Receipts print in under 2 seconds on a ₱3,000 thermal printer" |
| Stats row: "10K+ users, 99.9% uptime, 24/7 support, 150+ countries" | Template stat bar | Only numbers the client can defend. One or two is enough |
| "99.9% uptime" with no monitoring | Unsupported SLA | State it only if measured, with the period. Otherwise delete |
| Round numbers with plus signs everywhere (500+, 1M+, 50+) | Placeholder shape | Real figure: "1,284 enrolled students, SY 2025–2026" |
| Animated counters ticking up | Motion tell, see part 25 | Render the number |
| "Save up to 80%" | "Up to" hides the typical case | State the typical case, or delete |
| "Zero downtime" | Absolute claim | "Updates deploy without taking the site offline" if true |
| "#1 in the Philippines" | Unverifiable rank | Name the ranking source and year, or delete |
| Stats in dollars on a PH site | Wrong market | Peso with ₱ and thousands separators: ₱12,500. See part 09 |
| Numbers without units or period ("2,000 orders") | Missing context | "2,000 orders a month" |
| Government site: "Serving 50,000+ constituents" | Rounded, unsourced | "Population 48,213 (PSA 2020 Census)" |

## 05.10 Pricing page copy

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| H1 "Simple, transparent pricing" | Every SaaS template | "Pricing" or "Plans and prices" |
| Subhead "Choose the plan that's right for you" | Filler | State what differs between plans in one line: "Plans differ by number of branches and users." |
| "Unlock premium features! ✨" upgrade prompt | Banned verb, emoji | "Pro — ₱999/mo. Adds multi-branch reports and 10 users." |
| Price shown in $ on a PH client site | Wrong currency | ₱ with space rules from part 04: "₱499/month" |
| "Starting at ₱0" | Coy phrasing | "Free" plan, with its limits listed |
| "Most popular" badge on the middle plan by default | Template anchoring, often invented | Only if sales data shows it. Otherwise no badge |
| "Best value" badge on the annual plan | Template anchoring | State the saving: "₱4,990/year (2 months free)" |
| Feature checklists with 20 checkmarks per plan | Padding; hides the real difference | List only the rows that differ between plans. Put shared features in one line above |
| Rows like "Premium support", "Advanced analytics" | Vague tiers | "Email support, reply within 1 business day" vs "Phone support, 9am–6pm" |
| "Contact us for Enterprise pricing" on a small-business product | Borrowed enterprise tier | Remove the tier unless the client sells it |
| Toggle "Monthly / Annually (save 20%)" when the saving is a different number | Template number kept | Compute the real saving from the real prices |
| Price with ".99" on a PH local service | Foreign retail habit | Whole pesos unless the client prices otherwise |
| "No hidden fees" | Raises the suspicion it denies | List every fee: VAT included or not, setup fee, hardware |
| Missing VAT statement | PH buyers need it | "Prices include 12% VAT." or "Prices exclude VAT." Confirm with the client |
| Payment methods missing | PH buyers ask first | "Pay by GCash, Maya, bank transfer (BDO, BPI), or card." Only real ones |
| "Cancel anytime" when there is a contract | False | State the real term: "12-month contract. Cancel with 30 days notice after month 12." |
| "Free trial" with no length | Vague | "14-day trial. No card needed." Only if true |
| Money-back guarantee invented by the agent | Legal promise the client never made | Only what the client confirms in writing |

## 05.11 Plan and tier names

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Starter / Pro / Enterprise on every product | Default trio | Names from what the plan covers: "1 branch", "Up to 5 branches", "Custom" |
| Hobby / Pro / Team / Enterprise | Copied from dev-tool pricing | Match the client's buyers: "Sari-sari", "Grocery", "Chain" only if the client uses those words |
| Platinum Member, Diamond Tier, Mythic Rank, Elite Member | Gamified fantasy tiers | Plain: Free, Basic, Standard, Custom. Or by capacity |
| Galaxy / Rocket / Launch / Orbit plan names | Space theme default | Plain names |
| "Growth" plan that adds one feature | Name promises an outcome | Name by what is added: "With reports" |
| Plan descriptions: "Perfect for individuals", "Ideal for growing teams", "Built for large organizations" | Template trio | Limits: "1 user, 1 branch", "5 users, 3 branches" |
| Membership ranks in community products: Celestial Luminary, Code Wizard, Tech Ninja, Power User, Legendary Member | Fantasy titles, see part 04 for badges | Admin, Mod, Member, Contributor, Staff, Level 12, with the plain requirement: "50 posts" |

## 05.12 FAQ

FAQ answers questions real people asked. If no one asked, it is not a FAQ.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "What is {Product}?" as question 1 | The page already said it | Start with the most asked question from the client's inbox or chat |
| "Why should I choose {Product}?" | Sales pitch in a FAQ | Delete |
| "Is {Product} secure?" answered "Absolutely! We take security seriously." | Empty reassurance, exclamation | Specifics: where data is stored, who can access it, backups, how to delete it |
| "Is there a free trial?" "Yes! Get started today." | Pitch disguised as an answer | "Yes. 14 days. No card needed." |
| Every answer starts with "Great question!" or "Absolutely!" | Chatbot voice | Start with the answer: "Yes." "No." "₱499 a month." |
| Answers that end with "Contact us for more information" | Deflection | Answer fully, then link to contact only for account-specific cases |
| 6 questions exactly, all 2 lines | Template count | As many as real questions exist |
| "Still have questions? We're here to help! 💬" CTA block | Cheerful template closer | "Other questions: {email} or {phone}, Mon–Fri 9am–5pm." |
| Accordion that allows only one open item | Hides content, forces clicks | Plain list of questions and answers, or accordion that allows many open |
| School FAQ missing enrollment requirements, tuition, dates | Filled with brand questions instead | Requirements list (PSA birth certificate, Form 138, Good Moral), fees, schedule, contact |
| LGU FAQ missing office hours, fees, where to go | Generic questions | Service, office, room, hours, fee in ₱, requirements, processing time |
| Answer uses "simply" or "just" ("Simply click the button") | Minimising words, see part 01 | "Click Upload." |

## 05.13 About, Mission, Team

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "We believe in..." / "We're passionate about..." / "We care deeply about..." | Feelings instead of facts | What the company does, since when, where, for whom |
| "Our mission is to empower businesses to reach their full potential" | Template mission | One sentence of what they do: "We build point-of-sale software for small stores in Laguna." Or no mission line |
| "Founded in 2020 with a simple idea..." origin story invented by the agent | Fabricated history | Only the history the client provided |
| "Our values: Innovation, Integrity, Excellence" with icons | Value-word grid | Delete, or replace with concrete practices the client follows ("We reply to support email within 1 business day") |
| "A team of passionate innovators" | Hype about people | Names, roles, and what each person handles |
| Team grid with stock photos and invented names | Fabricated people | Real team with photos and permission, or no team section |
| Bio: "John is a visionary leader with 20+ years of experience driving transformation" | LinkedIn-summary voice | "John runs sales and support. Before this he managed 3 hardware stores in Cavite for 12 years." |
| Fun-fact line on every bio ("Coffee lover ☕") | Template filler | Delete unless the client asked |
| "Built by developers, for developers" / "Made by creators, for creators" | Fake specificity | Who built it and why, in one line, or nothing |
| "{App} understands your needs" / "{App} learns and adapts" | Anthropomorphising the product | Say what the software does: "Remembers your last 10 customers" |
| LGU page: "Meet our dedicated public servants" with "Hon. Juan Dela Cruz" placeholders | Fake officials, see part 09 | Real officials from the client with official photos and positions, or leave the list out until provided |
| School About: "a premier institution of academic excellence" | Hype, unverifiable | Founding year, location, levels offered, recognition numbers, accreditation body and level |
| Timeline section with evenly spaced milestones every year | Invented history shape | Only real dated events |

## 05.14 Careers

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "Join our rockstar team!" / "We're hiring ninjas" | Hype, exclamation | "Open roles" heading, list of roles |
| "Work with passionate people on exciting challenges" | Generic | What the job does day to day, the stack, the team size |
| Perks grid: unlimited PTO, free snacks, ping-pong table | US startup template | Real benefits: HMO, 13th month pay, leave days, work setup, location |
| No salary range | Readers skip the post | Salary range in ₱ per month, if the client allows |
| "Competitive salary" | Hides the number | The range, or omit the line |
| "Fast-paced environment" | Cliche, often a warning | Hours and work setup: "Mon–Fri, 8am–5pm, onsite in Makati" |
| "We're always looking for talent" with no open roles | Empty section | "No open roles now." plus an email for applications |
| "We value diversity and inclusion" as the only line | Boilerplate | Remove or add the actual policy |
| Requirements: "5+ years in a similar role" for a junior post | Template copy | Requirements from the actual job |
| Application steps missing | Reader does not know what happens next | "Send CV to {email}. We reply within 5 working days. One interview, one practical test." |

## 05.15 Comparison tables

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "Us vs Them" table where the client has every checkmark and competitors have red X's | Obviously biased, often false | Only verified, dated comparisons, with competitor names only if the client approves. Otherwise compare with "paper logbook" or "spreadsheet" |
| Rows that are adjectives ("Easy to use", "Modern design") | Unverifiable | Rows that are facts: "Works offline", "Prints BIR receipts", "Price per month" |
| Competitor columns named "Competitor A", "Others", "Legacy tools" | Template placeholder | Name the real alternative or compare with the old manual process |
| Green check and red X icons only, no text | Color-only meaning, see part 27 | "Yes", "No", or the value ("₱499", "Up to 5") |
| Comparison of features the product does not have yet | False | Current features only. Roadmap items go on a roadmap page with "Planned" |

## 05.16 CTA sections and landing-page buttons

The button says what happens when it is pressed. The section around it states the one condition the reader needs (price, time, what is needed). Button label rules for app UI are in part 03.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "Ready to get started?" heading + "Get Started Today" button | Rhetorical question and generic CTA | Heading states the action and its cost: "Try it free for 14 days". Button: "Create account" |
| "Start Your Free Trial" / "Start Free" / "Try it Free" | Default SaaS labels | "Create account", "Start 14-day trial" only if a trial exists |
| "Get Started" | Says nothing about the next screen | Name the next step: "Create account", "Apply online", "Order now" |
| "Learn More" / "Explore Features" / "Discover" | Vague, banned verbs | Name the destination: "See pricing", "Read the requirements", "View all services" |
| "Book a demo" / "Request access" / "See it in action" | B2B template when there is no sales team | Match what the client offers: "Message us on Messenger", "Call 0917 123 4567", "Visit the store" |
| "Join the revolution" / "Claim your spot" / "Reserve your seat" | Hype, false scarcity | "Register", "Sign up for the seminar (40 seats)" with the real number |
| "Take the first step" / "Start building" / "Start creating" / "See the magic" / "See the difference" | Abstract | The verb of the actual action |
| "Unlock Now" / "Supercharge your..." / "Dive in" | Banned verbs | Literal action |
| Two buttons side by side: "Get Started" (filled) + "Learn More" (outline) on every section | Template pair | One primary action per section. Secondary only if it goes somewhere different and useful |
| Final CTA section repeats the hero word for word | Filler | End with contact details and the single action, or end with the footer |
| "No credit card required. Cancel anytime. 14-day free trial." triple under every button | Reassurance triad | The one condition that applies, once, under the main button |
| CTA section on a gradient background with blobs | Visual tell, see part 10 | Same surface as the page, or one token-based solid band from DESIGN.md |
| PH small business site with "Sign up" as the only action when sales happen on Messenger | Wrong channel | "Message us on Facebook" or "Order via Messenger" with the real page link |
| LGU site CTA "Get Started" | Wrong frame for a public service | Task verbs: "Request barangay clearance", "Check requirements", "Pay online" |
| School site CTA "Enroll Now!" with exclamation | Hype mark | "Enroll for SY 2026–2027" plus the deadline |
| CTA copy mixing styles on one page ("Get Started", "Sign up", "Create your account") | Inconsistent verbs | One label for one action across the whole site |

## 05.17 Launch and product announcements

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "We're excited to announce..." / "Thrilled to share..." / "We're thrilled to introduce..." | Feeling-first opener | Start with the thing: "Version 2 adds offline mode and multi-branch reports." |
| "Today marks a new chapter..." / "This is just the beginning..." | Narrative filler | Date and change: "From 3 March 2026, receipts show your TIN and branch code." |
| "Be the first to try..." | Scarcity with no limit | "Available to all accounts from 3 March." |
| "Introducing: X ✨" as the headline | Emoji and colon reveal | "X is available" or "New: X" |
| "And that's just the beginning…" ellipsis closer | Mystery ending | End with what the reader can do now, or with the date of the next known change |
| Launch post with no date, version, or list of changes | Hype with no content | Date, version, bullet list of changes, what the user must do (if anything), link to full changelog. Changelog format is part 06 |
| "Stay tuned for more exciting updates!" | Filler closer, exclamation | Delete |
| "Coming soon" section full of features never scheduled | Invented roadmap | Only dated, client-approved plans, marked "Planned" |
| Waitlist page: "Something big is coming. Be the first to know. 🚀" | Teaser template | What it is, who it is for, when it launches (month at least), email field |

## 05.18 Urgency and scarcity

Urgency is allowed only when it is true and specific: a real deadline, a real seat count, a real stock count.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "Limited spots!" / "Only 3 left!" when untrue | False scarcity, may breach consumer rules | Real count pulled from data, or delete |
| Countdown timer that resets on reload | Dark pattern | Real deadline as a date: "Early rate ends 31 May 2026, 11:59pm PHT" |
| "Offer ends soon" | Vague deadline | The date |
| "Hurry! Prices go up tomorrow!" | Exclamation, pressure | "Price changes to ₱699 on 1 July 2026." |
| "X people are viewing this right now" | Fake live counter | Delete |
| "Don't miss out!" / "Act now!" / "Last chance!" | Pressure words | State the deadline and let the reader decide |
| Popup on exit: "Wait! Don't go!" | Dark pattern, exclamation | No exit popup |
| "Sold out" badge used as decoration | Misuse of status | Only when stock is 0 |
| Enrollment urgency on school site: "Slots filling up fast!" | Unsupported | "Grade 7 slots: 40. Enrollment closes 15 June 2026." |
| Confirm-shaming decline link: "No thanks, I don't want to save money" | Manipulative | "No thanks" |

## 05.19 Trust badges and guarantees

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "100% Secure Checkout" shield badge | Generic image, no meaning | Name the payment processor: "Payments processed by PayMongo" if true |
| "SSL Secured" badge | Every site has HTTPS; badge adds nothing | Delete |
| "GDPR compliant" on a PH-only product | Wrong law, often untrue | "We follow the Data Privacy Act of 2012 (RA 10173)." only if the client confirms, with a link to the privacy notice |
| "SOC 2", "ISO 27001", "HIPAA" badges without certification | False claim | Only certifications the client holds, with certificate number |
| "Money-back guarantee" seal | Promise the client never made | Only confirmed guarantees, with terms in plain text |
| "Verified", "Trusted", "Certified" badges with no issuer | Meaningless | Name the issuer: "DTI registered, BN 1234567" or "SEC Reg. No. CS2021..." |
| Fake government seals or DOST/DICT logos on a private site | Impersonation risk, see part 09 | Only real accreditations with permission |
| BIR registration claim without details | Incomplete | "BIR-registered. TIN 123-456-789-000." Only real numbers from the client |
| Payment-method logo strip with every wallet and card | Implies support that may not exist | Only the methods actually accepted (GCash, Maya, cards, bank transfer) |
| "Rated Excellent" badge from no named source | Invented | Real source and link, or delete |

## 05.20 Newsletter and lead capture

Email content itself is in part 08. This covers the signup block on a marketing page.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "Stay in the loop! Get exclusive updates 📬" | Exclamation, emoji, "exclusive" | "Email updates" with one line on what and how often: "New products and price changes. About twice a month." |
| Newsletter signup on a site that will never send a newsletter | Template block | Remove it |
| "Join our community of 5,000+ subscribers" | Invented number | Real number or nothing |
| "We respect your privacy. No spam, ever." | Boilerplate promise | "Unsubscribe from any email." plus link to privacy notice |
| Lead magnet "Download our free ultimate guide" that does not exist | Fake offer | Only real downloads with the file name and size |
| Popup newsletter after 3 seconds | Interrupting pattern | Inline block at the end of content, or footer link |
| Email field placeholder "Enter your email address to get started" | Long placeholder, vague | Label "Email", button "Subscribe" |
| Success message "You're in! 🎉 Welcome to the family!" | Emoji, family framing | "Subscribed. Check your email to confirm." |

## 05.21 Section headings on marketing pages

Heading grammar and patterns are in part 02. These are the marketing-specific headings to replace.

| AI heading | Use instead |
|---|---|
| What makes us different? | Delete, or a specific comparison heading: "Compared with a paper logbook" |
| Here's what you'll get | What's included |
| How it works (with 3 numbered steps that are "Sign up, Customize, Launch") | How to order / How to apply, with the real steps, however many |
| Our customers love us | Customer reviews (only with real reviews) |
| Built for the modern X | Who it is for, plainly |
| The {Product} difference | Delete |
| Pricing that scales with you | Pricing |
| Get in touch | Contact |
| Our story | About |

## 05.22 Filipino and local marketing copy

Language-level Filipino tells are in part 09. These are the marketing-page ones.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "Mabuhay!" as the hero headline on a non-tourism site | Forced local color | Plain headline naming the service |
| "Sulit na sulit!" / "Tara na!" on every CTA | Tourist-brochure Taglish | Use Taglish only if the client's audience and existing posts use it. Match their Facebook page voice |
| "Proudly Pinoy-made!" badge | Slogan with exclamation | "Made in Cebu by {Company}" if the client wants it |
| US-centric proof: "Trusted by Fortune 500 companies" on a sari-sari POS | Wrong market | Local proof: real store names, real barangays |
| Prices as "$29/mo" or "PHP 499.00" in hero | Wrong or clunky format | "₱499 a month" |
| Contact as a US-format phone "(555) 123-4567" | Placeholder never replaced | Real number: "0917 123 4567" or "+63 917 123 4567" |
| "Free shipping nationwide!" without zones | Often false for islands | "Free delivery within Metro Manila. Provincial rates at checkout." per client rules |
| "Cash on delivery available" missing on e-commerce | Local buyers expect it stated | State COD, GCash, Maya, bank transfer, and any limits |
| Business hours missing or written "Open 24/7" | Wrong or missing fact | "Mon–Sat, 8am–6pm. Closed Sundays and holidays." |
| Store address "123 Main Street" placeholder | Template data | Full local address: Unit, Street, Barangay, City/Municipality, Province |
| Hero photo of a Western office for a Davao bakery | Stock mismatch, see part 26 | Real photos of the store, product, staff |

## 05.23 Before-ship rewrite procedure

Run these steps on every marketing page before handing it over.

1. Grep the page for part 01 words and part 02 phrases. Replace each hit or delete the sentence.
2. For every number, find its source. No source: delete the number or mark `[TODO: confirm with client]`.
3. For every person, quote, logo, rating and award, confirm it came from the client. If not: delete.
4. For every button, write what the next screen is. If the label does not say it, rename the button.
5. Read the hero out loud with the client's name removed. If it could be any company, add the place, price or reader.
6. Delete every section that has no client-supplied content (testimonials, team, stats, logos, FAQ).
7. Check prices: ₱ symbol, VAT statement, payment methods, billing period.
8. Check contact: real phone, email, address, hours, Messenger or Facebook link.

## 05.24 Check

- [ ] Hero headline names what the product or service is, in 4 to 12 words, with no part 01 words
- [ ] Subhead adds a new fact (price, reader, place, platform, limit)
- [ ] No "all-in-one", "reimagined", "the future of", "the modern way", "made simple"
- [ ] No triad slogans ("Fast. Secure. Simple.")
- [ ] No rhetorical question headings ("Why choose us?", "Ready to get started?")
- [ ] At most one eyebrow on the page, and it carries a fact
- [ ] No glowing "New" pill unless there is a real dated release
- [ ] Each feature block names the feature, a number or limit, and where it lives
- [ ] No adjective-only feature titles ("Lightning Fast", "Rock Solid")
- [ ] No "AI-powered", "smart", "real-time" unless literally true
- [ ] Feature count equals real feature count; no padding to fill a grid
- [ ] No invented testimonials, names, avatars, ratings, review counts or case studies
- [ ] Logo wall shows only clients or partners with written permission
- [ ] No "Acme", "Globex", "Juan Dela Cruz", "Sarah J." placeholders
- [ ] Every stat has a source and a period; no "10x", "99.9%", "10K+" without evidence
- [ ] No animated counters or auto-rotating testimonial carousels
- [ ] Prices in ₱ with thousands separator, billing period and VAT statement
- [ ] Payment methods listed are the ones actually accepted
- [ ] "Most popular" / "Best value" badges only when backed by data or real saving
- [ ] Pricing table lists only rows that differ between plans
- [ ] Plan names describe capacity or scope, not fantasy tiers
- [ ] FAQ questions come from real questions; answers start with the answer
- [ ] No "Great question!", "Absolutely!", "Simply" in FAQ answers
- [ ] About page states what, where, since when, for whom; no "We believe" / "We're passionate"
- [ ] Team section shows only real people with permission
- [ ] Careers posts show role duties, work setup, salary range or omit the line, real benefits
- [ ] Comparison tables use facts as rows and text ("Yes", "No") not icons alone
- [ ] Every CTA label names the next step; one label per action site-wide
- [ ] No "Get Started", "Learn More", "Book a demo", "Start Free Trial" unless that exact thing exists
- [ ] At most one reassurance line under the main CTA
- [ ] Launch posts have a date, version and change list; no "We're excited to announce"
- [ ] Urgency only with a real deadline or real count; no reset timers, no confirm-shaming
- [ ] Trust badges only for real certifications, with issuer and number
- [ ] Privacy claims cite RA 10173 only when the client confirms compliance
- [ ] Newsletter block exists only if the client will send email; says what and how often
- [ ] LGU and school pages lead with services, requirements, fees and dates, not slogans
- [ ] Contact block has a real +63 or 09XX number, full PH address, hours
- [ ] Taglish or Tagalog marketing copy matches the client's existing voice, see part 09
- [ ] Every `[TODO]` marker is listed in the handover report, see part 07
