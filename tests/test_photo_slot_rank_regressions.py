"""Regression coverage for review-proven retrieval integration failures."""
import copy
import random
import unittest
from unittest.mock import patch
from tests import test_photo_slot_retrieval_evidence as fixture

g, bm = fixture.g, fixture.bm


class SlotRankRegressionTests(unittest.TestCase):
    def setUp(self):
        self.helper = fixture.SlotRetrievalEvidenceTests()

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
            got = g.candidate_pack_normalized_slot_contract({}, self.helper.core('An empty room.', subject='an empty room'), contract)
            self.assertEqual(got['subject_category'], category)
            self.assertEqual(contract, {'subject_category': category, 'no_people': True})

    def test_conflict_is_diagnostic_demotion_not_deletion(self):
        rows, metadata = self.helper.rank(self.helper.core('The lamp is switched off.'),
            [{'id': 'lamp', 'en': 'The lamp emits light.'}])
        self.assertEqual([r['id'] for r in rows], ['lamp'])
        self.assertEqual(metadata['_diagnostics']['conflict_demotions']['lamp'], ['inactive_entity_as_active_source'])
        self.assertNotIn('conflict_rejections', metadata['_diagnostics'])

    def test_forced_critical_atomic_pools_are_not_reranked(self):
        entries = [{'id': 'chosen', 'en': 'ordinary light'}, {'id': 'window', 'en': 'soft window light'}]
        for kind in ('forced', 'forced_slots', 'critical', 'atomic'):
            contract = {'candidate_pool_trace': {'lighting': {'forced': kind == 'forced'}},
                        'forced_slots': ['lighting'] if kind == 'forced_slots' else []}
            with patch.object(g, 'soft_anchor_critical_slot', return_value=kind == 'critical'), \
                 patch.object(g, 'soft_anchor_atomic_pool_for_slot', return_value=['chosen'] if kind == 'atomic' else []), \
                 patch.object(g, 'rank_bm25f', side_effect=AssertionError('protected pool reached ranker')):
                rows, metadata = self.helper.rank(self.helper.core('Soft window light.'), entries, contract_extra=contract)
            self.assertEqual([r['id'] for r in rows], ['chosen'])
            self.assertIsNone(metadata)

    def test_normalization_only_expansion_does_not_discard_sampler_alternatives(self):
        entries = [{'id': x, 'en': 'seated ordinary posture'} for x in ('chosen', 'a', 'b')]
        entries += [{'id': 'normalized', 'en': 'seated supporting pose', 'for_any': ['human']}]
        core = self.helper.core('An adult woman is seated.', event='seated posture')
        index = bm.build_bm25f_index({f'slot:body_pose:{e["id"]}': {'aliases':[e['en']]} for e in entries},
                                    policy={'fields': {'aliases': {'weight': 4, 'b': .2}}})
        def hits(_payload, query, **kwargs):
            ids = ['normalized'] if 'global_context' in query else ['normalized','a','b']
            return [{'document_id': f'slot:body_pose:{x}', 'score': 1.0} for x in ids]
        with patch.object(g, 'rank_bm25f', side_effect=hits):
            rows, metadata = g.candidate_pack_rank_slot_rows({'slots': {'body_pose': entries}}, 'body_pose',
                [{'id': x} for x in ('chosen','a','b')], 'chosen', {'body_pose': {'id':'chosen'}},
                core, index, g.authorial_core_retrieval_text(core)[0],
                {'subject_category':'generic','intent_constraints':{}}, {'id':'generic'})
        self.assertEqual(set(r['id'] for r in rows), {'chosen','a','b','normalized'})
        self.assertEqual(metadata['_diagnostics']['prior_eligible_expansion_count'], 0)
        self.assertEqual(metadata['_diagnostics']['normalization_only_expansion_count'], 1)

    def test_both_pack_build_paths_preserve_pointer_and_creative_alternative(self):
        entries = [{'id':'chosen', 'en':'soft daylight'}, {'id':'other', 'en':'hard colored spotlight'}]
        data = {'slots': {'lighting': entries}, g.SEMANTIC_INDEX_DATA_KEY: {'bm25f': {}}}
        core = self.helper.core('Soft daylight illuminates the room.')
        result = {'choices': {'lighting': {'id':'chosen'}}, 'provenance': {'creativity': 3}}
        contract = {'candidate_pool_trace': {'lighting': {'eligible_ids': ['chosen','other']}}}
        for score_mode in (True, False):
            trace = {'generation_contract': copy.deepcopy(contract)}
            if score_mode:
                trace['slot_scores'] = [{'slot':'lighting', 'selected':'chosen', 'top':[{'id':'chosen'},{'id':'other'}]}]
            def rank(*args):
                return ([{'id':'other','applicability_status':'eligible','applicability_source':'sampler_eligible_pool'},
                         {'id':'chosen','applicability_status':'eligible','applicability_source':'sampler_eligible_pool'}],
                        {'policy':'evidence-union','experimental':True,'_diagnostics':{}})
            candidate_entries = {}
            with patch.object(g, 'semantic_bm25f_payload_from_index', return_value={}), \
                 patch.object(g, 'candidate_pack_rank_slot_rows', side_effect=rank):
                slots = g.candidate_pack_build_slots(data, trace, result, candidate_entries, authorial_core=core)
            self.assertIn(slots['lighting']['selected'], candidate_entries)
            exploration = g.candidate_pack_creative_exploration(result, slots, candidate_entries)
            self.assertIsNotNone(exploration)
            self.assertIn('slot:lighting:other', str(exploration))
            self.assertNotIn('_diagnostics', slots['lighting']['retrieval'])

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



    def test_dense_lane_reuses_only_matching_cached_scene_vector(self):
        core = self.helper.core('Soft window light enters the room.')
        entries = [{'id': 'chosen', 'en': 'ordinary window light'},
                   {'id': 'window', 'en': 'soft window light'}]
        query = g.authorial_core_retrieval_text(core)[0]
        space = {'provider':'gemini', 'embedding_model':'test-space-a', 'embedding_dimensions':2}
        query_hash = g.candidate_pack_slot_vector_key(space, query)
        for key, expected in ((query_hash, 2), ('wrong-query-hash', 0)):
            extra = {g.SLOT_QUERY_VECTORS_DATA_KEY: {key: [1.0, 0.0]},
                     g.SEMANTIC_INDEX_DATA_KEY: {**space, 'entries': {
                         'slot:lighting:chosen': {'vector': [0.0, 1.0]},
                         'slot:lighting:window': {'vector': [1.0, 0.0]}}}}
            before = copy.deepcopy(extra)
            rows, metadata = self.helper.rank(core, entries, data_extra=extra)
            self.assertEqual(metadata['_diagnostics']['embedding_lane_count'], expected)
            self.assertEqual(extra, before)
            self.assertEqual({r['id'] for r in rows}, {'chosen', 'window'})

    def test_dense_lane_ignores_incompatible_cached_vector_dimensions(self):
        core = self.helper.core('Soft window light enters the room.')
        space = {'provider':'gemini', 'embedding_model':'test-space-a', 'embedding_dimensions':2}
        query_hash = g.candidate_pack_slot_vector_key(space, g.authorial_core_retrieval_text(core)[0])
        extra = {g.SLOT_QUERY_VECTORS_DATA_KEY: {query_hash: [1.0, 0.0]},
                 g.SEMANTIC_INDEX_DATA_KEY: {**space, 'entries': {'slot:lighting:chosen': {'vector': [1.0]}}}}
        _, metadata = self.helper.rank(core, [{'id':'chosen','en':'soft window light'}], data_extra=extra)
        self.assertEqual(metadata['_diagnostics']['embedding_lane_count'], 0)


    def test_normalized_broad_pool_tail_is_relevance_ordered_and_focus_supported(self):
        entries = [{'id': 'chosen', 'en': 'ordinary seated pose'},
                   {'id': 'legacy', 'en': 'ordinary seated pose'},
                   {'id': 'a_nohit', 'en': 'unrelated', 'for_any': ['human']},
                   {'id': 'm_lower', 'en': 'seated pose', 'for_any': ['human']},
                   {'id': 'z_best', 'en': 'seated supporting pose', 'for_any': ['human']}]
        core = self.helper.core('An adult woman is seated.', event='seated posture')
        index = bm.build_bm25f_index({f'slot:body_pose:{e["id"]}': {'aliases':[e['en']]} for e in entries},
                                    policy={'fields': {'aliases': {'weight': 4, 'b': .2}}})
        def hits(_payload, query, **kwargs):
            ids = ['legacy'] if 'global_context' in query else ['z_best', 'legacy', 'm_lower']
            return [{'document_id': f'slot:body_pose:{x}', 'score': 1.0} for x in ids]
        with patch.object(g, 'rank_bm25f', side_effect=hits):
            rows, metadata = g.candidate_pack_rank_slot_rows({'slots': {'body_pose': entries}}, 'body_pose',
                [{'id': 'chosen'}], 'chosen', {'body_pose': {'id':'chosen'}}, core, index,
                g.authorial_core_retrieval_text(core)[0],
                {'subject_category':'human', 'intent_constraints':{}}, {'id':'generic'})
        self.assertEqual([r['id'] for r in rows], ['chosen', 'legacy', 'z_best', 'm_lower'])
        self.assertEqual(metadata['_diagnostics']['prior_eligible_expansion_count'], 1)

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


    def test_cached_vectors_are_space_bound_and_memory_bounded(self):
        space = {'provider':'gemini', 'embedding_model':'test-space-a', 'embedding_dimensions':2}
        data = {}
        g.cache_candidate_pack_slot_vector(data, space, 'same query', [1.0, 0.0])
        key = g.candidate_pack_slot_vector_key(space, 'same query')
        for changed in ({**space, 'embedding_model':'test-space-b'},
                        {**space, 'provider':'other'}, {**space, 'embedding_dimensions':3}):
            self.assertNotIn(g.candidate_pack_slot_vector_key(changed, 'same query'), data[g.SLOT_QUERY_VECTORS_DATA_KEY])
        self.assertIsNone(g.candidate_pack_slot_vector_key({}, 'same query'))
        for n in range(70):
            g.cache_candidate_pack_slot_vector(data, space, f'query-{n}', [1.0, 0.0])
        self.assertEqual(len(data[g.SLOT_QUERY_VECTORS_DATA_KEY]), 64)
        self.assertNotIn(key, data[g.SLOT_QUERY_VECTORS_DATA_KEY])
        self.assertIn(g.candidate_pack_slot_vector_key(space, 'query-69'), data[g.SLOT_QUERY_VECTORS_DATA_KEY])


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


if __name__ == '__main__':
    unittest.main()
