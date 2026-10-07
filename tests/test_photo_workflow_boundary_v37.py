"""V37 source, full-pack, namespace and explicit-history negative controls.

These use immutable public fixtures and independent synthetic files. No test
publishes a runtime or generates a candidate pack.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

from tests import photo_workflow_boundary_v37 as v
from tests import photo_camera_guidance_history_v36 as history

ROOT = Path(__file__).resolve().parents[1]


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


class PackTests(unittest.TestCase):
    def setUp(self):
        self.raw = (ROOT / v.CURRENT_PACK).read_bytes()
        self.pack = v.strict_json(self.raw)[0]
        self.proof = {"reviewed_upstream_pack_delta": [], "reviewed_doc_only_pack_delta": [],
                      "current_pack_sha256": v.PACK_SHA256, "current_pack_id": v.PACK_ID,
                      "preserved_public_candidate_count": 64}
        self.baseline = {"sha256": v.PACK_SHA256, "pack_id": v.PACK_ID, "public_candidate_count": 64}

    def check(self, pack=None, raw=None):
        v.qualify_pack(self.proof, self.baseline, self.pack if pack is None else pack,
                       self.raw if raw is None else raw, self.raw, self.raw)

    def test_complete_recorded_pack_is_preserved(self):
        self.check()
        self.assertEqual(len(self.pack), 29)

    def test_private_or_new_candidate_fields_cannot_be_rehashed_into_acceptance(self):
        for field in ("private_runtime_receipt", "request_id", "new_candidate_surface"):
            pack = copy.deepcopy(self.pack); pack[field] = {"injected": True}
            raw = encoded([pack])
            self.proof["current_pack_sha256"] = self.baseline["sha256"] = v.digest(raw)
            with self.subTest(field=field), self.assertRaisesRegex(AssertionError, "documentation pack differs"):
                self.check(pack, raw)

    def test_types_semantics_order_and_protections_are_not_overridable(self):
        changes = [lambda p: p["authorial_core"].update(subject="changed"),
                   lambda p: p.update(negative_en=""),
                   lambda p: p["provenance"].update(seed=True),
                   lambda p: p["semantic_clarification"]["candidates"].reverse(),
                   lambda p: p["semantic_clarification"]["candidates"][0].update(id="changed")]
        for change in changes:
            pack = copy.deepcopy(self.pack); change(pack)
            with self.subTest(change=change), self.assertRaisesRegex(AssertionError, "pack JSON shape"):
                self.check(pack)

    def test_both_reviewed_deltas_must_be_exactly_empty(self):
        for field in ("reviewed_upstream_pack_delta", "reviewed_doc_only_pack_delta"):
            for value in (None, {}, [{"pointer": "/0/pack_id", "after": "replacement"}]):
                self.proof[field] = value
                with self.subTest(field=field, value=value), self.assertRaisesRegex(AssertionError, "must be empty"):
                    self.check()
            self.proof[field] = []

    def test_descriptor_counts_are_typed_and_ids_are_bound(self):
        for target, field, value in ((self.proof, "preserved_public_candidate_count", 64.0),
                                     (self.baseline, "public_candidate_count", True),
                                     (self.baseline, "pack_id", "other")):
            before = target[field]; target[field] = value
            with self.subTest(field=field), self.assertRaisesRegex(AssertionError, "descriptor binding"):
                self.check()
            target[field] = before


class SourceTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(); self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def write(self, name, raw=b"original"):
        path = self.root / name; path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw); path.chmod(0o644)
        return path

    def test_exact_173_members_reject_added_removed_and_replaced_sources(self):
        names = {v.SKILL, "tests/test_photo_visual_profile_shards.py"}
        names.update(v.PHOTO + f"/scripts/synthetic_{i}.py" for i in range(154))
        old = {"source_files_after": {name: v.digest(b"original") for name in names}}
        expected = names | v.NEW_SOURCE_PATHS
        mapping = {name: v.SKILL_SHA256 if name == v.SKILL else v.digest(b"original") for name in expected}
        upstream = SimpleNamespace(payload=lambda name: b"original", entry=lambda name: {"mode": "100644"})
        gate = SimpleNamespace(require_live_payload=mock.Mock())
        with mock.patch.object(v, "live_source_paths", return_value=expected):
            v.verify_sources(self.root, mapping, upstream, old, gate)
            self.assertEqual(gate.require_live_payload.call_count, 173)
            for mutation in (lambda m: m.pop(next(iter(m))),
                             lambda m: m.update({v.PHOTO + "/scripts/unreviewed.py": "0" * 64}),
                             lambda m: m.update({v.PHOTO + "/scripts/photo_workflow.py": "0" * 64})):
                changed = dict(mapping); mutation(changed)
                with self.subTest(mutation=mutation), self.assertRaisesRegex(AssertionError, "inventory|upstream/documentation"):
                    v.verify_sources(self.root, changed, upstream, old, gate)
        with mock.patch.object(v, "live_source_paths", return_value=expected | {"extra.py"}):
            with self.assertRaisesRegex(AssertionError, "exactly 173"):
                v.verify_sources(self.root, mapping, upstream, old, gate)

    def test_new_real_source_file_is_visible_to_inventory(self):
        for directory in ("assets", "precore", "references", "scripts"):
            (self.root / v.PHOTO / directory).mkdir(parents=True)
        name = v.PHOTO + "/scripts/unreviewed.py"
        self.write(name)
        self.assertIn(name, v.live_source_paths(self.root))

    def test_live_source_mode_bytes_and_symlink_stay_strict(self):
        name = "source.py"; path = self.write(name)
        expected = v.digest(path.read_bytes())
        history.require_live_payload(self.root, name, expected, "100644")
        for kind in ("bytes", "mode", "symlink"):
            path.unlink(); path = self.write(name)
            if kind == "bytes": path.write_bytes(b"different")
            elif kind == "mode": path.chmod(0o755)
            else:
                path.unlink(); path.symlink_to(self.write("other.py"))
            with self.subTest(kind=kind), self.assertRaises(AssertionError):
                history.require_live_payload(self.root, name, expected, "100644")

    def test_proof_lineage_and_zero_count_have_independent_checks(self):
        proof = {"schema": "photo-workflow-source-transition/v37", "upstream_commit": v.UPSTREAM_PIN,
                 "upstream_tree": v.UPSTREAM_TREE, "parent_boundary_commit": v.PARENT_PIN,
                 "parent_boundary_tree": v.PARENT_TREE, "reviewed_skill_sha256": v.SKILL_SHA256,
                 "data_improvement_count_delta": 0, "doc_only_comparison_control": "same_runtime"}
        for change in ({}, {"data_improvement_count_delta": False}, {"data_improvement_count_delta": 1},
                       {"upstream_commit": v.previous.UPSTREAM_PIN}, {"upstream_tree": "0" * 40},
                       {"parent_boundary_tree": "0" * 40}, {"doc_only_comparison_control": "observational"}):
            raw = encoded({**proof, **change}); self.write(v.PROOF, raw)
            with self.subTest(change=change), mock.patch.object(v, "PROOF_SHA256", v.digest(raw)):
                if change:
                    with self.assertRaisesRegex(AssertionError, "lineage or comparison"):
                        v.load_proof(self.root)
                else:
                    self.assertEqual(v.load_proof(self.root), proof)
        with self.assertRaisesRegex(AssertionError, "proof seal"):
            v.load_proof(self.root)

    def test_historical_live_reuse_requires_exact_old_blob_and_mode(self):
        raw = b"original"; path = self.write("source.py", raw)
        row = {"mode": "100644", "git_blob": history._object_id("blob", raw)}
        snapshot = SimpleNamespace(entry=mock.Mock(return_value=row), payload=mock.Mock(return_value=b"exact old"))
        self.assertEqual(v._parent_payload(self.root, snapshot, "source.py")[0], raw)
        snapshot.payload.assert_not_called()
        path.write_bytes(b"latest replacement")
        self.assertEqual(v._parent_payload(self.root, snapshot, "source.py")[0], b"exact old")
        path.write_bytes(raw); path.chmod(0o755)
        snapshot.payload.reset_mock()
        v._parent_payload(self.root, snapshot, "source.py")
        snapshot.payload.assert_called_once()

    def test_original_test_mapping_has_only_two_explicit_exceptions(self):
        self.assertEqual(len(v.ORIGINAL_TESTS), 2)
        for name, expected in v.ORIGINAL_TESTS.items():
            self.assertEqual(v.digest((ROOT / v.retained_name(name)).read_bytes()), expected)
        self.assertEqual(v.retained_name("tests/test_photo_camera_guidance_v36.py"),
                         "tests/test_photo_camera_guidance_v36.py")


class HistoricalImportTests(unittest.TestCase):
    def test_changed_live_inherited_test_cannot_replace_projected_original(self):
        name = "tests/test_photo_nape_metadata_boundary_history.py"
        original_history, parent, old_proof = v.parent_context(ROOT)
        expected = parent.payload(name)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "live"
            path = root / name; path.parent.mkdir(parents=True)
            path.write_bytes(expected + b"\nraise RuntimeError('untrusted live test executed')\n")
            target = Path(temporary) / "projected"
            with mock.patch.object(v, "parent_context", return_value=(original_history, parent, old_proof)), \
                    mock.patch.object(v, "_git_context"):
                v.materialize_parent_projection(target, source_root=root, names={name})
            self.assertEqual((target / name).read_bytes(), expected)
            self.assertNotEqual((target / name).read_bytes(), path.read_bytes())

    def test_projected_package_modules_and_path_restore_after_failure(self):
        import tests as package
        name = "test_photo_nape_metadata_boundary_history"
        full_name = "tests." + name
        missing = object()
        prior_module = sys.modules.get(full_name, missing)
        prior_attribute = getattr(package, name, missing)
        prior_validator = sys.modules.get("validate_illustration_assets", missing)
        prior_path = sys.path[:]
        projected, validator = SimpleNamespace(marker="original"), SimpleNamespace(marker="validator")
        with self.assertRaisesRegex(RuntimeError, "controlled"):
            with v._projected_imports(ROOT, {full_name: projected, "validate_illustration_assets": validator}):
                self.assertIs(sys.modules[full_name], projected)
                self.assertIs(getattr(package, name), projected)
                self.assertIs(sys.modules["validate_illustration_assets"], validator)
                raise RuntimeError("controlled")
        self.assertIs(sys.modules.get(full_name, missing), prior_module)
        self.assertIs(getattr(package, name, missing), prior_attribute)
        self.assertIs(sys.modules.get("validate_illustration_assets", missing), prior_validator)
        self.assertEqual(sys.path, prior_path)


class DispatchTests(unittest.TestCase):
    def test_asset_binding_precedes_proof_import_and_execution(self):
        for version in (None, 37, 36, 35, 6):
            with self.subTest(version=version), mock.patch.object(v, "proof_document") as proof, \
                    mock.patch.object(v, "validate_current") as current, mock.patch.object(v, "dispatch_historical") as historical:
                with self.assertRaisesRegex(AssertionError, "asset directory mismatch"):
                    v.dispatch(ROOT / "wrong", source_root=ROOT, baseline_version=version)
                for method in (proof, current, historical): method.assert_not_called()

    def test_latest_default_and_explicit_37_are_current(self):
        for version in (None, 37):
            with self.subTest(version=version), mock.patch.object(v, "validate_current", return_value="sentinel") as current:
                self.assertEqual(v.dispatch(ROOT / v.ASSETS, source_root=ROOT, baseline_version=version), "sentinel")
                current.assert_called_once_with(ROOT / v.ASSETS, source_root=ROOT)

    def test_explicit_history_failure_never_falls_back_to_current(self):
        for version in (6, 35, 36):
            failure = history.HistoricalReplayUnavailable("exact original unavailable")
            with self.subTest(version=version), mock.patch.object(v, "dispatch_historical", side_effect=failure), \
                    mock.patch.object(v, "validate_current") as current:
                with self.assertRaises(history.HistoricalReplayUnavailable) as caught:
                    v.dispatch(ROOT / v.ASSETS, source_root=ROOT, baseline_version=version)
                self.assertIs(caught.exception, failure)
                current.assert_not_called()

    def test_invalid_versions_never_execute_current_or_history(self):
        for version in (False, True, "37", 37.0, 5, 38):
            with self.subTest(version=version), mock.patch.object(v, "validate_current") as current, \
                    mock.patch.object(v, "dispatch_historical") as historical:
                with self.assertRaisesRegex(AssertionError, "Unsupported"):
                    v.dispatch(ROOT / v.ASSETS, source_root=ROOT, baseline_version=version)
                current.assert_not_called(); historical.assert_not_called()


if __name__ == "__main__":
    unittest.main()
