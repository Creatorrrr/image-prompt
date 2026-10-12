"""Object identity contracts preserve requested population and orientation."""
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as pg
import photo_candidate_corpus as c

class ObjectMorphologyOwnershipTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        source = c.load(SKILL / 'assets')
        cls.profiles = {cid: c.entry(source, cid) for cid in PROFILE_IDS}

    def test_guard_evidence_supports_object_and_held_scenes(self):
        p = self.profiles['cand_041cf4d825b053bab2c087d50b25f0d4']
        req = p['evidence_requirements']['guard_phrase']
        self.assertEqual(req['min_content_words'], 11)
        self.assertEqual(req['must_mention_any'], ['a swept or cup guard forms an elaborate protective enclosure around the grip', 'a swept or cup guard visibly encloses and protects the gripping hand'])
        self.assertIn('whether any person is present', p['composition_instruction'])
        self.assertEqual(p['runtime_expression']['prompt_label_terms'], ['rapier with an elaborate swept or cup guard'])

    def test_bow_orientation_and_population_are_scene_owned(self):
        p = self.profiles['cand_30dcc9b526fd5bbf80f6648c2b6d2198']
        self.assertIn('requested orientation', p['composition_instruction'])
        self.assertIn('whether any person is present', p['composition_instruction'])
        gates = {g['id']: g for g in p['render_gates']}
        self.assertIn('requested orientation', gates['vo_weapon_compound_bow_full_riser_limbs']['description'])
        self.assertIn('no hand is required', gates['vo_weapon_compound_bow_grip_relation']['description'])
        self.assertEqual(len(gates), 5)

    def test_complete_legacy_languages_and_neutral_guard(self):
        for pid in ['cand_041cf4d825b053bab2c087d50b25f0d4', 'cand_30dcc9b526fd5bbf80f6648c2b6d2198']:
            p = self.profiles[pid]
            groups = p['semantics']['component_semantics']['groups']
            for lang in [0, 1]:
                text = '; '.join((g['any_terms'][lang] for g in groups))
                self.assertEqual(pg.candidate_pack_visual_component_match(p, text), 'component_semantics')
        p = self.profiles['cand_041cf4d825b053bab2c087d50b25f0d4']
        groups = p['semantics']['component_semantics']['groups']
        for lang in [0, 1]:
            text = '; '.join((g['any_terms'][lang + 2 if g['id'] == 'elaborate_hand_guard' else lang] for g in groups))
            self.assertEqual(pg.candidate_pack_visual_component_match(p, text), 'component_semantics')
PROFILE_IDS=['cand_041cf4d825b053bab2c087d50b25f0d4', 'cand_30dcc9b526fd5bbf80f6648c2b6d2198']
