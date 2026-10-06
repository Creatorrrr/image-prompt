from __future__ import annotations

import copy
import json
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = Path(os.environ.get('PHOTO_WATER_TEST_ROOT', ROOT / 'skills/photo-prompt-image-generator'))
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as pg
from photo_contracts import property_effects_allowed
from visual_profile_contracts import compile_visual_profile, hard_activation_is_supported


class WaterRelationRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        asset = SKILL / 'assets'
        cls.profiles = {p['id']: p for p in json.loads((asset / 'photo_prompt_visual_obligations_water_relations.json').read_text())['profiles']}
        cls.candidates = {c['id']: c for entries in json.loads((asset / 'photo_prompt_water_relations_extension.json').read_text())['slots'].values() for c in entries}

    def supports(self, profile, text):
        return hard_activation_is_supported(profile, text, matches=pg.intent_alias_matches, is_negated=pg.intent_term_is_negated)

    def test_complete_proposition_requires_all_components_for_hard_activation(self):
        # A glossary label or neighboring physical sense must not prescribe
        # the entire selected camera/carrier realization.
        cases = {
            'w007': ('water glass meniscus', 'a glass lens projects a curved highlight'),
            'w027': ('underwater gas bubbles', 'airborne rain droplets over a street'),
            'w049': ('underwater caustics', 'sun glitter reflects toward the viewer'),
            'w050': ('Snell window', 'a circular glass porthole in a dry room'),
            'w054': ('bioluminescence', 'a blue lamp illuminates a plastic model'),
            'w055': ('biofluorescence', 'a self luminous trail without an excitation source'),
            'w070': ('braided river', 'two tributaries join once without a dividing bar'),
            'w146': ('scuba', 'a detached hose ending beside another person'),
            'w157': ('wet hair', 'damp clumps lying flat against a neck in air'),
            'w169': ('rip current', 'a circular drain vortex in a bathtub'),
            'w190': ('over under', 'a collage of two unrelated viewpoints'),
        }
        for uid, negatives in cases.items():
            p = self.profiles['water_rel_' + uid]
            with self.subTest(unit=uid):
                self.assertTrue(self.supports(p, p['activation']['exact_terms'][0]))
                for text in negatives:
                    self.assertFalse(self.supports(p, text))
                compiled = compile_visual_profile(p)
                self.assertEqual(len(compiled['required_evidence_fields']), 3)
                self.assertEqual(len(compiled['render_gates']), 3)

    def test_wetness_cannot_imply_transparency_or_change_garment_layering(self):
        film = self.candidates['water_w020']
        cling = self.candidates['water_w161']
        transmission = self.candidates['water_w162']
        self.assertNotIn('transmission', film['en'])
        self.assertNotIn('transmission', cling['en'])
        self.assertIn('partial transmission', transmission['en'])
        lock = {'contract_version':'photo-intent-lock/v2','semantic_anchors':[{
            'dimension':'appearance','target':'main_subject','property':'wardrobe.optical_transmission'}]}
        self.assertFalse(property_effects_allowed(lock, transmission['affected_dimensions'], transmission['affected_properties']))
        # Carrier changes must not evade the same semantic property lock.
        crossed = copy.deepcopy(transmission['affected_properties'])
        crossed[0]['dimension'] = 'appearance'
        self.assertFalse(property_effects_allowed(lock, ['appearance'], crossed))

    def test_camera_property_and_equipment_owner_are_declared(self):
        lock = {'contract_version':'photo-intent-lock/v2','semantic_anchors':[{
            'dimension':'camera','target':'capture_camera','property':'viewpoint.direction'}]}
        snell = self.candidates['water_w050']
        self.assertFalse(property_effects_allowed(lock, snell['affected_dimensions'], snell['affected_properties']))
        scuba = self.candidates['water_w146']
        self.assertIn('same diver', scuba['en'])
        self.assertTrue(any(r['subject']=='regulator_hose' or r['object']=='regulator_hose' for r in scuba['relations']))
        self.assertTrue(any(e['target']=='main_subject' and e['property']=='equipment_attachment' for e in scuba['affected_properties']))

    def test_anatomy_and_river_topology_keep_different_connections(self):
        kelp = self.candidates['water_w092']
        seagrass = self.candidates['water_w093']
        self.assertIn('stipes', kelp['en'])
        self.assertIn('rooted', seagrass['en'])
        self.assertNotEqual(kelp['relations'], seagrass['relations'])
        confluence = self.candidates['water_w064']
        braid = self.candidates['water_w070']
        oxbow = self.candidates['water_w069']
        self.assertIn('joined downstream', confluence['en'])
        self.assertIn('reconnections', braid['en'])
        self.assertIn('land separating', oxbow['en'])

    def test_nonvisual_properties_never_become_exact_shape_aliases(self):
        exact = [term for p in self.profiles.values() for term in p['activation']['exact_terms']]
        for term in ('water', '물', 'potable water', 'freshwater', 'salinity', '수압', '용존산소', 'haenyeo'):
            self.assertNotIn(term, exact)

    def test_nonportrait_subjects_keep_their_actual_category(self):
        for uid, category in [('w040','environment'),('w088','environment'),
                              ('w092','plant'),('w093','plant'),('w100','animal'),
                              ('w108','animal'),('w111','animal'),('w126','object')]:
            with self.subTest(unit=uid):
                self.assertEqual(pg.subject_category({'subject':self.candidates['water_'+uid]}), category)
        self.assertNotIn('species', self.candidates['water_w040']['affected_dimensions'])
        self.assertNotIn('species', self.candidates['water_w126']['affected_dimensions'])

    def test_natural_component_paraphrases_enable_only_optional_discovery(self):
        cases = {
            'w021': ('A water jet leaves a spout and lands in a shallow receiving basin.', 'A detached dry spout is displayed on a table.'),
            'w036': ('A vessel has a widening wake trailing from its stern.', 'A dry boat stands inside a workshop.'),
            'w044': ('A tapered ice form attaches to an overhead edge and ends in a melting tip.', 'A pointed glass ornament sits on a table.'),
            'w047': ('Reflections of reed stems bend across the river water plane.', 'Painted reeds decorate an opaque wall.'),
            'w049': ('Caustics from a rippled water surface illuminate the submerged pool floor.', 'Sun glitter reflects off dry metal toward the camera.'),
            'w146': ('A cylinder and BCD connect through a regulator hose to the mouthpiece of the same diver.', 'A cylinder with a detached hose lies in a shop.'),
        }
        for uid, (positive, negative) in cases.items():
            profile=compile_visual_profile(self.profiles['water_rel_'+uid])
            with self.subTest(unit=uid):
                self.assertIsNotNone(pg.candidate_pack_visual_component_match(profile, positive))
                self.assertIsNone(pg.candidate_pack_visual_component_match(profile, negative))
                self.assertFalse(self.supports(profile, positive))
                self.assertEqual(len(profile['render_gates']),3)


if __name__ == '__main__':
    unittest.main()
