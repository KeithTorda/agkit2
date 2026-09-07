# Browser verification — preconditions and failure modes

Read this when a browser step is refused, when a check behaves oddly, or before reporting that the
gate could not run. The protocol itself is in [SKILL.md](./SKILL.md).

## Preconditions (check these before blaming the code)

Antigravity drives a real Chrome through its browser subagent. Three settings decide whether this
skill can run at all, and each fails in a way that looks like a code problem:

| Requirement | Where | If missing |
|---|---|---|
| **Google Chrome installed** | system | The browser subagent cannot start at all |
| **Settings → Browser → Enable Browser Tools** | Antigravity settings | No navigation, no screenshot, no DOM |
| **Browser Actuation Rules allow the dev-server URL** | Settings → Browser → Actuation Permissions | Navigation to `localhost` is refused — looks like the server is down when it is a permission |

If a browser step is refused, check the actuation rules for `http://localhost:*` **before** touching
the app. Report the blocked precondition as the escape-hatch reason; do not silently fall back to
reading source and call it verified.

## Failure modes to watch for

- **Screenshotting the wrong thing** — an old port, a cached build, a route that redirected. Confirm
  the URL in the report matches what you meant to check.
- **Declaring it fine because it looks fine** — the screenshot is one of six checks. A page can look
  perfect and be throwing console errors, failing its data fetch, and unusable by keyboard.
- **Checking only desktop** — the width you developed at is the width least likely to be broken.
- **Reading source styles instead of computed styles** — a class name is an intention; the computed
  value is the fact. Tailwind arbitrary values, cascade order, and specificity all break the link
  between them.
- **Verifying the happy path only** — empty, error, and long-content states are where UI actually
  fails in production.
- **Treating a console error as advisory** — an uncaught exception or a failed request on the route
  you changed blocks "done".
- **Mistaking a blocked precondition for a passing check** — if browser actuation refused the URL or
  Chrome is not installed, you verified nothing. That is an escape-hatch skip with a stated reason,
  never a pass.

