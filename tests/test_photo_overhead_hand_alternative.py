"""Existing hand-or-prop perspective alternatives must reach render contracts."""
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/photo-prompt-image-generator'
sys.path.insert(0,str(SKILL/'scripts'))
import prompt_generator as pg
from audit_composed_prompt import authorial_evidence_tokens

class OverheadHandAlternativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        reg=pg.load_visual_obligation_registry(SKILL/'assets/photo_prompt_visual_obligations.json')
        cls.profile=next(p for p in reg['profiles'] if p['id']=='overhead_social_snapshot_relation')

    def test_prop_and_hand_languages_remain_complete(self):
        p=self.profile;groups=p['semantics']['component_semantics']['groups']
        for language in [0,1]:
            for variant in [language,language+2]:
                text='; '.join(g['any_terms'][variant if i==3 else language] for i,g in enumerate(groups))
                self.assertEqual(pg.candidate_pack_visual_component_match(p,text),'component_semantics')

    def test_evidence_retains_original_floor_and_alternatives(self):
        req=self.profile['evidence_requirements']['overhead_foreshortening_phrase']
        self.assertEqual(req['min_content_words'],13)
        self.assertEqual(len(req['must_mention_any']),2)
        self.assertIn('one near prop',req['must_mention_any'][0])
        self.assertIn('one near hand',req['must_mention_any'][1])
        for term in req['must_mention_any']:
            self.assertEqual(len(authorial_evidence_tokens(term)),12)
            self.assertGreaterEqual(len(authorial_evidence_tokens(term+' above the adult subject in the courtyard')),13)

    def test_gate_and_instruction_allow_current_definition(self):
        p=self.profile
        self.assertIn('hand or prop',p['render_gates'][3]['description'])
        self.assertIn('hand or prop',p['composition_instruction'])
        self.assertEqual(len(p['render_gates']),5)
