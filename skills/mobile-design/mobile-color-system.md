# Mobile color and surfaces

Use the accepted brand/direction and semantic roles. Mobile color must remain readable across actual content, display settings and lighting. Do not require a neutral brand, prohibit a purple accent, or add a second theme merely because the device supports it.

## Roles and themes

Define useful surface, foreground, emphasis, control, focus and status relationships. Pair task-critical color with text, shape or another cue. A brand hue can overlap a semantic hue if roles remain unambiguous; it does not require erasing the identity.

If the product supports light/dark themes, design their actual role mappings and preserve the preference mechanism. Dark palettes are not naive inversion, but do not universally need desaturation, gray text, no shadows or one near-black hex value. Check contrast and material hierarchy in the rendered states. Intentional mixed sections can belong to a single theme.

Use system semantic colors or dynamic color where the product chooses their behavior. Wallpaper-derived colors are optional, with suitable fallbacks and brand constraints. Verify the actual target/API/framework support rather than calling an imaginary shared helper such as `dynamicColorScheme()`.

## Display and lighting

OLED power consumption depends on pixel output, device/panel and brightness; do not repeat a universal ranking such as “blue cheapest”. Dark surfaces may reduce display power on OLED, while benefits and readability vary by device and use. True black, near black and other palettes have legitimate tradeoffs; test smear/halation or bright-light visibility when relevant rather than prescribing one value.

Contrast measurements help, but office screenshots do not establish outdoor readability. If the product is used outside or in low light, test representative conditions when possible. Preserve essential information over gradients, images and translucency using the actual backdrop/crop and an effective treatment; solid surfaces are an option, not an automatic design replacement.

## Accessibility and verification

For a WCAG-oriented target, normal text generally needs 4.5:1 and large text 3:1; meaningful non-text UI generally needs 3:1 against adjacent colors, with criterion-specific exceptions. Native platform requirements and actual supported settings also matter. Do not label every outline or disabled control as subject to the same rule.

Check relevant selected, disabled, error, focus and loading states, meaningful charts and required themes. Simulations can reveal color-only distinctions but do not establish full accessibility. Verify actual native screenshots/devices where available, including increased-contrast/reduced-transparency settings when supported. Record the checks and limits.
