"""Real sampler-to-public-pack contracts for the two retrieval policies.

These are lexical and explicit static-vector integration regressions, not
retrieval-quality or rendered-image evaluations. No expected candidate IDs select the fixtures or influence
queries. Embedding entry points are blocked so these tests cannot incur API cost.
"""
from __future__ import annotations

import copy
import random
import unittest
from contextlib import ExitStack
from unittest.mock import patch

from tests import photo_prompt_fixtures as fixtures
from tests import test_photo_authorial_core_v6 as v6
import prompt_generator as g
import photo_embodiment
import generate_photo_prompt as wrapper


def _dicts(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from _dicts(child)


def _slot_ids(pack):
    return {slot: [c['id'] for c in p['candidates']]
            for slot, p in pack.get('slots', {}).items()}


def configured_score_scene_fixture(data):
    """Deliberate recipe/2-D static-vector integration fixture, not a holdout.

    The real concept resolver configures atomic clay-workshop anchors. Only the
    embedding-provider seam is replaced; sampler scoring, trace population,
    protected pools, exploration generation and full pack builder remain real.
    """
    data = copy.deepcopy(data)
    source = 'Photograph an adult ceramic artist preparing clay tools for a studio work session. Keep the workshop activity practical and nonsexualized; leave photographic treatment open.'
    baseline = ('An adult ceramic artist prepares clay tools for a studio work session in a ceramics studio. '
                'One hand arranges a wooden modeling tool beside a damp block of clay, while unfinished cups '
                'and a wiping cloth remain on the scarred bench. Ordinary work clothes and clay-marked hands '
                'keep the craft role practical and nonsexualized. A coherent documentary photograph shows '
                'the artist, the material preparation and the studio together with legible surface detail.')
    raw = fixtures.core(source, interpreted_intent='A practical documentary study of preparing clay tools',
                        subject='an adult ceramic artist', setting='a quiet ceramics studio workshop',
                        event='preparing clay tools for a studio work session',
                        visual_priorities=('material preparation', 'practical craft activity'),
                        baseline_prompt_en=baseline,
                        anchor_evidence=('practical and nonsexualized', 'An adult ceramic artist',
                                         'prepares clay tools for a studio work session'))
    controls = g.creative_controls.resolve(source, overrides={'sensual':0,'fetish':0,'creativity':3,'surreal':0},seed=7)
    raw['creative_controls_sha256'] = controls['canonical_sha256']
    envelope = g.normalize_request_envelope(fixtures.envelope(source))
    core = g.normalize_authorial_core(raw, request_envelope=envelope, creative_control_snapshot=controls)
    _, explanations = wrapper.resolve_concepts(['--selection-mode','rule','--seed','42'],['도예가'],concept_mode='soft')
    anchor_spec = explanations[0]['soft_anchor_spec']
    index = data[g.SEMANTIC_INDEX_DATA_KEY]
    index['embedding_dimensions'] = 2
    for entry in index['entries'].values():
        entry['vector'] = [1.0, 0.0]
    observed_queries = []
    def static_embed(text, **kwargs):
        if kwargs.get('dimensions') != 2:
            raise AssertionError('the static integration seam only supports its explicit 2-D fixture')
        observed_queries.append(text)
        return [1.0, 0.0]
    with patch.object(g, 'embed_single_semantic_text', side_effect=static_embed):
        result = g.generate_once(data, random.Random(42), 'documentary_craftsperson_workshop',
                                 ['en'], True, 12, True, selection_mode='semantic', intent=source,
                                 include_trace=True, seed=42, semantic_index=index, semantic_dimensions=2,
                                 semantic_axis_mode='off', intent_steering='off', soft_anchor_spec=anchor_spec,
                                 authorial_core=core, creative_control_snapshot=controls)
    result['provenance']['embodiment_preflight'] = photo_embodiment.build_policy(core, fixtures.review(core['baseline_prompt_en']))
    return {'data': data, 'result': result, 'core': core,
            'observed_queries': observed_queries, 'anchor_spec': anchor_spec}


class PhotoSlotPipelineRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.guards = ExitStack()
        cls.addClassCleanup(cls.guards.close)
        for name in ('embed_texts_with_gemini', 'embed_single_semantic_text', 'cached_gemini_client'):
            cls.guards.enter_context(patch.object(g, name, side_effect=AssertionError('network/model calls forbidden in lexical pipeline tests')))
        cls.data = v6.PhotoAuthorialCoreV6Tests().runtime_data()
        cls.data.pop(g.SLOT_QUERY_VECTORS_DATA_KEY, None)
        cls.data.pop(g.VISUAL_PROFILE_QUERY_VECTORS_DATA_KEY, None)
        cls.results = {}
        cls.cores = {}
        cls.packs = {}
        for name, request, subject, setting, event, baseline, evidence in (
            ('reader',
             'Photograph an adult woman reading at a wooden table. Window daylight illuminates her from the left. The desk lamp is unplugged.',
             'an adult woman reading a folded letter', 'a quiet archive reading room',
             'she reads a folded letter at a wooden table',
             'An adult woman reading a folded letter sits at a wooden table in a quiet archive reading room. Window daylight illuminates her from the left, showing the paper surface and wood grain. The desk lamp is unplugged. Her ordinary coat rests against the chair while the archive shelves remain visible behind her. The taking camera records a calm eye-level view with natural perspective and gently separated foreground and background.',
             ('paper surface and wood grain', 'An adult woman reading a folded letter', 'sits at a wooden table', 'Window daylight illuminates her from the left')),
            ('objects',
             'Photograph three clear glass prisms on a matte tabletop with no living people or plants. A narrow white beam crosses the prisms.',
             'three clear glass prisms', 'a matte tabletop with no living people or plants',
             'a narrow white beam crosses the prisms',
             'Three clear glass prisms rest on a matte tabletop with no living people or plants. A narrow white beam crosses the prisms and separates into colored bands on the dark surface. Transparent edges stay sharp while the whole arrangement remains visible. The oblique camera view shows the incoming beam, glass thickness and separated colors together, with restrained exposure, coherent reflections and a plain background that keeps the optical study readable.',
             ('optical study readable', 'Three clear glass prisms', 'rest on a matte tabletop', 'A narrow white beam crosses the prisms')),
        ):
            raw = fixtures.core(request, subject=subject, setting=setting, event=event,
                                interpreted_intent='A factual photographic study of '+subject,
                                visual_priorities=('readable material surfaces', 'coherent photographic depth'),
                                baseline_prompt_en=baseline,
                                locked_dimensions=('concept', 'subject', 'event', 'lighting'),
                                open_dimensions=('framing', 'composition', 'camera', 'color', 'material', 'atmosphere'),
                                anchor_evidence=evidence)
            envelope = g.normalize_request_envelope(fixtures.envelope(request))
            controls = g.creative_controls.resolve(request, overrides={'sensual': 0, 'fetish': 0, 'creativity': 0, 'surreal': 0}, context={'subject_category': 'nonhuman' if name == 'objects' else 'human', 'no_people': name == 'objects'}, seed=7)
            raw['creative_controls_sha256'] = controls['canonical_sha256']
            core = g.normalize_authorial_core(raw, request_envelope=envelope, creative_control_snapshot=controls)
            result = g.generate_once(cls.data, random.Random(20260930), None, ['en'], True, 12, True,
                                     selection_mode='rule', include_trace=True, seed=20260930,
                                     authorial_core=core, creative_control_snapshot=controls)
            result['provenance']['embodiment_preflight'] = photo_embodiment.build_policy(core, fixtures.review(core['baseline_prompt_en']))
            cls.cores[name] = core
            cls.results[name] = result
            for policy in ('stable', 'evidence-union'):
                cls.packs[name, policy] = cls.build_observed(result, policy)

    @classmethod
    def build_observed(cls, result, policy, data_override=None):
        observed = {}
        original = g.candidate_pack_project
        def observe(pack, *args, **kwargs):
            observed['private'] = copy.deepcopy(pack)
            return original(pack, *args, **kwargs)
        data = dict(cls.data if data_override is None else data_override)
        data[g.SLOT_RETRIEVAL_POLICY_DATA_KEY] = policy
        with patch.object(g, 'candidate_pack_project', side_effect=observe):
            observed['public'] = g.build_candidate_pack(copy.deepcopy(result), data, 'v6')
        return observed

    def test_real_pack_preserves_internal_selected_and_scene_pointers(self):
        for key, observed in self.packs.items():
            with self.subTest(case=key):
                private = observed['private']
                all_ids = set()
                for slot, payload in private['slots'].items():
                    ids = {c['id'] for c in payload['candidates']}
                    all_ids.update(ids)
                    if payload.get('selected'):
                        self.assertIn(payload['selected'], ids, slot)
                for row in _dicts(private.get('scene_contract', {})):
                    if row.get('selected_entry_id'):
                        self.assertIn(row['selected_entry_id'], row.get('candidate_entry_ids', []))
                for row in _dicts(private.get('creative_exploration', {})):
                    if row.get('replaces_candidate_id'):
                        self.assertIn(row['replaces_candidate_id'], all_ids)
                        self.assertIn(row['candidate_id'], all_ids)

    def test_requester_locks_remain_immutable_and_public_rank_fields_are_private(self):
        for (case, policy), observed in self.packs.items():
            with self.subTest(case=case, policy=policy):
                pack = observed['public']
                core = self.cores[case]
                self.assertEqual(pack['authorial_core']['canonical_sha256'], core['canonical_sha256'])
                self.assertEqual(pack['authorial_core']['intent_lock'], core['intent_lock'])
                allowed = pack['authorial_composition']['authorship_policy']['allowed_dimensions']
                self.assertFalse(set(allowed) & set(core['intent_lock']['locked_dimensions']))
                for payload in pack['slots'].values():
                    self.assertEqual(payload['candidate_order'], 'seed_shuffled_non_preferential')
                    self.assertFalse({'selected', 'weight_floor', 'score_window', 'selected_filter'} & set(payload))
                    self.assertNotIn('_diagnostics', payload.get('retrieval', {}))
                    for candidate in payload['candidates']:
                        self.assertFalse({'selected_by_sampler', 'probability', 'weight', 'score', 'scores', '_v6_semantic_source'} & set(candidate))

    def test_audit_noise_does_not_enter_retrieval_or_public_candidate_membership(self):
        for policy in ('stable', 'evidence-union'):
            with self.subTest(policy=policy):
                result = copy.deepcopy(self.results['reader'])
                noise = 'AUDIT_ONLY_DO_NOT_USE ultraviolet neon dancing warrior extreme fisheye aerial camera'
                result['semantic_trace']['private_audit_only'] = {'text': noise}
                result['provenance']['private_audit_only'] = {'text': noise}
                changed = self.build_observed(result, policy)
                self.assertEqual(_slot_ids(changed['public']), _slot_ids(self.packs['reader', policy]['public']))
                self.assertNotIn(noise, str(changed['public']))

    def test_no_people_object_request_does_not_gain_human_pose_candidates(self):
        for policy in ('stable', 'evidence-union'):
            with self.subTest(policy=policy):
                observed = self.packs['objects', policy]
                contract = self.results['objects']['semantic_trace']['generation_contract']
                normalized = g.candidate_pack_normalized_slot_contract(self.data, self.cores['objects'], contract)
                self.assertTrue(normalized['intent_constraints']['no_people'])
                self.assertFalse(g.intent_explicitly_excludes_people(self.cores['objects']['source_request']),
                                 'fixture must test bound context rather than recognized request wording')
                bound = contract['authorial_core_constraints']
                self.assertTrue(bound['no_people'])
                self.assertIn('bound_creative_controls.context.no_people', bound['no_people_sources'])
                self.assertEqual(bound['creative_controls_sha256'], self.cores['objects']['creative_controls_sha256'])
                for candidate in observed['private']['slots'].get('body_pose', {}).get('candidates', []):
                    entry = g.candidate_pack_slot_entry_by_id(self.data, 'body_pose', candidate['entry_id'])
                    self.assertNotIn('human', g.entry_kinds(entry) | g.entry_tags(entry))

    def test_public_shuffle_is_seed_deterministic_and_membership_preserving(self):
        for policy in ('stable', 'evidence-union'):
            with self.subTest(policy=policy):
                private = self.packs['reader', policy]['private']
                original = self.packs['reader', policy]['public']
                repeated = g.candidate_pack_project(copy.deepcopy(private), 'v6')
                self.assertEqual(_slot_ids(repeated), _slot_ids(original))
                alternate = copy.deepcopy(private)
                alternate['provenance']['seed'] += 1
                shuffled = g.candidate_pack_project(alternate, 'v6')
                old_ids, new_ids = _slot_ids(original), _slot_ids(shuffled)
                self.assertEqual({k: set(v) for k, v in old_ids.items()}, {k: set(v) for k, v in new_ids.items()})
                self.assertTrue(any(old_ids[s] != new_ids[s] for s in old_ids if len(old_ids[s]) > 1))


    def test_score_mode_has_real_scene_and_exploration_references(self):
        fixture = configured_score_scene_fixture(self.data)
        result, data, core = fixture['result'], fixture['data'], fixture['core']
        score_rows = result['semantic_trace']['slot_scores']
        self.assertTrue(score_rows, 'must exercise the score-row pack path')
        self.assertGreater(result['provenance']['creativity'], 0)
        query = g.authorial_core_retrieval_text(core)[0]
        self.assertEqual(fixture['observed_queries'].count(query), 1,
                         'the exact core query must reach the static provider once; recipe axes may add local calls')
        self.assertEqual(data[g.SLOT_QUERY_VECTORS_DATA_KEY][g.candidate_pack_slot_vector_key(data[g.SEMANTIC_INDEX_DATA_KEY], query)], [1.0, 0.0])
        for policy in ('stable', 'evidence-union'):
            with self.subTest(policy=policy):
                observed = self.build_observed(result, policy, data)
                private = observed['private']
                scene_rows = [r for r in _dicts(private.get('scene_contract', {})) if r.get('selected_entry_id')]
                self.assertTrue(scene_rows, 'real configured atomic scene must produce selected scene references')
                exploration = private.get('creative_exploration')
                self.assertIsNotNone(exploration, 'positive creativity must reach exploration generation')
                self.assertTrue(exploration['enabled'])
                contrasts = exploration['contrast_candidates']
                self.assertTrue(contrasts, 'at least one real sampler alternative must exercise replacement references')
                all_ids = {c['id'] for p in private['slots'].values() for c in p['candidates']}
                score_slots = {r['slot'] for r in score_rows}
                self.assertTrue(score_slots & set(private['slots']))
                for slot, payload in private['slots'].items():
                    if payload.get('selected'):
                        self.assertIn(payload['selected'], {c['id'] for c in payload['candidates']}, slot)
                for row in scene_rows:
                    self.assertIn(row['selected_entry_id'], row['candidate_entry_ids'])
                    self.assertIn(row['selected_entry_id'], row['allowed_entry_ids'])
                for row in contrasts:
                    self.assertIn(row['replaces_candidate_id'], all_ids)
                    self.assertIn(row['candidate_id'], all_ids)
                noisy = copy.deepcopy(result)
                noisy['semantic_trace']['private_audit_only'] = 'AUDIT_ONLY extreme fisheye ultraviolet dancing'
                repeated = self.build_observed(noisy, policy, data)
                self.assertEqual(_slot_ids(observed['public']), _slot_ids(repeated['public']))
                self.assertEqual(observed['public']['authorial_core']['canonical_sha256'], core['canonical_sha256'])



    def test_bound_no_people_reaches_real_semantic_preset_selection(self):
        core = self.cores['objects']
        controls = self.results['objects']['provenance']['creative_controls']
        self.assertTrue(controls['context']['no_people'])
        self.assertFalse(g.intent_explicitly_excludes_people(core['source_request']))
        data = copy.deepcopy(self.data)
        index = data[g.SEMANTIC_INDEX_DATA_KEY]
        index['embedding_dimensions'] = 2
        for entry in index['entries'].values():
            entry['vector'] = [1.0, 0.0]
        observed = []
        choose = g.choose_preset
        def observe_choice(*args, **kwargs):
            context = args[3]
            observed.append(copy.deepcopy(context.get('intent_constraints', {})))
            return choose(*args, **kwargs)
        with patch.object(g, 'embed_single_semantic_text', return_value=[1.0, 0.0]), \
             patch.object(g, 'choose_preset', side_effect=observe_choice):
            result = g.generate_once(data, random.Random(20260930), None, ['en'], True, 12, True,
                                     selection_mode='semantic', intent=core['source_request'],
                                     include_trace=True, seed=20260930, semantic_index=index,
                                     semantic_dimensions=2, semantic_axis_mode='off', intent_steering='off',
                                     authorial_core=core, creative_control_snapshot=controls)
        self.assertEqual(len(observed), 1, 'observe actual initial preset selection')
        self.assertTrue(observed[0]['no_people'], 'bound exclusion must precede semantic preset selection')
        contract = result['semantic_trace']['generation_contract']
        self.assertTrue(contract['intent_constraints']['no_people'])
        self.assertIn('bound_creative_controls.context.no_people',
                      contract['authorial_core_constraints']['no_people_sources'])
        self.assertTrue(result['semantic_trace']['slot_scores'])


class DefaultIntentBoundContextTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.guards = ExitStack()
        cls.addClassCleanup(cls.guards.close)
        for name in ('embed_texts_with_gemini', 'embed_single_semantic_text', 'cached_gemini_client'):
            cls.guards.enter_context(patch.object(g, name, side_effect=AssertionError('network/model calls forbidden in static-vector test')))
        cls.data = v6.PhotoAuthorialCoreV6Tests().runtime_data()
        cls.data.pop(g.SLOT_QUERY_VECTORS_DATA_KEY, None)
        cls.data.pop(g.VISUAL_PROFILE_QUERY_VECTORS_DATA_KEY, None)

    def test_default_intent_bound_no_people_preserves_domain_routing_and_guarded_pool(self):
        from tests import test_photo_slot_rank_regressions as rank_fixture
        observations = []
        counts = []
        for bound in (False, True):
            core, controls = rank_fixture.SlotRankRegressionTests().bound_context_core(
                bound, interpreted_intent='A conservation photography record of an empty museum storage room')
            # This really is a core with domain routing, so an empty domain at
            # preset selection proves the default/user boundary is preserved.
            domains = g.resolve_request_intent_constraints(self.data, None, {}, authorial_core=core)['domains']
            self.assertIn('heritage_documentation', domains)
            data = copy.deepcopy(self.data)
            index = data[g.SEMANTIC_INDEX_DATA_KEY]
            index['embedding_dimensions'] = 2
            for entry in index['entries'].values():
                entry['vector'] = [1.0, 0.0]
            choose = g.choose_preset
            def observe(*args, **kwargs):
                observations.append(copy.deepcopy(args[3]['intent_constraints']))
                return choose(*args, **kwargs)
            with patch.object(g, 'embed_single_semantic_text', return_value=[1.0, 0.0]), \
                 patch.object(g, 'choose_preset', side_effect=observe):
                result = g.generate_once(data, random.Random(20260930), None, ['en'], True, 12, True,
                    selection_mode='semantic', intent='a photographic study', intent_source='default',
                    include_trace=True, seed=20260930, semantic_index=index,
                    semantic_dimensions=2, semantic_axis_mode='off', intent_steering='off',
                    authorial_core=core, creative_control_snapshot=controls)
            counts.append(int((result['semantic_trace'].get('preset_score') or {}).get('candidate_count', 0)))
        self.assertEqual(len(observations), 2)
        for key in ('domains', 'scoped_routes'):
            self.assertEqual(observations[1].get(key), observations[0].get(key), key)
        self.assertEqual(observations[1]['domains'], [])
        self.assertFalse(observations[0]['no_people'])
        self.assertTrue(observations[1]['no_people'])
        self.assertTrue(all(n > 0 for n in counts), counts)


if __name__ == '__main__':
    unittest.main()
