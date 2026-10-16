# Android implementation guidance

Inspect actual minimum/target SDK, supported devices, UI framework and build environment. Use current [Android developer guidance](https://developer.android.com/design) and [Material guidance](https://m3.material.io/) when a version-specific API or convention matters. An Android OS version does not automatically require a particular newest Material library or brand aesthetic.

## Adaptive layout and system behavior

Respect real window insets, navigation/status bars, keyboard and current edge-to-edge requirements for the target. Test configuration changes, process recreation and relevant phone/tablet/foldable sizes. Window size classes can guide adaptation, but the product's content decides how panes, rail, drawer or bottom navigation fit.

System back may first dismiss a keyboard/modal or navigate through a task; support the actual router and predictive-back API compatibility where applicable. Avoid a universal “always pop one screen” handler or blocking users to preserve a visual transition.

## Controls, brand and appearance

Use compatible native/Compose/Material primitives where useful, with their actual semantics and state behavior. Custom UI is valid when understandable and accessible; not every app needs wallpaper-derived dynamic colors, a ripple on every element, or the same rounded card geometry. Preserve the agreed brand and requested/existing theme scope.

Semantic color roles help coordinated themes. Check foreground/background and status/focus states rather than copying historical system hex values. Dynamic color can be an optional supported feature with static fallbacks, not a forced replacement of identity.

Use scalable text APIs (`sp` where appropriate) and density-aware layout; inspect the framework's actual scaling behavior, including large text and display scaling. Avoid fixed font/file counts, component heights, padding grids or icon opacity formulas presented as universal requirements. Common 48 dp target guidance is a useful baseline; check the actual component and platform rule.

## Semantics and lifecycle

Give controls meaningful names, role/state and a usable traversal order. Visible text often already supplies a label; adding “Play button” as a redundant content description can cause duplicate role announcements. Decorative imagery should be excluded appropriately. Test TalkBack and relevant keyboard/switch paths.

Handle permission grants, denial/revocation, activity/process recreation and account state through the supported lifecycle. Do not log secrets or persist credentials in ordinary preferences without the platform-supported protection the product requires. Current secure-storage APIs may change; inspect supported implementations rather than mandating a deprecated class name.

## Verify

Run relevant build/analyze/tests, then inspect the actual emulator/device output and affected flow. Include keyboard, back, text/display scale and relevant permissions/insets. A browser preview or shared logic test cannot prove Android-native behavior. Report the actual target/device checks and distribution/device limitations.
