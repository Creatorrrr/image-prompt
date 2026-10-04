"""A metadata successor cannot conceal a changed candidate or scene contract."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tarfile
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/subculture-illustration-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
import validate_illustration_assets as validator


class NapeMetadataBoundaryHistoryTests(unittest.TestCase):
    version = 10

    def setUp(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.assets = Path(temp.name)
        for path in (SKILL / 'assets').glob('photo_regression_baseline_v*.json'):
            shutil.copyfile(path, self.assets / path.name)
        shutil.copyfile(SKILL / 'assets/universal_scene_baseline_v1.json',
                        self.assets / 'universal_scene_baseline_v1.json')
        self.path = self.assets / f'photo_regression_baseline_v{self.version}.json'
        self.baseline = json.loads(self.path.read_bytes())
        if self.version == 10:
            archive = ROOT / 'docs/research-evidence/photo-prompt/camera-evidence-structure-20261003/independent-v9-boundary-diagnostics.tar.gz'
            with tarfile.open(archive) as saved:
                self.output = saved.extractfile('latest-current-boundary-after.json').read()
        else:
            self.output = (ROOT / 'docs/research-evidence/photo-prompt/camera-evidence-structure-20261003/pr-review-followup/latest-qualified-boundary-pack.json').read_bytes()
        self.pack = json.loads(self.output)[0]
        self.historical_source_hashes = dict(self.baseline['metadata_only_transition']['source_files'])

    def source_hash(self, path):
        # V10's saved pack is replayed with its original qualified DATA identity,
        # never the later corpus. Production validation still reads actual bytes.
        relative = str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else None
        if self.version == 10 and relative in self.historical_source_hashes:
            return self.historical_source_hashes[relative]
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def validate(self, version=None):
        def replay(command, **kwargs):
            Path(command[command.index('--output-file') + 1]).write_bytes(self.output)
            return SimpleNamespace(returncode=0, stderr='', stdout='')
        version = 10 if version is None and self.version == 10 else version
        with mock.patch.object(validator.subprocess, 'run', side_effect=replay), \
             mock.patch.object(validator, '_sha256', side_effect=self.source_hash):
            return validator.validate_photo_regression_baseline(self.assets, baseline_version=version)

    def validate_metadata(self, pack):
        with mock.patch.object(validator, '_sha256', side_effect=self.source_hash):
            return validator._validate_metadata_only_photo_successor(
                self.assets, ROOT, self.baseline, pack, version=self.version)

    def test_registered_version_replay_and_all_legacy_artifacts_are_unchanged(self):
        self.assertEqual(self.validate()['schema'], f'photo_regression_baseline/v{self.version}')
        for path in (SKILL / 'assets').glob('photo_regression_baseline_v*.json'):
            self.assertEqual(path.read_bytes(), (self.assets / path.name).read_bytes())
        self.assertEqual(hashlib.sha256((self.assets / 'photo_regression_baseline_v9_pack.json').read_bytes()).hexdigest(),
                         '5776db59f7c06fb0ba590b7365309f044f4aa1f93594e3ad466aa90d8b1539df')

    def test_explicit_v9_is_still_strict_against_current_data(self):
        with self.assertRaisesRegex(validator.ValidationFailure, 'candidate-pack bytes drift'):
            self.validate(9)
        self.output = (self.assets / 'photo_regression_baseline_v9_pack.json').read_bytes()
        self.assertEqual(self.validate(9)['schema'], 'photo_regression_baseline/v9')

    def test_changed_predecessor_manifest_or_archival_pack_is_rejected(self):
        for name, message in ((f'photo_regression_baseline_v{self.version - 1}.json', 'successor lineage'),
                              (f'photo_regression_baseline_v{self.version - 1}_pack.json', 'historical pack binding')):
            path = self.assets / name; raw = path.read_bytes()
            with self.subTest(file=name):
                path.write_bytes(raw + b'\n')
                with self.assertRaisesRegex(validator.ValidationFailure, message): self.validate()
                path.write_bytes(raw)

    def test_wrong_data_commit_source_hash_or_comparison_provenance_is_rejected(self):
        previous_key = 'pre_nape_data_commit' if self.version == 10 else 'previous_data_commit'
        for field in ('data_commit', previous_key, 'source_files', 'evidence_sha256'):
            row = copy.deepcopy(self.baseline)
            target = row['metadata_only_transition']
            if field == 'source_files': target[field][next(iter(target[field]))] = '0' * 64
            else: target[field] = '0' * (64 if field == 'evidence_sha256' else 40)
            with self.subTest(field=field):
                self.path.write_text(json.dumps(row))
                with self.assertRaisesRegex(validator.ValidationFailure, 'provenance drift|source bytes drift'): self.validate()

    def test_extra_semantic_candidate_order_negative_and_privacy_changes_fail(self):
        for kind in ('candidate', 'order', 'scene', 'composition', 'negative', 'privacy'):
            changed = copy.deepcopy(self.pack)
            slots = [slot for slot in changed['slots'].values() if len(slot['candidates']) >= 2]
            if kind == 'candidate': slots[0]['candidates'][0]['concept_terms'][0] += ' altered'
            if kind == 'order': slots[0]['candidates'].reverse()
            if kind == 'scene': changed['authorial_core']['subject'] += ' altered'
            if kind == 'composition': changed['authorial_composition']['candidate_order'] = 'preferential'
            if kind == 'negative': changed['negative_en'] += ', suppress the subject'
            if kind == 'privacy': changed['provenance']['private_routing_exposed'] = True
            with self.subTest(kind=kind), self.assertRaisesRegex(validator.ValidationFailure, 'semantics'):
                self.validate_metadata(changed)

    def test_metadata_delta_must_have_exactly_four_changed_fields(self):
        changed = copy.deepcopy(self.pack)
        historical = json.loads((self.assets / f'photo_regression_baseline_v{self.version - 1}_pack.json').read_bytes())[0]
        changed['provenance']['tags_hash'] = historical['provenance']['tags_hash']
        with self.assertRaisesRegex(validator.ValidationFailure, 'exactly four binding fields'):
            self.validate_metadata(changed)

    def test_recomputed_output_checksum_cannot_rebaseline_a_changed_candidate(self):
        self.pack['slots'][next(key for key, slot in self.pack['slots'].items() if slot['candidates'])]['candidates'][0]['concept_terms'][0] += ' altered'
        self.pack['pack_id'] = validator._canonical_photo_pack_id(self.pack)
        self.output = (json.dumps([self.pack], ensure_ascii=False, indent=2) + '\n').encode()
        self.baseline.update(sha256=hashlib.sha256(self.output).hexdigest(), pack_id=self.pack['pack_id'])
        self.path.write_text(json.dumps(self.baseline))
        with self.assertRaisesRegex(validator.ValidationFailure, 'historical pack binding'): self.validate()


if __name__ == '__main__': unittest.main()
