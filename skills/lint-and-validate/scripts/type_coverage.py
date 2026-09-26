#!/usr/bin/env python3
"""Type-safety check for TypeScript and Python projects.

TypeScript
  - Runs the project-local tsc --noEmit for every tsconfig.json (solution-style
    configs with "files": [] run their references instead). Compiler errors fail.
    Skipped, not failed, when node_modules/.bin/tsc is missing.
  - Counts explicit escape hatches (`: any`, `as any`, `<any>`, @ts-ignore,
    @ts-nocheck). Above a project-size threshold they fail; below it they are
    warnings. Inferred return types are never counted against you.
Python
  - Parses every file with ast: syntax errors fail.
  - Reports the share of fully annotated functions and Any usage as warnings
    (annotation coverage is guidance, never a failure).

Usage:
    python type_coverage.py <project> [--json] [--skip-compiler] [--timeout SECONDS]

Exit codes: 0 ok, 1 compiler errors / syntax errors / escape hatches above
threshold, 2 usage error.
"""
from __future__ import annotations

import argparse
import ast
import json
import math
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
# Type checks
# ---------------------------------------------------------------------------
TYPE_SKIP_DIRS = SKIP_DIRS | {"env"}


def _source_files(project: Path, suffixes: set[str]) -> list[Path]:
    files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(project):
        dirnames[:] = sorted(d for d in dirnames if d not in TYPE_SKIP_DIRS)
        for name in filenames:
            path = Path(dirpath) / name
            if path.suffix.lower() in suffixes and not name.endswith(".d.ts"):
                files.append(path)
    return sorted(files)


def _local_tsc(tsconfig: Path, project: Path) -> Path | None:
    names = ("tsc.cmd", "tsc.exe", "tsc") if IS_WINDOWS else ("tsc",)
    for parent in (tsconfig.parent, *tsconfig.parents):
        for name in names:
            candidate = parent / "node_modules" / ".bin" / name
            if candidate.is_file():
                return candidate
        if parent == project:
            break
    return None


def _tsconfig_targets(tsconfig: Path) -> list[Path]:
    """Solution-style tsconfig ("files": [] + references) type-checks nothing itself; use its references."""
    text = re.sub(r"(?m)^\s*//.*$", "", read_text(tsconfig))
    if re.search(r"\"files\"\s*:\s*\[\s*\]", text) and "\"references\"" in text:
        refs = []
        for ref in re.findall(r"\"path\"\s*:\s*\"([^\"]+)\"", text):
            target = (tsconfig.parent / ref).resolve()
            refs.append(target / "tsconfig.json" if target.is_dir() else target)
        return [r for r in refs if r.is_file()] or [tsconfig]
    return [tsconfig]


def _run_typescript_compilers(project: Path, timeout: int) -> list[dict[str, Any]]:
    runs: list[dict[str, Any]] = []
    tsconfigs = [p for p in _source_files(project, {".json"}) if p.name == "tsconfig.json"]
    seen: set[Path] = set()
    for tsconfig in tsconfigs:
        for config in _tsconfig_targets(tsconfig):
            if config in seen:
                continue
            seen.add(config)
            label = config.relative_to(project).as_posix() if config.is_relative_to(project) else str(config)
            compiler = _local_tsc(config, project)
            if compiler is None:
                runs.append({"config": label, "status": "skipped", "reason": "no local tsc (npm install)"})
                continue
            result = run_command([str(compiler), "--noEmit", "--pretty", "false", "-p", str(config)], config.parent, timeout)
            errors = len(re.findall(r"error TS\d+", result["output"]))
            runs.append({"config": label, "status": result["status"], "errors": errors,
                         "seconds": result["seconds"], "output": result["output"][-4000:]})
    return runs


def check_typescript_coverage(project_path: Path, run_compiler: bool = True, timeout: int = 300) -> dict[str, Any]:
    files = _source_files(project_path, {".ts", ".tsx", ".mts", ".cts"})
    result: dict[str, Any] = {"type": "typescript", "files": len(files), "errors": [], "warnings": [], "ok": [],
                              "stats": {"any_count": 0, "files_with_any": 0, "suppression_count": 0, "compiler_runs": []}}
    if not files:
        return result
    stats = result["stats"]
    any_pattern = re.compile(r"(?::\s*any\b(?!\s*\w)|\bas\s+any\b|<any>|\bany\[\])")
    suppression_pattern = re.compile(r"@ts-(?:ignore|nocheck)")
    for file_path in files:
        content = re.sub(r"/\*.*?\*/|(?<!:)//(?!\s*@ts-)[^\n]*", "", read_text(file_path), flags=re.S)
        any_count = len(any_pattern.findall(content))
        stats["any_count"] += any_count
        stats["files_with_any"] += int(any_count > 0)
        stats["suppression_count"] += len(suppression_pattern.findall(content))

    any_threshold = max(10, math.ceil(len(files) * 0.25))
    suppression_threshold = max(3, math.ceil(len(files) * 0.05))
    if stats["any_count"] > any_threshold:
        result["errors"].append(f"{stats['any_count']} explicit 'any' usages (threshold {any_threshold} for {len(files)} files)")
    elif stats["any_count"]:
        result["warnings"].append(f"{stats['any_count']} explicit 'any' usage(s) in {stats['files_with_any']} file(s)")
    else:
        result["ok"].append("no explicit 'any'")
    if stats["suppression_count"] > suppression_threshold:
        result["errors"].append(f"{stats['suppression_count']} @ts-ignore/@ts-nocheck (threshold {suppression_threshold})")
    elif stats["suppression_count"]:
        result["warnings"].append(f"{stats['suppression_count']} @ts-ignore/@ts-nocheck comment(s)")

    if run_compiler:
        stats["compiler_runs"] = _run_typescript_compilers(project_path, timeout)
    for run in stats["compiler_runs"]:
        if run["status"] == "passed":
            result["ok"].append(f"tsc passed: {run['config']}")
        elif run["status"] == "skipped":
            result["warnings"].append(f"tsc not run for {run['config']}: {run['reason']} (NOT VERIFIED)")
        else:
            detail = f"{run['errors']} error(s)" if run.get("errors") else run["status"]
            result["errors"].append(f"tsc failed for {run['config']}: {detail}")
    return result


def _annotation_complete(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    positional = [*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs]
    relevant = [arg for arg in positional if arg.arg not in {"self", "cls"}]
    args_typed = all(arg.annotation is not None for arg in relevant)
    varargs_typed = node.args.vararg is None or node.args.vararg.annotation is not None
    kwargs_typed = node.args.kwarg is None or node.args.kwarg.annotation is not None
    returns_typed = node.returns is not None or node.name == "__init__"
    return args_typed and varargs_typed and kwargs_typed and returns_typed


def check_python_coverage(project_path: Path) -> dict[str, Any]:
    files = _source_files(project_path, {".py"})
    result: dict[str, Any] = {"type": "python", "files": len(files), "errors": [], "warnings": [], "ok": [],
                              "stats": {"typed_functions": 0, "untyped_functions": 0, "any_count": 0, "parse_errors": []}}
    if not files:
        return result
    stats = result["stats"]
    for file_path in files:
        try:
            tree = ast.parse(read_text(file_path), filename=str(file_path))
        except SyntaxError as exc:
            stats["parse_errors"].append(f"{file_path.relative_to(project_path).as_posix()}:{exc.lineno} {exc.msg}")
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                key = "typed_functions" if _annotation_complete(node) else "untyped_functions"
                stats[key] += 1
            elif isinstance(node, ast.Name) and node.id == "Any":
                stats["any_count"] += 1
    total = stats["typed_functions"] + stats["untyped_functions"]
    ratio = (stats["typed_functions"] / total * 100) if total else 100.0
    stats["typed_ratio"] = round(ratio, 1)
    for error in stats["parse_errors"][:10]:
        result["errors"].append(f"syntax error: {error}")
    message = f"{ratio:.0f}% of {total} function(s) fully annotated"
    (result["ok"] if ratio >= 65 else result["warnings"]).append(message)
    if stats["any_count"]:
        result["warnings"].append(f"{stats['any_count']} typing.Any reference(s)")
    return result


def main() -> int:
    utf8_console()
    parser = argparse.ArgumentParser(description="TypeScript compiler check and escape-hatch / annotation coverage.")
    parser.add_argument("project", nargs="?", default=".", help="project directory (default: .)")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    parser.add_argument("--skip-compiler", action="store_true", help="do not run tsc (source scan only)")
    parser.add_argument("--timeout", type=int, default=300, help="seconds per tsc run (default: 300)")
    args = parser.parse_args()
    project = resolve_project(parser, args.project)

    results = [r for r in (check_typescript_coverage(project, not args.skip_compiler, args.timeout),
                           check_python_coverage(project)) if r["files"]]
    failed = any(r["errors"] for r in results)
    if args.json:
        print(json.dumps({"script": "type_coverage", "project": str(project), "passed": not failed,
                          "results": results}, indent=2, ensure_ascii=False))
        return 1 if failed else 0

    print(f"Type safety: {project}")
    if not results:
        print("No TypeScript or Python files found.")
        return 0
    for r in results:
        print(f"\n{r['type']} ({r['files']} files)")
        for item in r["errors"]:
            print(f"  error    {item}")
        for item in r["warnings"]:
            print(f"  warning  {item}")
        for item in r["ok"]:
            print(f"  ok       {item}")
        for run in r["stats"].get("compiler_runs", []):
            if run["status"] in {"failed", "timeout", "error"} and run.get("output"):
                print("    " + tail(run["output"], 15).replace("\n", "\n    "))
    print(f"\nResult: {'FAIL' if failed else 'PASS'}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
