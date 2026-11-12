"""Source and authority checks for the 109-row tsundere follow-up."""
import hashlib
import json
from pathlib import Path
import sys

ASSETS = Path(__file__).resolve().parents[1] / 'assets'
sys.path.insert(0, str(ASSETS.parent / 'scripts'))
import photo_candidate_corpus as corpus
import photo_candidate_retrieval_views as retrieval


def read(name):
    return json.loads((ASSETS / name).read_bytes())


def test_every_previously_unlinked_row_has_a_source_bound_review():
    review = read('photo_tsundere_109_reviewed_proposals_20261112.json')
    semantics = {r['id']: r for r in read('photo_tsundere_semantics_20261112.json')['rows']}
    views = {r['term_id']: r for r in read('photo_tsundere_research_context_views_20261112.json')['views']}
    audit = {r['source_row_id']: r for r in read('photo_tsundere_candidate_reconciliation_20261112.json')['rows']}
    rows = review['rows']
    assert len(rows) == len({r['source_row_id'] for r in rows}) == 109
    assert review['native_approval'] is False and review['automatic_activation'] is False
    for row in rows:
        key = row['source_row_id']
        assert row['source_cells'] == semantics[key]['source_cells'] == views[key]['source_cells'] == audit[key]['source_cells']
        assert row['meaning_ko'] and row['observation_limit_ko'] and row['medium_requirements']
        assert semantics[key]['followup_review']['review_sha256'] == corpus.digest(row)
        assert views[key]['followup_review']['review_sha256'] == corpus.digest(row)
        assert audit[key]['followup_review']['review_sha256'] == corpus.digest(row)
        assert views[key]['context_only'] is True and views[key]['native_approval'] is False
    assert sum(row['candidate_disposition'] == 'authored_partial_static_example' for row in rows) == 15
    assert sum(row['candidate_disposition'] == 'research_only_not_promoted' for row in rows) == 94


def test_selected_examples_have_bound_source_and_reviewed_views():
    rows = read('photo_tsundere_109_reviewed_proposals_20261112.json')['rows']
    candidates = read('photo_candidate_tsundere_109_20261112.json')['candidates']
    bindings = read('photo_candidate_tsundere_109_bindings_20261112.json')['slot_bindings']
    view_file = read('photo_candidate_retrieval_views_tsundere_109_20261112.json')
    retrieval.validate(view_file, candidates)
    assert len(candidates) == len(bindings) == 15 and len(view_file['views']) == 30
    for row in rows:
        cid, bid = row['new_candidate_id'], row['new_binding_id']
        if row['candidate_disposition'] == 'research_only_not_promoted':
            assert cid is None and bid is None
            continue
        candidate = candidates[cid]
        assert bindings[bid]['candidate_id'] == cid
        assert candidate['content']['research_semantics']['source_rows'][0]['cells'] == row['source_cells']
        assert candidate['content']['research_semantics']['native_approval'] is False
        assert candidate['content']['en'] == row['visual_example_en']
        assert candidate['content']['ko'] == row['visual_example_ko']
