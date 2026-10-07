"""Pure photo contract definitions shared by producer and independent auditors.

This module contains no candidate data, routing, filesystem access, or generators.
Sharing vocabulary and canonical serialization prevents policy drift; contract
construction and semantic validation remain separate in each consumer.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

from photo_precore_bridge import load as _load_precore
_contracts = _load_precore("photo_authoring_contracts")
AUTHORIAL_CORE_V3_CONTRACT_VERSION = _contracts.AUTHORIAL_CORE_V3_CONTRACT_VERSION
AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS = _contracts.AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS
AUTHORIAL_PROMPT_ABSOLUTE_MAX_WORDS = _contracts.AUTHORIAL_PROMPT_ABSOLUTE_MAX_WORDS
AUTHORIAL_PROMPT_MIN_WORDS = _contracts.AUTHORIAL_PROMPT_MIN_WORDS
AUTHORIAL_PROMPT_RECOMMENDED_MAX_WORDS = _contracts.AUTHORIAL_PROMPT_RECOMMENDED_MAX_WORDS
CHARACTER_RESPONSE_RELATION_MEMBERS = _contracts.CHARACTER_RESPONSE_RELATION_MEMBERS
CHARACTER_RESPONSE_REQUIRED_AXES = _contracts.CHARACTER_RESPONSE_REQUIRED_AXES
CHARACTER_RESPONSE_REQUIRED_EVIDENCE = _contracts.CHARACTER_RESPONSE_REQUIRED_EVIDENCE
INTENT_LOCK_CONTRACT_VERSION = _contracts.INTENT_LOCK_CONTRACT_VERSION
INTENT_LOCK_DIMENSIONS = _contracts.INTENT_LOCK_DIMENSIONS
INTENT_LOCK_PROPERTY_CONTRACT_VERSION = _contracts.INTENT_LOCK_PROPERTY_CONTRACT_VERSION
RENDER_REPAIR_ALLOWED_AXES = _contracts.RENDER_REPAIR_ALLOWED_AXES
RENDER_REPAIR_CONTACT_EXPECTATIONS = _contracts.RENDER_REPAIR_CONTACT_EXPECTATIONS
RENDER_REPAIR_DIMENSION_AXES = _contracts.RENDER_REPAIR_DIMENSION_AXES
RENDER_REPAIR_IMPORTANCE_VALUES = _contracts.RENDER_REPAIR_IMPORTANCE_VALUES
RENDER_REPAIR_INTERACTION_STATES = _contracts.RENDER_REPAIR_INTERACTION_STATES
RENDER_REPAIR_RELATION_ORIGINS = _contracts.RENDER_REPAIR_RELATION_ORIGINS
REQUEST_BINDING_CONTRACT_VERSION = _contracts.REQUEST_BINDING_CONTRACT_VERSION
REQUEST_ENVELOPE_CONTRACT_VERSION = _contracts.REQUEST_ENVELOPE_CONTRACT_VERSION
REQUEST_LINEAGE_V2_CONTRACT_VERSION = _contracts.REQUEST_LINEAGE_V2_CONTRACT_VERSION
REQUIRED_INTENT_LOCK_DIMENSIONS = _contracts.REQUIRED_INTENT_LOCK_DIMENSIONS
SUBJECT_CATEGORIES = _contracts.SUBJECT_CATEGORIES
authored_subject_category = _contracts.authored_subject_category
canonical_json_sha256 = _contracts.canonical_json_sha256



AUTHORIAL_CORE_CONTRACT_VERSION = "photo-authorial-core/v3"


ADULT_APPEAL_DIMENSION_SCOPE_CONTRACT_VERSION = "photo-adult-appeal-dimension-scope/v4"

# These are possible carriers, not a requirement to change every dimension.
# New v6 adult-axis additions preserve explicit locks; other augmentation
# contracts continue to require explicitly open dimensions.
ADULT_APPEAL_AXIS_DIMENSIONS = {
    "sensual": frozenset({
        "sexual_tone", "style", "composition", "expression", "pose",
        "body_geometry", "framing", "lighting", "camera", "action",
        "color", "atmosphere", "appearance", "material",
    }),
    "fetish": frozenset({
        "sexual_tone", "style", "appearance", "material", "action", "pose", "body_geometry",
    }),
}


def intent_property_locks(intent_lock: dict) -> list[dict]:
    if intent_lock.get("contract_version") != "photo-intent-lock/v2":
        return []
    return [dict(row) for row in intent_lock.get("semantic_anchors", []) if "property" in row]






def property_effects_allowed(intent_lock: dict, dimensions, effects) -> bool:
    """Check declared property effects; semantic truth still needs agent review.

    Unknown/broad effects cannot claim compatibility with a partial lock.
    Parent paths include their children, so 'wardrobe' cannot bypass a locked
    'wardrobe.color'. Whole-dimension locks remain independent of properties.
    """
    locks = intent_property_locks(intent_lock)
    if not locks:
        return True
    if not isinstance(effects, list):
        return False
    seen = set()
    for row in effects:
        if not isinstance(row, dict) or set(row) != {"dimension", "target", "property"}:
            return False
        key = tuple(row[k] for k in ("dimension", "target", "property"))
        if any(not isinstance(v, str) or not v.strip() for v in key) or key in seen or key[0] not in dimensions:
            return False
        seen.add(key)
    def overlaps(left, right):
        return left == "*" or right == "*" or left == right or left.startswith(right + ".") or right.startswith(left + ".")
    for dimension in set(dimensions) & {row["dimension"] for row in locks}:
        declared = [row for row in effects if row["dimension"] == dimension]
        if not declared:
            return False
    # A carrier dimension does not change which semantic property is affected.
    # For example, declaring wardrobe.color as a material effect cannot bypass
    # a wardrobe.color anchor recorded under appearance.
    if any(overlaps(effect["target"], lock["target"]) and overlaps(effect["property"], lock["property"])
           for effect in effects for lock in locks):
        return False
    return True

AUTHORIAL_PROMPT_BUDGET_CONTRACT_VERSION = "photo-authorial-prompt-budget/v3"




AUTHORIAL_PROMPT_REQUIRED_EVIDENCE_HEADROOM_WORDS = 320

AUTHORIAL_CORE_MODERN_CONTRACT_VERSIONS = {
    AUTHORIAL_CORE_CONTRACT_VERSION,
    AUTHORIAL_CORE_V3_CONTRACT_VERSION,
}

CHARACTER_RESPONSE_CONTRACT_VERSION = "photo-character-response/v1"

SEMANTIC_ASSERTION_OBLIGATIONS_CONTRACT_VERSION = (
    "photo-semantic-assertion-obligations/v1"
)


RENDER_REPAIR_CONTRACT_VERSION = "photo-render-repair/v1"












INTENT_PRESERVATION_CONTRACT_VERSION = "photo-intent-preservation/v1"

DOWNSTREAM_INTENT_PRECEDENCE_CONTRACT_VERSION = (
    "photo-downstream-intent-precedence/v1"
)

NEGATIVE_INTENT_GUARD_CONTRACT_VERSION = "photo-negative-intent-guard/v1"




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

AUTHORIAL_AUTHORSHIP_POLICY_CONTRACT_VERSION = "photo-authorial-authorship-policy/v2"
AUTHORIAL_CORE_BINDING_CONTRACT_VERSION = "photo-authorial-core-binding/v3"
