#!/usr/bin/env python3
"""Playwright smoke test (and lightweight accessibility pass) against a running URL.

Loads the page in headless Chromium and reports: HTTP status, uncaught page
errors, console errors, and visible elements with no accessible name (images
without alt, icon-only buttons/links, unlabeled form fields). Optional
full-page screenshot.

  fail     page did not load (network error / HTTP 4xx-5xx), uncaught JS errors,
           or accessibility errors (missing alt, unnamed controls, unlabeled fields)
  warn     console errors, missing <title>, zero or several <h1>

Playwright is optional: when the Python package or its browser is missing the
test is reported as SKIPPED (NOT VERIFIED) and the script exits 0.
Install: pip install playwright && python -m playwright install chromium

Usage:
    python playwright_runner.py <url> [--json] [--screenshot] [--screenshot-dir DIR]
                                [--a11y] [--mobile] [--timeout-ms 30000]

Exit codes: 0 passed or skipped, 1 failed, 2 usage error.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

try:
    from playwright.sync_api import sync_playwright
except ImportError:  # optional dependency
    sync_playwright = None

INSTALL_HINT = "pip install playwright && python -m playwright install chromium"

A11Y_PROBE = """() => {
  const visible = (el) => !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length)
      && getComputedStyle(el).visibility !== 'hidden';
  const byIds = (ids) => (ids || '').split(/\\s+/).map((id) => document.getElementById(id))
      .filter(Boolean).map((el) => el.textContent.trim()).join(' ');
  const name = (el) => (
      el.getAttribute('aria-label') || byIds(el.getAttribute('aria-labelledby')) ||
      (el.innerText || '').trim() ||
      [...el.querySelectorAll('img[alt]')].map((img) => img.alt).join(' ').trim() ||
      [...el.querySelectorAll('svg title')].map((t) => t.textContent).join(' ').trim() ||
      el.getAttribute('title') || '').trim();
  const describe = (el) => el.outerHTML.slice(0, 120);
  const unnamed = (selector) => [...document.querySelectorAll(selector)]
      .filter((el) => visible(el) && el.getAttribute('aria-hidden') !== 'true' && !name(el));
  const fields = [...document.querySelectorAll('input:not([type=hidden]):not([type=submit]):not([type=button]):not([type=reset]), select, textarea')]
      .filter((el) => visible(el) && !el.getAttribute('aria-label') && !byIds(el.getAttribute('aria-labelledby'))
          && !el.getAttribute('title') && !(el.labels && el.labels.length));
  const images = [...document.querySelectorAll('img:not([alt])')].filter(visible);
  const buttons = unnamed('button, [role=button]');
  const links = unnamed('a[href]');
  return {
    images_without_alt: images.map(describe).slice(0, 10),
    unnamed_buttons: buttons.map(describe).slice(0, 10),
    unnamed_links: links.map(describe).slice(0, 10),
    unlabeled_fields: fields.map(describe).slice(0, 10),
    counts: {images_without_alt: images.length, unnamed_buttons: buttons.length,
             unnamed_links: links.length, unlabeled_fields: fields.length},
    h1_count: document.querySelectorAll('h1').length,
    lang: document.documentElement.getAttribute('lang') || '',
  };
}"""


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


def run_test(url: str, screenshot: bool, accessibility_only: bool, timeout_ms: int,
             mobile: bool = False, screenshot_dir: Path | None = None) -> dict:
    result: dict = {"url": url, "timestamp": datetime.now(timezone.utc).isoformat()}
    if sync_playwright is None:
        return {**result, "status": "skipped", "passed": True, "reason": "Playwright is not installed", "fix": INSTALL_HINT}

    try:
        with sync_playwright() as runtime:
            try:
                browser = runtime.chromium.launch(headless=True)
            except Exception as exc:  # browser binary missing or cannot start
                message = str(exc).splitlines()[0][:300]
                if "Executable doesn't exist" in str(exc) or "playwright install" in str(exc):
                    return {**result, "status": "skipped", "passed": True, "reason": "Chromium for Playwright is not installed",
                            "fix": "python -m playwright install chromium"}
                return {**result, "status": "error", "passed": False, "error": f"browser launch failed: {message}"}
            viewport = {"width": 390, "height": 844} if mobile else {"width": 1440, "height": 900}
            context = browser.new_context(viewport=viewport, is_mobile=mobile, has_touch=mobile)
            page = context.new_page()
            console_errors: list[str] = []
            page_errors: list[str] = []
            page.on("console", lambda msg: console_errors.append(msg.text[:300]) if msg.type == "error" else None)
            page.on("pageerror", lambda err: page_errors.append(str(err)[:300]))

            # "load" is reliable; networkidle can hang on dev servers with open connections.
            response = page.goto(url, wait_until="load", timeout=timeout_ms)
            try:
                page.wait_for_load_state("networkidle", timeout=min(5000, timeout_ms))
            except Exception:
                pass  # long-polling / HMR: continue with the loaded page
            status_code = response.status if response else None
            title = page.title()
            a11y = page.evaluate(A11Y_PROBE)
            result.update({
                "viewport": viewport,
                "page": {"title": title, "final_url": page.url, "status_code": status_code},
                "accessibility": a11y,
                "console_errors": console_errors[:20],
                "page_errors": page_errors[:20],
            })
            if not accessibility_only:
                result["performance"] = page.evaluate("""() => {
                    const e = performance.getEntriesByType('navigation')[0];
                    return e ? {dom_content_loaded_ms: Math.round(e.domContentLoadedEventEnd),
                                load_ms: Math.round(e.loadEventEnd), response_ms: Math.round(e.responseEnd)} : {};
                }""")
            if screenshot:
                folder = screenshot_dir or Path(tempfile.gettempdir()) / "agkit_screenshots"
                folder.mkdir(parents=True, exist_ok=True)
                name = f"screenshot_{viewport['width']}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.png"
                page.screenshot(path=str(folder / name), full_page=True)
                result["screenshot"] = str(folder / name)
            context.close()
            browser.close()
    except Exception as exc:
        return {**result, "status": "error", "passed": False, "error": str(exc).splitlines()[0][:300]}

    failures, warnings = [], []
    if status_code is None or status_code >= 400:
        failures.append(f"HTTP status {status_code}")
    if page_errors:
        failures.append(f"{len(page_errors)} uncaught page error(s)")
    blocking = {k: v for k, v in a11y["counts"].items() if v}
    if blocking:
        failures.append("accessibility: " + ", ".join(f"{v} {k.replace('_', ' ')}" for k, v in blocking.items()))
    if console_errors:
        warnings.append(f"{len(console_errors)} console error(s)")
    if not title:
        warnings.append("page has no <title>")
    if a11y["h1_count"] != 1:
        warnings.append(f"{a11y['h1_count']} <h1> elements")
    if not a11y["lang"]:
        warnings.append("<html> has no lang")
    result.update({"failures": failures, "warnings": warnings, "passed": not failures,
                   "status": "passed" if not failures else "failed"})
    return result


def main() -> int:
    utf8_console()
    parser = argparse.ArgumentParser(description="Playwright smoke test and quick accessibility pass for a URL")
    parser.add_argument("url", type=valid_url, help="running page URL, e.g. http://localhost:3000")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    parser.add_argument("--screenshot", action="store_true", help="save a full-page screenshot")
    parser.add_argument("--screenshot-dir", type=Path, help="folder for screenshots (default: system temp/agkit_screenshots)")
    parser.add_argument("--a11y", action="store_true", help="accessibility checks only (skip timing)")
    parser.add_argument("--mobile", action="store_true", help="390x844 touch viewport (default 1440x900)")
    parser.add_argument("--timeout-ms", type=int, default=30000)
    args = parser.parse_args()
    result = run_test(args.url, args.screenshot, args.a11y, args.timeout_ms, args.mobile, args.screenshot_dir)
    code = 0 if result.get("passed") else 1

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return code
    print(f"Playwright smoke: {args.url}")
    if result["status"] == "skipped":
        print(f"  fix: {result['fix']}\nSKIPPED: {result['reason']}. NOT VERIFIED.")
        return 0
    if result["status"] == "error":
        print(f"ERROR: {result['error']}")
        return 1
    page = result["page"]
    print(f"  HTTP {page['status_code']}  title: {page['title'] or '(none)'}  viewport: {result['viewport']['width']}px")
    for item in result["failures"]:
        print(f"  FAIL  {item}")
    for key in ("images_without_alt", "unnamed_buttons", "unnamed_links", "unlabeled_fields"):
        for html in result["accessibility"][key][:3]:
            print(f"        {key}: {html}")
    for item in result["page_errors"][:3]:
        print(f"        page error: {item}")
    for item in result["warnings"]:
        print(f"  warn  {item}")
    for item in result["console_errors"][:3]:
        print(f"        console: {item}")
    if result.get("performance"):
        print("  timing: " + ", ".join(f"{k}={v}" for k, v in result["performance"].items()))
    if result.get("screenshot"):
        print(f"  screenshot: {result['screenshot']}")
    print(f"\nResult: {'PASS' if result['passed'] else 'FAIL'}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
