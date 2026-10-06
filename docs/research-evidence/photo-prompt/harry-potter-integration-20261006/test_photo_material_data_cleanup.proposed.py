"""Material source/projection invariants, not claims about rendered quality."""
from pathlib import Path
import hashlib
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
EVIDENCE = ROOT / 'docs/research-evidence/photo-prompt/material-data-cleanup-20261001'
sys.path.insert(0, str(ASSETS.parent / 'scripts'))
import prompt_generator as generator
import photo_candidate_semantics as semantics


class MaterialDataCleanupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frozen = json.loads((EVIDENCE / 'frozen-inventory-queries.json').read_text())
        cls.acceptance = json.loads((EVIDENCE / 'acceptance-decisions.json').read_text())
        cls.data = generator.load_json(ASSETS / 'photo_prompt_tags.json')
        cls.rows = {(slot, row['id']): row for slot, rows in cls.data['slots'].items() for row in rows}

    def test_inventory_and_queries_are_frozen(self):
        self.assertEqual(hashlib.sha256((EVIDENCE / 'frozen-inventory-queries.json').read_bytes()).hexdigest(), '7d58b34779ce9df0cc4ed2c9260d5f45b2b9488218a893d1b6ef9491d4908768')
        self.assertEqual(len(self.frozen['inventory']), 32)
        self.assertEqual(len(self.frozen['queries']), 26)
        self.assertEqual(sum(q['kind'] == 'positive' for q in self.frozen['queries']), 13)
        self.assertEqual(sum(q['language'] == 'ko' for q in self.frozen['queries']), 2)
        self.assertEqual(self.frozen['maximum_paid_calls'], 44)
        self.assertEqual(hashlib.sha256((EVIDENCE / 'acceptance-decisions.json').read_bytes()).hexdigest(), 'e01dec1ff3efdfa116dd34a3e3499d04e1277800df972c39561bbb48f40d5834')

    def test_twenty_three_retained_rows_preserve_specialization_and_construction(self):
        kept = [r for r in self.frozen['inventory'] if r['decision'] == 'keep' or r['id'] in self.acceptance['reverted_to_baseline']]
        self.assertEqual(len(kept), 23)
        for row in kept:
            expected = dict(row['before'])
            if row['id'] == 'sheer_organza_chiffon_transmission':
                # The 2026-10-06 appearance integration adds two reviewed
                # equivalent search expressions. Keep every original field
                # exact, and permit only these explicit additive paraphrases.
                expected['paraphrases'] = list(dict.fromkeys([
                    *expected.get('paraphrases', []),
                    'light passes through fine organza or chiffon with readable fabric threads and edges',
                    '천의 실 조직과 가장자리가 읽히는 얇은 오간자나 시폰으로 빛이 비친다',
                ]))
            self.assertEqual(self.rows[row['slot'], row['id']], expected, row['id'])

    def test_only_nine_accepted_fields_change(self):
        fixed = [r for r in self.frozen['inventory'] if r['decision'] == 'fix' and r['id'] not in self.acceptance['reverted_to_baseline']]
        self.assertEqual(len(fixed), 9)
        fields = []
        for row in fixed:
            current = self.rows[row['slot'], row['id']]
            self.assertEqual(current, row['proposed_after'], row['id'])
            changed = {k for k in current.keys() | row['before'].keys() if current.get(k) != row['before'].get(k)}
            self.assertEqual(len(changed), 1)
            fields.extend(changed)
        self.assertEqual(sorted(fields), sorted(['aliases'] * 6 + ['ko'] + ['relations'] * 2))

    def test_material_nouns_and_valid_plinth_terms_remain(self):
        nouns = {'matte_concrete_surface': 'concrete', 'brushed_steel_surface': 'steel', 'linen_fabric_surface': 'linen', 'dark_walnut_table': 'walnut', 'translucent_glass_block': 'glass', 'paper_seamless_backdrop': 'paper', 'wrinkled_bedsheet': 'bedsheet', 'black_acrylic_reflection': 'acrylic'}
        for entry_id, noun in nouns.items():
            self.assertIn(noun, self.rows['surface_material', entry_id]['aliases'])
        self.assertEqual(self.rows['surface_material', 'acrylic_plinth']['aliases'], ['acrylic', 'plinth'])

    def test_crochet_translation_does_not_add_open_weave_or_change_english(self):
        current = self.rows['texture', 'crochet_loop_texture']
        self.assertEqual(current['ko'], '코바늘뜨기의 고리 짜임 질감')
        self.assertEqual(current['en'], 'crochet loop texture')
        self.assertEqual(current['embedding_text'], 'crochet loop texture')
        original = next(r['before'] for r in self.frozen['inventory'] if r['id'] == 'crochet_loop_texture')
        self.assertEqual({k: v for k, v in current.items() if k != 'ko'}, {k: v for k, v in original.items() if k != 'ko'})

    def test_noise_owner_retains_dark_wall_tone_localization(self):
        row = self.rows['grain_profile', 'rb_low_light_noise_candidate']
        self.assertEqual(row['relations'][0]['object'], 'image_plane_darker_neutral_wall_tones')
        self.assertIn('darker neutral wall tones contain fine random luminance variation', row['concept_units'])
        self.assertIn('darker wall tones', row['en'])
        self.assertIn('the main object edges remain readable', row['concept_units'])

    def test_film_grain_owner_is_the_displayed_photograph(self):
        row = self.rows['film_emulation', 'rb_film_grain_choice_candidate']
        self.assertEqual(row['relations'][0]['object'], 'displayed_photograph_image_plane')
        self.assertEqual(row['relations'][0]['subject'], '표시된 사진 전체의 미세 질감')
        self.assertIn('scene edges and material differences stay readable', row['concept_units'])

    def test_owner_projection_and_all_other_semantics_are_preserved(self):
        for row in self.frozen['inventory']:
            if row['decision'] != 'fix':
                continue
            current = self.rows[row['slot'], row['id']]
            for field in ['keywords', 'tags', 'weight', 'requires_any_tags', 'for_any', 'facets', 'affected_dimensions', 'affected_properties']:
                self.assertEqual(current.get(field), row['before'].get(field), (row['id'], field))
            if current.get('relations'):
                projected = semantics.semantic_source(current, row['slot'], self.data['candidate_semantic_policy'])
                self.assertEqual(projected['relations'], current['relations'])


if __name__ == '__main__':
    unittest.main()
