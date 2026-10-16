import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('suite_evidence_target', ROOT / 'skills/testing-patterns/scripts/test_runner.py')
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class SuiteEvidenceTests(unittest.TestCase):
    def test_package_manager_choice_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / 'package.json').write_text('{"packageManager":"pnpm@9","scripts":{"test":"node --test"}}', 'utf-8')
            with mock.patch.object(runner, 'find_executable', side_effect=lambda name, *a, **kw: name if name == 'pnpm' else None):
                suites, missing = runner.plan_suites(project, False)
            self.assertEqual(['pnpm', 'run', 'test'], suites[0]['cmd'])

    def test_malformed_scripts_are_reported_without_crashing(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / 'package.json').write_text('{"scripts":["test"]}', 'utf-8')
            suites, missing = runner.plan_suites(project, False)
            self.assertEqual([], suites)
            self.assertTrue(missing)

    def test_malformed_node_metadata_does_not_hide_independent_suites(self):
        manifests = [
            '{"scripts":["test"]}',
            '{"scripts":{"test":42}}',
            '{"scripts":{"test:coverage":[]}}',
            '{"dependencies":["vitest"]}',
            '{broken',
            '[]',
        ]
        for manifest in manifests:
            with self.subTest(manifest=manifest), tempfile.TemporaryDirectory() as tmp:
                project = Path(tmp)
                (project / 'package.json').write_text(manifest, 'utf-8')
                (project / 'pyproject.toml').write_text('[project]\nname="fixture"\n', 'utf-8')
                (project / 'test_example.py').write_text('def test_example(): pass\n', 'utf-8')
                (project / 'composer.json').write_text('{}', 'utf-8')
                (project / 'artisan').write_text('fixture', 'utf-8')
                (project / 'vendor').mkdir()
                with mock.patch.object(runner, 'find_executable', return_value=None), \
                     mock.patch.object(runner.shutil, 'which', side_effect=lambda name: 'php' if name == 'php' else None), \
                     mock.patch.object(runner.importlib.util, 'find_spec', return_value=object()):
                    suites, missing = runner.plan_suites(project, False)
                self.assertEqual({'php artisan test', 'pytest'}, {suite['name'] for suite in suites})
                self.assertTrue(any(note.startswith('node:') for note in missing))
                report = self.report(suites, missing)
                self.assertEqual('INCOMPLETE', report['outcome'])
                self.assertEqual(2, len(report['suites']))

    def test_coverage_request_preserves_project_test_configuration(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / 'package.json').write_text('{"scripts":{"test":"vitest --config project.ts"},"devDependencies":{"vitest":"1"}}', 'utf-8')
            with mock.patch.object(runner, 'find_executable', side_effect=lambda name, *a, **kw: name):
                suites, missing = runner.plan_suites(project, True)
            self.assertEqual(['npm', 'test', '--silent'], suites[0]['cmd'])
            self.assertTrue(any('coverage' in note for note in missing))

    def test_native_project_test_command_does_not_require_node_modules(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / 'package.json').write_text('{"scripts":{"test":"node --test"}}', 'utf-8')
            with mock.patch.object(runner, 'find_executable', side_effect=lambda name, *a, **kw: 'npm' if name == 'npm' else None):
                suites, missing = runner.plan_suites(project, False)
            self.assertEqual(['npm', 'test', '--silent'], suites[0]['cmd'])
            self.assertEqual([], missing)

    def report(self, suites, missing, output='1 passed', status='passed'):
        with tempfile.TemporaryDirectory() as tmp:
            text = io.StringIO()
            with mock.patch.object(sys, 'argv', ['test_runner', tmp, '--json']), mock.patch.object(runner, 'plan_suites', return_value=(suites, missing)), mock.patch.object(runner, 'run_command', return_value={'status':status,'returncode':0,'output':output,'seconds':0}), contextlib.redirect_stdout(text):
                runner.main()
            return json.loads(text.getvalue())

    def test_no_suite_cannot_pass(self):
        report = self.report([], [])
        self.assertEqual('SKIPPED', report['outcome'])
        self.assertFalse(report['passed'])

    def test_missing_suite_with_other_pass_is_incomplete(self):
        report = self.report([{'name':'python','cmd':['python']}], ['node unavailable'])
        self.assertEqual('INCOMPLETE', report['outcome'])
        self.assertFalse(report['verified'])

    def test_reported_zero_tests_are_not_completed_evidence(self):
        report = self.report([{'name':'unittest','cmd':['python']}], [], 'Ran 0 tests in 0.0s\nOK')
        self.assertEqual('INCOMPLETE', report['outcome'])
        self.assertFalse(report['passed'])

    def test_all_skipped_pytest_and_unittest_are_incomplete(self):
        for output in ('3 skipped in 0.01s', 'Ran 3 tests in 0.000s\nOK (skipped=3)'):
            with self.subTest(output=output):
                report = self.report([{'name':'python','cmd':['python']}], [], output)
                self.assertEqual('INCOMPLETE', report['outcome'])
                self.assertFalse(report['verified'])
                self.assertEqual('skipped', report['suites'][0]['status'])

    def test_native_node_zero_and_all_skipped_summaries_are_incomplete(self):
        outputs = [
            'TAP version 13\n1..0\n# tests 0\n# pass 0\n# fail 0\n# skipped 0\n',
            'TAP version 13\n# tests 3\n# pass 0\n# fail 0\n# skipped 3\n',
            'ℹ tests 0\nℹ suites 0\nℹ pass 0\nℹ fail 0\nℹ skipped 0\n',
        ]
        for output in outputs:
            with self.subTest(output=output):
                report = self.report([{'name':'node test','cmd':['node']}], [], output)
                self.assertEqual('INCOMPLETE', report['outcome'])
                self.assertFalse(report['verified'])

    def test_executed_tests_with_some_skips_are_still_completed_evidence(self):
        outputs = [
            '2 passed, 3 skipped in 0.01s',
            'Ran 5 tests in 0.000s\nOK (skipped=3)',
            'TAP version 13\n# tests 5\n# pass 2\n# fail 0\n# skipped 3\n',
        ]
        for output in outputs:
            with self.subTest(output=output):
                report = self.report([{'name':'tests','cmd':['unused']}], [], output)
                self.assertEqual('PASS', report['outcome'])
                self.assertEqual(2, report['suites'][0]['counts']['passed'])

    def test_real_failure_is_not_reclassified_as_an_incomplete_skip(self):
        output = 'Ran 3 tests in 0.000s\nFAILED (failures=1, skipped=2)'
        report = self.report([{'name':'python','cmd':['python']}], [], output, status='failed')
        self.assertEqual('FAIL', report['outcome'])
        self.assertEqual(1, report['suites'][0]['counts']['failed'])

    def test_executed_suite_command_passes_with_explicit_scope(self):
        report = self.report([{'name':'python','cmd':['python']}], [])
        self.assertEqual('PASS', report['outcome'])
        self.assertIn('commands only', report['scope'])


if __name__ == '__main__':
    unittest.main()
