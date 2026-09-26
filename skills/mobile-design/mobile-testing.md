# Mobile Testing Patterns

Mobile testing is not web testing: the native layer, platform differences, wildly varying networks, app lifecycle (backgrounded, killed, restored), permission dialogs, and touch instead of clicks all matter. Test the right things, not everything — a flaky E2E test is worse than none.

## Web habits that fail on mobile

- Jest alone misses the native layer — pair it with device E2E.
- Cypress and other browser E2E cannot reach native features — use Detox or Maestro.
- Mocking everything hides integration bugs — test on a real device.
- Happy-path only ignores mobile's real edge cases — offline, permissions, interrupts.
- 100% unit coverage is false security — balance the pyramid.

## 1. Which tool

| Testing | React Native | Flutter |
|---------|--------------|---------|
| Pure functions, reducers, transformers | Jest | `test` package |
| Isolated components / widgets | React Native Testing Library | `flutter_test` (widget tests) |
| Components with hooks, context, navigation | RNTL + mocked providers | `integration_test` |
| Full user flows (login, checkout) | Detox (fast, reliable) or Maestro | Maestro |
| Performance / memory | Flashlight, device profiling | Flutter DevTools, `--profile` |

Maestro (mobile.dev) is cross-platform and YAML-based. Appium is a slow last resort. Prefer Detox for RN critical flows.

## 2. The pyramid

Roughly 40% unit, 30% component, 20% integration, 10% E2E. Unit tests are fastest and most stable; E2E is slow and flaky but the only thing that catches real integration bugs. 90% unit and 0% E2E means you are testing the wrong things.

## 3. What to test at each level

- **Unit (Jest / Dart test):** utility functions, state reducers and stores, API response transformers, validation, business rules. Not rendering, navigation, or third-party libraries.
- **Component (RNTL / flutter_test):** renders correctly, user interactions (tap, type, swipe), loading/error/empty states, accessibility labels present, behaviour when props change. Not implementation details or brittle styling snapshots.
- **Integration:** form submission, navigation between screens, state persisted across screens, API integration against a mocked server. Not every path, and not the real backend.
- **E2E (real devices):** critical journeys (login, purchase, signup), offline-to-online transitions, deep links, push-notification navigation, permission flows, payments. Not every edge case (too slow) or backend-only logic.

## 4. Platform differences worth testing on both

Back navigation (iOS edge-swipe vs Android system/predictive back), permissions (iOS asks once; Android asks with rationale and supports revoking), keyboard behaviour, push payload shape (APNs vs FCM), and deep links (Universal Links vs App Links). Date pickers and custom gestures only if you built custom UI around them. Run unit and component tests once (same on both); run E2E and platform-specific cases per platform.

## 5. Offline and network

Test: starting the app offline (cached data or a clear offline state), going offline mid-action (queued, not lost), coming back online (queue syncs, no duplicates), slow 2G (loading states and timeouts fire), and flaky connections (retry and recovery work). Drive it with mocked `NetInfo` in unit tests, mocked responses in integration, `device.setURLBlacklist()` in Detox, and Charles Proxy / Network Link Conditioner manually.

## 6. Performance

Measure app startup (under 2 s), screen transitions (under 300 ms), list scroll (60 fps), memory (stable, no leaks), and bundle size. Profile before release, after heavy features, after dependency upgrades, and when users report slowness. Test on a real low-end device (a Galaxy A-series or an old iPhone) on a release/profile build with production-like data — emulators and simulators hide performance problems; say so in the report when you only had one.

## 7. Accessibility

Verify interactive elements have labels, images have alt text or a decorative flag, form labels are linked, buttons expose a button role, touch targets meet 44pt/48dp, and contrast meets WCAG AA. Automate with jest-axe (RN) or the Flutter accessibility checker plus lint rules for missing labels; then manually navigate the whole app with VoiceOver / TalkBack, at increased text size, and with reduced motion.

## 8. CI/CD

| Stage | Tests | Devices |
|-------|-------|---------|
| PR | Unit + component | None (fast) |
| Merge to main | + integration | Simulator / emulator |
| Pre-release | + E2E | Real devices (farm) |
| Nightly | Full suite | Device farm |

Device farms: Firebase Test Lab (free tier, Android-leaning), AWS Device Farm and BrowserStack (wide but paid), local devices (free, reliable, limited variety).

## Before writing tests, ask

What could break — test that. What is critical for users — E2E that. What is complex logic — unit test that. What is platform-specific — test on both. What happens offline — test that scenario. Good coverage catches real regressions; a static-component snapshot rarely does.
