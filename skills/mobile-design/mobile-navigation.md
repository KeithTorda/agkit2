# Navigation, back and restoration

Model destinations and task relationships before choosing chrome. Frequent peer destinations can suit tabs or a rail; hierarchical detail can suit a stack; a focused temporary task may suit a sheet/modal; larger windows can support list-detail or sidebars. Item counts inform fit but do not force a drawer/tab architecture or a fixed bar height.

Use the project's supported router and platform conventions. Keep navigation state authoritative there rather than mirroring the whole stack into a global store. Preserve useful per-destination state and scroll position where users expect it; an explicit reset can still be a legitimate product action.

## Back and dismissal

Respect platform system-back and interactive navigation behavior. Back may dismiss a dialog, hide the keyboard, return through a stack or exit a task depending on the platform/state; it does not universally mean pop one screen. Handle unsaved changes and cancellation deliberately without trapping users. Confirm predictive-back support and APIs for the actual Android target/runtime rather than hardcoding an old OS baseline.

Sheets, dialogs and full-screen tasks need an accessible close/cancel path and appropriate focus behavior. Decide whether outside-tap/swipe dismisses from the task's consequences. Avoid blocking dismissal merely because it is easier than preserving a draft.

## Deep links and notifications

Implement links when the product needs external entry, sharing or notification destinations. Validate route parameters, identity and resource authorization. Do not trust a link to grant access. Define cold-start and warm-session behavior, invalid/deleted resource recovery and post-login continuation. The correct back stack depends on the entry context; do not always synthesize a Home stack or always push over the current flow.

Use current platform Universal/App Link configuration where needed. Test actual target behavior, redirects, app-not-installed fallback and relevant domain association. A local router URL test alone does not establish OS link association.

## Restore appropriately

Persist only useful state within its account/privacy boundary. Version stored navigation data, tolerate invalid JSON/obsolete routes and reconcile it with incoming links/session state. Sensitive route parameters and drafts can leak through naive persistence. Clear or isolate state on account switch as appropriate.

Transitions should support spatial understanding, fit the brand and respect motion preferences. Use native defaults when suitable; custom transitions can be appropriate when they preserve gestures, accessibility and interruption. Avoid a universal duration ceiling or a shared-element library requirement.

Verify the actual flow on available targets: back/dismiss, tab switching, keyboard, deep links, background/relaunch and larger-window layout where relevant. Report device/emulator coverage and any OS integration not checked.
