"""Re-embed only381 changed phrase projections, using the installed local model.

No meaning/tag adjudication, external provider, model download or source rewrite.
The actual lookup is a low-level phrase-consumer regression, not a final
core-bound slot-quality oracle or candidate adoption certificate.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
OUT = HERE / 'named-phrase-local-runtime-01'
OUT.mkdir(exist_ok=False)
sys.path[:0] = [str(SKILL / 'scripts'), str(SKILL / 'precore')]
import build_shared_candidate_index as builder
import photo_candidate_corpus as c
import photo_embedding_provider as provider
import photo_global_index as documents
import photo_sharded_search as search
from bm25f_retrieval import reciprocal_rank_fusion
from photo_search_reader import SearchReader
from photo_runtime_sources import source_update, SnapshotPublisher, RuntimeSnapshotProvider


def save(name, value):
    with (OUT / name).open('x') as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write('\n')


tests = json.loads((HERE / 'memberA-phrase-root-integration-01/ROOT-TESTS.json').read_bytes())
assert tests['failures'] == tests['errors'] == tests['skips'] == 0
for name, sha in tests['frozen_code_and_tests'].items():
    assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == sha
assets = SKILL / 'assets'
source = c.load(assets)
assert c.digest(source) == '125d3527c728fbdee9ebdc915dc21ae0d84c8e379dd928e0012ff9df039e701b'
space = provider.default_space()
assert space['provider'] == 'embeddinggemma2-local' and space['dimensions'] == 768
old = SearchReader(assets)
old_manifest = copy.deepcopy(old.manifest)
assert old_manifest['space'] == space
assert old_manifest['layout_id'] == 'f82ab43bc2a5a141ad1aedcc1f415b68737b9e5867af829a6c88d6750f27a285'
old_recipes = copy.deepcopy(old.meta['vector_recipes'])
positive = set(old.meta['positive_ids'])
old.close()
changed = set()
for cid in positive:
    recipe, body = documents.text(source['candidates'][cid])
    before = old_recipes[cid]
    if recipe != before['recipe'] or hashlib.sha256(body.encode()).hexdigest() != before['text_sha256']:
        changed.add(cid)
assert len(positive) == 18180 and len(changed) == 381
save('PREVIOUS-INDEX-MANIFEST.json', old_manifest)
save('PREFLIGHT.json', {
    'source_sha256': c.digest(source), 'space': space, 'changed_document_ids': sorted(changed),
    'changed_projection_documents': 381, 'expected_unchanged_vector_reuse': 17799,
    'os_network_denied': True, 'provider_keys_removed': True,
    'new_model_downloads_permitted': False, 'gemini_permitted': False,
    'canonical_source_or_tags_changed': False,
})
original_many = builder.embed_many
submitted, traces = [], []


def only_reviewed_local_many(texts, bindings, cache, *, space=None, kind='query'):
    assert space == provider.default_space() and space['provider'] == 'embeddinggemma2-local'
    assert kind == 'document' and len(texts) == len(bindings)
    for text, binding in zip(texts, bindings, strict=True):
        cid = binding['candidate_id']
        assert cid in changed and cid not in submitted
        recipe, actual = documents.text(source['candidates'][cid])
        assert text == actual and binding['recipe'] == recipe == documents.PHRASE_RECIPE
        submitted.append(cid)
    result = original_many(texts, bindings, cache, space=space, kind=kind)
    for text, binding, row in zip(texts, bindings, result, strict=True):
        provider.validate_execution(row['execution'], space, text, row['vector'], 'document')
        traces.append({'candidate_id': binding['candidate_id'], 'cache_hit': row['cache_hit'],
                       'execution': row['execution'], 'vector_sha256': row['vector_sha256']})
    return result


def forbidden_single(*args, **kwargs):
    raise AssertionError('build must use only the explicitly checked local document batches')


builder.embed_many = only_reviewed_local_many
builder.embed = forbidden_single
started = time.monotonic()
with source_update(SKILL):
    built = builder.build(assets, OUT / 'build-cache', space=space)
assert set(submitted) == changed and len(submitted) == 381
assert built['vector_reuse'] == 17799
assert built['provider_calls'] + built['provider_cache_hits'] == 381
assert c.digest(c.load(assets)) == c.digest(source)
current = SearchReader(assets)
for cid in positive - changed:
    assert current.meta['vector_recipes'][cid] == old_recipes[cid], cid
for cid in changed:
    recipe, body = documents.text(source['candidates'][cid])
    assert current.meta['vector_recipes'][cid]['recipe'] == recipe
    assert current.meta['vector_recipes'][cid]['text_sha256'] == hashlib.sha256(body.encode()).hexdigest()
current.close()
save('DOCUMENT-EXECUTIONS.json', {'documents': traces, 'local_inputs': sum(not row['cache_hit'] for row in traces),
    'cache_hits': sum(row['cache_hit'] for row in traces), 'gemini_calls': 0})
published = SnapshotPublisher(SKILL).publish()
runtime = RuntimeSnapshotProvider(SKILL)
snapshot = runtime.acquire()
reader = snapshot.data.reader
assert snapshot.cache_status == 'lazy_verified'
cid = 'cand_ac39d8f9844c5239a4e7f3937233fd91'
assert reader.record(cid) == source['candidates'][cid]
before_query_io = dict(reader.metrics)
query = 'deep inside a lush summer fruit orchard with vines and wet grass'
query_row = provider.embed(query, {'purpose': 'exact-named-phrase-consumer-regression', 'language': 'en'},
                           OUT / 'query-cache', space=space, kind='query')
assert query_row['cache_hit'] is False
provider.validate_execution(query_row['execution'], space, query, query_row['vector'], 'query')
lexical = search.lexical_rank(reader, {'slot_focus': query}, positive, 384)
vector, proof = search.cosine_rank(reader, query_row['vector'], positive, 384)
assert search.audit_cosine(reader, query_row['vector'], positive, vector, proof)
fused = reciprocal_rank_fusion([[row['document_id'] for row in lexical], [row['document_id'] for row in vector]], k=30)
lexical_hit = next(row for row in lexical if row['document_id'] == cid)
assert 'deep' in lexical_hit['matched_terms'] and 'inside' in lexical_hit['matched_terms']
assert any(row['document_id'] == cid for row in vector)
assert any(row['document_id'] == cid for row in fused)
query_evidence = {'query': query, 'query_execution': query_row['execution'], 'query_vector_sha256': query_row['vector_sha256'],
    'query_cache_hit': False, 'positive_pool_size': len(positive), 'tag_partition_or_filter_used': False,
    'lexical': lexical, 'cosine': vector, 'cosine_proof': proof, 'cosine_pruning_audit': True, 'rrf': fused,
    'io_before_query': before_query_io, 'io_after_query_and_pruning_audit': dict(reader.metrics),
    'boundary': 'Whole-positive-pool low-level functional lookup using an actually present phrase; no native core, slot spec context, role approval, candidate adoption or pixels.'}
save('QUERY-CONSUMER-VERIFICATION.json', query_evidence)
report = {'schema': 'photo-root-named-phrase-local-runtime-integration/v1', 'actor': '/root',
    'source_sha256': c.digest(source), 'canonical_source_or_bindings_changed': False,
    'operating_record_count': 18250, 'operating_catalog_count': 139, 'research146_activated': False,
    'build': built, 'changed_projection_documents': 381, 'unchanged_vector_entries_byte_identity': 17799,
    'fresh_local_document_inference_inputs': sum(not row['cache_hit'] for row in traces),
    'fresh_local_query_inference_inputs': 1, 'publication': published,
    'actual_acquire': {'generation_id': snapshot.generation_id, 'cache_status': snapshot.cache_status,
        'exact_phrase_source_payload_match': True},
    'low_level_bm25_cosine_rrf_and_pruning_verification': True,
    'whole146_core_bound_slot_retrieval_or_semantic_quality_complete': False,
    'operational_native_qualified_records': 0, 'pixels_verified': False,
    'os_network_denied': True, 'provider_keys_removed': True, 'gemini_calls': 0,
    'elapsed_seconds': time.monotonic() - started}
save('VERIFICATION.json', report)
reader.close()
print(json.dumps({'layout_id': built['layout_id'], 'generation_id': snapshot.generation_id,
    'local_document_inputs': report['fresh_local_document_inference_inputs'], 'local_query_inputs': 1,
    'vector_reuse': built['vector_reuse'], 'phrase_bm25_rank': 1 + next(i for i,row in enumerate(lexical) if row['document_id'] == cid),
    'gemini_calls': 0, 'operational_native_qualified': 0}))
