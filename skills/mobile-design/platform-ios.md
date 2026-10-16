# iPhone and iPad implementation guidance

Use the actual deployment target, SDK and chosen UI framework. Inspect current [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/) and official API documentation when a platform/version decision matters. Do not force the newest material, font, bar height or minimum OS onto an existing supported app.

## Native behavior with the agreed brand

Use supported navigation, controls and system presentations when they provide the required behavior. A distinctive custom interface can be valid if it preserves semantics, predictability and access. New system materials may require availability checks and older-target fallbacks; React Native/Flutter wrappers do not necessarily adopt every newest native capability automatically.

Respect safe areas and real window geometry, keyboard, rotation and iPad multitasking. Content can intentionally extend behind system chrome while controls and essential text maintain usable bounds. Do not hardcode a notch/top inset, universal 16 pt margin or a permanent tab-bar height.

## Text, materials and controls

Use semantic text styles or custom fonts tied to appropriate scaling behavior. Verify Dynamic Type, long labels, glyphs and actual font packaging. System symbols need availability/rights checks and a meaningful accessible name when interactive; a fixed symbol count soon becomes stale.

Semantic colors and system materials can adapt to appearance and contrast settings. Preserve the product's supported themes; custom palette/effects need actual contrast and reduced-transparency/increased-contrast handling where applicable. Do not replace a chosen shadow with glow or desaturate a brand by universal rule.

Touch areas around 44 pt are a useful common starting guideline, with actual current component/platform rules and exceptions. Make fields/actions resilient to larger text and the keyboard. Do not impose a fixed component height or action count solely from an old recipe.

## Navigation and accessibility

Preserve supported back/interactive-dismissal behavior and a usable cancel path. Choose stack, tabs, sidebar, sheet or popover from task and window rather than a fixed destination count. Unsaved work needs a deliberate preservation/confirmation model, not indiscriminate gesture disabling.

Provide correct labels, traits, values and reading order; avoid redundantly labeling every text-bearing control. Test VoiceOver, appropriate keyboard/switch paths, text size, motion/transparency settings and focus restoration when relevant. Native defaults help but do not prove the assembled screen is accessible.

## Verify

Build/run the actual iOS target when the environment permits. Exercise affected navigation, input, permission, media, deep-link or background behavior. Distinguish simulator checks from physical-device capabilities and distribution/signing checks. Report which target/device/settings were checked and what remains unavailable.
