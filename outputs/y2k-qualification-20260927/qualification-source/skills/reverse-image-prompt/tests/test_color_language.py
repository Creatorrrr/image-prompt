#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

from color_language import (  # noqa: E402
    classify_observation,
    compose_controlled_descriptor,
    review_candidates,
)


POLICY = json.loads(
    (Path(__file__).resolve().parents[1] / "references" / "surface-color-language-policy.json").read_text(encoding="utf-8")
)


def observation(l_value: float, a_value: float, b_value: float) -> dict:
    return {
        "observation_scope": "source-visible",
        "profile_status": "embedded-profile-converted-to-srgb",
        "region_id": "selected-surface",
        "lab_d65": [l_value, a_value, b_value],
        "dispersion": {"lightness_range": 3.0, "chroma_range": 2.0},
        "surface_evidence": {
            "finish": {
                "term": "satin",
                "confidence": "medium",
                "source_evidence": ["broad soft reflection"],
            },
            "evenness": {
                "term": "even",
                "confidence": "medium",
                "source_evidence": ["small variation across selected patches"],
            },
        },
    }


def candidate_payload(candidates: list[dict], *, kind: str = "user-supplied") -> dict:
    return {
        "candidate_source": {
            "kind": kind,
            "reference": "held-out test input",
        },
        "candidates": candidates,
    }


class ColorLanguageTests(unittest.TestCase):
    def test_controlled_descriptor_composes_current_axes_in_fixed_order(self) -> None:
        classification = classify_observation(observation(70.0, 7.0, 10.0), POLICY)
        descriptor = compose_controlled_descriptor(classification, "visible skin")
        self.assertEqual(descriptor["status"], "complete")
        self.assertEqual(
            descriptor["phrase"],
            "visible skin with a light value, low chroma, a golden undertone, and a satin finish",
        )
        self.assertEqual(
            descriptor["included_axes"],
            ["value_depth", "chroma", "undertone", "finish"],
        )
        self.assertNotIn("emit", descriptor)

    def test_controlled_descriptor_changes_with_held_out_axis_values(self) -> None:
        light = compose_controlled_descriptor(
            classify_observation(observation(70.0, 7.0, 10.0), POLICY),
            "selected surface",
            include_finish=False,
        )
        deep = compose_controlled_descriptor(
            classify_observation(observation(34.0, 1.0, 18.0), POLICY),
            "selected surface",
            include_finish=False,
        )
        self.assertNotEqual(light["phrase"], deep["phrase"])
        self.assertIn("a deep value", deep["phrase"])
        self.assertIn("an olive undertone", deep["phrase"])

    def test_controlled_descriptor_emits_stable_axes_when_one_axis_is_unresolved(self) -> None:
        classification = classify_observation(observation(70.0, 7.0, 10.0), POLICY)
        classification["axis_classification"]["undertone"]["confidence"] = "low"
        descriptor = compose_controlled_descriptor(
            classification, "selected surface", include_finish=False
        )
        self.assertEqual(descriptor["status"], "partial")
        self.assertEqual(
            descriptor["phrase"],
            "selected surface with a light value and low chroma",
        )
        self.assertEqual(descriptor["included_axes"], ["value_depth", "chroma"])
        self.assertEqual(descriptor["unresolved_axes"], ["undertone"])

    def test_boundary_only_axes_remain_non_emitted(self) -> None:
        classification = classify_observation(observation(70.0, 7.0, 10.0), POLICY)
        for axis in ("value_depth", "chroma", "undertone"):
            classification["axis_classification"][axis].update(
                {"confidence": "medium", "runner_up": "adjacent-held-out-class"}
            )
        descriptor = compose_controlled_descriptor(
            classification, "selected surface", include_finish=False
        )
        self.assertEqual(descriptor["status"], "bounded")
        self.assertEqual(descriptor["included_axes"], [])
        self.assertNotIn("phrase", descriptor)
        self.assertEqual(
            set(descriptor["bounded_axes"]),
            {"value_depth", "chroma", "undertone"},
        )

    def test_neutral_undertone_boundary_is_bounded_not_emitted(self) -> None:
        classification = classify_observation(observation(70.0, 5.0, 0.0), POLICY)
        undertone = classification["axis_classification"]["undertone"]
        self.assertEqual(undertone["term"], "neutral")
        self.assertEqual(undertone["confidence"], "medium")
        self.assertIsInstance(undertone["runner_up"], str)

        descriptor = compose_controlled_descriptor(
            classification, "selected surface", include_finish=False
        )
        self.assertNotIn("undertone", descriptor["included_axes"])
        self.assertEqual(
            descriptor["bounded_axes"]["undertone"]["term"], "neutral"
        )
        self.assertNotIn("a neutral undertone", descriptor.get("phrase", ""))

    def test_no_stable_or_bounded_axis_is_inconclusive(self) -> None:
        classification = classify_observation(observation(70.0, 7.0, 10.0), POLICY)
        for axis in ("value_depth", "chroma", "undertone"):
            classification["axis_classification"][axis]["confidence"] = "low"
        descriptor = compose_controlled_descriptor(
            classification, "selected surface", include_finish=False
        )
        self.assertEqual(descriptor["status"], "inconclusive")
        self.assertNotIn("phrase", descriptor)

    def test_controlled_descriptor_requires_analyst_supplied_surface_term(self) -> None:
        classification = classify_observation(observation(70.0, 7.0, 10.0), POLICY)
        with self.assertRaisesRegex(ValueError, "surface_term"):
            compose_controlled_descriptor(classification, "  ")

    def test_same_undertone_survives_value_depth_change(self) -> None:
        light = classify_observation(observation(78.0, 7.0, 12.0), POLICY)
        medium = classify_observation(observation(50.0, 7.0, 12.0), POLICY)
        self.assertNotEqual(
            light["axis_classification"]["value_depth"]["term"],
            medium["axis_classification"]["value_depth"]["term"],
        )
        self.assertEqual(
            light["axis_classification"]["undertone"]["term"],
            medium["axis_classification"]["undertone"]["term"],
        )

    def test_olive_is_undertone_not_depth(self) -> None:
        very_light = classify_observation(observation(82.0, 1.0, 18.0), POLICY)
        deep = classify_observation(observation(34.0, 1.0, 18.0), POLICY)
        self.assertEqual(very_light["axis_classification"]["undertone"]["term"], "olive")
        self.assertEqual(deep["axis_classification"]["undertone"]["term"], "olive")
        self.assertNotEqual(
            very_light["axis_classification"]["value_depth"]["term"],
            deep["axis_classification"]["value_depth"]["term"],
        )

    def test_boundary_and_missing_profile_reduce_confidence(self) -> None:
        payload = observation(75.2, 8.0, 10.0)
        payload["profile_status"] = "missing-profile-assumed-srgb"
        result = classify_observation(payload, POLICY)
        self.assertIn(result["axis_classification"]["value_depth"]["confidence"], {"medium", "low"})

    def test_candidate_review_does_not_force_incompatible_label(self) -> None:
        classification = classify_observation(observation(50.0, 1.0, 18.0), POLICY)
        reviewed = review_candidates(
            classification,
            candidate_payload(
                [
                    {
                        "phrase": "candidate label",
                        "label_scope": "composite-appearance",
                        "axis_requirements": {
                            "value_depth": ["very-light"],
                            "chroma": ["low", "moderate"],
                            "undertone": ["neutral", "peach"],
                            "finish": ["satin"],
                        },
                    }
                ]
            ),
        )
        self.assertEqual(reviewed[0]["review_status"], "conflicting")
        self.assertIn("value_depth", reviewed[0]["conflicting_axes"])
        self.assertIn("undertone", reviewed[0]["conflicting_axes"])

    def test_unobserved_finish_keeps_composite_label_inconclusive(self) -> None:
        payload = observation(82.0, 7.0, 10.0)
        payload["surface_evidence"] = {}
        classification = classify_observation(payload, POLICY)
        reviewed = review_candidates(
            classification,
            candidate_payload(
                [
                    {
                        "phrase": "candidate label",
                        "label_scope": "composite-appearance",
                        "axis_requirements": {
                            "value_depth": ["very-light"],
                            "chroma": ["low", "moderate"],
                            "undertone": ["peach", "golden"],
                            "finish": ["matte", "satin"],
                        },
                    }
                ]
            ),
        )
        self.assertEqual(reviewed[0]["review_status"], "inconclusive")
        self.assertIn("finish", reviewed[0]["unresolved_axes"])

    def test_composite_candidate_must_declare_all_core_axes(self) -> None:
        classification = classify_observation(observation(70.0, 7.0, 10.0), POLICY)
        with self.assertRaisesRegex(ValueError, "does not support its label scope"):
            review_candidates(
                classification,
                candidate_payload(
                    [
                        {
                            "phrase": "incomplete candidate",
                            "label_scope": "composite-appearance",
                            "axis_requirements": {"finish": ["satin"]},
                        }
                    ]
                ),
            )

    def test_candidate_source_is_required(self) -> None:
        classification = classify_observation(observation(70.0, 7.0, 10.0), POLICY)
        with self.assertRaisesRegex(ValueError, "candidate_source must be an object"):
            review_candidates(classification, {"candidates": []})

    def test_versioned_vocabulary_source_is_preserved(self) -> None:
        classification = classify_observation(observation(70.0, 7.0, 10.0), POLICY)
        reviewed = review_candidates(
            classification,
            candidate_payload(
                [
                    {
                        "phrase": "held-out vocabulary label",
                        "label_scope": "undertone",
                        "axis_requirements": {"undertone": ["peach", "golden"]},
                    }
                ],
                kind="versioned-vocabulary",
            ),
        )
        self.assertEqual(
            reviewed[0]["candidate_source"],
            {"kind": "versioned-vocabulary", "reference": "held-out test input"},
        )

    def test_current_source_candidate_provenance_is_preserved(self) -> None:
        for l_value, a_value, b_value, expected_depth in (
            (70.0, 7.0, 10.0, "light"),
            (34.0, 1.0, 18.0, "deep"),
        ):
            with self.subTest(expected_depth=expected_depth):
                classification = classify_observation(
                    observation(l_value, a_value, b_value), POLICY
                )
                reviewed = review_candidates(
                    classification,
                    candidate_payload(
                        [
                            {
                                "phrase": "held-out source-visible surface reading",
                                "label_scope": "value-depth",
                                "axis_requirements": {
                                    "value_depth": [expected_depth]
                                },
                            }
                        ],
                        kind="source-visible-approximation",
                    ),
                )
                self.assertEqual(reviewed[0]["review_status"], "compatible")
                self.assertEqual(
                    reviewed[0]["candidate_source"],
                    {
                        "kind": "source-visible-approximation",
                        "reference": "held-out test input",
                    },
                )

    def test_classification_does_not_invent_a_friendly_label(self) -> None:
        classification = classify_observation(observation(70.0, 7.0, 10.0), POLICY)
        self.assertNotIn("friendly_label_review", classification)


if __name__ == "__main__":
    unittest.main()
