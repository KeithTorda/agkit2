# 8. Advanced Patterns

> **Impact:** VARIABLE
> **Focus:** Advanced patterns for specific cases that require careful implementation.

---

## Overview

Two rules for specific cases.

---

## Rule 8.1: Initialize App Once, Not Per Mount

**Impact:** LOW-MEDIUM  
**Tags:** initialization, useEffect, app-startup, side-effects  

Do not put app-wide initialization that must run once per app load inside `useEffect([])` of a component. Components can remount and effects will re-run. Use a module-level guard or top-level init in the entry module instead.

**Incorrect (runs twice in dev, re-runs on remount):**

```tsx
function Comp() {
  useEffect(() => {
    loadFromStorage()
    checkAuthToken()
  }, [])

  // ...
}
```

**Correct (once per app load):**

```tsx
let didInit = false

function Comp() {
  useEffect(() => {
    if (didInit) return
    didInit = true
    loadFromStorage()
    checkAuthToken()
  }, [])

  // ...
}
```

Reference: [Initializing the application](https://react.dev/learn/you-might-not-need-an-effect#initializing-the-application)

---

## Rule 8.2: `useEffectEvent` for Callbacks Read Inside Effects

**Impact:** LOW  
**Tags:** advanced, hooks, useEffectEvent, refs

When an effect calls a callback (a prop handler, a logger) that should always see the latest values but should not re-run the effect when it changes, wrap it in `useEffectEvent` (stable in React 19.2).

**Incorrect (re-subscribes or restarts whenever the parent passes a new function):**

```tsx
function useWindowEvent(event: string, handler: (e: Event) => void) {
  useEffect(() => {
    window.addEventListener(event, handler)
    return () => window.removeEventListener(event, handler)
  }, [event, handler])
}

function SearchInput({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState('')
  useEffect(() => {
    const timeout = setTimeout(() => onSearch(query), 300)
    return () => clearTimeout(timeout)
  }, [query, onSearch])   // restarts the debounce when onSearch changes
}
```

**Correct:**

```tsx
import { useEffect, useEffectEvent, useState } from 'react'

function useWindowEvent(event: string, handler: (e: Event) => void) {
  const onEvent = useEffectEvent(handler)
  useEffect(() => {
    window.addEventListener(event, onEvent)
    return () => window.removeEventListener(event, onEvent)
  }, [event])
}

function SearchInput({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState('')
  const onSearchEvent = useEffectEvent(onSearch)
  useEffect(() => {
    const timeout = setTimeout(() => onSearchEvent(query), 300)
    return () => clearTimeout(timeout)
  }, [query])
}
```

Effect Events are called only from inside effects; do not pass them to child components or other hooks. On React versions before 19.2, the older pattern is a ref updated in an effect (`handlerRef.current = handler`) and read inside the listener.
