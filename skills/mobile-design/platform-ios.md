# iOS Platform Guidelines

> Human Interface Guidelines essentials, iOS conventions, SF Pro typography, and native patterns. Read this when building for iPhone/iPad.

---

## 1. HIG philosophy

Clarity (legible text, precise icons, function-led design), deference (content fills the screen; UI never competes with it; translucency hints at more), and depth (distinct layers and transitions convey hierarchy). Values: aesthetic integrity, consistency through system controls, direct manipulation, clear feedback, familiar metaphors, and user control (the user initiates and can cancel).

## 1a. iOS 26 baseline (Liquid Glass)

iOS 26 introduced the Liquid Glass design language: a system-wide adaptive material for navigation bars, tab bars, sheets, sidebars, and controls that refracts the content behind it and adapts to light and dark surroundings.

- Use the standard system components (navigation bar, tab bar, toolbar, sheets, search); they adopt Liquid Glass automatically with correct behavior.
- Do not hand-build glass by stacking blur views under custom chrome; let the material come from native components, and keep any custom translucency subtle and legible in both themes.
- Respect Reduce Transparency and Increase Contrast: the system falls back to opaque surfaces, and custom UI should too.
- SwiftUI exposes it through the standard containers and the `glassEffect` modifiers on current SDKs; React Native and Flutter get it through the native navigation and tab components.
- Platform specifics shift between releases. If unsure whether a component or modifier is current, say so and verify against the current Human Interface Guidelines rather than guessing.

---

## 2. Typography

SF Pro Text (body, under 20 pt), SF Pro Display (20 pt and up), SF Pro Rounded, SF Mono, SF Compact. Use Dynamic Type styles, not fixed sizes.

| Style | Size | Weight |
|-------|------|--------|
| Large Title | 34 pt | Bold |
| Title 1 / 2 / 3 | 28 / 22 / 20 pt | Bold / Bold / Semibold |
| Headline | 17 pt | Semibold |
| Body / Callout | 17 / 16 pt | Regular |
| Subhead | 15 pt | Regular |
| Footnote | 13 pt | Regular |
| Caption 1 / 2 | 12 / 11 pt | Regular |

```swift
Text("Hello").font(.body)          // scales with the user's setting
// Custom font that still scales:
Text("Hello").font(.custom("MyFont", size: 17, relativeTo: .body))
```

Supporting Dynamic Type is required; test up to the accessibility sizes.

---

## 3. Color

Use semantic colors so dark mode adapts automatically: `.label`/`.secondaryLabel`/`.tertiaryLabel` for text, `.systemBackground`/`.secondarySystemBackground` for backgrounds, `.systemFill` family for shapes. System accent colors have light and dark variants (Blue #007AFF/#0A84FF, Green #34C759/#30D158, Red #FF3B30/#FF453A, and so on). Dark mode is not an inversion: use true or near-black backgrounds, desaturated colors, light-gray text, and glows instead of drop shadows.

---

## 4. Layout and spacing

Respect safe areas (status bar, home indicator, Dynamic Island); never place interactive content in unsafe areas. Standard horizontal margin 16 pt, card and list padding 16 pt, buttons at least 44 pt tall with 12 pt vertical / 16 pt horizontal padding. Space content in 8 pt multiples (4 pt for compact); iPad uses 20 pt+ margins and often multi-column layouts.

---

## 5. Navigation

Tab bar for 3-5 top-level sections (always visible, labeled, SF Symbols, active tint), navigation controller for hierarchical drill-down (system chevron back, centered title, max 2 right actions, optional large title that collapses on scroll), modal for focused tasks, sidebar on iPad. Modal styles: sheet (default, parent visible), full screen, popover (iPad), alert (critical), action sheet (choices). Gestures: edge-swipe from the left navigates back, pull-down dismisses a sheet, long press opens a context menu; never override edge-swipe-back without strong reason.

---

## 6. Components

Buttons come in tinted (primary), bordered (secondary), and plain (tertiary), at least 44 pt tall for primary CTAs. Lists use `.plain`, `.insetGrouped` (default since iOS 14), `.grouped`, or `.sidebar`, with disclosure, detail, checkmark, reorder, and delete accessories. Text fields are rounded rectangles, at least 36 pt tall, with a clear button. Segmented controls suit 2-5 equal-width options; use tabs for anything more complex. iOS 15+ sheets support `.medium` and `.large` detents plus custom heights with a grabber.

---

## 7. iOS-specific patterns

Use the native `UIRefreshControl` for pull-to-refresh. Swipe actions reveal destructive actions on left-swipe and constructive on right-swipe (full swipe triggers the first). Long press opens a context menu with an enlarged preview and related actions, destructive last and in red. Half-sheets use detents for progressive disclosure.

---

## 8. SF Symbols

Apple's icon library (5000+). Match symbol weight to text weight, choose a scale (`.small`/`.medium`/`.large`), prefer standard symbols users recognize, use multicolor only when meaningful, and check availability for older iOS.

```swift
Image(systemName: "star.fill").font(.title2).foregroundStyle(.yellow)
Image(systemName: "checkmark.circle").symbolEffect(.bounce)   // iOS 17+
```

---

## 9. Accessibility

Every interactive element needs a label, correct traits (button, link), and state; add hints where useful.

```swift
.accessibilityLabel("Play")
.accessibilityHint("Plays the selected track")
```

React Native uses `accessibilityLabel`, `accessibilityHint`, and `accessibilityRole`. Support Dynamic Type across all sizes (up to ~53 pt accessibility sizes) and honor Reduce Motion (`@Environment(\.accessibilityReduceMotion)`; React Native `AccessibilityInfo.isReduceMotionEnabled()`) with instant transitions.

---

## 10. Ship checklist

Per-screen and release checks live in the mobile-design SKILL.md checklist. iOS-specific items: SF Pro / SF Symbols; Dynamic Type tested at accessibility sizes; safe areas and Dynamic Island respected; edge-swipe back works everywhere; VoiceOver labels present; dark mode and Liquid Glass materials verified; native components used where one exists.

> iOS users carry strong expectations from other iOS apps. Deviating from HIG patterns feels broken; when in doubt, use the native component.
