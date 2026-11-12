"""Tests run against a built, inactive artifact and a copied legacy index."""
import copy
import gzip
import importlib.util
import json
from pathlib import Path
import sys
import types

import pytest

OVERLAY = Path(__file__).resolve().parents[1]
SKILL = OVERLAY.parents[1]
STORE = Path.home() / '.cache/image-prompt/photo-shared-runtime/h-f2-installed'
BASE = '763c9e9032cdb8969fa1c1650697ccb24aaf1962798bf527ad980d39ade27bb7'
OLD = 'adbfbd2bedaf0be8948fc802305a5112b854ebf9d9143993cb1065ef533d391e'
pytest.importorskip('numpy', reason='research-context lane requires NumPy')
base_manifest = STORE / 'h-f2-generations' / BASE / 'manifest.json'
legacy_manifest = STORE / 'h-f2-generations' / OLD / 'manifest.json'
if not base_manifest.is_file() or not legacy_manifest.is_file():
    pytest.skip('sealed base and legacy runtime generations must be installed for integration tests', allow_module_level=True)
native_id = json.loads(base_manifest.read_text())['native_generation_id']
sys.path[:0] = [str(OVERLAY / 'scripts'), str(SKILL / 'scripts'), str(STORE / 'generations' / native_id / 'scripts')]
import photo_h_f2_research_context as lane
import photo_candidate_corpus as corpus
from bm25f_retrieval import build_bm25f_index

@pytest.fixture(scope='module')
def context(tmp_path_factory):
    # Execute the actual builder once; no installed runtime files are changed.
    import subprocess
    root = tmp_path_factory.mktemp('context')
    out = root / 'build'
    subprocess.run([sys.executable, str(OVERLAY / 'build_index.py'), '--output', str(out)], check=True,
                   stdout=subprocess.DEVNULL)
    lock = json.loads((out / 'build-lock.json').read_text())
    old = STORE / 'h-f2-generations' / OLD
    (out / lane.FILE).write_bytes((old / lane.FILE).read_bytes())
    base = json.loads((STORE / 'h-f2-generations' / BASE / 'manifest.json').read_text())
    base['research_context'] = lock['legacy_descriptor']
    base['tsundere_research_context'] = {'schema': lane.TS_SCHEMA, 'file': lane.TS_FILE,
                                         'rows': 437, 'canonical_sha256': lock['canonical_sha256']}
    base['files'][lane.FILE] = lock['legacy_index_sha256']
    base['files'][lane.TS_FILE] = lock['index_sha256']
    generation = types.SimpleNamespace(manifest=base, root=out, binding=base['binding'])
    return generation, lane.load(generation)


def ts_hits(generation, data, text):
    return [r for r in lane.query(generation, data, text, [1.0] + [0.0] * 767, limit=50)
            if r['id'].startswith('tsundere_')]


def test_source_population_and_qualification(context):
    g, data = context
    rows = data['tsundere']['rows']
    assert len(rows) == 437
    assert sum(r['term_id'].startswith('T') for r in rows) == 346
    assert sum(r['term_id'].startswith('P') for r in rows) == 70
    assert sum(r['term_id'].startswith('X') for r in rows) == 21
    hit = ts_hits(g, data, '～んだから')[0]
    assert hit['term_id'] == 'X001'
    assert hit['context_only'] and hit['native_approval'] is False and hit['automatic_activation'] is False
    assert hit['source']['url'].startswith('https://chatgpt.com/c/')
    assert len(hit['source']['snapshot_sha256']) == 64


def test_followup_metadata_is_preserved_in_index_and_search_result(context):
    g, data = context
    source = json.loads((SKILL / 'assets/photo_tsundere_research_context_views_20261112.json').read_text())
    expected = {r['term_id']: r['followup_review'] for r in source['views'] if 'followup_review' in r}
    actual = {r['term_id']: r['followup_review'] for r in data['tsundere']['rows'] if 'followup_review' in r}
    assert len(expected) == len(actual) == 109 and actual == expected
    hits = ts_hits(g, data, '테레')
    hit = next(r for r in hits if r['term_id'] == 'T01-05')
    assert hit['followup_review'] == expected['T01-05']
    assert hit['followup_review']['native_approval'] is False
    lock = json.loads((g.root / 'build-lock.json').read_text())
    assert lock['followup_review_rows'] == 109


@pytest.mark.parametrize('text', [
    '햇살 아래 커피를 마시는 여성의 사진', 'a woman holding coffee in a sunny cafe',
    'blue dress studio portrait', '빨간 드레스를 입은 인물 사진',
    '비 오는 거리에서 우산을 든 여자', 'flower garden portrait',
    '회의실에서 서류를 든 직장인', 'a woman in an office',
])
def test_unrelated_photo_queries_do_not_open_the_lane(context, text):
    g, data = context
    assert ts_hits(g, data, text) == []


@pytest.mark.parametrize(('text', 'wanted'), [
    ('ツンしゅん', 'T05-01'), ('ジト目', 'T09-02'), ('壁ドン', 'T20-11'),
    ('ニーハイ', 'T17-09'), ('knee-high socks', 'T17-06'),
    ('～んだから', 'X001'), ('目をそらしながら贈り物を渡す', 'T12-01'),
    ('상대를 피하며 우산을 건네는 츤데레', 'T12-12'), ('tsundere', 'T24-01'),
])
def test_source_expression_or_explicit_topic_opens_lane(context, text, wanted):
    g, data = context
    assert wanted in {r['term_id'] for r in ts_hits(g, data, text)}


def test_adult_rows_require_explicit_unnegated_context(context):
    g, data = context
    assert all(not r['adult_research_context'] for r in ts_hits(g, data, '브랫'))
    assert any(r['adult_research_context'] and r['term_id'] == 'T19-05'
               for r in ts_hits(g, data, 'BDSM 브랫'))
    assert not any(r['term_id'] == 'T16-02' for r in ts_hits(g, data, '코르셋'))
    assert any(r['term_id'] == 'T16-02' for r in ts_hits(g, data, '페티시 코르셋'))
    for text in ('without BDSM brat', 'no fetish 브랫', 'BDSM 제외 브랫',
                 '페티시 없이 브랫', '페티시 없는 브랫', "isn't BDSM brat", 'BDSM-free brat', 'non-fetish brat',
                 'ツンデレなし', 'fetish=3 브랫'):
        assert not any(r['adult_research_context'] for r in ts_hits(g, data, text)), text
    assert ts_hits(g, data, 'no tsundere') == []
    assert ts_hits(g, data, '츠데레 제외') == []


def test_legacy_results_unchanged_and_both_lanes_available(context):
    g, data = context
    vector = [1.0] + [0.0] * 767
    for text in ('foot fetish', 'latex fetish', 'leather jacket', '페티시 제외 가죽 재킷'):
        old = lane._legacy_query(g, data['legacy'], text, vector)
        combined = lane.query(g, data, text, vector)
        assert combined[:len(old)] == old
    assert len(data['legacy']['rows']) == 28
    assert lane.query(g, data, 'foot fetish', vector)[0]['id'].startswith('FASHION-CONTEXT-')


def test_receipt_audit_rejects_tampering(context):
    g, data = context
    vector = [1.0] + [0.0] * 767
    packet = {'query_set': {'slots': {'s': {'text': '～んだから'}}},
              'queries': {'s': {'row': {'vector': vector}}},
              'research_contexts': {'s': lane.query(g, data, '～んだから', vector)}}
    lane.audit(g, packet)
    changed = copy.deepcopy(packet)
    changed['research_contexts']['s'][0]['context_ko'] = 'tampered'
    with pytest.raises(ValueError, match='research context results changed'):
        lane.audit(g, changed)


def test_tampered_index_is_rejected(context):
    g, data = context
    changed = copy.deepcopy(data['tsundere'])
    changed['rows'][0]['native_approval'] = True
    with gzip.open(g.root / lane.TS_FILE, 'rt', encoding='utf-8') as f:
        original = f.read()
    try:
        with gzip.open(g.root / lane.TS_FILE, 'wt', encoding='utf-8') as f:
            json.dump(changed, f)
        with pytest.raises(ValueError, match='tsundere context changed'):
            lane.load(g)
    finally:
        with gzip.open(g.root / lane.TS_FILE, 'wt', encoding='utf-8') as f:
            f.write(original)


def test_changed_authority_is_rejected_even_if_canonical_digest_is_recomputed(context):
    g, data = context
    changed = copy.deepcopy(data['tsundere'])
    changed['rows'][0]['native_approval'] = True
    descriptor = g.manifest['tsundere_research_context']
    original_digest = descriptor['canonical_sha256']
    with gzip.open(g.root / lane.TS_FILE, 'rt', encoding='utf-8') as f:
        original = f.read()
    try:
        descriptor['canonical_sha256'] = corpus.digest(changed)
        with gzip.open(g.root / lane.TS_FILE, 'wt', encoding='utf-8') as f:
            json.dump(changed, f)
        with pytest.raises(ValueError, match='tsundere context authority changed'):
            lane.load(g)
    finally:
        descriptor['canonical_sha256'] = original_digest
        with gzip.open(g.root / lane.TS_FILE, 'wt', encoding='utf-8') as f:
            f.write(original)
