# Touch Psychology Reference

> Fitts' Law for touch, thumb-zone anatomy, gesture design, and haptics. Read this for any mobile interaction work.

---

## 1. Fitts' Law for Touch

A mouse cursor is one pixel and precise; a fingertip is a ~7 mm contact patch that also hides the target it taps. Touch acquisition time rises as the target shrinks, so touch targets must be far larger than desktop ones, and the error cost is higher (a wrong tap is frustrating, not a quick re-click).

| Platform | Minimum | Recommended | For |
|----------|---------|-------------|-----|
| iOS (HIG) | 44 pt | 48 pt+ | All tappable elements |
| Android (Material) | 48 dp | 56 dp+ | All tappable elements |
| WCAG 2.2 | 44 px | - | Accessibility compliance |
| Critical actions | - | 56-64 px | Primary CTAs, destructive actions |

Visual size and hit area are separate: a 24 px icon can have a 44-48 px hit area via padding. Apply that to icon buttons, text links (44 px tall), list rows (48-56 px), checkboxes and radios (44-48 px tap area), and close buttons (44 px minimum).

---

## 2. Thumb Zone Anatomy

About half of users hold a phone one-handed. The screen splits into an easy-to-reach arc (bottom and center), an okay middle, and a hard-to-reach top that needs a stretch.

| Element | Ideal position | Reason |
|---------|----------------|--------|
| Primary CTA | Bottom center/right | Easy thumb reach |
| Tab bar | Bottom | Natural thumb position |
| FAB | Bottom right | Easy for right hand |
| Navigation, settings | Top | Less frequent |
| Destructive actions | Top left | Hard to reach = hard to hit by accident |
| Dismiss / Cancel | Top left | Convention and safety |
| Confirm / Done | Top right or bottom | Convention |

On phones over 6", the top ~40 % becomes a dead zone one-handed; use reachability, pull-down interfaces, bottom sheets, FABs, and gesture alternatives to top actions.

---

## 3. Touch vs Click Psychology

Touch expects instant feedback (under ~50 ms) with no hover step, tolerates errors poorly, and uses long-press for context menus and swipe/outside-tap for cancel. On every tap give an immediate visual change (highlight, slight scale to 0.95-0.98, Android ripple) plus haptic confirmation; show a spinner within 100 ms for anything slower and disable the control to prevent double taps. Because the finger occludes the target, put feedback above the touch point for precision tasks (tooltips, a magnification loupe for text selection) or make targets large enough that precision does not matter.

---

## 4. Gesture Psychology

Gestures are invisible: users must discover and remember them, and many never do. Always pair a gesture with a visible alternative (swipe-to-delete also offers a delete button; pull-to-refresh also offers a refresh control).

| Gesture | Meaning | Usage |
|---------|---------|-------|
| Tap | Select, activate | Primary action |
| Double tap | Zoom, like | Quick action |
| Long press | Context menu, selection | Secondary options |
| Swipe horizontal | Navigate, delete, actions | List actions |
| Swipe down | Refresh, dismiss | Pull to refresh |
| Pinch | Zoom | Maps, images |

Give swipe actions a visual hint (an edge color peek, a drag handle, onboarding). Platform differences: back is edge-swipe on iOS and the system back on Android; dismiss-modal is swipe-down on iOS and back or swipe on Android.

---

## 5. Haptic Feedback Patterns

Haptics confirm actions without looking, add a premium feel, aid blind users, and reduce errors; their absence makes an app feel cheap and web-like.

iOS types: `selection` (picker/toggle), `light`/`medium`/`heavy` impact (minor to important), and `success`/`warning`/`error` notification patterns. Android types: `CLICK`, `HEAVY_CLICK`, `DOUBLE_CLICK`, `TICK`, `LONG_PRESS`, `REJECT`.

Use haptics for button taps, toggles, picker/slider values, pull-to-refresh trigger, successful completion, errors and warnings, swipe-action thresholds, and important state changes. Do not fire them on every scroll position, every list item, background events, or so often they cause haptic fatigue. Map intensity to importance: light for browsing, medium for standard actions, heavy or success for significant actions, error pattern for failures.

---

## 6. Mobile Cognitive Load

Mobile attention is interrupted, input is slow, the viewport is small, and error recovery is harder than on desktop. Reduce load: one primary action per screen, progressive disclosure, smart defaults and pre-fill, chunk long forms into steps, favor recognition over recall, and persist state on interrupt or backgrounding. Keep working-set choices to about 5 (Miller's law, tighter on mobile), and remember that more choices slow decisions more than on desktop (Hick's law): start with 3-5 options, add a "More", order by frequency, and remember previous selections.

---

## 7. Touch Accessibility

Users with motor impairments may have tremors, use assistive input, have limited reach, need more time, and make accidental touches. Respond with generous targets (48 dp+), adjustable gesture timing, undo for destructive actions, and switch- and voice-control support. WCAG 2.2 (2.5.8): targets at least 24x24 CSS px with spacing, and 44x44 is the safer mobile floor, unless the target is inline, user-resizable, or essential. Every gesture needs an accessible alternative: swipe actions expose a menu, drag-and-drop offers select-then-move, pinch offers zoom buttons, force-touch offers long-press, shake offers a button.

---

## 8. Emotion in Touch

A premium feel comes from instant response, appropriate haptics, smooth 60 fps animation, correct physics, and restraint. Match feedback to emotion: success (haptic success plus a check), error (haptic error plus a shake), warning (haptic warning plus an attention color), delight (an unexpected smooth animation). Build trust through consistency (same action, same response), reliable feedback that never fails silently, and confirmation before destructive actions.

---
> Every touch is a conversation between user and device. Make it feel natural, responsive, and respectful of human fingers, not precise cursor points.
