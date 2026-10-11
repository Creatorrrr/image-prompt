"""Real source/fixture checks plus isolated owner projection regressions."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/photo-prompt-image-generator/scripts'))
import prompt_generator as g
import photo_candidate_context as context
import audit_composed_prompt as audit


class PhotoSubjectContextRetrievalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = g.load_json(ROOT / 'skills/photo-prompt-image-generator/assets/photo_prompt_tags.json')

    def fixture(self, key):
        value = json.loads((ROOT / 'tests/fixtures/photo_prompt/subject_context_v1' / key / 'fixture.json').read_text())
        core = g.normalize_authorial_core(value['authorial_core_input'],
            request_envelope=g.normalize_request_envelope(value['request_envelope_input']),
            creative_control_snapshot=value['creative_controls'])
        self.assertEqual(core['canonical_sha256'], value['freeze_receipt']['contracts']['core'])
        return core, value['creative_controls']

    def entry(self, entry_id):
        return next(e for e in self.data['slots']['subject'] if e['id'] == entry_id)

    def test_cup_carrier_is_object_and_edible_subjects_keep_their_category(self):
        self.assertEqual(g.subject_category({'subject': self.entry('coffee_cup')}, self.data), 'object')
        self.assertIn('food', self.entry('coffee_cup')['tags'])
        for entry_id in ('bubble_tea_cup', 'sushi_omakase_plate', 'bibimbap_bowl'):
            self.assertEqual(g.subject_category({'subject': self.entry(entry_id)}, self.data), 'food')
        self.assertEqual(g.subject_category({'subject': self.entry('teacup_vessel_subject')}, self.data), 'object')
        self.assertNotIn('coffee', ' '.join(self.entry('teacup_vessel_subject')['concept_units']))

    def test_declared_candidate_type_precedes_incidental_keyword_classification(self):
        display = self.entry('black_hole_shadow_reconstruction_subject')
        self.assertEqual(g.subject_category({'subject':display},self.data),'sign')
        self.assertEqual(g.subject_category({'subject':self.entry('neon_sign')},self.data),'sign')
        self.assertEqual(g.subject_category({'subject':self.entry('robotic_dog')},self.data),'object')
        self.assertEqual(g.subject_category({'subject':self.entry('fire_f116')},self.data),'object')
        plant = {'id':'scientific_plant','en':'a scientific plant sample','kind':['plant'],'tags':['science']}
        self.assertEqual(g.subject_category({'subject':plant},self.data),'plant')
        self.assertEqual(g.subject_category({'subject':self.entry('bubble_tea_cup')},self.data),'food')
        value=json.loads((ROOT/'tests/fixtures/photo_prompt/slot_retrieval_natural_v1/holdout-10-fantasy-ko/fixture.json').read_text())
        controls=value['creative_controls']
        core=g.normalize_authorial_core(value['authorial_core_input'],
            request_envelope=g.normalize_request_envelope(value['request_envelope_input']),creative_control_snapshot=controls)
        contract,picked=g.frozen_core_context(self.data,core,controls)
        self.assertFalse(g.core_slot_entry_eligible(self.data,core,contract,picked,'subject',display))
        self.assertTrue(g.core_slot_entry_eligible(self.data,core,contract,picked,'subject',self.entry('constructed_golem_subject')))

    def test_actual_special_subtypes_keep_owned_prerequisites(self):
        targets = {
            'golem': 'constructed_golem_subject', 'automaton': 'ceramic_automaton_figure',
            'wyvern': 'heraldic_wyvern_subject', 'earth-diver': 'earth_diver_creation_subject',
            'karaoke': 'karaoke_friend_group', 'rail-switch': 'rail_switch_actuator',
            'living-armor': 'hollow_living_armor_subject', 'legend-teller': 'local_legend_teller_subject',
            'storm-cell': 'cumulonimbus_storm_cell_subject', 'solar-prominence': 'fire_f123',
            'mycelium': 'mycelium_forest_floor', 'seagrass': 'water_w093',
            'doctor': 'doctor_role_model', 'witch': 'witch_practitioner_role_model',
        }
        paths = sorted((ROOT / 'tests/fixtures/photo_prompt/subject_context_v1').glob('*/fixture.json'))
        self.assertEqual(len(paths), 28)
        for path in paths:
            key = path.parent.name
            name = key.removeprefix('context-').rsplit('-', 2)[0]
            core, controls = self.fixture(key)
            contract, picked = g.frozen_core_context(self.data, core, controls)
            with self.subTest(case=key):
                self.assertEqual(g.core_slot_entry_eligible(self.data, core, contract, picked,
                    'subject', self.entry(targets[name])), '-positive-' in key)

    def probe(self, phrase):
        """Source-derived predicate probes, not frozen authorial-pack cases."""
        controls = g.creative_controls.resolve(phrase,
            overrides={'sensual':0,'fetish':0,'surreal':0,'creativity':1},
            context={'subject_category':'human','no_people':False,'explicit_nonsexual':True},seed=17)
        core = {
            'contract_version': 'photo-authorial-core/v3', 'subject': phrase,
            'source_request':phrase, 'creative_controls_sha256':controls['canonical_sha256'],
            'setting': 'beside a plain studio wall', 'event': 'stands beside the wall',
            'style': {'domain': 'general_photo', 'evidence': []},
            'baseline_prompt_en': phrase + ' stands beside a plain studio wall.',
            'visual_priorities': [], 'user_exclusions': [],
            'intent_lock': {'locked_dimensions': [], 'open_dimensions': [], 'semantic_anchors': []},
            'request_binding': {'active_spans': [{'text': phrase}]},
            'semantic_assertions': [{'dimension': 'subject', 'polarity': 'required',
                'affected_dimensions': ['subject'], 'axes': {'subject_category': 'human'},
                'evidence': {'subject_phrase': phrase}}],
        }
        return core, controls

    def test_every_reviewed_role_label_matches_its_own_carrier_and_not_a_background(self):
        roles = [e for e in self.data['slots']['subject'] if {'role','occupation'} & g.entry_context_tokens(e)]
        self.assertTrue(roles)
        for entry in roles:
            own, controls = self.probe('An adult ' + entry['en'])
            _, picked = g.frozen_core_context(self.data, own, controls)
            elsewhere, background_controls = self.probe('One adult person')
            elsewhere['baseline_prompt_en'] += ' A separate printed card says ' + entry['en'] + '.'
            elsewhere['setting'] = 'beside a printed card saying ' + entry['en']
            _, background = g.frozen_core_context(self.data, elsewhere, background_controls)
            with self.subTest(role=entry['id']):
                self.assertTrue(context.primary_context_matches(entry, g.picked_core_context_tokens(picked)))
                self.assertFalse(context.primary_context_matches(entry, g.picked_core_context_tokens(background)))

    def test_subject_field_decoration_cannot_replace_the_typed_primary_carrier(self):
        core, controls = self.fixture('context-automaton-caption-en')
        # An isolated projection probe: the descriptive field includes another
        # actor while the unchanged typed witness still names the cup itself.
        core = copy.deepcopy(core)
        core.pop('canonical_sha256', None)
        core['subject'] += ' with printed words ceramic automaton'
        contract, picked = g.frozen_core_context(self.data, core, controls)
        self.assertNotIn('subject:automaton', g.entry_tags(picked['subject']))
        self.assertFalse(g.core_slot_entry_eligible(self.data, core, contract, picked,
            'subject', self.entry('ceramic_automaton_figure')))
        self.assertTrue(g.core_slot_entry_eligible(self.data, core, contract, picked,
            'subject', self.entry('teacup_vessel_subject')))

    def test_remaining_specific_carriers_need_their_owned_source_meaning(self):
        for entry_id in ('mature_elegant_model', 'androgynous_style_model',
                         'elevator_selfie_creator', 'conlang_conculture_world_reform_subject',
                         'esper_subject', 'soil_e107', 'alien_visitor_subject', 'idol_like_performer',
                         'modern_shaman_performer', 'hacker_operator', 'conworld_cartography_world_border_subject',
                         'former_vessel_spectral_ship_subject', 'bottle_service_waitress', 'mythic_flood_vessel_subject',
                         'drone_swarm_collective'):
            entry = self.entry(entry_id)
            own, controls = self.probe(entry['en'])
            _, picked = g.frozen_core_context(self.data, own, controls)
            elsewhere, controls = self.probe('One adult person')
            elsewhere['setting'] = 'beside a separate printed card saying ' + entry['en']
            _, background = g.frozen_core_context(self.data, elsewhere, controls)
            with self.subTest(carrier=entry_id):
                self.assertTrue(context.primary_context_matches(entry, g.picked_core_context_tokens(picked)))
                self.assertFalse(context.primary_context_matches(entry, g.picked_core_context_tokens(background)))

    def test_generic_human_carrier_preserves_count_and_has_no_special_role(self):
        entry = self.entry('adult_human_body_continuity_subject')
        core, controls = self.probe('Two adult friends')
        contract, picked = g.frozen_core_context(self.data, core, controls)
        self.assertTrue(g.core_slot_entry_eligible(self.data, core, contract, picked, 'subject', entry))
        self.assertEqual(g.subject_category({'subject':entry},self.data), 'human')
        self.assertIn('age_context_only',entry['tags'])
        child, child_controls = self.probe('One child')
        _, child_context = g.frozen_core_context(self.data, child, child_controls)
        self.assertFalse(context.primary_context_matches(entry, g.picked_core_context_tokens(child_context)))
        self.assertEqual(len(entry['relations']),3)
        self.assertIn('each visible head',' '.join(entry['concept_units']))
        self.assertNotIn('alien',' '.join(entry['concept_units']))

    def test_declared_all_and_excluded_subject_conditions_are_enforced(self):
        core, controls = self.fixture('context-golem-caption-ko')
        contract, picked = g.frozen_core_context(self.data, core, controls)
        entry = {'id':'vessel', 'en':'one cup vessel', 'kind':['object'], 'for_all':['cup','object']}
        self.assertTrue(g.core_slot_entry_eligible(self.data, core, contract, picked,'subject',entry))
        entry['for_all'].append('robot')
        self.assertFalse(g.core_slot_entry_eligible(self.data, core, contract, picked,'subject',entry))
        entry['for_all'] = ['cup','object']; entry['not_for'] = ['cup']
        self.assertFalse(g.core_slot_entry_eligible(self.data, core, contract, picked,'subject',entry))

    def test_candidate_facets_cannot_witness_their_own_scene_prerequisite(self):
        core, controls = self.fixture('context-golem-caption-ko')
        data = {'slots':{}, 'facet_vocab':{'subject_kind':['object','robot']}}
        contract, picked = g.frozen_core_context(data, core, controls)
        entry = {'id':'robot', 'en':'one robotic object', 'kind':['object'],
            'facets':{'subject_kind':['robot']}, 'hard_guards':{'requires_facets':['subject_kind:robot']}}
        self.assertFalse(g.core_slot_entry_eligible(data, core, contract, picked,'subject',entry))
        raw, controls = self.fixture('context-automaton-positive-ko')
        raw = copy.deepcopy(raw); raw.pop('canonical_sha256', None)
        raw['semantic_assertions'][0]['axes']['subject_kind'] = 'robot'
        contract, picked = g.frozen_core_context(data, raw, controls)
        self.assertTrue(g.core_slot_entry_eligible(data, raw, contract, picked,'subject',entry))
        raw['semantic_assertions'][0]['axes']['target'] = ['another_actor']
        contract, picked = g.frozen_core_context(data, raw, controls)
        self.assertFalse(g.core_slot_entry_eligible(data, raw, contract, picked,'subject',entry))

    def test_full_applicability_policy_is_bound_even_when_selected_inventory_is_stable(self):
        core, controls = self.fixture('context-golem-caption-ko')
        data = {'slots':{'prop':[{'id':'cup','en':'one plain porcelain cup'}]},
            'candidate_semantic_policy':{'slot_dimensions':{'prop':['subject']}}}
        slots, binding, _ = g.retrieve_core_slots(data, core, controls)
        pack = {'slots':slots, 'core_retrieval':binding,'authorial_core':core,'creative_controls':controls}
        altered = copy.deepcopy(data)
        altered['slot_applicability'] = {'subject_category_overrides':{'coffee_cup':'object'}}
        changed_slots, changed_binding, _ = g.retrieve_core_slots(altered, core, controls)
        self.assertEqual(slots, changed_slots)
        self.assertNotEqual(binding['slot_applicability_sha256'], changed_binding['slot_applicability_sha256'])
        self.assertTrue(audit.audit_core_retrieval(pack, altered))


class PhotoOwnedFocusProjectionTests(unittest.TestCase):
    def core(self, case):
        phrases = [a['prompt_evidence'] for a in case['anchors']] + [case['assertion_evidence']]
        return {'contract_version':'photo-authorial-core/v3',
            'subject':'One primary carrier', 'setting':'beside a separate background object',
            'event':'remains visible beside the background', 'style':{}, 'visual_priorities':[],
            'baseline_prompt_en':'. '.join(phrases), 'user_exclusions':case['user_exclusions'],
            'request_binding':{'active_spans':[]},
            'intent_lock':{'semantic_anchors':copy.deepcopy(case['anchors'])},
            'semantic_assertions':[{'dimension':case['dimensions'][0], 'polarity':'advisory',
                'axes':{}, 'evidence':{'background_phrase':case['assertion_evidence']}}]}

    def test_frozen_bilingual_owner_queries_and_unrelated_property_absence(self):
        cases = json.loads((ROOT/'tests/fixtures/photo_prompt/owner_focus_v1.json').read_text())['cases']
        self.assertEqual(len(cases), 12)
        for case in cases:
            core = self.core(case); before = copy.deepcopy(core)
            data = {'slots':{case['slot']:[]},
                'candidate_semantic_policy':{'slot_dimensions':{case['slot']:case['dimensions']}}}
            queries, fields = g.core_slot_focus_queries(data,core,case['slot'])
            with self.subTest(case=case['id']):
                self.assertEqual(queries,case['expected_queries'])
                self.assertEqual(core,before)
                if queries:self.assertEqual(fields,['intent_lock.semantic_anchors'])
                else:self.assertEqual(fields,[])

    def test_explicitly_same_owner_assertion_keeps_its_related_literal_evidence(self):
        case = {'dimensions':['lighting'], 'anchors':[{'dimension':'lighting','target':'key_light',
            'property':'source.direction','prompt_evidence':'the window lights the cup from the right'}],
            'assertion_evidence':'the same light leaves a shadow toward the left','user_exclusions':[]}
        core=self.core(case)
        core['semantic_assertions'][0]['axes']={'target':'key_light','property':'source.response'}
        data={'candidate_semantic_policy':{'slot_dimensions':{'light_direction':['lighting']}}}
        queries, fields=g.core_slot_focus_queries(data,core,'light_direction')
        self.assertEqual(queries,['the window lights the cup from the right',case['assertion_evidence']])
        self.assertEqual(fields,['intent_lock.semantic_anchors','semantic_assertions'])
        core['semantic_assertions'][0]['axes']['target']=['other_owner']
        self.assertEqual(g.core_slot_focus_queries(data,core,'light_direction')[0],queries[:1])

    def test_unscoped_anchor_cannot_bypass_an_unrelated_typed_property(self):
        cases = json.loads((ROOT/'tests/fixtures/photo_prompt/owner_focus_v1.json').read_text())['cases']
        for case in cases:
            if 'height_cannot_supply_direction' not in case['id']:
                continue
            core = self.core(case)
            core['intent_lock']['semantic_anchors'].append({
                'dimension':'lighting', 'prompt_evidence':case['assertion_evidence']})
            data = {'candidate_semantic_policy':{'slot_dimensions':{case['slot']:case['dimensions']}}}
            with self.subTest(case=case['id']):
                self.assertEqual(g.core_slot_focus_queries(data, core, case['slot']), ([], []))

    def test_generic_effect_dimension_fallback_keeps_its_grounded_carrier_query(self):
        data = {'slots':{'prop':[{'id':'cup','affected_dimensions':['subject','material']}]},
            'candidate_semantic_policy':{'slot_dimensions':{'prop':[]}}}
        core = {'contract_version':'photo-authorial-core/v3', 'user_exclusions':[],
            'intent_lock':{'semantic_anchors':[
                {'dimension':'subject','prompt_evidence':'a blue porcelain teacup'},
                {'dimension':'material','target':'cup','property':'surface.material',
                    'prompt_evidence':'the cup is porcelain'}]}, 'semantic_assertions':[]}
        self.assertEqual(g.core_slot_focus_queries(data,core,'prop'),
            (['a blue porcelain teacup'],['intent_lock.semantic_anchors']))


if __name__ == '__main__':
    unittest.main()
