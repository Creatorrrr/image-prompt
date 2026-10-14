"""Verify a saved discovery run without model execution or rerunning its oracle.

The saved run already executed a full scan per slot. This checks immutable
bindings, exact source provenance, both lanes and an independent RRF replay.
It does not adjudicate meaning, qualify candidates or certify a runtime core.
"""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path

from inverse_role_search import digest, fusion, validate_result

HERE = Path(__file__).resolve().parent


def verify():
    source = json.loads(gzip.decompress((HERE / 'SOURCE.json.gz').read_bytes()))
    directory = HERE / 'inverse-baseline-01'
    result_path = directory / 'inverse-search-baseline-query-139-01.json'
    result = json.loads(result_path.read_text())
    plan = json.loads((directory / 'query-plan.json').read_text())
    embeddings_path = directory / 'execution-ledger/baseline-query-139-01/query-results.json'
    embeddings = json.loads(embeddings_path.read_text())
    assert digest(source) == result['source_sha256'] == plan['source_sha256']
    assert result['catalog_sha256'] == digest(source['slot_catalog']) == plan['catalog_sha256']
    assert result['binding_sha256'] == digest(source['slot_bindings']) == plan['binding_sha256']
    assert result['plan_sha256'] == plan['canonical_sha256'] == embeddings['plan_sha256']
    assert result['index_sha256'] == plan['index_sha256']
    assert result['index_source_sha256'] == plan['index_source_sha256']
    assert result['space'] == plan['space']
    assert result['space_sha256'] == digest(result['space']) == plan['space_sha256']
    assert result['run_id'] == embeddings['run_id'] == 'baseline-query-139-01'
    assert not result['stage5c_complete'] and not result['semantic_adjudication_complete']
    assert not result['core_bound_runtime_proof']
    slots = sorted(source['slot_catalog'])
    positive = sorted(cid for cid, row in source['candidates'].items()
                      if row['record_kind'] != 'diagnostic')
    assert len(slots) == 139 and len(positive) == 18180
    assert len(result['searches']) == len(plan['queries']) == len(embeddings['rows']) == len(slots)
    assert [row['slot_id'] for row in result['searches']] == slots
    assert [row['slot_id'] for row in plan['queries']] == slots
    source_hashes = {cid: digest(row) for cid, row in source['candidates'].items()}
    unique_retrieved = set()
    lane_counts = Counter()
    for row, query, embedding in zip(result['searches'], plan['queries'], embeddings['rows'], strict=True):
        validate_result(plan, embedding, query)
        assert row['query_sha256'] == query['text_sha256']
        assert row['slot_spec_sha256'] == query['binding']['slot_spec_sha256']
        assert row['positive_count'] == len(positive)
        assert row['positive_ids_sha256'] == digest(positive)
        assert row['search_scope'] == 'whole_shared_positive_corpus'
        assert row['tag_admission_filter'] is False
        assert row['full_scan_oracle'] == {
            'state': 'passed', 'positive_count': len(positive),
            'scope': 'all source positive documents and all stored vectors', 'quality_claim': False}
        lanes = []
        for name in ['bm25f', 'embedding']:
            lane = row['lanes'][name]
            assert lane['state'] == 'executed'
            ids = [item['document_id'] for item in lane['ranks']]
            assert len(ids) == len(set(ids)) and set(ids) <= set(positive)
            assert len(ids) <= plan['lane_limit']
            lane_counts[name] += len(ids)
            lanes.append(lane['ranks'])
        assert fusion(lanes, k=plan['rrf_k']) == row['rrf']
        union = {item['document_id'] for lane in lanes for item in lane}
        assert sorted(union) == row['union_candidate_ids']
        assert set(row['source_ids']) == union
        for cid, metadata in row['source_ids'].items():
            actual = source['candidates'][cid]
            assert metadata == {'authored_record_sha256': source_hashes[cid],
                                'source_ids': [p['source'] for p in actual['provenance']],
                                'provenance': actual['provenance']}
        unique_retrieved.update(union)
    return {
        'schema': 'photo-direct-inverse-search-saved-verification/v1',
        'result_file': str(result_path.relative_to(HERE)),
        'result_file_sha256': hashlib.sha256(result_path.read_bytes()).hexdigest(),
        'result_canonical_sha256': digest(result),
        'plan_sha256': plan['canonical_sha256'], 'source_sha256': digest(source),
        'catalog_sha256': digest(source['slot_catalog']),
        'slots': len(slots), 'positive_records': len(positive),
        'full_scan_oracles_recorded_passed': len(slots),
        'saved_binding_source_lane_and_rrf_checks_passed': len(slots),
        'independent_oracles_rerun_by_this_verifier': False,
        'lane_candidate_occurrences': dict(lane_counts),
        'unique_candidates_retrieved': len(unique_retrieved),
        'reader_io_including_oracles_and_replays': result['reader_io_total'],
        'reader_cache_peak_is_not_process_or_model_memory': True,
        'fresh_local_query_inputs': 139, 'embedding_cache_hits': 0,
        'gemini_calls': 0, 'semantic_adjudication_complete': False,
        'native_qualification_complete': False, 'stage5c_complete': False,
        'core_bound_runtime_proof': False,
        'new_proposed_141_catalog_verified': False,
    }


if __name__ == '__main__':
    result = verify()
    output = HERE / 'inverse-baseline-01/SAVED-SEARCH-VERIFICATION.json'
    if output.exists():
        assert json.loads(output.read_text()) == result
    else:
        output.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n')
    print(json.dumps({key: result[key] for key in [
        'slots', 'positive_records', 'full_scan_oracles_recorded_passed',
        'saved_binding_source_lane_and_rrf_checks_passed', 'unique_candidates_retrieved',
        'semantic_adjudication_complete', 'stage5c_complete']}, ensure_ascii=False))
