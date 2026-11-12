"""Integrity checks for source-grounded tsundere research links."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / 'assets'


def read(name):
    return json.loads((ASSETS / name).read_bytes())


def digest(name):
    return hashlib.sha256((ASSETS / name).read_bytes()).hexdigest()


def test_registry_context_and_candidate_links_match_actual_sources():
    reg = read('photo_tsundere_semantics_20261112.json')
    context = read('photo_tsundere_research_context_views_20261112.json')
    candidates = read('photo_candidate_tsundere_20261112.json')['candidates']
    candidates.update(read('photo_candidate_tsundere_supplement_20261112.json')['candidates'])
    candidates.update(read('photo_candidate_tsundere_109_20261112.json')['candidates'])
    bindings = read('photo_candidate_tsundere_bindings_20261112.json')['slot_bindings']
    bindings.update(read('photo_candidate_tsundere_supplement_bindings_20261112.json')['slot_bindings'])
    bindings.update(read('photo_candidate_tsundere_109_bindings_20261112.json')['slot_bindings'])
    assert reg['linked_candidate_module_sha256'] == digest('photo_candidate_tsundere_20261112.json')
    assert reg['linked_binding_module_sha256'] == digest('photo_candidate_tsundere_bindings_20261112.json')
    assert reg['linked_supplement_candidate_module_sha256'] == digest('photo_candidate_tsundere_supplement_20261112.json')
    assert reg['linked_supplement_binding_module_sha256'] == digest('photo_candidate_tsundere_supplement_bindings_20261112.json')
    assert reg['linked_context_views_sha256'] == digest('photo_tsundere_research_context_views_20261112.json')
    assert reg['linked_followup_review_sha256'] == digest('photo_tsundere_109_reviewed_proposals_20261112.json')
    assert reg['linked_followup_candidate_module_sha256'] == digest('photo_candidate_tsundere_109_20261112.json')
    assert reg['linked_followup_binding_module_sha256'] == digest('photo_candidate_tsundere_109_bindings_20261112.json')
    views = {v['id']: v for v in context['views']}
    rows = {r['id']: r for r in reg['rows']}
    assert len(rows) == len(views) == 346
    for source_id, row in rows.items():
        assert row['research_context_ids'] == ['tsundere_context_' + source_id.lower()]
        view = views[row['research_context_ids'][0]]
        assert view['term_id'] == source_id and view['source_cells'] == row['source_cells']
        assert row['native_approval'] is False and row['automatic_hard_activation'] is False
        for cid in row['candidate_ids']:
            assert source_id in candidates[cid]['content']['research_semantics']['source_row_ids']
        for bid in row['binding_ids']:
            assert bindings[bid]['candidate_id'] in row['candidate_ids']
    for cid, candidate in candidates.items():
        for source_id in candidate['content']['research_semantics']['source_row_ids']:
            assert cid in rows[source_id]['candidate_ids']


def test_compound_decomposition_preserves_rows_and_does_not_claim_approval():
    reg = read('photo_tsundere_semantics_20261112.json')
    split = read('photo_tsundere_compound_senses_20261112.json')
    rows = {r['id']: r for r in reg['rows']}
    pieces = split['rows']
    assert len(pieces) == 68 and len({r['source_row_id'] for r in pieces}) == 68
    component_ids = []
    for row in pieces:
        assert row['source_cells'] == rows[row['source_row_id']]['source_cells']
        assert row['native_approval'] is False and row['automatic_hard_activation'] is False
        component_ids.extend(c['id'] for c in row['components'])
    assert len(component_ids) == len(set(component_ids)) == 210


def test_reconciled_candidates_bind_to_current_source_and_rows():
    import sys
    sys.path.insert(0, str(ASSETS.parent / 'scripts'))
    import photo_candidate_corpus as corpus

    audit = read('photo_tsundere_candidate_reconciliation_20261112.json')
    reg = read('photo_tsundere_semantics_20261112.json')
    assert audit['candidate_manifest_sha256'] == digest('photo_candidate_corpus_manifest.json')
    assert audit['native_approval'] is False and audit['automatic_hard_activation'] is False
    rows = {row['id']: row for row in reg['rows']}
    assert len(audit['rows']) == 346
    candidates = corpus.load(ASSETS)
    for row in audit['rows']:
        assert row['source_cells'] == rows[row['source_row_id']]['source_cells']
        for context_ref in row.get('research_context_refs', []):
            filename = context_ref['source_file']
            assert digest(filename) == context_ref['source_file_sha256']
            matches = [v for v in read(filename)['views'] if v['id'] == context_ref['view_id']]
            assert len(matches) == 1 and corpus.digest(matches[0]) == context_ref['view_sha256']
        refs = row.get('reviewed_candidate_refs', row.get('candidate_refs', []))
        for ref in refs:
            cid = ref['candidate_id']
            assert corpus.digest(candidates['candidates'][cid]) == ref.get('record_sha256', ref.get('candidate_sha256'))
            for binding in ref.get('bindings', []):
                bid = binding.get('id', binding.get('binding_id'))
                actual = candidates['slot_bindings'][bid]
                assert actual['candidate_id'] == cid
                assert corpus.digest(actual) == binding['verified_binding_sha256']
