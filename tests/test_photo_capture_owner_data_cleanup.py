"""Frozen capture DATA consistency; retrieval exposure is not final adoption."""
from pathlib import Path
import hashlib
import json
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
EVIDENCE = ROOT / 'docs/research-evidence/photo-prompt/capture-owner-data-cleanup-20261001'
sys.path.insert(0, str(ASSETS.parent / 'scripts'))
import prompt_generator as generator
import photo_candidate_semantics as semantics


class CaptureOwnerDataCleanupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frozen = json.loads((EVIDENCE / 'frozen-inventory-queries.json').read_text())
        cls.acceptance = json.loads((EVIDENCE / 'acceptance-decisions.json').read_text())
        # This oracle freezes the 20261001 ownership revision. Exclude only
        # the later additive motion paraphrase overlay; its current merged
        # data and activation contracts are tested independently.
        filenames = tuple(name for name in generator.RESEARCH_EXTENSION_FILENAMES
                          if name != 'photo_prompt_motion_graphics_extension.json')
        with patch.object(generator, 'RESEARCH_EXTENSION_FILENAMES', filenames):
            cls.data = generator.load_json(ASSETS / 'photo_prompt_tags.json')
        cls.rows = {(slot, row['id']): row for slot, rows in cls.data['slots'].items() for row in rows}

    def test_inventory_queries_and_bound_are_frozen(self):
        self.assertEqual(hashlib.sha256((EVIDENCE / 'frozen-inventory-queries.json').read_bytes()).hexdigest(), '560abefc7e8013b51ff2db5355758c3c59cb3bd318e1b13a9261bab14828af98')
        self.assertEqual(len(self.frozen['inventory']), 54)
        self.assertEqual(len(self.frozen['queries']), 32)
        self.assertEqual(sum(q['kind'] == 'positive' for q in self.frozen['queries']), 16)
        self.assertEqual(self.frozen['maximum_paid_calls'], 56)
        self.assertEqual(hashlib.sha256((EVIDENCE / 'acceptance-decisions.json').read_bytes()).hexdigest(), 'f783ef48380c0d1a1207e35c2ed4a2bfb0aba305583d8d1fb3af71b9e77e10ca')

    def test_all_forty_one_retained_rows_remain_identical(self):
        kept = [r for r in self.frozen['inventory'] if r['decision'] == 'keep' or r['id'] in self.acceptance['reverted_to_baseline']]
        self.assertEqual(len(kept), 41)
        for row in kept:
            self.assertEqual(self.rows[row['slot'], row['id']], row['before'], row['id'])

    def test_seven_alias_and_six_owner_changes_match_the_accepted_plan(self):
        fixed = [r for r in self.frozen['inventory'] if r['decision'] == 'fix' and r['id'] not in self.acceptance['reverted_to_baseline']]
        self.assertEqual(len(fixed), 13)
        alias_count = owner_count = 0
        for row in fixed:
            current = self.rows[row['slot'], row['id']]
            self.assertEqual(current, row['proposed_after'], row['id'])
            changed = {key for key in current.keys() | row['before'].keys() if current.get(key) != row['before'].get(key)}
            if changed == {'aliases'}:
                alias_count += 1
            else:
                self.assertEqual(changed, {'relations'})
                before = row['before']['relations'][0]
                after = current['relations'][0]
                self.assertEqual({k: v for k, v in before.items() if k != 'object'},
                                 {k: v for k, v in after.items() if k != 'object'})
                owner_count += 1
        self.assertEqual((alias_count, owner_count), (7, 6))

    def test_meaningful_model_and_format_shorthand_remains(self):
        shorthand = {'kodak_ektar_100': 'Ektar', 'kodak_tri_x_400_bw': 'Tri-X', 'ilford_hp5_bw': 'HP5', 'fuji_velvia_50': 'Velvia', 'fujifilm_pro_400h': '400H', 'polaroid_sx70': 'SX70', 'super8_film_frame': 'super8'}
        for entry_id, alias in shorthand.items():
            self.assertIn(alias.casefold(), [value.casefold() for value in self.rows['film_emulation', entry_id]['aliases']])

    def test_six_owners_match_complete_effect_scope(self):
        owners = {
            ('film_emulation', 'pe_instant_picture_area'): 'image_plane_tonal_color_regions',
            ('film_emulation', 'pe_disposable_picture_area'): 'image_plane_grain_and_frontally_lit_near_objects',
            ('film_emulation', 'pe_scan_dust_specks'): 'scanned_image_plane',
            ('film_emulation', 'pe_scan_scratches'): 'scanned_image_plane',
            ('lens_artifact', 'rb_optional_lens_falloff_candidate'): 'image_plane_center_and_periphery',
            ('lens_artifact', 'rb_optional_chromatic_fringe_candidate'): 'peripheral_high_contrast_image_edges',
        }
        for key, owner in owners.items():
            self.assertEqual(self.rows[key]['relations'][0]['object'], owner)

    def test_disposable_keeps_both_scene_lighting_and_image_grain(self):
        row = self.rows['film_emulation', 'pe_disposable_picture_area']
        self.assertEqual(row['affected_dimensions'], ['style', 'lighting'])
        self.assertIn('near objects show simple frontal flash illumination', row['concept_units'])
        self.assertIn('coarse image-plane grain overlays the picture area', row['concept_units'])
        self.assertIn('frontally_lit_near_objects', row['relations'][0]['object'])

    def test_source_projection_preserves_effect_properties_and_owners(self):
        for row in self.frozen['inventory']:
            if row['decision'] != 'fix' or not row['before'].get('relations'):
                continue
            current = self.rows[row['slot'], row['id']]
            self.assertEqual(current.get('affected_dimensions'), row['before'].get('affected_dimensions'))
            self.assertEqual(current.get('affected_properties'), row['before'].get('affected_properties'))
            projected = semantics.semantic_source(current, row['slot'], self.data['candidate_semantic_policy'])
            self.assertEqual(projected['relations'], current['relations'])

    def test_valid_optical_alternatives_are_not_blanket_normalized(self):
        self.assertEqual(self.rows['lens_artifact', 'rain_streaks_on_glass']['en'], 'rain streaks on glass or lens')
        self.assertEqual(self.rows['lens_artifact', 'pe_point_starburst']['relations'][0]['object'], 'point_light_center')
        self.assertEqual(self.rows['lens_artifact', 'pe_horizontal_anamorphic_streak']['relations'][0]['object'], 'point_light_center')
        self.assertEqual(self.rows['film_emulation', 'pe_edge_light_leak']['relations'][0]['object'], 'frame_edge_or_image_plane')


if __name__ == '__main__':
    unittest.main()
