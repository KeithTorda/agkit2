# Verify mobile behavior through the appropriate layer

Choose evidence from what can break. Pure business rules, widget/component behavior, native integration and real-device experience need different checks. Do not impose test-percentage quotas or assume a package makes end-to-end tests fast/reliable in every project.

| Concern | Useful verification |
|---|---|
| Domain calculation/validation/queue rules | Focused unit tests with boundary and duplicate/error cases |
| Component input and state | Supported React Native/widget tests with representative providers and semantics |
| API/storage integration | Appropriate integration tests against controlled real dependencies or explicit mocks |
| Navigation/device capability | Available native automation or manual simulator/device flow |
| Performance/graphics/battery | Relevant release/profile trace on representative hardware |
| Accessibility | Platform inspectors plus actual VoiceOver/TalkBack/input/scaling checks when available |

Reuse the project's tools. Detox, Maestro, Appium, native platform tests and Flutter integration tests have different compatibility and operational costs; none is a required universal choice. Browser E2E verifies a web surface, not native permissions or the packaged app. DOM-focused tools such as axe do not automatically audit a native accessibility tree.

## Relevant conditions

Exercise the primary changed flow and the failure cases it can encounter: invalid input, denied/revoked permissions, recoverable request failure, interrupted save, offline start or reconnection. If work is queued, check process death, duplicate delivery and account isolation. Do not require every static screen to invent an async skeleton/error/empty state.

When navigation changes, test back/dismissal, tab state, keyboard, deep links and launch/resume conditions as relevant. Native differences need platform coverage; shared logic may be tested once while platform integration still needs each target. Confirm actual permission/push/link behavior for the target OS rather than repeating old blanket rules.

Inspect real rendered screens with realistic content, larger text, focus/accessibility semantics, safe areas and relevant orientation/window sizes. Verify shipped themes only. For performance, state device/build/data/network and actual measurement; a simulator or debug build has limits.

## Maintainable checks and reporting

Use tests for meaningful contracts and behavior. Avoid brittle assertions mirroring every class/style value or snapshots accepted without review. Keep external-service side effects in the authorized environment; payment checks should use available sandbox/test paths rather than real charges by default.

Run appropriate project analyze/lint/type/build tests and available native checks. Report the actual target, device/emulator, flow and result; distinguish static, mocked, simulator, real-device and store-release verification. A missing build environment is an explicit unverified part, not a passing native test.
