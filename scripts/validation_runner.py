#!/usr/bin/env python3
"""Shared step runner for checklist.py and verify_all.py (not an entry point).

A Step is one check: a command (or a few commands run in sequence), whether it is required,
and why it might be skipped. Required checks gate the exit code; advisory checks are reported
and never fail a run unless the caller passes strict=True.

Result statuses:
  passed    the command exited 0
  failed    required: a blocking failure; advisory: findings to report
  skipped   not applicable here (no changed files of that kind, no URL, --quick)
  missing   the tool is not installed or not configured - a note, never a failure
  error     the check itself broke (crash, unexpected exit code, advisory timeout)

Python 3.10+, standard library only, Windows-safe (no shell, UTF-8 decoding, .cmd shims
resolved by shutil.which).
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, TextIO

KIT_ROOT = Path(__file__).resolve().parents[1]
STATUSES = ("passed", "failed", "skipped", "missing", "error")
OUTPUT_KEEP = 4000


def utf8_stdio() -> None:
    """Windows consoles default to cp1252; never crash on a non-ASCII character."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
        except (AttributeError, ValueError):
            pass


@dataclass
class Step:
    name: str
    category: str                      # security | types | tests | lint | build | audit | runtime
    commands: list[list[str]] = field(default_factory=list)
    required: bool = False
    cwd: Path | None = None
    timeout: int = 300
    kit_script: bool = False           # kit scripts: exit 1 = findings, >1 = the script broke
    skip_reason: str = ""              # set -> status "skipped"
    missing_reason: str = ""           # set -> status "missing"
    detail_regex: str = ""             # matches joined into the summary detail (else: last output line)


@dataclass
class CheckResult:
    name: str
    category: str
    status: str
    required: bool
    duration_seconds: float = 0.0
    commands: list[list[str]] = field(default_factory=list)
    exit_code: int | None = None
    detail: str = ""
    stdout: str = ""
    stderr: str = ""

    @property
    def blocking(self) -> bool:
        return self.required and self.status == "failed"

    @property
    def kind(self) -> str:
        return "required" if self.required else "advisory"


class Console:
    """Progress output. In JSON mode progress goes to stderr so stdout stays parseable."""

    def __init__(self, stream: TextIO | None = None, quiet: bool = False) -> None:
        self.stream = stream or sys.stdout
        self.quiet = quiet
        colour = hasattr(self.stream, "isatty") and self.stream.isatty() and "NO_COLOR" not in os.environ
        self.red = "\033[91m" if colour else ""
        self.green = "\033[92m" if colour else ""
        self.yellow = "\033[93m" if colour else ""
        self.dim = "\033[2m" if colour else ""
        self.end = "\033[0m" if colour else ""

    def line(self, text: str = "") -> None:
        if not self.quiet:
            print(text, file=self.stream, flush=True)


def _tail(text: str, limit: int = OUTPUT_KEEP) -> str:
    text = text.strip()
    return text if len(text) <= limit else "..." + text[-limit:]


def _detail_from(output: str) -> str:
    """The last meaningful line of a tool's output: usually its summary."""
    for raw in reversed(output.strip().splitlines()):
        line = " ".join(raw.split())
        if line and not set(line) <= set("=-_*~ "):
            return line[:90]
    return ""


def _decode(value: str | bytes | None) -> str:
    if value is None:
        return ""
    return value.decode("utf-8", errors="replace") if isinstance(value, bytes) else value


def run_step(step: Step, console: Console | None = None) -> CheckResult:
    console = console or Console(quiet=True)
    result = CheckResult(step.name, step.category, "skipped", step.required, commands=step.commands)
    if step.skip_reason:
        result.detail = step.skip_reason
        console.line(f"{console.dim}[skip] {step.name}: {step.skip_reason}{console.end}")
        return result
    if step.missing_reason or not step.commands:
        result.status = "missing"
        result.detail = step.missing_reason or "nothing to run"
        console.line(f"{console.dim}[note] {step.name}: {result.detail}{console.end}")
        return result

    console.line(f"[run ] {step.name} ...")
    env = dict(os.environ)
    env.setdefault("CI", "1")              # keeps vitest/jest/npm test out of watch mode
    env.setdefault("FORCE_COLOR", "0")
    env.setdefault("NO_COLOR", "1")
    env.setdefault("PYTHONIOENCODING", "utf-8")
    started = time.perf_counter()
    outs, errs = [], []
    first_failure = ""
    status, exit_code = "passed", 0
    for command in step.commands:
        try:
            proc = subprocess.run(
                command, cwd=step.cwd, capture_output=True, text=True, encoding="utf-8",
                errors="replace", timeout=step.timeout, check=False, env=env,
            )
        except subprocess.TimeoutExpired as exc:
            outs.append(_decode(exc.stdout))
            errs.append(_decode(exc.stderr))
            # A hung test suite is a real failure; a slow advisory audit is not.
            status = "failed" if step.required else "error"
            exit_code = None
            result.detail = f"timed out after {step.timeout}s"
            break
        except OSError as exc:
            status, exit_code = "missing", None
            result.detail = f"could not start {Path(command[0]).name}: {exc.strerror or exc}"
            break
        outs.append(proc.stdout)
        errs.append(proc.stderr)
        if proc.returncode != 0:
            if exit_code == 0 and len(step.commands) > 1:
                first_failure = _detail_from(proc.stdout) or _detail_from(proc.stderr)
            exit_code = proc.returncode
            if step.kit_script and proc.returncode not in (0, 1):
                status = "error"
                result.detail = f"script exited {proc.returncode}"
            elif status == "passed":
                status = "failed"
    result.duration_seconds = round(time.perf_counter() - started, 2)
    result.status, result.exit_code = status, exit_code
    result.stdout, result.stderr = _tail("\n".join(outs)), _tail("\n".join(errs))
    if not result.detail and first_failure:
        result.detail = first_failure
    if not result.detail and step.detail_regex:
        found = re.findall(step.detail_regex, "\n".join(outs))
        result.detail = ", ".join(" ".join(f.split()) for f in found if isinstance(f, str))[:90]
    if not result.detail:
        result.detail = _detail_from(result.stdout) or _detail_from(result.stderr)
        if status == "failed" and not result.detail:
            result.detail = f"exit {exit_code}"

    mark = {"passed": "pass", "failed": "FAIL" if step.required else "warn",
            "error": "err ", "missing": "note"}[status]
    colour = {"pass": console.green, "FAIL": console.red, "warn": console.yellow}.get(mark, console.dim)
    console.line(f"{colour}[{mark}] {step.name} ({result.duration_seconds:.1f}s){console.end}")
    if status == "failed" and step.required:
        tail = "\n".join(p for p in (result.stdout, result.stderr) if p)
        if tail:
            console.line("\n".join("       " + ln for ln in tail[-1600:].splitlines()))
    return result


def execute(steps: Iterable[Step], console: Console | None = None, stop_on_fail: bool = False) -> list[CheckResult]:
    results: list[CheckResult] = []
    for step in steps:
        result = run_step(step, console)
        results.append(result)
        if stop_on_fail and result.blocking:
            break
    return results


def suite_success(results: Iterable[CheckResult], strict: bool = False) -> bool:
    """Required failures block. With strict, advisory findings and errors block too."""
    for r in results:
        if r.blocking:
            return False
        if strict and r.status in {"failed", "error"}:
            return False
    return True


def advisory_findings(results: Iterable[CheckResult]) -> list[CheckResult]:
    return [r for r in results if not r.required and r.status in {"failed", "error"}]


def not_run(results: Iterable[CheckResult]) -> list[CheckResult]:
    """Required checks that could not run (tool missing, check broke) - a 'Not verified' line.

    Skips are deliberate (nothing of that kind changed, not applicable) and are not listed.
    """
    return [r for r in results if r.required and r.status in {"missing", "error"}]


def summary_table(results: list[CheckResult]) -> str:
    label = {"passed": "PASS", "skipped": "skip", "missing": "note", "error": "ERROR"}
    rows = [("Check", "Kind", "Result", "Time", "Detail")]
    for r in results:
        res = ("FAIL" if r.required else "WARN") if r.status == "failed" else label[r.status]
        time_s = f"{r.duration_seconds:.1f}s" if r.status not in {"skipped", "missing"} else ""
        rows.append((r.name, r.kind, res, time_s, r.detail[:70]))
    widths = [max(len(row[i]) for row in rows) for i in range(4)]
    lines = []
    for i, row in enumerate(rows):
        lines.append("  ".join(cell.ljust(widths[j]) for j, cell in enumerate(row[:4])) + "  " + row[4])
        if i == 0:
            lines.append("  ".join("-" * w for w in widths) + "  " + "-" * 6)
    return "\n".join(line.rstrip() for line in lines)


def verdict_line(results: list[CheckResult], strict: bool = False) -> str:
    blocking = [r.name for r in results if r.blocking]
    advisory = advisory_findings(results)
    missed = not_run(results)
    parts = []
    if blocking:
        parts.append(f"FAIL - required: {', '.join(blocking)}")
    elif strict and advisory:
        parts.append(f"FAIL (--strict) - advisory: {', '.join(r.name for r in advisory)}")
    else:
        parts.append("PASS - no required check failed")
    if advisory:
        parts.append(f"{len(advisory)} advisory finding(s)" + ("" if strict else ", not blocking"))
    if missed:
        parts.append(f"not verified: {', '.join(r.name for r in missed)}")
    return "Result: " + "; ".join(parts)


def report_payload(title: str, project: Path, mode: str, results: list[CheckResult],
                   started: datetime, strict: bool = False, extra: dict | None = None) -> dict:
    payload = {
        "tool": title,
        "project": str(project),
        "kit": str(KIT_ROOT),
        "mode": mode,
        "strict": strict,
        "started_at": started.isoformat(),
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "success": suite_success(results, strict),
        "required_failures": [r.name for r in results if r.blocking],
        "advisory_findings": [r.name for r in advisory_findings(results)],
        "not_verified": [r.name for r in not_run(results)],
        "results": [asdict(r) for r in results],
    }
    if extra:
        payload.update(extra)
    return payload


def write_report(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
