"""Synthetic root-binding controls; no production capture or runtime execution."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

from tests import photo_workflow_boundary_v37 as v


class NamespaceTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(); self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.source, self.target = self.base / "source", self.base / "copy"
        self.root, self.old_root = self.base / "new-root", self.base / "original-root"
        self.capture = {"files": {"data.json": v.digest(b"data")}, "code": {},
                        "environment": {"implementation": "cpython", "python": [3, 12, 14], "unicode": "15.0.0"}}
        cache_raw = b'{"synthetic":"cache"}'
        self.cache_path = "core-slot-index-data/" + v.digest(cache_raw) + ".json"
        self.manifest = {"schema": "photo-runtime-generation/v1", "source": copy.deepcopy(self.capture),
                         "source_fingerprint": v.digest(v.canonical(self.capture)), "algorithm_sha256": "a" * 64,
                         "members": {}, "slot_cache": {"payload": {"path": self.cache_path,
                             "sha256": v.digest(cache_raw), "bytes": len(cache_raw)}}}
        self.record = {"environment": self.capture["environment"], "generation_id": v.digest(v.canonical(self.manifest)),
                       "source_fingerprint": self.manifest["source_fingerprint"], "algorithm_sha256": "a" * 64}
        self.namespace = v.digest(v.canonical({"root": str(self.old_root / v.PHOTO), "mode": "local_current", "remote": ""}))
        self.pointer = {"schema": "photo-runtime-current/v1", "revision": 1,
                        "generation_id": self.record["generation_id"], "source_fingerprint": self.record["source_fingerprint"],
                        "observation": {"root": str(self.old_root / v.PHOTO), "mode": "local_current", "local_epoch": 0}}
        self.pointer_path = "local/" + self.namespace + "/CURRENT.json"
        self.write(self.pointer_path, v.canonical(self.pointer))
        self.write("generations/" + self.record["generation_id"] + "/manifest.json", v.canonical(self.manifest))
        self.write(self.cache_path, cache_raw)
        self.write("receipts/synthetic.json", b'{"request":"separate"}')
        self.runtime = SimpleNamespace(capture_sources=mock.Mock(side_effect=lambda root: (copy.deepcopy(self.capture), None)),
                                       algorithm_hash=mock.Mock(return_value="a" * 64),
                                       SnapshotPublisher=SimpleNamespace(_verify_generation=mock.Mock(return_value=self.manifest)))
        self.enterContext(mock.patch.object(v, "_binding_modules", return_value=(self.runtime, object())))

    def write(self, name, raw):
        path = self.source / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(raw)
        return path

    def bind(self):
        v.bind_runtime_root(self.source, self.target, self.root, self.record)

    def test_binding_checks_capture_and_shares_only_immutable_payloads(self):
        before = {str(p.relative_to(self.source)): p.read_bytes() for p in self.source.rglob("*") if p.is_file()}
        self.bind()
        namespace = v.digest(v.canonical({"root": str(self.root / v.PHOTO), "mode": "local_current", "remote": ""}))
        pointer = json.loads((self.target / "local" / namespace / "CURRENT.json").read_bytes())
        self.assertEqual(pointer["generation_id"], self.record["generation_id"])
        self.assertEqual(pointer["observation"]["root"], str(self.root / v.PHOTO))
        self.assertEqual((self.source / self.cache_path).stat().st_ino, (self.target / self.cache_path).stat().st_ino)
        for name in (self.pointer_path, "receipts/synthetic.json"):
            self.assertNotEqual((self.source / name).stat().st_ino, (self.target / name).stat().st_ino)
        self.assertEqual(before, {str(p.relative_to(self.source)): p.read_bytes() for p in self.source.rglob("*") if p.is_file()})
        self.assertEqual(self.runtime.capture_sources.call_count, 2)
        self.runtime.SnapshotPublisher._verify_generation.assert_called_once()

    def test_wrong_generation_pointer_and_namespace_cannot_rebind(self):
        for field, value in (("generation_id", "b" * 64), ("source_fingerprint", "b" * 64), ("revision", True)):
            pointer = copy.deepcopy(self.pointer); pointer[field] = value
            self.write(self.pointer_path, v.canonical(pointer))
            with self.subTest(field=field), self.assertRaisesRegex(AssertionError, "pointer drift"):
                self.bind()
            self.assertFalse(self.target.exists())
        pointer = copy.deepcopy(self.pointer); pointer["observation"]["root"] = str(self.base / "false-root")
        self.write(self.pointer_path, v.canonical(pointer))
        with self.assertRaisesRegex(AssertionError, "namespace digest drift"):
            self.bind()

    def test_pending_revision_or_epoch_mismatch_cannot_rebind(self):
        for revision in ({"epoch": 0, "editing": "in-progress"}, {"epoch": 1, "editing": None}):
            self.write("local/" + self.namespace + "/SOURCE.json", v.canonical(revision))
            with self.subTest(revision=revision), self.assertRaisesRegex(AssertionError, "source revision|epoch drift"):
                self.bind()
            self.assertFalse(self.target.exists())

    def test_manifest_source_algorithm_cache_and_symlink_fail_before_copy(self):
        self.runtime.capture_sources.side_effect = lambda root: ({"wrong": True}, None)
        with self.assertRaisesRegex(AssertionError, "source/algorithm capture"):
            self.bind()
        self.runtime.capture_sources.side_effect = lambda root: (copy.deepcopy(self.capture), None)
        self.runtime.algorithm_hash.return_value = "b" * 64
        with self.assertRaisesRegex(AssertionError, "source/algorithm capture"):
            self.bind()
        self.runtime.algorithm_hash.return_value = "a" * 64
        cache = self.source / self.cache_path; raw = cache.read_bytes(); cache.write_bytes(b"changed")
        with self.assertRaisesRegex(AssertionError, "cache binding"):
            self.bind()
        cache.write_bytes(raw)
        cache.unlink(); cache.symlink_to(self.source / self.pointer_path)
        with self.assertRaisesRegex(AssertionError, "runtime symlink"):
            self.bind()
        self.assertFalse(self.target.exists())

    def test_post_capture_source_change_is_rejected(self):
        self.runtime.capture_sources.side_effect = [(copy.deepcopy(self.capture), None), ({"changed": True}, None)]
        with self.assertRaisesRegex(AssertionError, "source changed after namespace"):
            self.bind()


if __name__ == "__main__":
    unittest.main()
