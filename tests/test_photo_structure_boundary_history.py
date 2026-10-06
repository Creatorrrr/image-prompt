"""V24 changes authored representation while preserving the complete V23 pack."""
from __future__ import annotations

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

from tests import photo_prompt_fixtures as fixtures

ROOT = Path(__file__).resolve().parents[1]
ILLUSTRATION = ROOT / "skills/subculture-illustration-image-generator"
EVIDENCE = Path("docs/research-evidence/photo-prompt/structure-maintenance-20261006/main-integration")
PROOF = EVIDENCE / "V24-STRUCTURE-BINDING-PROOF.json"
sys.path.insert(0, str(ILLUSTRATION / "scripts"))
import validate_illustration_assets as validator


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


class V23StructureParentFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        frozen = tempfile.TemporaryDirectory(prefix="sealed-v23-parent-")
        cls.addClassCleanup(frozen.cleanup)
        cls.root = Path(frozen.name)
        with mock.patch("subprocess.Popen", side_effect=AssertionError("Offline fixture invoked a subprocess")):
            cls.validator = fixtures.archived_v23_validator(cls.root, source_root=ROOT)
        cls.manifest = fixtures._v23_parent_manifest(ROOT)

    def test_original_v23_passes_with_the_original_runtime_and_data(self):
        assets = self.root / "skills/subculture-illustration-image-generator/assets"
        baseline = json.loads((assets / "photo_regression_baseline_v23.json").read_bytes())
        raw = (assets / "photo_regression_baseline_v23_pack.json").read_bytes()
        with mock.patch("subprocess.Popen", side_effect=AssertionError("Historical check invoked a subprocess")):
            self.validator._validate_v23_lobe_boundary_successor(
                assets, self.root, baseline, json.loads(raw)[0], raw)
        for row in self.manifest["members"]:
            with self.subTest(path=row["path"]):
                path = self.root / row["path"]
                self.assertFalse(path.is_symlink())
                self.assertEqual(row["sha256"], digest(path.read_bytes()))

    def test_manifest_mapping_and_coordinated_rehash_cannot_replace_the_parent(self):
        original = (ROOT / fixtures.V23_PARENT_MANIFEST).read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "input"
            path = source / fixtures.V23_PARENT_MANIFEST
            path.parent.mkdir(parents=True)
            for kind in ("source_pin", "traversal", "live_source", "missing", "duplicate", "coordinated_rehash"):
                changed = json.loads(original)
                if kind == "source_pin":
                    changed["source_pin"] = "0" * 40
                elif kind == "traversal":
                    changed["members"][0]["source_path"] = "../escape"
                elif kind == "live_source":
                    row = next(r for r in changed["members"] if r["kind"] == "new_immutable_snapshot_same_git_blob")
                    row["source_path"] = row["path"]
                elif kind == "missing":
                    changed["members"].pop()
                elif kind == "duplicate":
                    changed["members"][1] = copy.deepcopy(changed["members"][0])
                else:
                    row = changed["members"][0]
                    payload = (ROOT / row["source_path"]).read_bytes() + b"\n"
                    row.update(bytes=len(payload), sha256=digest(payload),
                               git_blob=hashlib.sha1(f"blob {len(payload)}\0".encode() + payload).hexdigest())
                path.write_bytes(encoded(changed))
                output = root / "output"
                with self.subTest(kind=kind), self.assertRaises(AssertionError):
                    fixtures.materialize_v23_parent_source(output, source_root=source)
                self.assertFalse(output.exists())

    def test_archived_imports_use_the_sealed_support_modules(self):
        hook = self.validator.__dict__["__builtins__"]["__import__"]
        with mock.patch.dict(sys.modules, {"illustration_runtime": object(), "universal_scene_runtime": object()}):
            for name in ("illustration_runtime", "universal_scene_runtime"):
                loaded = hook(name)
                self.assertEqual(self.root / "skills/subculture-illustration-image-generator/scripts" / (name + ".py"),
                                 Path(loaded.__file__))


class StructureBoundaryHistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proof = json.loads((ROOT / PROOF).read_bytes())
        cls.parent = json.loads((ROOT / cls.proof["parent_source_manifest"]).read_bytes())

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="v24-boundary-")
        self.addCleanup(temporary.cleanup)
        self.repo = Path(temporary.name)
        self.assets = self.repo / "skills/subculture-illustration-image-generator/assets"
        paths = {str(PROOF), self.proof["parent_source_manifest"], self.proof["previous_proof_path"],
                 self.proof["universal_v2_before_path"],
                 "skills/subculture-illustration-image-generator/assets/universal_scene_baseline_v2.json"}
        paths.update(self.proof["source_files_after"])
        paths.update(row["source_path"] for row in self.parent["members"])
        paths.update(row["path"] for row in self.parent["members"])
        for field in ("active_semantic_shards", "active_visual_shards",
                      "retained_semantic_shards", "retained_visual_shards"):
            paths.update(self.proof[field])
        paths.update(str(p.relative_to(ROOT)) for p in (ILLUSTRATION / "assets").glob("photo_regression_baseline_v*.json"))
        for name in paths:
            path = self.repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.symlink_to(ROOT / name)
        self.baseline = json.loads((self.assets / "photo_regression_baseline_v24.json").read_bytes())
        self.original_baseline = copy.deepcopy(self.baseline)
        self.raw = (self.assets / "photo_regression_baseline_v24_pack.json").read_bytes()
        self.pack = json.loads(self.raw)[0]

    @contextmanager
    def changed(self, name, raw):
        path = self.repo / name
        link = path.readlink() if path.is_symlink() else None
        path.unlink(missing_ok=True)
        path.parent.mkdir(parents=True, exist_ok=True)
        if raw is not None:
            path.write_bytes(raw)
        try:
            yield
        finally:
            path.unlink(missing_ok=True)
            if link is not None:
                path.symlink_to(link)

    def validate(self, pack=None, raw=None):
        validator._validate_v24_structure_source_successor(
            self.assets, self.repo, self.baseline,
            self.pack if pack is None else pack, self.raw if raw is None else raw)

    def test_complete_public_pack_and_retrieval_values_are_unchanged(self):
        self.validate()
        self.assertEqual((self.assets / "photo_regression_baseline_v23_pack.json").read_bytes(), self.raw)
        self.assertEqual([], self.proof["reviewed_pack_delta"])
        self.assertEqual(13, len(self.proof["reviewed_source_deltas"]))
        self.assertEqual(2, len(self.proof["added_source_paths"]))
        self.assertEqual((52, 34, 50), tuple(self.proof[key] for key in
                         ("registered_candidates", "registered_visual_profile_extensions", "required_candidate_files")))

    def test_current_default_and_explicit_v24_are_registered(self):
        def frozen_command(command, **kwargs):
            Path(command[command.index("--output-file") + 1]).write_bytes(self.raw)
            return subprocess.CompletedProcess(command, 0, "", "")

        with mock.patch.object(validator.subprocess, "run", side_effect=frozen_command):
            for version in (None, 24):
                with self.subTest(version=version):
                    result = validator.validate_photo_regression_baseline(ILLUSTRATION / "assets", baseline_version=version)
                    self.assertEqual("photo_regression_baseline/v24", result["schema"])
                    self.assertEqual(self.proof["current_pack_sha256"], result["sha256"])
        with self.assertRaisesRegex(validator.ValidationFailure, "unsupported photo baseline version"):
            validator.validate_photo_regression_baseline(self.assets, baseline_version=25)

    def test_original_v23_rejects_the_current_raw_source_representation(self):
        baseline = json.loads((self.assets / "photo_regression_baseline_v23.json").read_bytes())
        with self.assertRaises(validator.ValidationFailure):
            validator._validate_v23_lobe_boundary_successor(
                self.assets, self.repo, baseline, self.pack, self.raw)

    def test_fixed_proof_rejects_coordinated_rebinding(self):
        for field, value in (("source_parent_commit", "0" * 40), ("source_files_after", {}),
                             ("reviewed_pack_delta", [{"changed": True}]),
                             ("compiled_visual_meaning_sha256_after", "0" * 64)):
            changed = copy.deepcopy(self.proof)
            changed[field] = value
            raw = encoded(changed)
            self.baseline = copy.deepcopy(self.original_baseline)
            self.baseline["structure_source_transition"]["evidence_sha256"] = digest(raw)
            with self.subTest(field=field), self.changed(PROOF, raw), self.assertRaises(validator.ValidationFailure):
                self.validate()

    def test_source_and_registered_inventory_drift_are_rejected(self):
        names = ["skills/photo-prompt-image-generator/assets/photo_prompt_source_manifest.json",
                 "skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json",
                 "skills/photo-prompt-image-generator/scripts/visual_profile_contracts.py"]
        for name in names:
            with self.subTest(path=name), self.changed(name, (ROOT / name).read_bytes() + b"\n"), self.assertRaises(validator.ValidationFailure):
                self.validate()
        with self.changed("skills/photo-prompt-image-generator/assets/photo_prompt_unregistered_extension.json", b"{}"), self.assertRaises(validator.ValidationFailure):
            self.validate()

    def test_rehashed_pack_changes_and_mismatched_raw_are_rejected(self):
        name = "skills/subculture-illustration-image-generator/assets/photo_regression_baseline_v24_pack.json"
        for kind in ("order", "core", "negative", "privacy"):
            changed = copy.deepcopy(self.pack)
            if kind == "order":
                next(s for s in changed["slots"].values() if len(s["candidates"]) >= 2)["candidates"].reverse()
            elif kind == "core":
                changed["authorial_core"]["subject"] += " changed"
            elif kind == "negative":
                changed["negative_en"] += ", changed"
            else:
                changed["provenance"]["private_routing_exposed"] = True
            changed["pack_id"] = validator._canonical_photo_pack_id(changed)
            raw = encoded([changed])
            self.baseline = copy.deepcopy(self.original_baseline)
            self.baseline.update(sha256=digest(raw), pack_id=changed["pack_id"])
            with self.subTest(kind=kind), self.changed(name, raw), self.assertRaises(validator.ValidationFailure):
                self.validate(changed, raw)
        with self.assertRaises(validator.ValidationFailure):
            self.validate(raw=self.raw + b"\n")

    def test_active_retained_and_extra_shards_are_rejected(self):
        for field in ("active_semantic_shards", "active_visual_shards",
                      "retained_semantic_shards", "retained_visual_shards"):
            name = next(iter(self.proof[field]))
            for kind, path, raw in (("changed", name, (ROOT / name).read_bytes() + b" "),
                                    ("missing", name, None),
                                    ("extra", str(Path(name).parent / "shard-999.json"), b"{}")):
                with self.subTest(field=field, kind=kind), self.changed(path, raw), self.assertRaises((FileNotFoundError, validator.ValidationFailure)):
                    self.validate()

    def test_historical_source_and_descriptor_changes_are_rejected(self):
        archived = next(row["source_path"] for row in self.parent["members"]
                        if row["path"].endswith("/scripts/validate_illustration_assets.py")
                        and row["kind"] == "new_immutable_snapshot_same_git_blob")
        for name in (archived, "skills/subculture-illustration-image-generator/assets/universal_scene_baseline_v2.json"):
            with self.subTest(path=name), self.changed(name, (ROOT / name).read_bytes() + b"\n"), self.assertRaises(validator.ValidationFailure):
                self.validate()


if __name__ == "__main__":
    unittest.main()
