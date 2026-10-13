"""Behavioral regressions for native role applicability and explicit exclusions."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/photo-prompt-image-generator/scripts"))
import photo_candidate_corpus as corpus
from photo_global_retrieval import guard_policy
import prompt_generator as generator


class CandidateQualityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = corpus.load(ROOT / "skills/photo-prompt-image-generator/assets")

    def test_declared_human_material_use_survives_a_normal_fashion_context(self):
        checked = 0
        for binding in self.source["slot_bindings"].values():
            record = self.source["candidates"][binding["candidate_id"]]
            if binding["slot_id"] != "surface_material" or "human" not in record["conditions"].get("for_any", []):
                continue
            checked += 1
            policy = binding["conditions"].get("subject_applicability", {})
            with self.subTest(candidate=record["id"]):
                self.assertTrue(guard_policy(policy, {"subject_category": "human", "domains": ["fashion"]}))
        self.assertGreaterEqual(checked, 12)
        self.assertIsNone(generator.slot_block_reason(self.source, "surface_material",
            {"subject_category": "human", "domains": ["fashion"]}))

    def test_capture_role_supports_product_documentary_and_architecture(self):
        for category, domain in [("object", "product"), ("human", "documentary"), ("environment", "architecture")]:
            contract = {"subject_category": category, "domains": [domain]}
            with self.subTest(category=category, domain=domain):
                self.assertIsNone(generator.slot_block_reason(self.source, "capture_context", contract))
        for binding in self.source["slot_bindings"].values():
            record = self.source["candidates"][binding["candidate_id"]]
            if record["content"].get("en", "").startswith("an object macro editorial"):
                self.assertTrue(guard_policy(binding["conditions"]["subject_applicability"],
                    {"subject_category": "object", "domains": ["product"]}))
                return
        self.fail("macro product capture regression case is missing")

    def test_magnified_view_role_supports_objects_and_wildlife(self):
        for category in ("object", "animal"):
            self.assertIsNone(generator.slot_block_reason(self.source, "apparatus_pov",
                {"subject_category": category, "domains": ["wildlife"]}))

    def test_role_fixes_preserve_explicit_no_people_and_adult_exclusions(self):
        candidates = [record for record in self.source["candidates"].values()
            if record["record_kind"] == "visual_option" and record["conditions"].get("for_any") == ["human"]]
        self.assertTrue(candidates)
        for record in candidates[:20]:
            entry = corpus.entry(self.source, record["id"])
            contract = {"adult_allowed": True, "subject_category": "object", "domains": ["product"],
                "intent_constraints": {"no_people": True, "subject_categories": ["object"], "domains": ["product"]}}
            self.assertFalse(generator.core_entry_eligible(self.source, {"user_exclusions": []}, contract,
                {"subject": {"en": "a ceramic cup", "tags": ["object"]}}, "prop", entry))
        for binding in self.source["slot_bindings"].values():
            if binding["slot_id"] != "adult_presentation_context":
                continue
            entry = corpus.entry(self.source, binding["candidate_id"], binding["id"])
            self.assertEqual(generator.entry_block_reason(entry, "adult_presentation_context",
                {"adult_allowed": False, "intent_constraints": {}}), "adult_not_allowed")


if __name__ == "__main__":
    unittest.main()
