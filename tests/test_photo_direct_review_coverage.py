"""Parallel source review counts must not hide holes in candidate coverage."""
import importlib.util
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parents[1] / 'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
sys.path.insert(0, str(HERE))
spec = importlib.util.spec_from_file_location('direct_review_summary', HERE / 'summarize_batch.py')
summary = importlib.util.module_from_spec(spec)
spec.loader.exec_module(summary)


class ParallelCoverageTests(unittest.TestCase):
    def test_prefix_and_sparse_ranges_keep_the_actual_first_hole(self):
        order = ['a', 'b', 'c', 'd', 'e']
        self.assertEqual(summary.validate_coverage(order, {'a', 'b'}, 0, 2, 2), 2)
        self.assertEqual(summary.validate_coverage(order, {'a', 'd', 'e'}, 3, 5, 3,
                                                  allow_sparse=True), 1)

    def test_sparse_coverage_does_not_claim_a_complete_prefix_by_default(self):
        with self.assertRaisesRegex(ValueError, 'explicitly reviewed order'):
            summary.validate_coverage(['a', 'b', 'c'], {'a', 'c'}, 2, 3, 2)

    def test_management_batch_cannot_include_an_unreviewed_candidate(self):
        with self.assertRaisesRegex(ValueError, 'unreviewed IDs'):
            summary.validate_coverage(['a', 'b', 'c'], {'a', 'c'}, 1, 3, 2, allow_sparse=True)

    def test_coverage_count_and_foreign_ids_are_rejected(self):
        for rows, count in [({'a', 'c'}, 3), ({'a', 'outside'}, 2)]:
            with self.assertRaisesRegex(ValueError, 'coverage count or canonical IDs'):
                summary.validate_coverage(['a', 'b', 'c'], rows, 0, 1, count, allow_sparse=True)


if __name__ == '__main__':
    unittest.main()
