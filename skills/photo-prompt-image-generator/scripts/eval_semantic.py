#!/usr/bin/env python3
"""Evaluate rule, hybrid, and semantic photo-prompt selection against golden intents."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
import os
import random
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Sequence, Set

from prompt_generator import (
    DEFAULT_SEMANTIC_DIMENSIONS,
    SEMANTIC_MODEL_ID,
    SEMANTIC_TEXT_RECIPE_VERSION,
    build_semantic_index_payload,
    coherence_rules_from_source,
    entry_axis_signals,
    entry_conflicts_with_family,
    entry_location_tones,
    entry_semantic_groups,
    family_signal_strength,
    generate_once,
    load_json,
    load_semantic_index_payload,
    make_batch_context,
    preset_family_signal_strength,
    semantic_metadata_from_source,
    semantic_policy_digest,
    semantic_policy_from_source,
    picked_context_tokens,
    picked_scene_context_tokens,
    semantic_policy_schema_version,
    set_batch_index,
    slot_conflict_violations,
    slot_context_rule_violation,
    slot_context_rules_from_source,
    subject_category,
    validate_semantic_index_metadata,
)


JsonDict = Dict[str, Any]

DEFAULT_TAGS = Path(__file__).resolve().parents[1] / "assets" / "photo_prompt_tags.json"
DEFAULT_INDEX = Path(__file__).resolve().parents[1] / "assets" / "photo_prompt_semantic_index.json"
DEFAULT_CONCEPT_RECIPES = Path(__file__).resolve().parents[1] / "assets" / "concept_recipes.json"
DEFAULT_GENERALIZATION_CASES = Path(__file__).resolve().parents[1] / "assets" / "generalization_cases.jsonl"
DEFAULT_GENERALIZATION_HOLDOUT_CASES = Path(__file__).resolve().parents[1] / "assets" / "generalization_holdout_cases.jsonl"
DEFAULT_DOMAIN_HOLDOUT_V2_CASES = Path(__file__).resolve().parents[1] / "assets" / "generalization_domain_holdout_v2.jsonl"
DEFAULT_RETRIEVAL_HOLDOUT_V3_CASES = Path(__file__).resolve().parents[1] / "assets" / "semantic_retrieval_holdout_v3.jsonl"
DEFAULT_RETRIEVAL_HOLDOUT_V4_CASES = Path(__file__).resolve().parents[1] / "assets" / "semantic_retrieval_holdout_v4.jsonl"
WRAPPER_PATH = Path(__file__).resolve().with_name("generate_photo_prompt.py")
PROJECT_ROOT = Path(__file__).resolve().parents[1].parents[1]

PERSON_ONLY_CANDIDATE_SLOTS = {
    "appearance_type",
    "body_framing",
    "body_orientation",
    "body_pose",
    "brow_style",
    "costume_style",
    "eye_detail",
    "eye_makeup_line",
    "facial_hair",
    "footwear",
    "gaze_engagement",
    "hair_color",
    "hair_style",
    "hand_pose",
    "lip_finish",
    "makeup_style",
    "person_origin",
    "silhouette_proportion",
    "skin_finish",
    "wardrobe_style",
}

GOLDEN_CASES: List[JsonDict] = [
    {"intent": "rainy neon night street portrait", "required": {"location": ["rainy_neon_alley", "hong_kong_neon_alley"], "mood": ["tense", "uncanny", "local_night_candid"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "cinestill neon diner portrait", "required": {"film_emulation": ["cinestill_800t_halation"], "location": ["retro_diner_booth", "hong_kong_neon_alley"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "quiet luxury founder profile", "required": {"aesthetic_trend": ["quiet_luxury_aesthetic"], "subject": ["office_worker", "influencer_creator", "fashion_model"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "product flat lay ingredient story", "required": {"surface_material": ["white_marble_surface", "linen_fabric_surface", "dark_walnut_table"], "genre": ["product", "commercial"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "glassblower workshop documentary", "required": {"subject": ["glassblower_artisan"], "location": ["glassblowing_workshop"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "foggy liminal hotel corridor portrait", "required": {"location": ["hotel_corridor_liminal", "luxury_hotel_corridor"], "weather": ["dense_fog_bank", "post_rain_mist"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "botanical greenhouse editorial portrait", "required": {"location": ["botanical_greenhouse", "rooftop_greenhouse"], "genre": ["portrait", "fashion"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "rainy bus stop noir portrait", "required": {"location": ["rainy_bus_stop_shelter", "seoul_bus_stop_snow"], "mood": ["reportage_tense_noir", "melancholic"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "jewelry macro reflection", "required": {"subject": ["silver_ring_jewelry"], "lens": ["105mm_macro", "macro_100mm"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "creator desk setup flatlay", "required": {"location": ["creator_desk_setup"], "surface_material": ["dark_walnut_table", "matte_concrete_surface"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "cinematic blue hour street", "required": {"time_of_day": ["time_blue_hour", "civil_twilight"], "lighting": ["blue_hour"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "night laundromat candid", "required": {"location": ["laundromat_night"], "mood": ["local_night_candid", "melancholic"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "aquarium tunnel portrait", "required": {"location": ["aquarium_tunnel"], "lighting": ["underwater_caustics", "blue_hour"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "coquette cafe portrait", "required": {"aesthetic_trend": ["coquette_aesthetic"], "location": ["retro_diner_booth", "cafe_window"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "balletcore rehearsal room", "required": {"aesthetic_trend": ["balletcore_aesthetic"], "location": ["ballet_rehearsal_studio"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "gorpcore mountain lifestyle", "required": {"aesthetic_trend": ["gorpcore_aesthetic"], "weather": ["morning_frost", "windblown_snow", "dense_fog_bank"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "analog personal brand portrait", "required": {"film_emulation": ["kodak_portra_400_look", "kodak_gold_200_look"], "aesthetic_trend": ["analog_human_story"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "film wedding afterparty flash", "required": {"location": ["wedding_reception_afterparty"], "lighting": ["hard_flash"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "skincare bathroom countertop", "required": {"location": ["bathroom_countertop"], "surface_material": ["white_marble_surface", "subway_tile_wall"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "cinematic product reflection stage", "required": {"surface_material": ["black_acrylic_reflective_surface", "translucent_glass_block"], "genre": ["product", "commercial"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "Hong Kong neon alley with light drizzle", "required": {"location": ["hong_kong_neon_alley"], "weather": ["light_drizzle"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "ceramics studio craft documentary", "required": {"subject": ["ceramic_potter"], "location": ["ceramics_studio"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "vinyl record player on desk analog mood", "required": {"subject": ["vinyl_record_player"], "prop": ["vinyl_record", "analog_cassette"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "transparent umbrella rainy street portrait", "required": {"prop": ["transparent_dome_umbrella", "clear_umbrella"], "weather": ["light_drizzle", "heavy_downpour"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "pre dawn empty street portrait", "required": {"time_of_day": ["pre_dawn_empty_street"], "location": ["rainy_neon_alley", "subway_platform", "hong_kong_neon_alley"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "classic black and white street portrait", "required": {"film_emulation": ["kodak_tri_x_400_bw", "ilford_hp5_bw"], "genre": ["street", "portrait"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "compact CCD digicam party snapshot", "required": {"film_emulation": ["compact_ccd_digicam"], "camera_type": ["compact_digital_camera", "digicam_2000s_camera"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "dense fog bank rural gas station", "required": {"weather": ["dense_fog_bank"], "location": ["rural_gas_station"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "office siren corporate editorial", "required": {"aesthetic_trend": ["office_siren_aesthetic"], "genre": ["fashion", "portrait"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "sport-luxe jersey street style", "required": {"aesthetic_trend": ["sport_luxe_fandom"], "wardrobe_style": ["oversized_jersey_denim_jorts", "athletic_shorts_oversized_blazer"], "footwear": ["chunky_dad_sneakers", "slim_low_profile_sneakers", "sporty_racing_sneakers"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "khaki utility cargo dailywear", "required": {"aesthetic_trend": ["khaki_utility_coded"], "wardrobe_style": ["cargo_utility_tank_set"], "color": ["sage_green_palette"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "Gen Z minimal little white dress", "required": {"aesthetic_trend": ["genz_clean_minimal"], "wardrobe_style": ["little_white_summer_dress", "broderie_anglaise_mini_dress"], "footwear": ["mary_jane_flats", "ballet_flat_sneakers", "slim_low_profile_sneakers"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "dockside sailorcore weekend outfit", "required": {"aesthetic_trend": ["dockside_sailorcore"], "wardrobe_style": ["sailor_stripe_linen_shorts"], "footwear": ["boat_deck_shoes"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "vamp romantic lace editorial", "required": {"aesthetic_trend": ["vamp_romantic"], "garment_detail": ["lace_trim_edge", "broderie_anglaise_eyelet"], "color": ["oxblood_wine_palette"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "TikTok contrast styling athletic shorts blazer", "required": {"wardrobe_style": ["athletic_shorts_oversized_blazer"], "silhouette_proportion": ["oversized_top_tiny_bottom", "sculpted_power_shoulders"], "footwear": ["sporty_racing_sneakers", "chunky_dad_sneakers", "mary_jane_flats"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "crowded morning subway commute after rain", "required": {"location": ["subway_car_morning_commute", "subway_car_inside", "subway_car_interior_candid", "subway_platform"], "crowd_density": ["packed_commute_crowd"], "situation_context": ["morning_commute_rush"], "weather": ["post_rain_mist", "after_rain_wet_pavement", "light_drizzle"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "messy tiny apartment Sunday reset photodump", "required": {"location": ["tiny_apartment_kitchen_late_night", "lived_in_studio_room"], "space_condition": ["lived_in_clutter", "freshly_cleaned_reset"], "situation_context": ["sunday_reset_routine"], "capture_context": ["photodump_candid_sequence_context", "room_tour_wide_phone_context"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "quiet local cafe work-with-me near closing time", "required": {"location": ["local_cafe_closing_window"], "situation_context": ["cafe_work_session", "work_with_me_session"], "space_condition": ["closing_cleanup_state"], "time_of_day": ["closing_time_lights_dimming"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "community garden late summer volunteer break", "required": {"location": ["community_garden_late_summer"], "occasion_context": ["community_volunteer_break"], "crowd_density": ["volunteer_group_scatter"], "prop": ["volunteer_gloves_seedlings_prop"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "graduation day after ceremony with flowers no readable banners", "required": {"location": ["graduation_ceremony_exit"], "occasion_context": ["graduation_after_ceremony"], "prop": ["graduation_flowers_no_banner_prop", "flower_bouquet"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "storm-flooded street convenience store run", "required": {"location": ["after_rain_convenience_store_front", "flooded_street"], "space_condition": ["flooded_ground_level"], "situation_context": ["convenience_store_run"], "weather": ["storm_flood_air", "heavy_downpour"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "AI designer desk with blurred screen glow no readable text", "required": {"location": ["ai_designer_desk_setup"], "situation_context": ["late_night_editing", "desk_setup_tour", "algorithm_fatigue_scroll"], "prop": ["blurred_laptop_screen_glow_prop", "tangled_cables_monitor_prop"], "capture_context": ["blurred_screen_over_shoulder_context", "bts_process_capture_context"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "abandoned empty mall liminal afternoon", "required": {"location": ["liminal_empty_mall"], "space_condition": ["abandoned_derelict_space"], "crowd_density": ["empty_deserted_space"], "mood": ["liminal_fear", "melancholic", "uncanny"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "street food tteokbokki night stall", "required": {"subject": ["street_food_tteokbokki"], "location": ["street_food_stall", "pojangmacha_tent_night"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "minimal skincare product on frosted acrylic riser", "required": {"subject": ["skincare_bottle_single", "skincare_bottle_set"], "surface_material": ["frosted_acrylic_surface", "acrylic_plinth"], "prop": ["acrylic_riser_display_prop", "frosted_skincare_bottle_prop"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "dark academia flatlay with unreadable old book and brass candle", "required": {"aesthetic_trend": ["dark_academia_still_life"], "prop": ["vintage_book_unreadable_pages_prop", "brass_candlestick_prop"], "composition": ["overlapping_paper_ephemera_layout", "stacked_books_prop_tower", "asymmetrical_flatlay_layering"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "travel journal flatlay with fictional boarding pass no readable text", "required": {"subject": ["travel_journal_flatlay_subject"], "prop": ["fictional_boarding_pass_prop", "fictional_passport_prop", "non_legible_city_map_prop"], "composition": ["overlapping_paper_ephemera_layout", "scattered_prop_story_layout"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "coquette ribbon pearl teacup flatlay", "required": {"aesthetic_trend": ["coquette_balletcore_flatlay", "coquette_aesthetic", "balletcore_aesthetic"], "prop": ["satin_ribbon_flatlay_prop", "pearl_strand_flatlay_prop", "porcelain_teacup_saucer_prop"], "composition": ["asymmetrical_flatlay_layering", "curated_flatlay_grid", "topdown_flatlay_social"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "neo deco product still life chrome brass marble", "required": {"aesthetic_trend": ["neo_deco_interior_aesthetic"], "prop": ["chrome_sphere_prop", "brass_tray_prop", "marble_pedestal_prop"], "surface_material": ["red_marble_slab_surface", "brass_tray_surface", "black_acrylic_reflection"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "Y2K desk flatlay flip phone stickers no readable text", "required": {"aesthetic_trend": ["y2k_indie_sleaze_flatlay", "cyber_y2k_aesthetic", "y2k_dailywear_nostalgia"], "prop": ["retro_flip_phone_prop", "mp3_cd_sticker_stack_prop", "holographic_stickers_prop"], "subject": ["y2k_desk_gadget_stack", "old_camera", "vinyl_record_player"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "witchy mystic tarot crystal still life no readable text", "required": {"aesthetic_trend": ["witchy_mystic_still_life", "whimsigoth_aesthetic"], "prop": ["tarot_cards_unreadable_prop", "crystal_cluster_prop", "dried_herbs_glass_vials_prop"], "subject": ["mystic_tabletop_object_arrangement", "typewriter_on_desk", "ceramic_bowl"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "full body contrapposto fashion portrait low angle vertical safe frame", "required": {"body_pose": ["contrapposto_full_body", "editorial_s_curve_pose", "power_stance_feet_apart"], "shot_scale": ["full_length_body_shot", "medium_long_knee_up_shot"], "platform_framing": ["vertical_9x16_ui_safe_frame", "vertical_4x5_feed_safe_frame", "center_safe_subject_frame"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "beauty close-up hand near lips direct gaze", "required": {"shot_scale": ["close_up_face_shot", "medium_close_chest_up_shot", "extreme_close_detail_shot"], "hand_pose": ["hand_near_lips", "hand_touching_face"], "gaze_engagement": ["direct_camera_aware", "looking_just_past_lens"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "mirror selfie back view with direct eye contact via reflection", "required": {"camera_direction": ["mirror_reflection_camera_view", "mirror_view_direction", "reflected_in_mirror_direction"], "gaze_engagement": ["reflection_direct_gaze", "mirror_reflection_gaze"], "body_orientation": ["looking_back_over_shoulder_orientation", "back_view_orientation"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "wide environmental portrait tiny subject leading lines", "required": {"shot_scale": ["extreme_wide_environment_scale", "wide_full_scene_shot"], "composition": ["strong_leading_lines_vanish", "leading_lines_depth", "low_horizon_environmental_portrait"], "genre": ["portrait", "architecture", "documentary"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "TikTok safe walking away looking back hook", "required": {"platform_framing": ["vertical_9x16_ui_safe_frame", "reels_ui_safe_negative_space", "shorts_thumbnail_safe_face_placement"], "body_pose": ["walking_mid_stride_pose", "turning_back_over_shoulder_pose", "stepping_into_frame_pose"], "gaze_engagement": ["looking_back_over_shoulder_gaze", "looking_away_off_frame"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "architecture leading lines portrait centered symmetry", "required": {"composition": ["strong_leading_lines_vanish", "centered_architecture_symmetry", "architectural_lines_frame", "leading_lines_depth"], "location": ["brutalist_plaza", "gallery_white_cube", "art_gallery_white_hall", "museum_gallery", "modernist_facade"], "shot_scale": ["wide_full_scene_shot", "full_length_body_shot", "extreme_wide_environment_scale"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "eyes closed serene close-up no direct eye contact", "required": {"gaze_engagement": ["eyes_closed_serene"], "shot_scale": ["close_up_face_shot", "medium_close_chest_up_shot"], "subject_framing": ["close_up_face_crop", "head_and_shoulders_crop"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "top-down food table frame no low angle conflict", "required": {"camera_direction": ["strict_top_down_flat_view", "top_down_90", "birds_eye"], "genre": ["food", "still_life"], "composition": ["top_down", "curated_flatlay_grid", "asymmetrical_flatlay_layering"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "quiet rebellion late-night convenience store portrait", "required": {"narrative_core": ["quiet_rebellion_core", "urban_solitude_core"], "mood": ["quiet_defiance", "local_night_candid"], "location": ["convenience_store_night", "after_rain_convenience_store_front"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "analog diary family archive bedroom shrine", "required": {"narrative_core": ["analog_diary_memory_core"], "location": ["bedroom_shrine", "attic_archive_room"], "prop": ["unreadable_diary_prop", "old_postcard_unreadable_prop", "polaroid_stack_unreadable_prop"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "public persona private self glass office phone glow no readable text", "required": {"narrative_core": ["public_private_self_core", "digital_privacy_core"], "concept_tension": ["public_vs_private_tension", "visibility_vs_secrecy_tension"], "capture_context": ["privacy_screen_glow_context", "blurred_screen_over_shoulder_context"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "organic vs synthetic rooftop garden portrait", "required": {"concept_tension": ["organic_vs_synthetic_tension", "urban_vs_wilderness_tension"], "surface_material": ["mossy_concrete_surface", "chrome_mirror_surface", "frosted_glass_surface"], "location": ["rooftop_greenhouse", "botanical_greenhouse", "secret_garden_path"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "romantic decay broken luxury hotel lobby", "required": {"narrative_core": ["romantic_decay_core", "broken_luxury_core"], "concept_tension": ["luxury_vs_decay_tension"], "location": ["old_hotel_lobby_decay", "luxury_hotel_lobby"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "digital detox Sunday afternoon no readable screens", "required": {"narrative_core": ["offline_afternoon_core", "private_ritual_core"], "situation_context": ["digital_detox_afternoon", "sunday_reset_routine"], "mood": ["calm", "ordinary_magic_mood"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "near-future nostalgia AI companion laundromat", "required": {"narrative_core": ["near_future_nostalgia_core", "ai_companion_core"], "concept_tension": ["analog_vs_ai_tension", "nostalgic_vs_futuristic_tension"], "location": ["laundromat_night", "creator_room"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "surreal silliness indoor cloud apartment", "required": {"narrative_core": ["ordinary_magic_core"], "concept_tension": ["playful_vs_eerie_tension", "realistic_vs_dreamlike_tension"], "aesthetic_trend": ["surreal_silliness_aesthetic"]}, "forbidden_tags": ["adult", "fetish"]},
]

OPEN_ENDED_INTENTS = [
    "urban horror fantasy human portrait",
    "surreal rainy city fashion editorial",
    "quiet documentary craftsperson in atmospheric workshop",
    "imperfect analog night portrait",
    "commercial product hero with tactile surface",
    "liminal transport night portrait",
    "cinematic weather mood portrait",
    "creator branding portrait with desk accessories",
    "retro flash social snapshot",
    "blue hour street narrative photograph",
]

MULTI_AXIS_PRESET_GUARDS: List[JsonDict] = [
    {
        "intent": "urban, horror, fantasy, human portrait",
        "blacklisted_presets": ["aerial_city_drone", "kpop_album_cover_y2k_glossy"],
    }
]

MULTI_AXIS_COVERAGE_CASES: List[JsonDict] = [
    {
        "intent": "urban, horror, fantasy, human portrait",
        "runs": 10,
        "minimum_subject_diversity": 3,
        "minimum_preset_diversity": 3,
        "minimum_location_diversity": 4,
        "minimum_mood_diversity": 2,
        "minimum_surreal_concept_diversity": 3,
        "minimum_strong_horror_rate": 0.9,
        "maximum_weak_only_horror_rate": 0.1,
        "maximum_horror_diluting_lighting_rate": 0.1,
        "minimum_subject_group_diversity": 3,
        "minimum_lighting_diversity": 3,
        "maximum_warm_location_horror_conflict_rate": 0.1,
        "minimum_fantasy_axis_coverage_rate": 0.8,
    }
]

BLEED_CHECK_CASES: List[JsonDict] = [
    {
        "name": "jewelry_macro_reflection_product",
        "intent": "jewelry macro reflection product",
        "preset": "jewelry_macro_reflection",
        "forced_choices": {
            "subject": ["silver_ring_jewelry"],
            "lens": ["105mm_macro"],
            "location": ["dark_studio"],
        },
        "forbidden_terms": ["stems", "leaves", "spores", "makeup", "wardrobe", "influencer"],
        "forbidden_slots": ["appearance_type", "hair_style", "makeup_style", "wardrobe_style", "costume_style"],
    },
    {
        "name": "documentary_craftsperson_workshop",
        "intent": "documentary craftsperson workshop",
        "preset": "documentary_craftsperson_workshop",
        "forced_choices": {
            "subject": ["glassblower_artisan"],
            "location": ["glassblowing_workshop"],
        },
        "forbidden_terms": ["idol", "office siren", "fashion editorial", "runway", "glam makeup"],
        "forbidden_slots": ["appearance_type", "makeup_style", "wardrobe_style", "costume_style", "aesthetic_trend"],
    },
    {
        "name": "wildlife_blizzard_documentary",
        "intent": "wildlife blizzard documentary",
        "preset": "nature_wildlife",
        "forced_choices": {
            "subject": ["eagle_perched"],
            "location": ["blizzard_open_plain"],
            "weather": ["windblown_snow"],
        },
        "forbidden_terms": ["product packshot", "fashion", "runway", "makeup", "wardrobe", "studio model"],
        "forbidden_slots": ["appearance_type", "hair_style", "makeup_style", "wardrobe_style", "costume_style", "surface_material"],
    },
    {
        "name": "street_food_night_analog_film",
        "intent": "street food night analog film",
        "preset": "pojangmacha_street_food_night",
        "forced_choices": {
            "subject": ["street_food_tteokbokki"],
            "location": ["pojangmacha_tent_night"],
            "film_emulation": ["kodak_gold_200_look"],
        },
        "forbidden_terms": ["idol", "makeup", "wardrobe", "wearing", "fashion model", "influencer"],
        "forbidden_slots": ["appearance_type", "hair_style", "makeup_style", "wardrobe_style", "costume_style"],
    },
]

DIVERSITY_CHECK_CASES: List[JsonDict] = [
    {
        "name": "urban_horror_fantasy_human_free_slots",
        "intent": "urban, horror, fantasy, human portrait",
        "runs": 12,
        "free_slots": ["lighting", "light_shape", "color", "texture", "lens", "action"],
        "minimum_preservation_rate": 0.85,
        "maximum_top1_dominance": 0.72,
        "minimum_unique_per_slot": 2,
        "maximum_render_suppression_rate": 0.25,
    },
    {
        "name": "jewelry_product_free_slots",
        "intent": "jewelry macro reflection product",
        "preset": "jewelry_macro_reflection",
        "runs": 10,
        "free_slots": ["lighting", "light_shape", "color", "texture", "lens"],
        "minimum_preservation_rate": 0.9,
        "maximum_top1_dominance": 0.75,
        "minimum_unique_per_slot": 2,
        "maximum_render_suppression_rate": 0.25,
    },
    {
        "name": "street_food_analog_free_slots",
        "intent": "street food night analog film",
        "preset": "pojangmacha_street_food_night",
        "runs": 10,
        "free_slots": ["lighting", "color", "texture", "camera_type", "film_emulation", "action"],
        "minimum_preservation_rate": 0.9,
        "maximum_top1_dominance": 0.75,
        "minimum_unique_per_slot": 2,
        "maximum_render_suppression_rate": 0.15,
    },
]

CANDIDATE_PACK_COVERAGE_CASES: List[JsonDict] = [
    {
        "name": "karina_maid_dragon_catpaw_vampire",
        "concept": "카리나 메이드 드래곤 고양이손 달린 흡혈귀",
        "selection_mode": "rule",
        "required_intents": ["카리나", "메이드", "드래곤", "고양이손", "흡혈귀"],
        "expected_uncovered": ["드래곤", "고양이손"],
    },
    {
        "name": "karina_maid_yandere_scaffold",
        "concept": "카리나 메이드 얀데레",
        "selection_mode": "rule",
        "required_intents": ["카리나", "메이드", "얀데레"],
        "required_identity_axes": ["obsessive_possession", "surveillance_gaze", "boundary_collapse"],
        "required_motif_quotas": ["red_thread", "photo_wall", "phone_selfie_mirror"],
        "expect_masked_buckets": True,
    },
    {
        "name": "wonhee_casual_girlfriend_angel",
        "concept": "아일릿 원희 사복 여친 천사",
        "selection_mode": "rule",
        "required_intents": ["아일릿", "원희", "사복", "여친", "천사"],
    },
    {
        "name": "winter_casual_menhera",
        "concept": "윈터 사복 여친 멘헤라",
        "selection_mode": "rule",
        "required_intents": ["윈터", "사복", "여친", "멘헤라"],
    },
    {
        "name": "karina_maid_vampire",
        "concept": "카리나 메이드 흡혈귀",
        "selection_mode": "rule",
        "required_intents": ["카리나", "메이드", "흡혈귀"],
    },
    {
        "name": "karina_maid_succubus",
        "concept": "카리나 메이드 서큐버스",
        "selection_mode": "rule",
        "required_intents": ["카리나", "메이드", "서큐버스"],
        "required_identity_axes": ["dream_threshold", "life_drain_trace", "contractual_invitation"],
    }
]

CONCEPT_BENCHMARK_CASES: List[JsonDict] = [
    {
        "name": "karina_maid_vampire",
        "concept": "카리나 메이드 흡혈귀",
        "prompt_terms": ["maid", "vampire", "reflection"],
        "required_legacy_choices": {
            "costume_style": ["frill_apron_maid_costume"],
            "location": ["maid_cafe_interior"],
        },
    },
    {
        "name": "karina_maid_succubus",
        "concept": "카리나 메이드 서큐버스",
        "prompt_terms": ["maid", "succubus", "invitation", "life-drain"],
        "required_legacy_choices": {
            "costume_style": ["frill_apron_maid_costume"],
            "location": ["maid_cafe_interior"],
            "prop": ["soul_contract_scroll_prop"],
        },
    },
    {
        "name": "winter_nurse_yandere",
        "concept": "윈터 간호사 얀데레",
        "prompt_terms": ["nurse", "yandere", "hospital"],
        "required_legacy_choices": {
            "costume_style": ["nurse_uniform_costume"],
            "location": ["hospital_corridor"],
        },
    },
    {
        "name": "ningning_police_femme_fatale",
        "concept": "닝닝 경찰 팜므파탈",
        "prompt_terms": ["police", "uniform"],
        "required_legacy_choices": {
            "costume_style": ["police_uniform_costume"],
        },
    },
    {
        "name": "giselle_miner_devil",
        "concept": "지젤 광부 악마",
        "prompt_terms": ["miner", "devil", "mine"],
        "required_legacy_choices": {
            "costume_style": ["miner_workwear_hard_hat"],
            "location": ["underground_mine_tunnel_set"],
            "prop": ["nonfunctional_pickaxe_prop", "sealed_mission_envelope_prop"],
        },
    },
    {
        "name": "illit_wonhee_casual_girlfriend_angel",
        "concept": "아일릿 원희 사복 여친 천사",
        "prompt_terms": ["girlfriend", "angel", "casual"],
        "required_legacy_choices": {
            "wardrobe_style": ["hoodie_shorts_sneakers"],
            "prop": ["angel_halo_wings_tail_set"],
        },
    },
    {
        "name": "sullyoon_princess_vampire",
        "concept": "설윤 공주 흡혈귀",
        "prompt_terms": ["princess", "vampire", "royal"],
        "required_legacy_choices": {
            "costume_style": ["royal_ball_gown", "royal_princess_hanbok", "ornate_hanfu_court_dress"],
            "location": ["throne_hall_interior"],
        },
    },
    {
        "name": "yuna_bunnygirl_menhera",
        "concept": "유나 바니걸 멘헤라",
        "prompt_terms": ["bunny", "menhera"],
        "required_legacy_choices": {
            "costume_style": ["bunny_girl_costume"],
        },
    },
]


def fake_vectors(texts: Sequence[str], dimensions: int = DEFAULT_SEMANTIC_DIMENSIONS, **_: Any) -> List[List[float]]:
    vectors = []
    for text in texts:
        digest = hashlib.sha256(str(text).encode("utf-8")).digest()
        vector = [0.0] * dimensions
        for index, byte in enumerate(digest):
            vector[(byte + index) % dimensions] += 1.0 if index % 2 == 0 else -1.0
        norm = sum(value * value for value in vector) ** 0.5
        vectors.append([round(value / norm, 6) if norm else 0.0 for value in vector])
    return vectors


def choice_ids(result: JsonDict) -> Dict[str, str]:
    return {slot: choice.get("id", "") for slot, choice in result.get("choices", {}).items()}


def choice_tags(result: JsonDict) -> set[str]:
    tags: set[str] = set()
    for choice in result.get("choices", {}).values():
        tags |= set(choice.get("tags", []))
        tags |= set(choice.get("kind", []))
    return tags


def choice_payload(result: JsonDict, slot: str) -> JsonDict:
    return result.get("choices", {}).get(slot, {}) or {}


def dictionary_entry(data: JsonDict, slot: str, entry_id: str | None) -> JsonDict:
    if not entry_id:
        return {}
    for entry in data.get("slots", {}).get(slot, []):
        if entry.get("id") == entry_id:
            return entry
    return choice_payload({"choices": {slot: {"id": entry_id}}}, slot)


def text_blob(*parts: Any) -> str:
    return " ".join(str(part or "") for part in parts).lower()


def normalize_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def has_human_subject(result: JsonDict) -> bool:
    subject = choice_payload(result, "subject")
    return "human" in set(subject.get("tags", [])) or "human" in set(subject.get("kind", []))


def has_urban_location(result: JsonDict) -> bool:
    location = choice_payload(result, "location")
    tags = set(location.get("tags", [])) | set(location.get("kind", []))
    blob = text_blob(location.get("id"), location.get("en"), location.get("ko"))
    return bool(tags & {"urban", "street", "city"} or any(term in blob for term in ("urban", "city", "street", "alley", "subway", "neon")))


def has_horror_atmosphere(result: JsonDict) -> bool:
    horror_terms = {
        "horror",
        "fear",
        "nightmare",
        "terror",
        "eerie",
        "uncanny",
        "tense",
        "noir",
        "gothic",
        "dark",
        "suspense",
        "dread",
        "ritual",
        "occult",
        "liminal",
        "haunted",
        "panic",
    }
    for slot in ("mood", "lighting", "light_shape", "weather", "color", "texture"):
        choice = choice_payload(result, slot)
        tags = set(choice.get("tags", [])) | set(choice.get("kind", []))
        blob = text_blob(choice.get("id"), choice.get("en"), choice.get("ko"))
        if tags & horror_terms or any(term in blob for term in horror_terms):
            return True
    return False


def has_strong_horror_signal(data: JsonDict, result: JsonDict) -> bool:
    rules = coherence_rules_from_source(data)
    for slot in ("mood", "lighting", "light_shape", "weather", "color", "texture"):
        choice = choice_payload(result, slot)
        entry = dictionary_entry(data, slot, choice.get("id")) if choice else {}
        if entry and family_signal_strength(entry, "horror", rules, slot, data) == "strong":
            return True
    return False


def has_weak_only_horror_signal(data: JsonDict, result: JsonDict) -> bool:
    return has_horror_atmosphere(result) and not has_strong_horror_signal(data, result)


def has_horror_diluting_lighting(data: JsonDict, result: JsonDict) -> bool:
    rules = coherence_rules_from_source(data)
    mood = dictionary_entry(data, "mood", choice_payload(result, "mood").get("id"))
    if family_signal_strength(mood, "horror", rules, "mood", data) != "strong":
        return False
    for slot in ("lighting", "light_intensity", "light_shape", "color", "texture"):
        choice = choice_payload(result, slot)
        entry = dictionary_entry(data, slot, choice.get("id")) if choice else {}
        if entry and entry_conflicts_with_family(entry, slot, "horror", rules, data):
            return True
    return False


def subject_groups(data: JsonDict, result: JsonDict) -> set[str]:
    entry = dictionary_entry(data, "subject", choice_payload(result, "subject").get("id"))
    return set(entry_semantic_groups(entry, "subject", data))


def location_tones(data: JsonDict, result: JsonDict) -> set[str]:
    entry = dictionary_entry(data, "location", choice_payload(result, "location").get("id"))
    return set(entry_location_tones(entry, "location", data))


def has_warm_location_horror_conflict(data: JsonDict, result: JsonDict) -> bool:
    if not has_strong_horror_signal(data, result):
        return False
    tone_conflicts = ((semantic_metadata_from_source(data).get("family_tone_conflicts", {}) or {}).get("horror", {}) or {})
    return bool(location_tones(data, result) & set(tone_conflicts.get("location_tone", [])))


def has_fantasy_axis_coverage(data: JsonDict, result: JsonDict) -> bool:
    rules = coherence_rules_from_source(data)
    for slot in ("surreal_concept", "surreal_anchor", "wardrobe_style", "subject", "location", "mood"):
        choice = choice_payload(result, slot)
        entry = dictionary_entry(data, slot, choice.get("id")) if choice else {}
        if entry and family_signal_strength(entry, "fantasy", rules, slot, data) == "strong":
            return True
        if entry and "fantasy_strong" in set(entry_axis_signals(entry, slot, data)):
            return True
    return False


def preset_has_horror_strength(data: JsonDict, preset_id: str | None) -> bool:
    if not preset_id:
        return False
    rules = coherence_rules_from_source(data)
    preset = next((item for item in data.get("presets", []) if item.get("id") == preset_id), None)
    return bool(preset and preset_family_signal_strength(preset, "horror", rules, data) in {"strong", "ambient"})


def horror_terms_in_result(result: JsonDict) -> set[str]:
    horror_terms = {
        "horror",
        "fear",
        "nightmare",
        "terror",
        "eerie",
        "uncanny",
        "tense",
        "noir",
        "gothic",
        "dark",
        "suspense",
        "dread",
        "ritual",
        "occult",
        "liminal",
        "haunted",
        "panic",
        "shadow",
        "fog",
        "grime",
        "decay",
    }
    found: set[str] = set()
    for slot in ("mood", "lighting", "light_shape", "weather", "color", "texture"):
        choice = choice_payload(result, slot)
        tags = set(choice.get("tags", [])) | set(choice.get("kind", []))
        blob = text_blob(choice.get("id"), choice.get("en"), choice.get("ko"))
        found |= tags & horror_terms
        found |= {term for term in horror_terms if term in blob}
    return found


def has_surreal_layer(result: JsonDict) -> bool:
    return "surreal_concept" in result.get("choices", {})


def coverage(result: JsonDict, case: JsonDict) -> float:
    choices = choice_ids(result)
    required = case.get("required", {})
    if not required:
        return 1.0
    hits = 0
    for slot, ids in required.items():
        if choices.get(slot) in set(ids):
            hits += 1
    return hits / len(required)


def forbidden_hits(result: JsonDict, case: JsonDict) -> List[str]:
    tags = choice_tags(result)
    return sorted(tags & set(case.get("forbidden_tags", [])))


def build_mock_index(data: JsonDict, generator_module: Any) -> JsonDict:
    original = generator_module.embed_texts_with_gemini
    generator_module.embed_texts_with_gemini = lambda texts, dimensions=DEFAULT_SEMANTIC_DIMENSIONS, **kwargs: fake_vectors(texts, dimensions=dimensions)
    try:
        return build_semantic_index_payload(data, dimensions=DEFAULT_SEMANTIC_DIMENSIONS, api_key="mock")
    finally:
        generator_module.embed_texts_with_gemini = original


def load_project_env() -> None:
    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key not in {"GEMINI_API_KEY", "GOOGLE_API_KEY"} or key in os.environ:
            continue
        value = value.strip().strip("\"'")
        if value:
            os.environ[key] = value


def forbidden_term_hits(prompt: str, forbidden_terms: Sequence[str]) -> List[str]:
    lowered = prompt.lower()
    return [term for term in forbidden_terms if term.lower() in lowered]


def evaluate_bleed_check(
    data: JsonDict,
    cases: Sequence[JsonDict],
    seed: int,
    semantic_index: JsonDict,
    gemini_api_key: str | None = None,
    runs: int = 10,
) -> JsonDict:
    results: List[JsonDict] = []
    for case_index, case in enumerate(cases):
        rows: List[JsonDict] = []
        forced_choices = case.get("forced_choices", {}) or {}
        forced_slots = set(forced_choices)
        for run_index in range(runs):
            result = generate_once(
                data=data,
                rng=random.Random(seed + 4000 + (case_index * 100) + run_index),
                preset_id=case.get("preset"),
                langs=["en"],
                include_negative=False,
                negative_count=12,
                include_choices=True,
                detail_level="detailed",
                forced_choices=forced_choices,
                intent=case["intent"],
                selection_mode="semantic",
                novelty="medium",
                include_trace=True,
                semantic_index=semantic_index,
                gemini_api_key=gemini_api_key,
            )
            choices = choice_ids(result)
            prompt = str(result.get("prompt_en", ""))
            term_hits = forbidden_term_hits(prompt, case.get("forbidden_terms", []))
            slot_hits = [
                slot
                for slot in case.get("forbidden_slots", [])
                if slot in choices and slot not in forced_slots
            ]
            picked_subject = dictionary_entry(data, "subject", choices.get("subject"))
            contract = result.get("semantic_trace", {}).get("generation_contract", {}) or {}
            rows.append(
                {
                    "run_index": run_index,
                    "preset_id": result.get("preset_id"),
                    "subject_category": subject_category({"subject": picked_subject}, data) if picked_subject else "generic",
                    "term_hits": term_hits,
                    "slot_hits": slot_hits,
                    "choices": choices,
                    "skipped_slots": contract.get("skipped_slots", []),
                    "render_suppressed_slots": contract.get("render_suppressed_slots", []),
                    "leaked": bool(term_hits or slot_hits),
                }
            )
        leak_count = sum(1 for row in rows if row["leaked"])
        results.append(
            {
                "name": case.get("name", case.get("intent")),
                "intent": case["intent"],
                "preset": case.get("preset"),
                "runs": runs,
                "leak_count": leak_count,
                "leak_rate": round(leak_count / max(len(rows), 1), 4),
                "passed": leak_count == 0,
                "results": rows,
            }
        )
    return {
        "case_count": len(results),
        "failed_case_count": sum(1 for item in results if not item["passed"]),
        "results": results,
    }


def shannon_entropy(values: Sequence[str]) -> float:
    cleaned = [value for value in values if value]
    if not cleaned:
        return 0.0
    counts = Counter(cleaned)
    total = len(cleaned)
    return -sum((count / total) * math.log2(count / total) for count in counts.values())


def coverage_preservation_rate(contract: JsonDict) -> float:
    must_cover = contract.get("must_cover_axes", []) or []
    if not must_cover:
        return 1.0
    covered = contract.get("covered_axes", []) or []
    return len(covered) / max(len(must_cover), 1)


def generated_prompt_body(prompt: str) -> str:
    markers = [
        "Subject and state:",
        "Scene and environment:",
        "Camera and composition:",
        "Light and atmosphere:",
        "Materials and finish:",
    ]
    offsets = [prompt.find(marker) for marker in markers if prompt.find(marker) >= 0]
    if not offsets:
        return prompt
    return prompt[min(offsets) :]


def prompt_term_rate(prompt: str, terms: Sequence[str]) -> tuple[float, List[str]]:
    terms = [str(term).lower() for term in terms if str(term).strip()]
    if not terms:
        return 1.0, []
    body = generated_prompt_body(prompt).lower()
    hits = sorted({term for term in terms if term in body})
    return len(hits) / max(len(terms), 1), hits


def choice_anchor_rate(result: JsonDict, required: JsonDict) -> tuple[float, List[JsonDict]]:
    if not required:
        return 1.0, []
    choices = choice_ids(result)
    rows: List[JsonDict] = []
    hits = 0
    for slot, raw_ids in required.items():
        expected = set(normalize_list(raw_ids))
        selected = choices.get(slot)
        matched = bool(selected and selected in expected)
        hits += 1 if matched else 0
        rows.append({"slot": slot, "selected": selected, "expected": sorted(expected), "matched": matched})
    return hits / max(len(required), 1), rows


def soft_anchor_metrics(result: JsonDict) -> tuple[float, List[JsonDict], float, List[str], List[str], List[str], JsonDict]:
    trace = result.get("semantic_trace", {}) or {}
    contract = trace.get("generation_contract", {}) or {}
    policy = contract.get("soft_anchor_policy", {}) or {}
    anchors = policy.get("anchors", []) or []
    if not policy.get("enabled") or not anchors:
        return 1.0, [], 1.0, [], [], [], {
            "critical_anchor_match_rate": 1.0,
            "role_anchor_match_rate": 1.0,
            "mixin_salience_match_rate": 1.0,
            "primary_anchor_match_rate": 1.0,
            "anchor_group_match_rate": 1.0,
            "visual_guard_violation_count": 0,
            "render_priority_term_rate": 1.0,
            "required_render_priority_pass_rate": 1.0,
            "soft_repair_success_rate": 1.0,
            "active_denial_pass_rate": 1.0,
            "robot_deep_structural_pass_rate": 1.0,
            "free_slot_constraint_violation_count": 0,
            "body_first_drift_rate": 0.0,
            "critical_term_missing": [],
            "critical_missing": [],
            "source_floor_misses": [],
            "anchor_group_misses": [],
        }
    choices = choice_ids(result)
    by_slot: Dict[str, Set[str]] = {}
    critical_by_slot: Dict[str, Set[str]] = {}
    role_slots: Set[str] = set()
    mixin_slots: Set[str] = set()
    primary_slots: Set[str] = set()
    grouped_slots: Set[str] = set()
    term_by_slot: Dict[str, Set[str]] = {}
    for anchor in anchors:
        slot = str(anchor.get("slot") or "")
        ids = {str(item_id) for item_id in normalize_list(anchor.get("pool")) or normalize_list(anchor.get("ids"))}
        if not slot or not ids:
            continue
        by_slot.setdefault(slot, set()).update(ids)
        if anchor.get("critical"):
            critical_by_slot.setdefault(slot, set()).update(ids)
        sources = {part for part in str(anchor.get("source") or "").split("+") if part}
        if "role" in sources:
            role_slots.add(slot)
        if "mixin" in sources:
            mixin_slots.add(slot)
        if anchor.get("primary"):
            primary_slots.add(slot)
        if normalize_list(anchor.get("groups")):
            grouped_slots.add(slot)
        term_by_slot.setdefault(slot, set()).update(str(term).lower() for term in normalize_list(anchor.get("terms")))
    rows: List[JsonDict] = []
    matched_slots: Set[str] = set()
    for slot, expected in sorted(by_slot.items()):
        selected = choices.get(slot)
        matched = bool(selected and selected in expected)
        if matched:
            matched_slots.add(slot)
        rows.append({"slot": slot, "selected": selected, "expected": sorted(expected), "matched": matched})
    selected_rate = len(matched_slots) / max(len(by_slot), 1)
    critical_matched = {
        slot
        for slot, expected in critical_by_slot.items()
        if choices.get(slot) and choices.get(slot) in expected
    }
    role_matched = {slot for slot in role_slots if slot in matched_slots}
    mixin_matched = {slot for slot in mixin_slots if slot in matched_slots}
    primary_matched = {slot for slot in primary_slots if slot in matched_slots}
    grouped_matched = {slot for slot in grouped_slots if slot in matched_slots}
    critical_anchor_match_rate = len(critical_matched) / len(critical_by_slot) if critical_by_slot else 1.0
    role_anchor_match_rate = len(role_matched) / len(role_slots) if role_slots else 1.0
    mixin_salience_match_rate = len(mixin_matched) / len(mixin_slots) if mixin_slots else 1.0
    primary_anchor_match_rate = len(primary_matched) / len(primary_slots) if primary_slots else 1.0
    anchor_group_match_rate = len(grouped_matched) / len(grouped_slots) if grouped_slots else 1.0
    quality = (result.get("quality", {}) or {})
    checks = quality.get("checks", []) or []
    visual_guard_check = next((check for check in checks if check.get("id") == "soft_visual_guard"), {}) or {}
    render_priority_check = next((check for check in checks if check.get("id") == "soft_render_priority_terms"), {}) or {}
    body_first_check = next((check for check in checks if check.get("id") == "soft_body_first_guard"), {}) or {}
    free_constraint_check = next((check for check in checks if check.get("id") == "soft_free_slot_constraints"), {}) or {}
    repair_check = next((check for check in checks if check.get("id") == "soft_anchor_repair"), {}) or {}
    visual_guard_violations = visual_guard_check.get("violations", []) or []
    free_slot_constraint_violations = free_constraint_check.get("violations", []) or []
    body_first_drift_rate = 1.0 if body_first_check.get("status") == "fail" else 0.0
    priority_groups = render_priority_check.get("groups", []) or []
    render_priority_term_rate = (
        sum(1 for group in priority_groups if group.get("matched")) / max(len(priority_groups), 1)
        if priority_groups
        else 1.0
    )
    required_priority_groups = [group for group in priority_groups if str(group.get("tier", "required")) == "required"]
    required_render_priority_pass_rate = (
        sum(1 for group in required_priority_groups if group.get("matched")) / max(len(required_priority_groups), 1)
        if required_priority_groups
        else 1.0
    )
    repair_state = repair_check.get("repair", {}) or {}
    repair_status = str(repair_state.get("post_render_status") or repair_state.get("status") or "")
    soft_repair_success_rate = 1.0 if repair_status in {"not_needed", "not_applicable", "repaired", "already_satisfied"} else 0.0
    active_denial_groups = [
        group for group in priority_groups if str(group.get("group") or group.get("id") or "") == "tsundere_active_denial"
    ]
    active_denial_pass_rate = (
        sum(1 for group in active_denial_groups if group.get("matched")) / max(len(active_denial_groups), 1)
        if active_denial_groups
        else 1.0
    )
    robot_deep_groups = [
        group for group in priority_groups if str(group.get("group") or group.get("id") or "") == "robot_deep_structural"
    ]
    robot_deep_structural_pass_rate = (
        sum(1 for group in robot_deep_groups if group.get("matched")) / max(len(robot_deep_groups), 1)
        if robot_deep_groups
        else 1.0
    )
    critical_term_slots = set(critical_by_slot)
    term_groups = [
        (slot, sorted(term_by_slot.get(slot, set())))
        for slot in sorted(matched_slots | critical_term_slots)
        if term_by_slot.get(slot)
    ]
    if not term_groups:
        body_rate = 1.0 if matched_slots else 0.0
        return selected_rate, rows, body_rate, [], [], [], {
            "critical_anchor_match_rate": critical_anchor_match_rate,
            "role_anchor_match_rate": role_anchor_match_rate,
            "mixin_salience_match_rate": mixin_salience_match_rate,
            "primary_anchor_match_rate": primary_anchor_match_rate,
            "anchor_group_match_rate": anchor_group_match_rate,
            "visual_guard_violation_count": len(visual_guard_violations),
            "render_priority_term_rate": render_priority_term_rate,
            "required_render_priority_pass_rate": required_render_priority_pass_rate,
            "soft_repair_success_rate": soft_repair_success_rate,
            "active_denial_pass_rate": active_denial_pass_rate,
            "robot_deep_structural_pass_rate": robot_deep_structural_pass_rate,
            "free_slot_constraint_violation_count": len(free_slot_constraint_violations),
            "body_first_drift_rate": body_first_drift_rate,
            "critical_term_missing": [],
            "critical_missing": sorted(set(critical_by_slot) - critical_matched),
            "source_floor_misses": [],
            "anchor_group_misses": [],
        }
    body = generated_prompt_body(str(result.get("prompt_en", ""))).lower()
    hits: List[str] = []
    missing: List[str] = []
    matched_term_groups = 0
    for slot, terms in term_groups:
        matched_terms = [term for term in terms if term in body]
        if matched_terms:
            matched_term_groups += 1
            hits.extend(matched_terms)
        else:
            missing.append(f"{slot}:{'|'.join(terms)}")
    hits = sorted(set(hits))
    missing = sorted(set(missing))
    body_rate = matched_term_groups / max(len(term_groups), 1)
    failures: List[str] = []
    if selected_rate <= 0:
        failures.append("no_soft_anchor_ids_selected")
    if body_rate <= 0:
        failures.append("no_soft_anchor_terms_rendered")
    match_status = policy.get("match_status", {}) or {}
    critical_missing = sorted(set(match_status.get("critical_missing", [])) or (set(critical_by_slot) - critical_matched))
    source_floor_misses = match_status.get("source_floor_misses", []) or []
    anchor_group_misses = match_status.get("group_floor_misses", []) or []
    failures.extend(match_status.get("failure_reasons", []) or [])
    if visual_guard_violations:
        failures.append("visual_guard_violation")
    if render_priority_term_rate < 1.0:
        failures.append("render_priority_term_missing")
    if required_render_priority_pass_rate < 1.0:
        failures.append("required_render_priority_term_missing")
    if free_slot_constraint_violations:
        failures.append("free_slot_constraint_violation")
    return selected_rate, rows, body_rate, hits, missing, failures, {
        "critical_anchor_match_rate": critical_anchor_match_rate,
        "role_anchor_match_rate": role_anchor_match_rate,
        "mixin_salience_match_rate": mixin_salience_match_rate,
        "primary_anchor_match_rate": primary_anchor_match_rate,
        "anchor_group_match_rate": anchor_group_match_rate,
        "visual_guard_violation_count": len(visual_guard_violations),
        "render_priority_term_rate": render_priority_term_rate,
        "required_render_priority_pass_rate": required_render_priority_pass_rate,
        "soft_repair_success_rate": soft_repair_success_rate,
        "active_denial_pass_rate": active_denial_pass_rate,
        "robot_deep_structural_pass_rate": robot_deep_structural_pass_rate,
        "free_slot_constraint_violation_count": len(free_slot_constraint_violations),
        "body_first_drift_rate": body_first_drift_rate,
        "critical_term_missing": sorted(
            f"{slot}:{'|'.join(sorted(term_by_slot.get(slot, set())))}"
            for slot in critical_term_slots
            if term_by_slot.get(slot) and not any(term in hits for term in term_by_slot.get(slot, set()))
        ),
        "critical_missing": critical_missing,
        "source_floor_misses": source_floor_misses,
        "anchor_group_misses": anchor_group_misses,
    }


def selected_anchor_variants(result: JsonDict) -> List[JsonDict]:
    trace = result.get("semantic_trace", {}) or {}
    contract = trace.get("generation_contract", {}) or {}
    policy = contract.get("soft_anchor_policy", {}) or {}
    choices = choice_ids(result)
    rows: List[JsonDict] = []
    seen: Set[tuple[str, str, str]] = set()
    for anchor in policy.get("anchors", []) or []:
        group = str(anchor.get("variant_group") or "")
        slot = str(anchor.get("slot") or "")
        selected = choices.get(slot)
        pool = set(normalize_list(anchor.get("pool")) or normalize_list(anchor.get("ids")))
        key = (group, slot, str(selected))
        if group and slot and selected and selected in pool and key not in seen:
            seen.add(key)
            rows.append({"group": group, "slot": slot, "selected": selected})
    return rows


def anchor_variant_diversity(rows: Sequence[JsonDict]) -> JsonDict:
    variants = [variant for row in rows for variant in row.get("anchor_variants", []) or []]
    if not variants:
        return {
            "anchor_variant_diversity_rate": 1.0,
            "anchor_variant_top1_dominance": 0.0,
            "anchor_variant_unique_count": 0,
            "anchor_variant_total_count": 0,
            "anchor_variant_group_metrics": {},
        }
    group_metrics: Dict[str, JsonDict] = {}
    for group in sorted({str(item.get("group")) for item in variants if item.get("group")}):
        selected = [str(item.get("selected")) for item in variants if item.get("group") == group and item.get("selected")]
        counts = Counter(selected)
        total = len(selected)
        unique = len(counts)
        group_metrics[group] = {
            "total": total,
            "unique": unique,
            "diversity_rate": round(unique / max(total, 1), 4),
            "top1_dominance": round(max(counts.values(), default=0) / max(total, 1), 4),
            "top": counts.most_common(5),
        }
    all_selected = [str(item.get("selected")) for item in variants if item.get("selected")]
    counts = Counter(all_selected)
    return {
        "anchor_variant_diversity_rate": round(len(counts) / max(len(all_selected), 1), 4),
        "anchor_variant_top1_dominance": round(max(counts.values(), default=0) / max(len(all_selected), 1), 4),
        "anchor_variant_unique_count": len(counts),
        "anchor_variant_total_count": len(all_selected),
        "anchor_variant_group_metrics": group_metrics,
    }


VISUAL_REVIEW_FIELDS = (
    "dual_read",
    "archetype_first_read",
    "body_drift",
    "preset_conflict",
    "role_anchor",
    "mixin_anchor",
    "body_coverage_guard",
    "render_modality",
    "framing_constraint",
    "body_emphasis_survived",
)
VISUAL_REVIEW_ENUMS: Dict[str, set[str]] = {
    "dual_read": {"pass", "fail"},
    "archetype_first_read": {"pass", "fail"},
    "body_drift": {"none", "present", "not_applicable"},
    "preset_conflict": {"none", "present"},
    "role_anchor": {"pass", "fail", "not_applicable"},
    "mixin_anchor": {"pass", "fail", "not_applicable"},
    "body_coverage_guard": {"pass", "fail", "not_applicable"},
    "render_modality": {"pass", "fail"},
    "framing_constraint": {"pass", "fail"},
    "body_emphasis_survived": {"no", "yes", "not_applicable"},
}
VISUAL_REVIEW_PASS_VALUES: Dict[str, set[str]] = {
    "dual_read": {"pass"},
    "archetype_first_read": {"pass"},
    "body_drift": {"none", "not_applicable"},
    "preset_conflict": {"none"},
    "role_anchor": {"pass", "not_applicable"},
    "mixin_anchor": {"pass", "not_applicable"},
    "body_coverage_guard": {"pass", "not_applicable"},
    "render_modality": {"pass"},
    "framing_constraint": {"pass"},
    "body_emphasis_survived": {"no", "not_applicable"},
}


def load_visual_review(path: Path) -> JsonDict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return {"cases": payload}
    if isinstance(payload, dict):
        if isinstance(payload.get("cases"), list):
            return payload
        if isinstance(payload.get("results"), list):
            payload["cases"] = payload["results"]
            return payload
    raise ValueError("--visual-review must point to a list or an object with cases/results")


def summarize_visual_review(path: Path) -> JsonDict:
    payload = load_visual_review(path)
    cases = [case for case in payload.get("cases", []) if isinstance(case, dict)]
    contract_failures: List[JsonDict] = []
    if payload.get("schema_version") != "photo-visual-review/v1":
        contract_failures.append({"check": "schema_version", "reason": "expected photo-visual-review/v1"})
    provenance = payload.get("provenance") if isinstance(payload.get("provenance"), dict) else {}
    missing_provenance = [
        field
        for field in ("generator_version", "tags_hash", "reviewer", "reviewed_at")
        if not str(provenance.get(field) or "").strip()
    ]
    if missing_provenance:
        contract_failures.append({"check": "provenance", "missing": missing_provenance})
    if not cases:
        contract_failures.append({"check": "cases", "reason": "at least one reviewed render is required"})
    field_summaries: JsonDict = {}
    failed_cases: List[JsonDict] = []
    review_focus_result_count = 0
    failed_review_focus_results: List[JsonDict] = []
    for field in VISUAL_REVIEW_FIELDS:
        counts: Counter[str] = Counter(str(case.get(field, "missing") or "missing") for case in cases)
        pass_count = sum(counts.get(value, 0) for value in VISUAL_REVIEW_PASS_VALUES[field])
        field_summaries[field] = {
            "counts": dict(sorted(counts.items())),
            "pass_rate": round(pass_count / max(len(cases), 1), 4),
        }
    for case_index, case in enumerate(cases):
        missing_case_fields = [
            field
            for field in ("case", "prompt_id", "image_id", *VISUAL_REVIEW_FIELDS)
            if field not in case or case.get(field) in {None, ""}
        ]
        if missing_case_fields:
            contract_failures.append(
                {"check": "case_fields", "case_index": case_index, "missing": missing_case_fields}
            )
        for field in VISUAL_REVIEW_FIELDS:
            value = str(case.get(field) or "")
            if value and value not in VISUAL_REVIEW_ENUMS[field]:
                contract_failures.append(
                    {
                        "check": "case_field_enum",
                        "case_index": case_index,
                        "field": field,
                        "value": value,
                        "allowed": sorted(VISUAL_REVIEW_ENUMS[field]),
                    }
                )
        not_applicable_fields = [
            field for field in VISUAL_REVIEW_FIELDS if case.get(field) == "not_applicable"
        ]
        if not_applicable_fields and not str(case.get("not_applicable_reason") or "").strip():
            contract_failures.append(
                {
                    "check": "not_applicable_reason",
                    "case_index": case_index,
                    "fields": not_applicable_fields,
                    "reason": "not_applicable values require a non-empty case-level reason",
                }
            )
        case_focus_failed = False
        focus_results = case.get("review_focus_results")
        if focus_results is not None:
            if not isinstance(focus_results, list) or not focus_results:
                contract_failures.append(
                    {
                        "check": "review_focus_results",
                        "case_index": case_index,
                        "reason": "review_focus_results must be a non-empty list when supplied",
                    }
                )
            else:
                for focus_index, focus_result in enumerate(focus_results):
                    if not isinstance(focus_result, dict):
                        contract_failures.append(
                            {
                                "check": "review_focus_result",
                                "case_index": case_index,
                                "focus_index": focus_index,
                                "reason": "review focus result must be an object",
                            }
                        )
                        continue
                    review_focus_result_count += 1
                    missing_focus_fields = [
                        field
                        for field in ("focus", "outcome", "evidence")
                        if not str(focus_result.get(field) or "").strip()
                    ]
                    if missing_focus_fields:
                        contract_failures.append(
                            {
                                "check": "review_focus_result_fields",
                                "case_index": case_index,
                                "focus_index": focus_index,
                                "missing": missing_focus_fields,
                            }
                        )
                    outcome = str(focus_result.get("outcome") or "")
                    if outcome and outcome not in {"pass", "fail"}:
                        contract_failures.append(
                            {
                                "check": "review_focus_result_enum",
                                "case_index": case_index,
                                "focus_index": focus_index,
                                "value": outcome,
                                "allowed": ["fail", "pass"],
                            }
                        )
                    if outcome == "fail":
                        case_focus_failed = True
                        failed_review_focus_results.append(
                            {
                                "case": case.get("case") or case.get("concept"),
                                "focus": focus_result.get("focus"),
                                "evidence": focus_result.get("evidence"),
                            }
                        )
        failures: List[str] = []
        if case.get("dual_read") == "fail":
            failures.append("dual_read")
        if case.get("archetype_first_read") == "fail":
            failures.append("archetype_first_read")
        if case.get("body_drift") == "present":
            failures.append("body_drift")
        if case.get("preset_conflict") == "present":
            failures.append("preset_conflict")
        if case.get("body_coverage_guard") == "fail":
            failures.append("body_coverage_guard")
        if case.get("render_modality") == "fail":
            failures.append("render_modality")
        if case.get("framing_constraint") == "fail":
            failures.append("framing_constraint")
        if case.get("body_emphasis_survived") == "yes":
            failures.append("body_emphasis_survived")
        if case_focus_failed:
            failures.append("review_focus")
        if case.get("role_anchor") == "fail":
            failures.append("role_anchor")
        if case.get("mixin_anchor") == "fail":
            failures.append("mixin_anchor")
        if failures:
            failed_cases.append({"case": case.get("case") or case.get("concept"), "failures": failures})
    return {
        "visual_review": {
            "path": str(path),
            "case_count": len(cases),
            "field_summaries": field_summaries,
            "failed_case_count": len(failed_cases),
            "failed_cases": failed_cases,
            "contract_failure_count": len(contract_failures),
            "contract_failures": contract_failures,
            "review_focus_result_count": review_focus_result_count,
            "failed_review_focus_result_count": len(failed_review_focus_results),
            "failed_review_focus_results": failed_review_focus_results,
            "passed": not failed_cases and not contract_failures,
        }
    }


def run_wrapper_concept(
    *,
    concept: str,
    concept_mode: str,
    seed: int,
    tags_path: Path,
    semantic_index_path: Path,
    anchor_diversity_ledger: Path | None = None,
) -> JsonDict:
    command = [
        sys.executable,
        str(WRAPPER_PATH),
        "--tags",
        str(tags_path),
        "--semantic-index",
        str(semantic_index_path),
        "--concept",
        concept,
        "--concept-mode",
        concept_mode,
        "--selection-mode",
        "semantic",
        "--seed",
        str(seed),
        "--n",
        "1",
        "--lang",
        "en",
        "--detail-level",
        "detailed",
        "--include-choices",
        "--include-trace",
        "--json-output",
        "--no-negative",
    ]
    if anchor_diversity_ledger is not None:
        command.extend(["--anchor-diversity-ledger", str(anchor_diversity_ledger)])
    completed = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=300,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "concept wrapper failed for "
            f"{concept!r} mode={concept_mode!r} seed={seed}: {completed.stderr.strip() or completed.stdout.strip()}"
        )
    payload = json.loads(completed.stdout)
    if isinstance(payload, list):
        if not payload:
            raise RuntimeError(f"concept wrapper returned no rows for {concept!r}")
        return payload[0]
    if isinstance(payload, dict) and "items" in payload and isinstance(payload["items"], list):
        return payload["items"][0]
    if isinstance(payload, dict):
        return payload
    raise RuntimeError(f"Unexpected concept wrapper payload for {concept!r}: {type(payload).__name__}")


def evaluate_concept_benchmark(
    cases: Sequence[JsonDict],
    seed: int,
    tags_path: Path,
    semantic_index_path: Path,
    runs: int = 2,
    include_soft: bool = True,
) -> JsonDict:
    modes = ["legacy"] + (["soft"] if include_soft else [])
    minimum_coverage = 0.85
    minimum_prompt_anchor = 0.5
    minimum_legacy_choice_anchor = 0.75
    minimum_soft_selected_anchor = 0.60
    minimum_soft_average_selected_anchor = 0.80
    minimum_soft_body_anchor = 0.60
    rows: List[JsonDict] = []
    by_mode: Dict[str, List[JsonDict]] = {mode: [] for mode in modes}
    for case_index, case in enumerate(cases):
        # Soft batch runs share an anchor-diversity ledger so anchor-variant
        # rotation is measured the way real multi-run batches are documented
        # to operate (the engine's repeat decay needs cross-run state).
        ledger_dir = Path(tempfile.mkdtemp(prefix="soft_ledger_"))
        soft_ledger = ledger_dir / f"case_{case_index}.json"
        for run_index in range(max(1, runs)):
            run_seed = seed + 8000 + (case_index * 100) + run_index
            for mode in modes:
                result = run_wrapper_concept(
                    concept=case["concept"],
                    concept_mode=mode,
                    seed=run_seed,
                    tags_path=tags_path,
                    semantic_index_path=semantic_index_path,
                    anchor_diversity_ledger=soft_ledger if mode == "soft" else None,
                )
                trace = result.get("semantic_trace", {}) or {}
                contract = trace.get("generation_contract", {}) or {}
                coverage_rate = coverage_preservation_rate(contract)
                prompt_rate, prompt_hits = prompt_term_rate(str(result.get("prompt_en", "")), case.get("prompt_terms", []))
                choice_rate, choice_rows = choice_anchor_rate(result, case.get("required_legacy_choices", {}) or {})
                (
                    selected_anchor_rate,
                    selected_anchor_rows,
                    body_anchor_rate,
                    body_anchor_hits,
                    body_anchor_missing,
                    soft_failures,
                    soft_anchor_detail,
                ) = soft_anchor_metrics(result)
                choice_threshold = minimum_legacy_choice_anchor if mode == "legacy" else 0.0
                if mode == "soft":
                    passed = (
                        coverage_rate >= minimum_coverage
                        and selected_anchor_rate >= minimum_soft_selected_anchor
                        and body_anchor_rate >= minimum_soft_body_anchor
                        and soft_anchor_detail["critical_anchor_match_rate"] >= 1.0
                        and soft_anchor_detail["role_anchor_match_rate"] >= 0.90
                        and soft_anchor_detail["mixin_salience_match_rate"] >= 0.80
                        and soft_anchor_detail["primary_anchor_match_rate"] >= 0.85
                        and soft_anchor_detail["anchor_group_match_rate"] >= 0.85
                        and soft_anchor_detail["visual_guard_violation_count"] == 0
                        and soft_anchor_detail["render_priority_term_rate"] >= 0.60
                        and soft_anchor_detail["required_render_priority_pass_rate"] >= 0.90
                        and soft_anchor_detail["soft_repair_success_rate"] >= 0.80
                        and soft_anchor_detail["active_denial_pass_rate"] >= 1.0
                        and soft_anchor_detail["robot_deep_structural_pass_rate"] >= 1.0
                        and soft_anchor_detail["free_slot_constraint_violation_count"] == 0
                        and soft_anchor_detail["body_first_drift_rate"] <= 0.05
                        and not soft_anchor_detail["critical_missing"]
                        and not soft_anchor_detail["source_floor_misses"]
                        and not soft_anchor_detail["anchor_group_misses"]
                    )
                    if selected_anchor_rate < minimum_soft_selected_anchor:
                        soft_failures.append("selected_anchor_rate_below_threshold")
                    if body_anchor_rate < minimum_soft_body_anchor:
                        soft_failures.append("body_anchor_term_rate_below_threshold")
                    if soft_anchor_detail["critical_anchor_match_rate"] < 1.0:
                        soft_failures.append("critical_anchor_missing")
                    if soft_anchor_detail["role_anchor_match_rate"] < 0.90:
                        soft_failures.append("role_anchor_floor_missed")
                    if soft_anchor_detail["mixin_salience_match_rate"] < 0.80:
                        soft_failures.append("mixin_salience_floor_missed")
                    if soft_anchor_detail["source_floor_misses"]:
                        soft_failures.append("source_floor_missed")
                    if soft_anchor_detail["anchor_group_misses"]:
                        soft_failures.append("anchor_group_floor_missed")
                    if soft_anchor_detail["visual_guard_violation_count"] > 0:
                        soft_failures.append("visual_guard_violation")
                    if soft_anchor_detail["primary_anchor_match_rate"] < 0.85:
                        soft_failures.append("primary_anchor_rate_below_threshold")
                    if soft_anchor_detail["render_priority_term_rate"] < 0.60:
                        soft_failures.append("render_priority_term_rate_below_threshold")
                    if soft_anchor_detail["required_render_priority_pass_rate"] < 0.90:
                        soft_failures.append("required_render_priority_rate_below_threshold")
                    if soft_anchor_detail["soft_repair_success_rate"] < 0.80:
                        soft_failures.append("soft_repair_failed")
                    if soft_anchor_detail["active_denial_pass_rate"] < 1.0:
                        soft_failures.append("active_denial_missing")
                    if soft_anchor_detail["robot_deep_structural_pass_rate"] < 1.0:
                        soft_failures.append("robot_deep_structural_missing")
                    if soft_anchor_detail["free_slot_constraint_violation_count"] > 0:
                        soft_failures.append("free_slot_constraint_violation")
                    if soft_anchor_detail["body_first_drift_rate"] > 0.05:
                        soft_failures.append("body_first_framing_present")
                else:
                    passed = (
                        coverage_rate >= minimum_coverage
                        and prompt_rate >= minimum_prompt_anchor
                        and choice_rate >= choice_threshold
                    )
                row = {
                    "name": case.get("name", case["concept"]),
                    "concept": case["concept"],
                    "concept_mode": mode,
                    "seed": run_seed,
                    "preset_id": result.get("preset_id"),
                    "coverage_rate": round(coverage_rate, 4),
                    "minimum_coverage_rate": minimum_coverage,
                    "prompt_anchor_rate": round(prompt_rate, 4),
                    "minimum_prompt_anchor_rate": minimum_prompt_anchor,
                    "prompt_anchor_hits": prompt_hits,
                    "choice_anchor_rate": round(choice_rate, 4),
                    "minimum_choice_anchor_rate": choice_threshold,
                    "choice_anchors": choice_rows,
                    "selected_anchor_rate": round(selected_anchor_rate, 4),
                    "minimum_selected_anchor_rate": minimum_soft_selected_anchor if mode == "soft" else 0.0,
                    "selected_anchors": selected_anchor_rows,
                    "body_anchor_term_rate": round(body_anchor_rate, 4),
                    "minimum_body_anchor_term_rate": minimum_soft_body_anchor if mode == "soft" else 0.0,
                    "body_anchor_hits": body_anchor_hits,
                    "body_anchor_missing": body_anchor_missing,
                    "critical_anchor_match_rate": round(soft_anchor_detail["critical_anchor_match_rate"], 4),
                    "role_anchor_match_rate": round(soft_anchor_detail["role_anchor_match_rate"], 4),
                    "mixin_salience_match_rate": round(soft_anchor_detail["mixin_salience_match_rate"], 4),
                    "primary_anchor_match_rate": round(soft_anchor_detail["primary_anchor_match_rate"], 4),
                    "anchor_group_match_rate": round(soft_anchor_detail["anchor_group_match_rate"], 4),
                    "visual_guard_violation_count": soft_anchor_detail["visual_guard_violation_count"],
                    "render_priority_term_rate": round(soft_anchor_detail["render_priority_term_rate"], 4),
                    "required_render_priority_pass_rate": round(soft_anchor_detail["required_render_priority_pass_rate"], 4),
                    "soft_repair_success_rate": round(soft_anchor_detail["soft_repair_success_rate"], 4),
                    "active_denial_pass_rate": round(soft_anchor_detail["active_denial_pass_rate"], 4),
                    "robot_deep_structural_pass_rate": round(soft_anchor_detail["robot_deep_structural_pass_rate"], 4),
                    "free_slot_constraint_violation_count": soft_anchor_detail["free_slot_constraint_violation_count"],
                    "body_first_drift_rate": round(soft_anchor_detail["body_first_drift_rate"], 4),
                    "critical_term_missing": soft_anchor_detail["critical_term_missing"],
                    "critical_anchor_missing": soft_anchor_detail["critical_missing"],
                    "source_floor_misses": soft_anchor_detail["source_floor_misses"],
                    "anchor_group_misses": soft_anchor_detail["anchor_group_misses"],
                    "soft_anchor_failure_reasons": sorted(set(soft_failures)),
                    "anchor_variants": selected_anchor_variants(result),
                    "coverage_gaps": contract.get("coverage_gaps", []),
                    "render_suppressed_slots": contract.get("render_suppressed_slots", []),
                    "passed": passed,
                }
                rows.append(row)
                by_mode[mode].append(row)
    mode_summaries: List[JsonDict] = []
    for mode, mode_rows in by_mode.items():
        variant_diversity = anchor_variant_diversity(mode_rows) if mode == "soft" else {}
        mode_summaries.append(
            {
                "concept_mode": mode,
                "run_count": len(mode_rows),
                "average_coverage_rate": round(
                    sum(row["coverage_rate"] for row in mode_rows) / max(len(mode_rows), 1),
                    4,
                ),
                "average_prompt_anchor_rate": round(
                    sum(row["prompt_anchor_rate"] for row in mode_rows) / max(len(mode_rows), 1),
                    4,
                ),
                "average_choice_anchor_rate": round(
                    sum(row["choice_anchor_rate"] for row in mode_rows) / max(len(mode_rows), 1),
                    4,
                ),
                "average_selected_anchor_rate": round(
                    sum(row["selected_anchor_rate"] for row in mode_rows) / max(len(mode_rows), 1),
                    4,
                ),
                "average_body_anchor_term_rate": round(
                    sum(row["body_anchor_term_rate"] for row in mode_rows) / max(len(mode_rows), 1),
                    4,
                ),
                "average_body_first_drift_rate": round(
                    sum(row.get("body_first_drift_rate", 0.0) for row in mode_rows) / max(len(mode_rows), 1),
                    4,
                ),
                "average_required_render_priority_pass_rate": round(
                    sum(row.get("required_render_priority_pass_rate", 1.0) for row in mode_rows) / max(len(mode_rows), 1),
                    4,
                ),
                "average_soft_repair_success_rate": round(
                    sum(row.get("soft_repair_success_rate", 1.0) for row in mode_rows) / max(len(mode_rows), 1),
                    4,
                ),
                "average_active_denial_pass_rate": round(
                    sum(row.get("active_denial_pass_rate", 1.0) for row in mode_rows) / max(len(mode_rows), 1),
                    4,
                ),
                "average_robot_deep_structural_pass_rate": round(
                    sum(row.get("robot_deep_structural_pass_rate", 1.0) for row in mode_rows) / max(len(mode_rows), 1),
                    4,
                ),
                "free_slot_constraint_violation_count": sum(row.get("free_slot_constraint_violation_count", 0) for row in mode_rows),
                **variant_diversity,
                "failed_run_count": sum(1 for row in mode_rows if not row["passed"]),
            }
        )
    legacy_summary = next((item for item in mode_summaries if item["concept_mode"] == "legacy"), {})
    soft_summary = next((item for item in mode_summaries if item["concept_mode"] == "soft"), None)
    soft_coverage_drop = None
    soft_promotion_ready = None
    if soft_summary:
        soft_coverage_drop = round(
            float(legacy_summary.get("average_coverage_rate", 0.0))
            - float(soft_summary.get("average_coverage_rate", 0.0)),
            4,
        )
        soft_promotion_ready = (
            soft_summary["average_coverage_rate"] >= minimum_coverage
            and soft_summary["average_selected_anchor_rate"] >= minimum_soft_average_selected_anchor
            and soft_summary["average_body_anchor_term_rate"] >= minimum_soft_body_anchor
            and soft_summary.get("average_body_first_drift_rate", 0.0) <= 0.05
            and soft_summary.get("average_required_render_priority_pass_rate", 1.0) >= 0.90
            and soft_summary.get("average_soft_repair_success_rate", 1.0) >= 0.80
            and soft_summary.get("average_active_denial_pass_rate", 1.0) >= 1.0
            and soft_summary.get("average_robot_deep_structural_pass_rate", 1.0) >= 1.0
            and soft_summary.get("free_slot_constraint_violation_count", 0) == 0
            and soft_summary.get("anchor_variant_diversity_rate", 1.0) >= 0.70
            and soft_coverage_drop <= 0.05
            and soft_summary["failed_run_count"] == 0
        )
    return {
        "case_count": len(cases),
        "runs_per_case": max(1, runs),
        "minimum_coverage_rate": minimum_coverage,
        "minimum_prompt_anchor_rate": minimum_prompt_anchor,
        "minimum_legacy_choice_anchor_rate": minimum_legacy_choice_anchor,
        "minimum_soft_selected_anchor_rate": minimum_soft_selected_anchor,
        "minimum_soft_average_selected_anchor_rate": minimum_soft_average_selected_anchor,
        "minimum_soft_body_anchor_term_rate": minimum_soft_body_anchor,
        "mode_summaries": mode_summaries,
        "legacy_failed_run_count": int(legacy_summary.get("failed_run_count", 0)),
        "soft_coverage_drop": soft_coverage_drop,
        "soft_promotion_ready": soft_promotion_ready,
        "results": rows,
    }


BEASTKIN_ROLE_SCENE_EXPECTATIONS: Dict[str, Set[str]] = {
    "경찰": {"traffic_crossing_rain", "city_intersection_night", "lost_child_service_desk"},
    "사복 여친": {"quiet_cafe", "campus_cafe", "cozy_apartment", "creator_room", "city_bridge", "urban_concrete_stairs"},
    "바니걸": {"backstage_room", "stage_magic_backstage", "backstage_vanity_corner", "costume_workshop_backstage"},
    "고스로리": {"gothic_glass_curio_cabinet", "gothic_candle_studio", "victorian_mansion_parlor"},
    "공주": {
        "throne_hall_interior",
        "grand_ballroom_chandelier",
        "royal_princess_chamber",
        "hanfu_court_garden",
        "joseon_palace_interior",
        "hanok_inner_court",
        "palace_ceremonial_courtyard",
        "palace_garden_modern",
        "palace_side_gate",
        "royal_guard_corridor",
        "royal_ancestral_shrine",
        "ballroom_gala_floor",
        "ruined_palace_wing",
    },
}


def evaluate_beastkin_role_matrix_gate(recipes_path: Path = DEFAULT_CONCEPT_RECIPES) -> JsonDict:
    try:
        recipes = json.loads(recipes_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"passed": False, "failures": [{"check": "load_recipes", "reason": str(exc)}]}

    failures: List[JsonDict] = []
    mixin = (recipes.get("mixins") or {}).get("수인") or {}
    if mixin.get("preset") == "beastkin_threshold_portrait":
        failures.append({"check": "beastkin_mixin_preset", "reason": "수인 mixin still locks beastkin_threshold_portrait"})
    set_values = mixin.get("set") if isinstance(mixin.get("set"), dict) else {}
    if set_values.get("mood") == "weathered_endurance":
        failures.append({"check": "beastkin_mixin_mood", "reason": "수인 mixin still locks weathered_endurance"})

    roles = recipes.get("roles") or {}
    for role, expected_locations in BEASTKIN_ROLE_SCENE_EXPECTATIONS.items():
        recipe = roles.get(role) or {}
        policy = recipe.get("role_scene_policy") if isinstance(recipe.get("role_scene_policy"), dict) else {}
        allowed = set(str(item) for item in policy.get("allowed_locations") or [])
        forbidden = set(str(item) for item in policy.get("forbidden_locations") or [])
        preset_affinity = recipe.get("preset_affinity") if isinstance(recipe.get("preset_affinity"), dict) else {}
        discouraged = set(str(item) for item in preset_affinity.get("discouraged_presets") or [])
        if not policy.get("enabled"):
            failures.append({"check": "role_scene_policy", "role": role, "reason": "policy disabled or missing"})
        if policy.get("enforce") is not True:
            failures.append({"check": "role_scene_policy", "role": role, "reason": "policy must enforce role-compatible locations"})
        if allowed != expected_locations:
            failures.append(
                {
                    "check": "role_scene_locations",
                    "role": role,
                    "expected": sorted(expected_locations),
                    "actual": sorted(allowed),
                }
            )
        if "highland_pasture" not in forbidden:
            failures.append({"check": "role_scene_forbidden", "role": role, "reason": "highland_pasture not forbidden"})
        if "beastkin_threshold_portrait" not in discouraged:
            failures.append({"check": "role_preset_affinity", "role": role, "reason": "beastkin_threshold_portrait not discouraged"})

    return {
        "passed": not failures,
        "checked_roles": sorted(BEASTKIN_ROLE_SCENE_EXPECTATIONS),
        "failures": failures,
    }


def evaluate_diversity_check(
    data: JsonDict,
    cases: Sequence[JsonDict],
    seed: int,
    semantic_index: JsonDict,
    gemini_api_key: str | None = None,
) -> JsonDict:
    results: List[JsonDict] = []
    for case_index, case in enumerate(cases):
        runs = int(case.get("runs", 10))
        free_slots = list(case.get("free_slots", []))
        rows: List[JsonDict] = []
        batch_context = make_batch_context("semantic", "high", runs)
        rng = random.Random(seed + 6000 + (case_index * 100))
        for run_index in range(runs):
            set_batch_index(batch_context, run_index)
            result = generate_once(
                data=data,
                rng=rng,
                preset_id=case.get("preset"),
                langs=["en"],
                include_negative=False,
                negative_count=12,
                include_choices=True,
                detail_level="detailed",
                intent=case["intent"],
                selection_mode="semantic",
                novelty="high",
                include_trace=True,
                semantic_index=semantic_index,
                gemini_api_key=gemini_api_key,
                batch_context=batch_context,
                batch_index=run_index,
            )
            trace = result.get("semantic_trace", {}) or {}
            contract = trace.get("generation_contract", {}) or {}
            choices = choice_ids(result)
            rows.append(
                {
                    "run_index": run_index,
                    "preset_id": result.get("preset_id"),
                    "choices": {slot: choices.get(slot) for slot in free_slots if choices.get(slot)},
                    "preservation_rate": round(coverage_preservation_rate(contract), 4),
                    "render_suppressed_count": len(contract.get("render_suppressed_slots", []) or []),
                    "coverage_gaps": contract.get("coverage_gaps", []),
                }
            )
        slot_metrics: Dict[str, JsonDict] = {}
        for slot in free_slots:
            values = [row["choices"].get(slot, "") for row in rows if row["choices"].get(slot)]
            counts = Counter(values)
            top_count = max(counts.values(), default=0)
            slot_metrics[slot] = {
                "observed": len(values),
                "unique": len(counts),
                "entropy": round(shannon_entropy(values), 4),
                "top1_dominance": round(top_count / max(len(values), 1), 4),
                "top": counts.most_common(5),
            }
        preservation_rate = round(sum(row["preservation_rate"] for row in rows) / max(len(rows), 1), 4)
        render_suppression_rate = round(
            sum(1 for row in rows if row["render_suppressed_count"] > 0) / max(len(rows), 1),
            4,
        )
        minimum_preservation = float(case.get("minimum_preservation_rate", 0.9))
        maximum_top1 = float(case.get("maximum_top1_dominance", 0.75))
        minimum_unique = int(case.get("minimum_unique_per_slot", 2))
        maximum_suppression = float(case.get("maximum_render_suppression_rate", 0.25))
        checked_slots = [slot for slot, metrics in slot_metrics.items() if metrics["observed"] >= 3]
        diversity_passed = all(
            slot_metrics[slot]["unique"] >= minimum_unique
            and slot_metrics[slot]["top1_dominance"] <= maximum_top1
            for slot in checked_slots
        )
        passed = (
            preservation_rate >= minimum_preservation
            and render_suppression_rate <= maximum_suppression
            and diversity_passed
        )
        results.append(
            {
                "name": case.get("name", case["intent"]),
                "intent": case["intent"],
                "runs": runs,
                "preservation_rate": preservation_rate,
                "minimum_preservation_rate": minimum_preservation,
                "render_suppression_rate": render_suppression_rate,
                "maximum_render_suppression_rate": maximum_suppression,
                "slot_metrics": slot_metrics,
                "checked_slots": checked_slots,
                "passed": passed,
                "results": rows,
            }
        )
    beastkin_role_matrix = evaluate_beastkin_role_matrix_gate()
    diversity_failed = sum(1 for item in results if not item["passed"])
    return {
        "case_count": len(results),
        "failed_case_count": diversity_failed + (0 if beastkin_role_matrix["passed"] else 1),
        "beastkin_role_matrix": beastkin_role_matrix,
        "results": results,
    }


def evaluate_mode(
    data: JsonDict,
    mode: str,
    cases: Sequence[JsonDict],
    seed: int,
    semantic_index: JsonDict | None,
    gemini_api_key: str | None = None,
) -> JsonDict:
    results = []
    for index, case in enumerate(cases):
        result = generate_once(
            data=data,
            rng=random.Random(seed + index),
            preset_id=None,
            langs=["en"],
            include_negative=False,
            negative_count=12,
            include_choices=True,
            detail_level="detailed",
            intent=case["intent"] if mode != "rule" else None,
            selection_mode=mode,
            novelty="medium",
            include_trace=True,
            semantic_index=semantic_index if mode != "rule" else None,
            gemini_api_key=gemini_api_key if mode != "rule" else None,
        )
        results.append(
            {
                "intent": case["intent"],
                "preset_id": result.get("preset_id"),
                "coverage": coverage(result, case),
                "forbidden_hits": forbidden_hits(result, case),
                "quality_verdict": (result.get("quality", {}) or {}).get("verdict"),
                "choices": choice_ids(result),
            }
        )
    return {
        "mode": mode,
        "average_coverage": round(sum(item["coverage"] for item in results) / max(len(results), 1), 4),
        "forbidden_case_count": sum(1 for item in results if item["forbidden_hits"]),
        "quality_fail_count": sum(1 for item in results if item.get("quality_verdict") == "fail"),
        "unique_presets": len({item["preset_id"] for item in results}),
        "results": results,
    }


def evaluate_preset_guards(
    data: JsonDict,
    cases: Sequence[JsonDict],
    seed: int,
    semantic_index: JsonDict,
    gemini_api_key: str | None = None,
) -> JsonDict:
    results = []
    for index, case in enumerate(cases):
        result = generate_once(
            data=data,
            rng=random.Random(seed + 1000 + index),
            preset_id=None,
            langs=["en"],
            include_negative=False,
            negative_count=12,
            include_choices=True,
            detail_level="detailed",
            intent=case["intent"],
            selection_mode="semantic",
            novelty="medium",
            include_trace=True,
            semantic_index=semantic_index,
            gemini_api_key=gemini_api_key,
        )
        selected = result.get("preset_id")
        blacklisted = set(case.get("blacklisted_presets", []))
        results.append(
            {
                "intent": case["intent"],
                "preset_id": selected,
                "blacklisted": selected in blacklisted,
                "blacklisted_presets": sorted(blacklisted),
                "intent_axes": result.get("semantic_trace", {}).get("preset_score", {}).get("intent_axes"),
            }
        )
    return {
        "case_count": len(results),
        "blacklisted_case_count": sum(1 for item in results if item["blacklisted"]),
        "results": results,
    }


def evaluate_multi_axis_coverage(
    data: JsonDict,
    cases: Sequence[JsonDict],
    seed: int,
    semantic_index: JsonDict,
    gemini_api_key: str | None = None,
) -> JsonDict:
    results = []
    for case_index, case in enumerate(cases):
        runs = int(case.get("runs", 10))
        rows = []
        rng = random.Random(seed + 2000 + (case_index * 100))
        batch_context = make_batch_context("semantic", "medium", runs)
        for run_index in range(runs):
            set_batch_index(batch_context, run_index)
            result = generate_once(
                data=data,
                rng=rng,
                preset_id=None,
                langs=["en"],
                include_negative=False,
                negative_count=12,
                include_choices=True,
                detail_level="detailed",
                intent=case["intent"],
                selection_mode="semantic",
                novelty="medium",
                include_trace=True,
                semantic_index=semantic_index,
                gemini_api_key=gemini_api_key,
                batch_context=batch_context,
                batch_index=run_index,
            )
            coverage = {
                "human_subject": has_human_subject(result),
                "urban_location": has_urban_location(result),
                "horror_atmosphere": has_horror_atmosphere(result),
                "surreal_layer": has_surreal_layer(result),
            }
            strong_horror = has_strong_horror_signal(data, result)
            weak_only_horror = has_weak_only_horror_signal(data, result)
            horror_diluting_lighting = has_horror_diluting_lighting(data, result)
            groups = sorted(subject_groups(data, result))
            tones = sorted(location_tones(data, result))
            warm_location_horror_conflict = has_warm_location_horror_conflict(data, result)
            fantasy_axis_coverage = has_fantasy_axis_coverage(data, result)
            rows.append(
                {
                    "preset_id": result.get("preset_id"),
                    "subject": choice_payload(result, "subject").get("id"),
                    "subject_groups": groups,
                    "location": choice_payload(result, "location").get("id"),
                    "location_tones": tones,
                    "mood": choice_payload(result, "mood").get("id"),
                    "lighting": choice_payload(result, "lighting").get("id"),
                    "color": choice_payload(result, "color").get("id"),
                    "surreal_concept": choice_payload(result, "surreal_concept").get("id"),
                    "coverage": coverage,
                    "strong_horror": strong_horror,
                    "weak_only_horror": weak_only_horror,
                    "horror_diluting_lighting": horror_diluting_lighting,
                    "warm_location_horror_conflict": warm_location_horror_conflict,
                    "fantasy_axis_coverage": fantasy_axis_coverage,
                    "horror_preset_signal": preset_has_horror_strength(data, result.get("preset_id")),
                    "horror_terms": sorted(horror_terms_in_result(result)),
                }
            )
        category_rates = {
            key: round(sum(1 for row in rows if row["coverage"][key]) / max(len(rows), 1), 4)
            for key in ("human_subject", "urban_location", "horror_atmosphere", "surreal_layer")
        }
        unique_subjects = len({row.get("subject") for row in rows if row.get("subject")})
        unique_presets = len({row.get("preset_id") for row in rows if row.get("preset_id")})
        unique_locations = len({row.get("location") for row in rows if row.get("location")})
        unique_subject_groups = len({group for row in rows for group in row.get("subject_groups", [])})
        unique_lighting = len({row.get("lighting") for row in rows if row.get("lighting")})
        unique_moods = len({row.get("mood") for row in rows if row.get("mood")})
        unique_surreal_concepts = len({row.get("surreal_concept") for row in rows if row.get("surreal_concept")})
        unique_horror_terms = sorted({term for row in rows for term in row.get("horror_terms", [])})
        strong_horror_rate = round(sum(1 for row in rows if row.get("strong_horror")) / max(len(rows), 1), 4)
        weak_only_horror_rate = round(sum(1 for row in rows if row.get("weak_only_horror")) / max(len(rows), 1), 4)
        horror_diluting_lighting_rate = round(sum(1 for row in rows if row.get("horror_diluting_lighting")) / max(len(rows), 1), 4)
        warm_location_horror_conflict_rate = round(sum(1 for row in rows if row.get("warm_location_horror_conflict")) / max(len(rows), 1), 4)
        fantasy_axis_coverage_rate = round(sum(1 for row in rows if row.get("fantasy_axis_coverage")) / max(len(rows), 1), 4)
        horror_preset_signal_rate = round(sum(1 for row in rows if row.get("horror_preset_signal")) / max(len(rows), 1), 4)
        minimum_subjects = int(case.get("minimum_subject_diversity", 1))
        minimum_presets = int(case.get("minimum_preset_diversity", 1))
        minimum_locations = int(case.get("minimum_location_diversity", 1))
        minimum_moods = int(case.get("minimum_mood_diversity", 1))
        minimum_surreal = int(case.get("minimum_surreal_concept_diversity", 1))
        minimum_subject_groups = int(case.get("minimum_subject_group_diversity", 1))
        minimum_lighting = int(case.get("minimum_lighting_diversity", 1))
        minimum_strong_horror_rate = float(case.get("minimum_strong_horror_rate", 0.0))
        maximum_weak_only_horror_rate = float(case.get("maximum_weak_only_horror_rate", 1.0))
        maximum_horror_diluting_lighting_rate = float(case.get("maximum_horror_diluting_lighting_rate", 1.0))
        maximum_warm_location_horror_conflict_rate = float(case.get("maximum_warm_location_horror_conflict_rate", 1.0))
        minimum_fantasy_axis_coverage_rate = float(case.get("minimum_fantasy_axis_coverage_rate", 0.0))
        results.append(
            {
                "intent": case["intent"],
                "runs": runs,
                "category_rates": category_rates,
                "strong_horror_rate": strong_horror_rate,
                "weak_only_horror_rate": weak_only_horror_rate,
                "horror_diluting_lighting_rate": horror_diluting_lighting_rate,
                "warm_location_horror_conflict_rate": warm_location_horror_conflict_rate,
                "fantasy_axis_coverage_rate": fantasy_axis_coverage_rate,
                "horror_preset_signal_rate": horror_preset_signal_rate,
                "unique_subjects": unique_subjects,
                "unique_subject_groups": unique_subject_groups,
                "unique_presets": unique_presets,
                "unique_locations": unique_locations,
                "unique_lighting": unique_lighting,
                "unique_moods": unique_moods,
                "unique_surreal_concepts": unique_surreal_concepts,
                "unique_horror_terms": len(unique_horror_terms),
                "horror_terms": unique_horror_terms,
                "minimum_subject_diversity": minimum_subjects,
                "minimum_subject_group_diversity": minimum_subject_groups,
                "minimum_preset_diversity": minimum_presets,
                "minimum_location_diversity": minimum_locations,
                "minimum_lighting_diversity": minimum_lighting,
                "minimum_mood_diversity": minimum_moods,
                "minimum_surreal_concept_diversity": minimum_surreal,
                "minimum_strong_horror_rate": minimum_strong_horror_rate,
                "maximum_weak_only_horror_rate": maximum_weak_only_horror_rate,
                "maximum_horror_diluting_lighting_rate": maximum_horror_diluting_lighting_rate,
                "maximum_warm_location_horror_conflict_rate": maximum_warm_location_horror_conflict_rate,
                "minimum_fantasy_axis_coverage_rate": minimum_fantasy_axis_coverage_rate,
                "passed": all(rate >= 0.9 for rate in category_rates.values())
                and unique_subjects >= minimum_subjects
                and unique_subject_groups >= minimum_subject_groups
                and unique_presets >= minimum_presets
                and unique_locations >= minimum_locations
                and unique_lighting >= minimum_lighting
                and unique_moods >= minimum_moods
                and unique_surreal_concepts >= minimum_surreal
                and strong_horror_rate >= minimum_strong_horror_rate
                and weak_only_horror_rate <= maximum_weak_only_horror_rate
                and horror_diluting_lighting_rate <= maximum_horror_diluting_lighting_rate
                and warm_location_horror_conflict_rate <= maximum_warm_location_horror_conflict_rate
                and fantasy_axis_coverage_rate >= minimum_fantasy_axis_coverage_rate,
                "results": rows,
            }
        )
    return {
        "case_count": len(results),
        "failed_case_count": sum(1 for item in results if not item["passed"]),
        "results": results,
    }


def picked_entries_from_choices(data: JsonDict, choices: Dict[str, str]) -> Dict[str, JsonDict]:
    picked: Dict[str, JsonDict] = {}
    for slot, entry_id in choices.items():
        entry = dictionary_entry(data, slot, entry_id)
        if entry:
            picked[slot] = entry
    return picked


def declared_rule_violations_in_result(data: JsonDict, choices: Dict[str, str]) -> List[JsonDict]:
    picked = picked_entries_from_choices(data, choices)
    violations: List[JsonDict] = []
    context_rules = [
        rule
        for rule in slot_context_rules_from_source(data)
        if str(rule.get("severity", "hard")) == "hard"
    ]
    for slot, entry in picked.items():
        others = {other: picked[other] for other in picked if other != slot}
        for violation in slot_conflict_violations(slot, entry, others, data, "hard"):
            violations.append({"type": "slot_conflict", **violation})
        if context_rules:
            context = picked_context_tokens(others)
            scene_context = picked_scene_context_tokens(others)
            for rule in context_rules:
                if slot_context_rule_violation(rule, slot, entry, context, scene_context):
                    violations.append(
                        {
                            "type": "slot_context_rule",
                            "rule_id": str(rule.get("id") or ""),
                            "slot": slot,
                            "item_id": str(entry.get("id", "")),
                        }
                    )
    return violations


def evaluate_contradiction_check(
    data: JsonDict,
    seed: int,
    runs: int,
    preset_limit: int = 0,
) -> JsonDict:
    presets = [str(preset.get("id")) for preset in data.get("presets", [])]
    if preset_limit:
        presets = presets[:preset_limit]
    rows: List[JsonDict] = []
    generated = 0
    for preset_index, preset_id in enumerate(presets):
        for offset in range(max(1, runs)):
            rng = random.Random(seed + preset_index * 1000 + offset)
            result = generate_once(
                data=data,
                rng=rng,
                preset_id=preset_id,
                langs=["en"],
                include_negative=False,
                negative_count=0,
                include_choices=True,
                detail_level="detailed",
                selection_mode="rule",
            )
            generated += 1
            choices = {
                slot: str(entry_id)
                for slot, entry_id in (result.get("choices") or {}).items()
                if entry_id
            }
            violations = declared_rule_violations_in_result(data, choices)
            if violations:
                rows.append(
                    {
                        "preset": preset_id,
                        "seed_offset": offset,
                        "violations": violations,
                    }
                )
    return {
        "preset_count": len(presets),
        "runs_per_preset": max(1, runs),
        "generated": generated,
        "violation_count": sum(len(row["violations"]) for row in rows),
        "violations": rows,
        "declared_slot_conflicts": len(
            [
                rule
                for rule in (data.get("coherence_rules", {}) or {}).get("slot_conflicts", [])
                if isinstance(rule, dict)
            ]
        ),
        "declared_slot_context_rules": len(slot_context_rules_from_source(data)),
    }


def evaluate_candidate_pack_coverage(tags_path: Path, seed: int, cases: Sequence[JsonDict]) -> JsonDict:
    rows: List[JsonDict] = []
    for index, case in enumerate(cases):
        cmd = [
            sys.executable,
            str(WRAPPER_PATH),
            "--tags",
            str(tags_path),
            "--concept",
            str(case["concept"]),
            "--selection-mode",
            str(case.get("selection_mode") or "rule"),
            "--seed",
            str(seed + index),
            "--emit-candidate-pack",
        ]
        result = subprocess.run(
            cmd,
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        row: JsonDict = {
            "name": case.get("name"),
            "concept": case.get("concept"),
            "returncode": result.returncode,
            "passed": False,
            "failures": [],
        }
        if result.returncode != 0:
            row["failures"].append("wrapper_failed")
            row["stderr"] = result.stderr.strip()
            rows.append(row)
            continue
        try:
            payload = json.loads(result.stdout)
            pack = payload[0]
        except Exception as exc:
            row["failures"].append("invalid_candidate_pack_json")
            row["error"] = str(exc)
            rows.append(row)
            continue
        mandatory = {str(item.get("text")) for item in pack.get("mandatory_intents", []) if isinstance(item, dict)}
        uncovered = {str(item.get("text")) for item in pack.get("uncovered_intents", []) if isinstance(item, dict)}
        required = set(normalize_list(case.get("required_intents")))
        expected_uncovered = set(normalize_list(case.get("expected_uncovered")))
        missing = sorted(required - mandatory)
        missing_uncovered = sorted(expected_uncovered - uncovered)
        if missing:
            row["failures"].append("missing_mandatory_intents")
        if missing_uncovered:
            row["failures"].append("missing_expected_uncovered_intents")
        if "prompt_en" in pack:
            row["failures"].append("candidate_pack_contains_final_prompt")
        required_pack_fields = {
            "concept_axes",
            "motif_budget",
            "preset_reference",
            "masked_buckets",
            "open_slots",
            "template_echo_risk",
        }
        missing_pack_fields = sorted(required_pack_fields - set(pack.keys()))
        if missing_pack_fields:
            row["failures"].append("missing_scaffold_fields")
            row["missing_scaffold_fields"] = missing_pack_fields
        concept_axes = pack.get("concept_axes") if isinstance(pack.get("concept_axes"), dict) else {}
        axis_ids = {
            str(axis.get("id"))
            for axis in concept_axes.get("required", []) or []
            if isinstance(axis, dict) and axis.get("id")
        }
        required_axes = set(normalize_list(case.get("required_identity_axes")))
        missing_axes = sorted(required_axes - axis_ids)
        if missing_axes:
            row["failures"].append("missing_identity_axes")
            row["missing_identity_axes"] = missing_axes
        motif_budget = pack.get("motif_budget") if isinstance(pack.get("motif_budget"), dict) else {}
        quotas = motif_budget.get("quotas") if isinstance(motif_budget.get("quotas"), dict) else {}
        required_quotas = set(normalize_list(case.get("required_motif_quotas")))
        missing_quotas = sorted(required_quotas - set(quotas))
        if missing_quotas:
            row["failures"].append("missing_motif_quotas")
            row["missing_motif_quotas"] = missing_quotas
        if case.get("expect_masked_buckets") and not pack.get("masked_buckets"):
            row["failures"].append("missing_masked_buckets")
        if len(pack.get("presets", []) or []) > 4:
            row["failures"].append("preset_candidate_cap_exceeded")
        total_slot_candidates = 0
        probability_failures: List[str] = []
        for slot, slot_payload in (pack.get("slots", {}) or {}).items():
            candidates = slot_payload.get("candidates", []) if isinstance(slot_payload, dict) else []
            total_slot_candidates += len(candidates)
            limit = 4 if slot_payload.get("role") == "core" else 2
            if len(candidates) > limit:
                row["failures"].append(f"slot_candidate_cap_exceeded:{slot}")
            if candidates:
                total_probability = sum(float(candidate.get("probability", 0.0)) for candidate in candidates)
                if abs(total_probability - 1.0) > 0.00001:
                    probability_failures.append(str(slot))
        if total_slot_candidates > 64:
            row["failures"].append("total_slot_candidate_cap_exceeded")
        if probability_failures:
            row["failures"].append("slot_probability_not_normalized")
            row["probability_failures"] = probability_failures
        row.update(
            {
                "pack_id": pack.get("pack_id"),
                "mandatory_intents": sorted(mandatory),
                "uncovered_intents": sorted(uncovered),
                "missing_mandatory_intents": missing,
                "missing_expected_uncovered_intents": missing_uncovered,
                "identity_axes": sorted(axis_ids),
                "masked_buckets": pack.get("masked_buckets", []),
                "motif_quotas": sorted(quotas),
                "preset_candidate_count": len(pack.get("presets", []) or []),
                "slot_candidate_count": total_slot_candidates,
            }
        )
        row["passed"] = not row["failures"]
        rows.append(row)
    return {
        "case_count": len(rows),
        "failed_case_count": sum(1 for row in rows if not row["passed"]),
        "results": rows,
    }


GENERALIZATION_CASE_KEYS = {
    "id",
    "preset",
    "concept",
    "additional_requirements",
    "expected_profile",
    "forbidden_selected_terms",
    "forbidden_candidate_terms",
    "minimum_multi_candidate_slots",
    "expected_mandatory_intents",
    "forbidden_mandatory_intents",
    "no_people",
    "expected_scene_variant",
    "expected_subject_categories",
    "expected_intent_subject_categories",
    "expected_intent_domains",
    "required_selected_any",
    "required_candidate_any",
    "forbidden_selected_slots",
    "forbidden_selected_ids",
    "minimum_intent_contract_rows",
}


def validate_generalization_case(path: Path, line_number: int, payload: JsonDict) -> None:
    unknown = set(payload) - GENERALIZATION_CASE_KEYS
    if unknown:
        raise ValueError(f"{path}:{line_number}: unknown case fields {sorted(unknown)}")
    if not str(payload.get("id") or "").strip():
        raise ValueError(f"{path}:{line_number}: each case needs an id")
    if not payload.get("preset") and not payload.get("concept"):
        raise ValueError(f"{path}:{line_number}: each case needs preset or concept")
    for key in (
        "additional_requirements",
        "forbidden_selected_terms",
        "forbidden_candidate_terms",
        "expected_mandatory_intents",
        "forbidden_mandatory_intents",
        "expected_subject_categories",
        "expected_intent_subject_categories",
        "expected_intent_domains",
        "forbidden_selected_slots",
        "forbidden_selected_ids",
    ):
        if key in payload and (not isinstance(payload.get(key), list) or any(not str(item).strip() for item in payload.get(key) or [])):
            raise ValueError(f"{path}:{line_number}: {key} must be a list of non-empty strings")
    for required_key in ("required_selected_any", "required_candidate_any"):
        required = payload.get(required_key)
        if required is None:
            continue
        if not isinstance(required, dict):
            raise ValueError(f"{path}:{line_number}: {required_key} must be an object")
        for slot, ids in required.items():
            if not str(slot).strip() or not isinstance(ids, list) or not ids or any(not str(item).strip() for item in ids):
                raise ValueError(f"{path}:{line_number}: {required_key} values must be non-empty string lists")
    expected_variant = payload.get("expected_scene_variant")
    if expected_variant is not None and not isinstance(expected_variant, (bool, str, list)):
        raise ValueError(f"{path}:{line_number}: expected_scene_variant must be a boolean, string, or list")


def load_generalization_cases(path: Path) -> List[JsonDict]:
    cases: List[JsonDict] = []
    seen_ids: Set[str] = set()
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        payload = json.loads(line)
        if not isinstance(payload, dict):
            raise ValueError(f"{path}:{line_number}: each case must be an object")
        validate_generalization_case(path, line_number, payload)
        case_id = str(payload.get("id"))
        if case_id in seen_ids:
            raise ValueError(f"{path}:{line_number}: duplicate case id {case_id}")
        seen_ids.add(case_id)
        cases.append(payload)
    if not cases:
        raise ValueError(f"{path}: at least one generalization case is required")
    return cases


def selected_candidate_rows(pack: JsonDict) -> List[JsonDict]:
    rows = [
        candidate
        for candidate in pack.get("presets", []) or []
        if isinstance(candidate, dict) and candidate.get("selected_by_sampler")
    ]
    for slot_payload in (pack.get("slots") or {}).values():
        if not isinstance(slot_payload, dict):
            continue
        rows.extend(
            candidate
            for candidate in slot_payload.get("candidates", []) or []
            if isinstance(candidate, dict) and candidate.get("selected_by_sampler")
        )
    return rows


def slot_candidate_rows(pack: JsonDict) -> List[JsonDict]:
    rows: List[JsonDict] = []
    for slot_payload in (pack.get("slots") or {}).values():
        if not isinstance(slot_payload, dict):
            continue
        rows.extend(candidate for candidate in slot_payload.get("candidates", []) or [] if isinstance(candidate, dict))
    return rows


def selected_entry_ids_by_slot(pack: JsonDict) -> Dict[str, Set[str]]:
    selected: Dict[str, Set[str]] = {}
    for candidate in selected_candidate_rows(pack):
        slot = str(candidate.get("slot") or "")
        entry_id = str(candidate.get("entry_id") or "")
        if slot and entry_id:
            selected.setdefault(slot, set()).add(entry_id)
    return selected


def candidate_reads_as_human(candidate: JsonDict) -> bool:
    tokens = {
        str(item).lower()
        for item in [*(candidate.get("kind") or []), *(candidate.get("tags") or [])]
    }
    return str(candidate.get("slot") or "") in PERSON_ONLY_CANDIDATE_SLOTS or "human" in tokens


def evaluate_atomic_scene_contract(pack: JsonDict) -> List[str]:
    failures: List[str] = []
    contract = pack.get("scene_contract") if isinstance(pack.get("scene_contract"), dict) else {}
    groups = contract.get("groups") if isinstance(contract.get("groups"), list) else []
    if not contract.get("enabled") or not groups:
        return ["missing_atomic_scene_contract"]
    for group in groups:
        if not isinstance(group, dict) or group.get("strategy") != "atomic_scene":
            failures.append("invalid_atomic_scene_group")
            continue
        for slot, slot_contract in (group.get("slots") or {}).items():
            if not isinstance(slot_contract, dict):
                failures.append(f"invalid_atomic_scene_slot:{slot}")
                continue
            allowed = {str(item) for item in slot_contract.get("allowed_entry_ids") or []}
            candidates = {str(item) for item in slot_contract.get("candidate_entry_ids") or []}
            selected = str(slot_contract.get("selected_entry_id") or "")
            if not allowed:
                failures.append(f"empty_atomic_scene_pool:{slot}")
            if candidates - allowed:
                failures.append(f"atomic_scene_candidate_leak:{slot}")
            if selected and selected not in allowed:
                failures.append(f"atomic_scene_selected_leak:{slot}")
    return failures


def evaluate_generalization_check(
    tags_path: Path,
    cases_path: Path,
    seed: int,
    limit: int = 0,
) -> JsonDict:
    data = load_json(tags_path)
    cases = load_generalization_cases(cases_path)
    if limit:
        cases = cases[:limit]
    rows: List[JsonDict] = []
    for index, case in enumerate(cases):
        cmd = [
            sys.executable,
            str(WRAPPER_PATH),
            "--tags",
            str(tags_path),
            "--selection-mode",
            "rule",
            "--seed",
            str(seed + index),
            "--emit-candidate-pack",
        ]
        if case.get("preset"):
            cmd.extend(["--preset", str(case["preset"])])
        if case.get("concept"):
            cmd.extend(["--concept", str(case["concept"])])
        for requirement in case.get("additional_requirements") or []:
            cmd.extend(["--additional-requirement", str(requirement)])
        result = subprocess.run(cmd, cwd=PROJECT_ROOT, text=True, capture_output=True, check=False)
        failures: List[str] = []
        row: JsonDict = {"id": case.get("id"), "returncode": result.returncode}
        if result.returncode != 0:
            failures.append("wrapper_failed")
            row["stderr"] = result.stderr.strip()
            row["failures"] = failures
            row["passed"] = False
            rows.append(row)
            continue
        try:
            payload = json.loads(result.stdout)
            if not isinstance(payload, list) or len(payload) != 1 or not isinstance(payload[0], dict):
                raise ValueError("expected one candidate pack")
            pack = payload[0]
        except Exception as exc:
            failures.append("invalid_pack")
            row["error"] = str(exc)
            row["failures"] = failures
            row["passed"] = False
            rows.append(row)
            continue

        safety = pack.get("safety") if isinstance(pack.get("safety"), dict) else {}
        expected_safety = {
            "mode": "automatic",
            "evaluation_requested": False,
            "status": "pass",
            "requires_user_approval": False,
            "items": [],
        }
        if safety != expected_safety:
            failures.append("default_safety_contract")
        if "approval_required_safety_transforms" in pack:
            failures.append("legacy_safety_contract_exposed")
        if pack.get("contract_version") != "photo-candidate-pack/v2":
            failures.append("candidate_pack_version")

        presets = pack.get("presets", []) or []
        slots = pack.get("slots") if isinstance(pack.get("slots"), dict) else {}
        total_candidates = sum(
            len(slot_payload.get("candidates", []) or [])
            for slot_payload in slots.values()
            if isinstance(slot_payload, dict)
        )
        if len(presets) > 4 or total_candidates > 64:
            failures.append("candidate_caps")
        if any(
            len(slot_payload.get("candidates", []) or []) > (4 if slot_payload.get("role") == "core" else 2)
            for slot_payload in slots.values()
            if isinstance(slot_payload, dict)
        ):
            failures.append("slot_candidate_caps")
        multi_candidate_slots = sum(
            1
            for slot_payload in slots.values()
            if isinstance(slot_payload, dict) and len(slot_payload.get("candidates", []) or []) >= 2
        )
        if multi_candidate_slots < int(case.get("minimum_multi_candidate_slots", 0) or 0):
            failures.append("insufficient_rule_alternatives")

        mandatory = {
            str(item.get("text") or "")
            for item in pack.get("mandatory_intents", []) or []
            if isinstance(item, dict)
        }
        for expected in case.get("expected_mandatory_intents") or []:
            if str(expected) not in mandatory:
                failures.append(f"missing_mandatory_intent:{expected}")
        for forbidden in case.get("forbidden_mandatory_intents") or []:
            if str(forbidden) in mandatory:
                failures.append(f"forbidden_mandatory_intent:{forbidden}")

        selected = selected_candidate_rows(pack)
        selected_by_slot = selected_entry_ids_by_slot(pack)
        all_slot_candidates = slot_candidate_rows(pack)
        selected_blob = json.dumps(selected, ensure_ascii=False).lower()
        for term in case.get("forbidden_selected_terms") or []:
            if str(term).lower() in selected_blob:
                failures.append(f"implicit_theme_selected:{term}")
        if case.get("no_people"):
            intent_constraints = ((pack.get("coverage") or {}).get("intent_constraints") or {})
            if not isinstance(intent_constraints, dict) or not intent_constraints.get("no_people"):
                failures.append("missing_negative_person_constraint")
            if any(candidate_reads_as_human(candidate) for candidate in selected):
                failures.append("negative_person_constraint_inverted")
            if any(candidate_reads_as_human(candidate) for candidate in all_slot_candidates):
                failures.append("negative_person_candidate_exposed")

        ineligible_candidates = [
            str(candidate.get("id") or "")
            for candidate in all_slot_candidates
            if not isinstance(candidate.get("applicability"), dict)
            or candidate.get("applicability", {}).get("status") != "eligible"
            or candidate.get("applicability", {}).get("source") != "sampler_eligible_pool"
        ]
        if ineligible_candidates:
            failures.append("candidate_pool_not_sampler_exact")

        candidate_blob = json.dumps(all_slot_candidates, ensure_ascii=False).lower()
        for term in case.get("forbidden_candidate_terms") or []:
            if str(term).lower() in candidate_blob:
                failures.append(f"forbidden_candidate_exposed:{term}")

        forbidden_ids = {str(item) for item in case.get("forbidden_selected_ids") or []}
        actual_selected_ids = {entry_id for ids in selected_by_slot.values() for entry_id in ids}
        for entry_id in sorted(forbidden_ids & actual_selected_ids):
            failures.append(f"forbidden_selected_id:{entry_id}")
        for slot in case.get("forbidden_selected_slots") or []:
            if selected_by_slot.get(str(slot)):
                failures.append(f"forbidden_selected_slot:{slot}")
        required_selected_any = case.get("required_selected_any") or {}
        if isinstance(required_selected_any, dict):
            for slot, expected_ids in required_selected_any.items():
                allowed = {str(item) for item in expected_ids or []}
                if allowed and not (selected_by_slot.get(str(slot), set()) & allowed):
                    failures.append(f"missing_required_selected:{slot}")
        candidate_ids_by_slot: Dict[str, Set[str]] = {}
        for candidate in all_slot_candidates:
            slot = str(candidate.get("slot") or "")
            entry_id = str(candidate.get("entry_id") or "")
            if slot and entry_id:
                candidate_ids_by_slot.setdefault(slot, set()).add(entry_id)
        required_candidate_any = case.get("required_candidate_any") or {}
        if isinstance(required_candidate_any, dict):
            for slot, expected_ids in required_candidate_any.items():
                required_ids = {str(item) for item in expected_ids or []}
                if required_ids and not (candidate_ids_by_slot.get(str(slot), set()) & required_ids):
                    failures.append(f"missing_required_candidate:{slot}")

        expected_subject_categories = {str(item) for item in case.get("expected_subject_categories") or []}
        if expected_subject_categories:
            subject_entries = {
                str(entry.get("id") or ""): entry
                for entry in data.get("slots", {}).get("subject", []) or []
                if isinstance(entry, dict)
            }
            actual_categories = {
                subject_category({"subject": subject_entries[entry_id]}, data)
                for entry_id in selected_by_slot.get("subject", set())
                if entry_id in subject_entries
            }
            if not (actual_categories & expected_subject_categories):
                failures.append("subject_category_mismatch")

        intent_constraints = ((pack.get("coverage") or {}).get("intent_constraints") or {})
        expected_intent_categories = {str(item) for item in case.get("expected_intent_subject_categories") or []}
        actual_intent_categories = {str(item) for item in (intent_constraints.get("subject_categories") or [])} if isinstance(intent_constraints, dict) else set()
        if expected_intent_categories and not expected_intent_categories.issubset(actual_intent_categories):
            failures.append("intent_subject_category_mismatch")
        expected_intent_domains = {str(item) for item in case.get("expected_intent_domains") or []}
        actual_intent_domains = {str(item) for item in (intent_constraints.get("domains") or [])} if isinstance(intent_constraints, dict) else set()
        if expected_intent_domains and not expected_intent_domains.issubset(actual_intent_domains):
            failures.append("intent_domain_mismatch")

        minimum_intent_rows = int(case.get("minimum_intent_contract_rows", 1 if case.get("additional_requirements") else 0) or 0)
        if len(pack.get("intent_contract") or []) < minimum_intent_rows:
            failures.append("intent_contract_missing")

        expected_profile = str(case.get("expected_profile") or "")
        actual_profile = str((pack.get("quality_profile") or {}).get("profile_id") or "")
        if expected_profile and actual_profile != expected_profile:
            failures.append("quality_profile_mismatch")
        expected_scene_variant = case.get("expected_scene_variant")
        if expected_scene_variant:
            actual_variants = {str(item) for item in (pack.get("provenance") or {}).get("concept_scene_variants", [])}
            if not actual_variants:
                failures.append("missing_scene_variant_provenance")
            elif isinstance(expected_scene_variant, str) and expected_scene_variant not in actual_variants:
                failures.append("scene_variant_mismatch")
            elif isinstance(expected_scene_variant, list) and not (actual_variants & {str(item) for item in expected_scene_variant}):
                failures.append("scene_variant_mismatch")
            failures.extend(evaluate_atomic_scene_contract(pack))
        for open_slot in pack.get("open_slots") or []:
            if isinstance(open_slot, dict) and set(open_slot) - {"slot", "bucket", "status", "reason"}:
                failures.append("masked_detail_leak")
                break

        row.update(
            {
                "pack_id": pack.get("pack_id"),
                "quality_profile": actual_profile,
                "selected_ids": [candidate.get("id") for candidate in selected],
                "mandatory_intents": sorted(mandatory),
                "multi_candidate_slots": multi_candidate_slots,
                "total_slot_candidates": total_candidates,
                "scene_variants": (pack.get("provenance") or {}).get("concept_scene_variants", []),
                "failures": failures,
                "passed": not failures,
            }
        )
        rows.append(row)
    return {
        "cases_path": str(cases_path),
        "case_count": len(rows),
        "failed_case_count": sum(1 for row in rows if not row.get("passed")),
        "results": rows,
    }


RETRIEVAL_HOLDOUT_CASE_KEYS = {
    "id",
    "intent",
    "allowed_selected_presets",
    "forbidden_selected_presets",
    "expected_profile",
    "expected_intent_domains",
    "expected_character_runtime_ids",
    "expected_character_policy_ids",
    "no_people",
}


def load_retrieval_holdout_cases(path: Path) -> List[JsonDict]:
    cases: List[JsonDict] = []
    seen_ids: Set[str] = set()
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        payload = json.loads(line)
        if not isinstance(payload, dict):
            raise ValueError(f"{path}:{line_number}: each retrieval case must be an object")
        unknown = set(payload) - RETRIEVAL_HOLDOUT_CASE_KEYS
        if unknown:
            raise ValueError(f"{path}:{line_number}: unknown retrieval case fields {sorted(unknown)}")
        case_id = str(payload.get("id") or "").strip()
        intent = str(payload.get("intent") or "").strip()
        allowed = payload.get("allowed_selected_presets")
        if not case_id or not intent:
            raise ValueError(f"{path}:{line_number}: id and intent are required")
        if case_id in seen_ids:
            raise ValueError(f"{path}:{line_number}: duplicate case id {case_id}")
        if not isinstance(allowed, list) or not allowed or any(not str(item).strip() for item in allowed):
            raise ValueError(f"{path}:{line_number}: allowed_selected_presets must be a non-empty string list")
        for key in (
            "forbidden_selected_presets",
            "expected_intent_domains",
            "expected_character_runtime_ids",
            "expected_character_policy_ids",
        ):
            value = payload.get(key)
            if value is not None and (
                not isinstance(value, list) or any(not str(item).strip() for item in value)
            ):
                raise ValueError(f"{path}:{line_number}: {key} must be a string list")
        if "no_people" in payload and not isinstance(payload.get("no_people"), bool):
            raise ValueError(f"{path}:{line_number}: no_people must be a boolean")
        seen_ids.add(case_id)
        cases.append(payload)
    if not cases:
        raise ValueError(f"{path}: at least one retrieval holdout case is required")
    return cases


def evaluate_retrieval_holdout(
    tags_path: Path,
    semantic_index_path: Path,
    cases_path: Path,
    seed: int,
    limit: int = 0,
) -> JsonDict:
    cases = load_retrieval_holdout_cases(cases_path)
    if limit:
        cases = cases[:limit]
    rows: List[JsonDict] = []
    for index, case in enumerate(cases):
        cmd = [
            sys.executable,
            str(WRAPPER_PATH),
            "--tags",
            str(tags_path),
            "--semantic-index",
            str(semantic_index_path),
            "--selection-mode",
            "semantic",
            "--novelty",
            "low",
            "--semantic-profile",
            "conservative",
            "--intent",
            str(case["intent"]),
            "--seed",
            str(seed + index),
            "--emit-candidate-pack",
        ]
        result = subprocess.run(cmd, cwd=PROJECT_ROOT, text=True, capture_output=True, check=False)
        failures: List[str] = []
        row: JsonDict = {"id": case.get("id"), "returncode": result.returncode}
        if result.returncode != 0:
            row.update({"failures": ["wrapper_failed"], "passed": False, "stderr": result.stderr.strip()})
            rows.append(row)
            continue
        try:
            payload = json.loads(result.stdout)
            if not isinstance(payload, list) or len(payload) != 1 or not isinstance(payload[0], dict):
                raise ValueError("expected one candidate pack")
            pack = payload[0]
        except Exception as exc:
            row.update({"failures": ["invalid_pack"], "passed": False, "error": str(exc)})
            rows.append(row)
            continue

        selected_preset = str((pack.get("provenance") or {}).get("preset_id") or "")
        allowed = {str(item) for item in case.get("allowed_selected_presets") or []}
        forbidden = {str(item) for item in case.get("forbidden_selected_presets") or []}
        if selected_preset not in allowed:
            failures.append("selected_preset_not_allowed")
        if selected_preset in forbidden:
            failures.append("forbidden_preset_selected")
        profile_id = str((pack.get("quality_profile") or {}).get("profile_id") or "")
        if case.get("expected_profile") and profile_id != str(case["expected_profile"]):
            failures.append("quality_profile")
        actual_domains = {
            str(item)
            for item in ((pack.get("coverage") or {}).get("intent_constraints") or {}).get("domains", [])
        }
        expected_domains = {str(item) for item in case.get("expected_intent_domains") or []}
        if not expected_domains.issubset(actual_domains):
            failures.append("intent_domains")
        character_grammar = (
            pack.get("character_grammar")
            if isinstance(pack.get("character_grammar"), dict)
            else {}
        )
        actual_character_runtime_ids = {
            str(item)
            for item in character_grammar.get("runtime_anchor_ids") or []
            if str(item)
        }
        actual_character_runtime_ids.update(
            str(item.get("id"))
            for item in character_grammar.get("runtime_nodes") or []
            if isinstance(item, dict) and str(item.get("id") or "")
        )
        expected_character_runtime_ids = {
            str(item) for item in case.get("expected_character_runtime_ids") or []
        }
        if not expected_character_runtime_ids.issubset(actual_character_runtime_ids):
            failures.append("character_runtime_ids")
        actual_character_policy_ids = {
            str(item) for item in character_grammar.get("policy_ids") or [] if str(item)
        }
        expected_character_policy_ids = {
            str(item) for item in case.get("expected_character_policy_ids") or []
        }
        if not expected_character_policy_ids.issubset(actual_character_policy_ids):
            failures.append("character_policy_ids")
        if case.get("no_people"):
            selected_rows = selected_candidate_rows(pack)
            if any(candidate_reads_as_human(candidate) for candidate in selected_rows):
                failures.append("person_candidate_selected")
            selected_slots = {str(candidate.get("slot") or "") for candidate in selected_rows}
            if selected_slots & PERSON_ONLY_CANDIDATE_SLOTS:
                failures.append("person_only_slot_selected")

        row.update(
            {
                "selected_preset": selected_preset,
                "allowed_selected_presets": sorted(allowed),
                "profile_id": profile_id,
                "intent_domains": sorted(actual_domains),
                "character_runtime_ids": sorted(actual_character_runtime_ids),
                "character_policy_ids": sorted(actual_character_policy_ids),
                "failures": failures,
                "passed": not failures,
            }
        )
        rows.append(row)
    return {
        "cases_path": str(cases_path),
        "selection_mode": "semantic",
        "semantic_profile": "conservative",
        "novelty": "low",
        "preset_pinned": False,
        "case_count": len(rows),
        "failed_case_count": sum(1 for row in rows if not row.get("passed")),
        "results": rows,
    }


def compact_quality_gate_summary(summary: JsonDict) -> JsonDict:
    compact: JsonDict = {"quality_gate": dict(summary.get("quality_gate") or {}), "checks": {}}
    golden_rows = []
    for row in summary.get("golden_modes") or []:
        if not isinstance(row, dict):
            continue
        golden_rows.append(
            {
                key: row.get(key)
                for key in ("mode", "average_coverage", "forbidden_case_count", "quality_fail_count")
                if key in row
            }
        )
    compact["checks"]["golden_modes"] = golden_rows
    for name, result in summary.items():
        if name in {"quality_gate", "golden_modes", "visual_review"} or not isinstance(result, dict):
            continue
        wanted = (
            "case_count",
            "failed_case_count",
            "failed_run_count",
            "legacy_failed_run_count",
            "blacklisted_case_count",
            "violation_count",
            "soft_promotion_ready",
            "passed",
        )
        compact["checks"][name] = {key: result.get(key) for key in wanted if key in result}
    if isinstance(summary.get("visual_review"), dict):
        compact["checks"]["visual_review"] = {
            key: summary["visual_review"].get(key)
            for key in (
                "case_count",
                "failed_case_count",
                "contract_failure_count",
                "review_focus_result_count",
                "failed_review_focus_result_count",
                "passed",
            )
            if key in summary["visual_review"]
        }
    return compact


def emit_evaluation_summary(
    summary: JsonDict,
    *,
    summary_only: bool = False,
    report_json: str | Path | None = None,
) -> None:
    if report_json:
        report_path = Path(report_json)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    output = compact_quality_gate_summary(summary) if summary_only else summary
    print(json.dumps(output, ensure_ascii=False, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate semantic prompt selection against golden intents.")
    parser.add_argument("--tags", default=DEFAULT_TAGS)
    parser.add_argument("--semantic-index", default=DEFAULT_INDEX)
    parser.add_argument("--seed", type=int, default=20260529)
    parser.add_argument("--limit", type=int, default=0, help="Limit golden cases for a quick run.")
    parser.add_argument("--mock-embeddings", action="store_true", help="Use deterministic mock embeddings for CI structure checks, not quality evaluation.")
    parser.add_argument("--dry-run", action="store_true", help="Print case counts and exit without generating prompts.")
    parser.add_argument("--check-index", action="store_true", help="Validate semantic index metadata without embedding API calls.")
    parser.add_argument("--bleed-check", action="store_true", help="Run cross-category leakage checks for product, craft, wildlife, and food scenarios.")
    parser.add_argument("--bleed-runs", type=int, default=10, help="Number of seeds per bleed-check case.")
    parser.add_argument("--diversity-check", action="store_true", help="Run V8 keyword preservation and free-slot diversity checks.")
    parser.add_argument("--candidate-pack-check", action="store_true", help="Run candidate-pack mandatory intent and cap checks.")
    parser.add_argument("--generalization-check", action="store_true", help="Run versioned held-out rule-mode contract and overfitting checks without embedding or image API calls.")
    parser.add_argument("--generalization-cases", default=DEFAULT_GENERALIZATION_CASES, help="Path to held-out JSONL cases for --generalization-check.")
    parser.add_argument("--holdout-check", action="store_true", help="Run the frozen rule-mode holdout suite independently from the public generalization cases.")
    parser.add_argument("--holdout-cases", default=DEFAULT_GENERALIZATION_HOLDOUT_CASES, help="Path to frozen JSONL cases for --holdout-check and the quality gate.")
    parser.add_argument("--domain-holdout-v2-check", action="store_true", help="Run the frozen v2 rule-mode holdout for science, mobility, and climate domain packs.")
    parser.add_argument("--domain-holdout-v2-cases", default=DEFAULT_DOMAIN_HOLDOUT_V2_CASES, help="Path to the frozen domain holdout v2 cases for the standalone check and quality gate.")
    parser.add_argument("--retrieval-holdout-check", action="store_true", help="Run preset-free semantic retrieval holdout cases against the real index.")
    parser.add_argument("--retrieval-holdout-cases", default=DEFAULT_RETRIEVAL_HOLDOUT_V4_CASES, help="Path to preset-free semantic retrieval holdout v4 cases.")
    parser.add_argument("--quality-gate", action="store_true", help="Run the real embedding quality gate for semantic concept benchmarks and regression checks.")
    parser.add_argument("--acceptance-gate", action="store_true", help="Run the full quality gate and require a passing --visual-review artifact.")
    parser.add_argument("--quality-runs", type=int, default=2, help="Number of seeds per concept benchmark case for --quality-gate.")
    parser.add_argument("--quality-require-soft", action="store_true", help="Make soft concept-mode promotion readiness a hard --quality-gate failure.")
    parser.add_argument("--summary-only", action="store_true", help="Print a compact quality-gate summary instead of per-case detail.")
    parser.add_argument("--report-json", default=None, help="Write the complete quality-gate report JSON to this path even with --summary-only.")
    parser.add_argument("--visual-review", default=None, help="Summarize a manual visual review JSON without embedding/API calls.")
    parser.add_argument("--contradiction-check", action="store_true", help="Generate rule-mode prompts across presets and report violations of declared coherence_rules (no embedding API needed).")
    parser.add_argument("--contradiction-runs", type=int, default=3, help="Number of seeds per preset for --contradiction-check.")
    args = parser.parse_args()

    load_project_env()
    visual_review_result: Optional[JsonDict] = None
    if args.visual_review:
        summary = summarize_visual_review(Path(args.visual_review))
        visual_review_result = summary["visual_review"]
        if not args.acceptance_gate:
            print(json.dumps(summary, ensure_ascii=False, indent=2))
            return 0 if summary["visual_review"]["passed"] else 10
    elif args.acceptance_gate:
        print("--acceptance-gate requires a manual --visual-review JSON artifact.", file=sys.stderr)
        return 14

    data = load_json(args.tags)
    cases = GOLDEN_CASES[: args.limit] if args.limit else GOLDEN_CASES
    tags_path = Path(args.tags)
    semantic_index_path = Path(args.semantic_index)
    if args.check_index:
        semantic_index = load_semantic_index_payload(semantic_index_path)
        validate_semantic_index_metadata(
            semantic_index,
            data,
            model=SEMANTIC_MODEL_ID,
            dimensions=DEFAULT_SEMANTIC_DIMENSIONS,
        )
        print(
            json.dumps(
                {
                    "status": "ok",
                    "dictionary_hash": semantic_index.get("dictionary_hash"),
                    "policy_schema_version": semantic_policy_schema_version(data),
                    "semantic_policy_hash": semantic_policy_digest(semantic_policy_from_source(data)),
                    "semantic_text_recipe": semantic_index.get("semantic_text_recipe"),
                    "expected_semantic_text_recipe": SEMANTIC_TEXT_RECIPE_VERSION,
                    "embedding_model": semantic_index.get("embedding_model"),
                    "embedding_dimensions": semantic_index.get("embedding_dimensions"),
                    "entry_count": len(semantic_index.get("entries", {})),
                },
                indent=2,
            )
        )
        return 0
    if args.contradiction_check:
        summary = {
            "contradiction_check": evaluate_contradiction_check(
                data,
                args.seed,
                args.contradiction_runs,
                preset_limit=args.limit,
            )
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0 if summary["contradiction_check"]["violation_count"] == 0 else 7
    if args.dry_run:
        print(
            json.dumps(
                {
                    "golden_cases": len(cases),
                    "open_ended_intents": len(OPEN_ENDED_INTENTS),
                    "multi_axis_preset_guards": len(MULTI_AXIS_PRESET_GUARDS),
                    "multi_axis_coverage_cases": len(MULTI_AXIS_COVERAGE_CASES),
                    "bleed_check_cases": len(BLEED_CHECK_CASES),
                    "diversity_check_cases": len(DIVERSITY_CHECK_CASES),
                    "candidate_pack_coverage_cases": len(CANDIDATE_PACK_COVERAGE_CASES),
                    "concept_benchmark_cases": len(CONCEPT_BENCHMARK_CASES),
                    "generalization_cases": len(load_generalization_cases(Path(args.generalization_cases))),
                    "holdout_cases": len(load_generalization_cases(Path(args.holdout_cases))),
                    "domain_holdout_v2_cases": len(load_generalization_cases(Path(args.domain_holdout_v2_cases))),
                    "retrieval_holdout_v4_cases": len(load_retrieval_holdout_cases(Path(args.retrieval_holdout_cases))),
                },
                indent=2,
            )
        )
        return 0

    import prompt_generator as generator_module

    if args.generalization_check or args.holdout_check or args.domain_holdout_v2_check or args.retrieval_holdout_check:
        summary: JsonDict = {}
        if args.generalization_check:
            summary["generalization_check"] = evaluate_generalization_check(
                tags_path,
                Path(args.generalization_cases),
                args.seed,
                args.limit,
            )
        if args.holdout_check:
            summary["holdout_check"] = evaluate_generalization_check(
                tags_path,
                Path(args.holdout_cases),
                args.seed,
                args.limit,
            )
        if args.domain_holdout_v2_check:
            summary["domain_holdout_v2_check"] = evaluate_generalization_check(
                tags_path,
                Path(args.domain_holdout_v2_cases),
                args.seed,
                args.limit,
            )
        if args.retrieval_holdout_check:
            summary["retrieval_holdout_v4_check"] = evaluate_retrieval_holdout(
                tags_path,
                semantic_index_path,
                Path(args.retrieval_holdout_cases),
                args.seed,
                args.limit,
            )
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0 if all(result["failed_case_count"] == 0 for result in summary.values()) else 12

    quality_requested = bool(args.quality_gate or args.acceptance_gate)
    if quality_requested and args.mock_embeddings:
        print("--quality-gate and --acceptance-gate require real embeddings; remove --mock-embeddings.", file=sys.stderr)
        return 8
    if quality_requested and not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
        print("The quality gate requires GEMINI_API_KEY or GOOGLE_API_KEY in the environment or project .env.", file=sys.stderr)
        return 8

    semantic_index = build_mock_index(data, generator_module) if args.mock_embeddings else load_semantic_index_payload(semantic_index_path)
    original_embed_texts = generator_module.embed_texts_with_gemini
    if args.mock_embeddings:
        generator_module.embed_texts_with_gemini = lambda texts, dimensions=DEFAULT_SEMANTIC_DIMENSIONS, **kwargs: fake_vectors(texts, dimensions=dimensions)
    gemini_api_key = "mock" if args.mock_embeddings else None

    try:
        if args.candidate_pack_check:
            summary = {
                "candidate_pack_coverage": evaluate_candidate_pack_coverage(
                    tags_path,
                    args.seed,
                    CANDIDATE_PACK_COVERAGE_CASES[: args.limit] if args.limit else CANDIDATE_PACK_COVERAGE_CASES,
                )
            }
            print(json.dumps(summary, ensure_ascii=False, indent=2))
            return 0 if summary["candidate_pack_coverage"]["failed_case_count"] == 0 else 11
        if args.bleed_check:
            bleed_cases = BLEED_CHECK_CASES[: args.limit] if args.limit else BLEED_CHECK_CASES
            summary = {
                "warning": "mock embeddings are deterministic test doubles, not retrieval-quality evidence" if args.mock_embeddings else None,
                "bleed_check": evaluate_bleed_check(
                    data,
                    bleed_cases,
                    args.seed,
                    semantic_index,
                    gemini_api_key,
                    runs=max(1, args.bleed_runs),
                ),
            }
            print(json.dumps(summary, ensure_ascii=False, indent=2))
            return 0 if summary["bleed_check"]["failed_case_count"] == 0 else 6
        if args.diversity_check:
            diversity_cases = DIVERSITY_CHECK_CASES[: args.limit] if args.limit else DIVERSITY_CHECK_CASES
            diversity_result = evaluate_diversity_check(
                data,
                diversity_cases,
                args.seed,
                semantic_index,
                gemini_api_key,
            )
            if args.mock_embeddings:
                diversity_result["failed_case_count"] = 0
                for row in diversity_result.get("results", []):
                    row["passed"] = True
                    row["mock_quality_gate_skipped"] = True
            summary = {
                "warning": "mock embeddings are deterministic test doubles, not retrieval-quality evidence" if args.mock_embeddings else None,
                "diversity_check": diversity_result,
                "candidate_pack_coverage": evaluate_candidate_pack_coverage(
                    tags_path,
                    args.seed,
                    CANDIDATE_PACK_COVERAGE_CASES[: args.limit] if args.limit else CANDIDATE_PACK_COVERAGE_CASES,
                ),
            }
            print(json.dumps(summary, ensure_ascii=False, indent=2))
            if summary["candidate_pack_coverage"]["failed_case_count"] > 0:
                return 11
            return 0 if args.mock_embeddings or summary["diversity_check"]["failed_case_count"] == 0 else 7
        if quality_requested:
            concept_cases = CONCEPT_BENCHMARK_CASES[: args.limit] if args.limit else CONCEPT_BENCHMARK_CASES
            diversity_cases = DIVERSITY_CHECK_CASES[: args.limit] if args.limit else DIVERSITY_CHECK_CASES
            bleed_cases = BLEED_CHECK_CASES[: args.limit] if args.limit else BLEED_CHECK_CASES
            golden_modes = [
                evaluate_mode(data, "rule", cases, args.seed, None),
                evaluate_mode(data, "hybrid", cases, args.seed, semantic_index, gemini_api_key),
                evaluate_mode(data, "semantic", cases, args.seed, semantic_index, gemini_api_key),
            ]
            summary = {
                "quality_gate": {
                    "real_embeddings_required": True,
                    "mock_embeddings": False,
                    "acceptance_gate": bool(args.acceptance_gate),
                    "quality_runs": max(1, args.quality_runs),
                    "soft_required": bool(args.quality_require_soft),
                    "dictionary_hash": semantic_index.get("dictionary_hash"),
                    "policy_schema_version": semantic_policy_schema_version(data),
                    "semantic_policy_hash": semantic_policy_digest(semantic_policy_from_source(data)),
                    "semantic_text_recipe": semantic_index.get("semantic_text_recipe"),
                    "embedding_model": semantic_index.get("embedding_model"),
                    "embedding_dimensions": semantic_index.get("embedding_dimensions"),
                },
                "golden_modes": golden_modes,
                "concept_benchmark": evaluate_concept_benchmark(
                    concept_cases,
                    args.seed,
                    tags_path,
                    semantic_index_path,
                    runs=max(1, args.quality_runs),
                    include_soft=True,
                ),
                "diversity_check": evaluate_diversity_check(
                    data,
                    diversity_cases,
                    args.seed,
                    semantic_index,
                    gemini_api_key,
                ),
                "bleed_check": evaluate_bleed_check(
                    data,
                    bleed_cases,
                    args.seed,
                    semantic_index,
                    gemini_api_key,
                    runs=max(1, min(args.bleed_runs, args.quality_runs)),
                ),
                "candidate_pack_coverage": evaluate_candidate_pack_coverage(
                    tags_path,
                    args.seed,
                    CANDIDATE_PACK_COVERAGE_CASES[: args.limit] if args.limit else CANDIDATE_PACK_COVERAGE_CASES,
                ),
                "generalization_check": evaluate_generalization_check(
                    tags_path,
                    Path(args.generalization_cases),
                    args.seed,
                    args.limit,
                ),
                "holdout_check": evaluate_generalization_check(
                    tags_path,
                    Path(args.holdout_cases),
                    args.seed,
                    args.limit,
                ),
                "domain_holdout_v2_check": evaluate_generalization_check(
                    tags_path,
                    Path(args.domain_holdout_v2_cases),
                    args.seed,
                    args.limit,
                ),
                "retrieval_holdout_v4_check": evaluate_retrieval_holdout(
                    tags_path,
                    semantic_index_path,
                    Path(args.retrieval_holdout_cases),
                    args.seed,
                    args.limit,
                ),
                "preset_guards": evaluate_preset_guards(data, MULTI_AXIS_PRESET_GUARDS, args.seed, semantic_index, gemini_api_key),
                "multi_axis_coverage": evaluate_multi_axis_coverage(data, MULTI_AXIS_COVERAGE_CASES, args.seed, semantic_index, gemini_api_key),
            }
            if visual_review_result is not None:
                summary["visual_review"] = visual_review_result
            legacy_passed = summary["concept_benchmark"]["legacy_failed_run_count"] == 0
            soft_ready = bool(summary["concept_benchmark"].get("soft_promotion_ready"))
            rule_golden = next(item for item in golden_modes if item["mode"] == "rule")
            semantic_golden = next(item for item in golden_modes if item["mode"] == "semantic")
            golden_failed = (
                any(item.get("quality_fail_count", 0) > 0 for item in golden_modes)
                or any(item.get("forbidden_case_count", 0) > 0 for item in golden_modes if item["mode"] != "rule")
                or semantic_golden["average_coverage"] < rule_golden["average_coverage"]
            )
            failed = (
                not legacy_passed
                or golden_failed
                or summary["diversity_check"]["failed_case_count"] > 0
                or summary["bleed_check"]["failed_case_count"] > 0
                or summary["candidate_pack_coverage"]["failed_case_count"] > 0
                or summary["generalization_check"]["failed_case_count"] > 0
                or summary["holdout_check"]["failed_case_count"] > 0
                or summary["domain_holdout_v2_check"]["failed_case_count"] > 0
                or summary["retrieval_holdout_v4_check"]["failed_case_count"] > 0
                or summary["preset_guards"]["blacklisted_case_count"] > 0
                or summary["multi_axis_coverage"]["failed_case_count"] > 0
                or (args.quality_require_soft and not soft_ready)
                or (args.acceptance_gate and not bool((visual_review_result or {}).get("passed")))
            )
            summary["quality_gate"]["legacy_passed"] = legacy_passed
            summary["quality_gate"]["golden_passed"] = not golden_failed
            summary["quality_gate"]["soft_promotion_ready"] = soft_ready
            summary["quality_gate"]["passed"] = not failed
            emit_evaluation_summary(
                summary,
                summary_only=args.summary_only,
                report_json=args.report_json,
            )
            if failed:
                print("real semantic quality gate failed", file=sys.stderr)
                return 9
            return 0
        summary = {
            "warning": "mock embeddings are deterministic test doubles, not retrieval-quality evidence" if args.mock_embeddings else None,
            "modes": [
                evaluate_mode(data, "rule", cases, args.seed, None),
                evaluate_mode(data, "hybrid", cases, args.seed, semantic_index, gemini_api_key),
                evaluate_mode(data, "semantic", cases, args.seed, semantic_index, gemini_api_key),
            ],
            "preset_guards": evaluate_preset_guards(data, MULTI_AXIS_PRESET_GUARDS, args.seed, semantic_index, gemini_api_key),
            "multi_axis_coverage": evaluate_multi_axis_coverage(data, MULTI_AXIS_COVERAGE_CASES, args.seed, semantic_index, gemini_api_key),
        }
    finally:
        if args.mock_embeddings:
            generator_module.embed_texts_with_gemini = original_embed_texts

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if args.mock_embeddings:
        return 0
    semantic = next(item for item in summary["modes"] if item["mode"] == "semantic")
    rule = next(item for item in summary["modes"] if item["mode"] == "rule")
    if any(item.get("quality_fail_count", 0) > 0 for item in summary["modes"]):
        print("one or more generated prompts failed runtime quality checks", file=sys.stderr)
        return 10
    if semantic["average_coverage"] < rule["average_coverage"]:
        print("semantic average coverage is below rule average coverage", file=sys.stderr)
        return 2
    if semantic["forbidden_case_count"] > 0:
        print("semantic produced forbidden facet/tag hits", file=sys.stderr)
        return 3
    if not args.mock_embeddings and summary["preset_guards"]["blacklisted_case_count"] > 0:
        print("semantic selected a blacklisted single-axis preset for a multi-axis guard case", file=sys.stderr)
        return 4
    if not args.mock_embeddings and summary["multi_axis_coverage"]["failed_case_count"] > 0:
        print("semantic failed multi-axis category coverage", file=sys.stderr)
        return 5
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
