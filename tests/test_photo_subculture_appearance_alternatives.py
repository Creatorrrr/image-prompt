"""Alternative language must preserve carriers, complete relations and lock scope."""
from __future__ import annotations
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
ASSETS = SKILL / 'assets'
RUN = ROOT / 'docs/research-evidence/photo-prompt/subculture-appearance-integration-20261003'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as pg
import photo_contracts as contracts


class PhotoSubcultureAppearanceAlternativesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = pg.load_visual_obligation_registry(ASSETS / 'photo_prompt_visual_obligations.json')
        cls.profiles = {p['id']: p for p in cls.registry['profiles']}
        cls.extension = json.loads((ASSETS / 'photo_prompt_subculture_appearance_extension.json').read_text())
        cls.new_ids = [p['id'] for p in json.loads((ASSETS / 'photo_prompt_visual_obligations_subculture_appearance.json').read_text())['profiles']]
        cls.thin = copy.deepcopy(cls.registry)
        cls.thin['profiles'] = [cls.profiles[k] for k in cls.new_ids]

    def hard(self, text, source='user_requirement', polarity='required', adult=True):
        result = pg.resolve_visual_profile_hits(self.thin, [{'text': text, 'source': source, 'polarity': polarity}], adult_context=adult)
        return {h['profile_id'] for h in result['hits'] if h['hard_eligible']}

    def test_alternative_components_require_every_part(self):
        for profile_id in self.new_ids:
            p = self.profiles[profile_id]
            groups = p['semantics']['component_semantics']['groups']
            for variant in (0, -1):
                proof = [g['any_terms'][variant] for g in groups]
                with self.subTest(profile=profile_id, variant=variant):
                    self.assertEqual(pg.candidate_pack_visual_component_match(p, '; '.join(proof)), 'component_semantics')
                for missing in range(len(proof)):
                    with self.subTest(profile=profile_id, missing=missing, variant=variant):
                        self.assertIsNone(pg.candidate_pack_visual_component_match(p, '; '.join(t for i, t in enumerate(proof) if i != missing)))

    def test_exact_scope_is_positive_and_advisory_cannot_become_hard(self):
        for profile_id in ('sca_h01', 'sca_h05', 'sca_h13', 'sca_f01', 'sca_f05', 'sca_g01', 'sca_g14', 'sca_x01', 'sca_x10'):
            p = self.profiles[profile_id]
            text = 'an adult face with hair and a garment shows ' + p['activation']['exact_terms'][0]
            with self.subTest(profile=profile_id):
                self.assertIn(profile_id, self.hard(text))
                self.assertNotIn(profile_id, self.hard(text, source='authorial_core_interpretation', polarity='advisory'))
                self.assertNotIn(profile_id, self.hard(text, polarity='excluded'))
                self.assertNotIn(profile_id, self.hard('an adult face has no ' + p['activation']['exact_terms'][0]))
        self.assertNotIn('sca_f01', self.hard('an adult face shows upward outer canthus relation in face axes', adult=False))
        aliases = {t.casefold() for k in self.new_ids for t in self.profiles[k]['activation']['exact_terms']}
        self.assertTrue({'メカクレ', '메카쿠레', 'odd eyes', '오드아이', 'pannier', '패니에', '고딕', 'cyborg', '사이보그', 'yaeba', 'fang'}.isdisjoint(aliases))

    def test_wrong_carriers_and_neighbor_structures_do_not_supply_components(self):
        pairs = [
            ('sca_h01', 'two thin hair tufts rise from separate crown roots; the two tufts remain hair rather than attached hardware'),
            ('sca_h05', 'two straight ponytails hang down; a striped ribbon spirals around a separate rod'),
            ('sca_h06', 'two lateral hair masses descend as repeated helical turns; each spiral narrows toward its lower tip'),
            ('sca_h13', 'one patch covers one stated eye; the opposite eye remains outside that patch'),
            ('sca_h14', 'one cloth band spans both eye regions; the band leaves the selected lower face outside its coverage'),
            ('sca_x01', 'two anatomical ear roots emerge from head skin; fur covers both ears'),
            ('sca_x10', 'two dyed colors follow a hair helix; individual colored strands remain part of the hair'),
            ('sca_g04', 'a separate glove covers the hand and forearm; the sleeve stops at the wrist'),
            ('sca_g14', 'a rigid plate covers only the forearm; the hand remains separately exposed'),
            ('sca_f01', 'the head is rolled clockwise; the upper lids are partly lowered'),
            ('sca_f13', 'one long pointed canine tooth projects beyond its neighboring teeth'),
            ('sca_f05', 'a bounded wedge of color occupies part of one iris; the remainder of that same iris retains its selected different color'),
            ('sca_f05_sectoral', 'one iris is entirely blue; the opposite iris is entirely brown'),
            ('sca_f05_central', 'a star-shaped lamp highlight falls on one eye'),
        ]
        for profile_id, text in pairs:
            with self.subTest(profile=profile_id):
                self.assertIsNone(pg.candidate_pack_visual_component_match(self.profiles[profile_id], text))
        self.assertIsNone(pg.candidate_pack_visual_component_match(self.profiles['y2kr_mesh'], 'printed diamonds decorate a continuous opaque fabric'))

    def test_parent_property_locks_and_carrier_aliases_are_preserved(self):
        entries = {e['id']: e for rows in self.extension['slots'].values() for e in rows}
        for candidate_id, property_path in [('sca_h05', 'hair.style'), ('sca_h19', 'hair.color'), ('sca_g14', 'wardrobe.details.armour_owner_parts'), ('sca_g20', 'wardrobe.color')]:
            e = entries[candidate_id]
            lock = {'contract_version': 'photo-intent-lock/v2', 'semantic_anchors': [{'dimension': 'appearance', 'target': 'main_subject', 'property': property_path}]}
            with self.subTest(candidate=candidate_id):
                self.assertFalse(contracts.property_effects_allowed(lock, e['affected_dimensions'], e['affected_properties']))
        lock = {'contract_version': 'photo-intent-lock/v2', 'semantic_anchors': [{'dimension': 'appearance', 'target': 'main_subject', 'property': 'wardrobe.color'}]}
        disguised = [{'dimension': 'material', 'target': 'main_subject', 'property': 'wardrobe.color'}]
        self.assertFalse(contracts.property_effects_allowed(lock, ['material'], disguised))

    def test_existing_owners_keep_activation_effects_and_gate_meaning(self):
        old = {p['id']: p for p in json.loads((RUN / 'BASELINE-CATALOG.json').read_text())['profiles']}
        receipt = json.loads((RUN / 'INTEGRATION-MAINTENANCE.json').read_text())
        for row in receipt['existing_owner_enrichments']:
            before, after = old[row['profile_id']], self.profiles[row['profile_id']]
            with self.subTest(profile=after['id']):
                self.assertEqual(before['activation'], after['activation'])
                self.assertEqual(before['semantics']['definition'], after['semantics']['definition'])
                self.assertEqual(before['render_gates'], after['render_gates'])
                self.assertEqual(before['required_evidence_fields'], after['required_evidence_fields'])
                self.assertEqual(before['concept_candidate'].get('affected_properties'), after['concept_candidate'].get('affected_properties'))
                for field in before['required_evidence_fields']:
                    self.assertEqual(before['evidence_requirements'][field]['min_content_words'], after['evidence_requirements'][field]['min_content_words'])
                    self.assertTrue(set(before['evidence_requirements'][field]['must_mention_any']) <= set(after['evidence_requirements'][field]['must_mention_any']))

    def test_empty_scope_domains_and_body_conversion_are_not_hidden_in_appearance(self):
        self.assertFalse({'prop', 'aftermath_trace', 'species_marker'} & set(self.extension['slots']))
        for rows in self.extension['slots'].values():
            for e in rows:
                self.assertTrue(e['affected_properties'])
                self.assertTrue(all(row['target'] == 'main_subject' for row in e['affected_properties']))
        self.assertFalse({'sca_n16', 'sca_n17', 'sca_n18', 'sca_n19', 'sca_n23', 'sca_p17', 'sca_p18'} & set(self.new_ids))


if __name__ == '__main__':
    unittest.main()
