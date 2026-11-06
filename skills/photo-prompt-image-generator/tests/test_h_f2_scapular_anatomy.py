"""Anatomical scapula and similarly named religious garments remain distinct."""
import copy
import hashlib
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from photo_h_f2_source_relevance import compile_profiles, order_source_relevance, verify_source_relevance_trace


def fixture():
    texts = {'garment|base': 'The scapular has a front and back panel over the tunic.',
             'body|base': 'The scapular surface relief follows the shoulder position.',
             'alias|base': 'A garment is seen from the back.'}
    def units(identity):
        text = texts[identity]
        result = [{'pointer': '/content/en', 'text': text, 'literal_id': 'u0',
                   'source_sha256': hashlib.sha256(text.encode()).hexdigest()}]
        if identity.startswith('alias'):
            result.append({'pointer': '/content/aliases/0', 'text': 'scapular anatomy', 'literal_id': 'u1',
                           'source_sha256': hashlib.sha256(text.encode()).hexdigest()})
        return result
    def effects(identity):
        return {'dimensions': ['body_geometry'], 'properties': [{'dimension': 'body_geometry', 'property': 'body.upper_back.scapular_surface_relief',
                                'target': 'main_subject'}]} if not identity.startswith('garment') else {
            'dimensions': ['appearance'],
            'properties': [{'dimension': 'appearance', 'property': 'wardrobe.scapular', 'target': 'main_subject'}]}
    profiles = compile_profiles(texts, source_units=units, source_effects=effects)
    rows = [{'id': k, 'cid': k.split('|')[0], 'rid': 'base', 'rrf': .1, 'bm25': 1., 'cosine': .5} for k in texts]
    return rows, profiles


def test_direct_primary_and_effect_promoted_and_receipt_replays():
    rows, profiles = fixture()
    query = 'the scapular region of a human back shows shoulder blade anatomy'
    result, trace = order_source_relevance(rows, query, profiles)
    assert [r['id'] for r in result] == ['body|base', 'alias|base', 'garment|base']
    assert trace['scapular_anatomy_lane']['candidate_filter'] is False
    assert trace['scapular_anatomy_lane']['witness_count'] == 1
    assert verify_source_relevance_trace(rows, query, profiles, trace)[0] == result
    altered = copy.deepcopy(trace)
    altered['scapular_anatomy_lane']['witness_count'] = 2
    with pytest.raises(ValueError, match='replay mismatch'):
        verify_source_relevance_trace(rows, query, profiles, altered)


@pytest.mark.parametrize('query', [
    'a monastic scapular front panel over a long tunic',
    'scapular anatomy visible beneath a monastic habit',
    'not shoulder blade anatomy but a scapular',
    'no shoulder blade anatomy',
    'shoulder blade anatomy or religious scapular',
    'shoulder blade anatomy wearing a scapular',
    '"shoulder blade anatomy"',
    'scapular',
])
def test_ambiguous_excluded_quoted_or_garment_queries_abstain(query):
    rows, profiles = fixture()
    _, trace = order_source_relevance(rows, query, profiles)
    assert 'scapular_anatomy_lane' not in trace


def test_korean_anatomy_and_missing_primary_abstention():
    rows, profiles = fixture()
    result, trace = order_source_relevance(rows, '인체 등 견갑골의 해부학적 표면', profiles)
    assert result[0]['id'] == 'body|base'
    assert trace['scapular_anatomy_lane']['witness_count'] == 1
    profiles['body|base']['scapular_anatomy_witness'] = None
    result, trace = order_source_relevance(rows, '인체 등 견갑골의 해부학적 표면', profiles)
    assert trace['scapular_anatomy_lane']['witness_count'] == 0
    assert result == rows
