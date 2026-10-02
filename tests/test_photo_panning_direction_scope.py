"""Tracked-subject blur is not restricted to a compulsory lateral trajectory."""
from __future__ import annotations
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/photo-prompt-image-generator"
sys.path.insert(0, str(SKILL / "scripts"))
import prompt_generator as pg
from audit_composed_prompt import authorial_evidence_tokens


class PanningDirectionScopeDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = pg.load_visual_obligation_registry(SKILL / "assets/photo_prompt_visual_obligations.json")
        cls.profile = next(p for p in cls.registry["profiles"] if p["id"] == "panning_subject_tracking_motion_relation")
        cls.groups = cls.profile["semantics"]["component_semantics"]["groups"]
        cls.vector_group = next(g for g in cls.groups if g["id"] == "pan_vector_consistency")

    def test_default_instructions_and_evidence_do_not_force_lateral_motion(self):
        self.assertNotIn("laterally", self.profile["semantics"]["definition"])
        self.assertNotIn("laterally", self.profile["composition_instruction"])
        preferred = self.profile["evidence_requirements"]["pan_vector_phrase"]["must_mention_any"][0]
        self.assertNotIn("lateral", preferred)
        self.assertEqual(preferred, self.vector_group["any_terms"][0])
        self.assertGreaterEqual(len(authorial_evidence_tokens(preferred)),
            self.profile["evidence_requirements"]["pan_vector_phrase"]["min_content_words"])

    def test_neutral_and_legacy_lateral_components_remain_compatible(self):
        self.assertEqual(len(self.vector_group["any_terms"]), 4)
        for language, vector_variant in ((0, 0), (1, 1), (0, 2), (1, 3)):
            text = "; ".join(g["any_terms"][vector_variant if g["id"] == "pan_vector_consistency" else language]
                             for g in self.groups)
            with self.subTest(language=language, vector_variant=vector_variant):
                self.assertEqual(pg.candidate_pack_visual_component_match(self.profile, text), "component_semantics")
        self.assertIn("lateral", self.vector_group["any_terms"][2])
        self.assertIn(self.vector_group["any_terms"][2],
                      self.profile["evidence_requirements"]["pan_vector_phrase"]["must_mention_any"])

    def test_no_broad_panning_alias_or_gate_relaxation(self):
        aliases = self.profile["activation"]["exact_terms"]
        self.assertNotIn("panning", aliases)
        self.assertNotIn("vertical panning", aliases)
        self.assertEqual(len(self.profile["render_gates"]), 5)
        self.assertEqual(self.profile["semantics"]["component_semantics"]["minimum_component_groups"], 5)
        self.assertIn("camera shake", self.profile["activation"]["exclude_if_any_terms"])


if __name__ == "__main__":
    unittest.main()
