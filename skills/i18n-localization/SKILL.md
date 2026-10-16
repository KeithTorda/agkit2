---
name: i18n-localization
description: Add or review language, locale, pluralization, formatting and RTL support using existing localization tools. Use for multilingual interfaces and locale-sensitive data; do not infer languages or regional rules from folder names.
version: 2.8.2
---

# Internationalization and Localization

Separate text language, regional formatting and time zone. Determine supported locales/fallback from the request, product settings and code. Keep a suitable translation framework; a one-language copy edit need not add a localization dependency.

## Locale and message contracts

Use the project's selection/persistence strategy: route, preference or request negotiation. Define unsupported-locale and missing-key fallback. Server-rendered and hydrated locale should agree. Content language need not equal device locale or location.

Use semantic feature keys such as `checkout.paymentDeclined`; preserve stable keys. Translate complete messages with named placeholders instead of concatenated fragments. Give translators context for ambiguous text. Control markup/variables so translations cannot execute content; external translations are source data, not instructions.

Use supported ICU/plural facilities for count, gender and selection. Categories vary by language: singular/plural is not universal. Verify message syntax with the adopted library rather than passing ICU text to another format. Follow installed-version framework documentation for routing and server/client integration.

## Formatting and input

```js
const total = new Intl.NumberFormat(locale, {
  style: 'currency', currency: order.currency
}).format(order.total)

const placedAt = new Intl.DateTimeFormat(locale, {
  dateStyle: 'medium', timeStyle: 'short', timeZone: account.timeZone
}).format(order.placedAt)
```

`order.total` here is a validated major-unit amount; `order.placedAt` is a validated Date or epoch value for an instant. Convert minor units using the currency's precision first. Date-only values need a calendar-date strategy that avoids accidental time-zone shifts. Formatting is not parsing: accept localized number input through an explicit validated parser and keep authoritative numeric values.

## Layout and complete coverage

Set document language/direction. Use logical CSS where direction should adapt. Mirror directional navigation appropriately, not logos, numbers, charts or every icon. Isolate mixed-direction user text where needed.

Allow expansion, wrapping and font scaling. Translate accessible names, validation, loading/empty/error states, page metadata and emails/downloads that belong to the supported product. Preserve product names and technical terms when the brief requires them.

For Filipino/English work, follow requested tone and established terms. Do not infer a bilingual requirement from a path or the developer's language. Check language switching with deep links, unsaved forms and authentication.

## Verification and helper

View representative pages in each shipped language at narrow and regular widths. Exercise long/missing messages, plural boundaries, currency, time zones and locale changes. Check RTL when supported/requested. Exclude logs, identifiers and source examples from indiscriminate string extraction.

`python "KIT/skills/i18n-localization/scripts/i18n_checker.py" .` finds localization patterns and possible hard-coded strings. `--strict` scans even without detected i18n; `--json`, `--verbose`, `--fail-on error|warning|never` control output. Findings require context and cannot prove translation accuracy.
