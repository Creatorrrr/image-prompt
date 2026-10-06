"""Source-scoped robe correction preserves owned sides and opt-in duties."""
from __future__ import annotations
import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
sys.path.insert(0, str(ASSETS.parent / 'scripts'))
import prompt_generator as pg

BEFORE = ROOT / 'docs/research-evidence/photo-prompt/robe-back-source-consistency-20261006/SOURCE-SCOPE-BEFORE.json'
BEFORE_SHA = '3c3c138f02c57a4ba438393fea86d5c9ef0fd19b1cac934b93371c32c1aae732'

class RobeBackSourceScopeConsistencyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw = BEFORE.read_bytes()
        if hashlib.sha256(raw).hexdigest() != BEFORE_SHA:
            raise AssertionError('Immutable original-object fixture drift')
        cls.before = json.loads(raw)['before_objects']
        registry = pg.load_visual_obligation_registry(ASSETS / 'photo_prompt_visual_obligations.json')
        cls.profiles = {p['id']: p for p in registry['profiles']}
        cls.robe = cls.profiles['ri_daoist_robe_sky']
        cls.extension = json.loads((ASSETS / 'photo_prompt_religion_iconography_extension.json').read_text())

    def test_back_relation_requires_every_component_in_both_languages(self):
        groups = self.robe['semantics']['component_semantics']['groups']
        self.assertEqual(len(groups), 3)
        for language in (0, 1):
            terms = [g['any_terms'][language] for g in groups]
            self.assertIsNotNone(pg.candidate_pack_visual_component_match(self.robe, '; '.join(terms)))
            for missing in range(3):
                with self.subTest(language=language, missing=missing):
                    partial = '; '.join(t for i, t in enumerate(terms) if i != missing)
                    self.assertIsNone(pg.candidate_pack_visual_component_match(self.robe, partial))

    def test_front_and_mixed_side_relations_do_not_satisfy_back_variant(self):
        old = self.before['robe_profile']['semantics']['visual_components']
        self.assertIsNone(pg.candidate_pack_visual_component_match(self.robe, '; '.join(old)))
        current = [g['any_terms'][0] for g in self.robe['semantics']['component_semantics']['groups']]
        for changed in range(3):
            mixed = list(current)
            self.assertIn('back', mixed[changed])
            mixed[changed] = mixed[changed].replace('back', 'front')
            with self.subTest(component=changed):
                self.assertIsNone(pg.candidate_pack_visual_component_match(self.robe, '; '.join(mixed)))
        self.assertIsNone(pg.candidate_pack_visual_component_match(self.robe, 'Daoist ceremonial robe'))

    def test_source_repair_keeps_existing_component_api_and_owned_layout(self):
        current = next(p for p in json.loads((ASSETS / 'photo_prompt_visual_obligations_religion_iconography.json').read_text())['profiles'] if p['id'] == 'ri_daoist_robe_sky')
        previous = self.before['robe_profile']
        old_components = previous['authored_components']['components']
        new_components = current['authored_components']['components']
        self.assertEqual(len(old_components), len(new_components))
        for old, new in zip(old_components, new_components):
            old, new = copy.deepcopy(old), copy.deepcopy(new)
            for value in (old, new):
                for key in ('match_terms', 'evidence_terms', 'instruction'):
                    value.pop(key)
                value['render_gate'].pop('description')
            self.assertEqual(old, new)
        entry = next(e for e in self.extension['slots']['composition'] if e['id'] == 'ri_daoist_robe_sky_readable_composition')
        old_entry = self.before['robe_composition']
        for key in ('affected_dimensions', 'affected_properties', 'core_assertion_discovery', 'requires_primary_any_tags'):
            self.assertEqual(entry[key], old_entry[key], key)
        self.assertEqual([{k: v for k, v in rel.items() if k != 'object'} for rel in entry['relations']],
                         [{k: v for k, v in rel.items() if k != 'object'} for rel in old_entry['relations']])
        self.assertEqual(entry['relations'][0]['object'], '; '.join(current['semantics']['visual_components']))
        self.assertEqual(current['semantics']['claim_limits'], previous['semantics']['claim_limits'])


    def test_bundle_does_not_add_a_new_motif_or_change_the_garment_owner(self):
        current = next(b for b in self.extension['visual_semantics'] if b['id'] == self.before['robe_bundle_source']['id'])
        previous = self.before['robe_bundle_source']
        self.assertEqual(current.keys(), previous.keys())
        for key in ('id', 'candidate_ids', 'hard_profile_id', 'confusion_boundaries'):
            self.assertEqual(current[key], previous[key], key)
        self.assertEqual(len(current['component_groups']), 3)
        self.assertEqual(len(current['component_groups']), len(previous['component_groups']))
        self.assertEqual(current['component_groups'], self.robe['semantics']['visual_components'])
        self.assertEqual([{k: v for k, v in rel.items() if k != 'object'} for rel in current['relations']],
                         [{k: v for k, v in rel.items() if k != 'object'} for rel in previous['relations']])
        self.assertEqual(current['relations'][0]['object'], '; '.join(current['component_groups']))

if __name__ == '__main__':
    unittest.main()
