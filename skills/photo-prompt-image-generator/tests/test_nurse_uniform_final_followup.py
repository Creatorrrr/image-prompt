import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
sys.path.insert(0, str(ROOT / 'scripts'))
import photo_candidate_corpus as corpus
import photo_candidate_retrieval_views as retrieval_views


def read(name):
    return json.loads((ASSETS / name).read_text())


def test_followup_covers_exact_unresolved_population_and_source_boundaries():
    previous = read('photo_nurse_uniform_external_review_20261107.json')['rows']
    covered = set()
    for name in ('photo_nurse_uniform_external_source_supplement_20261107.json',
                 'photo_nurse_uniform_external_source_supplement2_20261107.json'):
        covered.update(x['source_row_id'] for x in read(name)['rows'])
    expected = {x['source_row_id'] for x in previous if not x['new_external_sources'] and x['source_row_id'] not in covered}
    assert len(expected) == 36
    expected.add('NURSE-ROW-285')
    review = read('photo_nurse_uniform_final_followup_review_20261107.json')
    rows = review['rows']
    assert len(rows) == len(expected) == 37
    assert {x['source_row_id'] for x in rows} == expected
    assert all(x['additional_sources'] and x['unresolved_ko'] and not x['native_approval'] for x in rows)
    assert all(s['supported_scope_ko'] and s['support'] in {'partial', 'direct_meaning'}
               for row in rows for s in row['additional_sources'])
    hold = next(x for x in rows if x['source_row_id'] == 'NURSE-ROW-285')
    assert hold['source_status'] == 'meaning_verified_visual_hold'
    assert hold['linked_candidate_ids'] == ['cand_1cc1ddabe95952d992cb345b76a8cf4f']
    assert '가려진' in hold['unresolved_ko'] and '연령' in hold['unresolved_ko']


def test_context_and_candidates_remain_separate_and_source_bound():
    review_path = ASSETS / 'photo_nurse_uniform_final_followup_review_20261107.json'
    digest = hashlib.sha256(review_path.read_bytes()).hexdigest()
    review = json.loads(review_path.read_text())
    context = read('photo_nurse_uniform_final_followup_context_views_20261107.json')
    assert context['review_sha256'] == digest and len(context['views']) == 37
    for view in context['views']:
        index = int(view['review_pointer'].rsplit('/', 1)[1])
        row = review['rows'][index]
        assert view['term_id'] == row['source_row_id']
        assert view['additional_sources'] == row['additional_sources']
        assert view['review_sha256'] == digest and view['context_only'] and not view['native_approval']
    records = read('photo_candidate_nurse_uniform_final_followup_20261107.json')['candidates']
    bindings = read('photo_candidate_nurse_uniform_final_followup_bindings_20261107.json')['slot_bindings']
    material = read('photo_candidate_retrieval_views_nurse_uniform_final_followup_20261107.json')
    semantics = read('photo_nurse_uniform_final_followup_semantics_20261107.json')
    positive = {key for key, value in records.items() if value['record_kind'] == 'visual_option'}
    diagnostic = {key for key, value in records.items() if value['record_kind'] == 'diagnostic'}
    assert len(positive) == len(bindings) == 25 and len(material['views']) == 50
    assert len(diagnostic) == 3
    assert diagnostic.isdisjoint(v['candidate_id'] for v in material['views'])
    assert diagnostic.isdisjoint(v['candidate_id'] for v in bindings.values())
    for view in material['views']:
        source = records[view['candidate_id']]['content']['en']
        assert source in view['text_en']
        if view['kind'] == 'context':
            assert view['text_en'].startswith('Optional research topic (component only): ')
            assert '필수 조건이 아니다' in view['context_ko']
        else:
            assert view['text_en'] == source
    assert all(v['content']['research_semantics']['source_review_sha256'] == digest for v in records.values())
    assert semantics['visual_hold_ids'] == ['NURSE-ROW-285']
    assert {'NURSE-ROW-262', 'NURSE-ROW-263', 'NURSE-ROW-264', 'NURSE-ROW-285'} == set(semantics['context_only_rows'])
    retrieval_views.validate(material, records)
    loaded = corpus.load(ASSETS)
    assert set(records) <= set(loaded['candidates'])
    for row in review['rows']:
        assert set(row['linked_candidate_ids']) <= set(loaded['candidates'])
    for rid in ('262', '263', '264'):
        row = next(x for x in review['rows'] if x['source_row_id'] == 'NURSE-ROW-' + rid)
        assert set(row['linked_candidate_ids']) <= diagnostic
    assert all(v['candidate_id'] != 'cand_1cc1ddabe95952d992cb345b76a8cf4f' for v in material['views'])
    assert all(v['candidate_id'] != 'cand_1cc1ddabe95952d992cb345b76a8cf4f' for v in bindings.values())
