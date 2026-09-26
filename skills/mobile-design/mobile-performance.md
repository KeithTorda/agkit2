# Mobile Performance Reference

React Native and Flutter performance: lists, animation, memory, battery, and network. This is where most mobile code goes wrong, and it only shows on a real low-end device.

## 1. The budget

Each frame must finish inside its window: 16.7 ms at 60 fps, 8.3 ms at 120 fps (ProMotion). Miss it and the frame drops, which the user reads as jank. Test on the worst device your users have, on a release build, with production-sized data — not a fast laptop, dev mode, and ten rows.

## 2. React Native

### Lists: never `ScrollView` for data

A `ScrollView` with mapped items renders every item at once — memory and initial render blow up on any real dataset. Use a virtualised list.

FlashList v2 (built for the New Architecture) is the default for long lists. It recycles views and measures automatically:

```tsx
import { FlashList } from "@shopify/flash-list";

<FlashList
  data={items}
  renderItem={({ item }) => <ListItem item={item} />}
  keyExtractor={(item) => item.id}   // stable id from data, never the index
/>
```

v2 removed `estimatedItemSize` and the other `estimated*` props — do not pass them. `masonry` is now a prop, not a separate component.

`FlatList` is fine for short fixed lists, or when FlashList is unavailable:

```tsx
<FlatList
  data={items}
  renderItem={({ item }) => <ListItem item={item} />}
  keyExtractor={(item) => item.id}
  getItemLayout={(_, i) => ({ length: ITEM_HEIGHT, offset: ITEM_HEIGHT * i, index: i })} // fixed height only
  removeClippedSubviews maxToRenderPerBatch={10} windowSize={5}
/>
```

A stable `keyExtractor` (wrong recycling on reorder without it), `getItemLayout` for fixed-height rows, cleanup, and list-window props are correctness and layout settings, not memoization — keep them regardless of the React Compiler.

### Memoization

Compiler-first when the React Compiler is enabled (the memo rule is in `nextjs-react-expert`). The New Architecture does not ship the compiler by itself; check for `babel-plugin-react-compiler` in `babel.config.js` and the lockfile. With the compiler on, do not wrap rows in `React.memo` or `renderItem` in `useCallback` unless profiling shows a bailout. Without it, memoize measured hot list items only.

### Animation

Native-driver `Animated` runs on the UI thread and stays smooth when JS is busy, but supports only `transform` and `opacity` — not width/height, colour, border radius, or margin/padding:

```js
Animated.timing(value, { toValue: 1, duration: 300, useNativeDriver: true }).start();
```

For anything the native driver cannot do (layout, colour, gesture-driven), use Reanimated 4 — it runs on the UI thread, animates any property, and supports CSS-style transitions on the New Architecture:

```tsx
import Animated, { useSharedValue, useAnimatedStyle, withSpring } from 'react-native-reanimated';
const offset = useSharedValue(0);
const style = useAnimatedStyle(() => ({ transform: [{ translateX: withSpring(offset.value) }] }));
return <Animated.View style={style} />;
```

### Memory leaks

Clean up everything you start. The common sources are timers, event listeners, subscriptions (WebSocket, PubSub), async work that sets state after unmount, and unbounded image caches.

```js
useEffect(() => {
  const id = setInterval(fetchData, 5000);
  return () => clearInterval(id);   // without this, the interval leaks
}, []);
```

## 3. Flutter

- Add `const` to every widget that does not depend on runtime state — const widgets do not rebuild.
- Keep `setState` scope tight; it rebuilds the whole `build` method. For surgical rebuilds use `ValueListenableBuilder` or `ref.watch(provider.select((s) => s.field))` instead of watching the whole provider.
- Lists: `ListView.builder` (lazy), never `ListView(children: ...)`; `itemExtent` for fixed height; `ListView.separated` for dividers.
- Images: `CachedNetworkImage` with `width`/`height` and `memCacheWidth`/`memCacheHeight` (2x for retina), placeholder and error widget — never a bare `Image.network`.
- Dispose controllers, subscriptions, and text controllers in `dispose()`, in reverse order of creation.
- Impeller is the default renderer on current Flutter; prefer `FadeTransition` over the `Opacity` widget for fades.

## 4. Animation quality (both platforms)

Target 60 fps, 120 on ProMotion; never ship an animation that drops below 60. Only `transform` and `opacity` are GPU-composited — everything else (width, height, top/left, margin, border-radius, box-shadow) forces layout recalculation. Timing: micro-interactions 100-200 ms, transitions 200-300 ms, page transitions 300-400 ms, all ease-out or ease-in-out. Spring feel: damping 10-20, stiffness 100-200, mass 0.5-2.

## 5. Memory

Leak sources and fixes are the same idea on both platforms: clear timers, listeners, and subscriptions on teardown; guard async-after-unmount (AbortController / `mounted` check on RN, dispose on Flutter); bound image caches.

Image memory is `width x height x 4` bytes: a 1080p image is 8.3 MB, a 4K image 33 MB, so ten 4K images can crash the app. Always resize images to their display size (2-3x for retina), never decode full resolution into a thumbnail.

Profile memory with React Native DevTools, Xcode Instruments, or Android Studio Profiler (RN); DevTools Memory tab and `flutter run --profile` (Flutter). Watch for a heap that grows and never settles, and detached views.

## 6. Battery

Biggest drains: screen brightness (dark mode helps on OLED), continuous GPS (use significant-change updates), frequent network (batch and cache so the radio wakes once), and background work (defer non-critical). Respect the platform's background rules: iOS background tasks are short (~30 s) and system-scheduled; Android uses WorkManager/JobScheduler and honours Doze — batch, do not poll.

## 7. Network

Read from cache first, then update from the network — instant UI, works offline, less data. Batch small requests, use ETag/`Cache-Control` and stale-while-revalidate to avoid re-fetching unchanged data, compress (gzip/brotli), request only needed fields, and paginate large lists.

## 8. What to measure, and where

| Metric | Target | Tool |
|--------|--------|------|
| Frame rate | 60 fps (120 on ProMotion) | Performance overlay |
| Memory | Stable, no growth | Profiler |
| Cold start | under 2 s | Manual timing |
| Time to interactive | under 3 s | Profiler / Lighthouse-style timing |
| List scroll / animation | No dropped frames | Performance monitor, real device |

Test on a low-end Android (a sub-$200 phone), an older iPhone (SE / 8), a release or profile build, and real data. A simulator or a flagship hides the problems your users will hit.

## 9. Anti-patterns

`ScrollView` for data lists; index as list key; JS-driven (`useNativeDriver: false`) animation of layout properties; uncleared timers and subscriptions; full-resolution images in small views; polling in the background; and trusting the simulator over a real low-end device.
