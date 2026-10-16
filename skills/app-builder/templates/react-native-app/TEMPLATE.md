# React Native mobile product

## Fit and inspection

Use when React Native is selected or installed. Choose Expo or a native-managed setup from device capability, build and distribution requirements; inspect actual compatible versions.

Inspect existing work before scaffolding. For a new foundation, use current official setup guidance and compatible versions; do not copy historical CLI flags blindly. Preserve the requested package manager, deployment constraints and user changes.

## Implementation decisions

- Reuse supported navigation and theme mechanisms. Adapt platform back/permission behavior and read real safe-area/keyboard insets.

- Choose server cache, local storage, secure credentials and offline synchronization separately. NativeWind, Reanimated and third-party virtualized lists are options when justified.

- Keep runtime-native compatibility and development/build profiles explicit. An over-the-air update cannot replace every native binary change.

For new visual design, complete the shared short style/reference intake and wait unless already answered or delegated. Reuse accepted tokens and design components; this template does not select an aesthetic or install a styling package. API/CLI-only work needs no visual questionnaire.

## Verify and hand off

Compile/run the available native target, inspect actual screens and text scaling, exercise primary navigation/data flow and relevant offline/permission behavior. State simulator versus device coverage.

Report the actual run command, implemented outcome, checks performed and concrete remaining setup. Starter code, a mocked integration or a successful dependency install is not proof of a working end-to-end product.
