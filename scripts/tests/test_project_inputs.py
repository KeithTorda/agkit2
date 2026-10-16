"""Malformed project metadata and failed Git reads cannot masquerade as clean state."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import checklist
import session_manager
from validation_runner import execute, suite_outcome


class ProjectInputTests(unittest.TestCase):
    def test_invalid_dependency_section_is_a_reported_defect_not_a_crash(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'package.json').write_text('{"dependencies":["react"]}', 'utf-8')
            steps = checklist.build_steps(root, 'quick', None)
            self.assertEqual('FAIL', suite_outcome(execute(steps)))
            self.assertIn('dependencies must be an object', steps[0].failed_reason)

    def test_invalid_json_does_not_become_no_checks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'package.json').write_text('{broken', 'utf-8')
            self.assertEqual('FAIL', suite_outcome(execute(checklist.build_steps(root, 'quick', []))))

    def test_status_reports_non_object_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'package.json').write_text('[]', 'utf-8')
            self.assertIn('error', session_manager.analyze_package(root))

    def test_git_status_failure_is_unknown_not_clean(self):
        def command(args, **kwargs):
            if args[1] == 'status':
                return subprocess.CompletedProcess(args, 1, '', 'read failed')
            return subprocess.CompletedProcess(args, 0, 'true' if args[1] == 'rev-parse' else '', '')
        with mock.patch.object(session_manager.shutil, 'which', return_value='git'), mock.patch.object(session_manager.subprocess, 'run', side_effect=command):
            report = session_manager.git_info(Path('.'))
        self.assertIsNone(report['uncommitted'])
        self.assertIn('worktree status', report['not_verified'])


if __name__ == '__main__':
    unittest.main()
