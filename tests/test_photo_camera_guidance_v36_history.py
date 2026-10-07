"""Negative controls for exact local V35 recovery; no pack/provider execution."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from tests import photo_camera_guidance_history_v36 as history

ROOT = Path(__file__).resolve().parents[1]


class AuthenticatedRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.git("init", "-q")
        self.contents = {
            "source/runtime.py": b"original = True\n",
            "history/proof.json": b'{"schema":"frozen","meaning":"original"}\n',
            "history/frozen-core.json": b'{"subject":"original subject"}\n',
            "history/pack.json": b'[{"negative_en":"frozen negative"}]\n',
            "tests/original_test.py": b"assert True\n",
            "tests/test_photo_character_response_concepts.py": b"assert 'original'\n",
        }
        for name, raw in self.contents.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
            path.chmod(0o644)
        (self.root / "tests/original_test.py").chmod(0o755)
        self.git("add", ".")
        self.tree = self.git("write-tree").strip()
        self.commit = self.git("commit-tree", self.tree, input="Original fixture\n").strip()
        self.snapshot = history.GitSnapshot(self.root, self.commit, self.tree)
        # Exercise resolver primitives against an actual isolated Git object
        # database. Production ExactV35Sources always uses the fixed 8c pin.
        self.resolver = object.__new__(history.ExactV35Sources)
        self.resolver.root = self.root
        self.resolver.original = self.snapshot
        self.resolver.proof = {"source_files_after": {
            "source/runtime.py": history.digest(self.contents["source/runtime.py"])
        }}

    def git(self, *args, input=None):
        env = os.environ.copy()
        env.update(GIT_AUTHOR_NAME="Recovery test", GIT_AUTHOR_EMAIL="recovery@example.invalid",
                   GIT_COMMITTER_NAME="Recovery test", GIT_COMMITTER_EMAIL="recovery@example.invalid",
                   GIT_AUTHOR_DATE="2026-10-07T00:00:00+0000", GIT_COMMITTER_DATE="2026-10-07T00:00:00+0000")
        return subprocess.check_output(["git", *args], cwd=self.root, input=input, text=True, env=env)

    def test_original_source_is_not_replaced_by_live_successor(self):
        name = "source/runtime.py"
        (self.root / name).write_bytes(b"original = False\n")
        self.git("add", ".")
        current_tree = self.git("write-tree").strip()
        self.assertNotEqual(current_tree, self.tree)
        self.assertEqual(self.resolver.original_payload(name), self.contents[name])

    def test_live_tampering_is_rejected_despite_an_available_exact_original(self):
        name = "source/runtime.py"
        expected = history.digest(self.contents[name])
        history.require_live_payload(self.root, name, expected, "100644")
        (self.root / name).write_bytes(b"tampered = True\n")
        with self.assertRaisesRegex(AssertionError, "live source payload"):
            history.require_live_payload(self.root, name, expected, "100644")
        self.assertEqual(self.resolver.original_payload(name), self.contents[name])

    def test_live_mode_changes_and_symlinks_are_rejected(self):
        name = "source/runtime.py"
        path = self.root / name
        expected = history.digest(self.contents[name])
        path.chmod(0o755)
        with self.assertRaisesRegex(AssertionError, "mode drift"):
            history.require_live_payload(self.root, name, expected, "100644")
        path.unlink()
        path.symlink_to(self.root / "tests/original_test.py")
        with self.assertRaisesRegex(AssertionError, "symlink"):
            history.require_live_payload(self.root, name, expected, "100644")

    def test_retained_proof_frozen_input_and_pack_cannot_be_rehashed_or_replaced(self):
        for name in ("history/proof.json", "history/frozen-core.json", "history/pack.json"):
            with self.subTest(name=name):
                original = self.contents[name]
                changed = original.replace(b"original", b"tampered").replace(b"frozen negative", b"new negative")
                path = self.root / name
                path.write_bytes(changed)
                with self.assertRaisesRegex(AssertionError, "retained payload"):
                    self.resolver.retained_payload(name, history.digest(original))
                with self.assertRaisesRegex(AssertionError, "original source SHA256"):
                    self.resolver.retained_payload(name, history.digest(changed))
                path.write_bytes(original)

    def test_sparse_absence_can_recover_but_present_bad_mode_cannot(self):
        name = "tests/original_test.py"
        path = self.root / name
        path.unlink()
        self.assertEqual(self.resolver.retained_payload(name), self.contents[name])
        path.write_bytes(self.contents[name])
        path.chmod(0o644)
        self.assertEqual(self.snapshot.entry(name)["mode"], "100755")
        with self.assertRaisesRegex(AssertionError, "mode drift"):
            self.resolver.retained_payload(name)

    def test_approved_upstream_current_test_keeps_its_original_replay_bytes(self):
        name = "tests/test_photo_character_response_concepts.py"
        path = self.root / name
        path.write_bytes(b"assert 'approved upstream'\n")
        self.git("add", ".")
        current_tree = self.git("write-tree").strip()
        current_commit = self.git("commit-tree", current_tree, input="Approved upstream fixture\n").strip()
        with mock.patch.object(history, "UPSTREAM_PIN", current_commit):
            self.assertEqual(self.resolver.retained_test_payload(name), self.contents[name])
            path.write_bytes(b"assert 'unapproved change'\n")
            with self.assertRaisesRegex(AssertionError, "live source payload"):
                self.resolver.retained_test_payload(name)

    def test_missing_original_blob_blocks_even_when_live_file_is_available(self):
        name = "source/runtime.py"
        oid = self.snapshot.entry(name)["git_blob"]
        (self.root / ".git/objects" / oid[:2] / oid[2:]).unlink()
        with self.assertRaisesRegex(history.HistoricalReplayUnavailable, "local Git object unavailable"):
            self.resolver.original_payload(name)
        self.assertTrue((self.root / name).is_file())

    def test_original_blob_payload_is_authenticated_independently(self):
        oid = self.snapshot.entry("source/runtime.py")["git_blob"]
        with mock.patch.object(self.snapshot, "git", return_value=b"modified original\n"):
            with self.assertRaisesRegex(AssertionError, "Git object payload drift"):
                self.snapshot.object("blob", oid)

    def test_commit_tree_binding_cannot_be_rebound(self):
        with self.assertRaisesRegex(AssertionError, "commit/tree identity"):
            history.GitSnapshot(self.root, self.commit, "0" * 40)

    def test_git_replace_refs_cannot_redirect_original_bytes(self):
        name = "source/runtime.py"
        oid = self.snapshot.entry(name)["git_blob"]
        alternate = self.git("hash-object", "-w", "--stdin", input="replacement\n").strip()
        self.git("replace", oid, alternate)
        self.assertEqual(self.snapshot.payload(name), self.contents[name])

    def test_path_traversal_and_symlink_ancestor_are_rejected(self):
        for name in (".", "../outside", "/absolute", "source//runtime.py", "source/./runtime.py", ".git/config"):
            with self.subTest(name=name), self.assertRaisesRegex(AssertionError, "Unsafe"):
                self.snapshot.entry(name)
        (self.root / "linked").symlink_to(self.root / "history", target_is_directory=True)
        with self.assertRaisesRegex(AssertionError, "symlink"):
            history._regular(self.root, "linked/proof.json")
        (self.root / "blocked").write_bytes(b"directory replaced by a file")
        with self.assertRaisesRegex(AssertionError, "ancestor is not a directory"):
            history._regular(self.root, "blocked/proof.json", optional=True)

    def test_successor_inventory_cannot_drop_old_or_new_sources(self):
        with self.assertRaisesRegex(AssertionError, "all 156 bound paths"):
            self.resolver.verify_live_sources(self.resolver.proof["source_files_after"])

    def test_each_new_grammar_and_runtime_source_is_required(self):
        sources = set(self.resolver.proof["source_files_after"]) | history.NEW_SOURCE_PATHS
        for missing in sorted(history.NEW_SOURCE_PATHS):
            partial = {name: "0" * 64 for name in sources - {missing}}
            with self.subTest(missing=missing), self.assertRaisesRegex(AssertionError, "all 156 bound paths"):
                self.resolver.verify_live_sources(partial)

    def test_added_only_latest_test_cannot_replace_an_original_test(self):
        name = "tests/test_photo_visual_grammar_integration.py"
        path = self.root / name
        path.write_bytes(b"assert 'latest only'\n")
        with self.assertRaisesRegex(history.HistoricalReplayUnavailable, "absent from exact historical tree"):
            self.resolver.retained_test_payload(name)

    def test_runtime_mismatch_is_an_explicit_blocker(self):
        expected = {"implementation": "cpython", "python": [0, 0, 0], "unicode": "unavailable"}
        with self.assertRaisesRegex(history.HistoricalReplayUnavailable, "environment unavailable"):
            history.require_original_environment(expected, sys.executable)

    def test_dispatch_stops_before_materialization_or_runtime_store_on_environment_blocker(self):
        resolver = mock.Mock()
        resolver.parent = {"environment": {
            "implementation": "cpython", "python": [0, 0, 0], "unicode": "unavailable"
        }}
        with mock.patch.object(history, "ExactV35Sources", return_value=resolver), \
                mock.patch.object(history.tempfile, "TemporaryDirectory", side_effect=AssertionError("unexpected replay write")):
            with self.assertRaisesRegex(history.HistoricalReplayUnavailable, "environment unavailable"):
                history.dispatch_historical(self.root / history.ASSETS, source_root=self.root,
                                            baseline_version=35, source_files_after={})
        resolver.materialize_original.assert_not_called()

    def test_unsupported_versions_are_not_silently_dispatched(self):
        for version in (True, 1, 5, 36, "35"):
            with self.subTest(version=version), self.assertRaisesRegex(AssertionError, "Unsupported"):
                history.dispatch_historical(self.root / history.ASSETS, source_root=self.root,
                                            baseline_version=version, source_files_after={})

    def test_test_module_replay_rejects_arbitrary_commands(self):
        for module in ("os", "tests.test_x --help", "tests/../other", "tests.test_x; echo unsafe"):
            with self.subTest(module=module), self.assertRaisesRegex(AssertionError, "Original test module"):
                history.replay_original_tests(self.root, test_module=module, source_files_after={})

    def test_original_test_replay_keeps_the_same_environment_blocker(self):
        resolver = mock.Mock()
        resolver.parent = {"environment": {
            "implementation": "cpython", "python": [0, 0, 0], "unicode": "unavailable"
        }}
        with mock.patch.object(history, "ExactV35Sources", return_value=resolver), \
                mock.patch.object(history.tempfile, "TemporaryDirectory", side_effect=AssertionError("unexpected replay write")):
            with self.assertRaisesRegex(history.HistoricalReplayUnavailable, "environment unavailable"):
                history.replay_original_tests(self.root, test_module="tests.test_original", source_files_after={})
        resolver.original.payload.assert_called_once_with("tests/test_original.py")
        resolver.materialize_original.assert_not_called()


class PinnedV35IdentityTests(unittest.TestCase):
    def test_exact_original_proof_and_validator_are_locally_authentic(self):
        original = history.ExactV35Sources(ROOT)
        self.assertEqual(len(original.proof["source_files_after"]), 152)
        self.assertEqual(history.digest(original.original.payload(history.VALIDATOR)), history.VALIDATOR_SHA256)
        self.assertEqual(original.parent["environment"], {
            "implementation": "cpython", "python": [3, 14, 3], "unicode": "16.0.0"
        })

    def test_latest_scope_preserves_original_sources_and_requires_four_additions(self):
        original = history.ExactV35Sources(ROOT)
        upstream = history.GitSnapshot(ROOT, history.UPSTREAM_PIN)
        self.assertEqual(history.UPSTREAM_PIN, "4f3d524ed035de8592e4b0c6ad5030b41ffc55af")
        self.assertEqual(len(set(original.proof["source_files_after"]) | history.NEW_SOURCE_PATHS), 156)
        self.assertEqual(len(history.NEW_SOURCE_PATHS), 4)
        for name in history.NEW_SOURCE_PATHS:
            with self.subTest(name=name):
                self.assertEqual(upstream.entry(name)["mode"], "100644")
                with self.assertRaisesRegex(history.HistoricalReplayUnavailable, "absent from exact historical tree"):
                    original.original.entry(name)

    def test_latest_approved_test_changes_are_exact_and_keep_original_bytes(self):
        original = history.ExactV35Sources(ROOT)
        upstream = history.GitSnapshot(ROOT, history.UPSTREAM_PIN)
        changed = {
            name for name in original.original.paths("tests")
            if original.original.entry(name) != upstream.entry(name)
        }
        self.assertEqual(changed, history.UPSTREAM_TEST_CHANGES)
        self.assertEqual(len(changed), 15)
        for name in sorted(changed):
            with self.subTest(name=name):
                self.assertEqual(original.retained_test_payload(name), original.original.payload(name))
                self.assertNotEqual(original.original.payload(name), upstream.payload(name))


if __name__ == "__main__":
    unittest.main()
