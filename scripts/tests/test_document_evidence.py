"""A partial document check must not become a complete verification claim."""
import contextlib
import copy
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('doc_evidence_target', SCRIPTS / 'doc_verify.py')
doc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(doc)


class DocumentEvidenceTests(unittest.TestCase):
    def test_partial_primary_render_does_not_mix_with_fallback_pages(self):
        class PartialDocument:
            def __init__(self, _path):
                pass

            def __len__(self):
                return 12

            def __getitem__(self, index):
                if index:
                    raise RuntimeError('primary backend failed after first page')
                image = mock.Mock()
                image.save.side_effect = lambda path: path.write_bytes(b'primary image')
                return types.SimpleNamespace(render=lambda **_: types.SimpleNamespace(to_pil=lambda: image))

        def fallback(command, **_):
            prefix = Path(command[-1])
            for page in range(1, 13):
                prefix.with_name(f'{prefix.name}-{page}.png').write_bytes(b'fallback image')

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            saved = root / 'page-saved.png'
            saved.write_bytes(b'user image')
            with mock.patch.dict(sys.modules, {'pypdfium2': types.SimpleNamespace(PdfDocument=PartialDocument)}), mock.patch('shutil.which', return_value='pdftoppm'), mock.patch('subprocess.run', side_effect=fallback):
                pages = doc.render_pages(root / 'report.pdf', root, 144, 'page')
            self.assertEqual(12, len(pages))
            self.assertTrue(all(path.parent.name == 'poppler' for path in pages))
            self.assertEqual(['page-1.png', 'page-2.png', 'page-3.png'], [p.name for p in pages[:3]])
            self.assertEqual(b'user image', saved.read_bytes())

    def run_report(self, checked=True, pages=1, reference=False, ref_pages=1, diffs=True, page_count=1):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pdf = root / 'report.pdf'
            pdf.write_bytes(b'fixture, parser mocked')
            argv = [str(pdf), '--outdir', str(root / 'artifacts'), '--json']
            if reference:
                ref = root / 'reference.pdf'
                ref.write_bytes(b'fixture')
                argv += ['--reference', str(ref)]
            inspected = {'checked': checked, 'pageCount': page_count if checked else None,
                         'pages': [], 'issues': [], 'notes': []}
            renders = [[root / f'page-{i}.png' for i in range(pages)]]
            if reference:
                renders.append([root / f'ref-{i}.png' for i in range(ref_pages)])
            output = io.StringIO()
            with mock.patch.object(doc, 'inspect', return_value=copy.deepcopy(inspected)), mock.patch.object(doc, 'render_pages', side_effect=renders), mock.patch.object(doc, 'diff_pages', return_value=[{'page': 1}] if diffs else []), contextlib.redirect_stdout(output):
                code = doc.main(argv)
            return code, json.loads(output.getvalue())

    def test_structure_without_render_is_incomplete(self):
        code, report = self.run_report(pages=0)
        self.assertEqual(0, code)  # legacy nonblocking exit does not imply complete evidence
        self.assertEqual('INCOMPLETE', report['outcome'])
        self.assertFalse(report['verified'])

    def test_render_without_structure_is_incomplete(self):
        self.assertEqual('INCOMPLETE', self.run_report(checked=False)[1]['outcome'])

    def test_requested_reference_without_diff_is_incomplete(self):
        self.assertEqual('INCOMPLETE', self.run_report(reference=True, diffs=False)[1]['outcome'])

    def test_partial_page_render_fails(self):
        code, report = self.run_report(pages=1, page_count=2)
        self.assertEqual(1, code)
        self.assertEqual('FAIL', report['outcome'])

    def test_complete_artifacts_have_an_explicit_limited_scope(self):
        code, report = self.run_report(reference=True)
        self.assertEqual(0, code)
        self.assertEqual('PASS', report['outcome'])
        self.assertIn('visual inspection', report['verificationScope'])


if __name__ == '__main__':
    unittest.main()
