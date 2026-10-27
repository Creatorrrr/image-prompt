"""Natural-query ranking boundaries, independent of a corpus or model."""
from pathlib import Path
import copy
import hashlib
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from photo_h_f2_source_relevance import (
    compile_profiles, order_source_relevance, verify_source_relevance_trace,
    DEFAULT_RELATION_LANE_WEIGHT,
)
from photo_h_f2_single_property import query_recognizer, source_witness


class SourceRelevanceTests(unittest.TestCase):
    def units(self, texts):
        digest = hashlib.sha256(repr(texts).encode()).hexdigest()
        return [{'pointer': pointer, 'text': text, 'literal_id': str(i),
                 'source_sha256': digest, 'candidate_id': 'synthetic',
                 'realization_id': 'base'}
                for i, (pointer, text) in enumerate(texts)]

    def score(self, query, texts, effects=None, structured=False, **kwargs):
        units = self.units(texts)
        profiles = compile_profiles({'synthetic|base': ''}, source_units=lambda _: units,
                                    source_effects=lambda _: effects or {})
        rows = [{'id': 'synthetic|base', 'cid': 'synthetic', 'rid': 'base',
                 'rrf': .05, 'bm25': 1., 'cosine': .5}]
        ordered, trace = order_source_relevance(rows, query, profiles,
                                               structured=structured, **kwargs)
        self.assertEqual(ordered, rows)
        self.assertFalse(trace['native_approval'])
        self.assertFalse(trace['semantic_approval'])
        return rows, profiles, trace

    def contribution(self, trace):
        return sum(x.get('source_lane_contribution', 0.)
                   for x in trace.get('top8_source_witnesses', []))

    def test_color_cannot_transfer_between_objects(self):
        for query, source in [
            ('Find a red jacket.', 'A red wall behind a black jacket.'),
            ('Find black nails.', 'A black dress beside blue nails.'),
            ('Find a red jacket.', 'A red shirt beside a black jacket.'),
            ('Find silver rings.', 'A silver dress beside black rings.'),
            ('Find pink lips.', 'A pink wall behind the woman.'),
        ]:
            with self.subTest(query=query, source=source):
                _, _, trace = self.score(query, [('/content/en', source)])
                self.assertEqual(self.contribution(trace), 0.)

    def test_duplicate_primary_fields_do_not_invalidate_one_complete_witness(self):
        _, _, trace = self.score('Find a red jacket.', [
            ('/content/en', 'A red jacket is worn by the woman.'),
            ('/content/ko', '여성이 빨간 재킷을 입고 있다.'),
            ('/content/definition', 'A red jacket is worn by the woman.'),
        ])
        self.assertGreater(self.contribution(trace), 0.)

    def test_split_primary_units_do_not_create_one_complete_attribute_witness(self):
        _, _, trace = self.score('Find a red jacket with black pants.', [
            ('/content/en', 'A red jacket is worn by the woman.'),
            ('/content/ko', 'The woman wears black pants.'),
        ])
        self.assertEqual(self.contribution(trace), 0.)

    def test_unknown_owner_and_unmodeled_finish_do_not_receive_color_bonus(self):
        for query, source in [
            ('Find red ceramivia.', 'A red jacket is visible.'),
            ('Find pink lips with a glossy finish.', 'Pink lips have a matte finish and no gloss.'),
        ]:
            with self.subTest(query=query):
                _, _, trace = self.score(query, [('/content/en', source)])
                self.assertEqual(self.contribution(trace), 0.)

    def test_lookup_alias_cannot_supply_a_primary_attribute(self):
        _, _, trace = self.score('Find a red jacket.', [
            ('/content/aliases/0', 'A red jacket.'),
            ('/content/en', 'A plain wall.'),
        ])
        self.assertEqual(self.contribution(trace), 0.)

    def test_unknown_and_structured_requests_keep_original_order(self):
        for query, structured in [('zxquv jalternix', False),
                                  ('Photographic role: camera height. Scene context: woman.', True)]:
            with self.subTest(query=query):
                _, _, trace = self.score(query, [('/content/en', 'A camera at eye level.')],
                                         structured=structured)
                self.assertFalse(trace['applied'])

    def test_receipt_replay_uses_sealed_weights(self):
        query = 'Find a red jacket.'
        rows, profiles, trace = self.score(query, [('/content/en', 'The woman wears a red jacket.')])
        replayed, _ = verify_source_relevance_trace(rows, query, profiles, trace)
        self.assertEqual(replayed, rows)
        alternative = .5 if DEFAULT_RELATION_LANE_WEIGHT != .5 else 1.
        _, forged = order_source_relevance(rows, query, profiles, relation_lane_weight=alternative)
        with self.assertRaises(ValueError):
            verify_source_relevance_trace(rows, query, profiles, forged)

    def test_receipt_rejects_changed_trace(self):
        query = 'Find a red jacket.'
        rows, profiles, trace = self.score(query, [('/content/en', 'The woman wears a red jacket.')])
        forged = copy.deepcopy(trace)
        forged['top8_source_witnesses'][0]['source_lane_contribution'] += .01
        with self.assertRaises(ValueError):
            verify_source_relevance_trace(rows, query, profiles, forged)


class SinglePropertyWitnessTests(unittest.TestCase):
    def witness(self, kind, text, properties=()):
        units = [{'pointer': '/content/en', 'literal_id': 'primary', 'text': text,
                  'source_sha256': 'a' * 64, 'candidate_id': 'synthetic',
                  'realization_id': 'base'}]
        effects = {'properties': [{'property': p, 'target': t, 'dimension': 'pose'}
                                  for p, t in properties]}
        return source_witness(kind, units, effects)

    def test_identity_questions_preserve_literal_spans_and_leave_answer_open(self):
        for query in [
            'Is the figure in the glass a second person, or the woman taking her own mirror photo?',
            '유리에 비친 인물은 다른 사람인가, 거울 셀카를 찍는 여성 본인인가?',
        ]:
            with self.subTest(query=query):
                result = query_recognizer(query)
                self.assertEqual(result['kind'], 'reflection_identity')
                for span in result['evidence_spans']:
                    self.assertEqual(query[span['start']:span['end']], span['quote'])

    def test_negated_quoted_and_uncertain_identity_are_not_promoted(self):
        effect = [('action.same_woman_photographs_self_in_mirror', 'woman, phone, mirror')]
        for text in [
            'In front of a mirror, the woman does not photograph herself.',
            'The caption says “same person” in the mirror reflection.',
            'The mirror reflection may be the same person, or the identity is unknown.',
        ]:
            with self.subTest(text=text):
                result = self.witness('reflection_identity', text, effect)
                self.assertFalse(result and result.get('promoted'))

    def test_identity_requires_direct_primary_and_matching_selected_effect(self):
        text = 'In front of a mirror, the woman photographs herself.'
        self.assertFalse(self.witness('reflection_identity', text).get('promoted'))
        result = self.witness('reflection_identity', text, [
            ('action.same_woman_photographs_self_in_mirror', 'woman, phone, mirror')])
        self.assertTrue(result['promoted'])
        for evidence in result['evidence_spans']:
            self.assertEqual(text[evidence['start']:evidence['end']], evidence['quote'])

    def test_tilt_requires_resolved_owner_and_positive_state(self):
        effect = [('camera.roll.tilted_horizon', 'image frame relative to horizon')]
        for text in [
            'The frame is not tilted while the head remains level.',
            'The frame and head are both level.',
            'The frame may be tilted while the head is level.',
            'The caption says “the frame is tilted rather than the head.”',
            'The head inclines while the chin points toward frame-left.',
        ]:
            with self.subTest(text=text):
                result = self.witness('tilt_owner_disambiguation', text, effect)
                self.assertFalse(result and result.get('promoted'))

    def test_both_tilted_needs_both_effect_families(self):
        text = 'The woman’s head is tilted while the image frame is canted.'
        frame = ('camera.roll.tilted_horizon', 'image frame relative to horizon')
        head = ('pose.head.orientation.tilted', 'head')
        for props in [[frame], [head]]:
            self.assertFalse(self.witness('tilt_owner_disambiguation', text, props).get('promoted'))
        self.assertTrue(self.witness('tilt_owner_disambiguation', text, [frame, head])['promoted'])


if __name__ == '__main__':
    unittest.main()
