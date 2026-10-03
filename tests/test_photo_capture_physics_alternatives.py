"""Motion ownership and split optical transition retain valid legacy subtypes."""
from __future__ import annotations
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/photo-prompt-image-generator'
sys.path.insert(0,str(SKILL/'scripts'))
import prompt_generator as pg

class CapturePhysicsAlternativesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        reg=pg.load_visual_obligation_registry(SKILL/'assets/photo_prompt_visual_obligations.json')
        cls.profiles={p['id']:p for p in reg['profiles']}

    def test_complete_languages_and_missing_groups(self):
        for pid in ['rolling_shutter_readout_skew','split_diopter_dual_focus_planes']:
            p=self.profiles[pid];groups=p['semantics']['component_semantics']['groups']
            for lang in [0,1]:
                parts=[g['any_terms'][lang] for g in groups]
                with self.subTest(profile=pid,language=lang):
                    self.assertEqual(pg.candidate_pack_visual_component_match(p,'; '.join(parts)),'component_semantics')
                    for i in range(len(parts)):
                        self.assertIsNone(pg.candidate_pack_visual_component_match(p,'; '.join(v for j,v in enumerate(parts) if i!=j)))
                    for term in p['activation']['exclude_if_any_terms']:
                        self.assertIsNone(pg.candidate_pack_visual_component_match(p,'; '.join(parts+[term])))

    def test_rolling_legacy_combined_motion_anchors_remain(self):
        p=self.profiles['rolling_shutter_readout_skew']
        self.assertIn('normally vertical repeated structures lean or bend consistently in one direction',p['evidence_requirements']['rolling_structure_phrase']['must_mention_any'])
        self.assertIn('the fast-moving subject shears across its height or width instead of remaining rigid',p['evidence_requirements']['rolling_subject_phrase']['must_mention_any'])
        self.assertIn('a separate background structure is not required',p['render_gates'][1]['description'])
        self.assertIn('relative to the camera',p['semantics']['definition'])

    def test_split_band_and_transition_are_alternatives(self):
        p=self.profiles['split_diopter_dual_focus_planes']
        fields=p['evidence_requirements']
        anchors=[t for req in fields.values() for t in req['must_mention_any']]
        self.assertIn('two separated sharp zones with a softer intervening band',anchors)
        self.assertTrue(any('optical transition' in t for t in anchors))
        self.assertEqual(len(p['render_gates']),5)

    def test_partial_motion_examples_do_not_bypass_components(self):
        p=self.profiles['rolling_shutter_readout_skew']
        for text in [
            'a fast lateral vehicle shears across its height against upright stationary posts when the camera is fixed',
            '빠른 피사체 움직임이나 카메라 이동에 따른 상대 영상 운동이 판독 축을 따라 일관된 전단을 만듦',
        ]:
            self.assertIsNone(pg.candidate_pack_visual_component_match(p,text))
        for text in p['semantics']['paraphrase_examples']:
            self.assertEqual(pg.candidate_pack_visual_component_match(p,text),'semantic_paraphrase_example')
