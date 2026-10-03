# /motionv craft - storyboard, timing, type, sound

Guidance, not law: the brief and `DESIGN.md` win. These are the defaults that make a video read as made on purpose.

## STORYBOARD.md format

```markdown
# <Video name>
Purpose: <who watches, where, what they should do after>
Format: 1080x1920 · 30 fps · 30 s · captions burned in · music bed
Look: <3 words, e.g. warm, local, confident> · Colours/fonts: DESIGN.md (or listed here)

| # | Time | On screen (exact words) | Visual | Motion | Audio |
|---|---|---|---|---|---|
| 1 | 0.0-2.5 | "Bagong Iced Latte" | cup photo, cream background | cup slides up, title types on per word | music in, soft hit at 0.4 |
| 2 | 2.5-6.0 | "₱120 · 16 oz" | price card | card scales from 0.96 to 1, price counts in | - |
| ... |
| 6 | 26.0-30.0 | "Kape Norte · Flora, Apayao" + logo | logo lock-up | hold 2 s still for the end card | music out |
```

## Timing
- On-screen text stays at least 0.4 s per word + 0.5 s. A 6-word line holds about 3 s.
- The first 1.5 s decides whether a social viewer stays: show the subject or the hook immediately, no slow logo intro.
- End card: hold 2-3 s with no motion so it can be read and screenshotted.
- Scene length 2-5 s for promos, 5-10 s for explainers. Vary it; identical scene lengths feel mechanical.
- Cut on action or on the music beat; when music drives the piece, use `npx hyperframes beats`.

## Motion
- Ease out for things arriving (`power2.out`, `power3.out`), ease in for things leaving (`power2.in`), `power2.inOut` for moves across the frame. Linear only for continuous things (tickers, rotating loaders, parallax drift).
- Durations: UI-like pops 0.25-0.45 s; text entrances 0.5-0.8 s; camera moves 1.5-4 s.
- Stagger groups by 0.04-0.08 s per item; more feels slow.
- One hero motion per scene. If everything moves, nothing leads.
- Animate transform and opacity. Blur, glow, gradients and 3D are fine when the look calls for them; check them in the contact sheet for banding and legibility.
- Loops (website hero, background): the last frame must match the first; build the timeline as a cycle and verify the seam by rendering twice the length once.

## Type on screen
- Minimum sizes at 1080p: body/captions 42 px (landscape) and 54 px (vertical); titles 96 px and up.
- Max ~8 words per line, max 2 lines of caption at a time.
- Contrast: text on footage gets a shade, a solid band, or an outline; check frames over the brightest part of the footage.
- Safe areas: landscape keep text 5% inside the edges; vertical keep it out of the top 220 px and bottom 380 px and away from the right-side button column.
- Numbers: tabular figures for counters and prices; `₱1,250` with the peso sign, not "P1250".

## Captions
- Burned in for social (most people watch muted); also export `captions.srt` for YouTube.
- Sentence case, natural line breaks at phrase boundaries, no orphan words.
- Taglish or Filipino: match how the speaker talks; do not machine-translate; keep one register for the whole video (see `anti-template` part 09).

## Sound
- Music bed about -18 to -20 dB under a voice; mix finishes near -14 LUFS for web/social (`motionv_verify.py` reports it).
- Fade music in over 0.3 s and out over 1-2 s; never cut it mid-bar at the end.
- Voiceover: the local voice (`npx hyperframes tts`, Kokoro) has English and a few other voices but no Filipino one; for Tagalog/Ilocano narration use the client's recorded voice or a TTS service with a fil-PH voice. Generated voice is fine; label it as generated if the client wants it disclosed. Never imitate a real person.

## Common briefs (Philippines clients)
| Brief | Shape |
|---|---|
| LGU / barangay announcement (FB page) | 1080x1350 or 1080x1080, 20-40 s, official seal only if the user supplies it, date/venue/time as the largest text, Filipino or English as the office writes it, end card with contact |
| School event or results | 16:9 for the screen at the event + 9:16 cut for reels; names spelled exactly from the source list |
| Product / POS / app promo | 15-30 s; real screenshots or `hyperframes capture` of the site, cursor-driven walkthrough, price and CTA on the end card |
| Explainer (process, how to register, how to pay) | 60-90 s, numbered steps, one idea per scene, voice + captions |
| Website hero loop | 6-12 s seamless, muted, low contrast so page text stays readable, MP4 + WebM ≤ 8 MB |
