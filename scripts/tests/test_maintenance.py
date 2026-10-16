"""Behavioral regressions for update checks and release evidence."""
from __future__ import annotations

import importlib.util
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


update = load('update_kit')
release = load('verify_all')
runner = load('validation_runner')


class UpdateBehaviorTests(unittest.TestCase):
    def exercise(self, same=True, dirty=False, check=True, branch='main', pull_error=False):
        self.calls = []
        def command(args, cwd):
            self.calls.append(args)
            tail = args[1:]
            output = ''
            code = 0
            if tail == ['rev-parse', 'HEAD']:
                output = 'abc123\n'
            elif tail and tail[0] == 'rev-parse':
                output = 'abc123\n' if same else 'def456\n'
            elif tail == ['status', '--porcelain']:
                output = ' M rules/design-rules.md\n' if dirty else ''
            elif tail == ['branch', '--show-current']:
                output = branch + '\n'
            elif tail and tail[0] == 'pull' and pull_error:
                code = 1
            return subprocess.CompletedProcess(args, code, output, 'simulated failure' if code else '')
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / '.git').mkdir()
            (repo / 'install.ps1').write_text('# fixture\n', 'utf-8')
            argv = ['--repo', str(repo)] + (['--check'] if check else [])
            with mock.patch.object(update, 'run_cmd', side_effect=command), mock.patch.object(update.shutil, 'which', side_effect=lambda cmd: cmd):
                return update.main(argv)

    def test_check_up_to_date_never_pulls_or_installs(self):
        self.assertEqual(0, self.exercise())
        self.assertFalse(any('pull' in call or '-File' in call for call in self.calls))

    def test_check_updates_available_never_pulls_or_installs(self):
        self.assertEqual(0, self.exercise(same=False))
        self.assertFalse(any('pull' in call or '-File' in call for call in self.calls))

    def test_dirty_source_is_preserved(self):
        self.assertEqual(1, self.exercise(same=False, dirty=True, check=False))
        self.assertFalse(any('pull' in call or '-File' in call for call in self.calls))

    def test_diverged_update_does_not_install_after_pull_failure(self):
        self.assertEqual(1, self.exercise(same=False, check=False, pull_error=True))
        self.assertTrue(any('--ff-only' in call for call in self.calls))
        self.assertFalse(any('-File' in call for call in self.calls))

    def test_non_target_branch_does_not_pull_or_install(self):
        self.assertEqual(1, self.exercise(same=False, check=False, branch='feature'))
        self.assertFalse(any('pull' in call or '-File' in call for call in self.calls))


class ReleaseEvidenceTests(unittest.TestCase):
    def test_php_syntax_scope_has_no_silent_300_file_cap(self):
        import checklist
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            for number in range(301):
                (project / f'source_{number:03}.php').write_text('<?php\n', 'utf-8')
            self.assertEqual(301, len(checklist._project_php_files(project)))

    def test_project_test_script_preserves_custom_config(self):
        import checklist
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / 'package.json').write_text('{"scripts":{"test":"vitest --config special.ts"},"devDependencies":{"vitest":"1.0"}}', 'utf-8')
            with mock.patch.object(checklist, 'which', return_value='npm'), mock.patch.object(checklist, 'node_bin', return_value='/fake/vitest'):
                steps = checklist.node_steps(project, checklist.detect_stack(project), None, True)
            test_step = next(step for step in steps if step.category == 'tests')
            self.assertEqual([['npm', 'test']], test_step.commands)

    def test_invalid_git_comparison_falls_back_to_whole_project(self):
        import checklist
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            def command(args, **kwargs):
                if args[1:] == ['rev-parse', '--show-toplevel']:
                    return subprocess.CompletedProcess(args, 0, str(project), '')
                if args[1:2] == ['status']:
                    return subprocess.CompletedProcess(args, 0, '', '')
                return subprocess.CompletedProcess(args, 128, '', 'unknown revision')
            with mock.patch.object(checklist, 'which', return_value='git'), mock.patch.object(checklist.subprocess, 'run', side_effect=command):
                scope, label = checklist.resolve_scope(project, 'quick', False, 'missing-ref')
            self.assertIsNone(scope)
            self.assertIn('scope unavailable', label)

    def test_full_test_runner_does_not_suppress_no_test_failure(self):
        import checklist
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / 'package.json').write_text('{"devDependencies":{"vitest":"1.0"}}', 'utf-8')
            with mock.patch.object(checklist, 'node_bin', side_effect=lambda p, name: '/fake/vitest' if name == 'vitest' else None):
                steps = checklist.node_steps(project, checklist.detect_stack(project), None, True)
            test_step = next(step for step in steps if step.category == 'tests')
            self.assertNotIn('--passWithNoTests', test_step.commands[0])

    def test_runtime_helpers_report_skip_without_pass_claim(self):
        root = SCRIPTS.parent
        for name, rel, function in [
            ('smoke_evidence', 'skills/testing-patterns/scripts/playwright_runner.py', 'run_test'),
            ('lighthouse_evidence', 'skills/performance-profiling/scripts/lighthouse_audit.py', 'run_lighthouse'),
        ]:
            with self.subTest(helper=name):
                spec = importlib.util.spec_from_file_location(name, root / rel)
                helper = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(helper)
                output = io.StringIO()
                skipped = {'status': 'skipped', 'passed': False, 'reason': 'tool unavailable', 'fix': 'install if needed'}
                with mock.patch.object(helper, function, return_value=skipped), mock.patch.object(sys, 'argv', [rel, 'http://localhost:3000', '--json']), contextlib.redirect_stdout(output):
                    self.assertEqual(0, helper.main())
                payload = json.loads(output.getvalue())
                self.assertEqual('SKIPPED', payload['outcome'])
                self.assertFalse(payload['passed'])
                self.assertFalse(payload['verified'])

    def test_child_skip_is_not_reported_as_pass(self):
        step = runner.Step('smoke', 'runtime', [[sys.executable, '-c',
                           'import json; print(json.dumps({"status":"skipped", "reason":"browser missing"}))']],
                           required=True, json_status=True)
        result = runner.run_step(step)
        self.assertEqual('skipped', result.status)
        self.assertEqual('INCOMPLETE', runner.suite_outcome([result]))

    def test_json_failure_cannot_pass_with_zero_exit(self):
        step = runner.Step('smoke', 'runtime', [[sys.executable, '-c',
                           'print(\'{"status":"failed","passed":false}\')']], required=True, json_status=True)
        result = runner.run_step(step)
        self.assertEqual('failed', result.status)
        self.assertEqual('FAIL', runner.suite_outcome([result]))

    def test_unknown_child_evidence_is_incomplete(self):
        step = runner.Step('smoke', 'runtime', [[sys.executable, '-c',
                           'print(\'{"status":"banana"}\')']], required=True, json_status=True)
        self.assertEqual('INCOMPLETE', runner.suite_outcome([runner.run_step(step)]))

    def test_disabled_applicable_build_remains_explicitly_unverified(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / 'package.json').write_text('{"scripts":{"build":"vite build"}}', 'utf-8')
            steps = release.release_steps(project, None, True, False)
            build = next(step for step in steps if step.category == 'build')
            self.assertTrue(build.skip_not_verified)
            self.assertEqual('--no-build', build.skip_reason)


if __name__ == '__main__':
    unittest.main()
