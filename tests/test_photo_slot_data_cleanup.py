"""Data-only regressions for reviewed camera candidate search expressions.

These assertions cover representation, not arbitrary scene compatibility.
"""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/photo-prompt-image-generator/scripts'))
import prompt_generator as generator
import photo_candidate_semantics as semantics


class PhotoSlotDataCleanupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = generator.load_json(ROOT / 'skills/photo-prompt-image-generator/assets/photo_prompt_tags.json')

    def row(self, slot, entry_id):
        return next(e for e in self.data['slots'][slot] if e['id'] == entry_id)

    def test_low_angle_component_does_not_repeat_unrelated_crop_alias(self):
        e = self.row('camera_height', 'pc_pc07_component_2')
        for key in ('aliases', 'keywords'):
            self.assertNotIn('three-quarter-length portrait', e[key])
            self.assertIn('knee-up subtle low angle', e[key])
        self.assertNotIn('three-quarter-length portrait', e['embedding_text'])
        self.assertEqual(e['concept_units'], ['the viewpoint lies modestly below the face with upward spatial cues'])

    def test_eye_level_component_retains_height_not_parent_crop(self):
        e = self.row('camera_height', 'pc_pc01_component_2')
        for key in ('aliases', 'keywords'):
            self.assertNotIn('head-and-shoulders portrait', e[key])
            self.assertIn('eye-level close portrait', e[key])
        self.assertNotIn('head-and-shoulders portrait', e['embedding_text'])
        self.assertEqual(e['concept_units'], ['the viewpoint meets the subject near the visible eye line'])

    def test_generic_mirror_does_not_assert_gaze(self):
        e = self.row('camera_direction', 'mirror_reflection_camera_view')
        self.assertEqual(e['embedding_text'], 'camera view through a mirror reflection')
        self.assertEqual(e['en'], 'camera view through a mirror reflection')
        self.assertNotIn('for_any', e)  # Human-free reflected products remain possible.
        self.assertNotIn('direct gaze', generator.semantic_text_for_entry(e, 'camera_direction'))

    def test_clean_observation_uses_positive_search_expression(self):
        e = self.row('camera_direction', 'over_shoulder_observer_clean')
        self.assertNotIn('voyeuristic', generator.semantic_text_for_entry(e, 'camera_direction'))
        self.assertIn('documentary distance', e['embedding_text'])
        self.assertEqual(e['for_any'], ['human', 'animal'])  # Existing limitation unchanged.
        self.assertEqual(e['en'], 'clean over-the-shoulder observer view')

    def test_crowd_premise_does_not_become_main_subject_guard(self):
        e = self.row('camera_direction', 'through_crowd_gap_direction')
        self.assertEqual(e['en'], 'view through a gap in the crowd')
        self.assertNotIn('for_any', e)
        self.assertNotIn('requires_any_tags', e)

    def test_camera_height_metaphor_does_not_require_child_subject(self):
        e = self.row('camera_height', 'child_height_public_gaze')
        self.assertEqual(e['en'], 'child-height public gaze perspective')
        self.assertNotIn('for_any', e)

    def test_actor_dependent_surveillance_is_preserved(self):
        e = self.row('camera_height', 'pr_fixed_surveillance_observation_candidate')
        self.assertIn('passing adult', e['en'])
        self.assertIn('small part', e['en'])
        self.assertEqual(e['affected_dimensions'], ['camera'])
        self.assertTrue(semantics.semantic_source(e, 'camera_height', self.data['candidate_semantic_policy']))

    def test_contrast_context_and_overhead_snapshot_remain(self):
        e = self.row('camera_direction', 'pc_px08_component_2')
        self.assertIn('body diagonal versus camera roll', e['aliases'])
        e = self.row('camera_direction', 'overhead_social_snapshot_relation')
        self.assertIn('MZ 항공샷', e['aliases'])
        self.assertIn('subject response toward the elevated camera', e['en'])
        self.assertIn('one clearly adult subject', e['embedding_text'])

    def test_reviewed_lighting_counterexamples_are_not_search_synonyms(self):
        groups = {
            'light_direction': ['lit_rembrandt_elevated_off_axis', 'lit_volume_single_source_axis', 'lit_practical_source_owned_direction'],
            'light_type': ['lit_rembrandt_controlled_directional_source', 'lit_volume_collimated_haze_source'],
            'light_intensity': ['lit_rembrandt_low_fill_readable_eye', 'lit_practical_pool_ambient_balance', 'lit_volume_beam_gap_separation'],
            'light_shape': ['lit_rembrandt_joined_shadow_triangle', 'lit_volume_occluder_pattern_shafts'],
        }
        for slot, ids in groups.items():
            for entry_id in ids:
                with self.subTest(slot=slot, entry=entry_id):
                    e = self.row(slot, entry_id)
                    self.assertNotIn(' and rejects ', e['embedding_text'])
                    self.assertTrue(e['embedding_text'].endswith('remains source-owned'))
                    self.assertTrue(e['requires_any_tags'])

    def test_generic_worklight_keeps_explicit_robot_family_support(self):
        for entry_id in ['repair_bay_worklight', 'hologram_underglow']:
            e = self.row('lighting', entry_id)
            self.assertEqual(e['embedding_text'], e['en'])

    def test_monitor_rectangle_is_not_bedroom_only(self):
        e = self.row('light_shape', 'monitor_rectangle_glow')
        self.assertEqual(e['embedding_text'], 'rectangular blue light cast by a computer monitor screen in a dark interior')
        self.assertIn('gaming', e['tags'])

    def test_lighting_removed_counterexamples_do_not_trigger_exclusion_predicate(self):
        for slot, entry_id, term in [
            ('light_type', 'lit_volume_collimated_haze_source', 'fog'),
            ('light_type', 'lit_volume_collimated_haze_source', 'flare'),
            ('light_direction', 'lit_practical_source_owned_direction', 'lamp'),
            ('light_direction', 'lit_practical_source_owned_direction', 'LUT'),
            ('light_shape', 'monitor_rectangle_glow', 'bedroom'),
        ]:
            e = self.row(slot, entry_id)
            blob = generator.candidate_pack_entry_blob(e, extra=[str(e.get('semantic_caption') or ''), str(e.get('embedding_text') or ''), str(e.get('definition') or ''), *generator.normalize_list(e.get('concept_units')), *generator.normalize_list(e.get('manifestations'))])
            self.assertFalse(generator.intent_alias_matches(blob, term), (entry_id, term))

    def test_full_frame_component_does_not_claim_pose_only_aliases(self):
        e = self.row('subject_framing', 'pc_pc08_component_1')
        self.assertEqual(e['aliases'], ['한쪽 다리에 무게를 둔 비대칭 전신'])
        self.assertEqual(e['keywords'], e['aliases'])
        self.assertEqual(e['embedding_text'], 'the full frame preserves the head and both feet | 한쪽 다리에 무게를 둔 비대칭 전신')
        self.assertEqual(e['concept_units'], ['the full frame preserves the head and both feet'])
        self.assertEqual(e['for_any'], ['human'])
        for slot, entry_id in [('body_pose', 'pc_pc08_component_2'), ('body_orientation', 'pc_pc08_component_3')]:
            sibling = self.row(slot, entry_id)
            self.assertIn('weight-shift pose', sibling['aliases'])
            self.assertIn('asymmetrical standing pose', sibling['aliases'])

    def test_crowd_gap_korean_keeps_subject_owner_generic(self):
        e = self.row('crowd_density', 'crowd_gap_single_subject')
        self.assertEqual(e['ko'], '군중 사이 틈으로 보이는 단일 피사체')
        self.assertEqual(e['phrase_ko'], '군중 사이 틈으로 단일 피사체가 보이는 배열로')
        self.assertEqual(e['en'], 'one subject visible through a gap in the surrounding crowd')
        self.assertNotIn('for_any', e)

    def test_repair_pit_korean_output_preserves_subject_type(self):
        location = self.row('location', 'repair_garage_pit')
        self.assertEqual(location['ko'], '자동차 정비소의 정비 피트')
        self.assertEqual(location['phrase_ko'], '자동차 정비소의 정비 피트에서')
        self.assertEqual(location['en'], 'an auto repair garage pit')
        self.assertNotIn('for_any', location)

    def test_closing_cleanup_only_says_visitors_have_left(self):
        occasion = self.row('occasion_context', 'closing_cleanup_after_hours')
        self.assertEqual(occasion['phrase_ko'], '방문객들이 떠난 뒤의 폐점 정리 시간으로')
        self.assertEqual(occasion['en'], 'after-hours closing cleanup after visitors have left')
        self.assertNotIn('사람들이 떠난', occasion['phrase_ko'])


if __name__ == '__main__':
    unittest.main()
