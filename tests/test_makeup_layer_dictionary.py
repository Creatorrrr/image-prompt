import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
TAGS_PATH = SKILL_DIR / "assets" / "photo_prompt_tags.json"

NEW_LAYER_SLOTS = {
    "brow_style",
    "cheek_makeup",
    "complexion_coverage",
    "eyeshadow_style",
    "lip_finish",
    "lip_color_placement",
    "eye_makeup_line",
    "face_sculpting",
    "lash_style",
    "makeup_decoration",
    "makeup_wear_state",
}


def load_tags():
    return json.loads(TAGS_PATH.read_text())


class MakeupLayerDictionaryTests(unittest.TestCase):
    def setUp(self):
        self.tags = load_tags()

    def test_makeup_layer_slots_are_human_only_surface_controls(self):
        for slot in NEW_LAYER_SLOTS:
            with self.subTest(slot=slot):
                entries = self.tags["slots"][slot]
                self.assertGreaterEqual(len(entries), 5)
                self.assertEqual(
                    self.tags["slot_applicability"]["slots"][slot]["subject_categories"],
                    ["human"],
                )
                self.assertTrue(
                    {"product", "jewelry", "food", "wildlife"}.issubset(
                        self.tags["slot_applicability"]["slots"][slot]["deny_domains"]
                    )
                )
                self.assertTrue(all(entry.get("for_any") == ["human"] for entry in entries))

    def test_makeup_axes_keep_line_lash_lip_finish_and_lip_placement_ownership_separate(self):
        eye_line_ids = {entry["id"] for entry in self.tags["slots"]["eye_makeup_line"]}
        lash_ids = {entry["id"] for entry in self.tags["slots"]["lash_style"]}
        lip_finish_ids = {entry["id"] for entry in self.tags["slots"]["lip_finish"]}
        lip_placement_ids = {
            entry["id"] for entry in self.tags["slots"]["lip_color_placement"]
        }

        self.assertTrue(eye_line_ids.isdisjoint(lash_ids))
        self.assertTrue(lip_finish_ids.isdisjoint(lip_placement_ids))
        self.assertIn("colored_mascara_accent", lash_ids)
        self.assertIn("lower_lash_statement_detail", lash_ids)
        self.assertNotIn("colored_mascara_accent", eye_line_ids)
        self.assertNotIn("lower_lash_statement_detail", eye_line_ids)
        for entry in self.tags["slots"]["lip_finish"]:
            rendered = entry["en"].casefold()
            self.assertNotIn("vermilion boundary", rendered)
            self.assertNotIn("lip line", rendered)

    def test_new_makeup_layer_render_terms_are_not_demographic_shortcuts(self):
        forbidden = (
            "for men",
            "for women",
            "male",
            "female",
            "masculine",
            "feminine",
            "genderless",
            "gender-neutral",
        )

        checked_entries = []
        for slot in NEW_LAYER_SLOTS:
            checked_entries.extend(self.tags["slots"][slot])
        checked_entries.extend(
            entry
            for entry in self.tags["slots"]["skin_finish"]
            if entry["id"] in {"cloud_blurred_skin_finish", "skincare_hybrid_second_skin_glow"}
        )

        for entry in checked_entries:
            with self.subTest(entry_id=entry["id"]):
                rendered = entry["en"].lower()
                self.assertFalse(any(term in rendered for term in forbidden))






if __name__ == "__main__":
    unittest.main()
