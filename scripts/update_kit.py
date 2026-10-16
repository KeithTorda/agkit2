#!/usr/bin/env python3
"""Check or update AGKIT2 without overwriting local work. --check never pulls or installs."""
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess
import sys


def run_cmd(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                          encoding='utf-8', errors='replace', check=False)


def default_repo() -> Path:
    adjacent = Path(__file__).resolve().parents[1]
    return adjacent if (adjacent / '.git').exists() else Path.home() / 'Desktop' / 'agkit2'


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='fetch and compare; never pull or install')
    parser.add_argument('--repo', type=Path, default=default_repo(), help='source Git repository')
    parser.add_argument('--branch', default='main', help='remote branch to compare (default: main)')
    args = parser.parse_args(argv)
    repo = args.repo.resolve()
    git = shutil.which('git')
    if not git or not (repo / '.git').exists():
        print(f'Cannot update: Git or source repository unavailable: {repo}', file=sys.stderr)
        return 2

    def invoke(*parts: str) -> subprocess.CompletedProcess[str]:
        return run_cmd([git, *parts], repo)

    fetched = invoke('fetch', 'origin', args.branch)
    if fetched.returncode:
        print(f'Fetch failed: {fetched.stderr.strip()}', file=sys.stderr)
        return 1
    local = invoke('rev-parse', 'HEAD')
    remote = invoke('rev-parse', f'origin/{args.branch}')
    if local.returncode or remote.returncode:
        print('Could not resolve local and remote revisions.', file=sys.stderr)
        return 1
    same = local.stdout.strip() == remote.stdout.strip()
    status = invoke('status', '--porcelain')
    if status.returncode:
        print('Could not inspect local changes.', file=sys.stderr)
        return 1
    print('Remote matches HEAD.' if same else 'Local and remote revisions differ.')
    if status.stdout.strip():
        print('Local changes exist; no update may overwrite them.')
    if args.check:
        print('Check complete. No pull or installation performed.')
        return 0
    if status.stdout.strip():
        print('Update stopped: preserve or commit your local changes first.', file=sys.stderr)
        return 1
    branch = invoke('branch', '--show-current')
    if branch.returncode or branch.stdout.strip() != args.branch:
        print(f'Update stopped: source must be on {args.branch}.', file=sys.stderr)
        return 1
    if not same:
        pulled = invoke('pull', '--ff-only', 'origin', args.branch)
        if pulled.returncode:
            print(f'Fast-forward update failed: {pulled.stderr.strip()}', file=sys.stderr)
            return 1
    shell = shutil.which('pwsh') or shutil.which('powershell')
    installer = repo / 'install.ps1'
    if not shell or not installer.is_file():
        print('Installer or PowerShell unavailable; installation not verified.', file=sys.stderr)
        return 2
    installed = run_cmd([shell, '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', str(installer)], repo)
    print(installed.stdout.strip())
    if installed.returncode:
        print(installed.stderr.strip(), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
