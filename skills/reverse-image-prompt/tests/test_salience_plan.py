#!/usr/bin/env python3

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import re
import sys
import unittest

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

from salience_plan import (  # noqa: E402
    BASE_SPATIAL_DIMENSIONS,
    HUMAN_SPATIAL_DIMENSIONS,
    SPATIAL_COVERAGE_SCHEMA_VERSION,
    SPATIAL_DIMENSION_FAMILIES,
    audit_plan,
    compare_plans,
)
from color_language import compose_controlled_descriptor  # noqa: E402


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
                    "prompt_excerpt": "a small source-supported offset from the frame center",
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
    surface_language = color_contract.get("surface_color_language", {})
    descriptor = surface_language.get("controlled_descriptor", {})
    composed_control_ids = (
        set(descriptor.get("axis_control_ids", {}).values())
        if descriptor.get("emit") is True
        else set()
    )
    excerpts = [
        item["prompt_excerpt"]
        for item in contract.get("emitted_controls", [])
        if item.get("id") not in composed_control_ids
    ]
    for specialized in ("color_tone_contract", "light_form_contract"):
        excerpts.extend(
            item["prompt_excerpt"]
            for item in contract.get(specialized, {}).get("emitted_controls", [])
            if item.get("id") not in composed_control_ids
        )
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
        "neutralization_checks": (
            [
                {
                    "subject_id": "subject-a",
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
                    "source_evidence": [
                        "held-out comparison against neutral axial alignment"
                    ],
                }
            ]
            if kind == "human"
            else []
        ),
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
                "counterfactual_preservation_reason": (
                    "varying this axis preserves the held-out visible relations"
                ),
            }
            for dimension in sorted(dimensions)
        ],
    }
    if kind == "human":
        contract["human_appearance_decisions"] = [
            {
                "id": "appearance-subject-a",
                "schema_version": "human-appearance/v2",
                "subject_id": "subject-a",
                "face_visibility": visibility,
                "frame_prominence": "secondary",
                "fidelity_salience": "not-material",
                "appearance_invariant_ids": [],
                "source_evidence": ["held-out source-visible human appearance"],
                "identity_context": {"disposition": "absent"},
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
                "skin_surface": {
                    "disposition": "not-material",
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
    """Give one coverage decision a complete source-relative actuation path."""

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
        prompt_excerpt=prompt_excerpt or f"preserve {direction}",
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
    decision.pop("counterfactual_preservation_reason", None)
    decision.pop("visibility_limit", None)
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
        prompt_excerpt="source-relative face silhouette and feature relations",
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
        }
    )
    return plan


def add_surface_language_review(plan: dict, *, conflicting: bool = False) -> dict:
    review = {
        "phrase": "analyst candidate label",
        "candidate_source": {
            "kind": "user-supplied",
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
    skin = plan["render_contract"]["human_appearance_decisions"][0]["skin_surface"]
    skin.update(
        {
            "disposition": "material",
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


def add_lighting_language_review(plan: dict, *, conflicting: bool = False) -> dict:
    review = {
        "phrase": "held-out candidate lighting label",
        "candidate_source": {
            "kind": "user-supplied",
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
                "schema_version" in error and "spatial-orientation/v2" in error
                for error in audit_plan(plan)
            )
        )

    def test_legacy_coarse_human_pose_dimension_cannot_satisfy_v2(self) -> None:
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

    def test_nonmaterial_pose_needs_counterfactual_preservation_reason(self) -> None:
        plan = with_spatial_coverage(valid_plan())
        decision = next(
            item
            for item in plan["render_contract"]["spatial_orientation_coverage"][
                "decisions"
            ]
            if item["dimension"] == "human-torso-yaw"
        )
        del decision["counterfactual_preservation_reason"]
        self.assertTrue(
            any(
                "counterfactual_preservation_reason" in error
                for error in audit_plan(plan)
            )
        )

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
        decision.pop("counterfactual_preservation_reason", None)
        self.assertTrue(
            any("visibility_limit" in error for error in audit_plan(plan))
        )

    def test_material_neutralization_requires_an_invariant_human_pose_axis(self) -> None:
        plan = with_spatial_coverage(valid_plan())
        check = plan["render_contract"]["spatial_orientation_coverage"][
            "neutralization_checks"
        ][0]
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
                "material neutralization requires at least one invariant human pose axis"
                in error
                for error in audit_plan(plan)
            )
        )

        promote_spatial_decision(
            plan,
            "human-head-body-yaw",
            direction="source-visible head-to-body yaw relation",
        )
        self.assertEqual(audit_plan(plan), [])

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
        head.pop("counterfactual_preservation_reason", None)
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
            "principal axis coincides with the source frame centerline",
            "principal axis remains offset toward source side A",
            "principal axis remains offset toward source side B",
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
            ("the head turns toward source side A relative to the torso", "material"),
            ("the head turns toward source side B relative to the torso", "material"),
            ("the head and torso remain source-frontally aligned", "not-material"),
        ):
            plan = with_spatial_coverage(valid_plan())
            check = plan["render_contract"]["spatial_orientation_coverage"][
                "neutralization_checks"
            ][0]
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
                "person prior and skin-surface handling cannot be silently omitted"
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
            prompt_excerpt="one source-relative non-identifying person gestalt",
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
            "source_reference": "verified casting metadata record 42",
        }
        self.assertEqual(audit_plan(trusted), [])

        missing_provenance = with_spatial_coverage(valid_plan())
        missing_provenance["render_contract"]["human_appearance_decisions"][0][
            "identity_context"
        ] = {"disposition": "trusted-metadata"}
        self.assertTrue(
            any(
                "source_reference is required for external identity context" in error
                for error in audit_plan(missing_provenance)
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

    def test_person_gestalt_generation_prior_requires_provenance_and_geometry(self) -> None:
        plan = valid_plan()
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
        self.assertEqual(audit_plan(plan), [])

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
        plan = valid_plan()
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

    def test_surface_language_review_requires_external_candidate_source(self) -> None:
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

    def test_uncalibrated_friendly_lighting_label_cannot_be_emitted(self) -> None:
        plan = add_lighting_language_review(valid_light_plan())
        lighting_label = plan["render_contract"]["light_form_contract"][
            "lighting_labels"
        ][0]
        lighting_label["emit"] = True
        self.assertTrue(
            any(
                "only a model-calibrated lighting label" in error
                for error in audit_plan(plan)
            )
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
                "only a model-calibrated appearance metaphor" in error
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
                "prompt_excerpt": "a matching source-visible illumination shift",
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

    def test_source_visible_aesthetic_shorthand_requires_calibrated_decomposition(self) -> None:
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
                "calibration_status": "unverified",
                "summary_control_id": "control-aesthetic-summary",
                "decomposed_claim_ids": ["claim-balance"],
                "decomposed_control_ids": ["control-balance"],
            }
        ]
        self.assertTrue(
            any("requires model calibration" in error for error in audit_plan(plan))
        )

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
