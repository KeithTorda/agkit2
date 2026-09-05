# Android Platform Guidelines

> Material Design 3 essentials, Android conventions, Roboto typography, and native patterns. Read this when building for Android.

---

## 1. Material Design 3 philosophy

Material as metaphor (surfaces in 3D space, light and shadow for hierarchy, motion for continuity), adaptive design (one UI across form factors, dynamic color from the wallpaper), and accessible by default (large targets, clear hierarchy, semantic colors, motion that respects preferences).

## 1a. Android 16 baseline (Material 3 Expressive)

Android 16 ships Material 3 Expressive: a refresh of Material 3 with more expressive shapes, motion, typographic emphasis, and richer color roles, tuned from Google's usability research. It builds on Material 3, so existing Material 3 apps keep working.

- Build on the Material 3 components (`androidx.compose.material3` or the Material 3 views); adopt Expressive's new shape, motion, and color roles through updated components and tokens, not hard-coded values.
- Dynamic color (Material You) remains the default: derive the scheme from the wallpaper with a static fallback for older versions.
- Android 16 enforces edge-to-edge by default on the latest target SDK: draw behind the system bars and apply window insets so content is not clipped. Support predictive back (Android 14+) throughout.
- Keep motion purposeful; Expressive encourages more animation, but it must respect the system animation and reduce-motion settings.
- Platform specifics change between releases. If unsure whether a token, component, or API is current, say so and verify against the current Material Design guidance.

---

## 2. Typography

Roboto (with Roboto Flex, Serif, Mono) is the system family; Google Sans is licensed for Google products. Always use `sp` for text (scales with the user's font setting) and `dp` for everything else.

| Role | Size | Weight |
|------|------|--------|
| Display L / M / S | 57 / 45 / 36 sp | Regular |
| Headline L / M / S | 32 / 28 / 24 sp | Regular |
| Title L / M / S | 22 / 16 / 14 sp | Regular / Medium / Medium |
| Body L / M / S | 16 / 14 / 12 sp | Regular |
| Label L / M / S | 14 / 12 / 11 sp | Medium |

Weights: Regular (400) for body, Medium (500) for buttons and emphasis, Bold (700) sparingly. Test at 200 % font scale.

---

## 3. Color

Dynamic Color (Android 12+) derives primary, secondary, tertiary, surface, and on-colors from the wallpaper; provide a static scheme as a fallback. Use the semantic roles (`Surface`, `SurfaceVariant`, `OnSurface`, `Outline`, `Primary`, `OnPrimary`, `PrimaryContainer`, and their secondary/tertiary counterparts). Error roles: #B3261E / #F2B8B5 (light / dark on container). Dark theme: near-black `#121212` backgrounds per platform guidance (true black only for OLED-focused media UIs), lighter surface overlays with elevation, desaturated colors, and checked contrast.

---

## 4. Layout and spacing

8 dp baseline grid (4 dp half-step): 8 dp minimum, 16 dp standard, 24 dp section, 32 dp large; phone margins 16 dp, tablet 24 dp+. Window size classes drive layout: compact (< 600 dp) single column with bottom nav; medium (600-840 dp) two columns or a navigation rail; expanded (> 840 dp) multi-column with a navigation drawer. Canonical layouts: list-detail, feed, supporting pane.

---

## 5. Navigation

Bottom navigation for 3-5 top-level destinations, navigation rail for tablets and foldables, navigation drawer for many destinations, top app bar for context and actions. Bottom nav is 80 dp, 3-5 items, Material Symbols (24 dp), labels shown, pill indicator plus filled icon for active, badges for notifications. Top app bar comes in center-aligned, small, medium, and large (collapsing) variants with at most 3 icon actions plus an overflow menu. Android provides system back (button or gesture) with predictive back (Android 14+): pop the stack correctly, support the predictive animation, never hijack back, and confirm before discarding unsaved work.

---

## 6. Components

Buttons: filled (primary), tonal (secondary), outlined (tertiary), text (lowest), at least 48 dp touch target. FAB in standard (56 dp), small (40 dp), large (96 dp), and extended sizes, bottom-right 16 dp from edges. Cards: elevated, filled, or outlined, 12 dp corner radius, 16 dp padding. Text fields: filled or outlined, 56 dp tall, floating label, red error state. Chips: assist, filter, input, suggestion (32 dp, 8 dp radius).

---

## 7. Android-specific patterns

Snackbars sit above the navigation, last 4-10 s, carry one text action, and queue (never stack). Bottom sheets are standard or modal (with scrim), 28 dp top corners, optional drag handle. Dialogs are centered with a scrim and at most two right-aligned actions (destructive may go left). Pull-to-refresh uses the Material circular indicator. Every touchable element needs a ripple (black or white at ~12 % opacity); this is required for the Android feel.

---

## 8. Material Symbols

Google's icon library in outlined (default), rounded, and sharp styles, with variable axes FILL (0-1), weight (100-700), grade, and optical size (20/24/40/48). Sizes: 20 dp dense, 24 dp standard, 40-48 dp emphasis. Disabled icons at 38 % opacity; active state is filled plus an indicator.

---

## 9. Accessibility

Every interactive element needs a `contentDescription`, correct semantics, and state.

```kotlin
Modifier.semantics { contentDescription = "Play button"; role = Role.Button }
```

React Native uses `accessibilityLabel`, `accessibilityRole`, and `accessibilityState`. Touch targets at least 48x48 dp (add padding around smaller visuals) with 8 dp spacing. Support font scaling to 200 % with `sp` units and flexible heights, and honor reduce-motion (`Settings.Global.ANIMATOR_DURATION_SCALE`).

---

## 10. Ship checklist

Per-screen and release checks live in the mobile-design SKILL.md checklist. Android-specific items: Material 3 (Expressive) components; 48 dp touch targets with ripple feedback; Roboto or the Material type scale in sp; dynamic color with a static fallback; edge-to-edge with window insets; predictive back; TalkBack labels; tested across phone and tablet sizes and at 200 % font scale.

> Android users expect Material Design. Custom UI that ignores Material patterns feels foreign; use Material components as the foundation and customize thoughtfully.
