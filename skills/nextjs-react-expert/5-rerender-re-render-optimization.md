# 5. Re-render Optimization

> **Impact:** MEDIUM
> **Focus:** Fewer wasted renders and no state drift. With the React Compiler on, most of this is about component structure, not memoization calls.

---

## Compiler first

Compiler-first when the React Compiler is enabled (`reactCompiler: true` in next.config / babel-plugin-react-compiler in Expo — the kit's templates enable it); check the flag before removing manual memo. The compiler memoizes components, hooks, and JSX automatically, so:

- Do not write `useMemo`, `useCallback`, or `React.memo` by default. They add noise and can hide real bugs (missing dependencies).
- Add manual memoization only when (a) the compiler bails out on a specific component (React DevTools shows a "Memo" badge on compiled components; `eslint-plugin-react-hooks` reports the code the compiler cannot handle), or (b) profiling shows a hot path the compiler did not cover, such as a very expensive computation whose inputs are stable.
- The compiler cannot fix structural problems: state stored in the wrong place, effects that set state, context values that change on every render, or components that subscribe to values they do not need. The rules below target those.
- If the project has the compiler off (older codebase, `reactCompiler: false`), the same structural rules apply first; add memo only after measuring.

Verify the compiler is active before adding or removing memo: `grep reactCompiler next.config.*` (Expo: `babel-plugin-react-compiler` in `babel.config.js`) and look for `babel-plugin-react-compiler` in the lockfile.

---

## Rule 5.1: Calculate Derived State During Rendering

**Impact:** MEDIUM  
**Tags:** rerender, derived-state, useEffect, state  

If a value can be computed from current props or state, do not store it in state or update it in an effect. Derive it during render; that removes an extra render per change and a whole class of drift bugs.

**Incorrect (redundant state and effect, renders twice):**

```tsx
function Form() {
  const [firstName, setFirstName] = useState('First')
  const [lastName, setLastName] = useState('Last')
  const [fullName, setFullName] = useState('')

  useEffect(() => {
    setFullName(firstName + ' ' + lastName)
  }, [firstName, lastName])

  return <p>{fullName}</p>
}
```

**Correct (derive during render):**

```tsx
function Form() {
  const [firstName, setFirstName] = useState('First')
  const [lastName, setLastName] = useState('Last')
  const fullName = firstName + ' ' + lastName
  return <p>{fullName}</p>
}
```

Expensive derivations (filtering thousands of rows) are memoized by the compiler; only reach for `useMemo` when profiling shows the compiler skipped the component.

Reference: [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect)

---

## Rule 5.2: Reset State with a `key`, Not an Effect

**Impact:** MEDIUM  
**Tags:** rerender, key, state-reset, useEffect  

When a component must start over for a new entity (a new user profile, a new document), do not clear its state in an effect that watches the id. Give the component a `key` so React remounts it with fresh state.

**Incorrect (effect resets state one render late, and the stale render is visible):**

```tsx
function ProfilePage({ userId }: { userId: string }) {
  const [comment, setComment] = useState('')
  useEffect(() => {
    setComment('')
  }, [userId])
  // ...
}
```

**Correct (remount on identity change):**

```tsx
function ProfilePage({ userId }: { userId: string }) {
  return <Profile userId={userId} key={userId} />
}

function Profile({ userId }: { userId: string }) {
  const [comment, setComment] = useState('')
  // ...
}
```

The same trick resets an uncontrolled form after submit (`key={submitCount}`) and restarts an animation.

---

## Rule 5.3: Split Context by Update Frequency

**Impact:** MEDIUM  
**Tags:** rerender, context, providers  

Every consumer of a context re-renders when the context value changes, regardless of which field it reads. Put fast-changing values (current user input, scroll position, mouse) in a different context from stable values (theme, session, config), and keep setters in their own context so components that only dispatch do not re-render on state changes.

**Incorrect (one context, every consumer renders on every keystroke):**

```tsx
const AppContext = createContext({ theme, user, query, setQuery })
```

**Correct (split by how often the value changes):**

```tsx
const ThemeContext = createContext<Theme>('light')      // rarely changes
const SessionContext = createContext<Session | null>(null)
const SearchQueryContext = createContext('')             // changes per keystroke
const SearchDispatchContext = createContext<(q: string) => void>(() => {})
```

The compiler keeps the provider `value` object stable between renders when its inputs are unchanged, so you no longer need `useMemo` around it; the split is still needed because it is about *which* consumers wake up. For app-wide client state with many fine-grained readers, a store with selectors (Zustand) avoids the problem entirely.

---

## Rule 5.4: Defer State Reads to the Usage Point

**Impact:** MEDIUM  
**Tags:** rerender, searchParams, subscription  

Do not subscribe a component to dynamic state (`useSearchParams`, a store, `localStorage`) if the value is only read inside a callback.

**Incorrect (subscribes to every searchParams change):**

```tsx
function ShareButton({ chatId }: { chatId: string }) {
  const searchParams = useSearchParams()
  const handleShare = () => shareChat(chatId, { ref: searchParams.get('ref') })
  return <button onClick={handleShare}>Share</button>
}
```

**Correct (reads on demand, no subscription):**

```tsx
function ShareButton({ chatId }: { chatId: string }) {
  const handleShare = () => {
    const ref = new URLSearchParams(window.location.search).get('ref')
    shareChat(chatId, { ref })
  }
  return <button onClick={handleShare}>Share</button>
}
```

---

## Rule 5.5: Subscribe to Derived Booleans, Not Continuous Values

**Impact:** MEDIUM  
**Tags:** rerender, derived-state, media-query  

Subscribe to the boolean you branch on instead of the raw continuous value.

**Incorrect (re-renders on every pixel):**

```tsx
function Sidebar() {
  const width = useWindowWidth()
  const isMobile = width < 768
  return <nav className={isMobile ? 'mobile' : 'desktop'} />
}
```

**Correct (re-renders only when the boolean flips):**

```tsx
function Sidebar() {
  const isMobile = useMediaQuery('(max-width: 767px)') // useSyncExternalStore over matchMedia
  return <nav className={isMobile ? 'mobile' : 'desktop'} />
}
```

The same applies to effect dependencies: depend on `user.id`, not `user`; on `isMobile`, not `width`.

---

## Rule 5.6: Put Interaction Logic in Event Handlers

**Impact:** MEDIUM  
**Tags:** rerender, useEffect, events, side-effects  

If a side effect is caused by a user action (submit, click, drag), run it in that handler. Modelling the action as state + effect re-runs the effect on unrelated changes and can duplicate the action.

**Incorrect:**

```tsx
function Form() {
  const [submitted, setSubmitted] = useState(false)
  const theme = useContext(ThemeContext)
  useEffect(() => {
    if (submitted) {
      post('/api/register')
      showToast('Registered', theme)
    }
  }, [submitted, theme])
  return <button onClick={() => setSubmitted(true)}>Submit</button>
}
```

**Correct:**

```tsx
function Form() {
  const theme = useContext(ThemeContext)
  function handleSubmit() {
    post('/api/register')
    showToast('Registered', theme)
  }
  return <button onClick={handleSubmit}>Submit</button>
}
```

For form submissions in Next.js prefer a Server Action wired through `<form action={...}>` and `useActionState`, which gives pending and error state without any effect.

Reference: [Should this code move to an event handler?](https://react.dev/learn/removing-effect-dependencies#should-this-code-move-to-an-event-handler)

---

## Rule 5.7: Use Functional setState Updates

**Impact:** MEDIUM  
**Tags:** react, hooks, useState, closures  

When the next state depends on the previous one, pass a function to the setter. This is a correctness rule (no stale closures in async code or batched updates), not a memoization trick.

```tsx
// Stale closure risk: `items` captured when the handler was created
setItems([...items, ...newItems])

// Always operates on the latest state
setItems((curr) => [...curr, ...newItems])
```

Direct updates are fine for static values (`setCount(0)`) or values derived only from arguments (`setName(newName)`).

---

## Rule 5.8: Use Lazy State Initialization

**Impact:** MEDIUM  
**Tags:** react, hooks, useState, initialization  

Pass a function to `useState` for expensive initial values. Without it the initializer expression runs on every render even though the result is only used once.

```tsx
// Runs buildSearchIndex on every render
const [index, setIndex] = useState(buildSearchIndex(items))

// Runs once
const [index, setIndex] = useState(() => buildSearchIndex(items))

// Reading storage once
const [settings, setSettings] = useState(() => {
  try {
    const stored = localStorage.getItem('settings')
    return stored ? JSON.parse(stored) : {}
  } catch {
    return {}
  }
})
```

Skip the function form for primitives, direct prop references, and cheap literals.

---

## Rule 5.9: Use Transitions for Non-Urgent Updates

**Impact:** MEDIUM  
**Tags:** rerender, transitions, startTransition  

Mark expensive, non-urgent state updates as transitions so typing and clicking stay responsive while React renders the heavy part in the background.

**Incorrect (the filtered list blocks the input on every keystroke):**

```tsx
function Search({ items }: { items: Item[] }) {
  const [query, setQuery] = useState('')
  const results = filterThousands(items, query)
  return (
    <>
      <input value={query} onChange={(e) => setQuery(e.target.value)} />
      <Results items={results} />
    </>
  )
}
```

**Correct (input updates immediately, results render as a transition):**

```tsx
import { useState, useTransition } from 'react'

function Search({ items }: { items: Item[] }) {
  const [query, setQuery] = useState('')
  const [deferredQuery, setDeferredQuery] = useState('')
  const [isPending, startTransition] = useTransition()

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const next = e.target.value
    setQuery(next)                                  // urgent
    startTransition(() => setDeferredQuery(next))   // non-urgent
  }

  const results = filterThousands(items, deferredQuery)
  return (
    <>
      <input value={query} onChange={handleChange} />
      <Results items={results} style={{ opacity: isPending ? 0.6 : 1 }} />
    </>
  )
}
```

`useDeferredValue(query)` is the shorter form when you only need the deferred copy.

**Scroll-linked UI is not a transition case.** Storing `window.scrollY` in state, even inside `startTransition`, re-renders on every frame. Use CSS scroll-driven animations for progress bars and reveals:

```css
.progress {
  animation: grow linear both;
  animation-timeline: scroll(root);
}
@keyframes grow { from { transform: scaleX(0) } to { transform: scaleX(1) } }
```

or `useScroll` from `motion/react`, which writes to a `MotionValue` and updates styles outside React renders:

```tsx
'use client'
import { motion, useScroll } from 'motion/react'

export function ScrollProgress() {
  const { scrollYProgress } = useScroll()
  return <motion.div className="progress" style={{ scaleX: scrollYProgress }} />
}
```

---

## Rule 5.10: Use `useRef` for Transient Values

**Impact:** MEDIUM  
**Tags:** rerender, useRef, state  

Values that change many times per second and do not affect what React renders (pointer position, timers, in-flight flags) belong in a ref, with the DOM updated imperatively. Updating a ref does not re-render.

**Incorrect (renders on every mousemove):**

```tsx
function Tracker() {
  const [lastX, setLastX] = useState(0)
  useEffect(() => {
    const onMove = (e: MouseEvent) => setLastX(e.clientX)
    window.addEventListener('mousemove', onMove)
    return () => window.removeEventListener('mousemove', onMove)
  }, [])
  return <div style={{ position: 'fixed', left: lastX, width: 8, height: 8, background: 'black' }} />
}
```

**Correct (no re-render):**

```tsx
function Tracker() {
  const dotRef = useRef<HTMLDivElement>(null)
  useEffect(() => {
    const onMove = (e: MouseEvent) => {
      if (dotRef.current) dotRef.current.style.transform = `translateX(${e.clientX}px)`
    }
    window.addEventListener('mousemove', onMove)
    return () => window.removeEventListener('mousemove', onMove)
  }, [])
  return <div ref={dotRef} style={{ position: 'fixed', left: 0, width: 8, height: 8, background: 'black' }} />
}
```

For anything animated, `motion/react` `MotionValue`s are the same idea with springs and gestures built in.

---

## Rule 5.11: When Manual Memoization Is Still Right

**Impact:** LOW  
**Tags:** memo, useMemo, useCallback, compiler-bailout  

Only after confirming the compiler bailed out or profiling shows a hot path:

- `React.memo` for a leaf that receives stable props from a parent the compiler could not compile (for example, code the compiler skipped because it mutates values after creation). Give optional object or function props a module-level default (`const NOOP = () => {}`) or the memo never hits.
- `useMemo` for a genuinely expensive computation with stable inputs, never for simple expressions with primitive results; the hook overhead exceeds the work.
- `useCallback` only when the callback is passed to a memoized child or used as an effect dependency, and the compiler did not stabilize it.

Remove manual memo when the compiler is enabled for that file; keep the project's compiler ESLint rules on so bailouts are visible.
