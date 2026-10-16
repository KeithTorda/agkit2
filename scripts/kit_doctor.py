#!/usr/bin/env python3
"""Read-only AGKIT2 source and installation health; never installs or edits files."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
from typing import Any

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_kit import KIT_RULES, validate


def read_text(path: Path) -> str:
    return path.read_text('utf-8-sig')


def default_source() -> Path:
    own = Path(__file__).resolve().parents[1]
    if (own / 'rules').is_dir():
        return own
    editable = Path.home() / 'Desktop' / 'agkit2'
    return editable if (editable / 'rules').is_dir() else own


def managed_files(root: Path) -> dict[str, Path]:
    found = {}
    for name in ('agents', 'skills', 'scripts'):
        folder = root / name
        for path in folder.rglob('*') if folder.is_dir() else ():
            if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc':
                found[path.relative_to(root).as_posix()] = path
    for name in ('plugin.json', 'VERSION', 'LICENSE'):
        if (root / name).is_file():
            found[name] = root / name
    return found


def is_legacy_kit_rule(text: str) -> bool:
    signature = re.search(r'\bAG\s?Kit\b|plugins[/\\]+agkit3|no automatic gates|Ten code rules that apply|Which agent handles which request', text, re.I)
    return bool(signature and re.search(r'^version:\s*3\.', text, re.M)
                and re.search(r'^name:\s*(core|code|routing|design|anti-ai)\s*$', text, re.M))


def diagnose(source: Path, config: Path) -> dict[str, Any]:
    source, config = source.resolve(), config.resolve()
    installed = config / 'plugins' / 'ag-kit-v2'
    rules = config / 'rules'
    global_file = config.parent / 'GEMINI.md'
    findings = []

    def add(level: str, code: str, message: str, paths: list[str] | None = None):
        item = {'level': level, 'code': code, 'message': message}
        if paths:
            item['paths'] = paths[:25]
            item['count'] = len(paths)
        findings.append(item)

    source_has_rules = (source / 'rules').is_dir()
    source_rules = source / 'rules' if source_has_rules else rules
    try:
        invalid = [f for f in validate(source, source_rules) if f.severity in {'error', 'warning'}]
        for issue in invalid:
            add('error' if issue.severity == 'error' else 'warning', 'source.' + issue.code,
                f'{issue.file}:{issue.line}: {issue.message}')
    except (OSError, ValueError) as exc:
        add('error', 'source.unreadable', f'Could not validate source: {exc}')

    versions = {}
    for label, root in (('source', source), ('installed', installed)):
        try:
            versions[label] = read_text(root / 'VERSION').strip()
        except OSError:
            versions[label] = None
            add('warning', label + '.missing_version', f'{label} VERSION unavailable: {root}')

    source_files, installed_files = managed_files(source), managed_files(installed)
    mismatched = []
    if source != installed:
        for rel, path in source_files.items():
            other = installed_files.get(rel)
            try:
                if other is None or hashlib.sha256(path.read_bytes()).digest() != hashlib.sha256(other.read_bytes()).digest():
                    mismatched.append(rel)
            except OSError:
                mismatched.append(rel)
        extras = sorted(set(installed_files) - set(source_files))
        if mismatched:
            add('warning', 'install.drift', 'Installed managed files differ from the editable source.', sorted(mismatched))
        if extras:
            add('warning', 'install.stale_files', 'Installed managed files are absent from source.', extras)
    else:
        add('info', 'source.unavailable', 'Only the installed kit is available; independent source synchronization was not checked.')

    core_source = source / 'rules' / 'core-protocol.md'
    template_root = None
    if core_source.is_file():
        match = re.search(r'`KIT`\s*=\s*`([^`]+)`', read_text(core_source))
        template_root = match.group(1) if match else None
    for name in KIT_RULES:
        active = rules / f'{name}.md'
        if not active.is_file():
            add('warning', 'rules.missing', f'Active managed rule unavailable: {name}.md')
            continue
        source_rule = source / 'rules' / f'{name}.md'
        if source_has_rules and source_rule.is_file():
            expected = read_text(source_rule)
            if name == 'core-protocol' and template_root:
                expected = expected.replace(template_root, installed.as_posix())
            if expected.replace('\r\n', '\n') != read_text(active).replace('\r\n', '\n'):
                add('warning', 'rules.drift', f'Active {name}.md differs from source.')
    if rules.is_dir():
        for path in rules.glob('*.md'):
            if path.stem not in KIT_RULES and is_legacy_kit_rule(read_text(path)):
                add('warning', 'rules.legacy_conflict', f'Recognized legacy kit rule still active: {path.name}')

    try:
        text = read_text(global_file)
        blocks = re.findall(r'<!-- AGKIT2:START -->(.*?)<!-- AGKIT2:END -->', text, re.S)
        if len(blocks) != 1:
            add('warning', 'entrypoint.managed_block', 'Expected one managed AGKIT2 block in GEMINI.md.')
        elif installed.as_posix() not in blocks[0].replace('\\', '/'):
            add('warning', 'entrypoint.path', 'Managed global entrypoint does not identify the active kit path.')
    except OSError:
        add('warning', 'entrypoint.missing', 'Global GEMINI.md is unavailable.')

    tools = {name: bool(shutil.which(name)) for name in ('python', 'node', 'git', 'pwsh', 'powershell')}
    if not source_has_rules:
        add('warning', 'source.sync_not_verified', 'Editable source/rules unavailable; pass --source to verify installation agreement.')
    outcome = 'FAIL' if any(f['level'] == 'error' for f in findings) else ('INCOMPLETE' if any(f['level'] == 'warning' for f in findings) else 'PASS')
    return {'tool': 'AGKIT2 doctor', 'read_only': True, 'outcome': outcome,
            'verified': outcome == 'PASS', 'source': str(source), 'installed': str(installed),
            'versions': versions, 'managed_files_compared': len(source_files) if source != installed else 0,
            'findings': findings, 'tools_available': tools,
            'scope': 'Kit structure and file synchronization only; no generated application or loaded chat was tested.'}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=default_source())
    parser.add_argument('--config-root', type=Path, default=Path.home() / '.gemini' / 'config')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    if not args.source.is_dir():
        parser.error('source must be an existing directory')
    try:
        report = diagnose(args.source, args.config_root)
    except (OSError, ValueError) as exc:
        print(f'Doctor could not complete a read-only check: {exc}', file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"AGKIT2 doctor: {report['outcome']}")
        for item in report['findings']:
            print(f"[{item['level']}] {item['code']}: {item['message']}")
        print(report['scope'])
    return 0 if report['outcome'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
