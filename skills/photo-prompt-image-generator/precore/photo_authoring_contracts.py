"""Neutral authoring wire constants; no candidate taxonomy or routing."""
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

AUTHORIAL_CORE_V3_CONTRACT_VERSION = "photo-authorial-core/v3"

SUBJECT_CATEGORIES = frozenset({
    "human", "animal", "object", "food", "plant", "environment", "sign", "unknown",
})

def authored_subject_category(assertions: list[dict], context: dict | None = None) -> str | None:
    """Read the optional primary-subject type from frozen, grounded assertions.

    This is a handoff, never a noun classifier. The coarse nonhuman creative
    context and an absent/unknown type do not authorize object-only slots.
    """
    categories = set()
    for row in assertions:
        axes = row.get("axes") or {}
        if "subject_category" not in axes:
            continue
        value = axes["subject_category"]
        values = value if isinstance(value, list) else [value]
        if (row.get("dimension") != "subject" or row.get("polarity") != "required"
                or "subject" not in (row.get("affected_dimensions") or [])
                or len(values) != 1 or not isinstance(values[0], str)
                or values[0] not in SUBJECT_CATEGORIES):
            raise ValueError("subject_category requires one supported category in a required subject assertion")
        categories.add(values[0])
    if len(categories) > 1:
        raise ValueError("subject_category assertions disagree about the primary subject")
    category = next(iter(categories), None)
    context = context or {}
    if category == "human" and (context.get("subject_category") == "nonhuman" or context.get("no_people")):
        raise ValueError("typed human subject conflicts with the frozen creative context")
    if category not in {None, "human"} and context.get("subject_category") == "human":
        raise ValueError("typed subject category conflicts with the frozen human creative context")
    return category

AUTHORIAL_PROMPT_MIN_WORDS = 48

AUTHORIAL_PROMPT_RECOMMENDED_MAX_WORDS = 720

AUTHORIAL_PROMPT_ABSOLUTE_MAX_WORDS = 1280

REQUEST_LINEAGE_V2_CONTRACT_VERSION = "photo-request-lineage/v2"

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

INTENT_LOCK_CONTRACT_VERSION = "photo-intent-lock/v2"

INTENT_LOCK_PROPERTY_CONTRACT_VERSION = "photo-intent-lock/v2"

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
