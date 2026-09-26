#!/usr/bin/env python3
"""Analyze built JavaScript/CSS asset sizes without external dependencies.

Looks in the usual client build folders (Next.js .next/static, Vite/Astro dist,
Laravel Vite public/build, CRA build/static, React Router build/client, Nuxt
.output/public, SvelteKit .svelte-kit/output/client). Server bundles and source
maps are ignored. Build the project first; with no build output the script
reports SKIP and exits 0.

  high    a single asset over --file-fail-kib (default 750 KiB raw)
  medium  an asset over --file-warn-kib (default 250 KiB), or total client JS
          over --total-js-fail-kib (default 2048 KiB; large apps may exceed it)

Usage:
    python bundle_analyzer.py <project> [--json | --output json|summary] [--fail-on none|low|medium|high|critical]

Exit codes: 0 ok, 1 finding at/above --fail-on (default: high), 2 usage error.
"""
from __future__ import annotations

import argparse
import gzip
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SKIP_DIRS = {"node_modules", ".git", ".agents", ".agent", ".venv", "venv"}
BUILD_ROOTS = (".next/static", "dist", "build/static", "build/assets", "build/client", "out/_next/static",
               "public/build", ".output/public", ".svelte-kit/output/client")
SERVER_DIRS = {"server", "ssr", "chunks-server"}
SEVERITY = {"none": 99, "low": 1, "medium": 2, "high": 3, "critical": 4}


def human_bytes(value: int) -> str:
    units = ("B", "KiB", "MiB", "GiB")
    size = float(value)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{value} B"


def analyze(root: Path, file_warn_kib: int, file_fail_kib: int, total_fail_kib: int) -> dict[str, Any]:
    assets: list[dict[str, Any]] = []
    seen: set[Path] = set()
    for relative in BUILD_ROOTS:
        build_root = root / relative
        if not build_root.is_dir():
            continue
        for path in build_root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".js", ".mjs", ".css"}:
                continue
            if SERVER_DIRS & {part.lower() for part in path.relative_to(build_root).parts[:-1]}:
                continue
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            try:
                data = path.read_bytes()
            except OSError:
                continue
            assets.append({
                "file": path.relative_to(root).as_posix(),
                "type": path.suffix.lower().lstrip("."),
                "bytes": len(data),
                "gzip_bytes": len(gzip.compress(data, compresslevel=6)),
            })

    findings: list[dict[str, Any]] = []
    for asset in assets:
        kib = asset["bytes"] / 1024
        if kib >= file_fail_kib:
            findings.append({"severity": "high", "issue": "Oversized asset", "file": asset["file"], "size": human_bytes(asset["bytes"])})
        elif kib >= file_warn_kib:
            findings.append({"severity": "medium", "issue": "Large asset", "file": asset["file"], "size": human_bytes(asset["bytes"])})

    js_total = sum(a["bytes"] for a in assets if a["type"] in {"js", "mjs"})
    if js_total / 1024 >= total_fail_kib:
        findings.append({"severity": "medium", "issue": "Large total JavaScript payload", "file": "<all JS assets>", "size": human_bytes(js_total)})

    assets.sort(key=lambda item: item["bytes"], reverse=True)
    counts = {severity: sum(f["severity"] == severity for f in findings) for severity in ("critical", "high", "medium", "low")}
    return {
        "project": str(root),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "build_roots_checked": [name for name in BUILD_ROOTS if (root / name).is_dir()],
        "asset_count": len(assets),
        "totals": {
            "bytes": sum(a["bytes"] for a in assets),
            "gzip_bytes": sum(a["gzip_bytes"] for a in assets),
            "javascript_bytes": js_total,
            "css_bytes": sum(a["bytes"] for a in assets if a["type"] == "css"),
        },
        "largest_assets": assets[:30],
        "findings": findings,
        "summary": {"total": len(findings), **counts},
    }


def should_fail(report: dict[str, Any], threshold: str) -> bool:
    if threshold == "none":
        return False
    rank = SEVERITY[threshold]
    return any(report["summary"].get(level, 0) and value >= rank for level, value in SEVERITY.items() if level != "none")


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    parser = argparse.ArgumentParser(description="Audit generated JavaScript and CSS bundle sizes")
    parser.add_argument("project", nargs="?", default=".", help="project directory (default: .)")
    parser.add_argument("--output", choices=["json", "summary"], default="summary")
    parser.add_argument("--json", action="store_true", help="same as --output json")
    parser.add_argument("--file-warn-kib", type=int, default=250)
    parser.add_argument("--file-fail-kib", type=int, default=750)
    parser.add_argument("--total-js-fail-kib", type=int, default=2048)
    parser.add_argument("--fail-on", choices=list(SEVERITY), default="high",
                        help="exit 1 when a finding at or above this severity exists (default: high)")
    args = parser.parse_args()
    root = Path(args.project).expanduser().resolve()
    if not root.is_dir():
        parser.error(f"Project directory does not exist: {root}")
    report = analyze(root, args.file_warn_kib, args.file_fail_kib, args.total_js_fail_kib)
    failed = should_fail(report, args.fail_on)
    if args.json or args.output == "json":
        print(json.dumps({**report, "passed": not failed}, indent=2, ensure_ascii=False))
        return 1 if failed else 0
    totals = report["totals"]
    print(f"Bundle analysis: {root}")
    if not report["build_roots_checked"]:
        print("SKIP: no client build output found (build the project first). NOT VERIFIED.")
        return 0
    print(f"Build folders: {', '.join(report['build_roots_checked'])}")
    print(f"{report['asset_count']} asset(s): JS {human_bytes(totals['javascript_bytes'])}, "
          f"CSS {human_bytes(totals['css_bytes'])}, gzip total {human_bytes(totals['gzip_bytes'])}")
    print("Largest:")
    for asset in report["largest_assets"][:8]:
        print(f"  {human_bytes(asset['bytes']):>10}  ({human_bytes(asset['gzip_bytes'])} gzip)  {asset['file']}")
    for finding in report["findings"]:
        print(f"  {finding['severity']:<7} {finding['issue']}: {finding['file']} ({finding['size']})")
    print(f"\nResult: {'FAIL' if failed else 'PASS'} - JS {human_bytes(totals['javascript_bytes'])}, "
          f"{len(report['findings'])} finding(s) (fail-on: {args.fail_on})")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
