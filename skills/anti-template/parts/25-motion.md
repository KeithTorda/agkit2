---
part: 25
title: Motion with purpose and character
covers: choreography, entrance, scroll, hover, parallax, counters, loops, loading, transitions, timing, reduced motion, libraries
---

# 25 - Motion with purpose and character

Read when adding or reviewing animation. Motion follows the user-approved style and references. There is no universal "no motion" default, required animation level, or rule that every redesign needs more movement.

## Choose a motion role

Motion can communicate state, continuity, hierarchy, spatial relationships, narrative, atmosphere, or brand personality. A quiet utility page may need only feedback. A campaign may intentionally use rich choreography, expressive type, parallax, 3D, or ambient movement. Identify the role and execute it coherently rather than adding unrelated effects from several demos.

Plan emphasis, sequence, distance, timing, easing, and how motion settles. Not every element needs a different animation. Repeated treatments can establish a consistent language. Long, gentle motion and quick feedback serve different purposes; use timing that fits the event, content, input method, and audience, without a universal duration cap.

## Entrance, scroll, and page transitions

Entrance and scroll reveals can make a composition engaging and direct attention. Ensure essential content remains available when scripts fail, observers do not fire, the user jumps to an anchor, the page prints, or reduced motion is enabled. Do not leave text at opacity zero indefinitely. Revisit trigger positions on short screens and keyboard navigation.

Parallax, pinned scenes, horizontal storytelling, and scroll-linked transformations are valid when selected. Test real performance, reading order, reverse scrolling, focus, and a useful reduced-motion alternative. Avoid taking away expected scrolling without a clear, usable experience. A motion concept should not require an unrelated interaction library just to copy a reference.

Route and component transitions should preserve state, focus, and a readable final frame. Handle interruption, rapid navigation, and unmounting. A transition must not leave a transparent overlay intercepting input or a stale page focus target.

## Hover, press, counters, and text effects

Hover lift, scale, tilt, glow, and cursor effects may enrich an interactive composition. Provide meaningful keyboard and touch behavior; no required action may depend solely on hover. Leave room for transforms and avoid accidental neighboring collisions.

Counters, rolling digits, typing, scramble, and rotating headlines can work as chosen presentation effects. Keep a complete semantic value or text available to assistive technology and avoid announcing each frame. Essential financial or operational values must be quickly readable and accurate. Do not animate to invented statistics or simulate real generation on static content without an appropriate presentation context.

## Ambient loops and celebration

Marquees, moving gradients, particles, video, logo animation, and celebratory effects are available tools. Assess distraction, battery, transfer, and frame cost on priority devices. Automatically moving content that meets the applicable pause/stop/hide criteria needs a usable control. Avoid unsafe flashing; merely lowering duration is not a reliable flash-safety test.

Celebration should fit the event, brand, and frequency. Confetti may suit a milestone; it may burden a cashier repeating a transaction all day. Feedback must communicate success even if the effect is skipped. Presence and live-status pulses must correspond to real state rather than fabricate urgency.

## Loading and implementation

Loading indicators should represent actual waiting. Use real measured progress or an indeterminate state, not a fake timer. Delayed indicators and skeletons can reduce flashing when based on actual latency and layout. Do not add artificial waits solely to showcase animation.

Choose CSS, Web Animations, a small library, or a richer runtime from the required behavior and existing stack. Clean up listeners, observers, timers, and animation instances. Profile expensive paint/filter/3D effects where they are material. Avoid a broad global reduced-motion rule that breaks JavaScript completion events or hides content; provide explicit settled states and reduced alternatives.

## Review

Inspect start, middle, settled, interrupted, reverse-scroll where relevant, and reduced-motion states. Check keyboard, touch, content availability, cleanup, and actual performance. Preserve the selected motion direction while fixing concrete problems.
