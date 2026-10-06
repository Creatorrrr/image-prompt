"""Robe-only V32 seals current DATA while preserving exact offline V31 history.

Sandboxes hardlink the existing replay closure; mutations always unlink first.
Successful historical CLI replays live in the V31/V30/V29 history modules, so these
tests never make another 2.59 GB copy merely to exercise a negative boundary.
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
from types import SimpleNamespace
import unittest
from unittest import mock

from tests import photo_prompt_fixtures as fixtures

ROOT = Path(__file__).resolve().parents[1]
ILLUSTRATION = Path('skills/subculture-illustration-image-generator')
PHOTO = Path('skills/photo-prompt-image-generator/assets')
sys.path.insert(0, str(ROOT / ILLUSTRATION / 'scripts'))
import validate_illustration_assets as validator

# Current DATA is V33; these unchanged V32 assertions use exact original bytes.
if (ROOT / ILLUSTRATION / 'assets/photo_regression_baseline_v33.json').is_file():
    import atexit
    _live_root = ROOT
    _v32_temporary = tempfile.TemporaryDirectory(prefix='.palette-v32-robe-tests-', dir=ROOT)
    _v32_root = Path(_v32_temporary.name) / 'tree'
    _v32_support = fixtures._v33_palette_support(ROOT)
    _v32_support.materialize_v32_parent_source(_v32_root, source_root=ROOT, link_verified=True)
    validator = _v32_support.pinned_v32_validator(_v32_root, source_root=ROOT)
    ROOT = _v32_root
    atexit.register(_v32_temporary.cleanup)

ROBE_DATA = {
    (PHOTO / 'photo_prompt_religion_iconography_extension.json').as_posix(),
    (PHOTO / 'photo_prompt_visual_obligations_religion_iconography.json').as_posix(),
}
INDEX_PATHS = {
    (PHOTO / 'photo_prompt_semantic_index.json').as_posix(),
    (PHOTO / 'photo_prompt_visual_profile_index.json').as_posix(),
}


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


def pointer_target(value, pointer):
    parts = [part.replace('~1', '/').replace('~0', '~')
             for part in pointer.split('/')[1:]]
    for part in parts[:-1]:
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value, int(parts[-1]) if isinstance(value, list) else parts[-1]


@contextlib.contextmanager
def offline():
    """A rejected fallback must not pass just because a mocked call raised."""
    with contextlib.ExitStack() as stack:
        calls = [stack.enter_context(mock.patch(name, side_effect=RuntimeError(
            'Historical fixture attempted external access: ' + name))) for name in (
                'subprocess.Popen', 'os.system', 'os.popen',
                'socket.create_connection', 'socket.socket.connect',
                'socket.socket.connect_ex', 'urllib.request.urlopen')]
        try:
            yield
        finally:
            for call in calls:
                call.assert_not_called()


class _RobeSandbox(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proof, cls.parent = fixtures._v32_transition(ROOT)
        cls.records = {row['path']: row for row in cls.parent['members']}
        assets = ROOT / ILLUSTRATION / 'assets'
        cls.baseline = json.loads((assets / 'photo_regression_baseline_v32.json').read_bytes())
        cls.raw = (assets / 'photo_regression_baseline_v32_pack.json').read_bytes()
        cls.pack = json.loads(cls.raw)[0]
        cls.previous = json.loads((assets / 'photo_regression_baseline_v31_pack.json').read_bytes())

    def setUp(self):
        # Hardlink sandboxes must share the checkout filesystem even when /tmp
        # is a separate mount. Mutations below always unlink shared files first.
        temporary = tempfile.TemporaryDirectory(prefix='.robe-v32-boundary-', dir=ROOT)
        self.addCleanup(temporary.cleanup)
        self.repo = Path(temporary.name).resolve()
        self.assets = self.repo / ILLUSTRATION / 'assets'
        paths = set(self.proof['source_files_after']) | set(self.proof['active_shards_after'])
        paths.update(self.proof['retained_shards_before'])
        paths.update(self.proof['evidence_files'])
        paths.update(self.proof['frozen_inputs'])
        paths.update(row['source_path'] for row in self.parent['members'])
        paths.update((fixtures.V32_ROBE_PROOF.as_posix(), fixtures.V31_PARENT_SOURCE.as_posix(),
                      self.proof['maintenance_successor']['path'],
                      (ILLUSTRATION / 'assets/universal_scene_baseline_v2.json').as_posix()))
        paths.update(path.relative_to(ROOT).as_posix() for path in
                     (ROOT / ILLUSTRATION / 'assets').glob('photo_regression_baseline_v*.json'))
        for name in sorted(paths):
            target = self.repo / name
            target.parent.mkdir(parents=True, exist_ok=True)
            os.link(ROOT / name, target)

    @contextlib.contextmanager
    def changed(self, name, raw, mode=None):
        path = self.repo / name
        original_mode = path.stat().st_mode & 0o7777
        path.unlink()  # Never write or chmod an inode shared with the repository.
        if raw is not None:
            path.write_bytes(raw)
            path.chmod(original_mode if mode is None else mode)
        try:
            yield path
        finally:
            path.unlink(missing_ok=True)
            os.link(ROOT / name, path)

    def validate(self, pack=None, raw=None, baseline=None, receipt=None):
        validator._validate_v32_robe_source_successor(
            self.assets, self.repo, self.baseline if baseline is None else baseline,
            self.pack if pack is None else pack, self.raw if raw is None else raw,
            receipt=receipt)


class RobeSourceBoundaryHistoryTests(_RobeSandbox):
    def test_current_default_real_cli_and_receipt_qualify_v32(self):
        if '_v32_support' in globals():
            result = _v32_support.replay_v32(ROOT, source_root=_live_root)
        else:
            result = validator.validate_photo_regression_baseline(ROOT / ILLUSTRATION / 'assets')
        self.assertEqual('photo_regression_baseline/v32', result['schema'])
        self.assertEqual(self.proof['current_pack_sha256'], result['sha256'])

    def test_current_v32_cli_requires_its_generated_sidecar(self):
        def exact_pack_without_sidecar(command, **kwargs):
            destination = Path(command[command.index('--output-file') + 1])
            destination.write_bytes(self.raw)
            self.assertFalse(Path(str(destination) + '.runtime-receipt.json').exists())
            return subprocess.CompletedProcess(command, 0, stdout='', stderr='')

        # Exercise the real current dispatcher through its mandatory sidecar
        # collection step, without repeating the already qualified generation.
        with mock.patch.object(validator.subprocess, 'run', side_effect=exact_pack_without_sidecar) as command:
            with self.assertRaisesRegex(validator.ValidationFailure, 'omitted its runtime receipt'):
                validator.validate_photo_regression_baseline(ROOT / ILLUSTRATION / 'assets', baseline_version=32)
        command.assert_called_once()

    def test_current_supplied_receipt_rejects_generation_source_and_algorithm_drift(self):
        import photo_runtime_sources as runtime
        from core_slot_index_storage import json_digest

        evidence = fixtures.V32_ROBE_PROOF.parent
        receipt_raw = (ROOT / evidence / 'CURRENT-BOUNDARY-RECEIPT.json').read_bytes()
        receipt = json.loads(receipt_raw)
        generation = json.loads((ROOT / evidence / 'CURRENT-GENERATION.json').read_bytes())
        self.assertEqual(self.proof['receipt_sha256'], hashlib.sha256(receipt_raw).hexdigest())
        self.assertEqual(self.proof['generation_id'], json_digest(generation))
        for field in ('generation_id', 'source_fingerprint', 'algorithm_sha256'):
            self.assertEqual(self.proof[field], receipt[field])
            wrong = copy.deepcopy(receipt)
            wrong[field] = '0' * 64
            wrong['canonical_sha256'] = json_digest({key: value for key, value in wrong.items()
                                                    if key != 'canonical_sha256'})
            with self.subTest(field=field):
                if field != 'algorithm_sha256':
                    with self.assertRaisesRegex(validator.ValidationFailure, 'receipt source generation drift'):
                        self.validate(receipt=wrong)
                else:
                    # Keep the real supplied-receipt validation. Only loading the
                    # immutable generation is substituted, avoiding another store
                    # publication; the full current CLI audit is covered above.
                    snapshot = SimpleNamespace(manifest=generation)
                    with mock.patch.object(runtime.RuntimeSnapshotProvider, 'load_generation',
                                           return_value=snapshot) as load, \
                            mock.patch.object(runtime, 'verify_pack_bindings',
                                              wraps=runtime.verify_pack_bindings) as recompute:
                        with self.assertRaisesRegex(runtime.FreshnessError, 'receipt generation binding mismatch'):
                            self.validate(receipt=wrong)
                    load.assert_called_once_with(receipt['generation_id'], independent_audit=True)
                    recompute.assert_not_called()
        self.assertEqual(receipt_raw, (ROOT / evidence / 'CURRENT-BOUNDARY-RECEIPT.json').read_bytes())

    def test_exact_sources_parent_and_reviewed_pack_are_qualified(self):
        self.validate()
        self.assertEqual('6b0338ebe6ad3a9a5ee3c603fc742311ad921054', self.parent['source_pin'])
        self.assertEqual('d7b3e9100a66c8b0e770ab37d8eb50bbd67ddb3b', self.parent['source_tree'])
        self.assertEqual((1354, 2590824970),
                         (self.parent['member_count'], self.parent['total_member_bytes']))
        self.assertEqual((148, 99, 32, 32), tuple(len(self.proof[key]) for key in
                         ('source_files_after', 'source_inventory_after',
                          'active_shards_after', 'retained_shards_before')))
        self.assertEqual(64, validator._public_photo_candidate_count(self.pack))

    def test_four_binding_leaves_preserve_every_candidate_object_and_order(self):
        delta = self.proof['reviewed_pack_delta']
        self.assertEqual([
            '/0/core_retrieval/canonical_sha256', '/0/core_retrieval/slot_corpus_sha256',
            '/0/pack_id', '/0/provenance/tags_hash',
        ], [row['pointer'] for row in delta])
        expected = copy.deepcopy(self.previous)
        for row in delta:
            target, key = pointer_target(expected, row['pointer'])
            self.assertEqual(row['before'], target[key])
            self.assertNotEqual(row['before'], row['after'])
            target[key] = row['after']
        self.assertEqual(expected, json.loads(self.raw))
        old_baseline = json.loads((self.assets / 'photo_regression_baseline_v31.json').read_bytes())
        self.assertEqual(old_baseline['frozen_inputs'], self.baseline['frozen_inputs'])
        old_command, new_command = list(old_baseline['command']), list(self.baseline['command'])
        for command in (old_command, new_command):
            command[command.index('--output-file') + 1] = '<output>'
        self.assertEqual(old_command, new_command)

    def test_only_reviewed_robe_leaves_change_in_the_two_authored_files(self):
        self.assertEqual(ROBE_DATA, set(self.proof['source_leaf_delta']))
        self.assertEqual(ROBE_DATA | INDEX_PATHS, set(self.proof['preserved_source_paths']))
        self.assertEqual({
            (PHOTO / 'photo_prompt_religion_iconography_extension.json').as_posix(): 20,
            (PHOTO / 'photo_prompt_visual_obligations_religion_iconography.json').as_posix(): 25,
        }, {name: len(delta) for name, delta in self.proof['source_leaf_delta'].items()})
        for name, delta in self.proof['source_leaf_delta'].items():
            expected = json.loads((self.repo / self.records[name]['source_path']).read_bytes())
            for row in delta:
                target, key = pointer_target(expected, row['pointer'])
                self.assertEqual(row['before'], target[key])
                target[key] = row['after']
            with self.subTest(path=name):
                self.assertEqual(expected, json.loads((self.repo / name).read_bytes()))

    def test_universal_descriptor_changes_only_the_validator_hash(self):
        name = (ILLUSTRATION / 'assets/universal_scene_baseline_v2.json').as_posix()
        before = (self.repo / self.records[name]['source_path']).read_bytes()
        old_sha = self.proof['previous_validator_sha256'].encode('ascii')
        self.assertEqual(1, before.count(old_sha))
        current_sha = hashlib.sha256(Path(validator.__file__).read_bytes()).hexdigest().encode('ascii')
        self.assertEqual(before.replace(old_sha, current_sha, 1), (self.repo / name).read_bytes())

    def test_rehashed_unreviewed_meaning_order_core_controls_budget_and_negative_fail(self):
        for kind in ('meaning', 'order', 'core', 'controls', 'budget', 'negative', 'age_policy'):
            pack = copy.deepcopy(self.pack)
            rows = next(slot['candidates'] for slot in pack['slots'].values()
                        if len(slot['candidates']) > 1)
            if kind == 'meaning': rows[0]['concept_terms'][0] += ' changed'
            elif kind == 'order': rows.reverse()
            elif kind == 'core': pack['authorial_core']['subject'] += ' changed'
            elif kind == 'controls': pack['creative_controls']['unexpected'] = True
            elif kind == 'budget': pack['authorial_composition']['prompt_budget']['absolute_maximum_words'] += 1
            elif kind == 'negative': pack['negative_en'] += ', changed'
            else: pack['adult_appeal']['composition_requirements']['adult_subject_phrase_required'] = True
            pack['pack_id'] = validator._canonical_photo_pack_id(pack)
            raw = encoded([pack])
            baseline = dict(self.baseline, sha256=hashlib.sha256(raw).hexdigest(), pack_id=pack['pack_id'])
            with self.subTest(kind=kind), self.changed(
                    ILLUSTRATION / 'assets/photo_regression_baseline_v32_pack.json', raw):
                with self.assertRaises(validator.ValidationFailure):
                    self.validate(pack, raw, baseline)

    def test_robe_unrelated_data_registry_runtime_and_ranking_drift_fail(self):
        names = sorted(ROBE_DATA | INDEX_PATHS) + [
            (PHOTO / 'photo_prompt_everyday_scene_extension.json').as_posix(),
            (PHOTO / 'photo_prompt_visual_obligations_everyday_scene.json').as_posix(),
            (PHOTO / 'photo_prompt_water_relations_extension.json').as_posix(),
            (PHOTO / 'photo_prompt_horror_extension.json').as_posix(),
            (PHOTO / 'photo_prompt_visual_obligations_horror.json').as_posix(),
            (PHOTO / 'photo_prompt_source_manifest.json').as_posix(),
            'skills/photo-prompt-image-generator/scripts/photo_runtime_sources.py',
            'skills/photo-prompt-image-generator/scripts/prompt_generator.py',
            'tests/test_photo_visual_profile_shards.py',
            self.proof['maintenance_successor']['path'],
        ]
        for name in names:
            with self.subTest(path=name), self.changed(name, (ROOT / name).read_bytes() + b'\n'):
                with self.assertRaises(validator.ValidationFailure):
                    self.validate()

    def test_extra_authored_leaf_or_unregistered_source_file_fails(self):
        name = sorted(ROBE_DATA)[0]
        source = json.loads((ROOT / name).read_bytes())
        source['unreviewed_robe_scope'] = 'changed'
        with self.changed(name, encoded(source)), self.assertRaises(validator.ValidationFailure):
            self.validate()
        (self.repo / PHOTO / 'photo_prompt_unreviewed_extension.json').write_text('{}\n')
        with self.assertRaises(validator.ValidationFailure):
            self.validate()

    def test_active_and_retained_original_shards_cannot_drift(self):
        active = set(self.proof['active_shards_after'])
        retained_only = set(self.proof['retained_shards_before']) - active
        self.assertTrue(retained_only, 'The replaced robe vectors must preserve their original shard paths')
        for name in (sorted(active)[0], sorted(retained_only)[0]):
            with self.subTest(path=name), self.changed(name, (ROOT / name).read_bytes() + b'\n'):
                with self.assertRaises(validator.ValidationFailure):
                    self.validate()

    def test_missing_or_rehashed_proof_manifest_and_generation_evidence_fail(self):
        names = [fixtures.V32_ROBE_PROOF, fixtures.V31_PARENT_SOURCE]
        names.extend(Path(name) for name in self.proof['evidence_files'])
        for name in names:
            for raw in (None, (ROOT / name).read_bytes() + b'\n'):
                with self.subTest(path=str(name), missing=raw is None), self.changed(name, raw):
                    with self.assertRaises((validator.ValidationFailure, OSError)):
                        self.validate()

    def test_proof_parent_live_source_and_archive_symlinks_fail(self):
        names = [fixtures.V32_ROBE_PROOF, fixtures.V31_PARENT_SOURCE,
                 Path(sorted(ROBE_DATA)[0]), Path(self.parent['members'][0]['source_path'])]
        for name in names:
            with self.subTest(path=str(name)), self.changed(name, None) as path:
                path.symlink_to(ROOT / name)
                with self.assertRaises(validator.ValidationFailure):
                    self.validate()

    def test_original_parent_bytes_and_modes_remain_bound(self):
        name = self.parent['members'][0]['source_path']
        raw = (ROOT / name).read_bytes()
        for payload, mode in ((raw + b'\n', 0o644), (raw, 0o600)):
            with self.subTest(mode=mode), self.changed(name, payload, mode):
                with self.assertRaises(validator.ValidationFailure):
                    self.validate()


class RobeHistoricalFixtureTests(_RobeSandbox):
    def original_rollback_cases(self):
        c72_rows = {row['path']: row for row in fixtures._v31_transition(self.repo)[1]['members']}
        cases = []
        # Resolve original bytes before removing any marker or changing a live file.
        for version, records in (('6b', self.records), ('c72', c72_rows)):
            for name in sorted(ROBE_DATA | INDEX_PATHS):
                row = records[name]
                raw = fixtures._v24_verified_payload(self.repo, row)
                cases.append((version, name, dict(row, source_path=name), raw))
        return cases

    def assert_rollback_routes_rejected(self, cases):
        for version, name, row, raw in cases:
            with self.subTest(original=version, path=name), self.changed(name, raw), offline():
                # The current file now exactly matches the requested historical
                # identity; a missing successor proof must still reject it.
                self.assertEqual(row['sha256'], hashlib.sha256(raw).hexdigest())
                with self.assertRaises(AssertionError):
                    fixtures._v24_verified_payload(self.repo, row)
                for resolver in (fixtures.v30_source_path, fixtures.v29_source_path,
                                 fixtures.v28_source_path):
                    with self.subTest(resolver=resolver.__name__), self.assertRaises(AssertionError):
                        resolver(name, source_root=self.repo)

    def test_missing_v32_proof_rejects_exact_rollbacks_with_parent_or_baseline_marker(self):
        cases = self.original_rollback_cases()
        baseline = ILLUSTRATION / 'assets/photo_regression_baseline_v32.json'
        for remaining in ('parent', 'baseline'):
            absent = baseline if remaining == 'parent' else fixtures.V31_PARENT_SOURCE
            with self.subTest(remaining=remaining), self.changed(fixtures.V32_ROBE_PROOF, None), \
                    self.changed(absent, None):
                self.assert_rollback_routes_rejected(cases)

    def test_dangling_v32_proof_alone_rejects_exact_original_rollbacks(self):
        cases = self.original_rollback_cases()
        baseline = ILLUSTRATION / 'assets/photo_regression_baseline_v32.json'
        with self.changed(fixtures.V31_PARENT_SOURCE, None), self.changed(baseline, None), \
                self.changed(fixtures.V32_ROBE_PROOF, None) as proof:
            proof.symlink_to(self.repo / 'missing-v32-proof-target')
            self.assertFalse(proof.exists())
            self.assertTrue(proof.is_symlink())
            self.assert_rollback_routes_rejected(cases)

    def test_marker_free_original_sources_accept_exact_historical_identities(self):
        histories = [(31, self.parent, None, None),
                     (30, fixtures._v31_transition(self.repo)[1], '_v31_transition', fixtures.v30_source_path),
                     (29, fixtures._v30_transition(self.repo)[1], '_v30_transition', fixtures.v29_source_path),
                     (28, fixtures._v29_transition(self.repo)[1], '_v29_transition', fixtures.v28_source_path)]
        for version, history, transition, resolver in histories:
            root = self.repo / f'original-v{version}-without-successor'
            rows, payloads = [], {}
            records = {row['path']: row for row in history['members']}
            for name in sorted(ROBE_DATA | INDEX_PATHS):
                raw = fixtures._v24_verified_payload(self.repo, records[name])
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(raw)
                target.chmod(int(records[name]['mode'][-3:], 8))
                rows.append(dict(records[name], source_path=name))
                payloads[name] = raw
            self.assertFalse(fixtures._v32_recovery_context(root))
            # Only the four real, exact original payloads are needed to exercise
            # marker-free payload authentication and the retained-source returns.
            original_manifest = dict(history, members=rows)
            original_proof = {'source_files_after': {row['path']: row['sha256'] for row in rows}}
            with offline(), contextlib.ExitStack() as stack:
                if transition is not None:
                    stack.enter_context(mock.patch.object(fixtures, transition,
                                        return_value=(original_proof, original_manifest)))
                for row in rows:
                    with self.subTest(version=version, path=row['path']):
                        self.assertEqual(payloads[row['path']], fixtures._v24_verified_payload(root, row))
                        if resolver is not None:
                            self.assertEqual(root / row['path'], resolver(row['path'], source_root=root))

    def test_materialization_copies_original_bytes_modes_and_independent_inodes(self):
        # The complete 1,354-member inventory has its own authenticated positive.
        # Two sealed small members isolate the actual staging/copy contract.
        rows = sorted(self.parent['members'], key=lambda row: row['bytes'])[:2]
        manifest = dict(self.parent, members=rows)
        destination = self.repo / 'independent-copy'
        with offline(), mock.patch.object(fixtures, '_v32_transition', return_value=(self.proof, manifest)):
            self.assertEqual(manifest, fixtures.materialize_v31_parent_source(destination, source_root=self.repo))
        for row in rows:
            source = self.repo / row['source_path']
            target = destination / row['path']
            source_stat, target_stat = source.stat(), target.stat()
            with self.subTest(path=row['path']):
                self.assertEqual(source.read_bytes(), target.read_bytes())
                self.assertEqual(int(row['mode'][-3:], 8), target_stat.st_mode & 0o777)
                self.assertNotEqual((source_stat.st_dev, source_stat.st_ino),
                                    (target_stat.st_dev, target_stat.st_ino))
        self.assertFalse(list(self.repo.glob('.sealed-v31-*')))

    def test_late_chmod_failure_keeps_destination_atomic(self):
        rows = sorted(self.parent['members'], key=lambda row: row['bytes'])[:2]
        manifest = dict(self.parent, members=rows)
        original_chmod = Path.chmod
        for existing in (False, True):
            destination = self.repo / ('chmod-existing' if existing else 'chmod-absent')
            if existing:
                destination.mkdir()
            changed = []

            def fail_second_staged_chmod(path, mode, *args, **kwargs):
                if any(part.startswith('.sealed-v31-') for part in path.parts):
                    changed.append(path)
                    if len(changed) == 2:
                        raise PermissionError('Injected late staged chmod failure')
                return original_chmod(path, mode, *args, **kwargs)

            with self.subTest(existing=existing), offline(), \
                    mock.patch.object(fixtures, '_v32_transition', return_value=(self.proof, manifest)), \
                    mock.patch.object(Path, 'chmod', fail_second_staged_chmod):
                with self.assertRaisesRegex(PermissionError, 'late staged chmod failure'):
                    fixtures.materialize_v31_parent_source(destination, source_root=self.repo)
            self.assertEqual(2, len(changed))
            self.assertEqual(existing, destination.exists())
            self.assertEqual([], list(destination.iterdir()) if existing else [])
            self.assertFalse(list(self.repo.glob('.sealed-v31-*')))

    def test_sealed_live_sources_recover_exact_v31_through_v27_without_external_access(self):
        histories = [(31, self.parent), (30, fixtures._v31_transition(self.repo)[1]),
                     (29, fixtures._v30_transition(self.repo)[1]),
                     (28, fixtures._v29_transition(self.repo)[1]),
                     (27, fixtures._v27_parent_manifest(self.repo))]
        with offline():
            for version, manifest in histories:
                rows = {row['path']: row for row in manifest['members']}
                for name in sorted(ROBE_DATA | INDEX_PATHS):
                    row = rows[name]
                    with self.subTest(version=version, path=name):
                        raw = fixtures._v24_verified_payload(self.repo, dict(row, source_path=name))
                        self.assertEqual(row['bytes'], len(raw))
                        self.assertEqual(row['sha256'], hashlib.sha256(raw).hexdigest())
                        self.assertEqual(row['git_blob'], hashlib.sha1(
                            f'blob {len(raw)}\0'.encode('ascii') + raw).hexdigest())
                        if version in (30, 29, 28):
                            resolver = {30: fixtures.v30_source_path, 29: fixtures.v29_source_path,
                                        28: fixtures.v28_source_path}[version]
                            self.assertEqual(raw, resolver(name, source_root=self.repo).read_bytes())

    def test_live_drift_and_6b_c72_older_rollbacks_cannot_bypass_v32_after_bytes(self):
        histories = [self.parent, fixtures._v31_transition(self.repo)[1],
                     fixtures._v30_transition(self.repo)[1], fixtures._v29_transition(self.repo)[1],
                     fixtures._v27_parent_manifest(self.repo)]
        rows_by_version = [{row['path']: row for row in manifest['members']} for manifest in histories]
        for name in sorted(ROBE_DATA | INDEX_PATHS):
            # Resolve each historical identity before replacing any live source.
            rollbacks = [(f'v{31 - index}-rollback', fixtures._v24_verified_payload(
                self.repo, records[name])) for index, records in enumerate(rows_by_version)]
            payloads = [('drift', (ROOT / name).read_bytes() + b'\n'), *rollbacks]
            for kind, raw in payloads:
                with self.subTest(path=name, kind=kind), self.changed(name, raw), offline():
                    for records in rows_by_version:
                        with self.assertRaises(AssertionError):
                            fixtures._v24_verified_payload(self.repo, dict(records[name], source_path=name))
                    for resolver in (fixtures.v30_source_path, fixtures.v29_source_path, fixtures.v28_source_path):
                        with self.assertRaises(AssertionError):
                            resolver(name, source_root=self.repo)

    def test_live_recovery_rejects_mode_and_historical_identity_drift(self):
        for name in sorted(ROBE_DATA | INDEX_PATHS):
            row = self.records[name]
            with self.subTest(path=name), self.changed(name, (ROOT / name).read_bytes(), 0o600), offline():
                with self.assertRaises(AssertionError):
                    fixtures._v24_verified_payload(self.repo, dict(row, source_path=name))
                for resolver in (fixtures.v30_source_path, fixtures.v29_source_path, fixtures.v28_source_path):
                    with self.assertRaises(AssertionError):
                        resolver(name, source_root=self.repo)
            for field, value in (('bytes', row['bytes'] + 1), ('sha256', '0' * 64),
                                 ('git_blob', '0' * 40), ('mode', '100600')):
                with self.subTest(path=name, field=field), offline(), self.assertRaises(AssertionError):
                    fixtures._v24_verified_payload(self.repo, dict(row, source_path=name, **{field: value}))

    def test_original_payload_rejects_bytes_missing_mode_symlink_size_hash_and_blob_drift(self):
        row = self.records['tests/photo_prompt_fixtures.py']
        name = row['source_path']
        raw = (ROOT / name).read_bytes()
        for kind in ('bytes', 'missing', 'mode', 'symlink'):
            payload = None if kind in ('missing', 'symlink') else raw + (b'\n' if kind == 'bytes' else b'')
            with self.subTest(kind=kind), self.changed(name, payload, 0o600 if kind == 'mode' else None) as path:
                if kind == 'symlink': path.symlink_to(ROOT / name)
                with offline(), self.assertRaises(AssertionError):
                    fixtures._v24_verified_payload(self.repo, row)
        for field, value in (('bytes', len(raw) + 1), ('sha256', '0' * 64), ('git_blob', '0' * 40)):
            with self.subTest(field=field), offline(), self.assertRaises(AssertionError):
                fixtures._v24_verified_payload(self.repo, dict(row, **{field: value}))

    def test_payload_paths_and_source_root_ancestors_cannot_escape(self):
        row = self.parent['members'][0]
        for name in ('/tmp/escaped-v32', '../escaped-v32', 'nested/../payload', './payload',
                     'nested//payload', 'nested\\payload', 'C:/payload', 'nested/\x00payload'):
            with self.subTest(path=name), self.assertRaises(AssertionError):
                fixtures._v24_verified_payload(self.repo, dict(row, source_path=name))
        alias = self.repo / 'linked-source'
        alias.symlink_to(ROOT, target_is_directory=True)
        with self.assertRaises(AssertionError):
            fixtures._v32_transition(alias)

    def test_rehashed_manifest_still_rejects_wrong_identity_paths_and_inventory(self):
        for kind in ('commit', 'tree', 'duplicate', 'absolute', 'traversal', 'noncanonical',
                     'conflicting_backing', 'mode', 'blob', 'count', 'total'):
            parent, proof = copy.deepcopy(self.parent), copy.deepcopy(self.proof)
            row = parent['members'][0]
            if kind == 'commit': parent['source_pin'] = '0' * 40
            elif kind == 'tree': parent['source_tree'] = '0' * 40
            elif kind == 'duplicate': parent['members'][1] = copy.deepcopy(row)
            elif kind == 'absolute': row['path'] = '/tmp/escaped-v32'
            elif kind == 'traversal': row['source_path'] = '../escaped-v32'
            elif kind == 'noncanonical': row['source_path'] = 'nested//payload'
            elif kind == 'conflicting_backing': parent['members'][1]['source_path'] = row['source_path']
            elif kind == 'mode': row['mode'] = '120000'
            elif kind == 'blob': row['git_blob'] = 'z' * 40
            elif kind == 'count': parent['member_count'] -= 1
            else: parent['total_member_bytes'] += 1
            parent_raw = encoded(parent)
            parent_sha = hashlib.sha256(parent_raw).hexdigest()
            proof['parent_manifest_sha256'] = parent_sha
            proof_raw = encoded(proof)
            # Bypass only outer digest pins to exercise independent structural checks.
            with self.subTest(kind=kind), self.changed(fixtures.V31_PARENT_SOURCE, parent_raw), \
                    self.changed(fixtures.V32_ROBE_PROOF, proof_raw), \
                    mock.patch.object(fixtures, 'V31_PARENT_SOURCE_SHA256', parent_sha), \
                    mock.patch.object(fixtures, 'V32_ROBE_PROOF_SHA256', hashlib.sha256(proof_raw).hexdigest()):
                with offline(), self.assertRaises(AssertionError):
                    fixtures._v32_transition(self.repo)

    def test_missing_or_rehashed_transition_never_falls_back_or_writes_output(self):
        for name in (fixtures.V32_ROBE_PROOF, fixtures.V31_PARENT_SOURCE):
            for raw in (None, (ROOT / name).read_bytes() + b'\n'):
                destination = self.repo / 'destination'
                with self.subTest(path=str(name), missing=raw is None), self.changed(name, raw):
                    with offline(), self.assertRaises(AssertionError):
                        fixtures.materialize_v31_parent_source(destination, source_root=self.repo)
                self.assertFalse(destination.exists())
        row = self.parent['members'][0]
        with self.changed(row['source_path'], None), offline(), self.assertRaises(AssertionError):
            fixtures.materialize_v31_parent_source(self.repo / 'destination', source_root=self.repo)
        self.assertFalse((self.repo / 'destination').exists())
        self.assertFalse(list(self.repo.glob('.sealed-v31-*')))

    def test_missing_archived_payload_cannot_substitute_identical_live_bytes(self):
        name = sorted(ROBE_DATA)[0]
        row = self.records[name]
        before = (ROOT / row['source_path']).read_bytes()
        with self.changed(name, before), self.changed(row['source_path'], None), offline():
            with self.assertRaises(AssertionError):
                fixtures._v24_verified_payload(self.repo, row)

    def test_destination_checks_and_late_failure_are_atomic_without_large_copies(self):
        occupied = self.repo / 'occupied'
        occupied.mkdir()
        (occupied / 'keep').write_text('keep')
        regular = self.repo / 'regular'
        regular.write_text('keep')
        empty = self.repo / 'empty'
        empty.mkdir()
        alias = self.repo / 'alias'
        alias.symlink_to(empty, target_is_directory=True)
        for destination in (occupied, regular, alias, alias / 'child'):
            with self.subTest(destination=destination), offline(), self.assertRaises(AssertionError):
                fixtures.materialize_v31_parent_source(destination, source_root=self.repo)
        self.assertEqual('keep', (occupied / 'keep').read_text())
        self.assertEqual('keep', regular.read_text())
        self.assertEqual([], list(empty.iterdir()))
        # Authenticating all 1,354 members is covered by the boundary positive.
        # A two-member injected inventory isolates late-copy atomicity cheaply.
        rows = sorted(self.parent['members'], key=lambda row: row['bytes'])[:2]
        manifest = dict(self.parent, members=rows)
        original = fixtures._v24_verified_payload
        for existing in (False, True):
            destination = self.repo / ('late-existing' if existing else 'late-absent')
            if existing: destination.mkdir()
            count = 0

            def changed_during_copy(source, row):
                nonlocal count
                count += 1
                if count == len(rows) + 2:
                    raise AssertionError('Source changed after preflight')
                return original(source, row)

            with self.subTest(existing=existing), offline(), \
                    mock.patch.object(fixtures, '_v32_transition', return_value=(self.proof, manifest)), \
                    mock.patch.object(fixtures, '_v24_verified_payload', side_effect=changed_during_copy):
                with self.assertRaisesRegex(AssertionError, 'after preflight'):
                    fixtures.materialize_v31_parent_source(destination, source_root=self.repo)
            self.assertEqual(existing, destination.exists())
            self.assertEqual([], list(destination.iterdir()) if existing else [])
            self.assertFalse(list(self.repo.glob('.sealed-v31-*')))


if __name__ == '__main__':
    unittest.main()
