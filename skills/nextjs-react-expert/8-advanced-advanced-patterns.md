# Initialization and external callback lifetimes

Use these patterns when a real lifecycle/subscription problem exists. Avoid clever global state or dependency suppression simply to make an effect run less often.

## Rule 8.1: Initialize once at the correct scope

"Once" needs an owner: per process, request, browser tab, user session, component instance or external resource. A module-level flag may be process-wide on a server and leak assumptions across users; module reloads or multiple bundles can also invalidate it.

A lazy process-level client/pool may be appropriate when documented by the runtime and safe to share. Per-request identity/data should remain scoped to its request. Browser-only initialization should not execute through a server import. Component setup needs symmetric cleanup and must tolerate the framework's supported mount/reconnect behavior.

Do not disable Strict Mode or add a global `initialized` flag just to silence repeated development effects. Determine whether the effect duplicates a real write, omits cleanup, or is placed at the wrong boundary. Idempotent setup and resource ownership usually solve the underlying issue more reliably.

For an irreversible user action, trigger it from the operation boundary and use business idempotency as needed; a component mount is not an exactly-once guarantee.

## Rule 8.2: Read current callbacks without hiding dependencies

External subscriptions may need a stable connection while their callback observes current values. Start with the framework's supported effect/dependency model. A stable wrapper/ref or a supported API such as `useEffectEvent` can serve a documented non-reactive callback case.

Verify the installed React version and restrictions before using `useEffectEvent`. It is not a general dependency-array escape hatch or a replacement for every callback. Do not pass an effect-only callback into arbitrary components or events if its contract forbids that.

When using refs deliberately, update/read them in a lifecycle-safe way and document why the referenced value should not resubscribe. Values that change the resource identity, permission or subscription target usually remain real dependencies. A callback seeing fresh values does not resolve a stale resource connection.

## Prove the lifecycle

Exercise mount/unmount, identity changes, reconnects, navigation and repeated events. Confirm only intended resources persist, callbacks see the correct state and old subscriptions cannot modify the current session. Check cleanup after failure/cancellation. Compare profiler evidence when reduced work is a goal; correctness comes before minimizing effect counts.
