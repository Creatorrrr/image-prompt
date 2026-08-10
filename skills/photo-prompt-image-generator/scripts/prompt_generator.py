#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Photo prompt generator
- Tags are managed in a JSON file.
- Generates Korean, English, or both using the same random choices.
- Uses presets, slot filters, weights, subject compatibility, priority-biased optional slots,
  and user-forced slot selections.

Usage examples:
  python prompt_generator.py --tags photo_prompt_tags.json --n 5 --lang both
  python prompt_generator.py --tags photo_prompt_tags.json --preset street_documentary --n 3 --seed 42
  python prompt_generator.py --tags photo_prompt_tags.json --list-presets
  python prompt_generator.py --tags photo_prompt_tags.json --show-slots
  python prompt_generator.py --tags photo_prompt_tags.json --list-tags camera_type
  python prompt_generator.py --tags photo_prompt_tags.json --preset tiktok_vertical_snapshot --set subject=influencer_creator --set person_origin=south_korea --set appearance_type=idol_like
  python prompt_generator.py --tags photo_prompt_tags.json --json-output --include-negative --include-choices --n 10 > prompts.json
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import random
import re
import sys
import time
from pathlib import Path
from typing import Any, Callable, Dict, Iterator, List, Optional, Sequence, Set

JsonDict = Dict[str, Any]
Entry = Dict[str, Any]

SURREAL_LAYER_SLOTS = (
    "surreal_concept",
    "surreal_anchor",
    "scale_relation",
    "surreal_physics_detail",
)

SURREAL_INTENSITY_SLOTS = {
    "subtle": ("surreal_concept", "surreal_physics_detail"),
    "moderate": ("surreal_concept", "surreal_anchor", "surreal_physics_detail"),
    "bold": SURREAL_LAYER_SLOTS,
}

REFERENCE_EDIT_MODES = ("off", "identity", "younger_self", "brand_board")
TREND_LAYERS = (
    "off",
    "scrapbook_collage",
    "action_figure_packaging",
    "retro_flash",
    "clean_brand_portrait",
)
SELECTION_MODES = ("rule", "semantic", "hybrid")
DEFAULT_SELECTION_MODE = "semantic"
DEFAULT_SEMANTIC_INTENT = (
    "photorealistic image-ready photo prompt with coherent subject, location, "
    "lighting, mood, camera, composition, texture, and format"
)
NOVELTY_LEVELS = ("low", "medium", "high")
FILTER_STRICTNESS_MODES = ("hard", "soft", "off")
SEMANTIC_PROFILES = ("conservative", "balanced", "exploratory")
SEMANTIC_AXIS_MODES = ("auto", "off")
INTENT_STEERING_MODES = ("auto", "off")
LLM_POLISH_MODES = ("off", "strict")
SEMANTIC_PROVIDER = "gemini"
DEFAULT_SEMANTIC_DIMENSIONS = 768
SEMANTIC_MODEL_ID = "gemini-embedding-2"
SEMANTIC_TEXT_RECIPE_VERSION = "semantic-text-v2"
GENERATOR_VERSION = "2026.06.0"
LIKENESS_MODES = ("off", "inspired")
QUALITY_LAYERS_FILENAME = "photo_prompt_quality_layers.json"
RESEARCH_EXTENSION_FILENAME = "photo_prompt_research_extension.json"
RESEARCH_EXTENSION_FILENAMES = (
    RESEARCH_EXTENSION_FILENAME,
    "photo_prompt_subculture_extension.json",
    "photo_prompt_worldbuilding_extension.json",
    "photo_prompt_cjk_worldbuilding_extension.json",
    "photo_prompt_scene_expression_extension.json",
    "photo_prompt_scene_expression_worldbuilding.json",
    "photo_prompt_scene_expression_cjk.json",
    "photo_prompt_character_moe_extension.json",
    "photo_prompt_scene_expression_character_moe.json",
)
RESEARCH_EXTENSION_SCHEMA = "photo-prompt-research-extension/v1"
CHARACTER_MECHANISM_GRAPH_SCHEMA = "photo-character-mechanism-graph/v1"
QUALITY_LAYERS_DATA_KEY = "_quality_layers"
SOFT_ANCHOR_WEIGHT_MULTIPLIER = 24.0
SOFT_ANCHOR_PROMOTED_WEIGHT_MULTIPLIER = 36.0
SOFT_ANCHOR_PRIMARY_WEIGHT_MULTIPLIER = 48.0
SOFT_ANCHOR_CRITICAL_WEIGHT_MULTIPLIER = 64.0
SOFT_ANCHOR_BODY_TERM_THRESHOLD = 0.60
SOFT_ANCHOR_SELECTED_RATE_FLOOR = 0.80
# Slot-level per-source anchor match-rate floors; aligned with the quality
# gate (eval_semantic.py) so the in-engine repair fires whenever the gate
# would fail the run. Override per spec via soft_anchor policy
# "source_rate_floors".
DEFAULT_SOFT_ANCHOR_SOURCE_RATE_FLOORS = {"role": 0.90, "mixin": 0.80}

CANDIDATE_PACK_PRESET_LIMIT = 4
CANDIDATE_PACK_CORE_SLOT_LIMIT = 4
CANDIDATE_PACK_SUPPORT_SLOT_LIMIT = 2
CANDIDATE_PACK_TOTAL_CANDIDATE_LIMIT = 64
CANDIDATE_PACK_CREATIVE_EXPLORATION_FLOOR = 0.75
CANDIDATE_PACK_CREATIVE_EXPLORATION_MIN_DISTANCE = 0.45
CANDIDATE_PACK_CREATIVE_EXPLORATION_LIMIT = 6
CANDIDATE_PACK_CREATIVE_DIRECTION_FLOOR = 0.75
CANDIDATE_PACK_CREATIVE_DIRECTION_MIN_PROPOSALS = 4
CANDIDATE_PACK_HYBRID_CONTRACT_VERSION = "photo-hybrid-augmentation/v1"
CANDIDATE_PACK_ADULT_APPEAL_CONTRACT_VERSION = "photo-adult-appeal/v2"
CANDIDATE_PACK_ADULT_APPEAL_AXES = ("sensual_editorial", "fetish_fashion")
CANDIDATE_PACK_ADULT_APPEAL_EMPHASES = ("sensual_led", "balanced", "fetish_led")
CANDIDATE_PACK_SENSUAL_EDITORIAL_DEFAULT_INTENSITY = 1
CANDIDATE_PACK_FETISH_FASHION_DEFAULT_INTENSITY = 0
CANDIDATE_PACK_ADULT_APPEAL_DEFAULT_EMPHASIS = "sensual_led"
CANDIDATE_PACK_CREATIVE_DIRECTION_OPERATORS = (
    (
        "structural_analogy",
        "Map the topic's relationship or pressure into a spatial, material, or causal structure rather than adding a decorative symbol.",
    ),
    (
        "expectation_inversion",
        "Reverse one familiar expectation while preserving the subject and scene so the reversal has readable consequences.",
    ),
    (
        "absence_as_evidence",
        "Make a missing thing legible through contact marks, behavior, displaced matter, or negative space rather than showing it directly.",
    ),
    (
        "rule_extension",
        "Extend one ordinary rule into an unexpected part of the scene and show at least two physical consequences of that extension.",
    ),
    (
        "temporal_fold",
        "Let before and after coexist through one repeated gesture, material state, reflection, or trace without using a diagram or montage.",
    ),
    (
        "relational_reversal",
        "Let setting, prop, foreground, or background take over one causal role normally assigned to the main subject.",
    ),
    (
        "functional_recontextualization",
        "Give a familiar object one new scene-consistent function whose use changes multiple visible relationships.",
    ),
    (
        "controlled_impossibility",
        "Introduce one impossible photographic law and make light, contact, matter, and behavior obey that law consistently.",
    ),
)
CANDIDATE_PACK_VIEWER_CONTEXTS = (
    "feed_thumbnail",
    "full_screen",
    "poster",
    "product_detail",
)
CANDIDATE_PACK_VIEWER_AUDIENCE_LITERACY = (
    "general",
    "genre_literate",
    "subculture_literate",
    "expert",
)
CANDIDATE_PACK_VIEWER_NEEDS = (
    "insight",
    "care",
    "relatedness",
    "identity",
    "meaning",
    "recovery",
    "aspiration",
    "trust",
)
CANDIDATE_PACK_VIEWER_ATTACHMENT_CHANNELS = (
    "none",
    "agency",
    "reciprocity",
    "continuity",
    "self_relevance",
)
CANDIDATE_PACK_VIEWER_REINSPECTION_MODES = (
    "none",
    "causal_second_reading",
)
CANDIDATE_PACK_VIEWER_COMMERCIAL_OBJECTIVES = (
    "none",
    "stop",
    "comprehend",
    "remember",
    "act",
    "share",
    "return",
)
CANDIDATE_PACK_CORE_SLOTS = {
    "subject",
    "appearance_type",
    "costume_style",
    "anatomical_connection",
    "body_evidence_region",
    "body_pose",
    "species_marker",
    "surface_material",
    "wardrobe_style",
    "footwear",
    "silhouette_proportion",
    "prop",
    "location",
    "space_condition",
    "crowd_density",
    "situation_context",
    "occasion_context",
    "narrative_core",
    "concept_tension",
    "action",
    "mood",
    "lighting",
    "light_type",
    "light_shape",
    "composition",
    "shot_scale",
    "platform_framing",
    "subject_framing",
    "camera_direction",
}
CANDIDATE_PACK_CREATIVE_EXPLORATION_SLOTS = {
    "action",
    "aftermath_trace",
    "ambient_particle",
    "camera_direction",
    "camera_height",
    "camera_type",
    "composition",
    "concept_tension",
    "crowd_density",
    "duty_prop_state",
    "frame_anchor_medium",
    "lens",
    "light_direction",
    "light_intensity",
    "light_shape",
    "light_type",
    "lighting",
    "location",
    "mood",
    "narrative_core",
    "occasion_context",
    "procedure_step",
    "prop",
    "relational_action",
    "sensory_focus",
    "shot_scale",
    "situation_context",
    "space_condition",
    "subject_framing",
    "time_of_day",
    "viewer_position",
    "weather",
}
CANDIDATE_PACK_INTENT_STOPWORDS = {
    "달린",
    "있는",
    "같은",
    "느낌",
    "스타일",
    "컨셉",
    "그리고",
    "및",
    "와",
    "과",
    "의",
    "한",
    "a",
    "an",
    "the",
    "and",
    "with",
    "of",
    "in",
}
CANDIDATE_PACK_SEMANTIC_DROPOUT_BUCKETS: Dict[str, tuple[str, ...]] = {
    "environment": (
        "location",
        "space_condition",
        "crowd_density",
        "occasion_context",
        "weather",
        "time_of_day",
        "lighting",
        "light_type",
        "light_shape",
        "light_direction",
        "light_intensity",
    ),
    "action_prop": (
        "action",
        "prop",
        "situation_context",
        "capture_context",
        "relational_action",
        "prop_direction",
        "body_pose",
    ),
    "camera_composition": (
        "composition",
        "shot_scale",
        "platform_framing",
        "subject_framing",
        "camera_direction",
        "camera_type",
        "lens",
        "focus",
        "motion",
        "body_framing",
    ),
    "style_finish": (
        "mood",
        "color",
        "texture",
        "film_emulation",
        "format",
        "quality",
        "aesthetic_trend",
        "narrative_core",
        "concept_tension",
        "wardrobe_style",
        "footwear",
        "silhouette_proportion",
        "garment_detail",
    ),
}
CANDIDATE_PACK_DROPOUT_PROTECTED_SLOTS = {
    "subject",
    "person_origin",
    "appearance_type",
    "costume_style",
    "wardrobe_style",
    "footwear",
    "silhouette_proportion",
    "anatomical_connection",
    "species_marker",
    "body_evidence_region",
    "surface_material",
}
CANDIDATE_PACK_MOTIF_TAXONOMY: Dict[str, tuple[str, ...]] = {
    "phone_selfie_mirror": (
        "clear_case_smartphone",
        "phone",
        "selfie",
        "mirror selfie",
        "mirror_selfie",
        "over_shoulder_phone_screen",
        "phone_arm_length_selfie",
        "checking_phone",
        "bedroom_mirror",
        "repeated-message phone",
    ),
    "red_thread": (
        "red thread",
        "red string",
        "red-string",
        "red ribbon",
        "붉은 실",
    ),
    "photo_wall": (
        "instant_photo_stack",
        "obsession_photo_wall_prop",
        "photo wall",
        "same-person photos",
        "repeated photos",
        "photo shrine",
        "scrapbook_photo_cutout_layout",
    ),
    "surveillance_evidence": (
        "surveillance evidence",
        "cctv",
        "cctv_corner_frame",
        "cctv_monitor_stack_prop",
        "contact sheet",
        "case-file",
        "one-way mirror",
    ),
    "sealed_keepsake": (
        "sealed_mission_envelope_prop",
        "sealed decree",
        "sealed letter",
        "sealed keepsake",
        "portrait keepsake",
        "wilted flower",
    ),
    "digital_fixation": (
        "clear_case_smartphone",
        "unread message",
        "notification",
        "phone-screen evidence",
        "repeated-message phone",
        "digital fixation",
    ),
    "threshold_watch": (
        "doorframe_shadow_watch",
        "doorway",
        "threshold",
        "frame_within_frame",
        "watching from the doorway",
    ),
    "record_board": (
        "logo_board_prop",
        "clinical_chart_clipboard_prop",
        "care_record_board_prop",
        "appointment_ledger_prop",
        "chart_records_board_prop",
        "records board",
        "care record",
        "appointment ledger",
        "route board",
    ),
}

SEMANTIC_PROFILE_CONFIGS: Dict[str, Dict[str, float]] = {
    "conservative": {
        "preset_window": 0.06,
        "preset_candidate_limit": 5,
        "preset_weight_floor": 0.86,
        "preset_overall_weight": 0.35,
        "preset_axis_mean_weight": 0.35,
        "preset_axis_floor_weight": 0.30,
        "axis_coverage_target": 0.70,
        "axis_coverage_weight": 0.14,
        "must_cover_weight": 0.30,
        "cliche_penalty_weight": 0.18,
        "routed_axis_floor": 0.16,
        "routed_axis_floor_penalty": 0.58,
        "coherence_conflict_penalty": 0.38,
        "coherence_strong_boost": 1.22,
        "coherence_ambient_boost": 1.06,
        "cross_slot_affinity_weight": 0.12,
        "contextual_redundancy_relief": 0.18,
        "weak_horror_compensation_boost": 1.34,
        "preset_family_strong_bonus": 0.045,
        "preset_family_ambient_bonus": 0.015,
        "preset_family_missing_penalty": 0.085,
        "slot_window": 0.08,
        "slot_candidate_limit": 5,
        "slot_weight_floor": 0.86,
        "filter_bonus": 0.12,
        "filter_penalty": 0.55,
        "temperature_multiplier": 1.2,
    },
    "balanced": {
        "preset_window": 0.14,
        "preset_candidate_limit": 8,
        "preset_weight_floor": 0.82,
        "preset_overall_weight": 0.45,
        "preset_axis_mean_weight": 0.35,
        "preset_axis_floor_weight": 0.20,
        "axis_coverage_target": 0.68,
        "axis_coverage_weight": 0.22,
        "must_cover_weight": 0.42,
        "cliche_penalty_weight": 0.24,
        "routed_axis_floor": 0.10,
        "routed_axis_floor_penalty": 0.68,
        "coherence_conflict_penalty": 0.45,
        "coherence_strong_boost": 1.18,
        "coherence_ambient_boost": 1.05,
        "cross_slot_affinity_weight": 0.16,
        "contextual_redundancy_relief": 0.24,
        "weak_horror_compensation_boost": 1.42,
        "preset_family_strong_bonus": 0.035,
        "preset_family_ambient_bonus": 0.012,
        "preset_family_missing_penalty": 0.065,
        "slot_window": 0.14,
        "slot_candidate_limit": 8,
        "slot_weight_floor": 0.82,
        "filter_bonus": 0.18,
        "filter_penalty": 0.35,
        "temperature_multiplier": 1.0,
    },
    "exploratory": {
        "preset_window": 0.24,
        "preset_candidate_limit": 14,
        "preset_weight_floor": 0.72,
        "preset_overall_weight": 0.55,
        "preset_axis_mean_weight": 0.30,
        "preset_axis_floor_weight": 0.15,
        "axis_coverage_target": 0.64,
        "axis_coverage_weight": 0.28,
        "must_cover_weight": 0.50,
        "cliche_penalty_weight": 0.18,
        "routed_axis_floor": 0.02,
        "routed_axis_floor_penalty": 0.78,
        "coherence_conflict_penalty": 0.62,
        "coherence_strong_boost": 1.12,
        "coherence_ambient_boost": 1.03,
        "cross_slot_affinity_weight": 0.20,
        "contextual_redundancy_relief": 0.30,
        "weak_horror_compensation_boost": 1.50,
        "preset_family_strong_bonus": 0.025,
        "preset_family_ambient_bonus": 0.008,
        "preset_family_missing_penalty": 0.035,
        "slot_window": 0.24,
        "slot_candidate_limit": 14,
        "slot_weight_floor": 0.72,
        "filter_bonus": 0.08,
        "filter_penalty": 0.12,
        "temperature_multiplier": 0.82,
    },
}

BATCH_DIVERSITY_TRACKED_SCOPES = (
    "preset",
    "subject",
    "subject_group",
    "location",
    "location_tone",
    "lighting",
    "light_type",
    "light_shape",
    "genre",
    "action",
    "prop",
    "style",
    "color",
    "texture",
    "species_marker",
    "anatomical_connection",
    "lens",
    "film_emulation",
    "weather",
    "camera_type",
    "mood",
    "surreal_concept",
)
BATCH_DIVERSITY_CONFIGS: Dict[str, Dict[str, Any]] = {
    "low": {
        "exact_decay": 0.84,
        "similarity_weight": 0.12,
        "similarity_threshold": 0.90,
        "min_penalty": 0.58,
        "scope_weights": {
            "preset": 0.75,
            "location": 0.85,
            "location_tone": 0.35,
            "lighting": 0.28,
            "mood": 0.45,
            "prop": 0.5,
            "subject": 0.35,
            "subject_group": 0.55,
            "surreal_concept": 0.35,
        },
    },
    "medium": {
        "exact_decay": 0.66,
        "similarity_weight": 0.26,
        "similarity_threshold": 0.88,
        "min_penalty": 0.38,
        "scope_weights": {
            "preset": 1.0,
            "location": 1.0,
            "location_tone": 0.55,
            "lighting": 0.55,
            "mood": 0.65,
            "prop": 0.9,
            "subject": 0.45,
            "subject_group": 0.85,
            "surreal_concept": 0.55,
        },
    },
    "high": {
        "exact_decay": 0.48,
        "similarity_weight": 0.42,
        "similarity_threshold": 0.84,
        "min_penalty": 0.24,
        "scope_weights": {
            "preset": 1.2,
            "location": 1.2,
            "location_tone": 0.85,
            "lighting": 0.85,
            "mood": 1.0,
            "prop": 1.1,
            "subject": 0.62,
            "subject_group": 1.15,
            "surreal_concept": 0.82,
        },
    },
}

CROSS_SLOT_AFFINITY_CONTEXT_SLOTS: Dict[str, tuple[str, ...]] = {
    "lighting": ("location", "space_condition", "situation_context", "time_of_day", "weather", "mood"),
    "light_type": ("location", "space_condition", "situation_context", "time_of_day", "weather", "mood", "lighting"),
    "light_shape": ("location", "space_condition", "situation_context", "time_of_day", "weather", "mood", "lighting"),
    "color": ("location", "space_condition", "occasion_context", "time_of_day", "weather", "mood", "lighting"),
    "texture": ("location", "space_condition", "weather", "mood", "lighting", "color"),
    "hair_color": ("subject", "appearance_type", "hair_style", "costume_style", "aesthetic_trend"),
    "wardrobe_style": ("subject", "location", "aesthetic_trend", "footwear", "silhouette_proportion"),
    "footwear": ("subject", "location", "aesthetic_trend", "wardrobe_style", "weather"),
    "silhouette_proportion": ("subject", "location", "aesthetic_trend", "wardrobe_style"),
    "makeup_style": ("subject", "location", "aesthetic_trend", "wardrobe_style"),
    "space_condition": ("location", "weather", "texture", "time_of_day"),
    "crowd_density": ("location", "situation_context", "occasion_context"),
    "situation_context": ("location", "action", "time_of_day", "crowd_density"),
    "occasion_context": ("location", "prop", "mood", "situation_context"),
    "narrative_core": ("mood", "situation_context", "occasion_context", "location", "prop", "capture_context", "aesthetic_trend"),
    "concept_tension": ("narrative_core", "mood", "location", "surface_material", "texture", "lighting", "world", "composition"),
    "body_pose": ("subject", "action", "hand_pose", "body_orientation", "shot_scale", "composition"),
    "shot_scale": ("composition", "subject_framing", "body_pose", "camera_direction", "lens"),
    "platform_framing": ("format", "composition", "capture_context", "shot_scale", "camera_direction"),
    "hand_pose": ("subject", "action", "body_pose", "gaze_engagement", "wardrobe_style"),
    "gaze_engagement": ("subject", "expression", "body_orientation", "camera_direction", "composition"),
    "capture_context": ("action", "prop", "location", "situation_context", "camera_direction", "composition"),
    "surreal_anchor": ("surreal_concept", "location", "space_condition"),
}

SEMANTIC_INTENT_SLOT_HINTS: Dict[str, List[JsonDict]] = {
    "narrative_core": [
        {
            "id": "intent_analog_diary_narrative_core",
            "any": ["analog diary", "family archive", "memory archive", "bedroom shrine", "found photograph"],
            "ids": ["analog_diary_memory_core", "private_ritual_core", "fragile_intimacy_core"],
        },
        {
            "id": "intent_quiet_rebellion_narrative_core",
            "any": ["quiet rebellion", "soft protest", "quiet defiance"],
            "ids": ["quiet_rebellion_core", "urban_solitude_core", "public_private_self_core"],
        },
        {
            "id": "intent_digital_privacy_narrative_core",
            "any": ["digital privacy", "privacy anxiety", "public persona", "private self", "phone glow"],
            "ids": ["digital_privacy_core", "public_private_self_core", "ai_companion_core"],
        },
        {
            "id": "intent_romantic_decay_narrative_core",
            "any": ["romantic decay", "broken luxury", "faded glamour"],
            "ids": ["romantic_decay_core", "broken_luxury_core", "fragile_intimacy_core"],
        },
        {
            "id": "intent_near_future_ai_narrative_core",
            "any": ["near-future nostalgia", "near future nostalgia", "ai companion"],
            "ids": ["near_future_nostalgia_core", "ai_companion_core", "ordinary_magic_core"],
        },
    ],
    "concept_tension": [
        {
            "id": "intent_organic_synthetic_tension",
            "any": ["organic vs synthetic", "organic versus synthetic", "natural vs artificial"],
            "ids": ["organic_vs_synthetic_tension", "urban_vs_wilderness_tension", "human_touch_vs_automation_tension"],
        },
        {
            "id": "intent_analog_ai_tension",
            "any": ["analog vs ai", "analog versus ai", "analog vs AI"],
            "ids": ["analog_vs_ai_tension", "nostalgic_vs_futuristic_tension"],
        },
        {
            "id": "intent_luxury_decay_tension",
            "any": ["luxury vs decay", "luxury versus decay", "broken luxury"],
            "ids": ["luxury_vs_decay_tension", "polished_vs_imperfect_tension"],
        },
        {
            "id": "intent_public_private_tension",
            "any": ["public vs private", "public versus private", "public persona", "private self"],
            "ids": ["public_vs_private_tension", "visibility_vs_secrecy_tension"],
        },
    ],
    "location": [
        {
            "id": "intent_archive_bedroom_location",
            "any": ["bedroom shrine", "family archive", "attic archive"],
            "ids": ["bedroom_shrine", "attic_archive_room", "lived_in_studio_room"],
        },
        {
            "id": "intent_broken_luxury_location",
            "any": ["broken luxury", "romantic decay", "hotel lobby"],
            "ids": ["old_hotel_lobby_decay", "luxury_hotel_lobby", "luxury_hotel_corridor"],
        },
        {
            "id": "intent_organic_synthetic_location",
            "any": ["organic vs synthetic", "rooftop garden", "rooftop greenhouse"],
            "ids": ["rooftop_greenhouse", "botanical_greenhouse", "secret_garden_path", "indoor_forest_room"],
        },
    ],
    "prop": [
        {
            "id": "intent_analog_diary_props",
            "any": ["analog diary", "family archive", "memory archive", "bedroom shrine", "found photograph"],
            "ids": ["unreadable_diary_prop", "old_postcard_unreadable_prop", "polaroid_stack_unreadable_prop", "fountain_pen_prop", "film_roll_contact_sheet_prop"],
        },
        {
            "id": "intent_privacy_screen_props",
            "any": ["digital privacy", "phone glow", "no readable text", "blurred screen"],
            "ids": ["smartphone_in_hand", "blurred_laptop_screen_glow_prop", "crt_tv_abstract_glow_prop"],
        },
    ],
    "capture_context": [
        {
            "id": "intent_analog_diary_capture_context",
            "any": ["analog diary", "family archive", "memory archive", "bedroom shrine"],
            "ids": ["analog_diary_snapshot_context", "contact_sheet_archive_context", "no_text_paper_ephemera_context"],
        },
        {
            "id": "intent_privacy_screen_capture_context",
            "any": ["digital privacy", "phone glow", "blurred screen", "no readable text"],
            "ids": ["privacy_screen_glow_context", "blurred_screen_over_shoulder_context"],
        },
    ],
    "body_pose": [
        {
            "id": "intent_contrapposto_pose",
            "any": ["contrapposto"],
            "ids": ["contrapposto_full_body", "editorial_s_curve_pose", "power_stance_feet_apart"],
        },
        {
            "id": "intent_walking_lookback_pose",
            "any": ["walking away", "looking back hook", "look back hook", "turning back"],
            "ids": ["walking_mid_stride_pose", "turning_back_over_shoulder_pose", "stepping_into_frame_pose"],
        },
    ],
    "shot_scale": [
        {
            "id": "intent_full_body_shot_scale",
            "any": ["full body", "full length", "full-length"],
            "ids": ["full_length_body_shot", "medium_long_knee_up_shot"],
        },
        {
            "id": "intent_closeup_shot_scale",
            "any": ["close up", "close-up", "beauty close", "face close"],
            "ids": ["close_up_face_shot", "medium_close_chest_up_shot", "extreme_close_detail_shot"],
        },
        {
            "id": "intent_wide_environment_shot_scale",
            "any": ["wide environmental", "tiny subject", "extreme wide", "architecture leading"],
            "ids": ["extreme_wide_environment_scale", "wide_full_scene_shot"],
        },
    ],
    "platform_framing": [
        {
            "id": "intent_tiktok_safe_frame",
            "any": ["tiktok safe", "reels safe", "shorts thumbnail"],
            "ids": [
                "vertical_9x16_ui_safe_frame",
                "reels_ui_safe_negative_space",
                "shorts_thumbnail_safe_face_placement",
            ],
        },
        {
            "id": "intent_vertical_safe_frame",
            "any": ["vertical safe frame", "9:16 safe", "tiktok safe", "reels safe", "safe frame"],
            "ids": [
                "vertical_9x16_ui_safe_frame",
                "vertical_4x5_feed_safe_frame",
                "center_safe_subject_frame",
                "reels_ui_safe_negative_space",
                "shorts_thumbnail_safe_face_placement",
            ],
        }
    ],
    "camera_direction": [
        {
            "id": "intent_low_angle_camera",
            "any": ["low angle"],
            "not_any": ["no low angle", "not low angle", "without low angle"],
            "ids": ["low_ground_angle", "extreme_low_hero_angle"],
        },
        {
            "id": "intent_top_down_camera",
            "any": ["top down", "top-down", "flatlay"],
            "ids": ["strict_top_down_flat_view", "top_down_90", "birds_eye"],
        },
        {
            "id": "intent_mirror_reflection_camera",
            "any": ["mirror selfie", "mirror reflection", "via reflection"],
            "ids": ["mirror_reflection_camera_view", "mirror_view_direction", "reflected_in_mirror_direction"],
        },
    ],
    "composition": [
        {
            "id": "intent_leading_lines_composition",
            "any": ["leading lines", "architecture leading"],
            "ids": ["strong_leading_lines_vanish", "leading_lines_depth", "architectural_lines_frame", "centered_architecture_symmetry"],
        },
        {
            "id": "intent_top_down_composition",
            "any": ["top down", "top-down", "flatlay"],
            "ids": ["top_down", "curated_flatlay_grid", "asymmetrical_flatlay_layering"],
        },
    ],
    "hand_pose": [
        {
            "id": "intent_hand_near_lips",
            "any": ["hand near lips", "hand near mouth", "hand touching face"],
            "ids": ["hand_near_lips", "hand_touching_face"],
        }
    ],
    "gaze_engagement": [
        {
            "id": "intent_eyes_closed",
            "any": ["eyes closed"],
            "ids": ["eyes_closed_serene"],
        },
        {
            "id": "intent_reflection_direct_gaze",
            "any": ["direct eye contact via reflection", "reflection direct", "mirror reflection gaze"],
            "ids": ["reflection_direct_gaze", "mirror_reflection_gaze"],
        },
        {
            "id": "intent_direct_gaze",
            "any": ["direct gaze", "looking camera", "looking at camera"],
            "ids": ["direct_camera_aware", "looking_just_past_lens"],
        },
        {
            "id": "intent_lookback_gaze",
            "any": ["walking away looking back", "looking back hook", "look back hook"],
            "ids": ["looking_back_over_shoulder_gaze", "looking_away_off_frame"],
        },
    ],
    "body_orientation": [
        {
            "id": "intent_back_reflection_orientation",
            "any": ["back view", "looking back", "over shoulder"],
            "ids": ["looking_back_over_shoulder_orientation", "back_view_orientation"],
        }
    ],
    "subject_framing": [
        {
            "id": "intent_closeup_subject_framing",
            "any": ["close up", "close-up", "eyes closed"],
            "ids": ["close_up_face_crop", "head_and_shoulders_crop"],
        }
    ],
    "genre": [
        {
            "id": "intent_food_table_genre",
            "any": ["food table", "top down food", "top-down food"],
            "ids": ["food", "still_life"],
        },
        {
            "id": "intent_architecture_portrait_genre",
            "any": ["architecture leading", "wide environmental portrait", "environmental portrait"],
            "ids": ["portrait", "architecture", "documentary"],
        },
    ],
    "location": [
        {
            "id": "intent_architecture_leading_location",
            "any": ["architecture leading", "centered symmetry"],
            "ids": ["brutalist_plaza", "gallery_white_cube", "art_gallery_white_hall", "museum_gallery", "modernist_facade"],
        }
    ],
}

SLOT_TEMPERATURE_MULTIPLIERS: Dict[str, float] = {
    "mood": 1.28,
    "action": 1.18,
    "genre": 1.12,
    "style": 1.18,
    "color": 1.26,
    "lens": 1.16,
    "lighting": 1.16,
    "light_type": 1.18,
    "film_emulation": 1.22,
    "weather": 1.16,
    "space_condition": 1.18,
    "crowd_density": 1.14,
    "situation_context": 1.2,
    "occasion_context": 1.16,
    "narrative_core": 1.2,
    "concept_tension": 1.16,
    "body_pose": 1.2,
    "shot_scale": 1.16,
    "platform_framing": 1.14,
    "hand_pose": 1.12,
    "gaze_engagement": 1.1,
    "hair_color": 1.12,
    "footwear": 1.16,
    "silhouette_proportion": 1.14,
    "capture_context": 1.18,
    "surreal_concept": 1.34,
    "surreal_anchor": 1.28,
    "texture": 1.24,
    "light_shape": 1.22,
}

COHERENT_DIVERSITY_SLOTS = {
    "genre",
    "action",
    "prop",
    "style",
    "color",
    "texture",
    "lens",
    "lighting",
    "light_type",
    "light_shape",
    "film_emulation",
    "weather",
    "space_condition",
    "crowd_density",
    "situation_context",
    "occasion_context",
    "narrative_core",
    "concept_tension",
    "camera_type",
    "composition",
    "body_pose",
    "shot_scale",
    "platform_framing",
    "hand_pose",
    "gaze_engagement",
    "capture_context",
    "footwear",
    "silhouette_proportion",
    "motion",
    "focus",
    "hair_color",
}

SEMANTIC_SLOT_CAPTION_TEMPLATES: Dict[str, str] = {
    "subject": "Photo subject concept: {description}. It should retrieve visual subjects by identity, role, species, object type, and scene relevance.",
    "location": "Photographic location concept: {description}. It should retrieve places by setting, environment, city or nature context, interior or exterior space, and atmosphere.",
    "lighting": "Photographic lighting concept: {description}. It should retrieve light by source, mood, shadow behavior, color temperature, and photographic realism.",
    "light_type": "Specific light-source concept: {description}. It should retrieve lamps, neon, flash, sun, screens, strobes, and practical light sources.",
    "light_shape": "Light-shape concept: {description}. It should retrieve visible beam shapes, shadow patterns, edge light, caustics, diffusion, and photographic light geometry.",
    "hair_color": "Hair-color concept: {description}. It should retrieve natural hair color, cosplay wig color, character hair color, and photographic hair-color cues.",
    "footwear": "Footwear concept: {description}. It should retrieve shoes, sandals, boots, heels, sneakers, loafers, and how they fit fashion dailywear context.",
    "silhouette_proportion": "Fashion silhouette and proportion concept: {description}. It should retrieve waistline, shoulder shape, layering, volume, body-con, oversized, and garment proportion cues.",
    "capture_context": "Capture-context concept: {description}. It should retrieve social-photo capture grammar, selfie viewpoint, POV interaction, screen overlay tricks, mirror capture, and passenger-seat observation.",
    "mood": "Image mood concept: {description}. It should retrieve emotional tone, genre feeling, tension, romance, nostalgia, horror, calm, or surreal atmosphere.",
    "film_emulation": "Film and camera-emulation concept: {description}. It should retrieve analog film stocks, halation, grain, color cast, instant film, disposable camera, or CCD looks.",
    "weather": "Weather and atmosphere concept: {description}. It should retrieve rain, fog, snow, humidity, frost, sea spray, heat haze, and environmental air effects.",
    "space_condition": "Space and environment condition concept: {description}. It should retrieve cleanliness, clutter, construction, decay, flooding, renovation, power outage, and lived-in state of a photographed place.",
    "crowd_density": "Crowd density and social arrangement concept: {description}. It should retrieve empty, sparse, solo, small-group, queue, packed commute, festival crowd, bystander-ring, and stage-facing crowd layouts.",
    "situation_context": "Everyday situation and routine concept: {description}. It should retrieve commute, errands, cafe work, room reset, laundry day, moving day, small-business packing, behind-the-scenes, and social routine grammar without readable text.",
    "occasion_context": "Occasion and event context concept: {description}. It should retrieve graduation, birthday, opening day, closing cleanup, holiday gathering, festival, exhibition opening, workshop, volunteer, and community event atmosphere using non-readable set dressing.",
    "narrative_core": "Narrative-core concept: {description}. It should retrieve poetic story anchors such as quiet rebellion, analog diary memory, urban solitude, ordinary magic, digital privacy, AI companion, romantic decay, broken luxury, and community ritual without relying on readable text.",
    "concept_tension": "Concept-tension concept: {description}. It should retrieve visual contrast pairs such as organic versus synthetic, analog versus AI, luxury versus decay, public versus private, documentary versus staged, and realistic versus dreamlike through material, light, setting, and composition.",
    "body_pose": "Clean human body-pose concept: {description}. It should retrieve standing, seated, leaning, crouching, walking, turning, group layering, and editorial posture without adult body-first framing.",
    "shot_scale": "Photographic shot-scale concept: {description}. It should retrieve extreme wide, wide, full-length, medium-long, medium, medium close-up, close-up, and extreme close-up framing.",
    "platform_framing": "Platform-safe framing concept: {description}. It should retrieve vertical social crops, UI-safe blank space, thumbnail-safe face placement, feed-safe composition, and no readable text or hashtags.",
    "surreal_concept": "Photoreal surreal event concept: {description}. It should retrieve impossible events that still look like real photographed scenes.",
    "surreal_anchor": "Physical anchor for a photoreal surreal scene: {description}. It should retrieve the real object or surface where the impossible event is grounded.",
}

DEFAULT_FACET_VOCAB: JsonDict = {
    "subject_kind": ["human", "animal", "object", "food", "environment", "plant", "sign"],
    "place_type": ["urban", "street", "interior", "nature", "studio", "commercial", "transport", "home", "collection_storage", "sports_venue"],
    "time_of_day": ["day", "night", "dawn", "dusk", "indoor_unspecified"],
    "weather": ["clear", "rain", "snow", "fog", "storm", "heat", "haze", "dust", "wind", "flood", "underwater", "hail", "frost", "none"],
    "lighting_family": ["natural_light", "artificial_light", "colored_light", "flash", "studio_light", "low_light"],
    "mood_family": ["calm", "tense", "romantic", "surreal", "nostalgic", "commercial", "documentary"],
    "camera_register": ["phone", "professional", "surveillance", "vintage", "studio", "macro"],
    "safety_tier": ["general", "adult_compatible", "adult_only"],
    "soft_body_role": ["body_emphasis", "narrative_safe"],
    "shot_scale": ["extreme_wide", "wide", "full_length", "medium_long", "medium", "medium_close", "close_up", "extreme_close"],
    "camera_angle": ["eye_level", "low", "high", "overhead_top_down", "dutch", "over_shoulder", "pov", "reflection", "hidden_observer"],
    "placement": ["centered", "rule_of_thirds", "negative_space", "frame_filling", "edge_tension", "entering_frame", "exiting_frame", "layered_depth", "foreground_frame", "symmetry"],
    "platform_frame": ["vertical_9_16_safe", "vertical_4_5_safe", "square_1_1_safe", "ui_safe_negative_space", "thumbnail_safe", "face_upper_middle", "center_safe", "blank_lower_third", "carousel_crop_safe"],
    "relation_type": ["cooperative", "caregiving", "instructional", "transactional", "handoff", "team", "crowd", "competitive"],
    "event_phase": ["preparation", "active_process", "pause", "handoff", "aftermath", "maintenance", "recovery", "dormancy", "reactivation"],
    "process_stage": ["setup", "calibration", "sampling", "measurement", "inspection", "transfer", "intervention", "monitoring", "cleanup"],
    "capture_modality": ["visible_light", "macro", "microscopy", "thermal", "ultraviolet", "aerial", "underwater", "surveillance", "machine_vision", "inspection", "fluorescence", "dic", "polarized_light", "light_sheet", "photogrammetry"],
    "weather_effect": ["visibility_loss", "surface_wetness", "airborne_particles", "wind_deformation", "heat_distortion", "frost_accumulation", "flooding", "hail_impact", "erosion_deposition", "none"],
    "movement_type": ["static", "fine_motor", "locomotion", "impact", "rotation", "fluid_flow", "crowd_flow", "mechanical_cycle", "vehicle_flow"],
    "acquisition_structure": ["fixed_roi", "time_series", "multichannel", "z_stack", "multiview"],
    "record_basis": ["human_observation", "machine_observation", "material_sample"],
    "movement_phase": ["readiness", "initiation", "loading_braking", "propulsion_release", "flight_transfer", "impact_absorption", "deceleration_stabilization", "recovery"],
    "contact_state": ["clearance_no_contact", "surface_or_medium_contact", "equipment_contact", "opponent_contact", "flight_or_separation", "post_contact_release"],
    "effort_state": ["controlled", "near_maximal", "fatigued", "recovering"],
    "material_response": ["compression", "elastic_bend", "rebound", "vibration", "surface_shear", "particle_or_fluid_displacement"],
    "learning_stage": ["orientation", "demonstration", "guided_practice", "collaborative_problem_solving", "performance_assessment"],
    "material_lifecycle_stage": ["manufacture", "use", "wear", "failure", "diagnosis", "maintenance", "repair", "reuse", "refurbishment", "remanufacture", "recovery", "disposal"],
    "material_state_evidence": ["reference_condition", "service_wear", "localized_failure", "diagnostic_contact", "cleaning_boundary", "removed_failed_part", "repaired_interface", "reassembled_state", "functional_test", "separated_fraction", "residual_route", "next_use_handoff"],
    "atmospheric_class": ["hydrometeor", "lithometeor", "photometeor"],
    "phenomenon_process": ["suspended_particles", "falling_particles", "wind_raised_particles", "deposited_particles", "optical_interaction"],
    "observation_interval": ["repeat_interval", "seasonal_cycle"],
}

VALID_SUBJECT_CATEGORIES = {"human", "animal", "food", "object", "sign", "plant", "environment", "generic"}
VALID_PRESET_DOMAINS = {
    "portrait",
    "fashion",
    "beauty",
    "social",
    "product",
    "jewelry",
    "food",
    "wildlife",
    "documentary",
    "craft",
    "street",
    "urban",
    "architecture",
    "science_inspection",
    "mobility_logistics",
    "climate_adaptation",
    "biodiversity_monitoring",
    "agriculture_food_systems",
    "circular_materials",
    "heritage_documentation",
    "health_access",
    "sports_motion",
    "education_training",
    "disaster_risk_operations",
    "human_interaction",
    "natural_process",
    "longitudinal_place_state",
    "visual_structure",
    "subculture_practice",
    "worldbuilding_system",
    "cjk_narrative_world",
    "character_moe_grammar",
    "surreal",
    "adult",
}

DEFAULT_SLOT_APPLICABILITY: JsonDict = {
    "subject_category_overrides": {},
    "preset_domain_overrides": {},
    "slots": {
        "person_origin": {
            "subject_categories": ["human"],
            "deny_domains": ["product", "jewelry", "food", "wildlife"],
        },
        "appearance_type": {
            "subject_categories": ["human"],
            "deny_domains": ["documentary", "craft", "wildlife", "product", "jewelry", "food"],
        },
        "hair_style": {
            "subject_categories": ["human"],
            "deny_domains": ["product", "jewelry", "food", "wildlife"],
        },
        "hair_color": {
            "subject_categories": ["human"],
            "deny_domains": ["product", "jewelry", "food", "wildlife"],
        },
        "makeup_style": {
            "subject_categories": ["human"],
            "deny_domains": ["documentary", "craft", "wildlife", "product", "jewelry", "food"],
        },
        "facial_hair": {
            "subject_categories": ["human"],
            "deny_domains": ["product", "jewelry", "food", "wildlife"],
        },
        "wardrobe_style": {
            "subject_categories": ["human"],
            "deny_domains": ["documentary", "craft", "wildlife", "product", "jewelry", "food"],
        },
        "footwear": {
            "subject_categories": ["human"],
            "deny_domains": ["documentary", "craft", "wildlife", "product", "jewelry", "food"],
        },
        "silhouette_proportion": {
            "subject_categories": ["human"],
            "deny_domains": ["documentary", "craft", "wildlife", "product", "jewelry", "food"],
        },
        "costume_style": {
            "subject_categories": ["human"],
            "deny_domains": ["documentary", "craft", "wildlife", "product", "jewelry", "food"],
        },
        "body_framing": {
            "subject_categories": ["human"],
            "deny_domains": ["product", "jewelry", "food", "wildlife"],
        },
        "body_pose": {
            "subject_categories": ["human"],
            "deny_domains": ["product", "jewelry", "food", "wildlife"],
        },
        "hand_pose": {
            "subject_categories": ["human"],
            "deny_domains": ["product", "jewelry", "food", "wildlife"],
        },
        "body_orientation": {
            "subject_categories": ["human"],
            "deny_domains": ["product", "jewelry", "food", "wildlife"],
        },
        "gaze_engagement": {
            "subject_categories": ["human"],
            "deny_domains": ["product", "jewelry", "food"],
        },
        "gaze_target": {
            "subject_categories": ["human", "animal"],
            "deny_domains": ["product", "jewelry", "food"],
        },
        "shot_scale": {
            "deny_domains": [],
        },
        "platform_framing": {
            "deny_domains": ["wildlife", "food"],
        },
        "fetish_styling": {
            "subject_categories": ["human"],
            "allow_domains": ["adult"],
            "deny_domains": ["documentary", "craft", "wildlife", "product", "jewelry", "food"],
            "require_domain_match": True,
        },
        "adult_context": {
            "subject_categories": ["human"],
            "allow_domains": ["adult"],
            "deny_domains": ["documentary", "craft", "wildlife", "product", "jewelry", "food"],
            "require_domain_match": True,
        },
        "capture_context": {
            "subject_categories": ["human", "animal", "food", "object", "plant", "environment"],
            "allow_domains": ["portrait", "fashion", "beauty", "social", "adult", "science_inspection", "mobility_logistics", "climate_adaptation", "biodiversity_monitoring", "agriculture_food_systems", "circular_materials", "heritage_documentation", "health_access", "sports_motion", "education_training", "disaster_risk_operations", "natural_process", "longitudinal_place_state"],
            "deny_domains": ["documentary", "craft", "wildlife", "product", "jewelry", "food", "architecture"],
            "require_domain_match": True,
        },
        "expression": {
            "subject_categories": ["human", "animal"],
        },
        "aesthetic_trend": {
            "deny_domains": ["documentary", "craft", "wildlife"],
        },
        "surface_material": {
            "subject_categories": ["object", "food", "plant", "environment", "sign"],
            "allow_domains": ["product", "jewelry", "food", "architecture"],
        },
        "space_condition": {
            "deny_domains": ["product", "jewelry", "food", "wildlife", "adult"],
        },
        "crowd_density": {
            "deny_domains": ["product", "jewelry", "food", "wildlife", "adult"],
        },
        "situation_context": {
            "deny_domains": ["product", "jewelry", "food", "wildlife", "adult"],
        },
        "occasion_context": {
            "deny_domains": ["product", "jewelry", "food", "wildlife", "adult"],
        },
        "narrative_core": {
            "deny_domains": ["food", "wildlife", "adult"],
        },
        "concept_tension": {
            "deny_domains": ["food", "wildlife", "adult"],
        },
    },
}


# -----------------------------------------------------------------------------
# Basic helpers
# -----------------------------------------------------------------------------

def merge_research_extension(data: JsonDict, extension: JsonDict) -> JsonDict:
    """Merge the optional research taxonomy pack without rewriting the base dictionary.

    The extension is intentionally append-only for ID-bearing collections and
    additive for facet vocabularies.  Duplicate IDs fail at load time so a
    research batch cannot silently shadow established behavior.
    """
    if extension.get("schema_version") != RESEARCH_EXTENSION_SCHEMA:
        raise ValueError(
            f"Unsupported research extension schema: {extension.get('schema_version')!r}"
        )

    def append_unique_id_entries(target: list[Any], additions: Any, label: str) -> None:
        incoming = additions if isinstance(additions, list) else []
        existing_ids = {
            str(item.get("id"))
            for item in target
            if isinstance(item, dict) and str(item.get("id") or "")
        }
        for item in incoming:
            if not isinstance(item, dict) or not str(item.get("id") or ""):
                raise ValueError(f"{label}: extension entries require a non-empty id")
            item_id = str(item["id"])
            if item_id in existing_ids:
                raise ValueError(f"{label}: duplicate extension id {item_id}")
            target.append(item)
            existing_ids.add(item_id)

    facet_vocab = data.setdefault("facet_vocab", {})
    for facet_key, values in (extension.get("facet_vocab") or {}).items():
        target_values = facet_vocab.setdefault(str(facet_key), [])
        for value in normalize_list(values):
            if value not in target_values:
                target_values.append(value)

    append_unique_id_entries(data.setdefault("preset_families", []), extension.get("preset_families"), "preset_families")
    preset_filter_defaults = extension.get("preset_filter_defaults") or {}
    auto_optional_policy = extension.get("auto_optional_policy")
    if auto_optional_policy not in {None, "authored_filters_only"}:
        raise ValueError(
            f"Unsupported research extension auto_optional_policy: {auto_optional_policy!r}"
        )
    def render_contract_template_value(value: Any, preset: JsonDict) -> Any:
        replacements = {
            "{preset_id}": str(preset.get("id") or ""),
            "{preset_en}": str(preset.get("en") or preset.get("id") or ""),
            "{preset_ko}": str(preset.get("ko") or preset.get("id") or ""),
        }
        if isinstance(value, str):
            rendered = value
            for token, replacement in replacements.items():
                rendered = rendered.replace(token, replacement)
            return rendered
        if isinstance(value, list):
            return [render_contract_template_value(item, preset) for item in value]
        if isinstance(value, dict):
            return {
                str(key): render_contract_template_value(item, preset)
                for key, item in value.items()
            }
        return copy.deepcopy(value)

    def deep_extend_render_contract(target: JsonDict, updates: JsonDict, label: str) -> None:
        for key, value in updates.items():
            key = str(key)
            if isinstance(value, dict):
                child = target.setdefault(key, {})
                if not isinstance(child, dict):
                    raise ValueError(f"{label}.{key}: cannot merge object into non-object")
                deep_extend_render_contract(child, value, f"{label}.{key}")
                continue
            if isinstance(value, list):
                child = target.setdefault(key, [])
                if not isinstance(child, list):
                    raise ValueError(f"{label}.{key}: cannot append list into non-list")
                if key == "scene_blueprints":
                    existing_ids = {
                        str(item.get("id") or "")
                        for item in child
                        if isinstance(item, dict)
                    }
                    for item in value:
                        if not isinstance(item, dict) or not str(item.get("id") or ""):
                            raise ValueError(f"{label}.{key}: every scene blueprint requires an id")
                        item_id = str(item.get("id"))
                        missing_fields = [
                            field
                            for field in ("subject", "action", "location", "prop")
                            if not str(item.get(field) or "").strip()
                        ]
                        if missing_fields:
                            raise ValueError(
                                f"{label}.{key}.{item_id}: missing scene fields {missing_fields}"
                            )
                        functions = normalize_list(item.get("scene_functions"))
                        if not functions:
                            raise ValueError(
                                f"{label}.{key}.{item_id}: scene_functions must be non-empty"
                            )
                        visual_provenance = normalize_list(
                            item.get("diegetic_visual_provenance")
                        )
                        if visual_provenance and len(set(visual_provenance)) != 1:
                            raise ValueError(
                                f"{label}.{key}.{item_id}: exactly one diegetic visual provenance is allowed"
                            )
                        if "operational" in item and not isinstance(item.get("operational"), bool):
                            raise ValueError(
                                f"{label}.{key}.{item_id}: operational must be boolean"
                            )
                        if item_id in existing_ids:
                            raise ValueError(f"{label}.{key}: duplicate scene blueprint id {item_id}")
                        child.append(copy.deepcopy(item))
                        existing_ids.add(item_id)
                else:
                    for item in value:
                        if item not in child:
                            child.append(copy.deepcopy(item))
                continue
            target[key] = copy.deepcopy(value)

    extension_presets = extension.get("presets") if isinstance(extension.get("presets"), list) else []
    render_contract_defaults = (
        extension.get("preset_render_contract_defaults")
        if isinstance(extension.get("preset_render_contract_defaults"), dict)
        else {}
    )
    for preset in extension_presets:
        if not isinstance(preset, dict):
            continue
        if auto_optional_policy:
            preset.setdefault("auto_optional_policy", auto_optional_policy)
        filters = preset.setdefault("filters", {})
        if not isinstance(filters, dict):
            raise ValueError(f"presets.{preset.get('id')}: filters must be an object")
        for slot, default_filter in preset_filter_defaults.items():
            if slot not in filters:
                filters[str(slot)] = default_filter
        if render_contract_defaults and not isinstance(preset.get("render_contract"), dict):
            preset["render_contract"] = render_contract_template_value(
                render_contract_defaults,
                preset,
            )
    append_unique_id_entries(data.setdefault("presets", []), extension_presets, "presets")

    presets_by_id = {
        str(preset.get("id")): preset
        for preset in data.get("presets", [])
        if isinstance(preset, dict) and str(preset.get("id") or "")
    }

    metadata_updates = extension.get("existing_preset_metadata_overrides") or {}
    allowed_metadata_keys = {
        "ko",
        "en",
        "weight",
        "template_style",
        "family",
        "embedding_text",
        "tags",
        "aliases",
        "keywords",
        "facets",
        "required_slots",
        "optional_slots",
        "automatic_discovery",
        "render_contract",
    }
    for preset_id, updates in metadata_updates.items():
        preset = presets_by_id.get(str(preset_id))
        if preset is None:
            raise ValueError(f"existing preset metadata override references unknown preset {preset_id}")
        if not isinstance(updates, dict):
            raise ValueError(f"existing preset metadata override for {preset_id} must be an object")
        unknown_keys = set(updates) - allowed_metadata_keys
        if unknown_keys:
            raise ValueError(
                f"existing preset metadata override for {preset_id} has unsupported keys {sorted(unknown_keys)}"
            )
        for key, value in updates.items():
            preset[str(key)] = copy.deepcopy(value)

    contract_extensions = extension.get("existing_preset_render_contract_extensions") or {}
    if not isinstance(contract_extensions, dict):
        raise ValueError("existing_preset_render_contract_extensions must be an object")
    for preset_id, updates in contract_extensions.items():
        preset = presets_by_id.get(str(preset_id))
        if preset is None:
            raise ValueError(f"render contract extension references unknown preset {preset_id}")
        if not isinstance(updates, dict):
            raise ValueError(f"render contract extension for {preset_id} must be an object")
        contract = preset.setdefault("render_contract", {})
        if not isinstance(contract, dict):
            raise ValueError(f"render contract target for {preset_id} must be an object")
        deep_extend_render_contract(
            contract,
            render_contract_template_value(updates, preset),
            f"existing_preset_render_contract_extensions.{preset_id}",
        )

    def existing_preset_filter_updates(mapping: Any, *, replace: bool) -> None:
        updates = mapping if isinstance(mapping, dict) else {}
        for preset_id, slot_updates in updates.items():
            preset = presets_by_id.get(str(preset_id))
            if preset is None:
                raise ValueError(f"existing preset filter update references unknown preset {preset_id}")
            if not isinstance(slot_updates, dict):
                raise ValueError(f"existing preset filter update for {preset_id} must be an object")
            filters = preset.setdefault("filters", {})
            for slot, filter_update in slot_updates.items():
                if not isinstance(filter_update, dict):
                    raise ValueError(f"existing preset filter update for {preset_id}.{slot} must be an object")
                if replace or slot not in filters:
                    filters[str(slot)] = {
                        str(key): list(value) if isinstance(value, list) else value
                        for key, value in filter_update.items()
                    }
                    continue
                target_filter = filters[str(slot)]
                if not isinstance(target_filter, dict):
                    raise ValueError(f"existing preset filter target {preset_id}.{slot} must be an object")
                for key, value in filter_update.items():
                    if not isinstance(value, list):
                        if key in target_filter and target_filter[key] != value:
                            raise ValueError(
                                f"existing preset filter extension cannot replace scalar {preset_id}.{slot}.{key}"
                            )
                        target_filter[str(key)] = value
                        continue
                    target_values = target_filter.setdefault(str(key), [])
                    if not isinstance(target_values, list):
                        raise ValueError(f"existing preset filter target {preset_id}.{slot}.{key} must be a list")
                    for item in value:
                        if item not in target_values:
                            target_values.append(item)

    existing_preset_filter_updates(extension.get("existing_preset_filter_extensions"), replace=False)
    existing_preset_filter_updates(extension.get("existing_preset_filter_overrides"), replace=True)

    slots = data.setdefault("slots", {})
    for slot, entries in (extension.get("slots") or {}).items():
        append_unique_id_entries(slots.setdefault(str(slot), []), entries, f"slots.{slot}")

    extension_coherence = extension.get("coherence_rules") or {}
    if not isinstance(extension_coherence, dict):
        raise ValueError("coherence_rules must be an object")
    coherence = data.setdefault("coherence_rules", {})
    if not isinstance(coherence, dict):
        raise ValueError("coherence_rules target must be an object")
    for collection in ("slot_conflicts", "slot_context_rules"):
        append_unique_id_entries(
            coherence.setdefault(collection, []),
            extension_coherence.get(collection),
            f"coherence_rules.{collection}",
        )

    extension_character_graph = extension.get("character_mechanism_graph")
    if extension_character_graph is not None:
        if not isinstance(extension_character_graph, dict):
            raise ValueError("character_mechanism_graph must be an object")
        if data.get("character_mechanism_graph"):
            raise ValueError("character_mechanism_graph may be declared by only one extension")
        data["character_mechanism_graph"] = copy.deepcopy(extension_character_graph)

    applicability = data.setdefault("slot_applicability", {})
    extension_applicability = extension.get("slot_applicability") or {}
    for mapping_key in ("preset_domain_overrides", "subject_category_overrides"):
        target_mapping = applicability.setdefault(mapping_key, {})
        for key, value in (extension_applicability.get(mapping_key) or {}).items():
            if key in target_mapping:
                raise ValueError(f"slot_applicability.{mapping_key}: duplicate extension key {key}")
            target_mapping[key] = value

    applicability_slots = applicability.setdefault("slots", {})
    for slot, policy_updates in (extension_applicability.get("slots") or {}).items():
        if not isinstance(policy_updates, dict):
            raise ValueError(f"slot_applicability.slots.{slot}: policy must be an object")
        target_policy = applicability_slots.setdefault(str(slot), {})
        if not isinstance(target_policy, dict):
            raise ValueError(f"slot_applicability.slots.{slot}: target policy must be an object")
        for key, value in policy_updates.items():
            if isinstance(value, list):
                target_values = target_policy.setdefault(str(key), [])
                if not isinstance(target_values, list):
                    raise ValueError(
                        f"slot_applicability.slots.{slot}.{key}: target must be a list"
                    )
                for item in value:
                    if item not in target_values:
                        target_values.append(item)
                continue
            if key in target_policy and target_policy[key] != value:
                raise ValueError(
                    f"slot_applicability.slots.{slot}.{key}: extension cannot replace scalar"
                )
            target_policy[str(key)] = value

    return data


def character_runtime_node_topic_ids(node: JsonDict) -> Set[str]:
    values = normalize_list(node.get("topic_ids"))
    if not values and str(node.get("topic_id") or ""):
        values = [str(node.get("topic_id"))]
    return {str(item) for item in values if str(item)}


def character_runtime_node_family_ids(node: JsonDict) -> Set[str]:
    values = normalize_list(node.get("family_ids"))
    if not values and str(node.get("family_id") or ""):
        values = [str(node.get("family_id"))]
    return {str(item) for item in values if str(item)}


def validate_character_mechanism_graph(data: JsonDict) -> None:
    """Validate the optional character graph and every bound preset scene.

    Character mechanisms stay outside the ordinary sampler pool.  Validation
    therefore treats scene runtime IDs as a small executable bundle: one
    primary visual atom plus at most two compatible support atoms.  Router and
    guard nodes may guide routing, but cannot masquerade as visual evidence.
    """
    graph = data.get("character_mechanism_graph")
    if not graph:
        return
    if not isinstance(graph, dict):
        raise ValueError("character_mechanism_graph must be an object")
    if graph.get("schema_version") != CHARACTER_MECHANISM_GRAPH_SCHEMA:
        raise ValueError(
            f"Unsupported character mechanism graph schema: {graph.get('schema_version')!r}"
        )
    domain = str(graph.get("domain") or "")
    if domain != "character_moe_grammar":
        raise ValueError(f"Unsupported character mechanism domain: {domain!r}")
    priority_order = normalize_list(graph.get("priority_order"))
    expected_priority = [
        "observable_action",
        "relationship_stake",
        "expression_or_gaze",
        "morphology_or_state",
        "costume",
    ]
    if priority_order != expected_priority:
        raise ValueError("character_mechanism_graph.priority_order must use the fixed sparse priority")
    max_support_cues = int(graph.get("max_support_cues", -1))
    if max_support_cues != 2:
        raise ValueError("character_mechanism_graph.max_support_cues must be 2")

    def unique_rows(key: str) -> Dict[str, JsonDict]:
        rows = graph.get(key)
        if not isinstance(rows, list) or not rows:
            raise ValueError(f"character_mechanism_graph.{key} must be a non-empty list")
        indexed: Dict[str, JsonDict] = {}
        for row in rows:
            if not isinstance(row, dict) or not str(row.get("id") or ""):
                raise ValueError(f"character_mechanism_graph.{key} entries require an id")
            row_id = str(row["id"])
            if row_id in indexed:
                raise ValueError(f"character_mechanism_graph.{key}: duplicate id {row_id}")
            indexed[row_id] = row
        return indexed

    families = unique_rows("families")
    nodes = unique_rows("runtime_nodes")
    policies = unique_rows("policies")
    edges = unique_rows("compatibility_edges")
    guards = unique_rows("guard_rules")
    topic_to_family: Dict[str, str] = {}
    for family_id, family in families.items():
        for topic_id in normalize_list(family.get("topic_ids")):
            if topic_id in topic_to_family:
                raise ValueError(f"character topic {topic_id} belongs to multiple families")
            topic_to_family[topic_id] = family_id
    if not topic_to_family:
        raise ValueError("character_mechanism_graph families declare no topics")

    valid_roles = {"visual_atom", "router", "guard"}
    for node_id, node in nodes.items():
        topic_ids = character_runtime_node_topic_ids(node)
        family_ids = character_runtime_node_family_ids(node)
        role = str(node.get("role") or "")
        if (
            not topic_ids
            or any(topic_id not in topic_to_family for topic_id in topic_ids)
            or family_ids != {topic_to_family[topic_id] for topic_id in topic_ids}
        ):
            raise ValueError(f"character runtime node {node_id} has invalid topic/family memberships")
        if role not in valid_roles:
            raise ValueError(f"character runtime node {node_id} has invalid role {role!r}")
        if not str(node.get("definition") or "").strip():
            raise ValueError(f"character runtime node {node_id} requires a definition")
        definition_lower = str(node.get("definition") or "").lower()
        obvious_nonvisual = (
            node_id.endswith("_guard")
            or node_id.endswith("_axis")
            or node_id.endswith("_limitation")
            or node_id.endswith("_declaration")
            or node_id.endswith("_evidence_map")
            or node_id in {"adult_work_or_life_context", "adult_peer_relationship_context"}
            or (
                "cjk_term_character_grammar_comparison" in topic_ids
                and ("term" in node_id or "alias" in node_id or "market_label" in node_id)
            )
            or "router" in definition_lower
            or "nonvisual" in definition_lower
            or definition_lower.startswith("guard:")
            or "safeguard" in definition_lower
        )
        if role == "visual_atom" and obvious_nonvisual:
            raise ValueError(f"character runtime node {node_id} misclassifies nonvisual guidance")
        if role == "visual_atom" and str(node.get("priority_dimension") or "") not in expected_priority:
            raise ValueError(f"character visual runtime node {node_id} has invalid priority dimension")

    for edge_id, edge in edges.items():
        topic_id = str(edge.get("topic_id") or "")
        node_ids = normalize_list(edge.get("node_ids"))
        if topic_id not in topic_to_family or not node_ids:
            raise ValueError(f"character compatibility edge {edge_id} has invalid topic or nodes")
        for node_id in node_ids:
            node = nodes.get(node_id)
            if (
                node is None
                or topic_id not in character_runtime_node_topic_ids(node)
                or str(node.get("role") or "") != "visual_atom"
            ):
                raise ValueError(f"character compatibility edge {edge_id} references invalid node {node_id}")
    for guard_id, guard in guards.items():
        topic_ids = normalize_list(guard.get("topic_ids"))
        if topic_ids and any(topic_id not in topic_to_family for topic_id in topic_ids):
            raise ValueError(f"character guard rule {guard_id} references an unknown topic")
        required_policies = normalize_list(guard.get("required_policy_ids"))
        if any(policy_id not in policies for policy_id in required_policies):
            raise ValueError(f"character guard rule {guard_id} references an unknown policy")
        forbidden_runtime_ids = normalize_list(guard.get("forbidden_runtime_ids"))
        if any(runtime_id not in nodes for runtime_id in forbidden_runtime_ids):
            raise ValueError(f"character guard rule {guard_id} references an unknown runtime node")
        forbidden_combinations = guard.get("forbidden_runtime_combinations") or []
        if not isinstance(forbidden_combinations, list):
            raise ValueError(f"character guard rule {guard_id} has invalid forbidden combinations")
        for combination in forbidden_combinations:
            combination_ids = normalize_list(combination)
            if len(set(combination_ids)) < 2 or any(runtime_id not in nodes for runtime_id in combination_ids):
                raise ValueError(f"character guard rule {guard_id} has an invalid forbidden combination")
        trigger_runtime_ids = normalize_list(guard.get("trigger_runtime_ids"))
        requires_runtime_any = normalize_list(guard.get("requires_runtime_any"))
        if any(runtime_id not in nodes for runtime_id in trigger_runtime_ids + requires_runtime_any):
            raise ValueError(f"character guard rule {guard_id} references an unknown conditional runtime node")
        if bool(trigger_runtime_ids) != bool(requires_runtime_any):
            raise ValueError(f"character guard rule {guard_id} requires both trigger and required runtime IDs")
        if (
            not required_policies
            and not forbidden_runtime_ids
            and not forbidden_combinations
            and not trigger_runtime_ids
        ):
            raise ValueError(f"character guard rule {guard_id} has no executable condition")
    for policy_id, policy in policies.items():
        if not str(policy.get("definition") or "").strip():
            raise ValueError(f"character policy {policy_id} requires a definition")

    character_presets = [
        preset
        for preset in data.get("presets", [])
        if isinstance(preset, dict) and domain in preset_domains(preset, data)
    ]
    preset_topic_ids: Set[str] = set()
    for preset in character_presets:
        preset_id = str(preset.get("id") or "")
        render_contract = preset.get("render_contract")
        grammar = (
            render_contract.get("character_grammar")
            if isinstance(render_contract, dict)
            and isinstance(render_contract.get("character_grammar"), dict)
            else {}
        )
        topic_id = str(grammar.get("topic_id") or "")
        family_id = str(grammar.get("family_id") or "")
        if topic_id not in topic_to_family or topic_to_family[topic_id] != family_id:
            raise ValueError(f"character preset {preset_id} has invalid topic/family binding")
        if topic_id in preset_topic_ids:
            raise ValueError(f"character topic {topic_id} is bound to multiple presets")
        preset_topic_ids.add(topic_id)
        policy_ids = normalize_list(grammar.get("policy_ids"))
        if any(policy_id not in policies for policy_id in policy_ids):
            raise ValueError(f"character preset {preset_id} references an unknown policy")
        runtime_anchor_ids = normalize_list(grammar.get("runtime_anchor_ids"))
        if not runtime_anchor_ids:
            raise ValueError(f"character preset {preset_id} requires runtime anchor IDs")
        for runtime_id in runtime_anchor_ids:
            node = nodes.get(runtime_id)
            if node is None or topic_id not in character_runtime_node_topic_ids(node):
                raise ValueError(f"character preset {preset_id} has invalid runtime anchor {runtime_id}")
        blueprints = (
            render_contract.get("scene_blueprints")
            if isinstance(render_contract, dict)
            and isinstance(render_contract.get("scene_blueprints"), list)
            else []
        )
        if len(blueprints) < 3:
            raise ValueError(f"character preset {preset_id} requires at least three scene blueprints")
        scene_functions: Set[str] = set()
        blueprint_ids: Set[str] = set()
        static_portrait_count = 0
        selected_runtime_bundles: Set[tuple[str, ...]] = set()
        selected_primary_ids: Set[str] = set()
        selected_runtime_union: Set[str] = set()
        micro_events: Set[tuple[str, str, str]] = set()
        required_evidence_types = set(normalize_list(grammar.get("required_evidence_types")))
        if not required_evidence_types:
            raise ValueError(f"character preset {preset_id} requires evidence-type bindings")
        for blueprint in blueprints:
            if not isinstance(blueprint, dict):
                raise ValueError(f"character preset {preset_id} has a non-object scene blueprint")
            blueprint_id = str(blueprint.get("id") or "")
            if not blueprint_id or blueprint_id in blueprint_ids:
                raise ValueError(f"character preset {preset_id} has a missing or duplicate blueprint ID")
            blueprint_ids.add(blueprint_id)
            micro_event = (
                str(blueprint.get("action") or "").strip(),
                str(blueprint.get("location") or "").strip(),
                str(blueprint.get("prop") or "").strip(),
            )
            if not all(micro_event) or micro_event in micro_events:
                raise ValueError(f"character scene {preset_id}.{blueprint_id} repeats an atomic micro-event")
            micro_events.add(micro_event)
            if not isinstance(blueprint.get("static_portrait"), bool):
                raise ValueError(f"character scene {preset_id}.{blueprint_id} requires static_portrait boolean")
            static_portrait_count += bool(blueprint.get("static_portrait"))
            if "adult" not in set(normalize_list(blueprint.get("subject_kind"))):
                raise ValueError(f"character scene {preset_id}.{blueprint_id} requires explicit adult subject metadata")
            visual_provenance = normalize_list(blueprint.get("diegetic_visual_provenance"))
            if len(visual_provenance) != 1 or len(set(visual_provenance)) != 1:
                raise ValueError(f"character scene {preset_id}.{blueprint_id} requires one visual provenance")
            if "nonvisual" not in str(blueprint.get("market_origin") or ""):
                raise ValueError(f"character scene {preset_id}.{blueprint_id} must keep market origin nonvisual")
            runtime_ids = normalize_list(blueprint.get("runtime_ids"))
            primary_id = str(blueprint.get("primary_runtime_id") or "")
            if not 1 <= len(runtime_ids) <= 1 + max_support_cues:
                raise ValueError(
                    f"character scene {preset_id}.{blueprint_id} must select one to three runtime IDs"
                )
            if len(runtime_ids) != len(set(runtime_ids)) or primary_id not in runtime_ids:
                raise ValueError(f"character scene {preset_id}.{blueprint_id} has an invalid primary/runtime set")
            selected_runtime_bundles.add(tuple(runtime_ids))
            selected_primary_ids.add(primary_id)
            selected_runtime_union.update(runtime_ids)
            scene_nodes: Dict[str, JsonDict] = {}
            for runtime_id in runtime_ids:
                node = nodes.get(runtime_id)
                if node is None or topic_id not in character_runtime_node_topic_ids(node):
                    raise ValueError(f"character scene {preset_id}.{blueprint_id} references invalid runtime ID {runtime_id}")
                if str(node.get("role") or "") != "visual_atom":
                    raise ValueError(f"character scene {preset_id}.{blueprint_id} selects nonvisual node {runtime_id}")
                scene_nodes[runtime_id] = node
            priority_rank = {value: index for index, value in enumerate(expected_priority)}
            primary_rank = priority_rank[str(scene_nodes[primary_id].get("priority_dimension"))]
            if any(
                priority_rank[str(scene_nodes[runtime_id].get("priority_dimension"))] < primary_rank
                for runtime_id in runtime_ids
                if runtime_id != primary_id
            ):
                raise ValueError(
                    f"character scene {preset_id}.{blueprint_id} promotes a lower-priority cue above its support"
                )
            if len(runtime_ids) > 1 and not any(
                str(edge.get("topic_id") or "") == topic_id
                and set(runtime_ids).issubset(set(normalize_list(edge.get("node_ids"))))
                for edge in edges.values()
            ):
                raise ValueError(f"character scene {preset_id}.{blueprint_id} has no compatibility edge")
            evidence_types = normalize_list(blueprint.get("character_evidence_types"))
            if not required_evidence_types.issubset(set(evidence_types)):
                raise ValueError(
                    f"character scene {preset_id}.{blueprint_id} does not cover its required evidence types"
                )
            scene_functions.update(normalize_list(blueprint.get("scene_functions")))
        if static_portrait_count / len(blueprints) > 0.5:
            raise ValueError(f"character preset {preset_id} has a static-portrait majority")
        available_visual_ids = {
            node_id
            for node_id, node in nodes.items()
            if topic_id in character_runtime_node_topic_ids(node)
            and str(node.get("role") or "") == "visual_atom"
        }
        minimum_primary_or_bundle_diversity = min(2, len(available_visual_ids))
        minimum_runtime_union = min(4, len(available_visual_ids))
        if (
            len(selected_primary_ids) < minimum_primary_or_bundle_diversity
            or len(selected_runtime_bundles) < minimum_primary_or_bundle_diversity
            or len(selected_runtime_union) < minimum_runtime_union
        ):
            raise ValueError(
                f"character preset {preset_id} does not rotate enough available runtime evidence"
            )
        if len(scene_functions) < 2:
            raise ValueError(f"character preset {preset_id} requires at least two scene functions")
    if preset_topic_ids != set(topic_to_family):
        missing = sorted(set(topic_to_family) - preset_topic_ids)
        extra = sorted(preset_topic_ids - set(topic_to_family))
        raise ValueError(f"character preset/topic coverage mismatch missing={missing} extra={extra}")


def load_json(path: str | Path) -> JsonDict:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Tag JSON not found: {p}")
    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if p.name == "photo_prompt_tags.json":
        for extension_filename in RESEARCH_EXTENSION_FILENAMES:
            extension_path = p.with_name(extension_filename)
            if not extension_path.exists():
                continue
            with extension_path.open("r", encoding="utf-8") as f:
                extension = json.load(f)
            data = merge_research_extension(data, extension)
        validate_character_mechanism_graph(data)
    return data


def default_quality_layers_path(tags_path: str | Path) -> Path:
    tags = Path(tags_path)
    if tags.parent:
        return tags.parent / QUALITY_LAYERS_FILENAME
    return Path(QUALITY_LAYERS_FILENAME)


def load_quality_layers(path: str | Path) -> JsonDict:
    return load_json(path)


def load_anchor_diversity_ledger(path: Optional[str]) -> JsonDict:
    if not path:
        return {}
    ledger_path = Path(path)
    if not ledger_path.exists():
        return {}
    try:
        payload = json.loads(ledger_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def save_anchor_diversity_ledger(path: Optional[str], ledger: JsonDict) -> None:
    if not path:
        return
    ledger_path = Path(path)
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def result_choice_ids(result: JsonDict) -> Dict[str, str]:
    choices: Dict[str, str] = {}
    for slot, value in (result.get("choices") or {}).items():
        if isinstance(value, dict):
            choices[slot] = str(value.get("id") or "")
        elif value:
            choices[slot] = str(value)
    return choices


def motif_group_taxonomy_from_policy(policy: Optional[JsonDict] = None) -> Dict[str, List[str]]:
    taxonomy: Dict[str, List[str]] = {
        group: list(terms)
        for group, terms in CANDIDATE_PACK_MOTIF_TAXONOMY.items()
    }
    raw_pools = (policy or {}).get("motif_pools") if isinstance(policy, dict) else {}
    if isinstance(raw_pools, dict):
        for group, pool in raw_pools.items():
            group_id = str(group or "").strip()
            if not group_id or not isinstance(pool, dict):
                continue
            values = taxonomy.setdefault(group_id, [])
            for term in normalize_list(pool.get("terms")):
                if term not in values:
                    values.append(term)
            slot_candidates = pool.get("slot_candidates")
            if isinstance(slot_candidates, dict):
                for ids in slot_candidates.values():
                    for entry_id in normalize_list(ids):
                        if entry_id not in values:
                            values.append(entry_id)
    return taxonomy


def infer_motif_groups_from_blob(blob: str, taxonomy: Optional[Dict[str, Sequence[str]]] = None) -> List[str]:
    normalized_blob = str(blob or "").lower()
    if not normalized_blob:
        return []
    groups: List[str] = []
    for group, terms in (taxonomy or CANDIDATE_PACK_MOTIF_TAXONOMY).items():
        for term in terms:
            normalized_term = str(term or "").strip().lower()
            if normalized_term and normalized_term in normalized_blob:
                groups.append(str(group))
                break
    return sorted(dict.fromkeys(groups))


def infer_motif_groups_from_choice_ids(
    choices: Dict[str, str],
    policy: Optional[JsonDict] = None,
) -> List[str]:
    taxonomy = motif_group_taxonomy_from_policy(policy)
    blob = " ".join(f"{slot} {entry_id}" for slot, entry_id in choices.items() if entry_id)
    return infer_motif_groups_from_blob(blob, taxonomy)


def update_anchor_diversity_ledger(ledger: JsonDict, result: JsonDict) -> None:
    trace = result.get("semantic_trace", {}) or {}
    contract = trace.get("generation_contract", {}) or {}
    policy = contract.get("soft_anchor_policy", {}) or {}
    if not policy.get("enabled"):
        return
    choices = result_choice_ids(result)
    species_policy = policy.get("species_family_policy") if isinstance(policy.get("species_family_policy"), dict) else {}
    family = str(species_policy.get("family") or "").strip()
    if family:
        family_counts = ledger.setdefault("species_family", {})
        family_counts[family] = int(family_counts.get(family, 0)) + 1
    variant_id = str(species_policy.get("variant_id") or "").strip()
    if variant_id:
        variant_counts = ledger.setdefault("species_variant", {})
        variant_counts[variant_id] = int(variant_counts.get(variant_id, 0)) + 1
    role_policy = policy.get("role_scene_policy") if isinstance(policy.get("role_scene_policy"), dict) else {}
    allowed_locations = set(normalize_list(role_policy.get("allowed_locations")))
    selected_location = choices.get("location", "")
    if role_policy.get("enabled") and selected_location and selected_location in allowed_locations:
        location_counts = ledger.setdefault("location", {})
        location_counts[selected_location] = int(location_counts.get(selected_location, 0)) + 1
    motif_counts = ledger.setdefault("motif_group", {})
    for motif_group in infer_motif_groups_from_choice_ids(choices, policy):
        motif_counts[motif_group] = int(motif_counts.get(motif_group, 0)) + 1
    for anchor in policy.get("anchors", []) or []:
        group = str(anchor.get("variant_group") or "")
        slot = str(anchor.get("slot") or "")
        selected = str(anchor.get("selected") or "") or choices.get(slot)
        pool = set(normalize_list(anchor.get("pool")) or normalize_list(anchor.get("ids")))
        if not group or not slot or not selected or selected not in pool:
            continue
        slot_counts = ledger.setdefault(slot, {})
        slot_counts[selected] = int(slot_counts.get(selected, 0)) + 1


def localize(item: JsonDict, lang: str) -> str:
    """Return localized text from {'ko': '...', 'en': '...'} style objects."""
    if lang in item and item[lang]:
        return str(item[lang])
    if "en" in item and item["en"]:
        return str(item["en"])
    if "ko" in item and item["ko"]:
        return str(item["ko"])
    if "id" in item:
        return str(item["id"])
    return ""


def last_hangul_char(text: str) -> Optional[str]:
    for ch in reversed(text.strip()):
        if "\uac00" <= ch <= "\ud7a3":
            return ch
    return None


def has_batchim(text: str) -> bool:
    ch = last_hangul_char(text)
    if ch is None:
        return False
    return (ord(ch) - 0xAC00) % 28 != 0


def josa(text: str, with_batchim: str, without_batchim: str) -> str:
    """Very small Korean particle helper: 을/를, 이/가, 은/는, etc."""
    return with_batchim if has_batchim(text) else without_batchim


def clean_spaces(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)
    text = re.sub(r"([.!?]){2,}", r"\1", text)
    return text


def ensure_period(text: str) -> str:
    text = clean_spaces(text)
    if text and text[-1] not in ".!?。":
        text += "."
    return text


def stable_text_id(text: Optional[str], length: int = 16) -> Optional[str]:
    if text is None:
        return None
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length]


def has_cli_option(args: Sequence[str], name: str) -> bool:
    return name in args or any(arg.startswith(name + "=") for arg in args)


def article_for(phrase: str) -> str:
    """Return a simple English indefinite article for a rendered noun phrase."""
    word = clean_spaces(phrase).lower().split(" ", 1)[0] if phrase else ""
    if not word:
        return "a"
    if word.startswith(("honest", "hour", "heir")):
        return "an"
    if word.startswith(("uni", "use", "user", "euro", "one")):
        return "a"
    return "an" if word[0] in "aeiou" else "a"


def with_indefinite_article(phrase: str) -> str:
    phrase = clean_spaces(phrase)
    if not phrase:
        return ""
    if phrase.lower().startswith(("a ", "an ", "the ")):
        return phrase
    return f"{article_for(phrase)} {phrase}"


def entry_tags(entry: Entry) -> Set[str]:
    return set(entry.get("tags", []))


def entry_kinds(entry: Entry) -> Set[str]:
    kinds = set(entry.get("kind", []))
    return kinds or entry_tags(entry)


def entry_context_tokens(entry: Entry) -> Set[str]:
    tokens = set(entry_tags(entry)) | set(entry_kinds(entry))
    if entry.get("id"):
        tokens.add(str(entry["id"]))
    return tokens


def picked_context_tokens(picked: Dict[str, Entry]) -> Set[str]:
    tokens: Set[str] = set()
    for slot, entry in picked.items():
        tokens.add(slot)
        tokens.add(f"slot:{slot}")
        tokens |= entry_context_tokens(entry)
        if entry.get("id"):
            tokens.add(f"{slot}:{entry['id']}")
    return tokens


def is_visible_multi_subject_prompt(picked: Dict[str, Entry]) -> bool:
    return bool(picked_context_tokens(picked) & {"visible_partner", "multi_subject"})


def picked_core_context_tokens(picked: Dict[str, Entry]) -> Set[str]:
    tokens: Set[str] = set()
    for slot in ("medium", "genre", "subject", "location"):
        entry = picked.get(slot)
        if entry:
            tokens |= entry_context_tokens(entry)
    return tokens


def picked_scene_context_tokens(picked: Dict[str, Entry]) -> Set[str]:
    tokens: Set[str] = set()
    for slot in ("medium", "genre", "location"):
        entry = picked.get(slot)
        if entry:
            tokens |= entry_context_tokens(entry)
    return tokens


def slot_applicability_from_source(source: Optional[JsonDict]) -> JsonDict:
    configured = (source or {}).get("slot_applicability", {}) or {}
    merged: JsonDict = {
        "subject_category_overrides": dict(DEFAULT_SLOT_APPLICABILITY["subject_category_overrides"]),
        "preset_domain_overrides": dict(DEFAULT_SLOT_APPLICABILITY["preset_domain_overrides"]),
        "slots": {
            slot: dict(policy)
            for slot, policy in DEFAULT_SLOT_APPLICABILITY["slots"].items()
        },
    }
    if not isinstance(configured, dict):
        return merged
    for key in ("subject_category_overrides", "preset_domain_overrides"):
        if isinstance(configured.get(key), dict):
            merged[key].update(configured[key])
    if isinstance(configured.get("slots"), dict):
        for slot, policy in configured["slots"].items():
            if isinstance(policy, dict):
                current = dict(merged["slots"].get(slot, {}))
                current.update(policy)
                merged["slots"][slot] = current
    return merged


def subject_category_overrides(source: Optional[JsonDict]) -> Dict[str, str]:
    return {
        str(entry_id): str(category)
        for entry_id, category in (slot_applicability_from_source(source).get("subject_category_overrides", {}) or {}).items()
    }


def subject_category(picked: Dict[str, Entry], source: Optional[JsonDict] = None) -> str:
    subject = picked.get("subject")
    if not subject:
        return "generic"

    subject_id = str(subject.get("id", ""))
    override = subject_category_overrides(source).get(subject_id)
    if override in VALID_SUBJECT_CATEGORIES:
        return override

    tokens = entry_context_tokens(subject) | facet_tokens(subject)
    subject_id = str(subject.get("id", ""))
    blob = " ".join(
        str(subject.get(key, ""))
        for key in ("id", "en", "ko", "embedding_text")
    ).lower()
    if "human" in tokens:
        return "human"
    if "animal" in tokens:
        return "animal"
    if "food" in tokens:
        return "food"
    if "environment" in entry_kinds(subject):
        return "environment"
    if "sign" in subject_id or "screen" in tokens or "text" in tokens:
        return "sign"
    object_signals = {
        "object",
        "product",
        "vehicle",
        "robot",
        "technology",
        "science",
        "jewelry",
        "watch",
        "commercial",
        "packshot",
        "prop",
    }
    if tokens & object_signals or any(
        fragment in blob
        for fragment in ("jewelry", "ring", "watch", "wristwatch", "camera", "phone", "bottle", "product", "object")
    ):
        return "object"
    plant_signals = {"plant", "botanical", "flower", "floral", "leaf", "leaves", "moss", "fungus", "mushroom"}
    if tokens & plant_signals or any(fragment in blob for fragment in ("plant", "botanical", "flower", "leaf", "moss")):
        return "plant"
    if tokens & {"landscape", "nature", "interior", "architecture", "urban"} and not tokens & {"object", "product", "vehicle"}:
        return "environment"
    return "generic"


def infer_preset_domains(preset: JsonDict) -> Set[str]:
    text = " ".join(
        str(preset.get(key, ""))
        for key in ("id", "en", "ko", "embedding_text")
    ).lower()
    text += " " + " ".join(str(item).lower() for item in normalize_list(preset.get("tags")) + normalize_list(preset.get("keywords")))
    domain_terms: Dict[str, tuple[str, ...]] = {
        "portrait": ("portrait", "profile", "selfie", "headshot", "인물"),
        "fashion": ("fashion", "editorial", "runway", "wardrobe", "style", "패션"),
        "beauty": ("beauty", "makeup", "skincare", "kbeauty", "뷰티"),
        "social": ("social", "creator", "influencer", "tiktok", "instagram", "vlogger"),
        "product": ("product", "packshot", "commercial", "cpg", "skincare", "catalog"),
        "jewelry": ("jewelry", "ring", "macro_reflection"),
        # "cafe" intentionally excluded: cafe-set portrait presets (maid cafe,
        # coquette cafe) are person-centric, and the food domain denies the
        # person-styling slots via slot_applicability.
        "food": ("food", "street_food", "pojangmacha", "tteokbokki"),
        "wildlife": ("wildlife", "animal", "nature_wildlife"),
        "documentary": ("documentary", "reportage", "candid"),
        "craft": ("craft", "craftsperson", "workshop", "artisan", "ceramic", "glassblowing"),
        "street": ("street", "bus_stop", "subway", "alley", "pojangmacha"),
        "urban": ("urban", "city", "neon", "hotel_corridor", "laundromat", "parking"),
        "architecture": ("architecture", "real_estate", "interior", "brutalist"),
        "science_inspection": ("scientific inspection", "technical measurement", "inspection record", "sensor survey", "measurement record"),
        "mobility_logistics": ("mobility logistics", "warehouse flow", "transit maintenance", "parcel sorting", "freight operations"),
        "climate_adaptation": ("climate adaptation", "resilience monitoring", "heat monitoring", "air quality record", "coastal erosion monitoring"),
        "biodiversity_monitoring": ("biodiversity monitoring", "species monitoring", "camera trap survey", "quadrat survey", "ecological monitoring"),
        "agriculture_food_systems": ("agriculture food systems", "harvest grading record", "fermentation batch monitoring", "post-harvest traceability"),
        "circular_materials": ("circular materials", "repair diagnostic record", "materials recovery sorting", "reuse inspection", "material flow audit"),
        "heritage_documentation": ("cultural heritage documentation", "conservation photography", "condition assessment record", "museum digitization", "collection storage inspection", "photogrammetry capture"),
        "health_access": ("person centered rehabilitation", "assistive technology fitting", "accessible route record", "community health access", "home care support"),
        "sports_motion": ("sports biomechanics", "pre contact anticipation", "impact material response", "post exertion recovery"),
        "education_training": ("guided skill learning", "supervised practice", "task demonstration", "competency assessment", "workplace learning"),
        "disaster_risk_operations": ("post disaster safety record", "evacuation flow monitoring", "wildfire mitigation audit", "post flood evidence survey"),
        "human_interaction": ("shared task interaction", "two people coordinating", "joint gaze shared workpiece", "small group interaction"),
        "natural_process": ("natural process trace", "germination boundary", "freeze thaw soil", "erosion deposition balance", "biological soil crust"),
        "longitudinal_place_state": ("longitudinal place state", "repeat photography", "same viewpoint record", "temporary closure record", "reopening readiness"),
        "visual_structure": ("visual structure study", "figure ground boundary", "occlusion continuity", "repeated rhythm", "material state boundary", "canonical size anchor"),
        "surreal": ("surreal", "fantasy", "impossible", "dream"),
        "adult": ("adult", "boudoir", "fetish", "lingerie"),
    }
    return {
        domain
        for domain, terms in domain_terms.items()
        if any(term in text for term in terms)
    }


def preset_domains(preset: JsonDict, source: Optional[JsonDict]) -> Set[str]:
    overrides = slot_applicability_from_source(source).get("preset_domain_overrides", {}) or {}
    preset_id = str(preset.get("id", ""))
    if preset_id in overrides:
        return {str(domain) for domain in normalize_list(overrides[preset_id]) if str(domain) in VALID_PRESET_DOMAINS}
    domains = infer_preset_domains(preset)
    if preset_uses_adult_context(preset):
        domains.add("adult")
    return domains


def make_generation_contract(
    data: JsonDict,
    preset: JsonDict,
    picked: Dict[str, Entry],
    forced_choices: Optional[Dict[str, List[str]]] = None,
    surreal_enabled: bool = False,
    concept_locks: Optional[Sequence[str]] = None,
    additional_requirements: Optional[Sequence[str]] = None,
    likeness_mode: str = "off",
    likeness_references: Optional[Sequence[str]] = None,
    user_mandatory_intents: Optional[Sequence[str]] = None,
    concept_gate_results: Optional[Sequence[JsonDict]] = None,
    concept_scene_variants: Optional[Sequence[str]] = None,
    safety_evaluation_requested: bool = False,
    soft_anchor_spec: Optional[JsonDict] = None,
) -> JsonDict:
    forced_slots = sorted((forced_choices or {}).keys())
    domains = sorted(preset_domains(preset, data))
    soft_anchor_policy = soft_anchor_trace(normalize_soft_anchor_spec(soft_anchor_spec), picked)
    safety_evaluation = soft_anchor_policy.get("safety_evaluation")
    if not isinstance(safety_evaluation, dict) or not safety_evaluation:
        safety_evaluation = {
            "mode": "explicit_evaluation" if safety_evaluation_requested else "automatic",
            "evaluation_requested": bool(safety_evaluation_requested),
            "status": "pass",
            "requires_user_approval": False,
            "items": [],
        }
    contract: JsonDict = {
        "subject_category": subject_category(picked, data),
        "preset_domains": domains,
        "forced_slots": forced_slots,
        "surreal_enabled": bool(surreal_enabled or any(slot in picked for slot in SURREAL_LAYER_SLOTS)),
        "adult_allowed": bool("adult" in domains or preset_uses_adult_context(preset)),
        "must_cover_axes": [],
        "covered_axes": [],
        "coverage_gaps": [],
        "coverage_events": [],
        "reselect_events": [],
        "skipped_slots": [],
        "render_suppressed_slots": [],
        "fallback_blocked_slots": [],
        "concept_locks": normalize_concept_locks(concept_locks),
        "additional_requirements": normalize_additional_requirements(additional_requirements),
        "likeness_mode": likeness_mode,
        "likeness_references": normalize_list(likeness_references),
        "user_mandatory_intents": normalize_list(user_mandatory_intents),
        "concept_gate_results": [dict(item) for item in concept_gate_results or [] if isinstance(item, dict)],
        "concept_scene_variants": normalize_list(concept_scene_variants),
        "intent_constraints": {},
        "candidate_pool_trace": {},
        "safety": safety_evaluation,
        "soft_anchor_policy": soft_anchor_policy,
        "soft_anchor_repair": {"status": "not_evaluated", "repair_attempts": []},
    }
    semantic_intent = str(contract.get("semantic_intent") or "").strip()
    contract["intent_constraints"] = resolve_request_intent_constraints(
        data,
        {"intent": semantic_intent} if semantic_intent else None,
        contract,
    )
    return contract


def refresh_generation_contract(
    contract: Optional[JsonDict],
    data: JsonDict,
    preset: JsonDict,
    picked: Dict[str, Entry],
    forced_choices: Optional[Dict[str, List[str]]] = None,
    surreal_enabled: Optional[bool] = None,
    concept_locks: Optional[Sequence[str]] = None,
    additional_requirements: Optional[Sequence[str]] = None,
    likeness_mode: Optional[str] = None,
    likeness_references: Optional[Sequence[str]] = None,
    user_mandatory_intents: Optional[Sequence[str]] = None,
    concept_gate_results: Optional[Sequence[JsonDict]] = None,
    concept_scene_variants: Optional[Sequence[str]] = None,
    safety_evaluation_requested: Optional[bool] = None,
    soft_anchor_spec: Optional[JsonDict] = None,
) -> JsonDict:
    if contract is None:
        return make_generation_contract(
            data,
            preset,
            picked,
            forced_choices,
            surreal_enabled=bool(surreal_enabled),
            concept_locks=concept_locks,
            additional_requirements=additional_requirements,
            likeness_mode=likeness_mode or "off",
            likeness_references=likeness_references,
            user_mandatory_intents=user_mandatory_intents,
            concept_gate_results=concept_gate_results,
            concept_scene_variants=concept_scene_variants,
            safety_evaluation_requested=bool(safety_evaluation_requested),
            soft_anchor_spec=soft_anchor_spec,
        )
    contract["subject_category"] = subject_category(picked, data)
    contract["preset_domains"] = sorted(preset_domains(preset, data))
    contract["forced_slots"] = sorted((forced_choices or {}).keys())
    if concept_locks is not None:
        contract["concept_locks"] = normalize_concept_locks(concept_locks)
    else:
        contract.setdefault("concept_locks", [])
    if additional_requirements is not None:
        contract["additional_requirements"] = normalize_additional_requirements(additional_requirements)
    else:
        contract.setdefault("additional_requirements", [])
    if likeness_mode is not None:
        contract["likeness_mode"] = likeness_mode
    else:
        contract.setdefault("likeness_mode", "off")
    if likeness_references is not None:
        contract["likeness_references"] = normalize_list(likeness_references)
    else:
        contract.setdefault("likeness_references", [])
    if user_mandatory_intents is not None:
        contract["user_mandatory_intents"] = normalize_list(user_mandatory_intents)
    else:
        contract.setdefault("user_mandatory_intents", [])
    if concept_gate_results is not None:
        contract["concept_gate_results"] = [
            dict(item) for item in concept_gate_results if isinstance(item, dict)
        ]
    else:
        contract.setdefault("concept_gate_results", [])
    if concept_scene_variants is not None:
        contract["concept_scene_variants"] = normalize_list(concept_scene_variants)
    else:
        contract.setdefault("concept_scene_variants", [])
    contract.setdefault("candidate_pool_trace", {})
    semantic_intent = str(contract.get("semantic_intent") or "").strip()
    contract["intent_constraints"] = resolve_request_intent_constraints(
        data,
        {"intent": semantic_intent} if semantic_intent else None,
        contract,
    )
    if surreal_enabled is not None:
        contract["surreal_enabled"] = bool(surreal_enabled)
    if any(slot in picked for slot in SURREAL_LAYER_SLOTS):
        contract["surreal_enabled"] = True
    contract["adult_allowed"] = bool("adult" in set(contract.get("preset_domains", [])) or preset_uses_adult_context(preset))
    if soft_anchor_spec is not None:
        contract["soft_anchor_policy"] = soft_anchor_trace(normalize_soft_anchor_spec(soft_anchor_spec), picked)
    else:
        contract["soft_anchor_policy"] = soft_anchor_trace(contract.get("soft_anchor_policy", {}), picked)
    safety_evaluation = contract["soft_anchor_policy"].get("safety_evaluation")
    if isinstance(safety_evaluation, dict) and safety_evaluation:
        contract["safety"] = safety_evaluation
    else:
        requested = bool(safety_evaluation_requested) if safety_evaluation_requested is not None else bool(
            (contract.get("safety") or {}).get("evaluation_requested")
        )
        contract["safety"] = {
            "mode": "explicit_evaluation" if requested else "automatic",
            "evaluation_requested": requested,
            "status": "pass",
            "requires_user_approval": False,
            "items": [],
        }
    contract.setdefault("soft_anchor_repair", {"status": "not_evaluated", "repair_attempts": []})
    for key in (
        "must_cover_axes",
        "covered_axes",
        "coverage_gaps",
        "coverage_events",
        "reselect_events",
        "skipped_slots",
        "render_suppressed_slots",
        "fallback_blocked_slots",
    ):
        contract.setdefault(key, [])
    return contract


def record_generation_contract_event(contract: Optional[JsonDict], key: str, event: JsonDict) -> None:
    if contract is None:
        return
    events = contract.setdefault(key, [])
    signature = json.dumps(event, ensure_ascii=False, sort_keys=True)
    existing = {json.dumps(item, ensure_ascii=False, sort_keys=True) for item in events}
    if signature not in existing:
        events.append(event)


def must_cover_enabled(context: Optional[JsonDict]) -> bool:
    if not context or context.get("intent_source") == "default":
        return False
    intent_axes = context.get("intent_axes", {}) or {}
    if intent_axes.get("source") == "default_full_intent":
        return False
    return bool(context.get("axis_vectors"))


def axis_covered_by_item(item: JsonDict, target: float) -> bool:
    strength = str(item.get("best_strength", "none"))
    if strength in {"strong", "ambient"}:
        return True
    return float(item.get("best_score", 0.0)) >= target


def sync_generation_contract_axis_coverage(contract: Optional[JsonDict], context: Optional[JsonDict]) -> None:
    if contract is None:
        return
    if not must_cover_enabled(context):
        contract["must_cover_axes"] = []
        contract["covered_axes"] = []
        contract["coverage_gaps"] = []
        return
    coverage = (context or {}).get("axis_coverage", {}) or {}
    target = float(coverage.get("target", 0.0))
    must_cover: List[JsonDict] = []
    covered: List[JsonDict] = []
    gaps: List[JsonDict] = []
    for item in coverage.get("items", []):
        row = {
            "index": int(item.get("index", -1)),
            "text": item.get("text", ""),
            "families": item.get("families", []),
            "target": round(target, 4),
            "best_score": round(float(item.get("best_score", 0.0)), 4),
            "best_slot": item.get("best_slot"),
            "best_entry": item.get("best_entry"),
            "best_strength": item.get("best_strength", "none"),
        }
        must_cover.append(row)
        if axis_covered_by_item(item, target):
            covered.append(row)
        else:
            gaps.append(row)
    contract["must_cover_axes"] = must_cover
    contract["covered_axes"] = covered
    contract["coverage_gaps"] = gaps


def slot_applicability_policy(data: JsonDict, slot: str) -> JsonDict:
    return slot_applicability_from_source(data).get("slots", {}).get(slot, {}) or {}


def slot_block_reason(
    data: JsonDict,
    slot: str,
    generation_contract: Optional[JsonDict],
    forced: bool = False,
) -> Optional[str]:
    if forced or generation_contract is None:
        return None
    policy = slot_applicability_policy(data, slot)
    if not policy:
        return None
    subject_cat = str(generation_contract.get("subject_category", "generic"))
    domains = set(generation_contract.get("preset_domains", []))
    allowed_categories = set(normalize_list(policy.get("subject_categories")))
    denied_categories = set(normalize_list(policy.get("deny_subject_categories")))
    allowed_domains = set(normalize_list(policy.get("allow_domains")))
    denied_domains = set(normalize_list(policy.get("deny_domains")))

    if subject_cat in denied_categories:
        return "subject_category_denied"
    subject_category_domain_override = bool(
        policy.get("allow_domains_override_subject_categories")
        and allowed_domains
        and domains & allowed_domains
    )
    if allowed_categories and subject_cat not in allowed_categories and not subject_category_domain_override:
        return "subject_category_not_allowed"
    if domains & denied_domains:
        return "preset_domain_denied"
    if policy.get("require_domain_match") and allowed_domains and not (domains & allowed_domains):
        return "preset_domain_not_allowed"
    return None


def entry_block_reason(
    item: Entry,
    slot: str,
    generation_contract: Optional[JsonDict],
    forced: bool = False,
) -> Optional[str]:
    if forced or generation_contract is None:
        return None
    intent_constraints = generation_contract.get("intent_constraints") or {}
    if isinstance(intent_constraints, dict) and intent_constraints.get("no_people"):
        if "human" in (entry_kinds(item) | entry_tags(item)):
            return "explicit_no_people"
    requested_categories = {
        str(value)
        for value in normalize_list(intent_constraints.get("subject_categories"))
        if str(value) in VALID_SUBJECT_CATEGORIES
    } if isinstance(intent_constraints, dict) else set()
    typed_nonhuman_person_slots = {
        "appearance_type", "body_framing", "body_orientation", "body_pose", "brow_style",
        "costume_style", "eye_detail", "eye_makeup_line", "facial_hair", "footwear",
        "gaze_engagement", "hair_color", "hair_style", "hand_pose", "lip_finish",
        "makeup_style", "person_origin", "silhouette_proportion", "skin_finish", "wardrobe_style",
    }
    if (
        requested_categories
        and "human" not in requested_categories
        and str(generation_contract.get("subject_category") or "generic") != "human"
        and slot in typed_nonhuman_person_slots
    ):
        if "human" in (entry_kinds(item) | entry_tags(item)):
            return "typed_nonhuman_request"
    if not generation_contract.get("adult_allowed"):
        tokens = adult_semantic_tokens(item)
        if tokens & {"adult", "fetish", "suggestive"}:
            if str(item.get("id", "")) not in soft_anchor_all_ids(generation_contract.get("soft_anchor_policy")):
                return "adult_not_allowed"
        if slot in {"adult_context", "fetish_styling"}:
            return "adult_slot_not_allowed"
    subject_cat = str(generation_contract.get("subject_category", "generic"))
    if subject_cat in {"object", "food", "plant", "environment", "sign"} and slot in {"genre", "texture", "focus", "color"}:
        tokens = entry_context_tokens(item) | facet_tokens(item)
        blob = " ".join(str(item.get(key, "")) for key in ("id", "en", "ko", "embedding_text")).lower()
        human_visual_terms = {"human", "portrait", "fashion", "beauty", "skin"}
        if tokens & human_visual_terms or any(term in blob for term in human_visual_terms):
            return "human_visual_signal_not_allowed"
    if subject_cat in {"object", "food", "sign"} and slot in {"lighting", "light_direction", "light_type", "light_shape", "texture"}:
        tokens = entry_context_tokens(item) | facet_tokens(item)
        blob = " ".join(str(item.get(key, "")) for key in ("id", "en", "ko", "embedding_text")).lower()
        plant_detail_terms = {"plant", "botanical", "leaf", "leaves", "stem", "stems", "spore", "spores"}
        if tokens & plant_detail_terms or any(term in blob for term in plant_detail_terms):
            return "plant_detail_signal_not_allowed"
    return None


def apply_anchor_reachability_guard(
    slot: str,
    pool: Sequence[Entry],
    data: JsonDict,
    generation_contract: Optional[JsonDict],
) -> List[Entry]:
    """Drop subject candidates whose category would deny another anchor slot.

    The subject pick fixes subject_category, and slot_applicability can then
    skip slots that still carry soft anchors (e.g. an automaton subject makes
    a human-only makeup anchor permanently unreachable). Falls back to the
    original pool when every candidate would block something.
    """
    if slot != "subject" or generation_contract is None:
        return list(pool)
    policy = generation_contract.get("soft_anchor_policy") or {}
    anchor_slots = {
        str(anchor.get("slot") or "")
        for anchor in (policy.get("anchors") or [])
        if anchor.get("slot") and anchor.get("slot") != "subject"
    }
    if not anchor_slots:
        return list(pool)
    # Anchors on both sides of a category divide (e.g. human-only makeup vs
    # robot-only surface_material) mean no candidate is conflict-free: keep
    # the candidates that leave the most anchor slots reachable.
    scored: List[tuple[int, Entry, List[str], str]] = []
    for item in pool:
        category = subject_category({"subject": item}, data)
        denied_slots: List[str] = []
        for anchor_slot in sorted(anchor_slots):
            slot_policy = slot_applicability_policy(data, anchor_slot)
            if not slot_policy:
                continue
            allowed = set(normalize_list(slot_policy.get("subject_categories")))
            denied = set(normalize_list(slot_policy.get("deny_subject_categories")))
            if category in denied or (allowed and category not in allowed):
                denied_slots.append(anchor_slot)
        scored.append((len(denied_slots), item, denied_slots, category))
    best = min(count for count, *_ in scored)
    if best == max(count for count, *_ in scored):
        return list(pool)
    survivors = [item for count, item, _slots, _cat in scored if count == best]
    blocked = [
        {"id": item.get("id"), "category": category, "denied_anchor_slots": denied_slots}
        for count, item, denied_slots, category in scored
        if count > best
    ]
    record_generation_contract_event(
        generation_contract,
        "reselect_events",
        {"slot": slot, "status": "anchor_reachability_filtered", "filtered": blocked},
    )
    return survivors


def reconcile_contract_blocked_picks(
    data: JsonDict,
    preset: JsonDict,
    rng: random.Random,
    picked: Dict[str, Entry],
    forced_choices: Optional[Dict[str, List[str]]] = None,
    semantic_context: Optional[JsonDict] = None,
    generation_contract: Optional[JsonDict] = None,
) -> None:
    """Re-pick slots whose entry became contract-blocked after later picks.

    The contract evolves while slots are picked (e.g. subject_category turns
    "object" once the subject lands), so an early pick can violate a rule it
    passed at selection time. Without this pass such picks are only dropped at
    render (render_suppressed_slots), losing the slot entirely.
    """
    if generation_contract is None:
        return
    forced_slots = set(generation_contract.get("forced_slots", []))
    soft_policy = generation_contract.get("soft_anchor_policy")
    for slot in list(picked.keys()):
        entry = picked[slot]
        protected = slot in forced_slots or (
            soft_anchor_critical_slot(soft_policy, slot)
            and str(entry.get("id", "")) in soft_anchor_pool_for_slot(soft_policy, slot, critical_only=True)
        )
        if protected:
            continue
        slot_reason = slot_block_reason(data, slot, generation_contract)
        entry_reason = None if slot_reason else entry_block_reason(entry, slot, generation_contract)
        if not slot_reason and not entry_reason:
            continue
        replacement = None
        if entry_reason:  # slot-level reasons make the whole slot inapplicable
            remaining = {key: value for key, value in picked.items() if key != slot}
            replacement = choose_slot(
                slot, data, preset, rng, remaining, forced_choices, semantic_context, generation_contract
            )
            if replacement is not None and entry_block_reason(replacement, slot, generation_contract):
                replacement = None
        if replacement is not None:
            picked[slot] = replacement
        else:
            picked.pop(slot, None)
        record_generation_contract_event(
            generation_contract,
            "reselect_events",
            {
                "slot": slot,
                "id": entry.get("id"),
                "reason": slot_reason or entry_reason,
                "status": "contract_reselected" if replacement is not None else "contract_dropped",
                "replacement": (replacement or {}).get("id"),
            },
        )
        refresh_generation_contract(generation_contract, data, preset, picked, forced_choices)


def render_guarded_picked(
    data: JsonDict,
    preset: JsonDict,
    picked: Dict[str, Entry],
    generation_contract: Optional[JsonDict] = None,
) -> Dict[str, Entry]:
    if generation_contract is None:
        return picked
    visible: Dict[str, Entry] = {}
    forced_slots = set(generation_contract.get("forced_slots", []))
    soft_policy = generation_contract.get("soft_anchor_policy")
    for slot, entry in picked.items():
        protected = slot in forced_slots or (
            soft_anchor_critical_slot(soft_policy, slot)
            and str(entry.get("id", "")) in soft_anchor_pool_for_slot(soft_policy, slot, critical_only=True)
        )
        reason = slot_block_reason(data, slot, generation_contract, forced=protected)
        if not reason:
            reason = entry_block_reason(entry, slot, generation_contract, forced=protected)
        if reason:
            record_generation_contract_event(
                generation_contract,
                "render_suppressed_slots",
                {"slot": slot, "id": entry.get("id"), "reason": reason},
            )
            continue
        visible[slot] = entry
    return visible


def values_as_set(item: JsonDict, *keys: str) -> Set[str]:
    values: Set[str] = set()
    for key in keys:
        raw = item.get(key)
        if isinstance(raw, str):
            values.add(raw)
        elif isinstance(raw, list):
            values |= {str(x) for x in raw}
    return values


# -----------------------------------------------------------------------------
# Filtering and weighted choices
# -----------------------------------------------------------------------------

def apply_filter(pool: Sequence[Entry], flt: Optional[JsonDict]) -> List[Entry]:
    if not flt:
        return list(pool)

    out = list(pool)

    if flt.get("ids"):
        ids = set(flt["ids"])
        out = [x for x in out if x.get("id") in ids]

    if flt.get("tags_any"):
        tags_any = set(flt["tags_any"])
        out = [x for x in out if entry_tags(x) & tags_any]

    if flt.get("tags_all"):
        tags_all = set(flt["tags_all"])
        out = [x for x in out if tags_all.issubset(entry_tags(x))]

    if flt.get("kinds_any"):
        kinds_any = set(flt["kinds_any"])
        out = [x for x in out if entry_kinds(x) & kinds_any]

    if flt.get("kinds_all"):
        kinds_all = set(flt["kinds_all"])
        out = [x for x in out if kinds_all.issubset(entry_kinds(x))]

    if flt.get("exclude_tags"):
        exclude = set(flt["exclude_tags"])
        out = [x for x in out if not (entry_tags(x) & exclude)]

    if flt.get("exclude_kinds"):
        exclude_kinds = set(flt["exclude_kinds"])
        out = [x for x in out if not (entry_kinds(x) & exclude_kinds)]

    multipliers = flt.get("weight_multipliers")
    if isinstance(multipliers, dict):
        weighted: List[Entry] = []
        for entry in out:
            copied = dict(entry)
            raw_multiplier = multipliers.get(str(entry.get("id") or ""), 1.0)
            try:
                multiplier = float(raw_multiplier)
            except (TypeError, ValueError):
                multiplier = 1.0
            if multiplier <= 0:
                continue
            try:
                base_weight = float(entry.get("weight", 1.0))
            except (TypeError, ValueError):
                base_weight = 1.0
            copied["weight"] = base_weight * multiplier
            weighted.append(copied)
        out = weighted

    return out


def weighted_choice(pool: Sequence[Entry], rng: random.Random) -> Entry:
    if not pool:
        raise ValueError("weighted_choice() received an empty pool")

    weights = []
    for item in pool:
        w = item.get("weight", 1)
        try:
            w = float(w)
        except (TypeError, ValueError):
            w = 1.0
        weights.append(max(w, 0.0))

    if sum(weights) <= 0:
        return rng.choice(list(pool))
    return rng.choices(list(pool), weights=weights, k=1)[0]


def normalize_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(x) for x in value]
    return [str(value)]


def candidate_pack_float(value: Any, digits: int = 6) -> Optional[float]:
    if value is None:
        return None
    try:
        return round(float(value), digits)
    except (TypeError, ValueError):
        return None


def candidate_pack_candidate_id(scope: str, raw_id: str, slot: Optional[str] = None) -> str:
    if scope == "preset":
        return f"preset:{raw_id}"
    return f"slot:{slot}:{raw_id}"


def candidate_pack_slot_limit(slot: str) -> int:
    return CANDIDATE_PACK_CORE_SLOT_LIMIT if slot in CANDIDATE_PACK_CORE_SLOTS else CANDIDATE_PACK_SUPPORT_SLOT_LIMIT


def candidate_pack_normalized_probabilities(rows: Sequence[JsonDict]) -> List[float]:
    weights: List[float] = []
    for row in rows:
        value = candidate_pack_float(row.get("weight")) or 0.0
        weights.append(max(value, 0.0))
    total = sum(weights)
    if total <= 0 and rows:
        return [round(1.0 / len(rows), 6) for _ in rows]
    if total <= 0:
        return []
    return [round(weight / total, 6) for weight in weights]


def candidate_pack_preset_by_id(data: JsonDict, preset_id: str) -> Optional[JsonDict]:
    for preset in data.get("presets", []) or []:
        if str(preset.get("id")) == preset_id:
            return preset
    return materialize_virtual_preset(data, preset_id)


def candidate_pack_slot_entry_by_id(data: JsonDict, slot: str, entry_id: str) -> Optional[Entry]:
    for entry in data.get("slots", {}).get(slot, []) or []:
        if str(entry.get("id")) == entry_id:
            return entry
    return None


def candidate_pack_score_payload(row: JsonDict) -> JsonDict:
    score: JsonDict = {}
    excluded = {"id"}
    for key, value in row.items():
        if key in excluded:
            continue
        if isinstance(value, (str, int, float, bool)) or value is None:
            score[key] = value
        elif isinstance(value, list):
            score[key] = value[:12]
        elif isinstance(value, dict):
            score[key] = value
    return score


def candidate_pack_entry_blob(entry: JsonDict, extra: Sequence[str] = ()) -> str:
    values: List[str] = [str(item) for item in extra if str(item).strip()]
    for key in (
        "id",
        "en",
        "ko",
        "family",
        "category",
        "description",
        "embedding_text",
        "aliases",
        "keywords",
        "tags",
        "kind",
        "facets",
    ):
        raw = entry.get(key)
        if isinstance(raw, list):
            values.extend(str(item) for item in raw)
        elif raw is not None:
            values.append(str(raw))
    return " ".join(values).lower()


def candidate_pack_rule_context_score(entry: JsonDict, request_text: str, context_tokens: Set[str]) -> int:
    """Rank sampler-eligible rule alternatives by request and scene relevance.

    The selected sampler result is still pinned first. This score only orders
    the remaining exact eligible pool so the bounded candidate pack exposes
    useful alternatives instead of whichever generic entries have the highest
    global weights.
    """
    compatibility_tokens = {
        str(token).lower()
        for key in (
            "for_any",
            "for_all",
            "requires_any_tags",
            "requires_primary_any_tags",
            "required_context_any",
        )
        for token in normalize_list(entry.get(key))
        if str(token).strip()
    }
    entry_tokens = {str(token).lower() for token in entry_context_tokens(entry)} | compatibility_tokens
    normalized_context = {str(token).lower() for token in context_tokens if str(token).strip()}
    context_hits = len(entry_tokens & normalized_context)

    blob = candidate_pack_entry_blob(entry, sorted(compatibility_tokens))
    request_hits = 0
    for term in candidate_pack_tokenize_intent_text(request_text):
        normalized = str(term).lower().strip()
        if len(normalized) < 2:
            continue
        if normalized in blob:
            request_hits += 1
    return context_hits * 3 + request_hits


def candidate_pack_summarize_preset_candidate(
    data: JsonDict,
    row: JsonDict,
    probability: float,
    selected_id: str,
) -> tuple[JsonDict, JsonDict]:
    raw_id = str(row.get("id") or selected_id or "")
    preset = candidate_pack_preset_by_id(data, raw_id) or {"id": raw_id}
    candidate = {
        "id": candidate_pack_candidate_id("preset", raw_id),
        "preset_id": raw_id,
        "label_en": localize(preset, "en") or raw_id,
        "label_ko": localize(preset, "ko") or raw_id,
        "family": preset.get("family"),
        "facets": {
            str(key): normalize_list(value)[:12]
            for key, value in (preset.get("facets") or {}).items()
            if str(key).strip() and normalize_list(value)
        },
        "probability": probability,
        "weight": candidate_pack_float(row.get("weight")),
        "selected_by_sampler": raw_id == selected_id,
        "scores": candidate_pack_score_payload(row),
        "conflicts_with": [],
    }
    return candidate, preset


def candidate_pack_summarize_slot_candidate(
    data: JsonDict,
    slot: str,
    row: JsonDict,
    probability: float,
    selected_id: str,
) -> tuple[JsonDict, Entry]:
    raw_id = str(row.get("id") or selected_id or "")
    entry = candidate_pack_slot_entry_by_id(data, slot, raw_id) or {"id": raw_id}
    candidate = {
        "id": candidate_pack_candidate_id("slot", raw_id, slot),
        "slot": slot,
        "entry_id": raw_id,
        "label_en": localize(entry, "en") or raw_id,
        "label_ko": localize(entry, "ko") or raw_id,
        "probability": probability,
        "weight": candidate_pack_float(row.get("weight")),
        "selected_by_sampler": raw_id == selected_id,
        "tags": normalize_list(entry.get("tags"))[:12],
        "kind": normalize_list(entry.get("kind"))[:8],
        "facets": {
            str(key): normalize_list(value)[:12]
            for key, value in (entry.get("facets") or {}).items()
            if str(key).strip() and normalize_list(value)
        },
        "scores": candidate_pack_score_payload(row),
        "applicability": {
            "status": str(row.get("applicability_status") or "eligible"),
            "source": str(row.get("applicability_source") or "sampler_eligible_pool"),
            "reason": row.get("applicability_reason"),
        },
        "conflicts_with": [],
    }
    return candidate, entry


def candidate_pack_rows_with_selected(rows: Sequence[JsonDict], selected_id: str, limit: int) -> List[JsonDict]:
    selected_id = str(selected_id or "")
    normalized = [dict(row) for row in rows if isinstance(row, dict) and row.get("id")]
    if selected_id and selected_id not in {str(row.get("id")) for row in normalized}:
        selected_row = {"id": selected_id, "weight": 0.0, "selected_fallback": True}
        if len(normalized) >= limit:
            normalized = normalized[: max(0, limit - 1)] + [selected_row]
        else:
            normalized.append(selected_row)
    return normalized[:limit]


def candidate_pack_build_presets(
    data: JsonDict,
    trace: JsonDict,
    result: JsonDict,
    candidate_entries: Dict[str, tuple[str, Optional[str], JsonDict]],
) -> List[JsonDict]:
    preset_score = trace.get("preset_score") if isinstance(trace.get("preset_score"), dict) else {}
    selected_id = str(preset_score.get("selected") or result.get("preset_id") or "")
    rows = candidate_pack_rows_with_selected(preset_score.get("top") or [], selected_id, CANDIDATE_PACK_PRESET_LIMIT)
    probabilities = candidate_pack_normalized_probabilities(rows)
    presets: List[JsonDict] = []
    for row, probability in zip(rows, probabilities):
        candidate, preset = candidate_pack_summarize_preset_candidate(data, row, probability, selected_id)
        presets.append(candidate)
        candidate_entries[candidate["id"]] = ("preset", None, preset)
    return presets


def candidate_pack_build_slots(
    data: JsonDict,
    trace: JsonDict,
    result: JsonDict,
    candidate_entries: Dict[str, tuple[str, Optional[str], JsonDict]],
) -> JsonDict:
    slots: JsonDict = {}
    choices = result.get("choices") if isinstance(result.get("choices"), dict) else {}
    contract = trace.get("generation_contract") if isinstance(trace.get("generation_contract"), dict) else {}
    pool_trace = contract.get("candidate_pool_trace") if isinstance(contract.get("candidate_pool_trace"), dict) else {}
    total = 0
    score_rows = [row for row in trace.get("slot_scores") or [] if isinstance(row, dict)]
    for score_index, score_row in enumerate(score_rows):
        if not isinstance(score_row, dict):
            continue
        slot = str(score_row.get("slot") or "")
        if not slot:
            continue
        limit = candidate_pack_slot_limit(slot)
        selected_id = str(score_row.get("selected") or ((choices.get(slot) or {}).get("id") if isinstance(choices.get(slot), dict) else "") or "")
        future_selected_count = sum(
            1
            for future in score_rows[score_index + 1 :]
            if str(future.get("selected") or "").strip()
        )
        available = max(
            1 if selected_id else 0,
            CANDIDATE_PACK_TOTAL_CANDIDATE_LIMIT - total - future_selected_count,
        )
        eligible_record = pool_trace.get(slot) if isinstance(pool_trace.get(slot), dict) else {}
        eligible_ids = [str(item) for item in eligible_record.get("eligible_ids") or [] if str(item).strip()]
        eligible_weights = eligible_record.get("weights") if isinstance(eligible_record.get("weights"), dict) else {}
        if eligible_ids:
            eligible_set = set(eligible_ids)
            scored_by_id = {
                str(row.get("id")): dict(row)
                for row in score_row.get("top") or []
                if isinstance(row, dict) and str(row.get("id") or "") in eligible_set
            }
            ordered_ids = [
                str(row.get("id"))
                for row in score_row.get("top") or []
                if isinstance(row, dict) and str(row.get("id") or "") in eligible_set
            ]
            ordered_ids.extend(item_id for item_id in eligible_ids if item_id not in set(ordered_ids))
            exact_rows: List[JsonDict] = []
            for item_id in ordered_ids:
                row = dict(scored_by_id.get(item_id, {}))
                row["id"] = item_id
                if item_id in eligible_weights:
                    row["weight"] = eligible_weights[item_id]
                row["applicability_status"] = "eligible"
                row["applicability_source"] = "sampler_eligible_pool"
                exact_rows.append(row)
            source_rows = exact_rows
        else:
            source_rows = [
                {**dict(row), "applicability_source": "legacy_score_trace"}
                for row in score_row.get("top") or []
                if isinstance(row, dict)
            ]
        rows = candidate_pack_rows_with_selected(source_rows, selected_id, min(limit, available))
        if not rows:
            continue
        probabilities = candidate_pack_normalized_probabilities(rows)
        candidates: List[JsonDict] = []
        for row, probability in zip(rows, probabilities):
            candidate, entry = candidate_pack_summarize_slot_candidate(data, slot, row, probability, selected_id)
            candidates.append(candidate)
            candidate_entries[candidate["id"]] = ("slot", slot, entry)
        slots[slot] = {
            "slot": slot,
            "role": "core" if slot in CANDIDATE_PACK_CORE_SLOTS else "support",
            "selected": candidate_pack_candidate_id("slot", selected_id, slot) if selected_id else None,
            "candidates": candidates,
            "candidate_count": score_row.get("candidate_count", len(rows)),
            "candidate_limit": score_row.get("candidate_limit", limit),
            "weight_floor": score_row.get("weight_floor"),
            "score_window": score_row.get("score_window"),
            "selected_filter": score_row.get("selected_filter"),
        }
        total += len(candidates)
        if total >= CANDIDATE_PACK_TOTAL_CANDIDATE_LIMIT and score_index + 1 >= len(score_rows):
            break

    if slots or not choices:
        return slots

    # Rule mode has no semantic score trace. Reuse the exact eligible pool
    # captured by choose_slot instead of rebuilding a weaker approximation
    # from preset filters. This keeps no-people, applicability, context, and
    # hard-conflict guards identical between sampling and candidate exposure.
    preset = candidate_pack_preset_by_id(data, str(result.get("preset_id") or "")) or {}
    filters = preset.get("filters") if isinstance(preset.get("filters"), dict) else {}
    provenance = result.get("provenance") if isinstance(result.get("provenance"), dict) else {}
    pack_request_text = " ".join(
        [
            str(trace.get("intent") or ""),
            *normalize_list(provenance.get("concept_lock")),
            *normalize_list(provenance.get("user_mandatory_intents")),
        ]
    ).lower()
    choice_items = [(slot, choice) for slot, choice in choices.items() if isinstance(choice, dict)]
    for choice_index, (slot, choice) in enumerate(choice_items):
        if not isinstance(choice, dict):
            continue
        raw_id = str(choice.get("id") or "")
        if not raw_id:
            continue
        eligible_record = pool_trace.get(str(slot)) if isinstance(pool_trace.get(str(slot)), dict) else {}
        eligible_ids = [str(item) for item in eligible_record.get("eligible_ids") or [] if str(item).strip()]
        eligible_weights = eligible_record.get("weights") if isinstance(eligible_record.get("weights"), dict) else {}
        if eligible_ids:
            by_id = {
                str(entry.get("id") or ""): entry
                for entry in data.get("slots", {}).get(str(slot), []) or []
                if isinstance(entry, dict) and str(entry.get("id") or "")
            }
            pool = [by_id[item_id] for item_id in eligible_ids if item_id in by_id]
        else:
            # Compatibility fallback for older/synthetic result objects.
            pool = apply_filter(data.get("slots", {}).get(str(slot), []) or [], filters.get(str(slot)))
        if not any(str(entry.get("id") or "") == raw_id for entry in pool):
            selected_entry = candidate_pack_slot_entry_by_id(data, str(slot), raw_id)
            if selected_entry:
                pool = [selected_entry, *pool]
        core_context_tokens = picked_core_context_tokens(
            {key: value for key, value in choices.items() if isinstance(value, dict) and key != str(slot)}
        )
        ranked = sorted(
            pool,
            key=lambda entry: (
                0 if str(entry.get("id") or "") == raw_id else 1,
                -candidate_pack_rule_context_score(entry, pack_request_text, core_context_tokens),
                -float(eligible_weights.get(str(entry.get("id") or ""), entry.get("weight", 1)) or 0)
                * (1.0 if eligible_ids else selection_balance_multiplier(data, entry, pack_request_text)[0]),
                str(entry.get("id") or ""),
            ),
        )
        limit = candidate_pack_slot_limit(str(slot))
        future_selected_count = sum(
            1
            for _future_slot, future_choice in choice_items[choice_index + 1 :]
            if str(future_choice.get("id") or "").strip()
        )
        remaining = max(
            1,
            CANDIDATE_PACK_TOTAL_CANDIDATE_LIMIT - total - future_selected_count,
        )
        rows = [
            {
                "id": str(entry.get("id") or ""),
                "weight": float(eligible_weights.get(str(entry.get("id") or ""), entry.get("weight", 1.0)) or 1.0)
                * (1.0 if eligible_ids else selection_balance_multiplier(data, entry, pack_request_text)[0]),
                "rule_selected": str(entry.get("id") or "") == raw_id,
                "rule_context_score": candidate_pack_rule_context_score(
                    entry, pack_request_text, core_context_tokens
                ),
                "applicability_status": "eligible",
                "applicability_source": "sampler_eligible_pool" if eligible_ids else "legacy_filter_fallback",
            }
            for entry in ranked[: min(limit, remaining)]
            if str(entry.get("id") or "")
        ]
        rows = candidate_pack_rows_with_selected(rows, raw_id, min(limit, remaining))
        probabilities = candidate_pack_normalized_probabilities(rows)
        candidates: List[JsonDict] = []
        for row, probability in zip(rows, probabilities):
            candidate, entry = candidate_pack_summarize_slot_candidate(
                data, str(slot), row, probability, raw_id
            )
            candidates.append(candidate)
            candidate_entries[candidate["id"]] = ("slot", str(slot), entry)
        slots[str(slot)] = {
            "slot": str(slot),
            "role": "core" if str(slot) in CANDIDATE_PACK_CORE_SLOTS else "support",
            "selected": candidate_pack_candidate_id("slot", raw_id, str(slot)),
            "candidates": candidates,
            "candidate_count": len(pool),
            "candidate_limit": min(limit, remaining),
            "weight_floor": None,
            "score_window": None,
            "selected_filter": "rule",
        }
        total += len(candidates)
    return slots


def candidate_pack_conflicts(
    data: JsonDict,
    candidate_entries: Dict[str, tuple[str, Optional[str], JsonDict]],
    limit: int = 100,
) -> List[JsonDict]:
    slot_items = [
        (candidate_id, slot, entry)
        for candidate_id, (scope, slot, entry) in candidate_entries.items()
        if scope == "slot" and slot
    ]
    conflicts: List[JsonDict] = []
    seen: Set[tuple[str, str, str]] = set()
    for rule in slot_conflict_rules_from_source(data):
        if str(rule.get("severity", "hard")) != "hard":
            continue
        left = rule.get("left") or {}
        right = rule.get("right") or {}
        left_matches = [
            (candidate_id, slot, entry)
            for candidate_id, slot, entry in slot_items
            if conflict_side_matches(left, slot or "", entry)
        ]
        right_matches = [
            (candidate_id, slot, entry)
            for candidate_id, slot, entry in slot_items
            if conflict_side_matches(right, slot or "", entry)
        ]
        for left_id, left_slot, _left_entry in left_matches:
            for right_id, right_slot, _right_entry in right_matches:
                if left_id == right_id:
                    continue
                key = (str(rule.get("id") or ""), *sorted([left_id, right_id]))
                if key in seen:
                    continue
                seen.add(key)
                conflicts.append(
                    {
                        "id": f"conflict:{stable_text_id('|'.join(key), 12)}",
                        "rule_id": str(rule.get("id") or ""),
                        "severity": "hard",
                        "candidates": [left_id, right_id],
                        "slots": [left_slot, right_slot],
                        "reason": str(rule.get("reason") or rule.get("description") or ""),
                    }
                )
                if len(conflicts) >= limit:
                    return conflicts
    return conflicts


def candidate_pack_apply_conflicts(slots: JsonDict, conflicts: Sequence[JsonDict]) -> None:
    by_id: Dict[str, JsonDict] = {}
    for slot_payload in slots.values():
        if not isinstance(slot_payload, dict):
            continue
        for candidate in slot_payload.get("candidates") or []:
            if isinstance(candidate, dict):
                by_id[str(candidate.get("id"))] = candidate
    for conflict in conflicts:
        ids = [str(item) for item in conflict.get("candidates", [])]
        for candidate_id in ids:
            candidate = by_id.get(candidate_id)
            if candidate is None:
                continue
            for other_id in ids:
                if other_id != candidate_id and other_id not in candidate["conflicts_with"]:
                    candidate["conflicts_with"].append(other_id)


def candidate_pack_apply_conflicts_to_candidates(
    candidates: Sequence[JsonDict],
    conflicts: Sequence[JsonDict],
) -> None:
    by_id = {
        str(candidate.get("id")): candidate
        for candidate in candidates
        if isinstance(candidate, dict) and str(candidate.get("id") or "")
    }
    for conflict in conflicts:
        ids = [str(item) for item in conflict.get("candidates", [])]
        for candidate_id in ids:
            candidate = by_id.get(candidate_id)
            if candidate is None:
                continue
            candidate.setdefault("conflicts_with", [])
            for other_id in ids:
                if other_id != candidate_id and other_id not in candidate["conflicts_with"]:
                    candidate["conflicts_with"].append(other_id)


def candidate_pack_source_texts(result: JsonDict, trace: JsonDict) -> List[tuple[str, str]]:
    texts: List[tuple[str, str]] = []
    seen_texts: Set[str] = set()
    provenance = result.get("provenance") if isinstance(result.get("provenance"), dict) else {}
    for concept in normalize_list(provenance.get("concept_lock")):
        if concept.strip() and concept.strip().lower() not in seen_texts:
            texts.append(("concept_lock", concept.strip()))
            seen_texts.add(concept.strip().lower())
    for requirement in normalize_list(provenance.get("user_mandatory_intents")):
        if requirement.strip() and requirement.strip().lower() not in seen_texts:
            texts.append(("user_requirement", requirement.strip()))
            seen_texts.add(requirement.strip().lower())
    for requirement in normalize_list(provenance.get("additional_requirements")):
        if requirement.strip() and requirement.strip().lower() not in seen_texts:
            texts.append(("additional_requirement", requirement.strip()))
            seen_texts.add(requirement.strip().lower())
    intent = str(trace.get("intent") or "").strip()
    if intent and trace.get("intent_source") == "user" and intent.lower() not in seen_texts:
        texts.append(("intent", intent))
    return texts


def candidate_pack_tokenize_intent_text(text: str) -> List[str]:
    # Keep negative-presence phrases atomic. Splitting ``사람 없는`` into a
    # positive ``사람`` token used to activate the human axis and invert the
    # user's request.
    negative_phrases = re.findall(
        r"(?:사람|인물|인간)\s*(?:이\s*)?(?:없는|없이)|(?:no|without)\s+(?:(?:a|any)\s+)?(?:people|person|persons|humans?)",
        text,
        flags=re.IGNORECASE,
    )
    masked = text
    for phrase in negative_phrases:
        masked = masked.replace(phrase, " ")
    tokens = re.findall(r"[A-Za-z0-9][A-Za-z0-9_+-]*|[가-힣]+", text)
    if negative_phrases:
        tokens = re.findall(r"[A-Za-z0-9][A-Za-z0-9_+-]*|[가-힣]+", masked)
    normalized: List[str] = [clean_spaces(phrase) for phrase in negative_phrases]
    for token in tokens:
        key = token.lower()
        if key in CANDIDATE_PACK_INTENT_STOPWORDS:
            continue
        if len(token) <= 1 and not token.isascii():
            continue
        normalized.append(token)
    return normalized or ([text.strip()] if text.strip() else [])


def intent_explicitly_excludes_people(text: str) -> bool:
    return bool(
        re.search(
            r"(?:사람|인물|인간)\s*(?:이\s*)?(?:없는|없이)|(?:no|without)\s+(?:(?:a|any)\s+)?(?:people|person|persons|humans?)",
            str(text or ""),
            flags=re.IGNORECASE,
        )
    )


def generation_explicitly_excludes_people(
    semantic_context: Optional[JsonDict],
    generation_contract: Optional[JsonDict],
) -> bool:
    values = [str((semantic_context or {}).get("intent") or "")]
    values.extend(normalize_list((generation_contract or {}).get("user_mandatory_intents")))
    values.extend(normalize_list((generation_contract or {}).get("concept_locks")))
    values.extend(normalize_list((generation_contract or {}).get("additional_requirements")))
    return any(intent_explicitly_excludes_people(value) for value in values)


def candidate_pack_intent_routing_policy(data: JsonDict) -> JsonDict:
    layers = data.get(QUALITY_LAYERS_DATA_KEY) if isinstance(data.get(QUALITY_LAYERS_DATA_KEY), dict) else {}
    policy = layers.get("intent_routing") if isinstance(layers.get("intent_routing"), dict) else {}
    return policy


def intent_alias_matches(text: str, alias: str) -> bool:
    normalized_text = clean_spaces(
        re.sub(r"[-\u2013\u2014/]+", " ", str(text or "").lower().replace("_", " "))
    )
    normalized_alias = clean_spaces(
        re.sub(r"[-\u2013\u2014/]+", " ", str(alias or "").lower().replace("_", " "))
    )
    if not normalized_text or not normalized_alias:
        return False
    if normalized_alias.isascii() and re.search(r"[a-z0-9]", normalized_alias):
        plural_suffix = ""
        final_word = normalized_alias.rsplit(" ", 1)[-1]
        if final_word.isalpha() and not final_word.endswith("s"):
            plural_suffix = r"(?:s|es)?"
        negated = (
            r"(?<![a-z0-9])(?:no|not|without)\s+(?:(?:a|any)\s+)?"
            + re.escape(normalized_alias)
            + plural_suffix
            + r"(?![a-z0-9])"
        )
        if re.search(negated, normalized_text):
            return False
        pattern = (
            r"(?<![a-z0-9])"
            + re.escape(normalized_alias)
            + plural_suffix
            + r"(?![a-z0-9])"
        )
        return re.search(pattern, normalized_text) is not None
    return normalized_alias in normalized_text


def resolve_request_intent_constraints(
    data: JsonDict,
    semantic_context: Optional[JsonDict],
    generation_contract: Optional[JsonDict],
) -> JsonDict:
    values = [str((semantic_context or {}).get("intent") or "")]
    for key in ("concept_locks", "user_mandatory_intents", "additional_requirements"):
        values.extend(normalize_list((generation_contract or {}).get(key)))
    texts: List[str] = []
    seen_texts: Set[str] = set()
    for value in values:
        normalized = clean_spaces(value)
        dedupe_key = normalized.lower()
        if normalized and dedupe_key not in seen_texts:
            texts.append(normalized)
            seen_texts.add(dedupe_key)
    policy = candidate_pack_intent_routing_policy(data)
    categories: Set[str] = set()
    domains: Set[str] = set()
    matched: List[JsonDict] = []
    for rule in policy.get("subject_categories") or []:
        if not isinstance(rule, dict):
            continue
        category = str(rule.get("category") or "")
        aliases = normalize_list(rule.get("aliases"))
        hits = sorted({alias for text in texts for alias in aliases if intent_alias_matches(text, alias)})
        if category in VALID_SUBJECT_CATEGORIES and hits:
            categories.add(category)
            matched.append({"axis": "subject_category", "value": category, "aliases": hits[:8]})
    for rule in policy.get("domains") or []:
        if not isinstance(rule, dict):
            continue
        domain = str(rule.get("domain") or "")
        aliases = normalize_list(rule.get("aliases"))
        hits = sorted({alias for text in texts for alias in aliases if intent_alias_matches(text, alias)})
        if domain in VALID_PRESET_DOMAINS and hits:
            domains.add(domain)
            matched.append({"axis": "domain", "value": domain, "aliases": hits[:8]})
    catalog_presets = {
        str(preset.get("id"))
        for preset in data.get("presets", [])
        if isinstance(preset, dict) and str(preset.get("id") or "")
    }
    scoped_routes: Set[str] = set()
    for rule in policy.get("scoped_routes") or []:
        if not isinstance(rule, dict):
            continue
        domain = str(rule.get("domain") or "")
        preset_id = str(rule.get("preset_id") or "")
        if domain not in domains or preset_id not in catalog_presets:
            continue
        aliases = normalize_list(rule.get("aliases"))
        hits = sorted({alias for text in texts for alias in aliases if intent_alias_matches(text, alias)})
        if hits:
            scoped_routes.add(preset_id)
            matched.append(
                {
                    "axis": "scoped_route",
                    "value": preset_id,
                    "domain": domain,
                    "aliases": hits[:8],
                }
            )
    no_people = any(intent_explicitly_excludes_people(text) for text in texts)
    if no_people:
        categories.discard("human")
        matched = [
            row
            for row in matched
            if not (row.get("axis") == "subject_category" and row.get("value") == "human")
        ]
    return {
        "no_people": no_people,
        "subject_categories": sorted(categories),
        "domains": sorted(domains),
        "scoped_routes": sorted(scoped_routes),
        "matched": matched,
        "source_text_count": len(texts),
    }


def candidate_pack_intent_contract(
    data: JsonDict,
    result: JsonDict,
    trace: JsonDict,
    candidate_blobs: Dict[str, str],
) -> List[JsonDict]:
    rows: List[JsonDict] = []
    seen: Set[tuple[str, str]] = set()
    policy = candidate_pack_intent_routing_policy(data)
    for source, source_text in candidate_pack_source_texts(result, trace):
        key = (source, source_text.lower())
        if key in seen:
            continue
        seen.add(key)
        no_people = intent_explicitly_excludes_people(source_text)
        facets: List[str] = []
        for axis, name_key, value_key in (
            ("subject_category", "subject_categories", "category"),
            ("domain", "domains", "domain"),
        ):
            for rule in policy.get(name_key) or []:
                if not isinstance(rule, dict):
                    continue
                value = str(rule.get(value_key) or "")
                if no_people and axis == "subject_category" and value == "human":
                    continue
                if value and any(intent_alias_matches(source_text, alias) for alias in normalize_list(rule.get("aliases"))):
                    facets.append(f"{axis}:{value}")
        meaningful_terms = candidate_pack_tokenize_intent_text(source_text)
        covered_by = [
            candidate_id
            for candidate_id, blob in candidate_blobs.items()
            if any(str(term).lower() in blob for term in meaningful_terms)
        ][:12]
        rows.append(
            {
                "id": f"intent:{stable_text_id(f'{source}|{source_text}', 12)}",
                "text": source_text,
                "source": source,
                "polarity": "excluded" if no_people else "required",
                "priority": "critical",
                "axis_hints": sorted(set(facets)),
                "constraints": ["no_people"] if no_people else [],
                "coverage_mode": "literal_or_asserted_translation",
                "status": "covered" if covered_by else "uncovered",
                "covered_by": covered_by,
            }
        )
    return rows


def candidate_pack_candidate_blobs(presets: Sequence[JsonDict], slots: JsonDict) -> Dict[str, str]:
    blobs: Dict[str, str] = {}
    for preset in presets:
        candidate_id = str(preset.get("id"))
        blobs[candidate_id] = candidate_pack_entry_blob(
            preset,
            [
                str(preset.get("preset_id") or ""),
                str(preset.get("label_en") or ""),
                str(preset.get("label_ko") or ""),
                str(preset.get("family") or ""),
            ],
        )
    for slot_payload in slots.values():
        if not isinstance(slot_payload, dict):
            continue
        for candidate in slot_payload.get("candidates") or []:
            if not isinstance(candidate, dict):
                continue
            candidate_id = str(candidate.get("id"))
            blobs[candidate_id] = candidate_pack_entry_blob(
                candidate,
                [
                    str(candidate.get("entry_id") or ""),
                    str(candidate.get("slot") or ""),
                    str(candidate.get("label_en") or ""),
                    str(candidate.get("label_ko") or ""),
                ],
            )
    return blobs


def candidate_pack_candidate_terms(presets: Sequence[JsonDict], slots: JsonDict) -> Dict[str, List[str]]:
    terms: Dict[str, List[str]] = {}
    for preset in presets:
        candidate_id = str(preset.get("id"))
        terms[candidate_id] = [
            str(preset.get("preset_id") or ""),
            str(preset.get("label_en") or ""),
            str(preset.get("label_ko") or ""),
            str(preset.get("family") or ""),
        ]
    for slot_payload in slots.values():
        if not isinstance(slot_payload, dict):
            continue
        for candidate in slot_payload.get("candidates") or []:
            if not isinstance(candidate, dict):
                continue
            candidate_id = str(candidate.get("id"))
            terms[candidate_id] = [
                str(candidate.get("entry_id") or ""),
                str(candidate.get("label_en") or ""),
                str(candidate.get("label_ko") or ""),
            ]
    return {
        candidate_id: list(dict.fromkeys(term for term in values if term.strip()))[:12]
        for candidate_id, values in terms.items()
    }


def candidate_pack_mandatory_intents(
    result: JsonDict,
    trace: JsonDict,
    candidate_blobs: Dict[str, str],
    candidate_terms: Dict[str, List[str]],
) -> tuple[List[JsonDict], List[JsonDict]]:
    intents: List[JsonDict] = []
    seen: Set[tuple[str, str]] = set()
    for source, source_text in candidate_pack_source_texts(result, trace):
        for token in candidate_pack_tokenize_intent_text(source_text):
            dedupe_key = (source, token.lower())
            if dedupe_key in seen:
                continue
            seen.add(dedupe_key)
            token_lower = token.lower()
            covered_by = [
                candidate_id
                for candidate_id, blob in candidate_blobs.items()
                if token_lower in blob
            ][:12]
            # Audit terms are literal user intent only. Candidate labels are
            # discovery metadata, not proof that the composed text preserved
            # the request.
            audit_terms = [token]
            intents.append(
                {
                    "text": token,
                    "source": source,
                    "source_text": source_text,
                    "status": "covered" if covered_by else "uncovered",
                    "covered_by": covered_by,
                    "audit_terms": list(dict.fromkeys(term for term in audit_terms if str(term).strip()))[:12],
                }
            )
    uncovered = [intent for intent in intents if intent.get("status") == "uncovered"]
    return intents, uncovered


def candidate_pack_diversity_state(trace: JsonDict) -> JsonDict:
    batch = trace.get("batch_diversity") if isinstance(trace.get("batch_diversity"), dict) else {}
    history = trace.get("batch_history_summary") if isinstance(trace.get("batch_history_summary"), dict) else {}
    ledger = trace.get("anchor_diversity_ledger_summary") if isinstance(trace.get("anchor_diversity_ledger_summary"), dict) else {}
    penalties = trace.get("batch_repetition_penalty") if isinstance(trace.get("batch_repetition_penalty"), list) else []
    return {
        "enabled": bool(batch.get("enabled")),
        "tracked_scopes": normalize_list(batch.get("tracked_scopes")),
        "novelty": batch.get("novelty"),
        "history": history,
        "anchor_ledger": ledger,
        "recent_penalties": penalties[-12:],
    }


def candidate_pack_creative_feature_tokens(entry: JsonDict) -> Set[str]:
    values: List[str] = []
    for key in ("en", "ko", "aliases", "keywords", "tags", "kind"):
        raw = entry.get(key)
        if isinstance(raw, list):
            values.extend(str(item) for item in raw)
        elif raw is not None:
            values.append(str(raw))
    tokens = {
        str(token).lower()
        for token in candidate_pack_tokenize_intent_text(
            " ".join(values).replace("_", " ").replace("-", " ")
        )
        if str(token).strip()
    }
    tokens.update(str(token).lower() for token in facet_tokens(entry))
    if not tokens and entry.get("id"):
        tokens.update(
            str(token).lower()
            for token in candidate_pack_tokenize_intent_text(str(entry["id"]).replace("_", " "))
        )
    return tokens


def candidate_pack_creative_feature_distance(left: JsonDict, right: JsonDict) -> tuple[float, int, int]:
    left_tokens = candidate_pack_creative_feature_tokens(left)
    right_tokens = candidate_pack_creative_feature_tokens(right)
    union = left_tokens | right_tokens
    shared = left_tokens & right_tokens
    if not union:
        return 0.0, 0, 0
    return round(1.0 - (len(shared) / len(union)), 6), len(shared), len(union)


def candidate_pack_creative_exploration(
    result: JsonDict,
    slots: JsonDict,
    candidate_entries: Dict[str, tuple[str, Optional[str], JsonDict]],
) -> Optional[JsonDict]:
    provenance = result.get("provenance") if isinstance(result.get("provenance"), dict) else {}
    creativity = candidate_pack_float(provenance.get("creativity"))
    if creativity is None or creativity < CANDIDATE_PACK_CREATIVE_EXPLORATION_FLOOR:
        return None

    selected_ids = {
        str(slot_payload.get("selected") or "")
        for slot_payload in slots.values()
        if isinstance(slot_payload, dict) and str(slot_payload.get("selected") or "")
    }
    contrast_rows: List[JsonDict] = []
    for slot in sorted(CANDIDATE_PACK_CREATIVE_EXPLORATION_SLOTS):
        slot_payload = slots.get(slot)
        if not isinstance(slot_payload, dict):
            continue
        selected_id = str(slot_payload.get("selected") or "")
        selected_record = candidate_entries.get(selected_id)
        if not selected_id or not selected_record or selected_record[0] != "slot":
            continue
        selected_entry = selected_record[2]
        alternatives: List[JsonDict] = []
        for rank, candidate in enumerate(slot_payload.get("candidates") or [], start=1):
            if not isinstance(candidate, dict) or candidate.get("selected_by_sampler"):
                continue
            candidate_id = str(candidate.get("id") or "")
            applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
            if (
                applicability.get("status") != "eligible"
                or applicability.get("source") != "sampler_eligible_pool"
            ):
                continue
            if set(normalize_list(candidate.get("conflicts_with"))) & (selected_ids - {selected_id}):
                continue
            entry_record = candidate_entries.get(candidate_id)
            if not entry_record or entry_record[0] != "slot":
                continue
            distance, shared_count, union_count = candidate_pack_creative_feature_distance(
                selected_entry, entry_record[2]
            )
            if distance < CANDIDATE_PACK_CREATIVE_EXPLORATION_MIN_DISTANCE:
                continue
            alternatives.append(
                {
                    "slot": slot,
                    "candidate_id": candidate_id,
                    "replaces_candidate_id": selected_id,
                    "feature_distance": distance,
                    "shared_feature_count": shared_count,
                    "feature_union_count": union_count,
                    "relevance_rank": rank,
                    "applicability_source": "sampler_eligible_pool",
                }
            )
        if alternatives:
            alternatives.sort(
                key=lambda row: (
                    -float(row["feature_distance"]),
                    int(row["relevance_rank"]),
                    str(row["candidate_id"]),
                )
            )
            contrast_rows.append(alternatives[0])

    contrast_rows.sort(
        key=lambda row: (
            -float(row["feature_distance"]),
            int(row["relevance_rank"]),
            str(row["slot"]),
            str(row["candidate_id"]),
        )
    )
    contrast_rows = contrast_rows[:CANDIDATE_PACK_CREATIVE_EXPLORATION_LIMIT]
    return {
        "enabled": True,
        "strategy": "relevance_anchored_contrast",
        "creativity": creativity,
        "activation_floor": CANDIDATE_PACK_CREATIVE_EXPLORATION_FLOOR,
        "minimum_feature_distance": CANDIDATE_PACK_CREATIVE_EXPLORATION_MIN_DISTANCE,
        "source": "exposed_sampler_eligible_pool",
        "contrast_candidate_count": len(contrast_rows),
        "contrast_candidates": contrast_rows,
        "composition_guidance": {
            "keep": ["sampler_selected_subject", "mandatory_intents", "scene_contract"],
            "replace_at_most": 2,
            "require_no_conflicts": True,
        },
    }


def candidate_pack_creative_direction(result: JsonDict) -> Optional[JsonDict]:
    """Expose an agent-level concept-development contract for explicit high-creativity runs.

    This contract deliberately contains no topic examples or resolved scene atoms. It changes
    how the agent develops and binds one idea; it does not enlarge or mutate the candidate pool.
    """
    provenance = result.get("provenance") if isinstance(result.get("provenance"), dict) else {}
    creativity = candidate_pack_float(provenance.get("creativity"))
    if creativity is None or creativity < CANDIDATE_PACK_CREATIVE_DIRECTION_FLOOR:
        return None

    operators = [
        {"id": operator_id, "definition": definition}
        for operator_id, definition in CANDIDATE_PACK_CREATIVE_DIRECTION_OPERATORS
    ]
    return {
        "enabled": True,
        "contract_version": "photo-creative-direction/v1",
        "source": "explicit_creativity_control",
        "creativity": creativity,
        "activation_floor": CANDIDATE_PACK_CREATIVE_DIRECTION_FLOOR,
        "purpose": "viewer_perceived_originality_ingenuity_and_authorial_intent",
        "ordinary_baseline": {
            "minimum_cliches": 3,
            "instruction": "Name the likely first-answer visual shortcuts before proposing alternatives.",
        },
        "proposal_contract": {
            "minimum_proposals": CANDIDATE_PACK_CREATIVE_DIRECTION_MIN_PROPOSALS,
            "select_exactly": 1,
            "distinct_operator_ids": True,
            "required_fields": [
                "id",
                "operator_id",
                "premise",
                "familiar_anchor",
                "viewer_expectation",
                "rule_break",
                "visible_consequences",
                "aboutness",
                "signature_phrase",
            ],
            "operators": operators,
        },
        "selected_concept_contract": {
            "required_fields": [
                "proposal_id",
                "familiar_anchor",
                "rule_break",
                "visible_consequences",
                "reveal_path",
                "aboutness",
                "authorial_grammar",
                "prompt_evidence",
            ],
            "rule_break_count": 1,
            "minimum_visible_consequences": 2,
            "minimum_reveal_steps": 3,
            "authorial_grammar_fields": ["vantage", "timing", "omission", "material_rule"],
        },
        "prompt_binding": {
            "literal": True,
            "selected_signature_required": True,
            "unselected_signatures_forbidden": True,
            "required_evidence_fields": [
                "familiar_anchor_phrase",
                "rule_break_phrase",
                "visible_consequence_phrases",
                "reveal_path_phrases",
                "authorial_grammar_phrases",
            ],
        },
        "composition_guidance": {
            "keep": [
                "sampler_selected_subject",
                "mandatory_intents",
                "scene_contract",
                "character_grammar",
                "safety_contract",
                "negative_en_bytes",
            ],
            "develop": [
                "familiar_anchor",
                "one_rule_break",
                "visible_consequence_chain",
                "viewer_reveal_path",
                "one_aboutness",
                "authorial_vantage_time_omission_material_rule",
            ],
            "reject": [
                "adjective_only_novelty",
                "unrelated_anomaly_stacking",
                "multiple_proposals_blended_into_one_frame",
                "named_artist_imitation_as_authorial_voice",
            ],
        },
        "artistic_final_touch_role": "surface_craft_only_not_authorial_evidence",
    }


def candidate_pack_viewer_experience(result: JsonDict) -> Optional[JsonDict]:
    """Expose a topic-neutral reader-response composition contract when requested.

    High creative-direction runs always receive this layer. Other commercial,
    subculture, affective, or audience-outcome requests opt in through the agent
    layer's explicit ``--viewer-experience`` control. The contract contains no
    topic candidates and does not claim that a composed prompt proves a human
    response.
    """
    provenance = result.get("provenance") if isinstance(result.get("provenance"), dict) else {}
    creativity = candidate_pack_float(provenance.get("creativity"))
    explicitly_requested = provenance.get("viewer_experience_requested") is True
    creative_direction_required = bool(
        creativity is not None and creativity >= CANDIDATE_PACK_CREATIVE_DIRECTION_FLOOR
    )
    if not explicitly_requested and not creative_direction_required:
        return None

    activation_sources = []
    if explicitly_requested:
        activation_sources.append("explicit_viewer_experience_control")
    if creative_direction_required:
        activation_sources.append("creative_direction_required")
    return {
        "enabled": True,
        "contract_version": "photo-viewer-experience/v1",
        "source": activation_sources[0],
        "activation_sources": activation_sources,
        "purpose": "viewer_response_hypothesis_with_visible_evidence_not_verified_human_outcome",
        "required_fields": [
            "target_audience",
            "viewing_context",
            "primary_viewer_need",
            "intended_experience",
            "viewer_promise",
            "first_glance_hook",
            "interpretive_question",
            "affect_evidence",
            "attachment_channel",
            "reinspection_reward",
            "commercial_objective",
            "prompt_evidence",
        ],
        "allowed_values": {
            "viewing_context": list(CANDIDATE_PACK_VIEWER_CONTEXTS),
            "audience_literacy": list(CANDIDATE_PACK_VIEWER_AUDIENCE_LITERACY),
            "primary_viewer_need": list(CANDIDATE_PACK_VIEWER_NEEDS),
            "attachment_channel": list(CANDIDATE_PACK_VIEWER_ATTACHMENT_CHANNELS),
            "reinspection_mode": list(CANDIDATE_PACK_VIEWER_REINSPECTION_MODES),
            "commercial_objective": list(CANDIDATE_PACK_VIEWER_COMMERCIAL_OBJECTIVES),
        },
        "target_audience_fields": ["literacy", "required_prior_knowledge"],
        "affect_evidence_fields": ["actor", "action", "target", "consequence"],
        "prompt_binding": {
            "literal": True,
            "required_evidence_fields": [
                "first_glance_hook_phrase",
                "affect_actor_phrase",
                "affect_action_phrase",
                "affect_target_phrase",
                "affect_consequence_phrase",
            ],
            "conditional_evidence_fields": {
                "attachment_channel_not_none": "attachment_phrase",
                "reinspection_mode_causal_second_reading": "reinspection_reward_phrase",
                "commercial_objective_comprehend_remember_act": "commercial_legibility_phrase",
            },
        },
        "conditional_rules": {
            "attachment_required_for_needs": ["care", "relatedness", "identity"],
            "commercial_legibility_required_for_objectives": ["comprehend", "remember", "act"],
            "creative_noncommercial_reinspection_required": True,
            "product_clarity_can_override_reinspection": True,
        },
        "composition_guidance": {
            "select_exactly_one": ["primary_viewer_need", "intended_experience", "commercial_objective"],
            "bind_visible_causes_not_outcome_claims": True,
            "keep": [
                "creative_direction",
                "scene_contract",
                "character_grammar",
                "product_or_subject_legibility",
                "safety_contract",
                "negative_en_bytes",
            ],
            "reject": [
                "affect_stacking",
                "viewer_will_feel_outcome_claim",
                "face_or_youth_morphology_as_attachment_evidence",
                "genre_term_or_style_adjective_as_experience_evidence",
                "commercial_attention_at_the_cost_of_product_clarity",
            ],
        },
        "evaluation_boundary": "prompt_binding_is_preflight;_metadata_free_pixels_are_local_product_evidence;human_response_requires_human_evaluation",
    }


def candidate_pack_hybrid_policy(data: JsonDict) -> JsonDict:
    layers = candidate_pack_quality_layers(data)
    policy = layers.get("hybrid_augmentation") if isinstance(layers.get("hybrid_augmentation"), dict) else {}
    return policy if policy.get("enabled", True) else {}


def candidate_pack_hybrid_activation_sources(
    result: JsonDict,
    adult_appeal: Optional[JsonDict],
) -> List[str]:
    provenance = result.get("provenance") if isinstance(result.get("provenance"), dict) else {}
    sources: List[str] = []
    if provenance.get("hybrid_augmentation_requested") is True:
        sources.append("explicit_hybrid_augmentation_control")
    creativity = candidate_pack_float(provenance.get("creativity"))
    if creativity is not None and creativity >= CANDIDATE_PACK_CREATIVE_DIRECTION_FLOOR:
        sources.append("creative_direction_required")
    if isinstance(adult_appeal, dict) and adult_appeal.get("enabled") is True:
        if adult_appeal.get("activation_source") == "skill_default":
            sources.append("configured_default_adult_appeal")
        else:
            sources.append("explicit_adult_appeal_control")
    return sources


def candidate_pack_adult_appeal_eligibility(
    data: JsonDict,
    result: JsonDict,
    activation_source: str,
) -> JsonDict:
    trace = result.get("semantic_trace") if isinstance(result.get("semantic_trace"), dict) else {}
    contract = trace.get("generation_contract") if isinstance(trace.get("generation_contract"), dict) else {}
    constraints = contract.get("intent_constraints") if isinstance(contract.get("intent_constraints"), dict) else {}
    subject_category_value = str(contract.get("subject_category") or "generic")
    hybrid_policy = candidate_pack_hybrid_policy(data)
    adult_policy = hybrid_policy.get("adult_appeal") if isinstance(hybrid_policy.get("adult_appeal"), dict) else {}
    default_eligibility = (
        adult_policy.get("default_eligibility")
        if isinstance(adult_policy.get("default_eligibility"), dict)
        else {}
    )
    if bool(default_eligibility.get("block_no_people", True)) and constraints.get("no_people") is True:
        return {
            "status": "ineligible",
            "reason": "explicit_no_people",
            "subject_category": subject_category_value,
        }
    allowed_default_categories = {
        str(item) for item in default_eligibility.get("subject_categories") or ["human"]
    }
    if activation_source == "skill_default" and subject_category_value not in allowed_default_categories:
        return {
            "status": "ineligible",
            "reason": "default_requires_eligible_human_subject",
            "subject_category": subject_category_value,
            "allowed_subject_categories": sorted(allowed_default_categories),
        }
    return {
        "status": "eligible",
        "reason": "eligible_human_default"
        if activation_source == "skill_default"
        else "explicit_control",
        "subject_category": subject_category_value,
    }


def candidate_pack_adult_appeal_request(data: JsonDict, result: JsonDict) -> JsonDict:
    provenance = result.get("provenance") if isinstance(result.get("provenance"), dict) else {}
    raw = provenance.get("adult_appeal") if isinstance(provenance.get("adult_appeal"), dict) else {}
    axes_raw = raw.get("axes") if isinstance(raw.get("axes"), dict) else {}
    axes: JsonDict = {}
    for axis_id in CANDIDATE_PACK_ADULT_APPEAL_AXES:
        axis = axes_raw.get(axis_id) if isinstance(axes_raw.get(axis_id), dict) else {}
        try:
            intensity = int(axis.get("intensity", 0) or 0)
        except (TypeError, ValueError):
            intensity = 0
        axes[axis_id] = {"intensity": max(0, min(3, intensity))}
    requested_enabled = any(axis["intensity"] > 0 for axis in axes.values())
    activation_source = str(raw.get("activation_source") or "skill_default")
    eligibility = candidate_pack_adult_appeal_eligibility(data, result, activation_source)
    enabled = requested_enabled and eligibility.get("status") == "eligible"
    emphasis = str((raw.get("blend") or {}).get("emphasis") or "") if isinstance(raw.get("blend"), dict) else ""
    if emphasis not in CANDIDATE_PACK_ADULT_APPEAL_EMPHASES:
        sensual = axes["sensual_editorial"]["intensity"]
        fetish = axes["fetish_fashion"]["intensity"]
        emphasis = "balanced" if sensual == fetish else ("sensual_led" if sensual > fetish else "fetish_led")
    return {
        "enabled": enabled,
        "requested_enabled": requested_enabled,
        "activation_source": activation_source if requested_enabled else "explicit_opt_out",
        "eligibility": eligibility,
        "axes": axes,
        "blend": {"emphasis": emphasis},
    }


def candidate_pack_filter_ids(preset: JsonDict, slot: str) -> List[str]:
    filters = preset.get("filters") if isinstance(preset.get("filters"), dict) else {}
    raw = filters.get(slot)
    if isinstance(raw, dict):
        return [str(item) for item in raw.get("ids") or [] if str(item).strip()]
    return [str(item) for item in normalize_list(raw) if str(item).strip()]


def candidate_pack_adult_risk_groups(entry_id: str, adult_policy: JsonDict) -> List[str]:
    groups: List[str] = []
    risk_groups = adult_policy.get("risk_groups") if isinstance(adult_policy.get("risk_groups"), dict) else {}
    for group_id, group in risk_groups.items():
        if not isinstance(group, dict):
            continue
        if entry_id in {str(item) for item in group.get("entry_ids") or []}:
            groups.append(str(group_id))
    return groups


def candidate_pack_hybrid_adult_appeal(
    data: JsonDict,
    result: JsonDict,
    candidate_entries: Dict[str, tuple[str, Optional[str], JsonDict]],
) -> Optional[JsonDict]:
    hybrid_policy = candidate_pack_hybrid_policy(data)
    adult_policy = hybrid_policy.get("adult_appeal") if isinstance(hybrid_policy.get("adult_appeal"), dict) else {}
    request = candidate_pack_adult_appeal_request(data, result)
    enabled = bool(request.get("enabled"))
    source_preset_id = str(adult_policy.get("source_preset_id") or "adult_fetish_fashion_editorial")
    source_preset = candidate_pack_preset_by_id(data, source_preset_id) or {}
    try:
        per_axis_limit = max(1, int(adult_policy.get("candidate_limit_per_axis", 12) or 12))
    except (TypeError, ValueError):
        per_axis_limit = 12
    try:
        per_carrier_limit = max(1, int(adult_policy.get("candidate_limit_per_carrier", 3) or 3))
    except (TypeError, ValueError):
        per_carrier_limit = 3

    configured_axes = adult_policy.get("axes") if isinstance(adult_policy.get("axes"), dict) else {}
    axes: JsonDict = {}
    for axis_id in CANDIDATE_PACK_ADULT_APPEAL_AXES:
        intensity = int(((request.get("axes") or {}).get(axis_id) or {}).get("intensity", 0) or 0)
        axis_policy = configured_axes.get(axis_id) if isinstance(configured_axes.get(axis_id), dict) else {}
        inventory: List[JsonDict] = []
        seen_sources: Set[str] = set()
        if enabled and intensity > 0:
            for carrier in axis_policy.get("carriers") or []:
                if not isinstance(carrier, dict) or len(inventory) >= per_axis_limit:
                    continue
                carrier_id = str(carrier.get("id") or "detail")
                required_tags = {str(item).lower() for item in carrier.get("required_tags_any") or []}
                try:
                    carrier_limit = max(1, int(carrier.get("candidate_limit", per_carrier_limit) or per_carrier_limit))
                except (TypeError, ValueError):
                    carrier_limit = per_carrier_limit
                carrier_count = 0
                for slot in [str(item) for item in carrier.get("slots") or [] if str(item).strip()]:
                    for entry_id in candidate_pack_filter_ids(source_preset, slot):
                        if carrier_count >= carrier_limit or len(inventory) >= per_axis_limit:
                            break
                        source_key = f"{slot}:{entry_id}"
                        if source_key in seen_sources:
                            continue
                        entry = candidate_pack_slot_entry_by_id(data, slot, entry_id)
                        if not isinstance(entry, dict):
                            continue
                        try:
                            minimum_intensity = int(
                                (adult_policy.get("entry_min_intensity") or {}).get(entry_id, 1)
                            )
                        except (TypeError, ValueError):
                            minimum_intensity = 1
                        if intensity < minimum_intensity:
                            continue
                        tags = {str(item).lower() for item in entry.get("tags") or []}
                        if required_tags and not (required_tags & tags):
                            continue
                        candidate_id = f"augmentation:adult_appeal:{axis_id}:{slot}:{entry_id}"
                        candidate = {
                            "id": candidate_id,
                            "source_candidate_id": candidate_pack_candidate_id("slot", entry_id, slot),
                            "slot": slot,
                            "entry_id": entry_id,
                            "axis": axis_id,
                            "carrier": carrier_id,
                            "minimum_intensity": minimum_intensity,
                            "label_en": localize(entry, "en") or entry_id,
                            "label_ko": localize(entry, "ko") or entry_id,
                            "weight": candidate_pack_float(entry.get("weight")),
                            "selected_by_sampler": False,
                            "tags": normalize_list(entry.get("tags"))[:12],
                            "kind": normalize_list(entry.get("kind"))[:8],
                            "facets": {
                                str(key): normalize_list(value)[:12]
                                for key, value in (entry.get("facets") or {}).items()
                                if str(key).strip() and normalize_list(value)
                            },
                            "risk_groups": candidate_pack_adult_risk_groups(entry_id, adult_policy),
                            "applicability": {
                                "status": "eligible",
                                "source": f"{request.get('activation_source')}_adult_appeal_inventory",
                                "reason": "axis activated by the configured low-intensity default"
                                if request.get("activation_source") == "skill_default"
                                else "axis activated by explicit user control",
                            },
                            "conflicts_with": [],
                        }
                        inventory.append(candidate)
                        candidate_entries[candidate_id] = ("slot", slot, entry)
                        seen_sources.add(source_key)
                        carrier_count += 1
        axes[axis_id] = {
            "intensity": intensity,
            "active": enabled and intensity > 0,
            "carrier_ids": [
                str(carrier.get("id"))
                for carrier in axis_policy.get("carriers") or []
                if isinstance(carrier, dict) and str(carrier.get("id") or "")
            ],
            "candidate_inventory": inventory,
        }

    return {
        "enabled": enabled,
        "requested_enabled": bool(request.get("requested_enabled")),
        "contract_version": CANDIDATE_PACK_ADULT_APPEAL_CONTRACT_VERSION,
        "activation_source": request.get("activation_source"),
        "eligibility": request.get("eligibility", {}),
        "defaults": {
            "sensual_editorial_intensity": int(
                (adult_policy.get("default_intensities") or {}).get(
                    "sensual_editorial", CANDIDATE_PACK_SENSUAL_EDITORIAL_DEFAULT_INTENSITY
                )
            ),
            "fetish_fashion_intensity": int(
                (adult_policy.get("default_intensities") or {}).get(
                    "fetish_fashion", CANDIDATE_PACK_FETISH_FASHION_DEFAULT_INTENSITY
                )
            ),
            "emphasis": str(
                adult_policy.get("default_emphasis")
                or CANDIDATE_PACK_ADULT_APPEAL_DEFAULT_EMPHASIS
            ),
        },
        "source_preset_id": source_preset_id,
        "axes": axes,
        "blend": {
            "emphasis": str((request.get("blend") or {}).get("emphasis") or "balanced"),
            "simultaneous_activation_allowed": True,
            "carrier_separation": {
                "sensual_editorial": ["gaze", "pose", "lighting", "silhouette"],
                "fetish_fashion": ["material", "garment_layering", "accessories", "footwear"],
            },
        },
        "composition_requirements": {
            "explicit_adult_original_subject": True,
            "adult_subject_phrase_required": True,
            "agency_phrase_required": True,
            "one_accepted_detail_per_active_axis": True,
            "configured_low_intensity_default": True,
            "appearance_or_popularity_inference_forbidden": True,
        },
        "combination_policy": {
            "risk_groups": adult_policy.get("risk_groups", {}),
            "hard_combinations": adult_policy.get("hard_combinations", []),
            "warning_combinations": adult_policy.get("warning_combinations", []),
        },
        "evaluation_boundary": "styling_intent_and_prompt_binding_are_preflight;_popularity_requires_human_or_engagement_evaluation",
    }


def candidate_pack_hybrid_adult_candidates(adult_appeal: Optional[JsonDict]) -> List[JsonDict]:
    candidates: List[JsonDict] = []
    if not isinstance(adult_appeal, dict):
        return candidates
    for axis in (adult_appeal.get("axes") or {}).values():
        if not isinstance(axis, dict):
            continue
        candidates.extend(
            candidate for candidate in axis.get("candidate_inventory") or [] if isinstance(candidate, dict)
        )
    return candidates


def candidate_pack_hybrid_candidates_compatible(candidate: JsonDict, selected: Sequence[JsonDict]) -> bool:
    candidate_id = str(candidate.get("id") or "")
    candidate_conflicts = {str(item) for item in candidate.get("conflicts_with") or []}
    for other in selected:
        other_id = str(other.get("id") or "")
        other_conflicts = {str(item) for item in other.get("conflicts_with") or []}
        if other_id in candidate_conflicts or candidate_id in other_conflicts:
            return False
    return True


def candidate_pack_hybrid_detail_function(candidate: JsonDict, route: JsonDict, index: int) -> str:
    axis = str(candidate.get("axis") or "")
    carrier = str(candidate.get("carrier") or "")
    if axis == "fetish_fashion":
        return "material_detail"
    if axis == "sensual_editorial":
        return "pose_camera" if carrier in {"gaze_pose", "framing"} else "viewer_hook"
    functions = [str(item) for item in route.get("functions") or [] if str(item).strip()]
    return functions[index % len(functions)] if functions else "material_detail"


def candidate_pack_hybrid_route_details(
    route: JsonDict,
    route_index: int,
    slots: JsonDict,
    masked_slot_names: Set[str],
    adult_appeal: Optional[JsonDict],
    limit: int,
) -> List[JsonDict]:
    selected: List[JsonDict] = []
    selected_sources: Set[str] = set()
    selected_slots: Set[str] = set()

    adult_axes = adult_appeal.get("axes") if isinstance(adult_appeal, dict) and isinstance(adult_appeal.get("axes"), dict) else {}
    for axis_id in CANDIDATE_PACK_ADULT_APPEAL_AXES:
        axis = adult_axes.get(axis_id) if isinstance(adult_axes.get(axis_id), dict) else {}
        inventory = [candidate for candidate in axis.get("candidate_inventory") or [] if isinstance(candidate, dict)]
        if not inventory or len(selected) >= limit:
            continue
        rotated = inventory[route_index % len(inventory) :] + inventory[: route_index % len(inventory)]
        for candidate in rotated:
            source = str(candidate.get("source_candidate_id") or candidate.get("id") or "")
            if source in selected_sources or not candidate_pack_hybrid_candidates_compatible(candidate, selected):
                continue
            selected.append(candidate)
            selected_sources.add(source)
            selected_slots.add(str(candidate.get("slot") or ""))
            break

    route_slots = [str(item) for item in route.get("slots") or [] if str(item).strip()]
    for slot_index, slot in enumerate(route_slots):
        if len(selected) >= limit or slot in masked_slot_names or slot in selected_slots:
            continue
        payload = slots.get(slot) if isinstance(slots.get(slot), dict) else {}
        candidates = [
            candidate
            for candidate in payload.get("candidates") or []
            if isinstance(candidate, dict)
            and (candidate.get("applicability") or {}).get("status", "eligible") == "eligible"
        ]
        alternatives = [candidate for candidate in candidates if not candidate.get("selected_by_sampler")]
        anchors = [candidate for candidate in candidates if candidate.get("selected_by_sampler")]
        ordered = alternatives + anchors
        if ordered:
            offset = (route_index + slot_index) % len(ordered)
            ordered = ordered[offset:] + ordered[:offset]
        for candidate in ordered:
            source = str(candidate.get("source_candidate_id") or candidate.get("id") or "")
            if source in selected_sources or not candidate_pack_hybrid_candidates_compatible(candidate, selected):
                continue
            selected.append(candidate)
            selected_sources.add(source)
            selected_slots.add(slot)
            break

    details: List[JsonDict] = []
    for index, candidate in enumerate(selected[:limit]):
        details.append(
            {
                "candidate_id": str(candidate.get("id") or ""),
                "slot": str(candidate.get("slot") or ""),
                "function": candidate_pack_hybrid_detail_function(candidate, route, index),
                "label_en": str(candidate.get("label_en") or candidate.get("entry_id") or ""),
                "label_ko": str(candidate.get("label_ko") or candidate.get("entry_id") or ""),
                "source": "adult_appeal_inventory" if candidate.get("axis") else "candidate_pack_slot",
                "axis": candidate.get("axis"),
                "carrier": candidate.get("carrier"),
                "minimum_intensity": candidate.get("minimum_intensity"),
                "selected_by_sampler": bool(candidate.get("selected_by_sampler")),
                "marginal_value_question": "Would removing this detail make the image less distinctive or less legible?",
            }
        )
    return details


def candidate_pack_hybrid_augmentation(
    data: JsonDict,
    result: JsonDict,
    slots: JsonDict,
    masked_slot_names: Set[str],
    adult_appeal: Optional[JsonDict],
) -> Optional[JsonDict]:
    policy = candidate_pack_hybrid_policy(data)
    activation_sources = candidate_pack_hybrid_activation_sources(result, adult_appeal)
    if not policy or not activation_sources:
        return None
    try:
        route_limit = max(2, int(policy.get("route_candidate_limit", 4) or 4))
    except (TypeError, ValueError):
        route_limit = 4
    routes: List[JsonDict] = []
    for route_index, route in enumerate(policy.get("routes") or []):
        if not isinstance(route, dict):
            continue
        details = candidate_pack_hybrid_route_details(
            route,
            route_index,
            slots,
            masked_slot_names,
            adult_appeal,
            route_limit,
        )
        routes.append(
            {
                "id": str(route.get("id") or f"route_{route_index + 1}"),
                "strategy": str(route.get("id") or f"route_{route_index + 1}"),
                "label": str(route.get("label") or route.get("id") or "augmentation route"),
                "candidate_ids": [detail["candidate_id"] for detail in details],
                "details": details,
            }
        )
    try:
        accepted_min = max(1, int(policy.get("accepted_detail_min", 2) or 2))
    except (TypeError, ValueError):
        accepted_min = 2
    try:
        accepted_max = max(accepted_min, int(policy.get("accepted_detail_max", 5) or 5))
    except (TypeError, ValueError):
        accepted_max = 5
    return {
        "enabled": True,
        "contract_version": CANDIDATE_PACK_HYBRID_CONTRACT_VERSION,
        "source": "candidate_pack_bounded_idea_amplifier",
        "activation_sources": activation_sources,
        "purpose": "preserve_an_agent_authored_concept_core_while_adding_optional_candidate_sourced_specificity",
        "core_policy": {
            "agent_authored_concept_core": True,
            "candidate_pack_may_expand_but_not_overwrite": True,
            "unconditional_candidate_acceptance_forbidden": True,
        },
        "route_contract": {
            "route_count": len(routes),
            "select_exactly": 1,
            "allow_select_none": True,
            "all_routes_must_be_considered": True,
            "routes": routes,
        },
        "adoption_contract": {
            "decision_states": policy.get("decision_states", ["accepted", "modified", "rejected"]),
            "detail_functions": policy.get(
                "detail_functions",
                ["concept_bridge", "material_detail", "pose_camera", "viewer_hook", "second_reading"],
            ),
            "minimum_accepted_if_selected": accepted_min,
            "maximum_accepted": accepted_max,
            "every_selected_route_candidate_requires_a_decision": True,
            "accepted_or_modified_candidate_must_be_chosen": True,
            "rejected_candidate_must_not_be_chosen": True,
            "accepted_or_modified_prompt_evidence_must_be_literal": True,
            "marginal_contribution_required": True,
        },
        "adult_appeal": adult_appeal or {"enabled": False},
        "evaluation_boundary": "audit_pass_proves_contract_and_literal_binding_only;_rendered_detail_and_audience_response_require_pixel_and_human_evaluation",
    }


def candidate_pack_concept_axes(soft_policy: JsonDict) -> JsonDict:
    axes = normalize_reference_identity_axes(soft_policy.get("identity_axes"))
    return {
        "required": axes,
        "required_count": len(axes),
        "source": "identity_axes" if axes else "none",
    }


def candidate_pack_scene_contract(
    soft_policy: JsonDict,
    slots: JsonDict,
    selected_blueprint: Optional[JsonDict] = None,
) -> JsonDict:
    groups: Dict[str, JsonDict] = {}
    for anchor in soft_policy.get("anchors", []) or []:
        if not isinstance(anchor, dict) or str(anchor.get("variant_strategy") or "") != "atomic_scene":
            continue
        group_id = str(anchor.get("variant_group") or "atomic_scene")
        slot = str(anchor.get("slot") or "")
        if not slot:
            continue
        group = groups.setdefault(
            group_id,
            {"group": group_id, "strategy": "atomic_scene", "fail_closed": True, "slots": {}},
        )
        allowed = normalize_list(anchor.get("pool")) or normalize_list(anchor.get("ids"))
        slot_payload = slots.get(slot) if isinstance(slots.get(slot), dict) else {}
        candidates = [
            str(candidate.get("entry_id") or "")
            for candidate in slot_payload.get("candidates", []) or []
            if isinstance(candidate, dict) and str(candidate.get("entry_id") or "")
        ]
        selected = candidate_pack_slot_selected_entry_id(slot_payload)
        group["slots"][slot] = {
            "allowed_entry_ids": allowed,
            "candidate_entry_ids": candidates,
            "selected_entry_id": selected or None,
        }
    if selected_blueprint:
        scene_tag = str(selected_blueprint.get("scene_tag") or "")
        atomic_scene = (
            selected_blueprint.get("atomic_scene")
            if isinstance(selected_blueprint.get("atomic_scene"), dict)
            else {}
        )
        required_slots = [
            slot
            for slot in ("subject", "action", "location", "prop")
            if isinstance(atomic_scene.get(slot), dict)
            and str(atomic_scene[slot].get("label_en") or "").strip()
        ]
        if scene_tag and len(required_slots) == 4:
            groups[scene_tag] = {
                "group": scene_tag,
                "strategy": "atomic_scene",
                "source": "selected_render_blueprint",
                "fail_closed": True,
                "required_slots": required_slots,
                "scene_functions": normalize_list(selected_blueprint.get("scene_functions")),
                "diegetic_visual_provenance": normalize_list(
                    selected_blueprint.get("diegetic_visual_provenance")
                ),
                "controlled_candidate_slots": required_slots,
                "slots": {
                    slot: {
                        "label_en": str(atomic_scene[slot].get("label_en") or "").strip(),
                        "label_ko": str(atomic_scene[slot].get("label_ko") or "").strip(),
                        "audit_terms": normalize_list(atomic_scene[slot].get("audit_terms")),
                    }
                    for slot in required_slots
                },
            }

    direct_scene_tags: Dict[str, int] = {}
    if not selected_blueprint:
        for slot in ("subject", "action", "location", "prop", "situation_context", "occasion_context"):
            slot_payload = slots.get(slot) if isinstance(slots.get(slot), dict) else {}
            selected_id = str(slot_payload.get("selected") or "")
            for candidate in slot_payload.get("candidates", []) or []:
                if not isinstance(candidate, dict) or str(candidate.get("id") or "") != selected_id:
                    continue
                for tag in normalize_list(candidate.get("tags")):
                    if tag.endswith("_scene"):
                        direct_scene_tags[tag] = direct_scene_tags.get(tag, 0) + 1
    selected_scene_tag = ""
    if direct_scene_tags:
        selected_scene_tag = sorted(
            direct_scene_tags,
            key=lambda tag: (-direct_scene_tags[tag], tag),
        )[0]
    if selected_scene_tag:
        group = {
            "group": selected_scene_tag,
            "strategy": "atomic_scene",
            "source": "selected_direct_preset_scene_tag",
            "fail_closed": True,
            "required_slots": [],
            "scene_functions": [],
            "diegetic_visual_provenance": [],
            "slots": {},
        }
        for slot in ("subject", "action", "location", "prop", "situation_context", "occasion_context"):
            slot_payload = slots.get(slot) if isinstance(slots.get(slot), dict) else {}
            matching = [
                candidate
                for candidate in slot_payload.get("candidates", []) or []
                if isinstance(candidate, dict) and selected_scene_tag in normalize_list(candidate.get("tags"))
            ]
            if not matching:
                continue
            allowed = [str(candidate.get("entry_id") or "") for candidate in matching if str(candidate.get("entry_id") or "")]
            selected = candidate_pack_slot_selected_entry_id(slot_payload)
            group["slots"][slot] = {
                "allowed_entry_ids": allowed,
                "candidate_entry_ids": [
                    str(candidate.get("entry_id") or "")
                    for candidate in slot_payload.get("candidates", []) or []
                    if isinstance(candidate, dict) and str(candidate.get("entry_id") or "")
                ],
                "selected_entry_id": selected or None,
            }
            if slot in {"subject", "action", "location", "prop"}:
                group["required_slots"].append(slot)
            for candidate in matching:
                facets = candidate.get("facets") if isinstance(candidate.get("facets"), dict) else {}
                group["scene_functions"].extend(normalize_list(facets.get("scene_function")))
                group["diegetic_visual_provenance"].extend(
                    normalize_list(facets.get("diegetic_visual_provenance"))
                )
        group["required_slots"] = sorted(set(group["required_slots"]))
        group["scene_functions"] = sorted(set(group["scene_functions"]))
        group["diegetic_visual_provenance"] = sorted(set(group["diegetic_visual_provenance"]))
        groups.setdefault(selected_scene_tag, group)
    return {
        "enabled": bool(groups),
        "strategy": "atomic_scene" if groups else "none",
        "groups": list(groups.values()),
    }


def candidate_pack_selected_preset(data: JsonDict, result: JsonDict) -> JsonDict:
    provenance = result.get("provenance") if isinstance(result.get("provenance"), dict) else {}
    preset_id = str(provenance.get("preset_id") or result.get("preset_id") or "")
    return candidate_pack_preset_by_id(data, preset_id) or {}


RENDER_CONTRACT_OPERATIONAL_TERMS = {
    "administer",
    "audit",
    "catalog",
    "check",
    "checking",
    "compare",
    "comparing",
    "coordinate",
    "coordinating",
    "document",
    "handoff",
    "inspect",
    "inspection",
    "ledger",
    "monitor",
    "record",
    "register",
    "review",
    "sorting",
    "verify",
    "verifying",
}


def render_contract_filter_ids(preset: JsonDict, slot: str) -> List[str]:
    filters = preset.get("filters") if isinstance(preset.get("filters"), dict) else {}
    slot_filter = filters.get(slot) if isinstance(filters.get(slot), dict) else {}
    return normalize_list(slot_filter.get("ids"))


def render_contract_entry_by_id(data: JsonDict, slot: str, entry_id: str) -> JsonDict:
    return next(
        (
            entry
            for entry in data.get("slots", {}).get(slot, []) or []
            if isinstance(entry, dict) and str(entry.get("id") or "") == str(entry_id)
        ),
        {},
    )


def render_contract_blueprint_scene_tag(preset_id: str, blueprint_id: str) -> str:
    normalized = re.sub(r"[^a-z0-9_]+", "_", f"{preset_id}_{blueprint_id}".lower()).strip("_")
    return f"scene_blueprint_{normalized}_scene"


def render_contract_action_is_operational(action: str) -> bool:
    action_tokens = {
        item
        for item in re.split(r"[^a-z0-9]+", str(action or "").lower())
        if item
    }
    return bool(action_tokens & RENDER_CONTRACT_OPERATIONAL_TERMS)


def render_contract_resolved_scene_blueprints(data: JsonDict, preset: JsonDict) -> List[JsonDict]:
    contract = preset.get("render_contract") if isinstance(preset.get("render_contract"), dict) else {}
    if not contract:
        return []
    preset_id = str(preset.get("id") or "")
    provenance = normalize_list(contract.get("diegetic_visual_provenance"))
    genre_anchors = normalize_list(contract.get("genre_anchors"))
    blueprints: List[JsonDict] = []

    if contract.get("derive_filtered_scenes") is True:
        try:
            derived_limit = max(1, min(6, int(contract.get("derived_scene_limit", 2))))
        except (TypeError, ValueError):
            derived_limit = 2
        cycles = normalize_list(contract.get("scene_function_cycle")) or ["controlled_action"]
        action_templates = normalize_list(contract.get("scene_action_templates")) or ["{action}"]
        slot_ids = {
            slot: render_contract_filter_ids(preset, slot)
            for slot in ("subject", "action", "location", "prop")
        }
        slot_entries = {
            slot: [render_contract_entry_by_id(data, slot, entry_id) for entry_id in ids]
            for slot, ids in slot_ids.items()
        }
        preset_en = str(preset.get("en") or preset_id).strip()
        preset_ko = str(preset.get("ko") or preset_id).strip()
        fallback_en = {
            "subject": f"the principal participants or material subject of {preset_en}",
            "action": f"a decisive observable change within {preset_en}",
            "location": f"a source-grounded setting specific to {preset_en}",
            "prop": "one unbranded physical clue tied to the event",
        }
        fallback_ko = {
            "subject": f"{preset_ko}의 핵심 참여자 또는 물질 대상",
            "action": f"{preset_ko}에서 관찰되는 결정적 변화",
            "location": f"{preset_ko}에 맞는 근거 기반 장소",
            "prop": "사건에 연결된 비상표 물리 단서 하나",
        }
        for index in range(derived_limit):
            entries: Dict[str, JsonDict] = {}
            for slot in ("subject", "action", "location", "prop"):
                available = slot_entries.get(slot) or []
                entries[slot] = available[index % len(available)] if available else {}
            action_en = localize(entries["action"], "en") or fallback_en["action"]
            action_ko = localize(entries["action"], "ko") or fallback_ko["action"]
            template = action_templates[index % len(action_templates)]
            rendered_action = (
                template.replace("{action}", action_en)
                .replace("{preset_en}", preset_en)
                .replace("{preset_ko}", preset_ko)
            )
            function = cycles[index % len(cycles)]
            blueprint_id = f"derived_{index + 1}"
            source_subject = entries["subject"]
            blueprints.append(
                {
                    "id": blueprint_id,
                    "scene_tag": render_contract_blueprint_scene_tag(preset_id, blueprint_id),
                    "scene_functions": [function],
                    "diegetic_visual_provenance": provenance,
                    "genre_anchors": genre_anchors,
                    "relationship_stakes": [],
                    "expression_mode": "derived_research_scene",
                    "subject": localize(source_subject, "en") or fallback_en["subject"],
                    "subject_ko": localize(source_subject, "ko") or fallback_ko["subject"],
                    "subject_kind": normalize_list(source_subject.get("kind")),
                    "subject_tags": normalize_list(source_subject.get("tags")),
                    "action": rendered_action,
                    "action_ko": action_ko,
                    "location": localize(entries["location"], "en") or fallback_en["location"],
                    "location_ko": localize(entries["location"], "ko") or fallback_ko["location"],
                    "prop": localize(entries["prop"], "en") or fallback_en["prop"],
                    "prop_ko": localize(entries["prop"], "ko") or fallback_ko["prop"],
                    "operational": function == "operational_documentary"
                    or render_contract_action_is_operational(rendered_action),
                    "source": "selected_preset.render_contract.derived_filtered_scene",
                }
            )

    for raw in contract.get("scene_blueprints") or []:
        if not isinstance(raw, dict) or not str(raw.get("id") or ""):
            continue
        blueprint_id = str(raw.get("id"))
        functions = normalize_list(raw.get("scene_functions")) or ["controlled_action"]
        blueprint = {
            "id": blueprint_id,
            "scene_tag": str(raw.get("scene_tag") or render_contract_blueprint_scene_tag(preset_id, blueprint_id)),
            "scene_functions": functions,
            "diegetic_visual_provenance": normalize_list(raw.get("diegetic_visual_provenance")) or provenance,
            "genre_anchors": normalize_list(raw.get("genre_anchors")) or genre_anchors,
            "relationship_stakes": normalize_list(raw.get("relationship_stakes")),
            "expression_mode": str(raw.get("expression_mode") or "authored_scene_blueprint"),
            "character_evidence_types": normalize_list(raw.get("character_evidence_types")),
            "runtime_ids": normalize_list(raw.get("runtime_ids")),
            "primary_runtime_id": str(raw.get("primary_runtime_id") or ""),
            "support_runtime_ids": normalize_list(raw.get("support_runtime_ids")),
            "policy_ids": normalize_list(raw.get("policy_ids")),
            "relationship_mode": str(raw.get("relationship_mode") or ""),
            "audience_familiarity": str(raw.get("audience_familiarity") or ""),
            "market_origin": str(raw.get("market_origin") or ""),
            "static_portrait": bool(raw.get("static_portrait")),
            "subject": str(raw.get("subject") or "").strip(),
            "subject_ko": str(raw.get("subject_ko") or raw.get("subject") or "").strip(),
            "subject_kind": normalize_list(raw.get("subject_kind")),
            "subject_tags": normalize_list(raw.get("subject_tags")),
            "action": str(raw.get("action") or "").strip(),
            "action_ko": str(raw.get("action_ko") or raw.get("action") or "").strip(),
            "location": str(raw.get("location") or "").strip(),
            "location_ko": str(raw.get("location_ko") or raw.get("location") or "").strip(),
            "prop": str(raw.get("prop") or "").strip(),
            "prop_ko": str(raw.get("prop_ko") or raw.get("prop") or "").strip(),
            "operational": (
                bool(raw.get("operational"))
                if "operational" in raw
                else (
                    "operational_documentary" in functions
                    or render_contract_action_is_operational(str(raw.get("action") or ""))
                )
            ),
            "source": "selected_preset.render_contract.scene_blueprints",
        }
        if all(blueprint.get(slot) for slot in ("subject", "action", "location", "prop")):
            blueprints.append(blueprint)

    unique: Dict[str, JsonDict] = {}
    for blueprint in blueprints:
        unique.setdefault(str(blueprint.get("id") or ""), blueprint)
    return list(unique.values())


def candidate_pack_scene_blueprint_request_text(result: JsonDict) -> str:
    provenance = result.get("provenance") if isinstance(result.get("provenance"), dict) else {}
    values = [
        *normalize_list(provenance.get("concept_lock")),
        *normalize_list(provenance.get("user_mandatory_intents")),
        *normalize_list(provenance.get("additional_requirements")),
    ]
    return " ".join(values).lower()


def render_scene_blueprint_supports_no_people(blueprint: JsonDict) -> bool:
    """Return true only when a scene explicitly declares a non-human subject.

    An empty declaration is intentionally not treated as compatible: the
    render instruction sits outside the ordinary subject sampler, so its
    people-presence constraint must be independently provable.
    """
    declarations = {
        item.lower()
        for item in (
            *normalize_list(blueprint.get("subject_kind")),
            *normalize_list(blueprint.get("subject_tags")),
        )
        if item
    }
    return bool(declarations) and not bool(
        declarations & {"human", "people", "person", "portrait"}
    )


def candidate_pack_select_scene_blueprint(
    result: JsonDict,
    preset: JsonDict,
    blueprints: Sequence[JsonDict],
) -> JsonDict:
    if not blueprints:
        return {}
    provenance = result.get("provenance") if isinstance(result.get("provenance"), dict) else {}
    request_text = candidate_pack_scene_blueprint_request_text(result)
    if intent_explicitly_excludes_people(request_text):
        no_people_blueprints = [
            blueprint
            for blueprint in blueprints
            if render_scene_blueprint_supports_no_people(blueprint)
        ]
        if not no_people_blueprints:
            preset_id = str(preset.get("id") or "")
            raise ValueError(
                f"Preset {preset_id!r} has no explicitly non-human render scene compatible with the no-people request"
            )
        blueprints = no_people_blueprints
    requested_function = str(provenance.get("requested_scene_function") or "").strip()
    if requested_function:
        matching = [
            blueprint
            for blueprint in blueprints
            if requested_function in normalize_list(blueprint.get("scene_functions"))
        ]
        if not matching:
            preset_id = str(preset.get("id") or "")
            raise ValueError(
                f"Preset {preset_id!r} has no render scene for requested function {requested_function!r}"
            )
        authored_matching = [
            blueprint
            for blueprint in matching
            if str(blueprint.get("source") or "").endswith(".scene_blueprints")
        ]
        if authored_matching:
            matching = authored_matching
        blueprints = matching
    scored: List[tuple[int, str, JsonDict]] = []
    for blueprint in blueprints:
        corpus = " ".join(
            [
                str(blueprint.get("id") or ""),
                str(blueprint.get("subject") or ""),
                str(blueprint.get("action") or ""),
                str(blueprint.get("location") or ""),
                str(blueprint.get("prop") or ""),
                *normalize_list(blueprint.get("scene_functions")),
                *normalize_list(blueprint.get("genre_anchors")),
            ]
        ).lower()
        terms = {
            token
            for token in re.split(r"[^a-z0-9가-힣]+", corpus)
            if len(token) >= 4
        }
        score = sum(1 for term in terms if term in request_text)
        scored.append((score, str(blueprint.get("id") or ""), blueprint))
    scored.sort(key=lambda row: (-row[0], row[1]))
    if scored[0][0] > 0 and (len(scored) == 1 or scored[0][0] > scored[1][0]):
        selected = dict(scored[0][2])
        selected["selection_source"] = "unique_request_relevance"
        return selected
    seed = str(provenance.get("seed") or "0")
    preset_id = str(preset.get("id") or "")
    preset_digest = hashlib.sha256(f"scene-blueprint-offset|{preset_id}".encode("utf-8")).digest()
    offset = int.from_bytes(preset_digest[:8], "big") % len(blueprints)
    try:
        index = (int(seed) + offset) % len(blueprints)
        selection_source = (
            "requested_scene_function"
            if requested_function
            else "deterministic_seed_cycle"
        )
    except (TypeError, ValueError):
        digest = hashlib.sha256(f"scene-blueprint|{seed}|{preset_id}".encode("utf-8")).digest()
        index = int.from_bytes(digest[:8], "big") % len(blueprints)
        selection_source = (
            "requested_scene_function"
            if requested_function
            else "deterministic_seed_hash"
        )
    selected = dict(blueprints[index])
    selected["selection_source"] = selection_source
    return selected


def candidate_pack_resolve_scene_blueprint(
    data: JsonDict,
    result: JsonDict,
    preset: JsonDict,
) -> JsonDict:
    """Resolve one render scene without mutating the sampler candidate pool.

    A scene blueprint is a mandatory render instruction, not an additional
    taxonomy candidate. Keeping it outside ``slots`` preserves the exact
    sampler-eligible pool and prevents a resolved scene from masquerading as a
    semantic/sampler result.
    """
    blueprints = render_contract_resolved_scene_blueprints(data, preset)
    selected = candidate_pack_select_scene_blueprint(result, preset, blueprints)
    if not selected:
        return {}
    selected["atomic_scene"] = {
        slot: {
            "label_en": str(selected.get(slot) or "").strip(),
            "label_ko": str(selected.get(f"{slot}_ko") or selected.get(slot) or "").strip(),
            "audit_terms": [str(selected.get(slot) or "").strip()],
        }
        for slot in ("subject", "action", "location", "prop")
    }
    selected["available_blueprint_count"] = len(blueprints)
    selected["available_blueprint_ids"] = [str(item.get("id") or "") for item in blueprints]
    return selected


def candidate_pack_render_contract(
    preset: JsonDict,
    scene_contract: JsonDict,
    selected_blueprint: Optional[JsonDict] = None,
) -> JsonDict:
    raw = preset.get("render_contract") if isinstance(preset.get("render_contract"), dict) else {}
    if not raw:
        return {
            "enabled": False,
            "source": "none",
            "topic_intents": [],
            "evidence_budget": {"enabled": False},
            "selected_scene": {},
        }
    topic_intents: List[JsonDict] = []
    for item in raw.get("topic_intents", []) or []:
        if isinstance(item, str):
            text = item.strip()
            normalized = {"text": text, "audit_terms": [text] if text else []}
        elif isinstance(item, dict):
            text = str(item.get("text") or "").strip()
            normalized = {
                "text": text,
                "audit_terms": normalize_list(item.get("audit_terms")) or ([text] if text else []),
                "kind": str(item.get("kind") or "topic_identity"),
            }
        else:
            continue
        if normalized.get("text") and normalized.get("audit_terms"):
            topic_intents.append(normalized)
    raw_budget = raw.get("evidence_budget") if isinstance(raw.get("evidence_budget"), dict) else {}
    world_clue_slots = normalize_list(raw_budget.get("world_clue_slots"))
    evidence_budget = {
        "enabled": bool(world_clue_slots),
        "world_clue_slots": world_clue_slots,
        "minimum_chosen": max(0, int(raw_budget.get("minimum_chosen", 1))) if world_clue_slots else 0,
        "maximum_chosen": max(0, int(raw_budget.get("maximum_chosen", 2))) if world_clue_slots else 0,
        "guidance": str(raw_budget.get("guidance") or "one core event, sparse world clues, one stake, one genre anchor"),
    }
    selected_scene: JsonDict = {}
    direct_groups = [
        group
        for group in scene_contract.get("groups", []) or []
        if isinstance(group, dict) and group.get("source") == "selected_direct_preset_scene_tag"
    ]
    if direct_groups:
        group = direct_groups[0]
        selected_scene = {
            "scene_tag": group.get("group"),
            "scene_functions": normalize_list(group.get("scene_functions")),
            "diegetic_visual_provenance": normalize_list(group.get("diegetic_visual_provenance")),
        }
        scene_metadata = raw.get("scene_metadata") if isinstance(raw.get("scene_metadata"), dict) else {}
        configured_scene = scene_metadata.get(str(group.get("group") or ""))
        if isinstance(configured_scene, dict):
            selected_scene["scene_functions"] = (
                normalize_list(configured_scene.get("scene_functions"))
                or selected_scene["scene_functions"]
            )
            selected_scene["diegetic_visual_provenance"] = (
                normalize_list(configured_scene.get("diegetic_visual_provenance"))
                or selected_scene["diegetic_visual_provenance"]
            )
            selected_scene["relationship_stakes"] = normalize_list(
                configured_scene.get("relationship_stakes")
            )
            selected_scene["genre_anchors"] = normalize_list(
                configured_scene.get("genre_anchors")
            )
            selected_scene["expression_mode"] = str(
                configured_scene.get("expression_mode") or ""
            )
    if selected_blueprint:
        selected_scene = {
            "scene_tag": selected_blueprint.get("scene_tag"),
            "blueprint_id": selected_blueprint.get("id"),
            "scene_functions": normalize_list(selected_blueprint.get("scene_functions")),
            "diegetic_visual_provenance": normalize_list(
                selected_blueprint.get("diegetic_visual_provenance")
            ),
            "relationship_stakes": normalize_list(selected_blueprint.get("relationship_stakes")),
            "genre_anchors": normalize_list(selected_blueprint.get("genre_anchors")),
            "expression_mode": str(selected_blueprint.get("expression_mode") or ""),
            "character_evidence_types": normalize_list(
                selected_blueprint.get("character_evidence_types")
            ),
            "runtime_ids": normalize_list(selected_blueprint.get("runtime_ids")),
            "primary_runtime_id": str(selected_blueprint.get("primary_runtime_id") or ""),
            "relationship_mode": str(selected_blueprint.get("relationship_mode") or ""),
            "audience_familiarity": str(selected_blueprint.get("audience_familiarity") or ""),
            "market_origin": str(selected_blueprint.get("market_origin") or ""),
            "operational": bool(selected_blueprint.get("operational")),
            "selection_source": str(selected_blueprint.get("selection_source") or ""),
            "available_blueprint_count": int(selected_blueprint.get("available_blueprint_count") or 0),
            "available_blueprint_ids": normalize_list(selected_blueprint.get("available_blueprint_ids")),
            "atomic_scene": copy.deepcopy(selected_blueprint.get("atomic_scene") or {}),
        }
    return {
        "enabled": True,
        "source": "selected_preset.render_contract",
        "profile": str(raw.get("profile") or "preset_specific"),
        "evidence_route_id": str(raw.get("evidence_route_id") or preset.get("id") or ""),
        "topic_intents": topic_intents,
        "evidence_budget": evidence_budget,
        "selected_scene": selected_scene,
    }


def candidate_pack_character_grammar(
    data: JsonDict,
    preset: JsonDict,
    selected_blueprint: Optional[JsonDict],
) -> JsonDict:
    """Materialize the selected sparse character-mechanism bundle."""
    graph = data.get("character_mechanism_graph")
    raw_contract = preset.get("render_contract") if isinstance(preset.get("render_contract"), dict) else {}
    grammar = (
        raw_contract.get("character_grammar")
        if isinstance(raw_contract.get("character_grammar"), dict)
        else {}
    )
    if not isinstance(graph, dict) or not grammar:
        return {
            "enabled": False,
            "domain": "",
            "runtime_nodes": [],
            "policy_ids": [],
            "valid": True,
        }
    if not isinstance(selected_blueprint, dict):
        raise ValueError(f"Character preset {preset.get('id')!r} has no selected scene blueprint")

    node_index = {
        str(node.get("id")): node
        for node in graph.get("runtime_nodes", [])
        if isinstance(node, dict) and str(node.get("id") or "")
    }
    policy_index = {
        str(policy.get("id")): policy
        for policy in graph.get("policies", [])
        if isinstance(policy, dict) and str(policy.get("id") or "")
    }
    topic_id = str(grammar.get("topic_id") or "")
    family_id = str(grammar.get("family_id") or "")
    runtime_anchor_ids = normalize_list(grammar.get("runtime_anchor_ids"))
    for runtime_id in runtime_anchor_ids:
        node = node_index.get(runtime_id)
        if node is None or topic_id not in character_runtime_node_topic_ids(node):
            raise ValueError(f"Character preset references invalid runtime anchor {runtime_id}")
    runtime_ids = normalize_list(selected_blueprint.get("runtime_ids"))
    primary_runtime_id = str(selected_blueprint.get("primary_runtime_id") or "")
    max_support_cues = int(graph.get("max_support_cues", 2))
    if not 1 <= len(runtime_ids) <= 1 + max_support_cues:
        raise ValueError(f"Character scene for {preset.get('id')!r} violates the sparse runtime budget")
    if len(runtime_ids) != len(set(runtime_ids)) or primary_runtime_id not in runtime_ids:
        raise ValueError(f"Character scene for {preset.get('id')!r} has an invalid primary/runtime set")
    selected_nodes: List[JsonDict] = []
    for runtime_id in runtime_ids:
        node = node_index.get(runtime_id)
        if node is None:
            raise ValueError(f"Character scene references unknown runtime node {runtime_id}")
        if (
            topic_id not in character_runtime_node_topic_ids(node)
            or family_id not in character_runtime_node_family_ids(node)
        ):
            raise ValueError(f"Character scene runtime node {runtime_id} crosses its topic/family boundary")
        if str(node.get("role") or "") != "visual_atom":
            raise ValueError(f"Character scene cannot select nonvisual runtime node {runtime_id}")
        selected_nodes.append(
            {
                "id": runtime_id,
                "role": "primary" if runtime_id == primary_runtime_id else "support",
                "definition": str(node.get("definition") or ""),
                "priority_dimension": str(node.get("priority_dimension") or "observable_action"),
            }
        )

    compatible_edge_ids = [
        str(edge.get("id"))
        for edge in graph.get("compatibility_edges", [])
        if isinstance(edge, dict)
        and str(edge.get("topic_id") or "") == topic_id
        and set(runtime_ids).issubset(set(normalize_list(edge.get("node_ids"))))
    ]
    if len(runtime_ids) > 1 and not compatible_edge_ids:
        raise ValueError(f"Character scene for {preset.get('id')!r} has no compatible runtime bundle")

    policy_ids = list(
        dict.fromkeys(
            normalize_list(grammar.get("policy_ids"))
            + normalize_list(selected_blueprint.get("policy_ids"))
        )
    )
    missing_policies = [policy_id for policy_id in policy_ids if policy_id not in policy_index]
    if missing_policies:
        raise ValueError(f"Character scene references unknown policies {missing_policies}")
    applicable_guards: List[JsonDict] = []
    for guard in graph.get("guard_rules", []) or []:
        if not isinstance(guard, dict):
            continue
        topic_ids = set(normalize_list(guard.get("topic_ids")))
        if topic_ids and topic_id not in topic_ids:
            continue
        required = set(normalize_list(guard.get("required_policy_ids")))
        if required and not required.issubset(set(policy_ids)):
            raise ValueError(
                f"Character scene for {preset.get('id')!r} is missing guard policies {sorted(required - set(policy_ids))}"
            )
        forbidden = set(normalize_list(guard.get("forbidden_runtime_ids")))
        if forbidden & set(runtime_ids):
            raise ValueError(
                f"Character scene for {preset.get('id')!r} selects forbidden runtime nodes {sorted(forbidden & set(runtime_ids))}"
            )
        for combination in guard.get("forbidden_runtime_combinations") or []:
            combination_ids = set(normalize_list(combination))
            if combination_ids and combination_ids.issubset(set(runtime_ids)):
                raise ValueError(
                    f"Character scene for {preset.get('id')!r} selects forbidden runtime combination {sorted(combination_ids)}"
                )
        trigger_runtime_ids = set(normalize_list(guard.get("trigger_runtime_ids")))
        requires_runtime_any = set(normalize_list(guard.get("requires_runtime_any")))
        if trigger_runtime_ids & set(runtime_ids) and not requires_runtime_any & set(runtime_ids):
            raise ValueError(
                f"Character scene for {preset.get('id')!r} omits a required runtime companion for {sorted(trigger_runtime_ids & set(runtime_ids))}"
            )
        applicable_guards.append(
            {
                "id": str(guard.get("id") or ""),
                "kind": str(guard.get("kind") or "constraint"),
            }
        )

    return {
        "enabled": True,
        "domain": str(graph.get("domain") or ""),
        "topic_id": topic_id,
        "family_id": family_id,
        "primary_runtime_id": primary_runtime_id,
        "runtime_anchor_ids": runtime_anchor_ids,
        "runtime_nodes": selected_nodes,
        "policy_ids": policy_ids,
        "policies": [
            {"id": policy_id, "definition": str(policy_index[policy_id].get("definition") or "")}
            for policy_id in policy_ids
        ],
        "priority_order": normalize_list(graph.get("priority_order")),
        "max_support_cues": max_support_cues,
        "compatible_edge_ids": compatible_edge_ids,
        "applicable_guard_rules": applicable_guards,
        "required_evidence_types": normalize_list(grammar.get("required_evidence_types")),
        "character_evidence_types": normalize_list(
            selected_blueprint.get("character_evidence_types")
        ),
        "audience_familiarity": str(
            selected_blueprint.get("audience_familiarity") or "literal_general"
        ),
        "market_origin": str(selected_blueprint.get("market_origin") or "nonvisual_unspecified"),
        "valid": True,
    }


def candidate_pack_render_mandatory_intents(
    render_contract: JsonDict,
    preset_id: str,
) -> List[JsonDict]:
    candidate_id = candidate_pack_candidate_id("preset", preset_id) if preset_id else ""
    rows: List[JsonDict] = []
    for intent in render_contract.get("topic_intents", []) or []:
        if not isinstance(intent, dict):
            continue
        text = str(intent.get("text") or "").strip()
        audit_terms = normalize_list(intent.get("audit_terms"))
        if not text or not audit_terms:
            continue
        rows.append(
            {
                "text": text,
                "source": "selected_preset.render_contract",
                "source_text": text,
                "kind": str(intent.get("kind") or "topic_identity"),
                "status": "covered",
                "covered_by": [candidate_id] if candidate_id else [],
                "audit_terms": audit_terms,
            }
        )
    return rows


def candidate_pack_slot_selected_entry_id(slot_payload: JsonDict) -> str:
    selected = str(slot_payload.get("selected") or "")
    parts = selected.split(":", 2)
    if len(parts) == 3 and parts[0] == "slot":
        return parts[2]
    return ""


def candidate_pack_selected_choice_entry(result: JsonDict, slot: str, entry_id: str) -> JsonDict:
    choices = result.get("choices") if isinstance(result.get("choices"), dict) else {}
    choice = choices.get(slot)
    if isinstance(choice, dict) and str(choice.get("id") or "") == entry_id:
        return choice
    return {"id": entry_id}


def candidate_pack_entry_terms(entry: JsonDict, candidate: Optional[JsonDict] = None) -> List[str]:
    terms: List[str] = []
    for source in (entry, candidate or {}):
        for key in ("id", "en", "ko", "label_en", "label_ko", "description", "embedding_text", "tags", "kind"):
            raw = source.get(key)
            if isinstance(raw, list):
                terms.extend(str(item) for item in raw if str(item).strip())
            elif raw is not None and str(raw).strip():
                terms.append(str(raw))
    return list(dict.fromkeys(terms))[:16]


def candidate_pack_motif_budget(result: JsonDict, trace: JsonDict, soft_policy: JsonDict) -> JsonDict:
    taxonomy = motif_group_taxonomy_from_policy(soft_policy)
    choice_ids = result_choice_ids(result)
    selected_motifs = infer_motif_groups_from_choice_ids(choice_ids, soft_policy)
    quotas = normalize_reference_motif_quotas(soft_policy.get("motif_quotas"))
    ledger_summary = (
        trace.get("anchor_diversity_ledger_summary")
        if isinstance(trace.get("anchor_diversity_ledger_summary"), dict)
        else {"enabled": False, "counts": {}}
    )
    ledger_counts = {}
    if isinstance(trace.get("anchor_diversity_ledger_summary"), dict):
        counts = trace["anchor_diversity_ledger_summary"].get("counts")
        if isinstance(counts, dict):
            ledger_counts = counts.get("motif_group") if isinstance(counts.get("motif_group"), dict) else {}
    batch_counts = {}
    history = trace.get("batch_history_summary") if isinstance(trace.get("batch_history_summary"), dict) else {}
    if isinstance(history.get("counts"), dict):
        batch_counts = history["counts"].get("motif_group") if isinstance(history["counts"].get("motif_group"), dict) else {}
    discouraged: List[str] = []
    for motif, quota in quotas.items():
        batch_count = int(batch_counts.get(motif, 0) or 0)
        recent_count = int(ledger_counts.get(motif, 0) or 0)
        max_batch_uses = quota.get("max_batch_uses")
        max_recent_uses = quota.get("max_recent_uses")
        if isinstance(max_batch_uses, int) and batch_count >= max_batch_uses:
            discouraged.append(motif)
            continue
        if isinstance(max_recent_uses, int) and recent_count >= max_recent_uses:
            discouraged.append(motif)
    return {
        "quotas": quotas,
        "motif_taxonomy": taxonomy,
        "selected_motifs": selected_motifs,
        "discouraged_now": sorted(dict.fromkeys(discouraged)),
        "ledger": ledger_summary,
    }


def candidate_pack_dropout_config(soft_policy: JsonDict) -> JsonDict:
    return normalize_reference_semantic_dropout(soft_policy.get("semantic_dropout"))


def candidate_pack_protected_dropout_slots(contract: JsonDict, soft_policy: JsonDict) -> Set[str]:
    protected = set(CANDIDATE_PACK_DROPOUT_PROTECTED_SLOTS)
    protected.update(str(slot) for slot in contract.get("forced_slots", []) or [])
    for anchor in soft_policy.get("anchors", []) or []:
        if anchor.get("critical"):
            protected.add(str(anchor.get("slot") or ""))
    return {slot for slot in protected if slot}


def candidate_pack_bucket_slots(bucket: str) -> tuple[str, ...]:
    return CANDIDATE_PACK_SEMANTIC_DROPOUT_BUCKETS.get(bucket, ())


def candidate_pack_eligible_dropout_buckets(
    slots: JsonDict,
    contract: JsonDict,
    soft_policy: JsonDict,
    config: JsonDict,
) -> Dict[str, List[str]]:
    if not config.get("enabled"):
        return {}
    protected = candidate_pack_protected_dropout_slots(contract, soft_policy)
    configured = normalize_list(config.get("maskable_buckets"))
    buckets = configured or list(CANDIDATE_PACK_SEMANTIC_DROPOUT_BUCKETS)
    eligible: Dict[str, List[str]] = {}
    for bucket in buckets:
        selected_slots: List[str] = []
        for slot in candidate_pack_bucket_slots(bucket):
            slot_payload = slots.get(slot)
            if not isinstance(slot_payload, dict) or slot in protected:
                continue
            if candidate_pack_slot_selected_entry_id(slot_payload):
                selected_slots.append(slot)
        if selected_slots:
            eligible[bucket] = selected_slots
    return eligible


def candidate_pack_choose_masked_buckets(
    result: JsonDict,
    contract: JsonDict,
    soft_policy: JsonDict,
    slots: JsonDict,
) -> List[str]:
    config = candidate_pack_dropout_config(soft_policy)
    eligible = candidate_pack_eligible_dropout_buckets(slots, contract, soft_policy, config)
    if not eligible:
        return []
    min_buckets = int(config.get("min_buckets", 0) or 0)
    max_buckets = int(config.get("max_buckets", 0) or 0)
    if max_buckets <= 0:
        max_buckets = max(1, min(2, len(eligible)))
    max_buckets = max(0, min(max_buckets, len(eligible)))
    min_buckets = min(max(min_buckets, 0), max_buckets)
    probability = float(config.get("probability", 1.0 if min_buckets else 0.0) or 0.0)
    seed = str((result.get("provenance") or {}).get("seed") or "")
    concept = str(soft_policy.get("concept") or "")
    preset = str((result.get("provenance") or {}).get("preset_id") or result.get("preset_id") or "")
    ordered = sorted(
        eligible,
        key=lambda bucket: hashlib.sha256(f"{seed}|{concept}|{preset}|{bucket}".encode("utf-8")).hexdigest(),
    )
    selected: List[str] = []
    for bucket in ordered:
        digest = hashlib.sha256(f"dropout|{seed}|{concept}|{preset}|{bucket}".encode("utf-8")).digest()
        threshold = int.from_bytes(digest[:8], "big") / 2**64
        if len(selected) < min_buckets or threshold <= probability:
            selected.append(bucket)
        if len(selected) >= max_buckets:
            break
    if len(selected) < min_buckets:
        selected.extend(bucket for bucket in ordered if bucket not in selected)
    return selected[:max_buckets]


def candidate_pack_open_slots(
    result: JsonDict,
    slots: JsonDict,
    masked_buckets: Sequence[str],
) -> List[JsonDict]:
    open_slots: List[JsonDict] = []
    for bucket in masked_buckets:
        for slot in candidate_pack_bucket_slots(bucket):
            slot_payload = slots.get(slot)
            if not isinstance(slot_payload, dict):
                continue
            entry_id = candidate_pack_slot_selected_entry_id(slot_payload)
            if not entry_id:
                continue
            open_slot = {
                "slot": slot,
                "bucket": bucket,
                "status": "intentionally_open",
                "reason": "semantic_dropout",
            }
            open_slots.append(open_slot)
            # The source choice itself is deliberately absent. Exposing its id,
            # terms, or label makes "dropout" a copyable answer key.
            slots.pop(slot, None)
    return open_slots


def candidate_pack_preset_reference(
    result: JsonDict,
    soft_policy: JsonDict,
    masked_buckets: Sequence[str],
    open_slots: Sequence[JsonDict],
) -> JsonDict:
    used_sections: List[str] = []
    if soft_policy.get("identity_axes"):
        used_sections.append("identity_axes")
    if soft_policy.get("motif_pools"):
        used_sections.append("motif_pools")
    if soft_policy.get("motif_quotas"):
        used_sections.append("motif_quotas")
    if soft_policy.get("safety_negative_floor"):
        used_sections.append("safety_constraints")
    dropped_sections = [f"bucket:{bucket}" for bucket in masked_buckets]
    return {
        "role": "reference_scaffold",
        "preset_id": (result.get("provenance") or {}).get("preset_id") or result.get("preset_id"),
        "used_sections": used_sections,
        "dropped_sections": dropped_sections,
        "masked_slots": [
            {"slot": slot.get("slot"), "bucket": slot.get("bucket")}
            for slot in open_slots
            if isinstance(slot, dict) and slot.get("slot")
        ],
        "exemplar_role": "optional_example_only" if soft_policy.get("exemplar_set") else "none",
    }


def candidate_pack_template_echo_risk(open_slots: Sequence[JsonDict]) -> JsonDict:
    masked_count = len([slot for slot in open_slots if isinstance(slot, dict)])
    return {
        "score": 0.0,
        "max_allowed_score": 0.2,
        "masked_slot_count": masked_count,
        "basis": "pre_composition_scaffold",
    }


def candidate_pack_integration_text_has_term(text: str, term: str) -> bool:
    term = str(term or "").strip().lower()
    if not term:
        return False
    lowered = text.lower()
    normalized_text = re.sub(r"[_/-]+", " ", lowered)
    normalized_term = re.sub(r"[_/-]+", " ", term)
    if term.isascii() and re.search(r"[A-Za-z0-9]", term):
        pattern = r"(?<![A-Za-z0-9])" + re.escape(term) + r"(?![A-Za-z0-9])"
        normalized_pattern = r"(?<![A-Za-z0-9])" + re.escape(normalized_term) + r"(?![A-Za-z0-9])"
        return re.search(pattern, lowered) is not None or re.search(normalized_pattern, normalized_text) is not None
    return term in lowered or normalized_term in normalized_text


def candidate_pack_integration_corpus(
    result: JsonDict,
    trace: JsonDict,
    presets: Sequence[JsonDict],
    slots: JsonDict,
    mandatory_intents: Sequence[JsonDict],
) -> str:
    provenance = result.get("provenance") if isinstance(result.get("provenance"), dict) else {}
    values: List[str] = [
        str(result.get("preset_id") or ""),
        str(provenance.get("preset_id") or ""),
        str(trace.get("intent") or ""),
    ]
    values.extend(normalize_list(provenance.get("concept_lock")))
    values.extend(normalize_list(provenance.get("additional_requirements")))
    for intent in mandatory_intents:
        if isinstance(intent, dict):
            values.append(str(intent.get("text") or ""))
            values.append(str(intent.get("source_text") or ""))
    for preset in presets:
        if not isinstance(preset, dict):
            continue
        values.extend(
            [
                str(preset.get("preset_id") or ""),
                str(preset.get("label_en") or ""),
                str(preset.get("label_ko") or ""),
                str(preset.get("family") or ""),
            ]
        )
    for slot_payload in slots.values():
        if not isinstance(slot_payload, dict):
            continue
        selected = str(slot_payload.get("selected") or "")
        if selected:
            values.append(selected)
        for candidate in slot_payload.get("candidates") or []:
            if not isinstance(candidate, dict):
                continue
            values.extend(
                [
                    str(candidate.get("id") or ""),
                    str(candidate.get("entry_id") or ""),
                    str(candidate.get("label_en") or ""),
                    str(candidate.get("label_ko") or ""),
                    " ".join(normalize_list(candidate.get("tags"))),
                    " ".join(normalize_list(candidate.get("kind"))),
                ]
            )
    return " ".join(value for value in values if value.strip())


def candidate_pack_integration_source_corpus(
    result: JsonDict,
    trace: JsonDict,
    mandatory_intents: Sequence[JsonDict],
) -> str:
    provenance = result.get("provenance") if isinstance(result.get("provenance"), dict) else {}
    values: List[str] = [
        str(result.get("preset_id") or ""),
        str(provenance.get("preset_id") or ""),
        str(trace.get("intent") or ""),
    ]
    values.extend(normalize_list(provenance.get("concept_lock")))
    values.extend(normalize_list(provenance.get("additional_requirements")))
    for intent in mandatory_intents:
        if not isinstance(intent, dict):
            continue
        values.append(str(intent.get("text") or ""))
        values.append(str(intent.get("source_text") or ""))
    return " ".join(value for value in values if value.strip())


def candidate_pack_quality_layers(data: JsonDict) -> JsonDict:
    quality = data.get(QUALITY_LAYERS_DATA_KEY)
    return quality if isinstance(quality, dict) else {}


def selection_balance_request_text(
    semantic_context: Optional[JsonDict],
    generation_contract: Optional[JsonDict],
) -> str:
    values = [str((semantic_context or {}).get("intent") or "")]
    values.extend(normalize_list((generation_contract or {}).get("concept_locks")))
    values.extend(normalize_list((generation_contract or {}).get("user_mandatory_intents")))
    return " ".join(values).lower()


def selection_balance_multiplier(data: JsonDict, entry: JsonDict, request_text: str) -> tuple[float, List[str]]:
    policy = candidate_pack_quality_layers(data).get("selection_balance")
    if not isinstance(policy, dict):
        return 1.0, []
    try:
        implicit_multiplier = float(policy.get("implicit_theme_multiplier", 0.35))
    except (TypeError, ValueError):
        implicit_multiplier = 0.35
    implicit_multiplier = min(max(implicit_multiplier, 0.0), 1.0)
    blob = candidate_pack_entry_blob(entry)
    matched: List[str] = []
    for theme, raw_terms in (policy.get("themes") or {}).items():
        terms = [str(term).lower() for term in normalize_list(raw_terms) if str(term).strip()]
        if not terms or not any(term in blob for term in terms):
            continue
        if any(term in request_text for term in terms):
            continue
        matched.append(str(theme))
    return (implicit_multiplier ** len(matched) if matched else 1.0), matched


def candidate_pack_intent_term_is_negated(text: str, term: str) -> bool:
    lowered = str(text or "").lower()
    normalized = str(term or "").lower().strip()
    if not normalized:
        return False
    if normalized.isascii():
        return bool(
            re.search(
                rf"\b(?:no|not|without)\b[^,;.]{{0,48}}(?<![a-z0-9]){re.escape(normalized)}(?![a-z0-9])",
                lowered,
            )
        )
    return bool(re.search(rf"{re.escape(normalized)}[^,;.]{{0,12}}(?:없는|없이|아닌)", lowered))


def request_relevance_match_terms(entry: JsonDict, request_text: str, minimum_length: int) -> List[str]:
    blob = candidate_pack_entry_blob(
        entry,
        [
            *normalize_list(entry.get("for_any")),
            *normalize_list(entry.get("requires_any_tags")),
            *normalize_list(entry.get("requires_primary_any_tags")),
        ],
    )
    matched: List[str] = []
    for term in candidate_pack_tokenize_intent_text(request_text):
        normalized = str(term).lower().strip()
        if len(normalized) < minimum_length or candidate_pack_intent_term_is_negated(request_text, normalized):
            continue
        if normalized in blob and normalized not in matched:
            matched.append(normalized)
    return matched


def apply_rule_request_relevance_bias(
    slot: str,
    pool: Sequence[Entry],
    data: JsonDict,
    generation_contract: Optional[JsonDict],
) -> List[Entry]:
    balance = candidate_pack_quality_layers(data).get("selection_balance")
    policy = balance.get("request_relevance") if isinstance(balance, dict) else None
    if not isinstance(policy, dict) or policy.get("enabled") is not True:
        return list(pool)
    request_text = selection_balance_request_text(None, generation_contract)
    if not request_text.strip():
        return list(pool)
    try:
        per_term = float(policy.get("per_term_multiplier", 2.0))
        max_multiplier = float(policy.get("max_multiplier", 12.0))
        minimum_length = max(2, int(policy.get("minimum_term_length", 3)))
    except (TypeError, ValueError):
        return list(pool)

    adjusted: List[Entry] = []
    boosted: List[JsonDict] = []
    for item in pool:
        matched = request_relevance_match_terms(item, request_text, minimum_length)
        if not matched:
            adjusted.append(item)
            continue
        factor = min(max_multiplier, 1.0 + per_term * len(matched))
        copied = dict(item)
        copied["weight"] = round(item_base_weight(item) * factor, 6)
        copied["request_relevance"] = {"multiplier": factor, "matched_terms": matched}
        adjusted.append(copied)
        boosted.append(
            {
                "id": str(item.get("id") or ""),
                "factor": round(factor, 4),
                "matched_terms": matched,
            }
        )
    if boosted:
        record_generation_contract_event(
            generation_contract,
            "request_relevance_bias",
            {
                "slot": slot,
                "reason": "explicit_request_term_match",
                "reason_code": "explicit_request_term_match",
                "boosted": boosted,
            },
        )
    return adjusted


def rule_request_relevance_choice(
    slot: str,
    pool: Sequence[Entry],
    data: JsonDict,
    generation_contract: Optional[JsonDict],
) -> Optional[Entry]:
    balance = candidate_pack_quality_layers(data).get("selection_balance")
    policy = balance.get("request_relevance") if isinstance(balance, dict) else None
    if not isinstance(policy, dict) or policy.get("enabled") is not True:
        return None
    try:
        minimum_matches = max(1, int(policy.get("deterministic_minimum_matches", 2)))
        minimum_lead = max(1, int(policy.get("deterministic_minimum_lead", 2)))
    except (TypeError, ValueError):
        return None
    ranked: List[tuple[int, str, Entry]] = []
    for item in pool:
        metadata = item.get("request_relevance") if isinstance(item.get("request_relevance"), dict) else {}
        matched = normalize_list(metadata.get("matched_terms"))
        ranked.append((len(matched), str(item.get("id") or ""), item))
    ranked.sort(key=lambda row: (-row[0], row[1]))
    if not ranked or ranked[0][0] < minimum_matches:
        return None
    runner_up = ranked[1][0] if len(ranked) > 1 else 0
    if ranked[0][0] - runner_up < minimum_lead:
        return None
    selected = ranked[0][2]
    record_generation_contract_event(
        generation_contract,
        "request_relevance_selection",
        {
            "slot": slot,
            "reason": "explicit_request_unique_lexical_lead",
            "reason_code": "explicit_request_unique_lexical_lead",
            "selected_id": str(selected.get("id") or ""),
            "matched_count": ranked[0][0],
            "runner_up_count": runner_up,
        },
    )
    return selected


def apply_selection_balance_bias(
    pool: Sequence[JsonDict],
    data: JsonDict,
    semantic_context: Optional[JsonDict],
    generation_contract: Optional[JsonDict],
) -> List[JsonDict]:
    request_text = selection_balance_request_text(semantic_context, generation_contract)
    balanced: List[JsonDict] = []
    for entry in pool:
        multiplier, matched = selection_balance_multiplier(data, entry, request_text)
        if multiplier >= 1.0:
            balanced.append(entry)
            continue
        cloned = dict(entry)
        try:
            cloned["weight"] = float(entry.get("weight", 1) or 1) * multiplier
        except (TypeError, ValueError):
            cloned["weight"] = multiplier
        cloned["selection_balance"] = {"multiplier": multiplier, "implicit_themes": matched}
        balanced.append(cloned)
    return balanced


def candidate_pack_quality_facet_vocab(data: JsonDict) -> Dict[str, Set[str]]:
    vocab: Dict[str, Set[str]] = {
        str(key): {str(item) for item in normalize_list(values)}
        for key, values in DEFAULT_FACET_VOCAB.items()
    }
    for key, values in (data.get("facet_vocab") or {}).items():
        vocab.setdefault(str(key), set()).update(str(item) for item in normalize_list(values))
    return vocab


def candidate_pack_photographic_policy(data: JsonDict) -> JsonDict:
    policy = candidate_pack_quality_layers(data).get("photographic_integration")
    return policy if isinstance(policy, dict) else {}


def candidate_pack_visual_policy(data: JsonDict) -> JsonDict:
    policy = candidate_pack_quality_layers(data).get("visual_proposition")
    return policy if isinstance(policy, dict) else {}


def candidate_pack_photographic_craft_policy(data: JsonDict) -> JsonDict:
    policy = candidate_pack_quality_layers(data).get("photographic_craft")
    if not isinstance(policy, dict) or policy.get("enabled") is False:
        return {}
    return policy


def artistic_final_touch_policy(data: JsonDict) -> JsonDict:
    policy = candidate_pack_quality_layers(data).get("artistic_final_touch")
    if not isinstance(policy, dict) or policy.get("enabled") is False:
        return {}
    return policy


def artistic_final_touch_sentence(
    data: JsonDict,
    lang: str,
    detail_level: str = "detailed",
    quality_profile_id: str = "general",
) -> str:
    policy = artistic_final_touch_policy(data)
    enabled_profiles = set(normalize_list(policy.get("enabled_profiles")))
    if enabled_profiles and quality_profile_id not in enabled_profiles:
        return ""
    if not enabled_profiles and not bool(policy.get("default_enabled", True)):
        return ""
    sentences = policy.get("sentences") if isinstance(policy.get("sentences"), dict) else {}
    localized = sentences.get(lang) if isinstance(sentences.get(lang), dict) else {}
    sentence = str(localized.get(detail_level) or localized.get("default") or "").strip()
    return ensure_period(sentence) if sentence else ""


def candidate_pack_artistic_final_touch(data: JsonDict, quality_profile: JsonDict) -> JsonDict:
    policy = artistic_final_touch_policy(data)
    if not policy:
        return {"enabled": False}
    profile_id = str(quality_profile.get("profile_id") or "general")
    final_sentence = artistic_final_touch_sentence(data, "en", "detailed", profile_id)
    if not final_sentence:
        return {"enabled": False, "profile_id": profile_id}
    return {
        "enabled": True,
        "profile_id": profile_id,
        "source": str(policy.get("source") or "quality_layers_artistic_final_touch"),
        "final_sentence_en": final_sentence,
        "audit_terms": normalize_list(policy.get("audit_terms"))[:12],
    }


def candidate_pack_quality_add_facet(
    facets: Dict[str, Set[str]],
    vocab: Dict[str, Set[str]],
    key: str,
    values: Any,
) -> None:
    if key not in vocab:
        return
    for value in normalize_list(values):
        if value in vocab[key]:
            facets.setdefault(key, set()).add(value)


QUALITY_TAG_FACET_SOURCE_SLOTS: Dict[str, Set[str]] = {
    "subject_kind": {"subject"},
    "place_type": {"subject", "location"},
    "time_of_day": {"time_of_day", "weather", "lighting", "location"},
    "weather": {"weather", "location"},
    "lighting_family": {"lighting"},
    "mood_family": {"mood", "genre"},
    "camera_register": {"medium", "camera_type", "capture_context"},
    "shot_scale": {"shot_scale", "composition"},
    "camera_angle": {"camera_direction", "composition"},
    "placement": {"composition", "platform_framing"},
    "platform_frame": {"composition", "platform_framing"},
    "relation_type": {"action", "relational_action", "procedure_step", "motion"},
    "event_phase": {"action", "procedure_step", "capture_context"},
    "process_stage": {"action", "procedure_step", "capture_context", "prop"},
    "capture_modality": {"medium", "camera_type", "capture_context"},
    "weather_effect": {"weather", "motion", "location"},
    "movement_type": {"action", "motion"},
    "acquisition_structure": {"capture_context", "procedure_step", "composition"},
    "record_basis": {"subject", "capture_context", "procedure_step"},
    "movement_phase": {"action", "motion", "procedure_step"},
    "contact_state": {"action", "contact_point", "motion", "prop"},
    "effort_state": {"action", "body_pose", "motion"},
    "material_response": {"surface_material", "texture", "motion", "prop"},
    "learning_stage": {"action", "procedure_step", "relational_action", "capture_context"},
    "material_lifecycle_stage": {"subject", "action", "procedure_step", "capture_context"},
    "material_state_evidence": {"subject", "surface_material", "prop", "capture_context"},
    "atmospheric_class": {"subject", "weather", "capture_context"},
    "phenomenon_process": {"weather", "action", "procedure_step"},
    "observation_interval": {"capture_context", "procedure_step", "space_condition"},
    "robot_form": {"subject"},
    "robot_degree": {"subject"},
    "robot_proof_family": {"subject"},
    "robot_metaphor": {"subject"},
    "robot_condition": {"subject"},
}
STRICT_TAG_FACET_SOURCE_DOMAINS = {
    "science_inspection",
    "mobility_logistics",
    "climate_adaptation",
    "biodiversity_monitoring",
    "agriculture_food_systems",
    "circular_materials",
    "heritage_documentation",
    "health_access",
    "sports_motion",
    "education_training",
    "disaster_risk_operations",
    "human_interaction",
    "natural_process",
    "longitudinal_place_state",
    "visual_structure",
    "subculture_practice",
    "worldbuilding_system",
    "cjk_narrative_world",
    "character_moe_grammar",
}

# These packs are deliberately broad in subject matter but operationally
# specific. Keep them out of unrelated random/concept preset pools unless the
# user's semantic intent names the domain; an explicit ``--preset`` continues
# to bypass this automatic-discovery scope.
INTENT_SCOPED_PRESET_DOMAINS = {
    "biodiversity_monitoring",
    "agriculture_food_systems",
    "circular_materials",
    "heritage_documentation",
    "health_access",
    "sports_motion",
    "education_training",
    "disaster_risk_operations",
    "human_interaction",
    "natural_process",
    "longitudinal_place_state",
    "visual_structure",
    "subculture_practice",
    "worldbuilding_system",
    "cjk_narrative_world",
    "character_moe_grammar",
}

# Slot entries in the new packs already carry one of these authored tags. The
# mapping prevents a generic overlap such as ``food`` or ``documentary`` from
# making a fermentation batch or camera-trap record eligible in a legacy
# portrait, while preserving direct preset filters and semantic discovery.
INTENT_SCOPED_ENTRY_DOMAIN_TAGS = {
    "biodiversity": "biodiversity_monitoring",
    "agriculture_food_systems": "agriculture_food_systems",
    "circular_materials": "circular_materials",
    "heritage_documentation": "heritage_documentation",
    "health_access": "health_access",
    "sports_motion": "sports_motion",
    "education_training": "education_training",
    "disaster_risk_operations": "disaster_risk_operations",
    "natural_process": "natural_process",
    "longitudinal_place_state": "longitudinal_place_state",
    "visual_structure": "visual_structure",
    "subculture_practice": "subculture_practice",
    "worldbuilding_system": "worldbuilding_system",
    "cjk_narrative_world": "cjk_narrative_world",
    "character_moe_grammar": "character_moe_grammar",
}


def candidate_pack_quality_inferred_tag_facet_keys(
    vocab: Dict[str, Set[str]],
    slot: str,
    strict: bool = False,
) -> Set[str]:
    """Limit implicit tag-to-facet inference for migrated typed domains.

    Explicit ``facets`` remain valid on every entry. The slot boundary only
    prevents incidental tokens such as ``street`` in a focus-mode tag from
    being misread as the scene's actual place type. Legacy domains retain
    their historical inference until their dictionaries are facet-migrated.
    """
    allowed = set(vocab)
    if not strict:
        return allowed
    for facet_key, source_slots in QUALITY_TAG_FACET_SOURCE_SLOTS.items():
        if slot not in source_slots:
            allowed.discard(facet_key)
    return allowed


def candidate_pack_quality_add_entry_facets(
    facets: Dict[str, Set[str]],
    vocab: Dict[str, Set[str]],
    entry: JsonDict,
    inferred_tag_facet_keys: Optional[Set[str]] = None,
    include_subject_kind: bool = True,
) -> None:
    raw_facets = entry.get("facets") if isinstance(entry.get("facets"), dict) else {}
    for key, values in raw_facets.items():
        if key == "subject_kind" and not include_subject_kind:
            continue
        candidate_pack_quality_add_facet(facets, vocab, str(key), values)
    if include_subject_kind:
        candidate_pack_quality_add_facet(facets, vocab, "subject_kind", entry.get("kind"))
    for token in normalize_list(entry.get("tags")) + normalize_list(entry.get("kind")):
        for key, allowed in vocab.items():
            if key == "subject_kind" and not include_subject_kind:
                continue
            if inferred_tag_facet_keys is not None and key not in inferred_tag_facet_keys:
                continue
            if token in allowed:
                facets.setdefault(key, set()).add(token)


def candidate_pack_quality_entry_match_blob(entry: JsonDict) -> str:
    values: List[str] = []
    for key in ("id", "en", "ko", "label_en", "label_ko", "keywords", "aliases"):
        raw = entry.get(key)
        if isinstance(raw, list):
            values.extend(str(item) for item in raw if str(item).strip())
        elif raw is not None and str(raw).strip():
            values.append(str(raw))
    return " ".join(values).lower()


def candidate_pack_quality_dictionary_entries(data: JsonDict) -> Iterator[JsonDict]:
    for preset in data.get("presets", []) or []:
        if isinstance(preset, dict):
            yield preset
    slots = data.get("slots") if isinstance(data.get("slots"), dict) else {}
    for entries in slots.values():
        for entry in entries or []:
            if isinstance(entry, dict):
                yield entry


def candidate_pack_quality_add_intent_facets(
    facets: Dict[str, Set[str]],
    vocab: Dict[str, Set[str]],
    data: JsonDict,
    mandatory_intents: Sequence[JsonDict],
) -> List[str]:
    del data  # Intent facets are literal; unrelated dictionary rows must not influence the profile.
    aliases: Dict[str, Dict[str, str]] = {
        "subject_kind": {
            "person": "human",
            "people": "human",
            "portrait": "human",
            "인물": "human",
            "사람": "human",
            "animal": "animal",
            "wildlife": "animal",
            "동물": "animal",
            "food": "food",
            "meal": "food",
            "dish": "food",
            "음식": "food",
            "product": "object",
            "object": "object",
            "제품": "object",
            "plant": "plant",
            "식물": "plant",
            "robot": "robot",
            "로봇": "robot",
        },
        "mood_family": {
            "documentary": "documentary",
            "다큐멘터리": "documentary",
            "commercial": "commercial",
            "광고": "commercial",
            "romantic": "romantic",
            "surreal": "surreal",
            "nostalgic": "nostalgic",
        },
        "place_type": {
            "street": "street",
            "거리": "street",
            "studio": "studio",
            "스튜디오": "studio",
            "nature": "nature",
            "자연": "nature",
            "interior": "interior",
            "실내": "interior",
        },
    }
    matched: List[str] = []
    for intent in mandatory_intents:
        if intent.get("status") != "uncovered":
            continue
        term = str(intent.get("text") or "").strip().lower()
        if not term:
            continue
        normalized_term = re.sub(r"[_/-]+", " ", term).strip()
        for facet_key, facet_aliases in aliases.items():
            value = facet_aliases.get(normalized_term)
            if value not in vocab.get(facet_key, set()):
                continue
            facets.setdefault(facet_key, set()).add(value)
            marker = f"{facet_key}:{value}"
            if marker not in matched:
                matched.append(marker)
    return matched


def candidate_pack_quality_add_literal_subject_entity_facets(
    facets: Dict[str, Set[str]],
    vocab: Dict[str, Set[str]],
    data: JsonDict,
    mandatory_intents: Sequence[JsonDict],
) -> List[str]:
    """Infer secondary visible subject kinds only from literal subject labels.

    Keywords and tags are intentionally excluded: a generic word such as
    "styling" must not turn a portrait into a food profile merely because it
    appears in an unrelated subject entry's retrieval metadata.
    """
    subject_entries = ((data.get("slots") or {}).get("subject") or [])
    routing_policy = candidate_pack_intent_routing_policy(data)
    stop_terms = {
        str(value).strip().lower()
        for value in normalize_list(routing_policy.get("literal_subject_stop_terms"))
        if str(value).strip()
    }
    matched_entry_ids: List[str] = []
    for intent in mandatory_intents:
        term = str(intent.get("text") or "").strip().lower()
        if not term or term in stop_terms or intent_explicitly_excludes_people(term):
            continue
        for entry in subject_entries:
            if not isinstance(entry, dict):
                continue
            values: List[str] = []
            for key in ("id", "en", "ko", "aliases"):
                raw = entry.get(key)
                values.extend(normalize_list(raw) if isinstance(raw, list) else [str(raw or "")])
            label_blob = " ".join(value for value in values if value.strip()).lower()
            if not candidate_pack_integration_text_has_term(label_blob, term):
                continue
            before = set(facets.get("subject_kind", set()))
            raw_facets = entry.get("facets") if isinstance(entry.get("facets"), dict) else {}
            candidate_pack_quality_add_facet(
                facets,
                vocab,
                "subject_kind",
                raw_facets.get("subject_kind"),
            )
            candidate_pack_quality_add_facet(facets, vocab, "subject_kind", entry.get("kind"))
            candidate_pack_quality_add_facet(facets, vocab, "subject_kind", entry.get("tags"))
            if set(facets.get("subject_kind", set())) == before:
                continue
            entry_id = str(entry.get("id") or "")
            if entry_id and entry_id not in matched_entry_ids:
                matched_entry_ids.append(entry_id)
            if len(matched_entry_ids) >= 12:
                return matched_entry_ids
    return matched_entry_ids


def candidate_pack_quality_profile_id(data: JsonDict, preset: JsonDict, facets: Dict[str, Set[str]]) -> str:
    domains = preset_domains(preset, data)
    subject_kinds = facets.get("subject_kind", set())
    mood_families = facets.get("mood_family", set())
    blob = candidate_pack_quality_entry_match_blob(preset)
    if "science_inspection" in domains:
        return "science_inspection"
    if "mobility_logistics" in domains:
        return "mobility_logistics"
    if "climate_adaptation" in domains:
        return "climate_adaptation"
    if "biodiversity_monitoring" in domains:
        return "biodiversity_monitoring"
    if "agriculture_food_systems" in domains:
        return "agriculture_food_systems"
    if "circular_materials" in domains:
        return "circular_materials"
    if "heritage_documentation" in domains:
        return "heritage_documentation"
    if "health_access" in domains:
        return "health_access"
    if "sports_motion" in domains:
        return "sports_motion"
    if "education_training" in domains:
        return "education_training"
    if "disaster_risk_operations" in domains:
        return "disaster_risk_operations"
    if "human_interaction" in domains:
        return "documentary"
    if "natural_process" in domains:
        return "natural_process"
    if "longitudinal_place_state" in domains:
        return "longitudinal_place_state"
    if "visual_structure" in domains:
        return "visual_structure"
    if "cjk_narrative_world" in domains:
        return "cjk_narrative_world"
    if "character_moe_grammar" in domains:
        return "character_moe_grammar"
    if "food" in subject_kinds or "food" in domains:
        return "food"
    if "architecture" in domains or "real_estate" in domains or any(term in blob for term in ("architecture", "interior", "building")):
        return "architecture"
    if subject_kinds & {"object", "sign"} or domains & {"product", "jewelry"}:
        return "product"
    if domains & {"wildlife", "landscape", "nature"} or subject_kinds & {"animal", "plant", "environment"}:
        return "nature"
    if "documentary" in domains:
        return "documentary"
    if domains & {"portrait", "fashion", "beauty", "editorial"}:
        return "portrait_editorial"
    if "documentary" in mood_families or any(term in blob for term in ("documentary", "candid", "reportage", "street")):
        return "documentary"
    if "human" in subject_kinds:
        return "portrait_editorial"
    return "general"


def candidate_pack_quality_profile(
    data: JsonDict,
    result: JsonDict,
    slots: JsonDict,
    mandatory_intents: Sequence[JsonDict],
) -> JsonDict:
    vocab = candidate_pack_quality_facet_vocab(data)
    facets: Dict[str, Set[str]] = {}
    preset_id = str((result.get("provenance") or {}).get("preset_id") or result.get("preset_id") or "")
    preset = candidate_pack_preset_by_id(data, preset_id) if preset_id else None
    if isinstance(preset, dict):
        candidate_pack_quality_add_entry_facets(facets, vocab, preset, include_subject_kind=False)
    strict_tag_facet_sources = bool(
        isinstance(preset, dict)
        and preset_domains(preset, data) & STRICT_TAG_FACET_SOURCE_DOMAINS
    )

    choices = result.get("choices") if isinstance(result.get("choices"), dict) else {}
    for slot, choice in choices.items():
        if isinstance(choice, dict):
            candidate_pack_quality_add_entry_facets(
                facets,
                vocab,
                choice,
                inferred_tag_facet_keys=candidate_pack_quality_inferred_tag_facet_keys(
                    vocab, str(slot), strict=strict_tag_facet_sources
                ),
                include_subject_kind=str(slot) == "subject",
            )

    for slot, slot_payload in slots.items():
        if not isinstance(slot_payload, dict):
            continue
        entry_id = candidate_pack_slot_selected_entry_id(slot_payload)
        if not entry_id:
            continue
        entry = candidate_pack_selected_choice_entry(result, str(slot), entry_id)
        # Rendered ``choices`` intentionally contain a compact public subset
        # and may omit dictionary-only facets. Always prefer the canonical
        # entry when building the internal quality profile so data-authored
        # lighting/material/place facets are not silently discarded.
        entry = candidate_pack_slot_entry_by_id(data, str(slot), entry_id) or entry
        if isinstance(entry, dict):
            candidate_pack_quality_add_entry_facets(
                facets,
                vocab,
                entry,
                inferred_tag_facet_keys=candidate_pack_quality_inferred_tag_facet_keys(
                    vocab, str(slot), strict=strict_tag_facet_sources
                ),
                include_subject_kind=str(slot) == "subject",
            )

    matched_facets = candidate_pack_quality_add_intent_facets(facets, vocab, data, mandatory_intents)
    profile_id = candidate_pack_quality_profile_id(data, preset or {}, facets)
    matched_subject_entries = candidate_pack_quality_add_literal_subject_entity_facets(
        facets,
        vocab,
        data,
        mandatory_intents,
    )
    return {
        "profile_id": profile_id,
        "source": "selected_preset_slots_and_literal_uncovered_intent_facets",
        "facets": {key: sorted(values) for key, values in sorted(facets.items()) if values},
        "matched_uncovered_intent_facets": matched_facets,
        "matched_literal_subject_entries": matched_subject_entries,
    }


def candidate_pack_quality_facet_hits(quality_profile: JsonDict, facet_match: Any) -> List[str]:
    if not isinstance(facet_match, dict) or not facet_match:
        return []
    profile_facets = quality_profile.get("facets") if isinstance(quality_profile.get("facets"), dict) else {}
    hits: List[str] = []
    for key, values in facet_match.items():
        profile_values = {str(item) for item in normalize_list(profile_facets.get(str(key)))}
        wanted = {str(item) for item in normalize_list(values)}
        for value in sorted(profile_values & wanted):
            hits.append(f"{key}:{value}")
    return hits


def candidate_pack_quality_profile_matches(quality_profile: JsonDict, profile_match: Any) -> bool:
    """Return whether an optional quality-layer profile guard applies.

    Facets remain the reusable matching surface, while ``profile_match`` keeps
    domain-specific axes and craft refinements from changing established
    profiles that happen to share generic facets such as ``nature`` or
    ``inspection``.
    """
    expected = {str(item) for item in normalize_list(profile_match) if str(item).strip()}
    if not expected:
        return True
    return str(quality_profile.get("profile_id") or "") in expected


def candidate_pack_quality_profile_from_selected(
    data: JsonDict,
    preset: JsonDict,
    picked: Dict[str, Entry],
) -> JsonDict:
    vocab = candidate_pack_quality_facet_vocab(data)
    facets: Dict[str, Set[str]] = {}
    candidate_pack_quality_add_entry_facets(facets, vocab, preset, include_subject_kind=False)
    strict_tag_facet_sources = bool(
        preset_domains(preset, data) & STRICT_TAG_FACET_SOURCE_DOMAINS
    )
    for slot, entry in picked.items():
        if isinstance(entry, dict):
            candidate_pack_quality_add_entry_facets(
                facets,
                vocab,
                entry,
                inferred_tag_facet_keys=candidate_pack_quality_inferred_tag_facet_keys(
                    vocab, str(slot), strict=strict_tag_facet_sources
                ),
                include_subject_kind=str(slot) == "subject",
            )
    return {
        "profile_id": candidate_pack_quality_profile_id(data, preset, facets),
        "source": "selected_preset_slots",
        "facets": {key: sorted(values) for key, values in sorted(facets.items()) if values},
        "matched_uncovered_intent_facets": [],
        "matched_literal_subject_entries": [],
    }


def candidate_pack_craft_text(raw: Any, lang: str) -> str:
    if isinstance(raw, dict):
        return str(raw.get(lang) or raw.get("en") or raw.get("default") or "").strip()
    return str(raw or "").strip()


def candidate_pack_photographic_craft(
    data: JsonDict,
    quality_profile: JsonDict,
) -> JsonDict:
    policy = candidate_pack_photographic_craft_policy(data)
    if not policy:
        return {"enabled": False}
    dimensions = [dimension for dimension in policy.get("dimensions", []) or [] if isinstance(dimension, dict)]
    if not dimensions:
        return {"enabled": False}
    try:
        refinement_limit = int(policy.get("refinement_limit_per_dimension", 2) or 2)
    except (TypeError, ValueError):
        refinement_limit = 2
    refinement_limit = max(0, min(refinement_limit, 4))

    active_dimensions: List[JsonDict] = []
    dimension_scores: Dict[str, int] = {}
    dimension_facets: Dict[str, List[str]] = {}
    matched_facets: List[str] = []
    all_audit_terms: List[str] = []
    for dimension in dimensions:
        dimension_id = str(dimension.get("id") or "").strip()
        if not dimension_id:
            continue
        scored_refinements: List[tuple[int, str, JsonDict, List[str]]] = []
        for refinement in dimension.get("refinements", []) or []:
            if not isinstance(refinement, dict):
                continue
            refinement_id = str(refinement.get("id") or "").strip()
            if not refinement_id:
                continue
            if not candidate_pack_quality_profile_matches(quality_profile, refinement.get("profile_match")):
                continue
            facet_hits = candidate_pack_quality_facet_hits(quality_profile, refinement.get("facet_match"))
            if not facet_hits:
                continue
            scored_refinements.append((len(facet_hits), refinement_id, refinement, facet_hits))
        scored_refinements.sort(key=lambda item: (-item[0], item[1]))

        active_refinements: List[JsonDict] = []
        selected_principle = str(dimension.get("baseline_principle") or "").strip()
        selected_guidance_en = candidate_pack_craft_text(dimension.get("guidance"), "en")
        selected_guidance_ko = candidate_pack_craft_text(dimension.get("guidance"), "ko")
        dimension_score = 0
        dimension_hits: List[str] = []
        for score, refinement_id, refinement, facet_hits in scored_refinements[:refinement_limit]:
            dimension_score += score
            for hit in facet_hits:
                if hit not in dimension_hits:
                    dimension_hits.append(hit)
                if hit not in matched_facets:
                    matched_facets.append(hit)
            refinement_guidance_en = candidate_pack_craft_text(refinement.get("guidance"), "en")
            refinement_guidance_ko = candidate_pack_craft_text(refinement.get("guidance"), "ko")
            active_refinements.append(
                {
                    "id": refinement_id,
                    "score": score,
                    "matched_facets": facet_hits[:12],
                    "principle": str(refinement.get("principle") or "").strip(),
                    "guidance_en": refinement_guidance_en,
                    "guidance_ko": refinement_guidance_ko,
                    "audit_terms": normalize_list(refinement.get("audit_terms"))[:10],
                }
            )
        if active_refinements:
            primary_refinement = active_refinements[0]
            selected_principle = str(primary_refinement.get("principle") or selected_principle)
            selected_guidance_en = str(primary_refinement.get("guidance_en") or selected_guidance_en)
            selected_guidance_ko = str(primary_refinement.get("guidance_ko") or selected_guidance_ko)

        audit_terms = normalize_list(dimension.get("audit_terms"))[:10]
        for term in audit_terms:
            if term not in all_audit_terms:
                all_audit_terms.append(term)
        for refinement in active_refinements:
            for term in normalize_list(refinement.get("audit_terms")):
                if term not in all_audit_terms:
                    all_audit_terms.append(term)

        dimension_scores[dimension_id] = dimension_score
        dimension_facets[dimension_id] = dimension_hits
        active_dimensions.append(
            {
                "id": dimension_id,
                "label": str(dimension.get("label") or dimension_id),
                "score": dimension_score,
                "matched_facets": dimension_hits[:12],
                "baseline_principle": str(dimension.get("baseline_principle") or "").strip(),
                "selected_principle": selected_principle,
                "guidance_en": candidate_pack_craft_text(dimension.get("guidance"), "en"),
                "guidance_ko": candidate_pack_craft_text(dimension.get("guidance"), "ko"),
                "selected_guidance_en": selected_guidance_en,
                "selected_guidance_ko": selected_guidance_ko,
                "audit_terms": audit_terms,
                "active_refinements": active_refinements,
            }
        )

    dimension_ids = [str(dimension.get("id") or "") for dimension in active_dimensions if dimension.get("id")]
    strategies: List[JsonDict] = []
    for strategy in policy.get("strategies", []) or []:
        if not isinstance(strategy, dict):
            continue
        strategy_id = str(strategy.get("id") or "").strip()
        if not strategy_id:
            continue
        if not candidate_pack_quality_profile_matches(quality_profile, strategy.get("profile_match")):
            continue
        emphasize = [
            str(dimension_id)
            for dimension_id in normalize_list(strategy.get("emphasize"))
            if str(dimension_id) in dimension_ids
        ]
        if not emphasize:
            continue
        strategy_facets: List[str] = []
        for dimension_id in emphasize:
            for hit in dimension_facets.get(dimension_id, []):
                if hit not in strategy_facets:
                    strategy_facets.append(hit)
        strategies.append(
            {
                "id": strategy_id,
                "label": str(strategy.get("label") or strategy_id),
                "score": sum(dimension_scores.get(dimension_id, 0) for dimension_id in emphasize),
                "emphasize": emphasize,
                "matched_facets": strategy_facets[:12],
            }
        )
    default_strategy = str(policy.get("default_strategy") or "").strip()
    if strategies:
        if all(int(strategy.get("score", 0)) <= 0 for strategy in strategies) and default_strategy:
            strategies.sort(key=lambda strategy: (0 if strategy.get("id") == default_strategy else 1, str(strategy.get("id") or "")))
        else:
            strategies.sort(key=lambda strategy: (-int(strategy.get("score", 0)), str(strategy.get("id") or "")))
    else:
        strategies = [
            {
                "id": default_strategy or "structure_led",
                "label": default_strategy or "structure_led",
                "score": 0,
                "emphasize": dimension_ids[:2],
                "matched_facets": [],
            }
        ]

    try:
        prompt_dimension_limit = int(policy.get("prompt_dimension_limit", 2) or 2)
    except (TypeError, ValueError):
        prompt_dimension_limit = 2
    prompt_dimension_limit = max(1, min(prompt_dimension_limit, 3))
    top_strategy = strategies[0]
    prompt_dimension_ids = [dimension_id for dimension_id in top_strategy.get("emphasize", []) if dimension_id in dimension_ids]
    if not prompt_dimension_ids:
        prompt_dimension_ids = dimension_ids[:prompt_dimension_limit]
    prompt_dimension_ids = prompt_dimension_ids[:prompt_dimension_limit]
    by_dimension = {str(dimension.get("id")): dimension for dimension in active_dimensions}
    prompt_guidance_en = [
        str(by_dimension[dimension_id].get("selected_guidance_en") or "").strip()
        for dimension_id in prompt_dimension_ids
        if dimension_id in by_dimension and str(by_dimension[dimension_id].get("selected_guidance_en") or "").strip()
    ]
    prompt_guidance_ko = [
        str(by_dimension[dimension_id].get("selected_guidance_ko") or "").strip()
        for dimension_id in prompt_dimension_ids
        if dimension_id in by_dimension and str(by_dimension[dimension_id].get("selected_guidance_ko") or "").strip()
    ]
    return {
        "enabled": True,
        "source": str(policy.get("source") or "facet_only_photographer_decision_layer"),
        "quality_profile": quality_profile,
        "selection_mode": "facet_only",
        "active_dimensions": active_dimensions,
        "matched_facets": matched_facets[:20],
        "top_strategy": top_strategy,
        "strategy_variants": strategies[:3],
        "prompt_dimension_ids": prompt_dimension_ids,
        "prompt_guidance_en": list(dict.fromkeys(prompt_guidance_en))[:prompt_dimension_limit],
        "prompt_guidance_ko": list(dict.fromkeys(prompt_guidance_ko))[:prompt_dimension_limit],
        "audit_terms": all_audit_terms[:40],
    }


def photographic_craft_sentence_from_pack(craft: JsonDict, lang: str, detail_level: str) -> str:
    if not isinstance(craft, dict) or not craft.get("enabled", True):
        return ""
    guidance_key = "prompt_guidance_ko" if lang == "ko" else "prompt_guidance_en"
    guidance = normalize_list(craft.get(guidance_key))
    if not guidance and lang != "en":
        guidance = normalize_list(craft.get("prompt_guidance_en"))
    if not guidance:
        return ""
    limit = 1 if detail_level == "compact" else 2
    guidance = guidance[:limit]
    if lang == "ko":
        return ensure_period("사진가의 촬영 판단으로 " + "; ".join(guidance))
    return ensure_period("Frame it with clear photographic intent: " + "; ".join(guidance))


def photographic_craft_sentence(
    data: JsonDict,
    preset: JsonDict,
    picked: Dict[str, Entry],
    lang: str,
    detail_level: str,
) -> str:
    if not candidate_pack_photographic_craft_policy(data):
        return ""
    quality_profile = candidate_pack_quality_profile_from_selected(data, preset, picked)
    craft = candidate_pack_photographic_craft(data, quality_profile)
    return photographic_craft_sentence_from_pack(craft, lang, detail_level)


def append_photographic_craft(
    data: JsonDict,
    prompt: str,
    preset: JsonDict,
    picked: Dict[str, Entry],
    lang: str,
    detail_level: str,
) -> str:
    sentence = photographic_craft_sentence(data, preset, picked, lang, detail_level)
    if not sentence:
        return clean_spaces(prompt)
    prompt_clean = clean_spaces(prompt)
    if sentence.lower() in prompt_clean.lower():
        return prompt_clean
    word_budget = {"compact": 120, "standard": 150, "detailed": 190}.get(detail_level, 150)
    if lang == "en" and len(f"{prompt_clean} {sentence}".split()) > word_budget:
        return prompt_clean
    return clean_spaces(f"{prompt_clean} {sentence}")


def candidate_pack_quality_matched_terms(text: str, terms: Any) -> List[str]:
    return [
        str(term)
        for term in normalize_list(terms)
        if candidate_pack_integration_text_has_term(text, str(term))
    ]


def candidate_pack_quality_merge_phrases(
    target: Dict[str, List[str]],
    suggested: Any,
) -> None:
    if not isinstance(suggested, dict):
        return
    for category, phrases in suggested.items():
        values = normalize_list(phrases)
        if not values:
            continue
        bucket = target.setdefault(str(category), [])
        for phrase in values:
            if phrase not in bucket:
                bucket.append(phrase)


def candidate_pack_photographic_integration(
    data: JsonDict,
    result: JsonDict,
    trace: JsonDict,
    presets: Sequence[JsonDict],
    slots: JsonDict,
    mandatory_intents: Sequence[JsonDict],
    quality_profile: JsonDict,
) -> JsonDict:
    corpus = candidate_pack_integration_corpus(result, trace, presets, slots, mandatory_intents)
    source_corpus = candidate_pack_integration_source_corpus(result, trace, mandatory_intents)
    policy = candidate_pack_photographic_policy(data)
    categories = policy.get("categories") if isinstance(policy.get("categories"), dict) else {}
    baseline = policy.get("baseline") if isinstance(policy.get("baseline"), dict) else {}
    axes = [axis for axis in policy.get("axes", []) or [] if isinstance(axis, dict)]

    required_categories = normalize_list(baseline.get("required_categories")) or ["environment_binding", "optical_depth"]
    principles = normalize_list(baseline.get("principles"))
    phrase_budget: Dict[str, List[str]] = {}
    candidate_pack_quality_merge_phrases(phrase_budget, baseline.get("suggested_phrases"))
    active_axes: List[JsonDict] = []
    matched_terms: List[str] = []

    scored_axes: List[tuple[int, int, str, JsonDict, List[str], List[str], List[str]]] = []
    subject_axis_kinds = {
        "person_presence": {"human"},
        "animal_presence": {"animal"},
        "object_or_product_presence": {"object", "food", "plant", "sign"},
    }
    known_subject_kinds = {
        str(value)
        for value in normalize_list((quality_profile.get("facets") or {}).get("subject_kind"))
    }
    for axis in axes:
        axis_id = str(axis.get("id") or "")
        if not candidate_pack_quality_profile_matches(quality_profile, axis.get("profile_match")):
            continue
        if axis_id == "person_presence" and intent_explicitly_excludes_people(source_corpus):
            continue
        facet_hits = candidate_pack_quality_facet_hits(quality_profile, axis.get("facet_match"))
        source_terms = candidate_pack_quality_matched_terms(source_corpus, axis.get("terms"))
        context_terms = candidate_pack_quality_matched_terms(corpus, axis.get("terms"))
        if (
            axis_id in subject_axis_kinds
            and known_subject_kinds
            and not (known_subject_kinds & subject_axis_kinds[axis_id])
            and not source_terms
        ):
            # Candidate alternatives are context, not visible subjects. When a
            # subject kind is known, they cannot invent a second presence axis.
            continue
        score = len(facet_hits) * 10 + len(source_terms) * 3 + len(context_terms)
        if score <= 0:
            continue
        if not facet_hits and not source_terms and len(context_terms) < 2:
            continue
        scored_axes.append((score, len(facet_hits), axis_id, axis, facet_hits, source_terms, context_terms))
    # A typed visible-subject facet and literal request/preset evidence are more
    # authoritative than incidental facets from a sampled optional slot.
    # Ranking raw facet count first allowed an unrelated texture or prop to
    # crowd explicit concepts such as "apple", "stained glass", or "LED wall"
    # out of the bounded axis set.
    scored_axes.sort(
        key=lambda item: (
            -int(item[2] in subject_axis_kinds and bool(item[4])),
            -int(bool(item[5])),
            -len(item[5]),
            -item[1],
            -item[0],
            item[2],
        )
    )

    matched_facets: List[str] = []
    for score, _facet_hit_count, axis_id, axis, facet_hits, source_terms, context_terms in scored_axes[:5]:
        axis_required = normalize_list(axis.get("required_categories"))
        for category in axis_required:
            if category not in required_categories:
                required_categories.append(category)
        for principle in normalize_list(axis.get("principles")):
            if principle not in principles:
                principles.append(principle)
        candidate_pack_quality_merge_phrases(phrase_budget, axis.get("suggested_phrases"))
        axis_terms = (source_terms or context_terms)[:12]
        matched_terms.extend(term for term in axis_terms if term not in matched_terms)
        matched_facets.extend(hit for hit in facet_hits if hit not in matched_facets)
        active_axes.append(
            {
                "id": axis_id,
                "score": score,
                "matched_facets": facet_hits[:12],
                "matched_terms": axis_terms,
                "required_categories": axis_required,
            }
        )

    phrase_budget = {
        category: phrases[:3]
        for category, phrases in phrase_budget.items()
        if phrases
    }
    try:
        minimum_hits = int(baseline.get("minimum_category_hits", 2) or 2)
    except (TypeError, ValueError):
        minimum_hits = 2
    minimum_hits = max(1, min(minimum_hits, len(required_categories)))
    return {
        "enabled": True,
        "profile_id": str(baseline.get("profile_id") or "axis_composite_photo_integration"),
        "source": "quality_layers_axis_composite",
        "active_axes": active_axes,
        "quality_profile": quality_profile,
        "matched_facets": matched_facets[:12],
        "matched_terms": matched_terms[:12],
        "required_categories": required_categories,
        "minimum_category_hits": minimum_hits,
        "principles": principles[:7],
        "suggested_phrases": phrase_budget,
        "category_terms": {
            category: list(terms)
            for category, terms in categories.items()
            if normalize_list(terms)
        },
        "anti_patterns": normalize_list(baseline.get("anti_patterns"))[:5],
    }


def candidate_pack_visual_entry_terms(entry: JsonDict) -> List[str]:
    terms: List[str] = []
    for key in ("id", "en", "ko", "keywords", "aliases", "tags", "embedding_text"):
        raw = entry.get(key)
        if isinstance(raw, list):
            terms.extend(str(item) for item in raw if str(item).strip())
        elif raw is not None and str(raw).strip():
            terms.append(str(raw))
    return list(dict.fromkeys(terms))[:18]


def candidate_pack_visual_subject_blob(result: JsonDict, slots: JsonDict) -> str:
    values: List[str] = []
    choices = result.get("choices") if isinstance(result.get("choices"), dict) else {}
    for slot in ("subject", "appearance_type", "costume_style", "wardrobe_style", "prop", "location", "medium", "genre"):
        choice = choices.get(slot)
        if isinstance(choice, dict):
            values.extend(candidate_pack_visual_entry_terms(choice))
    for slot in ("subject", "appearance_type", "costume_style", "wardrobe_style", "prop", "location"):
        slot_payload = slots.get(slot) if isinstance(slots, dict) else None
        if not isinstance(slot_payload, dict):
            continue
        for candidate in slot_payload.get("candidates") or []:
            if isinstance(candidate, dict):
                values.extend(
                    [
                        str(candidate.get("id") or ""),
                        str(candidate.get("entry_id") or ""),
                        str(candidate.get("label_en") or ""),
                        str(candidate.get("label_ko") or ""),
                        " ".join(normalize_list(candidate.get("tags"))),
                        " ".join(normalize_list(candidate.get("kind"))),
                    ]
                )
    return " ".join(value for value in values if value.strip())


def candidate_pack_visual_subject_classes(
    result: JsonDict,
    slots: JsonDict,
    corpus: str,
    policy: JsonDict,
    quality_profile: JsonDict,
) -> List[JsonDict]:
    subject_blob = candidate_pack_visual_subject_blob(result, slots) or corpus
    scored: List[JsonDict] = []
    for config in policy.get("subject_classes", []) or []:
        if not isinstance(config, dict):
            continue
        class_id = str(config.get("id") or "")
        if not class_id:
            continue
        facet_hits = candidate_pack_quality_facet_hits(quality_profile, config.get("facet_match"))
        term_score = sum(
            1
            for term in normalize_list(config.get("terms"))
            if candidate_pack_integration_text_has_term(subject_blob, term)
        )
        score = len(facet_hits) * 10 + term_score
        if score <= 0:
            continue
        scored.append(
            {
                "id": class_id,
                "score": score,
                "matched_facets": facet_hits[:12],
                "core_policy": str(config.get("core_policy", "allow")),
            }
        )
    scored.sort(key=lambda item: (-int(item.get("score", 0)), str(item.get("id") or "")))
    return scored or [{"id": "general", "score": 0, "core_policy": "allow"}]


def candidate_pack_visual_register(
    subject_classes: Sequence[JsonDict],
    source_corpus: str,
    corpus: str,
    policy: JsonDict,
    quality_profile: JsonDict,
) -> str:
    registers = policy.get("registers") if isinstance(policy.get("registers"), dict) else {}
    charged_policy = registers.get("charged") if isinstance(registers.get("charged"), dict) else {}
    observational_policy = registers.get("observational") if isinstance(registers.get("observational"), dict) else {}
    charged_terms = normalize_list(charged_policy.get("terms"))
    observational_terms = normalize_list(observational_policy.get("terms"))
    source_text_present = bool(source_corpus.strip())
    charged_facet_hits = candidate_pack_quality_facet_hits(quality_profile, charged_policy.get("facet_match"))
    observational_facet_hits = candidate_pack_quality_facet_hits(quality_profile, observational_policy.get("facet_match"))
    charged_source_hits = sum(
        1
        for term in charged_terms
        if candidate_pack_integration_text_has_term(source_corpus, term)
    )
    charged_context_hits = sum(
        1
        for term in charged_terms
        if candidate_pack_integration_text_has_term(corpus, term)
    )
    if charged_source_hits > 0:
        return "charged"
    class_ids = {str(item.get("id") or "") for item in subject_classes}
    if class_ids & {"object_scene", "animal"} and "person" not in class_ids:
        return "observational"
    if charged_facet_hits or (not source_text_present and charged_context_hits >= 2):
        return "charged"
    observational_hits = sum(
        1
        for term in observational_terms
        if candidate_pack_integration_text_has_term(source_corpus, term)
        or candidate_pack_integration_text_has_term(corpus, term)
    )
    if "person" not in class_ids and (observational_facet_hits or observational_hits >= 2) and charged_source_hits == 0:
        return "observational"
    return "understated"


def candidate_pack_visual_entry_score(entry: JsonDict, source_corpus: str, corpus: str, selected_id: str) -> int:
    entry_id = str(entry.get("id") or "")
    terms = candidate_pack_visual_entry_terms(entry)
    score = 0
    if entry_id and entry_id == selected_id:
        score += 20
    for term in terms:
        if candidate_pack_integration_text_has_term(source_corpus, term):
            score += 4
        elif candidate_pack_integration_text_has_term(corpus, term):
            score += 1
    return score


def candidate_pack_visual_fallback_order(entry: JsonDict, slot: str, result: JsonDict, corpus: str, policy: JsonDict) -> str:
    seed = str((result.get("provenance") or {}).get("seed") or "")
    preset = str((result.get("provenance") or {}).get("preset_id") or result.get("preset_id") or "")
    concept = str((result.get("provenance") or {}).get("concept_lock") or corpus)
    entry_id = str(entry.get("id") or "")
    fallback = policy.get("fallback") if isinstance(policy.get("fallback"), dict) else {}
    preferred = normalize_list(fallback.get(slot))
    prefix = "0" if entry_id in preferred else "1"
    return prefix + hashlib.sha256(f"visual-proposition|{seed}|{preset}|{concept}|{slot}|{entry_id}".encode("utf-8")).hexdigest()


def candidate_pack_visual_candidates_for_slot(
    data: JsonDict,
    result: JsonDict,
    slots: JsonDict,
    slot: str,
    source_corpus: str,
    corpus: str,
    policy: JsonDict,
    candidate_limit: int,
) -> List[JsonDict]:
    entries = [entry for entry in data.get("slots", {}).get(slot, []) or [] if isinstance(entry, dict)]
    if not entries:
        return []
    selected_id = ""
    slot_payload = slots.get(slot) if isinstance(slots, dict) else None
    if isinstance(slot_payload, dict):
        selected_id = candidate_pack_slot_selected_entry_id(slot_payload)
    ranked = sorted(
        entries,
        key=lambda entry: (
            -candidate_pack_visual_entry_score(entry, source_corpus, corpus, selected_id),
            candidate_pack_visual_fallback_order(entry, slot, result, corpus, policy),
        ),
    )
    candidates: List[JsonDict] = []
    for entry in ranked[:candidate_limit]:
        entry_id = str(entry.get("id") or "")
        if not entry_id:
            continue
        candidates.append(
            {
                "id": candidate_pack_candidate_id("slot", entry_id, slot),
                "slot": slot,
                "entry_id": entry_id,
                "label_en": localize(entry, "en") or entry_id,
                "label_ko": localize(entry, "ko") or entry_id,
                "terms": candidate_pack_visual_entry_terms(entry),
                "score": candidate_pack_visual_entry_score(entry, source_corpus, corpus, selected_id),
                "selected_by_sampler": bool(selected_id and entry_id == selected_id),
            }
        )
    return candidates


def candidate_pack_visual_proposition(
    data: JsonDict,
    result: JsonDict,
    trace: JsonDict,
    presets: Sequence[JsonDict],
    slots: JsonDict,
    mandatory_intents: Sequence[JsonDict],
    quality_profile: JsonDict,
) -> JsonDict:
    corpus = candidate_pack_integration_corpus(result, trace, presets, slots, mandatory_intents)
    source_corpus = candidate_pack_integration_source_corpus(result, trace, mandatory_intents)
    policy = candidate_pack_visual_policy(data)
    subject_classes = candidate_pack_visual_subject_classes(result, slots, corpus, policy, quality_profile)
    subject_class = str(subject_classes[0].get("id") or "general")
    register = candidate_pack_visual_register(subject_classes, source_corpus, corpus, policy, quality_profile)
    registers = policy.get("registers") if isinstance(policy.get("registers"), dict) else {}
    register_policy = registers.get(register) if isinstance(registers.get(register), dict) else {}
    if not register_policy:
        register_policy = registers.get("understated") if isinstance(registers.get("understated"), dict) else {}
    proposition_slots = normalize_list(policy.get("slots")) or ["narrative_core", "concept_tension"]
    core_slot = proposition_slots[0]
    tension_slot = proposition_slots[1] if len(proposition_slots) > 1 else "concept_tension"
    try:
        candidate_limit = int(policy.get("candidate_limit", 3) or 3)
    except (TypeError, ValueError):
        candidate_limit = 3
    candidate_limit = max(1, candidate_limit)
    core_allowed = any(str(item.get("core_policy", "allow")) != "none" for item in subject_classes)
    core_candidates = (
        candidate_pack_visual_candidates_for_slot(data, result, slots, core_slot, source_corpus, corpus, policy, candidate_limit)
        if core_allowed
        else []
    )
    tension_candidates = candidate_pack_visual_candidates_for_slot(
        data, result, slots, tension_slot, source_corpus, corpus, policy, candidate_limit
    )
    category_terms = {
        "narrative_core": list(
            dict.fromkeys(term for candidate in core_candidates for term in candidate.get("terms", []))
        )[:40],
        "concept_tension": list(
            dict.fromkeys(term for candidate in tension_candidates for term in candidate.get("terms", []))
        )[:40],
        "evidence": normalize_list(policy.get("evidence_terms"))[:40],
    }
    return {
        "enabled": True,
        "source": "quality_layers_narrative_core_and_concept_tension_slots",
        "quality_profile": quality_profile,
        "subject_class": subject_class,
        "subject_classes": subject_classes,
        "register": register,
        "minimum_hits": int(register_policy.get("minimum_hits", 1) or 0),
        "core_candidates": core_candidates,
        "tension_candidates": tension_candidates,
        "principles": normalize_list(register_policy.get("principles"))[:4],
        "anti_patterns": normalize_list(policy.get("anti_patterns"))[:5],
        "audit_categories": ["narrative_core", "concept_tension", "evidence"],
        "category_terms": category_terms,
    }


def build_candidate_pack(result: JsonDict, data: JsonDict) -> JsonDict:
    trace = result.get("semantic_trace") if isinstance(result.get("semantic_trace"), dict) else {}
    provenance = result.get("provenance") if isinstance(result.get("provenance"), dict) else {}
    candidate_entries: Dict[str, tuple[str, Optional[str], JsonDict]] = {}
    presets = candidate_pack_build_presets(data, trace, result, candidate_entries)
    slots = candidate_pack_build_slots(data, trace, result, candidate_entries)
    adult_appeal = candidate_pack_hybrid_adult_appeal(data, result, candidate_entries)
    selected_preset = candidate_pack_selected_preset(data, result)
    selected_blueprint = candidate_pack_resolve_scene_blueprint(
        data,
        result,
        selected_preset,
    )
    conflicts = candidate_pack_conflicts(data, candidate_entries)
    candidate_pack_apply_conflicts(slots, conflicts)
    candidate_pack_apply_conflicts_to_candidates(
        candidate_pack_hybrid_adult_candidates(adult_appeal), conflicts
    )
    candidate_blobs = candidate_pack_candidate_blobs(presets, slots)
    candidate_terms = candidate_pack_candidate_terms(presets, slots)
    mandatory_intents, uncovered_intents = candidate_pack_mandatory_intents(result, trace, candidate_blobs, candidate_terms)
    intent_contract = candidate_pack_intent_contract(data, result, trace, candidate_blobs)
    contract = trace.get("generation_contract") if isinstance(trace.get("generation_contract"), dict) else {}
    soft_policy = contract.get("soft_anchor_policy") if isinstance(contract.get("soft_anchor_policy"), dict) else {}
    scene_contract = candidate_pack_scene_contract(soft_policy, slots, selected_blueprint)
    render_contract = candidate_pack_render_contract(
        selected_preset,
        scene_contract,
        selected_blueprint,
    )
    character_grammar = candidate_pack_character_grammar(
        data,
        selected_preset,
        selected_blueprint,
    )
    render_intents = candidate_pack_render_mandatory_intents(
        render_contract,
        str(selected_preset.get("id") or ""),
    )
    mandatory_intents.extend(render_intents)
    uncovered_intents = [row for row in mandatory_intents if row.get("status") == "uncovered"]
    quality_profile = candidate_pack_quality_profile(data, result, slots, mandatory_intents)
    masked_buckets = candidate_pack_choose_masked_buckets(result, contract, soft_policy, slots)
    open_slots = candidate_pack_open_slots(result, slots, masked_buckets)
    masked_slot_names = {str(item.get("slot")) for item in open_slots if isinstance(item, dict)}
    if masked_slot_names:
        masked_prefixes = tuple(f"slot:{slot}:" for slot in sorted(masked_slot_names))
        conflicts = [
            conflict
            for conflict in conflicts
            if not any(str(candidate_id).startswith(masked_prefixes) for candidate_id in conflict.get("candidates", []))
        ]
        for intent_row in mandatory_intents:
            covered_by = [
                candidate_id
                for candidate_id in intent_row.get("covered_by", [])
                if not str(candidate_id).startswith(masked_prefixes)
            ]
            intent_row["covered_by"] = covered_by
            intent_row["status"] = "covered" if covered_by else "uncovered"
        uncovered_intents = [row for row in mandatory_intents if row.get("status") == "uncovered"]
    creative_exploration = candidate_pack_creative_exploration(result, slots, candidate_entries)
    creative_direction = candidate_pack_creative_direction(result)
    viewer_experience = candidate_pack_viewer_experience(result)
    hybrid_augmentation = candidate_pack_hybrid_augmentation(
        data,
        result,
        slots,
        masked_slot_names,
        adult_appeal,
    )
    pack: JsonDict = {
        "contract_version": "photo-candidate-pack/v2",
        "pack_id": "",
        "intent_contract": intent_contract,
        "mandatory_intents": mandatory_intents,
        "uncovered_intents": uncovered_intents,
        "presets": presets,
        "slots": slots,
        "quality_profile": quality_profile,
        "concept_axes": candidate_pack_concept_axes(soft_policy),
        "scene_contract": scene_contract,
        "render_contract": render_contract,
        "character_grammar": character_grammar,
        "evidence_budget": render_contract.get("evidence_budget", {"enabled": False}),
        "photographic_integration": candidate_pack_photographic_integration(
            data, result, trace, presets, slots, mandatory_intents, quality_profile
        ),
        "visual_proposition": candidate_pack_visual_proposition(
            data, result, trace, presets, slots, mandatory_intents, quality_profile
        ),
        "photographic_craft": candidate_pack_photographic_craft(data, quality_profile),
        "artistic_final_touch": candidate_pack_artistic_final_touch(data, quality_profile),
        "motif_budget": candidate_pack_motif_budget(result, trace, soft_policy),
        "preset_reference": candidate_pack_preset_reference(result, soft_policy, masked_buckets, open_slots),
        "masked_buckets": masked_buckets,
        "open_slots": open_slots,
        "template_echo_risk": candidate_pack_template_echo_risk(open_slots),
        "role_scene_policy": soft_policy.get("role_scene_policy", {"enabled": False}),
        "species_family": soft_policy.get("species_family_policy", {"enabled": False, "allowed": {}}),
        "safety": contract.get("safety") or {
            "mode": "automatic",
            "evaluation_requested": False,
            "status": "pass",
            "requires_user_approval": False,
            "items": [],
        },
        "concept_gates": contract.get("concept_gate_results", []),
        "diversity_state": candidate_pack_diversity_state(trace),
        "coverage": {
            "mandatory_intent_count": len(mandatory_intents),
            "covered_mandatory_intent_count": len(mandatory_intents) - len(uncovered_intents),
            "uncovered_intent_count": len(uncovered_intents),
            "intent_constraints": contract.get("intent_constraints", {}),
            "axis_coverage": trace.get("axis_coverage", {}),
            "contract": {
                "must_cover_axes": contract.get("must_cover_axes", []),
                "covered_axes": contract.get("covered_axes", []),
                "coverage_gaps": contract.get("coverage_gaps", []),
            },
            "candidate_limits": {
                "preset_top": CANDIDATE_PACK_PRESET_LIMIT,
                "core_slot_top": CANDIDATE_PACK_CORE_SLOT_LIMIT,
                "support_slot_top": CANDIDATE_PACK_SUPPORT_SLOT_LIMIT,
                "total": CANDIDATE_PACK_TOTAL_CANDIDATE_LIMIT,
            },
        },
        "conflicts": conflicts,
        "negative_en": result.get("negative_en"),
        "provenance": {
            "generator_version": provenance.get("generator_version", GENERATOR_VERSION),
            "seed": provenance.get("seed"),
            "batch_index": provenance.get("batch_index"),
            "preset_id": provenance.get("preset_id") or result.get("preset_id"),
            "selection_mode": provenance.get("selection_mode") or trace.get("selection_mode"),
            "requested_selection_mode": provenance.get("requested_selection_mode") or trace.get("requested_selection_mode"),
            "tags_hash": provenance.get("tags_hash") or trace.get("dictionary_hash"),
            "concept_lock": provenance.get("concept_lock", []),
            "additional_requirements": provenance.get("additional_requirements", []),
            "likeness_mode": provenance.get("likeness_mode"),
            "likeness_references": provenance.get("likeness_references", []),
            "user_mandatory_intents": provenance.get("user_mandatory_intents", []),
            "concept_gate_results": provenance.get("concept_gate_results", []),
            "concept_scene_variants": provenance.get("concept_scene_variants", []),
            "requested_scene_function": provenance.get("requested_scene_function"),
            "safety": provenance.get("safety", contract.get("safety", {})),
            "argv": provenance.get("argv", []),
            "sample_prompt_id": provenance.get("prompt_id"),
        },
    }
    if creative_exploration is not None:
        pack["creative_exploration"] = creative_exploration
    if creative_direction is not None:
        pack["creative_direction"] = creative_direction
    if viewer_experience is not None:
        pack["viewer_experience"] = viewer_experience
    if hybrid_augmentation is not None:
        pack["provenance"]["hybrid_augmentation_requested"] = bool(
            provenance.get("hybrid_augmentation_requested")
        )
        adult_axes = (
            adult_appeal.get("axes")
            if isinstance(adult_appeal, dict) and isinstance(adult_appeal.get("axes"), dict)
            else {}
        )
        pack["provenance"]["adult_appeal"] = {
            "enabled": bool((adult_appeal or {}).get("enabled")),
            "requested_enabled": bool((adult_appeal or {}).get("requested_enabled")),
            "activation_source": (adult_appeal or {}).get("activation_source"),
            "eligibility": (adult_appeal or {}).get("eligibility", {}),
            "axes": {
                axis_id: {
                    "intensity": int((adult_axes.get(axis_id) or {}).get("intensity", 0) or 0),
                    "active": bool((adult_axes.get(axis_id) or {}).get("active")),
                }
                for axis_id in CANDIDATE_PACK_ADULT_APPEAL_AXES
            },
            "blend": {"emphasis": ((adult_appeal or {}).get("blend") or {}).get("emphasis")},
        }
        pack["hybrid_augmentation"] = hybrid_augmentation
    hashable = dict(pack)
    hashable["pack_id"] = None
    pack["pack_id"] = stable_text_id(json.dumps(hashable, ensure_ascii=False, sort_keys=True, separators=(",", ":"))) or ""
    return pack


def semantic_description_for_entry(entry: Entry) -> str:
    if entry.get("embedding_text"):
        return " ".join(normalize_list(entry.get("embedding_text")))
    if entry.get("en"):
        return str(entry["en"])
    if entry.get("ko"):
        return str(entry["ko"])
    return str(entry.get("id", ""))


def semantic_caption_for_entry(entry: Entry, slot: Optional[str] = None) -> str:
    description = semantic_description_for_entry(entry)
    if slot:
        template = SEMANTIC_SLOT_CAPTION_TEMPLATES.get(
            slot,
            "Photo prompt slot concept for {slot}: {description}. It should retrieve visually compatible photographic details for this slot.",
        )
        return template.format(slot=slot, description=description)
    return (
        f"Photo prompt preset concept: {description}. It should retrieve a coherent photographic recipe "
        "including subject, place, lighting, camera, mood, and style."
    )


def dictionary_hash(data: JsonDict) -> str:
    material = {
        "version": data.get("version"),
        "presets": data.get("presets", []),
        "preset_families": data.get("preset_families", []),
        "recipes": data.get("recipes", []),
        "slots": data.get("slots", {}),
        "facet_vocab": data.get("facet_vocab", {}),
    }
    payload = json.dumps(material, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def semantic_policy_from_source(source: Optional[JsonDict]) -> JsonDict:
    if not source:
        return {}
    policy = source.get("semantic_policy", {}) or {}
    return policy if isinstance(policy, dict) else {}


def semantic_policy_digest(policy: Optional[JsonDict]) -> Optional[str]:
    if not policy:
        return None
    payload = json.dumps(policy, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def semantic_policy_schema_version(source: Optional[JsonDict]) -> Optional[int]:
    policy = semantic_policy_from_source(source)
    raw_version = policy.get("schema_version")
    if raw_version is None:
        return None
    try:
        return int(raw_version)
    except (TypeError, ValueError):
        return None


def semantic_policy_family_config(source: Optional[JsonDict], family: str) -> JsonDict:
    families = (semantic_policy_from_source(source).get("families", {}) or {})
    config = families.get(family, {}) if isinstance(families, dict) else {}
    return config if isinstance(config, dict) else {}


def semantic_policy_family_names(source: Optional[JsonDict] = None) -> List[str]:
    families = (semantic_policy_from_source(source).get("families", {}) or {})
    if isinstance(families, dict) and families:
        return list(families.keys())
    return []


def semantic_policy_float(source: Optional[JsonDict], path: Sequence[str], default: float) -> float:
    node: Any = semantic_policy_from_source(source)
    for key in path:
        if not isinstance(node, dict):
            return default
        node = node.get(key)
    try:
        return float(node)
    except (TypeError, ValueError):
        return default


def semantic_policy_id(source: Optional[JsonDict], family: str) -> str:
    return str(semantic_policy_family_config(source, family).get("policy_id") or f"{family}-legacy-code-policy")


def semantic_family_keywords(source: Optional[JsonDict], family: str) -> tuple[str, ...]:
    config = semantic_policy_family_config(source, family)
    configured = normalize_list(config.get("keywords")) + normalize_list(config.get("aliases"))
    if configured:
        return tuple(dict.fromkeys(configured))
    return ()


def semantic_family_axis_label(source: Optional[JsonDict], family: str) -> str:
    label = semantic_policy_family_config(source, family).get("axis_label")
    if label:
        return str(label)
    return family.replace("_", " ")


def semantic_family_axis_embedding_text(source: Optional[JsonDict], family: str) -> str:
    text = semantic_policy_family_config(source, family).get("axis_embedding_text")
    if text:
        return str(text)
    return semantic_family_axis_label(source, family)


def semantic_axis_route_slots(source: Optional[JsonDict], family: str) -> tuple[str, ...]:
    config = semantic_policy_family_config(source, family)
    routed_slots = normalize_list(config.get("routed_slots"))
    if routed_slots:
        return tuple(routed_slots)
    return ()


def semantic_axis_routed_families_for_slot(source: Optional[JsonDict], slot: str) -> Set[str]:
    return {
        family
        for family in semantic_policy_family_names(source)
        if slot in semantic_axis_route_slots(source, family)
    }


def semantic_text_for_entry(entry: Entry, slot: Optional[str] = None) -> str:
    parts: List[str] = [semantic_caption_for_entry(entry, slot)]
    for key in ("en", "ko"):
        if entry.get(key):
            parts.append(f"{key} label: {entry[key]}.")
    for key in ("aliases", "keywords", "tags", "kind"):
        values = normalize_list(entry.get(key))
        if values:
            parts.append(f"{key}: {', '.join(values)}.")
    if slot:
        parts.append(f"slot: {slot}.")
    if entry.get("id"):
        parts.append(f"stable id: {entry['id']}.")
    facets = entry.get("facets", {}) or {}
    if isinstance(facets, dict):
        for key, values in facets.items():
            normalized = normalize_list(values)
            if normalized:
                parts.append(f"facet {key}: {', '.join(normalized)}.")
    return " ".join(parts)


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    if not a or not b:
        return 0.0
    numerator = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a <= 0 or norm_b <= 0:
        return 0.0
    return numerator / (norm_a * norm_b)


def semantic_dimensions_value(dimensions: int) -> int:
    try:
        dims = int(dimensions)
    except (TypeError, ValueError) as exc:
        raise ValueError("embedding dimensions must be an integer") from exc
    if dims < 1:
        raise ValueError("embedding dimensions must be at least 1")
    return dims


def get_gemini_api_key(api_key: Optional[str] = None) -> str:
    key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        raise RuntimeError(
            "GEMINI_API_KEY or GOOGLE_API_KEY is required for Gemini semantic embeddings."
        )
    return key


def extract_embedding_values(response: Any) -> List[List[float]]:
    embeddings = getattr(response, "embeddings", None)
    if embeddings is None and isinstance(response, dict):
        embeddings = response.get("embeddings")
    if embeddings is None:
        embedding = getattr(response, "embedding", None)
        if embedding is None and isinstance(response, dict):
            embedding = response.get("embedding")
        embeddings = [embedding] if embedding is not None else []

    values_list: List[List[float]] = []
    for embedding in embeddings:
        values = getattr(embedding, "values", None)
        if values is None and isinstance(embedding, dict):
            values = embedding.get("values")
        if values is None:
            raise RuntimeError("Gemini embedding response did not include vector values.")
        values_list.append([float(value) for value in values])
    return values_list


def round_embedding_vector(vector: Sequence[float], dimensions: int) -> List[float]:
    if len(vector) != dimensions:
        raise ValueError(
            f"Gemini returned {len(vector)} embedding dimensions, expected {dimensions}."
        )
    return [round(float(value), 6) for value in vector]


def embed_texts_with_gemini(
    texts: Sequence[str],
    model: str = SEMANTIC_MODEL_ID,
    dimensions: int = DEFAULT_SEMANTIC_DIMENSIONS,
    api_key: Optional[str] = None,
    retry_attempts: int = 4,
    retry_initial_delay: float = 15.0,
) -> List[List[float]]:
    if not texts:
        return []
    dims = semantic_dimensions_value(dimensions)
    key = get_gemini_api_key(api_key)

    try:
        from google import genai
        from google.genai import types
    except ImportError as exc:
        raise RuntimeError(
            "google-genai is required for Gemini semantic embeddings. "
            "Install it with `python3 -m pip install -r requirements.txt`."
        ) from exc

    client = genai.Client(api_key=key)
    config = types.EmbedContentConfig(
        output_dimensionality=dims,
        task_type="SEMANTIC_SIMILARITY",
    )
    response = None
    attempts = max(1, int(retry_attempts) + 1)
    for attempt in range(attempts):
        try:
            response = client.models.embed_content(
                model=model,
                contents=[str(text) for text in texts],
                config=config,
            )
            break
        except Exception as exc:
            message = str(exc)
            retryable = (
                "429" in message
                or "503" in message
                or "RESOURCE_EXHAUSTED" in message
                or "UNAVAILABLE" in message
            )
            if not retryable or attempt >= attempts - 1:
                raise
            delay = max(0.0, float(retry_initial_delay)) * (2 ** attempt)
            if delay > 0:
                time.sleep(delay)
    if response is None:
        raise RuntimeError("Gemini embedding request did not return a response.")
    vectors = extract_embedding_values(response)
    if len(vectors) != len(texts):
        raise RuntimeError(
            f"Gemini returned {len(vectors)} embeddings for {len(texts)} input texts."
        )
    return [round_embedding_vector(vector, dims) for vector in vectors]


def semantic_entry_key(kind: str, entry: Entry, slot: Optional[str] = None) -> str:
    if kind == "preset":
        return f"preset:{entry.get('id')}"
    if kind == "virtual_preset":
        return f"preset:virtual:{entry.get('id')}"
    return f"slot:{slot}:{entry.get('id')}"


def iter_semantic_entries(data: JsonDict) -> List[tuple[str, str, Entry, Optional[str]]]:
    entries: List[tuple[str, str, Entry, Optional[str]]] = []
    for preset in data.get("presets", []):
        if preset.get("automatic_discovery") is False:
            continue
        key = semantic_entry_key("preset", preset)
        entries.append((key, "preset", preset, None))
    for recipe in data.get("recipes", []):
        key = semantic_entry_key("virtual_preset", recipe)
        entries.append((key, "virtual_preset", recipe, None))
    for slot, slot_entries in data.get("slots", {}).items():
        for entry in slot_entries:
            key = semantic_entry_key("slot", entry, slot)
            entries.append((key, "slot", entry, slot))
    return entries


def build_semantic_index_payload(
    data: JsonDict,
    dimensions: int = DEFAULT_SEMANTIC_DIMENSIONS,
    provider: str = SEMANTIC_PROVIDER,
    model: str = SEMANTIC_MODEL_ID,
    api_key: Optional[str] = None,
    batch_size: int = 1,
    request_interval: float = 0.0,
    retry_attempts: int = 4,
    retry_initial_delay: float = 15.0,
    progress_callback: Optional[Callable[[int, int], None]] = None,
) -> JsonDict:
    if provider != SEMANTIC_PROVIDER:
        raise ValueError(f"Unsupported semantic provider '{provider}'. Only '{SEMANTIC_PROVIDER}' is supported.")
    dims = semantic_dimensions_value(dimensions)
    batch = max(1, int(batch_size))
    rows = iter_semantic_entries(data)
    texts = [semantic_text_for_entry(entry, slot) for _, _, entry, slot in rows]
    vectors: List[List[float]] = []
    for start in range(0, len(texts), batch):
        vectors.extend(
            embed_texts_with_gemini(
                texts[start : start + batch],
                model=model,
                dimensions=dims,
                api_key=api_key,
                retry_attempts=retry_attempts,
                retry_initial_delay=retry_initial_delay,
            )
        )
        done = min(start + batch, len(texts))
        if progress_callback:
            progress_callback(done, len(texts))
        if request_interval > 0 and done < len(texts):
            time.sleep(request_interval)
    if len(vectors) != len(rows):
        raise RuntimeError(f"Expected {len(rows)} semantic vectors, received {len(vectors)}.")

    entries: JsonDict = {}
    for (key, kind, entry, slot), text, vector in zip(rows, texts, vectors):
        entries[key] = {
            "kind": kind,
            "slot": slot,
            "id": entry.get("id"),
            "text": text,
            "vector": vector,
        }
    return {
        "provider": provider,
        "dictionary_hash": dictionary_hash(data),
        "semantic_text_recipe": SEMANTIC_TEXT_RECIPE_VERSION,
        "embedding_model": model,
        "embedding_dimensions": dims,
        "entries": entries,
    }


SEMANTIC_INDEX_SHARDED_FORMAT = "sharded-json-v1"


def load_semantic_index_payload(path: str | Path) -> JsonDict:
    """Load either a legacy monolith or a sharded index with identical entry order.

    Sharding is a storage concern only. Callers continue to receive the same
    materialized ``entries`` mapping used by scoring, tie-breaking, and audit
    code, so a storage migration cannot alter retrieval behavior.
    """
    index_path = Path(path)
    payload = json.loads(index_path.read_text(encoding="utf-8"))
    storage = payload.get("storage") if isinstance(payload.get("storage"), dict) else {}
    if storage.get("format") != SEMANTIC_INDEX_SHARDED_FORMAT:
        return payload

    entry_order = payload.get("entry_order")
    shard_rows = payload.get("shards")
    if not isinstance(entry_order, list) or any(not isinstance(key, str) for key in entry_order):
        raise ValueError(f"Invalid sharded semantic index entry_order: {index_path}")
    if len(entry_order) != len(set(entry_order)):
        raise ValueError(f"Duplicate keys in sharded semantic index entry_order: {index_path}")
    if not isinstance(shard_rows, list) or not shard_rows:
        raise ValueError(f"Invalid sharded semantic index shard list: {index_path}")

    unordered_entries: JsonDict = {}
    root = index_path.parent.resolve()
    for shard_row in shard_rows:
        if not isinstance(shard_row, dict) or not str(shard_row.get("path") or "").strip():
            raise ValueError(f"Invalid shard descriptor in semantic index: {index_path}")
        shard_path = (index_path.parent / str(shard_row["path"])).resolve()
        if root not in shard_path.parents:
            raise ValueError(f"Semantic index shard escapes index directory: {shard_path}")
        raw = shard_path.read_bytes()
        expected_hash = str(shard_row.get("sha256") or "")
        if expected_hash and hashlib.sha256(raw).hexdigest() != expected_hash:
            raise ValueError(f"Semantic index shard checksum mismatch: {shard_path}")
        shard_payload = json.loads(raw.decode("utf-8"))
        shard_entries = shard_payload.get("entries") if isinstance(shard_payload, dict) else None
        if not isinstance(shard_entries, dict):
            raise ValueError(f"Semantic index shard has no entries object: {shard_path}")
        expected_count = shard_row.get("entry_count")
        if expected_count is not None and int(expected_count) != len(shard_entries):
            raise ValueError(f"Semantic index shard entry count mismatch: {shard_path}")
        duplicate_keys = set(unordered_entries) & set(shard_entries)
        if duplicate_keys:
            raise ValueError(f"Duplicate semantic index entry across shards: {sorted(duplicate_keys)[0]}")
        unordered_entries.update(shard_entries)

    ordered_keys = set(entry_order)
    if ordered_keys != set(unordered_entries):
        missing = sorted(ordered_keys - set(unordered_entries))
        unexpected = sorted(set(unordered_entries) - ordered_keys)
        raise ValueError(
            "Sharded semantic index manifest does not match shard entries "
            f"(missing={missing[:3]}, unexpected={unexpected[:3]})."
        )
    expected_total = payload.get("entry_count")
    if expected_total is not None and int(expected_total) != len(entry_order):
        raise ValueError(f"Semantic index manifest entry count mismatch: {index_path}")

    materialized = dict(payload)
    materialized["entries"] = {key: unordered_entries[key] for key in entry_order}
    return materialized


def validate_semantic_index_metadata(
    payload: JsonDict,
    data: JsonDict,
    provider: str = SEMANTIC_PROVIDER,
    model: str = SEMANTIC_MODEL_ID,
    dimensions: int = DEFAULT_SEMANTIC_DIMENSIONS,
) -> None:
    expected = dictionary_hash(data)
    if payload.get("dictionary_hash") != expected:
        raise ValueError(
            "Semantic index dictionary_hash does not match the tag dictionary. "
            "Regenerate it with build_semantic_index.py."
        )
    if payload.get("semantic_text_recipe") != SEMANTIC_TEXT_RECIPE_VERSION:
        raise ValueError(
            f"Semantic index semantic_text_recipe is {payload.get('semantic_text_recipe')!r}, "
            f"expected {SEMANTIC_TEXT_RECIPE_VERSION!r}. Regenerate it with build_semantic_index.py."
        )
    if payload.get("provider", SEMANTIC_PROVIDER) != provider:
        raise ValueError(
            f"Semantic index provider is {payload.get('provider')!r}, expected {provider!r}."
        )
    if payload.get("embedding_model") != model:
        raise ValueError(
            f"Semantic index embedding_model is {payload.get('embedding_model')!r}, expected {model!r}."
        )
    expected_dims = semantic_dimensions_value(dimensions)
    if int(payload.get("embedding_dimensions", -1)) != expected_dims:
        raise ValueError(
            f"Semantic index embedding_dimensions is {payload.get('embedding_dimensions')!r}, "
            f"expected {expected_dims}."
        )


def load_semantic_index(
    path: Optional[str | Path],
    data: JsonDict,
    semantic_index: Optional[JsonDict] = None,
    provider: str = SEMANTIC_PROVIDER,
    model: str = SEMANTIC_MODEL_ID,
    dimensions: int = DEFAULT_SEMANTIC_DIMENSIONS,
) -> JsonDict:
    if semantic_index is not None:
        payload = semantic_index
    else:
        if not path:
            raise FileNotFoundError(
                "Semantic index is required for semantic or hybrid selection. "
                "Build it with build_semantic_index.py."
            )
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Semantic index not found: {p}")
        payload = load_semantic_index_payload(p)
    validate_semantic_index_metadata(payload, data, provider, model, dimensions)
    return payload


def facet_tokens(entry: Entry) -> Set[str]:
    tokens: Set[str] = set()
    facets = entry.get("facets", {}) or {}
    if not isinstance(facets, dict):
        return tokens
    for key, values in facets.items():
        for value in normalize_list(values):
            tokens.add(f"{key}:{value}")
    return tokens


def guard_values(entry: Entry, key: str) -> Set[str]:
    guards = entry.get("hard_guards", {}) or {}
    if not isinstance(guards, dict):
        return set()
    return set(normalize_list(guards.get(key)))


def compatible_with_facet_guards(item: Entry, preset: JsonDict, picked: Dict[str, Entry]) -> bool:
    context: Set[str] = set()
    context |= facet_tokens(preset)
    for entry in picked.values():
        context |= facet_tokens(entry)
    item_facets = facet_tokens(item)

    preset_excludes = guard_values(preset, "exclude_facets")
    if preset_excludes & item_facets:
        return False

    requires = guard_values(item, "requires_facets")
    if requires and not requires.issubset(context | item_facets):
        return False

    excludes = guard_values(item, "exclude_facets")
    if excludes & context:
        return False

    return True


NOVELTY_SETTINGS_DEFAULTS: Dict[str, tuple[float, float]] = {
    "low": (1.8, 0.05),
    "medium": (1.15, 0.18),
    "high": (0.75, 0.45),
}


def creativity_override(source: Optional[JsonDict], key: str) -> Any:
    if not isinstance(source, dict):
        return None
    overrides = source.get("creativity_overrides")
    if not isinstance(overrides, dict):
        return None
    return overrides.get(key)


def novelty_settings(novelty: str, source: Optional[JsonDict] = None) -> tuple[float, float]:
    override = creativity_override(source, "novelty_settings")
    if isinstance(override, (list, tuple)) and len(override) == 2:
        try:
            return (float(override[0]), float(override[1]))
        except (TypeError, ValueError):
            pass
    base = NOVELTY_SETTINGS_DEFAULTS.get(novelty, NOVELTY_SETTINGS_DEFAULTS["medium"])
    temperature = semantic_policy_float(source, ("novelty", novelty, "temperature"), base[0])
    scale = semantic_policy_float(source, ("novelty", novelty, "novelty_scale"), base[1])
    return (temperature, scale)


def semantic_profile_config(profile: str, source: Optional[JsonDict] = None) -> Dict[str, float]:
    override = creativity_override(source, "profile_config")
    if isinstance(override, dict) and override:
        return override
    base = SEMANTIC_PROFILE_CONFIGS.get(profile, SEMANTIC_PROFILE_CONFIGS["balanced"])
    policy_profiles = semantic_policy_from_source(source).get("profiles", {}) if source else {}
    overlay = policy_profiles.get(profile, {}) if isinstance(policy_profiles, dict) else {}
    if isinstance(overlay, dict) and overlay:
        merged: Dict[str, float] = dict(base)
        for key, value in overlay.items():
            try:
                merged[str(key)] = float(value)
            except (TypeError, ValueError):
                continue
        return merged
    return base


def semantic_base_power(context: Optional[JsonDict]) -> float:
    """Exponent applied to base weights in semantic candidate scoring.

    Soft-anchor promotion factors are damped by this exponent, so the bias
    path compensates with factor ** (1 / base_power) to restore nominal
    multipliers in the final weights.
    """
    if not isinstance(context, dict):
        return 1.0
    selection_mode = str(context.get("selection_mode") or "semantic")
    semantic_weight = float(context.get("semantic_weight", default_semantic_weight(selection_mode)))
    return max(0.15, 1.0 - (semantic_weight * 0.85))


def batch_diversity_config(novelty: str, source: Optional[JsonDict] = None) -> Dict[str, Any]:
    override = creativity_override(source, "batch_diversity_config")
    if isinstance(override, dict) and override:
        return override
    base = BATCH_DIVERSITY_CONFIGS.get(novelty, BATCH_DIVERSITY_CONFIGS["medium"])
    policy_configs = semantic_policy_from_source(source).get("batch_diversity", {}) if source else {}
    overlay = policy_configs.get(novelty, {}) if isinstance(policy_configs, dict) else {}
    if isinstance(overlay, dict) and overlay:
        merged: Dict[str, Any] = dict(base)
        scope_weights = dict(base.get("scope_weights", {}))
        for key, value in overlay.items():
            if key == "scope_weights" and isinstance(value, dict):
                for scope, weight in value.items():
                    try:
                        scope_weights[str(scope)] = float(weight)
                    except (TypeError, ValueError):
                        continue
                continue
            try:
                merged[str(key)] = float(value)
            except (TypeError, ValueError):
                continue
        merged["scope_weights"] = scope_weights
        return merged
    return base


CREATIVITY_PROFILE_ANCHORS: tuple[tuple[float, str, str], ...] = (
    (0.0, "conservative", "low"),
    (0.5, "balanced", "medium"),
    (1.0, "exploratory", "high"),
)
CREATIVITY_INTEGER_CONFIG_KEYS = {"preset_candidate_limit", "slot_candidate_limit"}


def clamp_unit_interval(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def interpolate_numeric_config(
    low: Dict[str, Any],
    high: Dict[str, Any],
    fraction: float,
) -> Dict[str, Any]:
    merged: Dict[str, Any] = {}
    for key in set(low) | set(high):
        left = low.get(key, high.get(key))
        right = high.get(key, low.get(key))
        if isinstance(left, dict) and isinstance(right, dict):
            merged[key] = interpolate_numeric_config(left, right, fraction)
            continue
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            value = float(left) + (float(right) - float(left)) * fraction
            merged[key] = int(round(value)) if key in CREATIVITY_INTEGER_CONFIG_KEYS else value
            continue
        merged[key] = right if fraction >= 0.5 else left
    return merged


def creativity_settings(creativity: float, source: Optional[JsonDict] = None) -> JsonDict:
    """Map a single 0..1 creativity lever onto the layered diversity knobs.

    0.0 anchors at conservative/low-novelty, 0.5 at balanced/medium, 1.0 at
    exploratory/high. Coherence knobs (semantic_weight, filter_strictness)
    are deliberately not touched: they trade off correctness, not creativity.
    """
    value = clamp_unit_interval(creativity)
    anchors = CREATIVITY_PROFILE_ANCHORS
    for (low_pos, low_profile, low_novelty), (high_pos, high_profile, high_novelty) in zip(anchors, anchors[1:]):
        if value <= high_pos:
            span = high_pos - low_pos
            fraction = 0.0 if span <= 0 else (value - low_pos) / span
            break
    else:
        low_profile, low_novelty = anchors[-1][1], anchors[-1][2]
        high_profile, high_novelty = low_profile, low_novelty
        fraction = 1.0
    profile_config = interpolate_numeric_config(
        dict(semantic_profile_config(low_profile, source)),
        dict(semantic_profile_config(high_profile, source)),
        fraction,
    )
    low_temp, low_scale = novelty_settings(low_novelty, source)
    high_temp, high_scale = novelty_settings(high_novelty, source)
    batch_config = interpolate_numeric_config(
        dict(batch_diversity_config(low_novelty, source)),
        dict(batch_diversity_config(high_novelty, source)),
        fraction,
    )
    nearest_profile = high_profile if fraction >= 0.5 else low_profile
    nearest_novelty = high_novelty if fraction >= 0.5 else low_novelty
    return {
        "creativity": value,
        "profile_config": profile_config,
        "novelty_settings": (
            low_temp + (high_temp - low_temp) * fraction,
            low_scale + (high_scale - low_scale) * fraction,
        ),
        "batch_diversity_config": batch_config,
        "profile_label": nearest_profile,
        "novelty_label": nearest_novelty,
    }


def default_filter_strictness(selection_mode: str) -> str:
    if selection_mode == "semantic":
        return "soft"
    return "hard"


def default_semantic_profile(selection_mode: str) -> str:
    if selection_mode == "semantic":
        return "balanced"
    return "conservative"


def default_semantic_weight(selection_mode: str) -> float:
    if selection_mode == "semantic":
        return 0.75
    if selection_mode == "hybrid":
        return 0.35
    return 0.0


def default_intent_steering(selection_mode: str) -> str:
    if selection_mode in {"semantic", "hybrid"}:
        return "auto"
    return "off"


def resolve_semantic_runtime_options(
    selection_mode: str,
    filter_strictness: Optional[str],
    semantic_weight: Optional[float],
    semantic_profile: Optional[str],
) -> tuple[str, float, str]:
    resolved_filter = filter_strictness or default_filter_strictness(selection_mode)
    resolved_profile = semantic_profile or default_semantic_profile(selection_mode)
    resolved_weight = default_semantic_weight(selection_mode) if semantic_weight is None else float(semantic_weight)
    if resolved_filter not in FILTER_STRICTNESS_MODES:
        raise ValueError(f"Invalid filter_strictness '{resolved_filter}'.")
    if resolved_profile not in SEMANTIC_PROFILES:
        raise ValueError(f"Invalid semantic_profile '{resolved_profile}'.")
    if not 0.0 <= resolved_weight <= 1.0:
        raise ValueError("--semantic-weight must be between 0 and 1")
    return resolved_filter, resolved_weight, resolved_profile


def clean_intent_axis(text: str) -> str:
    return clean_spaces(text.strip(" \t\r\n,;+/|"))


def unique_axes(values: Sequence[str]) -> List[str]:
    axes: List[str] = []
    seen: Set[str] = set()
    for value in values:
        axis = clean_intent_axis(str(value))
        key = axis.lower()
        if axis and key not in seen:
            axes.append(axis)
            seen.add(key)
    return axes[:6]


def delimiter_intent_axes(intent: str) -> List[str]:
    chunks = re.split(r"\s*(?:[,+|/;\n]+|\band\b|\bwith\b|및)\s*", intent, flags=re.IGNORECASE)
    axes = unique_axes(chunks)
    return axes if len(axes) > 1 else []


def fallback_intent_axes(intent: str, policy_source: Optional[JsonDict] = None) -> List[str]:
    lowered = intent.lower()
    return [
        semantic_family_axis_label(policy_source, family)
        for family in semantic_policy_family_names(policy_source)
        if axis_text_has_family(lowered, family, policy_source)
    ][:6]


def axis_text_has_family(text: str, family: str, policy_source: Optional[JsonDict] = None) -> bool:
    lowered = text.lower()
    for keyword in semantic_family_keywords(policy_source, family):
        token = str(keyword).lower()
        if not token:
            continue
        if re.search(r"[a-z0-9]", token):
            if re.search(rf"(?<![a-z0-9]){re.escape(token)}(?![a-z0-9])", lowered):
                return True
        elif token in lowered:
            return True
    return False


def axis_families_for_text(text: str, policy_source: Optional[JsonDict] = None) -> List[str]:
    return [
        family
        for family in semantic_policy_family_names(policy_source)
        if axis_text_has_family(text, family, policy_source)
    ]


def semantic_axis_embedding_text(axis: str, policy_source: Optional[JsonDict] = None) -> str:
    matched = [
        semantic_family_axis_embedding_text(policy_source, family)
        for family in axis_families_for_text(axis, policy_source)
    ]
    if matched:
        return "; ".join(matched)
    return axis


def extract_intent_axes(
    intent: str,
    explicit_axes: Optional[Sequence[str]] = None,
    semantic_axis_mode: str = "auto",
    intent_source: str = "user",
    policy_source: Optional[JsonDict] = None,
) -> JsonDict:
    if semantic_axis_mode not in SEMANTIC_AXIS_MODES:
        raise ValueError(f"Invalid semantic_axis_mode '{semantic_axis_mode}'.")
    explicit = unique_axes(explicit_axes or [])
    if explicit:
        source = "explicit"
        axes = explicit
    elif intent_source == "default":
        source = "default_full_intent"
        axes = [clean_intent_axis(intent)]
    elif semantic_axis_mode == "off":
        source = "off"
        axes = [clean_intent_axis(intent)]
    else:
        axes = delimiter_intent_axes(intent)
        if axes:
            source = "delimiter"
        else:
            axes = fallback_intent_axes(intent, policy_source)
            source = "fallback" if axes else "full_intent"
    if not axes:
        axes = [clean_intent_axis(intent)]
        source = "full_intent"
    return {
        "mode": semantic_axis_mode,
        "source": source,
        "items": [{"text": axis, "source": source} for axis in axes[:6]],
    }


def embed_single_semantic_text(
    text: str,
    model: str,
    dimensions: int,
    api_key: Optional[str],
) -> List[float]:
    return embed_texts_with_gemini(
        [text],
        model=model,
        dimensions=dimensions,
        api_key=api_key,
    )[0]


def semantic_profile_float(context: JsonDict, key: str, default: float) -> float:
    config = semantic_profile_config(str(context.get("semantic_profile", "balanced")), context)
    try:
        return float(config.get(key, default))
    except (TypeError, ValueError):
        return default


def initial_axis_coverage(axis_vectors: Sequence[JsonDict], profile: str, source: Optional[JsonDict] = None) -> JsonDict:
    config = semantic_profile_config(profile, source)
    target = float(config.get("axis_coverage_target", 0.68))
    return {
        "target": target,
        "items": [
            {
                "index": index,
                "text": item.get("text", ""),
                "families": item.get("families", []),
                "best_score": 0.0,
                "best_slot": None,
                "best_entry": None,
                "best_strength": "none",
            }
            for index, item in enumerate(axis_vectors)
        ],
    }


def semantic_axis_coverage_trace(context: JsonDict) -> JsonDict:
    coverage = context.get("axis_coverage", {}) or {}
    return {
        "target": round(float(coverage.get("target", 0.0)), 4),
        "items": [
            {
                "text": item.get("text", ""),
                "families": item.get("families", []),
                "best_score": round(float(item.get("best_score", 0.0)), 4),
                "best_slot": item.get("best_slot"),
                "best_entry": item.get("best_entry"),
                "best_strength": item.get("best_strength", "none"),
            }
            for item in coverage.get("items", [])
        ],
    }


def make_batch_context(
    selection_mode: str,
    novelty: str,
    total_count: int = 1,
    source: Optional[JsonDict] = None,
    creativity: Optional[float] = None,
) -> Optional[JsonDict]:
    if selection_mode not in {"semantic", "hybrid"} or total_count <= 1:
        return None
    if creativity is not None:
        config = creativity_settings(creativity, source)["batch_diversity_config"]
    else:
        config = batch_diversity_config(novelty, source)
    return {
        "enabled": True,
        "novelty": novelty,
        "batch_index": 0,
        "total_count": total_count,
        "config": config,
        "counts": {scope: {} for scope in BATCH_DIVERSITY_TRACKED_SCOPES},
        "vectors": {scope: [] for scope in BATCH_DIVERSITY_TRACKED_SCOPES},
        "selected": [],
    }


def set_batch_index(batch_context: Optional[JsonDict], batch_index: int) -> None:
    if batch_context:
        batch_context["batch_index"] = batch_index


def batch_scope_weight(batch_context: JsonDict, scope: str) -> float:
    scope_weights = batch_context.get("config", {}).get("scope_weights", {})
    try:
        return float(scope_weights.get(scope, 1.0))
    except (TypeError, ValueError):
        return 1.0


def batch_history_summary(batch_context: Optional[JsonDict]) -> JsonDict:
    if not batch_context or not batch_context.get("enabled"):
        return {"enabled": False, "counts": {}, "selected_count": 0}
    return {
        "enabled": True,
        "batch_index": int(batch_context.get("batch_index", 0)),
        "total_count": int(batch_context.get("total_count", 0)),
        "novelty": batch_context.get("novelty"),
        "counts": {
            scope: dict(sorted((ids or {}).items()))
            for scope, ids in (batch_context.get("counts", {}) or {}).items()
        },
        "selected_count": len(batch_context.get("selected", [])),
    }


def anchor_diversity_ledger_summary(ledger: Optional[JsonDict]) -> JsonDict:
    if not isinstance(ledger, dict) or not ledger:
        return {"enabled": False, "counts": {}}
    counts: JsonDict = {}
    for scope, raw_counts in ledger.items():
        if not isinstance(raw_counts, dict):
            continue
        normalized_counts: JsonDict = {}
        for key, value in raw_counts.items():
            try:
                normalized_counts[str(key)] = int(value)
            except (TypeError, ValueError):
                continue
        counts[str(scope)] = dict(sorted(normalized_counts.items()))
    return {"enabled": bool(counts), "counts": counts}


def batch_diversity_penalty(
    context: Optional[JsonDict],
    scope: str,
    item_id: str,
    vector: Sequence[float],
    forced: bool = False,
) -> tuple[float, JsonDict]:
    batch_context = (context or {}).get("batch_context") if context else None
    if forced or scope not in BATCH_DIVERSITY_TRACKED_SCOPES or not batch_context or not batch_context.get("enabled"):
        return 1.0, {"scope": scope, "id": item_id, "penalty": 1.0, "reason": "disabled" if not batch_context else "forced_or_untracked"}
    counts = batch_context.get("counts", {}).get(scope, {})
    exact_count = int(counts.get(item_id, 0))
    config = batch_context.get("config", {})
    scope_weight = batch_scope_weight(batch_context, scope)
    exact_decay = float(config.get("exact_decay", 0.66))
    exact_factor = exact_decay ** (exact_count * scope_weight)
    max_similarity = 0.0
    for previous in batch_context.get("vectors", {}).get(scope, []):
        max_similarity = max(max_similarity, cosine_similarity(vector, previous.get("vector", [])))
    threshold = float(config.get("similarity_threshold", 0.88))
    similarity_factor = 1.0
    if max_similarity > threshold:
        denominator = max(1.0 - threshold, 0.0001)
        normalized = min(1.0, max(0.0, (max_similarity - threshold) / denominator))
        similarity_factor = 1.0 - (float(config.get("similarity_weight", 0.26)) * scope_weight * normalized)
    minimum = float(config.get("min_penalty", 0.38))
    penalty = max(minimum, min(1.0, exact_factor * similarity_factor))
    return penalty, {
        "scope": scope,
        "id": item_id,
        "penalty": round(penalty, 4),
        "exact_count": exact_count,
        "max_similarity": round(max_similarity, 4),
    }


def batch_group_diversity_penalty(
    context: Optional[JsonDict],
    slot: str,
    item: Entry,
    vector: Sequence[float],
    forced: bool = False,
) -> tuple[float, JsonDict]:
    if forced or not context:
        return 1.0, {"enabled": False, "events": []}
    events: List[JsonDict] = []
    factors: List[float] = []
    if slot == "subject":
        for group in entry_semantic_groups(item, slot, context):
            factor, summary = batch_diversity_penalty(context, "subject_group", group, vector, forced=forced)
            factors.append(factor)
            events.append(summary)
    elif slot == "location":
        for tone in entry_location_tones(item, slot, context):
            factor, summary = batch_diversity_penalty(context, "location_tone", tone, vector, forced=forced)
            factors.append(factor)
            events.append(summary)
    if not factors:
        return 1.0, {"enabled": False, "events": []}
    factor = min(factors)
    return factor, {"enabled": True, "penalty": round(factor, 4), "events": events}


def record_batch_selection(
    batch_context: Optional[JsonDict],
    scope: str,
    item_id: str,
    vector: Sequence[float],
    forced: bool = False,
) -> None:
    if forced or scope not in BATCH_DIVERSITY_TRACKED_SCOPES or not batch_context or not batch_context.get("enabled"):
        return
    counts = batch_context.setdefault("counts", {}).setdefault(scope, {})
    counts[item_id] = int(counts.get(item_id, 0)) + 1
    batch_context.setdefault("vectors", {}).setdefault(scope, []).append({"id": item_id, "vector": list(vector)})
    batch_context.setdefault("selected", []).append(
        {"batch_index": int(batch_context.get("batch_index", 0)), "scope": scope, "id": item_id}
    )


def record_batch_group_selection(
    semantic_context: JsonDict,
    batch_context: Optional[JsonDict],
    slot: str,
    entry: Entry,
    vector: Sequence[float],
    forced: bool = False,
) -> None:
    if forced:
        return
    if slot == "subject":
        for group in entry_semantic_groups(entry, slot, semantic_context):
            record_batch_selection(batch_context, "subject_group", group, vector, forced=False)
    elif slot == "location":
        for tone in entry_location_tones(entry, slot, semantic_context):
            record_batch_selection(batch_context, "location_tone", tone, vector, forced=False)


def update_axis_coverage(
    context: JsonDict,
    slot: str,
    entry_id: str,
    vector: Sequence[float],
    entry: Optional[Entry] = None,
) -> None:
    coverage = context.get("axis_coverage")
    if not coverage or not vector:
        return
    axis_vectors = context.get("axis_vectors", [])
    for item in coverage.get("items", []):
        index = int(item.get("index", -1))
        if index < 0 or index >= len(axis_vectors):
            continue
        score = cosine_similarity(axis_vectors[index].get("vector", []), vector)
        strength = "none"
        families = axis_vectors[index].get("families", [])
        if entry is not None:
            for family in families:
                strength = stronger_family_strength(
                    strength,
                    family_signal_strength(entry, str(family), coherence_rules_from_source(context), slot, context),
                )
        strength_rank = FAMILY_STRENGTH_RANK.get(strength, 0)
        best_rank = FAMILY_STRENGTH_RANK.get(str(item.get("best_strength", "none")), 0)
        if score > float(item.get("best_score", 0.0)) or strength_rank > best_rank:
            item["best_score"] = score
            item["best_slot"] = slot
            item["best_entry"] = entry_id
            item["best_strength"] = strength


def context_axis_families(context: JsonDict) -> Set[str]:
    families: Set[str] = set()
    for axis in context.get("axis_vectors", []):
        families |= set(axis.get("families", []))
    return families


FAMILY_STRENGTH_RANK = {"none": 0, "ambient": 1, "strong": 2}


def semantic_metadata_from_source(source: Optional[JsonDict]) -> JsonDict:
    if not source:
        return {}
    return source.get("semantic_metadata", {}) or {}


def metadata_group_values(metadata: JsonDict, collection: str, entry_id: str) -> List[str]:
    values: List[str] = []
    for group, ids in (metadata.get(collection, {}) or {}).items():
        if entry_id in set(normalize_list(ids)):
            values.append(str(group))
    return sorted(values)


def entry_semantic_groups(entry: Entry, slot: str, source: Optional[JsonDict]) -> List[str]:
    entry_id = str(entry.get("id", ""))
    metadata = semantic_metadata_from_source(source)
    values: Set[str] = set(normalize_list(entry.get("semantic_group")))
    if slot == "subject":
        values |= set(metadata_group_values(metadata, "subject_groups", entry_id))
    return sorted(values)


def entry_location_tones(entry: Entry, slot: str, source: Optional[JsonDict]) -> List[str]:
    entry_id = str(entry.get("id", ""))
    metadata = semantic_metadata_from_source(source)
    values: Set[str] = set(normalize_list(entry.get("location_tone")))
    if slot == "location":
        values |= set(metadata_group_values(metadata, "location_tones", entry_id))
    return sorted(values)


def entry_axis_signals(entry: Entry, slot: str, source: Optional[JsonDict]) -> List[str]:
    entry_id = str(entry.get("id", ""))
    metadata = semantic_metadata_from_source(source)
    values: Set[str] = set(normalize_list(entry.get("axis_signal")))
    for signal, slot_map in (metadata.get("axis_signals", {}) or {}).items():
        if not isinstance(slot_map, dict):
            continue
        ids = set(normalize_list(slot_map.get(slot))) | set(normalize_list(slot_map.get("*")))
        if entry_id in ids:
            values.add(str(signal))
    return sorted(values)


def metadata_family_signal_strength(entry: Entry, slot: str, family: str, source: Optional[JsonDict]) -> str:
    signals = set(entry_axis_signals(entry, slot, source))
    if f"{family}_strong" in signals:
        return "strong"
    if f"{family}_ambient" in signals:
        return "ambient"
    if family == "human" and "human_portrait" in signals:
        return "strong"
    return "none"


def coherence_rules_from_source(source: JsonDict) -> JsonDict:
    return source.get("coherence_rules", {}) or {}


def coherence_family_rules(rules: JsonDict, family: str) -> JsonDict:
    return (rules.get("family_strength", {}) or {}).get(family, {}) or {}


def family_rule_id_set(rules: JsonDict, family: str, tier: str) -> Set[str]:
    return set(normalize_list(coherence_family_rules(rules, family).get(tier)))


def family_id_signal_strength(entry_id: str, family: str, rules: JsonDict) -> str:
    if entry_id in family_rule_id_set(rules, family, "strong"):
        return "strong"
    if entry_id in family_rule_id_set(rules, family, "ambient"):
        return "ambient"
    return "none"


def stronger_family_strength(left: str, right: str) -> str:
    return left if FAMILY_STRENGTH_RANK.get(left, 0) >= FAMILY_STRENGTH_RANK.get(right, 0) else right


def slot_conflict_rules_from_source(source: Optional[JsonDict]) -> List[JsonDict]:
    rules = coherence_rules_from_source(source or {})
    declared = rules.get("slot_conflicts")
    if not isinstance(declared, list):
        return []
    return [rule for rule in declared if isinstance(rule, dict)]


def slot_context_rules_from_source(source: Optional[JsonDict]) -> List[JsonDict]:
    rules = coherence_rules_from_source(source or {})
    declared = rules.get("slot_context_rules")
    if not isinstance(declared, list):
        return []
    return [rule for rule in declared if isinstance(rule, dict)]


def builtin_slot_context_rules_enabled(source: Optional[JsonDict]) -> bool:
    # Legacy escape hatch: dictionaries that migrated the built-in Python
    # slot-context rules to coherence_rules.slot_context_rules set this false.
    if not source:
        return True
    rules = coherence_rules_from_source(source)
    return bool(rules.get("builtin_slot_context_rules", True))


def rule_slots(rule: JsonDict) -> Set[str]:
    slots = rule.get("slots")
    if isinstance(slots, str):
        return {slots}
    return set(normalize_list(slots))


def conflict_side_matches(side: JsonDict, slot: str, entry: Entry) -> bool:
    if not isinstance(side, dict) or str(side.get("slot") or "") != slot:
        return False
    ids = set(normalize_list(side.get("ids")))
    tokens = set(normalize_list(side.get("tokens")))
    facets = set(normalize_list(side.get("facets")))
    if not ids and not tokens and not facets:
        return False
    if ids and str(entry.get("id", "")) in ids:
        return True
    if tokens and tokens & entry_context_tokens(entry):
        return True
    if facets and facets & facet_tokens(entry):
        return True
    return False


def slot_conflict_violations(
    slot: str,
    item: Entry,
    picked: Dict[str, Entry],
    source: Optional[JsonDict],
    severity: str,
) -> List[JsonDict]:
    violations: List[JsonDict] = []
    for rule in slot_conflict_rules_from_source(source):
        if str(rule.get("severity", "hard")) != severity:
            continue
        left = rule.get("left") or {}
        right = rule.get("right") or {}
        for candidate_side, picked_side in ((left, right), (right, left)):
            if not conflict_side_matches(candidate_side, slot, item):
                continue
            picked_slot = str((picked_side or {}).get("slot") or "")
            entry = picked.get(picked_slot)
            if entry is not None and conflict_side_matches(picked_side, picked_slot, entry):
                violations.append(
                    {
                        "rule_id": str(rule.get("id") or ""),
                        "slot": slot,
                        "item_id": str(item.get("id", "")),
                        "picked_slot": picked_slot,
                        "picked_id": str(entry.get("id", "")),
                        "penalty": float(rule.get("penalty", 0.25)),
                    }
                )
                break
    return violations


def slot_context_rule_violation(
    rule: JsonDict,
    slot: str,
    item: Entry,
    context: Set[str],
    scene_context: Set[str],
) -> bool:
    if slot not in rule_slots(rule):
        return False
    match_ids = set(normalize_list(rule.get("match_ids")))
    match_tokens = set(normalize_list(rule.get("match_tokens")))
    match_facets = set(normalize_list(rule.get("match_facets")))
    if match_ids or match_tokens or match_facets:
        item_tokens = entry_context_tokens(item)
        matched = bool(
            (match_ids and str(item.get("id", "")) in match_ids)
            or (match_tokens and match_tokens & item_tokens)
            or (match_facets and match_facets & facet_tokens(item))
        )
        if not matched:
            return False
    when_context = set(normalize_list(rule.get("when_context_any")))
    if when_context and not (when_context & context):
        return False
    scope_context = scene_context if str(rule.get("context_scope") or "all") == "scene" else context
    requires_context = set(normalize_list(rule.get("requires_context_any")))
    if requires_context and not (requires_context & scope_context):
        return True
    requires_item = set(normalize_list(rule.get("requires_item_any")))
    if requires_item and not (requires_item & entry_context_tokens(item)):
        return True
    return False


def violates_declared_slot_context_rules(
    slot: str,
    item: Entry,
    picked: Dict[str, Entry],
    source: Optional[JsonDict],
) -> bool:
    rules = slot_context_rules_from_source(source)
    if not rules:
        return False
    context = picked_context_tokens(picked)
    scene_context = picked_scene_context_tokens(picked)
    return any(
        slot_context_rule_violation(rule, slot, item, context, scene_context)
        for rule in rules
        if str(rule.get("severity", "hard")) == "hard"
    )


def pending_forced_conflict_entries(
    data: JsonDict,
    forced_choices: Optional[Dict[str, List[str]]],
    picked: Dict[str, Entry],
) -> Dict[str, List[Entry]]:
    """Entries for forced slots that are not picked yet, for look-ahead conflict checks."""
    pending: Dict[str, List[Entry]] = {}
    for slot, forced_ids in (forced_choices or {}).items():
        if slot in picked or not forced_ids:
            continue
        wanted = {str(item_id) for item_id in forced_ids}
        entries = [item for item in data.get("slots", {}).get(slot, []) if str(item.get("id")) in wanted]
        if entries:
            pending[slot] = entries
    return pending


def conflicts_with_all_pending_forced(
    slot: str,
    item: Entry,
    pending: Dict[str, List[Entry]],
    source: Optional[JsonDict],
) -> bool:
    """True when a hard pair rule binds the candidate against EVERY forced
    candidate of some upcoming forced slot — the contradiction is then
    unavoidable, so the free-slot candidate must be filtered now."""
    if not pending or not slot_conflict_rules_from_source(source):
        return False
    for pending_slot, entries in pending.items():
        if not entries:
            continue
        if all(
            slot_conflict_violations(slot, item, {pending_slot: entry}, source, "hard")
            for entry in entries
        ):
            return True
    return False


def apply_slot_conflict_soft_penalties(
    slot: str,
    pool: Sequence[Entry],
    picked: Dict[str, Entry],
    data: JsonDict,
    generation_contract: Optional[JsonDict],
) -> List[Entry]:
    if not picked or not slot_conflict_rules_from_source(data):
        return list(pool)
    adjusted: List[Entry] = []
    penalized: List[JsonDict] = []
    for item in pool:
        violations = slot_conflict_violations(slot, item, picked, data, "soft")
        if not violations:
            adjusted.append(item)
            continue
        factor = 1.0
        for violation in violations:
            penalty = float(violation.get("penalty", 0.25))
            if 0.0 < penalty < 1.0:
                factor *= penalty
        if factor >= 1.0:
            adjusted.append(item)
            continue
        base_weight = item_base_weight(item)
        copied = dict(item)
        copied["weight"] = round(base_weight * factor, 6)
        adjusted.append(copied)
        penalized.append(
            {
                "id": item.get("id"),
                "factor": round(factor, 4),
                "rules": [violation.get("rule_id") for violation in violations],
            }
        )
    if penalized:
        record_generation_contract_event(
            generation_contract,
            "slot_conflict_soft_penalty",
            {
                "slot": slot,
                "reason": "declared_slot_conflict_soft_penalty",
                "reason_code": "declared_slot_conflict_soft_penalty",
                "penalized": penalized,
            },
        )
    return adjusted


MATCH_RULE_KEYS = {
    "id",
    "any_terms",
    "all_terms",
    "any_tokens",
    "all_tokens",
    "boundary",
    "match_fields",
    "case_sensitive",
}


def entry_match_blob(entry: Entry, fields: Sequence[str], case_sensitive: bool = False) -> str:
    blob = " ".join(str(entry.get(key, "")) for key in fields)
    return blob if case_sensitive else blob.lower()


def entry_word_blob(entry: Entry, fields: Sequence[str], case_sensitive: bool = False) -> str:
    return re.sub(r"[_-]+", " ", entry_match_blob(entry, fields, case_sensitive))


def normalize_match_rules(raw: Any) -> List[JsonDict]:
    if raw is None:
        return []
    if isinstance(raw, str):
        return [{"any_terms": [raw]}, {"any_tokens": [raw]}]
    if isinstance(raw, dict):
        if any(key in raw for key in MATCH_RULE_KEYS):
            return [raw]
        rules: List[JsonDict] = []
        for value in raw.values():
            rules.extend(normalize_match_rules(value))
        return rules
    if isinstance(raw, list):
        if all(not isinstance(item, dict) for item in raw):
            terms = normalize_list(raw)
            return [{"any_terms": terms}, {"any_tokens": terms}] if terms else []
        rules = []
        for item in raw:
            rules.extend(normalize_match_rules(item))
        return rules
    return []


def evaluate_match(rule: Any, entry: Entry) -> JsonDict:
    if isinstance(rule, str):
        rule = {"any_terms": [rule]}
    if not isinstance(rule, dict):
        return {"matched": False, "matched_terms": [], "matched_tokens": []}
    fields = normalize_list(rule.get("match_fields")) or ["id", "en", "ko", "embedding_text"]
    case_sensitive = bool(rule.get("case_sensitive"))
    boundary = bool(rule.get("boundary"))
    blob = entry_word_blob(entry, fields, case_sensitive) if boundary else entry_match_blob(entry, fields, case_sensitive)
    tokens = entry_context_tokens(entry) | facet_tokens(entry)
    if case_sensitive:
        normalized_tokens = {str(token) for token in tokens}
    else:
        normalized_tokens = {str(token).lower() for token in tokens}

    def normalize_term(term: str) -> str:
        return str(term) if case_sensitive else str(term).lower()

    def term_in_blob(term: str) -> bool:
        token = normalize_term(term).strip()
        if not token:
            return False
        if boundary:
            return re.search(rf"(?<![a-z0-9]){re.escape(token)}(?![a-z0-9])", blob) is not None
        return token in blob

    any_terms = [normalize_term(term) for term in normalize_list(rule.get("any_terms")) if str(term).strip()]
    all_terms = [normalize_term(term) for term in normalize_list(rule.get("all_terms")) if str(term).strip()]
    any_tokens = [normalize_term(term) for term in normalize_list(rule.get("any_tokens")) if str(term).strip()]
    all_tokens = [normalize_term(term) for term in normalize_list(rule.get("all_tokens")) if str(term).strip()]
    matched_terms = sorted({term for term in any_terms + all_terms if term_in_blob(term)})
    matched_tokens = sorted({term for term in any_tokens + all_tokens if term in normalized_tokens})
    checks: List[bool] = []
    if any_terms:
        checks.append(bool(set(matched_terms) & set(any_terms)))
    if all_terms:
        checks.append(set(all_terms).issubset(set(matched_terms)))
    if any_tokens:
        checks.append(bool(set(matched_tokens) & set(any_tokens)))
    if all_tokens:
        checks.append(set(all_tokens).issubset(set(matched_tokens)))
    matched = bool(checks) and all(checks)
    return {
        "matched": matched,
        "matched_terms": matched_terms,
        "matched_tokens": matched_tokens,
        "matched_rule_id": str(rule.get("id") or "") or None,
    }


def first_policy_match(raw_rules: Any, entry: Entry, matched_via: str) -> Optional[JsonDict]:
    for index, rule in enumerate(normalize_match_rules(raw_rules)):
        result = evaluate_match(rule, entry)
        if not result.get("matched"):
            continue
        rule_id = result.get("matched_rule_id") or f"{matched_via}[{index}]"
        return {
            "matched_via": matched_via,
            "matched_rule_id": rule_id,
            "matched_terms": sorted(set(result.get("matched_terms", [])) | set(result.get("matched_tokens", []))),
        }
    return None


def policy_signal_lexicon_strength(entry: Entry, family: str, source: Optional[JsonDict]) -> tuple[str, Optional[JsonDict]]:
    lexicon = semantic_policy_family_config(source, family).get("signal_lexicon", {}) or {}
    if not isinstance(lexicon, dict):
        return "none", None
    for tier in ("strong", "ambient"):
        matched_via = f"semantic_policy.families.{family}.signal_lexicon.{tier}"
        summary = first_policy_match(lexicon.get(tier), entry, matched_via)
        if summary:
            return tier, summary
    return "none", None


def family_signal_strength_summary(
    entry: Entry,
    family: str,
    rules: Optional[JsonDict] = None,
    slot: str = "",
    source: Optional[JsonDict] = None,
) -> tuple[str, Optional[JsonDict]]:
    rules = rules or {}
    entry_id = str(entry.get("id", ""))
    explicit = family_id_signal_strength(entry_id, family, rules)
    if explicit != "none":
        return explicit, {
            "matched_via": f"coherence_rules.family_strength.{family}.{explicit}",
            "matched_rule_id": entry_id,
            "matched_terms": [],
        }
    metadata_strength = metadata_family_signal_strength(entry, slot, family, source)
    if metadata_strength != "none":
        return metadata_strength, {
            "matched_via": f"semantic_metadata.axis_signals.{family}_{metadata_strength}",
            "matched_rule_id": entry_id,
            "matched_terms": [],
        }
    return policy_signal_lexicon_strength(entry, family, source)


def family_signal_strength(
    entry: Entry,
    family: str,
    rules: Optional[JsonDict] = None,
    slot: str = "",
    source: Optional[JsonDict] = None,
) -> str:
    strength, _summary = family_signal_strength_summary(entry, family, rules, slot, source)
    return strength


def entry_conflicts_with_family(
    entry: Entry,
    slot: str,
    family: str,
    rules: JsonDict,
    source: Optional[JsonDict] = None,
) -> bool:
    family_conflicts = (rules.get("family_conflicts", {}) or {}).get(family, {}) or {}
    if str(entry.get("id", "")) in set(normalize_list(family_conflicts.get(slot))):
        return True
    metadata = semantic_metadata_from_source(source)
    tone_conflicts = ((metadata.get("family_tone_conflicts", {}) or {}).get(family, {}) or {})
    if slot == "location":
        location_tones = set(entry_location_tones(entry, slot, source))
        if location_tones & set(normalize_list(tone_conflicts.get("location_tone"))):
            return True
    return False


def preset_family_signal_strength(preset: Entry, family: str, rules: JsonDict, source: Optional[JsonDict] = None) -> str:
    strength = family_signal_strength(preset, family, rules, "preset", source)
    family_filter_slots = {"mood", "weather", "light_shape", "color", "texture"}
    for slot, slot_filter in (preset.get("filters", {}) or {}).items():
        if slot not in family_filter_slots:
            continue
        for entry_id in normalize_list(slot_filter.get("ids")):
            strength = stronger_family_strength(strength, family_id_signal_strength(entry_id, family, rules))
    return strength


def semantic_coherence_factor(
    item: Entry,
    slot: str,
    context: JsonDict,
    picked: Dict[str, Entry],
    routed_axis_score: Optional[float],
) -> tuple[float, JsonDict]:
    rules = coherence_rules_from_source(context)
    if not rules:
        return 1.0, {"factor": 1.0, "events": []}
    active_families = sorted(context_axis_families(context))
    if not active_families:
        return 1.0, {"factor": 1.0, "events": []}
    config = semantic_profile_config(str(context.get("semantic_profile", "balanced")), context)
    factor = 1.0
    events: List[JsonDict] = []
    for family in active_families:
        routed_slot = slot in semantic_axis_route_slots(context, family)
        strength = family_signal_strength(item, family, rules, slot, context)
        if routed_slot and strength == "strong":
            boost = float(config.get("coherence_strong_boost", 1.18))
            factor *= boost
            events.append({"family": family, "type": "strength_boost", "strength": strength, "factor": round(boost, 4)})
        elif routed_slot and strength == "ambient":
            boost = float(config.get("coherence_ambient_boost", 1.05))
            factor *= boost
            events.append({"family": family, "type": "strength_boost", "strength": strength, "factor": round(boost, 4)})
        elif routed_slot and routed_axis_score is not None:
            floor = float(config.get("routed_axis_floor", 0.10))
            if float(routed_axis_score) < floor:
                penalty = float(config.get("routed_axis_floor_penalty", 0.68))
                factor *= penalty
                events.append(
                    {
                        "family": family,
                        "type": "routed_axis_floor",
                        "score": round(float(routed_axis_score), 4),
                        "floor": round(floor, 4),
                        "factor": round(penalty, 4),
                    }
                )
        if entry_conflicts_with_family(item, slot, family, rules, context):
            penalty = float(config.get("coherence_conflict_penalty", 0.45))
            if context.get("filter_strictness") == "hard":
                penalty = min(penalty, 0.25)
            factor *= penalty
            events.append({"family": family, "type": "family_conflict", "factor": round(penalty, 4)})
    return factor, {"factor": round(factor, 4), "events": events}


def picked_has_family_strength(
    picked: Dict[str, Entry],
    context: JsonDict,
    family: str,
    strength: str,
    slots: Sequence[str],
) -> bool:
    rules = coherence_rules_from_source(context)
    minimum_rank = FAMILY_STRENGTH_RANK.get(strength, 0)
    return any(
        FAMILY_STRENGTH_RANK.get(family_signal_strength(picked[slot], family, rules, slot, context), 0) >= minimum_rank
        for slot in slots
        if slot in picked
    )


def coverage_repair_config(context: Optional[JsonDict], family: str) -> JsonDict:
    config = semantic_policy_family_config(context, family).get("coverage_repair", {}) or {}
    return config if isinstance(config, dict) else {}


def coverage_repair_slots(context: Optional[JsonDict], family: str) -> tuple[str, ...]:
    configured = normalize_list(coverage_repair_config(context, family).get("target_slots"))
    if configured:
        return tuple(configured)
    return ()


def weak_horror_compensation_needed(context: JsonDict, picked: Dict[str, Entry]) -> bool:
    if "horror" not in context_axis_families(context):
        return False
    mood = picked.get("mood")
    if not mood:
        return False
    rules = coherence_rules_from_source(context)
    mood_strength = family_signal_strength(mood, "horror", rules, "mood", context)
    if mood_strength != "ambient":
        return False
    return not picked_has_family_strength(picked, context, "horror", "strong", coverage_repair_slots(context, "horror"))


def weak_horror_compensation_factor(
    item: Entry,
    slot: str,
    context: JsonDict,
    picked: Dict[str, Entry],
) -> tuple[float, JsonDict]:
    if slot not in coverage_repair_slots(context, "horror") or not weak_horror_compensation_needed(context, picked):
        return 1.0, {"active": False, "factor": 1.0}
    rules = coherence_rules_from_source(context)
    strength = family_signal_strength(item, "horror", rules, slot, context)
    if strength != "strong":
        return 1.0, {"active": True, "strength": strength, "factor": 1.0}
    factor = semantic_profile_float(context, "weak_horror_compensation_boost", 1.42)
    return factor, {"active": True, "strength": strength, "factor": round(factor, 4)}


def semantic_preset_family_coverage(preset: Entry, context: JsonDict) -> tuple[float, JsonDict]:
    rules = coherence_rules_from_source(context)
    families = sorted(context_axis_families(context))
    tracked = [family for family in families if family in (rules.get("family_strength", {}) or {})]
    if len(families) < 2 or not tracked:
        return 0.0, {"active": False, "families": []}
    config = semantic_profile_config(str(context.get("semantic_profile", "balanced")), context)
    adjustment = 0.0
    rows: List[JsonDict] = []
    for family in tracked:
        strength = preset_family_signal_strength(preset, family, rules, context)
        if strength == "strong":
            delta = float(config.get("preset_family_strong_bonus", 0.035))
        elif strength == "ambient":
            delta = float(config.get("preset_family_ambient_bonus", 0.012))
        else:
            delta = -float(config.get("preset_family_missing_penalty", 0.065))
        adjustment += delta
        rows.append({"family": family, "strength": strength, "score_adjustment": round(delta, 4)})
    return adjustment, {
        "active": True,
        "score_adjustment": round(adjustment, 4),
        "families": rows,
    }


def intent_steering_enabled(context: Optional[JsonDict]) -> bool:
    if not context:
        return False
    return context.get("intent_steering", {}).get("mode") == "auto"


def make_semantic_context(
    data: JsonDict,
    intent: Optional[str],
    selection_mode: str,
    novelty: str,
    filter_strictness: Optional[str] = None,
    semantic_weight: Optional[float] = None,
    semantic_profile: Optional[str] = None,
    semantic_index_path: Optional[str | Path] = None,
    semantic_index: Optional[JsonDict] = None,
    semantic_provider: str = SEMANTIC_PROVIDER,
    semantic_model: str = SEMANTIC_MODEL_ID,
    semantic_dimensions: int = DEFAULT_SEMANTIC_DIMENSIONS,
    gemini_api_key: Optional[str] = None,
    semantic_axis_mode: str = "auto",
    intent_axes: Optional[Sequence[str]] = None,
    intent_steering: Optional[str] = None,
    intent_source: str = "user",
    semantic_defaulted: bool = False,
    batch_context: Optional[JsonDict] = None,
    creativity: Optional[float] = None,
    novelty_explicit: bool = False,
) -> Optional[JsonDict]:
    resolved_filter, resolved_weight, resolved_profile = resolve_semantic_runtime_options(
        selection_mode,
        filter_strictness,
        semantic_weight,
        semantic_profile,
    )
    if selection_mode == "rule":
        return None
    if not intent:
        raise ValueError("--intent is required when --selection-mode is semantic or hybrid")
    resolved_steering = intent_steering or default_intent_steering(selection_mode)
    if resolved_steering not in INTENT_STEERING_MODES:
        raise ValueError(f"Invalid intent_steering '{resolved_steering}'.")
    index = load_semantic_index(
        semantic_index_path,
        data,
        semantic_index,
        semantic_provider,
        semantic_model,
        semantic_dimensions,
    )
    dimensions = int(index.get("embedding_dimensions", semantic_dimensions))
    semantic_policy = data.get("semantic_policy", {}) or {}
    axis_payload = extract_intent_axes(intent, intent_axes, semantic_axis_mode, intent_source, data)
    query_vector = embed_single_semantic_text(
        intent,
        model=semantic_model,
        dimensions=dimensions,
        api_key=gemini_api_key,
    )
    axis_vectors = []
    for item in axis_payload["items"]:
        text = str(item["text"])
        embedding_text = semantic_axis_embedding_text(text, data)
        families = axis_families_for_text(text, data) or axis_families_for_text(embedding_text, data)
        if clean_intent_axis(embedding_text).lower() == clean_intent_axis(intent).lower():
            vector = query_vector
        else:
            vector = embed_single_semantic_text(
                embedding_text,
                model=semantic_model,
                dimensions=dimensions,
                api_key=gemini_api_key,
            )
        axis_vectors.append(
            {
                "text": text,
                "embedding_text": embedding_text,
                "source": item.get("source", axis_payload["source"]),
                "families": families,
                "vector": vector,
            }
        )
    family_set = sorted({family for item in axis_vectors for family in item.get("families", [])})
    creativity_value: Optional[float] = None
    creativity_overrides: JsonDict = {}
    if creativity is not None:
        creativity_value = clamp_unit_interval(creativity)
        derived = creativity_settings(creativity_value, {"semantic_policy": semantic_policy})
        # Explicit --novelty / --semantic-profile always win over the lever.
        if semantic_profile is None:
            creativity_overrides["profile_config"] = derived["profile_config"]
        if not novelty_explicit:
            creativity_overrides["novelty_settings"] = derived["novelty_settings"]
    context_for_coverage = {
        "semantic_policy": semantic_policy,
        "creativity_overrides": creativity_overrides,
    }
    request_constraints = (
        resolve_request_intent_constraints(data, {"intent": intent}, {})
        if intent_source == "user"
        else {"no_people": False, "subject_categories": [], "domains": [], "matched": [], "source_text_count": 0}
    )
    return {
        "selection_mode": selection_mode,
        "intent": intent,
        "intent_source": intent_source,
        "intent_constraints": request_constraints,
        "preset_domain_map": {
            str(preset.get("id")): sorted(preset_domains(preset, data))
            for preset in data.get("presets", [])
            if isinstance(preset, dict) and preset.get("id")
        },
        "semantic_defaulted": semantic_defaulted,
        "novelty": novelty,
        "filter_strictness": resolved_filter,
        "semantic_weight": resolved_weight,
        "semantic_profile": resolved_profile,
        "creativity": creativity_value,
        "creativity_overrides": creativity_overrides,
        "index": index,
        "coherence_rules": data.get("coherence_rules", {}) or {},
        "semantic_metadata": data.get("semantic_metadata", {}) or {},
        "semantic_policy": semantic_policy,
        "policy_schema_version": semantic_policy_schema_version(data),
        "semantic_policy_hash": semantic_policy_digest(semantic_policy),
        "query_vector": query_vector,
        "semantic_axis_mode": semantic_axis_mode,
        "intent_axes": axis_payload,
        "axis_vectors": axis_vectors,
        "axis_coverage": initial_axis_coverage(axis_vectors, resolved_profile, context_for_coverage),
        "intent_steering": {
            "mode": resolved_steering,
            "enabled": resolved_steering == "auto",
            "families": family_set,
            "decisions": [],
        },
        "surreal_activation_reason": "not_evaluated",
        "surreal_activation_active": False,
        "weak_horror_compensation": {"status": "not_evaluated"},
        "slot_scores": [],
        "preset_score": None,
        "picked_vectors": [],
        "hard_rejected_count": 0,
        "hard_rejected": [],
        "soft_out_of_filter_selected_count": 0,
        "batch_context": batch_context,
        "batch_repetition_penalty": [],
        "dictionary_hash": index.get("dictionary_hash"),
        "semantic_text_recipe": index.get("semantic_text_recipe"),
        "embedding_provider": index.get("provider", SEMANTIC_PROVIDER),
        "embedding_model": index.get("embedding_model", SEMANTIC_MODEL_ID),
        "embedding_dimensions": dimensions,
    }


def semantic_vector(context: JsonDict, key: str) -> List[float]:
    entry = context["index"].get("entries", {}).get(key, {})
    return entry.get("vector", [])


def item_base_weight(item: Entry) -> float:
    try:
        return max(float(item.get("weight", 1)), 0.0)
    except (TypeError, ValueError):
        return 1.0


def preset_filter_match(item: Entry, flt: Optional[JsonDict]) -> Optional[bool]:
    if not flt:
        return None
    return bool(apply_filter([item], flt))


def adult_semantic_tokens(item: Entry) -> Set[str]:
    tokens = entry_tags(item) | entry_kinds(item)
    item_id = str(item.get("id", ""))
    if "adult" in item_id:
        tokens.add("adult")
    if "fetish" in item_id:
        tokens.add("fetish")
    # Some documentary taxonomies carry age-context metadata. That metadata
    # alone must not route an otherwise general scene through adult-content handling.
    if "age_context_only" in tokens:
        tokens.discard("adult")
    return tokens


def compatible_with_semantic_hard_guards(
    item: Entry,
    preset: JsonDict,
    picked: Dict[str, Entry],
    slot: str,
    allow_adult_item: bool = False,
) -> bool:
    if not compatible_with_facet_guards(item, preset, picked):
        return False
    if not preset_uses_adult_context(preset):
        tokens = adult_semantic_tokens(item)
        if tokens & {"adult", "fetish", "suggestive"} and not allow_adult_item:
            return False
        if slot in {"adult_context", "fetish_styling", "body_framing", "caption_context"}:
            return False
    return True


def semantic_facet_match_score(item: Entry, preset: JsonDict, picked: Dict[str, Entry]) -> float:
    item_facets = facet_tokens(item)
    if not item_facets:
        return 0.0
    context = facet_tokens(preset)
    for entry in picked.values():
        context |= facet_tokens(entry)
    if not context:
        return 0.0
    return len(item_facets & context) / max(len(item_facets), 1)


def semantic_filter_factor(context: JsonDict, filter_match: Optional[bool]) -> float:
    strictness = context.get("filter_strictness", "hard")
    if strictness == "off" or filter_match is None:
        return 1.0
    config = semantic_profile_config(str(context.get("semantic_profile", "balanced")), context)
    if filter_match:
        return 1.0 + float(config["filter_bonus"])
    return max(0.01, 1.0 - float(config["filter_penalty"]))


def routed_axis_items(context: JsonDict, slot: str) -> List[JsonDict]:
    routed_families = semantic_axis_routed_families_for_slot(context, slot)
    if not routed_families:
        return []
    return [
        axis
        for axis in context.get("axis_vectors", [])
        if routed_families & set(axis.get("families", []))
    ]


def semantic_axis_relevance(vector: Sequence[float], context: JsonDict, slot: str) -> JsonDict:
    axis_vectors = context.get("axis_vectors", [])
    scored_axes = [
        {
            "text": axis.get("text", ""),
            "families": axis.get("families", []),
            "score": cosine_similarity(axis.get("vector", []), vector),
        }
        for axis in axis_vectors
    ]
    axis_max_item = max(scored_axes, key=lambda item: item["score"], default=None)
    routed = [
        item
        for item in scored_axes
        if set(item.get("families", [])) & semantic_axis_routed_families_for_slot(context, slot)
    ]
    routed_item = max(routed, key=lambda item: item["score"], default=None)
    return {
        "axis_max": float(axis_max_item["score"]) if axis_max_item else 0.0,
        "axis_max_text": axis_max_item.get("text") if axis_max_item else None,
        "routed_axis_score": float(routed_item["score"]) if routed_item else None,
        "routed_axis": routed_item.get("text") if routed_item else None,
        "routed_families": sorted({family for item in routed for family in item.get("families", [])}),
    }


def semantic_axis_coverage_bonus(vector: Sequence[float], context: JsonDict, slot: str) -> float:
    coverage = context.get("axis_coverage", {}) or {}
    axis_vectors = context.get("axis_vectors", [])
    if not coverage or not axis_vectors:
        return 0.0
    routed = routed_axis_items(context, slot)
    routed_indices = {
        index
        for index, axis in enumerate(axis_vectors)
        if any(axis is routed_axis for routed_axis in routed)
    }
    if not routed_indices:
        routed_indices = set(range(len(axis_vectors)))
    target = max(float(coverage.get("target", 0.68)), 0.01)
    bonuses: List[float] = []
    for item in coverage.get("items", []):
        index = int(item.get("index", -1))
        if index not in routed_indices or index < 0 or index >= len(axis_vectors):
            continue
        current = float(item.get("best_score", 0.0))
        deficit = max(0.0, target - current) / target
        if deficit <= 0:
            continue
        axis_score = max(0.0, cosine_similarity(axis_vectors[index].get("vector", []), vector))
        bonuses.append(deficit * axis_score)
    return sum(bonuses) / len(bonuses) if bonuses else 0.0


def active_must_cover_bonus(
    item: Entry,
    vector: Sequence[float],
    context: JsonDict,
    slot: str,
) -> tuple[float, JsonDict]:
    active = context.get("active_must_cover_axis")
    if not active:
        return 0.0, {"active": False, "score": 0.0}
    axis_index = int(active.get("index", -1))
    axis_vectors = context.get("axis_vectors", [])
    if axis_index < 0 or axis_index >= len(axis_vectors):
        return 0.0, {"active": False, "score": 0.0}
    families = set(axis_vectors[axis_index].get("families", []))
    routed_slots = {routed_slot for family in families for routed_slot in semantic_axis_route_slots(context, family)}
    if routed_slots and slot not in routed_slots:
        return 0.0, {
            "active": True,
            "axis": active.get("text", ""),
            "score": 0.0,
            "reason": "slot_not_routed",
        }
    axis_score = max(0.0, cosine_similarity(axis_vectors[axis_index].get("vector", []), vector))
    strength = "none"
    for family in families:
        strength = stronger_family_strength(
            strength,
            family_signal_strength(item, family, coherence_rules_from_source(context), slot, context),
        )
    strength_bonus = 0.0
    if strength == "strong":
        strength_bonus = 0.24
    elif strength == "ambient":
        strength_bonus = 0.11
    score = min(1.2, axis_score + strength_bonus)
    return score, {
        "active": True,
        "axis": active.get("text", ""),
        "families": sorted(families),
        "score": round(score, 4),
        "axis_score": round(axis_score, 4),
        "strength": strength,
    }


def entry_cliche_weight(item: Entry, slot: str, context: JsonDict) -> float:
    raw = item.get("cliche_weight", 0.0)
    metadata = semantic_metadata_from_source(context)
    metadata_weights = ((metadata.get("cliche_weights", {}) or {}).get(slot, {}) or {})
    if str(item.get("id", "")) in metadata_weights:
        raw = metadata_weights[str(item.get("id", ""))]
    try:
        return max(0.0, min(1.0, float(raw)))
    except (TypeError, ValueError):
        return 0.0


def semantic_cliche_factor(item: Entry, slot: str, context: JsonDict, effective_query_score: float) -> tuple[float, JsonDict]:
    cliche = entry_cliche_weight(item, slot, context)
    if cliche <= 0.0 or slot not in COHERENT_DIVERSITY_SLOTS or effective_query_score < 0.78:
        return 1.0, {"active": False, "factor": 1.0, "cliche_weight": round(cliche, 4)}
    penalty_weight = semantic_profile_float(context, "cliche_penalty_weight", 0.24)
    dominance = min(1.0, max(0.0, (effective_query_score - 0.78) / 0.22))
    factor = max(0.58, 1.0 - (penalty_weight * cliche * dominance))
    return factor, {
        "active": True,
        "factor": round(factor, 4),
        "cliche_weight": round(cliche, 4),
        "effective_query": round(effective_query_score, 4),
    }


def semantic_contextual_affinity(
    slot: str,
    item: Entry,
    vector: Sequence[float],
    context: JsonDict,
    picked: Dict[str, Entry],
) -> tuple[float, JsonDict]:
    context_vectors: List[tuple[str, str, List[float]]] = []
    for context_slot in CROSS_SLOT_AFFINITY_CONTEXT_SLOTS.get(slot, ()):
        entry = picked.get(context_slot)
        if entry:
            context_vectors.append(
                (
                    context_slot,
                    str(entry.get("id", "")),
                    semantic_vector(context, semantic_entry_key("slot", entry, context_slot)),
                )
            )
    scores = [
        {
            "slot": context_slot,
            "id": entry_id,
            "score": cosine_similarity(vector, context_vector),
        }
        for context_slot, entry_id, context_vector in context_vectors
        if context_vector
    ]
    best = max(scores, key=lambda row: row["score"], default=None)
    score = float(best["score"]) if best else 0.0
    events: List[JsonDict] = []
    if best:
        events.append({"type": "picked_slot_affinity", **best, "score": round(float(best["score"]), 4)})
    fantasy_bonus = 0.0
    if slot == "surreal_anchor" and "fantasy" in context_axis_families(context):
        if family_signal_strength(item, "fantasy", coherence_rules_from_source(context), slot, context) == "strong":
            fantasy_bonus = 0.08
            score += fantasy_bonus
            events.append({"type": "fantasy_anchor_bonus", "score": round(fantasy_bonus, 4)})
    return score, {"score": round(score, 4), "events": events}


def semantic_candidate_weight(
    item: Entry,
    vector: Sequence[float],
    context: JsonDict,
    preset_vector: Sequence[float],
    preset: JsonDict,
    picked: Dict[str, Entry],
    slot: str,
    filter_match: Optional[bool] = None,
) -> tuple[float, JsonDict]:
    query_score = cosine_similarity(context["query_vector"], vector)
    axis = semantic_axis_relevance(vector, context, slot)
    axis_max = float(axis["axis_max"])
    routed_axis_score = axis.get("routed_axis_score")
    if routed_axis_score is not None:
        effective_query_score = (0.72 * float(routed_axis_score)) + (0.18 * axis_max) + (0.10 * query_score)
    else:
        effective_query_score = max(query_score, (0.65 * axis_max) + (0.35 * query_score))
    coverage_bonus = semantic_axis_coverage_bonus(vector, context, slot)
    must_cover_bonus, must_cover_summary = active_must_cover_bonus(item, vector, context, slot)
    contextual_score, contextual_summary = semantic_contextual_affinity(slot, item, vector, context, picked)
    coherence_factor, coherence_summary = semantic_coherence_factor(item, slot, context, picked, routed_axis_score)
    weak_horror_factor, weak_horror_summary = weak_horror_compensation_factor(item, slot, context, picked)
    preset_score = cosine_similarity(preset_vector, vector) if preset_vector else 0.0
    facet_score = semantic_facet_match_score(item, preset, picked)
    redundancy = 0.0
    if context.get("picked_vectors"):
        redundancy = max(cosine_similarity(vector, picked) for picked in context["picked_vectors"])
    temperature, novelty_scale = novelty_settings(context["novelty"], context)
    temperature *= semantic_profile_config(str(context.get("semantic_profile", "balanced")), context)["temperature_multiplier"]
    slot_temperature_multiplier = SLOT_TEMPERATURE_MULTIPLIERS.get(slot, 1.0)
    temperature *= slot_temperature_multiplier
    novelty_weight = 0.0
    try:
        novelty_weight = float(item.get("novelty_weight", 0.0))
    except (TypeError, ValueError):
        novelty_weight = 0.0

    semantic_weight = float(context.get("semantic_weight", default_semantic_weight(context["selection_mode"])))
    coverage_weight = semantic_profile_float(context, "axis_coverage_weight", 0.22)
    must_cover_weight = semantic_profile_float(context, "must_cover_weight", 0.42)
    contextual_weight = semantic_profile_float(context, "cross_slot_affinity_weight", 0.16)
    if slot in COHERENT_DIVERSITY_SLOTS and routed_axis_score is None:
        relevance = (
            (0.36 * effective_query_score)
            + (0.12 * query_score)
            + (0.24 * preset_score)
            + (0.12 * facet_score)
            + (coverage_weight * coverage_bonus)
            + (contextual_weight * contextual_score)
            + (must_cover_weight * must_cover_bonus)
        )
    else:
        relevance = (
            (0.50 * effective_query_score)
            + (0.16 * query_score)
            + (0.18 * preset_score)
            + (0.10 * facet_score)
            + (coverage_weight * coverage_bonus)
            + (contextual_weight * contextual_score)
            + (must_cover_weight * must_cover_bonus)
        )
    redundancy_scale = 0.55 if slot in SURREAL_LAYER_SLOTS else 1.0
    redundancy_relief = 1.0
    if contextual_score > 0.65:
        relief = semantic_profile_float(context, "contextual_redundancy_relief", 0.24)
        redundancy_relief = max(0.58, 1.0 - (relief * min(1.0, (contextual_score - 0.65) / 0.35)))
    effective_redundancy = redundancy * redundancy_scale * redundancy_relief
    mmr_affinity = (semantic_weight * relevance) - ((1.0 - semantic_weight) * effective_redundancy)
    affinity = mmr_affinity + (novelty_scale * novelty_weight)
    semantic_multiplier = math.exp(max(min(affinity, 3.0), -3.0) / max(temperature, 0.1))
    base_power = semantic_base_power(context)
    weighted = (max(item_base_weight(item), 0.01) ** base_power) * (semantic_multiplier ** semantic_weight)
    weighted *= semantic_filter_factor(context, filter_match)
    weighted *= coherence_factor
    weighted *= weak_horror_factor
    cliche_factor, cliche_summary = semantic_cliche_factor(item, slot, context, effective_query_score)
    weighted *= cliche_factor
    batch_penalty, batch_summary = batch_diversity_penalty(context, slot, str(item.get("id")), vector)
    weighted *= batch_penalty
    batch_group_penalty, batch_group_summary = batch_group_diversity_penalty(context, slot, item, vector)
    weighted *= batch_group_penalty
    return weighted, {
        "id": item.get("id"),
        "weight": round(weighted, 6),
        "query": round(query_score, 4),
        "effective_query": round(effective_query_score, 4),
        "preset": round(preset_score, 4),
        "facet": round(facet_score, 4),
        "contextual": round(contextual_score, 4),
        "cross_slot_affinity": contextual_summary,
        "coherence": coherence_summary,
        "weak_horror_compensation": weak_horror_summary,
        "must_cover": must_cover_summary,
        "cliche": cliche_summary,
        "relevance": round(relevance, 4),
        "temperature_multiplier": round(slot_temperature_multiplier, 4),
        "redundancy": round(redundancy, 4),
        "effective_redundancy": round(effective_redundancy, 4),
        "redundancy_relief": round(redundancy_relief, 4),
        "batch_penalty": batch_summary,
        "batch_group_penalty": batch_group_summary,
        "axis": {
            "axis_max": round(axis_max, 4),
            "axis_max_text": axis.get("axis_max_text"),
            "routed_axis": axis.get("routed_axis"),
            "routed_score": None if routed_axis_score is None else round(float(routed_axis_score), 4),
            "routed_families": axis.get("routed_families", []),
            "coverage_bonus": round(coverage_bonus, 4),
        },
        "filter": "none" if filter_match is None else ("in" if filter_match else "out"),
    }


def semantic_preset_candidate_weight(preset: Entry, score: float, context: JsonDict) -> float:
    temperature, novelty_scale = novelty_settings(context["novelty"], context)
    temperature *= semantic_profile_config(str(context.get("semantic_profile", "balanced")), context)["temperature_multiplier"]
    base = max(item_base_weight(preset), 0.01)
    novelty_weight = 0.0
    try:
        novelty_weight = float(preset.get("novelty_weight", 0.0))
    except (TypeError, ValueError):
        novelty_weight = 0.0
    affinity = max(min(score + (novelty_scale * novelty_weight), 3.0), -3.0)
    semantic_weight = float(context.get("semantic_weight", default_semantic_weight(context["selection_mode"])))
    return (base ** 0.35) * (math.exp(affinity / max(temperature * 0.45, 0.1)) ** semantic_weight)


def semantic_preset_score_window(context: JsonDict) -> float:
    base = semantic_profile_config(str(context.get("semantic_profile", "balanced")), context)["preset_window"]
    novelty = context.get("novelty", "medium")
    if novelty == "low":
        requested_typed_domains = (
            set(normalize_list((context.get("intent_constraints") or {}).get("domains")))
            & STRICT_TAG_FACET_SOURCE_DOMAINS
        )
        if requested_typed_domains:
            # Evidence-led operational packs prioritize subtype fidelity over
            # sibling-preset variety at low novelty.  Broader creative modes
            # keep the normal window.
            return max(0.02, min(0.04, base * 0.35))
        return max(0.04, base * 0.65)
    if novelty == "high":
        return min(0.32, base * 1.35)
    return base


def semantic_preset_candidate_limit(context: JsonDict) -> int:
    config = semantic_profile_config(str(context.get("semantic_profile", "balanced")), context)
    limit = int(config.get("preset_candidate_limit", 8))
    novelty = context.get("novelty", "medium")
    if novelty == "low":
        return max(3, int(round(limit * 0.7)))
    if novelty == "high":
        return max(limit + 2, int(round(limit * 1.35)))
    return limit


def semantic_preset_weight_floor(context: JsonDict) -> float:
    config = semantic_profile_config(str(context.get("semantic_profile", "balanced")), context)
    floor = float(config.get("preset_weight_floor", 0.82))
    novelty = context.get("novelty", "medium")
    if novelty == "low":
        return min(0.94, floor + 0.06)
    if novelty == "high":
        return max(0.55, floor - 0.10)
    return floor


def semantic_preset_score_breakdown(vector: Sequence[float], context: JsonDict, preset: Optional[Entry] = None) -> tuple[float, JsonDict]:
    overall = cosine_similarity(context["query_vector"], vector)
    axis_vectors = context.get("axis_vectors") or [
        {"text": context.get("intent", ""), "source": "full_intent", "vector": context["query_vector"]}
    ]
    axis_scores = [
            {
                "text": item.get("text", ""),
                "embedding_text": item.get("embedding_text", item.get("text", "")),
                "source": item.get("source", "full_intent"),
                "score": cosine_similarity(item.get("vector", []), vector),
            }
        for item in axis_vectors
    ]
    raw_scores = [item["score"] for item in axis_scores]
    axis_mean = sum(raw_scores) / len(raw_scores) if raw_scores else overall
    axis_floor = min(raw_scores) if raw_scores else overall
    config = semantic_profile_config(str(context.get("semantic_profile", "balanced")), context)
    overall_weight = float(config.get("preset_overall_weight", 0.45))
    axis_mean_weight = float(config.get("preset_axis_mean_weight", 0.35))
    axis_floor_weight = float(config.get("preset_axis_floor_weight", 0.20))
    total = max(overall_weight + axis_mean_weight + axis_floor_weight, 0.01)
    semantic_score = (
        (overall_weight * overall)
        + (axis_mean_weight * axis_mean)
        + (axis_floor_weight * axis_floor)
    ) / total
    family_adjustment = 0.0
    family_coverage: JsonDict = {"active": False, "families": []}
    if preset is not None:
        family_adjustment, family_coverage = semantic_preset_family_coverage(preset, context)
        semantic_score += family_adjustment
    return semantic_score, {
        "query": round(overall, 4),
        "overall": round(overall, 4),
        "axis_mean": round(axis_mean, 4),
        "axis_floor": round(axis_floor, 4),
        "axis_scores": [
            {
                "text": item["text"],
                "embedding_text": item["embedding_text"],
                "source": item["source"],
                "score": round(float(item["score"]), 4),
            }
            for item in axis_scores
        ],
        "semantic_score": round(semantic_score, 4),
        "family_coverage": family_coverage,
    }


def semantic_intent_allows_adult_context(context: JsonDict) -> bool:
    axis_text = " ".join(
        str(item.get("text", ""))
        for item in (context.get("intent_axes", {}) or {}).get("items", [])
    )
    text = f"{context.get('intent', '')} {axis_text}".lower()
    adult_terms = {
        "adult",
        "fetish",
        "boudoir",
        "lingerie",
        "sensual",
        "suggestive",
        "성인",
        "페티시",
    }
    return any(term in text for term in adult_terms)


def preset_denied_anchor_slot(
    preset: Entry,
    soft_policy: Optional[JsonDict],
    data: JsonDict,
) -> Optional[str]:
    """First soft-anchor slot this preset's domains would deny, if any.

    A preset whose domains block an anchor slot via slot_applicability makes
    that anchor permanently unreachable (repair cannot fill a denied slot), so
    preset choice must avoid it up front.
    """
    if not soft_policy:
        return None
    slots = {str(anchor.get("slot") or "") for anchor in (soft_policy.get("anchors") or [])}
    if not slots:
        return None
    domains = preset_domains(preset, data)
    if not domains:
        return None
    for slot in sorted(slots):
        policy = slot_applicability_policy(data, slot)
        if not policy:
            continue
        if domains & set(normalize_list(policy.get("deny_domains"))):
            return slot
    return None


def compatible_preset_with_semantic_hard_guards(
    preset: Entry,
    context: JsonDict,
    relax_family_policy: bool = False,
) -> tuple[bool, Optional[str]]:
    if preset_uses_adult_context(preset) and not semantic_intent_allows_adult_context(context):
        return False, "adult_context"
    tokens = facet_tokens(preset)
    if "safety_tier:adult_only" in tokens and not semantic_intent_allows_adult_context(context):
        return False, "adult_only"
    requested_typed_domains = (
        set(normalize_list((context.get("intent_constraints") or {}).get("domains")))
        & STRICT_TAG_FACET_SOURCE_DOMAINS
    )
    if requested_typed_domains:
        domain_map = context.get("preset_domain_map") if isinstance(context.get("preset_domain_map"), dict) else {}
        candidate_domains = set(normalize_list(domain_map.get(str(preset.get("id")))))
        if not (requested_typed_domains & candidate_domains):
            return False, "typed_intent_domain"
    if not relax_family_policy:
        for family in sorted(context_axis_families(context)):
            preset_policy = family_preset_policy(context, family)
            if preset_policy and not preset_has_family_policy_signal(preset, context, family):
                return False, f"{family}_preset"
    return True, None


def semantic_slot_score_window(context: JsonDict) -> float:
    base = semantic_profile_config(str(context.get("semantic_profile", "balanced")), context)["slot_window"]
    novelty = context.get("novelty", "medium")
    if novelty == "low":
        return max(0.04, base * 0.65)
    if novelty == "high":
        return min(0.34, base * 1.35)
    return base


def semantic_slot_candidate_limit(context: JsonDict, slot: Optional[str] = None) -> int:
    config = semantic_profile_config(str(context.get("semantic_profile", "balanced")), context)
    limit = int(config.get("slot_candidate_limit", 8))
    if slot in COHERENT_DIVERSITY_SLOTS:
        limit += 4
    novelty = context.get("novelty", "medium")
    if novelty == "low":
        return max(3, int(round(limit * 0.7)))
    if novelty == "high":
        return max(limit + 2, int(round(limit * 1.35)))
    return limit


def semantic_slot_weight_floor(context: JsonDict, slot: Optional[str] = None) -> float:
    config = semantic_profile_config(str(context.get("semantic_profile", "balanced")), context)
    floor = float(config.get("slot_weight_floor", 0.82))
    if slot in COHERENT_DIVERSITY_SLOTS:
        floor = max(0.58, floor - 0.12)
    novelty = context.get("novelty", "medium")
    if novelty == "low":
        return min(0.94, floor + 0.06)
    if novelty == "high":
        return max(0.55, floor - 0.10)
    return floor


def semantic_weighted_choice(
    pool: Sequence[Entry],
    rng: random.Random,
    slot: str,
    preset: JsonDict,
    context: Optional[JsonDict],
    forced: bool = False,
    slot_filter: Optional[JsonDict] = None,
    picked: Optional[Dict[str, Entry]] = None,
) -> Entry:
    if not context or forced:
        return weighted_choice(pool, rng)

    preset_key = semantic_entry_key("preset", preset)
    preset_vector = semantic_vector(context, preset_key)
    weights: List[float] = []
    scored: List[JsonDict] = []
    vectors: Dict[str, List[float]] = {}
    scored_items: List[tuple[Entry, List[float], Optional[bool], float, float, JsonDict]] = []

    for item in pool:
        key = semantic_entry_key("slot", item, slot)
        vector = semantic_vector(context, key)
        vectors[str(item.get("id"))] = vector
        filter_match = preset_filter_match(item, slot_filter)
        weight, summary = semantic_candidate_weight(
            item,
            vector,
            context,
            preset_vector,
            preset,
            picked or {},
            slot,
            filter_match,
        )
        scored_items.append((item, vector, filter_match, weight, float(summary.get("effective_query", summary["query"])), summary))
        scored.append(summary)

    if context.get("filter_strictness") == "soft" and slot_filter:
        best_query = max((query for _, _, _, _, query, _ in scored_items), default=0.0)
        score_window = semantic_slot_score_window(context)
        eligible = [
            row
            for row in scored_items
            if row[2] is not False or row[4] >= best_query - score_window
        ]
    else:
        score_window = None
        eligible = scored_items

    ordered = sorted(eligible, key=lambda row: row[3], reverse=True)
    if ordered:
        best_weight = max(ordered[0][3], 0.01)
        floor = best_weight * semantic_slot_weight_floor(context, slot)
        floored = [row for row in ordered if row[3] >= floor]
        limit = semantic_slot_candidate_limit(context, slot)
        minimum_size = 1 if context.get("filter_strictness") == "soft" and slot_filter else 3
        minimum = min(minimum_size, len(ordered), limit)
        candidates = floored[:limit]
        if len(candidates) < minimum:
            candidates = ordered[:minimum]
    else:
        candidates = []

    # Soft-anchor reinjection: pool members pruned by the weight floor or the
    # candidate limit re-enter the window so the probability floor can act.
    anchor_reinjection_summary: Optional[JsonDict] = None
    soft_policy = ((context or {}).get("generation_contract", {}) or {}).get("soft_anchor_policy", {})
    reinjection_anchor_ids = soft_anchor_pool_for_slot(soft_policy, slot)
    if reinjection_anchor_ids and candidates:
        candidate_ids = {str(row[0].get("id")) for row in candidates}
        missing_rows = [
            row
            for row in ordered
            if str(row[0].get("id")) in reinjection_anchor_ids and str(row[0].get("id")) not in candidate_ids
        ]
        reinjection_limit = int(
            semantic_policy_float(context, ("soft_anchor_diversity", "candidate_reinjection_limit"), 2)
        )
        if missing_rows and reinjection_limit > 0:
            injected = missing_rows[:reinjection_limit]
            candidates = list(candidates) + injected
            anchor_reinjection_summary = {
                "ids": [str(row[0].get("id")) for row in injected],
                "count": len(injected),
            }

    for item, _vector, _filter_match, weight, _query, _summary in candidates:
        weights.append(weight)

    anchor_probability_summary: Optional[JsonDict] = None
    if context and not forced:
        weights, anchor_probability_summary = apply_soft_anchor_probability_floor(slot, candidates, weights, context)

    if sum(weights) <= 0:
        selected = rng.choice([item for item, *_ in candidates] or list(pool))
    else:
        selected = rng.choices([item for item, *_ in candidates], weights=weights, k=1)[0]

    # Anchor-pool enforcement: concept anchor slots must stay inside the pool
    # (related randomness happens among pool members); leakage to non-pool
    # candidates is the job of the opt-in anchor_expansion, not the sampler.
    anchor_enforced = False
    if (
        reinjection_anchor_ids
        and str(selected.get("id")) not in reinjection_anchor_ids
        and semantic_policy_float(context, ("soft_anchor_diversity", "anchor_pool_enforcement"), 1.0) >= 1.0
    ):
        anchor_rows = [
            (row, weight)
            for row, weight in zip(candidates, weights)
            if str(row[0].get("id")) in reinjection_anchor_ids
        ]
        if anchor_rows:
            anchor_weights = [max(weight, 0.000001) for _, weight in anchor_rows]
            selected = rng.choices([row[0] for row, _ in anchor_rows], weights=anchor_weights, k=1)[0]
            anchor_enforced = True

    selected_id = str(selected.get("id"))
    if vectors.get(selected_id):
        context["picked_vectors"].append(vectors[selected_id])
        update_axis_coverage(context, slot, selected_id, vectors[selected_id], selected)
    selected_filter = preset_filter_match(selected, slot_filter)
    if context.get("filter_strictness") == "soft" and selected_filter is False:
        context["soft_out_of_filter_selected_count"] = int(context.get("soft_out_of_filter_selected_count", 0)) + 1
    top_scores = sorted(scored, key=lambda item: item["weight"], reverse=True)[:5]
    summary_by_id = {str(item.get("id")): item for item in scored}
    selected_batch_penalty = summary_by_id.get(selected_id, {}).get("batch_penalty")
    selected_batch_group_penalty = summary_by_id.get(selected_id, {}).get("batch_group_penalty")
    if selected_batch_penalty:
        context.setdefault("batch_repetition_penalty", []).append(selected_batch_penalty)
    if selected_batch_group_penalty and selected_batch_group_penalty.get("enabled"):
        context.setdefault("batch_repetition_penalty", []).append(selected_batch_group_penalty)
    context["slot_scores"].append(
        {
            "slot": slot,
            "selected": selected_id,
            "top": top_scores,
            "candidate_count": len(candidates),
            "candidate_limit": semantic_slot_candidate_limit(context, slot),
            "weight_floor": semantic_slot_weight_floor(context, slot),
            "score_window": score_window,
            "selected_filter": "none" if selected_filter is None else ("in" if selected_filter else "out"),
            "batch_penalty": selected_batch_penalty,
            "batch_group_penalty": selected_batch_group_penalty,
            "anchor_probability_floor": anchor_probability_summary,
            "anchor_reinjection": anchor_reinjection_summary,
            "anchor_enforced": anchor_enforced,
        }
    )
    return selected


def materialize_virtual_preset(data: JsonDict, preset_id: str) -> Optional[JsonDict]:
    recipe_id = preset_id.removeprefix("virtual:")
    recipe = next((item for item in data.get("recipes", []) if item.get("id") == recipe_id), None)
    if not recipe:
        return None
    base = next((item for item in data.get("presets", []) if item.get("id") == recipe.get("base_preset")), None)
    if not base:
        return None
    preset = dict(base)
    preset["id"] = f"virtual:{recipe_id}"
    preset["ko"] = recipe.get("ko", base.get("ko"))
    preset["en"] = recipe.get("en", base.get("en"))
    preset["weight"] = recipe.get("weight", base.get("weight", 1))
    preset["semantic_anchor"] = recipe.get("semantic_anchor", recipe.get("embedding_text", ""))
    preset["facets"] = recipe.get("facets", {})
    preset["hard_guards"] = recipe.get("hard_guards", {})
    filters = dict(base.get("filters", {}))
    filters.update(recipe.get("filters", {}))
    preset["filters"] = filters
    return preset


def preset_affinity_blob(preset: JsonDict, data: JsonDict) -> str:
    parts: List[str] = [
        str(preset.get("id", "")),
        str(preset.get("en", "")),
        str(preset.get("ko", "")),
        " ".join(normalize_list(preset.get("tags"))),
        " ".join(sorted(preset_domains(preset, data))),
    ]
    return " ".join(part.lower() for part in parts if part)


def preset_affinity_matches(preset: JsonDict, data: JsonDict, ids: Sequence[str], axes: Sequence[str]) -> List[str]:
    preset_id = str(preset.get("id") or "")
    matches = [item for item in normalize_list(ids) if item == preset_id]
    blob = preset_affinity_blob(preset, data)
    for axis in normalize_list(axes):
        axis_text = str(axis).lower().replace("_", " ")
        if axis_text and axis_text in blob.replace("_", " "):
            matches.append(str(axis))
    return sorted(set(matches))


def soft_preset_affinity_factor(preset: JsonDict, policy: Optional[JsonDict], data: JsonDict) -> tuple[float, JsonDict]:
    affinity = (policy or {}).get("preset_affinity", {}) or {}
    if not affinity:
        return 1.0, {"applied": False}
    preferred = preset_affinity_matches(
        preset,
        data,
        normalize_list(affinity.get("preferred_presets")),
        normalize_list(affinity.get("preferred_axes")),
    )
    discouraged = preset_affinity_matches(
        preset,
        data,
        normalize_list(affinity.get("discouraged_presets")),
        normalize_list(affinity.get("discouraged_axes")),
    )
    factor = 1.0
    if preferred:
        factor *= max(1.0, semantic_policy_float(data, ("preset_affinity", "preferred_multiplier"), 1.35))
    if discouraged:
        factor *= 0.35
    return factor, {
        "applied": bool(preferred or discouraged),
        "factor": round(factor, 4),
        "preferred_matches": preferred,
        "discouraged_matches": discouraged,
    }


def preset_filter_ids_for_slot(preset: JsonDict, slot: str) -> Set[str]:
    raw = (preset.get("filters") or {}).get(slot)
    if isinstance(raw, dict):
        values = normalize_list(raw.get("ids") or raw.get("allow") or raw.get("any_of"))
    else:
        values = normalize_list(raw)
    return {str(value) for value in values if str(value).strip()}


def role_scene_policy_factor(preset: JsonDict, policy: Optional[JsonDict]) -> tuple[float, JsonDict]:
    role_policy = normalize_role_scene_policy((policy or {}).get("role_scene_policy"))
    if not role_policy.get("enabled"):
        return 1.0, {"applied": False}
    preset_id = str(preset.get("id") or "")
    location_ids = preset_filter_ids_for_slot(preset, "location")
    mood_ids = preset_filter_ids_for_slot(preset, "mood")
    allowed_locations = set(normalize_list(role_policy.get("allowed_locations")))
    preferred_locations = set(normalize_list(role_policy.get("preferred_locations"))) or allowed_locations
    forbidden_locations = set(normalize_list(role_policy.get("forbidden_locations")))
    forbidden_locations.update(normalize_list(role_policy.get("discouraged_generic_locations")))
    discouraged_moods = set(normalize_list(role_policy.get("discouraged_generic_moods")))
    support_presets = set(normalize_list(role_policy.get("support_presets")))
    discouraged_presets = set(normalize_list(role_policy.get("discouraged_presets")))

    factor = 1.0
    reasons: List[str] = []
    allowed_hit = bool(location_ids & allowed_locations)
    preferred_hit = bool(location_ids & preferred_locations)
    forbidden_hit = bool(location_ids & forbidden_locations)
    mood_hit = bool(mood_ids & discouraged_moods)

    if preferred_hit:
        factor *= 1.25
        reasons.append("preferred_role_location")
    elif allowed_hit:
        factor *= 1.12
        reasons.append("allowed_role_location")

    if preset_id in support_presets:
        if allowed_locations and role_policy.get("generic_preset_support_only_when_role_scene_missing"):
            factor *= 0.55
            reasons.append("generic_support_deferred_to_role_scene")
        else:
            factor *= 1.08
            reasons.append("support_preset")

    if preset_id in discouraged_presets:
        factor *= 0.2
        reasons.append("discouraged_preset")
    if forbidden_hit and not allowed_hit:
        factor *= 0.05 if role_policy.get("enforce") else 0.35
        reasons.append("forbidden_role_location")
    if mood_hit:
        factor *= 0.35
        reasons.append("discouraged_generic_mood")
    if allowed_locations and location_ids and not allowed_hit and role_policy.get("role_first"):
        factor *= 0.35 if role_policy.get("enforce") else 0.65
        reasons.append("preset_location_outside_role_pool")

    return factor, {
        "applied": bool(reasons),
        "factor": round(factor, 4),
        "scene_family": role_policy.get("scene_family"),
        "preset_locations": sorted(location_ids),
        "preset_moods": sorted(mood_ids),
        "reasons": reasons,
    }


def soft_preset_affinity_status(preset: JsonDict, policy: Optional[JsonDict], data: JsonDict, forced: bool) -> JsonDict:
    factor, summary = soft_preset_affinity_factor(preset, policy, data)
    if not forced or not summary.get("discouraged_matches"):
        return {"status": "pass", "forced": forced, **summary}
    return {
        "status": "warn",
        "forced": True,
        "policy_conflict": "preset_concept_conflict",
        **summary,
    }


def preset_matches_automatic_intent_scope(
    preset: JsonDict,
    data: JsonDict,
    semantic_context: Optional[JsonDict],
) -> bool:
    """Keep on-demand typed packs out of unrelated automatic selection.

    Direct preset selection is handled before this predicate. Automatic
    semantic discovery admits the pack only when the user-authored intent was
    routed to the same typed domain.
    """
    if preset.get("automatic_discovery") is False:
        return False
    requested_domains = {
        str(value)
        for value in normalize_list(
            ((semantic_context or {}).get("intent_constraints") or {}).get("domains")
        )
    }
    matched_routes = {
        str(value)
        for value in normalize_list(
            ((semantic_context or {}).get("intent_constraints") or {}).get("scoped_routes")
        )
    }
    if (
        semantic_context
        and semantic_context.get("intent_source") == "user"
        and matched_routes
        and requested_domains
        & {"subculture_practice", "worldbuilding_system", "cjk_narrative_world", "character_moe_grammar"}
    ):
        # An explicit scoped-route alias is a stronger signal than embedding
        # similarity. Keep generic presets from competing with the named route
        # (for example, civic solarpunk versus a generic climate record).
        return str(preset.get("id") or "") in matched_routes
    scoped_domains = preset_domains(preset, data) & INTENT_SCOPED_PRESET_DOMAINS
    if not scoped_domains:
        return True
    if not semantic_context or semantic_context.get("intent_source") != "user":
        return False
    if not (scoped_domains & requested_domains):
        return False
    return True


def choose_preset(
    data: JsonDict,
    rng: random.Random,
    preset_id: Optional[str] = None,
    semantic_context: Optional[JsonDict] = None,
    soft_anchor_spec: Optional[JsonDict] = None,
) -> JsonDict:
    catalog_presets = data.get("presets", [])
    if not catalog_presets:
        raise ValueError("No presets found in JSON.")

    if preset_id:
        for p in catalog_presets:
            if p.get("id") == preset_id:
                return p
        virtual = materialize_virtual_preset(data, preset_id)
        if virtual:
            return virtual
        valid = ", ".join(p.get("id", "?") for p in catalog_presets)
        raise ValueError(f"Unknown preset '{preset_id}'. Available presets: {valid}")

    presets = [
        preset
        for preset in catalog_presets
        if preset_matches_automatic_intent_scope(preset, data, semantic_context)
    ]
    if not presets:
        raise ValueError("No presets remain after applying automatic intent scope.")

    if semantic_context:
        soft_policy = normalize_soft_anchor_spec(soft_anchor_spec)
        scored_presets: List[tuple[JsonDict, float, float, JsonDict]] = []
        summaries: List[JsonDict] = []
        rejected_by_reason: Dict[str, int] = {}
        guard_relaxed = False
        for relax_family_policy in (False, True):
            for preset in presets:
                allowed, reason = compatible_preset_with_semantic_hard_guards(
                    preset, semantic_context, relax_family_policy=relax_family_policy
                )
                if not allowed:
                    if not relax_family_policy:
                        rejected_by_reason[str(reason or "hard_guard")] = rejected_by_reason.get(str(reason or "hard_guard"), 0) + 1
                    continue
                denied_slot = preset_denied_anchor_slot(preset, soft_policy, data)
                if denied_slot:
                    if not relax_family_policy:
                        key = f"anchor_slot_domain:{denied_slot}"
                        rejected_by_reason[key] = rejected_by_reason.get(key, 0) + 1
                    continue
                vector = semantic_vector(semantic_context, semantic_entry_key("preset", preset))
                score, score_summary = semantic_preset_score_breakdown(vector, semantic_context, preset)
                weight = semantic_preset_candidate_weight(preset, score, semantic_context)
                balance_factor, balance_themes = selection_balance_multiplier(
                    data,
                    preset,
                    " ".join(
                        [
                            str(semantic_context.get("intent") or ""),
                            str(soft_policy.get("concept") or ""),
                        ]
                    ).lower(),
                )
                weight *= balance_factor
                affinity_factor, affinity_summary = soft_preset_affinity_factor(preset, soft_policy, data)
                weight *= affinity_factor
                role_scene_factor, role_scene_summary = role_scene_policy_factor(preset, soft_policy)
                weight *= role_scene_factor
                batch_penalty, batch_summary = batch_diversity_penalty(semantic_context, "preset", str(preset.get("id")), vector)
                weight *= batch_penalty
                summary = {
                    "id": preset.get("id"),
                    "weight": round(weight, 6),
                    "batch_penalty": batch_summary,
                    "soft_preset_affinity": affinity_summary,
                    "role_scene_policy": role_scene_summary,
                    "selection_balance": {"multiplier": balance_factor, "implicit_themes": balance_themes},
                    **score_summary,
                }
                scored_presets.append((preset, weight, score, summary))
            if scored_presets:
                guard_relaxed = relax_family_policy
                break
            # Family preset policies can reject every preset (e.g. a
            # relationship mixin whose capable presets are adult-gated).
            # Retry with the family policy relaxed but every safety guard
            # intact, instead of falling back to a guard-blind random pick.
        if guard_relaxed:
            semantic_context.setdefault("preset_guard_relaxations", []).append(
                {"reason": "family_preset_policy_relaxed", "rejected": dict(rejected_by_reason)}
            )
        # Concept-affine presets (explicit role/bundle preset ids) outrank a
        # mixin's atmospheric family lock: when the guards rejected every
        # preferred preset, score them with the family policy relaxed (all
        # safety guards intact) so reinjection/enforcement can reach them.
        affine_spec_ids = set(
            normalize_list((soft_policy.get("preset_affinity") or {}).get("preferred_presets"))
        )
        if affine_spec_ids and not (
            affine_spec_ids & {str(row[0].get("id")) for row in scored_presets}
        ):
            for preset in presets:
                if str(preset.get("id")) not in affine_spec_ids:
                    continue
                allowed, _reason = compatible_preset_with_semantic_hard_guards(
                    preset, semantic_context, relax_family_policy=True
                )
                if not allowed:
                    continue
                vector = semantic_vector(semantic_context, semantic_entry_key("preset", preset))
                score, score_summary = semantic_preset_score_breakdown(vector, semantic_context, preset)
                weight = semantic_preset_candidate_weight(preset, score, semantic_context)
                affinity_factor, affinity_summary = soft_preset_affinity_factor(preset, soft_policy, data)
                weight *= affinity_factor
                role_scene_factor, role_scene_summary = role_scene_policy_factor(preset, soft_policy)
                weight *= role_scene_factor
                batch_penalty, batch_summary = batch_diversity_penalty(semantic_context, "preset", str(preset.get("id")), vector)
                weight *= batch_penalty
                scored_presets.append(
                    (
                        preset,
                        weight,
                        score,
                        {
                            "id": preset.get("id"),
                            "weight": round(weight, 6),
                            "batch_penalty": batch_summary,
                            "soft_preset_affinity": affinity_summary,
                            "role_scene_policy": role_scene_summary,
                            "affine_guard_relaxed": True,
                            **score_summary,
                        },
                    )
                )
                guard_relaxed = True
        summaries = [row[3] for row in scored_presets]
        rejected_count = sum(rejected_by_reason.values())
        if rejected_count:
            semantic_context["hard_rejected_count"] = int(semantic_context.get("hard_rejected_count", 0)) + rejected_count
            semantic_context.setdefault("hard_rejected", []).append(
                {"scope": "preset", "count": rejected_count, "reasons": rejected_by_reason}
            )
        best_score = max((score for _, _, score, _ in scored_presets), default=0.0)
        score_window = semantic_preset_score_window(semantic_context)
        window_candidates = [
            (preset, weight, score, summary)
            for preset, weight, score, summary in scored_presets
            if score >= best_score - score_window
        ]
        limit = semantic_preset_candidate_limit(semantic_context)
        ordered = sorted(window_candidates, key=lambda row: row[2], reverse=True)[:limit]
        if ordered:
            best_weight = max((row[1] for row in ordered), default=0.01)
            floor = best_weight * semantic_preset_weight_floor(semantic_context)
            candidates = [row for row in ordered if row[1] >= floor][:limit]
            minimum = min(3, len(ordered), limit)
            if len(candidates) < minimum:
                candidates = ordered[:minimum]
        else:
            candidates = []
        # Preferred-preset reinjection + mass floor: concept-affine presets
        # (role/bundle presets) must stay reachable even when the semantic
        # score window prunes them, mirroring the soft-anchor slot treatment.
        # Pool semantics need exact ids: axis-text affinity ("portrait" etc.)
        # is a soft bias and must not widen the enforced affine pool.
        preferred_ids = set(
            normalize_list((soft_policy.get("preset_affinity") or {}).get("preferred_presets"))
        )
        scored_ids = {str(row[0].get("id")) for row in scored_presets}
        preferred_ids &= scored_ids
        if preferred_ids:
            candidate_ids = {str(preset.get("id")) for preset, *_ in candidates}
            missing = [
                row
                for row in sorted(scored_presets, key=lambda r: r[2], reverse=True)
                if str(row[0].get("id")) in preferred_ids and str(row[0].get("id")) not in candidate_ids
            ]
            # Reinjection limit applies to exact preferred presets only.
            reinjection_limit = int(
                semantic_policy_float(semantic_context, ("preset_affinity", "candidate_reinjection_limit"), 2)
            )
            if missing and reinjection_limit > 0:
                candidates = list(candidates) + missing[:reinjection_limit]
        candidate_presets = [preset for preset, *_ in candidates]
        candidate_weights = [weight for _, weight, *_ in candidates]
        if preferred_ids and candidate_presets:
            preferred_floor = semantic_policy_float(
                semantic_context, ("preset_affinity", "preferred_probability_floor"), 0.5
            )
            indexes = [
                index
                for index, preset in enumerate(candidate_presets)
                if str(preset.get("id")) in preferred_ids
            ]
            total = sum(max(weight, 0.0) for weight in candidate_weights)
            preferred_mass = sum(max(candidate_weights[index], 0.0) for index in indexes)
            other_mass = max(total - preferred_mass, 0.0)
            if indexes and other_mass > 0 and preferred_mass > 0 and 0.0 < preferred_floor < 1.0:
                share = preferred_mass / total
                if share < preferred_floor:
                    scale = (preferred_floor * other_mass) / ((1.0 - preferred_floor) * preferred_mass)
                    for index in indexes:
                        candidate_weights[index] = candidate_weights[index] * scale
        if candidate_presets and sum(candidate_weights) > 0:
            selected = rng.choices(candidate_presets, weights=candidate_weights, k=1)[0]
        else:
            selected = weighted_choice(presets, rng)
        # Preset-pool enforcement: like anchor slots, concept-affine presets
        # (preferred ids plus presets sharing their families) form the related
        # pool; randomness lives inside that pool, not outside it.
        if (
            preferred_ids
            and candidate_presets
            and semantic_policy_float(semantic_context, ("preset_affinity", "enforcement"), 1.0) >= 1.0
        ):
            preferred_families = {
                str(preset.get("family"))
                for preset in presets
                if str(preset.get("id")) in preferred_ids and preset.get("family")
            }
            def in_affine_pool(preset_entry: JsonDict) -> bool:
                return (
                    str(preset_entry.get("id")) in preferred_ids
                    or (preset_entry.get("family") and str(preset_entry.get("family")) in preferred_families)
                )
            if not in_affine_pool(selected):
                affine_rows = [
                    (preset_entry, max(weight, 0.000001))
                    for preset_entry, weight in zip(candidate_presets, candidate_weights)
                    if in_affine_pool(preset_entry)
                ]
                if affine_rows:
                    selected = rng.choices(
                        [row[0] for row in affine_rows],
                        weights=[row[1] for row in affine_rows],
                        k=1,
                    )[0]
        summary_by_id = {str(summary.get("id")): summary for summary in summaries}
        selected_batch_penalty = summary_by_id.get(str(selected.get("id")), {}).get("batch_penalty")
        if selected_batch_penalty:
            semantic_context.setdefault("batch_repetition_penalty", []).append(selected_batch_penalty)
        semantic_context["preset_score"] = {
            "selected": selected.get("id"),
            "guard_relaxed": guard_relaxed,
            "selected_summary": summary_by_id.get(str(selected.get("id")), {}),
            "intent_axes": semantic_context.get("intent_axes", {}),
            "top": [
                summary
                for _, _, _, summary in sorted(candidates, key=lambda row: row[2], reverse=True)[:5]
            ],
            "candidate_count": len(candidates),
            "window_candidate_count": len(window_candidates),
            "score_window": score_window,
            "preset_candidate_limit": semantic_preset_candidate_limit(semantic_context),
            "preset_weight_floor": semantic_preset_weight_floor(semantic_context),
            "hard_rejected_count": rejected_count,
            "hard_rejected_by_reason": rejected_by_reason,
        }
        return selected

    balanced_presets = apply_selection_balance_bias(presets, data, None, None)
    return weighted_choice(balanced_presets, rng)


def record_batch_generation(
    semantic_context: Optional[JsonDict],
    preset: JsonDict,
    picked: Dict[str, Entry],
    forced_choices: Optional[Dict[str, List[str]]] = None,
    preset_forced: bool = False,
) -> None:
    if not semantic_context:
        return
    batch_context = semantic_context.get("batch_context")
    if not batch_context or not batch_context.get("enabled"):
        return
    preset_id = str(preset.get("id"))
    record_batch_selection(
        batch_context,
        "preset",
        preset_id,
        semantic_vector(semantic_context, semantic_entry_key("preset", preset)),
        forced=preset_forced,
    )
    forced_slots = set((forced_choices or {}).keys())
    for slot in BATCH_DIVERSITY_TRACKED_SCOPES:
        if slot in {"subject_group", "location_tone"}:
            continue
        if slot == "preset" or slot in forced_slots:
            continue
        entry = picked.get(slot)
        if not entry:
            continue
        vector = semantic_vector(semantic_context, semantic_entry_key("slot", entry, slot))
        record_batch_selection(
            batch_context,
            slot,
            str(entry.get("id")),
            vector,
        )
        record_batch_group_selection(semantic_context, batch_context, slot, entry, vector, forced=False)


# -----------------------------------------------------------------------------
# Priority-biased slot selection
# -----------------------------------------------------------------------------

def get_generation_settings(data: JsonDict) -> JsonDict:
    return data.get("generation_settings", {}) or {}


def get_slot_priorities(data: JsonDict) -> Dict[str, float]:
    raw = data.get("slot_priorities", data.get("slot_priority", {})) or {}
    priorities: Dict[str, float] = {}
    for k, v in raw.items():
        try:
            priorities[str(k)] = float(v)
        except (TypeError, ValueError):
            priorities[str(k)] = 0.0
    return priorities


def boosted_probability(base: float, slot: str, data: JsonDict, priority_bias: Optional[float]) -> float:
    """
    Boost optional-slot probability according to global slot priority.

    base=0.45, priority=max, priority_bias=0.5 -> 0.725
    base=0.45, priority=half, priority_bias=0.5 -> 0.5875
    """
    base = max(0.0, min(1.0, float(base)))
    priorities = get_slot_priorities(data)
    if not priorities:
        return base

    if priority_bias is None:
        settings = get_generation_settings(data)
        priority_bias = float(settings.get("priority_bias", 0.0))

    bias = max(0.0, float(priority_bias))
    if bias <= 0:
        return base

    max_priority = max(max(priorities.values()), 1.0)
    slot_priority = max(priorities.get(slot, 0.0), 0.0)
    ratio = min(slot_priority / max_priority, 1.0)
    return max(0.0, min(1.0, base + (1.0 - base) * ratio * bias))


def optional_slot_specs(preset: JsonDict, data: JsonDict) -> List[JsonDict]:
    settings = get_generation_settings(data)
    default_p = float(settings.get("default_optional_probability", 0.5))

    specs: List[JsonDict] = []

    def normalize(opt: Any, source: str) -> Optional[JsonDict]:
        if isinstance(opt, str):
            return {"slot": opt, "probability": default_p, "source": source}
        if isinstance(opt, dict) and opt.get("slot"):
            spec = dict(opt)
            spec.setdefault("probability", spec.get("prob", default_p))
            spec["source"] = source
            return spec
        return None

    for opt in preset.get("optional_slots", []):
        spec = normalize(opt, "preset")
        if spec:
            specs.append(spec)

    if not preset.get("disable_auto_optional", False):
        disabled = set(preset.get("skip_auto_slots", []))
        already = set(preset.get("required_slots", [])) | {s["slot"] for s in specs}
        filters = preset.get("filters", {}) or {}
        authored_filters_only = preset.get("auto_optional_policy") == "authored_filters_only"
        for opt in settings.get("auto_optional_slots", []):
            spec = normalize(opt, "auto")
            if not spec:
                continue
            slot = spec["slot"]
            if slot in disabled or slot in already:
                continue
            if (authored_filters_only or spec.get("requires_filter")) and slot not in filters:
                continue
            specs.append(spec)
            already.add(slot)

    return specs


def preset_uses_adult_context(preset: JsonDict) -> bool:
    if "adult" in entry_tags(preset):
        return True
    if str(preset.get("id", "")).startswith("adult_"):
        return True
    required = set(preset.get("required_slots", []))
    return bool(required & {"adult_context", "fetish_styling", "body_framing", "caption_context"})


def has_forced_surreal_slot(forced_choices: Optional[Dict[str, List[str]]]) -> bool:
    return bool(set((forced_choices or {}).keys()) & set(SURREAL_LAYER_SLOTS))


def should_activate_surreal_layer(
    preset: JsonDict,
    rng: random.Random,
    mode: str,
    probability: float,
    forced_choices: Optional[Dict[str, List[str]]] = None,
    semantic_context: Optional[JsonDict] = None,
    mode_explicit: bool = False,
) -> bool:
    active = False
    reason = "off"
    if has_forced_surreal_slot(forced_choices):
        active = True
        reason = "forced_slot"
    elif mode == "on":
        active = True
        reason = "explicit"
    elif preset_uses_adult_context(preset):
        active = False
        reason = "adult_preset_blocked"
    elif (
        semantic_context
        and intent_steering_enabled(semantic_context)
        and not mode_explicit
        and mode == "off"
        and "fantasy" in context_axis_families(semantic_context)
    ):
        active = True
        reason = "semantic_axis"
    elif mode == "auto":
        active = rng.random() < max(0.0, min(1.0, probability))
        reason = "probability"
    elif mode == "off" and mode_explicit:
        active = False
        reason = "explicit_off"

    if semantic_context is not None:
        semantic_context["surreal_activation_reason"] = reason
        semantic_context["surreal_activation_active"] = active
    return active


def apply_surreal_layer(
    data: JsonDict,
    preset: JsonDict,
    rng: random.Random,
    picked: Dict[str, Entry],
    forced_choices: Optional[Dict[str, List[str]]] = None,
    intensity: str = "moderate",
    semantic_context: Optional[JsonDict] = None,
    generation_contract: Optional[JsonDict] = None,
) -> None:
    for slot in SURREAL_INTENSITY_SLOTS[intensity]:
        if slot in picked:
            continue
        entry = choose_slot(slot, data, preset, rng, picked, forced_choices, semantic_context, generation_contract)
        if entry is not None:
            picked[slot] = entry
            refresh_generation_contract(generation_contract, data, preset, picked, forced_choices, surreal_enabled=True)
            sync_generation_contract_axis_coverage(generation_contract, semantic_context)


def apply_coverage_repair(
    data: JsonDict,
    preset: JsonDict,
    rng: random.Random,
    picked: Dict[str, Entry],
    family: str,
    forced_choices: Optional[Dict[str, List[str]]] = None,
    semantic_context: Optional[JsonDict] = None,
    generation_contract: Optional[JsonDict] = None,
) -> None:
    if not semantic_context:
        return
    repair = coverage_repair_config(semantic_context, family)
    candidate_slots = coverage_repair_slots(semantic_context, family)
    trace_key = "weak_horror_compensation" if family == "horror" else f"{family}_coverage_repair"
    trace: JsonDict = {
        "status": "not_needed",
        "reason": "strong_horror_present_or_not_applicable" if family == "horror" else "coverage_satisfied_or_not_applicable",
        "reason_code": f"{family}_coverage_repair_not_needed",
        "family": family,
        "policy_id": str(repair.get("policy_id") or semantic_policy_id(semantic_context, family)),
        "policy_schema_version": semantic_policy_schema_version(semantic_context),
        "semantic_policy_hash": semantic_context.get("semantic_policy_hash"),
        "matched_via": f"semantic_policy.families.{family}.coverage_repair",
        "matched_terms": [],
        "candidate_slots": list(candidate_slots),
        "repair_attempts": [],
    }
    if family != "horror" or not weak_horror_compensation_needed(semantic_context, picked):
        semantic_context[trace_key] = trace
        return
    forced_slots = set((forced_choices or {}).keys())
    for slot in candidate_slots:
        if slot in picked or slot in forced_slots or slot not in data.get("slots", {}):
            continue
        entry = choose_slot(slot, data, preset, rng, picked, forced_choices, semantic_context, generation_contract)
        if entry is None:
            trace["repair_attempts"].append({"slot": slot, "selected": None, "status": "empty"})
            continue
        picked[slot] = entry
        refresh_generation_contract(generation_contract, data, preset, picked, forced_choices)
        sync_generation_contract_axis_coverage(generation_contract, semantic_context)
        strength = family_signal_strength(entry, "horror", coherence_rules_from_source(semantic_context), slot, semantic_context)
        semantic_context[trace_key] = {
            "status": "applied" if strength == "strong" else "attempted",
            "reason_code": f"{family}_coverage_repair_selected",
            "family": family,
            "policy_id": trace["policy_id"],
            "policy_schema_version": trace["policy_schema_version"],
            "semantic_policy_hash": trace["semantic_policy_hash"],
            "matched_via": trace["matched_via"],
            "matched_terms": [],
            "slot": slot,
            "selected": entry.get("id"),
            "strength": strength,
            "repair_attempts": trace["repair_attempts"] + [
                {"slot": slot, "selected": entry.get("id"), "strength": strength}
            ],
        }
        return
    semantic_context[trace_key] = {
        "status": "blocked_by_forced_set" if forced_slots & set(candidate_slots) else "blocked",
        "reason": "no_available_compensation_slot",
        "reason_code": f"{family}_coverage_repair_blocked",
        "family": family,
        "policy_id": trace["policy_id"],
        "policy_schema_version": trace["policy_schema_version"],
        "semantic_policy_hash": trace["semantic_policy_hash"],
        "matched_via": trace["matched_via"],
        "matched_terms": [],
        "forced_slots": sorted(forced_slots & set(candidate_slots)),
        "repair_attempts": trace["repair_attempts"],
    }


def apply_weak_horror_compensation(
    data: JsonDict,
    preset: JsonDict,
    rng: random.Random,
    picked: Dict[str, Entry],
    forced_choices: Optional[Dict[str, List[str]]] = None,
    semantic_context: Optional[JsonDict] = None,
    generation_contract: Optional[JsonDict] = None,
) -> None:
    apply_coverage_repair(
        data,
        preset,
        rng,
        picked,
        "horror",
        forced_choices,
        semantic_context,
        generation_contract,
    )


def route_slots_for_axis_gap(gap: JsonDict, semantic_context: Optional[JsonDict] = None) -> List[str]:
    ordered: List[str] = []
    source = semantic_context or (gap.get("semantic_context") if isinstance(gap.get("semantic_context"), dict) else None)
    for family in gap.get("families", []):
        for slot in semantic_axis_route_slots(source, str(family)):
            if slot not in ordered:
                ordered.append(slot)
    return ordered


def apply_axis_coverage_compensation(
    data: JsonDict,
    preset: JsonDict,
    rng: random.Random,
    picked: Dict[str, Entry],
    forced_choices: Optional[Dict[str, List[str]]] = None,
    semantic_context: Optional[JsonDict] = None,
    generation_contract: Optional[JsonDict] = None,
) -> None:
    if not semantic_context or generation_contract is None:
        return
    sync_generation_contract_axis_coverage(generation_contract, semantic_context)
    gaps = list(generation_contract.get("coverage_gaps", []))
    if not gaps:
        return
    forced_slots = set((forced_choices or {}).keys())
    max_attempts = 4
    attempts = 0
    for gap in gaps:
        if attempts >= max_attempts:
            break
        slots = route_slots_for_axis_gap(gap, semantic_context)
        if not slots:
            record_generation_contract_event(
                generation_contract,
                "reselect_events",
                {"axis": gap.get("text"), "status": "skipped", "reason": "no_routed_slots"},
            )
            continue
        selected = None
        for slot in slots:
            if slot in picked or slot in forced_slots or slot not in data.get("slots", {}):
                continue
            semantic_context["active_must_cover_axis"] = gap
            try:
                entry = choose_slot(slot, data, preset, rng, picked, forced_choices, semantic_context, generation_contract)
            finally:
                semantic_context.pop("active_must_cover_axis", None)
            attempts += 1
            if entry is None:
                continue
            picked[slot] = entry
            refresh_generation_contract(generation_contract, data, preset, picked, forced_choices)
            sync_generation_contract_axis_coverage(generation_contract, semantic_context)
            selected = {"slot": slot, "id": entry.get("id")}
            break
        record_generation_contract_event(
            generation_contract,
            "reselect_events",
            {
                "axis": gap.get("text"),
                "families": gap.get("families", []),
                "status": "applied" if selected else "blocked",
                "selected": selected,
            },
        )


def selected_semantic_metadata_summary(picked: Dict[str, Entry], context: Optional[JsonDict]) -> JsonDict:
    if not context:
        return {}
    return {
        "subject_groups": entry_semantic_groups(picked["subject"], "subject", context) if "subject" in picked else [],
        "location_tones": entry_location_tones(picked["location"], "location", context) if "location" in picked else [],
        "axis_signals": {
            slot: entry_axis_signals(entry, slot, context)
            for slot, entry in picked.items()
            if entry_axis_signals(entry, slot, context)
        },
    }


def rendered_prompt_blob(result: JsonDict) -> str:
    parts = [
        str(value)
        for key, value in result.items()
        if key.startswith("prompt_") and value
    ]
    return "\n".join(parts).lower()


def rendered_prompt_body_blob(result: JsonDict) -> str:
    blob = "\n".join(str(value) for key, value in result.items() if key.startswith("prompt_") and value)
    markers = [
        "Subject and state:",
        "Scene and location:",
        "Scene and environment:",
        "Camera and composition:",
        "Lighting:",
        "Light and atmosphere:",
        "Texture, format, and finish:",
        "Materials and finish:",
    ]
    offsets = [blob.find(marker) for marker in markers if blob.find(marker) >= 0]
    if offsets:
        blob = blob[min(offsets) :]
    return blob.lower()


def soft_anchor_body_term_rate(policy: JsonDict, picked: Dict[str, Entry], result: JsonDict) -> tuple[float, List[str], List[str]]:
    selected_slots = selected_soft_anchor_slots(policy, picked)
    term_groups: List[tuple[str, List[str]]] = []
    for anchor in policy.get("anchors", []):
        if anchor.get("critical") or anchor.get("slot") in selected_slots:
            terms = sorted({str(term).lower() for term in normalize_list(anchor.get("terms")) if str(term).strip()})
            if terms:
                term_groups.append((str(anchor.get("slot") or ""), terms))
    if not term_groups:
        return (1.0 if selected_slots else 0.0), [], []
    body = rendered_prompt_body_blob(result)
    hits: List[str] = []
    missing: List[str] = []
    matched_groups = 0
    for slot, terms in term_groups:
        matched_terms = [term for term in terms if term in body]
        if matched_terms:
            matched_groups += 1
            hits.extend(matched_terms)
        else:
            missing.append(f"{slot}:{'|'.join(terms)}")
    return matched_groups / max(len(term_groups), 1), sorted(set(hits)), sorted(set(missing))


def evaluate_generation_quality(
    generation_contract: Optional[JsonDict],
    render_picked: Dict[str, Entry],
    result: JsonDict,
    semantic_context: Optional[JsonDict],
) -> JsonDict:
    contract = generation_contract or {}
    checks: List[JsonDict] = []
    fail_reasons: List[str] = []
    warn_reasons: List[str] = []

    forced_slots = set(contract.get("forced_slots", []) or [])
    rendered_slots = set(render_picked)
    missing_forced = sorted(forced_slots - rendered_slots)
    suppressed_forced = [
        event
        for event in contract.get("render_suppressed_slots", []) or []
        if event.get("slot") in forced_slots
    ]
    forced_status = "fail" if missing_forced or suppressed_forced else "pass"
    if forced_status == "fail":
        fail_reasons.append("forced_slot_not_rendered")
    checks.append(
        {
            "id": "forced_slot_preserved",
            "status": forced_status,
            "missing_slots": missing_forced,
            "suppressed": suppressed_forced,
        }
    )

    prompt_blob = rendered_prompt_blob(result)
    missing_locks = [
        lock
        for lock in normalize_concept_locks(contract.get("concept_locks", []))
        if lock.lower() not in prompt_blob
    ]
    concept_status = "fail" if missing_locks else "pass"
    if concept_status == "fail":
        if (contract.get("soft_anchor_policy") or {}).get("enabled"):
            warn_reasons.append("concept_lock_not_rendered")
            concept_status = "warn"
        else:
            fail_reasons.append("concept_lock_not_rendered")
    checks.append(
        {
            "id": "concept_lock_rendered",
            "status": concept_status,
            "missing": missing_locks,
        }
    )

    must_cover = contract.get("must_cover_axes", []) or []
    covered = contract.get("covered_axes", []) or []
    coverage_rate = len(covered) / max(len(must_cover), 1) if must_cover else 1.0
    coverage_status = "pass"
    if contract.get("coverage_gaps"):
        coverage_status = "warn"
        warn_reasons.append("axis_coverage_gap")
    checks.append(
        {
            "id": "axis_coverage",
            "status": coverage_status,
            "coverage_rate": round(coverage_rate, 4),
            "must_cover_count": len(must_cover),
            "covered_count": len(covered),
            "gaps": contract.get("coverage_gaps", []),
        }
    )

    soft_policy = contract.get("soft_anchor_policy", {}) or {}
    if soft_policy.get("enabled"):
        match_status = soft_anchor_match_status(soft_policy, render_picked)
        selected_slots = set(match_status.get("selected_anchor_slots", []))
        min_anchors = int(soft_policy.get("min_anchors", 0))
        required_anchor_count = int(match_status.get("required_anchor_count", soft_anchor_required_count(soft_policy)))
        anchor_slot_count = int(match_status.get("anchor_slot_count", len(soft_anchor_slots(soft_policy))))
        missing_anchor_slots = [
            slot
            for slot in soft_anchor_slots(soft_policy)
            if slot not in selected_slots
        ]
        soft_anchor_status = "pass" if match_status.get("passed") else "fail"
        if soft_anchor_status == "fail":
            fail_reasons.extend(match_status.get("failure_reasons", []) or ["soft_anchor_minimum_not_selected"])
        checks.append(
            {
                "id": "soft_anchor_selected",
                "status": soft_anchor_status,
                "selected_anchor_count": match_status.get("selected_anchor_count", len(selected_slots)),
                "min_anchors": min_anchors,
                "required_anchor_count": required_anchor_count,
                "selected_anchor_rate": match_status.get("selected_anchor_rate", round(len(selected_slots) / max(1, anchor_slot_count), 4)),
                "minimum_selected_anchor_rate": soft_anchor_selected_rate_floor(soft_policy),
                "selected_anchor_slots": sorted(selected_slots),
                "missing_anchor_slots": missing_anchor_slots,
                "critical_missing": match_status.get("critical_missing", []),
                "source_floor_misses": match_status.get("source_floor_misses", []),
                "anchor_group_misses": match_status.get("group_floor_misses", []),
                "salience_matches": match_status.get("salience_matches", 0),
                "salience_floor": match_status.get("salience_floor", 0),
                "failure_reasons": match_status.get("failure_reasons", []),
                "repair": contract.get("soft_anchor_repair", {}),
            }
        )

        guard_status = soft_visual_guard_status(soft_policy, render_picked)
        if not guard_status.get("passed"):
            fail_reasons.append("soft_visual_guard_violation")
        checks.append(
            {
                "id": "soft_visual_guard",
                "status": "pass" if guard_status.get("passed") else "fail",
                "violations": guard_status.get("violations", []),
            }
        )

        body_rate, body_hits, body_missing = soft_anchor_body_term_rate(soft_policy, render_picked, result)
        body_status = "pass" if body_rate >= SOFT_ANCHOR_BODY_TERM_THRESHOLD else "fail"
        if body_status == "fail":
            fail_reasons.append("soft_anchor_terms_not_rendered")
        checks.append(
            {
                "id": "soft_anchor_body_terms",
                "status": body_status,
                "body_anchor_term_rate": round(body_rate, 4),
                "minimum_body_anchor_term_rate": SOFT_ANCHOR_BODY_TERM_THRESHOLD,
                "hits": body_hits,
                "missing": body_missing,
            }
        )

        priority_status = render_priority_term_status(soft_policy, result)
        if not priority_status.get("passed"):
            fail_reasons.append("render_priority_term_missing")
        checks.append(
            {
                "id": "soft_render_priority_terms",
                "status": "pass" if priority_status.get("passed") else "fail",
                "groups": priority_status.get("groups", []),
                "missing": priority_status.get("missing", []),
            }
        )

        preset_conflicts = contract.get("policy_conflicts", []) or []
        if preset_conflicts:
            warn_reasons.append("preset_concept_conflict")
        checks.append(
            {
                "id": "soft_preset_affinity",
                "status": "warn" if preset_conflicts else "pass",
                "policy_conflicts": preset_conflicts,
            }
        )

        dual_status = dual_read_term_status(soft_policy, result)
        if not dual_status.get("passed"):
            warn_reasons.append("dual_read_terms_weak")
        checks.append(
            {
                "id": "soft_dual_read_terms",
                "status": "pass" if dual_status.get("passed") else "warn",
                **dual_status,
            }
        )

        free_constraint_violations = soft_free_slot_constraint_violations(soft_policy, render_picked)
        if free_constraint_violations:
            fail_reasons.append("soft_free_slot_constraint_violation")
        checks.append(
            {
                "id": "soft_free_slot_constraints",
                "status": "pass" if not free_constraint_violations else "fail",
                "violations": free_constraint_violations,
            }
        )

        guard_policy = (semantic_policy_from_source(semantic_context).get("soft_body_first_guard", {}) or {})
        guard_slots = normalize_list(guard_policy.get("slots"))
        legacy_guard_slot = str(guard_policy.get("slot") or "").strip()
        if legacy_guard_slot and legacy_guard_slot not in guard_slots:
            guard_slots.append(legacy_guard_slot)
        if not guard_slots:
            guard_slots = ["body_framing"]
        body_emphasis_survivors = soft_body_first_survivors(soft_policy, render_picked, semantic_context)
        body_first = bool(body_emphasis_survivors)
        if body_first:
            fail_reasons.append("body_first_framing_present")
        checks.append(
            {
                "id": "soft_body_first_guard",
                "status": "fail" if body_first else "pass",
                "guard_slots": guard_slots,
                "body_emphasis_survived": body_emphasis_survivors,
                "body_first_guard_applied": bool(contract.get("soft_body_first_guard_events")),
                "events": contract.get("soft_body_first_guard_events", []),
            }
        )

        repair_state = contract.get("soft_anchor_repair", {}) or {}
        checks.append(
            {
                "id": "soft_anchor_repair",
                "status": "pass" if repair_state.get("post_render_status") in {None, "", "not_needed", "repaired"} and repair_state.get("status") != "failed" else "fail",
                "repair": repair_state,
            }
        )

        directive_events = contract.get("soft_render_directive_events", []) or []
        checks.append(
            {
                "id": "soft_render_directives",
                "status": "pass",
                "events": directive_events,
                "render_directive_count": len(directive_events),
            }
        )

    hard_blocked = [
        event
        for event in contract.get("fallback_blocked_slots", []) or []
        if str(event.get("reason", "")).endswith("_empty") or event.get("reason") in {"entry_contract_empty", "semantic_hard_guard_empty"}
    ]
    hard_status = "fail" if any(event.get("slot") in forced_slots for event in hard_blocked) else "pass"
    if hard_status == "fail":
        fail_reasons.append("forced_slot_blocked_by_empty_pool")
    checks.append(
        {
            "id": "hard_guard_empty_slot",
            "status": hard_status,
            "events": hard_blocked,
        }
    )

    verdict = "fail" if fail_reasons else ("warn" if warn_reasons else "pass")
    return {
        "verdict": verdict,
        "selection_mode": (semantic_context or {}).get("selection_mode", "rule"),
        "semantic_relevance": "scored" if semantic_context else "not_evaluated",
        "checks": checks,
        "reasons": fail_reasons + warn_reasons,
        "policy_schema_version": (semantic_context or {}).get("policy_schema_version"),
        "semantic_policy_hash": (semantic_context or {}).get("semantic_policy_hash"),
    }


def has_surreal_layer(picked: Dict[str, Entry]) -> bool:
    return any(slot in picked for slot in SURREAL_LAYER_SLOTS)


def selected_slots_for_preset(
    preset: JsonDict,
    data: JsonDict,
    rng: random.Random,
    forced_choices: Optional[Dict[str, List[str]]] = None,
    priority_bias: Optional[float] = None,
) -> List[str]:
    required = list(preset.get("required_slots", []))
    slots = required[:]

    for spec in optional_slot_specs(preset, data):
        slot = spec.get("slot")
        if not slot:
            continue
        base_probability = float(spec.get("probability", spec.get("prob", 0.5)))
        if spec.get("priority_boost", True):
            probability = boosted_probability(base_probability, slot, data, priority_bias)
        else:
            probability = max(0.0, min(1.0, base_probability))
        if rng.random() < probability:
            slots.append(slot)

    # Forced slots must be present even if the preset did not select them.
    for slot in (forced_choices or {}):
        if slot not in slots:
            slots.append(slot)

    # Make sure dependencies are available before compatible slots are picked.
    order = data.get("slot_pick_order", [])
    order_index = {slot: i for i, slot in enumerate(order)}
    fallback_order = {
        "medium": 0,
        "genre": 1,
        "subject": 2,
        "person_origin": 3,
        "appearance_type": 4,
        "action": 5,
        "location": 6,
    }

    def priority(s: str) -> int:
        if s in order_index:
            return order_index[s]
        return fallback_order.get(s, 100)

    deduped = []
    seen = set()
    for s in sorted(slots, key=priority):
        if s not in seen:
            deduped.append(s)
            seen.add(s)
    return deduped


# -----------------------------------------------------------------------------
# Compatibility and forced choices
# -----------------------------------------------------------------------------

def parse_forced_choices(items: Optional[Sequence[str]]) -> Dict[str, List[str]]:
    forced: Dict[str, List[str]] = {}
    for raw in items or []:
        if "=" not in raw:
            raise ValueError(f"Invalid --set value '{raw}'. Use --set slot=id or --set slot=id1,id2")
        slot, ids_raw = raw.split("=", 1)
        slot = slot.strip()
        ids = [x.strip() for x in re.split(r"[,|]", ids_raw) if x.strip()]
        if not slot or not ids:
            raise ValueError(f"Invalid --set value '{raw}'. Use --set slot=id or --set slot=id1,id2")
        forced[slot] = ids
    return forced


def load_forced_choices_from_json(raw: Optional[str]) -> Dict[str, List[str]]:
    if not raw:
        return {}

    candidate = Path(raw)
    if candidate.exists():
        payload = json.loads(candidate.read_text(encoding="utf-8"))
    else:
        payload = json.loads(raw)

    if not isinstance(payload, dict):
        raise ValueError("--set-json must be a JSON object, e.g. '{\"subject\":\"fashion_model\"}'")

    forced: Dict[str, List[str]] = {}
    for slot, value in payload.items():
        if isinstance(value, str):
            forced[str(slot)] = [value]
        elif isinstance(value, list):
            forced[str(slot)] = [str(x) for x in value]
        else:
            raise ValueError(f"Invalid --set-json value for slot '{slot}': expected string or list")
    return forced


def merge_forced_choices(*choices: Dict[str, List[str]]) -> Dict[str, List[str]]:
    merged: Dict[str, List[str]] = {}
    for choice in choices:
        for slot, ids in choice.items():
            merged[slot] = list(ids)
    return merged


def normalize_reference_identity_axes(raw: Any) -> List[JsonDict]:
    if isinstance(raw, dict):
        raw = raw.get("required") or raw.get("axes") or []
    if not isinstance(raw, list):
        raw = normalize_list(raw)
    axes: List[JsonDict] = []
    seen: Set[str] = set()
    for item in raw:
        if isinstance(item, dict):
            axis_id = str(item.get("id") or item.get("axis") or "").strip()
            if not axis_id:
                continue
            axis = {
                "id": axis_id,
                "terms": normalize_list(item.get("terms")),
                "description": str(item.get("description") or "").strip(),
            }
        else:
            axis_id = str(item or "").strip()
            if not axis_id:
                continue
            axis = {"id": axis_id, "terms": [], "description": ""}
        if axis_id in seen:
            continue
        seen.add(axis_id)
        axes.append(axis)
    return axes


def normalize_reference_motif_pools(raw: Any) -> JsonDict:
    if not isinstance(raw, dict):
        return {}
    pools: JsonDict = {}
    for motif, pool in raw.items():
        motif_id = str(motif or "").strip()
        if not motif_id or not isinstance(pool, dict):
            continue
        normalized: JsonDict = {
            "axis": str(pool.get("axis") or "").strip(),
            "bucket": str(pool.get("bucket") or "").strip(),
            "terms": normalize_list(pool.get("terms")),
        }
        slot_candidates = pool.get("slot_candidates")
        if isinstance(slot_candidates, dict):
            normalized["slot_candidates"] = {
                str(slot): normalize_list(ids)
                for slot, ids in slot_candidates.items()
                if normalize_list(ids)
            }
        exemplars = normalize_list(pool.get("exemplars"))
        if exemplars:
            normalized["exemplars"] = exemplars
        pools[motif_id] = {key: value for key, value in normalized.items() if value}
    return pools


def normalize_reference_motif_quotas(raw: Any) -> JsonDict:
    if not isinstance(raw, dict):
        return {}
    quotas: JsonDict = {}
    for motif, quota in raw.items():
        motif_id = str(motif or "").strip()
        if not motif_id:
            continue
        if isinstance(quota, dict):
            normalized: JsonDict = {}
            for key in ("max_batch_share", "max_recent_share"):
                if key in quota:
                    try:
                        value = float(quota.get(key))
                    except (TypeError, ValueError):
                        continue
                    normalized[key] = max(0.0, min(1.0, value))
            for key in ("max_batch_uses", "max_recent_uses"):
                if key in quota:
                    try:
                        value = int(quota.get(key))
                    except (TypeError, ValueError):
                        continue
                    if value >= 0:
                        normalized[key] = value
            if quota.get("avoid_when_pressure"):
                normalized["avoid_when_pressure"] = True
            if normalized:
                quotas[motif_id] = normalized
        else:
            try:
                share = float(quota)
            except (TypeError, ValueError):
                continue
            quotas[motif_id] = {"max_batch_share": max(0.0, min(1.0, share))}
    return quotas


def normalize_reference_semantic_dropout(raw: Any) -> JsonDict:
    if not isinstance(raw, dict):
        return {"enabled": False}
    normalized: JsonDict = {"enabled": bool(raw.get("enabled", True))}
    buckets = normalize_list(raw.get("maskable_buckets"))
    if buckets:
        normalized["maskable_buckets"] = [
            bucket for bucket in buckets if bucket in CANDIDATE_PACK_SEMANTIC_DROPOUT_BUCKETS
        ]
    for key, default in (("min_buckets", 0), ("max_buckets", 0)):
        if key in raw:
            try:
                normalized[key] = max(0, int(raw.get(key)))
            except (TypeError, ValueError):
                normalized[key] = default
    if "probability" in raw:
        try:
            normalized["probability"] = max(0.0, min(1.0, float(raw.get("probability"))))
        except (TypeError, ValueError):
            normalized["probability"] = 0.0
    return normalized


def normalize_reference_exemplar_set(raw: Any) -> JsonDict:
    if isinstance(raw, dict):
        normalized: JsonDict = {}
        for key, value in raw.items():
            values = normalize_list(value)
            if values:
                normalized[str(key)] = values
        return normalized
    values = normalize_list(raw)
    return {"examples": values} if values else {}


def normalize_soft_anchor_spec(payload: Any) -> JsonDict:
    if not payload:
        return {
            "enabled": False,
            "mode": "soft",
            "min_anchors": 0,
            "anchors": [],
            "source_floors": {},
            "group_floors": {},
            "salience_floor": 0,
            "visual_guards": [],
            "render_priority_terms": [],
            "free_slot_constraints": {},
            "render_suppress_terms": [],
            "render_directives": [],
            "dual_read_requirement": {},
            "preset_affinity": {},
            "role_scene_policy": {"enabled": False},
            "species_family_policy": {"enabled": False, "allowed": {}},
            "diversity_state": {},
            "soft_repair_policy": normalize_soft_repair_policy({}),
            "safety_negative_floor": [],
            "identity_axes": [],
            "motif_pools": {},
            "motif_quotas": {},
            "semantic_dropout": {"enabled": False},
            "exemplar_set": {},
            "safety_evaluation": {
                "mode": "automatic",
                "evaluation_requested": False,
                "status": "pass",
                "requires_user_approval": False,
                "items": [],
            },
        }
    if isinstance(payload, list):
        raw_anchors = payload
        min_anchors = len(raw_anchors)
        mode = "soft"
        concept = ""
        raw_anchor_expansion = {}
        raw_source_floors = {}
        raw_group_floors = {}
        raw_salience_floor = 0
        raw_visual_guards = []
        raw_render_priority_terms = []
        raw_free_slot_constraints = {}
        raw_render_suppress_terms = []
        raw_render_directives = []
        raw_dual_read_requirement = {}
        raw_preset_affinity = {}
        raw_role_scene_policy = {}
        raw_species_family_policy = {}
        raw_diversity_state = {}
        raw_soft_repair_policy = {}
        raw_safety_negative_floor = []
        raw_identity_axes = []
        raw_motif_pools = {}
        raw_motif_quotas = {}
        raw_semantic_dropout = {}
        raw_exemplar_set = {}
        raw_safety_evaluation = {}
    elif isinstance(payload, dict):
        raw_anchors = payload.get("anchors", [])
        min_anchors = payload.get("min_anchors", payload.get("soft_min_anchors", 0))
        mode = str(payload.get("mode") or "soft")
        concept = str(payload.get("concept") or "")
        raw_anchor_expansion = payload.get("anchor_expansion", {}) or {}
        raw_source_floors = payload.get("source_floors", payload.get("anchor_floor", {})) or {}
        raw_group_floors = payload.get("group_floors", payload.get("anchor_group_floor", {})) or {}
        raw_salience_floor = payload.get("salience_floor", 0)
        raw_visual_guards = payload.get("visual_guards", []) or []
        raw_render_priority_terms = payload.get("render_priority_terms", []) or []
        raw_free_slot_constraints = payload.get("free_slot_constraints", {}) or {}
        raw_render_suppress_terms = payload.get("render_suppress_terms", []) or []
        raw_render_directives = payload.get("render_directives", []) or []
        raw_dual_read_requirement = payload.get("dual_read_requirement", {}) or {}
        raw_preset_affinity = payload.get("preset_affinity", {}) or {}
        raw_role_scene_policy = payload.get("role_scene_policy", {}) or {}
        raw_species_family_policy = payload.get("species_family_policy", {}) or {}
        raw_diversity_state = payload.get("diversity_state", {}) or {}
        raw_soft_repair_policy = payload.get("soft_repair_policy", {}) or {}
        raw_safety_negative_floor = payload.get("safety_negative_floor", []) or []
        raw_identity_axes = payload.get("identity_axes", []) or []
        raw_motif_pools = payload.get("motif_pools", {}) or {}
        raw_motif_quotas = payload.get("motif_quotas", {}) or {}
        raw_semantic_dropout = payload.get("semantic_dropout", {}) or {}
        raw_exemplar_set = payload.get("exemplar_set", {}) or {}
        raw_safety_evaluation = payload.get("safety_evaluation", {}) or {}
    else:
        raise ValueError("--soft-anchor-spec must be a JSON object or list")
    if not isinstance(raw_anchors, list):
        raise ValueError("--soft-anchor-spec anchors must be a list")

    anchors: List[JsonDict] = []
    seen_slots: Set[str] = set()
    for raw in raw_anchors:
        if not isinstance(raw, dict):
            raise ValueError("--soft-anchor-spec anchor entries must be JSON objects")
        slot = str(raw.get("slot") or "").strip()
        ids = normalize_list(raw.get("ids"))
        if not slot or not ids:
            raise ValueError("--soft-anchor-spec anchor entries require slot and ids")
        terms = normalize_list(raw.get("terms"))
        pool = normalize_list(raw.get("pool")) or list(ids)
        source = str(raw.get("source") or "recipe")
        pool_weights: JsonDict = {}
        raw_pool_weights = raw.get("pool_weights")
        if isinstance(raw_pool_weights, dict):
            for item_id, weight in raw_pool_weights.items():
                try:
                    value = float(weight)
                except (TypeError, ValueError):
                    continue
                if value > 0 and str(item_id) in set(pool):
                    pool_weights[str(item_id)] = value
        anchors.append(
            {
                "slot": slot,
                "ids": ids,
                "pool": pool,
                "pool_weights": pool_weights,
                "terms": terms,
                "source": source,
                "required": bool(raw.get("required", True)),
                "critical": bool(raw.get("critical", False)),
                "groups": normalize_list(raw.get("groups")),
                "primary": bool(raw.get("primary", False)),
                "variant_group": str(raw.get("variant_group") or ""),
                "variant_strategy": str(raw.get("variant_strategy") or ""),
            }
        )
        seen_slots.add(slot)
    try:
        normalized_min = int(min_anchors)
    except (TypeError, ValueError):
        raise ValueError("--soft-anchor-spec min_anchors must be an integer")
    normalized_min = min(max(normalized_min, 0), len(seen_slots))
    source_floors: JsonDict = {}
    if isinstance(raw_source_floors, dict):
        for source, value in raw_source_floors.items():
            try:
                normalized_value = int(value)
            except (TypeError, ValueError):
                raise ValueError("--soft-anchor-spec source_floors values must be integers")
            if normalized_value > 0:
                source_floors[str(source)] = normalized_value
    group_floors: JsonDict = {}
    if isinstance(raw_group_floors, dict):
        for group, value in raw_group_floors.items():
            try:
                normalized_value = int(value)
            except (TypeError, ValueError):
                raise ValueError("--soft-anchor-spec group_floors values must be integers")
            if normalized_value > 0:
                group_floors[str(group)] = normalized_value
    try:
        salience_floor = int(raw_salience_floor)
    except (TypeError, ValueError):
        raise ValueError("--soft-anchor-spec salience_floor must be an integer")
    salience_floor = max(0, salience_floor)
    visual_guards = normalize_soft_visual_guards(raw_visual_guards)
    render_priority_terms = normalize_render_priority_terms(raw_render_priority_terms)
    free_slot_constraints = normalize_soft_free_slot_constraints(raw_free_slot_constraints)
    render_suppress_terms = normalize_list(raw_render_suppress_terms)
    render_directives = normalize_soft_render_directives(raw_render_directives)
    dual_read_requirement = normalize_dual_read_requirement(raw_dual_read_requirement)
    preset_affinity = normalize_soft_preset_affinity(raw_preset_affinity)
    role_scene_policy = normalize_role_scene_policy(raw_role_scene_policy)
    species_family_policy = normalize_species_family_policy(raw_species_family_policy)
    diversity_state = raw_diversity_state if isinstance(raw_diversity_state, dict) else {}
    soft_repair_policy = normalize_soft_repair_policy(raw_soft_repair_policy)
    safety_negative_floor = normalize_list(raw_safety_negative_floor)
    identity_axes = normalize_reference_identity_axes(raw_identity_axes)
    motif_pools = normalize_reference_motif_pools(raw_motif_pools)
    motif_quotas = normalize_reference_motif_quotas(raw_motif_quotas)
    semantic_dropout = normalize_reference_semantic_dropout(raw_semantic_dropout)
    exemplar_set = normalize_reference_exemplar_set(raw_exemplar_set)
    safety_evaluation = raw_safety_evaluation if isinstance(raw_safety_evaluation, dict) else {}
    selected_rate_floor = SOFT_ANCHOR_SELECTED_RATE_FLOOR
    if isinstance(payload, dict) and payload.get("selected_rate_floor") is not None:
        try:
            candidate_floor = float(payload.get("selected_rate_floor"))
        except (TypeError, ValueError):
            candidate_floor = selected_rate_floor
        if 0.0 < candidate_floor <= 1.0:
            selected_rate_floor = candidate_floor
    anchor_expansion: JsonDict = {}
    if isinstance(raw_anchor_expansion, dict) and raw_anchor_expansion:
        anchor_expansion = {"enabled": bool(raw_anchor_expansion.get("enabled"))}
        for key, caster in (("top_k", int), ("min_similarity", float), ("weight_ratio", float)):
            if key in raw_anchor_expansion:
                try:
                    anchor_expansion[key] = caster(raw_anchor_expansion[key])
                except (TypeError, ValueError):
                    continue
    return {
        "enabled": bool(anchors and normalized_min > 0),
        "mode": mode,
        "concept": concept,
        "selected_rate_floor": selected_rate_floor,
        "anchor_expansion": anchor_expansion,
        "min_anchors": normalized_min,
        "source_floors": source_floors,
        "group_floors": group_floors,
        "salience_floor": salience_floor,
        "visual_guards": visual_guards,
        "render_priority_terms": render_priority_terms,
        "free_slot_constraints": free_slot_constraints,
        "render_suppress_terms": render_suppress_terms,
        "render_directives": render_directives,
        "dual_read_requirement": dual_read_requirement,
        "preset_affinity": preset_affinity,
        "role_scene_policy": role_scene_policy,
        "species_family_policy": species_family_policy,
        "diversity_state": diversity_state,
        "soft_repair_policy": soft_repair_policy,
        "safety_negative_floor": safety_negative_floor,
        "identity_axes": identity_axes,
        "motif_pools": motif_pools,
        "motif_quotas": motif_quotas,
        "semantic_dropout": semantic_dropout,
        "exemplar_set": exemplar_set,
        "safety_evaluation": safety_evaluation,
        "anchors": anchors,
    }


def parse_soft_anchor_specs(items: Optional[Sequence[str]]) -> JsonDict:
    merged: JsonDict = {"mode": "soft", "concept": "", "min_anchors": 0, "anchors": []}
    for raw in items or []:
        payload = json.loads(raw)
        spec = normalize_soft_anchor_spec(payload)
        if spec.get("concept") and not merged.get("concept"):
            merged["concept"] = spec["concept"]
        merged["min_anchors"] = max(int(merged.get("min_anchors", 0)), int(spec.get("min_anchors", 0)))
        merged.setdefault("source_floors", {})
        for source, value in (spec.get("source_floors", {}) or {}).items():
            merged["source_floors"][source] = max(int(merged["source_floors"].get(source, 0)), int(value))
        merged.setdefault("group_floors", {})
        for group, value in (spec.get("group_floors", {}) or {}).items():
            merged["group_floors"][group] = max(int(merged["group_floors"].get(group, 0)), int(value))
        merged["salience_floor"] = max(int(merged.get("salience_floor", 0)), int(spec.get("salience_floor", 0)))
        merged.setdefault("visual_guards", [])
        for guard in spec.get("visual_guards", []) or []:
            if guard not in merged["visual_guards"]:
                merged["visual_guards"].append(guard)
        merged.setdefault("render_priority_terms", [])
        for group in spec.get("render_priority_terms", []) or []:
            if group not in merged["render_priority_terms"]:
                merged["render_priority_terms"].append(group)
        merged.setdefault("free_slot_constraints", {})
        for slot, constraint in (spec.get("free_slot_constraints", {}) or {}).items():
            if isinstance(constraint, dict):
                merged["free_slot_constraints"].setdefault(slot, {}).update(constraint)
        merged.setdefault("render_suppress_terms", [])
        for term in normalize_list(spec.get("render_suppress_terms")):
            if term not in merged["render_suppress_terms"]:
                merged["render_suppress_terms"].append(term)
        merged.setdefault("render_directives", [])
        for directive in spec.get("render_directives", []) or []:
            if directive not in merged["render_directives"]:
                merged["render_directives"].append(directive)
        if spec.get("dual_read_requirement"):
            merged["dual_read_requirement"] = spec.get("dual_read_requirement")
        if spec.get("preset_affinity"):
            merged.setdefault("preset_affinity", {}).update(spec.get("preset_affinity") or {})
        if spec.get("role_scene_policy"):
            merge_role_scene_policies(merged.setdefault("role_scene_policy", {}), spec.get("role_scene_policy") or {})
        if spec.get("species_family_policy"):
            merge_species_family_policies(
                merged.setdefault("species_family_policy", {}),
                spec.get("species_family_policy") or {},
            )
        if spec.get("diversity_state"):
            merged.setdefault("diversity_state", {}).update(spec.get("diversity_state") or {})
        if spec.get("soft_repair_policy"):
            merged.setdefault("soft_repair_policy", {}).update(spec.get("soft_repair_policy") or {})
        if spec.get("anchor_expansion"):
            merged.setdefault("anchor_expansion", {}).update(spec.get("anchor_expansion") or {})
        merged.setdefault("identity_axes", [])
        existing_axes = {str(axis.get("id")) for axis in merged["identity_axes"] if isinstance(axis, dict)}
        for axis in spec.get("identity_axes", []) or []:
            if isinstance(axis, dict) and str(axis.get("id")) not in existing_axes:
                merged["identity_axes"].append(axis)
                existing_axes.add(str(axis.get("id")))
        if spec.get("motif_pools"):
            merged.setdefault("motif_pools", {}).update(spec.get("motif_pools") or {})
        if spec.get("motif_quotas"):
            merged.setdefault("motif_quotas", {}).update(spec.get("motif_quotas") or {})
        if spec.get("semantic_dropout"):
            merged.setdefault("semantic_dropout", {}).update(spec.get("semantic_dropout") or {})
        if spec.get("exemplar_set"):
            merged.setdefault("exemplar_set", {}).update(spec.get("exemplar_set") or {})
        if spec.get("safety_evaluation"):
            merged.setdefault("safety_evaluation", {}).update(spec.get("safety_evaluation") or {})
        merged.setdefault("safety_negative_floor", [])
        for term in normalize_list(spec.get("safety_negative_floor")):
            if term not in merged["safety_negative_floor"]:
                merged["safety_negative_floor"].append(term)
        merged["anchors"].extend(spec.get("anchors", []))
    return normalize_soft_anchor_spec(merged)


def parse_json_object_list(items: Optional[Sequence[str]], option: str) -> List[JsonDict]:
    parsed: List[JsonDict] = []
    for raw in items or []:
        payload = json.loads(raw)
        rows = payload if isinstance(payload, list) else [payload]
        if not all(isinstance(row, dict) for row in rows):
            raise ValueError(f"{option} must contain a JSON object or array of objects")
        parsed.extend(dict(row) for row in rows)
    return parsed


def normalize_slot_id_map(raw: Any) -> JsonDict:
    if not isinstance(raw, dict):
        return {}
    normalized: JsonDict = {}
    for slot, ids in raw.items():
        values = normalize_list(ids)
        if values:
            normalized[str(slot)] = values
    return normalized


def normalize_soft_free_slot_constraints(raw: Any) -> JsonDict:
    if not isinstance(raw, dict):
        return {}
    normalized: JsonDict = {}
    for slot, constraint in raw.items():
        if not isinstance(constraint, dict):
            continue
        row: JsonDict = {}
        for key in ("allow_pool", "deny_pool", "prefer_ids"):
            values = normalize_list(constraint.get(key))
            if values:
                row[key] = values
        if bool(constraint.get("fail_closed")):
            row["fail_closed"] = True
        if row:
            normalized[str(slot)] = row
    return normalized


def normalize_soft_preset_affinity(raw: Any) -> JsonDict:
    if not isinstance(raw, dict):
        return {}
    normalized: JsonDict = {}
    for key in ("preferred_presets", "discouraged_presets", "preferred_axes", "discouraged_axes"):
        values = normalize_list(raw.get(key))
        if values:
            normalized[key] = values
    return normalized


def normalize_role_scene_policy(raw: Any) -> JsonDict:
    if not isinstance(raw, dict):
        return {"enabled": False}
    normalized: JsonDict = {}
    for key in (
        "allowed_locations",
        "preferred_locations",
        "forbidden_locations",
        "discouraged_generic_locations",
        "discouraged_generic_moods",
        "support_presets",
        "discouraged_presets",
    ):
        values = normalize_list(raw.get(key))
        if values:
            normalized[key] = values
    for key in ("enabled", "enforce", "role_first", "generic_preset_support_only_when_role_scene_missing"):
        if key in raw:
            normalized[key] = bool(raw.get(key))
    for key in ("scene_family", "reason"):
        value = str(raw.get(key) or "").strip()
        if value:
            normalized[key] = value
    if normalized and "enabled" not in normalized:
        normalized["enabled"] = True
    normalized.setdefault("enabled", False)
    return normalized


def merge_role_scene_policies(base: JsonDict, incoming: Any) -> JsonDict:
    policy = normalize_role_scene_policy(incoming)
    if not policy.get("enabled") and not any(policy.get(key) for key in ("allowed_locations", "preferred_locations", "forbidden_locations")):
        return base
    base["enabled"] = bool(base.get("enabled") or policy.get("enabled", True))
    for key in (
        "allowed_locations",
        "preferred_locations",
        "forbidden_locations",
        "discouraged_generic_locations",
        "discouraged_generic_moods",
        "support_presets",
        "discouraged_presets",
    ):
        bucket = base.setdefault(key, [])
        for value in normalize_list(policy.get(key)):
            if value not in bucket:
                bucket.append(value)
    for key in ("enforce", "role_first", "generic_preset_support_only_when_role_scene_missing"):
        if key in policy:
            base[key] = bool(base.get(key) or policy.get(key))
    for key in ("scene_family", "reason"):
        value = str(policy.get(key) or "").strip()
        if value and not base.get(key):
            base[key] = value
    return base


def normalize_species_family_policy(raw: Any) -> JsonDict:
    if not isinstance(raw, dict):
        return {"enabled": False, "allowed": {}}
    allowed: JsonDict = {}
    raw_allowed = raw.get("allowed")
    if isinstance(raw_allowed, dict):
        for slot, ids in raw_allowed.items():
            values = normalize_list(ids)
            if values:
                allowed[str(slot)] = values
    normalized: JsonDict = {
        "enabled": bool(raw.get("enabled", bool(allowed))),
        "allowed": allowed,
        "enforce": bool(raw.get("enforce", True)),
        "hybrid_allowed": bool(raw.get("hybrid_allowed", False)),
    }
    for key in ("family", "variant_id", "mixin", "tier"):
        value = str(raw.get(key) or "").strip()
        if value:
            normalized[key] = value
    return normalized


def merge_species_family_policies(base: JsonDict, incoming: Any) -> JsonDict:
    policy = normalize_species_family_policy(incoming)
    if not policy.get("enabled") and not policy.get("allowed"):
        return base
    base["enabled"] = bool(base.get("enabled") or policy.get("enabled", True))
    for key in ("family", "variant_id", "mixin", "tier"):
        value = str(policy.get(key) or "").strip()
        if value and not base.get(key):
            base[key] = value
    for key in ("enforce", "hybrid_allowed"):
        if key in policy:
            base[key] = bool(base.get(key) or policy.get(key))
    allowed = base.setdefault("allowed", {})
    for slot, ids in (policy.get("allowed") or {}).items():
        bucket = allowed.setdefault(str(slot), [])
        for value in normalize_list(ids):
            if value not in bucket:
                bucket.append(value)
    return base


def normalize_soft_render_directives(raw: Any) -> List[JsonDict]:
    if isinstance(raw, dict):
        raw_items = [raw]
    elif isinstance(raw, list):
        raw_items = [item for item in raw if isinstance(item, dict)]
    else:
        raw_items = []
    directives: List[JsonDict] = []
    for index, item in enumerate(raw_items):
        cue_terms = normalize_list(item.get("cue_terms"))
        positive_clause = str(item.get("positive_clause") or "").strip()
        suppress_terms = normalize_list(item.get("suppress_terms"))
        if not cue_terms or not positive_clause:
            continue
        directives.append(
            {
                "id": str(item.get("id") or f"render_directive_{index}"),
                "cue_terms": cue_terms,
                "render_as": str(item.get("render_as") or ""),
                "positive_clause": positive_clause,
                "suppress_terms": suppress_terms,
            }
        )
    return directives


def normalize_dual_read_requirement(raw: Any) -> JsonDict:
    if not isinstance(raw, dict):
        return {}
    role_terms = normalize_list(raw.get("role_terms"))
    mixin_terms = normalize_list(raw.get("mixin_terms"))
    if not role_terms and not mixin_terms and raw.get("enabled") is not False:
        return {}
    return {
        "enabled": bool(raw.get("enabled", True)),
        "role_terms": role_terms,
        "mixin_terms": mixin_terms,
        "min_role_hits": max(1, int(raw.get("min_role_hits", 1) or 1)),
        "min_mixin_hits": max(1, int(raw.get("min_mixin_hits", 1) or 1)),
    }


def normalize_soft_visual_guards(raw: Any) -> List[JsonDict]:
    if isinstance(raw, dict):
        raw_guards = [raw]
    elif isinstance(raw, list):
        raw_guards = [guard for guard in raw if isinstance(guard, dict)]
    else:
        raw_guards = []
    guards: List[JsonDict] = []
    for index, guard in enumerate(raw_guards):
        deny_ids = normalize_slot_id_map(guard.get("deny_ids") or guard.get("deny"))
        prefer_ids = normalize_slot_id_map(guard.get("prefer_ids") or guard.get("prefer"))
        deny_facets = normalize_slot_id_map(guard.get("deny_facets"))
        fail_closed = bool(guard.get("fail_closed"))
        if not deny_ids and not prefer_ids and not deny_facets:
            continue
        guards.append(
            {
                "id": str(guard.get("id") or f"visual_guard_{index}"),
                "reason": str(guard.get("reason") or "soft_visual_guard"),
                "deny_ids": deny_ids,
                "prefer_ids": prefer_ids,
                "deny_facets": deny_facets,
                "fail_closed": fail_closed,
            }
        )
    return guards


def normalize_render_priority_terms(raw: Any) -> List[JsonDict]:
    if isinstance(raw, dict):
        raw_groups = [raw]
    elif isinstance(raw, list):
        raw_groups = raw
    elif isinstance(raw, str):
        raw_groups = [raw]
    else:
        raw_groups = []
    groups: List[JsonDict] = []
    for index, group in enumerate(raw_groups):
        if isinstance(group, dict):
            terms = normalize_list(group.get("terms"))
            raw_min_hits = group.get("min_hits", 1)
            group_id = str(group.get("id") or f"priority_{index}")
            tier = str(group.get("tier") or "required").strip() or "required"
            group_name = str(group.get("group") or group_id).strip() or group_id
            target_slots = normalize_list(group.get("target_slots"))
        else:
            terms = normalize_list(group)
            raw_min_hits = 1
            group_id = f"priority_{index}"
            tier = "required"
            group_name = group_id
            target_slots = []
        try:
            min_hits = int(raw_min_hits)
        except (TypeError, ValueError):
            min_hits = 1
        if terms:
            groups.append(
                {
                    "id": group_id,
                    "group": group_name,
                    "tier": tier if tier in {"required", "support"} else "required",
                    "terms": terms,
                    "min_hits": max(1, min_hits),
                    "target_slots": target_slots,
                }
            )
    return groups


def normalize_soft_repair_policy(raw: Any) -> JsonDict:
    if not isinstance(raw, dict):
        raw = {}
    try:
        max_attempts = int(raw.get("max_attempts", 2))
    except (TypeError, ValueError):
        max_attempts = 2
    trigger_checks = normalize_list(raw.get("trigger_checks")) or [
        "required_render_priority_missing",
        "dual_read_missing",
        "body_first_survivor",
        "free_slot_constraint_violation",
    ]
    target_slots = normalize_list(raw.get("target_slots")) or [
        "subject_framing",
        "composition",
        "action",
        "prop",
        "body_framing",
    ]
    strategy = str(raw.get("strategy") or "prefer_then_reselect")
    if strategy not in {"prefer_then_reselect"}:
        strategy = "prefer_then_reselect"
    return {
        "enabled": bool(raw.get("enabled", True)),
        "max_attempts": max(0, max_attempts),
        "trigger_checks": trigger_checks,
        "target_slots": target_slots,
        "strategy": strategy,
        "fail_open": bool(raw.get("fail_open", False)),
    }


def soft_anchor_slots(policy: Optional[JsonDict]) -> List[str]:
    if not policy or not policy.get("enabled"):
        return []
    slots: List[str] = []
    for anchor in policy.get("anchors", []):
        slot = str(anchor.get("slot") or "")
        if slot and slot not in slots:
            slots.append(slot)
    return slots


def soft_anchor_ids_for_slot(policy: Optional[JsonDict], slot: str) -> Set[str]:
    if not policy or not policy.get("enabled"):
        return set()
    ids: Set[str] = set()
    for anchor in policy.get("anchors", []):
        if anchor.get("slot") == slot:
            ids.update(normalize_list(anchor.get("ids")))
    return ids


def soft_anchor_weight_multipliers(source: Optional[JsonDict]) -> tuple[float, float, float, float]:
    """(base, promoted, critical, primary) multipliers; overridable via semantic_policy.soft_anchor_weights."""
    base = semantic_policy_float(source, ("soft_anchor_weights", "base"), SOFT_ANCHOR_WEIGHT_MULTIPLIER)
    promoted = semantic_policy_float(source, ("soft_anchor_weights", "promoted"), SOFT_ANCHOR_PROMOTED_WEIGHT_MULTIPLIER)
    critical = semantic_policy_float(source, ("soft_anchor_weights", "critical"), SOFT_ANCHOR_CRITICAL_WEIGHT_MULTIPLIER)
    primary = semantic_policy_float(source, ("soft_anchor_weights", "primary"), SOFT_ANCHOR_PRIMARY_WEIGHT_MULTIPLIER)
    return base, promoted, critical, primary


def anchor_expansion_settings(policy: JsonDict, semantic_context: Optional[JsonDict]) -> Optional[JsonDict]:
    config = policy.get("anchor_expansion")
    if not isinstance(config, dict) or not config.get("enabled"):
        return None
    try:
        top_k = max(1, int(config.get("top_k", 3)))
    except (TypeError, ValueError):
        top_k = 3
    try:
        min_similarity = float(config.get("min_similarity", 0.78))
    except (TypeError, ValueError):
        min_similarity = 0.78
    try:
        weight_ratio = float(config.get("weight_ratio", 0.5))
    except (TypeError, ValueError):
        weight_ratio = 0.5
    creativity = (semantic_context or {}).get("creativity")
    if creativity is not None:
        # Higher creativity widens the semantic neighborhood slightly.
        value = clamp_unit_interval(creativity)
        if value >= 0.75:
            top_k += 1
        min_similarity = max(0.5, min_similarity - 0.06 * value)
    return {"top_k": top_k, "min_similarity": min_similarity, "weight_ratio": max(0.05, min(weight_ratio, 1.0))}


def expand_soft_anchor_pools(
    generation_contract: Optional[JsonDict],
    semantic_context: Optional[JsonDict],
    data: JsonDict,
) -> None:
    """Opt-in semantic widening of soft anchor pools.

    Each non-critical anchor pool member pulls its top-k same-slot embedding
    neighbors into the pool at a reduced in-pool weight. Expanded members stay
    subject to the normal hard guards and slot-conflict checks downstream, so
    expansion widens the related candidate set without bypassing coherence.
    """
    if not semantic_context:
        return
    policy = (generation_contract or {}).get("soft_anchor_policy") or {}
    if not policy.get("enabled"):
        return
    settings = anchor_expansion_settings(policy, semantic_context)
    if not settings:
        return
    index_entries = (semantic_context.get("index") or {}).get("entries", {}) or {}
    if not index_entries:
        return
    expansions: List[JsonDict] = []
    for anchor in policy.get("anchors", []):
        slot = str(anchor.get("slot") or "")
        if not slot or anchor.get("critical"):
            continue
        pool = normalize_list(anchor.get("pool")) or normalize_list(anchor.get("ids"))
        if not pool:
            continue
        slot_entries = data.get("slots", {}).get(slot, [])
        if not slot_entries:
            continue
        pool_set = set(pool)
        candidate_scores: Dict[str, float] = {}
        for member in pool:
            member_vector = (index_entries.get(f"slot:{slot}:{member}") or {}).get("vector")
            if not member_vector:
                continue
            scored: List[tuple[float, str]] = []
            for entry in slot_entries:
                entry_id = str(entry.get("id") or "")
                if not entry_id or entry_id in pool_set:
                    continue
                vector = (index_entries.get(f"slot:{slot}:{entry_id}") or {}).get("vector")
                if not vector:
                    continue
                similarity = cosine_similarity(member_vector, vector)
                if similarity >= settings["min_similarity"]:
                    scored.append((similarity, entry_id))
            scored.sort(reverse=True)
            for similarity, entry_id in scored[: settings["top_k"]]:
                candidate_scores[entry_id] = max(candidate_scores.get(entry_id, 0.0), similarity)
        if not candidate_scores:
            continue
        added = sorted(candidate_scores, key=lambda entry_id: (-candidate_scores[entry_id], entry_id))
        pool_weights = anchor.get("pool_weights")
        if not isinstance(pool_weights, dict):
            pool_weights = {}
            anchor["pool_weights"] = pool_weights
        for entry_id in added:
            pool.append(entry_id)
            pool_weights[entry_id] = settings["weight_ratio"]
        anchor["pool"] = pool
        expansions.append(
            {
                "slot": slot,
                "added": [
                    {"id": entry_id, "similarity": round(candidate_scores[entry_id], 4)}
                    for entry_id in added
                ],
                "settings": settings,
            }
        )
    if expansions:
        record_generation_contract_event(
            generation_contract,
            "soft_anchor_pool_expansion",
            {
                "reason": "anchor_expansion_semantic_neighbors",
                "reason_code": "anchor_expansion_semantic_neighbors",
                "expansions": expansions,
            },
        )


def soft_anchor_pool_for_slot(policy: Optional[JsonDict], slot: str, critical_only: bool = False) -> Set[str]:
    if not policy or not policy.get("enabled"):
        return set()
    ids: Set[str] = set()
    for anchor in policy.get("anchors", []):
        if anchor.get("slot") != slot:
            continue
        if critical_only and not bool(anchor.get("critical")):
            continue
        ids.update(normalize_list(anchor.get("pool")) or normalize_list(anchor.get("ids")))
    return ids


def soft_anchor_atomic_pool_for_slot(policy: Optional[JsonDict], slot: str) -> Set[str]:
    if not policy or not policy.get("enabled"):
        return set()
    ids: Set[str] = set()
    for anchor in policy.get("anchors", []):
        if anchor.get("slot") != slot or str(anchor.get("variant_strategy") or "") != "atomic_scene":
            continue
        ids.update(normalize_list(anchor.get("pool")) or normalize_list(anchor.get("ids")))
    return ids


def soft_anchor_entries_for_slot(policy: Optional[JsonDict], slot: str) -> List[JsonDict]:
    if not policy or not policy.get("enabled"):
        return []
    return [anchor for anchor in policy.get("anchors", []) if anchor.get("slot") == slot]


def soft_anchor_pool_weight(policy: Optional[JsonDict], slot: str, item_id: str) -> float:
    """Relative in-pool weight for a soft-anchor pool member (default 1.0)."""
    values: List[float] = []
    for anchor in soft_anchor_entries_for_slot(policy, slot):
        pool_weights = anchor.get("pool_weights")
        if not isinstance(pool_weights, dict):
            continue
        raw = pool_weights.get(item_id)
        if raw is None:
            continue
        try:
            value = float(raw)
        except (TypeError, ValueError):
            continue
        if value > 0:
            values.append(value)
    return max(values) if values else 1.0


def soft_anchor_critical_slot(policy: Optional[JsonDict], slot: str) -> bool:
    return bool(soft_anchor_pool_for_slot(policy, slot, critical_only=True))


def soft_anchor_all_ids(policy: Optional[JsonDict]) -> Set[str]:
    if not policy or not policy.get("enabled"):
        return set()
    ids: Set[str] = set()
    for anchor in policy.get("anchors", []):
        ids.update(normalize_list(anchor.get("ids")))
    return ids


def soft_anchor_variant_group_for_slot(policy: Optional[JsonDict], slot: str) -> str:
    if not policy or not policy.get("enabled"):
        return ""
    for anchor in policy.get("anchors", []):
        if anchor.get("slot") == slot and str(anchor.get("variant_group") or ""):
            return str(anchor.get("variant_group") or "")
    return ""


def soft_anchor_selected_rate_floor(policy: Optional[JsonDict]) -> float:
    raw = (policy or {}).get("selected_rate_floor")
    try:
        value = float(raw)
    except (TypeError, ValueError):
        return SOFT_ANCHOR_SELECTED_RATE_FLOOR
    if 0.0 < value <= 1.0:
        return value
    return SOFT_ANCHOR_SELECTED_RATE_FLOOR


def soft_anchor_required_count(policy: Optional[JsonDict]) -> int:
    if not policy or not policy.get("enabled"):
        return 0
    anchor_count = len(soft_anchor_slots(policy))
    configured_min = int(policy.get("min_anchors", 0) or 0)
    rate_floor = int(math.ceil(anchor_count * soft_anchor_selected_rate_floor(policy)))
    critical_slots = {str(anchor.get("slot")) for anchor in policy.get("anchors", []) if anchor.get("critical")}
    source_floor_total = 0
    for value in (policy.get("source_floors", {}) or {}).values():
        try:
            floor_value = int(value)
        except (TypeError, ValueError):
            continue
        if floor_value > 0:
            source_floor_total += floor_value
    return min(anchor_count, max(configured_min, rate_floor, len(critical_slots), source_floor_total))


def selected_soft_anchor_slots(policy: Optional[JsonDict], picked: Dict[str, Entry]) -> Set[str]:
    selected: Set[str] = set()
    if not policy or not policy.get("enabled"):
        return selected
    for slot in soft_anchor_slots(policy):
        entry = picked.get(slot)
        if not entry:
            continue
        if str(entry.get("id")) in soft_anchor_pool_for_slot(policy, slot):
            selected.add(slot)
    return selected


def soft_anchor_sources(source: Any) -> Set[str]:
    return {part for part in str(source or "recipe").split("+") if part}


def soft_anchor_match_status(policy: Optional[JsonDict], picked: Dict[str, Entry]) -> JsonDict:
    if not policy or not policy.get("enabled"):
        return {"enabled": False, "passed": True, "failure_reasons": []}
    anchors = policy.get("anchors", []) or []
    selected_slots = selected_soft_anchor_slots(policy, picked)
    matched_anchors: List[JsonDict] = []
    missing_anchors: List[JsonDict] = []
    source_counts: Dict[str, int] = {}
    source_totals: Dict[str, int] = {}
    group_counts: Dict[str, int] = {}
    group_totals: Dict[str, int] = {}
    critical_missing: List[str] = []
    salience_matches = 0
    salience_total = 0
    slot_union_pools: Dict[str, Set[str]] = {}
    source_slots: Dict[str, Set[str]] = {}
    for anchor in anchors:
        slot = str(anchor.get("slot") or "")
        pool_ids = set(normalize_list(anchor.get("pool")) or normalize_list(anchor.get("ids")))
        selected = picked.get(slot, {})
        selected_id = str(selected.get("id") or "")
        matched = bool(selected_id and selected_id in pool_ids)
        sources = soft_anchor_sources(anchor.get("source"))
        groups = set(normalize_list(anchor.get("groups")))
        row = {
            "slot": slot,
            "selected": selected_id,
            "expected": sorted(pool_ids),
            "source": anchor.get("source", "recipe"),
            "critical": bool(anchor.get("critical")),
                "groups": sorted(groups),
                "primary": bool(anchor.get("primary")),
                "variant_group": str(anchor.get("variant_group") or ""),
                "variant_strategy": str(anchor.get("variant_strategy") or ""),
                "matched": matched,
            }
        if matched:
            matched_anchors.append(row)
        else:
            missing_anchors.append(row)
        if anchor.get("critical") and not matched:
            critical_missing.append(slot)
        slot_union_pools.setdefault(slot, set()).update(pool_ids)
        for source in sources:
            source_totals[source] = source_totals.get(source, 0) + 1
            source_slots.setdefault(source, set()).add(slot)
            if matched:
                source_counts[source] = source_counts.get(source, 0) + 1
        if "mixin" in sources:
            salience_total += 1
            if matched:
                salience_matches += 1
        for group in groups:
            group_totals[group] = group_totals.get(group, 0) + 1
            if matched:
                group_counts[group] = group_counts.get(group, 0) + 1

    source_floor_misses: List[JsonDict] = []
    for source, raw_floor in (policy.get("source_floors", {}) or {}).items():
        floor = int(raw_floor)
        matched = int(source_counts.get(source, 0))
        if matched < floor:
            source_floor_misses.append({"source": source, "matched": matched, "floor": floor})
    group_floor_misses: List[JsonDict] = []
    for group, raw_floor in (policy.get("group_floors", {}) or {}).items():
        floor = int(raw_floor)
        matched = int(group_counts.get(group, 0))
        if matched < floor:
            group_floor_misses.append({"group": group, "matched": matched, "floor": floor})

    # Slot-level per-source match rates. The quality gate enforces rate floors
    # (role >= 0.90, mixin >= 0.80), so the repair contract must trip on the
    # same condition — count floors alone let a 2/3 source slip through.
    slot_matched_by_union = {
        slot
        for slot, ids in slot_union_pools.items()
        if str((picked.get(slot) or {}).get("id") or "") in ids
    }
    rate_floors = dict(DEFAULT_SOFT_ANCHOR_SOURCE_RATE_FLOORS)
    for source, raw in (policy.get("source_rate_floors", {}) or {}).items():
        rate_floors[str(source)] = float(raw)
    source_rate_misses: List[JsonDict] = []
    source_rates: Dict[str, float] = {}
    for source, slots in source_slots.items():
        rate = len(slots & slot_matched_by_union) / len(slots)
        source_rates[source] = round(rate, 4)
        floor = rate_floors.get(source)
        if floor is not None and rate < float(floor):
            source_rate_misses.append(
                {
                    "source": source,
                    "rate": round(rate, 4),
                    "floor": float(floor),
                    "missing_slots": sorted(slots - slot_matched_by_union),
                }
            )

    anchor_slot_count = len(soft_anchor_slots(policy))
    selected_rate = len(selected_slots) / max(1, anchor_slot_count)
    min_anchors = soft_anchor_required_count(policy)
    salience_floor = min(int(policy.get("salience_floor", 0) or 0), salience_total)
    failure_reasons: List[str] = []
    if critical_missing:
        failure_reasons.append("critical_anchor_missing")
    for miss in source_floor_misses:
        failure_reasons.append(f"source_floor_not_met:{miss['source']}")
    for miss in group_floor_misses:
        failure_reasons.append(f"anchor_group_floor_not_met:{miss['group']}")
    for miss in source_rate_misses:
        failure_reasons.append(f"source_rate_floor_not_met:{miss['source']}")
    if salience_matches < salience_floor:
        failure_reasons.append("mixin_salience_floor_not_met")
    if len(selected_slots) < min_anchors or selected_rate < soft_anchor_selected_rate_floor(policy):
        failure_reasons.append("selected_anchor_rate_below_floor")
    return {
        "enabled": True,
        "passed": not failure_reasons,
        "failure_reasons": sorted(set(failure_reasons)),
        "selected_anchor_count": len(selected_slots),
        "required_anchor_count": min_anchors,
        "selected_anchor_slots": sorted(selected_slots),
        "anchor_slot_count": anchor_slot_count,
        "selected_anchor_rate": round(selected_rate, 4),
        "critical_missing": sorted(set(critical_missing)),
        "source_counts": source_counts,
        "source_totals": source_totals,
        "source_floor_misses": source_floor_misses,
        "group_counts": group_counts,
        "group_totals": group_totals,
        "group_floor_misses": group_floor_misses,
        "source_rates": source_rates,
        "source_rate_misses": source_rate_misses,
        "salience_matches": salience_matches,
        "salience_total": salience_total,
        "salience_floor": salience_floor,
        "matched_anchors": matched_anchors,
        "missing_anchors": missing_anchors,
    }


def soft_anchor_trace(policy: Optional[JsonDict], picked: Optional[Dict[str, Entry]] = None) -> JsonDict:
    if not policy or not policy.get("enabled"):
        return {"enabled": False, "min_anchors": 0, "anchors": []}
    picked = picked or {}
    selected_slots = selected_soft_anchor_slots(policy, picked)
    anchors: List[JsonDict] = []
    for anchor in policy.get("anchors", []):
        slot = str(anchor.get("slot") or "")
        selected = picked.get(slot, {})
        anchors.append(
            {
                "slot": slot,
                "ids": normalize_list(anchor.get("ids")),
                "pool": normalize_list(anchor.get("pool")) or normalize_list(anchor.get("ids")),
                "terms": normalize_list(anchor.get("terms")),
                "source": anchor.get("source", "recipe"),
                "required": bool(anchor.get("required", True)),
                "critical": bool(anchor.get("critical", False)),
                "groups": normalize_list(anchor.get("groups")),
                "primary": bool(anchor.get("primary")),
                "variant_group": str(anchor.get("variant_group") or ""),
                "variant_strategy": str(anchor.get("variant_strategy") or ""),
                "pool_weights": dict(anchor.get("pool_weights") or {}),
                "selected": selected.get("id"),
                "matched": slot in selected_slots,
            }
        )
    status = soft_anchor_match_status(policy, picked)
    return {
        "enabled": True,
        "mode": policy.get("mode", "soft"),
        "concept": policy.get("concept", ""),
        "anchor_expansion": dict(policy.get("anchor_expansion") or {}),
        "min_anchors": int(policy.get("min_anchors", 0)),
        "source_floors": policy.get("source_floors", {}) or {},
        "group_floors": policy.get("group_floors", {}) or {},
        "salience_floor": int(policy.get("salience_floor", 0) or 0),
        "visual_guards": policy.get("visual_guards", []) or [],
        "render_priority_terms": policy.get("render_priority_terms", []) or [],
        "free_slot_constraints": policy.get("free_slot_constraints", {}) or {},
        "render_suppress_terms": policy.get("render_suppress_terms", []) or [],
        "render_directives": policy.get("render_directives", []) or [],
        "dual_read_requirement": policy.get("dual_read_requirement", {}) or {},
        "preset_affinity": policy.get("preset_affinity", {}) or {},
        "role_scene_policy": policy.get("role_scene_policy", {}) or {"enabled": False},
        "species_family_policy": policy.get("species_family_policy", {}) or {"enabled": False, "allowed": {}},
        "diversity_state": policy.get("diversity_state", {}) or {},
        "soft_repair_policy": policy.get("soft_repair_policy", {}) or normalize_soft_repair_policy({}),
        "safety_negative_floor": policy.get("safety_negative_floor", []) or [],
        "identity_axes": policy.get("identity_axes", []) or [],
        "motif_pools": policy.get("motif_pools", {}) or {},
        "motif_quotas": policy.get("motif_quotas", {}) or {},
        "semantic_dropout": policy.get("semantic_dropout", {}) or {"enabled": False},
        "exemplar_set": policy.get("exemplar_set", {}) or {},
        "safety_evaluation": policy.get("safety_evaluation", {}) or {},
        "required_anchor_count": soft_anchor_required_count(policy),
        "selected_anchor_count": len(selected_slots),
        "selected_anchor_slots": sorted(selected_slots),
        "anchor_slot_count": len(soft_anchor_slots(policy)),
        "match_status": status,
        "anchors": anchors,
    }


def entry_matches_guard_facets(item: Entry, raw_facets: Sequence[str]) -> bool:
    tokens = facet_tokens(item)
    for raw in raw_facets:
        token = str(raw)
        if ":" in token:
            key, value = token.split(":", 1)
            facets = item.get("facets", {}) or {}
            if value in normalize_list(facets.get(key)):
                return True
        elif token in tokens:
            return True
    return False


def soft_visual_guard_for_slot(policy: Optional[JsonDict], slot: str) -> JsonDict:
    deny_ids: Set[str] = set()
    prefer_ids: Set[str] = set()
    deny_facets: Set[str] = set()
    guard_ids: List[str] = []
    fail_closed = False
    for guard in (policy or {}).get("visual_guards", []) or []:
        deny_ids.update(normalize_list((guard.get("deny_ids", {}) or {}).get(slot)))
        prefer_ids.update(normalize_list((guard.get("prefer_ids", {}) or {}).get(slot)))
        deny_facets.update(normalize_list((guard.get("deny_facets", {}) or {}).get(slot)))
        if (guard.get("deny_ids", {}) or {}).get(slot) or (guard.get("prefer_ids", {}) or {}).get(slot) or (guard.get("deny_facets", {}) or {}).get(slot):
            guard_ids.append(str(guard.get("id") or "visual_guard"))
            fail_closed = fail_closed or bool(guard.get("fail_closed"))
    return {"deny_ids": deny_ids, "prefer_ids": prefer_ids, "deny_facets": deny_facets, "guard_ids": guard_ids, "fail_closed": fail_closed}


def apply_soft_body_first_guard(
    slot: str,
    pool: Sequence[Entry],
    semantic_context: Optional[JsonDict],
    generation_contract: Optional[JsonDict],
) -> List[Entry]:
    policy = (generation_contract or {}).get("soft_anchor_policy", {})
    if not policy or not policy.get("enabled") or not semantic_context:
        return list(pool)
    guard_policy = (semantic_policy_from_source(semantic_context).get("soft_body_first_guard", {}) or {})
    guard_slots = normalize_list(guard_policy.get("slots"))
    legacy_slot = str(guard_policy.get("slot") or "").strip()
    if legacy_slot and legacy_slot not in guard_slots:
        guard_slots.append(legacy_slot)
    if not guard_slots:
        guard_slots = ["body_framing"]
    if slot not in guard_slots:
        return list(pool)
    if not any(anchor.get("critical") for anchor in policy.get("anchors", []) or []):
        return list(pool)
    demote_facets = normalize_list(guard_policy.get("demote_facets")) or ["soft_body_role:body_emphasis"]
    prefer_facets = normalize_list(guard_policy.get("prefer_facets"))
    try:
        multiplier = float(guard_policy.get("demote_multiplier", 0.15))
    except (TypeError, ValueError):
        multiplier = 0.15
    per_slot_multiplier = guard_policy.get("per_slot_multiplier", {}) or {}
    if isinstance(per_slot_multiplier, dict) and slot in per_slot_multiplier:
        try:
            multiplier = float(per_slot_multiplier.get(slot))
        except (TypeError, ValueError):
            multiplier = multiplier
    multiplier = min(max(multiplier, 0.0), 1.0)
    adjusted: List[Entry] = []
    demoted: List[str] = []
    preferred: List[str] = []
    for item in pool:
        if entry_matches_guard_facets(item, demote_facets):
            copied = dict(item)
            base_weight = item_base_weight(item)
            copied["weight"] = round(base_weight * multiplier, 6)
            adjusted.append(copied)
            demoted.append(str(item.get("id")))
        elif prefer_facets and entry_matches_guard_facets(item, prefer_facets):
            copied = dict(item)
            copied["weight"] = round(item_base_weight(item) * soft_anchor_weight_multipliers(semantic_context)[1], 6)
            adjusted.append(copied)
            preferred.append(str(item.get("id")))
        else:
            adjusted.append(item)
    if demoted or preferred:
        record_generation_contract_event(
            generation_contract,
            "soft_body_first_guard_events",
            {
                "slot": slot,
                "reason": "soft_body_first_guard",
                "reason_code": "soft_body_first_guard",
                "body_first_guard_applied": True,
                "guard_slots": guard_slots,
                "demote_facets": demote_facets,
                "prefer_facets": prefer_facets,
                "demote_multiplier": round(multiplier, 4),
                "demoted_ids": sorted(set(demoted)),
                "preferred_ids": sorted(set(preferred)),
                "policy_schema_version": semantic_policy_schema_version(semantic_context),
                "semantic_policy_hash": semantic_context.get("semantic_policy_hash"),
            },
        )
    return adjusted


def apply_soft_free_slot_constraints(
    slot: str,
    pool: Sequence[Entry],
    semantic_context: Optional[JsonDict],
    generation_contract: Optional[JsonDict],
) -> List[Entry]:
    policy = (generation_contract or {}).get("soft_anchor_policy", {})
    if not policy or not policy.get("enabled"):
        return list(pool)
    constraints = policy.get("free_slot_constraints", {}) or {}
    constraint = constraints.get(slot)
    if not isinstance(constraint, dict):
        return list(pool)
    original_pool = list(pool)
    allow_ids = set(normalize_list(constraint.get("allow_pool")))
    deny_ids = set(normalize_list(constraint.get("deny_pool")))
    prefer_ids = set(normalize_list(constraint.get("prefer_ids")))
    fail_closed = bool(constraint.get("fail_closed"))
    constrained = [item for item in original_pool if str(item.get("id", "")) not in deny_ids]
    if allow_ids:
        allowed = [item for item in constrained if str(item.get("id", "")) in allow_ids]
        if allowed:
            constrained = allowed
    adjusted: List[Entry] = []
    boosted: List[str] = []
    for item in constrained:
        item_id = str(item.get("id", ""))
        if item_id not in prefer_ids:
            adjusted.append(item)
            continue
        copied = dict(item)
        copied["weight"] = round(item_base_weight(item) * soft_anchor_weight_multipliers(semantic_context)[1], 6)
        adjusted.append(copied)
        boosted.append(item_id)
    if len(adjusted) != len(original_pool) or boosted:
        record_generation_contract_event(
            generation_contract,
            "soft_free_slot_constraint_events",
            {
                "slot": slot,
                "reason": "soft_free_slot_constraints",
                "reason_code": "soft_free_slot_constraints",
                "before": len(original_pool),
                "after": len(adjusted),
                "allow_pool": sorted(allow_ids),
                "deny_pool": sorted(deny_ids),
                "preferred_ids": sorted(prefer_ids),
                "boosted_ids": sorted(set(boosted)),
                "fail_closed": fail_closed,
                "policy_schema_version": (semantic_context or {}).get("policy_schema_version"),
                "semantic_policy_hash": (semantic_context or {}).get("semantic_policy_hash"),
            },
        )
    return adjusted if adjusted or fail_closed else original_pool


def apply_soft_visual_guard(
    slot: str,
    pool: Sequence[Entry],
    semantic_context: Optional[JsonDict],
    generation_contract: Optional[JsonDict],
) -> List[Entry]:
    policy = (generation_contract or {}).get("soft_anchor_policy", {})
    guard = soft_visual_guard_for_slot(policy, slot)
    deny_ids: Set[str] = guard["deny_ids"]
    prefer_ids: Set[str] = guard["prefer_ids"]
    deny_facets: Set[str] = guard["deny_facets"]
    fail_closed = bool(guard.get("fail_closed"))
    if not deny_ids and not prefer_ids and not deny_facets:
        return list(pool)
    original_pool = list(pool)
    filtered = [
        item
        for item in original_pool
        if str(item.get("id", "")) not in deny_ids and not entry_matches_guard_facets(item, sorted(deny_facets))
    ]
    if filtered:
        pool = filtered
    elif fail_closed:
        pool = []
    adjusted: List[Entry] = []
    boosted: List[JsonDict] = []
    for item in pool:
        item_id = str(item.get("id", ""))
        if item_id not in prefer_ids:
            adjusted.append(item)
            continue
        copied = dict(item)
        base_weight = item_base_weight(item)
        copied["weight"] = round(base_weight * soft_anchor_weight_multipliers(semantic_context)[1], 6)
        adjusted.append(copied)
        boosted.append({"id": item_id, "base_weight": round(base_weight, 4), "adjusted_weight": copied["weight"]})
    if len(filtered) != len(original_pool) or boosted:
        record_generation_contract_event(
            generation_contract,
            "soft_visual_guard_events",
            {
                "slot": slot,
                "reason": "soft_visual_guard",
                "reason_code": "soft_visual_guard",
                "before": len(original_pool),
                "after": len(adjusted),
                "guard_ids": sorted(set(guard["guard_ids"])),
                "denied_ids": sorted(deny_ids),
                "preferred_ids": sorted(prefer_ids),
                "boosted_ids": sorted(item["id"] for item in boosted),
                "fail_closed": fail_closed,
                "policy_schema_version": (semantic_context or {}).get("policy_schema_version"),
                "semantic_policy_hash": (semantic_context or {}).get("semantic_policy_hash"),
            },
        )
    return adjusted


def soft_anchor_repeat_factor(
    slot: str,
    item_id: str,
    semantic_context: Optional[JsonDict],
    policy: Optional[JsonDict],
) -> tuple[float, JsonDict]:
    variant_group = soft_anchor_variant_group_for_slot(policy, slot)
    if not variant_group or not semantic_context:
        return 1.0, {"enabled": False, "reason": "not_variant_anchor"}
    config = (semantic_policy_from_source(semantic_context).get("soft_anchor_diversity", {}) or {})
    if config.get("enabled") is False:
        return 1.0, {"enabled": False, "reason": "policy_disabled"}
    batch_decay = semantic_policy_float(semantic_context, ("soft_anchor_diversity", "batch_repeat_decay"), 0.45)
    ledger_decay = semantic_policy_float(semantic_context, ("soft_anchor_diversity", "ledger_repeat_decay"), 0.5)
    batch_context = semantic_context.get("batch_context") or {}
    batch_count = int(((batch_context.get("counts", {}) or {}).get(slot, {}) or {}).get(item_id, 0))
    ledger = semantic_context.get("anchor_diversity_ledger") or {}
    ledger_counts = ledger.get(slot, {}) if isinstance(ledger, dict) else {}
    ledger_count = int((ledger_counts or {}).get(item_id, 0))
    factor = (batch_decay ** batch_count) * (ledger_decay ** ledger_count)
    factor = max(0.05, min(1.0, factor))
    return factor, {
        "enabled": bool(config.get("enabled", True)),
        "slot": slot,
        "id": item_id,
        "anchor_variant_group": variant_group,
        "diversity_penalty_applied": factor < 1.0,
        "repeat_penalty_source": "batch+ledger" if batch_count and ledger_count else ("batch" if batch_count else ("ledger" if ledger_count else "none")),
        "batch_count": batch_count,
        "ledger_count": ledger_count,
        "factor": round(factor, 4),
    }


def apply_soft_anchor_probability_floor(
    slot: str,
    candidates: Sequence[tuple[Entry, List[float], Optional[bool], float, float, JsonDict]],
    weights: List[float],
    context: Optional[JsonDict],
) -> tuple[List[float], Optional[JsonDict]]:
    policy = ((context or {}).get("generation_contract", {}) or {}).get("soft_anchor_policy", {})
    anchor_ids = soft_anchor_pool_for_slot(policy, slot)
    if not anchor_ids or not weights:
        return weights, None
    anchor_indexes = [index for index, row in enumerate(candidates) if str(row[0].get("id")) in anchor_ids]
    if not anchor_indexes:
        return weights, None
    variant_group = soft_anchor_variant_group_for_slot(policy, slot)
    adjusted = list(weights)
    summary: JsonDict = {"slot": slot, "mode": []}

    if variant_group and len(candidates) >= 2 and len(anchor_indexes) >= 2:
        total_before = sum(max(weight, 0.0) for weight in adjusted)
        top_before = max(adjusted[index] for index in anchor_indexes) / max(total_before, 0.000001)
        floor_ratio = semantic_policy_float(context, ("soft_anchor_diversity", "candidate_probability_floor"), 0.08)
        max_top = semantic_policy_float(context, ("soft_anchor_diversity", "max_single_candidate_probability"), 0.85)
        anchor_max = max(adjusted[index] for index in anchor_indexes)
        floor_weight = anchor_max * max(0.0, min(floor_ratio, 0.5))
        for index in anchor_indexes:
            adjusted[index] = max(adjusted[index], floor_weight)
        total_after = sum(max(weight, 0.0) for weight in adjusted)
        top_after = max(adjusted[index] for index in anchor_indexes) / max(total_after, 0.000001)
        if top_after > max_top and max_top > 0:
            top_weight = max(adjusted[index] for index in anchor_indexes)
            for index in anchor_indexes:
                if adjusted[index] == top_weight:
                    adjusted[index] = top_weight * max_top
                    break
            total_after = sum(max(weight, 0.0) for weight in adjusted)
            top_after = max(adjusted[index] for index in anchor_indexes) / max(total_after, 0.000001)
        summary["mode"].append("variant_floor")
        summary.update(
            {
                "anchor_variant_group": variant_group,
                "candidate_probability_floor": round(floor_ratio, 4),
                "max_single_candidate_probability": round(max_top, 4),
                "top1_probability_before": round(top_before, 4),
                "top1_probability_after": round(top_after, 4),
                "candidate_ids": [str(candidates[index][0].get("id")) for index in anchor_indexes],
            }
        )

    # Slot-level mass floor: guarantee the anchor pool a minimum share of the
    # selection probability even without a variant group or with one anchor.
    slot_floor = semantic_policy_float(context, ("soft_anchor_diversity", "anchor_slot_probability_floor"), 0.55)
    max_anchor_mass = semantic_policy_float(context, ("soft_anchor_diversity", "max_anchor_slot_probability"), 0.92)
    total = sum(max(weight, 0.0) for weight in adjusted)
    anchor_mass = sum(max(adjusted[index], 0.0) for index in anchor_indexes)
    non_anchor_mass = max(total - anchor_mass, 0.0)
    if total > 0 and non_anchor_mass > 0 and 0.0 < slot_floor < 1.0:
        anchor_share_before = anchor_mass / total
        target = min(max(slot_floor, 0.0), max(max_anchor_mass, slot_floor))
        if anchor_share_before < slot_floor and anchor_mass > 0:
            scale = (target * non_anchor_mass) / ((1.0 - target) * anchor_mass)
            for index in anchor_indexes:
                adjusted[index] = adjusted[index] * scale
            summary["mode"].append("slot_floor")
            summary["anchor_mass_before"] = round(anchor_share_before, 4)
            summary["anchor_mass_after"] = round(
                sum(max(adjusted[i], 0.0) for i in anchor_indexes)
                / max(sum(max(w, 0.0) for w in adjusted), 0.000001),
                4,
            )
        elif anchor_share_before > max_anchor_mass and max_anchor_mass > 0:
            scale = (max_anchor_mass * non_anchor_mass) / ((1.0 - max_anchor_mass) * anchor_mass)
            for index in anchor_indexes:
                adjusted[index] = adjusted[index] * scale
            summary["mode"].append("slot_cap")
            summary["anchor_mass_before"] = round(anchor_share_before, 4)
            summary["anchor_mass_after"] = round(
                sum(max(adjusted[i], 0.0) for i in anchor_indexes)
                / max(sum(max(w, 0.0) for w in adjusted), 0.000001),
                4,
            )

    if not summary["mode"]:
        return weights, None
    return adjusted, summary


def soft_visual_guard_status(policy: Optional[JsonDict], picked: Dict[str, Entry]) -> JsonDict:
    violations: List[JsonDict] = []
    if not policy or not policy.get("enabled"):
        return {"passed": True, "violations": []}
    for slot, entry in picked.items():
        guard = soft_visual_guard_for_slot(policy, slot)
        item_id = str(entry.get("id", ""))
        if item_id in guard["deny_ids"]:
            violations.append({"slot": slot, "id": item_id, "reason": "deny_ids", "guard_ids": sorted(set(guard["guard_ids"]))})
        if guard["deny_facets"] and entry_matches_guard_facets(entry, sorted(guard["deny_facets"])):
            violations.append({"slot": slot, "id": item_id, "reason": "deny_facets", "guard_ids": sorted(set(guard["guard_ids"]))})
    return {"passed": not violations, "violations": violations}


def render_priority_term_status(policy: Optional[JsonDict], result: JsonDict) -> JsonDict:
    groups = (policy or {}).get("render_priority_terms", []) or []
    if not groups:
        return {"passed": True, "groups": [], "missing": []}
    body = rendered_prompt_body_blob(result)
    rows: List[JsonDict] = []
    missing: List[JsonDict] = []
    for group in groups:
        terms = [str(term).lower() for term in normalize_list(group.get("terms")) if str(term).strip()]
        min_hits = max(1, int(group.get("min_hits", 1) or 1))
        hits = sorted({term for term in terms if term in body})
        tier = str(group.get("tier") or "required")
        if tier not in {"required", "support"}:
            tier = "required"
        row = {
            "id": group.get("id", ""),
            "group": group.get("group") or group.get("id", ""),
            "tier": tier,
            "terms": terms,
            "hits": hits,
            "min_hits": min_hits,
            "target_slots": normalize_list(group.get("target_slots")),
            "matched": len(hits) >= min_hits,
        }
        rows.append(row)
        if tier == "required" and not row["matched"]:
            missing.append(row)
    return {"passed": not missing, "groups": rows, "missing": missing}


def dual_read_term_status(policy: Optional[JsonDict], result: JsonDict) -> JsonDict:
    requirement = (policy or {}).get("dual_read_requirement", {}) or {}
    if not requirement or requirement.get("enabled") is False:
        return {"passed": True, "enabled": False}
    body = rendered_prompt_body_blob(result)
    role_terms = [str(term).lower() for term in normalize_list(requirement.get("role_terms"))]
    mixin_terms = [str(term).lower() for term in normalize_list(requirement.get("mixin_terms"))]
    role_hits = sorted({term for term in role_terms if term and term in body})
    mixin_hits = sorted({term for term in mixin_terms if term and term in body})
    min_role = max(1, int(requirement.get("min_role_hits", 1) or 1)) if role_terms else 0
    min_mixin = max(1, int(requirement.get("min_mixin_hits", 1) or 1)) if mixin_terms else 0
    passed = len(role_hits) >= min_role and len(mixin_hits) >= min_mixin
    return {
        "passed": passed,
        "enabled": True,
        "role_hits": role_hits,
        "mixin_hits": mixin_hits,
        "min_role_hits": min_role,
        "min_mixin_hits": min_mixin,
        "missing": {
            "role_terms": [] if len(role_hits) >= min_role else role_terms,
            "mixin_terms": [] if len(mixin_hits) >= min_mixin else mixin_terms,
        },
    }


def forced_required_subject_kinds(data: JsonDict, forced_choices: Dict[str, List[str]]) -> Set[str]:
    """If a forced slot item declares for_any, use it to steer random subject choice."""
    required: Set[str] = set()
    slots = data.get("slots", {})
    for slot, ids in forced_choices.items():
        if slot == "subject" or slot not in slots:
            continue
        id_set = set(ids)
        for item in slots[slot]:
            if item.get("id") in id_set and item.get("for_any"):
                allowed = set(item.get("for_any", []))
                required = allowed if not required else required & allowed
    return required


def family_preset_policy(context: Optional[JsonDict], family: str) -> JsonDict:
    policy = semantic_policy_family_config(context, family).get("preset_policy", {}) or {}
    return policy if isinstance(policy, dict) else {}


def family_preset_allow_ids(context: Optional[JsonDict], family: str) -> Set[str]:
    ids = set(normalize_list(family_preset_policy(context, family).get("allow_ids")))
    return ids


def family_preset_deny_ids(context: Optional[JsonDict], family: str) -> Set[str]:
    ids = set(normalize_list(family_preset_policy(context, family).get("deny_ids")))
    return ids


def family_preset_fallback_terms(context: Optional[JsonDict], family: str) -> List[str]:
    terms = normalize_list(family_preset_policy(context, family).get("fallback_terms"))
    return terms


def preset_has_family_policy_signal(preset: Entry, context: Optional[JsonDict], family: str) -> bool:
    preset_id = str(preset.get("id", ""))
    if preset_id in family_preset_deny_ids(context, family):
        return False
    if preset_id in family_preset_allow_ids(context, family):
        return True
    blob = " ".join(str(preset.get(key, "")) for key in ("id", "en", "ko", "embedding_text", "semantic_anchor")).lower()
    word_blob = re.sub(r"[_-]+", " ", blob)
    for term in family_preset_fallback_terms(context, family):
        token = str(term).lower().strip()
        if token and re.search(rf"(?<![a-z0-9]){re.escape(token)}(?![a-z0-9])", word_blob):
            return True
    return False


def preset_has_homebody_room_signal(preset: Entry, context: Optional[JsonDict] = None) -> bool:
    return preset_has_family_policy_signal(preset, context, "homebody_room")


def family_slot_signal_config(context: Optional[JsonDict], family: str, slot: str) -> JsonDict:
    signals = semantic_policy_family_config(context, family).get("slot_signals", {}) or {}
    if not isinstance(signals, dict):
        return {}
    slot_config = signals.get(slot, {}) or {}
    return slot_config if isinstance(slot_config, dict) else {}


def family_slot_signal_ids(context: Optional[JsonDict], family: str, slot: str, tier: str) -> Set[str]:
    ids = set(normalize_list(family_slot_signal_config(context, family, slot).get(tier)))
    return ids


def family_slot_has_explicit_signal_ids(context: Optional[JsonDict], family: str, slot: str) -> bool:
    config = family_slot_signal_config(context, family, slot)
    return bool(normalize_list(config.get("core")) or normalize_list(config.get("support")))


def family_slot_term_rules(context: Optional[JsonDict], family: str, slot: str, tier: str) -> Any:
    term_rules = family_slot_signal_config(context, family, slot).get("term_rules", {}) or {}
    if not isinstance(term_rules, dict):
        return []
    return term_rules.get(tier)


def family_slot_default_term_rules(context: Optional[JsonDict], family: str, tier: str) -> Any:
    defaults = semantic_policy_family_config(context, family).get("slot_signal_defaults", {}) or {}
    if not isinstance(defaults, dict):
        return []
    return defaults.get(tier)


def slot_signal_tier_summary(
    entry: Entry,
    family: str,
    slot: str,
    context: Optional[JsonDict] = None,
) -> tuple[Optional[str], Optional[JsonDict]]:
    entry_id = str(entry.get("id", ""))
    if entry_id in family_preset_deny_ids(context, family):
        return None, None
    for tier in ("core", "support"):
        if entry_id in family_slot_signal_ids(context, family, slot, tier):
            return tier, {
                "matched_via": f"semantic_policy.families.{family}.slot_signals.{slot}.{tier}",
                "matched_rule_id": entry_id,
                "matched_terms": [],
            }
    if family_slot_has_explicit_signal_ids(context, family, slot):
        return None, None
    for tier in ("core", "support"):
        matched_via = f"semantic_policy.families.{family}.slot_signals.{slot}.term_rules.{tier}"
        summary = first_policy_match(family_slot_term_rules(context, family, slot, tier), entry, matched_via)
        if summary:
            return tier, summary
    for tier in ("core", "support"):
        matched_via = f"semantic_policy.families.{family}.slot_signal_defaults.{tier}"
        summary = first_policy_match(family_slot_default_term_rules(context, family, tier), entry, matched_via)
        if summary:
            return tier, summary
    return None, None


def homebody_room_signal_tier(entry: Entry, slot: str, context: Optional[JsonDict] = None) -> Optional[str]:
    tier, _summary = slot_signal_tier_summary(entry, "homebody_room", slot, context)
    return tier


def entry_has_homebody_room_signal(entry: Entry, slot: str, context: Optional[JsonDict] = None) -> bool:
    return homebody_room_signal_tier(entry, slot, context) is not None


def homebody_concept_lock_blob(context: Optional[JsonDict]) -> str:
    contract = (context or {}).get("generation_contract", {}) or {}
    locks = contract.get("concept_locks", []) or []
    return " ".join(str(item) for item in locks if str(item).strip()).lower()


def family_concept_lock_promotion_rules(context: Optional[JsonDict], family: str, slot: str) -> List[JsonDict]:
    promotions = semantic_policy_family_config(context, family).get("concept_lock_promotions", {}) or {}
    configured = []
    if isinstance(promotions, dict):
        configured = [rule for rule in (promotions.get(slot, []) or []) if isinstance(rule, dict)]
    return configured


def family_concept_lock_promoted_ids(context: Optional[JsonDict], family: str, slot: str) -> Set[str]:
    blob = homebody_concept_lock_blob(context)
    if not blob:
        return set()
    promoted: Set[str] = set()
    for rule in family_concept_lock_promotion_rules(context, family, slot):
        terms = normalize_list(rule.get("terms"))
        ids = normalize_list(rule.get("ids"))
        if any(term.lower() in blob for term in terms):
            promoted.update(ids)
    return promoted


def homebody_concept_lock_promoted_ids(context: Optional[JsonDict], slot: str) -> Set[str]:
    return family_concept_lock_promoted_ids(context, "homebody_room", slot)


def family_redundancy_rules(context: Optional[JsonDict], family: str) -> List[JsonDict]:
    rules = semantic_policy_family_config(context, family).get("redundancy_rules", []) or []
    configured = [rule for rule in rules if isinstance(rule, dict)] if isinstance(rules, list) else []
    return configured


def apply_family_redundancy_rules(
    slot: str,
    pool: Sequence[Entry],
    context: Optional[JsonDict],
    picked: Dict[str, Entry],
    family: str,
) -> List[Entry]:
    if not context or family not in context_axis_families(context):
        return list(pool)
    redundant_ids: Set[str] = set()
    for rule in family_redundancy_rules(context, family):
        when_slot = str(rule.get("when_slot", ""))
        when_id = str(rule.get("when_id", ""))
        if str((picked.get(when_slot) or {}).get("id", "")) != when_id:
            continue
        suppress = rule.get("suppress", {}) or {}
        if isinstance(suppress, dict):
            redundant_ids.update(normalize_list(suppress.get(slot)))
    if not redundant_ids:
        return list(pool)
    filtered = [item for item in pool if str(item.get("id")) not in redundant_ids]
    if not filtered:
        return list(pool)
    record_intent_steering(
        context,
        {
            "slot": slot,
            "reason": f"{family}_{slot}_action_dedup",
            "reason_code": f"{family}_{slot}_action_dedup",
            "family": family,
            "before": len(pool),
            "after": len(filtered),
            "tier": "core",
            "signal_tier": "core",
            "matched_via": f"semantic_policy.families.{family}.redundancy_rules",
            "matched_terms": [],
            **policy_trace_fields(context, family),
        },
    )
    return filtered


def avoid_homebody_action_prop_redundancy(
    pool: Sequence[Entry],
    context: Optional[JsonDict],
    picked: Dict[str, Entry],
) -> List[Entry]:
    return apply_family_redundancy_rules("prop", pool, context, picked, "homebody_room")


def record_intent_steering(context: JsonDict, decision: JsonDict) -> None:
    steering = context.setdefault("intent_steering", {"mode": "off", "enabled": False, "families": [], "decisions": []})
    decisions = steering.setdefault("decisions", [])
    signature = json.dumps(decision, ensure_ascii=False, sort_keys=True)
    existing = {json.dumps(item, ensure_ascii=False, sort_keys=True) for item in decisions}
    if signature not in existing:
        decisions.append(decision)


def normalized_intent_hint_text(context: Optional[JsonDict]) -> str:
    if not context:
        return ""
    parts: List[str] = [str(context.get("intent") or "")]
    axes = (context.get("intent_axes") or {}).get("items", []) or []
    for axis in axes:
        parts.append(str(axis.get("text") or ""))
        parts.append(str(axis.get("embedding_text") or ""))
    text = " ".join(part for part in parts if part)
    return re.sub(r"[-_/]+", " ", text.lower())


def semantic_intent_hint_matches(rule: JsonDict, text: str) -> bool:
    any_terms = [re.sub(r"[-_/]+", " ", str(term).lower()).strip() for term in normalize_list(rule.get("any"))]
    all_terms = [re.sub(r"[-_/]+", " ", str(term).lower()).strip() for term in normalize_list(rule.get("all"))]
    not_any_terms = [re.sub(r"[-_/]+", " ", str(term).lower()).strip() for term in normalize_list(rule.get("not_any"))]
    any_terms = [term for term in any_terms if term]
    all_terms = [term for term in all_terms if term]
    not_any_terms = [term for term in not_any_terms if term]
    if not_any_terms and any(term in text for term in not_any_terms):
        return False
    if any_terms and not any(term in text for term in any_terms):
        return False
    if all_terms and not all(term in text for term in all_terms):
        return False
    return bool(any_terms or all_terms)


def semantic_intent_hint_slots(context: Optional[JsonDict], data: Optional[JsonDict] = None) -> List[str]:
    if not context or not intent_steering_enabled(context):
        return []
    text = normalized_intent_hint_text(context)
    if not text:
        return []
    known_slots = set((data or {}).get("slots", {}).keys()) if data else set(SEMANTIC_INTENT_SLOT_HINTS)
    slots: List[str] = []
    for slot, rules in SEMANTIC_INTENT_SLOT_HINTS.items():
        if slot not in known_slots:
            continue
        if any(semantic_intent_hint_matches(rule, text) for rule in rules):
            slots.append(slot)
    return slots


def semantic_intent_slot_has_active_hint(slot: str, context: Optional[JsonDict]) -> bool:
    if not context or not intent_steering_enabled(context):
        return False
    text = normalized_intent_hint_text(context)
    if not text:
        return False
    return any(semantic_intent_hint_matches(rule, text) for rule in SEMANTIC_INTENT_SLOT_HINTS.get(slot, []))


def apply_semantic_intent_slot_hints(
    slot: str,
    pool: Sequence[Entry],
    context: Optional[JsonDict],
) -> List[Entry]:
    if not context or not intent_steering_enabled(context):
        return list(pool)
    rules = SEMANTIC_INTENT_SLOT_HINTS.get(slot, [])
    if not rules:
        return list(pool)
    text = normalized_intent_hint_text(context)
    if not text:
        return list(pool)
    for rule in rules:
        if not semantic_intent_hint_matches(rule, text):
            continue
        allowed = set(normalize_list(rule.get("ids")))
        filtered = [item for item in pool if str(item.get("id")) in allowed]
        if not filtered:
            continue
        record_intent_steering(
            context,
            {
                "slot": slot,
                "reason": "explicit_intent_slot_hint",
                "reason_code": str(rule.get("id") or "explicit_intent_slot_hint"),
                "before": len(pool),
                "after": len(filtered),
                "allowed_ids": sorted(allowed),
            },
        )
        return filtered
    return list(pool)


def family_steering_slots(context: Optional[JsonDict], family: str) -> tuple[str, ...]:
    configured = normalize_list(semantic_policy_family_config(context, family).get("steering_slots"))
    return tuple(configured)


def ordered_steering_families(context: JsonDict) -> List[str]:
    active = context_axis_families(context)
    priority = normalize_list(semantic_policy_from_source(context).get("steering_priority"))
    ordered = [family for family in priority if family in active]
    ordered.extend(sorted(family for family in active if family not in set(priority)))
    return ordered


def steering_signal_tier_summary(
    entry: Entry,
    family: str,
    slot: str,
    context: JsonDict,
) -> tuple[Optional[str], Optional[JsonDict]]:
    tier, summary = slot_signal_tier_summary(entry, family, slot, context)
    if tier:
        return tier, summary
    if family_slot_has_explicit_signal_ids(context, family, slot):
        return None, None
    strength, summary = family_signal_strength_summary(entry, family, coherence_rules_from_source(context), slot, context)
    if strength == "strong":
        return "core", summary
    if strength == "ambient":
        return "support", summary
    return None, None


def steering_signal_tier(entry: Entry, family: str, slot: str, context: JsonDict) -> Optional[str]:
    tier, _summary = steering_signal_tier_summary(entry, family, slot, context)
    return tier


def family_steering_reason_code(family: str, slot: str, concept_lock: bool = False) -> str:
    if concept_lock:
        return f"{family}_{slot}_concept_lock"
    return f"{family}_{slot}"


def family_steering_reason(context: Optional[JsonDict], family: str, slot: str, concept_lock: bool = False) -> str:
    reason_code = family_steering_reason_code(family, slot, concept_lock)
    labels = semantic_policy_family_config(context, family).get("steering_reason_labels", {}) or {}
    if isinstance(labels, dict) and not concept_lock:
        return str(labels.get(slot) or reason_code)
    return reason_code


def policy_trace_fields(context: Optional[JsonDict], family: str) -> JsonDict:
    policy = semantic_policy_from_source(context)
    return {
        "policy_id": semantic_policy_id(context, family),
        "policy_schema_version": semantic_policy_schema_version(context),
        "semantic_policy_hash": (context or {}).get("semantic_policy_hash") or semantic_policy_digest(policy),
    }


def merge_match_summaries(summaries: Sequence[Optional[JsonDict]]) -> JsonDict:
    usable = [summary for summary in summaries if summary]
    if not usable:
        return {}
    matched_via = sorted({str(summary.get("matched_via")) for summary in usable if summary.get("matched_via")})
    matched_rule_ids = sorted({str(summary.get("matched_rule_id")) for summary in usable if summary.get("matched_rule_id")})
    matched_terms = sorted({str(term) for summary in usable for term in normalize_list(summary.get("matched_terms"))})
    result: JsonDict = {
        "matched_via": matched_via[0] if len(matched_via) == 1 else matched_via,
        "matched_rule_id": matched_rule_ids[0] if len(matched_rule_ids) == 1 else matched_rule_ids,
        "matched_terms": matched_terms,
    }
    return result


def apply_family_steering(
    slot: str,
    pool: Sequence[Entry],
    context: JsonDict,
    family: str,
) -> tuple[List[Entry], Optional[JsonDict]]:
    if slot not in family_steering_slots(context, family):
        return list(pool), None
    promoted_ids = family_concept_lock_promoted_ids(context, family, slot)
    signal_matches = [(item, *steering_signal_tier_summary(item, family, slot, context)) for item in pool]
    promoted = [item for item, tier, _summary in signal_matches if str(item.get("id")) in promoted_ids and tier == "core"]
    if promoted:
        summaries = [summary for item, tier, summary in signal_matches if item in promoted and tier == "core"]
        return promoted, {
            "slot": slot,
            "reason": family_steering_reason(context, family, slot, concept_lock=True),
            "reason_code": family_steering_reason_code(family, slot, concept_lock=True),
            "family": family,
            "before": len(pool),
            "after": len(promoted),
            "tier": "core",
            "signal_tier": "core",
            "promoted_by_concept_lock": True,
            "promoted_ids": sorted(promoted_ids),
            **policy_trace_fields(context, family),
            **merge_match_summaries(summaries),
        }

    core_steered = [item for item, tier, _summary in signal_matches if tier == "core"]
    support_steered = [item for item, tier, _summary in signal_matches if tier == "support"]
    if core_steered:
        tier = "core"
        steered = core_steered
    elif support_steered:
        tier = "support"
        steered = support_steered
    else:
        return list(pool), None

    summaries = [summary for item, item_tier, summary in signal_matches if item in steered and item_tier == tier]
    decision = {
        "slot": slot,
        "reason": family_steering_reason(context, family, slot),
        "reason_code": family_steering_reason_code(family, slot),
        "family": family,
        "before": len(pool),
        "after": len(steered),
        "tier": tier,
        "signal_tier": tier,
        **policy_trace_fields(context, family),
        **merge_match_summaries(summaries),
    }
    return steered, decision


def steer_semantic_candidate_pool(
    slot: str,
    pool: Sequence[Entry],
    context: Optional[JsonDict],
    anchor_ids: Optional[Set[str]] = None,
) -> List[Entry]:
    if not context or not intent_steering_enabled(context):
        return list(pool)
    for family in ordered_steering_families(context):
        steered, decision = apply_family_steering(slot, pool, context, family)
        if decision:
            # Soft-anchor pool members must stay reachable: steering narrows the
            # candidate set before anchor promotion/enforcement ever runs, so a
            # family signal can otherwise silently annihilate the entire pool.
            if anchor_ids:
                kept_ids = {str(item.get("id")) for item in steered}
                preserved = [
                    item
                    for item in pool
                    if str(item.get("id")) in anchor_ids and str(item.get("id")) not in kept_ids
                ]
                if preserved:
                    steered = list(steered) + preserved
                    decision["anchor_preserved"] = sorted(str(item.get("id")) for item in preserved)
                    decision["after"] = len(steered)
            record_intent_steering(context, decision)
            return steered
    return list(pool)


RULE_POLICY_WEIGHT_MULTIPLIERS = {
    "core": 2.25,
    "support": 1.45,
    "promoted_core": 3.0,
}


def rule_policy_context(data: JsonDict, generation_contract: Optional[JsonDict]) -> Optional[JsonDict]:
    if not generation_contract:
        return None
    locks = normalize_concept_locks(generation_contract.get("concept_locks", []))
    if not locks:
        return None
    axis_vectors: List[JsonDict] = []
    for lock in locks:
        families = axis_families_for_text(lock, data)
        if families:
            axis_vectors.append({"text": lock, "families": families, "source": "concept_lock"})
    family_set = sorted({family for axis in axis_vectors for family in axis.get("families", [])})
    if not family_set:
        return None
    policy = semantic_policy_from_source(data)
    return {
        "selection_mode": "rule",
        "intent": None,
        "intent_source": "concept_lock",
        "semantic_policy": policy,
        "policy_schema_version": semantic_policy_schema_version(data),
        "semantic_policy_hash": semantic_policy_digest(policy),
        "coherence_rules": data.get("coherence_rules", {}) or {},
        "semantic_metadata": data.get("semantic_metadata", {}) or {},
        "semantic_profile": default_semantic_profile("rule"),
        "axis_vectors": axis_vectors,
        "generation_contract": generation_contract,
        "intent_steering": {
            "mode": "rule_concept_lock",
            "enabled": True,
            "families": family_set,
            "decisions": [],
        },
    }


def rule_policy_candidate_bias(
    slot: str,
    item: Entry,
    context: JsonDict,
) -> Optional[JsonDict]:
    best: Optional[JsonDict] = None
    for family in ordered_steering_families(context):
        if slot not in family_steering_slots(context, family):
            continue
        tier, summary = steering_signal_tier_summary(item, family, slot, context)
        if not tier:
            continue
        promoted = tier == "core" and str(item.get("id")) in family_concept_lock_promoted_ids(context, family, slot)
        key = "promoted_core" if promoted else tier
        factor = semantic_policy_float(
            context, ("rule_policy_weights", key), float(RULE_POLICY_WEIGHT_MULTIPLIERS.get(key, 1.0))
        )
        rank = 3 if promoted else FAMILY_STRENGTH_RANK.get(tier, 0)
        candidate = {
            "family": family,
            "tier": tier,
            "signal_tier": tier,
            "factor": factor,
            "rank": rank,
            "promoted_by_concept_lock": promoted,
            **policy_trace_fields(context, family),
            **(summary or {}),
        }
        if best is None or int(candidate["rank"]) > int(best["rank"]) or factor > float(best["factor"]):
            best = candidate
    return best


def apply_rule_policy_bias(
    slot: str,
    pool: Sequence[Entry],
    data: JsonDict,
    generation_contract: Optional[JsonDict],
) -> List[Entry]:
    context = rule_policy_context(data, generation_contract)
    if not context:
        return list(pool)
    adjusted: List[Entry] = []
    boosted: List[JsonDict] = []
    for item in pool:
        bias = rule_policy_candidate_bias(slot, item, context)
        if not bias:
            adjusted.append(item)
            continue
        base_weight = item_base_weight(item)
        factor = float(bias.get("factor", 1.0))
        copied = dict(item)
        copied["weight"] = round(base_weight * factor, 6)
        adjusted.append(copied)
        boosted.append(
            {
                "id": item.get("id"),
                "family": bias.get("family"),
                "tier": bias.get("tier"),
                "signal_tier": bias.get("signal_tier"),
                "factor": round(factor, 4),
                "base_weight": round(base_weight, 4),
                "adjusted_weight": copied["weight"],
                "promoted_by_concept_lock": bool(bias.get("promoted_by_concept_lock")),
                "matched_via": bias.get("matched_via"),
                "matched_rule_id": bias.get("matched_rule_id"),
                "matched_terms": bias.get("matched_terms", []),
            }
        )
    if boosted:
        record_generation_contract_event(
            generation_contract,
            "rule_policy_bias",
            {
                "slot": slot,
                "reason": "rule_policy_concept_lock_bias",
                "reason_code": "rule_policy_concept_lock_bias",
                "before": len(pool),
                "after": len(adjusted),
                "active_families": sorted(context_axis_families(context)),
                "policy_schema_version": semantic_policy_schema_version(context),
                "semantic_policy_hash": context.get("semantic_policy_hash"),
                "boosted_count": len(boosted),
                "boosted": boosted,
            },
        )
    return adjusted


def apply_soft_anchor_bias(
    slot: str,
    pool: Sequence[Entry],
    semantic_context: Optional[JsonDict],
    generation_contract: Optional[JsonDict],
) -> List[Entry]:
    policy = (generation_contract or {}).get("soft_anchor_policy", {})
    ids = soft_anchor_pool_for_slot(policy, slot)
    critical_ids = soft_anchor_pool_for_slot(policy, slot, critical_only=True)
    atomic_ids = soft_anchor_atomic_pool_for_slot(policy, slot)
    primary_ids: Set[str] = set()
    for anchor in soft_anchor_entries_for_slot(policy, slot):
        if anchor.get("primary"):
            primary_ids.update(normalize_list(anchor.get("pool")) or normalize_list(anchor.get("ids")))
    if not ids:
        return list(pool)

    original_pool = list(pool)
    if atomic_ids:
        constrained = [item for item in original_pool if str(item.get("id")) in atomic_ids]
        record_generation_contract_event(
            generation_contract,
            "soft_anchor_pool_constraints",
            {
                "slot": slot,
                "reason": "atomic_scene_pool",
                "reason_code": "atomic_scene_pool",
                "before": len(original_pool),
                "after": len(constrained),
                "pool_ids": sorted(atomic_ids),
                "fail_closed": True,
                "policy_schema_version": (semantic_context or {}).get("policy_schema_version"),
                "semantic_policy_hash": (semantic_context or {}).get("semantic_policy_hash"),
            },
        )
        pool = constrained
    if critical_ids:
        critical_before = len(pool)
        constrained = [item for item in pool if str(item.get("id")) in critical_ids]
        if constrained:
            pool = constrained
            record_generation_contract_event(
                generation_contract,
                "soft_anchor_pool_constraints",
                {
                    "slot": slot,
                    "reason": "critical_soft_anchor_pool",
                    "reason_code": "critical_soft_anchor_pool",
                    "before": critical_before,
                    "after": len(constrained),
                    "pool_ids": sorted(critical_ids),
                    "policy_schema_version": (semantic_context or {}).get("policy_schema_version"),
                    "semantic_policy_hash": (semantic_context or {}).get("semantic_policy_hash"),
                },
            )

    adjusted: List[Entry] = []
    promoted: List[JsonDict] = []
    for item in pool:
        item_id = str(item.get("id"))
        if item_id not in ids:
            adjusted.append(item)
            continue
        base_weight = item_base_weight(item)
        base_multiplier, promoted_multiplier, critical_multiplier, primary_multiplier = soft_anchor_weight_multipliers(semantic_context)
        if item_id in critical_ids:
            factor = critical_multiplier
        elif item_id in primary_ids:
            factor = primary_multiplier
        else:
            factor = promoted_multiplier if item.get("anchor") else base_multiplier
        repeat_factor, repeat_summary = soft_anchor_repeat_factor(slot, item_id, semantic_context, policy)
        factor *= repeat_factor
        factor *= soft_anchor_pool_weight(policy, slot, item_id)
        # Semantic scoring damps base weights by base_power; compensate so the
        # nominal promotion factor survives into the final candidate weight.
        effective_factor = factor
        base_power = semantic_base_power(semantic_context)
        if semantic_context is not None and 0.0 < base_power < 1.0 and factor > 0:
            compensated = factor ** (1.0 / base_power)
            if math.isfinite(compensated):
                effective_factor = min(compensated, 1e12)
        copied = dict(item)
        copied["weight"] = round(base_weight * effective_factor, 6)
        adjusted.append(copied)
        promoted.append(
            {
                "id": item_id,
                "base_weight": round(base_weight, 4),
                "factor": round(factor, 4),
                "effective_factor": round(effective_factor, 4),
                "adjusted_weight": copied["weight"],
                "anchor_variant_group": soft_anchor_variant_group_for_slot(policy, slot),
                "diversity": repeat_summary,
            }
        )

    if promoted:
        record_generation_contract_event(
            generation_contract,
            "soft_anchor_promotions",
            {
                "slot": slot,
                "reason": "soft_anchor_candidate_promotion",
                "reason_code": "soft_anchor_candidate_promotion",
                "before": len(original_pool),
                "after": len(adjusted),
                "promoted_ids": sorted(item["id"] for item in promoted),
                "promoted": promoted,
                "anchor_variant_group": soft_anchor_variant_group_for_slot(policy, slot),
                "policy_schema_version": (semantic_context or {}).get("policy_schema_version"),
                "semantic_policy_hash": (semantic_context or {}).get("semantic_policy_hash"),
            },
        )
    return adjusted


def apply_role_scene_policy(
    slot: str,
    pool: Sequence[Entry],
    semantic_context: Optional[JsonDict],
    generation_contract: Optional[JsonDict],
) -> List[Entry]:
    if slot != "location":
        return list(pool)
    policy = normalize_role_scene_policy(((generation_contract or {}).get("soft_anchor_policy") or {}).get("role_scene_policy"))
    if not policy.get("enabled"):
        return list(pool)
    original_pool = list(pool)
    allowed = set(normalize_list(policy.get("allowed_locations")))
    preferred = set(normalize_list(policy.get("preferred_locations"))) or allowed
    forbidden = set(normalize_list(policy.get("forbidden_locations")))
    forbidden.update(normalize_list(policy.get("discouraged_generic_locations")))

    constrained = original_pool
    reason = ""
    if allowed:
        allowed_pool = [item for item in constrained if str(item.get("id")) in allowed]
        if allowed_pool:
            constrained = allowed_pool
            reason = "role_scene_allowed_pool"
    if forbidden and constrained:
        filtered = [item for item in constrained if str(item.get("id")) not in forbidden]
        if filtered and len(filtered) != len(constrained):
            constrained = filtered
            reason = reason or "role_scene_forbidden_removed"
    if allowed and len(constrained) > 1 and semantic_context:
        ledger = semantic_context.get("anchor_diversity_ledger") if isinstance(semantic_context.get("anchor_diversity_ledger"), dict) else {}
        ledger_counts = ledger.get(slot, {}) if isinstance(ledger.get(slot), dict) else {}
        batch_context = semantic_context.get("batch_context") if isinstance(semantic_context.get("batch_context"), dict) else {}
        batch_counts = ((batch_context.get("counts") or {}).get(slot) or {}) if isinstance(batch_context.get("counts"), dict) else {}

        def seen_count(item: Entry) -> int:
            item_id = str(item.get("id") or "")
            return int(ledger_counts.get(item_id, 0) or 0) + int(batch_counts.get(item_id, 0) or 0)

        min_count = min(seen_count(item) for item in constrained)
        least_seen = [item for item in constrained if seen_count(item) == min_count]
        if least_seen and len(least_seen) < len(constrained):
            constrained = least_seen
            reason = "role_scene_least_used_location"
    if preferred and constrained and not allowed:
        adjusted: List[Entry] = []
        for item in constrained:
            if str(item.get("id")) not in preferred:
                adjusted.append(item)
                continue
            copied = dict(item)
            copied["weight"] = round(item_base_weight(item) * 1.35, 6)
            adjusted.append(copied)
        constrained = adjusted
        reason = reason or "role_scene_preferred_boost"

    if constrained is not original_pool and len(constrained) != len(original_pool):
        record_generation_contract_event(
            generation_contract,
            "role_scene_policy",
            {
                "slot": slot,
                "reason": reason or "role_scene_policy_applied",
                "reason_code": reason or "role_scene_policy_applied",
                "scene_family": policy.get("scene_family"),
                "before": len(original_pool),
                "after": len(constrained),
                "allowed_locations": sorted(allowed),
                "preferred_locations": sorted(preferred),
                "forbidden_locations": sorted(forbidden),
                "remaining_ids": sorted(str(item.get("id")) for item in constrained),
                "policy_schema_version": (semantic_context or {}).get("policy_schema_version"),
                "semantic_policy_hash": (semantic_context or {}).get("semantic_policy_hash"),
            },
        )
    return constrained


def apply_species_family_policy(
    slot: str,
    pool: Sequence[Entry],
    semantic_context: Optional[JsonDict],
    generation_contract: Optional[JsonDict],
) -> List[Entry]:
    if slot not in {"species_marker", "texture", "anatomical_connection"}:
        return list(pool)
    policy = normalize_species_family_policy(
        ((generation_contract or {}).get("soft_anchor_policy") or {}).get("species_family_policy")
    )
    if not policy.get("enabled") or policy.get("hybrid_allowed"):
        return list(pool)
    allowed = set(normalize_list((policy.get("allowed") or {}).get(slot)))
    if not allowed:
        return list(pool)
    original_pool = list(pool)
    constrained = [item for item in original_pool if str(item.get("id")) in allowed]
    if not constrained:
        record_generation_contract_event(
            generation_contract,
            "species_family_policy",
            {
                "slot": slot,
                "reason": "species_family_allowed_pool_empty",
                "reason_code": "species_family_allowed_pool_empty",
                "family": policy.get("family"),
                "variant_id": policy.get("variant_id"),
                "allowed_ids": sorted(allowed),
                "before": len(original_pool),
                "after": len(original_pool),
            },
        )
        return original_pool
    if len(constrained) != len(original_pool):
        record_generation_contract_event(
            generation_contract,
            "species_family_policy",
            {
                "slot": slot,
                "reason": "species_family_allowed_pool",
                "reason_code": "species_family_allowed_pool",
                "family": policy.get("family"),
                "variant_id": policy.get("variant_id"),
                "allowed_ids": sorted(allowed),
                "before": len(original_pool),
                "after": len(constrained),
                "remaining_ids": sorted(str(item.get("id")) for item in constrained),
                "policy_schema_version": (semantic_context or {}).get("policy_schema_version"),
                "semantic_policy_hash": (semantic_context or {}).get("semantic_policy_hash"),
            },
        )
    return constrained


def semantic_steering_slots(context: Optional[JsonDict], data: JsonDict) -> List[str]:
    if not context or not intent_steering_enabled(context):
        return []
    available = set(data.get("slots", {}).keys())
    wanted: List[str] = []
    for family in ordered_steering_families(context):
        for slot in family_steering_slots(context, family):
            if slot in available and slot not in wanted:
                wanted.append(slot)
    return wanted


def quality_layer_primary_context_requirements(data: JsonDict, slot: str, item: Entry) -> Set[str]:
    requirements: Set[str] = set()
    item_tokens = {str(token) for token in entry_context_tokens(item)}
    item_blob = candidate_pack_entry_blob(item)
    for guard in candidate_pack_quality_layers(data).get("applicability_guards", []) or []:
        if not isinstance(guard, dict):
            continue
        included_slots = {str(value) for value in normalize_list(guard.get("slots"))}
        excluded_slots = {str(value) for value in normalize_list(guard.get("exclude_slots"))}
        if (included_slots and slot not in included_slots) or slot in excluded_slots:
            continue
        match_tags = {str(value) for value in normalize_list(guard.get("match_any_tags"))}
        match_terms = [
            str(value).lower()
            for value in normalize_list(guard.get("match_any_terms"))
            if str(value).strip()
        ]
        if match_tags or match_terms:
            tag_match = bool(match_tags & item_tokens)
            term_match = any(term in item_blob for term in match_terms)
            if not tag_match and not term_match:
                continue
        requirements.update(str(value) for value in normalize_list(guard.get("requires_primary_any_tags")))
    return requirements


def compatible_with_slot_context(
    slot: str,
    item: Entry,
    picked: Dict[str, Entry],
    source: Optional[JsonDict] = None,
) -> bool:
    context = picked_context_tokens(picked)
    scene_context = picked_scene_context_tokens(picked)
    primary_context = picked_core_context_tokens(picked)
    if picked.get("action"):
        primary_context |= entry_context_tokens(picked["action"])
    item_tokens = entry_context_tokens(item)
    item_id = str(item.get("id", ""))

    if values_as_set(item, "requires_any_tags", "requires_any") and not (
        values_as_set(item, "requires_any_tags", "requires_any") & context
    ):
        return False
    if values_as_set(item, "requires_primary_any_tags") and not (
        values_as_set(item, "requires_primary_any_tags") & primary_context
    ):
        return False
    if source is not None:
        quality_primary_requirements = quality_layer_primary_context_requirements(source, slot, item)
        if quality_primary_requirements and not (quality_primary_requirements & primary_context):
            return False
    if not values_as_set(item, "requires_all_tags", "requires_all").issubset(context):
        return False
    if values_as_set(item, "exclude_any_tags", "exclude_any") & context:
        return False

    if source is not None:
        if violates_declared_slot_context_rules(slot, item, picked, source):
            return False
        if slot_conflict_violations(slot, item, picked, source, "hard"):
            return False
        if not builtin_slot_context_rules_enabled(source):
            return True

    if slot in {"camera_type", "composition", "lens", "motion"}:
        if "surveillance" in item_tokens and not (context & {"surveillance", "cctv_frame", "dashcam_still", "bodycam_frame"}):
            return False
        if "vehicle" in item_tokens and not (context & {"vehicle", "automotive", "dashcam_still", "highway_dashcam"}):
            return False

    if slot == "lens" and context & {"phone", "front_facing_phone", "smartphone_camera", "selfie_camera_photo"}:
        if not (item_tokens & {"phone", "selfie", "social", "wide", "general"}):
            return False

    if slot in {"lighting", "light_type"}:
        if item_id == "headlights" and not (scene_context & {"street", "urban", "vehicle", "night", "surveillance"}):
            return False
        if item_id == "moonlight" and not (scene_context & {"nature", "night", "landscape", "wild"}):
            return False
        if item_id == "underwater_caustics" and not (scene_context & {"nature", "aquatic", "wild", "travel", "landscape"}):
            return False
        if item_id == "streetlamp" and not (scene_context & {"street", "urban", "night"}):
            return False
        if item_id == "lab_led" and not (context & {"science", "technology", "laboratory", "biolab", "data_center"}):
            return False
        if item_id == "monitor_glow" and not (context & {"technology", "gaming", "creator", "creator_room", "esports_room", "glass_office"}):
            return False
        if item_id in {"studio_strobe", "studio_flash", "softbox"} and not (
            context & {"studio", "commercial", "fashion", "beauty", "product", "portrait"}
        ):
            return False

    if slot == "light_shape":
        if item_id == "small_point_light" and not (context & {"flash", "night", "stage", "concert"}):
            return False
        if item_id in {"large_softbox_shape", "strip_light_shape", "gobo_pattern"} and not (
            context & {"studio", "commercial", "fashion", "beauty", "product", "portrait"}
        ):
            return False

    if slot == "body_framing" and "adult" in item_tokens and "adult" not in context:
        return False

    return True


def entry_matches_preset_domain_scope(item: Entry, preset: JsonDict, data: JsonDict) -> bool:
    """Restrict typed-pack entries to presets from their authored domain."""
    item_tokens = entry_tags(item) | entry_kinds(item)
    required_domains = {
        domain
        for marker, domain in INTENT_SCOPED_ENTRY_DOMAIN_TAGS.items()
        if marker in item_tokens
    }
    if not required_domains:
        return True
    return bool(required_domains & preset_domains(preset, data))


def compatible_with_picked(
    pool: Sequence[Entry],
    picked: Dict[str, Entry],
    forced: bool = False,
    slot: str = "",
    source: Optional[JsonDict] = None,
) -> List[Entry]:
    """
    Generic compatibility check.
    - for_any: keep item only if selected subject kind/tag intersects.
    - exclude_for_any: remove item if selected subject kind/tag intersects.
    - requires/excludes metadata and built-in slot guards compare against all picked tags.

    Forced choices bypass this check because user intent should win.
    """
    if forced:
        return list(pool)

    subject = picked.get("subject")
    if not subject:
        # Do not remove generic items when the subject is not chosen yet.
        return [item for item in pool if not item.get("for_any")]

    # ``for_any`` is documented as matching either subject kind or subject
    # tags. Subjects with an explicit ``kind`` previously lost all of their
    # more specific tags here (for example an animal/insect subject could not
    # activate an insect-only action).
    subject_kinds = entry_kinds(subject) | entry_tags(subject)
    compatible: List[Entry] = []
    for item in pool:
        allowed = set(item.get("for_any", []))
        excluded = set(item.get("exclude_for_any", []))
        if allowed and not (allowed & subject_kinds):
            continue
        if excluded and (excluded & subject_kinds):
            continue
        if slot and not compatible_with_slot_context(slot, item, picked, source):
            continue
        compatible.append(item)
    return compatible


def record_candidate_pool_trace(
    generation_contract: Optional[JsonDict],
    slot: str,
    pool: Sequence[Entry],
    selected: Optional[Entry],
    *,
    forced: bool,
    stage: str,
) -> None:
    if generation_contract is None:
        return
    weights = {
        str(item.get("id") or ""): candidate_pack_float(item.get("weight")) or 0.0
        for item in pool
        if str(item.get("id") or "")
    }
    generation_contract.setdefault("candidate_pool_trace", {})[slot] = {
        "eligible_ids": [str(item.get("id")) for item in pool if str(item.get("id") or "")],
        "weights": weights,
        "selected": str((selected or {}).get("id") or ""),
        "forced": forced,
        "stage": stage,
        "subject_category": generation_contract.get("subject_category", "generic"),
        "preset_domains": list(generation_contract.get("preset_domains", [])),
        "intent_constraints": dict(generation_contract.get("intent_constraints", {})),
    }


def choose_slot(
    slot: str,
    data: JsonDict,
    preset: JsonDict,
    rng: random.Random,
    picked: Dict[str, Entry],
    forced_choices: Optional[Dict[str, List[str]]] = None,
    semantic_context: Optional[JsonDict] = None,
    generation_contract: Optional[JsonDict] = None,
) -> Optional[Entry]:
    slots = data.get("slots", {})
    if slot not in slots:
        raise ValueError(f"Slot '{slot}' is referenced but not defined in JSON.")

    catalog_pool = list(slots[slot])
    filters = preset.get("filters", {}).get(slot)
    preset_required = slot in set(preset.get("required_slots", []))

    forced_ids = (forced_choices or {}).get(slot)
    forced = bool(forced_ids)
    if forced_ids:
        ids = set(forced_ids)
        forced_pool = [x for x in catalog_pool if x.get("id") in ids]
        if not forced_pool:
            valid = ", ".join(x.get("id", "?") for x in catalog_pool[:30])
            raise ValueError(f"Unknown id for slot '{slot}': {forced_ids}. Example valid ids: {valid}")
        full_pool = catalog_pool
        pool = forced_pool
    else:
        full_pool = [
            item
            for item in catalog_pool
            if entry_matches_preset_domain_scope(item, preset, data)
        ]
        pool = list(full_pool)

    soft_policy = (generation_contract or {}).get("soft_anchor_policy")
    critical_soft_anchor_slot = soft_anchor_critical_slot(soft_policy, slot)
    atomic_soft_anchor_ids = soft_anchor_atomic_pool_for_slot(soft_policy, slot)
    block_reason = slot_block_reason(data, slot, generation_contract, forced=forced or critical_soft_anchor_slot)
    if block_reason:
        record_generation_contract_event(
            generation_contract,
            "skipped_slots",
            {
                "slot": slot,
                "reason": block_reason,
                "subject_category": generation_contract.get("subject_category") if generation_contract else "generic",
                "preset_domains": generation_contract.get("preset_domains", []) if generation_contract else [],
            },
        )
        return None

    if not forced:
        before_contract = len(pool)
        pool = [item for item in pool if not entry_block_reason(item, slot, generation_contract, forced=False)]
        if before_contract > 0 and not pool:
            record_generation_contract_event(
                generation_contract,
                "fallback_blocked_slots",
                {"slot": slot, "reason": "entry_contract_empty", "rejected": before_contract},
            )
            return None

    # If a human-only forced modifier is given, steer subject choice toward human.
    if slot == "subject" and not forced:
        if generation_explicitly_excludes_people(semantic_context, generation_contract):
            non_human_pool = [
                item
                for item in pool
                if "human" not in entry_kinds(item) and "human" not in entry_tags(item)
            ]
            if non_human_pool:
                pool = non_human_pool
                record_generation_contract_event(
                    generation_contract,
                    "typed_intent_events",
                    {"slot": "subject", "reason": "explicit_no_people", "remaining": len(pool)},
                )
        required_kinds = forced_required_subject_kinds(data, forced_choices or {})
        if required_kinds and not generation_explicitly_excludes_people(semantic_context, generation_contract):
            steered = [x for x in pool if entry_kinds(x) & required_kinds]
            if steered:
                pool = steered
        request_categories = {
            str(item)
            for item in ((generation_contract or {}).get("intent_constraints", {}) or {}).get("subject_categories", [])
            if str(item) in VALID_SUBJECT_CATEGORIES
        }
        if request_categories:
            steered = [
                item
                for item in pool
                if subject_category({"subject": item}, data) in request_categories
            ]
            if steered:
                pool = steered
                record_generation_contract_event(
                    generation_contract,
                    "typed_intent_events",
                    {
                        "slot": "subject",
                        "reason": "typed_subject_category",
                        "categories": sorted(request_categories),
                        "remaining": len(pool),
                    },
                )

    if semantic_context and not forced:
        slot_anchor_ids = soft_anchor_pool_for_slot(
            (generation_contract or {}).get("soft_anchor_policy"), slot
        )
        pool = apply_semantic_intent_slot_hints(slot, pool, semantic_context)
        pool = steer_semantic_candidate_pool(slot, pool, semantic_context, anchor_ids=slot_anchor_ids)
        pool = apply_anchor_reachability_guard(slot, pool, data, generation_contract)
        pool = apply_soft_free_slot_constraints(slot, pool, semantic_context, generation_contract)
        pool = apply_soft_body_first_guard(slot, pool, semantic_context, generation_contract)
        pool = apply_soft_visual_guard(slot, pool, semantic_context, generation_contract)
        pool = apply_soft_anchor_bias(slot, pool, semantic_context, generation_contract)
        pool = apply_role_scene_policy(slot, pool, semantic_context, generation_contract)
        pool = apply_species_family_policy(slot, pool, semantic_context, generation_contract)
        if slot == "prop":
            pool = avoid_homebody_action_prop_redundancy(pool, semantic_context, picked)

    if semantic_context and not forced:
        before_hard = len(pool)
        anchor_ids = soft_anchor_pool_for_slot((generation_contract or {}).get("soft_anchor_policy"), slot)
        pool = [
            item
            for item in pool
            if compatible_with_semantic_hard_guards(
                item,
                preset,
                picked,
                slot,
                allow_adult_item=str(item.get("id", "")) in anchor_ids,
            )
        ]
        rejected = before_hard - len(pool)
        if rejected > 0:
            semantic_context["hard_rejected_count"] = int(semantic_context.get("hard_rejected_count", 0)) + rejected
            semantic_context.setdefault("hard_rejected", []).append({"slot": slot, "count": rejected})
        if before_hard > 0 and not pool:
            record_generation_contract_event(
                generation_contract,
                "fallback_blocked_slots",
                {"slot": slot, "reason": "semantic_hard_guard_empty", "rejected": rejected},
            )
            return None

    typed_record_filter_contract = bool(
        preset_domains(preset, data) & STRICT_TAG_FACET_SOURCE_DOMAINS
    )
    authored_hard_filter_contract = bool(
        not forced
        and (
            typed_record_filter_contract
            or (
                semantic_context
                and semantic_context.get("filter_strictness") == "hard"
            )
        )
    )
    if authored_hard_filter_contract:
        # Semantic steering may prune every authored filter id before this
        # stage. A hard contract must recover from the original domain-scoped
        # pool, and every later fallback must stay inside that recovered set.
        filtered = apply_filter(pool, filters)
        if not filtered:
            filtered = apply_filter(full_pool, filters)
        if filtered:
            pool = filtered
            full_pool = list(filtered)
    elif not semantic_context or forced:
        filtered = apply_filter(pool, filters)
        if filtered:
            pool = filtered

    if not forced:
        pending_forced = pending_forced_conflict_entries(data, forced_choices, picked)
        if pending_forced:
            ahead_filtered = [
                item for item in pool
                if not conflicts_with_all_pending_forced(slot, item, pending_forced, data)
            ]
            if ahead_filtered:
                pool = ahead_filtered

    # Compatibility is generic, but action keeps the older generous fallback.
    compatible = compatible_with_picked(pool, picked, forced=forced, slot=slot, source=data)
    if compatible:
        pool = compatible
    elif semantic_intent_slot_has_active_hint(slot, semantic_context):
        relaxed = [
            item
            for item in pool
            if not violates_declared_slot_context_rules(slot, item, picked, data)
            and not slot_conflict_violations(slot, item, picked, data, "hard")
        ]
        if relaxed:
            record_generation_contract_event(
                generation_contract,
                "semantic_intent_hint_relaxed_compatibility",
                {
                    "slot": slot,
                    "reason": "explicit_intent_hint_relaxed_to_declared_hard_rules",
                    "reason_code": "explicit_intent_hint_relaxed_to_declared_hard_rules",
                    "before": len(pool),
                    "after": len(relaxed),
                },
            )
            pool = relaxed
    elif slot == "action" and not atomic_soft_anchor_ids:
        fallback = compatible_with_picked(full_pool, picked, forced=False, slot=slot, source=data)
        pool = fallback or pool or full_pool
    elif forced:
        # Forced choices should already be in pool; allow them even if odd.
        pass
    elif not preset_required:
        record_generation_contract_event(
            generation_contract,
            "fallback_blocked_slots",
            {"slot": slot, "reason": "optional_context_incompatible"},
        )
        return None
    else:
        # Required slots with explicit compatibility metadata may still be skipped.
        if any(
            item.get("for_any")
            or item.get("exclude_for_any")
            or item.get("requires_any_tags")
            or item.get("requires_all_tags")
            or item.get("exclude_any_tags")
            for item in full_pool
        ):
            return None

    # If preset filters are too narrow, fall back to the full slot.
    if not pool:
        if forced:
            return None
        if atomic_soft_anchor_ids:
            record_generation_contract_event(
                generation_contract,
                "fallback_blocked_slots",
                {
                    "slot": slot,
                    "reason": "atomic_scene_pool_empty",
                    "pool_ids": sorted(atomic_soft_anchor_ids),
                    "fail_closed": True,
                },
            )
            return None
        if not preset_required:
            record_generation_contract_event(
                generation_contract,
                "fallback_blocked_slots",
                {"slot": slot, "reason": "optional_empty_candidate_pool"},
            )
            return None
        record_generation_contract_event(
            generation_contract,
            "fallback_blocked_slots",
            {"slot": slot, "reason": "empty_candidate_pool"},
        )
        pool = compatible_with_picked(full_pool, picked, forced=False, slot=slot, source=data) or full_pool

    if not forced:
        pool = apply_slot_conflict_soft_penalties(slot, pool, picked, data, generation_contract)

    if not semantic_context and not forced:
        pool = apply_rule_policy_bias(slot, pool, data, generation_contract)
        pool = apply_rule_request_relevance_bias(slot, pool, data, generation_contract)

    if not forced:
        pool = apply_selection_balance_bias(pool, data, semantic_context, generation_contract)

    selected = None
    if not semantic_context and not forced:
        selected = rule_request_relevance_choice(slot, pool, data, generation_contract)
    if selected is None:
        selected = semantic_weighted_choice(
            pool,
            rng,
            slot,
            preset,
            semantic_context,
            forced=forced,
            slot_filter=filters,
            picked=picked,
        )
    record_candidate_pool_trace(
        generation_contract,
        slot,
        pool,
        selected,
        forced=forced,
        stage="initial_selection",
    )
    return selected


def soft_anchor_repair_candidates(
    data: JsonDict,
    preset: JsonDict,
    slot: str,
    ids: Set[str],
    picked: Dict[str, Entry],
    generation_contract: Optional[JsonDict],
    allow_current_in_pool: bool = False,
) -> List[Entry]:
    if slot not in data.get("slots", {}):
        return []
    if slot_block_reason(
        data,
        slot,
        generation_contract,
        forced=soft_anchor_critical_slot((generation_contract or {}).get("soft_anchor_policy"), slot),
    ):
        return []
    current = picked.get(slot)
    candidate_picked = dict(picked)
    candidate_picked.pop(slot, None)
    candidates = [item for item in data["slots"][slot] if str(item.get("id")) in ids]
    candidates = [
        item
        for item in candidates
        if entry_matches_preset_domain_scope(item, preset, data)
    ]
    candidates = [item for item in candidates if not entry_block_reason(item, slot, generation_contract, forced=False)]
    candidates = [
        item
        for item in candidates
        if compatible_with_semantic_hard_guards(
            item,
            preset,
            candidate_picked,
            slot,
            allow_adult_item=str(item.get("id", "")) in ids,
        )
    ]
    tier1 = compatible_with_picked(candidates, candidate_picked, forced=False, slot=slot, source=data)
    if tier1:
        candidates = tier1
    else:
        # Relaxed tier: drop tag-requirement heuristics but keep declared hard
        # rules so repair can never introduce a hard slot contradiction.
        tier2 = [
            item
            for item in candidates
            if not violates_declared_slot_context_rules(slot, item, candidate_picked, data)
            and not slot_conflict_violations(slot, item, candidate_picked, data, "hard")
        ]
        if tier2 and tier2 != candidates:
            record_generation_contract_event(
                generation_contract,
                "soft_anchor_repair_relaxed",
                {
                    "slot": slot,
                    "reason": "repair_relaxed_to_declared_hard_rules",
                    "reason_code": "repair_relaxed_to_declared_hard_rules",
                    "candidate_ids": sorted(str(item.get("id")) for item in tier2),
                },
            )
        candidates = tier2
    if current and str(current.get("id")) in ids:
        if not allow_current_in_pool:
            return []
        current_id = str(current.get("id"))
        candidates = [item for item in candidates if str(item.get("id")) != current_id]
    return candidates


def soft_free_slot_constraint_violations(policy: Optional[JsonDict], picked: Dict[str, Entry]) -> List[JsonDict]:
    if not policy or not policy.get("enabled"):
        return []
    violations: List[JsonDict] = []
    for slot, constraint in (policy.get("free_slot_constraints", {}) or {}).items():
        if not isinstance(constraint, dict):
            continue
        entry = picked.get(slot)
        if not entry:
            continue
        entry_id = str(entry.get("id") or "")
        allow_ids = set(normalize_list(constraint.get("allow_pool")))
        deny_ids = set(normalize_list(constraint.get("deny_pool")))
        if entry_id in deny_ids:
            violations.append({"slot": slot, "id": entry_id, "reason": "deny_pool"})
        if allow_ids and entry_id not in allow_ids:
            violations.append({"slot": slot, "id": entry_id, "reason": "outside_allow_pool"})
    return violations


def soft_body_first_survivors(
    policy: Optional[JsonDict],
    picked: Dict[str, Entry],
    semantic_context: Optional[JsonDict],
) -> List[JsonDict]:
    if not policy or not policy.get("enabled") or not semantic_context:
        return []
    guard_policy = (semantic_policy_from_source(semantic_context).get("soft_body_first_guard", {}) or {})
    guard_slots = normalize_list(guard_policy.get("slots"))
    legacy_guard_slot = str(guard_policy.get("slot") or "").strip()
    if legacy_guard_slot and legacy_guard_slot not in guard_slots:
        guard_slots.append(legacy_guard_slot)
    if not guard_slots:
        guard_slots = ["body_framing"]
    demote_facets = normalize_list(guard_policy.get("demote_facets")) or ["soft_body_role:body_emphasis"]
    protected_ids = soft_anchor_all_ids(policy)
    survivors: List[JsonDict] = []
    for guard_slot in guard_slots:
        entry = picked.get(guard_slot)
        if not entry or str(entry.get("id") or "") in protected_ids:
            continue
        if entry_matches_guard_facets(entry, demote_facets):
            survivors.append({"slot": guard_slot, "id": entry.get("id"), "reason": "body_emphasis_survived"})
    return survivors


def soft_repair_candidate_ids_for_slot(policy: JsonDict, slot: str) -> Set[str]:
    ids = set(soft_anchor_pool_for_slot(policy, slot))
    constraint = (policy.get("free_slot_constraints", {}) or {}).get(slot)
    if isinstance(constraint, dict):
        ids.update(normalize_list(constraint.get("prefer_ids")))
        ids.update(normalize_list(constraint.get("allow_pool")))
    guard = soft_visual_guard_for_slot(policy, slot)
    ids.update(guard.get("prefer_ids", set()))
    return {item for item in ids if item}


def soft_post_render_repair_triggers(
    policy: Optional[JsonDict],
    picked: Dict[str, Entry],
    result: JsonDict,
    semantic_context: Optional[JsonDict],
) -> List[JsonDict]:
    if not policy or not policy.get("enabled"):
        return []
    repair_policy = policy.get("soft_repair_policy", {}) or {}
    enabled_checks = set(normalize_list(repair_policy.get("trigger_checks")))
    triggers: List[JsonDict] = []
    priority_status = render_priority_term_status(policy, result)
    if "required_render_priority_missing" in enabled_checks:
        for group in priority_status.get("missing", []) or []:
            target_slots = normalize_list(group.get("target_slots"))
            if not target_slots:
                group_name = str(group.get("group") or group.get("id") or "")
                for anchor in policy.get("anchors", []) or []:
                    if group_name and group_name in normalize_list(anchor.get("groups")):
                        slot = str(anchor.get("slot") or "")
                        if slot and slot not in target_slots:
                            target_slots.append(slot)
            triggers.append(
                {
                    "reason": "required_render_priority_missing",
                    "group": group.get("group") or group.get("id"),
                    "id": group.get("id"),
                    "target_slots": target_slots,
                    "missing_terms": group.get("terms", []),
                }
            )
    dual_status = dual_read_term_status(policy, result)
    if "dual_read_missing" in enabled_checks and not dual_status.get("passed"):
        triggers.append(
            {
                "reason": "dual_read_missing",
                "target_slots": ["subject_framing", "composition", "action", "prop"],
                "missing": dual_status.get("missing", {}),
            }
        )
    if "body_first_survivor" in enabled_checks:
        survivors = soft_body_first_survivors(policy, picked, semantic_context)
        if survivors:
            triggers.append(
                {
                    "reason": "body_first_survivor",
                    "target_slots": ["subject_framing", "composition", "action", "prop", "body_framing"],
                    "survivors": survivors,
                }
            )
    if "free_slot_constraint_violation" in enabled_checks:
        violations = soft_free_slot_constraint_violations(policy, picked)
        if violations:
            triggers.append(
                {
                    "reason": "free_slot_constraint_violation",
                    "target_slots": [str(item.get("slot")) for item in violations if item.get("slot")],
                    "violations": violations,
                }
            )
    return triggers


def apply_soft_post_render_repair(
    data: JsonDict,
    preset: JsonDict,
    rng: random.Random,
    picked: Dict[str, Entry],
    result: JsonDict,
    forced_choices: Optional[Dict[str, List[str]]] = None,
    semantic_context: Optional[JsonDict] = None,
    generation_contract: Optional[JsonDict] = None,
) -> bool:
    if not generation_contract:
        return False
    policy = generation_contract.get("soft_anchor_policy", {})
    if not policy or not policy.get("enabled"):
        return False
    repair_policy = policy.get("soft_repair_policy", {}) or normalize_soft_repair_policy({})
    if repair_policy.get("enabled") is False:
        return False
    max_attempts = int(repair_policy.get("max_attempts", 2) or 0)
    if max_attempts <= 0:
        return False
    triggers = soft_post_render_repair_triggers(policy, picked, result, semantic_context)
    if not triggers:
        current = generation_contract.get("soft_anchor_repair", {}) or {}
        if current.get("status") in {"not_needed", "not_evaluated"}:
            current.update({"post_render_status": "not_needed", "post_render_triggers": []})
            generation_contract["soft_anchor_repair"] = current
        return False

    forced_slots = set((forced_choices or {}).keys())
    default_targets = normalize_list(repair_policy.get("target_slots")) or ["subject_framing", "composition", "action", "prop", "body_framing"]
    ordered_slots: List[str] = []
    for trigger in triggers:
        for slot in normalize_list(trigger.get("target_slots")):
            if slot and slot not in ordered_slots:
                ordered_slots.append(slot)
    for slot in default_targets:
        if slot and slot not in ordered_slots:
            ordered_slots.append(slot)

    attempts: List[JsonDict] = []
    changed = False
    for slot in ordered_slots:
        if len(attempts) >= max_attempts:
            break
        if slot in forced_slots or slot not in data.get("slots", {}):
            attempts.append({"slot": slot, "status": "skipped_forced_or_unknown"})
            continue
        if slot == "costume_style" and soft_anchor_critical_slot(policy, slot):
            attempts.append({"slot": slot, "status": "skipped_role_critical_costume"})
            continue
        ids = soft_repair_candidate_ids_for_slot(policy, slot)
        if ids:
            # Post-render repair may need to swap one pool member for another
            # (the current pick can be in-pool yet fail render-term checks).
            candidates = soft_anchor_repair_candidates(
                data, preset, slot, ids, picked, generation_contract, allow_current_in_pool=True
            )
        else:
            candidate_picked = dict(picked)
            candidate_picked.pop(slot, None)
            candidates = [item for item in data.get("slots", {}).get(slot, []) if not entry_block_reason(item, slot, generation_contract, forced=False)]
            candidates = compatible_with_picked(candidates, candidate_picked, forced=False, slot=slot, source=data) or candidates
        if not candidates:
            attempts.append({"slot": slot, "status": "blocked", "candidate_ids": sorted(ids)})
            continue
        candidates = apply_soft_free_slot_constraints(slot, candidates, semantic_context, generation_contract)
        candidates = apply_soft_body_first_guard(slot, candidates, semantic_context, generation_contract)
        candidates = apply_soft_visual_guard(slot, candidates, semantic_context, generation_contract)
        candidates = apply_soft_anchor_bias(slot, candidates, semantic_context, generation_contract)
        candidates = apply_role_scene_policy(slot, candidates, semantic_context, generation_contract)
        candidates = apply_species_family_policy(slot, candidates, semantic_context, generation_contract)
        before_id = str((picked.get(slot) or {}).get("id") or "")
        selection_candidates = candidates
        selected_entry = semantic_weighted_choice(
            selection_candidates,
            rng,
            slot,
            preset,
            semantic_context,
            forced=False,
            slot_filter=preset.get("filters", {}).get(slot),
            picked={key: value for key, value in picked.items() if key != slot},
        )
        after_id = str(selected_entry.get("id") or "")
        if after_id == before_id and len(candidates) > 1:
            alternatives = [item for item in candidates if str(item.get("id") or "") != before_id]
            if alternatives:
                selection_candidates = alternatives
                selected_entry = semantic_weighted_choice(
                    selection_candidates,
                    rng,
                    slot,
                    preset,
                    semantic_context,
                    forced=False,
                    slot_filter=preset.get("filters", {}).get(slot),
                    picked={key: value for key, value in picked.items() if key != slot},
                )
                after_id = str(selected_entry.get("id") or "")
        record_candidate_pool_trace(
            generation_contract,
            slot,
            selection_candidates,
            selected_entry,
            forced=False,
            stage="soft_post_render_repair",
        )
        picked[slot] = selected_entry
        changed = changed or after_id != before_id
        attempts.append(
            {
                "slot": slot,
                "status": "reselected" if after_id != before_id else "kept",
                "before": before_id,
                "after": after_id,
                "candidate_ids": sorted(ids) if ids else [str(item.get("id")) for item in candidates],
            }
        )

    current = generation_contract.get("soft_anchor_repair", {}) or {}
    current.update(
        {
            "post_render_status": "repaired" if changed else "failed",
            "post_render_triggers": triggers,
            "repair_trigger": [trigger.get("reason") for trigger in triggers],
            "repair_target_slots": ordered_slots,
            "post_render_attempts": attempts,
            "repair_result": "post_render_reselected" if changed else "post_render_unresolved",
            "unresolved_required_groups": [
                trigger.get("group")
                for trigger in triggers
                if trigger.get("reason") == "required_render_priority_missing"
            ],
        }
    )
    generation_contract["soft_anchor_repair"] = current
    if changed:
        refresh_generation_contract(generation_contract, data, preset, picked, forced_choices)
    return changed


def apply_soft_anchor_repair(
    data: JsonDict,
    preset: JsonDict,
    rng: random.Random,
    picked: Dict[str, Entry],
    forced_choices: Optional[Dict[str, List[str]]] = None,
    semantic_context: Optional[JsonDict] = None,
    generation_contract: Optional[JsonDict] = None,
) -> None:
    if not generation_contract:
        return
    policy = generation_contract.get("soft_anchor_policy", {})
    if not policy or not policy.get("enabled"):
        generation_contract["soft_anchor_repair"] = {"status": "not_applicable", "repair_attempts": []}
        return
    forced_slots = set((forced_choices or {}).keys())
    min_anchors = int(policy.get("min_anchors", 0))
    required_anchor_count = soft_anchor_required_count(policy)
    status = soft_anchor_match_status(policy, picked)
    attempts: List[JsonDict] = []
    if status.get("passed"):
        generation_contract["soft_anchor_repair"] = {
            "status": "not_needed",
            "selected_anchor_count": status.get("selected_anchor_count", 0),
            "min_anchors": min_anchors,
            "required_anchor_count": required_anchor_count,
            "repair_attempts": attempts,
            "repair_result": "already_satisfied",
            "match_status": status,
            "policy_schema_version": (semantic_context or {}).get("policy_schema_version"),
            "semantic_policy_hash": (semantic_context or {}).get("semantic_policy_hash"),
        }
        return

    ordered_slots: List[str] = []
    for slot in status.get("critical_missing", []) or []:
        if slot not in ordered_slots:
            ordered_slots.append(slot)
    # Primary anchors repair right after critical ones.
    for anchor in policy.get("anchors", []) or []:
        slot = str(anchor.get("slot") or "")
        if anchor.get("primary") and slot and slot not in ordered_slots:
            ordered_slots.append(slot)
    for miss in status.get("group_floor_misses", []) or []:
        group = str(miss.get("group") or "")
        for anchor in policy.get("anchors", []) or []:
            slot = str(anchor.get("slot") or "")
            if group in normalize_list(anchor.get("groups")) and slot not in ordered_slots:
                ordered_slots.append(slot)
    for miss in status.get("source_floor_misses", []) or []:
        source = str(miss.get("source") or "")
        for anchor in policy.get("anchors", []) or []:
            slot = str(anchor.get("slot") or "")
            if source in soft_anchor_sources(anchor.get("source")) and slot not in ordered_slots:
                ordered_slots.append(slot)
    for slot in soft_anchor_slots(policy):
        if slot not in ordered_slots:
            ordered_slots.append(slot)

    for slot in ordered_slots:
        status = soft_anchor_match_status(policy, picked)
        if status.get("passed"):
            break
        if slot in forced_slots:
            attempts.append({"slot": slot, "status": "skipped_forced_slot"})
            continue
        if slot in status.get("selected_anchor_slots", []) and slot not in status.get("critical_missing", []):
            continue
        ids = soft_anchor_pool_for_slot(policy, slot, critical_only=slot in (status.get("critical_missing", []) or []))
        if not ids:
            ids = soft_anchor_pool_for_slot(policy, slot)
        candidates = soft_anchor_repair_candidates(data, preset, slot, ids, picked, generation_contract)
        if not candidates:
            attempts.append({"slot": slot, "status": "blocked", "candidate_ids": sorted(ids)})
            continue
        candidates = apply_soft_free_slot_constraints(slot, candidates, semantic_context, generation_contract)
        candidates = apply_soft_body_first_guard(slot, candidates, semantic_context, generation_contract)
        candidates = apply_soft_visual_guard(slot, candidates, semantic_context, generation_contract)
        biased_candidates = apply_soft_anchor_bias(slot, candidates, semantic_context, generation_contract)
        selected_entry = semantic_weighted_choice(
            biased_candidates,
            rng,
            slot,
            preset,
            semantic_context,
            forced=False,
            slot_filter=preset.get("filters", {}).get(slot),
            picked={key: value for key, value in picked.items() if key != slot},
        )
        record_candidate_pool_trace(
            generation_contract,
            slot,
            biased_candidates,
            selected_entry,
            forced=False,
            stage="soft_anchor_repair",
        )
        picked[slot] = selected_entry
        status = soft_anchor_match_status(policy, picked)
        attempts.append(
            {
                "slot": slot,
                "status": "reselected",
                "selected": selected_entry.get("id"),
                "candidate_ids": sorted(ids),
                "match_status": status,
            }
        )

    status = soft_anchor_match_status(policy, picked)
    generation_contract["soft_anchor_repair"] = {
        "status": "repaired" if status.get("passed") else "failed",
        "selected_anchor_count": status.get("selected_anchor_count", 0),
        "min_anchors": min_anchors,
        "required_anchor_count": required_anchor_count,
        "repair_attempts": attempts,
        "repair_result": "satisfied" if status.get("passed") else "insufficient_anchors",
        "match_status": status,
        "policy_schema_version": (semantic_context or {}).get("policy_schema_version"),
        "semantic_policy_hash": (semantic_context or {}).get("semantic_policy_hash"),
    }
    refresh_generation_contract(generation_contract, data, preset, picked, forced_choices)


# -----------------------------------------------------------------------------
# Rendering
# -----------------------------------------------------------------------------

DETAIL_REINFORCEMENT_SLOTS = (
    "camera_type",
    "camera_direction",
    "shot_scale",
    "focus",
    "motion",
    "light_direction",
    "light_type",
    "light_intensity",
    "light_shape",
    "texture",
    "format",
)


def reinforce_detail_slots(
    data: JsonDict,
    preset: JsonDict,
    rng: random.Random,
    picked: Dict[str, Entry],
    forced_choices: Optional[Dict[str, List[str]]] = None,
    semantic_context: Optional[JsonDict] = None,
    generation_contract: Optional[JsonDict] = None,
) -> None:
    """Add compatible high-signal slots so detailed prompts are consistently specific."""
    minimum_slots = {
        "lighting": 3,
        "camera": 4,
        "finish": 2,
    }
    slot_groups = {
        "lighting": ("lighting", "light_direction", "light_type", "light_intensity", "light_shape"),
        "camera": ("camera_type", "camera_direction", "composition", "shot_scale", "platform_framing", "lens", "focus", "motion", "body_framing"),
        "finish": ("texture", "format", "quality"),
    }

    def group_count(group: str) -> int:
        return sum(1 for slot in slot_groups[group] if slot in picked)

    for slot in DETAIL_REINFORCEMENT_SLOTS:
        if slot in picked:
            continue
        if slot in slot_groups["lighting"] and group_count("lighting") >= minimum_slots["lighting"]:
            continue
        if slot in slot_groups["camera"] and group_count("camera") >= minimum_slots["camera"]:
            continue
        if slot in slot_groups["finish"] and group_count("finish") >= minimum_slots["finish"]:
            continue

        entry = choose_slot(slot, data, preset, rng, picked, forced_choices, semantic_context, generation_contract)
        if entry is not None:
            picked[slot] = entry
            refresh_generation_contract(generation_contract, data, preset, picked, forced_choices)


def build_fields(picked: Dict[str, Entry], lang: str, data: Optional[JsonDict] = None) -> Dict[str, str]:
    values = {slot: localize(entry, lang) for slot, entry in picked.items()}

    subject = values.get("subject", "")
    action = values.get("action", "")
    hair = values.get("hair_style", "")
    hair_color = values.get("hair_color", "")
    makeup = values.get("makeup_style", "")
    expression = values.get("expression", "")
    facial_hair = values.get("facial_hair", "")
    accessory = values.get("wearable_accessory", "")
    wardrobe = values.get("wardrobe_style", "")
    footwear = values.get("footwear", "")
    silhouette = values.get("silhouette_proportion", "")
    body_pose = values.get("body_pose", "")
    costume = values.get("costume_style", "")

    if lang == "ko":
        subject_mods = [values[s] for s in ("person_origin", "appearance_type") if values.get(s)]
        if hair:
            subject_mods.append(hair)
        if hair_color:
            subject_mods.append(hair_color)
        if facial_hair:
            subject_mods.append(facial_hair + "의")
        if makeup:
            subject_mods.append(makeup)
        if expression:
            subject_mods.append(expression + "의")
        if accessory:
            subject_mods.append(accessory + josa(accessory, "을", "를") + " 착용한")
        if wardrobe:
            subject_mods.append(wardrobe + josa(wardrobe, "을", "를") + " 입은")
        if footwear:
            subject_mods.append(footwear + josa(footwear, "을", "를") + " 신은")
        if silhouette:
            subject_mods.append(silhouette + " 실루엣의")
        if costume:
            subject_mods.append(costume + josa(costume, "을", "를") + " 입은")
        subject_with_mods = clean_spaces(" ".join(subject_mods + ([subject] if subject else [])))
        pose_action = clean_spaces(" ".join(part for part in (action, body_pose) if part))
        subject_phrase = clean_spaces(f"{pose_action} {subject_with_mods}")
        object_phrase = subject_phrase + josa(subject_phrase, "을", "를") if subject_phrase else ""
    else:
        subject_suffixes = []
        with_details = []
        wearing_details = []
        for slot_name in ("person_origin", "appearance_type"):
            value = values.get(slot_name)
            if not value:
                continue
            lowered = value.lower()
            if lowered.startswith("with "):
                with_details.append(value[5:])
            elif lowered.startswith("wearing "):
                wearing_details.append(value[8:])
            else:
                subject_suffixes.append(value)
        if hair:
            with_details.append(hair)
        if hair_color:
            with_details.append(hair_color)
        if facial_hair:
            with_details.append(facial_hair)
        if makeup:
            with_details.append(makeup)
        if expression:
            with_details.append(expression)
        if accessory:
            wearing_details.append(accessory)
        if wardrobe:
            wearing_details.append(wardrobe)
        if footwear:
            wearing_details.append(footwear)
        if silhouette:
            with_details.append(silhouette)
        if costume:
            wearing_details.append(costume)
        if with_details:
            subject_suffixes.append("with " + unique_join(with_details))
        if wearing_details:
            subject_suffixes.append("wearing " + unique_join(wearing_details))
        subject_with_mods = clean_spaces(" ".join(([subject] if subject else []) + subject_suffixes))
        subject_phrase = clean_spaces(f"{subject_with_mods} {action} {body_pose}")
        object_phrase = subject_phrase

    location_entry = picked.get("location")
    if location_entry and lang == "ko":
        location_phrase = location_entry.get("phrase_ko") or (localize(location_entry, "ko") + "에서")
    elif location_entry:
        raw_location = localize(location_entry, "en")
        location_phrase = location_entry.get("phrase_en") or (
            raw_location
            if raw_location.lower().startswith(("in ", "inside ", "at ", "on ", "beside ", "near ", "under "))
            else "in " + raw_location
        )
    else:
        location_phrase = ""

    def slot_phrase(slot_name: str) -> str:
        entry = picked.get(slot_name)
        if not entry:
            return ""
        if lang == "ko":
            return entry.get("phrase_ko") or localize(entry, "ko")
        return entry.get("phrase_en") or localize(entry, "en")

    scene_context_slots = (
        "space_condition",
        "crowd_density",
        "situation_context",
        "occasion_context",
    )
    scene_context_parts = [slot_phrase(slot) for slot in scene_context_slots if slot_phrase(slot)]
    if lang == "ko":
        scene_context_sentence = (
            ensure_period("장면 맥락은 " + ", ".join(scene_context_parts)) if scene_context_parts else ""
        )
    else:
        scene_context_sentence = (
            ensure_period("Scene context: " + ", ".join(scene_context_parts)) if scene_context_parts else ""
        )

    narrative_context_slots = (
        "narrative_core",
        "concept_tension",
    )
    narrative_context_parts = [slot_phrase(slot) for slot in narrative_context_slots if slot_phrase(slot)]
    if lang == "ko":
        narrative_context_sentence = (
            ensure_period("서사와 대비는 " + ", ".join(narrative_context_parts)) if narrative_context_parts else ""
        )
    else:
        narrative_context_sentence = (
            ensure_period("Narrative and visual tension: " + ", ".join(narrative_context_parts))
            if narrative_context_parts
            else ""
        )

    lighting_slots = ("lighting", "light_direction", "light_type", "light_intensity", "light_shape")
    camera_slots = (
        "camera_type",
        "capture_context",
        "camera_direction",
        "shot_scale",
        "platform_framing",
        "composition",
        "subject_framing",
        "body_framing",
        "lens",
        "focus",
        "motion",
    )
    style_slots = (
        "world",
        "aesthetic_trend",
        "film_emulation",
        "color",
        "mood",
        "surreal_concept",
        "surreal_anchor",
        "scale_relation",
        "surreal_physics_detail",
        "adult_context",
        "caption_context",
    )
    detail_slots = (
        "wearable_accessory",
        "facial_hair",
        "body_pose",
        "body_orientation",
        "hand_pose",
        "gaze_engagement",
        "wardrobe_style",
        "footwear",
        "silhouette_proportion",
        "garment_detail",
        "makeup_style",
        "skin_finish",
        "skin_condition",
        "brow_style",
        "lip_finish",
        "eye_makeup_line",
        "eye_detail",
        "costume_style",
        "fetish_styling",
        "surface_material",
        "texture",
        "format",
        "quality",
    )

    lighting_parts = [values[s] for s in lighting_slots if values.get(s)]
    camera_parts = [values[s] for s in camera_slots if values.get(s)]

    if lang == "ko":
        technique_chunks = []
        if camera_parts:
            technique_chunks.append("카메라는 " + ", ".join(camera_parts))
        if lighting_parts:
            technique_chunks.append("조명은 " + ", ".join(lighting_parts))
        technique_sentence = ensure_period("; ".join(technique_chunks)) if technique_chunks else ""

        style_parts = [values[s] for s in style_slots if values.get(s)]
        style_sentence = ensure_period("전체 분위기는 " + ", ".join(style_parts)) if style_parts else ""

        detail_parts = [values[s] for s in detail_slots if values.get(s)]
        if narrative_context_sentence:
            detail_parts.insert(0, narrative_context_sentence)
        if scene_context_sentence:
            detail_parts.insert(0, scene_context_sentence)
        detail_sentence = ensure_period("디테일은 " + ", ".join(detail_parts)) if detail_parts else ""
    else:
        technique_chunks = []
        if camera_parts:
            technique_chunks.append("Camera: " + ", ".join(camera_parts))
        if lighting_parts:
            technique_chunks.append("Lighting: " + ", ".join(lighting_parts))
        technique_sentence = ensure_period("; ".join(technique_chunks)) if technique_chunks else ""

        style_parts = [values[s] for s in style_slots if values.get(s)]
        style_sentence = ensure_period("Overall mood: " + ", ".join(style_parts)) if style_parts else ""

        detail_parts = [values[s] for s in detail_slots if values.get(s)]
        if narrative_context_sentence:
            detail_parts.insert(0, narrative_context_sentence)
        if scene_context_sentence:
            detail_parts.insert(0, scene_context_sentence)
        detail_sentence = ensure_period("Finishing details: " + ", ".join(detail_parts)) if detail_parts else ""

    fields = {
        **values,
        "location_phrase": location_phrase,
        "scene_context_sentence": scene_context_sentence,
        "narrative_context_sentence": narrative_context_sentence,
        "subject_with_mods": subject_with_mods,
        "subject_phrase": subject_phrase,
        "object_phrase": object_phrase,
        "technique_sentence": technique_sentence,
        "style_sentence": style_sentence,
        "detail_sentence": detail_sentence,
    }
    return fields


def join_parts(parts: Sequence[str], fallback: str = "") -> str:
    return ", ".join(part for part in parts if part) or fallback


def render_surreal_layer_detail(picked: Dict[str, Entry], lang: str) -> str:
    if not has_surreal_layer(picked):
        return ""

    values = {slot: localize(entry, lang) for slot, entry in picked.items()}
    concept = values.get("surreal_concept", "")
    anchor = values.get("surreal_anchor", "")
    scale = values.get("scale_relation", "")
    physics = values.get("surreal_physics_detail", "")

    if lang == "ko":
        parts = []
        if concept:
            parts.append(f"초현실 사건은 {concept}")
        if anchor:
            parts.append(f"현실 앵커는 {anchor}")
        if scale:
            parts.append(f"스케일 관계는 {scale}")
        if physics:
            parts.append(f"물리 단서는 {physics}")
        body = "; ".join(parts)
        return ensure_period(
            f"포토리얼 초현실 레이어: {body}; 불가능한 장면이지만 합성이나 일러스트가 아니라 "
            "실제 카메라로 촬영된 순간처럼 보이게 하고, 스케일 단서, 그림자, 반사, 초점, "
            "경계면 가림, 현실 조명의 일관성을 분명히 유지한다."
        )

    parts = []
    if concept:
        parts.append(f"surreal event: {concept}")
    if anchor:
        parts.append(f"real-world anchor: {anchor}")
    if scale:
        parts.append(f"scale relation: {scale}")
    if physics:
        parts.append(f"physical realism cue: {physics}")
    body = "; ".join(parts)
    return ensure_period(
        f"Photoreal surreal layer: {body}; make the impossible scene read as a real camera capture, "
        "not a collage or illustration, with clear scale cues, shadows, reflections, focus behavior, "
        "boundary occlusion, and consistent real-world lighting."
    )


def render_subject_guidance(category: str, lang: str) -> str:
    if lang == "ko":
        guidance = {
            "human": "피사체의 자세, 시선, 표정, 손동작, 즉각적인 동작 의도가 한눈에 읽히게 하고, 주변 소품과 배경 요소는 그 행동을 설명하도록 배치한다",
            "animal": "동물의 자세, 움직임, 시선 방향, 털이나 깃의 질감이 자연스럽게 읽히게 하고, 주변 환경은 행동의 맥락을 설명하도록 배치한다",
            "food": "음식의 형태, 표면 질감, 온도감, 수분, 김, 소스나 부스러기 같은 식감 단서가 실제 촬영처럼 읽히게 한다",
            "object": "사물의 형태, 재질, 가장자리, 접지면, 스케일, 사용 흔적이 분명하게 보이게 하고, 주변 소품은 크기와 용도를 설명하도록 배치한다",
            "sign": "문자나 발광면의 가독성, 반사, 표면 오염, 주변 벽이나 바닥에 번지는 빛이 실제 장소 안에 자연스럽게 통합되게 한다",
            "plant": "식물의 줄기, 잎, 포자, 물방울, 표면 결이 실제 매크로 사진처럼 읽히게 한다",
            "environment": "공간의 구조, 주요 형태, 바닥/벽/천장 또는 하늘의 관계, 전경/중경/후경의 거리감이 명확히 읽히게 한다",
        }
        return guidance.get(category, "중심 피사체의 형태, 위치, 동작 또는 상태가 사진 안에서 명확히 읽히게 한다")

    guidance = {
        "human": "make the pose, gaze, expression, hand placement, and immediate intention readable, with nearby props and background details supporting the action",
        "animal": "make the animal posture, motion, eye direction, and fur or feather texture read naturally, with the environment supporting the behavior",
        "food": "make the shape, surface texture, temperature cues, moisture, steam, sauce, crumbs, and edible detail read like a real food photograph",
        "object": "make the object's form, material, edges, contact surface, scale, and signs of use clear, with nearby props explaining size and purpose",
        "sign": "make lettering or illuminated surfaces readable, with reflections, surface grime, and spill light integrated into the real location",
        "plant": "make stems, leaves, spores, droplets, and surface texture read like real macro photographic detail",
        "environment": "make the spatial structure, major forms, floor/wall/ceiling or sky relationships, foreground, midground, and background depth clear",
    }
    return guidance.get(category, "make the main subject's form, placement, action, or state clearly readable in the photograph")


def render_scene_guidance(category: str, lang: str) -> str:
    if lang == "ko":
        if category in {"food", "object", "plant", "sign"}:
            return "촬영 표면, 배경 거리, 접촉 그림자, 주변 소품의 크기 단서를 분명히 보여준다"
        return "공간의 깊이, 바닥/벽/하늘 또는 실내 구조, 전경/중경/후경의 거리감을 분명히 보여준다"

    if category in {"food", "object", "plant", "sign"}:
        return "show the shooting surface, background distance, contact shadows, and scale cues from nearby props"
    return "show clear spatial depth, environmental structure, foreground, midground, and background cues"


def render_finish_guidance(category: str, lang: str, generation_contract: Optional[JsonDict] = None) -> str:
    domains = set((generation_contract or {}).get("preset_domains", []))
    if lang == "ko":
        if category == "human" and domains & {"documentary", "craft"}:
            return "피부, 머리카락, 손, 작업복, 도구, 유리나 세라믹 같은 작업 재료, 먼지와 사용 흔적을 실제 다큐멘터리 질감으로 표현한다"
        guidance = {
            "human": "피부, 머리카락, 천, 금속, 유리, 메이크업, 액세서리 같은 소재 단서를 실제 질감으로 표현한다",
            "animal": "털, 깃, 눈, 발, 젖은 표면, 흙, 식물, 배경 질감을 실제 질감으로 표현한다",
            "food": "빵 껍질, 면, 소스, 수분, 김, 접시, 식기, 테이블 표면을 실제 식감과 재질로 표현한다",
            "object": "금속, 유리, 플라스틱, 세라믹, 종이, 먼지, 스크래치, 반사 같은 물성 단서를 정확히 표현한다",
            "sign": "발광면, 유리, 금속 프레임, 빗물, 먼지, 반사광, 표면 스크래치를 실제 재질처럼 표현한다",
            "plant": "잎맥, 줄기, 흙, 이끼, 물방울, 미세한 표면 결을 실제 매크로 질감으로 표현한다",
            "environment": "벽, 바닥, 천장, 창, 먼지, 습기, 반사, 그레인 같은 공간 질감을 실제 사진처럼 표현한다",
        }
        return guidance.get(category, "보이는 소재 단서를 실제 사진 질감으로 표현한다")

    if category == "human" and domains & {"documentary", "craft"}:
        return "render skin, hair, hands, work clothing, tools, glass or ceramic work materials, dust, and signs of use with documentary photographic texture"
    guidance = {
        "human": "render skin, hair, fabric, metal, glass, makeup, and accessories with accurate material detail",
        "animal": "render fur, feathers, eyes, paws, moisture, soil, plants, and background texture with accurate detail",
        "food": "render crust, noodles, sauce, moisture, steam, plates, utensils, and tabletop surfaces with appetizing real texture",
        "object": "render metal, glass, plastic, ceramic, paper, dust, scratches, and reflections with accurate physical detail",
        "sign": "render illuminated panels, glass, metal frames, rain, dust, reflected light, and surface scratches like real materials",
        "plant": "render leaf veins, stems, soil, moss, droplets, and fine surface texture as real macro detail",
        "environment": "render walls, floors, ceilings, windows, dust, moisture, reflections, and grain as real photographic texture",
    }
    return guidance.get(category, "render visible material cues with accurate photographic texture")


def render_reference_edit_detail(mode: str, lang: str) -> str:
    if mode == "off":
        return ""
    if lang == "ko":
        details = {
            "identity": (
                "레퍼런스 편집 지시: 업로드된 인물 사진이 있다면 얼굴의 눈 모양과 간격, 눈썹, 코, 입술, 턱선, "
                "광대, 피부톤, 자연스러운 비대칭, 헤어라인을 유지하고, 조명과 배경만 새 장면에 맞게 바꾼다."
            ),
            "younger_self": (
                "레퍼런스 편집 지시: 현재 모습과 어린 시절 사진 두 장이 있다면 두 인물을 같은 공간 안에 배치하고, "
                "시선 방향, 거리, 중앙 오브젝트, 공통 조명과 그림자를 명확히 맞춰 한 장의 실제 사진처럼 만든다."
            ),
            "brand_board": (
                "레퍼런스 편집 지시: 업로드된 인물이나 제품의 핵심 형태를 유지하며, 같은 색감과 조명으로 여러 컷이 "
                "묶인 개인 브랜드 보드처럼 일관되게 구성한다."
            ),
        }
    else:
        details = {
            "identity": (
                "Reference-edit instruction: if an uploaded portrait is provided, preserve eye shape and spacing, eyebrows, nose, "
                "lips, jawline, cheekbones, skin tone, natural asymmetry, and hairline while changing only lighting, outfit, and setting."
            ),
            "younger_self": (
                "Reference-edit instruction: if current and childhood photos are provided, place both versions in one shared space, "
                "with clear gaze direction, distance, a central anchor object, shared lighting, and matching shadows."
            ),
            "brand_board": (
                "Reference-edit instruction: preserve the uploaded person or product identity while arranging multiple consistent shots "
                "as a personal brand board with unified color, lighting, and crop logic."
            ),
        }
    return ensure_period(details.get(mode, ""))


def render_trend_layer_detail(layer: str, lang: str) -> str:
    if layer == "off":
        return ""
    if lang == "ko":
        details = {
            "scrapbook_collage": (
                "트렌드 레이어: 같은 피사체의 겹쳐진 인화 사진, 테이프, 찢어진 종이, 작은 스티커, 클로즈업 조각을 "
                "포함한 스크랩북 콜라주 구성이며, 모든 조각은 같은 촬영 세계의 빛과 색을 공유한다."
            ),
            "action_figure_packaging": (
                "트렌드 레이어: 피사체를 수집용 액션 피규어 패키지처럼 구성하되, 투명 플라스틱 블리스터, 제품 카드, "
                "작은 액세서리 칸, 실제 제품 사진 같은 반사와 그림자를 명확히 표현한다."
            ),
            "retro_flash": (
                "트렌드 레이어: 2000년대 컴팩트 디지털카메라나 폰 직광 플래시처럼 강한 정면 플래시, 미세한 흔들림, "
                "살짝 과노출된 피부/표면, 어두운 배경 낙차를 사용한다."
            ),
            "clean_brand_portrait": (
                "트렌드 레이어: 개인 브랜드 프로필에 맞게 깨끗한 배경, 안정적인 크롭, 자연스러운 피부/소재 질감, "
                "프로필과 썸네일에서 읽히는 명확한 실루엣을 유지한다."
            ),
        }
    else:
        details = {
            "scrapbook_collage": (
                "Trend layer: build a scrapbook collage with overlapping printed photos of the same subject, tape, torn paper, "
                "small stickers, and close-up fragments, all sharing one coherent lighting and color world."
            ),
            "action_figure_packaging": (
                "Trend layer: stage the subject like a collectible action figure package with clear plastic blister, product card, "
                "small accessory compartments, and realistic product-photo reflections and shadows."
            ),
            "retro_flash": (
                "Trend layer: use a 2000s compact digital camera or phone direct-flash look with hard frontal flash, slight motion blur, "
                "a little overexposure on skin or surfaces, and a dark background falloff."
            ),
            "clean_brand_portrait": (
                "Trend layer: keep a clean personal-brand portrait structure with a tidy background, stable crop, natural skin or material texture, "
                "and a clear silhouette readable as a profile image or thumbnail."
            ),
        }
    return ensure_period(details.get(layer, ""))


PROMPT_SECTION_ORDER = (
    "intent",
    "subject",
    "action",
    "scene",
    "camera",
    "lighting",
    "palette_mood",
    "finish",
    "special_layers",
    "constraints",
)


def inline_constraints(lang: str) -> List[str]:
    if lang == "ko":
        return ["텍스트나 워터마크 없음"]
    return ["no text or watermark"]


def dedupe_parts(parts: Sequence[str]) -> List[str]:
    seen: Set[str] = set()
    unique: List[str] = []
    for part in parts:
        cleaned = clean_spaces(part)
        if not cleaned:
            continue
        key = cleaned.lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(cleaned)
    return unique


def normalize_concept_locks(items: Optional[Sequence[str]]) -> List[str]:
    if not items:
        return []
    return dedupe_parts(str(item) for item in items if str(item).strip())


def concept_lock_text(generation_contract: Optional[JsonDict]) -> str:
    return unique_join(normalize_concept_locks((generation_contract or {}).get("concept_locks", [])), "; ")


def render_concept_lock_sentence(generation_contract: Optional[JsonDict], lang: str, compact: bool = False) -> str:
    concept = concept_lock_text(generation_contract)
    if not concept:
        return ""
    if compact:
        if lang == "ko":
            return f"원래 핵심 컨셉인 {concept}을 유지하고, 생성된 세부 요소는 그 컨셉을 보조하는 방향"
        return f"preserving the core concept of {concept}, with generated details supporting rather than replacing it"
    if lang == "ko":
        return (
            f"핵심 컨셉 잠금: {concept}. "
            "아래의 피사체, 동작, 조명, 카메라 디테일은 이 컨셉을 대체하지 않고 보조해야 한다."
        )
    return (
        f"Core concept lock: {concept}. "
        "Treat every generated subject, action, lighting, and camera detail as support for this concept, not a replacement."
    )


def normalize_additional_requirements(items: Optional[Sequence[str]]) -> List[str]:
    return dedupe_parts(str(item) for item in items or [] if str(item).strip())


def render_additional_requirements_sentence(items: Optional[Sequence[str]], lang: str) -> str:
    requirements = normalize_additional_requirements(items)
    if not requirements:
        return ""
    joined = "; ".join(clean_spaces(item).rstrip(".!?。") for item in requirements)
    if lang == "ko":
        return f"추가 요구사항: {joined}."
    return f"Additional requirements: {joined}."


def render_likeness_sentence(mode: str, lang: str) -> str:
    if mode == "off":
        return ""
    if mode != "inspired":
        raise ValueError(f"Unknown likeness mode: {mode}")
    if lang == "ko":
        return (
            "묘사된 스타일과 분위기에서 영감을 받은 가상의 성인 인물이며, "
            "특정 실존 인물의 정확한 외모 재현이 아니다."
        )
    return (
        "Inspired by the described styling and vibe; an original adult fictional person, "
        "not an exact likeness of any real individual."
    )


def append_render_contract_sentences(
    prompt: str,
    lang: str,
    additional_requirements: Optional[Sequence[str]],
    likeness_mode: str,
) -> str:
    additions = [
        render_additional_requirements_sentence(additional_requirements, lang),
        render_likeness_sentence(likeness_mode, lang),
    ]
    for addition in additions:
        if addition and addition.lower() not in prompt.lower():
            prompt = clean_spaces(f"{prompt} {ensure_period(addition)}")
    return clean_spaces(prompt)


def append_artistic_final_touch(
    data: JsonDict,
    prompt: str,
    preset: JsonDict,
    picked: Dict[str, Entry],
    lang: str,
    detail_level: str,
) -> str:
    quality_profile = candidate_pack_quality_profile_from_selected(data, preset, picked)
    touch = artistic_final_touch_sentence(
        data,
        lang,
        detail_level,
        str(quality_profile.get("profile_id") or "general"),
    )
    if not touch:
        return clean_spaces(prompt)
    prompt_clean = clean_spaces(prompt)
    if prompt_clean.lower().endswith(touch.lower()):
        return prompt_clean
    word_budget = {"compact": 120, "standard": 150, "detailed": 190}.get(detail_level, 150)
    if lang == "en" and len(f"{prompt_clean} {touch}".split()) > word_budget:
        return prompt_clean
    return clean_spaces(f"{prompt_clean} {touch}")


def build_prompt_sections(
    data: JsonDict,
    preset: JsonDict,
    picked: Dict[str, Entry],
    lang: str,
    reference_edit_mode: str = "off",
    trend_layer: str = "off",
) -> Dict[str, List[str]]:
    fields = build_fields(picked, lang, data)
    values = {slot: localize(entry, lang) for slot, entry in picked.items()}

    def selected(slots: Sequence[str]) -> List[str]:
        return [values[slot] for slot in slots if values.get(slot)]

    sections: Dict[str, List[str]] = {section: [] for section in PROMPT_SECTION_ORDER}
    sections["intent"] = selected(("medium", "genre", "format", "quality"))
    sections["subject"] = [
        fields.get("subject_with_mods") or values.get("subject", "")
    ]
    sections["action"] = selected(
        (
            "action",
            "body_pose",
            "hand_pose",
            "gaze_engagement",
            "procedure_step",
            "duty_prop_state",
            "relational_action",
            "prop",
            "prop_direction",
            "social_cue",
            "partner_role",
            "contact_point",
            "intent_state",
            "emotional_contradiction",
            "narrative_phase",
        )
    )
    sections["scene"] = [
        fields.get("location_phrase") or values.get("location", ""),
        fields.get("scene_context_sentence", ""),
        fields.get("narrative_context_sentence", ""),
        values.get("time_of_day", ""),
        values.get("weather", ""),
        values.get("surface_material", ""),
        values.get("world", ""),
        values.get("reflection_logic", ""),
    ]
    sections["camera"] = selected(
        (
            "camera_type",
            "capture_context",
            "viewer_position",
            "camera_height",
            "camera_direction",
            "shot_scale",
            "platform_framing",
            "composition",
            "partner_framing",
            "gaze_target",
            "body_orientation",
            "proxemics",
            "distance_narrative",
            "subject_framing",
            "body_framing",
            "body_evidence_region",
            "lens",
            "focus",
            "motion",
            "frame_anchor_medium",
        )
    )
    sections["lighting"] = selected(
        ("lighting", "light_direction", "light_type", "light_intensity", "light_shape")
    )
    sections["palette_mood"] = selected(("color", "mood", "adult_context", "caption_context"))
    sections["finish"] = selected(
        (
            "film_emulation",
            "aesthetic_trend",
            "wearable_accessory",
            "facial_hair",
            "species_marker",
            "transition_stage",
            "anatomical_connection",
            "costume_absorption_guard",
            "sensory_focus",
            "texture",
            "wardrobe_style",
            "makeup_style",
            "skin_finish",
            "skin_condition",
            "brow_style",
            "lip_finish",
            "eye_makeup_line",
            "eye_detail",
            "costume_style",
            "fetish_styling",
            "surface_material",
            "format",
            "quality",
        )
    )
    sections["special_layers"] = dedupe_parts(
        [
            render_surreal_layer_detail(picked, lang),
            render_reference_edit_detail(reference_edit_mode, lang),
            render_trend_layer_detail(trend_layer, lang),
        ]
    )
    sections["constraints"] = dedupe_parts(inline_constraints(lang) + selected(("safety_profile",)))
    return {section: dedupe_parts(parts) for section, parts in sections.items()}


def section_text(sections: Dict[str, List[str]], section: str, fallback: str = "") -> str:
    return unique_join(sections.get(section, [])) or fallback


def section_ordered_standard_templates(templates: Sequence[str]) -> List[str]:
    ordered: List[str] = []
    for template in templates:
        subject_positions = [
            pos for pos in (template.find("{subject_phrase}"), template.find("{object_phrase}")) if pos >= 0
        ]
        location_positions = [
            pos for pos in (template.find("{location_phrase}"), template.find("{location}")) if pos >= 0
        ]
        if subject_positions and location_positions and min(subject_positions) < min(location_positions):
            ordered.append(template)
    return ordered


def ensure_standard_section_order(
    prompt: str,
    sections: Dict[str, List[str]],
    fields: Dict[str, str],
    lang: str,
) -> str:
    scene_markers = dedupe_parts(
        list(sections.get("scene", []))
        + [
            fields.get("location_phrase", ""),
            fields.get("location", ""),
        ]
    )
    subject_markers = [
        part
        for part in (
            fields.get("subject_phrase", ""),
            fields.get("object_phrase", ""),
            section_text(sections, "subject"),
        )
        if part
    ]

    subject_positions = [prompt.find(marker) for marker in subject_markers if prompt.find(marker) >= 0]
    scene_positions = [prompt.find(marker) for marker in scene_markers if prompt.find(marker) >= 0]
    if not subject_positions or not scene_positions or min(subject_positions) < min(scene_positions):
        return prompt

    subject = fields.get("subject", "") or section_text(sections, "subject")
    if not subject:
        return prompt
    prefix = ("중심 피사체: " if lang == "ko" else "Subject: ") + subject
    return clean_spaces(f"{ensure_period(prefix)} {prompt}")


def render_detailed_prompt(
    data: JsonDict,
    preset: JsonDict,
    picked: Dict[str, Entry],
    lang: str,
    sections: Dict[str, List[str]],
    generation_contract: Optional[JsonDict] = None,
) -> str:
    fields = build_fields(picked, lang, data)
    values = {slot: localize(entry, lang) for slot, entry in picked.items()}
    category = subject_category(picked, data)
    concept_lock = render_concept_lock_sentence(generation_contract, lang)

    if lang == "ko":
        subject = section_text(sections, "subject", values.get("subject", "중심 피사체"))
        action = section_text(sections, "action")
        subject_state = f"{subject}; 동작과 소품: {action}" if action else subject
        location = section_text(sections, "scene", values.get("location", "구체적인 장소"))
        camera = section_text(sections, "camera", "명확한 카메라 위치, 의도적인 구도, 사실적인 초점")
        lighting = section_text(sections, "lighting", "자연스럽고 설득력 있는 사진 조명")
        mood = section_text(sections, "palette_mood", "일관된 색감, 분위기, 세계관 맥락")
        finish = section_text(sections, "finish", "정확한 소재 디테일을 가진 이미지 생성용 마감")
        special = " ".join(sections.get("special_layers", []))
        constraints = section_text(sections, "constraints")
        genre = values.get("genre", "사진")
        medium = values.get("medium", "실사 사진")
        subject_guidance = render_subject_guidance(category, lang)
        scene_guidance = render_scene_guidance(category, lang)
        finish_guidance = render_finish_guidance(category, lang, generation_contract)
        constraint_sentence = f"제약: {constraints}. " if constraints else ""
        prompt = " ".join(
            part
            for part in [
                concept_lock,
                f"{medium}로 렌더링할 {genre}. "
                f"중심 피사체와 상태: {subject_state}; {subject_guidance}. "
                f"장면과 장소: {location}; {scene_guidance}. "
                f"카메라와 구도: {camera}; 피사체 크기, 포즈 가시성, 플랫폼 안전 프레임, 프레임 가장자리, 원근감, 초점 위치, 움직임 처리를 명확히 한다. "
                f"조명: {lighting}; 그림자 방향, 하이라이트, 반사광, 노출 균형, 대기감을 실제 촬영처럼 보이게 한다. "
                f"색감과 분위기: {mood}; 색 대비, 감정 톤, 세계관 맥락이 피사체와 장소에 맞아야 한다. ",
                special,
                f"질감과 마감: {finish}; {finish_guidance}. "
                f"{constraint_sentence}"
                "이미지 생성 시 요구사항을 빠뜨리지 말고, 막연한 스타일 요약보다 구체적인 사진 결과를 우선한다.",
            ]
            if part
        )
    else:
        subject = section_text(sections, "subject", values.get("subject", "the main subject"))
        action = section_text(sections, "action")
        subject_state = f"{subject}; action and prop: {action}" if action else subject
        location = section_text(sections, "scene", values.get("location", "a specific location"))
        camera = section_text(sections, "camera", "clear camera placement, deliberate composition, realistic focus")
        lighting = section_text(sections, "lighting", "natural, believable photographic light")
        mood = section_text(sections, "palette_mood", "coherent color, mood, and world context")
        finish = section_text(sections, "finish", "photo-ready finish with accurate material detail")
        special = " ".join(sections.get("special_layers", []))
        constraints = section_text(sections, "constraints")
        genre = values.get("genre", "photography")
        medium = values.get("medium", "photograph")
        subject_guidance = render_subject_guidance(category, lang)
        scene_guidance = render_scene_guidance(category, lang)
        finish_guidance = render_finish_guidance(category, lang, generation_contract)
        constraint_sentence = f"Constraints: {constraints}. " if constraints else ""
        prompt = " ".join(
            part
            for part in [
                concept_lock,
                f"Create {with_indefinite_article(medium)} in the style of {genre}. "
                f"Subject and state: {subject_state}; {subject_guidance}. "
                f"Scene and location: {location}; {scene_guidance}. "
                f"Camera and composition: {camera}; define subject scale, pose visibility, platform-safe frame edges, perspective, focus behavior, and any motion treatment clearly. "
                f"Lighting: {lighting}; make shadow direction, highlights, reflected light, exposure balance, and atmosphere feel like a real photographic capture. "
                f"Color and mood: {mood}; keep the palette, emotional tone, and world context coherent with the subject and setting. ",
                special,
                f"Texture, format, and finish: {finish}; {finish_guidance}. "
                f"{constraint_sentence}"
                "Prioritize a specific, image-ready photographic result over a vague style summary.",
            ]
            if part
        )

    return clean_spaces(prompt)


def unique_join(parts: Sequence[str], separator: str = ", ") -> str:
    seen: Set[str] = set()
    unique: List[str] = []
    for part in parts:
        cleaned = clean_spaces(part)
        if not cleaned:
            continue
        key = cleaned.lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(cleaned)
    return separator.join(unique)


def render_compact_prompt(
    data: JsonDict,
    preset: JsonDict,
    picked: Dict[str, Entry],
    lang: str,
    sections: Dict[str, List[str]],
    generation_contract: Optional[JsonDict] = None,
) -> str:
    values = {slot: localize(entry, lang) for slot, entry in picked.items()}
    category = subject_category(picked, data)
    concept_lock = render_concept_lock_sentence(generation_contract, lang, compact=True)

    def render_with_drops(drop_sections: Set[str]) -> str:
        content_parts: List[str] = []
        if concept_lock:
            content_parts.append(concept_lock)
        for section in ("action", "scene", "camera", "lighting", "palette_mood", "finish", "special_layers"):
            if section in drop_sections:
                continue
            if section == "scene" and "world" in drop_sections:
                content = unique_join(sections.get("scene", [])[:1])
            elif section == "finish" and values.get("format"):
                content = unique_join([part for part in sections.get("finish", []) if part != values.get("format")])
            else:
                content = section_text(sections, section)
            if content:
                content_parts.append(content)
        if category == "human" and "finish" not in drop_sections:
            content_parts.append("자연스러운 피부 질감" if lang == "ko" else "natural skin texture")
        constraints = section_text(sections, "constraints")
        if constraints:
            content_parts.append(constraints)

        subject = section_text(sections, "subject", "중심 피사체" if lang == "ko" else "the main subject")
        if lang == "ko":
            lead = unique_join(
                ["초사실적", values.get("format", ""), values.get("genre", ""), values.get("medium", "실사 사진")],
                " ",
            )
            return ensure_period(f"{lead}, {subject}, {unique_join(content_parts)}")

        lead = unique_join(
            ["Ultra-realistic", values.get("format", ""), values.get("genre", ""), values.get("medium", "photograph")],
            " ",
        )
        return ensure_period(f"{lead} of {subject}, {unique_join(content_parts)}")

    drop_sections: Set[str] = set()
    prompt = render_with_drops(drop_sections)
    forced_slots = set((generation_contract or {}).get("forced_slots", []) or [])
    section_forced_slots = {
        "palette_mood": {"color", "color_grading", "mood", "world"},
        "finish": {
            "texture",
            "format",
            "quality",
            "skin_finish",
            "skin_condition",
            "brow_style",
            "lip_finish",
            "eye_makeup_line",
            "eye_detail",
            "film_emulation",
            "grain_profile",
            "lens_artifact",
        },
        "caption_context": {"caption_context"},
        "world": {"world"},
    }
    for section in ("palette_mood", "finish", "caption_context", "world"):
        if lang != "en" or len(prompt.split()) <= 120:
            break
        if forced_slots & section_forced_slots.get(section, set()):
            continue
        drop_sections.add(section)
        prompt = render_with_drops(drop_sections)
    return clean_spaces(prompt)


def render_prompt(
    data: JsonDict,
    preset: JsonDict,
    picked: Dict[str, Entry],
    lang: str,
    rng: random.Random,
    detail_level: str = "standard",
    reference_edit_mode: str = "off",
    trend_layer: str = "off",
    generation_contract: Optional[JsonDict] = None,
    additional_requirements: Optional[Sequence[str]] = None,
    likeness_mode: str = "off",
) -> str:
    render_picked = render_guarded_picked(data, preset, picked, generation_contract)
    sections = build_prompt_sections(data, preset, render_picked, lang, reference_edit_mode, trend_layer)

    if detail_level == "detailed":
        prompt = render_detailed_prompt(data, preset, render_picked, lang, sections, generation_contract)
    elif detail_level == "compact":
        prompt = render_compact_prompt(data, preset, render_picked, lang, sections, generation_contract)
    else:
        style = preset.get("template_style", "natural")
        templates_by_lang = data.get("templates", {}).get(style, {})
        templates = templates_by_lang.get(lang) or templates_by_lang.get("en")

        if not templates:
            # Safe fallback template if JSON has no template section.
            if lang == "ko":
                templates = [
                    "{medium}. {location_phrase} {object_phrase} 담은 {genre}. {technique_sentence} {style_sentence} {detail_sentence}"
                ]
            else:
                templates = [
                    "{medium}. {genre} featuring {subject_phrase} {location_phrase}. {technique_sentence} {style_sentence} {detail_sentence}"
                ]

        ordered_templates = section_ordered_standard_templates(templates)
        template = rng.choice(ordered_templates or templates)
        fields = build_fields(render_picked, lang, data)
        prompt = template.format(**fields)
        prompt = ensure_standard_section_order(prompt, sections, fields, lang)

        concept_lock = render_concept_lock_sentence(generation_contract, lang)
        if concept_lock and concept_lock.lower() not in prompt.lower():
            prompt = clean_spaces(f"{ensure_period(concept_lock)} {prompt}")

        additions: List[str] = []
        action = section_text(sections, "action")
        if action and any(part.lower() not in prompt.lower() for part in sections.get("action", [])):
            additions.append(("동작과 소품: " if lang == "ko" else "Action and prop: ") + action)
        for special in sections.get("special_layers", []):
            if special and special.lower() not in prompt.lower():
                additions.append(special)
        constraints = section_text(sections, "constraints")
        if constraints and constraints.lower() not in prompt.lower():
            additions.append(("제약: " if lang == "ko" else "Constraints: ") + constraints)

        if additions:
            prompt = clean_spaces(" ".join([prompt] + [ensure_period(part) for part in additions]))

    prompt = append_render_contract_sentences(prompt, lang, additional_requirements, likeness_mode)
    prompt = append_photographic_craft(data, prompt, preset, render_picked, lang, detail_level)
    return append_artistic_final_touch(data, prompt, preset, render_picked, lang, detail_level)


def choose_negative_entries(
    data: JsonDict,
    rng: random.Random,
    count: int = 12,
    include_surreal: bool = False,
    picked: Optional[Dict[str, Entry]] = None,
) -> List[Entry]:
    picked = picked or {}
    negative_pools = data.get("negative_prompt_pools", {})
    if negative_pools:
        pool_names = ["base"]
        category = subject_category(picked, data)
        context = picked_context_tokens(picked)
        core_context = picked_core_context_tokens(picked)
        if category == "human":
            pool_names.append("human")
        if category == "animal":
            pool_names.append("animal")
        if category == "food":
            pool_names.extend(["object_product", "food"])
        if category in {"object", "plant"}:
            pool_names.append("object_product")
        if category == "sign":
            pool_names.extend(["object_product", "text_signage"])
        if core_context & {"architecture", "real_estate"} or (category == "environment" and "interior" in core_context):
            pool_names.append("architecture_interior")

        seen: Set[str] = set()
        negatives: List[Entry] = []
        for pool_name in pool_names:
            for entry in negative_pools.get(pool_name, []):
                key = localize(entry, "en")
                if key and key not in seen:
                    negatives.append(entry)
                    seen.add(key)
    else:
        negatives = data.get("negative_prompt", [])

    if not negatives:
        entries: List[Entry] = []
    else:
        count = min(max(count, 1), len(negatives))
        entries = rng.sample(negatives, k=count)

    def append_context_pool(pool_name: str) -> None:
        seen = {localize(entry, "en") for entry in entries}
        for entry in negative_pools.get(pool_name, []):
            key = localize(entry, "en")
            if key and key not in seen:
                entries.append(entry)
                seen.add(key)

    if negative_pools:
        screen_context = {
            "screen",
            "server",
            "server_room",
            "server_room_aisle",
            "control",
            "control_room",
            "surveillance",
            "surveillance_control_room",
            "security_control_room",
            "digital",
            "ui",
            "monitor",
            "dashboard",
            "anti_diagram_context",
            "slot:frame_anchor_medium",
        }
        beastkin_context = {
            "beastkin",
            "beastkin_subject",
            "species_marker",
            "slot:species_marker",
            "transition_stage",
            "slot:transition_stage",
            "anatomical_connection",
            "slot:anatomical_connection",
            "body_evidence_region",
            "slot:body_evidence_region",
            "costume_absorption_guard",
            "slot:costume_absorption_guard",
            "costume_swap",
            "body_evidence",
            "human_animal_boundary",
        }
        ornament_risk_context = {
            "ornament_risk",
            "costume_absorption_risk",
            "costume_absorption_guard",
            "slot:costume_absorption_guard",
            "costume_style:covered_santa_fur_trim_costume",
            "costume_style:bunny_girl_costume",
            "costume_style:gothic_lolita_dress",
            "costume_style:gothic_doll_lace_dress",
            "costume_style:royal_princess_hanbok",
            "costume_style:crown_princess_ceremonial_robe",
            "costume_style:miner_workwear_hard_hat",
            "wardrobe_style:covered_track_jacket_training_set",
        }
        uniform_context = {
            "uniform",
            "authority",
            "safety_profile:uniformed_authority_profile",
            "safety_profile:procedural_authority_profile",
            "costume_style:police_uniform_costume",
            "costume_style:nurse_uniform_costume",
            "costume_style:covered_santa_fur_trim_costume",
            "costume_style:bunny_girl_costume",
        }
        food_mouth_context = {
            "single_ripe_tomato_near_lips",
            "prop:single_ripe_tomato_near_lips",
            "food_mouth_non_sensual",
            "anti_sensual_food",
            "mouth_nearby",
        }
        if context & screen_context or core_context & screen_context:
            append_context_pool("anti_diagram")
            append_context_pool("screen_workplace")
        if context & beastkin_context or core_context & beastkin_context:
            append_context_pool("anti_costume_shortcut")
            if context & ornament_risk_context or core_context & ornament_risk_context:
                append_context_pool("anti_ornament_absorption")
        if context & uniform_context or core_context & uniform_context:
            append_context_pool("role_dignity")
        if context & food_mouth_context or core_context & food_mouth_context:
            append_context_pool("anti_food_sensual")

    if include_surreal:
        seen = {localize(entry, "en") for entry in entries}
        surreal_pool = data.get("surreal_negative_prompt", [])
        if negative_pools:
            surreal_pool = negative_pools.get("surreal", surreal_pool)
        for entry in surreal_pool:
            if localize(entry, "en") not in seen:
                entries.append(entry)
                seen.add(localize(entry, "en"))

    if is_visible_multi_subject_prompt(picked):
        entries = [entry for entry in entries if localize(entry, "en").strip().lower() != "duplicate faces"]

    return entries


def render_negative_prompt(entries: Sequence[Entry], lang: str) -> str:
    return ", ".join(localize(x, lang) for x in entries)


def soft_render_suppress_negative_entries(policy: Optional[JsonDict]) -> List[Entry]:
    if not policy or not policy.get("enabled"):
        return []
    entries: List[Entry] = []
    seen: Set[str] = set()
    for term in normalize_list(policy.get("render_suppress_terms")) + normalize_list(policy.get("safety_negative_floor")):
        key = term.strip()
        if not key or key.lower() in seen:
            continue
        seen.add(key.lower())
        entries.append({"id": f"soft_suppress_{stable_text_id(key)}", "en": key, "ko": key})
    return entries


def render_directive_match_blob(picked: Dict[str, Entry], policy: Optional[JsonDict]) -> str:
    parts: List[str] = []
    for slot, entry in picked.items():
        parts.append(slot)
        parts.append(str(entry.get("id") or ""))
        parts.append(localize(entry, "en"))
        parts.append(localize(entry, "ko"))
        parts.extend(normalize_list(entry.get("tags")))
        parts.extend(normalize_list(entry.get("keywords")))
        parts.extend(normalize_list(entry.get("aliases")))
        parts.append(str(entry.get("embedding_text") or ""))
    for anchor in (policy or {}).get("anchors", []) or []:
        parts.extend(normalize_list(anchor.get("terms")))
        parts.extend(normalize_list(anchor.get("ids")))
        parts.extend(normalize_list(anchor.get("pool")))
    return " ".join(str(part).lower() for part in parts if str(part).strip())


def soft_render_directive_events(policy: Optional[JsonDict], picked: Dict[str, Entry]) -> List[JsonDict]:
    if not policy or not policy.get("enabled"):
        return []
    blob = render_directive_match_blob(picked, policy)
    events: List[JsonDict] = []
    for directive in policy.get("render_directives", []) or []:
        cue_terms = normalize_list(directive.get("cue_terms"))
        matched_terms = [term for term in cue_terms if str(term).strip() and str(term).lower() in blob]
        if not matched_terms:
            continue
        positive_clause = str(directive.get("positive_clause") or "").strip()
        if not positive_clause:
            continue
        events.append(
            {
                "id": str(directive.get("id") or "render_directive"),
                "cue_matched": True,
                "matched_terms": matched_terms,
                "render_as": str(directive.get("render_as") or ""),
                "positive_clause": positive_clause,
                "positive_clause_injected": True,
                "suppress_terms": normalize_list(directive.get("suppress_terms")),
                "suppress_terms_injected": bool(normalize_list(directive.get("suppress_terms"))),
            }
        )
    return events


def soft_render_directive_negative_entries(events: Sequence[JsonDict]) -> List[Entry]:
    entries: List[Entry] = []
    seen: Set[str] = set()
    for event in events:
        for term in normalize_list(event.get("suppress_terms")):
            key = term.strip()
            if not key or key.lower() in seen:
                continue
            seen.add(key.lower())
            entries.append({"id": f"soft_directive_suppress_{stable_text_id(key)}", "en": key, "ko": key})
    return entries


# Keep the low-level API neutral for internal research and holdout callers.
# ``main`` injects the user-facing CLI defaults (sensual 1, fetish 0) into candidate-pack runs.
def generate_once(
    data: JsonDict,
    rng: random.Random,
    preset_id: Optional[str],
    langs: Sequence[str],
    include_negative: bool,
    negative_count: int,
    include_choices: bool,
    forced_choices: Optional[Dict[str, List[str]]] = None,
    priority_bias: Optional[float] = None,
    detail_level: str = "standard",
    surreal_mode: str = "off",
    surreal_probability: float = 0.35,
    surreal_intensity: str = "moderate",
    reference_edit_mode: str = "off",
    trend_layer: str = "off",
    intent: Optional[str] = None,
    concept_locks: Optional[Sequence[str]] = None,
    selection_mode: str = "rule",
    novelty: str = "medium",
    filter_strictness: Optional[str] = None,
    semantic_weight: Optional[float] = None,
    semantic_profile: Optional[str] = None,
    include_trace: bool = False,
    llm_polish: str = "off",
    semantic_index_path: Optional[str | Path] = None,
    semantic_index: Optional[JsonDict] = None,
    semantic_provider: str = SEMANTIC_PROVIDER,
    semantic_model: str = SEMANTIC_MODEL_ID,
    semantic_dimensions: int = DEFAULT_SEMANTIC_DIMENSIONS,
    gemini_api_key: Optional[str] = None,
    semantic_axis_mode: str = "auto",
    intent_axes: Optional[Sequence[str]] = None,
    intent_steering: Optional[str] = None,
    surreal_mode_explicit: bool = False,
    semantic_defaulted: bool = False,
    intent_source: str = "user",
    requested_selection_mode: Optional[str] = None,
    batch_context: Optional[JsonDict] = None,
    batch_index: int = 0,
    additional_requirements: Optional[Sequence[str]] = None,
    likeness_mode: str = "off",
    likeness_references: Optional[Sequence[str]] = None,
    user_mandatory_intents: Optional[Sequence[str]] = None,
    concept_gate_results: Optional[Sequence[JsonDict]] = None,
    concept_scene_variants: Optional[Sequence[str]] = None,
    safety_evaluation_requested: bool = False,
    viewer_experience_requested: bool = False,
    hybrid_augmentation_requested: bool = False,
    sensual_editorial_intensity: int = 0,
    fetish_fashion_intensity: int = 0,
    adult_appeal_emphasis: str = CANDIDATE_PACK_ADULT_APPEAL_DEFAULT_EMPHASIS,
    adult_appeal_activation_source: str = "none",
    adult_appeal_candidate_pack_requested: bool = False,
    soft_anchor_spec: Optional[JsonDict] = None,
    source_argv: Optional[Sequence[str]] = None,
    seed: Optional[int] = None,
    anchor_diversity_ledger: Optional[JsonDict] = None,
    creativity: Optional[float] = None,
    novelty_explicit: bool = False,
) -> JsonDict:
    requested_selection_mode = requested_selection_mode or selection_mode
    effective_selection_mode = selection_mode
    fallback_reason: Optional[str] = None
    if intent and selection_mode == "rule":
        raise ValueError("--intent cannot be used with --selection-mode rule")
    try:
        semantic_context = make_semantic_context(
            data,
            intent,
            selection_mode,
            novelty,
            filter_strictness,
            semantic_weight,
            semantic_profile,
            semantic_index_path,
            semantic_index,
            semantic_provider,
            semantic_model,
            semantic_dimensions,
            gemini_api_key,
            semantic_axis_mode,
            intent_axes,
            intent_steering,
            intent_source,
            semantic_defaulted,
            batch_context,
            creativity=creativity,
            novelty_explicit=novelty_explicit,
        )
    except Exception as exc:
        if semantic_defaulted and selection_mode != "rule":
            fallback_reason = str(exc)
            effective_selection_mode = "rule"
            semantic_context = None
            print(f"Warning: semantic default fell back to rule mode: {fallback_reason}", file=sys.stderr)
        else:
            raise
    preset = choose_preset(data, rng, preset_id, semantic_context, soft_anchor_spec=soft_anchor_spec)
    picked: Dict[str, Entry] = {}
    generation_contract = make_generation_contract(
        data,
        preset,
        picked,
        forced_choices,
        concept_locks=concept_locks,
        additional_requirements=additional_requirements,
        likeness_mode=likeness_mode,
        likeness_references=likeness_references,
        user_mandatory_intents=user_mandatory_intents,
        concept_gate_results=concept_gate_results,
        concept_scene_variants=concept_scene_variants,
        safety_evaluation_requested=safety_evaluation_requested,
        soft_anchor_spec=soft_anchor_spec,
    )
    if semantic_context is not None and intent_source == "user":
        generation_contract["semantic_intent"] = str(semantic_context.get("intent") or "")
        generation_contract["intent_constraints"] = resolve_request_intent_constraints(
            data,
            semantic_context,
            generation_contract,
        )
    expand_soft_anchor_pools(generation_contract, semantic_context, data)
    affinity_status = soft_preset_affinity_status(
        preset,
        generation_contract.get("soft_anchor_policy"),
        data,
        forced=bool(preset_id),
    )
    if affinity_status.get("status") == "warn":
        generation_contract.setdefault("policy_conflicts", []).append(
            {
                "slot": "preset",
                "selected": preset.get("id"),
                "reason": affinity_status.get("policy_conflict"),
                "discouraged_matches": affinity_status.get("discouraged_matches", []),
            }
        )
    if semantic_context is not None:
        if anchor_diversity_ledger is not None:
            semantic_context["anchor_diversity_ledger"] = anchor_diversity_ledger
        semantic_context["generation_contract"] = generation_contract
        sync_generation_contract_axis_coverage(generation_contract, semantic_context)

    slots_to_pick = selected_slots_for_preset(preset, data, rng, forced_choices, priority_bias)
    for slot in soft_anchor_slots(generation_contract.get("soft_anchor_policy")):
        if slot in data.get("slots", {}) and slot not in slots_to_pick:
            slots_to_pick.append(slot)
    for slot in (generation_contract.get("soft_anchor_policy", {}) or {}).get("free_slot_constraints", {}) or {}:
        if slot in data.get("slots", {}) and slot not in slots_to_pick:
            slots_to_pick.append(slot)
    for slot in semantic_steering_slots(semantic_context, data):
        if slot not in slots_to_pick:
            slots_to_pick.append(slot)
            if semantic_context:
                record_intent_steering(
                    semantic_context,
                    {"slot": slot, "reason": "required_by_axis", "before": len(slots_to_pick) - 1, "after": len(slots_to_pick)},
                )
    for slot in semantic_intent_hint_slots(semantic_context, data):
        if slot not in slots_to_pick:
            slots_to_pick.append(slot)
            if semantic_context:
                record_intent_steering(
                    semantic_context,
                    {
                        "slot": slot,
                        "reason": "required_by_explicit_intent_hint",
                        "before": len(slots_to_pick) - 1,
                        "after": len(slots_to_pick),
                    },
                )

    for slot in slots_to_pick:
        entry = choose_slot(slot, data, preset, rng, picked, forced_choices, semantic_context, generation_contract)
        if entry is not None:
            picked[slot] = entry
            refresh_generation_contract(
                generation_contract,
                data,
                preset,
                picked,
                forced_choices,
                additional_requirements=additional_requirements,
                likeness_mode=likeness_mode,
                likeness_references=likeness_references,
                user_mandatory_intents=user_mandatory_intents,
                concept_gate_results=concept_gate_results,
                safety_evaluation_requested=safety_evaluation_requested,
                soft_anchor_spec=soft_anchor_spec,
            )
            sync_generation_contract_axis_coverage(generation_contract, semantic_context)

    reconcile_contract_blocked_picks(
        data, preset, rng, picked, forced_choices, semantic_context, generation_contract
    )
    apply_soft_anchor_repair(data, preset, rng, picked, forced_choices, semantic_context, generation_contract)
    refresh_generation_contract(
        generation_contract,
        data,
        preset,
        picked,
        forced_choices,
        additional_requirements=additional_requirements,
        likeness_mode=likeness_mode,
        likeness_references=likeness_references,
        user_mandatory_intents=user_mandatory_intents,
        concept_gate_results=concept_gate_results,
        safety_evaluation_requested=safety_evaluation_requested,
        soft_anchor_spec=soft_anchor_spec,
    )
    sync_generation_contract_axis_coverage(generation_contract, semantic_context)

    surreal_active = should_activate_surreal_layer(
        preset,
        rng,
        surreal_mode,
        surreal_probability,
        forced_choices,
        semantic_context,
        surreal_mode_explicit,
    )
    refresh_generation_contract(
        generation_contract,
        data,
        preset,
        picked,
        forced_choices,
        surreal_enabled=surreal_active,
        additional_requirements=additional_requirements,
        likeness_mode=likeness_mode,
        likeness_references=likeness_references,
        user_mandatory_intents=user_mandatory_intents,
        concept_gate_results=concept_gate_results,
        safety_evaluation_requested=safety_evaluation_requested,
        soft_anchor_spec=soft_anchor_spec,
    )
    sync_generation_contract_axis_coverage(generation_contract, semantic_context)
    if surreal_active:
        apply_surreal_layer(data, preset, rng, picked, forced_choices, surreal_intensity, semantic_context, generation_contract)

    apply_weak_horror_compensation(data, preset, rng, picked, forced_choices, semantic_context, generation_contract)
    apply_axis_coverage_compensation(data, preset, rng, picked, forced_choices, semantic_context, generation_contract)

    if detail_level == "detailed":
        reinforce_detail_slots(data, preset, rng, picked, forced_choices, semantic_context, generation_contract)
        sync_generation_contract_axis_coverage(generation_contract, semantic_context)

    render_picked = render_guarded_picked(data, preset, picked, generation_contract)
    directive_events = soft_render_directive_events(generation_contract.get("soft_anchor_policy"), render_picked)
    effective_additional_requirements = normalize_additional_requirements(additional_requirements)
    if directive_events:
        for event in directive_events:
            record_generation_contract_event(
                generation_contract,
                "soft_render_directive_events",
                {
                    "id": event.get("id"),
                    "cue_matched": True,
                    "matched_terms": event.get("matched_terms", []),
                    "render_as": event.get("render_as", ""),
                    "positive_clause_injected": True,
                    "suppress_terms_injected": bool(event.get("suppress_terms")),
                },
            )
            clause = str(event.get("positive_clause") or "").strip()
            if clause and clause not in effective_additional_requirements:
                effective_additional_requirements.append(clause)
        generation_contract["soft_render_directive_suppress_terms"] = [
            term
            for event in directive_events
            for term in normalize_list(event.get("suppress_terms"))
        ]
    generation_contract["additional_requirements"] = effective_additional_requirements

    result: JsonDict = {
        "preset_id": preset.get("id"),
        "preset": {lang: localize(preset, lang) for lang in langs},
    }

    for lang in langs:
        result[f"prompt_{lang}"] = render_prompt(
            data,
            preset,
            picked,
            lang,
            rng,
            detail_level,
            reference_edit_mode,
            trend_layer,
            generation_contract,
            effective_additional_requirements,
            likeness_mode,
        )

    if apply_soft_post_render_repair(
        data,
        preset,
        rng,
        picked,
        result,
        forced_choices,
        semantic_context,
        generation_contract,
    ):
        refresh_generation_contract(
            generation_contract,
            data,
            preset,
            picked,
            forced_choices,
            surreal_enabled=surreal_active,
            additional_requirements=additional_requirements,
            likeness_mode=likeness_mode,
            likeness_references=likeness_references,
            user_mandatory_intents=user_mandatory_intents,
            concept_gate_results=concept_gate_results,
            safety_evaluation_requested=safety_evaluation_requested,
            soft_anchor_spec=soft_anchor_spec,
        )
        sync_generation_contract_axis_coverage(generation_contract, semantic_context)
        render_picked = render_guarded_picked(data, preset, picked, generation_contract)
        directive_events = soft_render_directive_events(generation_contract.get("soft_anchor_policy"), render_picked)
        effective_additional_requirements = normalize_additional_requirements(additional_requirements)
        if directive_events:
            for event in directive_events:
                record_generation_contract_event(
                    generation_contract,
                    "soft_render_directive_events",
                    {
                        "id": event.get("id"),
                        "cue_matched": True,
                        "matched_terms": event.get("matched_terms", []),
                        "render_as": event.get("render_as", ""),
                        "positive_clause_injected": True,
                        "suppress_terms_injected": bool(event.get("suppress_terms")),
                    },
                )
                clause = str(event.get("positive_clause") or "").strip()
                if clause and clause not in effective_additional_requirements:
                    effective_additional_requirements.append(clause)
            generation_contract["soft_render_directive_suppress_terms"] = [
                term
                for event in directive_events
                for term in normalize_list(event.get("suppress_terms"))
            ]
        generation_contract["additional_requirements"] = effective_additional_requirements
        for lang in langs:
            result[f"prompt_{lang}"] = render_prompt(
                data,
                preset,
                picked,
                lang,
                rng,
                detail_level,
                reference_edit_mode,
                trend_layer,
                generation_contract,
                effective_additional_requirements,
                likeness_mode,
            )

    record_batch_generation(
        semantic_context,
        preset,
        render_picked,
        forced_choices=forced_choices,
        preset_forced=bool(preset_id),
    )

    if llm_polish == "strict":
        for lang in langs:
            result[f"polished_prompt_{lang}"] = result[f"prompt_{lang}"]
        result["rewrite_trace"] = {
            "mode": "strict",
            "status": "preserved",
            "provider": "none",
            "fallback": False,
            "preserved_anchors": [
                f"{slot}:{entry.get('id')}"
                for slot, entry in picked.items()
                if entry.get("anchor") or slot in {"subject", "location", "lens", "lighting", "format"}
            ],
        }

    if include_negative:
        negative_entries = choose_negative_entries(
            data,
            rng,
            negative_count,
            has_surreal_layer(render_picked),
            render_picked,
        )
        soft_suppress_entries = soft_render_suppress_negative_entries(generation_contract.get("soft_anchor_policy"))
        soft_suppress_entries.extend(soft_render_directive_negative_entries(directive_events))
        if soft_suppress_entries:
            existing = {localize(entry, "en").lower() for entry in negative_entries}
            for entry in soft_suppress_entries:
                if localize(entry, "en").lower() not in existing:
                    negative_entries.append(entry)
                    existing.add(localize(entry, "en").lower())
            generation_contract["soft_render_suppress_terms"] = [localize(entry, "en") for entry in soft_suppress_entries]
        for lang in langs:
            result[f"negative_{lang}"] = render_negative_prompt(negative_entries, lang)

    result["quality"] = evaluate_generation_quality(generation_contract, render_picked, result, semantic_context)

    prompt_for_id = result.get("prompt_en") or next((result.get(f"prompt_{lang}") for lang in langs if result.get(f"prompt_{lang}")), "")
    negative_for_id = result.get("negative_en") if include_negative else None
    result["provenance"] = {
        "generator_version": GENERATOR_VERSION,
        "prompt_id": stable_text_id(prompt_for_id) or "",
        "negative_id": stable_text_id(negative_for_id),
        "seed": seed,
        "batch_index": batch_index,
        "preset_id": preset.get("id"),
        "selection_mode": effective_selection_mode,
        "requested_selection_mode": requested_selection_mode,
        "tags_hash": (semantic_context or {}).get("dictionary_hash"),
        "concept_lock": normalize_concept_locks(concept_locks),
        "additional_requirements": effective_additional_requirements,
        "likeness_mode": likeness_mode,
        "likeness_references": normalize_list(likeness_references),
        "user_mandatory_intents": normalize_list(user_mandatory_intents),
        "concept_gate_results": [
            dict(item) for item in concept_gate_results or [] if isinstance(item, dict)
        ],
        "concept_scene_variants": normalize_list(concept_scene_variants),
        "safety": generation_contract.get("safety", {}),
        "viewer_experience_requested": bool(viewer_experience_requested),
        "hybrid_augmentation_requested": bool(hybrid_augmentation_requested),
        "adult_appeal": {
            "enabled": bool(
                adult_appeal_candidate_pack_requested
                and (sensual_editorial_intensity > 0 or fetish_fashion_intensity > 0)
            ),
            "configured": bool(
                sensual_editorial_intensity > 0 or fetish_fashion_intensity > 0
            ),
            "application_scope": "candidate_pack_composition",
            "activation_source": adult_appeal_activation_source
            if sensual_editorial_intensity > 0 or fetish_fashion_intensity > 0
            else "explicit_opt_out",
            "axes": {
                "sensual_editorial": {"intensity": int(sensual_editorial_intensity)},
                "fetish_fashion": {"intensity": int(fetish_fashion_intensity)},
            },
            "blend": {"emphasis": adult_appeal_emphasis},
        },
        "creativity": creativity if creativity is not None else (semantic_context or {}).get("creativity"),
        "argv": list(source_argv or []),
    }

    if include_choices:
        result["choices"] = {
            slot: {
                "id": entry.get("id"),
                "ko": localize(entry, "ko"),
                "en": localize(entry, "en"),
                "tags": entry.get("tags", []),
                "kind": entry.get("kind", []),
            }
            for slot, entry in picked.items()
        }

    if include_trace and semantic_context:
        result["semantic_trace"] = {
            "selection_mode": effective_selection_mode,
            "requested_selection_mode": requested_selection_mode,
            "intent": intent,
            "intent_source": semantic_context.get("intent_source", intent_source),
            "semantic_defaulted": bool(semantic_context.get("semantic_defaulted", semantic_defaulted)),
            "novelty": novelty,
            "filter_strictness": semantic_context.get("filter_strictness"),
            "semantic_weight": semantic_context.get("semantic_weight"),
            "semantic_profile": semantic_context.get("semantic_profile"),
            "semantic_axis_mode": semantic_context.get("semantic_axis_mode"),
            "intent_axes": semantic_context.get("intent_axes"),
            "intent_steering": semantic_context.get("intent_steering"),
            "generation_contract": generation_contract,
            "soft_anchor_policy": generation_contract.get("soft_anchor_policy", {}),
            "soft_anchor_repair": generation_contract.get("soft_anchor_repair", {}),
            "axis_coverage": semantic_axis_coverage_trace(semantic_context),
            "semantic_groups": selected_semantic_metadata_summary(picked, semantic_context),
            "coherence_scope": {
                "family_conflicts": sorted((semantic_context.get("coherence_rules", {}).get("family_conflicts", {}) or {}).keys()),
                "tone_conflicts": sorted((semantic_context.get("semantic_metadata", {}).get("family_tone_conflicts", {}) or {}).keys()),
            },
            "weak_horror_compensation": semantic_context.get("weak_horror_compensation", {"status": "not_evaluated"}),
            "surreal_activation_reason": semantic_context.get("surreal_activation_reason"),
            "surreal_activation_active": semantic_context.get("surreal_activation_active"),
            "dictionary_hash": semantic_context.get("dictionary_hash"),
            "policy_schema_version": semantic_context.get("policy_schema_version"),
            "semantic_policy_hash": semantic_context.get("semantic_policy_hash"),
            "semantic_text_recipe": semantic_context.get("semantic_text_recipe"),
            "embedding_provider": semantic_context.get("embedding_provider"),
            "embedding_model": semantic_context.get("embedding_model"),
            "embedding_dimensions": semantic_context.get("embedding_dimensions"),
            "hard_rejected_count": semantic_context.get("hard_rejected_count", 0),
            "hard_rejected": semantic_context.get("hard_rejected", []),
            "soft_out_of_filter_selected_count": semantic_context.get("soft_out_of_filter_selected_count", 0),
            "preset_score": semantic_context.get("preset_score"),
            "slot_scores": semantic_context.get("slot_scores", []),
            "batch_index": batch_index,
            "batch_diversity": {
                "enabled": bool((semantic_context.get("batch_context") or {}).get("enabled")),
                "tracked_scopes": list(BATCH_DIVERSITY_TRACKED_SCOPES),
                "novelty": novelty,
            },
            "batch_group_diversity": {
                "enabled": bool((semantic_context.get("batch_context") or {}).get("enabled")),
                "tracked_scopes": ["subject_group", "location_tone", "lighting"],
                "counts": {
                    scope: dict(((semantic_context.get("batch_context") or {}).get("counts", {}) or {}).get(scope, {}))
                    for scope in ("subject_group", "location_tone", "lighting")
                },
            },
            "batch_repetition_penalty": semantic_context.get("batch_repetition_penalty", []),
            "batch_history_summary": batch_history_summary(semantic_context.get("batch_context")),
            "anchor_diversity_ledger_summary": anchor_diversity_ledger_summary(
                semantic_context.get("anchor_diversity_ledger")
            ),
        }
    elif include_trace:
        result["semantic_trace"] = {
            "selection_mode": effective_selection_mode,
            "requested_selection_mode": requested_selection_mode,
            "intent": intent,
            "intent_source": intent_source,
            "semantic_defaulted": semantic_defaulted,
            "fallback_reason": fallback_reason,
            "novelty": novelty,
            "filter_strictness": filter_strictness,
            "semantic_weight": semantic_weight,
            "semantic_profile": semantic_profile,
            "semantic_axis_mode": semantic_axis_mode,
            "intent_axes": {"mode": semantic_axis_mode, "source": "none", "items": []},
            "intent_steering": {"mode": intent_steering or "off", "enabled": False, "families": [], "decisions": []},
            "generation_contract": generation_contract,
            "axis_coverage": {"target": 0.0, "items": []},
            "semantic_groups": {},
            "coherence_scope": {"family_conflicts": [], "tone_conflicts": []},
            "weak_horror_compensation": {"status": "not_evaluated"},
            "surreal_activation_reason": "none",
            "surreal_activation_active": False,
            "policy_schema_version": None,
            "semantic_policy_hash": None,
            "slot_scores": [],
            "batch_index": batch_index,
            "batch_diversity": {
                "enabled": bool((batch_context or {}).get("enabled")),
                "tracked_scopes": list(BATCH_DIVERSITY_TRACKED_SCOPES),
                "novelty": novelty,
            },
            "batch_group_diversity": {
                "enabled": bool((batch_context or {}).get("enabled")),
                "tracked_scopes": ["subject_group", "location_tone", "lighting"],
                "counts": {},
            },
            "batch_repetition_penalty": [],
            "batch_history_summary": batch_history_summary(batch_context),
            "anchor_diversity_ledger_summary": anchor_diversity_ledger_summary(anchor_diversity_ledger),
        }

    return result


# -----------------------------------------------------------------------------
# CLI utilities
# -----------------------------------------------------------------------------

def parse_langs(lang: str) -> List[str]:
    if lang == "both":
        return ["ko", "en"]
    if lang in {"ko", "en"}:
        return [lang]
    raise ValueError("--lang must be one of: ko, en, both")


def print_plain(results: Sequence[JsonDict], langs: Sequence[str], include_negative: bool, include_choices: bool) -> None:
    for i, item in enumerate(results, start=1):
        print(f"\n[{i}] preset: {item.get('preset_id')}")
        for lang in langs:
            label = "KO" if lang == "ko" else "EN"
            print(f"{label}: {item.get(f'prompt_{lang}', '')}")
            if include_negative and item.get(f"negative_{lang}"):
                print(f"{label} negative: {item[f'negative_{lang}']}")
        if include_choices and item.get("choices"):
            compact = {slot: choice.get("id") for slot, choice in item["choices"].items()}
            print("choices:", json.dumps(compact, ensure_ascii=False))


def list_presets(data: JsonDict, include_virtual: bool = False) -> None:
    for p in data.get("presets", []):
        ko = localize(p, "ko")
        en = localize(p, "en")
        print(f"{p.get('id')}: {ko} / {en}")
    if include_virtual:
        for recipe in data.get("recipes", []):
            ko = localize(recipe, "ko")
            en = localize(recipe, "en")
            print(f"virtual:{recipe.get('id')}: {ko} / {en}")


def show_slots(data: JsonDict) -> None:
    priorities = get_slot_priorities(data)
    for slot, entries in data.get("slots", {}).items():
        priority = priorities.get(slot, 0)
        print(f"{slot}: {len(entries)} tags, priority={priority:g}")


def list_tags(data: JsonDict, slot: str) -> None:
    slots = data.get("slots", {})
    if slot not in slots:
        valid = ", ".join(slots.keys())
        raise ValueError(f"Unknown slot '{slot}'. Available slots: {valid}")
    for item in slots[slot]:
        print(f"{item.get('id')}: {localize(item, 'ko')} / {localize(item, 'en')}")


def main(argv: Optional[Sequence[str]] = None) -> int:
    raw_args = list(argv or sys.argv[1:])
    parser = argparse.ArgumentParser(description="Random photo prompt generator using JSON-managed tags.")
    parser.add_argument("--tags", default="photo_prompt_tags.json", help="Path to tag JSON file.")
    parser.add_argument("--quality-layers", default=None, help=argparse.SUPPRESS)
    parser.add_argument("--lang", choices=["ko", "en", "both"], default="both", help="Output language.")
    parser.add_argument("--n", type=int, default=5, help="Number of prompts to generate.")
    parser.add_argument("--preset", default=None, help="Preset id. Omit for random preset.")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducible output.")
    parser.add_argument(
        "--detail-level",
        choices=["standard", "detailed", "compact"],
        default="standard",
        help="Prompt rendering detail level. Use detailed for a longer image-ready prompt or compact for a ReactorPrompt-style single paragraph.",
    )
    parser.add_argument("--surreal-mode", choices=["off", "auto", "on"], default="off", help="Apply a photoreal surreal layer: off disables it, auto applies by probability, on always applies it.")
    parser.add_argument("--surreal-probability", type=float, default=0.35, help="Probability for --surreal-mode auto. Clamped to 0..1.")
    parser.add_argument("--surreal-intensity", choices=["subtle", "moderate", "bold"], default="moderate", help="How many surreal layer slots to add when the layer is active.")
    parser.add_argument("--reference-edit-mode", choices=REFERENCE_EDIT_MODES, default="off", help="Append reference-image editing instructions for uploaded-photo workflows.")
    parser.add_argument("--trend-layer", choices=TREND_LAYERS, default="off", help="Append a social trend layout layer without changing the base photo preset.")
    parser.add_argument("--intent", default=None, help="Free-text visual intent for semantic selection. A broad photo intent is used when semantic/hybrid mode has no explicit intent.")
    parser.add_argument(
        "--concept-lock",
        dest="concept_locks",
        action="append",
        default=[],
        help="Verbatim core concept to keep visually dominant while generated slots add supporting detail. Repeatable.",
    )
    parser.add_argument(
        "--additional-requirement",
        dest="additional_requirements",
        action="append",
        default=[],
        help="Concrete requirement not represented by tags. Repeatable; rendered into the final prompt before prompt_id is computed.",
    )
    parser.add_argument(
        "--likeness-mode",
        choices=LIKENESS_MODES,
        default="off",
        help="Prompt-level real-person likeness handling. Use inspired for an original fictional person inspired by styling/vibe.",
    )
    parser.add_argument("--likeness-reference", dest="likeness_references", action="append", default=[], help=argparse.SUPPRESS)
    parser.add_argument("--user-mandatory-intent", dest="user_mandatory_intents", action="append", default=[], help=argparse.SUPPRESS)
    parser.add_argument("--concept-gates-json", dest="concept_gate_payloads", action="append", default=[], help=argparse.SUPPRESS)
    parser.add_argument("--concept-scene-variant", dest="concept_scene_variants", action="append", default=[], help=argparse.SUPPRESS)
    parser.add_argument(
        "--safety-evaluation",
        action="store_true",
        help="Explicitly include a safety evaluation report. Normal generation uses a simple automatic-pass safety contract.",
    )
    parser.add_argument(
        "--viewer-experience",
        action="store_true",
        help="Expose a topic-neutral viewer-experience composition contract for explicit audience, affect, attachment, commercial, or subculture-response goals. High creative-direction runs include it automatically.",
    )
    parser.add_argument(
        "--hybrid-augmentation",
        action="store_true",
        help="Expose three candidate-sourced idea-augmentation routes while preserving an agent-authored concept core. High creative-direction and adult-appeal runs enable it automatically.",
    )
    parser.add_argument(
        "--sensual-editorial-intensity",
        type=int,
        default=CANDIDATE_PACK_SENSUAL_EDITORIAL_DEFAULT_INTENSITY,
        help="Adult sensual-editorial styling axis intensity from 0 to 3; defaults to 1 for eligible human candidate packs. Use 0 to disable this axis.",
    )
    parser.add_argument(
        "--fetish-fashion-intensity",
        type=int,
        default=CANDIDATE_PACK_FETISH_FASHION_DEFAULT_INTENSITY,
        help="Adult fetish-fashion styling axis intensity from 0 to 3; defaults to 0 and requires explicit opt-in.",
    )
    parser.add_argument(
        "--adult-appeal-emphasis",
        choices=CANDIDATE_PACK_ADULT_APPEAL_EMPHASES,
        default=None,
        help="Blend emphasis when one or both adult-appeal axes are active. Equal default intensities resolve to balanced.",
    )
    parser.add_argument("--selection-mode", choices=SELECTION_MODES, default=DEFAULT_SELECTION_MODE, help="Selection mode. semantic is the default; use rule for the original deterministic weighted path.")
    parser.add_argument("--default-intent", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--semantic-default", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--novelty", choices=NOVELTY_LEVELS, default="medium", help="Semantic sampling diversity level. Used only with semantic or hybrid selection.")
    parser.add_argument("--creativity", type=float, default=None, help="Single 0..1 creativity control: 0 maps to conservative/low-novelty, 0.5 to balanced exploration, and 0.75..1 adds a creative-direction composition contract alongside exploratory candidate breadth. Explicit --novelty or --semantic-profile values win over the corresponding diversity settings. Coherence controls (semantic weight, filter strictness) are not affected.")
    parser.add_argument(
        "--scene-function",
        default=None,
        help="Select one supported render scene function for a direct research-backed preset without adding user intent text.",
    )
    parser.add_argument("--filter-strictness", choices=FILTER_STRICTNESS_MODES, default=None, help="Preset filter behavior for semantic/hybrid selection. Defaults to soft for semantic and hard for hybrid/rule.")
    parser.add_argument("--semantic-weight", type=float, default=None, help="0..1 blend weight for semantic scoring. Defaults by selection mode.")
    parser.add_argument("--semantic-profile", choices=SEMANTIC_PROFILES, default=None, help="Semantic candidate window/profile. Defaults by selection mode.")
    parser.add_argument("--semantic-axis-mode", choices=SEMANTIC_AXIS_MODES, default="auto", help="Intent-axis decomposition for semantic preset scoring. Use off to keep a single intent axis.")
    parser.add_argument("--intent-axis", dest="intent_axes", action="append", default=[], help="Explicit semantic intent axis. Repeat to replace automatic axis extraction.")
    parser.add_argument("--intent-steering", choices=INTENT_STEERING_MODES, default=None, help="Semantic axis-based slot steering. Defaults to auto for semantic/hybrid and off for rule.")
    parser.add_argument("--semantic-index", default=None, help="Path to a precomputed semantic index JSON. Defaults to a sibling asset when present.")
    parser.add_argument("--semantic-model", default=SEMANTIC_MODEL_ID, help="Gemini embedding model required by the semantic index.")
    parser.add_argument("--semantic-dimensions", type=int, default=DEFAULT_SEMANTIC_DIMENSIONS, help="Gemini embedding dimensions required by the semantic index.")
    parser.add_argument("--soft-anchor-spec", dest="soft_anchor_specs", action="append", default=[], help=argparse.SUPPRESS)
    parser.add_argument("--soft-requirement", dest="soft_requirements", action="append", default=[], help=argparse.SUPPRESS)
    parser.add_argument("--anchor-diversity-ledger", default=None, help=argparse.SUPPRESS)
    parser.add_argument("--include-trace", action="store_true", help="Include semantic/rewrite trace metadata in JSON output.")
    parser.add_argument("--llm-polish", choices=LLM_POLISH_MODES, default="off", help="Optional strict prompt polish contract. strict currently preserves the deterministic prompt unless a provider is wired explicitly.")
    parser.add_argument("--priority-bias", type=float, default=None, help="Optional-slot priority boost. Omit to use JSON setting.")
    parser.add_argument("--set", dest="set_values", action="append", default=[], help="Force a slot id, e.g. --set subject=fashion_model. Repeatable. Use commas to randomly choose among ids.")
    parser.add_argument("--set-json", default=None, help="Inline JSON or path to JSON file for forced slots, e.g. '{\"subject\":\"fashion_model\"}'.")
    parser.add_argument("--include-negative", action="store_true", help="Also output a negative prompt.")
    parser.add_argument("--negative-count", type=int, default=12, help="Number of negative tags to sample.")
    parser.add_argument("--include-choices", action="store_true", help="Include chosen slot details in plain or JSON output.")
    parser.add_argument(
        "--emit-candidate-pack",
        action="store_true",
        help="Emit candidate-pack JSON for agent composition instead of final prompt JSON/plain text.",
    )
    parser.add_argument("--json-output", action="store_true", help="Print results as JSON.")
    parser.add_argument(
        "--output-file",
        default=None,
        help="Write the exact generated output bytes to this file instead of stdout.",
    )
    parser.add_argument("--list-presets", action="store_true", help="List preset ids and exit.")
    parser.add_argument("--include-virtual", action="store_true", help="Include virtual recipe presets when listing presets.")
    parser.add_argument("--show-slots", action="store_true", help="List slots, tag counts, and priorities then exit.")
    parser.add_argument("--list-tags", metavar="SLOT", help="List tag ids for a slot then exit.")
    args = parser.parse_args(raw_args)

    for option_name, value in (
        ("--sensual-editorial-intensity", args.sensual_editorial_intensity),
        ("--fetish-fashion-intensity", args.fetish_fashion_intensity),
    ):
        if value < 0 or value > 3:
            raise ValueError(f"{option_name} must be between 0 and 3")
    adult_appeal_enabled = bool(
        args.sensual_editorial_intensity > 0 or args.fetish_fashion_intensity > 0
    )
    explicit_adult_control = any(
        has_cli_option(raw_args, option)
        for option in (
            "--sensual-editorial-intensity",
            "--fetish-fashion-intensity",
            "--adult-appeal-emphasis",
        )
    )
    if (args.hybrid_augmentation or explicit_adult_control) and not args.emit_candidate_pack:
        raise ValueError(
            "--hybrid-augmentation and explicit adult-appeal controls require --emit-candidate-pack"
        )
    if args.adult_appeal_emphasis and not adult_appeal_enabled:
        raise ValueError("--adult-appeal-emphasis requires an active adult-appeal axis")
    if args.adult_appeal_emphasis:
        adult_appeal_emphasis = args.adult_appeal_emphasis
    elif args.sensual_editorial_intensity == args.fetish_fashion_intensity:
        adult_appeal_emphasis = "balanced"
    elif args.sensual_editorial_intensity > args.fetish_fashion_intensity:
        adult_appeal_emphasis = "sensual_led"
    else:
        adult_appeal_emphasis = "fetish_led"
    if adult_appeal_enabled:
        if adult_appeal_emphasis == "sensual_led" and args.sensual_editorial_intensity == 0:
            raise ValueError("sensual_led emphasis requires sensual_editorial intensity above 0")
        if adult_appeal_emphasis == "fetish_led" and args.fetish_fashion_intensity == 0:
            raise ValueError("fetish_led emphasis requires fetish_fashion intensity above 0")
        if adult_appeal_emphasis == "balanced" and (
            args.sensual_editorial_intensity == 0 or args.fetish_fashion_intensity == 0
        ):
            raise ValueError("balanced adult appeal requires both axes above 0")
    adult_appeal_activation_source = (
        "explicit_user_control" if explicit_adult_control else "skill_default"
    )

    data = load_json(args.tags)
    quality_layers_path = Path(args.quality_layers) if args.quality_layers else default_quality_layers_path(args.tags)
    data[QUALITY_LAYERS_DATA_KEY] = load_quality_layers(quality_layers_path)
    available_scene_functions = set(
        normalize_list((data.get("facet_vocab") or {}).get("scene_function"))
    )
    for preset in data.get("presets", []):
        for blueprint in render_contract_resolved_scene_blueprints(data, preset):
            available_scene_functions.update(
                normalize_list(blueprint.get("scene_functions"))
            )
    if args.scene_function and args.scene_function not in available_scene_functions:
        raise ValueError(
            f"Unknown --scene-function {args.scene_function!r}; available values: "
            + ", ".join(sorted(available_scene_functions))
        )
    if args.scene_function and not args.preset:
        raise ValueError("--scene-function requires an explicit --preset")

    if args.list_presets:
        list_presets(data, args.include_virtual)
        return 0
    if args.show_slots:
        show_slots(data)
        return 0
    if args.list_tags:
        list_tags(data, args.list_tags)
        return 0

    rng = random.Random(args.seed)
    langs = parse_langs(args.lang)
    forced_choices = merge_forced_choices(
        parse_forced_choices(args.set_values),
        load_forced_choices_from_json(args.set_json),
    )
    soft_anchor_spec = parse_soft_anchor_specs(args.soft_anchor_specs)
    concept_gate_results = parse_json_object_list(args.concept_gate_payloads, "--concept-gates-json")
    effective_additional_requirements = list(args.additional_requirements)
    effective_additional_requirements.extend(
        f"Soft visual guidance: {requirement}"
        for requirement in args.soft_requirements
        if str(requirement).strip()
    )

    if args.n < 1:
        raise ValueError("--n must be at least 1")

    selection_mode = args.selection_mode
    selection_mode_explicit = has_cli_option(raw_args, "--selection-mode")
    intent_explicit = has_cli_option(raw_args, "--intent")
    intent_axis_explicit = bool(args.intent_axes)
    resolved_intent = args.intent
    if args.intent and selection_mode == "rule":
        raise ValueError("--intent cannot be used with --selection-mode rule")
    semantic_defaulted = bool(
        args.semantic_default
        or (
            selection_mode == DEFAULT_SELECTION_MODE
            and not selection_mode_explicit
            and not intent_explicit
            and not intent_axis_explicit
        )
    )
    intent_source = "user"
    if selection_mode != "rule" and not resolved_intent:
        resolved_intent = DEFAULT_SEMANTIC_INTENT
        intent_source = "default"
    elif selection_mode != "rule" and resolved_intent == DEFAULT_SEMANTIC_INTENT and (args.default_intent or semantic_defaulted or not intent_explicit):
        intent_source = "default"
    filter_strictness, semantic_weight, semantic_profile = resolve_semantic_runtime_options(
        selection_mode,
        args.filter_strictness,
        args.semantic_weight,
        args.semantic_profile,
    )

    semantic_index_path = args.semantic_index
    if selection_mode != "rule" and semantic_index_path is None:
        candidate = Path(args.tags).resolve().with_name("photo_prompt_semantic_index.json")
        if candidate.exists():
            semantic_index_path = str(candidate)

    if args.creativity is not None and not 0.0 <= args.creativity <= 1.0:
        raise ValueError("--creativity must be between 0 and 1")
    novelty_explicit = has_cli_option(raw_args, "--novelty")
    batch_context = make_batch_context(
        selection_mode,
        args.novelty,
        args.n,
        source=data,
        creativity=None if novelty_explicit else args.creativity,
    )
    anchor_diversity_ledger = load_anchor_diversity_ledger(args.anchor_diversity_ledger)
    results = []
    for batch_index in range(args.n):
        set_batch_index(batch_context, batch_index)
        result = generate_once(
            data=data,
            rng=rng,
            preset_id=args.preset,
            langs=langs,
            include_negative=args.include_negative or args.emit_candidate_pack,
            negative_count=args.negative_count,
            include_choices=args.include_choices or args.emit_candidate_pack,
            forced_choices=forced_choices,
            priority_bias=args.priority_bias,
            detail_level=args.detail_level,
            surreal_mode=args.surreal_mode,
            surreal_probability=args.surreal_probability,
            surreal_intensity=args.surreal_intensity,
            reference_edit_mode=args.reference_edit_mode,
            trend_layer=args.trend_layer,
            intent=resolved_intent,
            concept_locks=args.concept_locks,
            selection_mode=selection_mode,
            novelty=args.novelty,
            filter_strictness=filter_strictness,
            semantic_weight=semantic_weight,
            semantic_profile=semantic_profile,
            semantic_axis_mode=args.semantic_axis_mode,
            intent_axes=args.intent_axes,
            intent_steering=args.intent_steering,
            surreal_mode_explicit=has_cli_option(raw_args, "--surreal-mode"),
            semantic_defaulted=semantic_defaulted,
            intent_source=intent_source,
            requested_selection_mode=selection_mode,
            batch_context=batch_context,
            batch_index=batch_index,
            include_trace=args.include_trace or args.emit_candidate_pack,
            llm_polish=args.llm_polish,
            semantic_index_path=semantic_index_path,
            semantic_model=args.semantic_model,
            semantic_dimensions=args.semantic_dimensions,
            additional_requirements=effective_additional_requirements,
            likeness_mode=args.likeness_mode,
            likeness_references=args.likeness_references,
            user_mandatory_intents=args.user_mandatory_intents,
            concept_gate_results=concept_gate_results,
            concept_scene_variants=args.concept_scene_variants,
            safety_evaluation_requested=args.safety_evaluation,
            viewer_experience_requested=args.viewer_experience,
            hybrid_augmentation_requested=args.hybrid_augmentation,
            sensual_editorial_intensity=args.sensual_editorial_intensity,
            fetish_fashion_intensity=args.fetish_fashion_intensity,
            adult_appeal_emphasis=adult_appeal_emphasis,
            adult_appeal_activation_source=adult_appeal_activation_source,
            adult_appeal_candidate_pack_requested=args.emit_candidate_pack,
            soft_anchor_spec=soft_anchor_spec,
            source_argv=raw_args,
            seed=args.seed,
            anchor_diversity_ledger=anchor_diversity_ledger if args.anchor_diversity_ledger else None,
            creativity=args.creativity,
            novelty_explicit=novelty_explicit,
        )
        if args.scene_function:
            result.setdefault("provenance", {})["requested_scene_function"] = args.scene_function
        results.append(result)
        if args.anchor_diversity_ledger:
            update_anchor_diversity_ledger(anchor_diversity_ledger, result)
    if args.anchor_diversity_ledger:
        save_anchor_diversity_ledger(args.anchor_diversity_ledger, anchor_diversity_ledger)

    if args.emit_candidate_pack:
        packs = [build_candidate_pack(result, data) for result in results]
        output = json.dumps(packs, ensure_ascii=False, indent=2) + "\n"
        if args.output_file:
            Path(args.output_file).write_text(output, encoding="utf-8")
        else:
            print(output, end="")
    elif args.json_output:
        output = json.dumps(results, ensure_ascii=False, indent=2) + "\n"
        if args.output_file:
            Path(args.output_file).write_text(output, encoding="utf-8")
        else:
            print(output, end="")
    else:
        if args.output_file:
            raise ValueError("--output-file requires --json-output or --emit-candidate-pack")
        print_plain(results, langs, args.include_negative, args.include_choices)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
