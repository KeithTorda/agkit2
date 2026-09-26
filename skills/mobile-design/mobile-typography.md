# Mobile Typography Reference

Type scale, system fonts, Dynamic Type, accessibility, and dark-mode text. Read for any text-heavy screen. Unreadable text is the fastest way to make an app feel broken.

## 1. What mobile changes

Phones are held closer than a monitor but on a smaller, narrower screen, in variable light, and the user controls the font size. So versus desktop: body text is larger (16px minimum, 14pt/14sp is the floor), lines are shorter (40-60 characters), line height is more generous (1.4-1.6), regular weight dominates, and sizing must respect the user's accessibility setting rather than being fixed.

## 2. System fonts

Prefer the system font unless the brand mandates a custom one: it is tuned for screens, supports Dynamic Type and wide languages for free, and adds no download.

- iOS: SF Pro Text (body, under 20 pt), SF Pro Display (20 pt and up), SF Pro Rounded, SF Mono. Optical sizing and dynamic tracking are automatic.
- Android: Roboto (plus Roboto Flex, Serif, Mono). Google Sans is licensed for Google products only.

Use a custom font when brand identity or an editorial style needs it. Then: include only the weights you use, subset for size, ship WOFF2, keep to 2-3 files, provide a system fallback, and test at every Dynamic Type size.

## 3. Type scale

Use the platform's built-in scale rather than inventing one; both map to Dynamic Type / font scaling.

### iOS (SF Pro, Dynamic Type styles)

| Style | Size | Weight | Line height |
|-------|------|--------|-------------|
| Large Title | 34 pt | Bold | 41 pt |
| Title 1 / 2 / 3 | 28 / 22 / 20 pt | Bold / Bold / Semibold | 34 / 28 / 25 pt |
| Headline / Body | 17 pt | Semibold / Regular | 22 pt |
| Callout / Subhead | 16 / 15 pt | Regular | 21 / 20 pt |
| Footnote | 13 pt | Regular | 18 pt |
| Caption 1 / 2 | 12 / 11 pt | Regular | 16 / 13 pt |

### Android (Material 3)

| Role | Size | Weight | Line height |
|------|------|--------|-------------|
| Display L / M / S | 57 / 45 / 36 sp | 400 | 64 / 52 / 44 sp |
| Headline L / M / S | 32 / 28 / 24 sp | 400 | 40 / 36 / 32 sp |
| Title L / M / S | 22 / 16 / 14 sp | 400 / 500 / 500 | 28 / 24 / 20 sp |
| Body L / M / S | 16 / 14 / 12 sp | 400 | 24 / 20 / 16 sp |
| Label L / M / S | 14 / 12 / 11 sp | 500 | 20 / 16 / 16 sp |

Custom scale (only when the brand needs it): a modular ratio from 16px base — 1.2 (compact), 1.25 (balanced, common), 1.333 (spacious). Keep to 5-7 sizes total.

## 4. Dynamic Type / text scaling (required)

The single most-skipped mobile requirement. Text must scale with the user's setting, and layouts must survive it.

```swift
Text("Hello").font(.body)                                 // scales with the setting
Text("Hello").font(.custom("MyFont", size: 17, relativeTo: .body))  // custom, still scales
```

Android: always use `sp` for text (scales), `dp` for everything else. Users scale from 85% to 200%, so 14sp can become 28dp. Test at 200%.

Large sizes break naive layouts: text overflows, buttons grow, icons look small. Fix with flexible (not fixed-height) containers, text wrapping, icons that scale with text, and scrollable containers for long text.

## 5. Accessibility

Minimum sizes: body 14, secondary 12, captions 11 (px/pt/sp) — nothing below 11. Buttons 14-16.

Contrast (WCAG): normal text 4.5:1 (AA), large text (18pt+, or 14pt+ bold) 3:1; aim for 7:1 outdoors. Verify the actual foreground/background pair rather than trusting that a colour "looks dark enough".

Spacing (WCAG 1.4.12): line height at least 1.5x for body paragraphs, paragraph spacing at least 2x font size, letter spacing at least 0.12x, word spacing at least 0.16x. Mobile body line height 1.4-1.6, headings 1.2-1.3, never below 1.2.

## 6. Dark-mode text

Dark text needs its own treatment, not an inversion. On a dark background, very high-contrast text (a bright, fully saturated white) can look harsh and "halate" (light bleeding into the dark), so text is usually a light grey rather than the brightest possible white — but let `DESIGN.md` and the measured contrast decide the exact value, not a fixed rule. Keep contrast at AA or better either way.

Because dark-mode text can appear thinner (halation), consider a slightly heavier body weight and a touch more letter spacing than in light mode, and check on a real OLED display. Use the platform's semantic text roles (`.label`/`.secondaryLabel` on iOS, `onSurface`/`onSurfaceVariant` on Android) so light and dark adapt together.

## 7. Common mistakes

- Fixed px font sizes that ignore the user's setting — use Dynamic Type / `sp`.
- Body text under 14 — unreadable at arm's length.
- Low-contrast "aesthetic" greys that vanish in sunlight — meet 4.5:1 and test outdoors.
- Lines longer than ~60 characters, or tighter than 1.4 line height — hard to track.
- Reusing a desktop scale on mobile, or shipping without testing the largest accessibility size.

## 8. Font loading

Custom fonts cost bytes and can block first paint: subset to the characters you use (15-40KB per weight vs 100-300KB full), prefer a variable font, cap at 2-3 files, and never block content on font load — show the system fallback and swap when the custom face is ready.
