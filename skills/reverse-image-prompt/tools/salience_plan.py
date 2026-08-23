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
from color_language import compose_controlled_descriptor


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
VALID_GENERIC_EFFECT_AXES = VALID_AXES - {"color", "light-to-form"}
VALID_COMPONENT_RELATION_KINDS = {
    "frame-zone",
    "axis-offset",
    "principal-axis",
    "viewpoint",
    "part-whole-orientation",
    "attention-direction",
    "cross-component-orientation",
    "edge-contact",
    "overlap",
    "layer-order",
    "partial-visibility",
    "contact",
    "support",
    "containment",
    "boundary-crossing",
}
VALID_COMPONENT_RELATION_ROLES = {"primary", "supporting"}
VALID_FRAME_EDGES = {"top", "bottom", "left", "right"}
VALID_COMPLETION_RISKS = {"low", "medium", "high"}
VALID_SPATIAL_SUBJECT_KINDS = {"human", "non-human", "group", "component"}
VALID_SPATIAL_VISIBILITY = {"readable", "partial", "indistinct"}
VALID_SPATIAL_DISPOSITIONS = {
    "invariant",
    "flexible",
    "not-material",
    "not-visible",
    "uncertain",
}
VALID_SPATIAL_CONFIDENCE = {"high", "medium", "low"}
SPATIAL_DIMENSION_FAMILIES = {
    "frame-placement": "frame-placement",
    "subject-principal-axis": "principal-axis",
    "viewpoint-elevation": "viewpoint",
    "viewpoint-azimuth": "viewpoint",
    "viewpoint-roll": "viewpoint",
    "viewpoint-distance-foreshortening": "viewpoint",
    "human-body-orientation": "principal-axis",
    "human-head-body-relation": "part-whole",
    "human-shoulder-line": "part-whole",
    "human-attention-direction": "attention-direction",
    "cross-component-orientation": "cross-component",
}
BASE_SPATIAL_DIMENSIONS = {
    "frame-placement",
    "subject-principal-axis",
    "viewpoint-elevation",
    "viewpoint-azimuth",
    "viewpoint-roll",
    "viewpoint-distance-foreshortening",
    "cross-component-orientation",
}
HUMAN_SPATIAL_DIMENSIONS = {
    "human-body-orientation",
    "human-head-body-relation",
    "human-shoulder-line",
    "human-attention-direction",
}
SPATIAL_DIMENSION_ALLOWED_ORIGINS = {
    "frame-placement": {"spatial-relation", "layout"},
    "subject-principal-axis": {"spatial-relation", "pose-deformation", "layout"},
    "viewpoint-elevation": {"perspective"},
    "viewpoint-azimuth": {"perspective"},
    "viewpoint-roll": {"perspective"},
    "viewpoint-distance-foreshortening": {"perspective"},
    "human-body-orientation": {"pose-deformation"},
    "human-head-body-relation": {"pose-deformation"},
    "human-shoulder-line": {"pose-deformation"},
    "human-attention-direction": {"pose-deformation", "spatial-relation"},
    "cross-component-orientation": {"spatial-relation", "layout"},
}
VALID_GENERATION_PRIOR_SCOPES = {"person-gestalt", "attractiveness"}
VALID_GENERATION_PRIOR_SOURCES = {
    "user-supplied",
    "source-visible-approximation",
    "model-calibrated",
}
VALID_HUMAN_FACE_VISIBILITY = {
    "readable",
    "partial",
    "indistinct",
    "not-visible",
    "uncertain",
}
VALID_PERSON_PRIOR_DISPOSITIONS = {"emit", "omit", "uncertain"}
VALID_SKIN_SURFACE_DISPOSITIONS = {
    "material",
    "not-material",
    "not-visible",
    "uncertain",
}
VALID_SKIN_COVERAGE = {"exposed", "through-sheer", "mixed"}
VALID_DESCRIPTOR_DISPOSITIONS = {"emit", "omit", "uncertain"}
CONTROLLED_DESCRIPTOR_AXIS_TO_COLOR_AXIS = {
    "value_depth": "value",
    "chroma": "chroma",
    "undertone": "hue",
}
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


def _audit_generation_prior(claim: dict[str, Any], label: str) -> list[str]:
    """Validate an optional broad human generation prior without judging its phrase."""

    prior = claim.get("generation_prior")
    if prior is None:
        return []
    if not isinstance(prior, dict):
        return [f"{label}.generation_prior must be an object"]

    errors: list[str] = []
    prefix = f"{label}.generation_prior"
    if prior.get("scope") not in VALID_GENERATION_PRIOR_SCOPES:
        errors.append(f"{prefix}.scope is invalid")

    source = prior.get("candidate_source")
    if not isinstance(source, dict):
        errors.append(f"{prefix}.candidate_source must be an object")
    else:
        if source.get("kind") not in VALID_GENERATION_PRIOR_SOURCES:
            errors.append(f"{prefix}.candidate_source.kind is invalid")
        if not _nonempty_string(source.get("reference")):
            errors.append(f"{prefix}.candidate_source.reference must be non-empty")

    if prior.get("non_identifying") is not True:
        errors.append(f"{prefix}.non_identifying must be true")
    if not _nonempty_strings(prior.get("visible_geometry_evidence")):
        errors.append(
            f"{prefix}.visible_geometry_evidence must contain source-visible geometry"
        )
    geometry_claim_ids = prior.get("geometry_claim_ids")
    if not _nonempty_strings(geometry_claim_ids):
        errors.append(
            f"{prefix}.geometry_claim_ids must contain emitted geometry claim ids"
        )
    elif len(geometry_claim_ids) != len(set(geometry_claim_ids)):
        errors.append(f"{prefix}.geometry_claim_ids contains duplicates")
    if claim.get("owner") not in {"subject.human", "detail.human-face-likeness"}:
        errors.append(f"{prefix} may be owned only by a human subject or face module")
    return errors


def _audit_generation_prior_links(
    prior_claim_id: str,
    claim: dict[str, Any],
    claim_map: dict[str, dict[str, Any]],
    specialized_claim_ids: set[str],
    controlled_claim_counts: dict[str, int],
) -> list[str]:
    """Require a broad human prior to terminate in separate visible geometry controls."""

    prior = claim.get("generation_prior")
    if not isinstance(prior, dict):
        return []
    geometry_claim_ids = prior.get("geometry_claim_ids")
    if not _nonempty_strings(geometry_claim_ids):
        return []

    errors: list[str] = []
    prefix = f"candidate claim {prior_claim_id!r}.generation_prior"
    if prior_claim_id in specialized_claim_ids:
        errors.append(f"{prefix} must be owned by the generic prompt-control ledger")
    for geometry_claim_id in geometry_claim_ids:
        if geometry_claim_id == prior_claim_id:
            errors.append(
                f"{prefix}.geometry_claim_ids must reference a separate geometry claim"
            )
            continue
        geometry_claim = claim_map.get(geometry_claim_id)
        if geometry_claim is None:
            errors.append(
                f"{prefix}.geometry_claim_ids references unknown geometry claim "
                f"{geometry_claim_id!r}"
            )
            continue
        if (
            geometry_claim.get("emit") is not True
            or geometry_claim.get("polarity") != "affirmative"
        ):
            errors.append(
                f"{prefix}.geometry_claim_ids must reference emitted affirmative geometry claims"
            )
        if geometry_claim.get("owner") not in {
            "subject.human",
            "detail.human-face-likeness",
        }:
            errors.append(
                f"{prefix}.geometry_claim_ids may reference only a human or face module"
            )
        if geometry_claim_id in specialized_claim_ids:
            errors.append(
                f"{prefix}.geometry_claim_ids must reference generic geometry claims"
            )
        if controlled_claim_counts.get(geometry_claim_id, 0) != 1:
            errors.append(
                f"{prefix}.geometry_claim_ids needs exactly one generic prompt control "
                f"for {geometry_claim_id!r}"
            )
    return errors


def _audit_component_relations(
    contract: dict[str, Any], known_regions: set[str]
) -> tuple[list[str], dict[str, dict[str, Any]]]:
    """Validate sparse source-relative component and frame relations."""

    errors: list[str] = []
    relations = contract.get("component_relations", [])
    if not isinstance(relations, list):
        return ["component_relations must be a list"], {}

    relation_map: dict[str, dict[str, Any]] = {}
    for index, relation in enumerate(relations):
        label = f"component_relations[{index}]"
        if not isinstance(relation, dict):
            errors.append(f"{label} must be an object")
            continue
        relation_id = relation.get("id")
        if not _nonempty_string(relation_id):
            errors.append(f"{label}.id must be non-empty")
            continue
        relation_id = relation_id.strip()
        if relation_id in relation_map:
            errors.append(f"duplicate component relation id: {relation_id}")
        relation_map[relation_id] = relation

        kind = relation.get("kind")
        if kind not in VALID_COMPONENT_RELATION_KINDS:
            errors.append(f"{label}.kind is invalid")
        subject_region_id = relation.get("subject_region_id")
        if subject_region_id not in known_regions:
            errors.append(f"{label}.subject_region_id must reference a major region")

        reference_region_id = relation.get("reference_region_id")
        frame_reference = relation.get("frame_reference")
        has_region_reference = _nonempty_string(reference_region_id)
        has_frame_reference = _nonempty_string(frame_reference)
        if has_region_reference == has_frame_reference:
            errors.append(
                f"{label} must name exactly one reference_region_id or frame_reference"
            )
        elif has_region_reference and reference_region_id not in known_regions:
            errors.append(f"{label}.reference_region_id must reference a major region")

        if not _nonempty_string(relation.get("observation")):
            errors.append(f"{label}.observation must be source-relative and non-empty")
        if relation.get("role") not in VALID_COMPONENT_RELATION_ROLES:
            errors.append(f"{label}.role is invalid")
        if not _nonempty_strings(relation.get("source_evidence")):
            errors.append(f"{label}.source_evidence must contain visible evidence")

        edge_contacts = relation.get("edge_contacts", [])
        if not _string_list(edge_contacts):
            errors.append(f"{label}.edge_contacts must be a list of frame edges")
            edge_contacts = []
        unknown_edges = sorted(set(edge_contacts) - VALID_FRAME_EDGES)
        if unknown_edges:
            errors.append(f"{label}.edge_contacts contains invalid frame edges")
        if len(edge_contacts) != len(set(edge_contacts)):
            errors.append(f"{label}.edge_contacts contains duplicates")
        if kind == "edge-contact" and not edge_contacts:
            errors.append(f"{label}.edge_contacts must be non-empty for edge-contact")

        visible_fragments = relation.get("visible_fragments", [])
        hidden_or_cropped = relation.get("hidden_or_cropped", [])
        if not _string_list(visible_fragments):
            errors.append(f"{label}.visible_fragments must be a list of strings")
            visible_fragments = []
        if not _string_list(hidden_or_cropped):
            errors.append(f"{label}.hidden_or_cropped must be a list of strings")
            hidden_or_cropped = []
        completion_risk = relation.get("completion_risk")
        if completion_risk is not None and completion_risk not in VALID_COMPLETION_RISKS:
            errors.append(f"{label}.completion_risk is invalid")
        if kind == "partial-visibility":
            if not visible_fragments:
                errors.append(
                    f"{label}.visible_fragments must name the surviving fragments"
                )
            if not hidden_or_cropped:
                errors.append(
                    f"{label}.hidden_or_cropped must name cropped or hidden counterparts"
                )
            if completion_risk not in VALID_COMPLETION_RISKS:
                errors.append(
                    f"{label}.completion_risk is required for partial-visibility"
                )

    return errors, relation_map


def _audit_spatial_orientation_coverage(
    plan: dict[str, Any],
    contract: dict[str, Any],
    known_regions: set[str],
    relation_map: dict[str, dict[str, Any]],
    invariant_map: dict[str, dict[str, Any]],
    claim_map: dict[str, dict[str, Any]],
) -> list[str]:
    """Require an explicit disposition for spatial degrees of freedom.

    This is a coverage and ownership check, not a preferred-pose policy.  The
    validator never assigns a centered, off-center, frontal, profile, left, or
    right target; it only verifies that every generic degree of freedom was
    considered and that invariant decisions reach one relation/effect/claim/
    literal-control path.
    """

    routing = plan.get("routing")
    routed_modules: set[str] = set()
    if isinstance(routing, dict):
        resolved = routing.get("resolved_non_core_modules", [])
        if isinstance(resolved, list):
            routed_modules = {
                item for item in resolved if isinstance(item, str) and item.strip()
            }
    human_routed = "subject.human" in routed_modules

    coverage = contract.get("spatial_orientation_coverage")
    if coverage is None:
        return (
            [
                "a routed subject.human requires spatial_orientation_coverage; "
                "a frame-zone relation alone cannot prove pose/orientation coverage"
            ]
            if human_routed
            else []
        )
    if not isinstance(coverage, dict):
        return ["spatial_orientation_coverage must be an object"]

    errors: list[str] = []
    subjects = coverage.get("subjects")
    if not isinstance(subjects, list) or not subjects:
        errors.append(
            "spatial_orientation_coverage.subjects must contain at least one subject"
        )
        subjects = []

    subject_map: dict[str, dict[str, Any]] = {}
    for index, subject in enumerate(subjects):
        label = f"spatial_orientation_coverage.subjects[{index}]"
        if not isinstance(subject, dict):
            errors.append(f"{label} must be an object")
            continue
        subject_id = subject.get("id")
        if not _nonempty_string(subject_id):
            errors.append(f"{label}.id must be non-empty")
            continue
        subject_id = subject_id.strip()
        if subject_id in subject_map:
            errors.append(f"duplicate spatial coverage subject id: {subject_id}")
        subject_map[subject_id] = subject
        if subject.get("kind") not in VALID_SPATIAL_SUBJECT_KINDS:
            errors.append(f"{label}.kind is invalid")
        if subject.get("visibility") not in VALID_SPATIAL_VISIBILITY:
            errors.append(f"{label}.visibility is invalid")
        region_id = subject.get("region_id")
        if region_id not in known_regions:
            errors.append(f"{label}.region_id must reference a major region")
        if not _nonempty_strings(subject.get("source_evidence")):
            errors.append(f"{label}.source_evidence must contain visible evidence")

    if human_routed and not any(
        subject.get("kind") == "human" for subject in subject_map.values()
    ):
        errors.append(
            "a routed subject.human requires at least one human spatial coverage subject"
        )

    decisions = coverage.get("decisions")
    if not isinstance(decisions, list) or not decisions:
        errors.append(
            "spatial_orientation_coverage.decisions must contain disposition records"
        )
        decisions = []

    effect_map = {
        item.get("id"): item
        for item in contract.get("aggregate_effects", [])
        if isinstance(item, dict) and _nonempty_string(item.get("id"))
    }
    control_map = {
        item.get("id"): item
        for item in contract.get("emitted_controls", [])
        if isinstance(item, dict) and _nonempty_string(item.get("id"))
    }

    decisions_by_subject: dict[str, dict[str, dict[str, Any]]] = {}
    decision_ids: set[str] = set()
    decision_axes: dict[str, str] = {}
    invariant_axes: dict[str, str] = {}
    flexible_set = {
        item
        for item in contract.get("flexible_dimensions", [])
        if isinstance(item, str)
    }

    link_fields = (
        "relation_id",
        "invariant_id",
        "claim_id",
        "aggregate_effect_id",
        "control_id",
    )
    for index, decision in enumerate(decisions):
        label = f"spatial_orientation_coverage.decisions[{index}]"
        if not isinstance(decision, dict):
            errors.append(f"{label} must be an object")
            continue
        decision_id = decision.get("id")
        if not _nonempty_string(decision_id):
            errors.append(f"{label}.id must be non-empty")
            continue
        decision_id = decision_id.strip()
        if decision_id in decision_ids:
            errors.append(f"duplicate spatial coverage decision id: {decision_id}")
        decision_ids.add(decision_id)

        subject_id = decision.get("subject_id")
        if subject_id not in subject_map:
            errors.append(f"{label}.subject_id references an unknown coverage subject")
        dimension = decision.get("dimension")
        expected_family = SPATIAL_DIMENSION_FAMILIES.get(dimension)
        if expected_family is None:
            errors.append(f"{label}.dimension is invalid")
        elif decision.get("family") != expected_family:
            errors.append(
                f"{label}.family must be {expected_family!r} for dimension {dimension!r}"
            )
        if isinstance(subject_id, str) and isinstance(dimension, str):
            bucket = decisions_by_subject.setdefault(subject_id, {})
            if dimension in bucket:
                errors.append(
                    f"coverage subject {subject_id!r} repeats dimension {dimension!r}"
                )
            bucket[dimension] = decision

        disposition = decision.get("disposition")
        if disposition not in VALID_SPATIAL_DISPOSITIONS:
            errors.append(f"{label}.disposition is invalid")
        if decision.get("confidence") not in VALID_SPATIAL_CONFIDENCE:
            errors.append(f"{label}.confidence is invalid")
        causal_origin = decision.get("causal_origin")
        if causal_origin not in VALID_CAUSAL_ORIGINS:
            errors.append(f"{label}.causal_origin is invalid")
        elif causal_origin not in SPATIAL_DIMENSION_ALLOWED_ORIGINS.get(
            dimension, set()
        ):
            errors.append(
                f"{label}.causal_origin {causal_origin!r} is not allowed for "
                f"dimension {dimension!r}"
            )
        if not _nonempty_string(decision.get("observation")):
            errors.append(f"{label}.observation must be source-relative and non-empty")
        if not _nonempty_strings(decision.get("source_evidence")):
            errors.append(f"{label}.source_evidence must contain visible evidence")

        control_axis_id = decision.get("control_axis_id")
        if not _nonempty_string(control_axis_id):
            errors.append(f"{label}.control_axis_id must be non-empty")
            control_axis_id = ""
        elif control_axis_id in decision_axes:
            errors.append(
                "spatial coverage decisions must merge a shared control_axis_id: "
                f"{decision_axes[control_axis_id]}, {decision_id}"
            )
        else:
            decision_axes[control_axis_id] = decision_id

        if disposition != "invariant":
            if not _nonempty_string(decision.get("non_emission_reason")):
                errors.append(
                    f"{label}.non_emission_reason is required for {disposition!r}"
                )
            linked = [field for field in link_fields if _nonempty_string(decision.get(field))]
            if linked:
                errors.append(
                    f"{label} is {disposition!r} and cannot carry emitted-path fields: "
                    + ", ".join(linked)
                )
            if disposition == "flexible" and decision_id not in flexible_set:
                errors.append(
                    f"{label} is flexible and its id must appear in flexible_dimensions"
                )
            continue

        missing_links = [
            field for field in link_fields if not _nonempty_string(decision.get(field))
        ]
        if missing_links:
            errors.append(
                f"{label} is invariant and needs a complete relation/effect/claim/control path: "
                + ", ".join(missing_links)
            )
            continue

        relation_id = decision["relation_id"]
        invariant_id = decision["invariant_id"]
        claim_id = decision["claim_id"]
        effect_id = decision["aggregate_effect_id"]
        control_id = decision["control_id"]
        relation = relation_map.get(relation_id)
        invariant = invariant_map.get(invariant_id)
        claim = claim_map.get(claim_id)
        effect = effect_map.get(effect_id)
        control = control_map.get(control_id)
        for field, value, mapping in (
            ("relation_id", relation_id, relation_map),
            ("invariant_id", invariant_id, invariant_map),
            ("claim_id", claim_id, claim_map),
            ("aggregate_effect_id", effect_id, effect_map),
            ("control_id", control_id, control_map),
        ):
            if value not in mapping:
                errors.append(f"{label}.{field} references an unknown id")
        if relation is not None and relation.get("subject_region_id") != subject_map.get(
            subject_id, {}
        ).get("region_id"):
            errors.append(f"{label}.relation_id must describe the covered subject region")
        if invariant is not None and invariant.get("causal_origin") != causal_origin:
            errors.append(f"{label}.causal_origin must match its invariant")
        if claim is not None:
            if claim.get("semantic_slot") != invariant_id:
                errors.append(f"{label}.claim_id must own its linked invariant slot")
            if claim.get("emit") is not True or claim.get("polarity") != "affirmative":
                errors.append(f"{label}.claim_id must be emitted and affirmative")
        if effect is not None:
            if claim_id not in effect.get("claim_ids", []):
                errors.append(f"{label}.aggregate_effect_id must contain its claim_id")
            if relation_id not in effect.get("relation_ids", []):
                errors.append(f"{label}.aggregate_effect_id must contain its relation_id")
            if effect.get("control_axis_id") != control_axis_id:
                errors.append(f"{label}.control_axis_id must match its aggregate effect")
            if effect.get("causal_origin") != causal_origin:
                errors.append(f"{label}.causal_origin must match its aggregate effect")
        if control is not None:
            if control.get("claim_id") != claim_id:
                errors.append(f"{label}.control_id must actuate its claim_id")
            if effect_id not in control.get("aggregate_effect_ids", []):
                errors.append(f"{label}.control_id must actuate its aggregate_effect_id")
            if control.get("control_axis_id") != control_axis_id:
                errors.append(f"{label}.control_axis_id must match its emitted control")
            if control.get("causal_origin") != causal_origin:
                errors.append(f"{label}.causal_origin must match its emitted control")
        if control_axis_id:
            invariant_axes[control_axis_id] = decision_id

    for subject_id, subject in subject_map.items():
        required = set(BASE_SPATIAL_DIMENSIONS)
        if subject.get("kind") == "human":
            required |= HUMAN_SPATIAL_DIMENSIONS
        present = set(decisions_by_subject.get(subject_id, {}))
        missing = sorted(required - present)
        if missing:
            errors.append(
                f"spatial coverage subject {subject_id!r} is missing dispositions for: "
                + ", ".join(missing)
            )

    effect_axes: dict[str, str] = {}
    for effect_id, effect in effect_map.items():
        control_axis_id = effect.get("control_axis_id")
        if control_axis_id is None:
            continue
        if not _nonempty_string(control_axis_id):
            errors.append(
                f"generic aggregate effect {effect_id!r}.control_axis_id must be non-empty"
            )
            continue
        if control_axis_id in effect_axes:
            errors.append(
                "generic aggregate effects duplicate one spatial control_axis_id across slots: "
                f"{effect_axes[control_axis_id]}, {effect_id}"
            )
        else:
            effect_axes[control_axis_id] = effect_id
        if control_axis_id not in invariant_axes:
            errors.append(
                f"generic aggregate effect {effect_id!r} emits unowned or non-invariant "
                f"spatial control axis {control_axis_id!r}"
            )

    control_axes: dict[str, str] = {}
    for control_id, control in control_map.items():
        control_axis_id = control.get("control_axis_id")
        if control_axis_id is None:
            continue
        if not _nonempty_string(control_axis_id):
            errors.append(
                f"generic emitted control {control_id!r}.control_axis_id must be non-empty"
            )
            continue
        if control_axis_id in control_axes:
            errors.append(
                "generic emitted controls duplicate one spatial control_axis_id across slots: "
                f"{control_axes[control_axis_id]}, {control_id}"
            )
        else:
            control_axes[control_axis_id] = control_id
        if control_axis_id not in invariant_axes:
            errors.append(
                f"generic emitted control {control_id!r} emits unowned or non-invariant "
                f"spatial control axis {control_axis_id!r}"
            )

    return errors


def _audit_human_appearance_decisions(
    plan: dict[str, Any],
    contract: dict[str, Any],
    claim_map: dict[str, dict[str, Any]],
) -> list[str]:
    """Require explicit, source-relative decisions for human priors and skin language."""

    routing = plan.get("routing")
    routed_modules = (
        routing.get("resolved_non_core_modules", [])
        if isinstance(routing, dict)
        else []
    )
    human_routed = (
        isinstance(routed_modules, list) and "subject.human" in routed_modules
    )

    coverage = contract.get("spatial_orientation_coverage")
    subjects = coverage.get("subjects", []) if isinstance(coverage, dict) else []
    human_subjects = {
        item.get("id"): item
        for item in subjects
        if isinstance(item, dict)
        and item.get("kind") == "human"
        and _nonempty_string(item.get("id"))
    }

    decisions = contract.get("human_appearance_decisions")
    if decisions is None:
        return (
            [
                "a routed subject.human requires human_appearance_decisions; "
                "person prior and skin-surface handling cannot be silently omitted"
            ]
            if human_routed
            else []
        )
    if not isinstance(decisions, list):
        return ["human_appearance_decisions must be a list"]

    errors: list[str] = []
    decision_ids: set[str] = set()
    decisions_by_subject: dict[str, int] = {}
    emitted_prior_claim_ids: set[str] = set()

    color_contract = contract.get("color_tone_contract")
    color_regions = (
        color_contract.get("regions", []) if isinstance(color_contract, dict) else []
    )
    color_region_ids = {
        item.get("id")
        for item in color_regions
        if isinstance(item, dict) and _nonempty_string(item.get("id"))
    }
    surface_language = (
        color_contract.get("surface_color_language")
        if isinstance(color_contract, dict)
        else None
    )
    controlled_descriptor = (
        surface_language.get("controlled_descriptor")
        if isinstance(surface_language, dict)
        else None
    )

    for index, decision in enumerate(decisions):
        label = f"human_appearance_decisions[{index}]"
        if not isinstance(decision, dict):
            errors.append(f"{label} must be an object")
            continue
        decision_id = decision.get("id")
        if not _nonempty_string(decision_id):
            errors.append(f"{label}.id must be non-empty")
        elif decision_id in decision_ids:
            errors.append(f"duplicate human appearance decision id: {decision_id}")
        else:
            decision_ids.add(decision_id)

        subject_id = decision.get("subject_id")
        if not _nonempty_string(subject_id) or subject_id not in human_subjects:
            errors.append(f"{label}.subject_id must reference a human coverage subject")
        else:
            decisions_by_subject[subject_id] = decisions_by_subject.get(subject_id, 0) + 1
        face_visibility = decision.get("face_visibility")
        if face_visibility not in VALID_HUMAN_FACE_VISIBILITY:
            errors.append(f"{label}.face_visibility is invalid")
        if not _nonempty_strings(decision.get("source_evidence")):
            errors.append(f"{label}.source_evidence must contain visible evidence")

        prior = decision.get("person_prior")
        if not isinstance(prior, dict):
            errors.append(f"{label}.person_prior must be an object")
        else:
            disposition = prior.get("disposition")
            if disposition not in VALID_PERSON_PRIOR_DISPOSITIONS:
                errors.append(f"{label}.person_prior.disposition is invalid")
            if prior.get("confidence") not in VALID_SPATIAL_CONFIDENCE:
                errors.append(f"{label}.person_prior.confidence is invalid")
            if not _nonempty_strings(prior.get("source_evidence")):
                errors.append(
                    f"{label}.person_prior.source_evidence must contain visible evidence"
                )
            claim_id = prior.get("claim_id")
            if disposition == "emit":
                if face_visibility not in {"readable", "partial"}:
                    errors.append(
                        f"{label}.person_prior cannot emit for face visibility {face_visibility!r}"
                    )
                if not _nonempty_string(claim_id):
                    claim = None
                    errors.append(f"{label}.person_prior.claim_id must be non-empty")
                else:
                    claim = claim_map.get(claim_id)
                if _nonempty_string(claim_id) and claim is None:
                    errors.append(
                        f"{label}.person_prior.claim_id references an unknown claim"
                    )
                elif claim is not None:
                    emitted_prior_claim_ids.add(str(claim_id))
                    generation_prior = claim.get("generation_prior")
                    if (
                        claim.get("emit") is not True
                        or claim.get("polarity") != "affirmative"
                    ):
                        errors.append(
                            f"{label}.person_prior.claim_id must be emitted and affirmative"
                        )
                    if claim.get("owner") not in {
                        "subject.human",
                        "detail.human-face-likeness",
                    }:
                        errors.append(
                            f"{label}.person_prior.claim_id must have a human owner"
                        )
                    if (
                        not isinstance(generation_prior, dict)
                        or generation_prior.get("scope") != "person-gestalt"
                    ):
                        errors.append(
                            f"{label}.person_prior.claim_id must own a person-gestalt "
                            "generation_prior"
                        )
            else:
                if not _nonempty_string(prior.get("non_emission_reason")):
                    errors.append(
                        f"{label}.person_prior.non_emission_reason is required for {disposition!r}"
                    )
                if _nonempty_string(claim_id):
                    errors.append(
                        f"{label}.person_prior cannot reference a claim when not emitted"
                    )

        skin = decision.get("skin_surface")
        if not isinstance(skin, dict):
            errors.append(f"{label}.skin_surface must be an object")
            continue
        skin_disposition = skin.get("disposition")
        if skin_disposition not in VALID_SKIN_SURFACE_DISPOSITIONS:
            errors.append(f"{label}.skin_surface.disposition is invalid")
        if skin.get("confidence") not in VALID_SPATIAL_CONFIDENCE:
            errors.append(f"{label}.skin_surface.confidence is invalid")
        if not _nonempty_strings(skin.get("source_evidence")):
            errors.append(
                f"{label}.skin_surface.source_evidence must contain visible evidence"
            )
        region_ids = skin.get("region_ids", [])
        if not isinstance(region_ids, list) or not all(
            _nonempty_string(item) for item in region_ids
        ):
            errors.append(
                f"{label}.skin_surface.region_ids must be a list of region ids"
            )
            region_ids = []
        elif len(region_ids) != len(set(region_ids)):
            errors.append(f"{label}.skin_surface.region_ids contains duplicates")

        descriptor_disposition = skin.get("descriptor_disposition")
        if descriptor_disposition not in VALID_DESCRIPTOR_DISPOSITIONS:
            errors.append(f"{label}.skin_surface.descriptor_disposition is invalid")
        if skin_disposition != "material":
            if region_ids:
                errors.append(
                    f"{label}.skin_surface.region_ids must be empty when not material"
                )
            if not _nonempty_string(skin.get("non_emission_reason")):
                errors.append(
                    f"{label}.skin_surface.non_emission_reason is required for {skin_disposition!r}"
                )
            if descriptor_disposition == "emit":
                errors.append(
                    f"{label}.skin_surface descriptor cannot emit when skin is not material"
                )
            if not _nonempty_string(skin.get("descriptor_non_emission_reason")):
                errors.append(
                    f"{label}.skin_surface.descriptor_non_emission_reason is "
                    "required when not emitted"
                )
            continue

        if skin.get("coverage") not in VALID_SKIN_COVERAGE:
            errors.append(f"{label}.skin_surface.coverage is invalid")
        if not region_ids:
            errors.append(f"{label}.skin_surface.region_ids must name material skin regions")
        unknown_regions = sorted(set(region_ids) - color_region_ids)
        if unknown_regions:
            errors.append(
                f"{label}.skin_surface.region_ids require matching Color/Tone regions: "
                + ", ".join(unknown_regions)
            )
        if descriptor_disposition == "emit":
            if not isinstance(surface_language, dict):
                errors.append(
                    f"{label}.skin_surface descriptor emission requires surface_color_language"
                )
            elif surface_language.get("region_id") not in region_ids:
                errors.append(
                    f"{label}.skin_surface descriptor must target one listed skin region"
                )
            if (
                not isinstance(controlled_descriptor, dict)
                or controlled_descriptor.get("emit") is not True
            ):
                errors.append(
                    f"{label}.skin_surface descriptor emission requires an emitted controlled_descriptor"
                )
        else:
            if not _nonempty_string(skin.get("descriptor_non_emission_reason")):
                errors.append(
                    f"{label}.skin_surface.descriptor_non_emission_reason is required for {descriptor_disposition!r}"
                )
            if (
                isinstance(controlled_descriptor, dict)
                and controlled_descriptor.get("emit") is True
                and isinstance(surface_language, dict)
                and surface_language.get("region_id") in region_ids
            ):
                errors.append(
                    f"{label}.skin_surface descriptor decision contradicts the emitted controlled_descriptor"
                )

    for subject_id in human_subjects:
        count = decisions_by_subject.get(subject_id, 0)
        if count != 1:
            errors.append(
                f"human coverage subject {subject_id!r} requires exactly one human appearance decision"
            )

    if human_routed:
        person_prior_claim_ids = {
            str(claim_id)
            for claim_id, claim in claim_map.items()
            if claim.get("emit") is True
            and isinstance(claim.get("generation_prior"), dict)
            and claim["generation_prior"].get("scope") == "person-gestalt"
        }
        unowned = sorted(person_prior_claim_ids - emitted_prior_claim_ids)
        if unowned:
            errors.append(
                "emitted person-gestalt generation priors require a human appearance decision: "
                + ", ".join(unowned)
            )

    return errors


def _specialized_claim_ids(contract: dict[str, Any]) -> tuple[set[str], set[str]]:
    def claim_ids(name: str) -> set[str]:
        specialized = contract.get(name)
        if not isinstance(specialized, dict):
            return set()
        values = specialized.get("claim_ids", [])
        return {value for value in values if _nonempty_string(value)} if isinstance(values, list) else set()

    return claim_ids("color_tone_contract"), claim_ids("light_form_contract")


def _audit_generic_contract(
    contract: dict[str, Any],
    claim_map: dict[str, dict[str, Any]],
    invariant_map: dict[str, dict[str, Any]],
    known_regions: set[str],
    relation_map: dict[str, dict[str, Any]],
) -> list[str]:
    """Validate non-color/non-light effects and literal final-prompt controls."""

    errors: list[str] = []
    color_claim_ids, light_claim_ids = _specialized_claim_ids(contract)
    specialized_claim_ids = color_claim_ids | light_claim_ids
    emitted_claim_ids = {
        claim_id
        for claim_id, claim in claim_map.items()
        if bool(claim.get("emit"))
    }
    generic_emitted_claim_ids = emitted_claim_ids - specialized_claim_ids

    effects = contract.get("aggregate_effects", [])
    if not isinstance(effects, list):
        errors.append("aggregate_effects must be a list")
        effects = []
    if generic_emitted_claim_ids and not effects:
        errors.append(
            "aggregate_effects must contain source-relative effects for generic emitted claims"
        )

    effect_map: dict[str, dict[str, Any]] = {}
    canonical_effects: dict[tuple[Any, ...], str] = {}
    for index, effect in enumerate(effects):
        label = f"aggregate_effects[{index}]"
        if not isinstance(effect, dict):
            errors.append(f"{label} must be an object")
            continue
        effect_id = effect.get("id")
        if not _nonempty_string(effect_id):
            errors.append(f"{label}.id must be non-empty")
            continue
        effect_id = effect_id.strip()
        if effect_id in effect_map:
            errors.append(f"duplicate generic aggregate effect id: {effect_id}")
        effect_map[effect_id] = effect

        axis = effect.get("axis")
        if axis not in VALID_GENERIC_EFFECT_AXES:
            errors.append(
                f"{label}.axis must be a non-color, non-light salience axis"
            )
        direction = effect.get("direction")
        if not _nonempty_string(direction):
            errors.append(f"{label}.direction must be source-relative and non-empty")
            direction = ""
        if effect.get("role") not in VALID_INVARIANT_ROLES:
            errors.append(f"{label}.role is invalid")
        if effect.get("target_strength") not in VALID_STRENGTHS:
            errors.append(f"{label}.target_strength is invalid")
        if not isinstance(effect.get("source_supported"), bool):
            errors.append(f"{label}.source_supported must be boolean")
        if not _nonempty_strings(effect.get("source_evidence")):
            errors.append(f"{label}.source_evidence must contain visible evidence")

        members = effect.get("claim_ids")
        if not _nonempty_strings(members):
            errors.append(f"{label}.claim_ids must contain claim ids")
            members = []
        elif len(members) != len(set(members)):
            errors.append(f"{label}.claim_ids contains duplicates")
        unknown_claims = sorted(set(members) - set(claim_map))
        if unknown_claims:
            errors.append(f"{label} references unknown claims: {', '.join(unknown_claims)}")

        region_ids = effect.get("region_ids", [])
        if not _string_list(region_ids):
            errors.append(f"{label}.region_ids must be a list of major region ids")
            region_ids = []
        unknown_regions = sorted(set(region_ids) - known_regions)
        if unknown_regions:
            errors.append(f"{label} references unknown regions: {', '.join(unknown_regions)}")
        if len(region_ids) != len(set(region_ids)):
            errors.append(f"{label}.region_ids contains duplicates")

        relation_ids = effect.get("relation_ids", [])
        if not _string_list(relation_ids):
            errors.append(f"{label}.relation_ids must be a list of component relation ids")
            relation_ids = []
        unknown_relations = sorted(set(relation_ids) - set(relation_map))
        if unknown_relations:
            errors.append(
                f"{label} references unknown component relations: {', '.join(unknown_relations)}"
            )
        if len(relation_ids) != len(set(relation_ids)):
            errors.append(f"{label}.relation_ids contains duplicates")

        canonical = (
            axis,
            direction.strip().lower() if isinstance(direction, str) else "",
            tuple(sorted(region_ids)),
            tuple(sorted(relation_ids)),
        )
        if canonical in canonical_effects:
            errors.append(
                "generic aggregate effects split one axis/direction/region/relation "
                f"across effect ids: {canonical_effects[canonical]}, {effect_id}"
            )
        else:
            canonical_effects[canonical] = effect_id

    claim_effect_ids: dict[str, set[str]] = {}
    for claim_id, claim in claim_map.items():
        label = f"candidate claim {claim_id!r}"
        errors.extend(_audit_generation_prior(claim, label))
        raw_effects = claim.get("salience_effects")
        if claim_id in generic_emitted_claim_ids and not isinstance(raw_effects, list):
            errors.append(
                f"{label}.salience_effects must link generic emitted claims to aggregate effects"
            )
            raw_effects = []
        elif raw_effects is None:
            raw_effects = []
        elif not isinstance(raw_effects, list):
            errors.append(f"{label}.salience_effects must be a list")
            raw_effects = []

        linked_ids: set[str] = set()
        for index, item in enumerate(raw_effects):
            effect_label = f"{label}.salience_effects[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{effect_label} must be an object")
                continue
            effect_id = item.get("aggregate_effect_id")
            if not _nonempty_string(effect_id):
                errors.append(f"{effect_label}.aggregate_effect_id must be non-empty")
                continue
            effect_id = effect_id.strip()
            if effect_id in linked_ids:
                errors.append(f"{label}.salience_effects contains duplicate effects")
            linked_ids.add(effect_id)
            if effect_id not in effect_map:
                errors.append(f"{effect_label} references unknown effect {effect_id!r}")
            if not _nonempty_strings(item.get("source_evidence")):
                errors.append(f"{effect_label}.source_evidence must be non-empty")
        claim_effect_ids[claim_id] = linked_ids
        if claim_id in generic_emitted_claim_ids and not linked_ids:
            errors.append(f"{label}.salience_effects must contain at least one effect")
        if claim_id in specialized_claim_ids and linked_ids:
            errors.append(
                f"Generic and specialized contracts cannot own the same claims: {claim_id}"
            )

    for effect_id, effect in effect_map.items():
        declared_claims = {
            item for item in effect.get("claim_ids", []) if _nonempty_string(item)
        }
        linked_claims = {
            claim_id
            for claim_id, linked_ids in claim_effect_ids.items()
            if effect_id in linked_ids
        }
        if declared_claims != linked_claims:
            errors.append(
                f"generic aggregate effect {effect_id!r} claim_ids must exactly match claim salience_effects"
            )
        emitted_members = declared_claims & generic_emitted_claim_ids
        if len(emitted_members) > 1:
            errors.append(
                f"generic aggregate effect {effect_id!r} has multiple emitted claims"
            )
        elif len(emitted_members) == 0:
            errors.append(
                f"generic aggregate effect {effect_id!r} needs exactly one emitted generic claim"
            )
        if effect.get("source_supported") is False and emitted_members:
            errors.append(
                f"generic aggregate effect {effect_id!r} is unsupported but emitted"
            )
        if len(emitted_members) == 1:
            claim = claim_map[next(iter(emitted_members))]
            if effect.get("target_strength") != claim.get("target_strength"):
                errors.append(
                    f"generic aggregate effect {effect_id!r} strength must match its emitted claim"
                )

    controls = contract.get("emitted_controls", [])
    if not isinstance(controls, list):
        errors.append("emitted_controls must be a list")
        controls = []
    if generic_emitted_claim_ids and not controls:
        errors.append("emitted_controls must contain exact generic final-prompt controls")

    control_ids: set[str] = set()
    prompt_excerpts: set[str] = set()
    controlled_claim_counts: dict[str, int] = {}
    generic_control_claim_ids: set[str] = set()
    for index, control in enumerate(controls):
        label = f"emitted_controls[{index}]"
        if not isinstance(control, dict):
            errors.append(f"{label} must be an object")
            continue
        control_id = control.get("id")
        if not _nonempty_string(control_id):
            errors.append(f"{label}.id must be non-empty")
        elif control_id in control_ids:
            errors.append(f"duplicate generic emitted control id: {control_id}")
        else:
            control_ids.add(control_id)

        excerpt = control.get("prompt_excerpt")
        if not _nonempty_string(excerpt):
            errors.append(f"{label}.prompt_excerpt must be non-empty")
        elif excerpt.strip() in prompt_excerpts:
            errors.append("generic emitted controls must use distinct prompt excerpts")
        else:
            prompt_excerpts.add(excerpt.strip())

        claim_id = control.get("claim_id")
        if claim_id not in claim_map:
            errors.append(f"{label}.claim_id references an unknown claim")
            continue
        generic_control_claim_ids.add(claim_id)
        controlled_claim_counts[claim_id] = controlled_claim_counts.get(claim_id, 0) + 1
        claim = claim_map[claim_id]
        if claim_id in specialized_claim_ids:
            errors.append(
                f"Generic and specialized contracts cannot own the same claims: {claim_id}"
            )
        if control.get("owner") != claim.get("owner"):
            errors.append(f"{label}.owner must match the claim owner")
        effect_ids = control.get("aggregate_effect_ids")
        if not _nonempty_strings(effect_ids):
            errors.append(f"{label}.aggregate_effect_ids must contain effect ids")
            effect_ids = []
        unknown_effects = sorted(set(effect_ids) - set(effect_map))
        if unknown_effects:
            errors.append(f"{label} references unknown effects: {', '.join(unknown_effects)}")
        if set(effect_ids) != claim_effect_ids.get(claim_id, set()):
            errors.append(
                f"{label}.aggregate_effect_ids must exactly match the claim salience effects"
            )

    for claim_id in sorted(generic_emitted_claim_ids):
        if controlled_claim_counts.get(claim_id, 0) != 1:
            errors.append(
                f"generic claim {claim_id!r} must have exactly one emitted final-prompt control"
            )

    for claim_id, claim in claim_map.items():
        errors.extend(
            _audit_generation_prior_links(
                claim_id,
                claim,
                claim_map,
                specialized_claim_ids,
                controlled_claim_counts,
            )
        )

    used_relation_ids = {
        relation_id
        for effect in effect_map.values()
        for relation_id in effect.get("relation_ids", [])
        if _nonempty_string(relation_id)
    }
    for relation_id in relation_map:
        if relation_id not in used_relation_ids:
            errors.append(
                f"component relation {relation_id!r} must terminate in a generic aggregate effect"
            )

    for invariant_id, invariant in invariant_map.items():
        axis = invariant.get("axis")
        if axis not in VALID_GENERIC_EFFECT_AXES:
            continue
        matching_claims = [
            claim
            for claim in claim_map.values()
            if claim.get("semantic_slot") == invariant_id
            and claim.get("emit") is True
            and claim.get("polarity") == "affirmative"
        ]
        if len(matching_claims) != 1:
            continue
        claim_id = matching_claims[0].get("id")
        linked_effects = [
            effect_map[effect_id]
            for effect_id in claim_effect_ids.get(claim_id, set())
            if effect_id in effect_map
        ]
        if not any(effect.get("axis") == axis for effect in linked_effects):
            errors.append(
                f"invariant {invariant_id!r} needs a same-axis generic aggregate effect"
            )
        if invariant.get("causal_origin") == "spatial-relation" or axis == "topology":
            if not any(effect.get("relation_ids") for effect in linked_effects):
                errors.append(
                    f"spatial-relation invariant {invariant_id!r} needs a linked component relation"
                )

    specialized_contracts = (
        ("Color/Tone", contract.get("color_tone_contract"), color_claim_ids),
        ("Light/Form", contract.get("light_form_contract"), light_claim_ids),
    )
    generic_owned_claim_ids = set().union(
        *(set(effect.get("claim_ids", [])) for effect in effect_map.values())
    ) | generic_control_claim_ids
    for name, specialized, listed_claim_ids in specialized_contracts:
        if not isinstance(specialized, dict):
            continue
        claim_overlap = sorted(generic_owned_claim_ids & listed_claim_ids)
        if claim_overlap:
            errors.append(
                f"Generic and {name} contracts cannot own the same claims: "
                + ", ".join(claim_overlap)
            )
        specialized_excerpts = {
            item.get("prompt_excerpt", "").strip()
            for item in specialized.get("emitted_controls", [])
            if isinstance(item, dict) and _nonempty_string(item.get("prompt_excerpt"))
        }
        if prompt_excerpts & specialized_excerpts:
            errors.append(
                f"Generic and {name} contracts cannot own the same prompt excerpts"
            )

    return errors


def _audit_authored_prompt(contract: dict[str, Any], prompt_text: Any) -> list[str]:
    """Check literal ledger excerpts against an explicitly supplied authored prompt."""

    if not isinstance(prompt_text, str):
        return ["authored prompt text must be a string"]
    errors: list[str] = []
    ledgers = [
        ("emitted_controls", contract.get("emitted_controls", [])),
        (
            "color_tone_contract.emitted_controls",
            contract.get("color_tone_contract", {}).get("emitted_controls", [])
            if isinstance(contract.get("color_tone_contract"), dict)
            else [],
        ),
        (
            "light_form_contract.emitted_controls",
            contract.get("light_form_contract", {}).get("emitted_controls", [])
            if isinstance(contract.get("light_form_contract"), dict)
            else [],
        ),
    ]
    for ledger_name, controls in ledgers:
        if not isinstance(controls, list):
            continue
        for index, control in enumerate(controls):
            if not isinstance(control, dict):
                continue
            excerpt = control.get("prompt_excerpt")
            if not _nonempty_string(excerpt):
                continue
            count = prompt_text.count(excerpt.strip())
            if count != 1:
                errors.append(
                    f"{ledger_name}[{index}].prompt_excerpt appears {count} times "
                    "in the authored prompt; expected exactly once"
                )
    color_contract = contract.get("color_tone_contract")
    if isinstance(color_contract, dict):
        surface_language = color_contract.get("surface_color_language")
        descriptor = (
            surface_language.get("controlled_descriptor")
            if isinstance(surface_language, dict)
            else None
        )
        if isinstance(descriptor, dict) and descriptor.get("emit") is True:
            phrase = descriptor.get("phrase")
            if _nonempty_string(phrase):
                count = prompt_text.count(phrase.strip())
                if count != 1:
                    errors.append(
                        "controlled_descriptor.phrase appears "
                        f"{count} times in the authored prompt; expected exactly once"
                    )
    return errors


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


def _audit_controlled_surface_descriptor(
    surface_language: dict[str, Any],
    classifications: dict[str, Any],
    color_control_map: dict[str, dict[str, Any]],
    generic_control_map: dict[str, dict[str, Any]],
    generic_effect_map: dict[str, dict[str, Any]],
) -> list[str]:
    """Validate a deterministic axis-composed surface phrase and its controls."""

    descriptor = surface_language.get("controlled_descriptor")
    if descriptor is None:
        return []
    prefix = "color_tone_contract.surface_color_language.controlled_descriptor"
    if not isinstance(descriptor, dict):
        return [f"{prefix} must be an object"]

    errors: list[str] = []
    included_axes = descriptor.get("included_axes")
    allowed_axis_orders = [
        ["value_depth", "chroma", "undertone"],
        ["value_depth", "chroma", "undertone", "finish"],
    ]
    if included_axes not in allowed_axis_orders:
        errors.append(
            f"{prefix}.included_axes must contain the three core axes in order, "
            "with optional finish last"
        )
        return errors

    surface_term = descriptor.get("surface_term")
    if not _nonempty_string(surface_term):
        errors.append(f"{prefix}.surface_term must be an analyst-supplied region phrase")
        return errors
    try:
        expected = compose_controlled_descriptor(
            {"axis_classification": classifications},
            surface_term,
            include_finish="finish" in included_axes,
        )
    except ValueError as exc:
        errors.append(f"{prefix} cannot be reconstructed: {exc}")
        return errors

    for field in (
        "status",
        "surface_term",
        "included_axes",
        "axis_excerpts",
        "unresolved_axes",
        "composition_source",
    ):
        if descriptor.get(field) != expected.get(field):
            errors.append(f"{prefix}.{field} does not match the classified axes")
    if expected.get("status") == "ready":
        if descriptor.get("phrase") != expected.get("phrase"):
            errors.append(f"{prefix}.phrase does not match the classified axes")
    elif "phrase" in descriptor:
        errors.append(f"{prefix}.phrase must be absent while classification is inconclusive")

    emit = descriptor.get("emit")
    if not isinstance(emit, bool):
        errors.append(f"{prefix}.emit must be boolean")
        return errors
    if not _nonempty_strings(descriptor.get("source_evidence")):
        errors.append(f"{prefix}.source_evidence must contain current-source evidence")

    axis_control_ids = descriptor.get("axis_control_ids", {})
    if not isinstance(axis_control_ids, dict):
        errors.append(f"{prefix}.axis_control_ids must be an object")
        axis_control_ids = {}

    if not emit:
        if not _nonempty_string(descriptor.get("non_emission_reason")):
            errors.append(f"{prefix}.non_emission_reason is required when not emitted")
        if axis_control_ids:
            errors.append(f"{prefix}.axis_control_ids must be empty when not emitted")
        return errors

    if expected.get("status") != "ready":
        errors.append(f"{prefix} cannot emit while classified axes are inconclusive")
    if set(axis_control_ids) != set(included_axes):
        errors.append(f"{prefix}.axis_control_ids must cover exactly included_axes")

    expected_excerpts = expected.get("axis_excerpts", {})
    surface_region_id = surface_language.get("region_id")
    for axis in included_axes:
        control_id = axis_control_ids.get(axis)
        if not _nonempty_string(control_id):
            continue
        if axis == "finish":
            control = generic_control_map.get(control_id)
            if control is None:
                errors.append(
                    f"{prefix}.axis_control_ids.finish must reference a generic surface control"
                )
                continue
            effect_ids = control.get("aggregate_effect_ids", [])
            resolved_effects = (
                [
                    generic_effect_map[effect_id]
                    for effect_id in effect_ids
                    if effect_id in generic_effect_map
                ]
                if isinstance(effect_ids, list)
                else []
            )
            if len(resolved_effects) != 1:
                errors.append(
                    f"{prefix}.axis_control_ids.finish must own one generic surface effect"
                )
            elif (
                resolved_effects[0].get("axis") != "surface"
                or surface_region_id not in resolved_effects[0].get("region_ids", [])
            ):
                errors.append(
                    f"{prefix}.axis_control_ids.finish must control the same region's surface axis"
                )
        else:
            control = color_control_map.get(control_id)
            if control is None:
                errors.append(
                    f"{prefix}.axis_control_ids.{axis} references an unknown color control"
                )
                continue
            if control.get("control_role") != "axis-control":
                errors.append(f"{prefix}.axis_control_ids.{axis} must reference an axis-control")
            if control.get("region_id") != surface_region_id:
                errors.append(f"{prefix}.axis_control_ids.{axis} must control the same region")
            if control.get("axis") != CONTROLLED_DESCRIPTOR_AXIS_TO_COLOR_AXIS[axis]:
                errors.append(f"{prefix}.axis_control_ids.{axis} controls the wrong color axis")
        if control.get("prompt_excerpt") != expected_excerpts.get(axis):
            errors.append(
                f"{prefix}.axis_control_ids.{axis} prompt excerpt must equal its composed axis excerpt"
            )

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
    control_map: dict[str, dict[str, Any]] = {}
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
            control_map[control_id] = control

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

        generic_control_map = {
            item.get("id"): item
            for item in contract.get("emitted_controls", [])
            if isinstance(item, dict) and _nonempty_string(item.get("id"))
        }
        generic_effect_map = {
            item.get("id"): item
            for item in contract.get("aggregate_effects", [])
            if isinstance(item, dict) and _nonempty_string(item.get("id"))
        }
        errors.extend(
            _audit_controlled_surface_descriptor(
                surface_language,
                classifications,
                control_map,
                generic_control_map,
                generic_effect_map,
            )
        )

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
    observed_region_pairs: set[tuple[str, str]] = set()
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
        region_id = effect.get("region_id")
        if region_id not in known_regions:
            errors.append(f"{label}.region_id references an unknown region")
        reference_region_id = effect.get("reference_region_id")
        if reference_region_id is not None:
            if not _nonempty_string(reference_region_id):
                errors.append(
                    f"{label}.reference_region_id must be non-empty when present"
                )
            elif region_id not in major_region_ids:
                errors.append(
                    f"{label}.region_id must reference a major region for comparison"
                )
            elif reference_region_id not in major_region_ids:
                errors.append(
                    f"{label}.reference_region_id references an unknown region"
                )
            elif reference_region_id == region_id:
                errors.append(
                    f"{label}.reference_region_id must reference a distinct region"
                )
            else:
                observed_region_pairs.add((str(region_id), reference_region_id))
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
    aggregate_signatures: dict[tuple[str, str, str, str], str] = {}
    aggregate_region_pairs: set[tuple[str, str]] = set()
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
        reference_region_id = effect.get("reference_region_id")
        if reference_region_id is not None:
            if not _nonempty_string(reference_region_id):
                errors.append(
                    f"{label}.reference_region_id must be non-empty when present"
                )
            elif region_id not in major_region_ids:
                errors.append(
                    f"{label}.region_id must reference a major region for comparison"
                )
            elif reference_region_id not in major_region_ids:
                errors.append(
                    f"{label}.reference_region_id references an unknown region"
                )
            elif reference_region_id == region_id:
                errors.append(
                    f"{label}.reference_region_id must reference a distinct region"
                )
            else:
                aggregate_region_pairs.add((str(region_id), reference_region_id))
        if (
            axis in VALID_LIGHT_EFFECT_AXES
            and _nonempty_string(direction)
            and region_id in known_regions
        ):
            normalized_direction = "-".join(
                direction.casefold().replace("_", " ").replace("-", " ").split()
            )
            signature = (
                str(region_id),
                str(reference_region_id or ""),
                str(axis),
                normalized_direction,
            )
            previous = aggregate_signatures.get(signature)
            if previous is not None:
                errors.append(
                    f"aggregate lighting effects {previous!r} and {effect_id!r} split one region/reference/axis/direction"
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

    for region_pair in sorted(observed_region_pairs - aggregate_region_pairs):
        errors.append(
            "observed regional light relation must terminate in an aggregate effect: "
            + " -> ".join(region_pair)
        )
    for region_pair in sorted(aggregate_region_pairs - observed_region_pairs):
        errors.append(
            "aggregate regional light relation needs a matching observed region effect: "
            + " -> ".join(region_pair)
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


def audit_plan(plan: dict[str, Any], prompt_text: str | None = None) -> list[str]:
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

    relation_errors, relation_map = _audit_component_relations(contract, region_ids)
    errors.extend(relation_errors)
    errors.extend(
        _audit_generic_contract(
            contract,
            claim_map,
            invariant_map,
            region_ids,
            relation_map,
        )
    )
    errors.extend(
        _audit_spatial_orientation_coverage(
            plan,
            contract,
            region_ids,
            relation_map,
            invariant_map,
            claim_map,
        )
    )

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
    errors.extend(_audit_human_appearance_decisions(plan, contract, claim_map))

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

    if prompt_text is not None:
        errors.extend(_audit_authored_prompt(contract, prompt_text))

    return errors


def primary_signature(plan: dict[str, Any]) -> set[tuple[str, str, str]]:
    contract = _contract(plan)
    signature = {
        (str(item.get("id")), str(item.get("axis")), str(item.get("target_strength")))
        for item in contract.get("invariants", [])
        if isinstance(item, dict) and item.get("role") == "primary"
    }
    signature.update(
        (
            f"generic-effect:{item.get('id')}",
            (
                f"{item.get('axis')}:regions="
                f"{','.join(sorted(item.get('region_ids', [])))}:relations="
                f"{','.join(sorted(item.get('relation_ids', [])))}"
            ),
            f"{item.get('direction')}:{item.get('target_strength')}",
        )
        for item in contract.get("aggregate_effects", [])
        if isinstance(item, dict) and item.get("role") == "primary"
    )
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
                (
                    f"{item.get('axis')}:{item.get('region_id')}:"
                    f"reference={item.get('reference_region_id')}"
                ),
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
    baseline_prompt_text: str | None = None,
    variant_prompt_text: str | None = None,
) -> list[str]:
    """Check a matched pair without comparing generated wording."""

    errors = [
        f"baseline: {error}"
        for error in audit_plan(baseline, prompt_text=baseline_prompt_text)
    ]
    errors.extend(
        f"variant: {error}"
        for error in audit_plan(variant, prompt_text=variant_prompt_text)
    )
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
        "--prompt",
        default="",
        help="authored prompt text for literal emitted-control reconciliation",
    )
    parser.add_argument(
        "--compare-prompt",
        default="",
        help="authored prompt text for the matched variant plan",
    )
    parser.add_argument(
        "--relation",
        choices=["invariant-preserving", "aesthetic-changing"],
        default="invariant-preserving",
    )
    args = parser.parse_args(argv)

    try:
        baseline = _load_json(args.plan)
        baseline_prompt = (
            Path(args.prompt).read_text(encoding="utf-8") if args.prompt else None
        )
        variant_prompt = (
            Path(args.compare_prompt).read_text(encoding="utf-8")
            if args.compare_prompt
            else None
        )
        if args.compare_prompt and not args.compare:
            raise ValueError("--compare-prompt requires --compare")
        errors = (
            compare_plans(
                baseline,
                _load_json(args.compare),
                args.relation,
                baseline_prompt_text=baseline_prompt,
                variant_prompt_text=variant_prompt,
            )
            if args.compare
            else audit_plan(baseline, prompt_text=baseline_prompt)
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
