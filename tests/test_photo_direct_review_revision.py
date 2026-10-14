"""A root rereview replaces one judgement without changing source identity."""
import copy
import importlib.util
from pathlib import Path
import sys
import unittest

from tests.test_photo_direct_review import decision, fixture, A, B

HERE = Path(__file__).resolve().parents[1] / 'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
sys.path.insert(0, str(HERE))
spec = importlib.util.spec_from_file_location('direct_review_revision', HERE / 'revise_registered.py')
revision = importlib.util.module_from_spec(spec)
spec.loader.exec_module(revision)


class RootRevisionTests(unittest.TestCase):
    def test_replacement_preserves_bindings_and_removes_worker_attribution(self):
        data = fixture();old = decision(data)
        old.update(schema=revision.review.DELEGATED_SCHEMA,
                   review_method='codex_subagent_direct_source_read', review_provenance={'old': True})
        authored = {key: copy.deepcopy(old[key]) for key in revision.AUTHORED_FIELDS}
        authored['meaning_summary'] = 'Root explicitly reread this entire fixture source.'
        result = revision.replace_row(old, authored, HERE / 'authored/root-test.json', 1, data)
        self.assertNotIn('review_provenance', result)
        self.assertEqual(result['review_method'], 'codex_direct_source_read')
        for key in ['candidate_id', 'packet_sha256', 'source_record_sha256',
                    'catalog_sha256', 'reference_sha256']:
            self.assertEqual(result[key], old[key])
        self.assertEqual(result['authored_decision']['sha256'], revision.review.c.digest(authored))
        self.assertIn('review_provenance', old)

    def test_foreign_candidate_and_invented_quote_cannot_be_rebound(self):
        for defect in ['foreign_id', 'invented_quote']:
            data = fixture();old = decision(data)
            authored = {key: copy.deepcopy(old[key]) for key in revision.AUTHORED_FIELDS}
            if defect == 'foreign_id':
                authored['candidate_id'] = B
            else:
                authored['roles'][0]['evidence'][0]['quote'] = 'invented silk'
            with self.subTest(defect=defect), self.assertRaises(ValueError):
                revision.replace_row(old, authored, HERE / 'authored/root-test.json', 1, data)


if __name__ == '__main__':
    unittest.main()
