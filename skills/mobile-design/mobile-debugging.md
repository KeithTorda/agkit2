# Mobile Debugging Guide

Mobile apps have a native layer under the JavaScript or Dart, so text logs alone are not enough. When the code looks correct but the app still fails, look at the native side. Key differences from web debugging:

- A JS error shows a red screen; a native crash drops straight to the home screen.
- You cannot just refresh — state gets stuck, and a clean native build is often needed.
- Network is harder to inspect (SSL pinning, proxy setup).
- `adb logcat` and Xcode's Console are the source of truth for native problems.

## Habits to drop

- "Add console.logs" — use React Native DevTools or Reactotron instead.
- "Check the network tab" — use Charles Proxy or Proxyman.
- "It works on the simulator" — reproduce on a real device; some bugs are hardware-specific.
- "Reinstall node_modules" — clean the native build (Gradle / Pod cache) when the failure is native.
- Ignoring native logs — read `logcat` / Xcode logs.

## 1. Tools

React Native / Expo: Reactotron (state, API, Redux), React Native DevTools (console, network, components, profiler — the default debugger on RN 0.76+), Expo's element inspector for quick UI checks.

Native layer: `adb logcat` for Android native crashes and ANRs; Xcode Console (via Window > Devices) for iOS native exceptions and memory; Android Studio Layout Inspector and Xcode View Inspector for UI hierarchy bugs.

## 2. Common workflows

**App crashed.** A red screen is a JS error — read the on-screen stack trace, usually clear (undefined access, bad import). A crash to the home screen is native — filter Android errors with `adb logcat *:E`, or open Xcode > Window > Devices > View Device Logs. A crash immediately on launch is almost always native configuration (Info.plist, AndroidManifest.xml).

**API request failed.** You usually cannot see mobile traffic in a browser devtools panel. Use React Native DevTools or Reactotron to view requests, or a proxy (Charles / Proxyman) to see all traffic including native SDKs — the proxy needs its SSL cert installed on the device.

**UI is laggy.** Measure, do not guess. RN: the Performance Monitor from the shake menu. Android: "Profile GPU Rendering" in Developer Options. A JS FPS drop means heavy work on the JS thread; a UI FPS drop means too many views, a deep hierarchy, or heavy images.

## 3. Platform-specific traps

Android: Gradle sync failures are usually a Java version mismatch or duplicate classes; the emulator reaches the host at `10.0.2.2`, not `127.0.0.1`; `./gradlew clean` clears cached builds. iOS: `pod deintegrate && pod install` for Pod issues; check Team ID and Bundle Identifier for signing errors; Product > Clean Build Folder clears Xcode's cache.
