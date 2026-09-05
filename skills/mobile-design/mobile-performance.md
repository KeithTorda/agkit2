# Mobile Performance Reference

> Deep dive into React Native and Flutter performance optimization, 60fps animations, memory management, and battery considerations.
> **This file covers the #1 area where AI-generated code FAILS.**

---

## 1. The Mobile Performance Mindset

### Why Mobile Performance is Different

```
DESKTOP:                          MOBILE:
├── Unlimited power               ├── Battery matters
├── Abundant RAM                  ├── RAM is shared, limited
├── Stable network                ├── Network is unreliable
├── CPU always available          ├── CPU throttles when hot
└── User expects fast anyway      └── User expects INSTANT
```

### Performance Budget Concept

```
Every frame must complete in:
├── 60fps → 16.67ms per frame
├── 120fps (ProMotion) → 8.33ms per frame

If your code takes longer:
├── Frame drops → Janky scroll/animation
├── User perceives as "slow" or "broken"
└── They WILL uninstall your app
```

---

## 2. React Native Performance

### The #1 mistake: ScrollView for lists

```javascript
// Wrong: renders every item at once
<ScrollView>
  {items.map(item => (
    <ItemComponent key={item.id} item={item} />
  ))}
</ScrollView>

// Why it's catastrophic:
// ├── Renders ALL items immediately (1000 items = 1000 renders)
// ├── Memory explodes
// ├── Initial render takes seconds
// └── Scroll becomes janky

// Use a virtualised list: FlashList v2 for long lists (FlatList is acceptable for short fixed lists)
<FlatList
  data={items}
  renderItem={renderItem}
  keyExtractor={item => item.id}
/>
```

### FlashList v2 (the default)

FlashList v2 (built for the New Architecture) is the default list on React Native; it recycles views and does not need size estimates.

```tsx
import { FlashList } from "@shopify/flash-list";

<FlashList
  data={items}
  renderItem={({ item }) => <ListItem item={item} />}
  keyExtractor={(item) => item.id}   // stable id from data, never the index
/>
```

v2 removed `estimatedItemSize` (and the other `estimated*` props); it measures automatically. Do not pass them. `masonry` is a prop now, not a separate component. Compiler-first when the React Compiler is enabled (`babel-plugin-react-compiler` in Expo — the kit's templates enable it); check the flag before removing manual memo. With the compiler on you usually do not wrap the row in `React.memo` or `renderItem` in `useCallback`; add them only if profiling shows the compiler bailed out.

### FlatList (short fixed lists, or when FlashList is unavailable)

```tsx
<FlatList
  data={items}
  renderItem={({ item }) => <ListItem item={item} />}
  keyExtractor={(item) => item.id}          // stable id, not index
  getItemLayout={(_, index) => ({ length: ITEM_HEIGHT, offset: ITEM_HEIGHT * index, index })} // fixed height only
  removeClippedSubviews                       // Android: detach off-screen
  maxToRenderPerBatch={10}
  windowSize={5}
/>
```

| Prop | What it prevents |
|------|------------------|
| Stable `keyExtractor` | Wrong item recycling on reorder |
| `getItemLayout` (fixed height) | Async layout measurement, jank on fast scroll |
| `removeClippedSubviews` | Memory held by off-screen rows |
| `maxToRenderPerBatch` / `windowSize` | Main-thread blocking and excess memory |

The `keyExtractor`, `getItemLayout`, and cleanup are correctness and layout settings, not memoization; keep them regardless of the compiler.

### Animation Performance

```javascript
// ❌ JS-driven animation (blocks JS thread)
Animated.timing(value, {
  toValue: 1,
  duration: 300,
  useNativeDriver: false, // BAD!
}).start();

// ✅ Native-driver animation (runs on UI thread)
Animated.timing(value, {
  toValue: 1,
  duration: 300,
  useNativeDriver: true, // GOOD!
}).start();

// Native driver supports ONLY:
// ├── transform (translate, scale, rotate)
// └── opacity
// 
// Does NOT support:
// ├── width, height
// ├── backgroundColor
// ├── borderRadius changes
// └── margin, padding
```

### Reanimated 4 for complex animations

```tsx
// For anything the native driver can't handle, use Reanimated 4 (New Architecture)
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
} from 'react-native-reanimated';

const Component = () => {
  const offset = useSharedValue(0);

  const animatedStyles = useAnimatedStyle(() => ({
    transform: [{ translateX: withSpring(offset.value) }],
  }));

  return <Animated.View style={animatedStyles} />;
};

// Benefits:
// ├── Runs on the UI thread (smooth even when JS is busy)
// ├── Animates any property, including layout and colors
// ├── Gesture-driven animations via react-native-gesture-handler
// └── Reanimated 4 also supports CSS-style transitions on the New Architecture
```

### Memory Leak Prevention

```javascript
// ❌ Memory leak: uncleared interval
useEffect(() => {
  const interval = setInterval(() => {
    fetchData();
  }, 5000);
  // Missing cleanup!
}, []);

// ✅ Proper cleanup
useEffect(() => {
  const interval = setInterval(() => {
    fetchData();
  }, 5000);
  
  return () => clearInterval(interval); // CLEANUP!
}, []);

// Common memory leak sources:
// ├── Timers (setInterval, setTimeout)
// ├── Event listeners
// ├── Subscriptions (WebSocket, PubSub)
// ├── Async operations that update state after unmount
// └── Image caching without limits
```

### React Native Performance Checklist

```markdown
## Before Every List
- [ ] Using FlashList v2 or FlatList (NOT ScrollView)
- [ ] keyExtractor uses a stable ID (NOT the index)
- [ ] getItemLayout provided for fixed-height FlatList rows
- [ ] Manual memo only if profiling shows the compiler bailed out

## Before Every Animation
- [ ] useNativeDriver: true for Animated, or Reanimated 4 for complex cases
- [ ] Only animating transform/opacity on the native driver
- [ ] Tested on a low-end Android device

## Before Any Release
- [ ] console.log statements removed
- [ ] Cleanup functions in all useEffects
- [ ] No memory leaks (test with profiler)
- [ ] Tested in release build (not dev)
```

---

## 3. Flutter Performance

### The #1 mistake: setState overuse

```dart
// ❌ WRONG: setState rebuilds ENTIRE widget tree
class BadCounter extends StatefulWidget {
  @override
  State<BadCounter> createState() => _BadCounterState();
}

class _BadCounterState extends State<BadCounter> {
  int _counter = 0;
  
  void _increment() {
    setState(() {
      _counter++; // This rebuilds EVERYTHING below!
    });
  }
  
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Counter: $_counter'),
        ExpensiveWidget(), // Rebuilds unnecessarily!
        AnotherExpensiveWidget(), // Rebuilds unnecessarily!
      ],
    );
  }
}
```

### The `const` Constructor Revolution

```dart
// ✅ CORRECT: const prevents rebuilds

class GoodCounter extends StatefulWidget {
  const GoodCounter({super.key}); // CONST constructor!
  
  @override
  State<GoodCounter> createState() => _GoodCounterState();
}

class _GoodCounterState extends State<GoodCounter> {
  int _counter = 0;
  
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Counter: $_counter'),
        const ExpensiveWidget(), // Won't rebuild!
        const AnotherExpensiveWidget(), // Won't rebuild!
      ],
    );
  }
}

// RULE: Add `const` to EVERY widget that doesn't depend on state
```

### Targeted State Management

```dart
// ❌ setState rebuilds whole tree
setState(() => _value = newValue);

// ✅ ValueListenableBuilder: surgical rebuilds
class TargetedState extends StatelessWidget {
  final ValueNotifier<int> counter = ValueNotifier(0);
  
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // Only this rebuilds when counter changes
        ValueListenableBuilder<int>(
          valueListenable: counter,
          builder: (context, value, child) => Text('$value'),
          child: const Icon(Icons.star), // Won't rebuild!
        ),
        const ExpensiveWidget(), // Never rebuilds
      ],
    );
  }
}
```

### Riverpod/Provider Best Practices

```dart
// ❌ WRONG: Reading entire provider in build
Widget build(BuildContext context) {
  final state = ref.watch(myProvider); // Rebuilds on ANY change
  return Text(state.name);
}

// ✅ CORRECT: Select only what you need
Widget build(BuildContext context) {
  final name = ref.watch(myProvider.select((s) => s.name));
  return Text(name); // Only rebuilds when name changes
}
```

### ListView Optimization

```dart
// ❌ WRONG: ListView without builder (renders all)
ListView(
  children: items.map((item) => ItemWidget(item)).toList(),
)

// ✅ CORRECT: ListView.builder (lazy rendering)
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) => ItemWidget(items[index]),
  // Additional optimizations:
  itemExtent: 56, // Fixed height = faster layout
  cacheExtent: 100, // Pre-render distance
)

// ✅ EVEN BETTER: ListView.separated for dividers
ListView.separated(
  itemCount: items.length,
  itemBuilder: (context, index) => ItemWidget(items[index]),
  separatorBuilder: (context, index) => const Divider(),
)
```

### Image Optimization

```dart
// ❌ WRONG: No caching, full resolution
Image.network(url)

// ✅ CORRECT: Cached with proper sizing
CachedNetworkImage(
  imageUrl: url,
  width: 100,
  height: 100,
  fit: BoxFit.cover,
  memCacheWidth: 200, // Cache at 2x for retina
  memCacheHeight: 200,
  placeholder: (context, url) => const Skeleton(),
  errorWidget: (context, url, error) => const Icon(Icons.error),
)
```

### Dispose Pattern

```dart
class MyWidget extends StatefulWidget {
  @override
  State<MyWidget> createState() => _MyWidgetState();
}

class _MyWidgetState extends State<MyWidget> {
  late final StreamSubscription _subscription;
  late final AnimationController _controller;
  late final TextEditingController _textController;
  
  @override
  void initState() {
    super.initState();
    _subscription = stream.listen((_) {});
    _controller = AnimationController(vsync: this);
    _textController = TextEditingController();
  }
  
  @override
  void dispose() {
    // ALWAYS dispose in reverse order of creation
    _textController.dispose();
    _controller.dispose();
    _subscription.cancel();
    super.dispose();
  }
  
  @override
  Widget build(BuildContext context) => Container();
}
```

### Flutter Performance Checklist

```markdown
## Before Every Widget
- [ ] const constructor added (if no runtime args)
- [ ] const keywords on static children
- [ ] Minimal setState scope
- [ ] Using selectors for provider watches

## Before Every List
- [ ] Using ListView.builder (NOT ListView with children)
- [ ] itemExtent provided (if fixed height)
- [ ] Image caching with size limits

## Before Any Animation
- [ ] Impeller renderer enabled (default on current Flutter)
- [ ] Avoiding Opacity widget (use FadeTransition)
- [ ] TickerProviderStateMixin for AnimationController

## Before Any Release
- [ ] All dispose() methods implemented
- [ ] No print() in production
- [ ] Tested in profile/release mode
- [ ] DevTools performance overlay checked
```

---

## 4. Animation Performance (Both Platforms)

### The 60fps Imperative

```
Human eye detects:
├── < 24 fps → "Slideshow" (broken)
├── 24-30 fps → "Choppy" (uncomfortable)
├── 30-45 fps → "Noticeably not smooth"
├── 45-60 fps → "Smooth" (acceptable)
├── 60 fps → "Buttery" (target)
└── 120 fps → "Premium" (ProMotion devices)

NEVER ship < 60fps animations.
```

### GPU vs CPU Animation

```
GPU-ACCELERATED (FAST):          CPU-BOUND (SLOW):
├── transform: translate          ├── width, height
├── transform: scale              ├── top, left, right, bottom
├── transform: rotate             ├── margin, padding
├── opacity                       ├── border-radius (animated)
└── (Composited, off main)        └── box-shadow (animated)

RULE: Only animate transform and opacity.
Everything else causes layout recalculation.
```

### Animation Timing Guide

| Animation Type | Duration | Easing |
|----------------|----------|--------|
| Micro-interaction | 100-200ms | ease-out |
| Standard transition | 200-300ms | ease-out |
| Page transition | 300-400ms | ease-in-out |
| Complex/dramatic | 400-600ms | ease-in-out |
| Loading skeletons | 1000-1500ms | linear (loop) |

### Spring Physics

```javascript
// React Native Reanimated
withSpring(targetValue, {
  damping: 15,      // How quickly it settles (higher = faster stop)
  stiffness: 150,   // How "tight" the spring (higher = faster)
  mass: 1,          // Weight of the object
})

// Flutter
SpringSimulation(
  SpringDescription(
    mass: 1,
    stiffness: 150,
    damping: 15,
  ),
  start,
  end,
  velocity,
)

// Natural feel ranges:
// Damping: 10-20 (bouncy to settled)
// Stiffness: 100-200 (loose to tight)
// Mass: 0.5-2 (light to heavy)
```

---

## 5. Memory Management

### Common Memory Leaks

| Source | Platform | Solution |
|--------|----------|----------|
| Timers | Both | Clear in cleanup/dispose |
| Event listeners | Both | Remove in cleanup/dispose |
| Subscriptions | Both | Cancel in cleanup/dispose |
| Large images | Both | Limit cache, resize |
| Async after unmount | RN | isMounted check or AbortController |
| Animation controllers | Flutter | Dispose controllers |

### Image Memory

```
Image memory = width × height × 4 bytes (RGBA)

1080p image = 1920 × 1080 × 4 = 8.3 MB
4K image = 3840 × 2160 × 4 = 33.2 MB

10 4K images = 332 MB → App crash!

RULE: Always resize images to display size (or 2-3x for retina).
```

### Memory Profiling

```
React Native:
├── React Native DevTools → Memory/Performance
├── Xcode Instruments (iOS)
└── Android Studio Profiler

Flutter:
├── DevTools → Memory tab
├── Observatory
└── flutter run --profile
```

---

## 6. Battery Optimization

### Battery Drain Sources

| Source | Impact | Mitigation |
|--------|--------|------------|
| **Screen on** | Highest | Dark mode on OLED |
| **GPS continuous** | Very high | Use significant change |
| **Network requests** | 🟡 High | Batch, cache aggressively |
| **Animations** | 🟡 Medium | Reduce when low battery |
| **Background work** | 🟡 Medium | Defer non-critical |
| **CPU computation** | 🟢 Lower | Offload to backend |

### OLED Battery Saving

```
OLED screens: Black pixels = OFF = 0 power

Dark mode savings:
├── True black (#000000) → Maximum savings (but black smear on scroll, harsh contrast)
├── Near black (#121212) → Most of the savings, smoother scrolling
├── Any color → Some power
└── White (#FFFFFF) → Maximum power

Rule: true black only for OLED-focused media UIs; otherwise near-black per platform guidance (#121212 Android).
```

### Background Task Guidelines

```
iOS:
├── Background refresh: Limited, system-scheduled
├── Push notifications: Use for important updates
├── Background modes: Location, audio, VoIP only
└── Background tasks: Max ~30 seconds

Android:
├── WorkManager: System-scheduled, battery-aware
├── Foreground service: Visible to user, continuous
├── JobScheduler: Batch network operations
└── Doze mode: Respect it, batch operations
```

---

## 7. Network Performance

### Offline-First Architecture

```
                    ┌──────────────┐
                    │     UI       │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │   Cache      │ ← Read from cache FIRST
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │   Network    │ ← Update cache from network
                    └──────────────┘

Benefits:
├── Instant UI (no loading spinner for cached data)
├── Works offline
├── Reduces data usage
└── Better UX on slow networks
```

### Request Optimization

```
BATCH: Combine multiple requests into one
├── 10 small requests → 1 batch request
├── Reduces connection overhead
└── Better for battery (radio on once)

CACHE: Don't re-fetch unchanged data
├── ETag/If-None-Match headers
├── Cache-Control headers
└── Stale-while-revalidate pattern

COMPRESS: Reduce payload size
├── gzip/brotli compression
├── Request only needed fields (GraphQL)
└── Paginate large lists
```

---

## 8. Performance Testing

### What to Test

| Metric | Target | Tool |
|--------|--------|------|
| **Frame rate** | ≥ 60fps | Performance overlay |
| **Memory** | Stable, no growth | Profiler |
| **Cold start** | < 2s | Manual timing |
| **TTI (Time to Interactive)** | < 3s | Lighthouse |
| **List scroll** | No jank | Manual feel |
| **Animation smoothness** | No drops | Performance monitor |

### Test on Real Devices

```
⚠️ NEVER trust only:
├── Simulator/emulator (faster than real)
├── Dev mode (slower than release)
├── High-end devices only

✅ ALWAYS test on:
├── Low-end Android (< $200 phone)
├── Older iOS device (iPhone 8 or SE)
├── Release/profile build
└── With real data (not 10 items)
```

### Performance Monitoring Checklist

```markdown
## During Development
- [ ] Performance overlay enabled
- [ ] Watching for dropped frames
- [ ] Memory usage stable
- [ ] No console warnings about performance

## Before Release
- [ ] Tested on low-end device
- [ ] Profiled memory over extended use
- [ ] Cold start time measured
- [ ] List scroll tested with 1000+ items
- [ ] Animations tested at 60fps
- [ ] Network tested on slow 3G
```

---

> **Remember:** Performance is not optimization—it's baseline quality. A slow app is a broken app. Test on the worst device your users have, not the best device you have.
