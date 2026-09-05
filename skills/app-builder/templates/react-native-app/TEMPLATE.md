---
name: react-native-app
description: React Native mobile app template. Expo SDK 54+, Expo Router, New Architecture, NativeWind 4, Reanimated 4, FlashList v2.
---

# React Native App Template

> Pin to the current stable line when scaffolding. Install every package that touches native code with `npx expo install` so versions match the SDK.

## Tech Stack

| Component | Technology | Notes |
|---|---|---|
| Core | React Native + Expo | SDK 54+, New Architecture enabled (default) |
| Language | TypeScript | Strict mode |
| UI logic | React 19 | React Compiler enabled by this template (`babel-plugin-react-compiler`); compiler-first when the React Compiler is enabled (`reactCompiler: true` in next.config / babel-plugin-react-compiler in Expo — the kit's templates enable it); check the flag before removing manual memo |
| Navigation | Expo Router | File-based, typed routes, universal links |
| Styling | NativeWind 4+ (stable) | Tailwind classes in RN; use the Tailwind version NativeWind's install guide specifies |
| Animation | Reanimated 4 | UI-thread animations; requires the New Architecture |
| Lists | FlashList v2 | Drop-in for long lists; no `estimatedItemSize` |
| State | Zustand + TanStack Query | Client state + server state |
| Storage | Expo SecureStore | Encrypted key-value storage |

## Directory Structure

```
project-name/
├── src/
│   ├── app/                 # Expo Router routes only
│   │   ├── _layout.tsx      # Root layout (Stack/Tabs); imports global.css
│   │   ├── index.tsx
│   │   ├── (tabs)/          # Tab group: _layout.tsx, home.tsx, profile.tsx
│   │   ├── +not-found.tsx
│   │   └── [id].tsx         # Dynamic route (typed)
│   ├── components/ui/       # Primitives (Button, Text)
│   ├── components/features/ # Composed components
│   ├── hooks/
│   ├── lib/api.ts           # fetch client
│   ├── lib/storage.ts       # SecureStore wrapper
│   ├── store/               # Zustand stores
│   └── constants/           # Theme values from DESIGN.md
├── assets/                  # Fonts, images
├── global.css               # NativeWind entry
├── babel.config.js          # nativewind/babel preset
├── metro.config.js          # withNativeWind wrapper
├── DESIGN.md                # Visual source of truth (required before UI)
└── app.json                 # Expo config: scheme, newArchEnabled, typed routes
```

## Navigation Patterns

| Pattern | Implement |
|---|---|
| Stack | `<Stack />` in `_layout.tsx` |
| Tabs | `<Tabs />` in `(tabs)/_layout.tsx` |
| Drawer | `expo-router/drawer` |
| Modal | `presentation: 'modal'` on a Stack screen |
| Deep links | `scheme` in `app.json`; `expo-linking` for incoming URLs |

## Setup Steps

1. Create the project:
   ```bash
   npx create-expo-app@latest my-app
   cd my-app
   ```
2. Core dependencies (SDK-matched):
   ```bash
   npx expo install expo-router expo-linking expo-constants expo-status-bar react-native-safe-area-context react-native-screens
   npx expo install react-native-reanimated react-native-worklets @shopify/flash-list expo-image expo-secure-store
   npm install nativewind zustand @tanstack/react-query
   npm install -D babel-plugin-react-compiler
   ```
3. NativeWind 4, per its current install guide: add `nativewind/babel` and `jsxImportSource: "nativewind"` to `babel.config.js`, and `plugins: ['babel-plugin-react-compiler']` in the same file (the New Architecture alone does not enable the compiler); wrap Metro with `withNativeWind(config, { input: './global.css' })`; create `global.css` with the Tailwind directives; import it in `src/app/_layout.tsx`; set `content` paths in `tailwind.config.js`.
4. Enable typed routes in `app.json` (`experiments.typedRoutes: true`) and set the URL `scheme`.
5. Run: `npx expo start -c` (`i` for the iOS simulator, `a` for the Android emulator).

## Best Practices

- Keep `newArchEnabled: true`; Reanimated 4 and FlashList v2 depend on it.
- Use `expo-image` instead of `<Image />`; FlashList v2 for long lists, FlatList acceptable for short fixed lists.
- Server data goes through TanStack Query; no fetches inside `useEffect`.
- Theme values (colors, spacing, type scale) come from `DESIGN.md`; mirror them in the Tailwind theme and `constants/`.
- Respect safe areas and platform conventions (iOS 26 and Android 16 baselines; see `@[skills/mobile-design]`).
