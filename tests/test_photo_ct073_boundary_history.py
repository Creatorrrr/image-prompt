"""V25 seals CT073 owner consistency and exactly four observed pack bindings."""
import copy
import ast
from contextlib import contextmanager, ExitStack
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from tests import photo_prompt_fixtures as fixtures

ROOT = Path(__file__).resolve().parents[1]
ILLUSTRATION = ROOT / 'skills/subculture-illustration-image-generator'
EVIDENCE = Path('docs/research-evidence/photo-prompt/ct073-back-band-maintenance-integration-20261006')
PROOF = EVIDENCE / 'V25-CT073-BINDING-PROOF.json'
sys.path.insert(0, str(ILLUSTRATION / 'scripts'))
import validate_illustration_assets as v


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


class CT073BoundaryHistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        original = {name: globals()[name] for name in ('ROOT', 'ILLUSTRATION', 'v')}
        frozen = tempfile.TemporaryDirectory(prefix='sealed-v25-ct073-')
        cls.addClassCleanup(frozen.cleanup)
        root = Path(frozen.name).resolve()
        archived = fixtures.archived_v25_validator(root, source_root=ROOT)
        cls.addClassCleanup(lambda: globals().update(original))
        globals().update(ROOT=root, ILLUSTRATION=root / 'skills/subculture-illustration-image-generator',
                         v=archived)
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
                      'retained_semantic_shards', 'retained_visual_shards', 'retained_shard_files'):
            paths.update(self.proof[field])
        paths.update(self.qualification['files'])
        paths.update(self.proof['exact_data_paths'])
        paths.add(self.proof['textile_maintenance_path'])
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
        self.baseline = json.loads((self.assets / 'photo_regression_baseline_v25.json').read_bytes())
        self.original_baseline = copy.deepcopy(self.baseline)
        self.raw = (self.assets / 'photo_regression_baseline_v25_pack.json').read_bytes()
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
        return v._validate_v25_ct073_back_band_successor(
            self.assets, self.repo, self.baseline,
            self.pack if pack is None else pack, self.raw if raw is None else raw)

    def test_only_four_reviewed_pack_bindings_change(self):
        self.validate()
        previous = json.loads((self.assets / 'photo_regression_baseline_v24_pack.json').read_bytes())[0]
        reviewed = self.proof['reviewed_pack_delta']
        self.assertEqual({'pack_id', 'provenance/tags_hash', 'core_retrieval/canonical_sha256', 'core_retrieval/slot_corpus_sha256'},
                         {row['path'] for row in reviewed['bindings']})
        self.assertEqual(4, len(reviewed['bindings']))
        self.assertEqual([], reviewed['optional_blocks'])
        self.assertIs(True, reviewed['all_other_pack_fields_exactly_equal'])
        self.assertIs(True, reviewed['slot_candidates_and_order_unchanged'])
        self.assertEqual(64, v._public_photo_candidate_count(self.pack))
        self.assertEqual(previous['slots'], self.pack['slots'])
        for name in ('authorial_core', 'creative_controls', 'authorial_composition',
                     'negative_en', 'semantic_clarification',
                     'visual_concept_candidates'):
            self.assertEqual(previous[name], self.pack[name], name)
        old_remaining, new_remaining = copy.deepcopy(previous), copy.deepcopy(self.pack)
        for pack in (old_remaining, new_remaining):
            del pack['pack_id']
            del pack['provenance']['tags_hash']
            del pack['core_retrieval']['canonical_sha256']
            del pack['core_retrieval']['slot_corpus_sha256']
        self.assertEqual(old_remaining, new_remaining)
        self.assertEqual(23, len(self.proof['exact_data_paths']))
        self.assertEqual(23, len(set(self.proof['exact_data_paths'])))
        self.assertEqual(set(self.proof['exact_data_paths']),
                         {row['path'] for row in self.proof['reviewed_source_deltas']}
                         | set(self.proof['active_semantic_shards'])
                         | (set(self.proof['active_visual_shards']) - set(self.proof['retained_visual_shards']))
                         | {self.proof['maintenance_path']})
        self.assertEqual(5, len(self.proof['reviewed_source_deltas']))

    def test_original_default_and_explicit_v25_are_registered(self):
        def frozen_command(command, **kwargs):
            Path(command[command.index('--output-file') + 1]).write_bytes(self.raw)
            return subprocess.CompletedProcess(command, 0, '', '')

        with mock.patch.object(v.subprocess, 'run', side_effect=frozen_command):
            for version in (None, 25):
                with self.subTest(version=version):
                    result = v.validate_photo_regression_baseline(
                        ILLUSTRATION / 'assets', baseline_version=version)
                    self.assertEqual('photo_regression_baseline/v25', result['schema'])
                    self.assertEqual(self.proof['current_pack_sha256'], result['sha256'])
        with self.assertRaisesRegex(v.ValidationFailure, 'unsupported photo baseline version'):
            v.validate_photo_regression_baseline(self.assets, baseline_version=26)

    def test_rehashed_candidate_order_core_owner_control_negative_and_privacy_changes_rejected(self):
        name = str((ILLUSTRATION / 'assets/photo_regression_baseline_v25_pack.json').relative_to(ROOT))
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
        name = str((ILLUSTRATION / 'assets/photo_regression_baseline_v25_pack.json').relative_to(ROOT))
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
            ('retained_visual_shards', {}), ('qualified_parent_tree', '0' * 40), ('qualified_parent_parents', []), ('retained_shard_git_bindings', {}), ('retained_shard_files', {}),
            ('source_parents', []), ('exact_data_diff', []), ('receipt_bindings', {}),
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
            self.baseline['ct073_back_band_transition']['evidence_sha256'] = digest(raw)
            if field in self.baseline['ct073_back_band_transition']:
                self.baseline['ct073_back_band_transition'][field] = value
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
        self.baseline['ct073_back_band_transition']['source_files'] = changed['source_files']
        self.baseline['ct073_back_band_transition']['evidence_sha256'] = digest(proof_raw)
        with self.changed(name, source_raw), self.changed(PROOF, proof_raw), self.assertRaises(v.ValidationFailure):
            self.validate()
        # Updating both source and generated-index claims still cannot replace the
        # code-pinned proof, even when the caller coordinates every local hash.
        index_name = 'skills/photo-prompt-image-generator/assets/photo_prompt_semantic_index.json'
        index = json.loads((ROOT / index_name).read_bytes())
        index['dictionary_hash'] = '0' * 64
        index_raw = encoded(index)
        changed['source_files'][index_name] = digest(index_raw)
        changed['source_inventory_after'][Path(index_name).name] = digest(index_raw)
        changed['exact_data_files'][name] = digest(source_raw)
        changed['exact_data_files'][index_name] = digest(index_raw)
        changed['source_index']['ordinary']['full_manifest_sha256'] = digest(index_raw)
        for row in changed['reviewed_source_deltas']:
            if row['path'] == index_name:
                row['current'] = digest(index_raw)
        proof_raw = encoded(changed)
        self.baseline['ct073_back_band_transition']['source_files'] = changed['source_files']
        self.baseline['ct073_back_band_transition']['evidence_sha256'] = digest(proof_raw)
        with self.changed(name, source_raw), self.changed(index_name, index_raw), \
                self.changed(PROOF, proof_raw), self.assertRaises(v.ValidationFailure):
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
                 'skills/subculture-illustration-image-generator/assets/photo_regression_baseline_v24.json',
                 'skills/subculture-illustration-image-generator/assets/photo_regression_baseline_v24_pack.json')
        for name in names:
            with self.subTest(path=name), self.changed(name, (ROOT / name).read_bytes() + b'\n'), self.assertRaises(v.ValidationFailure):
                self.validate()

    def test_transition_provenance_and_predecessor_relabeling_rejected(self):
        for field in ('source_commit', 'evidence_sha256'):
            self.baseline = copy.deepcopy(self.original_baseline)
            self.baseline['ct073_back_band_transition'][field] = 'PENDING'
            with self.subTest(field=field), self.assertRaises(v.ValidationFailure):
                self.validate()
        for field in ('structure_source_transition', 'lobe_boundary_transition', 'ornament_data_transition', 'visual_index_storage_transition',
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

    def test_original_v24_rejects_current_ct073_data_at_its_data_check(self):
        baseline = json.loads((self.assets / 'photo_regression_baseline_v24.json').read_bytes())
        raw = (self.assets / 'photo_regression_baseline_v24_pack.json').read_bytes()
        with self.assertRaisesRegex(v.ValidationFailure, 'photo V24 authored source or runtime binding drift'):
            v._validate_v24_structure_source_successor(
                self.assets, ROOT, baseline, json.loads(raw)[0], raw)

    def test_all_previous_validator_helpers_and_history_bytes_are_preserved(self):
        original_path = Path(self.proof['universal_v2_before_path']).parents[1] / 'scripts/validate_illustration_assets.py'
        original = (ROOT / original_path).read_text()
        current = Path(v.__file__).read_text()
        original_functions = {node.name: ast.get_source_segment(original, node)
                              for node in ast.parse(original).body
                              if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
        current_functions = {node.name: ast.get_source_segment(current, node)
                             for node in ast.parse(current).body
                             if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
        for name, body in original_functions.items():
            if name != 'validate_photo_regression_baseline':
                self.assertEqual(body, current_functions[name], name)
        self.assertEqual({'_validate_v25_ct073_back_band_successor'},
                         set(current_functions) - set(original_functions))
        historical = {name: sha for name, sha in self.proof['immutable_history'].items()
                      if Path(name).name.startswith('photo_regression_baseline_v')}
        self.assertEqual(41, len(historical))
        for name, sha in historical.items():
            self.assertEqual(sha, digest((ROOT / name).read_bytes()), name)

    def test_frozen_lineage_inputs_command_and_public_contract_cannot_be_changed(self):
        name = str((ILLUSTRATION / 'assets/photo_regression_baseline_v25.json').relative_to(ROOT))
        for kind in ('lineage', 'seed', 'input_path', 'input_hash', 'contract', 'preserved_contract'):
            changed = copy.deepcopy(self.original_baseline)
            if kind == 'lineage':
                changed['historical_baseline']['sha256'] = '0' * 64
            elif kind == 'seed':
                changed['command'][changed['command'].index('--seed') + 1] = '910001'
            elif kind == 'input_path':
                changed['command'][changed['command'].index('--authorial-core-json') + 1] += '.changed'
            elif kind == 'input_hash':
                changed['frozen_inputs'][next(iter(changed['frozen_inputs']))] = '0' * 64
            elif kind == 'contract':
                changed['contract_version'] = 'photo-candidate-pack/v7'
            else:
                changed['preserved_contract_sha256'] = '0' * 64
            with self.subTest(kind=kind), self.changed(name, encoded(changed)), \
                    mock.patch.object(v.subprocess, 'run', side_effect=AssertionError('must reject before CLI')), \
                    self.assertRaises(v.ValidationFailure):
                v.validate_photo_regression_baseline(self.assets, baseline_version=25)

    def test_each_reviewed_authored_and_maintenance_leaf_is_sealed(self):
        self.assertEqual(12, len(self.proof['reviewed_source_leaf_deltas']))
        for row in self.proof['reviewed_source_leaf_deltas']:
            value = json.loads((ROOT / row['file']).read_bytes())
            parts = row['pointer'].strip('/').split('/')
            target = value
            for part in parts[:-1]:
                target = target[int(part)] if isinstance(target, list) else target[part]
            key = int(parts[-1]) if isinstance(target, list) else parts[-1]
            self.assertEqual(row['after'], target[key])
            target[key] = row['before']
            with self.subTest(pointer=row['pointer']), self.changed(row['file'], encoded(value)), \
                    self.assertRaises(v.ValidationFailure):
                self.validate()

    def test_siblings_aliases_activation_eligibility_components_and_native_gates_are_sealed(self):
        ordinary = 'skills/photo-prompt-image-generator/assets/photo_prompt_clothing_structure_extension.json'
        visual = 'skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_clothing_structure.json'
        for name, pointer in (
            (ordinary, ('slots', 'garment_detail', 88, 'en')),
            (ordinary, ('slots', 'garment_detail', 89, 'aliases')),
            (ordinary, ('slots', 'garment_detail', 89, 'relations')),
            (visual, ('profiles', 143, 'semantics')),
            (visual, ('profiles', 144, 'activation')),
            (visual, ('profiles', 144, 'authored_components')),
            (visual, ('profiles', 144, 'runtime_expression')),
            (visual, ('profiles', 144, 'concept_candidate')),
        ):
            value = json.loads((ROOT / name).read_bytes())
            target = value
            for key in pointer[:-1]:
                target = target[key]
            target[pointer[-1]] = None
            with self.subTest(pointer=pointer), self.changed(name, encoded(value)), \
                    self.assertRaises(v.ValidationFailure):
                self.validate()

    def test_index_metadata_bm25f_exact_lookup_and_vectors_cannot_be_rehashed(self):
        source_assets = 'skills/photo-prompt-image-generator/assets/'
        for basename in ('photo_prompt_semantic_index.json', 'photo_prompt_visual_profile_index.json'):
            name = source_assets + basename
            original = json.loads((ROOT / name).read_bytes())
            for key in original:
                changed = copy.deepcopy(original)
                changed[key] = None
                with self.subTest(index=basename, field=key), self.changed(name, encoded(changed)), \
                        self.assertRaises(v.ValidationFailure):
                    self.validate()
        old_proof = json.loads((ROOT / self.proof['previous_proof_path']).read_bytes())
        for field, key, bucket in (
            ('active_semantic_shards', 'slot:garment_detail:clt_ct073_v2', 'shard-000'),
            ('active_visual_shards', 'clothing_ct073_v2', 'shard-012'),
        ):
            name = next(name for name in self.proof[field] if Path(name).name.startswith(bucket))
            old_name = next(name for name in old_proof[field] if Path(name).name.startswith(bucket))
            original = json.loads((ROOT / name).read_bytes())
            prior = json.loads((ROOT / old_name).read_bytes())
            for kind in ('wrong_vector', 'old_vector', 'reused_vector', 'wrong_text', 'text_hash', 'dimension', 'bm25f'):
                changed = copy.deepcopy(original)
                row = changed['entries'][key]
                if kind == 'wrong_vector':
                    row['vector'][0] += 0.01
                elif kind == 'old_vector':
                    self.assertNotEqual(row['vector'], prior['entries'][key]['vector'])
                    row['vector'] = prior['entries'][key]['vector']
                elif kind == 'reused_vector':
                    unrelated = next(entry for entry in changed['entries'] if entry != key)
                    changed['entries'][unrelated]['vector'][0] += 0.01
                elif kind == 'wrong_text':
                    row['text'] += ' altered'
                elif kind == 'text_hash':
                    row['text_sha256'] = '0' * 64
                elif kind == 'dimension':
                    row['vector'].pop()
                else:
                    row['bm25f_document'] = {}
                with self.subTest(field=field, kind=kind), self.changed(name, encoded(changed)), \
                        self.assertRaises(v.ValidationFailure):
                    self.validate()

    def test_bound_older_generation_and_unregistered_generation_are_rejected(self):
        bound = next(iter(self.proof['retained_shard_files']))
        for raw in ((ROOT / bound).read_bytes() + b' ', None):
            with self.changed(bound, raw), self.assertRaises((FileNotFoundError, v.ValidationFailure)):
                self.validate()
        name = 'skills/photo-prompt-image-generator/assets/photo_prompt_semantic_index_shards/unregistered/shard-000.json'
        with self.changed(name, b'{}'), self.assertRaises(v.ValidationFailure):
            self.validate()

    def test_textile_reference_record_and_authored_scope_are_sealed(self):
        name = 'skills/photo-prompt-image-generator/assets/photo_prompt_textile_surface_extension.json'
        original = json.loads((ROOT / name).read_bytes())
        self.assertEqual('7047c44cb9013a58102835f529f44a570b61bd7d4f4851b89e86d3d48005ef5a',
                         digest((ROOT / name).read_bytes()))
        record_name = self.proof['textile_maintenance_path']
        self.assertEqual('7d8933f1db6a61eaea1aa79bc01f8063ef2c64b6c4b7bd496bb71552fb9d465a',
                         digest((ROOT / record_name).read_bytes()))
        for kind in ('wrong_record', 'raw_instead_of_canonical_hash', 'extra_reference_key', 'remove_opacity', 'authored_text'):
            changed = copy.deepcopy(original)
            if kind == 'wrong_record':
                changed['maintenance_ref']['record_id'] = 'photo_prompt_textile_surface_extension-vocaloid-equivalents-20261004'
            elif kind == 'raw_instead_of_canonical_hash':
                changed['maintenance_ref']['sha256'] = digest((ROOT / record_name).read_bytes())
            elif kind == 'extra_reference_key':
                changed['maintenance_ref']['unreviewed'] = True
            elif kind == 'remove_opacity':
                changed['slots']['surface_material'][24]['affected_properties'].pop()
            else:
                changed['slots']['surface_material'][24]['en'] += ' changed'
            with self.subTest(kind=kind), self.changed(name, encoded(changed)), self.assertRaises(v.ValidationFailure):
                self.validate()
        with self.changed(record_name, (ROOT / record_name).read_bytes() + b'\n'), self.assertRaises(v.ValidationFailure):
            self.validate()


if __name__ == '__main__':
    unittest.main()
