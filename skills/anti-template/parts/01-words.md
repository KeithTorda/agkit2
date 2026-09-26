---
part: 01
title: Banned Words
covers: hype adjectives, speed and scale adjectives, aesthetic adjectives, banned verbs, abstract nouns, adverbs, intensifiers, hedges, LLM-signature words, corporate jargon, institutional hype words, product-naming words, context exceptions, replacement tables
---

# 01 — Banned Words

Read when: writing or reviewing any text a person will read: UI strings, landing pages, docs, meta tags, emails, commit messages, plans.

## 01.1 How to apply these lists

A banned word is a word that adds tone but no fact. Delete it first. If the sentence breaks, replace it with a number, a name, or the literal action. If neither works, the sentence had no content; delete the sentence.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Swap a banned word for its synonym ("robust" to "sturdy") | Same empty claim, new spelling | Replace with a fact: a number, a limit, a named feature |
| Keep the adjective and add a number ("blazing fast, under 200ms") | The adjective still reads as sales copy | Keep only the number: "Loads in under 200ms" |
| Stack two banned words ("powerful, intuitive dashboard") | Stacked adjectives are the strongest single tell | Name what the dashboard shows: "Dashboard with daily sales and stock levels" |
| Use a banned word because the client brief used it | The brief is sales talk, the page is not | Ask what the claim means, write that fact |
| Put banned words in `alt`, `title`, `aria-label`, meta tags | Screen readers and search results read them aloud | Same rules apply to every attribute string |

Phrases and sentence shapes are in part 02. Button and toast wording is in part 03. Tagalog and Taglish hype words are in part 09.

## 01.2 Banned adjectives: quality and hype

```
seamless, powerful, robust, enterprise-grade, cutting-edge, next-gen, next-generation, state-of-the-art, revolutionary, game-changing, groundbreaking, transformative, delightful, world-class, best-in-class, industry-leading, market-leading, leading, premier, unparalleled, unmatched, unrivaled, unprecedented, exceptional, remarkable, extraordinary, incredible, amazing, awesome, fantastic, phenomenal, outstanding, superior, ultimate, top-notch, first-class, top-tier, high-end, premium, exclusive, VIP, pro-level, professional-grade, military-grade, bank-grade, bulletproof, rock-solid, battle-tested, future-proof, innovative, visionary, disruptive, magical, epic, legendary, insane, mind-blowing, jaw-dropping, must-have, essential, indispensable, invaluable, perfect, flawless, ideal, optimal, holistic, comprehensive, extensive, all-encompassing, end-to-end, full-featured, feature-rich, all-in-one, one-stop, turnkey, curated, handcrafted, hand-picked, bespoke, tailor-made, tailored, personalized (when it is not), trusted, proven, reliable (without evidence)
```

| AI word | Use instead |
|---|---|
| seamless, hassle-free | "works with X", "compatible with X", "imports CSV from X" |
| powerful, robust | solid, reliable, or state the limit: "handles 10,000 rows" |
| enterprise-grade | the actual fact: "for teams of 50+", "SSO and audit log included" |
| cutting-edge, next-gen, state-of-the-art | current, rebuilt, v2, or the version number |
| revolutionary, game-changing, groundbreaking | new, changed, rewritten, or say what changed |
| transformative, disruptive | say the before and after: "Enrollment went from paper forms to one online form" |
| delightful, gorgeous, magical | simple, clear, or delete |
| world-class, best-in-class, industry-leading | delete entirely |
| premier, leading (school, LGU, company) | delete, or state a verifiable fact: "Founded 1965", "Level III accredited by PAASCU" |
| unparalleled, unmatched, unrivaled | delete; comparisons need a named competitor and a number |
| exceptional, remarkable, extraordinary, incredible, amazing | delete |
| ultimate | delete, or "complete" only if every item is listed |
| premium, exclusive, VIP | paid, members-only, Pro plan |
| bank-grade, military-grade | the real thing: "TLS 1.3", "AES-256 at rest", "passwords hashed with bcrypt" |
| bulletproof, rock-solid, battle-tested | "running since 2023", "used by 14 barangays", or delete |
| future-proof | delete; nobody can check it |
| innovative, visionary, futuristic | delete, or say what is new |
| holistic, all-encompassing | list what it covers |
| comprehensive, extensive, full-featured, feature-rich | "covers X, Y, Z" (list them) |
| all-in-one, one-stop, end-to-end, turnkey | list the parts: "Sales, stock and payroll in one app" |
| curated, handcrafted, hand-picked | picked, chosen, built, written |
| bespoke, tailor-made, tailored | custom, or "built for {client}" |
| essential, indispensable, must-have | delete; let the reader decide |
| perfect, flawless, ideal, optimal | delete, or "recommended" with a reason |
| trusted, proven | who trusts it and how many: "Used by 3 schools in Pangasinan" |

## 01.3 Banned adjectives: speed, scale, ease

```
blazing, blazing-fast, lightning-fast, ultra-fast, super-fast, rapid, instant (when not), real-time (when not), effortless, frictionless, hassle-free, painless, pain-free, easy-to-use, user-friendly, intuitive, simple (as a claim), straightforward, no-code (when code is needed), scalable, infinitely scalable, limitless, unlimited (when capped), massive, huge, tons of, countless, endless, ultra, hyper, mega, supercharged, turbocharged, high-performance, performant, lightweight (without size), blazingly
```

| AI word | Use instead |
|---|---|
| blazing, lightning-fast, ultra-fast | the measured time: "under 200ms", "page loads in 1.2s on 3G" |
| instant | "under 100ms", or drop it if not measured |
| real-time | "Live" only for push (WebSocket, SSE); "Updated every 30s" for polling. See part 04. |
| effortless, frictionless, painless | the step count: "3 fields", "no account needed" |
| easy-to-use, user-friendly | delete |
| intuitive | delete. If the UI needs the word, it is not intuitive. |
| simple (as a selling point) | say how: "One page, no setup" |
| scalable, infinitely scalable | the tested number: "tested with 50,000 voter records" |
| unlimited | the real cap, or "no limit on projects" if true and checked |
| limitless, endless, countless | a number or delete |
| lightweight | the size: "12 KB gzipped" |
| high-performance, performant | a benchmark or delete |
| no-code | "no programming needed for X"; state what still needs code |
| massive, huge, tons of | a number: "3,400 products" |

## 01.4 Banned adjectives: look and feel

```
stunning, gorgeous, beautiful, breathtaking, elegant, sleek, slick, polished, sophisticated, refined, modern, contemporary, futuristic, fresh, clean (as a claim), minimalist (as a claim), crisp, vibrant, dynamic, immersive, engaging, captivating, compelling, eye-catching, striking, bold, luxurious, lush, rich, pixel-perfect, beautifully designed, thoughtfully designed, carefully crafted
```

| AI word | Use instead |
|---|---|
| stunning, gorgeous, beautiful, breathtaking | delete; show the screenshot |
| elegant, sleek, polished, sophisticated, refined | delete |
| modern, contemporary, fresh | delete, or the year or version: "Redesigned 2026" |
| clean, minimalist, crisp | delete; a clean page does not announce it |
| vibrant, dynamic, immersive | active, full-screen, or delete |
| engaging, captivating, compelling | delete, or the measurable effect |
| pixel-perfect | delete |
| beautifully designed, thoughtfully designed, carefully crafted | delete the whole phrase |
| luxurious, lush, rich (for UI) | delete |

## 01.5 Banned verbs

```
unlock, unleash, empower, elevate, supercharge, turbocharge, streamline, accelerate, revolutionize, transform, reimagine, reinvent, redefine, rethink, disrupt, dive in, dive into, deep-dive, embark, forge, harness, leverage, utilize, curate, craft (as UI verb), discover, explore (as CTA), uncover, onboard (as a user-facing verb), spearhead, pioneer, champion, orchestrate, catalyze, amplify, boost, skyrocket, maximize, optimize (unless real performance work), synergize, ideate, galvanize, ignite, spark, fuel, drive (as "drive growth"), propel, turbocharge, level up, future-proof, democratize, operationalize, productize, incentivize, actualize, enable (as filler), facilitate, enhance, augment, bolster, cultivate, nurture, foster, embrace, unlock the power of, tap into, delight, wow, thrill
```

Use the literal action the user or system performs: Save, Post, Sign in, Sign out, Filter, Sort, Export, Import, Delete, Create, Add, Edit, Run, View, Open, Copy, Send, Download, Upload, Print, Pay, Approve, Reject, Assign, Search, Share, Archive, Restore.

| AI word | Use instead |
|---|---|
| unlock, unleash | get, open, turn on, or name the feature: "Export to Excel (Pro)" |
| empower, enable | lets, can: "Teachers can post grades" |
| elevate, enhance, augment, boost | improve, add, or the change: "adds barcode scanning" |
| supercharge, turbocharge, skyrocket | delete, or the number: "cuts checkout to 2 taps" |
| streamline | shorten, fewer steps, or the count: "4 steps instead of 9" |
| accelerate | speed up, or the time saved |
| revolutionize, transform, reimagine, reinvent, redefine | change, replace, rebuild |
| disrupt | delete |
| dive in, dive into, deep-dive | read, open, start, look at |
| embark | start, begin |
| forge | build, make |
| harness, leverage, utilize, tap into | use |
| curate | pick, choose, list |
| craft (UI verb) | write, make, build, create |
| discover, explore, uncover (as CTA) | View, Browse, See, Search, or the object: "View listings" |
| onboard (to users) | set up, sign up, add |
| spearhead, pioneer, champion | lead, start, run |
| orchestrate | run, schedule, coordinate |
| catalyze, galvanize, ignite, spark, fuel, propel | cause, start, or delete |
| amplify | increase, spread |
| maximize, optimize (non-technical) | improve, raise, or the number |
| synergize, ideate | work together, plan |
| foster, nurture, cultivate | build, support, grow, help |
| facilitate | help, run, host |
| embrace | use, adopt, accept |
| democratize | "makes X free", "makes X available to Y" |
| bolster | strengthen, add to |
| delight, wow, thrill | delete |
| level up | improve, upgrade, move to Level 2 |

## 01.6 Banned nouns

```
solution, solutions, ecosystem, landscape, realm, tapestry, testament, synergy, paradigm, paradigm shift, journey, experience (as a noun for anything), platform (for a small app), suite, hub, powerhouse, game-changer, cornerstone, bedrock, linchpin, backbone, beacon, catalyst, symphony, labyrinth, odyssey, treasure trove, plethora, myriad, multitude, array (non-technical), gamut, spectrum, arsenal, toolkit (for 2 tools), playbook, blueprint, roadmap (non-plan), framework (non-code), north star, magic, wizardry, secret sauce, one-stop shop, next level, peace of mind, empowerment, excellence, innovation, transformation, value proposition, value-add, thought leadership, mindshare, bandwidth (for time), learnings, key takeaways, insights (without data), actionable insights, best practices, pain points, deliverables, stakeholders (in user copy), touchpoints, space (as "in the X space"), world (as "in the world of X"), sphere, arena, frontier, era, age (as "in the age of AI"), revolution, movement, community (for a user list), family (for customers), tribe, hero, rockstar, ninja, wizard, guru
```

| AI word | Use instead |
|---|---|
| solution, solutions | the thing: app, system, form, tool, service, "inventory app" |
| ecosystem | "works with X, Y, Z" (list them) |
| landscape, realm, space, world, sphere, arena | delete: "in the payments space" becomes "for payments" |
| tapestry, symphony, mosaic | delete |
| testament | "shows", or delete the sentence |
| synergy | delete, or "X and Y share data" |
| paradigm, paradigm shift | approach, change |
| journey | process, steps, or the real name: "enrollment", "checkout" |
| experience ("shopping experience", "user experience" in UI copy) | the activity: shopping, checkout, sign-in |
| platform (single app) | app, site, system |
| suite, toolkit | list the tools |
| hub | page, list, "all X in one list" |
| powerhouse, game-changer | delete |
| cornerstone, bedrock, linchpin, backbone | base, main part, or delete |
| beacon, north star | goal, or delete |
| catalyst | cause, reason, or delete |
| labyrinth, odyssey | delete |
| treasure trove | collection, archive, list |
| plethora, myriad, multitude, array, gamut, spectrum | many, or the count: "42 templates" |
| arsenal | set, list |
| playbook, blueprint | guide, plan, steps |
| magic, wizardry, secret sauce | the mechanism: "auto-fills from last order" |
| peace of mind | the fact: "daily backups kept 30 days" |
| excellence, innovation, transformation | delete, or the result |
| value proposition, value-add | benefit, or the benefit itself |
| insights, actionable insights | report, chart, "sales by week" |
| best practices | rules, steps, "recommended settings" |
| pain points | problems, or name the problem |
| learnings, key takeaways | notes, findings, lessons |
| stakeholders (user-facing) | the group: parents, voters, staff, owners |
| touchpoints | pages, messages, visits |
| community, family, tribe (for customers) | users, members, customers, residents |
| hero, rockstar, ninja, wizard, guru | the role: admin, member, developer |
| era, age, revolution, frontier | delete |

## 01.7 Adverbs and intensifiers

```
seamlessly, effortlessly, truly, simply, just, really, very, extremely, incredibly, highly, deeply, super, totally, absolutely, completely, entirely, fully, utterly, literally, actually, basically, essentially, fundamentally, virtually, practically, genuinely, honestly, definitely, certainly, undoubtedly, unquestionably, clearly, obviously, of course, naturally, surely, significantly, substantially, dramatically, drastically, exponentially, massively, vastly, remarkably, exceptionally, profoundly, intimately, meticulously, carefully, thoughtfully, beautifully, perfectly, instantly, easily, quickly, rapidly, swiftly, smoothly, intuitively, dynamically, intelligently, smartly, magically, ultimately, arguably, notably, importantly, interestingly, crucially, increasingly, ever-, always (when not), never (when not)
```

| AI word | Use instead |
|---|---|
| seamlessly, effortlessly, smoothly | delete |
| truly, genuinely, honestly | delete |
| simply, just (as in "just click") | delete. "Simply click Save" becomes "Click Save". Keep "just" only for time: "just now". |
| really, very, extremely, super, highly | delete, or use a stronger plain word: "very large" becomes "large" or "3 GB" |
| incredibly, remarkably, exceptionally | delete |
| totally, absolutely, completely, entirely, fully, utterly | delete unless it is a fact: "fully refunded" is fine |
| literally, actually, basically, essentially, fundamentally | delete |
| virtually, practically | almost, or the number: "99% of orders" |
| definitely, certainly, undoubtedly, clearly, obviously, of course | delete |
| significantly, substantially, dramatically, drastically | the number: "from 9s to 2s" |
| exponentially | delete unless the curve is exponential |
| meticulously, carefully, thoughtfully | delete |
| instantly, quickly, rapidly, swiftly | the time, or delete |
| intelligently, smartly, dynamically, magically | say the rule: "sorted by due date" |
| easily | delete |
| ultimately | delete |
| arguably | delete, or make the argument |
| notably, importantly, interestingly, crucially | delete; state the fact |
| increasingly | "more each month", or the trend numbers |

## 01.8 LLM-signature words

These words appear in model output far more than in human writing. One of them in a paragraph is a warning. Two means rewrite the paragraph.

```
delve, delve into, underscore, underscores, pivotal, crucial, vital, paramount, foster, navigate, navigating, bustling, meticulous, meticulously, vibrant, intricate, intricacies, nuanced, nuance, multifaceted, interplay, realm, tapestry, testament, embark, showcase, showcasing, commendable, noteworthy, garner, bolster, holistic, invaluable, endeavor, endeavour, facilitate, utilize, leverage, robust, comprehensive, seamless, ever-evolving, ever-changing, ever-growing, dynamic, unwavering, resonate, resonates, align, alignment, elevate, enhance, empower, streamline, spearhead, harness, cultivate, illuminate, encompass, encompassing, beacon, cornerstone, synergy, paradigm, pinnacle, zenith, epitome, quintessential, hallmark, bespoke, profound, profoundly, captivating, enthralling, enigmatic, symphony, labyrinth, kaleidoscope, mosaic, myriad, plethora, whimsical, ethereal, breathtaking, awe-inspiring, nestled, boasts, boasting, stands as, serves as, acts as, is a testament to, plays a vital role, a key role, key (as adjective for everything), notable, remarkable, significant, groundbreaking, transformative, revolutionize, reimagine, redefine, game-changer, unlock, unleash, embrace, strive, striving, endeavor to, aim to, seek to, in the realm of, the world of, the landscape of, it is worth noting, moreover, furthermore, additionally
```

| AI word | Use instead |
|---|---|
| delve, delve into | look at, read, cover, check |
| underscore, underscores | shows, means |
| pivotal, crucial, vital, paramount | important, needed, required, or delete |
| foster | build, help, support |
| navigate (non-UI) | handle, deal with, get through, use |
| bustling | busy, or the number: "2,000 residents" |
| meticulous, meticulously | careful, checked, or delete |
| vibrant | active, bright, or delete |
| intricate, intricacies | complex, details |
| nuanced, nuance | detail, difference |
| multifaceted | has several parts; list them |
| interplay | how X and Y affect each other |
| showcase, showcasing | show, list |
| commendable, noteworthy, notable | good, or delete |
| garner | get, win |
| bolster | strengthen, add |
| endeavor, endeavour | try, work, project |
| utilize | use |
| ever-evolving, ever-changing | changing, or delete |
| unwavering | steady, or delete |
| resonate | matter to, fit |
| align, alignment | match, agree |
| illuminate | show, explain |
| encompass | include, cover |
| pinnacle, zenith, epitome, quintessential, hallmark | delete |
| profound, profoundly | large, deep, or delete |
| whimsical, ethereal, enigmatic, enthralling | delete |
| nestled (location copy) | "in", "at", "beside": "The school is on Rizal St., beside the plaza" |
| boasts, boasting | has |
| stands as, serves as, acts as | is |
| plays a vital/key role in | helps, runs, handles |
| strive, aim to, seek to, endeavor to | the verb itself: "We aim to reply" becomes "We reply within 1 day" |
| key (on every noun) | main, or delete |
| significant (non-statistical) | large, or the number |

## 01.9 Hedges and fillers

```
various, several, numerous, a variety of, a range of, a wide range of, a number of, a host of, a wealth of, a plethora of, different (as filler), certain, some (as filler), somewhat, fairly, quite, rather, relatively, perhaps, possibly, potentially, may help, can help, might, generally, typically, usually (when always), often (without data), in many cases, to some extent, in some ways, kind of, sort of, a bit, a little, overall, in general, in terms of, with regard to, with respect to, regarding, in order to, due to the fact that, at this point in time, at the end of the day, for all intents and purposes, needless to say
```

| AI word | Use instead |
|---|---|
| various, several, numerous, a variety of, a range of, a number of | the count or the list: "3 payment methods: GCash, Maya, cash" |
| a wide range of, a host of, a wealth of | the count |
| certain, some (filler) | name them, or delete |
| somewhat, fairly, quite, rather, relatively | delete |
| perhaps, possibly, potentially, might (in product copy) | state the condition: "if the file is over 10 MB" |
| can help, may help | say what it does: "sends a reminder 1 day before" |
| generally, typically, usually, often | the rule, or the exception stated plainly |
| in terms of, with regard to, regarding, with respect to | "for", "about", or restructure |
| in order to | to |
| due to the fact that | because |
| at this point in time | now |
| overall, in general | delete |
| kind of, sort of, a bit | delete |

## 01.10 Corporate and startup jargon

```
circle back, touch base, reach out (for "contact"), loop in, ping (in customer copy), sync up, deep dive, drill down (non-UI), low-hanging fruit, move the needle, boil the ocean, win-win, game plan, going forward, moving forward, at scale, best-of-breed, bleeding edge, mission-critical, core competency, value chain, go-to-market, growth hacking, disruption, pivot, unicorn, hockey stick, 10x (as adjective), rockstar team, hustle, grind, crush it, killer feature, secret weapon, ninja, guru, evangelist, thought leader, influencer (for staff), impactful, actionable, learnings, onboarding journey, customer journey, user journey (in UI copy), omnichannel, hyper-personalized, data-driven (without data), AI-driven, AI-first, cloud-native (as a selling point), digital transformation, digitalization (as hype), empowerment, capacity-building (without program), stakeholder engagement, whole-of-government approach (outside official text)
```

| AI word | Use instead |
|---|---|
| reach out, touch base, circle back, ping | contact, call, email, message, reply |
| loop in | add, copy (cc) |
| going forward, moving forward | from now on, from {date}, or delete |
| low-hanging fruit | easy fixes, first fixes |
| move the needle | change {metric} by {amount} |
| mission-critical | required; say what breaks without it |
| at scale | "for 10,000 users", or delete |
| impactful | the effect |
| actionable | say the action |
| data-driven, AI-driven, AI-first | say what the data or model does: "suggests reorder quantity from last 90 days of sales" |
| digital transformation, digitalization | the change: "Barangay clearance requests now online" |
| customer journey, user journey (UI) | steps, process, or the real name |
| 10x (adjective) | the measured ratio, or delete |
| hustle, grind, crush it | delete |
| killer feature, secret weapon | the feature name |
| omnichannel | list channels: "Facebook, SMS and email" |
| capacity-building, stakeholder engagement | the event: "training for 40 barangay health workers" |

## 01.11 Institutional hype words: schools, LGUs, government, clinics, churches

English hype that shows up on generated school, barangay, city and agency sites. Tagalog versions are in part 09. Mission and About copy is in part 05.

```
premier, prestigious, leading, top, renowned, esteemed, distinguished, illustrious, world-class, globally competitive, center of excellence (unless officially designated), holistic education, quality education, excellence, dedicated, committed, passionate, service-oriented, people-centered, citizen-centric, responsive governance, transparent governance, good governance (as slogan), progressive, dynamic leadership, visionary leader, honorable (as adjective), beloved, humble (for an official), selfless, tireless, heartfelt, warmest, utmost, fullest, unwavering commitment, noble, sacred, historic (without history), vibrant community, thriving community, bustling town, hidden gem, paradise, haven, oasis
```

| AI word | Use instead |
|---|---|
| premier, prestigious, renowned, esteemed, illustrious | a checkable fact: founding year, accreditation level, board exam passing rate with year and source |
| leading, top | ranking with source and year, or delete |
| globally competitive, world-class | delete |
| center of excellence | only when CHED or the agency designated it; cite the program and year |
| quality education, holistic education | the programs: "K to 12, STEM and ABM strands, SPED class" |
| dedicated, committed, passionate (staff) | what they do and when: "Office hours Mon to Fri, 8 AM to 5 PM" |
| service-oriented, people-centered, citizen-centric | the services list with requirements and fees |
| transparent governance | the documents: "Budget, SALN and bids posted under Transparency" |
| dynamic leadership, visionary leader | the official's name and position only |
| honorable (as praise) | use "Hon." only where the LGU's own style requires the title; no praise adjectives |
| tireless, selfless, beloved, humble | delete |
| utmost, fullest, warmest | delete |
| vibrant, thriving, bustling (community) | population, land area, main industries, with source |
| hidden gem, paradise, haven, oasis | the attraction name and how to get there |

## 01.12 Product and feature naming words

Words agents bolt onto feature names. ALL CAPS feature names are covered in part 02.

```
Smart, Intelligent, AI-powered, AI-enhanced, Auto-magic, Magic, Genie, Wizard (for a form), Assistant (for a filter), Copilot (for autocomplete), Pro (on free features), Ultra, Max, Plus (without a plan), Turbo, Hyper, Nexus, Nova, Quantum, Zen, Flow, Pulse, Spark, Sync (for a manual import), Hub, Center, Studio (for a settings page), Insights (for one chart), Engine, Core, Cloud (for local storage), 360, X (as suffix)
```

| AI word | Use instead |
|---|---|
| Smart Search, Intelligent Search | Search |
| AI-powered {feature} | say what the model does, or drop "AI" if no model is called |
| Magic Fill, Auto-magic | Auto-fill |
| Setup Wizard (for 3 fields) | Setup |
| Insights (one chart) | the chart name: "Sales by week" |
| Analytics Hub, Reports Center | Reports |
| Pulse, Nexus, Nova, Quantum, Zen (module names) | what the module holds: Inventory, Payroll, Enrollment |
| Studio (settings page) | Settings |
| Sync (manual import) | Import |
| Cloud Storage (local disk) | Files |
| Customer 360 | Customer profile |

## 01.13 Emotional and sensory words in product copy

```
love, fall in love, obsessed, excited, thrilled, delighted, happy to, proud to, passionate, joy, joyful, fun (for a form), exciting, peace of mind, stress-free, worry-free, carefree, feel, feeling, vibe, vibes, magic, spark joy, wow, oh-so, yay, woohoo, hooray, bliss, dream, dreamy, heaven, heavenly, cozy (non-hospitality), warm (non-hospitality)
```

| AI word | Use instead |
|---|---|
| love, fall in love, obsessed | delete |
| excited, thrilled, delighted, proud (announcement) | state the news: "Online payment is now available." |
| happy to (help) | delete: "Contact support" |
| stress-free, worry-free, carefree, peace of mind | the fact that removes the worry: "Refund within 7 days" |
| fun, joyful (utility app) | delete |
| vibe, vibes | delete |
| dream, dreamy, heaven | delete |

## 01.14 Words that are fine in their literal sense

Do not strip a word that carries a fact. Check the context before deleting.

| Word | Banned use | Allowed use |
|---|---|---|
| optimize | "Optimize your workflow" | "Optimized image sizes: 1.8 MB to 240 KB" |
| dynamic | "A dynamic experience" | "Dynamic import", "dynamic route" in code or docs |
| robust | "Robust platform" | "Robust standard errors" in statistics |
| real-time | Label on a polled dashboard | WebSocket or SSE push, documented |
| instant | "Instant results" (unmeasured) | "Instant transfer" when the provider states it, e.g. InstaPay |
| seamless | "Seamless integration" | never needed; use "works with" |
| scalable | "Infinitely scalable" | "Scales to 8 workers" with the config |
| navigate | "Navigate the complexities" | "Navigate to Settings" in UI help text |
| leverage | "Leverage our tools" | financial leverage in finance copy |
| experience | "Shopping experience" | "Work experience" field on a job form |
| platform | "Our platform" (for one app) | "Platform: Android 10+" in requirements |
| journey | "Your learning journey" | a travel site describing an actual trip |
| key | "Key features" | "API key", "primary key", "key" on a map legend |
| powerful | "Powerful dashboard" | never needed in UI copy |
| simple | "Simple. Powerful." | "Simple interest" in a loan calculator |
| community | "Join our community" (customer list) | a real forum or member group that exists |
| premium | "Premium experience" | "Premium" as the actual plan name, or insurance premium |
| unlimited | cap exists | no cap, checked in code |

## 01.15 Replacement method

Use this order on every flagged word.

| Step | Action | Example |
|---|---|---|
| 1 | Delete the word; reread | "a powerful reporting tool" becomes "a reporting tool" |
| 2 | If meaning was lost, replace with a number | "fast" becomes "loads in 1.2s" |
| 3 | If no number, replace with a name or list | "various payment options" becomes "GCash, Maya, card or cash" |
| 4 | If a verb, replace with the literal action | "unlock insights" becomes "view reports" |
| 5 | If nothing is left, delete the sentence | "Experience the future of learning." becomes (deleted) |

## 01.16 Check

- [ ] Search the diff for every word in 01.2 to 01.13; each hit is deleted or replaced.
- [ ] No adjective survives without a number, name or list behind it.
- [ ] No "seamless", "powerful", "robust", "intuitive", "cutting-edge" anywhere, including `alt`, `title`, `aria-label` and meta tags.
- [ ] No "solution", "ecosystem", "platform" (for one app), "journey", "experience" used as filler nouns.
- [ ] No "unlock", "unleash", "empower", "elevate", "supercharge", "streamline", "leverage", "utilize".
- [ ] Button and link verbs are literal actions (Save, Export, View). Details in part 03.
- [ ] No "simply", "just", "easily", "seamlessly", "effortlessly" in instructions.
- [ ] No "very", "really", "truly", "extremely", "incredibly".
- [ ] No LLM-signature words: delve, underscore, pivotal, crucial, foster, navigate (non-UI), bustling, meticulous, vibrant, tapestry, testament, realm, intricate, multifaceted, showcase.
- [ ] No "serves as", "stands as", "boasts", "nestled", "plays a vital role".
- [ ] "various", "several", "numerous", "a range of" replaced by a count or a list.
- [ ] "in order to" is "to"; "due to the fact that" is "because".
- [ ] Speed claims have a measured number or are removed.
- [ ] "Real-time" and "Live" only where push is implemented. See part 04.
- [ ] "Unlimited" only where the code has no cap.
- [ ] Security claims name the mechanism (TLS, bcrypt, 2FA), never "bank-grade".
- [ ] School, LGU and agency pages carry no "premier", "prestigious", "world-class", "globally competitive" without a cited source.
- [ ] Officials are listed by name and position, with no praise adjectives.
- [ ] Feature names are plain nouns: Search, Reports, Import. No Smart, Magic, Pulse, Nexus, 360.
- [ ] "AI-powered" appears only where a model is actually called.
- [ ] No emotional words in system copy: excited, thrilled, love, peace of mind.
- [ ] Words kept for literal meaning (API key, dynamic import, premium plan name) are checked against 01.14.
- [ ] Two or more flagged words in one paragraph means the paragraph is rewritten, not patched.
