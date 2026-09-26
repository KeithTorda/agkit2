#!/usr/bin/env python3
"""Lint runner: detects the project's own linters and runs the ones that are installed.

  Node      npm run lint (when a "lint" script exists), else local eslint or biome;
            local tsc --noEmit when TypeScript is present (skip with --no-types)
  PHP       vendor/bin/pint --test and vendor/bin/phpstan when installed,
            otherwise `php -l` syntax check on PHP files when php is on PATH
  Python    ruff check (if installed); mypy when configured, else pyright if installed

Binaries are taken from node_modules/.bin or vendor/bin first, then PATH. Nothing
is downloaded (no bare npx). A missing tool or missing node_modules/vendor is a
SKIP with a note, never a failure.

Usage:
    python lint_runner.py <project> [--json] [--no-types] [--timeout SECONDS]

Exit codes: 0 every linter that ran passed (or none ran), 1 a linter reported
errors or timed out, 2 usage error.
"""
from __future__ import annotations

import argparse
import json
import os
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
# Linter detection
# ---------------------------------------------------------------------------
def plan_checks(project: Path, include_types: bool) -> tuple[list[dict[str, Any]], list[str]]:
    checks: list[dict[str, Any]] = []
    notes: list[str] = []

    package = project / "package.json"
    if package.is_file():
        pkg = read_json(package)
        scripts = pkg.get("scripts") or {}
        deps = {**(pkg.get("dependencies") or {}), **(pkg.get("devDependencies") or {})}
        has_modules = (project / "node_modules").is_dir()
        npm = find_executable("npm")
        if "lint" in scripts:
            if not has_modules:
                notes.append("package.json has a lint script but node_modules is missing; run npm install")
            elif npm:
                checks.append({"name": "npm run lint", "cmd": [npm, "run", "lint", "--silent"]})
            else:
                notes.append("npm not found on PATH; lint script skipped")
        else:
            eslint_config = any(project.glob("eslint.config.*")) or any(project.glob(".eslintrc*")) or "eslintConfig" in pkg
            biome_config = (project / "biome.json").is_file() or (project / "biome.jsonc").is_file()
            eslint = find_executable("eslint", project, local_only=True)
            biome = find_executable("biome", project, local_only=True)
            if eslint and eslint_config:
                checks.append({"name": "eslint", "cmd": [eslint, "."]})
            elif biome and biome_config:
                checks.append({"name": "biome check", "cmd": [biome, "check", "."]})
            elif (eslint_config or biome_config) and not (eslint or biome):
                notes.append("linter config found but the linter is not installed locally; run npm install")
        if include_types and ("typescript" in deps or (project / "tsconfig.json").is_file()):
            tsc = find_executable("tsc", project, local_only=True)
            if tsc and (project / "tsconfig.json").is_file():
                checks.append({"name": "tsc --noEmit", "cmd": [tsc, "--noEmit", "--pretty", "false"]})
            else:
                notes.append("TypeScript present but no local tsc (node_modules/.bin/tsc); type check skipped")

    if (project / "composer.json").is_file() or any(project.glob("*.php")):
        php = shutil.which("php")
        pint = find_executable("pint", project) if (project / "vendor").is_dir() else None
        phpstan = find_executable("phpstan", project) if (project / "vendor").is_dir() else None
        if not php:
            notes.append("php not found on PATH; PHP checks skipped")
        else:
            if pint:
                checks.append({"name": "pint --test", "cmd": [php, pint, "--test"] if not IS_WINDOWS else [pint, "--test"]})
            if phpstan:
                cmd = [phpstan, "analyse", "--no-progress", "--memory-limit=1G"]
                checks.append({"name": "phpstan", "cmd": [php, *cmd] if not IS_WINDOWS else cmd})
            if not pint and not phpstan:
                files = [str(p) for p in iter_php_files(project)]
                if files:
                    checks.append({"name": f"php -l ({len(files)} files)", "php_lint": files, "php": php})
                composer = read_text(project / "composer.json")
                if composer and not (project / "vendor").is_dir():
                    notes.append("vendor/ missing (run composer install); ran php -l syntax check only")
                elif composer:
                    notes.append("no Pint/PHPStan in vendor/bin; ran php -l syntax check only "
                                 "(composer require --dev laravel/pint larastan/larastan)")

    if any((project / name).is_file() for name in ("pyproject.toml", "requirements.txt", "setup.py", "setup.cfg")):
        ruff = find_executable("ruff")
        if ruff:
            checks.append({"name": "ruff check", "cmd": [ruff, "check", "."]})
        else:
            notes.append("ruff not installed; Python lint skipped (pip install ruff)")
        pyproject = read_text(project / "pyproject.toml")
        mypy_configured = (project / "mypy.ini").is_file() or "[tool.mypy]" in pyproject or \
            "[mypy]" in read_text(project / "setup.cfg")
        mypy, pyright = find_executable("mypy"), find_executable("pyright")
        if include_types and mypy and mypy_configured:
            checks.append({"name": "mypy", "cmd": [mypy, "."]})
        elif include_types and pyright and ((project / "pyrightconfig.json").is_file() or "[tool.pyright]" in pyproject):
            checks.append({"name": "pyright", "cmd": [pyright]})
    return checks, notes


def iter_php_files(project: Path):
    count = 0
    for dirpath, dirnames, filenames in os.walk(project):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and d != "storage"]
        for name in filenames:
            if name.endswith(".php") and not name.endswith(".blade.php"):
                yield Path(dirpath) / name
                count += 1
                if count >= 800:
                    return


def run_php_lint(check: dict[str, Any], project: Path, timeout: int) -> dict[str, Any]:
    started = time.monotonic()
    errors = []
    for file in check["php_lint"]:
        if time.monotonic() - started > timeout:
            return {"status": "timeout", "returncode": None, "output": "\n".join(errors) + f"\n[timed out after {timeout}s]",
                    "seconds": round(time.monotonic() - started, 1)}
        result = run_command([check["php"], "-l", file], project, 30)
        if result["status"] != "passed":
            errors.append(result["output"].strip())
    return {"status": "failed" if errors else "passed", "returncode": 1 if errors else 0,
            "output": "\n".join(errors), "seconds": round(time.monotonic() - started, 1)}


def main() -> int:
    utf8_console()
    parser = argparse.ArgumentParser(description="Run the project's installed linters (never downloads tools).")
    parser.add_argument("project", nargs="?", default=".", help="project directory (default: .)")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    parser.add_argument("--no-types", action="store_true", help="skip tsc/mypy/pyright (type_coverage.py runs tsc too)")
    parser.add_argument("--timeout", type=int, default=300, help="seconds per linter (default: 300)")
    args = parser.parse_args()
    project = resolve_project(parser, args.project)

    checks, notes = plan_checks(project, not args.no_types)
    results = []
    for check in checks:
        result = run_php_lint(check, project, args.timeout) if "php_lint" in check else run_command(check["cmd"], project, args.timeout)
        results.append({"name": check["name"], **result})
    failed = [r for r in results if r["status"] != "passed"]

    if args.json:
        print(json.dumps({"script": "lint_runner", "project": str(project), "passed": not failed,
                          "notes": notes, "checks": results}, indent=2, ensure_ascii=False))
    else:
        print(f"Lint: {project}")
        for note in notes:
            print(f"  note: {note}")
        if not results:
            print("No installed linters found for this project; nothing ran (NOT VERIFIED).")
        for r in results:
            print(f"  {r['status'].upper():<7} {r['name']} ({r['seconds']}s)")
            if r["status"] != "passed" and r["output"]:
                print("    " + tail(r["output"], 15).replace("\n", "\n    "))
        if results:
            print(f"\nResult: {'FAIL' if failed else 'PASS'} ({len(results) - len(failed)}/{len(results)} passed)")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
