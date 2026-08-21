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
            "observation": "the central field stays lighter and lower-chroma than the surround",
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
                        "observation": "lighter than the surrounding field",
                        "confidence": "high",
                        "source_evidence": ["broad value separation at the boundary"],
                    },
                    {
                        "axis": "chroma",
                        "observation": "restrained rather than vivid",
                        "confidence": "medium",
                        "source_evidence": ["small channel separation across midtones"],
                    },
                    {
                        "axis": "hue",
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
