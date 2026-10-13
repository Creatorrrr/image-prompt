import unittest
from tests.test_photo_global_retrieval import GlobalDiscoveryTests
from tests.photo_slot_oracle import full_scan
import photo_global_index as index
import photo_shared_views as views


class SlotOracleTests(unittest.TestCase):
    def test_full_scan_has_one_vote_per_candidate_and_retains_untagged(self):
        data = GlobalDiscoveryTests().data()
        ids = sorted(data['candidates'])
        result = full_scan(index.lexical(views.source(data)), data['_global_index']['entries'],
                           {'slot_focus': 'left edge light'}, [1.0] + [0.0] * 767, ids)
        self.assertEqual(len(result['embedding']), 3)
        self.assertEqual(len({r['document_id'] for r in result['rrf']}), len(result['rrf']))
        self.assertIn('cand_' + 'b' * 32, {r['document_id'] for r in result['embedding']})

    def test_ties_use_identity_and_threshold_excludes_negative(self):
        data = GlobalDiscoveryTests().data()
        entries = data['_global_index']['entries']
        entries['cand_' + 'c' * 32]['vector'] = [-1.0] + [0.0] * 767
        result = full_scan(index.lexical(views.source(data)), entries, {'slot_focus': ''},
                           [1.0] + [0.0] * 767, entries)
        self.assertEqual([r['document_id'] for r in result['embedding']],
                         ['cand_' + 'a' * 32, 'cand_' + 'b' * 32])
