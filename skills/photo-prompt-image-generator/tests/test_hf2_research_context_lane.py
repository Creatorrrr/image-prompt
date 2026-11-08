"""Boundary and tamper checks for the sealed research lane, without a model."""
import copy
import importlib.util
from pathlib import Path
import sys
import types
from unittest.mock import patch

import pytest

pytest.importorskip('numpy', reason='H-F2 lane uses the installed embedding runtime')

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / 'scripts'))
from bm25f_retrieval import build_bm25f_index

stub = types.ModuleType('photo_recall_first')
def require(value, message):
    if not value:
        raise ValueError(message)
stub.require = require
path = SKILL / 'runtime-overlays/fetish-context-20261108/scripts/photo_h_f2_research_context.py'
spec = importlib.util.spec_from_file_location('test_hf2_research_context_lane_module', path)
lane = importlib.util.module_from_spec(spec)
with patch.dict(sys.modules, {'photo_recall_first': stub}):
    spec.loader.exec_module(lane)


def fixture():
    rows = []
    for i, (term, alias) in enumerate((('Foot fetish', '발 페티시'),
                                       ('Latex fetish', '라텍스 페티시'),
                                       ('Fetish fashion', '페티시 패션'))):
        vector = [0.0] * 768
        vector[i] = 1.0
        rows.append({'id': str(i), 'term': term, 'search_aliases': [alias],
                     'context_ko': alias, 'boundary': '관심과 외관은 별개',
                     'tags': ['fetish'], 'source_file': 'source.json',
                     'source_sha256': '0' * 64, 'context_only': True,
                     'native_approval': False, 'vector': vector})
    return {'rows': rows, 'lexical_index': build_bm25f_index(lane.documents(rows), policy=lane.POLICY)}


@pytest.mark.parametrize(('query', 'wanted', 'vector'), [
    ('foot fetish', '0', 0), ('발에 대한 페티시의 의미', '0', 0),
    ('latex fetish', '1', 1), ('fetish-fashion', '2', 2),
])
def test_explicit_context_returns_source_bound_research(query, wanted, vector):
    q = [0.0] * 768
    q[vector] = 1.0
    first = lane.query(None, fixture(), query, q)[0]
    assert first['id'] == wanted
    assert first['context_only'] is True and first['native_approval'] is False
    assert 'candidate_id' not in first


@pytest.mark.parametrize('query', ['leather jacket', '가죽 재킷', 'without fetish',
                                   '페티시 제외 가죽 재킷', 'fetish=3, blue coat'])
def test_nonexplicit_or_excluded_context_is_not_returned(query):
    q = [1.0] + [0.0] * 767
    assert lane.query(None, fixture(), query, q) == []


def test_audit_rejects_research_result_tampering(monkeypatch):
    data = fixture()
    monkeypatch.setattr(lane, 'load', lambda generation: data)
    q = [1.0] + [0.0] * 767
    packet = {'query_set': {'slots': {'s': {'text': 'foot fetish'}}},
              'queries': {'s': {'row': {'vector': q}}},
              'research_contexts': {'s': lane.query(None, data, 'foot fetish', q)}}
    lane.audit(None, packet)
    changed = copy.deepcopy(packet)
    changed['research_contexts']['s'][0]['term'] = 'altered'
    with pytest.raises(ValueError, match='research context results changed'):
        lane.audit(None, changed)
