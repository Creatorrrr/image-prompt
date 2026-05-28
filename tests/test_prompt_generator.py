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

CREATIVE_PRESET_IDS = {
    "cinematic_fantasy_portrait",
    "retro_era_fashion_editorial",
    "surreal_contrast_editorial",
}
FANTASY_PROPS = {
    "cosplay_prop_katana",
    "cosplay_prop_broadsword",
    "fantasy_costume_staff",
    "glowing_lantern_prop",
}
COSMIC_EXTREME_LOCATIONS = {
    "antarctic_ice_landscape",
    "glacier_face_wall",
    "volcanic_rim_dusk",
    "salt_flats_mirror",
    "deep_canyon_floor",
    "milky_way_meadow_night",
    "aurora_borealis_field",
    "frozen_lake_surface",
}
ERA_WORLDS = {
    "eighties_glam_editorial",
    "nineties_grunge_editorial",
    "y2k_chrome_editorial",
}
CONTRAST_PROPS = {
    "melting_pastel_ice_cream_cone",
    "oversized_lollipop_prop",
    "glowing_lantern_prop",
}
SURREAL_LAYER_SLOTS = {
    "surreal_concept",
    "surreal_anchor",
    "scale_relation",
    "surreal_physics_detail",
}


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

    def generate_langs(self, preset: str, langs: list[str], seed: int = 1, **kwargs):
        return self.generator.generate_once(
            data=self.data,
            rng=random.Random(seed),
            preset_id=preset,
            langs=langs,
            include_negative=kwargs.pop("include_negative", False),
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
        self.assertIn("wardrobe_style", slots)
        self.assertIn("makeup_style", slots)
        self.assertIn("expression", slots)
        self.assertIn("subject_framing", slots)

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

    def test_reactor_neutral_slots_are_visible_in_cli(self):
        result = subprocess.run(
            [sys.executable, str(WRAPPER_PATH), "--show-slots", "--plain"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        for slot in ("wardrobe_style", "makeup_style", "expression", "subject_framing"):
            self.assertIn(f"{slot}:", result.stdout)

        tags = subprocess.run(
            [sys.executable, str(WRAPPER_PATH), "--list-tags", "wardrobe_style", "--plain"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(tags.returncode, 0, tags.stderr)
        self.assertIn("casual_bomber_jacket_miniskirt", tags.stdout)

    def test_compact_prompt_includes_forced_neutral_reactor_slots(self):
        item = self.generate(
            "compact_urban_fashion_portrait",
            seed=11,
            detail_level="compact",
            forced_choices={
                "wardrobe_style": ["casual_bomber_jacket_miniskirt"],
                "makeup_style": ["delicate_makeup_glossy_lips"],
                "expression": ["calm_intense_gaze"],
                "subject_framing": ["full_body_framing"],
                "prop": ["compact_digital_camera"],
            },
        )

        prompt = item["prompt_en"]
        self.assertIn("navy bomber jacket with a casual mini skirt", prompt)
        self.assertIn("delicate makeup with glossy lips", prompt)
        self.assertIn("calm intense gaze", prompt)
        self.assertIn("full-body framing", prompt)
        self.assertIn("small compact digital camera", prompt)

    def test_neutral_wardrobe_and_framing_do_not_inject_adult_only_language(self):
        item = self.generate(
            "clean_mirror_selfie_snapshot",
            seed=8,
            detail_level="compact",
            forced_choices={
                "wardrobe_style": ["hoodie_shorts_sneakers"],
                "subject_framing": ["upper_body_framing"],
                "expression": ["neutral_camera_gaze"],
            },
        )

        prompt = item["prompt_en"].lower()
        self.assertNotIn("adult", prompt)
        self.assertNotIn("fetish", prompt)
        self.assertNotIn("thirst trap", prompt)
        self.assertNotIn("adult_context", item["choices"])
        self.assertNotIn("fetish_styling", item["choices"])

    def test_creative_photo_presets_are_registered_and_non_adult(self):
        preset_ids = {preset["id"] for preset in self.data["presets"]}
        self.assertTrue(CREATIVE_PRESET_IDS.issubset(preset_ids))

        for preset_id in CREATIVE_PRESET_IDS:
            preset = next(preset for preset in self.data["presets"] if preset["id"] == preset_id)
            self.assertLessEqual(preset["weight"], 0.6)
            all_slots = preset.get("required_slots", []) + [
                item["slot"] for item in preset.get("optional_slots", [])
            ]
            self.assertNotIn("adult_context", all_slots)
            self.assertNotIn("fetish_styling", all_slots)
            self.assertNotIn("caption_context", all_slots)

            for seed in range(1, 4):
                item = self.generate(preset_id, seed=seed, detail_level="compact")
                self.assertNotIn("adult_context", item["choices"])
                self.assertNotIn("fetish_styling", item["choices"])
                self.assertNotIn("caption_context", item["choices"])

    def test_cinematic_fantasy_portrait_uses_fantasy_prop_or_extreme_location(self):
        item = self.generate("cinematic_fantasy_portrait", seed=3, detail_level="compact")
        prop_id = item["choices"].get("prop", {}).get("id")
        location_id = item["choices"].get("location", {}).get("id")

        self.assertTrue(prop_id in FANTASY_PROPS or location_id in COSMIC_EXTREME_LOCATIONS)

    def test_retro_era_fashion_editorial_uses_era_world(self):
        item = self.generate("retro_era_fashion_editorial", seed=4, detail_level="compact")

        self.assertIn(item["choices"]["world"]["id"], ERA_WORLDS)

    def test_surreal_contrast_editorial_uses_photo_contrast_not_surreal_layer(self):
        item = self.generate("surreal_contrast_editorial", seed=5, detail_level="compact")

        self.assertIn(item["choices"]["location"]["id"], COSMIC_EXTREME_LOCATIONS)
        self.assertIn(item["choices"]["prop"]["id"], CONTRAST_PROPS)
        for slot in SURREAL_LAYER_SLOTS:
            self.assertNotIn(slot, item["choices"])

    def test_product_commercial_excludes_food_subjects_but_food_editorial_keeps_them(self):
        product = self.generate("product_commercial", seed=1)
        food = self.generate("food_editorial", seed=1)

        self.assertNotIn("food", product["choices"]["subject"].get("kind", []))
        self.assertNotIn("food", product["choices"]["subject"].get("tags", []))
        self.assertIn("food", food["choices"]["subject"].get("kind", []) + food["choices"]["subject"].get("tags", []))

    def test_cross_mode_preserves_forced_prompt_facts(self):
        forced = {
            "subject": ["fashion_model"],
            "action": ["taking_selfie"],
            "prop": ["camera_held_as_prop"],
            "location": ["creator_room"],
            "lighting": ["softbox"],
            "light_type": ["ring_light"],
            "camera_type": ["smartphone_camera"],
            "composition": ["vertical_centered_caption_space"],
            "color": ["phone_hdr_color"],
            "mood": ["aspirational_lifestyle"],
            "texture": ["clean_digital"],
        }
        expected_phrases = {
            "en": [
                "a fashion model",
                "taking an arm-length selfie",
                "a camera held as a visible prop",
                "a creator room with LED lights",
                "large softbox lighting",
                "ring light with circular catchlights",
                "a native smartphone camera",
                "vertical centered framing with room for captions",
                "crisp smartphone HDR color",
                "aspirational lifestyle mood",
                "clean digital image quality",
            ],
            "ko": [
                "패션 모델",
                "팔을 뻗어 셀피를 찍는",
                "손에 든 카메라 소품",
                "LED 조명이 켜진 크리에이터 방",
                "대형 소프트박스 조명",
                "눈동자에 원형 반사가 생기는 링라이트",
                "스마트폰 기본 카메라",
                "자막 공간을 남긴 세로 중앙 구도",
                "스마트폰 HDR 특유의 선명한 색감",
                "동경을 부르는 라이프스타일 무드",
                "깨끗한 디지털 이미지",
            ],
        }

        for detail_level in ("detailed", "standard", "compact"):
            with self.subTest(detail_level=detail_level):
                item = self.generate_langs(
                    "compact_urban_fashion_portrait",
                    langs=["ko", "en"],
                    seed=21,
                    detail_level=detail_level,
                    forced_choices=forced,
                )
                for lang, phrases in expected_phrases.items():
                    prompt = item[f"prompt_{lang}"]
                    for phrase in phrases:
                        self.assertIn(phrase, prompt)

    def test_all_detail_levels_include_common_inline_constraints(self):
        for detail_level in ("detailed", "standard", "compact"):
            with self.subTest(detail_level=detail_level):
                item = self.generate_langs(
                    "compact_urban_fashion_portrait",
                    langs=["ko", "en"],
                    seed=22,
                    detail_level=detail_level,
                )

                self.assertIn("no text", item["prompt_en"].lower())
                self.assertIn("watermark", item["prompt_en"].lower())
                self.assertIn("텍스트", item["prompt_ko"])
                self.assertIn("워터마크", item["prompt_ko"])

    def test_cross_mode_section_order_is_stable(self):
        forced = {
            "subject": ["fashion_model"],
            "location": ["creator_room"],
            "camera_type": ["smartphone_camera"],
            "lighting": ["softbox"],
            "texture": ["clean_digital"],
        }

        for detail_level in ("detailed", "standard", "compact"):
            with self.subTest(detail_level=detail_level):
                item = self.generate_langs(
                    "compact_urban_fashion_portrait",
                    langs=["ko", "en"],
                    seed=23,
                    detail_level=detail_level,
                    forced_choices=forced,
                    include_negative=False,
                )

                markers = {
                    "en": (
                        "a fashion model",
                        "a creator room with LED lights",
                        "a native smartphone camera",
                        "large softbox lighting",
                        "no text",
                    ),
                    "ko": (
                        "패션 모델",
                        "LED 조명이 켜진 크리에이터 방",
                        "스마트폰 기본 카메라",
                        "대형 소프트박스 조명",
                        "텍스트",
                    ),
                }
                for lang, phrases in markers.items():
                    prompt = item[f"prompt_{lang}"]
                    subject_index = prompt.index(phrases[0])
                    scene_index = prompt.index(phrases[1])
                    camera_index = prompt.index(phrases[2])
                    lighting_index = prompt.index(phrases[3])
                    constraint_index = prompt.lower().index(phrases[4])
                    self.assertLess(subject_index, scene_index)
                    self.assertLess(scene_index, camera_index)
                    self.assertLess(camera_index, lighting_index)
                    self.assertLess(lighting_index, constraint_index)

    def test_detailed_prompt_surfaces_prop(self):
        item = self.generate(
            "compact_urban_fashion_portrait",
            seed=24,
            detail_level="detailed",
            forced_choices={"prop": ["camera_held_as_prop"]},
            include_negative=False,
        )

        self.assertIn("a camera held as a visible prop", item["prompt_en"])

    def test_reference_and_trend_layers_are_rendered_in_all_detail_levels(self):
        for detail_level in ("detailed", "standard", "compact"):
            with self.subTest(detail_level=detail_level):
                item = self.generate(
                    "candid_iphone_portrait",
                    seed=25,
                    detail_level=detail_level,
                    reference_edit_mode="identity",
                    trend_layer="scrapbook_collage",
                    include_negative=False,
                )

                self.assertIn("Reference-edit instruction", item["prompt_en"])
                self.assertIn("Trend layer", item["prompt_en"])
                self.assertIn("scrapbook collage", item["prompt_en"])

    def test_compact_prompt_keeps_required_sections_when_many_optional_slots_are_forced(self):
        item = self.generate(
            "compact_urban_fashion_portrait",
            seed=26,
            detail_level="compact",
            forced_choices={
                "subject": ["fashion_model"],
                "action": ["taking_selfie"],
                "prop": ["camera_held_as_prop"],
                "location": ["creator_room"],
                "lighting": ["softbox"],
                "light_direction": ["front_light"],
                "light_type": ["ring_light"],
                "light_intensity": ["high_key_bright"],
                "light_shape": ["large_softbox_shape"],
                "camera_type": ["smartphone_camera"],
                "camera_direction": ["eye_level_front"],
                "composition": ["vertical_centered_caption_space"],
                "subject_framing": ["full_body_framing"],
                "lens": ["phone_1x_main"],
                "focus": ["eye_focus"],
                "motion": ["handheld_microshake"],
                "color": ["phone_hdr_color"],
                "mood": ["aspirational_lifestyle"],
                "texture": ["clean_digital"],
                "format": ["portrait_4_5"],
                "quality": ["photoreal"],
            },
            include_negative=False,
        )

        prompt = item["prompt_en"]
        self.assertLessEqual(len(prompt.split()), 140)
        for phrase in (
            "a fashion model",
            "taking an arm-length selfie",
            "a camera held as a visible prop",
            "a creator room with LED lights",
            "large softbox lighting",
            "no text or watermark",
        ):
            self.assertIn(phrase, prompt)


if __name__ == "__main__":
    unittest.main()
