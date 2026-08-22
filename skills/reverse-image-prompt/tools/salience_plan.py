#!/usr/bin/env python3
"""Validate source-relative salience plans and matched behavior-test pairs.

The tool checks the structured decision contract used by the skill. It does not
score prose style or infer semantics from keywords.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

from lighting_language import (
    classify_observation as classify_lighting_observation,
    review_candidates as review_lighting_candidates,
)


VALID_MODES = {"relationship-led", "appearance-led", "information-led", "mixed"}
VALID_AXES = {
    "form",
    "surface",
    "light-to-form",
    "color",
    "sharpness",
    "hierarchy",
    "topology",
    "information",
}
VALID_INVARIANT_ROLES = {"primary", "supporting"}
VALID_CLAIM_ROLES = {"primary", "supporting", "secondary", "drift-boundary"}
VALID_CAUSAL_ORIGINS = {
    "intrinsic",
    "pose-deformation",
    "perspective",
    "lighting-shadow",
    "material-interaction",
    "processing",
    "spatial-relation",
    "layout",
}
VALID_STRENGTHS = {"subtle", "moderate", "strong"}
VALID_POLARITIES = {"affirmative", "negative"}
VALID_SOURCE_KINDS = {
    "visible-evidence",
    "translated-causal-control",
    "diagnostic-appeal",
}
VALID_REGION_ROLES = {"dominant", "supporting", "edge-frame", "low-legibility"}
VALID_RELATIVE_AREAS = {"small", "medium", "large"}
VALID_ATTENTION = {"primary", "secondary", "background"}
VALID_COLOR_IMPORTANCE = {"primary", "supporting"}
VALID_COLOR_OBSERVATION_SCOPES = {"source-visible", "color-managed", "user-specified"}
VALID_DISPLAYED_TONE_AXES = {
    "displayed-key-level",
    "shadow-floor",
    "highlight-rolloff",
    "microcontrast",
}
VALID_COLOR_AXES = {"value", "chroma", "hue", "contrast"} | VALID_DISPLAYED_TONE_AXES
VALID_INTRINSIC_COLOR_AXES = {"value", "chroma", "hue"}
VALID_COLOR_CAUSAL_LAYERS = {
    "intrinsic",
    "illumination",
    "global-cast",
    "exposure",
    "processing",
    "hierarchy",
}
VALID_COLOR_CONFIDENCE = {"high", "medium", "low"}
VALID_NEUTRAL_ANCHOR_STATUS = {"available", "unavailable", "uncertain"}
VALID_TONE_ZONES = {"highlight", "midtone", "shadow", "flat"}
VALID_COLOR_AXIS_ROLES = {"primary", "supporting"}
VALID_COLOR_AXIS_EMISSIONS = {"required", "diagnostic-only"}
VALID_COLOR_EVIDENCE_SCOPES = VALID_TONE_ZONES | {"mixed"}
VALID_COLOR_CONTROL_ROLES = {"axis-control", "compound-control"}
VALID_APPEARANCE_METAPHOR_STATUS = {
    "explanation-only",
    "model-calibrated",
    "unverified",
}
VALID_DISPLAYED_TONE_CLASSES = {
    "displayed-key-level": {"very-low", "low", "middle", "high", "very-high", "uncertain"},
    "shadow-floor": {"crushed", "deep", "open", "lifted", "mixed", "uncertain"},
    "highlight-rolloff": {
        "clipped",
        "abrupt-unclipped",
        "gradual-unclipped",
        "compressed",
        "mixed",
        "uncertain",
    },
    "microcontrast": {"suppressed", "natural", "emphasized", "mixed", "uncertain"},
}
DISPLAYED_TONE_ALLOWED_LAYERS = {
    "displayed-key-level": {"illumination", "exposure", "processing"},
    "shadow-floor": {"illumination", "exposure", "processing"},
    "highlight-rolloff": {"exposure", "processing"},
    "microcontrast": {"illumination", "processing"},
}
VALID_SURFACE_LANGUAGE_POLICY_STATUS = {
    "uncalibrated-language-prototype",
    "model-calibrated",
}
VALID_SURFACE_VALUE_DEPTH = {"very-light", "light", "medium", "deep", "uncertain"}
VALID_SURFACE_CHROMA = {"very-low", "low", "moderate", "rich", "uncertain"}
VALID_SURFACE_UNDERTONES = {
    "rosy",
    "peach",
    "neutral",
    "golden",
    "olive",
    "mixed",
    "uncertain",
}
VALID_SURFACE_FINISH = {"matte", "satin", "luminous", "dewy", "uncertain"}
VALID_SURFACE_EVENNESS = {"even", "naturally-varied", "freckled", "uncertain"}
VALID_FRIENDLY_LABEL_SCOPES = {
    "value-depth",
    "undertone",
    "surface-finish",
    "composite-appearance",
}
VALID_FRIENDLY_LABEL_REVIEWS = {"compatible", "conflicting", "inconclusive"}
VALID_FRIENDLY_LABEL_SOURCES = {"user-supplied", "versioned-vocabulary"}
VALID_LIGHT_IMPORTANCE = {"primary", "supporting"}
VALID_LIGHT_OBSERVATION_SCOPES = {"source-visible", "user-specified"}
VALID_LIGHT_FORM_CONTRAST = {"flattening", "subtle", "moderate", "strong"}
VALID_LIGHT_BRIGHT_COVERAGE = {"narrow", "balanced", "broad", "mixed", "uncertain"}
VALID_LIGHT_GRADIENT_EXTENT = {"short", "medium", "long", "mixed", "uncertain"}
VALID_LIGHT_BACKGROUND_SPILL = {"suppressed", "low", "moderate", "high", "mixed", "uncertain"}
VALID_LIGHT_MODEL_TYPES = {"physical-light", "rendered-shading", "mixed", "uncertain"}
VALID_LIGHT_SOURCE_COUNTS = {"one-dominant", "multiple", "mixed", "uncertain"}
VALID_LIGHT_AXIS_OFFSETS = {"near-axis", "slight", "moderate", "strong", "uncertain"}
VALID_LIGHT_ELEVATIONS = {"below", "level", "slight-above", "high", "uncertain"}
VALID_LIGHT_SOURCE_SIZES = {"small", "medium", "large", "uncertain"}
VALID_LIGHT_FILL_STRUCTURES = {"high", "moderate", "low", "mixed", "uncertain"}
VALID_LIGHT_ACTUATIONS = {
    "physical-cause",
    "physical-plus-result",
    "result-space-only",
    "diagnostic-only",
}
VALID_LIGHT_REGION_EFFECT_ROLES = {
    "broad-plane",
    "gradient",
    "highlight",
    "shadow",
    "rim",
    "spill",
}
VALID_SHADOW_OWNERS = {
    "cast",
    "self",
    "contact-occlusion",
    "material-response",
    "processing",
    "mixed",
    "uncertain",
}
VALID_LIGHT_MATERIAL_RESPONSES = {
    "diffuse",
    "absorbent",
    "glossy",
    "metallic",
    "translucent",
    "woven",
    "mixed",
}
VALID_LIGHT_GEOMETRY_DEPENDENCIES = {
    "pose-bound",
    "pose-robust",
    "mixed",
    "uncertain",
}
VALID_LIGHT_EFFECT_AXES = {
    "source-geometry",
    "fill",
    "local-form-contrast",
    "bright-plane-coverage",
    "gradient-extent",
    "shadow-topology",
    "material-response",
    "background-spill",
}
VALID_LIGHT_LANGUAGE_POLICY_STATUS = {
    "uncalibrated-language-prototype",
    "model-calibrated",
}
VALID_LIGHT_LABEL_STATUS = {
    "explanation-only",
    "unverified",
    "model-calibrated",
}

LIGHTING_LANGUAGE_POLICY_PATH = (
    Path(__file__).resolve().parents[1]
    / "references"
    / "lighting-language-policy.json"
)


def _contract(plan: dict[str, Any]) -> dict[str, Any]:
    nested = plan.get("render_contract")
    return nested if isinstance(nested, dict) else plan


def _nonempty_strings(value: Any) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) and item.strip() for item in value)
    )


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: Any) -> bool:
    return isinstance(value, list) and all(_nonempty_string(item) for item in value)


def _audit_lighting_language(
    light_contract: dict[str, Any],
    color_contract: dict[str, Any] | None,
    known_regions: set[str],
    control_ids: set[str],
) -> list[str]:
    """Validate optional axis-first lighting language and emitted shorthand."""

    errors: list[str] = []
    lighting_language = light_contract.get("lighting_language")
    labels = light_contract.get("lighting_labels", [])
    if lighting_language is None:
        if not isinstance(labels, list):
            errors.append("light_form_contract.lighting_labels must be a list")
        elif labels:
            errors.append(
                "light_form_contract.lighting_labels requires lighting_language compatibility review"
            )
        return errors
    if not isinstance(lighting_language, dict):
        return ["light_form_contract.lighting_language must be an object"]

    try:
        policy = json.loads(LIGHTING_LANGUAGE_POLICY_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"lighting language policy could not be loaded: {exc}"]

    prefix = "light_form_contract.lighting_language"
    if lighting_language.get("policy_id") != policy.get("id"):
        errors.append(f"{prefix}.policy_id must match the selected policy")
    if lighting_language.get("policy_status") not in VALID_LIGHT_LANGUAGE_POLICY_STATUS:
        errors.append(f"{prefix}.policy_status is invalid")
    elif lighting_language.get("policy_status") != policy.get("status"):
        errors.append(f"{prefix}.policy_status must match the selected policy")
    if lighting_language.get("observation_scope") != light_contract.get(
        "observation_scope"
    ):
        errors.append(
            f"{prefix}.observation_scope must match the Light/Form contract"
        )
    if lighting_language.get("region_id") not in known_regions:
        errors.append(f"{prefix}.region_id references an unknown region")
    if not _nonempty_strings(lighting_language.get("source_evidence")):
        errors.append(f"{prefix}.source_evidence must contain visible evidence")

    observation = {
        "observation_scope": lighting_language.get("observation_scope"),
        "region_id": lighting_language.get("region_id"),
        "source_evidence": lighting_language.get("source_evidence"),
        "axis_classification": lighting_language.get("axis_classification"),
    }
    classification: dict[str, Any] | None = None
    try:
        classification = classify_lighting_observation(observation, policy)
    except ValueError as exc:
        errors.append(f"{prefix}: {exc}")

    compatible_phrases: set[str] = set()
    if classification is not None:
        expected_summary = classification["controlled_summary"]
        if lighting_language.get("controlled_summary") != expected_summary:
            errors.append(
                f"{prefix}.controlled_summary must match the policy-derived explanation-only summary"
            )

        classifications = classification["axis_classification"]
        observed = light_contract.get("observed_result", {})
        hypothesis = light_contract.get("source_hypothesis", {})
        contract_axis_values = {
            "local_form_contrast": observed.get("local_form_contrast"),
            "bright_plane_coverage": observed.get("bright_plane_coverage"),
            "gradient_extent": observed.get("gradient_extent"),
            "fill_structure": hypothesis.get("fill_structure"),
        }
        for axis, contract_value in contract_axis_values.items():
            language_value = classifications[axis]["term"]
            if language_value not in {"mixed", "uncertain"} and language_value != contract_value:
                errors.append(
                    f"{prefix}.axis_classification.{axis} conflicts with the Light/Form contract"
                )

        if isinstance(color_contract, dict):
            tone_responses = color_contract.get("displayed_tone_response", [])
            if isinstance(tone_responses, list):
                language_region = lighting_language.get("region_id")
                tone_axis_map = {
                    "displayed-key-level": "displayed_key_level",
                    "shadow-floor": "shadow_floor",
                }
                for tone_axis, language_axis in tone_axis_map.items():
                    matching_classes = {
                        item.get("class")
                        for item in tone_responses
                        if isinstance(item, dict)
                        and item.get("axis") == tone_axis
                        and item.get("region_id") == language_region
                    }
                    language_value = classifications[language_axis]["term"]
                    if (
                        matching_classes
                        and language_value not in {"mixed", "uncertain"}
                        and matching_classes != {language_value}
                    ):
                        errors.append(
                            f"{prefix}.axis_classification.{language_axis} conflicts with the Color/Tone contract"
                        )

        reviews = lighting_language.get("friendly_label_review", [])
        if not isinstance(reviews, list):
            errors.append(f"{prefix}.friendly_label_review must be a list")
            reviews = []
        seen_phrases: set[str] = set()
        for index, review in enumerate(reviews):
            label = f"{prefix}.friendly_label_review[{index}]"
            if not isinstance(review, dict):
                errors.append(f"{label} must be an object")
                continue
            phrase = review.get("phrase")
            if _nonempty_string(phrase):
                normalized_phrase = phrase.strip()
                if normalized_phrase in seen_phrases:
                    errors.append(f"{label}.phrase is duplicated")
                seen_phrases.add(normalized_phrase)
            try:
                expected_reviews = review_lighting_candidates(
                    classification,
                    {
                        "candidate_source": review.get("candidate_source"),
                        "candidates": [
                            {
                                "phrase": phrase,
                                "label_scope": review.get("label_scope"),
                                "axis_requirements": review.get("axis_requirements"),
                            }
                        ],
                    },
                    policy,
                )
            except ValueError as exc:
                errors.append(f"{label}: {exc}")
                continue
            expected = expected_reviews[0]
            if any(review.get(field) != value for field, value in expected.items()):
                errors.append(
                    f"{label} compatibility result does not match the classified evidence"
                )
                continue
            if expected["review_status"] == "compatible":
                compatible_phrases.add(expected["phrase"])

    if not isinstance(labels, list):
        errors.append("light_form_contract.lighting_labels must be a list")
        labels = []
    seen_label_phrases: set[str] = set()
    emitted_label_count = 0
    for index, lighting_label in enumerate(labels):
        label = f"light_form_contract.lighting_labels[{index}]"
        if not isinstance(lighting_label, dict):
            errors.append(f"{label} must be an object")
            continue
        phrase = lighting_label.get("phrase")
        if not _nonempty_string(phrase):
            errors.append(f"{label}.phrase must be non-empty")
        else:
            normalized_phrase = phrase.strip()
            if normalized_phrase in seen_label_phrases:
                errors.append(f"{label}.phrase is duplicated")
            seen_label_phrases.add(normalized_phrase)
        status = lighting_label.get("status")
        if status not in VALID_LIGHT_LABEL_STATUS:
            errors.append(f"{label}.status is invalid")
        emit = lighting_label.get("emit")
        if not isinstance(emit, bool):
            errors.append(f"{label}.emit must be boolean")
            emit = False
        elif emit:
            emitted_label_count += 1
        if emit and status != "model-calibrated":
            errors.append(f"{label}: only a model-calibrated lighting label may be emitted")
        if status == "model-calibrated":
            for field in ("generator_id", "generator_version", "conditioning_route"):
                if not _nonempty_string(lighting_label.get(field)):
                    errors.append(f"{label}.{field} is required for model calibration")
            if not _nonempty_strings(lighting_label.get("calibration_evidence")):
                errors.append(f"{label}.calibration_evidence is required for model calibration")
        if emit and (
            not _nonempty_string(phrase) or phrase.strip() not in compatible_phrases
        ):
            errors.append(
                f"{label}: an emitted friendly lighting label requires a compatible review"
            )
        decomposed_ids = lighting_label.get("decomposed_control_ids", [])
        if not isinstance(decomposed_ids, list) or not all(
            _nonempty_string(item) for item in decomposed_ids
        ):
            errors.append(f"{label}.decomposed_control_ids must be strings")
            decomposed_ids = []
        if emit and not decomposed_ids:
            errors.append(
                f"{label}: an emitted friendly lighting label requires literal decomposed controls"
            )
        unknown_controls = sorted(set(decomposed_ids) - control_ids)
        if unknown_controls:
            errors.append(
                f"{label}.decomposed_control_ids references unknown controls: "
                + ", ".join(unknown_controls)
            )

    if emitted_label_count > 1:
        errors.append("light_form_contract may emit at most one friendly lighting label")

    return errors


def _audit_color_tone_contract(
    contract: dict[str, Any],
    claim_map: dict[str, dict[str, Any]],
    major_region_ids: set[str],
) -> list[str]:
    """Validate the optional source-relative color/tone decision contract."""

    errors: list[str] = []
    color_contract = contract.get("color_tone_contract")
    claims_with_effects = {
        claim_id
        for claim_id, claim in claim_map.items()
        if isinstance(claim.get("perceptual_effects"), list)
        and bool(claim["perceptual_effects"])
    }
    if color_contract is None:
        if claims_with_effects:
            errors.append(
                "candidate claims with perceptual_effects require color_tone_contract"
            )
        return errors
    if not isinstance(color_contract, dict):
        return ["color_tone_contract must be an object"]

    importance = color_contract.get("importance")
    if importance not in VALID_COLOR_IMPORTANCE:
        errors.append(
            f"color_tone_contract.importance must be one of {sorted(VALID_COLOR_IMPORTANCE)}"
        )

    observation_scope = color_contract.get("observation_scope")
    if not isinstance(observation_scope, str) or observation_scope not in VALID_COLOR_OBSERVATION_SCOPES:
        errors.append(
            "color_tone_contract.observation_scope must be one of "
            f"{sorted(VALID_COLOR_OBSERVATION_SCOPES)}"
        )

    global_spec = color_contract.get("global")
    if not isinstance(global_spec, dict):
        errors.append("color_tone_contract.global must be an object")
    else:
        global_fields = (
            "cast_or_palette_shift",
            "exposure_behavior",
            "contrast_and_tone_curve",
            "processing_shift",
        )
        populated = False
        for field in global_fields:
            value = global_spec.get(field)
            if value is not None and not isinstance(value, str):
                errors.append(f"color_tone_contract.global.{field} must be a string")
            populated = populated or _nonempty_string(value)
        if not populated:
            errors.append(
                "color_tone_contract.global must record at least one observed or uncertain global behavior"
            )
        if not _nonempty_strings(global_spec.get("source_evidence")):
            errors.append(
                "color_tone_contract.global.source_evidence must contain visible evidence"
            )

    regions = color_contract.get("regions")
    if not isinstance(regions, list) or not regions:
        errors.append("color_tone_contract.regions must contain at least one region")
        regions = []

    color_region_ids: set[str] = set()
    axis_requirements: list[tuple[str, str, str, dict[str, Any]]] = []
    displayed_tone_requirements: list[tuple[str, str, str, dict[str, Any]]] = []
    for index, region in enumerate(regions):
        label = f"color_tone_contract.regions[{index}]"
        if not isinstance(region, dict):
            errors.append(f"{label} must be an object")
            continue
        region_id = region.get("id")
        if not _nonempty_string(region_id):
            errors.append(f"{label}.id must be non-empty")
            continue
        if region_id in color_region_ids:
            errors.append(f"duplicate color/tone region id: {region_id}")
        color_region_ids.add(region_id)
        if region.get("role") not in VALID_REGION_ROLES:
            errors.append(f"{label}.role is invalid")
        if not _nonempty_strings(region.get("source_evidence")):
            errors.append(f"{label}.source_evidence must contain visible evidence")

        intrinsic_axes = region.get("intrinsic_axes")
        if not isinstance(intrinsic_axes, list) or not intrinsic_axes:
            errors.append(f"{label}.intrinsic_axes must contain observed axes")
            intrinsic_axes = []
        seen_axes: set[str] = set()
        for axis_index, axis_spec in enumerate(intrinsic_axes):
            axis_label = f"{label}.intrinsic_axes[{axis_index}]"
            if not isinstance(axis_spec, dict):
                errors.append(f"{axis_label} must be an object")
                continue
            axis = axis_spec.get("axis")
            if axis not in VALID_INTRINSIC_COLOR_AXES:
                errors.append(f"{axis_label}.axis is invalid")
                continue
            if axis in seen_axes:
                errors.append(f"{label} repeats intrinsic axis {axis!r}")
            seen_axes.add(axis)
            if not _nonempty_string(axis_spec.get("observation")):
                errors.append(f"{axis_label}.observation must be non-empty")
            if axis_spec.get("confidence") not in VALID_COLOR_CONFIDENCE:
                errors.append(f"{axis_label}.confidence is invalid")
            if not _nonempty_strings(axis_spec.get("source_evidence")):
                errors.append(f"{axis_label}.source_evidence must contain visible evidence")
            if axis_spec.get("role") not in VALID_COLOR_AXIS_ROLES:
                errors.append(f"{axis_label}.role is invalid")
            evidence_scope = axis_spec.get("evidence_scope")
            if evidence_scope not in VALID_COLOR_EVIDENCE_SCOPES:
                errors.append(f"{axis_label}.evidence_scope is invalid")
            emission = axis_spec.get("emission")
            if emission not in VALID_COLOR_AXIS_EMISSIONS:
                errors.append(f"{axis_label}.emission is invalid")
            effect_id = axis_spec.get("aggregate_effect_id")
            if emission == "required" and not _nonempty_string(effect_id):
                errors.append(
                    f"{axis_label}.aggregate_effect_id is required for an emitted axis"
                )
            if emission == "diagnostic-only":
                if not _nonempty_string(axis_spec.get("non_emission_reason")):
                    errors.append(
                        f"{axis_label}.non_emission_reason is required for a diagnostic-only axis"
                    )
                if _nonempty_string(effect_id):
                    errors.append(
                        f"{axis_label} cannot reference an aggregate effect when diagnostic-only"
                    )
            if evidence_scope == "mixed" and emission == "required":
                errors.append(
                    f"{axis_label}: mixed tone-zone evidence cannot drive an emitted intrinsic axis"
                )
            axis_requirements.append((str(region_id), str(axis), axis_label, axis_spec))
        if (
            importance == "primary"
            and region.get("role") == "dominant"
            and seen_axes != VALID_INTRINSIC_COLOR_AXES
        ):
            missing = sorted(VALID_INTRINSIC_COLOR_AXES - seen_axes)
            if missing:
                errors.append(
                    f"{label} must account for primary intrinsic axes: {', '.join(missing)}"
                )

        tone_zones = region.get("tone_zones", [])
        if not isinstance(tone_zones, list):
            errors.append(f"{label}.tone_zones must be a list")
            tone_zones = []
        if importance == "primary" and region.get("role") == "dominant" and not tone_zones:
            errors.append(
                f"{label}.tone_zones must record highlight/midtone/shadow or flat behavior"
            )
        seen_zones: set[str] = set()
        for zone_index, zone_spec in enumerate(tone_zones):
            zone_label = f"{label}.tone_zones[{zone_index}]"
            if not isinstance(zone_spec, dict):
                errors.append(f"{zone_label} must be an object")
                continue
            zone = zone_spec.get("zone")
            if zone not in VALID_TONE_ZONES:
                errors.append(f"{zone_label}.zone is invalid")
                continue
            if zone in seen_zones:
                errors.append(f"{label} repeats tone zone {zone!r}")
            seen_zones.add(zone)
            if not _nonempty_string(zone_spec.get("observation")):
                errors.append(f"{zone_label}.observation must be non-empty")
            if zone_spec.get("confidence") not in VALID_COLOR_CONFIDENCE:
                errors.append(f"{zone_label}.confidence is invalid")
            if not _nonempty_strings(zone_spec.get("source_evidence")):
                errors.append(f"{zone_label}.source_evidence must contain visible evidence")

        relations = region.get("relative_relations", [])
        if not isinstance(relations, list) or not all(
            _nonempty_string(item) for item in relations
        ):
            errors.append(f"{label}.relative_relations must be non-empty strings")
        elif importance == "primary" and region.get("role") == "dominant" and not relations:
            errors.append(
                f"{label}.relative_relations must calibrate a primary color/tone region"
            )

    neutral_status = color_contract.get("neutral_anchor_status")
    if neutral_status not in VALID_NEUTRAL_ANCHOR_STATUS:
        errors.append("color_tone_contract.neutral_anchor_status is invalid")
    uncertainty_note = color_contract.get("uncertainty_note", "")
    if neutral_status in {"unavailable", "uncertain"} and not _nonempty_string(
        uncertainty_note
    ):
        errors.append(
            "color_tone_contract.uncertainty_note is required without a reliable neutral anchor"
        )

    neutral_anchors = color_contract.get("neutral_anchors", [])
    if not isinstance(neutral_anchors, list):
        errors.append("color_tone_contract.neutral_anchors must be a list")
        neutral_anchors = []
    known_regions = color_region_ids | major_region_ids | {"global"}
    reliable_anchor_count = 0
    for index, anchor in enumerate(neutral_anchors):
        label = f"color_tone_contract.neutral_anchors[{index}]"
        if not isinstance(anchor, dict):
            errors.append(f"{label} must be an object")
            continue
        region_id = anchor.get("region_id")
        if region_id not in known_regions:
            errors.append(f"{label}.region_id references an unknown region")
        confidence = anchor.get("confidence")
        if confidence not in VALID_COLOR_CONFIDENCE:
            errors.append(f"{label}.confidence is invalid")
        elif confidence in {"high", "medium"}:
            reliable_anchor_count += 1
        if not _nonempty_strings(anchor.get("source_evidence")):
            errors.append(f"{label}.source_evidence must contain visible evidence")
    if neutral_status == "available" and reliable_anchor_count == 0:
        errors.append(
            "color_tone_contract requires a medium- or high-confidence neutral anchor when status is available"
        )

    displayed_tone_response = color_contract.get("displayed_tone_response", [])
    if not isinstance(displayed_tone_response, list):
        errors.append("color_tone_contract.displayed_tone_response must be a list")
        displayed_tone_response = []
    seen_displayed_axes: set[tuple[str, str]] = set()
    for index, response in enumerate(displayed_tone_response):
        label = f"color_tone_contract.displayed_tone_response[{index}]"
        if not isinstance(response, dict):
            errors.append(f"{label} must be an object")
            continue
        region_id = response.get("region_id")
        axis = response.get("axis")
        if region_id not in known_regions:
            errors.append(f"{label}.region_id references an unknown region")
        if axis not in VALID_DISPLAYED_TONE_AXES:
            errors.append(f"{label}.axis is invalid")
            continue
        signature = (str(region_id), str(axis))
        if signature in seen_displayed_axes:
            errors.append(f"{label} repeats one region and displayed-tone axis")
        seen_displayed_axes.add(signature)
        if response.get("class") not in VALID_DISPLAYED_TONE_CLASSES[axis]:
            errors.append(f"{label}.class is invalid for {axis}")
        if response.get("role") not in VALID_COLOR_AXIS_ROLES:
            errors.append(f"{label}.role is invalid")
        if response.get("confidence") not in VALID_COLOR_CONFIDENCE:
            errors.append(f"{label}.confidence is invalid")
        if not _nonempty_strings(response.get("source_evidence")):
            errors.append(f"{label}.source_evidence must contain visible evidence")
        emission = response.get("emission")
        if emission not in VALID_COLOR_AXIS_EMISSIONS:
            errors.append(f"{label}.emission is invalid")
        effect_id = response.get("aggregate_effect_id")
        if emission == "required" and not _nonempty_string(effect_id):
            errors.append(
                f"{label}.aggregate_effect_id is required for an emitted displayed-tone axis"
            )
        if emission == "diagnostic-only":
            if not _nonempty_string(response.get("non_emission_reason")):
                errors.append(
                    f"{label}.non_emission_reason is required for a diagnostic-only axis"
                )
            if _nonempty_string(effect_id):
                errors.append(
                    f"{label} cannot reference an aggregate effect when diagnostic-only"
                )
        displayed_tone_requirements.append(
            (str(region_id), str(axis), label, response)
        )

    aggregate_effects = color_contract.get("aggregate_effects")
    if not isinstance(aggregate_effects, list) or not aggregate_effects:
        errors.append(
            "color_tone_contract.aggregate_effects must contain at least one source target"
        )
        aggregate_effects = []
    aggregate_map: dict[str, dict[str, Any]] = {}
    aggregate_signatures: dict[tuple[str, str, str], str] = {}
    primary_effect_count = 0
    for index, effect in enumerate(aggregate_effects):
        label = f"color_tone_contract.aggregate_effects[{index}]"
        if not isinstance(effect, dict):
            errors.append(f"{label} must be an object")
            continue
        effect_id = effect.get("id")
        if not _nonempty_string(effect_id):
            errors.append(f"{label}.id must be non-empty")
            continue
        if effect_id in aggregate_map:
            errors.append(f"duplicate aggregate color/tone effect id: {effect_id}")
        aggregate_map[effect_id] = effect
        axis = effect.get("axis")
        if axis not in VALID_COLOR_AXES:
            errors.append(f"{label}.axis is invalid")
        direction = effect.get("direction")
        if not _nonempty_string(direction):
            errors.append(f"{label}.direction must be non-empty")
        region_id = effect.get("region_id")
        if region_id not in known_regions:
            errors.append(f"{label}.region_id references an unknown region")
        if axis in VALID_COLOR_AXES and _nonempty_string(direction) and region_id in known_regions:
            normalized_direction = "-".join(
                direction.casefold().replace("_", " ").replace("-", " ").split()
            )
            signature = (str(region_id), str(axis), normalized_direction)
            previous = aggregate_signatures.get(signature)
            if previous is not None:
                errors.append(
                    f"aggregate effects {previous!r} and {effect_id!r} split one region/axis/direction"
                )
            else:
                aggregate_signatures[signature] = str(effect_id)
        if effect.get("role") not in VALID_INVARIANT_ROLES:
            errors.append(f"{label}.role is invalid")
        elif effect.get("role") == "primary":
            primary_effect_count += 1
        if effect.get("target_strength") not in VALID_STRENGTHS:
            errors.append(f"{label}.target_strength is invalid")
        if not isinstance(effect.get("source_supported"), bool):
            errors.append(f"{label}.source_supported must be boolean")
        if not _nonempty_strings(effect.get("source_evidence")):
            errors.append(f"{label}.source_evidence must contain visible evidence")
        if not _nonempty_strings(effect.get("claim_ids")):
            errors.append(f"{label}.claim_ids must contain emitted color/tone claims")
    if importance == "primary" and primary_effect_count == 0:
        errors.append(
            "a primary color_tone_contract must contain a primary aggregate effect"
        )

    for region_id, axis, axis_label, axis_spec in axis_requirements:
        if axis_spec.get("emission") != "required":
            continue
        effect_id = axis_spec.get("aggregate_effect_id")
        effect = aggregate_map.get(effect_id)
        if effect is None:
            errors.append(f"{axis_label}.aggregate_effect_id is unknown")
            continue
        if effect.get("region_id") != region_id or effect.get("axis") != axis:
            errors.append(
                f"{axis_label}.aggregate_effect_id must match the same region and axis"
            )
        if axis_spec.get("role") == "primary" and effect.get("role") != "primary":
            errors.append(
                f"{axis_label}: a primary intrinsic axis requires a primary aggregate effect"
            )

    for region_id, axis, axis_label, axis_spec in displayed_tone_requirements:
        if axis_spec.get("emission") != "required":
            continue
        effect_id = axis_spec.get("aggregate_effect_id")
        effect = aggregate_map.get(effect_id)
        if effect is None:
            errors.append(f"{axis_label}.aggregate_effect_id is unknown")
            continue
        if effect.get("region_id") != region_id or effect.get("axis") != axis:
            errors.append(
                f"{axis_label}.aggregate_effect_id must match the same region and displayed-tone axis"
            )
        if axis_spec.get("role") == "primary" and effect.get("role") != "primary":
            errors.append(
                f"{axis_label}: a primary displayed-tone axis requires a primary aggregate effect"
            )

    color_claim_ids = color_contract.get("claim_ids")
    if not _nonempty_strings(color_claim_ids):
        errors.append(
            "color_tone_contract.claim_ids must contain emitted color/tone claims"
        )
        color_claim_ids = []
    listed_claim_ids = set(color_claim_ids)
    unknown_claims = sorted(listed_claim_ids - set(claim_map))
    if unknown_claims:
        errors.append(
            "color_tone_contract.claim_ids references unknown claims: "
            + ", ".join(unknown_claims)
        )
    unlisted_effect_claims = sorted(claims_with_effects - listed_claim_ids)
    if unlisted_effect_claims:
        errors.append(
            "claims with perceptual_effects missing from color_tone_contract.claim_ids: "
            + ", ".join(unlisted_effect_claims)
        )

    observed_effect_claims: dict[str, set[str]] = {}
    observed_effect_layers: dict[str, list[str]] = {}
    for claim_id in sorted(listed_claim_ids & set(claim_map)):
        claim = claim_map[claim_id]
        if not claim.get("emit"):
            errors.append(f"{claim_id}: color/tone contract may reference only emitted claims")
        effects = claim.get("perceptual_effects")
        if not isinstance(effects, list) or not effects:
            errors.append(f"{claim_id}: perceptual_effects must be a non-empty list")
            continue
        for index, effect_ref in enumerate(effects):
            label = f"{claim_id}.perceptual_effects[{index}]"
            if not isinstance(effect_ref, dict):
                errors.append(f"{label} must be an object")
                continue
            effect_id = effect_ref.get("aggregate_effect_id")
            if effect_id not in aggregate_map:
                errors.append(f"{label}.aggregate_effect_id is unknown")
                continue
            layer = effect_ref.get("causal_layer")
            if layer not in VALID_COLOR_CAUSAL_LAYERS:
                errors.append(f"{label}.causal_layer is invalid")
                continue
            confidence = effect_ref.get("confidence")
            if confidence not in VALID_COLOR_CONFIDENCE:
                errors.append(f"{label}.confidence is invalid")
            if not _nonempty_strings(effect_ref.get("source_evidence")):
                errors.append(f"{label}.source_evidence must contain visible evidence")

            aggregate = aggregate_map[effect_id]
            if (
                layer == "hierarchy"
                and aggregate.get("axis") == "hue"
                and effect_ref.get("hue_contrast_invariant") is not True
            ):
                errors.append(
                    f"{label}: hierarchy may carry hue only when hue_contrast_invariant is true"
                )
            if (
                layer == "global-cast"
                and neutral_status == "unavailable"
                and confidence == "high"
            ):
                errors.append(
                    f"{label}: high-confidence global cast requires more than unavailable neutral evidence"
                )
            observed_effect_claims.setdefault(effect_id, set()).add(claim_id)
            observed_effect_layers.setdefault(effect_id, []).append(layer)

    for effect_id, effect in aggregate_map.items():
        declared_claims = set(effect.get("claim_ids", []))
        unknown = sorted(declared_claims - set(claim_map))
        if unknown:
            errors.append(
                f"aggregate effect {effect_id!r} references unknown claims: {', '.join(unknown)}"
            )
        observed_claims = observed_effect_claims.get(effect_id, set())
        if declared_claims != observed_claims:
            errors.append(
                f"aggregate effect {effect_id!r} claim_ids must match claims that reference it"
            )
        layers = observed_effect_layers.get(effect_id, [])
        if len(layers) != len(set(layers)):
            errors.append(
                f"aggregate effect {effect_id!r} repeats one causal layer across emitted claims"
            )
        if len(set(layers)) > 1 and effect.get("source_supported") is not True:
            errors.append(
                f"aggregate effect {effect_id!r} spans causal layers without source support"
            )
        if effect.get("source_supported") is False and observed_claims:
            errors.append(
                f"aggregate effect {effect_id!r} is unsupported but contains emitted claims"
            )

    emitted_controls = color_contract.get("emitted_controls")
    if not isinstance(emitted_controls, list) or not emitted_controls:
        errors.append(
            "color_tone_contract.emitted_controls must contain exact final-prompt controls"
        )
        emitted_controls = []

    control_ids: set[str] = set()
    prompt_excerpts: set[str] = set()
    controlled_claim_counts: dict[str, int] = {}
    axis_control_effects: set[str] = set()
    intrinsic_axis_control_effects: set[str] = set()
    for index, control in enumerate(emitted_controls):
        label = f"color_tone_contract.emitted_controls[{index}]"
        if not isinstance(control, dict):
            errors.append(f"{label} must be an object")
            continue

        control_id = control.get("id")
        if not _nonempty_string(control_id):
            errors.append(f"{label}.id must be non-empty")
        elif control_id in control_ids:
            errors.append(f"duplicate emitted color control id: {control_id}")
        else:
            control_ids.add(control_id)

        prompt_excerpt = control.get("prompt_excerpt")
        if not _nonempty_string(prompt_excerpt):
            errors.append(f"{label}.prompt_excerpt must be non-empty")
        else:
            normalized_excerpt = prompt_excerpt.strip()
            if normalized_excerpt in prompt_excerpts:
                errors.append(
                    f"duplicate emitted color control excerpt: {normalized_excerpt!r}"
                )
            prompt_excerpts.add(normalized_excerpt)

        claim_id = control.get("claim_id")
        if not _nonempty_string(claim_id) or claim_id not in listed_claim_ids:
            errors.append(f"{label}.claim_id must reference a listed color/tone claim")
            continue
        controlled_claim_counts[claim_id] = controlled_claim_counts.get(claim_id, 0) + 1

        layer = control.get("causal_layer")
        if not isinstance(layer, str) or layer not in VALID_COLOR_CAUSAL_LAYERS:
            errors.append(f"{label}.causal_layer is invalid")

        control_role = control.get("control_role")
        if control_role not in VALID_COLOR_CONTROL_ROLES:
            errors.append(f"{label}.control_role is invalid")

        effect_ids = control.get("aggregate_effect_ids")
        if not _nonempty_strings(effect_ids):
            errors.append(f"{label}.aggregate_effect_ids must be non-empty")
            effect_ids = []
        elif len(effect_ids) != len(set(effect_ids)):
            errors.append(f"{label}.aggregate_effect_ids contains duplicates")
        unknown_effect_ids = sorted(set(effect_ids) - set(aggregate_map))
        if unknown_effect_ids:
            errors.append(
                f"{label}.aggregate_effect_ids references unknown effects: "
                + ", ".join(unknown_effect_ids)
            )

        claim = claim_map.get(claim_id)
        if not claim:
            continue
        claim_effects = claim.get("perceptual_effects")
        if not isinstance(claim_effects, list):
            continue
        expected_effect_ids = {
            ref.get("aggregate_effect_id")
            for ref in claim_effects
            if isinstance(ref, dict) and ref.get("aggregate_effect_id") in aggregate_map
        }
        expected_layers = {
            ref.get("causal_layer")
            for ref in claim_effects
            if isinstance(ref, dict) and ref.get("causal_layer") in VALID_COLOR_CAUSAL_LAYERS
        }
        if set(effect_ids) != expected_effect_ids:
            errors.append(
                f"{label}.aggregate_effect_ids must exactly match the claim's perceptual effects"
            )
        if expected_layers != {layer}:
            errors.append(
                f"{label} must represent exactly one causal layer matching its claim"
            )

        resolved_effects = [
            aggregate_map[effect_id]
            for effect_id in effect_ids
            if effect_id in aggregate_map
        ]
        if control_role == "axis-control":
            region_id = control.get("region_id")
            axis = control.get("axis")
            if region_id not in known_regions:
                errors.append(f"{label}.region_id references an unknown region")
            if axis not in VALID_COLOR_AXES:
                errors.append(f"{label}.axis is invalid")
            if any(
                effect.get("region_id") != region_id or effect.get("axis") != axis
                for effect in resolved_effects
            ):
                errors.append(
                    f"{label}: an axis-control may reference only one matching region and axis"
                )
            axis_control_effects.update(effect_ids)
            if layer == "intrinsic":
                intrinsic_axis_control_effects.update(effect_ids)
            if axis in VALID_DISPLAYED_TONE_AXES and layer not in DISPLAYED_TONE_ALLOWED_LAYERS[axis]:
                errors.append(
                    f"{label}: {axis} cannot be owned by causal layer {layer!r}"
                )
        elif control_role == "compound-control":
            if not _nonempty_string(control.get("compound_justification")):
                errors.append(
                    f"{label}.compound_justification is required for a compound-control"
                )
            effect_signatures = {
                (effect.get("region_id"), effect.get("axis"))
                for effect in resolved_effects
            }
            if len(effect_signatures) < 2:
                errors.append(
                    f"{label}: use axis-control when a control affects only one region and axis"
                )

    for claim_id in sorted(listed_claim_ids & set(claim_map)):
        count = controlled_claim_counts.get(claim_id, 0)
        if count != 1:
            errors.append(
                f"color/tone claim {claim_id!r} must have exactly one emitted final-prompt control"
            )

    for _region_id, _axis, axis_label, axis_spec in axis_requirements:
        if axis_spec.get("emission") != "required":
            continue
        effect_id = axis_spec.get("aggregate_effect_id")
        if effect_id not in intrinsic_axis_control_effects:
            errors.append(
                f"{axis_label}: required intrinsic axis needs its own intrinsic axis-control"
            )

    for _region_id, _axis, axis_label, axis_spec in displayed_tone_requirements:
        if axis_spec.get("emission") != "required":
            continue
        effect_id = axis_spec.get("aggregate_effect_id")
        if effect_id not in axis_control_effects:
            errors.append(
                f"{axis_label}: required displayed-tone axis needs its own axis-control"
            )

    compatible_friendly_labels: set[str] = set()
    surface_language = color_contract.get("surface_color_language")
    if surface_language is not None:
        if not isinstance(surface_language, dict):
            errors.append("color_tone_contract.surface_color_language must be an object")
            surface_language = {}
        if not _nonempty_string(surface_language.get("policy_id")):
            errors.append("color_tone_contract.surface_color_language.policy_id must be non-empty")
        if surface_language.get("policy_status") not in VALID_SURFACE_LANGUAGE_POLICY_STATUS:
            errors.append("color_tone_contract.surface_color_language.policy_status is invalid")
        if surface_language.get("observation_scope") != observation_scope:
            errors.append(
                "color_tone_contract.surface_color_language.observation_scope must match the Color/Tone contract"
            )
        if not _nonempty_string(surface_language.get("profile_status")):
            errors.append("color_tone_contract.surface_color_language.profile_status must be non-empty")
        if surface_language.get("region_id") not in known_regions:
            errors.append(
                "color_tone_contract.surface_color_language.region_id references an unknown region"
            )
        if not _nonempty_strings(surface_language.get("source_evidence")):
            errors.append(
                "color_tone_contract.surface_color_language.source_evidence must contain measurement or visible evidence"
            )

        classifications = surface_language.get("axis_classification")
        if not isinstance(classifications, dict):
            errors.append(
                "color_tone_contract.surface_color_language.axis_classification must be an object"
            )
            classifications = {}
        valid_terms = {
            "value_depth": VALID_SURFACE_VALUE_DEPTH,
            "chroma": VALID_SURFACE_CHROMA,
            "undertone": VALID_SURFACE_UNDERTONES,
            "finish": VALID_SURFACE_FINISH,
            "evenness": VALID_SURFACE_EVENNESS,
        }
        for axis, terms in valid_terms.items():
            axis_label = f"color_tone_contract.surface_color_language.axis_classification.{axis}"
            axis_spec = classifications.get(axis)
            if not isinstance(axis_spec, dict):
                errors.append(f"{axis_label} must be an object")
                continue
            if axis_spec.get("term") not in terms:
                errors.append(f"{axis_label}.term is invalid")
            if axis_spec.get("confidence") not in VALID_COLOR_CONFIDENCE:
                errors.append(f"{axis_label}.confidence is invalid")

        reviews = surface_language.get("friendly_label_review", [])
        if not isinstance(reviews, list):
            errors.append(
                "color_tone_contract.surface_color_language.friendly_label_review must be a list"
            )
            reviews = []
        seen_phrases: set[str] = set()
        required_scope_axes = {
            "value-depth": {"value_depth"},
            "undertone": {"undertone"},
            "surface-finish": {"finish"},
            "composite-appearance": {"value_depth", "chroma", "undertone"},
        }
        for index, review in enumerate(reviews):
            label = (
                "color_tone_contract.surface_color_language."
                f"friendly_label_review[{index}]"
            )
            if not isinstance(review, dict):
                errors.append(f"{label} must be an object")
                continue
            phrase = review.get("phrase")
            if not _nonempty_string(phrase):
                errors.append(f"{label}.phrase must be non-empty")
                continue
            phrase = phrase.strip()
            if phrase in seen_phrases:
                errors.append(f"{label}.phrase is duplicated")
            seen_phrases.add(phrase)
            candidate_source = review.get("candidate_source")
            if not isinstance(candidate_source, dict):
                errors.append(f"{label}.candidate_source must be an object")
            else:
                if candidate_source.get("kind") not in VALID_FRIENDLY_LABEL_SOURCES:
                    errors.append(f"{label}.candidate_source.kind is invalid")
                if not _nonempty_string(candidate_source.get("reference")):
                    errors.append(f"{label}.candidate_source.reference must be non-empty")
            scope = review.get("label_scope")
            if scope not in VALID_FRIENDLY_LABEL_SCOPES:
                errors.append(f"{label}.label_scope is invalid")
                continue
            requirements = review.get("axis_requirements")
            if not isinstance(requirements, dict) or not requirements:
                errors.append(f"{label}.axis_requirements must be a non-empty object")
                continue
            unknown_axes = sorted(set(requirements) - set(valid_terms))
            if unknown_axes:
                errors.append(
                    f"{label}.axis_requirements contains unknown axes: {', '.join(unknown_axes)}"
                )
            missing_scope_axes = required_scope_axes[scope] - set(requirements)
            if scope == "composite-appearance" and not ({"finish", "evenness"} & set(requirements)):
                missing_scope_axes.add("finish-or-evenness")
            if missing_scope_axes:
                errors.append(
                    f"{label}.axis_requirements does not support its label scope: "
                    + ", ".join(sorted(missing_scope_axes))
                )

            expected_matched: set[str] = set()
            expected_conflicting: set[str] = set()
            expected_unresolved: set[str] = set()
            for axis, allowed in requirements.items():
                if axis not in valid_terms:
                    continue
                if not isinstance(allowed, list) or not allowed or not all(
                    isinstance(item, str) and item in valid_terms[axis] for item in allowed
                ):
                    errors.append(f"{label}.axis_requirements.{axis} contains invalid terms")
                    continue
                axis_spec = classifications.get(axis, {})
                term = axis_spec.get("term") if isinstance(axis_spec, dict) else None
                confidence = axis_spec.get("confidence") if isinstance(axis_spec, dict) else None
                if term == "uncertain" or confidence == "low":
                    expected_unresolved.add(axis)
                elif term in allowed:
                    expected_matched.add(axis)
                else:
                    expected_conflicting.add(axis)

            reported_sets: dict[str, set[str]] = {}
            for field in ("matched_axes", "conflicting_axes", "unresolved_axes"):
                value = review.get(field, [])
                if not _string_list(value):
                    errors.append(f"{label}.{field} must be a list of strings")
                    value = []
                reported_sets[field] = set(value)
            expected_sets = {
                "matched_axes": expected_matched,
                "conflicting_axes": expected_conflicting,
                "unresolved_axes": expected_unresolved,
            }
            if reported_sets != expected_sets:
                errors.append(f"{label} axis review does not match the classified evidence")
            expected_status = (
                "conflicting"
                if expected_conflicting
                else "inconclusive"
                if expected_unresolved
                else "compatible"
            )
            if review.get("review_status") not in VALID_FRIENDLY_LABEL_REVIEWS:
                errors.append(f"{label}.review_status is invalid")
            elif review.get("review_status") != expected_status:
                errors.append(f"{label}.review_status does not match its axis review")
            if expected_status == "compatible":
                compatible_friendly_labels.add(phrase)

    appearance_metaphors = color_contract.get("appearance_metaphors", [])
    if not isinstance(appearance_metaphors, list):
        errors.append("color_tone_contract.appearance_metaphors must be a list")
        appearance_metaphors = []
    for index, metaphor in enumerate(appearance_metaphors):
        label = f"color_tone_contract.appearance_metaphors[{index}]"
        if not isinstance(metaphor, dict):
            errors.append(f"{label} must be an object")
            continue
        if not _nonempty_string(metaphor.get("phrase")):
            errors.append(f"{label}.phrase must be non-empty")
        status = metaphor.get("status")
        if status not in VALID_APPEARANCE_METAPHOR_STATUS:
            errors.append(f"{label}.status is invalid")
        emit = metaphor.get("emit")
        if not isinstance(emit, bool):
            errors.append(f"{label}.emit must be boolean")
        if emit and status != "model-calibrated":
            errors.append(
                f"{label}: only a model-calibrated appearance metaphor may be emitted"
            )
        if emit and not _nonempty_strings(metaphor.get("calibration_evidence")):
            errors.append(
                f"{label}.calibration_evidence is required for an emitted metaphor"
            )
        metaphor_phrase = metaphor.get("phrase")
        if emit and (
            not _nonempty_string(metaphor_phrase)
            or metaphor_phrase.strip() not in compatible_friendly_labels
        ):
            errors.append(
                f"{label}: an emitted friendly label requires a compatible surface-color-language review"
            )
        decomposed_ids = metaphor.get("decomposed_control_ids", [])
        if not isinstance(decomposed_ids, list) or not all(
            _nonempty_string(item) for item in decomposed_ids
        ):
            errors.append(f"{label}.decomposed_control_ids must be strings")
        unknown_controls = sorted(set(decomposed_ids) - control_ids)
        if unknown_controls:
            errors.append(
                f"{label}.decomposed_control_ids references unknown controls: "
                + ", ".join(unknown_controls)
            )

    return errors


def _audit_light_form_contract(
    contract: dict[str, Any],
    claim_map: dict[str, dict[str, Any]],
    major_region_ids: set[str],
) -> list[str]:
    """Validate the optional source-relative lighting decision contract."""

    errors: list[str] = []
    light_contract = contract.get("light_form_contract")
    claims_with_effects = {
        claim_id
        for claim_id, claim in claim_map.items()
        if isinstance(claim.get("lighting_effects"), list)
        and bool(claim["lighting_effects"])
    }
    if light_contract is None:
        if claims_with_effects:
            errors.append(
                "candidate claims with lighting_effects require light_form_contract"
            )
        return errors
    if not isinstance(light_contract, dict):
        return ["light_form_contract must be an object"]

    importance = light_contract.get("importance")
    if importance not in VALID_LIGHT_IMPORTANCE:
        errors.append(
            "light_form_contract.importance must be one of "
            f"{sorted(VALID_LIGHT_IMPORTANCE)}"
        )
    scope = light_contract.get("observation_scope")
    if scope not in VALID_LIGHT_OBSERVATION_SCOPES:
        errors.append(
            "light_form_contract.observation_scope must be one of "
            f"{sorted(VALID_LIGHT_OBSERVATION_SCOPES)}"
        )

    observed = light_contract.get("observed_result")
    if not isinstance(observed, dict):
        errors.append("light_form_contract.observed_result must be an object")
        observed = {}
    for field in ("global_tonal_range", "gradient_character"):
        if not _nonempty_string(observed.get(field)):
            errors.append(
                f"light_form_contract.observed_result.{field} must be non-empty"
            )
    if observed.get("local_form_contrast") not in VALID_LIGHT_FORM_CONTRAST:
        errors.append(
            "light_form_contract.observed_result.local_form_contrast is invalid"
        )
    observed_enums = (
        ("bright_plane_coverage", VALID_LIGHT_BRIGHT_COVERAGE),
        ("gradient_extent", VALID_LIGHT_GRADIENT_EXTENT),
        ("background_spill_relation", VALID_LIGHT_BACKGROUND_SPILL),
    )
    for field, allowed in observed_enums:
        if observed.get(field) not in allowed:
            errors.append(
                f"light_form_contract.observed_result.{field} is invalid"
            )
    for field in ("largest_bright_masses", "largest_dark_masses"):
        value = observed.get(field, [])
        if not _string_list(value):
            errors.append(
                f"light_form_contract.observed_result.{field} must be a list of strings"
            )
        elif importance == "primary" and not value:
            errors.append(
                f"light_form_contract.observed_result.{field} must record primary massing"
            )
    if not _nonempty_strings(observed.get("source_evidence")):
        errors.append(
            "light_form_contract.observed_result.source_evidence must contain visible evidence"
        )

    hypothesis = light_contract.get("source_hypothesis")
    if not isinstance(hypothesis, dict):
        errors.append("light_form_contract.source_hypothesis must be an object")
        hypothesis = {}
    hypothesis_fields = (
        ("model_type", VALID_LIGHT_MODEL_TYPES),
        ("source_count", VALID_LIGHT_SOURCE_COUNTS),
        ("camera_axis_offset", VALID_LIGHT_AXIS_OFFSETS),
        ("elevation", VALID_LIGHT_ELEVATIONS),
        ("apparent_angular_size", VALID_LIGHT_SOURCE_SIZES),
        ("fill_structure", VALID_LIGHT_FILL_STRUCTURES),
        ("confidence", VALID_COLOR_CONFIDENCE),
        ("actuation", VALID_LIGHT_ACTUATIONS),
    )
    for field, allowed in hypothesis_fields:
        if hypothesis.get(field) not in allowed:
            errors.append(f"light_form_contract.source_hypothesis.{field} is invalid")
    if not _nonempty_string(hypothesis.get("front_side_back_relation")):
        errors.append(
            "light_form_contract.source_hypothesis.front_side_back_relation must be non-empty"
        )
    if not _nonempty_strings(hypothesis.get("source_evidence")):
        errors.append(
            "light_form_contract.source_hypothesis.source_evidence must contain visible evidence"
        )
    if hypothesis.get("confidence") == "low" and hypothesis.get("actuation") in {
        "physical-cause",
        "physical-plus-result",
    }:
        errors.append(
            "a low-confidence source hypothesis cannot emit a physical-light cause"
        )

    known_regions = major_region_ids | {"global"}
    region_effects = light_contract.get("region_effects", [])
    if not isinstance(region_effects, list):
        errors.append("light_form_contract.region_effects must be a list")
        region_effects = []
    if importance == "primary" and not region_effects:
        errors.append(
            "a primary light_form_contract must contain observed region effects"
        )
    region_effect_ids: set[str] = set()
    spill_region_count = 0
    region_effect_roles: set[str] = set()
    for index, effect in enumerate(region_effects):
        label = f"light_form_contract.region_effects[{index}]"
        if not isinstance(effect, dict):
            errors.append(f"{label} must be an object")
            continue
        effect_id = effect.get("id")
        if not _nonempty_string(effect_id):
            errors.append(f"{label}.id must be non-empty")
        elif effect_id in region_effect_ids:
            errors.append(f"duplicate observed lighting region effect id: {effect_id}")
        else:
            region_effect_ids.add(effect_id)
        if effect.get("region_id") not in known_regions:
            errors.append(f"{label}.region_id references an unknown region")
        if effect.get("role") not in VALID_LIGHT_REGION_EFFECT_ROLES:
            errors.append(f"{label}.role is invalid")
        else:
            region_effect_roles.add(str(effect.get("role")))
            if effect.get("role") == "spill":
                spill_region_count += 1
        if not _nonempty_string(effect.get("value_relation")):
            errors.append(f"{label}.value_relation must be non-empty")
        if effect.get("gradient_strength") not in VALID_STRENGTHS:
            errors.append(f"{label}.gradient_strength is invalid")
        if not _nonempty_string(effect.get("edge_character")):
            errors.append(f"{label}.edge_character must be non-empty")
        if not _nonempty_strings(effect.get("source_evidence")):
            errors.append(f"{label}.source_evidence must contain visible evidence")

    shadow_events = light_contract.get("shadow_events", [])
    if not isinstance(shadow_events, list):
        errors.append("light_form_contract.shadow_events must be a list")
        shadow_events = []
    shadow_ids: set[str] = set()
    for index, shadow in enumerate(shadow_events):
        label = f"light_form_contract.shadow_events[{index}]"
        if not isinstance(shadow, dict):
            errors.append(f"{label} must be an object")
            continue
        shadow_id = shadow.get("id")
        if not _nonempty_string(shadow_id):
            errors.append(f"{label}.id must be non-empty")
        elif shadow_id in shadow_ids:
            errors.append(f"duplicate shadow event id: {shadow_id}")
        else:
            shadow_ids.add(shadow_id)
        if shadow.get("region_id") not in known_regions:
            errors.append(f"{label}.region_id references an unknown region")
        if shadow.get("owner") not in VALID_SHADOW_OWNERS:
            errors.append(f"{label}.owner is invalid")
        if not _nonempty_string(shadow.get("footprint")):
            errors.append(f"{label}.footprint must be non-empty")
        if not _nonempty_string(shadow.get("edge_character")):
            errors.append(f"{label}.edge_character must be non-empty")
        if shadow.get("confidence") not in VALID_COLOR_CONFIDENCE:
            errors.append(f"{label}.confidence is invalid")
        if not _nonempty_strings(shadow.get("source_evidence")):
            errors.append(f"{label}.source_evidence must contain visible evidence")

    material_responses = light_contract.get("material_responses", [])
    if not isinstance(material_responses, list):
        errors.append("light_form_contract.material_responses must be a list")
        material_responses = []
    material_region_ids: set[str] = set()
    for index, material in enumerate(material_responses):
        label = f"light_form_contract.material_responses[{index}]"
        if not isinstance(material, dict):
            errors.append(f"{label} must be an object")
            continue
        region_id = material.get("region_id")
        if region_id not in known_regions:
            errors.append(f"{label}.region_id references an unknown region")
        elif region_id in material_region_ids:
            errors.append(f"duplicate material-light response region: {region_id}")
        else:
            material_region_ids.add(region_id)
        if material.get("response") not in VALID_LIGHT_MATERIAL_RESPONSES:
            errors.append(f"{label}.response is invalid")
        for field in ("highlight_width", "highlight_strength", "black_level_behavior"):
            if not _nonempty_string(material.get(field)):
                errors.append(f"{label}.{field} must be non-empty")
        if not _nonempty_strings(material.get("source_evidence")):
            errors.append(f"{label}.source_evidence must contain visible evidence")

    pose_dependency = light_contract.get("pose_light_dependency")
    if not isinstance(pose_dependency, dict):
        errors.append("light_form_contract.pose_light_dependency must be an object")
        pose_dependency = {}
    geometry_dependency = pose_dependency.get("geometry_dependency")
    if geometry_dependency not in VALID_LIGHT_GEOMETRY_DEPENDENCIES:
        errors.append(
            "light_form_contract.pose_light_dependency.geometry_dependency is invalid"
        )
    if not _nonempty_string(pose_dependency.get("preserved_result")):
        errors.append(
            "light_form_contract.pose_light_dependency.preserved_result must be non-empty"
        )
    flexible_effects = pose_dependency.get("flexible_effects", [])
    if not _string_list(flexible_effects):
        errors.append(
            "light_form_contract.pose_light_dependency.flexible_effects must be a list of strings"
        )
    elif geometry_dependency in {"pose-robust", "mixed"} and not flexible_effects:
        errors.append(
            "pose-robust or mixed lighting must name flexible light effects"
        )
    if not _nonempty_strings(pose_dependency.get("source_evidence")):
        errors.append(
            "light_form_contract.pose_light_dependency.source_evidence must contain visible evidence"
        )

    aggregate_effects = light_contract.get("aggregate_effects")
    if not isinstance(aggregate_effects, list) or not aggregate_effects:
        errors.append(
            "light_form_contract.aggregate_effects must contain at least one source target"
        )
        aggregate_effects = []
    aggregate_map: dict[str, dict[str, Any]] = {}
    aggregate_signatures: dict[tuple[str, str, str], str] = {}
    primary_effect_count = 0
    effect_axes: set[str] = set()
    for index, effect in enumerate(aggregate_effects):
        label = f"light_form_contract.aggregate_effects[{index}]"
        if not isinstance(effect, dict):
            errors.append(f"{label} must be an object")
            continue
        effect_id = effect.get("id")
        if not _nonempty_string(effect_id):
            errors.append(f"{label}.id must be non-empty")
            continue
        if effect_id in aggregate_map:
            errors.append(f"duplicate aggregate lighting effect id: {effect_id}")
        aggregate_map[str(effect_id)] = effect
        axis = effect.get("axis")
        if axis not in VALID_LIGHT_EFFECT_AXES:
            errors.append(f"{label}.axis is invalid")
        else:
            effect_axes.add(str(axis))
        direction = effect.get("direction")
        if not _nonempty_string(direction):
            errors.append(f"{label}.direction must be non-empty")
        region_id = effect.get("region_id")
        if region_id not in known_regions:
            errors.append(f"{label}.region_id references an unknown region")
        if (
            axis in VALID_LIGHT_EFFECT_AXES
            and _nonempty_string(direction)
            and region_id in known_regions
        ):
            normalized_direction = "-".join(
                direction.casefold().replace("_", " ").replace("-", " ").split()
            )
            signature = (str(region_id), str(axis), normalized_direction)
            previous = aggregate_signatures.get(signature)
            if previous is not None:
                errors.append(
                    f"aggregate lighting effects {previous!r} and {effect_id!r} split one region/axis/direction"
                )
            else:
                aggregate_signatures[signature] = str(effect_id)
        if effect.get("role") not in VALID_INVARIANT_ROLES:
            errors.append(f"{label}.role is invalid")
        elif effect.get("role") == "primary":
            primary_effect_count += 1
        if effect.get("target_strength") not in VALID_STRENGTHS:
            errors.append(f"{label}.target_strength is invalid")
        if not isinstance(effect.get("source_supported"), bool):
            errors.append(f"{label}.source_supported must be boolean")
        if not _nonempty_strings(effect.get("source_evidence")):
            errors.append(f"{label}.source_evidence must contain visible evidence")
        if not _nonempty_strings(effect.get("claim_ids")):
            errors.append(f"{label}.claim_ids must contain emitted lighting claims")
    if importance == "primary" and primary_effect_count == 0:
        errors.append(
            "a primary light_form_contract must contain a primary aggregate effect"
        )

    actuation = hypothesis.get("actuation")
    physical_axes = effect_axes & {"source-geometry", "fill"}
    result_axes = effect_axes - {"source-geometry", "fill"}
    if actuation == "physical-cause" and "source-geometry" not in effect_axes:
        errors.append("physical-cause actuation requires a source-geometry effect")
    if actuation == "physical-plus-result" and (
        "source-geometry" not in effect_axes or not result_axes
    ):
        errors.append(
            "physical-plus-result actuation requires source geometry and a result-space effect"
        )
    if actuation in {"result-space-only", "diagnostic-only"} and physical_axes:
        errors.append(
            f"{actuation} actuation cannot emit source-geometry or fill effects"
        )
    if "fill" in effect_axes and hypothesis.get("fill_structure") == "uncertain":
        errors.append("an emitted fill effect requires a source-supported fill structure")
    if "shadow-topology" in effect_axes and not shadow_events:
        errors.append("a shadow-topology effect requires at least one shadow event")
    if "material-response" in effect_axes and not material_responses:
        errors.append("a material-response effect requires observed material response")
    if "background-spill" in effect_axes and spill_region_count == 0:
        errors.append("a background-spill effect requires an observed spill region")
    if "bright-plane-coverage" in effect_axes and "broad-plane" not in region_effect_roles:
        errors.append(
            "a bright-plane-coverage effect requires an observed broad-plane region"
        )
    if "gradient-extent" in effect_axes and "gradient" not in region_effect_roles:
        errors.append(
            "a gradient-extent effect requires an observed gradient region"
        )

    light_claim_ids = light_contract.get("claim_ids")
    if not _nonempty_strings(light_claim_ids):
        errors.append(
            "light_form_contract.claim_ids must contain emitted lighting claims"
        )
        light_claim_ids = []
    listed_claim_ids = set(light_claim_ids)
    unknown_claims = sorted(listed_claim_ids - set(claim_map))
    if unknown_claims:
        errors.append(
            "light_form_contract.claim_ids references unknown claims: "
            + ", ".join(unknown_claims)
        )
    unlisted_effect_claims = sorted(claims_with_effects - listed_claim_ids)
    if unlisted_effect_claims:
        errors.append(
            "claims with lighting_effects missing from light_form_contract.claim_ids: "
            + ", ".join(unlisted_effect_claims)
        )

    observed_effect_claims: dict[str, set[str]] = {}
    for claim_id in sorted(listed_claim_ids & set(claim_map)):
        claim = claim_map[claim_id]
        if not claim.get("emit"):
            errors.append(f"{claim_id}: Light/Form contract may reference only emitted claims")
        effects = claim.get("lighting_effects")
        if not isinstance(effects, list) or not effects:
            errors.append(f"{claim_id}: lighting_effects must be a non-empty list")
            continue
        for index, effect_ref in enumerate(effects):
            label = f"{claim_id}.lighting_effects[{index}]"
            if not isinstance(effect_ref, dict):
                errors.append(f"{label} must be an object")
                continue
            effect_id = effect_ref.get("aggregate_effect_id")
            if effect_id not in aggregate_map:
                errors.append(f"{label}.aggregate_effect_id is unknown")
                continue
            if effect_ref.get("confidence") not in VALID_COLOR_CONFIDENCE:
                errors.append(f"{label}.confidence is invalid")
            if not _nonempty_strings(effect_ref.get("source_evidence")):
                errors.append(f"{label}.source_evidence must contain visible evidence")
            observed_effect_claims.setdefault(str(effect_id), set()).add(claim_id)

    for effect_id, effect in aggregate_map.items():
        declared_claims = set(effect.get("claim_ids", []))
        unknown = sorted(declared_claims - listed_claim_ids)
        if unknown:
            errors.append(
                f"aggregate lighting effect {effect_id!r} references unlisted claims: "
                + ", ".join(unknown)
            )
        observed = observed_effect_claims.get(effect_id, set())
        if declared_claims != observed:
            errors.append(
                f"aggregate lighting effect {effect_id!r} claim_ids do not match lighting_effects references"
            )

    controls = light_contract.get("emitted_controls")
    if not isinstance(controls, list) or not controls:
        errors.append(
            "light_form_contract.emitted_controls must contain exact final-prompt controls"
        )
        controls = []
    control_ids: set[str] = set()
    prompt_excerpts: set[str] = set()
    controlled_claim_counts: dict[str, int] = {}
    for index, control in enumerate(controls):
        label = f"light_form_contract.emitted_controls[{index}]"
        if not isinstance(control, dict):
            errors.append(f"{label} must be an object")
            continue
        control_id = control.get("id")
        if not _nonempty_string(control_id):
            errors.append(f"{label}.id must be non-empty")
        elif control_id in control_ids:
            errors.append(f"duplicate emitted lighting control id: {control_id}")
        else:
            control_ids.add(str(control_id))
        excerpt = control.get("prompt_excerpt")
        if not _nonempty_string(excerpt):
            errors.append(f"{label}.prompt_excerpt must be non-empty")
        elif excerpt.strip() in prompt_excerpts:
            errors.append(f"duplicate emitted lighting control excerpt: {excerpt.strip()!r}")
        else:
            prompt_excerpts.add(excerpt.strip())
        claim_id = control.get("claim_id")
        if not _nonempty_string(claim_id) or claim_id not in listed_claim_ids:
            errors.append(f"{label}.claim_id must reference a listed lighting claim")
            continue
        controlled_claim_counts[str(claim_id)] = (
            controlled_claim_counts.get(str(claim_id), 0) + 1
        )
        owner = control.get("owner")
        if owner not in VALID_LIGHT_EFFECT_AXES:
            errors.append(f"{label}.owner is invalid")
        effect_ids = control.get("aggregate_effect_ids")
        if not _nonempty_strings(effect_ids):
            errors.append(f"{label}.aggregate_effect_ids must be non-empty")
            effect_ids = []
        elif len(effect_ids) != len(set(effect_ids)):
            errors.append(f"{label}.aggregate_effect_ids contains duplicates")
        unknown_effects = sorted(set(effect_ids) - set(aggregate_map))
        if unknown_effects:
            errors.append(
                f"{label}.aggregate_effect_ids references unknown effects: "
                + ", ".join(unknown_effects)
            )
        claim = claim_map.get(str(claim_id), {})
        claim_effects = claim.get("lighting_effects", [])
        expected_effect_ids = {
            ref.get("aggregate_effect_id")
            for ref in claim_effects
            if isinstance(ref, dict) and ref.get("aggregate_effect_id") in aggregate_map
        }
        if set(effect_ids) != expected_effect_ids:
            errors.append(
                f"{label}.aggregate_effect_ids must exactly match the claim's lighting effects"
            )
        resolved_axes = {
            aggregate_map[effect_id].get("axis")
            for effect_id in effect_ids
            if effect_id in aggregate_map
        }
        if resolved_axes != {owner}:
            errors.append(
                f"{label} must represent exactly one Light/Form owner matching its effects"
            )

    for claim_id in sorted(listed_claim_ids & set(claim_map)):
        count = controlled_claim_counts.get(claim_id, 0)
        if count != 1:
            errors.append(
                f"lighting claim {claim_id!r} must have exactly one emitted final-prompt control"
            )

    color_contract = contract.get("color_tone_contract")
    errors.extend(
        _audit_lighting_language(
            light_contract,
            color_contract if isinstance(color_contract, dict) else None,
            known_regions,
            control_ids,
        )
    )

    if isinstance(color_contract, dict):
        color_claim_ids = set(color_contract.get("claim_ids", []))
        overlap = sorted(listed_claim_ids & color_claim_ids)
        if overlap:
            errors.append(
                "Light/Form and Color/Tone contracts cannot own the same claims: "
                + ", ".join(overlap)
            )
        color_excerpts = {
            item.get("prompt_excerpt", "").strip()
            for item in color_contract.get("emitted_controls", [])
            if isinstance(item, dict) and _nonempty_string(item.get("prompt_excerpt"))
        }
        excerpt_overlap = sorted(prompt_excerpts & color_excerpts)
        if excerpt_overlap:
            errors.append(
                "Light/Form and Color/Tone contracts cannot own the same prompt excerpts"
            )

    return errors


def audit_plan(plan: dict[str, Any]) -> list[str]:
    """Return actionable contract errors for one salience plan."""

    errors: list[str] = []
    contract = _contract(plan)
    mode = contract.get("mode")
    if mode not in VALID_MODES:
        errors.append(f"mode must be one of {sorted(VALID_MODES)}")

    appeal = plan.get("direct_appeal_read", "")
    if not isinstance(appeal, str):
        errors.append("direct_appeal_read must be a string when present")

    invariants = contract.get("invariants")
    if not isinstance(invariants, list) or not invariants:
        errors.append("invariants must contain at least one source-supported entry")
        invariants = []

    invariant_ids: set[str] = set()
    invariant_map: dict[str, dict[str, Any]] = {}
    for index, invariant in enumerate(invariants):
        label = f"invariants[{index}]"
        if not isinstance(invariant, dict):
            errors.append(f"{label} must be an object")
            continue
        invariant_id = invariant.get("id")
        if not isinstance(invariant_id, str) or not invariant_id.strip():
            errors.append(f"{label}.id must be a non-empty string")
            continue
        if invariant_id in invariant_ids:
            errors.append(f"duplicate invariant id: {invariant_id}")
        invariant_ids.add(invariant_id)
        invariant_map[invariant_id] = invariant
        if invariant.get("axis") not in VALID_AXES:
            errors.append(f"{label}.axis is invalid")
        if invariant.get("role") not in VALID_INVARIANT_ROLES:
            errors.append(f"{label}.role is invalid")
        if (
            not isinstance(invariant.get("observation"), str)
            or not invariant["observation"].strip()
        ):
            errors.append(f"{label}.observation must be non-empty")
        if invariant.get("causal_origin") not in VALID_CAUSAL_ORIGINS:
            errors.append(f"{label}.causal_origin is invalid")
        if invariant.get("target_strength") not in VALID_STRENGTHS:
            errors.append(f"{label}.target_strength is invalid")
        if not _nonempty_strings(invariant.get("source_evidence")):
            errors.append(f"{label}.source_evidence must contain visible evidence")
        if (
            not isinstance(invariant.get("clause_owner"), str)
            or not invariant["clause_owner"].strip()
        ):
            errors.append(f"{label}.clause_owner must be non-empty")

    flexible = contract.get("flexible_dimensions", [])
    if not isinstance(flexible, list) or not all(
        isinstance(item, str) and item.strip() for item in flexible
    ):
        errors.append("flexible_dimensions must be a list of non-empty strings")
        flexible = []
    flexible_set = set(flexible)
    if len(flexible_set) != len(flexible):
        errors.append("flexible_dimensions contains duplicates")

    claims = contract.get("candidate_claims", contract.get("claims", []))
    if not isinstance(claims, list):
        errors.append("candidate_claims must be a list")
        claims = []

    claim_ids: set[str] = set()
    claim_map: dict[str, dict[str, Any]] = {}
    emitted_affirmative: dict[str, list[dict[str, Any]]] = {}
    emitted_boundaries: dict[str, list[dict[str, Any]]] = {}
    for index, claim in enumerate(claims):
        label = f"candidate_claims[{index}]"
        if not isinstance(claim, dict):
            errors.append(f"{label} must be an object")
            continue
        claim_id = claim.get("id")
        if not isinstance(claim_id, str) or not claim_id.strip():
            errors.append(f"{label}.id must be a non-empty string")
            continue
        if claim_id in claim_ids:
            errors.append(f"duplicate claim id: {claim_id}")
        claim_ids.add(claim_id)
        claim_map[claim_id] = claim

        slot = claim.get("semantic_slot")
        if not isinstance(slot, str) or not slot.strip():
            errors.append(f"{label}.semantic_slot must be non-empty")
            continue
        if not isinstance(claim.get("owner"), str) or not claim["owner"].strip():
            errors.append(f"{label}.owner must be non-empty")
        if claim.get("role") not in VALID_CLAIM_ROLES:
            errors.append(f"{label}.role is invalid")
        if claim.get("polarity") not in VALID_POLARITIES:
            errors.append(f"{label}.polarity is invalid")
        if claim.get("target_strength") not in VALID_STRENGTHS:
            errors.append(f"{label}.target_strength is invalid")
        if claim.get("source_kind") not in VALID_SOURCE_KINDS:
            errors.append(f"{label}.source_kind is invalid")
        if not _nonempty_strings(claim.get("source_evidence")):
            errors.append(f"{label}.source_evidence must contain visible evidence")
        if not isinstance(claim.get("emit"), bool):
            errors.append(f"{label}.emit must be boolean")
            continue
        if not claim["emit"]:
            continue
        if claim.get("source_kind") == "diagnostic-appeal":
            errors.append(
                f"{claim_id}: diagnostic appeal cannot be emitted as a render claim"
            )
        if slot in flexible_set and claim.get("role") == "primary":
            errors.append(
                f"{claim_id}: flexible dimension {slot!r} cannot be a primary claim"
            )
        if claim.get("polarity") == "affirmative":
            if claim.get("role") == "drift-boundary":
                errors.append(
                    f"{claim_id}: an affirmative claim cannot be a drift boundary"
                )
            emitted_affirmative.setdefault(slot, []).append(claim)
        else:
            if claim.get("role") != "drift-boundary" or claim.get("risk") != "high":
                errors.append(
                    f"{claim_id}: emitted negative claims must be high-risk drift boundaries"
                )
            emitted_boundaries.setdefault(slot, []).append(claim)

    for slot, slot_claims in emitted_affirmative.items():
        if len(slot_claims) > 1:
            errors.append(
                f"semantic slot {slot!r} has multiple emitted affirmative owners"
            )
    for slot, slot_claims in emitted_boundaries.items():
        if len(slot_claims) > 1:
            errors.append(
                f"semantic slot {slot!r} has multiple emitted drift boundaries"
            )

    for invariant_id, invariant in invariant_map.items():
        slot_claims = emitted_affirmative.get(invariant_id, [])
        if len(slot_claims) != 1:
            errors.append(
                f"invariant {invariant_id!r} must have exactly one emitted affirmative claim"
            )
            continue
        claim = slot_claims[0]
        if claim.get("owner") != invariant.get("clause_owner"):
            errors.append(
                f"invariant {invariant_id!r} claim owner does not match clause_owner"
            )
        if claim.get("target_strength") != invariant.get("target_strength"):
            errors.append(
                f"invariant {invariant_id!r} claim strength exceeds or changes its source target"
            )

    regions = contract.get("major_regions", [])
    if not isinstance(regions, list) or len(regions) < 2:
        errors.append(
            "major_regions must contain at least two comparative image regions"
        )
        regions = []
    region_ids: set[str] = set()
    for index, region in enumerate(regions):
        label = f"major_regions[{index}]"
        if not isinstance(region, dict):
            errors.append(f"{label} must be an object")
            continue
        region_id = region.get("id")
        if not isinstance(region_id, str) or not region_id.strip():
            errors.append(f"{label}.id must be non-empty")
        elif region_id in region_ids:
            errors.append(f"duplicate major region id: {region_id}")
        else:
            region_ids.add(region_id)
        if region.get("role") not in VALID_REGION_ROLES:
            errors.append(f"{label}.role is invalid")
        if region.get("relative_area") not in VALID_RELATIVE_AREAS:
            errors.append(f"{label}.relative_area is invalid")
        if region.get("attention") not in VALID_ATTENTION:
            errors.append(f"{label}.attention is invalid")
        if not _nonempty_strings(region.get("source_evidence")):
            errors.append(f"{label}.source_evidence must contain visible evidence")

    clusters = contract.get("prior_clusters", [])
    if not isinstance(clusters, list):
        errors.append("prior_clusters must be a list")
        clusters = []
    for index, cluster in enumerate(clusters):
        label = f"prior_clusters[{index}]"
        if not isinstance(cluster, dict):
            errors.append(f"{label} must be an object")
            continue
        members = cluster.get("claim_ids")
        if not isinstance(members, list) or not all(
            isinstance(item, str) for item in members
        ):
            errors.append(f"{label}.claim_ids must be a list of claim ids")
            continue
        unknown = sorted(set(members) - claim_ids)
        if unknown:
            errors.append(f"{label} references unknown claims: {', '.join(unknown)}")
        if not isinstance(cluster.get("source_supported"), bool):
            errors.append(f"{label}.source_supported must be boolean")
        elif not cluster["source_supported"] and any(
            bool(claim_map.get(claim_id, {}).get("emit")) for claim_id in members
        ):
            errors.append(f"{label}: unsupported prior cluster contains emitted claims")

    if any(
        isinstance(invariant, dict) and invariant.get("axis") == "color"
        for invariant in invariants
    ) and "color_tone_contract" not in contract:
        errors.append(
            "a color invariant requires a source-relative color_tone_contract"
        )
    errors.extend(_audit_color_tone_contract(contract, claim_map, region_ids))

    if any(
        isinstance(invariant, dict)
        and invariant.get("axis") == "light-to-form"
        and invariant.get("role") == "primary"
        for invariant in invariants
    ) and "light_form_contract" not in contract:
        errors.append(
            "a primary light-to-form invariant requires a source-relative light_form_contract"
        )
    errors.extend(_audit_light_form_contract(contract, claim_map, region_ids))

    return errors


def primary_signature(plan: dict[str, Any]) -> set[tuple[str, str, str]]:
    contract = _contract(plan)
    signature = {
        (str(item.get("id")), str(item.get("axis")), str(item.get("target_strength")))
        for item in contract.get("invariants", [])
        if isinstance(item, dict) and item.get("role") == "primary"
    }
    color_contract = contract.get("color_tone_contract")
    if isinstance(color_contract, dict):
        signature.update(
            (
                f"color-effect:{item.get('id')}",
                f"{item.get('axis')}:{item.get('region_id')}",
                f"{item.get('direction')}:{item.get('target_strength')}",
            )
            for item in color_contract.get("aggregate_effects", [])
            if isinstance(item, dict) and item.get("role") == "primary"
        )
    light_contract = contract.get("light_form_contract")
    if isinstance(light_contract, dict):
        signature.update(
            (
                f"light-effect:{item.get('id')}",
                f"{item.get('axis')}:{item.get('region_id')}",
                f"{item.get('direction')}:{item.get('target_strength')}",
            )
            for item in light_contract.get("aggregate_effects", [])
            if isinstance(item, dict) and item.get("role") == "primary"
        )
    return signature


def compare_plans(
    baseline: dict[str, Any],
    variant: dict[str, Any],
    relation: str,
) -> list[str]:
    """Check a matched pair without comparing generated wording."""

    errors = [f"baseline: {error}" for error in audit_plan(baseline)]
    errors.extend(f"variant: {error}" for error in audit_plan(variant))
    if errors:
        return errors

    baseline_signature = primary_signature(baseline)
    variant_signature = primary_signature(variant)
    if relation == "invariant-preserving":
        if baseline_signature != variant_signature:
            errors.append(
                "invariant-preserving pair changed the primary salience signature"
            )
    elif relation == "aesthetic-changing":
        if baseline_signature == variant_signature:
            errors.append(
                "aesthetic-changing pair retained an identical primary salience signature"
            )
    else:
        errors.append("relation must be invariant-preserving or aesthetic-changing")
    return errors


def _load_json(path: str) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return data


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", help="salience-plan JSON file")
    parser.add_argument("--compare", default="", help="matched variant plan JSON file")
    parser.add_argument(
        "--relation",
        choices=["invariant-preserving", "aesthetic-changing"],
        default="invariant-preserving",
    )
    args = parser.parse_args(argv)

    try:
        baseline = _load_json(args.plan)
        errors = (
            compare_plans(baseline, _load_json(args.compare), args.relation)
            if args.compare
            else audit_plan(baseline)
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors = [str(exc)]

    print(
        json.dumps(
            {"status": "ok" if not errors else "failed", "errors": errors}, indent=2
        )
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
