#!/usr/bin/env python3
"""Test runner: detects every test suite in the project and runs the ones that can run.

  Node      npm test when package.json has a real test script (the npm-init
            placeholder "no test specified" is ignored), else local vitest/jest
  PHP       php artisan test (Laravel), vendor/bin/pest, vendor/bin/phpunit
  Python    pytest when installed, else python -m unittest discover
            (only when test files exist: tests/, test_*.py, *_test.py)

Suites run with CI=true so watch modes exit. A suite whose tool or dependencies
are missing is reported as NOT RUN with the fix, not as a pass or a failure.

Usage:
    python test_runner.py <project> [--coverage] [--json] [--timeout SECONDS]

Exit codes: 0 every suite that ran passed (or none could run), 1 a suite failed
or timed out, 2 usage error.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Shared runner helpers (same block in every AG Kit tool-runner script; stdlib only)
# ---------------------------------------------------------------------------
SKIP_DIRS = frozenset({
    "node_modules", "vendor", "dist", "build", ".next", ".nuxt", ".svelte-kit",
    ".output", "out", ".git", ".hg", ".svn", "__pycache__", ".venv", "venv",
    ".tox", ".mypy_cache", ".pytest_cache", ".ruff_cache", "coverage", ".turbo",
    ".cache", ".vercel", ".expo", ".agents", ".agent", ".idea", ".vscode",
})
IS_WINDOWS = os.name == "nt"


def utf8_console() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def read_text(path: Path) -> str:
    """Read a text file as UTF-8 (BOM and UTF-16 aware). Never raises."""
    try:
        data = path.read_bytes()
    except OSError:
        return ""
    if data[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return data.decode("utf-16", errors="replace")
    return data.decode("utf-8-sig", errors="replace")


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(read_text(path))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def find_executable(name: str, project: Path | None = None, local_only: bool = False) -> str | None:
    """Project-local binary first (node_modules/.bin, vendor/bin), then PATH. Never downloads."""
    if project is not None:
        for folder in (project / "node_modules" / ".bin", project / "vendor" / "bin"):
            for candidate in ((f"{name}.cmd", f"{name}.bat", f"{name}.exe", name) if IS_WINDOWS else (name,)):
                path = folder / candidate
                if path.is_file():
                    return str(path)
    return None if local_only else shutil.which(name)


def run_command(cmd: list[str], cwd: Path, timeout: int, env: dict[str, str] | None = None) -> dict[str, Any]:
    """Run a command without a shell. Returns status passed|failed|timeout|error plus output."""
    started = time.monotonic()
    merged_env = {**os.environ, **(env or {})}
    try:
        proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=timeout, env=merged_env, stdin=subprocess.DEVNULL,
                              check=False)
    except FileNotFoundError:
        return {"status": "error", "returncode": None, "output": f"command not found: {cmd[0]}",
                "seconds": 0.0}
    except subprocess.TimeoutExpired as exc:
        partial = exc.stdout if isinstance(exc.stdout, str) else (exc.stdout or b"").decode("utf-8", "replace")
        return {"status": "timeout", "returncode": None, "output": (partial or "")[-4000:] + f"\n[timed out after {timeout}s]",
                "seconds": round(time.monotonic() - started, 1)}
    except OSError as exc:
        return {"status": "error", "returncode": None, "output": str(exc), "seconds": 0.0}
    output = "\n".join(part.strip() for part in (proc.stdout, proc.stderr) if part and part.strip())
    return {"status": "passed" if proc.returncode == 0 else "failed", "returncode": proc.returncode,
            "output": output[-12000:], "seconds": round(time.monotonic() - started, 1)}


def tail(text: str, lines: int) -> str:
    parts = text.rstrip().splitlines()
    shown = parts[-lines:]
    prefix = [f"... ({len(parts) - lines} earlier lines)"] if len(parts) > lines else []
    return "\n".join(prefix + shown)


def resolve_project(parser: argparse.ArgumentParser, value: str) -> Path:
    path = Path(value).expanduser().resolve()
    if not path.is_dir():
        parser.error(f"project directory not found: {path}")
    return path

# ---------------------------------------------------------------------------
# Suite detection
# ---------------------------------------------------------------------------
NPM_PLACEHOLDER = re.compile(r"no test specified", re.I)


def has_python_tests(project: Path) -> bool:
    for dirpath, dirnames, filenames in os.walk(project):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        if any(re.match(r"(test_.*|.*_test)\.py$", name) for name in filenames):
            return True
    return False


def plan_suites(project: Path, coverage: bool) -> tuple[list[dict[str, Any]], list[str]]:
    suites: list[dict[str, Any]] = []
    not_run: list[str] = []

    package = project / "package.json"
    if package.is_file():
        pkg = read_json(package)
        scripts = pkg.get("scripts") or {}
        deps = {**(pkg.get("dependencies") or {}), **(pkg.get("devDependencies") or {})}
        test_script = scripts.get("test", "")
        real_script = bool(test_script) and not NPM_PLACEHOLDER.search(test_script)
        has_modules = (project / "node_modules").is_dir()
        vitest = find_executable("vitest", project, local_only=True)
        jest = find_executable("jest", project, local_only=True)
        npm = find_executable("npm")
        if real_script or "vitest" in deps or "jest" in deps:
            if not has_modules:
                not_run.append("node: node_modules missing; run npm install (tests NOT RUN)")
            elif coverage and vitest:
                suites.append({"name": "vitest --coverage", "cmd": [vitest, "run", "--coverage"]})
            elif coverage and jest:
                suites.append({"name": "jest --coverage", "cmd": [jest, "--coverage"]})
            elif real_script and npm:
                suites.append({"name": "npm test", "cmd": [npm, "test", "--silent"]})
            elif vitest:
                suites.append({"name": "vitest run", "cmd": [vitest, "run"]})
            elif jest:
                suites.append({"name": "jest", "cmd": [jest]})
            else:
                not_run.append("node: test tool not found (npm/vitest/jest); tests NOT RUN")

    if (project / "composer.json").is_file():
        php = shutil.which("php")
        vendor = (project / "vendor").is_dir()
        pest = find_executable("pest", project, local_only=True)
        phpunit = find_executable("phpunit", project, local_only=True)
        if not php:
            not_run.append("php: php not found on PATH; tests NOT RUN")
        elif not vendor:
            if (project / "tests").is_dir():
                not_run.append("php: vendor/ missing; run composer install (tests NOT RUN)")
        elif (project / "artisan").is_file():
            suites.append({"name": "php artisan test", "cmd": [php, "artisan", "test", *(["--coverage"] if coverage else [])]})
        elif pest:
            suites.append({"name": "pest", "cmd": ([pest] if IS_WINDOWS else [php, pest]) + (["--coverage"] if coverage else [])})
        elif phpunit:
            suites.append({"name": "phpunit", "cmd": ([phpunit] if IS_WINDOWS else [php, phpunit]) + (["--coverage-text"] if coverage else [])})

    python_project = any((project / n).is_file() for n in ("pyproject.toml", "requirements.txt", "setup.py", "setup.cfg", "pytest.ini", "tox.ini"))
    if python_project and has_python_tests(project):
        if importlib.util.find_spec("pytest") is not None:
            cmd = [sys.executable, "-m", "pytest", "-q"]
            if coverage and importlib.util.find_spec("pytest_cov") is not None:
                cmd += ["--cov", "--cov-report=term-missing"]
            suites.append({"name": "pytest", "cmd": cmd})
        elif shutil.which("pytest"):
            suites.append({"name": "pytest", "cmd": [shutil.which("pytest"), "-q"]})
        else:
            start = "tests" if (project / "tests").is_dir() else "."
            suites.append({"name": "unittest", "cmd": [sys.executable, "-m", "unittest", "discover", "-s", start, "-t", "."]})
    return suites, not_run


def parse_counts(output: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for key, pattern in (("passed", r"(\d+)\s+passed"), ("failed", r"(\d+)\s+failed"), ("skipped", r"(\d+)\s+skipped")):
        values = [int(v) for v in re.findall(pattern, output, re.I)]
        if values:
            counts[key] = max(values)
    ran = re.search(r"Ran (\d+) tests?", output)  # unittest
    if ran:
        failures = sum(int(v) for v in re.findall(r"(?:failures|errors)=(\d+)", output))
        counts = {"passed": int(ran.group(1)) - failures, "failed": failures}
    return counts


def main() -> int:
    utf8_console()
    parser = argparse.ArgumentParser(description="Detect and run the project's test suites.")
    parser.add_argument("project", nargs="?", default=".", help="project directory (default: .)")
    parser.add_argument("--coverage", action="store_true", help="run with coverage when the tool supports it")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    parser.add_argument("--timeout", type=int, default=600, help="seconds per suite (default: 600)")
    args = parser.parse_args()
    project = resolve_project(parser, args.project)

    suites, not_run = plan_suites(project, args.coverage)
    results = []
    for suite in suites:
        result = run_command(suite["cmd"], project, args.timeout, env={"CI": "true", "FORCE_COLOR": "0", "NO_COLOR": "1"})
        results.append({"name": suite["name"], "counts": parse_counts(result["output"]), **result})
    failed = [r for r in results if r["status"] != "passed"]

    if args.json:
        print(json.dumps({"script": "test_runner", "project": str(project), "passed": not failed,
                          "suites": results, "not_run": not_run}, indent=2, ensure_ascii=False))
        return 1 if failed else 0

    print(f"Tests: {project}")
    for note in not_run:
        print(f"  NOT RUN  {note}")
    if not results and not not_run:
        print("No test suite found. Logic changes need tests (testing-patterns skill). NOT VERIFIED.")
    for r in results:
        counts = ", ".join(f"{v} {k}" for k, v in r["counts"].items())
        print(f"  {r['status'].upper():<7}  {r['name']} ({r['seconds']}s){' - ' + counts if counts else ''}")
        if r["status"] != "passed" and r["output"]:
            print("    " + tail(r["output"], 30).replace("\n", "\n    "))
    if results:
        print(f"\nResult: {'FAIL' if failed else 'PASS'} ({len(results) - len(failed)}/{len(results)} suite(s) passed)")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
