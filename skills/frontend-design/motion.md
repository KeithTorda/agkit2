# Motion (frontend-design §5, §5.A-§5.D)

Read when: `MOTION_INTENSITY` ≥ 6, or the brief asks for scroll, pinned, or animated sections. SKILL.md core comes first (§1 dials, §5 motivated-or-absent rule, §5.E feedback on action).

## 5. Motion principles
- Perpetual loops (pulse, typewriter, shimmer, float) only where "live" means something (status, feeds, AI-feel), never on every card. Spring physics (`type: "spring", stiffness: 100, damping: 20`), not linear easing.
- Magnetic / pointer physics only at `MOTION_INTENSITY > 5` for premium / playful / agency briefs, via motion values (design-systems.md §3.B). One marquee per page at most.
- **One animation library per component.** A component imports `motion/react` or `gsap`, never both; they fight over the same frames. GSAP and Three.js live in dedicated client leaves with cleanup. Reduced motion is handled by the library in use: `useReducedMotion()` for Motion, `gsap.matchMedia()` for GSAP, `@media (prefers-reduced-motion)` for CSS; every animation above `MOTION_INTENSITY 3` degrades under it and cleans up on unmount.

### 5.A Sticky stack (GSAP, pin/scrub)
The one GSAP recipe worth memorising; §5.B is a variant of it.
```tsx
"use client";
gsap.registerPlugin(ScrollTrigger);
useEffect(() => {
  const mm = gsap.matchMedia();                                   // reduced-motion guard
  mm.add("(prefers-reduced-motion: no-preference)", () => {
    gsap.timeline({ scrollTrigger: { trigger: wrap.current, start: "top top",
      end: () => `+=${panels.length * 100}%`, pin: true, scrub: 1, invalidateOnRefresh: true } })
      .to(panels, { yPercent: -100, stagger: 1, ease: "none" }); // each panel scrolls over the last
  });
  return () => mm.revert();                                       // cleanup, always
}, []);
```
Panels are absolutely positioned, full-height (`h-[100dvh]`), inside a `relative overflow-hidden` wrap. No `scroll` listeners; ScrollTrigger owns the scroll.

### 5.B Horizontal pan (GSAP, pin/scrub)
Same structure as §5.A (`matchMedia` reduced-motion guard, `pin: true`, `scrub: 1`, `invalidateOnRefresh`, `mm.revert()` on cleanup) with two changes: the track is `flex h-[100dvh] items-center` inside an `overflow-hidden` section, and the tween is `x: () => -(track.scrollWidth - window.innerWidth)` with `end: () => \`+=${distance()}\`` so the scroll length equals the horizontal travel. Pin before the first slide moves (`start: "top top"`).

### 5.C Reveal stagger (Motion, no pinning)
For "items appear as they enter", prefer `motion/react` over GSAP: lighter, no ScrollTrigger.
```tsx
"use client";
import { motion, useReducedMotion } from "motion/react";

export function RevealStagger({ items }: { items: string[] }) {
  const reduce = useReducedMotion();
  return (
    <ul className="grid gap-6">
      {items.map((item, i) => (
        <motion.li key={item} initial={reduce ? false : { opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, amount: 0.3 }}
          transition={{ duration: 0.6, delay: i * 0.06, ease: [0.16, 1, 0.3, 1] }}>
          {item}
        </motion.li>
      ))}
    </ul>
  );
}
```

### 5.D Forbidden patterns
- `window.addEventListener("scroll", ...)` and `window.scrollY` in React state: runs every frame, re-renders the tree (`grep -rn "addEventListener(.scroll"` before delivering). Use `useScroll()` from `motion/react`, GSAP ScrollTrigger, `IntersectionObserver`, or CSS scroll-driven animations (`animation-timeline: view()`).
- `requestAnimationFrame` loops that set React state: use motion values.
- Animating `top / left / width / height`: animate `transform` and `opacity` only; `will-change` only on elements that actually animate.
- `layout` / `layoutId` props on static content "for safety": they cost measurement. `staggerChildren` parents and children in the same client tree.
- Grain and noise filters only on a `fixed inset-0 pointer-events-none` layer, never on scrolling containers.
