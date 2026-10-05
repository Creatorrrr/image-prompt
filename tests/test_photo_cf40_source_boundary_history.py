"""V19 binds three source changes without changing any reviewed V18 pack field."""
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
EVIDENCE = Path('docs/research-evidence/photo-prompt/cf40-history-repair-20261005')
sys.path.insert(0, str(ILLUSTRATION / 'scripts'))


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


class AuthoringSourceBoundaryHistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global ROOT, ILLUSTRATION, v
        cls.live_root = ROOT
        temp = tempfile.TemporaryDirectory(prefix='immutable-v19-parent-')
        cls.addClassCleanup(temp.cleanup)
        ROOT = Path(temp.name)
        with mock.patch('subprocess.Popen', side_effect=AssertionError('Historical fixture invoked a subprocess')):
            v = fixtures.archived_validator_with_v21_source(ROOT, version=19, source_root=cls.live_root)
        ILLUSTRATION = ROOT / 'skills/subculture-illustration-image-generator'
        cls.proof = json.loads((ROOT / EVIDENCE / 'V19-SOURCE-BINDING-PROOF.json').read_bytes())
        cls.parent = json.loads((ROOT / cls.proof['source_parent_manifest']).read_bytes())

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.repo = Path(temp.name)
        self.assets = self.repo / ILLUSTRATION.relative_to(ROOT) / 'assets'
        paths = set()
        for field in ('immutable_history', 'historical_dependencies', 'source_parent_files',
                      'source_files', 'active_semantic_shards'):
            paths.update(self.proof[field])
        paths.update(str(path.relative_to(ROOT)) for path in (ILLUSTRATION / 'assets').glob('photo_regression_baseline_v*.json'))
        paths.update([str(EVIDENCE / 'V19-SOURCE-BINDING-PROOF.json'),
                      self.proof['source_parent_manifest'],
                      str((ILLUSTRATION / 'assets/universal_scene_baseline_v2.json').relative_to(ROOT))])
        for name in paths:
            target = self.repo / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.symlink_to(ROOT / name)
        self.baseline = json.loads((self.assets / 'photo_regression_baseline_v19.json').read_bytes())
        self.raw = (self.assets / 'photo_regression_baseline_v19_pack.json').read_bytes()
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
        return v._validate_v19_authoring_source_successor(
            self.assets, self.repo, self.baseline,
            self.pack if pack is None else pack, self.raw if raw is None else raw)

    def test_zero_pack_delta_preserves_every_field_and_byte(self):
        self.validate()
        old = (self.assets / 'photo_regression_baseline_v18_pack.json').read_bytes()
        self.assertEqual(old, self.raw)
        self.assertEqual(json.loads(old)[0], self.pack)
        self.assertEqual([], self.proof['changed_pack_leaves'])
        self.assertEqual(64, v._public_photo_candidate_count(self.pack))

    def test_registered_default_and_explicit_v19(self):
        def frozen_command(command, **kwargs):
            Path(command[command.index('--output-file') + 1]).write_bytes(self.raw)
            return subprocess.CompletedProcess(command, 0, '', '')
        # This tests dispatch. The focused universal test executes the real CLI.
        with mock.patch.object(v.subprocess, 'run', side_effect=frozen_command):
            for version in (None, 19):
                result = v.validate_photo_regression_baseline(ILLUSTRATION / 'assets', baseline_version=version)
                self.assertEqual('photo_regression_baseline/v19', result['schema'])
                self.assertEqual(self.proof['unchanged_pack_sha256'], result['sha256'])

    def test_unregistered_future_version_is_rejected(self):
        with self.assertRaisesRegex(v.ValidationFailure, 'unsupported photo baseline version'):
            v.validate_photo_regression_baseline(self.assets, baseline_version=20)

    def test_exact_three_source_changes_and_preserved_extension_meaning(self):
        old = json.loads((ROOT / self.proof['previous_proof_path']).read_bytes())['source_files']
        current = self.proof['source_files']
        rows = [{'path': name, 'previous': old[name], 'current': current[name]}
                for name in sorted(old) if old[name] != current[name]]
        self.assertEqual(self.proof['reviewed_source_deltas'], rows)
        self.assertEqual(3, len(rows))
        members = {row['path']: row for row in self.parent['members']}
        for row in rows:
            before = (ROOT / members[row['path']]['source_path']).read_bytes()
            after = (ROOT / row['path']).read_bytes()
            self.assertEqual(row['previous'], digest(before))
            self.assertEqual(row['current'], digest(after))
            if row['path'].endswith('.json'):
                a, b = json.loads(before), json.loads(after)
                self.assertNotEqual(a.pop('maintenance_ref'), b.pop('maintenance_ref'))
                self.assertEqual(a, b)
        self.assertTrue(self.proof['qualification_scope']['authoring_guidance_changed'])
        self.assertTrue(self.proof['qualification_scope']['future_authored_output_equivalence_not_established'])

    def test_candidate_order_core_owner_controls_negative_and_privacy_rehash_rejected(self):
        name = str((ILLUSTRATION / 'assets/photo_regression_baseline_v19_pack.json').relative_to(ROOT))
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
            with self.subTest(kind=kind), self.changed(name, raw), self.assertRaisesRegex(v.ValidationFailure, 'zero pack delta'):
                self.validate(changed, raw)

    def test_source_guidance_runtime_extra_data_and_index_mutations_rejected(self):
        source = Path(self.baseline['command'][1]).parent.parent
        names = [row['path'] for row in self.proof['reviewed_source_deltas']]
        names += [str(source / 'scripts/prompt_generator.py'),
                  str(source / 'assets/photo_prompt_semantic_index.json'),
                  str(source / 'assets/photo_prompt_visual_profile_index.json')]
        for name in names:
            with self.subTest(path=name), self.changed(name, (ROOT / name).read_bytes() + b'\n'), self.assertRaisesRegex(v.ValidationFailure, 'historical source manifest|DATA inventory|source binding'):
                self.validate()
        with self.changed(source / 'assets/unexpected.json', b'{}'), self.assertRaisesRegex(v.ValidationFailure, 'exact DATA inventory'):
            self.validate()

    def test_active_shard_mutation_extra_and_missing_are_rejected(self):
        name = next(iter(self.proof['active_semantic_shards']))
        for path, raw in ((name, (ROOT / name).read_bytes() + b' '),
                          (str(Path(name).parent / 'shard-999.json'), b'{}')):
            with self.subTest(path=path), self.changed(path, raw), self.assertRaisesRegex(v.ValidationFailure, 'historical source|active semantic'):
                self.validate()
        (self.repo / name).unlink()
        with self.assertRaises((v.ValidationFailure, FileNotFoundError)):
            self.validate()

    def test_fixed_proof_cannot_authorize_rehashed_source_or_pack_changes(self):
        for field, value in (('reviewed_source_deltas', []), ('source_commit', '0' * 40),
                             ('source_tree', '0' * 40), ('source_inventory_after', {}),
                             ('source_parent_files', {}), ('unchanged_pack_sha256', '0' * 64)):
            changed = copy.deepcopy(self.proof)
            changed[field] = value
            raw = json.dumps(changed).encode()
            self.baseline['authoring_source_transition']['evidence_sha256'] = digest(raw)
            with self.subTest(field=field), self.changed(EVIDENCE / 'V19-SOURCE-BINDING-PROOF.json', raw), self.assertRaisesRegex(v.ValidationFailure, 'immutable source proof'):
                self.validate()

    def test_history_parent_manifest_snapshot_and_previous_proof_are_immutable(self):
        cases = [
            (str((ILLUSTRATION / 'assets/photo_regression_baseline_v18.json').relative_to(ROOT)), 'immutable predecessor'),
            (self.proof['previous_proof_path'], 'historical dependency'),
            (self.proof['source_parent_manifest'], 'historical source manifest'),
            (self.proof['universal_v2_before_path'], 'historical source manifest'),
        ]
        for name, message in cases:
            with self.subTest(path=name), self.changed(name, (ROOT / name).read_bytes() + b'\n'), self.assertRaisesRegex(v.ValidationFailure, message):
                self.validate()

    def test_baseline_cannot_change_the_source_commit(self):
        self.baseline['authoring_source_transition']['source_commit'] = 'PENDING'
        with self.assertRaisesRegex(v.ValidationFailure, 'source provenance'):
            self.validate()

    def test_transition_cannot_be_reclassified(self):
        for field in ('metadata_only_transition', 'zero_pack_delta_transition', 'optional_inventory_transition',
                      'authored_metadata_ownership_transition', 'cute_equivalent_language_inventory_transition',
                      'glass_interface_inventory_transition'):
            self.baseline[field] = {}
            with self.subTest(field=field), self.assertRaisesRegex(v.ValidationFailure, 'cannot relabel'):
                self.validate()
            del self.baseline[field]

    def test_v18_still_rejects_live_changed_sources(self):
        baseline = json.loads((self.assets / 'photo_regression_baseline_v18.json').read_bytes())
        with self.assertRaisesRegex(v.ValidationFailure, 'exact DATA inventory'):
            v._validate_v18_glass_data_successor(self.assets, ROOT, baseline, self.pack, self.raw)

    def test_universal_descriptor_only_replaces_validator_hash(self):
        old = (ROOT / self.proof['universal_v2_before_path']).read_bytes()
        actual = (self.assets / 'universal_scene_baseline_v2.json').read_bytes()
        self.assertEqual(old.replace(self.proof['previous_validator_sha256'].encode(), digest(Path(v.__file__).read_bytes()).encode(), 1), actual)
        name = str((ILLUSTRATION / 'assets/universal_scene_baseline_v2.json').relative_to(ROOT))
        with self.changed(name, actual + b'\n'), self.assertRaisesRegex(v.ValidationFailure, 'universal descriptor changed beyond validator hash'):
            self.validate()


if __name__ == '__main__':
    unittest.main()
