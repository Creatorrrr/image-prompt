"""Precise color/lighting owners without changing their complete visible meaning."""
from pathlib import Path
import hashlib
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
EVIDENCE = ROOT / 'docs/research-evidence/photo-prompt/lighting-color-owner-data-cleanup-20261001'
sys.path.insert(0, str(ASSETS.parent / 'scripts'))
import prompt_generator as generator
import photo_candidate_semantics as semantics


class LightingColorOwnerDataCleanupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frozen = json.loads((EVIDENCE / 'frozen-inventory-queries.json').read_text())
        cls.data = generator.load_json(ASSETS / 'photo_prompt_tags.json')
        cls.rows = {(slot, row['id']): row for slot, rows in cls.data['slots'].items() for row in rows}

    def test_inventory_and_queries_are_frozen(self):
        self.assertEqual(hashlib.sha256((EVIDENCE / 'frozen-inventory-queries.json').read_bytes()).hexdigest(), '7ab5d852803537a280a06f3c8d945ca29d47afa7d51bb3586210480d9e7731bc')
        self.assertEqual(len(self.frozen['inventory']), 40)
        self.assertEqual(len(self.frozen['queries']), 14)
        self.assertEqual(sum(q['kind'] == 'positive' for q in self.frozen['queries']), 7)
        self.assertEqual(self.frozen['maximum_paid_calls'], 20)

    def test_thirty_five_kept_rows_remain_exact(self):
        rows = [r for r in self.frozen['inventory'] if r['decision'] == 'keep']
        self.assertEqual(len(rows), 35)
        for row in rows:
            self.assertEqual(self.rows[row['slot'], row['id']], row['before'], row['id'])

    def test_five_proposals_change_only_relation_objects(self):
        rows = [r for r in self.frozen['inventory'] if r['decision'] == 'fix']
        self.assertEqual(len(rows), 5)
        for row in rows:
            current = self.rows[row['slot'], row['id']]
            self.assertEqual(current, row['proposed_after'], row['id'])
            self.assertEqual({k: v for k, v in current.items() if k != 'relations'}, {k: v for k, v in row['before'].items() if k != 'relations'})
            self.assertEqual(len(current['relations']), 1)
            self.assertEqual({k: v for k, v in current['relations'][0].items() if k != 'object'}, {k: v for k, v in row['before']['relations'][0].items() if k != 'object'})

    def test_split_tone_owners_are_brightness_regions(self):
        warm = self.rows['color_grading', 'pe_warm_highlight_cool_shadow']
        teal = self.rows['color_grading', 'pe_teal_shadow_orange_midtones']
        self.assertEqual(warm['relations'][0]['object'], 'image_plane_highlight_and_shadow_tones')
        self.assertEqual(teal['relations'][0]['object'], 'image_plane_shadow_and_selected_midtone_regions')
        self.assertEqual(warm['concept_units'], ['bright tonal regions carry a warm tint', 'shadow tonal regions carry a cool tint'])
        self.assertIn('selected midtones carry a restrained orange tint', teal['concept_units'])

    def test_red_splash_owner_preserves_colored_object_and_achromatic_remainder(self):
        row = self.rows['color_grading', 'pe_red_object_splash']
        self.assertEqual(row['relations'][0]['object'], 'selected_red_object_and_achromatic_picture_remainder')
        self.assertEqual(row['concept_units'], ['one declared red object retains its red color', 'the rest of the picture is achromatic'])

    def test_cheek_triangle_is_local_beneath_its_eye(self):
        row = self.rows['lighting', 'pe_cheek_triangle']
        self.assertEqual(row['relations'][0]['object'], 'shadow_side_cheek_beneath_its_eye')
        self.assertEqual(row['concept_units'], ['one cheek is predominantly shadowed', 'a small bounded light triangle remains beneath its eye'])

    def test_silhouette_includes_dark_interior_outline_and_bright_background(self):
        row = self.rows['lighting', 'pe_silhouette_outline']
        self.assertEqual(row['relations'][0]['object'], 'dark_subject_interior_and_outline_against_bright_background')
        self.assertEqual(row['concept_units'], ['subject interior is predominantly dark', 'subject outline is legible against the brighter background'])

    def test_projection_and_declared_effects_remain_exact(self):
        for row in self.frozen['inventory']:
            current = self.rows[row['slot'], row['id']]
            projected = semantics.semantic_source(current, row['slot'], self.data['candidate_semantic_policy'])
            self.assertEqual(projected['relations'], current['relations'])
            for field in ['concept_units', 'affected_dimensions', 'affected_properties', 'aliases', 'keywords', 'weight', 'requires_any_tags']:
                self.assertEqual(current.get(field), row['before'].get(field), (row['id'], field))

    def test_compatible_operator_bounce_and_historical_provenance_are_preserved(self):
        self.assertEqual(self.rows['color_grading', 'pe_s_shaped_separation']['relations'][0]['object'], 'input_to_output_tone')
        self.assertEqual(self.rows['lighting', 'pe_ceiling_bounce']['relations'][0]['object'], 'source_subject_surface')
        record = ROOT / 'docs/research-evidence/photo-prompt/extension-maintenance/photo-editing-effects-20261001-v2.json'
        self.assertEqual(hashlib.sha256(record.read_bytes()).hexdigest(), 'f6c9e6f18f2932b09520f66a73d1dba83afb4e1e34501f88ea9472092f9ecf27')
        self.assertNotIn('authored_source_sha256', json.loads(record.read_text()))


if __name__ == '__main__':
    unittest.main()
