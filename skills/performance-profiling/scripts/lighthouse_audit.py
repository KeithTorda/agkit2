#!/usr/bin/env python3
"""Run a Lighthouse audit against a running URL and compare scores with thresholds.

Uses a project-local node_modules/.bin/lighthouse or one on PATH; it never
downloads Lighthouse. When Lighthouse or Chrome is missing the audit is
reported as SKIPPED (NOT VERIFIED) and the script exits 0 - it does not pass
or fail the page. Install with `npm install -g lighthouse` (needs Chrome).

Lab runs have no real user interaction, so INP is not measured; TBT is the lab proxy.

Usage:
    python lighthouse_audit.py <url> [--json] [--min-performance 50] [--min-accessibility 80]
                               [--min-best-practices 80] [--min-seo 80] [--desktop] [--timeout 180]

Exit codes: 0 thresholds met or audit skipped, 1 a threshold missed or the
page could not be audited, 2 usage error.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse

CATEGORIES = (("performance", "performance"), ("accessibility", "accessibility"),
              ("best-practices", "best_practices"), ("seo", "seo"))
MISSING_CHROME = ("No Chrome installations found", "CHROME_PATH", "Unable to connect to Chrome", "ECONNREFUSED 127.0.0.1")


def utf8_console() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def valid_url(value: str) -> str:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise argparse.ArgumentTypeError("URL must start with http:// or https://")
    return value


def find_lighthouse() -> str | None:
    local = Path.cwd() / "node_modules" / ".bin"
    for name in (("lighthouse.cmd", "lighthouse") if os.name == "nt" else ("lighthouse",)):
        if (local / name).is_file():
            return str(local / name)
    return shutil.which("lighthouse")


def run_lighthouse(url: str, timeout: int = 180, mobile: bool = True, chrome_flags: str = "--headless=new") -> dict:
    executable = find_lighthouse()
    if not executable:
        return {"url": url, "status": "skipped", "reason": "Lighthouse CLI not found",
                "fix": "npm install -g lighthouse (or npx lighthouse <url> once, with network access)"}

    fd, raw_path = tempfile.mkstemp(prefix="agkit-lighthouse-", suffix=".json")
    os.close(fd)
    output_path = Path(raw_path)
    cmd = [executable, url, "--output=json", f"--output-path={output_path}", f"--chrome-flags={chrome_flags}",
           "--only-categories=performance,accessibility,best-practices,seo", "--quiet"]
    if not mobile:
        cmd.append("--preset=desktop")
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                              timeout=timeout, check=False, stdin=subprocess.DEVNULL)
        if proc.returncode != 0 and (not output_path.exists() or output_path.stat().st_size == 0):
            stderr = (proc.stderr or "")[-1500:]
            if any(marker in stderr for marker in MISSING_CHROME):
                return {"url": url, "status": "skipped", "reason": "Chrome not found or not startable",
                        "fix": "install Chrome/Chromium or set CHROME_PATH; in containers add --chrome-flags=\"--headless=new --no-sandbox\""}
            return {"url": url, "status": "error", "error": "Lighthouse run failed", "stderr": stderr}
        report = json.loads(output_path.read_text("utf-8", errors="replace"))
    except subprocess.TimeoutExpired:
        return {"url": url, "status": "error", "error": f"Lighthouse timed out after {timeout}s"}
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return {"url": url, "status": "error", "error": str(exc)}
    finally:
        output_path.unlink(missing_ok=True)

    if report.get("runtimeError", {}).get("code"):
        return {"url": url, "status": "error", "error": report["runtimeError"].get("message", "runtime error")}
    categories = report.get("categories", {})
    scores = {}
    for key, label in CATEGORIES:
        raw = categories.get(key, {}).get("score")
        scores[label] = None if raw is None else round(float(raw) * 100)
    audits = report.get("audits", {})
    metrics = {}
    for key, label in (("first-contentful-paint", "fcp_ms"), ("largest-contentful-paint", "lcp_ms"),
                       ("cumulative-layout-shift", "cls"), ("total-blocking-time", "tbt_ms"),
                       ("speed-index", "speed_index_ms")):
        value = audits.get(key, {}).get("numericValue")
        if value is not None:
            metrics[label] = round(float(value), 3 if label == "cls" else 0)
    failing_audits = sorted(
        ((a.get("title", k), a.get("score")) for k, a in audits.items()
         if a.get("scoreDisplayMode") == "binary" and a.get("score") == 0),
        key=lambda item: item[0])[:10]
    return {"url": url, "status": "success", "form_factor": "mobile" if mobile else "desktop",
            "scores": scores, "metrics": metrics, "failing_audits": [t for t, _ in failing_audits]}


def main() -> int:
    utf8_console()
    parser = argparse.ArgumentParser(description="Run Lighthouse and compare category scores with thresholds")
    parser.add_argument("url", type=valid_url, help="running page URL, e.g. http://localhost:3000")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    parser.add_argument("--min-performance", type=int, default=50)
    parser.add_argument("--min-accessibility", type=int, default=80)
    parser.add_argument("--min-best-practices", type=int, default=80)
    parser.add_argument("--min-seo", type=int, default=80)
    parser.add_argument("--desktop", action="store_true", help="desktop preset (default: Lighthouse mobile emulation)")
    parser.add_argument("--chrome-flags", default="--headless=new", help="flags passed to Chrome (default: --headless=new)")
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()

    result = run_lighthouse(args.url, args.timeout, not args.desktop, args.chrome_flags)
    thresholds = {"performance": args.min_performance, "accessibility": args.min_accessibility,
                  "best_practices": args.min_best_practices, "seo": args.min_seo}
    if result["status"] == "success":
        failures = [name for name, minimum in thresholds.items()
                    if result["scores"].get(name) is not None and result["scores"][name] < minimum]
        result.update({"thresholds": thresholds, "failed_thresholds": failures, "passed": not failures})
    else:
        result["passed"] = result["status"] == "skipped"
    exit_code = 0 if result["passed"] else 1

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return exit_code
    print(f"Lighthouse: {args.url}")
    if result["status"] == "skipped":
        print(f"  fix: {result['fix']}\nSKIPPED: {result['reason']}. NOT VERIFIED.")
        return 0
    if result["status"] == "error":
        print(f"ERROR: {result['error']}")
        if result.get("stderr"):
            print("  " + result["stderr"].strip().replace("\n", "\n  "))
        return 1
    for name, score in result["scores"].items():
        minimum = thresholds[name]
        mark = "n/a " if score is None else ("ok  " if score >= minimum else "LOW ")
        print(f"  {mark} {name:<15} {'-' if score is None else score:>3}  (min {minimum})")
    metrics = result["metrics"]
    if metrics:
        print("  " + ", ".join(f"{k}={v:g}" for k, v in metrics.items()))
    if result["failing_audits"]:
        print("  failing audits: " + "; ".join(result["failing_audits"]))
    print(f"\nResult: {'PASS' if result['passed'] else 'FAIL'} ({result['form_factor']})")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
