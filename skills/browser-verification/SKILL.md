---
name: browser-verification
description: "Verifies what actually rendered by opening the running app in the browser: screenshot, real DOM, computed styles against DESIGN.md tokens, console and network errors, one interaction pass, and the breakpoint matrix. Use after any change that affects rendered UI, before reporting done, and for /see."
version: 1.0.0
---

# Browser Verification

> Reading the source tells you what you wrote. Only the browser tells you what the user gets.

Static analysis cannot see a render. Contrast comes from computed CSS, not from the class name;
focus order comes from the live tree, not the JSX; overflow only exists at a width. This skill is
how the kit stops guessing about UI.

## When this runs

Required for any change that affects rendered UI — the gate and its escape hatch are defined in the
global `code-rules` rule. This skill is *how* to run it, not *whether*.

**Read when:** a browser step is refused, or a check behaves oddly → `troubleshooting.md`
(preconditions: Chrome, Enable Browser Tools, actuation rules; and the seven ways this verification
goes wrong).

## Protocol

### 1. Get the app running

Reuse the dev server that is already up. Never start a second one — a stale port serves an old
build and you will verify the wrong thing. If nothing is running, start it and wait for the ready
line before navigating. Note the exact URL and route you are about to check.

### 2. Render and look

Open the route in the browser tool and take a screenshot. Then answer, in words, what you see —
not what you expect to see. "The card grid renders three across with the CTA below the fold" is an
observation; "the layout should be fine" is not.

### 2b. Critique your own draft against the bar, then refine

A first render of your own work is a draft, not a finding to escalate. With the screenshot in front
of you, answer `frontend-design` §4.0 as questions: what wins the eye first, and is it the right
thing (the §0.F primary action or first-seen item)? Can you name the type-scale step and the
spacing step of every gap you see? Is there anything on this page the named reference (§0.C)
would not do? Does the empty state say what to create, does the error say what to do next (§4.7)?

Fix what fails **before** writing the report, then render again. Two passes is normal; a page that
needs none was probably not looked at. This is your own un-reviewed UI in the same task, so you
refine it without asking (the carve-out in `code-rules`); only changes that alter scope or a
user-approved design direction need a question.

### 3. Read the DOM, not the source

Pull the rendered element tree for the region you changed. This is where you catch what source
review cannot: a component that rendered nothing, a list that rendered zero items, a conditional
that fell to the wrong branch, a wrapper that collapsed to zero height, duplicated ids.

### 4. Check computed styles against the tokens

The highest-value check in this skill, and the one nothing else in the kit does.

Read the **computed** values — color, background, font-size, spacing, radius, shadow — for the
elements you touched, and compare them to the `DESIGN.md` token scale (`design-spec` skill owns the
token format). Flag every value that is not on the scale.

Do not eyeball this. Antigravity's JavaScript execution policy is on, so collect the real values
with `getComputedStyle` and compare them as data:

```js
// Dump computed values for the region you changed, then diff against DESIGN.md
[...document.querySelectorAll('main *')].slice(0, 80).map(el => {
  const s = getComputedStyle(el);
  return {
    el: el.tagName.toLowerCase() + (el.className ? '.' + String(el.className).split(' ')[0] : ''),
    color: s.color, bg: s.backgroundColor, size: s.fontSize,
    pad: s.padding, gap: s.gap, radius: s.borderRadius,
  };
});
```

Then reduce to the distinct values per property — a page using nine different font sizes or six
greys has a token problem regardless of how any single element looks.

```text
WRONG (what source review concludes)
  "className='text-slate-600 p-5' — looks consistent with the design."

RIGHT (what the render actually reports)
  Computed: color rgb(71,85,105) · padding 20px · font-size 15px
  DESIGN.md scale: text-secondary #5A6472 · spacing 16/24 · type 14/16/20
  → 3 token violations: color off-scale, 20px not on the spacing scale, 15px not on the type scale.
```

Off-scale values are how a design drifts into mush one component at a time. Catch them at the
render or they ship.

### 5. Read the console and the network

Capture both. A page that *looks* right while throwing hydration errors, failed fetches, or 404s on
assets is not right. Report every error and warning with its message. A 4xx/5xx on the route's own
data call is a required failure, not an advisory note.

### 6. Interact once

Click the primary action of what you changed and confirm it does what it should. Submit the form
with valid input, then with invalid input, and confirm the error state renders. One real pass
through the flow catches what no amount of reading finds — a dead button, a handler wired to the
wrong element, a state update that never re-renders.

### 7. Breakpoint matrix

Render at mobile (~390px), tablet (~768px), and desktop (~1440px). At each width confirm: no
horizontal overflow, nothing clipped or overlapping, text stays readable, touch targets stay
tappable on mobile. Most layout bugs live at exactly one width and are invisible at the others.

## What to actually look for

A screenshot teaches nothing if you do not know what you are looking at. Work this list:

- **Overflow** — anything forcing a horizontal scrollbar: a fixed width, an unbroken string, an image with no `max-width`.
- **Stacking** — a dropdown, modal, or tooltip rendering behind its neighbour.
- **Contrast** — judge the *computed* pair: body below 4.5:1 fails, large text below 3:1 fails.
- **Focus visibility** — tab through; an invisible focus ring is a real failure and is invisible in source review.
- **Layout shift** — content jumping as images or fonts load; usually a missing dimension.
- **The four states** — loading, empty, error, long content. Render the empty list and the 200-character title.
- **Image aspect** — stretched or squashed media.
- **Spacing rhythm** — inconsistent gaps between siblings; reads as sloppiness even when nothing is broken.

## Report

```markdown
## Visual Verification Report
### Target
- Route: <url> · widths checked: 390 / 768 / 1440
### Rendered
- <what you actually observed, per width>
### Token conformance
- <violations with computed value vs DESIGN.md scale, or "no violations">
### Console / network
- Errors: <messages, or none> · Failed requests: <status + url, or none>
### Interaction
- <action taken → observed result; error path result>
### Findings
- Required: <render/console/network failures that block done>
- Advisory: <polish, spacing rhythm, non-blocking heuristics>
### Not verified
- <what needs a human eye and why>
```

## Leave the evidence on disk

A report in the reply is a claim; a file is evidence. Also write to
`<project>/.agents/verify/<task-slug>/`: `after.png` (1440) and `mobile-after.png` (390), plus
`before.png` on a repair — the only proof the defect existed — and `verdict.json`:

```json
{ "route": "/dashboard", "widths": [390,768,1440], "consoleErrors": 0, "failedRequests": 0,
  "interaction": "pass", "tokenViolations": [], "status": "pass", "notVerified": [] }
```

`status` is `pass` only when the route rendered, no uncaught console error, no failed data request on
this route, and the interaction pass succeeded; otherwise `fail`, or `skipped` with a `reason` naming
the blocked precondition. If the directory cannot be written, say so in one line and report inline.

## Boundaries

Functional E2E suites belong to `testing-patterns` (`playwright_runner.py`); this skill is
exploratory verification of what rendered, not a regression suite. Performance numbers (Lighthouse,
INP) belong to `performance-profiling`. Design judgment and token authoring belong to
`frontend-design` and `design-spec`. Report what you see here; fix it there.
