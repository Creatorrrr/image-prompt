"""Discovery scope and narrow requester ownership, against a sealed code closure."""
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
import audit_composed_prompt as auditor
import photo_h_f2_queries as queries
wire = generator._authoring_wire
scope_module = wire.photo_request_query_scope
from photo_precore_bridge import load
features = load('photo_feature_selection')


def fixture():
    request = '그 주제. 푸른 조명 surreal=0. 같은 사진. 독립 에이전트로 시험하고 저장.'
    prior = '캠퍼스물 용어를 조사해줘.'
    span = dict(span_id='scene', start=0, end=len(request), text=request)
    rows = []
    start = 0
    for text, purpose in [('그 주제.', 'topic_reference'), (' 푸른 조명 surreal=0.', 'visual'),
                          (' 같은 사진.', 'reference_use'), (' 독립 에이전트로 시험하고 저장.', 'workflow')]:
        rows.append(dict(active_span_id='scene', start=start, end=start+len(text),
                         text=text, purpose=purpose, reason='Reviewed current requester meaning.'))
        start += len(text)
    envelope = dict(contract_version='photo-request-envelope/v1', provenance='requesting_user',
                    request_id='query-scope-regression', request_text=request,
                    request_sha256=hashlib.sha256(request.encode()).hexdigest(), active_spans=[span],
                    query_scope=dict(contract_version=scope_module.VERSION, segments=rows),
                    topic_context=dict(contract_version='photo-request-topic-context/v1', links=[dict(
                        context_id='antecedent', active_span_id='scene',
                        request_quote=dict(start=0, end=4, text='그 주제'),
                        source_message=dict(provenance='requesting_user', locator='fixture:prior-user',
                                            text=prior, sha256=hashlib.sha256(prior.encode()).hexdigest()),
                        topic_quote=dict(start=0, end=4, text='캠퍼스물'),
                        review=dict(polarity='positive_topic', rationale='Exact positive prior-user topic.'))]))
    return envelope


def core(envelope):
    e = wire.normalize_request_envelope(envelope)
    return dict(contract_version='photo-authorial-core/v3', canonical_sha256='a'*64,
                source_request=e['request_text'], user_exclusions=[],
                baseline_prompt_en='A person stands beside the blue-lit window of a campus room.',
                request_binding={k: copy.deepcopy(e[k]) for k in ('active_spans','topic_context','query_scope')})


class QueryScope(unittest.TestCase):
    def test_topic_projection_retains_visual_meaning_without_execution_text(self):
        c = core(fixture())
        result = queries.whole_scene(c, {}, dict(canonical_sha256='b'*64))
        self.assertEqual(result[queries.REQUEST_TOPIC]['text'], '캠퍼스물 | 푸른 조명.')
        self.assertEqual(result[queries.BASELINE_PROMPT]['text'], c['baseline_prompt_en'])
        self.assertEqual(c['source_request'], fixture()['request_text'])
        self.assertEqual(c['request_binding']['active_spans'], fixture()['active_spans'])

    def test_independent_auditor_rebuilds_new_projection_and_binding(self):
        for excluded in ([], ['푸른 조명'], ['캠퍼스물']):
            c = core(fixture()); c['user_exclusions'] = excluded
            text, provenance = generator.authorial_core_retrieval_text(c)
            self.assertEqual(provenance, auditor.expected_authorial_core_retrieval_provenance(c))
            for phrase in excluded:
                self.assertNotIn(phrase, text)
            self.assertEqual(provenance['request_query_scope_sha256'], c['request_binding']['query_scope']['canonical_sha256'])

    def test_historical_projection_is_unchanged_without_reviewed_scope(self):
        c = core(fixture()); del c['request_binding']['query_scope']
        text = queries.whole_scene(c, {}, dict(canonical_sha256='b'*64))[queries.REQUEST_TOPIC]['text']
        self.assertIn('독립 에이전트', text)
        self.assertIn('캠퍼스물', text)
        self.assertEqual(generator.authorial_core_retrieval_text(c)[1], auditor.expected_authorial_core_retrieval_provenance(c))

    def test_unreviewed_overlap_tampered_offspan_or_unresolved_segments_fail(self):
        mutations = [lambda e: e['query_scope']['segments'].pop(),
                     lambda e: e['query_scope']['segments'].append(copy.deepcopy(e['query_scope']['segments'][0])),
                     lambda e: e['query_scope']['segments'][0].update(text='invented'),
                     lambda e: e['query_scope']['segments'][0].update(active_span_id='other_arm'),
                     lambda e: e.pop('topic_context'),
                     lambda e: e['query_scope']['segments'][0].update(purpose='inferred_topic'),
                     lambda e: e['query_scope']['segments'][0].update(start=True)]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                e=fixture(); mutate(e)
                with self.assertRaises(ValueError): wire.normalize_request_envelope(e)

    def test_scope_or_topic_hash_mutation_is_rejected_by_both_consumers(self):
        for field in ('query_scope','topic_context'):
            c=core(fixture()); c['request_binding'][field]['canonical_sha256']='0'*64
            with self.assertRaises(ValueError): generator.authorial_core_retrieval_text(c)
            with self.assertRaises(ValueError): auditor.expected_authorial_core_retrieval_provenance(c)


class Ownership(unittest.TestCase):
    def fixture(self, atom='interior'):
        baseline='A person in a campus interior arranges a shared practical assignment.'
        envelope=dict(request_sha256='a'*64)
        anchor=dict(anchor_id='event', source_text='캠퍼스물', prompt_evidence='campus interior')
        core=dict(baseline_prompt_en=baseline, intent_lock=dict(semantic_anchors=[anchor]),
                  user_definitions=[], semantic_assertions=[])
        selection=dict(selected=[dict(category_id='feature.setting', basis='agent_visual_choice', baseline_evidence='campus interior')])
        review=dict(contract_version=features.photo_request_ownership.VERSION,
                    request_sha256=envelope['request_sha256'], baseline_prompt_sha256=hashlib.sha256(baseline.encode()).hexdigest(),
                    anchors=[dict(**anchor,requester_meaning='Campus context',reason='Review the user-owned meaning.')],
                    authorial_details=[dict(category_id='feature.setting',literals=[atom],reason='Author-chosen replaceable staging.')])
        return core,selection,envelope,review

    def test_fragment_inside_longer_required_evidence_is_rejected(self):
        for phrase in ('interior','practical assignment','preparing a club activity'):
            c,s,e,r=self.fixture(); c['baseline_prompt_en']='A campus '+phrase+' under blue light.'
            c['intent_lock']['semantic_anchors'][0]['prompt_evidence']='campus '+phrase
            s['selected'][0]['baseline_evidence']=phrase+' under blue light'
            r['anchors'][0]['prompt_evidence']='campus '+phrase
            r['baseline_prompt_sha256']=hashlib.sha256(c['baseline_prompt_en'].encode()).hexdigest()
            r['authorial_details'][0]['literals']=[phrase]
            with self.subTest(phrase=phrase), self.assertRaisesRegex(ValueError,'authorial detail is locked'):
                features.photo_request_ownership.validate(r,c,s,e,features._required_evidence_phrases(c))

    def test_narrow_anchor_leaves_authorial_staging_replaceable(self):
        c,s,e,r=self.fixture()
        c['intent_lock']['semantic_anchors'][0]['prompt_evidence']='campus'
        r['anchors'][0]['prompt_evidence']='campus'
        self.assertTrue(features.photo_request_ownership.validate(r,c,s,e,features._required_evidence_phrases(c))['valid'])

    def test_required_definition_and_assertion_are_also_checked(self):
        for kind in ('definition','assertion'):
            c,s,e,r=self.fixture(); c['intent_lock']['semantic_anchors'][0]['prompt_evidence']='campus';r['anchors'][0]['prompt_evidence']='campus'
            if kind=='definition': c['user_definitions']=[dict(prompt_evidence='campus interior')]
            else:c['semantic_assertions']=[dict(polarity='required',evidence=dict(location='campus interior'))]
            with self.subTest(kind=kind),self.assertRaisesRegex(ValueError,'authorial detail is locked'):
                features.photo_request_ownership.validate(r,c,s,e,features._required_evidence_phrases(c))

    def test_missing_review_coverage_stale_hash_or_literal_fails(self):
        for mutation in (lambda r:r['anchors'].clear(),lambda r:r['anchors'].append(copy.deepcopy(r['anchors'][0])),
                         lambda r:r.update(baseline_prompt_sha256='0'*64),lambda r:r['authorial_details'].clear(),
                         lambda r:r['authorial_details'][0].update(literals=['outside evidence'])):
            c,s,e,r=self.fixture();mutation(r)
            with self.assertRaises(ValueError):features.photo_request_ownership.validate(r,c,s,e,[])

    def test_request_owned_feature_is_not_reclassified_by_word_overlap(self):
        c,s,e,r=self.fixture();s['selected'][0]['basis']='request_derived';r['authorial_details']=[]
        self.assertTrue(features.photo_request_ownership.validate(r,c,s,e,features._required_evidence_phrases(c))['valid'])


if __name__ == '__main__':
    unittest.main()
