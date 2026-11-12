"""Research context must preserve source rows without turning them into authority."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import pytest

SKILL = Path(__file__).resolve().parents[1]
REPO = SKILL.parent.parent
sys.path.insert(0, str(SKILL / 'scripts'))
from photo_tsundere_context_search import search  # noqa: E402


def ids(q, **kw):
    return [row['term_id'] for row in search(q, limit=50, **kw)['results']]


def test_preserves_every_frozen_table_cell():
    context = json.loads((SKILL / 'assets/photo_tsundere_research_context_views_20261112.json').read_text())
    views = {row['term_id']: row for row in context['views']}
    assert len(views) == len(context['views']) == 346
    assert all(v['context_only'] is True and v['native_approval'] is False
               and v['automatic_activation'] is False for v in views.values())
    snapshot = SKILL / 'runtime-overlays/tsundere-context-20261112/source-snapshots/source-tables.json'
    raw = snapshot.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == context['source']['source_table_sha256']
    tables = json.loads(raw)
    assert len(tables) == 24
    expected = {f"T{t['table']:02d}-{i:02d}": cells
                for t in tables for i, cells in enumerate(t['rows'], 1)}
    assert set(views) == set(expected)
    assert all(views[k]['source_cells'] == cells for k, cells in expected.items())


def test_multilingual_source_and_unverified_examples_are_searchable():
    for q, expected in [('ツンしゅん', 'T05-01'), ('ジト目', 'T09-02'),
                        ('壁ドン', 'T20-11'), ('ニーハイ', 'T17-09'),
                        ('knee-high socks', 'T17-06'), ('tsundere', 'T24-01'),
                        ('ツンデレ', 'T24-01')]:
        assert expected in ids(q), q
    hit = search('tsundere')['results'][0]
    assert 'tsundere' in hit['related_search_examples']
    assert 'tsundere' not in hit['source_alternate_form_leads']
    assert hit['candidate_refs'] == [] and hit['context_only']


def test_japanese_sentence_discovers_partial_evidence_without_synonym_claim():
    result = search('相手を避けながら傘を渡す', limit=5)['results']
    by_id = {row['term_id']: row for row in result}
    # These two source rows cover separate parts of the query; neither
    # establishes that avoiding a person means averted gaze or romantic care.
    assert 'T12-12' in by_id and 'T12-01' in by_id
    assert by_id['T12-12']['partial_related_search_boundary']
    assert by_id['T12-01']['partial_related_search_boundary']
    assert '目をそらしながら贈り物を渡す' in by_id['T12-01']['partial_related_search_leads']
    assert '目をそらしながら贈り物を渡す' not in by_id['T12-01']['source_alternate_form_leads']
    assert ids('目をそらしながら贈り物を渡す')[0] == 'T12-01'
    assert ids('相手の方へ傘を傾ける')[0] == 'T12-12'

def test_no_latin_substring_and_adult_context_is_explicit():
    assert ids('sun') == []
    for query in ('가터벨트', '초커', '스위치', '칭찬', '브랫'):
        assert not search(query)['adult_context_lookup']
        assert all(not row['adult_research_context'] for row in search(query, limit=50)['results'])
    assert 'T19-05' in ids('브랫', adult_context=True)
    assert 'T19-08' in ids('펨돔')
    assert 'T19-05' in ids('BDSM 브랫')
    assert search('fetish leather')['adult_context_lookup']


def test_invalid_inputs_rejected():
    with pytest.raises(ValueError):
        search(' ')
    with pytest.raises(ValueError):
        search('test', limit=51)
    with pytest.raises(ValueError):
        search('test', adult_context='yes')


def test_prose_is_opt_in_and_each_original_span_is_bound():
    baseline = search('～んだから', limit=20)
    assert baseline['source_count'] == 346
    assert 'prose_context_sha256' not in baseline
    assert all(not row['term_id'].startswith(('P', 'X')) for row in baseline['results'])
    result = search('～んだから', limit=20, include_prose=True)
    assert result['prose_record_count'] == 91
    assert result['source_count'] == 436  # one original empty paragraph is preserved, not indexed
    assert result['results'][0]['term_id'] == 'X001'
    row = result['results'][0]
    location = row['source_location']
    assert row['context_ko'][location['start_codepoint']:location['end_codepoint_exclusive']] == '～んだから'
    assert row['context_only'] is True and row['native_approval'] is False
    snapshot = SKILL / 'runtime-overlays/tsundere-context-20261112/source-snapshots/source-prose.json'
    raw = snapshot.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == result['source_prose_sha256']
    assert json.loads(raw)[location['snapshot_item_1based'] - 1]['text'] == row['context_ko']


def test_prose_six_patterns_are_separate_and_adult_context_is_filtered():
    for i, phrase in enumerate(('～んだから', '～てあげる', '～てもいい',
                                 '～だけ', '別に', '勘違いしないで'), 1):
        hit = search(phrase, include_prose=True)['results'][0]
        assert hit['term_id'] == f'X{i:03d}'
        assert hit['source_location']['quoted_text'] == phrase
    no_adult = search('호감·홍조·도발과 동의', include_prose=True, limit=50)
    assert not no_adult['adult_context_lookup']
    assert all(not item['adult_research_context'] for item in no_adult['results'])
    adult = search('호감·홍조·도발과 동의', include_prose=True,
                   adult_context=True, limit=50)
    assert 'X019' in {item['term_id'] for item in adult['results']}
    assert search('sun', include_prose=True)['results'] == []
