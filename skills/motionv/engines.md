# /motionv engines - commands and pitfalls

Read with `KIT/skills/motionv/SKILL.md`. The installed engine skills (`~/.gemini/config/skills/hyperframes*`, `remotion-*`) are the full reference; this file is the short version plus what bit us in testing.

## HyperFrames (default)

Tested with HyperFrames 0.8.111 (Oct 2026). Projects pin the CLI version in `package.json`; check for updates with `npx hyperframes@latest upgrade --project . --check`.

| Task | Command |
|---|---|
| New project | `npx hyperframes@latest init <name> --non-interactive --example blank --resolution landscape` (`portrait`, `square`, `landscape-4k`) |
| From footage / audio | `npx hyperframes@latest init <name> --non-interactive --video clip.mp4` or `--audio track.mp3` (transcribes for captions) |
| Capture a website for a promo | `npx hyperframes capture <url>` |
| Add a ready block | `npx hyperframes catalog`, then `npx hyperframes add <block>` |
| Preview (user can scrub and edit) | `npx hyperframes preview` |
| What is on the timeline | `npx hyperframes timeline --json` |
| Validate | `npx hyperframes check` (lint + runtime + layout + contrast) |
| Still frames at given times | `npx hyperframes snapshot --at 1.5,4,9.2` |
| Draft render | `npx hyperframes render -q draft -o renders/draft.mp4` |
| Final render | `npx hyperframes render -q delivery -o renders/final.mp4` |
| Other formats | `--format webm` (hero, transparency) · `--format mov` (ProRes 4444 alpha overlay) · `--format gif --fps 15` · `--format png-sequence` |
| Vertical from same comp | only if the composition is vertical; `--resolution` scales, it does not re-layout |
| Many versions from data | declare `data-composition-variables`, then `render --batch rows.json` (e.g. one video per barangay or per product) |
| Voiceover | `npx hyperframes tts script.txt -v am_michael -o assets/vo.wav` (local Kokoro; English voices, no Filipino; needs Python packages, see doctor) |
| Captions from audio | `npx hyperframes transcribe audio.mp3 -o captions.srt` (needs whisper; see doctor) |
| Beat-synced cuts | `npx hyperframes beats` on the music track |
| Environment check | `npx hyperframes doctor` |

Composition contract essentials (full rules: `hyperframes-core`):
- Root `<div data-composition-id="main" data-start="0" data-duration="30" data-width="1920" data-height="1080">`; timed elements get `class="clip"` plus `data-start` / `data-duration`.
- Exactly one `gsap.timeline({ paused: true })`, registered as `window.__timelines["main"]` (key = composition id) after it is fully built.
- Render length is the root `data-duration`, not the timeline length.
- Set initial state inside tweens (`fromTo`), never a CSS `transform` on the same property GSAP animates.
- Do not tween `visibility` / `autoAlpha` / `display` on a `.clip`; animate a child.
- Every `<audio>` needs an `id` (otherwise the render is silent). No `crossorigin` on media.
- No `Math.random()` without a seed, no `Date.now()`, no network calls, no `repeat: -1` (use a finite count).
- Fonts: `@font-face` pointing to a font file inside the project.
- A lint error disables the layout and contrast audits, so "0 samples" is not a pass. Clear errors first.

Problems we hit in testing:
| Symptom | Cause | Fix |
|---|---|---|
| `sub_timeline_script_failure ... cdn.jsdelivr.net` and render blocked | the starter loads GSAP from a CDN; the render machine could not reach it | `npm i gsap`, copy `node_modules/gsap/dist/gsap.min.js` to `vendor/`, change the `<script src>` to `vendor/gsap.min.js` |
| `All providers failed for chrome-headless-shell` | the render browser download was blocked | `npx hyperframes browser ensure` on a network that allows it, or set `HYPERFRAMES_BROWSER_PATH` to an installed Chrome / headless shell |
| `ffmpeg not found` right after installing it | PATH is read when the terminal starts | open a new terminal or restart Antigravity; or set `HYPERFRAMES_FFMPEG_PATH` / `HYPERFRAMES_FFPROBE_PATH` |
| Slow renders on Windows | software GPU path | try `--browser-gpu`; use `-q draft` while iterating; `--workers auto` is the default |

## Remotion (React projects, or when asked)

Licence: free for individuals, non-profits and organisations of up to 3 people; above that a company license is required. Tell the user once.
| Task | Command |
|---|---|
| New project | `npx create-video@latest --yes --blank --no-tailwind <name>` then `npm i` |
| Studio preview | `npx remotion studio` |
| Render | `npx remotion render <CompositionId> renders/<name>.mp4` |
| Still | `npx remotion still <CompositionId> --frame=45 out.png` |
| Read the rules | `remotion-best-practices` (timing with `useCurrentFrame`, `interpolate`, `spring`; no CSS animations; `staticFile()` for assets) |

## FFmpeg recipes (no new animation)

```powershell
# Join clips with the same codec
ffmpeg -f concat -safe 0 -i list.txt -c copy joined.mp4          # list.txt lines: file 'a.mp4'
# Trim without re-encoding (cut on keyframes)
ffmpeg -ss 00:00:05 -to 00:00:20 -i in.mp4 -c copy cut.mp4
# Add a music bed at -18 dB under the video's own audio, ending with the video
ffmpeg -i video.mp4 -i music.mp3 -filter_complex "[1:a]volume=-18dB[m];[0:a][m]amix=inputs=2:duration=first[a]" -map 0:v -map "[a]" -c:v copy -c:a aac out.mp4
# Burn subtitles (SRT) into the picture
ffmpeg -i in.mp4 -vf "subtitles=captions.srt:force_style='FontName=Inter,FontSize=22,OutlineColour=&H80000000,BorderStyle=3'" -c:a copy out.mp4
# Normalise loudness for social (-14 LUFS)
ffmpeg -i in.mp4 -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:v copy out.mp4
# Website hero: muted, small, two formats, poster
ffmpeg -i final.mp4 -an -c:v libx264 -crf 26 -preset slow -movflags +faststart -pix_fmt yuv420p hero.mp4
ffmpeg -i final.mp4 -an -c:v libvpx-vp9 -crf 34 -b:v 0 hero.webm
ffmpeg -ss 1 -i final.mp4 -frames:v 1 -q:v 3 hero-poster.jpg
# GIF for docs / PRs
ffmpeg -i in.mp4 -vf "fps=15,scale=960:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse" out.gif
```
