#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Photo prompt generator
- Tags are managed in a JSON file.
- A frozen authorial core owns the scene; all retrieved candidates are optional.
- The public entrypoint is generate_photo_prompt.py.
"""

from __future__ import annotations

import argparse
import copy
import functools
import hashlib
import json
import math
import os
import random
import re
import secrets
import sys
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Set

_SCRIPTS_IMPORT_DIR = str(Path(__file__).resolve().parent)
_SCRIPTS_IMPORT_DIR_ADDED = _SCRIPTS_IMPORT_DIR not in sys.path
if _SCRIPTS_IMPORT_DIR_ADDED:
    sys.path.insert(0, _SCRIPTS_IMPORT_DIR)
try:
    import photo_camera_evidence
    import photo_candidate_semantics
    import photo_contextual_appeal
    import photo_embodiment
    import photo_creative_controls as creative_controls
    from visual_profile_contracts import (
        compile_visual_profile,
        hard_activation_is_supported,
    )
    from photo_contracts import (
        ADULT_APPEAL_AXIS_DIMENSIONS,
        ADULT_APPEAL_DIMENSION_SCOPE_CONTRACT_VERSION,
        AUTHORIAL_AUTHORSHIP_POLICY_CONTRACT_VERSION,
        AUTHORIAL_CORE_BINDING_CONTRACT_VERSION,
        AUTHORIAL_CORE_CONTRACT_VERSION,
        AUTHORIAL_CORE_MODERN_CONTRACT_VERSIONS,
        AUTHORIAL_CORE_V3_CONTRACT_VERSION,
        AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS,
        AUTHORIAL_IDENTITY_PRESERVATION_NEGATIVE_TERMS,
        AUTHORIAL_INTENT_NEUTRAL_NEGATIVE_TERMS,
        AUTHORIAL_PROMPT_ABSOLUTE_MAX_WORDS,
        AUTHORIAL_PROMPT_BUDGET_CONTRACT_VERSION,
        AUTHORIAL_PROMPT_MIN_WORDS,
        AUTHORIAL_PROMPT_RECOMMENDED_MAX_WORDS,
        AUTHORIAL_PROMPT_REQUIRED_EVIDENCE_HEADROOM_WORDS,
        CHARACTER_RESPONSE_CONTRACT_VERSION,
        CHARACTER_RESPONSE_RELATION_MEMBERS,
        CHARACTER_RESPONSE_REQUIRED_AXES,
        CHARACTER_RESPONSE_REQUIRED_EVIDENCE,
        DOWNSTREAM_INTENT_PRECEDENCE_CONTRACT_VERSION,
        INTENT_LOCK_CONTRACT_VERSION,
        INTENT_LOCK_PROPERTY_CONTRACT_VERSION,
        intent_property_locks,
        authored_subject_category,
        property_effects_allowed,
        INTENT_LOCK_DIMENSIONS,
        INTENT_PRESERVATION_CONTRACT_VERSION,
        NEGATIVE_INTENT_GUARD_CONTRACT_VERSION,
        RENDER_REPAIR_ALLOWED_AXES,
        RENDER_REPAIR_CONTACT_EXPECTATIONS,
        RENDER_REPAIR_CONTRACT_VERSION,
        RENDER_REPAIR_DIMENSION_AXES,
        RENDER_REPAIR_IMPORTANCE_VALUES,
        RENDER_REPAIR_INTERACTION_STATES,
        RENDER_REPAIR_RELATION_ORIGINS,
        REQUEST_BINDING_CONTRACT_VERSION,
        REQUEST_ENVELOPE_CONTRACT_VERSION,
        REQUEST_LINEAGE_V2_CONTRACT_VERSION,
        REQUIRED_INTENT_LOCK_DIMENSIONS,
        SEMANTIC_ASSERTION_OBLIGATIONS_CONTRACT_VERSION,
        canonical_json_sha256,
    )
    from photo_visual_retrieval import (
        positive_visual_profile_fields,
        positive_visual_profile_text,
    )
    from bm25f_retrieval import (
        build_bm25f_index,
        normalize_bm25f_text,
        rank_bm25f,
        reciprocal_rank_fusion,
        tokenize_bm25f_text,
        validate_bm25f_index,
    )
finally:
    if _SCRIPTS_IMPORT_DIR_ADDED:
        sys.path.remove(_SCRIPTS_IMPORT_DIR)

JsonDict = Dict[str, Any]
Entry = Dict[str, Any]


# Internal candidate breadth only; the pre-core definition owns visual prominence.

SEMANTIC_PROVIDER = "gemini"
DEFAULT_SEMANTIC_DIMENSIONS = 768
SEMANTIC_MODEL_ID = "gemini-embedding-2"
SEMANTIC_TEXT_RECIPE_VERSION = "semantic-text-v5"
SEMANTIC_BM25F_POLICY_VERSION = "photo-semantic-bm25f-policy/v3"
VISUAL_PROFILE_BM25F_POLICY_VERSION = "photo-visual-profile-bm25f-policy/v2"
GENERATOR_VERSION = "2026.10.1"
QUALITY_LAYERS_FILENAME = "photo_prompt_quality_layers.json"
VISUAL_OBLIGATION_REGISTRY_FILENAME = "photo_prompt_visual_obligations.json"
VISUAL_PROFILE_INDEX_FILENAME = "photo_prompt_visual_profile_index.json"
VISUAL_OBLIGATION_EXTENSION_FILENAMES = (
    "photo_prompt_visual_obligations_tactile_reality.json",
    "photo_prompt_visual_obligations_reactorprompt.json",
    "photo_prompt_visual_obligations_photo_era.json",
    "photo_prompt_visual_obligations_poverty.json",
    "photo_prompt_visual_obligations_opening_era.json",
    "photo_prompt_visual_obligations_historical_womenswear.json",
    "photo_prompt_visual_obligations_costume_cosplay.json",
    "photo_prompt_visual_obligations_palace_fortification.json",
    "photo_prompt_visual_obligations_swimwear.json",
    "photo_prompt_visual_obligations_color_relations.json",
    "photo_prompt_visual_obligations_model_editorial.json",
    "photo_prompt_visual_obligations_realistic_background.json",
    "photo_prompt_visual_obligations_photorealism_elements.json",
    "photo_prompt_visual_obligations_everyday_scene.json",
    "photo_prompt_visual_obligations_y2k.json",
    "photo_prompt_visual_obligations_portrait_composition.json",
    "photo_prompt_visual_obligations_portrait_fashion_exposure.json",
    "photo_prompt_visual_obligations_editing_effects.json",
    "photo_prompt_visual_obligations_motion_graphics.json",
    "photo_prompt_visual_obligations_clothing_structure.json",
    "photo_prompt_visual_obligations_textile_surface.json",
    "photo_prompt_visual_obligations_accessory_structure.json",
    "photo_prompt_visual_obligations_traditional_clothing_detail.json",
    "photo_prompt_visual_obligations_pose_vocabulary.json",
    "photo_prompt_visual_obligations_body_morphology.json",
    "photo_prompt_visual_obligations_acting_expression.json",
    "photo_prompt_visual_obligations_neutral_expression.json",
    "photo_prompt_visual_obligations_slang_visual.json",
    "photo_prompt_visual_obligations_religion_iconography.json",
    "photo_prompt_visual_obligations_subculture_appearance.json",
    "photo_prompt_visual_obligations_character_appearance.json",
    "photo_prompt_visual_obligations_seduction_expression.json",
)
VISUAL_OBLIGATION_EXTENSION_SCHEMA_VERSION = (
    "photo-visual-obligation-registry-extension/v1"
)
VISUAL_RELATION_CONTRACT_VERSION = "photo-visual-relation/v1"
RESEARCH_EXTENSION_FILENAME = "photo_prompt_research_extension.json"
RESEARCH_EXTENSION_FILENAMES = (
    "photo_prompt_clothing_structure_extension.json",
    "photo_prompt_textile_surface_extension.json",
    "photo_prompt_accessory_structure_extension.json",
    "photo_prompt_traditional_clothing_detail_extension.json",
    "photo_prompt_tactile_reality_extension.json",
    RESEARCH_EXTENSION_FILENAME,
    "photo_prompt_reactorprompt_visual_relations_extension.json",
    "photo_prompt_natural_environment_extension.json",
    "photo_prompt_imaginal_extension.json",
    "photo_prompt_mythology_extension.json",
    "photo_prompt_legend_extension.json",
    "photo_prompt_space_extension.json",
    "photo_prompt_boundary_transition_extension.json",
    "photo_prompt_desire_extension.json",
    "photo_prompt_harem_extension.json",
    "photo_prompt_emotional_place_extension.json",
    "photo_prompt_poverty_extension.json",
    "photo_prompt_opening_era_extension.json",
    "photo_prompt_historical_womenswear_extension.json",
    "photo_prompt_costume_cosplay_extension.json",
    "photo_prompt_palace_fortification_extension.json",
    "photo_prompt_swimwear_extension.json",
    "photo_prompt_color_relations_extension.json",
    "photo_prompt_model_editorial_extension.json",
    "photo_prompt_realistic_background_extension.json",
    "photo_prompt_photorealism_elements_extension.json",
    "photo_prompt_everyday_scene_extension.json",
    "photo_prompt_lighting_extension.json",
    "photo_prompt_photo_era_extension.json",
    "photo_prompt_violence_crime_extension.json",
    "photo_prompt_subculture_extension.json",
    "photo_prompt_worldbuilding_extension.json",
    "photo_prompt_punk_aesthetics_extension.json",
    "photo_prompt_cjk_worldbuilding_extension.json",
    "photo_prompt_character_moe_extension.json",
    "photo_prompt_y2k_extension.json",
    "photo_prompt_portrait_composition_extension.json",
    "photo_prompt_portrait_fashion_exposure_extension.json",
    "photo_prompt_sensual_fetish_fashion_extension.json",
    "photo_prompt_contextual_appeal_extension.json",
    "photo_prompt_editing_effects_extension.json",
    "photo_prompt_motion_graphics_extension.json",
    "photo_prompt_pose_vocabulary_extension.json",
    "photo_prompt_body_morphology_extension.json",
    "photo_prompt_acting_expression_extension.json",
    "photo_prompt_neutral_expression_extension.json",
    "photo_prompt_slang_visual_extension.json",
    "photo_prompt_religion_iconography_extension.json",
    "photo_prompt_subculture_appearance_extension.json",
    "photo_prompt_seduction_expression_extension.json",
)
RESEARCH_EXTENSION_SCHEMA = "photo-prompt-research-extension/v1"
CHARACTER_MECHANISM_GRAPH_SCHEMA = "photo-character-mechanism-graph/v2"
CHARACTER_RESPONSE_RELATION_FIELDS = {
    "contrasts": {"operator", "left", "right"},
    "same_target": {"operator", "members"},
    "temporal_order": {"operator", "first", "then"},
}
CHARACTER_CONCEPT_EVIDENCE_ROLES = {
    "baseline",
    "relationship_target",
    "surface_behavior",
    "primary_action",
    "affect_leak",
    "contradicting_action_or_leak",
    "visible_response",
    "immediate_consequence",
    "continuity",
}
QUALITY_LAYERS_DATA_KEY = "_quality_layers"
VISUAL_OBLIGATIONS_DATA_KEY = "_visual_obligations"
VISUAL_PROFILE_INDEX_DATA_KEY = "_visual_profile_index"
VISUAL_PROFILE_QUERY_VECTORS_DATA_KEY = "_visual_profile_query_vectors"
SEMANTIC_INDEX_DATA_KEY = "_semantic_index"

CANDIDATE_PACK_CORE_SLOT_LIMIT = 4
CANDIDATE_PACK_SUPPORT_SLOT_LIMIT = 2
CANDIDATE_PACK_TOTAL_CANDIDATE_LIMIT = 64
CANDIDATE_PACK_CONTRACT_V6 = "photo-candidate-pack/v6"
DEFAULT_CANDIDATE_PACK_VERSION = "v6"
CANDIDATE_PACK_CREATIVE_EXPLORATION_FLOOR = 3
CANDIDATE_PACK_CREATIVE_EXPLORATION_MIN_DISTANCE = 0.45
CANDIDATE_PACK_CREATIVE_EXPLORATION_LIMIT = 6
CANDIDATE_PACK_CREATIVE_DIRECTION_FLOOR = 3
CANDIDATE_PACK_CREATIVE_DIRECTION_MIN_PROPOSALS = 4
CANDIDATE_PACK_AUTHORIAL_COMPOSITION_VERSION = "photo-authorial-composition/v1"

# These maps describe semantic impact, not topic meaning.  They let the current
# request lock govern downstream defaults without special-casing any named
# archetype, expression, culture, or genre.
SEMANTIC_CLARIFICATION_CONTRACT_VERSION = "photo-semantic-clarification/v1"
CREATIVE_AUGMENTATION_CONTRACT_VERSION = "photo-creative-augmentation/v1"
VISUAL_INTENT_CONTRACT_VERSION = "photo-visual-intent/v1"
VISUAL_OBLIGATION_REGISTRY_SCHEMA_VERSION = "photo-visual-obligation-registry/v3"
VISUAL_PROFILE_INDEX_SCHEMA_VERSION = "photo-visual-profile-index/v2"
VISUAL_PROFILE_TEXT_RECIPE_VERSION = "photo-visual-profile-text/v2"
VISUAL_PROFILE_RESOLUTION_CONTRACT_VERSION = "photo-visual-profile-resolution/v1"
VISUAL_OBLIGATIONS_CONTRACT_VERSION = "photo-visual-obligations/v1"
VISUAL_CONCEPTS_CONTRACT_VERSION = "photo-visual-concepts/v1"

# Generic lexical retrieval policy.  The values govern fields rather than
# named concepts and are copied into the generated, hash-bound indexes.
SEMANTIC_BM25F_POLICY: JsonDict = {
    "policy_version": SEMANTIC_BM25F_POLICY_VERSION,
    "k1": 1.2,
    "fields": {
        "aliases": {"weight": 4.0, "b": 0.2},
        "labels": {"weight": 3.0, "b": 0.35},
        "semantic_caption": {"weight": 2.5, "b": 0.7},
        "definition": {"weight": 3.0, "b": 0.65},
        "paraphrases": {"weight": 2.25, "b": 0.7},
        "semantic_relations": {"weight": 2.5, "b": 0.55},
        "concept_units": {"weight": 2.0, "b": 0.55},
        "manifestations": {"weight": 0.75, "b": 0.7},
        "keywords": {"weight": 1.5, "b": 0.6},
        "slot_context": {"weight": 0.35, "b": 0.2},
    },
    "query_fields": {
        "active_request": 3.0,
        "interpreted_intent": 2.5,
        "event": 2.25,
        "subject": 1.5,
        "visual_priorities": 1.5,
        "baseline_prompt": 0.75,
    },
    "rrf_k": 60,
    "candidate_limit": 12,
}

VISUAL_PROFILE_BM25F_POLICY: JsonDict = {
    "policy_version": VISUAL_PROFILE_BM25F_POLICY_VERSION,
    "k1": 1.2,
    "fields": {
        "aliases": {"weight": 4.0, "b": 0.2},
        "definition": {"weight": 2.75, "b": 0.65},
        "paraphrases": {"weight": 2.25, "b": 0.7},
        "visual_components": {"weight": 2.0, "b": 0.65},
        "support_cues": {"weight": 0.75, "b": 0.75},
    },
    "query_fields": {
        "active_request": 3.0,
        "interpreted_intent": 2.5,
        "event": 2.25,
        "subject": 1.5,
        "visual_priorities": 1.5,
        "baseline_prompt": 0.75,
    },
    "rrf_k": 60,
    "candidate_limit": 8,
}
CANDIDATE_PACK_AUTHORIAL_LENSES = (
    "gesture_and_interruption",
    "material_and_contact",
    "spatial_relationship",
    "light_and_visibility",
    "aftermath_and_trace",
    "framing_and_withheld_information",
)
CANDIDATE_PACK_ADULT_APPEAL_CONTRACT_VERSION = "photo-adult-appeal/v2"
CANDIDATE_PACK_ADULT_APPEAL_AXES = ("sensual", "fetish")
CREATIVE_CONTROL_DEFAULTS = {name: definition["default"] for name, definition in creative_controls.load_definitions()["controls"].items()}
CANDIDATE_PACK_SENSUAL_DEFAULT_INTENSITY = CREATIVE_CONTROL_DEFAULTS["sensual"]
CANDIDATE_PACK_FETISH_DEFAULT_INTENSITY = CREATIVE_CONTROL_DEFAULTS["fetish"]
CANDIDATE_PACK_ADULT_APPEAL_DEFAULT_EMPHASIS = CREATIVE_CONTROL_DEFAULTS["adult_appeal_emphasis"]
if CANDIDATE_PACK_ADULT_APPEAL_DEFAULT_EMPHASIS == "auto":
    CANDIDATE_PACK_ADULT_APPEAL_DEFAULT_EMPHASIS = (
        "balanced" if CANDIDATE_PACK_SENSUAL_DEFAULT_INTENSITY == CANDIDATE_PACK_FETISH_DEFAULT_INTENSITY
        else ("sensual_led" if CANDIDATE_PACK_SENSUAL_DEFAULT_INTENSITY > CANDIDATE_PACK_FETISH_DEFAULT_INTENSITY else "fetish_led")
    )
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

# These expressions are request controls, not positive objects to render.
# Keep them centralized so routing, mandatory-intent extraction, and adult-tone
# policy all interpret Korean, Japanese, and English wording identically.
MOE_NONSEXUAL_PATTERNS = (
    r"야하지\s*않(?:은|게|으면서도|으면서|고|도록|다)?",
    r"성적이지\s*않(?:은|게|고|도록|다)?",
    r"선정적이지\s*않(?:은|게|고|도록|다)?",
    r"비\s*성적(?:인|으로|인\s*방식)?",
    r"(?:성적|선정적|에로틱한)\s*(?:톤|느낌|연출)?\s*없이",
    r"노출\s*없이",
    r"non[-\s]?sexual(?:ized|ised)?",
    r"not\s+(?:sexy|sexual(?:ized|ised)?|erotic|sensual|suggestive)",
    r"without\s+(?:sexuali[sz]ation|eroticism|sensuality|sensual\s+framing|suggestive\s+framing|body\s+emphasis)",
    r"no\s+(?:sexuali[sz]ation|eroticism|sensuality|sensual\s+framing|suggestive\s+framing|body\s+emphasis)",
    r"性的(?:では|じゃ)?ない",
    r"性的でなく",
    r"非性的(?:な|に)?",
    r"セクシー(?:では|じゃ)?ない",
    r"エロくない",
    r"性的な演出(?:は|が)?(?:ない|なし)",
    r"露出(?:は|が)?(?:ない|なし)",
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
# Safety tier remains an internal hard-guard facet. Retired research, market,
# audience, and authorship classifications are no longer distributed in the
# authoring assets, so they do not need a runtime exclusion list.
CONTROL_ONLY_FACET_KEYS = {
    "safety_tier",
}
CANDIDATE_PACK_ALWAYS_PRIVATE_TAGS = {
    "adult_compatible",
    "adult_only",
    "age_context_only",
    "market_label_nonvisual",
    "no_national_style",
    "source_grounded",
    "market_researched",
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
VALID_INTENT_DOMAINS = {
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
    "character_scene_grammar",
    "surreal",
    "adult",
}

DEFAULT_SLOT_APPLICABILITY: JsonDict = {
    "subject_category_overrides": {},
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
    photo_candidate_semantics.validate_extension_keys(extension)

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

    slots = data.setdefault("slots", {})
    for slot, entries in (extension.get("slots") or {}).items():
        append_unique_id_entries(slots.setdefault(str(slot), []), entries, f"slots.{slot}")

    photo_candidate_semantics.extend_slot_contexts(
        slots, extension.get("existing_slot_context_extensions"))

    extension_coherence = extension.get("coherence_rules") or {}
    if not isinstance(extension_coherence, dict):
        raise ValueError("coherence_rules must be an object")
    unknown = set(extension_coherence) - {"slot_conflicts", "slot_context_rules"}
    if unknown:
        raise ValueError(f"unsupported coherence rules: {sorted(unknown)}")
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
    for mapping_key in ("subject_category_overrides",):
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

    photo_candidate_semantics.compile_extension_bundles(data, extension)
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


def character_axis_vocabularies(data: JsonDict) -> Dict[str, JsonDict]:
    """Return authored semantic-axis vocabularies keyed by generic axis name."""

    graph = data.get("character_mechanism_graph")
    rows = graph.get("axis_vocabularies") if isinstance(graph, dict) else []
    return {
        str(row.get("id") or ""): row
        for row in rows or []
        if isinstance(row, dict) and str(row.get("id") or "")
    }


def character_axis_class_aliases(data: JsonDict, axis: str) -> Dict[str, List[str]]:
    vocabulary = character_axis_vocabularies(data).get(str(axis)) or {}
    result: Dict[str, List[str]] = {}
    for row in vocabulary.get("classes") or []:
        if not isinstance(row, dict) or not str(row.get("id") or ""):
            continue
        class_id = str(row["id"])
        aliases = [class_id]
        aliases.extend(
            clean_spaces(str(value))
            for value in normalize_list(row.get("aliases"))
            if clean_spaces(str(value))
        )
        result[class_id] = list(dict.fromkeys(aliases))
    return result


def semantic_text_contains_authored_term(text: Any, term: Any) -> bool:
    """Match an authored term with the shared multilingual tokenizer boundaries."""

    normalized_term = clean_spaces(str(term or ""))
    normalized_text = clean_spaces(str(text or ""))
    if not normalized_term or not normalized_text:
        return False
    term_tokens = set(
        tokenize_bm25f_text(normalized_term, lexicon=[normalized_term])
    )
    text_tokens = set(
        tokenize_bm25f_text(normalized_text, lexicon=[normalized_term])
    )
    return bool(term_tokens) and term_tokens.issubset(text_tokens)


def character_axis_value_classes(data: JsonDict, axis: str, value: Any) -> Set[str]:
    """Map an authored free-text axis value onto data-declared semantic classes."""

    text = clean_spaces(str(value or "")).casefold()
    if not text:
        return set()
    matched: Set[str] = set()
    for class_id, aliases in character_axis_class_aliases(data, axis).items():
        if any(
            text == clean_spaces(str(alias)).casefold()
            or semantic_text_contains_authored_term(text, alias)
            for alias in aliases
            if clean_spaces(str(alias))
        ):
            matched.add(class_id)
    return matched


def validate_character_mechanism_graph(data: JsonDict) -> None:
    """Validate the optional character-response graph.

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
    if domain != "character_scene_grammar":
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
    axis_vocabularies = unique_rows("axis_vocabularies")
    concept_profiles = unique_rows("concept_profiles")
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

    vocabulary_classes: Dict[str, Set[str]] = {}
    for axis_id, vocabulary in axis_vocabularies.items():
        allowed_vocabulary_fields = {"id", "description", "classes"}
        unknown_vocabulary_fields = set(vocabulary) - allowed_vocabulary_fields
        if unknown_vocabulary_fields:
            raise ValueError(
                f"character axis vocabulary {axis_id} has unsupported fields "
                f"{sorted(unknown_vocabulary_fields)}"
            )
        classes = vocabulary.get("classes")
        if not isinstance(classes, list) or not classes:
            raise ValueError(f"character axis vocabulary {axis_id} requires classes")
        class_ids: Set[str] = set()
        for row in classes:
            if not isinstance(row, dict) or set(row) - {"id", "aliases", "description"}:
                raise ValueError(
                    f"character axis vocabulary {axis_id} has an invalid class row"
                )
            class_id = str(row.get("id") or "")
            aliases = normalize_list(row.get("aliases"))
            if not class_id or class_id in class_ids or not aliases:
                raise ValueError(
                    f"character axis vocabulary {axis_id} classes require unique IDs and aliases"
                )
            class_ids.add(class_id)
        vocabulary_classes[axis_id] = class_ids

    allowed_profile_fields = {
        "id",
        "domain",
        "en",
        "ko",
        "ja",
        "aliases",
        "definition",
        "paraphrases",
        "axis_requirements",
        "axis_exclusions",
        "required_relations",
        "required_evidence_roles",
        "confounders",
        "optional_runtime_node_ids",
        "applicability",
    }
    for profile_id, profile in concept_profiles.items():
        unknown_profile_fields = set(profile) - allowed_profile_fields
        if unknown_profile_fields:
            raise ValueError(
                f"character concept profile {profile_id} has unsupported fields "
                f"{sorted(unknown_profile_fields)}"
            )
        if str(profile.get("domain") or "") != "character_response":
            raise ValueError(
                f"character concept profile {profile_id} must use character_response domain"
            )
        if not str(profile.get("definition") or "").strip():
            raise ValueError(f"character concept profile {profile_id} requires a definition")
        paraphrases = normalize_list(profile.get("paraphrases"))
        if len(paraphrases) < 3 or len(paraphrases) != len(set(paraphrases)):
            raise ValueError(
                f"character concept profile {profile_id} requires distinct multilingual paraphrases"
            )
        aliases = normalize_list(profile.get("aliases"))
        if not aliases or len(aliases) != len(set(aliases)):
            raise ValueError(
                f"character concept profile {profile_id} requires distinct aliases"
            )
        for label in ("en", "ko", "ja"):
            if not str(profile.get(label) or "").strip():
                raise ValueError(
                    f"character concept profile {profile_id} requires {label} label"
                )
        for field in ("axis_requirements", "axis_exclusions"):
            constraints = profile.get(field) or {}
            if not isinstance(constraints, dict):
                raise ValueError(
                    f"character concept profile {profile_id}.{field} must be an object"
                )
            for axis_id, constraint in constraints.items():
                if axis_id not in vocabulary_classes or not isinstance(constraint, dict):
                    raise ValueError(
                        f"character concept profile {profile_id}.{field}.{axis_id} is invalid"
                    )
                if set(constraint) != {"semantic_classes"}:
                    raise ValueError(
                        f"character concept profile {profile_id}.{field}.{axis_id} "
                        "must declare semantic_classes only"
                    )
                class_ids = normalize_list(constraint.get("semantic_classes"))
                if not class_ids or not set(class_ids).issubset(
                    vocabulary_classes[axis_id]
                ):
                    raise ValueError(
                        f"character concept profile {profile_id}.{field}.{axis_id} "
                        "references unknown semantic classes"
                    )
        relations = profile.get("required_relations")
        if not isinstance(relations, list) or not 1 <= len(relations) <= 8:
            raise ValueError(
                f"character concept profile {profile_id} requires semantic relations"
            )
        relation_signatures: Set[tuple[Any, ...]] = set()
        for relation in relations:
            if not isinstance(relation, dict):
                raise ValueError(
                    f"character concept profile {profile_id} has a non-object relation"
                )
            operator = str(relation.get("operator") or "")
            expected_fields = CHARACTER_RESPONSE_RELATION_FIELDS.get(operator)
            if expected_fields is None or set(relation) != expected_fields:
                raise ValueError(
                    f"character concept profile {profile_id} has an invalid relation shape"
                )
            if operator == "same_target":
                members = normalize_list(relation.get("members"))
                valid = bool(
                    2 <= len(members) <= 8
                    and len(members) == len(set(members))
                    and "relationship_target" in members
                    and set(members) <= CHARACTER_RESPONSE_RELATION_MEMBERS
                )
            else:
                left_key, right_key = (
                    ("left", "right")
                    if operator == "contrasts"
                    else ("first", "then")
                )
                left = str(relation.get(left_key) or "")
                right = str(relation.get(right_key) or "")
                valid = bool(
                    left != right
                    and {left, right} <= CHARACTER_RESPONSE_RELATION_MEMBERS
                )
            signature = character_response_relation_signature(relation)
            if not valid or signature in relation_signatures:
                raise ValueError(
                    f"character concept profile {profile_id} has invalid or repeated semantic relation members"
                )
            relation_signatures.add(signature)
        evidence_roles = normalize_list(profile.get("required_evidence_roles"))
        if (
            not evidence_roles
            or len(evidence_roles) != len(set(evidence_roles))
            or not set(evidence_roles).issubset(CHARACTER_CONCEPT_EVIDENCE_ROLES)
        ):
            raise ValueError(
                f"character concept profile {profile_id} has invalid evidence roles"
            )
        confounders = profile.get("confounders")
        if not isinstance(confounders, list) or not confounders:
            raise ValueError(
                f"character concept profile {profile_id} requires confounders"
            )
        confounder_ids: Set[str] = set()
        for confounder in confounders:
            confounder_id = str(
                confounder.get("id") if isinstance(confounder, dict) else ""
            )
            definition = str(
                confounder.get("definition") if isinstance(confounder, dict) else ""
            )
            if not confounder_id or confounder_id in confounder_ids or not definition:
                raise ValueError(
                    f"character concept profile {profile_id} has invalid confounders"
                )
            allowed_confounder_fields = {
                "id",
                "en",
                "ko",
                "ja",
                "aliases",
                "definition",
                "paraphrases",
            }
            if set(confounder) - allowed_confounder_fields:
                raise ValueError(
                    f"character concept profile {profile_id} confounder "
                    f"{confounder_id} has unsupported fields"
                )
            if any(
                not str(confounder.get(label) or "").strip()
                for label in ("en", "ko", "ja")
            ):
                raise ValueError(
                    f"character concept profile {profile_id} confounder "
                    f"{confounder_id} requires en, ko, and ja meanings"
                )
            confounder_paraphrases = normalize_list(
                confounder.get("paraphrases")
            )
            if (
                len(confounder_paraphrases) < 2
                or len(confounder_paraphrases)
                != len(set(confounder_paraphrases))
            ):
                raise ValueError(
                    f"character concept profile {profile_id} confounder "
                    f"{confounder_id} requires distinct paraphrases"
                )
            confounder_ids.add(confounder_id)
        optional_runtime_ids = normalize_list(profile.get("optional_runtime_node_ids"))
        if (
            not optional_runtime_ids
            or len(optional_runtime_ids) != len(set(optional_runtime_ids))
            or any(runtime_id not in nodes for runtime_id in optional_runtime_ids)
        ):
            raise ValueError(
                f"character concept profile {profile_id} has invalid optional runtime nodes"
            )
        applicability = profile.get("applicability")
        if not isinstance(applicability, dict) or applicability != {
            "retrieval_only": True,
            "hard_eligible": False,
            "requester_definition_precedence": True,
        }:
            raise ValueError(
                f"character concept profile {profile_id} must remain requester-first and advisory"
            )

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


def load_json(path: str | Path) -> JsonDict:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Tag JSON not found: {p}")
    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if p.name == "photo_prompt_tags.json":
        allowed_keys = {
            "candidate_semantic_policy", "version", "description", "facet_vocab", "slots",
            "negative_prompt", "negative_prompt_pools", "coherence_rules", "slot_applicability",
        }
        unknown = set(data) - allowed_keys
        if unknown:
            raise ValueError(f"unsupported photo corpus fields: {sorted(unknown)}")
        coherence = data.get("coherence_rules") or {}
        if not isinstance(coherence, dict) or set(coherence) - {"slot_conflicts", "slot_context_rules"}:
            raise ValueError("unsupported coherence rules")
        candidate_policy = data.get("candidate_semantic_policy") or {}
        photo_candidate_semantics.validate_semantic_policy(candidate_policy, AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS)
        required_extensions = candidate_policy.get("required_extensions") or []
        missing_extensions = [name for name in required_extensions if not p.with_name(name).is_file()]
        if missing_extensions:
            raise ValueError(f"required candidate extensions are missing: {missing_extensions}")
        for extension_filename in RESEARCH_EXTENSION_FILENAMES:
            extension_path = p.with_name(extension_filename)
            if not extension_path.exists():
                continue
            with extension_path.open("r", encoding="utf-8") as f:
                extension = json.load(f)
            data = merge_research_extension(data, extension)
        validate_character_mechanism_graph(data)
        photo_candidate_semantics.validate_candidate_entries(data, AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS)
        if data.get("candidate_bundles"):
            registry = load_visual_obligation_registry(default_visual_obligation_registry_path(p))
            photo_candidate_semantics.validate_bundle_references(data, registry.get("profiles") or [])
    return data


def load_quality_layers(path: str | Path) -> JsonDict:
    return load_json(path)


def default_visual_obligation_registry_path(tags_path: str | Path) -> Path:
    tags = Path(tags_path)
    sibling = tags.parent / VISUAL_OBLIGATION_REGISTRY_FILENAME
    if sibling.exists():
        return sibling
    return Path(__file__).resolve().parents[1] / "assets" / VISUAL_OBLIGATION_REGISTRY_FILENAME


def load_visual_obligation_registry(path: str | Path) -> JsonDict:
    registry_path = Path(path)
    payload = load_json(registry_path)
    if payload.get("schema_version") != VISUAL_OBLIGATION_REGISTRY_SCHEMA_VERSION:
        raise ValueError(
            "visual obligation registry schema_version must be "
            f"{VISUAL_OBLIGATION_REGISTRY_SCHEMA_VERSION!r}"
        )
    if payload.get("contract_version") != VISUAL_OBLIGATIONS_CONTRACT_VERSION:
        raise ValueError(
            "visual obligation registry contract_version must be "
            f"{VISUAL_OBLIGATIONS_CONTRACT_VERSION!r}"
        )
    if payload.get("visual_intent_contract_version") != VISUAL_INTENT_CONTRACT_VERSION:
        raise ValueError(
            "visual obligation registry visual_intent_contract_version must be "
            f"{VISUAL_INTENT_CONTRACT_VERSION!r}"
        )
    if payload.get("concept_contract_version") != VISUAL_CONCEPTS_CONTRACT_VERSION:
        raise ValueError(
            "visual obligation registry concept_contract_version must be "
            f"{VISUAL_CONCEPTS_CONTRACT_VERSION!r}"
        )
    profiles = payload.get("profiles")
    if not isinstance(profiles, list) or not profiles:
        raise ValueError("visual obligation registry requires a non-empty profiles list")
    existing_ids = {
        str(profile.get("id") or "")
        for profile in profiles
        if isinstance(profile, dict)
    }
    for extension_filename in VISUAL_OBLIGATION_EXTENSION_FILENAMES:
        extension_path = registry_path.with_name(extension_filename)
        if not extension_path.exists():
            continue
        extension = load_json(extension_path)
        if (
            extension.get("schema_version")
            != VISUAL_OBLIGATION_EXTENSION_SCHEMA_VERSION
        ):
            raise ValueError(
                "visual obligation extension schema_version must be "
                f"{VISUAL_OBLIGATION_EXTENSION_SCHEMA_VERSION!r}"
            )
        if (
            extension.get("relation_contract_version")
            != VISUAL_RELATION_CONTRACT_VERSION
        ):
            raise ValueError(
                "visual obligation extension relation_contract_version must be "
                f"{VISUAL_RELATION_CONTRACT_VERSION!r}"
            )
        extension_profiles = extension.get("profiles")
        if not isinstance(extension_profiles, list) or not extension_profiles:
            raise ValueError(
                f"visual obligation extension {extension_filename} requires profiles"
            )
        for profile in extension_profiles:
            if not isinstance(profile, dict) or not str(profile.get("id") or ""):
                raise ValueError(
                    f"visual obligation extension {extension_filename} has invalid profile"
                )
            profile_id = str(profile["id"])
            if profile_id in existing_ids:
                raise ValueError(
                    f"visual obligation extension duplicate profile id {profile_id}"
                )
            profiles.append(copy.deepcopy(profile))
            existing_ids.add(profile_id)
        payload["relation_contract_version"] = VISUAL_RELATION_CONTRACT_VERSION
    payload["profiles"] = [compile_visual_profile(profile) for profile in profiles]
    for profile in payload["profiles"]:
        candidate = profile.get("concept_candidate") or {}
        if "core_assertion_discovery" in candidate:
            photo_candidate_semantics.validate_candidate_entries({"slots": {"profile": [{
                **candidate, "id": profile["id"],
                "concept_units": (profile.get("semantics") or {}).get("visual_components") or [],
            }]}}, AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS)
    return payload


def character_response_relation_signature(
    relation: Mapping[str, Any],
) -> tuple[Any, ...]:
    """Return a semantic signature; same-target member order is immaterial."""

    operator = str(relation.get("operator") or "")
    if operator == "same_target":
        return operator, tuple(sorted(normalize_list(relation.get("members"))))
    if operator == "contrasts":
        return operator, str(relation.get("left") or ""), str(
            relation.get("right") or ""
        )
    if operator == "temporal_order":
        return operator, str(relation.get("first") or ""), str(
            relation.get("then") or ""
        )
    return operator, canonical_json_sha256(relation)


def visual_profile_registry_sha256(registry: JsonDict) -> str:
    """Bind every generated visual-profile index to its single authored source."""

    return canonical_json_sha256(registry)


def visual_profile_exact_term_rows(registry: JsonDict) -> List[JsonDict]:
    """Compile boundary-aware exact terms from the registry's activation lane."""

    rows: List[JsonDict] = []
    for profile in registry.get("profiles") or []:
        if not isinstance(profile, dict):
            continue
        profile_id = str(profile.get("id") or "").strip()
        activation = (
            profile.get("activation")
            if isinstance(profile.get("activation"), dict)
            else {}
        )
        fields = (
            ("exact_terms", "exact_term"),
            ("project_glossary_aliases", "project_glossary_alias"),
        )
        for field, term_type in fields:
            for raw_term in activation.get(field) or []:
                term = clean_spaces(str(raw_term or ""))
                if profile_id and term:
                    rows.append(
                        {
                            "term": term,
                            "term_key": term.casefold(),
                            "profile_id": profile_id,
                            "term_type": term_type,
                        }
                    )
    rows.sort(
        key=lambda row: (
            str(row.get("term_key") or ""),
            str(row.get("profile_id") or ""),
            str(row.get("term_type") or ""),
        )
    )
    return rows


def visual_profile_semantic_text(profile: JsonDict) -> str:
    """Create a positive prototype from the shared authored-field allowlist."""
    return positive_visual_profile_text(profile)


def visual_profile_bm25f_fields(profile: JsonDict) -> JsonDict:
    """Use the same positive meaning fields as vector retrieval."""
    return positive_visual_profile_fields(profile)


def visual_profile_bm25f_documents(registry: JsonDict) -> Dict[str, JsonDict]:
    return {
        str(profile.get("id")): visual_profile_bm25f_fields(profile)
        for profile in registry.get("profiles") or []
        if isinstance(profile, dict) and str(profile.get("id") or "").strip()
    }


def _bm25f_lexicon_from_documents(
    documents: Mapping[str, JsonDict],
    fields: Sequence[str] = ("aliases",),
) -> List[str]:
    return sorted(
        {
            clean_spaces(str(value))
            for document in documents.values()
            for field in fields
            for value in document.get(field) or []
            if clean_spaces(str(value))
        },
        key=lambda value: (-len(value), value.casefold()),
    )


def build_visual_profile_bm25f_payload(registry: JsonDict) -> JsonDict:
    documents = visual_profile_bm25f_documents(registry)
    payload = build_bm25f_index(
        documents,
        policy=VISUAL_PROFILE_BM25F_POLICY,
        lexicon=_bm25f_lexicon_from_documents(documents),
    )
    payload["policy_version"] = VISUAL_PROFILE_BM25F_POLICY_VERSION
    payload["policy_sha256"] = canonical_json_sha256(VISUAL_PROFILE_BM25F_POLICY)
    return payload


def build_visual_profile_index_payload(
    registry: JsonDict,
    *,
    vectors: Optional[Dict[str, Sequence[float]]] = None,
    provider: str = SEMANTIC_PROVIDER,
    model: str = SEMANTIC_MODEL_ID,
    dimensions: int = DEFAULT_SEMANTIC_DIMENSIONS,
) -> JsonDict:
    """Materialize the generated exact+vector sidecar from one registry."""

    supplied_vectors = vectors or {}
    entries: JsonDict = {}
    for profile in registry.get("profiles") or []:
        if not isinstance(profile, dict):
            continue
        profile_id = str(profile.get("id") or "").strip()
        if not profile_id:
            continue
        text = visual_profile_semantic_text(profile)
        entries[profile_id] = {
            "text": text,
            "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "vector": [float(value) for value in supplied_vectors.get(profile_id, [])],
        }
    return {
        "schema_version": VISUAL_PROFILE_INDEX_SCHEMA_VERSION,
        "registry_schema_version": registry.get("schema_version"),
        "registry_sha256": visual_profile_registry_sha256(registry),
        "semantic_text_recipe": VISUAL_PROFILE_TEXT_RECIPE_VERSION,
        "provider": provider,
        "embedding_model": model,
        "embedding_dimensions": int(dimensions),
        "retrieval_policy": copy.deepcopy(registry.get("retrieval_policy") or {}),
        "exact_lookup": visual_profile_exact_term_rows(registry),
        "bm25f": build_visual_profile_bm25f_payload(registry),
        "entries": entries,
    }


def validate_visual_profile_index_metadata(
    payload: JsonDict,
    registry: JsonDict,
    *,
    provider: str = SEMANTIC_PROVIDER,
    model: str = SEMANTIC_MODEL_ID,
    dimensions: int = DEFAULT_SEMANTIC_DIMENSIONS,
) -> None:
    if payload.get("schema_version") != VISUAL_PROFILE_INDEX_SCHEMA_VERSION:
        raise ValueError(
            "visual profile index schema_version must be "
            f"{VISUAL_PROFILE_INDEX_SCHEMA_VERSION!r}"
        )
    if payload.get("registry_sha256") != visual_profile_registry_sha256(registry):
        raise ValueError(
            "visual profile index registry_sha256 does not match the visual registry; "
            "regenerate it with build_visual_profile_index.py"
        )
    if payload.get("semantic_text_recipe") != VISUAL_PROFILE_TEXT_RECIPE_VERSION:
        raise ValueError(
            "visual profile index semantic_text_recipe is stale; regenerate the index"
        )
    if payload.get("provider") != provider:
        raise ValueError(
            f"visual profile index provider is {payload.get('provider')!r}, expected {provider!r}"
        )
    if payload.get("embedding_model") != model:
        raise ValueError(
            "visual profile index embedding_model is "
            f"{payload.get('embedding_model')!r}, expected {model!r}"
        )
    expected_dimensions = int(dimensions)
    if int(payload.get("embedding_dimensions", -1)) != expected_dimensions:
        raise ValueError(
            "visual profile index embedding_dimensions is "
            f"{payload.get('embedding_dimensions')!r}, expected {expected_dimensions}"
        )
    expected_lookup = visual_profile_exact_term_rows(registry)
    if payload.get("exact_lookup") != expected_lookup:
        raise ValueError(
            "visual profile index exact_lookup is stale; regenerate the index"
        )
    bm25f_payload = payload.get("bm25f")
    if not isinstance(bm25f_payload, dict):
        raise ValueError("visual profile index is missing its BM25F payload")
    if bm25f_payload.get("policy_version") != VISUAL_PROFILE_BM25F_POLICY_VERSION:
        raise ValueError("visual profile index BM25F policy_version is stale")
    if bm25f_payload.get("policy_sha256") != canonical_json_sha256(
        VISUAL_PROFILE_BM25F_POLICY
    ):
        raise ValueError("visual profile index BM25F policy hash is stale")
    bm25f_material = {
        key: value
        for key, value in bm25f_payload.items()
        if key not in {"policy_version", "policy_sha256"}
    }
    documents = visual_profile_bm25f_documents(registry)
    validate_bm25f_index(
        bm25f_material,
        documents,
        policy=VISUAL_PROFILE_BM25F_POLICY,
        lexicon=_bm25f_lexicon_from_documents(documents),
    )
    expected_entries = {
        str(profile.get("id") or ""): visual_profile_semantic_text(profile)
        for profile in registry.get("profiles") or []
        if isinstance(profile, dict) and str(profile.get("id") or "").strip()
    }
    entries = payload.get("entries")
    if not isinstance(entries, dict) or set(entries) != set(expected_entries):
        raise ValueError("visual profile index entries do not match registry profiles")
    for profile_id, expected_text in expected_entries.items():
        entry = entries.get(profile_id)
        if not isinstance(entry, dict) or entry.get("text") != expected_text:
            raise ValueError(
                f"visual profile index text is stale for profile {profile_id!r}"
            )
        expected_text_hash = hashlib.sha256(expected_text.encode("utf-8")).hexdigest()
        if entry.get("text_sha256") != expected_text_hash:
            raise ValueError(
                f"visual profile index text_sha256 is stale for profile {profile_id!r}"
            )
        vector = entry.get("vector")
        if not isinstance(vector, list) or len(vector) != expected_dimensions:
            raise ValueError(
                f"visual profile index vector for {profile_id!r} must have "
                f"{expected_dimensions} dimensions"
            )


def load_visual_profile_index(
    path: str | Path,
    registry: JsonDict,
    *,
    provider: str = SEMANTIC_PROVIDER,
    model: str = SEMANTIC_MODEL_ID,
    dimensions: int = DEFAULT_SEMANTIC_DIMENSIONS,
) -> JsonDict:
    index_path = Path(path)
    if not index_path.exists():
        raise FileNotFoundError(f"visual profile index not found: {index_path}")
    payload = load_json(index_path)
    validate_visual_profile_index_metadata(
        payload,
        registry,
        provider=provider,
        model=model,
        dimensions=dimensions,
    )
    return payload


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


def clean_spaces(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)
    text = re.sub(r"([.!?]){2,}", r"\1", text)
    return text


def split_negative_prompt_terms(value: Any) -> List[str]:
    if value is None:
        return []
    return [
        clean_spaces(part)
        for part in str(value).split(",")
        if clean_spaces(part)
    ]


def find_blanket_negative_directives(text: str) -> List[str]:
    """Find prompt-writing directives that delete broad visual semantics.

    This deliberately targets instruction-shaped prose, not every grammatical
    negation.  Narrative phrases such as ``she does not look away`` are not
    classified here.  Broad clauses such as ``No contact, gore, or extra
    people`` and ``never touching anyone`` are, because they behave like a
    second ungrounded request embedded in the positive prompt.
    """

    value = str(text or "")
    patterns = (
        re.compile(
            r"(?:^|[.;!?:—]\s+|,\s+)((?:no\b|do\s+not\b|don't\b|avoid\b|exclude\b)[^.;!?]*)",
            flags=re.IGNORECASE,
        ),
        re.compile(
            r"(?:^|[.;!?:—]\s+|,\s+)(never\s+(?:touch(?:es|ed|ing)?|inject(?:s|ed|ing)?|contact(?:s|ed|ing)?|show(?:s|ed|ing)?|depict(?:s|ed|ing)?|include(?:s|d|ing)?|use(?:s|d|ing)?|reveal(?:s|ed|ing)?|sexualiz(?:e|es|ed|ing)|crop(?:s|ped|ping)?|add(?:s|ed|ing)?)\b[^.;!?]*)",
            flags=re.IGNORECASE,
        ),
    )
    directives: List[str] = []
    seen: Set[str] = set()
    for pattern in patterns:
        for match in pattern.finditer(value):
            directive = clean_spaces(match.group(1))
            key = directive.casefold()
            if directive and key not in seen:
                directives.append(directive)
                seen.add(key)
    return directives


def build_negative_intent_guard(
    core: JsonDict,
    negative_en: Any,
    *,
    identity_preservation_enabled: bool,
) -> JsonDict:
    """Build the public, recomputable v6 negative-intent boundary."""

    guard: JsonDict = {
        "contract_version": NEGATIVE_INTENT_GUARD_CONTRACT_VERSION,
        "source_authorial_core_sha256": str(core.get("canonical_sha256") or ""),
        "source_intent_lock_sha256": str(
            ((core.get("intent_lock") or {}).get("canonical_sha256") or "")
        ),
        "positive_prompt_policy": "positive_description_only_no_blanket_negative_directives",
        "automatic_negative_policy": "intent_neutral_photographic_defects_only",
        "requester_exclusion_policy": "exact_active_request_scope_only",
        "platform_safety_policy": "enforce_outside_prompt_unless_requester_explicit",
        "local_boundary_policy": "positive_geometry_or_visible_state",
        "identity_preservation_enabled": bool(identity_preservation_enabled),
        "explicit_user_exclusions": [
            str(item) for item in core.get("user_exclusions") or []
        ],
        "emitted_terms": split_negative_prompt_terms(negative_en),
    }
    guard["canonical_sha256"] = canonical_json_sha256(guard)
    guard["guard_id"] = str(guard["canonical_sha256"])[:16]
    return guard


def ensure_period(text: str) -> str:
    text = clean_spaces(text)
    if text and text[-1] not in ".!?。":
        text += "."
    return text


def stable_text_id(text: Optional[str], length: int = 16) -> Optional[str]:
    if text is None:
        return None
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length]


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
        "slots": {
            slot: dict(policy)
            for slot, policy in DEFAULT_SLOT_APPLICABILITY["slots"].items()
        },
    }
    if not isinstance(configured, dict):
        return merged
    for key in ("subject_category_overrides",):
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
    domains = set(generation_contract.get("domains", []))
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
        return "request_domain_denied"
    if policy.get("require_domain_match") and allowed_domains and not (domains & allowed_domains):
        return "request_domain_not_allowed"
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
        "cheek_makeup", "complexion_coverage", "costume_style", "eye_detail", "eye_makeup_line",
        "eyeshadow_style", "face_sculpting", "facial_hair", "footwear",
        "gaze_engagement", "hair_color", "hair_style", "hand_pose", "lip_finish",
        "lash_style", "lip_color_placement", "makeup_decoration", "makeup_style", "makeup_wear_state",
        "person_origin", "silhouette_proportion", "skin_finish", "wardrobe_style",
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
    return f"slot:{slot}:{raw_id}"


def candidate_pack_slot_limit(slot: str) -> int:
    return CANDIDATE_PACK_CORE_SLOT_LIMIT if slot in CANDIDATE_PACK_CORE_SLOTS else CANDIDATE_PACK_SUPPORT_SLOT_LIMIT


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
    """Return user-visible relevance text without private control metadata."""
    values: List[str] = [str(item) for item in extra if str(item).strip()]
    for key in (
        "en",
        "ko",
        "label_en",
        "label_ko",
        "aliases",
        "keywords",
        "terms",
    ):
        raw = entry.get(key)
        if isinstance(raw, list):
            values.extend(str(item) for item in raw)
        elif raw is not None:
            values.append(str(raw))
    return " ".join(values).lower()


def candidate_pack_public_facets(entry: JsonDict) -> JsonDict:
    return {
        str(key): normalize_list(value)[:12]
        for key, value in (entry.get("facets") or {}).items()
        if str(key).strip()
        and str(key) not in CONTROL_ONLY_FACET_KEYS
        and normalize_list(value)
    }


def candidate_pack_control_only_tags(data: JsonDict) -> Set[str]:
    private = set(CANDIDATE_PACK_ALWAYS_PRIVATE_TAGS)
    graph = data.get("character_mechanism_graph")
    if not isinstance(graph, dict):
        return private
    domain = str(graph.get("domain") or "")
    if domain:
        private.add(domain)
    for family in graph.get("families", []) or []:
        if not isinstance(family, dict):
            continue
        private.add(str(family.get("id") or ""))
        private.update(normalize_list(family.get("topic_ids")))
    for node in graph.get("runtime_nodes", []) or []:
        if not isinstance(node, dict) or str(node.get("role") or "") == "visual_atom":
            continue
        private.add(str(node.get("id") or ""))
    for collection in ("policies", "compatibility_edges", "guard_rules"):
        for item in graph.get(collection, []) or []:
            if isinstance(item, dict):
                private.add(str(item.get("id") or ""))
    return {tag for tag in private if tag}


def candidate_pack_public_tags(data: JsonDict, entry: JsonDict) -> List[str]:
    private = candidate_pack_control_only_tags(data)
    public: List[str] = []
    for raw_tag in normalize_list(entry.get("tags")):
        tag = str(raw_tag).strip()
        lowered = tag.lower()
        if not tag or tag in private:
            continue
        if photo_candidate_semantics.maintenance_tag(lowered):
            continue
        if lowered.startswith("character_") and lowered.endswith("_scene_atomic_scene"):
            continue
        public.append(tag)
    return public[:12]


def candidate_pack_summarize_slot_candidate(
    data: JsonDict,
    slot: str,
    row: JsonDict,
) -> tuple[JsonDict, Entry]:
    raw_id = str(row.get("id") or "")
    entry = candidate_pack_slot_entry_by_id(data, slot, raw_id) or {"id": raw_id}
    candidate = {
        "id": candidate_pack_candidate_id("slot", raw_id, slot),
        "slot": slot,
        "entry_id": raw_id,
        "label_en": localize(entry, "en") or raw_id,
        "label_ko": localize(entry, "ko") or raw_id,
        "tags": candidate_pack_public_tags(data, entry),
        "kind": normalize_list(entry.get("kind"))[:8],
        "facets": candidate_pack_public_facets(entry),
        "scores": candidate_pack_score_payload(row),
        "applicability": {
            "status": str(row.get("applicability_status") or "eligible"),
            "source": str(row.get("applicability_source") or "frozen_core_slot_contract"),
            "reason": row.get("applicability_reason"),
        },
        "conflicts_with": [],
    }
    return candidate, entry


SLOT_FOCUS_SUBJECT_SLOTS = {
    "subject", "appearance_type", "anatomical_connection", "body_evidence_region",
    "costume_style", "species_marker", "surface_material", "wardrobe_style",
    "footwear", "silhouette_proportion",
}
SLOT_FOCUS_SETTING_SLOTS = {
    "location", "space_condition", "crowd_density", "situation_context",
    "occasion_context", "ambient_particle", "weather", "time_of_day",
}
SLOT_FOCUS_EVENT_SLOTS = {
    "action", "body_pose", "prop", "narrative_core", "concept_tension",
    "relational_action", "aftermath_trace", "duty_prop_state", "procedure_step",
}
SLOT_FOCUS_AFFECT_SLOTS = {"expression", "mood", "sensory_focus"}
SLOT_FOCUS_LIGHT_SLOTS = {
    "lighting", "light_type", "light_shape", "light_direction", "light_intensity",
}
SLOT_FOCUS_STYLE_SLOTS = {
    "aesthetic_trend", "composition", "shot_scale", "platform_framing",
    "subject_framing", "camera_direction", "camera_height", "camera_type",
    "lens", "format", "medium", "genre",
}


def candidate_pack_slot_focus_text(core: JsonDict, slot: str) -> tuple[str, List[str]]:
    """Project only relevant frozen-core fields into one advisory slot query."""

    fields: List[str] = []
    if slot in SLOT_FOCUS_SUBJECT_SLOTS:
        fields = ["subject"]
    elif slot in SLOT_FOCUS_SETTING_SLOTS:
        fields = ["setting", "event"] if slot == "situation_context" else ["setting"]
    elif slot in SLOT_FOCUS_EVENT_SLOTS:
        fields = ["event", "subject"] if slot in {"body_pose", "prop"} else ["event"]
    elif slot in SLOT_FOCUS_AFFECT_SLOTS:
        fields = ["event", "visual_priorities"]
    elif slot in SLOT_FOCUS_LIGHT_SLOTS:
        fields = ["setting", "visual_priorities"]
    elif slot in SLOT_FOCUS_STYLE_SLOTS:
        fields = ["style", "visual_priorities"]
    if not fields:
        return "", []
    projection: JsonDict = {
        "contract_version": core.get("contract_version"),
        "request_binding": {"active_spans": []},
        "user_exclusions": core.get("user_exclusions") or [],
    }
    for field in fields:
        if field in core:
            projection[field] = core[field]
    focus_text, _ = authorial_core_retrieval_text(projection)
    return focus_text, fields if focus_text else []


def candidate_pack_age_only_subject_match(entry: Entry, slot: str, core: JsonDict) -> bool:
    """Distinguish an explicitly adult human role from adult-content styling."""

    if slot != "subject" or not re.search(r"\badult\b", str(core.get("subject") or ""), re.I):
        return False
    tags = entry_tags(entry) | entry_kinds(entry) | facet_tokens(entry)
    if (
        "human" not in tags
        or not (tags & {"role", "occupation"})
        or "adult" not in adult_semantic_tokens(entry)
    ):
        return False
    return not bool(tags & {
        "fetish", "suggestive", "sexual", "adult_context", "adult_only",
        "safety_tier:adult_only",
    })


def candidate_pack_direct_subject_categories(subject: str) -> list[str]:
    """Recognize a narrow English direct human noun phrase, not a depicted person.

    The existing category policy omits woman/man. Do not match an embedded
    mention (statue/photo of a person), a compound object head (woman statue),
    or a nonhuman adult. Unknown syntax remains unclassified.
    """
    match = re.match(r'^\s*(?:(?:a|an|the)\s+)?adult\s+(?:woman|man|women|men)\b(.*)$', subject, re.I)
    if not match:
        return []
    suffix = match.group(1).strip()
    if suffix and suffix != '.' and not re.match(r'^(?:in|with|who|whose|wearing)\b', suffix, re.I):
        return []
    # An image/container is not the main physical human. Restrict this check
    # to the immediate "in a ... image" complement; a person carrying a photo
    # or standing in a room with pictures is still a person.
    representation = r'(?:photo(?:graph)?|picture|painting|poster|portrait|drawing|print|sculpture|statue)'
    if re.match(r'^in\s+(?:(?:a|an|the)\s+)?(?:(?!(?:with|of|beside|containing|near|behind)\b)[a-z-]+\s+){0,3}' + representation + r'\b', suffix, re.I):
        return []
    if re.match(r'^in\s+(?:bronze|marble|stone|clay|wax)\s*(?:$|[,.])', suffix, re.I):
        return []
    return ['human']


def candidate_pack_assertion_discovery(
    data: JsonDict, core: JsonDict, documents: JsonDict, bm25f: JsonDict,
    *, include_visual_priorities: bool = False, include_frozen_baseline: bool = False,
) -> List[str]:
    """Find source-opted-in options per frozen assertion, never hard duties.

    Whole-scene similarity must not hide an explicitly
    authored observation. All additions still require open dimensions and
    source-declared property compatibility. No keyword or concept IDs route
    this lane, and exclusions are checked before lexical ranking.
    """
    policy = (data.get("candidate_semantic_policy") or {}).get("core_assertion_discovery") or {}
    if not policy or not bm25f:
        return []
    lock = core.get("intent_lock") or {}
    open_dimensions = set(lock.get("open_dimensions") or [])
    assertions = [a for a in core.get("semantic_assertions") or [] if isinstance(a, dict)]

    def assertion_text(assertion: JsonDict) -> str:
        def values(node: Any) -> List[str]:
            if isinstance(node, dict):
                return [text for value in node.values() for text in values(value)]
            if isinstance(node, list):
                return [text for value in node for text in values(value)]
            return [str(node).replace("_", " ")] if isinstance(node, str) else []
        return clean_spaces(" ".join(values(assertion.get("evidence")) + values(assertion.get("axes"))))

    minimum = policy["minimum_shared_content_words"]
    excluded = [str(text) for text in core.get("user_exclusions") or []]
    excluded.extend(assertion_text(a) for a in assertions if a.get("polarity") == "excluded")
    allowed: JsonDict = {}
    for document_id, source in documents.items():
        dimensions = normalize_list(source.get("affected_dimensions"))
        if (source.get("core_assertion_discovery") is not True
                or not dimensions or not set(dimensions) <= open_dimensions
                or not property_effects_allowed(lock, dimensions, source.get("affected_properties"))):
            continue
        blob = candidate_pack_entry_blob(source, extra=[
            *normalize_list(source.get("concept_units")), *normalize_list(source.get("concept_terms")),
            *normalize_list(source.get("paraphrases")),
        ])
        tokens = candidate_pack_relevance_tokens(blob)
        if any(intent_alias_matches(blob, text) or len(tokens & candidate_pack_relevance_tokens(text)) >= minimum
               for text in excluded if clean_spaces(text)):
            continue
        allowed[document_id] = tokens
    found: List[str] = []
    queries = [assertion_text(a) for a in assertions
               if a.get("polarity") in {"advisory", "required"}]
    if include_visual_priorities:
        # These are already-authored observations, not requester assertions.
        # Keep them advisory and subject to the same opt-in/effect/lock guards.
        queries.extend(str(value) for value in core.get("visual_priorities") or []
                       if isinstance(value, str) and value.strip())
    if include_frozen_baseline:
        # Only the component-constrained profile lane opts into these
        # frozen authorial observations. They remain optional discoveries.
        queries.extend(str(core.get(field) or "") for field in
                       ("baseline_prompt_en", "interpreted_intent") if core.get(field))
    for query in queries:
        tokens = candidate_pack_relevance_tokens(query)
        eligible = {key for key, source_tokens in allowed.items() if len(tokens & source_tokens) >= minimum}
        for hit in rank_bm25f(bm25f, {"assertion_evidence": query}, allowed_ids=eligible,
                              limit=policy["maximum_per_assertion"]):
            document_id = str(hit.get("document_id") or "")
            if document_id and document_id not in found:
                found.append(document_id)
        if len(found) >= policy["maximum_candidates"]:
            break
    return found[:policy["maximum_candidates"]]


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


def candidate_pack_source_texts(result: JsonDict, trace: JsonDict) -> List[JsonDict]:
    texts: List[JsonDict] = []
    seen_texts: Set[str] = set()
    provenance = result.get("provenance") if isinstance(result.get("provenance"), dict) else {}
    core = provenance.get("authorial_core") or {}
    snapshot = provenance.get("creative_controls")
    visual_sources: Dict[str, List[str]] = {}
    if isinstance(snapshot, dict) and isinstance(core, dict):
        creative_controls.validate(snapshot, core.get("source_request"))
        if core.get("creative_controls_sha256") != snapshot["canonical_sha256"]:
            raise ValueError("source text controls must match the frozen authorial core")
        active_spans = (core.get("request_binding") or {}).get("active_spans", [])
        visual_spans, _ = creative_controls.split_request_spans(
            {"request_text": core.get("source_request"), "active_spans": active_spans},
            snapshot,
        )
        # Keep the raw request/provenance intact. Only visual fragments enter
        # composition requirements; a bound configuration-only span adds none.
        for span in active_spans:
            visual_sources[clean_spaces(span["text"])] = [
                row["text"] for row in visual_spans
                if row.get("source_span_id", row["span_id"]) == span["span_id"]
            ]

    def add_source(
        source: str,
        text: str,
        *,
        polarity: str,
        priority: str,
        mandatory: bool,
    ) -> None:
        fragments = visual_sources.get(clean_spaces(text), [text]) if mandatory else [text]
        for fragment in fragments:
            normalized = clean_spaces(fragment)
            key = normalized.lower()
            if not normalized or key in seen_texts:
                continue
            seen_texts.add(key)
            texts.append(
                {
                    "source": source,
                    "text": normalized,
                    "polarity": polarity,
                    "priority": priority,
                    "mandatory": mandatory,
                }
            )

    for concept in normalize_list(provenance.get("concept_lock")):
        no_people = intent_explicitly_excludes_people(concept)
        has_tone_constraint = text_explicitly_requests_nonsexual_moe(concept)
        add_source(
            "concept_lock",
            concept,
            polarity="mixed" if no_people or has_tone_constraint else "required",
            priority="critical",
            mandatory=True,
        )
    for requirement in normalize_list(provenance.get("user_mandatory_intents")):
        no_people = intent_explicitly_excludes_people(requirement)
        has_tone_constraint = text_explicitly_requests_nonsexual_moe(requirement)
        add_source(
            "user_requirement",
            requirement,
            polarity="mixed" if no_people or has_tone_constraint else "required",
            priority="critical",
            mandatory=True,
        )
    for requirement in normalize_list(provenance.get("additional_requirements")):
        no_people = intent_explicitly_excludes_people(requirement)
        has_tone_constraint = text_explicitly_requests_nonsexual_moe(requirement)
        add_source(
            "additional_requirement",
            requirement,
            polarity="mixed" if no_people or has_tone_constraint else "required",
            priority="critical",
            mandatory=True,
        )
    for requirement in normalize_list(provenance.get("negative_requirements")):
        add_source(
            "negative_requirement",
            requirement,
            polarity="excluded",
            priority="critical",
            mandatory=False,
        )
    for requirement in normalize_list(provenance.get("role_requirements")):
        add_source(
            "role_requirement",
            requirement,
            polarity="advisory",
            priority="support",
            mandatory=False,
        )
    for requirement in normalize_list(provenance.get("soft_requirements")):
        add_source(
            "soft_guidance",
            requirement,
            polarity="advisory",
            priority="support",
            mandatory=False,
        )
    authorial_core = (
        provenance.get("authorial_core")
        if isinstance(provenance.get("authorial_core"), dict)
        else {}
    )
    add_source(
        "authorial_core_interpretation",
        str(authorial_core.get("interpreted_intent") or ""),
        polarity="advisory",
        priority="critical",
        mandatory=False,
    )
    add_source(
        "authorial_core_baseline",
        str(authorial_core.get("baseline_prompt_en") or ""),
        polarity="advisory",
        priority="support",
        mandatory=False,
    )
    for definition in authorial_core.get("user_definitions") or []:
        if not isinstance(definition, dict):
            continue
        add_source(
            "authorial_core_definition",
            str(definition.get("interpreted_meaning") or ""),
            polarity="advisory",
            priority="critical",
            mandatory=False,
        )
    intent = str(trace.get("intent") or "").strip()
    if intent and trace.get("intent_source") == "user":
        no_people = intent_explicitly_excludes_people(intent)
        has_tone_constraint = text_explicitly_requests_nonsexual_moe(intent)
        add_source(
            "intent",
            intent,
            polarity="mixed" if no_people or has_tone_constraint else "required",
            priority="critical",
            mandatory=True,
        )
    return texts


def text_matches_any_pattern(text: str, patterns: Sequence[str]) -> bool:
    return any(re.search(pattern, str(text or ""), flags=re.IGNORECASE) for pattern in patterns)


def text_explicitly_requests_nonsexual_moe(text: str) -> bool:
    return text_matches_any_pattern(text, MOE_NONSEXUAL_PATTERNS)


def mask_patterns(text: str, patterns: Sequence[str]) -> str:
    masked = str(text or "")
    for pattern in patterns:
        masked = re.sub(pattern, " ", masked, flags=re.IGNORECASE)
    return clean_spaces(masked)


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
    masked = mask_patterns(masked, MOE_NONSEXUAL_PATTERNS)
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


def typed_core_routing_text(value: str) -> str:
    """Keep animal-ear modifiers from becoming an animal subject route."""

    return clean_spaces(
        re.sub(
            r"(?i)\b[a-z]+(?:[- ]eared|\s+ears)\b",
            " ",
            str(value or ""),
        )
    )


@functools.lru_cache(maxsize=65_536)
def intent_term_is_negated(text: str, term: str) -> bool:
    """Return whether one otherwise-positive term is locally negated.

    This is deliberately shared by ordinary intent aliases and visual-concept
    routing.  A concept must not become positive merely because one caller has
    a narrower negation vocabulary than another.
    """

    lowered = clean_spaces(str(text or "").lower())
    normalized = clean_spaces(str(term or "").lower())
    if not lowered or not normalized:
        return False
    if normalized.isascii() and re.search(r"[a-z0-9]", normalized):
        term_pattern = (
            r"(?<![a-z0-9])" + re.escape(normalized) + r"(?:s|es)?(?![a-z0-9])"
        )
        return bool(
            re.search(
                rf"(?<![a-z0-9])(?:no|without|exclude|excluding|omit|omitting|avoid|avoiding|"
                rf"not(?:\s+(?:include|use|show|add))?)"
                rf"(?:\s+(?:a|an|any|the))?\s+{term_pattern}",
                lowered,
            )
            or re.search(
                rf"{term_pattern}(?:\s+(?:concept|element|expression|pose|style|emphasis|keyword))?"
                r"\s*(?:is|are|must\s+be|should\s+be)?\s*"
                r"(?:excluded|omitted|forbidden|not\s+wanted|not\s+included)",
                lowered,
            )
        )
    escaped = re.escape(normalized)
    korean_suffix = (
        r"(?:\s*(?:요소|표현|장면|포즈|강조|개념|스타일|키워드))?"
        r"\s*(?:은|는|이|가|을|를|도)?\s*"
        r"(?:없는|없이|아닌|빼(?:고|줘|주세요)?|제외(?:하고|해|해주세요)?|"
        r"금지|말고|하지\s*마|넣지\s*마|안\s*넣)"
    )
    korean_prefix = (
        r"(?:빼고|제외하고|금지하고|넣지\s*말고|사용하지\s*말고)"
        rf"[^,;.]{{0,12}}{escaped}"
    )
    japanese_suffix = (
        rf"{escaped}(?:\s*(?:要素|表現|ラベル|ポーズ|強調|概念|スタイル))?"
        r"\s*(?:は|を|が|も|の)?\s*(?:なし|抜き|除外|禁止|不要)"
    )
    return bool(
        re.search(
            rf"(?<![a-z0-9])(?:no|without|exclude|excluding|omit|omitting|avoid|avoiding|"
            rf"not(?:\s+(?:include|use|show|add))?)"
            rf"(?:\s+(?:a|an|any|the))?\s+{escaped}",
            lowered,
        )
        or re.search(rf"{escaped}{korean_suffix}", lowered)
        or re.search(korean_prefix, lowered)
        or re.search(japanese_suffix, lowered)
    )


@functools.lru_cache(maxsize=65_536)
def intent_alias_matches(text: str, alias: str) -> bool:
    normalized_text = clean_spaces(
        re.sub(r"[-\u2013\u2014/]+", " ", str(text or "").lower().replace("_", " "))
    )
    normalized_alias = clean_spaces(
        re.sub(r"[-\u2013\u2014/]+", " ", str(alias or "").lower().replace("_", " "))
    )
    if not normalized_text or not normalized_alias:
        return False
    # Every literal alias match (including an English plural) contains the
    # normalized alias. Avoid compiling negation expressions for absent terms.
    if normalized_alias not in normalized_text:
        return False
    if intent_term_is_negated(normalized_text, normalized_alias):
        return False
    if normalized_alias.isascii() and re.search(r"[a-z0-9]", normalized_alias):
        plural_suffix = ""
        final_word = normalized_alias.rsplit(" ", 1)[-1]
        if final_word.isalpha() and not final_word.endswith("s"):
            plural_suffix = r"(?:s|es)?"
        pattern = (
            r"(?<![a-z0-9])"
            + re.escape(normalized_alias)
            + plural_suffix
            + r"(?![a-z0-9])"
        )
        return re.search(pattern, normalized_text) is not None
    # General intent aliases retain CJK substring matching. Typed character
    # response activation is owned by the frozen core, not this helper.
    return normalized_alias in normalized_text


def resolve_request_intent_constraints(
    data: JsonDict,
    semantic_context: Optional[JsonDict],
    generation_contract: Optional[JsonDict],
    *,
    authorial_core: Optional[JsonDict] = None
) -> JsonDict:
    if not isinstance(authorial_core, dict):
        embedded_core = (generation_contract or {}).get("_authorial_core")
        authorial_core = embedded_core if isinstance(embedded_core, dict) else None
    typed_v3 = bool(
        isinstance(authorial_core, dict)
        and authorial_core.get("contract_version") == AUTHORIAL_CORE_V3_CONTRACT_VERSION
    )
    if typed_v3:
        assert isinstance(authorial_core, dict)
        values = [
            str(authorial_core.get('interpreted_intent') or ''),
            str(authorial_core.get('subject') or ''),
            str(authorial_core.get('setting') or ''),
            str(authorial_core.get('event') or ''),
            *normalize_list(authorial_core.get("visual_priorities")),
        ]
        for assertion in authorial_core.get("semantic_assertions") or []:
            if not isinstance(assertion, dict) or assertion.get("polarity") == "excluded":
                continue
            axes = assertion.get("axes") if isinstance(assertion.get("axes"), dict) else {}
            for value in axes.values():
                values.extend(normalize_list(value))
    else:
        values = [str((semantic_context or {}).get('intent') or '')]
        for key in ("concept_locks", "user_mandatory_intents", "additional_requirements"):
            values.extend(normalize_list((generation_contract or {}).get(key)))
    texts: List[str] = []
    seen_texts: Set[str] = set()
    for value in values:
        normalized = typed_core_routing_text(value) if typed_v3 else clean_spaces(value)
        dedupe_key = normalized.lower()
        if normalized and dedupe_key not in seen_texts:
            texts.append(normalized)
            seen_texts.add(dedupe_key)
    subject_texts = (
        [typed_core_routing_text(str(authorial_core.get('subject') or ''))]
        if typed_v3 and isinstance(authorial_core, dict)
        else texts
    )
    policy = candidate_pack_intent_routing_policy(data)
    categories: Set[str] = set()
    subject_entry_ids: Set[str] = set()
    subject_entry_categories: Dict[str, str] = {}
    domains: Set[str] = set()
    matched: List[JsonDict] = []
    catalog_subject_ids = {
        str(entry.get('id') or '')
        for entry in (data.get("slots") or {}).get("subject") or []
        if isinstance(entry, dict) and str(entry.get('id') or '')
    }
    for rule in policy.get("subject_routes") or []:
        if not isinstance(rule, dict):
            continue
        entry_id = str(rule.get('entry_id') or '')
        category = str(rule.get('category') or '')
        aliases = normalize_list(rule.get("aliases"))
        hits = sorted(
            {
                alias
                for text in subject_texts
                for alias in aliases
                if intent_alias_matches(text, alias)
            }
        )
        if entry_id in catalog_subject_ids and category in VALID_SUBJECT_CATEGORIES and hits:
            subject_entry_ids.add(entry_id)
            subject_entry_categories[entry_id] = category
            categories.add(category)
            matched.append(
                {
                    "axis": "subject_entry",
                    "value": entry_id,
                    "category": category,
                    "aliases": hits[:8],
                }
            )
    for rule in policy.get("subject_categories") or []:
        if not isinstance(rule, dict):
            continue
        category = str(rule.get('category') or '')
        aliases = normalize_list(rule.get("aliases"))
        hits = sorted(
            {
                alias
                for text in subject_texts
                for alias in aliases
                if intent_alias_matches(text, alias)
            }
        )
        if category in VALID_SUBJECT_CATEGORIES and hits:
            categories.add(category)
            matched.append({"axis": "subject_category", "value": category, "aliases": hits[:8]})
    for rule in policy.get("domains") or []:
        if not isinstance(rule, dict):
            continue
        domain = str(rule.get('domain') or '')
        aliases = normalize_list(rule.get("aliases"))
        hits = sorted(
            {alias for text in texts for alias in aliases if intent_alias_matches(text, alias)}
        )
        if domain in VALID_INTENT_DOMAINS and hits:
            domains.add(domain)
            matched.append({"axis": "domain", "value": domain, "aliases": hits[:8]})
    authorial_core_constraints = (
        (generation_contract or {}).get("authorial_core_constraints")
        if isinstance((generation_contract or {}).get("authorial_core_constraints"), dict)
        else {}
    )
    no_people = any((intent_explicitly_excludes_people(text) for text in texts)) or bool(
        authorial_core_constraints.get("no_people")
    )
    character_response = resolve_character_response_intent(authorial_core)
    if typed_v3 and character_response.get("enabled") is True:
        matched.append(
            {
                "axis": "character_response",
                "value": str(character_response.get('source_assertion_id') or ''),
                "source": "authorial_core_semantic_assertion",
            }
        )
    if no_people:
        categories.discard("human")
        subject_entry_ids = {
            entry_id
            for entry_id in subject_entry_ids
            if subject_entry_categories.get(entry_id) != "human"
        }
        matched = [
            row
            for row in matched
            if not (
                row.get("axis") == "subject_category"
                and row.get("value") == "human"
                or (row.get("axis") == "subject_entry" and row.get("category") == "human")
            )
        ]
    resolved = {
        "no_people": no_people,
        **({"subject_entry_ids": sorted(subject_entry_ids)} if subject_entry_ids else {}),
        "subject_categories": sorted(categories),
        "domains": sorted(domains),
        "character_response": character_response,
        "matched": matched,
        "source_text_count": len(texts),
    }
    if typed_v3:
        resolved["routing_input"] = "authorial_core_typed_semantics"
    return resolved


def candidate_pack_intent_contract(
    data: JsonDict, result: JsonDict, trace: JsonDict, candidate_blobs: Dict[str, str]
) -> List[JsonDict]:
    rows: List[JsonDict] = []
    seen: Set[tuple[str, str]] = set()
    policy = candidate_pack_intent_routing_policy(data)
    provenance = result.get("provenance") if isinstance(result.get("provenance"), dict) else {}
    authorial_core = (
        provenance.get("authorial_core")
        if isinstance(provenance.get("authorial_core"), dict)
        else {}
    )
    typed_v3 = authorial_core.get("contract_version") == AUTHORIAL_CORE_V3_CONTRACT_VERSION
    generation_contract = (
        trace.get("generation_contract")
        if isinstance(trace.get("generation_contract"), dict)
        else {}
    )
    typed_constraints = (
        generation_contract.get("intent_constraints")
        if typed_v3 and isinstance(generation_contract.get("intent_constraints"), dict)
        else {}
    )
    typed_facets = [
        f"{item.get('axis')}:{item.get('value')}"
        for item in typed_constraints.get("matched") or []
        if isinstance(item, dict)
        and str(item.get('axis') or '') in {"subject_entry", "subject_category", "domain"}
        and str(item.get('value') or '')
    ]
    typed_character_response = resolve_character_response_intent(authorial_core)
    for source_row in candidate_pack_source_texts(result, trace):
        source = str(source_row.get('source') or '')
        source_text = str(source_row.get('text') or '')
        key = (source, source_text.lower())
        if key in seen:
            continue
        seen.add(key)
        no_people = (
            bool(typed_constraints.get("no_people"))
            if typed_v3
            else intent_explicitly_excludes_people(source_text)
        )
        facets: List[str] = list(typed_facets) if typed_v3 else []
        if not typed_v3:
            for rule in policy.get("subject_routes") or []:
                if not isinstance(rule, dict):
                    continue
                entry_id = str(rule.get('entry_id') or '')
                category = str(rule.get('category') or '')
                if no_people and category == "human":
                    continue
                if entry_id and any(
                    (
                        intent_alias_matches(source_text, alias)
                        for alias in normalize_list(rule.get("aliases"))
                    )
                ):
                    facets.append(f"subject_entry:{entry_id}")
            for axis, name_key, value_key in (
                ("subject_category", "subject_categories", "category"),
                ("domain", "domains", "domain"),
            ):
                for rule in policy.get(name_key) or []:
                    if not isinstance(rule, dict):
                        continue
                    value = str(rule.get(value_key) or '')
                    if no_people and axis == "subject_category" and (value == "human"):
                        continue
                    if value and any(
                        (
                            intent_alias_matches(source_text, alias)
                            for alias in normalize_list(rule.get("aliases"))
                        )
                    ):
                        facets.append(f"{axis}:{value}")
        character_response = (
            typed_character_response
            if typed_v3
            else resolve_character_response_intent(authorial_core)
        )
        if typed_v3 and character_response.get("enabled") is True:
            facets.append(f"character_response:{character_response.get('source_assertion_id')}")
        meaningful_terms = candidate_pack_tokenize_intent_text(source_text)
        covered_by = [
            candidate_id
            for candidate_id, blob in candidate_blobs.items()
            if any((str(term).lower() in blob for term in meaningful_terms))
        ][:12]
        constraints = ["no_people"] if no_people else []
        if not typed_v3 and text_explicitly_requests_nonsexual_moe(source_text):
            constraints.append("sexual_tone:nonsexual")
        if typed_v3 and character_response.get("enabled") is True:
            constraints.extend(
                [
                    "character_response:typed_semantic_assertion",
                    "retrieval_candidates:advisory_only",
                ]
            )
        rows.append(
            {
                "id": f"intent:{stable_text_id(f'{source}|{source_text}', 12)}",
                "text": source_text,
                "source": source,
                "polarity": source_row.get("polarity") or ("excluded" if no_people else "required"),
                "priority": source_row.get("priority") or "critical",
                "axis_hints": sorted(set(facets)),
                "constraints": constraints,
                "coverage_mode": "literal_or_asserted_translation",
                "status": "covered" if covered_by else "uncovered",
                "covered_by": covered_by,
            }
        )
    return rows


def candidate_pack_candidate_blobs(slots: JsonDict) -> Dict[str, str]:
    blobs: Dict[str, str] = {}
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
                    str(candidate.get("label_en") or ""),
                    str(candidate.get("label_ko") or ""),
                ],
            )
    return blobs


def candidate_pack_mandatory_intents(
    result: JsonDict, trace: JsonDict, candidate_blobs: Dict[str, str]
) -> tuple[List[JsonDict], List[JsonDict]]:
    intents: List[JsonDict] = []
    seen: Set[tuple[str, str]] = set()
    provenance = result.get("provenance") if isinstance(result.get("provenance"), dict) else {}
    authorial_core = (
        provenance.get("authorial_core")
        if isinstance(provenance.get("authorial_core"), dict)
        else {}
    )
    typed_v3 = authorial_core.get("contract_version") == AUTHORIAL_CORE_V3_CONTRACT_VERSION
    intent_anchors = (
        (authorial_core.get("intent_lock") or {}).get("semantic_anchors") or []
        if authorial_core.get("contract_version") in AUTHORIAL_CORE_MODERN_CONTRACT_VERSIONS
        and isinstance(authorial_core.get("intent_lock"), dict)
        else []
    )
    for source_row in candidate_pack_source_texts(result, trace):
        if source_row.get("mandatory") is not True:
            continue
        source = str(source_row.get('source') or '')
        source_text = str(source_row.get('text') or '')
        character_response = resolve_character_response_intent(authorial_core)
        positive_source_text = source_text
        anchored_terms = [
            clean_spaces(str(anchor.get('prompt_evidence') or ''))
            for anchor in intent_anchors
            if isinstance(anchor, dict)
            and str(anchor.get('source_text') or '').casefold() in source_text.casefold()
            and clean_spaces(str(anchor.get('prompt_evidence') or ''))
        ]
        if anchored_terms and source in {
            "concept_lock",
            "intent",
            "user_requirement",
            "additional_requirement",
        }:
            intent_terms = list(dict.fromkeys(anchored_terms))
        elif source in {"concept_lock", "intent"} or intent_explicitly_excludes_people(source_text):
            intent_terms = [
                term
                for term in candidate_pack_tokenize_intent_text(positive_source_text)
                if not intent_explicitly_excludes_people(term)
            ]
        else:
            intent_terms = [positive_source_text] if positive_source_text else []
        for token in intent_terms:
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
            audit_terms = [token]
            intents.append(
                {
                    "text": token,
                    "source": source,
                    "source_text": source_text,
                    "status": "covered" if covered_by else "uncovered",
                    "covered_by": covered_by,
                    "audit_terms": list(
                        dict.fromkeys((term for term in audit_terms if str(term).strip()))
                    )[:12],
                }
            )
    uncovered = [intent for intent in intents if intent.get("status") == "uncovered"]
    return (intents, uncovered)


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


def candidate_pack_creativity_level(provenance: JsonDict) -> Optional[int]:
    value = provenance.get("creativity")
    if value is not None:
        creativity_sampling_strength(value)
    return value


def candidate_pack_creative_exploration(
    result: JsonDict,
    slots: JsonDict,
    candidate_entries: Dict[str, tuple[str, Optional[str], JsonDict]],
) -> Optional[JsonDict]:
    provenance = result.get("provenance") if isinstance(result.get("provenance"), dict) else {}
    creativity = candidate_pack_creativity_level(provenance)
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
                or applicability.get("source") != "frozen_core_slot_contract"
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
                    "applicability_source": "frozen_core_slot_contract",
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
        "source": "exposed_core_eligible_pool",
        "contrast_candidate_count": len(contrast_rows),
        "contrast_candidates": contrast_rows,
        "composition_guidance": {
            "keep": ["frozen_core_subject", "mandatory_intents", "scene_contract"],
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
    creativity = candidate_pack_creativity_level(provenance)
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
                "frozen_core_subject",
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


def authorial_core_intent_dimension_scope(core: Any) -> JsonDict:
    """Return the explicit versioned dimension boundary for downstream defaults."""

    if (
        not isinstance(core, dict)
        or core.get("contract_version") not in AUTHORIAL_CORE_MODERN_CONTRACT_VERSIONS
    ):
        return {"enabled": False}
    allowed_dimensions = (
        AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS
        if core.get("contract_version") == AUTHORIAL_CORE_V3_CONTRACT_VERSION
        else INTENT_LOCK_DIMENSIONS
    )
    intent_lock = core.get("intent_lock") if isinstance(core.get("intent_lock"), dict) else {}
    locked_dimensions = [
        str(item)
        for item in intent_lock.get("locked_dimensions") or []
        if str(item) in allowed_dimensions
    ]
    open_dimensions = [
        str(item)
        for item in intent_lock.get("open_dimensions") or []
        if str(item) in allowed_dimensions
    ]
    return {
        "enabled": True,
        "source_intent_lock_sha256": str(intent_lock.get("canonical_sha256") or ""),
        "locked_dimensions": locked_dimensions,
        "open_dimensions": open_dimensions,
        "closed_dimensions": sorted(allowed_dimensions - set(open_dimensions)),
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
    creativity = candidate_pack_creativity_level(provenance)
    explicitly_requested = provenance.get("viewer_experience_requested") is True
    creative_direction_required = bool(
        creativity is not None and creativity >= CANDIDATE_PACK_CREATIVE_DIRECTION_FLOOR
    )
    response = (
        provenance.get("character_response")
        if isinstance(provenance.get("character_response"), dict)
        else {}
    )
    core = (
        provenance.get("authorial_core")
        if isinstance(provenance.get("authorial_core"), dict)
        else {}
    )
    typed_response = resolve_character_response_intent(core)
    character_response_required = bool(typed_response.get("enabled") is True)
    if (
        not explicitly_requested
        and (not creative_direction_required)
        and (not character_response_required)
    ):
        return None
    activation_sources = []
    if explicitly_requested:
        activation_sources.append("explicit_viewer_experience_control")
    if creative_direction_required:
        activation_sources.append("creative_direction_required")
    if character_response_required:
        activation_sources.append("typed_character_response_required")
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
            "select_exactly_one": [
                "primary_viewer_need",
                "intended_experience",
                "commercial_objective",
            ],
            "bind_visible_causes_not_outcome_claims": True,
            "keep": [
                "creative_direction",
                "character_response",
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


def candidate_pack_adult_policy(data: JsonDict) -> JsonDict:
    policy = candidate_pack_quality_layers(data).get("adult_appeal")
    return policy if isinstance(policy, dict) else {}


def candidate_pack_adult_appeal_request(data: JsonDict, result: JsonDict) -> JsonDict:
    snapshot = (result.get("provenance") or {}).get("creative_controls")
    if not isinstance(snapshot, dict):
        raise ValueError("adult appeal requires a bound current creative-control snapshot")
    axes = {axis: {"intensity": snapshot["adult_appeal"][axis]["effective_intensity"]}
            for axis in CANDIDATE_PACK_ADULT_APPEAL_AXES}
    requested = any(row["intensity"] > 0 for row in axes.values())
    reasons = {axis: snapshot["adult_appeal"][axis]["reason"] for axis in axes}
    eligible = "eligible" in reasons.values()
    return {"enabled": requested and eligible, "requested_enabled": requested,
            "activation_source": "precore_controls", "axes": axes,
            "eligibility": {"status": "eligible" if eligible else "ineligible",
                "reason": "resolved_precore_context", "axis_reasons": reasons,
                "subject_category": snapshot["context"]["subject_category"]},
            "blend": {"emphasis": snapshot["resolved_emphasis"]}}


def candidate_pack_adult_risk_groups(entry_id: str, adult_policy: JsonDict) -> List[str]:
    groups: List[str] = []
    risk_groups = adult_policy.get("risk_groups") if isinstance(adult_policy.get("risk_groups"), dict) else {}
    for group_id, group in risk_groups.items():
        if not isinstance(group, dict):
            continue
        if entry_id in {str(item) for item in group.get("entry_ids") or []}:
            groups.append(str(group_id))
    return groups


def candidate_pack_adult_appeal_metadata(
    data: JsonDict,
    result: JsonDict,
    candidate_entries: Dict[str, tuple[str, Optional[str], JsonDict]],
    *,
    authorial_core: Optional[JsonDict] = None,
) -> Optional[JsonDict]:
    adult_policy = candidate_pack_adult_policy(data)
    request = candidate_pack_adult_appeal_request(data, result)
    enabled = bool(request.get("enabled"))
    dimension_scope = None
    if isinstance(authorial_core, dict) and authorial_core.get("contract_version") == AUTHORIAL_CORE_V3_CONTRACT_VERSION:
        intent_lock = authorial_core.get("intent_lock") or {}
        locked = set(intent_lock.get("locked_dimensions") or [])
        dimension_scope = {
            "contract_version": photo_contextual_appeal.SCOPE_VERSION,
            "policy": "preserve_locked_dimensions",
            "source_intent_lock_sha256": str(intent_lock.get("canonical_sha256") or ""),
            "locked_dimensions": sorted(locked),
            "axis_allowed_dimensions": {
                axis: sorted(photo_contextual_appeal.allowed_dimensions(intent_lock))
                for axis in CANDIDATE_PACK_ADULT_APPEAL_AXES
            },
            "protected_properties": intent_property_locks(intent_lock),
        }
    axes: JsonDict = {}
    for axis_id in CANDIDATE_PACK_ADULT_APPEAL_AXES:
        intensity = int(((request.get("axes") or {}).get(axis_id) or {}).get("intensity", 0) or 0)
        requested_intensity = intensity
        allowed_dimensions = (
            set(dimension_scope["axis_allowed_dimensions"][axis_id])
            if dimension_scope is not None else None
        )
        if allowed_dimensions is not None and not allowed_dimensions:
            intensity = 0
        inventory: List[JsonDict] = []
        axes[axis_id] = {
            "intensity": intensity,
            "active": enabled and intensity > 0,
            "carrier_ids": [],
            "candidate_inventory": inventory,
        }
        if dimension_scope is not None:
            axes[axis_id]["requested_intensity"] = requested_intensity
        snapshot = (result.get("provenance") or {}).get("creative_controls")
        definitions = snapshot["definitions"]
        axes[axis_id]["intensity_meaning"] = definitions["controls"][axis_id]["levels"][str(intensity)]
        axes[axis_id]["definition"] = definitions["controls"][axis_id]["definition"]
        if isinstance(snapshot, dict):
            axes[axis_id]["configured_intensity"] = snapshot["adult_appeal"][axis_id]["requested_intensity"]
            axes[axis_id]["configuration_source"] = snapshot["controls"][axis_id]["source"]

    if dimension_scope is not None:
        enabled = any(axis["active"] for axis in axes.values())

    configured_defaults = {
        axis: int(definitions["controls"][axis]["default"])
        for axis in CANDIDATE_PACK_ADULT_APPEAL_AXES
    }
    configured_emphasis = definitions["controls"]["adult_appeal_emphasis"]["default"]
    if configured_emphasis == "auto":
        sensual_default, fetish_default = (configured_defaults[axis] for axis in CANDIDATE_PACK_ADULT_APPEAL_AXES)
        configured_emphasis = "balanced" if sensual_default == fetish_default else ("sensual_led" if sensual_default > fetish_default else "fetish_led")
    contract = {
        "enabled": enabled,
        "requested_enabled": bool(request.get("requested_enabled")),
        "contract_version": CANDIDATE_PACK_ADULT_APPEAL_CONTRACT_VERSION,
        "activation_source": request.get("activation_source"),
        "eligibility": request.get("eligibility", {}),
        "defaults": {
            "sensual_intensity": configured_defaults["sensual"],
            "fetish_intensity": configured_defaults["fetish"],
            "emphasis": configured_emphasis,
        },
        "axes": axes,
        "blend": {
            "emphasis": str((request.get("blend") or {}).get("emphasis") or "balanced"),
            "simultaneous_activation_allowed": True,
            "carrier_separation": {
                "sensual": ["gaze", "pose", "lighting", "silhouette", "wardrobe", "material"],
                "fetish": ["material", "garment_layering", "accessories", "footwear"],
            },
        },
        "composition_requirements": {
            "explicit_adult_original_subject": True,
            "adult_subject_phrase_required": True,
            "agency_phrase_required": True,
            "intensity_is_ordinal_not_exposure_or_detail_count": True,
            "baseline_expression_may_be_retained": True,
            "shared_styling_between_axes_allowed": True,
            "appearance_or_popularity_inference_forbidden": True,
        },
        "combination_policy": {
            "risk_groups": adult_policy.get("risk_groups", {}),
            "hard_combinations": adult_policy.get("hard_combinations", []),
            "warning_combinations": adult_policy.get("warning_combinations", []),
        },
        "evaluation_boundary": "configuration_scope_and_literal_binding_are_preflight;_perceived_intensity_requires_image_review;_appeal_requires_user_judgment",
    }
    if dimension_scope is not None:
        contract["dimension_scope"] = dimension_scope
        contract["composition_requirements"]["affected_dimensions_per_active_axis"] = True
        contract["blend"]["requested_emphasis"] = contract["blend"]["emphasis"]
        active_axes = [axis_id for axis_id, axis in axes.items() if axis["active"]]
        if len(active_axes) == 1:
            contract["blend"]["emphasis"] = "sensual_led" if active_axes[0] == "sensual" else "fetish_led"
        elif not active_axes:
            contract["blend"]["emphasis"] = "balanced"
    return contract


def candidate_pack_contextual_adult_appeal(
    data: JsonDict,
    result: JsonDict,
    candidate_entries: Dict[str, tuple[str, Optional[str], JsonDict]],
    *,
    authorial_core: Optional[JsonDict] = None,
) -> Optional[JsonDict]:
    policy = candidate_pack_adult_policy(data)
    retrieval_policy = policy.get("contextual_retrieval") or {}
    snapshot = (result.get("provenance") or {}).get("creative_controls")
    modern = bool(
        authorial_core
        and authorial_core.get("creative_controls_sha256")
        and isinstance(snapshot, dict)
        and retrieval_policy.get("contract_version") == photo_contextual_appeal.VERSION
    )
    if not modern:
        raise ValueError(
            "current adult appeal requires the frozen core, creative-control snapshot and contextual policy"
        )

    contract = candidate_pack_adult_appeal_metadata(data, result, {}, authorial_core=authorial_core)
    core = authorial_core
    lock = core["intent_lock"]
    locked = set(lock.get("locked_dimensions") or [])
    scope = contract["dimension_scope"]
    scope["contract_version"] = photo_contextual_appeal.SCOPE_VERSION
    scope["axis_allowed_dimensions"] = {
        axis: sorted(photo_contextual_appeal.allowed_dimensions(lock))
        for axis in photo_contextual_appeal.AXES
    }
    intensities = {axis: row["requested_intensity"] for axis, row in contract["axes"].items()}
    queries = photo_contextual_appeal.queries(
        core, snapshot["definitions"], intensities, authorial_core_retrieval_text
    )
    scene_query, _ = authorial_core_retrieval_text(
        {
            key: value
            for key, value in core.items()
            if key
            in {
                "contract_version",
                "request_binding",
                "source_request",
                "user_definitions",
                "user_exclusions",
            }
        }
    )
    prompt_id = str((result.get("provenance") or {}).get("prompt_id") or "")
    cached = (data.get(photo_contextual_appeal.QUERY_CACHE) or {}).get(prompt_id) or {}
    vectors = cached.get("vectors", {}) if cached.get("queries") == queries else {}
    constraints = {
        "subject_category": snapshot["context"]["subject_category"],
        "domains": [],
        "adult_allowed": contract["eligibility"]["status"] == "eligible",
        "intent_constraints": authorial_core_generation_constraints(core, creative_control_snapshot=snapshot),
    }
    exclusions = [
        candidate_pack_relevance_tokens(value) for value in core.get("user_exclusions") or []
    ]
    excluded_identity_slots = {
        "subject",
        "appearance_type",
        "age",
        "species",
        "species_morphology",
        "face",
        "body_type",
        "person_origin",
    }
    review_ids = []
    traces = {}
    for axis, axis_row in contract["axes"].items():
        allowed = set(scope["axis_allowed_dimensions"][axis])
        axis_row["intensity"] = intensities[axis] if allowed else 0
        axis_row["active"] = bool(axis_row["intensity"] and constraints["adult_allowed"])
        axis_row["intensity_meaning"] = snapshot["definitions"]["controls"][axis]["levels"][
            str(axis_row["intensity"])
        ]
        axis_row["candidate_inventory"] = []
        axis_row["carrier_ids"] = []
        if not axis_row["active"]:
            continue
        rows = []
        sources = {}
        for slot, entries in data.get("slots", {}).items():
            if slot in excluded_identity_slots or slot_block_reason(data, slot, constraints):
                continue
            for entry in entries:
                source_key = f"{slot}:{entry['id']}"
                dimensions = sorted(
                    set(entry.get("affected_dimensions") or [])
                    | set((policy.get("entry_dimensions") or {}).get(source_key) or [])
                )
                dimensions = dimensions or photo_candidate_semantics.slot_dimensions(
                    slot, data.get("candidate_semantic_policy")
                )
                if (
                    not dimensions
                    or not set(dimensions).issubset(allowed)
                    or not property_effects_allowed(
                        lock, dimensions, entry.get("affected_properties", [])
                    )
                    or entry_block_reason(entry, slot, constraints)
                    or not compatible_with_facet_guards(entry, {})
                ):
                    continue
                # Requirements that need other garments or scene objects are
                # supplied as context, never silently presumed to be satisfied.
                fields = semantic_bm25f_fields_for_entry(entry, slot, kind="slot")
                text = [str(value) for values in fields.values() for value in values]
                tokens = candidate_pack_relevance_tokens(" ".join(text))
                if any(group and group <= tokens for group in exclusions):
                    continue
                candidate_id = f"augmentation:adult_appeal:{axis}:{source_key}"
                sources[candidate_id] = ("slot", slot, entry)
                rows.append(
                    {
                        "id": candidate_id,
                        "source_candidate_id": f"slot:{source_key}",
                        "slot": slot,
                        "entry_id": entry["id"],
                        "axis": axis,
                        "carrier": slot,
                        "label_en": localize(entry, "en") or entry["id"],
                        "label_ko": localize(entry, "ko") or entry["id"],
                        "expression_scope": entry.get("expression_scope")
                        or photo_contextual_appeal.expression_scope(slot),
                        "affected_dimensions": dimensions,
                        "affected_properties": copy.deepcopy(
                            entry.get("affected_properties") or []
                        ),
                        "contextual_usage": copy.deepcopy(entry.get("contextual_usage") or {}),
                        "applicability": {
                            "status": "eligible",
                            "source": "contextual_corpus_retrieval",
                            "basis": "writable_scope",
                            "reason": "scope compatible; scene and aesthetic interpretation pending",
                        },
                        "risk_groups": candidate_pack_adult_risk_groups(entry["id"], policy),
                        "conflicts_with": [],
                        "search_fields": fields,
                        "visual_text": text,
                        "_v6_semantic_source": photo_candidate_semantics.semantic_source(
                            dict(entry, affected_dimensions=dimensions),
                            slot,
                            data.get("candidate_semantic_policy"),
                        ),
                    }
                )
        inventory, traces[axis] = photo_contextual_appeal.rank_candidates(
            rows,
            queries[axis],
            policy=SEMANTIC_BM25F_POLICY,
            query_vectors=vectors.get(axis),
            index=data.get(SEMANTIC_INDEX_DATA_KEY),
            limit=int(retrieval_policy.get("candidate_limit_per_axis", 12)),
            scene_query=scene_query,
        )
        for row in inventory:
            _, slot, entry = sources[row["id"]]
            row.update(photo_contextual_appeal.compile_context(
                entry, row["source_candidate_id"],
                quality_layer_primary_context_requirement_sources(data, slot, entry),
            ))
        axis_row["candidate_inventory"] = inventory
        axis_row["carrier_ids"] = sorted({row["carrier"] for row in inventory})
        candidate_entries.update({row["id"]: sources[row["id"]] for row in inventory})
        review_ids.extend(
            photo_contextual_appeal.review_ids(
                inventory, int(retrieval_policy.get("review_limit_per_axis", 4))
            )
        )
    active = [axis for axis, row in contract["axes"].items() if row["active"]]
    contract["enabled"] = bool(active)
    contract["blend"]["emphasis"] = (
        contract["blend"]["requested_emphasis"]
        if len(active) == 2
        else ("sensual_led" if active == ["sensual"] else "fetish_led" if active else "balanced")
    )
    contract["blend"].pop("carrier_separation", None)
    contract["contextual_retrieval"] = {
        "contract_version": photo_contextual_appeal.VERSION,
        "axes": traces,
        "review_candidate_ids": review_ids,
        "candidate_adoption_required": False,
        "review_location": "adult_appeal_brief.contextual_review",
        "comparison_location": "adult_appeal_brief.contextual_comparison",
        "query_sha256": canonical_json_sha256(queries),
        "interpretation_owner": "composer_in_current_scene",
        "comparison_policy": "baseline_and_coherent_alternatives_at_same_requested_strengths",
        "adoption_context_contract_version": photo_contextual_appeal.CONTEXT_VERSION,
    }
    return contract


def candidate_pack_adult_candidates(adult_appeal: Optional[JsonDict]) -> List[JsonDict]:
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


def authorial_request_content_words(text: str) -> List[str]:
    stopwords = {
        "a",
        "an",
        "and",
        "as",
        "at",
        "by",
        "for",
        "from",
        "in",
        "into",
        "of",
        "on",
        "or",
        "the",
        "to",
        "with",
    }
    return [
        token.lower()
        for token in re.findall(r"[A-Za-z0-9][A-Za-z0-9_-]*|[가-힣]{2,}|[ぁ-んァ-ン一-龯]{2,}", str(text or ""))
        if token.lower() not in stopwords
    ]


def authorial_prompt_budget_contract() -> JsonDict:
    return {
        "contract_version": AUTHORIAL_PROMPT_BUDGET_CONTRACT_VERSION,
        "language": "en",
        "minimum_words": AUTHORIAL_PROMPT_MIN_WORDS,
        "recommended_maximum_words": AUTHORIAL_PROMPT_RECOMMENDED_MAX_WORDS,
        "absolute_maximum_words": AUTHORIAL_PROMPT_ABSOLUTE_MAX_WORDS,
        "required_evidence_headroom_words": AUTHORIAL_PROMPT_REQUIRED_EVIDENCE_HEADROOM_WORDS,
        "counting_rule": "ascii_words_with_internal_hyphens_or_apostrophes",
        "policy": {
            "recommended_maximum_is_warning": True,
            "absolute_bounds_are_blocking": True,
            "required_evidence_expands_advisory_ceiling": True,
            "requester_meaning_outranks_concision": True,
        },
    }


def normalize_request_envelope(payload: Any) -> JsonDict:
    """Validate the requesting-user text before an agent authors a v2 core.

    The envelope is intentionally separate from the core.  It gives the CLI a
    second, exact source of truth and lets a multi-part request select only
    byte-grounded spans instead of inventing a per-arm paraphrase.
    """

    if not isinstance(payload, dict):
        raise ValueError("--request-envelope-json must contain one JSON object")
    allowed_fields = {
        "contract_version",
        "provenance",
        "request_id",
        "request_text",
        "request_sha256",
        "active_spans",
    }
    unknown_fields = sorted(set(payload) - allowed_fields)
    if unknown_fields:
        raise ValueError(
            "request envelope contains unsupported fields: "
            + ", ".join(unknown_fields)
        )
    if payload.get("contract_version") != REQUEST_ENVELOPE_CONTRACT_VERSION:
        raise ValueError(
            "request envelope contract_version must be "
            f"{REQUEST_ENVELOPE_CONTRACT_VERSION!r}"
        )
    if payload.get("provenance") != "requesting_user":
        raise ValueError("request envelope provenance must be 'requesting_user'")

    request_id = str(payload.get("request_id") or "").strip()
    if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}", request_id) is None:
        raise ValueError(
            "request envelope request_id must be a stable 1-128 character identifier"
        )
    request_text = payload.get("request_text")
    if not isinstance(request_text, str) or not request_text.strip():
        raise ValueError("request envelope request_text must be the non-empty exact user text")
    request_sha256 = str(payload.get("request_sha256") or "").lower()
    expected_request_sha256 = hashlib.sha256(request_text.encode("utf-8")).hexdigest()
    if request_sha256 != expected_request_sha256:
        raise ValueError("request envelope request_sha256 does not match request_text bytes")

    raw_spans = payload.get("active_spans")
    if not isinstance(raw_spans, list) or not 1 <= len(raw_spans) <= 16:
        raise ValueError("request envelope active_spans must contain one to sixteen rows")
    spans: List[JsonDict] = []
    seen_ids: Set[str] = set()
    seen_texts: Set[str] = set()
    for index, item in enumerate(raw_spans):
        if not isinstance(item, dict) or set(item) != {"span_id", "start", "end", "text"}:
            raise ValueError(
                f"request envelope active span {index} must contain only span_id, start, end, and text"
            )
        span_id = str(item.get("span_id") or "").strip()
        if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", span_id) is None:
            raise ValueError(f"request envelope active span {index} has an invalid span_id")
        if span_id in seen_ids:
            raise ValueError(f"request envelope repeats active span id {span_id!r}")
        seen_ids.add(span_id)
        start = item.get("start")
        end = item.get("end")
        if (
            isinstance(start, bool)
            or isinstance(end, bool)
            or not isinstance(start, int)
            or not isinstance(end, int)
            or start < 0
            or end <= start
            or end > len(request_text)
        ):
            raise ValueError(f"request envelope active span {index} has invalid offsets")
        text = item.get("text")
        if not isinstance(text, str) or request_text[start:end] != text:
            raise ValueError(
                f"request envelope active span {index} text does not match request_text offsets"
            )
        text_key = text.casefold()
        if text_key in seen_texts:
            raise ValueError("request envelope active span texts must be distinct")
        seen_texts.add(text_key)
        spans.append({"span_id": span_id, "start": start, "end": end, "text": text})
    spans.sort(key=lambda row: (int(row["start"]), int(row["end"]), str(row["span_id"])))
    for previous, current in zip(spans, spans[1:]):
        if int(current["start"]) < int(previous["end"]):
            raise ValueError("request envelope active spans must not overlap")

    normalized: JsonDict = {
        "contract_version": REQUEST_ENVELOPE_CONTRACT_VERSION,
        "provenance": "requesting_user",
        "request_id": request_id,
        "request_text": request_text,
        "request_sha256": request_sha256,
        "active_spans": spans,
    }
    normalized["canonical_sha256"] = canonical_json_sha256(normalized)
    normalized["envelope_id"] = normalized["canonical_sha256"][:16]
    return normalized


def load_request_envelope_arg(raw: Optional[str]) -> Optional[JsonDict]:
    if not raw:
        return None
    payload: Any
    try:
        candidate = Path(raw)
        is_file = candidate.exists()
    except OSError:
        is_file = False
        candidate = Path(".")
    if is_file:
        payload = json.loads(candidate.read_text(encoding="utf-8"))
    else:
        payload = json.loads(raw)
    return normalize_request_envelope(payload)


def request_envelope_active_texts(envelope: JsonDict) -> List[str]:
    return [
        str(item.get("text") or "")
        for item in envelope.get("active_spans") or []
        if isinstance(item, dict) and str(item.get("text") or "")
    ]


def request_scope_contains(envelope: JsonDict, source_text: str) -> bool:
    needle = str(source_text or "").strip().casefold()
    return bool(needle) and any(
        needle in text.casefold() for text in request_envelope_active_texts(envelope)
    )


def normalize_intent_lock(
    payload: Any,
    *,
    envelope: JsonDict,
    baseline_prompt_en: str,
    allowed_dimensions: Set[str] = INTENT_LOCK_DIMENSIONS,
    minimum_open_dimensions: int = 2,
) -> JsonDict:
    if not isinstance(payload, dict):
        raise ValueError("authorial core intent_lock must be one JSON object")
    allowed_fields = {
        "contract_version",
        "priority",
        "semantic_anchors",
        "locked_dimensions",
        "open_dimensions",
    }
    unknown_fields = sorted(set(payload) - allowed_fields)
    if unknown_fields:
        raise ValueError(
            "authorial core intent_lock contains unsupported fields: "
            + ", ".join(unknown_fields)
        )
    property_lock = payload.get("contract_version") == INTENT_LOCK_PROPERTY_CONTRACT_VERSION
    if payload.get("contract_version") not in {INTENT_LOCK_CONTRACT_VERSION, INTENT_LOCK_PROPERTY_CONTRACT_VERSION}:
        raise ValueError(
            f"authorial core intent_lock contract_version must be {INTENT_LOCK_CONTRACT_VERSION!r}"
        )
    if payload.get("priority") != "requesting_user":
        raise ValueError("authorial core intent_lock priority must be 'requesting_user'")
    if minimum_open_dimensions == 0 and not isinstance(
        payload.get("open_dimensions"), list
    ):
        raise ValueError(
            "authorial core intent_lock requires an explicit open_dimensions list; use [] when no variation is permitted"
        )

    locked_dimensions = [
        str(item).strip()
        for item in normalize_list(payload.get("locked_dimensions"))
        if str(item).strip()
    ]
    open_dimensions = [
        str(item).strip()
        for item in normalize_list(payload.get("open_dimensions"))
        if str(item).strip()
    ]
    if not locked_dimensions or len(set(locked_dimensions)) != len(locked_dimensions):
        raise ValueError("authorial core intent_lock requires distinct locked_dimensions")
    if len(open_dimensions) < minimum_open_dimensions:
        raise ValueError(
            "authorial core intent_lock requires at least two distinct open_dimensions"
        )
    if len(set(open_dimensions)) != len(open_dimensions):
        raise ValueError("authorial core intent_lock requires distinct open_dimensions")
    unknown_dimensions = sorted(
        (set(locked_dimensions) | set(open_dimensions)) - allowed_dimensions
    )
    if unknown_dimensions:
        raise ValueError(
            "authorial core intent_lock contains unknown dimensions: "
            + ", ".join(unknown_dimensions)
        )
    missing_required_dimensions = sorted(
        REQUIRED_INTENT_LOCK_DIMENSIONS - set(locked_dimensions)
    )
    if missing_required_dimensions:
        raise ValueError(
            "authorial core intent_lock must lock the governing concept, subject, and event dimensions: "
            + ", ".join(missing_required_dimensions)
        )
    overlap = sorted(set(locked_dimensions) & set(open_dimensions))
    if overlap:
        raise ValueError(
            "authorial core intent_lock dimensions cannot be both locked and open: "
            + ", ".join(overlap)
        )

    raw_anchors = payload.get("semantic_anchors")
    if not isinstance(raw_anchors, list) or not 1 <= len(raw_anchors) <= 16:
        raise ValueError(
            "authorial core intent_lock semantic_anchors must contain one to sixteen rows"
        )
    anchors: List[JsonDict] = []
    seen_ids: Set[str] = set()
    seen_evidence: Set[str] = set()
    seen_properties: Set[tuple] = set()
    for index, item in enumerate(raw_anchors):
        anchor_fields = {
            "anchor_id",
            "source_text",
            "dimension",
            "prompt_evidence",
        }
        if property_lock and isinstance(item, dict) and "property" in item:
            anchor_fields.update({"target", "property"})
        if not isinstance(item, dict) or set(item) != anchor_fields:
            raise ValueError(
                f"authorial core intent anchor {index} must contain only anchor_id, source_text, dimension, and prompt_evidence"
            )
        anchor_id = str(item.get("anchor_id") or "").strip()
        if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", anchor_id) is None:
            raise ValueError(f"authorial core intent anchor {index} has an invalid anchor_id")
        if anchor_id in seen_ids:
            raise ValueError(f"authorial core repeats intent anchor id {anchor_id!r}")
        seen_ids.add(anchor_id)
        source_text = str(item.get("source_text") or "").strip()
        dimension = str(item.get("dimension") or "").strip()
        evidence = clean_spaces(str(item.get("prompt_evidence") or ""))
        if len(authorial_request_content_words(source_text)) < 1:
            raise ValueError(
                f"authorial core intent anchor {index} source_text must contain a substantive requester term"
            )
        if not request_scope_contains(envelope, source_text):
            raise ValueError(
                f"authorial core intent anchor {index} source_text is not grounded in an active requesting-user span"
            )
        is_property = "property" in item
        if is_property:
            if dimension not in open_dimensions or any(
                re.fullmatch(r"[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)*", str(item[key])) is None
                for key in ("target", "property")
            ):
                raise ValueError("a property anchor needs an open dimension and canonical target/property paths")
            property_key = (dimension, item["target"], item["property"])
            if property_key in seen_properties:
                raise ValueError("intent_lock contains duplicate property anchors")
            seen_properties.add(property_key)
        elif dimension not in locked_dimensions:
            raise ValueError(
                f"authorial core intent anchor {index} dimension must be locked"
            )
        if len(authorial_request_content_words(evidence)) < 2:
            raise ValueError(
                f"authorial core intent anchor {index} prompt_evidence needs at least two content words"
            )
        if evidence.casefold() not in baseline_prompt_en.casefold():
            raise ValueError(
                f"authorial core intent anchor {index} prompt_evidence must occur in baseline_prompt_en"
            )
        if evidence.casefold() in seen_evidence and not is_property:
            raise ValueError(
                "authorial core intent anchors require distinct prompt_evidence for each locked dimension"
            )
        seen_evidence.add(evidence.casefold())
        anchors.append(
            {
                "anchor_id": anchor_id,
                "source_text": source_text,
                "dimension": dimension,
                "prompt_evidence": evidence,
                **({"target": item["target"], "property": item["property"]} if is_property else {}),
            }
        )

    anchored_dimensions = {str(item["dimension"]) for item in anchors}
    missing_dimension_anchors = sorted(set(locked_dimensions) - anchored_dimensions)
    if missing_dimension_anchors:
        raise ValueError(
            "authorial core intent_lock requires at least one semantic anchor for every locked dimension: "
            + ", ".join(missing_dimension_anchors)
        )
    uncovered_span_ids = [
        str(span.get("span_id") or "")
        for span in envelope.get("active_spans") or []
        if isinstance(span, dict)
        and not any(
            str(anchor.get("source_text") or "").casefold()
            in str(span.get("text") or "").casefold()
            for anchor in anchors
        )
    ]
    if uncovered_span_ids:
        raise ValueError(
            "authorial core intent_lock requires semantic-anchor coverage for every active requesting-user span: "
            + ", ".join(uncovered_span_ids)
        )

    normalized: JsonDict = {
        "contract_version": payload["contract_version"],
        "priority": "requesting_user",
        "semantic_anchors": anchors,
        "locked_dimensions": locked_dimensions,
        "open_dimensions": open_dimensions,
        "augmentation_policy": "open_dimensions_only_and_subordinate",
        "material_change_policy": "rebuild_core_after_requester_input",
        "candidate_revision_policy": "forbidden",
    }
    normalized["canonical_sha256"] = canonical_json_sha256(normalized)
    normalized["lock_id"] = normalized["canonical_sha256"][:16]
    return normalized


def normalize_semantic_assertions(
    payload: Any,
    *,
    envelope: JsonDict,
    intent_lock: JsonDict,
    baseline_prompt_en: str,
) -> List[JsonDict]:
    """Validate typed, source-grounded meaning without re-parsing raw text."""

    if not isinstance(payload, list) or len(payload) > 16:
        raise ValueError(
            "authorial core v3 semantic_assertions must be a list of at most sixteen rows"
        )
    span_ids = {
        str(item.get("source_span_id", item.get("span_id")) or "")
        for item in envelope.get("active_spans") or []
        if isinstance(item, dict)
    }
    locked_dimensions = set(intent_lock.get("locked_dimensions") or [])
    open_dimensions = set(intent_lock.get("open_dimensions") or [])
    normalized: List[JsonDict] = []
    seen_ids: Set[str] = set()
    for index, item in enumerate(payload):
        if not isinstance(item, dict):
            raise ValueError(f"semantic assertion {index} must be one JSON object")
        allowed_fields = {
            "assertion_id",
            "dimension",
            "polarity",
            "source_span_ids",
            "axes",
            "relations",
            "evidence",
            "affected_dimensions",
        }
        unknown_fields = sorted(set(item) - allowed_fields)
        if unknown_fields:
            raise ValueError(
                f"semantic assertion {index} contains unsupported fields: "
                + ", ".join(unknown_fields)
            )
        assertion_id = str(item.get("assertion_id") or "").strip()
        if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", assertion_id) is None:
            raise ValueError(f"semantic assertion {index} has an invalid assertion_id")
        if assertion_id in seen_ids:
            raise ValueError(f"semantic assertion repeats id {assertion_id!r}")
        seen_ids.add(assertion_id)
        dimension = str(item.get("dimension") or "").strip()
        if dimension not in AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS:
            raise ValueError(
                f"semantic assertion {assertion_id!r} has unknown dimension {dimension!r}"
            )
        polarity = str(item.get("polarity") or "").strip()
        if polarity not in {"required", "advisory", "excluded"}:
            raise ValueError(
                f"semantic assertion {assertion_id!r} polarity must be required, advisory, or excluded"
            )
        source_span_ids = [
            str(value).strip()
            for value in normalize_list(item.get("source_span_ids"))
            if str(value).strip()
        ]
        if (
            not source_span_ids
            or len(source_span_ids) != len(set(source_span_ids))
            or not set(source_span_ids).issubset(span_ids)
        ):
            raise ValueError(
                f"semantic assertion {assertion_id!r} requires distinct active source_span_ids"
            )
        affected_dimensions = [
            str(value).strip()
            for value in normalize_list(item.get("affected_dimensions") or [dimension])
            if str(value).strip()
        ]
        if (
            not affected_dimensions
            or len(affected_dimensions) != len(set(affected_dimensions))
            or not set(affected_dimensions).issubset(
                AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS
            )
        ):
            raise ValueError(
                f"semantic assertion {assertion_id!r} has invalid affected_dimensions"
            )
        if polarity == "required" and not set(affected_dimensions).issubset(
            locked_dimensions
        ):
            raise ValueError(
                f"required semantic assertion {assertion_id!r} must affect only locked dimensions"
            )
        if polarity == "advisory" and not set(affected_dimensions).issubset(
            open_dimensions
        ):
            raise ValueError(
                f"advisory semantic assertion {assertion_id!r} must affect only open dimensions"
            )

        raw_axes = item.get("axes")
        if not isinstance(raw_axes, dict) or not 1 <= len(raw_axes) <= 16:
            raise ValueError(
                f"semantic assertion {assertion_id!r} axes must contain one to sixteen typed values"
            )
        axes: JsonDict = {}
        for raw_key, raw_value in raw_axes.items():
            key = str(raw_key).strip()
            if re.fullmatch(r"[a-z][a-z0-9_]{0,63}", key) is None:
                raise ValueError(
                    f"semantic assertion {assertion_id!r} has invalid axis key {key!r}"
                )
            values = (
                [clean_spaces(str(value)) for value in raw_value]
                if isinstance(raw_value, list)
                else [clean_spaces(str(raw_value))]
            )
            values = [value for value in values if value]
            if not values or len(values) > 8 or len(values) != len(set(values)):
                raise ValueError(
                    f"semantic assertion {assertion_id!r} axis {key!r} has invalid values"
                )
            axes[key] = values if isinstance(raw_value, list) else values[0]

        relations: List[JsonDict] = []
        if "relations" in item:
            raw_relations = item.get("relations")
            if dimension != "character_response":
                raise ValueError(
                    f"semantic assertion {assertion_id!r} relations are supported only for character_response"
                )
            if not isinstance(raw_relations, list) or not 1 <= len(raw_relations) <= 8:
                raise ValueError(
                    f"semantic assertion {assertion_id!r} relations must contain one to eight rows"
                )
            relation_signatures: Set[tuple[Any, ...]] = set()
            for relation_index, raw_relation in enumerate(raw_relations):
                if not isinstance(raw_relation, dict):
                    raise ValueError(
                        f"semantic assertion {assertion_id!r} relation {relation_index} must be one object"
                    )
                operator = str(raw_relation.get("operator") or "").strip()
                expected_fields = CHARACTER_RESPONSE_RELATION_FIELDS.get(operator)
                if expected_fields is None or set(raw_relation) != expected_fields:
                    raise ValueError(
                        f"semantic assertion {assertion_id!r} relation {relation_index} has an invalid operator or shape"
                    )
                if operator == "same_target":
                    members = [
                        str(value).strip()
                        for value in normalize_list(raw_relation.get("members"))
                        if str(value).strip()
                    ]
                    if (
                        not 2 <= len(members) <= 8
                        or len(members) != len(set(members))
                        or "relationship_target" not in members
                        or not set(members).issubset(
                            CHARACTER_RESPONSE_RELATION_MEMBERS
                        )
                        or any(
                            re.fullmatch(r"[a-z][a-z0-9_]{0,63}", value) is None
                            for value in members
                        )
                    ):
                        raise ValueError(
                            f"semantic assertion {assertion_id!r} relation {relation_index} needs distinct semantic members"
                        )
                    normalized_relation = {"operator": operator, "members": members}
                    signature = character_response_relation_signature(
                        normalized_relation
                    )
                    if signature in relation_signatures:
                        raise ValueError(
                            f"semantic assertion {assertion_id!r} relation {relation_index} repeats a semantic relation"
                        )
                    relation_signatures.add(signature)
                    relations.append(normalized_relation)
                    continue
                left_key, right_key = (
                    ("left", "right")
                    if operator == "contrasts"
                    else ("first", "then")
                )
                left = str(raw_relation.get(left_key) or "").strip()
                right = str(raw_relation.get(right_key) or "").strip()
                if (
                    left == right
                    or left not in CHARACTER_RESPONSE_RELATION_MEMBERS
                    or right not in CHARACTER_RESPONSE_RELATION_MEMBERS
                    or re.fullmatch(r"[a-z][a-z0-9_]{0,63}", left) is None
                    or re.fullmatch(r"[a-z][a-z0-9_]{0,63}", right) is None
                ):
                    raise ValueError(
                        f"semantic assertion {assertion_id!r} relation {relation_index} needs two distinct semantic members"
                    )
                normalized_relation = {
                    "operator": operator,
                    left_key: left,
                    right_key: right,
                }
                signature = character_response_relation_signature(
                    normalized_relation
                )
                if signature in relation_signatures:
                    raise ValueError(
                        f"semantic assertion {assertion_id!r} relation {relation_index} repeats a semantic relation"
                    )
                relation_signatures.add(signature)
                relations.append(normalized_relation)

        raw_evidence = item.get("evidence") or {}
        if not isinstance(raw_evidence, dict) or len(raw_evidence) > 16:
            raise ValueError(
                f"semantic assertion {assertion_id!r} evidence must be one bounded object"
            )
        evidence: JsonDict = {}
        for raw_key, raw_value in raw_evidence.items():
            key = str(raw_key).strip()
            if re.fullmatch(r"[a-z][a-z0-9_]{0,63}", key) is None:
                raise ValueError(
                    f"semantic assertion {assertion_id!r} has invalid evidence key {key!r}"
                )
            phrase = clean_spaces(str(raw_value or ""))
            if len(authorial_request_content_words(phrase)) < 2:
                raise ValueError(
                    f"semantic assertion {assertion_id!r} evidence {key!r} needs at least two content words"
                )
            if phrase.casefold() not in baseline_prompt_en.casefold():
                raise ValueError(
                    f"semantic assertion {assertion_id!r} evidence {key!r} must occur in baseline_prompt_en"
                )
            evidence[key] = phrase
        if polarity == "required" and not evidence:
            raise ValueError(
                f"required semantic assertion {assertion_id!r} needs frozen baseline evidence"
            )
        if dimension == "character_response" and polarity == "required":
            missing_axes = sorted(CHARACTER_RESPONSE_REQUIRED_AXES - set(axes))
            if missing_axes:
                raise ValueError(
                    "required character_response assertion is missing generic semantic axes: "
                    + ", ".join(missing_axes)
                )
            primary_actions = normalize_list(axes.get("primary_action"))
            if len(primary_actions) != 1:
                raise ValueError(
                    "required character_response assertion must select exactly one primary_action"
                )
            leak_channels = axes.get("affect_leak_channels")
            if not isinstance(leak_channels, list) or len(leak_channels) != 1:
                raise ValueError(
                    "required character_response assertion must select exactly one primary affect_leak_channel"
                )
            missing_evidence = sorted(
                CHARACTER_RESPONSE_REQUIRED_EVIDENCE - set(evidence)
            )
            if missing_evidence:
                raise ValueError(
                    "required character_response assertion is missing generic causal evidence: "
                    + ", ".join(missing_evidence)
                )
        normalized_assertion = {
            "assertion_id": assertion_id,
            "dimension": dimension,
            "polarity": polarity,
            "source_span_ids": source_span_ids,
            "axes": axes,
            "evidence": evidence,
            "affected_dimensions": affected_dimensions,
        }
        if relations:
            normalized_assertion["relations"] = relations
        normalized.append(normalized_assertion)
    required_character_assertions = [
        item
        for item in normalized
        if item.get("dimension") == "character_response"
        and item.get("polarity") == "required"
    ]
    if len(required_character_assertions) > 1:
        raise ValueError(
            "authorial core v3 allows at most one required character_response assertion"
        )
    return normalized


def normalize_request_lineage(
    payload: Any,
    *,
    current_request_id: str,
    envelope: Optional[JsonDict] = None,
    intent_lock: Optional[JsonDict] = None,
    baseline_prompt_en: str = "",
    semantic_assertions: Optional[Sequence[JsonDict]] = None,
) -> Optional[JsonDict]:
    if payload is None:
        return None
    if not isinstance(payload, dict):
        raise ValueError("authorial core request_lineage must be an object or null")
    base_fields = {
        "parent_request_id",
        "parent_core_sha256",
        "preserved_dimensions",
        "allowed_changes",
    }
    contract_version = str(payload.get("contract_version") or "").strip()
    is_v2 = contract_version == REQUEST_LINEAGE_V2_CONTRACT_VERSION
    if contract_version and not is_v2:
        raise ValueError(
            "request_lineage contract_version must be "
            f"{REQUEST_LINEAGE_V2_CONTRACT_VERSION!r} when supplied"
        )
    allowed_fields = set(base_fields)
    if is_v2:
        allowed_fields.update({"contract_version", "repair_targets"})
    unknown_fields = sorted(set(payload) - allowed_fields)
    if unknown_fields:
        raise ValueError(
            "authorial core request_lineage contains unsupported fields: "
            + ", ".join(unknown_fields)
        )
    parent_request_id = str(payload.get("parent_request_id") or "").strip()
    if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}", parent_request_id) is None:
        raise ValueError("request_lineage parent_request_id is invalid")
    if parent_request_id == current_request_id:
        raise ValueError("request_lineage parent_request_id must differ from the current request")
    parent_core_sha256 = str(payload.get("parent_core_sha256") or "").lower()
    if re.fullmatch(r"[0-9a-f]{64}", parent_core_sha256) is None:
        raise ValueError("request_lineage parent_core_sha256 must be one SHA-256 digest")
    preserved_dimensions = [
        str(value).strip()
        for value in normalize_list(payload.get("preserved_dimensions"))
        if str(value).strip()
    ]
    allowed_changes = [
        str(value).strip()
        for value in normalize_list(payload.get("allowed_changes"))
        if str(value).strip()
    ]
    for label, values in (
        ("preserved_dimensions", preserved_dimensions),
        ("allowed_changes", allowed_changes),
    ):
        if (
            not values
            or len(values) != len(set(values))
            or not set(values).issubset(AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS)
        ):
            raise ValueError(f"request_lineage {label} contains invalid dimensions")
    if set(preserved_dimensions) & set(allowed_changes):
        raise ValueError(
            "request_lineage preserved_dimensions and allowed_changes must be disjoint"
        )
    normalized: JsonDict = {
        "parent_request_id": parent_request_id,
        "parent_core_sha256": parent_core_sha256,
        "preserved_dimensions": preserved_dimensions,
        "allowed_changes": allowed_changes,
    }
    if not is_v2:
        return normalized

    if envelope is None or intent_lock is None:
        raise ValueError(
            "photo-request-lineage/v2 requires the active request envelope and intent lock"
        )
    raw_targets = payload.get("repair_targets")
    if not isinstance(raw_targets, list) or not 1 <= len(raw_targets) <= 8:
        raise ValueError(
            "photo-request-lineage/v2 repair_targets must contain one to eight rows"
        )
    active_span_ids = {
        str(row.get("span_id") or "")
        for row in envelope.get("active_spans") or []
        if isinstance(row, dict)
    }
    locked_dimensions = set(intent_lock.get("locked_dimensions") or [])
    assertions = [
        row
        for row in semantic_assertions or []
        if isinstance(row, dict) and row.get("polarity") == "required"
    ]
    normalized_targets: List[JsonDict] = []
    seen_repair_ids: Set[str] = set()
    for index, raw_target in enumerate(raw_targets):
        if not isinstance(raw_target, dict):
            raise ValueError(f"request_lineage repair target {index} must be one object")
        expected_fields = {
            "repair_id",
            "source_span_ids",
            "importance",
            "relation_origin",
            "actor_phrase",
            "object_phrase",
            "interaction_state",
            "actor_object_contact",
            "protected_dimensions",
            "allowed_repair_axes",
            "interaction_phrase",
            "recognition_phrase",
        }
        if set(raw_target) != expected_fields:
            raise ValueError(
                f"request_lineage repair target {index} must contain exactly: "
                + ", ".join(sorted(expected_fields))
            )
        repair_id = str(raw_target.get("repair_id") or "").strip()
        if (
            re.fullmatch(r"[a-z][a-z0-9_]{0,63}", repair_id) is None
            or repair_id in seen_repair_ids
        ):
            raise ValueError(
                f"request_lineage repair target {index} has an invalid or repeated repair_id"
            )
        seen_repair_ids.add(repair_id)
        source_span_ids = [
            str(value).strip()
            for value in normalize_list(raw_target.get("source_span_ids"))
            if str(value).strip()
        ]
        if (
            not source_span_ids
            or len(source_span_ids) != len(set(source_span_ids))
            or not set(source_span_ids).issubset(active_span_ids)
        ):
            raise ValueError(
                f"request_lineage repair target {repair_id!r} requires distinct active source_span_ids"
            )
        importance = str(raw_target.get("importance") or "").strip()
        if importance not in RENDER_REPAIR_IMPORTANCE_VALUES:
            raise ValueError(
                f"request_lineage repair target {repair_id!r} importance must be primary or supporting"
            )
        relation_origin = str(raw_target.get("relation_origin") or "").strip()
        if relation_origin not in RENDER_REPAIR_RELATION_ORIGINS:
            raise ValueError(
                f"request_lineage repair target {repair_id!r} has an unsupported relation_origin"
            )
        interaction_state = str(raw_target.get("interaction_state") or "").strip()
        if interaction_state not in RENDER_REPAIR_INTERACTION_STATES:
            raise ValueError(
                f"request_lineage repair target {repair_id!r} has an unsupported interaction_state"
            )
        actor_object_contact = str(
            raw_target.get("actor_object_contact") or ""
        ).strip()
        if actor_object_contact not in RENDER_REPAIR_CONTACT_EXPECTATIONS:
            raise ValueError(
                f"request_lineage repair target {repair_id!r} has an unsupported actor_object_contact"
            )
        if (
            interaction_state
            in {"held", "wielded", "used", "handed_off", "carried", "worn"}
            and actor_object_contact == "absent"
        ):
            raise ValueError(
                f"request_lineage repair target {repair_id!r} cannot remove actor-object contact from an interactive state"
            )
        protected_dimensions = [
            str(value).strip()
            for value in normalize_list(raw_target.get("protected_dimensions"))
            if str(value).strip()
        ]
        protected_source_dimensions = (
            set(preserved_dimensions)
            if relation_origin == "parent_preserved"
            else set(allowed_changes)
        )
        if (
            not protected_dimensions
            or len(protected_dimensions) != len(set(protected_dimensions))
            or "action" not in protected_dimensions
            or not set(protected_dimensions).issubset(locked_dimensions)
            or not set(protected_dimensions).issubset(protected_source_dimensions)
        ):
            raise ValueError(
                f"request_lineage repair target {repair_id!r} must protect locked action plus any other dimensions from its declared relation origin"
            )
        allowed_repair_axes = [
            str(value).strip()
            for value in normalize_list(raw_target.get("allowed_repair_axes"))
            if str(value).strip()
        ]
        if (
            not allowed_repair_axes
            or len(allowed_repair_axes) != len(set(allowed_repair_axes))
            or not set(allowed_repair_axes).issubset(RENDER_REPAIR_ALLOWED_AXES)
        ):
            raise ValueError(
                f"request_lineage repair target {repair_id!r} has invalid allowed_repair_axes"
            )
        for repair_axis, dimension in RENDER_REPAIR_DIMENSION_AXES.items():
            if repair_axis in allowed_repair_axes and dimension not in allowed_changes:
                raise ValueError(
                    f"request_lineage repair target {repair_id!r} axis {repair_axis!r} requires {dimension!r} in allowed_changes"
                )

        actor_phrase = clean_spaces(str(raw_target.get("actor_phrase") or ""))
        object_phrase = clean_spaces(str(raw_target.get("object_phrase") or ""))
        interaction_phrase = clean_spaces(
            str(raw_target.get("interaction_phrase") or "")
        )
        recognition_phrase = clean_spaces(
            str(raw_target.get("recognition_phrase") or "")
        )
        for label, phrase, minimum in (
            ("actor_phrase", actor_phrase, 1),
            ("object_phrase", object_phrase, 1),
            ("interaction_phrase", interaction_phrase, 4),
            ("recognition_phrase", recognition_phrase, 4),
        ):
            if len(authorial_request_content_words(phrase)) < minimum:
                raise ValueError(
                    f"request_lineage repair target {repair_id!r} {label} is not substantive"
                )
            if phrase.casefold() not in baseline_prompt_en.casefold():
                raise ValueError(
                    f"request_lineage repair target {repair_id!r} {label} must occur in baseline_prompt_en"
                )
        if interaction_phrase.casefold() == recognition_phrase.casefold():
            raise ValueError(
                f"request_lineage repair target {repair_id!r} needs distinct interaction and recognition evidence"
            )
        if actor_phrase.casefold() not in interaction_phrase.casefold():
            raise ValueError(
                f"request_lineage repair target {repair_id!r} interaction_phrase must contain actor_phrase"
            )
        if object_phrase.casefold() not in interaction_phrase.casefold():
            raise ValueError(
                f"request_lineage repair target {repair_id!r} interaction_phrase must contain object_phrase"
            )
        if object_phrase.casefold() not in recognition_phrase.casefold():
            raise ValueError(
                f"request_lineage repair target {repair_id!r} recognition_phrase must contain object_phrase"
            )
        evidence_pair = {interaction_phrase.casefold(), recognition_phrase.casefold()}
        owns_evidence_pair = any(
            evidence_pair.issubset(
                {
                    str(value).casefold()
                    for value in (assertion.get("evidence") or {}).values()
                    if str(value).strip()
                }
            )
            for assertion in assertions
            if "action" in set(assertion.get("affected_dimensions") or [])
        )
        if not owns_evidence_pair:
            raise ValueError(
                f"request_lineage repair target {repair_id!r} must bind interaction and recognition phrases through one required action semantic assertion"
            )
        normalized_targets.append(
            {
                "repair_id": repair_id,
                "source_span_ids": source_span_ids,
                "importance": importance,
                "relation_origin": relation_origin,
                "actor_phrase": actor_phrase,
                "object_phrase": object_phrase,
                "interaction_state": interaction_state,
                "actor_object_contact": actor_object_contact,
                "protected_dimensions": protected_dimensions,
                "allowed_repair_axes": allowed_repair_axes,
                "interaction_phrase": interaction_phrase,
                "recognition_phrase": recognition_phrase,
            }
        )

    normalized = {
        "contract_version": REQUEST_LINEAGE_V2_CONTRACT_VERSION,
        **normalized,
        "repair_targets": normalized_targets,
    }
    normalized["canonical_sha256"] = canonical_json_sha256(normalized)
    return normalized


def normalize_authorial_core(
    payload: Any,
    *,
    request_envelope: Optional[JsonDict] = None,
    creative_control_snapshot: Optional[JsonDict] = None,
) -> JsonDict:
    """Validate an agent-authored concept core frozen before candidate retrieval.

    This contract is deliberately domain-neutral.  The deterministic generator
    validates and preserves the agent's work; it does not invent a replacement
    concept from taxonomy entries or candidate-pack output.
    """

    if not isinstance(payload, dict):
        raise ValueError("--authorial-core-json must contain one JSON object")
    visual_envelope = request_envelope
    if creative_control_snapshot is not None:
        creative_controls.validate(creative_control_snapshot, payload.get("source_request"))
        if payload.get("creative_controls_sha256") != creative_control_snapshot["canonical_sha256"]:
            raise ValueError("authorial core must bind the supplied creative-control snapshot")
    if request_envelope is not None:
        visual_spans, _ = creative_controls.split_request_spans(
            request_envelope, creative_control_snapshot
        )
        visual_envelope = {**request_envelope, "active_spans": visual_spans}
    core_version = str(payload.get("contract_version") or "")
    if core_version != AUTHORIAL_CORE_V3_CONTRACT_VERSION:
        raise ValueError(
            f"authorial core contract_version must be {AUTHORIAL_CORE_V3_CONTRACT_VERSION}"
        )
    allowed_fields = {
        "contract_version",
        "provenance",
        "source_request",
        "interpreted_intent",
        "subject",
        "setting",
        "event",
        "visual_priorities",
        "baseline_prompt_en",
        "user_definitions",
        "interpretation_provenance",
        "unresolved_ambiguities",
        "user_exclusions",
        "style",
        "variation_key",
    }
    allowed_fields.update({"intent_lock", "runtime_forbidden_labels"})
    allowed_fields.update({"semantic_assertions", "request_lineage", "creative_controls_sha256"})
    unknown_fields = sorted(set(payload) - allowed_fields)
    if unknown_fields:
        raise ValueError(
            "authorial core contains pack-derived or unsupported fields: "
            + ", ".join(unknown_fields)
        )
    for required_field in ("interpretation_provenance", "unresolved_ambiguities"):
        if required_field not in payload:
            raise ValueError(
                f"authorial core requires {required_field}; resolve meaning before freezing the baseline"
            )
    source_request = str(payload.get("source_request") or "")
    normalized: JsonDict = {
        "contract_version": "photo-authorial-core/v3",
        "provenance": str(payload.get("provenance") or ""),
        "source_request": source_request,
        "interpreted_intent": clean_spaces(str(payload.get("interpreted_intent") or "")),
        "subject": clean_spaces(str(payload.get("subject") or "")),
        "setting": clean_spaces(str(payload.get("setting") or "")),
        "event": clean_spaces(str(payload.get("event") or "")),
        "visual_priorities": [
            clean_spaces(str(item))
            for item in normalize_list(payload.get("visual_priorities"))
            if clean_spaces(str(item))
        ],
        "baseline_prompt_en": clean_spaces(str(payload.get("baseline_prompt_en") or "")),
        "user_definitions": [],
        "interpretation_provenance": [],
        "unresolved_ambiguities": [],
        "user_exclusions": [
            clean_spaces(str(item))
            for item in normalize_list(payload.get("user_exclusions"))
            if clean_spaces(str(item))
        ],
        "style": None,
        "variation_key": str(payload.get("variation_key") or "").strip(),
    }
    if request_envelope is None:
        raise ValueError("photo-authorial-core/v3 requires --request-envelope-json")
    if source_request != str(request_envelope.get("request_text") or ""):
        raise ValueError(
            "authorial core source_request must exactly match request envelope request_text bytes"
        )
    normalized["request_binding"] = {
        "contract_version": REQUEST_BINDING_CONTRACT_VERSION,
        "request_id": str(request_envelope.get("request_id") or ""),
        "request_sha256": str(request_envelope.get("request_sha256") or ""),
        "request_envelope_sha256": str(request_envelope.get("canonical_sha256") or ""),
        "active_spans": copy.deepcopy(request_envelope.get("active_spans") or []),
    }
    runtime_forbidden_labels = [
        str(item).strip()
        for item in normalize_list(payload.get("runtime_forbidden_labels"))
        if str(item).strip()
    ]
    if len(runtime_forbidden_labels) > 12 or len(
        {item.casefold() for item in runtime_forbidden_labels}
    ) != len(runtime_forbidden_labels):
        raise ValueError(
            "authorial core runtime_forbidden_labels must contain at most twelve distinct phrases"
        )
    for label in runtime_forbidden_labels:
        if not request_scope_contains(request_envelope, label):
            raise ValueError(
                "authorial core runtime_forbidden_labels must be grounded in an active requesting-user span"
            )
    normalized["runtime_forbidden_labels"] = runtime_forbidden_labels
    if normalized["provenance"] != "agent_prepack":
        raise ValueError("authorial core provenance must be 'agent_prepack'")
    if "creative_controls_sha256" in payload:
        if re.fullmatch("[0-9a-f]{64}", str(payload["creative_controls_sha256"])) is None:
            raise ValueError("creative_controls_sha256 must bind the resolved pre-core snapshot")
        normalized["creative_controls_sha256"] = payload["creative_controls_sha256"]
    if not normalized["source_request"]:
        raise ValueError("authorial core source_request must be non-empty")
    minimum_words = {"interpreted_intent": 4, "subject": 2, "setting": 3, "event": 3}
    for field, minimum in minimum_words.items():
        if len(authorial_request_content_words(normalized[field])) < minimum:
            raise ValueError(
                f"authorial core {field} needs at least {minimum} concrete content words"
            )
    priorities = normalized["visual_priorities"]
    if not 2 <= len(priorities) <= 6:
        raise ValueError("authorial core visual_priorities must contain two to six phrases")
    if len({item.lower() for item in priorities}) != len(priorities):
        raise ValueError("authorial core visual_priorities must be distinct")
    for phrase in priorities:
        if len(authorial_request_content_words(phrase)) < 2:
            raise ValueError(
                "each authorial core visual priority needs at least two concrete content words"
            )
    baseline_words = re.findall(
        "[A-Za-z0-9]+(?:['’\\-][A-Za-z0-9]+)*", normalized["baseline_prompt_en"]
    )
    if not AUTHORIAL_PROMPT_MIN_WORDS <= len(baseline_words) <= AUTHORIAL_PROMPT_ABSOLUTE_MAX_WORDS:
        raise ValueError(
            "authorial core baseline_prompt_en must contain 48 to 640 English words; 360 is the recommended maximum"
        )
    blanket_negative_directives = find_blanket_negative_directives(normalized["baseline_prompt_en"])
    if blanket_negative_directives:
        raise ValueError(
            "authorial core baseline_prompt_en contains blanket negative directives; keep semantic exclusions in request-grounded user_exclusions, keep platform policy outside prompt prose, and express local boundaries as positive geometry or visible state: "
            + " | ".join(blanket_negative_directives)
        )
    assert request_envelope is not None
    normalized["intent_lock"] = normalize_intent_lock(
        payload.get("intent_lock"),
        envelope=visual_envelope,
        baseline_prompt_en=normalized["baseline_prompt_en"],
        allowed_dimensions=AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS,
        minimum_open_dimensions=0,
    )
    leaked_runtime_labels = [
        label
        for label in normalized.get("runtime_forbidden_labels") or []
        if str(label).casefold() in normalized["baseline_prompt_en"].casefold()
    ]
    if leaked_runtime_labels:
        raise ValueError(
            "authorial core baseline_prompt_en contains runtime-only labels: "
            + ", ".join(leaked_runtime_labels)
        )
    if "semantic_assertions" not in payload:
        raise ValueError("photo-authorial-core/v3 requires an explicit semantic_assertions list")
    normalized["semantic_assertions"] = normalize_semantic_assertions(
        payload.get("semantic_assertions"),
        envelope=visual_envelope,
        intent_lock=normalized["intent_lock"],
        baseline_prompt_en=normalized["baseline_prompt_en"],
    )
    authored_subject_category(normalized["semantic_assertions"],
        (creative_control_snapshot or {}).get("context"))
    normalized["request_lineage"] = normalize_request_lineage(
        payload.get("request_lineage"),
        current_request_id=str(normalized.get("request_binding", {}).get("request_id") or ""),
        envelope=request_envelope,
        intent_lock=normalized["intent_lock"],
        baseline_prompt_en=normalized["baseline_prompt_en"],
        semantic_assertions=normalized["semantic_assertions"],
    )
    raw_definitions = payload.get("user_definitions", [])
    if raw_definitions is None:
        raw_definitions = []
    if not isinstance(raw_definitions, list) or len(raw_definitions) > 8:
        raise ValueError("authorial core user_definitions must be a list of at most eight items")
    seen_terms: Set[str] = set()
    source_request_lower = normalized["source_request"].lower()
    for index, item in enumerate(raw_definitions):
        if not isinstance(item, dict):
            raise ValueError(f"authorial core user definition {index} must be an object")
        allowed_definition_fields = {
            "term",
            "source_text",
            "interpreted_meaning",
            "prompt_evidence",
        }
        item_unknown = sorted(set(item) - allowed_definition_fields)
        if item_unknown:
            raise ValueError(
                f"authorial core user definition {index} contains unsupported fields: "
                + ", ".join(item_unknown)
            )
        term = clean_spaces(str(item.get("term") or ""))
        source_text = clean_spaces(str(item.get("source_text") or ""))
        meaning = clean_spaces(str(item.get("interpreted_meaning") or ""))
        prompt_evidence = clean_spaces(str(item.get("prompt_evidence") or ""))
        if not term or not source_text:
            raise ValueError(
                f"authorial core user definition {index} requires term and source_text"
            )
        if term.lower() in seen_terms:
            raise ValueError(f"authorial core repeats user definition term {term!r}")
        seen_terms.add(term.lower())
        if source_text.lower() not in source_request_lower:
            raise ValueError(
                f"authorial core user definition {index} source_text is not grounded in source_request"
            )
        if request_envelope is not None and source_text.casefold() not in {
            text.casefold() for text in request_envelope_active_texts(visual_envelope)
        }:
            raise ValueError(
                f"authorial core user definition {index} source_text must equal one complete active requesting-user span"
            )
        if source_text.casefold() == term.casefold():
            raise ValueError(
                f"authorial core user definition {index} cannot infer a requesting-user definition from a bare term; use interpretation_provenance instead"
            )
        if len(authorial_request_content_words(meaning)) < 4:
            raise ValueError(
                f"authorial core user definition {index} interpreted_meaning needs at least four content words"
            )
        if len(authorial_request_content_words(prompt_evidence)) < 4:
            raise ValueError(
                f"authorial core user definition {index} prompt_evidence needs at least four content words"
            )
        if prompt_evidence.lower() not in normalized["baseline_prompt_en"].lower():
            raise ValueError(
                f"authorial core user definition {index} prompt_evidence must occur in baseline_prompt_en"
            )
        normalized["user_definitions"].append(
            {
                "term": term,
                "source_text": source_text,
                "interpreted_meaning": meaning,
                "prompt_evidence": prompt_evidence,
            }
        )
    raw_interpretations = payload.get("interpretation_provenance")
    if not isinstance(raw_interpretations, list) or len(raw_interpretations) > 8:
        raise ValueError(
            "authorial core interpretation_provenance must be a list of at most eight items"
        )
    allowed_interpretation_bases = {
        "agent_general_knowledge",
        "request_context",
        "public_web_research",
    }
    seen_interpretation_terms: Set[str] = set()
    for index, item in enumerate(raw_interpretations):
        if not isinstance(item, dict):
            raise ValueError(f"authorial core interpretation provenance {index} must be an object")
        allowed_interpretation_fields = {"term", "source_text", "basis", "resolution", "sources"}
        item_unknown = sorted(set(item) - allowed_interpretation_fields)
        if item_unknown:
            raise ValueError(
                f"authorial core interpretation provenance {index} contains unsupported fields: "
                + ", ".join(item_unknown)
            )
        term = clean_spaces(str(item.get("term") or ""))
        source_text = clean_spaces(str(item.get("source_text") or ""))
        basis = str(item.get("basis") or "").strip()
        resolution = clean_spaces(str(item.get("resolution") or ""))
        raw_sources = item.get("sources", [])
        if not term or not source_text:
            raise ValueError(
                f"authorial core interpretation provenance {index} requires term and source_text"
            )
        if term.lower() in seen_interpretation_terms:
            raise ValueError(f"authorial core repeats interpreted term {term!r}")
        if term.lower() in seen_terms:
            raise ValueError(
                f"authorial core term {term!r} cannot be both a requesting-user definition and an agent interpretation"
            )
        seen_interpretation_terms.add(term.lower())
        if source_text.lower() not in source_request_lower:
            raise ValueError(
                f"authorial core interpretation provenance {index} source_text is not grounded in source_request"
            )
        if request_envelope is not None and (
            not request_scope_contains(visual_envelope, source_text)
        ):
            raise ValueError(
                f"authorial core interpretation provenance {index} source_text is not grounded in an active requesting-user span"
            )
        if basis not in allowed_interpretation_bases:
            raise ValueError(
                f"authorial core interpretation provenance {index} basis must be one of {sorted(allowed_interpretation_bases)}"
            )
        if len(authorial_request_content_words(resolution)) < 4:
            raise ValueError(
                f"authorial core interpretation provenance {index} resolution needs at least four content words"
            )
        if not isinstance(raw_sources, list) or len(raw_sources) > 4:
            raise ValueError(
                f"authorial core interpretation provenance {index} sources must be a list of at most four URLs"
            )
        sources = [clean_spaces(str(value)) for value in raw_sources]
        if any((not value for value in sources)) or len(set(sources)) != len(sources):
            raise ValueError(
                f"authorial core interpretation provenance {index} sources must be non-empty and distinct"
            )
        if basis == "public_web_research":
            if not sources or any(
                (
                    re.fullmatch("https?://[^\\s]+", value, flags=re.IGNORECASE) is None
                    for value in sources
                )
            ):
                raise ValueError(
                    f"authorial core interpretation provenance {index} public web research requires at least one HTTP(S) source"
                )
        elif sources:
            raise ValueError(
                f"authorial core interpretation provenance {index} sources are allowed only for public_web_research"
            )
        normalized["interpretation_provenance"].append(
            {
                "term": term,
                "source_text": source_text,
                "basis": basis,
                "resolution": resolution,
                "sources": sources,
            }
        )
    assert request_envelope is not None
    semantic_source_texts = [
        str(item.get("source_text") or "")
        for item in [*normalized["user_definitions"], *normalized["interpretation_provenance"]]
        if isinstance(item, dict) and str(item.get("source_text") or "")
    ]
    uncovered_interpretation_spans = [
        str(span.get("span_id") or "")
        for span in visual_envelope.get("active_spans") or []
        if isinstance(span, dict)
        and (
            not any(
                (
                    source.casefold() in str(span.get("text") or "").casefold()
                    for source in semantic_source_texts
                )
            )
        )
    ]
    if uncovered_interpretation_spans:
        raise ValueError(
            "photo-authorial-core/v3 requires requesting-user definition or interpretation provenance coverage for every active span: "
            + ", ".join(uncovered_interpretation_spans)
        )
    raw_unresolved = payload.get("unresolved_ambiguities")
    if not isinstance(raw_unresolved, list):
        raise ValueError("authorial core unresolved_ambiguities must be a list")
    unresolved = [clean_spaces(str(item)) for item in raw_unresolved if clean_spaces(str(item))]
    if unresolved:
        raise ValueError(
            "authorial core cannot be frozen with unresolved ambiguities; ask the requester or research the public meaning first: "
            + "; ".join(unresolved)
        )
    exclusions = normalized["user_exclusions"]
    if len(exclusions) > 12:
        raise ValueError("authorial core user_exclusions must contain at most twelve phrases")
    if len({item.lower() for item in exclusions}) != len(exclusions):
        raise ValueError("authorial core user_exclusions must be distinct")
    assert request_envelope is not None
    ungrounded_exclusions = [
        item for item in exclusions if not request_scope_contains(request_envelope, item)
    ]
    if ungrounded_exclusions:
        raise ValueError(
            "photo-authorial-core/v3 user_exclusions must be grounded in active requesting-user spans: "
            + ", ".join(ungrounded_exclusions)
        )
    runtime_label_keys = {
        str(item).casefold() for item in normalized.get("runtime_forbidden_labels") or []
    }
    overlap = [item for item in exclusions if item.casefold() in runtime_label_keys]
    if overlap:
        raise ValueError(
            "a runtime-only label cannot also be a semantic user exclusion: " + ", ".join(overlap)
        )
    leaked_exclusions = [
        item for item in exclusions if item.lower() in normalized["baseline_prompt_en"].lower()
    ]
    if leaked_exclusions:
        raise ValueError(
            "authorial core baseline_prompt_en contains excluded phrases: "
            + ", ".join(leaked_exclusions)
        )
    raw_style = payload.get("style")
    if raw_style is not None:
        if not isinstance(raw_style, dict):
            raise ValueError("authorial core style must be an object or null")
        unknown_style_fields = sorted(set(raw_style) - {"domain", "family", "evidence"})
        if unknown_style_fields:
            raise ValueError(
                "authorial core style contains unsupported fields: "
                + ", ".join(unknown_style_fields)
            )
        domain = clean_spaces(str(raw_style.get("domain") or ""))
        family = clean_spaces(str(raw_style.get("family") or ""))
        evidence = [
            clean_spaces(str(item))
            for item in normalize_list(raw_style.get("evidence"))
            if clean_spaces(str(item))
        ]
        if not domain or not family or len(evidence) < 2:
            raise ValueError(
                "authorial core style requires domain, family, and at least two evidence phrases"
            )
        if len({item.lower() for item in evidence}) != len(evidence):
            raise ValueError("authorial core style evidence phrases must be distinct")
        normalized["style"] = {"domain": domain, "family": family, "evidence": evidence}
    canonical_bytes = json.dumps(
        normalized, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    normalized["canonical_sha256"] = hashlib.sha256(canonical_bytes).hexdigest()
    normalized["core_id"] = normalized["canonical_sha256"][:16]
    return normalized


def load_authorial_core_arg(
    raw: Optional[str],
    *,
    request_envelope: Optional[JsonDict] = None,
    creative_control_snapshot: Optional[JsonDict] = None,
) -> Optional[JsonDict]:
    if not raw:
        return None
    payload: Any
    try:
        candidate = Path(raw)
        is_file = candidate.exists()
    except OSError:
        is_file = False
        candidate = Path(".")
    if is_file:
        payload = json.loads(candidate.read_text(encoding="utf-8"))
    else:
        payload = json.loads(raw)
    return normalize_authorial_core(payload, request_envelope=request_envelope,
                                   creative_control_snapshot=creative_control_snapshot)


def authorial_core_retrieval_text(
    core: JsonDict,
    fallback_intent: Optional[str] = None,
) -> tuple[str, JsonDict]:
    """Compose positive retrieval material without promoting exclusions."""

    fields: List[tuple[str, str]] = []
    exclusions = [
        clean_spaces(str(item))
        for item in core.get("user_exclusions") or []
        if clean_spaces(str(item))
    ]
    redacted_source_fields: Set[str] = set()

    def without_exclusions(field: str, value: str) -> str:
        sanitized = value
        for exclusion in exclusions:
            if exclusion.isascii() and re.search(r"[A-Za-z0-9]", exclusion):
                pattern = (
                    r"(?<![A-Za-z0-9])"
                    + re.escape(exclusion)
                    + r"(?![A-Za-z0-9])"
                )
                updated = re.sub(pattern, " ", sanitized, flags=re.IGNORECASE)
            else:
                updated = re.sub(
                    re.escape(exclusion),
                    " ",
                    sanitized,
                    flags=re.IGNORECASE,
                )
            if updated != sanitized:
                redacted_source_fields.add(field)
            sanitized = updated
        return clean_spaces(
            re.sub(r"(?:\s*[,;:/|]\s*){2,}", " ", sanitized).strip(" ,;:/|")
        )

    def add(field: str, value: Any) -> None:
        text = without_exclusions(field, clean_spaces(str(value or "")))
        if text:
            fields.append((field, text))

    request_binding = (
        core.get("request_binding")
        if isinstance(core.get("request_binding"), dict)
        else {}
    )
    active_spans = [
        item
        for item in request_binding.get("active_spans") or []
        if isinstance(item, dict) and str(item.get("text") or "")
    ]
    if core.get("contract_version") in AUTHORIAL_CORE_MODERN_CONTRACT_VERSIONS:
        for item in active_spans:
            add("source_request_scope", creative_controls.strip_assignments(str(item.get("text") or "")))
    else:
        add("source_request", core.get("source_request"))
    add("interpreted_intent", core.get("interpreted_intent"))
    add("subject", core.get("subject"))
    add("setting", core.get("setting"))
    add("event", core.get("event"))
    for value in core.get("visual_priorities") or []:
        add("visual_priority", value)
    add("baseline_prompt_en", core.get("baseline_prompt_en"))
    for definition in core.get("user_definitions") or []:
        if isinstance(definition, dict):
            add("user_definition_meaning", definition.get("interpreted_meaning"))
            add("user_definition_prompt_evidence", definition.get("prompt_evidence"))
    for interpretation in core.get("interpretation_provenance") or []:
        if isinstance(interpretation, dict):
            add("interpretation_resolution", interpretation.get("resolution"))
    style = core.get("style") if isinstance(core.get("style"), dict) else {}
    add("style_domain", style.get("domain"))
    add("style_family", style.get("family"))
    for value in style.get("evidence") or []:
        add("style_evidence", value)
    if not fields and fallback_intent:
        add("fallback_intent", fallback_intent)

    deduped: List[tuple[str, str]] = []
    seen: Set[str] = set()
    for field, value in fields:
        key = value.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append((field, value))
    query = " | ".join(value for _, value in deduped)
    query_sha256 = hashlib.sha256(query.encode("utf-8")).hexdigest()
    provenance: JsonDict = {
        "contract_version": (
            "photo-retrieval-query-provenance/v2"
            if core.get("contract_version") in AUTHORIAL_CORE_MODERN_CONTRACT_VERSIONS
            else "photo-retrieval-query-provenance/v1"
        ),
        "source_authorial_core_sha256": str(core.get("canonical_sha256") or ""),
        "source_request_sha256": hashlib.sha256(
            str(core.get("source_request") or "").encode("utf-8")
        ).hexdigest(),
        "source_fields": [field for field, _ in deduped],
        "query_sha256": query_sha256,
        "redacted_source_fields": sorted(redacted_source_fields),
        "excluded_term_count": len(exclusions),
        "exclusions_used_as_positive_query": False,
    }
    if core.get("contract_version") in AUTHORIAL_CORE_MODERN_CONTRACT_VERSIONS:
        intent_lock = (
            core.get("intent_lock")
            if isinstance(core.get("intent_lock"), dict)
            else {}
        )
        provenance.update(
            {
                "request_envelope_sha256": str(
                    request_binding.get("request_envelope_sha256") or ""
                ),
                "active_scope_sha256": canonical_json_sha256(active_spans),
                "source_intent_lock_sha256": str(
                    intent_lock.get("canonical_sha256") or ""
                ),
                "runtime_forbidden_label_count": len(
                    core.get("runtime_forbidden_labels") or []
                ),
            }
        )
    return query, provenance


def authorial_core_bm25f_query_fields(core: JsonDict) -> JsonDict:
    """Project a frozen core into fielded retrieval input without classifying it.

    These fields are authored before retrieval.  BM25F may rank optional
    material from them, but it is never allowed to create a semantic assertion
    or promote one of its own hits into a hard requirement.
    """

    request_binding = (
        core.get("request_binding")
        if isinstance(core.get("request_binding"), dict)
        else {}
    )
    active_request = [
        clean_spaces(str(item.get("text") or ""))
        for item in request_binding.get("active_spans") or []
        if isinstance(item, dict) and clean_spaces(str(item.get("text") or ""))
    ]
    if not active_request and clean_spaces(str(core.get("source_request") or "")):
        active_request = [clean_spaces(str(core.get("source_request") or ""))]
    return {
        "active_request": active_request,
        "interpreted_intent": [
            clean_spaces(str(core.get("interpreted_intent") or ""))
        ],
        "event": [clean_spaces(str(core.get("event") or ""))],
        "subject": [clean_spaces(str(core.get("subject") or ""))],
        "visual_priorities": [
            clean_spaces(str(value))
            for value in core.get("visual_priorities") or []
            if clean_spaces(str(value))
        ],
        "baseline_prompt": [
            clean_spaces(str(core.get("baseline_prompt_en") or ""))
        ],
    }


def resolve_character_response_intent(core: Any) -> JsonDict:
    """Read the v3 typed assertion; never infer behavior from request text."""

    if (
        not isinstance(core, dict)
        or core.get("contract_version") != AUTHORIAL_CORE_V3_CONTRACT_VERSION
    ):
        return {
            "contract_version": CHARACTER_RESPONSE_CONTRACT_VERSION,
            "enabled": False,
            "reason": "no_typed_v3_core",
        }
    assertions = [
        item
        for item in core.get("semantic_assertions") or []
        if isinstance(item, dict)
        and item.get("dimension") == "character_response"
    ]
    required = [item for item in assertions if item.get("polarity") == "required"]
    if not required:
        return {
            "contract_version": CHARACTER_RESPONSE_CONTRACT_VERSION,
            "enabled": False,
            "reason": (
                "explicitly_excluded"
                if any(item.get("polarity") == "excluded" for item in assertions)
                else "no_required_typed_assertion"
            ),
            "source_authorial_core_sha256": str(core.get("canonical_sha256") or ""),
        }
    if len(required) != 1:
        raise ValueError(
            "typed character response resolution requires exactly one required assertion"
        )
    assertion = required[0]
    axes = copy.deepcopy(assertion.get("axes") or {})
    evidence = copy.deepcopy(assertion.get("evidence") or {})
    leak_channels = normalize_list(axes.get("affect_leak_channels"))
    resolution: JsonDict = {
        "contract_version": CHARACTER_RESPONSE_CONTRACT_VERSION,
        "enabled": True,
        "source": "authorial_core_semantic_assertion",
        "source_authorial_core_sha256": str(core.get("canonical_sha256") or ""),
        "source_intent_lock_sha256": str(
            ((core.get("intent_lock") or {}).get("canonical_sha256") or "")
        ),
        "source_assertion_id": str(assertion.get("assertion_id") or ""),
        "source_span_ids": copy.deepcopy(assertion.get("source_span_ids") or []),
        "semantic_axes": axes,
        "primary_affect_leak_channel": str(leak_channels[0] if leak_channels else ""),
        "frozen_evidence": evidence,
    }
    if assertion.get("relations"):
        resolution["semantic_relations"] = copy.deepcopy(assertion["relations"])
    resolution["canonical_sha256"] = canonical_json_sha256(resolution)
    return resolution


def semantic_character_response_concept_document_ids(data: JsonDict) -> Set[str]:
    return {
        key
        for key, kind, _entry, _slot in iter_semantic_entries(data)
        if kind == "character_response_concept"
    }


def semantic_character_response_confounder_document_ids(
    data: JsonDict,
    *,
    profile_id: Optional[str] = None,
) -> Set[str]:
    """Return data-authored contrast documents for one or all concept profiles."""

    expected_profile_id = str(profile_id or "")
    return {
        key
        for key, kind, entry, _slot in iter_semantic_entries(data)
        if kind == "character_response_confounder"
        and (
            not expected_profile_id
            or str(entry.get("concept_profile_id") or "") == expected_profile_id
        )
    }


def rank_character_response_concept_candidates(
    data: JsonDict,
    bm25f_payload: JsonDict,
    query_fields: JsonDict,
    *,
    limit: int = 3,
) -> List[JsonDict]:
    """Rank concept meanings contrastively against their authored confounders.

    Scores and matched terms remain private retrieval evidence. A concept is
    eligible only when its BM25F document outranks every matching confounder
    declared by that same profile. This supplies a data-driven negative class
    without concept-specific regular expressions or a second meaning store.
    """

    concept_ids = semantic_character_response_concept_document_ids(data)
    confounder_ids = semantic_character_response_confounder_document_ids(data)
    allowed_ids = concept_ids | confounder_ids
    if not concept_ids or not allowed_ids or int(limit) <= 0:
        return []
    ranked = rank_bm25f(
        bm25f_payload,
        query_fields,
        allowed_ids=allowed_ids,
        limit=len(allowed_ids),
    )
    entries_by_key = {
        key: (kind, entry)
        for key, kind, entry, _slot in iter_semantic_entries(data)
    }
    rows_by_id = {
        str(row.get("document_id") or ""): row
        for row in ranked
        if str(row.get("document_id") or "")
    }
    accepted: List[JsonDict] = []
    for row in ranked:
        document_id = str(row.get("document_id") or "")
        source = entries_by_key.get(document_id)
        if source is None or source[0] != "character_response_concept":
            continue
        profile_id = str(source[1].get("id") or "")
        matching_confounders = [
            rows_by_id[confounder_id]
            for confounder_id in semantic_character_response_confounder_document_ids(
                data,
                profile_id=profile_id,
            )
            if confounder_id in rows_by_id
        ]
        concept_score = float(row.get("score", 0.0) or 0.0)
        best_confounder_score = max(
            (float(candidate.get("score", 0.0) or 0.0) for candidate in matching_confounders),
            default=0.0,
        )
        if concept_score > best_confounder_score:
            accepted.append(row)
        if len(accepted) >= int(limit):
            break
    return accepted


def semantic_character_response_document_ids(data: JsonDict) -> Set[str]:
    """Select generic behavior support by typed kind or authored membership."""

    allowed: Set[str] = set()
    for key, kind, entry, _slot in iter_semantic_entries(data):
        if kind == "character_mechanism_node":
            allowed.add(key)
            continue
        tags = {str(value) for value in normalize_list(entry.get("tags"))}
        if tags & {"character_scene_grammar", "character_scene_grammar"}:
            allowed.add(key)
    return allowed


def character_profile_requester_definition_override(
    core: JsonDict,
    profile: JsonDict,
) -> bool:
    aliases = [
        clean_spaces(str(value))
        for value in normalize_list(profile.get("aliases"))
        if clean_spaces(str(value))
    ]
    if not aliases:
        return False
    for definition in core.get("user_definitions") or []:
        if not isinstance(definition, dict):
            continue
        text = " ".join(
            clean_spaces(str(definition.get(key) or ""))
            for key in (
                "term",
                "source_text",
                "interpreted_meaning",
                "definition",
                "resolution",
            )
        )
        if any(
            semantic_text_contains_authored_term(text, alias)
            for alias in aliases
        ):
            return True
    return False


def evaluate_character_response_profile(
    core: JsonDict,
    data: JsonDict,
    profile: JsonDict,
) -> JsonDict:
    """Advisory data-driven conformance; never revises the frozen assertion."""

    resolution = resolve_character_response_intent(core)
    if resolution.get("enabled") is not True:
        return {
            "status": "not_applicable",
            "reason": "no_required_character_response_assertion",
            "hard_eligible": False,
        }
    if character_profile_requester_definition_override(core, profile):
        return {
            "status": "superseded_by_requester_definition",
            "reason": "requester_definition_precedence",
            "hard_eligible": False,
        }
    axes = resolution.get("semantic_axes") or {}
    missing_axes: List[str] = []
    conflicting_axes: List[str] = []
    matched_classes: JsonDict = {}
    for axis, constraint in (profile.get("axis_requirements") or {}).items():
        allowed_classes = set(normalize_list((constraint or {}).get("semantic_classes")))
        values = normalize_list(axes.get(axis))
        actual_classes = {
            class_id
            for value in values
            for class_id in character_axis_value_classes(data, axis, value)
        }
        matched_classes[str(axis)] = sorted(actual_classes)
        if not actual_classes & allowed_classes:
            missing_axes.append(str(axis))
    for axis, constraint in (profile.get("axis_exclusions") or {}).items():
        excluded_classes = set(normalize_list((constraint or {}).get("semantic_classes")))
        values = normalize_list(axes.get(axis))
        actual_classes = {
            class_id
            for value in values
            for class_id in character_axis_value_classes(data, axis, value)
        }
        if actual_classes & excluded_classes:
            conflicting_axes.append(str(axis))
    asserted_relations = [
        relation
        for assertion in core.get("semantic_assertions") or []
        if isinstance(assertion, dict)
        and assertion.get("dimension") == "character_response"
        and assertion.get("polarity") == "required"
        for relation in assertion.get("relations") or []
        if isinstance(relation, dict)
    ]
    asserted_relation_signatures = {
        character_response_relation_signature(relation)
        for relation in asserted_relations
    }
    missing_relations = [
        str(relation.get("operator") or "")
        for relation in profile.get("required_relations") or []
        if isinstance(relation, dict)
        and character_response_relation_signature(relation)
        not in asserted_relation_signatures
    ]
    if conflicting_axes:
        status = "conflicting"
        reason = "excluded_semantic_classes_present"
    elif missing_axes or missing_relations:
        status = "incomplete"
        reason = "required_axes_or_relations_missing"
    else:
        status = "consistent"
        reason = "typed_assertion_matches_profile"
    return {
        "status": status,
        "reason": reason,
        "missing_axes": sorted(set(missing_axes)),
        "conflicting_axes": sorted(set(conflicting_axes)),
        "missing_relation_operators": sorted(set(missing_relations)),
        "matched_axis_classes": matched_classes,
        "hard_eligible": False,
        "frozen_core_revision_forbidden": True,
    }


def retrieve_character_response_behavior_candidates(
    data: JsonDict,
    core: JsonDict,
    *,
    semantic_index: Optional[JsonDict],
    limit: int = 6,
) -> JsonDict:
    """Retrieve bounded advisory behavior nodes after the core is frozen."""

    if not isinstance(semantic_index, dict) or not isinstance(
        semantic_index.get("bm25f"), dict
    ):
        return {
            "evaluated": False,
            "reason": "bm25f_index_unavailable",
            "candidates": [],
        }
    concept_ids = semantic_character_response_concept_document_ids(data)
    behavior_ids = semantic_character_response_document_ids(data)
    if not concept_ids and not behavior_ids:
        return {
            "evaluated": False,
            "reason": "no_authored_behavior_documents",
            "candidates": [],
        }
    query_fields = authorial_core_bm25f_query_fields(core)
    bm25f_payload = semantic_bm25f_payload_from_index(semantic_index)
    concept_rows = rank_character_response_concept_candidates(
        data,
        bm25f_payload,
        query_fields,
        limit=min(3, max(1, int(limit))),
    )
    entries_by_key = {
        key: (kind, entry, slot)
        for key, kind, entry, slot in iter_semantic_entries(data)
    }
    linked_behavior_ids: Set[str] = set()
    concept_consistency_by_id: Dict[str, JsonDict] = {}
    for row in concept_rows:
        document_id = str(row.get("document_id") or "")
        source = entries_by_key.get(document_id)
        if source is None:
            continue
        _kind, profile, _slot = source
        consistency = evaluate_character_response_profile(core, data, profile)
        concept_consistency_by_id[document_id] = consistency
        if consistency.get("status") in {
            "conflicting",
            "superseded_by_requester_definition",
        }:
            continue
        linked_behavior_ids.update(
            f"character_mechanism_node:{runtime_id}"
            for runtime_id in normalize_list(profile.get("optional_runtime_node_ids"))
        )
    unlinked_behavior_ids = {
        key
        for key in behavior_ids
        if (entries_by_key.get(key) or (None, None, None))[0]
        != "character_mechanism_node"
    }
    ranked_behavior_ids = linked_behavior_ids if concept_rows else unlinked_behavior_ids
    remaining = max(0, int(limit) - len(concept_rows))
    behavior_rows = (
        rank_bm25f(
            bm25f_payload,
            query_fields,
            allowed_ids=ranked_behavior_ids,
            limit=remaining,
        )
        if remaining and ranked_behavior_ids
        else []
    )
    rows = [*concept_rows, *behavior_rows]
    candidates: List[JsonDict] = []
    for row in rows:
        key = str(row.get("document_id") or "")
        source = entries_by_key.get(key)
        if source is None:
            continue
        kind, entry, slot = source
        terms = [
            clean_spaces(str(value))
            for value in (
                *normalize_list(entry.get("aliases")),
                *normalize_list(entry.get("embedding_text")),
                str(entry.get("en") or ""),
                str(entry.get("ko") or ""),
                str(entry.get("ja") or ""),
            )
            if clean_spaces(str(value))
        ]
        candidate: JsonDict = {
            "candidate_id": key,
            "candidate_type": (
                "concept_profile"
                if kind == "character_response_concept"
                else "behavior_support"
            ),
            "kind": kind,
            "slot": slot,
            "concept_terms": list(dict.fromkeys(terms))[:12],
            "applicability": "advisory_only",
            "hard_eligible": False,
        }
        if kind == "character_response_concept":
            consistency = concept_consistency_by_id.get(key) or (
                evaluate_character_response_profile(core, data, entry)
            )
            candidate["semantic_consistency"] = consistency
            if consistency.get("status") in {
                "conflicting",
                "superseded_by_requester_definition",
            }:
                candidate["applicability"] = "diagnostic_only"
        candidates.append(candidate)
    seed = int.from_bytes(
        hashlib.sha256(
            f"character-response-bm25f|{core.get('canonical_sha256') or ''}".encode(
                "utf-8"
            )
        ).digest()[:8],
        "big",
    )
    random.Random(seed).shuffle(candidates)
    return {
        "evaluated": True,
        "method": "bm25f_post_core",
        "query_fields_sha256": canonical_json_sha256(query_fields),
        "candidate_order": "deterministically_shuffled_non_preferential",
        "hardening_policy": "retrieval_hits_never_create_required_evidence",
        "concept_profile_matches": len(concept_rows),
        "concept_profile_support_matches": sum(
            1
            for consistency in concept_consistency_by_id.values()
            if consistency.get("status") not in {
                "conflicting",
                "superseded_by_requester_definition",
            }
        ),
        "candidates": candidates,
    }


def compile_character_response_contract(
    core: Any,
    *,
    data: Optional[JsonDict] = None,
    semantic_index: Optional[JsonDict] = None,
) -> Optional[JsonDict]:
    """Compile a generic visible-response contract from frozen typed evidence."""

    resolution = resolve_character_response_intent(core)
    if resolution.get("enabled") is not True:
        return None
    assert isinstance(core, dict)
    evidence = copy.deepcopy(resolution.get("frozen_evidence") or {})
    semantic_axes = copy.deepcopy(resolution.get("semantic_axes") or {})
    causal_roles = (
        ("actor", "actor_phrase"),
        ("baseline", "baseline_phrase"),
        ("trigger", "trigger_phrase"),
        ("target", "target_phrase"),
        ("primary_action", "primary_action_phrase"),
        ("affect_leak", "affective_leak_phrase"),
        ("visible_response", "visible_response_phrase"),
        ("immediate_consequence", "immediate_consequence_phrase"),
        ("continuity", "continuity_phrase"),
    )
    advisory_retrieval = retrieve_character_response_behavior_candidates(
        data or {},
        core,
        semantic_index=semantic_index,
    )
    contract: JsonDict = {
        "contract_version": CHARACTER_RESPONSE_CONTRACT_VERSION,
        "enabled": True,
        "source": resolution["source"],
        "source_authorial_core_sha256": resolution[
            "source_authorial_core_sha256"
        ],
        "source_intent_lock_sha256": resolution["source_intent_lock_sha256"],
        "source_assertion_id": resolution["source_assertion_id"],
        "source_span_ids": copy.deepcopy(resolution.get("source_span_ids") or []),
        "semantic_axes": semantic_axes,
        "semantic_relations": copy.deepcopy(
            resolution.get("semantic_relations") or []
        ),
        "primary_affect_leak_channel": resolution[
            "primary_affect_leak_channel"
        ],
        "causal_sequence": [
            {
                "role": role,
                "evidence_field": field,
                "phrase": str(evidence.get(field) or ""),
            }
            for role, field in causal_roles
        ],
        "frozen_evidence": evidence,
        "behavior_budget": {
            "primary_action_count": 1,
            "primary_affect_leak_channel_count": 1,
            "retrieved_support_is_optional": True,
            "unrequested_relationship_or_emotion_inference_forbidden": True,
        },
        "prompt_binding": {
            "composed_field": "character_response",
            "required_composed_fields": [
                "source_contract_sha256",
                "evidence",
                "selected_advisory_candidate_ids",
            ],
            "required_evidence_fields": [field for _role, field in causal_roles],
            "all_required_phrases_must_be_literal_in_final_prompt": True,
            "new_hard_evidence_from_retrieval_forbidden": True,
            "semantic_values_must_not_be_replaced_by_taxonomy_labels": True,
        },
        "render_gates": [
            {
                "id": f"character_response_{role}",
                "evidence_field": field,
                "criterion": "visible_and_literal",
            }
            for role, field in causal_roles
        ],
        "advisory_retrieval": advisory_retrieval,
    }
    contract["canonical_sha256"] = canonical_json_sha256(contract)
    return contract


def compile_semantic_assertion_obligations(core: Any) -> Optional[JsonDict]:
    """Bind required non-character typed meaning to final prompt evidence.

    Character response keeps its specialized causal contract. Every other
    required v3 semantic assertion is projected through this generic contract
    so a registry or retrieval candidate cannot silently replace the meaning
    that the pre-pack author froze.
    """

    if (
        not isinstance(core, dict)
        or core.get("contract_version") != AUTHORIAL_CORE_V3_CONTRACT_VERSION
    ):
        return None
    assertions = [
        item
        for item in core.get("semantic_assertions") or []
        if isinstance(item, dict)
        and item.get("polarity") == "required"
        and item.get("dimension") != "character_response"
    ]
    if not assertions:
        return None
    obligations: List[JsonDict] = []
    for assertion in assertions:
        evidence = copy.deepcopy(assertion.get("evidence") or {})
        obligations.append(
            {
                "assertion_id": str(assertion.get("assertion_id") or ""),
                "dimension": str(assertion.get("dimension") or ""),
                "affected_dimensions": copy.deepcopy(
                    assertion.get("affected_dimensions") or []
                ),
                "source_span_ids": copy.deepcopy(
                    assertion.get("source_span_ids") or []
                ),
                "semantic_axes": copy.deepcopy(assertion.get("axes") or {}),
                "frozen_evidence": evidence,
                "prompt_binding": {
                    "required_evidence_fields": list(evidence),
                    "all_required_phrases_must_be_literal_in_final_prompt": True,
                    "evidence_must_remain_byte_identical": True,
                    "new_hard_evidence_from_retrieval_forbidden": True,
                },
            }
        )
    contract: JsonDict = {
        "contract_version": SEMANTIC_ASSERTION_OBLIGATIONS_CONTRACT_VERSION,
        "enabled": True,
        "source": "authorial_core_semantic_assertions",
        "source_authorial_core_sha256": str(core.get("canonical_sha256") or ""),
        "source_intent_lock_sha256": str(
            ((core.get("intent_lock") or {}).get("canonical_sha256") or "")
        ),
        "composed_field": "semantic_assertion_evidence",
        "obligations": obligations,
    }
    contract["canonical_sha256"] = canonical_json_sha256(contract)
    return contract


def render_repair_target_gates(target: JsonDict) -> List[JsonDict]:
    """Return the generic coarse pixel gates for one meaningful prop interaction."""

    repair_id = str(target.get("repair_id") or "")
    gates: List[JsonDict] = [
        {
            "id": f"rr_{repair_id}_object_class_legible",
            "review_scale": "both",
            "criterion": (
                "The target object is recognizable as the intended object class at thumbnail "
                "and native scale."
            ),
        },
        {
            "id": f"rr_{repair_id}_gross_structure_coherent",
            "review_scale": "native",
            "criterion": (
                "The target object's major parts form one coherent, non-grotesque structure; "
                "minor ornament differences are non-blocking."
            ),
        },
        {
            "id": f"rr_{repair_id}_intended_interaction_matches",
            "review_scale": "both",
            "criterion": (
                "The actor, object, and intended interaction state match the frozen relation; "
                "removal, relocation, concealment, or transfer is not a repair."
            ),
        },
    ]
    if str(target.get("actor_object_contact") or "") in {
        "required",
        "transitional",
    }:
        gates.append(
            {
                "id": f"rr_{repair_id}_contact_anatomy_coherent",
                "review_scale": "native",
                "criterion": (
                    "The event-critical actor-object contact and principal anatomy are coherent "
                    "without severe fusion or impossible articulation."
                ),
            }
        )
    return gates


def compile_render_repair_contract(core: Any) -> Optional[JsonDict]:
    """Project a lineage-bound fidelity repair into prompt and pixel duties.

    The contract is intentionally object-agnostic.  It preserves the actor-object
    affordance frozen before retrieval and permits only local rendering repair;
    it does not contain named props or domain-specific prompt prose.
    """

    if not isinstance(core, dict):
        return None
    lineage = (
        core.get("request_lineage")
        if isinstance(core.get("request_lineage"), dict)
        else {}
    )
    if lineage.get("contract_version") != REQUEST_LINEAGE_V2_CONTRACT_VERSION:
        return None
    targets: List[JsonDict] = []
    required_hard_gates: List[str] = []
    for target in lineage.get("repair_targets") or []:
        if not isinstance(target, dict):
            continue
        gates = render_repair_target_gates(target)
        gate_ids = [str(gate["id"]) for gate in gates]
        required_hard_gates.extend(gate_ids)
        targets.append(
            {
                "repair_id": str(target.get("repair_id") or ""),
                "source_span_ids": copy.deepcopy(target.get("source_span_ids") or []),
                "importance": str(target.get("importance") or ""),
                "relation_origin": str(target.get("relation_origin") or ""),
                "actor_phrase": str(target.get("actor_phrase") or ""),
                "object_phrase": str(target.get("object_phrase") or ""),
                "interaction_state": str(target.get("interaction_state") or ""),
                "actor_object_contact": str(
                    target.get("actor_object_contact") or ""
                ),
                "protected_dimensions": copy.deepcopy(
                    target.get("protected_dimensions") or []
                ),
                "allowed_repair_axes": copy.deepcopy(
                    target.get("allowed_repair_axes") or []
                ),
                "frozen_evidence": {
                    "interaction_phrase": str(
                        target.get("interaction_phrase") or ""
                    ),
                    "recognition_phrase": str(
                        target.get("recognition_phrase") or ""
                    ),
                },
                "prompt_binding": {
                    "required_evidence_fields": [
                        "interaction_phrase",
                        "recognition_phrase",
                    ],
                    "all_required_phrases_must_be_literal_in_final_prompt": True,
                    "evidence_must_remain_byte_identical": True,
                    "semantic_substitution_forbidden": True,
                },
                "render_gates": gates,
                "required_hard_gates": gate_ids,
            }
        )
    contract: JsonDict = {
        "contract_version": RENDER_REPAIR_CONTRACT_VERSION,
        "enabled": True,
        "source": "authorial_core_request_lineage",
        "source_authorial_core_sha256": str(core.get("canonical_sha256") or ""),
        "source_intent_lock_sha256": str(
            ((core.get("intent_lock") or {}).get("canonical_sha256") or "")
        ),
        "source_request_lineage_sha256": str(
            lineage.get("canonical_sha256") or ""
        ),
        "composed_field": "render_repair_evidence",
        "strict_gate_set": True,
        "major_only": True,
        "targets": targets,
        "required_hard_gates": required_hard_gates,
        "retry_policy": {
            "preserve_interaction_relation": True,
            "repair_smallest_failed_gate_set": True,
            "removal_relocation_concealment_or_transfer_is_not_repair": True,
            "minor_decorative_variation_is_non_blocking": True,
            "maximum_additional_attempts": 1,
        },
    }
    contract["canonical_sha256"] = canonical_json_sha256(contract)
    return contract


def authorial_core_generation_constraints(
    core: JsonDict, *, creative_control_snapshot: Optional[JsonDict] = None,
) -> JsonDict:
    """Translate only explicit structural exclusions into existing guards.

    Exclusions never become positive retrieval text. A supplied pre-core
    snapshot must bind the same request/core and may only strengthen this
    existing guard through its explicit no_people context. Neither nonhuman
    category inference nor candidate metadata supplies that boolean.
    """

    exclusions = [
        clean_spaces(str(item))
        for item in core.get("user_exclusions") or []
        if clean_spaces(str(item))
    ]
    no_people = any(
        intent_explicitly_excludes_people(variant)
        for exclusion in exclusions
        for variant in (
            f"no {exclusion}",
            f"without {exclusion}",
            f"{exclusion} 없이",
            f"{exclusion} 제외",
            f"{exclusion}なし",
        )
    )
    exclusion_no_people = no_people
    bound_no_people = False
    if creative_control_snapshot is not None:
        if core.get("contract_version") != AUTHORIAL_CORE_V3_CONTRACT_VERSION:
            raise ValueError("bound creative context requires a v3 authorial core")
        # Context is an explicit requester interpretation frozen before local
        # retrieval, not a candidate-derived or inferred subject preference.
        creative_controls.validate(creative_control_snapshot, core.get("source_request"))
        if core.get("creative_controls_sha256") != creative_control_snapshot["canonical_sha256"]:
            raise ValueError("authorial core does not bind the supplied pre-core creative controls")
        bound_no_people = (creative_control_snapshot.get("context") or {}).get("no_people") is True
    no_people = exclusion_no_people or bound_no_people
    dimension_scope = authorial_core_intent_dimension_scope(core)
    return {
        "no_people": no_people,
        "source": ("explicit_request_exclusions_and_bound_creative_context" if bound_no_people
                   else "explicit_authorial_core_user_exclusions"),
        **({"no_people_sources": [
                *(["user_exclusions"] if exclusion_no_people else []),
                "bound_creative_controls.context.no_people",
            ], "creative_controls_sha256": creative_control_snapshot["canonical_sha256"]}
           if bound_no_people else {}),
        "excluded_term_count": len(exclusions),
        **(
            {
                "intent_precedence": {
                    "contract_version": DOWNSTREAM_INTENT_PRECEDENCE_CONTRACT_VERSION,
                    "source_intent_lock_sha256": dimension_scope[
                        "source_intent_lock_sha256"
                    ],
                    "locked_dimensions": dimension_scope["locked_dimensions"],
                    "open_dimensions": dimension_scope["open_dimensions"],
                    "default_rule_policy": (
                        "active_only_when_all_affected_dimensions_are_explicitly_open"
                    ),
                }
            }
            if dimension_scope.get("enabled") is True
            else {}
        ),
    }


def visual_profile_context_applicability(
    profile: JsonDict,
    context_text: str,
    *,
    has_authorial_core_context: bool,
    require_positive_context_terms: bool = True,
) -> tuple[bool, str]:
    """Apply shared negatives and lane-appropriate positive sense proof."""

    activation = (
        profile.get("activation")
        if isinstance(profile.get("activation"), dict)
        else {}
    )
    excluded_terms = [
        str(term).strip()
        for term in activation.get("exclude_if_any_terms") or []
        if str(term).strip()
    ]
    if any(intent_alias_matches(context_text, term) for term in excluded_terms):
        return False, "request_exclusion"
    disambiguation = (
        activation.get("context_disambiguation")
        if isinstance(activation.get("context_disambiguation"), dict)
        else {}
    )
    if (
        has_authorial_core_context
        and disambiguation.get("required_with_authorial_core") is True
    ):
        excluded_context = [
            str(term).strip()
            for term in disambiguation.get("exclude_if_any_terms") or []
            if str(term).strip()
        ]
        if any(
            intent_alias_matches(context_text, term) for term in excluded_context
        ):
            return False, "context_disambiguation_exclusion"
        required_context = [
            str(term).strip()
            for term in disambiguation.get("any_terms") or []
            if str(term).strip()
        ]
        if (
            require_positive_context_terms
            and required_context
            and not any(
                intent_alias_matches(context_text, term)
                for term in required_context
            )
        ):
            return False, "context_disambiguation_mismatch"
    return True, "context_applicable"


def visual_profile_user_definition_override_ids(
    registry: JsonDict,
    index: JsonDict,
    user_definitions: Sequence[JsonDict],
) -> Set[str]:
    """Find genuine requester redefinitions, not aligned term explanations."""

    override_ids: Set[str] = set()
    lookup = [row for row in index.get("exact_lookup") or [] if isinstance(row, dict)]
    profiles = {
        str(profile.get("id") or ""): profile
        for profile in registry.get("profiles") or []
        if isinstance(profile, dict) and str(profile.get("id") or "").strip()
    }
    for definition in user_definitions:
        if not isinstance(definition, dict):
            continue
        definition_text = " | ".join(
            clean_spaces(str(definition.get(field) or ""))
            for field in ("term", "source_text")
            if clean_spaces(str(definition.get(field) or ""))
        )
        supplied_meaning = " | ".join(
            clean_spaces(str(definition.get(field) or ""))
            for field in ("interpreted_meaning", "prompt_evidence")
            if clean_spaces(str(definition.get(field) or ""))
        )
        if not supplied_meaning:
            continue
        for row in lookup:
            term = str(row.get("term") or "")
            if term and intent_alias_matches(definition_text, term):
                profile_id = str(row.get("profile_id") or "")
                profile = profiles.get(profile_id)
                if profile is None:
                    continue
                concept_terms = [
                    clean_spaces(str(value))
                    for value in (
                        (profile.get("concept_candidate") or {}).get(
                            "concept_terms"
                        )
                        or []
                    )
                    if clean_spaces(str(value))
                ]
                definition_is_aligned = bool(
                    candidate_pack_visual_component_match(
                        profile,
                        supplied_meaning,
                    )
                    is not None
                    or any(
                        intent_alias_matches(supplied_meaning, term)
                        for term in concept_terms
                    )
                )
                if definition_is_aligned:
                    continue
                override_ids.add(profile_id)
    return {profile_id for profile_id in override_ids if profile_id}


def resolve_visual_profile_hits(
    registry: JsonDict,
    source_rows: Sequence[JsonDict],
    *,
    visual_profile_index: Optional[JsonDict] = None,
    query_text: str = "",
    query_fields: Optional[Mapping[str, Any]] = None,
    query_vector: Optional[Sequence[float]] = None,
    user_definitions: Sequence[JsonDict] = (),
    adult_context: bool = False,
) -> JsonDict:
    """Resolve exact activation and semantic discovery through one typed path.

    Exact terms may preserve the existing request-scoped hard behavior.
    BM25F- and embedding-only hits are structurally incapable of becoming hard
    here. Fielded lexical retrieval uses the structured query supplied by the
    frozen core; exact-only diagnostic calls need no fielded query.
    """

    index = visual_profile_index or build_visual_profile_index_payload(registry)
    lookup = [row for row in index.get("exact_lookup") or [] if isinstance(row, dict)]
    profiles = {
        str(profile.get("id") or ""): profile
        for profile in registry.get("profiles") or []
        if isinstance(profile, dict) and str(profile.get("id") or "").strip()
    }
    trigger_sources = {
        "concept_lock",
        "user_requirement",
        "additional_requirement",
        "intent",
    }
    trigger_rows = [
        row
        for row in source_rows
        if isinstance(row, dict)
        and str(row.get("source") or "") in trigger_sources
        and str(row.get("polarity") or "") != "excluded"
    ]
    requesting_user_text = " ".join(str(row.get("text") or "") for row in trigger_rows)
    context_text = " ".join(
        str(row.get("text") or "")
        for row in source_rows
        if isinstance(row, dict) and str(row.get("polarity") or "") != "excluded"
    )
    has_authorial_core_context = any(
        str(row.get("source") or "").startswith("authorial_core_")
        for row in source_rows
        if isinstance(row, dict)
    )
    user_override_ids = visual_profile_user_definition_override_ids(
        registry,
        index,
        user_definitions,
    )
    exact_sources: Dict[str, List[JsonDict]] = {}
    exact_evidence_ids: Set[str] = set()
    exact_negated_ids: Set[str] = set()
    exact_context_mismatches: Dict[str, str] = {}
    for row in trigger_rows:
        text = str(row.get("text") or "")
        for lookup_row in lookup:
            profile_id = str(lookup_row.get("profile_id") or "")
            term = str(lookup_row.get("term") or "")
            term_is_negated = bool(
                term and intent_term_is_negated(text, term)
            )
            if (
                not profile_id
                or not term
                or (not intent_alias_matches(text, term) and not term_is_negated)
            ):
                continue
            exact_evidence_ids.add(profile_id)
            if term_is_negated:
                exact_negated_ids.add(profile_id)
                continue
            profile = profiles.get(profile_id)
            if profile is None:
                continue
            applicable, applicability_reason = visual_profile_context_applicability(
                profile,
                context_text,
                has_authorial_core_context=has_authorial_core_context,
            )
            if not applicable:
                exact_context_mismatches[profile_id] = applicability_reason
                continue
            source_key = hashlib.sha256(
                f"{row.get('source')}|{clean_spaces(text).lower()}".encode("utf-8")
            ).hexdigest()[:16]
            source_record = {
                "source_intent_id": f"{row.get('source')}:{source_key}",
                "source": str(row.get("source") or ""),
            }
            bucket = exact_sources.setdefault(profile_id, [])
            if source_record not in bucket:
                bucket.append(source_record)

    hits: List[JsonDict] = []
    for profile_id in profiles:
        matched_sources = exact_sources.get(profile_id, [])
        if not matched_sources:
            continue
        profile = profiles[profile_id]
        requires_adult = (
            (profile.get("activation") or {}).get("requires_adult_character") is True
        )
        user_override = profile_id in user_override_ids
        mechanism_supported = hard_activation_is_supported(
            profile,
            requesting_user_text,
            matches=intent_alias_matches,
            is_negated=intent_term_is_negated,
        )
        hard_eligible = bool(
            not user_override
            and (not requires_adult or adult_context)
            and mechanism_supported
        )
        if user_override:
            status = "user_definition_override"
        elif requires_adult and not adult_context:
            status = "requires_existing_adult_context"
        elif not mechanism_supported:
            status = "requires_explicit_mechanism"
        else:
            status = "required"
        hits.append(
            {
                "profile_id": profile_id,
                "match_basis": "exact",
                "applicability_status": status,
                "hard_eligible": hard_eligible,
                "optional_eligible": bool(
                    not mechanism_supported
                    and not user_override
                    and (not requires_adult or adult_context)
                ),
                "source_intent_ids": [
                    str(item.get("source_intent_id") or "")
                    for item in matched_sources
                ],
                "source_records": copy.deepcopy(matched_sources),
            }
        )
    for profile_id in profiles:
        if profile_id not in exact_context_mismatches or profile_id in exact_sources:
            continue
        hits.append(
            {
                "profile_id": profile_id,
                "match_basis": "exact",
                "applicability_status": "context_mismatch",
                "applicability_reason": exact_context_mismatches[profile_id],
                "hard_eligible": False,
                "optional_eligible": False,
                "source_intent_ids": [],
                "source_records": [],
            }
        )

    semantic_candidates: List[JsonDict] = []
    entries = index.get("entries") if isinstance(index.get("entries"), dict) else {}
    retrieval_policy = (
        index.get("retrieval_policy")
        if isinstance(index.get("retrieval_policy"), dict)
        else registry.get("retrieval_policy") or {}
    )
    try:
        minimum_similarity = float(retrieval_policy.get("minimum_similarity", 0.5))
        best_score_margin = float(retrieval_policy.get("best_score_margin", 0.08))
        candidate_limit = max(1, int(retrieval_policy.get("candidate_limit", 2)))
    except (TypeError, ValueError):
        minimum_similarity = 0.5
        best_score_margin = 0.08
        candidate_limit = 2
    blocked_by_exact = exact_evidence_ids | exact_negated_ids | user_override_ids
    # Some profiles encode a multi-part relation whose participants, action,
    # and consequence must not be invented from a nearby portrait embedding.
    # Those profiles may require their existing component semantics as
    # positive context proof while leaving ordinary embedding discovery intact.
    semantically_applicable_ids = {
        profile_id
        for profile_id, profile in profiles.items()
        if visual_profile_context_applicability(
            profile,
            context_text,
            has_authorial_core_context=has_authorial_core_context,
            require_positive_context_terms=False,
        )[0]
        and (
            (profile.get("activation") or {}).get(
                "semantic_discovery_requires_component_evidence"
            )
            is not True
            or candidate_pack_visual_component_match(profile, context_text)
            is not None
        )
    }

    bm25f_rows: List[JsonDict] = []
    bm25f_payload = index.get("bm25f") if isinstance(index.get("bm25f"), dict) else {}
    bm25f_ready = bool(query_fields and bm25f_payload)
    if bm25f_ready:
        bm25f_rows = rank_bm25f(
            bm25f_payload,
            query_fields or {},
            limit=max(candidate_limit, int((bm25f_payload.get("policy") or {}).get("candidate_limit", candidate_limit))),
            allowed_ids=semantically_applicable_ids,
            blocked_ids=blocked_by_exact,
        )

    dimensions = int(index.get("embedding_dimensions", 0) or 0)
    vector_ready = bool(
        query_vector
        and dimensions > 0
        and len(query_vector or []) == dimensions
    )
    if vector_ready:
        reference_scores: List[float] = []
        for profile_id, profile in profiles.items():
            if profile_id not in semantically_applicable_ids:
                continue
            vector = (entries.get(profile_id) or {}).get("vector")
            if not isinstance(vector, list) or len(vector) != dimensions:
                continue
            score = cosine_similarity(query_vector or [], vector)
            reference_scores.append(float(score))
            if profile_id in blocked_by_exact:
                continue
            if score < minimum_similarity:
                continue
            requires_adult = (
                (profile.get("activation") or {}).get("requires_adult_character")
                is True
            )
            semantic_candidates.append(
                {
                    "profile_id": profile_id,
                    "match_basis": "embedding",
                    "applicability_status": (
                        "eligible"
                        if not requires_adult or adult_context
                        else "requires_existing_adult_context"
                    ),
                    "hard_eligible": False,
                    "optional_eligible": bool(
                        not requires_adult or adult_context
                    ),
                    "source_intent_ids": [],
                    "semantic_score": round(float(score), 6),
                }
            )
        semantic_candidates.sort(
            key=lambda item: (
                -float(item.get("semantic_score", 0.0)),
                str(item.get("profile_id") or ""),
            )
        )
        if semantic_candidates:
            best_score = max(reference_scores) if reference_scores else float(
                semantic_candidates[0]["semantic_score"]
            )
            semantic_candidates = [
                item
                for item in semantic_candidates
                if float(item.get("semantic_score", 0.0))
                >= best_score - best_score_margin
            ][: max(candidate_limit, len(bm25f_rows))]

    bm25f_by_id = {
        str(row.get("document_id") or ""): row
        for row in bm25f_rows
        if str(row.get("document_id") or "")
    }
    embedding_by_id = {
        str(row.get("profile_id") or ""): row
        for row in semantic_candidates
        if str(row.get("profile_id") or "")
    }
    if bm25f_by_id or embedding_by_id:
        rrf_k = int((bm25f_payload.get("policy") or {}).get("rrf_k", 60) or 60)
        fused = reciprocal_rank_fusion(
            [list(bm25f_by_id), list(embedding_by_id)],
            k=rrf_k,
            limit=candidate_limit,
        )
        for fused_row in fused:
            profile_id = str(fused_row.get("document_id") or "")
            profile = profiles.get(profile_id)
            if profile is None:
                continue
            requires_adult = (
                (profile.get("activation") or {}).get("requires_adult_character")
                is True
            )
            bm25f_row = bm25f_by_id.get(profile_id)
            embedding_row = embedding_by_id.get(profile_id)
            if bm25f_row is not None and embedding_row is not None:
                match_basis = "bm25f+embedding"
            elif bm25f_row is not None:
                match_basis = "bm25f"
            else:
                match_basis = "embedding"
            hits.append(
                {
                    "profile_id": profile_id,
                    "match_basis": match_basis,
                    "applicability_status": (
                        "eligible"
                        if not requires_adult or adult_context
                        else "requires_existing_adult_context"
                    ),
                    "hard_eligible": False,
                    "optional_eligible": bool(
                        not requires_adult or adult_context
                    ),
                    "source_intent_ids": [],
                    **(
                        {"bm25f_score": float(bm25f_row.get("score", 0.0))}
                        if bm25f_row is not None
                        else {}
                    ),
                    **(
                        {"semantic_score": float(embedding_row.get("semantic_score", 0.0))}
                        if embedding_row is not None
                        else {}
                    ),
                    "fusion_score": float(fused_row.get("score", 0.0)),
                }
            )

    return {
        "contract_version": VISUAL_PROFILE_RESOLUTION_CONTRACT_VERSION,
        "registry_sha256": visual_profile_registry_sha256(registry),
        "index_registry_sha256": str(index.get("registry_sha256") or ""),
        "query_sha256": hashlib.sha256(
            clean_spaces(query_text).encode("utf-8")
        ).hexdigest(),
        "bm25f_evaluated": bm25f_ready,
        "embedding_evaluated": vector_ready,
        "adult_context": bool(adult_context),
        "hits": hits,
    }


def visual_obligation_profile_by_id(registry: JsonDict, profile_id: str) -> Optional[JsonDict]:
    for profile in registry.get("profiles") or []:
        if isinstance(profile, dict) and str(profile.get("id") or "") == profile_id:
            return profile
    return None


def visual_intent_profile_ids_for_source_text(
    registry: JsonDict,
    source_text: str,
    visual_profile_index: Optional[JsonDict] = None,
) -> List[str]:
    """Resolve direct profile IDs through the same exact lane used by runtime."""

    resolution = resolve_visual_profile_hits(
        registry,
        [
            {
                "source": "concept_lock",
                "text": source_text,
                "polarity": "required",
            },
            {
                "source": "authorial_core_interpretation",
                "text": source_text,
                "polarity": "advisory",
            }
        ],
        visual_profile_index=visual_profile_index,
        query_text=source_text,
        adult_context=True,
    )
    return sorted(
        {
            str(hit.get("profile_id") or "")
            for hit in resolution.get("hits") or []
            if isinstance(hit, dict)
            and hit.get("match_basis") == "exact"
            and hit.get("hard_eligible") is True
            and str(hit.get("profile_id") or "")
        }
    )


VISUAL_INTENT_EVIDENCE_STOPWORDS = {
    "a",
    "an",
    "and",
    "as",
    "at",
    "by",
    "for",
    "from",
    "in",
    "into",
    "is",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
    "without",
}


def visual_intent_evidence_tokens(text: str) -> Set[str]:
    """Mirror composed-audit evidence counting before a binding is frozen."""

    return {
        token.lower()
        for token in re.findall(
            r"[A-Za-z0-9]+(?:[./'’\-][A-Za-z0-9]+)*",
            str(text or ""),
        )
        if token.lower() not in VISUAL_INTENT_EVIDENCE_STOPWORDS
    }


def validate_visual_intent_binding(
    *,
    obligation_index: int,
    field: str,
    phrase: str,
    requirement: JsonDict,
) -> None:
    """Reject bindings that would make the emitted pack impossible to audit."""

    try:
        minimum_content_words = int(requirement.get("min_content_words", 3))
    except (TypeError, ValueError):
        minimum_content_words = 3
    actual_content_words = len(visual_intent_evidence_tokens(phrase))
    if actual_content_words < minimum_content_words:
        raise ValueError(
            f"visual intent obligation {obligation_index} binding {field!r} has "
            f"{actual_content_words} content words but requires at least "
            f"{minimum_content_words}; extend the same component evidence before "
            "candidate-pack generation"
        )

    phrase_key = clean_spaces(phrase).lower()
    required_anchors = [
        clean_spaces(str(value))
        for value in requirement.get("must_mention_any") or []
        if clean_spaces(str(value))
    ]
    if required_anchors and not any(
        clean_spaces(anchor).lower() in phrase_key for anchor in required_anchors
    ):
        raise ValueError(
            f"visual intent obligation {obligation_index} binding {field!r} must "
            f"contain one profile component anchor: {required_anchors}"
        )

    forbidden_terms = [
        clean_spaces(str(value))
        for value in requirement.get("must_not_contain") or []
        if clean_spaces(str(value))
    ]
    forbidden_hits = [
        term for term in forbidden_terms if term.lower() in phrase_key
    ]
    if forbidden_hits:
        raise ValueError(
            f"visual intent obligation {obligation_index} binding {field!r} "
            f"contains forbidden profile terms: {forbidden_hits}"
        )

    blanket_directives = find_blanket_negative_directives(phrase)
    if blanket_directives:
        raise ValueError(
            f"visual intent obligation {obligation_index} binding {field!r} "
            "contains a blanket negative directive; express the same local boundary "
            "as positive geometry or visible state: "
            + " | ".join(blanket_directives)
        )


def normalize_visual_intent(
    payload: Any,
    registry: JsonDict,
    visual_profile_index: Optional[JsonDict] = None,
) -> JsonDict:
    """Validate request-scoped hard visual bindings before candidate-pack creation."""

    if not isinstance(payload, dict):
        raise ValueError("--visual-intent-json must contain one JSON object")
    allowed_fields = {"contract_version", "provenance", "obligations"}
    unknown_fields = sorted(set(payload) - allowed_fields)
    if unknown_fields:
        raise ValueError(
            "visual intent contains pack-derived or unsupported fields: "
            + ", ".join(unknown_fields)
        )
    if str(payload.get("contract_version") or "") != VISUAL_INTENT_CONTRACT_VERSION:
        raise ValueError(
            f"visual intent contract_version must be {VISUAL_INTENT_CONTRACT_VERSION!r}"
        )
    if str(payload.get("provenance") or "") != "agent_prepack":
        raise ValueError("visual intent provenance must be 'agent_prepack'")
    raw_obligations = payload.get("obligations")
    if not isinstance(raw_obligations, list) or not raw_obligations:
        raise ValueError("visual intent requires a non-empty obligations list")

    allowed_sources = {
        "requesting_user_definition",
        "explicit_user_requirement",
        "agent_prepack_interpretation",
        "agent_postcore_interpretation",
    }
    normalized_obligations: List[JsonDict] = []
    seen_profile_ids: Set[str] = set()
    for index, item in enumerate(raw_obligations):
        if not isinstance(item, dict):
            raise ValueError(f"visual intent obligation {index} must be an object")
        allowed_item_fields = {
            "profile_id",
            "source",
            "scope",
            "source_text",
            "bindings",
        }
        item_unknown = sorted(set(item) - allowed_item_fields)
        if item_unknown:
            raise ValueError(
                f"visual intent obligation {index} contains unsupported fields: "
                + ", ".join(item_unknown)
            )
        source_text = clean_spaces(str(item.get("source_text") or ""))
        if not source_text:
            raise ValueError(f"visual intent obligation {index} source_text must be non-empty")
        profile_id = str(item.get("profile_id") or "").strip()
        if not profile_id:
            resolved_profile_ids = visual_intent_profile_ids_for_source_text(
                registry,
                source_text,
                visual_profile_index,
            )
            if len(resolved_profile_ids) != 1:
                raise ValueError(
                    f"visual intent obligation {index} without profile_id must resolve exactly one "
                    f"direct profile from source_text; matched {resolved_profile_ids}"
                )
            profile_id = resolved_profile_ids[0]
        profile = visual_obligation_profile_by_id(registry, profile_id)
        if profile is None:
            raise ValueError(f"visual intent obligation {index} has unknown profile_id {profile_id!r}")
        if profile_id in seen_profile_ids:
            raise ValueError(f"visual intent repeats profile_id {profile_id!r}")
        seen_profile_ids.add(profile_id)
        source = str(item.get("source") or "").strip()
        if source not in allowed_sources:
            raise ValueError(
                f"visual intent obligation {index} source must be one of {sorted(allowed_sources)}"
            )
        if str(item.get("scope") or "") != "request_only":
            raise ValueError(
                f"visual intent obligation {index} scope must be 'request_only'"
            )
        raw_bindings = item.get("bindings", {})
        if not isinstance(raw_bindings, dict):
            raise ValueError(f"visual intent obligation {index} bindings must be an object")
        allowed_bindings = {
            str(field)
            for field in profile.get("required_evidence_fields") or []
            if str(field).strip()
        }
        unknown_bindings = sorted(set(raw_bindings) - allowed_bindings)
        if unknown_bindings:
            raise ValueError(
                f"visual intent obligation {index} has unknown binding fields: "
                + ", ".join(unknown_bindings)
            )
        bindings: JsonDict = {}
        evidence_requirements = (
            profile.get("evidence_requirements")
            if isinstance(profile.get("evidence_requirements"), dict)
            else {}
        )
        for field, value in raw_bindings.items():
            phrase = clean_spaces(str(value or ""))
            if not phrase:
                raise ValueError(
                    f"visual intent obligation {index} binding {field!r} must be non-empty"
                )
            requirement = (
                evidence_requirements.get(str(field))
                if isinstance(evidence_requirements.get(str(field)), dict)
                else {}
            )
            validate_visual_intent_binding(
                obligation_index=index,
                field=str(field),
                phrase=phrase,
                requirement=requirement,
            )
            bindings[str(field)] = phrase
        normalized_obligations.append(
            {
                "profile_id": profile_id,
                "source": source,
                "scope": "request_only",
                "source_text": source_text,
                "bindings": bindings,
            }
        )

    normalized: JsonDict = {
        "contract_version": VISUAL_INTENT_CONTRACT_VERSION,
        "provenance": "agent_prepack",
        "obligations": normalized_obligations,
    }
    canonical_bytes = json.dumps(
        normalized,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    normalized["canonical_sha256"] = hashlib.sha256(canonical_bytes).hexdigest()
    normalized["request_id"] = normalized["canonical_sha256"][:16]
    return normalized


def load_visual_intent_arg(
    raw: Optional[str],
    registry: JsonDict,
    visual_profile_index: Optional[JsonDict] = None,
) -> Optional[JsonDict]:
    if not raw:
        return None
    try:
        candidate = Path(raw)
        is_file = candidate.exists()
    except OSError:
        is_file = False
        candidate = Path(".")
    if is_file:
        payload: Any = json.loads(candidate.read_text(encoding="utf-8"))
    else:
        payload = json.loads(raw)
    return normalize_visual_intent(payload, registry, visual_profile_index)


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
    slots: JsonDict,
    mandatory_intents: Sequence[JsonDict],
) -> str:
    provenance = result.get("provenance") if isinstance(result.get("provenance"), dict) else {}
    values: List[str] = [
        str(trace.get("intent") or ""),
    ]
    values.extend(normalize_list(provenance.get("concept_lock")))
    values.extend(normalize_list(provenance.get("additional_requirements")))
    for intent in mandatory_intents:
        if isinstance(intent, dict):
            values.append(str(intent.get("text") or ""))
    for slot_payload in slots.values():
        if not isinstance(slot_payload, dict):
            continue
        for candidate in slot_payload.get("candidates") or []:
            if not isinstance(candidate, dict):
                continue
            values.extend(
                [
                    str(candidate.get("label_en") or ""),
                    str(candidate.get("label_ko") or ""),
                ]
            )
    return " ".join(value for value in values if value.strip())


def candidate_pack_integration_source_corpus(
    result: JsonDict,
    trace: JsonDict,
    mandatory_intents: Sequence[JsonDict],
) -> str:
    provenance = result.get("provenance") if isinstance(result.get("provenance"), dict) else {}
    values: List[str] = [str(trace.get("intent") or "")]
    values.extend(normalize_list(provenance.get("concept_lock")))
    values.extend(normalize_list(provenance.get("additional_requirements")))
    values.extend(normalize_list(provenance.get("user_mandatory_intents")))
    for intent in mandatory_intents:
        if not isinstance(intent, dict):
            continue
        if str(intent.get("source") or "") in {"user_requirement", "additional_requirement"}:
            values.append(str(intent.get("text") or ""))
    return " ".join(value for value in values if value.strip())


def candidate_pack_quality_layers(data: JsonDict) -> JsonDict:
    quality = data.get(QUALITY_LAYERS_DATA_KEY)
    return quality if isinstance(quality, dict) else {}


def candidate_pack_visual_obligation_request_sources(
    result: JsonDict,
    trace: JsonDict,
) -> List[JsonDict]:
    allowed_sources = {
        "concept_lock",
        "user_requirement",
        "additional_requirement",
        "intent",
        "authorial_core_interpretation",
        "authorial_core_baseline",
        "authorial_core_definition",
    }
    return [
        row
        for row in candidate_pack_source_texts(result, trace)
        if isinstance(row, dict)
        and str(row.get("source") or "") in allowed_sources
        and str(row.get("polarity") or "") != "excluded"
        and str(row.get("text") or "").strip()
    ]


def candidate_pack_auto_visual_obligation_matches(
    registry: JsonDict,
    source_rows: Sequence[JsonDict],
) -> Dict[str, List[JsonDict]]:
    """Project the resolver's exact activation lane into source records."""

    resolution = resolve_visual_profile_hits(
        registry,
        source_rows,
        adult_context=True,
    )
    return {
        str(hit.get("profile_id") or ""): copy.deepcopy(
            hit.get("source_records") or []
        )
        for hit in resolution.get("hits") or []
        if isinstance(hit, dict)
        and hit.get("match_basis") == "exact"
        and hit.get("hard_eligible") is True
        and str(hit.get("profile_id") or "")
    }


def candidate_pack_visual_component_match(
    profile: JsonDict,
    text: str,
) -> Optional[str]:
    """Classify indirect lexical semantics without hard-activating a profile.

    The component lexicon is intentionally data-driven.  It may make a concept
    eligible for authorial opt-in, but it can never create a hard obligation.
    """

    activation = (
        profile.get("activation")
        if isinstance(profile.get("activation"), dict)
        else {}
    )
    excluded_terms = [
        str(term).strip()
        for term in activation.get("exclude_if_any_terms") or []
        if str(term).strip()
    ]
    if any(intent_alias_matches(text, term) for term in excluded_terms):
        return None
    profile_semantics = (
        profile.get("semantics")
        if isinstance(profile.get("semantics"), dict)
        else {}
    )
    semantics = (
        profile_semantics.get("component_semantics")
        if isinstance(profile_semantics.get("component_semantics"), dict)
        else {}
    )
    groups = [
        group
        for group in semantics.get("groups") or []
        if isinstance(group, dict) and str(group.get("id") or "").strip()
    ]
    matched_group_ids = {
        str(group["id"])
        for group in groups
        if any(
            intent_alias_matches(text, str(term))
            for term in group.get("any_terms") or []
            if str(term).strip()
        )
    }
    try:
        minimum_groups = int(semantics.get("minimum_component_groups", 2))
    except (TypeError, ValueError):
        minimum_groups = 2
    required_groups = {
        str(value)
        for value in semantics.get("required_group_ids") or []
        if str(value).strip()
    }
    if (
        groups
        and len(matched_group_ids) >= max(1, minimum_groups)
        and required_groups <= matched_group_ids
    ):
        return "component_semantics"
    soft_terms = [
        str(term).strip()
        for term in profile_semantics.get("paraphrase_examples") or []
        if str(term).strip()
    ]
    if any(intent_alias_matches(text, term) for term in soft_terms):
        return "semantic_paraphrase_example"
    return None


def candidate_pack_auto_visual_concept_matches(
    registry: JsonDict,
    source_rows: Sequence[JsonDict],
) -> Dict[str, List[JsonDict]]:
    """Return indirect concept eligibility; never return hard activation."""

    resolution = resolve_visual_profile_hits(registry, source_rows, adult_context=True)
    matches: Dict[str, List[JsonDict]] = {
        str(hit["profile_id"]): [
            {**copy.deepcopy(source), "match_kind": "request_scoped_related_concept"}
            for source in hit.get("source_records") or []
        ]
        for hit in resolution.get("hits") or []
        if hit.get("optional_eligible") is True
    }
    hard_matches = {
        str(hit["profile_id"])
        for hit in resolution.get("hits") or []
        if hit.get("hard_eligible") is True
    }
    for profile in registry.get("profiles") or []:
        if not isinstance(profile, dict):
            continue
        profile_id = str(profile.get("id") or "").strip()
        if not profile_id or profile_id in hard_matches:
            continue
        profile_matches: List[JsonDict] = []
        for row in source_rows:
            text = str(row.get("text") or "")
            match_kind = candidate_pack_visual_component_match(profile, text)
            if match_kind is None:
                continue
            source_key = hashlib.sha256(
                f"{row.get('source')}|{clean_spaces(text).lower()}".encode("utf-8")
            ).hexdigest()[:16]
            profile_matches.append(
                {
                    "source_intent_id": f"{row.get('source')}:{source_key}",
                    "source": str(row.get("source") or ""),
                    "match_kind": match_kind,
                }
            )
        if profile_matches:
            matches.setdefault(profile_id, []).extend(profile_matches)
    return matches


def candidate_pack_visual_obligation_adult_context(
    source_rows: Sequence[JsonDict],
    moe_response: Optional[JsonDict],
) -> bool:
    if isinstance(moe_response, dict) and moe_response.get("enabled") is True:
        return True
    adult_terms = (
        "adult",
        "mid twenties",
        "mid-twenties",
        "twenty five or older",
        "25 or older",
        "성인",
        "여성",
        "20대 중반",
        "成人",
        "女性",
        "woman",
        "women",
        "lady",
    )
    return any(
        intent_alias_matches(str(row.get("text") or ""), term)
        for row in source_rows
        for term in adult_terms
    )


def candidate_pack_resolve_visual_profiles(
    data: JsonDict,
    result: JsonDict,
    trace: JsonDict,
    moe_response: Optional[JsonDict],
) -> JsonDict:
    """Resolve the private visual-profile match set exactly once per pack."""

    registry = (
        data.get(VISUAL_OBLIGATIONS_DATA_KEY)
        if isinstance(data.get(VISUAL_OBLIGATIONS_DATA_KEY), dict)
        else {}
    )
    if not registry:
        return {
            "contract_version": VISUAL_PROFILE_RESOLUTION_CONTRACT_VERSION,
            "hits": [],
        }
    visual_profile_index = (
        data.get(VISUAL_PROFILE_INDEX_DATA_KEY)
        if isinstance(data.get(VISUAL_PROFILE_INDEX_DATA_KEY), dict)
        else build_visual_profile_index_payload(registry)
    )
    source_rows = candidate_pack_visual_obligation_request_sources(result, trace)
    provenance = (
        result.get("provenance")
        if isinstance(result.get("provenance"), dict)
        else {}
    )
    core = (
        provenance.get("authorial_core")
        if isinstance(provenance.get("authorial_core"), dict)
        else {}
    )
    if core:
        query_text, _query_provenance = authorial_core_retrieval_text(core)
    else:
        query_text = " | ".join(
            clean_spaces(str(row.get("text") or ""))
            for row in source_rows
            if clean_spaces(str(row.get("text") or ""))
        )
    prompt_id = str(provenance.get("prompt_id") or "")
    query_vectors = (
        data.get(VISUAL_PROFILE_QUERY_VECTORS_DATA_KEY)
        if isinstance(data.get(VISUAL_PROFILE_QUERY_VECTORS_DATA_KEY), dict)
        else {}
    )
    query_vector = query_vectors.get(prompt_id)
    resolution = resolve_visual_profile_hits(
        registry,
        source_rows,
        visual_profile_index=visual_profile_index,
        query_text=query_text,
        query_fields=(
            authorial_core_bm25f_query_fields(core)
            if core.get("contract_version") == AUTHORIAL_CORE_V3_CONTRACT_VERSION
            else None
        ),
        query_vector=(query_vector if isinstance(query_vector, list) else None),
        user_definitions=[
            item
            for item in core.get("user_definitions") or []
            if isinstance(item, dict)
        ],
        adult_context=candidate_pack_visual_obligation_adult_context(
            source_rows,
            moe_response,
        ),
    )
    existing_ids = {hit["profile_id"] for hit in resolution.get("hits") or []}
    context_text = authorial_core_retrieval_text(core)[0] if core else ""
    adult_context = candidate_pack_visual_obligation_adult_context(source_rows, moe_response)
    documents: JsonDict = {}
    for profile in registry.get("profiles") or []:
        candidate = profile.get("concept_candidate") or {}
        if (candidate.get("core_assertion_discovery") is not True
                or profile["id"] in existing_ids
                or ((profile.get("activation") or {}).get("requires_adult_character") and not adult_context)
                or not visual_profile_context_applicability(
                    profile, context_text, has_authorial_core_context=bool(core),
                    require_positive_context_terms=False,
                )[0]):
            continue
        documents[profile["id"]] = {**candidate, "en": (profile.get("semantics") or {}).get("definition") or ""}
    for profile_id in candidate_pack_assertion_discovery(
        data, core, documents, visual_profile_index.get("bm25f") or {},
    ):
        resolution.setdefault("hits", []).append({
            "profile_id": profile_id, "match_basis": "bm25f_frozen_assertion",
            "applicability_status": "eligible", "hard_eligible": False,
            "optional_eligible": True, "source_intent_ids": [],
        })
    # A fully observed, source-opted-in relation can be drowned out by a
    # long scene's broad similarity hits. Rank this narrow lane separately;
    # preserve the same effect, lock, exclusion and optionality guards.
    observed_text = " ".join(str(row.get("text") or "") for row in source_rows)
    component_documents = {
        profile["id"]: documents[profile["id"]]
        for profile in registry.get("profiles") or []
        if profile["id"] in documents
        and (profile.get("activation") or {}).get(
            "semantic_discovery_requires_component_evidence") is True
        and candidate_pack_visual_component_match(profile, observed_text) is not None
    }
    existing_ids = {hit["profile_id"] for hit in resolution.get("hits") or []}
    for profile_id in candidate_pack_assertion_discovery(
        data, core, component_documents, visual_profile_index.get("bm25f") or {},
        include_frozen_baseline=True,
    ):
        if profile_id not in existing_ids:
            resolution.setdefault("hits", []).append({
                "profile_id": profile_id, "match_basis": "bm25f_frozen_components",
                "applicability_status": "eligible", "hard_eligible": False,
                "optional_eligible": True, "source_intent_ids": [],
            })
    return resolution


def candidate_pack_visual_profile_obligation(
    profile: JsonDict,
    registry: JsonDict,
    *,
    activation_source: str,
    source_intent_ids: Sequence[str],
    bindings: Optional[JsonDict] = None,
    context_text: str = "",
    request_text: str = "",
) -> JsonDict:
    """Materialize one profile into the same auditable obligation shape."""

    profile = compile_visual_profile(
        profile,
        context_text=context_text,
        request_text=request_text,
        matches=intent_alias_matches,
    )
    render_gates = [
        copy.deepcopy(gate)
        for gate in profile.get("render_gates") or []
        if isinstance(gate, dict) and str(gate.get("id") or "").strip()
    ]
    required_fields = [
        str(field)
        for field in profile.get("required_evidence_fields") or []
        if str(field).strip()
    ]
    evidence_policy = (
        registry.get("evidence_policy")
        if isinstance(registry.get("evidence_policy"), dict)
        else {}
    )
    obligation: JsonDict = {
        "id": str(profile.get("id") or ""),
        "category": str(profile.get("category") or "visual_mechanism"),
        "activation": {
            "source": activation_source,
            "scope": "request_only",
            "source_intent_ids": [str(value) for value in source_intent_ids],
        },
        "composition_instruction": str(profile.get("composition_instruction") or ""),
        "component_semantics": copy.deepcopy(
            ((profile.get("semantics") or {}).get("component_semantics")) or {}
        ),
        "prompt_binding": {
            "composed_field": "visual_obligation_evidence",
            "required_evidence_fields": required_fields,
            "minimum_distinct_evidence_phrases": len(required_fields),
            "prompt_evidence_must_be_literal": True,
            "maximum_pairwise_content_token_overlap_ratio": float(
                evidence_policy.get("maximum_pairwise_content_token_overlap_ratio", 0.8)
            ),
            "forbidden_filler_phrases": [
                str(value)
                for value in evidence_policy.get("forbidden_filler_phrases") or []
                if str(value).strip()
            ],
        },
        "evidence_requirements": copy.deepcopy(
            profile.get("evidence_requirements") or {}
        ),
        "runtime_expression": copy.deepcopy(profile.get("runtime_expression") or {}),
        "render_gates": render_gates,
        "reject_substitutes": [
            str(value)
            for value in profile.get("reject_substitutes") or []
            if str(value).strip()
        ],
    }
    if isinstance(profile.get("visual_relation"), dict):
        obligation["visual_relation"] = copy.deepcopy(profile["visual_relation"])
    if bindings:
        obligation["bindings"] = copy.deepcopy(bindings)
    return obligation


def candidate_pack_visual_obligations(
    data: JsonDict,
    result: JsonDict,
    trace: JsonDict,
    moe_response: Optional[JsonDict],
    visual_profile_resolution: Optional[JsonDict] = None,
) -> Optional[JsonDict]:
    registry = (
        data.get(VISUAL_OBLIGATIONS_DATA_KEY)
        if isinstance(data.get(VISUAL_OBLIGATIONS_DATA_KEY), dict)
        else {}
    )
    if not registry:
        return None
    source_rows = candidate_pack_visual_obligation_request_sources(result, trace)
    if isinstance(visual_profile_resolution, dict):
        auto_matches = {
            str(hit.get("profile_id") or ""): copy.deepcopy(
                hit.get("source_records") or []
            )
            for hit in visual_profile_resolution.get("hits") or []
            if isinstance(hit, dict)
            and hit.get("match_basis") == "exact"
            and hit.get("hard_eligible") is True
            and str(hit.get("profile_id") or "")
        }
    else:
        auto_matches = candidate_pack_auto_visual_obligation_matches(
            registry,
            source_rows,
        )
    adult_context = candidate_pack_visual_obligation_adult_context(
        source_rows,
        moe_response,
    )
    provenance = result.get("provenance") if isinstance(result.get("provenance"), dict) else {}
    explicit_intent = (
        provenance.get("visual_intent")
        if isinstance(provenance.get("visual_intent"), dict)
        else None
    )

    requesting_user_source_texts = {
        clean_spaces(str(row.get("text") or "")).lower()
        for row in source_rows
        if str(row.get("source") or "")
        in {"concept_lock", "user_requirement", "additional_requirement", "intent"}
        if clean_spaces(str(row.get("text") or ""))
    }
    authorial_source_texts: Set[str] = set()
    authorial_core = (
        provenance.get("authorial_core")
        if isinstance(provenance.get("authorial_core"), dict)
        else {}
    )
    authorial_source_texts.update(
        clean_spaces(str(value)).lower()
        for value in [
            authorial_core.get("interpreted_intent"),
            authorial_core.get("baseline_prompt_en"),
            *(authorial_core.get("visual_priorities") or []),
            *(
                item.get("interpreted_meaning")
                for item in authorial_core.get("user_definitions") or []
                if isinstance(item, dict)
            ),
            *(
                item.get("resolution")
                for item in authorial_core.get("interpretation_provenance") or []
                if isinstance(item, dict)
            ),
        ]
        if clean_spaces(str(value or ""))
    )
    explicit_by_profile: Dict[str, JsonDict] = {}
    if explicit_intent is not None:
        for item in explicit_intent.get("obligations") or []:
            if not isinstance(item, dict):
                continue
            profile_id = str(item.get("profile_id") or "")
            source_text = clean_spaces(str(item.get("source_text") or "")).lower()
            allowed_texts = set(requesting_user_source_texts)
            if str(item.get("source") or "") in {
                "agent_prepack_interpretation",
                "agent_postcore_interpretation",
            }:
                allowed_texts.update(authorial_source_texts)
            if source_text not in allowed_texts:
                raise ValueError(
                    f"visual intent profile {profile_id!r} source_text must exactly match "
                    "a requesting-user source or its governing frozen authorial field"
                )
            explicit_by_profile[profile_id] = item

    obligations: List[JsonDict] = []
    required_hard_gates: List[str] = []
    for profile in registry.get("profiles") or []:
        if not isinstance(profile, dict):
            continue
        profile_id = str(profile.get("id") or "").strip()
        activation = (
            profile.get("activation")
            if isinstance(profile.get("activation"), dict)
            else {}
        )
        explicit = explicit_by_profile.get(profile_id)
        matched_sources = auto_matches.get(profile_id, [])
        active = explicit is not None or bool(matched_sources)
        if not active:
            continue
        if activation.get("requires_adult_character") is True and not adult_context:
            if explicit is not None:
                raise ValueError(
                    f"visual intent profile {profile_id!r} requires explicit adult-character context"
                )
            continue
        source_intent_ids = (
            [
                "visual-intent:"
                + hashlib.sha256(
                    clean_spaces(str(explicit.get("source_text") or "")).lower().encode("utf-8")
                ).hexdigest()[:16]
            ]
            if explicit is not None
            else [str(row["source_intent_id"]) for row in matched_sources]
        )
        obligation = candidate_pack_visual_profile_obligation(
            profile,
            registry,
            activation_source=(
                str(explicit.get("source") or "")
                if explicit is not None
                else "explicit_request_semantics"
            ),
            source_intent_ids=source_intent_ids,
            bindings=(
                explicit.get("bindings")
                if explicit is not None and isinstance(explicit.get("bindings"), dict)
                else None
            ),
            context_text=" ".join(str(row.get("text") or "") for row in source_rows),
            request_text=" ".join(
                str(row.get("text") or "") for row in source_rows
                if str(row.get("source") or "") in {
                    "concept_lock", "user_requirement", "additional_requirement", "intent"
                }
            ),
        )
        required_hard_gates.extend(
            str(gate.get("id") or "")
            for gate in obligation.get("render_gates") or []
            if isinstance(gate, dict) and str(gate.get("id") or "").strip()
        )
        obligations.append(obligation)

    if not obligations:
        return None
    contract: JsonDict = {
        "enabled": True,
        "contract_version": VISUAL_OBLIGATIONS_CONTRACT_VERSION,
        "precedence": copy.deepcopy(registry.get("precedence") or []),
        "scope": "request_only",
        "strict_gate_set": True,
        "obligations": obligations,
        "required_hard_gates": list(dict.fromkeys(required_hard_gates)),
        "retry_policy": {
            "preserve_every_attempt": True,
            "repair_only_failed_visual_obligations": True,
            "preserve_passed_identity_and_mechanism_evidence": True,
            "stop_at_first_all_hard_gates_pass": True,
            "requesting_user_judgment_remains_separate": True,
        },
    }
    if explicit_intent is not None:
        contract["source_visual_intent_sha256"] = str(
            explicit_intent.get("canonical_sha256") or ""
        )
    return contract


def candidate_pack_visual_concept_candidates(
    data: JsonDict,
    result: JsonDict,
    trace: JsonDict,
    moe_response: Optional[JsonDict],
    visual_obligations: Optional[JsonDict],
    visual_profile_resolution: Optional[JsonDict] = None,
) -> Optional[JsonDict]:
    """Expose indirect concepts as optional, non-ranked candidates.

    The public candidate omits scores, matched terms, and routing reasons.  If
    the composer selects it, its pre-baked opt-in obligation becomes hard in
    the composed and render-review audits; otherwise it contributes no gate.
    """

    registry = (
        data.get(VISUAL_OBLIGATIONS_DATA_KEY)
        if isinstance(data.get(VISUAL_OBLIGATIONS_DATA_KEY), dict)
        else {}
    )
    if not registry:
        return None
    source_rows = candidate_pack_visual_obligation_request_sources(result, trace)
    if isinstance(visual_profile_resolution, dict):
        matches = {
            str(hit.get("profile_id") or ""): [
                {
                    "source": "hybrid_visual_profile_resolution",
                    "match_kind": str(hit.get("match_basis") or ""),
                }
            ]
            for hit in visual_profile_resolution.get("hits") or []
            if isinstance(hit, dict)
            and hit.get("optional_eligible") is True
            and str(hit.get("profile_id") or "")
        }
    else:
        adult_context = candidate_pack_visual_obligation_adult_context(
            source_rows,
            moe_response,
        )
        matches = candidate_pack_auto_visual_concept_matches(registry, source_rows)
        profiles_by_id = {
            str(profile.get("id") or ""): profile
            for profile in registry.get("profiles") or []
            if isinstance(profile, dict) and str(profile.get("id") or "").strip()
        }
        matches = {
            profile_id: rows
            for profile_id, rows in matches.items()
            if (
                (profiles_by_id.get(profile_id, {}).get("activation") or {}).get(
                    "requires_adult_character"
                )
                is not True
                or adult_context
            )
        }
    active_hard_ids = {
        str(item.get("id") or "")
        for item in (visual_obligations or {}).get("obligations") or []
        if isinstance(item, dict) and str(item.get("id") or "")
    }
    candidates: List[JsonDict] = []
    for profile in registry.get("profiles") or []:
        if not isinstance(profile, dict):
            continue
        profile_id = str(profile.get("id") or "").strip()
        if not profile_id or profile_id in active_hard_ids or profile_id not in matches:
            continue
        concept_candidate = (
            profile.get("concept_candidate")
            if isinstance(profile.get("concept_candidate"), dict)
            else {}
        )
        concept_terms = [
            str(term).strip()
            for term in concept_candidate.get("concept_terms") or []
            if str(term).strip()
        ]
        if not concept_terms:
            continue
        core = (result.get("provenance") or {}).get("authorial_core") or {}
        scope = {key: copy.deepcopy(concept_candidate[key]) for key in ("affected_dimensions", "affected_properties")
                 if key in concept_candidate}
        if scope and (
            not set(scope.get("affected_dimensions") or []) <= set((core.get("intent_lock") or {}).get("open_dimensions") or [])
            or not property_effects_allowed(core.get("intent_lock") or {}, scope.get("affected_dimensions") or [], scope.get("affected_properties"))
        ):
            continue
        obligation = candidate_pack_visual_profile_obligation(
            profile,
            registry,
            activation_source="composer_opt_in",
            source_intent_ids=[],
            context_text=" ".join(str(row.get("text") or "") for row in source_rows),
            request_text=" ".join(
                str(row.get("text") or "") for row in source_rows
                if str(row.get("source") or "") in {
                    "concept_lock", "user_requirement", "additional_requirement", "intent"
                }
            ),
        )
        candidates.append(
            {
                "id": f"visual-concept:{profile_id}",
                "content_form": "unordered_inspiration_terms",
                "concept_terms": concept_terms,
                **scope,
                "applicability": {
                    "status": "eligible",
                    "source": (
                        "hybrid_visual_profile_resolution"
                        if isinstance(visual_profile_resolution, dict)
                        else "request_scoped_concept_eligibility"
                    ),
                },
                "opt_in_contract": {
                    "effect": "promote_to_hard_visual_obligation",
                    "visual_obligations_contract_version": VISUAL_OBLIGATIONS_CONTRACT_VERSION,
                    "obligation": obligation,
                },
            }
        )
    if not candidates:
        return None
    return {
        "enabled": True,
        "contract_version": VISUAL_CONCEPTS_CONTRACT_VERSION,
        "candidate_order": "seed_shuffled_non_preferential",
        "selection_field": "chosen_visual_concept_ids",
        "selection_policy": {
            "all_candidates_optional": True,
            "selection_list_required_even_when_empty": True,
            "unselected_candidates_add_no_prompt_or_review_duty": True,
            "selected_candidates_promote_opt_in_contract_to_hard_obligation": True,
            "matched_terms_scores_and_routing_reasons_not_exposed": True,
        },
        "candidates": candidates,
    }


def authorial_meaning_clarification(core: JsonDict) -> JsonDict:
    """Project requester duties without promoting the whole authored direction."""
    intent_lock = core.get("intent_lock") if isinstance(core.get("intent_lock"), dict) else {}
    phrases = [
        str(anchor.get("prompt_evidence") or "")
        for anchor in intent_lock.get("semantic_anchors") or []
        if isinstance(anchor, dict)
    ]
    for assertion in core.get("semantic_assertions") or []:
        if isinstance(assertion, dict) and assertion.get("polarity") == "required":
            evidence = assertion.get("evidence")
            if isinstance(evidence, dict):
                phrases.extend(value for value in evidence.values() if isinstance(value, str))
    return {
        "id": "clarification:authorial-core:interpreted-intent",
        "source": "requester_meaning_bound_by_authorial_core",
        "interpreted_meaning": "Preserve the requester-owned meaning expressed by the frozen anchors and required assertions.",
        "meaning_components": list(dict.fromkeys(phrase for phrase in phrases if phrase.strip())),
        "applicability": {
            "status": "required",
            "reason": "requester_owned_meaning_is_fixed_while_unbound_authorial_choices_remain_editable",
        },
        "required_in_final_prompt": True,
        "revisable": False,
        "creative_sampling": False,
        **(
            {"forbidden_runtime_labels": copy.deepcopy(core["runtime_forbidden_labels"])}
            if core.get("runtime_forbidden_labels") else {}
        ),
    }


def authorial_direction_context(core: JsonDict) -> JsonDict:
    """Keep the initial whole-image judgment visible as context, not a new lock."""
    return {
        "source": "agent_prepack",
        "interpreted_intent": str(core.get("interpreted_intent") or ""),
        "visual_priorities": copy.deepcopy(core.get("visual_priorities") or []),
        "creates_additional_locks": False,
        "revision_policy": "recompose_agent_choices_within_requester_locks",
    }


def candidate_pack_semantic_clarification(
    data: JsonDict,
    result: JsonDict,
    trace: JsonDict,
    visual_obligations: Optional[JsonDict],
    visual_concept_candidates: Optional[JsonDict],
    visual_profile_resolution: Optional[JsonDict] = None,
) -> Optional[JsonDict]:
    """Expose deterministic meaning aids separately from creative material."""
    provenance = result.get("provenance") if isinstance(result.get("provenance"), dict) else {}
    core = (
        provenance.get("authorial_core")
        if isinstance(provenance.get("authorial_core"), dict)
        else {}
    )
    candidates: List[JsonDict] = []
    if core:
        if core.get("contract_version") != AUTHORIAL_CORE_V3_CONTRACT_VERSION:
            raise ValueError("semantic clarification requires the current authorial core")
        candidates.append(authorial_meaning_clarification(core))
    for definition in core.get("user_definitions") or []:
        if not isinstance(definition, dict):
            continue
        term = str(definition.get('term') or '')
        definition_id = hashlib.sha256(
            f"user-definition|{term.lower()}|{definition.get('source_text')}".encode("utf-8")
        ).hexdigest()[:16]
        candidates.append(
            {
                "id": f"clarification:user-definition:{definition_id}",
                "source": "requesting_user_definition",
                "term": term,
                "interpreted_meaning": str(definition.get('interpreted_meaning') or ''),
                "meaning_components": [str(definition.get('prompt_evidence') or '')],
                "required_prompt_evidence": str(definition.get('prompt_evidence') or ''),
                "applicability": {
                    "status": "required",
                    "reason": "requesting_user_definition_has_precedence",
                },
                "required_in_final_prompt": True,
                "revisable": False,
                "creative_sampling": False,
            }
        )
    registry = (
        data.get(VISUAL_OBLIGATIONS_DATA_KEY)
        if isinstance(data.get(VISUAL_OBLIGATIONS_DATA_KEY), dict)
        else {}
    )
    if isinstance(visual_profile_resolution, dict):
        resolution_hits = {
            str(hit.get('profile_id') or ''): hit
            for hit in visual_profile_resolution.get("hits") or []
            if isinstance(hit, dict) and str(hit.get('profile_id') or '')
        }
    else:
        source_rows = candidate_pack_visual_obligation_request_sources(result, trace)
        direct_matches = candidate_pack_auto_visual_obligation_matches(registry, source_rows)
        raw_trigger_rows = [
            row
            for row in source_rows
            if str(row.get('source') or '')
            in {"concept_lock", "user_requirement", "additional_requirement", "intent"}
        ]
        raw_direct_matches = candidate_pack_auto_visual_obligation_matches(
            registry, raw_trigger_rows
        )
        resolution_hits = {
            profile_id: {
                "profile_id": profile_id,
                "match_basis": "exact",
                "applicability_status": "required",
            }
            for profile_id in set(direct_matches) | set(raw_direct_matches)
        }
    active_ids = {
        str(item.get('id') or '')
        for item in (visual_obligations or {}).get("obligations") or []
        if isinstance(item, dict)
    }
    optional_ids = {
        str(((item.get('opt_in_contract') or {}).get('obligation') or {}).get('id') or '')
        for item in (visual_concept_candidates or {}).get("candidates") or []
        if isinstance(item, dict)
    }
    for profile in registry.get("profiles") or []:
        if not isinstance(profile, dict):
            continue
        profile_id = str(profile.get('id') or '')
        resolution_hit = resolution_hits.get(profile_id)
        if (
            resolution_hit is None
            and profile_id not in active_ids
            and (profile_id not in optional_ids)
        ):
            continue
        if (
            isinstance(resolution_hit, dict)
            and resolution_hit.get("applicability_status") == "user_definition_override"
        ):
            continue
        runtime = (
            profile.get("runtime_expression")
            if isinstance(profile.get("runtime_expression"), dict)
            else {}
        )
        concept_candidate = (
            profile.get("concept_candidate")
            if isinstance(profile.get("concept_candidate"), dict)
            else {}
        )
        if profile_id in active_ids:
            status = "required"
            reason = "active_request_scoped_visual_obligation"
            required = True
        elif profile_id in optional_ids:
            status = "eligible"
            reason = (
                "embedding_retrieved_optional_visual_concept"
                if isinstance(resolution_hit, dict)
                and resolution_hit.get("match_basis") == "embedding"
                else "contextual_visual_concept_candidate"
            )
            required = False
        elif (
            isinstance(resolution_hit, dict)
            and resolution_hit.get("applicability_status") == "context_mismatch"
        ):
            status = "context_mismatch"
            reason = "the_authorial_core_resolved_the_term_to_a_different_contextual_sense"
            required = False
        else:
            status = "requires_existing_adult_context"
            reason = "meaning_is_exposed_but_the_existing_adult_context_gate_did_not_activate"
            required = False
        candidates.append(
            {
                "id": f"clarification:visual-profile:{profile_id}",
                "source": "visual_meaning_registry",
                "profile_id": profile_id,
                "interpreted_meaning": str((profile.get('semantics') or {}).get('definition') or profile.get('composition_instruction') or ''),
                "meaning_components": [
                    str(item)
                    for item in concept_candidate.get("concept_terms") or []
                    if str(item).strip()
                ],
                "runtime_expression_mode": str(runtime.get('default_mode') or 'definition_only'),
                "forbidden_runtime_labels": [
                    str(item)
                    for item in runtime.get("runtime_forbidden_labels") or []
                    if str(item).strip()
                ],
                "applicability": {"status": status, "reason": reason},
                "required_in_final_prompt": required,
                "revisable": False,
                "creative_sampling": False,
            }
        )
    if not candidates:
        return None
    candidates.sort(key=lambda item: str(item.get('id') or ''))
    return {
        "enabled": True,
        "contract_version": SEMANTIC_CLARIFICATION_CONTRACT_VERSION,
        "source_authorial_core_sha256": str(core.get('canonical_sha256') or ''),
        "selection": "deterministic_contextual_meaning_resolution",
        "affected_by_creativity": False,
        "affected_by_seed": False,
        "user_definition_precedence": True,
        "candidates": candidates,
        **({"authorial_direction": authorial_direction_context(core)} if core else {}),
        "composition_contract": {
            "composed_field": "semantic_clarification_decisions",
            "every_candidate_requires_a_typed_decision": True,
            "required_candidates_cannot_be_rejected": True,
            "governing_meaning_change_requires_new_core": True,
            "applied_evidence_must_be_literal": True,
            "forbidden_runtime_labels_must_remain_absent": True,
        },
    }


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

# These packs are deliberately broad in subject matter but operationally
# to bypass this automatic-discovery scope.

# Slot entries in the new packs already carry one of these authored tags. The
# mapping prevents a generic overlap such as ``food`` or ``documentary`` from
# making a fermentation batch or camera-trap record eligible in a generic
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
    "character_scene_grammar": "character_scene_grammar",
}


def candidate_pack_quality_inferred_tag_facet_keys(
    vocab: Dict[str, Set[str]],
    slot: str,
    strict: bool = False,
) -> Set[str]:
    """Limit implicit tag-to-facet inference for typed domains.

    Explicit ``facets`` remain valid on every entry. The slot boundary only
    prevents incidental tokens such as ``street`` in a focus-mode tag from
    being misread as the scene's actual place type. Untyped domains use
    the full vocabulary for tag-to-facet inference.
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
    *,
    exclude_people: bool = False,
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
            if exclude_people and "human" in (entry_kinds(entry) | entry_tags(entry)):
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


def candidate_pack_quality_profile_id(domains: Set[str], facets: Dict[str, Set[str]]) -> str:
    subject_kinds = facets.get("subject_kind", set())
    mood_families = facets.get("mood_family", set())
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
    if "character_scene_grammar" in domains:
        return "character_scene_grammar"
    if "food" in subject_kinds or "food" in domains:
        return "food"
    if "architecture" in domains or "real_estate" in domains:
        return "architecture"
    if subject_kinds & {"object", "sign"} or domains & {"product", "jewelry"}:
        return "product"
    if domains & {"wildlife", "landscape", "nature"} or subject_kinds & {"animal", "plant", "environment"}:
        return "nature"
    if "documentary" in domains:
        return "documentary"
    if domains & {"portrait", "fashion", "beauty", "editorial"}:
        return "portrait_editorial"
    if "documentary" in mood_families:
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
    choices = result.get("choices") if isinstance(result.get("choices"), dict) else {}
    for slot, choice in choices.items():
        if isinstance(choice, dict):
            candidate_pack_quality_add_entry_facets(
                facets,
                vocab,
                choice,
                inferred_tag_facet_keys=candidate_pack_quality_inferred_tag_facet_keys(
                    vocab, str(slot), strict=True
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
                    vocab, str(slot), strict=True
                ),
                include_subject_kind=str(slot) == "subject",
            )

    matched_facets = candidate_pack_quality_add_intent_facets(facets, vocab, data, mandatory_intents)
    profile_id = candidate_pack_quality_profile_id(set(((result.get("semantic_trace") or {}).get("generation_contract") or {}).get("domains") or []), facets)
    trace = result.get("semantic_trace") if isinstance(result.get("semantic_trace"), dict) else {}
    generation_contract = (
        trace.get("generation_contract")
        if isinstance(trace.get("generation_contract"), dict)
        else {}
    )
    no_people = bool(
        ((generation_contract.get("intent_constraints") or {}).get("no_people"))
    ) or generation_explicitly_excludes_people(None, generation_contract)
    provenance = result.get("provenance") if isinstance(result.get("provenance"), dict) else {}
    no_people = no_people or any(
        intent_explicitly_excludes_people(value)
        for key in ("concept_lock", "user_mandatory_intents", "additional_requirements")
        for value in normalize_list(provenance.get(key))
    )
    matched_subject_entries = candidate_pack_quality_add_literal_subject_entity_facets(
        facets,
        vocab,
        data,
        mandatory_intents,
        exclude_people=no_people,
    )
    return {
        "profile_id": profile_id,
        "source": "frozen_core_and_literal_intent_facets",
        "facets": {
            key: sorted(values)
            for key, values in sorted(facets.items())
            if values and key not in CONTROL_ONLY_FACET_KEYS
        },
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
    slots: JsonDict,
    mandatory_intents: Sequence[JsonDict],
    quality_profile: JsonDict,
) -> JsonDict:
    corpus = candidate_pack_integration_corpus(result, trace, slots, mandatory_intents)
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
    # A typed visible-subject facet and literal frozen-core evidence are more
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
    concept = str((result.get("provenance") or {}).get("concept_lock") or corpus)
    entry_id = str(entry.get("id") or "")
    fallback = policy.get("fallback") if isinstance(policy.get("fallback"), dict) else {}
    preferred = normalize_list(fallback.get(slot))
    prefix = "0" if entry_id in preferred else "1"
    return prefix + hashlib.sha256(f"visual-proposition|{seed}|{concept}|{slot}|{entry_id}".encode("utf-8")).hexdigest()


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
    slots: JsonDict,
    mandatory_intents: Sequence[JsonDict],
    quality_profile: JsonDict,
) -> JsonDict:
    corpus = candidate_pack_integration_corpus(result, trace, slots, mandatory_intents)
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


def candidate_pack_contract_version(version: str) -> str:
    if version not in {"v6", CANDIDATE_PACK_CONTRACT_V6}:
        raise ValueError(f"unsupported candidate-pack version: {version!r}; expected v6")
    return CANDIDATE_PACK_CONTRACT_V6


def candidate_pack_recompute_id(pack: JsonDict) -> JsonDict:
    hashable = dict(pack)
    hashable["pack_id"] = None
    pack["pack_id"] = stable_text_id(
        json.dumps(hashable, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    ) or ""
    return pack


def candidate_pack_remove_quality_profile_sources(value: Any) -> None:
    if isinstance(value, dict):
        if "profile_id" in value and "facets" in value:
            value.pop("source", None)
        for item in value.values():
            candidate_pack_remove_quality_profile_sources(item)
    elif isinstance(value, list):
        for item in value:
            candidate_pack_remove_quality_profile_sources(item)


CANDIDATE_PACK_CONCEPT_STOPWORDS = {
    "a",
    "an",
    "and",
    "as",
    "at",
    "by",
    "for",
    "from",
    "in",
    "into",
    "is",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
    "without",
    "augmentation",
    "candidate",
    "entry",
    "label",
    "sampler",
    "score",
    "selected",
    "slot",
    "source",
    "terms",
}


def candidate_pack_concept_terms(
    values: Sequence[Any],
    *,
    salt: str,
    limit: int = 20,
) -> List[str]:
    """Reduce copyable candidate prose to an unordered vocabulary.

    The public pack does not expose a source sentence that can be pasted into
    a prompt.  Technical terms and semantic cues remain available, but their
    source order is destroyed so the composer must decide how they relate.
    """

    tokens: List[str] = []

    def visit(value: Any) -> None:
        if isinstance(value, str):
            tokens.extend(
                re.findall(
                    r"[A-Za-z0-9]+(?:[./'’\-][A-Za-z0-9]+)*|[가-힣]+|[ぁ-んァ-ヶ一-龠々]+",
                    value,
                )
            )
        elif isinstance(value, (list, tuple, set)):
            for item in value:
                visit(item)

    for value in values:
        visit(value)
    unique: Dict[str, str] = {}
    for token in tokens:
        normalized = token.strip().lower()
        if not normalized or normalized in CANDIDATE_PACK_CONCEPT_STOPWORDS:
            continue
        unique.setdefault(normalized, normalized if token.isascii() else token.strip())
    ordered = sorted(
        unique.values(),
        key=lambda token: hashlib.sha256(
            f"authorial-concept-term|{salt}|{token.lower()}".encode("utf-8")
        ).hexdigest(),
    )
    return ordered[: max(1, limit)]


def candidate_pack_project_candidate(candidate: JsonDict, *, salt: str) -> None:
    values: List[Any] = [
        candidate.pop("label_en", None),
        candidate.pop("label_ko", None),
        candidate.pop("terms", None),
        candidate.get("entry_id"),
        candidate.get("candidate_id"),
        candidate.get("tags"),
    ]
    concept_terms = candidate_pack_concept_terms(values, salt=salt)
    if concept_terms:
        candidate["concept_terms"] = concept_terms
    candidate["content_form"] = "unordered_inspiration_terms"
    for key in ("selected_by_sampler", "probability", "weight", "score", "scores"):
        candidate.pop(key, None)


def candidate_pack_project_candidate_surfaces(projected: JsonDict) -> None:
    slots = projected.get("slots") if isinstance(projected.get("slots"), dict) else {}
    for slot_payload in slots.values():
        if not isinstance(slot_payload, dict):
            continue
        for key in ("selected", "weight_floor", "score_window", "selected_filter"):
            slot_payload.pop(key, None)
        slot_payload["candidate_order"] = "seed_shuffled_non_preferential"
        for candidate in slot_payload.get("candidates") or []:
            if isinstance(candidate, dict):
                candidate_pack_project_candidate(
                    candidate, salt=str(candidate.get("id") or slot_payload.get("slot") or "slot")
                )
    proposition = (
        projected.get("visual_proposition")
        if isinstance(projected.get("visual_proposition"), dict)
        else {}
    )
    for key in ("core_candidates", "tension_candidates"):
        for candidate in proposition.get(key) or []:
            if isinstance(candidate, dict):
                candidate_pack_project_candidate(candidate, salt=str(candidate.get("id") or key))
    adult = projected.get("adult_appeal") or {}
    axes = adult.get("axes") if isinstance(adult.get("axes"), dict) else {}
    for axis in axes.values():
        if not isinstance(axis, dict):
            continue
        for candidate in axis.get("candidate_inventory") or []:
            if isinstance(candidate, dict):
                candidate_pack_project_candidate(
                    candidate, salt=str(candidate.get("id") or "adult-axis")
                )
    exploration = (
        projected.get("creative_exploration")
        if isinstance(projected.get("creative_exploration"), dict)
        else {}
    )
    for contrast in exploration.get("contrast_candidates") or []:
        if not isinstance(contrast, dict):
            continue
        contrast.pop("replaces_candidate_id", None)
        contrast.pop("relevance_rank", None)
    if exploration:
        previous_guidance = (
            exploration.get("composition_guidance")
            if isinstance(exploration.get("composition_guidance"), dict)
            else {}
        )
        exploration["composition_guidance"] = {
            "candidate_use": "optional_authorial_inspiration",
            "use_at_most": int(previous_guidance.get("replace_at_most", 2) or 2),
            "require_no_conflicts": True,
            "no_sampler_default_is_exposed": True,
        }


def candidate_pack_project_quality_surfaces(projected: JsonDict) -> None:
    """Project core-grounded quality choices into optional authorial pools.

    The frozen scene provides the context for relevant craft
    material.  The public pack must not reveal which axes, strategy, or refinement won that
    internal ranking, because those fields become a second prompt template.
    """

    integration = (
        projected.get("photographic_integration")
        if isinstance(projected.get("photographic_integration"), dict)
        else {}
    )
    suggested = integration.pop("suggested_phrases", None)
    if isinstance(suggested, dict):
        integration["suggested_concepts"] = {
            str(category): candidate_pack_concept_terms(
                phrases if isinstance(phrases, list) else [phrases],
                salt=f"integration:{category}",
            )
            for category, phrases in suggested.items()
        }
    category_terms = (
        integration.get("category_terms")
        if isinstance(integration.get("category_terms"), dict)
        else {}
    )
    category_ids = sorted(
        {
            *[str(item) for item in integration.get("required_categories") or [] if str(item)],
            *[str(item) for item in category_terms if str(item)],
        }
    )
    integration["category_candidates"] = [
        {
            "id": f"integration:{category}",
            "category": category,
            "concept_terms": candidate_pack_concept_terms(
                [category, category_terms.get(category)],
                salt=f"integration-category:{category}",
                limit=40,
            ),
            "content_form": "unordered_inspiration_terms",
        }
        for category in category_ids
    ]
    for key in (
        "active_axes",
        "quality_profile",
        "matched_facets",
        "matched_terms",
        "required_categories",
        "minimum_category_hits",
        "profile_id",
        "principles",
        "suggested_concepts",
        "source",
    ):
        integration.pop(key, None)
    integration.update(
        {
            "selection_mode": "agent_authored_non_preferential",
            "candidate_order": "seed_shuffled_non_preferential",
            "minimum_selected_categories": min(2, len(category_ids)),
            "maximum_selected_categories": min(3, len(category_ids)),
            "sampler_axis_selection_exposed": False,
        }
    )

    proposition = (
        projected.get("visual_proposition")
        if isinstance(projected.get("visual_proposition"), dict)
        else {}
    )
    category_terms = (
        proposition.get("category_terms")
        if isinstance(proposition.get("category_terms"), dict)
        else {}
    )
    proposition["category_terms"] = {
        str(category): candidate_pack_concept_terms(
            terms if isinstance(terms, list) else [terms],
            salt=f"proposition:{category}",
            limit=40,
        )
        for category, terms in category_terms.items()
    }
    for key in (
        "quality_profile",
        "subject_class",
        "subject_classes",
        "register",
        "minimum_hits",
        "principles",
        "source",
    ):
        proposition.pop(key, None)
    proposition.update(
        {
            "selection_mode": "agent_authored_non_preferential",
            "candidate_order": "seed_shuffled_non_preferential",
            "sampler_proposition_selection_exposed": False,
        }
    )

    craft = (
        projected.get("photographic_craft")
        if isinstance(projected.get("photographic_craft"), dict)
        else {}
    )
    dimension_candidates: List[JsonDict] = []
    for dimension in craft.get("active_dimensions") or []:
        if not isinstance(dimension, dict):
            continue
        dimension_id = str(dimension.get("id") or "").strip()
        if not dimension_id:
            continue
        dimension_candidates.append(
            {
                "id": f"craft:{dimension_id}",
                "dimension": dimension_id,
                "concept_terms": candidate_pack_concept_terms(
                    [
                        dimension_id,
                        dimension.get("label"),
                        dimension.get("baseline_principle"),
                        dimension.get("guidance_en"),
                        dimension.get("guidance_ko"),
                        dimension.get("audit_terms"),
                    ],
                    salt=f"craft-dimension:{dimension_id}",
                    limit=40,
                ),
                "content_form": "unordered_inspiration_terms",
            }
        )
    guidance_values = [
        craft.pop("prompt_guidance_en", None),
        craft.pop("prompt_guidance_ko", None),
    ]
    # The popped prompt guidance came from the private top-ranked strategy.
    # Its concepts are already represented inside the unordered dimension
    # candidates; publishing a separate summary would reveal the winner again.
    for key in (
        "active_dimensions",
        "quality_profile",
        "matched_facets",
        "top_strategy",
        "strategy_variants",
        "prompt_dimension_ids",
        "audit_terms",
        "selection_mode",
        "source",
    ):
        craft.pop(key, None)
    craft.update(
        {
            "dimension_candidates": dimension_candidates,
            "selection_mode": "agent_authored_optional",
            "candidate_order": "seed_shuffled_non_preferential",
            "minimum_selected_dimensions": 0,
            "maximum_selected_dimensions": min(2, len(dimension_candidates)),
            "sampler_strategy_selection_exposed": False,
        }
    )

    final_touch = (
        projected.get("artistic_final_touch")
        if isinstance(projected.get("artistic_final_touch"), dict)
        else {}
    )
    final_sentence = final_touch.pop("final_sentence_en", None)
    final_touch_terms = candidate_pack_concept_terms(
        [final_sentence, final_touch.get("audit_terms")],
        salt="artistic-final-touch",
    )
    if final_touch_terms:
        final_touch["concept_terms"] = final_touch_terms
    for key in ("audit_terms", "profile_id", "source"):
        final_touch.pop(key, None)
    if final_touch.get("enabled"):
        final_touch.update(
            {
                "optional": True,
                "selection_mode": "agent_decides",
                "sampler_surface_sentence_exposed": False,
            }
        )


def candidate_pack_project_adult_requirements(projected: JsonDict) -> None:
    adult = projected.get('adult_appeal') or {}
    requirements = adult.get('composition_requirements') if isinstance(adult.get('composition_requirements'), dict) else {}
    if requirements:
        requirements.pop('one_accepted_detail_per_active_axis', None)
        requirements['authorial_axis_interpretation_per_active_axis'] = True
        requirements['candidate_adoption_per_active_axis'] = 'optional'


def candidate_pack_project_provenance(projected: JsonDict) -> None:
    """Publish only the allowed core-derived provenance."""

    provenance = (
        projected.get("provenance")
        if isinstance(projected.get("provenance"), dict)
        else {}
    )
    allowed_fields = (
        "generator_version",
        "seed",
        "batch_index",
        "selection_mode",
        "requested_selection_mode",
        "tags_hash",
        "concept_lock",
        "additional_requirements",
        "reference_edit_mode",
        "likeness_mode",
        "likeness_references",
        "user_mandatory_intents",
        "requested_scene_function",
        "safety",
    )
    projected["provenance"] = {
        **{
            key: copy.deepcopy(provenance.get(key))
            for key in allowed_fields
            if key in provenance
        },
        "private_routing_exposed": False,
        "omitted_private_fields": [
            "argv",
            "sample_prompt_id",
            "concept_gate_results",
            "concept_scene_variants",
            "character_response",
            "adult_appeal",
        ],
    }


def candidate_pack_project_quality_profile(projected: JsonDict) -> None:
    """Expose only request-critical subject kind, not a sampled style profile."""

    profile = (
        projected.get("quality_profile")
        if isinstance(projected.get("quality_profile"), dict)
        else {}
    )
    facets = profile.get("facets") if isinstance(profile.get("facets"), dict) else {}
    projected["quality_profile"] = {
        "profile_id": "authorial",
        "facets": {
            "subject_kind": normalize_list(facets.get("subject_kind")),
        },
        "selection_mode": "agent_authored",
        "source_profile_exposed": False,
    }


def candidate_pack_shuffle(items: List[Any], *, seed: str, scope: str) -> None:
    items.sort(
        key=lambda item: hashlib.sha256(
            f"authorial-order|{seed}|{scope}|{json.dumps(item, ensure_ascii=False, sort_keys=True, separators=(',', ':'))}".encode(
                "utf-8"
            )
        ).hexdigest()
    )


def candidate_pack_remove_selection_answer_keys(value: Any) -> None:
    if isinstance(value, dict):
        value.pop("covered_by", None)
        for item in value.values():
            candidate_pack_remove_selection_answer_keys(item)
    elif isinstance(value, list):
        for item in value:
            candidate_pack_remove_selection_answer_keys(item)


def candidate_pack_shuffle_candidate_surfaces(projected: JsonDict, *, seed: str) -> None:
    slots = projected.get('slots') if isinstance(projected.get('slots'), dict) else {}
    for slot, payload in slots.items():
        if not isinstance(payload, dict) or not isinstance(payload.get('candidates'), list):
            continue
        candidate_pack_shuffle(payload['candidates'], seed=seed, scope=f'slot:{slot}')
    proposition = projected.get('visual_proposition') if isinstance(projected.get('visual_proposition'), dict) else {}
    for key in ('core_candidates', 'tension_candidates'):
        if isinstance(proposition.get(key), list):
            candidate_pack_shuffle(proposition[key], seed=seed, scope=f'proposition:{key}')
    visual_concepts = projected.get('visual_concept_candidates') if isinstance(projected.get('visual_concept_candidates'), dict) else {}
    visual_candidates = visual_concepts.get('candidates') if isinstance(visual_concepts.get('candidates'), list) else []
    for candidate in visual_candidates:
        if isinstance(candidate, dict) and isinstance(candidate.get('concept_terms'), list):
            candidate_pack_shuffle(candidate['concept_terms'], seed=seed, scope=f"visual-concept-terms:{candidate.get('id') or ''}")
    candidate_pack_shuffle(visual_candidates, seed=seed, scope='visual-concepts')
    integration = projected.get('photographic_integration') if isinstance(projected.get('photographic_integration'), dict) else {}
    if isinstance(integration.get('category_candidates'), list):
        candidate_pack_shuffle(integration['category_candidates'], seed=seed, scope='photographic-integration')
    craft = projected.get('photographic_craft') if isinstance(projected.get('photographic_craft'), dict) else {}
    if isinstance(craft.get('dimension_candidates'), list):
        candidate_pack_shuffle(craft['dimension_candidates'], seed=seed, scope='photographic-craft')
    adult = projected.get('adult_appeal') or {}
    axes = adult.get('axes') if isinstance(adult.get('axes'), dict) else {}
    for axis_id, axis in axes.items():
        if isinstance(axis, dict) and isinstance(axis.get('candidate_inventory'), list):
            candidate_pack_shuffle(axis['candidate_inventory'], seed=seed, scope=f'adult-axis:{axis_id}')


def candidate_pack_prepare_authorial_surfaces(projected: JsonDict) -> JsonDict:
    candidate_pack_project_candidate_surfaces(projected)
    candidate_pack_project_quality_surfaces(projected)
    candidate_pack_project_adult_requirements(projected)
    provenance = projected.get("provenance") if isinstance(projected.get("provenance"), dict) else {}
    variation_material = "|".join(
        [
            str(provenance.get("seed") or ""),
            str(provenance.get("batch_index") or 0),
        ]
    )
    variation_digest = hashlib.sha256(
        f"authorial-variation|{variation_material}".encode("utf-8")
    ).digest()
    variation_index = int.from_bytes(variation_digest[:8], "big") % len(
        CANDIDATE_PACK_AUTHORIAL_LENSES
    )
    candidate_pack_remove_selection_answer_keys(projected)
    candidate_pack_project_provenance(projected)
    candidate_pack_project_quality_profile(projected)
    candidate_pack_shuffle_candidate_surfaces(projected, seed=variation_material)
    projected["authorial_composition"] = {
        "enabled": True,
        "contract_version": CANDIDATE_PACK_AUTHORIAL_COMPOSITION_VERSION,
        "candidate_content_form": "unordered_inspiration_terms",
        "candidate_order": "seed_shuffled_non_preferential",
        "variation_lens": CANDIDATE_PACK_AUTHORIAL_LENSES[variation_index],
        "policy": {
            "agent_is_final_author": True,
            "select_reinterpret_or_reject_by_artistic_judgment": True,
            "candidate_sentence_copying_forbidden": True,
            "technical_or_identity_terms_may_be_used_selectively": True,
            "candidate_pack_must_not_supply_final_prompt_prose": True,
            "all_advisory_candidates_may_be_rejected": True,
            "hard_identity_and_safety_constraints_remain_required": True,
            "chosen_candidate_interpretations_required": True,
        },
        "candidate_interpretation_contract": {
            "composed_field": "candidate_interpretations",
            "required_for_every_non_augmentation_chosen_candidate": True,
            "required_fields": [
                "candidate_id",
                "artistic_interpretation",
                "transformation",
                "prompt_evidence",
            ],
            "prompt_evidence_must_be_literal_and_newly_authored": True,
            "minimum_prompt_evidence_content_words": 4,
            "minimum_new_content_words_beyond_source_terms": 2,
            "source_term_only_evidence_forbidden": True,
            "augmentation_candidates_use_augmentation_brief": True,
        },

    }
    return projected


def candidate_pack_private_relevance(pack: JsonDict) -> JsonDict:
    """Capture private ranking evidence before applying the public privacy boundary."""
    rows: List[JsonDict] = []
    slots = pack.get('slots') if isinstance(pack.get('slots'), dict) else {}
    for payload in slots.values():
        if isinstance(payload, dict):
            rows.extend((candidate for candidate in payload.get('candidates') or [] if isinstance(candidate, dict)))
    adult = pack.get('adult_appeal') or {}
    axes = adult.get('axes') if isinstance(adult.get('axes'), dict) else {}
    for axis in axes.values():
        if isinstance(axis, dict):
            rows.extend((candidate for candidate in axis.get('candidate_inventory') or [] if isinstance(candidate, dict)))
    relevance: JsonDict = {}
    score_keys = ('relevance', 'effective_query', 'semantic_score', 'query', 'rule_context_score')
    for candidate in rows:
        candidate_id = str(candidate.get('id') or '')
        if not candidate_id:
            continue
        scores = candidate.get('scores') if isinstance(candidate.get('scores'), dict) else {}
        value: Optional[float] = None
        source = 'lexical_fallback'
        for key in score_keys:
            raw = scores.get(key)
            try:
                value = float(raw)
            except (TypeError, ValueError):
                continue
            source = key
            break
        relevance[candidate_id] = {'value': value, 'source': source}
    return relevance


def candidate_pack_relevance_tokens(text: str) -> Set[str]:
    return {
        token.lower()
        for token in re.findall(
            r"[A-Za-z0-9]+(?:['’\-][A-Za-z0-9]+)*|[가-힣]{2,}|[ぁ-んァ-ヶ一-龠々]{2,}",
            str(text or ""),
        )
        if token.lower() not in CANDIDATE_PACK_CONCEPT_STOPWORDS
        and len(token.strip()) >= 2
    }


def candidate_pack_creative_augmentation(
    projected: JsonDict,
    private_relevance: JsonDict,
) -> JsonDict:
    core = (
        projected.get("authorial_core")
        if isinstance(projected.get("authorial_core"), dict)
        else {}
    )
    provenance = (
        projected.get("provenance")
        if isinstance(projected.get("provenance"), dict)
        else {}
    )
    query_text, _ = authorial_core_retrieval_text(core)
    query_tokens = candidate_pack_relevance_tokens(query_text)
    exclusion_token_groups = [
        candidate_pack_relevance_tokens(str(item))
        for item in core.get("user_exclusions") or []
        if candidate_pack_relevance_tokens(str(item))
    ]
    excluded_identity_slots = {
        "subject",
        "appearance_type",
        "age",
        "species",
        "species_morphology",
        "face",
        "body_type",
    }
    rows: List[JsonDict] = []
    excluded_by_user_filter: List[str] = []

    def add_candidate(candidate: Any, *, source_kind: str, axis: Optional[str] = None) -> None:
        if not isinstance(candidate, dict):
            return
        candidate_id = str(candidate.get("id") or "")
        slot = str(candidate.get("slot") or "")
        applicability = (
            candidate.get("applicability")
            if isinstance(candidate.get("applicability"), dict)
            else {"status": "eligible"}
        )
        if (
            not candidate_id
            or slot in excluded_identity_slots
            or applicability.get("status", "eligible") != "eligible"
        ):
            return
        concept_terms = [
            str(item)
            for item in candidate.get("concept_terms") or []
            if str(item).strip()
        ]
        candidate_tokens = candidate_pack_relevance_tokens(
            " ".join([candidate_id, slot, *concept_terms])
        )
        if any(group <= candidate_tokens for group in exclusion_token_groups):
            excluded_by_user_filter.append(candidate_id)
            return
        overlap = len(query_tokens & candidate_tokens)
        lexical = overlap / max(math.sqrt(max(len(query_tokens), 1) * max(len(candidate_tokens), 1)), 1.0)
        private = (
            private_relevance.get(candidate_id)
            if isinstance(private_relevance.get(candidate_id), dict)
            else {}
        )
        raw_value = private.get("value")
        try:
            raw_score = float(raw_value)
        except (TypeError, ValueError):
            raw_score = None
        if raw_score is None:
            relevance = lexical
            basis = "authorial_core_lexical_overlap"
        elif str(private.get("source") or "") == "rule_context_score":
            normalized_rule = max(0.0, raw_score) / (max(0.0, raw_score) + 3.0)
            relevance = (0.65 * normalized_rule) + (0.35 * lexical)
            basis = "rule_context_plus_authorial_core_overlap"
        else:
            normalized_semantic = max(0.0, min(1.0, (raw_score + 1.0) / 2.0))
            relevance = (0.75 * normalized_semantic) + (0.25 * lexical)
            basis = "semantic_score_plus_authorial_core_overlap"
        rows.append(
            {
                "id": candidate_id,
                "slot": slot or None,
                "axis": axis,
                "source_kind": source_kind,
                "concept_terms": concept_terms,
                "applicability": copy.deepcopy(applicability),
                **{key: copy.deepcopy(candidate[key])
                   for key in photo_contextual_appeal.PRESERVED_FIELDS if key in candidate},
                "conflicts_with": [
                    str(item)
                    for item in candidate.get("conflicts_with") or []
                    if str(item).strip()
                ],
                "_relevance": float(relevance),
                "_basis": basis,
            }
        )

    slots = (
        projected.get("slots")
        if isinstance(projected.get("slots"), dict)
        else {}
    )
    for payload in slots.values():
        if isinstance(payload, dict):
            for candidate in payload.get("candidates") or []:
                add_candidate(candidate, source_kind="slot")
    adult = (
        projected.get("adult_appeal")
        if isinstance(projected.get("adult_appeal"), dict)
        else {}
    )
    axes = adult.get("axes") if isinstance(adult.get("axes"), dict) else {}
    for axis_id, axis in axes.items():
        if not isinstance(axis, dict):
            continue
        for candidate in axis.get("candidate_inventory") or []:
            add_candidate(
                candidate,
                source_kind="adult_appeal",
                axis=str(axis_id),
            )

    deduped: Dict[str, JsonDict] = {}
    for row in rows:
        candidate_id = str(row.get("id") or "")
        prior = deduped.get(candidate_id)
        if prior is None or float(row.get("_relevance", 0.0)) > float(
            prior.get("_relevance", 0.0)
        ):
            deduped[candidate_id] = row
    ranked = sorted(
        deduped.values(),
        key=lambda row: (
            -float(row.get("_relevance", 0.0)),
            str(row.get("id") or ""),
        ),
    )
    if not ranked:
        return {
            "enabled": False,
            "contract_version": CREATIVE_AUGMENTATION_CONTRACT_VERSION,
            "reason": "no_advisory_candidates_after_hard_guards",
            "user_exclusion_filter": {
                "applied": bool(exclusion_token_groups),
                "excluded_candidate_count": len(set(excluded_by_user_filter)),
                "exclusions_used_as_positive_query": False,
            },
        }

    total = len(ranked)
    near_end = max(1, int(math.ceil(total * 0.34)))
    adjacent_end = max(near_end + 1, int(math.ceil(total * 0.67)))
    adjacent_end = min(adjacent_end, total)
    for index, row in enumerate(ranked):
        if index < near_end:
            row["_band"] = "near"
        elif index < adjacent_end:
            row["_band"] = "adjacent"
        else:
            row["_band"] = "lateral"

    creativity = candidate_pack_creativity_level(provenance)
    if creativity is None:
        creativity = CREATIVE_CONTROL_DEFAULTS["creativity"]
    if creativity <= 1:
        allowed_bands = ["near"]
        band_weights = {"near": 1.0}
        sample_limit = 5
    elif creativity < 3:
        allowed_bands = ["near", "adjacent"]
        band_weights = {"near": 0.68, "adjacent": 0.32}
        sample_limit = 6
    else:
        allowed_bands = ["near", "adjacent", "lateral"]
        band_weights = {"near": 0.46, "adjacent": 0.34, "lateral": 0.20}
        sample_limit = 7

    available: Dict[str, List[JsonDict]] = {
        band: [row for row in ranked if row.get("_band") == band]
        for band in ("near", "adjacent", "lateral")
    }
    seed_material = "|".join(
        [
            str(provenance.get("seed") or ""),
            str(core.get("canonical_sha256") or ""),
            "creative-augmentation-v1",
        ]
    )
    seed_value = int.from_bytes(
        hashlib.sha256(seed_material.encode("utf-8")).digest()[:8],
        "big",
    )
    rng = random.Random(seed_value)
    selected: List[JsonDict] = []

    def take_from_band(band: str) -> None:
        pool = available.get(band) or []
        if not pool:
            return
        weights = [
            0.1 + max(0.0, float(row.get("_relevance", 0.0)))
            for row in pool
        ]
        chosen = rng.choices(pool, weights=weights, k=1)[0]
        pool.remove(chosen)
        selected.append(chosen)

    if "adjacent" in allowed_bands:
        take_from_band("adjacent")
    if "lateral" in allowed_bands:
        take_from_band("lateral")
    while len(selected) < min(sample_limit, total):
        nonempty_bands = [
            band for band in allowed_bands if available.get(band)
        ]
        if not nonempty_bands:
            break
        band = rng.choices(
            nonempty_bands,
            weights=[band_weights[band_id] for band_id in nonempty_bands],
            k=1,
        )[0]
        take_from_band(band)
    rng.shuffle(selected)

    public_candidates: List[JsonDict] = []
    for row in selected:
        public_candidates.append(
            {
                key: copy.deepcopy(value)
                for key, value in row.items()
                if key not in {"_relevance", "_basis", "_band"}
            }
            | {
                "semantic_band": str(row.get("_band") or "near"),
                "content_form": "unordered_inspiration_terms",
            }
        )
    eligible_ids = sorted(deduped)
    eligible_pool_sha256 = hashlib.sha256(
        json.dumps(
            eligible_ids,
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    guard_material = {
        "safety": projected.get("safety"),
        "negative_en": projected.get("negative_en"),
        "species_family": projected.get("species_family"),
        "intent_constraints": ((projected.get("coverage") or {}).get("intent_constraints")),
    }
    guard_sha256 = hashlib.sha256(
        json.dumps(
            guard_material,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    return {
        "enabled": True,
        "contract_version": CREATIVE_AUGMENTATION_CONTRACT_VERSION,
        "source_authorial_core_sha256": str(core.get("canonical_sha256") or ""),
        "requested_creativity": creativity,
        "distance_policy": {
            "bands": ["near", "adjacent", "lateral"],
            "allowed_bands": allowed_bands,
            "selection": "seeded_weighted_sampling_without_replacement",
            "same_hard_eligible_pool_across_creativity": True,
            "hard_guards_relaxed_by_creativity": False,
            "relevance_basis": "authorial_core_query_with_semantic_score_when_available",
        },
        "hard_eligible_pool_sha256": eligible_pool_sha256,
        "hard_eligible_candidate_count": len(eligible_ids),
        "guard_invariant_sha256": guard_sha256,
        "user_exclusion_filter": {
            "applied": bool(exclusion_token_groups),
            "excluded_candidate_count": len(set(excluded_by_user_filter)),
            "exclusions_used_as_positive_query": False,
        },
        "candidate_order": "seed_shuffled_non_preferential",
        "candidates": public_candidates,
        "selection_contract": {
            "composed_field": "creative_augmentation_brief",
            "all_sampled_candidates_require_a_decision": True,
            "decision_states": ["transformed", "rejected"],
            "agent_may_reject_all": True,
            "maximum_transformed": 3,
            "candidate_copying_forbidden": True,
            "new_literal_prompt_evidence_required": True,
        },
    }


def candidate_pack_bind_authorial_core(
    projected: JsonDict, private_relevance: JsonDict
) -> JsonDict:
    original_provenance = copy.deepcopy(
        projected.get("provenance") if isinstance(projected.get("provenance"), dict) else {}
    )
    projected = candidate_pack_prepare_authorial_surfaces(projected)
    core = (
        projected.get("authorial_core")
        if isinstance(projected.get("authorial_core"), dict)
        else None
    )
    if core is None:
        raise ValueError("candidate pack is missing its pre-pack authorial core")
    _, retrieval_provenance = authorial_core_retrieval_text(core)
    public_provenance = (
        projected.get("provenance") if isinstance(projected.get("provenance"), dict) else {}
    )
    public_provenance.update(
        {
            "creativity": original_provenance.get("creativity", CREATIVE_CONTROL_DEFAULTS["creativity"]),
            "candidate_pool_creativity": original_provenance.get("candidate_pool_creativity"),
            "retrieval_query": retrieval_provenance,
        }
    )
    if "embodiment_preflight_required" in original_provenance:
        public_provenance["embodiment_preflight_required"] = original_provenance[
            "embodiment_preflight_required"
        ]
    if "creative_control_runtime" in original_provenance:
        public_provenance["creative_control_runtime"] = copy.deepcopy(
            original_provenance["creative_control_runtime"]
        )
    projected["provenance"] = public_provenance
    adult = projected.get("adult_appeal")
    if adult is not None:
        projected["adult_appeal"] = adult
    authorial = (
        projected.get("authorial_composition")
        if isinstance(projected.get("authorial_composition"), dict)
        else {}
    )
    authorial["prepack_authorial_core_bound"] = True
    authorial["governing_core_sha256"] = str(core.get("canonical_sha256") or "")
    authorial["baseline_prompt_precedes_candidate_pack"] = True
    authorial["prompt_budget"] = authorial_prompt_budget_contract()
    authorial["core_binding_contract"] = {
        "composed_field": "authorial_core_binding",
        "minimum_preserved_evidence_phrases": 0,
        "minimum_authorial_decisions": 0,
        "evidence_must_be_literal_in_baseline_and_final_prompt": True,
    }
    intent_lock = core.get("intent_lock") if isinstance(core.get("intent_lock"), dict) else {}
    if core.get("contract_version") in AUTHORIAL_CORE_MODERN_CONTRACT_VERSIONS:
        authorial["core_binding_contract"].update(
            {
                "source_intent_lock_sha256_required": True,
                "all_semantic_anchor_ids_required": True,
                "authorial_decisions_limited_to_open_dimensions": True,
            }
        )
        projected["intent_preservation"] = {
            "contract_version": INTENT_PRESERVATION_CONTRACT_VERSION,
            "source_authorial_core_sha256": str(core.get("canonical_sha256") or ""),
            "source_intent_lock_sha256": str(intent_lock.get("canonical_sha256") or ""),
            "priority_order": [
                "requesting_user_definition",
                "requesting_user_semantic_anchor",
                "requesting_user_modifier_or_exclusion",
                "agent_prepack_interpretation",
                "creative_augmentation",
            ],
            "required_anchor_ids": [
                str(item.get("anchor_id") or "")
                for item in intent_lock.get("semantic_anchors") or []
                if isinstance(item, dict) and str(item.get("anchor_id") or "")
            ],
            "locked_dimensions": copy.deepcopy(intent_lock.get("locked_dimensions") or []),
            "open_dimensions": copy.deepcopy(intent_lock.get("open_dimensions") or []),
            "material_change_action": "stop_and_rebuild_core_after_requester_input",
            "creative_change_boundary": "open_dimensions_only_and_subordinate",
        }
    projected["authorial_composition"] = authorial
    creative_augmentation = candidate_pack_creative_augmentation(projected, private_relevance)
    if core.get("contract_version") in AUTHORIAL_CORE_MODERN_CONTRACT_VERSIONS:
        creative_augmentation.setdefault("selection_contract", {})[
            "transformed_affected_dimensions_required"
        ] = True
        creative_augmentation["selection_contract"]["transformed_dimensions_must_be_open"] = True
    projected["creative_augmentation"] = creative_augmentation
    if isinstance((projected.get("adult_appeal") or {}).get("dimension_scope"), dict):
        creative_augmentation.setdefault("selection_contract", {})[
            "adult_appeal_scope_exception"
        ] = projected["adult_appeal"]["dimension_scope"]["contract_version"]
    return projected


def candidate_pack_compose_current(
    projected: JsonDict,
    private_relevance: JsonDict,
) -> JsonDict:
    """Compose the current typed core, optional candidates, and authorship policy."""

    core = (
        projected.get("authorial_core")
        if isinstance(projected.get("authorial_core"), dict)
        else {}
    )
    if core.get("contract_version") != AUTHORIAL_CORE_V3_CONTRACT_VERSION:
        raise ValueError("v6 candidate pack requires photo-authorial-core/v3")
    semantic_sources: Dict[str, JsonDict] = {}

    def capture_semantic_sources(value: Any) -> None:
        if isinstance(value, list):
            for item in value:
                capture_semantic_sources(item)
        elif isinstance(value, dict):
            candidate_id = str(value.get("id") or value.get("candidate_id") or "")
            source = value.pop("_v6_semantic_source", None)
            if source is None and candidate_id and value.get("label_en"):
                source = photo_candidate_semantics.semantic_source(value, str(value.get("slot") or ""))
                if source:
                    semantic_sources.setdefault(candidate_id, source)
            elif candidate_id and source:
                semantic_sources[candidate_id] = source
            for item in value.values():
                capture_semantic_sources(item)

    capture_semantic_sources(projected)
    projected = candidate_pack_bind_authorial_core(projected, private_relevance)
    photo_candidate_semantics.apply_public_semantics(projected, semantic_sources)
    intent_lock = core["intent_lock"]
    open_dimensions = copy.deepcopy(intent_lock["open_dimensions"])
    authorship_policy: JsonDict = {
        "contract_version": AUTHORIAL_AUTHORSHIP_POLICY_CONTRACT_VERSION,
        "source_authorial_core_sha256": str(core.get("canonical_sha256") or ""),
        "source_intent_lock_sha256": str(intent_lock.get("canonical_sha256") or ""),
        "allowed_dimensions": open_dimensions,
        "minimum_authorial_decisions": 0,
        "minimum_preserved_evidence_phrases": 0,
        "dimension_policy": "distinct_open_dimensions_only",
        "insufficient_freedom_policy": "do_not_invent_open_dimensions",
    }
    authorship_policy["canonical_sha256"] = canonical_json_sha256(authorship_policy)
    projected["authorial_composition"]["authorship_policy"] = authorship_policy
    projected["authorial_composition"]["core_binding_contract"].update(
        {
            "contract_version": AUTHORIAL_CORE_BINDING_CONTRACT_VERSION,
            "source_authorship_policy_sha256": authorship_policy["canonical_sha256"],
            "minimum_authorial_decisions": authorship_policy[
                "minimum_authorial_decisions"
            ],
            "minimum_preserved_evidence_phrases": authorship_policy[
                "minimum_preserved_evidence_phrases"
            ],
        }
    )
    provenance = (
        projected.get("provenance")
        if isinstance(projected.get("provenance"), dict)
        else {}
    )
    provenance.pop("character_response", None)
    projected["provenance"] = provenance
    return projected


def candidate_pack_project(pack: JsonDict, version: str = "v6") -> JsonDict:
    candidate_pack_contract_version(version)
    projected = copy.deepcopy(pack)
    private_relevance = projected.pop("_candidate_relevance", {})
    projected["contract_version"] = CANDIDATE_PACK_CONTRACT_V6
    candidate_pack_remove_quality_profile_sources(projected)
    for field in ("photographic_craft", "artistic_final_touch"):
        if isinstance(projected.get(field), dict):
            projected[field].pop("source", None)
    projected = candidate_pack_compose_current(projected, private_relevance)
    return candidate_pack_recompute_id(projected)


def candidate_pack_candidate_bundles(data: JsonDict, pack: JsonDict) -> JsonDict:
    """Admit self-contained optional bundles without exposing sampler choices.

    A bundle's internal dependencies may be satisfied by joint adoption. Any
    prerequisite requiring an unproven external context fails closed. The same
    calculation is run by the composition auditor from the frozen core and the
    original dictionary snapshot, so an eligibility assertion is not authority.
    """
    core = pack.get("authorial_core") or {}
    policy = (data.get("candidate_semantic_policy") or {}).get("joint_adoption") or {}
    if not policy:
        return photo_candidate_semantics.public_bundles(data, pack)
    query, _ = authorial_core_retrieval_text(core)
    query_tokens = candidate_pack_relevance_tokens(query)
    exclusions = [candidate_pack_relevance_tokens(value) for value in core.get("user_exclusions") or []]
    opened = set((core.get("intent_lock") or {}).get("open_dimensions") or [])
    constraints = {
        "subject_category": "generic", "domains": [],
        "adult_allowed": candidate_pack_visual_obligation_adult_context([{"text": query}], None),
        "intent_constraints": authorial_core_generation_constraints(core, creative_control_snapshot=pack.get("creative_controls")),
    }
    admissions: JsonDict = {}
    for bundle in data.get("candidate_bundles") or []:
        members = bundle["member_candidates"]
        dimensions = {dimension for member in members for dimension in member.get("affected_dimensions") or []}
        if (len(members) > policy["maximum_members_per_bundle"]
                or len({member["slot"] for member in members}) != len(members)
                or any(not member.get("affected_dimensions") for member in members)
                or not dimensions.issubset(opened)):
            continue
        if any(not property_effects_allowed(core.get("intent_lock") or {},
                                           member.get("affected_dimensions") or [],
                                           member.get("affected_properties", [])) for member in members):
            continue
        units = [unit for member in members for unit in member.get("concept_units") or []]
        tokens = candidate_pack_relevance_tokens(" ".join(units))
        if (len(tokens & query_tokens) < policy["minimum_shared_content_words"]
                or not any(len(candidate_pack_relevance_tokens(unit)) >= 2 and intent_alias_matches(query, unit) for unit in units)
                or any(exclusion and exclusion.issubset(tokens) for exclusion in exclusions)):
            continue
        picked = {member["slot"]: candidate_pack_slot_entry_by_id(data, member["slot"], member["entry_id"]) for member in members}
        if any(entry is None for entry in picked.values()):
            continue
        if any(
            slot_block_reason(data, slot, constraints)
            or entry_block_reason(entry, slot, constraints)
            or not compatible_with_facet_guards(entry, picked)
            or not compatible_with_slot_context(slot, entry, picked, data)
            for slot, entry in picked.items()
        ):
            continue
        admissions[bundle["id"]] = {
            "contract_version": "photo-candidate-joint-admission/v1",
            "context_policy": policy["context_policy"],
            "source_authorial_core_sha256": str(core.get("canonical_sha256") or ""),
            "source_intent_lock_sha256": str((core.get("intent_lock") or {}).get("canonical_sha256") or ""),
            "source_dictionary_sha256": dictionary_hash(data),
            "source_quality_policy_sha256": canonical_json_sha256(candidate_pack_quality_layers(data)),
            "all_member_guards_satisfied": True,
            "external_context_assumed": False,
        }
    return photo_candidate_semantics.public_bundles(data, pack, admissions)


def build_candidate_pack(
    result: JsonDict,
    data: JsonDict,
    candidate_pack_version: str = DEFAULT_CANDIDATE_PACK_VERSION,
) -> JsonDict:
    candidate_pack_contract_version(candidate_pack_version)
    trace = result.get("semantic_trace") if isinstance(result.get("semantic_trace"), dict) else {}
    provenance = result.get("provenance") if isinstance(result.get("provenance"), dict) else {}
    authorial_core = (
        provenance.get("authorial_core")
        if isinstance(provenance.get("authorial_core"), dict)
        else None
    )
    if (
        not isinstance(authorial_core, dict)
        or authorial_core.get("contract_version") != AUTHORIAL_CORE_V3_CONTRACT_VERSION
    ):
        raise ValueError("candidate pack requires a current v3 authorial core")
    if not isinstance(provenance.get("creative_controls"), dict) or not isinstance(
        provenance.get("embodiment_preflight"), dict
    ):
        raise ValueError("candidate pack requires bound creative controls and embodiment review")
    contract = (
        trace.get("generation_contract")
        if isinstance(trace.get("generation_contract"), dict)
        else {}
    )
    slots, core_retrieval, contract = retrieve_core_slots(data, authorial_core, provenance["creative_controls"])
    trace = {**trace, "generation_contract": contract}
    candidate_entries: Dict[str, tuple[str, Optional[str], JsonDict]] = {}
    for slot, payload in slots.items():
        for candidate in payload["candidates"]:
            entry = candidate_pack_slot_entry_by_id(data, slot, candidate["entry_id"])
            candidate_entries[candidate["id"]] = ("slot", slot, entry)
    adult_appeal = candidate_pack_contextual_adult_appeal(data, result, candidate_entries, authorial_core=authorial_core)
    conflicts = candidate_pack_conflicts(data, candidate_entries)
    candidate_pack_apply_conflicts(slots, conflicts)
    candidate_pack_apply_conflicts_to_candidates(candidate_pack_adult_candidates(adult_appeal), conflicts)
    candidate_blobs = candidate_pack_candidate_blobs(slots)
    mandatory_intents, uncovered_intents = candidate_pack_mandatory_intents(result, trace, candidate_blobs)
    intent_contract = candidate_pack_intent_contract(data, result, trace, candidate_blobs)
    quality_profile = candidate_pack_quality_profile(data, result, slots, mandatory_intents)
    creative_exploration = candidate_pack_creative_exploration(result, slots, candidate_entries)
    creative_direction = candidate_pack_creative_direction(result)
    character_response = compile_character_response_contract(
        authorial_core,
        data=data,
        semantic_index=(
            data.get(SEMANTIC_INDEX_DATA_KEY)
            if isinstance(data.get(SEMANTIC_INDEX_DATA_KEY), dict)
            else None
        ),
    )
    semantic_assertion_obligations = compile_semantic_assertion_obligations(authorial_core)
    render_repair = compile_render_repair_contract(authorial_core)
    response_context = character_response
    visual_profile_resolution = candidate_pack_resolve_visual_profiles(
        data, result, trace, response_context
    )
    visual_obligations = candidate_pack_visual_obligations(
        data, result, trace, response_context, visual_profile_resolution
    )
    visual_concept_candidates = candidate_pack_visual_concept_candidates(
        data, result, trace, response_context, visual_obligations, visual_profile_resolution
    )
    semantic_clarification = candidate_pack_semantic_clarification(
        data,
        result,
        trace,
        visual_obligations,
        visual_concept_candidates,
        visual_profile_resolution,
    )
    viewer_experience = candidate_pack_viewer_experience(result)
    intent_constraints = copy.deepcopy(contract.get("intent_constraints", {}))
    if isinstance(intent_constraints, dict):
        response_constraint = intent_constraints.get("character_response")
        if not (
            isinstance(response_constraint, dict)
            and (
                response_constraint.get("requested") is True
                or response_constraint.get("enabled") is True
            )
        ):
            intent_constraints.pop("character_response", None)
    pack: JsonDict = {
        "contract_version": "photo-candidate-pack/v6",
        "pack_id": "",
        "intent_contract": intent_contract,
        "mandatory_intents": mandatory_intents,
        "uncovered_intents": uncovered_intents,
        "slots": slots,
        "quality_profile": quality_profile,
        "photographic_integration": candidate_pack_photographic_integration(
            data, result, trace, slots, mandatory_intents, quality_profile
        ),
        "visual_proposition": candidate_pack_visual_proposition(
            data, result, trace, slots, mandatory_intents, quality_profile
        ),
        "photographic_craft": candidate_pack_photographic_craft(data, quality_profile),
        "artistic_final_touch": candidate_pack_artistic_final_touch(data, quality_profile),
        "safety": contract.get("safety")
        or {
            "mode": "automatic",
            "evaluation_requested": False,
            "status": "pass",
            "requires_user_approval": False,
            "items": [],
        },
        "coverage": {
            "mandatory_intent_count": len(mandatory_intents),
            "covered_mandatory_intent_count": len(mandatory_intents) - len(uncovered_intents),
            "uncovered_intent_count": len(uncovered_intents),
            "intent_constraints": intent_constraints,
            "axis_coverage": trace.get("axis_coverage", {}),
            "contract": {
                "must_cover_axes": contract.get("must_cover_axes", []),
                "covered_axes": contract.get("covered_axes", []),
                "coverage_gaps": contract.get("coverage_gaps", []),
            },
            "candidate_limits": {
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
            "selection_mode": provenance.get("selection_mode") or trace.get("selection_mode"),
            "requested_selection_mode": provenance.get("requested_selection_mode")
            or trace.get("requested_selection_mode"),
            "tags_hash": provenance.get("tags_hash") or trace.get("dictionary_hash"),
            "concept_lock": provenance.get("concept_lock", []),
            "additional_requirements": provenance.get("additional_requirements", []),
            "reference_edit_mode": provenance.get("reference_edit_mode", "off"),
            "likeness_mode": provenance.get("likeness_mode"),
            "likeness_references": provenance.get("likeness_references", []),
            "user_mandatory_intents": provenance.get("user_mandatory_intents", []),
            "requested_scene_function": provenance.get("requested_scene_function"),
            "safety": provenance.get("safety", contract.get("safety", {})),
            "argv": provenance.get("argv", []),
        },
    }
    if creative_exploration is not None:
        pack["creative_exploration"] = creative_exploration
    if isinstance(provenance.get("creative_controls"), dict):
        pack["creative_controls"] = copy.deepcopy(provenance["creative_controls"])
        pack["provenance"]["creative_control_runtime"] = copy.deepcopy(
            provenance["creative_control_runtime"]
        )
    if authorial_core is not None:
        pack["authorial_core"] = copy.deepcopy(authorial_core)
    if authorial_core is None:
        raise ValueError("v6 candidate pack requires a pre-pack authorial core")
    pack["provenance"]["creativity"] = provenance.get("creativity", CREATIVE_CONTROL_DEFAULTS["creativity"])
    pack["provenance"]["candidate_pool_creativity"] = provenance.get("candidate_pool_creativity")
    pack["provenance"]["retrieval_query"] = copy.deepcopy(provenance.get("retrieval_query", {}))
    if (
        isinstance(authorial_core, dict)
        and authorial_core.get("contract_version") in AUTHORIAL_CORE_MODERN_CONTRACT_VERSIONS
    ):
        negative_intent_guard = (
            result.get("negative_intent_guard")
            if isinstance(result.get("negative_intent_guard"), dict)
            else None
        )
        if negative_intent_guard is None:
            raise ValueError("modern v6 candidate pack requires the negative-intent guard")
        pack["negative_intent_guard"] = copy.deepcopy(negative_intent_guard)
    visual_intent = (
        provenance.get("visual_intent")
        if isinstance(provenance.get("visual_intent"), dict)
        else None
    )
    if visual_intent is not None:
        pack["visual_intent"] = copy.deepcopy(visual_intent)
    if visual_obligations is not None:
        pack["visual_obligations"] = visual_obligations
    if visual_concept_candidates is not None:
        pack["visual_concept_candidates"] = visual_concept_candidates
    if semantic_clarification is not None:
        pack["semantic_clarification"] = semantic_clarification
    if creative_direction is not None:
        pack["creative_direction"] = creative_direction
    if character_response is not None:
        pack["character_response"] = character_response
    if semantic_assertion_obligations is not None:
        pack["semantic_assertion_obligations"] = semantic_assertion_obligations
    if render_repair is not None:
        pack["render_repair"] = render_repair
    if "embodiment_preflight" in provenance:
        pack["embodiment_preflight"] = copy.deepcopy(provenance["embodiment_preflight"])
        pack["provenance"]["embodiment_preflight_required"] = True
        photo_embodiment.policy_from_pack({**pack, "contract_version": "photo-candidate-pack/v6"})
    if viewer_experience is not None:
        pack["viewer_experience"] = viewer_experience
    if adult_appeal is not None:
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
                    "intensity": int((adult_axes.get(axis_id) or {}).get('intensity', 0) or 0),
                    "active": bool((adult_axes.get(axis_id) or {}).get("active")),
                }
                for axis_id in CANDIDATE_PACK_ADULT_APPEAL_AXES
            },
            "blend": {"emphasis": ((adult_appeal or {}).get("blend") or {}).get("emphasis")},
        }
        pack["adult_appeal"] = adult_appeal
    pack["core_retrieval"] = core_retrieval
    pack["_candidate_relevance"] = candidate_pack_private_relevance(pack)
    for slot, payload in (pack.get("slots") or {}).items():
        for candidate in payload.get("candidates") or []:
            entry = candidate_pack_slot_entry_by_id(data, slot, str(candidate.get('entry_id') or ''))
            if entry:
                candidate["_v6_semantic_source"] = photo_candidate_semantics.semantic_source(
                    entry, slot, data.get("candidate_semantic_policy")
                )
                source = candidate["_v6_semantic_source"]
                if not property_effects_allowed(
                    authorial_core.get("intent_lock") or {}, source.get("affected_dimensions") or [],
                    source.get("affected_properties", [])
                ):
                    candidate["applicability"] = {
                        "status": "ineligible", "source": "authored_property_scope",
                        "reason": "effect overlaps a protected requester property",
                    }
    pack["candidate_bundles"] = candidate_pack_candidate_bundles(data, pack)
    candidate_pack_recompute_id(pack)
    return candidate_pack_project(pack, candidate_pack_version)


def semantic_description_for_entry(entry: Entry) -> str:
    if entry.get("embedding_text"):
        return " ".join(normalize_list(entry.get("embedding_text")))
    if entry.get("en"):
        return str(entry["en"])
    if entry.get("ko"):
        return str(entry["ko"])
    return "photo prompt concept"


def semantic_caption_for_entry(entry: Entry, slot: Optional[str] = None) -> str:
    description = semantic_description_for_entry(entry)
    if slot:
        template = SEMANTIC_SLOT_CAPTION_TEMPLATES.get(
            slot,
            "Photo prompt slot concept for {slot}: {description}. It should retrieve visually compatible photographic details for this slot.",
        )
        return template.format(slot=slot, description=description)
    raise ValueError("slot captions require an authored slot name")


def dictionary_hash(data: JsonDict) -> str:
    material = {
        "version": data.get("version"),
        "slots": data.get("slots", {}),
        "facet_vocab": data.get("facet_vocab", {}),
        "character_mechanism_graph": data.get("character_mechanism_graph", {}),
        "candidate_bundles": data.get("candidate_bundles", []),
        "candidate_semantic_policy": data.get("candidate_semantic_policy", {}),
    }
    payload = json.dumps(material, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def semantic_relation_texts(entry: Entry) -> List[str]:
    texts: List[str] = []
    for relation in entry.get("relations") or []:
        if not isinstance(relation, dict):
            continue
        subject = clean_spaces(str(relation.get("subject") or ""))
        relation_type = clean_spaces(str(relation.get("type") or "").replace("_", " "))
        target = clean_spaces(str(relation.get("object") or ""))
        if subject and relation_type and target:
            texts.append(f"{subject} {relation_type} {target}")
    for relation in entry.get("required_relations") or []:
        if not isinstance(relation, dict):
            continue
        operator = clean_spaces(str(relation.get("operator") or ""))
        if operator == "contrasts":
            texts.append(
                f"{relation.get('left')} contrasts with {relation.get('right')}"
            )
        elif operator == "same_target":
            texts.append(
                "same relationship target for "
                + ", ".join(normalize_list(relation.get("members")))
            )
        elif operator == "temporal_order":
            texts.append(
                f"{relation.get('first')} precedes or coexists before {relation.get('then')}"
            )
        else:
            texts.append(" ".join(str(value) for value in relation.values()))
    return [clean_spaces(value) for value in texts if clean_spaces(value)]


def semantic_text_for_entry(
    entry: Entry,
    slot: Optional[str] = None,
    *,
    kind: Optional[str] = None,
) -> str:
    """Build embedding input from public visual-language fields only.

    Stable IDs, tags, kinds, facets, routing metadata, and validation notes are
    control-plane data. Including them makes retrieval learn how an entry was
    developed instead of what should be visible in the photograph.
    """
    if kind == "character_response_concept":
        parts: List[str] = [
            "Character-response concept meaning: "
            + clean_spaces(str(entry.get("definition") or ""))
        ]
    elif kind == "character_response_confounder":
        parts = [
            "Character-response confounder meaning: "
            + clean_spaces(str(entry.get("definition") or ""))
        ]
    elif kind == "character_mechanism_node":
        parts = [
            "Optional character-response mechanism: "
            + clean_spaces(str(entry.get("definition") or ""))
        ]
    else:
        parts = [semantic_caption_for_entry(entry, slot)]
    for key in ("en", "ko", "ja"):
        if entry.get(key):
            parts.append(f"{key} label: {entry[key]}.")
    for key in ("aliases", "keywords", "terms"):
        values = normalize_list(entry.get(key))
        if values:
            parts.append(f"{key}: {', '.join(values)}.")
    if slot:
        parts.append(f"slot: {slot}.")
    concept_units = normalize_list(entry.get("concept_units"))
    if concept_units:
        parts.append("visual concepts: " + "; ".join(concept_units) + ".")
    relations = semantic_relation_texts(entry)
    if relations:
        parts.append("semantic relations: " + "; ".join(relations) + ".")
    manifestations = normalize_list(entry.get("manifestations"))
    if manifestations:
        parts.append("optional manifestations: " + "; ".join(manifestations) + ".")
    paraphrases = normalize_list(entry.get("paraphrases"))
    if paraphrases:
        parts.append("paraphrases: " + "; ".join(paraphrases) + ".")
    return " ".join(parts)


def semantic_bm25f_fields_for_entry(
    entry: Entry,
    slot: Optional[str] = None,
    *,
    kind: Optional[str] = None,
) -> JsonDict:
    """Project public visual-language fields into one generic BM25F document."""

    return {
        "aliases": [
            clean_spaces(str(value))
            for value in normalize_list(entry.get("aliases"))
            if clean_spaces(str(value))
        ],
        "labels": [
            clean_spaces(str(entry.get(key) or ""))
            for key in ("en", "ko", "ja")
            if clean_spaces(str(entry.get(key) or ""))
        ],
        "semantic_caption": [
            semantic_caption_for_entry(entry, slot)
            if kind
            not in {
                "character_response_concept",
                "character_response_confounder",
                "character_mechanism_node",
            }
            else (
                "Character-response concept meaning"
                if kind == "character_response_concept"
                else (
                    "Character-response confounder meaning"
                    if kind == "character_response_confounder"
                    else "Optional character-response mechanism"
                )
            )
        ],
        "definition": [clean_spaces(str(entry.get("definition") or ""))]
        if clean_spaces(str(entry.get("definition") or ""))
        else [],
        "paraphrases": [
            clean_spaces(str(value))
            for value in normalize_list(entry.get("paraphrases"))
            if clean_spaces(str(value))
        ],
        "semantic_relations": semantic_relation_texts(entry),
        "concept_units": [
            clean_spaces(str(value))
            for value in normalize_list(entry.get("concept_units"))
            if clean_spaces(str(value))
        ],
        "manifestations": [
            clean_spaces(str(value))
            for value in normalize_list(entry.get("manifestations"))
            if clean_spaces(str(value))
        ],
        "keywords": [
            clean_spaces(str(value))
            for key in ("keywords", "terms", "embedding_text")
            for value in normalize_list(entry.get(key))
            if clean_spaces(str(value))
        ],
        "slot_context": [
            clean_spaces(str(slot or kind or ""))
        ]
        if slot
        or kind
        in {
            "character_response_concept",
            "character_response_confounder",
            "character_mechanism_node",
        }
        else [],
    }


def semantic_bm25f_documents(data: JsonDict) -> Dict[str, JsonDict]:
    return {
        key: semantic_bm25f_fields_for_entry(entry, slot, kind=kind)
        for key, kind, entry, slot in iter_semantic_entries(data)
    }


def build_semantic_bm25f_payload(data: JsonDict) -> JsonDict:
    documents = semantic_bm25f_documents(data)
    payload = build_bm25f_index(
        documents,
        policy=SEMANTIC_BM25F_POLICY,
        lexicon=_bm25f_lexicon_from_documents(
            documents, ("aliases", "labels", "paraphrases")
        ),
    )
    payload["policy_version"] = SEMANTIC_BM25F_POLICY_VERSION
    payload["policy_sha256"] = canonical_json_sha256(SEMANTIC_BM25F_POLICY)
    return payload


def semantic_bm25f_payload_from_index(
    index: JsonDict, *, copy_values: bool = True
) -> JsonDict:
    """Project BM25F fields; allow read-only validation to avoid corpus copies."""
    metadata = (
        (copy.deepcopy(index["bm25f"]) if copy_values else dict(index["bm25f"]))
        if isinstance(index.get("bm25f"), dict)
        else {}
    )
    metadata["documents"] = {
        str(key): (
            copy.deepcopy(entry.get("bm25f_document") or {})
            if copy_values
            else entry.get("bm25f_document") or {}
        )
        for key, entry in (index.get("entries") or {}).items()
        if isinstance(entry, dict)
    }
    return metadata


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


@functools.lru_cache(maxsize=4)
def cached_gemini_client(api_key: str) -> Any:
    """Reuse the SDK transport while keeping each embedding request isolated."""
    from google import genai

    return genai.Client(api_key=api_key)


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
        from google.genai import types
    except ImportError as exc:
        raise RuntimeError(
            "google-genai is required for Gemini semantic embeddings. "
            "Install it with `python3 -m pip install -r requirements.txt`."
        ) from exc

    client = cached_gemini_client(key)
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
    if kind == "character_response_concept":
        return f"character_response_concept:{entry.get('id')}"
    if kind == "character_response_confounder":
        return (
            "character_response_confounder:"
            f"{entry.get('concept_profile_id')}:{entry.get('id')}"
        )
    if kind == "character_mechanism_node":
        return f"character_mechanism_node:{entry.get('id')}"
    return f"slot:{slot}:{entry.get('id')}"


def iter_semantic_entries(data: JsonDict) -> List[tuple[str, str, Entry, Optional[str]]]:
    entries: List[tuple[str, str, Entry, Optional[str]]] = []
    for slot, slot_entries in data.get("slots", {}).items():
        for entry in slot_entries:
            key = semantic_entry_key("slot", entry, slot)
            entries.append((key, "slot", entry, slot))
    graph = data.get("character_mechanism_graph")
    if isinstance(graph, dict):
        nodes_by_id = {
            str(node.get("id") or ""): node
            for node in graph.get("runtime_nodes") or []
            if isinstance(node, dict) and str(node.get("id") or "")
        }
        referenced_runtime_ids: Set[str] = set()
        for raw_profile in graph.get("concept_profiles") or []:
            if not isinstance(raw_profile, dict):
                continue
            profile = copy.deepcopy(raw_profile)
            runtime_ids = normalize_list(profile.get("optional_runtime_node_ids"))
            referenced_runtime_ids.update(runtime_ids)
            profile["manifestations"] = [
                clean_spaces(str((nodes_by_id.get(runtime_id) or {}).get("definition") or ""))
                for runtime_id in runtime_ids
                if clean_spaces(
                    str((nodes_by_id.get(runtime_id) or {}).get("definition") or "")
                )
            ]
            key = semantic_entry_key("character_response_concept", profile)
            entries.append((key, "character_response_concept", profile, None))
            for raw_confounder in profile.get("confounders") or []:
                if not isinstance(raw_confounder, dict):
                    continue
                confounder = copy.deepcopy(raw_confounder)
                confounder["concept_profile_id"] = str(profile.get("id") or "")
                key = semantic_entry_key(
                    "character_response_confounder",
                    confounder,
                )
                entries.append(
                    (key, "character_response_confounder", confounder, None)
                )
        for runtime_id in sorted(referenced_runtime_ids):
            node = nodes_by_id.get(runtime_id)
            if node is None:
                continue
            key = semantic_entry_key("character_mechanism_node", node)
            entries.append((key, "character_mechanism_node", node, None))
    return entries


SEMANTIC_INDEX_SHARDED_FORMAT = "sharded-json-v1"


def load_semantic_index_payload(path: str | Path) -> JsonDict:
    """Load the sharded final index with its exact logical entry order.

    Sharding is a storage concern only. Callers continue to receive the same
    materialized ``entries`` mapping used by scoring, tie-breaking, and audit
    code, so a storage migration cannot alter retrieval behavior.
    """
    index_path = Path(path)
    payload = json.loads(index_path.read_text(encoding="utf-8"))
    storage = payload.get("storage") if isinstance(payload.get("storage"), dict) else {}
    if storage.get("format") != SEMANTIC_INDEX_SHARDED_FORMAT:
        raise ValueError("final semantic index must use the sharded manifest format")

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
    *,
    require_bm25f: bool = True,
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
    if not isinstance(payload.get("bm25f"), dict):
        if require_bm25f:
            raise ValueError(
                "Semantic index has no BM25F metadata. Regenerate it with "
                "build_semantic_index.py."
            )
        return
    bm25f_payload = semantic_bm25f_payload_from_index(payload, copy_values=False)
    if bm25f_payload.get("policy_version") != SEMANTIC_BM25F_POLICY_VERSION:
        raise ValueError("Semantic index BM25F policy_version is stale")
    if bm25f_payload.get("policy_sha256") != canonical_json_sha256(
        SEMANTIC_BM25F_POLICY
    ):
        raise ValueError("Semantic index BM25F policy hash is stale")
    bm25f_material = {
        key: value
        for key, value in bm25f_payload.items()
        if key not in {"policy_version", "policy_sha256"}
    }
    documents = semantic_bm25f_documents(data)
    validate_bm25f_index(
        bm25f_material,
        documents,
        policy=SEMANTIC_BM25F_POLICY,
        lexicon=_bm25f_lexicon_from_documents(
            documents, ("aliases", "labels", "paraphrases")
        ),
    )


def facet_tokens(entry: Entry, *, include_control: bool = True) -> Set[str]:
    tokens: Set[str] = set()
    facets = entry.get("facets", {}) or {}
    if not isinstance(facets, dict):
        return tokens
    for key, values in facets.items():
        if not include_control and str(key) in CONTROL_ONLY_FACET_KEYS:
            continue
        for value in normalize_list(values):
            tokens.add(f"{key}:{value}")
    return tokens


def guard_values(entry: Entry, key: str) -> Set[str]:
    guards = entry.get("hard_guards", {}) or {}
    if not isinstance(guards, dict):
        return set()
    return set(normalize_list(guards.get(key)))


def compatible_with_facet_guards(item: Entry, picked: Dict[str, Entry]) -> bool:
    context: Set[str] = set()
    for entry in picked.values():
        context |= facet_tokens(entry)
    item_facets = facet_tokens(item)

    requires = guard_values(item, "requires_facets")
    if requires and not requires.issubset(context | item_facets):
        return False

    excludes = guard_values(item, "exclude_facets")
    if excludes & context:
        return False

    return True


CREATIVITY_SAMPLING_STRENGTHS = (0.0, 0.25, 0.5, 1.0)


def creativity_sampling_strength(level: int) -> float:
    """Convert an authored 0..3 level to private numeric sampling coefficients."""
    if type(level) is not int or level not in range(4):
        raise ValueError("creativity must be an integer in 0..3")
    return CREATIVITY_SAMPLING_STRENGTHS[level]


def coherence_rules_from_source(source: JsonDict) -> JsonDict:
    return source.get("coherence_rules", {}) or {}


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


# -----------------------------------------------------------------------------
# Priority-biased slot selection
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Compatibility and forced choices
# -----------------------------------------------------------------------------


def quality_layer_primary_context_requirement_sources(data: JsonDict, slot: str, item: Entry) -> List[JsonDict]:
    sources: List[JsonDict] = []
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
        values = sorted({str(value) for value in normalize_list(guard.get("requires_primary_any_tags"))})
        if values:
            sources.append({"id": str(guard.get("id") or f"quality_guard:{len(sources)}"),
                            "requires_primary_any_tags": values})
    return sources


def quality_layer_primary_context_requirements(data: JsonDict, slot: str, item: Entry) -> Set[str]:
    return {value for row in quality_layer_primary_context_requirement_sources(data, slot, item)
            for value in row["requires_primary_any_tags"]}


def compatible_with_slot_context(
    slot: str,
    item: Entry,
    picked: Dict[str, Entry],
    source: Optional[JsonDict] = None,
) -> bool:
    context = picked_context_tokens(picked)
    primary_context = picked_core_context_tokens(picked)
    if picked.get("action"):
        primary_context |= entry_context_tokens(picked["action"])

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

    return True


# -----------------------------------------------------------------------------
# Frozen-core candidate retrieval
# -----------------------------------------------------------------------------

DIMENSION_FIELDS = {
    "subject": ["subject"], "identity": ["subject"], "age": ["subject"],
    "count": ["subject"], "species": ["subject"], "role": ["subject"],
    "appearance": ["subject", "style"], "body_geometry": ["subject", "event"],
    "setting": ["setting"], "timing": ["setting", "event"],
    "action": ["event"], "event": ["event"], "pose": ["event", "subject"],
    "relationship": ["event", "subject"], "character_response": ["event"],
    "expression": ["event", "visual_priorities"],
    "atmosphere": ["setting", "visual_priorities"],
    "lighting": ["style", "setting", "visual_priorities"],
    "style": ["style", "visual_priorities"], "color": ["style", "visual_priorities"],
    "material": ["subject", "setting", "visual_priorities"],
    "framing": ["style", "visual_priorities"],
    "composition": ["style", "visual_priorities"],
    "camera": ["style", "visual_priorities"], "format": ["style"],
    "text": ["event", "visual_priorities"],
    "viewer_outcome": ["visual_priorities"], "sexual_tone": ["subject", "style"],
}

def core_slot_focus_queries(data: dict, core: dict, slot: str) -> tuple[list[str], list[str]]:
    ownership = photo_candidate_semantics.slot_dimensions(slot, data.get("candidate_semantic_policy"))
    ownership = ownership or list(dict.fromkeys(
        dimension for entry in data.get("slots", {}).get(slot, [])
        for dimension in normalize_list(entry.get("affected_dimensions"))
    ))
    if not ownership:
        return [], []
    # Prefer literal, typed owner evidence to a generic field projection. The
    # property path distinguishes direction, height, focus, etc. within one
    # dimension; another owner's left/right words cannot supply this evidence.
    slot_parts = set(slot.split("_")) - {"camera", "light", "subject", "surface", "body"}
    evidence, evidence_fields = [], []
    anchors = [a for a in (core.get("intent_lock") or {}).get("semantic_anchors") or []
               if a.get("dimension") in ownership]
    # Keep the same owner's related evidence together (for example source
    # direction and its front/edge response), without borrowing focus evidence
    # for viewpoint or another object's property.
    property_scopes = {(a["dimension"], a["target"], a["property"].split(".")[0])
                       for a in anchors if "property" in a
                       and slot_parts & set(re.findall(r"[a-z]+", a["property"]))}
    for anchor in anchors:
        if "property" in anchor and (anchor["dimension"], anchor["target"], anchor["property"].split(".")[0]) not in property_scopes:
            continue
        evidence.append(anchor["prompt_evidence"])
        evidence_fields.append("intent_lock.semantic_anchors")
    for assertion in core.get("semantic_assertions") or []:
        if assertion.get("dimension") in ownership and assertion.get("polarity") in {"required", "advisory"}:
            evidence.extend((assertion.get("evidence") or {}).values())
            evidence_fields.append("semantic_assertions")
    if evidence:
        queries = []
        for phrase in dict.fromkeys(evidence):
            text, _ = authorial_core_retrieval_text({
                "contract_version": core["contract_version"], "request_binding": {"active_spans": []},
                "user_exclusions": core.get("user_exclusions") or [], "baseline_prompt_en": phrase,
            })
            if text and text not in queries:
                queries.append(text)
        return queries, list(dict.fromkeys(evidence_fields)) if queries else []
    if slot in {"camera_direction", "camera_height"}:
        clauses = photo_camera_evidence.legacy_camera_clauses(core, slot.removeprefix("camera_"))
        queries = []
        for clause in clauses:
            text, _ = authorial_core_retrieval_text({
                "contract_version": core["contract_version"], "request_binding": {"active_spans": []},
                "user_exclusions": core.get("user_exclusions") or [], "baseline_prompt_en": clause,
            })
            # Redaction may remove an excluded owner or verb. Do not turn its
            # remaining fragments into a positive camera clause.
            if text == clause:
                queries.append(text)
        if queries:
            return queries, ["baseline_prompt_en.camera_clause"]
    text, fields = candidate_pack_slot_focus_text(core, slot)
    if text:
        return [text], fields
    fields = list(dict.fromkeys(
        field for dimension in ownership for field in DIMENSION_FIELDS.get(dimension, [])
        if core.get(field)
    ))
    projection = {
        "contract_version": core["contract_version"],
        "request_binding": {"active_spans": []},
        "user_exclusions": core.get("user_exclusions") or [],
        **{field: core[field] for field in fields},
    }
    text, _ = authorial_core_retrieval_text(projection)
    return [text] if text else [], fields if text else []


def core_slot_focus_text(data: dict, core: dict, slot: str) -> tuple[str, list[str]]:
    queries, fields = core_slot_focus_queries(data, core, slot)
    return " | ".join(queries), fields


def core_focal_hit_supported(index: dict, query_terms: set[str], document_id: str) -> bool:
    """Require authored content overlap, not function words or boilerplate."""
    fields = index["documents"][document_id]["fields"]
    terms = {term for name, field in fields.items() if name != "semantic_caption"
             for term in field["term_frequencies"]}
    return bool(query_terms & terms)

def frozen_core_context(data: dict, core: dict, controls: dict) -> tuple[dict, dict]:
    constraints = resolve_request_intent_constraints(data, None, {}, authorial_core=core)
    typed_category = authored_subject_category(core.get("semantic_assertions") or [], controls["context"])
    if typed_category is not None:
        categories = {typed_category} if typed_category != "unknown" else set()
    else:
        categories = set(constraints.get("subject_categories") or [])
        categories.update(candidate_pack_direct_subject_categories(core["subject"]))
        if controls["context"]["subject_category"] == "human":
            categories.add("human")
    explicit = authorial_core_generation_constraints(core, creative_control_snapshot=controls)
    constraints["no_people"] = bool(constraints.get("no_people") or explicit["no_people"])
    if constraints["no_people"]:
        if typed_category == "human":
            raise ValueError("typed human subject conflicts with the requester no-people constraint")
        categories.discard("human")
    constraints["subject_categories"] = sorted(categories)
    domains = sorted(constraints.get("domains") or [])
    contract = {
        "subject_category": next(iter(categories)) if len(categories) == 1 else "generic",
        "domains": domains, "intent_constraints": constraints,
        "no_people": constraints["no_people"],
        "adult_allowed": any(controls["adult_appeal"][axis]["effective_intensity"] > 0
                             for axis in CANDIDATE_PACK_ADULT_APPEAL_AXES),
        "authorial_core_constraints": explicit, "_authorial_core": core,
        "concept_locks": [row["text"] for row in core["request_binding"]["active_spans"]],
        "candidate_pool_trace": {},
    }
    picked = {}
    for slot, field in (("subject", "subject"), ("location", "setting"), ("action", "event")):
        tokens = candidate_pack_relevance_tokens(str(core[field]))
        picked[slot] = {"en": core[field], "tags": sorted(tokens | set(domains)),
                        "kind": sorted(categories) if slot == "subject" else []}
    # Resolve only declared facet vocabulary against frozen text. Candidate
    # tags or another optional candidate never satisfy a prerequisite.
    facets: dict[str, set[str]] = {}
    candidate_pack_quality_add_intent_facets(
        facets, candidate_pack_quality_facet_vocab(data), data,
        [{"text": authorial_core_retrieval_text(core)[0]}],
    )
    picked["subject"]["facets"] = {key: sorted(values) for key, values in facets.items()}
    return contract, picked

def core_slot_entry_eligible(data: dict, core: dict, contract: dict, picked: dict, slot: str, entry: dict) -> bool:
    if slot_block_reason(data, slot, contract):
        return False
    reason = entry_block_reason(entry, slot, contract)
    if reason and not (reason == "adult_not_allowed"
                       and candidate_pack_age_only_subject_match(entry, slot, core)):
        return False
    subject_tokens = (entry_tags(picked["subject"])
                      | entry_kinds(picked["subject"]))
    if entry.get("for_any") and not set(entry["for_any"]) & subject_tokens:
        return False
    if set(entry.get("exclude_for_any") or []) & subject_tokens:
        return False
    if slot == "subject":
        categories = set(contract["intent_constraints"].get("subject_categories") or [])
        if categories and subject_category({"subject": entry}, data) not in categories:
            return False
    domains = {domain for tag, domain in INTENT_SCOPED_ENTRY_DOMAIN_TAGS.items()
               if tag in (entry_tags(entry) | entry_kinds(entry))}
    if domains and not domains & set(contract["intent_constraints"].get("domains") or []):
        return False
    others = {key: value for key, value in picked.items() if key != slot}
    if not compatible_with_facet_guards(entry, others):
        return False
    if not compatible_with_slot_context(slot, entry, others, data):
        return False
    blob = candidate_pack_entry_blob(entry, extra=[str(entry.get("embedding_text") or "")])
    return not any(intent_alias_matches(blob, exclusion)
                   for exclusion in core.get("user_exclusions") or [])

@functools.lru_cache(maxsize=2)
def _core_slot_index(corpus_json: str) -> dict:
    """Reuse derived statistics only for byte-identical authored slot data."""
    corpus = json.loads(corpus_json)
    documents = {
        f"slot:{slot}:{entry['id']}": semantic_bm25f_fields_for_entry(entry, slot, kind="slot")
        for slot, entries in corpus.items() for entry in entries
    }
    # Only the authored slot corpus contributes lexical retrieval statistics.
    return build_bm25f_index(
        documents, policy=SEMANTIC_BM25F_POLICY,
        lexicon=_bm25f_lexicon_from_documents(documents, ("aliases", "labels", "paraphrases")),
    )


def retrieve_core_slots(data: dict, core: dict, controls: dict) -> tuple[dict, dict, dict]:
    """Rank same-slot corpus only; never pad empty queries with default slots."""
    contract, picked = frozen_core_context(data, core, controls)
    global_query, _ = authorial_core_retrieval_text(core)
    corpus_json = json.dumps(data["slots"], ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    bm25f = _core_slot_index(corpus_json)
    eligible = {
        slot: {entry["id"]: entry for entry in entries
               if core_slot_entry_eligible(data, core, contract, picked, slot, entry)}
        for slot, entries in data["slots"].items()
    }
    discovery = candidate_pack_assertion_discovery(data, core, {
        f"slot:{slot}:{entry_id}": entry
        for slot, entries in eligible.items() for entry_id, entry in entries.items()
    }, bm25f, include_visual_priorities=True)
    observation_fields = [field for field in ("semantic_assertions", "visual_priorities")
                          if core.get(field)]
    discovery_slots = list(dict.fromkeys(document_id.split(":", 2)[1] for document_id in discovery))
    discovery_order = {slot: i for i, slot in enumerate(discovery_slots)}
    slots, active = {}, {}
    ranked_slots = {}
    # Rank every grounded slot before admission. Authored observations retain
    # priority within each round, but an early slot cannot spend the entire cap
    # before a later, successfully retrieved observation gets its first option.
    slot_order = sorted(data["slots"], key=lambda value: (
        value not in discovery_order, discovery_order.get(value, len(discovery_order)),
        value not in CANDIDATE_PACK_CORE_SLOTS, value,
    ))
    for slot in slot_order:
        queries, fields = core_slot_focus_queries(data, core, slot)
        query = " | ".join(queries)
        if not queries or slot_block_reason(data, slot, contract):
            continue
        entries = eligible[slot]
        ids = [f"slot:{slot}:{entry_id}" for entry_id in entries]
        limit = candidate_pack_slot_limit(slot)
        broad = rank_bm25f(bm25f, {"global_context": global_query}, allowed_ids=ids, limit=max(12, limit * 6))
        focal_lists = []
        for focus_query in queries:
            hits = rank_bm25f(bm25f, {"slot_focus": focus_query}, allowed_ids=ids, limit=max(12, limit * 6))
            query_terms = set(tokenize_bm25f_text(focus_query, lexicon=bm25f.get("lexicon") or [])) - CANDIDATE_PACK_CONCEPT_STOPWORDS
            focal_lists.append([row for row in hits if core_focal_hit_supported(bm25f, query_terms, row["document_id"])])
        focal = [row for hits in focal_lists for row in hits]
        observed = [document_id for document_id in discovery if document_id in ids]
        if (not broad or not focal) and not observed:
            continue
        broad_ids = {row["document_id"] for row in broad}
        focal_ids = {row["document_id"] for row in focal}
        intersection = broad_ids & focal_ids
        fused = reciprocal_rank_fusion(
            [[row["document_id"] for row in hits] for hits in [broad, *focal_lists]], k=30,
        )
        ranked = [row["document_id"] for row in fused if row["document_id"] in intersection]
        ranked = ranked or ([focal[0]["document_id"]] if focal else [])
        # Separate scoped statements can describe a source and its visible
        # consequence. Give each supported owner query a representative before
        # consensus fusion, so repeated incidental words cannot erase a cause.
        representatives = []
        if {"intent_lock.semantic_anchors", "semantic_assertions"} & set(fields):
            representatives = [next((row["document_id"] for row in hits if row["document_id"] in broad_ids), "")
                               for hits in focal_lists]
        ranked = list(dict.fromkeys(observed + [value for value in representatives if value] + ranked))
        if ranked:
            ranked_slots[slot] = (ranked[:limit], fields, observed, query)
    admitted = {slot: [] for slot in ranked_slots}
    total = 0
    # A frozen observation can independently support more than one candidate
    # in its slot. Preserve those bounded discoveries before generic options
    # consume the first round; optional adoption and every slot limit remain.
    for document_id in discovery:
        slot = document_id.split(":", 2)[1]
        if total >= CANDIDATE_PACK_TOTAL_CANDIDATE_LIMIT:
            break
        if slot in ranked_slots and document_id in ranked_slots[slot][0] and document_id not in admitted[slot]:
            admitted[slot].append(document_id)
            total += 1
    for position in range(max((len(rows[0]) for rows in ranked_slots.values()), default=0)):
        for slot, (ranked, _, _, _) in ranked_slots.items():
            if total >= CANDIDATE_PACK_TOTAL_CANDIDATE_LIMIT:
                break
            if position < len(ranked) and ranked[position] not in admitted[slot]:
                admitted[slot].append(ranked[position])
                total += 1
    for slot, document_ids in admitted.items():
        if not document_ids:
            continue
        _, fields, observed, query = ranked_slots[slot]
        candidates = []
        for document_id in document_ids:
            entry_id = document_id.split(":", 2)[2]
            candidate, _ = candidate_pack_summarize_slot_candidate(data, slot, {
                "id": entry_id, "applicability_status": "eligible",
                "applicability_source": "frozen_core_slot_contract",
            })
            candidates.append(candidate)
        active[slot] = {"source_fields": list(dict.fromkeys(fields + (observation_fields if observed else []))),
                        "focus_query_sha256": hashlib.sha256(query.encode()).hexdigest()}
        slots[slot] = {"slot": slot, "role": "core" if slot in CANDIDATE_PACK_CORE_SLOTS else "support",
                       "selected": None, "candidates": candidates, "candidate_count": len(eligible[slot]),
                       "candidate_limit": candidate_pack_slot_limit(slot)}
    binding = {
        "contract_version": "photo-core-retrieval/v1",
        "source_authorial_core_sha256": core["canonical_sha256"],
        "slot_corpus_sha256": hashlib.sha256(corpus_json.encode()).hexdigest(),
        "slot_ownership_sha256": canonical_json_sha256(data.get("candidate_semantic_policy") or {}),
        "slot_applicability_sha256": canonical_json_sha256(slot_applicability_from_source(data)["slots"]),
        "whole_scene_query_sha256": hashlib.sha256(global_query.encode()).hexdigest(),
        "active_slots": active, "retrieval": "same_slot_core_focus_and_frozen_observation_bm25f_rrf",
        "candidate_allocation": "one_supported_hit_per_slot_per_round",
        "observation_priority": "bounded_frozen_evidence_before_slot_rounds",
        "candidate_adoption": "optional",
    }
    binding["canonical_sha256"] = canonical_json_sha256(binding)
    return slots, binding, contract

def prepare_candidate_source(data: JsonDict, core: JsonDict, controls: JsonDict,
                             embodiment: JsonDict, *, seed: int = 0,
                             visual_intent: Optional[JsonDict] = None) -> JsonDict:
    """Bind an already-authored core before optional candidate retrieval."""
    creative_controls.validate(controls, core["source_request"])
    if core.get("creative_controls_sha256") != controls["canonical_sha256"]:
        raise ValueError("core does not bind the supplied creative controls")
    if core.get("contract_version") != AUTHORIAL_CORE_V3_CONTRACT_VERSION:
        raise ValueError("candidate retrieval requires a current v3 authorial core")
    values = creative_controls.runtime_values(controls)
    contract, _ = frozen_core_context(data, core, controls)
    negative = ", ".join(sorted(AUTHORIAL_INTENT_NEUTRAL_NEGATIVE_TERMS))
    return {
        "prompt_en": core["baseline_prompt_en"],
        "negative_en": negative,
        "choices": {},
        "negative_intent_guard": build_negative_intent_guard(
            core, negative, identity_preservation_enabled=values["reference_edit_mode"] == "identity"),
        "semantic_trace": {"generation_contract": contract, "selection_mode": "core_bm25f",
                           "slot_scores": [], "intent": None},
        "provenance": {
            "generator_version": GENERATOR_VERSION, "seed": seed, "batch_index": 0,
            "selection_mode": "core_bm25f", "tags_hash": dictionary_hash(data),
            "concept_lock": contract["concept_locks"], "additional_requirements": [],
            "reference_edit_mode": values["reference_edit_mode"], "likeness_mode": "off",
            "creative_controls": copy.deepcopy(controls), "creative_control_runtime": values,
            "creativity": values["creativity"], "candidate_pool_creativity": 3,
            "authorial_core": copy.deepcopy(core),
            "embodiment_preflight": photo_embodiment.build_policy(core, embodiment),
            **({"visual_intent": copy.deepcopy(visual_intent)} if visual_intent else {}),
        },
    }


def generate_candidate_pack(data: JsonDict, core: JsonDict, controls: JsonDict,
                            embodiment: JsonDict, *, seed: int = 0,
                            visual_intent: Optional[JsonDict] = None) -> JsonDict:
    result = prepare_candidate_source(data, core, controls, embodiment, seed=seed,
                                      visual_intent=visual_intent)
    return build_candidate_pack(result, data)


def load_runtime_data(tags_path: Optional[str | Path] = None) -> JsonDict:
    """Load and validate the authored corpus and its generated indexes."""
    path = Path(tags_path) if tags_path is not None else Path(__file__).resolve().parents[1] / "assets/photo_prompt_tags.json"
    assets = path.parent
    data = load_json(path)
    data[QUALITY_LAYERS_DATA_KEY] = load_quality_layers(assets / QUALITY_LAYERS_FILENAME)
    registry = load_visual_obligation_registry(assets / VISUAL_OBLIGATION_REGISTRY_FILENAME)
    data[VISUAL_OBLIGATIONS_DATA_KEY] = registry
    data[VISUAL_PROFILE_INDEX_DATA_KEY] = load_visual_profile_index(assets / VISUAL_PROFILE_INDEX_FILENAME, registry)
    data[SEMANTIC_INDEX_DATA_KEY] = load_semantic_index_payload(assets / "photo_prompt_semantic_index.json")
    validate_semantic_index_metadata(data[SEMANTIC_INDEX_DATA_KEY], data)
    return data


def filter_authorial_negative_entries(
    entries: Sequence[Entry],
    core: JsonDict,
    *,
    identity_preservation_enabled: bool,
) -> tuple[List[Entry], List[str]]:
    """Remove downstream negatives that can author a different image meaning."""

    kept: List[Entry] = []
    suppressed: List[str] = []
    for entry in entries:
        term = localize(entry, "en").strip()
        if authorial_negative_term_allowed(
            term,
            core,
            identity_preservation_enabled=identity_preservation_enabled,
        ):
            kept.append(entry)
        elif term:
            suppressed.append(term)
    return kept, suppressed


def authorial_negative_term_allowed(
    term: str,
    core: JsonDict,
    *,
    identity_preservation_enabled: bool,
) -> bool:
    """Return whether a v6 runtime-negative item is intent-safe.

    Generic safety, taste, count, action, relationship, expression, wardrobe,
    and genre suppressions are intentionally absent from the automatic lane.
    They are allowed only when they are a true requester exclusion.  Identity
    controls are a separate opt-in lane tied to an attached identity source.
    """

    key = normalize_negative_intent_term(term)
    if key in AUTHORIAL_INTENT_NEUTRAL_NEGATIVE_TERMS:
        return True
    if (
        identity_preservation_enabled
        and key in AUTHORIAL_IDENTITY_PRESERVATION_NEGATIVE_TERMS
    ):
        return True
    return negative_term_matches_requester_exclusion(
        key,
        [str(item) for item in core.get("user_exclusions") or []],
    )


def character_response_concept_profiles(data: JsonDict) -> List[JsonDict]:
    """Return data-authored character-response meanings without scene recipes."""

    graph = data.get("character_mechanism_graph")
    rows = graph.get("concept_profiles") if isinstance(graph, dict) else []
    return [copy.deepcopy(row) for row in rows or [] if isinstance(row, dict)]


def normalize_negative_intent_term(text: str) -> str:
    """Normalize one runtime-negative item without changing its meaning."""

    return clean_spaces(str(text or "")).strip(" .;:!?\"'").casefold()


def strip_negative_directive_prefix(text: str) -> str:
    normalized = normalize_negative_intent_term(text)
    return re.sub(
        r"^(?:no|without|avoid|exclude|excluding|do\s+not|don't|never)\s+",
        "",
        normalized,
        count=1,
    ).strip()


def negative_term_matches_requester_exclusion(
    term: str,
    exclusions: Sequence[str],
) -> bool:
    """Admit only an exclusion that is visibly grounded in requester text.

    The comparison removes only an explicit negative directive prefix.  The
    remaining phrase must equal one complete exclusion; splitting a combined
    exclusion, matching a substring, synonym expansion, and broader category
    inference are intentionally forbidden.
    """

    term_key = strip_negative_directive_prefix(term)
    if not term_key:
        return False
    for exclusion in exclusions:
        exclusion_key = strip_negative_directive_prefix(str(exclusion))
        if exclusion_key and term_key == exclusion_key:
            return True
    return False


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



def prepare_contextual_appeal_queries(data, result, core, snapshot, semantic_context, api_key=None):
    """Bind private query vectors to the exact post-core lanes and run ID."""
    retrieval = (candidate_pack_adult_policy(data)).get("contextual_retrieval") or {}
    if (semantic_context is None or not core or not snapshot
            or retrieval.get("contract_version") != photo_contextual_appeal.VERSION):
        return
    queries = photo_contextual_appeal.queries(
        core, snapshot["definitions"],
        {axis: snapshot["adult_appeal"][axis]["effective_intensity"] for axis in photo_contextual_appeal.AXES},
        authorial_core_retrieval_text,
    )
    by_axis: JsonDict = {}
    for axis, lanes in queries.items():
        for lane, text in lanes.items():
            # Match the existing single-query path. This provider can treat a
            # list of strings as one multimodal content rather than a batch.
            by_axis.setdefault(axis, {})[lane] = embed_single_semantic_text(
                text, model=semantic_context["embedding_model"],
                dimensions=semantic_context["embedding_dimensions"], api_key=api_key,
            )
    if queries:
        data.setdefault(photo_contextual_appeal.QUERY_CACHE, {})[result["provenance"]["prompt_id"]] = {
            "queries": queries, "vectors": by_axis,
        }
