"""Positive component evidence must not exclude its own authored profile."""
from __future__ import annotations
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/photo-prompt-image-generator"
sys.path.insert(0, str(SKILL / "scripts"))
import prompt_generator as pg
from audit_composed_prompt import authorial_evidence_tokens

PROFILE_IDS = {
    "wide_angle_near_field_perspective", "panning_subject_tracking_motion_relation",
    "rear_curtain_flash_motion_trace", "negative_fill_shadow_deepening_relation",
    "diffusion_filter_highlight_halation", "mixed_illuminant_white_balance_relation",
    "highlight_rolloff_tone_response",
}


class CaptureBoundaryDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        registry = pg.load_visual_obligation_registry(SKILL / "assets/photo_prompt_visual_obligations.json")
        cls.profiles = [p for p in registry["profiles"] if p["id"] in PROFILE_IDS]
        assert len(cls.profiles) == 7

    def test_complete_positive_components_are_applicable_in_both_languages(self):
        for p in self.profiles:
            groups = p["semantics"]["component_semantics"]["groups"]
            for language in (0, 1):
                text = "; ".join(g["any_terms"][language] for g in groups)
                with self.subTest(profile=p["id"], language=language):
                    self.assertTrue(pg.visual_profile_context_applicability(
                        p, text, has_authorial_core_context=True,
                        require_positive_context_terms=False)[0])
                    self.assertIsNotNone(pg.candidate_pack_visual_component_match(p, text))

    def test_affirmative_exclusions_still_block_complete_components(self):
        for p in self.profiles:
            text = "; ".join(g["any_terms"][0] for g in p["semantics"]["component_semantics"]["groups"])
            for exclusion in p["activation"]["exclude_if_any_terms"]:
                with self.subTest(profile=p["id"], exclusion=exclusion):
                    self.assertIsNone(pg.candidate_pack_visual_component_match(p, text + "; " + exclusion))

    def test_missing_required_components_are_not_replaced_by_boundary_prose(self):
        for p in self.profiles:
            groups = p["semantics"]["component_semantics"]["groups"]
            for missing in range(len(groups)):
                for language in (0, 1):
                    text = "; ".join(g["any_terms"][language] for i, g in enumerate(groups) if i != missing)
                    with self.subTest(profile=p["id"], missing=missing, language=language):
                        self.assertIsNone(pg.candidate_pack_visual_component_match(p, text))

    def test_boundary_anchor_meets_its_existing_evidence_minimum(self):
        for p in self.profiles:
            boundary = p["semantics"]["component_semantics"]["groups"][-1]["any_terms"][0]
            requirements = [r for r in p["evidence_requirements"].values() if boundary in r["must_mention_any"]]
            self.assertEqual(len(requirements), 1, p["id"])
            self.assertGreaterEqual(len(authorial_evidence_tokens(boundary)), requirements[0]["min_content_words"], p["id"])


if __name__ == "__main__":
    unittest.main()
