"""Original horror V31 assertions and an independent archived-source receipt audit.

The frozen V31 validator never reads its generated sidecar. Its seven original
tests remain intact; the separate sidecar audit below closes that coverage gap
without changing the original validator or its 60-second generation budget.
"""
from __future__ import annotations
import contextlib
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
ILL = ROOT / 'skills/subculture-illustration-image-generator'
sys.path.insert(0, str(ILL / 'scripts'))
import validate_illustration_assets as validator
from tests import photo_prompt_fixtures as fixtures


OFFLINE_WORKER_GUARD = '''\
import builtins
import sys
def prohibit_external_access(event, args):
    if event in ('socket.connect', 'socket.getaddrinfo', 'urllib.Request',
                 'http.client.connect', 'subprocess.Popen', 'os.system', 'os.posix_spawn'):
        raise RuntimeError('Original V31 worker attempted external access: ' + event)
sys.addaudithook(prohibit_external_access)
builtins._original_v31_offline_guard = True
'''

PUBLISH_ORIGINAL_V31 = '''\
import builtins
import json
import os
from pathlib import Path
import sys
assert builtins._original_v31_offline_guard
assert Path(os.environ['PHOTO_RUNTIME_STORE']).is_absolute()
import photo_runtime_sources as runtime
assert Path(runtime.__file__).resolve() == Path.cwd() / 'skills/photo-prompt-image-generator/scripts/photo_runtime_sources.py'
pointer = runtime.SnapshotPublisher().publish()
Path(sys.argv[1]).write_text(json.dumps(pointer))
'''

AUDIT_ORIGINAL_V31 = '''\
import builtins
import copy
import hashlib
import json
import os
from pathlib import Path
import sys

assert builtins._original_v31_offline_guard
assert Path(os.environ['PHOTO_RUNTIME_STORE']).is_absolute()
import photo_runtime_sources as runtime
import prompt_generator as generator
from core_slot_index_storage import canonical_bytes, digest, json_digest

root = Path.cwd()
assert Path(runtime.__file__).resolve() == root / 'skills/photo-prompt-image-generator/scripts/photo_runtime_sources.py'
assert Path(generator.__file__).resolve() == root / 'skills/photo-prompt-image-generator/scripts/prompt_generator.py'
output, pointer_path, report_path = map(Path, sys.argv[1:])
baseline = json.loads((root / 'skills/subculture-illustration-image-generator/assets/photo_regression_baseline_v31.json').read_bytes())
official = (root / 'skills/subculture-illustration-image-generator/assets/photo_regression_baseline_v31_pack.json').read_bytes()
raw = output.read_bytes()
assert raw == official
assert hashlib.sha256(raw).hexdigest() == baseline['sha256']
pack = json.loads(raw)[0]
assert pack['pack_id'] == baseline['pack_id']
receipt_path = Path(str(output) + '.runtime-receipt.json')
receipt_raw = receipt_path.read_bytes()
receipt = json.loads(receipt_raw)
pointer = json.loads(pointer_path.read_bytes())
provider = runtime.RuntimeSnapshotProvider()
assert provider.publisher.root == root / 'skills/photo-prompt-image-generator'
assert provider.publisher.store == Path(os.environ['PHOTO_RUNTIME_STORE'])

# Supply this command's exact sidecar. A fresh process performs independent
# corpus/index rebuilding and full candidate-pack recomputation in from_receipt.
snapshot = provider.from_receipt(pack, receipt)
assert snapshot.cache_status == 'independent_audit'
assert snapshot.generation_id == pointer['generation_id'] == receipt['generation_id']
assert snapshot.manifest['source_fingerprint'] == pointer['source_fingerprint'] == receipt['source_fingerprint']
assert snapshot.manifest['algorithm_sha256'] == receipt['algorithm_sha256'] == runtime.algorithm_hash(generator)
assert snapshot.manifest['slot_cache']['slot_cache_key'] == receipt['slot_cache_key']
assert snapshot.manifest['source']['code'] == runtime.LOADED_CODE
assert snapshot.manifest['source']['environment'] == runtime.LOADED_ENVIRONMENT == runtime.environment_binding()
assert runtime.capture_sources(provider.publisher.root)[0] == snapshot.manifest['source']
assert receipt['observation']['root'] == str(provider.publisher.root)
assert receipt['observation']['mode'] == 'local_current'
assert receipt['cache_status'] == 'hit'
assert {name: digest((root / name).read_bytes()) for name in baseline['frozen_inputs']} == baseline['frozen_inputs']

rejections = []
def rejected(label, call, expected_message=None):
    try:
        call()
    except (runtime.FreshnessError, OSError, KeyError, TypeError) as exc:
        if expected_message is not None:
            assert expected_message in str(exc), (label, str(exc))
        rejections.append({'case': label, 'error': str(exc)})
    else:
        raise AssertionError('Original V31 receipt audit accepted ' + label)

def reseal_receipt(value):
    value['canonical_sha256'] = json_digest({key: item for key, item in value.items() if key != 'canonical_sha256'})
    return value

# Missing sidecars must fail rather than quietly switching to the receipt index.
receipt_path.unlink()
try:
    rejected('missing_sidecar', receipt_path.read_bytes)
finally:
    receipt_path.write_bytes(receipt_raw)
index_path = provider.publisher.store / 'receipt-index' / (json_digest(pack) + '.json')
index_raw = index_path.read_bytes()
index_path.unlink()
try:
    rejected('missing_receipt_without_index', lambda: provider.from_receipt(pack, None))
finally:
    index_path.write_bytes(index_raw)
rejected('empty_receipt', lambda: provider.from_receipt(pack, {}))
wrong = copy.deepcopy(receipt)
wrong['canonical_sha256'] = '0' * 64
rejected('receipt_checksum', lambda: provider.from_receipt(pack, wrong))
for field in ('pack_sha256', 'source_fingerprint', 'algorithm_sha256', 'slot_cache_key', 'generation_id'):
    wrong = copy.deepcopy(receipt)
    wrong[field] = '0' * 64
    reseal_receipt(wrong)
    rejected('receipt_' + field, lambda wrong=wrong: provider.from_receipt(pack, wrong))
wrong = copy.deepcopy(receipt)
wrong['bindings']['tags_hash'] = '0' * 64
reseal_receipt(wrong)
rejected('receipt_bindings', lambda: provider.from_receipt(pack, wrong))
for label, store in (('empty_store', output.parent / 'empty-store'),
                     ('wrong_store', provider.publisher.store / 'source-data')):
    store.mkdir(exist_ok=True)
    rejected(label, lambda store=store: runtime.RuntimeSnapshotProvider(store=store).from_receipt(pack, receipt))

# Rehash the forged manifests and receipts so these checks reach the independent
# source and loaded-code comparisons, beyond the outer checksum protections.
for kind in ('source', 'code'):
    manifest = copy.deepcopy(snapshot.manifest)
    staging = output.parent / ('forged-' + kind)
    staging.mkdir()
    for name in manifest['members']:
        target = staging / name
        target.parent.mkdir(parents=True, exist_ok=True)
        os.link(snapshot.root / name, target)
    if kind == 'source':
        name = 'assets/photo_prompt_religion_iconography_extension.json'
        manifest['source']['files'][name] = '0' * 64
    else:
        name = 'scripts/photo_runtime_sources.py'
        target = staging / name
        payload = target.read_bytes() + b'\\n# Unqualified original-code change.\\n'
        target.unlink()  # Runtime storage and archive inodes stay immutable.
        target.write_bytes(payload)
        manifest['members'][name] = {'sha256': digest(payload), 'bytes': len(payload)}
        manifest['source']['code'][name] = digest(payload)
    manifest['source_fingerprint'] = json_digest(manifest['source'])
    generation = json_digest(manifest)
    (staging / 'manifest.json').write_bytes(canonical_bytes(manifest))
    target = provider.publisher.store / 'generations' / generation
    staging.replace(target)
    wrong = copy.deepcopy(receipt)
    wrong['generation_id'] = generation
    wrong['source_fingerprint'] = manifest['source_fingerprint']
    reseal_receipt(wrong)
    expected_message = ('generation source inventory/presence changed' if kind == 'source'
                        else 'source code/environment differs from this imported implementation')
    rejected('generation_' + kind + '_mismatch', lambda wrong=wrong: provider.from_receipt(pack, wrong),
             expected_message)

# A same-generation, checksum-valid receipt must still reject altered public
# candidates after it reaches the full independent pack recomputation.
wrong_pack = copy.deepcopy(pack)
wrong_pack['slots']['anatomical_connection']['candidates'].reverse()
assert wrong_pack != pack
wrong = copy.deepcopy(receipt)
wrong['pack_sha256'] = json_digest(wrong_pack)
wrong['bindings'] = runtime.pack_bindings(wrong_pack)
reseal_receipt(wrong)
rejected('full_candidate_pack_recomputation', lambda: provider.from_receipt(wrong_pack, wrong),
         'full candidate pack differs from pinned generation recomputation')
assert output.read_bytes() == official
assert receipt_path.read_bytes() == receipt_raw
report_path.write_text(json.dumps({'pack_id': pack['pack_id'], 'sha256': digest(raw),
    'generation_id': snapshot.generation_id, 'cache_status': snapshot.cache_status,
    'frozen_inputs': baseline['frozen_inputs'], 'rejections': rejections}))
'''

class HorrorMainBoundaryHistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proof, cls.parent = fixtures._v31_transition(ROOT)
        original = tempfile.TemporaryDirectory(prefix="v31-original-source-")
        cls.addClassCleanup(original.cleanup)
        cls.original_root = Path(original.name).resolve() / "tree"
        cls.original_validator = fixtures.archived_v31_validator(cls.original_root)
        cls.baseline = json.loads((ILL / 'assets/photo_regression_baseline_v31.json').read_bytes())
        cls.raw = (ILL / 'assets/photo_regression_baseline_v31_pack.json').read_bytes()
        cls.pack = json.loads(cls.raw)[0]

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='horror-v31-boundary-')
        self.addCleanup(temporary.cleanup)
        self.repo = Path(temporary.name)
        self.assets = self.repo / ILL.relative_to(ROOT) / 'assets'
        paths = set(self.proof['source_files_after']) | set(self.proof['active_shards_after'])
        paths.update(row['source_path'] for row in self.parent['members'])
        paths.update([str(fixtures.V31_HORROR_PROOF), str(fixtures.V30_PARENT_SOURCE), str(fixtures.V30_WATER_PROOF)])
        paths.update(str(p.relative_to(self.original_root)) for p in
                     (self.original_root / ILL.relative_to(ROOT) / 'assets').glob('photo_regression_baseline_v*.json'))
        paths.add(str((ILL / 'assets/universal_scene_baseline_v2.json').relative_to(ROOT)))
        for name in paths:
            path = self.repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.symlink_to(self.original_root / name)

    def validate(self, pack=None, raw=None):
        try:
            self.original_validator._validate_v31_horror_main_successor(
                self.assets, self.repo, self.baseline,
                self.pack if pack is None else pack, self.raw if raw is None else raw)
        except self.original_validator.ValidationFailure as exc:
            raise validator.ValidationFailure(str(exc)) from exc

    @contextlib.contextmanager
    def changed(self, name, raw, mode=None):
        path = self.repo / name
        original = path.readlink()
        path.unlink()
        if raw is not None:
            path.write_bytes(raw)
            if mode is not None:
                path.chmod(mode)
        try:
            yield
        finally:
            path.unlink(missing_ok=True)
            path.symlink_to(original)

    def test_current_public_cli_receipt_and_exact_reviewed_delta(self):
        result = validator.validate_photo_regression_baseline(ILL / 'assets', baseline_version=31)
        self.assertEqual(result['schema'], 'photo_regression_baseline/v31')
        self.assertEqual(result['sha256'], self.proof['current_pack_sha256'])
        self.assertEqual(64, validator._public_photo_candidate_count(self.pack))
        self.assertEqual(41, len(self.proof['reviewed_pack_delta']))
        previous = json.loads((ILL / 'assets/photo_regression_baseline_v30_pack.json').read_bytes())[0]
        for key in self.proof['preserved_contract_keys']:
            with self.subTest(key=key):
                self.assertEqual(previous[key], self.pack[key])

    def test_current_sources_and_byte_exact_v30_parent_pass(self):
        self.validate()
        self.assertEqual(1307, self.parent['member_count'])
        self.assertEqual(155, self.proof['horror_candidates'])
        self.assertEqual(155, self.proof['horror_profiles'])

    def test_original_v31_rejects_v32_and_corrected_live_source(self):
        with self.assertRaises(self.original_validator.ValidationFailure):
            self.original_validator.validate_photo_regression_baseline(
                self.original_root / ILL.relative_to(ROOT) / 'assets', baseline_version=32)
        name = 'skills/photo-prompt-image-generator/assets/photo_prompt_religion_iconography_extension.json'
        self.assertNotEqual((self.original_root / name).read_bytes(), (ROOT / name).read_bytes())
        with self.changed(name, (ROOT / name).read_bytes()):
            with self.assertRaises(validator.ValidationFailure):
                self.validate()

    def test_original_v31_cli_sidecar_is_independently_audited_with_negative_boundaries(self):
        temporary = tempfile.TemporaryDirectory(prefix='v31-original-receipt-')
        self.addCleanup(temporary.cleanup)
        work = Path(temporary.name).resolve()
        store = work / 'runtime-store'
        guard = work / 'offline-worker'
        guard.mkdir()
        (guard / 'sitecustomize.py').write_text(OFFLINE_WORKER_GUARD)
        photo_scripts = self.original_root / 'skills/photo-prompt-image-generator/scripts'
        environment = {
            **os.environ,
            'PHOTO_RUNTIME_STORE': str(store),
            'PYTHONPATH': os.pathsep.join((str(guard), str(photo_scripts))),
            'PYTHONDONTWRITEBYTECODE': '1',
            'PYTHONNOUSERSITE': '1',
            'GEMINI_API_KEY': '',
            'GOOGLE_API_KEY': '',
            'OPENAI_API_KEY': '',
        }
        venv = self.original_root / '.venv'
        interpreter_environment = Path(sys.executable).parent.parent
        if not venv.exists():
            venv.symlink_to(interpreter_environment, target_is_directory=True)
        self.assertEqual(interpreter_environment.resolve(), venv.resolve())
        self.assertTrue((venv / 'bin/python').is_file())
        pointer = work / 'published-original.json'
        output = work / 'original-v31-pack.json'
        report = work / 'original-v31-audit.json'

        def worker(command, timeout):
            completed = subprocess.run(command, cwd=self.original_root, env=environment,
                                       capture_output=True, text=True, check=False, timeout=timeout)
            self.assertEqual(0, completed.returncode, completed.stderr or completed.stdout)

        # Publish before generation, without extending the original CLI budget.
        worker([str(venv / 'bin/python'), '-c', PUBLISH_ORIGINAL_V31, str(pointer)], 300)
        original_baseline = self.original_root / ILL.relative_to(ROOT) / 'assets/photo_regression_baseline_v31.json'
        original_baseline_raw = original_baseline.read_bytes()
        self.assertEqual((ILL / 'assets/photo_regression_baseline_v31.json').read_bytes(), original_baseline_raw)
        baseline = json.loads(original_baseline_raw)
        command = list(baseline['command'])
        self.assertEqual(1, command.count('--output-file'))
        output_index = command.index('--output-file') + 1
        command[output_index] = str(output)
        self.assertEqual([output_index], [index for index, (before, after) in
                         enumerate(zip(baseline['command'], command)) if before != after])
        for name, expected in baseline['frozen_inputs'].items():
            with self.subTest(input=name):
                self.assertEqual(expected, hashlib.sha256((self.original_root / name).read_bytes()).hexdigest())
        worker(command, 60)
        self.assertEqual(self.raw, output.read_bytes())
        self.assertEqual(self.proof['current_pack_sha256'], hashlib.sha256(output.read_bytes()).hexdigest())
        sidecar = Path(str(output) + '.runtime-receipt.json')
        self.assertTrue(sidecar.is_file())
        worker([str(venv / 'bin/python'), '-c', AUDIT_ORIGINAL_V31,
                str(output), str(pointer), str(report)], 300)
        audit = json.loads(report.read_bytes())
        self.assertEqual(self.pack['pack_id'], audit['pack_id'])
        self.assertEqual(self.proof['current_pack_sha256'], audit['sha256'])
        self.assertEqual(baseline['frozen_inputs'], audit['frozen_inputs'])
        self.assertEqual('independent_audit', audit['cache_status'])
        self.assertEqual(json.loads(pointer.read_bytes())['generation_id'], audit['generation_id'])
        self.assertEqual({
            'missing_sidecar', 'missing_receipt_without_index', 'empty_receipt',
            'receipt_checksum', 'receipt_pack_sha256', 'receipt_source_fingerprint',
            'receipt_algorithm_sha256', 'receipt_slot_cache_key', 'receipt_generation_id',
            'receipt_bindings', 'empty_store', 'wrong_store', 'generation_source_mismatch',
            'generation_code_mismatch', 'full_candidate_pack_recomputation',
        }, {row['case'] for row in audit['rejections']})
        self.assertEqual(original_baseline_raw, original_baseline.read_bytes())

    def test_unreviewed_candidate_order_meaning_core_controls_or_budget_fail(self):
        for kind in ('meaning', 'order', 'core', 'controls', 'budget', 'negative'):
            pack = copy.deepcopy(self.pack)
            rows = pack['slots']['anatomical_connection']['candidates']
            if kind == 'meaning': rows[0]['concept_terms'][0] += ' changed'
            if kind == 'order': rows.reverse()
            if kind == 'core': pack['authorial_core']['subject'] += ' changed'
            if kind == 'controls': pack['creative_controls']['extra'] = True
            if kind == 'budget': pack['authorial_composition']['prompt_budget']['absolute_maximum_words'] += 1
            if kind == 'negative': pack['negative_en'] += ', changed'
            pack['pack_id'] = validator._canonical_photo_pack_id(pack)
            raw = (json.dumps([pack], ensure_ascii=False, indent=2) + '\n').encode()
            with self.subTest(kind=kind), self.assertRaises(validator.ValidationFailure):
                self.validate(pack, raw)

    def test_horror_water_runtime_registration_and_shards_are_bound(self):
        names = ['skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_horror.json',
                 'skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_water_relations.json',
                 'skills/photo-prompt-image-generator/assets/photo_prompt_source_manifest.json',
                 'skills/photo-prompt-image-generator/scripts/photo_runtime_sources.py',
                 next(iter(self.proof['active_shards_after']))]
        for name in names:
            with self.subTest(path=name), self.changed(name, (self.original_root / name).read_bytes() + b'\n'):
                with self.assertRaises(validator.ValidationFailure):
                    self.validate()

    def test_undeclared_source_cannot_enter_current_inventory(self):
        (self.repo / 'skills/photo-prompt-image-generator/assets/photo_prompt_unrelated_extension.json').write_text('{}')
        with self.assertRaises(validator.ValidationFailure):
            self.validate()

    def test_missing_or_rehashed_proof_and_parent_fail(self):
        for name in (str(fixtures.V31_HORROR_PROOF), str(fixtures.V30_PARENT_SOURCE)):
            for raw in (None, (self.original_root / name).read_bytes() + b'\n'):
                with self.subTest(path=name, missing=raw is None), self.changed(name, raw):
                    with self.assertRaises((validator.ValidationFailure, OSError)):
                        self.validate()

    def test_original_v30_source_bytes_and_mode_cannot_drift(self):
        row = next(row for row in self.parent['members'] if row['path'] == 'tests/photo_prompt_fixtures.py')
        name = row['source_path']; raw = (self.original_root / name).read_bytes()
        for payload, mode in ((raw + b'\n', 0o644), (raw, 0o600)):
            with self.subTest(mode=mode), self.changed(name, payload, mode):
                with self.assertRaises(validator.ValidationFailure):
                    self.validate()

if __name__ == '__main__':
    unittest.main()
