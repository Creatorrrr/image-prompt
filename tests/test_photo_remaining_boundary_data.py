"""Authored positive component bundles must not trip their own exclusion guard."""
from __future__ import annotations
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/photo-prompt-image-generator"
sys.path.insert(0, str(SKILL / "scripts"))
import prompt_generator as pg
from audit_composed_prompt import authorial_evidence_tokens

IDS = {"mirror_selfie_reflection_device_topology", "overhead_social_snapshot_relation",
       "intentional_face_occluded_mood_portrait", "under_eye_high_cheek_blush_distribution",
       "cheekbone_temple_blush_drape", "photobooth_four_cut_sequence",
       "material_replacement_deferral_repair_cycle"}

class RemainingBoundaryDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = pg.load_visual_obligation_registry(SKILL / "assets/photo_prompt_visual_obligations.json")
        cls.profiles = [p for p in cls.registry["profiles"] if p["id"] in IDS]
        assert len(cls.profiles) == 7

    def test_all_authored_english_component_bundles_avoid_self_exclusion(self):
        failures = []
        for p in self.registry["profiles"]:
            groups = p.get("semantics", {}).get("component_semantics", {}).get("groups", [])
            if not groups:
                continue
            text = "; ".join(g["any_terms"][0] for g in groups)
            ok, reason = pg.visual_profile_context_applicability(p, text,
                has_authorial_core_context=True, require_positive_context_terms=False)
            if not ok:
                failures.append((p["id"], reason))
        self.assertEqual(failures, [])

    def test_repaired_full_bundles_preserve_available_languages(self):
        for p in self.profiles:
            groups = p["semantics"]["component_semantics"]["groups"]
            for language in range(min(len(g["any_terms"]) for g in groups)):
                text = "; ".join(g["any_terms"][language] for g in groups)
                with self.subTest(profile=p["id"], language=language):
                    self.assertEqual(pg.candidate_pack_visual_component_match(p, text), "component_semantics")

    def test_declared_exclusions_still_reject_complete_contexts(self):
        for p in self.profiles:
            text = "; ".join(g["any_terms"][0] for g in p["semantics"]["component_semantics"]["groups"])
            for term in p["activation"]["exclude_if_any_terms"]:
                with self.subTest(profile=p["id"], excluded=term):
                    self.assertIsNone(pg.candidate_pack_visual_component_match(p, text + "; " + term))

    def test_mirror_occlusion_and_head_turn_remain_alternatives(self):
        profiles = {p["id"]: p for p in self.profiles}
        mirror = profiles["mirror_selfie_reflection_device_topology"]["semantics"]["component_semantics"]["groups"][-1]["any_terms"][0]
        self.assertIn("any facial occlusion", mirror)
        face = profiles["intentional_face_occluded_mood_portrait"]["semantics"]["component_semantics"]["groups"][-1]["any_terms"][0]
        self.assertIn("head turn", face)


if __name__ == "__main__":
    unittest.main()
