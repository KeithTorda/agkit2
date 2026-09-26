---
name: browser-verification
description: "How to check what actually rendered in the running app: screenshot, real DOM, computed styles against DESIGN.md tokens, console and network errors, one interaction, mobile and desktop widths. Use for /see, when UI looks wrong, or when code-rules calls for a visual check of a layout change."
version: 2.5.0
---

# Browser Verification

> Reading the source tells you what you wrote. Only the browser tells you what the user gets.

Static analysis cannot see a render. Contrast comes from computed CSS, not from the class name;
focus order comes from the live tree, not the JSX; overflow only exists at a width. This skill is
how to look when looking is worth it.

## When this runs

`code-rules` decides whether: a layout change at tier 1 or above with a dev server running, or
whenever the user asks (`/see`). Non-visual changes, a colour or copy tweak, or no server/browser:
skip it and say so in one line of the report. This skill is *how* to look, not a gate on every
UI edit. Match the depth to the change: a new page gets the full pass; a fixed margin gets one
screenshot at the width that was broken.

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

Fix what fails **before** writing the report, then render again. Two passes is normal on a new
page. This is your own work in the same task, so refine it without asking; only changes that
alter scope or a user-approved design direction need a question.

### 3. Read the DOM, not the source

Pull the rendered element tree for the region you changed. This is where you catch what source
review cannot: a component that rendered nothing, a list that rendered zero items, a conditional
that fell to the wrong branch, a wrapper that collapsed to zero height, duplicated ids.

### 4. Check computed styles against the tokens

The highest-value check in this skill, and the one nothing else in the kit does.

Read the **computed** values — color, background, font-size, spacing, radius, shadow — for the
elements you touched, and compare them to the `DESIGN.md` token scale (`design-spec` skill owns the
token format). Flag every value that is not on the scale.

Do not eyeball it — collect the real values with `getComputedStyle` and compare them as data, then reduce to the distinct values per property: a page using nine font sizes or six greys has a token problem however good any single element looks. The dump snippet and a worked wrong-vs-right example are in [computed-styles.md](./computed-styles.md).

### 5. Read the console and the network

Capture both. A page that *looks* right while throwing hydration errors, failed fetches, or 404s on
assets is not right. Report every error and warning with its message. A 4xx/5xx on the route's own
data call is a required failure, not an advisory note.

### 6. Interact once

Click the primary action of what you changed and confirm it does what it should. Submit the form
with valid input, then with invalid input, and confirm the error state renders. One real pass
through the flow catches what no amount of reading finds — a dead button, a handler wired to the
wrong element, a state update that never re-renders.

### 7. Widths

Render at mobile (~390px) and desktop (~1440px); add tablet (~768px) when the layout has a
tablet breakpoint or the bug lives there. At each width confirm: no horizontal overflow, nothing
clipped or overlapping, text stays readable, touch targets stay tappable on mobile. Most layout
bugs live at one width and are invisible at the others.

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

### Must-fix when you see them

Each one is visible in a single screenshot, and each has shipped because nobody looked:

- **Two design languages on one screen.** An existing header, nav, or footer left in the old style
  beside your new work is an *unfinished redesign*. Either restyle the shell to the same
  tokens, or state in the report that it is out of scope and why. "New dashboard bolted under the old
  chrome" is the most common version of this.
- **Mutually exclusive states rendered together** — Login and Logout both visible, an empty state
  behind real data, a loading skeleton beside loaded content.
- **Text you cannot read.** Any string at or near the background's own colour. If you cannot read it
  in the screenshot, neither can the user; check its computed pair rather than assuming a theme
  variable resolved.
- **Colour that encodes nothing.** The same quantity in two different colours, or values coloured for
  variety. Colour carries state — good, fair, poor, destructive — or it is not applied at all. Two
  readings with the same unit and the same meaning get the same treatment.
- **An icon that denotes something other than its label** — a currency mark beside a data volume, a
  filled block where a status glyph belongs, a placeholder that shipped.
- **A raw or concatenated field rendered as a value** — a model code fused to an identifier, an
  untranslated key, an ISO timestamp where a date belongs. Read every value on screen and confirm it
  is the value, formatted.
- **Two units of different scale side by side** — `0.56Kb/s` next to `488b/s`. Normalise, or state
  the rule you used.
- **The same fact twice** in one view, unless the repetition is doing work.

## Report

```markdown
## Visual Verification Report
### Target
- Route: <url> · widths checked: <the widths you actually rendered>
### Rendered
- <what you actually observed, per width>
### Token conformance
- <violations with computed value vs DESIGN.md scale, or "no violations">
### Console / network
- Errors: <messages, or none> · Failed requests: <status + url, or none>
### Interaction
- <action taken → observed result; error path result>
### Findings
- Must fix: <render, console, network, broken interaction, unreadable text>
- Polish: <spacing rhythm, off-scale values, craft notes>
### Not verified
- <what needs a human eye and why>
```

## Evidence on disk (optional)

Useful for tier 2-3 work, client handoff, or when the user asks for proof. Write to
`<project>/.agents/verify/<task-slug>/` one screenshot per width you checked, named
`<before|after>-<cssWidth>.png` (`after-390.png`, `after-1440.png`, plus `before-<width>.png` on a
repair). Then `verdict.json`:

```json
{ "route": "/dashboard", "widths": [390,768,1440], "consoleErrors": 0, "failedRequests": 0,
  "interaction": "pass", "tokenViolations": [], "status": "pass", "notVerified": [] }
```

`status` is `pass` only when the route rendered, no uncaught console error, no failed data request on
this route, and the interaction succeeded; otherwise `fail`, or `skipped` with a `reason`.

`ui_verify.py` checks that the files are what they claim:

```bash
python "KIT/scripts/ui_verify.py" .agents/verify/<task-slug> --widths 390,1440 [--require-before]
```

Without `--widths` it checks the widths in `verdict.json`, else 390 and 1440. It fails (exit 1) when
a width has no screenshot, when a file's real pixel width does not match its name (at a device pixel
ratio of 1, 1.25, 1.5, 2 or 3), when two "different" views are byte-identical, or when the verdict
says `pass` while recording console or network errors. A verdict with status `skipped` and a
`reason` is an honest skip and exits 0. `--json` prints the result; `--report FILE` also writes it. Whether or not you save files, never claim a width you did not render.

## Boundaries

Functional E2E suites belong to `testing-patterns` (`playwright_runner.py`); this skill is
exploratory verification of what rendered, not a regression suite. Performance numbers (Lighthouse,
INP) belong to `performance-profiling`. Design judgment and token authoring belong to
`frontend-design` and `design-spec`. Report what you see here; fix it there.
