"""Exercise the current 149-slot local runtime without changing its sources/index.

Writes evidence and normal runtime query caches/receipts. This is a functional
synthetic-fixture check, not a semantic quality benchmark or adoption approval.
Run with the project Python to keep the local model in its pinned pipe worker.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.abc
import json
import os
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[4]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
FIXTURE = ROOT / 'docs/research-evidence/photo-prompt/shared-candidate-pool-20261012/stage01/inputs/dev-02-blue-cup-en'
DENIED = {'requests', 'httpx', 'google', 'openai', 'anthropic'}


class NoRemoteProvider(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in DENIED:
            raise RuntimeError('Remote provider/HTTP imports forbidden in verifier: ' + fullname)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--core', type=Path, help='Frozen core file; sibling fixture files are used by default.')
    parser.add_argument('--controls', type=Path)
    parser.add_argument('--envelope', type=Path)
    parser.add_argument('--embodiment', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--query-cache', type=Path)
    parser.add_argument('--runtime-store', type=Path)
    parser.add_argument('--expected-generation')
    args = parser.parse_args()
    started = time.monotonic()
    if any(name.split('.')[0] in DENIED for name in sys.modules):
        raise RuntimeError('Remote provider/HTTP module already loaded')
    sys.meta_path.insert(0, NoRemoteProvider())
    sys.dont_write_bytecode = True
    for key in ('HF_HUB_OFFLINE', 'TRANSFORMERS_OFFLINE'):
        os.environ[key] = '1'
    # The child inherits these removals and offline settings.
    for key in ('GEMINI_API_KEY', 'GOOGLE_API_KEY', 'OPENAI_API_KEY', 'ANTHROPIC_API_KEY'):
        os.environ.pop(key, None)
    sys.path[:0] = [str(SKILL / 'scripts'), str(SKILL / 'precore')]
    import photo_candidate_corpus as c
    import photo_embedding_provider as embeddings
    import photo_local_embedding as local
    import photo_slot_queries as queries
    import prompt_generator as generator
    import audit_global_retrieval as independent
    from photo_runtime_sources import RuntimeSnapshotProvider

    args.output = args.output.resolve()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.exists():
        raise FileExistsError('Preserve previous report: ' + str(args.output))
    evidence = args.output.parent / (args.output.stem + '-evidence')
    evidence.mkdir(exist_ok=False)

    def save(name, value):
        raw = c.canonical_bytes(value) + b'\n'
        if len(raw) > 1024 * 1024:
            name += '.gz'
            raw = gzip.compress(raw, mtime=0)
        path = evidence / name
        with path.open('xb') as handle:
            handle.write(raw)
        return {'file': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}

    core_path = (args.core or FIXTURE / 'authorial-core.json').resolve()
    fixture = core_path.parent
    paths = {'core': core_path,
             'controls': (args.controls or fixture / 'creative-controls.json').resolve(),
             'envelope': (args.envelope or fixture / 'request-envelope.json').resolve(),
             'embodiment': (args.embodiment or fixture / 'embodiment-review.json').resolve()}
    inputs = {key: {'file': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
              for key, path in paths.items()}
    controls = c.decode(paths['controls'].read_bytes())
    core = generator.load_authorial_core_arg(paths['core'],
        request_envelope=generator.load_request_envelope_arg(paths['envelope']),
        creative_control_snapshot=controls)
    embodiment = c.decode(paths['embodiment'].read_bytes())
    space = embeddings.default_space()
    lock = local.runtime_lock()
    assert space['provider'] == 'embeddinggemma2-local' and space == lock['space']
    # Direct model imports may require HTTP helper libraries. A separate pinned
    # worker permits this parent to deny those imports while OS sandboxing both.
    assert Path(sys.prefix).resolve() != (SKILL / lock['python']).parents[1].resolve(), \
        'Use project .venv/bin/python so the pinned local pipe worker owns model imports'
    provider = RuntimeSnapshotProvider(SKILL, args.runtime_store)
    snapshot = provider.acquire(bootstrap=False)
    if args.expected_generation:
        assert snapshot.generation_id == args.expected_generation
    reader = snapshot.data.reader
    assert reader.manifest['space'] == space
    assert snapshot.cache_status == 'lazy_verified'
    slots = sorted(snapshot.data['slot_catalog'])
    assert len(slots) == len(set(slots)) == 149
    metrics_acquired = dict(reader.metrics)
    assert metrics_acquired['vector_reads'] == metrics_acquired['payload_reads'] == 0
    positive = list(reader.meta['positive_ids'])
    assert len(positive) == len(set(positive))
    context = queries.prepare(core, controls, snapshot.data['slot_catalog'], slots,
        args.query_cache or evidence / 'query-cache', space=space)
    queries.validate_set(context, core, controls, snapshot.data['slot_catalog'], slots, space=space)
    context_ref = save('QUERY-CONTEXT.json', context)
    print(json.dumps({'local_query_vectors_ready': len(context['slots']), 'generation_id': snapshot.generation_id}), flush=True)
    pack = generator.generate_candidate_pack(snapshot.data, core, controls, embodiment,
        seed=0, query_context=context, requested_slots=slots, retrieval_mode='hybrid_required')
    metrics_pack = dict(reader.metrics)
    pack_ref = save('CANDIDATE-PACK.json', pack)
    receipt = provider.receipt(snapshot, pack)
    receipt_ref = save('ISSUED-RECEIPT.json', receipt)
    replay = provider.from_receipt(pack, receipt)
    assert replay.generation_id == snapshot.generation_id
    failures = independent.audit(pack, replay.data, replay.query_context)
    assert not failures, failures
    retrieval = pack['global_retrieval']
    assert retrieval['mode'] == 'hybrid_required' and retrieval['tag_admission_filter'] is False
    assert retrieval['active_slot_ids'] == retrieval['requested_slot_ids'] == slots
    assert set(retrieval['slot_searches']) == set(slots)
    query_hashes = set()
    traces = {}
    for slot in slots:
        row, trace = context['slots'][slot], retrieval['slot_searches'][slot]
        assert row['space'] == space and trace['state'] == 'executed'
        assert trace['search_scope'] == 'whole_shared_positive_corpus'
        assert trace['tag_admission_filter'] is False
        assert trace['query_sha256'] == row['text_sha256']
        assert trace['slot_spec_sha256'] == row['binding']['slot_spec_sha256']
        assert trace['eligible_candidates'] == retrieval['eligible_candidates']
        assert trace['lanes']['bm25f']['state'] == trace['lanes']['embedding']['state'] == 'executed'
        assert trace['cosine_proof'] is not None and trace['lane_limit'] >= 384
        query_hashes.add(row['text_sha256'])
        traces[slot] = {'query_sha256': row['text_sha256'], 'slot_spec_sha256': trace['slot_spec_sha256'],
            'query_context_sha256': row['canonical_sha256'], 'cache_hit': row['cache_hit'],
            'eligible_candidates': trace['eligible_candidates'], 'lane_limit': trace['lane_limit'],
            'bm25f_hits': trace['lanes']['bm25f']['positive_hits'],
            'embedding_hits': trace['lanes']['embedding']['positive_hits'],
            'cosine_proof_sha256': c.digest(trace['cosine_proof']), 'role_block_reason': trace['role_block_reason']}
    assert len(query_hashes) == 149
    assert reader.cache_limit == 64 * 1024 * 1024 and len(reader.descriptors) <= 64
    assert reader.metrics['cache_peak_bytes'] <= reader.cache_limit
    assert not any(name.split('.')[0] in DENIED for name in sys.modules)
    report = {'schema': 'photo-slot149-reduced-runtime-verification/v1', 'status': 'PASS',
        'generation_id': snapshot.generation_id, 'source_fingerprint': snapshot.manifest['source_fingerprint'],
        'corpus_sha256': reader.manifest['corpus_sha256'], 'layout_id': reader.manifest['layout_id'],
        'embedding_space': space, 'model_worker_python': str(SKILL / lock['python']),
        'verifier_python': sys.executable, 'parent_remote_provider_imports': 0,
        'provider_keys_removed': True, 'offline_environment': True,
        'network_boundary': 'OS network denial must be supplied by the invoking sandbox; import guard covers the verifier parent',
        'frozen_inputs': inputs, 'requested_slots': 149, 'independent_query_hashes': len(query_hashes),
        'positive_population': len(positive), 'source_records': len(reader.meta['record_sha256']),
        'eligible_population_after_intrinsic_guards': retrieval['eligible_candidates'],
        'search_scope': 'whole_shared_positive_corpus', 'tag_admission_filter': False,
        'independent_retrieval_audit_failures': failures, 'issued_receipt_replayed': True,
        'artifacts': {'pack': pack_ref, 'receipt': receipt_ref, 'query_context': context_ref},
        'per_slot': traces, 'reader_metrics_at_acquire': metrics_acquired,
        'reader_metrics_after_pack': metrics_pack, 'reader_metrics_after_receipt': dict(reader.metrics),
        'replay_reader_metrics': dict(replay.data.reader.metrics),
        'cache_limit_bytes': reader.cache_limit, 'descriptor_count': len(reader.descriptors),
        'vector_shards': len(reader.meta['vector_shards']), 'payload_shards': len(reader.meta['payload_shards']),
        'query_cache_hits': sum(row['cache_hit'] for row in context['slots'].values()),
        'elapsed_seconds': round(time.monotonic() - started, 3),
        'quality_review_required': True, 'whole_corpus_semantic_approval': False,
        'boundary': 'One frozen synthetic maintenance core; functional retrieval, index bindings and lazy reader limits only. No full benchmark, new persistent bindings, candidate adoption, render or pixel-quality claim.'}
    with args.output.open('xb') as handle:
        handle.write(c.canonical_bytes(report) + b'\n')
    reader.close()
    replay.data.reader.close()
    print(json.dumps({'status': report['status'], 'report': str(args.output), 'slots': 149,
                      'quality_review_required': True}), flush=True)


if __name__ == '__main__':
    main()
