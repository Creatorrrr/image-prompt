"""Focused embedding request tests; synthetic credentials and no network."""
from __future__ import annotations

import hashlib
import importlib.util
import unittest
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from google.genai import types as genai_types


GENERATOR_PATH = (
    Path(__file__).resolve().parents[1]
    / "skills/photo-prompt-image-generator/scripts/prompt_generator.py"
)


class PhotoGeminiEmbeddingRequestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location(
            "photo_gemini_request_generator", GENERATOR_PATH
        )
        cls.generator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.generator)

    @contextmanager
    def mocked_client(self, *, vectors=None, error=None):
        if vectors is None:
            vectors = [[0.123456789, -0.987654321] + [0.0] * 766]
        client = mock.Mock()
        client.models.embed_content.return_value = SimpleNamespace(
            embeddings=[SimpleNamespace(values=vector) for vector in vectors]
        )
        client.models.embed_content.side_effect = error
        with (
            mock.patch.object(
                self.generator, "get_gemini_api_key", return_value="mock-only"
            ),
            mock.patch.object(
                self.generator, "cached_gemini_client", return_value=client
            ),
            mock.patch("socket.socket", side_effect=AssertionError("No network")),
            mock.patch.object(
                self.generator.time, "sleep", side_effect=AssertionError("No retry")
            ),
        ):
            yield client

    def test_embedding_two_omits_task_type_and_preserves_exact_text(self):
        text = "  신선한 화환과 주변의 마른 꽃\n"
        for model in ("gemini-embedding-2", "models/gemini-embedding-2"):
            with self.subTest(model=model), self.mocked_client() as client:
                vectors = self.generator.embed_texts_with_gemini(
                    [text], model=model, dimensions=768,
                    api_key="mock-only", retry_attempts=0,
                )
                client.models.embed_content.assert_called_once()
                request = client.models.embed_content.call_args.kwargs
                self.assertEqual(request["model"], model)
                self.assertEqual(request["contents"], [text])
                config = request["config"]
                self.assertIsInstance(config, genai_types.EmbedContentConfig)
                self.assertEqual(config.output_dimensionality, 768)
                self.assertNotIn("task_type", config.model_fields_set)
                self.assertNotIn("task_type", config.model_dump(exclude_none=True))
                self.assertEqual(vectors, [[0.123457, -0.987654] + [0.0] * 766])

    def test_other_models_keep_semantic_similarity(self):
        for model in ("gemini-embedding-001", "models/gemini-embedding-001"):
            with self.subTest(model=model), self.mocked_client() as client:
                self.generator.embed_texts_with_gemini(
                    ["unchanged"], model=model,
                    api_key="mock-only", retry_attempts=0,
                )
                client.models.embed_content.assert_called_once()
                config = client.models.embed_content.call_args.kwargs["config"]
                self.assertEqual(config.task_type, "SEMANTIC_SIMILARITY")
                self.assertEqual(config.output_dimensionality, 768)

    def test_zero_retry_rethrows_a_retryable_failure_after_one_call(self):
        with self.mocked_client(error=RuntimeError("503 UNAVAILABLE")) as client:
            with self.assertRaisesRegex(RuntimeError, "503 UNAVAILABLE"):
                self.generator.embed_texts_with_gemini(
                    ["unchanged"], api_key="mock-only", retry_attempts=0
                )
            client.models.embed_content.assert_called_once()

    def test_invalid_dimensions_and_cardinality_fail_closed(self):
        cases = (([[0.0] * 767], ValueError), ([], RuntimeError))
        for vectors, error in cases:
            with self.subTest(error=error), self.mocked_client(vectors=vectors) as client:
                with self.assertRaises(error):
                    self.generator.embed_texts_with_gemini(
                        ["unchanged"], api_key="mock-only", retry_attempts=0
                    )
                client.models.embed_content.assert_called_once()

    def test_wreath_inputs_keep_fresh_wreath_and_dried_surroundings_distinct(self):
        assets = GENERATOR_PATH.parents[1] / "assets"
        data = self.generator.load_json(assets / "photo_prompt_tags.json")
        registry = self.generator.load_visual_obligation_registry(
            assets / "photo_prompt_visual_obligations.json"
        )
        entry = next(row for row in data["slots"]["prop"]
                     if row["id"] == "hr_wreath_fresh_decay_contrast")
        profile = next(row for row in registry["profiles"]
                       if row["id"] == "hvr_profile_wreath_fresh_decay_contrast")
        self.assertEqual(entry["ko"],
                         "신선한 화환과 주변의 마른 꽃의 관찰 가능한 관계")
        self.assertIn("one fresh floral wreath", entry["en"])
        self.assertIn("nearby dried flowers", entry["en"])
        inputs = (
            (self.generator.semantic_text_for_entry(entry, "prop", kind="slot"),
             "040d49b151307c13b0cf9f041b621ba13f80060e3320f20bb90ade4d2a54772c"),
            (self.generator.visual_profile_semantic_text(profile),
             "da979ab6edd8660f6e27edff24dd937684122e3ef82e0c7c6e0ff3de38b9765a"),
        )
        for text, expected in inputs:
            with self.subTest(input_sha256=expected):
                self.assertNotIn("시든 꽃·마른 화환", text)
                self.assertIn("신선한 화환과 주변의 마른 꽃", text)
                self.assertEqual(hashlib.sha256(text.encode("utf-8")).hexdigest(),
                                 expected)


if __name__ == "__main__":
    unittest.main()
