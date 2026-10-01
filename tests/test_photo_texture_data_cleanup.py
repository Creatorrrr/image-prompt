"""Frozen texture DATA consistency, not final prompt or image-quality claims."""
from pathlib import Path
import copy
import gzip
import hashlib
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
EVIDENCE = ROOT / 'docs/research-evidence/photo-prompt/texture-data-cleanup-20261001'
sys.path.insert(0, str(ASSETS.parent / 'scripts'))
import prompt_generator as generator


class TextureDataCleanupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frozen = json.loads((EVIDENCE / 'frozen-inventory-queries.json').read_text())
        cls.data = generator.load_json(ASSETS / 'photo_prompt_tags.json')
        cls.rows = {row['id']: row for row in cls.data['slots']['texture']}

    def test_frozen_inventory_queries_and_call_bound_are_unchanged(self):
        self.assertEqual(hashlib.sha256((EVIDENCE / 'frozen-inventory-queries.json').read_bytes()).hexdigest(), '2416cae247494e971d48cb730dc003995ddb03d8c6c9e13ed34bd3135804f487')
        self.assertEqual(len(self.frozen['inventory']), 44)
        self.assertEqual(len(self.frozen['queries']), 27)
        self.assertEqual(sum(q['kind'] == 'positive' for q in self.frozen['queries']), 18)
        self.assertEqual(self.frozen['maximum_paid_calls'], 40)

    def test_all_thirty_five_keep_rows_are_preserved(self):
        kept = [r for r in self.frozen['inventory'] if r['decision'] == 'keep']
        self.assertEqual(len(kept), 35)
        for row in kept:
            self.assertEqual(self.rows[row['id']], row['before'], row['id'])

    def test_only_eight_alias_arrays_and_one_translation_are_changed(self):
        fixed = [r for r in self.frozen['inventory'] if r['decision'] == 'fix']
        self.assertEqual(len(fixed), 9)
        for row in fixed:
            current = self.rows[row['id']]
            self.assertEqual(current, row['proposed_after'])
            fields = {key for key in set(current) | set(row['before']) if current.get(key) != row['before'].get(key)}
            self.assertEqual(fields, {'en'} if row['id'] == 'glitter_dust' else {'aliases'})

    def test_compound_aliases_retain_legitimate_standalone_moire(self):
        expected = {
            'light_leak_burn': 'light-leak film burn',
            'ccd_purple_fringing': 'CCD purple fringing',
            'chromatic_aberration_edges': 'chromatic aberration',
            'moire_screen_pattern': 'screen moire pattern',
            'mold_stained_wall': 'mold-stained wall',
            'scratched_found_footage_grain': 'scratched found-footage grain',
            'peeling_paint_decay': 'peeling paint decay',
            'wet_concrete_grime': 'wet concrete grime',
        }
        for entry_id, alias in expected.items():
            self.assertIn(alias, self.rows[entry_id]['aliases'])
        self.assertIn('moire', self.rows['moire_screen_pattern']['aliases'])

    def test_broad_keywords_and_specialized_horror_meanings_remain(self):
        for row in self.frozen['inventory']:
            if row['decision'] != 'fix' or row['id'] == 'glitter_dust':
                continue
            current = self.rows[row['id']]
            for field in ['ko', 'en', 'embedding_text', 'keywords', 'tags', 'weight', 'facets', 'requires_any_tags']:
                self.assertEqual(current.get(field), row['before'].get(field), (row['id'], field))
        self.assertIn('horror', self.rows['mold_stained_wall']['tags'])
        self.assertIn('neglected liminal interior', self.rows['peeling_paint_decay']['embedding_text'])

    def test_glitter_restores_existing_lens_location_only(self):
        row = self.rows['glitter_dust']
        self.assertIn('렌즈 앞', row['ko'])
        self.assertEqual(row['en'], 'fine glitter dust in front of the lens catching the light')
        self.assertEqual(row['requires_any_tags'], ['cosplay', 'magical_girl', 'kpop'])
        self.assertNotIn('suspended', row['en'])

    def test_frozen_proposal_changes_only_nine_baseline_rows(self):
        baseline = json.loads(gzip.decompress((EVIDENCE / 'baseline-merged-data.json.gz').read_bytes()))
        self.assertEqual(generator.dictionary_hash(baseline), self.frozen['baseline_dictionary_hash'])
        expected = copy.deepcopy(baseline)
        for row in self.frozen['inventory']:
            rows = expected['slots'][row['slot']]
            index = next(i for i, entry in enumerate(rows) if entry['id'] == row['id'])
            self.assertEqual(rows[index], row['before'])
            rows[index] = row['proposed_after']
        changed = [(slot, before['id']) for slot, rows in baseline['slots'].items()
                   for before, after in zip(rows, expected['slots'][slot]) if before != after]
        self.assertEqual(changed, [('texture', row['id']) for row in self.frozen['inventory'] if row['decision'] == 'fix'])
        self.assertEqual({key: value for key, value in baseline.items() if key != 'slots'},
                         {key: value for key, value in expected.items() if key != 'slots'})


if __name__ == '__main__':
    unittest.main()
