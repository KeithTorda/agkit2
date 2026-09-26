#!/usr/bin/env python3
"""Check that a UI verification actually happened.

A report can claim several widths passed. This checks the evidence behind the claim: every
promised width has a screenshot, each screenshot's pixel width matches the width its filename
claims (at a device pixel ratio of 1, 1.25, 1.5, 2 or 3), and no two screenshots are the same file.

Screenshots are named <before|after>-<cssWidth>.png, e.g. after-390.png, after-1440.png.
The name is the claim; the pixels are the evidence.

Widths: --widths wins; otherwise the widths listed in verdict.json; otherwise 390,1440 (one
mobile and one desktop, per code-rules). A verdict with status "skipped" and a reason (no dev
server, no browser) is an honest skip and exits 0.

Usage:
  python ui_verify.py .agents/verify/<task-slug>
  python ui_verify.py .agents/verify/dashboard --widths 390,768,1440 --require-before --json
Exit codes: 0 verified (or honestly skipped), 1 evidence missing or contradicting the claim, 2 usage.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

DEFAULT_WIDTHS = (390, 1440)
DEVICE_PIXEL_RATIOS = (1, 1.25, 1.5, 1.75, 2, 2.5, 3)
NAME = re.compile(r"^(before|after)-(\d{3,4})\.png$", re.I)
REQUIRED_KEYS = ("route", "widths", "status")


def _png_size(path: Path) -> tuple[int, int] | None:
    """Width and height from the PNG IHDR chunk - no image library needed."""
    try:
        with path.open("rb") as fh:
            head = fh.read(24)
    except OSError:
        return None
    if len(head) < 24 or head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        return None
    return int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big")


def _digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def _as_width(value: object) -> int | None:
    try:
        return int(str(value).strip().rstrip("px"))
    except ValueError:
        return None


def verify(dirpath: Path, widths: tuple[int, ...] | None = None, require_before: bool = False) -> dict:
    report: dict = {"dir": str(dirpath), "screenshots": [], "issues": [], "notes": []}

    if not dirpath.is_dir():
        report["issues"].append(f"no verification directory at {dirpath} - the check did not run")
        report["status"] = "fail"
        return report

    verdict_path = dirpath / "verdict.json"
    verdict: dict | None = None
    if not verdict_path.is_file():
        report["issues"].append("verdict.json missing - a report with no verdict file is only a claim")
    else:
        try:
            loaded = json.loads(verdict_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            report["issues"].append(f"verdict.json is not valid JSON: {exc}")
        else:
            if not isinstance(loaded, dict):
                report["issues"].append("verdict.json must be a JSON object")
            else:
                verdict = loaded
                missing = [k for k in REQUIRED_KEYS if k not in verdict]
                if missing:
                    report["issues"].append(f"verdict.json missing key(s): {', '.join(missing)}")

    status = str((verdict or {}).get("status", "")).lower()
    if status == "skipped":
        if verdict and verdict.get("reason"):
            report["notes"].append(f"verification skipped: {verdict['reason']}")
            report["status"] = "skipped" if not report["issues"] else "fail"
        else:
            report["issues"].append("verdict is 'skipped' with no reason - name the missing precondition")
            report["status"] = "fail"
        return report

    claimed_widths = [w for w in (_as_width(x) for x in ((verdict or {}).get("widths") or [])) if w]
    wanted = tuple(widths) if widths else (tuple(claimed_widths) or DEFAULT_WIDTHS)
    report["widths"] = list(wanted)

    shots: dict[str, dict[int, dict]] = {}
    by_hash: dict[str, list[str]] = {}
    for png in sorted(dirpath.glob("*.png")):
        m = NAME.match(png.name)
        size = _png_size(png)
        digest = _digest(png)
        entry: dict = {"file": png.name, "sha256_16": digest, "pixels": list(size) if size else None}
        if not m:
            entry["note"] = "not named <before|after>-<width>.png; not counted as evidence"
            report["screenshots"].append(entry)
            continue
        state, claimed = m.group(1).lower(), int(m.group(2))
        entry["state"], entry["claimedWidth"] = state, claimed
        if size is None:
            report["issues"].append(f"{png.name}: not a readable PNG")
        elif not any(abs(size[0] - claimed * dpr) <= 2 for dpr in DEVICE_PIXEL_RATIOS):
            report["issues"].append(
                f"{png.name} is {size[0]}px wide but its name claims {claimed}px - this screenshot was not "
                "taken at the width it reports")
        by_hash.setdefault(digest, []).append(png.name)
        shots.setdefault(state, {})[claimed] = entry
        report["screenshots"].append(entry)

    for names in by_hash.values():
        if len(names) > 1:
            report["issues"].append(
                f"identical image reported as different views: {', '.join(names)} (same bytes) - these cannot "
                "be captures of different widths or states")

    have_after = shots.get("after", {})
    for w in wanted:
        if w not in have_after:
            report["issues"].append(f"no after-{w}.png - width {w} was never rendered")
    if require_before and not shots.get("before"):
        report["issues"].append("no before-*.png - on a repair this is the only proof the defect existed")

    if verdict is not None:
        for w in claimed_widths:
            if w not in have_after:
                report["issues"].append(f"verdict.json claims width {w} was checked, but no after-{w}.png exists")
        if status == "pass":
            for key in ("consoleErrors", "failedRequests"):
                val = verdict.get(key)
                if isinstance(val, int) and val > 0:
                    report["issues"].append(f"verdict says pass but {key} is {val} - that is a failure")
        elif status and status != "fail":
            report["notes"].append(f"verdict status is '{status}' (expected pass, fail or skipped)")
        if status == "fail":
            report["notes"].append("verdict.json records a failed verification")

    report["status"] = "fail" if report["issues"] or status == "fail" else "pass"
    return report


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description="Check that a UI verification actually happened.",
                                 epilog="Exit codes: 0 verified or honestly skipped, 1 evidence problem, 2 usage.")
    ap.add_argument("dir", type=Path, help=".agents/verify/<task-slug>")
    ap.add_argument("--widths", help="CSS widths that need an after-<width>.png (default: verdict.json, else 390,1440)")
    ap.add_argument("--require-before", action="store_true", help="a repair must also carry before-<width>.png")
    ap.add_argument("--json", action="store_true", help="print the result as JSON")
    ap.add_argument("--report", type=Path, help="also write the JSON result here")
    args = ap.parse_args(argv)

    widths = None
    if args.widths:
        try:
            widths = tuple(int(w) for w in args.widths.split(",") if w.strip())
        except ValueError:
            ap.error("--widths must be comma-separated integers, e.g. 390,1440")
    result = verify(args.dir, widths, args.require_before)

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2), encoding="utf-8")
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        label = {"pass": "[PASS]", "skipped": "[SKIP]"}.get(result["status"], "[FAIL]")
        counted = len([s for s in result["screenshots"] if s.get("claimedWidth")])
        print(f"{label} {args.dir} - {counted} screenshot(s), {len(result['issues'])} issue(s)")
        for issue in result["issues"]:
            print(f"  - {issue}")
        for note in result["notes"]:
            print(f"  . {note}")
    return 1 if result["status"] == "fail" else 0


if __name__ == "__main__":
    raise SystemExit(main())
