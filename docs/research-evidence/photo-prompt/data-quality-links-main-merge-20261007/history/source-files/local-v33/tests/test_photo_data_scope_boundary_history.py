"""V33 scope restrictions preserve exact V32 and fail closed on history drift."""
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
from unittest import mock

from tests import photo_prompt_fixtures as fixtures

ROOT = Path(__file__).resolve().parents[1]
ILLUSTRATION = Path('skills/subculture-illustration-image-generator')
PHOTO = Path('skills/photo-prompt-image-generator/assets')
sys.path.insert(0, str(ROOT / ILLUSTRATION / 'scripts'))
import validate_illustration_assets as validator


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


def target(value, pointer):
    parts = [part.replace('~1', '/').replace('~0', '~') for part in pointer.split('/')[1:]]
    for part in parts[:-1]:
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value, int(parts[-1]) if isinstance(value, list) else parts[-1]


@contextlib.contextmanager
def offline():
    with contextlib.ExitStack() as stack:
        calls = [stack.enter_context(mock.patch(name, side_effect=RuntimeError(name))) for name in (
            'subprocess.Popen', 'os.system', 'os.popen', 'socket.create_connection',
            'socket.socket.connect', 'socket.socket.connect_ex', 'urllib.request.urlopen')]
        try:
            yield
        finally:
            for call in calls:
                call.assert_not_called()


class DataScopeBoundaryHistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proof, cls.parent = fixtures._v33_transition(ROOT)
        cls.records = {row['path']: row for row in cls.parent['members']}
        cls.assets = ROOT / ILLUSTRATION / 'assets'
        cls.baseline = json.loads((cls.assets / 'photo_regression_baseline_v33.json').read_bytes())
        cls.raw = (cls.assets / 'photo_regression_baseline_v33_pack.json').read_bytes()
        cls.pack = json.loads(cls.raw)[0]
        cls.previous = json.loads((cls.assets / 'photo_regression_baseline_v32_pack.json').read_bytes())

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='.scope-v33-', dir=ROOT)
        self.addCleanup(temporary.cleanup)
        self.repo = Path(temporary.name).resolve()
        paths = {row['source_path'] for row in self.parent['members']}
        paths.update(self.proof['source_files_after'])
        paths.update(self.proof['active_shards_after'])
        paths.update(self.proof['retained_shards_before'])
        paths.update(self.proof['evidence_files'])
        paths.update(self.proof['frozen_inputs'])
        paths.update((fixtures.V33_SCOPE_PROOF.as_posix(), fixtures.V32_PARENT_SOURCE.as_posix(),
                      (ILLUSTRATION / 'assets/universal_scene_baseline_v2.json').as_posix()))
        paths.update(path.relative_to(ROOT).as_posix() for path in self.assets.glob('photo_regression_baseline_v*.json'))
        for name in sorted(paths):
            path = self.repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            os.link(ROOT / name, path)

    @contextlib.contextmanager
    def changed(self, name, raw, mode=None):
        path = self.repo / name
        before, old_mode = path.read_bytes(), path.stat().st_mode & 0o7777
        path.unlink()
        if raw is not None:
            path.write_bytes(raw)
            path.chmod(old_mode if mode is None else mode)
        try:
            yield path
        finally:
            if path.is_symlink() or path.exists():
                path.unlink()
            path.write_bytes(before)
            path.chmod(old_mode)

    def validate(self, *, pack=None, raw=None, baseline=None, receipt=None):
        validator._validate_v33_data_scope_successor(
            self.repo / ILLUSTRATION / 'assets', self.repo, baseline or self.baseline,
            pack or self.pack, raw or self.raw, receipt)

    def test_current_default_cli_and_real_receipt_qualify_v33(self):
        import photo_runtime_sources as runtime
        with tempfile.TemporaryDirectory(prefix='photo-v33-store-') as temporary, mock.patch.dict(
                os.environ, PHOTO_RUNTIME_STORE=temporary, GEMINI_API_KEY='', GOOGLE_API_KEY=''):
            runtime.SnapshotPublisher().publish()
            result = validator.validate_photo_regression_baseline(self.assets)
        self.assertEqual('photo_regression_baseline/v33', result['schema'])
        self.assertEqual(self.proof['current_pack_sha256'], result['sha256'])
        self.assertEqual(self.proof['current_pack_id'], result['pack_id'])

    def test_requested_v32_cli_uses_original_validator_and_qualified_hash(self):
        result = validator.validate_photo_regression_baseline(self.assets, baseline_version=32)
        self.assertEqual('photo_regression_baseline/v32', result['schema'])
        self.assertEqual(self.proof['previous_pack_sha256'], result['sha256'])
        self.assertEqual(self.proof['previous_pack_id'], result['pack_id'])

    def test_five_pack_leaves_preserve_candidates_order_and_all_frozen_contracts(self):
        expected = copy.deepcopy(self.previous)
        self.assertEqual(5, len(self.proof['reviewed_pack_delta']))
        for row in self.proof['reviewed_pack_delta']:
            parent, key = target(expected, row['pointer'])
            self.assertEqual(row['before'], parent[key])
            parent[key] = row['after']
        self.assertEqual(expected, [self.pack])
        self.assertEqual((34, 33), (self.previous[0]['slots']['motion']['candidate_count'],
                                   self.pack['slots']['motion']['candidate_count']))
        self.assertEqual(64, validator._public_photo_candidate_count(self.pack))
        previous = json.loads((self.assets / 'photo_regression_baseline_v32.json').read_bytes())
        for field in ('frozen_inputs', 'preserved_contract_sha256', 'negative_en', 'private_fields_absent'):
            self.assertEqual(previous[field], self.baseline[field])

    def test_six_added_source_leaves_are_the_entire_authored_delta(self):
        self.assertEqual([2, 2, 2], sorted(map(len, self.proof['source_leaf_delta'].values())))
        for name, changes in self.proof['source_leaf_delta'].items():
            source = json.loads(fixtures._v24_verified_payload(self.repo, self.records[name]))
            for row in changes:
                self.assertEqual('add', row['operation'])
                parent, key = target(source, row['pointer'])
                self.assertNotIn(key, parent)
                parent[key] = row['after']
            self.assertEqual(source, json.loads((self.repo / name).read_bytes()))

    def test_unreviewed_pack_meaning_order_core_budget_negative_or_count_fails(self):
        for kind in ('meaning', 'order', 'core', 'budget', 'negative', 'count'):
            pack = copy.deepcopy(self.pack)
            rows = next(slot['candidates'] for slot in pack['slots'].values() if len(slot['candidates']) > 1)
            if kind == 'meaning': rows[0]['concept_terms'][0] += ' changed'
            elif kind == 'order': rows.reverse()
            elif kind == 'core': pack['authorial_core']['subject'] += ' changed'
            elif kind == 'budget': pack['authorial_composition']['prompt_budget']['absolute_maximum_words'] += 1
            elif kind == 'negative': pack['negative_en'] += ', changed'
            else: pack['slots']['motion']['candidate_count'] += 1
            pack['pack_id'] = validator._canonical_photo_pack_id(pack)
            raw = encoded([pack])
            baseline = dict(self.baseline, sha256=hashlib.sha256(raw).hexdigest(), pack_id=pack['pack_id'])
            with self.subTest(kind=kind), self.changed(ILLUSTRATION / 'assets/photo_regression_baseline_v33_pack.json', raw):
                with self.assertRaises(validator.ValidationFailure):
                    self.validate(pack=pack, raw=raw, baseline=baseline)

    def test_live_drift_original_rollbacks_and_mode_drift_never_bypass_v33(self):
        for name in sorted(fixtures.V33_SCOPE_SOURCE_PATHS):
            row = self.records[name]
            current = (ROOT / name).read_bytes()
            original = fixtures._v24_verified_payload(self.repo, row)
            for kind, raw, mode in (('drift', current + b'\n', None), ('v32-rollback', original, None),
                                    ('mode', current, 0o600)):
                with self.subTest(path=name, kind=kind), self.changed(name, raw, mode), offline():
                    with self.assertRaises(AssertionError):
                        fixtures._v24_verified_payload(self.repo, dict(row, source_path=name))
                    with self.assertRaises(AssertionError):
                        fixtures._v33_original_live_path(self.repo, name)

    def test_exact_v31_through_v27_identities_recover_without_external_access(self):
        histories = [fixtures._v32_transition(self.repo)[1], fixtures._v31_transition(self.repo)[1],
                     fixtures._v30_transition(self.repo)[1], fixtures._v29_transition(self.repo)[1],
                     fixtures._v27_parent_manifest(self.repo)]
        with offline():
            for manifest in histories:
                records = {row['path']: row for row in manifest['members']}
                for name in sorted(fixtures.V33_SCOPE_SOURCE_PATHS):
                    row = records[name]
                    with self.subTest(version=manifest['schema'], path=name):
                        raw = fixtures._v24_verified_payload(self.repo, dict(row, source_path=name))
                        self.assertEqual(row['sha256'], hashlib.sha256(raw).hexdigest())
                        self.assertEqual(row['git_blob'], hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest())

    def test_missing_or_rehashed_proof_and_parent_never_fall_back_to_live(self):
        name = sorted(fixtures.V33_SCOPE_SOURCE_PATHS)[0]
        row = self.records[name]
        for evidence in (fixtures.V33_SCOPE_PROOF, fixtures.V32_PARENT_SOURCE):
            for raw in (None, (ROOT / evidence).read_bytes() + b'\n'):
                with self.subTest(path=str(evidence), missing=raw is None), self.changed(evidence, raw), offline():
                    with self.assertRaises(AssertionError):
                        fixtures._v24_verified_payload(self.repo, dict(row, source_path=name))

    def test_archived_payload_missing_bytes_mode_symlink_or_identity_drift_fails(self):
        row = self.records['tests/test_photo_robe_source_boundary_history.py']
        name = row['source_path']
        raw = (ROOT / name).read_bytes()
        for kind in ('missing', 'bytes', 'mode', 'symlink'):
            payload = None if kind in ('missing', 'symlink') else raw + (b'\n' if kind == 'bytes' else b'')
            with self.subTest(kind=kind), self.changed(name, payload, 0o600 if kind == 'mode' else None) as path:
                if kind == 'symlink': path.symlink_to(ROOT / name)
                with offline(), self.assertRaises(AssertionError):
                    fixtures._v24_verified_payload(self.repo, row)
        for key, value in (('bytes', len(raw) + 1), ('sha256', '0' * 64), ('git_blob', '0' * 40)):
            with self.subTest(field=key), offline(), self.assertRaises(AssertionError):
                fixtures._v24_verified_payload(self.repo, dict(row, **{key: value}))

    def test_parent_source_paths_cannot_escape_or_alias_a_symlink(self):
        row = self.parent['members'][0]
        for name in ('/tmp/escaped-v33', '../escape', 'nested/../payload', './payload', 'nested//payload',
                     'nested\\payload', 'C:/payload', 'nested/\x00payload'):
            with self.subTest(path=name), self.assertRaises(AssertionError):
                fixtures._v24_verified_payload(self.repo, dict(row, source_path=name))
        alias = self.repo / 'linked-source'
        alias.symlink_to(ROOT, target_is_directory=True)
        with self.assertRaises(AssertionError):
            fixtures._v33_parent_manifest(alias)

    def test_rehashed_parent_still_rejects_wrong_inventory_identity_and_backing(self):
        for kind in ('commit', 'tree', 'duplicate', 'path', 'backing', 'mode', 'blob', 'count', 'total'):
            parent = copy.deepcopy(self.parent)
            row = parent['members'][0]
            if kind == 'commit': parent['source_pin'] = '0' * 40
            elif kind == 'tree': parent['source_tree'] = '0' * 40
            elif kind == 'duplicate': parent['members'][1] = copy.deepcopy(row)
            elif kind == 'path': row['path'] = '../escape-v33'
            elif kind == 'backing': row['source_path'] = 'unregistered/backing'
            elif kind == 'mode': row['mode'] = '120000'
            elif kind == 'blob': row['git_blob'] = 'z' * 40
            elif kind == 'count': parent['member_count'] -= 1
            else: parent['total_member_bytes'] += 1
            raw = encoded(parent)
            with self.subTest(kind=kind), self.changed(fixtures.V32_PARENT_SOURCE, raw), \
                    mock.patch.object(fixtures, 'V32_PARENT_SOURCE_SHA256', hashlib.sha256(raw).hexdigest()):
                with offline(), self.assertRaises(AssertionError):
                    fixtures._v33_parent_manifest(self.repo)

    def test_parent_destination_and_late_copy_failures_are_atomic(self):
        occupied = self.repo / 'occupied'
        occupied.mkdir(); (occupied / 'keep').write_text('keep')
        alias = self.repo / 'alias'
        alias.symlink_to(occupied, target_is_directory=True)
        with offline():
            for destination in (occupied, alias, alias / 'child'):
                with self.subTest(destination=destination), self.assertRaises(AssertionError):
                    fixtures.materialize_v32_parent_source(destination, source_root=self.repo)
        self.assertEqual('keep', (occupied / 'keep').read_text())
        rows = sorted(self.parent['members'], key=lambda row: row['bytes'])[:2]
        original = fixtures._v24_verified_payload
        count = 0
        def fail_during_copy(source, row):
            nonlocal count
            count += 1
            if count == len(rows) + 2:
                raise AssertionError('Source changed after preflight')
            return original(source, row)
        destination = self.repo / 'destination'
        with offline(), mock.patch.object(fixtures, '_v33_parent_manifest', return_value=dict(self.parent, members=rows)), \
                mock.patch.object(fixtures, '_v24_verified_payload', side_effect=fail_during_copy):
            with self.assertRaisesRegex(AssertionError, 'after preflight'):
                fixtures.materialize_v32_parent_source(destination, source_root=self.repo)
        self.assertFalse(destination.exists())
        self.assertFalse(list(self.repo.glob('.sealed-v32-*')))

    def test_history_python_explicit_override_requires_exact_original_environment(self):
        required = fixtures._v32_transition(self.repo)[0]['runtime_environment']
        python = '/tmp/photo-history-test-python'
        with mock.patch.dict(os.environ, PHOTO_HISTORY_PYTHON=python), \
                mock.patch.object(Path, 'is_file', return_value=True), \
                mock.patch.object(fixtures.subprocess, 'run', return_value=subprocess.CompletedProcess(
                    [], 0, stdout=json.dumps(required))) as probe:
            self.assertEqual(Path(python), fixtures.v32_history_python(source_root=self.repo))
        self.assertEqual(python, probe.call_args.args[0][0])

    def test_history_python_mismatched_local_runtimes_fail_clearly(self):
        wrong = dict(implementation='cpython', python=[3, 14, 3], unicode='16.0.0')
        with mock.patch.object(Path, 'is_file', return_value=True), \
                mock.patch.object(fixtures.subprocess, 'run', return_value=subprocess.CompletedProcess(
                    [], 0, stdout=json.dumps(wrong))):
            with self.assertRaisesRegex(AssertionError, 'requires its exact Python/Unicode environment'):
                fixtures.v32_history_python(source_root=self.repo)

    def test_history_python_wrong_explicit_override_cannot_silently_fall_back(self):
        wrong = dict(implementation='cpython', python=[3, 14, 3], unicode='16.0.0')
        with mock.patch.dict(os.environ, PHOTO_HISTORY_PYTHON='/tmp/wrong-history-python'), \
                mock.patch.object(Path, 'is_file', return_value=True), \
                mock.patch.object(fixtures.subprocess, 'run', return_value=subprocess.CompletedProcess(
                    [], 0, stdout=json.dumps(wrong))) as probe:
            with self.assertRaisesRegex(AssertionError, 'requires its exact Python/Unicode environment'):
                fixtures.v32_history_python(source_root=self.repo)
        probe.assert_called_once()

    def test_v33_supplied_receipt_source_generation_drift_fails(self):
        path = fixtures.V33_SCOPE_PROOF.parent / 'CURRENT-BOUNDARY-RECEIPT.json'
        receipt = json.loads((ROOT / path).read_bytes())
        for field in ('generation_id', 'source_fingerprint'):
            wrong = dict(receipt, **{field: '0' * 64})
            with self.subTest(field=field), self.assertRaisesRegex(validator.ValidationFailure, 'receipt source generation drift'):
                self.validate(receipt=wrong)


if __name__ == '__main__':
    unittest.main()
