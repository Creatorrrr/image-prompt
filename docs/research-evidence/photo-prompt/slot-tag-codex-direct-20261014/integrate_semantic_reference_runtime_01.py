"""Publish tested metadata with zero embedding/provider invocations.

Reuse the pinned prior root rebuild implementation with a new evidence root.
The operating source/catalog remain unchanged and every vector is reused only
through the builder's verified same-space full-text identity checks.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = HERE / 'semantic-reference-integration-01'
tests = json.loads((OUT / 'ROOT-TESTS.json').read_bytes())
assert tests['failures'] == tests['errors'] == tests['skips'] == 0
assert tests['production_unchanged_during_tests'] is True
module_path = ROOT / 'skills/photo-prompt-image-generator/scripts/photo_semantic_evidence.py'
assert hashlib.sha256(module_path.read_bytes()).hexdigest() == '0f4a974435f7cb9e71a23a726f092bff73d0dd61bb9deb3df2537f59d5be15e4'
old_path = HERE / 'root_verify_native_v4.py'
spec = importlib.util.spec_from_file_location('root_preserved_runtime_verifier', old_path)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
assert helper.ROOT == ROOT
helper.HERE = OUT
helper.runtime()
report = json.loads((OUT / 'native-v4-runtime-01/VERIFICATION.json').read_bytes())
assert report['build']['vector_reuse'] == 18180
assert report['fresh_local_inference_inputs'] == report['embedding_attempts'] == report['gemini_calls'] == 0
assert report['canonical_slot_count'] == 139 and report['canonical_record_count'] == 18250
assert report['actual_acquire']['cache_status'] == 'lazy_verified'
assert report['actual_acquire']['exact_source_record_match'] is True
assert hashlib.sha256(module_path.read_bytes()).hexdigest() == '0f4a974435f7cb9e71a23a726f092bff73d0dd61bb9deb3df2537f59d5be15e4'
print(json.dumps({'metadata_runtime_verified': True, 'actual_generation_id': report['actual_acquire']['generation_id'], 'new_document_or_query_inference': 0, 'research146_catalog_activated': False, 'native_candidate_approvals': 0}))
