#!/usr/bin/env python3
"""Check that a UI verification actually happened.

A report can claim three viewports passed. This checks the evidence behind the claim:
every promised width has a screenshot, each screenshot's real pixel width matches the width
its filename claims, and no two screenshots are the same file. Re-reporting one desktop
capture as the mobile pass fails here.

Screenshots are named <before|after>-<cssWidth>.png, e.g. after-390.png, after-1440.png.
The name is the claim; the pixels are the evidence.

Usage:
  python ui_verify.py .agents/verify/<task-slug>
  python ui_verify.py .agents/verify/dashboard --widths 390,768,1440 --require-before
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

DEFAULT_WIDTHS = (390, 768, 1440)
NAME = re.compile(r"^(before|after)-(\d{3,4})\.png$", re.I)
REQUIRED_KEYS = ("route", "widths", "status")


def _png_size(path: Path) -> tuple[int, int] | None:
    """Width and height from the PNG IHDR chunk — no image library needed."""
    try:
        head = path.read_bytes()[:33]
    except OSError:
        return None
    if len(head) < 33 or head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return (int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big"))


def verify(dirpath: Path, widths: tuple[int, ...], require_before: bool) -> dict:
    report: dict = {"dir": str(dirpath), "screenshots": [], "issues": [], "notes": []}

    if not dirpath.is_dir():
        report["issues"].append(f"no verification directory at {dirpath} — the gate did not run")
        report["status"] = "fail"
        return report

    # --- the verdict file
    verdict_path = dirpath / "verdict.json"
    verdict = None
    if not verdict_path.is_file():
        report["issues"].append("verdict.json missing — a report with no verdict file is a claim")
    else:
        try:
            verdict = json.loads(verdict_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            report["issues"].append(f"verdict.json is not valid JSON: {exc}")
        else:
            missing = [k for k in REQUIRED_KEYS if k not in verdict]
            if missing:
                report["issues"].append(f"verdict.json missing key(s): {', '.join(missing)}")

    # --- the screenshots
    shots, by_hash = {}, {}
    for png in sorted(dirpath.glob("*.png")):
        m = NAME.match(png.name)
        size = _png_size(png)
        digest = hashlib.sha256(png.read_bytes()).hexdigest()[:16]
        entry = {"file": png.name, "sha256_16": digest,
                 "pixels": list(size) if size else None}
        if not m:
            entry["note"] = "not named <before|after>-<width>.png; not counted as evidence"
            report["screenshots"].append(entry)
            continue
        state, claimed = m.group(1).lower(), int(m.group(2))
        entry["state"], entry["claimedWidth"] = state, claimed
        if size is None:
            report["issues"].append(f"{png.name}: not a readable PNG")
        else:
            # a screenshot may be captured at a device pixel ratio of 1, 2 or 3
            if not any(abs(size[0] - claimed * dpr) <= 2 for dpr in (1, 2, 3)):
                report["issues"].append(
                    f"{png.name} is {size[0]}px wide but its name claims {claimed}px "
                    f"(allowing 1x/2x/3x) — this screenshot was not taken at the width it reports")
        by_hash.setdefault(digest, []).append(png.name)
        shots.setdefault(state, {})[claimed] = entry
        report["screenshots"].append(entry)

    # --- the fabrication check: one capture reported as several
    for digest, names in by_hash.items():
        if len(names) > 1:
            report["issues"].append(
                f"identical image reported as different views: {', '.join(names)} "
                "(same bytes) — these cannot be captures of different widths or states")

    # --- coverage
    have_after = shots.get("after", {})
    for w in widths:
        if w not in have_after:
            report["issues"].append(f"no after-{w}.png — width {w} was never rendered")
    if require_before and not shots.get("before"):
        report["issues"].append(
            "no before-*.png — on a repair this is the only proof the defect existed")

    # --- the verdict must agree with itself
    if verdict is not None:
        status = str(verdict.get("status", "")).lower()
        claimed_widths = verdict.get("widths") or []
        for w in claimed_widths:
            if isinstance(w, int) and w not in have_after:
                report["issues"].append(
                    f"verdict.json claims width {w} was checked, but no after-{w}.png exists")
        if status == "pass":
            for field in ("consoleErrors", "failedRequests"):
                val = verdict.get(field)
                if isinstance(val, int) and val > 0:
                    report["issues"].append(
                        f"verdict says pass but {field} is {val} — that is a required failure")
        elif status not in ("fail", "skipped"):
            report["notes"].append(f"verdict status is '{status}' (expected pass, fail or skipped)")
        if status == "skipped" and not verdict.get("reason"):
            report["issues"].append("verdict is 'skipped' with no reason — name the blocked precondition")

    report["status"] = "fail" if report["issues"] else "pass"
    return report


def main() -> int:
    ap = argparse.ArgumentParser(description="Check that a UI verification actually happened")
    ap.add_argument("dir", type=Path, help=".agents/verify/<task-slug>")
    ap.add_argument("--widths", default=",".join(str(w) for w in DEFAULT_WIDTHS),
                    help="CSS widths that must have an after-<width>.png (default 390,768,1440)")
    ap.add_argument("--require-before", action="store_true",
                    help="a repair must also carry before-<width>.png")
    ap.add_argument("--report", type=Path, help="write the JSON result here")
    args = ap.parse_args()

    widths = tuple(int(w) for w in args.widths.split(",") if w.strip())
    result = verify(args.dir, widths, args.require_before)

    if args.report:
        args.report.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(f"{'[PASS]' if result['status'] == 'pass' else '[FAIL]'} {args.dir} — "
          f"{len([s for s in result['screenshots'] if s.get('claimedWidth')])} screenshot(s), "
          f"{len(result['issues'])} issue(s)")
    for issue in result["issues"]:
        print(f"  - {issue}")
    for note in result["notes"]:
        print(f"  . {note}")
    return 1 if result["status"] == "fail" else 0


if __name__ == "__main__":
    raise SystemExit(main())
