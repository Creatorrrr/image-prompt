"""Narrow canonical effect declarations; not general garment/layer understanding."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
sys.path.insert(0, str(ASSETS.parent / 'scripts'))
import photo_contracts as contracts
import prompt_generator as pg

IDS = ('clt_ct091_v1', 'clt_ct091_v2')
OPACITY = 'wardrobe.surface.sheer_opacity'
FAMILY = 'wardrobe.surface.chiffon_organza_taffeta'

class PhotoTextileOpacityEffectScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        extension = json.loads((ASSETS / 'photo_prompt_textile_surface_extension.json').read_text())
        cls.entries = {r['id']: r for r in extension['slots']['surface_material']}
        cls.registry = pg.load_visual_obligation_registry(ASSETS / 'photo_prompt_visual_obligations.json')
        cls.profiles = {p['id']: p for p in cls.registry['profiles']}

    @staticmethod
    def lock(path, target='main_subject', dimension='appearance'):
        return {'contract_version': 'photo-intent-lock/v2', 'semantic_anchors': [
            {'dimension': dimension, 'target': target, 'property': path}]}

    def allowed(self, candidate_id, path, target='main_subject', dimension='appearance'):
        row = self.entries[candidate_id]
        return contracts.property_effects_allowed(self.lock(path, target, dimension), row['affected_dimensions'], row['affected_properties'])

    def test_matching_sources_append_opacity_preserving_family_owner_and_carrier(self):
        for cid in IDS:
            with self.subTest(candidate=cid):
                row = self.entries[cid]
                profile = self.profiles[cid.replace('clt_', 'clothing_', 1)]
                expected = [{'dimension': 'appearance', 'target': 'main_subject', 'property': p} for p in (FAMILY, OPACITY)]
                self.assertEqual(row['affected_dimensions'], ['appearance'])
                self.assertEqual(row['affected_properties'], expected)
                self.assertEqual(profile['concept_candidate']['affected_properties'], expected)

    def test_canonical_opacity_and_ancestor_locks_reject(self):
        for cid in IDS:
            for path in (OPACITY, 'wardrobe.surface', 'wardrobe'):
                with self.subTest(candidate=cid, path=path):
                    self.assertFalse(self.allowed(cid, path))

    def test_disjoint_owner_and_properties_stay_open(self):
        for cid in IDS:
            for path, target in [('wardrobe.color.hue', 'main_subject'), ('wardrobe.type', 'main_subject'), (OPACITY, 'secondary_subject')]:
                with self.subTest(candidate=cid, path=path, target=target):
                    self.assertTrue(self.allowed(cid, path, target))

    def test_removing_only_added_effect_reproduces_canonical_gap(self):
        for cid in IDS:
            with self.subTest(candidate=cid):
                row = self.entries[cid]
                old = [p for p in row['affected_properties'] if p['property'] != OPACITY]
                self.assertTrue(contracts.property_effects_allowed(self.lock(OPACITY), row['affected_dimensions'], old))

    def test_deferred_gradient_color_scope_remains_unchanged(self):
        row = self.entries['clt_ct098_v2']
        expected = [{'dimension': 'appearance', 'target': 'main_subject', 'property': 'wardrobe.surface.wash_distress_dye'}]
        self.assertEqual(row['affected_properties'], expected)
        self.assertEqual(self.profiles['clothing_ct098_v2']['concept_candidate']['affected_properties'], expected)

    def test_profile_index_texts_match_current_authored_profiles(self):
        index = pg.load_visual_profile_index(ASSETS / 'photo_prompt_visual_profile_index.json', self.registry)
        for cid in IDS:
            pid = cid.replace('clt_', 'clothing_', 1)
            with self.subTest(profile=pid):
                self.assertEqual(index['entries'][pid]['text'], pg.visual_profile_semantic_text(self.profiles[pid]))

if __name__ == '__main__':
    unittest.main()
