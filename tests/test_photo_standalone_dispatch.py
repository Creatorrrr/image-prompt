import importlib.util
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/photo-prompt-image-generator/scripts'
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location('standalone_entry', SCRIPTS / 'generate_photo_prompt.py')
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)


class StandaloneDispatchTest(unittest.TestCase):
    args = ['--request-envelope-json', 'request.json', '--authorial-core-json', 'core.json',
            '--creative-controls-json', 'controls.json', '--embodiment-review-json', 'review.json',
            '--slot-expression-plan-json', 'plan.json', '--output-directory', 'output']

    def test_requires_explicit_authored_plan(self):
        args = self.args[:8] + self.args[10:]
        with patch.object(entry.installed, 'release') as release, self.assertRaises(SystemExit):
            entry.main(args)
        release.assert_not_called()

    def test_dispatches_verified_installed_generation(self):
        config = {'schema': entry.installed.SCHEMA, 'policy': 'photo-h-f2/v1',
                  'store_subdirectory': 'h-f2-installed', 'generation_id': 'h-id',
                  'native_generation_id': 'n-id', 'code_sha256': 'expected'}
        manifest = {'native_generation_id': 'n-id'}
        native_manifest = {'source': {'code': {}}}
        with patch.object(entry.installed, 'read', return_value=config), \
             patch.object(entry.installed, 'default_store', return_value=Path('/tmp/example')), \
             patch.object(entry.installed, 'release', return_value=(Path('/tmp/native'), manifest, native_manifest)) as release, \
             patch.object(entry.installed, 'digest', return_value='expected'), \
             patch.object(entry.installed, 'runtime_python', return_value=Path('/tmp/python')), \
             patch.object(entry.subprocess, 'run') as run:
            run.return_value.returncode = 0
            self.assertEqual(entry.main(self.args), 0)
        self.assertTrue(release.call_args.kwargs['full'])
        command = run.call_args.args[0]
        self.assertIn('h-id', command)
        self.assertIn('photo_h_f2_standalone.py', ' '.join(command))
        self.assertNotIn('PYTHONPATH', run.call_args.kwargs['env'])

    def test_rejects_mismatched_installed_native_generation(self):
        config = {'schema': entry.installed.SCHEMA, 'policy': 'photo-h-f2/v1',
                  'store_subdirectory': 'h-f2-installed', 'generation_id': 'h-id',
                  'native_generation_id': 'n-id', 'code_sha256': 'expected'}
        with patch.object(entry.installed, 'read', return_value=config), \
             patch.object(entry.installed, 'default_store', return_value=Path('/tmp/example')), \
             patch.object(entry.installed, 'release', return_value=(Path('/tmp/native'),
                 {'native_generation_id': 'other'}, {'source': {'code': {}}})), \
             patch.object(entry.subprocess, 'run') as run:
            with self.assertRaises(ValueError):
                entry.main(self.args)
            run.assert_not_called()


if __name__ == '__main__':
    unittest.main()
