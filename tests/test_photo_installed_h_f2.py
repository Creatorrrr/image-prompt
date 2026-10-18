"""The normal entrypoint must select a sealed release without research paths."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/photo-prompt-image-generator/scripts'))
import photo_installed_h_f2 as installed


def fixture(root):
    skill = root / 'skill'
    store = root / 'store'
    skill.mkdir()
    native = {'schema': 'photo-runtime-generation/v3', 'source': {'code': {}},
              'members': {}, 'search_layout': {'corpus_sha256': 'corpus'}}
    code = b"print('sealed workflow')\n"
    h = __import__('hashlib').sha256(code).hexdigest()
    native['source']['code']['scripts/photo_workflow.py'] = h
    native['members']['scripts/photo_workflow.py'] = {'sha256': h}
    nid = installed.digest(native)
    nroot = store / 'generations' / nid
    (nroot / 'scripts').mkdir(parents=True)
    (nroot / 'scripts/photo_workflow.py').write_bytes(code)
    (nroot / 'manifest.json').write_text(json.dumps(native))
    source = b'{"source_sha256":"corpus"}'
    manifest = {'schema': 'photo-h-f2-generation/v1', 'native_generation_id': nid,
                'files': {'source-manifest.json': __import__('hashlib').sha256(source).hexdigest()}}
    gid = installed.digest(manifest)
    hroot = store / 'h-f2-generations' / gid
    hroot.mkdir(parents=True)
    (hroot / 'manifest.json').write_text(json.dumps(manifest))
    (hroot / 'source-manifest.json').write_bytes(source)
    config = {'schema': installed.SCHEMA, 'policy': 'photo-h-f2/v1',
              'store_subdirectory': 'h-f2-installed', 'generation_id': gid,
              'native_generation_id': nid, 'code_sha256': installed.digest(native['source']['code'])}
    (skill / installed.CONFIG).write_text(json.dumps(config))
    return skill, store, gid, nroot


class InstalledSearch(unittest.TestCase):
    def test_default_injects_one_policy_and_generation_and_installed_model(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill, store, gid, _ = fixture(Path(tmp))
            with patch.object(installed, 'default_store', return_value=store), patch.object(
                    installed, 'runtime_python', return_value=Path(sys.executable)), patch.object(
                    installed.subprocess, 'run') as child:
                child.return_value.returncode = 0
                self.assertEqual(installed.dispatch(['retrieve', '--run', str(Path(tmp)/'new')], skill_root=skill), 0)
                command = child.call_args.args[0]
                self.assertEqual(command.count('--retrieval-policy'), 1)
                self.assertEqual(command[command.index('--retrieval-policy')+1], 'h-f2')
                self.assertEqual(command[command.index('--generation-id')+1], gid)
                self.assertEqual(command[command.index('--local-embedding-skill')+1], str(skill.resolve()))
                env = child.call_args.kwargs['env']
                self.assertEqual(env['HF_HUB_OFFLINE'], '1')
                for key in ['PYTHONPATH', 'GEMINI_API_KEY', 'GOOGLE_API_KEY', 'OPENAI_API_KEY', 'ANTHROPIC_API_KEY']:
                    self.assertNotIn(key, env)

    def test_tampered_code_stops_before_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill, store, _, native = fixture(Path(tmp))
            (native/'scripts/photo_workflow.py').write_text('tampered')
            with patch.object(installed, 'default_store', return_value=store), patch.object(installed.subprocess, 'run') as child:
                self.assertEqual(installed.dispatch(['retrieve'], skill_root=skill), 2)
                child.assert_not_called()

    def test_explicit_image_render_keeps_its_openai_key_and_removes_gemini(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill, store, _, _ = fixture(Path(tmp))
            with patch.object(installed, 'default_store', return_value=store), patch.object(
                    installed, 'runtime_python', return_value=Path(sys.executable)), patch.object(
                    installed.os, 'environ', {'OPENAI_API_KEY': 'test-image-key', 'GEMINI_API_KEY': 'test'}), patch.object(
                    installed.subprocess, 'run') as child:
                child.return_value.returncode = 0
                self.assertEqual(installed.dispatch(['render-api', '--run', str(Path(tmp)/'new')], skill_root=skill), 0)
                env = child.call_args.kwargs['env']
                self.assertEqual(env['OPENAI_API_KEY'], 'test-image-key')
                self.assertNotIn('GEMINI_API_KEY', env)

    def test_missing_generation_does_not_fall_back_or_create_current(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill, store, gid, _ = fixture(Path(tmp))
            (store/'h-f2-generations'/gid/'manifest.json').unlink()
            with patch.object(installed, 'default_store', return_value=store), patch.object(installed.subprocess, 'run') as child:
                self.assertEqual(installed.dispatch(['retrieve'], skill_root=skill), 2)
                child.assert_not_called()
                self.assertEqual(list(store.rglob('CURRENT.json')), [])

    def test_partial_explicit_binding_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill, store, _, _ = fixture(Path(tmp))
            with patch.object(installed, 'default_store', return_value=store), patch.object(installed.subprocess, 'run') as child:
                self.assertEqual(installed.dispatch(['retrieve', '--runtime-store', str(store)], skill_root=skill), 2)
                child.assert_not_called()

    def test_existing_native_receipt_keeps_original_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill, _, _, _ = fixture(Path(tmp))
            run = Path(tmp)/'native-run'
            run.mkdir()
            (run/'workflow.json').write_text(json.dumps({'artifacts': {'pack': {}}}))
            with patch.object(installed.subprocess, 'run') as child:
                self.assertIsNone(installed.dispatch(['view', '--run', str(run)], skill_root=skill))
                child.assert_not_called()

    def test_bound_h_run_reuses_issued_store_even_after_default_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill, store, gid, _ = fixture(Path(tmp))
            run = Path(tmp)/'h-run'
            run.mkdir()
            (run/'workflow.json').write_text(json.dumps({'h_f2_binding': {'store': str(store), 'generation_id': gid}}))
            with patch.object(installed, 'default_store', side_effect=AssertionError('must use bound store')), patch.object(
                    installed, 'runtime_python', return_value=Path(sys.executable)), patch.object(installed.subprocess, 'run') as child:
                child.return_value.returncode = 0
                self.assertEqual(installed.dispatch(['resume', '--run', str(run)], skill_root=skill), 0)
                command = child.call_args.args[0]
                self.assertEqual(command[command.index('--runtime-store')+1], str(store))


if __name__ == '__main__':
    unittest.main()
