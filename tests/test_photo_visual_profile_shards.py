"""Offline contracts for visual-index storage and incremental vector reuse."""
from __future__ import annotations

import copy
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import build_visual_profile_index as builder  # noqa: E402
import prompt_generator as generator  # noqa: E402
import visual_profile_index_storage as storage  # noqa: E402


def encoded(payload):
    return (json.dumps(payload, ensure_ascii=False, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


class PhotoVisualProfileShardTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="visual-shards-test-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.path = self.root / "assets" / "visual_index.json"
        self.path.parent.mkdir()
        self.payload = {
            "schema_version": "test-index/v1",
            "provider": "test-provider",
            "embedding_model": "test-model",
            "embedding_dimensions": 4,
            "retrieval_policy": {"minimum_similarity": 0.7, "candidate_limit": 8},
            "exact_lookup": [{"term": "풍경", "profile_id": "profile-17"}],
            "bm25f": {"documents": {"z": {"terms": ["풍경", "café"]}, "a": {"terms": []}}},
            "entries": {
                f"profile-{index}": {
                    "text": f"풍경 café {index}",
                    "text_sha256": hashlib.sha256(f"풍경 café {index}".encode()).hexdigest(),
                    "vector": [-0.0, 0.12345678901234568, -1e-20, float(index)],
                }
                for index in reversed(range(24))
            },
        }

    def write(self, payload=None, count=4):
        return storage.write_sharded_visual_profile_index(self.path, payload or self.payload, shard_count=count)

    def save_manifest(self, manifest):
        self.path.write_bytes(encoded(manifest))

    def read_shard(self, manifest, index):
        return json.loads((self.path.parent / manifest["shards"][index]["path"]).read_bytes())

    def replace_shard(self, manifest, index, shard=None, raw=None):
        """Recompute checksum so structural corruption reaches its own validator."""
        row = manifest["shards"][index]
        raw = encoded(shard) if raw is None else raw
        (self.path.parent / row["path"]).write_bytes(raw)
        row["sha256"] = hashlib.sha256(raw).hexdigest()
        if shard is not None:
            row["entry_count"] = len(shard["entries"])
        self.save_manifest(manifest)

    def test_round_trip_preserves_every_value_and_nested_insertion_order(self):
        before = encoded(self.payload)
        manifest = self.write()
        result = storage.load_visual_profile_index_payload(self.path)
        self.assertEqual(encoded(result), before)
        self.assertEqual(encoded(self.payload), before, "writer mutated input")
        self.assertEqual(list(result["entries"]), list(self.payload["entries"]))
        self.assertEqual(manifest["entry_order"], list(self.payload["entries"]))
        self.assertEqual(manifest["storage"]["format"], storage.FORMAT)
        self.assertNotIn("entries", manifest)
        for index, row in enumerate(manifest["shards"]):
            raw = (self.path.parent / row["path"]).read_bytes()
            self.assertEqual(row["sha256"], hashlib.sha256(raw).hexdigest())
            part = json.loads(raw)["entries"]
            expected = [key for key in self.payload["entries"] if int(hashlib.sha256(key.encode()).hexdigest(), 16) % 4 == index]
            self.assertEqual(list(part), expected)
            self.assertEqual(row["entry_count"], len(expected))

    def test_repeat_write_is_byte_identical_and_does_not_rewrite_files(self):
        self.write()
        paths = sorted(path for path in self.path.parent.rglob("*") if path.is_file())
        before = {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in paths}
        with mock.patch.object(storage.Path, "replace", side_effect=AssertionError("unchanged content was rewritten")):
            self.write()
        self.assertEqual(before, {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in paths})
        other = self.root / "independent-install" / self.path.name
        storage.write_sharded_visual_profile_index(other, self.payload, shard_count=4)
        self.assertEqual(other.read_bytes(), self.path.read_bytes())
        for row in json.loads(other.read_bytes())["shards"]:
            self.assertEqual((other.parent / row["path"]).read_bytes(), (self.path.parent / row["path"]).read_bytes())

    def test_one_entry_mutation_changes_only_its_shard_and_retains_old_snapshot(self):
        first = self.write()
        old_manifest = self.path.read_bytes()
        old_shards = {row["path"]: (self.path.parent / row["path"]).read_bytes() for row in first["shards"]}
        changed = copy.deepcopy(self.payload)
        changed["entries"]["profile-17"]["vector"][1] = 0.25
        second = self.write(changed)
        changed_ids = [old["id"] for old, new in zip(first["shards"], second["shards"]) if old != new]
        expected = int(hashlib.sha256(b"profile-17").hexdigest(), 16) % 4
        self.assertEqual(changed_ids, [f"{expected:03d}"])
        self.assertEqual(encoded(storage.load_visual_profile_index_payload(self.path)), encoded(changed))
        for relative, raw in old_shards.items():
            self.assertEqual((self.path.parent / relative).read_bytes(), raw)
        old_snapshot = self.path.with_name("old_snapshot.json")
        old_snapshot.write_bytes(old_manifest)
        self.assertEqual(encoded(storage.load_visual_profile_index_payload(old_snapshot)), encoded(self.payload))

    def test_manifest_is_published_only_after_all_shards_are_written(self):
        self.write()
        old_manifest = self.path.read_bytes()
        changed = copy.deepcopy(self.payload)
        changed["entries"]["profile-17"]["vector"][0] = 1.0
        write = storage._write
        def interrupted(path, raw):
            if Path(path) == self.path:
                raise OSError("simulated interruption before manifest publication")
            return write(path, raw)
        with mock.patch.object(storage, "_write", side_effect=interrupted):
            with self.assertRaisesRegex(OSError, "simulated interruption"):
                self.write(changed)
        self.assertEqual(self.path.read_bytes(), old_manifest)
        self.assertEqual(encoded(storage.load_visual_profile_index_payload(self.path)), encoded(self.payload))

    def test_legacy_json_still_loads_without_modification(self):
        self.path.write_text(json.dumps(self.payload, ensure_ascii=False, indent=2), encoding="utf-8")
        original = self.path.read_bytes()
        self.assertEqual(encoded(storage.load_visual_profile_index_payload(self.path)), encoded(self.payload))
        self.assertEqual(self.path.read_bytes(), original)

    def test_empty_entries_and_empty_shards_round_trip(self):
        for count in (1, 4, 32):
            with self.subTest(count=count):
                payload = copy.deepcopy(self.payload)
                payload["entries"] = {}
                self.write(payload, count=count)
                self.assertEqual(storage.load_visual_profile_index_payload(self.path), payload)

    def test_rejects_corrupt_or_missing_shard(self):
        for kind in ("corrupt", "missing"):
            with self.subTest(kind=kind):
                manifest = self.write()
                path = self.path.parent / manifest["shards"][0]["path"]
                if kind == "corrupt":
                    path.write_bytes(path.read_bytes() + b" ")
                    error = ValueError
                else:
                    path.unlink()
                    error = FileNotFoundError
                with self.assertRaises(error):
                    storage.load_visual_profile_index_payload(self.path)

    def test_rejects_duplicate_json_keys_even_with_correct_checksum(self):
        manifest = self.write()
        self.replace_shard(manifest, 0, raw=b'{"schema_version":1,"shard_id":"000","entries":{},"entries":{}}\n')
        with self.assertRaisesRegex(ValueError, "Duplicate JSON key"):
            storage.load_visual_profile_index_payload(self.path)
        self.path.write_bytes(b'{"entries":{},"entries":{}}')
        with self.assertRaisesRegex(ValueError, "Duplicate JSON key"):
            storage.load_visual_profile_index_payload(self.path)

    def test_rejects_duplicate_entries_across_shards(self):
        manifest = self.write()
        first, second = self.read_shard(manifest, 0), self.read_shard(manifest, 1)
        key = next(iter(first["entries"]))
        second["entries"][key] = first["entries"][key]
        self.replace_shard(manifest, 1, shard=second)
        with self.assertRaisesRegex(ValueError, "Duplicate visual profile entry across shards"):
            storage.load_visual_profile_index_payload(self.path)

    def test_rejects_wrong_bucket_even_when_checksums_and_counts_are_consistent(self):
        manifest = self.write()
        first, second = self.read_shard(manifest, 0), self.read_shard(manifest, 1)
        key = next(iter(first["entries"]))
        second["entries"][key] = first["entries"].pop(key)
        self.replace_shard(manifest, 0, shard=first)
        self.replace_shard(manifest, 1, shard=second)
        with self.assertRaisesRegex(ValueError, "wrong hash shard"):
            storage.load_visual_profile_index_payload(self.path)

    def test_rejects_manifest_structure_and_membership_corruption(self):
        mutations = {
            "format": lambda m: m["storage"].update(format="unknown"),
            "hash": lambda m: m["storage"].update(hash_algorithm="md5"),
            "boolean_count": lambda m: m["storage"].update(shard_count=True),
            "zero_count": lambda m: m["storage"].update(shard_count=0),
            "missing_row": lambda m: m["shards"].pop(),
            "duplicate_id": lambda m: m["shards"][1].update(id=m["shards"][0]["id"]),
            "duplicate_path": lambda m: m["shards"][1].update(path=m["shards"][0]["path"]),
            "wrong_count": lambda m: m.update(entry_count=m["entry_count"] + 1),
            "boolean_entry_count": lambda m: m["shards"][0].update(entry_count=True),
            "wrong_shard_count": lambda m: m["shards"][0].update(entry_count=-1),
            "duplicate_order": lambda m: m["entry_order"].__setitem__(1, m["entry_order"][0]),
            "unknown_order_key": lambda m: m["entry_order"].__setitem__(0, "missing-profile"),
            "mixed_entries": lambda m: m.update(entries={}),
        }
        for kind, mutate in mutations.items():
            with self.subTest(kind=kind):
                manifest = self.write()
                mutate(manifest)
                self.save_manifest(manifest)
                with self.assertRaises(ValueError):
                    storage.load_visual_profile_index_payload(self.path)

    def test_rejects_wrong_shard_identity_with_correct_checksum(self):
        for field, value in (("schema_version", 2), ("shard_id", "999")):
            with self.subTest(field=field):
                manifest = self.write()
                shard = self.read_shard(manifest, 0)
                shard[field] = value
                self.replace_shard(manifest, 0, shard=shard)
                with self.assertRaisesRegex(ValueError, "shard identity"):
                    storage.load_visual_profile_index_payload(self.path)

    def test_rejects_path_traversal_absolute_escape_and_symlink_escape_before_read(self):
        for kind in ("parent", "absolute", "symlink"):
            with self.subTest(kind=kind):
                manifest = self.write()
                row = manifest["shards"][0]
                outside = self.root / "outside.json"
                outside.write_bytes((self.path.parent / row["path"]).read_bytes())
                if kind == "parent":
                    row["path"] = "../outside.json"
                elif kind == "absolute":
                    row["path"] = str(outside)
                else:
                    link = self.path.parent / "escape.json"
                    link.symlink_to(outside)
                    row["path"] = link.name
                self.save_manifest(manifest)
                original = Path.read_bytes
                def guarded_read(path):
                    self.assertNotEqual(Path(path).resolve(), outside.resolve(), "read escaped the asset root")
                    return original(path)
                with mock.patch.object(Path, "read_bytes", guarded_read):
                    with self.assertRaisesRegex(ValueError, "escapes directory"):
                        storage.load_visual_profile_index_payload(self.path)

    def test_invalid_writer_counts_are_rejected_without_publishing(self):
        for count in (0, -1, True, 1.5, "4"):
            with self.subTest(count=count), self.assertRaises(ValueError):
                self.write(count=count)
        self.assertFalse(self.path.exists())


class PhotoVisualProfileShardIntegrationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="visual-shards-integration-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.path = self.root / "visual_index.json"
        self.registry = {
            "schema_version": generator.VISUAL_OBLIGATION_REGISTRY_SCHEMA_VERSION,
            "contract_version": generator.VISUAL_OBLIGATIONS_CONTRACT_VERSION,
            "visual_intent_contract_version": generator.VISUAL_INTENT_CONTRACT_VERSION,
            "concept_contract_version": generator.VISUAL_CONCEPTS_CONTRACT_VERSION,
            "retrieval_policy": {"minimum_similarity": 0.7, "best_score_margin": 0.08, "candidate_limit": 8},
            "profiles": [
                {
                    "id": name,
                    "activation": {"exact_terms": [f"{name} scene"], "project_glossary_aliases": [f"풍경 {name}"]},
                    "semantics": {"definition": f"visible {name} scene", "paraphrase_examples": [f"a {name} composition"]},
                }
                for name in ("zebra", "apple", "middle")
            ],
        }
        self.vectors = {"zebra": [1.0, -0.0], "apple": [0.0, 1.0], "middle": [0.25, 0.75]}
        self.payload = generator.build_visual_profile_index_payload(self.registry, vectors=self.vectors, dimensions=2)

    def reusable(self, paths, registry=None):
        return builder.reusable_vectors(paths, registry or self.registry, provider=generator.SEMANTIC_PROVIDER, model=generator.SEMANTIC_MODEL_ID, dimensions=2)

    def run_builder(self, *extra_args):
        registry = self.root / "registry.json"
        registry.write_bytes(encoded(self.registry))
        args = ["build_visual_profile_index.py", "--registry", str(registry), "--output", str(self.path), "--dimensions", "2", *map(str, extra_args)]
        with mock.patch.object(sys, "argv", args), mock.patch.object(sys, "stdout", new_callable=io.StringIO):
            return builder.main()

    def test_runtime_loader_validates_legacy_and_sharded_identically(self):
        for sharded in (False, True):
            with self.subTest(sharded=sharded):
                if sharded:
                    builder.write_payload(self.path, self.payload)
                else:
                    self.path.write_bytes(encoded(self.payload))
                loaded = generator.load_visual_profile_index(self.path, self.registry, dimensions=2)
                self.assertEqual(encoded(loaded), encoded(self.payload))
                self.assertEqual(self.reusable([self.path]), self.vectors)
                changed_registry = copy.deepcopy(self.registry)
                changed_registry["profiles"][0]["semantics"]["definition"] += " changed"
                with self.assertRaisesRegex(ValueError, "registry_sha256"):
                    generator.load_visual_profile_index(self.path, changed_registry, dimensions=2)

    def test_cache_only_build_migrates_legacy_and_rebuilds_shards_without_embeddings(self):
        self.path.write_bytes(encoded(self.payload))
        with mock.patch.object(builder, "embed_texts_with_gemini", side_effect=AssertionError("embedding API must not be called")) as embed:
            with mock.patch.object(builder, "load_project_env", side_effect=AssertionError("credentials must not be read")) as credentials:
                self.assertEqual(self.run_builder(), 0)
                first = self.path.read_bytes()
                self.assertEqual(json.loads(first)["storage"]["format"], storage.FORMAT)
                self.assertEqual(self.run_builder(), 0)
                self.assertEqual(self.path.read_bytes(), first)
                self.assertEqual(self.run_builder("--check"), 0)
        embed.assert_not_called()
        credentials.assert_not_called()
        self.assertEqual(encoded(storage.load_visual_profile_index_payload(self.path)), encoded(self.payload))

    def test_incremental_registry_update_reuses_legacy_and_sharded_cache_without_api(self):
        old_payload = copy.deepcopy(self.payload)
        old_payload["entries"].pop("middle")
        old_payload["registry_sha256"] = "older-registry-hash"
        old_payload["semantic_text_recipe"] = "older-text-recipe"
        legacy = self.root / "legacy_cache.json"
        legacy.write_bytes(encoded(old_payload))
        cached_addition = copy.deepcopy(self.payload)
        cached_addition["entries"] = {"middle": self.payload["entries"]["middle"]}
        cache = self.root / "addition_cache.json"
        builder.write_payload(cache, cached_addition)
        with mock.patch.object(builder, "embed_texts_with_gemini", side_effect=AssertionError("all matching vectors are cached")), mock.patch.object(builder, "load_project_env", side_effect=AssertionError("credentials must not be read")):
            self.assertEqual(self.run_builder("--cache-index", legacy, "--cache-index", cache), 0)
        self.assertEqual(encoded(storage.load_visual_profile_index_payload(self.path)), encoded(self.payload))

    def test_cache_reuse_requires_matching_provider_model_dimensions_and_text(self):
        for key, wrong in (("provider", "other"), ("embedding_model", "other"), ("embedding_dimensions", 3)):
            with self.subTest(key=key):
                payload = copy.deepcopy(self.payload)
                payload[key] = wrong
                builder.write_payload(self.path, payload)
                self.assertEqual(self.reusable([self.path]), {})
        payload = copy.deepcopy(self.payload)
        payload["entries"]["zebra"]["text"] += " changed"
        payload["entries"]["apple"]["vector"] = [1.0]
        builder.write_payload(self.path, payload)
        self.assertEqual(self.reusable([self.path]), {"middle": self.vectors["middle"]})
        self.assertEqual(self.reusable([self.root / "missing.json"]), {})

    def test_corrupt_cache_fails_before_embedding_or_credential_access(self):
        manifest = storage.write_sharded_visual_profile_index(self.path, self.payload)
        shard = self.path.parent / manifest["shards"][0]["path"]
        shard.write_bytes(shard.read_bytes() + b" ")
        with mock.patch.object(builder, "embed_texts_with_gemini", side_effect=AssertionError("corrupt cache must not trigger an API call")), mock.patch.object(builder, "load_project_env", side_effect=AssertionError("credentials must not be read")):
            with self.assertRaisesRegex(ValueError, "checksum mismatch"):
                self.run_builder()

    def test_missing_referenced_cache_shard_fails_before_embedding_or_credentials(self):
        manifest = storage.write_sharded_visual_profile_index(self.path, self.payload)
        shard = self.path.parent / manifest["shards"][0]["path"]
        shard.unlink()
        with mock.patch.object(builder, "embed_texts_with_gemini", side_effect=AssertionError("missing cache shard must not trigger an API call")), mock.patch.object(builder, "load_project_env", side_effect=AssertionError("credentials must not be read")):
            with self.assertRaises(FileNotFoundError):
                self.run_builder()

    def test_invalid_cache_json_fails_before_embedding_or_credential_access(self):
        self.path.write_bytes(b'{"entries": invalid-json}')
        with mock.patch.object(builder, "embed_texts_with_gemini", side_effect=AssertionError("invalid cache JSON must not trigger an API call")), mock.patch.object(builder, "load_project_env", side_effect=AssertionError("credentials must not be read")):
            with self.assertRaises(json.JSONDecodeError):
                self.run_builder()

    def test_installed_copy_loads_shards_without_repository_or_pythonpath(self):
        installed = self.root / "installed-photo-skill"
        scripts = installed / "scripts"
        shutil.copytree(SCRIPT_DIR, scripts, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        shutil.copytree(SKILL_DIR / "precore", installed / "precore", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        assets = installed / "assets"
        assets.mkdir()
        index_path = assets / "visual_index.json"
        registry_path = assets / "registry.json"
        registry_path.write_bytes(encoded(self.registry))
        builder.write_payload(index_path, self.payload)
        expected = hashlib.sha256(encoded(self.payload)).hexdigest()
        code = r'''
import hashlib, importlib.util, json, pathlib, sys
skill, expected = pathlib.Path(sys.argv[1]), sys.argv[2]
spec = importlib.util.spec_from_file_location("installed_generator", skill / "scripts" / "prompt_generator.py")
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)
registry = generator.load_visual_obligation_registry(skill / "assets" / "registry.json")
payload = generator.load_visual_profile_index(skill / "assets" / "visual_index.json", registry, dimensions=2)
raw = (json.dumps(payload, ensure_ascii=False, separators=(",", ":"), allow_nan=False) + "\n").encode()
assert hashlib.sha256(raw).hexdigest() == expected
storage = sys.modules["visual_profile_index_storage"]
assert pathlib.Path(storage.__file__).resolve().parent == (skill / "scripts").resolve()
assert list(payload["entries"]) == ["zebra", "apple", "middle"]
print("copied skill loaded and validated")
'''
        result = subprocess.run([sys.executable, "-I", "-c", code, str(installed), expected], cwd=self.root, env={"PATH": os.environ.get("PATH", "")}, capture_output=True, text=True, check=False, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("copied skill loaded and validated", result.stdout)
        checked = subprocess.run([sys.executable, str(scripts / "build_visual_profile_index.py"), "--check", "--registry", str(registry_path), "--output", str(index_path), "--dimensions", "2"], cwd=self.root, env={"PATH": os.environ.get("PATH", "")}, capture_output=True, text=True, check=False, timeout=30)
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        self.assertIn("3 profiles", checked.stdout)


if __name__ == "__main__":
    unittest.main()
