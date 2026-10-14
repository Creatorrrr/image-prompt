"""Root's exact StageA neutral member inventory and named phrase regressions."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sys
import time
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = HERE / 'memberA-phrase-root-integration-01'
OUT.mkdir(exist_ok=False)
sys.path.insert(0, str(ROOT))
MODULES = ['tests.test_photo_existing_member_scope_witnesses', 'tests.test_photo_native_fact_wire', 'tests.test_photo_native_v4_guards', 'tests.test_photo_workflow_precore', 'tests.test_photo_creative_control_wire_replay', 'tests.test_photo_precore_feature_selection', 'tests.test_photo_named_phrase_fields', 'tests.test_photo_semantic_evidence', 'tests.test_photo_semantic_reference_units', 'tests.test_photo_semantic_reference_workflow', 'tests.test_photo_native_owner_selection', 'tests.test_photo_native_object_ownership', 'tests.test_photo_native_wardrobe_owners', 'tests.test_photo_global_index', 'tests.test_photo_search_layout', 'tests.test_photo_search_reader']
production = ROOT / 'skills/photo-prompt-image-generator/scripts/photo_semantic_evidence.py'
before_sha = hashlib.sha256(production.read_bytes()).hexdigest()
assert before_sha == '309876bbe95adcddbf9d4c84d7b68791f7d5f731a10d0a2cab42913482168ac7'

PINNED = {'skills/photo-prompt-image-generator/precore/photo_semantic_witnesses.py': 'cc9bfca271ae1650c28a08b379bc84030b38a5cbcf9918c18d55d50a93094a58', 'skills/photo-prompt-image-generator/precore/photo_authoring_wire.py': '6a0b55830d171a8be46e225c226c15f0cd95ca41cbfba3ee68180c4cebe35964', 'skills/photo-prompt-image-generator/scripts/photo_semantic_evidence.py': '309876bbe95adcddbf9d4c84d7b68791f7d5f731a10d0a2cab42913482168ac7', 'skills/photo-prompt-image-generator/scripts/photo_global_index.py': '905ba7178acc49fd2ecbd7350a3c88d7b467273b05ae3221077590e59aff7275', 'tests/test_photo_existing_member_scope_witnesses.py': 'c655c483b2e08628156346dc3d33bffc4b02da4a180fbb86bbd983dccb2dbcff', 'tests/test_photo_named_phrase_fields.py': '41107c204afef7be1999b39497f95d767d5ad1a9bd5f000cf06b46207148ffdf'}
for path, sha in PINNED.items():
    assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == sha, path


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

PINNED = {'skills/photo-prompt-image-generator/precore/photo_semantic_witnesses.py': 'cc9bfca271ae1650c28a08b379bc84030b38a5cbcf9918c18d55d50a93094a58', 'skills/photo-prompt-image-generator/precore/photo_authoring_wire.py': '6a0b55830d171a8be46e225c226c15f0cd95ca41cbfba3ee68180c4cebe35964', 'skills/photo-prompt-image-generator/scripts/photo_semantic_evidence.py': '309876bbe95adcddbf9d4c84d7b68791f7d5f731a10d0a2cab42913482168ac7', 'skills/photo-prompt-image-generator/scripts/photo_global_index.py': '905ba7178acc49fd2ecbd7350a3c88d7b467273b05ae3221077590e59aff7275', 'tests/test_photo_existing_member_scope_witnesses.py': 'c655c483b2e08628156346dc3d33bffc4b02da4a180fbb86bbd983dccb2dbcff', 'tests/test_photo_named_phrase_fields.py': '41107c204afef7be1999b39497f95d767d5ad1a9bd5f000cf06b46207148ffdf'}
for path, sha in PINNED.items():
    assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == sha, path

report = {'schema': 'photo-root-memberA-and-named-phrase-regression/v1', 'actor': '/root',
    'frozen_code_and_tests': PINNED, 'modules': MODULES, 'test_executions': result.testsRun, 'unique_test_ids': len(set(result.ids)),
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
