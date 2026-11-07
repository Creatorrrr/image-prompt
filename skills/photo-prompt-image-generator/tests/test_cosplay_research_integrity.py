"""Research context must not silently become positive, authorized image data."""
import hashlib
import json
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / 'assets'


def read(name):
    return json.loads((ASSETS / name).read_text())


def test_research_context_quotes_match_all_reviewed_source_rows():
    name = 'photo_cosplay_semantics_20261106.json'
    registry = read(name)
    contexts = read('photo_cosplay_research_context_views_20261107.json')
    rows = registry['source_term_inventory']['rows']
    assert contexts['source_registry_sha256'] == hashlib.sha256((ASSETS / name).read_bytes()).hexdigest()
    assert len(rows) == len(contexts['views']) == 356
    assert len({row['id'] for row in rows}) == 356
    for row, view in zip(rows, contexts['views'], strict=True):
        assert view['term_id'] == row['id']
        assert view['source_term_label'] == row['source_term_label']
        assert view['context_ko'] == row['source_definition_ko']
        assert view['context_only'] and not view['native_approval']
        assert row['bounded_semantic_comparison']['classification'] in {
            'existing_realization', 'partial_example', 'diagnostic_context', 'insufficient_evidence'
        }


def test_unverified_glossary_context_cannot_become_positive_or_bound():
    registry = read('photo_cosplay_semantics_20261106.json')['source_term_inventory']['rows']
    records = read('photo_candidate_cosplay_supplement_20261107.json')['candidates']
    bindings = read('photo_candidate_cosplay_supplement_bindings_20261107.json')['slot_bindings']
    contextual = [r for r in registry if r['bounded_semantic_comparison']['classification'] == 'insufficient_evidence']
    bound = {v['candidate_id'] for v in bindings.values()}
    assert len(contextual) == 44
    for row in contextual:
        cid = row['context_only_candidate_id']
        record = records[cid]
        assert record['record_kind'] == 'diagnostic'
        assert record['content']['ko'] == row['source_definition_ko']
        assert record['effects'] == {'dimensions': [], 'properties': []}
        assert cid not in bound


def test_corrected_subject_and_optical_contracts_are_bound_to_matching_slots():
    primary = read('photo_candidate_cosplay_20261106.json')['candidates']
    source = read('photo_candidate_cosplay_supplement_20261107.json')['candidates']
    bindings = read('photo_candidate_cosplay_supplement_bindings_20261107.json')['slot_bindings']
    eyes = primary['cand_69a8978e0e3452609bc2ac18491d1dbe']
    assert 'color' in eyes['effects']['dimensions']
    pairs = {b['candidate_id']: b['slot_id'] for b in bindings.values()}
    face_off = source['cand_e608af79acfa5ef88979ced76d81f042']
    assert '간격' in face_off['content']['ko'] and '마주 서서' not in face_off['content']['ko']
    assert pairs[face_off['id']] == 'gaze_engagement'
    assert pairs['cand_36b2f3db370654a5a3679fd83e841cf6'] == 'depth_of_field'
