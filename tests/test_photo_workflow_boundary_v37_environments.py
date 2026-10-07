"""Current629 environment controls; synthetic stores and production doubles only.

The sixteen immutable V36 controls run against V37 through per-case patches of
the test module. V36 production globals are never rebound. These controls do
not run a public CLI, qualify an interpreter, or replace a receipt replay.
"""
from __future__ import annotations

import copy
import sys
import unittest
from unittest import mock

from tests import photo_workflow_boundary_v37 as v
from tests import test_photo_camera_guidance_v36_environments as previous


# Exact environment/runtime projections of the fresh current629 evidence:
# runtime312-preparation/compact/RESULT.json and
# runtime314-preparation/compact/RESULT.json. The full-row seals are independent
# literals, so changing a fixture cannot silently change its expected seal.
ROWS = [
    {"environment": {"implementation": "cpython", "python": [3, 12, 14], "unicode": "15.0.0"},
     "generation_id": "22ca4ea2bf0ca757e81dbd17259ca204ab36b9da6405d501e194164c7f4c30c2",
     "source_fingerprint": "6762a852bb0bea52bfa468d733f5d5aa29ed681eab21c276239435db98814685",
     "algorithm_sha256": "ab3ded01f178785718a1ad64e44d041958889ebcca7d25ebb4db23caa694f589"},
    {"environment": {"implementation": "cpython", "python": [3, 14, 3], "unicode": "16.0.0"},
     "generation_id": "956332d237a7e24770080e93134feb26d03b4886f91a5858975d16d6f83e9432",
     "source_fingerprint": "35af9b17b6ebc71ae6a54c94f7b6ae4fae3b4c375d23036e146fea3a0c72cd09",
     "algorithm_sha256": "8ddb08f89426727a9366de119f3c85b1d815a8c2a7db6d839e6715fbe6ad4ba6"},
]
ROW_SEALS = (
    "fae35801d8d0c86e805db503e11c66cea4baec440939f335146fab5ea7a7bd8d",
    "0833e12ab9da117160c94f529436c5229138be69cec8e734f017c044280bbe20",
)
OLD4F_ROWS = copy.deepcopy(previous.ROWS)


class _Current629Cases:
    def setUp(self):
        self.enterContext(mock.patch.object(previous, "v", v))
        self.enterContext(mock.patch.object(previous, "ROWS", copy.deepcopy(ROWS)))
        super().setUp()


class EnvironmentRecordTests(_Current629Cases, previous.EnvironmentRecordTests):
    def test_current629_rows_match_independent_complete_row_seals(self):
        expected = {v.environment_key(row["environment"]): seal for row, seal in zip(ROWS, ROW_SEALS)}
        self.assertEqual(v.VERIFIED_RUNTIME_RECORDS, expected)
        for row, seal in zip(ROWS, ROW_SEALS):
            with self.subTest(environment=row["environment"]):
                self.assertEqual(v.digest(v.canonical(row)), seal)
                self.assertEqual(self.select(environment=row["environment"]), row)

    def test_old4f_complete_rows_fail_even_when_not_selected(self):
        for index, old in enumerate(OLD4F_ROWS):
            for selected in ROWS:
                proof = previous.proof_fixture()
                proof["verified_runtime_environments"][index] = copy.deepcopy(old)
                with self.subTest(index=index, selected=selected["environment"]), \
                        self.assertRaisesRegex(AssertionError, "runtime record seal"):
                    self.select(proof, selected["environment"])

    def test_old4f_identity_components_cannot_enter_current_rows(self):
        for index, old in enumerate(OLD4F_ROWS):
            for field in v.RUNTIME_IDENTITY_FIELDS:
                proof = previous.proof_fixture()
                proof["verified_runtime_environments"][index][field] = old[field]
                with self.subTest(index=index, field=field), \
                        self.assertRaisesRegex(AssertionError, "runtime record seal"):
                    self.select(proof)

    def test_current_identity_cannot_move_to_the_other_exact_environment(self):
        proof = previous.proof_fixture()
        for index, row in enumerate(proof["verified_runtime_environments"]):
            row["environment"] = copy.deepcopy(ROWS[1 - index]["environment"])
        with self.assertRaisesRegex(AssertionError, "runtime record seal"):
            self.select(proof)

    def test_environment_container_and_missing_fields_fail_closed(self):
        environments = [None, [], "cpython", False]
        environments.extend({key: value for key, value in ROWS[0]["environment"].items() if key != missing}
                            for missing in ROWS[0]["environment"])
        for environment in environments:
            with self.subTest(environment=environment), \
                    self.assertRaisesRegex(AssertionError, "runtime environment shape"):
                v.environment_key(environment)

    def test_well_formed_unreviewed_hashes_fail_the_unselected_row_seal(self):
        for field in v.RUNTIME_IDENTITY_FIELDS:
            proof = previous.proof_fixture()
            proof["verified_runtime_environments"][0][field] = "f" * 64
            with self.subTest(field=field), self.assertRaisesRegex(AssertionError, "runtime record seal"):
                self.select(proof, ROWS[1]["environment"])


class RuntimeCopyTests(_Current629Cases, previous.RuntimeCopyTests):
    def test_old4f_pointer_fails_despite_available_current_generation(self):
        for index, (row, old) in enumerate(zip(ROWS, OLD4F_ROWS)):
            self.prepare(old)
            with self.subTest(environment=row["environment"]), \
                    mock.patch.object(v, "current_environment", return_value=row["environment"]), \
                    self.assertRaisesRegex(AssertionError, "runtime pointer drift"):
                v.copy_runtime(self.source, self.root / f"old-pointer-{index}", self.root, previous.proof_fixture())

    def test_old4f_generation_cannot_replace_missing_current_generation(self):
        for index, (row, old) in enumerate(zip(ROWS, OLD4F_ROWS)):
            self.prepare(row)
            (self.source / "generations" / row["generation_id"]).rmdir()
            (self.source / "generations" / old["generation_id"]).mkdir()
            with self.subTest(environment=row["environment"]), \
                    mock.patch.object(v, "current_environment", return_value=row["environment"]), \
                    self.assertRaisesRegex(AssertionError, "published generation unavailable"):
                v.copy_runtime(self.source, self.root / f"old-generation-{index}", self.root, previous.proof_fixture())

    def test_current_generation_with_old4f_source_pointer_fails(self):
        for index, (row, old) in enumerate(zip(ROWS, OLD4F_ROWS)):
            self.prepare({**row, "source_fingerprint": old["source_fingerprint"]})
            with self.subTest(environment=row["environment"]), \
                    mock.patch.object(v, "current_environment", return_value=row["environment"]), \
                    self.assertRaisesRegex(AssertionError, "runtime pointer drift"):
                v.copy_runtime(self.source, self.root / f"old-source-{index}", self.root, previous.proof_fixture())


class SnapshotEnvironmentTests(_Current629Cases, previous.SnapshotEnvironmentTests):
    def setUp(self):
        super().setUp()
        self.proof["current_pack_path"] = v.ASSETS + "/photo_regression_baseline_v36_pack.json"
        self.baseline["schema"] = "photo_regression_baseline/v37"

    def test_old4f_receipts_and_mixed_components_fail_before_provider(self):
        for row, old in zip(ROWS, OLD4F_ROWS):
            self.environment.return_value = row["environment"]
            current = {field: row[field] for field in v.RUNTIME_IDENTITY_FIELDS}
            receipts = [{field: old[field] for field in v.RUNTIME_IDENTITY_FIELDS}]
            receipts.extend({**current, field: old[field]} for field in v.RUNTIME_IDENTITY_FIELDS)
            for receipt in receipts:
                with self.subTest(environment=row["environment"], receipt=receipt), \
                        self.assertRaisesRegex(AssertionError, "receipt identity drift"):
                    self.qualify(receipt)
        self.runtime.RuntimeSnapshotProvider.assert_not_called()
        self.runtime.capture_sources.assert_not_called()
        self.composed.audit_composed_prompt.assert_not_called()
        self.render.audit_image_render_request.assert_not_called()

    def test_old4f_snapshot_generation_fails_for_a_current_receipt(self):
        for row, old in zip(ROWS, OLD4F_ROWS):
            self.environment.return_value = row["environment"]
            self.snapshot.generation_id = old["generation_id"]
            self.snapshot.manifest.update({field: row[field] for field in ("source_fingerprint", "algorithm_sha256")})
            self.snapshot.manifest["source"]["environment"] = copy.deepcopy(row["environment"])
            receipt = {field: row[field] for field in v.RUNTIME_IDENTITY_FIELDS}
            with self.subTest(environment=row["environment"]), \
                    self.assertRaisesRegex(AssertionError, "snapshot identity drift"):
                self.qualify(receipt)
        self.composed.audit_composed_prompt.assert_not_called()
        self.render.audit_image_render_request.assert_not_called()

    def test_wrong_private_pack_binding_is_forwarded_and_provider_rejection_propagates(self):
        # Production from_receipt owns pack/canonical/bindings validation. This
        # double checks delegation and failure propagation, not that validation.
        receipt = {**self.receipt, "schema": "photo-runtime-receipt/v1", "pack_sha256": "0" * 64}
        error = RuntimeError("receipt/pack binding mismatch")
        provider = self.runtime.RuntimeSnapshotProvider.return_value
        provider.from_receipt.side_effect = error
        with self.assertRaises(RuntimeError) as raised:
            self.qualify(receipt)
        self.assertIs(raised.exception, error)
        provider.from_receipt.assert_called_once_with(self.pack, receipt)
        self.runtime.capture_sources.assert_not_called()
        self.composed.audit_composed_prompt.assert_not_called()
        self.render.audit_image_render_request.assert_not_called()

    def test_provider_failures_propagate_without_leaving_import_path_changes(self):
        constructor = self.runtime.RuntimeSnapshotProvider
        for stage in (constructor, constructor.return_value.from_receipt):
            error = RuntimeError("generation deep validation failed")
            stage.side_effect = error
            before = sys.path.copy()
            with self.subTest(stage=stage), self.assertRaises(RuntimeError) as raised:
                self.qualify()
            self.assertIs(raised.exception, error)
            self.assertEqual(sys.path, before)
            stage.side_effect = None
        self.runtime.capture_sources.assert_not_called()
        self.composed.audit_composed_prompt.assert_not_called()
        self.render.audit_image_render_request.assert_not_called()

    def test_complete_private_receipt_is_preserved_and_deep_copied(self):
        receipt = {**self.receipt, "schema": "photo-runtime-receipt/v1",
                   "bindings": {"source": {"sha256": "a" * 64}}, "request_id": "synthetic-request"}
        result = self.qualify(receipt)
        self.assertEqual(result["schema"], "photo_regression_baseline/v37")
        self.assertEqual(result["private_runtime_receipt"], receipt)
        self.runtime.RuntimeSnapshotProvider.return_value.from_receipt.assert_called_once_with(self.pack, receipt)
        result["private_runtime_receipt"]["bindings"]["source"]["sha256"] = "b" * 64
        self.assertEqual(receipt["bindings"]["source"]["sha256"], "a" * 64)


if __name__ == "__main__":
    unittest.main()
