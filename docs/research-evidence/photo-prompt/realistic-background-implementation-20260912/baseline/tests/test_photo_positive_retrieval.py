from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "skills/photo-prompt-image-generator/scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from photo_visual_retrieval import positive_visual_profile_fields, positive_visual_profile_text
import prompt_generator


class PositiveVisualRetrievalTests(unittest.TestCase):
    def setUp(self):
        self.profile = {
            "id": "unrelated_internal_id",
            "category": "private_review_batch",
            "activation": {"exact_terms": ["bare-faced finish"]},
            "semantics": {
                "definition": "No-makeup makeup with softly visible natural skin texture",
                "paraphrase_examples": ["화장한 티 없는 피부 표현"],
                "visual_components": ["skin texture visible through a sheer base"],
                "component_semantics": {"groups": [{
                    "id": "internal_evaluation_marker",
                    "any_terms": ["subtle color variation across the skin"],
                }]},
                "claim_limits": ["This is not evidence of health or personality"],
                "contrast_examples": ["a solid opaque mask"],
            },
            "concept_candidate": {"concept_terms": ["lightly defined brows"]},
            "composition_instruction": "internal mandatory orchestration instruction",
        }

    def test_control_and_boundary_mutations_cannot_change_positive_documents(self):
        original = positive_visual_profile_fields(self.profile)
        changed = copy.deepcopy(self.profile)
        changed["category"] = "another_review_batch"
        changed["semantics"]["claim_limits"].append("rare health fertility signal")
        changed["semantics"]["contrast_examples"].append("futuristic architecture")
        changed["semantics"]["interpretation_scope"] = "private research taxonomy"
        changed["semantics"]["component_semantics"]["groups"][0]["id"] = "other_id"
        changed["composition_instruction"] = "a different validation-only instruction"
        self.assertEqual(original, positive_visual_profile_fields(changed))
        self.assertEqual(positive_visual_profile_text(self.profile), positive_visual_profile_text(changed))
        self.assertNotIn("health", positive_visual_profile_text(changed))
        self.assertNotIn("private", positive_visual_profile_text(changed))

    def test_negative_form_meaning_and_multilingual_relations_are_retained(self):
        text = positive_visual_profile_text(self.profile)
        self.assertIn("No-makeup makeup", text)
        self.assertIn("화장한 티 없는 피부 표현", text)
        self.assertIn("skin texture visible through a sheer base", text)
        self.assertIn("subtle color variation across the skin", text)

    def test_positive_meaning_mutation_changes_both_retrieval_lanes(self):
        changed = copy.deepcopy(self.profile)
        changed["semantics"]["definition"] = "Opaque geometric face paint"
        self.assertNotEqual(positive_visual_profile_fields(self.profile), positive_visual_profile_fields(changed))
        self.assertNotEqual(positive_visual_profile_text(self.profile), positive_visual_profile_text(changed))

    def test_exact_names_keep_their_separate_authority_lane(self):
        fields = positive_visual_profile_fields(self.profile)
        self.assertEqual(fields["aliases"], ["bare-faced finish"])
        self.assertNotIn("bare-faced finish", positive_visual_profile_text(self.profile))

    def test_candidate_relation_direction_is_visible_to_both_search_lanes(self):
        entry = {
            "id": "internal_candidate_id",
            "en": "two light sources",
            "concept_units": ["upper soft key", "lower fill"],
            "relations": [{
                "id": "private_relation_id", "type": "weaker_than",
                "subject": "lower fill", "object": "upper soft key",
            }],
        }
        before = prompt_generator.semantic_text_for_entry(entry, "lighting")
        fields = prompt_generator.semantic_bm25f_fields_for_entry(entry, "lighting")
        self.assertIn("lower fill weaker than upper soft key", before)
        self.assertEqual(fields["semantic_relations"], ["lower fill weaker than upper soft key"])
        self.assertEqual(fields["concept_units"], ["upper soft key", "lower fill"])
        self.assertNotIn("private_relation_id", before)
        entry["relations"][0].update(subject="upper soft key", object="lower fill")
        self.assertNotEqual(before, prompt_generator.semantic_text_for_entry(entry, "lighting"))
        self.assertNotEqual(fields, prompt_generator.semantic_bm25f_fields_for_entry(entry, "lighting"))


if __name__ == "__main__":
    unittest.main()
