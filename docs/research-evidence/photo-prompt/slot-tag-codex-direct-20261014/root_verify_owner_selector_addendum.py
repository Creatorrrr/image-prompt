"""Independently verify the frozen two-file actual-owner conflict addendum.

Run with env -i and OS network denial. Preserve the pre-addendum 335-test
evidence; this focused rerun and the actual runtime rebuild are fresh evidence.
This helper authors no candidate meaning, approval, tag, or proof.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(ROOT), str(ROOT / 'skills/photo-prompt-image-generator/scripts')]
INITIAL = HERE / 'worker-notes/native-owner-selector-final-handoff-20261014.json'
ADDENDUM = HERE / 'worker-notes/native-resolved-assignment-handoff-addendum-20261014.json'


def digest_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write('\n')


def frozen_files():
    if digest_file(INITIAL) != '0391a89847297d31bc15015eed8e51af5e07e91f5ead44a8a2590ac24b03275e':
        raise ValueError('initial handoff changed')
    if digest_file(ADDENDUM) != '93df9c03a19b8fa1d98a40ebffcd6d6a46f2320e987483d96dfd91d7d3debe3b':
        raise ValueError('addendum handoff changed')
    expected = {row['path']: row['after_sha256']
                for row in json.loads(INITIAL.read_text())['changed_code_files']}
    for row in json.loads(ADDENDUM.read_text())['changed_files']:
        if expected[row['path']] != row['before_sha256']:
            raise ValueError('addendum does not extend initial handoff')
        expected[row['path']] = row['after_sha256']
    for name, expected_sha in expected.items():
        if digest_file(ROOT / name) != expected_sha:
            raise ValueError('frozen code changed: ' + name)
    return expected


def tests():
    names = '''test_photo_native_owner_selection test_photo_semantic_evidence
        test_photo_native_compound_evidence test_photo_native_adoption
        test_photo_native_v4_guards test_photo_candidate_realizations
        test_photo_global_retrieval test_photo_global_retrieval_audit
        test_photo_workflow_precore test_photo_workflow_state
        test_photo_workflow_transport_bindings test_photo_native_fact_wire
        test_photo_candidate_corpus test_photo_realization_content
        test_photo_slot_semantics test_photo_direct_native_reviews
        test_photo_direct_native_adoption test_photo_prepare_native_inputs
        test_photo_api_render_preflight test_photo_workflow_runtime_bridge'''.split()

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

    before = frozen_files()
    started = time.monotonic()
    log = HERE / 'NATIVE-OWNER-ADDENDUM-ROOT-TESTS.log'
    with log.open('x') as stream:
        result = unittest.TextTestRunner(stream=stream, verbosity=2, resultclass=Counted).run(
            unittest.defaultTestLoader.loadTestsFromNames(['tests.' + name for name in names]))
    if frozen_files() != before:
        raise ValueError('code changed during tests')
    report = {
        'schema': 'photo-native-owner-addendum-root-tests/v1', 'modules': names,
        'test_executions': result.testsRun, 'unique_test_ids': len(result.identities),
        'subtests': result.subtests, 'failures': len(result.failures),
        'errors': len(result.errors), 'skips': len(result.skipped),
        'elapsed_seconds': round(time.monotonic() - started, 3),
        'log_sha256': digest_file(log), 'frozen_code_files': before,
        'pre_addendum_broad_evidence': 'NATIVE-OWNER-ROOT-TEST-VERIFICATION.json',
        'os_network_denied': True, 'provider_keys_removed': True,
        'provider_or_inference_calls': 0, 'canonical_source_changes': False,
        'operational_qualified_records': 0,
    }
    save(HERE / 'NATIVE-OWNER-ADDENDUM-ROOT-TEST-VERIFICATION.json', report)
    print(json.dumps(report), flush=True)
    if not result.wasSuccessful():
        raise SystemExit(1)


def runtime():
    before = frozen_files()
    evidence = HERE / 'native-owner-selector-addendum-integration-01'
    evidence.mkdir(exist_ok=False)
    spec = importlib.util.spec_from_file_location('root_v4_runtime_procedure', HERE / 'root_verify_native_v4.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.HERE = evidence
    module.runtime()
    if frozen_files() != before:
        raise ValueError('code changed during runtime rebuild')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['tests', 'runtime'])
    args = parser.parse_args()
    {'tests': tests, 'runtime': runtime}[args.action]()
