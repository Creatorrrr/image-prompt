"""Execute the exact original V32 assertions in their sealed V32 source tree."""
from __future__ import annotations

import os
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tests import photo_prompt_fixtures as fixtures

ROOT = Path(__file__).resolve().parents[1]


class RobeSourceBoundaryHistoryTests(unittest.TestCase):
    def test_original_v32_assertions_replay_from_authenticated_source(self):
        with tempfile.TemporaryDirectory(prefix='photo-v32-original-tests-') as temporary:
            tree = Path(temporary).resolve() / 'tree'
            python = fixtures.v32_history_python(source_root=ROOT)
            expected_environment = fixtures._v32_transition(ROOT)[0]['runtime_environment']
            probe = "import json,sys,unicodedata; print(json.dumps({'implementation':sys.implementation.name,'python':list(sys.version_info[:3]),'unicode':unicodedata.unidata_version}))"
            actual_environment = json.loads(subprocess.check_output([str(python), '-c', probe], text=True))
            self.assertEqual(expected_environment, actual_environment)
            selection = ROOT / fixtures.V33_SCOPE_PROOF.parent / 'V32-PYTHON-ENVIRONMENT.json'
            selection.write_text(json.dumps({
                'schema': 'photo-v32-history-python-selection/v1', 'python': str(python),
                'original_proof_sha256': fixtures.V32_ROBE_PROOF_SHA256,
                'required_environment': expected_environment, 'actual_environment': actual_environment,
                'reason': 'Exact equality to the unchanged original V32 proof environment.',
            }, ensure_ascii=False, indent=2) + '\n')
            manifest = fixtures.materialize_v32_parent_source(tree, source_root=ROOT)
            record = next(row for row in manifest['members']
                          if row['path'] == 'tests/test_photo_robe_source_boundary_history.py')
            self.assertEqual(fixtures._v24_verified_payload(ROOT, record),
                             (tree / record['path']).read_bytes())
            (tree / '.venv').symlink_to(python.parent.parent, target_is_directory=True)
            environment = os.environ.copy()
            environment['PHOTO_RUNTIME_STORE'] = str(Path(temporary).resolve() / 'runtime-store')
            environment['GEMINI_API_KEY'] = ''
            environment['GOOGLE_API_KEY'] = ''
            # Original generation keeps its unchanged 60-second request budget.
            # Publish its original source snapshot before executing the replay.
            setup = "import sys; sys.path.insert(0,'skills/photo-prompt-image-generator/scripts'); from photo_runtime_sources import SnapshotPublisher; SnapshotPublisher().publish()"
            prepared = subprocess.run([str(python), '-c', setup], cwd=tree, env=environment,
                                      capture_output=True, text=True, timeout=300)
            self.assertEqual(0, prepared.returncode, prepared.stderr or prepared.stdout)
            completed = subprocess.run(
                [str(python), '-m', 'unittest', 'tests.test_photo_robe_source_boundary_history', '-v'],
                cwd=tree, env=environment, capture_output=True, text=True, timeout=900)
            evidence = ROOT / fixtures.V33_SCOPE_PROOF.parent / 'V32-ORIGINAL-TESTS.log'
            evidence.write_text(completed.stdout + completed.stderr)
            self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)


if __name__ == '__main__':
    unittest.main()
