import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import photo_candidate_corpus as corpus
import photo_candidate_retrieval_views as views


def read(name):
    return json.loads((ROOT / 'assets' / name).read_text())


def test_all_previously_unsourced_rows_have_a_scoped_review():
    old = read('photo_nurse_uniform_deep_context_views_20261107.json')['views']
    expected = {x['term_id'] for x in old if not x['external_sources']}
    report = read('photo_nurse_uniform_external_review_20261107.json')
    rows = report['rows']
    assert len(expected) == len(rows) == 280
    assert {x['source_row_id'] for x in rows} == expected
    assert sum(bool(x['new_external_sources']) for x in rows) == 194
    assert all(x['native_approval'] is False and x['unresolved_ko'] for x in rows)
    supplement = read('photo_nurse_uniform_external_source_supplement_20261107.json')['rows']
    assert len(supplement) == len({x['source_row_id'] for x in supplement}) == 22
    assert {x['source_row_id'] for x in supplement} <= {x['source_row_id'] for x in rows if not x['new_external_sources']}
    assert all(x['context_only'] and not x['native_approval'] for x in supplement)
    supplement2 = read('photo_nurse_uniform_external_source_supplement2_20261107.json')['rows']
    ids2 = {x['source_row_id'] for x in supplement2}
    assert len(supplement2) == len(ids2) == 28
    assert ids2.isdisjoint({x['source_row_id'] for x in supplement})
    assert ids2 <= {x['source_row_id'] for x in rows if not x['new_external_sources']}
    assert all(x['context_only'] and not x['native_approval'] for x in supplement2)


def test_positive_views_exclude_meaning_only_diagnostic():
    records = read('photo_candidate_nurse_uniform_external_20261107.json')['candidates']
    bindings = read('photo_candidate_nurse_uniform_external_bindings_20261107.json')['slot_bindings']
    material = read('photo_candidate_retrieval_views_nurse_uniform_external_20261107.json')
    semantics = read('photo_nurse_uniform_external_semantics_20261107.json')
    positive = {key for key, value in records.items() if value['record_kind'] == 'visual_option'}
    diag = semantics['diagnostic']['candidate_id']
    assert len(positive) == len(bindings) == 26
    assert records[diag]['record_kind'] == 'diagnostic'
    assert all(x['candidate_id'] != diag for x in bindings.values())
    assert all(x['candidate_id'] != diag for x in material['views'])
    assert len(material['views']) == 52
    views.validate(material, records)
    loaded = corpus.load(ROOT / 'assets')
    assert set(records) <= set(loaded['candidates'])
    assert set(bindings) <= set(loaded['slot_bindings'])
    apron = records[semantics['source_row_to_candidates']['NURSE-ROW-285'][0]]
    assert 'does not depict or establish a nude-apron outfit' in apron['content']['application_contract']
    assert 'flat' in apron['content']['en']


def test_context_links_to_immutable_review_bytes():
    path = ROOT / 'assets' / 'photo_nurse_uniform_external_review_20261107.json'
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    context = read('photo_nurse_uniform_external_context_views_20261107.json')
    assert context['review_sha256'] == digest
    assert len(context['views']) == 280
    assert all(x['review_sha256'] == digest and x['context_only'] for x in context['views'])
    for entry in context['source_supplements']:
        path = ROOT / 'assets' / entry['file']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == entry['sha256']
        sources = read(entry['file'])['rows']
        by_id = {v['term_id']: v for v in context['views']}
        assert all(by_id[x['source_row_id']]['supplemental_sources'] == x['additional_sources'] for x in sources)
