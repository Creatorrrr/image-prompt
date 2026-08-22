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

from salience_plan import audit_plan, compare_plans  # noqa: E402


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
            "prompt_excerpt": "a high displayed key while preserving highlight detail",
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


class SaliencePlanTests(unittest.TestCase):
    def test_valid_source_relative_plan_passes(self) -> None:
        self.assertEqual(audit_plan(valid_plan()), [])

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
            contract["invariants"].append(
                {
                    "id": invariant_id,
                    "axis": "information",
                    "role": "supporting",
                    "observation": f"distinct reading-order band {index}",
                    "causal_origin": "layout",
                    "target_strength": "subtle",
                    "source_evidence": [f"separate visible container {index}"],
                    "clause_owner": "subject.document-data-diagram",
                }
            )
            contract["candidate_claims"].append(
                {
                    "id": f"claim-information-{index}",
                    "semantic_slot": invariant_id,
                    "owner": "subject.document-data-diagram",
                    "role": "supporting",
                    "polarity": "affirmative",
                    "target_strength": "subtle",
                    "source_kind": "visible-evidence",
                    "source_evidence": [f"separate visible container {index}"],
                    "emit": True,
                }
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
