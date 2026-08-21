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
VALID_COLOR_AXES = {"value", "chroma", "hue", "contrast"}
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
