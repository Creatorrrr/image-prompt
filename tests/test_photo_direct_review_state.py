"""A fully read but unresolved candidate must remain unfinished."""
import importlib.util
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parents[1] / 'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
spec = importlib.util.spec_from_file_location('direct_review_state', HERE / 'review_state.py')
state = importlib.util.module_from_spec(spec)
spec.loader.exec_module(state)
import sys
sys.path.insert(0, str(HERE))
spec = importlib.util.spec_from_file_location('direct_review_integrator', HERE / 'integrate_ready_batch.py')
integrator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(integrator)


class ReviewStateTests(unittest.TestCase):
    def test_structured_proposals_are_not_reported_as_text_corrections(self):
        rows = [{'corrections': [
            {'before': 'old', 'after': 'new'}, {'before': None, 'after': {'standing': {}}}]},
            {'corrections': [{'before': {}, 'after': {'dimensions': ['pose']}}]},
            {'corrections': []}]
        self.assertEqual(state.correction_counts(rows), {
            'text_records': 1, 'text_fields': 1, 'structured_records': 2, 'structured_values': 2})

    def test_pending_and_diagnostic_have_distinct_completion_meanings(self):
        rows = [{'candidate_id': cid, 'status': status} for cid, status in
                [('a', 'approved'), ('b', 'needs_boundary_review'), ('d', 'diagnostic_reviewed')]]
        result = state.coverage(['a', 'b', 'c', 'd'], rows)
        self.assertEqual(result['registered_source_judgements'], 3)
        self.assertEqual(result['accepted_source_judgements'], 2)
        self.assertEqual(result['pending_source_judgements'], 1)
        self.assertEqual(result['unreviewed_source_records'], 1)
        self.assertEqual(result['first_unreviewed_order_offset'], 2)
        self.assertEqual(result['first_unfinished_order_offset'], 1)
        self.assertFalse(result['source_review_approval_complete'])

    def test_all_read_is_not_all_approved(self):
        result = state.coverage(['a'], [{'candidate_id': 'a', 'status': 'needs_source_fix'}])
        self.assertEqual(result['first_unreviewed_order_offset'], 1)
        self.assertEqual(result['first_unfinished_order_offset'], 0)
        self.assertFalse(result['source_review_approval_complete'])

    def test_duplicate_foreign_and_unknown_status_are_rejected(self):
        a = {'candidate_id': 'a', 'status': 'approved'}
        for rows in [[a, a], [{'candidate_id': 'x', 'status': 'approved'}],
                     [{'candidate_id': 'a', 'status': 'ready'}]]:
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                state.coverage(['a'], rows)

    def test_pending_batch_requires_explicit_checkpoint_and_exact_worker_attestation(self):
        rows = {'decisions': [{'candidate_id': 'b', 'status': 'needs_boundary_review'},
                              {'candidate_id': 'a', 'status': 'approved'}]}
        note = {'start': 0, 'stop': 2, 'unresolved_ordinals': [1]}
        with self.assertRaisesRegex(ValueError, 'explicit checkpoint'):
            integrator.validate_selected_batch(note, rows, ['a', 'b'])
        self.assertEqual(integrator.validate_selected_batch(note, rows, ['a', 'b'],
                         source_read_checkpoint=True), [1])
        with self.assertRaisesRegex(ValueError, 'attestation differs'):
            integrator.validate_selected_batch({**note, 'unresolved_ordinals': []}, rows,
                                              ['a', 'b'], source_read_checkpoint=True)

    def test_checkpoint_cannot_approve_missing_foreign_or_duplicate_ids(self):
        note = {'start': 0, 'stop': 2, 'unresolved_ordinals': []}
        for ids in [['a'], ['a', 'a'], ['a', 'x']]:
            rows = {'decisions': [{'candidate_id': cid, 'status': 'approved'} for cid in ids]}
            with self.subTest(ids=ids), self.assertRaisesRegex(ValueError, 'exact canonical range'):
                integrator.validate_selected_batch(note, rows, ['a', 'b'], source_read_checkpoint=True)


if __name__ == '__main__':
    unittest.main()
