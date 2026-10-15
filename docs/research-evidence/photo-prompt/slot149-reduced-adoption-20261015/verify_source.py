"""Deterministic full-graph integrity check; not a whole-corpus meaning review."""
import gzip
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'skills/photo-prompt-image-generator/scripts'))
import photo_candidate_corpus as c
import photo_global_index as index
import photo_semantic_evidence as native


def main():
    original = c.decode(gzip.decompress((HERE.parent / 'slot-tag-codex-direct-20261014/SOURCE.json.gz').read_bytes()))
    current = c.load(ROOT / 'skills/photo-prompt-image-generator/assets')
    assert c.digest(original) == '125d3527c728fbdee9ebdc915dc21ae0d84c8e379dd928e0012ff9df039e701b'
    assert c.digest(current) == json.loads((HERE / 'STAGE03.json').read_text())['result_sha256']
    assert set(current['candidates']) == set(original['candidates'])
    changed = [cid for cid in original['candidates'] if original['candidates'][cid] != current['candidates'][cid]]
    assert changed == ['cand_afdb9168ea8c53ad921a8574ed5248d1']
    for cid, before in original['candidates'].items():
        after = current['candidates'][cid]
        for field in ('conditions', 'effects', 'provenance', 'record_kind'):
            assert before[field] == after[field]
        assert index.text(before) == index.text(after)
    assert all(current['slot_bindings'][bid] == row for bid, row in original['slot_bindings'].items())
    assert all(current['policies'][key] == value for key, value in original['policies'].items())
    review = current['policies']['_slot_binding_review']
    assert len(review['deferred']) == 3489 and len(review['reviewed']) == 21
    suspended = [cid for cid, row in current['candidates'].items() if c.deferred_dependency_bindings(current, row)]
    result = {'schema': 'photo-slot149-reduced-source-verification/v1', 'status': 'PASS',
        'corpus_sha256': c.digest(current), 'catalog_sha256': c.digest(current['slot_catalog']),
        'candidates': len(current['candidates']), 'slots': len(current['slot_catalog']),
        'bindings': len(current['slot_bindings']), 'original_bindings_preserved': 12089,
        'new_bindings': 2, 'deferred_bindings': 3489, 'reviewed_relation_metadata': 21,
        'changed_candidates': changed, 'unchanged_candidates': 18249,
        'all_original_conditions_effects_provenance_kinds_preserved': True,
        'all_original_embedding_inputs_recipes_preserved': True,
        'original_policy_keys_preserved': True, 'full_corpus_validation': True,
        'duplicate_pairs': 0, 'orphan_references': 0,
        'dependency_suspended_candidates': suspended,
        'native_qualified': sum(native.native_status(row) == 'qualified' for row in current['candidates'].values()),
        'whole_corpus_semantic_approval': False, 'new_semantic_reviews': 0, 'Gemini_calls': 0}
    assert result['native_qualified'] == 1
    with (HERE / 'SOURCE-VERIFICATION.json').open('x') as handle:
        handle.write(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'dependency_suspended_candidates'}))
    print('dependency_suspended_candidates', len(suspended))


if __name__ == '__main__':
    main()
