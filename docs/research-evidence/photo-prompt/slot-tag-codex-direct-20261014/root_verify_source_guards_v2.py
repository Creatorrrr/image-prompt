"""Independently check the exact frozen source-target guard implementation.

Run keyless with OS network denial. This grants no source or tag approval.
Runtime mode rebuilds metadata with exact same-space vectors, then publishes
and actually acquires that generation without inference or source mutations.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import time
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(ROOT), str(ROOT / 'skills/photo-prompt-image-generator/scripts')]
HANDOFF = HERE / 'worker-notes/native-source-guards-v2-handoff-20261015.json'


def raw(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write('\n')


def frozen_files():
    if raw(HANDOFF) != 'df0c982f8f9359ea1e5f756d2a89cd85940ab164e478fa2bf6c12cba32410c2c':
        raise ValueError('frozen handoff changed')
    handoff = json.loads(HANDOFF.read_bytes())
    before_path = ROOT / handoff['before_manifest']['path']
    if raw(before_path) != handoff['before_manifest']['sha256']:
        raise ValueError('before manifest changed')
    expected = {}
    for row in handoff['changed_files']:
        path = ROOT / row['path']
        if raw(path) != row['after_sha256']:
            raise ValueError('frozen implementation changed: ' + row['path'])
        if row['before_sha256'] is not None:
            backup = before_path.parent / path.name
            head = subprocess.check_output(['git', 'show', handoff['before_manifest']['head'] + ':' + row['path']], cwd=ROOT)
            if raw(backup) != row['before_sha256'] or backup.read_bytes() != head:
                raise ValueError('before source recovery mismatch: ' + row['path'])
        expected[row['path']] = row['after_sha256']
    for row in handoff['preserved_unowned_inputs']:
        if raw(ROOT / row['path']) != row['raw_sha256']:
            raise ValueError('preserved external input changed: ' + row['path'])
    return expected


def tests():
    names = '''test_photo_native_source_guards_v2 test_photo_semantic_evidence
        test_photo_native_compound_evidence test_photo_native_v4_guards
        test_photo_native_owner_selection test_photo_native_fact_wire
        test_photo_native_adoption test_photo_candidate_corpus
        test_photo_candidate_realizations test_photo_realization_content
        test_photo_global_retrieval test_photo_global_retrieval_audit
        test_photo_search_layout test_photo_slot_queries test_photo_slot_retrieval
        test_photo_slot_semantics test_photo_workflow_precore
        test_photo_workflow_state test_photo_workflow_transport_bindings
        test_photo_direct_native_reviews test_photo_direct_native_adoption
        test_photo_prepare_native_inputs test_photo_api_render_preflight
        test_photo_native_runtime_freshness test_photo_workflow_runtime_bridge'''.split()
    for name in names:
        if not (ROOT / 'tests' / (name + '.py')).is_file():
            raise ValueError('selected regression module missing: ' + name)

    class Counted(unittest.TextTestResult):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.ids = []
            self.subtests = 0

        def startTest(self, test):
            self.ids.append(test.id())
            super().startTest(test)

        def addSubTest(self, test, subtest, err):
            self.subtests += 1
            super().addSubTest(test, subtest, err)

    before = frozen_files()
    started = time.monotonic()
    log = HERE / 'NATIVE-SOURCE-GUARDS-V2-ROOT-TESTS.log'
    with log.open('x') as stream:
        result = unittest.TextTestRunner(stream=stream, verbosity=2, resultclass=Counted).run(
            unittest.defaultTestLoader.loadTestsFromNames(['tests.' + name for name in names]))
    assert frozen_files() == before
    report = {
        'schema': 'photo-source-target-guard-root-tests/v1', 'modules': names,
        'test_executions': result.testsRun, 'unique_test_ids': len(set(result.ids)),
        'subtests': result.subtests, 'failures': len(result.failures), 'errors': len(result.errors),
        'skips': len(result.skipped), 'elapsed_seconds': round(time.monotonic() - started, 3),
        'test_ids': result.ids, 'log_sha256': raw(log), 'frozen_code_files': before,
        'root_review': 'All eight complete production diffs and the complete frozen24-test source were directly read. Intermediate truncated broad test displays were supplemented with bounded complete displays; no corpus-wide semantic approval is implied.',
        'os_network_denied': True, 'provider_keys_removed': True, 'provider_or_inference_calls': 0,
        'canonical_source_changes': False, 'operational_qualified_records': 0,
    }
    save(HERE / 'NATIVE-SOURCE-GUARDS-V2-ROOT-TEST-VERIFICATION.json', report)
    print(json.dumps({key: value for key, value in report.items() if key not in {'test_ids', 'frozen_code_files'}}), flush=True)
    if not result.wasSuccessful():
        raise SystemExit(1)


def runtime():
    before = frozen_files()
    passed = json.loads((HERE / 'NATIVE-SOURCE-GUARDS-V2-ROOT-TEST-VERIFICATION.json').read_bytes())
    assert passed['frozen_code_files'] == before and not (passed['failures'] or passed['errors'] or passed['skips'])
    evidence = HERE / 'native-source-target-guards-v2-integration-01'
    evidence.mkdir(exist_ok=False)
    spec = importlib.util.spec_from_file_location('root_v4_zero_inference_rebuild', HERE / 'root_verify_native_v4.py')
    procedure = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(procedure)
    procedure.HERE = evidence
    procedure.runtime()
    assert frozen_files() == before


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['tests', 'runtime'])
    args = parser.parse_args()
    {'tests': tests, 'runtime': runtime}[args.action]()
