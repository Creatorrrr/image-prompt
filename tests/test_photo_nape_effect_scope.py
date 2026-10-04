"""Scoped DATA protection for the two explicitly nape-affecting SCA relations."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
sys.path.insert(0, str(ASSETS.parent / 'scripts'))
import photo_contracts as contracts
import prompt_generator as pg

NAPE = {'sca_h15': 'hair.style.nape.layer_length',
        'sca_h16': 'hair.style.nape.undercut_length'}
LEGACY = {'sca_h15': 'hair.style.layers.crown_nape_length',
          'sca_h16': 'hair.style.side.undercut_length'}

class PhotoNapeEffectScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        extension = json.loads((ASSETS / 'photo_prompt_subculture_appearance_extension.json').read_text())
        cls.entries = {e['id']: e for e in extension['slots']['hair_style']}
        cls.registry = pg.load_visual_obligation_registry(ASSETS / 'photo_prompt_visual_obligations.json')
        cls.profiles = {p['id']: p for p in cls.registry['profiles']}

    @staticmethod
    def lock(path, target='main_subject'):
        return {'contract_version': 'photo-intent-lock/v2', 'semantic_anchors': [
            {'dimension': 'appearance', 'target': target, 'property': path}]}

    def test_both_source_surfaces_declare_nape_and_preserve_original_effect(self):
        for pid, path in NAPE.items():
            with self.subTest(profile=pid):
                effects = self.entries[pid]['affected_properties']
                self.assertEqual(effects, self.profiles[pid]['concept_candidate']['affected_properties'])
                self.assertIn({'dimension': 'appearance', 'target': 'main_subject', 'property': path}, effects)
                self.assertIn({'dimension': 'appearance', 'target': 'main_subject', 'property': LEGACY[pid]}, effects)

    def test_nape_parent_and_declared_leaf_are_protected(self):
        for pid, leaf in NAPE.items():
            for path in ('hair', 'hair.style', 'hair.style.nape', leaf):
                with self.subTest(profile=pid, path=path):
                    e = self.entries[pid]
                    self.assertFalse(contracts.property_effects_allowed(self.lock(path), e['affected_dimensions'], e['affected_properties']))

    def test_unrelated_properties_and_other_owners_remain_open(self):
        for pid in NAPE:
            e = self.entries[pid]
            for path, target in [('hair.color', 'main_subject'), ('face.eyes.iris_color', 'main_subject'), ('hair.style.nape', 'secondary_subject')]:
                with self.subTest(profile=pid, path=path, target=target):
                    self.assertTrue(contracts.property_effects_allowed(self.lock(path, target), e['affected_dimensions'], e['affected_properties']))

    def test_counterfactual_missing_nape_metadata_reproduces_guard_gap(self):
        for pid, leaf in NAPE.items():
            with self.subTest(profile=pid):
                e = self.entries[pid]
                old = [p for p in e['affected_properties'] if p['property'] != leaf]
                self.assertTrue(contracts.property_effects_allowed(self.lock('hair.style.nape'), e['affected_dimensions'], old))

    def test_cached_profile_texts_are_current(self):
        index = pg.load_visual_profile_index(ASSETS / 'photo_prompt_visual_profile_index.json', self.registry)
        for pid in NAPE:
            with self.subTest(profile=pid):
                self.assertEqual(index['entries'][pid]['text'], pg.visual_profile_semantic_text(self.profiles[pid]))

if __name__ == '__main__':
    unittest.main()
