import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import photo_candidate_corpus as corpus
import photo_candidate_retrieval_views as views


def read(name):
    return json.loads((ROOT / 'assets' / name).read_text())


def test_deep_review_covers_distinct_source_rows_without_promoting_context():
    registry = read('photo_nurse_uniform_semantics_20261107.json')
    originals = {row['id']: row for row in registry['source_term_inventory']['rows']}
    context = read('photo_nurse_uniform_deep_context_views_20261107.json')
    rows = context['views']
    assert len(rows) == len({row['term_id'] for row in rows}) == 362
    for row in rows:
        original = originals[row['term_id']]
        assert row['source_term_label'] == original['source_term_label']
        assert row['source_definition_ko'] == original['source_definition_ko']
        assert row['context_only'] is True and row['native_approval'] is False


def test_deep_candidates_bind_complete_records_and_retrieval_views():
    candidates = read('photo_candidate_nurse_uniform_deep_20261107.json')['candidates']
    bindings = read('photo_candidate_nurse_uniform_deep_bindings_20261107.json')['slot_bindings']
    material = read('photo_candidate_retrieval_views_nurse_uniform_deep_20261107.json')
    semantics = read('photo_nurse_uniform_deep_semantics_20261107.json')
    assert len(candidates) == len(bindings) == len(semantics['cards']) == 75
    assert len(material['views']) == 2 * len(candidates)
    assert {x['candidate_id'] for x in bindings.values()} == set(candidates)
    assert {x['candidate_id'] for x in semantics['cards']} == set(candidates)
    assert all(row['native_approval'] is False for row in semantics['cards'])
    views.validate(material, candidates)
    loaded = corpus.load(ROOT / 'assets')
    assert set(candidates) <= set(loaded['candidates'])
    assert set(bindings) <= set(loaded['slot_bindings'])
    assert 'NURSE-ROW-285' not in semantics['source_row_to_candidates']
