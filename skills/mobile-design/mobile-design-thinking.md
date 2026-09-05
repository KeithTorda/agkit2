# Mobile Design Thinking

Choose mobile patterns for the project in front of you, not the pattern you have seen most often. Before building a screen, run the decomposition below and question any default you reach for.

## Question the defaults

Common AI defaults and the question that should precede each:

| Default | Question | Alternative to weigh |
|---------|----------|----------------------|
| Tab bar for everything | How many top-level destinations, and are they equal? | 3 or fewer: minimal tabs; 6+: drawer or hybrid |
| Redux for all state | How complex is the shared state? | Zustand or Jotai for shared client state; React Context only for rarely-changing values; TanStack Query for server state |
| Global state by default | Is this state really global? | Local state, lifted only when shared |
| FlatList as the list | Is this the New Architecture? | FlashList v2 is the default there |
| FAB bottom-right | Which hand, which reach? | Position for the primary flow and accessibility |
| Pull-to-refresh on every list | Does this data change on demand? | Only where a manual refresh helps |
| Bottom sheet for every modal | How much content and interaction? | Full-screen for complex tasks |
| BLoC for every Flutter app | Is the boilerplate worth it here? | Riverpod for less code |

If you chose something "because that's how it's always done", stop and name one alternative before deciding.

## Decompose the screen

For each screen, answer:

- Primary action: what is it, and is it reachable one-handed (thumb zone)?
- Touch targets: every tappable element at least 44 pt / 48 dp, with at least 8 pt spacing?
- Scrollable content: is it a list? Which list component, and why? Fixed height (so `getItemLayout` helps)?
- State: local, lifted, or global, and why?
- Platform differences: does iOS or Android need anything different here?
- Offline: should this screen work offline? What is cached?
- Performance: any heavy component, image, or animation to plan for?

## Analyze each gesture

Before adding a gesture:

- Discoverability: how does the user find it, and is there a visible button alternative? (Always provide one.)
- Platform meaning: what does this gesture already mean on iOS and on Android? Are you fighting a convention?
- Accessibility: can a motor-impaired user perform it? Is there a screen-reader and switch-control path?
- Conflicts: does it clash with system gestures (iOS edge-swipe back, Android back, home-indicator swipe)?
- Feedback: haptic, visual, or both on success?

## Think by project type

Different app types push different defaults; use these as starting points, not rules:

- E-commerce: tab bar (Home, Search, Cart, Account); product grids with cached images; cart persistence; secure, short checkout.
- Social / content: tab bar with a create action; infinite feeds; media upload queue; real-time notifications; feed cache and draft posts.
- Productivity / SaaS: drawer or adaptive navigation (tabs on phone, rail on tablet); data tables and forms; full offline editing with conflict resolution.
- Utility: minimal, often stack-only navigation; fast startup; core feature working offline; widgets and shortcuts.
- Media / streaming: tab bar; horizontal carousels and vertical feeds; preloading and buffering; background playback and download management.

## Honest self-check

Passing a checklist is not the goal; good mobile UX is. Ask the harder version of each check: not "is the target 44 pt" but "can the user reach it one-handed"; not "did I use FlashList" but "is the scroll smooth on a low-end device"; not "is there a loading state" but "does the user know how long to wait". If you cannot describe the project's platform, one default you are deliberately not using, and the area you will optimize, you do not understand it well enough yet: re-read the brief or ask.
