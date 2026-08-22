#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

from color_language import classify_observation, review_candidates  # noqa: E402


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


class ColorLanguageTests(unittest.TestCase):
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
            {
                "candidates": [
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
            },
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
            {
                "candidates": [
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
            },
        )
        self.assertEqual(reviewed[0]["review_status"], "inconclusive")
        self.assertIn("finish", reviewed[0]["unresolved_axes"])

    def test_composite_candidate_must_declare_all_core_axes(self) -> None:
        classification = classify_observation(observation(70.0, 7.0, 10.0), POLICY)
        with self.assertRaisesRegex(ValueError, "does not support its label scope"):
            review_candidates(
                classification,
                {
                    "candidates": [
                        {
                            "phrase": "incomplete candidate",
                            "label_scope": "composite-appearance",
                            "axis_requirements": {"finish": ["satin"]},
                        }
                    ]
                },
            )


if __name__ == "__main__":
    unittest.main()
