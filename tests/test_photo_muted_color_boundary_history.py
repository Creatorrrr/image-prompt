"""V28 changes three source negatives and only two frozen-pack hash leaves."""
from contextlib import contextmanager
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
ASSETS = ILLUSTRATION / 'assets'
PHOTO = Path('skills/photo-prompt-image-generator/assets')
EVIDENCE = Path('docs/research-evidence/photo-prompt/muted-color-contrast-20261006')
sys.path.insert(0, str(ROOT / ILLUSTRATION / 'scripts'))
import validate_illustration_assets as validator


def load(path):
    return json.loads(path.read_bytes())


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


class MutedColorBoundaryHistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        temporary = tempfile.TemporaryDirectory(prefix='sealed-v28-color-')
        cls.addClassCleanup(temporary.cleanup)
        cls.source_root = Path(temporary.name).resolve() / 'tree'
        cls.validator = fixtures.archived_v28_validator(cls.source_root)
        interpreter = cls.source_root / '.venv/bin/python'
        interpreter.parent.mkdir(parents=True)
        interpreter.symlink_to(Path(sys.executable).resolve())
        cls.proof = load(cls.source_root / EVIDENCE / 'V28-MUTED-COLOR-PROOF.json')
        cls.parent = load(cls.source_root / EVIDENCE / 'V27-PARENT-SOURCE.json')
        cls.baseline = load(cls.source_root / ASSETS / 'photo_regression_baseline_v28.json')
        cls.raw = (cls.source_root / ASSETS / 'photo_regression_baseline_v28_pack.json').read_bytes()
        cls.pack = json.loads(cls.raw)[0]

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='.v28-muted-color-boundary-', dir=self.source_root)
        self.addCleanup(temporary.cleanup)
        self.repo = Path(temporary.name)
        self.assets = self.repo / ASSETS
        paths = {r['source_path'] for r in self.parent['members']}
        paths.update(self.proof['source_files_after'])
        paths.update(self.proof['active_shards_after'])
        paths.update(str(p.relative_to(self.source_root)) for p in (self.source_root / PHOTO).glob('*.json'))
        paths.update(str(p.relative_to(self.source_root)) for p in (self.source_root / ASSETS).glob('photo_regression_baseline_v*.json'))
        paths.update(str(EVIDENCE / name) for name in (
            'V28-MUTED-COLOR-PROOF.json', 'V27-PARENT-SOURCE.json', 'SOURCE-QUALITY-EVIDENCE.json'))
        paths.update({self.proof['previous_maintenance_record'], str(ASSETS / 'universal_scene_baseline_v2.json')})
        for name in sorted(paths):
            target = self.repo / name
            target.parent.mkdir(parents=True, exist_ok=True)
            os.link(self.source_root / name, target)

    def validate(self, pack=None, raw=None):
        self.validator._validate_v28_muted_color_successor(
            self.assets, self.repo, self.baseline,
            self.pack if pack is None else pack, self.raw if raw is None else raw)

    @contextmanager
    def changed(self, name, raw):
        path = self.repo / name
        path.unlink()
        if raw is not None:
            path.write_bytes(raw)
        try:
            yield path
        finally:
            path.unlink(missing_ok=True)
            os.link(self.source_root / name, path)

    def test_archived_command_reproduces_v28(self):
        result = self.validator.validate_photo_regression_baseline(self.source_root / ASSETS)
        self.assertEqual(result['schema'], 'photo_regression_baseline/v28')
        self.assertEqual(result['sha256'], self.proof['current_pack_sha256'])
        self.assertEqual(result['pack_id'], '86418117c79c90b5')

    def test_archived_default_and_explicit_28_keep_strict_version_boundary(self):
        def frozen(command, **kwargs):
            Path(command[command.index('--output-file') + 1]).write_bytes(self.raw)
            return subprocess.CompletedProcess(command, 0, '', '')
        with mock.patch.object(self.validator.subprocess, 'run', side_effect=frozen):
            for version in (None, 28):
                result = self.validator.validate_photo_regression_baseline(self.source_root / ASSETS, baseline_version=version)
                self.assertEqual(result['schema'], 'photo_regression_baseline/v28')
        with self.assertRaisesRegex(self.validator.ValidationFailure, 'unsupported photo baseline version'):
            self.validator.validate_photo_regression_baseline(self.assets, baseline_version=29)

    def test_only_two_hash_leaves_change_and_all_64_candidates_remain_exact(self):
        before = load(self.source_root / ASSETS / 'photo_regression_baseline_v27_pack.json')[0]
        expected = copy.deepcopy(before)
        expected['provenance']['tags_hash'] = self.proof['current_dictionary_hash']
        expected['pack_id'] = self.validator._canonical_photo_pack_id(expected)
        self.assertEqual(expected, self.pack)
        self.assertEqual(64, self.validator._public_photo_candidate_count(self.pack))
        self.assertEqual({'/0/pack_id', '/0/provenance/tags_hash'},
                         {r['pointer'] for r in self.proof['reviewed_pack_delta']})
        self.assertEqual(before['authorial_composition'], self.pack['authorial_composition'])

    def test_rehashed_candidate_order_meaning_scene_controls_negative_and_budget_fail(self):
        for key in ('candidate', 'order', 'core', 'controls', 'negative', 'budget', 'locks'):
            changed = copy.deepcopy(self.pack)
            candidates = next(r['candidates'] for r in changed['slots'].values() if len(r['candidates']) > 1)
            if key == 'candidate': candidates[0]['concept_terms'][0] += ' changed'
            if key == 'order': candidates.reverse()
            if key == 'core': changed['authorial_core']['subject'] += ' changed'
            if key == 'controls': changed['creative_controls']['extra'] = True
            if key == 'negative': changed['negative_en'] += ', changed'
            if key == 'budget': changed['authorial_composition']['prompt_budget']['absolute_maximum_words'] += 1
            if key == 'locks': changed['authorial_core']['intent_lock']['locked_dimensions'] = []
            changed['pack_id'] = self.validator._canonical_photo_pack_id(changed)
            with self.subTest(mutation=key), self.assertRaises(self.validator.ValidationFailure):
                self.validate(changed, encoded([changed]))

    def test_three_negatives_and_bookkeeping_are_the_entire_source_delta(self):
        records = {r['path']:r for r in self.parent['members']}
        total = 0
        for name, changes in self.proof['reviewed_source_deltas'].items():
            previous = load(self.source_root / records[name]['source_path'])
            expected = copy.deepcopy(previous)
            for change in changes:
                target = expected
                parts = change['pointer'].split('/')[1:]
                for part in parts[:-1]:
                    target = target[int(part)] if isinstance(target, list) else target[part]
                key = int(parts[-1]) if isinstance(target, list) else parts[-1]
                self.assertEqual(target[key], change['before'])
                target[key] = change['after']
                total += 1
            self.assertEqual(load(self.source_root / name), expected)
        self.assertEqual(total, 7)  # three negatives, two maintenance reference leaves, two index headers

    def test_original_v27_source_pin_still_rejects_live_data_successor(self):
        baseline = load(self.source_root / ASSETS / 'photo_regression_baseline_v27.json')
        raw = (self.source_root / ASSETS / 'photo_regression_baseline_v27_pack.json').read_bytes()
        with self.assertRaisesRegex(self.validator.ValidationFailure, 'photo V27 exact DATA inventory drift'):
            self.validator._validate_v27_appearance_data_successor(self.source_root / ASSETS, ROOT, baseline, json.loads(raw)[0], raw)

    def test_positive_negative_alias_maintenance_runtime_and_index_drift_fail(self):
        names = [PHOTO / 'photo_prompt_color_relations_extension.json',
                 PHOTO / 'photo_prompt_visual_obligations_color_relations.json',
                 PHOTO / 'photo_prompt_semantic_index.json', PHOTO / 'photo_prompt_visual_profile_index.json',
                 Path(self.proof['successor_maintenance_record']),
                 Path(self.proof['previous_maintenance_record']),
                 Path('skills/photo-prompt-image-generator/scripts/prompt_generator.py')]
        for name in names:
            with self.subTest(path=str(name)), self.changed(name, (self.source_root / name).read_bytes() + b'\n'):
                with self.assertRaises(self.validator.ValidationFailure):
                    self.validate()
        name = PHOTO / 'photo_prompt_visual_obligations_color_relations.json'
        for field in ('positive', 'negative', 'alias'):
            value = load(self.source_root / name)
            profile = value['profiles'][16]
            if field == 'positive': profile['authored_components']['unexpected'] = 'changed'
            if field == 'negative': profile['reject_substitutes'][0] += ' changed'
            if field == 'alias': profile['aliases'] = ['changed']
            with self.subTest(field=field), self.changed(name, encoded(value)):
                with self.assertRaises(self.validator.ValidationFailure): self.validate()

    def test_index_order_shard_references_and_stored_vector_bytes_fail(self):
        name = PHOTO / 'photo_prompt_semantic_index.json'
        for field in ('entry_order', 'shards'):
            value = load(self.source_root / name)
            value[field].reverse()
            with self.subTest(field=field), self.changed(name, encoded(value)):
                with self.assertRaises(self.validator.ValidationFailure): self.validate()
        name = next(iter(self.proof['active_shards_after']))
        with self.changed(name, (self.source_root / name).read_bytes() + b'\n'):
            with self.assertRaisesRegex(self.validator.ValidationFailure, 'vectors or shard references drift'):
                self.validate()

    def test_rehashed_or_missing_evidence_manifest_and_previous_baseline_fail(self):
        names = [EVIDENCE / 'V28-MUTED-COLOR-PROOF.json', EVIDENCE / 'V27-PARENT-SOURCE.json',
                 EVIDENCE / 'SOURCE-QUALITY-EVIDENCE.json', ASSETS / 'photo_regression_baseline_v27.json',
                 Path(self.proof['previous_proof_path'])]
        for name in names:
            for raw in ((self.source_root / name).read_bytes() + b'\n', None):
                with self.subTest(path=str(name), missing=raw is None), self.changed(name, raw):
                    with self.assertRaises((self.validator.ValidationFailure, FileNotFoundError)): self.validate()

    def test_archive_bytes_modes_missing_symlinks_and_traversal_fail(self):
        row = next(r for r in self.parent['members'] if r['path'] == str(PHOTO / 'photo_prompt_color_relations_extension.json'))
        source = row['source_path']
        for raw in ((self.source_root / source).read_bytes() + b'\n', None):
            with self.changed(source, raw):
                with self.assertRaises(self.validator.ValidationFailure):
                    self.validator._photo_v28_archived_payload(self.repo, row)
        with self.changed(source, None) as path:
            path.symlink_to(self.source_root / source)
            with self.assertRaisesRegex(self.validator.ValidationFailure, 'unsafe historical source'):
                self.validator._photo_v28_archived_payload(self.repo, row)
        with self.changed(source, (self.source_root / source).read_bytes()) as path:
            path.chmod(0o755)
            with self.assertRaises(self.validator.ValidationFailure):
                self.validator._photo_v28_archived_payload(self.repo, row)
        for path in ('../outside', '/tmp/outside'):
            with self.assertRaisesRegex(self.validator.ValidationFailure, 'unsafe historical source path'):
                self.validator._photo_v28_archived_payload(self.repo, dict(row, source_path=path))

    def test_sealed_manifest_and_evidence_symlink_aliases_fail(self):
        for name in ('V27-PARENT-SOURCE.json', 'V28-MUTED-COLOR-PROOF.json', 'SOURCE-QUALITY-EVIDENCE.json'):
            relative = EVIDENCE / name
            with self.subTest(path=name), self.changed(relative, None) as path:
                path.symlink_to(self.source_root / relative)
                with self.assertRaisesRegex(self.validator.ValidationFailure, 'unsafe historical source'):
                    self.validate()

    def test_universal_descriptor_changes_only_validator_hash(self):
        name = ASSETS / 'universal_scene_baseline_v2.json'
        row = next(r for r in self.parent['members'] if r['path'] == str(name))
        previous = (self.source_root / row['source_path']).read_bytes()
        current_sha = hashlib.sha256(Path(self.validator.__file__).read_bytes()).hexdigest().encode()
        self.assertEqual((self.source_root / name).read_bytes(),
                         previous.replace(self.proof['previous_validator_sha256'].encode(), current_sha, 1))


if __name__ == '__main__':
    unittest.main()
