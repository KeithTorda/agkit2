---
part: 09
title: Philippine audiences and local formats
covers: language, regional context, government, schools, elections, peso, phones, addresses, names, dates, privacy, payments, receipts
---

# 09 - Philippine audiences and local formats

Read when the brief establishes Philippine users, institutions, content, or locale. Do not infer nationality, preferred language, aesthetic, or required symbols merely from a path, name, or example.

## Language and tone

Use the user's requested language and the audience's natural register. English, Filipino, Taglish, Cebuano, Ilocano, and other regional languages are valid choices. Do not add slogans such as "Para sa bayan" or overly formal translated vocabulary just to signal locality; keep them when they genuinely fit the brand or institution.

Use consistent task terms in bilingual UI and offer language names in the switcher. Proper names and official labels may remain untranslated. Translate meaning and action rather than word-for-word structure. Set page and block `lang` values appropriately, and test long translations, accented letters, and natural line breaks.

## Names, addresses, and phones

- Preserve names as supplied, including spaces, suffixes, accents, and punctuation. Do not assume everybody has a middle name or a Western first/last structure.
- Use actual institution names, roles, contact information, and official identifiers. Never fabricate officeholders, school IDs, precincts, or accreditation.
- Build address fields around actual service coverage. Barangay, municipality/city, province, region, postal code, and landmarks are distinct concepts; not every address has the same hierarchy.
- Preserve leading zeros in IDs and phone display. Store identifiers as strings.
- Philippine mobile examples can use `09...` or `+63 9...`; normalize accepted input and validate with a maintained numbering approach rather than rejecting everything except one hand-written prefix list.
- International or landline users may need different formats. The product's real coverage should determine validation.

## Money and time

Use explicit currency such as PHP and an audience-appropriate peso display. For example, `Intl.NumberFormat('en-PH', { style: 'currency', currency: 'PHP' })` handles formatting; calculations need exact decimal or integer minor-unit handling. Distinguish estimated, pending, paid, refunded, and voided amounts. Show fees and recurring terms before commitment.

Use `Asia/Manila` for Philippine local times when the product calls for it. Keep UTC instants and date-only values distinct. Use unambiguous deadlines with time zone where relevant. Currency and date formatting should follow the selected locale, not hard-coded string slicing.

## Official, school, and election information

Design can be contemporary, traditional, colorful, or restrained according to the brief. Government and school projects do not automatically require seals, flag colors, official portraits, or a template layout. Use legitimate marks appropriately and do not imply official status for an unofficial tool.

Service pages should expose requirements, fees, hours, location, and the actual process. Schools need current admissions, programs, calendars, and contact details. Election information needs an authoritative source, date, and clear update cadence. Do not fabricate precinct results, polling places, filing deadlines, or voter records. Sensitive lookup tools need appropriate access control and must not expose private records by default.

## Payments, receipts, and personal data

Use real provider states for GCash, Maya, banks, and payment gateways. A screenshot or client callback is not proof of settled payment. Verify server-side status and webhook authenticity, handle retries idempotently, and avoid collecting account credentials.

Receipt fields, numbering, taxes, discounts, retention, accessibility duties, and privacy obligations depend on the actual business and current requirements. Verify them against current authoritative guidance and project requirements before implementing compliance claims. Do not turn a generic example into a universal BIR or legal rule.

Collect only needed personal data, restrict access, protect exports, redact logs, and use fictional data in public demos. Do not invent government IDs or display real sensitive records as sample content.

## Imagery and channels

Use local or client-specific imagery when it helps authenticity, but do not require a fixed number of photos or force a stereotyped "Filipino" look. Respect consent, rights, cultural context, and correct symbols. Test the actual priority devices and channels, including mobile and embedded browsers when the audience uses them.

## Review

Check natural language, exact names, actual service information, locale handling, source freshness, and sensitive-data boundaries. Ask for missing official content rather than inventing it.
