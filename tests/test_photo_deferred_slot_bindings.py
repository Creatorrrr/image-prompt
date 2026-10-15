import copy
import unittest

from tests.test_photo_candidate_corpus import fixture, A, X
import photo_candidate_corpus as c
import photo_role_proposals as roles


class DeferredBindingTests(unittest.TestCase):
    def deferred(self):
        data = fixture()
        data['policies'][c.BINDING_REVIEW_POLICY] = {
            'schema': 'photo-slot-binding-review/v1',
            'deferred': {X: {'reason': 'Changed scope is not reviewed.',
                             'source_citation': 'authored migration decision'}},
            'reviewed': {}}
        return data

    def test_deferred_reference_preserves_source_and_graph_but_blocks_role(self):
        data = self.deferred()
        data['policies']['required_reference'] = {'candidate_id': A, 'binding_id': X}
        c.validate(data)
        self.assertEqual(c.entry(data, A)['_native_qualification'], 'unqualified')
        self.assertEqual(list(c.role_entries(data, 'wardrobe_style')), [])
        with self.assertRaisesRegex(ValueError, 'deferred'):
            c.entry(data, A, X)
        proposal = roles.propose(data, 'wardrobe_style', A, [X])
        self.assertEqual(proposal['semantic_fit']['reason'], 'declared_role_semantic_review_deferred')
        self.assertEqual(proposal['applicability_status'], 'incompatible')

    def test_different_role_and_global_identity_remain_available(self):
        data = self.deferred()
        self.assertEqual(list(c.all_entries(data))[0]['id'], A)
        proposal = roles.propose(data, 'garment_detail', A, [])
        self.assertEqual(proposal['applicability_status'], 'review_required')
        self.assertIsNone(proposal['source_binding_id'])

    def test_reviewed_relation_cannot_grant_native_qualification(self):
        data = self.deferred()
        state = data['policies'][c.BINDING_REVIEW_POLICY]
        state['reviewed'][X] = state['deferred'].pop(X)
        c.validate(data)
        self.assertEqual(c.binding_review_status(data, X), 'reviewed')
        proposal = roles.propose(data, 'wardrobe_style', A, [X])
        self.assertEqual(proposal['applicability_status'], 'review_required')
        self.assertEqual(proposal['native_qualification'], 'unqualified')

    def test_unbound_forgery_is_rejected_by_actual_source_replay(self):
        data = self.deferred()
        forged = roles.propose(data, 'wardrobe_style', A, [], declared_bindings=[])
        with self.assertRaisesRegex(ValueError, 'changed'):
            roles.validate(data, forged, [])

    def test_invalid_review_policy_rejected(self):
        original = self.deferred()
        variants = []
        data = copy.deepcopy(original)
        data['policies'][c.BINDING_REVIEW_POLICY]['reviewed'][X] = {'reason': 'overlap', 'source_citation': 'test'}
        variants.append(data)
        data = copy.deepcopy(original)
        data['policies'][c.BINDING_REVIEW_POLICY]['deferred']['bind_'+'f'*32] = {'reason': 'orphan', 'source_citation': 'test'}
        variants.append(data)
        data = copy.deepcopy(original)
        data['policies'][c.BINDING_REVIEW_POLICY]['deferred'][X]['reason'] = ''
        variants.append(data)
        data = copy.deepcopy(original)
        data['policies'][c.BINDING_REVIEW_POLICY]['automatic_approval'] = True
        variants.append(data)
        for data in variants:
            with self.subTest(data=data), self.assertRaises(ValueError):
                c.validate(data)

    def test_real_lazy_discovery_and_independent_audit_skip_deferred_before_entry(self):
        from tests import test_photo_global_retrieval as fixtures
        import photo_slot_retrieval as slot_search
        import photo_native_pack as packs
        import audit_global_retrieval as audit
        fixtures.GlobalDiscoveryTests.setUpClass()
        helper = fixtures.GlobalDiscoveryTests()
        self.addCleanup(helper.doCleanups)
        source = helper.data()
        bid = 'bind_' + 'd' * 32
        cid = 'cand_' + 'a' * 32
        source['policies'][c.BINDING_REVIEW_POLICY] = {
            'schema': 'photo-slot-binding-review/v1', 'reviewed': {},
            'deferred': {bid: {'reason': 'Unreviewed changed role.', 'source_citation': 'fixture'}}}
        data, context = helper.lazy(source), helper.context()
        cards, record, _ = slot_search.retrieve(data, helper.core, helper.controls, context)
        self.assertEqual(record['eligible_candidates'], 2)
        self.assertNotIn(cid, [row['id'] for row in cards['lighting']['candidates']])
        self.assertIn(cid, record['selected_candidate_ids'])
        work = packs.WorkingPack({'contract_version': packs.CONTRACT,
            'global_retrieval': record, 'authorial_core': helper.core,
            'creative_controls': helper.controls}, cards)
        pack = packs.finalize(work, data, record['selected_candidate_ids'], context)
        self.assertEqual(audit.audit(pack, data, context), [])

    def test_optional_bundle_with_deferred_member_is_suspended_without_losing_source(self):
        from tests import test_photo_global_retrieval as fixtures
        import photo_global_index as index
        import photo_slot_retrieval as slot_search
        import photo_candidate_realizations as realizations
        fixtures.GlobalDiscoveryTests.setUpClass()
        helper = fixtures.GlobalDiscoveryTests()
        self.addCleanup(helper.doCleanups)
        source = helper.data()
        parent, child, bid = 'cand_'+'f'*32, 'cand_'+'a'*32, 'bind_'+'d'*32
        source['policies'][c.BINDING_REVIEW_POLICY] = {
            'schema': 'photo-slot-binding-review/v1', 'reviewed': {},
            'deferred': {bid: {'reason': 'Pending child role.', 'source_citation': 'fixture'}}}
        row = copy.deepcopy(source['candidates'][child])
        row.update(id=parent, record_kind='visual_bundle')
        row['content'] = {'en': 'a blue cup lighting bundle',
            'source_sha256': 'a'*64, 'associated_profile_ids': [],
            'components': [{'id': 'fixture_light', 'concept_units': ['left light'], 'minimum_realizations': 1}],
            'confusion_boundaries': ['Do not omit a declared member.'],
            'member_candidates': [{'candidate_id': child, 'binding_id': bid,
                'adoption': 'optional', 'requirements': {'relations': []}}],
            'relations': [], 'adoption': 'optional', 'profile_activation': 'independent_request_evidence_only'}
        source['candidates'][parent] = row
        source['policies']['bundle_refs'] = [parent]
        recipe, text = index.text(row)
        import hashlib
        source['_global_index']['entries'][parent] = {'id': parent, 'recipe': recipe,
            'text': text, 'text_sha256': hashlib.sha256(text.encode()).hexdigest(),
            'vector': [1.0]+[0.0]*767}
        before = c.digest(row)
        data = helper.lazy(source)
        self.assertEqual(c.deferred_dependency_bindings(data, row), [bid])
        self.assertEqual(realizations.eligible_ids(data, child, helper.core, {}, {}, binding_id=bid), [])
        cards, record, _ = slot_search.retrieve(data, helper.core, helper.controls, helper.context())
        self.assertNotIn(parent, record['selected_candidate_ids'])
        self.assertIn(child, record['selected_candidate_ids'])
        self.assertEqual(c.digest(data['candidates'][parent]), before)
        self.assertEqual(c.deferred_dependency_bindings(data, data['candidates'][parent]), [bid])
