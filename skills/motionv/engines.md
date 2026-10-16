# Select and operate the actual motion engine

Inspect the existing project, manifest/lockfile, installed tool versions and available engine skills first. Keep a supported existing engine when it serves the request. For new coded motion, HyperFrames is a suitable default when available; use the user-selected framework when explicit. A simple trim/concatenation/conversion may need only FFmpeg.

## HyperFrames

Read the installed `hyperframes` entry skill and the workflow it selects; read its composition/runtime contract before authoring. Search the configured skill roots rather than assuming one home-directory layout. Do not invent an engine skill if missing; use available official documentation or report the missing capability.

Use the project-pinned CLI and its help for initialization, validation, preview, snapshots and render options. Typical command families include `init`, `check`, `snapshot`, `render` and `doctor`; exact arguments and capabilities can change. Avoid fetching `@latest` in every command or upgrading merely to follow a historical kit example.

Keep composition metadata, clip timing and runtime timeline registration consistent with the installed contract. Rendering must seek deterministically: no uncontrolled wall-clock state, random values or required network result changing the frame. Isolate framework-owned visibility/media timing from animated child properties where the contract requires it. Stable local/package-managed assets help avoid blocked CDN renders; use the engine's supported asset mechanism and preserve rights.

Check validation sampling, not just exit text: a lint/runtime failure can prevent later layout samples from running. A zero sample count is not proof of no layout issue. Inspect actual snapshots and rendered output.

## Remotion or another chosen framework

Reuse the installed engine's frame/time model, supported asset paths and render commands. In Remotion, frame-driven animation must resolve correctly on arbitrary seek rather than depending on uncontrolled CSS playback. Existing engine skills/official docs are the authority for version-specific API and renderer options.

Verify current licensing/terms for the actual engine and organization/use when adopting it; do not repeat hardcoded team-size thresholds or pricing from an old note. A reference UI using React does not require the video to use Remotion, and a requested engine does not authorize silently switching it.

## FFmpeg for direct media operations

Inspect input streams, duration, dimensions, frame rate and audio before selecting arguments. Use current installed help for the relevant codec/filter. Write to a separate output unless replacing the source is explicitly intended. For example:

```powershell
ffprobe -v error -show_streams -show_format -of json input.mp4
ffmpeg -i input.mp4 -an -c:v libx264 -pix_fmt yuv420p -movflags +faststart output.mp4
ffmpeg -ss 1 -i output.mp4 -frames:v 1 poster.jpg
```

The second command is an example muted H.264 delivery copy, not a universal bitrate/quality recipe. Stream-copy trims can land on keyframe boundaries; re-encode when exact timing is needed. Concatenation needs compatible streams or deliberate normalization. Audio mixing must handle missing audio and the desired duration; a recipe assuming two input audio streams can fail on silent video. Subtitle paths/fonts need correct shell/filter escaping, especially on Windows. Inspect the actual output rather than assuming the command preserves every track/metadata.

## Diagnose the failed boundary

| Symptom | Evidence and useful response |
|---|---|
| Missing script/font/media | Inspect resolved paths and renderer network/file errors; package supported stable assets rather than disabling checks. |
| Browser unavailable | Inspect engine diagnostics and supported browser configuration; do not automatically download or point at an unrelated binary. |
| FFmpeg missing after setup | Confirm the actual executable/path and process environment; a new shell may be needed. |
| Blank/frozen frame | Check composition duration, arbitrary seeking, runtime errors, media readiness and the engine's visibility contract. |
| Slow render | Measure scene cost and environment; draft quality/GPU/workers are version-specific choices, not guaranteed fixes. |

Use the kit's doctor/verifier as bounded diagnostics with actual supported options. Review metadata, frame artifacts, playback/audio and final output. Report a setup/render failure precisely without claiming that source code alone constitutes a delivered video.
