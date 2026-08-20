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


def _contract(plan: dict[str, Any]) -> dict[str, Any]:
    nested = plan.get("render_contract")
    return nested if isinstance(nested, dict) else plan


def _nonempty_strings(value: Any) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) and item.strip() for item in value)
    )


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

    return errors


def primary_signature(plan: dict[str, Any]) -> set[tuple[str, str, str]]:
    contract = _contract(plan)
    return {
        (str(item.get("id")), str(item.get("axis")), str(item.get("target_strength")))
        for item in contract.get("invariants", [])
        if isinstance(item, dict) and item.get("role") == "primary"
    }


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
