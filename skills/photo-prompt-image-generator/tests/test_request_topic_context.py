"""Regressions for quoted requester topic antecedents.

Run against the exact staged/installed native closure via PHOTO_H_F2_TEST_NATIVE.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import sys
import unittest

SKILL = Path(__file__).resolve().parents[1]
config = json.loads((SKILL / 'retrieval-runtime.json').read_bytes())
store = Path.home() / '.cache/image-prompt/photo-shared-runtime/h-f2-installed'
native = Path(os.environ.get('PHOTO_H_F2_TEST_NATIVE', store / 'generations' / config['native_generation_id']))
sys.path.insert(0, str(native / 'scripts'))
import prompt_generator as generator
import photo_h_f2_queries as queries
import audit_composed_prompt as auditor
wire = generator._authoring_wire


def fixture():
    request = '그 주제로 다른 장면을 만들어줘. Save the output.'
    active = request.split(' Save')[0]
    prior = 'Investigate 코스믹 호러 visual meanings. Also discuss a red bus.'
    topic = '코스믹 호러'
    offset = prior.index(topic)
    context = {'contract_version': 'photo-request-topic-context/v1', 'links': [{
        'context_id': 'prior_topic', 'active_span_id': 'scene',
        'request_quote': {'start': 0, 'end': 4, 'text': request[:4]},
        'source_message': {'provenance': 'requesting_user', 'locator': 'fixture:previous-user-message',
                           'text': prior, 'sha256': hashlib.sha256(prior.encode()).hexdigest()},
        'topic_quote': {'start': offset, 'end': offset + len(topic), 'text': topic},
        'review': {'polarity': 'positive_topic', 'rationale': 'The current antecedent continues the explicitly quoted prior topic.'}}]}
    envelope = {'contract_version': 'photo-request-envelope/v1', 'provenance': 'requesting_user',
                'request_id': 'context-regression', 'request_text': request,
                'request_sha256': hashlib.sha256(request.encode()).hexdigest(),
                'active_spans': [{'span_id': 'scene', 'start': 0, 'end': len(active), 'text': active}],
                'topic_context': context}
    return envelope


def core(envelope):
    normalized = wire.normalize_request_envelope(envelope)
    return {'contract_version': 'photo-authorial-core/v3', 'canonical_sha256': 'a' * 64,
            'source_request': normalized['request_text'], 'user_exclusions': [],
            'baseline_prompt_en': 'A surveyor holds a measuring reel beside a curved black sea at dawn.',
            'request_binding': {'active_spans': normalized['active_spans'],
                                'request_envelope_sha256': normalized['canonical_sha256'],
                                'topic_context': normalized['topic_context']}}


class TopicContext(unittest.TestCase):
    def test_exact_topic_reaches_discovery_without_rewriting_request_or_baseline(self):
        envelope = fixture(); frozen = core(envelope)
        result = queries.whole_scene(frozen, {}, {'canonical_sha256': 'b' * 64})
        topic = result[queries.REQUEST_TOPIC]
        self.assertIn('코스믹 호러', topic['text'])
        self.assertNotIn('red bus', topic['text'])
        self.assertNotIn('Save the output', topic['text'])
        self.assertEqual(result[queries.BASELINE_PROMPT]['text'], frozen['baseline_prompt_en'])
        self.assertEqual(frozen['source_request'].encode(), envelope['request_text'].encode())
        self.assertIn('request_topic_context', topic['binding']['projection']['source_fields'])
        self.assertEqual(topic['binding']['projection']['topic_context_sha256'], frozen['request_binding']['topic_context']['canonical_sha256'])

    def test_context_creates_no_active_span_or_requester_authority(self):
        raw = fixture(); normalized = wire.normalize_request_envelope(raw)
        self.assertEqual(normalized['active_spans'], raw['active_spans'])
        self.assertFalse(wire.request_scope_contains(normalized, '코스믹 호러'))

    def test_independent_consumer_reconstructs_the_producer_provenance(self):
        for contextual in (True, False):
            for exclusions in ([], ['코스믹 호러']):
                with self.subTest(contextual=contextual, exclusions=exclusions):
                    frozen = core(fixture()); frozen['user_exclusions'] = exclusions
                    if not contextual: del frozen['request_binding']['topic_context']
                    _, producer = generator.authorial_core_retrieval_text(frozen)
                    self.assertEqual(auditor.expected_authorial_core_retrieval_provenance(frozen), producer)

    def test_consumer_rejects_mutated_context_instead_of_reusing_provenance(self):
        frozen = core(fixture())
        frozen['request_binding']['topic_context']['links'][0]['topic_quote']['text'] = 'invented topic'
        with self.assertRaises(ValueError):
            auditor.expected_authorial_core_retrieval_provenance(frozen)

    def test_no_context_keeps_old_topic_projection(self):
        frozen = core(fixture()); del frozen['request_binding']['topic_context']
        result = queries.whole_scene(frozen, {}, {'canonical_sha256': 'b' * 64})
        self.assertEqual(result[queries.REQUEST_TOPIC]['text'], frozen['request_binding']['active_spans'][0]['text'])
        self.assertNotIn('topic_context_sha256', result[queries.REQUEST_TOPIC]['binding']['projection'])

    def test_exclusion_also_removes_context_topic(self):
        frozen = core(fixture()); frozen['user_exclusions'] = ['코스믹 호러']
        result = queries.whole_scene(frozen, {}, {'canonical_sha256': 'b' * 64})
        self.assertNotIn('코스믹 호러', result[queries.REQUEST_TOPIC]['text'])

    def test_context_mutation_invalidates_its_frozen_hash(self):
        frozen = core(fixture()); frozen['request_binding']['topic_context']['links'][0]['review']['rationale'] += ' changed'
        with self.assertRaisesRegex(ValueError, 'canonical hash'):
            queries.whole_scene(frozen, {}, {'canonical_sha256': 'b' * 64})

    def test_inactive_nonliteral_tampered_or_nonuser_links_fail(self):
        changes = [
            lambda r: r.update(active_span_id='other_arm'),
            lambda r: r['request_quote'].update(text='invented request'),
            lambda r: r['topic_quote'].update(text='invented topic'),
            lambda r: r['source_message'].update(sha256='0' * 64),
            lambda r: r['source_message'].update(provenance='assistant'),
            lambda r: r.update(baseline_prompt_en='injected staging'),
        ]
        for change in changes:
            with self.subTest(change=change):
                envelope = fixture(); change(envelope['topic_context']['links'][0])
                with self.assertRaises(ValueError): wire.normalize_request_envelope(envelope)

    def test_negative_directive_cannot_be_promoted_as_positive_topic(self):
        envelope = fixture(); row = envelope['topic_context']['links'][0]; text = 'No tentacles'
        row['source_message'].update(text=text, sha256=hashlib.sha256(text.encode()).hexdigest())
        row['topic_quote'] = {'start': 0, 'end': len(text), 'text': text}
        with self.assertRaisesRegex(ValueError, 'negative directive'):
            wire.normalize_request_envelope(envelope)



if __name__ == '__main__': unittest.main()
