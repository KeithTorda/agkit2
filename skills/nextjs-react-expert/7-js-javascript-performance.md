# 7. JavaScript Performance

> **Impact:** LOW-MEDIUM
> **Focus:** Micro-optimizations for hot paths (render loops, event handlers, large collections). Measure first; most code never needs these.

---

## Rule 7.1: Avoid Layout Thrashing

**Impact:** MEDIUM  
**Tags:** dom, reflow, layout-thrashing  

Reading a layout property (`offsetWidth`, `getBoundingClientRect()`, `getComputedStyle()`) between style writes forces a synchronous reflow each time. Batch all writes, then read once; or batch all reads, then write.

```typescript
// Incorrect: write, read, write, read = two forced reflows
el.style.width = '100px'
const w = el.offsetWidth
el.style.height = '200px'
const h = el.offsetHeight

// Correct: writes together, one read
el.style.width = '100px'
el.style.height = '200px'
const { width, height } = el.getBoundingClientRect()
```

In React, prefer toggling a class (`className={isHighlighted ? 'highlighted' : ''}`) over imperative style writes in effects. See [what forces layout](https://gist.github.com/paulirish/5d52fb081b3570c81e3a).

---

## Rule 7.2: Build Index Maps for Repeated Lookups

**Impact:** LOW-MEDIUM  
**Tags:** map, indexing  

Repeated `.find()` by the same key is O(n) per lookup. Build a `Map` once.

```typescript
// Incorrect: O(n) per order
orders.map(order => ({ ...order, user: users.find(u => u.id === order.userId) }))

// Correct: O(1) per order
const userById = new Map(users.map(u => [u.id, u]))
orders.map(order => ({ ...order, user: userById.get(order.userId) }))
```

Same idea for membership checks: `new Set(allowedIds).has(id)` instead of `allowedIds.includes(id)`.

---

## Rule 7.3: Cache Repeated Function Calls and Storage Reads

**Impact:** MEDIUM  
**Tags:** cache, memoization, localStorage, cookies  

When a pure function is called many times with the same input during render (`slugify(project.name)` for 100 rows), cache results in a module-level `Map`; it works in utilities and handlers, not only components.

```typescript
const slugCache = new Map<string, string>()
export function cachedSlugify(text: string) {
  let slug = slugCache.get(text)
  if (slug === undefined) {
    slug = slugify(text)
    slugCache.set(text, slug)
  }
  return slug
}
```

`localStorage`, `sessionStorage`, and `document.cookie` are synchronous and slow; cache reads in memory and keep the cache in sync on writes. Invalidate when storage can change externally:

```typescript
window.addEventListener('storage', (e) => { if (e.key) storageCache.delete(e.key) })
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible') storageCache.clear()
})
```

Reference: [How we made the Vercel Dashboard twice as fast](https://vercel.com/blog/how-we-made-the-vercel-dashboard-twice-as-fast)

---

## Rule 7.4: Combine Multiple Array Iterations

**Impact:** LOW-MEDIUM  
**Tags:** arrays, loops  

Three `.filter()` calls iterate three times. In hot paths, one loop:

```typescript
const admins: User[] = [], testers: User[] = [], inactive: User[] = []
for (const user of users) {
  if (user.isAdmin) admins.push(user)
  if (user.isTester) testers.push(user)
  if (!user.isActive) inactive.push(user)
}
```

---

## Rule 7.5: Cheap Checks Before Expensive Comparisons

**Impact:** MEDIUM-HIGH  
**Tags:** arrays, comparison, early-return  

Compare lengths before sorting or deep-comparing arrays; return early from validation loops on the first failure.

```typescript
function hasChanges(current: string[], original: string[]) {
  if (current.length !== original.length) return true
  const a = current.toSorted(), b = original.toSorted()
  for (let i = 0; i < a.length; i++) if (a[i] !== b[i]) return true
  return false
}
```

---

## Rule 7.6: Hoist RegExp Creation

**Impact:** LOW-MEDIUM  
**Tags:** regexp  

Do not build a `RegExp` inside render. Hoist constant patterns to module scope; for patterns derived from props, escape the input and let the compiler memoize the derivation.

```tsx
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function Highlighter({ text, query }: Props) {
  const regex = new RegExp(`(${escapeRegex(query)})`, 'gi') // compiler memoizes on query
  return <>{text.split(regex).map(renderPart)}</>
}
```

Global regexes (`/g`) carry mutable `lastIndex` state; do not share one instance across `test()` calls.

---

## Rule 7.7: Use a Loop for Min/Max Instead of Sort

**Impact:** LOW  
**Tags:** arrays, sorting  

Finding the latest item is O(n) with a loop; sorting is O(n log n) and copies the array. `Math.max(...arr)` throws on very large arrays because of argument-count limits, so use the loop for unbounded input.

```typescript
function latest(projects: Project[]) {
  if (projects.length === 0) return null
  let best = projects[0]
  for (let i = 1; i < projects.length; i++) {
    if (projects[i].updatedAt > best.updatedAt) best = projects[i]
  }
  return best
}
```

---

## Rule 7.8: Use `toSorted()` Instead of `sort()` for Immutability

**Impact:** MEDIUM-HIGH  
**Tags:** arrays, immutability, react-state  

`.sort()` mutates in place, which corrupts React props and state and causes stale-closure bugs. `.toSorted()`, `.toReversed()`, `.toSpliced()`, and `.with()` return new arrays and are available in all current browsers and Node 20+.

```typescript
// Incorrect: mutates the users prop
const sorted = users.sort((a, b) => a.name.localeCompare(b.name))

// Correct
const sorted = users.toSorted((a, b) => a.name.localeCompare(b.name))
```
