"""The glass row is additive DATA; V18 permits only four frozen-pack bindings."""
import copy
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import photo_prompt_fixtures as fixtures

ROOT = Path(__file__).resolve().parents[1]
ILLUSTRATION = ROOT / 'skills/subculture-illustration-image-generator'
EVIDENCE = Path('docs/research-evidence/photo-prompt/glass-main-merge-20261005')
sys.path.insert(0, str(ILLUSTRATION / 'scripts'))


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


class GlassInventoryBoundaryHistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global ROOT, ILLUSTRATION, v
        cls.live_root = ROOT
        temp = tempfile.TemporaryDirectory(prefix='immutable-v18-parent-')
        cls.addClassCleanup(temp.cleanup)
        ROOT = Path(temp.name)
        with mock.patch('subprocess.Popen', side_effect=AssertionError('Historical fixture invoked a subprocess')):
            v = fixtures.archived_v18_validator(ROOT, source_root=cls.live_root)
        ILLUSTRATION = ROOT / 'skills/subculture-illustration-image-generator'
        cls.proof = json.loads((ROOT / EVIDENCE / 'V18-GLASS-DATA-PROOF.json').read_bytes())
        cls.manifest = json.loads((ROOT / cls.proof['source_parent_manifest']).read_bytes())
        cls.members = {row['path']: row for row in cls.manifest['members']}

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.repo = Path(temp.name)
        self.assets = self.repo / ILLUSTRATION.relative_to(ROOT) / 'assets'
        # An isolated file-level mirror avoids copying historical archives for each mutation.
        paths = set()
        for field in ('immutable_history', 'historical_dependencies', 'source_parent_files',
                      'source_files', 'active_semantic_shards'):
            paths.update(self.proof[field])
        paths.update(str(path.relative_to(ROOT)) for path in (ILLUSTRATION / 'assets').glob('photo_regression_baseline_v*.json'))
        paths.update([str(EVIDENCE / 'V18-GLASS-DATA-PROOF.json'),
                      self.proof['source_parent_manifest'], self.proof['qualification_path'],
                      str((ILLUSTRATION / 'assets/universal_scene_baseline_v2.json').relative_to(ROOT))])
        for name in paths:
            target = self.repo / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.symlink_to(ROOT / name)
        self.baseline = json.loads((self.assets / 'photo_regression_baseline_v18.json').read_bytes())
        self.raw = (self.assets / 'photo_regression_baseline_v18_pack.json').read_bytes()
        self.pack = json.loads(self.raw)[0]

    @contextmanager
    def changed(self, name, raw):
        path = self.repo / name
        existed = path.exists()
        if path.is_symlink():
            path.unlink()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        try:
            yield path
        finally:
            path.unlink()
            if existed:
                path.symlink_to(ROOT / name)

    def validate(self, pack=None, raw=None):
        return v._validate_v18_glass_data_successor(
            self.assets, self.repo, self.baseline,
            self.pack if pack is None else pack, self.raw if raw is None else raw)

    def test_exact_four_reviewed_values_and_all_other_pack_fields(self):
        self.validate()
        old = json.loads((self.assets / 'photo_regression_baseline_v17_pack.json').read_bytes())[0]
        current = copy.deepcopy(self.pack)
        actual = []
        for path in (('core_retrieval', 'canonical_sha256'), ('core_retrieval', 'slot_corpus_sha256'),
                     ('pack_id',), ('provenance', 'tags_hash')):
            left, right = old, current
            for key in path[:-1]:
                left, right = left[key], right[key]
            key = path[-1]
            actual.append({'path': '/' + '/'.join(path), 'previous': left.pop(key), 'current': right.pop(key)})
        self.assertEqual(actual, self.proof['reviewed_binding_deltas'])
        self.assertEqual(old, current)
        self.assertEqual(64, v._public_photo_candidate_count(self.pack))

    def test_default_and_explicit_v18_registration(self):
        def frozen_command(command, **kwargs):
            Path(command[command.index('--output-file') + 1]).write_bytes(self.raw)
            return subprocess.CompletedProcess(command, 0, '', '')
        # Registration is isolated here; the real current-boundary command is checked separately.
        with mock.patch.object(v.subprocess, 'run', side_effect=frozen_command) as run:
            for version in (None, 18):
                result = v.validate_photo_regression_baseline(ILLUSTRATION / 'assets', baseline_version=version)
                self.assertEqual('photo_regression_baseline/v18', result['schema'])
                self.assertEqual(self.proof['current_pack_sha256'], result['sha256'])
            self.assertEqual(2, run.call_count)

    def test_unregistered_future_version_is_rejected(self):
        with self.assertRaisesRegex(v.ValidationFailure, 'unsupported photo baseline version'):
            v.validate_photo_regression_baseline(self.assets, baseline_version=19)

    def test_frozen_v18_rejects_current_source_binding_successor(self):
        with self.assertRaisesRegex(v.ValidationFailure, 'V18 (exact DATA inventory|DATA or runtime source binding)'):
            v._validate_v18_glass_data_successor(
                self.assets, self.live_root, self.baseline, self.pack, self.raw)

    def test_fixture_preserves_all_e68_source_and_support_bytes_without_git(self):
        manifest = fixtures._v18_parent_manifest(self.live_root)
        self.assertEqual((149, 193), (len(manifest['members']), len(manifest['dependencies'])))
        for row in manifest['members'] + manifest['dependencies']:
            raw = (ROOT / row['path']).read_bytes()
            self.assertEqual(digest(raw), row['sha256'], row['path'])
            self.assertEqual(len(raw), row['bytes'], row['path'])
        for row in fixtures._v17_support_manifest(self.live_root)['members']:
            self.assertEqual(digest((ROOT / row['path']).read_bytes()), row['sha256'])

    def test_fixture_manifest_cannot_rehash_relabel_or_redirect_source_members(self):
        original = (self.live_root / fixtures.V18_PARENT_MANIFEST).read_bytes()
        source = self.repo / 'bad-fixture-input'
        target = source / fixtures.V18_PARENT_MANIFEST
        target.parent.mkdir(parents=True)
        for kind in ('absolute', 'traversal', 'duplicate', 'missing', 'source_pin', 'live_source', 'coordinated_rehash'):
            manifest = json.loads(original)
            if kind == 'absolute': manifest['members'][0]['path'] = '/tmp/escaped-v18-fixture'
            elif kind == 'traversal': manifest['members'][0]['source_path'] = '../escaped-v18-fixture'
            elif kind == 'duplicate': manifest['members'][1] = manifest['members'][0]
            elif kind == 'missing': manifest['members'].pop()
            elif kind == 'source_pin': manifest['source_pin'] = '0' * 40
            elif kind == 'live_source': manifest['members'][0]['source_path'] = manifest['members'][0]['path']
            else:
                row = manifest['members'][0]
                raw = (self.live_root / row['source_path']).read_bytes() + b'\n'
                payload = source / row['source_path']
                payload.parent.mkdir(parents=True, exist_ok=True)
                payload.write_bytes(raw)
                manifest['total_member_bytes'] += 1
                row.update(sha256=digest(raw), bytes=len(raw),
                           git_blob=hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest())
            target.write_text(json.dumps(manifest))
            output = self.repo / 'invalid-fixture-output'
            with self.subTest(kind=kind), self.assertRaisesRegex(AssertionError, 'V18 parent source manifest drift'):
                fixtures.materialize_v18_parent_source(output, source_root=source)
            self.assertFalse(output.exists())

    def test_fixture_payload_snapshots_and_retained_shard_reject_missing_tampered_or_symlink_bytes(self):
        manifest = fixtures._v18_parent_manifest(self.live_root)
        rows = [row for row in manifest['members'] if row['kind'] == 'new_immutable_snapshot_same_git_blob']
        rows += [next(row for row in manifest['members'] if '/7ff3e10cc7163368/' in row['path'])]
        source = self.repo / 'payload-input'
        for row in rows:
            target = source / row['source_path']
            target.parent.mkdir(parents=True, exist_ok=True)
            with self.subTest(path=row['path'], change='missing'), self.assertRaisesRegex(AssertionError, 'Missing .*historical source payload'):
                fixtures._v17_verified_payload(source, row)
            target.write_bytes((self.live_root / row['source_path']).read_bytes() + b'\n')
            with self.subTest(path=row['path'], change='tampered'), self.assertRaisesRegex(AssertionError, 'payload drift'):
                fixtures._v17_verified_payload(source, row)
            target.unlink()
            target.symlink_to(self.live_root / row['source_path'])
            with self.subTest(path=row['path'], change='symlink'), self.assertRaisesRegex(AssertionError, 'historical source symlink'):
                fixtures._v17_verified_payload(source, row)
            target.unlink()

    def test_exact_one_row_and_old_semantic_objects_vectors_text_and_order(self):
        source = Path(self.baseline['command'][1]).parent.parent / 'assets'
        def old(name):
            return ROOT / self.members[str(source / name)]['source_path']
        previous = json.loads(old('photo_prompt_tags.json').read_bytes())
        current = json.loads((ROOT / source / 'photo_prompt_tags.json').read_bytes())
        row = current['slots']['texture'].pop()
        self.assertEqual('glass_near_contact_reflected_fringes', row['id'])
        self.assertEqual(134, len(previous['slots']['texture']))
        self.assertEqual(previous, current)
        before = json.loads(old('photo_prompt_semantic_index.json').read_bytes())
        after = json.loads((ROOT / source / 'photo_prompt_semantic_index.json').read_bytes())
        entry_id = 'slot:texture:' + row['id']
        self.assertEqual(10015, before['entry_count'])
        self.assertEqual(10016, after['entry_count'])
        self.assertEqual(before['entry_order'], [item for item in after['entry_order'] if item != entry_id])
        old_total = 0
        new_total = 0
        for previous_shard, current_shard in zip(before['shards'], after['shards']):
            previous_rows = json.loads(old(previous_shard['path']).read_bytes())['entries']
            current_rows = json.loads((ROOT / source / current_shard['path']).read_bytes())['entries']
            old_total += len(previous_rows)
            new_total += len(current_rows)
            current_rows.pop(entry_id, None)
            self.assertEqual(previous_rows, current_rows)
        self.assertEqual((10015, 10016), (old_total, new_total))
        self.assertEqual(old('photo_prompt_visual_profile_index.json').read_bytes(),
                         (ROOT / source / 'photo_prompt_visual_profile_index.json').read_bytes())

    def test_candidate_order_core_owner_controls_negative_and_privacy_mutations_rejected(self):
        for kind in ('candidate', 'order', 'core', 'owner', 'controls', 'negative', 'privacy'):
            changed = copy.deepcopy(self.pack)
            rows = next(slot['candidates'] for slot in changed['slots'].values() if len(slot['candidates']) >= 2)
            if kind == 'candidate': rows[0]['concept_terms'][0] += ' altered'
            elif kind == 'order': rows.reverse()
            elif kind == 'core': changed['authorial_core']['subject'] += ' altered'
            elif kind == 'owner': changed['core_retrieval']['slot_ownership_sha256'] = '0' * 64
            elif kind == 'controls': changed['creative_controls']['extra'] = True
            elif kind == 'negative': changed['negative_en'] += ', altered'
            else: changed['provenance']['private_routing_exposed'] = True
            changed['pack_id'] = v._canonical_photo_pack_id(changed)
            raw = (json.dumps([changed], ensure_ascii=False, indent=2) + '\n').encode()
            self.baseline.update(sha256=digest(raw), pack_id=changed['pack_id'])
            name = str((ILLUSTRATION / 'assets/photo_regression_baseline_v18_pack.json').relative_to(ROOT))
            with self.subTest(kind=kind), self.changed(name, raw), self.assertRaisesRegex(v.ValidationFailure, 'immutable pack binding'):
                self.validate(changed, raw)

    def test_each_reviewed_binding_value_is_fixed(self):
        for row in self.proof['reviewed_binding_deltas']:
            changed = copy.deepcopy(self.pack)
            target = changed
            parts = row['path'].strip('/').split('/')
            for key in parts[:-1]: target = target[key]
            target[parts[-1]] = row['previous']
            raw = (json.dumps([changed], ensure_ascii=False, indent=2) + '\n').encode()
            with self.subTest(path=row['path']), self.assertRaisesRegex(v.ValidationFailure, 'immutable pack binding'):
                self.validate(changed, raw)

    def test_extra_data_and_changed_data_or_index_order_are_rejected(self):
        source = Path(self.baseline['command'][1]).parent.parent / 'assets'
        cases = [(source / 'unexpected.json', b'{}')]
        for name in ('photo_prompt_tags.json', 'photo_prompt_visual_profile_index.json'):
            cases.append((source / name, (ROOT / source / name).read_bytes() + b'\n'))
        index = json.loads((ROOT / source / 'photo_prompt_semantic_index.json').read_bytes())
        index['entry_order'].reverse()
        cases.append((source / 'photo_prompt_semantic_index.json', json.dumps(index).encode()))
        for name, raw in cases:
            with self.subTest(path=str(name)), self.changed(name, raw), self.assertRaisesRegex(v.ValidationFailure, 'exact DATA inventory'):
                self.validate()

    def test_active_shard_mutation_extra_shard_and_missing_shard_are_rejected(self):
        name = next(iter(self.proof['active_semantic_shards']))
        for path, raw in ((name, (ROOT / name).read_bytes() + b' '),
                          (str(Path(name).parent / 'shard-999.json'), b'{}')):
            with self.subTest(path=path), self.changed(path, raw), self.assertRaisesRegex(v.ValidationFailure, 'active semantic shard'):
                self.validate()
        (self.repo / name).unlink()
        with self.assertRaisesRegex(v.ValidationFailure, 'active semantic shard'):
            self.validate()

    def test_proof_rehash_cannot_authorize_changed_scope(self):
        name = EVIDENCE / 'V18-GLASS-DATA-PROOF.json'
        for field, value in (('reviewed_binding_deltas', []), ('data_commit', '0' * 40),
                             ('source_inventory_after', {}), ('source_parent_files', {})):
            changed = copy.deepcopy(self.proof)
            changed[field] = value
            raw = json.dumps(changed).encode()
            self.baseline['glass_interface_inventory_transition']['evidence_sha256'] = digest(raw)
            with self.subTest(field=field), self.changed(name, raw), self.assertRaisesRegex(v.ValidationFailure, 'immutable glass DATA proof'):
                self.validate()

    def test_history_archive_manifest_and_qualification_mutations_are_rejected(self):
        cases = [
            (next(iter(self.proof['immutable_history'])), 'immutable predecessor'),
            (next(name for name in self.proof['historical_dependencies'] if name.endswith('.zip')), 'historical dependency'),
            (self.proof['source_parent_manifest'], 'historical source manifest'),
            (self.proof['qualification_path'], 'qualification evidence'),
            (self.proof['universal_v2_before_path'], 'historical source manifest'),
        ]
        for name, message in cases:
            with self.subTest(path=name), self.changed(name, (ROOT / name).read_bytes() + b'\n'), self.assertRaisesRegex(v.ValidationFailure, message):
                self.validate()

    def test_parent_shard_dependency_is_sealed(self):
        names = [name for name in self.proof['source_parent_files'] if '/7ed22190c0382b63/' in name]
        self.assertEqual(16, len(names))
        for name in names:
            with self.subTest(path=name), self.changed(name, b'{}'), self.assertRaisesRegex(v.ValidationFailure, 'historical source manifest'):
                self.validate()

    def test_transition_cannot_be_reclassified(self):
        for field in ('metadata_only_transition', 'zero_pack_delta_transition', 'optional_inventory_transition',
                      'authored_metadata_ownership_transition', 'cute_equivalent_language_inventory_transition'):
            self.baseline[field] = {}
            with self.subTest(field=field), self.assertRaisesRegex(v.ValidationFailure, 'cannot relabel'):
                self.validate()
            del self.baseline[field]

    def test_universal_descriptor_is_exact_except_validator_sha(self):
        old = (ROOT / self.proof['universal_v2_before_path']).read_bytes()
        actual = (self.assets / 'universal_scene_baseline_v2.json').read_bytes()
        self.assertEqual(old.replace(self.proof['previous_validator_sha256'].encode(), digest(Path(v.__file__).read_bytes()).encode(), 1), actual)
        name = str((ILLUSTRATION / 'assets/universal_scene_baseline_v2.json').relative_to(ROOT))
        with self.changed(name, actual + b'\n'), self.assertRaisesRegex(v.ValidationFailure, 'universal descriptor changed beyond validator hash'):
            self.validate()


if __name__ == '__main__':
    unittest.main()
