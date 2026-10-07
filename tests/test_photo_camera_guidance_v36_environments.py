"""Sealed two-environment routing controls, without production runtime calls.

Synthetic stores and module doubles isolate the acceptance helper's gates.
They do not qualify either interpreter or replace the shared exact pack oracle.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import tempfile
from types import ModuleType, SimpleNamespace
import unittest
from unittest import mock

from tests import photo_camera_guidance_v36 as v


ROWS = [
    {"environment": {"implementation": "cpython", "python": [3, 12, 14], "unicode": "15.0.0"},
     "generation_id": "456ab66e03ca8c8196458ca9fbdf81c9d5ec082feaf2980f00cdfbd4754ff703",
     "source_fingerprint": "64ddd1e44c0137305a401ce5c34cbb71766bd56e3b7ebd406bd81c70a8cdd95a",
     "algorithm_sha256": "3fde760470ecdd9e06e95113fbf3af604dfe42f601e1f806ec71d2aa6d00ca3a"},
    {"environment": {"implementation": "cpython", "python": [3, 14, 3], "unicode": "16.0.0"},
     "generation_id": "2a2978af8e16aaf313570832eb6f1f6f942440bd17958a66b7d9c837ade0d70b",
     "source_fingerprint": "5e1b8c83ee0aae5489f0b73441f377e4f11031c20844c80a1a126c4c8d0364ff",
     "algorithm_sha256": "3309db453022b4db499b9d0f99bf6270526dadff7c738a99494f2b0de77a6cff"},
]


def proof_fixture():
    return {**copy.deepcopy(ROWS[0]), "verified_runtime_environments": copy.deepcopy(ROWS)}


def write_json(root, name, value):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value) + "\n")
    return path


class EnvironmentRecordTests(unittest.TestCase):
    def select(self, proof=None, environment=None):
        with mock.patch.object(v, "current_environment", return_value=environment or ROWS[1]["environment"]):
            return v.selected_runtime_record(proof if proof is not None else proof_fixture())

    def test_each_exact_tuple_selects_its_own_sealed_record_in_either_order(self):
        for row in ROWS:
            for reverse in (False, True):
                with self.subTest(environment=row["environment"], reverse=reverse):
                    proof = proof_fixture()
                    if reverse:
                        proof["verified_runtime_environments"].reverse()
                    before = copy.deepcopy(proof)
                    result = self.select(proof, row["environment"])
                    self.assertEqual(result, row)
                    result["environment"]["python"][0] = 999
                    self.assertEqual(proof, before)

    def test_unknown_and_mixed_current_tuples_fail(self):
        for change in ({"python": [3, 12, 13]}, {"python": [3, 14, 4]},
                       {"python": [3, 13, 0]}, {"implementation": "pypy"},
                       {"unicode": "15.0.0"}, {"unicode": "17.0.0"}):
            with self.subTest(change=change), self.assertRaisesRegex(AssertionError, "exact runtime environment unavailable"):
                self.select(environment={**ROWS[1]["environment"], **change})

    def test_environment_json_types_and_exact_fields_are_required(self):
        changes = [{"python": [3.0, 14, 3]}, {"python": [3, True, 3]},
                   {"python": "3.14.3"}, {"python": (3, 14, 3)}, {"python": [3, 14]},
                   {"implementation": 1}, {"unicode": 16}, {"extra": True}]
        for change in changes:
            environment = {**ROWS[1]["environment"], **change}
            with self.subTest(change=change), self.assertRaisesRegex(AssertionError, "runtime environment (types|shape)"):
                self.select(environment=environment)
            proof = proof_fixture()
            proof["verified_runtime_environments"][1]["environment"] = environment
            with self.assertRaisesRegex(AssertionError, "runtime environment (types|shape)"):
                self.select(proof)

    def test_exact_two_row_inventory_and_no_duplicate_tuple(self):
        for rows in (None, {}, [], ROWS[:1], ROWS + ROWS[:1]):
            proof = proof_fixture(); proof["verified_runtime_environments"] = rows
            with self.subTest(rows=rows), self.assertRaisesRegex(AssertionError, "runtime inventory"):
                self.select(proof)
        proof = proof_fixture(); proof["verified_runtime_environments"][1] = copy.deepcopy(ROWS[0])
        with self.assertRaisesRegex(AssertionError, "duplicate runtime environment"):
            self.select(proof)

    def test_unknown_unselected_record_is_not_ignored(self):
        proof = proof_fixture()
        proof["verified_runtime_environments"][0]["environment"]["python"] = [3, 12, 15]
        with self.assertRaisesRegex(AssertionError, "unverified runtime environment"):
            self.select(proof)

    def test_mixed_identity_components_and_duplicate_identities_fail(self):
        for field in v.RUNTIME_IDENTITY_FIELDS:
            with self.subTest(field=field):
                proof = proof_fixture()
                proof["verified_runtime_environments"][0][field] = ROWS[1][field]
                with self.assertRaisesRegex(AssertionError, "runtime record seal"):
                    self.select(proof)
                proof = proof_fixture()
                proof["verified_runtime_environments"][1][field] = ROWS[0][field]
                with self.assertRaisesRegex(AssertionError, "duplicate runtime identity"):
                    self.select(proof)

    def test_invalid_hash_and_unreviewed_row_fields_fail(self):
        for value in (None, True, 123, "A" * 64, "f" * 63, "f" * 64 + "\n"):
            proof = proof_fixture(); proof["verified_runtime_environments"][1]["generation_id"] = value
            with self.subTest(value=value), self.assertRaisesRegex(AssertionError, "invalid runtime identity"):
                self.select(proof)
        for field in ("pack_sha256", "runtime_store", "default"):
            proof = proof_fixture(); proof["verified_runtime_environments"][1][field] = "override"
            with self.subTest(field=field), self.assertRaisesRegex(AssertionError, "runtime record fields"):
                self.select(proof)

    def test_original_top_level_reference_identity_remains_unchanged(self):
        for field in ("environment", *v.RUNTIME_IDENTITY_FIELDS):
            proof = proof_fixture(); proof[field] = copy.deepcopy(ROWS[1][field])
            with self.subTest(field=field), self.assertRaisesRegex(AssertionError, "reference runtime identity"):
                self.select(proof)
        proof = proof_fixture(); proof["environment"]["python"][0] = 3.0
        with self.assertRaisesRegex(AssertionError, "reference runtime identity"):
            self.select(proof)


class RuntimeCopyTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.source, self.target = self.root / "source", self.root / "copy"
        self.namespace = v.digest(v.canonical({"root": str(self.root / v.PHOTO), "mode": "local_current", "remote": ""}))

    def prepare(self, row):
        for record in ROWS:
            (self.source / "generations" / record["generation_id"]).mkdir(parents=True, exist_ok=True)
        write_json(self.source, "local/" + self.namespace + "/CURRENT.json",
                   {field: row[field] for field in ("generation_id", "source_fingerprint")})

    def test_copy_uses_current_environment_record_and_preserves_source(self):
        for index, row in enumerate(ROWS):
            self.prepare(row)
            before = {str(p.relative_to(self.source)): p.read_bytes() for p in self.source.rglob("*") if p.is_file()}
            with self.subTest(environment=row["environment"]), mock.patch.object(v, "current_environment", return_value=row["environment"]):
                target = self.root / f"copy-{index}"
                v.copy_runtime(self.source, target, self.root, proof_fixture())
                self.assertTrue((target / "generations" / row["generation_id"]).is_dir())
                self.assertEqual({str(p.relative_to(self.source)): p.read_bytes() for p in self.source.rglob("*") if p.is_file()}, before)

    def test_cross_environment_pointer_and_missing_selected_generation_fail(self):
        self.prepare(ROWS[0])
        with mock.patch.object(v, "current_environment", return_value=ROWS[1]["environment"]):
            with self.assertRaisesRegex(AssertionError, "runtime pointer drift"):
                v.copy_runtime(self.source, self.target, self.root, proof_fixture())
            (self.source / "generations" / ROWS[1]["generation_id"]).rmdir()
            with self.assertRaisesRegex(AssertionError, "published generation unavailable"):
                v.copy_runtime(self.source, self.root / "missing-copy", self.root, proof_fixture())

    def test_unknown_environment_fails_before_copy(self):
        with mock.patch.object(v, "current_environment", return_value={**ROWS[1]["environment"], "unicode": "15.0.0"}), \
                mock.patch.object(v.shutil, "copytree") as copytree:
            with self.assertRaisesRegex(AssertionError, "exact runtime environment unavailable"):
                v.copy_runtime(self.source, self.target, self.root, proof_fixture())
            copytree.assert_not_called()


class SnapshotEnvironmentTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.store = self.root / "runtime"; self.store.mkdir()
        self.proof = proof_fixture()
        self.proof.update(baseline_composed_path="composed.json", runtime_request_path="request.json")
        write_json(self.root, "composed.json", {"prompt_en": "synthetic prompt"})
        write_json(self.root, "request.json", {"runtime_prompt_en": "synthetic prompt"})
        self.baseline = {"schema": "photo_regression_baseline/v36"}
        self.pack = {"pack_id": "synthetic", "authorial_core": {"baseline_prompt_en": "synthetic prompt"}}
        self.row = copy.deepcopy(ROWS[1])
        self.receipt = {field: self.row[field] for field in v.RUNTIME_IDENTITY_FIELDS}
        self.snapshot = SimpleNamespace(generation_id=self.row["generation_id"], manifest={
            "source": {"environment": copy.deepcopy(self.row["environment"])},
            **{field: self.row[field] for field in ("source_fingerprint", "algorithm_sha256")}})
        self.runtime = ModuleType("photo_runtime_sources")
        self.runtime.RuntimeSnapshotProvider = mock.Mock()
        self.runtime.RuntimeSnapshotProvider.return_value.from_receipt.return_value = self.snapshot
        self.runtime.capture_sources = mock.Mock(side_effect=lambda root: (copy.deepcopy(self.snapshot.manifest["source"]), None))
        self.composed = ModuleType("audit_composed_prompt")
        self.composed.audit_composed_prompt = mock.Mock(return_value={"status": "pass"})
        self.render = ModuleType("audit_image_render_request")
        self.render.audit_image_render_request = mock.Mock(return_value={"status": "pass"})
        for module in (self.runtime, self.composed, self.render):
            module.__file__ = str(self.root / v.PHOTO / "scripts" / (module.__name__ + ".py"))
        self.enterContext(mock.patch.dict(sys.modules, {m.__name__: m for m in (self.runtime, self.composed, self.render)}))
        self.enterContext(mock.patch.object(v, "qualify_current", return_value=self.proof))
        self.environment = self.enterContext(mock.patch.object(v, "current_environment", return_value=self.row["environment"]))

    def qualify(self, receipt=None):
        return v.qualify_snapshot(self.root, self.baseline, self.pack, b"synthetic", self.receipt if receipt is None else receipt,
                                  runtime_store=self.store)

    def test_each_environment_uses_its_own_receipt_and_snapshot(self):
        for row in ROWS:
            self.environment.return_value = row["environment"]
            self.snapshot.generation_id = row["generation_id"]
            self.snapshot.manifest.update({field: row[field] for field in ("source_fingerprint", "algorithm_sha256")})
            self.snapshot.manifest["source"]["environment"] = row["environment"]
            receipt = {field: row[field] for field in v.RUNTIME_IDENTITY_FIELDS}
            with self.subTest(environment=row["environment"]):
                result = self.qualify(receipt)
                self.assertEqual(result["generation_id"], row["generation_id"])
                self.assertEqual(result["private_runtime_receipt"], receipt)
                self.assertIsNot(result["private_runtime_receipt"], receipt)
                self.runtime.RuntimeSnapshotProvider.return_value.from_receipt.assert_called_with(self.pack, receipt)
                self.composed.audit_composed_prompt.assert_called_with(
                    self.pack, {"prompt_en": "synthetic prompt"}, runtime_receipt=receipt, runtime_store=self.store)
                self.render.audit_image_render_request.assert_called()

    def test_receipt_cannot_select_another_environment_or_mix_identities(self):
        receipts = [{field: ROWS[0][field] for field in v.RUNTIME_IDENTITY_FIELDS}]
        receipts.extend({**self.receipt, field: ROWS[0][field]} for field in v.RUNTIME_IDENTITY_FIELDS)
        for receipt in receipts:
            with self.subTest(receipt=receipt), self.assertRaisesRegex(AssertionError, "receipt identity drift"):
                self.qualify(receipt)
        self.runtime.RuntimeSnapshotProvider.assert_not_called()

    def test_snapshot_identity_and_typed_environment_must_match_selected_record(self):
        original = copy.deepcopy(self.snapshot)
        changes = [("generation_id", ROWS[0]["generation_id"]),
                   ("source_fingerprint", ROWS[0]["source_fingerprint"]),
                   ("algorithm_sha256", ROWS[0]["algorithm_sha256"]),
                   ("environment", ROWS[0]["environment"]),
                   ("environment", {**ROWS[1]["environment"], "python": [3.0, 14, 3]})]
        for field, value in changes:
            self.snapshot.generation_id = original.generation_id
            self.snapshot.manifest = copy.deepcopy(original.manifest)
            if field == "generation_id":
                self.snapshot.generation_id = value
            elif field == "environment":
                self.snapshot.manifest["source"][field] = value
            else:
                self.snapshot.manifest[field] = value
            with self.subTest(field=field, value=value), self.assertRaisesRegex(AssertionError, "snapshot identity drift"):
                self.qualify()
        self.composed.audit_composed_prompt.assert_not_called()
        self.render.audit_image_render_request.assert_not_called()

    def test_live_source_and_production_audits_remain_required(self):
        self.runtime.capture_sources.return_value = ({"changed": True}, None)
        self.runtime.capture_sources.side_effect = None
        with self.assertRaisesRegex(AssertionError, "live source differs"):
            self.qualify()
        self.runtime.capture_sources.return_value = (self.snapshot.manifest["source"], None)
        for audit in (self.composed.audit_composed_prompt, self.render.audit_image_render_request):
            audit.return_value = {"status": "fail"}
            with self.assertRaisesRegex(AssertionError, "production audits failed"):
                self.qualify()
            audit.return_value = {"status": "pass"}

    def test_unknown_environment_fails_before_provider_and_current_cli(self):
        self.environment.return_value = {**ROWS[1]["environment"], "python": [3, 14, 4]}
        with self.assertRaisesRegex(AssertionError, "exact runtime environment unavailable"):
            self.qualify()
        self.runtime.RuntimeSnapshotProvider.assert_not_called()
        self.proof["unedited_upstream_pack_path"] = "upstream.json"
        write_json(self.root, "upstream.json", [self.pack])
        write_json(self.root, v.ASSETS + "/photo_regression_baseline_v36_pack.json", [self.pack])
        with mock.patch.object(v, "qualification_context", return_value=(self.proof, self.baseline, b"original")), \
                mock.patch.object(v, "qualify_pack"), mock.patch.object(v, "copy_runtime") as copy_runtime, \
                mock.patch.object(v.subprocess, "run") as run:
            with self.assertRaisesRegex(AssertionError, "exact runtime environment unavailable"):
                v.validate_current(self.root / v.ASSETS, source_root=self.root, runtime_store=self.store)
            copy_runtime.assert_not_called()
            run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
