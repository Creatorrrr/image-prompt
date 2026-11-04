import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import photo_candidate_retrieval_views as views
import photo_prepare_reviewed_views as prepare


class PrepareReviewedViews(unittest.TestCase):
    def setUp(self):
        self.record = {'id': 'cand_a', 'record_kind': 'visual_option',
                       'content': {'en': 'A blue coat.', 'ko': '파란 코트.'}, 'effects': {}}
        self.records = {'cand_a': self.record}
        self.whole = self.row('whole', 'whole')
        self.context = self.row('context', 'context')
        self.baseline = {'schema': views.SCHEMA, 'recipe': views.RECIPE,
                         'views': [self.whole, self.context]}

    def row(self, key, kind):
        return {'id': views.view_id('cand_a', 'base', key), 'candidate_id': 'cand_a',
                'realization_id': 'base', 'key': key, 'kind': kind,
                'source_record_sha256': views.digest(self.record), 'text_en': 'A blue coat.',
                'text_ko': '파란 코트.', 'source_quotes': [{'pointer': '/content/en', 'quote': 'A blue coat.'}]}

    def test_restores_reviewed_context_when_generator_omits_it(self):
        generated = {**self.baseline, 'views': [self.whole]}
        result, count = prepare.merge_reviewed(generated, self.baseline, self.records)
        self.assertEqual(count, 1)
        self.assertEqual(result['views'], self.baseline['views'])
        self.assertEqual(len(generated['views']), 1)

    def test_rejects_conflicting_view_and_stale_candidate(self):
        changed = copy.deepcopy(self.context); changed['text_en'] = 'A red coat.'
        with self.assertRaisesRegex(ValueError, 'conflicts'):
            prepare.merge_reviewed({**self.baseline, 'views': [self.whole, changed]}, self.baseline, self.records)
        altered = copy.deepcopy(self.record); altered['content']['en'] = 'A different coat.'
        with self.assertRaisesRegex(ValueError, 'stale'):
            prepare.merge_reviewed(self.baseline, self.baseline, {'cand_a': altered})

    def test_rejects_a_view_whose_quote_is_not_in_current_candidate(self):
        altered = copy.deepcopy(self.context)
        altered['source_quotes'][0]['quote'] = 'A red coat.'
        with self.assertRaises(ValueError):
            prepare.merge_reviewed({**self.baseline, 'views': [self.whole, altered]},
                                   {**self.baseline, 'views': [self.whole, altered]}, self.records)


if __name__ == '__main__':
    unittest.main()
