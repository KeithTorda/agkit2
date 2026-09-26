---
part: 09
title: Filipino Context
covers: language register, Tagalog and Taglish tells, machine translation, regional languages, bilingual UI, government and LGU sites, barangay sites, school sites, election sites, peso formatting, phone numbers, addresses, names and titles, dates and time, government ID numbers, GCash and Maya and bank transfer copy, BIR invoices and receipts, discounts, local photos and imagery, Philippine symbols
---

# 09 — Filipino Context

Read when: the client, users or content are in the Philippines. Any LGU, barangay, school, COMELEC-related, POS, store, clinic or cooperative project. Any screen with pesos, phone numbers, addresses, dates or Filipino text.

## 09.1 Language choice and register

Most Philippine business, school and government web UI is written in English. Filipino appears in public notices, social posts, community services and forms for the general public. Taglish is how people talk and chat, not how an LGU writes an ordinance. Pick the register from the audience, then hold it for the whole screen.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Sprinkling Filipino words into English UI for "local flavour" ("Welcome, Kabayan! Your dashboard is ready.") | Nobody writes system UI like this. It reads as a foreigner's idea of Filipino | Plain English UI. Use Filipino only where the whole screen or message is in Filipino |
| Full formal Tagalog UI for an internal admin or POS | Staff are trained on English terms (Save, Void, Refund, Inventory). Formal Tagalog slows them down | English for staff tools unless the client asks otherwise |
| Gen-Z Taglish ("Petmalu 'to, lodi!") on a government or school page | Wrong register for public service. Reads as a meme generator | Formal English or standard Filipino for public-facing government text |
| Deep formal Tagalog heading over casual Taglish body | Mixed register inside one block. A sign of stitched model output | One register per screen. If body is Taglish, heading is Taglish |
| Switching between "ikaw" and "kayo" in the same flow | Inconsistent politeness | Public service and older audiences: "kayo/inyo/ninyo". Peer apps for young users: "ikaw/mo" is fine. Pick one |
| "po" on every sentence ("Salamat po sa pagbisita po!") | Over-politeness that no human writes. A stock Filipino-AI tic | One "po" per sentence at most, only in Filipino text addressed to the public. None in button labels |
| No "po" at all in a Filipino notice from a barangay to residents | Reads curt for that audience | Use "po" in announcement body text where a clerk would say it aloud. Leave it out of labels and headings |
| English UI with one Filipino button ("Isumite") | Half-translated. Looks broken | Translate the whole screen or none of it |
| Tagalog for Visayas or Mindanao audiences by default | Many users there speak Cebuano, Hiligaynon, Waray and others first. Tagalog is not neutral for them | Ask the client. English is often the safer neutral default outside Luzon |
| Assuming Filipino = Tagalog in code (`lang="tl"` for Filipino UI) | Mislabels the language | See part 27 for `lang` values. `fil` for Filipino, `tl` only for Tagalog proper |

## 09.2 Forced Filipino flavour words

These words are real Filipino. The tell is using them as decoration, in UI chrome, or in places a Filipino writer would not.

```
Mabuhay!, Tara na!, Tara!, Sulit!, Sulit na sulit!, Kabayan, Ka-barangay (as greeting), Lodi, Petmalu, Werpa, Astig!, Galing!, Grabe!, Solid!, Ayos!, Salamat po!, Ingat!, Kain tayo!, Pinoy Pride, Proudly Pinoy, Tatak Pinoy (as slogan), Bayanihan (as feature name), Para sa Bayan, Para sa Masa, Serbisyong Totoo, Serbisyong Tapat, Juan (as persona), Juan's journey, Pinoy-made, Gawang Pinoy, Pang-masa, Bida, Bida ka!, Ikaw ang bida, Kapamilya, Kapuso, Kasambahay (as marketing noun), Suki (as loyalty tier), Chika, Keri, Push mo 'yan!
```

| AI word | Use instead |
|---|---|
| Mabuhay! (hero headline, login heading) | The page's actual title. "Sign in". "Municipality of San Isidro" |
| Tara na! (CTA) | The verb: "Mag-register", "Register", "Order" |
| Sulit! / Sulit na sulit! (price label) | The price and what it includes: "₱299 — 3 kg, delivered" |
| Kabayan (greeting to every user) | The user's name, or no greeting. See part 22 on dashboard greetings |
| Bayanihan (as a feature name, e.g. "Bayanihan Mode") | The function: "Shared list", "Volunteer sign-up" |
| Pinoy Pride / Proudly Pinoy badge | Delete. If the client is a Filipino maker, state the fact once in About: "Made in Marikina since 1998" |
| Serbisyong Totoo / Kapamilya / Kapuso | Delete. These are TV network slogans and names. Using them is borrowing a brand |
| Tatak Pinoy | Delete unless the client is enrolled in the government programme of that name and can show it |
| Juan / Juan's journey (persona in copy) | "Residents", "students", "customers", or "you" |
| Suki tier / Suki points | "Loyalty points", or the client's own programme name |
| Salamat po! 🙏 (toast) | "Na-save na." or "Saved." |
| Ingat! (sign-out message) | "Signed out." / "Naka-sign out ka na." |
| Grabe! / Galing! (success state) | State the result: "Nabayaran na ang ₱1,250." |

## 09.3 Machine-translated and "deep" Tagalog

Machine translation produces textbook Tagalog that no Filipino uses on a screen. Real Filipino UI keeps English tech words and adds Filipino affixes: i-save, i-click, mag-log in, i-upload, na-save, nag-expire.

| English UI | Machine or deep Tagalog (banned) | What Filipinos write |
|---|---|---|
| Sign in / Log in | Pumasok, Lumagda, Pumirma | Mag-sign in / Mag-log in |
| Sign out | Lumabas, Umalis | Mag-sign out / Mag-log out |
| Save | Iligtas, Itago | I-save |
| Submit | Ipasa (fine in forms), Isumite (formal) | I-submit / Ipasa |
| Cancel | Kanselahin, Ikansela | Cancel / Huwag ituloy |
| Delete | Burahin, Pawiin | I-delete / Burahin (both used) |
| Edit | Baguhin, Iwasto | I-edit |
| Upload | Magkarga, Ikarga | I-upload |
| Download | Ibaba, Magbaba | I-download |
| Search | Paghahanap, Hanapin (as a label) | Search / Maghanap |
| Home | Tahanan, Bahay | Home |
| Settings | Mga Kagustuhan, Mga Setting (inconsistent) | Settings |
| Password | Lihim na salita, Hudyat | Password |
| Username | Pangalan ng gumagamit | Username |
| Email | Sulatroniko, E-liham | Email |
| Website | Pook-sapot, Sapot-pook | Website |
| Computer | Kompyuter (spelled as proof of "Filipino"), Kalkulador | Computer |
| Click here | Pindutin dito, Pumindot dito | I-click ito / Pindutin (for tap on mobile) |
| Loading | Naglo-load… (fine), Kinakarga (textbook) | Naglo-load… |
| Error | Kamalian, Pagkakamali | Error / May problema |
| Page not found | Hindi natagpuan ang pahina | Walang ganitong page. / Page not found. |
| Account | Kuwenta, Talaan | Account |
| Contact us | Makipag-ugnayan sa amin (acceptable, formal), Pakikipag-ugnayan | Contact / Makipag-ugnayan (formal notices only) |
| Terms of service | Mga Tadhana ng Paglilingkod | Terms of Service (keep English, legal docs are in English) |
| Required | Kinakailangan (long), Sapilitan | Required / Kailangan |
| Optional | Opsyonal (fine), Hindi sapilitan | Optional / Opsyonal |

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Invented purist words (salumpuwit, salipawpaw, salungpuwit, pook-sapot, sipnayan in a math app) | Internet jokes or academic coinages. No real user reads these | The English loanword with Filipino affix |
| Literal idiom translation ("Break a leg" → "Bali ang binti") | Machine output. Meaning is lost | Rewrite the idea in plain Filipino or skip it |
| English word order kept in Filipino ("Ang iyong account ay na-save na") | "ay" inversion everywhere sounds like a textbook | Predicate-first: "Na-save na ang account mo." |
| Every sentence uses "ay" ("Ang bayad ay natanggap na. Ang resibo ay ipapadala.") | Formal inversion stacked. A strong MT tell | "Natanggap na ang bayad. Ipapadala ang resibo sa email mo." |
| Mixed spelling of the same affix ("i-save", "isave", "i save") | No consistency pass | Hyphen before English roots: i-save, mag-upload, na-verify. Pick it and grep for the rest |
| Hyphen misuse on native roots ("i-bigay", "mag-bayad") | Hyphen belongs before a loanword or vowel-initial root, not native consonant roots | ibigay, magbayad, mag-ayos (vowel), i-print (loanword) |
| "ng" vs "nang" wrong ("Magbayad ng mabilis") | Common machine and learner error | "nang" for manner and "when": "Magbayad nang maaga". "ng" for object and possession: "Magbayad ng ₱500" |
| "din/rin", "daw/raw" never alternating | Phonetic rule ignored | "rin/raw" after vowels and w/y: "Ako rin", "Siya raw". "din/daw" after consonants: "Bayad din", "Tapos daw" |
| Filipino copy with English capitalisation ("Mag-Sign In Na Ngayon") | Title case does not exist in Filipino UI | Sentence case: "Mag-sign in" |
| Translating brand and product names ("Pera-G" for GCash, "Tindahan ng Laro" for Play Store) | Wrong and unrecognisable | Keep names as the brand writes them |

## 09.4 Regional languages

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Ilocano, Cebuano, Hiligaynon, Kapampangan, Bikol or Waray text generated without a native reviewer | Model output in these languages is weak. Errors are obvious to every local reader | Ship regional-language text only after a native speaker from the client signs off. Otherwise English or Filipino |
| Regional greeting as hero decoration ("Naimbag nga aldaw!", "Maayong adlaw!") | Decoration, not communication | The page title. Put a greeting only in a message the client wrote |
| Language picker with 8 Philippine languages where 7 are empty or machine-translated | Fake coverage | List only languages with complete, reviewed strings |
| Mixing Cebuano and Tagalog in one string ("Salamat kaayo po") | Model blending | One language per string |
| Regional text without a `lang` attribute | Screen readers read it with the wrong voice | See part 27. `lang="ilo"`, `lang="ceb"`, `lang="hil"`, `lang="pam"`, `lang="bik"`, `lang="war"` on the element |

## 09.5 Bilingual UI rules

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Language switcher with flags (PH flag for Filipino, US or UK flag for English) | Flags are countries, not languages. English is an official language of the Philippines | Text switcher: "English · Filipino". Current language marked with `aria-current="true"` |
| Every label doubled ("Name / Pangalan", "Submit / Ipasa") on an ordinary app | Doubles reading load | One language per UI. Doubling is fine on printed or official forms where the client's paper form already does it |
| Doubled labels where the two lines disagree | Translation drift | Keep both strings in one translation file, keyed together. Review in pairs |
| Filipino strings dropped into buttons sized for English | Filipino is often longer. Buttons clip or wrap | Test every button and tab with the Filipino string. No fixed widths on buttons |
| Date and number format changed with the language | Confuses users who switch | Same ₱, date and phone format in both languages |
| Legal pages "translated" by model (Privacy Notice, Terms) | Legal meaning changes | Keep the lawyer-approved text. Add a Filipino summary only if the client provides it |
| Language toggle that reloads to the homepage | Loses place | Switch in place, keep the same route and form state |
| Auto-detecting language from IP and forcing it | Everyone in PH gets Filipino, including users who want English | Default to the client's choice. Remember the user's pick |
| Mixed-language error messages ("Invalid input. Pakisubukan ulit.") | Two sources glued together | Fully translated message set per language |

## 09.6 Taglish and Filipino microcopy

| Context | AI (banned) | Use |
|---|---|---|
| Save success | "Yay! Na-save na! 🎉" | "Na-save na." |
| Save error | "Oops! May mali po! 😅 Sorry po!" | "Hindi na-save. Subukan ulit." |
| Empty list | "Wala pang laman dito, bes! ✨" | "Wala pang record." |
| Empty search | "Hala! Walang nahanap 🔍" | "Walang resulta para sa 'Santos'." |
| Login heading | "Maligayang pagbabalik, Kabayan!" | "Mag-sign in" |
| Wrong password | "Mali po ang password niyo, pakiulit po!" | "Mali ang password." |
| Session expired | "Naku! Nag-expire na session mo! 😢" | "Nag-expire ang session. Mag-sign in ulit." |
| Delete confirm | "Sigurado ka ba talaga? Wala nang balikan! 😱" | "Burahin ang record na ito? Hindi na ito maibabalik." |
| Payment received | "Ayos! Bayad ka na! 💸" | "Natanggap ang ₱1,250. Ref. no. 1234 5678 9012." |
| Payment pending | "Chill lang, pino-process pa! ⏳" | "Hinihintay pa ang kumpirmasyon ng bayad." |
| Loading | "Sandali lang po, inihahanda namin! ✨" | "Naglo-load…" |
| Offline | "Walang signal, lods! 📶" | "Walang internet. Susubukan ulit kapag may koneksyon." |
| Form required | "Kailangan po ito, pakisagot po!" | "Kailangan ito." |
| Order placed | "Salamat sa order, suki! 🛒" | "Na-order na. Order no. 10234." |
| Appointment set | "Game na! Kita-kits sa Lunes! 👋" | "Naka-schedule: Lunes, 5 Okt, 9:00 AM, Barangay Hall." |
| Account created | "Welcome sa pamilya! 🇵🇭" | "Nagawa na ang account." |
| Upload done | "Ayan na, na-upload na! 🙌" | "Na-upload na ang file." |
| Copied | "Kinopya na! 📋" | "Na-copy." |
| Signed out | "Ingat ka palagi! 💙" | "Naka-sign out ka na." |

## 09.7 Government, LGU and barangay sites

Government sites in the Philippines have conventions users recognise: the GOVPH top bar and footer from the Government Website Template, the Philippine Standard Time clock, the Transparency Seal page, the Citizen's Charter, the FOI link, the Data Privacy notice. Missing these reads as an amateur site. Faking them is worse.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Hero: "Welcome to the Official Website of the Premier Municipality of X — Your Gateway to Progress!" | Hype on a public service page | "Municipality of X, Province of Y". Then the top tasks: permits, clearances, hotlines, announcements |
| AI-generated or redrawn seal | The seal is set by ordinance. A redrawn seal is a fake government mark | Use the seal file the LGU provides. If none yet, a plain text wordmark and a TODO in the handoff. Never generate a seal |
| Seal used as a large faded watermark behind content | Decoration of an official mark | Seal once, in the header, at 40–64px height |
| "Hon. Juan Dela Cruz, Municipal Mayor" left as a placeholder at ship | Obvious filler with a real title | Real names from the client, or block the release. Grep for "Juan Dela Cruz", "Hon. ", "Lorem" before ship |
| Invented officials list (Vice Mayor, 8 councilors, all with stock headshots) | Fake people with public titles | Only the roster the client sends, with their photos. No photos → names and positions only |
| Official's photo and name on every banner, every page, every announcement | Many LGUs follow anti-epal policies. It also reads as a campaign site | Office names in content ("Office of the Municipal Mayor"). Official's photo on the Officials page only, unless the client insists in writing |
| "Mayor's Message" filled with generated inspirational text | Putting words in a real official's mouth | Leave the section out until the office supplies the text |
| Invented vision, mission and core values | Every LGU and school has an adopted text | Ask for the adopted text. Do not write one |
| Invented hotline numbers | People will call them in emergencies | Only numbers from the client. National lines that are real: 911 (emergency), 8888 (citizens' complaints). Mark any unconfirmed number as a ship blocker |
| "Smart City", "Digital Transformation Journey", "e-Governance Hub" as hero copy | Buzzwords, no task | Name the service: "Apply for a business permit", "Request a barangay clearance" |
| No Citizen's Charter | Required posting under the Ease of Doing Business Act (RA 11032). Users look for it | A Citizen's Charter page per office: service, requirements, steps, fees, processing time, person responsible |
| Fake "Transparency Seal" badge that links nowhere | The seal is tied to real required disclosures | Only if the client has the content: budget, plans, procurement, reports. The badge links to that page |
| No privacy notice on forms that collect personal data | Data Privacy Act (RA 10173) applies to LGUs | A privacy notice link beside every form submit, naming the office and purpose. Name the Data Protection Officer contact the client gives |
| Fake "ISO 9001:2015 Certified" badge | Certification is a real claim | Show it only if the client provides the certificate details |
| "Latest News" filled with generated articles and stock photos | Fake public records | Empty state "No announcements yet." until real posts exist. See part 04 |
| Carousel of five hero images of the town plaza | Slow on mobile data, hides content | One photo or none. Top tasks and hotlines above the fold |
| Weather widget, clock, visitor counter, Facebook page embed stacked in a sidebar | 2010 portal clutter, heavy scripts | Philippine Standard Time line in the top bar if the template calls for it. Link to the Facebook page. No embeds |
| "Barangay Portal" with login required to read announcements | Public info behind a wall | Announcements, hotlines, office hours, requirements public. Login only for requests and tracking |
| Clearance and certificate request form asking for 30 fields | Asks for data the office does not use | Fields from the client's paper form. No extra fields. See part 17 |
| Services listed as icon cards ("🏥 Health", "📜 Permits") | Emoji icons, card grid | Plain list of services with one-line descriptions and the office responsible |
| Using the national government's GOVPH wordmark on a private site | Impersonation | GOVPH bar only on sites the government office actually owns and runs |
| Punong Barangay labelled "Barangay Captain" in official copy | "Kapitan" is how people talk. The legal title is Punong Barangay | "Punong Barangay" in official lists; "Kapitan" only in informal social posts if the client uses it |
| Barangay council listed as "Board Members" | Wrong body | "Sangguniang Barangay Members (Kagawad)". SK: "SK Chairperson", "SK Kagawad" |
| Municipal council called "City Council" for a municipality | Wrong LGU type | Municipality: Sangguniang Bayan. City: Sangguniang Panlungsod. Province: Sangguniang Panlalawigan |
| Hours "24/7 Online Services!" when requests are processed by a clerk | Overclaim | "Requests are processed Monday to Friday, 8:00 AM–5:00 PM." |

## 09.8 School sites

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "Welcome to the Home of Champions!" / "Where Excellence Begins!" | Stock school hype | School name, location, and the three things visitors come for: enrollment, calendar, contact |
| Invented vision, mission, core values, hymn lyrics | Every school has adopted texts; public schools follow DepEd's | Ask for the texts. For DepEd public schools, use the DepEd vision, mission and core values the school supplies |
| "Enroll Now!" button | Vague, urgent | "Enrollment for SY 2026–2027: 2 June–13 June". Link: "Enrollment requirements" |
| School year written inconsistently (2026-27, SY26, S.Y 2026/2027) | No format decided | One format: "SY 2026–2027" (en dash). Semester: "1st Semester, SY 2026–2027" |
| Stock photos of American campuses, lockers, yellow school buses | Wrong country | Photos from the school. No photos → no hero image |
| Photos of identifiable students without consent notes | Minors, Data Privacy Act | Only photos the school confirms it has consent for. Group shots from behind or events the school cleared |
| Fake achievements ("#1 School in the Region", "98% Board Passing Rate") | Invented numbers | Only results the school provides, with year and source: "2025 LET passing rate: 86% (PRC)" |
| Faculty page with generated names and AI headshots | Fake people | Real roster or leave the page out |
| Grades UI with A–F letters for a K–12 school | Wrong system | Numeric grades. K–12 passing mark is 75. Use the school's scale and descriptors |
| LRN field accepting any length | Learner Reference Number is 12 digits | `inputmode="numeric"`, 12 digits, spaces allowed on input, stripped on save |
| "Student Portal" with gamified badges and XP | Gamification nobody asked for | Grades, schedule, balance, announcements. See part 22 |
| Tuition shown in $ or without the peso sign | Template leftover | ₱ with centavos on statements: "₱18,500.00". See 09.10 |
| Class suspension notice as a hero carousel slide | Urgent info buried in a slider | Site-wide banner with date, levels affected and source: "No classes, all levels, Wed 7 Oct 2026. Source: Municipal Mayor's Office advisory." |

## 09.9 Election and COMELEC-related sites

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Using the COMELEC seal or name as if the site is COMELEC's | Impersonation of an election body | Unless the client is COMELEC, name the real owner in the header and add: "This site is not operated by COMELEC." Link to comelec.gov.ph for official data |
| "Official Precinct Finder" on a third-party site | False authority | "Precinct lookup (based on COMELEC's published list, updated 3 Mar 2026)" |
| "Live Election Results" | Results come in batches; the standard wording is well known | "Partial and unofficial results, as of 9:40 PM, 12 May 2025, 78.4% of precincts reporting" with the data source |
| Generated candidate photos, bios or platforms | Putting words and faces on real candidates | Only official candidate list data. No photos unless the client has rights to them |
| Colour-coded candidate bars in party colours chosen by the model | Implies affiliation | Neutral colour for all candidates. See part 12 |
| Precinct finder asking for full name, birthday, address, mother's maiden name | Over-collection of voter data | The minimum the lookup needs. Show only precinct no., clustered precinct, voting centre, and address |
| Countdown timer "Election in 23:14:05:09!" with glow | Hype on civic info | "Election day: Monday, 8 May 2028. Polls open 7:00 AM–7:00 PM." |
| Map pins for every precinct generated from guesses | Wrong locations send voters to the wrong school | Pins only from verified coordinates. Otherwise address text and "Get directions" link |
| Terms "voter's ID" for current voters | COMELEC stopped issuing voter's IDs | "Voter's certification" or the term the client uses |

## 09.10 Peso and money formatting

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `$` on prices for a PH client | Template leftover | `₱`. Currency code PHP in data and APIs |
| "P1,500" or "P 1,500" with a Latin P | ASCII fallback from before the sign was common | `₱1,500`. HTML `&#8369;` or the literal ₱ (U+20B1) |
| "Php 1,500", "PHP₱1,500", "₱ 1,500 PHP" | Mixed forms, doubled currency | UI: `₱1,500.00`, no space. Formal documents and exports: `PHP 1,500.00` is acceptable. One form per surface |
| `1.500,00` or `1 500,00` | European format | Comma thousands, period decimals: `₱1,500.00` |
| Centavos shown in some places, hidden in others | No rule | Money in transactions, invoices, balances: always 2 decimals. Marketing prices: whole pesos if all prices are whole (`₱499/month`) |
| Hand-written formatting (`"₱" + n.toFixed(2)`) | No thousands separators, breaks on negatives | `new Intl.NumberFormat('en-PH', { style: 'currency', currency: 'PHP' }).format(n)` gives `₱1,500.00` |
| Negative amounts as `₱-500.00` | Sign in the wrong place | `−₱500.00` in UI; `(₱500.00)` in accounting reports if the client's accountant uses it |
| Font without a ₱ glyph (falls back to a different font mid-number) | Visible font swap in prices | Check the chosen font covers U+20B1. If not, set a fallback in the stack that does. See part 13 |
| Float maths for money in JS (`0.1 + 0.2`) | Wrong centavos on receipts | Store centavos as integers or use a decimal type. See part 32 |
| "₱1.5K" on invoices | Abbreviation where exact amount is needed | Exact amount on documents. Abbreviate (`₱1.2M`) only on dashboard tiles, with exact value on hover or in the table |
| Price with no VAT statement on B2B quotes | Buyer cannot tell | "₱11,200.00 (VAT inclusive)" or "₱10,000.00 + 12% VAT". Pick what the client's BIR registration requires |
| Amount in words generated wrongly ("One Thousand Five Hundred Peso's") | Checks and vouchers need exact words | "One thousand five hundred pesos and 00/100" using a tested number-to-words function |
| "Free!" in a POS | Hype on a till | "₱0.00" in totals, "Free item" as the line description |
| Tipping UI copied from US apps (15% / 18% / 20%) | Not a PH norm in most contexts | Leave out unless the client asks |

## 09.11 Phone numbers

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Placeholder `(555) 123-4567` or `+1` default | US template | Example in helper text: `0917 123 4567`. No placeholder that looks like a real number |
| `09123456789` shipped in the footer or contact page | Placeholder that looks real and belongs to someone | Real number from the client. Grep for `09XX`, `0912345`, `0917 123` before ship |
| Input rejects spaces or dashes | Users type `0917-123-4567` | Accept `0917 123 4567`, `0917-123-4567`, `+63 917 123 4567`, `639171234567`. Normalise on save to `+639171234567` |
| Input forces `+63` and then users type `+63 0917…` | Double prefix | If showing a `+63` prefix, strip a leading 0 from what the user types |
| Validating network by prefix (Globe vs Smart vs DITO) | Prefixes move with number portability | Validate length and the leading 9 only |
| Display mixes formats (`+639171234567`, `0917 123 4567`, `(0917)1234567`) | No display rule | Display local format for PH users: `0917 123 4567`. Store E.164 |
| Landline written as `8123-4567` with no area code | Ambiguous outside Metro Manila | `(02) 8123 4567` for Metro Manila. Provinces: `(034) 432 1234`. Area code in parentheses |
| Landline input that only allows 7 digits | Metro Manila numbers are 8 digits | Allow the area code plus 7 or 8 digits |
| `tel:` links missing on mobile | Users on phones cannot tap to call | `<a href="tel:+639171234567">0917 123 4567</a>`. Hotlines: `<a href="tel:911">911</a>` |
| Viber, WhatsApp buttons added by default | Many PH businesses use Messenger and SMS instead | Only channels the client actually monitors. Often a Facebook Messenger link and a mobile number |
| SMS OTP copy "Your OTP is 123456. Don't share it with anyone! 🔐" | Emoji, exclamation | "123456 is your verification code for {Site}. Do not share it. Expires in 5 minutes." See part 08 |
| Phone field `type="number"` | Drops leading zero, shows spinners | `type="tel" inputmode="tel" autocomplete="tel"`. See part 17 |

## 09.12 Addresses

Philippine addresses go from small to large: unit or house number, street, subdivision or village, purok/sitio/zone, barangay, city or municipality, province, ZIP code. Region is useful for routing. NCR cities have no province.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| US fields: Address line 1, Address line 2, City, State, ZIP (5 digits) | Template form | House/Unit no. and street · Subdivision/Village (optional) · Barangay · City/Municipality · Province · ZIP code (4 digits) |
| "State" or "County" label | Wrong country | Province. Region only if the client needs it |
| Barangay as free text | Misspellings break reports and routing | Cascading selects from the PSA's Philippine Standard Geographic Code (PSGC): Region → Province → City/Municipality → Barangay |
| Province select required for Manila, Quezon City, Makati | NCR cities are not under a province | Province optional or auto-set "Metro Manila (NCR)" when an NCR city is chosen |
| Barangay select for Manila showing names only | Many Manila, Caloocan and Pasay barangays are numbered and grouped by zone | Show number and zone: "Barangay 649, Zone 68". Search by number |
| No Purok/Sitio/Zone field for rural or barangay-level forms | Barangay offices use purok to locate residents | "Purok/Sitio/Zone" field on barangay and LGU forms |
| No landmark field on delivery forms | Street numbers are missing in many areas | "Landmark (optional)" with helper: "Example: near the chapel, blue gate" |
| ZIP validation for 5 digits | PH ZIP codes are 4 digits | `pattern="\d{4}"`, `inputmode="numeric"` |
| Sample address using a real person's house or a real office | Privacy, confusion | "Unit 4B, 12 Mabini St., Brgy. San Roque, Antipolo City, Rizal 1870"-style sample with no real occupant, marked as an example |
| Address autocomplete from a foreign provider that returns "Manila, PH" for every town | Wrong data | Use PSGC data locally. Map picker optional, not required |
| "Brgy." "Bgy." "Barangay" mixed in one list | No style rule | "Brgy." in compact tables, "Barangay" in headings and documents |
| Sorting barangays by ID instead of name | Hard to find | Alphabetical, numbered barangays by number |

## 09.13 Names and titles

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Single "Full name" field on government, school or HR forms | Offices file by surname and need the middle name | Last name · First name · Middle name · Suffix. Order matches the client's paper form |
| Middle name required | Some people have none (foundlings, some foreign nationals, some Muslim Filipinos) | Middle name optional, with a "No middle name" checkbox if the office needs an explicit answer |
| No suffix field | Jr., Sr., II, III are common and legally part of the name | Suffix select: none, Jr., Sr., II, III, IV, V. Free text allowed |
| Name validation rejects spaces, periods or ñ | Blocks "Dela Cruz", "De los Santos", "Ma. Cristina", "Peñaflorida", "Muñoz" | Allow letters with diacritics, spaces, hyphens, periods and apostrophes. Test with `Ñ` and `ñ` |
| Surname particles capitalised by a formatter ("De La Cruz" → "De La Cruz", "dela cruz" → "Dela cruz") | Auto title-case breaks names | Store and show the name as typed. Uppercase only on printed forms that already use caps |
| "Ma." expanded to "Maria" automatically | "Ma." is the registered form for many people | Keep as typed |
| Sample names: John Doe, Jane Smith | Foreign template | Juan Dela Cruz and Maria Clara are the accepted sample names on PH forms. Use them only as labelled examples, never in live data or testimonials |
| Honorifics in UI greetings ("Hi, Ate Joy!", "Kuya, your order is ready") | Family terms from a system feel fake | The user's first name, or no greeting |
| Titles invented or wrong ("Hon." for a barangay secretary, "Engr." added to everyone) | "Hon." is for elected officials. Professional titles need a licence | Titles only as the client provides: Hon., Atty., Engr., Dr., Arch., Kgd. (Kagawad) |
| Title stacking ("Hon. Atty. Dr. Juan Dela Cruz, MD, LLB, PhD") | Parody of formal lists | Use what the office uses on its own letterhead |
| Gender field with only Male/Female on non-legal forms | May not be needed at all | Ask only if the office uses it. Legal forms follow the PSA birth certificate field ("Sex") |
| Civil status field missing on government forms, or present on a shop checkout | Wrong for both | Government and HR: Single, Married, Widowed, Legally separated, Annulled. Shops: leave it out |

## 09.14 Dates, time and calendars

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `05/06/2026` shown with no label | Many PH forms use MM/DD/YYYY, others use DD/MM/YYYY. Readers guess | Display with a month name: "6 May 2026" or "May 6, 2026". Pick one style per project |
| Typed date input with no format hint | Users do not know the order | Label: "Date of birth (MM/DD/YYYY)" matching the client's paper form. Or three fields: Month (select), Day, Year |
| Birthdate using a date picker that starts at today | Scrolling back 40 years | Three fields or typed input. See part 17 |
| ISO dates (`2026-05-06`) in user-facing tables | Machine format | Keep ISO in data and exports. UI: "6 May 2026" |
| "PST" for Philippine time | PST also means Pacific Standard Time | "PHT" or "Philippine Standard Time (UTC+8)" |
| Times computed in the server's zone (UTC) and shown raw | Off by 8 hours | Store UTC, render in `Asia/Manila`. PH has no daylight saving time |
| 24-hour time on public-facing pages | Most PH readers use 12-hour | "9:00 AM", "5:30 PM". 24-hour is fine in logs and staff tools if the client prefers |
| "a.m.", "am", "AM", "A.M." mixed | No rule | One form. "AM/PM" is the common PH form |
| Hardcoded holiday list | Holidays change each year by proclamation, and regional and local holidays exist | Holidays come from an admin-editable table. Label type: Regular holiday, Special non-working day, Local holiday |
| Office hours "Mon–Fri 9–6" copied from a template | LGU offices usually run 8:00 AM–5:00 PM | Ask. Write in full on public pages: "Monday to Friday, 8:00 AM–5:00 PM, except holidays" |
| Filipino dates with English month names in a Filipino UI ("ika-6 ng May") | Half-translated | Filipino months: Enero, Pebrero, Marso, Abril, Mayo, Hunyo, Hulyo, Agosto, Setyembre, Oktubre, Nobyembre, Disyembre. "Ika-6 ng Mayo 2026" in formal text; "6 Mayo 2026" in tables |
| Filipino weekdays missing | Same problem | Lunes, Martes, Miyerkules, Huwebes, Biyernes, Sabado, Linggo |
| Relative time in Filipino machine-translated ("2 minuto ang lumipas nakaraan") | Broken grammar | "2 minuto na ang nakalipas" or "kanina" for under an hour, "kahapon" for yesterday. See part 04 for when to use relative time |
| Fiscal year assumed April–March | Foreign default | Government fiscal year is the calendar year. Ask private clients |
| School year treated as calendar year | Wrong grouping in reports | Group school data by SY. Ask the client for the SY start month; it has shifted over the years |
| Week starting Sunday in business reports without asking | Mixed practice | Ask. Show the start day in report headers: "Week of Mon 5 Oct" |

## 09.15 Government ID numbers and personal data

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "SSN" or "Social Security Number" field | US template | Name the actual ID: TIN, SSS no., PhilHealth no. (PIN), Pag-IBIG MID no., PhilSys number, UMID, LRN, PRC licence no. Ask only for the ones the process needs |
| One generic "Government ID number" text field with no type | Cannot be validated or used | ID type select + number field. Format hint per type from the client's rules |
| Strict regex for an ID format guessed by the model | Blocks valid IDs | Length and digit checks only where the client confirms the format. Accept spaces and dashes, strip on save |
| Collecting every ID "just in case" | Over-collection under the Data Privacy Act | Collect the minimum. State why beside the field: "Needed for your barangay clearance record" |
| Showing full ID numbers in tables and receipts | Exposure | Mask: "TIN •••-•••-123-000". Full number only on the record page, to roles that need it |
| Uploading ID photos with no stated retention | Privacy risk | Privacy notice says who sees it and how long it is kept. Store outside the public web root |
| Consent checkbox pre-ticked | Not valid consent | Unticked. Plain text: "I agree to the processing of my personal data for this request. Privacy notice." |
| "We value your privacy" banner with no notice behind it | Empty claim | Link to the actual Privacy Notice with the controller name, purpose, retention and DPO contact from the client |
| TIN field without branch code on business forms | Invoices and registrations use TIN plus branch code | TIN and branch code as shown on the client's BIR certificate |

## 09.16 GCash, Maya, banks and payments copy

Many PH small businesses, schools and barangays take payment by GCash, Maya or bank transfer and verify by hand. The copy must say which kind of flow it is.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "Pay instantly with GCash!" when payment is a QR image and a clerk checks screenshots | Overclaim | "Pay by GCash, then upload your receipt. We confirm payments within 1 working day." |
| Redrawn or generated GCash, Maya, InstaPay or QR Ph logos | Brand misuse; also looks off | Official brand assets from the provider or payment gateway kit, at the size their guidelines give. Text label if no asset is supplied |
| "PayMaya" | Old name | "Maya" |
| "G-Cash", "Gcash", "GCASH" | Wrong casing | "GCash" |
| Personal GCash number and full name posted on a public page | Exposes a private person; invites scams | Business or merchant account. If the client insists on a personal account, show masked name ("JU** DE** CR**") as the app shows it, and the number only on the payment step |
| No field for the reference number | Staff cannot match payments | "GCash reference no." field, digits only, with helper: "Found at the bottom of your GCash receipt" |
| "Send proof of payment via DM" | Payment proof scattered across Messenger | Upload field on the order page, one screenshot, JPG or PNG, max 5 MB |
| Amount field left for the user to type | Mismatched amounts | Show the exact amount to send: "Send exactly ₱1,250.00". Copy button beside it |
| Payment status "Success!" right after upload | Nothing is verified yet | Statuses: "Awaiting payment" → "Payment submitted, for verification" → "Paid" or "Payment not found: check the reference no." |
| Gateway flow copy "Redirecting you to our secure partner… 🔒" | Vague, emoji | "You will be sent to GCash to approve ₱1,250.00. Come back to this page after." |
| Bank transfer with no method named | InstaPay and PESONet settle differently | "InstaPay: usually arrives within minutes, per-transfer limit set by your bank. PESONet: arrives the same or next banking day." |
| Bank details as an image | Cannot be copied; unreadable on small screens | Text with copy buttons: Bank, Account name, Account no. |
| Card payment as the first or only option for a PH consumer site | Many users do not use cards online | Order from the client's data. Common mix: GCash, Maya, bank transfer/InstaPay, over-the-counter (7-Eleven, Bayad, Cebuana Lhuillier, M Lhuillier, Palawan Express), Cash on delivery |
| COD offered with no fee or area rule | Staff get surprised | "Cash on delivery: Metro Manila only, +₱50" or whatever the client sets |
| "Refund processed!" with no timeline | Users wait with no information | "Refund of ₱1,250.00 sent to your GCash 0917 •••• 567 on 6 Oct 2026. Ref. no. …" |
| Fee hidden until the last step | Feels like a trick | Show the convenience fee on the method choice: "GCash (+₱15.00)" |
| "Load" and "e-wallet" used interchangeably | Load means mobile prepaid credit | "GCash balance" or "e-wallet". "Load" only for prepaid airtime |

## 09.17 BIR invoices, receipts and POS text

Philippine sales documents follow BIR rules. Under the Ease of Paying Taxes Act (RA 11976), the sales invoice is the primary document for both goods and services; the official receipt became a supplementary document. The client's accountant and BIR registration decide the exact wording. The agent never invents registration numbers.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "OFFICIAL RECEIPT" printed by a system that is not BIR-registered | A tax document claim the system cannot make | "Order summary" or "Acknowledgment receipt" until the client confirms registration. Then the exact title their registration allows, usually "SALES INVOICE" |
| "This serves as your official receipt" on an email order confirmation | False | "This is an order confirmation, not a BIR invoice." Or attach the actual invoice |
| Invented Acknowledgment Certificate / PTU / ATP numbers, serial ranges or TINs | Fake tax registration data | Placeholders in the template (`{{BIR_AC_NO}}`, `{{TIN}}`) and a ship check that fails if any placeholder is unfilled |
| Invoice header missing registered name, "VAT Reg. TIN" or "Non-VAT Reg. TIN", branch code, and registered address | Required fields | Seller block: registered name, business style, address, VAT/Non-VAT Reg. TIN with branch code, exactly as on the Certificate of Registration |
| VAT shown as one total with no breakdown | VAT invoices need the split | Lines: VATable Sales · VAT-Exempt Sales · Zero-Rated Sales · VAT (12%) · Total Amount Due |
| Non-VAT seller showing a VAT line | Wrong registration type | No VAT line. The document title and TIN label say "Non-VAT Reg." |
| Buyer name, address and TIN fields missing for business customers | Needed for input tax claims | Buyer block: Sold to, Address, TIN, Business style. Required when the client's accountant says so |
| Senior Citizen / PWD discount as a generic "Promo 20%" | These are statutory discounts with records required | Line: "SC discount (20%)" or "PWD discount (20%)", VAT-exempt handling as the accountant sets, plus fields for ID no., name and signature on file |
| Solo Parent discount missing where the client sells covered goods | Statutory discount | Add when the client says it applies, with ID no. captured |
| Receipt footer "Thank you for shopping with us! We appreciate your business! 🙏✨" | Emoji and filler on a tax document | "Thank you. Come again." or the client's one line. Plus the supplier/accreditation lines the registration requires |
| Voided sale deleted from the database | Audit trail lost | Void keeps the record with reason, user and time. POS shows "VOID" on reprints |
| Reprint looks identical to the original | Duplicates can be claimed twice | "REPRINT" or "DUPLICATE" marked on reprinted documents |
| Z-reading and X-reading called "Daily Summary" and "Report" | Cashiers and auditors know the real names | "X-reading" (shift) and "Z-reading" (end of day) with the fields the client's registration requires |
| Receipt width designed for A4 | POS printers are 58 mm or 80 mm | Receipt template at 58 mm or 80 mm width, monospace or narrow font, tested on the client's printer |
| LGU fees printed on a generic receipt template | LGUs issue their own accountable forms | For LGU collections, match the treasurer's form (for example Accountable Form No. 51). Do not design a replacement official receipt |
| "Tax" as a label | Unspecific | "VAT (12%)" or "Percentage tax" per registration |

## 09.18 Photos, imagery and national symbols

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Western stock photos (snowy streets, suburban houses, Caucasian office teams) | Wrong country | Client photos: the store, the barangay hall, the school building, real events. No photos → no photo |
| AI-generated "Filipino" faces | Fake people; often off in skin, clothing, setting | Real photos with consent. Otherwise illustrations of objects, not people, or nothing |
| Generic "Asian" stock standing in for Filipinos | Wrong and noticeable | Same: real photos or none |
| Jeepney, nipa hut, rice terraces, carabao, sari-sari store on every PH site | Tourist clichés as decoration | Use them only if the content is about them. A dental clinic in Cebu needs the clinic, not Banaue |
| Philippine flag as a background, wave animation, gradient or festoon | Decoration of the flag; restricted uses under RA 8491 | Do not use the flag as decoration. If the client needs it, show it flat, correctly oriented, in its official colours, at a normal size |
| Flag drawn with red on top | Upside-down flag signals a state of war | Blue field on top in peacetime. Check any flag image |
| Sun and three stars used as a logo motif for a private business | Borrowing national symbols | Client's own mark |
| Baybayin script as decorative texture | Script used as ornament, often misspelled | Use Baybayin only for real text a reader approved |
| Christmas banner with snowflakes and snowmen | Imported imagery | If the client wants seasonal art: parol lanterns, belen, simbang gabi, supplied by their designer |
| Map of the Philippines missing islands or with wrong borders | Visible error to every local | Use an official or verified map asset. Or no map |
| Stock hospital, school or police images for LGU services | Fake depiction of real offices | Photos of the actual office, or icons and text |
| Photos of barangay officials in a hero carousel | Personality over service | See 09.7 |

## 09.19 Local channels and habits

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Footer with X/Twitter, Instagram, TikTok, LinkedIn, YouTube, Discord icons for a barangay | Accounts do not exist | The channels the client runs. For LGUs and schools this is usually the Facebook page |
| "Join our Discord community" on a local business site | Wrong channel | Facebook page or Messenger link if that is where the client answers |
| Newsletter signup on an LGU site | Nobody runs it | Leave out. Announcements page and Facebook page link |
| "Chat with us 24/7" widget on a site staffed 8–5 | False promise | "Message us on Facebook. We reply Monday to Friday, 8:00 AM–5:00 PM." |
| App-store badges for an app that does not exist | Template leftover | Remove |
| Pages that need fast broadband (autoplay video, 5 MB hero) | Many users are on prepaid mobile data | See part 15 and part 34. Keep first load light |
| "Download our PDF" as the only format for requirements | Hard to read on phones | Requirements as an HTML list on the page, with the PDF as an extra link with its file size: "Download form (PDF, 240 KB)" |

## 09.20 Check

- [ ] One language and one register per screen. No Filipino words sprinkled into English UI.
- [ ] No "Mabuhay!", "Tara na!", "Sulit!", "Kabayan", "Lodi" or network slogans in UI chrome.
- [ ] Filipino copy uses English tech loanwords with affixes (i-save, mag-log in), not textbook words (pook-sapot, lumagda).
- [ ] No "ay" inversion in every sentence. "ng/nang" and "din/rin" checked.
- [ ] At most one "po" per sentence; none in labels or buttons.
- [ ] Regional-language text approved by a native speaker, or not shipped.
- [ ] Language switcher uses text, not flags. Switching keeps the route and form state.
- [ ] Every button tested with the Filipino string length.
- [ ] No generated or redrawn seals. Seal comes from the client file.
- [ ] No placeholder officials ("Hon. Juan Dela Cruz"), vision, mission, core values, or Mayor's message.
- [ ] No invented hotline numbers. Unconfirmed numbers block release.
- [ ] Government site has Citizen's Charter, Privacy Notice, and Transparency pages if the client provides the content.
- [ ] Correct titles: Punong Barangay, Sangguniang Bayan/Panlungsod/Panlalawigan, SK Chairperson.
- [ ] Third-party election sites say they are not operated by COMELEC and use "partial and unofficial" wording for counts.
- [ ] School year written as "SY 2026–2027" everywhere.
- [ ] No student photos without the school's consent confirmation.
- [ ] Money shown as `₱1,500.00` via `Intl.NumberFormat('en-PH', { style: 'currency', currency: 'PHP' })`. No `$`, no "P1,500".
- [ ] Font renders ₱ without falling back mid-number.
- [ ] Money stored as integer centavos or a decimal type.
- [ ] Phone input accepts 09XX, +63 and spaces; stored as E.164; displayed as `0917 123 4567`.
- [ ] Landlines include area code in parentheses.
- [ ] No `09123456789` or other placeholder numbers in shipped pages.
- [ ] Address uses Barangay, City/Municipality, Province, 4-digit ZIP. PSGC-based selects. NCR cities need no province.
- [ ] Purok/Sitio/Zone on barangay forms; Landmark on delivery forms.
- [ ] Name fields: last, first, middle (optional), suffix. Accept ñ, spaces, periods.
- [ ] Dates shown with month names. Typed date inputs state the format.
- [ ] Times rendered in Asia/Manila, 12-hour with AM/PM, labelled PHT or UTC+8 if a zone is shown.
- [ ] Holidays come from an editable table.
- [ ] Only needed government IDs collected; IDs masked in lists.
- [ ] Consent checkbox unticked and linked to a real privacy notice.
- [ ] GCash/Maya copy states whether payment is automatic or verified by staff.
- [ ] Reference number field and exact amount with copy button on manual payment flows.
- [ ] "GCash" and "Maya" spelled correctly; logos from official kits only.
- [ ] No "OFFICIAL RECEIPT" or "SALES INVOICE" unless the client confirms BIR registration for that system.
- [ ] No invented TIN, AC, PTU or ATP numbers. Placeholder check fails the build.
- [ ] VAT breakdown lines present on VAT invoices; none on Non-VAT.
- [ ] SC and PWD discounts are named lines with ID capture, not promos.
- [ ] Voids kept, reprints marked, X/Z-reading named correctly.
- [ ] Receipt template tested at 58 mm or 80 mm on the client's printer.
- [ ] No Western stock photos, no AI-generated Filipino faces, no tourist clichés as decoration.
- [ ] Philippine flag not used as decoration; blue on top.
- [ ] Only social channels the client actually runs.
