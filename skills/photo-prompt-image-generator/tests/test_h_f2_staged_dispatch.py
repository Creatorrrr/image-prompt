"""A partially retrieved run stays bound to its original sealed generation."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import photo_installed_h_f2 as dispatch


class StagedDispatch(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.run = Path(self.tmp.name)
        self.state = {'run_id': 'one', 'phase': 'slot_intents_authored', 'artifacts': {}}
        self.path = self.run / '.staging/h-f2/preflight.json'
        self.path.parent.mkdir(parents=True)

    def save(self, **changes):
        value = {'schema': 'photo-h-f2-preflight/v1', 'run_id': 'one', 'generation_id': 'a' * 64}
        value.update(changes)
        self.path.write_text(json.dumps(value))

    def test_missing_preflight_uses_default(self):
        self.assertIsNone(dispatch.staged_generation(self.run, self.state))

    def test_unbound_interrupted_run_uses_original_generation(self):
        self.save()
        self.assertEqual(dispatch.staged_generation(self.run, self.state), 'a' * 64)
        self.assertIsNone(dispatch.staged_generation(self.run, {**self.state, 'h_f2_binding': {'generation_id': 'b' * 64}}))

    def test_wrong_run_or_invalid_generation_fails_closed(self):
        for changed in ({'run_id': 'other'}, {'generation_id': '../escape'}, {'generation_id': None}):
            self.save(**changed)
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                dispatch.staged_generation(self.run, self.state)


if __name__ == '__main__':
    unittest.main()
