---
name: motionv
description: "Create and edit rendered video or motion graphics from a brief, brand, footage or data. Establish visual direction, choose a supported engine, plan timing, implement seek-safe scenes, render and inspect actual frames and audio. Use frontend-design for motion inside a normal interactive site."
version: 2.8.2
---

# Motion video production

Produce an editable motion project and a usable rendered deliverable. Input can be a short `/motionv` brief, script, assets, existing project, website, footage or audio. Determine whether the requested result is a video file, an interactive web animation, or a simple media edit before choosing tooling.

## Brief and visual direction

Before every new visual design, ask one short question about style and references and wait unless the user already answered or delegated those choices. An approved look carried into a small edit needs no repeat. Inspect assets, existing project, engine availability and technical requirements while waiting.

Use the brief to resolve purpose, audience, duration, aspect ratio, destination, necessary copy, audio/captions, source assets and delivery format. Ask only for missing decisions that materially alter production; a request to choose grants discretion, not license to invent factual claims. State reasonable technical assumptions without forcing a default music bed, voice, theme or social format.

Read [craft.md](craft.md) for timing and composition; read [engines.md](engines.md) for engine selection and render mechanics. The optional [BrewedOps Motion Library](https://brewedops.cloud/motionlibrary/) can inform selected transitions or interface presentation patterns. It is a web pattern reference, not a video runtime or a required source of animation. Rebuild relevant ideas for the chosen engine's deterministic timeline.

## Establish a working toolchain

Inspect the existing manifest, lockfile, engine/project version and normal commands. For a new coded motion project, use the available HyperFrames entry skill and its routed workflow when suitable; an existing Remotion or other supported project can stay with its engine. FFmpeg may be enough for a trim, mix, caption burn or conversion. Do not introduce an animation framework merely to concatenate clips.

The optional setup helper is diagnostic:

```powershell
python "KIT/skills/motionv/scripts/motionv_doctor.py"
```

Read its actual result. Use its install mode only when needed, compatible with this machine and within the user's authorized setup scope; inspect the actions first. Do not make a mandatory installation approval ritual if setup is already authorized. Avoid downloading fresh engines for every run or relying on hardcoded CLI options without checking the installed version's help. Verify current licensing for adopted engines and assets rather than repeating dated pricing rules.

## Plan and build

Write a proportional storyboard/timing plan with scene purpose, time range, on-screen copy, visual action and audio. For substantial work save `STORYBOARD.md`; a small existing-clip edit may need only an edit note. Present consequential creative decisions for input when they remain unresolved. Once the brief or delegated direction is sufficient, proceed without requiring a second ceremonial approval.

Use one authoritative timing source. Make animation deterministic and seek-safe for the engine: use its frame/time model rather than wall-clock timers or uncontrolled random values. Load required assets through supported stable paths, preserve font and media provenance, and avoid network-dependent rendering where local packaging is supported. Organize scenes for editability without imposing a universal duration threshold or scene count.

Keep text readable at the final viewing size and duration. Platform safe areas depend on the actual destination and may change; verify them when material. Respect reduced-motion/static fallbacks for an embedded web deliverable. Use licensed/supplied media, truthful demo labeling and rights appropriate to the assets. If generation or a paid service is needed, use available tooling under the user's authorization and report provenance.

## Render, inspect, refine

Run the engine's relevant validation, render a draft when useful, and inspect representative frames plus transitions and the final frame. Play audio-bearing output when tools permit to check intelligibility, sync, clipping and start/end behavior. A contact sheet misses timing and sound, so do not claim playback review from frames alone.

```powershell
python "KIT/skills/motionv/scripts/motionv_verify.py" <rendered-file> --preset <supported-preset> --duration <seconds>
```

Use only helper options/presets confirmed by `--help`. Inspect its output artifacts and result; it cannot judge whether the creative direction works or prove full playback. Fix observed defects and recheck the affected output. Confirm final duration, dimensions, frame rate, codec/container, audio and file size from actual media metadata when available.

Deliver the actual file and editable project path with the render command, relevant asset/license notes, checks performed, and exact limits. Include an appropriate poster/fallback and embed guidance when the output is a site background. Do not promise zero errors or treat a successful render as complete visual and audio verification.
