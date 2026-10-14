"""Independently verify frozen joint effects and metadata runtime integration."""
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
HANDOFF = HERE / 'worker-notes/native-joint-assignment-handoff-20261015.json'


def raw(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write('\n')


def frozen_files():
    assert raw(HANDOFF) == 'be6b1383c0998b1e33b5eb17fab26ca5f5cf4c709ed32ec4502257897363bb62'
    handoff = json.loads(HANDOFF.read_bytes())
    expected = {}
    for row in handoff['changed_files']:
        assert raw(ROOT / row['path']) == row['raw_sha256'], row['path']
        expected[row['path']] = row['raw_sha256']
    for row in handoff['evidence']:
        assert raw(ROOT / row['path']) == row['raw_sha256'], row['path']
    for name, sha in handoff['old_diagnostic_pins_unchanged'].items():
        assert raw(HERE / 'worker-notes' / name) == sha
    unchanged = handoff['authorized_but_unchanged']
    assert raw(ROOT / unchanged['path']) == unchanged['raw_sha256']
    before = json.loads((HERE / 'worker-notes/native-joint-assignment-before-20261015/MANIFEST.json').read_bytes())
    for row in before['files']:
        saved = ROOT / row['backup_path']
        assert raw(saved) == row['raw_sha256']
        assert saved.read_bytes() == subprocess.check_output(
            ['git', 'show', '32c500c4b:' + row['path']], cwd=ROOT), row['path']
    return expected


def tests():
    names = '''test_photo_native_joint_assignments test_photo_native_source_guards_v2
        test_photo_semantic_evidence test_photo_native_compound_evidence test_photo_native_v4_guards
        test_photo_native_owner_selection test_photo_native_fact_wire test_photo_native_adoption
        test_photo_candidate_corpus test_photo_candidate_realizations test_photo_realization_content
        test_photo_global_retrieval test_photo_global_retrieval_audit test_photo_search_layout
        test_photo_slot_queries test_photo_slot_retrieval test_photo_slot_semantics
        test_photo_workflow_precore test_photo_workflow_state test_photo_workflow_transport_bindings
        test_photo_direct_native_reviews test_photo_direct_native_adoption test_photo_prepare_native_inputs
        test_photo_api_render_preflight test_photo_native_runtime_freshness test_photo_workflow_runtime_bridge'''.split()

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
    log = HERE / 'NATIVE-JOINT-ASSIGNMENTS-ROOT-TESTS.log'
    with log.open('x') as stream:
        result = unittest.TextTestRunner(stream=stream, verbosity=2, resultclass=Counted).run(
            unittest.defaultTestLoader.loadTestsFromNames(['tests.' + name for name in names]))
    assert frozen_files() == before
    report = {'schema': 'photo-native-joint-root-tests/v1', 'modules': names,
              'test_executions': result.testsRun, 'unique_test_ids': len(set(result.ids)),
              'subtests': result.subtests, 'failures': len(result.failures), 'errors': len(result.errors),
              'skips': len(result.skipped), 'elapsed_seconds': round(time.monotonic() - started, 3),
              'test_ids': result.ids, 'log_sha256': raw(log), 'frozen_code_files': before,
              'root_review': 'All three complete production diffs, complete352-line fourteen-test source, full diagnostic and frozen handoff were directly read. No semantic approval for corpus source records is granted.',
              'os_network_denied': True, 'provider_keys_removed': True,
              'provider_or_inference_calls': 0, 'gemini_calls': 0,
              'canonical_source_changes': False, 'operational_native_qualified_count': 0}
    save(HERE / 'NATIVE-JOINT-ASSIGNMENTS-ROOT-TEST-VERIFICATION.json', report)
    print(json.dumps({k: v for k, v in report.items() if k not in {'test_ids', 'frozen_code_files'}}), flush=True)
    if not result.wasSuccessful():
        raise SystemExit(1)


def runtime():
    before = frozen_files()
    passed = json.loads((HERE / 'NATIVE-JOINT-ASSIGNMENTS-ROOT-TEST-VERIFICATION.json').read_bytes())
    assert passed['frozen_code_files'] == before and not (passed['failures'] or passed['errors'] or passed['skips'])
    evidence = HERE / 'native-joint-assignment-integration-01'
    evidence.mkdir(exist_ok=False)
    spec = importlib.util.spec_from_file_location('root_joint_zero_inference_rebuild', HERE / 'root_verify_native_v4.py')
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
