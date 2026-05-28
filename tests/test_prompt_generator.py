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
REACTOR_EXPORT_PRESET_IDS = {
    "hanbok_seasonal_editorial",
    "wuxia_xianxia_portrait",
    "joseon_period_portrait",
    "hanfu_china_court_portrait",
    "maid_cafe_cosplay_portrait",
    "magical_girl_cosplay_portrait",
    "mecha_pilot_cosplay_portrait",
    "gothic_doll_cosplay_portrait",
    "game_rpg_cosplay_portrait",
    "casual_weapon_lifestyle",
    "kpop_album_cover_y2k_glossy",
    "kpop_dance_practice_room_mirror",
    "tv_music_show_stage_screencap",
    "korea_2000s_classroom_nostalgia",
    "korean_yearbook_senior_portrait",
    "wide_angle_mirror_selfie_editorial",
    "high_angle_floor_selfie",
    "korean_photobooth_strip",
    "kbeauty_idol_skincare_campaign",
    "soju_liquor_model_campaign",
    "vacuum_packaging_concept_photo",
    "action_figure_blister_product_photo",
    "amigurumi_plush_catalog_photo",
    "needle_felt_character_macro",
    "noodle_lettering_food_topdown",
    "cherry_blossom_romance_portrait",
    "autumn_foliage_warm_portrait",
    "flower_field_dreamcore_portrait",
    "foggy_mist_atmospheric_portrait",
    "blizzard_expedition_fashion_editorial",
    "desert_dune_editorial",
    "underwater_surface_portrait",
    "pool_deck_swimwear_editorial",
    "hotel_rooftop_dusk_editorial",
    "subway_interior_candid",
    "train_station_platform_portrait",
    "elevator_steel_box_portrait",
    "convenience_store_late_night",
    "pc_bang_neon_session",
    "karaoke_room_neon_friends",
    "pojangmacha_street_food_night",
    "gym_mirror_selfie_fitness",
    "motorcycle_rider_portrait_dusk",
    "esports_arena_live_show",
    "dark_academia_library_portrait",
    "double_exposure_silhouette_portrait",
    "color_gel_split_lighting_studio",
    "silhouette_window_backlight_portrait",
    "infrared_aerochrome_dreamscape",
    "tilt_shift_miniature_city",
    "reflection_puddle_inverted_portrait",
    "broken_glass_fragmented_portrait",
    "photo_collage_cutout_y2k",
    "vhs_camcorder_home_video",
    "taxi_backseat_night_portrait",
    "airplane_window_seat_lifestyle",
    "crime_scene_yellow_tape_reportage",
}
NON_PHOTO_RESERVED_PRESET_IDS = {
    "poster_advertising",
    "infographic_savepic",
    "messenger_sticker_sheet",
    "children_picturebook_illustration",
    "webtoon_panel_strip",
    "toy_figure_render",
    "poster_cinematic_cover",
    "exploded_anatomy_diagram",
    "ui_mock_screen_prompt",
    "minimal_typography_art_print",
}
REACTOR_EXPORT_REPRESENTATIVE_CASES = {
    "wuxia_xianxia_portrait": (
        {
            "costume_style": ["flowing_wuxia_robe"],
            "prop": ["jian_sword_prop"],
            "location": ["misty_xianxia_cliff"],
        },
        ["wuxia", "jian sword", "misty xianxia"],
    ),
    "kpop_album_cover_y2k_glossy": (
        {
            "world": ["kpop_y2k_album_world"],
            "prop": ["glass_soda_bottle_prop"],
            "format": ["square_album_jacket"],
        },
        ["K-pop", "Y2K", "square album jacket"],
    ),
    "korean_photobooth_strip": (
        {
            "format": ["nine_cut_grid"],
            "prop": ["photobooth_remote_prop"],
            "location": ["korean_photobooth_booth"],
        },
        ["Korean photobooth", "nine-cut"],
    ),
    "amigurumi_plush_catalog_photo": (
        {
            "subject": ["amigurumi_plush_doll"],
            "texture": ["crochet_yarn_texture"],
            "location": ["craft_catalog_tabletop"],
        },
        ["amigurumi", "crochet yarn"],
    ),
    "noodle_lettering_food_topdown": (
        {
            "subject": ["noodle_lettering_plate"],
            "action": ["arranged_as_lettering"],
            "camera_direction": ["top_down_90"],
        },
        ["noodle lettering", "top-down"],
    ),
    "double_exposure_silhouette_portrait": (
        {
            "composition": ["double_exposure_profile"],
            "texture": ["layered_film_exposure"],
            "mood": ["quiet_surreal_optical"],
        },
        ["double exposure", "layered film exposure"],
    ),
}
REACTOR_SPECIALIZED_CONTEXT_TAGS = {
    "lighting": {
        "misty_backlight",
        "oil_lamp_warm",
        "stage_led_rgb",
        "fluorescent_classroom_cool",
        "photobooth_flash",
        "beauty_white_studio_light",
        "blizzard_whiteout_light",
        "underwater_caustic_light",
        "harsh_noon",
        "neon_pc_monitor_glow",
        "karaoke_blacklight_neon",
        "cyan_magenta_split_light",
        "infrared_aerochrome_light",
        "window_blowout_backlight",
        "subway_car_fluorescent_light",
        "train_platform_fluorescent_light",
        "convenience_store_cool_led_light",
        "elevator_panel_overhead_light",
        "gym_overhead_led_light",
    },
    "light_direction": {
        "mist_backlight_direction",
        "window_blowout_backlight",
        "overhead_fluorescent_toplight",
        "low_neon_side_light",
    },
    "light_type": {
        "paper_lantern_light",
        "oil_lamp_practical",
        "broadcast_led_wall",
        "school_fluorescent_tube",
        "convenience_store_led",
        "subway_train_fluorescent",
        "elevator_panel_light",
        "pojangmacha_tent_light",
        "taxi_signal_light",
        "airplane_window_daylight",
    },
    "motion": {
        "fabric_drift",
        "sleeve_wave_motion",
        "robe_billow_motion",
        "petal_swirl_motion",
        "water_surface_ripple_motion",
        "long_exposure_streak",
        "vhs_interlace_smear",
    },
    "camera_type": {
        "broadcast_tv_camera",
        "vhs_camcorder_camera",
        "photobooth_camera",
    },
    "camera_direction": {
        "photobooth_front_direction",
        "practice_mirror_wide_direction",
        "broadcast_close_camera_direction",
        "floor_high_angle_direction",
        "taxi_backseat_window_direction",
        "airplane_window_side_direction",
    },
    "composition": {
        "square_album_cover_centered",
        "photobooth_grid_strip",
        "yearbook_centered_headshot",
        "blister_pack_centered_product",
        "vacuum_pack_flat_product",
        "double_exposure_profile",
        "split_color_gel_portrait",
        "window_silhouette_negative_space",
        "tilt_shift_overhead_city",
        "puddle_inverted_reflection",
        "broken_glass_fragments_frame",
        "scrapbook_photo_cutout_layout",
    },
    "lens": {
        "album_50mm_clean",
        "photobooth_fixed_lens",
        "topdown_macro_60mm",
    },
    "focus": {
        "album_cover_eye_focus",
        "photobooth_face_focus",
        "craft_macro_focus",
        "optical_layered_focus",
    },
    "texture": {
        "silk_hanbok_texture",
        "broadcast_camera_video",
        "crochet_yarn_texture",
        "needle_felt_fiber_texture",
        "clear_plastic_packaging_glare",
        "noodle_sauce_surface",
        "snow_whiteout_grain",
        "water_refraction_texture",
        "layered_film_exposure",
        "vhs_scanline_texture",
        "aerochrome_film_texture",
        "broken_glass_refraction",
        "glitter_dust",
    },
    "format": {
        "square_album_jacket",
        "photobooth_strip_layout",
        "broadcast_screencap_lower_third_safe",
        "vhs_date_overlay_free",
        "passport_centered_no_text",
        "collage_cutout_photo_series",
    },
}
CONTEXT_GUARD_GENERAL_PRESETS = {
    "vintage_family_archive",
    "corporate_startup_profile",
}
REACTOR_LOCAL_PRESET_EXPECTATIONS = {
    "convenience_store_late_night": {
        "subject": {"convenience_store_customer"},
        "composition": {"handheld_candid", "medium_close", "wide_establishing", "rule_of_thirds"},
        "light_type": {"convenience_store_led"},
    },
    "train_station_platform_portrait": {
        "subject": {"train_platform_commuter"},
        "composition": {"handheld_candid", "medium_close", "wide_establishing", "frame_within_frame"},
        "light_type": {"subway_train_fluorescent", "streetlamp"},
    },
    "motorcycle_rider_portrait_dusk": {
        "composition": {"handheld_candid", "medium_close", "wide_establishing", "rule_of_thirds"},
        "light_type": {"streetlamp", "car_headlights", "neon_sign_light"},
    },
    "dark_academia_library_portrait": {
        "composition": {"medium_close", "frame_within_frame", "centered_symmetric", "rule_of_thirds"},
        "light_type": {"tungsten_practical", "candlelight", "oil_lamp_practical"},
    },
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

    def test_reactor_export_presets_are_registered_without_non_photo_presets(self):
        preset_ids = {preset["id"] for preset in self.data["presets"]}

        self.assertTrue(REACTOR_EXPORT_PRESET_IDS.issubset(preset_ids))
        self.assertTrue(NON_PHOTO_RESERVED_PRESET_IDS.isdisjoint(preset_ids))

        for preset_id in REACTOR_EXPORT_PRESET_IDS:
            preset = next(preset for preset in self.data["presets"] if preset["id"] == preset_id)
            self.assertLessEqual(preset["weight"], 0.6, preset_id)

    def test_reactor_export_presets_generate_across_detail_levels(self):
        for preset_id in sorted(REACTOR_EXPORT_PRESET_IDS):
            for detail_level in ("detailed", "compact"):
                with self.subTest(preset_id=preset_id, detail_level=detail_level):
                    item = self.generate(
                        preset_id,
                        seed=1,
                        detail_level=detail_level,
                        include_negative=False,
                    )
                    prompt = item["prompt_en"]

                    self.assertIn("prompt_en", item)
                    self.assertIn("no text", prompt.lower())
                    self.assertIn("watermark", prompt.lower())

    def test_reactor_export_representative_presets_include_core_vocab(self):
        for preset_id, (forced_choices, expected_phrases) in REACTOR_EXPORT_REPRESENTATIVE_CASES.items():
            with self.subTest(preset_id=preset_id):
                item = self.generate(
                    preset_id,
                    seed=1,
                    detail_level="compact",
                    include_negative=False,
                    forced_choices=forced_choices,
                )
                prompt = item["prompt_en"]

                for phrase in expected_phrases:
                    self.assertIn(phrase, prompt)

    def test_reactor_export_presets_do_not_leak_adult_only_slots(self):
        adult_only_slots = {"adult_context", "fetish_styling", "body_framing", "caption_context"}

        for preset_id in sorted(REACTOR_EXPORT_PRESET_IDS):
            preset = next(preset for preset in self.data["presets"] if preset["id"] == preset_id)
            all_slots = preset.get("required_slots", []) + [
                item["slot"] for item in preset.get("optional_slots", [])
            ]
            self.assertTrue(adult_only_slots.isdisjoint(all_slots), preset_id)

            with self.subTest(preset_id=preset_id):
                for seed in range(1, 8):
                    item = self.generate(preset_id, seed=seed, detail_level="compact")

                    self.assertTrue(adult_only_slots.isdisjoint(item["choices"]), preset_id)

    def test_reactor_export_specialized_tags_have_context_guards(self):
        for slot, tag_ids in REACTOR_SPECIALIZED_CONTEXT_TAGS.items():
            entries = {entry["id"]: entry for entry in self.data["slots"][slot]}
            for tag_id in tag_ids:
                with self.subTest(slot=slot, tag_id=tag_id):
                    self.assertIn(tag_id, entries)
                    self.assertTrue(entries[tag_id].get("requires_any_tags"), tag_id)

    def test_general_presets_do_not_sample_specialized_reactor_context_tags(self):
        for preset_id in sorted(CONTEXT_GUARD_GENERAL_PRESETS):
            for seed in range(1, 81):
                with self.subTest(preset_id=preset_id, seed=seed):
                    item = self.generate(preset_id, seed=seed, detail_level="compact")

                    for slot, disallowed_ids in REACTOR_SPECIALIZED_CONTEXT_TAGS.items():
                        selected = item["choices"].get(slot, {}).get("id")
                        self.assertNotIn(selected, disallowed_ids)

    def test_reactor_local_presets_use_contextual_subjects_and_compositions(self):
        presets = {preset["id"]: preset for preset in self.data["presets"]}
        for preset_id, expectations in REACTOR_LOCAL_PRESET_EXPECTATIONS.items():
            preset = presets[preset_id]
            filters = preset.get("filters", {})
            for slot, expected_ids in expectations.items():
                with self.subTest(preset_id=preset_id, slot=slot):
                    self.assertEqual(set(filters[slot]["ids"]), expected_ids)

    def test_tilt_shift_miniature_city_uses_environment_subject(self):
        item = self.generate("tilt_shift_miniature_city", seed=3, detail_level="compact")
        subject = item["choices"]["subject"]

        self.assertIn("environment", subject.get("kind", []) + subject.get("tags", []))
        self.assertNotIn("human", subject.get("kind", []))
        self.assertNotIn("pose, gaze, gesture", item["prompt_en"])

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
