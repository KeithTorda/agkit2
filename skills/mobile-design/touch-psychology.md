# Touch, reach and feedback

Design for imprecise input, occlusion, different hands and assistive technologies. Use the actual platform and component guidance: common comfortable minimum target guidance is about 44 pt for iOS and 48 dp for Android. Native units, CSS px and physical millimeters are not interchangeable.

For a web accessibility target, distinguish WCAG 2.2's AA target-size criterion and its spacing/exceptions from the enhanced 44 CSS px criterion. Do not label every 44 px preference a universal WCAG AA requirement. Verify applicable current guidance when making compliance claims.

## Hit area and layout

Visual icon size and touch area can differ through appropriate padding or supported hit expansion. Avoid overlapping invisible hit regions, clipped hit slop and targets so close that users trigger the neighbor. Check the actual interactive bounds and screen-reader focus, including row controls, tiny close buttons and sliders.

Place frequent actions where the current task and device allow comfortable use. Reach varies with hand, grip, screen and accessibility settings; there is no reliable universal top-screen “dead zone” percentage. Respect platform navigation placement and system gestures. A destructive action needs understandable consequence and recovery rather than merely being harder to reach.

## Gestures and accessibility

Use gestures for discoverable, familiar behavior. Essential gesture-only actions need an accessible path appropriate to the platform: a named action/menu, buttons, select-then-move or supported assistive action. Do not require a redundant visible control for every standard scroll or navigation gesture if the platform already supplies an accessible equivalent. Avoid hijacking edge-back/home gestures.

Check movement cancellation, accidental activation, drag thresholds, single-pointer alternatives where applicable, long-press timing and interruption. Provide clear state feedback without relying on motion, color or vibration alone.

## Haptics and latency

Respond promptly and communicate actual progress. Use platform-supported press/selection feedback and haptics when they help the action and the user permits them. Haptics are optional; their absence does not make an app cheap. Do not vibrate on every tap/scroll or force an error shake that conflicts with reduced motion.

Prevent duplicate consequential submissions at the correct boundary. A disabled button may communicate pending state but does not provide server idempotency; repeated input can also be intentional in some controls. Match feedback, timing and recovery to the actual action instead of fixed spinner delays or scale values.

Verify on available devices with touch, larger text, screen-reader/switch behavior where relevant, and the actual keyboard/system UI. Report emulation limits honestly.
