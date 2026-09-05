---
name: i18n-localization
description: Internationalisation and localisation for web and Python apps - translation keys and locale files, next-intl and react-i18next, ICU plurals, Intl date and number formatting, RTL layout with logical CSS properties, and the kit's hard-coded-string checker. Use when adding languages to an app, reviewing UI text for hard-coded strings, or handling locale-specific formatting and RTL.
version: 2.0.0
---

# i18n and Localisation

Make the app translatable before the second language arrives: keyed strings instead of literals, formatting through `Intl`, layout that survives right-to-left, and — on Next.js — the right translation API for the server/client boundary. Retrofitting these later is the expensive path.

## Setup order

1. **Pick the library:** next-intl for Next.js App Router (Server-Component-aware), react-i18next for Vite/SPA React, gettext for Python.
2. **Route and negotiate the locale** (below) — before extracting strings, so keys land in the right place.
3. **Extract** every user-facing string to a keyed, feature-namespaced locale file.
4. **Route all dates, numbers, and plurals** through `Intl` / ICU — never string concatenation.
5. **Run the checker** (§8) and, if any RTL locale is in scope, verify with `dir="rtl"`.

## Next.js App Router: server vs client (next-intl)

The mistake that bites: `useTranslations()` is a hook, so it runs only in Client Components. Server Components (the default) call the async `getTranslations()`. Reaching for the hook on the server throws at render.

```tsx
// Server Component (default): async, no hook
import { getTranslations } from 'next-intl/server';
export default async function Page() {
  const t = await getTranslations('Home');
  return <h1>{t('title')}</h1>;
}

// Client Component: the hook — requires 'use client'
'use client';
import { useTranslations } from 'next-intl';
export function Greeting({ name }: { name: string }) {
  const t = useTranslations('Home');
  return <p>{t('greeting', { name })}</p>;   // greeting: "Hi {name}"
}

// Wrong — the hook in a Server Component: throws at render
export default async function Page() {
  const t = useTranslations('Home');         // ✗ hooks can't run on the server
  return <h1>{t('title')}</h1>;
}
```

Keep components server-first; drop to `useTranslations()` only in the interactive leaf that already needs `'use client'`. Format dates/numbers with next-intl's `useFormatter` (client) or `getFormatter` (server), which carry the request locale for you.

## Locale routing and negotiation

Define locales once in `routing.ts` (next-intl v3+); middleware and the navigation helpers both read it.

```ts
// routing.ts — single source of truth
import { defineRouting } from 'next-intl/routing';
export const routing = defineRouting({
  locales: ['en', 'tr', 'ar'],
  defaultLocale: 'en',
  localePrefix: 'as-needed',   // no /en prefix for the default locale
});

// middleware.ts — negotiates the request locale, redirects to app/[locale]/...
import createMiddleware from 'next-intl/middleware';
import { routing } from './routing';
export default createMiddleware(routing);
export const config = { matcher: ['/((?!api|_next|.*\\..*).*)'] };
```

next-intl's middleware negotiates the `Accept-Language` header for you (via `@formatjs/intl-localematcher`). Call that package's `match(requestedLocales, supportedLocales, defaultLocale)` directly only when you negotiate outside next-intl — a custom middleware or a non-Next stack. Set `<html lang>` and `dir` in the locale layout from the active locale.

## Message keys

Namespace by feature or route, not by component; depth two to three. The key is a stable identifier, never the English sentence — so a copy edit does not rename the key across every locale file.

```
checkout.payment.cardDeclined     // ✓ stable id
"Your card was declined"          // ✗ becomes the key; breaks on reword
```

## Pluralization and gender (ICU)

Plural categories are language-specific (Arabic has six, Polish three), so `count === 1 ? a : b` is wrong outside English. Use ICU:

```
{count, plural, =0 {No items} one {# item} other {# items}}
{gender, select, female {She} male {He} other {They}} replied
```

## Dates, numbers, currency (Intl)

Never format by hand. `Intl.DateTimeFormat` and `Intl.NumberFormat` (with `{ style: 'currency', currency }`), `Intl.RelativeTimeFormat` for "3 days ago", `Intl.PluralRules` if you build your own plural logic — each takes the active locale. next-intl's formatters wrap these with the request locale.

## Python (gettext)

```python
from gettext import gettext as _
print(_("Welcome to our app"))   # extract with xgettext / Babel; ICU plurals via ngettext
```

## Locale files

```
locales/
├── en/  common.json  auth.json  errors.json
├── tr/  common.json  auth.json  errors.json
└── ar/  ...          # RTL
```

Do: namespace by feature, keep a fallback locale configured, size containers for the longest translation (German and Finnish run ~30 % longer than English). Avoid: hard-coded UI strings, concatenating translated fragments (word order differs by language), fixed-width text containers, and translating identifiers or log messages.

## RTL

Author with CSS logical properties so one stylesheet serves both directions; mirror only direction-carrying glyphs.

```css
.container { margin-inline-start: 1rem; padding-inline-end: 1rem; }  /* not left/right */
[dir="rtl"] .chevron { transform: scaleX(-1); }
```

## Checklist

All user-facing strings use keys; every supported locale file has the same key set; dates and numbers go through `Intl`; plurals use ICU; RTL tested with `dir="rtl"` when Arabic, Hebrew, Persian, or Urdu is supported; fallback locale configured; `lang` and `dir` set on `<html>`.

## Script (advisory)

`./scripts/i18n_checker.py <project>` compares key sets across locale JSON files (missing keys are high severity) and flags likely hard-coded UI strings in JSX, Vue, and Python files. It only enforces the hard-coded-string scan when it detects an i18n setup (locale files or `useTranslations`, `t()`, `gettext`, and similar); otherwise it prints a skip notice. Use `--strict` to scan anyway and `--json` for machine output. Findings are advisory; confirm each string is user-facing before extracting it.

```powershell
python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/skills/i18n-localization/scripts/i18n_checker.py .
```
