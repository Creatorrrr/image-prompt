"""Owned iconographic alternatives preserve complete forms and remain optional."""
from __future__ import annotations

import json
import sys
import unittest
from unittest.mock import patch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as pg
import photo_candidate_semantics as candidate_semantics
from tests import photo_prompt_fixtures as fixtures


class ReligionIconographyAlternativesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        assets = SKILL / 'assets'
        cls.extension = json.loads((assets / 'photo_prompt_religion_iconography_extension.json').read_text())
        cls.registry = pg.load_visual_obligation_registry(assets / 'photo_prompt_visual_obligations.json')
        cls.profiles = {p['id']: p for p in cls.registry['profiles']}
        cls.index = pg.load_visual_profile_index(assets / 'photo_prompt_visual_profile_index.json', cls.registry)
        cls.data = pg.load_json(assets / 'photo_prompt_tags.json')

    def resolution(self, text, *, source='user_requirement', polarity='required', vector=None):
        return pg.resolve_visual_profile_hits(self.registry,
            [{'source': source, 'text': text, 'polarity': polarity}],
            visual_profile_index=self.index, query_text=text, query_vector=vector,
            adult_context=True)

    @staticmethod
    def hard(result):
        return {x['profile_id'] for x in result['hits'] if x['hard_eligible']}

    def test_bare_names_and_polysemy_do_not_fix_a_variant(self):
        for text in ('Chakrasamvara', '두르가', 'Durga', 'Ganesha', '나가', 'Cerberus',
                     'Rebis', 'Maat', 'a halo around a camera highlight',
                     'an ordinary portrait of an adult with a short bob and brown eyes',
                     'a ceramic teacup beside an illustrated bird'):
            with self.subTest(text=text):
                self.assertFalse({p for p in self.hard(self.resolution(text)) if p.startswith('ri_')})

    def test_complete_form_requires_request_evidence_and_respects_negation(self):
        for pid in ('ri_chimera_topology', 'ri_head_halo', 'ri_body_mandorla',
                    'ri_daoist_robe_xuanwu', 'ri_sleipnir_eight_legs'):
            p = self.profiles[pid]
            exact = p['activation']['exact_terms'][0]
            self.assertIn(pid, self.hard(self.resolution(exact)))
            self.assertNotIn(pid, self.hard(self.resolution('without ' + exact)))
            self.assertNotIn(pid, self.hard(self.resolution(exact, polarity='excluded')))
            self.assertNotIn(pid, self.hard(self.resolution(exact,
                source='authorial_core_interpretation', polarity='advisory')))

    def test_all_components_required_including_owned_junction_and_count(self):
        new = [p for p in self.profiles.values() if p['id'].startswith('ri_')]
        self.assertEqual(len(new), 54)
        for p in new:
            groups = p['semantics']['component_semantics']['groups']
            canonical = [g['any_terms'][0] for g in groups]
            self.assertIsNotNone(pg.candidate_pack_visual_component_match(p, '; '.join(canonical)), p['id'])
            for omit in range(len(canonical)):
                partial = '; '.join(t for i, t in enumerate(canonical) if i != omit)
                with self.subTest(profile=p['id'], missing=groups[omit]['id']):
                    self.assertIsNone(pg.candidate_pack_visual_component_match(p, partial))

    def test_new_korean_component_alternatives_preserve_the_complete_form(self):
        for pid in ('ri_head_halo', 'ri_body_mandorla', 'ri_chimera_topology', 'ri_daoist_robe_xuanwu'):
            groups = self.profiles[pid]['semantics']['component_semantics']['groups']
            alternatives = [g['any_terms'][1] for g in groups]
            self.assertIsNotNone(pg.candidate_pack_visual_component_match(self.profiles[pid], '; '.join(alternatives)))
            for omit in range(len(alternatives)):
                self.assertIsNone(pg.candidate_pack_visual_component_match(self.profiles[pid],
                    '; '.join(t for i, t in enumerate(alternatives) if i != omit)))

    def test_existing_heart_owner_remains_feather_specific(self):
        p = self.profiles['egyptian_heart_weighing_judgment']
        sem = p['semantics']['component_semantics']
        self.assertEqual(sem['required_group_ids'], ['deceased_subject', 'heart_feather_balance',
            'anubis_attendance', 'thoth_recording', 'judgment_consequence'])
        groups = sem['groups']
        alternatives = [g['any_terms'][-1] for g in groups]
        self.assertIsNotNone(pg.candidate_pack_visual_component_match(p, '; '.join(alternatives)))
        alternatives[1] = 'a heart on one balance pan and a small seated Maat figure on the opposite pan'
        self.assertIsNone(pg.candidate_pack_visual_component_match(p, '; '.join(alternatives)))
        self.assertNotIn('ri_heart_maat_figure', self.profiles)

    def test_muqarnas_and_griffin_keep_existing_owners(self):
        self.assertIn('pf_muqarnas', self.profiles)
        self.assertIn('griffin_eagle_lion_topology', self.profiles)
        self.assertNotIn('ri_muqarnas_cells', self.profiles)
        self.assertNotIn('ri_griffin_eagle_lion', self.profiles)
        p = self.profiles['pf_muqarnas']
        self.assertIsNone(pg.candidate_pack_visual_component_match(p,
            'flat geometric star tiles painted on a ceiling'))

    def test_layout_candidates_cannot_declare_anatomy_identity_or_prop_effects(self):
        entries = self.extension['slots']['composition']
        self.assertEqual(len(entries), 80)
        for e in entries:
            with self.subTest(candidate=e['id']):
                self.assertEqual(e['affected_dimensions'], ['composition'])
                self.assertEqual(e['affected_properties'], [
                    {'dimension': 'composition', 'target': 'image_plane', 'property': 'layout'}])
                self.assertTrue(e['relations'])
                self.assertEqual(candidate_semantics.semantic_source(e, 'composition',
                    self.data['candidate_semantic_policy'])['adoption'], 'optional')
        self.assertNotIn('prop', self.extension['slots'])
        self.assertEqual(self.data['candidate_semantic_policy']['slot_dimensions']['prop'], [])

    def test_frozen_ordinary_portrait_cannot_admit_unrequested_iconography(self):
        raw = fixtures.core('An ordinary adult beauty portrait in a quiet photographic studio.',
            subject='one adult portrait subject', setting='a quiet photographic studio',
            event='the adult holds a still seated portrait pose')
        controls = pg.creative_controls.resolve(raw['source_request'],
            overrides={'sensual': 0, 'fetish': 0, 'surreal': 0, 'creativity': 1}, seed=11)
        raw['creative_controls_sha256'] = controls['canonical_sha256']
        core = pg.normalize_authorial_core(raw,
            request_envelope=pg.normalize_request_envelope(fixtures.envelope(raw['source_request'])),
            creative_control_snapshot=controls)
        contract, picked = pg.frozen_core_context(self.data, core, controls)
        for entry in self.extension['slots']['composition']:
            self.assertFalse(pg.core_slot_entry_eligible(self.data, core, contract, picked,
                'composition', entry), entry['id'])
        # A distinctive core-owned represented form can admit its layout aid.
        core['subject'] = 'one depicted chimera with a lion body, a goat on its back and a snake tail'
        contract, picked = pg.frozen_core_context(self.data, core, controls)
        entry = next(e for e in self.extension['slots']['composition']
            if e['id'] == 'ri_chimera_topology_readable_composition')
        self.assertTrue(pg.core_slot_entry_eligible(self.data, core, contract, picked,
            'composition', entry))

    def test_pending_variants_have_no_hard_profile_link(self):
        by_id = {b['id']: b for b in self.extension['visual_semantics']}
        for uid in ('heart_maat_figure', 'cerberus_two_heads', 'minotaur_bull_head',
                    'baphomet_levi_scope', 'ngalyod_regional'):
            b = by_id['ri_' + uid]
            self.assertTrue(b['candidate_only'])
            self.assertNotIn('hard_profile_id', b)
            self.assertNotIn('ri_' + uid, self.profiles)

    def test_existing_candidate_context_preserves_all_prior_owned_fields(self):
        filenames = tuple(name for name in pg.RESEARCH_EXTENSION_FILENAMES
            if name != 'photo_prompt_religion_iconography_extension.json')
        with patch.object(pg, 'RESEARCH_EXTENSION_FILENAMES', filenames):
            before = pg.load_json(SKILL / 'assets/photo_prompt_tags.json')
        for slot, updates in self.extension['existing_slot_context_extensions'].items():
            prior = {row['id']: row for row in before['slots'][slot]}
            current = {row['id']: row for row in self.data['slots'][slot]}
            for candidate_id, update in updates.items():
                original, enriched = prior[candidate_id], current[candidate_id]
                with self.subTest(candidate=candidate_id):
                    self.assertEqual({k: v for k, v in original.items() if k != 'paraphrases'},
                        {k: v for k, v in enriched.items() if k != 'paraphrases'})
                    self.assertTrue(set(original.get('paraphrases', [])) <= set(enriched['paraphrases']))
                    self.assertTrue(set(update['paraphrases']) <= set(enriched['paraphrases']))

    def test_semantic_only_paraphrase_does_not_harden_a_profile(self):
        pid = 'ri_chimera_topology'
        vector = self.index['entries'][pid]['vector']
        result = self.resolution('a leonine body with a horned goat head growing from the same back and an ophidian head at the end of its tail', vector=vector)
        self.assertNotIn(pid, self.hard(result))
        self.assertIn(pid, {x['profile_id'] for x in result['hits']})

    def test_unrelated_even_embedding_close_context_cannot_expose_new_profiles(self):
        # Lexical or vector similarity is insufficient without sense-specific
        # represented-component evidence. A forced nearest vector is deliberate.
        for pid in ('ri_durga_four', 'ri_chakra_white2', 'ri_chimera_topology'):
            result = self.resolution('a ceramic teacup beside an illustrated bird',
                vector=self.index['entries'][pid]['vector'])
            self.assertFalse({x['profile_id'] for x in result['hits']
                if x['profile_id'].startswith('ri_')})

    def test_scoped_alternatives_are_optional_discovery_in_an_agent_core(self):
        for pid, phrase in (
            ('ri_daoist_robe_xuanwu', 'tortoise-and-coiled-snake emblem'),
            ('ri_body_mandorla', 'whole-body mandorla'),
            ('ri_head_halo', 'head nimbus'),
            ('ri_siren_human_bird', 'human-headed avian Greek siren'),
            ('ri_chimera_topology', 'lion-goat-snake chimera')):
            result = self.resolution(phrase, source='authorial_core_interpretation',
                polarity='advisory', vector=self.index['entries'][pid]['vector'])
            self.assertNotIn(pid, self.hard(result))
            self.assertIn(pid, {x['profile_id'] for x in result['hits']})

    def test_owned_junction_paraphrases_are_discovered_from_runtime_baseline(self):
        text = ('A female human head and neck join directly into one feather-covered bird trunk; '
            'its wings and two bird legs belong to that same Greek siren. A lion-bodied chimera '
            'stands nearby; its goat head and neck grow upward from the middle of that same back '
            'and its connected tail terminates in a snake head.')
        result = pg.resolve_visual_profile_hits(self.registry,
            [{'source': 'authorial_core_baseline', 'text': text, 'polarity': 'advisory'}],
            visual_profile_index=self.index, query_text=text,
            query_fields={'subject': text, 'event': text}, adult_context=True)
        selected = {'ri_siren_human_bird', 'ri_chimera_topology'}
        self.assertTrue(selected <= {x['profile_id'] for x in result['hits']})
        self.assertFalse(selected & self.hard(result))


if __name__ == '__main__':
    unittest.main()
