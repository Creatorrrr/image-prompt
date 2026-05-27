from __future__ import annotations

import importlib.util
import json
import random
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
TAGS_PATH = SKILL_DIR / "assets" / "photo_prompt_tags.json"
GENERATOR_PATH = SKILL_DIR / "scripts" / "prompt_generator.py"
WRAPPER_PATH = SKILL_DIR / "scripts" / "generate_photo_prompt.py"


def load_generator():
    spec = importlib.util.spec_from_file_location("photo_prompt_generator", GENERATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load generator module: {GENERATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PromptGeneratorRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.generator = load_generator()
        cls.data = json.loads(TAGS_PATH.read_text(encoding="utf-8"))

    def generate(self, preset: str, seed: int = 1, **kwargs):
        return self.generator.generate_once(
            data=self.data,
            rng=random.Random(seed),
            preset_id=preset,
            langs=["en"],
            include_negative=kwargs.pop("include_negative", True),
            negative_count=kwargs.pop("negative_count", 12),
            include_choices=kwargs.pop("include_choices", True),
            forced_choices=kwargs.pop("forced_choices", None),
            priority_bias=kwargs.pop("priority_bias", None),
            detail_level=kwargs.pop("detail_level", "detailed"),
            surreal_mode=kwargs.pop("surreal_mode", "off"),
            surreal_probability=kwargs.pop("surreal_probability", 0.35),
            surreal_intensity=kwargs.pop("surreal_intensity", "moderate"),
            reference_edit_mode=kwargs.pop("reference_edit_mode", "off"),
            trend_layer=kwargs.pop("trend_layer", "off"),
        )

    def test_nonhuman_subject_does_not_get_human_pose_guidance(self):
        item = self.generate(
            "street_documentary",
            seed=17,
            forced_choices={"subject": ["neon_sign"], "action": ["reflecting_puddle"]},
        )

        self.assertNotIn("pose, gaze, gesture", item["prompt_en"])
        self.assertIn("lettering or illuminated surfaces", item["prompt_en"])

    def test_food_subject_uses_food_guidance_and_food_negative_pool(self):
        item = self.generate(
            "food_editorial",
            seed=9,
            forced_choices={"subject": ["croissant"], "action": ["steam_rising"]},
        )

        self.assertNotIn("pose, gaze, gesture", item["prompt_en"])
        self.assertIn("edible detail", item["prompt_en"])
        self.assertNotIn("unrealistic hands", item["negative_en"])
        self.assertNotIn("broken facial features", item["negative_en"])

    def test_context_guard_blocks_lab_lighting_in_family_archive_cafe(self):
        item = self.generate("vintage_family_archive", seed=6)

        self.assertNotEqual(item["choices"].get("lighting", {}).get("id"), "lab_led")
        self.assertNotIn("laboratory equipment", item["prompt_en"])

    def test_context_guard_blocks_surveillance_composition_in_office_profile(self):
        item = self.generate("corporate_startup_profile", seed=12)

        self.assertNotEqual(item["choices"].get("composition", {}).get("id"), "bodycam_chest_height")

    def test_clean_mirror_selfie_has_no_adult_slots(self):
        item = self.generate("clean_mirror_selfie_snapshot", seed=5)

        self.assertNotIn("adult_context", item["choices"])
        self.assertNotIn("fetish_styling", item["choices"])
        self.assertNotIn("caption_context", item["choices"])
        self.assertNotIn("adult", item["prompt_en"].lower())
        self.assertNotIn("fetish", item["prompt_en"].lower())

    def test_forced_incompatible_choice_is_preserved_for_dictionary_testing(self):
        item = self.generate(
            "corporate_startup_profile",
            seed=12,
            forced_choices={"composition": ["bodycam_chest_height"]},
        )

        self.assertEqual(item["choices"].get("composition", {}).get("id"), "bodycam_chest_height")

    def test_reference_and_trend_layers_are_explicit_opt_in(self):
        item = self.generate(
            "candid_iphone_portrait",
            seed=3,
            reference_edit_mode="identity",
            trend_layer="scrapbook_collage",
        )

        self.assertIn("Reference-edit instruction", item["prompt_en"])
        self.assertIn("Trend layer", item["prompt_en"])
        self.assertIn("scrapbook collage", item["prompt_en"])

    def test_preset_filters_reference_existing_tag_ids(self):
        slots = self.data["slots"]
        for preset in self.data["presets"]:
            for slot, flt in preset.get("filters", {}).items():
                self.assertIn(slot, slots, f"{preset['id']} references missing slot {slot}")
                valid_ids = {entry.get("id") for entry in slots[slot]}
                for tag_id in flt.get("ids", []):
                    self.assertIn(tag_id, valid_ids, f"{preset['id']} {slot} references missing id {tag_id}")

    def test_negative_prompt_pools_are_localized(self):
        for pool_name, entries in self.data.get("negative_prompt_pools", {}).items():
            self.assertTrue(entries, pool_name)
            for entry in entries:
                self.assertTrue(entry.get("ko"), pool_name)
                self.assertTrue(entry.get("en"), pool_name)

    def test_indefinite_article_helper_handles_advertising_medium(self):
        self.assertEqual(
            self.generator.with_indefinite_article("advertising campaign photograph"),
            "an advertising campaign photograph",
        )

    def test_compact_prompt_is_single_paragraph_label_free_and_reactor_sized(self):
        item = self.generate(
            "compact_urban_fashion_portrait",
            seed=11,
            detail_level="compact",
            forced_choices={
                "subject": ["fashion_influencer"],
                "hair_style": ["long_black_twin_tails"],
                "prop": ["oversized_silver_toy_pistol"],
            },
        )

        prompt = item["prompt_en"]
        self.assertNotIn("\n", prompt)
        self.assertNotIn("Subject and state:", prompt)
        self.assertNotIn("Camera and composition:", prompt)
        self.assertNotIn("Texture, format, and finish:", prompt)
        self.assertGreaterEqual(len(prompt.split()), 45)
        self.assertLessEqual(len(prompt.split()), 140)
        self.assertIn("long black twin-tail hair", prompt)
        self.assertIn("oversized silver toy pistol prop", prompt)
        self.assertIn("no text or watermark", prompt)

    def test_compact_detail_level_is_available_through_wrapper(self):
        result = subprocess.run(
            [
                sys.executable,
                str(WRAPPER_PATH),
                "--preset",
                "compact_cinematic_prop_portrait",
                "--detail-level",
                "compact",
                "--seed",
                "7",
                "--lang",
                "en",
                "--plain",
                "--no-negative",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("EN:", result.stdout)
        self.assertNotIn("Subject and state:", result.stdout)

    def test_compact_slots_presets_and_formats_are_registered(self):
        slots = self.data["slots"]
        self.assertIn("prop", slots)
        self.assertIn("hair_style", slots)

        format_ids = {entry["id"] for entry in slots["format"]}
        self.assertTrue(
            {
                "portrait_3_4",
                "portrait_4_5",
                "multi_image_series",
                "four_cut_grid",
                "nine_cut_grid",
            }.issubset(format_ids)
        )

        preset_ids = {preset["id"] for preset in self.data["presets"]}
        self.assertTrue(
            {
                "compact_urban_fashion_portrait",
                "compact_cinematic_prop_portrait",
                "compact_multicut_portrait_series",
            }.issubset(preset_ids)
        )

    def test_product_commercial_excludes_food_subjects_but_food_editorial_keeps_them(self):
        product = self.generate("product_commercial", seed=1)
        food = self.generate("food_editorial", seed=1)

        self.assertNotIn("food", product["choices"]["subject"].get("kind", []))
        self.assertNotIn("food", product["choices"]["subject"].get("tags", []))
        self.assertIn("food", food["choices"]["subject"].get("kind", []) + food["choices"]["subject"].get("tags", []))


if __name__ == "__main__":
    unittest.main()
