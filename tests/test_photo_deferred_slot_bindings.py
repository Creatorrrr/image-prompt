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
