"""Merged V34 qualifies current scope while both committed V33 originals survive."""
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

from tests import photo_data_scope_history_v34 as history
from tests import photo_prompt_fixtures as fixtures

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / history.ILLUSTRATION / 'scripts'))
sys.path.insert(0, str(ROOT / 'skills/photo-prompt-image-generator/scripts'))
import validate_illustration_assets as validator
import photo_candidate_semantics as semantics
import prompt_generator as generator


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


class MergedDataScopeBoundaryHistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proof, cls.parent = history.transition(ROOT)
        cls.manifests = {stage: history.source_manifest(stage, ROOT) for stage in history.SOURCES}
        cls.records = {stage: {row['path']: row for row in manifest['members']}
                       for stage, manifest in cls.manifests.items()}
        cls.assets = ROOT / history.ILLUSTRATION / 'assets'
        cls.baseline = json.loads((cls.assets / 'photo_regression_baseline_v34.json').read_bytes())
        cls.raw = (cls.assets / 'photo_regression_baseline_v34_pack.json').read_bytes()
        cls.pack = json.loads(cls.raw)[0]
        cls.previous = json.loads((cls.assets / 'photo_regression_baseline_v33_pack.json').read_bytes())

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='.scope-v34-', dir=ROOT)
        self.addCleanup(temporary.cleanup)
        self.repo = Path(temporary.name).resolve()
        paths = {row['source_path'] for manifest in self.manifests.values() for row in manifest['members']}
        for field in ('source_files_after', 'active_shards_after', 'retained_shards_before',
                      'evidence_files', 'frozen_inputs'):
            paths.update(self.proof[field])
        paths.update((history.PROOF.as_posix(), self.proof['upstream_proof'],
                      'tests/photo_data_scope_history_v34.py', 'tests/photo_palette_history.py',
                      (history.ILLUSTRATION / 'scripts/validate_illustration_assets.py').as_posix(),
                      (history.ILLUSTRATION / 'assets/universal_scene_baseline_v2.json').as_posix()))
        paths.update((history.BASE / config[0]).as_posix() for config in history.SOURCES.values())
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
        history.qualify_current(validator, self.repo / history.ILLUSTRATION / 'assets', self.repo,
                                baseline or self.baseline, pack or self.pack, raw or self.raw, receipt)

    def test_current_default_cli_and_real_receipt_qualify_v34(self):
        import photo_runtime_sources as runtime
        with tempfile.TemporaryDirectory(prefix='photo-v34-store-') as temporary, mock.patch.dict(
                os.environ, PHOTO_RUNTIME_STORE=temporary, GEMINI_API_KEY='', GOOGLE_API_KEY=''):
            runtime.SnapshotPublisher().publish()
            result = validator.validate_photo_regression_baseline(self.assets)
        self.assertEqual('photo_regression_baseline/v34', result['schema'])
        self.assertEqual(self.proof['current_pack_sha256'], result['sha256'])
        self.assertEqual(self.proof['current_pack_id'], result['pack_id'])

    def test_requested_v32_and_v33_dispatch_execute_exact_original_validators(self):
        expected = {'v32': 32, 'upstream-v33': 33}
        for stage, version in expected.items():
            row = self.records[stage][(history.ILLUSTRATION / f'assets/photo_regression_baseline_v{version}.json').as_posix()]
            baseline = json.loads(history.exact_payload(ROOT, row))
            with self.subTest(stage=stage):
                result = validator.validate_photo_regression_baseline(self.assets, baseline_version=version)
                self.assertEqual(baseline['schema'], result['schema'])
                self.assertEqual(baseline['sha256'], result['sha256'])
                self.assertEqual(baseline['pack_id'], result['pack_id'])

    def test_five_pack_leaves_preserve_palette_candidates_order_and_all_contracts(self):
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
        previous = json.loads((self.assets / 'photo_regression_baseline_v33.json').read_bytes())
        for field in ('frozen_inputs', 'preserved_contract_sha256', 'negative_en', 'private_fields_absent'):
            self.assertEqual(previous[field], self.baseline[field])

    def test_six_scope_additions_and_four_maintenance_replacements_are_entire_authored_delta(self):
        self.assertEqual([2, 4, 4], sorted(map(len, self.proof['source_leaf_delta'].values())))
        operations=[row['operation'] for rows in self.proof['source_leaf_delta'].values() for row in rows]
        self.assertEqual((6,4),(operations.count('add'),operations.count('replace')))
        for name, changes in self.proof['source_leaf_delta'].items():
            source = json.loads(history.exact_payload(self.repo, self.records['upstream-v33'][name]))
            for row in changes:
                parent, key = target(source, row['pointer'])
                if row['pointer'].startswith('/maintenance_ref/'):
                    self.assertEqual('replace',row['operation'])
                    self.assertEqual(row['before'],parent[key])
                else:
                    self.assertEqual('add',row['operation'])
                    self.assertNotIn(key,parent)
                parent[key] = row['after']
            self.assertEqual(source, json.loads((self.repo / name).read_bytes()))
        policy=json.loads((ROOT/history.PHOTO/'photo_prompt_tags.json').read_bytes()).get('candidate_semantic_policy',{})
        for name,row in self.proof['maintenance_scope_corrections'].items():
            source=json.loads((self.repo/name).read_bytes())
            ref=source.pop('maintenance_ref')
            record=json.loads((self.repo/row['current_record_path']).read_bytes())
            previous=json.loads((self.repo/row['previous_record_path']).read_bytes())
            self.assertEqual(ref['sha256'],semantics.digest(record))
            self.assertEqual(record['authored_source_sha256'],semantics.digest(source))
            self.assertEqual({k:v for k,v in previous['maintenance_only'].items() if k!='source_revision'},
                             {k:v for k,v in record['maintenance_only'].items() if k!='source_revision'})
            old_revision=previous['maintenance_only']['source_revision']
            new_revision=copy.deepcopy(record['maintenance_only']['source_revision'])
            self.assertEqual(row['scoped_source_raw_sha256'],new_revision.pop('scope_correction')['previous_scoped_source_raw_sha256'])
            self.assertEqual(old_revision,new_revision)
            before=copy.deepcopy(source); before['maintenance_ref']=row['previous_reference']
            after=copy.deepcopy(source); after['maintenance_ref']=ref
            self.assertEqual(generator.merge_research_extension({'candidate_semantic_policy':copy.deepcopy(policy)},before),
                             generator.merge_research_extension({'candidate_semantic_policy':copy.deepcopy(policy)},after))
        palette = ('photo_prompt_palette_applications_extension.json', 'photo_prompt_visual_obligations_palette_applications.json',
                   'photo_prompt_source_manifest.json')
        for basename in palette:
            name = (history.PHOTO / basename).as_posix()
            self.assertEqual(history.exact_payload(self.repo, self.records['upstream-v33'][name]),
                             (self.repo / name).read_bytes())

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
            baseline = dict(self.baseline, sha256=history.digest(raw), pack_id=pack['pack_id'])
            with self.subTest(kind=kind), self.changed(history.ILLUSTRATION / 'assets/photo_regression_baseline_v34_pack.json', raw):
                with self.assertRaises(validator.ValidationFailure):
                    self.validate(pack=pack, raw=raw, baseline=baseline)

    def test_live_drift_original_rollbacks_and_mode_never_bypass_v34(self):
        for name in sorted(history.RECOVERY):
            current = (ROOT / name).read_bytes()
            variants = [('bytes', current + b'\n', None), ('mode', current, 0o600)]
            for stage in self.manifests:
                original = history.exact_payload(self.repo, self.records[stage][name])
                if original != current:
                    variants.append((stage + '-rollback', original, None))
            for kind, raw, mode in variants:
                with self.subTest(path=name, kind=kind), self.changed(name, raw, mode), offline():
                    with self.assertRaises(AssertionError):
                        history.previous_path(self.repo, name)
                    with self.assertRaises(AssertionError):
                        fixtures._v24_verified_payload(self.repo, dict(self.records['v32'][name], source_path=name))

    def test_exact_v31_through_v27_identities_recover_without_external_access(self):
        histories = [fixtures._v32_transition(self.repo)[1], fixtures._v31_transition(self.repo)[1],
                     fixtures._v30_transition(self.repo)[1], fixtures._v29_transition(self.repo)[1],
                     fixtures._v27_parent_manifest(self.repo)]
        with offline():
            for manifest in histories:
                records = {row['path']: row for row in manifest['members']}
                for name in sorted(history.DATA | history.INDEX):
                    row = records[name]
                    with self.subTest(version=manifest['schema'], path=name):
                        raw = fixtures._v24_verified_payload(self.repo, dict(row, source_path=name))
                        self.assertEqual(row['sha256'], history.digest(raw))
                        self.assertEqual(row['git_blob'], hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest())

    def test_missing_or_rehashed_proof_and_all_source_manifests_never_fall_back(self):
        name = sorted(history.DATA)[0]
        for evidence in (history.PROOF, *(history.BASE / c[0] for c in history.SOURCES.values())):
            for raw in (None, (ROOT / evidence).read_bytes() + b'\n'):
                with self.subTest(path=str(evidence), missing=raw is None), self.changed(evidence, raw), offline():
                    with self.assertRaises(AssertionError):
                        history.previous_path(self.repo, name)
        for row in self.proof['maintenance_scope_corrections'].values():
            for field in ('previous_record_path','current_record_path'):
                name=row[field]
                for raw in (None,(ROOT/name).read_bytes()+b'\n'):
                    with self.subTest(record=name,missing=raw is None),self.changed(name,raw),offline():
                        with self.assertRaises((validator.ValidationFailure,AssertionError)):
                            self.validate()

    def test_archived_original_payload_bytes_mode_symlink_and_identity_are_authenticated(self):
        for stage, module in (('v32', 'tests/test_photo_robe_source_boundary_history.py'),
                              ('local-v33', 'tests/test_photo_data_scope_boundary_history.py'),
                              ('upstream-v33', 'tests/test_photo_palette_boundary_history.py')):
            row = self.records[stage][module]
            name, raw = row['source_path'], history.exact_payload(self.repo, row)
            for kind in ('missing', 'bytes', 'mode', 'symlink'):
                payload = None if kind in ('missing', 'symlink') else raw + (b'\n' if kind == 'bytes' else b'')
                with self.subTest(stage=stage, kind=kind), self.changed(name, payload, 0o600 if kind == 'mode' else None) as path:
                    if kind == 'symlink': path.symlink_to(ROOT / name)
                    with offline(), self.assertRaises(AssertionError):
                        history.exact_payload(self.repo, row)
            for key, value in (('bytes', len(raw) + 1), ('sha256', '0' * 64), ('git_blob', '0' * 40)):
                with self.subTest(stage=stage, field=key), offline(), self.assertRaises(AssertionError):
                    history.exact_payload(self.repo, dict(row, **{key: value}))

    def test_source_paths_cannot_escape_or_alias_symlink(self):
        row = self.parent['members'][0]
        for name in ('/tmp/escaped-v34', '../escape', 'nested/../payload', './payload', 'nested//payload',
                     'nested\\payload', 'C:/payload', 'nested/\x00payload'):
            with self.subTest(path=name), self.assertRaises(AssertionError):
                history.exact_payload(self.repo, dict(row, source_path=name))
        alias = self.repo / 'linked-source'
        alias.symlink_to(ROOT, target_is_directory=True)
        with self.assertRaises(AssertionError):
            history.source_manifest('upstream-v33', alias)

    def test_rehashed_manifests_still_reject_inventory_provenance_and_overlap_drift(self):
        stage = 'upstream-v33'
        for kind in ('commit', 'tree', 'duplicate', 'path', 'mode', 'blob', 'count', 'total', 'overlap'):
            parent = copy.deepcopy(self.manifests[stage])
            row = parent['members'][0]
            if kind == 'commit': parent['source_pin'] = '0' * 40
            elif kind == 'tree': parent['source_tree'] = '0' * 40
            elif kind == 'duplicate': parent['members'][1] = copy.deepcopy(row)
            elif kind == 'path': row['path'] = '../escape-v34'
            elif kind == 'mode': row['mode'] = '120000'
            elif kind == 'blob': row['git_blob'] = 'z' * 40
            elif kind == 'count': parent['member_count'] -= 1
            elif kind == 'total': parent['total_member_bytes'] += 1
            else:
                parent['members'][1]['path'] = row['path'] + '/overlap'
                parent['members'][1]['git_path'] = row['path'] + '/overlap'
            raw = encoded(parent)
            config = list(history.SOURCES[stage]); config[1] = history.digest(raw)
            with self.subTest(kind=kind), self.changed(history.BASE / config[0], raw), \
                    mock.patch.dict(history.SOURCES, {stage: tuple(config)}), offline():
                with self.assertRaises(AssertionError):
                    history.source_manifest(stage, self.repo)

    def test_destination_and_late_copy_failures_are_atomic(self):
        occupied = self.repo / 'occupied'
        occupied.mkdir(); (occupied / 'keep').write_text('keep')
        alias = self.repo / 'alias'
        alias.symlink_to(occupied, target_is_directory=True)
        with offline():
            for destination in (occupied, alias, alias / 'child'):
                with self.subTest(destination=destination), self.assertRaises(AssertionError):
                    history.materialize('upstream-v33', destination, source_root=self.repo)
        self.assertEqual('keep', (occupied / 'keep').read_text())
        rows = sorted(self.parent['members'], key=lambda row: row['bytes'])[:2]
        original, count = history.exact_payload, 0
        def fail_during_copy(source, row):
            nonlocal count
            count += 1
            if count == len(rows) + 2:
                raise AssertionError('Source changed after preflight')
            return original(source, row)
        destination = self.repo / 'destination'
        with offline(), mock.patch.object(history, 'source_manifest', return_value=dict(self.parent, members=rows)), \
                mock.patch.object(history, 'exact_payload', side_effect=fail_during_copy):
            with self.assertRaisesRegex(AssertionError, 'after preflight'):
                history.materialize('upstream-v33', destination, source_root=self.repo)
        self.assertFalse(destination.exists())
        self.assertFalse(list(self.repo.glob('.sealed-upstream-v33-*')))

    def test_history_python_explicit_override_requires_each_exact_environment(self):
        for stage, manifest in self.manifests.items():
            variable = 'PHOTO_V32_PYTHON' if stage == 'v32' else 'PHOTO_HISTORY_PYTHON'
            python = '/tmp/photo-v34-' + stage + '-python'
            with self.subTest(stage=stage), mock.patch.dict(os.environ, {variable: python}), \
                    mock.patch.object(history.subprocess, 'run', return_value=subprocess.CompletedProcess(
                        [], 0, stdout=json.dumps(manifest['environment']))) as probe:
                selected, actual = history.resolve_python(stage, self.repo)
                self.assertEqual(Path(python), selected)
                self.assertEqual(manifest['environment'], actual)
            probe.assert_called_once()
            self.assertEqual(python, probe.call_args.args[0][0])

    def test_history_python_wrong_override_cannot_silently_fall_back(self):
        for stage in self.manifests:
            variable = 'PHOTO_V32_PYTHON' if stage == 'v32' else 'PHOTO_HISTORY_PYTHON'
            with self.subTest(stage=stage), mock.patch.dict(os.environ, {variable: '/tmp/wrong-history-python'}), \
                    mock.patch.object(history.subprocess, 'run', return_value=subprocess.CompletedProcess(
                        [], 0, stdout=json.dumps(dict(implementation='cpython', python=[3, 1, 0], unicode='0.0')))) as probe:
                with self.assertRaisesRegex(AssertionError, 'Exact .* Python/Unicode environment unavailable'):
                    history.resolve_python(stage, self.repo)
            probe.assert_called_once()

    def test_current_receipt_generation_fingerprint_and_algorithm_drift_fail(self):
        receipt = json.loads((ROOT / history.BASE / 'CURRENT-BOUNDARY-RECEIPT.json').read_bytes())
        for field in ('generation_id', 'source_fingerprint', 'algorithm_sha256'):
            wrong = dict(receipt, **{field: '0' * 64})
            with self.subTest(field=field), self.assertRaisesRegex(validator.ValidationFailure, 'receipt source generation drift'):
                self.validate(receipt=wrong)

    def test_local_original_qualification_is_parallel_and_canonical_v33_is_upstream(self):
        path = (history.ILLUSTRATION / 'assets/photo_regression_baseline_v33_pack.json').as_posix()
        local = history.exact_payload(self.repo, self.records['local-v33'][path])
        upstream = history.exact_payload(self.repo, self.records['upstream-v33'][path])
        self.assertEqual('d6f893dfeecad5968ba80db4e44689c09f99ab16f4b4aa6ae9b88fcc84a6e525', history.digest(local))
        self.assertEqual('117d4261b14676bf59968f2d52717a36a9722d584a40970cb1b74c400ffdd783', history.digest(upstream))
        self.assertEqual(upstream, (self.assets / 'photo_regression_baseline_v33_pack.json').read_bytes())
        self.assertNotEqual(json.loads(local)[0]['pack_id'], json.loads(upstream)[0]['pack_id'])
        self.assertEqual(16, sum(1 for line in history.exact_payload(self.repo,
            self.records['local-v33']['tests/test_photo_data_scope_boundary_history.py']).splitlines() if line.startswith(b'    def test_')))


if __name__ == '__main__':
    unittest.main()
