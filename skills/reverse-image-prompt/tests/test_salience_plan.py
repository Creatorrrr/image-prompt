#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import sys
import unittest
from copy import deepcopy
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

from color_language import compose_controlled_descriptor
from salience_plan import (
    BASE_SPATIAL_DIMENSIONS,
    HUMAN_SPATIAL_DIMENSIONS,
    SPATIAL_COVERAGE_SCHEMA_VERSION,
    SPATIAL_DIMENSION_FAMILIES,
    audit_plan,
    audit_standalone_prompt_text,
    compare_plans,
)


STANDALONE_SPATIAL_TARGETS = {
    "frame-placement": "the subject sits slightly left of frame center",
    "subject-principal-axis": "the subject has a diagonal principal axis rising toward viewer-right",
    "viewpoint-elevation": "a low upward-looking camera viewpoint",
    "viewpoint-azimuth": "a three-quarter camera view from viewer-left",
    "viewpoint-roll": "a slight clockwise camera roll",
    "viewpoint-distance-foreshortening": "close camera distance with visible near-side enlargement",
    "human-torso-yaw": "the torso turns three-quarters toward viewer-left",
    "human-torso-pitch": "the torso leans slightly back",
    "human-torso-roll": "the torso axis tilts toward viewer-right",
    "human-head-body-yaw": "the head turns farther toward viewer-left than the torso",
    "human-head-body-pitch": "the chin tilts upward relative to the torso",
    "human-head-body-roll": "the head tilts toward viewer-left relative to the torso",
    "human-head-body-lateral-offset": "the head sits slightly viewer-left of the torso axis",
    "human-shoulder-image-slope": "the shoulder line slopes downward toward viewer-right",
    "human-shoulder-depth-order": "the viewer-right shoulder sits farther back",
    "human-attention-direction": "the gaze aims above and past viewer-left",
    "cross-component-orientation": "the two components keep visibly offset diagonal axes",
}


def valid_plan() -> dict:
    return {
        "direct_appeal_read": "A restrained balance between a simple central form and a rough surrounding field.",
        "render_contract": {
            "mode": "appearance-led",
            "invariants": [
                {
                    "id": "silhouette-transition",
                    "axis": "form",
                    "role": "primary",
                    "observation": "one compact silhouette with gradual width transitions",
                    "causal_origin": "intrinsic",
                    "target_strength": "moderate",
                    "source_evidence": ["continuous outer boundary"],
                    "clause_owner": "subject.generic-object",
                },
                {
                    "id": "field-balance",
                    "axis": "hierarchy",
                    "role": "primary",
                    "observation": "the central form remains smaller than the surrounding field",
                    "causal_origin": "spatial-relation",
                    "target_strength": "subtle",
                    "source_evidence": ["broad low-detail area around the subject"],
                    "clause_owner": "core.frame-coordinates",
                },
            ],
            "flexible_dimensions": ["minor-placement"],
            "major_regions": [
                {
                    "id": "central-form",
                    "role": "dominant",
                    "relative_area": "medium",
                    "attention": "primary",
                    "source_evidence": ["highest local contrast"],
                },
                {
                    "id": "surrounding-field",
                    "role": "supporting",
                    "relative_area": "large",
                    "attention": "background",
                    "source_evidence": ["largest continuous low-detail region"],
                },
            ],
            "component_relations": [
                {
                    "id": "central-field-relation",
                    "kind": "frame-zone",
                    "subject_region_id": "central-form",
                    "frame_reference": "full frame",
                    "observation": "the compact form remains nested inside a broader surrounding field",
                    "role": "primary",
                    "source_evidence": ["surrounding field remains visible on every side"],
                },
                {
                    "id": "minor-placement-relation",
                    "kind": "axis-offset",
                    "subject_region_id": "central-form",
                    "frame_reference": "frame centerline",
                    "observation": "a small source-supported offset may vary without changing the hierarchy",
                    "role": "supporting",
                    "source_evidence": ["minor displacement within the surrounding field"],
                },
            ],
            "candidate_claims": [
                {
                    "id": "claim-form",
                    "semantic_slot": "silhouette-transition",
                    "owner": "subject.generic-object",
                    "role": "primary",
                    "polarity": "affirmative",
                    "target_strength": "moderate",
                    "source_kind": "translated-causal-control",
                    "source_evidence": ["continuous outer boundary"],
                    "emit": True,
                    "salience_effects": [
                        {
                            "aggregate_effect_id": "compact-silhouette-effect",
                            "source_evidence": ["continuous outer boundary"],
                        }
                    ],
                },
                {
                    "id": "claim-balance",
                    "semantic_slot": "field-balance",
                    "owner": "core.frame-coordinates",
                    "role": "primary",
                    "polarity": "affirmative",
                    "target_strength": "subtle",
                    "source_kind": "visible-evidence",
                    "source_evidence": ["broad low-detail area around the subject"],
                    "emit": True,
                    "salience_effects": [
                        {
                            "aggregate_effect_id": "field-balance-effect",
                            "source_evidence": ["broad low-detail area around the subject"],
                        }
                    ],
                },
                {
                    "id": "claim-placement",
                    "semantic_slot": "minor-placement",
                    "owner": "core.frame-coordinates",
                    "role": "supporting",
                    "polarity": "affirmative",
                    "target_strength": "subtle",
                    "source_kind": "visible-evidence",
                    "source_evidence": ["small offset from frame center"],
                    "emit": True,
                    "salience_effects": [
                        {
                            "aggregate_effect_id": "minor-placement-effect",
                            "source_evidence": ["small offset from frame center"],
                        }
                    ],
                },
            ],
            "aggregate_effects": [
                {
                    "id": "compact-silhouette-effect",
                    "axis": "form",
                    "direction": "compact-silhouette-with-gradual-transitions",
                    "role": "primary",
                    "target_strength": "moderate",
                    "claim_ids": ["claim-form"],
                    "region_ids": ["central-form"],
                    "relation_ids": [],
                    "source_supported": True,
                    "source_evidence": ["continuous outer boundary"],
                },
                {
                    "id": "field-balance-effect",
                    "axis": "hierarchy",
                    "direction": "compact-form-subordinate-to-broader-field",
                    "role": "primary",
                    "target_strength": "subtle",
                    "claim_ids": ["claim-balance"],
                    "region_ids": ["central-form", "surrounding-field"],
                    "relation_ids": ["central-field-relation"],
                    "source_supported": True,
                    "source_evidence": ["broad low-detail area around the subject"],
                },
                {
                    "id": "minor-placement-effect",
                    "axis": "hierarchy",
                    "direction": "small-source-relative-frame-offset",
                    "role": "supporting",
                    "target_strength": "subtle",
                    "claim_ids": ["claim-placement"],
                    "region_ids": ["central-form"],
                    "relation_ids": ["minor-placement-relation"],
                    "source_supported": True,
                    "source_evidence": ["small offset from frame center"],
                },
            ],
            "emitted_controls": [
                {
                    "id": "control-form",
                    "prompt_excerpt": "a compact silhouette with gradual width transitions",
                    "claim_id": "claim-form",
                    "owner": "subject.generic-object",
                    "aggregate_effect_ids": ["compact-silhouette-effect"],
                },
                {
                    "id": "control-balance",
                    "prompt_excerpt": "the form remains smaller than the surrounding field",
                    "claim_id": "claim-balance",
                    "owner": "core.frame-coordinates",
                    "aggregate_effect_ids": ["field-balance-effect"],
                },
                {
                    "id": "control-placement",
                    "prompt_excerpt": "a small offset from the frame center",
                    "claim_id": "claim-placement",
                    "owner": "core.frame-coordinates",
                    "aggregate_effect_ids": ["minor-placement-effect"],
                },
            ],
            "prior_clusters": [
                {
                    "id": "ordinary-capture",
                    "claim_ids": ["claim-balance"],
                    "source_supported": True,
                }
            ],
        },
    }


def authored_prompt_text(plan: dict) -> str:
    contract = plan["render_contract"]
    color_contract = contract.get("color_tone_contract", {})
    light_contract = contract.get("light_form_contract", {})
    surface_language = color_contract.get("surface_color_language", {})
    descriptor = surface_language.get("controlled_descriptor", {})
    composed_control_ids = (
        set(descriptor.get("axis_control_ids", {}).values())
        if descriptor.get("emit") is True
        else set()
    )
    generic_controls = contract.get("emitted_controls", [])
    color_controls = color_contract.get("emitted_controls", [])
    light_controls = light_contract.get("emitted_controls", [])
    all_controls = {
        item["id"]: item
        for item in [*generic_controls, *color_controls, *light_controls]
        if isinstance(item, dict) and item.get("id") and item.get("prompt_excerpt")
    }
    excerpts: list[str] = []
    used_control_ids: set[str] = set(composed_control_ids)

    emitted_clusters = [
        cluster
        for cluster in contract.get("prior_clusters", [])
        if isinstance(cluster, dict)
        and cluster.get("schema_version") == "prior-cluster/v2"
        and cluster.get("disposition") == "emit"
    ]
    cluster_by_summary = {
        cluster.get("summary_control_id"): cluster for cluster in emitted_clusters
    }
    cluster_decomposed_ids = {
        control_id
        for cluster in emitted_clusters
        for control_id in cluster.get("decomposed_control_ids", [])
    }
    for control in generic_controls:
        control_id = control.get("id")
        if control_id in used_control_ids or control_id in cluster_decomposed_ids:
            continue
        excerpts.append(control["prompt_excerpt"])
        used_control_ids.add(control_id)
        cluster = cluster_by_summary.get(control_id)
        if cluster is not None:
            for decomposed_id in cluster.get("decomposed_control_ids", []):
                decomposed = all_controls.get(decomposed_id)
                if decomposed is not None and decomposed_id not in used_control_ids:
                    excerpts.append(decomposed["prompt_excerpt"])
                    used_control_ids.add(decomposed_id)

    lighting_labels = light_contract.get("lighting_labels", [])
    for lighting_label in (
        lighting_labels if isinstance(lighting_labels, list) else []
    ):
        if not isinstance(lighting_label, dict) or lighting_label.get("emit") is not True:
            continue
        excerpts.append(lighting_label["phrase"])
        for control_id in lighting_label.get("decomposed_control_ids", []):
            control = all_controls.get(control_id)
            if control is not None and control_id not in used_control_ids:
                excerpts.append(control["prompt_excerpt"])
                used_control_ids.add(control_id)
    for control in light_controls:
        if control.get("id") not in used_control_ids:
            excerpts.append(control["prompt_excerpt"])
            used_control_ids.add(control.get("id"))

    appearance_metaphors = color_contract.get("appearance_metaphors", [])
    for metaphor in (
        appearance_metaphors if isinstance(appearance_metaphors, list) else []
    ):
        if not isinstance(metaphor, dict) or metaphor.get("emit") is not True:
            continue
        excerpts.append(metaphor["phrase"])
        for control_id in metaphor.get("decomposed_control_ids", []):
            control = all_controls.get(control_id)
            if control is not None and control_id not in used_control_ids:
                excerpts.append(control["prompt_excerpt"])
                used_control_ids.add(control_id)
    for control in color_controls:
        if control.get("id") not in used_control_ids:
            excerpts.append(control["prompt_excerpt"])
            used_control_ids.add(control.get("id"))

    if descriptor.get("emit") is True:
        excerpts.append(descriptor["phrase"])
    return "PROMPT:\n" + ". ".join(excerpts)


def add_generic_claim(
    contract: dict,
    *,
    invariant_id: str,
    axis: str,
    owner: str,
    role: str,
    target_strength: str,
    observation: str,
    causal_origin: str,
    evidence: str,
    direction: str,
    prompt_excerpt: str,
    region_ids: list[str] | None = None,
    relation_ids: list[str] | None = None,
) -> None:
    claim_id = f"claim-{invariant_id}"
    effect_id = f"effect-{invariant_id}"
    contract["invariants"].append(
        {
            "id": invariant_id,
            "axis": axis,
            "role": role,
            "observation": observation,
            "causal_origin": causal_origin,
            "target_strength": target_strength,
            "source_evidence": [evidence],
            "clause_owner": owner,
        }
    )
    contract["candidate_claims"].append(
        {
            "id": claim_id,
            "semantic_slot": invariant_id,
            "owner": owner,
            "role": role,
            "polarity": "affirmative",
            "target_strength": target_strength,
            "source_kind": "visible-evidence",
            "source_evidence": [evidence],
            "emit": True,
            "salience_effects": [
                {
                    "aggregate_effect_id": effect_id,
                    "source_evidence": [evidence],
                }
            ],
        }
    )
    contract["aggregate_effects"].append(
        {
            "id": effect_id,
            "axis": axis,
            "direction": direction,
            "role": role,
            "target_strength": target_strength,
            "claim_ids": [claim_id],
            "region_ids": region_ids or [],
            "relation_ids": relation_ids or [],
            "source_supported": True,
            "source_evidence": [evidence],
        }
    )
    contract["emitted_controls"].append(
        {
            "id": f"control-{invariant_id}",
            "prompt_excerpt": prompt_excerpt,
            "claim_id": claim_id,
            "owner": owner,
            "aggregate_effect_ids": [effect_id],
        }
    )


def with_spatial_coverage(
    plan: dict,
    *,
    kind: str = "human",
    visibility: str = "readable",
) -> dict:
    """Add a direction-neutral coverage ledger to a synthetic plan."""

    contract = plan["render_contract"]
    plan["routing"] = {
        "resolved_non_core_modules": [
            "subject.human" if kind == "human" else "subject.generic-object"
        ]
    }
    dimensions = set(BASE_SPATIAL_DIMENSIONS)
    if kind == "human":
        dimensions |= HUMAN_SPATIAL_DIMENSIONS
    origins = {
        "frame-placement": "spatial-relation",
        "subject-principal-axis": "spatial-relation",
        "viewpoint-elevation": "perspective",
        "viewpoint-azimuth": "perspective",
        "viewpoint-roll": "perspective",
        "viewpoint-distance-foreshortening": "perspective",
        "human-torso-yaw": "pose-deformation",
        "human-torso-pitch": "pose-deformation",
        "human-torso-roll": "pose-deformation",
        "human-head-body-yaw": "pose-deformation",
        "human-head-body-pitch": "pose-deformation",
        "human-head-body-roll": "pose-deformation",
        "human-head-body-lateral-offset": "spatial-relation",
        "human-shoulder-image-slope": "pose-deformation",
        "human-shoulder-depth-order": "spatial-relation",
        "human-attention-direction": "pose-deformation",
        "cross-component-orientation": "spatial-relation",
    }
    evidence_cues = [
        {
            "id": f"cue-{dimension}",
            "subject_id": "subject-a",
            "family": (
                "frame-placement"
                if dimension == "frame-placement"
                else "perspective"
                if dimension.startswith("viewpoint-")
                else "attention"
                if dimension == "human-attention-direction"
                else "axis-relation"
            ),
            "observation": f"held-out source-visible cue for {dimension}",
            "source_evidence": [f"held-out evidence for {dimension}"],
            "confounders": [],
        }
        for dimension in sorted(dimensions)
    ]
    contract["spatial_orientation_coverage"] = {
        "schema_version": SPATIAL_COVERAGE_SCHEMA_VERSION,
        "subjects": [
            {
                "id": "subject-a",
                "kind": kind,
                "visibility": visibility,
                "region_id": "central-form",
                "source_evidence": ["held-out source-visible subject region"],
            }
        ],
        "evidence_cues": evidence_cues,
        "counterfactual_checks": (
            [
                {
                    "id": "counterfactual-subject-a-whole",
                    "subject_id": "subject-a",
                    "scope": "whole-orientation",
                    "tested_change": "replace the source relation with neutral axial alignment",
                    "verdict": "not-material",
                    "changed_relations": [],
                    "preserved_relations": [
                        "the held-out proposition survives neutral alignment"
                    ],
                    "evidence_cue_ids": [
                        item["id"]
                        for item in evidence_cues
                        if item["family"] != "frame-placement"
                    ],
                    "neutralized_decision_ids": [
                        f"coverage-{dimension}"
                        for dimension in sorted(dimensions - {"frame-placement"})
                    ],
                    "held_fixed_decision_ids": [],
                    "source_evidence": [
                        "held-out comparison against neutral axial alignment"
                    ],
                },
                {
                    "id": "counterfactual-subject-a-residual",
                    "subject_id": "subject-a",
                    "scope": "residual-alignment",
                    "tested_change": "hold viewpoint fixed and neutralize residual human pose alignment",
                    "verdict": "not-material",
                    "changed_relations": [],
                    "preserved_relations": [
                        "the held-out proposition survives residual pose neutralization"
                    ],
                    "evidence_cue_ids": [
                        item["id"]
                        for item in evidence_cues
                        if item["family"] != "frame-placement"
                    ],
                    "neutralized_decision_ids": [
                        f"coverage-{dimension}"
                        for dimension in sorted(HUMAN_SPATIAL_DIMENSIONS - {"human-attention-direction"})
                    ],
                    "held_fixed_decision_ids": [
                        f"coverage-{dimension}"
                        for dimension in sorted(
                            {
                                "viewpoint-elevation",
                                "viewpoint-azimuth",
                                "viewpoint-roll",
                                "viewpoint-distance-foreshortening",
                            }
                        )
                    ],
                    "source_evidence": [
                        "held-out comparison with viewpoint held fixed"
                    ],
                }
            ]
            if kind == "human"
            else []
        ),
        "coupled_effects": [],
        "prompt_effect_audits": [],
        "decisions": [
            {
                "id": f"coverage-{dimension}",
                "subject_id": "subject-a",
                "dimension": dimension,
                "family": SPATIAL_DIMENSION_FAMILIES[dimension],
                "disposition": "not-material",
                "observation": f"the held-out source does not make {dimension} material",
                "causal_origin": origins[dimension],
                "confidence": "high",
                "source_evidence": [f"held-out evidence for {dimension}"],
                "evidence_cue_ids": [f"cue-{dimension}"],
                "control_axis_id": f"subject-a/{dimension}",
                "non_emission_reason": "no separate prompt control is warranted",
                "neutralization_test": {
                    "test_scope": (
                        "single-dimension-with-adjacent-spatial-relations-held"
                    ),
                    "tested_change": (
                        f"neutralize only {dimension} while holding adjacent relations"
                    ),
                    "verdict": "preserved",
                    "preserved_relations": [
                        "the held-out visible proposition and adjacent relations survive"
                    ],
                    "changed_relations": [],
                    "held_fixed_decision_ids": [
                        f"coverage-{held_dimension}"
                        for held_dimension in sorted(dimensions - {dimension})
                    ],
                    "evidence_cue_ids": [f"cue-{dimension}"],
                    "confidence": "high",
                    "source_evidence": [
                        f"held-out isolated neutralization evidence for {dimension}"
                    ],
                },
            }
            for dimension in sorted(dimensions)
        ],
    }
    if kind == "human":
        contract["human_appearance_decisions"] = [
            {
                "id": "appearance-subject-a",
                "schema_version": "human-appearance/v3",
                "subject_id": "subject-a",
                "face_visibility": visibility,
                "frame_prominence": "secondary",
                "fidelity_salience": "not-material",
                "appearance_invariant_ids": [],
                "source_evidence": ["held-out source-visible human appearance"],
                "identity_context": {
                    "disposition": "absent",
                    "context_use": "none",
                    "prompt_disposition": "omit",
                    "viewer_priority": "not-material",
                },
                "person_prior": {
                    "disposition": "omit",
                    "confidence": "high",
                    "candidate_support": "unsupported",
                    "default_drift_risk": "low",
                    "local_geometry_sufficiency": "uncertain",
                    "geometry_claim_ids": [],
                    "source_evidence": ["no broad person prior is material in this fixture"],
                    "non_emission_reason": "local visible geometry is sufficient",
                    "omission_counterfactual": {
                        "verdict": "preserved",
                        "source_evidence": ["appearance is not material in this held-out fixture"],
                    },
                },
                "appearance_gestalt": {
                    "scope": "person-aesthetic",
                    "disposition": "omit",
                    "confidence": "high",
                    "candidate_support": "unsupported",
                    "viewer_priority": "not-material",
                    "default_drift_risk": "low",
                    "source_evidence": [
                        "no aggregate person aesthetic is material in this fixture"
                    ],
                    "decomposition_control_ids": [],
                    "effect_budget": {
                        "intended_dimensions": [],
                        "protected_dimensions": ["identity-context"],
                        "source_evidence": [
                            "the omitted aggregate cannot alter identity context"
                        ],
                    },
                    "non_emission_reason": (
                        "no P0 or P1 aggregate person aesthetic is supported"
                    ),
                    "omission_counterfactual": {
                        "verdict": "preserved",
                        "source_evidence": [
                            "omitting an aggregate person aesthetic preserves this fixture"
                        ],
                    },
                },
                "skin_surface": {
                    "disposition": "not-material",
                    "viewer_priority": "not-material",
                    "observation_scope": "source-visible",
                    "semantic_use": "displayed-surface",
                    "confidence": "high",
                    "source_evidence": ["skin color does not carry this fixture's proposition"],
                    "region_ids": [],
                    "descriptor_disposition": "omit",
                    "non_emission_reason": "skin surface is not material",
                    "descriptor_non_emission_reason": "no skin descriptor is warranted",
                },
            }
        ]
    return plan


def promote_spatial_decision(
    plan: dict,
    dimension: str,
    *,
    direction: str = "held-out-source-relative-direction",
    prompt_excerpt: str | None = None,
) -> dict:
    """Give one coverage decision a complete source-relative actuation path.

    Internal direction metadata may remain source-relative. The emitted fixture
    always uses a self-contained visible target.
    """

    contract = plan["render_contract"]
    decision = next(
        item
        for item in contract["spatial_orientation_coverage"]["decisions"]
        if item["dimension"] == dimension
    )
    relation_id = f"relation-{dimension}"
    invariant_id = f"spatial-{dimension}"
    relation_kind = {
        "frame-placement": "frame-zone",
        "principal-axis": "principal-axis",
        "viewpoint": "viewpoint",
        "part-whole": "part-whole-orientation",
        "attention-direction": "attention-direction",
        "cross-component": "cross-component-orientation",
    }[decision["family"]]
    contract["component_relations"].append(
        {
            "id": relation_id,
            "kind": relation_kind,
            "subject_region_id": "central-form",
            "frame_reference": "source-relative frame and visible subject",
            "observation": direction,
            "role": "primary",
            "source_evidence": [f"held-out source evidence for {dimension}"],
        }
    )
    add_generic_claim(
        contract,
        invariant_id=invariant_id,
        axis="hierarchy" if dimension in {"frame-placement", "cross-component-orientation"} else "form",
        owner="subject.human" if dimension.startswith("human-") else "core.frame-coordinates",
        role="primary",
        target_strength="moderate",
        observation=direction,
        causal_origin=decision["causal_origin"],
        evidence=f"held-out source evidence for {dimension}",
        direction=direction,
        prompt_excerpt=prompt_excerpt or STANDALONE_SPATIAL_TARGETS[dimension],
        region_ids=["central-form"],
        relation_ids=[relation_id],
    )
    effect_id = f"effect-{invariant_id}"
    control_id = f"control-{invariant_id}"
    effect = next(
        item for item in contract["aggregate_effects"] if item["id"] == effect_id
    )
    control = next(
        item for item in contract["emitted_controls"] if item["id"] == control_id
    )
    for item in (effect, control):
        item["control_axis_id"] = decision["control_axis_id"]
        item["causal_origin"] = decision["causal_origin"]
    decision.update(
        {
            "disposition": "invariant",
            "observation": direction,
            "source_evidence": [f"held-out source evidence for {dimension}"],
            "relation_id": relation_id,
            "invariant_id": invariant_id,
            "claim_id": f"claim-{invariant_id}",
            "aggregate_effect_id": effect_id,
            "control_id": control_id,
        }
    )
    decision.pop("non_emission_reason", None)
    decision.pop("neutralization_test", None)
    decision.pop("visibility_limit", None)
    contract["spatial_orientation_coverage"]["prompt_effect_audits"].append(
        {
            "id": f"prompt-effect-{control_id}",
            "control_id": control_id,
            "subject_id": decision["subject_id"],
            "effect_scope": "explicit-and-implicit-spatial-effects",
            "prompt_excerpt": control["prompt_excerpt"],
            "explicit_decision_ids": [decision["id"]],
            "implicit_decision_ids": [],
            "verdict": "source-consistent",
            "rationale": "the source-relative clause actuates only its owned spatial axis",
            "source_evidence": decision["source_evidence"],
        }
    )
    return plan


def promote_coupled_orientation(
    plan: dict,
    *,
    member_dimensions: tuple[str, ...] = (
        "human-torso-yaw",
        "human-head-body-yaw",
        "human-shoulder-depth-order",
    ),
    result_direction: str = "source-relative coupled orientation result",
    summary_excerpt: str = "the torso, head, and shoulder depth form one three-quarter turn toward viewer-left",
    summary_adequacy: str = "lossy",
    residual_dimensions: tuple[str, ...] | None = None,
) -> dict:
    """Merge weak decisions under one summary plus owned residual actuations."""

    contract = plan["render_contract"]
    coverage = contract["spatial_orientation_coverage"]
    subject_kind = coverage["subjects"][0]["kind"]
    member_decisions = [
        next(
            decision
            for decision in coverage["decisions"]
            if decision["dimension"] == dimension
        )
        for dimension in member_dimensions
    ]
    if residual_dimensions is None:
        residual_dimensions = member_dimensions if summary_adequacy != "sufficient" else ()
    residual_dimension_set = set(residual_dimensions)
    residual_excerpts = {
        dimension: STANDALONE_SPATIAL_TARGETS[dimension]
        for dimension in residual_dimensions
    }
    prompt_excerpt = ". ".join(
        [summary_excerpt, *(residual_excerpts[dimension] for dimension in residual_dimensions)]
    )
    for decision in member_decisions:
        dimension = decision["dimension"]
        decision["observation"] = f"source-visible weak contribution for {dimension}"
        decision["source_evidence"] = [f"held-out weak cue for {dimension}"]
    relation_id = "relation-coupled-orientation"
    invariant_id = "coupled-orientation"
    effect_id = "effect-coupled-orientation"
    control_id = "control-coupled-orientation"
    control_axis_id = "subject-a/coupled-orientation"
    contract["component_relations"].append(
        {
            "id": relation_id,
            "kind": "part-whole-orientation",
            "subject_region_id": "central-form",
            "frame_reference": "source-relative visible subject axes",
            "observation": result_direction,
            "role": "primary",
            "source_evidence": ["jointly readable held-out pose cues"],
        }
    )
    add_generic_claim(
        contract,
        invariant_id=invariant_id,
        axis="form",
        owner="subject.human" if subject_kind == "human" else "core.frame-coordinates",
        role="primary",
        target_strength="moderate",
        observation=result_direction,
        causal_origin="pose-deformation",
        evidence="jointly readable held-out pose cues",
        direction=result_direction,
        prompt_excerpt=prompt_excerpt,
        region_ids=["central-form"],
        relation_ids=[relation_id],
    )
    effect = next(
        item for item in contract["aggregate_effects"] if item["id"] == effect_id
    )
    control = next(
        item for item in contract["emitted_controls"] if item["id"] == control_id
    )
    for item in (effect, control):
        item["control_axis_id"] = control_axis_id
        item["causal_origin"] = "pose-deformation"
    coverage["coupled_effects"].append(
        {
            "id": "coupled-subject-a",
            "subject_id": "subject-a",
            "member_decision_ids": [item["id"] for item in member_decisions],
            "evidence_cue_ids": [
                cue_id
                for item in member_decisions
                for cue_id in item["evidence_cue_ids"]
            ],
            "visible_result": "the weak cues jointly establish one non-neutral orientation",
            "result_direction": result_direction,
            "result_direction_confidence": "medium",
            "physical_attribution": "confounded",
            "confounders": ["individual pose axes are weak in isolation"],
            "causal_origin": "pose-deformation",
            "disposition": "invariant",
            "role": "primary",
            "target_strength": "moderate",
            "source_evidence": ["jointly readable held-out pose cues"],
            "control_axis_id": control_axis_id,
            "relation_id": relation_id,
            "invariant_id": invariant_id,
            "claim_id": f"claim-{invariant_id}",
            "aggregate_effect_id": effect_id,
            "control_id": control_id,
            "prompt_decomposition": {
                "summary_anchor": {
                    "visible_result": "the source-relative orientation remains one coherent whole",
                    "prompt_excerpt": summary_excerpt,
                    "source_evidence": ["jointly readable held-out pose cues"],
                },
                "summary_adequacy": {
                    "verdict": summary_adequacy,
                    "at_risk_decision_ids": [
                        item["id"]
                        for item in member_decisions
                        if item["dimension"] in residual_dimension_set
                    ],
                    "rationale": (
                        "the compact summary preserves every material member"
                        if summary_adequacy == "sufficient"
                        else "the compact summary would neutralize source-visible residual relations"
                    ),
                    "source_evidence": ["summary-only neutralization comparison"],
                    **(
                        {
                            "uncertainty_note": (
                                "the macro summary's member coverage is not fully "
                                "separable from the visible evidence"
                            )
                        }
                        if summary_adequacy == "uncertain"
                        else {}
                    ),
                },
                "member_actuations": [
                    {
                        "decision_id": item["id"],
                        "summary_coverage": (
                            "lost"
                            if item["dimension"] in residual_dimension_set
                            else "complete"
                        ),
                        "visible_result": item["observation"],
                        "source_evidence": item["source_evidence"],
                        **(
                            {"prompt_excerpt": residual_excerpts[item["dimension"]]}
                            if item["dimension"] in residual_dimension_set
                            else {
                                "non_emission_reason": (
                                    "the summary anchor preserves this member without an extra clause"
                                )
                            }
                        ),
                    }
                    for item in member_decisions
                ],
            },
            "prompt_order_after_control_ids": [],
            "prompt_order_before_control_ids": ["control-form"],
            "net_effect_audit": {
                "included_control_ids": [control_id],
                "verdict": "source-consistent",
                "rationale": "one coupled control preserves the joint result without separately amplifying its weak members",
                "source_evidence": ["jointly readable held-out pose cues"],
            },
        }
    )
    coverage["prompt_effect_audits"].append(
        {
            "id": "prompt-effect-control-coupled-orientation",
            "control_id": control_id,
            "subject_id": "subject-a",
            "effect_scope": "explicit-and-implicit-spatial-effects",
            "prompt_excerpt": control["prompt_excerpt"],
            "explicit_decision_ids": [item["id"] for item in member_decisions],
            "implicit_decision_ids": [],
            "verdict": "source-consistent",
            "rationale": "the coupled clause preserves only its source-supported member result",
            "source_evidence": ["jointly readable held-out pose cues"],
        }
    )
    residual = next(
        (
            item
            for item in coverage["counterfactual_checks"]
            if item["scope"] == "residual-alignment"
        ),
        None,
    )
    if residual is not None:
        residual.update(
            {
                "verdict": "material",
                "changed_relations": [
                    "residual neutralization removes the jointly readable orientation"
                ],
                "preserved_relations": [],
            }
        )
    return plan


def with_material_human_appearance_omission(
    plan: dict,
    *,
    drift_risk: str = "high",
    geometry_sufficiency: str = "insufficient",
    counterfactual: str = "material-drift",
) -> dict:
    """Create a readable secondary person whose appearance is fidelity-primary."""

    plan = with_spatial_coverage(plan)
    contract = plan["render_contract"]
    add_generic_claim(
        contract,
        invariant_id="held-out-person-geometry",
        axis="form",
        owner="detail.human-face-likeness",
        role="primary",
        target_strength="subtle",
        observation="source-visible face silhouette and feature relations",
        causal_origin="intrinsic",
        evidence="held-out readable face geometry",
        direction="source-relative-face-geometry",
        prompt_excerpt="the visible face silhouette and feature relations",
        region_ids=["central-form"],
    )
    decision = contract["human_appearance_decisions"][0]
    decision.update(
        {
            "frame_prominence": "secondary",
            "fidelity_salience": "primary",
            "appearance_invariant_ids": ["held-out-person-geometry"],
        }
    )
    decision["person_prior"].update(
        {
            "candidate_support": "uncertain",
            "default_drift_risk": drift_risk,
            "local_geometry_sufficiency": geometry_sufficiency,
            "geometry_claim_ids": ["claim-held-out-person-geometry"],
            "omission_counterfactual": {
                "verdict": counterfactual,
                "source_evidence": ["held-out neutral-prior comparison"],
            },
            "non_emission_reason": "testing explicit omission gate",
        }
    )
    return plan


def with_emitted_person_aesthetic(plan: dict) -> dict:
    """Add one source-qualified person aesthetic and cross-module decomposition."""

    plan = with_spatial_coverage(plan)
    contract = plan["render_contract"]
    additions = [
        (
            "person-aesthetic-summary",
            "hierarchy",
            "subject.human",
            "one material source-relative person aesthetic",
            "source-relative-person-aesthetic",
            "a bounded restrained editorial person aesthetic",
            None,
        ),
        (
            "person-face-form",
            "form",
            "detail.human-face-likeness",
            "source-specific face form constrains the aesthetic",
            "source-relative-person-face-form",
            "visible face form constrains that aesthetic",
            "face-form",
        ),
        (
            "person-hair-boundary",
            "form",
            "detail.human-face-likeness",
            "source-specific hair mass and occlusion constrain the aesthetic",
            "source-relative-person-hair-boundary",
            "the visible hair mass and face occlusion remain authoritative",
            "hair-boundary",
        ),
        (
            "person-garment-coverage",
            "form",
            "detail.clothing-fashion",
            "source-specific garment coverage constrains the aesthetic",
            "source-relative-person-garment-coverage",
            "the visible garment coverage and construction legibility remain bounded",
            "garment-coverage",
        ),
        (
            "person-capture-treatment",
            "sharpness",
            "medium.photographic-capture",
            "source-specific softness and polish ceiling constrain the aesthetic",
            "source-relative-person-capture-treatment",
            "soft capture and a restrained polish ceiling remain unchanged",
            "capture-treatment",
        ),
    ]
    for (
        invariant_id,
        axis,
        owner,
        observation,
        direction,
        excerpt,
        appearance_dimension,
    ) in additions:
        add_generic_claim(
            contract,
            invariant_id=invariant_id,
            axis=axis,
            owner=owner,
            role="primary",
            target_strength="moderate",
            observation=observation,
            causal_origin="processing" if axis == "sharpness" else "intrinsic",
            evidence=f"held-out current-source evidence for {invariant_id}",
            direction=direction,
            prompt_excerpt=excerpt,
            region_ids=["central-form"],
        )
        if appearance_dimension is not None:
            contract["emitted_controls"][-1][
                "appearance_dimension"
            ] = appearance_dimension

    decomposition_control_ids = [
        "control-person-face-form",
        "control-person-hair-boundary",
        "control-person-garment-coverage",
        "control-person-capture-treatment",
    ]
    summary_claim = next(
        claim
        for claim in contract["candidate_claims"]
        if claim["id"] == "claim-person-aesthetic-summary"
    )
    summary_claim["generation_prior"] = {
        "scope": "person-aesthetic",
        "candidate_source": {
            "kind": "source-visible-approximation",
            "reference": "held-out current-source observation",
        },
        "non_identifying": True,
        "visible_appearance_evidence": [
            "the overall person styling remains independently readable"
        ],
        "decomposed_control_ids": decomposition_control_ids,
    }

    decision = contract["human_appearance_decisions"][0]
    decision.update(
        {
            "fidelity_salience": "primary",
            "appearance_invariant_ids": [item[0] for item in additions],
        }
    )
    decision["person_prior"].update(
        {
            "default_drift_risk": "low",
            "local_geometry_sufficiency": "sufficient",
            "geometry_claim_ids": ["claim-person-face-form"],
            "omission_counterfactual": {
                "verdict": "preserved",
                "source_evidence": [
                    "the separate face-form control preserves non-demographic geometry"
                ],
            },
        }
    )
    decision["appearance_gestalt"] = {
        "scope": "person-aesthetic",
        "disposition": "emit",
        "confidence": "high",
        "candidate_support": "supported",
        "viewer_priority": "P0",
        "default_drift_risk": "high",
        "source_evidence": [
            "the held-out person aesthetic is independently source-material"
        ],
        "claim_id": "claim-person-aesthetic-summary",
        "decomposition_control_ids": decomposition_control_ids,
        "effect_budget": {
            "intended_dimensions": [
                "face-form",
                "hair-boundary",
                "garment-coverage",
                "capture-treatment",
            ],
            "protected_dimensions": [
                "identity-context",
                "pose-occlusion",
                "scale-crop",
                "age-presentation",
            ],
            "source_evidence": [
                "the aggregate direction is bounded by independent visible controls"
            ],
        },
        "omission_counterfactual": {
            "verdict": "material-drift",
            "source_evidence": [
                "detail-only wording loses the material overall person aesthetic"
            ],
        },
    }
    return plan


def valid_color_plan() -> dict:
    plan = valid_plan()
    contract = plan["render_contract"]
    contract["invariants"].append(
        {
            "id": "surface-tone",
            "axis": "color",
            "role": "primary",
            "observation": "the central field stays visibly lighter than the surround",
            "causal_origin": "intrinsic",
            "target_strength": "moderate",
            "source_evidence": ["consistent central midtone across a broad region"],
            "clause_owner": "detail.color-tone-fidelity",
        }
    )
    contract["candidate_claims"].append(
        {
            "id": "claim-surface-tone",
            "semantic_slot": "surface-tone",
            "owner": "detail.color-tone-fidelity",
            "role": "primary",
            "polarity": "affirmative",
            "target_strength": "moderate",
            "source_kind": "translated-causal-control",
            "source_evidence": ["central field is lighter than the surround"],
            "emit": True,
            "perceptual_effects": [
                {
                    "aggregate_effect_id": "central-value-relation",
                    "causal_layer": "intrinsic",
                    "confidence": "high",
                    "source_evidence": ["broad central value remains consistently higher"],
                }
            ],
        }
    )
    contract["color_tone_contract"] = {
        "importance": "primary",
        "observation_scope": "source-visible",
        "global": {
            "cast_or_palette_shift": "no strong global shift is visible",
            "exposure_behavior": "the central field retains highlight detail",
            "contrast_and_tone_curve": "moderate global range with soft local transitions",
            "processing_shift": "no strong selective color grade is visible",
            "source_evidence": ["surrounding low-chroma field remains stable"],
        },
        "regions": [
            {
                "id": "central-form",
                "prompt_anchor": "central form",
                "role": "dominant",
                "intrinsic_axes": [
                    {
                        "axis": "value",
                        "role": "primary",
                        "evidence_scope": "flat",
                        "emission": "required",
                        "aggregate_effect_id": "central-value-relation",
                        "observation": "lighter than the surrounding field",
                        "confidence": "high",
                        "source_evidence": ["broad value separation at the boundary"],
                    },
                    {
                        "axis": "chroma",
                        "role": "supporting",
                        "evidence_scope": "flat",
                        "emission": "diagnostic-only",
                        "non_emission_reason": "the visible chroma bias is too weak to justify a separate prompt control",
                        "observation": "restrained rather than vivid",
                        "confidence": "medium",
                        "source_evidence": ["small channel separation across midtones"],
                    },
                    {
                        "axis": "hue",
                        "role": "supporting",
                        "evidence_scope": "flat",
                        "emission": "diagnostic-only",
                        "non_emission_reason": "the near-neutral hue direction is not stable enough to emit",
                        "observation": "near-neutral with a slight source-visible bias",
                        "confidence": "medium",
                        "source_evidence": ["stable hue relationship across the region"],
                    },
                ],
                "tone_zones": [
                    {
                        "zone": "flat",
                        "observation": "mostly even with a gentle value rolloff",
                        "confidence": "high",
                        "source_evidence": ["no distinct hard highlight or shadow band"],
                    }
                ],
                "relative_relations": [
                    "lighter and less contrasty than the surrounding-field region"
                ],
                "source_evidence": ["largest coherent lighter region"],
            }
        ],
        "neutral_anchor_status": "available",
        "uncertainty_note": "",
        "neutral_anchors": [
            {
                "region_id": "surrounding-field",
                "confidence": "medium",
                "source_evidence": ["broad low-chroma background area"],
            }
        ],
        "claim_ids": ["claim-surface-tone"],
        "aggregate_effects": [
            {
                "id": "central-value-relation",
                "region_id": "central-form",
                "axis": "value",
                "direction": "lighter-than-surrounding-field",
                "role": "primary",
                "target_strength": "moderate",
                "claim_ids": ["claim-surface-tone"],
                "source_supported": True,
                "source_evidence": ["broad source-visible value separation"],
            }
        ],
        "emitted_controls": [
            {
                "id": "control-surface-tone",
                "prompt_excerpt": "a central field visibly lighter than the surround",
                "claim_id": "claim-surface-tone",
                "causal_layer": "intrinsic",
                "control_role": "axis-control",
                "region_id": "central-form",
                "axis": "value",
                "aggregate_effect_ids": ["central-value-relation"],
            }
        ],
    }
    return plan


def valid_light_plan() -> dict:
    plan = valid_plan()
    contract = plan["render_contract"]
    contract["invariants"].append(
        {
            "id": "light-shape",
            "axis": "light-to-form",
            "role": "primary",
            "observation": "broad planes remain readable through shallow gradients",
            "causal_origin": "lighting-shadow",
            "target_strength": "moderate",
            "source_evidence": ["large continuous plane with low internal value variation"],
            "clause_owner": "detail.light-form-fidelity",
        }
    )
    contract["candidate_claims"].append(
        {
            "id": "claim-light-shape",
            "semantic_slot": "light-shape",
            "owner": "detail.light-form-fidelity",
            "role": "primary",
            "polarity": "affirmative",
            "target_strength": "moderate",
            "source_kind": "translated-causal-control",
            "source_evidence": ["shallow gradients across the dominant plane"],
            "emit": True,
            "lighting_effects": [
                {
                    "aggregate_effect_id": "dominant-local-form-contrast",
                    "confidence": "high",
                    "source_evidence": ["broad plane retains low internal contrast"],
                }
            ],
        }
    )
    contract["light_form_contract"] = {
        "importance": "primary",
        "observation_scope": "source-visible",
        "observed_result": {
            "global_tonal_range": "wide separation between the central form and surrounding field",
            "local_form_contrast": "subtle",
            "bright_plane_coverage": "broad",
            "gradient_character": "long shallow transitions across the dominant plane",
            "gradient_extent": "long",
            "background_spill_relation": "low",
            "largest_bright_masses": ["central-form"],
            "largest_dark_masses": ["surrounding-field"],
            "source_evidence": ["continuous source-visible value massing"],
        },
        "source_hypothesis": {
            "model_type": "uncertain",
            "source_count": "uncertain",
            "camera_axis_offset": "uncertain",
            "elevation": "uncertain",
            "front_side_back_relation": "the physical source is not uniquely recoverable",
            "apparent_angular_size": "uncertain",
            "fill_structure": "uncertain",
            "confidence": "low",
            "actuation": "result-space-only",
            "source_evidence": ["visible gradient without a decisive cast-shadow direction"],
        },
        "region_effects": [
            {
                "id": "central-broad-plane",
                "region_id": "central-form",
                "reference_region_id": "surrounding-field",
                "role": "broad-plane",
                "value_relation": "internally even relative to the surrounding field",
                "gradient_strength": "subtle",
                "edge_character": "long feathered transition",
                "source_evidence": ["low internal variation across a broad area"],
            }
        ],
        "shadow_events": [],
        "material_responses": [],
        "pose_light_dependency": {
            "geometry_dependency": "pose-robust",
            "preserved_result": "the dominant plane retains shallow light-to-form modeling",
            "flexible_effects": ["the exact highlight coordinate may move"],
            "source_evidence": ["the invariant is regional contrast rather than a point highlight"],
        },
        "claim_ids": ["claim-light-shape"],
        "aggregate_effects": [
            {
                "id": "dominant-local-form-contrast",
                "region_id": "central-form",
                "reference_region_id": "surrounding-field",
                "axis": "local-form-contrast",
                "direction": "shallow-internal-modeling",
                "role": "primary",
                "target_strength": "moderate",
                "claim_ids": ["claim-light-shape"],
                "source_supported": True,
                "source_evidence": ["broad plane retains low internal contrast"],
            }
        ],
        "emitted_controls": [
            {
                "id": "control-light-shape",
                "prompt_excerpt": "broad planes revealed only by long shallow gradients",
                "claim_id": "claim-light-shape",
                "owner": "local-form-contrast",
                "aggregate_effect_ids": ["dominant-local-form-contrast"],
            }
        ],
    }
    return plan


def valid_color_and_light_plan() -> dict:
    plan = valid_color_plan()
    light_plan = valid_light_plan()["render_contract"]
    plan_contract = plan["render_contract"]
    plan_contract["invariants"].append(deepcopy(light_plan["invariants"][-1]))
    plan_contract["candidate_claims"].append(
        deepcopy(light_plan["candidate_claims"][-1])
    )
    plan_contract["light_form_contract"] = deepcopy(
        light_plan["light_form_contract"]
    )
    for control in plan_contract["color_tone_contract"]["emitted_controls"]:
        control["protected_light_effect_ids"] = [
            "dominant-local-form-contrast"
        ]
    return plan


def with_displayed_key_response(plan: dict) -> dict:
    contract = plan["render_contract"]
    contract["candidate_claims"].append(
        {
            "id": "claim-displayed-key",
            "semantic_slot": "displayed-key-level",
            "owner": "detail.color-tone-fidelity",
            "role": "supporting",
            "polarity": "affirmative",
            "target_strength": "moderate",
            "source_kind": "translated-causal-control",
            "source_evidence": ["major relevant tones sit high without clipping"],
            "emit": True,
            "perceptual_effects": [
                {
                    "aggregate_effect_id": "central-displayed-key",
                    "causal_layer": "exposure",
                    "confidence": "high",
                    "source_evidence": ["midtone and high-side evidence move together"],
                }
            ],
        }
    )
    color_contract = contract["color_tone_contract"]
    color_contract["displayed_tone_response"] = [
        {
            "region_id": "central-form",
            "axis": "displayed-key-level",
            "class": "high",
            "role": "supporting",
            "confidence": "high",
            "emission": "required",
            "aggregate_effect_id": "central-displayed-key",
            "source_evidence": ["broad high-side tones remain below clipping"],
            "tone_scope": {
                "kind": "region",
                "affected_region_ids": ["central-form"],
                "protected_region_ids": ["surrounding-field"],
                "prompt_anchor": "central form",
                "source_evidence": ["only the central form carries the high displayed key"],
            },
        }
    ]
    color_contract["claim_ids"].append("claim-displayed-key")
    color_contract["aggregate_effects"].append(
        {
            "id": "central-displayed-key",
            "region_id": "central-form",
            "axis": "displayed-key-level",
            "direction": "high-displayed-key-with-detail",
            "role": "supporting",
            "target_strength": "moderate",
            "claim_ids": ["claim-displayed-key"],
            "source_supported": True,
            "source_evidence": ["major relevant tones sit high without clipping"],
        }
    )
    color_contract["emitted_controls"].append(
        {
            "id": "control-displayed-key",
            "prompt_excerpt": "on the central form, a high displayed key while preserving highlight detail",
            "claim_id": "claim-displayed-key",
            "causal_layer": "exposure",
            "control_role": "axis-control",
            "region_id": "central-form",
            "axis": "displayed-key-level",
            "aggregate_effect_ids": ["central-displayed-key"],
            **(
                {
                    "protected_light_effect_ids": [
                        "dominant-local-form-contrast"
                    ]
                }
                if "light_form_contract" in contract
                else {}
            ),
        }
    )
    return plan


def add_surface_language_review(
    plan: dict,
    *,
    conflicting: bool = False,
    source_kind: str = "user-supplied",
) -> dict:
    review = {
        "phrase": "analyst candidate label",
        "candidate_source": {
            "kind": source_kind,
            "reference": "held-out test input",
        },
        "label_scope": "composite-appearance",
        "axis_requirements": {
            "value_depth": ["light"],
            "chroma": ["low"],
            "undertone": ["olive"],
            "finish": ["satin"],
        },
        "matched_axes": ["value_depth", "chroma", "undertone", "finish"],
        "conflicting_axes": [],
        "unresolved_axes": [],
        "review_status": "compatible",
    }
    if conflicting:
        review["axis_requirements"]["undertone"] = ["rosy"]
        review["matched_axes"] = ["value_depth", "chroma", "finish"]
        review["conflicting_axes"] = ["undertone"]
        review["review_status"] = "conflicting"
    color_contract = plan["render_contract"]["color_tone_contract"]
    color_contract["surface_color_language"] = {
        "policy_id": "source-visible-surface-language-v1",
        "policy_status": "uncalibrated-language-prototype",
        "observation_scope": "source-visible",
        "profile_status": "missing-profile-assumed-srgb",
        "region_id": "central-form",
        "source_evidence": ["analyst-selected comparable flat patches"],
        "axis_classification": {
            "value_depth": {"term": "light", "confidence": "high"},
            "chroma": {"term": "low", "confidence": "high"},
            "undertone": {"term": "olive", "confidence": "high"},
            "finish": {"term": "satin", "confidence": "medium"},
            "evenness": {"term": "uncertain", "confidence": "low"},
        },
        "friendly_label_review": [review],
    }
    return plan


def add_controlled_surface_descriptor(plan: dict) -> dict:
    """Add a held-out axis-composed surface phrase with complete control ownership."""

    contract = plan["render_contract"]
    color_contract = contract["color_tone_contract"]
    color_contract["emitted_controls"][0]["prompt_excerpt"] = "a light value"
    for axis_spec in color_contract["regions"][0]["intrinsic_axes"]:
        if axis_spec["axis"] == "chroma":
            axis_spec.update(
                {
                    "emission": "required",
                    "aggregate_effect_id": "central-chroma",
                }
            )
            axis_spec.pop("non_emission_reason", None)
        elif axis_spec["axis"] == "hue":
            axis_spec.update(
                {
                    "emission": "required",
                    "aggregate_effect_id": "central-hue",
                }
            )
            axis_spec.pop("non_emission_reason", None)

    for axis, effect_id, claim_id, direction, excerpt in (
        ("chroma", "central-chroma", "claim-surface-chroma", "low-chroma", "low chroma"),
        ("hue", "central-hue", "claim-surface-hue", "olive-undertone", "an olive undertone"),
    ):
        contract["candidate_claims"].append(
            {
                "id": claim_id,
                "semantic_slot": f"surface-{axis}",
                "owner": "detail.color-tone-fidelity",
                "role": "supporting",
                "polarity": "affirmative",
                "target_strength": "subtle",
                "source_kind": "translated-causal-control",
                "source_evidence": [f"held-out source-visible {axis}"],
                "emit": True,
                "perceptual_effects": [
                    {
                        "aggregate_effect_id": effect_id,
                        "causal_layer": "intrinsic",
                        "confidence": "high",
                        "source_evidence": [f"held-out flat-region {axis} evidence"],
                    }
                ],
            }
        )
        color_contract["claim_ids"].append(claim_id)
        color_contract["aggregate_effects"].append(
            {
                "id": effect_id,
                "region_id": "central-form",
                "axis": axis,
                "direction": direction,
                "role": "supporting",
                "target_strength": "subtle",
                "claim_ids": [claim_id],
                "source_supported": True,
                "source_evidence": [f"held-out flat-region {axis} evidence"],
            }
        )
        color_contract["emitted_controls"].append(
            {
                "id": f"control-surface-{axis}",
                "prompt_excerpt": excerpt,
                "claim_id": claim_id,
                "causal_layer": "intrinsic",
                "control_role": "axis-control",
                "region_id": "central-form",
                "axis": axis,
                "aggregate_effect_ids": [effect_id],
            }
        )

    add_generic_claim(
        contract,
        invariant_id="visible-surface-finish",
        axis="surface",
        owner="subject.human",
        role="supporting",
        target_strength="subtle",
        observation="a source-visible satin finish",
        causal_origin="intrinsic",
        evidence="held-out broad soft reflection",
        direction="satin-surface-finish",
        prompt_excerpt="a satin finish",
        region_ids=["central-form"],
    )
    color_contract["surface_color_language"] = {
        "policy_id": "source-visible-surface-language-v1",
        "policy_status": "uncalibrated-language-prototype",
        "observation_scope": "source-visible",
        "profile_status": "missing-profile-assumed-srgb",
        "region_id": "central-form",
        "source_evidence": ["analyst-selected comparable flat patches"],
        "axis_classification": {
            "value_depth": {"term": "light", "confidence": "high"},
            "chroma": {"term": "low", "confidence": "high"},
            "undertone": {"term": "olive", "confidence": "high"},
            "finish": {"term": "satin", "confidence": "medium"},
            "evenness": {"term": "uncertain", "confidence": "low"},
        },
        "controlled_descriptor": {
            "status": "complete",
            "surface_term": "visible skin",
            "phrase": "visible skin with a light value, low chroma, an olive undertone, and a satin finish",
            "requested_axes": ["value_depth", "chroma", "undertone", "finish"],
            "included_axes": ["value_depth", "chroma", "undertone", "finish"],
            "axis_excerpts": {
                "value_depth": "a light value",
                "chroma": "low chroma",
                "undertone": "an olive undertone",
                "finish": "a satin finish",
            },
            "unresolved_axes": [],
            "bounded_axes": {},
            "composition_source": "axis-composed",
            "emit": True,
            "axis_control_ids": {
                "value_depth": "control-surface-tone",
                "chroma": "control-surface-chroma",
                "undertone": "control-surface-hue",
                "finish": "control-visible-surface-finish",
            },
            "source_evidence": ["current-source axis classification"],
        },
        "friendly_label_review": [],
    }
    return plan


def with_material_skin_descriptor(plan: dict) -> dict:
    """Route a human and mark the held-out skin surface descriptor as material."""

    plan = with_spatial_coverage(add_controlled_surface_descriptor(plan))
    decision = plan["render_contract"]["human_appearance_decisions"][0]
    decision.update(
        {
            "face_visibility": "indistinct",
            "fidelity_salience": "primary",
            "appearance_invariant_ids": ["surface-tone"],
        }
    )
    skin = decision["skin_surface"]
    skin.update(
        {
            "disposition": "material",
            "viewer_priority": "P0",
            "confidence": "high",
            "source_evidence": ["held-out visible skin occupies a material region"],
            "region_ids": ["central-form"],
            "coverage": "exposed",
            "descriptor_disposition": "emit",
        }
    )
    skin.pop("non_emission_reason", None)
    skin.pop("descriptor_non_emission_reason", None)
    return plan


def add_lighting_language_review(
    plan: dict,
    *,
    conflicting: bool = False,
    source_kind: str = "user-supplied",
) -> dict:
    review = {
        "phrase": "held-out candidate lighting label",
        "candidate_source": {
            "kind": source_kind,
            "reference": "held-out test input",
        },
        "label_scope": "composite-lighting",
        "axis_requirements": {
            "displayed_key_level": ["high"],
            "edge_softness": ["soft"],
            "local_form_contrast": ["subtle"],
        },
        "matched_axes": [
            "displayed_key_level",
            "edge_softness",
            "local_form_contrast",
        ],
        "conflicting_axes": [],
        "unresolved_axes": [],
        "review_status": "compatible",
    }
    if conflicting:
        review["axis_requirements"]["displayed_key_level"] = ["low"]
        review["matched_axes"] = ["edge_softness", "local_form_contrast"]
        review["conflicting_axes"] = ["displayed_key_level"]
        review["review_status"] = "conflicting"
    light_contract = plan["render_contract"]["light_form_contract"]

    def axis(term: str, confidence: str = "high") -> dict:
        return {
            "term": term,
            "confidence": confidence,
            "source_evidence": (
                [] if term in {"mixed", "uncertain"} else ["held-out visible evidence"]
            ),
        }

    light_contract["lighting_language"] = {
        "policy_id": "source-visible-lighting-language-v1",
        "policy_status": "uncalibrated-language-prototype",
        "observation_scope": "source-visible",
        "region_id": "central-form",
        "source_evidence": ["analyst-separated broad and local lighting evidence"],
        "axis_classification": {
            "displayed_key_level": axis("high"),
            "shadow_floor": axis("deep", "medium"),
            "edge_softness": axis("soft"),
            "local_form_contrast": axis("subtle"),
            "bright_plane_coverage": axis("broad"),
            "gradient_extent": axis("long"),
            "directionality": axis("uncertain", "low"),
            "fill_structure": axis("uncertain", "low"),
        },
        "controlled_summary": {
            "phrase": "high-key soft-edged gently-modeling light",
            "status": "explanation-only",
            "emit": False,
            "decomposed_axes": [
                "displayed_key_level",
                "edge_softness",
                "local_form_contrast",
            ],
            "unresolved_axes": [],
        },
        "friendly_label_review": [review],
    }
    light_contract["lighting_labels"] = [
        {
            "phrase": "held-out candidate lighting label",
            "status": "explanation-only",
            "emit": False,
            "decomposed_control_ids": ["control-light-shape"],
        }
    ]
    return plan


class SaliencePlanTests(unittest.TestCase):
    def test_valid_source_relative_plan_passes(self) -> None:
        self.assertEqual(audit_plan(valid_plan()), [])

    def test_authored_prompt_must_compile_internal_provenance_into_visible_state(self) -> None:
        phrases = (
            "a poised, source-relative high-glamour presentation",
            "source-visible shoulder geometry",
            "source-specific garment coverage",
            "source-supported shadow topology",
            "the current-source lighting reading",
        )
        for phrase in phrases:
            with self.subTest(phrase=phrase):
                errors = audit_standalone_prompt_text(f"PROMPT:\n{phrase}.")
                self.assertTrue(
                    any("internal provenance label" in error for error in errors)
                )

    def test_plan_ledger_cannot_normalize_non_standalone_prompt_text(self) -> None:
        plan = valid_plan()
        plan["render_contract"]["emitted_controls"][2]["prompt_excerpt"] = (
            "a small source-relative offset from the frame center"
        )
        errors = audit_plan(plan, authored_prompt_text(plan))
        self.assertTrue(
            any("authored prompt is not standalone" in error for error in errors)
        )

    def test_authored_prompt_rejects_unavailable_artifact_instructions(self) -> None:
        prompts = (
            "PROMPT:\nMatch the reference while keeping the same crop.",
            "PROMPT:\nPreserve the original pose and lighting.",
            "PROMPT:\nUse the attached image as shown in the reference image.",
            "PROMPT:\nThe head turns toward source side A.",
        )
        for prompt in prompts:
            with self.subTest(prompt=prompt):
                self.assertTrue(audit_standalone_prompt_text(prompt))

    def test_authored_prompt_allows_physical_sources_and_self_contained_state_verbs(self) -> None:
        prompt = (
            "PROMPT:\nA large soft light source above viewer-left creates broad "
            "highlight coverage. Keep the head turned three-quarters toward "
            "viewer-right, preserve the diagonal shoulder line, let the lower "
            "half remain outside the frame, and keep the text small and indistinct."
        )
        self.assertEqual(audit_standalone_prompt_text(prompt), [])
        self.assertEqual(audit_plan(valid_plan(), authored_prompt_text(valid_plan())), [])

    def test_generic_emitted_claim_requires_effect_and_final_control(self) -> None:
        plan = valid_plan()
        contract = plan["render_contract"]
        del contract["candidate_claims"][0]["salience_effects"]
        del contract["emitted_controls"][0]
        errors = audit_plan(plan)
        self.assertTrue(any("salience_effects" in error for error in errors))
        self.assertTrue(
            any("exactly one emitted final-prompt control" in error for error in errors)
        )

    def test_one_generic_effect_cannot_have_two_emitted_claims(self) -> None:
        plan = valid_plan()
        contract = plan["render_contract"]
        duplicate = deepcopy(contract["candidate_claims"][0])
        duplicate["id"] = "claim-form-support"
        duplicate["semantic_slot"] = "silhouette-support"
        duplicate["role"] = "supporting"
        contract["candidate_claims"].append(duplicate)
        contract["aggregate_effects"][0]["claim_ids"].append(duplicate["id"])
        contract["emitted_controls"].append(
            {
                "id": "control-form-support",
                "prompt_excerpt": "the same compact silhouette repeated as support",
                "claim_id": duplicate["id"],
                "owner": duplicate["owner"],
                "aggregate_effect_ids": ["compact-silhouette-effect"],
            }
        )
        self.assertTrue(
            any(
                "generic aggregate effect" in error
                and "multiple emitted claims" in error
                for error in audit_plan(plan)
            )
        )

    def test_same_generic_direction_cannot_hide_behind_two_effect_ids(self) -> None:
        plan = valid_plan()
        contract = plan["render_contract"]
        duplicate_claim = deepcopy(contract["candidate_claims"][0])
        duplicate_claim["id"] = "claim-form-split"
        duplicate_claim["semantic_slot"] = "silhouette-support"
        duplicate_claim["role"] = "supporting"
        duplicate_claim["salience_effects"][0]["aggregate_effect_id"] = (
            "compact-silhouette-effect-split"
        )
        contract["candidate_claims"].append(duplicate_claim)
        duplicate_effect = deepcopy(contract["aggregate_effects"][0])
        duplicate_effect["id"] = "compact-silhouette-effect-split"
        duplicate_effect["role"] = "supporting"
        duplicate_effect["claim_ids"] = [duplicate_claim["id"]]
        contract["aggregate_effects"].append(duplicate_effect)
        contract["emitted_controls"].append(
            {
                "id": "control-form-split",
                "prompt_excerpt": "a second phrase pushing the same compact form",
                "claim_id": duplicate_claim["id"],
                "owner": duplicate_claim["owner"],
                "aggregate_effect_ids": [duplicate_effect["id"]],
            }
        )
        self.assertTrue(
            any(
                "split one axis/direction/region/relation" in error
                for error in audit_plan(plan)
            )
        )

    def test_spatial_invariant_requires_linked_component_relation(self) -> None:
        plan = valid_plan()
        plan["render_contract"]["aggregate_effects"][1]["relation_ids"] = []
        self.assertTrue(
            any(
                "spatial-relation invariant" in error
                for error in audit_plan(plan)
            )
        )

    def test_flexible_center_and_opposite_offsets_remain_valid_nonhuman_variants(self) -> None:
        baseline = valid_plan()
        relation = baseline["render_contract"]["component_relations"][1]
        effect = baseline["render_contract"]["aggregate_effects"][2]
        control = baseline["render_contract"]["emitted_controls"][2]
        relation["observation"] = "the source axis coincides with the frame centerline"
        effect["direction"] = "source-axis-on-frame-centerline"
        control["prompt_excerpt"] = "the principal axis follows the frame centerline"

        for observation, direction, excerpt in (
            (
                "the source axis sits to the viewer-left of the frame centerline",
                "source-axis-offset-viewer-left",
                "the principal axis stays to the viewer-left of the frame centerline",
            ),
            (
                "the source axis sits to the viewer-right of the frame centerline",
                "source-axis-offset-viewer-right",
                "the principal axis stays to the viewer-right of the frame centerline",
            ),
        ):
            variant = deepcopy(baseline)
            variant_relation = variant["render_contract"]["component_relations"][1]
            variant_effect = variant["render_contract"]["aggregate_effects"][2]
            variant_control = variant["render_contract"]["emitted_controls"][2]
            variant_relation["observation"] = observation
            variant_effect["direction"] = direction
            variant_control["prompt_excerpt"] = excerpt
            self.assertEqual(audit_plan(variant), [])
            self.assertEqual(
                compare_plans(baseline, variant, "invariant-preserving"), []
            )

    def test_material_human_orientation_changes_signature_without_a_direction_default(self) -> None:
        baseline = valid_plan()
        contract = baseline["render_contract"]
        add_generic_claim(
            contract,
            invariant_id="head-torso-axis-relation",
            axis="form",
            owner="subject.human",
            role="primary",
            target_strength="moderate",
            observation="the head and torso retain source-visible relative orientation A",
            causal_origin="pose-deformation",
            evidence="visible head turn, shoulder line, and torso axis",
            direction="source-visible-head-torso-relation-a",
            prompt_excerpt="the head turn and shoulder line retain relation A",
            region_ids=["central-form"],
        )
        variant = deepcopy(baseline)
        variant_contract = variant["render_contract"]
        variant_invariant = variant_contract["invariants"][-1]
        variant_effect = variant_contract["aggregate_effects"][-1]
        variant_control = variant_contract["emitted_controls"][-1]
        variant_invariant["observation"] = (
            "the head and torso retain source-visible relative orientation B"
        )
        variant_effect["direction"] = "source-visible-head-torso-relation-b"
        variant_control["prompt_excerpt"] = (
            "the head turn and shoulder line retain relation B"
        )
        self.assertEqual(audit_plan(baseline), [])
        self.assertEqual(audit_plan(variant), [])
        self.assertTrue(
            any(
                "changed the primary salience signature" in error
                for error in compare_plans(
                    baseline, variant, "invariant-preserving"
                )
            )
        )

    def test_routed_human_needs_coverage_beyond_a_frame_zone_relation(self) -> None:
        plan = valid_plan()
        plan["routing"] = {"resolved_non_core_modules": ["subject.human"]}
        self.assertTrue(
            any(
                "frame-zone relation alone" in error
                for error in audit_plan(plan)
            )
        )

    def test_spatial_coverage_requires_the_current_evidence_schema(self) -> None:
        plan = with_spatial_coverage(valid_plan())
        del plan["render_contract"]["spatial_orientation_coverage"][
            "schema_version"
        ]
        self.assertTrue(
            any(
                "schema_version" in error and "spatial-orientation/v5" in error
                for error in audit_plan(plan)
            )
        )

    def test_legacy_coarse_human_pose_dimension_cannot_satisfy_v5(self) -> None:
        plan = with_spatial_coverage(valid_plan())
        decision = next(
            item
            for item in plan["render_contract"]["spatial_orientation_coverage"][
                "decisions"
            ]
            if item["dimension"] == "human-head-body-yaw"
        )
        decision["dimension"] = "human-head-body-relation"
        self.assertTrue(
            any(
                "legacy coarse human pose dimension" in error
                for error in audit_plan(plan)
            )
        )

    def test_spatial_evidence_cue_records_confounders_explicitly(self) -> None:
        plan = with_spatial_coverage(valid_plan())
        cue = plan["render_contract"]["spatial_orientation_coverage"][
            "evidence_cues"
        ][0]
        del cue["confounders"]
        self.assertTrue(
            any("confounders must be a list" in error for error in audit_plan(plan))
        )

    def test_pose_decision_needs_owned_structured_evidence_cues(self) -> None:
        plan = with_spatial_coverage(valid_plan())
        coverage = plan["render_contract"]["spatial_orientation_coverage"]
        decision = next(
            item
            for item in coverage["decisions"]
            if item["dimension"] == "human-head-body-yaw"
        )
        decision["evidence_cue_ids"] = ["cue-frame-placement"]
        self.assertTrue(
            any(
                "orientation decision cannot rely only on frame-placement cues"
                in error
                for error in audit_plan(plan)
            )
        )

        unknown = with_spatial_coverage(valid_plan())
        decision = next(
            item
            for item in unknown["render_contract"]["spatial_orientation_coverage"][
                "decisions"
            ]
            if item["dimension"] == "human-head-body-yaw"
        )
        decision["evidence_cue_ids"] = ["missing-cue"]
        self.assertTrue(
            any(
                "references unknown evidence cues" in error
                for error in audit_plan(unknown)
            )
        )

    def test_nonmaterial_pose_needs_dimension_neutralization_test(self) -> None:
        plan = with_spatial_coverage(valid_plan())
        decision = next(
            item
            for item in plan["render_contract"]["spatial_orientation_coverage"][
                "decisions"
            ]
            if item["dimension"] == "human-torso-yaw"
        )
        del decision["neutralization_test"]
        self.assertTrue(
            any(
                "neutralization_test must be an object" in error
                for error in audit_plan(plan)
            )
        )

    def test_nonmaterial_pose_cannot_hide_material_drift_in_free_prose(self) -> None:
        plan = with_spatial_coverage(valid_plan())
        decision = next(
            item
            for item in plan["render_contract"]["spatial_orientation_coverage"][
                "decisions"
            ]
            if item["dimension"] == "human-torso-yaw"
        )
        decision["non_emission_reason"] = "minor variation is acceptable"
        decision["neutralization_test"].update(
            {
                "verdict": "material-drift",
                "preserved_relations": [],
                "changed_relations": [
                    "neutralizing torso yaw changes the visible side-depth relation"
                ],
            }
        )
        self.assertTrue(
            any(
                "must be 'preserved'" in error
                for error in audit_plan(plan)
            )
        )

    def test_low_confidence_pose_cannot_be_discarded_without_coupled_owner(self) -> None:
        plan = with_spatial_coverage(valid_plan())
        decision = next(
            item
            for item in plan["render_contract"]["spatial_orientation_coverage"][
                "decisions"
            ]
            if item["dimension"] == "human-torso-yaw"
        )
        decision["confidence"] = "low"
        self.assertTrue(
            any(
                "cannot be discarded from low-confidence" in error
                for error in audit_plan(plan)
            )
        )

    def test_fully_confounded_pose_cannot_be_discarded_without_coupled_owner(self) -> None:
        plan = with_spatial_coverage(valid_plan())
        coverage = plan["render_contract"]["spatial_orientation_coverage"]
        decision = next(
            item
            for item in coverage["decisions"]
            if item["dimension"] == "human-shoulder-depth-order"
        )
        for cue in coverage["evidence_cues"]:
            if cue["id"] in decision["evidence_cue_ids"]:
                cue["confounders"] = ["garment and perspective cues cannot be separated"]
        self.assertTrue(
            any(
                "cannot be discarded from low-confidence or fully confounded evidence"
                in error
                for error in audit_plan(plan)
            )
        )

    def test_confounded_weak_pose_can_survive_through_one_coupled_owner(self) -> None:
        plan = with_spatial_coverage(valid_plan())
        coverage = plan["render_contract"]["spatial_orientation_coverage"]
        member_dimensions = {
            "human-torso-yaw",
            "human-head-body-yaw",
            "human-shoulder-depth-order",
        }
        for decision in coverage["decisions"]:
            if decision["dimension"] not in member_dimensions:
                continue
            decision["confidence"] = "low"
            cue = next(
                cue
                for cue in coverage["evidence_cues"]
                if cue["id"] in decision["evidence_cue_ids"]
            )
            cue["confounders"] = ["the individual axis is weak in isolation"]
        promote_coupled_orientation(plan)
        self.assertEqual(audit_plan(plan), [])

    def test_uncertain_pose_needs_a_visibility_or_confound_limit(self) -> None:
        plan = with_spatial_coverage(valid_plan())
        decision = next(
            item
            for item in plan["render_contract"]["spatial_orientation_coverage"][
                "decisions"
            ]
            if item["dimension"] == "human-shoulder-depth-order"
        )
        decision["disposition"] = "uncertain"
        decision["non_emission_reason"] = "the visible evidence conflicts"
        self.assertTrue(
            any("visibility_limit" in error for error in audit_plan(plan))
        )

    def test_material_residual_counterfactual_requires_an_orientation_effect(self) -> None:
        plan = with_spatial_coverage(valid_plan())
        check = next(
            item
            for item in plan["render_contract"]["spatial_orientation_coverage"][
                "counterfactual_checks"
            ]
            if item["scope"] == "residual-alignment"
        )
        check.update(
            {
                "verdict": "material",
                "changed_relations": [
                    "neutral alignment changes a held-out part-axis relation"
                ],
                "preserved_relations": [],
            }
        )
        self.assertTrue(
            any(
                "material residual-alignment counterfactual" in error
                for error in audit_plan(plan)
            )
        )

        promote_spatial_decision(
            plan,
            "human-head-body-yaw",
            direction="source-visible head-to-body yaw relation",
        )
        self.assertEqual(audit_plan(plan), [])

    def test_human_orientation_requires_whole_and_residual_counterfactuals(self) -> None:
        plan = with_spatial_coverage(valid_plan())
        checks = plan["render_contract"]["spatial_orientation_coverage"][
            "counterfactual_checks"
        ]
        checks[:] = [item for item in checks if item["scope"] != "residual-alignment"]
        self.assertTrue(
            any(
                "requires counterfactual scopes" in error
                and "residual-alignment" in error
                for error in audit_plan(plan)
            )
        )

    def test_residual_counterfactual_holds_viewpoint_fixed(self) -> None:
        plan = with_spatial_coverage(valid_plan())
        residual = next(
            item
            for item in plan["render_contract"]["spatial_orientation_coverage"][
                "counterfactual_checks"
            ]
            if item["scope"] == "residual-alignment"
        )
        residual["held_fixed_decision_ids"].remove("coverage-viewpoint-elevation")
        self.assertTrue(
            any(
                "must hold every viewpoint decision fixed" in error
                for error in audit_plan(plan)
            )
        )

    def test_individually_weak_pose_cues_can_emit_one_coupled_effect(self) -> None:
        plan = promote_coupled_orientation(with_spatial_coverage(valid_plan()))
        self.assertEqual(audit_plan(plan), [])

        duplicated = deepcopy(plan)
        promote_spatial_decision(duplicated, "human-torso-yaw")
        self.assertTrue(
            any(
                "must merge individually non-emitted decisions" in error
                for error in audit_plan(duplicated)
            )
        )

        lost_direction = deepcopy(plan)
        lost_direction["render_contract"]["spatial_orientation_coverage"][
            "coupled_effects"
        ][0]["result_direction"] = "a different integrated direction"
        self.assertTrue(
            any(
                "result_direction must match its aggregate effect" in error
                for error in audit_plan(lost_direction)
            )
        )

    def test_coupled_pose_prompt_order_and_net_effect_are_enforced(self) -> None:
        plan = promote_coupled_orientation(with_spatial_coverage(valid_plan()))
        contract = plan["render_contract"]
        controls = {item["id"]: item for item in contract["emitted_controls"]}
        ordered_ids = [
            "control-coupled-orientation",
            "control-form",
            "control-balance",
            "control-placement",
        ]
        prompt = "PROMPT:\n" + ". ".join(
            controls[control_id]["prompt_excerpt"] for control_id in ordered_ids
        )
        self.assertEqual(audit_plan(plan, prompt_text=prompt), [])

        wrong_order = authored_prompt_text(plan)
        self.assertTrue(
            any(
                "must appear before control 'control-form'" in error
                for error in audit_plan(plan, prompt_text=wrong_order)
            )
        )

        incomplete_net = deepcopy(plan)
        incomplete_net["render_contract"]["spatial_orientation_coverage"][
            "coupled_effects"
        ][0]["net_effect_audit"]["included_control_ids"] = []
        self.assertTrue(
            any(
                "included_control_ids must be non-empty" in error
                for error in audit_plan(incomplete_net)
            )
        )

    def test_lossy_coupled_summary_requires_every_at_risk_residual(self) -> None:
        plan = promote_coupled_orientation(with_spatial_coverage(valid_plan()))
        coupled = plan["render_contract"]["spatial_orientation_coverage"][
            "coupled_effects"
        ][0]
        actuation = coupled["prompt_decomposition"]["member_actuations"][0]
        del actuation["prompt_excerpt"]
        self.assertTrue(
            any(
                "prompt_excerpt is required" in error
                and "summary coverage" in error
                for error in audit_plan(plan)
            )
        )

    def test_coupled_summary_cannot_hide_residuals_outside_its_control(self) -> None:
        plan = promote_coupled_orientation(with_spatial_coverage(valid_plan()))
        contract = plan["render_contract"]
        coupled = contract["spatial_orientation_coverage"]["coupled_effects"][0]
        control = next(
            item
            for item in contract["emitted_controls"]
            if item["id"] == coupled["control_id"]
        )
        control["prompt_excerpt"] = coupled["prompt_decomposition"]["summary_anchor"][
            "prompt_excerpt"
        ]
        self.assertTrue(
            any(
                "must be contained in its coupled control" in error
                for error in audit_plan(plan)
            )
        )

    def test_coupled_summary_precedes_its_residual_actuations(self) -> None:
        plan = promote_coupled_orientation(with_spatial_coverage(valid_plan()))
        contract = plan["render_contract"]
        coupled = contract["spatial_orientation_coverage"]["coupled_effects"][0]
        decomposition = coupled["prompt_decomposition"]
        summary_excerpt = decomposition["summary_anchor"]["prompt_excerpt"]
        residual_excerpts = [
            item["prompt_excerpt"]
            for item in decomposition["member_actuations"]
            if "prompt_excerpt" in item
        ]
        control = next(
            item
            for item in contract["emitted_controls"]
            if item["id"] == coupled["control_id"]
        )
        control["prompt_excerpt"] = ". ".join([*residual_excerpts, summary_excerpt])
        self.assertTrue(
            any(
                "summary anchor must appear before residual actuation" in error
                for error in audit_plan(plan)
            )
        )

    def test_sufficient_coupled_summary_does_not_force_residual_details(self) -> None:
        plan = promote_coupled_orientation(
            with_spatial_coverage(valid_plan()),
            summary_adequacy="sufficient",
            residual_dimensions=(),
        )
        self.assertEqual(audit_plan(plan), [])
        coupled = plan["render_contract"]["spatial_orientation_coverage"][
            "coupled_effects"
        ][0]
        self.assertTrue(
            all(
                item["summary_coverage"] == "complete"
                and "prompt_excerpt" not in item
                for item in coupled["prompt_decomposition"]["member_actuations"]
            )
        )

    def test_lossy_coupled_summary_emits_only_at_risk_member_residuals(self) -> None:
        plan = promote_coupled_orientation(
            with_spatial_coverage(valid_plan()),
            residual_dimensions=("human-head-body-yaw",),
        )
        self.assertEqual(audit_plan(plan), [])
        coupled = plan["render_contract"]["spatial_orientation_coverage"][
            "coupled_effects"
        ][0]
        actuations = coupled["prompt_decomposition"]["member_actuations"]
        self.assertEqual(
            [item["decision_id"] for item in actuations if "prompt_excerpt" in item],
            ["coverage-human-head-body-yaw"],
        )

    def test_uncertain_coupled_summary_retains_supported_partial_residual(self) -> None:
        plan = promote_coupled_orientation(
            with_spatial_coverage(valid_plan()),
            summary_adequacy="uncertain",
            residual_dimensions=("human-shoulder-depth-order",),
        )
        coupled = plan["render_contract"]["spatial_orientation_coverage"][
            "coupled_effects"
        ][0]
        residual = next(
            item
            for item in coupled["prompt_decomposition"]["member_actuations"]
            if item["decision_id"] == "coverage-human-shoulder-depth-order"
        )
        residual["summary_coverage"] = "partial"
        self.assertEqual(audit_plan(plan), [])

    def test_non_human_coupled_summary_uses_the_same_loss_audit(self) -> None:
        plan = promote_coupled_orientation(
            with_spatial_coverage(valid_plan(), kind="non-human"),
            member_dimensions=(
                "subject-principal-axis",
                "cross-component-orientation",
            ),
            residual_dimensions=("cross-component-orientation",),
        )
        self.assertEqual(audit_plan(plan), [])

    def test_coupled_member_actuation_covers_every_member_once(self) -> None:
        plan = promote_coupled_orientation(with_spatial_coverage(valid_plan()))
        coupled = plan["render_contract"]["spatial_orientation_coverage"][
            "coupled_effects"
        ][0]
        coupled["prompt_decomposition"]["member_actuations"].pop()
        self.assertTrue(
            any(
                "must cover every coupled member exactly once" in error
                for error in audit_plan(plan)
            )
        )

    def test_authored_prompt_rejects_duplicate_coupled_residual_excerpt(self) -> None:
        plan = promote_coupled_orientation(with_spatial_coverage(valid_plan()))
        coupled = plan["render_contract"]["spatial_orientation_coverage"][
            "coupled_effects"
        ][0]
        residual_excerpt = next(
            item["prompt_excerpt"]
            for item in coupled["prompt_decomposition"]["member_actuations"]
            if "prompt_excerpt" in item
        )
        prompt = authored_prompt_text(plan) + ". " + residual_excerpt
        self.assertTrue(
            any(
                "residual excerpt appears 2 times" in error
                for error in audit_plan(plan, prompt_text=prompt)
            )
        )

    def test_readable_human_coverage_requires_every_decomposed_pose_dimension(self) -> None:
        plan = with_spatial_coverage(valid_plan())
        decisions = plan["render_contract"]["spatial_orientation_coverage"][
            "decisions"
        ]
        decisions[:] = [
            item
            for item in decisions
            if item["dimension"] != "human-head-body-yaw"
        ]
        self.assertTrue(
            any(
                "missing dispositions" in error
                and "human-head-body-yaw" in error
                for error in audit_plan(plan)
            )
        )

    def test_head_pitch_alone_cannot_cover_yaw_roll_and_lateral_offset(self) -> None:
        plan = with_spatial_coverage(valid_plan())
        decisions = plan["render_contract"]["spatial_orientation_coverage"][
            "decisions"
        ]
        decisions[:] = [
            item
            for item in decisions
            if item["dimension"]
            not in {
                "human-head-body-yaw",
                "human-head-body-roll",
                "human-head-body-lateral-offset",
            }
        ]
        errors = audit_plan(plan)
        self.assertTrue(any("human-head-body-yaw" in error for error in errors))
        self.assertTrue(any("human-head-body-roll" in error for error in errors))
        self.assertTrue(
            any("human-head-body-lateral-offset" in error for error in errors)
        )

    def test_spatial_invariant_needs_relation_effect_claim_and_control_path(self) -> None:
        plan = promote_spatial_decision(
            with_spatial_coverage(valid_plan()),
            "subject-principal-axis",
        )
        self.assertEqual(audit_plan(plan), [])
        decision = next(
            item
            for item in plan["render_contract"]["spatial_orientation_coverage"][
                "decisions"
            ]
            if item["dimension"] == "subject-principal-axis"
        )
        decision.pop("control_id", None)
        self.assertTrue(
            any(
                "complete relation/effect/claim/control path" in error
                for error in audit_plan(plan)
            )
        )

    def test_every_emitted_spatial_control_needs_a_prompt_effect_audit(self) -> None:
        plan = promote_spatial_decision(
            with_spatial_coverage(valid_plan()),
            "subject-principal-axis",
        )
        plan["render_contract"]["spatial_orientation_coverage"][
            "prompt_effect_audits"
        ] = []
        self.assertTrue(
            any(
                "must cover every emitted spatial control" in error
                for error in audit_plan(plan)
            )
        )

    def test_prompt_alignment_clause_cannot_implicitly_actuate_discarded_axis(self) -> None:
        plan = promote_spatial_decision(
            with_spatial_coverage(valid_plan()),
            "frame-placement",
            direction="source-supported frame placement",
            prompt_excerpt="place the subject slightly left of frame center",
        )
        audit = plan["render_contract"]["spatial_orientation_coverage"][
            "prompt_effect_audits"
        ][0]
        audit["implicit_decision_ids"] = ["coverage-human-torso-yaw"]
        self.assertTrue(
            any(
                "would actuate non-invariant or uncertain spatial decisions" in error
                and "coverage-human-torso-yaw" in error
                for error in audit_plan(plan)
            )
        )

    def test_prompt_effect_audit_must_match_the_exact_spatial_clause(self) -> None:
        plan = promote_spatial_decision(
            with_spatial_coverage(valid_plan()),
            "human-head-body-yaw",
        )
        audit = plan["render_contract"]["spatial_orientation_coverage"][
            "prompt_effect_audits"
        ][0]
        audit["prompt_excerpt"] = "a softened paraphrase"
        self.assertTrue(
            any(
                "prompt_excerpt must exactly match" in error
                for error in audit_plan(plan)
            )
        )

    def test_flexible_and_not_visible_spatial_dimensions_cannot_emit(self) -> None:
        plan = with_spatial_coverage(valid_plan(), visibility="indistinct")
        contract = plan["render_contract"]
        head = next(
            item
            for item in contract["spatial_orientation_coverage"]["decisions"]
            if item["dimension"] == "human-head-body-yaw"
        )
        head["disposition"] = "not-visible"
        head["observation"] = "the head-to-body relation is not separable at this scale"
        head["non_emission_reason"] = "the relevant parts are indistinct"
        head["visibility_limit"] = "the head and torso axes are not separately readable"
        principal = next(
            item
            for item in contract["spatial_orientation_coverage"]["decisions"]
            if item["dimension"] == "subject-principal-axis"
        )
        principal["disposition"] = "flexible"
        principal["non_emission_reason"] = "axis variation preserves the proposition"
        contract["flexible_dimensions"].append(principal["id"])
        self.assertEqual(audit_plan(plan), [])

        promoted = promote_spatial_decision(
            deepcopy(plan), "human-head-body-yaw"
        )
        promoted_head = next(
            item
            for item in promoted["render_contract"]["spatial_orientation_coverage"][
                "decisions"
            ]
            if item["dimension"] == "human-head-body-yaw"
        )
        promoted_head["disposition"] = "not-visible"
        promoted_head["non_emission_reason"] = "the relevant parts are indistinct"
        self.assertTrue(
            any(
                "cannot carry emitted-path fields" in error
                for error in audit_plan(promoted)
            )
        )

    def test_camera_elevation_and_head_body_pitch_need_distinct_causal_axes(self) -> None:
        plan = with_spatial_coverage(valid_plan())
        promote_spatial_decision(
            plan,
            "viewpoint-elevation",
            direction="source-relative camera elevation",
        )
        promote_spatial_decision(
            plan,
            "human-head-body-pitch",
            direction="source-relative head pitch against the torso",
        )
        self.assertEqual(audit_plan(plan), [])

        duplicate = deepcopy(plan)
        contract = duplicate["render_contract"]
        decisions = contract["spatial_orientation_coverage"]["decisions"]
        camera = next(
            item for item in decisions if item["dimension"] == "viewpoint-elevation"
        )
        head = next(
            item
            for item in decisions
            if item["dimension"] == "human-head-body-pitch"
        )
        head["control_axis_id"] = camera["control_axis_id"]
        next(
            item
            for item in contract["aggregate_effects"]
            if item["id"] == head["aggregate_effect_id"]
        )["control_axis_id"] = camera["control_axis_id"]
        next(
            item
            for item in contract["emitted_controls"]
            if item["id"] == head["control_id"]
        )["control_axis_id"] = camera["control_axis_id"]
        self.assertTrue(
            any(
                "shared control_axis_id" in error
                or "duplicate one spatial control_axis_id" in error
                for error in audit_plan(duplicate)
            )
        )

    def test_centered_opposite_and_mirrored_axes_are_all_valid_values(self) -> None:
        for direction in (
            "the principal axis coincides with the frame vertical centerline",
            "the principal axis remains offset toward viewer-left",
            "the principal axis remains offset toward viewer-right",
        ):
            plan = promote_spatial_decision(
                with_spatial_coverage(valid_plan()),
                "subject-principal-axis",
                direction=direction,
                prompt_excerpt=direction,
            )
            self.assertEqual(audit_plan(plan), [])

    def test_mirrored_head_body_yaw_relations_are_equally_valid(self) -> None:
        for direction, verdict in (
            ("the head turns toward viewer-left relative to the torso", "material"),
            ("the head turns toward viewer-right relative to the torso", "material"),
            ("the head and torso remain frontally aligned", "not-material"),
        ):
            plan = with_spatial_coverage(valid_plan())
            check = next(
                item
                for item in plan["render_contract"]["spatial_orientation_coverage"][
                    "counterfactual_checks"
                ]
                if item["scope"] == "residual-alignment"
            )
            if verdict == "material":
                check.update(
                    {
                        "verdict": verdict,
                        "changed_relations": [
                            "neutral replacement changes the source head-to-body relation"
                        ],
                        "preserved_relations": [],
                    }
                )
            promote_spatial_decision(
                plan,
                "human-head-body-yaw",
                direction=direction,
                prompt_excerpt=direction,
            )
            self.assertEqual(audit_plan(plan), [])

    def test_nonhuman_principal_axis_uses_the_same_coverage_contract(self) -> None:
        plan = promote_spatial_decision(
            with_spatial_coverage(valid_plan(), kind="non-human"),
            "subject-principal-axis",
            direction="source-visible diagonal product axis",
        )
        self.assertEqual(audit_plan(plan), [])

    def test_routed_human_cannot_silently_skip_appearance_decisions(self) -> None:
        plan = with_spatial_coverage(valid_plan())
        del plan["render_contract"]["human_appearance_decisions"]
        self.assertTrue(
            any(
                "appearance gestalt, and skin handling cannot be silently omitted"
                in error
                for error in audit_plan(plan)
            )
        )

        malformed = with_spatial_coverage(valid_plan())
        malformed["render_contract"]["human_appearance_decisions"][0][
            "subject_id"
        ] = []
        self.assertTrue(
            any(
                "subject_id must reference a human coverage subject" in error
                for error in audit_plan(malformed)
            )
        )

    def test_person_prior_emit_requires_one_linked_generation_prior(self) -> None:
        plan = with_spatial_coverage(valid_plan())
        contract = plan["render_contract"]
        add_generic_claim(
            contract,
            invariant_id="broad-person-gestalt",
            axis="form",
            owner="subject.human",
            role="supporting",
            target_strength="subtle",
            observation="one source-visible non-identifying person gestalt",
            causal_origin="intrinsic",
            evidence="held-out broad face gestalt",
            direction="source-relative-person-gestalt",
            prompt_excerpt="one bounded non-identifying person gestalt",
            region_ids=["central-form"],
        )
        prior_claim = contract["candidate_claims"][-1]
        add_generic_claim(
            contract,
            invariant_id="person-geometry-correction",
            axis="form",
            owner="detail.human-face-likeness",
            role="supporting",
            target_strength="subtle",
            observation="visible geometry constrains the broad person gestalt",
            causal_origin="intrinsic",
            evidence="held-out silhouette and feature relations",
            direction="source-relative-person-geometry",
            prompt_excerpt="visible silhouette and feature relations constrain that gestalt",
            region_ids=["central-form"],
        )
        prior_claim["generation_prior"] = {
            "scope": "person-gestalt",
            "candidate_source": {
                "kind": "source-visible-approximation",
                "reference": "held-out source observation",
            },
            "non_identifying": True,
            "visible_geometry_evidence": ["held-out silhouette and feature relations"],
            "geometry_claim_ids": ["claim-person-geometry-correction"],
        }
        decision = contract["human_appearance_decisions"][0]["person_prior"]
        contract["human_appearance_decisions"][0].update(
            {
                "fidelity_salience": "supporting",
                "appearance_invariant_ids": ["broad-person-gestalt"],
            }
        )
        decision.update(
            {
                "disposition": "emit",
                "confidence": "medium",
                "candidate_support": "supported",
                "default_drift_risk": "high",
                "local_geometry_sufficiency": "sufficient",
                "geometry_claim_ids": ["claim-person-geometry-correction"],
                "source_evidence": ["held-out broad person gestalt is readable"],
                "claim_id": "claim-broad-person-gestalt",
            }
        )
        decision.pop("non_emission_reason", None)
        decision.pop("omission_counterfactual", None)
        self.assertEqual(audit_plan(plan), [])

        unlinked = deepcopy(plan)
        del unlinked["render_contract"]["human_appearance_decisions"][0][
            "person_prior"
        ]["claim_id"]
        self.assertTrue(
            any("person_prior.claim_id" in error for error in audit_plan(unlinked))
        )

        malformed_claim = deepcopy(plan)
        malformed_claim["render_contract"]["human_appearance_decisions"][0][
            "person_prior"
        ]["claim_id"] = []
        self.assertTrue(
            any(
                "person_prior.claim_id must be non-empty" in error
                for error in audit_plan(malformed_claim)
            )
        )

        unreadable = deepcopy(plan)
        unreadable["render_contract"]["human_appearance_decisions"][0][
            "face_visibility"
        ] = "indistinct"
        self.assertTrue(
            any("cannot emit for face visibility" in error for error in audit_plan(unreadable))
        )

    def test_readable_secondary_primary_appearance_cannot_use_weak_omit(self) -> None:
        plan = with_material_human_appearance_omission(valid_plan())
        errors = audit_plan(plan)
        self.assertTrue(any("sufficient emitted local geometry" in error for error in errors))
        self.assertTrue(any("low model-default drift risk" in error for error in errors))
        self.assertTrue(any("preserved omission counterfactual" in error for error in errors))

    def test_material_appearance_omit_passes_only_with_low_risk_geometry_counterfactual(self) -> None:
        plan = with_material_human_appearance_omission(
            valid_plan(),
            drift_risk="low",
            geometry_sufficiency="sufficient",
            counterfactual="preserved",
        )
        self.assertEqual(audit_plan(plan), [])

    def test_high_drift_without_supported_prior_remains_explicitly_uncertain(self) -> None:
        plan = with_material_human_appearance_omission(valid_plan())
        prior = plan["render_contract"]["human_appearance_decisions"][0][
            "person_prior"
        ]
        prior.update(
            {
                "disposition": "uncertain",
                "candidate_support": "uncertain",
                "omission_counterfactual": {
                    "verdict": "uncertain",
                    "source_evidence": ["held-out ambiguity remains"],
                },
                "residual_risk": "model default may change the broad person reading",
            }
        )
        self.assertEqual(audit_plan(plan), [])

    def test_source_visible_identity_inference_is_not_a_valid_identity_context(self) -> None:
        plan = with_spatial_coverage(valid_plan())
        decision = plan["render_contract"]["human_appearance_decisions"][0]
        decision["identity_context"] = {
            "disposition": "absent",
            "source_reference": "inferred nationality from pixels",
        }
        self.assertTrue(
            any("cannot infer identity" in error for error in audit_plan(plan))
        )

        invalid_disposition = with_spatial_coverage(valid_plan())
        invalid_disposition["render_contract"]["human_appearance_decisions"][0][
            "identity_context"
        ] = {"disposition": "source-visible"}
        self.assertTrue(
            any("identity_context.disposition" in error for error in audit_plan(invalid_disposition))
        )

    def test_external_identity_context_requires_provenance(self) -> None:
        trusted = with_spatial_coverage(valid_plan())
        trusted["render_contract"]["human_appearance_decisions"][0][
            "identity_context"
        ] = {
            "disposition": "trusted-metadata",
            "context_use": "trusted-factual-context",
            "prompt_disposition": "diagnostic-only",
            "viewer_priority": "P1",
            "source_reference": "verified casting metadata record 42",
        }
        self.assertEqual(audit_plan(trusted), [])

        missing_provenance = with_spatial_coverage(valid_plan())
        missing_provenance["render_contract"]["human_appearance_decisions"][0][
            "identity_context"
        ] = {
            "disposition": "trusted-metadata",
            "context_use": "trusted-factual-context",
            "prompt_disposition": "diagnostic-only",
            "viewer_priority": "P1",
        }
        self.assertTrue(
            any(
                "source_reference is required for external identity context" in error
                for error in audit_plan(missing_provenance)
            )
        )

    def test_user_supplied_identity_can_be_prioritized_only_as_external_context(self) -> None:
        plan = with_spatial_coverage(valid_plan())
        contract = plan["render_contract"]
        add_generic_claim(
            contract,
            invariant_id="user-identity-context",
            axis="form",
            owner="subject.human",
            role="primary",
            target_strength="subtle",
            observation="one explicit user-supplied casting target",
            causal_origin="intrinsic",
            evidence="held-out user request field",
            direction="retain-explicit-user-casting-target",
            prompt_excerpt="one explicit user-supplied casting target",
            region_ids=["central-form"],
        )
        contract["emitted_controls"][-1][
            "appearance_dimension"
        ] = "identity-context"
        decision = contract["human_appearance_decisions"][0]
        decision.update(
            {
                "face_visibility": "indistinct",
                "fidelity_salience": "primary",
                "appearance_invariant_ids": ["user-identity-context"],
            }
        )
        decision["identity_context"] = {
            "disposition": "user-supplied",
            "context_use": "creative-target",
            "prompt_disposition": "emit",
            "viewer_priority": "P0",
            "source_reference": "held-out user request field",
            "claim_id": "claim-user-identity-context",
        }
        self.assertEqual(audit_plan(plan, authored_prompt_text(plan)), [])

        low_priority = deepcopy(plan)
        low_priority["render_contract"]["human_appearance_decisions"][0][
            "identity_context"
        ]["viewer_priority"] = "P2"
        self.assertTrue(
            any(
                "identity_context emit requires P0 or P1" in error
                for error in audit_plan(low_priority)
            )
        )

        mismatched_use = deepcopy(plan)
        mismatched_use["render_contract"]["human_appearance_decisions"][0][
            "identity_context"
        ]["context_use"] = "trusted-factual-context"
        self.assertTrue(
            any(
                "does not match its external provenance" in error
                for error in audit_plan(mismatched_use)
            )
        )

    def test_external_identity_context_precedes_person_aesthetic_decomposition(self) -> None:
        plan = with_emitted_person_aesthetic(valid_plan())
        contract = plan["render_contract"]
        add_generic_claim(
            contract,
            invariant_id="external-identity-context",
            axis="form",
            owner="subject.human",
            role="primary",
            target_strength="subtle",
            observation="one explicit externally supplied casting context",
            causal_origin="intrinsic",
            evidence="held-out user request field",
            direction="retain-external-casting-context",
            prompt_excerpt="one explicit externally supplied casting context",
            region_ids=["central-form"],
        )
        identity_control = contract["emitted_controls"].pop()
        summary_index = next(
            index
            for index, control in enumerate(contract["emitted_controls"])
            if control["id"] == "control-person-aesthetic-summary"
        )
        contract["emitted_controls"].insert(summary_index, identity_control)

        decision = contract["human_appearance_decisions"][0]
        decision["appearance_invariant_ids"].append("external-identity-context")
        decision["identity_context"] = {
            "disposition": "user-supplied",
            "context_use": "creative-target",
            "prompt_disposition": "emit",
            "viewer_priority": "P0",
            "source_reference": "held-out user request field",
            "claim_id": "claim-external-identity-context",
        }

        prompt = authored_prompt_text(plan)
        self.assertEqual(audit_plan(plan, prompt), [])
        reversed_prompt = prompt.replace(
            (
                "one explicit externally supplied casting context. "
                "a bounded restrained editorial person aesthetic"
            ),
            (
                "a bounded restrained editorial person aesthetic. "
                "one explicit externally supplied casting context"
            ),
        )
        self.assertTrue(
            any(
                "external identity context must precede" in error
                for error in audit_plan(plan, reversed_prompt)
            )
        )

    def test_person_aesthetic_anchor_leads_owned_cross_module_decomposition(self) -> None:
        plan = with_emitted_person_aesthetic(valid_plan())
        prompt = authored_prompt_text(plan)
        self.assertEqual(audit_plan(plan, prompt), [])
        summary = "a bounded restrained editorial person aesthetic"
        for excerpt in (
            "visible face form constrains that aesthetic",
            "the visible hair mass and face occlusion remain authoritative",
            "the visible garment coverage and construction legibility remain bounded",
            "soft capture and a restrained polish ceiling remain unchanged",
        ):
            self.assertLess(prompt.index(summary), prompt.index(excerpt))

        reversed_prompt = prompt.replace(
            (
                "a bounded restrained editorial person aesthetic. "
                "visible face form constrains that aesthetic"
            ),
            (
                "visible face form constrains that aesthetic. "
                "a bounded restrained editorial person aesthetic"
            ),
        )
        self.assertTrue(
            any(
                "must lead its literal decomposed controls" in error
                for error in audit_plan(plan, reversed_prompt)
            )
        )

    def test_person_aesthetic_effect_budget_rejects_missing_or_misowned_controls(self) -> None:
        plan = with_emitted_person_aesthetic(valid_plan())

        missing_dimension = deepcopy(plan)
        next(
            control
            for control in missing_dimension["render_contract"]["emitted_controls"]
            if control["id"] == "control-person-hair-boundary"
        ).pop("appearance_dimension")
        self.assertTrue(
            any(
                "requires a valid appearance_dimension" in error
                for error in audit_plan(missing_dimension)
            )
        )

        wrong_owner = deepcopy(plan)
        wrong_contract = wrong_owner["render_contract"]
        wrong_invariant = next(
            item
            for item in wrong_contract["invariants"]
            if item["id"] == "person-hair-boundary"
        )
        wrong_claim = next(
            item
            for item in wrong_contract["candidate_claims"]
            if item["id"] == "claim-person-hair-boundary"
        )
        wrong_control = next(
            item
            for item in wrong_contract["emitted_controls"]
            if item["id"] == "control-person-hair-boundary"
        )
        for entry in (wrong_invariant, wrong_claim, wrong_control):
            if "clause_owner" in entry:
                entry["clause_owner"] = "detail.clothing-fashion"
            else:
                entry["owner"] = "detail.clothing-fashion"
        self.assertTrue(
            any(
                "invalid owner for 'hair-boundary'" in error
                for error in audit_plan(wrong_owner)
            )
        )

        identity_leak = deepcopy(plan)
        identity_leak["render_contract"]["human_appearance_decisions"][0][
            "appearance_gestalt"
        ]["effect_budget"]["protected_dimensions"].remove("identity-context")
        self.assertTrue(
            any(
                "must include identity-context" in error
                for error in audit_plan(identity_leak)
            )
        )

    def test_person_aesthetic_generation_prior_requires_a_v3_decision(self) -> None:
        plan = with_emitted_person_aesthetic(valid_plan())
        del plan["render_contract"]["human_appearance_decisions"][0][
            "appearance_gestalt"
        ]
        errors = audit_plan(plan)
        self.assertTrue(
            any("appearance_gestalt must be an object" in error for error in errors)
        )
        self.assertTrue(
            any(
                "require an appearance_gestalt decision" in error for error in errors
            )
        )

    def test_primary_invariant_cannot_be_demoted_to_supporting_claim(self) -> None:
        plan = valid_plan()
        plan["render_contract"]["candidate_claims"][0]["role"] = "supporting"
        self.assertTrue(
            any("claim role does not preserve" in error for error in audit_plan(plan))
        )

    def test_skin_or_surface_claim_cannot_stand_in_for_face_geometry(self) -> None:
        plan = with_material_human_appearance_omission(
            valid_plan(),
            drift_risk="low",
            geometry_sufficiency="sufficient",
            counterfactual="preserved",
        )
        invariant = next(
            item
            for item in plan["render_contract"]["invariants"]
            if item["id"] == "held-out-person-geometry"
        )
        effect = next(
            item
            for item in plan["render_contract"]["aggregate_effects"]
            if item["id"] == "effect-held-out-person-geometry"
        )
        invariant["axis"] = "surface"
        effect["axis"] = "surface"
        self.assertTrue(
            any("emitted human form geometry" in error for error in audit_plan(plan))
        )

    def test_body_form_can_own_material_appearance_geometry(self) -> None:
        plan = with_material_human_appearance_omission(
            valid_plan(),
            drift_risk="low",
            geometry_sufficiency="sufficient",
            counterfactual="preserved",
        )
        contract = plan["render_contract"]
        appearance = contract["human_appearance_decisions"][0]
        appearance_invariant = contract["invariants"][-1]
        appearance_claim = next(
            claim
            for claim in contract["candidate_claims"]
            if claim["id"] == appearance["person_prior"]["geometry_claim_ids"][0]
        )
        appearance_invariant["clause_owner"] = "detail.human-body-form"
        appearance_claim["owner"] = "detail.human-body-form"
        control = next(
            item
            for item in contract["emitted_controls"]
            if item["claim_id"] == appearance_claim["id"]
        )
        control["owner"] = "detail.human-body-form"
        self.assertEqual(audit_plan(plan), [])

    def test_axis_composed_skin_descriptor_reaches_the_exact_prompt(self) -> None:
        plan = with_material_skin_descriptor(valid_color_plan())
        prompt = authored_prompt_text(plan)
        self.assertEqual(audit_plan(plan, prompt), [])
        self.assertIn(
            "visible skin with a light value, low chroma, an olive undertone, and a satin finish",
            prompt,
        )

        missing_phrase = prompt.replace(
            "visible skin with a light value, low chroma, an olive undertone, and a satin finish",
            "visible skin",
        )
        self.assertTrue(
            any(
                "controlled_descriptor.phrase appears 0 times" in error
                for error in audit_plan(plan, missing_phrase)
            )
        )

    def test_skin_surface_is_prioritized_as_displayed_color_not_identity(self) -> None:
        plan = with_material_skin_descriptor(valid_color_plan())
        self.assertEqual(audit_plan(plan, authored_prompt_text(plan)), [])

        identity_proxy = deepcopy(plan)
        identity_proxy["render_contract"]["human_appearance_decisions"][0][
            "skin_surface"
        ]["semantic_use"] = "demographic-identity"
        self.assertTrue(
            any(
                "semantic_use must remain displayed-surface" in error
                for error in audit_plan(identity_proxy)
            )
        )

        low_priority = deepcopy(plan)
        low_priority["render_contract"]["human_appearance_decisions"][0][
            "skin_surface"
        ]["viewer_priority"] = "P2"
        self.assertTrue(
            any(
                "descriptor emission requires P0 or P1" in error
                for error in audit_plan(low_priority)
            )
        )

        scope_mismatch = deepcopy(plan)
        scope_mismatch["render_contract"]["human_appearance_decisions"][0][
            "skin_surface"
        ]["observation_scope"] = "user-specified"
        self.assertTrue(
            any(
                "observation_scope must match surface_color_language" in error
                for error in audit_plan(scope_mismatch)
            )
        )

    def test_controlled_descriptor_rejects_hardcoded_or_misowned_axes(self) -> None:
        phrase_tamper = with_material_skin_descriptor(valid_color_plan())
        descriptor = phrase_tamper["render_contract"]["color_tone_contract"][
            "surface_color_language"
        ]["controlled_descriptor"]
        descriptor["phrase"] = descriptor["phrase"].replace(
            "a light value", "a very light value"
        )
        self.assertTrue(
            any(
                "phrase does not match the classified axes" in error
                for error in audit_plan(phrase_tamper)
            )
        )

        wrong_owner = with_material_skin_descriptor(valid_color_plan())
        descriptor = wrong_owner["render_contract"]["color_tone_contract"][
            "surface_color_language"
        ]["controlled_descriptor"]
        descriptor["axis_control_ids"]["undertone"] = "control-surface-chroma"
        self.assertTrue(
            any(
                "axis_control_ids.undertone controls the wrong color axis" in error
                for error in audit_plan(wrong_owner)
            )
        )

        wrong_finish = with_material_skin_descriptor(valid_color_plan())
        finish_effect = next(
            item
            for item in wrong_finish["render_contract"]["aggregate_effects"]
            if item["id"] == "effect-visible-surface-finish"
        )
        finish_effect["region_ids"] = ["surrounding-field"]
        self.assertTrue(
            any(
                "finish must control the same region's surface axis" in error
                for error in audit_plan(wrong_finish)
            )
        )

    def test_partial_descriptor_emits_only_stable_requested_axes(self) -> None:
        plan = with_material_skin_descriptor(valid_color_plan())
        contract = plan["render_contract"]
        surface = contract["color_tone_contract"]["surface_color_language"]
        surface["axis_classification"]["finish"]["confidence"] = "low"
        descriptor = compose_controlled_descriptor(
            {"axis_classification": surface["axis_classification"]},
            "visible skin",
            include_finish=True,
        )
        descriptor.update(
            {
                "emit": True,
                "axis_control_ids": {
                    "value_depth": "control-surface-tone",
                    "chroma": "control-surface-chroma",
                    "undertone": "control-surface-hue",
                },
                "source_evidence": ["held-out stable core axes"],
            }
        )
        surface["controlled_descriptor"] = descriptor
        contract["invariants"] = [
            item for item in contract["invariants"] if item["id"] != "visible-surface-finish"
        ]
        contract["candidate_claims"] = [
            item
            for item in contract["candidate_claims"]
            if item["id"] != "claim-visible-surface-finish"
        ]
        contract["aggregate_effects"] = [
            item
            for item in contract["aggregate_effects"]
            if item["id"] != "effect-visible-surface-finish"
        ]
        contract["emitted_controls"] = [
            item
            for item in contract["emitted_controls"]
            if item["id"] != "control-visible-surface-finish"
        ]
        prompt = authored_prompt_text(plan)
        self.assertEqual(audit_plan(plan, prompt), [])
        self.assertIn(
            "visible skin with a light value, low chroma, and an olive undertone",
            prompt,
        )
        self.assertNotIn("satin finish", prompt)

    def test_boundary_only_descriptor_cannot_emit(self) -> None:
        plan = with_material_skin_descriptor(valid_color_plan())
        surface = plan["render_contract"]["color_tone_contract"][
            "surface_color_language"
        ]
        for axis in ("value_depth", "chroma", "undertone", "finish"):
            surface["axis_classification"][axis].update(
                {"confidence": "medium", "runner_up": "adjacent-held-out-class"}
            )
        descriptor = compose_controlled_descriptor(
            {"axis_classification": surface["axis_classification"]},
            "visible skin",
            include_finish=True,
        )
        descriptor.update(
            {
                "emit": True,
                "axis_control_ids": {},
                "source_evidence": ["held-out boundary evidence"],
            }
        )
        surface["controlled_descriptor"] = descriptor
        self.assertTrue(
            any(
                "cannot emit without stable classified axes" in error
                for error in audit_plan(plan)
            )
        )

    def test_material_skin_requires_a_matching_color_region(self) -> None:
        plan = with_material_skin_descriptor(valid_color_plan())
        plan["render_contract"]["human_appearance_decisions"][0]["skin_surface"][
            "region_ids"
        ] = ["untracked-skin-region"]
        self.assertTrue(
            any(
                "require matching Color/Tone regions" in error
                for error in audit_plan(plan)
            )
        )

        contradictory = with_material_skin_descriptor(valid_color_plan())
        skin = contradictory["render_contract"]["human_appearance_decisions"][0][
            "skin_surface"
        ]
        skin["descriptor_disposition"] = "omit"
        skin["descriptor_non_emission_reason"] = "prompt budget"
        self.assertTrue(
            any(
                "descriptor decision contradicts" in error
                for error in audit_plan(contradictory)
            )
        )

    def test_cross_component_alignment_and_offset_are_both_valid(self) -> None:
        for direction in (
            "the source components share one aligned axis",
            "the source components keep visibly offset axes",
        ):
            plan = promote_spatial_decision(
                with_spatial_coverage(valid_plan(), kind="non-human"),
                "cross-component-orientation",
                direction=direction,
            )
            self.assertEqual(audit_plan(plan), [])

    def test_pose_owned_axis_cannot_be_relabelled_as_intrinsic_anatomy(self) -> None:
        plan = promote_spatial_decision(
            with_spatial_coverage(valid_plan()),
            "human-shoulder-image-slope",
            direction="source-visible shoulder-line relation",
        )
        invariant_id = next(
            item
            for item in plan["render_contract"]["spatial_orientation_coverage"][
                "decisions"
            ]
            if item["dimension"] == "human-shoulder-image-slope"
        )["invariant_id"]
        next(
            item
            for item in plan["render_contract"]["invariants"]
            if item["id"] == invariant_id
        )["causal_origin"] = "intrinsic"
        self.assertTrue(
            any(
                "causal_origin must match its invariant" in error
                for error in audit_plan(plan)
            )
        )

    def test_spatial_dimension_rejects_a_consistently_wrong_causal_owner(self) -> None:
        plan = promote_spatial_decision(
            with_spatial_coverage(valid_plan()),
            "human-head-body-yaw",
        )
        contract = plan["render_contract"]
        decision = next(
            item
            for item in contract["spatial_orientation_coverage"]["decisions"]
            if item["dimension"] == "human-head-body-yaw"
        )
        decision["causal_origin"] = "intrinsic"
        next(
            item
            for item in contract["invariants"]
            if item["id"] == decision["invariant_id"]
        )["causal_origin"] = "intrinsic"
        next(
            item
            for item in contract["aggregate_effects"]
            if item["id"] == decision["aggregate_effect_id"]
        )["causal_origin"] = "intrinsic"
        next(
            item
            for item in contract["emitted_controls"]
            if item["id"] == decision["control_id"]
        )["causal_origin"] = "intrinsic"
        self.assertTrue(
            any(
                "is not allowed for dimension" in error
                for error in audit_plan(plan)
            )
        )

    def test_partial_component_relation_requires_fragment_and_completion_budget(self) -> None:
        plan = valid_plan()
        contract = plan["render_contract"]
        contract["component_relations"].append(
            {
                "id": "partial-secondary-layer",
                "kind": "partial-visibility",
                "subject_region_id": "surrounding-field",
                "reference_region_id": "central-form",
                "observation": "only a few secondary-layer fragments remain inside the crop",
                "role": "supporting",
                "visible_fragments": ["one contour fragment", "one low-detail mark"],
                "hidden_or_cropped": ["the counterpart stays outside the frame"],
                "completion_risk": "high",
                "source_evidence": ["hard crop interrupts the secondary layer"],
            }
        )
        contract["aggregate_effects"][1]["relation_ids"].append(
            "partial-secondary-layer"
        )
        self.assertEqual(audit_plan(plan), [])
        del contract["component_relations"][-1]["hidden_or_cropped"]
        self.assertTrue(
            any("hidden_or_cropped" in error for error in audit_plan(plan))
        )

    def test_multi_region_form_topology_requires_a_region_boundary_relation(self) -> None:
        plan = valid_plan()
        contract = plan["render_contract"]
        add_generic_claim(
            contract,
            invariant_id="multi-region-boundary",
            axis="topology",
            owner="concept.primary-relationship",
            role="primary",
            target_strength="moderate",
            observation="two visible regions keep their source-relative boundary topology",
            causal_origin="material-interaction",
            evidence="two independently visible boundary components",
            direction="source-relative-multi-boundary-topology",
            prompt_excerpt="two visible regions retain an asymmetric interlocking boundary topology",
            region_ids=["central-form", "surrounding-field"],
            relation_ids=["central-field-relation"],
        )
        self.assertTrue(
            any(
                "must preserve a region-to-region boundary relation" in error
                for error in audit_plan(plan)
            )
        )

        contract["component_relations"].append(
            {
                "id": "central-to-surround-boundary",
                "kind": "boundary-crossing",
                "subject_region_id": "central-form",
                "reference_region_id": "surrounding-field",
                "observation": "the two regions meet along the source-visible asymmetric boundary",
                "role": "primary",
                "source_evidence": ["continuous shared boundary"],
            }
        )
        contract["aggregate_effects"][-1]["relation_ids"] = [
            "central-to-surround-boundary"
        ]
        self.assertEqual(audit_plan(plan), [])

    def test_person_gestalt_generation_prior_requires_provenance_and_geometry(self) -> None:
        plan = with_spatial_coverage(valid_plan())
        contract = plan["render_contract"]
        add_generic_claim(
            contract,
            invariant_id="readable-face-gestalt",
            axis="form",
            owner="subject.human",
            role="supporting",
            target_strength="subtle",
            observation="a source-relative readable face gestalt",
            causal_origin="intrinsic",
            evidence="visible face silhouette and feature relationships",
            direction="preserve-source-relative-face-gestalt",
            prompt_excerpt="one compact face passage constrained by visible geometry",
            region_ids=["central-form"],
        )
        prior_claim = contract["candidate_claims"][-1]
        add_generic_claim(
            contract,
            invariant_id="source-face-geometry",
            axis="form",
            owner="detail.human-face-likeness",
            role="supporting",
            target_strength="subtle",
            observation="source-visible face silhouette and feature relationships",
            causal_origin="intrinsic",
            evidence="visible jaw taper, feature spacing, and asymmetry",
            direction="source-relative-face-geometry",
            prompt_excerpt="visible jaw taper and feature spacing constrain the face gestalt",
            region_ids=["central-form"],
        )
        prior_claim["generation_prior"] = {
            "scope": "person-gestalt",
            "candidate_source": {
                "kind": "user-supplied",
                "reference": "held-out request context",
            },
            "non_identifying": True,
            "visible_geometry_evidence": [
                "source-visible silhouette, feature relations, and asymmetry"
            ],
            "geometry_claim_ids": ["claim-source-face-geometry"],
        }
        appearance_decision = contract["human_appearance_decisions"][0]
        appearance_decision.update(
            {
                "fidelity_salience": "supporting",
                "appearance_invariant_ids": ["readable-face-gestalt"],
            }
        )
        appearance_decision["person_prior"].update(
            {
                "disposition": "emit",
                "confidence": "medium",
                "candidate_support": "supported",
                "default_drift_risk": "high",
                "local_geometry_sufficiency": "sufficient",
                "geometry_claim_ids": ["claim-source-face-geometry"],
                "source_evidence": ["source-relative readable face gestalt"],
                "claim_id": "claim-readable-face-gestalt",
            }
        )
        appearance_decision["person_prior"].pop("non_emission_reason", None)
        appearance_decision["person_prior"].pop("omission_counterfactual", None)
        self.assertEqual(audit_plan(plan), [])
        self.assertEqual(
            audit_plan(plan, prompt_text=authored_prompt_text(plan)), []
        )

        controls = {
            item["id"]: item for item in contract["emitted_controls"]
        }
        separated_prompt = "PROMPT:\n" + ". ".join(
            controls[control_id]["prompt_excerpt"]
            for control_id in (
                "control-readable-face-gestalt",
                "control-form",
                "control-source-face-geometry",
                "control-balance",
                "control-placement",
            )
        )
        self.assertTrue(
            any(
                "must remain adjacent to linked local geometry" in error
                for error in audit_plan(plan, prompt_text=separated_prompt)
            )
        )

        missing_source = deepcopy(plan)
        missing_source_claim = next(
            item
            for item in missing_source["render_contract"]["candidate_claims"]
            if item["id"] == "claim-readable-face-gestalt"
        )
        del missing_source_claim["generation_prior"]["candidate_source"]
        self.assertTrue(
            any("candidate_source" in error for error in audit_plan(missing_source))
        )

        missing_geometry = deepcopy(plan)
        missing_geometry_claim = next(
            item
            for item in missing_geometry["render_contract"]["candidate_claims"]
            if item["id"] == "claim-readable-face-gestalt"
        )
        missing_geometry_claim["generation_prior"]["visible_geometry_evidence"] = []
        self.assertTrue(
            any(
                "visible_geometry_evidence" in error
                for error in audit_plan(missing_geometry)
            )
        )

    def test_generation_prior_geometry_claim_ids_must_reach_owned_prompt_controls(self) -> None:
        plan = with_spatial_coverage(valid_plan())
        contract = plan["render_contract"]
        add_generic_claim(
            contract,
            invariant_id="broad-person-anchor",
            axis="form",
            owner="subject.human",
            role="supporting",
            target_strength="subtle",
            observation="one non-identifying source-relative person anchor",
            causal_origin="intrinsic",
            evidence="readable broad face gestalt",
            direction="bounded-source-relative-person-anchor",
            prompt_excerpt="one bounded non-identifying person anchor",
            region_ids=["central-form"],
        )
        prior_claim = contract["candidate_claims"][-1]
        add_generic_claim(
            contract,
            invariant_id="local-face-geometry",
            axis="form",
            owner="detail.human-face-likeness",
            role="supporting",
            target_strength="subtle",
            observation="local visible geometry corrects the broad person prior",
            causal_origin="intrinsic",
            evidence="source-visible silhouette and feature relations",
            direction="source-relative-local-face-geometry",
            prompt_excerpt="local silhouette and feature relations correct the broad anchor",
            region_ids=["central-form"],
        )
        prior_claim["generation_prior"] = {
            "scope": "person-gestalt",
            "candidate_source": {
                "kind": "source-visible-approximation",
                "reference": "held-out source observation",
            },
            "non_identifying": True,
            "visible_geometry_evidence": ["local silhouette and feature relations"],
            "geometry_claim_ids": ["claim-local-face-geometry"],
        }
        appearance_decision = contract["human_appearance_decisions"][0]
        appearance_decision.update(
            {
                "fidelity_salience": "supporting",
                "appearance_invariant_ids": ["broad-person-anchor"],
            }
        )
        appearance_decision["person_prior"].update(
            {
                "disposition": "emit",
                "confidence": "medium",
                "candidate_support": "supported",
                "default_drift_risk": "high",
                "local_geometry_sufficiency": "sufficient",
                "geometry_claim_ids": ["claim-local-face-geometry"],
                "source_evidence": ["one non-identifying source-relative person anchor"],
                "claim_id": "claim-broad-person-anchor",
            }
        )
        appearance_decision["person_prior"].pop("non_emission_reason", None)
        appearance_decision["person_prior"].pop("omission_counterfactual", None)
        self.assertEqual(audit_plan(plan), [])

        missing_ids = deepcopy(plan)
        next(
            item
            for item in missing_ids["render_contract"]["candidate_claims"]
            if item["id"] == "claim-broad-person-anchor"
        )["generation_prior"]["geometry_claim_ids"] = []
        self.assertTrue(
            any("geometry_claim_ids" in error for error in audit_plan(missing_ids))
        )

        unknown = deepcopy(plan)
        next(
            item
            for item in unknown["render_contract"]["candidate_claims"]
            if item["id"] == "claim-broad-person-anchor"
        )["generation_prior"]["geometry_claim_ids"] = ["claim-not-present"]
        self.assertTrue(
            any("unknown geometry claim" in error for error in audit_plan(unknown))
        )

        self_reference = deepcopy(plan)
        next(
            item
            for item in self_reference["render_contract"]["candidate_claims"]
            if item["id"] == "claim-broad-person-anchor"
        )["generation_prior"]["geometry_claim_ids"] = [
            "claim-broad-person-anchor"
        ]
        self.assertTrue(
            any("separate geometry claim" in error for error in audit_plan(self_reference))
        )

        wrong_owner = deepcopy(plan)
        wrong_contract = wrong_owner["render_contract"]
        geometry_claim = next(
            item
            for item in wrong_contract["candidate_claims"]
            if item["id"] == "claim-local-face-geometry"
        )
        geometry_claim["owner"] = "subject.generic-object"
        next(
            item
            for item in wrong_contract["invariants"]
            if item["id"] == "local-face-geometry"
        )["clause_owner"] = "subject.generic-object"
        next(
            item
            for item in wrong_contract["emitted_controls"]
            if item["claim_id"] == "claim-local-face-geometry"
        )["owner"] = "subject.generic-object"
        self.assertTrue(
            any(
                "human, face, or body-form module" in error
                for error in audit_plan(wrong_owner)
            )
        )

        uncontrolled = deepcopy(plan)
        uncontrolled["render_contract"]["emitted_controls"] = [
            item
            for item in uncontrolled["render_contract"]["emitted_controls"]
            if item["claim_id"] != "claim-local-face-geometry"
        ]
        self.assertTrue(
            any(
                "exactly one generic prompt control" in error
                for error in audit_plan(uncontrolled)
            )
        )

    def test_source_visible_attractiveness_anchor_is_retained_with_local_geometry(self) -> None:
        plan = with_spatial_coverage(valid_plan())
        contract = plan["render_contract"]
        add_generic_claim(
            contract,
            invariant_id="overall-face-reading",
            axis="form",
            owner="detail.human-face-likeness",
            role="primary",
            target_strength="moderate",
            observation="a material source-visible overall attractiveness reading",
            causal_origin="intrinsic",
            evidence="coherent visible facial gestalt",
            direction="retain-source-visible-overall-face-reading",
            prompt_excerpt="a distinctly attractive overall facial reading",
            region_ids=["central-form"],
        )
        prior_claim = contract["candidate_claims"][-1]
        add_generic_claim(
            contract,
            invariant_id="decisive-face-relations",
            axis="form",
            owner="detail.human-face-likeness",
            role="primary",
            target_strength="moderate",
            observation="decisive local feature relationships constrain the overall reading",
            causal_origin="intrinsic",
            evidence="source-visible eye spacing, jaw taper, and feature projection",
            direction="source-relative-decisive-face-relations",
            prompt_excerpt="large readable eyes, clear feature definition, and a long tapered facial outline",
            region_ids=["central-form"],
        )
        prior_claim["generation_prior"] = {
            "scope": "attractiveness",
            "candidate_source": {
                "kind": "source-visible-approximation",
                "reference": "held-out current-source observation",
            },
            "non_identifying": True,
            "visible_geometry_evidence": [
                "source-visible eye spacing, jaw taper, and feature projection"
            ],
            "geometry_claim_ids": ["claim-decisive-face-relations"],
            "decomposed_control_ids": ["control-decisive-face-relations"],
        }
        geometry_control = next(
            control
            for control in contract["emitted_controls"]
            if control["id"] == "control-decisive-face-relations"
        )
        geometry_control["appearance_dimension"] = "face-form"
        decision = contract["human_appearance_decisions"][0]
        decision.update(
            {
                "fidelity_salience": "primary",
                "appearance_invariant_ids": [
                    "overall-face-reading",
                    "decisive-face-relations",
                ],
            }
        )
        decision["person_prior"].update(
            {
                "default_drift_risk": "low",
                "local_geometry_sufficiency": "sufficient",
                "geometry_claim_ids": ["claim-decisive-face-relations"],
                "omission_counterfactual": {
                    "verdict": "preserved",
                    "source_evidence": [
                        "local geometry preserves the non-demographic face reading"
                    ],
                },
            }
        )
        decision["appearance_gestalt"] = {
            "scope": "attractiveness",
            "disposition": "emit",
            "confidence": "high",
            "candidate_support": "supported",
            "viewer_priority": "P0",
            "default_drift_risk": "high",
            "source_evidence": [
                "coherent visible facial gestalt carries the overall reading"
            ],
            "claim_id": "claim-overall-face-reading",
            "decomposition_control_ids": ["control-decisive-face-relations"],
            "effect_budget": {
                "intended_dimensions": ["face-form"],
                "protected_dimensions": [
                    "identity-context",
                    "cosmetic-visibility",
                    "capture-treatment",
                    "scale-crop",
                ],
                "source_evidence": [
                    "the aggregate must not add demographic, makeup, polish, or crop changes"
                ],
            },
            "omission_counterfactual": {
                "verdict": "material-drift",
                "source_evidence": [
                    "geometry alone loses the material overall facial reading"
                ],
            },
        }
        prompt = authored_prompt_text(plan)
        self.assertEqual(audit_plan(plan, prompt), [])
        self.assertLess(
            prompt.index("a distinctly attractive overall facial reading"),
            prompt.index(
                "large readable eyes, clear feature definition, and a long tapered facial outline"
            ),
        )

    def test_authored_prompt_must_contain_each_control_excerpt_exactly_once(self) -> None:
        plan = valid_plan()
        prompt = authored_prompt_text(plan)
        self.assertEqual(audit_plan(plan, prompt_text=prompt), [])

        duplicated = prompt + ". " + plan["render_contract"]["emitted_controls"][0][
            "prompt_excerpt"
        ]
        self.assertTrue(
            any("appears 2 times" in error for error in audit_plan(plan, duplicated))
        )

        self.assertTrue(
            any(
                "appears 0 times" in error
                for error in audit_plan(plan, "PROMPT: unrelated wording")
            )
        )

    def test_generic_and_light_contracts_cannot_share_claim_or_excerpt(self) -> None:
        plan = valid_light_plan()
        contract = plan["render_contract"]
        light_claim = contract["candidate_claims"][-1]
        light_claim["salience_effects"] = [
            {
                "aggregate_effect_id": "generic-light-duplicate",
                "source_evidence": ["duplicated light direction"],
            }
        ]
        contract["aggregate_effects"].append(
            {
                "id": "generic-light-duplicate",
                "axis": "form",
                "direction": "duplicate-light-induced-form",
                "role": "primary",
                "target_strength": "moderate",
                "claim_ids": [light_claim["id"]],
                "region_ids": ["central-form"],
                "relation_ids": [],
                "source_supported": True,
                "source_evidence": ["duplicated light direction"],
            }
        )
        contract["emitted_controls"].append(
            {
                "id": "control-generic-light-duplicate",
                "prompt_excerpt": contract["light_form_contract"][
                    "emitted_controls"
                ][0]["prompt_excerpt"],
                "claim_id": light_claim["id"],
                "owner": light_claim["owner"],
                "aggregate_effect_ids": ["generic-light-duplicate"],
            }
        )
        errors = audit_plan(plan)
        self.assertTrue(any("cannot own the same claims" in error for error in errors))
        self.assertTrue(
            any("cannot own the same prompt excerpts" in error for error in errors)
        )

    def test_primary_generic_effect_changes_pair_signature(self) -> None:
        baseline = valid_plan()
        variant = deepcopy(baseline)
        variant["render_contract"]["aggregate_effects"][0]["direction"] = (
            "expanded-silhouette-with-abrupt-transitions"
        )
        self.assertTrue(
            any(
                "changed the primary salience signature" in error
                for error in compare_plans(
                    baseline, variant, "invariant-preserving"
                )
            )
        )

    def test_documented_evaluation_schema_passes(self) -> None:
        reference = (
            Path(__file__).resolve().parents[1]
            / "references"
            / "behavior-evaluation.md"
        ).read_text(encoding="utf-8")
        match = re.search(r"```json\n(.*?)\n```", reference, re.DOTALL)
        self.assertIsNotNone(match)
        self.assertEqual(audit_plan(json.loads(match.group(1))), [])

    def test_valid_color_tone_contract_passes(self) -> None:
        self.assertEqual(audit_plan(valid_color_plan()), [])

    def test_displayed_key_and_local_form_contrast_can_coexist_independently(self) -> None:
        plan = with_displayed_key_response(valid_color_and_light_plan())
        self.assertEqual(audit_plan(plan), [])
        self.assertEqual(
            audit_plan(plan, prompt_text=authored_prompt_text(plan)), []
        )

        missing_protection = deepcopy(plan)
        del missing_protection["render_contract"]["color_tone_contract"][
            "emitted_controls"
        ][0]["protected_light_effect_ids"]
        self.assertTrue(
            any(
                "must protect overlapping primary Light/Form effects" in error
                for error in audit_plan(missing_protection)
            )
        )

        contract = plan["render_contract"]
        generic = [
            item["prompt_excerpt"] for item in contract["emitted_controls"]
        ]
        color = [
            item["prompt_excerpt"]
            for item in contract["color_tone_contract"]["emitted_controls"]
        ]
        light = [
            item["prompt_excerpt"]
            for item in contract["light_form_contract"]["emitted_controls"]
        ]
        buried_light_prompt = "PROMPT:\n" + ". ".join(generic + color + light)
        self.assertTrue(
            any(
                "must appear before overlapping tone control" in error
                for error in audit_plan(plan, prompt_text=buried_light_prompt)
            )
        )

    def test_regional_displayed_tone_requires_color_region_and_exact_prompt_anchor(self) -> None:
        coarse = with_displayed_key_response(valid_color_plan())
        color_contract = coarse["render_contract"]["color_tone_contract"]
        response = color_contract["displayed_tone_response"][0]
        response["region_id"] = "surrounding-field"
        response["tone_scope"].update(
            {
                "affected_region_ids": ["surrounding-field"],
                "protected_region_ids": ["central-form"],
                "prompt_anchor": "surrounding field",
            }
        )
        color_contract["aggregate_effects"][-1]["region_id"] = "surrounding-field"
        color_contract["emitted_controls"][-1].update(
            {
                "region_id": "surrounding-field",
                "prompt_excerpt": "on the surrounding field, a high displayed key",
            }
        )
        self.assertTrue(
            any("must target one color region" in error for error in audit_plan(coarse))
        )

        unscoped = with_displayed_key_response(valid_color_plan())
        unscoped["render_contract"]["color_tone_contract"]["emitted_controls"][-1][
            "prompt_excerpt"
        ] = "a high displayed key while preserving detail"
        self.assertTrue(
            any("exact region scope anchor" in error for error in audit_plan(unscoped))
        )

    def test_displayed_tone_scope_cannot_also_protect_its_target(self) -> None:
        plan = with_displayed_key_response(valid_color_plan())
        scope = plan["render_contract"]["color_tone_contract"][
            "displayed_tone_response"
        ][0]["tone_scope"]
        scope["protected_region_ids"] = ["central-form"]
        self.assertTrue(
            any("cannot protect an affected region" in error for error in audit_plan(plan))
        )

    def test_region_group_tone_scope_reuses_declared_prompt_anchor(self) -> None:
        plan = with_displayed_key_response(valid_color_plan())
        color_contract = plan["render_contract"]["color_tone_contract"]
        color_contract["regions"].append(
            {
                "id": "secondary-form",
                "prompt_anchor": "secondary form",
                "role": "supporting",
                "intrinsic_axes": [
                    {
                        "axis": "value",
                        "role": "supporting",
                        "evidence_scope": "flat",
                        "emission": "diagnostic-only",
                        "non_emission_reason": "the local value does not need its own prompt control",
                        "observation": "near the central form in value",
                        "confidence": "medium",
                        "source_evidence": ["source-visible adjacent region"],
                    }
                ],
                "tone_zones": [],
                "relative_relations": ["close to the central form"],
                "source_evidence": ["coherent supporting patch"],
            }
        )
        color_contract["region_groups"] = [
            {
                "id": "paired-forms",
                "member_region_ids": ["central-form", "secondary-form"],
                "prompt_anchor": "paired forms",
                "source_evidence": ["both regions share the displayed response"],
            }
        ]
        response = color_contract["displayed_tone_response"][0]
        response["region_id"] = "paired-forms"
        response["tone_scope"].update(
            {
                "kind": "region-group",
                "affected_region_ids": ["central-form", "secondary-form"],
                "prompt_anchor": "both forms",
            }
        )
        color_contract["aggregate_effects"][-1]["region_id"] = "paired-forms"
        color_contract["emitted_controls"][-1].update(
            {
                "region_id": "paired-forms",
                "prompt_excerpt": "on both forms, a high displayed key",
            }
        )
        self.assertTrue(
            any(
                "must reuse the declared group prompt anchor" in error
                for error in audit_plan(plan)
            )
        )

    def test_displayed_tone_scope_rejects_trivial_substring_anchor(self) -> None:
        plan = with_displayed_key_response(valid_color_plan())
        color_contract = plan["render_contract"]["color_tone_contract"]
        color_contract["regions"][0]["prompt_anchor"] = "a"
        color_contract["displayed_tone_response"][0]["tone_scope"][
            "prompt_anchor"
        ] = "a"
        self.assertTrue(
            any("non-trivial exact" in error for error in audit_plan(plan))
        )

    def test_required_displayed_tone_axis_needs_its_own_axis_control(self) -> None:
        plan = with_displayed_key_response(valid_color_plan())
        controls = plan["render_contract"]["color_tone_contract"]["emitted_controls"]
        controls[-1]["control_role"] = "compound-control"
        controls[-1]["compound_justification"] = "generic brightness shorthand"
        self.assertTrue(
            any(
                "required displayed-tone axis needs its own axis-control" in error
                for error in audit_plan(plan)
            )
        )

    def test_displayed_tone_axis_rejects_wrong_causal_owner(self) -> None:
        plan = with_displayed_key_response(valid_color_plan())
        contract = plan["render_contract"]
        contract["candidate_claims"][-1]["perceptual_effects"][0][
            "causal_layer"
        ] = "intrinsic"
        contract["color_tone_contract"]["emitted_controls"][-1][
            "causal_layer"
        ] = "intrinsic"
        self.assertTrue(
            any(
                "displayed-key-level cannot be owned" in error
                for error in audit_plan(plan)
            )
        )

    def test_compatible_surface_language_review_can_remain_non_emitted(self) -> None:
        plan = add_surface_language_review(valid_color_plan())
        plan["render_contract"]["color_tone_contract"]["appearance_metaphors"] = [
            {
                "phrase": "analyst candidate label",
                "status": "explanation-only",
                "emit": False,
                "decomposed_control_ids": ["control-surface-tone"],
            }
        ]
        self.assertEqual(audit_plan(plan), [])

    def test_surface_language_review_requires_candidate_provenance(self) -> None:
        plan = add_surface_language_review(valid_color_plan())
        review = plan["render_contract"]["color_tone_contract"][
            "surface_color_language"
        ]["friendly_label_review"][0]
        del review["candidate_source"]
        self.assertTrue(
            any(
                "candidate_source must be an object" in error
                for error in audit_plan(plan)
            )
        )

    def test_surface_language_review_rejects_internal_candidate_source(self) -> None:
        plan = add_surface_language_review(valid_color_plan())
        review = plan["render_contract"]["color_tone_contract"][
            "surface_color_language"
        ]["friendly_label_review"][0]
        review["candidate_source"]["kind"] = "skill-example"
        self.assertTrue(
            any(
                "candidate_source.kind is invalid" in error
                for error in audit_plan(plan)
            )
        )

    def test_source_visible_surface_descriptor_may_lead_literal_controls(self) -> None:
        plan = add_surface_language_review(
            valid_color_plan(), source_kind="source-visible-approximation"
        )
        plan["render_contract"]["color_tone_contract"]["appearance_metaphors"] = [
            {
                "phrase": "analyst candidate label",
                "status": "source-evidence-qualified",
                "emit": True,
                "source_evidence": ["current-source surface reading and stable axis evidence"],
                "confidence": "high",
                "viewer_priority": "P0",
                "omission_counterfactual": "material-drift",
                "decomposed_control_ids": ["control-surface-tone"],
            }
        ]
        self.assertEqual(audit_plan(plan), [])
        prompt = authored_prompt_text(plan)
        self.assertEqual(audit_plan(plan, prompt), [])
        self.assertLess(
            prompt.index("analyst candidate label"),
            prompt.index("a central field visibly lighter than the surround"),
        )

        wrong_order = prompt.replace(
            "analyst candidate label. a central field visibly lighter than the surround",
            "a central field visibly lighter than the surround. analyst candidate label",
        )
        self.assertTrue(
            any(
                "must lead its literal decomposed controls" in error
                for error in audit_plan(plan, wrong_order)
            )
        )

    def test_source_visible_surface_descriptor_requires_material_evidence(self) -> None:
        plan = add_surface_language_review(
            valid_color_plan(), source_kind="source-visible-approximation"
        )
        plan["render_contract"]["color_tone_contract"]["appearance_metaphors"] = [
            {
                "phrase": "analyst candidate label",
                "status": "source-evidence-qualified",
                "emit": True,
                "source_evidence": [],
                "confidence": "low",
                "viewer_priority": "P2",
                "omission_counterfactual": "preserved",
                "decomposed_control_ids": ["control-surface-tone"],
            }
        ]
        errors = audit_plan(plan)
        self.assertTrue(any("source_evidence" in error for error in errors))
        self.assertTrue(any("confidence must be high or medium" in error for error in errors))
        self.assertTrue(any("viewer_priority must be P0 or P1" in error for error in errors))
        self.assertTrue(any("must be material-drift" in error for error in errors))

    def test_conflicting_surface_label_cannot_be_emitted(self) -> None:
        plan = add_surface_language_review(valid_color_plan(), conflicting=True)
        plan["render_contract"]["color_tone_contract"]["appearance_metaphors"] = [
            {
                "phrase": "analyst candidate label",
                "status": "model-calibrated",
                "emit": True,
                "calibration_evidence": ["matched generator/version response study"],
                "decomposed_control_ids": ["control-surface-tone"],
            }
        ]
        self.assertTrue(
            any(
                "requires a compatible surface-color-language review" in error
                for error in audit_plan(plan)
            )
        )

    def test_valid_light_form_contract_passes(self) -> None:
        self.assertEqual(audit_plan(valid_light_plan()), [])

    def test_pairwise_light_regions_must_reference_known_distinct_regions(self) -> None:
        unknown = valid_light_plan()
        unknown["render_contract"]["light_form_contract"]["region_effects"][0][
            "reference_region_id"
        ] = "missing-region"
        self.assertTrue(
            any(
                "reference_region_id references an unknown region" in error
                for error in audit_plan(unknown)
            )
        )

        same = valid_light_plan()
        same["render_contract"]["light_form_contract"]["region_effects"][0][
            "reference_region_id"
        ] = "central-form"
        self.assertTrue(
            any("reference a distinct region" in error for error in audit_plan(same))
        )

        global_target = valid_light_plan()
        light_contract = global_target["render_contract"]["light_form_contract"]
        light_contract["region_effects"][0]["region_id"] = "global"
        light_contract["region_effects"][0]["reference_region_id"] = "central-form"
        self.assertTrue(
            any(
                "region_id must reference a major region for comparison" in error
                for error in audit_plan(global_target)
            )
        )

    def test_pairwise_light_observation_and_aggregate_actuation_must_match(self) -> None:
        missing_actuation = valid_light_plan()
        del missing_actuation["render_contract"]["light_form_contract"][
            "aggregate_effects"
        ][0]["reference_region_id"]
        self.assertTrue(
            any(
                "observed regional light relation" in error
                for error in audit_plan(missing_actuation)
            )
        )

        missing_observation = valid_light_plan()
        del missing_observation["render_contract"]["light_form_contract"][
            "region_effects"
        ][0]["reference_region_id"]
        self.assertTrue(
            any(
                "aggregate regional light relation" in error
                for error in audit_plan(missing_observation)
            )
        )

    def test_pairwise_light_reference_changes_primary_signature(self) -> None:
        baseline = valid_light_plan()
        variant = deepcopy(baseline)
        variant["render_contract"]["major_regions"].append(
            {
                "id": "comparison-field",
                "role": "supporting",
                "relative_area": "small",
                "attention": "secondary",
                "source_evidence": ["a separate held-out comparison region"],
            }
        )
        light_contract = variant["render_contract"]["light_form_contract"]
        light_contract["region_effects"][0]["reference_region_id"] = (
            "comparison-field"
        )
        light_contract["aggregate_effects"][0]["reference_region_id"] = (
            "comparison-field"
        )
        self.assertEqual(audit_plan(variant), [])
        self.assertTrue(
            any(
                "changed the primary salience signature" in error
                for error in compare_plans(
                    baseline, variant, "invariant-preserving"
                )
            )
        )

    def test_valid_axis_first_lighting_language_review_passes(self) -> None:
        self.assertEqual(
            audit_plan(add_lighting_language_review(valid_light_plan())), []
        )

    def test_controlled_lighting_summary_cannot_be_emitted(self) -> None:
        plan = add_lighting_language_review(valid_light_plan())
        summary = plan["render_contract"]["light_form_contract"][
            "lighting_language"
        ]["controlled_summary"]
        summary["emit"] = True
        self.assertTrue(
            any(
                "policy-derived explanation-only summary" in error
                for error in audit_plan(plan)
            )
        )

    def test_conflicting_friendly_lighting_label_cannot_be_emitted(self) -> None:
        plan = add_lighting_language_review(valid_light_plan(), conflicting=True)
        lighting_label = plan["render_contract"]["light_form_contract"][
            "lighting_labels"
        ][0]
        lighting_label.update(
            {
                "status": "model-calibrated",
                "emit": True,
                "generator_id": "held-out-generator",
                "generator_version": "held-out-version",
                "conditioning_route": "text-only",
                "calibration_evidence": ["held-out matched response study"],
            }
        )
        self.assertTrue(
            any(
                "requires a compatible review" in error for error in audit_plan(plan)
            )
        )

    def test_unqualified_friendly_lighting_label_cannot_be_emitted(self) -> None:
        plan = add_lighting_language_review(valid_light_plan())
        lighting_label = plan["render_contract"]["light_form_contract"][
            "lighting_labels"
        ][0]
        lighting_label["emit"] = True
        self.assertTrue(
            any(
                "must be model-calibrated or source-evidence-qualified" in error
                for error in audit_plan(plan)
            )
        )

    def test_source_visible_lighting_descriptor_may_lead_literal_controls(self) -> None:
        plan = add_lighting_language_review(
            valid_light_plan(), source_kind="source-visible-approximation"
        )
        lighting_label = plan["render_contract"]["light_form_contract"][
            "lighting_labels"
        ][0]
        lighting_label.update(
            {
                "status": "source-evidence-qualified",
                "emit": True,
                "source_evidence": ["current-source global lighting gestalt"],
                "confidence": "medium",
                "viewer_priority": "P1",
                "omission_counterfactual": "material-drift",
            }
        )
        self.assertEqual(audit_plan(plan), [])
        prompt = authored_prompt_text(plan)
        self.assertEqual(audit_plan(plan, prompt), [])
        self.assertLess(
            prompt.index("held-out candidate lighting label"),
            prompt.index("broad planes revealed only by long shallow gradients"),
        )

    def test_model_calibrated_friendly_lighting_label_may_lead_literal_controls(self) -> None:
        plan = add_lighting_language_review(valid_light_plan())
        lighting_label = plan["render_contract"]["light_form_contract"][
            "lighting_labels"
        ][0]
        lighting_label.update(
            {
                "status": "model-calibrated",
                "emit": True,
                "generator_id": "held-out-generator",
                "generator_version": "held-out-version",
                "conditioning_route": "text-only",
                "calibration_evidence": ["held-out matched response study"],
            }
        )
        self.assertEqual(audit_plan(plan), [])

    def test_lighting_language_must_match_color_tone_key_class(self) -> None:
        plan = add_lighting_language_review(
            with_displayed_key_response(valid_color_and_light_plan())
        )
        language = plan["render_contract"]["light_form_contract"][
            "lighting_language"
        ]
        language["axis_classification"]["displayed_key_level"]["term"] = "low"
        language["controlled_summary"]["phrase"] = (
            "low-key soft-edged gently-modeling light"
        )
        self.assertTrue(
            any(
                "conflicts with the Color/Tone contract" in error
                for error in audit_plan(plan)
            )
        )

    def test_at_most_one_friendly_lighting_label_may_be_emitted(self) -> None:
        plan = add_lighting_language_review(valid_light_plan())
        light_contract = plan["render_contract"]["light_form_contract"]
        calibrated = light_contract["lighting_labels"][0]
        calibrated.update(
            {
                "status": "model-calibrated",
                "emit": True,
                "generator_id": "held-out-generator",
                "generator_version": "held-out-version",
                "conditioning_route": "text-only",
                "calibration_evidence": ["held-out matched response study"],
            }
        )
        duplicate = deepcopy(calibrated)
        duplicate["phrase"] = "second held-out candidate lighting label"
        light_contract["lighting_language"]["friendly_label_review"].append(
            {
                **deepcopy(
                    light_contract["lighting_language"]["friendly_label_review"][0]
                ),
                "phrase": duplicate["phrase"],
            }
        )
        light_contract["lighting_labels"].append(duplicate)
        self.assertTrue(
            any("at most one friendly lighting label" in error for error in audit_plan(plan))
        )

    def test_light_observation_requires_separate_coverage_extent_and_spill(self) -> None:
        plan = valid_light_plan()
        observed = plan["render_contract"]["light_form_contract"]["observed_result"]
        del observed["bright_plane_coverage"]
        del observed["gradient_extent"]
        del observed["background_spill_relation"]
        errors = audit_plan(plan)
        self.assertTrue(any("bright_plane_coverage" in error for error in errors))
        self.assertTrue(any("gradient_extent" in error for error in errors))
        self.assertTrue(any("background_spill_relation" in error for error in errors))

    def test_bright_plane_coverage_is_a_separate_valid_light_owner(self) -> None:
        plan = valid_light_plan()
        light_contract = plan["render_contract"]["light_form_contract"]
        light_contract["aggregate_effects"][0]["axis"] = "bright-plane-coverage"
        light_contract["aggregate_effects"][0]["direction"] = "broad-bright-side-coverage"
        light_contract["emitted_controls"][0]["owner"] = "bright-plane-coverage"
        self.assertEqual(audit_plan(plan), [])

    def test_gradient_extent_effect_requires_an_observed_gradient_region(self) -> None:
        plan = valid_light_plan()
        light_contract = plan["render_contract"]["light_form_contract"]
        light_contract["aggregate_effects"][0]["axis"] = "gradient-extent"
        light_contract["emitted_controls"][0]["owner"] = "gradient-extent"
        self.assertTrue(
            any(
                "gradient-extent effect requires" in error
                for error in audit_plan(plan)
            )
        )

    def test_primary_light_invariant_requires_light_form_contract(self) -> None:
        plan = valid_light_plan()
        del plan["render_contract"]["light_form_contract"]
        self.assertTrue(
            any(
                "primary light-to-form invariant requires" in error
                for error in audit_plan(plan)
            )
        )

    def test_low_confidence_rig_cannot_emit_physical_cause(self) -> None:
        plan = valid_light_plan()
        hypothesis = plan["render_contract"]["light_form_contract"][
            "source_hypothesis"
        ]
        hypothesis["actuation"] = "physical-cause"
        effect = plan["render_contract"]["light_form_contract"][
            "aggregate_effects"
        ][0]
        effect["axis"] = "source-geometry"
        control = plan["render_contract"]["light_form_contract"][
            "emitted_controls"
        ][0]
        control["owner"] = "source-geometry"
        self.assertTrue(
            any(
                "low-confidence source hypothesis" in error
                for error in audit_plan(plan)
            )
        )

    def test_result_space_actuation_rejects_source_geometry(self) -> None:
        plan = valid_light_plan()
        effect = plan["render_contract"]["light_form_contract"][
            "aggregate_effects"
        ][0]
        effect["axis"] = "source-geometry"
        control = plan["render_contract"]["light_form_contract"][
            "emitted_controls"
        ][0]
        control["owner"] = "source-geometry"
        self.assertTrue(
            any(
                "result-space-only actuation cannot emit" in error
                for error in audit_plan(plan)
            )
        )

    def test_shadow_topology_requires_owned_shadow_event(self) -> None:
        plan = valid_light_plan()
        light_contract = plan["render_contract"]["light_form_contract"]
        light_contract["aggregate_effects"][0]["axis"] = "shadow-topology"
        light_contract["emitted_controls"][0]["owner"] = "shadow-topology"
        self.assertTrue(
            any(
                "requires at least one shadow event" in error
                for error in audit_plan(plan)
            )
        )

    def test_pose_robust_light_contract_names_flexible_effect(self) -> None:
        plan = valid_light_plan()
        plan["render_contract"]["light_form_contract"]["pose_light_dependency"][
            "flexible_effects"
        ] = []
        self.assertTrue(
            any(
                "pose-robust or mixed lighting" in error
                for error in audit_plan(plan)
            )
        )

    def test_lighting_control_owner_must_match_effect_axis(self) -> None:
        plan = valid_light_plan()
        plan["render_contract"]["light_form_contract"]["emitted_controls"][0][
            "owner"
        ] = "material-response"
        self.assertTrue(
            any(
                "exactly one Light/Form owner" in error
                for error in audit_plan(plan)
            )
        )

    def test_color_and_light_contracts_cannot_share_claim_or_excerpt(self) -> None:
        plan = valid_color_and_light_plan()
        contract = plan["render_contract"]
        light_contract = contract["light_form_contract"]
        light_contract["claim_ids"] = ["claim-surface-tone"]
        light_contract["emitted_controls"][0]["claim_id"] = "claim-surface-tone"
        light_contract["emitted_controls"][0]["prompt_excerpt"] = contract[
            "color_tone_contract"
        ]["emitted_controls"][0]["prompt_excerpt"]
        errors = audit_plan(plan)
        self.assertTrue(any("cannot own the same claims" in error for error in errors))
        self.assertTrue(any("cannot own the same prompt excerpts" in error for error in errors))

    def test_primary_lighting_effect_changes_pair_signature(self) -> None:
        baseline = valid_light_plan()
        variant = deepcopy(baseline)
        variant["render_contract"]["light_form_contract"]["aggregate_effects"][0][
            "direction"
        ] = "strong-internal-modeling"
        self.assertTrue(
            any(
                "changed the primary salience signature" in error
                for error in compare_plans(
                    baseline, variant, "invariant-preserving"
                )
            )
        )

    def test_color_tone_contract_requires_observation_scope(self) -> None:
        plan = valid_color_plan()
        del plan["render_contract"]["color_tone_contract"]["observation_scope"]
        self.assertTrue(
            any("observation_scope" in error for error in audit_plan(plan))
        )

    def test_color_tone_contract_requires_final_prompt_controls(self) -> None:
        plan = valid_color_plan()
        del plan["render_contract"]["color_tone_contract"]["emitted_controls"]
        self.assertTrue(
            any("emitted_controls" in error for error in audit_plan(plan))
        )

    def test_one_color_claim_cannot_have_two_final_prompt_controls(self) -> None:
        plan = valid_color_plan()
        controls = plan["render_contract"]["color_tone_contract"]["emitted_controls"]
        duplicate = deepcopy(controls[0])
        duplicate["id"] = "control-surface-tone-again"
        duplicate["prompt_excerpt"] = "the central field remains visibly lighter"
        controls.append(duplicate)
        self.assertTrue(
            any("exactly one emitted final-prompt control" in error for error in audit_plan(plan))
        )

    def test_final_prompt_control_must_match_claim_layer_and_effects(self) -> None:
        plan = valid_color_plan()
        control = plan["render_contract"]["color_tone_contract"]["emitted_controls"][0]
        control["causal_layer"] = "illumination"
        control["aggregate_effect_ids"] = ["unknown-effect"]
        errors = audit_plan(plan)
        self.assertTrue(any("unknown effects" in error for error in errors))
        self.assertTrue(any("exactly match" in error for error in errors))
        self.assertTrue(any("exactly one causal layer" in error for error in errors))

    def test_color_invariant_requires_color_tone_contract(self) -> None:
        plan = valid_color_plan()
        del plan["render_contract"]["color_tone_contract"]
        self.assertTrue(
            any(
                "color invariant requires" in error for error in audit_plan(plan)
            )
        )

    def test_primary_color_region_accounts_for_value_chroma_and_hue(self) -> None:
        plan = valid_color_plan()
        axes = plan["render_contract"]["color_tone_contract"]["regions"][0][
            "intrinsic_axes"
        ]
        axes[:] = [axis for axis in axes if axis["axis"] != "hue"]
        self.assertTrue(
            any("primary intrinsic axes" in error for error in audit_plan(plan))
        )

    def test_required_intrinsic_axis_must_link_to_an_effect(self) -> None:
        plan = valid_color_plan()
        axis = plan["render_contract"]["color_tone_contract"]["regions"][0][
            "intrinsic_axes"
        ][0]
        del axis["aggregate_effect_id"]
        self.assertTrue(
            any(
                "aggregate_effect_id is required" in error
                for error in audit_plan(plan)
            )
        )

    def test_diagnostic_only_axis_requires_reason(self) -> None:
        plan = valid_color_plan()
        axis = plan["render_contract"]["color_tone_contract"]["regions"][0][
            "intrinsic_axes"
        ][1]
        del axis["non_emission_reason"]
        self.assertTrue(
            any("non_emission_reason" in error for error in audit_plan(plan))
        )

    def test_mixed_tone_zone_cannot_drive_intrinsic_axis(self) -> None:
        plan = valid_color_plan()
        axis = plan["render_contract"]["color_tone_contract"]["regions"][0][
            "intrinsic_axes"
        ][0]
        axis["evidence_scope"] = "mixed"
        self.assertTrue(
            any("mixed tone-zone evidence" in error for error in audit_plan(plan))
        )

    def test_required_intrinsic_axis_needs_intrinsic_axis_control(self) -> None:
        plan = valid_color_plan()
        contract = plan["render_contract"]
        claim = contract["candidate_claims"][-1]
        claim["perceptual_effects"][0]["causal_layer"] = "hierarchy"
        control = contract["color_tone_contract"]["emitted_controls"][0]
        control["causal_layer"] = "hierarchy"
        self.assertTrue(
            any(
                "required intrinsic axis needs its own intrinsic axis-control" in error
                for error in audit_plan(plan)
            )
        )

    def test_axis_control_cannot_cover_multiple_axes(self) -> None:
        plan = valid_color_plan()
        contract = plan["render_contract"]
        claim = contract["candidate_claims"][-1]
        claim["perceptual_effects"].append(
            {
                "aggregate_effect_id": "central-chroma-relation",
                "causal_layer": "intrinsic",
                "confidence": "medium",
                "source_evidence": ["the central field remains restrained"],
            }
        )
        color_contract = contract["color_tone_contract"]
        color_contract["aggregate_effects"].append(
            {
                "id": "central-chroma-relation",
                "region_id": "central-form",
                "axis": "chroma",
                "direction": "restrained-chroma",
                "role": "supporting",
                "target_strength": "subtle",
                "claim_ids": ["claim-surface-tone"],
                "source_supported": True,
                "source_evidence": ["small channel separation"],
            }
        )
        color_contract["emitted_controls"][0]["aggregate_effect_ids"].append(
            "central-chroma-relation"
        )
        self.assertTrue(
            any(
                "axis-control may reference only one matching region and axis" in error
                for error in audit_plan(plan)
            )
        )

    def test_unverified_appearance_metaphor_cannot_emit(self) -> None:
        plan = valid_color_plan()
        plan["render_contract"]["color_tone_contract"]["appearance_metaphors"] = [
            {
                "phrase": "material-like color shorthand",
                "status": "unverified",
                "emit": True,
                "decomposed_control_ids": ["control-surface-tone"],
            }
        ]
        self.assertTrue(
            any(
                "must be model-calibrated or source-evidence-qualified" in error
                for error in audit_plan(plan)
            )
        )

    def test_invalid_appearance_metaphor_phrase_reports_instead_of_crashing(self) -> None:
        plan = valid_color_plan()
        plan["render_contract"]["color_tone_contract"]["appearance_metaphors"] = [
            {
                "phrase": 7,
                "status": "model-calibrated",
                "emit": True,
                "calibration_evidence": ["matched response study"],
                "decomposed_control_ids": ["control-surface-tone"],
            }
        ]
        self.assertTrue(
            any("phrase must be non-empty" in error for error in audit_plan(plan))
        )

    def test_same_color_effect_cannot_repeat_one_causal_layer(self) -> None:
        plan = valid_color_plan()
        contract = plan["render_contract"]
        duplicate = deepcopy(contract["candidate_claims"][-1])
        duplicate["id"] = "claim-surface-tone-again"
        duplicate["semantic_slot"] = "surface-tone-support"
        duplicate["role"] = "supporting"
        contract["candidate_claims"].append(duplicate)
        color_contract = contract["color_tone_contract"]
        color_contract["claim_ids"].append(duplicate["id"])
        color_contract["aggregate_effects"][0]["claim_ids"].append(duplicate["id"])
        self.assertTrue(
            any("repeats one causal layer" in error for error in audit_plan(plan))
        )

    def test_same_color_direction_cannot_hide_behind_two_effect_ids(self) -> None:
        plan = valid_color_plan()
        contract = plan["render_contract"]
        duplicate_claim = deepcopy(contract["candidate_claims"][-1])
        duplicate_claim["id"] = "claim-surface-tone-split"
        duplicate_claim["semantic_slot"] = "surface-tone-split"
        duplicate_claim["role"] = "supporting"
        duplicate_claim["perceptual_effects"][0][
            "aggregate_effect_id"
        ] = "central-value-relation-split"
        contract["candidate_claims"].append(duplicate_claim)

        color_contract = contract["color_tone_contract"]
        color_contract["claim_ids"].append(duplicate_claim["id"])
        duplicate_effect = deepcopy(color_contract["aggregate_effects"][0])
        duplicate_effect["id"] = "central-value-relation-split"
        duplicate_effect["claim_ids"] = [duplicate_claim["id"]]
        color_contract["aggregate_effects"].append(duplicate_effect)

        self.assertTrue(
            any(
                "split one region/axis/direction" in error
                for error in audit_plan(plan)
            )
        )

    def test_cross_layer_color_effect_requires_source_supported_aggregate(self) -> None:
        plan = valid_color_plan()
        contract = plan["render_contract"]
        illumination = deepcopy(contract["candidate_claims"][-1])
        illumination["id"] = "claim-light-shift"
        illumination["semantic_slot"] = "light-shift"
        illumination["owner"] = "medium.photographic-capture"
        illumination["role"] = "supporting"
        illumination["perceptual_effects"][0]["causal_layer"] = "illumination"
        contract["candidate_claims"].append(illumination)
        color_contract = contract["color_tone_contract"]
        color_contract["claim_ids"].append(illumination["id"])
        aggregate = color_contract["aggregate_effects"][0]
        aggregate["claim_ids"].append(illumination["id"])
        aggregate["source_supported"] = False
        self.assertTrue(
            any("spans causal layers" in error for error in audit_plan(plan))
        )

    def test_source_supported_cross_layer_color_effect_is_allowed(self) -> None:
        plan = valid_color_plan()
        contract = plan["render_contract"]
        illumination = deepcopy(contract["candidate_claims"][-1])
        illumination["id"] = "claim-supported-light-shift"
        illumination["semantic_slot"] = "supported-light-shift"
        illumination["owner"] = "medium.photographic-capture"
        illumination["role"] = "supporting"
        illumination["perceptual_effects"][0]["causal_layer"] = "illumination"
        illumination["perceptual_effects"][0]["source_evidence"] = [
            "the same directional shift appears in highlights across materials"
        ]
        contract["candidate_claims"].append(illumination)
        color_contract = contract["color_tone_contract"]
        color_contract["claim_ids"].append(illumination["id"])
        color_contract["emitted_controls"].append(
            {
                "id": "control-supported-light-shift",
                "prompt_excerpt": "a warm illumination shift across both materials",
                "claim_id": illumination["id"],
                "causal_layer": "illumination",
                "control_role": "axis-control",
                "region_id": "central-form",
                "axis": "value",
                "aggregate_effect_ids": ["central-value-relation"],
            }
        )
        aggregate = color_contract["aggregate_effects"][0]
        aggregate["claim_ids"].append(illumination["id"])
        aggregate["source_evidence"].append(
            "intrinsic relation and illumination shift are independently visible"
        )
        self.assertEqual(audit_plan(plan), [])

    def test_hierarchy_hue_requires_named_hue_contrast_invariant(self) -> None:
        plan = valid_color_plan()
        contract = plan["render_contract"]
        aggregate = contract["color_tone_contract"]["aggregate_effects"][0]
        aggregate["axis"] = "hue"
        effect = contract["candidate_claims"][-1]["perceptual_effects"][0]
        effect["causal_layer"] = "hierarchy"
        self.assertTrue(
            any("hierarchy may carry hue" in error for error in audit_plan(plan))
        )

    def test_high_confidence_global_cast_needs_more_than_unavailable_neutral(self) -> None:
        plan = valid_color_plan()
        contract = plan["render_contract"]
        color_contract = contract["color_tone_contract"]
        color_contract["neutral_anchor_status"] = "unavailable"
        color_contract["uncertainty_note"] = "no reliable neutral region is visible"
        color_contract["neutral_anchors"] = []
        effect = contract["candidate_claims"][-1]["perceptual_effects"][0]
        effect["causal_layer"] = "global-cast"
        effect["confidence"] = "high"
        self.assertTrue(
            any(
                "high-confidence global cast" in error for error in audit_plan(plan)
            )
        )

    def test_color_effect_changes_primary_signature(self) -> None:
        baseline = valid_color_plan()
        variant = deepcopy(baseline)
        variant["render_contract"]["color_tone_contract"]["aggregate_effects"][0][
            "direction"
        ] = "darker-than-surrounding-field"
        self.assertTrue(
            any(
                "changed the primary salience signature" in error
                for error in compare_plans(
                    baseline, variant, "invariant-preserving"
                )
            )
        )

    def test_layout_dense_plan_is_not_forced_into_four_invariants(self) -> None:
        plan = valid_plan()
        contract = plan["render_contract"]
        contract["mode"] = "information-led"
        for index in range(3):
            invariant_id = f"information-band-{index}"
            add_generic_claim(
                contract,
                invariant_id=invariant_id,
                axis="information",
                owner="subject.document-data-diagram",
                role="supporting",
                target_strength="subtle",
                observation=f"distinct reading-order band {index}",
                causal_origin="layout",
                evidence=f"separate visible container {index}",
                direction=f"separate-reading-order-band-{index}",
                prompt_excerpt=f"a distinct reading-order band {index}",
            )
        self.assertEqual(audit_plan(plan), [])

    def test_duplicate_affirmative_slot_fails(self) -> None:
        plan = valid_plan()
        duplicate = deepcopy(plan["render_contract"]["candidate_claims"][0])
        duplicate["id"] = "claim-form-again"
        duplicate["owner"] = "medium.photographic-capture"
        plan["render_contract"]["candidate_claims"].append(duplicate)
        self.assertTrue(
            any(
                "multiple emitted affirmative owners" in error
                for error in audit_plan(plan)
            )
        )

    def test_diagnostic_appeal_cannot_be_emitted(self) -> None:
        plan = valid_plan()
        plan["render_contract"]["candidate_claims"][0]["source_kind"] = (
            "diagnostic-appeal"
        )
        self.assertTrue(
            any(
                "diagnostic appeal cannot be emitted" in error
                for error in audit_plan(plan)
            )
        )

    def test_flexible_dimension_cannot_be_promoted(self) -> None:
        plan = valid_plan()
        plan["render_contract"]["candidate_claims"][2]["role"] = "primary"
        self.assertTrue(
            any("flexible dimension" in error for error in audit_plan(plan))
        )

    def test_unsupported_prior_cluster_cannot_emit(self) -> None:
        plan = valid_plan()
        plan["render_contract"]["prior_clusters"][0]["source_supported"] = False
        self.assertTrue(
            any("unsupported prior cluster" in error for error in audit_plan(plan))
        )

    def test_source_visible_aesthetic_shorthand_retains_qualified_summary_and_decomposition(self) -> None:
        plan = valid_plan()
        contract = plan["render_contract"]
        add_generic_claim(
            contract,
            invariant_id="aesthetic-summary",
            axis="hierarchy",
            owner="medium.photographic-capture",
            role="supporting",
            target_strength="subtle",
            observation="one broad source-visible production aesthetic summary",
            causal_origin="processing",
            evidence="held-out softness and restrained contrast",
            direction="held-out-production-aesthetic-summary",
            prompt_excerpt="held-out broad aesthetic shorthand",
            region_ids=["central-form", "surrounding-field"],
        )
        contract["prior_clusters"] = [
            {
                "id": "aesthetic-cluster",
                "schema_version": "prior-cluster/v2",
                "scope": "aesthetic",
                "disposition": "emit",
                "claim_ids": ["claim-aesthetic-summary", "claim-balance"],
                "source_supported": True,
                "candidate_source": {
                    "kind": "source-visible-approximation",
                    "reference": "held-out source observation",
                },
                "source_evidence": ["held-out softness and restrained contrast"],
                "confidence": "high",
                "viewer_priority": "P0",
                "omission_counterfactual": "material-drift",
                "calibration_status": "unverified",
                "summary_control_id": "control-aesthetic-summary",
                "decomposed_claim_ids": ["claim-balance"],
                "decomposed_control_ids": ["control-balance"],
            }
        ]
        self.assertEqual(audit_plan(plan), [])
        prompt = authored_prompt_text(plan)
        self.assertEqual(audit_plan(plan, prompt), [])
        self.assertLess(
            prompt.index("held-out broad aesthetic shorthand"),
            prompt.index("the form remains smaller than the surrounding field"),
        )

        unqualified = deepcopy(plan)
        cluster = unqualified["render_contract"]["prior_clusters"][0]
        cluster["confidence"] = "low"
        cluster["viewer_priority"] = "P2"
        cluster["omission_counterfactual"] = "preserved"
        errors = audit_plan(unqualified)
        self.assertTrue(any("confidence must be high or medium" in error for error in errors))
        self.assertTrue(any("viewer_priority must be P0 or P1" in error for error in errors))
        self.assertTrue(any("must be material-drift" in error for error in errors))

        calibrated = deepcopy(plan)
        cluster = calibrated["render_contract"]["prior_clusters"][0]
        cluster.update(
            {
                "calibration_status": "model-calibrated",
                "generator_id": "held-out-generator",
                "generator_version": "held-out-version",
                "calibration_evidence": ["independent held-out generator comparison"],
            }
        )
        self.assertEqual(audit_plan(calibrated), [])

    def test_invariant_preserving_pair_allows_flexible_change(self) -> None:
        baseline = valid_plan()
        variant = deepcopy(baseline)
        variant["render_contract"]["candidate_claims"][2]["source_evidence"] = [
            "small offset toward the opposite side"
        ]
        self.assertEqual(compare_plans(baseline, variant, "invariant-preserving"), [])

    def test_invariant_preserving_pair_rejects_strength_change(self) -> None:
        baseline = valid_plan()
        variant = deepcopy(baseline)
        variant["render_contract"]["invariants"][0]["target_strength"] = "strong"
        variant["render_contract"]["candidate_claims"][0]["target_strength"] = "strong"
        variant["render_contract"]["aggregate_effects"][0]["target_strength"] = (
            "strong"
        )
        self.assertTrue(
            any(
                "changed the primary salience signature" in error
                for error in compare_plans(baseline, variant, "invariant-preserving")
            )
        )

    def test_aesthetic_changing_pair_requires_primary_change(self) -> None:
        baseline = valid_plan()
        self.assertTrue(
            any(
                "retained an identical" in error
                for error in compare_plans(
                    baseline, deepcopy(baseline), "aesthetic-changing"
                )
            )
        )


if __name__ == "__main__":
    unittest.main()
