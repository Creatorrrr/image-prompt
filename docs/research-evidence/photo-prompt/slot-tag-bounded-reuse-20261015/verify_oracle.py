"""Offline exact full-pool oracle for the six changed presentation roles."""
import gzip
import time
from common import *
import photo_global_index as index
import photo_sharded_search as lazy
from photo_search_reader import SearchReader
from build_shared_candidate_index import offline_vector_map
from bm25f_retrieval import rank_bm25f, reciprocal_rank_fusion


def main():
    started = time.monotonic()
    # The runtime verifier seals this context before generating the pack, so
    # this independent offline check may run alongside its 149-slot replay.
    path = HERE / 'RUNTIME-evidence/QUERY-CONTEXT.json.gz'
    raw = path.read_bytes()
    context = json.loads(gzip.decompress(raw) if path.suffix == '.gz' else raw)
    source = c.load(SKILL / 'assets')
    reader = SearchReader(SKILL / 'assets')
    assert reader.manifest['corpus_sha256'] == read(HERE / 'STAGE04.json')['result_sha256']
    vectors = offline_vector_map(reader, source)
    lexical = index.lexical(source)
    allowed = set(vectors['entries'])
    assert len(allowed) == 18180
    # Explicit all-vector materialization above is this offline oracle only.
    reader.close()
    reader = SearchReader(SKILL / 'assets')
    slots = sorted({v['slot_id'] for v in read(HERE / 'RELATION-REVIEW.json')['records']})
    result = {}
    for slot in slots:
        row = context['slots'][slot]
        fields, vector = row['binding']['query_fields'], row['vector']
        expected_lexical = rank_bm25f(lexical, fields, allowed_ids=allowed, limit=384)
        expected_vector = index.cosine_rank(vectors, vector, allowed, limit=384)
        actual_lexical = lazy.lexical_rank(reader, fields, allowed, limit=384)
        actual_vector, proof = lazy.cosine_rank(reader, vector, allowed, limit=384)
        assert actual_lexical == expected_lexical, slot + ' BM25F'
        assert actual_vector == expected_vector, slot + ' cosine'
        assert lazy.audit_cosine(reader, vector, allowed, actual_vector, proof) is True
        def fused(a, b):
            return reciprocal_rank_fusion([[v['document_id'] for v in a], [v['document_id'] for v in b]], k=30)
        assert fused(actual_lexical, actual_vector) == fused(expected_lexical, expected_vector)
        result[slot] = {'bm25f_rows': len(actual_lexical), 'cosine_rows': len(actual_vector),
            'ranks_and_scores_equal': True, 'cosine_proof_sha256': c.digest(proof),
            'query_sha256': row['text_sha256']}
        print(json.dumps({'oracle_role_complete': slot}), flush=True)
    metrics = dict(reader.metrics)
    assert metrics['cache_peak_bytes'] <= 64 * 1024 * 1024
    assert len(reader.descriptors) <= 64
    reader.close()
    save('OFFLINE-ORACLE.json', {'status': 'PASS', 'roles': result, 'positive_candidates': len(allowed),
        'search_scope': 'whole_shared_positive_corpus', 'tag_filter': False,
        'reader_metrics': metrics, 'elapsed_seconds': round(time.monotonic() - started, 3),
        'boundary': 'Offline technical full-scan comparison; no new semantic candidate review or model inference.',
        'Gemini_calls': 0})


if __name__ == '__main__':
    main()
