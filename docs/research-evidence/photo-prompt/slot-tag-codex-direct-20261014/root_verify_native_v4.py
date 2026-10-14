"""Root's explicit offline v4 checks and zero-inference production rebuild.

Invoke with env -i and an OS network-deny profile. This never authors candidate
meaning, roles or proofs. Runtime mode preserves the canonical source exactly.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
import time
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path[:0] = [str(ROOT), str(SKILL / 'scripts')]


def save(path, value):
    if path.exists():
        raise ValueError('preserve previous evidence: ' + str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n')


def tests():
    names = '''test_photo_semantic_evidence test_photo_native_fact_wire
        test_photo_native_compound_evidence test_photo_native_adoption
        test_photo_candidate_corpus test_photo_candidate_realizations
        test_photo_realization_content test_photo_slot_semantics
        test_photo_slot_workflow test_photo_native_runtime_freshness
        test_photo_workflow_precore test_photo_global_retrieval
        test_photo_search_layout test_photo_slot_queries test_photo_slot_retrieval
        test_photo_global_retrieval_audit test_photo_native_wardrobe_owners
        test_photo_native_v4_guards test_photo_direct_native_reviews
        test_photo_direct_native_adoption test_photo_prepare_native_inputs
        test_photo_api_render_preflight'''.split()

    class Counted(unittest.TextTestResult):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.identities = set()
            self.subtests = 0

        def startTest(self, test):
            self.identities.add(test.id())
            super().startTest(test)

        def addSubTest(self, test, subtest, err):
            self.subtests += 1
            super().addSubTest(test, subtest, err)

    started = time.monotonic()
    log = HERE / 'NATIVE-V4-ROOT-TESTS.log'
    if log.exists():
        raise ValueError('preserve previous test log')
    with log.open('w') as stream:
        result = unittest.TextTestRunner(stream=stream, verbosity=2, resultclass=Counted).run(
            unittest.defaultTestLoader.loadTestsFromNames(['tests.' + name for name in names]))
    report = {
        'schema': 'photo-native-v4-root-tests/v1', 'modules': names,
        'test_executions': result.testsRun, 'unique_test_ids': len(result.identities),
        'subtests': result.subtests, 'failures': len(result.failures),
        'errors': len(result.errors), 'skips': len(result.skipped),
        'elapsed_seconds': round(time.monotonic() - started, 3),
        'log_sha256': hashlib.sha256(log.read_bytes()).hexdigest(),
        'os_network_denied': True, 'provider_keys_removed': True,
        'provider_or_inference_calls': 0, 'canonical_source_changes': False,
        'operational_qualified_records': 0,
    }
    save(HERE / 'NATIVE-V4-ROOT-TEST-VERIFICATION.json', report)
    print(json.dumps(report), flush=True)
    if not result.wasSuccessful():
        raise SystemExit(1)


def runtime():
    import build_shared_candidate_index as builder
    import photo_candidate_corpus as corpus
    import photo_embedding_provider as provider
    import photo_search_layout as layout
    from photo_runtime_sources import source_update, SnapshotPublisher, RuntimeSnapshotProvider

    out = HERE / 'native-v4-runtime-01'
    out.mkdir(exist_ok=False)
    started = time.monotonic()
    assets = SKILL / 'assets'
    original = corpus.load(assets)
    source_sha = corpus.digest(original)
    if source_sha != '125d3527c728fbdee9ebdc915dc21ae0d84c8e379dd928e0012ff9df039e701b':
        raise ValueError('canonical source changed before explicit root rebuild')
    space = provider.default_space()
    if space['provider'] != 'embeddinggemma2-local':
        raise ValueError('local embedding space required; no provider fallback')
    positive = sum(record['record_kind'] != 'diagnostic' for record in original['candidates'].values())
    save(out / 'PREFLIGHT.json', {
        'schema': 'photo-native-v4-zero-inference-build-preflight/v1',
        'source_sha256': source_sha, 'positive_count': positive, 'space': space,
        'expected_exact_same_space_vector_reuse': positive,
        'planned_fresh_document_inputs': 0, 'provider_execution_forbidden': True,
        'gemini_calls': 0,
    })
    attempted_calls = []

    def forbidden(*args, **kwargs):
        attempted_calls.append(True)
        raise RuntimeError('root rebuild forbids every embedding/provider invocation')

    builder.embed = forbidden
    builder.embed_many = forbidden
    provider.embed = forbidden
    provider.embed_many = forbidden
    with source_update(SKILL):
        built = builder.build(assets, out / 'build-cache', space=space)
        if built['vector_reuse'] != positive or built['provider_calls'] or built['provider_cache_hits'] or attempted_calls:
            raise ValueError('zero-inference exact vector reuse failed')
    published = SnapshotPublisher(SKILL).publish()
    active = RuntimeSnapshotProvider(SKILL)
    snapshot = active.acquire()
    cid = sorted(original['candidates'])[0]
    actual = snapshot.data.reader.record(cid)
    if corpus.digest(actual) != corpus.digest(original['candidates'][cid]):
        raise ValueError('actual acquired payload does not match canonical source')
    if corpus.digest(corpus.load(assets)) != source_sha:
        raise ValueError('canonical source changed during runtime verification')
    report = {
        'schema': 'photo-native-v4-runtime-integration-verification/v1',
        'source_sha256': source_sha, 'canonical_record_count': len(original['candidates']),
        'canonical_slot_count': len(original['slot_catalog']), 'positive_count': positive,
        'canonical_native_qualified_records': sum(
            'role_evidence' in record['content'] for record in original['candidates'].values()),
        'canonical_source_or_bindings_changed': False,
        'build': built, 'publication': published,
        'actual_acquire': {
            'generation_id': snapshot.generation_id, 'cache_status': snapshot.cache_status,
            'mode': 'local_current', 'source_fingerprint': snapshot.manifest['source_fingerprint'],
            'source_record_id': cid, 'source_record_sha256': corpus.digest(actual),
            'exact_source_record_match': True,
        },
        'reader_io_after_acquire_and_one_payload': dict(snapshot.data.reader.metrics),
        'elapsed_seconds': round(time.monotonic() - started, 3),
        'provider_keys_removed': True, 'os_network_denied': True,
        'fresh_local_inference_inputs': 0, 'embedding_attempts': len(attempted_calls),
        'gemini_calls': 0, 'native_code_and_fixture_integration_complete': True,
        'runtime_core_bound_hybrid_query_verified': False,
        'full_corpus_native_qualification_complete': False, 'stages05_08_complete': False,
    }
    save(out / 'VERIFICATION.json', report)
    print(json.dumps(report), flush=True)
    snapshot.data.reader.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['tests', 'runtime'])
    args = parser.parse_args()
    {'tests': tests, 'runtime': runtime}[args.action]()
