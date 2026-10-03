#!/usr/bin/env python3
"""motionv_verify.py - check a rendered video against its target and make a contact sheet to look at.

Reports: container, codec, resolution, aspect, fps, duration, audio presence and loudness, file size,
black/frozen stretches. Writes <outdir>/contact-sheet.png (a grid of frames across the timeline) and
<outdir>/frame-XX.png so the agent can open and look at the actual output.

Usage:
  python motionv_verify.py renders/final.mp4 --preset reels --duration 30
  python motionv_verify.py renders/final.mp4 --width 1920 --height 1080 --fps 30 --frames 12 --json

Exit codes: 0 matches the target, 1 a required check failed, 2 usage / file error.
Requires ffmpeg and ffprobe on PATH.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

PRESETS = {
    # name: (width, height, fps, max_seconds or None, max_mb or None)
    "youtube": (1920, 1080, 30, None, None),
    "youtube-4k": (3840, 2160, 30, None, None),
    "reels": (1080, 1920, 30, 90, None),
    "tiktok": (1080, 1920, 30, 600, None),
    "shorts": (1080, 1920, 30, 180, None),
    "square": (1080, 1080, 30, None, None),
    "feed-4x5": (1080, 1350, 30, None, None),
    "hero": (1920, 1080, 30, 30, 8),   # website hero loop: short, muted, light
}


def sh(cmd: list[str], timeout: int = 600) -> tuple[int, str, str]:
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def probe(path: Path) -> dict:
    code, out, err = sh(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)])
    if code != 0:
        raise RuntimeError(err.strip() or "ffprobe failed")
    return json.loads(out)


def fps_of(stream: dict) -> float:
    num, _, den = (stream.get("avg_frame_rate") or stream.get("r_frame_rate") or "0/1").partition("/")
    try:
        return float(num) / float(den or 1)
    except ZeroDivisionError:
        return 0.0


def loudness(path: Path) -> float | None:
    code, _, err = sh(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=framelog=quiet",
                       "-f", "null", "-"], timeout=900)
    m = re.findall(r"I:\s+(-?\d+(?:\.\d+)?) LUFS", err)
    return float(m[-1]) if m else None


def detect(path: Path, filt: str, key: str, timeout: int = 900) -> list[tuple[float, float]]:
    _, _, err = sh(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-vf", filt, "-an", "-f", "null", "-"],
                   timeout=timeout)
    spans = []
    if key == "black":
        for s, e in re.findall(r"black_start:(\d+\.?\d*) black_end:(\d+\.?\d*)", err):
            spans.append((float(s), float(e)))
    else:  # freeze
        starts = [float(x) for x in re.findall(r"freeze_start: (\d+\.?\d*)", err)]
        ends = [float(x) for x in re.findall(r"freeze_end: (\d+\.?\d*)", err)]
        spans = list(zip(starts, ends + [math.inf] * (len(starts) - len(ends))))
    return spans


def contact_sheet(path: Path, outdir: Path, duration: float, frames: int, width: int, height: int) -> list[Path]:
    outdir.mkdir(parents=True, exist_ok=True)
    shots = []
    for i in range(frames):
        t = duration * (i + 0.5) / frames
        f = outdir / f"frame-{i + 1:02d}.png"
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(path), "-frames:v", "1",
            "-vf", "scale=480:-2", str(f)])
        if f.exists():
            shots.append(f)
    if shots:
        cols = 4 if width >= height else 6
        inputs = []
        for s in shots:
            inputs += ["-i", str(s)]
        parts = []  # xstack layout: column offsets as w0+w0..., row offsets as h0+h0...
        for i in range(len(shots)):
            c, r = i % cols, i // cols
            x = "+".join(["w0"] * c) or "0"
            y = "+".join(["h0"] * r) or "0"
            parts.append(f"{x}_{y}")
        layout = "|".join(parts)
        filt = (f"xstack=inputs={len(shots)}:layout={layout}:fill=black" if len(shots) > 1 else "null")
        sh(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", filt, "-frames:v", "1",
            str(outdir / "contact-sheet.png")])
    return shots


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify a rendered video and build a contact sheet.")
    ap.add_argument("video", type=Path)
    ap.add_argument("--preset", choices=sorted(PRESETS))
    ap.add_argument("--width", type=int)
    ap.add_argument("--height", type=int)
    ap.add_argument("--fps", type=float)
    ap.add_argument("--duration", type=float, help="expected duration in seconds (±0.5 s)")
    ap.add_argument("--audio", choices=["required", "none", "any"], default="any")
    ap.add_argument("--frames", type=int, default=8, help="frames in the contact sheet (default 8)")
    ap.add_argument("--outdir", type=Path, help="default: <video folder>/verify-<video name>")
    ap.add_argument("--no-scan", action="store_true", help="skip loudness and black/freeze scans (faster)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if not shutil.which("ffprobe") or not shutil.which("ffmpeg"):
        print("ffmpeg/ffprobe not on PATH - run motionv_doctor.py", file=sys.stderr)
        return 2
    if not a.video.is_file():
        print(f"not found: {a.video}", file=sys.stderr)
        return 2

    w_t, h_t, fps_t, max_s, max_mb = (None,) * 5
    if a.preset:
        w_t, h_t, fps_t, max_s, max_mb = PRESETS[a.preset]
        if a.preset == "hero" and a.audio == "any":
            a.audio = "none"
    w_t, h_t, fps_t = a.width or w_t, a.height or h_t, a.fps or fps_t

    try:
        info = probe(a.video)
    except RuntimeError as e:
        print(f"cannot read video: {e}", file=sys.stderr)
        return 2
    v = next((s for s in info["streams"] if s.get("codec_type") == "video"), None)
    au = next((s for s in info["streams"] if s.get("codec_type") == "audio"), None)
    if not v:
        print("no video stream", file=sys.stderr)
        return 2
    dur = float(info["format"].get("duration") or v.get("duration") or 0)
    size_mb = a.video.stat().st_size / 1_048_576
    fps = fps_of(v)
    facts = {
        "file": str(a.video), "container": info["format"].get("format_name"), "video_codec": v.get("codec_name"),
        "pix_fmt": v.get("pix_fmt"), "width": v.get("width"), "height": v.get("height"), "fps": round(fps, 3),
        "duration_s": round(dur, 3), "size_mb": round(size_mb, 2),
        "audio_codec": au.get("codec_name") if au else None,
    }

    checks: list[dict] = []

    def check(name: str, ok: bool, detail: str, required: bool = True) -> None:
        checks.append({"name": name, "ok": ok, "required": required, "detail": detail})

    if w_t and h_t:
        check("resolution", (v.get("width"), v.get("height")) == (w_t, h_t), f"{v.get('width')}x{v.get('height')} (target {w_t}x{h_t})")
    if fps_t:
        check("fps", abs(fps - fps_t) < 0.05, f"{fps:.3f} (target {fps_t})")
    if a.duration:
        check("duration", abs(dur - a.duration) <= 0.5, f"{dur:.2f}s (target {a.duration}s)")
    if max_s:
        check("platform max length", dur <= max_s, f"{dur:.1f}s (max {max_s}s)")
    if max_mb:
        check("file size", size_mb <= max_mb, f"{size_mb:.1f} MB (max {max_mb} MB)", required=False)
    check("playable pixel format", v.get("pix_fmt") in ("yuv420p", "yuvj420p", None) or facts["container"] not in ("mov,mp4,m4a,3gp,3g2,mj2",),
          f"{v.get('pix_fmt')} (yuv420p plays everywhere)", required=False)
    if a.audio == "required":
        check("audio track", au is not None, "present" if au else "missing")
    elif a.audio == "none":
        check("no audio (muted hero/loop)", au is None, "none" if not au else "has audio - strip with -an", required=False)

    if not a.no_scan:
        if au is not None:
            lufs = loudness(a.video)
            facts["loudness_lufs"] = lufs
            if lufs is not None:
                check("loudness", -18 <= lufs <= -11, f"{lufs:.1f} LUFS (web/social target about -14)", required=False)
        black = detect(a.video, "blackdetect=d=0.5:pix_th=0.01", "black")
        facts["black_spans"] = black
        check("no long black stretches", not any(e - s > 1.0 for s, e in black),
              ", ".join(f"{s:.1f}-{e:.1f}s" for s, e in black) or "none", required=False)
        frozen = detect(a.video, "freezedetect=n=0.001:d=2", "freeze")
        facts["frozen_spans"] = frozen
        check("no frozen stretches > 2 s", not frozen,
              ", ".join(f"{s:.1f}s-" + ("end" if e == math.inf else f"{e:.1f}s") for s, e in frozen) or "none",
              required=False)

    outdir = a.outdir or a.video.parent / f"verify-{a.video.stem}"
    shots = contact_sheet(a.video, outdir, dur, max(1, a.frames), v.get("width") or 1, v.get("height") or 1)
    facts["contact_sheet"] = str(outdir / "contact-sheet.png") if (outdir / "contact-sheet.png").exists() else None
    facts["frames"] = [str(s) for s in shots]

    failed = [c for c in checks if c["required"] and not c["ok"]]
    if a.json:
        print(json.dumps({"ok": not failed, "facts": facts, "checks": checks}, indent=2))
    else:
        print(f"motionv verify: {a.video}")
        print(f"  {facts['width']}x{facts['height']} @ {facts['fps']} fps · {facts['duration_s']} s · "
              f"{facts['video_codec']}/{facts['pix_fmt']} · audio: {facts['audio_codec'] or 'none'} · {facts['size_mb']} MB")
        for c in checks:
            mark = "ok  " if c["ok"] else ("FAIL" if c["required"] else "warn")
            print(f"  [{mark}] {c['name']:<28} {c['detail']}")
        print(f"  Look at: {facts['contact_sheet'] or outdir}")
        print("Result: PASS" if not failed else f"Result: FAIL - {len(failed)} required check(s)")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
