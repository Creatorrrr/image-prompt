"""Faithful Korean labels and bilingual V6 terms, not rendered-quality claims."""
from pathlib import Path
import copy
import hashlib
import json
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
EVIDENCE = ROOT / 'docs/research-evidence/photo-prompt/occupation-korean-label-data-cleanup-20261001'
sys.path.insert(0, str(ASSETS.parent / 'scripts'))
import prompt_generator as generator


class OccupationKoreanLabelDataCleanupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frozen = json.loads((EVIDENCE / 'frozen-inventory-queries.json').read_text())
        cls.acceptance = json.loads((EVIDENCE / 'acceptance-decisions.json').read_text())
        cls.data = generator.load_json(ASSETS / 'photo_prompt_tags.json')
        cls.rows = {row['id']: row for row in cls.data['slots']['subject']}

    def test_five_rows_and_twenty_bilingual_probes_are_frozen(self):
        self.assertEqual(hashlib.sha256((EVIDENCE / 'frozen-inventory-queries.json').read_bytes()).hexdigest(), '08b50359e9d7a3736e808744ccdad55b66775a3d022618c7524284cefabe24b3')
        self.assertEqual(len(self.frozen['inventory']), 5)
        self.assertEqual(len(self.frozen['queries']), 20)
        for language in ['en', 'ko']:
            for kind in ['positive', 'near_miss']:
                self.assertEqual(sum(q['language'] == language and q['kind'] == kind for q in self.frozen['queries']), 5)
        self.assertEqual(self.frozen['maximum_paid_calls'], 28)
        self.assertEqual(hashlib.sha256((EVIDENCE / 'acceptance-decisions.json').read_bytes()).hexdigest(), '4267bb658ae0a73777ee5e37b663407be51996cb65193fbf5cbcb4e6e76c501a')
        self.assertEqual(self.acceptance['accepted_ids'], ['harbor_fisherman'])

    def test_only_korean_labels_change(self):
        for row in self.frozen['inventory']:
            current = self.rows[row['id']]
            expected = row['proposed_after'] if row['id'] in self.acceptance['accepted_ids'] else row['before']
            self.assertEqual(current, expected)
            self.assertEqual({k: v for k, v in current.items() if k != 'ko'}, {k: v for k, v in row['before'].items() if k != 'ko'})
            self.assertEqual(row['before']['ko'], row['before']['en'])
            if row['id'] in self.acceptance['accepted_ids']:
                self.assertRegex(current['ko'], '[가-힣]')
            else:
                self.assertEqual(current['ko'], row['before']['ko'])

    def test_english_localization_and_semantic_description_remain_exact(self):
        for row in self.frozen['inventory']:
            current = self.rows[row['id']]
            self.assertEqual(generator.localize(current, 'en'), row['before']['en'])
            self.assertEqual(generator.semantic_description_for_entry(current), generator.semantic_description_for_entry(row['before']))
            expected = row['proposed_after'] if row['id'] in self.acceptance['accepted_ids'] else row['before']
            self.assertEqual(generator.localize(current, 'ko'), expected['ko'])

    def test_deferred_gear_and_hand_labels_are_exact_baseline(self):
        self.assertEqual(self.rows['welder_worker']['ko'], 'a welder worker in protective gear')
        self.assertEqual(self.rows['auto_mechanic']['ko'], 'an auto mechanic with grease-marked hands')

    def test_harbor_dawn_is_precise_and_other_two_labels_stay_baseline(self):
        self.assertEqual(self.rows['harbor_fisherman']['ko'], '동틀 무렵 항구에 있는 어부')
        self.assertEqual(self.rows['rice_paddy_farmer']['ko'], 'a rice paddy farmer working in wet soil')
        self.assertEqual(self.rows['blacksmith_forge_worker']['ko'], 'a blacksmith forge worker')

    def test_human_applicability_and_original_weights_stay_exact(self):
        for row in self.frozen['inventory']:
            current = self.rows[row['id']]
            self.assertEqual(current['for_any'], ['human'])
            self.assertEqual(current['weight'], row['before']['weight'])
            self.assertEqual(current['tags'], row['before']['tags'])
            self.assertFalse(re.search('남성|여성|노인|청년|소년|소녀', current['ko']))

    def test_intermediate_projection_adds_korean_terms_without_losing_baseline_terms(self):
        for row in self.frozen['inventory']:
            current, source = generator.candidate_pack_summarize_slot_candidate(self.data, 'subject', {'id': row['id']})
            expected = row['proposed_after'] if row['id'] in self.acceptance['accepted_ids'] else row['before']
            self.assertEqual(current['label_ko'], expected['ko'])
            before = copy.deepcopy(current)
            before['label_ko'] = row['before']['ko']
            generator.candidate_pack_project_candidate(before, salt=before['id'])
            generator.candidate_pack_project_candidate(current, salt=current['id'])
            old, new = set(before['concept_terms']), set(current['concept_terms'])
            self.assertLessEqual(old, new)
            if row['id'] in self.acceptance['accepted_ids']:
                self.assertTrue(new - old)
                self.assertTrue(all(re.search('[가-힣]', term) for term in new - old))
            else:
                self.assertEqual(new, old)
            self.assertLessEqual(len(new), 20)
            self.assertNotIn('label_ko', current)
            self.assertNotIn('label_en', current)
            self.assertEqual(current['content_form'], 'unordered_inspiration_terms')

    def test_korean_positives_do_not_copy_the_complete_new_label(self):
        labels = {row['id']: row['proposed_after']['ko'] for row in self.frozen['inventory']}
        for query in self.frozen['queries']:
            if query['kind'] == 'positive' and query['language'] == 'ko':
                self.assertNotEqual(query['query'], labels[query['target'].split(':')[-1]])


if __name__ == '__main__':
    unittest.main()
