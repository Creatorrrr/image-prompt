"""Real-file and process boundaries for optional BM25F and current sources.

Temporary source roots use the maintained corpus. Embedding providers are never
called; structural index refreshes below change only source metadata, not texts.
"""
from __future__ import annotations

import contextlib
import copy
import io
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

from tests import photo_prompt_fixtures as fixtures
import prompt_generator as pg
import generate_photo_prompt as cli
import audit_composed_prompt as auditor
import photo_runtime_sources as runtime
from core_slot_index_storage import CoreSlotIndexStore, atomic_write, canonical_bytes, decode, digest, json_digest
from photo_source_manifest import SourceInventory


class SlotCacheTests(unittest.TestCase):
    def test_v28_frozen_original_statistics_and_unicode_scope(self):
        path = Path(__file__).parent / "fixtures/photo_prompt/runtime_freshness_v1.json"
        expected = decode(path.read_bytes())
        self.assertEqual(pg.build_core_slot_index(canonical_bytes(expected["slot_corpus"]).decode()), expected["full_expected_index"])

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="photo-slot-cache-")
        self.addCleanup(temporary.cleanup)
        self.store = CoreSlotIndexStore(Path(temporary.name))
        self.corpus = canonical_bytes({"prop": [{"id": "a", "en": "blue porcelain cup"},
                                                {"id": "b", "en": "red paper lantern"}]}).decode()
        self.algorithm = runtime.algorithm_hash(pg)
        self.metadata = self.store.create(self.corpus, self.algorithm, pg.build_core_slot_index)

    def test_exact_full_derivation_and_caller_isolation(self):
        index, status = self.store.load(self.metadata, self.corpus, self.algorithm, pg.build_core_slot_index)
        self.assertEqual(status, "hit")
        self.assertEqual(index, pg.build_core_slot_index(self.corpus))
        index["documents"].clear()
        self.assertEqual(self.store.load(self.metadata, self.corpus, self.algorithm, pg.build_core_slot_index)[0], pg.build_core_slot_index(self.corpus))

    def test_missing_truncated_and_rehashed_wrong_statistics_fall_back_cpu_only(self):
        path = self.store.root / self.metadata["payload"]["path"]
        wrong = pg.build_core_slot_index(self.corpus)
        wrong["average_field_lengths"] = {"aliases": 999999}
        with mock.patch.object(pg, "embed_texts_with_gemini", side_effect=AssertionError("no API")):
            for raw in (None, b"{", canonical_bytes(wrong)):
                with self.subTest(raw=raw is None):
                    if path.exists():
                        path.unlink()
                    if raw is not None:
                        atomic_write(path, raw)
                    index, status = self.store.load(self.metadata, self.corpus, self.algorithm, pg.build_core_slot_index)
                    self.assertEqual(status, "fallback")
                    self.assertEqual(index, pg.build_core_slot_index(self.corpus))
        with self.assertRaisesRegex(ValueError, "full source-derived"):
            self.store.create(self.corpus, self.algorithm, pg.build_core_slot_index, proposed=wrong)

    def test_same_id_source_change_and_algorithm_change_reject_old_cache(self):
        edited = self.corpus.replace("blue", "teal")
        for corpus, algorithm in ((edited, self.algorithm), (self.corpus, "1" * 64)):
            index, status = self.store.load(self.metadata, corpus, algorithm, pg.build_core_slot_index)
            self.assertEqual(status, "fallback")
            self.assertEqual(index, pg.build_core_slot_index(corpus))

    def test_old_memory_key_cannot_hide_policy_change(self):
        before = pg._core_slot_index(self.corpus)
        policy = copy.deepcopy(pg.SEMANTIC_BM25F_POLICY)
        policy["k1"] = float(policy["k1"]) + 0.3
        with mock.patch.object(pg, "SEMANTIC_BM25F_POLICY", policy):
            self.assertNotEqual(runtime.algorithm_hash(pg), self.algorithm)
            self.assertEqual(pg._core_slot_index(self.corpus), pg.build_core_slot_index(self.corpus))
            self.assertNotEqual(pg._core_slot_index(self.corpus), before)

    def test_synthetic_corpus_bypasses_live_artifact(self):
        from tests.test_photo_core_retrieval import PhotoCoreRetrievalTests
        data, core, controls = PhotoCoreRetrievalTests().inputs()
        with mock.patch.object(CoreSlotIndexStore, "load", side_effect=AssertionError("synthetic must not load live cache")):
            slots, _, _ = pg.retrieve_core_slots(data, core, controls)
        self.assertEqual([row["entry_id"] for row in slots["prop"]["candidates"]], ["cup"])


class PhotoRuntimeFreshnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix="photo-runtime-boundary-")
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.store = Path(cls.temporary.name) / "store"
        cls.base_provider = runtime.RuntimeSnapshotProvider(store=cls.store)
        cls.base = cls.base_provider.acquire()
        cls.pointer = decode((cls.base_provider.publisher.directory / "CURRENT.json").read_bytes())

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="photo-runtime-source-", dir=self.temporary.name)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        # Runtime-owned immutable files only. Edits use atomic replacement so
        # neither the original checkout nor the sealed template is touched.
        for relative in self.base.manifest["members"]:
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            os.link(self.base.root / relative, target)
        self.provider = runtime.RuntimeSnapshotProvider(self.root, self.store)
        atomic_write(self.provider.publisher.directory / "CURRENT.json", canonical_bytes(self.pointer))

    def write(self, relative, value):
        atomic_write(self.root / relative, canonical_bytes(value))

    def read(self, relative):
        return decode((self.root / relative).read_bytes())

    def change_description(self, *, valid_indexes=True):
        raw = self.read("assets/photo_prompt_tags.json")
        raw["description"] = str(raw.get("description", "")) + " Additional source metadata."
        self.write("assets/photo_prompt_tags.json", raw)
        if valid_indexes:
            data = pg.load_json(self.root / "assets/photo_prompt_tags.json")
            index = self.read("assets/photo_prompt_semantic_index.json")
            index["dictionary_hash"] = pg.dictionary_hash(data)
            self.write("assets/photo_prompt_semantic_index.json", index)

    def inputs(self):
        raw = fixtures.core("A blue porcelain teacup on a rainlit kitchen counter.")
        controls = pg.creative_controls.resolve(raw["source_request"], overrides={"sensual": 0, "fetish": 0, "surreal": 0, "creativity": 1}, seed=7)
        raw["creative_controls_sha256"] = controls["canonical_sha256"]
        core = pg.normalize_authorial_core(raw,
            request_envelope=pg.normalize_request_envelope(fixtures.envelope(raw["source_request"])),
            creative_control_snapshot=controls)
        return core, controls, fixtures.review(core["baseline_prompt_en"])

    def test_unchanged_source_exact_index_retrieval_and_full_pack(self):
        first, second = self.provider.acquire(), self.provider.acquire()
        self.assertIs(first.data, second.data)
        corpus = canonical_bytes(first.data["slots"]).decode()
        self.assertEqual(first.data.slot_index(corpus), pg.build_core_slot_index(corpus))
        core, controls, review = self.inputs()
        original = pg.generate_candidate_pack(copy.deepcopy(first.data), core, controls, review, seed=7)
        actual = pg.generate_candidate_pack(first.data, core, controls, review, seed=7)
        self.assertEqual(canonical_bytes(actual), canonical_bytes(original))
        self.assertEqual(auditor.audit_core_retrieval(actual, first.data), [])
        receipt = self.provider.receipt(first, actual)
        independent = self.provider.from_receipt(actual, receipt)
        self.assertEqual(independent.cache_status, "independent_audit")

    def test_preserved_mtime_and_size_edit_is_detected(self):
        path = self.root / "assets/photo_prompt_tags.json"
        before, _ = runtime.capture_sources(self.root)
        stat = path.stat()
        raw = path.read_bytes()
        self.assertIn(b'"description"', raw)
        changed = raw.replace(b"Photographic", b"photographic", 1)
        if changed == raw:
            changed = raw.replace(b"photo", b"Photo", 1)
        self.assertNotEqual(changed, raw)
        self.assertEqual(len(changed), len(raw))
        atomic_write(path, changed)
        os.utime(path, ns=(stat.st_atime_ns, stat.st_mtime_ns))
        after, _ = runtime.capture_sources(self.root)
        self.assertNotEqual(before, after)
        with self.assertRaisesRegex(runtime.FreshnessError, "source_revision_pending"):
            self.provider.acquire()

    def test_optional_presence_registration_and_missing_required_are_checked(self):
        source = self.read("assets/photo_prompt_source_manifest.json")
        rows = [row for row in source["sources"] if row["kind"] == "candidate"]
        source["sources"].append({"file": "photo_prompt_test_extension.json", "kind": "candidate", "required": False, "load_order": len(rows)})
        self.write("assets/photo_prompt_source_manifest.json", source)
        before, _ = runtime.capture_sources(self.root)
        self.write("assets/photo_prompt_test_extension.json", {})
        after, _ = runtime.capture_sources(self.root)
        self.assertNotEqual(before, after)
        self.write("assets/photo_prompt_unregistered_extension.json", {})
        with self.assertRaisesRegex(runtime.FreshnessError, "unregistered"):
            runtime.capture_sources(self.root)
        (self.root / "assets/photo_prompt_unregistered_extension.json").unlink()
        (self.root / "assets" / next(row["file"] for row in rows if row["required"])).unlink()
        with self.assertRaisesRegex(runtime.FreshnessError, "required"):
            runtime.capture_sources(self.root)

    def test_alternate_source_roots_use_one_explicit_inventory(self):
        manifest = self.read("assets/photo_prompt_source_manifest.json")
        manifest["sources"].append({"file": "photo_prompt_other_extension.json", "kind": "candidate", "required": True,
                                   "load_order": len([row for row in manifest["sources"] if row["kind"] == "candidate"])})
        self.write("assets/photo_prompt_source_manifest.json", manifest)
        self.write("assets/photo_prompt_other_extension.json", {"schema_version": pg.RESEARCH_EXTENSION_SCHEMA, "slots": {}})
        inventory = SourceInventory.load(self.root / "assets")
        # Bundle-reference loading must receive this inventory too.
        with mock.patch.object(pg, "load_visual_obligation_registry", wraps=pg.load_visual_obligation_registry) as load:
            data = pg.load_json(self.root / "assets/photo_prompt_tags.json", inventory=inventory)
        self.assertIn("photo_prompt_other_extension.json", data["candidate_semantic_policy"]["required_extensions"])
        self.assertNotIn("photo_prompt_other_extension.json", SourceInventory.load(runtime.SKILL_ROOT / "assets").required("candidate"))
        self.assertTrue(load.called)
        self.assertTrue(all(call.kwargs["inventory"] is inventory for call in load.call_args_list))
        with self.assertRaisesRegex(ValueError, "different assets"):
            pg.load_json(self.root / "assets/photo_prompt_tags.json", inventory=SourceInventory.load(runtime.SKILL_ROOT / "assets"))
        with self.assertRaisesRegex(ValueError, "different assets"):
            pg.load_runtime_data(self.root / "assets/photo_prompt_tags.json", inventory=SourceInventory.for_test(Path("/different")))

    def test_changed_source_with_stale_required_index_never_uses_old_snapshot(self):
        old = self.provider.acquire()
        raw = self.read("assets/photo_prompt_tags.json")
        entry = next(rows[0] for rows in raw["slots"].values() if rows)
        unchanged_id = entry["id"]
        entry["en"] = str(entry["en"]) + " visibly altered surface"
        self.write("assets/photo_prompt_tags.json", raw)
        self.assertEqual(entry["id"], unchanged_id)
        with self.assertRaisesRegex(runtime.FreshnessError, "source_invalid"):
            self.provider.publisher.publish()
        with self.assertRaisesRegex(runtime.FreshnessError, "source_revision_pending"):
            self.provider.acquire()
        self.assertEqual(old.generation_id, self.base.generation_id)
        self.assertEqual(decode((self.provider.publisher.directory / "CURRENT.json").read_bytes()), self.pointer)

    def test_data_reload_and_inflight_pack_audit_stay_pinned(self):
        old = self.provider.acquire()
        core, controls, review = self.inputs()
        pack = pg.generate_candidate_pack(old.data, core, controls, review, seed=7)
        receipt = self.provider.receipt(old, pack)
        self.change_description()
        pointer = self.provider.publisher.publish()
        new = self.provider.acquire()
        self.assertEqual(new.generation_id, pointer["generation_id"])
        self.assertNotEqual(new.generation_id, old.generation_id)
        self.assertEqual(old.manifest["slot_cache"]["payload"], new.manifest["slot_cache"]["payload"])
        new_pack = pg.generate_candidate_pack(new.data, core, controls, review, seed=7)
        self.provider.receipt(new, new_pack)
        if new_pack == pack:
            with self.assertRaisesRegex(runtime.FreshnessError, "ambiguous runtime receipt"):
                self.provider.from_receipt(pack)
        self.assertEqual(pg.generate_candidate_pack(old.data, core, controls, review, seed=7), pack)
        # New publication cannot change an already acquired observation.
        retained = self.provider.receipt(old, pack)
        self.assertEqual(retained["observation"], receipt["observation"])
        audited = self.provider.from_receipt(pack, receipt)
        self.assertEqual(audited.generation_id, old.generation_id)
        self.assertEqual(auditor.audit_core_retrieval(pack, audited.data), [])

    def test_visual_only_generation_reuses_slot_payload(self):
        old = self.provider.acquire()
        raw = self.read("assets/photo_prompt_visual_obligations.json")
        raw["description"] = str(raw.get("description", "")) + " Registry metadata update."
        self.write("assets/photo_prompt_visual_obligations.json", raw)
        registry = pg.load_visual_obligation_registry(self.root / "assets/photo_prompt_visual_obligations.json")
        index = self.read("assets/photo_prompt_visual_profile_index.json")
        index["registry_sha256"] = pg.visual_profile_registry_sha256(registry)
        self.write("assets/photo_prompt_visual_profile_index.json", index)
        self.provider.publisher.publish()
        new = self.provider.acquire()
        self.assertNotEqual(new.generation_id, old.generation_id)
        self.assertEqual(new.manifest["slot_cache"], old.manifest["slot_cache"])

    def test_optional_cache_corruption_uses_same_validated_generation(self):
        metadata = self.base.manifest["slot_cache"]
        path = self.store / metadata["payload"]["path"]
        original = path.read_bytes()
        self.addCleanup(atomic_write, path, original)
        atomic_write(path, b"{truncated")
        with mock.patch.object(pg, "embed_texts_with_gemini", side_effect=AssertionError("no embedding API")):
            snapshot = self.provider.acquire()
        self.assertEqual(snapshot.generation_id, self.base.generation_id)
        self.assertEqual(snapshot.cache_status, "fallback")
        corpus = canonical_bytes(snapshot.data["slots"]).decode()
        self.assertEqual(snapshot.data.slot_index(corpus), pg.build_core_slot_index(corpus))

    def test_wrong_statistics_with_rewritten_self_metadata_cannot_replace_expectations(self):
        wrong = pg.build_core_slot_index(canonical_bytes(self.base.data["slots"]).decode())
        wrong["average_field_lengths"] = {"aliases": 999999}
        with self.assertRaisesRegex(runtime.FreshnessError, "full source-derived"):
            self.provider.publisher.publish(proposed_slot_index=wrong)
        self.assertEqual(decode((self.provider.publisher.directory / "CURRENT.json").read_bytes()), self.pointer)

    def test_partial_publication_and_source_race_do_not_switch_current(self):
        self.change_description()
        def fail():
            raise RuntimeError("injected interruption before CURRENT")
        with self.assertRaisesRegex(RuntimeError, "injected"):
            self.provider.publisher.publish(before_publish=fail)
        self.assertEqual(decode((self.provider.publisher.directory / "CURRENT.json").read_bytes()), self.pointer)
        with self.assertRaisesRegex(runtime.FreshnessError, "source_revision_pending"):
            self.provider.publisher.publish(before_publish=lambda: self.change_description())
        self.assertEqual(decode((self.provider.publisher.directory / "CURRENT.json").read_bytes()), self.pointer)

    def test_new_generation_member_failure_does_not_assign_old_handle(self):
        old = self.provider.acquire()
        self.change_description()
        pointer = self.provider.publisher.publish()
        new_root = self.store / "generations" / pointer["generation_id"]
        path = new_root / "assets/photo_prompt_tags.json"
        original = path.read_bytes()
        self.addCleanup(atomic_write, path, original)
        atomic_write(path, b"{}")
        with self.assertRaisesRegex(runtime.FreshnessError, "checksum mismatch"):
            self.provider.acquire()
        self.assertEqual(old.generation_id, self.base.generation_id)

    def test_current_cannot_relabel_an_old_generation_as_the_new_source(self):
        self.provider.acquire()
        self.change_description()
        self.provider.publisher.publish()
        path = self.provider.publisher.directory / "CURRENT.json"
        current = decode(path.read_bytes())
        current["generation_id"] = self.base.generation_id
        atomic_write(path, canonical_bytes(current))
        with self.assertRaisesRegex(runtime.FreshnessError, "observed source binding"):
            self.provider.acquire()
        current["generation_id"] = "../foreign-generation"
        atomic_write(path, canonical_bytes(current))
        with self.assertRaisesRegex(runtime.FreshnessError, "invalid CURRENT"):
            self.provider.acquire()

    def test_imported_old_code_and_changed_policy_require_new_worker(self):
        self.provider.acquire()
        policy = copy.deepcopy(pg.SEMANTIC_BM25F_POLICY)
        policy["k1"] = float(policy["k1"]) + 0.3
        with mock.patch.object(pg, "SEMANTIC_BM25F_POLICY", policy):
            with self.assertRaisesRegex(runtime.FreshnessError, "runtime_restart_required"):
                self.provider.acquire()
        path = self.root / "scripts/bm25f_retrieval.py"
        atomic_write(path, path.read_bytes() + b"\n# changed implementation\n")
        with self.assertRaisesRegex(runtime.FreshnessError, "runtime_restart_required"):
            self.provider.acquire()
        with mock.patch.object(runtime.unicodedata, "unidata_version", "different"):
            with self.assertRaisesRegex(runtime.FreshnessError, "runtime_restart_required"):
                runtime._require_implementation({"code": runtime.LOADED_CODE, "environment": runtime.environment_binding()}, pg)

    def test_snapshot_mutation_fails_and_explicit_copies_remain_isolated(self):
        snapshot = self.provider.acquire()
        entry = next(iter(snapshot.data["slots"].values()))[0]
        with self.assertRaisesRegex(runtime.FreshnessError, "snapshot object mutation"):
            entry["en"] = "replacement"
        with self.assertRaisesRegex(runtime.FreshnessError, "snapshot object mutation"):
            snapshot.data["slots"].clear()
        copy_data = copy.deepcopy(snapshot.data)
        copy_data["slots"].clear()
        self.assertTrue(snapshot.data["slots"])

    def test_receipt_pack_mismatch_and_missing_receipt_fail(self):
        snapshot = self.provider.acquire()
        core, controls, review = self.inputs()
        pack = pg.generate_candidate_pack(snapshot.data, core, controls, review, seed=7)
        receipt = self.provider.receipt(snapshot, pack)
        wrong = copy.deepcopy(pack)
        wrong["provenance"]["seed"] = 8
        with self.assertRaisesRegex(runtime.FreshnessError, "receipt/pack"):
            self.provider.from_receipt(wrong, receipt)
        with self.assertRaisesRegex(runtime.FreshnessError, "missing runtime receipt"):
            self.provider.from_receipt(wrong)

    def test_cooperative_writer_epoch_blocks_unfinished_publication(self):
        with runtime.source_update(self.root, self.store):
            with self.assertRaisesRegex(runtime.FreshnessError, "unfinished"):
                self.provider.acquire()
            with self.assertRaisesRegex(runtime.FreshnessError, "unfinished"):
                self.provider.publisher.publish()
        self.assertEqual(self.provider.acquire().generation_id, self.base.generation_id)

    def test_late_old_publisher_two_processes_cannot_overwrite_new_current(self):
        ready, resume = self.root / "READY", self.root / "RESUME"
        code = '''
import sys, time
from pathlib import Path
from photo_runtime_sources import SnapshotPublisher, FreshnessError
root, store, ready, resume = map(Path, sys.argv[1:])
def barrier():
    ready.write_text("captured")
    deadline = time.monotonic() + 180
    while not resume.exists():
        if time.monotonic() > deadline: raise RuntimeError("barrier timeout")
        time.sleep(0.05)
try:
    SnapshotPublisher(root, store).publish(before_publish=barrier)
except FreshnessError as exc:
    print(exc.state)
    sys.exit(3)
'''
        env = {**os.environ, "PYTHONPATH": str(fixtures.SCRIPT_DIR), "PYTHONDONTWRITEBYTECODE": "1"}
        process = subprocess.Popen([sys.executable, "-c", code, str(self.root), str(self.store), str(ready), str(resume)], env=env,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.addCleanup(lambda: process.kill() if process.poll() is None else None)
        deadline = time.monotonic() + 180
        while not ready.exists():
            if process.poll() is not None or time.monotonic() > deadline:
                out, err = process.communicate(timeout=5)
                self.fail(f"publisher never reached barrier: {out} {err}")
            time.sleep(0.05)
        self.change_description()
        current = self.provider.publisher.publish()
        resume.write_text("go")
        out, err = process.communicate(timeout=60)
        self.assertEqual(process.returncode, 3, out + err)
        self.assertIn("source_revision_pending", out)
        self.assertEqual(decode((self.provider.publisher.directory / "CURRENT.json").read_bytes()), current)


class PhotoPrecoreFreshnessTests(unittest.TestCase):
    def test_invalid_authored_inputs_never_load_sources_or_fetch(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            envelope = root / "request.json"
            envelope.write_text("{}")
            args = ["--request-envelope-json", str(envelope), "--authorial-core-json", "unused", "--creative-controls-json", "unused",
                    "--embodiment-review-json", "unused", "--source-mode", "remote_before_retrieval", "--source-remote", "invalid"]
            with mock.patch.object(runtime.RuntimeSnapshotProvider, "acquire", side_effect=AssertionError("pre-core source access")), \
                    mock.patch.object(runtime.RemoteSourceUpdater, "fetch", side_effect=AssertionError("pre-core fetch")):
                with self.assertRaises(ValueError):
                    cli.main(args)


class RemoteSourceUpdaterTests(unittest.TestCase):
    def test_actual_fetch_commit_dirty_primary_and_network_failure(self):
        with tempfile.TemporaryDirectory(prefix="photo-remote-boundary-") as temp:
            root = Path(temp)
            primary = root / "primary"
            primary.mkdir()
            def git(*args):
                return subprocess.run(["git", "-C", str(primary), *args], check=True, capture_output=True, text=True).stdout.strip()
            git("init", "-b", "main")
            skill = primary / "skills/photo-prompt-image-generator"
            skill.mkdir(parents=True)
            (skill / "data").write_text("first")
            git("add", ".")
            git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "first")
            first = git("rev-parse", "HEAD")
            (primary / "untracked-research").write_text("keep")
            (skill / "data").write_text("dirty")
            before = git("status", "--porcelain")
            updater = runtime.RemoteSourceUpdater(root / "store", str(primary))
            checkout, observation = updater.fetch()
            self.assertEqual(observation["commit"], first)
            self.assertEqual((checkout / "data").read_text(), "first")
            self.assertEqual(git("status", "--porcelain"), before)
            git("add", "skills")
            git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "second")
            second = git("rev-parse", "HEAD")
            new_checkout, new_observation = updater.fetch()
            self.assertEqual(new_observation["commit"], second)
            self.assertNotEqual(new_checkout, checkout)
            self.assertEqual(observation["commit"], first)
            self.assertEqual((checkout / "data").read_text(), "first")
            primary.rename(root / "unavailable")
            with self.assertRaisesRegex(runtime.FreshnessError, "remote_unverified"):
                updater.fetch()


if __name__ == "__main__":
    unittest.main()
