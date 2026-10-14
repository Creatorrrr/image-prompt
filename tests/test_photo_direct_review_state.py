"""A fully read but unresolved candidate must remain unfinished."""
import importlib.util
from pathlib import Path
import subprocess
import json
import tempfile
import unittest
from unittest.mock import patch

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
    def test_execution_accounting_preserves_unknown_after_start_or_failure(self):
        from local_execution_ledger import Ledger
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch.object(integrator.review, 'HERE', root):
                self.assertEqual(integrator.local_execution_counts()['exact_total'], 0)
                (root/'LOCAL-INFERENCE-LEDGERS.json').write_text(json.dumps({'directories': ['inverse/ledger']}))
                ledger = Ledger(root/'inverse/ledger')
                ledger.plan('fixture', ['explicit fixture input'], binding={},
                            space={'provider': 'embeddinggemma2-local'})
                self.assertEqual(integrator.local_execution_counts()['exact_total'], 0)
                ledger.start('fixture')
                result = integrator.local_execution_counts()
                self.assertIsNone(result['exact_total'])
                self.assertEqual(result['unknown_run_ids'], ['inverse/ledger/fixture'])
                ledger.finish('fixture', state='failed', receipts=[], error_type='FixtureFailure')
                self.assertIsNone(integrator.local_execution_counts()['exact_total'])
                (root/'LOCAL-INFERENCE-LEDGERS.json').write_text(json.dumps({'directories': ['../outside']}))
                with self.assertRaisesRegex(ValueError, 'inside this evidence run'):
                    integrator.local_execution_counts()

    def test_shared_tracked_packet_and_new_batch_have_an_exact_commit_boundary(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            def git(*args):
                return subprocess.check_output(['git', *args], cwd=root, stderr=subprocess.DEVNULL)
            git('init'); git('config', 'user.name', 'Fixture'); git('config', 'user.email', 'fixture@example.test')
            (root/'packet.json').write_text('immutable packet')
            git('add', 'packet.json'); git('commit', '-m', 'fixture')
            (root/'batch.json').write_text('new literal source decisions')
            with patch.object(integrator.review, 'ROOT', root):
                integrator.stage_selected(['packet.json', 'batch.json'])
                self.assertEqual(git('diff', '--cached', '--name-only').decode().strip(), 'batch.json')
                (root/'unrelated.txt').write_text('protected work'); git('add', 'unrelated.txt')
                with self.assertRaisesRegex(ValueError, 'explicitly selected'):
                    integrator.stage_selected(['packet.json', 'batch.json'])

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
