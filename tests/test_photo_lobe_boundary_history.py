"""V23 preserves the V22 pack while sealing the reviewed lobe DATA boundary."""
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

ROOT = Path(__file__).resolve().parents[1]
ILLUSTRATION = ROOT / 'skills/subculture-illustration-image-generator'
EVIDENCE = Path('docs/research-evidence/photo-prompt/lobe-boundary-integration-20261005')
PROOF = EVIDENCE / 'V23-LOBE-BINDING-PROOF.json'
sys.path.insert(0, str(ILLUSTRATION / 'scripts'))
import validate_illustration_assets as v


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


class LobeBoundaryHistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proof = json.loads((ROOT / PROOF).read_bytes())
        cls.qualification = json.loads((ROOT / cls.proof['qualification_path']).read_bytes())

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.repo = Path(temp.name)
        self.assets = self.repo / ILLUSTRATION.relative_to(ROOT) / 'assets'
        paths = set()
        for field in ('immutable_history', 'historical_dependencies', 'source_parent_files',
                      'source_files', 'active_semantic_shards', 'active_visual_shards',
                      'retained_semantic_shards', 'retained_visual_shards'):
            paths.update(self.proof[field])
        paths.update(self.qualification['files'])
        paths.update(str(path.relative_to(ROOT)) for path in
                     (ILLUSTRATION / 'assets').glob('photo_regression_baseline_v*.json'))
        paths.update((str(PROOF), self.proof['source_parent_manifest'],
                      self.proof['qualification_path'], self.proof['previous_proof_path'],
                      self.proof['universal_v2_before_path'],
                      str((ILLUSTRATION / 'assets/universal_scene_baseline_v2.json').relative_to(ROOT))))
        for name in paths:
            target = self.repo / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.symlink_to(ROOT / name)
        self.baseline = json.loads((self.assets / 'photo_regression_baseline_v23.json').read_bytes())
        self.original_baseline = copy.deepcopy(self.baseline)
        self.raw = (self.assets / 'photo_regression_baseline_v23_pack.json').read_bytes()
        self.pack = json.loads(self.raw)[0]

    @contextmanager
    def changed(self, name, raw):
        """Replace or remove a fixture file without changing the repository source."""
        path = self.repo / name
        link = path.readlink() if path.is_symlink() else None
        original = path.read_bytes() if link is None and path.is_file() else None
        path.unlink(missing_ok=True)
        path.parent.mkdir(parents=True, exist_ok=True)
        if raw is not None:
            path.write_bytes(raw)
        try:
            yield path
        finally:
            path.unlink(missing_ok=True)
            if link is not None:
                path.symlink_to(link)
            elif original is not None:
                path.write_bytes(original)

    def validate(self, pack=None, raw=None):
        return v._validate_v23_lobe_boundary_successor(
            self.assets, self.repo, self.baseline,
            self.pack if pack is None else pack, self.raw if raw is None else raw)

    def test_only_pack_identity_and_tags_hash_change(self):
        self.validate()
        previous = json.loads((self.assets / 'photo_regression_baseline_v22_pack.json').read_bytes())[0]
        reviewed = self.proof['reviewed_pack_delta']
        self.assertEqual({'pack_id', 'provenance/tags_hash'},
                         {row['path'] for row in reviewed['bindings']})
        self.assertEqual(2, len(reviewed['bindings']))
        self.assertEqual([], reviewed['optional_blocks'])
        self.assertIs(True, reviewed['all_other_pack_fields_exactly_equal'])
        self.assertIs(True, reviewed['slot_candidates_and_order_unchanged'])
        self.assertEqual(64, v._public_photo_candidate_count(self.pack))
        self.assertEqual(previous['slots'], self.pack['slots'])
        for name in ('authorial_core', 'creative_controls', 'authorial_composition',
                     'negative_en', 'core_retrieval', 'semantic_clarification',
                     'visual_concept_candidates'):
            self.assertEqual(previous[name], self.pack[name], name)
        old_remaining, new_remaining = copy.deepcopy(previous), copy.deepcopy(self.pack)
        for pack in (old_remaining, new_remaining):
            del pack['pack_id']
            del pack['provenance']['tags_hash']
        self.assertEqual(old_remaining, new_remaining)
        self.assertEqual(20, len(self.proof['exact_data_paths']))
        self.assertEqual(20, len(set(self.proof['exact_data_paths'])))
        self.assertEqual(set(self.proof['exact_data_paths']),
                         {row['path'] for row in self.proof['reviewed_source_deltas']}
                         | set(self.proof['active_semantic_shards']))
        self.assertEqual(4, len(self.proof['reviewed_source_deltas']))

    def test_current_default_and_explicit_v23_are_registered(self):
        def frozen_command(command, **kwargs):
            Path(command[command.index('--output-file') + 1]).write_bytes(self.raw)
            return subprocess.CompletedProcess(command, 0, '', '')

        with mock.patch.object(v.subprocess, 'run', side_effect=frozen_command):
            for version in (None, 23):
                with self.subTest(version=version):
                    result = v.validate_photo_regression_baseline(
                        ILLUSTRATION / 'assets', baseline_version=version)
                    self.assertEqual('photo_regression_baseline/v23', result['schema'])
                    self.assertEqual(self.proof['current_pack_sha256'], result['sha256'])
        with self.assertRaisesRegex(v.ValidationFailure, 'unsupported photo baseline version'):
            v.validate_photo_regression_baseline(self.assets, baseline_version=24)

    def test_rehashed_candidate_order_core_owner_control_negative_and_privacy_changes_rejected(self):
        name = str((ILLUSTRATION / 'assets/photo_regression_baseline_v23_pack.json').relative_to(ROOT))
        for kind in ('candidate', 'order', 'candidate_count', 'core', 'owner', 'controls',
                     'composition', 'negative', 'privacy', 'private_field', 'tags_hash'):
            self.baseline = copy.deepcopy(self.original_baseline)
            changed = copy.deepcopy(self.pack)
            slot = next(slot for slot in changed['slots'].values() if len(slot['candidates']) >= 2)
            if kind == 'candidate':
                slot['candidates'][0]['concept_terms'][0] += ' altered'
            elif kind == 'order':
                slot['candidates'].reverse()
            elif kind == 'candidate_count':
                slot['candidate_count'] += 1
            elif kind == 'core':
                changed['authorial_core']['subject'] += ' altered'
            elif kind == 'owner':
                changed['core_retrieval']['slot_ownership_sha256'] = '0' * 64
            elif kind == 'controls':
                changed['creative_controls']['extra'] = True
            elif kind == 'composition':
                changed['authorial_composition']['policy']['agent_is_final_author'] = False
            elif kind == 'negative':
                changed['negative_en'] += ', altered'
            elif kind == 'privacy':
                changed['provenance']['private_routing_exposed'] = True
            elif kind == 'private_field':
                changed['provenance']['argv'] = ['private-routing-value']
            else:
                changed['provenance']['tags_hash'] = '0' * 64
            changed['pack_id'] = v._canonical_photo_pack_id(changed)
            raw = encoded([changed])
            self.baseline.update(sha256=digest(raw), pack_id=changed['pack_id'])
            with self.subTest(kind=kind), self.changed(name, raw), self.assertRaises(v.ValidationFailure):
                self.validate(changed, raw)

    def test_rehashed_optional_contract_content_inventory_and_order_changes_rejected(self):
        name = str((ILLUSTRATION / 'assets/photo_regression_baseline_v23_pack.json').relative_to(ROOT))
        for block in ('semantic_clarification', 'visual_concept_candidates'):
            for kind in ('content', 'identity', 'order', 'added', 'removed'):
                self.baseline = copy.deepcopy(self.original_baseline)
                changed = copy.deepcopy(self.pack)
                rows = changed[block]['candidates']
                if kind == 'content':
                    if block == 'semantic_clarification':
                        rows[0]['interpreted_meaning'] += ' altered'
                    else:
                        rows[0]['concept_terms'][0] += ' altered'
                elif kind == 'identity':
                    rows[0]['id'] += '-altered'
                elif kind == 'order':
                    rows.reverse()
                elif kind == 'added':
                    rows.append(dict(rows[0], id=rows[0]['id'] + '-added'))
                else:
                    rows.pop()
                changed['pack_id'] = v._canonical_photo_pack_id(changed)
                raw = encoded([changed])
                self.baseline.update(sha256=digest(raw), pack_id=changed['pack_id'])
                with self.subTest(block=block, kind=kind), self.changed(name, raw), self.assertRaises(v.ValidationFailure):
                    self.validate(changed, raw)

    def test_supplied_pack_and_raw_must_match_the_sealed_file(self):
        changed = copy.deepcopy(self.pack)
        changed['provenance']['private_routing_exposed'] = True
        changed['pack_id'] = v._canonical_photo_pack_id(changed)
        with self.assertRaises(v.ValidationFailure):
            self.validate(pack=changed)
        with self.assertRaises(v.ValidationFailure):
            self.validate(raw=self.raw + b'\n')

    def test_fixed_proof_rejects_coordinated_rehash(self):
        mutations = (
            ('source_commit', '0' * 40), ('source_tree', '0' * 40),
            ('reviewed_source_deltas', []), ('reviewed_source_leaf_deltas', []),
            ('reviewed_pack_delta', {}), ('source_inventory_after', {}),
            ('source_files', {}), ('active_semantic_shards', {}),
            ('active_visual_shards', {}), ('retained_semantic_shards', {}),
            ('retained_visual_shards', {}),
            ('source_parent_files', {}), ('historical_dependencies', {}),
            ('immutable_history', {}), ('exact_data_paths', []),
            ('qualification_sha256', '0' * 64), ('previous_validator_sha256', '0' * 64),
            ('previous_pack_sha256', '0' * 64), ('current_pack_sha256', '0' * 64),
        )
        for field, value in mutations:
            self.baseline = copy.deepcopy(self.original_baseline)
            changed = copy.deepcopy(self.proof)
            changed[field] = value
            raw = encoded(changed)
            self.baseline['lobe_boundary_transition']['evidence_sha256'] = digest(raw)
            if field in self.baseline['lobe_boundary_transition']:
                self.baseline['lobe_boundary_transition'][field] = value
            with self.subTest(field=field), self.changed(PROOF, raw), self.assertRaises(v.ValidationFailure):
                self.validate()

    def test_reviewed_data_and_runtime_bytes_and_unregistered_data_rejected(self):
        names = self.proof['exact_data_paths'] + [
            'skills/photo-prompt-image-generator/scripts/prompt_generator.py',
            'skills/photo-prompt-image-generator/scripts/visual_profile_index_storage.py',
        ]
        for name in names:
            with self.subTest(path=name), self.changed(name, (ROOT / name).read_bytes() + b'\n'), self.assertRaises(v.ValidationFailure):
                self.validate()
        with self.changed('skills/photo-prompt-image-generator/assets/unexpected.json', b'{}'), self.assertRaises(v.ValidationFailure):
            self.validate()

    def test_source_and_proof_cannot_be_rebaselined_together(self):
        name = self.proof['reviewed_source_deltas'][0]['path']
        source_raw = (ROOT / name).read_bytes() + b'\n'
        changed = copy.deepcopy(self.proof)
        changed['source_files'][name] = digest(source_raw)
        changed['source_inventory_after'][Path(name).name] = digest(source_raw)
        for row in changed['reviewed_source_deltas']:
            if row['path'] == name:
                row['current'] = digest(source_raw)
        proof_raw = encoded(changed)
        self.baseline['lobe_boundary_transition']['source_files'] = changed['source_files']
        self.baseline['lobe_boundary_transition']['evidence_sha256'] = digest(proof_raw)
        with self.changed(name, source_raw), self.changed(PROOF, proof_raw), self.assertRaises(v.ValidationFailure):
            self.validate()

    def test_active_and_retained_shard_mutation_removal_and_addition_rejected(self):
        for field in ('active_semantic_shards', 'active_visual_shards',
                      'retained_semantic_shards', 'retained_visual_shards'):
            name = next(iter(self.proof[field]))
            for kind, path, raw in (
                ('mutated', name, (ROOT / name).read_bytes() + b' '),
                ('missing', name, None),
                ('extra', str(Path(name).parent / 'shard-999.json'), b'{}'),
            ):
                failure = (FileNotFoundError, v.ValidationFailure) if kind == 'missing' else v.ValidationFailure
                with self.subTest(field=field, kind=kind), self.changed(path, raw), self.assertRaises(failure):
                    self.validate()

    def test_parent_history_qualification_and_source_archive_are_immutable(self):
        names = (self.proof['source_parent_manifest'], self.proof['previous_proof_path'],
                 self.proof['universal_v2_before_path'], self.proof['qualification_path'],
                 next(iter(self.proof['source_parent_files'])),
                 next(iter(self.proof['historical_dependencies'])),
                 next(iter(self.qualification['files'])),
                 'skills/subculture-illustration-image-generator/assets/photo_regression_baseline_v22.json',
                 'skills/subculture-illustration-image-generator/assets/photo_regression_baseline_v22_pack.json')
        for name in names:
            with self.subTest(path=name), self.changed(name, (ROOT / name).read_bytes() + b'\n'), self.assertRaises(v.ValidationFailure):
                self.validate()

    def test_transition_provenance_and_predecessor_relabeling_rejected(self):
        for field in ('source_commit', 'evidence_sha256'):
            self.baseline = copy.deepcopy(self.original_baseline)
            self.baseline['lobe_boundary_transition'][field] = 'PENDING'
            with self.subTest(field=field), self.assertRaises(v.ValidationFailure):
                self.validate()
        for field in ('ornament_data_transition', 'visual_index_storage_transition',
                      'zero_pack_delta_transition', 'metadata_only_transition'):
            self.baseline = copy.deepcopy(self.original_baseline)
            self.baseline[field] = {}
            with self.subTest(field=field), self.assertRaises(v.ValidationFailure):
                self.validate()

    def test_universal_descriptor_changes_only_the_validator_hash(self):
        name = str((ILLUSTRATION / 'assets/universal_scene_baseline_v2.json').relative_to(ROOT))
        before = (ROOT / self.proof['universal_v2_before_path']).read_bytes()
        previous_sha = self.proof['previous_validator_sha256'].encode('ascii')
        current_sha = digest(Path(v.__file__).read_bytes()).encode('ascii')
        self.assertEqual(1, before.count(previous_sha))
        self.assertEqual(before.replace(previous_sha, current_sha, 1), (ROOT / name).read_bytes())
        for kind, raw in (('old_validator', before),
                          ('other_bytes', (ROOT / name).read_bytes() + b'\n')):
            with self.subTest(kind=kind), self.changed(name, raw), self.assertRaises(v.ValidationFailure):
                self.validate()

    def test_v22_still_rejects_current_lobe_data(self):
        baseline = json.loads((self.assets / 'photo_regression_baseline_v22.json').read_bytes())
        raw = (self.assets / 'photo_regression_baseline_v22_pack.json').read_bytes()
        with self.assertRaises(v.ValidationFailure):
            v._validate_v22_ornament_data_successor(
                self.assets, ROOT, baseline, json.loads(raw)[0], raw)


if __name__ == '__main__':
    unittest.main()
