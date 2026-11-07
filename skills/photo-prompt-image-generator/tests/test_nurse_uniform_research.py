"""Nurse research views preserve evidence without upgrading it into image authority."""
import hashlib
import json
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / 'scripts'))
import photo_candidate_retrieval_views as retrieval_views


def read(name):
    return json.loads((SKILL / 'assets' / name).read_text())


def test_research_context_preserves_every_source_row_without_granting_authority():
    registry_path = SKILL / 'assets' / 'photo_nurse_uniform_semantics_20261107.json'
    registry = json.loads(registry_path.read_text())
    context = read('photo_nurse_uniform_research_context_views_20261107.json')
    rows, views = registry['source_term_inventory']['rows'], context['views']
    assert len(rows) == len(views) == 407
    assert context['source_registry_sha256'] == hashlib.sha256(registry_path.read_bytes()).hexdigest()
    for row, view in zip(rows, views, strict=True):
        assert row['id'] == view['term_id']
        assert row['source_term_label'] == view['source_term_label']
        assert row['source_definition_ko'] == view['context_ko']
        assert view['context_only'] is True and view['native_approval'] is False
    for phrase in ('Nursing bra', 'Bubble Head Nurse', 'ケーシー', '크로치리스'):
        assert any(phrase in row['source_term_label'] for row in rows)


def test_retrieval_views_are_bound_to_complete_current_candidate_records():
    candidates = read('photo_candidate_nurse_uniform_20261107.json')['candidates']
    views = read('photo_candidate_retrieval_views_nurse_uniform_20261107.json')
    retrieval_views.validate(views, candidates)
    assert len(candidates) == 45
    assert len(views['views']) == 2 * len(candidates)
    assert all(row['record_kind'] == 'visual_option' for row in candidates.values())
    assert all(row['native_approval'] is False for row in views['views'])


def test_each_term_review_is_bound_to_its_reviewed_evidence():
    registry = read('photo_nurse_uniform_semantics_20261107.json')
    context = read('photo_nurse_uniform_research_context_views_20261107.json')
    review_files = {}
    for review in registry['coverage_reviews']:
        path = SKILL / 'assets' / review['file']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == review['sha256']
        review_files[review['file']] = json.loads(path.read_text())
    for row, view in zip(registry['source_term_inventory']['rows'], context['views'], strict=True):
        ref = row['coverage_review']
        assert view['coverage_review'] == ref
        assert ref['native_approval'] is False
        index = int(ref['review_pointer'].split('/')[-1])
        evidence = review_files[ref['review_file']]['rows'][index]
        assert evidence['row_id'] == row['id']
        assert evidence['classification'] == ref['classification']
        assert evidence['reason'] == ref['reason']


def test_second_review_links_cover_every_source_row():
    registry = read('photo_nurse_uniform_semantics_20261107.json')
    context = read('photo_nurse_uniform_research_context_views_20261107.json')
    reviews = {}
    for ref in registry['coverage_reviews_pass2']:
        path = SKILL / 'assets' / ref['file']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == ref['sha256']
        reviews[ref['file']] = json.loads(path.read_text())
    for row, view in zip(registry['source_term_inventory']['rows'], context['views'], strict=True):
        ref = row['coverage_review_pass2']
        evidence = reviews[ref['review_file']]['rows'][int(ref['review_pointer'].split('/')[-1])]
        assert row['id'] == evidence['row_id']
        assert ref == view['coverage_review_pass2']
        assert ref['classification'] == evidence['classification']
        assert ref['native_approval'] is False


def test_third_review_only_refines_prior_holds_and_keeps_source_links():
    registry = read('photo_nurse_uniform_semantics_20261107.json')
    context = read('photo_nurse_uniform_research_context_views_20261107.json')
    reviews = {}
    for ref in registry['coverage_reviews_pass3']:
        path = SKILL / 'assets' / ref['file']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == ref['sha256']
        reviews[ref['file']] = json.loads(path.read_text())
    count = 0
    for row, view in zip(registry['source_term_inventory']['rows'], context['views'], strict=True):
        if 'coverage_review_pass3' not in row:
            continue
        count += 1
        assert row['coverage_review_pass2']['classification'] == 'hold'
        ref = row['coverage_review_pass3']
        assert ref == view['coverage_review_pass3']
        evidence = reviews[ref['review_file']]['rows'][int(ref['review_pointer'].split('/')[-1])]
        assert evidence['row_id'] == row['id']
        assert evidence['classification'] == ref['classification']
        assert ref['native_approval'] is False
    assert count == 112


def test_supplement_preserves_proposals_and_adult_preconditions():
    candidates = read('photo_candidate_nurse_uniform_supplement_20261107.json')['candidates']
    views = read('photo_candidate_retrieval_views_nurse_uniform_supplement_20261107.json')
    sem = read('photo_nurse_uniform_supplement_semantics_20261107.json')
    retrieval_views.validate(views, candidates)
    assert len(candidates) == 61 and len(views['views']) == 122
    assert len(sem['source_row_to_candidates']) == 59
    assert len(sem['context_or_held']) == 22
    for row_id in ('NURSE-ROW-252', 'NURSE-ROW-253', 'NURSE-ROW-280'):
        for cid in sem['source_row_to_candidates'][row_id]:
            assert candidates[cid]['conditions']['requires_adult_context'] is True
    for entry in sem['source_proposals']:
        assert hashlib.sha256((SKILL / 'assets' / entry['file']).read_bytes()).hexdigest() == entry['sha256']
    registry = read('photo_nurse_uniform_semantics_20261107.json')
    context = read('photo_nurse_uniform_research_context_views_20261107.json')
    for row, view in zip(registry['source_term_inventory']['rows'], context['views'], strict=True):
        assert row.get('supplement_review') == view.get('supplement_review')
