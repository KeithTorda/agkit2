---
name: motionv
description: "/motionv - Makes motion videos as code and renders them to MP4/WebM/GIF: promos, explainers, product and website showcases, social reels, title cards, logo stings, lower thirds, data/stat animations, captioned clips, website hero loops. Brief, storyboard, build with HyperFrames (HTML + GSAP, default) or Remotion (React), render, then check the actual frames. Use for any request to make, animate, edit or render a video or motion graphic."
version: 2.5.0
---

# /motionv

Makes a video the way a small motion studio would: agree the brief, storyboard it, build it as code, render it, look at the frames, fix, deliver. Videos are code here, so they are versioned, editable by text, and re-renderable with new copy or data.

**Input:** the text after `/motionv` is the brief (`/motionv 30s reel for Kape Norte's new iced latte, Taglish captions`). It may include a URL, images, footage, a music file, a script, or a `DESIGN.md` to follow. `/motionv doctor` only runs the setup check.
**Agent:** you (main agent). Hand UI-only pieces to `frontend-specialist` only if the video is embedded into a site build.
**Read now:** this file, then `KIT/skills/motionv/engines.md`.
**Read when:** writing scenes or timing → `KIT/skills/motionv/craft.md`; the engine skill you route to (installed in `~/.gemini/config/skills/`): `hyperframes` (entry), then the workflow it routes to; or `remotion-best-practices` + `remotion-create`.

## 0. Setup check (first run on a machine, or when a command fails)

```powershell
python "KIT/skills/motionv/scripts/motionv_doctor.py"
```

It checks Node.js 22+, git, FFmpeg/FFprobe, the HyperFrames CLI, the render browser, and whether the engine skills are installed where Antigravity reads them. If it says NOT READY, tell the user what is missing in one line each and ask once: "Install the missing pieces now? (FFmpeg via winget, engine skills into ~/.gemini/config/skills, render browser)". On yes:

```powershell
python "KIT/skills/motionv/scripts/motionv_doctor.py" --install            # HyperFrames
python "KIT/skills/motionv/scripts/motionv_doctor.py" --install --engine all  # also Remotion skills
```

After installing FFmpeg, a new terminal (or an Antigravity restart) is needed before `ffmpeg` is on PATH. Engine skills installed for the first time are picked up after an Antigravity restart; until then, read them by path from `~/.gemini/config/skills/<name>/SKILL.md`.

## 1. Brief (one message, max 5 questions, each with a default)

Skip what the request already answers. Typical gaps:

| Question | Default |
|---|---|
| Where will it play? | YouTube / website 16:9 1920x1080 30 fps |
| Length? | 15 s for a sting or ad, 30 s for a reel, 60-90 s for an explainer |
| Voice, music, captions? | Music bed + burned-in captions, no voice |
| Look? | `DESIGN.md` if the project has one; else brand colours from the logo/site; else one direction proposed in the storyboard |
| Assets? | User's logo/photos/screenshots; otherwise typography and shapes only, no stock-photo look |

"Proceed" or "just make it" means: use the defaults, state them, go.

Platform presets (pass the preset name to the verifier):

| Preset | Size | Notes |
|---|---|---|
| `youtube` | 1920x1080, 30 fps | 16:9; `youtube-4k` 3840x2160 |
| `reels` / `shorts` / `tiktok` | 1080x1920, 30 fps | keep text out of the top 220 px and bottom 380 px (UI overlays); captions on, most viewers watch muted |
| `square` / `feed-4x5` | 1080x1080 / 1080x1350 | Facebook and Instagram feed (LGU and school pages) |
| `hero` | 1920x1080, muted loop, ≤ 8 MB | website background: MP4 + WebM, seamless loop, poster frame, nothing essential in the text |

## 2. Pick the engine

| Situation | Engine |
|---|---|
| Default; any promo, explainer, social clip, title, overlay, captions over footage, website showcase | **HyperFrames** - HTML + CSS + GSAP compositions, rendered deterministically. Apache-2.0, no fees. Has workflows for product launches, explainers, captions, music-synced edits, slideshows |
| The project is already React/Next.js and the video reuses its components or data, or the user asks for Remotion | **Remotion** - React components as frames. Free for individuals and teams of up to 3 people; larger companies need a Remotion company license. Say this once when choosing it for a client |
| Join clips, trim, add music, burn subtitles, convert, make a GIF, no new animation | **FFmpeg** directly (recipes in `engines.md`) |
| Real-world footage that cannot be designed (people, places) | Ask the user for footage, or generate stills/clips with an image/video model as assets, then cut them in HyperFrames. Never fake a real person, a real event, or a client's product |

## 3. Storyboard before building

Write `STORYBOARD.md` in the video project (format in `craft.md`): duration, size, look in 3 words, then one row per scene with time range, on-screen text, visual, motion, audio cue. Count reading time: on-screen text holds at least 0.4 s per word plus 0.5 s. Show it to the user and wait for one round of edits, unless they said proceed. This is the only checkpoint; changing a storyboard costs seconds, changing a render costs minutes.

## 4. Build

**HyperFrames** (default):
```powershell
npx hyperframes@latest init <video-name> --non-interactive --example blank --resolution landscape   # or portrait / square
cd <video-name>
```
Then follow the `hyperframes` skill and the workflow it routes to (`general-video`, `product-launch-video`, `faceless-explainer`, `motion-graphics`, `embedded-captions`, `music-to-video`, `slideshow`). Its authoring contract (`hyperframes-core`) is the rulebook for composition HTML; read it before writing any.

**Remotion:** follow `remotion-create` (scaffold with `npx create-video@latest --yes --blank --no-tailwind <name>`), then `remotion-best-practices`.

Kit rules on top of the engine's rules:
- **Everything local at render time.** Download GSAP, fonts, images, audio into the project (`vendor/`, `assets/`) and reference them by relative path. A CDN that is slow or blocked during render fails the whole render. (`npm i gsap` then copy `node_modules/gsap/dist/gsap.min.js` to `vendor/`.)
- **Brand from `DESIGN.md`** when it exists: colours, fonts, radius. Otherwise define them once as CSS variables at the top of the composition.
- **Text is real copy.** Final words, correct spelling (₱, ñ, Filipino diacritics), no lorem. Hype-free per `anti-template` parts 01-05; `craft.md` covers on-screen copy.
- **Audio is licensed.** Use music the user supplies or that is royalty-free with terms you can name; generated voice (HyperFrames `tts`, Kokoro) is fine; never clone a real person's voice.
- One composition per scene for anything longer than ~20 s; keep scene timing in one place.

## 5. Check, then render

1. `npx hyperframes check` (lint + runtime + layout) - fix every error before rendering.
2. Draft render: `npx hyperframes render -q draft -o renders/draft.mp4`.
3. Verify and look:
   ```powershell
   python "KIT/skills/motionv/scripts/motionv_verify.py" renders/draft.mp4 --preset <preset> --duration <s>
   ```
   Open `contact-sheet.png` and the frames it lists. Say what you see, scene by scene: text readable and inside safe areas, nothing clipped or overlapping, brand colours right, no blank or frozen stretch you did not intend. For specific moments use `npx hyperframes snapshot` at those times.
4. Fix and repeat 2-3 until clean.
5. Final render: `npx hyperframes render -q delivery -o renders/<name>.mp4` (add `--format webm` for a site hero, `--format gif --fps 15` for docs/PRs, `--format mov` for transparent overlays). Re-run the verifier on the final file.

Remotion: `npx remotion render <CompositionId> renders/<name>.mp4`, then the same verifier.

## 6. Deliver

Report in this shape:
```
Video: renders/kape-norte-latte-reel.mp4 - 1080x1920, 30 fps, 30.0 s, 6.4 MB, audio -14 LUFS
Engine: HyperFrames 0.8.x · Scenes: 6 (STORYBOARD.md) · Captions: burned in
Checked: hyperframes check clean, motionv_verify PASS, contact sheet reviewed
Edit later: change copy in compositions/*.html or STORYBOARD.md, then `npx hyperframes render`
Not verified: playback on an actual phone; music licence is the client's file
```
For a website hero also hand over the `<video autoplay muted loop playsinline poster>` snippet with MP4 + WebM sources.

## Never
- Render without looking at the frames, or claim a video is done from the code alone.
- Load scripts, fonts or media from a CDN at render time.
- Use someone's likeness, voice, logo or footage without the user's right to use it; invent testimonials or fake "as seen on" logos.
- Put essential text inside platform UI zones on vertical video, or rely on sound for meaning on social.
