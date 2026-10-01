"""Stable slot eligibility, selected-reference and bound-context regressions."""
from __future__ import annotations

import copy
import random
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/photo-prompt-image-generator/scripts'
sys.path.insert(0, str(SCRIPTS))
import bm25f_retrieval as bm
import prompt_generator as g


class SlotRankRegressionTests(unittest.TestCase):
    def core(self, baseline, **kwargs):
        return {'contract_version': 'photo-authorial-core/v3', 'canonical_sha256': 'a'*64,
                'subject': 'adult woman', 'setting': 'an interior', 'event': 'quiet moment',
                'style': {}, 'visual_priorities': [], 'baseline_prompt_en': baseline,
                'intent_lock': {'locked_dimensions': ['lighting'], 'open_dimensions': ['composition'],
                                'semantic_anchors': []}, **kwargs}

    def rank(self, core, entries, slot='lighting', selected=None, data_extra=None, contract_extra=None):
        data = {'slots': {slot: entries}, **(data_extra or {})}
        index = bm.build_bm25f_index({f'slot:{slot}:{e["id"]}': {'aliases': [e['en']]}
                                      for e in entries}, policy={'fields': {'aliases': {'weight': 4, 'b': .2}}})
        contract = {'adult_allowed': True, 'intent_constraints': {'subject_categories': []},
                    **(contract_extra or {})}
        selected = selected or entries[0]['id']
        return g.candidate_pack_rank_slot_rows(data, slot, [{'id': selected}], selected,
                                               {slot: {'id': selected}}, core, index,
                                               g.authorial_core_retrieval_text(core)[0], contract, {'id': 'generic'})

    def test_selected_below_cutoff_keeps_original_eligibility_without_first_place(self):
        rows = [{'id': 'best'}, {'id': 'next'}, {'id': 'chosen', 'applicability_source': 'sampler_eligible_pool'}]
        before = copy.deepcopy(rows)
        limited = g.candidate_pack_rows_with_selected(rows, 'chosen', 2)
        self.assertEqual([r['id'] for r in limited], ['best', 'chosen'])
        self.assertEqual(limited[-1]['applicability_source'], 'sampler_eligible_pool')
        self.assertEqual(rows, before)
        self.assertEqual(g.candidate_pack_rows_with_selected(rows, 'chosen', 0), [])

    def test_nonhuman_no_people_category_is_not_erased(self):
        for category in ('object', 'food', 'sign', 'animal', 'plant'):
            contract = {'subject_category': category, 'no_people': True}
            got = g.candidate_pack_normalized_slot_contract({}, self.core('An empty room.', subject='an empty room'), contract)
            self.assertEqual(got['subject_category'], category)
            self.assertEqual(contract, {'subject_category': category, 'no_people': True})

    def test_normalization_only_expansion_keeps_narrow_ranking_branch(self):
        entries = [{'id': x, 'en': 'seated ordinary posture'} for x in ('chosen', 'a', 'b')]
        entries += [{'id': 'normalized', 'en': 'seated supporting pose', 'for_any': ['human']}]
        core = self.core('An adult woman is seated.', event='seated posture')
        index = bm.build_bm25f_index({f'slot:body_pose:{e["id"]}': {'aliases':[e['en']]} for e in entries},
                                    policy={'fields': {'aliases': {'weight': 4, 'b': .2}}})
        def hits(_payload, query, **kwargs):
            ids = ['normalized'] if 'global_context' in query else ['normalized','a','b']
            return [{'document_id': f'slot:body_pose:{x}', 'score': 1.0} for x in ids]
        with patch.object(g, 'rank_bm25f', side_effect=hits), \
             patch.object(g, 'reciprocal_rank_fusion', wraps=g.reciprocal_rank_fusion) as fuse:
            rows, _ = g.candidate_pack_rank_slot_rows({'slots': {'body_pose': entries}}, 'body_pose',
                [{'id': x} for x in ('chosen','a','b')], 'chosen', {'body_pose': {'id':'chosen'}},
                core, index, g.authorial_core_retrieval_text(core)[0],
                {'subject_category':'generic','intent_constraints':{}}, {'id':'generic'})
        lanes = fuse.call_args.args[0]
        self.assertEqual(len(lanes), 3, 'normalization-only expansion retains the original ranking lane')
        self.assertEqual(lanes[0], [f'slot:body_pose:{entry_id}' for entry_id in ('chosen', 'a', 'b')])
        limited = g.candidate_pack_rows_with_selected(rows, 'chosen', 2)
        self.assertEqual(len(limited), 2)
        self.assertIn('chosen', [row['id'] for row in limited])

    def test_both_pack_build_paths_preserve_pointer_and_creative_alternative(self):
        entries = [{'id':'chosen', 'en':'soft daylight'}, {'id':'other', 'en':'hard colored spotlight'}]
        data = {'slots': {'lighting': entries}, g.SEMANTIC_INDEX_DATA_KEY: {'bm25f': {}}}
        core = self.core('Soft daylight illuminates the room.')
        result = {'choices': {'lighting': {'id':'chosen'}}, 'provenance': {'creativity': 3}}
        contract = {'candidate_pool_trace': {'lighting': {'eligible_ids': ['chosen','other']}}}
        for score_mode in (True, False):
            trace = {'generation_contract': copy.deepcopy(contract)}
            if score_mode:
                trace['slot_scores'] = [{'slot':'lighting', 'selected':'chosen', 'top':[{'id':'chosen'},{'id':'other'}]}]
            def rank(*args, **kwargs):
                return ([{'id':'other','applicability_status':'eligible','applicability_source':'sampler_eligible_pool'},
                         {'id':'chosen','applicability_status':'eligible','applicability_source':'sampler_eligible_pool'}],
                        {'method': 'test_ranker'})
            candidate_entries = {}
            with patch.object(g, 'semantic_bm25f_payload_from_index', return_value={}), \
                 patch.object(g, 'candidate_pack_rank_slot_rows', side_effect=rank):
                slots = g.candidate_pack_build_slots(data, trace, result, candidate_entries, authorial_core=core)
            self.assertIn(slots['lighting']['selected'], candidate_entries)
            exploration = g.candidate_pack_creative_exploration(result, slots, candidate_entries)
            self.assertIsNotNone(exploration)
            self.assertIn('slot:lighting:other', str(exploration))
            self.assertNotIn('_diagnostics', slots['lighting']['retrieval'])

    def test_pack_normalizes_subject_once_across_slots_without_mutating_sources(self):
        entries = {
            'lighting': [{'id': 'daylight', 'en': 'soft window daylight'}],
            'body_pose': [{'id': 'seated', 'en': 'ordinary seated pose'},
                          {'id': 'supported', 'en': 'seated on a supporting surface',
                           'for_any': ['human']}],
        }
        data = {'slots': entries, g.SEMANTIC_INDEX_DATA_KEY: {'bm25f': {}}}
        index = bm.build_bm25f_index(
            {f'slot:{slot}:{entry["id"]}': {'aliases': [entry['en']]}
             for slot, rows in entries.items() for entry in rows},
            policy={'fields': {'aliases': {'weight': 4, 'b': .2}}},
        )
        core = self.core('An adult woman is seated in soft window daylight.',
                         event='seated on a supporting surface')
        choices = {'lighting': {'id': 'daylight'}, 'body_pose': {'id': 'seated'}}
        contract = {
            'subject_category': 'generic', 'adult_allowed': True,
            'intent_constraints': {'subject_categories': []},
            'candidate_pool_trace': {
                slot: {'eligible_ids': [choice['id']]} for slot, choice in choices.items()
            },
        }
        before = copy.deepcopy((core, contract))
        for score_mode in (True, False):
            with self.subTest(score_mode=score_mode):
                trace = {'generation_contract': contract}
                if score_mode:
                    trace['slot_scores'] = [
                        {'slot': slot, 'selected': choice['id'], 'top': [dict(choice)]}
                        for slot, choice in choices.items()
                    ]
                with patch.object(g, 'semantic_bm25f_payload_from_index', return_value=index), \
                     patch.object(g, 'candidate_pack_normalized_slot_contract',
                                  wraps=g.candidate_pack_normalized_slot_contract) as normalize, \
                     patch.object(g, 'candidate_pack_rank_slot_rows',
                                  wraps=g.candidate_pack_rank_slot_rows) as rank:
                    slots = g.candidate_pack_build_slots(
                        data, trace, {'choices': choices}, {}, authorial_core=core,
                    )
                normalize.assert_called_once_with(data, core, contract)
                self.assertEqual(rank.call_count, 2)
                self.assertEqual(set(slots), set(choices))
                for call in rank.call_args_list:
                    self.assertEqual(call.args[8]['intent_constraints']['subject_categories'], ['human'])
                    self.assertIs(call.kwargs['prior_contract'], contract)
                self.assertEqual((core, contract), before)

    def test_selected_pointer_keeps_atomic_scene_contract_coherent(self):
        rows = g.candidate_pack_rows_with_selected([{'id': 'best'}, {'id': 'chosen'}], 'chosen', 1)
        slots = {'action': {'selected': 'slot:action:chosen',
                 'candidates': [{'id': f'slot:action:{row["id"]}', 'entry_id': row['id'],
                                 'tags': ['workshop_scene']} for row in rows]}}
        policy = {'anchors': [{'slot': 'action', 'variant_strategy': 'atomic_scene',
                              'variant_group': 'workshop', 'pool': ['chosen', 'best']}]}
        contract = g.candidate_pack_scene_contract(policy, slots)
        self.assertIn('workshop_scene', str(contract))
        self.assertIn('selected_entry_id', str(contract))
        self.assertNotIn('best', [c['entry_id'] for c in slots['action']['candidates']])

    def test_normalized_broad_pool_uses_same_two_lane_exposure_rule(self):
        entries = [{'id': 'chosen', 'en': 'ordinary seated pose'},
                   {'id': 'legacy', 'en': 'ordinary seated pose'},
                   {'id': 'a_nohit', 'en': 'unrelated', 'for_any': ['human']},
                   {'id': 'm_lower', 'en': 'seated pose', 'for_any': ['human']},
                   {'id': 'z_best', 'en': 'seated supporting pose', 'for_any': ['human']}]
        core = self.core('An adult woman is seated.', event='seated posture')
        index = bm.build_bm25f_index({f'slot:body_pose:{e["id"]}': {'aliases':[e['en']]} for e in entries},
                                    policy={'fields': {'aliases': {'weight': 4, 'b': .2}}})
        for global_ids, focus_ids, expected in (
            (['legacy', 'z_best'], ['z_best', 'm_lower', 'legacy'], ['chosen', 'z_best', 'legacy']),
            (['legacy'], ['z_best', 'm_lower'], ['chosen', 'z_best']),
        ):
            with self.subTest(global_ids=global_ids, focus_ids=focus_ids):
                def hits(_payload, query, **kwargs):
                    ids = global_ids if 'global_context' in query else focus_ids
                    return [{'document_id': f'slot:body_pose:{x}', 'score': 1.0} for x in ids]
                with patch.object(g, 'rank_bm25f', side_effect=hits):
                    rows, _ = g.candidate_pack_rank_slot_rows({'slots': {'body_pose': entries}}, 'body_pose',
                        [{'id': 'chosen'}], 'chosen', {'body_pose': {'id':'chosen'}}, core, index,
                        g.authorial_core_retrieval_text(core)[0],
                        {'subject_category':'human', 'intent_constraints':{}}, {'id':'generic'})
                self.assertEqual([r['id'] for r in rows], expected)
                self.assertNotIn('m_lower', [r['id'] for r in rows])
                self.assertNotIn('a_nohit', [r['id'] for r in rows])

    def bound_context_core(self, no_people, exclusions=(), interpreted_intent='A factual photographic study of a bronze sculpture'):
        from tests import photo_prompt_fixtures as inputs
        request = 'Photograph a bronze statue in a quiet gallery with no living people.'
        controls = g.creative_controls.resolve(request, context={'subject_category': 'nonhuman', 'no_people': no_people}, seed=7)
        raw = inputs.core(request, subject='a weathered bronze statue', setting='a quiet spacious museum gallery',
                          event='the sculpture stands on a plinth',
                          interpreted_intent=interpreted_intent,
                          visual_priorities=('weathered bronze patina', 'stone gallery plinth', 'subtle overhead illumination'),
                          baseline_prompt_en='A weathered bronze statue stands on a plinth in a quiet gallery. The bronze sculpture has a textured patina, lit by soft overhead illumination. The gallery is otherwise empty, and the camera keeps the complete sculpture and its stone support clearly readable.',
                          anchor_evidence=('bronze sculpture', 'A weathered bronze statue', 'stands on a plinth'),
                          exclusions=exclusions)
        raw['creative_controls_sha256'] = controls['canonical_sha256']
        core = g.normalize_authorial_core(raw, request_envelope=g.normalize_request_envelope(inputs.envelope(request)), creative_control_snapshot=controls)
        return core, controls

    def test_explicit_bound_no_people_context_reaches_existing_guard_without_text_guessing(self):
        core, controls = self.bound_context_core(True)
        before = copy.deepcopy((core, controls))
        self.assertFalse(g.intent_explicitly_excludes_people(core['source_request']))
        constraints = g.authorial_core_generation_constraints(core, creative_control_snapshot=controls)
        self.assertTrue(constraints['no_people'])
        self.assertEqual(constraints['no_people_sources'], ['bound_creative_controls.context.no_people'])
        self.assertEqual(constraints['creative_controls_sha256'], core['creative_controls_sha256'])
        resolved = g.resolve_request_intent_constraints({}, None, {'authorial_core_constraints': constraints}, authorial_core=core)
        self.assertTrue(resolved['no_people'])
        self.assertEqual((core, controls), before)

    def test_false_context_cannot_override_exclusion_or_infer_no_people_from_category(self):
        core, controls = self.bound_context_core(False)
        self.assertFalse(g.authorial_core_generation_constraints(core, creative_control_snapshot=controls)['no_people'])
        core, controls = self.bound_context_core(False, exclusions=('people',))
        self.assertTrue(g.authorial_core_generation_constraints(core, creative_control_snapshot=controls)['no_people'])

    def test_stale_or_mutated_context_cannot_enter_no_people_guard(self):
        core, controls = self.bound_context_core(True)
        stale = g.creative_controls.resolve(core['source_request'], context={'subject_category':'nonhuman','no_people':True}, seed=8)
        with self.assertRaises(ValueError):
            g.authorial_core_generation_constraints(core, creative_control_snapshot=stale)
        mutated = copy.deepcopy(controls)
        mutated['context']['no_people'] = False
        with self.assertRaises(ValueError):
            g.authorial_core_generation_constraints(core, creative_control_snapshot=mutated)
        with self.assertRaises(ValueError):
            g.authorial_core_generation_constraints({**core, 'contract_version':'photo-authorial-core/v2'}, creative_control_snapshot=controls)
        wrong_request = {**core, 'source_request': 'A different request'}
        with self.assertRaises(ValueError):
            g.authorial_core_generation_constraints(wrong_request, creative_control_snapshot=controls)

    def test_no_people_bridge_changes_only_people_fields_without_mutating_source(self):
        core, controls = self.bound_context_core(True)
        original = {'no_people':False, 'subject_categories':['human','animal'],
                    'subject_entry_ids':['person_role','cat'], 'domains':['science_inspection'],
                    'scoped_routes':['user_route'], 'source_text_count':3,
                    'opaque':{'preserve':True}, 'matched':[
                        {'axis':'subject_category','value':'human'},
                        {'axis':'subject_entry','value':'person_role','category':'human'},
                        {'axis':'subject_entry','value':'cat','category':'animal'},
                        {'axis':'domain','value':'science_inspection'}]}
        before = copy.deepcopy(original)
        class StopBeforeSampling(Exception):
            pass
        for intent_source in ('user','default'):
            observed = []
            def capture(*args, **kwargs):
                observed.append(copy.deepcopy(args[3]['intent_constraints']))
                raise StopBeforeSampling()
            with patch.object(g, 'make_semantic_context', return_value={'intent_constraints':original}), \
                 patch.object(g, 'choose_preset', side_effect=capture):
                with self.assertRaises(StopBeforeSampling):
                    g.generate_once({}, random.Random(7), None, ['en'], True, 12, True,
                        selection_mode='semantic', intent='photographic study', intent_source=intent_source,
                        authorial_core=core, creative_control_snapshot=controls)
            after = observed[0]
            self.assertTrue(after['no_people'])
            self.assertEqual(after['subject_categories'], ['animal'])
            self.assertEqual(after['subject_entry_ids'], ['cat'])
            self.assertEqual(after['matched'], before['matched'][2:])
            for key in ('domains','scoped_routes','source_text_count','opaque'):
                self.assertEqual(after[key], before[key])
            self.assertEqual(original, before)

    def test_stable_default_also_repairs_frozen_subject_eligibility(self):
        core = self.core('An adult woman is seated on a supporting surface.', event='seated reading')
        entries = [{'id': 'generic', 'en': 'ordinary seated pose'},
                   {'id': 'seated', 'en': 'seated on a supporting surface', 'for_any': ['human']}]
        extra = {g.QUALITY_LAYERS_DATA_KEY: {
            'intent_routing': {'subject_categories': [{'category': 'human', 'aliases': ['woman']}]}}}
        rows, _ = self.rank(core, entries, slot='body_pose', data_extra=extra)
        self.assertIn('seated', [r['id'] for r in rows])

    def test_stable_pack_restores_missing_sampler_selection(self):
        entries = [{'id': 'chosen', 'en': 'soft daylight'}, {'id': 'other', 'en': 'window light'}]
        data = {'slots': {'lighting': entries}, g.SEMANTIC_INDEX_DATA_KEY: {'bm25f': {}}}
        trace = {'slot_scores': [{'slot': 'lighting', 'selected': 'chosen', 'top': [{'id': 'other'}]}],
                 'generation_contract': {}}
        result = {'choices': {'lighting': {'id': 'chosen'}}}
        def stable_rank(*args, **kwargs):
            return [{'id': 'other'}], {'method': 'test_ranker'}
        with patch.object(g, 'semantic_bm25f_payload_from_index', return_value={}), patch.object(g, 'candidate_pack_rank_slot_rows', side_effect=stable_rank):
            slots = g.candidate_pack_build_slots(data, trace, result, {}, authorial_core=self.core('Soft daylight enters the room.'))
        self.assertIn('slot:lighting:chosen', [r['id'] for r in slots['lighting']['candidates']])
        self.assertNotIn('_diagnostics', slots['lighting']['retrieval'])

    def test_real_policy_direct_human_normalization_and_negative_controls(self):
        import json
        policy_path = SCRIPTS.parent / 'assets/photo_prompt_quality_layers.json'
        data = {g.QUALITY_LAYERS_DATA_KEY: json.loads(policy_path.read_text())}
        core = self.core('An adult woman reads.', subject='An adult woman in everyday clothes.')
        self.assertEqual(g.resolve_request_intent_constraints(data, None, {}, authorial_core=core)['subject_categories'], [])
        normalized = g.candidate_pack_normalized_slot_contract(data, core, {'intent_constraints': {'subject_categories': []}})
        self.assertEqual(normalized['intent_constraints']['subject_categories'], ['human'])
        self.assertEqual(normalized['subject_category'], 'human')
        for subject in ('a statue of an adult woman', 'an adult woman statue',
                        'a photograph of an adult woman', 'an adult female cat',
                        'a mannequin shaped like an adult woman',
                        'An adult woman, depicted on a poster',
                        'An adult man in a framed photograph',
                        'An adult woman, a life-size bronze statue'):
            self.assertEqual(g.candidate_pack_direct_subject_categories(subject), [], subject)
        for subject in ('An adult woman wearing a red jacket', 'An adult man with a cane',
                        'An adult woman in a room with a poster'):
            self.assertEqual(g.candidate_pack_direct_subject_categories(subject), ['human'], subject)
        normalized = g.candidate_pack_normalized_slot_contract(data, core, {'subject_category': 'human', 'intent_constraints': {'no_people': True}})
        self.assertNotIn('human', normalized['intent_constraints']['subject_categories'])
        self.assertNotEqual(normalized['subject_category'], 'human')

    def test_frozen_direct_human_subject_overrides_sampler_robot_without_mutation(self):
        core = self.core('An adult man repairs a bicycle.', subject='an adult man')
        contract = {
            'subject_category': 'robot',
            'intent_constraints': {'subject_categories': [], 'domains': ['workshop']},
            'opaque': {'preserve': True},
        }
        before = copy.deepcopy((core, contract))
        self.assertEqual(g.candidate_pack_direct_subject_categories(core['subject']), ['human'])
        normalized = g.candidate_pack_normalized_slot_contract({}, core, contract)
        self.assertEqual(normalized['subject_category'], 'human')
        self.assertEqual(normalized['intent_constraints']['subject_categories'], ['human'])
        self.assertEqual(normalized['intent_constraints']['domains'], ['workshop'])
        self.assertEqual(normalized['opaque'], {'preserve': True})
        self.assertEqual((core, contract), before)

    def test_stable_newly_human_eligible_entry_still_requires_primary_context(self):
        core = self.core('An adult woman is seated in an ordinary room.', event='a seated resting pose')
        entries = [{'id': 'generic', 'en': 'a seated resting pose'},
                   {'id': 'guarded', 'en': 'a seated resting pose', 'for_any': ['human'],
                    'requires_primary_any_tags': ['missing_scene_context']}]
        rows, _ = self.rank(core, entries, slot='body_pose',
                            contract_extra={'subject_category': 'generic'})
        self.assertNotIn('guarded', [r['id'] for r in rows])

    def test_no_people_block_is_not_bypassed_by_expansion(self):
        core = self.core('An empty room without people.', subject='an empty room')
        entries = [{'id': 'existing', 'en': 'empty space'},
                   {'id': 'person', 'en': 'a seated person', 'for_any': ['human']}]
        with patch.object(g, 'slot_block_reason', return_value='no_people'):
            rows, _ = self.rank(core, entries, slot='body_pose', contract_extra={'no_people': True})
        self.assertNotIn('person', [r['id'] for r in rows])

    def test_direct_human_material_representations_are_not_human(self):
        for subject in ('An adult man in bronze, standing on a plinth', 'An adult woman in marble'):
            self.assertEqual(g.candidate_pack_direct_subject_categories(subject), [], subject)
        self.assertEqual(g.candidate_pack_direct_subject_categories('An adult woman in bronze-colored clothing'), ['human'])


if __name__ == '__main__':
    unittest.main()
