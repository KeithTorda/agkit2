---
name: mobile-design
description: Mobile-first design and engineering for iOS and Android apps built with React Native (Expo) or Flutter - touch targets and thumb zones, list and animation performance, navigation, platform conventions, offline, and mobile testing. Use when building or reviewing a mobile app's UI, native layer, or mobile-specific backend; not for web apps.
version: 2.0.0
---

# Mobile Design

Mobile is not a small desktop: imprecise fingers, one hand, bad networks, limited battery, interrupted sessions. Design for the worst case and it works everywhere. This file is the index and the checklist; each area has a reference file below. Tech baseline: Expo SDK 54+ with Expo Router, React Native New Architecture (the React Compiler is a separate opt-in via `babel-plugin-react-compiler`; the kit's Expo template enables it), Reanimated 4, FlashList v2, NativeWind 4; Flutter 3.3x with Riverpod or Drift; iOS 26 and Android 16 are the current platform baselines.

## Reference files

| File | Read when |
|------|-----------|
| [mobile-design-thinking.md](mobile-design-thinking.md) | Deciding a screen's structure; questioning default patterns |
| [touch-psychology.md](touch-psychology.md) | Touch targets, thumb zone, gestures, haptics |
| [mobile-performance.md](mobile-performance.md) | Lists, animations, memory, battery, 60/120 fps |
| [mobile-navigation.md](mobile-navigation.md) | Tabs, stack, drawer, deep linking |
| [mobile-typography.md](mobile-typography.md) | Type scale, Dynamic Type, text scaling |
| [mobile-color-system.md](mobile-color-system.md) | OLED, dark mode, outdoor contrast |
| [mobile-backend.md](mobile-backend.md) | Push, offline sync, mobile API shape, auth |
| [mobile-testing.md](mobile-testing.md) | Unit, component, E2E (real devices when available) |
| [mobile-debugging.md](mobile-debugging.md) | Native vs JS crashes, device logs |
| [platform-ios.md](platform-ios.md) | Building for iPhone/iPad (HIG, iOS 26) |
| [platform-android.md](platform-android.md) | Building for Android (Material 3, Android 16) |
| [decision-trees.md](decision-trees.md) | Framework, state, storage, offline, auth choices |

Read only the files the task needs. For cross-platform work read both platform files and branch on platform where conventions differ.

## Questions before building

Questions: follow the global `core-protocol` rule.

For mobile the answers that most often change the build are platform (iOS, Android, or both), framework (React Native, Flutter, or native), and whether it must work offline; infer them from the brief or existing project when you can, and state the default you chose.

## Decision tree

Framework, state management, storage, offline, and auth decisions live in [decision-trees.md](decision-trees.md). Default for a cross-platform app that wants OTA updates: React Native + Expo, Expo Router, TanStack Query for server state plus a light client store, SecureStore for secrets.

## Platform-adaptive: share vs diverge

One codebase, two platforms — the skill is knowing which layer is shared and which the OS owns. Clone iOS onto Android and it feels foreign; fork the whole UI and you double the work and drift.

- **Share** (one source of truth): brand identity — color, type ramp, spacing, radius, motion feel, copy — plus information architecture and all business logic. These come from `DESIGN.md` tokens (`@[skills/design-spec]`) and the shared-taste bar in `@[skills/frontend-design]`; do not fork them per platform.
- **Diverge** (per platform): the interaction grammar the OS owns — navigation transitions and the back model (iOS edge-swipe, no system back button; Android system/predictive back), native controls (iOS switch / action sheet / wheel picker vs Android checkbox / bottom sheet / M3 pickers), the share sheet, default type (SF Pro + Dynamic Type vs Roboto + sp), touch minimums (44 pt vs 48 dp), haptics, and the safe-area / edge-to-edge model.
- **The test**: would a native user of *this* platform be surprised by this control or gesture? If yes, adapt it. Prefer a native-stack navigator (each platform gets its own transitions and back behavior for free) and `Platform.select` for the few controls that genuinely differ — not a top-to-bottom fork. Platform details: [platform-ios.md](platform-ios.md), [platform-android.md](platform-android.md).

Safe areas are load-bearing, not decoration — never hard-code inset padding:

```tsx
// Wrong — a magic number for "the notch": breaks on other devices, on
// rotation, and on Android 16 edge-to-edge (now enforced for the target SDK).
<View style={{ paddingTop: 44 }}>…</View>

// Right — read the real insets (SafeAreaView with explicit `edges` also works).
import { useSafeAreaInsets } from 'react-native-safe-area-context';
const insets = useSafeAreaInsets();
<View style={{ paddingTop: insets.top }}>…</View>
```

## Non-negotiables

- Touch targets at least 44 pt (iOS) / 48 dp (Android) with at least 8 pt spacing; primary actions in the thumb zone; every gesture has a visible alternative.
- FlashList v2 for long lists (`ListView.builder` in Flutter); FlatList acceptable for short fixed lists; never `ScrollView` with mapped items; stable `keyExtractor` from data, never the index.
- Secrets in Keychain / EncryptedSharedPreferences / SecureStore, never `AsyncStorage`; no hard-coded API keys; no tokens or PII in logs.
- Every screen has loading, error-with-retry, and empty states, and degrades gracefully offline.
- Follow platform conventions (share vs diverge above): iOS feels like iOS, Android like Android.

## Memoization

Compiler-first when the React Compiler is enabled; the memo rule is in `nextjs-react-expert`. The New Architecture does not ship the compiler by itself: look for `babel-plugin-react-compiler` in `babel.config.js` and the lockfile. Profile on a low-end device; without the compiler, memoize measured hot list items only. Correctness rules still apply: a stable `keyExtractor`, cleanup in `useEffect`, and `useNativeDriver: true` (or Reanimated 4, which runs on the UI thread) are not memoization and are always required. Flutter's equivalent is `const` constructors and targeted rebuilds (`ValueListenableBuilder`, `ref.watch(provider.select(...))`).

## Checklist

Before starting: platform, framework, navigation pattern, state approach, offline requirement, and target devices settled (asked or stated as defaults); deep linking planned from the start.

Every screen: touch targets and spacing meet the minimums; primary CTA reachable one-handed; loading, error, and empty states present; offline handled; platform conventions followed; interactive elements have accessibility labels.

Before release: no `console.log` / `print` in release builds; secrets in secure storage; SSL pinning where required; lists and animations profiled on a low-end device; subscriptions and timers cleaned up; Dynamic Type / font scaling to 200 % tested; dark mode and outdoor contrast checked; E2E run on real devices when available, simulators/emulators otherwise.

## Script (advisory)

`./scripts/mobile_audit.py <project>` scans React Native and Flutter code for the non-negotiables above (touch sizes, `ScrollView` for lists, index keys, secrets in `AsyncStorage`, missing cleanup, `console.log`). It is heuristic; confirm each finding in context before changing code.

```powershell
python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/skills/mobile-design/scripts/mobile_audit.py .
```
