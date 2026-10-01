from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


SCRIPT_DIR = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "photo-prompt-image-generator"
    / "scripts"
)
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator as generator  # noqa: E402


class PhotoLoadingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = {
            "version": "loading-test",
            "slots": {
                "subject": [{"id": "one", "en": "practical care", "aliases": ["care"]}]
            },
        }
        bm25f = generator.build_semantic_bm25f_payload(self.data)
        documents = bm25f.pop("documents")
        self.index = {
            "provider": generator.SEMANTIC_PROVIDER,
            "dictionary_hash": generator.dictionary_hash(self.data),
            "semantic_text_recipe": generator.SEMANTIC_TEXT_RECIPE_VERSION,
            "embedding_model": generator.SEMANTIC_MODEL_ID,
            "embedding_dimensions": 2,
            "bm25f": bm25f,
            "entries": {
                key: {"bm25f_document": document, "vector": [1.0, 0.0]}
                for key, document in documents.items()
            },
        }

    def validate(self) -> None:
        generator.validate_semantic_index_metadata(self.index, self.data, dimensions=2)

    def test_semantic_validation_preserves_both_inputs(self):
        original_data = copy.deepcopy(self.data)
        original_index = copy.deepcopy(self.index)
        self.validate()
        self.assertEqual(self.data, original_data)
        self.assertEqual(self.index, original_index)

    def test_successful_validation_does_not_hide_later_corpus_corruption(self):
        self.validate()
        fields = self.index["entries"]["slot:subject:one"]["bm25f_document"]["fields"]
        fields["aliases"]["term_frequencies"]["care"] += 1
        with self.assertRaisesRegex(ValueError, "BM25F index is stale"):
            self.validate()

    def test_changed_source_is_rejected_even_with_an_updated_dictionary_hash(self):
        self.validate()
        self.data["slots"]["subject"][0]["aliases"].append("甲乙")
        self.index["dictionary_hash"] = generator.dictionary_hash(self.data)
        with self.assertRaisesRegex(ValueError, "BM25F index is stale"):
            self.validate()

    def test_changed_bm25f_policy_is_rejected(self):
        self.validate()
        self.index["bm25f"]["policy"]["fields"]["aliases"]["weight"] += 1.0
        with self.assertRaisesRegex(ValueError, "BM25F index is stale"):
            self.validate()

    def test_public_bm25f_projection_keeps_independent_nested_copies(self):
        original_index = copy.deepcopy(self.index)
        projection = generator.semantic_bm25f_payload_from_index(self.index)
        projection["policy"]["fields"]["aliases"]["weight"] += 1.0
        projection["documents"]["slot:subject:one"]["fields"]["aliases"]["length"] += 1
        self.assertEqual(self.index, original_index)

    def test_visual_validation_is_read_only_and_rejects_later_corruption(self):
        registry = {
            "schema_version": generator.VISUAL_OBLIGATION_REGISTRY_SCHEMA_VERSION,
            "profiles": [{"id": "one", "activation": {"exact_terms": ["care"]}}],
        }
        index = generator.build_visual_profile_index_payload(
            registry, vectors={"one": [1.0, 0.0]}, dimensions=2
        )
        original_registry = copy.deepcopy(registry)
        original_index = copy.deepcopy(index)
        generator.validate_visual_profile_index_metadata(index, registry, dimensions=2)
        self.assertEqual(registry, original_registry)
        self.assertEqual(index, original_index)
        fields = index["bm25f"]["documents"]["one"]["fields"]
        fields["aliases"]["term_frequencies"]["care"] += 1
        with self.assertRaisesRegex(ValueError, "BM25F index is stale"):
            generator.validate_visual_profile_index_metadata(index, registry, dimensions=2)


if __name__ == "__main__":
    unittest.main()
