from __future__ import annotations
import copy
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/photo-prompt-image-generator/scripts'
sys.path.insert(0, str(SCRIPTS))
import bm25f_retrieval as bm
import prompt_generator as g
import slot_retrieval as evidence


class SlotRetrievalEvidenceTests(unittest.TestCase):
    def core(self, baseline, **kwargs):
        return {'contract_version': 'photo-authorial-core/v3', 'canonical_sha256': 'a'*64,
                'subject': 'adult woman', 'setting': 'an interior', 'event': 'quiet moment',
                'style': {}, 'visual_priorities': [], 'baseline_prompt_en': baseline,
                'intent_lock': {'locked_dimensions': ['lighting'], 'open_dimensions': ['composition'],
                                'semantic_anchors': []}, **kwargs}

    def rank(self, core, entries, slot='lighting', selected=None, data_extra=None, contract_extra=None):
        data = {'slots': {slot: entries}, g.SLOT_RETRIEVAL_POLICY_DATA_KEY: 'evidence-union', **(data_extra or {})}
        index = bm.build_bm25f_index({f'slot:{slot}:{e["id"]}': {'aliases': [e['en']]}
                                      for e in entries}, policy={'fields': {'aliases': {'weight': 4, 'b': .2}}})
        contract = {'adult_allowed': True, 'intent_constraints': {'subject_categories': []},
                    **(contract_extra or {})}
        selected = selected or entries[0]['id']
        return g.candidate_pack_rank_slot_rows(data, slot, [{'id': selected}], selected,
                                               {slot: {'id': selected}}, core, index,
                                               g.authorial_core_retrieval_text(core)[0], contract, {'id': 'generic'})

    def test_risky_union_requires_explicit_opt_in_and_stable_keeps_sampler_order(self):
        core = self.core('Soft window light enters from the left. The lamp is switched off.', setting='soft window light')
        entries = [{'id': 'active', 'en': 'The lamp produces a localized light pool.'},
                   {'id': 'window', 'en': 'soft window light'}]
        stable, metadata = self.rank(core, entries, data_extra={g.SLOT_RETRIEVAL_POLICY_DATA_KEY: 'stable'})
        self.assertEqual(stable[0]['id'], 'active')
        self.assertFalse(metadata['experimental'])
        self.assertEqual(metadata['policy'], 'stable')
        experiment, metadata = self.rank(core, entries)
        self.assertEqual([r['id'] for r in experiment], ['window', 'active'])
        self.assertTrue(metadata['experimental'])

    def test_stable_default_also_repairs_frozen_subject_eligibility(self):
        core = self.core('An adult woman is seated on a supporting surface.', event='seated reading')
        entries = [{'id': 'generic', 'en': 'ordinary seated pose'},
                   {'id': 'seated', 'en': 'seated on a supporting surface', 'for_any': ['human']}]
        extra = {g.SLOT_RETRIEVAL_POLICY_DATA_KEY: 'stable', g.QUALITY_LAYERS_DATA_KEY: {
            'intent_routing': {'subject_categories': [{'category': 'human', 'aliases': ['woman']}]}}}
        rows, metadata = self.rank(core, entries, slot='body_pose', data_extra=extra)
        self.assertIn('seated', [r['id'] for r in rows])
        self.assertEqual(metadata['_diagnostics']['normalized_subject_categories'], ['human'])

    def test_stable_pack_restores_missing_sampler_selection(self):
        entries = [{'id': 'chosen', 'en': 'soft daylight'}, {'id': 'other', 'en': 'window light'}]
        data = {'slots': {'lighting': entries}, g.SEMANTIC_INDEX_DATA_KEY: {'bm25f': {}}}
        trace = {'slot_scores': [{'slot': 'lighting', 'selected': 'chosen', 'top': [{'id': 'other'}]}],
                 'generation_contract': {}}
        result = {'choices': {'lighting': {'id': 'chosen'}}}
        def stable_rank(*args, **kwargs):
            return [{'id': 'other'}], {'policy': 'stable', 'experimental': False, '_diagnostics': {}}
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
            self.assertEqual(evidence.direct_subject_categories(subject), [], subject)
        for subject in ('An adult woman wearing a red jacket', 'An adult man with a cane',
                        'An adult woman in a room with a poster'):
            self.assertEqual(evidence.direct_subject_categories(subject), ['human'], subject)
        normalized = g.candidate_pack_normalized_slot_contract(data, core, {'subject_category': 'human', 'intent_constraints': {'no_people': True}})
        self.assertNotIn('human', normalized['intent_constraints']['subject_categories'])
        self.assertNotEqual(normalized['subject_category'], 'human')

    def test_stable_newly_human_eligible_entry_still_requires_primary_context(self):
        core = self.core('An adult woman is seated in an ordinary room.', event='a seated resting pose')
        entries = [{'id': 'generic', 'en': 'a seated resting pose'},
                   {'id': 'guarded', 'en': 'a seated resting pose', 'for_any': ['human'],
                    'requires_primary_any_tags': ['missing_scene_context']}]
        rows, _ = self.rank(core, entries, slot='body_pose', data_extra={g.SLOT_RETRIEVAL_POLICY_DATA_KEY: 'stable'},
                            contract_extra={'subject_category': 'generic'})
        self.assertNotIn('guarded', [r['id'] for r in rows])

    def test_frozen_projection_keeps_state_relations_locks_and_ignores_audit(self):
        core = self.core('Soft window light enters from the left. The lamp is switched off.')
        before = copy.deepcopy(core)
        meaning = evidence.project(core, 'lighting')
        core['precore_feature_selection'] = {'malicious': 'neon flash flash flash'}
        self.assertEqual(meaning, evidence.project(core, 'lighting'))
        self.assertEqual(meaning['locked_dimensions'], ['lighting'])
        self.assertEqual(meaning['entities'][0]['entity'], 'lamp')
        text, fields = g.candidate_pack_slot_focus_text(core, 'lighting')
        self.assertIn('Soft window light', text)
        self.assertNotIn('neon', text)
        self.assertIn('baseline_prompt_en', fields)
        core.pop('precore_feature_selection')
        self.assertEqual(core, before)

    def test_spatial_off_and_surface_paint_are_not_state_or_depiction(self):
        for baseline in ('The lamp is off-white and shines onto the table.',
                         'The lamp is off camera and lights the actor.',
                         'The lamp is off-camera and lights the actor.'):
            self.assertEqual(evidence.inactive_entities(baseline), [])
            self.assertEqual(evidence.conflict_reasons(self.core(baseline),
                {'en': 'The lamp illuminates the face.'}, 'lighting'), [])
        meaning = evidence.project(self.core('Warm light falls on the painted ceramic mug.'), 'lighting')
        self.assertTrue(evidence.positive_evidence(meaning))
        self.assertEqual(evidence.inactive_entities('The lamp is off.')[0]['entity'], 'lamp')
        self.assertEqual(evidence.inactive_entities('A switched-off brass lamp stands on the table.')[0]['entity'], 'lamp')

    def test_inactive_state_does_not_transfer_between_entities_or_invert_negation(self):
        cases = [
            ('The desk lamp is switched off. The ceiling lamp illuminates the room.', 'The ceiling lamp illuminates the room.'),
            ('The lamp is switched off beneath sunlight.', 'The lamp casts a sharp shadow on the table.'),
            ('The lamp is switched off.', 'The lamp does not emit light.'),
            ('The lamp is switched off.', 'The lamp emits no light.'),
            ('The lamp is switched off.', 'The lamp produces no illumination.'),
            ('The brass table lamp is switched off.', 'The wall lamp illuminates the room.'),
        ]
        for baseline, label in cases:
            self.assertEqual(evidence.conflict_reasons(self.core(baseline), {'en': label}, 'lighting'), [], (baseline, label))

    def test_off_source_conflict_is_demoted_without_deleting_eligible_selection(self):
        core = self.core('Soft window light enters from the left. A brass lamp is visible but switched off.')
        entries = [{'id': 'active', 'en': 'The lamp produces a localized light pool on the table.'},
                   {'id': 'window', 'en': 'soft window light'}]
        rows, meta = self.rank(core, entries)
        self.assertEqual([r['id'] for r in rows], ['window', 'active'])
        self.assertEqual(meta['_diagnostics']['conflict_demotions']['active'], ['inactive_entity_as_active_source'])

    def test_underwater_evidence_outweighs_ambiguous_pool(self):
        core = self.core('Shimmering underwater caustic light crosses the scene beneath the water surface.', setting='a swimming pool')
        entries = [{'id': 'practical', 'en': 'The wall lamp produces a localized pool on the adjacent wall and table.'},
                   {'id': 'caustic', 'en': 'shimmering underwater caustic light'}]
        rows, _ = self.rank(core, entries)
        self.assertEqual(rows[0]['id'], 'caustic')

    def test_subject_eligibility_uses_frozen_router_not_sampler_guess(self):
        core = self.core('An adult woman is seated on a supporting surface.', event='reading')
        entries = [{'id': 'generic', 'en': 'ordinary seated pose'},
                   {'id': 'seated', 'en': 'seated on a supporting surface', 'for_any': ['human']}]
        extra = {g.QUALITY_LAYERS_DATA_KEY: {'intent_routing': {'subject_categories': [
            {'category': 'human', 'aliases': ['woman']}]}}}
        rows, _ = self.rank(core, entries, slot='body_pose', data_extra=extra)
        self.assertIn('seated', [r['id'] for r in rows])

    def test_camera_projection_does_not_promote_carried_camera_into_lens_evidence(self):
        core = self.core('She is holding a telephoto camera. The photograph is framed at eye level with a wide-angle lens.')
        meaning = evidence.project(core, 'lens')
        self.assertEqual(meaning['evidence'][0]['role'], 'carried_object')
        text, _ = g.candidate_pack_slot_focus_text(core, 'lens')
        self.assertNotIn('telephoto', text)
        self.assertIn('wide-angle', text)

    def test_requested_inactive_prop_is_diagnosed_without_bypassing_guards(self):
        core = self.core('She is holding a ceramic mug.')
        trace = {'slot_scores': [], 'generation_contract': {}}
        self.assertEqual(g.candidate_pack_build_slots({'slots': {'prop': [{'id': 'mug'}]}}, trace, {}, {}, authorial_core=core), {})
        diag = trace['slot_retrieval_diagnostics']['prop']
        self.assertEqual(diag['coverage_status'], 'inactive_not_a_ranking_failure')
        self.assertEqual(diag['catalog_count'], 1)

    def test_no_people_block_is_not_bypassed_by_expansion(self):
        core = self.core('An empty room without people.', subject='an empty room')
        entries = [{'id': 'existing', 'en': 'empty space'},
                   {'id': 'person', 'en': 'a seated person', 'for_any': ['human']}]
        with patch.object(g, 'slot_block_reason', return_value='no_people'):
            rows, meta = self.rank(core, entries, slot='body_pose', contract_extra={'no_people': True})
        self.assertNotIn('person', [r['id'] for r in rows])
        if meta:
            self.assertFalse(meta['_diagnostics']['expansion_enabled'])

    def test_open_authorial_state_is_not_promoted_to_requester_lock(self):
        core = self.core('A lamp is switched off.', intent_lock={
            'locked_dimensions': [], 'open_dimensions': ['lighting'], 'semantic_anchors': []})
        entry = {'id': 'active', 'en': 'The lamp produces a pool of light.'}
        self.assertEqual(evidence.conflict_reasons(core, entry, 'lighting'), [])
        core['request_binding'] = {'active_spans': [{'text': 'The lamp must remain switched off.'}]}
        # Unrecognized grammar is not invented as hard evidence.
        core['request_binding']['active_spans'][0]['text'] = 'The lamp is switched off.'
        self.assertEqual(evidence.conflict_reasons(core, entry, 'lighting'), ['inactive_entity_as_active_source'])

    def test_required_typed_evidence_is_literal_and_role_preserving(self):
        core = self.core('Light enters from the left.', semantic_assertions=[{
            'assertion_id': 'light', 'dimension': 'lighting', 'polarity': 'required',
            'evidence': {'source_phrase': 'Light enters from the left.', 'invented_phrase': 'neon red'},
            'axes': {'source': 'window'}, 'source_span_ids': ['request']}])
        rows = evidence.project(core, 'lighting')['evidence']
        typed = [r for r in rows if r['source'] == 'semantic_assertions.evidence']
        self.assertEqual(len(typed), 1)
        self.assertEqual(typed[0]['role'], 'source_phrase')
        self.assertEqual(typed[0]['ownership'], 'requester_locked')
        self.assertEqual(typed[0]['relations'], [])

    def test_exclusion_preserves_relation_direction_and_word_order(self):
        core = self.core('An adult keeps their hands low.',
            intent_lock={'open_dimensions': ['pose'], 'locked_dimensions': []},
            request_binding={'active_spans': [{'text': 'An adult, without hands above the head.'}]})
        self.assertEqual(evidence.conflict_reasons(core, {'en': 'the head above the hands'}, 'body_pose'), [])
        self.assertEqual(evidence.conflict_reasons(core, {'en': 'hands above the head'}, 'body_pose'), ['explicit_baseline_exclusion'])

    def test_empty_expansion_cannot_bypass_primary_context_guards(self):
        core = self.core('An adult human is seated in an ordinary room.', subject='an adult human')
        entries = [{'id': 'narrow', 'en': 'a seated body pose', 'for_any': ['human'],
                    'requires_primary_any_tags': ['missing_atomic_scene']}]
        index = bm.build_bm25f_index({'slot:body_pose:narrow': {'aliases': ['a seated body pose']}},
                                     policy={'fields': {'aliases': {'weight': 4, 'b': .2}}})
        rows, _ = g.candidate_pack_rank_slot_rows({'slots': {'body_pose': entries}, g.SLOT_RETRIEVAL_POLICY_DATA_KEY: 'evidence-union'}, 'body_pose', [], '', {}, core, index,
            g.authorial_core_retrieval_text(core)[0], {'subject_category': 'human', 'adult_allowed': True,
            'intent_constraints': {'subject_categories': ['human']}}, {'id': 'generic'})
        self.assertEqual(rows, [])

    def test_union_recovers_candidate_outside_global_lane(self):
        core = self.core('Soft window light enters from the left.')
        entries = [{'id': 'unrelated', 'en': 'an interior lamp'}, {'id': 'window', 'en': 'soft window light'}]
        real = g.rank_bm25f
        def narrowed(payload, queries, **kwargs):
            result = real(payload, queries, **kwargs)
            target = 'unrelated' if 'global_context' in queries else 'window'
            return [r for r in result if r['document_id'].endswith(':'+target)]
        with patch.object(g, 'rank_bm25f', side_effect=narrowed):
            rows, _ = self.rank(core, entries)
        self.assertIn('window', [r['id'] for r in rows])


if __name__ == '__main__':
    unittest.main()
