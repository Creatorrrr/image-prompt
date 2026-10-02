"""Keep positive lighting/composition components compatible with their guards."""
from __future__ import annotations
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/photo-prompt-image-generator"
sys.path.insert(0, str(SKILL / "scripts"))
import prompt_generator as pg
from audit_composed_prompt import authorial_evidence_tokens

IDS = {"loop_face_light_pattern", "split_face_light_pattern", "low_key_selective_illumination",
       "third_grid_focal_anchor_relation", "asymmetric_counterbalance_relation",
       "subject_field_negative_space_relation", "pattern_break_focal_exception"}


class LightingCompositionBoundaryDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        registry = pg.load_visual_obligation_registry(SKILL / "assets/photo_prompt_visual_obligations.json")
        cls.profiles = [p for p in registry["profiles"] if p["id"] in IDS]
        assert len(cls.profiles) == len(IDS)

    def test_authored_complete_contexts_do_not_self_exclude(self):
        for p in self.profiles:
            groups = p["semantics"]["component_semantics"]["groups"]
            for language in range(min(len(g["any_terms"]) for g in groups)):
                text = "; ".join(g["any_terms"][language] for g in groups)
                with self.subTest(profile=p["id"], language=language):
                    self.assertTrue(pg.visual_profile_context_applicability(p, text,
                        has_authorial_core_context=True, require_positive_context_terms=False)[0])
                    self.assertEqual(pg.candidate_pack_visual_component_match(p, text), "component_semantics")

    def test_affirmative_excluded_relations_remain_blocked(self):
        for p in self.profiles:
            text = "; ".join(g["any_terms"][0] for g in p["semantics"]["component_semantics"]["groups"])
            for excluded in p["activation"]["exclude_if_any_terms"]:
                with self.subTest(profile=p["id"], excluded=excluded):
                    self.assertIsNone(pg.candidate_pack_visual_component_match(p, text + "; " + excluded))

    def test_boundary_evidence_anchor_meets_unchanged_minimum(self):
        for p in self.profiles:
            boundary = p["semantics"]["component_semantics"]["groups"][-1]["any_terms"][0]
            requirements = [r for r in p["evidence_requirements"].values() if boundary in r["must_mention_any"]]
            self.assertEqual(len(requirements), 1, p["id"])
            self.assertGreaterEqual(len(authorial_evidence_tokens(boundary)), requirements[0]["min_content_words"], p["id"])

    def test_one_generic_lighting_component_is_not_a_complete_paraphrase(self):
        lighting_ids = {"loop_face_light_pattern", "split_face_light_pattern", "low_key_selective_illumination"}
        for profile in self.profiles:
            if profile["id"] not in lighting_ids:
                continue
            for group in profile["semantics"]["component_semantics"]["groups"][:3]:
                with self.subTest(profile=profile["id"], group=group["id"]):
                    self.assertIsNone(pg.candidate_pack_visual_component_match(profile, group["any_terms"][0]))

    def test_complete_lighting_paraphrases_remain_discoverable(self):
        lighting_ids = {"loop_face_light_pattern", "split_face_light_pattern", "low_key_selective_illumination"}
        for profile in self.profiles:
            if profile["id"] not in lighting_ids:
                continue
            for phrase in profile["semantics"]["paraphrase_examples"]:
                self.assertIsNotNone(pg.candidate_pack_visual_component_match(profile, phrase))


if __name__ == "__main__":
    unittest.main()
