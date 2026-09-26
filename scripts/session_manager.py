#!/usr/bin/env python3
"""Project snapshot for /status: name, stack, scripts, feature folders, file counts, recent
git activity, open plan tasks and whether project memory exists. Read-only.

Usage:
  python "KIT/scripts/session_manager.py" status [project]
  python "KIT/scripts/session_manager.py" status . --json
  python "KIT/scripts/session_manager.py" info [project]      # package metadata as JSON
Exit codes: 0 ok, 2 usage.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from checklist import detect_stack, package_manager  # noqa: E402

EXCLUDE = {".git", "node_modules", ".next", ".nuxt", ".svelte-kit", "dist", "build", "out", ".agents",
           ".gemini", "__pycache__", ".venv", "venv", "vendor", "storage", "coverage", ".turbo", ".cache"}
FEATURE_PARENTS = ("src/features", "src/modules", "src/components", "src/app", "app", "src/pages",
                   "src/services", "app/Http/Controllers", "app/Models", "resources/views", "components")


def analyze_package(root: Path) -> dict[str, Any]:
    info: dict[str, Any] = {"name": root.name, "version": None, "scripts": []}
    pkg = root / "package.json"
    if pkg.is_file():
        try:
            data = json.loads(pkg.read_text("utf-8"))
        except (OSError, ValueError) as exc:
            info["error"] = f"package.json unreadable: {exc}"
        else:
            info.update(name=data.get("name") or root.name, version=data.get("version"),
                        scripts=sorted((data.get("scripts") or {}).keys()),
                        packageManager=package_manager(root))
    composer = root / "composer.json"
    if composer.is_file():
        try:
            data = json.loads(composer.read_text("utf-8"))
            info.setdefault("composer", {})["name"] = data.get("name")
            info["composer"]["require"] = sorted((data.get("require") or {}).keys())[:15]
        except (OSError, ValueError):
            pass
    pyproject = root / "pyproject.toml"
    if pyproject.is_file():
        m = re.search(r'^name\s*=\s*"([^"]+)"', pyproject.read_text("utf-8", errors="replace"), re.M)
        if m:
            info["python_name"] = m.group(1)
    return info


def count_files(root: Path) -> dict[str, Any]:
    total, by_ext = 0, Counter()
    for _dir, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in EXCLUDE]
        for name in files:
            total += 1
            by_ext[Path(name).suffix.lower() or "(none)"] += 1
    return {"total": total, "top_extensions": dict(by_ext.most_common(8))}


def detect_features(root: Path, limit: int = 12) -> list[str]:
    features: list[str] = []
    for parent in FEATURE_PARENTS:
        folder = root / parent
        if folder.is_dir():
            for child in sorted(folder.iterdir()):
                if child.is_dir() and not child.name.startswith((".", "_")) and child.name not in features:
                    features.append(child.name)
    return features[:limit]


def git_info(root: Path) -> dict[str, Any] | None:
    git = shutil.which("git")
    if not git:
        return None

    def run(*args: str) -> str | None:
        try:
            proc = subprocess.run([git, *args], cwd=root, capture_output=True, text=True, encoding="utf-8",
                                  errors="replace", timeout=20, check=False)
        except (OSError, subprocess.TimeoutExpired):
            return None
        return proc.stdout if proc.returncode == 0 else None

    if run("rev-parse", "--is-inside-work-tree") is None:
        return None
    status = run("status", "--porcelain") or ""
    log = run("log", "-5", "--pretty=format:%h %ad %s", "--date=short") or ""
    return {
        "branch": (run("branch", "--show-current") or "").strip() or None,
        "uncommitted": len([ln for ln in status.splitlines() if ln.strip()]),
        "recent_commits": [ln for ln in log.splitlines() if ln.strip()],
    }


def open_plan_tasks(root: Path, limit: int = 10) -> list[dict[str, Any]]:
    plans = []
    for folder in (root / "docs" / "plans", root / "docs" / "proplan"):
        if not folder.is_dir():
            continue
        for path in sorted(folder.rglob("*.md")):
            try:
                text = path.read_text("utf-8", errors="replace")
            except OSError:
                continue
            open_items = len(re.findall(r"^\s*- \[ \]", text, re.M))
            done = len(re.findall(r"^\s*- \[[xX]\]", text, re.M))
            if open_items:
                plans.append({"plan": path.relative_to(root).as_posix(), "open": open_items, "done": done})
    return plans[:limit]


def snapshot(root: Path) -> dict[str, Any]:
    stack = detect_stack(root)
    return {
        "project": analyze_package(root),
        "path": str(root),
        "stack": stack.names,
        "features": detect_features(root),
        "files": count_files(root),
        "git": git_info(root),
        "plans": open_plan_tasks(root),
        "memory": (root / ".agents" / "memory" / "MEMORY.md").is_file(),
        "design_md": (root / "DESIGN.md").is_file(),
    }


def print_status(snap: dict[str, Any]) -> None:
    proj = snap["project"]
    print(f"Project:  {proj.get('name')}" + (f" {proj['version']}" if proj.get("version") else ""))
    print(f"Path:     {snap['path']}")
    print(f"Stack:    {', '.join(snap['stack']) or 'unknown'}")
    if proj.get("scripts"):
        print(f"Scripts:  {', '.join(proj['scripts'][:12])}")
    print(f"Features: {', '.join(snap['features']) or 'none detected'}")
    files = snap["files"]
    exts = ", ".join(f"{k} {v}" for k, v in files["top_extensions"].items())
    print(f"Files:    {files['total']} ({exts})")
    git = snap["git"]
    if git:
        print(f"Git:      branch {git['branch'] or '(detached)'}, {git['uncommitted']} uncommitted change(s)")
        for line in git["recent_commits"]:
            print(f"          {line}")
    else:
        print("Git:      not a repository (or git not installed)")
    for plan in snap["plans"]:
        print(f"Plan:     {plan['plan']} - {plan['open']} open, {plan['done']} done")
    print(f"Memory:   {'.agents/memory/MEMORY.md' if snap['memory'] else 'none'}")
    print(f"Design:   {'DESIGN.md' if snap['design_md'] else 'no DESIGN.md'}")


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
        except (AttributeError, ValueError):
            pass
    parser = argparse.ArgumentParser(description="Read-only project snapshot for /status.",
                                     epilog="Exit codes: 0 ok, 2 usage.")
    parser.add_argument("command", choices=["status", "info"], help="status: snapshot; info: package metadata")
    parser.add_argument("path", nargs="?", default=".", help="project path (default: .)")
    parser.add_argument("--json", action="store_true", help="print JSON")
    args = parser.parse_args(argv)
    root = Path(args.path).resolve()
    if not root.is_dir():
        print(f"session_manager: not a directory: {root}", file=sys.stderr)
        return 2
    if args.command == "info":
        print(json.dumps(analyze_package(root), indent=2, ensure_ascii=False))
        return 0
    snap = snapshot(root)
    if args.json:
        print(json.dumps(snap, indent=2, ensure_ascii=False))
    else:
        print_status(snap)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
