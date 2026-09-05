---
name: flutter-app
description: Flutter mobile app template. Riverpod 3, go_router, Drift, feature-first clean architecture.
---

# Flutter App Template

> Pin to the current stable line when scaffolding.

## Tech Stack

| Component | Technology |
|---|---|
| Framework | Flutter 3.3x (Dart 3.x) |
| State | Riverpod 3 with `riverpod_annotation` codegen |
| Navigation | go_router |
| HTTP | Dio |
| Local database | Drift (type-safe SQLite); `hive_ce` only for simple key-value caches |
| Secure storage | flutter_secure_storage |
| Models | Freezed |

## Directory Structure

```
project_name/
├── lib/
│   ├── main.dart
│   ├── app.dart
│   ├── core/
│   │   ├── constants/
│   │   ├── theme/            # Material 3 theme from DESIGN.md tokens
│   │   ├── router/
│   │   └── utils/
│   ├── features/
│   │   ├── auth/
│   │   │   ├── data/         # repositories, DTOs, Drift DAOs
│   │   │   ├── domain/       # entities, use cases
│   │   │   └── presentation/ # screens, widgets, providers
│   │   └── home/
│   ├── shared/
│   │   ├── widgets/
│   │   └── providers/
│   └── services/
│       ├── api/              # Dio client, interceptors
│       └── database/         # Drift database and migrations
├── test/
├── DESIGN.md                 # Visual source of truth (required before UI)
└── pubspec.yaml
```

## Architecture Layers

| Layer | Contents |
|---|---|
| Presentation | Screens, widgets, Riverpod providers |
| Domain | Entities, use cases |
| Data | Repositories, models, Drift DAOs, API clients |

## Key Packages

| Package | Purpose |
|---|---|
| flutter_riverpod, riverpod_annotation, riverpod_generator | State management with codegen |
| go_router | Declarative navigation, deep links |
| dio | HTTP client |
| drift, drift_flutter, drift_dev | Local SQL database with generated DAOs |
| freezed, freezed_annotation, json_serializable | Immutable models and JSON |
| flutter_secure_storage | Tokens and secrets |
| build_runner | Code generation |

## Setup Steps

1. `flutter create {{name}} --org com.{{bundle}}`
2. Add the packages above (`flutter pub add ...`), then `flutter pub get`
3. Define the Drift database (`@DriftDatabase(tables: [...])`) in `services/database/`
4. `dart run build_runner build -d` (Riverpod, Freezed, Drift codegen)
5. `flutter run`

## Best Practices

- Feature-first folders: data / domain / presentation per feature.
- Riverpod 3: generated providers via `riverpod_annotation`; plain `Notifier` classes; the generated ref is `Ref`. Legacy `StateProvider`/`StateNotifierProvider` live in `package:riverpod/legacy.dart`; avoid them in new code.
- Drift for anything relational or queried; migrations are versioned in the database class. Never store secrets in Drift or Hive.
- Freezed for models; `json_serializable` for API DTOs.
- Material 3 theming (Material 3 Expressive on Android 16) built from `DESIGN.md` tokens; see `@[skills/mobile-design]`.
- Tests: unit tests for use cases and DAOs (Drift in-memory), widget tests for screens.
