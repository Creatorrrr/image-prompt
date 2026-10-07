"""Observed independent prompt cases: roles are not performing mechanisms."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as pg
from visual_profile_contracts import hard_activation_is_supported


class DataQualityScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = pg.load_json(SKILL / 'assets/photo_prompt_tags.json')
        cls.registry = pg.load_visual_obligation_registry(SKILL / 'assets/photo_prompt_visual_obligations.json')
        cls.profile = next(row for row in cls.registry['profiles'] if row['id'] == 'cello_endpin_seated_bowed')

    def supported(self, text):
        return hard_activation_is_supported(self.profile, text, matches=pg.intent_alias_matches, is_negated=pg.intent_term_is_negated)

    def test_cello_role_and_inspection_do_not_require_bowed_seated_playing(self):
        for text in ['cello', '첼리스트', 'a cellist checking the bow before an outdoor performance',
                     'a seated cellist inspecting the bow', 'a standing musician playing the cello']:
            with self.subTest(text=text): self.assertFalse(self.supported(text))

    def test_explicit_seated_playing_still_supported(self):
        for text in ['a seated musician bowing the cello strings', '앉아서 첼로를 연주하는 연주자']:
            with self.subTest(text=text): self.assertTrue(self.supported(text))

    def test_preperformance_inspection_exclusion_is_narrow(self):
        supported, reason = pg.visual_profile_context_applicability(
            self.profile, 'a seated cellist checking the bow before playing the cello', has_authorial_core_context=True)
        self.assertFalse(supported)
        self.assertEqual(reason, 'request_exclusion')

    def test_human_receiver_candidates_reject_no_people_requests(self):
        for slot, identity in [('platform_framing', 'pr_casual_crop_subject_legibility_candidate'),
                               ('motion', 'rb_shared_wind_response_candidate')]:
            row = next(row for row in self.data['slots'][slot] if row['id'] == identity)
            with self.subTest(candidate=identity):
                self.assertEqual(pg.entry_block_reason(row, slot, {'intent_constraints': {'no_people': True}}), 'explicit_no_people')
                self.assertIsNone(pg.entry_block_reason(row, slot, {'intent_constraints': {'no_people': False}}))


if __name__ == '__main__': unittest.main()
