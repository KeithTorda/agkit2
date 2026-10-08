#!/usr/bin/env python3
"""motionv_doctor.py - check (and optionally install) what /motionv needs to make videos.

Checks: Node.js >= 22, npm/npx, git, FFmpeg + FFprobe, the HyperFrames CLI and its render
browser, the engine skills Antigravity reads (HyperFrames, optionally Remotion), and optional
extras (Python TTS, whisper). Nothing is installed unless you pass --install.

Usage:
  python motionv_doctor.py                     check only
  python motionv_doctor.py --install           install missing pieces (asks nothing; the agent asks you first)
  python motionv_doctor.py --install --engine all   also install the Remotion skills
  python motionv_doctor.py --json

Exit codes: 0 ready, 1 something required is missing, 2 usage error.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

IS_WIN = platform.system() == "Windows"
HOME = Path.home()
# Antigravity global skill scope (codelab: ~/.gemini/config/skills). Override with --skills-dir.
DEFAULT_SKILLS_DIR = HOME / ".gemini" / "config" / "skills"
ENGINE_REPOS = {
    "hyperframes": ("https://github.com/heygen-com/hyperframes.git", "skills"),
    "remotion": ("https://github.com/remotion-dev/skills.git", "skills"),
}
HYPERFRAMES_MARKER = "hyperframes"          # folder name of the HyperFrames entry skill
REMOTION_MARKER = "remotion-best-practices"  # folder name of a core Remotion skill


def run(cmd: list[str], timeout: int = 600, env: dict | None = None) -> tuple[int, str]:
    exe = shutil.which(cmd[0])
    if not exe and IS_WIN:
        candidate = Path.home() / "AppData" / "Local" / "Microsoft" / "WinGet" / "Links" / f"{cmd[0]}.exe"
        if candidate.is_file():
            exe = str(candidate)
    if not exe:
        return 127, f"{cmd[0]} not found"
    try:
        p = subprocess.run([exe, *cmd[1:]], capture_output=True, text=True, timeout=timeout,
                           encoding="utf-8", errors="replace",
                           env={**os.environ, **(env or {})})
        return p.returncode, (p.stdout + p.stderr).strip()
    except subprocess.TimeoutExpired:
        return 124, f"timed out after {timeout}s"
    except OSError as e:
        return 126, str(e)


def version_of(cmd: list[str]) -> str | None:
    code, out = run(cmd, timeout=60)
    if code != 0:
        return None
    m = re.search(r"(\d+\.\d+(?:\.\d+)?)", out)
    return m.group(1) if m else out.splitlines()[0][:40]


class Report:
    def __init__(self) -> None:
        self.rows: list[dict] = []

    def add(self, name: str, ok: bool, detail: str, required: bool = True, fix: str = "") -> None:
        self.rows.append({"name": name, "ok": ok, "required": required, "detail": detail, "fix": fix})

    @property
    def missing_required(self) -> list[dict]:
        return [r for r in self.rows if r["required"] and not r["ok"]]


def check_node(rep: Report) -> None:
    v = version_of(["node", "--version"])
    if not v:
        rep.add("Node.js", False, "not found", fix="Install Node.js 22+ (winget install OpenJS.NodeJS.LTS)")
        return
    major = int(v.split(".")[0])
    rep.add("Node.js", major >= 22, f"v{v}", fix="" if major >= 22 else "Upgrade to Node.js 22+ (winget upgrade OpenJS.NodeJS.LTS)")
    rep.add("npx", bool(shutil.which("npx")), shutil.which("npx") or "not found", fix="Comes with Node.js; reinstall Node")


def check_git(rep: Report) -> None:
    v = version_of(["git", "--version"])
    rep.add("git", bool(v), v or "not found", fix="Install Git (winget install Git.Git)")


def check_ffmpeg(rep: Report) -> None:
    for tool in ("ffmpeg", "ffprobe"):
        v = version_of([tool, "-version"])
        rep.add(tool, bool(v), v or "not found",
                fix="winget install Gyan.FFmpeg  (then open a new terminal so PATH updates)")


def check_hyperframes(rep: Report) -> None:
    if not shutil.which("npx"):
        rep.add("HyperFrames CLI", False, "needs npx", fix="Install Node.js 22+")
        return
    code, out = run(["npx", "--yes", "hyperframes@latest", "--version"], timeout=600,
                    env={"HYPERFRAMES_SKIP_SKILLS": "1"})
    ver = re.search(r"(\d+\.\d+\.\d+)", out)
    rep.add("HyperFrames CLI", code == 0 and bool(ver), f"v{ver.group(1)}" if ver else out[-160:],
            fix="Check network access to registry.npmjs.org, then rerun")
    if code != 0:
        return
    code, out = run(["npx", "--yes", "hyperframes@latest", "doctor"], timeout=600,
                    env={"HYPERFRAMES_SKIP_SKILLS": "1", "NO_COLOR": "1"})
    clean = re.sub(r"\x1b\[[0-9;]*m", "", out)
    # Optional extras reported by `hyperframes doctor`
    for label, key in (("TTS voice (Kokoro, optional)", "TTS"), ("Transcription (whisper, optional)", "whisper")):
        line = next((l for l in clean.splitlines() if key.lower() in l.lower()), "")
        has_ok = "✓" in line or "[ok" in line.lower()
        detail = line.replace("✓", "[ok]").replace("✗", "[x]").replace("\u2717", "[x]").strip()[:120] or "not reported"
        rep.add(label, has_ok, detail, required=False,
                fix="See `npx hyperframes doctor` for the install line")


def skill_installed(skills_dir: Path, marker: str) -> bool:
    return (skills_dir / marker / "SKILL.md").is_file()


def check_skills(rep: Report, skills_dir: Path, engine: str) -> None:
    rep.add("HyperFrames skills for Antigravity", skill_installed(skills_dir, HYPERFRAMES_MARKER),
            str(skills_dir / HYPERFRAMES_MARKER), fix="python motionv_doctor.py --install")
    rep.add("Remotion skills for Antigravity", skill_installed(skills_dir, REMOTION_MARKER),
            str(skills_dir / REMOTION_MARKER), required=(engine in ("remotion", "all")),
            fix="python motionv_doctor.py --install --engine remotion")


def check_extras(rep: Report) -> None:
    py = shutil.which("python") or shutil.which("python3")
    rep.add("Python", bool(py), py or "not found", required=False, fix="Only needed for local TTS / music models")


# ---------- install ----------

def install_engine_skills(name: str, skills_dir: Path, log: list[str]) -> bool:
    url, sub = ENGINE_REPOS[name]
    skills_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=f"motionv-{name}-") as tmp:
        dest = Path(tmp) / "repo"
        env = {"GIT_LFS_SKIP_SMUDGE": "1"}
        code, out = run(["git", "clone", "--depth", "1", "--filter=blob:none", "--sparse", url, str(dest)],
                        timeout=900, env=env)
        if code == 0:
            code, out = run(["git", "-C", str(dest), "sparse-checkout", "set", sub], timeout=900, env=env)
        if code != 0:
            log.append(f"[fail] clone {url}: {out[-300:]}")
            return False
        src = dest / sub
        count = 0
        for skill in sorted(p for p in src.iterdir() if (p / "SKILL.md").is_file()):
            target = skills_dir / skill.name
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(skill, target)
            count += 1
        log.append(f"[ok] {name}: {count} skills -> {skills_dir}")
        return count > 0


def install_missing(rep: Report, skills_dir: Path, engine: str, skip_browser: bool = False) -> list[str]:
    log: list[str] = []
    by_name = {r["name"]: r for r in rep.rows}

    if not by_name.get("ffmpeg", {}).get("ok") or not by_name.get("ffprobe", {}).get("ok"):
        if IS_WIN and shutil.which("winget"):
            code, out = run(["winget", "install", "--id", "Gyan.FFmpeg", "-e",
                             "--accept-source-agreements", "--accept-package-agreements"], timeout=1800)
            log.append(("[ok] " if code == 0 else "[fail] ") + "winget install Gyan.FFmpeg" +
                       ("" if code == 0 else f": {out[-300:]}"))
            if code == 0:
                log.append("[note] open a new terminal (or restart Antigravity) so ffmpeg is on PATH")
        else:
            log.append("[skip] ffmpeg: install it with your package manager (apt install ffmpeg / brew install ffmpeg)")

    if by_name.get("git", {}).get("ok"):
        if not skill_installed(skills_dir, HYPERFRAMES_MARKER):
            install_engine_skills("hyperframes", skills_dir, log)
        if engine in ("remotion", "all") and not skill_installed(skills_dir, REMOTION_MARKER):
            install_engine_skills("remotion", skills_dir, log)
    else:
        log.append("[skip] engine skills: git is required")

    if by_name.get("HyperFrames CLI", {}).get("ok") and not skip_browser:
        code, out = run(["npx", "--yes", "hyperframes@latest", "browser", "ensure"], timeout=900,
                        env={"HYPERFRAMES_SKIP_SKILLS": "1"})
        log.append(("[ok] " if code == 0 else "[fail] ") + "hyperframes browser ensure" +
                   ("" if code == 0 else f": {out[-300:]}"))
    return log


def main() -> int:
    ap = argparse.ArgumentParser(description="Check and install what /motionv needs.")
    ap.add_argument("--install", action="store_true", help="install missing pieces")
    ap.add_argument("--engine", choices=["hyperframes", "remotion", "all"], default="hyperframes",
                    help="which engine skills are required (default: hyperframes)")
    ap.add_argument("--skills-dir", type=Path, default=DEFAULT_SKILLS_DIR,
                    help=f"where Antigravity reads global skills (default: {DEFAULT_SKILLS_DIR})")
    ap.add_argument("--skip-browser", action="store_true",
                    help="do not download the render browser (use HYPERFRAMES_BROWSER_PATH instead)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rep = Report()
    check_node(rep)
    check_git(rep)
    check_ffmpeg(rep)
    check_hyperframes(rep)
    check_skills(rep, args.skills_dir, args.engine)
    check_extras(rep)

    log: list[str] = []
    if args.install:
        log = install_missing(rep, args.skills_dir, args.engine, args.skip_browser)
        rep2 = Report()
        check_node(rep2); check_git(rep2); check_ffmpeg(rep2)
        rep2.rows += [r for r in rep.rows if r["name"].startswith(("HyperFrames CLI", "TTS", "Transcription"))]
        check_skills(rep2, args.skills_dir, args.engine)
        check_extras(rep2)
        rep = rep2

    missing = rep.missing_required
    if args.json:
        print(json.dumps({"ready": not missing, "checks": rep.rows, "install_log": log}, indent=2))
    else:
        print("motionv doctor")
        for r in rep.rows:
            mark = "ok  " if r["ok"] else ("MISS" if r["required"] else "opt ")
            print(f"  [{mark}] {r['name']:<36} {r['detail']}")
            if not r["ok"] and r["fix"]:
                print(f"         fix: {r['fix']}")
        for line in log:
            print("  " + line)
        print("Result: READY" if not missing else
              f"Result: NOT READY - {len(missing)} required item(s) missing"
              + ("" if args.install else " (run with --install after the user agrees)"))
    return 0 if not missing else 1


if __name__ == "__main__":
    sys.exit(main())
