"""Pure photo contract definitions shared by producer and independent auditors.

This module contains no candidate data, routing, filesystem access, or generators.
Sharing vocabulary and canonical serialization prevents policy drift; contract
construction and semantic validation remain separate in each consumer.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

CHARACTER_RESPONSE_RELATION_MEMBERS = {
    "actor",
    "baseline",
    "surface_affect",
    "underlying_affiliation",
    "relationship_target",
    "target",
    "primary_action",
    "affect_leak",
    "affect_leak_timing",
    "trigger",
    "visible_response",
    "immediate_consequence",
    "continuity",
    "event_phase",
}

LEGACY_AUTHORIAL_CORE_CONTRACT_VERSION = "photo-authorial-core/v1"

AUTHORIAL_CORE_CONTRACT_VERSION = "photo-authorial-core/v2"

AUTHORIAL_CORE_V3_CONTRACT_VERSION = "photo-authorial-core/v3"

AUTHORIAL_PROMPT_BUDGET_CONTRACT_VERSION = "photo-authorial-prompt-budget/v2"

AUTHORIAL_PROMPT_MIN_WORDS = 48

AUTHORIAL_PROMPT_RECOMMENDED_MAX_WORDS = 360

AUTHORIAL_PROMPT_ABSOLUTE_MAX_WORDS = 640

AUTHORIAL_PROMPT_REQUIRED_EVIDENCE_HEADROOM_WORDS = 160

AUTHORIAL_CORE_MODERN_CONTRACT_VERSIONS = {
    AUTHORIAL_CORE_CONTRACT_VERSION,
    AUTHORIAL_CORE_V3_CONTRACT_VERSION,
}

CHARACTER_RESPONSE_CONTRACT_VERSION = "photo-character-response/v1"

SEMANTIC_ASSERTION_OBLIGATIONS_CONTRACT_VERSION = (
    "photo-semantic-assertion-obligations/v1"
)

REQUEST_LINEAGE_V2_CONTRACT_VERSION = "photo-request-lineage/v2"

RENDER_REPAIR_CONTRACT_VERSION = "photo-render-repair/v1"

RENDER_REPAIR_IMPORTANCE_VALUES = {"primary", "supporting"}

RENDER_REPAIR_INTERACTION_STATES = {
    "held",
    "wielded",
    "used",
    "handed_off",
    "carried",
    "worn",
    "sheathed",
    "mounted",
    "resting",
    "other",
}

RENDER_REPAIR_CONTACT_EXPECTATIONS = {
    "required",
    "transitional",
    "absent",
    "unspecified",
}

RENDER_REPAIR_RELATION_ORIGINS = {
    "parent_preserved",
    "requester_corrected",
}

RENDER_REPAIR_ALLOWED_AXES = {
    "object_geometry",
    "contact_geometry",
    "local_pose",
    "camera",
    "framing",
    "lighting",
    "material",
    "occlusion",
}

RENDER_REPAIR_DIMENSION_AXES = {
    "camera": "camera",
    "framing": "framing",
    "lighting": "lighting",
    "material": "material",
}

CHARACTER_RESPONSE_REQUIRED_AXES = {
    "surface_affect",
    "underlying_affiliation",
    "relationship_target",
    "primary_action",
    "affect_leak_timing",
    "affect_leak_channels",
    "event_phase",
}

CHARACTER_RESPONSE_REQUIRED_EVIDENCE = {
    "actor_phrase",
    "baseline_phrase",
    "trigger_phrase",
    "target_phrase",
    "primary_action_phrase",
    "affective_leak_phrase",
    "visible_response_phrase",
    "immediate_consequence_phrase",
    "continuity_phrase",
}

REQUEST_ENVELOPE_CONTRACT_VERSION = "photo-request-envelope/v1"

REQUEST_BINDING_CONTRACT_VERSION = "photo-request-binding/v1"

INTENT_LOCK_CONTRACT_VERSION = "photo-intent-lock/v1"

INTENT_PRESERVATION_CONTRACT_VERSION = "photo-intent-preservation/v1"

DOWNSTREAM_INTENT_PRECEDENCE_CONTRACT_VERSION = (
    "photo-downstream-intent-precedence/v1"
)

NEGATIVE_INTENT_GUARD_CONTRACT_VERSION = "photo-negative-intent-guard/v1"

INTENT_LOCK_DIMENSIONS = {
    "concept",
    "subject",
    "identity",
    "count",
    "age",
    "role",
    "species",
    "appearance",
    "pose",
    "body_geometry",
    "expression",
    "action",
    "event",
    "setting",
    "relationship",
    "sexual_tone",
    "style",
    "reference_use",
    "viewer_outcome",
    "text",
    "format",
    "framing",
    "composition",
    "lighting",
    "camera",
    "color",
    "material",
    "timing",
    "atmosphere",
}

AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS = INTENT_LOCK_DIMENSIONS | {
    "character_response",
}

REQUIRED_INTENT_LOCK_DIMENSIONS = {"concept", "subject", "event"}

# Automatic negatives describe photographic defects. Requester exclusions and
# identity-preservation controls are admitted through separate consumer checks.
AUTHORIAL_INTENT_NEUTRAL_NEGATIVE_TERMS = {
    "3d render look",
    "awkward animal anatomy",
    "body distortion",
    "broken facial features",
    "broken window geometry",
    "cartoon style",
    "cgi look",
    "digital illustration",
    "distorted fingers",
    "excessive hdr",
    "fake-looking background",
    "flat collage look",
    "illustration look",
    "impossible perspective",
    "inaccurate reflections",
    "inconsistent shadows",
    "low resolution",
    "obvious cutout edges",
    "over-processed retouching",
    "overly smooth fur",
    "plastic-looking food texture",
    "plastic-looking skin",
    "unmatched lighting",
    "unrealistic hands",
    "unrealistic steam",
    "warped product geometry",
    "warped walls",
}

# These controls require explicit identity-reference preservation; they are not
# generic safety or taste defaults.
AUTHORIAL_IDENTITY_PRESERVATION_NEGATIVE_TERMS = {
    "de-aged identity",
    "dollified facial proportions",
    "duplicate primary subject",
    "enlarged or rounder eyes than the identity reference",
    "narrowed jaw compared with the identity reference",
    "second full recipient face",
    "shortened face compared with the identity reference",
}

AUTHORIAL_AUTHORSHIP_POLICY_CONTRACT_VERSION = "photo-authorial-authorship-policy/v1"
AUTHORIAL_CORE_BINDING_CONTRACT_VERSION = "photo-authorial-core-binding/v2"


def canonical_json_sha256(payload: Any) -> str:
    """Hash exact canonical UTF-8 JSON bytes without interpreting their content."""

    return hashlib.sha256(
        json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
