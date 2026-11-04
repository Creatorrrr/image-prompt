"""Recovery evidence is not a replacement for the complete receipt audit.

Run with PHOTO_H_F2_TEST_NATIVE pointing at the staged sealed native directory
and the skill-owned embedding Python. No corpus search or model call is made.
"""
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

SKILL = Path(__file__).resolve().parents[1]
NATIVE = os.environ.get('PHOTO_H_F2_TEST_NATIVE')
if NATIVE:
    sys.path.insert(0, str(Path(NATIVE) / 'scripts'))
    sys.path.insert(0, str(SKILL / 'runtime-overlays/h-f2/scripts'))
    import photo_candidate_corpus as corpus
    import photo_h_f2_workflow as workflow
    import photo_h_f2_receipts as receipts


@unittest.skipUnless(NATIVE, 'requires sealed H-F2 code dependencies')
class RecoveryBoundary(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.query = {'slots': {'topic': {'text': 'fixed'}}}
        self.preflight = {'schema': 'test', 'run_id': 'one'}
        self.packet = {'generation_id': 'generation', 'query_set': self.query,
                       'sampling_seed': 42, 'sampling_policy': {'creativity': 3}, 'goals': {}}
        self.packet['canonical_sha256'] = corpus.digest(self.packet)
        self.journal = {'state': 'completed', 'generation_id': 'generation',
                        'query_set_sha256': corpus.digest(self.query),
                        'preflight_sha256': corpus.digest(self.preflight),
                        'sampling_seed': 42, 'sampling_policy': {'creativity': 3},
                        'material_sha256': self.packet['canonical_sha256']}
        self.save()

    def save(self):
        (self.root / 'material.json').write_text(json.dumps(self.packet))
        (self.root / 'transaction.json').write_text(json.dumps(self.journal))

    def load(self):
        return workflow.load_saved_material(self.root, 'generation', self.query, self.preflight)

    def test_completed_packet_is_reused_exactly(self):
        self.assertEqual(self.load(), self.packet)
        self.assertEqual(self.load()['sampling_seed'], 42)

    def test_reused_material_marks_progress_complete_even_after_composition(self):
        class Args:
            run = self.root
        with patch.object(workflow, '_retrieve', return_value={'status': 'pass', 'phase': 'composition_audited', 'reused': True}):
            result = workflow.retrieve(Args())
        progress = json.loads((self.root / '.staging/h-f2/progress.json').read_text())
        self.assertTrue(result['reused'])
        self.assertEqual((progress['stage'], progress['status']), ('complete', 'complete'))

    def test_partial_or_mixed_transaction_cannot_recover(self):
        for field, value, code in [('state', 'started', 'h_f2_partial_search_requires_reconciliation'),
                             ('generation_id', 'different', 'h_f2_recovery_transaction_binding_changed'),
                             ('query_set_sha256', 'bad', 'h_f2_recovery_transaction_binding_changed'),
                             ('preflight_sha256', 'bad', 'h_f2_recovery_transaction_binding_changed'),
                             ('sampling_seed', 43, 'h_f2_recovery_material_binding_changed'),
                             ('material_sha256', 'bad', 'h_f2_recovery_material_binding_changed')]:
            original = self.journal[field]
            self.journal[field] = value
            self.save()
            with self.subTest(field=field), self.assertRaises(ValueError) as error:
                self.load()
            self.assertEqual(error.exception.code, code)
            self.journal[field] = original

    def test_changed_packet_is_not_accepted_even_if_seed_is_preserved(self):
        self.packet['goals'] = {'injected': {}}
        self.save()
        with self.assertRaises(ValueError):
            self.load()

    def test_receipt_idempotence_still_reaudits_and_rejects_conflict(self):
        class Generation:
            id = 'generation'
            store = self.root
        packet = {'generation_id': 'generation', 'schema': 'historical',
                  'canonical_sha256': 'material', 'raw_files': {}}
        with patch.object(receipts, 'audit_packet') as audit:
            first = receipts.issue(Generation(), packet, self.root, {'pack': 1}, {'receipt': 1}, request_id='a' * 32)
            second = receipts.issue(Generation(), packet, self.root, {'pack': 1}, {'receipt': 1}, request_id='a' * 32)
            self.assertEqual(first, second)
            self.assertEqual(audit.call_count, 2)
            with self.assertRaises(ValueError):
                receipts.issue(Generation(), packet, self.root, {'pack': 2}, {'receipt': 1}, request_id='a' * 32)
            with self.assertRaises(ValueError):
                receipts.issue(Generation(), packet, self.root, {'pack': 1}, {'receipt': 1}, request_id='../foreign')


if __name__ == '__main__':
    unittest.main()
