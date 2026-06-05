from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import os
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
TAGS_PATH = SKILL_DIR / "assets" / "photo_prompt_tags.json"
GENERATOR_PATH = SKILL_DIR / "scripts" / "prompt_generator.py"
WRAPPER_PATH = SKILL_DIR / "scripts" / "generate_photo_prompt.py"
RECORD_RUN_PATH = SKILL_DIR / "scripts" / "record_image_run.py"
VALIDATOR_PATH = SKILL_DIR / "scripts" / "validate_photo_prompt_dictionary.py"
INDEX_BUILDER_PATH = SKILL_DIR / "scripts" / "build_semantic_index.py"

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
EXPANDED_SLOT_IDS = {
    "film_emulation",
    "weather",
    "time_of_day",
    "wearable_accessory",
    "facial_hair",
    "surface_material",
    "aesthetic_trend",
}
EXPANDED_PRESET_IDS = {
    "analog_personal_brand_portrait",
    "cinestill_neon_diner_portrait",
    "cinematic_blue_hour_street",
    "rainy_bus_stop_noir",
    "film_wedding_afterparty_flash",
    "quiet_luxury_founder_profile",
    "office_siren_corporate_editorial",
    "coquette_cafe_portrait",
    "balletcore_rehearsal_room",
    "gorpcore_mountain_lifestyle",
    "night_laundromat_candid",
    "hotel_corridor_liminal_portrait",
    "aquarium_tunnel_portrait",
    "botanical_greenhouse_editorial",
    "documentary_craftsperson_workshop",
    "product_packshot_white_sweep",
    "product_flatlay_ingredient_story",
    "cpg_shelf_lifestyle_hero",
    "jewelry_macro_reflection",
    "skincare_bathroom_countertop",
    "cinematic_product_reflection_stage",
    "creator_desk_setup_flatlay",
}
EXPANDED_FAMILY_IDS = {
    "analog_film_family",
    "weather_mood_portrait_family",
    "product_surface_family",
    "creator_branding_family",
    "craft_workshop_family",
    "transport_night_family",
}
EXPANDED_UNIQUE_TAG_IDS = {
    "kodak_portra_400_look",
    "cinestill_800t_halation",
    "light_drizzle",
    "time_blue_hour",
    "wireframe_round_glasses",
    "clean_shaven",
    "white_marble_surface",
    "quiet_luxury_aesthetic",
    "smoky_eye_makeup",
    "candid_laugh",
    "two_block_korean_cut",
    "rembrandt_lighting",
    "probe_lens_macro",
    "knee_up_framing",
    "light_leak_burn",
    "glassblower_artisan",
    "laundromat_night",
    "disposable_camera",
}
SOCIAL_CHARACTER_SLOT_IDS = {"hair_color", "capture_context"}
SOCIAL_CHARACTER_PRESET_IDS = {
    "garden_phone_backlight_portrait",
    "gothic_curio_bunny_cosplay",
    "anime_poster_low_angle_noir_fashion",
    "gas_station_passenger_seat_lifestyle",
    "blue_rimlight_character_cosplay",
    "clean_uniform_vsign_selfie",
    "adult_crouching_mirror_ribbon_fashion",
    "botanical_greenhouse_soft_romance",
    "phone_screen_face_overlay_cosplay",
    "interactive_2_5d_living_room_pov",
}
SOCIAL_CHARACTER_TAG_IDS = {
    "hair_color": {
        "glossy_black_hair",
        "soft_dark_brown_hair",
        "silver_blonde_gothic_hair",
        "pale_blue_cosplay_wig",
        "mint_green_cosplay_wig",
        "lavender_silver_character_hair",
        "warm_auburn_brown_hair",
    },
    "capture_context": {
        "front_camera_close_selfie",
        "mirror_crouch_selfie_context",
        "phone_screen_face_overlay_context",
        "first_person_hand_interaction_context",
        "passenger_seat_observed_candid",
        "low_angle_dominance_capture",
        "cosplay_reference_realism_context",
        "botanical_editorial_portrait_context",
        "social_perspective_trick_context",
    },
}
SOCIAL_CHARACTER_EXISTING_SLOT_TAG_IDS = {
    "action": {
        "holding_phone_in_garden_backlight",
        "holding_ornate_bottle_to_chest",
        "looking_down_at_low_camera",
        "passenger_seat_coffee_window_gaze",
        "over_shoulder_floor_turn",
        "front_camera_v_sign_cheek",
        "seated_botanical_cheek_rest",
        "phone_screen_face_overlay_pose",
        "reacting_to_pov_hand_tail_pull",
    },
    "prop": {
        "clear_case_smartphone",
        "ornate_gothic_perfume_bottle",
        "anime_poster_wall",
        "takeaway_coffee_cup",
        "phone_with_anime_face_screen",
        "angel_halo_wings_tail_set",
        "red_ribbon_leg_wrap_adult",
        "lanyard_badge",
    },
    "location": {
        "garden_cafe_path_backlight",
        "gothic_glass_curio_cabinet",
        "anime_poster_wall_interior",
        "gas_station_car_passenger_seat_night",
        "blue_rimlight_cosplay_studio",
        "simple_indoor_selfie_room",
        "plain_wall_mirror_selfie_room",
        "botanical_greenhouse_deck_floor",
        "otaku_living_room_sofa_tv",
    },
    "camera_direction": {
        "extreme_low_angle_under_subject",
        "passenger_seat_side_profile_view",
        "phone_screen_overlay_close_pov",
        "first_person_pov_hand_foreground",
        "over_shoulder_back_seated",
    },
    "composition": {
        "cheek_close_selfie_crop",
        "crouching_mirror_full_body",
    },
    "lighting": {
        "soft_overexposed_garden_backlight",
        "cool_blue_character_rimlight",
        "gas_station_fluorescent_car_mix",
        "greenhouse_diffused_leaf_light",
    },
    "light_type": {
        "phone_screen_face_glow",
    },
    "light_shape": {
        "glass_curio_specular_sparkle",
        "hairline_rim_glow",
        "screen_rectangle_mask",
        "leaf_foreground_bokeh",
    },
    "texture": {
        "phone_beauty_filter_smoothing",
        "cosplay_wig_fiber_detail",
    },
}


def load_generator():
    spec = importlib.util.spec_from_file_location("photo_prompt_generator", GENERATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load generator module: {GENERATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_wrapper():
    spec = importlib.util.spec_from_file_location("photo_prompt_generator_wrapper", WRAPPER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load wrapper module: {WRAPPER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_index_builder():
    scripts_dir = str(SKILL_DIR / "scripts")
    inserted = False
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
        inserted = True
    try:
        spec = importlib.util.spec_from_file_location("photo_prompt_index_builder", INDEX_BUILDER_PATH)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Could not load index builder module: {INDEX_BUILDER_PATH}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        if inserted:
            sys.path.remove(scripts_dir)


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
            intent=kwargs.pop("intent", None),
            concept_locks=kwargs.pop("concept_locks", None),
            selection_mode=kwargs.pop("selection_mode", "rule"),
            novelty=kwargs.pop("novelty", "medium"),
            filter_strictness=kwargs.pop("filter_strictness", None),
            semantic_weight=kwargs.pop("semantic_weight", None),
            semantic_profile=kwargs.pop("semantic_profile", None),
            include_trace=kwargs.pop("include_trace", False),
            llm_polish=kwargs.pop("llm_polish", "off"),
            semantic_index=kwargs.pop("semantic_index", None),
            gemini_api_key=kwargs.pop("gemini_api_key", None),
            semantic_axis_mode=kwargs.pop("semantic_axis_mode", "auto"),
            intent_axes=kwargs.pop("intent_axes", None),
            intent_steering=kwargs.pop("intent_steering", None),
            surreal_mode_explicit=kwargs.pop("surreal_mode_explicit", False),
            semantic_defaulted=kwargs.pop("semantic_defaulted", False),
            intent_source=kwargs.pop("intent_source", "user"),
            requested_selection_mode=kwargs.pop("requested_selection_mode", None),
            batch_context=kwargs.pop("batch_context", None),
            batch_index=kwargs.pop("batch_index", 0),
            additional_requirements=kwargs.pop("additional_requirements", None),
            likeness_mode=kwargs.pop("likeness_mode", "off"),
            source_argv=kwargs.pop("source_argv", None),
            seed=seed,
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
            intent=kwargs.pop("intent", None),
            concept_locks=kwargs.pop("concept_locks", None),
            selection_mode=kwargs.pop("selection_mode", "rule"),
            novelty=kwargs.pop("novelty", "medium"),
            filter_strictness=kwargs.pop("filter_strictness", None),
            semantic_weight=kwargs.pop("semantic_weight", None),
            semantic_profile=kwargs.pop("semantic_profile", None),
            include_trace=kwargs.pop("include_trace", False),
            llm_polish=kwargs.pop("llm_polish", "off"),
            semantic_index=kwargs.pop("semantic_index", None),
            gemini_api_key=kwargs.pop("gemini_api_key", None),
            semantic_axis_mode=kwargs.pop("semantic_axis_mode", "auto"),
            intent_axes=kwargs.pop("intent_axes", None),
            intent_steering=kwargs.pop("intent_steering", None),
            surreal_mode_explicit=kwargs.pop("surreal_mode_explicit", False),
            semantic_defaulted=kwargs.pop("semantic_defaulted", False),
            intent_source=kwargs.pop("intent_source", "user"),
            requested_selection_mode=kwargs.pop("requested_selection_mode", None),
            batch_context=kwargs.pop("batch_context", None),
            batch_index=kwargs.pop("batch_index", 0),
            additional_requirements=kwargs.pop("additional_requirements", None),
            likeness_mode=kwargs.pop("likeness_mode", "off"),
            source_argv=kwargs.pop("source_argv", None),
            seed=seed,
        )

    def fake_gemini_vectors(self, texts, model=None, dimensions=768, api_key=None, **kwargs):
        vectors = []
        for text in texts:
            digest = hashlib.sha256(str(text).encode("utf-8")).digest()
            vector = [0.0] * dimensions
            for index, byte in enumerate(digest):
                vector[(byte + index) % dimensions] += 1.0 if index % 2 == 0 else -1.0
            norm = sum(value * value for value in vector) ** 0.5
            vectors.append([round(value / norm, 6) if norm else 0.0 for value in vector])
        return vectors

    def build_mock_semantic_index(self, dimensions: int = 768):
        original_embedder = self.generator.embed_texts_with_gemini
        self.generator.embed_texts_with_gemini = self.fake_gemini_vectors
        try:
            return self.generator.build_semantic_index_payload(
                self.data,
                provider="gemini",
                model="gemini-embedding-2",
                dimensions=dimensions,
                api_key="test-api-key",
            )
        finally:
            self.generator.embed_texts_with_gemini = original_embedder

    def run_wrapper_json(self, *args: str):
        result = subprocess.run(
            [sys.executable, str(WRAPPER_PATH), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

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

    def test_concept_lock_is_rendered_before_generated_details(self):
        concept = "방구석 집돌이, small lived-in bedroom, game controller, snacks, blanket"
        semantic_index = self.build_mock_semantic_index()
        original_embedder = self.generator.embed_texts_with_gemini
        self.generator.embed_texts_with_gemini = self.fake_gemini_vectors
        try:
            item = self.generate(
                "interior_lifestyle",
                seed=20260602,
                detail_level="detailed",
                forced_choices={
                    "subject": ["gamer_streamer"],
                    "action": ["editing_laptop"],
                    "location": ["cozy_apartment"],
                    "lighting": ["monitor_glow"],
                },
                intent=concept,
                selection_mode="semantic",
                semantic_index=semantic_index,
                gemini_api_key="test-api-key",
                concept_locks=[concept],
                include_trace=True,
            )
        finally:
            self.generator.embed_texts_with_gemini = original_embedder

        prompt = item["prompt_en"]
        self.assertIn(f"Core concept lock: {concept}.", prompt)
        self.assertIn("support for this concept, not a replacement", prompt)
        self.assertLess(prompt.index("Core concept lock:"), prompt.index("Subject and state:"))
        self.assertIn("editing content on a laptop", prompt)
        self.assertEqual(item["semantic_trace"]["generation_contract"]["concept_locks"], [concept])

    def test_compact_concept_lock_stays_label_free_and_single_paragraph(self):
        concept = "quiet homebody in a small bedroom"
        item = self.generate(
            "compact_urban_fashion_portrait",
            seed=12,
            detail_level="compact",
            concept_locks=[concept],
        )

        prompt = item["prompt_en"]
        self.assertNotIn("\n", prompt)
        self.assertNotIn("Core concept lock:", prompt)
        self.assertIn(f"preserving the core concept of {concept}", prompt)

    def test_provenance_ids_are_based_on_rendered_prompt_text(self):
        source_argv = ["--preset", "compact_urban_fashion_portrait", "--seed", "31"]
        item = self.generate(
            "compact_urban_fashion_portrait",
            seed=31,
            detail_level="compact",
            source_argv=source_argv,
        )

        provenance = item["provenance"]
        self.assertRegex(provenance["prompt_id"], r"^[0-9a-f]{16}$")
        self.assertEqual(provenance["prompt_id"], hashlib.sha256(item["prompt_en"].encode("utf-8")).hexdigest()[:16])
        self.assertEqual(provenance["negative_id"], hashlib.sha256(item["negative_en"].encode("utf-8")).hexdigest()[:16])
        self.assertEqual(provenance["seed"], 31)
        self.assertEqual(provenance["argv"], source_argv)
        self.assertEqual(provenance["preset_id"], item["preset_id"])

    def test_additional_requirements_and_likeness_mode_are_rendered_before_hashing(self):
        item = self.generate(
            "compact_urban_fashion_portrait",
            seed=32,
            detail_level="compact",
            additional_requirements=["coal miner workwear", "mining helmet with headlamp"],
            likeness_mode="inspired",
            include_trace=True,
        )

        prompt = item["prompt_en"]
        self.assertIn("Additional requirements: coal miner workwear; mining helmet with headlamp.", prompt)
        self.assertIn("an original adult fictional person, not an exact likeness", prompt)
        self.assertEqual(item["provenance"]["prompt_id"], hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16])
        self.assertEqual(item["provenance"]["additional_requirements"], ["coal miner workwear", "mining helmet with headlamp"])
        self.assertEqual(item["provenance"]["likeness_mode"], "inspired")
        self.assertEqual(
            item["semantic_trace"]["generation_contract"]["additional_requirements"],
            ["coal miner workwear", "mining helmet with headlamp"],
        )
        self.assertEqual(item["semantic_trace"]["generation_contract"]["likeness_mode"], "inspired")

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
                "--selection-mode",
                "rule",
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

    def test_concept_lock_is_available_through_wrapper(self):
        result = subprocess.run(
            [
                sys.executable,
                str(WRAPPER_PATH),
                "--preset",
                "interior_lifestyle",
                "--selection-mode",
                "rule",
                "--concept-lock",
                "방구석 집돌이",
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
        self.assertIn("Core concept lock: 방구석 집돌이", result.stdout)

    def test_concept_recipe_explain_expands_korean_role_to_forward_args(self):
        result = subprocess.run(
            [
                sys.executable,
                str(WRAPPER_PATH),
                "--concept",
                "유나 바니걸",
                "--explain-concept",
                "--selection-mode",
                "rule",
                "--plain",
                "--no-negative",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["concepts"][0]["name"], "유나")
        self.assertEqual(payload["concepts"][0]["role"], "바니걸")
        self.assertIn("--concept-lock", payload["forward_args"])
        self.assertIn("유나 바니걸", payload["forward_args"])
        self.assertIn("costume_style=bunny_girl_costume", payload["forward_args"])
        self.assertIn("covered adult bunny-girl stage costume", payload["forward_args"])
        self.assertIn("--likeness-mode", payload["forward_args"])
        self.assertIn("inspired", payload["forward_args"])
        self.assertNotIn("expression=cold_unreadable_stare", payload["forward_args"])
        self.assertNotIn("hiding in plain sight", " ".join(payload["forward_args"]))

    def test_concept_recipe_expands_vampire_as_non_graphic_mixin(self):
        payload = self.run_wrapper_json(
            "--concept",
            "흡혈귀",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--seed",
            "77",
            "--plain",
            "--no-negative",
        )

        concept = payload["concepts"][0]
        self.assertEqual(concept["name"], "흡혈귀")
        self.assertIsNone(concept["role"])
        self.assertIsNone(concept["applied_role"])
        self.assertEqual(concept["applied_mixins"], ["흡혈귀"])
        self.assertTrue(concept["matched"])
        self.assertEqual(concept["mixins"]["흡혈귀"]["preset"], "gothic_doll_cosplay_portrait")
        self.assertEqual(concept["combined_forced_slots"]["appearance_type"], ["classic_elegant"])
        self.assertEqual(concept["combined_forced_slots"]["expression"], ["calm_intense_gaze"])
        self.assertEqual(concept["combined_forced_slots"]["light_intensity"], ["deep_shadow_detail"])
        self.assertEqual(len(concept["selected_bundles"]), 1)
        bundle = concept["selected_bundles"][0]
        self.assertEqual(bundle["mixin"], "흡혈귀")
        self.assertTrue(bundle["bundle_id"].startswith("standalone_"))
        self.assertIn("--concept-lock", payload["forward_args"])
        self.assertIn("흡혈귀", payload["forward_args"])
        joined = " ".join(payload["forward_args"])
        self.assertIn("immortal nocturnal aristocrat", joined)
        self.assertIn("positive visible supernatural anchors beyond gothic fashion", joined)
        self.assertIn("do not leave all vampire cues as distant background props", joined)
        self.assertIn("first reading within a couple of seconds", joined)
        self.assertIn("do not rely on absence cues alone", joined)
        self.assertIn("reflection unease", joined)
        self.assertIn("no visible blood", joined)
        self.assertIn("no bared fangs", joined)
        self.assertIn("no visible victims", joined)
        self.assertIn("no gore", joined)

    def test_vampire_mixin_preserves_role_costume_without_assassin_note(self):
        payload = self.run_wrapper_json(
            "--concept",
            "카리나 메이드 흡혈귀",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--seed",
            "701",
            "--plain",
            "--no-negative",
        )

        concept = payload["concepts"][0]
        self.assertEqual(concept["name"], "카리나")
        self.assertEqual(concept["role"], "메이드")
        self.assertEqual(concept["applied_role"], "메이드")
        self.assertEqual(concept["applied_mixins"], ["흡혈귀"])
        self.assertEqual(concept["combined_forced_slots"]["costume_style"], ["frill_apron_maid_costume"])
        self.assertEqual(concept["combined_forced_slots"]["subject_framing"], ["upper_body_framing"])
        self.assertNotIn("gothic_doll_lace_dress", concept["combined_forced_slots"]["costume_style"])
        self.assertEqual(len(concept["selected_bundles"]), 1)
        self.assertEqual(concept["selected_bundles"][0]["mixin"], "흡혈귀")
        self.assertEqual(concept["selected_bundles"][0]["bundle_id"], "maid_reflection_service")
        joined = " ".join(payload["forward_args"])
        self.assertIn("keep the role outfit readable", joined)
        self.assertIn("open compact mirror faces the camera", joined)
        self.assertIn("lit face and hands must be visible", joined)
        self.assertIn("positive vampire anchor", joined)
        self.assertIn("no visible blood", joined)
        self.assertNotIn("assassin persona", joined)

    def test_vampire_concept_prompt_keeps_non_graphic_requirements(self):
        payload = self.run_wrapper_json(
            "--concept",
            "설윤 공주 흡혈귀",
            "--selection-mode",
            "rule",
            "--seed",
            "706",
            "--lang",
            "en",
            "--no-negative",
            "--include-choices",
        )

        item = payload[0]
        self.assertEqual(item["choices"]["appearance_type"]["id"], "classic_elegant")
        self.assertEqual(item["choices"]["costume_style"]["id"], "royal_princess_hanbok")
        self.assertEqual(item["choices"]["subject_framing"]["id"], "waist_up_framing")
        self.assertIn("Core concept lock: 설윤 공주 흡혈귀", item["prompt_en"])
        self.assertIn("predatory stillness", item["prompt_en"])
        self.assertIn("positive, visible non-graphic vampire identity anchors", item["prompt_en"])
        self.assertIn("role outfit readable", item["prompt_en"])
        self.assertIn("moonlit bat silhouettes", item["prompt_en"])
        self.assertIn("ruby eye catchlight", item["prompt_en"])
        self.assertIn("Eastern and Korean court-coded", item["prompt_en"])
        self.assertIn("do not convert the look into a Western black-lace gothic gown", item["prompt_en"])
        self.assertIn("no visible blood", item["prompt_en"])
        self.assertIn("no bared fangs", item["prompt_en"])
        self.assertIn("no visible victims", item["prompt_en"])
        self.assertIn("no gore", item["prompt_en"])
        self.assertNotIn("assassin persona", item["prompt_en"])

    def test_vampire_weak_role_prompts_include_positive_anchors(self):
        miner = self.run_wrapper_json(
            "--concept",
            "지젤 광부 흡혈귀",
            "--selection-mode",
            "rule",
            "--seed",
            "704",
            "--lang",
            "en",
            "--no-negative",
            "--include-choices",
        )[0]
        self.assertEqual(miner["choices"]["costume_style"]["id"], "miner_workwear_hard_hat")
        self.assertEqual(miner["choices"]["composition"]["id"], "puddle_inverted_reflection")
        self.assertEqual(miner["choices"]["subject_framing"]["id"], "upper_body_framing")
        self.assertIn("small antique cup of dark red wine or ruby cameo", miner["prompt_en"])
        self.assertIn("real subject's lit face or hand", miner["prompt_en"])
        self.assertIn("avoid generic mine horror", miner["prompt_en"])
        self.assertIn("bat-wing-shaped shadow", miner["prompt_en"])
        self.assertNotIn("analog_horror_dread", miner["prompt_en"])

        police = self.run_wrapper_json(
            "--concept",
            "닝닝 경찰 흡혈귀",
            "--selection-mode",
            "rule",
            "--seed",
            "703",
            "--lang",
            "en",
            "--no-negative",
            "--include-choices",
        )[0]
        self.assertEqual(police["choices"]["subject"]["id"], "adult_cosplay_performer")
        self.assertEqual(police["choices"]["costume_style"]["id"], "police_uniform_costume")
        self.assertEqual(police["choices"]["prop"]["id"], "clear_umbrella")
        self.assertEqual(police["choices"]["composition"]["id"], "reflection")
        self.assertEqual(police["choices"]["subject_framing"]["id"], "upper_body_framing")
        self.assertIn("clear umbrella, car glass, or reflective wall sits close to the subject", police["prompt_en"])
        self.assertIn("wrong reflection must sit in the foreground", police["prompt_en"])
        self.assertIn("bat-wing shadow must connect visually", police["prompt_en"])
        self.assertIn("no cute plush doll, mascot toy, or unrelated playful prop", police["prompt_en"])

        casual = self.run_wrapper_json(
            "--concept",
            "아일릿 원희 사복 여친 흡혈귀",
            "--selection-mode",
            "rule",
            "--seed",
            "705",
            "--lang",
            "en",
            "--no-negative",
            "--include-choices",
        )[0]
        self.assertEqual(casual["provenance"]["preset_id"], "compact_urban_fashion_portrait")
        self.assertEqual(casual["choices"]["subject"]["id"], "fashion_influencer")
        self.assertEqual(casual["choices"]["wardrobe_style"]["id"], "hoodie_shorts_sneakers")
        self.assertEqual(casual["choices"]["prop"]["id"], "clear_case_smartphone")
        self.assertEqual(casual["choices"]["action"]["id"], "mirror_selfie")
        self.assertEqual(casual["choices"]["composition"]["id"], "mirror_selfie_composition")
        self.assertEqual(casual["choices"]["subject_framing"]["id"], "waist_up_framing")
        self.assertIn("heavy black curtain or narrow overbright window edge", casual["prompt_en"])
        self.assertIn("mirror and phone screen should both visibly fail as normal reflections", casual["prompt_en"])
        self.assertIn("face, phone hand, and wrong reflection must be readable", casual["prompt_en"])
        self.assertIn("ruby choker or antique cameo", casual["prompt_en"])
        self.assertNotIn("work clothing, tools", casual["prompt_en"])

        bunny = self.run_wrapper_json(
            "--concept",
            "유나 바니걸 흡혈귀",
            "--selection-mode",
            "rule",
            "--seed",
            "707",
            "--lang",
            "en",
            "--no-negative",
            "--include-choices",
        )[0]
        self.assertEqual(bunny["choices"]["subject"]["id"], "adult_cosplay_performer")
        self.assertEqual(bunny["choices"]["costume_style"]["id"], "bunny_girl_costume")
        self.assertEqual(bunny["choices"]["prop"]["id"], "compact_mirror")
        self.assertEqual(bunny["choices"]["composition"]["id"], "reflection")
        self.assertEqual(bunny["choices"]["subject_framing"]["id"], "upper_body_framing")
        self.assertIn("bunny ears are pushed into deep shadow or silhouette", bunny["prompt_en"])
        self.assertIn("compact mirror or vanity reflection near the face or hand", bunny["prompt_en"])
        self.assertIn("face, hand, compact mirror, and failed reflection should be sharper", bunny["prompt_en"])
        self.assertIn("ordinary nightclub or dark bunny-girl costume portrait", bunny["prompt_en"])

    def test_vampire_role_batch_uses_distinct_facet_bundles(self):
        cases = [
            ("카리나 메이드 흡혈귀", 701),
            ("윈터 간호사 흡혈귀", 702),
            ("닝닝 경찰 흡혈귀", 703),
            ("지젤 광부 흡혈귀", 704),
            ("아일릿 원희 사복 여친 흡혈귀", 705),
            ("설윤 공주 흡혈귀", 706),
            ("유나 바니걸 흡혈귀", 707),
        ]
        selected_bundle_ids = set()
        selected_locations = set()
        selected_lighting = set()
        for concept, seed in cases:
            explanation = self.run_wrapper_json(
                "--concept",
                concept,
                "--explain-concept",
                "--selection-mode",
                "rule",
                "--seed",
                str(seed),
                "--plain",
                "--no-negative",
            )
            concept_payload = explanation["concepts"][0]
            self.assertEqual(concept_payload["applied_mixins"], ["흡혈귀"])
            selected_bundle = concept_payload["selected_bundles"][0]
            self.assertFalse(selected_bundle["bundle_id"].startswith("shared_"))
            selected_bundle_ids.add(selected_bundle["bundle_id"])
            selected_locations.add(concept_payload["combined_forced_slots"]["location"][0])
            selected_lighting.add(concept_payload["combined_forced_slots"]["lighting"][0])
            self.assertNotEqual(
                concept_payload["combined_forced_slots"].get("costume_style"),
                ["gothic_doll_lace_dress"],
            )
            if concept_payload["role"] == "사복 여친":
                self.assertEqual(selected_bundle["bundle_id"], "casual_daylight_refusal")
                self.assertEqual(selected_bundle["preset"], "compact_urban_fashion_portrait")
                self.assertEqual(concept_payload["combined_forced_slots"]["subject"], ["fashion_influencer"])
                self.assertEqual(concept_payload["combined_forced_slots"]["wardrobe_style"], ["hoodie_shorts_sneakers"])
                self.assertEqual(concept_payload["combined_forced_slots"]["subject_framing"], ["waist_up_framing"])
            if concept_payload["role"] == "간호사":
                self.assertEqual(concept_payload["combined_forced_slots"]["mood"], ["occult_noir"])
                self.assertEqual(concept_payload["combined_forced_slots"]["subject_framing"], ["upper_body_framing"])
            if concept_payload["role"] == "경찰":
                self.assertEqual(concept_payload["combined_forced_slots"]["subject_framing"], ["upper_body_framing"])
            if concept_payload["role"] == "광부":
                self.assertEqual(concept_payload["combined_forced_slots"]["subject_framing"], ["upper_body_framing"])
                self.assertIn(
                    "small antique cup of dark red wine or ruby cameo",
                    " ".join(explanation["forward_args"]),
                )
            if concept_payload["role"] == "공주":
                self.assertEqual(concept_payload["combined_forced_slots"]["costume_style"], ["royal_princess_hanbok"])
                self.assertEqual(concept_payload["combined_forced_slots"]["subject_framing"], ["waist_up_framing"])
            if concept_payload["role"] == "바니걸":
                self.assertEqual(concept_payload["combined_forced_slots"]["subject_framing"], ["upper_body_framing"])

        self.assertGreaterEqual(len(selected_bundle_ids), 5)
        self.assertGreaterEqual(len(selected_locations), 4)
        self.assertGreaterEqual(len(selected_lighting), 4)

    def test_vampire_role_specific_bundle_selection_ignores_shared_fallbacks(self):
        payload = self.run_wrapper_json(
            "--concept",
            "아일릿 원희 사복 여친 흡혈귀",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--seed",
            "705",
            "--plain",
            "--no-negative",
        )

        concept = payload["concepts"][0]
        selected_bundle = concept["selected_bundles"][0]
        self.assertEqual(selected_bundle["bundle_id"], "casual_daylight_refusal")
        self.assertEqual(selected_bundle["preset"], "compact_urban_fashion_portrait")
        self.assertNotIn("shared_daylight_threshold_refusal", [selected_bundle["bundle_id"]])

    def test_concept_recipe_expands_femme_fatale_as_non_objectifying_mixin(self):
        payload = self.run_wrapper_json(
            "--concept",
            "팜므파탈",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--seed",
            "811",
            "--plain",
            "--no-negative",
        )

        concept = payload["concepts"][0]
        self.assertEqual(concept["name"], "팜므파탈")
        self.assertIsNone(concept["role"])
        self.assertIsNone(concept["applied_role"])
        self.assertEqual(concept["applied_mixins"], ["팜므파탈"])
        self.assertTrue(concept["matched"])
        self.assertEqual(concept["mixins"]["팜므파탈"]["preset"], "compact_cinematic_prop_portrait")
        self.assertEqual(concept["combined_forced_slots"]["expression"], ["cold_unreadable_stare"])
        self.assertEqual(concept["combined_forced_slots"]["action"], ["looking_down_at_low_camera"])
        self.assertEqual(concept["combined_forced_slots"]["light_shape"], ["venetian_blind_shadows"])
        self.assertEqual(concept["combined_forced_slots"]["subject_framing"], ["upper_body_framing"])
        self.assertEqual(len(concept["selected_bundles"]), 1)
        bundle = concept["selected_bundles"][0]
        self.assertEqual(bundle["mixin"], "팜므파탈")
        self.assertTrue(bundle["bundle_id"].startswith("standalone_"))
        joined = " ".join(payload["forward_args"])
        self.assertIn("gaze reversal", joined)
        self.assertIn("information-control anchor", joined)
        self.assertIn("magnetic, deliberate allure", joined)
        self.assertIn("invitation itself is the trap", joined)
        self.assertIn("agency over availability", joined)
        self.assertIn("not a sexy villainess stereotype", joined)
        self.assertIn("never as an objectifying full-body or pin-up body angle", joined)
        self.assertNotIn("assassin persona", joined)

    def test_femme_fatale_mixin_preserves_role_costume_without_weapon_cue(self):
        payload = self.run_wrapper_json(
            "--concept",
            "카리나 메이드 팜므파탈",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--seed",
            "812",
            "--plain",
            "--no-negative",
        )

        concept = payload["concepts"][0]
        self.assertEqual(concept["name"], "카리나")
        self.assertEqual(concept["role"], "메이드")
        self.assertEqual(concept["applied_role"], "메이드")
        self.assertEqual(concept["applied_mixins"], ["팜므파탈"])
        self.assertEqual(concept["combined_forced_slots"]["costume_style"], ["frill_apron_maid_costume"])
        self.assertEqual(concept["combined_forced_slots"]["expression"], ["cold_unreadable_stare"])
        self.assertEqual(concept["combined_forced_slots"]["prop"], ["ornate_gothic_perfume_bottle"])
        self.assertEqual(concept["combined_forced_slots"]["subject_framing"], ["upper_body_framing"])
        self.assertEqual(len(concept["selected_bundles"]), 1)
        self.assertEqual(concept["selected_bundles"][0]["mixin"], "팜므파탈")
        joined = " ".join(payload["forward_args"])
        self.assertIn("keep the role outfit readable", joined)
        self.assertIn("the maid outfit stays readable", joined)
        self.assertIn("poison omen", joined)
        self.assertIn("guest book, key ring, or house ledger", joined)
        self.assertNotIn("sheathed utility blade", joined)
        self.assertNotIn("holster grip", joined)
        self.assertNotIn("assassin persona", joined)

    def test_femme_fatale_concept_prompt_contains_agency_and_noir_guards(self):
        payload = self.run_wrapper_json(
            "--concept",
            "설윤 공주 팜므파탈",
            "--selection-mode",
            "rule",
            "--seed",
            "816",
            "--lang",
            "en",
            "--no-negative",
            "--include-choices",
        )

        item = payload[0]
        self.assertEqual(item["choices"]["costume_style"]["id"], "royal_princess_hanbok")
        self.assertEqual(item["choices"]["expression"]["id"], "cold_unreadable_stare")
        self.assertEqual(item["choices"]["action"]["id"], "looking_down_at_low_camera")
        self.assertEqual(item["choices"]["prop"]["id"], "phoenix_hairpin_prop")
        self.assertEqual(item["choices"]["subject_framing"]["id"], "upper_body_framing")
        self.assertIn("Core concept lock: 설윤 공주 팜므파탈", item["prompt_en"])
        self.assertIn("gaze reversal", item["prompt_en"])
        self.assertIn("femme fatale reinterpreted as a powerful, intelligent, dangerous woman", item["prompt_en"])
        self.assertIn("noir and symbolist grammar", item["prompt_en"])
        self.assertIn("information-control anchor", item["prompt_en"])
        self.assertIn("magnetic, deliberate allure", item["prompt_en"])
        self.assertIn("no nudity, no explicit or fetish content", item["prompt_en"])
        self.assertIn("never as an objectifying full-body or pin-up body angle", item["prompt_en"])
        self.assertIn("political power and lethal intelligence", item["prompt_en"])
        self.assertNotIn("assassin persona", item["prompt_en"])

    def test_femme_fatale_role_batch_uses_role_specific_bundles(self):
        cases = [
            ("카리나 메이드 팜므파탈", 812),
            ("윈터 간호사 팜므파탈", 813),
            ("닝닝 경찰 팜므파탈", 814),
            ("지젤 광부 팜므파탈", 815),
            ("아일릿 원희 사복 여친 팜므파탈", 816),
            ("설윤 공주 팜므파탈", 817),
            ("유나 바니걸 팜므파탈", 818),
        ]
        expected_slots_by_role = {
            "간호사": {
                "prop": ["black_leather_gloves_prop"],
                "action": ["looking_down_at_low_camera"],
                "mood": ["occult_noir"],
                "composition": ["frame_within_frame"],
                "color": ["desaturated_cold_blue"],
                "subject_framing": ["upper_body_framing"],
            },
            "경찰": {
                "prop": ["single_playing_card_calling_card_prop"],
                "action": ["holding_story_prop"],
                "mood": ["reportage_tense_noir"],
                "composition": ["medium_close"],
                "subject_framing": ["head_and_shoulders_crop"],
            },
            "광부": {
                "prop": ["sealed_mission_envelope_prop"],
                "action": ["looking_down_at_low_camera"],
                "mood": ["occult_noir"],
                "composition": ["low_angle"],
                "subject_framing": ["waist_up_framing"],
            },
            "사복 여친": {
                "prop": ["clear_case_smartphone"],
                "action": ["holding_story_prop"],
                "location": ["taxi_backseat_seoul_night"],
                "light_type": ["phone_screen_face_glow"],
                "mood": ["reportage_tense_noir"],
                "composition": ["over_shoulder_phone_screen"],
                "subject_framing": ["upper_body_framing"],
            },
            "바니걸": {
                "prop": ["ornate_gothic_perfume_bottle"],
                "action": ["holding_ornate_bottle_to_chest"],
                "location": ["hotel_rooftop_dusk"],
                "lighting": ["rim_light"],
                "light_direction": ["rim_light"],
                "mood": ["luxury"],
                "composition": ["medium_close"],
                "color": ["tungsten_cinestill_blue_red"],
                "subject_framing": ["upper_body_framing"],
            },
        }
        selected_bundle_ids = set()
        selected_locations = set()
        for concept, seed in cases:
            explanation = self.run_wrapper_json(
                "--concept",
                concept,
                "--explain-concept",
                "--selection-mode",
                "rule",
                "--seed",
                str(seed),
                "--plain",
                "--no-negative",
            )
            concept_payload = explanation["concepts"][0]
            self.assertEqual(concept_payload["applied_mixins"], ["팜므파탈"])
            selected_bundle = concept_payload["selected_bundles"][0]
            selected_bundle_ids.add(selected_bundle["bundle_id"])
            selected_locations.add(concept_payload["combined_forced_slots"]["location"][0])
            self.assertEqual(concept_payload["combined_forced_slots"]["expression"], ["cold_unreadable_stare"])
            self.assertIn(
                concept_payload["combined_forced_slots"]["composition"][0],
                {"low_angle", "frame_within_frame", "silhouette", "centered_symmetry", "broken_glass_fragments_frame", "medium_close", "reflection", "over_shoulder_phone_screen"},
            )
            self.assertIn(
                concept_payload["combined_forced_slots"]["subject_framing"][0],
                {"upper_body_framing", "head_and_shoulders_crop", "waist_up_framing", "detail_crop_hands_accessories"},
            )
            self.assertFalse(
                concept_payload["combined_forced_slots"]["action"][0] == "looking_down_at_low_camera"
                and concept_payload["combined_forced_slots"]["composition"][0] == "low_angle"
                and concept_payload["role"] in {"경찰", "바니걸", "사복 여친"},
            )
            role = concept_payload["role"]
            for slot, ids in expected_slots_by_role.get(role, {}).items():
                self.assertEqual(concept_payload["combined_forced_slots"][slot], ids)
            if role in {"간호사", "바니걸"}:
                self.assertEqual(selected_bundle["preset"], "compact_cinematic_prop_portrait")
                preset_index = explanation["forward_args"].index("--preset")
                self.assertEqual(explanation["forward_args"][preset_index + 1], "compact_cinematic_prop_portrait")

        self.assertGreaterEqual(len(selected_bundle_ids), 6)
        self.assertGreaterEqual(len(selected_locations), 5)

    def test_femme_fatale_weak_roles_force_face_hands_and_information_anchors(self):
        cases = [
            (
                "닝닝 경찰 팜므파탈",
                814,
                {
                    "composition": "medium_close",
                    "subject_framing": "head_and_shoulders_crop",
                    "action": "holding_story_prop",
                    "phrases": ["case-file evidence", "viewer is the suspect", "full-body uniform pose"],
                },
            ),
            (
                "아일릿 원희 사복 여친 팜므파탈",
                816,
                {
                    "composition": "over_shoulder_phone_screen",
                    "subject_framing": "upper_body_framing",
                    "action": "holding_story_prop",
                    "prop": "clear_case_smartphone",
                    "phrases": ["dominant foreground anchor", "already knows the viewer's secret", "not an ordinary lifestyle selfie"],
                },
            ),
            (
                "유나 바니걸 팜므파탈",
                818,
                {
                    "composition": "medium_close",
                    "subject_framing": "upper_body_framing",
                    "action": "holding_ornate_bottle_to_chest",
                    "prop": "ornate_gothic_perfume_bottle",
                    "phrases": ["allure itself is the weapon", "drawn into a trap", "full-body side pose or pin-up body angle"],
                },
            ),
        ]

        for concept, seed, expected in cases:
            item = self.run_wrapper_json(
                "--concept",
                concept,
                "--selection-mode",
                "rule",
                "--seed",
                str(seed),
                "--lang",
                "en",
                "--no-negative",
                "--include-choices",
            )[0]
            self.assertEqual(item["choices"]["composition"]["id"], expected["composition"])
            self.assertEqual(item["choices"]["subject_framing"]["id"], expected["subject_framing"])
            self.assertEqual(item["choices"]["action"]["id"], expected["action"])
            if "prop" in expected:
                self.assertEqual(item["choices"]["prop"]["id"], expected["prop"])
            self.assertIn("information-control anchor", item["prompt_en"])
            self.assertIn("face, eyes, hands, and symbolic evidence", item["prompt_en"])
            for phrase in expected["phrases"]:
                self.assertIn(phrase, item["prompt_en"])

    def test_concept_recipe_expands_menhera_as_non_graphic_mixin(self):
        payload = self.run_wrapper_json(
            "--concept",
            "멘헤라",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--seed",
            "901",
            "--plain",
            "--no-negative",
        )

        concept = payload["concepts"][0]
        self.assertEqual(concept["name"], "멘헤라")
        self.assertIsNone(concept["role"])
        self.assertIsNone(concept["applied_role"])
        self.assertEqual(concept["applied_mixins"], ["멘헤라"])
        self.assertTrue(concept["matched"])
        self.assertEqual(concept["mixins"]["멘헤라"]["preset"], "candid_iphone_portrait")
        self.assertEqual(concept["combined_forced_slots"]["expression"], ["emotional_teary_eyes"])
        self.assertEqual(concept["combined_forced_slots"]["makeup_style"], ["igari_blush"])
        self.assertEqual(concept["combined_forced_slots"]["subject"], ["adult_alt_fashion_creator"])
        self.assertEqual(concept["combined_forced_slots"]["prop"], ["clear_case_smartphone"])
        self.assertEqual(concept["combined_forced_slots"]["light_type"], ["phone_screen_face_glow"])
        self.assertEqual(len(concept["selected_bundles"]), 1)
        bundle = concept["selected_bundles"][0]
        self.assertEqual(bundle["mixin"], "멘헤라")
        self.assertTrue(bundle["bundle_id"].startswith("standalone_"))
        joined = " ".join(payload["forward_args"])
        self.assertIn("yami-kawaii / jirai-kei internet-fashion mood", joined)
        self.assertIn("not a medical diagnosis", joined)
        self.assertIn("unread-message screen", joined)
        self.assertIn("no self-harm", joined)
        self.assertIn("no wounds, scars, cuts, blood", joined)
        self.assertNotIn("assassin persona", joined)

    def test_menhera_mixin_preserves_role_costume_without_assassin_note(self):
        payload = self.run_wrapper_json(
            "--concept",
            "카리나 메이드 멘헤라",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--seed",
            "902",
            "--plain",
            "--no-negative",
        )

        concept = payload["concepts"][0]
        self.assertEqual(concept["name"], "카리나")
        self.assertEqual(concept["role"], "메이드")
        self.assertEqual(concept["applied_role"], "메이드")
        self.assertEqual(concept["applied_mixins"], ["멘헤라"])
        self.assertEqual(concept["combined_forced_slots"]["costume_style"], ["frill_apron_maid_costume"])
        self.assertEqual(concept["combined_forced_slots"]["prop"], ["clear_case_smartphone"])
        self.assertEqual(concept["combined_forced_slots"]["action"], ["checking_phone"])
        self.assertEqual(concept["selected_bundles"][0]["bundle_id"], "maid_after_hours_overcare")
        joined = " ".join(payload["forward_args"])
        self.assertIn("keep the role outfit readable", joined)
        self.assertIn("after-hours over-giving and quiet exhaustion", joined)
        self.assertIn("never read as submissive sexual fantasy", joined)
        self.assertNotIn("sheathed utility blade", joined)
        self.assertNotIn("holster grip", joined)
        self.assertNotIn("assassin persona", joined)

    def test_menhera_sensitive_role_prompts_keep_safe_anchors(self):
        nurse = self.run_wrapper_json(
            "--concept",
            "윈터 간호사 멘헤라",
            "--selection-mode",
            "rule",
            "--seed",
            "903",
            "--lang",
            "en",
            "--no-negative",
            "--include-choices",
        )[0]
        self.assertEqual(nurse["choices"]["costume_style"]["id"], "nurse_uniform_costume")
        self.assertEqual(nurse["choices"]["location"]["id"], "hospital_waiting_room")
        self.assertEqual(nurse["choices"]["prop"]["id"], "flower_bouquet")
        self.assertEqual(nurse["choices"]["action"]["id"], "standing_silence")
        self.assertEqual(nurse["choices"]["expression"]["id"], "eyes_closed_serene")
        self.assertIn("care-fatigue and quiet waiting", nurse["prompt_en"])
        self.assertIn("wilted bouquet the single dominant anchor", nurse["prompt_en"])
        self.assertIn("not actively held or checked", nurse["prompt_en"])
        self.assertIn("no syringes, IV lines, medication, pills", nurse["prompt_en"])

        casual = self.run_wrapper_json(
            "--concept",
            "아일릿 원희 사복 여친 멘헤라",
            "--selection-mode",
            "rule",
            "--seed",
            "904",
            "--lang",
            "en",
            "--no-negative",
            "--include-choices",
        )[0]
        self.assertEqual(casual["provenance"]["preset_id"], "candid_iphone_portrait")
        self.assertEqual(casual["choices"]["subject"]["id"], "fashion_influencer")
        self.assertEqual(casual["choices"]["prop"]["id"], "clear_case_smartphone")
        self.assertEqual(casual["choices"]["action"]["id"], "checking_phone")
        self.assertEqual(casual["choices"]["location"]["id"], "dim_monitor_glow_bedroom")
        self.assertEqual(casual["choices"]["expression"]["id"], "shy_downward_glance")
        self.assertIn("unread-message waiting", casual["prompt_en"])
        self.assertIn("not merely a tired person on a phone", casual["prompt_en"])
        self.assertIn("read-but-unanswered chat", casual["prompt_en"])
        self.assertIn("adult original fictional person only", casual["prompt_en"])
        self.assertIn("never sexualized, never youthful-minor coded", casual["prompt_en"])

        bunny = self.run_wrapper_json(
            "--concept",
            "유나 바니걸 멘헤라",
            "--selection-mode",
            "rule",
            "--seed",
            "905",
            "--lang",
            "en",
            "--no-negative",
            "--include-choices",
        )[0]
        self.assertEqual(bunny["choices"]["costume_style"]["id"], "bunny_girl_costume")
        self.assertEqual(bunny["choices"]["prop"]["id"], "compact_mirror")
        self.assertEqual(bunny["choices"]["location"]["id"], "makeup_vanity")
        self.assertEqual(bunny["choices"]["subject_framing"]["id"], "upper_body_framing")
        self.assertEqual(bunny["choices"]["expression"]["id"], "neutral_camera_gaze")
        self.assertIn("fully covered adult stage costume", bunny["prompt_en"])
        self.assertIn("upper-body backstage exhaustion portrait", bunny["prompt_en"])
        self.assertIn("no pin-up pose", bunny["prompt_en"])
        self.assertIn("no cleavage-centered framing", bunny["prompt_en"])

    def test_menhera_role_batch_uses_role_specific_bundles(self):
        cases = [
            ("카리나 메이드 멘헤라", 902, "maid_after_hours_overcare"),
            ("윈터 간호사 멘헤라", 903, "nurse_waiting_room_burnout"),
            ("닝닝 경찰 멘헤라", 904, "police_off_duty_mirror_wait"),
            ("지젤 광부 멘헤라", 905, "miner_sunless_message_wait"),
            ("아일릿 원희 사복 여친 멘헤라", 906, "casual_unread_message_glow"),
            ("설윤 공주 멘헤라", 907, "princess_gilded_loneliness"),
            ("유나 바니걸 멘헤라", 908, "bunny_backstage_exhaustion"),
        ]
        selected_bundle_ids = set()
        selected_locations = set()
        selected_light_types = set()
        selected_expressions = set()
        allowed_menhera_expressions = {
            "emotional_teary_eyes",
            "neutral_camera_gaze",
            "eyes_closed_serene",
            "looking_away_pensive",
            "shy_downward_glance",
            "mysterious_half_smile",
        }

        for concept, seed, expected_bundle_id in cases:
            explanation = self.run_wrapper_json(
                "--concept",
                concept,
                "--explain-concept",
                "--selection-mode",
                "rule",
                "--seed",
                str(seed),
                "--plain",
                "--no-negative",
            )
            concept_payload = explanation["concepts"][0]
            self.assertEqual(concept_payload["applied_mixins"], ["멘헤라"])
            selected_bundle = concept_payload["selected_bundles"][0]
            self.assertEqual(selected_bundle["bundle_id"], expected_bundle_id)
            self.assertFalse(selected_bundle["bundle_id"].startswith("shared_"))
            expression = concept_payload["combined_forced_slots"]["expression"][0]
            self.assertIn(expression, allowed_menhera_expressions)
            selected_expressions.add(expression)
            self.assertTrue(
                {"costume_style", "wardrobe_style"} & set(concept_payload["combined_forced_slots"]),
                concept_payload["combined_forced_slots"],
            )
            selected_bundle_ids.add(selected_bundle["bundle_id"])
            selected_locations.add(concept_payload["combined_forced_slots"]["location"][0])
            selected_light_types.add(concept_payload["combined_forced_slots"]["light_type"][0])
            joined = " ".join(explanation["forward_args"])
            self.assertIn("not a medical diagnosis", joined)
            self.assertIn("no self-harm", joined)
            self.assertNotIn("assassin persona", joined)
            self.assertNotIn("sheathed utility blade", joined)
            self.assertNotIn("holster grip", joined)

        self.assertEqual(len(selected_bundle_ids), len(cases))
        self.assertGreaterEqual(len(selected_expressions), 4)
        self.assertGreaterEqual(len(selected_locations), 6)
        self.assertGreaterEqual(len(selected_light_types), 4)

    def test_menhera_weak_role_prompts_include_explicit_anxiety_anchors(self):
        police = self.run_wrapper_json(
            "--concept",
            "닝닝 경찰 멘헤라",
            "--selection-mode",
            "rule",
            "--seed",
            "904",
            "--lang",
            "en",
            "--no-negative",
            "--include-choices",
        )[0]
        self.assertEqual(police["choices"]["costume_style"]["id"], "police_uniform_costume")
        self.assertEqual(police["choices"]["composition"]["id"], "mirror_selfie_composition")
        self.assertEqual(police["choices"]["expression"]["id"], "looking_away_pensive")
        self.assertIn("must NOT read as a pretty police cosplay shoot", police["prompt_en"])
        self.assertIn("gaze avoids her own reflection", police["prompt_en"])
        self.assertIn("empty or one-sided chat", police["prompt_en"])
        self.assertIn("undone or askew", police["prompt_en"])

        miner = self.run_wrapper_json(
            "--concept",
            "지젤 광부 멘헤라",
            "--selection-mode",
            "rule",
            "--seed",
            "905",
            "--lang",
            "en",
            "--no-negative",
            "--include-choices",
        )[0]
        self.assertEqual(miner["choices"]["costume_style"]["id"], "miner_workwear_hard_hat")
        self.assertEqual(miner["choices"]["location"]["id"], "underground_mine_tunnel_set")
        self.assertEqual(miner["choices"]["expression"]["id"], "looking_away_pensive")
        self.assertIn("discordant kawaii contrast", miner["prompt_en"])
        self.assertIn("pastel sticker-covered phone case", miner["prompt_en"])
        self.assertIn("pink ribbon tied to the helmet strap", miner["prompt_en"])

        casual = self.run_wrapper_json(
            "--concept",
            "아일릿 원희 사복 여친 멘헤라",
            "--selection-mode",
            "rule",
            "--seed",
            "906",
            "--lang",
            "en",
            "--no-negative",
            "--include-choices",
        )[0]
        self.assertEqual(casual["choices"]["expression"]["id"], "shy_downward_glance")
        self.assertEqual(casual["choices"]["prop"]["id"], "clear_case_smartphone")
        self.assertIn("plush doll on the pillow", casual["prompt_en"])
        self.assertIn("wilted bouquet on the nightstand", casual["prompt_en"])
        self.assertIn("read-but-unanswered chat", casual["prompt_en"])
        self.assertIn("contained and defensive", casual["prompt_en"])

        princess = self.run_wrapper_json(
            "--concept",
            "설윤 공주 멘헤라",
            "--selection-mode",
            "rule",
            "--seed",
            "907",
            "--lang",
            "en",
            "--no-negative",
            "--include-choices",
        )[0]
        self.assertEqual(princess["choices"]["costume_style"]["id"], "royal_princess_hanbok")
        self.assertEqual(princess["choices"]["light_type"]["id"], "phone_screen_face_glow")
        self.assertEqual(princess["choices"]["expression"]["id"], "eyes_closed_serene")
        self.assertIn("do NOT place a modern phone in the main silhouette", princess["prompt_en"])
        self.assertIn("faint cold rectangular glow", princess["prompt_en"])
        self.assertIn("dominant physical anchor", princess["prompt_en"])

    def test_menhera_nurse_uses_single_dominant_anchor_without_active_phone_check(self):
        nurse = self.run_wrapper_json(
            "--concept",
            "윈터 간호사 멘헤라",
            "--selection-mode",
            "rule",
            "--seed",
            "903",
            "--lang",
            "en",
            "--no-negative",
            "--include-choices",
        )[0]

        self.assertEqual(nurse["choices"]["prop"]["id"], "flower_bouquet")
        self.assertEqual(nurse["choices"]["action"]["id"], "standing_silence")
        self.assertNotEqual(nurse["choices"]["action"]["id"], "checking_phone")
        self.assertIn("single dominant anchor", nurse["prompt_en"])
        self.assertIn("dark phone lies face-down", nurse["prompt_en"])

    def test_concept_recipe_expands_yandere_as_non_graphic_mixin(self):
        payload = self.run_wrapper_json(
            "--concept",
            "얀데레",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--seed",
            "901",
            "--plain",
            "--no-negative",
        )

        concept = payload["concepts"][0]
        self.assertEqual(concept["name"], "얀데레")
        self.assertIsNone(concept["role"])
        self.assertIsNone(concept["applied_role"])
        self.assertEqual(concept["applied_mixins"], ["얀데레"])
        self.assertTrue(concept["matched"])
        self.assertEqual(concept["mixins"]["얀데레"]["preset"], "compact_cinematic_prop_portrait")
        self.assertEqual(concept["combined_forced_slots"]["expression"], ["soft_smile"])
        self.assertEqual(concept["combined_forced_slots"]["light_intensity"], ["deep_shadow_detail"])
        self.assertIn(
            concept["combined_forced_slots"]["subject_framing"][0],
            {"close_up_face_crop", "head_and_shoulders_crop", "upper_body_framing"},
        )
        self.assertEqual(len(concept["selected_bundles"]), 1)
        bundle = concept["selected_bundles"][0]
        self.assertEqual(bundle["mixin"], "얀데레")
        self.assertTrue(bundle["bundle_id"].startswith("standalone_"))
        joined = " ".join(payload["forward_args"])
        self.assertIn("soft, genuinely loving smile combined with hollow, fixed, unblinking eyes", joined)
        self.assertIn("repeated photos", joined)
        self.assertIn("red thread", joined)
        self.assertIn("glass dome", joined)
        self.assertIn("empty birdcage", joined)
        self.assertIn("no weapon", joined)
        self.assertIn("no visible captive or victim", joined)
        self.assertIn("no minors and no sexual content", joined)

    def test_yandere_mixin_preserves_role_costume_without_weapon_cue(self):
        payload = self.run_wrapper_json(
            "--concept",
            "카리나 메이드 얀데레",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--seed",
            "902",
            "--plain",
            "--no-negative",
        )

        concept = payload["concepts"][0]
        self.assertEqual(concept["name"], "카리나")
        self.assertEqual(concept["role"], "메이드")
        self.assertEqual(concept["applied_role"], "메이드")
        self.assertEqual(concept["applied_mixins"], ["얀데레"])
        self.assertEqual(concept["combined_forced_slots"]["costume_style"], ["frill_apron_maid_costume"])
        self.assertNotIn("gothic_doll_lace_dress", concept["combined_forced_slots"]["costume_style"])
        self.assertEqual(concept["combined_forced_slots"]["expression"], ["soft_smile"])
        self.assertEqual(concept["combined_forced_slots"]["prop"], ["instant_photo_stack"])
        self.assertEqual(concept["combined_forced_slots"]["subject_framing"], ["head_and_shoulders_crop"])
        self.assertEqual(len(concept["selected_bundles"]), 1)
        self.assertEqual(concept["selected_bundles"][0]["bundle_id"], "maid_devotion_possession")
        joined = " ".join(payload["forward_args"])
        self.assertIn("the maid outfit stays clearly readable", joined)
        self.assertIn("white-knuckled grip", joined)
        self.assertIn("red thread runs from her finger", joined)
        self.assertIn("no visible blood", joined)
        self.assertIn("no weapon", joined)
        self.assertNotIn("sheathed utility blade", joined)
        self.assertNotIn("holster grip", joined)
        self.assertNotIn("assassin persona", joined)

    def test_yandere_concept_prompt_contains_paradox_and_safety_guards(self):
        payload = self.run_wrapper_json(
            "--concept",
            "설윤 공주 얀데레",
            "--selection-mode",
            "rule",
            "--seed",
            "906",
            "--lang",
            "en",
            "--no-negative",
            "--include-choices",
        )

        item = payload[0]
        self.assertEqual(item["choices"]["costume_style"]["id"], "royal_princess_hanbok")
        self.assertEqual(item["choices"]["expression"]["id"], "soft_smile")
        self.assertEqual(item["choices"]["prop"]["id"], "flower_bouquet")
        self.assertEqual(item["choices"]["composition"]["id"], "centered_symmetry")
        self.assertEqual(item["choices"]["subject_framing"]["id"], "upper_body_framing")
        self.assertIn("Core concept lock: 설윤 공주 얀데레", item["prompt_en"])
        self.assertIn("soft, genuinely loving smile combined with hollow, fixed, unblinking eyes", item["prompt_en"])
        self.assertIn("empty gilded birdcage or glass dome", item["prompt_en"])
        self.assertIn("no weapon", item["prompt_en"])
        self.assertIn("no blood", item["prompt_en"])
        self.assertIn("no victim", item["prompt_en"])
        self.assertIn("no explicit or fetish content", item["prompt_en"])

    def test_yandere_role_batch_uses_role_specific_bundles(self):
        cases = [
            ("카리나 메이드 얀데레", 902),
            ("윈터 간호사 얀데레", 903),
            ("닝닝 경찰 얀데레", 904),
            ("지젤 광부 얀데레", 905),
            ("아일릿 원희 사복 여친 얀데레", 906),
            ("설윤 공주 얀데레", 907),
            ("유나 바니걸 얀데레", 908),
        ]
        expected_slots_by_role = {
            "메이드": {
                "prop": ["instant_photo_stack"],
                "action": ["doorframe_shadow_watch"],
                "composition": ["frame_within_frame"],
                "subject_framing": ["head_and_shoulders_crop"],
            },
            "간호사": {
                "prop": ["instant_photo_stack"],
                "location": ["hospital_corridor"],
                "mood": ["quiet_dread"],
                "subject_framing": ["head_and_shoulders_crop"],
            },
            "경찰": {
                "prop": ["instant_photo_stack"],
                "composition": ["medium_close"],
                "subject_framing": ["head_and_shoulders_crop"],
            },
            "광부": {
                "prop": ["instant_photo_stack"],
                "location": ["underground_mine_tunnel_set"],
                "lighting": ["single_flashlight_beam"],
                "subject_framing": ["waist_up_framing"],
            },
            "사복 여친": {
                "prop": ["instant_photo_stack"],
                "action": ["mirror_selfie"],
                "composition": ["extreme_close"],
                "subject_framing": ["close_up_face_crop"],
            },
            "공주": {
                "prop": ["flower_bouquet"],
                "location": ["royal_princess_chamber"],
                "composition": ["centered_symmetry"],
                "subject_framing": ["upper_body_framing"],
            },
            "바니걸": {
                "prop": ["compact_mirror"],
                "location": ["makeup_vanity"],
                "composition": ["reflection"],
                "subject_framing": ["upper_body_framing"],
            },
        }
        selected_bundle_ids = set()
        selected_locations = set()
        for concept, seed in cases:
            explanation = self.run_wrapper_json(
                "--concept",
                concept,
                "--explain-concept",
                "--selection-mode",
                "rule",
                "--seed",
                str(seed),
                "--plain",
                "--no-negative",
            )
            concept_payload = explanation["concepts"][0]
            self.assertEqual(concept_payload["applied_mixins"], ["얀데레"])
            selected_bundle = concept_payload["selected_bundles"][0]
            self.assertEqual(selected_bundle["mixin"], "얀데레")
            self.assertFalse(selected_bundle["bundle_id"].startswith("shared_"))
            self.assertFalse(selected_bundle["bundle_id"].startswith("standalone_"))
            selected_bundle_ids.add(selected_bundle["bundle_id"])
            selected_locations.add(concept_payload["combined_forced_slots"]["location"][0])
            self.assertEqual(concept_payload["combined_forced_slots"]["expression"], ["soft_smile"])
            role = concept_payload["role"]
            for slot, ids in expected_slots_by_role[role].items():
                self.assertEqual(concept_payload["combined_forced_slots"][slot], ids)

        self.assertGreaterEqual(len(selected_bundle_ids), 7)
        self.assertGreaterEqual(len(selected_locations), 5)

    def test_yandere_weak_roles_force_possession_anchors_and_safe_framing(self):
        cases = [
            (
                "닝닝 경찰 얀데레",
                904,
                {
                    "prop": "instant_photo_stack",
                    "composition": "medium_close",
                    "subject_framing": "head_and_shoulders_crop",
                    "phrases": ["overprotective watchfulness", "repeated surveillance-like photos", "never a full-body pin-up pose"],
                },
            ),
            (
                "지젤 광부 얀데레",
                905,
                {
                    "prop": "instant_photo_stack",
                    "composition": "centered_symmetry",
                    "subject_framing": "waist_up_framing",
                    "phrases": ["sealed sanctuary", "private shrine", "never a threat"],
                },
            ),
            (
                "아일릿 원희 사복 여친 얀데레",
                906,
                {
                    "prop": "instant_photo_stack",
                    "composition": "extreme_close",
                    "subject_framing": "close_up_face_crop",
                    "phrases": [
                        "not a real-person stalking scene",
                        "no identifiable target",
                        "no minors",
                        "as if no personal space is allowed",
                    ],
                },
            ),
            (
                "유나 바니걸 얀데레",
                908,
                {
                    "prop": "compact_mirror",
                    "composition": "reflection",
                    "subject_framing": "upper_body_framing",
                    "phrases": ["never becomes a pin-up", "you are my only audience", "no sexualized framing"],
                },
            ),
        ]

        for concept, seed, expected in cases:
            item = self.run_wrapper_json(
                "--concept",
                concept,
                "--selection-mode",
                "rule",
                "--seed",
                str(seed),
                "--lang",
                "en",
                "--no-negative",
                "--include-choices",
            )[0]
            self.assertEqual(item["choices"]["prop"]["id"], expected["prop"])
            self.assertEqual(item["choices"]["composition"]["id"], expected["composition"])
            self.assertEqual(item["choices"]["subject_framing"]["id"], expected["subject_framing"])
            self.assertIn("soft, genuinely loving smile combined with hollow, fixed, unblinking eyes", item["prompt_en"])
            self.assertIn("no weapon", item["prompt_en"])
            self.assertIn("no visible captive or victim", item["prompt_en"])
            for phrase in expected["phrases"]:
                self.assertIn(phrase, item["prompt_en"])

    def test_concept_recipe_explain_combines_role_and_assassin_mixin(self):
        payload = self.run_wrapper_json(
            "--concept",
            "닝닝 경찰 암살자",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--seed",
            "1",
            "--plain",
            "--no-negative",
        )

        concept = payload["concepts"][0]
        self.assertEqual(concept["name"], "닝닝")
        self.assertEqual(concept["applied_role"], "경찰")
        self.assertEqual(concept["applied_mixins"], ["암살자"])
        self.assertEqual(len(concept["selected_bundles"]), 1)
        bundle = concept["selected_bundles"][0]
        self.assertEqual(bundle["mixin"], "암살자")
        self.assertTrue(bundle["bundle_id"])
        self.assertIn("weight", bundle)
        self.assertEqual(concept["combined_forced_slots"]["costume_style"], ["police_uniform_costume"])
        for slot in ("prop", "action", "location", "lighting", "mood", "composition"):
            self.assertEqual(concept["combined_forced_slots"][slot], [bundle["set"][slot]])
        self.assertEqual(concept["combined_forced_slots"]["expression"], ["cold_unreadable_stare"])
        self.assertEqual(concept["combined_forced_slots"]["light_type"], ["narrow_spotlight"])
        self.assertEqual(concept["combined_forced_slots"]["light_intensity"], ["deep_shadow_detail"])
        self.assertEqual(concept["combined_forced_slots"]["color"], ["desaturated_cold_blue"])
        self.assertIn("costume_style=police_uniform_costume", payload["forward_args"])
        for slot in ("prop", "action", "location", "lighting", "mood", "composition"):
            self.assertIn(f"{slot}={bundle['set'][slot]}", payload["forward_args"])
        self.assertIn("expression=cold_unreadable_stare", payload["forward_args"])
        self.assertIn("role outfit is a cover identity/disguise for the assassin persona", payload["forward_args"])
        self.assertIn("the figure is hiding in plain sight: an ordinary cover identity concealing a different purpose", payload["forward_args"])
        self.assertIn("non-graphic staged character photo with no depicted injury, blood, victim, or violence", payload["forward_args"])

        repeated = self.run_wrapper_json(
            "--concept",
            "닝닝 경찰 암살자",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--seed",
            "1",
            "--plain",
            "--no-negative",
        )
        changed_seed = self.run_wrapper_json(
            "--concept",
            "닝닝 경찰 암살자",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--seed",
            "3",
            "--plain",
            "--no-negative",
        )
        self.assertEqual(bundle["bundle_id"], repeated["concepts"][0]["selected_bundles"][0]["bundle_id"])
        self.assertNotEqual(bundle["bundle_id"], changed_seed["concepts"][0]["selected_bundles"][0]["bundle_id"])

    def test_assassin_concept_batch_uses_cohesive_bundles(self):
        cases = [
            ("카리나 메이드 암살자", 1),
            ("윈터 간호사 암살자", 1),
            ("닝닝 경찰 암살자", 1),
            ("지젤 광부 암살자", 1),
            ("아일릿 원희 사복 여친 암살자", 1),
            ("설윤 공주 암살자", 2),
            ("유나 바니걸 암살자", 8),
        ]
        banned_actions = {
            "turning_back",
            "over_shoulder_pose",
            "slow_walk_turnaround",
            "window_silhouette_stand",
            "weapon_low_ready_stance",
            "blade_guarded_ready_pose",
            "staged_archery_draw_pose",
            "holding_real_weapon_reference_pose",
            "rpg_weapon_ready_pose",
        }
        expected_common_slots = {
            "expression": "cold_unreadable_stare",
            "light_type": "narrow_spotlight",
            "light_intensity": "deep_shadow_detail",
            "color": "desaturated_cold_blue",
        }
        selected_bundle_ids = set()
        for concept, seed in cases:
            explanation = self.run_wrapper_json(
                "--concept",
                concept,
                "--explain-concept",
                "--selection-mode",
                "rule",
                "--seed",
                str(seed),
                "--plain",
                "--no-negative",
            )
            concept_payload = explanation["concepts"][0]
            selected_bundle = concept_payload["selected_bundles"][0]
            selected_bundle_ids.add(selected_bundle["bundle_id"])

            generated = self.run_wrapper_json(
                "--concept",
                concept,
                "--selection-mode",
                "rule",
                "--seed",
                str(seed),
                "--lang",
                "en",
                "--no-negative",
                "--include-choices",
            )
            item = generated[0]
            for slot, expected_id in selected_bundle["set"].items():
                self.assertEqual(item["choices"][slot]["id"], expected_id)
            for slot, expected_id in expected_common_slots.items():
                self.assertEqual(item["choices"][slot]["id"], expected_id)
            self.assertNotIn(item["choices"]["action"]["id"], banned_actions)

            if "costume_style" in concept_payload["combined_forced_slots"]:
                expected_costume = concept_payload["combined_forced_slots"]["costume_style"][0]
                self.assertEqual(item["choices"]["costume_style"]["id"], expected_costume)

            self.assertIn("hiding in plain sight", item["prompt_en"])
            self.assertIn("stillness and tight emotional control just before a mission", item["prompt_en"])
            self.assertIn("never drawn, aimed, used, bloody, or shown with a victim", item["prompt_en"])
            self.assertIn("the gaze, hands, or body angle should point toward a task", item["prompt_en"])
            self.assertIn("implied target", item["prompt_en"])
            self.assertIn("concealed prop", item["prompt_en"])
            self.assertIn("non-graphic staged character photo with no depicted injury, blood, victim, or violence", item["prompt_en"])

        self.assertGreaterEqual(len(selected_bundle_ids), 3)

    def test_assassin_default_weapon_cue_per_role_preserves_bundle_slots(self):
        cases = [
            (
                "카리나 메이드 암살자",
                1,
                "a slim sheathed utility blade sits partially visible beneath the apron tie",
            ),
            (
                "윈터 간호사 암살자",
                1,
                "a slim sheathed utility blade rides partially visible at the hip under the uniform or jacket",
            ),
            (
                "닝닝 경찰 암살자",
                1,
                "a duty holster grip is partially visible at the belt as a quiet cover-identity tell",
            ),
            (
                "지젤 광부 암살자",
                1,
                "a nonfunctional pickaxe tool head is subtly visible in-context as work equipment held low or shouldered",
            ),
            (
                "아일릿 원희 사복 여친 암살자",
                1,
                "a compact sheathed blade peeks at the waistband or hoodie edge",
            ),
            (
                "설윤 공주 암살자",
                2,
                "a phoenix hairpin catches a subtle metallic glint as the only weapon cue, with no firearm or modern weapon",
            ),
            (
                "유나 바니걸 암살자",
                8,
                "a slim sheathed blade is just visible along the garment seam or edge",
            ),
        ]

        for concept, seed, expected_cue in cases:
            with self.subTest(concept=concept):
                explanation = self.run_wrapper_json(
                    "--concept",
                    concept,
                    "--explain-concept",
                    "--selection-mode",
                    "rule",
                    "--seed",
                    str(seed),
                    "--plain",
                    "--no-negative",
                )
                selected_bundle = explanation["concepts"][0]["selected_bundles"][0]
                generated = self.run_wrapper_json(
                    "--concept",
                    concept,
                    "--selection-mode",
                    "rule",
                    "--seed",
                    str(seed),
                    "--lang",
                    "en",
                    "--no-negative",
                    "--include-choices",
                )
                item = generated[0]

                self.assertIn(expected_cue, item["prompt_en"])
                self.assertIn("never drawn, aimed, used, bloody, or shown with a victim", item["prompt_en"])
                for slot in ("prop", "action"):
                    self.assertEqual(item["choices"][slot]["id"], selected_bundle["set"][slot])

    def test_assassin_default_weapon_cue_is_text_not_pose_override(self):
        cases = [
            ("카리나 메이드 암살자", 1),
            ("윈터 간호사 암살자", 1),
            ("지젤 광부 암살자", 1),
            ("설윤 공주 암살자", 2),
            ("유나 바니걸 암살자", 8),
        ]
        forbidden_default_actions = {
            "concealed_holster_adjust_pose",
            "weapon_low_ready_stance",
        }

        for concept, seed in cases:
            with self.subTest(concept=concept):
                generated = self.run_wrapper_json(
                    "--concept",
                    concept,
                    "--selection-mode",
                    "rule",
                    "--seed",
                    str(seed),
                    "--lang",
                    "en",
                    "--no-negative",
                    "--include-choices",
                )
                self.assertNotIn(generated[0]["choices"]["action"]["id"], forbidden_default_actions)

    def test_concept_explicit_set_overrides_recipe_slots(self):
        visible_weapon_requirement = (
            "a slim sheathed utility blade sits partially visible beneath the apron tie; "
            "never drawn, aimed, used, bloody, or shown with a victim"
        )
        payload = self.run_wrapper_json(
            "--concept",
            "카리나 메이드 암살자",
            "--selection-mode",
            "rule",
            "--seed",
            "3100",
            "--lang",
            "en",
            "--no-negative",
            "--include-choices",
            "--set",
            "prop=sheathed_utility_knife_prop",
            "--set",
            "action=concealed_holster_adjust_pose",
            "--additional-requirement",
            visible_weapon_requirement,
        )

        item = payload[0]
        self.assertEqual(item["choices"]["prop"]["id"], "sheathed_utility_knife_prop")
        self.assertEqual(item["choices"]["action"]["id"], "concealed_holster_adjust_pose")
        self.assertIn(visible_weapon_requirement, item["prompt_en"])
        set_values = [
            value
            for index, value in enumerate(item["provenance"]["argv"][1:], start=1)
            if item["provenance"]["argv"][index - 1] == "--set"
        ]
        self.assertEqual(
            set_values[-2:],
            ["prop=sheathed_utility_knife_prop", "action=concealed_holster_adjust_pose"],
        )

    def test_explicit_weapon_set_suppresses_default_role_weapon_cue(self):
        payload = self.run_wrapper_json(
            "--concept",
            "카리나 메이드 암살자",
            "--selection-mode",
            "rule",
            "--seed",
            "3100",
            "--lang",
            "en",
            "--no-negative",
            "--include-choices",
            "--set",
            "prop=sheathed_utility_knife_prop",
            "--set",
            "action=concealed_holster_adjust_pose",
        )

        item = payload[0]
        self.assertEqual(item["choices"]["prop"]["id"], "sheathed_utility_knife_prop")
        self.assertEqual(item["choices"]["action"]["id"], "concealed_holster_adjust_pose")
        self.assertNotIn("beneath the apron tie", item["prompt_en"])

    def test_assassin_visible_weapon_request_role_map_uses_39df660_tags(self):
        cases = [
            (
                "카리나 메이드 암살자",
                "sheathed_utility_knife_prop",
                "concealed_holster_adjust_pose",
                "a slim sheathed utility blade sits partially visible beneath the apron tie; never drawn, aimed, used, bloody, or shown with a victim",
            ),
            (
                "윈터 간호사 암살자",
                "sheathed_utility_knife_prop",
                "concealed_holster_adjust_pose",
                "a slim sheathed utility blade rides partially visible at the hip under the uniform or jacket; never drawn, aimed, used, bloody, or shown with a victim",
            ),
            (
                "닝닝 경찰 암살자",
                "real_holstered_service_pistol",
                "concealed_holster_adjust_pose",
                "a duty holster grip is partially visible at the belt as a quiet cover-identity tell; never drawn, aimed, used, bloody, or shown with a victim",
            ),
            (
                "지젤 광부 암살자",
                "nonfunctional_pickaxe_prop",
                "weapon_low_ready_stance",
                "a nonfunctional pickaxe tool head is subtly visible in-context as work equipment held low or shouldered; never drawn, aimed, used, bloody, or shown with a victim",
            ),
            (
                "아일릿 원희 사복 여친 암살자",
                "sheathed_utility_knife_prop",
                "concealed_holster_adjust_pose",
                "a compact sheathed blade peeks at the waistband or hoodie edge; never drawn, aimed, used, bloody, or shown with a victim",
            ),
            (
                "설윤 공주 암살자",
                "phoenix_hairpin_prop",
                "standing_silence",
                "a phoenix hairpin catches a subtle metallic glint as the only weapon cue, with no firearm or modern weapon; never drawn, aimed, used, bloody, or shown with a victim",
            ),
            (
                "유나 바니걸 암살자",
                "sheathed_utility_knife_prop",
                "concealed_holster_adjust_pose",
                "a slim sheathed blade is just visible along the garment seam or edge; never drawn, aimed, used, bloody, or shown with a victim",
            ),
        ]

        for concept, expected_prop, expected_action, visible_weapon_requirement in cases:
            with self.subTest(concept=concept):
                payload = self.run_wrapper_json(
                    "--concept",
                    concept,
                    "--selection-mode",
                    "rule",
                    "--seed",
                    "3100",
                    "--lang",
                    "en",
                    "--no-negative",
                    "--include-choices",
                    "--set",
                    f"prop={expected_prop}",
                    "--set",
                    f"action={expected_action}",
                    "--additional-requirement",
                    visible_weapon_requirement,
                )
                item = payload[0]
                self.assertEqual(item["choices"]["prop"]["id"], expected_prop)
                self.assertEqual(item["choices"]["action"]["id"], expected_action)
                self.assertIn(visible_weapon_requirement, item["prompt_en"])

    def test_concept_recipe_generation_records_expanded_argv_in_provenance(self):
        result = subprocess.run(
            [
                sys.executable,
                str(WRAPPER_PATH),
                "--concept",
                "지젤 광부",
                "--selection-mode",
                "rule",
                "--seed",
                "9",
                "--lang",
                "en",
                "--no-negative",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        item = payload[0]
        self.assertIn("Core concept lock: 지젤 광부", item["prompt_en"])
        self.assertIn("Additional requirements: coal miner workwear", item["prompt_en"])
        self.assertIn("miner workwear with a safety helmet and headlamp", item["prompt_en"])
        self.assertIn("underground mine tunnel set", item["prompt_en"])
        self.assertIn("not an exact likeness", item["prompt_en"])
        self.assertIn("지젤 광부", item["provenance"]["concept_lock"])
        self.assertTrue(
            any("coal miner workwear" in requirement for requirement in item["provenance"]["additional_requirements"])
        )
        self.assertIn("costume_style=miner_workwear_hard_hat", item["provenance"]["argv"])
        self.assertIn("location=underground_mine_tunnel_set", item["provenance"]["argv"])
        self.assertIn("--concept-lock", item["provenance"]["argv"])
        self.assertIn("--additional-requirement", item["provenance"]["argv"])

    def test_record_image_run_ledger_preserves_prompt_hash_across_retries(self):
        prompt = "Exact prompt text for unchanged retry"
        prompt_id = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]
        with tempfile.TemporaryDirectory() as tmpdir:
            ledger = Path(tmpdir) / "runs.ndjson"
            first = subprocess.run(
                [
                    sys.executable,
                    str(RECORD_RUN_PATH),
                    "--ts",
                    "2026-06-03T10:00:00+09:00",
                    "--concept",
                    "유나 바니걸",
                    "--prompt-en",
                    prompt,
                    "--prompt-id",
                    prompt_id,
                    "--attempt",
                    "1",
                    "--status",
                    "safety_block",
                    "--failure-reason",
                    "safety filter",
                    "--tool",
                    "image_gen",
                    "--ledger",
                    str(ledger),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(first.returncode, 0, first.stderr)
            first_payload = json.loads(first.stdout)

            second = subprocess.run(
                [
                    sys.executable,
                    str(RECORD_RUN_PATH),
                    "--ts",
                    "2026-06-03T10:01:00+09:00",
                    "--concept",
                    "유나 바니걸",
                    "--prompt-en",
                    prompt,
                    "--prompt-id",
                    prompt_id,
                    "--attempt",
                    "2",
                    "--retry-of",
                    first_payload["run_id"],
                    "--status",
                    "success",
                    "--image-path",
                    "/tmp/generated.png",
                    "--tool",
                    "image_gen",
                    "--ledger",
                    str(ledger),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(second.returncode, 0, second.stderr)

            rows = [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["prompt_id"], prompt_id)
            self.assertEqual(rows[1]["prompt_id"], prompt_id)
            self.assertEqual(rows[1]["retry_of"], rows[0]["run_id"])
            self.assertEqual(rows[1]["image_paths"], ["/tmp/generated.png"])

    def test_record_image_run_default_ledger_is_worktree_local_runs_file(self):
        spec = importlib.util.spec_from_file_location("record_image_run", RECORD_RUN_PATH)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        self.assertEqual(module.PROJECT_ROOT, ROOT)
        self.assertEqual(module.DEFAULT_LEDGER, ROOT / "runs" / "image_runs.ndjson")

    def test_record_image_run_rejects_changed_prompt_text(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            ledger = Path(tmpdir) / "runs.ndjson"
            result = subprocess.run(
                [
                    sys.executable,
                    str(RECORD_RUN_PATH),
                    "--ts",
                    "2026-06-03T10:00:00+09:00",
                    "--prompt-en",
                    "changed prompt",
                    "--prompt-id",
                    "0000000000000000",
                    "--attempt",
                    "1",
                    "--status",
                    "success",
                    "--ledger",
                    str(ledger),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 2)
            self.assertIn("prompt_id mismatch", result.stderr)
            self.assertFalse(ledger.exists())

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

    def test_concept_recipe_supporting_tags_are_registered(self):
        expected = {
            "costume_style": {
                "frill_apron_maid_costume",
                "nurse_uniform_costume",
                "miner_workwear_hard_hat",
                "royal_princess_hanbok",
            },
            "prop": {
                "nonfunctional_pickaxe_prop",
                "real_survival_knife",
                "real_saber",
                "real_longbow",
                "real_holstered_service_pistol",
                "deactivated_crossbow_display_prop",
                "vintage_film_camera_prop",
                "single_playing_card_calling_card_prop",
                "black_leather_gloves_prop",
                "sealed_mission_envelope_prop",
                "sheathed_utility_knife_prop",
                "phoenix_hairpin_prop",
                "ornate_gothic_perfume_bottle",
                "compact_mirror",
                "flower_bouquet",
            },
            "action": {
                "standing_silence",
                "looking_down_at_low_camera",
                "weapon_low_ready_stance",
                "concealed_holster_adjust_pose",
                "doorframe_shadow_watch",
                "staged_archery_draw_pose",
                "blade_guarded_ready_pose",
                "recorded_by_surveillance",
            },
            "location": {
                "maid_cafe_interior",
                "hospital_corridor",
                "underground_mine_tunnel_set",
                "royal_princess_chamber",
                "underground_parking_garage",
                "joseon_palace_interior",
                "luxury_hotel_corridor",
                "luxury_hotel_lobby",
                "yellow_tape_alley_reportage",
                "reflective_dark_corridor",
                "mirrored_elevator_box",
                "broken_mirror_fragment_studio",
                "glass_office",
            },
            "lighting": {
                "neon",
                "flickering_fluorescent_horror",
                "headlights",
                "single_flashlight_beam",
                "candlelight",
                "rim_light",
                "hard_flash",
                "chiaroscuro_window_light",
                "low_key",
                "chiaroscuro",
            },
            "mood": {"clinical", "elegant", "uncanny", "reportage_tense_noir", "occult_noir"},
            "composition": {
                "cctv_corner_frame",
                "paparazzi_diagonal_flash",
                "broken_glass_fragments_frame",
                "frame_within_frame",
                "silhouette",
                "low_angle",
                "centered_symmetry",
            },
            "expression": {"cold_unreadable_stare"},
            "appearance_type": {"classic_elegant"},
            "subject": {"fashion_influencer"},
            "wardrobe_style": {"clean_blazer_trousers", "minimal_black_dress", "hoodie_shorts_sneakers"},
            "light_direction": {"side_light_left"},
            "light_shape": {"venetian_blind_shadows"},
            "light_type": {"narrow_spotlight"},
            "light_intensity": {"deep_shadow_detail"},
            "color": {"desaturated_cold_blue", "luxury_black_gold", "clinical_white", "tungsten_cinestill_blue_red", "monochrome"},
        }

        for slot, ids in expected.items():
            with self.subTest(slot=slot):
                actual = {entry["id"] for entry in self.data["slots"][slot]}
                self.assertTrue(ids.issubset(actual))

    def test_all_concept_recipe_forced_slots_are_registered(self):
        recipes = json.loads((SKILL_DIR / "assets" / "concept_recipes.json").read_text(encoding="utf-8"))
        slot_ids = {slot: {entry["id"] for entry in entries} for slot, entries in self.data["slots"].items()}
        missing: list[tuple[str, str, str]] = []

        def normalize_values(value):
            if isinstance(value, str):
                return [value]
            if isinstance(value, list):
                return value
            return []

        def check_set(path: str, raw_set) -> None:
            if isinstance(raw_set, dict):
                items = raw_set.items()
            elif isinstance(raw_set, list):
                parsed_items = []
                for raw in raw_set:
                    if not isinstance(raw, str) or "=" not in raw:
                        continue
                    slot, values = raw.split("=", 1)
                    parsed_items.append((slot.strip(), [item.strip() for item in values.replace("|", ",").split(",")]))
                items = parsed_items
            else:
                return

            for slot, values in items:
                for value in normalize_values(values):
                    if value and value not in slot_ids.get(slot, set()):
                        missing.append((path, slot, value))

        for role, recipe in recipes.get("roles", {}).items():
            check_set(f"roles.{role}.set", recipe.get("set"))
        for mixin, recipe in recipes.get("mixins", {}).items():
            check_set(f"mixins.{mixin}.set", recipe.get("set"))
            for bundle in recipe.get("bundles", []):
                check_set(f"mixins.{mixin}.bundles.{bundle.get('id')}.set", bundle.get("set"))

        self.assertEqual(missing, [])

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

    def test_expanded_slots_presets_and_families_are_registered(self):
        slots = self.data["slots"]
        preset_ids = {preset["id"] for preset in self.data["presets"]}
        family_ids = {family["id"] for family in self.data.get("preset_families", [])}

        self.assertTrue(EXPANDED_SLOT_IDS.issubset(slots))
        self.assertTrue(EXPANDED_PRESET_IDS.issubset(preset_ids))
        self.assertTrue(EXPANDED_FAMILY_IDS.issubset(family_ids))

    def test_social_character_slots_presets_and_tags_are_registered(self):
        slots = self.data["slots"]
        preset_ids = {preset["id"] for preset in self.data["presets"]}

        self.assertTrue(SOCIAL_CHARACTER_SLOT_IDS.issubset(slots))
        self.assertTrue(SOCIAL_CHARACTER_PRESET_IDS.issubset(preset_ids))
        for slot, expected_ids in SOCIAL_CHARACTER_TAG_IDS.items():
            actual_ids = {entry["id"] for entry in slots[slot]}
            self.assertTrue(expected_ids.issubset(actual_ids), slot)
        for slot, expected_ids in SOCIAL_CHARACTER_EXISTING_SLOT_TAG_IDS.items():
            actual_ids = {entry["id"] for entry in slots[slot]}
            self.assertTrue(expected_ids.issubset(actual_ids), slot)

    def test_social_character_slots_render_across_detail_levels(self):
        forced = {
            "subject": ["adult_cosplay_performer"],
            "hair_color": ["mint_green_cosplay_wig"],
            "capture_context": ["phone_screen_face_overlay_context"],
            "action": ["phone_screen_face_overlay_pose"],
            "prop": ["phone_with_anime_face_screen"],
            "location": ["simple_indoor_selfie_room"],
            "camera_direction": ["phone_screen_overlay_close_pov"],
            "composition": ["cheek_close_selfie_crop"],
            "light_type": ["phone_screen_face_glow"],
            "texture": ["phone_beauty_filter_smoothing"],
        }
        expected = (
            "mint-green cosplay wig color",
            "smartphone screen used as a face-overlay perspective trick",
            "phone screen showing an anime-style face aligned over the lower face",
        )

        for detail_level in ("detailed", "standard", "compact"):
            with self.subTest(detail_level=detail_level):
                item = self.generate(
                    "phone_screen_face_overlay_cosplay",
                    seed=61,
                    detail_level=detail_level,
                    forced_choices=forced,
                    include_negative=False,
                )
                prompt = item["prompt_en"]
                for phrase in expected:
                    self.assertIn(phrase, prompt)

    def test_botanical_greenhouse_uses_botanical_capture_context(self):
        item = self.generate(
            "botanical_greenhouse_soft_romance",
            seed=64,
            detail_level="compact",
            include_negative=False,
        )
        prompt = item["prompt_en"].lower()

        self.assertEqual(
            item["choices"]["capture_context"]["id"],
            "botanical_editorial_portrait_context",
        )
        self.assertIn("soft botanical editorial portrait capture context", prompt)
        self.assertNotIn("cosplay reference", prompt)
        self.assertNotIn("cosplay_reference_realism_context", json.dumps(item["choices"]))
        self.assertNotIn("fireworks", prompt)

    def test_social_character_light_filters_block_context_noise(self):
        cases = [
            (
                "garden_phone_backlight_portrait",
                701,
                {"streetlamp"},
                ("orange streetlamp", "streetlamp light"),
            ),
            (
                "anime_poster_low_angle_noir_fashion",
                703,
                {"blacklight_uv", "pool_caustic_reflections"},
                ("blacklight", "pool-caustic"),
            ),
            (
                "gas_station_passenger_seat_lifestyle",
                704,
                {"screen_rectangle_mask"},
                ("phone-screen light", "masking shape"),
            ),
        ]

        for preset, seed, banned_ids, banned_phrases in cases:
            with self.subTest(preset=preset):
                item = self.generate(preset, seed=seed, detail_level="compact", include_negative=False)
                selected_ids = {choice["id"] for choice in item["choices"].values()}
                prompt = item["prompt_en"].lower()

                self.assertFalse(selected_ids & banned_ids)
                for phrase in banned_phrases:
                    self.assertNotIn(phrase, prompt)

    def test_compact_subject_modifiers_are_grouped_without_repeated_withs(self):
        item = self.generate(
            "garden_phone_backlight_portrait",
            seed=701,
            detail_level="compact",
            include_negative=False,
            forced_choices={
                "subject": ["beauty_influencer"],
                "appearance_type": ["kbeauty_influencer"],
                "hair_style": ["long_dark_wavy_hair"],
                "hair_color": ["glossy_black_hair"],
                "makeup_style": ["minimal_no_makeup_look"],
                "wardrobe_style": ["summer_dress_sneakers"],
            },
        )
        subject_clause = item["prompt_en"].split(", holding", 1)[0]

        self.assertIn(
            "with K-beauty influencer styling, long dark wavy hair, glossy black hair color, minimal no-makeup look",
            subject_clause,
        )
        self.assertNotIn("with K-beauty influencer styling with", subject_clause)
        self.assertNotIn("with long dark wavy hair with", subject_clause)

    def test_clean_uniform_selfie_blocks_adult_only_slots(self):
        item = self.generate("clean_uniform_vsign_selfie", seed=62, detail_level="compact")
        prompt = item["prompt_en"].lower()

        self.assertNotIn("adult_context", item["choices"])
        self.assertNotIn("fetish_styling", item["choices"])
        self.assertNotIn("body_framing", item["choices"])
        self.assertNotIn("adult", prompt)
        self.assertNotIn("fetish", prompt)

    def test_adult_ribbon_fashion_uses_adult_compatible_ribbon_context(self):
        item = self.generate(
            "adult_crouching_mirror_ribbon_fashion",
            seed=63,
            detail_level="compact",
            include_negative=False,
        )

        self.assertEqual(item["choices"]["prop"]["id"], "red_ribbon_leg_wrap_adult")
        ribbon = next(entry for entry in self.data["slots"]["prop"] if entry["id"] == "red_ribbon_leg_wrap_adult")
        self.assertIn(
            ribbon.get("facets", {}).get("safety_tier", [None])[0],
            {"adult_compatible", "adult_only"},
        )

    def test_expanded_tag_ids_do_not_add_new_global_duplicates(self):
        all_ids = []
        for entries in self.data["slots"].values():
            all_ids.extend(entry["id"] for entry in entries)
        all_ids.extend(preset["id"] for preset in self.data.get("presets", []))
        all_ids.extend(recipe["id"] for recipe in self.data.get("recipes", []))

        for tag_id in EXPANDED_UNIQUE_TAG_IDS:
            self.assertEqual(all_ids.count(tag_id), 1, tag_id)

    def test_new_cinestill_preset_renders_new_slots_without_preposition_duplication(self):
        item = self.generate("cinestill_neon_diner_portrait", seed=1, include_negative=False)
        prompt = item["prompt_en"]
        choices = item["choices"]

        for slot in ("film_emulation", "time_of_day", "weather", "aesthetic_trend"):
            self.assertIn(slot, choices)
        self.assertIn("CineStill 800T tungsten halation", prompt)
        self.assertIn("blue-hour twilight", prompt)
        self.assertIn("inside a retro diner booth", prompt)
        self.assertNotIn("in inside", prompt)
        self.assertNotEqual(choices.get("camera_type", {}).get("id"), "microscope_camera")

    def test_product_surface_preset_renders_surface_and_stable_product_motion(self):
        item = self.generate("product_packshot_white_sweep", seed=2, include_negative=False)
        prompt = item["prompt_en"]
        choices = item["choices"]

        self.assertIn("surface_material", choices)
        self.assertIn(choices["surface_material"]["en"], prompt)
        self.assertEqual(choices.get("motion", {}).get("id"), "stable_tripod")
        self.assertNotEqual(choices.get("location", {}).get("id"), "joseon_palace_interior")

    def test_forced_new_human_detail_slots_render_on_existing_preset(self):
        item = self.generate(
            "street_documentary",
            seed=42,
            include_negative=False,
            forced_choices={
                "film_emulation": ["kodak_portra_400_look"],
                "wearable_accessory": ["wireframe_round_glasses"],
                "facial_hair": ["light_stubble"],
            },
        )
        prompt = item["prompt_en"]

        self.assertIn("Kodak Portra 400", prompt)
        self.assertIn("thin wire-frame round glasses", prompt)
        self.assertIn("light stubble", prompt)

    def test_semantic_mode_is_deterministic_and_traced(self):
        semantic_index = self.build_mock_semantic_index()
        original_embedder = self.generator.embed_texts_with_gemini
        self.generator.embed_texts_with_gemini = self.fake_gemini_vectors
        try:
            first = self.generate(
                "street_documentary",
                seed=42,
                intent="rainy neon night street portrait",
                selection_mode="semantic",
                novelty="medium",
                include_trace=True,
                include_negative=False,
                semantic_index=semantic_index,
                gemini_api_key="test-api-key",
            )
            second = self.generate(
                "street_documentary",
                seed=42,
                intent="rainy neon night street portrait",
                selection_mode="semantic",
                novelty="medium",
                include_trace=True,
                include_negative=False,
                semantic_index=semantic_index,
                gemini_api_key="test-api-key",
            )
        finally:
            self.generator.embed_texts_with_gemini = original_embedder

        self.assertEqual(first["prompt_en"], second["prompt_en"])
        self.assertEqual(first["choices"], second["choices"])
        self.assertEqual(first["semantic_trace"], second["semantic_trace"])
        self.assertEqual(first["semantic_trace"]["selection_mode"], "semantic")
        self.assertEqual(first["semantic_trace"]["intent"], "rainy neon night street portrait")
        self.assertEqual(first["semantic_trace"]["embedding_provider"], "gemini")
        self.assertEqual(first["semantic_trace"]["embedding_model"], "gemini-embedding-2")
        self.assertEqual(first["semantic_trace"]["embedding_dimensions"], 768)
        self.assertEqual(first["semantic_trace"]["filter_strictness"], "soft")
        self.assertEqual(first["semantic_trace"]["semantic_weight"], 0.75)
        self.assertEqual(first["semantic_trace"]["semantic_profile"], "balanced")
        self.assertEqual(first["semantic_trace"]["semantic_axis_mode"], "auto")
        self.assertIn("intent_axes", first["semantic_trace"])
        self.assertIn("intent_steering", first["semantic_trace"])
        self.assertIn("axis_coverage", first["semantic_trace"])
        self.assertIn("surreal_activation_reason", first["semantic_trace"])
        self.assertIsNone(first["semantic_trace"]["preset_score"])
        self.assertEqual(first["semantic_trace"]["semantic_text_recipe"], self.generator.SEMANTIC_TEXT_RECIPE_VERSION)
        self.assertIn("hard_rejected_count", first["semantic_trace"])
        self.assertIn("soft_out_of_filter_selected_count", first["semantic_trace"])
        self.assertGreaterEqual(len(first["semantic_trace"]["slot_scores"]), 1)

    def test_semantic_preset_trace_includes_axis_breakdown_when_preset_is_not_forced(self):
        semantic_index = self.build_mock_semantic_index()
        original_embedder = self.generator.embed_texts_with_gemini
        self.generator.embed_texts_with_gemini = self.fake_gemini_vectors
        try:
            item = self.generate(
                None,
                seed=7,
                intent="urban + horror + fantasy + human portrait",
                selection_mode="semantic",
                include_trace=True,
                include_negative=False,
                semantic_index=semantic_index,
                gemini_api_key="test-api-key",
            )
        finally:
            self.generator.embed_texts_with_gemini = original_embedder

        preset_score = item["semantic_trace"]["preset_score"]
        self.assertIsNotNone(preset_score)
        self.assertIn("intent_axes", preset_score)
        self.assertIn("selected_summary", preset_score)
        self.assertIn("axis_mean", preset_score["selected_summary"])
        self.assertIn("axis_floor", preset_score["selected_summary"])
        self.assertIn("axis_scores", preset_score["selected_summary"])
        self.assertIn("preset_candidate_limit", preset_score)
        self.assertIn("preset_weight_floor", preset_score)
        top_ids = [entry["id"] for entry in preset_score["top"]]
        self.assertEqual(len(top_ids), len(set(top_ids)))

    def test_semantic_axis_family_detection_and_slot_routing(self):
        self.assertEqual(self.generator.axis_families_for_text("urban city street"), ["urban"])
        self.assertEqual(self.generator.axis_families_for_text("방구석 집돌이 작은 방 게임패드"), ["homebody_room"])
        self.assertEqual(self.generator.axis_families_for_text("horror nightmare portrait"), ["human", "horror"])
        context = {
            "axis_vectors": [
                {"text": "human portrait", "families": ["human"], "vector": [1.0, 0.0]},
                {"text": "horror nightmare", "families": ["horror"], "vector": [0.0, 1.0]},
            ]
        }
        self.assertEqual([item["text"] for item in self.generator.routed_axis_items(context, "subject")], ["human portrait"])
        self.assertEqual([item["text"] for item in self.generator.routed_axis_items(context, "mood")], ["horror nightmare"])

    def test_semantic_slot_routed_axis_outweighs_full_intent_centroid(self):
        axis_vectors = [
            {"text": "human portrait", "families": ["human"], "vector": [1.0, 0.0]},
            {"text": "horror nightmare", "families": ["horror"], "vector": [0.0, 1.0]},
        ]
        context = {
            "selection_mode": "semantic",
            "semantic_profile": "balanced",
            "semantic_weight": 1.0,
            "novelty": "medium",
            "query_vector": [0.7071, 0.7071],
            "axis_vectors": axis_vectors,
            "axis_coverage": self.generator.initial_axis_coverage(axis_vectors, "balanced"),
            "picked_vectors": [],
        }

        human_weight, human_summary = self.generator.semantic_candidate_weight(
            {"id": "specific_human", "weight": 1.0},
            [1.0, 0.0],
            context,
            [],
            {},
            {},
            "subject",
        )
        generic_weight, generic_summary = self.generator.semantic_candidate_weight(
            {"id": "generic_centroid", "weight": 1.0},
            [0.7071, 0.7071],
            context,
            [],
            {},
            {},
            "subject",
        )

        self.assertGreater(human_weight, generic_weight)
        self.assertEqual(human_summary["axis"]["routed_axis"], "human portrait")
        self.assertGreater(human_summary["effective_query"], generic_summary["effective_query"])

    def test_semantic_axis_coverage_bonus_prefers_deficit_axis(self):
        axis_vectors = [
            {"text": "human portrait", "families": ["human"], "vector": [1.0, 0.0]},
            {"text": "horror nightmare", "families": ["horror"], "vector": [0.0, 1.0]},
        ]
        context = {
            "selection_mode": "semantic",
            "semantic_profile": "balanced",
            "semantic_weight": 1.0,
            "novelty": "medium",
            "query_vector": [0.7071, 0.7071],
            "axis_vectors": axis_vectors,
            "axis_coverage": self.generator.initial_axis_coverage(axis_vectors, "balanced"),
            "picked_vectors": [],
        }
        self.generator.update_axis_coverage(context, "subject", "specific_human", [1.0, 0.0])

        _weight, summary = self.generator.semantic_candidate_weight(
            {"id": "horror_mood", "weight": 1.0},
            [0.0, 1.0],
            context,
            [],
            {},
            {},
            "mood",
        )

        self.assertEqual(summary["axis"]["routed_axis"], "horror nightmare")
        self.assertGreater(summary["axis"]["coverage_bonus"], 0.0)

    def test_semantic_coherence_rules_strength_and_conflict_factor(self):
        rules = self.data["coherence_rules"]
        soft_window = next(item for item in self.data["slots"]["lighting"] if item["id"] == "soft_window")
        low_key = next(item for item in self.data["slots"]["lighting"] if item["id"] == "low_key")
        quiet_dread = next(item for item in self.data["slots"]["mood"] if item["id"] == "quiet_dread")
        context = {
            "semantic_profile": "balanced",
            "filter_strictness": "soft",
            "axis_vectors": [{"text": "horror", "families": ["horror"], "vector": [1.0, 0.0]}],
            "coherence_rules": rules,
        }

        conflict_factor, conflict_summary = self.generator.semantic_coherence_factor(
            soft_window,
            "lighting",
            context,
            {},
            routed_axis_score=0.5,
        )
        strong_factor, strong_summary = self.generator.semantic_coherence_factor(
            low_key,
            "lighting",
            context,
            {},
            routed_axis_score=0.5,
        )

        self.assertEqual(self.generator.family_signal_strength(quiet_dread, "horror", rules), "strong")
        self.assertEqual(self.generator.family_signal_strength(soft_window, "horror", rules), "none")
        self.assertLess(conflict_factor, 1.0)
        self.assertGreater(strong_factor, 1.0)
        self.assertEqual(conflict_summary["events"][0]["type"], "family_conflict")
        self.assertEqual(strong_summary["events"][0]["type"], "strength_boost")

    def test_semantic_preset_family_coverage_rewards_horror_signal(self):
        rules = self.data["coherence_rules"]
        context = {
            "semantic_profile": "balanced",
            "axis_vectors": [
                {"text": "urban", "families": ["urban"], "vector": [1.0, 0.0]},
                {"text": "horror", "families": ["horror"], "vector": [0.0, 1.0]},
                {"text": "fantasy", "families": ["fantasy"], "vector": [0.5, 0.5]},
                {"text": "human", "families": ["human"], "vector": [0.5, 0.0]},
            ],
            "coherence_rules": rules,
        }
        horror_preset = next(item for item in self.data["presets"] if item["id"] == "analog_horror_found_footage_portrait")
        broad_preset = next(item for item in self.data["presets"] if item["id"] == "cinematic_fantasy_portrait")

        horror_adjustment, horror_summary = self.generator.semantic_preset_family_coverage(horror_preset, context)
        broad_adjustment, broad_summary = self.generator.semantic_preset_family_coverage(broad_preset, context)

        self.assertGreater(horror_adjustment, broad_adjustment)
        self.assertEqual(horror_summary["families"][0]["strength"], "strong")
        self.assertEqual(broad_summary["families"][0]["strength"], "ambient")

    def test_semantic_metadata_drives_group_and_tone_signals(self):
        metadata = self.data["semantic_metadata"]
        fashion_model = next(item for item in self.data["slots"]["subject"] if item["id"] == "fashion_model")
        rooftop_sunset = next(item for item in self.data["slots"]["location"] if item["id"] == "rooftop_sunset")
        mirror_space_fold = next(item for item in self.data["slots"]["surreal_concept"] if item["id"] == "mirror_space_fold")

        context = {
            "semantic_metadata": metadata,
            "coherence_rules": self.data["coherence_rules"],
        }

        self.assertIn("fashion", self.generator.entry_semantic_groups(fashion_model, "subject", context))
        self.assertIn("warm_sunset", self.generator.entry_location_tones(rooftop_sunset, "location", context))
        self.assertEqual(
            self.generator.family_signal_strength(mirror_space_fold, "fantasy", self.data["coherence_rules"], "surreal_concept", context),
            "strong",
        )

    def test_semantic_group_batch_penalty_repeats_subject_group(self):
        batch_context = self.generator.make_batch_context("semantic", "medium", 3)
        context = {"batch_context": batch_context, "semantic_metadata": self.data["semantic_metadata"]}
        fashion_model = next(item for item in self.data["slots"]["subject"] if item["id"] == "fashion_model")
        influencer = next(item for item in self.data["slots"]["subject"] if item["id"] == "influencer_creator")

        self.generator.record_batch_selection(batch_context, "subject_group", "fashion", [1.0, 0.0])
        repeated_factor, repeated_summary = self.generator.batch_group_diversity_penalty(
            context, "subject", fashion_model, [1.0, 0.0]
        )
        fresh_factor, fresh_summary = self.generator.batch_group_diversity_penalty(
            context, "subject", influencer, [0.0, 1.0]
        )

        self.assertLess(repeated_factor, fresh_factor)
        self.assertTrue(repeated_summary["enabled"])
        self.assertEqual(fresh_factor, 1.0)
        self.assertTrue(fresh_summary["enabled"])

    def test_semantic_contextual_affinity_uses_picked_location_for_lighting(self):
        location = next(item for item in self.data["slots"]["location"] if item["id"] == "rainy_neon_alley")
        neon = next(item for item in self.data["slots"]["lighting"] if item["id"] == "neon")
        context = {
            "index": {
                "entries": {
                    self.generator.semantic_entry_key("slot", location, "location"): {"vector": [1.0, 0.0]},
                    self.generator.semantic_entry_key("slot", neon, "lighting"): {"vector": [0.9, 0.1]},
                }
            },
            "axis_vectors": [],
            "semantic_metadata": self.data["semantic_metadata"],
            "coherence_rules": self.data["coherence_rules"],
        }

        score, summary = self.generator.semantic_contextual_affinity("lighting", neon, [0.9, 0.1], context, {"location": location})

        self.assertGreater(score, 0.9)
        self.assertEqual(summary["events"][0]["slot"], "location")

    def test_weak_horror_compensation_boosts_strong_horror_slot(self):
        tense = next(item for item in self.data["slots"]["mood"] if item["id"] == "tense")
        flashlight = next(item for item in self.data["slots"]["lighting"] if item["id"] == "single_flashlight_beam")
        soft_window = next(item for item in self.data["slots"]["lighting"] if item["id"] == "soft_window")
        context = {
            "semantic_profile": "balanced",
            "axis_vectors": [{"text": "horror", "families": ["horror"], "vector": [1.0, 0.0]}],
            "coherence_rules": self.data["coherence_rules"],
            "semantic_metadata": self.data["semantic_metadata"],
        }
        picked = {"mood": tense}

        strong_factor, strong_summary = self.generator.weak_horror_compensation_factor(flashlight, "lighting", context, picked)
        weak_factor, weak_summary = self.generator.weak_horror_compensation_factor(soft_window, "lighting", context, picked)

        self.assertGreater(strong_factor, 1.0)
        self.assertEqual(strong_summary["strength"], "strong")
        self.assertEqual(weak_factor, 1.0)
        self.assertTrue(weak_summary["active"])

    def test_horror_location_tone_conflict_penalizes_warm_sunset(self):
        rooftop_sunset = next(item for item in self.data["slots"]["location"] if item["id"] == "rooftop_sunset")
        context = {
            "semantic_profile": "balanced",
            "filter_strictness": "soft",
            "axis_vectors": [{"text": "horror", "families": ["horror"], "vector": [1.0, 0.0]}],
            "coherence_rules": self.data["coherence_rules"],
            "semantic_metadata": self.data["semantic_metadata"],
        }

        factor, summary = self.generator.semantic_coherence_factor(
            rooftop_sunset,
            "location",
            context,
            {},
            routed_axis_score=0.5,
        )

        self.assertLess(factor, 1.0)
        self.assertEqual(summary["events"][0]["type"], "family_conflict")

    def test_horror_axis_does_not_penalize_fantasy_surreal_slot(self):
        mirror_space_fold = next(item for item in self.data["slots"]["surreal_concept"] if item["id"] == "mirror_space_fold")
        context = {
            "semantic_profile": "balanced",
            "filter_strictness": "soft",
            "axis_vectors": [
                {"text": "horror", "families": ["horror"], "vector": [1.0, 0.0]},
                {"text": "fantasy", "families": ["fantasy"], "vector": [0.0, 1.0]},
            ],
            "coherence_rules": self.data["coherence_rules"],
            "semantic_metadata": self.data["semantic_metadata"],
        }

        factor, summary = self.generator.semantic_coherence_factor(
            mirror_space_fold,
            "surreal_concept",
            context,
            {},
            routed_axis_score=0.6,
        )

        self.assertGreater(factor, 1.0)
        self.assertFalse(any(event["type"] == "family_conflict" for event in summary["events"]))

    def test_product_macro_subject_is_not_classified_as_plant(self):
        silver_ring = next(item for item in self.data["slots"]["subject"] if item["id"] == "silver_ring_jewelry")
        mechanical_watch = next(item for item in self.data["slots"]["subject"] if item["id"] == "mechanical_watch")

        self.assertEqual(self.generator.subject_category({"subject": silver_ring}, self.data), "object")
        self.assertEqual(self.generator.subject_category({"subject": mechanical_watch}, self.data), "object")

    def test_non_human_product_subject_skips_human_only_required_slots(self):
        item = self.generate(
            "pojangmacha_street_food_night",
            seed=91,
            forced_choices={"subject": ["street_food_tteokbokki"]},
            include_trace=True,
            include_negative=False,
        )

        choices = item["choices"]
        self.assertNotIn("appearance_type", choices)
        self.assertNotIn("wardrobe_style", choices)
        self.assertNotIn("wearing", item["prompt_en"].lower())
        skipped = item["semantic_trace"]["generation_contract"]["skipped_slots"]
        self.assertIn("appearance_type", {row["slot"] for row in skipped})
        self.assertIn("wardrobe_style", {row["slot"] for row in skipped})

    def test_craft_documentary_blocks_fashion_modifier_slots(self):
        item = self.generate(
            "documentary_craftsperson_workshop",
            seed=92,
            forced_choices={"subject": ["glassblower_artisan"], "location": ["glassblowing_workshop"]},
            include_trace=True,
            include_negative=False,
        )

        choices = item["choices"]
        self.assertNotIn("appearance_type", choices)
        self.assertNotIn("aesthetic_trend", choices)
        lowered = item["prompt_en"].lower()
        self.assertNotIn("idol", lowered)
        self.assertNotIn("fashion editorial", lowered)
        skipped = item["semantic_trace"]["generation_contract"]["skipped_slots"]
        self.assertIn("appearance_type", {row["slot"] for row in skipped})
        self.assertIn("aesthetic_trend", {row["slot"] for row in skipped})

    def test_forced_wardrobe_bypasses_generation_contract_and_renders(self):
        item = self.generate(
            "documentary_craftsperson_workshop",
            seed=93,
            forced_choices={
                "subject": ["glassblower_artisan"],
                "location": ["glassblowing_workshop"],
                "wardrobe_style": ["clean_blazer_trousers"],
            },
            include_trace=True,
            include_negative=False,
        )

        self.assertEqual(item["choices"]["wardrobe_style"]["id"], "clean_blazer_trousers")
        self.assertIn("clean blazer", item["prompt_en"].lower())
        suppressed = item["semantic_trace"]["generation_contract"]["render_suppressed_slots"]
        self.assertNotIn("wardrobe_style", {row["slot"] for row in suppressed})

    def test_applicability_blocked_slot_does_not_fall_back_to_full_pool(self):
        preset = next(item for item in self.data["presets"] if item["id"] == "analog_personal_brand_portrait")
        subject = next(item for item in self.data["slots"]["subject"] if item["id"] == "fashion_model")
        picked = {"subject": subject}
        contract = self.generator.make_generation_contract(self.data, preset, picked, {})

        entry = self.generator.choose_slot(
            "surface_material",
            self.data,
            preset,
            random.Random(94),
            picked,
            {},
            None,
            contract,
        )

        self.assertIsNone(entry)
        self.assertIn("surface_material", {row["slot"] for row in contract["skipped_slots"]})

    def test_semantic_intent_steering_filters_subject_location_and_mood_pools(self):
        context = {
            "intent_steering": {"mode": "auto", "enabled": True, "families": ["human", "urban", "horror"], "decisions": []},
            "axis_vectors": [
                {"text": "human portrait", "families": ["human"], "vector": [1.0, 0.0]},
                {"text": "urban street", "families": ["urban"], "vector": [0.0, 1.0]},
                {"text": "horror nightmare", "families": ["horror"], "vector": [0.0, 0.5]},
            ],
        }
        subjects = [
            {"id": "robot", "tags": ["object"], "kind": ["object"]},
            {"id": "commuter", "tags": ["human"], "kind": ["human"]},
        ]
        locations = [
            {"id": "forest", "tags": ["nature"]},
            {"id": "rainy_city_street", "tags": ["urban", "street"]},
        ]
        moods = [
            {"id": "calm", "en": "calm and peaceful", "tags": []},
            {"id": "uncanny", "en": "slightly uncanny and unfamiliar", "tags": []},
        ]

        self.assertEqual(
            [item["id"] for item in self.generator.steer_semantic_candidate_pool("subject", subjects, context)],
            ["commuter"],
        )
        self.assertEqual(
            [item["id"] for item in self.generator.steer_semantic_candidate_pool("location", locations, context)],
            ["rainy_city_street"],
        )
        self.assertEqual(
            [item["id"] for item in self.generator.steer_semantic_candidate_pool("mood", moods, context)],
            ["uncanny"],
        )

    def test_homebody_room_intent_steering_filters_drift_candidates(self):
        context = {
            "intent_steering": {"mode": "auto", "enabled": True, "families": ["homebody_room"], "decisions": []},
            "axis_vectors": [
                {"text": "homebody guy in a small bedroom", "families": ["homebody_room"], "vector": [1.0]},
            ],
        }

        subjects = [
            {"id": "young_barista", "en": "a young barista", "tags": ["human", "cafe"], "kind": ["human"]},
            {"id": "traveler_backpack", "en": "a backpacking traveler", "tags": ["human", "travel"], "kind": ["human"]},
            {"id": "gamer_streamer", "en": "a gaming streamer", "tags": ["human", "gaming", "interior"], "kind": ["human"]},
        ]
        locations = [
            {"id": "rainy_city_street", "en": "a rainy city street", "tags": ["urban", "street"]},
            {"id": "cozy_apartment", "en": "a cozy small apartment", "tags": ["interior", "home"]},
            {"id": "small_messy_gaming_bedroom", "en": "a small cluttered gaming bedroom", "tags": ["interior", "home", "gaming"]},
            {"id": "bedroom_mirror", "en": "a bedroom mirror", "tags": ["interior", "home", "social"]},
        ]
        actions = [
            {"id": "live_streaming", "en": "hosting a live stream", "tags": ["social", "technology"]},
            {"id": "checking_phone", "en": "checking a smartphone", "tags": ["daily"]},
            {"id": "slouched_in_gaming_chair", "en": "slouched loosely in a gaming chair", "tags": ["gaming", "home"]},
            {"id": "writing_notes", "en": "writing notes in a notebook", "tags": ["daily"]},
        ]
        props = [
            {"id": "handheld_microphone", "en": "a handheld microphone", "tags": ["stage"]},
            {"id": "gaming_keyboard_mouse_prop", "en": "an RGB keyboard and gaming mouse", "tags": ["gaming"]},
            {"id": "game_controller_prop", "en": "a game controller held in both hands", "tags": ["gaming", "home"]},
            {"id": "coffee_cup_prop", "en": "a ceramic coffee cup", "tags": ["home"]},
        ]
        lighting = [
            {"id": "neon", "en": "neon light reflected on wet pavement", "tags": ["urban"]},
            {"id": "monitor_glow", "en": "blue glow from computer monitors", "tags": ["technology", "interior"]},
        ]

        self.assertEqual(
            [item["id"] for item in self.generator.steer_semantic_candidate_pool("subject", subjects, context)],
            ["gamer_streamer"],
        )
        self.assertEqual(
            [item["id"] for item in self.generator.steer_semantic_candidate_pool("location", locations, context)],
            ["cozy_apartment", "small_messy_gaming_bedroom"],
        )
        self.assertEqual(
            [item["id"] for item in self.generator.steer_semantic_candidate_pool("action", actions, context)],
            ["slouched_in_gaming_chair"],
        )
        self.assertEqual(
            [item["id"] for item in self.generator.steer_semantic_candidate_pool("prop", props, context)],
            ["gaming_keyboard_mouse_prop", "game_controller_prop"],
        )
        self.assertEqual(
            [item["id"] for item in self.generator.steer_semantic_candidate_pool("lighting", lighting, context)],
            ["monitor_glow"],
        )
        self.assertIn(
            {"slot": "prop", "reason": "homebody_room_prop", "before": 4, "after": 2, "tier": "core"},
            context["intent_steering"]["decisions"],
        )
        self.assertIn("prop", self.generator.semantic_steering_slots(context, {"slots": {"prop": [], "subject": []}}))
        self.assertEqual(
            self.generator.compatible_preset_with_semantic_hard_guards({"id": "interior_lifestyle"}, context),
            (True, None),
        )
        self.assertEqual(
            self.generator.compatible_preset_with_semantic_hard_guards({"id": "selfie_mirror_snapshot"}, context),
            (False, "homebody_room_preset"),
        )
        self.assertEqual(
            self.generator.compatible_preset_with_semantic_hard_guards({"id": "creator_brand_profile"}, context),
            (False, "homebody_room_preset"),
        )
        self.assertEqual(
            self.generator.compatible_preset_with_semantic_hard_guards({"id": "gas_station_passenger_seat_lifestyle"}, context),
            (False, "homebody_room_preset"),
        )
        self.assertEqual(
            self.generator.compatible_preset_with_semantic_hard_guards({"id": "pc_bang_neon_session"}, context),
            (False, "homebody_room_preset"),
        )

    def test_homebody_room_core_tags_and_drift_exclusions(self):
        by_slot = {slot: {item["id"]: item for item in entries} for slot, entries in self.data["slots"].items()}

        for entry_id in {
            "game_controller_prop",
            "messy_snacks_prop",
            "rumpled_blanket_prop",
            "instant_ramen_cup_prop",
            "energy_drink_cans_prop",
            "tangled_charging_cables_prop",
            "gaming_headset_on_desk_prop",
        }:
            self.assertEqual(self.generator.homebody_room_signal_tier(by_slot["prop"][entry_id], "prop"), "core")

        for entry_id in {"small_messy_gaming_bedroom", "dim_monitor_glow_bedroom", "floor_mattress_gaming_corner"}:
            self.assertEqual(self.generator.homebody_room_signal_tier(by_slot["location"][entry_id], "location"), "core")
        self.assertEqual(self.generator.homebody_room_signal_tier(by_slot["world"]["lived_in_homebody_room"], "world"), "core")

        for slot, entry_id in [
            ("prop", "coffee_cup_prop"),
            ("prop", "takeaway_coffee_cup"),
            ("action", "writing_notes"),
            ("action", "pouring_coffee"),
            ("location", "bedroom_mirror"),
            ("location", "modern_apartment_living_room"),
            ("world", "cozy_creator"),
            ("world", "clean_social"),
        ]:
            self.assertIsNone(self.generator.homebody_room_signal_tier(by_slot[slot][entry_id], slot))

    def test_homebody_concept_lock_promotes_core_slot_candidates(self):
        context = {
            "intent_steering": {"mode": "auto", "enabled": True, "families": ["homebody_room"], "decisions": []},
            "generation_contract": {"concept_locks": ["방구석 집돌이, 작은 방, 모니터 빛, 게임패드, 간식, 담요"]},
            "axis_vectors": [
                {"text": "homebody guy in a small bedroom", "families": ["homebody_room"], "vector": [1.0]},
            ],
        }
        by_slot = {slot: {item["id"]: item for item in entries} for slot, entries in self.data["slots"].items()}

        props = [
            by_slot["prop"]["gaming_keyboard_mouse_prop"],
            by_slot["prop"]["game_controller_prop"],
            by_slot["prop"]["messy_snacks_prop"],
            by_slot["prop"]["rumpled_blanket_prop"],
            by_slot["prop"]["energy_drink_cans_prop"],
        ]
        self.assertEqual(
            [item["id"] for item in self.generator.steer_semantic_candidate_pool("prop", props, context)],
            ["game_controller_prop", "messy_snacks_prop", "rumpled_blanket_prop"],
        )
        prop_decision = next(item for item in context["intent_steering"]["decisions"] if item["slot"] == "prop")
        self.assertTrue(prop_decision["promoted_by_concept_lock"])
        self.assertEqual(prop_decision["tier"], "core")

        locations = [
            by_slot["location"]["cozy_apartment"],
            by_slot["location"]["small_messy_gaming_bedroom"],
            by_slot["location"]["dim_monitor_glow_bedroom"],
            by_slot["location"]["floor_mattress_gaming_corner"],
        ]
        self.assertEqual(
            [item["id"] for item in self.generator.steer_semantic_candidate_pool("location", locations, context)],
            ["small_messy_gaming_bedroom", "dim_monitor_glow_bedroom", "floor_mattress_gaming_corner"],
        )

    def test_homebody_prop_dedupes_detail_already_carried_by_action(self):
        context = {
            "intent_steering": {"mode": "auto", "enabled": True, "families": ["homebody_room"], "decisions": []},
            "generation_contract": {"concept_locks": ["방구석 집돌이, 게임패드, 간식, 담요"]},
            "axis_vectors": [
                {"text": "homebody guy in a small bedroom", "families": ["homebody_room"], "vector": [1.0]},
            ],
        }
        by_slot = {slot: {item["id"]: item for item in entries} for slot, entries in self.data["slots"].items()}
        promoted = self.generator.steer_semantic_candidate_pool(
            "prop",
            [
                by_slot["prop"]["game_controller_prop"],
                by_slot["prop"]["messy_snacks_prop"],
                by_slot["prop"]["rumpled_blanket_prop"],
            ],
            context,
        )
        deduped = self.generator.avoid_homebody_action_prop_redundancy(
            promoted,
            context,
            {"action": by_slot["action"]["checking_game_controller"]},
        )
        self.assertEqual([item["id"] for item in deduped], ["messy_snacks_prop", "rumpled_blanket_prop"])
        self.assertTrue(any(decision["reason"] == "homebody_room_prop_action_dedup" for decision in context["intent_steering"]["decisions"]))

    def test_homebody_concept_lock_generation_uses_promoted_core_slots(self):
        concept = "방구석 집돌이, 작은 방, 모니터 빛, 게임패드, 간식, 담요"
        semantic_index = self.build_mock_semantic_index()
        original_embedder = self.generator.embed_texts_with_gemini
        self.generator.embed_texts_with_gemini = self.fake_gemini_vectors
        try:
            item = self.generate(
                "interior_lifestyle",
                seed=20260606,
                intent="cozy homebody guy in a small lived-in bedroom at night, gaming desk, snacks, blanket",
                concept_locks=[concept],
                selection_mode="semantic",
                semantic_index=semantic_index,
                gemini_api_key="test-api-key",
                intent_axes=["homebody guy in small bedroom", "gaming desk snacks blanket"],
                include_trace=True,
                include_negative=False,
            )
        finally:
            self.generator.embed_texts_with_gemini = original_embedder

        choices = item["choices"]
        self.assertIn(choices["prop"]["id"], {"game_controller_prop", "messy_snacks_prop", "rumpled_blanket_prop"})
        self.assertIn(
            choices["location"]["id"],
            {"small_messy_gaming_bedroom", "dim_monitor_glow_bedroom", "floor_mattress_gaming_corner"},
        )
        self.assertEqual(choices["light_shape"]["id"], "monitor_rectangle_glow")
        if "world" in choices:
            self.assertEqual(choices["world"]["id"], "lived_in_homebody_room")
        chosen_ids = {entry["id"] for entry in choices.values()}
        self.assertFalse(
            chosen_ids
            & {
                "coffee_cup_prop",
                "takeaway_coffee_cup",
                "writing_notes",
                "pouring_coffee",
                "bedroom_mirror",
                "modern_apartment_living_room",
            }
        )
        decisions = item["semantic_trace"]["intent_steering"]["decisions"]
        self.assertTrue(any(decision.get("slot") == "prop" and decision.get("promoted_by_concept_lock") for decision in decisions))

    def test_homebody_room_core_pool_has_diverse_non_drift_candidates(self):
        context = {
            "intent_steering": {"mode": "auto", "enabled": True, "families": ["homebody_room"], "decisions": []},
            "axis_vectors": [
                {"text": "homebody guy in a small bedroom", "families": ["homebody_room"], "vector": [1.0]},
            ],
        }
        drift_ids = {
            "coffee_cup_prop",
            "takeaway_coffee_cup",
            "writing_notes",
            "pouring_coffee",
            "bedroom_mirror",
            "modern_apartment_living_room",
            "selfie_mirror_snapshot",
            "creator_brand_profile",
        }

        for slot, minimum in {"prop": 7, "action": 4, "location": 4}.items():
            steered = self.generator.steer_semantic_candidate_pool(slot, self.data["slots"][slot], context)
            ids = {item["id"] for item in steered}
            self.assertGreaterEqual(len(ids), minimum)
            self.assertFalse(ids & drift_ids)

    def test_semantic_surreal_axis_auto_activates_unless_explicit_off(self):
        context = {
            "intent_steering": {"mode": "auto", "enabled": True, "families": ["fantasy"], "decisions": []},
            "axis_vectors": [{"text": "fantasy surreal", "families": ["fantasy"], "vector": [1.0]}],
        }
        active = self.generator.should_activate_surreal_layer(
            {},
            random.Random(1),
            "off",
            0.0,
            semantic_context=context,
            mode_explicit=False,
        )
        self.assertTrue(active)
        self.assertEqual(context["surreal_activation_reason"], "semantic_axis")

        explicit_context = {
            "intent_steering": {"mode": "auto", "enabled": True, "families": ["fantasy"], "decisions": []},
            "axis_vectors": [{"text": "fantasy surreal", "families": ["fantasy"], "vector": [1.0]}],
        }
        active = self.generator.should_activate_surreal_layer(
            {},
            random.Random(1),
            "off",
            0.0,
            semantic_context=explicit_context,
            mode_explicit=True,
        )
        self.assertFalse(active)
        self.assertEqual(explicit_context["surreal_activation_reason"], "explicit_off")

    def test_intent_axis_extraction_modes(self):
        explicit = self.generator.extract_intent_axes(
            "urban horror fantasy human portrait",
            explicit_axes=["urban city", "horror mood"],
            semantic_axis_mode="auto",
        )
        self.assertEqual(explicit["source"], "explicit")
        self.assertEqual([item["text"] for item in explicit["items"]], ["urban city", "horror mood"])

        delimiter = self.generator.extract_intent_axes("urban + horror, fantasy and human", semantic_axis_mode="auto")
        self.assertEqual(delimiter["source"], "delimiter")
        self.assertEqual([item["text"] for item in delimiter["items"]], ["urban", "horror", "fantasy", "human"])

        fallback = self.generator.extract_intent_axes("urban horror fantasy human portrait", semantic_axis_mode="auto")
        self.assertEqual(fallback["source"], "fallback")
        self.assertEqual(
            [item["text"] for item in fallback["items"]],
            ["human portrait", "urban city street", "horror fear nightmare", "fantasy magic surreal"],
        )
        product_axes = self.generator.extract_intent_axes("jewelry macro reflection product", semantic_axis_mode="auto")
        self.assertIn("product commercial packshot", [item["text"] for item in product_axes["items"]])
        self.assertIn("jewelry macro reflection", [item["text"] for item in product_axes["items"]])
        homebody_axes = self.generator.extract_intent_axes("방구석 집돌이 작은 방 게임패드", semantic_axis_mode="auto")
        self.assertIn("homebody gamer in a small bedroom", [item["text"] for item in homebody_axes["items"]])
        self.assertIn("metropolitan environment", self.generator.semantic_axis_embedding_text("urban"))
        self.assertIn("gaming desk", self.generator.semantic_axis_embedding_text("방구석 집돌이"))
        self.assertIn("readable face", self.generator.semantic_axis_embedding_text("human portrait"))
        self.assertIn("polished metal", self.generator.semantic_axis_embedding_text("jewelry macro reflection"))

        single = self.generator.extract_intent_axes("quiet portrait", semantic_axis_mode="off")
        self.assertEqual(single["source"], "off")
        self.assertEqual([item["text"] for item in single["items"]], ["quiet portrait"])

        default_axis = self.generator.extract_intent_axes(
            self.generator.DEFAULT_SEMANTIC_INTENT,
            semantic_axis_mode="auto",
            intent_source="default",
        )
        self.assertEqual(default_axis["source"], "default_full_intent")
        self.assertEqual(len(default_axis["items"]), 1)
        self.assertEqual(default_axis["items"][0]["text"], self.generator.DEFAULT_SEMANTIC_INTENT)

    def test_generation_contract_tracks_must_cover_axes(self):
        preset = next(item for item in self.data["presets"] if item["id"] == "jewelry_macro_reflection")
        axis_vectors = [{"text": "product", "families": ["product"], "vector": [1.0, 0.0]}]
        context = {
            "intent_source": "user",
            "intent_axes": {"source": "fallback", "items": [{"text": "product"}]},
            "semantic_profile": "balanced",
            "axis_vectors": axis_vectors,
            "axis_coverage": self.generator.initial_axis_coverage(axis_vectors, "balanced"),
            "coherence_rules": self.data.get("coherence_rules", {}),
            "semantic_metadata": self.data.get("semantic_metadata", {}),
        }
        contract = self.generator.make_generation_contract(self.data, preset, {})
        self.generator.sync_generation_contract_axis_coverage(contract, context)
        self.assertEqual([item["text"] for item in contract["coverage_gaps"]], ["product"])

        genre = next(item for item in self.data["slots"]["genre"] if item["id"] == "product")
        self.generator.update_axis_coverage(context, "genre", "product", [1.0, 0.0], genre)
        self.generator.sync_generation_contract_axis_coverage(contract, context)
        self.assertEqual([item["text"] for item in contract["covered_axes"]], ["product"])
        self.assertEqual(contract["coverage_gaps"], [])

    def test_cliche_weight_softly_reduces_dominant_free_slot_candidate(self):
        context = {
            "selection_mode": "semantic",
            "novelty": "medium",
            "semantic_profile": "balanced",
            "semantic_weight": 0.75,
            "query_vector": [1.0, 0.0],
            "axis_vectors": [],
            "axis_coverage": self.generator.initial_axis_coverage([], "balanced"),
            "picked_vectors": [],
            "coherence_rules": {},
            "semantic_metadata": {"cliche_weights": {"lighting": {"neon": 1.0}}},
        }
        preset = {}
        neon = {"id": "neon", "en": "neon light", "weight": 1.0}
        alternate = {"id": "alternate", "en": "alternate light", "weight": 1.0}
        neon_weight, neon_summary = self.generator.semantic_candidate_weight(
            neon, [1.0, 0.0], context, [], preset, {}, "lighting"
        )
        alternate_weight, alternate_summary = self.generator.semantic_candidate_weight(
            alternate, [1.0, 0.0], context, [], preset, {}, "lighting"
        )

        self.assertLess(neon_weight, alternate_weight)
        self.assertTrue(neon_summary["cliche"]["active"])
        self.assertFalse(alternate_summary["cliche"]["active"])

    def test_coherent_diversity_slots_use_wider_candidate_window(self):
        context = {"semantic_profile": "balanced", "novelty": "medium"}
        self.assertGreater(
            self.generator.semantic_slot_candidate_limit(context, "texture"),
            self.generator.semantic_slot_candidate_limit(context, "subject"),
        )
        self.assertLess(
            self.generator.semantic_slot_weight_floor(context, "texture"),
            self.generator.semantic_slot_weight_floor(context, "subject"),
        )

    def test_semantic_preset_similarity_can_outweigh_base_weight(self):
        context = {"novelty": "medium", "selection_mode": "semantic"}
        close_match = {"id": "cinestill_neon_diner_portrait", "weight": 1.0}
        broad_default = {"id": "street_documentary", "weight": 3.0}

        close_weight = self.generator.semantic_preset_candidate_weight(close_match, 0.80, context)
        broad_weight = self.generator.semantic_preset_candidate_weight(broad_default, 0.50, context)

        self.assertGreater(close_weight, broad_weight)

    def test_semantic_preset_axis_floor_penalizes_single_axis_match(self):
        context = {
            "semantic_profile": "balanced",
            "query_vector": [1.0, 1.0, 1.0, 1.0],
            "axis_vectors": [
                {"text": "urban", "source": "test", "vector": [1.0, 0.0, 0.0, 0.0]},
                {"text": "horror", "source": "test", "vector": [0.0, 1.0, 0.0, 0.0]},
                {"text": "fantasy", "source": "test", "vector": [0.0, 0.0, 1.0, 0.0]},
                {"text": "human", "source": "test", "vector": [0.0, 0.0, 0.0, 1.0]},
            ],
        }

        all_axis_score, all_axis = self.generator.semantic_preset_score_breakdown([1.0, 1.0, 1.0, 1.0], context)
        one_axis_score, one_axis = self.generator.semantic_preset_score_breakdown([1.0, 0.0, 0.0, 0.0], context)

        self.assertGreater(all_axis_score, one_axis_score)
        self.assertEqual(all_axis["axis_floor"], 0.5)
        self.assertEqual(one_axis["axis_floor"], 0.0)

    def test_semantic_preset_single_axis_matches_overall_similarity(self):
        context = {
            "semantic_profile": "balanced",
            "query_vector": [1.0, 1.0, 0.0],
            "axis_vectors": [
                {"text": "quiet portrait", "source": "off", "vector": [1.0, 1.0, 0.0]},
            ],
        }
        score, summary = self.generator.semantic_preset_score_breakdown([1.0, 0.0, 0.0], context)

        self.assertAlmostEqual(score, summary["overall"], places=4)
        self.assertAlmostEqual(summary["overall"], summary["axis_mean"], places=4)
        self.assertAlmostEqual(summary["overall"], summary["axis_floor"], places=4)

    def test_semantic_preset_auto_excludes_adult_context_without_explicit_intent(self):
        data = {
            "version": "test",
            "presets": [
                {"id": "adult_test", "en": "adult test", "weight": 10, "required_slots": ["adult_context"]},
                {"id": "safe_test", "en": "safe test", "weight": 1},
            ],
        }
        context = {
            "selection_mode": "semantic",
            "intent": "urban horror fantasy human portrait",
            "novelty": "medium",
            "semantic_profile": "balanced",
            "semantic_weight": 0.75,
            "intent_axes": {"mode": "auto", "source": "fallback", "items": [{"text": "urban", "source": "fallback"}]},
            "query_vector": [1.0, 0.0],
            "axis_vectors": [{"text": "urban", "source": "fallback", "vector": [1.0, 0.0]}],
            "index": {
                "entries": {
                    "preset:adult_test": {"vector": [1.0, 0.0]},
                    "preset:safe_test": {"vector": [0.8, 0.2]},
                }
            },
            "hard_rejected_count": 0,
            "hard_rejected": [],
        }

        selected = self.generator.choose_preset(data, random.Random(1), None, context)

        self.assertEqual(selected["id"], "safe_test")
        self.assertEqual(context["hard_rejected_count"], 1)
        self.assertEqual(context["preset_score"]["hard_rejected_by_reason"], {"adult_context": 1})

    def test_semantic_soft_filter_can_select_intent_match_outside_preset_filter(self):
        data = {
            "version": "test",
            "presets": [
                {
                    "id": "test_preset",
                    "en": "test preset",
                    "required_slots": ["location"],
                    "filters": {"location": {"ids": ["in_filter_city"]}},
                }
            ],
            "slots": {
                "location": [
                    {"id": "in_filter_city", "en": "a generic city street", "tags": ["urban"], "weight": 0.01},
                    {"id": "out_filter_fog_castle", "en": "a haunted fog castle", "tags": ["fantasy"], "weight": 100},
                ]
            },
        }
        index = {
            "provider": "gemini",
            "dictionary_hash": self.generator.dictionary_hash(data),
            "semantic_text_recipe": self.generator.SEMANTIC_TEXT_RECIPE_VERSION,
            "embedding_model": "gemini-embedding-2",
            "embedding_dimensions": 2,
            "entries": {
                "preset:test_preset": {"vector": [1.0, 0.0]},
                "slot:location:in_filter_city": {"vector": [-1.0, 0.0]},
                "slot:location:out_filter_fog_castle": {"vector": [1.0, 0.0]},
            },
        }
        original_embedder = self.generator.embed_texts_with_gemini
        self.generator.embed_texts_with_gemini = lambda *args, **kwargs: [[1.0, 0.0]]
        try:
            context = self.generator.make_semantic_context(
                data,
                "haunted fog castle",
                "semantic",
                "medium",
                filter_strictness="soft",
                semantic_weight=1.0,
                semantic_profile="balanced",
                semantic_index=index,
                semantic_dimensions=2,
                gemini_api_key="test-api-key",
            )
            selected = self.generator.choose_slot(
                "location",
                data,
                data["presets"][0],
                random.Random(2),
                {},
                semantic_context=context,
            )
        finally:
            self.generator.embed_texts_with_gemini = original_embedder

        self.assertEqual(selected["id"], "out_filter_fog_castle")
        self.assertEqual(context["soft_out_of_filter_selected_count"], 1)
        self.assertEqual(context["slot_scores"][0]["selected_filter"], "out")

    def test_hybrid_hard_filter_keeps_preset_filter_boundary(self):
        data = {
            "version": "test",
            "presets": [
                {
                    "id": "test_preset",
                    "en": "test preset",
                    "required_slots": ["location"],
                    "filters": {"location": {"ids": ["in_filter_city"]}},
                }
            ],
            "slots": {
                "location": [
                    {"id": "in_filter_city", "en": "a generic city street", "tags": ["urban"], "weight": 0.01},
                    {"id": "out_filter_fog_castle", "en": "a haunted fog castle", "tags": ["fantasy"], "weight": 100},
                ]
            },
        }
        index = {
            "provider": "gemini",
            "dictionary_hash": self.generator.dictionary_hash(data),
            "semantic_text_recipe": self.generator.SEMANTIC_TEXT_RECIPE_VERSION,
            "embedding_model": "gemini-embedding-2",
            "embedding_dimensions": 2,
            "entries": {
                "preset:test_preset": {"vector": [1.0, 0.0]},
                "slot:location:in_filter_city": {"vector": [-1.0, 0.0]},
                "slot:location:out_filter_fog_castle": {"vector": [1.0, 0.0]},
            },
        }
        original_embedder = self.generator.embed_texts_with_gemini
        self.generator.embed_texts_with_gemini = lambda *args, **kwargs: [[1.0, 0.0]]
        try:
            context = self.generator.make_semantic_context(
                data,
                "haunted fog castle",
                "hybrid",
                "medium",
                filter_strictness="hard",
                semantic_weight=0.35,
                semantic_profile="conservative",
                semantic_index=index,
                semantic_dimensions=2,
                gemini_api_key="test-api-key",
            )
            selected = self.generator.choose_slot(
                "location",
                data,
                data["presets"][0],
                random.Random(2),
                {},
                semantic_context=context,
            )
        finally:
            self.generator.embed_texts_with_gemini = original_embedder

        self.assertEqual(selected["id"], "in_filter_city")
        self.assertEqual(context["soft_out_of_filter_selected_count"], 0)

    def test_wrapper_defaults_to_semantic_mode(self):
        wrapper = load_wrapper()

        default_args = wrapper.build_forward_args(["--no-negative"])
        self.assertIn("--selection-mode", default_args)
        self.assertEqual(default_args[default_args.index("--selection-mode") + 1], "semantic")
        self.assertIn("--intent", default_args)
        self.assertEqual(default_args[default_args.index("--intent") + 1], wrapper.DEFAULT_SEMANTIC_INTENT)
        self.assertIn("--default-intent", default_args)
        self.assertIn("--semantic-default", default_args)

        explicit_intent_args = wrapper.build_forward_args(["--intent", "rainy neon night portrait", "--no-negative"])
        self.assertEqual(explicit_intent_args[explicit_intent_args.index("--selection-mode") + 1], "semantic")
        self.assertEqual(explicit_intent_args.count("--intent"), 1)
        self.assertIn("rainy neon night portrait", explicit_intent_args)
        self.assertNotIn("--default-intent", explicit_intent_args)
        self.assertNotIn("--semantic-default", explicit_intent_args)

        rule_args = wrapper.build_forward_args(["--selection-mode", "rule", "--no-negative"])
        self.assertNotIn("--intent", rule_args)
        self.assertNotIn("--default-intent", rule_args)
        self.assertNotIn("--semantic-default", rule_args)

        explicit_axis_args = wrapper.build_forward_args(["--intent-axis", "urban", "--no-negative"])
        self.assertIn("--intent", explicit_axis_args)
        self.assertIn("--default-intent", explicit_axis_args)
        self.assertNotIn("--semantic-default", explicit_axis_args)

    def test_default_semantic_missing_index_falls_back_to_rule(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing_index = Path(tmp) / "missing_semantic_index.json"
            result = subprocess.run(
                [
                    sys.executable,
                    str(WRAPPER_PATH),
                    "--semantic-index",
                    str(missing_index),
                    "--include-trace",
                    "--no-negative",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("semantic default fell back to rule mode", result.stderr)
        payload = json.loads(result.stdout)
        trace = payload[0]["semantic_trace"]
        self.assertEqual(trace["selection_mode"], "rule")
        self.assertEqual(trace["requested_selection_mode"], "semantic")
        self.assertTrue(trace["semantic_defaulted"])
        self.assertEqual(trace["intent_source"], "default")
        self.assertIn("fallback_reason", trace)

    def test_explicit_semantic_missing_index_still_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing_index = Path(tmp) / "missing_semantic_index.json"
            result = subprocess.run(
                [
                    sys.executable,
                    str(WRAPPER_PATH),
                    "--selection-mode",
                    "semantic",
                    "--semantic-index",
                    str(missing_index),
                    "--no-negative",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Semantic index", result.stderr)

    def test_explicit_intent_missing_index_still_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing_index = Path(tmp) / "missing_semantic_index.json"
            result = subprocess.run(
                [
                    sys.executable,
                    str(WRAPPER_PATH),
                    "--intent",
                    "rainy neon portrait",
                    "--semantic-index",
                    str(missing_index),
                    "--no-negative",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Semantic index", result.stderr)

    def test_batch_diversity_penalty_is_soft_and_forced_safe(self):
        batch_context = self.generator.make_batch_context("semantic", "medium", 3)
        context = {"batch_context": batch_context}
        first_penalty, _ = self.generator.batch_diversity_penalty(context, "location", "rainy_neon_alley", [1.0, 0.0])
        self.generator.record_batch_selection(batch_context, "location", "rainy_neon_alley", [1.0, 0.0])
        repeated_penalty, summary = self.generator.batch_diversity_penalty(context, "location", "rainy_neon_alley", [1.0, 0.0])
        forced_penalty, _ = self.generator.batch_diversity_penalty(context, "location", "rainy_neon_alley", [1.0, 0.0], forced=True)

        self.assertEqual(first_penalty, 1.0)
        self.assertLess(repeated_penalty, 1.0)
        self.assertGreater(repeated_penalty, 0.0)
        self.assertEqual(forced_penalty, 1.0)
        self.assertEqual(summary["exact_count"], 1)

    def test_semantic_batch_trace_records_shared_history(self):
        semantic_index = self.build_mock_semantic_index()
        batch_context = self.generator.make_batch_context("semantic", "medium", 2)
        original_embedder = self.generator.embed_texts_with_gemini
        self.generator.embed_texts_with_gemini = self.fake_gemini_vectors
        try:
            self.generator.set_batch_index(batch_context, 0)
            first = self.generate(
                None,
                seed=55,
                intent="urban, horror, fantasy, human portrait",
                selection_mode="semantic",
                include_trace=True,
                include_negative=False,
                semantic_index=semantic_index,
                gemini_api_key="test-api-key",
                batch_context=batch_context,
                batch_index=0,
            )
            self.generator.set_batch_index(batch_context, 1)
            second = self.generate(
                None,
                seed=56,
                intent="urban, horror, fantasy, human portrait",
                selection_mode="semantic",
                include_trace=True,
                include_negative=False,
                semantic_index=semantic_index,
                gemini_api_key="test-api-key",
                batch_context=batch_context,
                batch_index=1,
            )
        finally:
            self.generator.embed_texts_with_gemini = original_embedder

        self.assertEqual(first["semantic_trace"]["batch_index"], 0)
        self.assertEqual(second["semantic_trace"]["batch_index"], 1)
        self.assertTrue(second["semantic_trace"]["batch_diversity"]["enabled"])
        self.assertGreater(second["semantic_trace"]["batch_history_summary"]["selected_count"], 0)
        self.assertIn("batch_repetition_penalty", second["semantic_trace"])

    def test_llm_polish_strict_is_explicit_and_preserves_prompt_with_trace(self):
        item = self.generate(
            "compact_urban_fashion_portrait",
            seed=31,
            detail_level="compact",
            include_negative=False,
            include_trace=True,
            llm_polish="strict",
        )

        self.assertEqual(item["polished_prompt_en"], item["prompt_en"])
        self.assertEqual(item["rewrite_trace"]["mode"], "strict")
        self.assertEqual(item["rewrite_trace"]["status"], "preserved")

    def test_virtual_presets_are_hidden_unless_explicitly_requested(self):
        base = subprocess.run(
            [sys.executable, str(WRAPPER_PATH), "--list-presets", "--plain"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        virtual = subprocess.run(
            [sys.executable, str(WRAPPER_PATH), "--list-presets", "--include-virtual", "--plain"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(base.returncode, 0, base.stderr)
        self.assertEqual(virtual.returncode, 0, virtual.stderr)
        self.assertNotIn("virtual:rainy_neon_portrait_recipe", base.stdout)
        self.assertIn("virtual:rainy_neon_portrait_recipe", virtual.stdout)

    def test_dictionary_validator_rejects_unknown_facet_guard(self):
        data = json.loads(TAGS_PATH.read_text(encoding="utf-8"))
        data["slots"]["lighting"][0]["facets"] = {"time_of_day": ["night"]}
        data["slots"]["lighting"][0]["hard_guards"] = {"exclude_facets": ["time_of_day:unknown_value"]}

        with tempfile.TemporaryDirectory() as tmp:
            invalid_path = Path(tmp) / "invalid_tags.json"
            invalid_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(VALIDATOR_PATH), "--tags", str(invalid_path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unknown facet value", result.stderr)

    def test_dictionary_validator_rejects_unknown_coherence_rule_id(self):
        data = json.loads(TAGS_PATH.read_text(encoding="utf-8"))
        data["coherence_rules"]["family_conflicts"]["horror"]["lighting"].append("missing_light_id")

        with tempfile.TemporaryDirectory() as tmp:
            invalid_path = Path(tmp) / "invalid_tags.json"
            invalid_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(VALIDATOR_PATH), "--tags", str(invalid_path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("coherence_rules.family_conflicts.horror.lighting: unknown id missing_light_id", result.stderr)

    def test_dictionary_validator_rejects_unknown_semantic_metadata_id(self):
        data = json.loads(TAGS_PATH.read_text(encoding="utf-8"))
        data["semantic_metadata"]["subject_groups"]["fashion"].append("missing_subject_id")

        with tempfile.TemporaryDirectory() as tmp:
            invalid_path = Path(tmp) / "invalid_tags.json"
            invalid_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(VALIDATOR_PATH), "--tags", str(invalid_path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("semantic_metadata.subject_groups.fashion: unknown subject id missing_subject_id", result.stderr)

    def test_dictionary_validator_rejects_unknown_slot_applicability_id(self):
        data = json.loads(TAGS_PATH.read_text(encoding="utf-8"))
        data["slot_applicability"]["subject_category_overrides"]["missing_subject_id"] = "object"

        with tempfile.TemporaryDirectory() as tmp:
            invalid_path = Path(tmp) / "invalid_tags.json"
            invalid_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(VALIDATOR_PATH), "--tags", str(invalid_path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("slot_applicability.subject_category_overrides: unknown subject id missing_subject_id", result.stderr)

    def test_semantic_index_builder_records_gemini_metadata_and_entries(self):
        original_embedder = self.generator.embed_texts_with_gemini
        self.generator.embed_texts_with_gemini = self.fake_gemini_vectors
        try:
            payload = self.generator.build_semantic_index_payload(
                self.data,
                provider="gemini",
                model="gemini-embedding-2",
                dimensions=768,
                api_key="test-api-key",
            )
        finally:
            self.generator.embed_texts_with_gemini = original_embedder

        self.assertEqual(payload["provider"], "gemini")
        self.assertEqual(payload["embedding_model"], "gemini-embedding-2")
        self.assertEqual(payload["embedding_dimensions"], 768)
        self.assertEqual(payload["semantic_text_recipe"], self.generator.SEMANTIC_TEXT_RECIPE_VERSION)
        self.assertIn("dictionary_hash", payload)
        self.assertIn("preset:street_documentary", payload["entries"])
        self.assertIn("slot:location:rainy_neon_alley", payload["entries"])
        self.assertEqual(len(payload["entries"]["preset:street_documentary"]["vector"]), 768)

    def test_semantic_index_builder_dry_run_does_not_require_api_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "semantic_index.json"
            env = os.environ.copy()
            env.pop("GEMINI_API_KEY", None)
            env.pop("GOOGLE_API_KEY", None)
            result = subprocess.run(
                [
                    sys.executable,
                    str(INDEX_BUILDER_PATH),
                    "--tags",
                    str(TAGS_PATH),
                    "--output",
                    str(out_path),
                    "--dry-run",
                ],
                cwd=ROOT,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(out_path.exists())
        self.assertIn("gemini-embedding-2", result.stdout)
        self.assertIn("768", result.stdout)
        self.assertIn("semantic-text-v2", result.stdout)

    def test_semantic_index_builder_loads_project_env_file(self):
        builder = load_index_builder()
        with tempfile.TemporaryDirectory() as tmp:
            env_path = Path(tmp) / ".env"
            env_path.write_text(
                "\n".join(
                    [
                        "GEMINI_API_KEY='from-env-file'",
                        "GOOGLE_API_KEY=from-google-env-file",
                        "IGNORED_KEY=ignored",
                    ]
                ),
                encoding="utf-8",
            )

            with mock.patch.object(builder, "PROJECT_ROOT", Path(tmp)):
                with mock.patch.dict(os.environ, {}, clear=True):
                    builder.load_project_env()
                    self.assertEqual(os.environ["GEMINI_API_KEY"], "from-env-file")
                    self.assertEqual(os.environ["GOOGLE_API_KEY"], "from-google-env-file")
                    self.assertNotIn("IGNORED_KEY", os.environ)

                with mock.patch.dict(os.environ, {"GEMINI_API_KEY": "already-set"}, clear=True):
                    builder.load_project_env()
                    self.assertEqual(os.environ["GEMINI_API_KEY"], "already-set")
                    self.assertEqual(os.environ["GOOGLE_API_KEY"], "from-google-env-file")

    def test_semantic_index_builder_main_loads_project_env_before_running(self):
        builder = load_index_builder()
        with mock.patch.object(builder, "load_project_env") as load_env:
            with mock.patch.object(sys, "argv", ["build_semantic_index.py", "--dry-run"]):
                self.assertEqual(builder.main(), 0)

        load_env.assert_called_once_with()

    def test_semantic_index_builder_reuses_existing_vectors_after_tag_addition(self):
        builder = load_index_builder()
        base_data = {
            "version": "test",
            "presets": [{"id": "base_portrait", "en": "Base portrait", "ko": "기본 인물"}],
            "recipes": [],
            "slots": {
                "subject": [{"id": "person", "en": "person", "ko": "사람"}],
            },
        }
        updated_data = json.loads(json.dumps(base_data, ensure_ascii=False))
        updated_data["slots"]["subject"].append({"id": "new_actor", "en": "new actor", "ko": "새 배우"})
        embed_calls: list[list[str]] = []

        def fake_embed(texts, model=None, dimensions=768, **kwargs):
            embed_calls.append(list(texts))
            return self.fake_gemini_vectors(texts, model=model, dimensions=dimensions, **kwargs)

        original_embedder = builder.embed_texts_with_gemini
        builder.embed_texts_with_gemini = fake_embed
        try:
            with tempfile.TemporaryDirectory() as tmp:
                output = Path(tmp) / "semantic_index.json"
                checkpoint = Path(tmp) / "semantic_index.json.partial"
                first_payload = builder.build_resumable_index_payload(
                    base_data,
                    output=output,
                    checkpoint=checkpoint,
                    provider="gemini",
                    model="gemini-embedding-2",
                    dimensions=768,
                    batch_size=1,
                    request_interval=0,
                    retry_attempts=0,
                    retry_initial_delay=0,
                    cache_indexes=[],
                )
                builder.write_payload(output, first_payload)
                embed_calls.clear()

                second_payload = builder.build_resumable_index_payload(
                    updated_data,
                    output=output,
                    checkpoint=checkpoint,
                    provider="gemini",
                    model="gemini-embedding-2",
                    dimensions=768,
                    batch_size=1,
                    request_interval=0,
                    retry_attempts=0,
                    retry_initial_delay=0,
                    cache_indexes=[output],
                )
        finally:
            builder.embed_texts_with_gemini = original_embedder

        self.assertEqual(len(embed_calls), 1)
        self.assertEqual(len(embed_calls[0]), 1)
        self.assertIn("new_actor", embed_calls[0][0])
        self.assertEqual(len(second_payload["entries"]), 3)
        self.assertEqual(
            second_payload["entries"]["preset:base_portrait"]["vector"],
            first_payload["entries"]["preset:base_portrait"]["vector"],
        )
        self.assertNotEqual(second_payload["dictionary_hash"], first_payload["dictionary_hash"])

    def test_semantic_index_builder_requires_api_key_for_real_build(self):
        builder = load_index_builder()
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "semantic_index.json"
            with mock.patch.object(builder, "PROJECT_ROOT", Path(tmp)):
                with mock.patch.dict(os.environ, {}, clear=True):
                    with mock.patch.object(
                        sys,
                        "argv",
                        [
                            "build_semantic_index.py",
                            "--tags",
                            str(TAGS_PATH),
                            "--output",
                            str(out_path),
                            "--dimensions",
                            "768",
                            "--request-interval",
                            "0",
                            "--retry-attempts",
                            "0",
                        ],
                    ):
                        with mock.patch("sys.stderr", new_callable=io.StringIO) as stderr:
                            result = builder.main()

        self.assertNotEqual(result, 0)
        self.assertFalse(out_path.exists())
        self.assertIn("GEMINI_API_KEY", stderr.getvalue())

    def test_semantic_index_builder_subprocess_uses_project_env_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source"
            target = source / "skills" / "photo-prompt-image-generator"
            scripts = target / "scripts"
            assets = target / "assets"
            scripts.mkdir(parents=True)
            assets.mkdir(parents=True)
            (source / ".env").write_text("GEMINI_API_KEY=from-env-file\n", encoding="utf-8")
            (scripts / "build_semantic_index.py").write_text(
                INDEX_BUILDER_PATH.read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            (scripts / "prompt_generator.py").write_text(
                GENERATOR_PATH.read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            tags_path = assets / "photo_prompt_tags.json"
            tags_path.write_text(
                json.dumps(
                    {
                        "version": "test",
                        "presets": [],
                        "recipes": [],
                        "slots": {},
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            out_path = Path(tmp) / "semantic_index.json"
            env = os.environ.copy()
            env.pop("GEMINI_API_KEY", None)
            env.pop("GOOGLE_API_KEY", None)
            result = subprocess.run(
                [
                    sys.executable,
                    str(scripts / "build_semantic_index.py"),
                    "--tags",
                    str(tags_path),
                    "--output",
                    str(out_path),
                ],
                cwd=source,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(out_path.exists())
            payload = json.loads(out_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["entries"], {})

    def test_rule_mode_does_not_import_gemini_dependency(self):
        real_import = __import__

        def block_google_genai(name, *args, **kwargs):
            if name == "google" or name.startswith("google.genai"):
                raise ImportError("blocked google.genai import")
            return real_import(name, *args, **kwargs)

        with mock.patch("builtins.__import__", side_effect=block_google_genai):
            item = self.generate("street_documentary", seed=4, include_negative=False)

        self.assertIn("prompt_en", item)

    def test_gemini_embed_reports_missing_sdk(self):
        real_import = __import__

        def block_google_genai(name, *args, **kwargs):
            if name == "google" or name.startswith("google.genai"):
                raise ImportError("No module named google.genai")
            return real_import(name, *args, **kwargs)

        with mock.patch("builtins.__import__", side_effect=block_google_genai):
            with self.assertRaisesRegex(RuntimeError, "google-genai"):
                self.generator.embed_texts_with_gemini(
                    ["rainy neon night street portrait"],
                    model="gemini-embedding-2",
                    dimensions=768,
                    api_key="test-api-key",
                )

    def test_semantic_runtime_rejects_stale_index(self):
        semantic_index = self.build_mock_semantic_index()
        semantic_index["dictionary_hash"] = "stale"

        with self.assertRaisesRegex(ValueError, "dictionary_hash"):
            self.generate(
                "street_documentary",
                seed=42,
                intent="rainy neon night street portrait",
                selection_mode="semantic",
                semantic_index=semantic_index,
                gemini_api_key="test-api-key",
            )

    def test_semantic_runtime_rejects_stale_text_recipe(self):
        semantic_index = self.build_mock_semantic_index()
        semantic_index["semantic_text_recipe"] = "old-recipe"

        with self.assertRaisesRegex(ValueError, "semantic_text_recipe"):
            self.generate(
                "street_documentary",
                seed=42,
                intent="rainy neon night street portrait",
                selection_mode="semantic",
                semantic_index=semantic_index,
                gemini_api_key="test-api-key",
            )

    def test_semantic_runtime_rejects_dimension_mismatch(self):
        semantic_index = self.build_mock_semantic_index(dimensions=16)

        with self.assertRaisesRegex(ValueError, "embedding_dimensions"):
            self.generate(
                "street_documentary",
                seed=42,
                intent="rainy neon night street portrait",
                selection_mode="semantic",
                semantic_index=semantic_index,
                gemini_api_key="test-api-key",
            )


if __name__ == "__main__":
    unittest.main()
