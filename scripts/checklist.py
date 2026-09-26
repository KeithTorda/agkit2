#!/usr/bin/env python3
"""Risk-aware project checks (code-rules verification tiers).

  --quick (default, tier 1)  Detect the stack and run the project's own fast checks - lint,
                             type check, tests - scoped to git-changed files where the tool
                             supports it. No security scan, no audits.
  --full  (tier 2)           Everything on the whole project: lint, types, tests, the kit's
                             security scan, and the advisory audits (CSS, naming, UX,
                             accessibility, SEO, i18n, schema). Runtime checks with --url.

Required (can fail the run): security findings high or above, type errors, failing tests.
Advisory (reported, never fail unless --strict): lint style, naming, CSS audit, UX/SEO/i18n
heuristics. A tool that is not installed or not configured is a note, not a failure.

Exit codes: 0 no required failure, 1 a required check failed (or an advisory one with
--strict), 2 usage error.

Usage:
  python "KIT/scripts/checklist.py" .
  python "KIT/scripts/checklist.py" . --full --url http://localhost:3000
  python "KIT/scripts/checklist.py" . --quick --since origin/main --json
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validation_runner import (  # noqa: E402
    KIT_ROOT,
    Console,
    Step,
    execute,
    report_payload,
    suite_success,
    summary_table,
    utf8_stdio,
    verdict_line,
    write_report,
)

IS_WINDOWS = os.name == "nt"
JS_EXT = {".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".mts", ".cts", ".vue", ".svelte", ".astro"}
TS_EXT = {".ts", ".tsx", ".mts", ".cts", ".vue", ".svelte"}
PY_EXT = {".py", ".pyi"}
PHP_EXT = {".php"}
NPM_PLACEHOLDER_TEST = "no test specified"
TYPECHECK_SCRIPTS = ("typecheck", "type-check", "check-types", "types", "tsc")


# ------------------------------------------------------------------ git scope
def git_changed_files(project: Path, since: str | None = None) -> list[str] | None:
    """Changed files relative to `project` (uncommitted + untracked, plus `since`...HEAD).

    None when git is missing or the project is not inside a work tree: the caller then checks
    the whole project instead of pretending nothing changed.
    """
    git = shutil.which("git")
    if not git:
        return None

    def run(*args: str) -> subprocess.CompletedProcess | None:
        try:
            return subprocess.run([git, *args], cwd=project, capture_output=True, text=True,
                                  encoding="utf-8", errors="replace", timeout=30, check=False)
        except (OSError, subprocess.TimeoutExpired):
            return None

    top = run("rev-parse", "--show-toplevel")
    if top is None or top.returncode != 0 or not top.stdout.strip():
        return None
    top_dir = Path(top.stdout.strip()).resolve()
    paths: set[str] = set()

    status = run("status", "--porcelain=v1", "-z", "--untracked-files=all")
    if status is None or status.returncode != 0:
        return None
    tokens = status.stdout.split("\0")
    i = 0
    while i < len(tokens):
        entry = tokens[i]
        i += 1
        if len(entry) < 4:
            continue
        code, rel = entry[:2], entry[3:]
        if "R" in code or "C" in code:
            i += 1                                   # the next token is the old path
        if "D" in code:
            continue
        paths.add(rel)

    if since:
        diff = run("diff", "--name-only", "-z", "--diff-filter=ACMR", f"{since}...HEAD")
        if diff is None or diff.returncode != 0:
            diff = run("diff", "--name-only", "-z", "--diff-filter=ACMR", since)
        if diff is not None and diff.returncode == 0:
            paths.update(p for p in diff.stdout.split("\0") if p)

    project_res = project.resolve()
    out = []
    for rel in sorted(paths):
        full = (top_dir / rel).resolve()
        if not full.is_file():
            continue
        try:
            out.append(full.relative_to(project_res).as_posix())
        except ValueError:
            continue                                 # changed, but outside this project
    return out


# ------------------------------------------------------------------ stack detection
@dataclass
class Stack:
    names: list[str] = field(default_factory=list)
    node: dict | None = None
    python: bool = False
    php: bool = False


def _read_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text("utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def detect_stack(project: Path) -> Stack:
    stack = Stack()
    pkg_path = project / "package.json"
    if pkg_path.is_file():
        pkg = _read_json(pkg_path)
        deps = {**(pkg.get("dependencies") or {}), **(pkg.get("devDependencies") or {})}
        stack.node = {"pkg": pkg, "deps": deps, "scripts": pkg.get("scripts") or {}}
        label = next((n for key, n in (("next", "Next.js"), ("nuxt", "Nuxt"), ("@sveltejs/kit", "SvelteKit"),
                                         ("astro", "Astro"), ("vue", "Vue"), ("react", "React"),
                                         ("hono", "Hono"), ("express", "Express")) if key in deps), "Node")
        stack.names.append(label)
        if "typescript" in deps or (project / "tsconfig.json").is_file():
            stack.names.append("TypeScript")
    if any((project / m).is_file() for m in ("pyproject.toml", "setup.py", "setup.cfg", "requirements.txt",
                                             "manage.py", "Pipfile")):
        stack.python = True
        stack.names.append("Django" if (project / "manage.py").is_file() else "Python")
    if (project / "composer.json").is_file():
        stack.php = True
        stack.names.append("Laravel" if (project / "artisan").is_file() else "PHP")
    if not stack.names and any(project.glob("*.html")):
        stack.names.append("Static HTML")
    return stack


def package_manager(project: Path) -> str:
    for lock, pm in (("pnpm-lock.yaml", "pnpm"), ("yarn.lock", "yarn"), ("bun.lockb", "bun"),
                     ("bun.lock", "bun"), ("package-lock.json", "npm")):
        if (project / lock).is_file():
            return pm
    return "npm"


def which(name: str) -> str | None:
    return shutil.which(name)


def node_bin(project: Path, name: str) -> str | None:
    base = project / "node_modules" / ".bin"
    for candidate in ((base / f"{name}.cmd", base / name) if IS_WINDOWS else (base / name,)):
        if candidate.is_file():
            return str(candidate)
    return None


def venv_tool(project: Path, name: str) -> str | None:
    for venv in (".venv", "venv", "env"):
        folder = project / venv / ("Scripts" if IS_WINDOWS else "bin")
        names = (f"{name}.exe", f"{name}.cmd", f"{name}.bat", name) if IS_WINDOWS else (name,)
        for candidate in (folder / n for n in names):
            if candidate.is_file():
                return str(candidate)
    return which(name)


def php_bin(project: Path, name: str) -> str | None:
    base = project / "vendor" / "bin"
    for candidate in ((base / f"{name}.bat", base / name) if IS_WINDOWS else (base / name,)):
        if candidate.is_file():
            return str(candidate)
    return None


def _run_script(pm: str, script: str) -> list[str] | None:
    exe = which(pm)
    return [exe, "run", script] if exe else None


def _pyproject_has(project: Path, section: str) -> bool:
    try:
        return f"[{section}" in (project / "pyproject.toml").read_text("utf-8", errors="replace")
    except OSError:
        return False


def _has_python_tests(project: Path) -> bool:
    if any((project / d).is_dir() for d in ("tests", "test")):
        return True
    if (project / "pytest.ini").is_file() or _pyproject_has(project, "tool.pytest"):
        return True
    return any(project.glob("test_*.py")) or any(project.glob("*_test.py"))


# ------------------------------------------------------------------ step builders
def _filter(scope: list[str] | None, exts: set[str]) -> list[str] | None:
    """None = whole project; a list = only these changed files."""
    if scope is None:
        return None
    return [f for f in scope if Path(f).suffix.lower() in exts
            and not any(part in {"node_modules", "vendor", "dist", "build", ".next"} for part in Path(f).parts)]


def node_steps(project: Path, stack: Stack, scope: list[str] | None, full: bool) -> list[Step]:
    info = stack.node or {}
    scripts, deps = info.get("scripts", {}), info.get("deps", {})
    pm = package_manager(project)
    js_files = _filter(scope, JS_EXT)
    ts_files = _filter(scope, TS_EXT)
    steps: list[Step] = []
    no_js = "no changed JS/TS files"

    # --- lint (advisory)
    lint = Step("Lint (JS/TS)", "lint", cwd=project)
    eslint, biome = node_bin(project, "eslint"), node_bin(project, "biome")
    has_eslint_cfg = any(project.glob("eslint.config.*")) or any(project.glob(".eslintrc*"))
    if js_files == []:
        lint.skip_reason = no_js
    elif eslint and has_eslint_cfg:
        lint.name = "Lint (eslint)" + (f" {len(js_files)} file(s)" if js_files else "")
        lint.commands = [[eslint, *(js_files or ["."])]]
    elif biome and any(project.glob("biome.json*")):
        lint.name = "Lint (biome)"
        lint.commands = [[biome, "check", "--no-errors-on-unmatched", *(js_files or ["."])]]
    elif "lint" in scripts and _run_script(pm, "lint"):
        lint.name = f"Lint ({pm} run lint)"
        lint.commands = [_run_script(pm, "lint")]  # type: ignore[list-item]
    else:
        lint.missing_reason = "no JS linter configured (eslint/biome or a lint script)"
    steps.append(lint)

    # --- types (required)
    types = Step("Type check (TS)", "types", required=True, cwd=project, timeout=600)
    script = next((s for s in TYPECHECK_SCRIPTS if s in scripts), None)
    has_tsconfig = (project / "tsconfig.json").is_file()
    if not has_tsconfig and not script:
        types.skip_reason = "no tsconfig.json"
    elif ts_files == [] and js_files == []:
        types.skip_reason = no_js
    elif script and _run_script(pm, script):
        types.name = f"Type check ({pm} run {script})"
        types.commands = [_run_script(pm, script)]  # type: ignore[list-item]
    elif "vue" in deps and node_bin(project, "vue-tsc"):
        types.name = "Type check (vue-tsc)"
        types.commands = [[node_bin(project, "vue-tsc"), "--noEmit"]]  # type: ignore[list-item]
    elif "svelte" in deps and node_bin(project, "svelte-check"):
        types.name = "Type check (svelte-check)"
        types.commands = [[node_bin(project, "svelte-check")]]  # type: ignore[list-item]
    elif node_bin(project, "tsc"):
        types.name = "Type check (tsc --noEmit)"
        types.commands = [[node_bin(project, "tsc"), "--noEmit", "-p", "tsconfig.json"]]  # type: ignore[list-item]
    else:
        types.missing_reason = "typescript is not installed (run the package install)"
    steps.append(types)

    # --- tests (required)
    tests = Step("Tests (JS)", "tests", required=True, cwd=project, timeout=900)
    vitest, jest = node_bin(project, "vitest"), node_bin(project, "jest")
    test_script = str(scripts.get("test", ""))
    src_files = [f for f in (js_files or []) if f]
    if js_files == []:
        tests.skip_reason = no_js
    elif vitest and "vitest" in deps:
        if src_files and not full:
            tests.name = f"Tests (vitest related, {len(src_files)} file(s))"
            tests.commands = [[vitest, "related", "--run", "--passWithNoTests", *src_files]]
        else:
            tests.name = "Tests (vitest run)"
            tests.commands = [[vitest, "run", "--passWithNoTests"]]
    elif jest and "jest" in deps:
        if src_files and not full:
            tests.name = f"Tests (jest related, {len(src_files)} file(s))"
            tests.commands = [[jest, "--findRelatedTests", "--passWithNoTests", *src_files]]
        else:
            tests.name = "Tests (jest)"
            tests.commands = [[jest, "--passWithNoTests"]]
    elif test_script and NPM_PLACEHOLDER_TEST not in test_script and which(pm):
        tests.name = f"Tests ({pm} test)"
        tests.commands = [[which(pm), "test"]]  # type: ignore[list-item]
    else:
        tests.missing_reason = "no JS test runner (vitest/jest or a test script)"
    steps.append(tests)
    return steps


def python_steps(project: Path, scope: list[str] | None, full: bool) -> list[Step]:
    py_files = _filter(scope, PY_EXT)
    steps: list[Step] = []
    no_py = "no changed Python files"

    lint = Step("Lint (Python)", "lint", cwd=project)
    ruff = venv_tool(project, "ruff")
    if py_files == []:
        lint.skip_reason = no_py
    elif ruff:
        lint.name = "Lint (ruff)"
        lint.commands = [[ruff, "check", *(py_files or ["."])]]
    else:
        lint.missing_reason = "ruff not installed (pip install ruff)"
    steps.append(lint)

    types = Step("Type check (Python)", "types", required=True, cwd=project, timeout=600)
    mypy_cfg = (project / "mypy.ini").is_file() or (project / ".mypy.ini").is_file() or _pyproject_has(project, "tool.mypy")
    pyright_cfg = (project / "pyrightconfig.json").is_file() or _pyproject_has(project, "tool.pyright")
    if py_files == []:
        types.skip_reason = no_py
    elif mypy_cfg and venv_tool(project, "mypy"):
        types.name = "Type check (mypy)"
        types.commands = [[venv_tool(project, "mypy"), *(py_files or ["."])]]  # type: ignore[list-item]
    elif pyright_cfg and venv_tool(project, "pyright"):
        types.name = "Type check (pyright)"
        types.commands = [[venv_tool(project, "pyright"), *(py_files or [])]]  # type: ignore[list-item]
    elif mypy_cfg or pyright_cfg:
        types.missing_reason = "type checker configured but not installed"
    else:
        types.skip_reason = "no mypy/pyright configuration"
    steps.append(types)

    tests = Step("Tests (Python)", "tests", required=True, cwd=project, timeout=900)
    python = venv_tool(project, "python") or sys.executable
    pytest = venv_tool(project, "pytest")
    if py_files == []:
        tests.skip_reason = no_py
    elif not _has_python_tests(project) and not (project / "manage.py").is_file():
        tests.missing_reason = "no Python tests found"
    elif pytest:
        tests.name = "Tests (pytest)"
        tests.commands = [[pytest, "-q"] + ([] if full else ["-x"])]
    elif (project / "manage.py").is_file():
        tests.name = "Tests (manage.py test)"
        tests.commands = [[python, "manage.py", "test"]]
    else:
        start = "tests" if (project / "tests").is_dir() else "."
        tests.name = "Tests (unittest)"
        tests.commands = [[python, "-m", "unittest", "discover", "-s", start, "-t", "."]]
    steps.append(tests)
    return steps


def _project_php_files(project: Path, limit: int = 300) -> list[str]:
    skip = {"vendor", "node_modules", "storage", "bootstrap", ".git", "public"}
    found: list[str] = []
    for path in sorted(project.rglob("*.php")):
        rel = path.relative_to(project)
        if any(part in skip for part in rel.parts[:-1]):
            continue
        found.append(rel.as_posix())
        if len(found) >= limit:
            break
    return found


def php_steps(project: Path, scope: list[str] | None, full: bool) -> list[Step]:
    php_files = _filter(scope, PHP_EXT)
    steps: list[Step] = []
    no_php = "no changed PHP files"
    php = which("php")

    lint = Step("Lint (pint)", "lint", cwd=project)
    pint = php_bin(project, "pint")
    if php_files == []:
        lint.skip_reason = no_php
    elif pint:
        lint.commands = [[pint, "--test", *(php_files or [])]]
    else:
        lint.missing_reason = "pint not installed"
    steps.append(lint)

    types = Step("Static analysis (PHP)", "types", required=True, cwd=project, timeout=600)
    phpstan = php_bin(project, "phpstan")
    has_cfg = any((project / n).is_file() for n in ("phpstan.neon", "phpstan.neon.dist", "phpstan.dist.neon"))
    if php_files == []:
        types.skip_reason = no_php
    elif phpstan and has_cfg:
        types.name = "Static analysis (phpstan)"
        types.commands = [[phpstan, "analyse", "--no-progress", "--memory-limit=1G", *(php_files or [])]]
    elif php:
        targets = php_files if php_files is not None else _project_php_files(project)
        types.name = f"Syntax (php -l, {len(targets)} file(s))"
        types.commands = [[php, "-l", f] for f in targets]
        if not targets:
            types.skip_reason = "no PHP files"
    else:
        types.missing_reason = "php is not on PATH"
    steps.append(types)

    tests = Step("Tests (PHP)", "tests", required=True, cwd=project, timeout=900)
    pest, phpunit = php_bin(project, "pest"), php_bin(project, "phpunit")
    if php_files == []:
        tests.skip_reason = no_php
    elif pest:
        tests.name = "Tests (pest)"
        tests.commands = [[pest] + ([] if full else ["--bail"])]
    elif (project / "artisan").is_file() and php and phpunit:
        tests.name = "Tests (artisan test)"
        tests.commands = [[php, "artisan", "test"]]
    elif phpunit:
        tests.name = "Tests (phpunit)"
        tests.commands = [[phpunit]]
    else:
        tests.missing_reason = "no PHP test runner (pest/phpunit)"
    steps.append(tests)
    return steps


def kit_step(name: str, rel_script: str, category: str, project: Path, *args: str,
             required: bool = False, timeout: int = 300) -> Step:
    script = KIT_ROOT / rel_script
    step = Step(name, category, required=required, cwd=project, timeout=timeout, kit_script=True)
    if script.is_file():
        step.commands = [[sys.executable, str(script), str(project), *args]]
    else:
        step.missing_reason = f"kit script not found: {rel_script}"
    return step


def security_step(project: Path) -> Step:
    step = kit_step("Security scan (high+)", "skills/vulnerability-scanner/scripts/security_scan.py",
                    "security", project, "--output", "summary", "--fail-on", "high",
                    required=True, timeout=600)
    step.detail_regex = r"(?m)^\s*((?:Critical|High):\s*\d+)"
    return step


def audit_steps(project: Path) -> list[Step]:
    return [
        kit_step("CSS audit", "scripts/css_audit.py", "audit", project, "--strict"),
        kit_step("Naming check", "scripts/naming_check.py", "audit", project, "--strict"),
        kit_step("UX audit", "skills/frontend-design/scripts/ux_audit.py", "audit", project),
        kit_step("Accessibility check", "skills/frontend-design/scripts/accessibility_checker.py", "audit", project),
        kit_step("SEO check", "skills/seo-fundamentals/scripts/seo_checker.py", "audit", project),
        kit_step("i18n check", "skills/i18n-localization/scripts/i18n_checker.py", "audit", project),
        kit_step("Schema check", "skills/database-design/scripts/schema_validator.py", "audit", project),
    ]


def runtime_steps(url: str | None) -> list[Step]:
    steps = []
    for name, rel, timeout in (("Lighthouse", "skills/performance-profiling/scripts/lighthouse_audit.py", 240),
                               ("Playwright smoke", "skills/testing-patterns/scripts/playwright_runner.py", 180)):
        step = Step(name, "runtime", timeout=timeout, kit_script=True)
        if not url:
            step.skip_reason = "no --url"
        elif not (KIT_ROOT / rel).is_file():
            step.missing_reason = f"kit script not found: {rel}"
        else:
            step.commands = [[sys.executable, str(KIT_ROOT / rel), url]]
        steps.append(step)
    return steps


def build_steps(project: Path, mode: str, scope: list[str] | None, url: str | None = None) -> list[Step]:
    """The ordered step list. mode: 'quick' or 'full'. scope: changed files or None (all)."""
    full = mode == "full"
    stack = detect_stack(project)
    steps: list[Step] = []
    if full:
        steps.append(security_step(project))
    if stack.node is not None:
        steps += node_steps(project, stack, scope, full)
    if stack.python:
        steps += python_steps(project, scope, full)
    if stack.php:
        steps += php_steps(project, scope, full)
    if stack.node is None and not stack.python and not stack.php:
        steps.append(Step("Lint / types / tests", "tests", required=True,
                          missing_reason="no package.json, pyproject/requirements or composer.json: "
                                         "no project checks to run"))
    if full:
        steps += audit_steps(project)
        steps += runtime_steps(url)
    elif url:
        steps += runtime_steps(url)
    return steps


# ------------------------------------------------------------------ CLI
def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Risk-aware project checks: --quick (tier 1, default) or --full (tier 2).",
        epilog="Exit codes: 0 no required failure, 1 required failure (or advisory with --strict), 2 usage.")
    parser.add_argument("project", nargs="?", default=".", help="project directory (default: .)")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--quick", dest="mode", action="store_const", const="quick",
                      help="lint, types, tests on git-changed files (default)")
    mode.add_argument("--full", dest="mode", action="store_const", const="full",
                      help="whole project + security scan + advisory audits")
    parser.add_argument("--all-files", action="store_true", help="--quick without git scoping")
    parser.add_argument("--since", metavar="REF", help="also include files changed since REF (e.g. origin/main)")
    parser.add_argument("--url", help="running app URL for Lighthouse and Playwright smoke checks")
    parser.add_argument("--strict", action="store_true", help="advisory findings fail the run too")
    parser.add_argument("--stop-on-fail", action="store_true", help="stop after the first required failure")
    parser.add_argument("--timeout", type=int, help="override the per-step timeout in seconds")
    parser.add_argument("--json", action="store_true", help="print a JSON report to stdout")
    parser.add_argument("--report", type=Path, help="also write the JSON report to this file")
    parser.set_defaults(mode="quick")
    return parser.parse_args(argv)


def resolve_scope(project: Path, mode: str, all_files: bool, since: str | None) -> tuple[list[str] | None, str]:
    if mode == "full" or all_files:
        return None, "whole project"
    changed = git_changed_files(project, since)
    if changed is None:
        return None, "whole project (no git repository)"
    return changed, f"{len(changed)} changed file(s)" + (f" since {since}" if since else "")


def main(argv: list[str] | None = None) -> int:
    utf8_stdio()
    args = parse_args(argv)
    project = Path(args.project).resolve()
    if not project.is_dir():
        print(f"checklist: not a directory: {project}", file=sys.stderr)
        return 2

    console = Console(sys.stderr if args.json else sys.stdout)
    started = datetime.now(timezone.utc)
    scope, scope_label = resolve_scope(project, args.mode, args.all_files, args.since)
    stack = detect_stack(project)
    console.line(f"checklist --{args.mode} | {project}")
    console.line(f"stack: {', '.join(stack.names) or 'unknown'} | scope: {scope_label}")
    if scope is not None and not scope:
        console.line("No changed files. Nothing to check (use --all-files or --full).")

    steps = build_steps(project, args.mode, scope, args.url)
    if args.timeout:
        for step in steps:
            step.timeout = args.timeout
    results = execute(steps, console, args.stop_on_fail)
    ok = suite_success(results, args.strict)
    payload = report_payload("checklist", project, args.mode, results, started, args.strict,
                             {"stack": stack.names, "scope": scope_label, "changed_files": scope})

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        console.line()
        console.line(summary_table(results))
        console.line()
        console.line(verdict_line(results, args.strict))
    if args.report:
        write_report(args.report.resolve(), payload)
        if not args.json:
            console.line(f"Report: {args.report.resolve()}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
