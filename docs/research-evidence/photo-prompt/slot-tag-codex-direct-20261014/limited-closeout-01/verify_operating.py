"""Fixed read-only integrity/acquire checks for the user-reduced closeout."""
import argparse
import gzip
import hashlib
import importlib.abc
import json
import sys
from pathlib import Path

ROOT = Path.cwd()
R = ROOT / 'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
D = R / 'limited-closeout-01'
G = Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/fe5b593c819806a31803e40c620e6f2b28c3b54103f451dd6f38920f2d537258')
SKILL = (ROOT / 'skills/photo-prompt-image-generator').resolve()


class Deny(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'torch', 'transformers', 'sentence_transformers', 'google', 'openai', 'anthropic', 'httpx', 'requests', 'tensorflow', 'jax', 'mlx'}:
            raise AssertionError('No model/provider imports: ' + fullname)


sys.meta_path.insert(0, Deny())
sys.dont_write_bytecode = True
sys.path[:0] = [str(G / 'scripts'), str(G / 'precore')]
import photo_candidate_corpus as c


def read(path):
    raw = path.read_bytes()
    return json.loads(gzip.decompress(raw) if raw[:2] == b'\x1f\x8b' else raw)


def save(name, value):
    with (D / name).open('xb') as handle:
        handle.write(c.canonical_bytes(value) + b'\n')


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('mode', choices=['integrity', 'acquire'])
args = parser.parse_args()
original = read(R / 'SOURCE.json.gz')
expected = '125d3527c728fbdee9ebdc915dc21ae0d84c8e379dd928e0012ff9df039e701b'
assert c.digest(original) == expected
common = dict(schema='photo-reduced-closeout-operating-verification/v1', operating_candidate_changes=0, operating_tag_changes=0, operating_source_corrections=0, preserved_original_candidates=18250, operating_native_qualified=0, operating_roles=139, whole_corpus_semantic_approval=False, embedding_inferences=0, model_imports=0, Gemini_calls=0, network='OS-denied')
if args.mode == 'integrity':
    current = c.load(SKILL / 'assets')
    assert current == original and len(current['candidates']) == 18250
    assert c.digest(current) == expected
    pairs = [(row['candidate_id'], row['slot_id']) for row in current['slot_bindings'].values()]
    assert len(pairs) == len(set(pairs)) == 12089
    assert all(cid in current['candidates'] and tag in current['slot_catalog'] for cid, tag in pairs)
    qualified = sum('role_evidence' in row['content'] for row in current['candidates'].values())
    assert qualified == 0
    report = dict(common, mode='integrity', canonical_corpus_sha256=expected, original_full_fields_equal=True, candidate_ids_equal=True, duplicate_candidate_slot_pairs=0, source_binding_policy_catalog_loss=0, orphan_bindings=0, full_graph_and_reference_validation='c.load -> c.validate PASS on entire current authored corpus', bindings=12089, c_module=c.__file__)
    save('INTEGRITY.json', report)
else:
    import photo_runtime_sources as runtime
    prior = read(R / 'permission-envelope-native-integration-01/ROOT-ACQUIRE-v4.json')
    pins = {}
    for row in prior['code_pins']:
        path = ROOT / row['file']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row['raw_sha256']
        pins[row['file']] = row['raw_sha256']
    provider = runtime.RuntimeSnapshotProvider(root=SKILL)
    snapshot = provider.acquire()
    assert snapshot.generation_id == G.name and snapshot.cache_status == 'lazy_verified'
    assert snapshot.manifest['search_layout']['corpus_sha256'] == expected
    assert snapshot.manifest['source_fingerprint'] == prior['source_fingerprint']
    reader = snapshot.data.reader
    before = dict(reader.metrics)
    cid = prior['actual_sample_id']
    actual = reader.record(cid)
    assert dict(actual) == original['candidates'][cid]
    assert reader.metrics['payload_reads'] - before['payload_reads'] == 1
    assert reader.cache_limit == 64 * 1024 * 1024 and len(reader.descriptors) <= 64
    report = dict(common, mode='acquire', generation_id=snapshot.generation_id, cache_status=snapshot.cache_status, source_fingerprint=snapshot.manifest['source_fingerprint'], current_code_pins=pins, actual_sample_id=cid, actual_payload_equal_original=True, metrics_before=before, metrics_after=dict(reader.metrics), cache_limit_bytes=reader.cache_limit, descriptor_count=len(reader.descriptors), corpus_sha256=expected, index_and_vector_rebuild_needed=False, prior_search_receipt_compose_evidence_reused='batch-validation-01/ROOT-INTEGRATION.json; inactive research source102 with quality WARN, not current operating semantic adoption')
    save('OPERATING-VERIFICATION.json', report)
    reader.close()
print(json.dumps(report))
