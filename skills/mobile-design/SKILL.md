---
name: mobile-design
description: "Design and implement native or cross-platform iOS and Android interfaces with platform-aware navigation, touch, typography, safe areas, data and device verification. Supports existing React Native, Flutter and native projects without forcing a framework or package."
version: 2.8.2
---

# Mobile product design and engineering

Build for real devices, interrupted sessions, touch input, accessibility settings and variable networks. Preserve the project's supported native or cross-platform foundation. A mobile request does not automatically select Expo, Flutter, a state manager, list package, platform release, or minimum OS version.

## Establish the brief and environment

Before every new visual design, ask one short style-and-reference question and wait unless the user already answered or explicitly delegated. Maintenance matching the approved system does not repeat this intake. Inspect existing screens, navigation, tokens, manifests, build configuration and device targets while waiting.

Identify iOS/Android scope, device classes, existing framework, minimum/deployment targets, needed native capabilities, distribution path and offline expectations. Resolve consequential gaps; use current platform documentation when an SDK/API decision depends on a moving target. Do not call an old kit version “current”.

## Pick references by the work

| Concern | Reference |
|---|---|
| Screen structure and user task | [mobile-design-thinking.md](mobile-design-thinking.md) |
| Touch, gesture alternatives and haptics | [touch-psychology.md](touch-psychology.md) |
| Navigation, back, deep links and restoration | [mobile-navigation.md](mobile-navigation.md) |
| Text scaling and semantics | [mobile-typography.md](mobile-typography.md) |
| Color, contrast and supported themes | [mobile-color-system.md](mobile-color-system.md) |
| Lists, animation, startup and battery | [mobile-performance.md](mobile-performance.md) |
| Auth, API, offline state and push | [mobile-backend.md](mobile-backend.md) |
| Testing and evidence | [mobile-testing.md](mobile-testing.md) |
| Reproducing JS/native/device defects | [mobile-debugging.md](mobile-debugging.md) |
| Platform behavior | [iOS](platform-ios.md), [Android](platform-android.md) |
| Framework, state, storage and offline decisions | [decision-trees.md](decision-trees.md) |

## Share deliberately, adapt deliberately

Share product concepts, domain logic, contracts, brand and semantic roles where appropriate. Adapt platform-owned behavior—back navigation, permission prompts, pickers, share sheets, safe areas, keyboard behavior and accessibility—to what users expect. Native controls can coexist with a distinctive brand. Do not fork every screen merely to change a picker, or force Android users through an iOS navigation model.

Read actual insets and window dimensions; do not encode a notch height or assume orientation never changes. Account for the on-screen keyboard, tab bars, system UI, foldable/tablet layouts and text expansion as the target scope requires. Typical platform target guidance is around 44 pt on iOS and 48 dp on Android, subject to current component/platform rules; a CSS pixel is not a universal native unit.

Keep controls named and usable with screen readers, larger text and keyboard/switch input where supported. Avoid color-only status and hover-only actions. Gestures need discoverability and an accessible equivalent for essential actions. Use haptics selectively with normal visual/state feedback.

## Implement and verify the real flow

Keep transient state local and authoritative state at the proper data boundary. Preserve entered data during recoverable errors. Handle loading, empty, permission, failure and offline conditions where the screen can encounter them. Offline writes need a defined queue/conflict policy; do not label unsent work as server-confirmed.

Use platform-backed secure storage for sensitive credentials, redact logs, validate API input and authorize server operations. List virtualization and animation tools follow measured need and installed versions; do not require a specific list library or memoization pattern everywhere. Clean up subscriptions, timers and async callbacks.

Run relevant project checks, compile the changed target when available, and inspect the actual simulator/emulator/device output. Exercise the primary flow and affected permissions, keyboard, back behavior or rotation. Use representative devices and network conditions proportional to the feature; a web preview does not prove native behavior.

`python "KIT/skills/mobile-design/scripts/mobile_audit.py" <project-or-file>` offers heuristic source checks; inspect findings and supported options before relying on a failure level. It cannot establish touch usability, secure storage behavior, device performance or accessibility compliance.

Report target/runtime, device or emulator used, actual flow checks, visual findings, and what could not run. Separate simulator verification from real-device or store-release validation. Do not promise error-free operation from static checks.
