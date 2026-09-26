---
name: i18n-localization
description: Internationalisation and localisation - translation keys and locale files, next-intl (Next.js 16) and react-i18next, Laravel lang files, ICU plurals, Intl date, number and peso formatting, Filipino/English bilingual sites, RTL with logical CSS, and the kit's hard-coded-string checker. Use when adding a language, building a bilingual Philippine site, reviewing UI text for hard-coded strings, or handling locale formatting.
version: 2.5.0
---

# i18n and Localisation

Two separate jobs: **localisation** (format dates, numbers and money correctly for the audience, even in a one-language site) and **internationalisation** (make text translatable). Every Philippine project needs the first; add the second when a second language is actually planned. When it is, set it up early: keyed strings, formatting through `Intl`, and layout that survives longer text. Retrofitting is the expensive path.

## Setup order (when adding languages)

1. **Pick the library:** next-intl for Next.js App Router (Server-Component-aware), react-i18next for Vite/SPA React, vue-i18n for Vue, Laravel's `lang/` files with `__()`, gettext or Babel for Python.
2. **Route and negotiate the locale** before extracting strings, so keys land in the right place.
3. **Extract** user-facing strings to keyed, feature-namespaced locale files.
4. **Route dates, numbers, money and plurals** through `Intl` / ICU, not string concatenation.
5. **Run the checker** (last section) and view each locale once at mobile width.

## Filipino and English (Philippine projects)

- **Language tags.** English: `en` (or `en-PH` when formatting matters). Filipino: `fil` (`fil-PH` for formatting). Set `<html lang="fil">` on Filipino pages and `lang="en"` on English ones; a Filipino passage inside an English page gets `<span lang="fil">`. Use `fil`, not `tl`, for new work (`tl` is the older Tagalog code; accept it as an alias if a library or browser sends it).
- **Money.** Format pesos with `Intl`, never by string-building `"₱" + amount`:
  ```ts
  const peso = new Intl.NumberFormat('en-PH', { style: 'currency', currency: 'PHP' })
  peso.format(1234.5)   // "₱1,234.50"
  ```
  Keep amounts as integer centavos or decimal strings in storage and convert only for display (`database-design`). For receipts and reports, fix the fraction digits explicitly (`minimumFractionDigits: 2`).
- **Dates and time.** Philippines is `Asia/Manila` (UTC+8, no daylight saving). Store UTC, display with `timeZone: 'Asia/Manila'`. Prefer unambiguous formats: `new Intl.DateTimeFormat('en-PH', { dateStyle: 'long', timeZone: 'Asia/Manila' })` gives "September 27, 2026"; `'fil-PH'` gives Filipino month names. Avoid numeric-only dates in public notices (09/10 reads differently to different readers).
- **Numbers.** Filipino and Philippine English both use `,` for thousands and `.` for decimals; still format through `Intl.NumberFormat` so the code works if another locale is added.
- **Which language where.** Follow the brief. Common patterns: government and school portals in English with Filipino versions of key public pages (announcements, how-to guides, forms); community pages (barangay) often Filipino-first. Keep one language per string: do not mix English and Filipino inside one label unless the brief asks for a Taglish voice. Proper nouns and official terms stay as written (Barangay, Sangguniang Kabataan, COMELEC, form names like CEF-1).
- **Translation quality.** Machine-translated Filipino reads stiffly; mark generated Filipino copy for review by a native speaker in the report, and prefer the common spoken term over a coined formal one when both exist (ask when unsure).
- **Plurals.** Filipino has its own CLDR plural rules; let ICU handle `{count, plural, ...}` with the `fil` locale instead of hand-rolled `count === 1` logic.
- **Names and addresses.** Forms commonly need first name, middle name (often the mother's maiden surname), last name and suffix (Jr., III) as separate fields; addresses as house/street, barangay, city or municipality, province, and a 4-digit ZIP code. Mobile numbers as `09XX XXX XXXX` for display, stored in E.164 (`+639XXXXXXXXX`).
- **Text length.** Filipino strings often run longer than English; size buttons and table headers for the longer version.

## Next.js App Router with next-intl

`useTranslations()` is a hook, so it runs in Client Components only. Server Components (the default) call the async `getTranslations()`. Using the hook in an async Server Component throws at render.

```tsx
// Server Component (default): async, no hook
import { getTranslations } from 'next-intl/server'
export default async function Page() {
  const t = await getTranslations('Home')
  return <h1>{t('title')}</h1>
}

// Client Component: the hook, inside 'use client'
'use client'
import { useTranslations } from 'next-intl'
export function Greeting({ name }: { name: string }) {
  const t = useTranslations('Home')
  return <p>{t('greeting', { name })}</p>   // en: "Hi {name}"  fil: "Kumusta, {name}"
}
```

Keep components server-first; use `useTranslations()` only in the interactive leaf that already needs `'use client'`. Format with next-intl's `getFormatter` (server) or `useFormatter` (client), which carry the request locale.

### Locale routing

Define locales once in `i18n/routing.ts`; the proxy and navigation helpers both read it. On Next.js 16 the request interceptor file is `proxy.ts` (it was `middleware.ts` before 16; follow next-intl's docs for the version in the project).

```ts
// i18n/routing.ts - single source of truth
import { defineRouting } from 'next-intl/routing'
export const routing = defineRouting({
  locales: ['en', 'fil'],
  defaultLocale: 'en',
  localePrefix: 'as-needed',   // no /en prefix for the default locale; Filipino at /fil/...
})

// proxy.ts - negotiates the request locale, redirects to app/[locale]/...
import createMiddleware from 'next-intl/middleware'
import { routing } from './i18n/routing'
export default createMiddleware(routing)
export const config = { matcher: ['/((?!api|_next|.*\\..*).*)'] }
```

next-intl negotiates `Accept-Language` for you. Set `<html lang>` (and `dir` if an RTL locale exists) in `app/[locale]/layout.tsx` from the active locale, and add `hreflang` alternates for each locale (`seo-fundamentals`).

## Laravel

Strings in `lang/en/*.php` and `lang/fil/*.php` (or `lang/fil.json` for key-by-sentence), read with `__('orders.created')` or `@lang`. Set the locale per request in a middleware from the URL segment, session or user setting (`App::setLocale`). Format money and dates for display with PHP's `NumberFormatter` (`intl` extension) and Carbon's `->locale('fil')->isoFormat(...)`, with `APP_TIMEZONE` or display conversion to `Asia/Manila`.

## Message keys

Namespace by feature or route, two to three levels deep. The key is a stable identifier, not the English sentence, so a copy edit does not rename the key in every locale file.

```
checkout.payment.cardDeclined     // stable id
"Your card was declined"          // avoid: the sentence becomes the key and breaks on reword
```

(Laravel's JSON sentence keys are an accepted exception when the project already uses them.)

## Plurals and select (ICU)

Plural categories differ by language (Arabic has six, Polish three, Filipino has its own rule), so `count === 1 ? a : b` is wrong outside English.

```
{count, plural, =0 {No items} one {# item} other {# items}}
{count, plural, =0 {Walang item} other {# item}}
```

## Dates, numbers, currency (Intl)

`Intl.DateTimeFormat`, `Intl.NumberFormat` (with `{ style: 'currency', currency }`), `Intl.RelativeTimeFormat` for "3 days ago", `Intl.ListFormat` for "A, B, and C", `Intl.PluralRules` if you build plural logic yourself. Each takes the active locale.

## Python (gettext / Babel)

```python
from gettext import gettext as _
print(_("Welcome to our app"))   # extract with Babel (pybabel extract); ngettext for plurals
```
Babel's `format_currency(1234.5, 'PHP', locale='en_PH')` and `format_date(..., locale='fil_PH')` cover formatting.

## Locale files

```
messages/            (next-intl)      lang/            (Laravel)
├── en.json                           ├── en/orders.php
└── fil.json                          └── fil/orders.php
```

Do: namespace by feature, configure a fallback locale, size containers for the longest translation (German and Finnish run about 30% longer than English; Filipino is often longer too). Avoid: concatenating translated fragments (word order differs by language), fixed-width text containers, translating identifiers or log messages.

## RTL

Only when an RTL language (Arabic, Hebrew, Persian, Urdu) is in scope. Author with CSS logical properties so one stylesheet serves both directions, and mirror only direction-carrying icons.

```css
.container { margin-inline-start: 1rem; padding-inline-end: 1rem; }  /* not left/right */
[dir="rtl"] .chevron { transform: scaleX(-1); }
```

Logical properties are a good default even without RTL; they cost nothing.

## Checklist (when multiple languages ship)

User-facing strings use keys; every locale file has the same key set; dates, numbers and money go through `Intl`; plurals use ICU; fallback locale configured; `lang` (and `dir` when needed) set on `<html>`; generated translations flagged for native review.

## Script (advisory)

`i18n_checker.py <project>` reads `locales/<lang>/<ns>.json`, `messages/<lang>.json` (next-intl) and `.po` files; Laravel `lang/` PHP arrays are not parsed. The base language is `en` when present, else the one with the most keys. Errors: invalid locale JSON, keys in the base language missing from another. Warnings: untranslated `.po` entries, likely hard-coded user-facing strings in files that do not use the i18n helper. Info: extra keys the base language lacks. Hard-coded string scanning runs only when an i18n setup is detected; `--strict` scans anyway. Flags: `--json`, `--verbose`, `--fail-on error|warning|never` (default `error`). Confirm each string is user-facing before extracting it.

```powershell
python "KIT/skills/i18n-localization/scripts/i18n_checker.py" .
```
