"""Data-only cleanup regressions; these are not rendering quality claims."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/photo-prompt-image-generator/scripts'))
import prompt_generator as g


class NextSlotDataCleanupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = g.load_json(ROOT / 'skills/photo-prompt-image-generator/assets/photo_prompt_tags.json')

    def row(self, slot, entry_id):
        return next(e for e in self.data['slots'][slot] if e['id'] == entry_id)

    def test_neutral_pose_search_matches_its_authored_label(self):
        for slot, entry_id in [('body_pose', 'arms_crossed_stance'), ('hand_pose', 'hand_on_hip')]:
            e = self.row(slot, entry_id)
            self.assertEqual(e['embedding_text'], e['en'])
        self.assertIn('narrative_safe', self.row('body_pose', 'arms_crossed_stance')['tags'])

    def test_explicit_covered_pose_variants_remain_covered(self):
        for entry_id in ['power_stance_feet_apart', 'kneeling_soft_pose']:
            e = self.row('body_pose', entry_id)
            self.assertIn('covered', e['en'])
            self.assertIn('covered', e['embedding_text'])
            self.assertTrue(all('covered' in alias for alias in e['aliases']))
            self.assertEqual(e['facets']['soft_body_role'], ['narrative_safe'])

    def test_body_proportion_component_does_not_repeat_crop_alias(self):
        e = self.row('body_pose', 'pc_pc07_component_3')
        self.assertNotIn('three-quarter-length portrait', g.semantic_text_for_entry(e, 'body_pose'))
        self.assertIn('knee-up subtle low angle', e['aliases'])
        self.assertEqual(e['concept_units'], ['the torso and legs retain coherent near-to-far proportions'])
        self.assertEqual(e['relations'][0]['subject'], 'main torso and legs')

    def test_pose_counterexamples_are_not_positive_search_terms(self):
        for slot, entry_id, negative, positive in [
            ('body_pose', 'editorial_s_curve_pose', 'Hogarthian', 'continuous planar S rhythm'),
            ('body_orientation', 'thorax_pelvis_opposed_azimuth', 'camera tilt', 'separate ribcage and pelvic planes'),
            ('hand_pose', 'relaxed_wrist_offset_line', 'broken-wrist', 'joint stays anatomically continuous'),
        ]:
            text = g.semantic_text_for_entry(self.row(slot, entry_id), slot)
            self.assertNotIn(negative, text)
            self.assertIn(positive, text)

    def test_contact_and_noncontact_owners_stay_distinct(self):
        e = self.row('contact_point', 'fingertip_contact_visible_target_non_support')
        self.assertIn('non-load-bearing', e['en'])
        self.assertIn('body support remains elsewhere', e['embedding_text'])
        e = self.row('contact_point', 'theremin_no_contact_dual_field_relation')
        self.assertIn('no hand touching the cabinet', e['embedding_text'])
        self.assertIn('forearm contacting a stable surface', self.row('body_pose', 'propped_elbow_recline_support')['embedding_text'])
        self.assertIn('contact patch against a wall', self.row('body_pose', 'casual_lean_against_wall')['embedding_text'])


    def test_expression_aliases_name_complete_expressions(self):
        expected = {
            'candid_laugh': ['candid laugh', 'a candid laugh'],
            'eyes_closed_serene': ['serene eyes closed', 'serene eyes-closed expression'],
            'looking_away_pensive': ['pensive look away from camera', 'looking away pensively'],
            'playful_smirk': ['playful smirk', 'a playful smirk'],
        }
        for entry_id, aliases in expected.items():
            self.assertEqual(self.row('expression', entry_id)['aliases'], aliases)

    def test_coordinated_gaze_search_keeps_target_not_inferences(self):
        e = self.row('gaze_engagement', 'same_adult_target_coordinated_gaze')
        self.assertIn('one identifiable adult target', e['embedding_text'])
        for word in ['seduction', 'consent', 'attraction']:
            self.assertNotIn(word, e['embedding_text'])
        e = self.row('gaze_target', 'gaze_to_distant_horizon')
        self.assertEqual(e['embedding_text'], 'gaze toward exile horizon or future rule')
        self.assertIn('royal', e['tags'])

    def test_material_alias_and_construction_search_avoid_substitutes(self):
        self.assertEqual(self.row('surface_material', 'white_marble_surface')['aliases'], ['white marble surface', '흰 대리석 표면'])
        for slot, entry_id, negatives in [
            ('garment_detail', 'button_down_collar_point_fastening', ['not button-up alone', 'generic button-up']),
            ('garment_detail', 'jumpsuit_bodice_crotch_leg_continuity', ['not matching separates', 'coordinated top and pants']),
            ('garment_detail', 'athletic_gusset_panel', ['not fold shadow', 'printed shape']),
            ('surface_material', 'athletic_mesh_open_structure', ['not printed grid', 'printed dots']),
            ('garment_detail', 'sheer_visible_edge_weave', ['wet skin', 'overexposure']),
        ]:
            text = g.semantic_text_for_entry(self.row(slot, entry_id), slot)
            for term in negatives:
                self.assertNotIn(term, text)
        self.assertIn('two separate small buttons', self.row('garment_detail', 'button_down_collar_point_fastening')['embedding_text'])
        self.assertIn('two distinct trouser legs', self.row('garment_detail', 'jumpsuit_bodice_crotch_leg_continuity')['embedding_text'])
        self.assertIn('blue-gray hanbok', self.row('garment_detail', 'landscape_embroidery_hem')['embedding_text'])
        self.assertIn('robot casing', self.row('surface_material', 'worn_alloy_surface')['embedding_text'])

    def test_optical_variants_keep_effects_without_false_aliases(self):
        e = self.row('film_emulation', 'lit_filmic_grain_rolloff_halation')
        self.assertEqual(e['embedding_text'], e['en'])
        for term in ['global bloom', 'vintage preset', 'lens ghost']:
            self.assertNotIn(term, g.semantic_text_for_entry(e, 'film_emulation'))
        self.assertEqual(self.row('texture', 'dust_on_lens')['aliases'], ['dust on lens', 'tiny dust specks on the lens'])
        self.assertEqual(self.row('film_emulation', 'kodak_portra_400_look')['aliases'], ['Kodak Portra 400', 'Portra 400 film look'])
        e = self.row('film_emulation', 'cinestill_800t_halation')
        self.assertNotIn('halation', e['aliases'])
        self.assertIn('halation', e['keywords'])
        self.assertIn('halation', e['embedding_text'])
        self.assertEqual(self.row('lens_artifact', 'rain_streaks_on_glass')['en'], 'rain streaks on glass or lens')
        self.assertEqual(self.row('texture', 'halation')['en'], 'film halation and soft light bloom')

if __name__ == '__main__':
    unittest.main()
