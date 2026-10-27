"""Behavioral health checks in an isolated configuration, without mutations."""
from pathlib import Path
import hashlib
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location('kit_health_test_target', SCRIPTS / 'kit_doctor.py')
doctor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(doctor)


def hashes(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file()}


class KitHealthTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.source = self.root / 'source'
        self.config = self.root / 'profile' / 'config'
        self.plugin = self.config / 'plugins' / 'ag-kit-v2'
        for name in ('agents', 'skills', 'scripts', 'rules'):
            (self.source / name).mkdir(parents=True)
        (self.source / 'VERSION').write_text('2.8.0\n', 'utf-8')
        (self.source / 'plugin.json').write_text('{"name":"ag-kit-v2","version":"2.8.0"}', 'utf-8')
        (self.source / 'scripts' / 'example.py').write_text('print("example")\n', 'utf-8')
        for name in doctor.KIT_RULES:
            body = f'---\nname: {name}\nversion: 2.8.0\n---\n'
            if name == 'kit-core':
                body += f'`KIT` = `{(self.root / "template-kit").as_posix()}`\n'
            (self.source / 'rules' / f'{name}.md').write_text(body, 'utf-8')
        shutil.copytree(self.source, self.plugin, ignore=shutil.ignore_patterns('rules'))
        shutil.copytree(self.source / 'rules', self.config / 'rules')
        core = self.config / 'rules' / 'kit-core.md'
        core.write_text(core.read_text('utf-8').replace((self.root / 'template-kit').as_posix(), self.plugin.as_posix()), 'utf-8')
        self.global_file = self.config.parent / 'GEMINI.md'
        self.global_file.write_text(f'Personal note.\n<!-- AGKIT2:START -->\nKit: `{self.plugin.as_posix()}`\n<!-- AGKIT2:END -->\n', 'utf-8')
        self.validation = mock.patch.object(doctor, 'validate', return_value=[])
        self.validation.start()

    def tearDown(self):
        self.validation.stop()
        self.tmp.cleanup()

    def report(self):
        return doctor.diagnose(self.source, self.config)

    def test_healthy_rebased_install_is_read_only(self):
        before = hashes(self.root)
        report = self.report()
        self.assertEqual('PASS', report['outcome'])
        self.assertTrue(report['read_only'])
        self.assertEqual(before, hashes(self.root))

    def test_missing_installed_file_is_not_healthy(self):
        (self.plugin / 'scripts' / 'example.py').unlink()
        report = self.report()
        self.assertEqual('INCOMPLETE', report['outcome'])
        self.assertFalse(report['verified'])
        self.assertIn('install.drift', {f['code'] for f in report['findings']})

    def test_extra_installed_file_is_stale(self):
        (self.plugin / 'scripts' / 'obsolete.py').write_text('# stale\n', 'utf-8')
        self.assertIn('install.stale_files', {f['code'] for f in self.report()['findings']})

    def test_unrelated_v3_name_is_not_a_kit_conflict(self):
        path = self.config / 'rules' / 'core.md'
        path.write_text('---\nname: core\nversion: 3.0.0\n---\nKeep personal preferences.\n', 'utf-8')
        self.assertEqual('PASS', self.report()['outcome'])
        path.write_text('---\nname: core\nversion: 3.0.0\n---\nAG Kit v3\n', 'utf-8')
        self.assertIn('rules.legacy_conflict', {f['code'] for f in self.report()['findings']})

    def test_duplicate_entrypoint_is_not_healthy(self):
        text = self.global_file.read_text('utf-8')
        self.global_file.write_text(text + text, 'utf-8')
        self.assertIn('entrypoint.managed_block', {f['code'] for f in self.report()['findings']})

    def test_installed_only_cannot_claim_source_sync(self):
        report = doctor.diagnose(self.plugin, self.config)
        self.assertEqual('INCOMPLETE', report['outcome'])
        self.assertIn('source.sync_not_verified', {f['code'] for f in report['findings']})


if __name__ == '__main__':
    unittest.main()
