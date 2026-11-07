"""Preserve provenance, unresolved scopes and positive/diagnostic separation."""
import hashlib
import json
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
ASSETS = SKILL / 'assets'

def read(name):
    return json.loads((ASSETS / name).read_text())

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def test_followup_covers_exactly_previously_unresolved_terms_and_keeps_context_bound():
    old = read('photo_cosplay_semantics_20261106.json')['source_term_inventory']['rows']
    expected = {r['id'] for r in old if r['bounded_semantic_comparison']['classification'] in {'partial_example', 'insufficient_evidence'}}
    regname = 'photo_cosplay_followup_semantics_20261107.json'
    reg = read(regname)
    ctx = read('photo_cosplay_followup_context_views_20261107.json')
    assert len(expected) == len(reg['term_reviews']) == len(ctx['views']) == 236
    assert {r['term_id'] for r in reg['term_reviews']} == expected
    assert ctx['source_registry_sha256'] == digest(ASSETS / regname)
    assert reg['sources_reference_sha256'] == digest(SKILL / 'references/cosplay-followup-20261107.md')
    for row, view in zip(reg['term_reviews'], ctx['views'], strict=True):
        assert row['term_id'] == view['term_id']
        assert row['new_linked_records'] == view['linked_records']
        assert row['direct_external_sources'] == view['external_sources']
        assert view['context_only'] and not view['native_approval']
        if not row['new_linked_records']:
            assert row['status'] == 'prior_partial_or_insufficient_remains_open'

def test_new_diagnostics_never_enter_positive_bindings_or_retrieval_views():
    cf = 'photo_candidate_cosplay_followup_20261107.json'
    candidates = read(cf)['candidates']
    bindings = read('photo_candidate_cosplay_followup_bindings_20261107.json')['slot_bindings']
    views = read('photo_candidate_retrieval_views_cosplay_followup_20261107.json')
    positives = {cid for cid, r in candidates.items() if r['record_kind'] == 'visual_option'}
    diagnostics = {cid for cid, r in candidates.items() if r['record_kind'] == 'diagnostic'}
    assert len(positives) == 40 and len(diagnostics) == 21
    assert {b['candidate_id'] for b in bindings.values()} == positives
    assert {v['candidate_id'] for v in views['views']} == positives
    assert views['coverage']['source_module_sha256'] == digest(ASSETS / cf)
    assert len(views['views']) == 2 * len(positives)
    for cid in diagnostics:
        assert candidates[cid]['effects'] == {'dimensions': [], 'properties': []}
    for rec in candidates.values():
        assert rec['provenance'][0]['sha256'] == digest(SKILL / 'references/cosplay-followup-20261107.md')
        assert not rec['content']['research_semantics']['native_approval']
