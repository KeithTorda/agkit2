# Diagnose mobile failures with evidence

Record device/emulator, OS, app build/variant, framework/native versions, reproduction and observed failure. Compare expected and actual behavior. Inspect relevant client, native and backend logs without dumping tokens or personal records. A red screen versus app exit is a clue, not an infallible JS/native classification.

## Locate the failing boundary

- **Build/install:** inspect the first meaningful compiler/package/signing error and actual toolchain compatibility. Dependency resolution, permissions, certificates, architecture and SDK requirements have different remedies.
- **Runtime crash/ANR:** use platform crash logs, stack traces and appropriate debugger. Android `adb logcat`, Android Studio and Xcode device diagnostics may help when available. Match symbols/source maps to the actual build.
- **UI/state defect:** reproduce with real content, navigation and accessibility settings; inspect hierarchy, constraints, safe areas, lifecycle and stale async state.
- **Network/auth:** inspect actual request/status and server correlation evidence. Emulator host routing, device firewall, TLS, provider configuration and session refresh can differ from a desktop browser.
- **Performance:** profile the affected thread/workload rather than inferring the cause from a deep component tree alone.

Use supported tools already available for the installed runtime. Do not assume every React Native version has identical debugger/network features or install a proxy just to see one sanitized API error. If intercepting device traffic is required and authorized, understand certificate/pinning and environment boundaries; do not weaken production TLS to debug.

## Test one hypothesis

Trace the cause, make an explanatory change, and reproduce the failure again. A clean/reinstall can be useful for a demonstrated stale generated artifact or dependency issue, but is not the first universal fix. Preserve diagnostic evidence and user data before destructive cache/app resets. Do not run `pod deintegrate`, remove lockfiles, wipe databases or clean every cache without understanding the affected boundary.

For async behavior check cancellation, stale responses, effect/controller cleanup and callbacks after disposal. For native configuration inspect the actual manifest/entitlements/build target and dependency requirements rather than applying generic flags.

Recheck the original defect and relevant adjacent behavior. Report root cause, correction, actual build/device checks and exact limitations. A simulator-only fix should not be described as verified on physical hardware.
