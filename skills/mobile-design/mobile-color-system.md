# Mobile Color System Reference

OLED behaviour, dark mode, outdoor visibility, semantic colour, and colour accessibility. On mobile, colour is also battery and readability, not only aesthetics. `DESIGN.md` and the brief decide the palette; this file is the physics and the accessibility floor those choices have to clear. Hex values below are platform system colours, quoted as examples.

## 1. Why mobile colour differs

Phones use OLED often (each pixel emits its own light), are viewed in bright sun, run on a battery, and follow a system-wide light/dark setting. Priorities, in order: readability in variable light, battery on OLED, system dark/light integration, clear semantics (error/success/warning), then brand.

## 2. OLED and battery

On OLED a black pixel is off and draws no power, so darker UIs save battery; brighter and more saturated pixels cost more (blue is cheapest, red dearest). On LCD, dark mode saves nothing. This is why a dark theme matters on mobile beyond taste.

There is a real trade-off at the dark end, and `DESIGN.md` should pick the point on it:

- A true-black background (`#000000`) gives maximum battery saving and the deepest contrast, but can show "black smear" on scroll and can feel harsh. It fits OLED-focused media apps.
- A near-black background (around `#121212` on Android) keeps most of the saving, scrolls more smoothly, and is easier on the eyes. It is the common default.

Neither is banned. State which the design uses and why; raised surfaces sit a step lighter (`#1E1E1E`-`#2C2C2C`) to convey elevation.

## 3. Dark mode

Dark mode is a distinct palette, not an inversion of the light one. Inverting makes saturated colours glow and breaks semantic meaning and contrast.

Typical mapping (Material-style, as an example — take real values from `DESIGN.md`):

| Role | Light | Dark |
|------|-------|------|
| Background | `#FFFFFF` | `#121212` (true black for OLED media UIs) |
| Surface / raised | `#F5F5F5` / `#EEEEEE` | `#1E1E1E` / `#2C2C2C` |
| Primary | a mid tone | a lighter, desaturated tint |
| Text primary / secondary | `#212121` / `#757575` | a light grey / a mid grey |

Rules that hold regardless of palette: desaturate colours for dark mode, use lighter tints for emphasis, keep semantic meanings, convey elevation with a lighter surface overlay rather than shadows, and re-check every contrast pair — light-mode ratios do not carry over.

## 4. Outdoor visibility

Bright sun washes out low contrast, glare, and pale colours; users end up shading the screen. The fix is contrast, not brightness: meet WCAG AA (4.5:1 normal text, 3:1 large text and UI outlines), aim for 7:1 on anything critical, use solid colours rather than subtle gradients for important information, and test in a genuinely bright environment. A pale grey on white that passes in the office fails on the street.

## 5. Semantic colours

Keep error/success/warning/info consistent across the app and both themes, and never repurpose them for branding or decoration. Platform system values (examples):

| Semantic | iOS (light / dark) | Android (light / dark on container) |
|----------|--------------------|-------------------------------------|
| Error | `#FF3B30` / `#FF453A` | `#B3261E` / `#F2B8B5` |
| Success | `#34C759` / `#30D158` | `#4CAF50` |
| Warning | `#FF9500` | `#FFC107` |
| Info | `#007AFF` / `#0A84FF` | `#2196F3` |

Always pair a semantic colour with an icon or text so colourblind users get the meaning too.

## 6. Dynamic colour (Android, Material You)

Android 12+ derives primary/secondary/tertiary/surface roles from the user's wallpaper. Support it and provide a static scheme as fallback for older versions or when the user disables it.

```kotlin
MaterialTheme(colorScheme = dynamicColorScheme() ?: staticColorScheme())
```

React Native support is limited; use a library or ship a static scheme.

## 7. Colour accessibility

About 8% of men and 0.5% of women have some colour blindness (red, green, or blue weakness most commonly). So: never carry meaning in colour alone — add icons, patterns, or text; avoid distinguishing states only by red vs green; and simulate the common types during design. Verify contrast with the platform inspectors (Xcode Accessibility Inspector, Android Accessibility Scanner) and a real device in sunlight.

Contrast floor: AA (4.5:1 normal, 3:1 large and UI components) is the minimum; AAA (7:1 / 4.5:1) is the target on critical text.

## 8. Common mistakes

- Pale grey text on white — fails outdoors; meet 4.5:1.
- Reusing the light palette in dark mode — garish and low-contrast; build a real dark palette.
- Same saturation in dark mode — colours glow; desaturate.
- Colour as the only signal for a state — invisible to colourblind users; add an icon.
- Semantic colours used for brand — muddies meaning; keep brand neutral.
- Defaulting to a purple/violet accent with no brand reason — a generated-app tell; let `DESIGN.md` choose.
