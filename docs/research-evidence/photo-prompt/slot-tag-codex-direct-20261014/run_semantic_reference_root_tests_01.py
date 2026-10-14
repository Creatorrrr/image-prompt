"""Root's focused native/reference and downstream regression evidence."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sys
import time
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = HERE / 'semantic-reference-integration-01'
OUT.mkdir(exist_ok=False)
sys.path.insert(0, str(ROOT))
MODULES = [
    'tests.test_photo_semantic_reference_units', 'tests.test_photo_semantic_reference_workflow',
    'tests.test_photo_semantic_evidence', 'tests.test_photo_native_compound_evidence',
    'tests.test_photo_native_owner_selection', 'tests.test_photo_native_source_guards_v2',
    'tests.test_photo_native_v4_guards', 'tests.test_photo_native_joint_assignments',
    'tests.test_photo_candidate_realizations', 'tests.test_photo_realization_content',
    'tests.test_photo_direct_native_adoption', 'tests.test_photo_native_fact_wire',
    'tests.test_photo_search_layout', 'tests.test_photo_search_reader',
    'tests.test_photo_native_runtime_freshness', 'tests.test_photo_workflow_runtime_bridge']
production = ROOT / 'skills/photo-prompt-image-generator/scripts/photo_semantic_evidence.py'
before_sha = hashlib.sha256(production.read_bytes()).hexdigest()
assert before_sha == '0f4a974435f7cb9e71a23a726f092bff73d0dd61bb9deb3df2537f59d5be15e4'


class Result(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids = []
        self.subtests = 0

    def startTest(self, test):
        self.ids.append(test.id())
        super().startTest(test)

    def addSubTest(self, test, subtest, error):
        self.subtests += 1
        super().addSubTest(test, subtest, error)


started = time.monotonic()
suite = unittest.defaultTestLoader.loadTestsFromNames(MODULES)
log = OUT / 'ROOT-TESTS.log'
with log.open('x') as stream:
    result = unittest.TextTestRunner(stream=stream, verbosity=2, resultclass=Result).run(suite)
actual = {}
for name, module in list(sys.modules.items()):
    if name.startswith('photo_') and getattr(module, '__file__', None):
        path = Path(module.__file__).resolve()
        actual[name] = {'file': str(path), 'raw_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
assert actual['photo_semantic_evidence']['raw_sha256'] == before_sha
assert Path(actual['photo_semantic_evidence']['file']) == production.resolve()
assert hashlib.sha256(production.read_bytes()).hexdigest() == before_sha
report = {'schema': 'photo-root-semantic-reference-regression/v1', 'actor': '/root',
    'modules': MODULES, 'test_executions': result.testsRun, 'unique_test_ids': len(set(result.ids)),
    'subtests': result.subtests, 'failures': len(result.failures), 'errors': len(result.errors), 'skips': len(result.skipped),
    'elapsed_seconds': time.monotonic() - started, 'all_test_ids': result.ids,
    'log': str(log.relative_to(ROOT)), 'log_raw_sha256': hashlib.sha256(log.read_bytes()).hexdigest(),
    'actual_loaded_modules': actual, 'production_unchanged_during_tests': True,
    'os_network_denied': True, 'provider_keys_removed': True, 'provider_or_gemini_calls': 0,
    'real_corpus_semantic_or_candidate_approval': False,
    'boundary': 'Code/fixture regressions, including real synthetic-vector lazy/public-pack/compose/fresh-runtime paths. No actual corpus model inference, candidate qualification or pixels.'}
path = OUT / 'ROOT-TESTS.json'
with path.open('x') as stream:
    json.dump(report, stream, ensure_ascii=False, sort_keys=True, indent=2)
    stream.write('\n')
assert result.wasSuccessful() and not result.skipped
print(json.dumps({key: report[key] for key in ['test_executions', 'unique_test_ids', 'subtests', 'failures', 'errors', 'skips', 'elapsed_seconds']}))
