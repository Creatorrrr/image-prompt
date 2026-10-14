"""Root's independent frozen-owner-selector tests and zero-inference rebuild.

Use keyless env-i and an OS network-deny profile. No corpus meaning is authored.
The existing v4 runtime procedure is reused under a new evidence directory;
its source identity, exact vector-space and forbidden-provider checks remain.
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
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path[:0] = [str(ROOT), str(SKILL / 'scripts')]
MANIFEST = HERE / 'worker-notes/native-owner-selector-final-handoff-20261014.json'


def save(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write('\n')


def frozen_files():
    manifest = json.loads(MANIFEST.read_text())
    hashes = {}
    for row in manifest['changed_code_files']:
        path = ROOT / row['path']
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        if sha != row['after_sha256']:
            raise ValueError('handoff code changed: ' + row['path'])
        hashes[row['path']] = sha
    return hashes


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
        test_photo_api_render_preflight test_photo_native_owner_selection
        test_photo_workflow_state test_photo_workflow_transport_bindings
        test_photo_workflow_runtime_bridge'''.split()

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
    log = HERE / 'NATIVE-OWNER-ROOT-TESTS.log'
    with log.open('x') as stream:
        result = unittest.TextTestRunner(stream=stream, verbosity=2, resultclass=Counted).run(
            unittest.defaultTestLoader.loadTestsFromNames(['tests.' + name for name in names]))
    if frozen_files() != before:
        raise ValueError('code changed during tests')
    report = {
        'schema': 'photo-native-owner-root-tests/v1', 'modules': names,
        'test_executions': result.testsRun, 'unique_test_ids': len(result.identities),
        'subtests': result.subtests, 'failures': len(result.failures),
        'errors': len(result.errors), 'skips': len(result.skipped),
        'elapsed_seconds': round(time.monotonic() - started, 3),
        'log_sha256': hashlib.sha256(log.read_bytes()).hexdigest(),
        'frozen_code_files': before, 'os_network_denied': True,
        'provider_keys_removed': True, 'provider_or_inference_calls': 0,
        'canonical_source_changes': False, 'operational_qualified_records': 0,
    }
    save(HERE / 'NATIVE-OWNER-ROOT-TEST-VERIFICATION.json', report)
    print(json.dumps(report), flush=True)
    if not result.wasSuccessful():
        raise SystemExit(1)


def runtime():
    frozen_files()
    evidence = HERE / 'native-owner-selector-integration-01'
    evidence.mkdir(exist_ok=False)
    spec = importlib.util.spec_from_file_location('root_v4_runtime_procedure', HERE / 'root_verify_native_v4.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.HERE = evidence
    module.runtime()
    frozen_files()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['tests', 'runtime'])
    args = parser.parse_args()
    {'tests': tests, 'runtime': runtime}[args.action]()
