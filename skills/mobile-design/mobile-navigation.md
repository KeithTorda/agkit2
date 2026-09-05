# Mobile Navigation Reference

> Navigation patterns, deep linking, back handling, and tab/stack/drawer decisions.
> Navigation is the skeleton of the app; get it wrong and everything feels broken.

---

## 1. Navigation Selection Decision Tree

```
WHAT TYPE OF APP?
        │
        ├── 3-5 top-level sections (equal importance)
        │   └── Tab Bar / Bottom Navigation (Social, E-commerce, Utility)
        │
        ├── Deep hierarchical content (drill down)
        │   └── Stack Navigation (Settings, Email folders)
        │
        ├── Many destinations (>5 top-level)
        │   └── Drawer Navigation (Gmail, complex enterprise)
        │
        ├── Single linear flow
        │   └── Stack only (wizard/onboarding: checkout, setup)
        │
        └── Tablet/Foldable
            └── Navigation Rail + List-Detail (Mail, Notes on iPad)
```

---

## 2. Tab Bar Navigation

Use a tab bar for 3-5 equally important top-level destinations the user switches between often, each with its own navigation stack. Avoid it for more than 5 destinations, clear hierarchy, or a linear sequence.

- iOS tab bar: 49 pt tall (plus home indicator), max 5 items, SF Symbols, labels always shown, tint for the active item.
- Android bottom navigation: 80 dp tall, 3-5 items, Material Symbols (24 dp), labels shown, pill indicator plus filled icon for active.

### Tab State Preservation

Each tab keeps its own navigation stack: drilling into Home, switching to Profile, and returning to Home must land back on the drilled-in screen, not the Home root. React Navigation gives each tab its own navigator; Flutter uses `IndexedStack`. Never reset a tab's stack on switch.

---

## 3. Stack Navigation

Push adds a screen, pop removes the top (back), replace swaps the current screen, reset clears the stack and sets a new root. New screens slide in from the trailing edge.

| Pattern | Use Case | Implementation |
|---------|----------|----------------|
| Simple Stack | Linear flow | Push each step |
| Nested Stack | Sections with sub-navigation | Stack inside a tab |
| Modal Stack | Focused tasks | Present modally |
| Auth Stack | Login vs main | Conditional root |

Back handling: iOS uses the interactive edge-swipe from the left plus an optional nav-bar button; Android uses the system back button/gesture with predictive back (Android 14+). Back always pops the stack, never hijack it, confirm before discarding unsaved data, and let deep links build a stack the user can back out of.

---

## 4. Drawer Navigation

Use a drawer for more than 5 destinations, less-frequent destinations, or a large screen with a persistent drawer; avoid it when 5 or fewer equally important destinations fit a tab bar (drawers hide navigation and hurt discoverability). Modal drawers slide over content with a scrim (hamburger trigger); permanent drawers stay visible on large screens; a navigation rail (80 dp) is the tablet-portrait option.

---

## 5. Modal Navigation

Push (horizontal slide, part of the hierarchy, back returns) versus modal (vertical slide, a separate self-contained task, dismiss returns). Use modals for creating content, settings, transactions, and quick actions.

| Type | iOS | Android | Use Case |
|------|-----|---------|----------|
| Sheet | `.sheet` | Bottom Sheet | Quick tasks |
| Full Screen | `.fullScreenCover` | Full Activity | Complex forms |
| Alert | Alert | Dialog | Confirmations |
| Action Sheet | Action Sheet | Menu / Bottom Sheet | Choose from options |

Let users dismiss modals by close button, swipe down (sheet), scrim tap (non-critical), or system back (Android); only block dismissal to protect unsaved data.

---

## 6. Deep Linking

Plan deep links from day one; retrofitting them forces a navigation refactor. They power push-notification navigation, sharing, marketing, search integration, and widgets.

URL structure mirrors navigation: `myapp://home/product/123/reviews` and the Universal/App Link `https://myapp.com/product/123`. Rules:

1. Full stack construction: a deep link to a product puts Home at the root and pushes Product, so back returns to Home.
2. Auth awareness: save the destination, send the user to login, then continue to it.
3. Invalid links: fall back to home with a message, never crash or blank-screen.
4. Stateful navigation: during an active session, push on top rather than blowing away the current stack.

---

## 7. Navigation State Persistence

Persist the current tab, list scroll positions, form drafts, and the recent stack; do not persist modal state, transient UI, stale data (refresh on return), or auth (use secure storage).

```javascript
// React Navigation state persistence
const [initialState, setInitialState] = useState();
useEffect(() => {
  (async () => {
    const saved = await AsyncStorage.getItem('NAV_STATE');
    if (saved) setInitialState(JSON.parse(saved));
  })();
}, []);

<NavigationContainer
  initialState={initialState}
  onStateChange={(state) => AsyncStorage.setItem('NAV_STATE', JSON.stringify(state))}
>
```

---

## 8. Transition Animations

Use platform defaults for most navigation (iOS: slide from trailing edge, modal from bottom, interactive swipe-back; Android: fade-through, shared-element hero animations). Customize only for brand identity or shared-element connections, keep it under 300 ms, and use defaults on performance-critical paths. Shared-element transitions: React Navigation shared-element libraries, Flutter `Hero`, SwiftUI `matchedGeometryEffect`, Compose shared-element transitions.

---

## 9. Navigation Anti-Patterns

| Anti-pattern | Problem | Fix |
|--------------|---------|-----|
| Inconsistent back | User cannot predict it | Always pop the stack |
| Hidden navigation | Features undiscoverable | Visible tab or drawer trigger |
| Deep nesting | User gets lost | Max 3-4 levels; breadcrumbs |
| Breaking swipe-back | iOS users frustrated | Never override the gesture |
| No deep links | Cannot share; broken notifications | Plan from the start |
| Tab stack reset | Work lost on switch | Preserve tab state |
| Modal for a primary flow | Cannot back-track | Use stack navigation |

AI tends to use modals for everything, forget tab-state preservation, skip deep linking, override platform back, and ignore predictive back (Android 14+). Use platform navigation patterns; do not reinvent navigation.

---
> Navigation is invisible when done right. Users should not think about how to get somewhere; if they notice navigation, something is wrong.
