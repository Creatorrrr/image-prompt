from __future__ import annotations

import gc
import hashlib
import importlib.util
import io
import json
import os
import random
import re
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
GENERATE_IMAGES_VIA_API_PATH = SKILL_DIR / "scripts" / "generate_images_via_api.py"
AUDIT_COMPOSED_PATH = SKILL_DIR / "scripts" / "audit_composed_prompt.py"
VALIDATOR_PATH = SKILL_DIR / "scripts" / "validate_photo_prompt_dictionary.py"
INDEX_BUILDER_PATH = SKILL_DIR / "scripts" / "build_semantic_index.py"
BM25F_RETRIEVAL_PATH = SKILL_DIR / "scripts" / "bm25f_retrieval.py"
EVAL_SEMANTIC_PATH = SKILL_DIR / "scripts" / "eval_semantic.py"
QUALITY_LAYERS_PATH = SKILL_DIR / "assets" / "photo_prompt_quality_layers.json"
SEMANTIC_INDEX_PATH = SKILL_DIR / "assets" / "photo_prompt_semantic_index.json"
RUN_LEDGER_SCHEMA_PATH = SKILL_DIR / "assets" / "run_ledger.schema.json"

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

BROAD_PRINCESS_COSTUME_IDS = {
    "royal_ball_gown",
    "royal_princess_hanbok",
    "ornate_hanfu_court_dress",
    "crown_princess_ceremonial_robe",
    "elegant_modern_daywear",
    "commoner_disguise_over_silk",
    "faded_court_robe_worn",
}

BROAD_PRINCESS_LOCATION_IDS = {
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
    "relational_action",
    "prop_direction",
    "partner_role",
    "partner_framing",
    "gaze_target",
    "body_orientation",
    "proxemics",
    "contact_point",
    "intent_state",
    "emotional_contradiction",
    "viewer_position",
    "narrative_phase",
    "safety_profile",
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
    "tray_handoff_counter",
    "clipboard_handover_corridor",
    "umbrella_share_threshold",
    "lunchbox_doorway_handoff",
    "coat_collar_adjust_indoor",
    "two_cups_one_table_silent",
    "hand_to_hand_envelope_drop",
    "field_blanket_aftercare",
    "palace_token_offhand_offer",
    "backstage_saved_ticket_note",
    "clinic_scold_care_chart",
    "counter_dessert_small_thunk",
    "vehicle_passenger_silent_handoff",
    "night_convenience_store_care_bag",
    "used_bookshop_reserved_note",
    "train_platform_saved_ticket_farewell",
    "garage_returned_key_aftercare",
    "winter_handwarmer_under_table",
    "memory_object_ticket_cups_still",
}
EXPANDED_FAMILY_IDS = {
    "analog_film_family",
    "weather_mood_portrait_family",
    "product_surface_family",
    "creator_branding_family",
    "craft_workshop_family",
    "transport_night_family",
    "relational_handoff_family",
    "caretaking_gesture_family",
    "domestic_intimacy_documentary_family",
    "service_counter_exchange_family",
    "clinical_handover_family",
    "field_relief_family",
    "paired_silence_family",
    "textless_evidence_family",
    "role_identity_action_family",
    "viewer_role_pov_family",
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
    "toward_partner_handoff",
    "off_frame_viewer_recipient",
    "partner_hand_visible_only",
    "to_handoff_object",
    "face_away_hands_toward_partner",
    "mid_handoff",
    "cold_face_warm_hands",
    "viewer_as_recipient",
    "warm_thermos_cup_prop",
    "table_edge_handover",
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
ASSASSIN_VIEWPOINT_PRESET_IDS = {
    "reflection_surveillance_portrait",
    "long_lens_distance_watch",
    "crowd_blend_stillpoint",
    "exit_route_threshold",
    "cover_identity_crack_closeup",
    "service_corridor_infiltration",
    "transit_tail_candid",
    "dead_drop_signal_portrait",
    "period_intrigue_observer",
    "macro_hidden_cue_detail",
}
ASSASSIN_VIEWPOINT_FAMILY_IDS = {
    "covert_surveillance_family",
    "reflection_surface_portrait_family",
    "crowd_blend_candid_family",
    "noir_threshold_family",
    "transit_observation_family",
    "cover_identity_fracture_family",
    "macro_covert_detail_family",
    "period_intrigue_family",
    "service_access_family",
    "dead_drop_signal_family",
}
ASSASSIN_VIEWPOINT_TAG_IDS = {
    "action": {
        "mirror_reflection_watch",
        "window_reflection_observe",
        "crowd_gap_target_glance",
        "blending_into_crowd",
        "exit_route_glance_back",
        "stairwell_pause_listen",
        "checking_wristwatch_timing",
        "adjusting_earpiece_discreet",
        "feigning_phone_call_cover",
        "pocketing_note_quietly",
        "leaning_pillar_watch",
        "sunglasses_reflection_watch",
        "passing_keycard_low",
        "pausing_before_threshold",
        "checking_service_door",
        "closing_compact_mirror",
        "watching_from_balcony_shadow",
        "reading_sealed_orders",
        "turning_away_from_security_camera",
        "rooftop_distance_watch",
        "over_railing_observe",
    },
    "prop": {
        "hotel_keycard_prop",
        "staff_lanyard_badge_prop",
        "discreet_earpiece_comms_prop",
        "antique_pocket_watch_prop",
        "folded_newspaper_cover_prop",
        "pressed_flower_bookmark_token",
        "single_chess_piece_token",
        "folded_origami_token",
        "coat_check_tag_prop",
        "train_ticket_stub_prop",
        "lipstick_marked_napkin_token",
        "florist_delivery_box_cover",
        "waiter_serving_tray_cover",
        "instrument_case_concealment_prop",
        "chalk_mark_signal_prop",
        "colored_thread_marker_prop",
        "compact_mirror_surveillance_prop",
        "sealed_black_envelope_prop",
        "single_unmatched_glove_prop",
    },
    "location": {
        "service_stairwell",
        "freight_elevator_interior",
        "fire_escape_landing",
        "hotel_back_corridor",
        "hotel_laundry_service_room",
        "banquet_kitchen_pass",
        "train_station_concourse",
        "subway_transfer_passage",
        "airport_arrivals_barrier",
        "taxi_rear_seat_interior",
        "crowded_night_market",
        "art_gallery_white_hall",
        "museum_gallery_after_hours",
        "opera_house_box_seat",
        "ballroom_gala_floor",
        "library_reading_room",
        "tea_house_private_room",
        "palace_side_gate",
        "rooftop_helipad_edge",
        "parking_payment_kiosk",
        "hotel_lobby",
    },
    "composition": {
        "mirror_layered_watch_frame",
        "shopwindow_reflection_frame",
        "puddle_reflection_split_frame",
        "sidemirror_observation_frame",
        "one_still_in_motion_blur_frame",
        "compressed_tele_layers",
        "foreground_crowd_occlusion",
        "over_railing_observation_frame",
        "exit_sign_glow_frame",
        "through_doorway_deep_frame",
        "elevator_gap_frame",
        "waist_level_hidden_prop_crop",
        "hands_only_detail_frame",
        "target_implied_off_frame_blur",
        "service_window_frame",
        "half_face_shadow_split",
        "chandelier_high_watch_frame",
    },
    "lighting": {
        "exit_sign_green_glow",
        "elevator_panel_glow",
        "gallery_track_spotlight",
        "chandelier_warm_pools",
        "market_string_lights",
        "single_match_or_lighter_glow",
        "venetian_blind_slats",
        "opera_stage_spill_light",
        "passing_headlight_sweep",
        "security_monitor_glow",
        "underpass_sodium_lamp",
        "service_corridor_fluorescent",
    },
    "mood": {
        "patient_predatory_calm",
        "poised_anonymity",
        "courtly_conspiracy",
        "countdown_stillness",
        "clinical_detachment",
        "surveillance_unease",
        "near_discovery_tension",
        "cover_identity_fracture",
        "public_place_paranoia",
        "professional_detachment",
        "vanishing_route_anxiety",
    },
    "capture_context": {
        "surveillance_reflection_capture",
        "long_lens_observation_capture",
        "hidden_in_crowd_candid_capture",
        "cover_role_documentary_capture",
        "rearview_or_sidemirror_capture",
        "accidental_phone_snapshot",
        "service_staff_id_photo",
        "dashcam_reflection_capture",
    },
    "camera_direction": {
        "long_lens_compressed_direction",
        "reflected_in_mirror_direction",
        "through_crowd_gap_direction",
        "over_railing_down_direction",
        "elevator_corner_camera_direction",
        "sidemirror_reflection_direction",
        "from_table_edge_hidden_camera",
        "from_inside_service_window",
    },
    "wearable_accessory": {
        "discreet_earpiece",
        "staff_lanyard_id",
        "plain_wristwatch_timing",
        "tinted_sunglasses_indoor",
        "wide_brim_hat_shadow",
        "high_collar_coat",
        "silk_opera_gloves",
        "service_apron_tie_cue",
        "phoenix_hairpin_glint",
        "camera_strap_cover",
    },
    "world": {
        "surveillance_noir",
        "period_court_intrigue",
        "cold_war_espionage_realism",
        "high_society_gala_world",
        "service_worker_access_world",
        "public_transit_tail_world",
        "ordinary_lifestyle_crack_world",
        "cover_identity_thriller_world",
        "dead_drop_signal_world",
    },
}
ASSASSIN_VIEWPOINT_BUNDLE_IDS = {
    "gallery_reflection_watch",
    "rooftop_long_lens_overwatch",
    "night_market_crowd_blend",
    "service_stairwell_egress",
    "gala_ballroom_cover_crack",
    "taxi_sidemirror_tail",
    "library_silent_signal_drop",
    "freight_elevator_access",
    "banquet_kitchen_service_cover",
    "opera_box_observer",
    "airport_arrivals_tail",
    "palace_side_gate_messenger",
    "parking_kiosk_exit_check",
    "museum_after_hours_relic",
    "safehouse_departure_noir",
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


def load_eval_semantic():
    scripts_dir = str(SKILL_DIR / "scripts")
    inserted = False
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
        inserted = True
    try:
        spec = importlib.util.spec_from_file_location("photo_prompt_eval_semantic", EVAL_SEMANTIC_PATH)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Could not load eval semantic module: {EVAL_SEMANTIC_PATH}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        if inserted:
            sys.path.remove(scripts_dir)


def prepare_audit_fixture(pack, *composed_payloads):
    """Finish hand-written audit fixtures with the strict v2 transport contract."""
    pack.setdefault("contract_version", "photo-candidate-pack/v2")
    pack.setdefault(
        "safety",
        {
            "mode": "automatic",
            "evaluation_requested": False,
            "status": "pass",
            "requires_user_approval": False,
            "items": [],
        },
    )
    pack.setdefault("concept_gates", [])

    candidate_ids = [
        str(candidate.get("id"))
        for candidate in pack.get("presets", [])
        if isinstance(candidate, dict) and candidate.get("id")
    ]
    for slot_payload in (pack.get("slots") or {}).values():
        if not isinstance(slot_payload, dict):
            continue
        candidate_ids.extend(
            str(candidate.get("id"))
            for candidate in slot_payload.get("candidates", [])
            if isinstance(candidate, dict) and candidate.get("id")
        )
    if not candidate_ids:
        pack.setdefault("presets", []).append({"id": "preset:test_fixture"})
        candidate_ids.append("preset:test_fixture")

    hashable = dict(pack)
    hashable["pack_id"] = None
    canonical = json.dumps(hashable, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    pack["pack_id"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]
    for composed in composed_payloads:
        composed["pack_id"] = pack["pack_id"]
        composed.setdefault("negative_en", pack.get("negative_en"))
        composed.setdefault("composer", "agent")
        if not composed.get("chosen_candidate_ids"):
            composed["chosen_candidate_ids"] = [candidate_ids[0]]
    return (pack, *composed_payloads)


class PromptGeneratorRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.generator = load_generator()
        cls.data = json.loads(TAGS_PATH.read_text(encoding="utf-8"))

    def generate(self, preset: str, seed: int = 1, **kwargs):
        return self.generator.generate_once(
            data=kwargs.pop("data", self.data),
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
            soft_anchor_spec=kwargs.pop("soft_anchor_spec", None),
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
            soft_anchor_spec=kwargs.pop("soft_anchor_spec", None),
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
        forwarded = list(args)
        if "--candidate-pack-version" in forwarded:
            version_index = forwarded.index("--candidate-pack-version") + 1
            if (
                version_index < len(forwarded)
                and forwarded[version_index] in {"v2", "v3"}
                and "--legacy-replay-reason" not in forwarded
            ):
                forwarded.extend(
                    ["--legacy-replay-reason", "test fixture compatibility replay"]
                )
        result = subprocess.run(
            [sys.executable, str(WRAPPER_PATH), *forwarded],
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

    def test_wizard_standalone_role_and_role_mixin_stay_distinct_from_stage_magic(self):
        standalone = self.run_wrapper_json(
            "--concept",
            "마법사",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--plain",
            "--no-negative",
        )
        standalone_concept = standalone["concepts"][0]
        self.assertEqual(standalone_concept["role"], "마법사")
        self.assertEqual(standalone_concept["applied_mixins"], [])
        self.assertEqual(standalone_concept["combined_forced_slots"]["subject"], ["archivist_role_model"])
        self.assertEqual(standalone_concept["combined_forced_slots"]["costume_style"], ["archivist_apron_gloves_costume"])
        self.assertIn("grand_archive_hall", standalone_concept["combined_forced_slots"]["location"])
        self.assertTrue(
            {
                "restoration_lab",
                "glass_office",
                "observatory_dome_room",
                "oak_library_dark_academia",
            }.intersection(standalone_concept["combined_forced_slots"]["location"])
        )
        self.assertEqual(standalone_concept["combined_forced_slots"]["camera_type"], ["full_frame_mirrorless"])
        self.assertIn("grimoire_candle_prop", standalone_concept["combined_forced_slots"]["prop"])
        self.assertIn("starmap_note_prop", standalone_concept["combined_forced_slots"]["prop"])
        self.assertTrue(
            {"slim_office_tablet_prop", "gift_tag_ledger_prop", "levitating_teacup_prop"}.intersection(
                standalone_concept["combined_forced_slots"]["prop"]
            )
        )
        self.assertIn("surreal_physics_detail", standalone_concept["combined_forced_slots"])
        self.assertIn("world_where_craft_is_spellcraft", standalone_concept["combined_forced_slots"]["world"])
        standalone_joined = " ".join(standalone["forward_args"])
        self.assertIn("mechanism rather than one prop", standalone_joined)
        self.assertIn("only one axis among", standalone_joined)
        self.assertIn("do not add visible tech visors", standalone_joined)
        self.assertIn("visibly change matter or force", standalone_joined)
        self.assertIn("distinct from stage magician", standalone_joined)
        self.assertIn("generic blue aura", standalone_joined)
        self.assertNotIn("stage_magician_role_model", standalone_joined)
        self.assertNotIn("magician_playing_card_fan_prop", standalone_joined)
        self.assertNotIn("witch_robe_wide_hat", standalone_joined)
        self.assertIn("--soft-anchor-spec", standalone["forward_args"])
        standalone_spec_index = standalone["forward_args"].index("--soft-anchor-spec") + 1
        standalone_spec = json.loads(standalone["forward_args"][standalone_spec_index])
        self.assertTrue(standalone_spec["visual_guards"][0]["fail_closed"])
        self.assertIn("sensor_visor_band", standalone_spec["free_slot_constraints"]["wearable_accessory"]["deny_pool"])
        self.assertIn("antenna_headset", standalone_spec["free_slot_constraints"]["wearable_accessory"]["deny_pool"])
        self.assertIn("machine_vision_camera", standalone_spec["free_slot_constraints"]["camera_type"]["deny_pool"])
        self.assertIn("lens_array_focus", standalone_spec["free_slot_constraints"]["focus"]["deny_pool"])
        self.assertIn("exposed_joint_focus", standalone_spec["free_slot_constraints"]["focus"]["deny_pool"])
        self.assertIn("boot_flicker_motion", standalone_spec["free_slot_constraints"]["motion"]["deny_pool"])
        self.assertIn("woven_cable_fiber_texture", standalone_spec["free_slot_constraints"]["texture"]["deny_pool"])
        self.assertIn("liquid_metal_specular_texture", standalone_spec["free_slot_constraints"]["texture"]["deny_pool"])
        self.assertIn("matte_synthetic_skin_pore", standalone_spec["free_slot_constraints"]["texture"]["deny_pool"])
        self.assertIn("brushed_alloy_microscratch", standalone_spec["free_slot_constraints"]["texture"]["deny_pool"])
        self.assertIn("automated_machine_civilization", standalone_spec["free_slot_constraints"]["world"]["deny_pool"])
        self.assertIn("visible tech visor", standalone_spec["render_suppress_terms"])

        role_combo = self.run_wrapper_json(
            "--concept",
            "마법사 연구원",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--plain",
            "--no-negative",
        )
        combo_concept = role_combo["concepts"][0]
        self.assertEqual(combo_concept["role"], "연구원")
        self.assertEqual(combo_concept["applied_mixins"], ["마법사"])
        self.assertEqual(combo_concept["combined_forced_slots"]["subject"], ["clinical_researcher_role_model"])
        self.assertEqual(combo_concept["combined_forced_slots"]["costume_style"], ["clinical_lab_coat_professional"])
        self.assertIn("glass_specimen_case_prop", combo_concept["combined_forced_slots"]["prop"])
        self.assertIn(
            combo_concept["selected_bundles"][0]["aspect"],
            {
                "micro_object_magic",
                "technomancy_interface",
                "contract_logomancy",
                "practical_craft_material_magic",
                "bureaucratic_contract_magic",
                "scientific_thaumaturgy",
                "domestic_urban_ward_magic",
                "spell_cost_aftermath",
                "scale_paradox_magic",
            },
        )
        self.assertIn("surreal_physics_detail", combo_concept["combined_forced_slots"])
        combo_joined = " ".join(role_combo["forward_args"])
        self.assertIn("medium plus scale plus transformation plus cost or trace", combo_joined)
        self.assertIn("tool -> material response -> residue", combo_joined)
        self.assertIn("expand wizardry beyond glow", combo_joined)
        self.assertIn("do not add visible tech visors", combo_joined)
        self.assertIn("visibly change matter or force", combo_joined)
        self.assertTrue(
            any(
                cue in combo_joined
                for cue in (
                    "lifted_glyph_self_glow",
                    "near_hand_glyphs_lift_and_orbit",
                    "wax_melting_resolidifying",
                    "ink_flowing_uphill_slow",
                    "cold_breath_in_warm_room",
                    "surface_tension_air",
                )
            )
        )
        self.assertNotIn("grimoire_candle_prop", combo_joined)
        self.assertNotIn("witch_robe_wide_hat", combo_joined)
        self.assertNotIn("magician_playing_card_fan_prop", combo_joined)
        self.assertIn("--soft-anchor-spec", role_combo["forward_args"])
        combo_spec_index = role_combo["forward_args"].index("--soft-anchor-spec") + 1
        combo_spec = json.loads(role_combo["forward_args"][combo_spec_index])
        self.assertTrue(combo_spec["visual_guards"][0]["fail_closed"])
        self.assertIn("sensor_visor_band", combo_spec["free_slot_constraints"]["wearable_accessory"]["deny_pool"])
        self.assertIn("antenna_headset", combo_spec["free_slot_constraints"]["wearable_accessory"]["deny_pool"])
        self.assertIn("machine_vision_camera", combo_spec["free_slot_constraints"]["camera_type"]["deny_pool"])
        self.assertIn("lens_array_focus", combo_spec["free_slot_constraints"]["focus"]["deny_pool"])
        self.assertIn("exposed_joint_focus", combo_spec["free_slot_constraints"]["focus"]["deny_pool"])
        self.assertIn("boot_flicker_motion", combo_spec["free_slot_constraints"]["motion"]["deny_pool"])
        self.assertIn("woven_cable_fiber_texture", combo_spec["free_slot_constraints"]["texture"]["deny_pool"])
        self.assertIn("liquid_metal_specular_texture", combo_spec["free_slot_constraints"]["texture"]["deny_pool"])
        self.assertIn("matte_synthetic_skin_pore", combo_spec["free_slot_constraints"]["texture"]["deny_pool"])
        self.assertIn("brushed_alloy_microscratch", combo_spec["free_slot_constraints"]["texture"]["deny_pool"])
        self.assertIn("lidar_scan_dot_pattern", combo_spec["free_slot_constraints"]["light_shape"]["deny_pool"])
        self.assertIn("AR hologram interface as the main magic cue", combo_spec["render_suppress_terms"])

    def test_wizard_expansion_presets_families_and_tags_are_registered(self):
        preset_ids = {preset["id"] for preset in self.data["presets"]}
        family_ids = {family["id"] for family in self.data.get("preset_families", [])}

        self.assertTrue(
            {
                "practical_craft_magic_family",
                "bureaucratic_magic_family",
                "scientific_thaumaturgy_family",
                "domestic_subtle_magic_family",
                "spell_cost_aftermath_family",
                "urban_modern_wizard_family",
                "institutional_guardian_magic_family",
                "scale_paradox_magic_family",
                "professional_mystic_family",
                "fundamental_reality_magic_family",
            }.issubset(family_ids)
        )
        self.assertTrue(
            {
                "seamstress_thread_binding_portrait",
                "notary_binding_stamp_portrait",
                "lab_glassware_transmutation_portrait",
                "kitchen_steam_script_portrait",
                "spell_exhaustion_aftermath_portrait",
                "convenience_store_night_charm_portrait",
                "school_nurse_remedy_ward_portrait",
                "teacup_storm_keeper_portrait",
                "wizard_forensic",
                "wizard_architect",
            }.issubset(preset_ids)
        )

        expected_slot_ids = {
            "surreal_concept": {
                "tool_caused_material_change",
                "written_word_binding_reality",
                "contract_enforced_by_world",
                "spatial_folding",
            },
            "surreal_anchor": {
                "wax_seal_pool",
                "ledger_open_page",
                "taut_sewing_thread",
                "crystal_growth_anchor",
            },
            "surreal_physics_detail": {
                "wax_melting_resolidifying",
                "ink_flowing_uphill_slow",
                "salt_grains_vibrating",
                "surface_tension_air",
            },
            "prop": {
                "wax_seal_kit_prop",
                "rubber_stamp_sigil_prop",
                "storm_glass_vial_prop",
                "tuning_fork_wand_prop",
            },
            "action": {
                "pressing_seal_into_wax",
                "weighing_intangible_action",
                "stirring_counterclockwise",
                "folding_blueprint_space",
            },
            "location": {
                "notary_office_after_hours",
                "herbal_pharmacy_drawers",
                "storm_glass_weather_lab",
                "city_intersection_night",
            },
        }
        for slot, expected_ids in expected_slot_ids.items():
            with self.subTest(slot=slot):
                actual_ids = {entry["id"] for entry in self.data["slots"][slot]}
                self.assertTrue(expected_ids.issubset(actual_ids))

    def test_wizard_mixin_uses_tool_material_trace_grammar(self):
        recipes = json.loads((SKILL_DIR / "assets" / "concept_recipes.json").read_text(encoding="utf-8"))
        wizard = recipes["mixins"]["마법사"]

        self.assertGreaterEqual(wizard["soft_min_anchors"], 3)
        self.assertTrue(
            {
                "surreal_concept",
                "surreal_anchor",
                "surreal_physics_detail",
                "contact_point",
            }.issubset(wizard["soft_anchor_slots"])
        )
        self.assertTrue(
            {
                "tool_to_material_to_trace",
                "spell_cost_aftermath",
                "scale_and_system_magic",
            }.issubset(wizard["anchor_families"])
        )
        self.assertTrue(
            {
                "tool_caused_material_change",
                "written_word_binding_reality",
                "contract_enforced_by_world",
                "spatial_folding",
            }.issubset(wizard["anchor_pool"]["surreal_concept"])
        )
        self.assertTrue(
            {
                "wax_seal_pool",
                "ledger_open_page",
                "taut_sewing_thread",
                "crystal_growth_anchor",
            }.issubset(wizard["anchor_pool"]["surreal_anchor"])
        )
        self.assertTrue(
            {
                "wax_melting_resolidifying",
                "ink_flowing_uphill_slow",
                "salt_grains_vibrating",
                "surface_tension_air",
            }.issubset(wizard["anchor_pool"]["surreal_physics_detail"])
        )

        bundle_ids = {bundle["id"] for bundle in wizard["bundles"]}
        self.assertTrue(
            {
                "generic_practical_craft_material_spell",
                "generic_bureaucratic_contract_spell",
                "generic_scientific_thaumaturgy",
                "generic_domestic_urban_ward",
                "generic_spell_cost_aftermath",
                "generic_scale_paradox_magic",
            }.issubset(bundle_ids)
        )

    def test_wizard_role_batch_uses_role_specific_active_spell_bundles(self):
        cases = [
            (
                "카리나 메이드 마법사",
                260609,
                "메이드",
                "maid_service_cantrip",
                "levitating_teacup_prop",
                "levitating_small_objects",
                "hands_only_detail_frame",
                "service cantrip",
                "tiny_levitation_contact_shadow",
            ),
            (
                "윈터 간호사 마법사",
                260610,
                "간호사",
                "nurse_diagnostic_star_chart",
                "clinical_chart_clipboard_prop",
                "checking_medical_chart",
                "document_foreground_face_background",
                "diagnostic logomancer",
                "condensation_forming_pattern",
            ),
            (
                "닝닝 경찰 마법사",
                260611,
                "경찰",
                "police_evidence_scrying_case",
                "case_file_folder_prop",
                "studying_caseboard",
                "caseboard_over_shoulder_frame",
                "procedural divination",
                "thread_tension_visible",
            ),
            (
                "지젤 광부 마법사",
                260612,
                "광부",
                "miner_headlamp_ore_sigils",
                "nonfunctional_pickaxe_prop",
                "checking_ore_contact_point",
                "document_foreground_face_background",
                "subterranean geomancer",
                "crystal_growth_contact_point",
            ),
            (
                "아일릿 원희 사복 여친 마법사",
                260613,
                "사복 여친",
                "casual_phone_constellation",
                "clear_case_smartphone",
                "checking_phone",
                "over_shoulder_phone_screen",
                "phone pressure",
                "surface_tension_air",
            ),
            (
                "설윤 공주 마법사",
                260614,
                "공주",
                "princess_royal_seal_thaumaturgy",
                "royal_seal_okse_prop",
                "touching_state_seal",
                "seal_hand_close_portrait",
                "court thaumaturgy",
                "paper_charring_along_line",
            ),
            (
                "유나 바니걸 마법사",
                260615,
                "바니걸",
                "bunny_backstage_scrying_mirror",
                "compact_mirror",
                "closing_compact_mirror",
                "reflection",
                "backstage scryer",
                "localized_refraction_at_contact",
            ),
            (
                "아이유 고스로리 마법사",
                260616,
                "고스로리",
                "gothic_lolita_curio_sorcery",
                "ornate_gothic_perfume_bottle",
                "levitating_small_objects",
                "frame_within_frame",
                "curio sorcerer",
                "tiny_levitation_contact_shadow",
            ),
            (
                "장원영 오피스룩 마법사",
                260617,
                "회사원",
                "office_ledger_spellwork",
                "staff_lanyard_badge_prop",
                "reviewing_ledger_columns",
                "document_foreground_face_background",
                "bureaucratic spellwork",
                "ink_flowing_uphill_slow",
            ),
            (
                "김채원 산타복 마법사",
                260618,
                "산타복",
                "santa_gift_contract_spell",
                "gift_tag_ledger_prop",
                "levitating_small_objects",
                "hands_foreground_face_behind",
                "holiday contract mage",
                "frost_crystallizing_realtime",
            ),
            (
                "카즈하 운동복 마법사",
                260619,
                "운동복",
                "sports_kinetic_training_spell",
                "stopwatch_training_prop",
                "sprint_start_drive",
                "medium_close",
                "kinetic trainer",
                "gravity_gradient_lean",
            ),
        ]
        selected_bundle_ids = set()
        selected_aspects = set()
        selected_props = set()
        selected_compositions = set()
        for (
            concept,
            seed,
            expected_role,
            expected_bundle,
            expected_prop,
            expected_action,
            expected_composition,
            expected_text,
            expected_surreal_detail,
        ) in cases:
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
            combined = concept_payload["combined_forced_slots"]
            joined = " ".join(explanation["forward_args"])

            self.assertEqual(concept_payload["role"], expected_role)
            self.assertEqual(concept_payload["applied_mixins"], ["마법사"])
            self.assertEqual(selected_bundle["bundle_id"], expected_bundle)
            self.assertFalse(selected_bundle["bundle_id"].startswith("shared_"))
            self.assertFalse(selected_bundle["bundle_id"].startswith("standalone_"))
            self.assertIn(expected_prop, combined["prop"])
            self.assertEqual(combined["action"], [expected_action])
            self.assertEqual(combined["composition"], [expected_composition])
            self.assertIn(expected_surreal_detail, combined["surreal_physics_detail"])
            self.assertNotEqual(combined["prop"], ["grimoire_candle_prop"])
            self.assertTrue("world-response" in joined or "world response" in joined or "respond" in joined)
            self.assertIn("distinct from stage magician", joined)
            self.assertIn("generic blue aura", joined)
            self.assertIn(expected_text, joined)

            if expected_role in {"메이드", "간호사", "사복 여친", "공주", "회사원", "산타복"}:
                self.assertIn("color", combined)
                self.assertNotIn("monochrome", combined["color"])
            if expected_role in {"간호사", "사복 여친", "공주", "회사원", "산타복"}:
                self.assertIn("lifted_glyph_self_glow", combined["light_shape"])
                self.assertNotEqual(combined["surreal_physics_detail"], ["near_hand_glyphs_lift_and_orbit"])
                self.assertTrue(
                    {
                        "condensation_forming_pattern",
                        "surface_tension_air",
                        "paper_charring_along_line",
                        "wax_melting_resolidifying",
                        "ink_flowing_uphill_slow",
                        "frost_crystallizing_realtime",
                        "gravity_gradient_lean",
                    }.intersection(combined["surreal_physics_detail"])
                )
            if expected_role == "공주":
                self.assertTrue(set(combined["costume_style"]).issubset(BROAD_PRINCESS_COSTUME_IDS))
                self.assertTrue(set(combined["costume_style"]))
                self.assertIn("royal_edict_gyoji_scroll_prop", combined["prop"])
            if expected_role == "회사원":
                self.assertEqual(combined["wardrobe_style"], ["clean_blazer_trousers"])
                self.assertIn("security_access_card_prop", combined["prop"])
                self.assertIn("slim_office_tablet_prop", combined["prop"])
                self.assertNotIn("star_map_tablet_prop", combined["prop"])
                self.assertEqual(combined["color"], ["cool_blue"])
                self.assertIn("ink visibly climbs", joined)
                self.assertNotIn("lift slightly", joined)
            if expected_role == "사복 여친":
                self.assertEqual(combined["wardrobe_style"], ["hoodie_shorts_sneakers"])
                self.assertIn("glitching_phone_screen_prop", combined["prop"])
                self.assertNotIn("star_map_tablet_prop", combined["prop"])
                self.assertEqual(combined["color"], ["cool_blue"])
            if expected_role == "산타복":
                self.assertEqual(combined["costume_style"], ["covered_santa_fur_trim_costume"])
                self.assertIn("christmas_lights_prop", combined["prop"])
                self.assertEqual(combined["color"], ["warm_kodak_gold"])
                self.assertEqual(combined["motion"], ["suspended_snowflake_motion"])
                self.assertEqual(combined["weather"], ["windblown_snow"])
                self.assertIn("frost grows across the gift tag", joined)
            if expected_role == "운동복":
                self.assertEqual(combined["wardrobe_style"], ["covered_track_jacket_training_set"])
                self.assertEqual(combined["motion"], ["kinetic_spell_trail_motion"])
                self.assertIn("kinetic_trail_edge_light", combined["light_shape"])

            selected_bundle_ids.add(selected_bundle["bundle_id"])
            selected_aspects.add(selected_bundle["aspect"])
            selected_props.add(expected_prop)
            selected_compositions.add(expected_composition)

        self.assertEqual(len(selected_bundle_ids), len(cases))
        self.assertEqual(len(selected_aspects), len(cases))
        self.assertGreaterEqual(len(selected_props), 10)
        self.assertGreaterEqual(len(selected_compositions), 7)

    def test_wizard_glow_dependent_bundles_pin_color_and_volumetric_spell_proof(self):
        cases = {
            "윈터 간호사 마법사": ("clinical_white", "condensation_forming_pattern"),
            "아일릿 원희 사복 여친 마법사": ("cool_blue", "surface_tension_air"),
            "설윤 공주 마법사": ("warm_kodak_gold", "paper_charring_along_line"),
            "장원영 오피스룩 마법사": ("cool_blue", "ink_flowing_uphill_slow"),
            "김채원 산타복 마법사": ("warm_kodak_gold", "frost_crystallizing_realtime"),
        }
        for concept, (expected_color, expected_surreal_detail) in cases.items():
            explanation = self.run_wrapper_json(
                "--concept",
                concept,
                "--explain-concept",
                "--selection-mode",
                "rule",
                "--seed",
                "260620",
                "--plain",
                "--no-negative",
            )
            combined = explanation["concepts"][0]["combined_forced_slots"]
            joined = " ".join(explanation["forward_args"])

            self.assertEqual(combined["color"], [expected_color])
            self.assertNotEqual(combined["color"], ["monochrome"])
            self.assertIn("lifted_glyph_self_glow", combined["light_shape"])
            self.assertIn(expected_surreal_detail, combined["surreal_physics_detail"])
            self.assertIn(expected_surreal_detail, joined)
            self.assertNotEqual(combined["surreal_physics_detail"], ["near_hand_glyphs_lift_and_orbit"])
            self.assertIn("lifted_glyph_self_glow", joined)

    def test_company_worker_role_aliases_anchor_corporate_time_pressure(self):
        payload = self.run_wrapper_json(
            "--concept",
            "회사원",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--plain",
            "--no-negative",
        )
        concept = payload["concepts"][0]
        self.assertEqual(concept["role"], "회사원")
        self.assertEqual(concept["applied_mixins"], [])
        self.assertEqual(concept["combined_forced_slots"]["subject"], ["office_worker"])
        self.assertNotIn("person_origin", concept["combined_forced_slots"])
        self.assertEqual(concept["combined_forced_slots"]["appearance_type"], ["corporate_professional"])
        self.assertEqual(concept["combined_forced_slots"]["wardrobe_style"], ["clean_blazer_trousers"])
        self.assertEqual(len(concept["selected_scene_variants"]), 1)
        selected_scene = concept["selected_scene_variants"][0]
        self.assertIn(selected_scene["id"], {"glass_office_task", "commute_threshold", "late_ledger_shift"})
        self.assertEqual(len(concept["recipe"]["scene_variants"]), 3)
        for slot, values in selected_scene["set"].items():
            expected_values = values if isinstance(values, list) else [values]
            self.assertEqual(concept["combined_forced_slots"][slot], expected_values)
        joined = " ".join(payload["forward_args"])
        self.assertIn("organizational anonymity", joined)
        self.assertIn("time discipline", joined)
        self.assertIn("commute fatigue", joined)
        self.assertIn("Avoid office-siren glamour", joined)
        self.assertNotIn("Korean salaried", joined)
        self.assertNotIn("--likeness-mode", payload["forward_args"])
        self.assertNotIn("witch_robe_wide_hat", joined)
        self.assertNotIn("traditional_shrine_interior", joined)

        alias_payload = self.run_wrapper_json(
            "--concept",
            "직장인",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--plain",
            "--no-negative",
        )
        alias_concept = alias_payload["concepts"][0]
        self.assertEqual(alias_concept["concept"], "회사원")
        self.assertEqual(alias_concept["role"], "회사원")
        self.assertEqual(alias_concept["combined_forced_slots"]["subject"], ["office_worker"])

        office_look_payload = self.run_wrapper_json(
            "--concept",
            "장원영 오피스룩 마법사",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--plain",
            "--no-negative",
        )
        office_look_concept = office_look_payload["concepts"][0]
        self.assertEqual(office_look_concept["role"], "회사원")
        self.assertEqual(office_look_concept["applied_mixins"], ["마법사"])
        self.assertEqual(office_look_concept["selected_bundles"][0]["bundle_id"], "office_ledger_spellwork")

    def test_company_worker_mixin_preserves_role_costumes_and_adds_corporate_layer(self):
        duplicate_payload = self.run_wrapper_json(
            "--concept",
            "장원영 오피스룩 회사원",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--plain",
            "--no-negative",
        )
        duplicate_concept = duplicate_payload["concepts"][0]
        self.assertEqual(duplicate_concept["concept"], "장원영 회사원 회사원")
        self.assertEqual(duplicate_concept["role"], "회사원")
        self.assertEqual(duplicate_concept["applied_mixins"], [])
        self.assertEqual(duplicate_concept["combined_forced_slots"]["subject"], ["office_worker"])

        cases = [
            (
                "카리나 메이드 회사원",
                "메이드",
                "maid_corporate_service_shift",
                {"subject": "maid_cafe_performer", "costume_style": "frill_apron_maid_costume"},
                "corporate service labor",
            ),
            (
                "윈터 간호사 회사원",
                "간호사",
                "nurse_corporate_health_admin",
                {"costume_style": "nurse_uniform_costume", "prop": "clinical_chart_clipboard_prop"},
                "company medical labor",
            ),
            (
                "닝닝 경찰 회사원",
                "경찰",
                "police_internal_compliance_shift",
                {"costume_style": "police_uniform_costume", "prop": "case_file_folder_prop"},
                "internal compliance",
            ),
            (
                "지젤 광부 회사원",
                "광부",
                "miner_shift_report_ledgers",
                {"costume_style": "miner_workwear_hard_hat", "prop": "nonfunctional_pickaxe_prop"},
                "shift reports",
            ),
            (
                "아일릿 원희 사복 여친 회사원",
                "사복 여친",
                "casual_after_work_phone_report",
                {"wardrobe_style": "hoodie_shorts_sneakers", "prop": "slim_office_tablet_prop"},
                "do not count a lanyard alone",
            ),
            (
                "설윤 공주 회사원",
                "공주",
                "princess_boardroom_succession_packet",
                {"costume_style": "royal_ball_gown", "wearable_accessory": "subtle_diamond_tiara"},
                "corporate succession pressure",
            ),
            (
                "유나 바니걸 회사원",
                "바니걸",
                "bunny_event_staff_timesheet",
                {"costume_style": "bunny_girl_costume", "prop": "compact_mirror"},
                "event staff company labor",
            ),
            (
                "아이유 고스로리 회사원",
                "고스로리",
                "gothic_lolita_office_records",
                {"costume_style": "gothic_lolita_dress", "prop": "slim_office_tablet_prop"},
                "corporate archive labor",
            ),
            (
                "김채원 산타복 회사원",
                "산타복",
                "santa_year_end_event_admin",
                {"costume_style": "covered_santa_fur_trim_costume", "prop": "gift_tag_ledger_prop"},
                "year-end event checklist",
            ),
            (
                "카즈하 운동복 회사원",
                "운동복",
                "sportswear_company_wellness_shift",
                {"wardrobe_style": "covered_track_jacket_training_set", "prop": "stopwatch_training_prop"},
                "do not replace the sportswear",
            ),
        ]

        for index, (concept, expected_role, expected_bundle, expected_slots, expected_text) in enumerate(cases, start=1):
            with self.subTest(concept=concept):
                payload = self.run_wrapper_json(
                    "--concept",
                    concept,
                    "--explain-concept",
                    "--selection-mode",
                    "rule",
                    "--seed",
                    str(270000 + index),
                    "--plain",
                    "--no-negative",
                )
                concept_payload = payload["concepts"][0]
                combined = concept_payload["combined_forced_slots"]
                selected_bundle = concept_payload["selected_bundles"][0]
                joined = " ".join(payload["forward_args"])

                self.assertEqual(concept_payload["role"], expected_role)
                self.assertEqual(concept_payload["applied_mixins"], ["회사원"])
                self.assertEqual(selected_bundle["mixin"], "회사원")
                self.assertEqual(selected_bundle["bundle_id"], expected_bundle)
                self.assertNotEqual(selected_bundle["bundle_id"], "generic_badge_commute_routine")
                self.assertIn("staff_lanyard_id", combined["wearable_accessory"])
                if expected_role == "사복 여친":
                    self.assertEqual(combined["prop"], ["slim_office_tablet_prop"])
                    self.assertIn("access card", joined)
                else:
                    self.assertIn("staff_lanyard_badge_prop", combined["prop"])
                    self.assertIn("security_access_card_prop", combined["prop"])
                self.assertTrue(
                    {"upper_body_framing", "waist_up_regalia_visible"} & set(combined["subject_framing"])
                )
                self.assertNotIn("office_worker", combined.get("subject", []))
                self.assertIn("base role's subject and costume", joined)
                self.assertIn("staff lanyard ID", joined)
                self.assertIn("access card", joined)
                self.assertIn(expected_text, joined)

                for slot, expected_id in expected_slots.items():
                    self.assertIn(expected_id, combined[slot], slot)

                if expected_role == "고스로리":
                    self.assertNotIn("ornate_gothic_perfume_bottle", combined["prop"])
                    self.assertIn("office tablet", joined)
                    self.assertIn("perfume bottle", joined)
                if expected_role == "사복 여친":
                    self.assertNotIn("clear_case_smartphone", combined["prop"])
                    self.assertNotIn("takeaway_coffee_cup", combined["prop"])
                if expected_role == "산타복":
                    self.assertNotIn("clean_blazer_trousers", combined.get("wardrobe_style", []))
                    self.assertIn("do not replace the Santa outfit", joined)
                if expected_role == "운동복":
                    self.assertNotIn("clean_blazer_trousers", combined.get("wardrobe_style", []))
                    self.assertIn("staff lanyard", joined)
                    self.assertIn("track jacket", joined)

        reversed_order = self.run_wrapper_json(
            "--concept",
            "회사원 경찰",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--plain",
            "--no-negative",
        )["concepts"][0]
        self.assertEqual(reversed_order["role"], "경찰")
        self.assertEqual(reversed_order["applied_mixins"], ["회사원"])
        self.assertEqual(reversed_order["selected_bundles"][0]["bundle_id"], "police_internal_compliance_shift")

    def test_concept_recipe_assassin_conditional_additional_is_data_driven(self):
        payload = self.run_wrapper_json(
            "--concept",
            "메이드 암살자",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--plain",
            "--no-negative",
            "--seed",
            "42",
        )

        concept = payload["concepts"][0]
        self.assertEqual(concept["concept_mode"], "legacy")
        self.assertEqual(concept["role"], "메이드")
        self.assertEqual(concept["applied_mixins"], ["암살자"])
        self.assertIn("role outfit is a cover identity/disguise for the assassin persona", payload["forward_args"])

    def test_concept_recipe_soft_mode_keeps_lock_and_axes_without_forced_slots(self):
        payload = self.run_wrapper_json(
            "--concept",
            "메이드 암살자",
            "--concept-mode",
            "soft",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--plain",
            "--no-negative",
            "--seed",
            "42",
        )

        concept = payload["concepts"][0]
        self.assertEqual(concept["concept_mode"], "soft")
        self.assertFalse(concept["forced_slots_applied"])
        self.assertIn("--concept-lock", payload["forward_args"])
        self.assertIn("--intent-axis", payload["forward_args"])
        self.assertIn("--soft-anchor-spec", payload["forward_args"])
        self.assertNotIn("--preset", payload["forward_args"])
        self.assertNotIn("--set", payload["forward_args"])
        self.assertIn("--additional-requirement", payload["forward_args"])
        # v2 개선(A2): soft 모드도 역할/믹스인의 정체성 서술 지시문을 전달한다
        # (강제 슬롯은 여전히 없음 — forced_slots_applied=False 어서션이 보장).
        self.assertIn(
            "role outfit is a cover identity/disguise for the assassin persona",
            payload["forward_args"],
        )
        spec_index = payload["forward_args"].index("--soft-anchor-spec") + 1
        forwarded_spec = json.loads(payload["forward_args"][spec_index])
        self.assertEqual(forwarded_spec["mode"], "soft")
        self.assertEqual(forwarded_spec["concept"], "메이드 암살자")
        self.assertGreaterEqual(forwarded_spec["min_anchors"], 2)
        slots = {anchor["slot"] for anchor in forwarded_spec["anchors"]}
        self.assertIn("costume_style", slots)
        self.assertIn("expression", slots)
        self.assertIn("prop", slots)
        self.assertEqual(concept["soft_anchor_spec"], forwarded_spec)

    def test_soft_anchor_spec_validation_and_bias_do_not_shrink_pool(self):
        with self.assertRaisesRegex(ValueError, "min_anchors"):
            self.generator.normalize_soft_anchor_spec(
                {
                    "min_anchors": "many",
                    "anchors": [{"slot": "prop", "ids": ["compact_mirror"]}],
                }
            )

        policy = self.generator.normalize_soft_anchor_spec(
            {
                "mode": "soft",
                "concept": "흡혈귀",
                "min_anchors": 1,
                "anchors": [
                    {
                        "slot": "prop",
                        "ids": ["compact_mirror"],
                        "terms": ["compact mirror", "mirror"],
                        "source": "mixin",
                    }
                ],
            }
        )
        contract = {"soft_anchor_policy": self.generator.soft_anchor_trace(policy)}
        pool = [
            {"id": "compact_mirror", "en": "a compact mirror", "weight": 1.0},
            {"id": "coffee_cup_prop", "en": "a paper coffee cup", "weight": 1.0},
        ]

        adjusted = self.generator.apply_soft_anchor_bias(
            "prop",
            pool,
            {"policy_schema_version": 1, "semantic_policy_hash": "test-hash"},
            contract,
        )

        self.assertEqual([item["id"] for item in adjusted], ["compact_mirror", "coffee_cup_prop"])
        self.assertGreater(adjusted[0]["weight"], adjusted[1]["weight"])
        self.assertEqual(pool[0]["weight"], 1.0)
        events = contract.get("soft_anchor_promotions", [])
        self.assertTrue(events)
        self.assertEqual(events[0]["promoted_ids"], ["compact_mirror"])

    def test_soft_anchor_critical_pool_constrains_candidate_window(self):
        policy = self.generator.normalize_soft_anchor_spec(
            {
                "mode": "soft",
                "concept": "경찰",
                "min_anchors": 1,
                "source_floors": {"role": 1},
                "anchors": [
                    {
                        "slot": "costume_style",
                        "ids": ["police_uniform_costume"],
                        "pool": ["police_uniform_costume"],
                        "terms": ["police"],
                        "source": "role",
                        "critical": True,
                    }
                ],
            }
        )
        contract = {"soft_anchor_policy": self.generator.soft_anchor_trace(policy)}
        pool = [
            {"id": "police_uniform_costume", "en": "police uniform", "weight": 1.0},
            {"id": "royal_princess_hanbok", "en": "princess hanbok", "weight": 99.0},
        ]

        adjusted = self.generator.apply_soft_anchor_bias(
            "costume_style",
            pool,
            {"policy_schema_version": 1, "semantic_policy_hash": "test-hash"},
            contract,
        )

        self.assertEqual([item["id"] for item in adjusted], ["police_uniform_costume"])
        self.assertEqual(contract["soft_anchor_pool_constraints"][0]["reason_code"], "critical_soft_anchor_pool")

    def test_soft_anchor_match_status_fails_critical_miss_even_with_min_anchor(self):
        policy = self.generator.normalize_soft_anchor_spec(
            {
                "mode": "soft",
                "concept": "광부 악마",
                "min_anchors": 1,
                "source_floors": {"role": 1, "mixin": 1},
                "anchors": [
                    {
                        "slot": "costume_style",
                        "ids": ["miner_workwear_hard_hat"],
                        "pool": ["miner_workwear_hard_hat"],
                        "terms": ["miner"],
                        "source": "role",
                        "critical": True,
                    },
                    {
                        "slot": "prop",
                        "ids": ["sealed_mission_envelope_prop"],
                        "pool": ["sealed_mission_envelope_prop"],
                        "terms": ["contract"],
                        "source": "mixin",
                    },
                ],
            }
        )

        status = self.generator.soft_anchor_match_status(
            policy,
            {
                "costume_style": {"id": "royal_princess_hanbok"},
                "prop": {"id": "sealed_mission_envelope_prop"},
            },
        )

        self.assertFalse(status["passed"])
        self.assertEqual(status["critical_missing"], ["costume_style"])
        self.assertIn("critical_anchor_missing", status["failure_reasons"])

    def test_soft_anchor_group_floor_does_not_cross_match_same_slot_sources(self):
        policy = self.generator.normalize_soft_anchor_spec(
            {
                "mode": "soft",
                "concept": "공주 흡혈귀",
                "min_anchors": 1,
                "group_floors": {"role_primary": 1, "mixin_primary": 1},
                "anchors": [
                    {
                        "slot": "prop",
                        "ids": ["round_fan_prop"],
                        "pool": ["round_fan_prop"],
                        "source": "role",
                        "groups": ["role_primary"],
                    },
                    {
                        "slot": "prop",
                        "ids": ["compact_mirror"],
                        "pool": ["compact_mirror"],
                        "source": "mixin",
                        "groups": ["mixin_primary"],
                        "primary": True,
                    },
                ],
            }
        )

        status = self.generator.soft_anchor_match_status(policy, {"prop": {"id": "round_fan_prop"}})

        self.assertFalse(status["passed"])
        self.assertEqual(status["group_counts"], {"role_primary": 1})
        self.assertEqual(status["group_floor_misses"], [{"group": "mixin_primary", "matched": 0, "floor": 1}])
        self.assertIn("anchor_group_floor_not_met:mixin_primary", status["failure_reasons"])

    def test_concept_soft_spec_carries_v3_group_guard_and_priority_terms(self):
        payload = self.run_wrapper_json(
            "--concept",
            "닝닝 경찰 팜므파탈",
            "--concept-mode",
            "soft",
            "--explain-concept",
            "--selection-mode",
            "semantic",
            "--plain",
            "--no-negative",
            "--seed",
            "3103",
        )

        self.assertNotIn("--set", payload["forward_args"])
        spec_index = payload["forward_args"].index("--soft-anchor-spec") + 1
        forwarded_spec = json.loads(payload["forward_args"][spec_index])

        self.assertEqual(forwarded_spec["group_floors"].get("mixin_primary"), 1)
        self.assertEqual(forwarded_spec["source_floors"].get("role"), 1)
        self.assertTrue(forwarded_spec["visual_guards"])
        self.assertTrue(forwarded_spec["render_priority_terms"])
        role_costume = [
            anchor
            for anchor in forwarded_spec["anchors"]
            if anchor["slot"] == "costume_style" and "role_primary" in anchor.get("groups", [])
        ]
        self.assertTrue(role_costume)
        self.assertIn("police_uniform_costume", role_costume[0]["pool"])
        femme_prop = [
            anchor
            for anchor in forwarded_spec["anchors"]
            if anchor["slot"] == "prop" and "mixin_primary" in anchor.get("groups", [])
        ]
        self.assertTrue(femme_prop)
        self.assertIn("single_playing_card_calling_card_prop", femme_prop[0]["pool"])

    def test_concept_soft_spec_carries_v4_anchor_variants_and_alias(self):
        payload = self.run_wrapper_json(
            "--concept",
            "닝닝 경찰 팜프파탈",
            "--concept-mode",
            "soft",
            "--explain-concept",
            "--selection-mode",
            "semantic",
            "--plain",
            "--no-negative",
            "--seed",
            "4104",
        )

        self.assertNotIn("--set", payload["forward_args"])
        spec_index = payload["forward_args"].index("--soft-anchor-spec") + 1
        forwarded_spec = json.loads(payload["forward_args"][spec_index])
        self.assertEqual(forwarded_spec["concept"], "닝닝 경찰 팜므파탈")
        femme_prop = [
            anchor
            for anchor in forwarded_spec["anchors"]
            if anchor["slot"] == "prop" and anchor.get("variant_group") == "femme_fatale_leverage"
        ]
        self.assertTrue(femme_prop)
        self.assertGreaterEqual(len(femme_prop[0]["pool"]), 2)
        self.assertIn("wax_sealed_dossier_prop", femme_prop[0]["pool"])

    def test_menhera_soft_mode_keeps_role_constraints_without_legacy_scaffold(self):
        payload = self.run_wrapper_json(
            "--concept",
            "유나 바니걸 멘헤라",
            "--concept-mode",
            "soft",
            "--explain-concept",
            "--selection-mode",
            "semantic",
            "--plain",
            "--no-negative",
            "--seed",
            "5105",
        )

        self.assertNotIn("--set", payload["forward_args"])
        spec_index = payload["forward_args"].index("--soft-anchor-spec") + 1
        forwarded_spec = json.loads(payload["forward_args"][spec_index])

        subject_constraints = forwarded_spec["free_slot_constraints"].get("subject_framing", {})
        self.assertIn("head_and_shoulders_crop", subject_constraints.get("prefer_ids", []))
        self.assertIn("full_body_framing", subject_constraints.get("deny_pool", []))
        self.assertEqual(forwarded_spec["render_suppress_terms"], [])
        self.assertEqual(forwarded_spec["dual_read_requirement"], {})
        self.assertEqual(forwarded_spec.get("mixin_cue_budget"), 1)
        self.assertIn("preferred_presets", forwarded_spec["preset_affinity"])
        explanation = payload["concepts"][0]
        self.assertEqual(explanation["selected_bundles"], [])
        self.assertEqual(
            explanation["combined_forced_slots"],
            {
                "subject": ["adult_stage_dancer"],
                "costume_style": ["bunny_girl_costume"],
            },
        )
        joined = " ".join(payload["forward_args"])
        self.assertIn("controlled social surface", joined)
        self.assertIn("do not require a phone, flower, mirror, ribbon", joined)

    def test_concept_soft_spec_carries_v6_render_directives(self):
        payload = self.run_wrapper_json(
            "--concept",
            "카리나 메이드 흡혈귀",
            "--concept-mode",
            "soft",
            "--explain-concept",
            "--selection-mode",
            "semantic",
            "--plain",
            "--no-negative",
            "--seed",
            "6106",
        )

        spec_index = payload["forward_args"].index("--soft-anchor-spec") + 1
        forwarded_spec = json.loads(payload["forward_args"][spec_index])
        directive_ids = {directive["id"] for directive in forwarded_spec["render_directives"]}

        self.assertIn("vampire_cast_shadow_not_wings", directive_ids)
        vampire_directive = next(
            directive
            for directive in forwarded_spec["render_directives"]
            if directive["id"] == "vampire_cast_shadow_not_wings"
        )
        self.assertIn("flat dark shadow", vampire_directive["positive_clause"])
        self.assertIn("physical wings", vampire_directive["suppress_terms"])

        angel_payload = self.run_wrapper_json(
            "--concept",
            "아일릿 원희 사복 여친 천사",
            "--concept-mode",
            "soft",
            "--explain-concept",
            "--selection-mode",
            "semantic",
            "--plain",
            "--no-negative",
            "--seed",
            "6107",
        )
        angel_spec_index = angel_payload["forward_args"].index("--soft-anchor-spec") + 1
        angel_spec = json.loads(angel_payload["forward_args"][angel_spec_index])
        self.assertIn(
            "angel_trace_shadow_not_costume",
            {directive["id"] for directive in angel_spec["render_directives"]},
        )

    def test_concept_soft_spec_carries_v7_repair_and_gothloli_robot(self):
        payload = self.run_wrapper_json(
            "--concept",
            "아이유 고스로리 로봇",
            "--concept-mode",
            "soft",
            "--explain-concept",
            "--selection-mode",
            "semantic",
            "--plain",
            "--no-negative",
            "--seed",
            "7107",
        )

        concept = payload["concepts"][0]
        self.assertEqual(concept["name"], "아이유")
        self.assertEqual(concept["role"], "고스로리")
        self.assertEqual(concept["applied_mixins"], ["로봇"])
        self.assertFalse(concept["forced_slots_applied"])
        self.assertNotIn("--set", payload["forward_args"])

        spec_index = payload["forward_args"].index("--soft-anchor-spec") + 1
        forwarded_spec = json.loads(payload["forward_args"][spec_index])
        render_groups = {
            group.get("group")
            for group in forwarded_spec.get("render_priority_terms", [])
            if group.get("tier") == "required"
        }
        self.assertIn("robot_deep_structural", render_groups)
        self.assertEqual(forwarded_spec["soft_repair_policy"]["max_attempts"], 2)
        self.assertIn("required_render_priority_missing", forwarded_spec["soft_repair_policy"]["trigger_checks"])
        self.assertIn("body horror", forwarded_spec["safety_negative_floor"])
        self.assertIn("service_android_role_unit", forwarded_spec["preset_affinity"]["preferred_presets"])

    def test_soft_post_render_repair_reselects_required_group_without_costume_demote(self):
        def entry(slot: str, item_id: str):
            return next(item for item in self.data["slots"][slot] if item["id"] == item_id)

        preset = next(item for item in self.data["presets"] if item["id"] == "compact_cinematic_prop_portrait")
        policy = self.generator.normalize_soft_anchor_spec(
            {
                "mode": "soft",
                "concept": "간호사 얀데레",
                "min_anchors": 1,
                "soft_repair_policy": {
                    "enabled": True,
                    "max_attempts": 2,
                    "trigger_checks": ["required_render_priority_missing"],
                    "target_slots": ["costume_style", "prop"],
                    "strategy": "prefer_then_reselect",
                    "fail_open": False,
                },
                "render_priority_terms": [
                    {
                        "id": "yandere_evidence",
                        "group": "yandere_records_evidence",
                        "tier": "required",
                        "terms": ["clinical chart"],
                        "min_hits": 1,
                        "target_slots": ["prop"],
                    }
                ],
                "anchors": [
                    {
                        "slot": "costume_style",
                        "ids": ["nurse_uniform_costume"],
                        "pool": ["nurse_uniform_costume"],
                        "source": "role",
                        "critical": True,
                    },
                    {
                        "slot": "prop",
                        "ids": ["clinical_chart_clipboard_prop"],
                        "pool": ["clinical_chart_clipboard_prop"],
                        "source": "mixin",
                        "groups": ["mixin_primary", "yandere_records_evidence"],
                        "primary": True,
                    },
                ],
            }
        )
        picked = {
            "costume_style": entry("costume_style", "nurse_uniform_costume"),
            "prop": entry("prop", "compact_mirror"),
        }
        contract = {"soft_anchor_policy": policy}
        result = {"prompt_en": "A covered nurse portrait with a compact mirror, no chart evidence."}

        changed = self.generator.apply_soft_post_render_repair(
            self.data,
            preset,
            random.Random(7),
            picked,
            result,
            forced_choices=None,
            semantic_context=None,
            generation_contract=contract,
        )

        self.assertTrue(changed)
        self.assertEqual(picked["costume_style"]["id"], "nurse_uniform_costume")
        self.assertEqual(picked["prop"]["id"], "clinical_chart_clipboard_prop")
        repair = contract["soft_anchor_repair"]
        self.assertEqual(repair["post_render_status"], "repaired")
        self.assertIn("yandere_records_evidence", repair["unresolved_required_groups"])
        self.assertEqual(repair["post_render_attempts"][0]["slot"], "prop")
        self.assertEqual(repair["post_render_attempts"][0]["status"], "reselected")

    def test_soft_body_first_guard_demotes_body_emphasis_candidates(self):
        data = {
            "semantic_policy": {
                "schema_version": 1,
                "soft_body_first_guard": {
                    "slot": "body_framing",
                    "demote_facets": ["soft_body_role:body_emphasis"],
                    "demote_multiplier": 0.15,
                },
            }
        }
        context = {
            "semantic_policy": data["semantic_policy"],
            "policy_schema_version": 1,
            "semantic_policy_hash": "test-policy",
        }
        contract = {
            "soft_anchor_policy": self.generator.normalize_soft_anchor_spec(
                {
                    "mode": "soft",
                    "concept": "간호사 얀데레",
                    "min_anchors": 1,
                    "anchors": [
                        {
                            "slot": "costume_style",
                            "ids": ["nurse_uniform_costume"],
                            "pool": ["nurse_uniform_costume"],
                            "source": "role",
                            "critical": True,
                        }
                    ],
                }
            )
        }
        pool = [
            {
                "id": "legs_heels_framing",
                "weight": 1.0,
                "facets": {"soft_body_role": ["body_emphasis"]},
            },
            {
                "id": "hands_nails_accessory_closeup",
                "weight": 1.0,
                "facets": {"soft_body_role": ["narrative_safe"]},
            },
        ]

        adjusted = self.generator.apply_soft_body_first_guard("body_framing", pool, context, contract)

        weights = {item["id"]: item["weight"] for item in adjusted}
        self.assertEqual(weights["legs_heels_framing"], 0.15)
        self.assertEqual(weights["hands_nails_accessory_closeup"], 1.0)
        self.assertTrue(contract["soft_body_first_guard_events"][0]["body_first_guard_applied"])

    def test_soft_body_first_guard_supports_slots_prefer_and_per_slot_multiplier(self):
        context = {
            "semantic_policy": {
                "schema_version": 1,
                "soft_body_first_guard": {
                    "slots": ["wardrobe_style", "subject_framing"],
                    "slot": "body_framing",
                    "demote_facets": ["soft_body_role:body_emphasis"],
                    "prefer_facets": ["soft_body_role:narrative_safe"],
                    "demote_multiplier": 0.5,
                    "per_slot_multiplier": {"wardrobe_style": 0.2},
                },
            },
            "policy_schema_version": 1,
            "semantic_policy_hash": "test-policy",
        }
        contract = {
            "soft_anchor_policy": self.generator.normalize_soft_anchor_spec(
                {
                    "mode": "soft",
                    "concept": "광부 악마",
                    "min_anchors": 1,
                    "anchors": [
                        {
                            "slot": "costume_style",
                            "ids": ["miner_workwear_hard_hat"],
                            "pool": ["miner_workwear_hard_hat"],
                            "source": "role",
                            "critical": True,
                        }
                    ],
                }
            )
        }
        pool = [
            {
                "id": "street_jacket_boots",
                "weight": 1.0,
                "facets": {"soft_body_role": ["body_emphasis"]},
            },
            {
                "id": "knit_cardigan_jeans",
                "weight": 1.0,
                "facets": {"soft_body_role": ["narrative_safe"]},
            },
            {"id": "neutral_wardrobe", "weight": 1.0},
        ]

        adjusted = self.generator.apply_soft_body_first_guard("wardrobe_style", pool, context, contract)

        weights = {item["id"]: item["weight"] for item in adjusted}
        self.assertEqual(weights["street_jacket_boots"], 0.2)
        self.assertGreater(weights["knit_cardigan_jeans"], 1.0)
        event = contract["soft_body_first_guard_events"][0]
        self.assertEqual(event["slot"], "wardrobe_style")
        self.assertIn("wardrobe_style", event["guard_slots"])
        self.assertEqual(event["demoted_ids"], ["street_jacket_boots"])
        self.assertEqual(event["preferred_ids"], ["knit_cardigan_jeans"])

    def test_soft_free_slot_constraints_narrow_pool_and_trace(self):
        policy = self.generator.normalize_soft_anchor_spec(
            {
                "mode": "soft",
                "concept": "멘헤라",
                "min_anchors": 1,
                "free_slot_constraints": {
                    "subject_framing": {
                        "allow_pool": ["head_and_shoulders_crop", "upper_body_framing"],
                        "deny_pool": ["upper_body_framing"],
                        "prefer_ids": ["head_and_shoulders_crop"],
                    }
                },
                "anchors": [
                    {
                        "slot": "subject_framing",
                        "ids": ["head_and_shoulders_crop"],
                        "pool": ["head_and_shoulders_crop"],
                        "source": "mixin",
                    }
                ],
            }
        )
        contract = {"soft_anchor_policy": policy}
        pool = [
            {"id": "full_body_framing", "weight": 1.0},
            {"id": "upper_body_framing", "weight": 1.0},
            {"id": "head_and_shoulders_crop", "weight": 1.0},
        ]

        adjusted = self.generator.apply_soft_free_slot_constraints(
            "subject_framing",
            pool,
            {"generation_contract": contract},
            contract,
        )

        self.assertEqual([item["id"] for item in adjusted], ["head_and_shoulders_crop"])
        self.assertGreater(adjusted[0]["weight"], 1.0)
        event = contract["soft_free_slot_constraint_events"][0]
        self.assertEqual(event["slot"], "subject_framing")
        self.assertEqual(event["before"], 3)
        self.assertEqual(event["after"], 1)

    def test_soft_free_slot_constraints_add_constrained_slot_to_generation(self):
        semantic_index = self.build_mock_semantic_index()
        original_embedder = self.generator.embed_texts_with_gemini
        self.generator.embed_texts_with_gemini = self.fake_gemini_vectors
        try:
            item = self.generate(
                "street_documentary",
                seed=6101,
                include_negative=False,
                intent="간호사 얀데레",
                selection_mode="semantic",
                semantic_index=semantic_index,
                gemini_api_key="test-api-key",
                soft_anchor_spec={
                    "mode": "soft",
                    "concept": "간호사 얀데레",
                    "min_anchors": 1,
                    "free_slot_constraints": {
                        "subject_framing": {
                            "allow_pool": ["head_and_shoulders_crop"],
                            "deny_pool": ["full_body_framing"],
                        }
                    },
                    "anchors": [
                        {
                            "slot": "subject",
                            "ids": ["fashion_influencer"],
                            "pool": ["fashion_influencer"],
                            "source": "role",
                        }
                    ],
                },
            )
        finally:
            self.generator.embed_texts_with_gemini = original_embedder

        self.assertEqual(item["choices"]["subject_framing"]["id"], "head_and_shoulders_crop")

    def test_soft_anchor_probability_floor_preserves_variant_candidates(self):
        policy = self.generator.normalize_soft_anchor_spec(
            {
                "mode": "soft",
                "concept": "팜므파탈",
                "min_anchors": 1,
                "anchors": [
                    {
                        "slot": "prop",
                        "ids": ["single_playing_card_calling_card_prop"],
                        "pool": ["single_playing_card_calling_card_prop", "wax_sealed_dossier_prop"],
                        "source": "mixin",
                        "primary": True,
                        "variant_group": "femme_fatale_leverage",
                    }
                ],
            }
        )
        context = {
            "generation_contract": {"soft_anchor_policy": policy},
            "semantic_policy": {
                "soft_anchor_diversity": {
                    "candidate_probability_floor": 0.2,
                    "max_single_candidate_probability": 0.85,
                }
            },
        }
        candidates = [
            ({"id": "single_playing_card_calling_card_prop"}, [], None, 100.0, 1.0, {}),
            ({"id": "wax_sealed_dossier_prop"}, [], None, 1.0, 1.0, {}),
        ]

        weights, summary = self.generator.apply_soft_anchor_probability_floor("prop", candidates, [100.0, 1.0], context)

        self.assertIsNotNone(summary)
        self.assertGreaterEqual(weights[1], 20.0)
        self.assertEqual(summary["anchor_variant_group"], "femme_fatale_leverage")

    def test_soft_render_suppress_terms_extend_negative_prompt(self):
        item = self.generate(
            "street_documentary",
            seed=5105,
            include_negative=True,
            soft_anchor_spec={
                "mode": "soft",
                "concept": "바니걸 멘헤라",
                "min_anchors": 1,
                "render_suppress_terms": ["bare shoulders", "full-body costume display"],
                "anchors": [
                    {
                        "slot": "subject",
                        "ids": ["fashion_influencer"],
                        "pool": ["fashion_influencer"],
                        "source": "role",
                    }
                ],
            },
        )

        self.assertIn("bare shoulders", item["negative_en"])
        self.assertIn("full-body costume display", item["negative_en"])

    def test_soft_render_directive_injects_positive_clause_and_negative_terms(self):
        item = self.generate(
            "compact_cinematic_prop_portrait",
            seed=6102,
            include_negative=True,
            forced_choices={"prop": ["bat_shadow_lace_prop"]},
            soft_anchor_spec={
                "mode": "soft",
                "concept": "메이드 흡혈귀",
                "min_anchors": 1,
                "render_directives": [
                    {
                        "id": "vampire_cast_shadow_not_wings",
                        "cue_terms": ["bat-wing-shaped lace shadow"],
                        "render_as": "cast_shadow",
                        "positive_clause": "the bat-wing motif appears only as a flat dark shadow cast onto a nearby wall",
                        "suppress_terms": ["physical wings", "wing prop"],
                    }
                ],
                "anchors": [
                    {
                        "slot": "prop",
                        "ids": ["bat_shadow_lace_prop"],
                        "pool": ["bat_shadow_lace_prop"],
                        "source": "mixin",
                    }
                ],
            },
        )

        self.assertIn("flat dark shadow cast onto a nearby wall", item["prompt_en"])
        self.assertIn("physical wings", item["negative_en"])
        self.assertIn("wing prop", item["negative_en"])
        self.assertEqual(item["provenance"]["additional_requirements"], [])
        self.assertIn(
            "the bat-wing motif appears only as a flat dark shadow cast onto a nearby wall",
            item["provenance"]["soft_requirements"],
        )
        directive_check = next(check for check in item["quality"]["checks"] if check["id"] == "soft_render_directives")
        self.assertEqual(directive_check["render_directive_count"], 1)

    def test_forced_preset_affinity_records_policy_conflict(self):
        item = self.generate(
            "candid_iphone_portrait",
            seed=5106,
            include_negative=False,
            include_trace=True,
            soft_anchor_spec={
                "mode": "soft",
                "concept": "공주 츤데레",
                "min_anchors": 1,
                "preset_affinity": {"discouraged_presets": ["candid_iphone_portrait"]},
                "anchors": [
                    {
                        "slot": "subject",
                        "ids": ["fashion_influencer"],
                        "pool": ["fashion_influencer"],
                        "source": "role",
                    }
                ],
            },
        )

        soft_check = next(check for check in item["quality"]["checks"] if check["id"] == "soft_preset_affinity")
        self.assertEqual(soft_check["status"], "warn")
        self.assertEqual(soft_check["policy_conflicts"][0]["selected"], "candid_iphone_portrait")

    def test_visual_review_summary_reports_body_drift(self):
        eval_semantic = load_eval_semantic()
        cases = []
        for index in range(7):
            cases.append(
                {
                    "case": f"review-{index}",
                    "prompt_id": f"prompt-{index}",
                    "image_id": f"image-{index}",
                    "dual_read": "pass",
                    "archetype_first_read": "pass",
                    "body_drift": "present" if index == 3 else "none",
                    "preset_conflict": "none",
                    "role_anchor": "pass",
                    "mixin_anchor": "pass",
                    "body_coverage_guard": "pass",
                    "render_modality": "pass",
                    "framing_constraint": "pass",
                    "body_emphasis_survived": "no",
                }
            )
        payload = {
            "schema_version": "photo-visual-review/v1",
            "provenance": {
                "generator_version": "test",
                "tags_hash": "test-tags",
                "reviewer": "unit-test",
                "reviewed_at": "2026-08-05T00:00:00Z",
            },
            "cases": cases,
        }
        with tempfile.TemporaryDirectory() as tmp:
            review_path = Path(tmp) / "review.json"
            review_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            summary = eval_semantic.summarize_visual_review(review_path)

        self.assertEqual(summary["visual_review"]["case_count"], 7)
        self.assertEqual(summary["visual_review"]["failed_case_count"], 1)
        self.assertEqual(
            summary["visual_review"]["field_summaries"]["body_drift"]["counts"].get("present"),
            1,
        )

    def test_visual_review_summary_reports_v6_fields(self):
        eval_semantic = load_eval_semantic()
        with tempfile.TemporaryDirectory() as tmp:
            review_path = Path(tmp) / "review.json"
            review_path.write_text(
                json.dumps(
                    {
                        "schema_version": "photo-visual-review/v1",
                        "provenance": {
                            "generator_version": "test",
                            "tags_hash": "test-tags",
                            "reviewer": "unit-test",
                            "reviewed_at": "2026-08-05T00:00:00Z",
                        },
                        "cases": [
                            {
                                "case": "카리나 메이드 흡혈귀",
                                "prompt_id": "prompt-1",
                                "image_id": "image-1",
                                "dual_read": "pass",
                                "archetype_first_read": "pass",
                                "body_drift": "none",
                                "preset_conflict": "none",
                                "role_anchor": "pass",
                                "mixin_anchor": "pass",
                                "body_coverage_guard": "pass",
                                "render_modality": "fail",
                                "framing_constraint": "pass",
                                "body_emphasis_survived": "no",
                            },
                            {
                                "case": "유나 바니걸 멘헤라",
                                "prompt_id": "prompt-2",
                                "image_id": "image-2",
                                "dual_read": "pass",
                                "archetype_first_read": "pass",
                                "body_drift": "none",
                                "preset_conflict": "none",
                                "role_anchor": "pass",
                                "mixin_anchor": "pass",
                                "body_coverage_guard": "pass",
                                "render_modality": "pass",
                                "framing_constraint": "pass",
                                "body_emphasis_survived": "yes",
                            },
                        ]
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            summary = eval_semantic.summarize_visual_review(review_path)

        self.assertEqual(summary["visual_review"]["case_count"], 2)
        self.assertEqual(summary["visual_review"]["failed_case_count"], 2)
        self.assertEqual(summary["visual_review"]["field_summaries"]["render_modality"]["counts"]["fail"], 1)
        self.assertEqual(summary["visual_review"]["field_summaries"]["body_emphasis_survived"]["counts"]["yes"], 1)

    def test_concept_recipe_princess_base_uses_broad_royal_register_language(self):
        payload = self.run_wrapper_json(
            "--concept",
            "설윤 공주",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--plain",
            "--no-negative",
        )

        concept = payload["concepts"][0]
        self.assertEqual(concept["name"], "설윤")
        self.assertEqual(concept["role"], "공주")
        self.assertEqual(concept["applied_role"], "공주")
        self.assertEqual(concept["applied_mixins"], [])
        self.assertEqual(concept["combined_forced_slots"]["subject"], ["princess_role"])
        self.assertEqual(concept["combined_forced_slots"]["appearance_type"], ["classic_elegant"])
        self.assertEqual(concept["combined_forced_slots"]["hair_style"], ["low_bun_hair"])
        self.assertEqual(concept["combined_forced_slots"]["makeup_style"], ["natural_makeup"])
        self.assertEqual(concept["combined_forced_slots"]["costume_style"], ["royal_ball_gown"])
        self.assertEqual(concept["combined_forced_slots"]["wearable_accessory"], ["subtle_diamond_tiara"])
        self.assertEqual(concept["combined_forced_slots"]["action"], ["poised_standing"])
        self.assertEqual(concept["combined_forced_slots"]["prop"], ["crown_on_cushion_prop"])
        self.assertEqual(concept["combined_forced_slots"]["composition"], ["centered_symmetric"])
        self.assertEqual(concept["combined_forced_slots"]["location"], ["throne_hall_interior"])

        joined = " ".join(payload["forward_args"])
        self.assertIn("appearance_type=classic_elegant", joined)
        self.assertIn("hair_style=low_bun_hair", joined)
        self.assertIn("makeup_style=natural_makeup", joined)
        self.assertIn("wearable_accessory=subtle_diamond_tiara", joined)
        self.assertIn("action=poised_standing", joined)
        self.assertIn("prop=crown_on_cushion_prop", joined)
        self.assertIn("composition=centered_symmetric", joined)
        self.assertIn("broad adult royal archetype", joined)
        self.assertIn("single Joseon-only costume", joined)
        self.assertIn("Chinese hanfu court", joined)
        self.assertIn("Western ballroom royalty", joined)
        self.assertIn("modern royal heiress", joined)
        self.assertIn("Do not collapse every princess prompt into hanbok/Joseon palace", joined)
        self.assertNotIn("Korean Joseon court princess styling", joined)
        self.assertNotIn("keep the East-Asian Joseon palace identity dominant", joined)

    def test_broad_role_recipes_expose_multiple_scene_registers(self):
        recipes = json.loads((SKILL_DIR / "assets" / "concept_recipes.json").read_text(encoding="utf-8"))
        expected_locations = {
            "광부": {"underground_mine_tunnel_set", "mine_rest_stop"},
            "산타복": {"christmas_market_lights", "seoul_bus_stop_snow", "gift_logistics_warehouse", "apartment_door_threshold"},
            "학생": {"school_reference_studio", "campus_cafe", "library_reading_room", "classroom_interior"},
            "무녀": {"traditional_shrine_interior", "urban_shrine_corner", "temple_gate_stone_steps", "temple_back_gate"},
            "기사": {"castle_armory_hall", "historical_armory_exhibit_room", "royal_guard_corridor", "palace_side_gate", "rpg_ruin_studio_set"},
            "퇴마사": {"shrine_exorcism_threshold", "urban_shrine_corner", "temple_back_gate", "apartment_door_threshold"},
            "음양사": {"shrine_exorcism_threshold", "traditional_shrine_interior", "temple_gate_stone_steps", "temple_back_gate"},
            "사제": {"cathedral_nave_interior", "stained_glass_chapel"},
            "수도자": {"stained_glass_chapel", "cathedral_nave_interior", "temple_lantern_hall"},
        }

        for role, locations in expected_locations.items():
            with self.subTest(role=role):
                recipe = recipes["roles"][role]
                anchor_locations = set(recipe["anchor_pool"]["location"])
                self.assertGreaterEqual(len(anchor_locations), 2)
                self.assertTrue(locations.issubset(anchor_locations))

                set_locations = set()
                for assignment in recipe["set"]:
                    if assignment.startswith("location="):
                        set_locations.update(assignment.split("=", 1)[1].split(","))
                self.assertTrue(locations.issubset(set_locations))

                policy = recipe["role_scene_policy"]
                self.assertTrue(policy["enabled"])
                self.assertTrue(policy["enforce"])
                self.assertEqual(set(policy["allowed_locations"]), anchor_locations)
                self.assertIn("highland_pasture", policy["forbidden_locations"])

    def test_princess_mixin_applies_to_role_combination_with_royal_anchors(self):
        payload = self.run_wrapper_json(
            "--concept",
            "카리나 메이드 공주",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--seed",
            "260609",
            "--plain",
            "--no-negative",
        )

        concept = payload["concepts"][0]
        self.assertEqual(concept["name"], "카리나")
        self.assertEqual(concept["role"], "메이드")
        self.assertEqual(concept["applied_role"], "메이드")
        self.assertEqual(concept["applied_mixins"], ["공주"])
        self.assertEqual(len(concept["selected_bundles"]), 1)
        self.assertEqual(concept["selected_bundles"][0]["bundle_id"], "maid_princess_role_reversal")
        self.assertEqual(concept["selected_bundles"][0]["preset"], "princess_servant_role_reversal_portrait")
        self.assertEqual(concept["combined_forced_slots"]["costume_style"], ["royal_apron_hanbok_hybrid"])
        self.assertEqual(concept["combined_forced_slots"]["wearable_accessory"], ["subtle_diamond_tiara"])
        self.assertEqual(concept["combined_forced_slots"]["prop"], ["royal_seal_okse_prop"])
        self.assertEqual(concept["combined_forced_slots"]["action"], ["served_by_attendants"])
        self.assertEqual(concept["combined_forced_slots"]["composition"], ["attendant_flanked_symmetry"])
        self.assertEqual(concept["combined_forced_slots"]["viewer_position"], ["viewer_as_attendant"])
        joined = " ".join(payload["forward_args"])
        self.assertIn("royal/princess identity must read before ordinary occupation", joined)
        self.assertIn("mirror selfie", joined)
        self.assertIn("phone covering face", joined)
        self.assertNotIn("costume_style=frill_apron_maid_costume", joined)

    def test_princess_role_is_not_also_applied_as_mixin_without_another_role(self):
        payload = self.run_wrapper_json(
            "--concept",
            "설윤 공주 흡혈귀",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--seed",
            "77",
            "--plain",
            "--no-negative",
        )

        concept = payload["concepts"][0]
        self.assertEqual(concept["name"], "설윤")
        self.assertEqual(concept["role"], "공주")
        self.assertEqual(concept["applied_role"], "공주")
        self.assertEqual(concept["applied_mixins"], ["흡혈귀"])
        self.assertTrue(
            set(concept["combined_forced_slots"]["costume_style"]).issubset(BROAD_PRINCESS_COSTUME_IDS)
        )
        self.assertIn("wearable_accessory", concept["combined_forced_slots"])

    def test_princess_expansion_assets_include_facets_bundles_and_aliases(self):
        recipes = json.loads((SKILL_DIR / "assets" / "concept_recipes.json").read_text(encoding="utf-8"))
        tags = json.loads(TAGS_PATH.read_text(encoding="utf-8"))

        self.assertEqual(recipes["aliases"]["프린세스"], "공주")
        self.assertEqual(recipes["aliases"]["왕녀"], "공주")
        self.assertIn("공주", recipes["mixins"])
        princess = recipes["mixins"]["공주"]
        self.assertIn("anchor_families", princess)
        self.assertEqual(princess["anchor_families"]["regalia"]["min_hits"], 1)
        self.assertIn("costume_style", recipes["bundle_override_slots"])
        self.assertIn("royal_anti_selfie", recipes["concept_safety"])

        bundle_ids = {bundle["id"] for bundle in princess["bundles"]}
        self.assertTrue(
            {
                "maid_princess_role_reversal",
                "nurse_princess_court_healer",
                "police_princess_royal_guard",
                "miner_princess_subterranean_exile",
                "casual_princess_modern_off_duty",
                "bunny_princess_gala_show",
                "incognito_princess_generic",
            }.issubset(bundle_ids)
        )
        preset_ids = {preset["id"] for preset in tags["presets"]}
        self.assertTrue(
            {
                "princess_lineage_succession_portrait",
                "princess_protection_confinement_portrait",
                "princess_incognito_disguise_portrait",
                "princess_servant_role_reversal_portrait",
                "subterranean_imprisoned_princess_portrait",
                "modern_casual_princess_portrait",
                "bunny_show_princess_portrait",
            }.issubset(preset_ids)
        )
        wearable_ids = {entry["id"] for entry in tags["slots"]["wearable_accessory"]}
        self.assertTrue(
            {
                "phoenix_binyeo_ornament",
                "cheopji_hair_ornament",
                "tteoljam_hair_ornament",
                "subtle_diamond_tiara",
                "signet_ring_concealed",
            }.issubset(wearable_ids)
        )

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
        self.assertIn(item["choices"]["costume_style"]["id"], BROAD_PRINCESS_COSTUME_IDS)
        self.assertEqual(item["choices"]["subject_framing"]["id"], "waist_up_framing")
        self.assertIn("Core concept lock: 설윤 공주 흡혈귀", item["prompt_en"])
        self.assertIn("predatory stillness", item["prompt_en"])
        self.assertIn("positive, visible non-graphic vampire identity anchors", item["prompt_en"])
        self.assertIn("role outfit readable", item["prompt_en"])
        self.assertIn("moonlit bat silhouettes", item["prompt_en"])
        self.assertIn("ruby eye catchlight", item["prompt_en"])
        self.assertIn("selected princess register as a coherent royal identity", item["prompt_en"])
        self.assertIn("do not flatten it into generic black-lace gothic costume", item["prompt_en"])
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
        self.assertEqual(police["choices"]["subject"]["id"], "police_officer_role")
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
        self.assertEqual(bunny["choices"]["subject"]["id"], "adult_stage_dancer")
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
                self.assertTrue(
                    set(concept_payload["combined_forced_slots"]["costume_style"]).issubset(
                        BROAD_PRINCESS_COSTUME_IDS
                    )
                )
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

    def test_concept_recipe_expands_devil_as_non_graphic_mixin(self):
        payload = self.run_wrapper_json(
            "--concept",
            "악마",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--seed",
            "606",
            "--plain",
            "--no-negative",
        )

        concept = payload["concepts"][0]
        self.assertEqual(concept["name"], "악마")
        self.assertIsNone(concept["role"])
        self.assertIsNone(concept["applied_role"])
        self.assertEqual(concept["applied_mixins"], ["악마"])
        self.assertTrue(concept["matched"])
        self.assertEqual(concept["mixins"]["악마"]["preset"], "compact_cinematic_prop_portrait")
        self.assertEqual(concept["combined_forced_slots"]["appearance_type"], ["classic_elegant"])
        self.assertEqual(concept["combined_forced_slots"]["expression"], ["mysterious_half_smile"])
        self.assertEqual(concept["combined_forced_slots"]["prop"], ["sealed_mission_envelope_prop"])
        self.assertEqual(concept["combined_forced_slots"]["lighting"], ["low_key"])
        self.assertEqual(concept["combined_forced_slots"]["light_shape"], ["cracked_door_sliver_light"])
        self.assertNotIn("light_direction", concept["combined_forced_slots"])
        self.assertEqual(len(concept["selected_bundles"]), 1)
        bundle = concept["selected_bundles"][0]
        self.assertEqual(bundle["mixin"], "악마")
        self.assertTrue(bundle["bundle_id"].startswith("standalone_"))
        joined = " ".join(payload["forward_args"])
        self.assertIn("devil/demon reinterpreted as a functional archetype", joined)
        self.assertIn("social or systemic evil", joined)
        self.assertIn("make at least two positive, visible devil identity anchors", joined)
        self.assertIn("do not make horned shadows the default solution", joined)
        self.assertIn("avoid product-commercial drift", joined)
        self.assertIn("sealed bargain", joined)
        self.assertIn("no visible blood", joined)
        self.assertIn("harmed or restrained victims", joined)
        self.assertIn("gore, wounds", joined)

    def test_devil_mixin_preserves_role_costume_and_contract_anchor(self):
        payload = self.run_wrapper_json(
            "--concept",
            "카리나 메이드 악마",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--seed",
            "606",
            "--plain",
            "--no-negative",
        )

        concept = payload["concepts"][0]
        self.assertEqual(concept["name"], "카리나")
        self.assertEqual(concept["role"], "메이드")
        self.assertEqual(concept["applied_role"], "메이드")
        self.assertEqual(concept["applied_mixins"], ["악마"])
        self.assertEqual(concept["combined_forced_slots"]["subject"], ["maid_cafe_performer"])
        self.assertEqual(concept["combined_forced_slots"]["costume_style"], ["frill_apron_maid_costume"])
        self.assertEqual(concept["combined_forced_slots"]["prop"], ["sealed_mission_envelope_prop"])
        self.assertEqual(concept["combined_forced_slots"]["lighting"], ["candlelit_ritual_light"])
        self.assertEqual(concept["combined_forced_slots"]["light_shape"], ["small_point_light"])
        self.assertNotIn("light_direction", concept["combined_forced_slots"])
        self.assertEqual(concept["combined_forced_slots"]["subject_framing"], ["upper_body_framing"])
        self.assertEqual(concept["selected_bundles"][0]["bundle_id"], "maid_contract_service")
        self.assertNotIn("gothic_doll_lace_dress", concept["combined_forced_slots"]["costume_style"])
        joined = " ".join(payload["forward_args"])
        self.assertIn("service cover identity", joined)
        self.assertIn("quiet contract or bargain offered to the viewer", joined)
        self.assertIn("courteous service becoming a binding offer", joined)
        self.assertIn("if any demonic silhouette appears, keep it secondary", joined)
        self.assertIn("contract, hand, face, and candlelit table", joined)
        self.assertIn("before ordinary maid cosplay", joined)
        self.assertNotIn("assassin persona", joined)

    def test_devil_concept_prompt_avoids_product_commercial_drift(self):
        item = self.run_wrapper_json(
            "--concept",
            "악마",
            "--selection-mode",
            "rule",
            "--seed",
            "606",
            "--lang",
            "en",
            "--no-negative",
            "--include-choices",
        )[0]

        self.assertNotEqual(item["provenance"]["preset_id"], "product_commercial")
        self.assertNotEqual(item["choices"]["subject"]["id"], "ceramic_bowl")
        self.assertEqual(item["choices"]["prop"]["id"], "sealed_mission_envelope_prop")
        self.assertEqual(item["choices"]["lighting"]["id"], "low_key")
        self.assertEqual(item["choices"]["light_shape"]["id"], "cracked_door_sliver_light")
        self.assertIn("Core concept lock: 악마", item["prompt_en"])
        self.assertIn("devil/demon reinterpreted as a functional archetype", item["prompt_en"])
        self.assertIn("social or systemic evil", item["prompt_en"])
        self.assertIn("do not make horned shadows the default solution", item["prompt_en"])
        self.assertIn("avoid product-commercial drift", item["prompt_en"])
        self.assertIn("standalone devil as a quiet tempter", item["prompt_en"])
        self.assertIn("sealed bargain", item["prompt_en"])
        self.assertIn("no visible blood", item["prompt_en"])
        self.assertIn("gore, wounds", item["prompt_en"])

    def test_devil_role_batch_uses_role_specific_anchors(self):
        cases = [
            (
                "카리나 메이드 악마",
                606,
                "maid_contract_service",
                "sealed_mission_envelope_prop",
                "small_point_light",
                "holding_story_prop",
                "frame_within_frame",
            ),
            (
                "윈터 간호사 악마",
                607,
                "nurse_accuser_chart",
                "sealed_mission_envelope_prop",
                "hairline_rim_glow",
                "holding_story_prop",
                "frame_within_frame",
            ),
            (
                "닝닝 경찰 악마",
                608,
                "police_adversary_dossier",
                "single_playing_card_calling_card_prop",
                "long_corridor_shadow",
                "holding_story_prop",
                "reflection",
            ),
            (
                "지젤 광부 악마",
                609,
                "miner_underworld_threshold",
                "sealed_mission_envelope_prop",
                "hairline_rim_glow",
                "holding_story_prop",
                "low_angle_hero",
            ),
            (
                "아일릿 원희 사복 여친 악마",
                610,
                "casual_phone_temptation",
                "paper_coffee_receipt",
                "neon_edge_shape",
                "holding_story_prop",
                "medium_close",
            ),
            (
                "설윤 공주 악마",
                611,
                "princess_fallen_light_decree",
                "sealed_mission_envelope_prop",
                "hairline_rim_glow",
                "holding_story_prop",
                "centered_symmetry",
            ),
            (
                "유나 바니걸 악마",
                612,
                "bunny_lure_mirror_trap",
                "compact_mirror",
                "screen_rectangle_mask",
                "holding_story_prop",
                "reflection",
            ),
        ]
        selected_bundle_ids = set()
        selected_props = set()
        selected_light_shapes = set()
        selected_anchor_signatures = set()
        for (
            concept,
            seed,
            expected_bundle,
            expected_prop,
            expected_light_shape,
            expected_action,
            expected_composition,
        ) in cases:
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
            self.assertEqual(concept_payload["applied_mixins"], ["악마"])
            self.assertEqual(selected_bundle["bundle_id"], expected_bundle)
            self.assertFalse(selected_bundle["bundle_id"].startswith("standalone_"))
            self.assertEqual(concept_payload["combined_forced_slots"]["prop"], [expected_prop])
            self.assertEqual(concept_payload["combined_forced_slots"]["light_shape"], [expected_light_shape])
            self.assertEqual(concept_payload["combined_forced_slots"]["action"], [expected_action])
            self.assertEqual(concept_payload["combined_forced_slots"]["composition"], [expected_composition])
            self.assertNotIn("light_direction", concept_payload["combined_forced_slots"])
            selected_bundle_ids.add(selected_bundle["bundle_id"])
            selected_props.add(expected_prop)
            selected_light_shapes.add(expected_light_shape)
            selected_anchor_signatures.add(
                (expected_prop, expected_light_shape, expected_action, expected_composition)
            )

            if concept_payload["role"] == "사복 여친":
                self.assertEqual(selected_bundle["preset"], "compact_urban_fashion_portrait")
                self.assertEqual(concept_payload["combined_forced_slots"]["wardrobe_style"], ["hoodie_shorts_sneakers"])
            if concept_payload["role"] == "공주":
                self.assertTrue(
                    set(concept_payload["combined_forced_slots"]["costume_style"]).issubset(
                        BROAD_PRINCESS_COSTUME_IDS
                    )
                )
                self.assertEqual(concept_payload["combined_forced_slots"]["subject_framing"], ["waist_up_framing"])
            if concept_payload["role"] == "바니걸":
                self.assertEqual(concept_payload["combined_forced_slots"]["subject_framing"], ["head_and_shoulders_crop"])

        self.assertEqual(len(selected_bundle_ids), len(cases))
        self.assertGreaterEqual(len(selected_props), 4)
        self.assertGreaterEqual(len(selected_light_shapes), 5)
        self.assertEqual(len(selected_anchor_signatures), len(cases))

    def test_devil_role_batch_limits_reflection_primary_anchors(self):
        cases = [
            ("카리나 메이드 악마", 606),
            ("윈터 간호사 악마", 607),
            ("닝닝 경찰 악마", 608),
            ("지젤 광부 악마", 609),
            ("아일릿 원희 사복 여친 악마", 610),
            ("설윤 공주 악마", 611),
            ("유나 바니걸 악마", 612),
        ]
        reflection_primary_compositions = {
            "reflection",
            "puddle_inverted_reflection",
            "over_shoulder_phone_screen",
        }
        reflection_roles = []
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
            composition = concept_payload["combined_forced_slots"]["composition"][0]
            if composition in reflection_primary_compositions:
                reflection_roles.append(concept_payload["role"])

        self.assertLessEqual(len(reflection_roles), 2)
        self.assertEqual(set(reflection_roles), {"경찰", "바니걸"})

    def test_devil_standalone_variants_include_systemic_and_trickster_modes(self):
        cases = [
            (
                0,
                "standalone_systemic_evil",
                "holographic_screen_prop",
                "cctv_corner_frame",
                "monitor_glow",
                "monitor_rectangle_glow",
                "standalone devil as social or systemic evil",
            ),
            (
                1,
                "standalone_playful_trickster",
                "paper_coffee_receipt",
                "medium_close",
                "neon_sign_light",
                "neon_edge_shape",
                "standalone devil as playful trickster",
            ),
        ]
        for (
            seed,
            expected_bundle,
            expected_prop,
            expected_composition,
            expected_light_type,
            expected_light_shape,
            expected_text,
        ) in cases:
            explanation = self.run_wrapper_json(
                "--concept",
                "악마",
                "--explain-concept",
                "--selection-mode",
                "rule",
                "--seed",
                str(seed),
                "--plain",
                "--no-negative",
            )
            concept_payload = explanation["concepts"][0]
            self.assertEqual(concept_payload["applied_mixins"], ["악마"])
            self.assertEqual(concept_payload["selected_bundles"][0]["bundle_id"], expected_bundle)
            self.assertEqual(concept_payload["combined_forced_slots"]["prop"], [expected_prop])
            self.assertEqual(concept_payload["combined_forced_slots"]["composition"], [expected_composition])
            self.assertEqual(concept_payload["combined_forced_slots"]["light_type"], [expected_light_type])
            self.assertEqual(concept_payload["combined_forced_slots"]["light_shape"], [expected_light_shape])
            joined = " ".join(explanation["forward_args"])
            self.assertIn("functional archetype", joined)
            self.assertIn(expected_text, joined)
            self.assertIn("do not make horned shadows the default solution", joined)

    def test_concept_recipe_expands_succubus_as_non_graphic_mixin(self):
        payload = self.run_wrapper_json(
            "--concept",
            "서큐버스",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--seed",
            "713",
            "--plain",
            "--no-negative",
        )

        concept = payload["concepts"][0]
        self.assertEqual(concept["name"], "서큐버스")
        self.assertIsNone(concept["role"])
        self.assertIsNone(concept["applied_role"])
        self.assertEqual(concept["applied_mixins"], ["서큐버스"])
        self.assertTrue(concept["matched"])
        self.assertEqual(concept["mixins"]["서큐버스"]["preset"], "compact_cinematic_prop_portrait")
        self.assertEqual(concept["combined_forced_slots"]["appearance_type"], ["classic_elegant"])
        self.assertEqual(concept["combined_forced_slots"]["subject_framing"], ["upper_body_framing"])
        self.assertEqual(len(concept["selected_bundles"]), 1)
        self.assertEqual(concept["selected_bundles"][0]["mixin"], "서큐버스")
        self.assertTrue(concept["selected_bundles"][0]["bundle_id"].startswith("standalone_"))
        joined = " ".join(payload["forward_args"])
        self.assertIn("dream-threshold tempter and life-drain presence", joined)
        self.assertIn("not a horned pin-up monster", joined)
        self.assertIn("invitation or bargain cue plus a life-drain trace", joined)
        self.assertIn("never through nudity, explicit sex, bedroom-victim staging", joined)
        self.assertIn("dread-allure duality without explicit sex, victim, coercion, or fetish framing", joined)

    def test_succubus_mixin_preserves_role_costume_and_dual_anchor(self):
        payload = self.run_wrapper_json(
            "--concept",
            "카리나 메이드 서큐버스",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--seed",
            "713",
            "--plain",
            "--no-negative",
        )

        concept = payload["concepts"][0]
        self.assertEqual(concept["name"], "카리나")
        self.assertEqual(concept["role"], "메이드")
        self.assertEqual(concept["applied_role"], "메이드")
        self.assertEqual(concept["applied_mixins"], ["서큐버스"])
        self.assertEqual(concept["combined_forced_slots"]["subject"], ["maid_cafe_performer"])
        self.assertEqual(concept["combined_forced_slots"]["costume_style"], ["frill_apron_maid_costume"])
        self.assertEqual(concept["combined_forced_slots"]["prop"], ["soul_contract_scroll_prop"])
        self.assertEqual(concept["combined_forced_slots"]["lighting"], ["candlelit_ritual_light"])
        self.assertEqual(concept["combined_forced_slots"]["composition"], ["frame_within_frame"])
        self.assertEqual(concept["combined_forced_slots"]["subject_framing"], ["upper_body_framing"])
        self.assertEqual(concept["selected_bundles"][0]["bundle_id"], "maid_dream_bargain_service")
        self.assertNotIn("gothic_doll_lace_dress", concept["combined_forced_slots"]["costume_style"])
        joined = " ".join(payload["forward_args"])
        self.assertIn("covered service role", joined)
        self.assertIn("candlelight bending toward the hand", joined)
        self.assertIn("not from body-display service fantasy", joined)
        self.assertIn("one invitation cue and one dimming, withered, stopped, or drawn-toward vitality trace", joined)
        self.assertNotIn("assassin persona", joined)

    def test_succubus_role_batch_uses_role_specific_anchors(self):
        cases = [
            ("카리나 메이드 서큐버스", 713, "메이드", "maid_dream_bargain_service", "soul_contract_scroll_prop", "frame_within_frame", "upper_body_framing"),
            ("윈터 간호사 서큐버스", 714, "간호사", "nurse_night_triage_lure", "glass_specimen_case_prop", "specimen_case_reflection_frame", "upper_body_framing"),
            ("닝닝 경찰 서큐버스", 715, "경찰", "police_badge_reflection_lure", "single_playing_card_calling_card_prop", "reflection", "head_and_shoulders_crop"),
            ("지젤 광부 서큐버스", 716, "광부", "miner_underworld_life_drain", "nonfunctional_pickaxe_prop", "low_angle_hero", "upper_body_framing"),
            ("아일릿 원희 사복 여친 서큐버스", 717, "사복 여친", "casual_second_cup_phone_lure", "paper_coffee_receipt", "over_shoulder_phone_screen", "waist_up_framing"),
            ("설윤 공주 서큐버스", 718, "공주", "princess_court_dream_decree", "sealed_heraldic_scroll_prop", "centered_symmetry", "waist_up_framing"),
            ("유나 바니걸 서큐버스", 719, "바니걸", "bunny_backstage_mirror_trap", "compact_mirror", "reflection", "head_and_shoulders_crop"),
            ("아이유 고스로리 서큐버스", 720, "고스로리", "gothic_lolita_perfume_dream", "ornate_gothic_perfume_bottle", "reflection", "upper_body_framing"),
            ("장원영 오피스룩 서큐버스", 721, "회사원", "office_afterhours_bargain_screen", "security_access_card_prop", "reflection", "upper_body_framing"),
            ("김채원 산타복 서큐버스", 722, "산타복", "santa_midnight_gift_pact", "gift_tag_ledger_prop", "frame_within_frame", "upper_body_framing"),
            ("카즈하 운동복 서큐버스", 723, "운동복", "athletic_stopwatch_breath_lure", "stopwatch_training_prop", "medium_close", "upper_body_framing"),
        ]
        selected_bundle_ids = set()
        selected_props = set()
        selected_compositions = set()
        for concept, seed, expected_role, expected_bundle, expected_prop, expected_composition, expected_framing in cases:
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
            self.assertEqual(concept_payload["applied_mixins"], ["서큐버스"])
            self.assertEqual(concept_payload["role"], expected_role)
            self.assertEqual(selected_bundle["bundle_id"], expected_bundle)
            self.assertFalse(selected_bundle["bundle_id"].startswith("standalone_"))
            self.assertEqual(concept_payload["combined_forced_slots"]["prop"], [expected_prop])
            self.assertEqual(concept_payload["combined_forced_slots"]["composition"], [expected_composition])
            self.assertEqual(concept_payload["combined_forced_slots"]["subject_framing"], [expected_framing])
            self.assertNotEqual(concept_payload["combined_forced_slots"].get("costume_style"), ["gothic_doll_lace_dress"])
            selected_bundle_ids.add(expected_bundle)
            selected_props.add(expected_prop)
            selected_compositions.add(expected_composition)

        self.assertEqual(len(selected_bundle_ids), len(cases))
        self.assertGreaterEqual(len(selected_props), 8)
        self.assertGreaterEqual(len(selected_compositions), 5)

    def test_succubus_prompts_include_invitation_and_drain_trace(self):
        cases = [
            ("서큐버스", 713),
            ("카리나 메이드 서큐버스", 713),
            ("윈터 간호사 서큐버스", 714),
            ("닝닝 경찰 서큐버스", 715),
            ("지젤 광부 서큐버스", 716),
            ("아일릿 원희 사복 여친 서큐버스", 717),
            ("설윤 공주 서큐버스", 718),
            ("유나 바니걸 서큐버스", 719),
            ("아이유 고스로리 서큐버스", 720),
            ("장원영 오피스룩 서큐버스", 721),
            ("김채원 산타복 서큐버스", 722),
            ("카즈하 운동복 서큐버스", 723),
        ]
        invitation_terms = {
            "invitation",
            "contract",
            "bargain",
            "offered",
            "viewer-facing",
            "threshold",
            "doorway",
        }
        drain_terms = {
            "life-drain",
            "life-force",
            "dimming",
            "drained",
            "withered",
            "stopped",
            "empty second cup",
            "candlelight bending",
            "drawn toward",
        }
        for concept, seed in cases:
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
            prompt = item["prompt_en"].lower()
            self.assertTrue(any(term in prompt for term in invitation_terms), msg=concept)
            self.assertTrue(any(term in prompt for term in drain_terms), msg=concept)

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
        self.assertIn(item["choices"]["costume_style"]["id"], BROAD_PRINCESS_COSTUME_IDS)
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

    def test_concept_recipe_expands_bulpan_dogeza_as_public_pressure_mixin(self):
        payload = self.run_wrapper_json(
            "--concept",
            "불판 도게자",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--seed",
            "701",
            "--plain",
            "--no-negative",
        )

        concept = payload["concepts"][0]
        self.assertEqual(concept["name"], "불판 도게자")
        self.assertIsNone(concept["role"])
        self.assertIsNone(concept["applied_role"])
        self.assertEqual(concept["applied_mixins"], ["불판 도게자"])
        self.assertTrue(concept["matched"])
        self.assertEqual(concept["combined_forced_slots"]["body_pose"], ["kneeling_soft_pose"])
        self.assertIn("underworld_red_underlight", concept["combined_forced_slots"]["light_type"])
        self.assertIn("forge_ember_glow", concept["combined_forced_slots"]["light_type"])
        self.assertIn("public_humiliation", concept["guide"]["불판 도게자"]["dominant_axes"])
        identity_axis_ids = {axis["id"] for axis in concept["soft_anchor_spec"]["identity_axes"]}
        self.assertTrue(
            {
                "abasement_pose",
                "heat_pressure_from_below",
                "public_surveillance_accountability",
            }.issubset(identity_axis_ids)
        )
        gate_status = {item["id"]: item["status"] for item in concept["gate_results"]}
        self.assertEqual(gate_status["mixin_shape"], "pass")
        self.assertEqual(gate_status["heat_from_below_forced"], "pass")
        self.assertEqual(gate_status["no_graphic_heat_injury"], "manual")
        joined = " ".join(payload["forward_args"])
        self.assertIn("깊은 도게자-style 부복", joined)
        self.assertIn("do not silently replace", joined)
        self.assertIn(
            "adult fictional subject only",
            " ".join(concept["mixins"]["불판 도게자"]["safety_requirements"]),
        )

    def test_bulpan_dogeza_alias_preserves_idol_role(self):
        payload = self.run_wrapper_json(
            "--concept",
            "리아 아이돌 철판도게자",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--seed",
            "702",
            "--plain",
            "--no-negative",
        )

        concept = payload["concepts"][0]
        self.assertEqual(concept["name"], "리아")
        self.assertEqual(concept["role"], "아이돌")
        self.assertEqual(concept["applied_role"], "아이돌")
        self.assertEqual(concept["applied_mixins"], ["불판 도게자"])
        gate_status = {item["id"]: item["status"] for item in concept["gate_results"]}
        self.assertEqual(gate_status["role_costume_preserved"], "pass")
        self.assertIn("kneeling_soft_pose", concept["combined_forced_slots"]["body_pose"])
        self.assertIn("underworld_red_underlight", concept["combined_forced_slots"]["light_type"])

    def test_dogeza_alone_is_not_overbroad_bulpan_alias(self):
        payload = self.run_wrapper_json(
            "--concept",
            "도게자",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--seed",
            "703",
            "--plain",
            "--no-negative",
        )

        concept = payload["concepts"][0]
        self.assertFalse(concept["matched"])
        self.assertEqual(concept["applied_mixins"], [])

    def test_concept_recipe_expands_white_bandage_fashion_as_couture_mixin(self):
        payload = self.run_wrapper_json(
            "--concept",
            "흰 붕대 패션",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--seed",
            "711",
            "--plain",
            "--no-negative",
        )

        concept = payload["concepts"][0]
        self.assertEqual(concept["concept"], "흰 붕대 패션")
        self.assertEqual(concept["applied_mixins"], ["흰 붕대 패션"])
        self.assertTrue(concept["matched"])
        self.assertIn(
            "opaque_white_bandage_couture_costume",
            concept["combined_forced_slots"]["costume_style"],
        )
        self.assertIn(
            "opaque_cotton_gauze_wrap_layers",
            concept["combined_forced_slots"]["garment_detail"],
        )
        self.assertIn(
            "crisscross_linen_bandage_wrapping",
            concept["combined_forced_slots"]["garment_detail"],
        )
        self.assertIn(
            "sculptural_bandage_bodycon",
            concept["combined_forced_slots"]["silhouette_proportion"],
        )
        guide_axes = set(concept["guide"]["흰 붕대 패션"]["dominant_axes"])
        self.assertIn("opaque_full_coverage", guide_axes)
        self.assertIn("fashion_not_medical_or_restraint", guide_axes)
        identity_axis_ids = {axis["id"] for axis in concept["soft_anchor_spec"]["identity_axes"]}
        self.assertTrue(
            {
                "opaque_full_coverage",
                "sculptural_wrap_engineering",
                "protective_rebirth_symbolism",
            }.issubset(identity_axis_ids)
        )
        gate_status = {item["id"]: item["status"] for item in concept["gate_results"]}
        self.assertEqual(gate_status["mixin_shape"], "pass")
        self.assertEqual(gate_status["full_coverage_costume_forced"], "pass")
        self.assertEqual(gate_status["wrapping_material_forced"], "pass")
        self.assertEqual(gate_status["sculptural_silhouette_forced"], "pass")
        self.assertEqual(gate_status["full_coverage_not_body_exposure"], "manual")
        self.assertEqual(gate_status["dual_read_high_fashion_not_patient"], "manual")
        joined = " ".join(payload["forward_args"])
        self.assertIn("--preset white_bandage_couture_editorial", joined)
        self.assertIn("opaque full intentional fashion coverage", joined)
        self.assertIn("Do not silently convert", joined)

    def test_white_bandage_alias_preserves_wrap_only_fashion_context(self):
        payload = self.run_wrapper_json(
            "--concept",
            "흰 붕대만 감은 코스튬",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--seed",
            "712",
            "--plain",
            "--no-negative",
        )

        concept = payload["concepts"][0]
        self.assertEqual(concept["concept"], "흰 붕대 패션")
        self.assertEqual(concept["applied_mixins"], ["흰 붕대 패션"])
        self.assertIn("only visible garment", " ".join(concept["mixins"]["흰 붕대 패션"]["additional"]))
        safety = " ".join(concept["mixins"]["흰 붕대 패션"]["safety_requirements"])
        self.assertIn("adult fictional subject only", safety)
        self.assertIn("no minors", safety)
        self.assertIn("nudity", safety)
        self.assertIn("restraint", safety)

    def test_white_bandage_concept_generation_uses_fashion_wrap_slots(self):
        item = self.run_wrapper_json(
            "--concept",
            "흰 붕대 패션",
            "--selection-mode",
            "rule",
            "--seed",
            "713",
            "--lang",
            "en",
            "--include-choices",
            "--no-negative",
        )[0]

        self.assertEqual(item["preset_id"], "white_bandage_couture_editorial")
        self.assertIn(
            item["choices"]["costume_style"]["id"],
            {
                "opaque_white_bandage_couture_costume",
                "deconstructed_mummy_wrap_dress",
                "sci_fi_rebirth_bandage_wrap_costume",
            },
        )
        self.assertIn(
            item["choices"]["garment_detail"]["id"],
            {
                "opaque_cotton_gauze_wrap_layers",
                "crisscross_linen_bandage_wrapping",
                "frayed_trailing_bandage_edges",
                "matte_white_bandage_weave",
            },
        )
        self.assertIn(
            item["choices"]["silhouette_proportion"]["id"],
            {"sculptural_bandage_bodycon", "protective_cocoon_wrap_silhouette"},
        )
        self.assertIn("Core concept lock: 흰 붕대 패션", item["prompt_en"])
        self.assertIn("bandage", item["prompt_en"])
        self.assertIn("gauze", item["prompt_en"])
        self.assertNotIn(
            item["choices"]["location"]["id"],
            {"hospital_corridor", "clinic_corridor_handover", "clinical_observation_lab"},
        )
        self.assertNotIn("hospital", item["prompt_en"].lower())

    def test_menhera_defaults_to_semantic_soft_mode_without_fixed_props(self):
        payload = self.run_wrapper_json(
            "--concept",
            "멘헤라",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--seed",
            "900",
            "--plain",
            "--no-negative",
        )

        concept = payload["concepts"][0]
        self.assertEqual(concept["concept_mode"], "soft")
        self.assertEqual(concept["applied_mixins"], ["멘헤라"])
        self.assertEqual(concept["combined_forced_slots"], {})
        self.assertEqual(concept["selected_bundles"], [])
        self.assertNotIn("--preset", payload["forward_args"])
        self.assertNotIn("--soft-anchor-spec", payload["forward_args"])
        joined = " ".join(payload["forward_args"])
        self.assertIn("controlled social surface", joined)
        self.assertIn("interrupted self-regulation or connection gesture", joined)

    def test_explicit_legacy_concept_recipe_expands_menhera_as_non_graphic_mixin(self):
        payload = self.run_wrapper_json(
            "--concept",
            "멘헤라",
            "--concept-mode",
            "legacy",
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
            "--concept-mode",
            "legacy",
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
            "--concept-mode",
            "legacy",
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
            "--concept-mode",
            "legacy",
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
            "--concept-mode",
            "legacy",
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
        # B4 재구성: 바니걸 멘헤라는 얼굴/손 중심 크롭으로 좁힘
        self.assertEqual(bunny["choices"]["subject_framing"]["id"], "head_and_shoulders_crop")
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
                "--concept-mode",
                "legacy",
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
            "--concept-mode",
            "legacy",
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
            "--concept-mode",
            "legacy",
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
            "--concept-mode",
            "legacy",
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
            "--concept-mode",
            "legacy",
            "--selection-mode",
            "rule",
            "--seed",
            "907",
            "--lang",
            "en",
            "--no-negative",
            "--include-choices",
        )[0]
        self.assertIn(princess["choices"]["costume_style"]["id"], BROAD_PRINCESS_COSTUME_IDS)
        self.assertEqual(princess["choices"]["light_type"]["id"], "phone_screen_face_glow")
        self.assertEqual(princess["choices"]["expression"]["id"], "eyes_closed_serene")
        self.assertIn("do NOT place a modern phone in the main silhouette", princess["prompt_en"])
        self.assertIn("faint cold rectangular glow", princess["prompt_en"])
        self.assertIn("dominant physical anchor", princess["prompt_en"])

    def test_menhera_nurse_uses_single_dominant_anchor_without_active_phone_check(self):
        nurse = self.run_wrapper_json(
            "--concept",
            "윈터 간호사 멘헤라",
            "--concept-mode",
            "legacy",
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

    def test_concept_recipe_expands_tsundere_as_warm_denial_mixin(self):
        payload = self.run_wrapper_json(
            "--concept",
            "츤데레",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--seed",
            "1201",
            "--plain",
            "--no-negative",
        )

        concept = payload["concepts"][0]
        self.assertEqual(concept["name"], "츤데레")
        self.assertIsNone(concept["role"])
        self.assertIsNone(concept["applied_role"])
        self.assertEqual(concept["applied_mixins"], ["츤데레"])
        self.assertTrue(concept["matched"])
        self.assertEqual(concept["mixins"]["츤데레"]["preset"], "candid_iphone_portrait")
        self.assertEqual(concept["combined_forced_slots"]["makeup_style"], ["natural_makeup"])
        self.assertIn(
            concept["combined_forced_slots"]["expression"][0],
            {"shy_downward_glance", "looking_away_pensive", "surprised_open_eyes", "eyes_dart_to_partner_then_away"},
        )
        self.assertIn("relational_action", concept["combined_forced_slots"])
        self.assertIn("prop_direction", concept["combined_forced_slots"])
        self.assertIn("partner_role", concept["combined_forced_slots"])
        self.assertEqual(len(concept["selected_bundles"]), 1)
        bundle = concept["selected_bundles"][0]
        self.assertEqual(bundle["mixin"], "츤데레")
        self.assertTrue(bundle["bundle_id"].startswith("standalone_"))
        self.assertTrue(bundle["subtype"])
        joined = " ".join(payload["forward_args"])
        self.assertIn("denial-vs-evidence contradiction", joined)
        self.assertIn("caring-evidence object", joined)
        self.assertIn("side-eye is only one optional denial cue", joined)
        self.assertIn("blush must remain photographic and restrained", joined)
        self.assertIn("never hoarded", joined)
        self.assertIn("explicitly NOT yandere", joined)
        self.assertIn("alive and embarrassed", joined)
        self.assertNotIn("assassin persona", joined)
        self.assertNotIn("instant_photo_stack", joined)
        self.assertNotIn("sheathed_utility_knife_prop", joined)

    def test_tsundere_mixin_preserves_role_costume_without_yandere_cues(self):
        payload = self.run_wrapper_json(
            "--concept",
            "카리나 메이드 츤데레",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--seed",
            "1202",
            "--plain",
            "--no-negative",
        )

        concept = payload["concepts"][0]
        self.assertEqual(concept["name"], "카리나")
        self.assertEqual(concept["role"], "메이드")
        self.assertEqual(concept["applied_role"], "메이드")
        self.assertEqual(concept["applied_mixins"], ["츤데레"])
        self.assertEqual(concept["combined_forced_slots"]["costume_style"], ["frill_apron_maid_costume"])
        self.assertEqual(concept["combined_forced_slots"]["expression"], ["pursed_lips_tiny_huff"])
        self.assertEqual(concept["combined_forced_slots"]["makeup_style"], ["natural_makeup"])
        self.assertEqual(concept["combined_forced_slots"]["prop"], ["coffee_cup_prop"])
        self.assertEqual(concept["combined_forced_slots"]["action"], ["maid_cafe_tray_pose"])
        self.assertEqual(concept["combined_forced_slots"]["composition"], ["table_edge_handover"])
        self.assertEqual(concept["combined_forced_slots"]["relational_action"], ["setting_down_dessert_with_small_thunk"])
        self.assertEqual(concept["combined_forced_slots"]["prop_direction"], ["set_down_between_two"])
        self.assertEqual(concept["combined_forced_slots"]["partner_role"], ["off_frame_customer"])
        self.assertEqual(concept["combined_forced_slots"]["intent_state"], ["just_after_handoff_pretending_indifference"])
        self.assertEqual(concept["selected_bundles"][0]["bundle_id"], "maid_extra_dessert_denial")
        self.assertEqual(concept["selected_bundles"][0]["subtype"], "verbal_denial")
        joined = " ".join(payload["forward_args"])
        self.assertIn("heart-latte coffee", joined)
        self.assertIn("tiny huff", joined)
        self.assertIn("small brusque thunk", joined)
        self.assertIn("no demure barista smile", joined)
        self.assertIn("warm comedic service", joined)
        self.assertIn("no chest-forward posture", joined)
        self.assertIn("no possessive watching", joined)
        self.assertNotIn("assassin persona", joined)
        self.assertNotIn("sheathed utility", joined)
        self.assertNotIn("instant_photo_stack", joined)

    def test_tsundere_concept_prompt_keeps_warm_denial_guards(self):
        payload = self.run_wrapper_json(
            "--concept",
            "설윤 공주 츤데레",
            "--selection-mode",
            "rule",
            "--seed",
            "1207",
            "--lang",
            "en",
            "--no-negative",
            "--include-choices",
        )

        item = payload[0]
        self.assertIn(item["choices"]["costume_style"]["id"], BROAD_PRINCESS_COSTUME_IDS)
        self.assertEqual(item["choices"]["expression"]["id"], "haughty_chin_soft_gaze")
        self.assertEqual(item["choices"]["makeup_style"]["id"], "natural_makeup")
        self.assertEqual(item["choices"]["prop"]["id"], "sealed_court_token_prop")
        self.assertEqual(item["choices"]["action"]["id"], "covering_face_with_fan_offering_token")
        self.assertEqual(item["choices"]["relational_action"]["id"], "covering_face_with_fan_offering_token")
        self.assertEqual(item["choices"]["prop_direction"]["id"], "presented_on_open_palm")
        self.assertEqual(item["choices"]["composition"]["id"], "fan_barrier_token_offer")
        self.assertIn("Core concept lock: 설윤 공주 츤데레", item["prompt_en"])
        self.assertIn("denial-vs-evidence contradiction", item["prompt_en"])
        self.assertIn("faint ear-tip or nose-bridge warmth", item["prompt_en"])
        self.assertIn("preserve the selected royal princess register and visible regalia", item["prompt_en"])
        self.assertIn("courtly haughtiness", item["prompt_en"])
        self.assertIn("slightly raised chin", item["prompt_en"])
        self.assertIn("warm personal gesture", item["prompt_en"])
        self.assertIn("no gaze-reversal trap", item["prompt_en"])
        self.assertIn("no weapon use", item["prompt_en"])
        self.assertNotIn("assassin persona", item["prompt_en"])
        self.assertNotIn("instant_photo_stack", item["prompt_en"])

    def test_tsundere_role_batch_uses_role_specific_bundles(self):
        cases = [
            (
                "카리나 메이드 츤데레",
                1202,
                "maid_extra_dessert_denial",
                {
                    "expression": ["pursed_lips_tiny_huff"],
                    "prop": ["coffee_cup_prop"],
                    "action": ["maid_cafe_tray_pose"],
                    "relational_action": ["setting_down_dessert_with_small_thunk"],
                    "prop_direction": ["set_down_between_two"],
                    "partner_role": ["off_frame_customer"],
                    "composition": ["table_edge_handover"],
                },
            ),
            (
                "윈터 간호사 츤데레",
                1203,
                "nurse_get_well_denial",
                {
                    "expression": ["scolding_mouth_soft_eyes"],
                    "prop": ["clinic_handover_chart_prop"],
                    "action": ["chart_tapping_scold"],
                    "relational_action": ["chart_tapping_scold"],
                    "prop_direction": ["toward_partner_handoff"],
                    "partner_role": ["off_frame_patient"],
                    "location": ["hospital_waiting_room"],
                    "subject_framing": ["upper_body_framing"],
                },
            ),
            (
                "닝닝 경찰 츤데레",
                1204,
                "police_shared_umbrella_denial",
                {
                    "expression": ["annoyed_but_worried"],
                    "prop": ["shared_umbrella_two_prop"],
                    "action": ["holding_umbrella_over_partner"],
                    "relational_action": ["holding_umbrella_over_partner"],
                    "prop_direction": ["kept_as_soft_barrier"],
                    "partner_role": ["off_frame_viewer_recipient"],
                    "location": ["rainy_bus_stop_shelter"],
                    "lighting": ["soft_window"],
                    "subject_framing": ["head_and_shoulders_crop"],
                },
            ),
            (
                "지젤 광부 츤데레",
                1205,
                "miner_shared_warmth_denial",
                {
                    "expression": ["worry_masked_as_irritation"],
                    "prop": ["warm_thermos_cup_prop"],
                    "action": ["placing_hot_drink_without_eye_contact"],
                    "relational_action": ["wrapping_blanket_around_partner"],
                    "prop_direction": ["toward_partner_handoff"],
                    "partner_role": ["off_frame_colleague"],
                    "lighting": ["single_flashlight_beam"],
                    "subject_framing": ["head_and_shoulders_crop"],
                },
            ),
            (
                "아일릿 원희 사복 여친 츤데레",
                1206,
                "casual_lunchbox_denial",
                {
                    "expression": ["pursed_lips_tiny_huff"],
                    "wardrobe_style": ["faded_hoodie_sweatpants"],
                    "prop": ["foil_wrapped_lunchbox_prop"],
                    "action": ["sliding_lunchbox_across_table"],
                    "relational_action": ["sliding_lunchbox_across_table"],
                    "prop_direction": ["set_down_between_two"],
                    "partner_role": ["off_frame_partner_romantic"],
                    "location": ["sunlit_kitchen"],
                    "lighting": ["soft_window"],
                    "light_intensity": ["high_key_bright"],
                    "mood": ["playful_sweet_cosplay"],
                },
            ),
            (
                "설윤 공주 츤데레",
                1207,
                "princess_kept_token_denial",
                {
                    "expression": ["haughty_chin_soft_gaze"],
                    "prop": ["sealed_court_token_prop"],
                    "action": ["covering_face_with_fan_offering_token"],
                    "relational_action": ["covering_face_with_fan_offering_token"],
                    "prop_direction": ["presented_on_open_palm"],
                    "partner_role": ["off_frame_partner_romantic"],
                    "color": ["hanbok_pastel_seasonal"],
                },
            ),
            (
                "유나 바니걸 츤데레",
                1208,
                "bunny_saved_drink_denial",
                {
                    "expression": ["caught_softening"],
                    "prop": ["extra_ticket_stub_prop"],
                    "action": ["offering_ticket_while_looking_away"],
                    "relational_action": ["offering_ticket_while_looking_away"],
                    "prop_direction": ["toward_partner_handoff"],
                    "partner_role": ["off_frame_customer"],
                    "composition": ["mirror_caught_kindness"],
                },
            ),
        ]
        selected_bundle_ids = set()
        selected_props = set()
        selected_prop_ids = []
        selected_subtypes = set()
        selected_expression_ids = []
        dark_drift_moods = {"occult_noir", "quiet_dread", "uncanny", "gothic_melancholy", "reportage_tense_noir"}

        for concept, seed, expected_bundle_id, expected_slots in cases:
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
            self.assertEqual(concept_payload["applied_mixins"], ["츤데레"])
            selected_bundle = concept_payload["selected_bundles"][0]
            self.assertEqual(selected_bundle["bundle_id"], expected_bundle_id)
            self.assertFalse(selected_bundle["bundle_id"].startswith("shared_"))
            self.assertFalse(selected_bundle["bundle_id"].startswith("standalone_"))
            self.assertTrue(selected_bundle["subtype"])
            selected_bundle_ids.add(selected_bundle["bundle_id"])
            selected_subtypes.add(selected_bundle["subtype"])
            forced_slots = concept_payload["combined_forced_slots"]
            self.assertEqual(forced_slots["makeup_style"], ["natural_makeup"])
            self.assertNotIn(forced_slots["mood"][0], dark_drift_moods)
            selected_props.add(forced_slots["prop"][0])
            selected_prop_ids.append(forced_slots["prop"][0])
            selected_expression_ids.append(forced_slots["expression"][0])
            for slot, ids in expected_slots.items():
                self.assertEqual(forced_slots[slot], ids)
            joined = " ".join(explanation["forward_args"])
            self.assertIn("caring-evidence object", joined)
            self.assertIn("blush must remain photographic and restrained", joined)
            self.assertIn("active rejection cue beyond gaze aversion", joined)
            self.assertIn("never hoarded", joined)
            self.assertIn("explicitly NOT yandere", joined)
            self.assertIn("costume-swap test", joined)

        self.assertEqual(len(selected_bundle_ids), len(cases))
        self.assertGreaterEqual(len(selected_subtypes), 4)
        self.assertGreaterEqual(len(selected_props), 6)
        self.assertGreaterEqual(len(set(selected_expression_ids)), 5)
        self.assertLessEqual(selected_expression_ids.count("skeptical_side_eye"), 1)
        drink_props = {"coffee_cup_prop", "takeaway_coffee_cup"}
        drink_anchored = sum(1 for prop_id in selected_prop_ids if prop_id in drink_props)
        self.assertLessEqual(drink_anchored, 1)

    def test_tsundere_nurse_bundle_uses_chart_anchor_not_bouquet(self):
        payload = self.run_wrapper_json(
            "--concept",
            "윈터 간호사 츤데레",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--seed",
            "1203",
            "--plain",
            "--no-negative",
        )

        concept = payload["concepts"][0]
        self.assertEqual(concept["selected_bundles"][0]["bundle_id"], "nurse_get_well_denial")
        self.assertEqual(concept["combined_forced_slots"]["prop"], ["clinic_handover_chart_prop"])
        self.assertEqual(concept["combined_forced_slots"]["relational_action"], ["chart_tapping_scold"])
        self.assertEqual(concept["combined_forced_slots"]["partner_role"], ["off_frame_patient"])
        joined = " ".join(payload["forward_args"])
        self.assertIn("handover chart", joined)
        self.assertIn("care checklist", joined)
        self.assertIn("pursed lecture mouth", joined)
        self.assertIn("chart-tapping", joined)
        self.assertIn("not a logo sign", joined)
        self.assertIn("no professional bedside-manner", joined)
        self.assertIn("no pin-up nurse pose", joined)
        self.assertIn("no full-figure uniform display", joined)

    def test_tsundere_bunny_bundle_avoids_coffee_anchor(self):
        payload = self.run_wrapper_json(
            "--concept",
            "유나 바니걸 츤데레",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--seed",
            "1208",
            "--plain",
            "--no-negative",
        )

        concept = payload["concepts"][0]
        forced = concept["combined_forced_slots"]
        self.assertEqual(concept["selected_bundles"][0]["bundle_id"], "bunny_saved_drink_denial")
        self.assertEqual(forced["prop"], ["extra_ticket_stub_prop"])
        self.assertEqual(forced["relational_action"], ["offering_ticket_while_looking_away"])
        self.assertEqual(forced["prop_direction"], ["toward_partner_handoff"])
        self.assertNotIn(forced["prop"][0], {"coffee_cup_prop", "takeaway_coffee_cup"})
        joined = " ".join(payload["forward_args"])
        self.assertIn("saved spare ticket", joined)
        self.assertIn("caught mid-gesture", joined)
        self.assertIn("vanity-mirror frame", joined)
        self.assertIn("no full-body side pose", joined)
        self.assertIn("no chest-forward posture", joined)

    def test_tsundere_weak_roles_apply_costume_swap_frame_budget(self):
        cases = [
            ("카리나 메이드 츤데레", 1202, "head_and_shoulders_crop"),
            ("윈터 간호사 츤데레", 1203, "upper_body_framing"),
            ("닝닝 경찰 츤데레", 1204, "head_and_shoulders_crop"),
            ("지젤 광부 츤데레", 1205, "head_and_shoulders_crop"),
            ("아일릿 원희 사복 여친 츤데레", 1206, "upper_body_framing"),
            ("설윤 공주 츤데레", 1207, "upper_body_framing"),
            ("유나 바니걸 츤데레", 1208, "head_and_shoulders_crop"),
        ]

        for concept, seed, expected_framing in cases:
            payload = self.run_wrapper_json(
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
            concept_payload = payload["concepts"][0]
            self.assertEqual(concept_payload["combined_forced_slots"]["subject_framing"], [expected_framing])
            joined = " ".join(payload["forward_args"])
            self.assertIn("costume-swap test", joined)
            self.assertIn("face and hands holding the caring object", joined)
            self.assertIn("restrained warmth", joined)
            self.assertIn("no full-body costume display", joined)
            self.assertIn("no chest-forward", joined)

    def test_tsundere_mid_string_role_uses_casual_girlfriend_bundle(self):
        payload = self.run_wrapper_json(
            "--concept",
            "카리나 사복 여친 츤데레",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--seed",
            "1206",
            "--plain",
            "--no-negative",
        )

        concept = payload["concepts"][0]
        self.assertEqual(concept["name"], "카리나")
        self.assertEqual(concept["role"], "사복 여친")
        self.assertEqual(concept["applied_role"], "사복 여친")
        self.assertEqual(concept["applied_mixins"], ["츤데레"])
        self.assertEqual(concept["selected_bundles"][0]["bundle_id"], "casual_lunchbox_denial")
        self.assertEqual(concept["combined_forced_slots"]["wardrobe_style"], ["faded_hoodie_sweatpants"])
        self.assertEqual(concept["combined_forced_slots"]["prop"], ["foil_wrapped_lunchbox_prop"])
        self.assertEqual(concept["combined_forced_slots"]["relational_action"], ["sliding_lunchbox_across_table"])
        self.assertEqual(concept["combined_forced_slots"]["prop_direction"], ["set_down_between_two"])
        self.assertEqual(concept["combined_forced_slots"]["location"], ["sunlit_kitchen"])
        self.assertEqual(concept["combined_forced_slots"]["mood"], ["playful_sweet_cosplay"])
        joined = " ".join(payload["forward_args"])
        self.assertIn("conservative everyday outfit", joined)
        self.assertIn("modest wrapped gift", joined)
        self.assertIn("suppressed pout", joined)
        self.assertIn("small thunk", joined)
        self.assertIn("no slumped shoulders", joined)
        self.assertIn("no listless body", joined)
        self.assertIn("no break-up melancholy", joined)
        self.assertIn("no phone-screen evidence", joined)
        forwarded_sets = [
            payload["forward_args"][index + 1]
            for index, value in enumerate(payload["forward_args"][:-1])
            if value == "--set"
        ]
        self.assertIn("wardrobe_style=faded_hoodie_sweatpants", forwarded_sets)
        self.assertNotIn("wardrobe_style=hoodie_shorts_sneakers", forwarded_sets)

    def test_tsundere_weak_roles_have_active_denial_and_anti_drift_guards(self):
        cases = [
            ("카리나 메이드 츤데레", 1202, ["tiny huff", "pursed protest", "small brusque thunk", "no demure barista smile"]),
            ("윈터 간호사 츤데레", 1203, ["pursed lecture mouth", "faint scold", "chart-tapping", "no professional bedside-manner"]),
            ("아일릿 원희 사복 여친 츤데레", 1206, ["suppressed pout", "briefly puffed cheek", "small thunk", "no listless body"]),
            ("설윤 공주 츤데레", 1207, ["courtly haughtiness", "slightly raised chin", "fan or sleeve barrier", "no demure courtly shyness"]),
        ]

        for concept, seed, required_phrases in cases:
            payload = self.run_wrapper_json(
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
            joined = " ".join(payload["forward_args"])
            self.assertIn("active rejection cue beyond gaze aversion", joined)
            self.assertIn("mouth tension", joined)
            self.assertIn("never shyly cradled", joined)
            self.assertIn("weak-role drift guard", joined)
            for phrase in required_phrases:
                self.assertIn(phrase, joined)

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
        self.assertIn(
            concept["combined_forced_slots"]["expression"][0],
            {
                "mysterious_half_smile",
                "cold_unreadable_stare",
                "calm_intense_gaze",
                "looking_away_pensive",
                "emotional_teary_eyes",
                "neutral_camera_gaze",
                "skeptical_side_eye",
            },
        )
        self.assertEqual(concept["combined_forced_slots"]["light_intensity"], ["deep_shadow_detail"])
        self.assertIn(
            concept["combined_forced_slots"]["subject_framing"][0],
            {"close_up_face_crop", "head_and_shoulders_crop", "upper_body_framing"},
        )
        self.assertEqual(len(concept["selected_bundles"]), 1)
        bundle = concept["selected_bundles"][0]
        self.assertEqual(bundle["mixin"], "얀데레")
        self.assertTrue(bundle["bundle_id"].startswith("standalone_"))
        self.assertIn("subtype", bundle)
        joined = " ".join(payload["forward_args"])
        self.assertIn("subtype-specific affect paradox", joined)
        self.assertIn("overwhelming rather than decorative", joined)
        self.assertIn("same single off-frame fictional person", joined)
        self.assertIn("no weapon use", joined)
        self.assertIn("no visible captive or victim", joined)
        self.assertIn("no minors and no sexual content", joined)
        self.assertNotIn("only when the user explicitly asks for weapon or blood symbolism", joined)

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
        self.assertEqual(concept["combined_forced_slots"]["expression"], ["mysterious_half_smile"])
        self.assertEqual(concept["combined_forced_slots"]["prop"], ["compact_mirror"])
        self.assertEqual(concept["combined_forced_slots"]["subject_framing"], ["close_up_face_crop"])
        self.assertEqual(len(concept["selected_bundles"]), 1)
        self.assertEqual(concept["selected_bundles"][0]["bundle_id"], "maid_devotion_possession")
        self.assertEqual(concept["selected_bundles"][0]["subtype"], "shrine_surveillance")
        joined = " ".join(payload["forward_args"])
        self.assertIn("the maid outfit stays clearly readable", joined)
        self.assertIn("hollow fixed half-smile", joined)
        self.assertIn("hard-shadowed empty eyes", joined)
        self.assertIn("overloaded with repeated photos", joined)
        self.assertIn("not a few decorative snapshots", joined)
        self.assertIn("possession anchor must read before cute maid cosplay", joined)
        self.assertIn("no visible blood", joined)
        self.assertIn("no weapon use", joined)
        self.assertNotIn("sheathed utility blade", joined)
        self.assertNotIn("holster grip", joined)
        self.assertNotIn("assassin persona", joined)

    def test_yandere_symbolic_weapon_request_is_explicit_and_non_operational(self):
        payload = self.run_wrapper_json(
            "--concept",
            "카리나 메이드 얀데레 칼",
            "--explain-concept",
            "--selection-mode",
            "rule",
            "--seed",
            "902",
            "--plain",
            "--no-negative",
        )

        concept = payload["concepts"][0]
        self.assertEqual(concept["name"], "카리나 칼")
        self.assertEqual(concept["role"], "메이드")
        self.assertEqual(concept["applied_mixins"], ["얀데레"])
        self.assertEqual(concept["combined_forced_slots"]["prop"], ["compact_mirror"])
        joined = " ".join(payload["forward_args"])
        self.assertIn("only when the user explicitly asks for weapon or blood symbolism", joined)
        self.assertIn("static, inert, non-instructional cue", joined)
        self.assertIn("never show use, aiming, swinging", joined)
        self.assertIn("never show use", joined)
        self.assertIn("visible victims", joined)
        self.assertNotIn("sheathed_utility_knife_prop", joined)
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
        self.assertIn(item["choices"]["costume_style"]["id"], BROAD_PRINCESS_COSTUME_IDS)
        self.assertEqual(item["choices"]["expression"]["id"], "cold_unreadable_stare")
        self.assertEqual(item["choices"]["prop"]["id"], "phoenix_hairpin_prop")
        self.assertEqual(item["choices"]["composition"]["id"], "centered_symmetry")
        self.assertEqual(item["choices"]["subject_framing"]["id"], "upper_body_framing")
        self.assertIn("Core concept lock: 설윤 공주 얀데레", item["prompt_en"])
        self.assertIn("decree confinement yandere", item["prompt_en"])
        self.assertIn("royal possession made legal and ritual", item["prompt_en"])
        self.assertIn("sealed royal decree", item["prompt_en"])
        self.assertIn("empty gilded birdcage", item["prompt_en"])
        self.assertIn("phoenix hairpin remains a courtly possession marker, not a weapon cue", item["prompt_en"])
        self.assertIn("preserve the selected royal princess register and visible regalia", item["prompt_en"])
        self.assertIn("no weapon use", item["prompt_en"])
        self.assertIn("no blood", item["prompt_en"])
        self.assertIn("no harmed person", item["prompt_en"])
        self.assertIn("no captive shown", item["prompt_en"])

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
                "expression": ["mysterious_half_smile"],
                "prop": ["compact_mirror"],
                "action": ["doorframe_shadow_watch"],
                "composition": ["frame_within_frame"],
                "subject_framing": ["close_up_face_crop"],
            },
            "간호사": {
                "expression": ["cold_unreadable_stare"],
                "prop": ["logo_board_prop"],
                "action": ["doorframe_shadow_watch"],
                "location": ["hospital_corridor"],
                "lighting": ["fluorescent"],
                "mood": ["quiet_dread"],
                "composition": ["frame_within_frame"],
                "subject_framing": ["upper_body_framing"],
            },
            "경찰": {
                "expression": ["cold_unreadable_stare"],
                "prop": ["instant_photo_stack"],
                "action": ["holding_story_prop"],
                "composition": ["cctv_corner_frame"],
                "subject_framing": ["head_and_shoulders_crop"],
            },
            "광부": {
                "expression": ["calm_intense_gaze"],
                "prop": ["instant_photo_stack"],
                "location": ["underground_mine_tunnel_set"],
                "lighting": ["single_flashlight_beam"],
                "composition": ["medium_close"],
                "subject_framing": ["head_and_shoulders_crop"],
            },
            "사복 여친": {
                "expression": ["emotional_teary_eyes"],
                "wardrobe_style": ["faded_hoodie_sweatpants"],
                "prop": ["clear_case_smartphone"],
                "action": ["checking_phone"],
                "composition": ["over_shoulder_phone_screen"],
                "subject_framing": ["close_up_face_crop"],
            },
            "공주": {
                "expression": ["cold_unreadable_stare"],
                "prop": ["phoenix_hairpin_prop"],
                "action": ["holding_story_prop"],
                "location": ["royal_princess_chamber"],
                "composition": ["centered_symmetry"],
                "subject_framing": ["upper_body_framing"],
            },
            "바니걸": {
                "expression": ["skeptical_side_eye"],
                "prop": ["logo_board_prop"],
                "action": ["standing_backstage"],
                "location": ["makeup_vanity"],
                "composition": ["frame_within_frame"],
                "subject_framing": ["close_up_face_crop"],
            },
        }
        selected_bundle_ids = set()
        selected_locations = set()
        anchor_tuples = set()
        selected_props = set()
        role_props = []
        selected_expressions = set()
        selected_compositions = set()
        selected_subtypes = set()
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
            self.assertTrue(selected_bundle["subtype"])
            selected_bundle_ids.add(selected_bundle["bundle_id"])
            selected_subtypes.add(selected_bundle["subtype"])
            selected_locations.add(concept_payload["combined_forced_slots"]["location"][0])
            forced_slots = concept_payload["combined_forced_slots"]
            selected_expressions.add(forced_slots["expression"][0])
            selected_compositions.add(forced_slots["composition"][0])
            anchor_tuples.add(
                (
                    forced_slots.get("prop", [""])[0],
                    forced_slots.get("action", [""])[0],
                    forced_slots.get("composition", [""])[0],
                )
            )
            role_prop = forced_slots.get("prop", [""])[0]
            selected_props.add(role_prop)
            role_props.append(role_prop)
            role = concept_payload["role"]
            for slot, ids in expected_slots_by_role[role].items():
                self.assertEqual(forced_slots[slot], ids)

        self.assertGreaterEqual(len(selected_bundle_ids), 7)
        self.assertGreaterEqual(len(selected_locations), 5)
        self.assertGreaterEqual(len(anchor_tuples), 6)
        self.assertGreaterEqual(len(selected_props), 4)
        self.assertGreaterEqual(len(selected_expressions), 5)
        self.assertGreaterEqual(len(selected_compositions), 5)
        self.assertGreaterEqual(len(selected_subtypes), 7)
        self.assertLessEqual(sum(1 for prop in role_props if prop == "instant_photo_stack"), 2)

    def test_yandere_weak_roles_force_possession_anchors_and_safe_framing(self):
        cases = [
            (
                "닝닝 경찰 얀데레",
                904,
                {
                    "prop": "instant_photo_stack",
                    "action": "holding_story_prop",
                    "composition": "cctv_corner_frame",
                    "subject_framing": "head_and_shoulders_crop",
                    "phrases": [
                        "authority-protection inversion",
                        "ceiling-corner CCTV",
                        "movement arrows",
                        "do not make red thread the primary cue",
                        "never an ordinary noir police portrait",
                    ],
                },
            ),
            (
                "윈터 간호사 얀데레",
                903,
                {
                    "expression": "cold_unreadable_stare",
                    "prop": "logo_board_prop",
                    "action": "doorframe_shadow_watch",
                    "lighting": "fluorescent",
                    "composition": "frame_within_frame",
                    "subject_framing": "upper_body_framing",
                    "phrases": [
                        "caretaking surveillance yandere",
                        "open-eyed clinical watchfulness",
                        "clinical chart or care-record board",
                        "costume were replaced",
                        "do not let a bouquet or phone selfie",
                        "no syringe",
                    ],
                },
            ),
            (
                "지젤 광부 얀데레",
                2404,
                {
                    "expression": "skeptical_side_eye",
                    "prop": "sealed_mission_envelope_prop",
                    "action": "holding_story_prop",
                    "composition": "frame_within_frame",
                    "subject_framing": "upper_body_framing",
                    "phrases": [
                        "sealed route document",
                        "controlled access",
                        "avoid a broad photo wall",
                        "miner workwear were replaced",
                    ],
                },
            ),
            (
                "아일릿 원희 사복 여친 얀데레",
                906,
                {
                    "wardrobe_style": "faded_hoodie_sweatpants",
                    "prop": "clear_case_smartphone",
                    "action": "checking_phone",
                    "composition": "over_shoulder_phone_screen",
                    "subject_framing": "close_up_face_crop",
                    "phrases": [
                        "conservative everyday wardrobe",
                        "clear-case smartphone is the dominant possession anchor",
                        "unread-message wall",
                        "unanswered-call grid",
                        "phone-screen evidence",
                        "no identifiable target",
                        "no minors",
                        "no pin-up, no full-body display, no thirst-trap selfie",
                    ],
                },
            ),
            (
                "설윤 공주 얀데레",
                906,
                {
                    "expression": "cold_unreadable_stare",
                    "prop": "phoenix_hairpin_prop",
                    "action": "holding_story_prop",
                    "composition": "centered_symmetry",
                    "subject_framing": "upper_body_framing",
                    "phrases": [
                        "decree confinement yandere",
                        "royal possession made legal and ritual",
                        "sealed royal decree",
                        "empty gilded birdcage",
                        "not a weapon cue",
                    ],
                },
            ),
            (
                "유나 바니걸 얀데레",
                908,
                {
                    "expression": "skeptical_side_eye",
                    "prop": "logo_board_prop",
                    "action": "standing_backstage",
                    "composition": "frame_within_frame",
                    "subject_framing": "close_up_face_crop",
                    "phrases": [
                        "performance log possession yandere",
                        "booking board and mirror-edge notes read first",
                        "reservation log or performance schedule",
                        "single-name reservation log",
                        "repeated reservation times",
                        "avoid a broad wall of photos",
                        "no full-body stage display",
                    ],
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
            if "expression" in expected:
                self.assertEqual(item["choices"]["expression"]["id"], expected["expression"])
            self.assertEqual(item["choices"]["prop"]["id"], expected["prop"])
            if "action" in expected:
                self.assertEqual(item["choices"]["action"]["id"], expected["action"])
            if "lighting" in expected:
                self.assertEqual(item["choices"]["lighting"]["id"], expected["lighting"])
            if "wardrobe_style" in expected:
                self.assertEqual(item["choices"]["wardrobe_style"]["id"], expected["wardrobe_style"])
            self.assertEqual(item["choices"]["composition"]["id"], expected["composition"])
            self.assertEqual(item["choices"]["subject_framing"]["id"], expected["subject_framing"])
            self.assertIn("subtype:", item["prompt_en"])
            self.assertIn("no weapon", item["prompt_en"])
            self.assertIn("no visible captive or victim", item["prompt_en"])
            self.assertNotIn("navy bomber jacket with a casual mini skirt", item["prompt_en"])
            self.assertNotIn("clean blazer and tailored trousers", item["prompt_en"])
            for phrase in expected["phrases"]:
                self.assertIn(phrase, item["prompt_en"])

    def test_yandere_weak_role_anchors_survive_costume_swap_proxy(self):
        cases = [
            (
                "윈터 간호사 얀데레",
                903,
                {
                    "prop": "logo_board_prop",
                    "action": "doorframe_shadow_watch",
                    "composition": "frame_within_frame",
                    "phrase": "costume were replaced with plain clothes",
                },
            ),
            (
                "지젤 광부 얀데레",
                2404,
                {
                    "prop": "sealed_mission_envelope_prop",
                    "action": "holding_story_prop",
                    "composition": "frame_within_frame",
                    "phrase": "miner workwear were replaced with plain clothes",
                },
            ),
            (
                "유나 바니걸 얀데레",
                908,
                {
                    "prop": "logo_board_prop",
                    "action": "standing_backstage",
                    "composition": "frame_within_frame",
                    "phrase": "costume were swapped for plain clothes",
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
                "--set",
                "wardrobe_style=clean_blazer_trousers",
            )[0]

            self.assertEqual(item["choices"]["prop"]["id"], expected["prop"])
            self.assertEqual(item["choices"]["action"]["id"], expected["action"])
            self.assertEqual(item["choices"]["composition"]["id"], expected["composition"])
            self.assertIn(expected["phrase"], item["prompt_en"])

    def test_yandere_drift_risk_roles_have_seed_selectable_variants(self):
        seeds = [101, 202, 303, 404, 505]
        for role in ("간호사", "광부", "공주", "바니걸"):
            subtypes = set()
            props = set()
            bundle_ids = set()
            for seed in seeds:
                explanation = self.run_wrapper_json(
                    "--concept",
                    f"테스트 {role} 얀데레",
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
                self.assertEqual(concept_payload["applied_mixins"], ["얀데레"])
                self.assertFalse(selected_bundle["bundle_id"].startswith("shared_"))
                self.assertFalse(selected_bundle["bundle_id"].startswith("standalone_"))
                subtypes.add(selected_bundle["subtype"])
                bundle_ids.add(selected_bundle["bundle_id"])
                props.add(concept_payload["combined_forced_slots"]["prop"][0])

            self.assertGreaterEqual(len(subtypes), 2, role)
            self.assertGreaterEqual(len(bundle_ids), 2, role)
            if role == "바니걸":
                self.assertEqual(props, {"logo_board_prop"}, role)
            else:
                self.assertGreaterEqual(len(props), 2, role)

    def test_yandere_recent_role_batch_reduces_photo_wall_convergence(self):
        cases = [
            ("카리나 메이드 얀데레", 2401),
            ("윈터 간호사 얀데레", 2402),
            ("닝닝 경찰 얀데레", 2403),
            ("지젤 광부 얀데레", 2404),
            ("아일릿 원희 사복 여친 얀데레", 2405),
            ("설윤 공주 얀데레", 2406),
            ("유나 바니걸 얀데레", 2407),
        ]
        props = []
        bundle_ids = []
        prompt_texts = []
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
            props.append(item["choices"]["prop"]["id"])
            bundle_ids.append(explanation["concepts"][0]["selected_bundles"][0]["bundle_id"])
            prompt_texts.append(item["prompt_en"])

        self.assertLessEqual(sum(1 for prop in props if prop == "instant_photo_stack"), 2)
        self.assertLessEqual(sum(1 for prop in props if prop == "clear_case_smartphone"), 3)
        institutional_props = {
            "logo_board_prop",
            "sealed_mission_envelope_prop",
            "transparent_dome_umbrella",
            "holographic_screen_prop",
        }
        self.assertGreaterEqual(sum(1 for prop in props if prop in institutional_props), 2)
        self.assertGreaterEqual(len(set(props)), 4)
        self.assertIn("nurse_chart_doorway_surveillance", bundle_ids)
        self.assertIn("miner_route_lock_niche", bundle_ids)
        self.assertIn("princess_decree_birdcage_possession", bundle_ids)
        self.assertTrue(any("costume were replaced" in prompt for prompt in prompt_texts))
        self.assertTrue(any("booking board" in prompt for prompt in prompt_texts))
        self.assertTrue(
            any("avoid a broad photo wall" in prompt for prompt in prompt_texts),
            "At least one drift-risk role should explicitly avoid broad photo-wall convergence.",
        )

    def test_yandere_photo_wall_requires_overwhelming_density(self):
        item = self.run_wrapper_json(
            "--concept",
            "얀데레",
            "--selection-mode",
            "rule",
            "--seed",
            "901",
            "--lang",
            "en",
            "--no-negative",
            "--include-choices",
        )[0]

        self.assertEqual(item["choices"]["composition"]["id"], "extreme_wide_environmental")
        self.assertEqual(item["choices"]["location"]["id"], "anime_poster_wall_interior")
        self.assertIn("environment is the main evidence", item["prompt_en"])
        self.assertIn("wall is overrun with same-person photos", item["prompt_en"])
        self.assertIn("date labels", item["prompt_en"])
        self.assertIn("route maps", item["prompt_en"])
        self.assertIn("red-string paths", item["prompt_en"])
        self.assertIn("not a decorative poster room or photographer studio", item["prompt_en"])

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
        self.assertTrue(bundle["aspect"])
        self.assertIn("weight", bundle)
        self.assertEqual(concept["combined_forced_slots"]["costume_style"], ["police_uniform_costume"])
        for slot in bundle["set"]:
            self.assertEqual(concept["combined_forced_slots"][slot], [bundle["set"][slot]])
        self.assertEqual(concept["combined_forced_slots"]["expression"], ["cold_unreadable_stare"])
        self.assertEqual(concept["combined_forced_slots"]["light_type"], ["narrow_spotlight"])
        self.assertEqual(concept["combined_forced_slots"]["light_intensity"], ["deep_shadow_detail"])
        self.assertEqual(concept["combined_forced_slots"]["color"], ["desaturated_cold_blue"])
        self.assertIn("costume_style=police_uniform_costume", payload["forward_args"])
        for slot in bundle["set"]:
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

    def test_assassin_viewpoint_presets_tags_and_cliche_weights_registered(self):
        slots = self.data["slots"]
        preset_ids = {preset["id"] for preset in self.data["presets"]}
        family_ids = {family["id"] for family in self.data.get("preset_families", [])}
        metadata = self.data["semantic_metadata"]

        self.assertTrue(ASSASSIN_VIEWPOINT_PRESET_IDS.issubset(preset_ids))
        self.assertTrue(ASSASSIN_VIEWPOINT_FAMILY_IDS.issubset(family_ids))
        for slot, expected_ids in ASSASSIN_VIEWPOINT_TAG_IDS.items():
            actual_ids = {entry["id"] for entry in slots[slot]}
            self.assertTrue(expected_ids.issubset(actual_ids), slot)

        cliche_weights = metadata["cliche_weights"]
        self.assertLess(cliche_weights["prop"]["black_leather_gloves_prop"], 1.0)
        self.assertLess(cliche_weights["prop"]["single_playing_card_calling_card_prop"], 1.0)
        self.assertLess(cliche_weights["composition"]["cctv_corner_frame"], 1.0)
        self.assertLess(cliche_weights["action"]["doorframe_shadow_watch"], 1.0)

    def test_assassin_viewpoint_bundles_expose_aspects_and_extended_slots(self):
        recipes = json.loads((SKILL_DIR / "assets" / "concept_recipes.json").read_text(encoding="utf-8"))
        assassin = recipes["mixins"]["암살자"]
        bundle_ids = {bundle["id"] for bundle in assassin["bundles"]}
        aspects = {bundle.get("aspect") for bundle in assassin["bundles"]}
        override_slots = set(assassin["bundle_override_slots"])

        self.assertTrue(ASSASSIN_VIEWPOINT_BUNDLE_IDS.issubset(bundle_ids))
        self.assertGreaterEqual(len(aspects), 10)
        for slot in ("camera_direction", "capture_context", "lens", "wearable_accessory"):
            self.assertIn(slot, override_slots)
        self.assertEqual(
            recipes["mixin_diversity_policy"]["암살자"]["min_distinct_aspects_per_batch"],
            5,
        )

    def test_assassin_recent_role_batch_covers_viewpoint_aspects(self):
        cases = [
            ("카리나 메이드 암살자", 7401),
            ("윈터 간호사 암살자", 7402),
            ("닝닝 경찰 암살자", 7403),
            ("지젤 광부 암살자", 7404),
            ("아일릿 원희 사복 여친 암살자", 7405),
            ("설윤 공주 암살자", 7406),
            ("유나 바니걸 암살자", 7407),
        ]
        bundle_ids = set()
        aspects = set()
        props = set()
        compositions = set()
        extended_slot_hits = set()

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
            selected_bundle = explanation["concepts"][0]["selected_bundles"][0]
            bundle_ids.add(selected_bundle["bundle_id"])
            aspects.add(selected_bundle["aspect"])
            props.add(selected_bundle["set"]["prop"])
            compositions.add(selected_bundle["set"]["composition"])
            extended_slot_hits.update(
                slot for slot in ("camera_direction", "capture_context", "lens", "wearable_accessory")
                if slot in selected_bundle["set"]
            )

        self.assertGreaterEqual(len(bundle_ids), 7)
        self.assertGreaterEqual(len(aspects), 5)
        self.assertGreaterEqual(len(props), 5)
        self.assertGreaterEqual(len(compositions), 5)
        self.assertGreaterEqual(len(extended_slot_hits), 3)

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
        self.assertTrue(
            "underground mine tunnel set" in item["prompt_en"]
            or "mine worksite rest stop" in item["prompt_en"]
        )
        self.assertIn("not an exact likeness", item["prompt_en"])
        self.assertIn("지젤 광부", item["provenance"]["concept_lock"])
        self.assertTrue(
            any("coal miner workwear" in requirement for requirement in item["provenance"]["additional_requirements"])
        )
        self.assertIn("costume_style=miner_workwear_hard_hat", item["provenance"]["argv"])
        self.assertIn("location=underground_mine_tunnel_set,mine_rest_stop", item["provenance"]["argv"])
        self.assertIn("--concept-lock", item["provenance"]["argv"])
        self.assertIn("--additional-requirement", item["provenance"]["argv"])

    def test_candidate_pack_preserves_unmatched_concept_intents(self):
        payload = self.run_wrapper_json(
            "--concept",
            "카리나 메이드 드래곤 고양이손 달린 흡혈귀",
            "--selection-mode",
            "rule",
            "--seed",
            "701",
            "--emit-candidate-pack",
        )

        pack = payload[0]
        self.assertRegex(pack["pack_id"], r"^[0-9a-f]{16}$")
        self.assertNotIn("prompt_en", pack)
        self.assertEqual(
            {
                "pack_id",
                "contract_version",
                "intent_contract",
                "mandatory_intents",
                "uncovered_intents",
                "presets",
                "slots",
                "quality_profile",
                "concept_axes",
                "scene_contract",
                "render_contract",
                "character_grammar",
                "evidence_budget",
                "photographic_integration",
                "visual_proposition",
                "photographic_craft",
                "artistic_final_touch",
                "authorial_composition",
                "hybrid_augmentation",
                "motif_budget",
                "preset_reference",
                "masked_buckets",
                "open_slots",
                "authorial_open_slots",
                "template_echo_risk",
                "role_scene_policy",
                "species_family",
                "safety",
                "concept_gates",
                "diversity_state",
                "coverage",
                "conflicts",
                "negative_en",
                "provenance",
            },
            set(pack.keys()),
        )
        self.assertFalse(pack["render_contract"]["enabled"])
        self.assertFalse(pack["evidence_budget"]["enabled"])
        intent_texts = {item["text"] for item in pack["mandatory_intents"]}
        self.assertTrue({"카리나", "메이드", "드래곤", "고양이손", "흡혈귀"} <= intent_texts)
        uncovered = {item["text"] for item in pack["uncovered_intents"]}
        self.assertIn("드래곤", uncovered)
        self.assertIn("고양이손", uncovered)
        integration = pack["photographic_integration"]
        self.assertTrue(integration["enabled"])
        self.assertEqual(
            integration["selection_mode"],
            "agent_authored_non_preferential",
        )
        self.assertTrue(integration["category_candidates"])
        self.assertNotIn("active_axes", integration)
        self.assertNotIn("required_categories", integration)
        self.assertIn("facets", pack["quality_profile"])
        self.assertEqual(pack["quality_profile"]["profile_id"], "authorial")
        self.assertNotIn("quality_profile", integration)
        proposition = pack["visual_proposition"]
        self.assertTrue(proposition["enabled"])
        self.assertNotIn("quality_profile", proposition)
        self.assertNotIn("register", proposition)
        self.assertTrue(proposition["core_candidates"])
        self.assertTrue(proposition["tension_candidates"])
        craft = pack["photographic_craft"]
        self.assertTrue(craft["enabled"])
        self.assertNotIn("source", craft)
        self.assertEqual(craft["selection_mode"], "agent_authored_optional")
        self.assertNotIn("quality_profile", craft)
        self.assertNotIn("top_strategy", craft)
        self.assertTrue(craft["dimension_candidates"])
        self.assertEqual(
            {"shot_intent", "light_provenance", "frame_hierarchy", "decisive_moment", "environment_consequence"},
            {dimension["dimension"] for dimension in craft["dimension_candidates"]},
        )
        final_touch = pack["artistic_final_touch"]
        self.assertFalse(final_touch["enabled"])
        self.assertNotIn("profile_id", final_touch)
        self.assertEqual(pack["contract_version"], "photo-candidate-pack/v4")
        self.assertNotIn("argv", pack["provenance"])
        self.assertNotIn("preset_id", pack["provenance"])
        self.assertNotIn("selected_motifs", pack["motif_budget"])
        adult = pack["hybrid_augmentation"]["adult_appeal"]
        self.assertTrue(adult["enabled"])
        self.assertEqual(adult["activation_source"], "skill_default")
        self.assertEqual(adult["axes"]["sensual_editorial"]["intensity"], 1)
        self.assertEqual(adult["axes"]["fetish_fashion"]["intensity"], 0)
        self.assertEqual(pack["safety"]["status"], "pass")
        self.assertFalse(pack["safety"]["requires_user_approval"])
        self.assertLessEqual(len(pack["presets"]), 4)
        total_slot_candidates = 0
        for slot, slot_payload in pack["slots"].items():
            candidates = slot_payload["candidates"]
            total_slot_candidates += len(candidates)
            expected_limit = 4 if slot_payload["role"] == "core" else 2
            self.assertLessEqual(len(candidates), expected_limit)
            self.assertEqual(slot_payload["candidate_order"], "seed_shuffled_non_preferential")
            self.assertNotIn("selected", slot_payload)
            for candidate in candidates:
                self.assertFalse(
                    {"selected_by_sampler", "probability", "weight", "score", "scores"}
                    & set(candidate)
                )
        self.assertLessEqual(total_slot_candidates, 64)

    def test_candidate_pack_profiles_photographic_integration_for_cathedral(self):
        payload = self.run_wrapper_json(
            "--preset",
            "stained_glass_cathedral_portrait",
            "--selection-mode",
            "rule",
            "--seed",
            "701",
            "--emit-candidate-pack",
            "--candidate-pack-version",
            "v3",
        )

        pack = payload[0]
        integration = pack["photographic_integration"]
        quality_profile = pack["quality_profile"]
        self.assertEqual(integration["profile_id"], "axis_composite_photo_integration")
        self.assertEqual(integration["source"], "quality_layers_axis_composite")
        self.assertEqual(integration["quality_profile"], quality_profile)
        self.assertIn("human", quality_profile["facets"].get("subject_kind", []))
        active_axes = {axis["id"] for axis in integration["active_axes"]}
        self.assertTrue({"sacred_or_monumental_interior", "colored_or_mixed_light", "person_presence"} <= active_axes)
        person_axis = next(axis for axis in integration["active_axes"] if axis["id"] == "person_presence")
        self.assertIn("subject_kind:human", person_axis["matched_facets"])
        self.assertIn("subject_kind:human", integration["matched_facets"])
        colored_axis = next(axis for axis in integration["active_axes"] if axis["id"] == "colored_or_mixed_light")
        self.assertIn("stained glass", colored_axis["matched_terms"])
        self.assertTrue({"environment_binding", "optical_depth", "human_trace"} <= set(integration["required_categories"]))
        self.assertIn("environment_binding", integration["suggested_phrases"])
        self.assertIn("optical_depth", integration["suggested_phrases"])
        self.assertIn(
            "parallax",
            integration["category_terms"]["optical_depth"],
        )
        self.assertIn(
            "native material identity",
            integration["category_terms"]["material_trace"],
        )
        self.assertIn("centered beauty headshot pasted over a scenic background", integration["anti_patterns"])
        self.assertIn(
            "a visible effect shell or flat image-plane slice that ignores local material identity, depth, and occlusion",
            integration["anti_patterns"],
        )

    def test_candidate_pack_composes_quality_axes_across_domains(self):
        cases = [
            (
                ("--concept", "kpop 여자 아이돌 페르시안 고양이 일상복 실내"),
                {"person_presence", "animal_presence", "interior_environment"},
            ),
            (
                ("--concept", "사과 펠트 동화느낌의 배경 kpop 아이돌 네코미미 상큼함"),
                {"person_presence", "handmade_or_miniature_set", "object_or_product_presence"},
            ),
            (
                ("--concept", "스테이지에서 공연하는 케이팝 여성 아이돌 전광판 역동적 살짝 땀이 맺힌 활짝 웃음"),
                {"person_presence", "performance_stage_environment", "colored_or_mixed_light"},
            ),
            (
                ("--preset", "product_packshot_white_sweep"),
                {"object_or_product_presence", "interior_environment"},
            ),
        ]
        axis_sets = []
        for args, expected_axes in cases:
            payload = self.run_wrapper_json(
                *args,
                "--selection-mode",
                "rule",
                "--seed",
                "715",
                "--emit-candidate-pack",
                "--candidate-pack-version",
                "v3",
            )
            pack = payload[0]
            integration = pack["photographic_integration"]
            active_axes = {axis["id"] for axis in integration["active_axes"]}
            axis_sets.append(tuple(sorted(active_axes)))
            self.assertEqual(integration["source"], "quality_layers_axis_composite")
            self.assertEqual(integration["quality_profile"], pack["quality_profile"])
            self.assertTrue(
                integration["matched_facets"] or any(axis["matched_facets"] for axis in integration["active_axes"])
            )
            self.assertTrue(expected_axes <= active_axes)
            self.assertTrue({"environment_binding", "optical_depth"} <= set(integration["required_categories"]))
            self.assertGreaterEqual(len(active_axes), 3)

            proposition = pack["visual_proposition"]
            self.assertEqual(proposition["source"], "quality_layers_narrative_core_and_concept_tension_slots")
            self.assertEqual(proposition["quality_profile"], pack["quality_profile"])
            self.assertIn("evidence", proposition["category_terms"])
            self.assertTrue(proposition["core_candidates"])
            self.assertTrue(proposition["tension_candidates"])

            craft = pack["photographic_craft"]
            self.assertEqual(craft["selection_mode"], "facet_only")
            self.assertEqual(craft["quality_profile"], pack["quality_profile"])
            self.assertTrue(craft["prompt_guidance_en"])
            self.assertNotIn("matched_terms", craft)

        self.assertEqual(len(set(axis_sets)), len(cases))

    def test_candidate_pack_photographic_craft_degrades_to_generic_for_empty_facets(self):
        data = {
            "facet_vocab": self.data.get("facet_vocab", {}),
            self.generator.QUALITY_LAYERS_DATA_KEY: self.generator.load_quality_layers(QUALITY_LAYERS_PATH),
        }

        craft = self.generator.candidate_pack_photographic_craft(
            data,
            {"source": "test_empty", "facets": {}, "matched_uncovered_intent_entries": []},
        )

        self.assertTrue(craft["enabled"])
        self.assertEqual(craft["selection_mode"], "facet_only")
        self.assertEqual(craft["matched_facets"], [])
        self.assertEqual(craft["top_strategy"]["id"], "structure_led")
        self.assertEqual(craft["prompt_dimension_ids"], ["frame_hierarchy", "shot_intent"])
        self.assertTrue(craft["prompt_guidance_en"])
        self.assertEqual(
            {"shot_intent", "light_provenance", "frame_hierarchy", "decisive_moment", "environment_consequence"},
            {dimension["id"] for dimension in craft["active_dimensions"]},
        )

    def test_candidate_pack_photographic_craft_holdout_generalizes_without_example_nouns(self):
        cases = [
            ("--concept", "새벽 산 능선 풍경 안개 역광"),
            ("--preset", "product_packshot_white_sweep"),
            ("--concept", "비 오는 거리 다큐멘터리 사진 우산 없이 걷는 사람"),
            ("--concept", "테이블 위 음식 정물 사진 자연광"),
            ("--concept", "현대 건축 실내 넓은 공간 대칭 구도"),
        ]
        blocked_terms = {"kpop", "idol", "cathedral", "cat", "felt", "apple", "stage", "고양이", "성당", "사과", "펠트", "무대"}
        strategies = []
        matched_facet_sets = []
        for args in cases:
            payload = self.run_wrapper_json(
                *args,
                "--selection-mode",
                "rule",
                "--seed",
                "731",
                "--emit-candidate-pack",
                "--candidate-pack-version",
                "v3",
            )
            craft = payload[0]["photographic_craft"]
            strategies.append(craft["top_strategy"]["id"])
            matched_facet_sets.append(tuple(craft["matched_facets"]))
            craft_without_profile = {key: value for key, value in craft.items() if key != "quality_profile"}
            craft_blob = json.dumps(craft_without_profile, ensure_ascii=False).lower()
            ascii_tokens = set(re.findall(r"[a-z0-9][a-z0-9-]*", craft_blob))
            for blocked in blocked_terms:
                if re.search(r"[A-Za-z0-9]", blocked):
                    self.assertNotIn(blocked, ascii_tokens)
                else:
                    self.assertNotIn(blocked, craft_blob)
            self.assertTrue(craft["prompt_guidance_en"])
            self.assertTrue(craft["active_dimensions"])

        self.assertGreaterEqual(len(set(strategies)), 2)
        self.assertGreaterEqual(len(set(matched_facet_sets)), 2)

    def test_candidate_pack_exposes_visual_proposition_layer(self):
        payload = self.run_wrapper_json(
            "--concept",
            "도시에서 혼자 늦은 밤 돌아오는 사람",
            "--selection-mode",
            "rule",
            "--seed",
            "715",
            "--emit-candidate-pack",
            "--candidate-pack-version",
            "v3",
        )

        pack = payload[0]
        proposition = pack["visual_proposition"]
        self.assertEqual(proposition["source"], "quality_layers_narrative_core_and_concept_tension_slots")
        self.assertEqual(proposition["quality_profile"], pack["quality_profile"])
        self.assertEqual(proposition["subject_class"], "person")
        self.assertIn("person", {subject["id"] for subject in proposition["subject_classes"]})
        person_class = next(subject for subject in proposition["subject_classes"] if subject["id"] == "person")
        self.assertIn("subject_kind:human", person_class["matched_facets"])
        self.assertIn(proposition["register"], {"understated", "charged"})
        core_ids = {candidate["entry_id"] for candidate in proposition["core_candidates"]}
        tension_ids = {candidate["entry_id"] for candidate in proposition["tension_candidates"]}
        self.assertTrue(core_ids)
        self.assertTrue(tension_ids)
        self.assertEqual(proposition["audit_categories"], ["narrative_core", "concept_tension", "evidence"])
        self.assertIn("evidence", proposition["category_terms"])
        self.assertNotIn("visual_argument", proposition["category_terms"])

    def test_candidate_pack_uses_object_facets_before_context_term_fallback(self):
        payload = self.run_wrapper_json(
            "--preset",
            "product_packshot_white_sweep",
            "--selection-mode",
            "rule",
            "--seed",
            "715",
            "--emit-candidate-pack",
            "--candidate-pack-version",
            "v3",
        )

        pack = payload[0]
        integration = pack["photographic_integration"]
        active_axes = {axis["id"] for axis in integration["active_axes"]}
        self.assertIn("object_or_product_presence", active_axes)
        self.assertIn("interior_environment", active_axes)
        self.assertNotIn("person_presence", active_axes)
        object_axis = next(axis for axis in integration["active_axes"] if axis["id"] == "object_or_product_presence")
        self.assertTrue(
            {"subject_kind:object", "subject_kind:food"} & set(object_axis["matched_facets"]),
            object_axis,
        )
        proposition = pack["visual_proposition"]
        self.assertEqual(proposition["subject_class"], "object_scene")
        self.assertEqual(proposition["register"], "observational")

    def test_dictionary_validator_rejects_unknown_quality_layer_facet_match(self):
        quality_layers = json.loads(QUALITY_LAYERS_PATH.read_text(encoding="utf-8"))
        quality_layers["photographic_integration"]["axes"][0]["facet_match"] = {
            "subject_kind": ["not_a_subject_kind"]
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            quality_layers_path = Path(tmpdir) / "photo_prompt_quality_layers.json"
            quality_layers_path.write_text(json.dumps(quality_layers, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(VALIDATOR_PATH), "--quality-layers", str(quality_layers_path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unknown value not_a_subject_kind", result.stderr)

    def test_dictionary_validator_rejects_photographic_craft_terms_field(self):
        quality_layers = json.loads(QUALITY_LAYERS_PATH.read_text(encoding="utf-8"))
        quality_layers["photographic_craft"]["dimensions"][0]["terms"] = ["cathedral"]
        with tempfile.TemporaryDirectory() as tmpdir:
            quality_layers_path = Path(tmpdir) / "photo_prompt_quality_layers.json"
            quality_layers_path.write_text(json.dumps(quality_layers, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(VALIDATOR_PATH), "--quality-layers", str(quality_layers_path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("photographic_craft.dimensions[0].terms: not allowed", result.stderr)

    def test_dictionary_validator_rejects_retired_runtime_metadata(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            asset_dir = TAGS_PATH.parent
            temporary_assets = Path(tmpdir)
            filenames = [
                TAGS_PATH.name,
                *self.generator.RESEARCH_EXTENSION_FILENAMES,
            ]
            for filename in filenames:
                source = asset_dir / filename
                if source.exists():
                    (temporary_assets / filename).write_bytes(source.read_bytes())
            extension_path = temporary_assets / "photo_prompt_subculture_extension.json"
            extension = json.loads(extension_path.read_text(encoding="utf-8"))
            extension["authorship_basis"] = ["retired_test_value"]
            extension_path.write_text(
                json.dumps(extension, ensure_ascii=False),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(VALIDATOR_PATH),
                    "--tags",
                    str(temporary_assets / TAGS_PATH.name),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "authorship_basis: retired runtime metadata key is not allowed",
            result.stderr,
        )

    def test_dictionary_validator_rejects_retired_quality_source_traces(self):
        quality_layers = json.loads(QUALITY_LAYERS_PATH.read_text(encoding="utf-8"))
        quality_layers["photographic_craft"]["source"] = "legacy_trace"
        quality_layers["artistic_final_touch"]["source"] = "legacy_trace"
        with tempfile.TemporaryDirectory() as tmpdir:
            quality_layers_path = Path(tmpdir) / "photo_prompt_quality_layers.json"
            quality_layers_path.write_text(
                json.dumps(quality_layers, ensure_ascii=False),
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(VALIDATOR_PATH), "--quality-layers", str(quality_layers_path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("photographic_craft.source: retired nonfunctional trace", result.stderr)
        self.assertIn("artistic_final_touch.source: retired nonfunctional trace", result.stderr)

    def test_dictionary_validator_rejects_unknown_photographic_craft_facet_match(self):
        quality_layers = json.loads(QUALITY_LAYERS_PATH.read_text(encoding="utf-8"))
        quality_layers["photographic_craft"]["dimensions"][0]["refinements"][0]["facet_match"] = {
            "subject_kind": ["not_a_subject_kind"]
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            quality_layers_path = Path(tmpdir) / "photo_prompt_quality_layers.json"
            quality_layers_path.write_text(json.dumps(quality_layers, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(VALIDATOR_PATH), "--quality-layers", str(quality_layers_path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("photographic_craft.dimensions[0].refinements[0].facet_match.subject_kind: unknown value not_a_subject_kind", result.stderr)

    def test_dictionary_validator_rejects_unknown_quality_profile_guards(self):
        cases = [
            (
                lambda quality: quality["photographic_integration"]["axes"][0].update(
                    {"profile_match": ["not_a_quality_profile"]}
                ),
                "photographic_integration.axes[0].profile_match: unknown quality profile not_a_quality_profile",
            ),
            (
                lambda quality: quality["photographic_craft"]["dimensions"][0]["refinements"][0].update(
                    {"profile_match": ["not_a_quality_profile"]}
                ),
                "photographic_craft.dimensions[0].refinements[0].profile_match: unknown quality profile not_a_quality_profile",
            ),
            (
                lambda quality: quality["photographic_craft"]["strategies"][0].update(
                    {"profile_match": ["not_a_quality_profile"]}
                ),
                "photographic_craft.strategies[0].profile_match: unknown quality profile not_a_quality_profile",
            ),
        ]
        for mutate, expected in cases:
            with self.subTest(expected=expected):
                quality_layers = json.loads(QUALITY_LAYERS_PATH.read_text(encoding="utf-8"))
                mutate(quality_layers)
                with tempfile.TemporaryDirectory() as tmpdir:
                    quality_layers_path = Path(tmpdir) / "photo_prompt_quality_layers.json"
                    quality_layers_path.write_text(
                        json.dumps(quality_layers, ensure_ascii=False),
                        encoding="utf-8",
                    )
                    result = subprocess.run(
                        [sys.executable, str(VALIDATOR_PATH), "--quality-layers", str(quality_layers_path)],
                        cwd=ROOT,
                        text=True,
                        capture_output=True,
                        check=False,
                    )

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected, result.stderr)

    def test_artistic_touch_is_profile_specific_instead_of_global(self):
        payload = self.run_wrapper_json(
            "--preset",
            "compact_urban_fashion_portrait",
            "--selection-mode",
            "rule",
            "--seed",
            "31",
            "--detail-level",
            "compact",
        )

        item = payload[0]
        expected = (
            "Let one quiet imperfection, shared light, and a small material trace make the frame feel "
            "discovered rather than assembled."
        )
        self.assertNotIn(expected, item["prompt_en"])
        self.assertIn("no text or watermark", item["prompt_en"])
        self.assertEqual(item["provenance"]["prompt_id"], hashlib.sha256(item["prompt_en"].encode("utf-8")).hexdigest()[:16])

        documentary_pack = self.run_wrapper_json(
            "--preset",
            "street_observer_framing",
            "--selection-mode",
            "rule",
            "--seed",
            "31",
            "--emit-candidate-pack",
            "--candidate-pack-version",
            "v3",
        )[0]
        self.assertEqual(documentary_pack["quality_profile"]["profile_id"], "documentary")
        self.assertTrue(documentary_pack["artistic_final_touch"]["enabled"])

    def test_audit_composed_prompt_warns_for_missing_artistic_final_touch(self):
        final_sentence = (
            "Let the final frame keep one quiet imperfection, shared light across subject and setting, "
            "and a small material trace, so it feels discovered by a real photographer rather than assembled as a clean concept image."
        )
        pack = {
            "pack_id": "abababababababab",
            "mandatory_intents": [],
            "uncovered_intents": [],
            "presets": [],
            "slots": {},
            "artistic_final_touch": {
                "enabled": True,
                "final_sentence_en": final_sentence,
                "audit_terms": ["quiet imperfection", "shared light", "material trace"],
            },
            "coverage": {},
            "conflicts": [],
            "negative_en": None,
            "provenance": {},
        }
        bland = {
            "pack_id": "abababababababab",
            "prompt_en": "A quiet portrait with no text or watermark.",
            "chosen_candidate_ids": [],
        }
        touched = {
            "pack_id": "abababababababab",
            "prompt_en": f"A quiet portrait with no text or watermark. {final_sentence}",
            "chosen_candidate_ids": [],
        }
        pack, bland, touched = prepare_audit_fixture(pack, bland, touched)
        with tempfile.TemporaryDirectory() as tmpdir:
            pack_path = Path(tmpdir) / "pack.json"
            bland_path = Path(tmpdir) / "bland.json"
            touched_path = Path(tmpdir) / "touched.json"
            pack_path.write_text(json.dumps(pack, ensure_ascii=False), encoding="utf-8")
            bland_path.write_text(json.dumps(bland, ensure_ascii=False), encoding="utf-8")
            touched_path.write_text(json.dumps(touched, ensure_ascii=False), encoding="utf-8")
            warned = subprocess.run(
                [sys.executable, str(AUDIT_COMPOSED_PATH), "--pack", str(pack_path), "--composed", str(bland_path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            passed = subprocess.run(
                [sys.executable, str(AUDIT_COMPOSED_PATH), "--pack", str(pack_path), "--composed", str(touched_path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(warned.returncode, 0, warned.stdout + warned.stderr)
        warned_audit = json.loads(warned.stdout)
        self.assertIn("artistic_final_touch", {warning["check"] for warning in warned_audit["warnings"]})
        self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)
        passed_audit = json.loads(passed.stdout)
        self.assertNotIn("artistic_final_touch", {warning["check"] for warning in passed_audit["warnings"]})

    def test_candidate_pack_exposes_reference_scaffold_for_yandere(self):
        args = (
            "--concept",
            "카리나 메이드 얀데레",
            "--selection-mode",
            "rule",
            "--seed",
            "701",
            "--emit-candidate-pack",
        )
        payload = self.run_wrapper_json(*args)
        repeat_payload = self.run_wrapper_json(*args)

        pack = payload[0]
        repeat_pack = repeat_payload[0]
        self.assertEqual(pack["masked_buckets"], repeat_pack["masked_buckets"])
        self.assertEqual(pack["open_slots"], repeat_pack["open_slots"])

        required_axes = {axis["id"] for axis in pack["concept_axes"]["required"]}
        self.assertTrue({"obsessive_possession", "surveillance_gaze", "boundary_collapse"} <= required_axes)
        self.assertIn("motif_budget", pack)
        self.assertIn("motif_taxonomy", pack["motif_budget"])
        self.assertIn("phone_selfie_mirror", pack["motif_budget"]["motif_taxonomy"])
        self.assertIn("red_thread", pack["motif_budget"]["quotas"])
        self.assertIn("photo_wall", pack["motif_budget"]["quotas"])
        self.assertIn("phone_selfie_mirror", pack["motif_budget"]["quotas"])
        self.assertEqual(pack["preset_reference"]["role"], "private_routing_scaffold")
        self.assertFalse(pack["preset_reference"]["source_preset_exposed"])
        self.assertFalse(pack["preset_reference"]["source_prompt_exposed"])
        self.assertNotIn("preset_id", pack["preset_reference"])
        self.assertTrue(pack["preset_reference"]["used_sections"])
        self.assertTrue(pack["preset_reference"]["dropped_sections"])
        self.assertTrue(pack["masked_buckets"])
        self.assertTrue(pack["open_slots"])
        self.assertTrue({slot["bucket"] for slot in pack["open_slots"]} <= set(pack["masked_buckets"]))
        self.assertTrue(all(slot["status"] == "intentionally_open" for slot in pack["open_slots"]))
        self.assertIn("score", pack["template_echo_risk"])
        self.assertLessEqual(pack["template_echo_risk"]["score"], pack["template_echo_risk"]["max_allowed_score"])

    def test_candidate_pack_defaults_concept_resolution_to_soft_mode(self):
        payload = self.run_wrapper_json(
            "--concept",
            "카리나 메이드 흡혈귀",
            "--emit-candidate-pack",
            "--explain-concept",
        )

        concept = payload["concepts"][0]
        self.assertEqual(concept["concept_mode"], "soft")
        self.assertFalse(concept["forced_slots_applied"])

        legacy_payload = self.run_wrapper_json(
            "--concept",
            "카리나 메이드 흡혈귀",
            "--concept-mode",
            "legacy",
            "--emit-candidate-pack",
            "--explain-concept",
        )
        self.assertEqual(legacy_payload["concepts"][0]["concept_mode"], "legacy")
        self.assertTrue(legacy_payload["concepts"][0]["forced_slots_applied"])

    def test_audit_composed_prompt_enforces_pack_contract(self):
        pack = {
            "pack_id": "aaaaaaaaaaaaaaaa",
            "mandatory_intents": [{"text": "dragon", "status": "covered", "covered_by": ["slot:subject:dragon"], "audit_terms": ["dragon"]}],
            "uncovered_intents": [],
            "presets": [{"id": "preset:p1"}],
            "slots": {
                "subject": {"candidates": [{"id": "slot:subject:dragon"}]},
                "mood": {"candidates": [{"id": "slot:mood:cozy"}, {"id": "slot:mood:tense"}]},
            },
            "coverage": {},
            "conflicts": [{"id": "conflict:1", "severity": "hard", "candidates": ["slot:mood:cozy", "slot:mood:tense"]}],
            "negative_en": "bad anatomy",
            "provenance": {},
        }
        good = {
            "pack_id": "aaaaaaaaaaaaaaaa",
            "prompt_en": "A dragon portrait with warm studio light, no text or watermark.",
            "negative_en": "bad anatomy",
            "chosen_candidate_ids": ["preset:p1", "slot:subject:dragon", "slot:mood:cozy"],
            "composer": "agent",
        }
        bad = {
            **good,
            "prompt_en": "A portrait with blood on the costume, no text or watermark.",
            "chosen_candidate_ids": ["slot:subject:dragon", "slot:mood:cozy", "slot:mood:tense", "slot:missing:nope"],
        }
        pack, good, bad = prepare_audit_fixture(pack, good, bad)
        with tempfile.TemporaryDirectory() as tmpdir:
            pack_path = Path(tmpdir) / "pack.json"
            good_path = Path(tmpdir) / "good.json"
            bad_path = Path(tmpdir) / "bad.json"
            pack_path.write_text(json.dumps(pack, ensure_ascii=False), encoding="utf-8")
            good_path.write_text(json.dumps(good, ensure_ascii=False), encoding="utf-8")
            bad_path.write_text(json.dumps(bad, ensure_ascii=False), encoding="utf-8")

            passed = subprocess.run(
                [sys.executable, str(AUDIT_COMPOSED_PATH), "--pack", str(pack_path), "--composed", str(good_path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(passed.returncode, 0, passed.stderr)
            self.assertEqual(json.loads(passed.stdout)["status"], "pass")

            failed = subprocess.run(
                [sys.executable, str(AUDIT_COMPOSED_PATH), "--pack", str(pack_path), "--composed", str(bad_path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(failed.returncode, 1)
            audit = json.loads(failed.stdout)
            self.assertEqual(audit["status"], "fail")
            failure_checks = {failure["check"] for failure in audit["failures"]}
            self.assertTrue({"mandatory_intent", "chosen_candidate_ids", "hard_conflict"} <= failure_checks)

    def test_audit_composed_prompt_warns_for_missing_photographic_integration(self):
        pack = {
            "pack_id": "dddddddddddddddd",
            "mandatory_intents": [{"text": "cathedral", "status": "covered", "covered_by": ["preset:p1"], "audit_terms": ["cathedral"]}],
            "uncovered_intents": [],
            "presets": [{"id": "preset:p1"}],
            "slots": {},
            "photographic_integration": {
                "enabled": True,
                "profile_id": "axis_composite_photo_integration",
                "required_categories": ["environment_binding", "optical_depth", "human_trace"],
                "minimum_category_hits": 2,
                "category_terms": {
                    "environment_binding": ["color spill", "dust", "reflection"],
                    "optical_depth": ["foreground", "falloff", "grain"],
                    "human_trace": ["rain-damp", "stray hair", "tired"],
                },
                "principles": ["bind the subject and cathedral with shared light"],
            },
            "coverage": {},
            "conflicts": [],
            "negative_en": None,
            "provenance": {},
        }
        bland = {
            "pack_id": "dddddddddddddddd",
            "prompt_en": "A polished cathedral portrait, no text or watermark.",
            "chosen_candidate_ids": ["preset:p1"],
        }
        integrated = {
            "pack_id": "dddddddddddddddd",
            "prompt_en": (
                "A cathedral portrait where stained-glass color spill crosses the cheek and cassock, "
                "with foreground candle blur and gentle falloff through dusty nave air, no text or watermark."
            ),
            "chosen_candidate_ids": ["preset:p1"],
        }
        pack, bland, integrated = prepare_audit_fixture(pack, bland, integrated)
        with tempfile.TemporaryDirectory() as tmpdir:
            pack_path = Path(tmpdir) / "pack.json"
            bland_path = Path(tmpdir) / "bland.json"
            integrated_path = Path(tmpdir) / "integrated.json"
            pack_path.write_text(json.dumps(pack, ensure_ascii=False), encoding="utf-8")
            bland_path.write_text(json.dumps(bland, ensure_ascii=False), encoding="utf-8")
            integrated_path.write_text(json.dumps(integrated, ensure_ascii=False), encoding="utf-8")

            warned = subprocess.run(
                [sys.executable, str(AUDIT_COMPOSED_PATH), "--pack", str(pack_path), "--composed", str(bland_path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(warned.returncode, 0, warned.stdout + warned.stderr)
            warned_audit = json.loads(warned.stdout)
            self.assertEqual(warned_audit["status"], "pass")
            self.assertIn("photographic_integration", {warning["check"] for warning in warned_audit["warnings"]})

            passed = subprocess.run(
                [sys.executable, str(AUDIT_COMPOSED_PATH), "--pack", str(pack_path), "--composed", str(integrated_path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)
            passed_audit = json.loads(passed.stdout)
            self.assertNotIn("photographic_integration", {warning["check"] for warning in passed_audit["warnings"]})

    def test_audit_composed_prompt_warns_for_missing_visual_proposition(self):
        pack = {
            "pack_id": "eeeeeeeeeeeeeeee",
            "mandatory_intents": [{"text": "portrait", "status": "covered", "covered_by": ["preset:p1"], "audit_terms": ["portrait"]}],
            "uncovered_intents": [],
            "presets": [{"id": "preset:p1"}],
            "slots": {},
            "visual_proposition": {
                "enabled": True,
                "subject_class": "person",
                "register": "understated",
                "minimum_hits": 1,
                "core_candidates": [
                    {
                        "id": "slot:narrative_core:private_ritual_core",
                        "slot": "narrative_core",
                        "entry_id": "private_ritual_core",
                        "terms": ["private ritual", "small personal routine"],
                    }
                ],
                "tension_candidates": [
                    {
                        "id": "slot:concept_tension:public_vs_private_tension",
                        "slot": "concept_tension",
                        "entry_id": "public_vs_private_tension",
                        "terms": ["public versus private", "private emotion held inside public space"],
                    }
                ],
                "category_terms": {
                    "narrative_core": ["private ritual", "small personal routine"],
                    "concept_tension": ["public versus private", "private emotion held inside public space"],
                    "evidence": ["hand", "placement", "trace"],
                },
                "audit_categories": ["narrative_core", "concept_tension", "evidence"],
                "principles": ["Give the frame one quiet reason to exist beyond beauty."],
            },
            "coverage": {},
            "conflicts": [],
            "negative_en": None,
            "provenance": {},
        }
        bland = {
            "pack_id": "eeeeeeeeeeeeeeee",
            "prompt_en": "A polished portrait in a detailed room, no text or watermark.",
            "chosen_candidate_ids": ["preset:p1"],
        }
        integrated = {
            "pack_id": "eeeeeeeeeeeeeeee",
            "prompt_en": (
                "A portrait built around a private ritual in public, her hand hiding a small personal routine "
                "inside an otherwise polished room, no text or watermark."
            ),
            "chosen_candidate_ids": ["preset:p1", "slot:narrative_core:private_ritual_core"],
        }
        pack, bland, integrated = prepare_audit_fixture(pack, bland, integrated)
        with tempfile.TemporaryDirectory() as tmpdir:
            pack_path = Path(tmpdir) / "pack.json"
            bland_path = Path(tmpdir) / "bland.json"
            integrated_path = Path(tmpdir) / "integrated.json"
            pack_path.write_text(json.dumps(pack, ensure_ascii=False), encoding="utf-8")
            bland_path.write_text(json.dumps(bland, ensure_ascii=False), encoding="utf-8")
            integrated_path.write_text(json.dumps(integrated, ensure_ascii=False), encoding="utf-8")

            warned = subprocess.run(
                [sys.executable, str(AUDIT_COMPOSED_PATH), "--pack", str(pack_path), "--composed", str(bland_path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(warned.returncode, 0, warned.stdout + warned.stderr)
            warned_audit = json.loads(warned.stdout)
            self.assertIn("visual_proposition", {warning["check"] for warning in warned_audit["warnings"]})

            passed = subprocess.run(
                [sys.executable, str(AUDIT_COMPOSED_PATH), "--pack", str(pack_path), "--composed", str(integrated_path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)
        passed_audit = json.loads(passed.stdout)
        self.assertNotIn("visual_proposition", {warning["check"] for warning in passed_audit["warnings"]})

    def test_audit_composed_prompt_warns_for_missing_photographic_craft(self):
        pack = {
            "pack_id": "1212121212121212",
            "mandatory_intents": [],
            "uncovered_intents": [],
            "presets": [{"id": "preset:p1"}],
            "slots": {},
            "photographic_craft": {
                "enabled": True,
                "selection_mode": "facet_only",
                "top_strategy": {"id": "structure_led", "emphasize": ["frame_hierarchy", "shot_intent"]},
                "prompt_dimension_ids": ["frame_hierarchy", "shot_intent"],
                "active_dimensions": [
                    {
                        "id": "frame_hierarchy",
                        "selected_principle": "Organize the viewer's reading order.",
                        "selected_guidance_en": "organize foreground, subject plane, and background into a clear reading order",
                        "audit_terms": ["foreground", "subject plane", "background", "reading order"],
                        "active_refinements": [],
                    },
                    {
                        "id": "shot_intent",
                        "selected_principle": "Make the frame's intent legible.",
                        "selected_guidance_en": "make the frame's photographic intent legible before surface styling",
                        "audit_terms": ["photographic intent", "frame intent"],
                        "active_refinements": [],
                    },
                ],
            },
            "coverage": {},
            "conflicts": [],
            "negative_en": None,
            "provenance": {},
        }
        bland = {
            "pack_id": "1212121212121212",
            "prompt_en": "A polished portrait in a detailed room, no text or watermark.",
            "chosen_candidate_ids": ["preset:p1"],
        }
        crafted = {
            "pack_id": "1212121212121212",
            "prompt_en": (
                "A portrait with foreground, subject plane, and background arranged into a clear reading order, "
                "no text or watermark."
            ),
            "chosen_candidate_ids": ["preset:p1"],
        }
        pack, bland, crafted = prepare_audit_fixture(pack, bland, crafted)
        with tempfile.TemporaryDirectory() as tmpdir:
            pack_path = Path(tmpdir) / "pack.json"
            bland_path = Path(tmpdir) / "bland.json"
            crafted_path = Path(tmpdir) / "crafted.json"
            pack_path.write_text(json.dumps(pack, ensure_ascii=False), encoding="utf-8")
            bland_path.write_text(json.dumps(bland, ensure_ascii=False), encoding="utf-8")
            crafted_path.write_text(json.dumps(crafted, ensure_ascii=False), encoding="utf-8")
            warned = subprocess.run(
                [sys.executable, str(AUDIT_COMPOSED_PATH), "--pack", str(pack_path), "--composed", str(bland_path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            passed = subprocess.run(
                [sys.executable, str(AUDIT_COMPOSED_PATH), "--pack", str(pack_path), "--composed", str(crafted_path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(warned.returncode, 0, warned.stdout + warned.stderr)
        warned_audit = json.loads(warned.stdout)
        self.assertIn("photographic_craft", {warning["check"] for warning in warned_audit["warnings"]})
        self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)
        passed_audit = json.loads(passed.stdout)
        self.assertNotIn("photographic_craft", {warning["check"] for warning in passed_audit["warnings"]})

    def test_audit_visual_proposition_applies_lightweight_observational_register(self):
        pack = {
            "pack_id": "ffffffffffffffff",
            "mandatory_intents": [],
            "uncovered_intents": [],
            "presets": [{"id": "preset:p1"}],
            "slots": {},
            "visual_proposition": {
                "enabled": True,
                "subject_class": "object_scene",
                "register": "observational",
                "minimum_hits": 1,
                "category_terms": {
                    "narrative_core": ["quiet arrangement"],
                    "concept_tension": ["organic versus synthetic"],
                    "evidence": ["placement", "contact", "trace"],
                },
                "audit_categories": ["narrative_core", "concept_tension", "evidence"],
            },
            "coverage": {},
            "conflicts": [],
            "negative_en": None,
            "provenance": {},
        }
        bland = {
            "pack_id": "ffffffffffffffff",
            "prompt_en": "A clean product still life, no text or watermark.",
            "chosen_candidate_ids": ["preset:p1"],
        }
        integrated = {
            "pack_id": "ffffffffffffffff",
            "prompt_en": "A product still life where placement, contact shadow, and small use trace organize the arrangement, no text or watermark.",
            "chosen_candidate_ids": ["preset:p1"],
        }
        pack, bland, integrated = prepare_audit_fixture(pack, bland, integrated)
        with tempfile.TemporaryDirectory() as tmpdir:
            pack_path = Path(tmpdir) / "pack.json"
            bland_path = Path(tmpdir) / "bland.json"
            integrated_path = Path(tmpdir) / "integrated.json"
            pack_path.write_text(json.dumps(pack, ensure_ascii=False), encoding="utf-8")
            bland_path.write_text(json.dumps(bland, ensure_ascii=False), encoding="utf-8")
            integrated_path.write_text(json.dumps(integrated, ensure_ascii=False), encoding="utf-8")
            warned = subprocess.run(
                [sys.executable, str(AUDIT_COMPOSED_PATH), "--pack", str(pack_path), "--composed", str(bland_path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            passed = subprocess.run(
                [sys.executable, str(AUDIT_COMPOSED_PATH), "--pack", str(pack_path), "--composed", str(integrated_path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertEqual(warned.returncode, 0, warned.stdout + warned.stderr)
        warned_audit = json.loads(warned.stdout)
        self.assertIn("visual_proposition", {warning["check"] for warning in warned_audit["warnings"]})
        self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)
        passed_audit = json.loads(passed.stdout)
        self.assertNotIn("visual_proposition", {warning["check"] for warning in passed_audit["warnings"]})

    def test_audit_composed_prompt_rejects_masked_bucket_and_motif_echo(self):
        pack = {
            "pack_id": "cccccccccccccccc",
            "mandatory_intents": [],
            "uncovered_intents": [],
            "presets": [{"id": "preset:p1"}],
            "slots": {},
            "concept_axes": {
                "required": [
                    {"id": "surveillance_gaze", "terms": ["surveillance evidence", "records board"]}
                ]
            },
            "motif_budget": {
                "quotas": {"photo_wall": {"max_batch_share": 0.3}},
                "discouraged_now": ["photo_wall"],
                "motif_taxonomy": {
                    "photo_wall": ["instant_photo_stack", "photo wall", "same-person photos"],
                    "record_board": ["logo_board_prop", "records board"],
                },
            },
            "preset_reference": {
                "role": "reference_scaffold",
                "masked_slots": [{"slot": "prop", "bucket": "action_prop"}],
            },
            "masked_buckets": ["action_prop"],
            "open_slots": [
                {
                    "slot": "prop",
                    "bucket": "action_prop",
                    "status": "intentionally_open",
                    "reason": "semantic_dropout",
                }
            ],
            "template_echo_risk": {"max_allowed_score": 0.2},
            "coverage": {},
            "conflicts": [],
            "negative_en": None,
            "provenance": {},
        }
        good = {
            "pack_id": "cccccccccccccccc",
            "prompt_en": "A tense portrait built around surveillance evidence on a records board, no text or watermark.",
            "chosen_candidate_ids": ["preset:p1"],
        }
        bad = {
            "pack_id": "cccccccccccccccc",
            "prompt_en": "A tense portrait with surveillance evidence, an instant photo stack, and same-person photos on the wall, no text or watermark.",
            "chosen_candidate_ids": ["preset:p1", "slot:prop:instant_photo_stack"],
        }
        pack, good, bad = prepare_audit_fixture(pack, good, bad)
        with tempfile.TemporaryDirectory() as tmpdir:
            pack_path = Path(tmpdir) / "pack.json"
            good_path = Path(tmpdir) / "good.json"
            bad_path = Path(tmpdir) / "bad.json"
            pack_path.write_text(json.dumps(pack, ensure_ascii=False), encoding="utf-8")
            good_path.write_text(json.dumps(good, ensure_ascii=False), encoding="utf-8")
            bad_path.write_text(json.dumps(bad, ensure_ascii=False), encoding="utf-8")

            passed = subprocess.run(
                [sys.executable, str(AUDIT_COMPOSED_PATH), "--pack", str(pack_path), "--composed", str(good_path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)

            failed = subprocess.run(
                [sys.executable, str(AUDIT_COMPOSED_PATH), "--pack", str(pack_path), "--composed", str(bad_path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(failed.returncode, 1)
            audit = json.loads(failed.stdout)
            failure_checks = {failure["check"] for failure in audit["failures"]}
            self.assertTrue({"masked_bucket_echo", "motif_quota", "template_echo_risk"} <= failure_checks)

    def test_audit_composed_prompt_rejects_role_scene_and_species_mismatch(self):
        pack = {
            "pack_id": "bbbbbbbbbbbbbbbb",
            "mandatory_intents": [{"text": "beastkin", "status": "covered", "covered_by": ["slot:subject:beastkin"], "audit_terms": ["beastkin"]}],
            "uncovered_intents": [],
            "presets": [{"id": "preset:p1"}],
            "slots": {
                "subject": {"candidates": [{"id": "slot:subject:beastkin"}]},
                "location": {
                    "candidates": [
                        {"id": "slot:location:traffic_crossing_rain"},
                        {"id": "slot:location:highland_pasture"},
                    ]
                },
                "species_marker": {
                    "candidates": [
                        {"id": "slot:species_marker:feline_reflective_eye_whisker_shadow"},
                        {"id": "slot:species_marker:avian_feather_ruff_wing_sleeve"},
                    ]
                },
            },
            "role_scene_policy": {
                "enabled": True,
                "enforce": True,
                "scene_family": "procedural_public_safety",
                "allowed_locations": ["traffic_crossing_rain"],
                "forbidden_locations": ["highland_pasture"],
            },
            "species_family": {
                "enabled": True,
                "family": "feline",
                "variant_id": "feline_cat_bigcat",
                "allowed": {"species_marker": ["feline_reflective_eye_whisker_shadow"]},
            },
            "coverage": {},
            "conflicts": [],
            "negative_en": "bad anatomy",
            "provenance": {},
        }
        composed = {
            "pack_id": "bbbbbbbbbbbbbbbb",
            "prompt_en": "A beastkin police portrait, no text or watermark.",
            "negative_en": "bad anatomy",
            "chosen_candidate_ids": [
                "preset:p1",
                "slot:subject:beastkin",
                "slot:location:highland_pasture",
                "slot:species_marker:avian_feather_ruff_wing_sleeve",
            ],
            "composer": "agent",
        }
        pack, composed = prepare_audit_fixture(pack, composed)
        with tempfile.TemporaryDirectory() as tmpdir:
            pack_path = Path(tmpdir) / "pack.json"
            composed_path = Path(tmpdir) / "composed.json"
            pack_path.write_text(json.dumps(pack, ensure_ascii=False), encoding="utf-8")
            composed_path.write_text(json.dumps(composed, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(AUDIT_COMPOSED_PATH), "--pack", str(pack_path), "--composed", str(composed_path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(result.returncode, 1)
        audit = json.loads(result.stdout)
        failure_checks = {failure["check"] for failure in audit["failures"]}
        self.assertIn("role_scene_policy", failure_checks)
        self.assertIn("species_family", failure_checks)

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

    def test_record_image_run_accepts_candidate_pack_provenance(self):
        prompt = "Audited composed prompt with no text or watermark"
        prompt_id = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]
        with tempfile.TemporaryDirectory() as tmpdir:
            ledger = Path(tmpdir) / "runs.ndjson"
            result = subprocess.run(
                [
                    sys.executable,
                    str(RECORD_RUN_PATH),
                    "--ts",
                    "2026-06-03T10:00:00+09:00",
                    "--prompt-en",
                    prompt,
                    "--prompt-id",
                    prompt_id,
                    "--attempt",
                    "1",
                    "--status",
                    "success",
                    "--tool",
                    "image_gen",
                    "--pack-id",
                    "aaaaaaaaaaaaaaaa",
                    "--chosen-candidate-ids-json",
                    json.dumps({"subject": ["slot:subject:dragon"], "preset": "preset:p1"}),
                    "--composer",
                    "agent",
                    "--audit-status",
                    "pass",
                    "--augmentation-brief-json",
                    json.dumps(
                        {
                            "selected_route_id": "material_world",
                            "decisions": [
                                {
                                    "candidate_id": "slot:subject:dragon",
                                    "decision": "modified",
                                }
                            ],
                        }
                    ),
                    "--ledger",
                    str(ledger),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            row = json.loads(ledger.read_text(encoding="utf-8").splitlines()[0])
            self.assertEqual(row["pack_id"], "aaaaaaaaaaaaaaaa")
            self.assertEqual(row["chosen_candidate_ids"]["subject"], ["slot:subject:dragon"])
            self.assertEqual(row["chosen_candidate_ids"]["preset"], "preset:p1")
            self.assertEqual(row["composer"], "agent")
            self.assertEqual(row["audit_status"], "pass")
            self.assertEqual(row["augmentation_brief"]["selected_route_id"], "material_world")
            self.assertEqual(row["augmentation_brief"]["decisions"][0]["decision"], "modified")

    def test_record_image_run_writes_independent_arm_manifest(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            ledger = root / "runs.ndjson"
            manifest = root / "run_manifest.json"
            image_path = root / "image.png"
            image_path.write_bytes(b"native-pixels")
            result = subprocess.run(
                [
                    sys.executable,
                    str(RECORD_RUN_PATH),
                    "--ts",
                    "2026-08-13T15:00:00+09:00",
                    "--prompt-en",
                    "Audited independent Japanese-subculture moe prompt",
                    "--attempt",
                    "1",
                    "--status",
                    "success",
                    "--image-path",
                    str(image_path),
                    "--tool",
                    "built_in_image_gen_edit",
                    "--pack-id",
                    "a" * 16,
                    "--composer",
                    "agent",
                    "--audit-status",
                    "pass",
                    "--arm-id",
                    "arm-1",
                    "--worktree-id",
                    "detached-worktree-arm-1",
                    "--skill-sha256",
                    "b" * 64,
                    "--source-ref",
                    "c" * 40,
                    "--candidate-pack-version",
                    "v4",
                    "--authorial-request-sha256",
                    "d" * 64,
                    "--reference-sha256",
                    "e" * 64,
                    "--image-call-count",
                    "1",
                    "--independent-no-cross-arm-inputs",
                    "--manifest",
                    str(manifest),
                    "--ledger",
                    str(ledger),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            row = json.loads(ledger.read_text(encoding="utf-8").splitlines()[0])
            self.assertEqual(row["candidate_pack_version"], "v4")
            self.assertEqual(row["authorial_request_sha256"], "d" * 64)
            self.assertEqual(row["reference_sha256"], ["e" * 64])
            self.assertEqual(row["image_call_count"], 1)
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["contract_version"],
                "photo-independent-run-manifest/v1",
            )
            self.assertEqual(payload["arm_id"], "arm-1")
            self.assertFalse(payload["cross_arm_inputs_used"])
            self.assertEqual(payload["skill_sha256"], "b" * 64)
            self.assertEqual(payload["source_ref"], "c" * 40)
            self.assertEqual(payload["image_call_count"], 1)
            self.assertEqual(payload["image_paths"], [str(image_path)])

    def test_generate_images_via_api_forwards_audited_provenance_and_retry_chain(self):
        spec = importlib.util.spec_from_file_location(
            "generate_images_via_api", GENERATE_IMAGES_VIA_API_PATH
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        prompt = "Exact audited prompt text"
        negative = "watermark, readable text"
        prompt_id = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]
        source_argv = ["--intent", "adult repair handoff", "--seed", "42"]
        chosen = {"preset": "preset:p1", "subject": ["slot:subject:s1"]}
        chosen_visual = ["visual-concept:inner_thigh_negative_space"]
        effective_visual_sha = "f" * 64
        brief = {
            "selected_route_id": "material_world",
            "decisions": [{"candidate_id": "slot:subject:s1", "decision": "accepted"}],
        }
        api_prompts = []
        ledger_calls = []

        def fake_call_api(_key, _model, full_prompt, _size):
            api_prompts.append(full_prompt)
            if len(api_prompts) == 1:
                raise RuntimeError("temporary network failure")
            return b"image-bytes"

        def fake_record(args):
            ledger_calls.append(list(args))
            attempt = int(args[args.index("--attempt") + 1])
            return {"run_id": f"{attempt:016x}"}

        def flag_value(args, flag):
            return args[args.index(flag) + 1]

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            prompt_file = tmp / "audited.prompt.json"
            prompt_file.write_text(
                json.dumps(
                    {
                        "prompt_en": prompt,
                        "negative_en": negative,
                        "pack_id": "a" * 16,
                        "chosen_candidate_ids": chosen,
                        "chosen_visual_concept_ids": chosen_visual,
                        "effective_visual_contract_sha256": effective_visual_sha,
                        "composer": "agent",
                        "audit_status": "pass",
                        "augmentation_brief": brief,
                        "provenance": {
                            "seed": 42,
                            "argv": source_argv,
                            "concept_lock": ["adult repair handoff"],
                        },
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            with mock.patch.object(module, "call_api", side_effect=fake_call_api), mock.patch.object(
                module, "record", side_effect=fake_record
            ):
                ok = module.generate_for_file(
                    prompt_file,
                    key="test-key",
                    model="gpt-image-2",
                    size="1024x1536",
                    attempts=2,
                    concept=None,
                    slug=None,
                    out_base=tmp / "outside-worktree-output",
                    timestamp="20260812_120000",
                )

            self.assertTrue(ok)
            self.assertEqual(
                api_prompts,
                [prompt + "\n\nAvoid: " + negative] * 2,
            )
            self.assertEqual(len(ledger_calls), 2)
            first, second = ledger_calls
            self.assertEqual(flag_value(first, "--status"), "error")
            self.assertEqual(flag_value(second, "--status"), "success")
            self.assertNotIn("--retry-of", first)
            self.assertEqual(flag_value(second, "--retry-of"), "0000000000000001")
            self.assertEqual(flag_value(second, "--prompt-id"), prompt_id)
            self.assertEqual(flag_value(second, "--negative-en"), negative)
            self.assertEqual(flag_value(second, "--pack-id"), "a" * 16)
            self.assertEqual(json.loads(flag_value(second, "--chosen-candidate-ids-json")), chosen)
            self.assertEqual(
                json.loads(flag_value(second, "--chosen-visual-concept-ids-json")),
                chosen_visual,
            )
            self.assertEqual(
                flag_value(second, "--effective-visual-contract-sha256"),
                effective_visual_sha,
            )
            self.assertEqual(flag_value(second, "--composer"), "agent")
            self.assertEqual(flag_value(second, "--audit-status"), "pass")
            self.assertEqual(json.loads(flag_value(second, "--augmentation-brief-json")), brief)
            self.assertEqual(json.loads(flag_value(second, "--argv-json")), source_argv)
            image_path = Path(flag_value(second, "--image-path"))
            self.assertTrue(image_path.is_absolute())
            self.assertEqual(image_path.read_bytes(), b"image-bytes")

    def test_run_ledger_schema_covers_recorder_output_contract(self):
        spec = importlib.util.spec_from_file_location("record_image_run", RECORD_RUN_PATH)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        args = module.parse_args(
            [
                "--ts",
                "2026-08-12T12:00:00+09:00",
                "--prompt-en",
                "Audited prompt",
                "--attempt",
                "1",
                "--status",
                "success",
                "--pack-id",
                "a" * 16,
                "--chosen-candidate-ids-json",
                json.dumps({"preset": "preset:p1"}),
                "--composer",
                "agent",
                "--audit-status",
                "pass",
            ]
        )
        entry = module.build_entry(args)
        schema = json.loads(RUN_LEDGER_SCHEMA_PATH.read_text(encoding="utf-8"))

        self.assertFalse(set(entry) - set(schema["properties"]))
        self.assertTrue(set(schema["required"]) <= set(entry))
        self.assertEqual(set(schema["properties"]["status"]["enum"]), module.VALID_STATUSES)
        self.assertEqual(set(schema["properties"]["composer"]["enum"]), module.VALID_COMPOSERS)
        self.assertEqual(
            set(schema["properties"]["audit_status"]["enum"]),
            module.VALID_AUDIT_STATUSES,
        )

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
                "royal_ball_gown",
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
                "throne_hall_interior",
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

    def test_expanded_viewpoint_presets_tags_and_recipes_are_registered(self):
        preset_ids = {preset["id"] for preset in self.data["presets"]}
        self.assertTrue(
            {
                "flight_attendant_service_portrait",
                "modern_shaman_ritual_portrait",
                "archivist_library_observation",
                "digital_glitch_entity_portrait",
                "environmental_erosion_portrait",
                "era_costume_editorial",
                "dynamic_motion_portrait",
            }.issubset(preset_ids)
        )
        self.assertTrue(
            {
                "welding_sparks_portrait",
                "auto_mechanic_grease",
                "harbor_fisherman_dawn",
                "farmer_soil_documentary",
                "blacksmith_forge_portrait",
                "climbing_chalk_wall",
                "swimmer_lane_splash",
                "combat_sport_sweat",
                "track_sprint_blur",
                "equestrian_dust",
                "freediver_blue_depth",
                "submerged_fabric_portrait",
                "underwater_housing_portrait",
                "forensic_uv_macro",
                "evidence_table_flash",
                "nitrile_glove_specimen_closeup",
                "seoul_7080_bus_stop",
                "old_dabang_window_portrait",
                "vintage_korean_market_flash",
                "high_speed_splash_flash",
                "uv_fluorescence_still",
                "thermal_camera_look",
                "dj_booth_haze",
                "jazz_club_smoke",
                "orchestra_pit_warm",
                "punk_basement_show",
                "falconry_glove",
                "sheepdog_herding",
                "horse_training_dust",
                "facade_golden_symmetry",
                "spiral_stairwell_vertigo",
                "parking_garage_vanishing_point",
                "lighthouse_storm",
                "fish_market_auction_dawn",
                "ship_deck_salt_spray",
                "warehouse_rave_uv",
                "lowrider_night_meet",
                "tattoo_parlor_documentary",
                "three_generation_hands",
                "grandmother_kitchen_window",
                "old_photo_album_table",
                "star_trail_human_scale",
                "beastkin_threshold_portrait",
                "dragonkin_scale_portrait",
                "grim_reaper_hourglass_portrait",
                "circus_backstage_clown_portrait",
                "living_doll_joint_portrait",
                "pirate_deck_portrait",
                "goddess_gilded_hall_portrait",
                "girl_crush_street_portrait",
                "ethereal_dream_window_portrait",
                "rugged_tough_documentary_portrait",
            }.issubset(preset_ids)
        )

        family_ids = {family["id"] for family in self.data["preset_families"]}
        self.assertTrue(
            {
                "seasonal_event_family",
                "folk_mystic_family",
                "professional_observation_family",
                "era_world_family",
                "dynamic_motion_family",
                "digital_entity_family",
                "environmental_transformation_family",
                "manual_labor_trades_family",
                "sports_athletic_action_family",
                "underwater_submersion_family",
                "technical_forensics_family",
                "korean_7080_retro_family",
                "scientific_imaging_aesthetic_family",
                "live_music_performance_family",
                "working_animal_partnership_family",
                "architectural_lines_family",
                "maritime_coastal_labor_family",
                "subculture_scene_family",
                "family_generational_documentary_family",
                "night_sky_long_exposure_family",
                "mythic_archetype_portrait_family",
            }.issubset(family_ids)
        )

        expected_slot_ids = {
            "subject": {
                "flight_attendant_role_model",
                "modern_shaman_performer",
                "archivist_role_model",
                "clinical_researcher_role_model",
                "alien_visitor_subject",
                "esper_subject",
                "welder_worker",
                "competitive_swimmer",
                "freediver",
                "forensic_technician",
                "dj_performer",
                "falconer",
                "retro_seoul_commuter",
                "three_generation_family",
                "beastkin_subject",
                "dragonkin_subject",
                "grim_reaper_figure",
                "clown_performer",
                "living_doll_subject",
                "pirate_sailor",
                "goddess_figure",
            },
            "costume_style": {
                "flight_attendant_uniform_costume",
                "modern_shaman_ritual_costume",
                "adult_school_uniform_cosplay_costume",
                "clinical_lab_coat_professional",
                "witch_robe_wide_hat",
                "celestial_silk_ribbon_robe",
                "pirate_weathered_coat_costume",
                "ritual_goddess_drape_costume",
                "circus_clown_tailcoat_costume",
                "living_doll_lace_joint_costume",
                "dragonkin_scale_robe_costume",
                "beastkin_tailored_folk_costume",
                "detective_trench_coat_costume",
                "secretary_office_uniform",
                "ballet_rehearsal_wrap_costume",
                "knight_armor_cloak_costume",
                "saint_modest_robe_costume",
                "ghost_bride_veil_dress",
                "covered_santa_fur_trim_costume",
            },
            "wardrobe_style": {
                "covered_track_jacket_training_set",
            },
            "prop": {
                "shaman_bells_prop",
                "five_color_silk_strip_prop",
                "fox_fire_wisp_prop",
                "glitching_phone_screen_prop",
                "archive_box_prop",
                "levitating_teacup_prop",
                "welding_mask_prop",
                "wet_fishing_net_prop",
                "chalk_bag_prop",
                "dj_mixer_console_prop",
                "leather_falconry_glove_prop",
                "evidence_marker_prop",
                "nitrile_gloves_prop",
                "hourglass_prop",
                "tall_scythe_prop",
                "pointed_ear_tail_set_prop",
                "curved_horn_set_prop",
                "radiant_disc_halo_prop",
                "stage_reservation_log_prop",
                "chart_records_board_prop",
                "cctv_monitor_stack_prop",
                "obsession_photo_wall_prop",
                "red_string_pinboard_prop",
                "two_coffee_cups_prop",
                "returned_lost_item_prop",
                "votive_candle_row_prop",
                "evidence_corkboard_prop",
                "case_file_folder_prop",
                "dragon_orb_prop",
                "gift_tag_ledger_prop",
                "stopwatch_training_prop",
            },
            "action": {
                "checking_ore_contact_point",
                "sprint_start_drive",
            },
            "location": {
                "airplane_cabin_aisle",
                "traditional_shrine_interior",
                "grand_archive_hall",
                "clinical_observation_lab",
                "glitch_monitor_room",
                "moss_reclaimed_room",
                "welding_workshop_pit",
                "open_water_blue",
                "forensic_lab_table",
                "seoul_7080_bus_stop_location",
                "old_dabang_window",
                "club_dj_booth",
                "spiral_stairwell",
                "fish_market_auction",
                "grandmother_kitchen_window",
                "night_sky_field",
                "temple_gilded_hall",
                "circus_backstage_tent",
                "sailing_ship_deck",
                "overloaded_evidence_bedroom",
                "stained_glass_chapel",
                "detective_office_caseboard",
                "dragon_court_hall",
                "ghost_bride_window_room",
            },
            "texture": {
                "pixel_drift_edges",
                "localized_chromatic_glitch",
                "moss_surface_detail",
                "pressed_paper_archive_dust",
                "metal_spark_shower",
                "water_droplet_freeze",
                "flowing_fabric_underwater",
                "uv_fluorescent_glow",
                "star_trail_streaks",
                "fur_patch_skin_blend",
                "scale_skin_macro",
                "porcelain_hairline_crack",
                "visible_ball_joint_seam",
                "bio_tissue_membrane_texture",
                "ceramic_hairline_joint_texture",
            },
            "aesthetic_trend": {
                "dark_feminine_aesthetic",
                "old_money_aesthetic",
                "light_academia_aesthetic",
                "whimsigoth_aesthetic",
                "tomboy_aesthetic",
                "girl_crush_aesthetic",
                "ethereal_dream_aesthetic",
                "rugged_tough_aesthetic",
                "living_doll_aesthetic",
            },
            "lighting": {
                "welding_arc_flash",
                "surface_caustic_light",
                "uv_blacklight",
                "temple_disc_backlight",
                "bright_window_silhouette_light",
                "phone_screen_face_glow",
                "bioluminescent_grotto_light",
            },
            "surface_material": {
                "porcelain_doll_joint_surface",
                "salt_weathered_leather_surface",
                "gold_leaf_skin_surface",
                "dragon_scale_surface",
                "translucent_spirit_glow_surface",
            },
            "expression": {
                "dissociated_blank_calm",
                "huffy_pout",
                "flustered_glance_away",
                "knowing_lidded_gaze",
                "quiet_yearning",
                "predatory_calm_lidded",
            },
            "composition": {
                "shrine_wall_overload_frame",
                "birdcage_bar_frame",
                "halo_backlight_centered",
                "caseboard_over_shoulder_frame",
            },
            "light_shape": {
                "god_ray_volumetric_shaft",
                "stained_glass_color_cast",
                "halo_aura_bloom",
                "birdcage_bar_shadows",
                "snowflake_pinpoint_glow",
                "kinetic_trail_edge_light",
            },
            "motion": {
                "suspended_snowflake_motion",
                "kinetic_spell_trail_motion",
            },
            "surreal_physics_detail": {
                "localized_refraction_at_contact",
                "tiny_levitation_contact_shadow",
                "textless_mark_rearrangement_boundary",
            },
        }
        for slot, ids in expected_slot_ids.items():
            with self.subTest(slot=slot):
                actual = {entry["id"] for entry in self.data["slots"][slot]}
                self.assertTrue(ids.issubset(actual))

        recipes = json.loads((SKILL_DIR / "assets" / "concept_recipes.json").read_text(encoding="utf-8"))
        self.assertTrue(
            {
                "승무원",
                "소방관",
                "보안요원",
                "요리사",
                "군장교",
                "학생",
                "무녀",
                "기록가",
                "연구원",
                "교사",
                "의사",
                "형사",
                "탐정",
                "비서",
                "발레리나",
                "아이돌",
                "사제",
                "수도자",
                "호텔리어",
                "회사원",
                "산타복",
                "운동복",
            }.issubset(recipes["roles"])
        )
        self.assertTrue(
            {
                "구미호",
                "원귀",
                "인어",
                "마녀",
                "선녀",
                "도깨비",
                "데이터망령",
                "환경침식",
                "청순",
                "쿨뷰티",
                "도도",
                "발랄",
                "연상",
                "보이시",
                "외계인",
                "초능력자",
                "마법사",
                "수인",
                "용인",
                "사신",
                "광대",
                "리빙돌",
                "해적",
                "여신",
                "걸크러시",
                "몽환",
                "터프",
                "쿨데레",
                "단데레",
                "소악마",
                "첫사랑",
                "여왕",
                "성녀",
                "늑대인간",
                "요정",
                "정령",
                "드래곤족",
                "유령신부",
                "회사원",
            }.issubset(recipes["mixins"])
        )
        self.assertEqual(recipes["aliases"]["사서"], "도서관 사서")
        self.assertEqual(recipes["aliases"]["글리치"], "데이터망령")
        self.assertEqual(recipes["aliases"]["늑대인간"], "늑대인간")
        self.assertEqual(recipes["aliases"]["걸크"], "걸크러시")
        self.assertEqual(recipes["aliases"]["저승사자"], "사신")
        self.assertEqual(recipes["aliases"]["쿠데레"], "쿨데레")
        self.assertEqual(recipes["aliases"]["クーデレ"], "쿨데레")
        self.assertEqual(recipes["aliases"]["kuudere"], "쿨데레")
        self.assertEqual(recipes["aliases"]["cool-dere"], "쿨데레")
        kuudere = recipes["mixins"]["쿨데레"]
        self.assertEqual(kuudere["set"]["expression"], "aloof_composed_gaze")
        self.assertEqual(kuudere["set"]["action"], "offering_spare_umbrella")
        self.assertNotIn("makeup_style", kuudere["set"])
        self.assertNotIn("prop", kuudere["set"])
        self.assertEqual(
            set(kuudere["anchor_families"]),
            {"stable_composure", "target_linked_quiet_care"},
        )
        self.assertEqual(recipes["aliases"]["선생님"], "교사")
        self.assertEqual(recipes["aliases"]["직장인"], "회사원")
        self.assertEqual(recipes["aliases"]["월급쟁이"], "회사원")
        self.assertEqual(recipes["aliases"]["샐러리맨"], "회사원")
        self.assertEqual(recipes["aliases"]["산타 코스튬"], "산타복")
        self.assertEqual(recipes["aliases"]["트레이닝복"], "운동복")
        self.assertEqual(recipes["aliases"]["sportswear"], "운동복")
        self.assertIn("concept_safety", recipes)
        self.assertIn("dark_non_graphic", recipes["concept_safety"])
        self.assertIn("anchor_families", recipes["mixins"]["성녀"])
        self.assertIn("forbidden_slot_values", recipes["mixins"]["소악마"])

        beastkin = recipes["mixins"]["수인"]
        self.assertNotIn("costume_style", beastkin["set"])
        species_variants = beastkin["species_variants"]["variants"]
        self.assertGreaterEqual(len(species_variants), 8)
        self.assertTrue(
            {
                "canid_fox_wolf",
                "feline_cat_bigcat",
                "rabbit_hare",
                "deer_ungulate",
                "bear",
                "horse_equine",
                "aquatic_mammal_otter_seal",
                "avian_owl_raptor_corvid",
                "reptile_lizard_gecko",
            }.issubset({variant["id"] for variant in species_variants})
        )
        self.assertTrue(
            {
                "snake",
                "fish_shark_koi",
                "amphibian",
                "insect_arthropod",
            }.issubset(set(beastkin["species_variants"]["excluded_default_families"]))
        )
        self.assertTrue(
            {
                "threshold_body_transition",
                "sensory_social_othering",
                "shadow_reflection_duality",
            }.issubset({bundle["id"] for bundle in beastkin["bundles"]})
        )
        self.assertTrue(
            {
                "bestiality",
                "dehumanizing caricature",
                "full animal mascot suit",
            }.issubset(set(beastkin["safety_negative_floor"]))
        )
        self.assertIn("body_transition", recipes["mixin_diversity_policy"]["수인"]["aspect_axes"])
        self.assertIn("sensory_othering", recipes["mixin_diversity_policy"]["수인"]["aspect_axes"])
        self.assertIn("shadow_reflection", recipes["mixin_diversity_policy"]["수인"]["aspect_axes"])
        self.assertIn("species_family", recipes["mixin_diversity_policy"]["수인"]["aspect_axes"])
        self.assertGreaterEqual(recipes["mixin_diversity_policy"]["수인"]["min_distinct_species_per_batch"], 4)
        self.assertEqual(beastkin["dual_read_requirement"]["min_role_hits"], 2)
        self.assertIn("holiday_contract_magic", recipes["mixin_diversity_policy"]["마법사"]["aspect_axes"])
        self.assertIn("kinetic_training_magic", recipes["mixin_diversity_policy"]["마법사"]["aspect_axes"])
        self.assertIn("technomancy_interface", recipes["mixin_diversity_policy"]["마법사"]["aspect_axes"])

        robot_bundle_ids = {bundle["id"] for bundle in recipes["mixins"]["로봇"]["bundles"]}
        self.assertTrue(
            {
                "flight_attendant_cabin_safety_android",
                "firefighter_rescue_labor_android",
                "chef_kitchen_process_android",
                "researcher_lab_observation_android",
                "archivist_cataloging_android",
                "shaman_ceremonial_automaton",
            }.issubset(robot_bundle_ids)
        )
        self.assertIn(
            "backstage_booking_burnout",
            {bundle["id"] for bundle in recipes["mixins"]["멘헤라"]["bundles"]},
        )
        self.assertIn(
            "sealed_route_document_control",
            {bundle["id"] for bundle in recipes["mixins"]["얀데레"]["bundles"]},
        )

    def test_expanded_concepts_resolve_role_mixin_and_visible_anchors(self):
        cases = [
            (
                "카리나 무녀 구미호",
                "무녀",
                "구미호",
                "modern_shaman_ritual_portrait",
                {
                    "subject": {"modern_shaman_performer"},
                    "costume_style": {"modern_shaman_ritual_costume"},
                    "prop": {"shaman_bells_prop", "five_color_silk_strip_prop", "fox_fire_wisp_prop"},
                    "expression": {"golden_fox_eye_gaze"},
                    "lighting": {"moonlit_folk_ritual_light"},
                },
            ),
            (
                "윈터 연구원 데이터망령",
                "연구원",
                "데이터망령",
                "researcher_clinical_observation",
                {
                    "subject": {"clinical_researcher_role_model"},
                    "costume_style": {"clinical_lab_coat_professional"},
                    "location": {"clinical_observation_lab"},
                    "prop": {"glass_specimen_case_prop", "glitching_phone_screen_prop"},
                    "light_type": {"ui_projection_on_skin"},
                    "texture": {"pixel_drift_edges", "localized_chromatic_glitch"},
                },
            ),
            (
                "설윤 승무원 쿨뷰티",
                "승무원",
                "쿨뷰티",
                "flight_attendant_service_portrait",
                {
                    "subject": {"flight_attendant_role_model"},
                    "costume_style": {"flight_attendant_uniform_costume"},
                    "location": {"airplane_cabin_aisle"},
                    "expression": {"aloof_composed_gaze"},
                    "makeup_style": {"graphic_eyeliner_sharp"},
                },
            ),
            (
                "지젤 기록가 환경침식",
                "기록가",
                "환경침식",
                "archivist_library_observation",
                {
                    "subject": {"archivist_role_model"},
                    "location": {"grand_archive_hall", "moss_reclaimed_room"},
                    "action": {"organizing_old_manuscripts", "lightly_touching_moss_wall"},
                    "texture": {"moss_surface_detail", "pressed_paper_archive_dust"},
                    "surface_material": {"moss_attached_surface"},
                },
            ),
            (
                "카리나 메이드 수인",
                "메이드",
                "수인",
                "maid_cafe_cosplay_portrait",
                {
                    "subject": {"maid_cafe_performer", "beastkin_subject"},
                    "costume_style": {"frill_apron_maid_costume"},
                    "location": {"maid_cafe_interior"},
                    "action": {"pausing_before_threshold"},
                    "composition": {"threshold_backlit_center"},
                    "world": {"folk_threshold_world"},
                    "light_shape": {"threshold_sliver_light"},
                },
            ),
            (
                "윈터 승무원 로봇",
                "승무원",
                "로봇",
                "service_android_role_unit",
                {
                    "costume_style": {"flight_attendant_uniform_costume"},
                    "location": {"airplane_cabin_aisle"},
                    "subject": {"service_android_unit"},
                    "surface_material": {"matte_synthetic_skin_surface"},
                    "prop": {"serial_spec_plate_prop", "diagnostic_readout_prop"},
                    "composition": {"exposed_joint_detail_crop"},
                    "light_shape": {"status_led_array_pattern"},
                },
            ),
            (
                "카리나 교사 첫사랑",
                "교사",
                "첫사랑",
                "korea_2000s_classroom_nostalgia",
                {
                    "subject": {"teacher_role_model"},
                    "costume_style": {"teacher_blazer_uniform"},
                    "location": {"classroom_interior"},
                    "prop": {"blackboard_chalk_prop", "pressed_flower_bookmark_token"},
                    "expression": {"quiet_yearning"},
                    "mood": {"bittersweet_nostalgia"},
                },
            ),
            (
                "윈터 사제 성녀",
                "사제",
                "성녀",
                "stained_glass_cathedral_portrait",
                {
                    "subject": {"priest_role_model", "saint_role_model"},
                    "costume_style": {"priest_black_cassock_costume", "saint_modest_robe_costume"},
                    "location": {"cathedral_nave_interior"},
                    "prop": {"votive_candle_row_prop"},
                    "light_shape": {"stained_glass_color_cast"},
                    "mood": {"sacred_stillness"},
                },
            ),
            (
                "닝닝 형사 소악마",
                "형사",
                "소악마",
                "detective_caseboard_noir_portrait",
                {
                    "subject": {"detective_role_model"},
                    "costume_style": {"detective_trench_coat_costume"},
                    "location": {"detective_office_caseboard"},
                    "prop": {"evidence_corkboard_prop", "chess_endgame_board_prop"},
                    "expression": {"playful_smirk"},
                    "mood": {"ominous_seduction"},
                },
            ),
            (
                "지젤 기사 드래곤족",
                "기사",
                "드래곤족",
                "cinematic_fantasy_portrait",
                {
                    "subject": {"knight_role_model", "dragon_lineage_subject"},
                    "costume_style": {"knight_armor_cloak_costume", "dragon_scale_court_costume"},
                    "location": {"castle_armory_hall"},
                    "prop": {"heraldic_shield_prop", "dragon_orb_prop"},
                    "surface_material": {"dragon_scale_surface"},
                },
            ),
            (
                "설윤 공주 여신",
                "공주",
                "여신",
                "princess_lineage_succession_portrait",
                {
                    "costume_style": {"royal_ball_gown", "ritual_goddess_drape_costume"},
                    "location": {"throne_hall_interior"},
                    "prop": {"crown_on_cushion_prop", "radiant_disc_halo_prop"},
                    "lighting": {"temple_disc_backlight"},
                    "surface_material": {"gold_leaf_skin_surface"},
                },
            ),
        ]

        for concept, expected_role, expected_mixin, expected_preset, expected_slots in cases:
            with self.subTest(concept=concept):
                payload = self.run_wrapper_json(
                    "--concept",
                    concept,
                    "--selection-mode",
                    "rule",
                    "--seed",
                    "17",
                    "--explain-concept",
                )
                explanation = payload["concepts"][0]
                self.assertEqual(explanation["role"], expected_role)
                self.assertEqual(explanation["applied_mixins"], [expected_mixin])
                preset_index = payload["forward_args"].index("--preset")
                self.assertEqual(payload["forward_args"][preset_index + 1], expected_preset)
                forced = explanation["combined_forced_slots"]
                for slot, expected_ids in expected_slots.items():
                    self.assertTrue(expected_ids.issubset(set(forced.get(slot, []))), (slot, forced))
                self.assertGreaterEqual(explanation["soft_anchor_spec"]["min_anchors"], 2)

    def test_beastkin_concept_rotates_liminal_bundles_and_preserves_role(self):
        seen_aspects = set()
        expected_by_seed = {
            "1": "motion_logic",
            "3": "shadow_reflection",
            "5": "body_transition",
            "9": "sensory_othering",
        }
        for seed, expected_aspect in expected_by_seed.items():
            with self.subTest(seed=seed):
                payload = self.run_wrapper_json(
                    "--concept",
                    "카리나 메이드 수인",
                    "--selection-mode",
                    "rule",
                    "--seed",
                    seed,
                    "--explain-concept",
                )
                concept = payload["concepts"][0]
                self.assertEqual(concept["role"], "메이드")
                self.assertEqual(concept["applied_mixins"], ["수인"])
                self.assertEqual(len(concept["selected_bundles"]), 1)
                bundle = concept["selected_bundles"][0]
                self.assertEqual(bundle["aspect"], expected_aspect)
                seen_aspects.add(bundle["aspect"])
                forced = concept["combined_forced_slots"]
                self.assertEqual(forced["costume_style"], ["frill_apron_maid_costume"])
                self.assertNotIn("beastkin_tailored_folk_costume", forced["costume_style"])
                self.assertIn("beastkin_subject", forced["subject"])
                # 표정/텍스처/소품은 종 variant가 종에 맞는 단일 값으로 핀한다.
                self.assertEqual(len(forced.get("expression", [])), 1)
                self.assertIn(
                    forced["expression"][0],
                    {
                        "slit_pupil_intense_gaze",
                        "side_set_prey_alert_gaze",
                        "round_unblinking_bird_gaze",
                        "round_pupil_quiet_predator_focus",
                    },
                )
                self.assertEqual(len(forced.get("texture", [])), 1)
                self.assertIn(
                    forced["texture"][0],
                    {
                        "fur_patch_skin_blend",
                        "feather_skin_follicle_blend",
                        "scale_skin_gradient_patch",
                        "velvet_antler_skin_texture",
                        "damp_fur_sheen_boundary",
                    },
                )
                beastkin_props = set(forced.get("prop", [])) & {
                    "pointed_ear_tail_set_prop",
                    "single_feather_trace_prop",
                }
                self.assertLessEqual(len(beastkin_props), 1)
                self.assertIn("anatomical_connection", forced)
                self.assertIn("body_evidence_region", forced)
                self.assertEqual(len(concept["selected_species_variants"]), 1)
                self.assertTrue(
                    {
                        "bestiality",
                        "dehumanizing caricature",
                        "full animal mascot suit",
                    }.issubset(set(concept["soft_anchor_spec"]["safety_negative_floor"]))
                )
                self.assertGreaterEqual(concept["soft_anchor_spec"]["min_anchors"], 2)
        self.assertEqual(seen_aspects, {"motion_logic", "shadow_reflection", "sensory_othering", "body_transition"})

    def test_beastkin_species_variants_are_deterministic_diverse_and_aliasable(self):
        first = self.run_wrapper_json(
            "--concept",
            "카리나 메이드 수인",
            "--selection-mode",
            "rule",
            "--seed",
            "23",
            "--explain-concept",
        )["concepts"][0]
        repeated = self.run_wrapper_json(
            "--concept",
            "카리나 메이드 수인",
            "--selection-mode",
            "rule",
            "--seed",
            "23",
            "--explain-concept",
        )["concepts"][0]
        self.assertEqual(first["selected_species_variants"], repeated["selected_species_variants"])
        self.assertEqual(first["selected_bundles"], repeated["selected_bundles"])

        variant_ids = set()
        bundle_aspects = set()
        for seed in range(1, 25):
            payload = self.run_wrapper_json(
                "--concept",
                "수인",
                "--selection-mode",
                "rule",
                "--seed",
                str(seed),
                "--explain-concept",
            )
            concept = payload["concepts"][0]
            variant_ids.add(concept["selected_species_variants"][0]["variant_id"])
            bundle_aspects.add(concept["selected_bundles"][0]["aspect"])
            self.assertEqual(concept["combined_forced_slots"]["subject"], ["beastkin_subject"])
        self.assertGreaterEqual(len(variant_ids), 4)
        self.assertEqual(bundle_aspects, {"body_transition", "motion_logic", "sensory_othering", "shadow_reflection"})

        rabbit = self.run_wrapper_json(
            "--concept",
            "유나 토끼 수인",
            "--selection-mode",
            "rule",
            "--seed",
            "9",
            "--explain-concept",
        )["concepts"][0]
        owl = self.run_wrapper_json(
            "--concept",
            "장원영 올빼미 수인",
            "--selection-mode",
            "rule",
            "--seed",
            "9",
            "--explain-concept",
        )["concepts"][0]
        self.assertEqual(rabbit["selected_species_variants"][0]["variant_id"], "rabbit_hare")
        self.assertEqual(owl["selected_species_variants"][0]["variant_id"], "avian_owl_raptor_corvid")

    def test_beastkin_santa_and_sportswear_preserve_role_priority(self):
        cases = [
            (
                "김채원 산타복 수인",
                {
                    "costume_style": {"covered_santa_fur_trim_costume"},
                    "prop": {"modest_wrapped_gift_prop", "christmas_lights_prop", "gift_tag_ledger_prop"},
                    "location": {"christmas_market_lights", "seoul_bus_stop_snow"},
                    "action": {"brisk_gift_handoff_pose"},
                },
                "santa_role_floor",
                "covered red fur-trim Santa costume",
            ),
            (
                "카즈하 운동복 수인",
                {
                    "wardrobe_style": {"covered_track_jacket_training_set"},
                    "prop": {"stopwatch_training_prop"},
                    "location": {"gym_track", "track_lane_stadium"},
                    "action": {"sprint_start_drive"},
                },
                "sportswear_role_floor",
                "covered track jacket",
            ),
        ]
        for concept_text, expected_slots, priority_id, requirement_text in cases:
            with self.subTest(concept=concept_text):
                payload = self.run_wrapper_json(
                    "--concept",
                    concept_text,
                    "--selection-mode",
                    "rule",
                    "--seed",
                    "17",
                    "--explain-concept",
                )
                concept = payload["concepts"][0]
                self.assertEqual(concept["applied_mixins"], ["수인"])
                self.assertEqual(len(concept["selected_species_variants"]), 1)
                forced = concept["combined_forced_slots"]
                for slot, expected_ids in expected_slots.items():
                    self.assertTrue(expected_ids.issubset(set(forced.get(slot, []))), (slot, forced))
                self.assertIn("beastkin_subject", forced["subject"])
                # 신체 소품은 종에 따라 0~1개만 추가된다(역할 소품은 expected_slots에서 검증).
                beastkin_props = set(forced.get("prop", [])) & {
                    "pointed_ear_tail_set_prop",
                    "single_feather_trace_prop",
                }
                self.assertLessEqual(len(beastkin_props), 1)
                spec = concept["soft_anchor_spec"]
                priority_ids = {group["id"] for group in spec["render_priority_terms"]}
                self.assertIn(priority_id, priority_ids)
                self.assertIn("beastkin_species_specificity", priority_ids)
                self.assertEqual(spec["dual_read_requirement"]["min_role_hits"], 2)
                self.assertIn(requirement_text, "\n".join(payload["forward_args"]))

    def test_perspective_concept_expansion_presets_slots_roles_and_mixins_are_registered(self):
        preset_ids = {preset["id"] for preset in self.data["presets"]}
        family_ids = {family["id"] for family in self.data.get("preset_families", [])}

        self.assertTrue(
            {
                "fur_boundary_macro_portrait",
                "bus_seat_distance_candid",
                "id_check_counter_tension",
                "shop_window_species_reflection",
                "same_beastkin_three_scenes_series",
                "police_traffic_control_documentary",
                "santa_gift_logistics_warehouse",
                "grocery_run_two_baskets_candid",
                "costume_workshop_fitting_pins",
                "server_room_human_scale_portrait",
                "pov_hands_repairing_watch",
            }.issubset(preset_ids)
        )
        self.assertTrue(
            {
                "beastkin_body_evidence_family",
                "beastkin_social_otherness_family",
                "beastkin_reflection_duality_family",
                "procedural_duty_family",
                "companion_daily_errand_family",
                "bunny_stagecraft_family",
                "anti_diagram_photo_anchor_family",
                "first_person_task_pov_family",
            }.issubset(family_ids)
        )

        expected_slots = {
            "species_marker": {"snake_smooth_scale_neckline", "caprine_horizontal_pupil_small_horns"},
            "transition_stage": {"boundary_stage_visible_skin_shift", "mid_shift_stage_opt_in"},
            "social_cue": {"empty_adjacent_seat", "species_access_signage"},
            "reflection_logic": {"species_truth_reflection", "cctv_other_self"},
            "procedure_step": {"identity_verification", "safety_inspection"},
            "duty_prop_state": {"checklist_half_ticked", "access_card_scanned"},
            "frame_anchor_medium": {"single_camera_perspective", "screen_out_of_focus_anchor"},
        }
        for slot, ids in expected_slots.items():
            with self.subTest(slot=slot):
                self.assertTrue(ids.issubset({entry["id"] for entry in self.data["slots"][slot]}))

        self.assertIn("anti_diagram", self.data["negative_prompt_pools"])
        self.assertIn("anti_costume_shortcut", self.data["negative_prompt_pools"])

        recipes = json.loads((SKILL_DIR / "assets" / "concept_recipes.json").read_text(encoding="utf-8"))
        self.assertTrue(
            {
                "조향사",
                "시계 수리공",
                "문화재 복원가",
                "수어 통역사",
                "무대조명 디자이너",
                "인형극사",
            }.issubset(recipes["roles"])
        )
        self.assertTrue(
            {
                "파수꾼",
                "이방인",
                "중재자",
                "목격자",
                "직업적 완벽주의",
                "사수-부사수",
                "단골과 주인",
            }.issubset(recipes["mixins"])
        )

    def test_beastkin_opt_in_species_are_alias_only_and_force_species_marker(self):
        opt_in_seen = set()
        for seed in range(1, 80):
            concept = self.run_wrapper_json(
                "--concept",
                "수인",
                "--selection-mode",
                "rule",
                "--seed",
                str(seed),
                "--explain-concept",
            )["concepts"][0]
            variants = concept["selected_species_variants"]
            self.assertEqual(len(variants), 1)
            if variants[0]["tier"] == "opt_in":
                opt_in_seen.add(variants[0]["variant_id"])
        self.assertEqual(opt_in_seen, set())

        snake = self.run_wrapper_json(
            "--concept",
            "뱀 수인",
            "--selection-mode",
            "rule",
            "--seed",
            "11",
            "--explain-concept",
        )["concepts"][0]
        self.assertEqual(snake["selected_species_variants"][0]["variant_id"], "snake_serpent")
        self.assertEqual(snake["selected_species_variants"][0]["tier"], "opt_in")
        self.assertTrue(snake["selected_species_variants"][0]["opt_in_activated"])
        self.assertIn("snake_smooth_scale_neckline", snake["combined_forced_slots"]["species_marker"])

    def test_anti_diagram_negative_pool_is_context_attached(self):
        item = self.generate(
            "server_room_human_scale_portrait",
            seed=1510,
            include_negative=True,
            negative_count=3,
        )

        self.assertIn("diagram layout", item["negative_en"])
        self.assertIn("floating UI panels", item["negative_en"])
        self.assertIn("screen-only frontal close-up", item["negative_en"])

    def test_new_perspective_slots_render_into_prompt(self):
        item = self.generate(
            "fur_boundary_macro_portrait",
            seed=1511,
            forced_choices={
                "subject": ["beastkin_subject"],
                "species_marker": ["canid_mobile_ears_tail_counterbalance"],
                "transition_stage": ["boundary_stage_visible_skin_shift"],
                "composition": ["body_part_evidence_crop"],
                "safety_profile": ["beastkin_dignity_profile"],
            },
            include_negative=False,
        )

        prompt = item["prompt_en"]
        self.assertIn("mobile canid ears and weighted tail balance", prompt)
        self.assertIn("visible boundary-stage skin to trait shift", prompt)
        self.assertIn("body-part evidence crop", prompt)
        self.assertIn("beastkin dignity profile", prompt)

    def test_wide_archetype_presets_tags_roles_and_mixins_are_registered(self):
        preset_ids = {preset["id"] for preset in self.data["presets"]}
        family_ids = {family["id"] for family in self.data.get("preset_families", [])}
        self.assertTrue(
            {
                "contract_exchange_table_portrait",
                "judgement_packet_portrait",
                "digital_void_server_room_preset",
                "urban_shrine_convenience_preset",
                "oracle_vision_portrait",
                "two_person_rival_reflection",
                "transformation_midstage_portrait",
                "feral_moon_threshold_portrait",
                "obsessive_collection_shelf",
                "gravity_defiance_portrait",
            }.issubset(preset_ids)
        )
        self.assertTrue(
            {
                "contract_symbolic_exchange_family",
                "modern_power_authority_family",
                "surveillance_control_family",
                "digital_void_family",
                "urban_folk_shrine_family",
                "psychological_double_family",
                "obsessive_collection_family",
                "gravity_defiance_family",
            }.issubset(family_ids)
        )

        expected_slot_ids = {
            "prop": {
                "red_seal_contract_prop",
                "soul_ledger_book_prop",
                "corrupted_receipt_prop",
                "sealed_verdict_packet_prop",
                "scrying_mirror_prop",
                "encrypted_drive_prop",
                "auction_gavel_prop",
                "calculator_ledger_prop",
            },
            "action": {
                "signing_invisible_contract",
                "stamping_verdict_packet",
                "watching_offscreen_monitor",
                "awed_upward_gaze",
                "dealing_cards_precisely",
                "reviewing_ledger_columns",
            },
            "location": {
                "corporate_high_floor_office",
                "server_room_aisle",
                "surveillance_control_room",
                "urban_shrine_corner",
                "archive_stacks",
                "casino_table_room",
                "insurance_claims_office",
            },
            "composition": {
                "first_person_contract_handoff",
                "document_foreground_face_background",
                "mirror_mismatch_same_frame",
                "cctv_low_corner_view",
                "low_angle_authority_frame",
                "leaf_foreground_bokeh",
            },
            "lighting": {
                "archive_desk_lamp",
                "god_ray_threshold_light",
                "threshold_sliver_light",
                "server_rack_blue_light",
                "phone_notification_pulse",
            },
            "mood": {
                "procedural_damnation",
                "friendly_unease",
                "bureaucratic_horror",
                "technological_haunting",
                "predatory_stillness",
                "urban_legend_wrongness",
            },
            "subject": {
                "prosecutor_role_model",
                "judge_role_model",
                "lawyer_role_model",
                "hacker_operator",
                "call_center_agent",
                "casino_dealer_role_model",
                "accountant_role_model",
            },
        }
        for slot, expected_ids in expected_slot_ids.items():
            with self.subTest(slot=slot):
                actual = {entry["id"] for entry in self.data["slots"][slot]}
                self.assertTrue(expected_ids.issubset(actual), slot)

        recipes = json.loads((SKILL_DIR / "assets" / "concept_recipes.json").read_text(encoding="utf-8"))
        self.assertTrue(
            {
                "검사",
                "판사",
                "변호사",
                "해커",
                "콜센터 상담원",
                "카지노 딜러",
                "경매사",
                "역무원",
                "회계사",
                "보험조사원",
                "회사원",
                "산타복",
                "운동복",
            }.issubset(recipes["roles"])
        )
        self.assertTrue(
            {
                "트릭스터",
                "현자",
                "방랑자",
                "구원자",
                "배신자",
                "수집가",
                "권력자",
                "예언자",
                "치유자",
                "계약자",
                "도시전설",
                "회사원",
            }.issubset(recipes["mixins"])
        )

    def test_role_specific_mixin_bundles_preserve_role_anchors_and_do_not_leak(self):
        miko = self.run_wrapper_json(
            "--concept",
            "카리나 무녀 구미호",
            "--selection-mode",
            "rule",
            "--seed",
            "17",
            "--explain-concept",
        )["concepts"][0]
        self.assertEqual(miko["selected_bundles"][0]["bundle_id"], "gumiho_무녀_facet")
        self.assertTrue(
            {
                "shaman_bells_prop",
                "five_color_silk_strip_prop",
                "fox_fire_wisp_prop",
            }.issubset(set(miko["combined_forced_slots"]["prop"]))
        )

        archivist = self.run_wrapper_json(
            "--concept",
            "지젤 기록가 환경침식",
            "--selection-mode",
            "rule",
            "--seed",
            "17",
            "--explain-concept",
        )["concepts"][0]
        self.assertEqual(archivist["selected_bundles"], [])
        self.assertEqual(archivist["combined_forced_slots"]["location"][0], "grand_archive_hall")

        researcher = self.run_wrapper_json(
            "--concept",
            "윈터 연구원 데이터망령",
            "--selection-mode",
            "rule",
            "--seed",
            "17",
            "--explain-concept",
        )["concepts"][0]
        self.assertEqual(researcher["role"], "연구원")
        self.assertEqual(researcher["selected_bundles"], [])
        self.assertEqual(researcher["combined_forced_slots"]["location"][0], "clinical_observation_lab")

    def test_new_roles_and_archetypes_resolve_to_visible_slots(self):
        cases = [
            (
                "카리나 검사 계약자",
                "검사",
                "계약자",
                {"subject": {"prosecutor_role_model"}, "prop": {"sealed_verdict_packet_prop", "red_seal_contract_prop"}},
            ),
            (
                "윈터 해커 도시전설",
                "해커",
                "도시전설",
                {"subject": {"hacker_operator"}, "location": {"server_room_aisle", "midnight_convenience_store_aisle"}, "prop": {"encrypted_drive_prop", "corrupted_receipt_prop"}},
            ),
            (
                "닝닝 회계사 권력자",
                "회계사",
                "권력자",
                {"subject": {"accountant_role_model"}, "prop": {"calculator_ledger_prop"}, "composition": {"low_angle_authority_frame"}},
            ),
            (
                "지젤 사서 현자",
                "도서관 사서",
                "현자",
                {"prop": {"soul_ledger_book_prop"}, "lighting": {"archive_desk_lamp"}},
            ),
        ]

        for concept, expected_role, expected_mixin, expected_slots in cases:
            with self.subTest(concept=concept):
                payload = self.run_wrapper_json(
                    "--concept",
                    concept,
                    "--selection-mode",
                    "rule",
                    "--seed",
                    "23",
                    "--explain-concept",
                )
                explanation = payload["concepts"][0]
                self.assertEqual(explanation["role"], expected_role)
                self.assertEqual(explanation["applied_mixins"], [expected_mixin])
                forced = explanation["combined_forced_slots"]
                for slot, expected_ids in expected_slots.items():
                    self.assertTrue(expected_ids.issubset(set(forced.get(slot, []))), (slot, forced))

    def test_all_concept_recipe_forced_slots_are_registered(self):
        recipes = json.loads((SKILL_DIR / "assets" / "concept_recipes.json").read_text(encoding="utf-8"))
        slot_ids = {slot: {entry["id"] for entry in entries} for slot, entries in self.data["slots"].items()}
        missing: list[tuple[str, str, str]] = []

        def normalize_values(value):
            if isinstance(value, str):
                return [value]
            if isinstance(value, dict):
                # Weighted pool entry: {"id": ..., "w": ...}
                entry_id = str(value.get("id") or "")
                return [entry_id] if entry_id else []
            if isinstance(value, list):
                flattened: list[str] = []
                for item in value:
                    flattened.extend(normalize_values(item))
                return flattened
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
            check_set(f"roles.{role}.anchor_pool", recipe.get("anchor_pool"))
            check_set(f"roles.{role}.primary_anchor_pool", recipe.get("primary_anchor_pool"))
        for mixin, recipe in recipes.get("mixins", {}).items():
            check_set(f"mixins.{mixin}.set", recipe.get("set"))
            check_set(f"mixins.{mixin}.anchor_pool", recipe.get("anchor_pool"))
            check_set(f"mixins.{mixin}.primary_anchor_pool", recipe.get("primary_anchor_pool"))
            for bundle in recipe.get("bundles", []):
                check_set(f"mixins.{mixin}.bundles.{bundle.get('id')}.set", bundle.get("set"))
                check_set(f"mixins.{mixin}.bundles.{bundle.get('id')}.anchor_pool", bundle.get("anchor_pool"))
                check_set(
                    f"mixins.{mixin}.bundles.{bundle.get('id')}.primary_anchor_pool",
                    bundle.get("primary_anchor_pool"),
                )

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

    def test_relationship_grammar_slots_render_in_prompt(self):
        item = self.generate(
            "tray_handoff_counter",
            seed=612,
            forced_choices={
                "subject": ["young_barista"],
                "action": ["setting_down_dessert_with_small_thunk"],
                "relational_action": ["offering_prop_with_averted_gaze"],
                "prop": ["warm_thermos_cup_prop"],
                "prop_direction": ["toward_partner_handoff"],
                "partner_role": ["off_frame_customer"],
                "partner_framing": ["partner_hand_visible_only"],
                "gaze_target": ["to_handoff_object"],
                "body_orientation": ["face_away_hands_toward_partner"],
                "proxemics": ["formal_counter_distance"],
                "contact_point": ["knuckle_tap_on_tray"],
                "intent_state": ["mid_handoff"],
                "emotional_contradiction": ["cold_face_warm_hands"],
                "viewer_position": ["viewer_as_customer"],
                "composition": ["table_edge_handover"],
                "safety_profile": ["civilian_service_profile"],
            },
            include_negative=False,
        )

        prompt = item["prompt_en"]
        for phrase in (
            "offering a prop while averting gaze",
            "directed toward the partner for handoff",
            "an off-frame customer",
            "partner hand visible only",
            "face turned away while hands move toward the partner",
            "mid-handoff moment",
            "cold face with warm hands",
            "viewer as customer POV",
            "civilian service anti body-display safety profile",
        ):
            self.assertIn(phrase, prompt)

    def test_visible_multi_subject_slots_render_and_drop_duplicate_faces_negative(self):
        item = self.generate(
            "contract_exchange_table_portrait",
            seed=1401,
            forced_choices={
                "subject": ["office_worker"],
                "partner_role": ["in_frame_counterparty"],
                "partner_framing": ["two_faces_visible_medium_shot"],
                "composition": ["first_person_contract_handoff"],
            },
            include_negative=True,
            negative_count=99,
        )

        prompt = item["prompt_en"]
        self.assertIn("an in-frame counterparty seated across from the subject", prompt)
        self.assertIn("two faces visible in a medium shot", prompt)
        self.assertNotIn("duplicate faces", item["negative_en"])
        self.assertIn("unrealistic hands", item["negative_en"])

    def test_single_subject_presets_do_not_auto_select_visible_partner_slots(self):
        item = self.generate(
            "street_documentary",
            seed=1402,
            forced_choices={
                "subject": ["office_worker"],
            },
            include_negative=True,
            negative_count=99,
        )

        self.assertNotIn("partner_role", item["choices"])
        self.assertNotIn("partner_framing", item["choices"])
        self.assertIn("duplicate faces", item["negative_en"])
        self.assertNotIn("in-frame counterparty", item["prompt_en"])
        self.assertNotIn("two faces visible", item["prompt_en"])

    def test_priority_multi_subject_presets_accept_visible_partner_framing(self):
        cases = {
            "contract_exchange_table_portrait": ("in_frame_counterparty", "face_to_face_table_two_shot"),
            "hand_to_hand_envelope_drop": ("in_frame_recipient", "two_faces_visible_medium_shot"),
            "two_person_rival_reflection": ("in_frame_rival", "foreground_background_power_two_shot"),
            "shared_umbrella_two_shot": ("in_frame_companion", "side_by_side_two_shot"),
        }

        for index, (preset, (role_id, framing_id)) in enumerate(cases.items(), start=1):
            with self.subTest(preset=preset):
                item = self.generate(
                    preset,
                    seed=1410 + index,
                    forced_choices={
                        "subject": ["office_worker"],
                        "partner_role": [role_id],
                        "partner_framing": [framing_id],
                    },
                    include_negative=False,
                )

                self.assertEqual(item["choices"]["partner_role"]["id"], role_id)
                self.assertEqual(item["choices"]["partner_framing"]["id"], framing_id)
                self.assertIn("in-frame", item["prompt_en"])
                self.assertTrue(
                    "two-shot" in item["prompt_en"] or "two faces visible" in item["prompt_en"],
                    item["prompt_en"],
                )

    def test_small_group_documentary_preset_supports_visible_group_framing(self):
        item = self.generate(
            "small_group_interaction_documentary",
            seed=1420,
            forced_choices={
                "subject": ["office_worker"],
                "partner_role": ["in_frame_companion"],
                "partner_framing": ["small_group_visible_midshot"],
            },
            include_negative=True,
            negative_count=99,
        )

        self.assertEqual(item["choices"]["partner_framing"]["id"], "small_group_visible_midshot")
        self.assertIn("small visible group of three to five people in a mid-shot", item["prompt_en"])
        self.assertNotIn("duplicate faces", item["negative_en"])

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
        self.assertEqual(self.generator.axis_families_for_text("urban city street", self.data), ["urban"])
        self.assertEqual(self.generator.axis_families_for_text("방구석 집돌이 작은 방 게임패드", self.data), ["homebody_room"])
        self.assertEqual(self.generator.axis_families_for_text("horror nightmare portrait", self.data), ["human", "horror"])
        context = {
            "semantic_policy": self.data["semantic_policy"],
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
            "semantic_policy": self.data["semantic_policy"],
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
            "semantic_policy": self.data["semantic_policy"],
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
            "semantic_policy": self.data["semantic_policy"],
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

    def test_policy_match_rule_supports_terms_tokens_boundary_and_case(self):
        entry = {
            "id": "programmer_room",
            "en": "Programmer in a Gaming Room",
            "tags": ["gaming", "interior"],
            "facets": {"style": ["casual"]},
        }

        combined = self.generator.evaluate_match(
            {
                "id": "subject-combined",
                "any_tokens": ["gaming"],
                "all_terms": ["room"],
                "boundary": True,
            },
            entry,
        )
        self.assertTrue(combined["matched"])
        self.assertEqual(combined["matched_rule_id"], "subject-combined")
        self.assertIn("gaming", combined["matched_tokens"])
        self.assertIn("room", combined["matched_terms"])

        self.assertFalse(
            self.generator.evaluate_match({"any_terms": ["gamer"], "boundary": True}, entry)["matched"]
        )
        self.assertTrue(self.generator.evaluate_match({"any_terms": ["gaming"]}, entry)["matched"])
        self.assertFalse(
            self.generator.evaluate_match({"any_terms": ["gaming"], "case_sensitive": True}, entry)["matched"]
        )

    def test_semantic_preset_family_coverage_rewards_horror_signal(self):
        rules = self.data["coherence_rules"]
        context = {
            "semantic_policy": self.data["semantic_policy"],
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
            "semantic_policy": self.data["semantic_policy"],
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
            "semantic_policy": self.data["semantic_policy"],
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
            "semantic_policy": self.data["semantic_policy"],
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
            "semantic_policy": self.data["semantic_policy"],
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
            "semantic_policy": self.data["semantic_policy"],
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
        prop_decision = next(
            decision
            for decision in context["intent_steering"]["decisions"]
            if decision["slot"] == "prop" and decision["reason"] == "homebody_room_prop"
        )
        self.assertEqual(
            {key: prop_decision[key] for key in ("slot", "reason", "before", "after", "tier")},
            {"slot": "prop", "reason": "homebody_room_prop", "before": 4, "after": 2, "tier": "core"},
        )
        self.assertEqual(prop_decision["family"], "homebody_room")
        self.assertEqual(prop_decision["signal_tier"], "core")
        self.assertIn("policy_id", prop_decision)
        self.assertEqual(prop_decision["reason_code"], "homebody_room_prop")
        self.assertEqual(prop_decision["policy_schema_version"], 1)
        self.assertIn("semantic_policy_hash", prop_decision)
        self.assertEqual(prop_decision["matched_via"], "semantic_policy.families.homebody_room.slot_signals.prop.core")
        self.assertNotEqual(prop_decision["matched_via"], "default_fallback")
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
        policy_context = {"semantic_policy": self.data["semantic_policy"]}

        for entry_id in {
            "game_controller_prop",
            "messy_snacks_prop",
            "rumpled_blanket_prop",
            "instant_ramen_cup_prop",
            "energy_drink_cans_prop",
            "tangled_charging_cables_prop",
            "gaming_headset_on_desk_prop",
        }:
            self.assertEqual(self.generator.homebody_room_signal_tier(by_slot["prop"][entry_id], "prop", policy_context), "core")

        for entry_id in {"small_messy_gaming_bedroom", "dim_monitor_glow_bedroom", "floor_mattress_gaming_corner"}:
            self.assertEqual(self.generator.homebody_room_signal_tier(by_slot["location"][entry_id], "location", policy_context), "core")
        self.assertEqual(self.generator.homebody_room_signal_tier(by_slot["world"]["lived_in_homebody_room"], "world", policy_context), "core")

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
            self.assertIsNone(self.generator.homebody_room_signal_tier(by_slot[slot][entry_id], slot, policy_context))

    def test_homebody_concept_lock_promotes_core_slot_candidates(self):
        context = {
            "semantic_policy": self.data["semantic_policy"],
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

    def test_rule_mode_rejects_intent_even_with_policy_available(self):
        with self.assertRaisesRegex(ValueError, "--intent cannot be used with --selection-mode rule"):
            self.generate(
                "interior_lifestyle",
                seed=20260606,
                intent="homebody gamer in a small bedroom",
                selection_mode="rule",
                concept_locks=["방구석 집돌이, 작은 방, 모니터 빛, 게임패드"],
                include_trace=True,
            )

    def test_rule_quality_reports_semantic_relevance_not_evaluated(self):
        concept = "방구석 집돌이, 작은 방, 모니터 빛, 게임패드"
        item = self.generate(
            "interior_lifestyle",
            seed=20260607,
            selection_mode="rule",
            concept_locks=[concept],
            include_trace=True,
            include_negative=False,
        )

        self.assertEqual(item["quality"]["semantic_relevance"], "not_evaluated")
        self.assertIn(item["quality"]["verdict"], {"pass", "warn"})
        concept_check = next(check for check in item["quality"]["checks"] if check["id"] == "concept_lock_rendered")
        self.assertEqual(concept_check["status"], "pass")

    def test_rule_policy_bias_uses_concept_lock_policy_without_filtering_pool(self):
        concept = "방구석 집돌이, 작은 방, 모니터 빛, 게임패드, 간식, 담요"
        preset = next(item for item in self.data["presets"] if item["id"] == "interior_lifestyle")
        contract = self.generator.make_generation_contract(
            self.data,
            preset,
            {},
            {},
            concept_locks=[concept],
        )
        by_slot = {slot: {item["id"]: item for item in entries} for slot, entries in self.data["slots"].items()}
        props = [
            by_slot["prop"]["coffee_cup_prop"],
            by_slot["prop"]["game_controller_prop"],
            by_slot["prop"]["messy_snacks_prop"],
        ]

        biased = self.generator.apply_rule_policy_bias("prop", props, self.data, contract)
        weights = {item["id"]: float(item.get("weight", 1)) for item in biased}

        self.assertEqual([item["id"] for item in biased], [item["id"] for item in props])
        self.assertGreater(weights["game_controller_prop"], weights["coffee_cup_prop"])
        self.assertGreater(weights["messy_snacks_prop"], weights["coffee_cup_prop"])
        event = contract["rule_policy_bias"][0]
        self.assertEqual(event["reason_code"], "rule_policy_concept_lock_bias")
        self.assertIn("homebody_room", event["active_families"])
        self.assertEqual(event["policy_schema_version"], 1)
        self.assertIn("semantic_policy_hash", event)
        self.assertTrue(
            all(item.get("matched_via") != "default_fallback" for item in event["boosted"])
        )

    def test_homebody_prop_dedupes_detail_already_carried_by_action(self):
        context = {
            "semantic_policy": self.data["semantic_policy"],
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
            "semantic_policy": self.data["semantic_policy"],
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

        delimiter = self.generator.extract_intent_axes("urban + horror, fantasy and human", semantic_axis_mode="auto", policy_source=self.data)
        self.assertEqual(delimiter["source"], "delimiter")
        self.assertEqual([item["text"] for item in delimiter["items"]], ["urban", "horror", "fantasy", "human"])

        fallback = self.generator.extract_intent_axes("urban horror fantasy human portrait", semantic_axis_mode="auto", policy_source=self.data)
        self.assertEqual(fallback["source"], "fallback")
        self.assertEqual(
            [item["text"] for item in fallback["items"]],
            ["human portrait", "urban city street", "horror fear nightmare", "fantasy magic surreal"],
        )
        product_axes = self.generator.extract_intent_axes("jewelry macro reflection product", semantic_axis_mode="auto", policy_source=self.data)
        self.assertIn("product commercial packshot", [item["text"] for item in product_axes["items"]])
        self.assertIn("jewelry macro reflection", [item["text"] for item in product_axes["items"]])
        homebody_axes = self.generator.extract_intent_axes("방구석 집돌이 작은 방 게임패드", semantic_axis_mode="auto", policy_source=self.data)
        self.assertIn("homebody gamer in a small bedroom", [item["text"] for item in homebody_axes["items"]])
        self.assertIn("metropolitan environment", self.generator.semantic_axis_embedding_text("urban", self.data))
        self.assertIn("gaming desk", self.generator.semantic_axis_embedding_text("방구석 집돌이", self.data))
        self.assertIn("readable face", self.generator.semantic_axis_embedding_text("human portrait", self.data))
        self.assertIn("polished metal", self.generator.semantic_axis_embedding_text("jewelry macro reflection", self.data))

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
            "semantic_policy": self.data["semantic_policy"],
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

    def test_role_scene_policy_records_and_prefers_least_used_location(self):
        ledger = {}
        result = {
            "choices": {"location": {"id": "traffic_crossing_rain"}},
            "semantic_trace": {
                "generation_contract": {
                    "soft_anchor_policy": {
                        "enabled": True,
                        "role_scene_policy": {
                            "enabled": True,
                            "allowed_locations": [
                                "traffic_crossing_rain",
                                "city_intersection_night",
                            ],
                        },
                    }
                }
            },
        }
        self.generator.update_anchor_diversity_ledger(ledger, result)
        self.assertEqual(ledger["location"]["traffic_crossing_rain"], 1)

        contract = {
            "soft_anchor_policy": {
                "role_scene_policy": {
                    "enabled": True,
                    "role_first": True,
                    "enforce": True,
                    "allowed_locations": [
                        "traffic_crossing_rain",
                        "city_intersection_night",
                    ],
                }
            }
        }
        context = {"anchor_diversity_ledger": ledger}
        pool = [
            {"id": "traffic_crossing_rain", "weight": 100.0},
            {"id": "city_intersection_night", "weight": 1.0},
            {"id": "highland_pasture", "weight": 1.0},
        ]
        adjusted = self.generator.apply_role_scene_policy("location", pool, context, contract)
        self.assertEqual([item["id"] for item in adjusted], ["city_intersection_night"])

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

    def test_dictionary_validator_rejects_unknown_semantic_policy_id(self):
        data = json.loads(TAGS_PATH.read_text(encoding="utf-8"))
        data["semantic_policy"]["families"]["homebody_room"]["slot_signals"]["prop"]["core"].append("missing_prop_id")

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
        self.assertIn(
            "semantic_policy.families.homebody_room.slot_signals.prop.core: unknown prop id missing_prop_id",
            result.stderr,
        )

    def test_dictionary_validator_rejects_runtime_process_metadata(self):
        data = json.loads(TAGS_PATH.read_text(encoding="utf-8"))
        data["presets"][0]["embedding_text"] = (
            "source-grounded visual taxonomy copied from a cited interview study"
        )

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
        self.assertIn("runtime metadata boundary", result.stderr)
        self.assertIn("source_grounded", result.stderr)
        self.assertIn("cited_study", result.stderr)

    def test_dictionary_validator_rejects_control_language_in_visual_scene_atoms(self):
        data = json.loads(TAGS_PATH.read_text(encoding="utf-8"))
        extension = {
            "existing_preset_render_contract_extensions": {
                "portrait_editorial": {
                    "scene_blueprints": [
                        {
                            "id": "invalid_control_instruction",
                            "subject": "two adults",
                            "action": "keeping the market term nonvisual",
                            "location": "a blank studio",
                            "prop": "one plain object",
                        }
                    ]
                }
            }
        }

        with tempfile.TemporaryDirectory() as tmp:
            tags_path = Path(tmp) / "invalid_tags.json"
            extension_path = Path(tmp) / "photo_prompt_scene_expression_character_moe.json"
            tags_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            extension_path.write_text(json.dumps(extension, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(VALIDATOR_PATH), "--tags", str(tags_path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("runtime visual atom boundary", result.stderr)
        self.assertIn("market_control_language", result.stderr)
        self.assertIn("nonvisual_instruction", result.stderr)

    def test_dictionary_validator_rejects_control_language_in_public_visual_text(self):
        data = json.loads(TAGS_PATH.read_text(encoding="utf-8"))
        data["presets"][0]["embedding_text"] = (
            "route a market label through nonvisual provenance metadata using "
            "rights-cleared and copyrighted status language; prefer a Japanese-market variant "
            "for audience interest"
        )

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
        self.assertIn("runtime public visual text boundary", result.stderr)
        self.assertIn("provenance_language", result.stderr)
        self.assertIn("market_control_language", result.stderr)
        self.assertIn("nonvisual_instruction", result.stderr)
        self.assertIn("rights_status_language", result.stderr)
        self.assertIn("copyright_status_language", result.stderr)
        self.assertIn("market_comparison_language", result.stderr)
        self.assertIn("audience_priority_language", result.stderr)

    def test_dictionary_validator_rejects_invalid_semantic_policy_match_rule(self):
        data = json.loads(TAGS_PATH.read_text(encoding="utf-8"))
        data["semantic_policy"]["families"]["human"]["signal_lexicon"]["strong"].append(
            {"id": "bad-rule", "boundary": "yes"}
        )

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
        self.assertIn(
            "semantic_policy.families.human.signal_lexicon.strong[8]: any_terms, all_terms, any_tokens, or all_tokens is required",
            result.stderr,
        )
        self.assertIn("semantic_policy.families.human.signal_lexicon.strong[8].boundary: must be a boolean", result.stderr)

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

    def test_dictionary_validator_rejects_unknown_motif_pool_slot_id(self):
        data = json.loads(TAGS_PATH.read_text(encoding="utf-8"))
        recipes_path = SKILL_DIR / "assets" / "concept_recipes.json"
        recipes = json.loads(recipes_path.read_text(encoding="utf-8"))
        recipes["mixins"]["얀데레"]["motif_pools"] = {
            "bad_pool": {
                "axis": "surveillance_gaze",
                "slot_candidates": {"prop": ["missing_prop_id"]},
                "terms": ["bad pool"],
            }
        }

        with tempfile.TemporaryDirectory() as tmp:
            tags_path = Path(tmp) / "tags.json"
            recipes_tmp_path = Path(tmp) / "concept_recipes.json"
            tags_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            recipes_tmp_path.write_text(json.dumps(recipes, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(VALIDATOR_PATH),
                    "--tags",
                    str(tags_path),
                    "--concept-recipes",
                    str(recipes_tmp_path),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "concept_recipes.mixins.얀데레.motif_pools.bad_pool.slot_candidates.prop: unknown id missing_prop_id",
            result.stderr,
        )

    def test_semantic_text_uses_only_public_visual_language(self):
        entry = {
            "id": "internal_source_document_id",
            "en": "visible ceramic cup",
            "ko": "보이는 세라믹 컵",
            "embedding_text": "a handmade ceramic cup with a chipped blue glaze",
            "aliases": ["blue glazed cup"],
            "keywords": ["ceramic vessel"],
            "terms": ["small handle"],
            "tags": ["cited_study_marker"],
            "kind": ["market_researched_marker"],
            "facets": {"content_basis": ["source_grounded_marker"]},
        }

        text = self.generator.semantic_text_for_entry(entry, "subject")

        self.assertIn("handmade ceramic cup", text)
        self.assertIn("visible ceramic cup", text)
        self.assertIn("보이는 세라믹 컵", text)
        self.assertIn("blue glazed cup", text)
        self.assertIn("ceramic vessel", text)
        self.assertIn("small handle", text)
        self.assertNotIn("internal_source_document_id", text)
        self.assertNotIn("cited_study_marker", text)
        self.assertNotIn("market_researched_marker", text)
        self.assertNotIn("source_grounded_marker", text)
        self.assertNotIn("content_basis", text)

    def test_all_semantic_inputs_exclude_control_and_process_metadata(self):
        forbidden = re.compile(
            r"stable id:|facet |tags:|kind:|source[-_ ]grounded|"
            r"(?:public|cjk)[-_ ]market[-_ ]researched|research[-_ ](?:backed|based|router)|"
            r"cited(?:[-_ ]interview)?[-_ ]study|nonvisual[-_ ]provenance|"
            r"provenance_scope|\bprovenance\b|moe[-_ ]review|모에\s*리뷰|萌えレビュー|"
            r"rights[-_ ]cleared|\bcopyrighted\b|권리\s*(?:확인|정리)|"
            r"(?:japanese|korean|chinese|cjk)[-_ ]market[-_ ](?:variant|comparison)|"
            r"audience[-_ ](?:interest|preference|appeal|priority)|"
            r"(?:시청자|관객)\s*(?:흥미|선호|관심)",
            re.IGNORECASE,
        )
        failures = []
        rows = self.generator.iter_semantic_entries(self.generator.load_json(TAGS_PATH))
        for key, kind, entry, slot in rows:
            text = self.generator.semantic_text_for_entry(entry, slot, kind=kind)
            match = forbidden.search(text)
            if match:
                failures.append((key, match.group(0), text[:240]))

        self.assertEqual(len(rows), 6910)
        self.assertEqual(failures, [])

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
        self.assertIn(
            self.generator.SEMANTIC_TEXT_RECIPE_VERSION,
            result.stdout,
        )

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

    def test_semantic_policy_only_change_does_not_change_dictionary_hash(self):
        data = json.loads(json.dumps(self.data, ensure_ascii=False))
        first_dictionary_hash = self.generator.dictionary_hash(data)
        first_policy_hash = self.generator.semantic_policy_digest(self.generator.semantic_policy_from_source(data))

        data["semantic_policy"]["families"]["human"]["signal_lexicon"]["strong"].append("face")
        data["semantic_policy"]["families"]["human"]["axis_embedding_text"] += " close portrait axis"

        self.assertEqual(self.generator.dictionary_hash(data), first_dictionary_hash)
        self.assertNotEqual(
            self.generator.semantic_policy_digest(self.generator.semantic_policy_from_source(data)),
            first_policy_hash,
        )

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
                first_payload["semantic_text_recipe"] = "semantic-text-older"
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
        self.assertIn("new actor", embed_calls[0][0])
        self.assertNotIn("new_actor", embed_calls[0][0])
        self.assertEqual(len(second_payload["entries"]), 3)
        self.assertEqual(
            second_payload["entries"]["preset:base_portrait"]["vector"],
            first_payload["entries"]["preset:base_portrait"]["vector"],
        )
        self.assertNotEqual(second_payload["dictionary_hash"], first_payload["dictionary_hash"])
        self.assertEqual(
            second_payload["semantic_text_recipe"],
            self.generator.SEMANTIC_TEXT_RECIPE_VERSION,
        )

    def test_semantic_index_shards_round_trip_exact_entry_order_and_values(self):
        builder = load_index_builder()
        payload = {
            "provider": "gemini",
            "dictionary_hash": "a" * 64,
            "semantic_text_recipe": self.generator.SEMANTIC_TEXT_RECIPE_VERSION,
            "embedding_model": "gemini-embedding-2",
            "embedding_dimensions": 3,
            "entries": {
                "preset:first": {"kind": "preset", "slot": None, "id": "first", "text": "first", "vector": [1.0, 0.0, 0.0]},
                "slot:subject:second": {"kind": "slot", "slot": "subject", "id": "second", "text": "second", "vector": [0.0, 1.0, 0.0]},
                "slot:location:third": {"kind": "slot", "slot": "location", "id": "third", "text": "third", "vector": [0.0, 0.0, 1.0]},
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "semantic_index.json"
            manifest = builder.write_sharded_payload(output, payload, shard_count=2)
            loaded = self.generator.load_semantic_index_payload(output)
            shard_bytes = [
                (output.parent / shard["path"]).read_bytes()
                for shard in manifest["shards"]
            ]

        self.assertNotIn("entries", manifest)
        self.assertEqual(manifest["storage"]["format"], "sharded-json-v1")
        self.assertEqual(manifest["entry_count"], 3)
        self.assertEqual(list(loaded["entries"]), list(payload["entries"]))
        self.assertEqual(loaded["entries"], payload["entries"])
        for raw in shard_bytes:
            self.assertNotIn(b"\n", raw)
            self.assertEqual(
                raw,
                json.dumps(
                    json.loads(raw),
                    ensure_ascii=False,
                    separators=(",", ":"),
                ).encode("utf-8"),
            )

    def test_semantic_index_shards_prune_only_prior_generation_directories(self):
        builder = load_index_builder()
        payload = {
            "provider": "gemini",
            "dictionary_hash": "a" * 64,
            "semantic_text_recipe": self.generator.SEMANTIC_TEXT_RECIPE_VERSION,
            "embedding_model": "gemini-embedding-2",
            "embedding_dimensions": 3,
            "entries": {
                "preset:first": {
                    "kind": "preset",
                    "slot": None,
                    "id": "first",
                    "text": "first",
                    "vector": [1.0, 0.0, 0.0],
                },
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "semantic_index.json"
            builder.write_sharded_payload(output, payload, shard_count=2)
            shard_parent = output.with_name("semantic_index_shards")
            first_generation = shard_parent / ("a" * 16)
            marker = shard_parent / "README.keep"
            marker.write_text("not a generation directory", encoding="utf-8")

            updated_payload = json.loads(json.dumps(payload))
            updated_payload["dictionary_hash"] = "b" * 64
            builder.write_sharded_payload(output, updated_payload, shard_count=2)

            self.assertFalse(first_generation.exists())
            self.assertTrue((shard_parent / ("b" * 16)).is_dir())
            self.assertEqual(marker.read_text(encoding="utf-8"), "not a generation directory")

    def test_real_compact_semantic_shards_preserve_candidate_pack_bytes(self):
        builder = load_index_builder()
        merged_data = self.generator.load_json(TAGS_PATH)
        committed_manifest = json.loads(SEMANTIC_INDEX_PATH.read_text(encoding="utf-8"))
        for shard in committed_manifest["shards"]:
            shard_path = SEMANTIC_INDEX_PATH.parent / shard["path"]
            raw = shard_path.read_bytes()
            self.assertEqual(
                raw,
                json.dumps(
                    json.loads(raw),
                    ensure_ascii=False,
                    separators=(",", ":"),
                ).encode("utf-8"),
            )
        source_index = self.generator.load_semantic_index_payload(SEMANTIC_INDEX_PATH)

        def entry_digest(entries):
            digest = hashlib.sha256()
            for key, value in entries.items():
                digest.update(
                    json.dumps(
                        [key, value],
                        ensure_ascii=False,
                        separators=(",", ":"),
                    ).encode("utf-8")
                )
                digest.update(b"\n")
            return digest.hexdigest()

        def candidate_pack_bytes(index):
            with mock.patch.object(
                self.generator,
                "embed_texts_with_gemini",
                side_effect=self.fake_gemini_vectors,
            ):
                result = self.generate(
                    None,
                    seed=20260806,
                    intent="rainy neon night street portrait",
                    selection_mode="hybrid",
                    novelty="medium",
                    include_trace=True,
                    semantic_index=index,
                    gemini_api_key="test-api-key",
                    data=merged_data,
                )
            pack = self.generator.build_candidate_pack(result, merged_data)
            return json.dumps(pack, ensure_ascii=False, separators=(",", ":")).encode("utf-8")

        source_digest = entry_digest(source_index["entries"])
        source_pack = candidate_pack_bytes(source_index)
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "semantic_index.json"
            builder.write_sharded_payload(output, source_index, shard_count=16)
            del source_index
            gc.collect()

            compact_index = self.generator.load_semantic_index_payload(output)
            compact_digest = entry_digest(compact_index["entries"])
            compact_pack = candidate_pack_bytes(compact_index)

        self.assertEqual(compact_digest, source_digest)
        self.assertEqual(compact_pack, source_pack)

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
            (scripts / "bm25f_retrieval.py").write_text(
                BM25F_RETRIEVAL_PATH.read_text(encoding="utf-8"),
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
            self.assertEqual(payload["entry_count"], 0)
            self.assertEqual(payload["storage"]["format"], "sharded-json-v1")

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
