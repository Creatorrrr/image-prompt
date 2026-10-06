from __future__ import annotations
import copy, gc, hashlib, importlib.util, io, json, os, subprocess, sys, tempfile, unittest
from pathlib import Path
from unittest import mock
ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills/photo-prompt-image-generator"
TAGS_PATH = SKILL_DIR / "assets/photo_prompt_tags.json"
GENERATOR_PATH = SKILL_DIR / "scripts/prompt_generator.py"
INDEX_BUILDER_PATH = SKILL_DIR / "scripts/build_semantic_index.py"
BM25F_RETRIEVAL_PATH = SKILL_DIR / "scripts/bm25f_retrieval.py"
SEMANTIC_INDEX_PATH = SKILL_DIR / "assets/photo_prompt_semantic_index.json"


def load_generator():
    spec = importlib.util.spec_from_file_location("photo_prompt_generator", GENERATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load generator module: {GENERATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def load_index_builder():
    scripts_dir = str(SKILL_DIR / "scripts")
    inserted = False
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
        inserted = True
    try:
        spec = importlib.util.spec_from_file_location("photo_prompt_index_builder", INDEX_BUILDER_PATH)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Could not load index builder module: {INDEX_BUILDER_PATH}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        if inserted:
            sys.path.remove(scripts_dir)

class PhotoSemanticIndexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.generator = load_generator()
        cls.data = json.loads(TAGS_PATH.read_text(encoding="utf-8"))


    def fake_gemini_vectors(self, texts, model=None, dimensions=768, api_key=None, **kwargs):
        vectors = []
        for text in texts:
            digest = hashlib.sha256(str(text).encode("utf-8")).digest()
            vector = [0.0] * dimensions
            for index, byte in enumerate(digest):
                vector[(byte + index) % dimensions] += 1.0 if index % 2 == 0 else -1.0
            norm = sum(value * value for value in vector) ** 0.5
            vectors.append([round(value / norm, 6) if norm else 0.0 for value in vector])
        return vectors


    def test_semantic_index_builder_dry_run_does_not_require_api_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "semantic_index.json"
            env = os.environ.copy()
            env.pop("GEMINI_API_KEY", None)
            env.pop("GOOGLE_API_KEY", None)
            result = subprocess.run(
                [
                    sys.executable,
                    str(INDEX_BUILDER_PATH),
                    "--tags",
                    str(TAGS_PATH),
                    "--output",
                    str(out_path),
                    "--dry-run",
                ],
                cwd=ROOT,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(out_path.exists())
        self.assertIn("gemini-embedding-2", result.stdout)
        self.assertIn("768", result.stdout)
        self.assertIn(
            self.generator.SEMANTIC_TEXT_RECIPE_VERSION,
            result.stdout,
        )


    def test_semantic_index_builder_loads_project_env_file(self):
        builder = load_index_builder()
        with tempfile.TemporaryDirectory() as tmp:
            env_path = Path(tmp) / ".env"
            env_path.write_text(
                "\n".join(
                    [
                        "GEMINI_API_KEY='from-env-file'",
                        "GOOGLE_API_KEY=from-google-env-file",
                        "IGNORED_KEY=ignored",
                    ]
                ),
                encoding="utf-8",
            )

            with mock.patch.object(builder, "PROJECT_ROOT", Path(tmp)):
                with mock.patch.dict(os.environ, {}, clear=True):
                    builder.load_project_env()
                    self.assertEqual(os.environ["GEMINI_API_KEY"], "from-env-file")
                    self.assertEqual(os.environ["GOOGLE_API_KEY"], "from-google-env-file")
                    self.assertNotIn("IGNORED_KEY", os.environ)

                with mock.patch.dict(os.environ, {"GEMINI_API_KEY": "already-set"}, clear=True):
                    builder.load_project_env()
                    self.assertEqual(os.environ["GEMINI_API_KEY"], "already-set")
                    self.assertEqual(os.environ["GOOGLE_API_KEY"], "from-google-env-file")


    def test_semantic_index_builder_main_loads_project_env_before_running(self):
        builder = load_index_builder()
        with mock.patch.object(builder, "load_project_env") as load_env:
            with mock.patch.object(sys, "argv", ["build_semantic_index.py", "--dry-run"]):
                self.assertEqual(builder.main(), 0)

        load_env.assert_called_once_with()


    def test_semantic_index_builder_reuses_existing_vectors_after_tag_addition(self):
        builder = load_index_builder()
        base_data = {
            "version": "test",
            "slots": {
                "subject": [{"id": "person", "en": "person", "ko": "사람"}],
            },
        }
        updated_data = json.loads(json.dumps(base_data, ensure_ascii=False))
        updated_data["slots"]["subject"].append({"id": "new_actor", "en": "new actor", "ko": "새 배우"})
        embed_calls: list[list[str]] = []

        def fake_embed(texts, model=None, dimensions=768, **kwargs):
            embed_calls.append(list(texts))
            return self.fake_gemini_vectors(texts, model=model, dimensions=dimensions, **kwargs)

        original_embedder = builder.embed_texts_with_gemini
        builder.embed_texts_with_gemini = fake_embed
        try:
            with tempfile.TemporaryDirectory() as tmp:
                output = Path(tmp) / "semantic_index.json"
                checkpoint = Path(tmp) / "semantic_index.json.partial"
                first_payload = builder.build_resumable_index_payload(
                    base_data,
                    output=output,
                    checkpoint=checkpoint,
                    provider="gemini",
                    model="gemini-embedding-2",
                    dimensions=768,
                    batch_size=1,
                    request_interval=0,
                    retry_attempts=0,
                    retry_initial_delay=0,
                    cache_indexes=[],
                )
                first_payload["semantic_text_recipe"] = "semantic-text-older"
                builder.write_sharded_payload(output, first_payload)
                embed_calls.clear()

                second_payload = builder.build_resumable_index_payload(
                    updated_data,
                    output=output,
                    checkpoint=checkpoint,
                    provider="gemini",
                    model="gemini-embedding-2",
                    dimensions=768,
                    batch_size=1,
                    request_interval=0,
                    retry_attempts=0,
                    retry_initial_delay=0,
                    cache_indexes=[output],
                )
        finally:
            builder.embed_texts_with_gemini = original_embedder

        self.assertEqual(len(embed_calls), 1)
        self.assertEqual(len(embed_calls[0]), 1)
        self.assertIn("new actor", embed_calls[0][0])
        self.assertNotIn("new_actor", embed_calls[0][0])
        self.assertEqual(len(second_payload["entries"]), 2)
        self.assertEqual(
            second_payload["entries"]["slot:subject:person"]["vector"],
            first_payload["entries"]["slot:subject:person"]["vector"],
        )
        self.assertNotEqual(second_payload["dictionary_hash"], first_payload["dictionary_hash"])
        self.assertEqual(
            second_payload["semantic_text_recipe"],
            self.generator.SEMANTIC_TEXT_RECIPE_VERSION,
        )


    def test_semantic_index_shards_round_trip_exact_entry_order_and_values(self):
        builder = load_index_builder()
        payload = {
            "provider": "gemini",
            "dictionary_hash": "a" * 64,
            "semantic_text_recipe": self.generator.SEMANTIC_TEXT_RECIPE_VERSION,
            "embedding_model": "gemini-embedding-2",
            "embedding_dimensions": 3,
            "entries": {
                "slot:subject:first": {"kind": "slot", "slot": "subject", "id": "first", "text": "first", "vector": [1.0, 0.0, 0.0]},
                "slot:subject:second": {"kind": "slot", "slot": "subject", "id": "second", "text": "second", "vector": [0.0, 1.0, 0.0]},
                "slot:location:third": {"kind": "slot", "slot": "location", "id": "third", "text": "third", "vector": [0.0, 0.0, 1.0]},
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "semantic_index.json"
            manifest = builder.write_sharded_payload(output, payload, shard_count=2)
            loaded = self.generator.load_semantic_index_payload(output)
            shard_bytes = [
                (output.parent / shard["path"]).read_bytes()
                for shard in manifest["shards"]
            ]

        self.assertNotIn("entries", manifest)
        self.assertEqual(manifest["storage"]["format"], "sharded-json-v1")
        self.assertEqual(manifest["entry_count"], 3)
        self.assertEqual(list(loaded["entries"]), list(payload["entries"]))
        self.assertEqual(loaded["entries"], payload["entries"])
        for raw in shard_bytes:
            self.assertNotIn(b"\n", raw)
            self.assertEqual(
                raw,
                json.dumps(
                    json.loads(raw),
                    ensure_ascii=False,
                    separators=(",", ":"),
                ).encode("utf-8"),
            )


    def test_semantic_index_shards_prune_only_prior_generation_directories(self):
        builder = load_index_builder()
        payload = {
            "provider": "gemini",
            "dictionary_hash": "a" * 64,
            "semantic_text_recipe": self.generator.SEMANTIC_TEXT_RECIPE_VERSION,
            "embedding_model": "gemini-embedding-2",
            "embedding_dimensions": 3,
            "entries": {
                "slot:subject:first": {
                    "kind": "slot",
                    "slot": "subject",
                    "id": "first",
                    "text": "first",
                    "vector": [1.0, 0.0, 0.0],
                },
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "semantic_index.json"
            builder.write_sharded_payload(output, payload, shard_count=2)
            shard_parent = output.with_name("semantic_index_shards")
            first_generation = shard_parent / ("a" * 16)
            marker = shard_parent / "README.keep"
            marker.write_text("not a generation directory", encoding="utf-8")

            updated_payload = json.loads(json.dumps(payload))
            updated_payload["dictionary_hash"] = "b" * 64
            builder.write_sharded_payload(output, updated_payload, shard_count=2)

            self.assertFalse(first_generation.exists())
            self.assertTrue((shard_parent / ("b" * 16)).is_dir())
            self.assertEqual(marker.read_text(encoding="utf-8"), "not a generation directory")


    def test_semantic_index_builder_requires_api_key_for_real_build(self):
        builder = load_index_builder()
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "semantic_index.json"
            with mock.patch.object(builder, "PROJECT_ROOT", Path(tmp)):
                with mock.patch.dict(os.environ, {}, clear=True):
                    with mock.patch.object(
                        sys,
                        "argv",
                        [
                            "build_semantic_index.py",
                            "--tags",
                            str(TAGS_PATH),
                            "--output",
                            str(out_path),
                            "--dimensions",
                            "768",
                            "--request-interval",
                            "0",
                            "--retry-attempts",
                            "0",
                        ],
                    ):
                        with mock.patch("sys.stderr", new_callable=io.StringIO) as stderr:
                            result = builder.main()

        self.assertNotEqual(result, 0)
        self.assertFalse(out_path.exists())
        self.assertIn("GEMINI_API_KEY", stderr.getvalue())


    def test_semantic_index_builder_subprocess_uses_project_env_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source"
            target = source / "skills" / "photo-prompt-image-generator"
            scripts = target / "scripts"
            assets = target / "assets"
            scripts.mkdir(parents=True)
            assets.mkdir(parents=True)
            (source / ".env").write_text("GEMINI_API_KEY=from-env-file\n", encoding="utf-8")
            (scripts / "build_semantic_index.py").write_text(
                INDEX_BUILDER_PATH.read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            (scripts / "prompt_generator.py").write_text(
                GENERATOR_PATH.read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            (scripts / "bm25f_retrieval.py").write_text(
                BM25F_RETRIEVAL_PATH.read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            (scripts.parent / "assets/photo_prompt_source_manifest.json").write_bytes(
                (SKILL_DIR / "assets/photo_prompt_source_manifest.json").read_bytes()
            )
            for dependency in GENERATOR_PATH.parent.glob("*.py"):
                (scripts / dependency.name).write_bytes(dependency.read_bytes())
            precore = target / "precore"
            precore.mkdir()
            for dependency in (SKILL_DIR / "precore").iterdir():
                if dependency.is_file():
                    (precore / dependency.name).write_bytes(dependency.read_bytes())
            tags_path = assets / "photo_prompt_tags.json"
            tags_path.write_text(
                json.dumps(
                    {
                        "version": "test",
                        
                                    "slots": {},
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            out_path = Path(tmp) / "semantic_index.json"
            env = os.environ.copy()
            env.pop("GEMINI_API_KEY", None)
            env.pop("GOOGLE_API_KEY", None)
            result = subprocess.run(
                [
                    sys.executable,
                    str(scripts / "build_semantic_index.py"),
                    "--tags",
                    str(tags_path),
                    "--output",
                    str(out_path),
                ],
                cwd=source,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(out_path.exists())
            payload = json.loads(out_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["entry_count"], 0)
            self.assertEqual(payload["storage"]["format"], "sharded-json-v1")
