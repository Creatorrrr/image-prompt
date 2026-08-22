#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

from lighting_language import classify_observation, review_candidates  # noqa: E402


POLICY = json.loads(
    (
        Path(__file__).resolve().parents[1]
        / "references"
        / "lighting-language-policy.json"
    ).read_text(encoding="utf-8")
)


def axis(term: str, confidence: str = "high") -> dict:
    return {
        "term": term,
        "confidence": confidence,
        "source_evidence": [] if term in {"mixed", "uncertain"} else ["held-out visible evidence"],
    }


def observation(**overrides: tuple[str, str]) -> dict:
    terms = {
        "displayed_key_level": ("high", "high"),
        "shadow_floor": ("deep", "medium"),
        "edge_softness": ("soft", "high"),
        "local_form_contrast": ("strong", "high"),
        "bright_plane_coverage": ("broad", "high"),
        "gradient_extent": ("long", "high"),
        "directionality": ("side-biased", "medium"),
        "fill_structure": ("low", "medium"),
    }
    terms.update(overrides)
    return {
        "observation_scope": "source-visible",
        "region_id": "dominant-lit-form",
        "source_evidence": ["largest bright and dark masses were compared"],
        "axis_classification": {
            name: axis(term, confidence) for name, (term, confidence) in terms.items()
        },
    }


def candidate_payload(candidates: list[dict], *, kind: str = "user-supplied") -> dict:
    return {
        "candidate_source": {"kind": kind, "reference": "held-out test input"},
        "candidates": candidates,
    }


class LightingLanguageTests(unittest.TestCase):
    def test_controlled_summary_combines_independent_core_axes(self) -> None:
        result = classify_observation(observation(), POLICY)
        summary = result["controlled_summary"]
        self.assertEqual(summary["phrase"], "high-key soft-edged sculpting light")
        self.assertEqual(summary["status"], "explanation-only")
        self.assertFalse(summary["emit"])
        self.assertEqual(
            summary["decomposed_axes"],
            ["displayed_key_level", "edge_softness", "local_form_contrast"],
        )

    def test_softness_does_not_determine_modeling_strength(self) -> None:
        strong = classify_observation(observation(), POLICY)
        flat = classify_observation(
            observation(local_form_contrast=("flattening", "high")), POLICY
        )
        self.assertIn("soft-edged sculpting", strong["controlled_summary"]["phrase"])
        self.assertIn("soft-edged flat", flat["controlled_summary"]["phrase"])

    def test_unresolved_core_axis_withholds_controlled_summary(self) -> None:
        result = classify_observation(
            observation(edge_softness=("uncertain", "low")), POLICY
        )
        summary = result["controlled_summary"]
        self.assertIsNone(summary["phrase"])
        self.assertEqual(summary["status"], "inconclusive")
        self.assertIn("edge_softness", summary["unresolved_axes"])

    def test_composite_candidate_requires_core_axes(self) -> None:
        classification = classify_observation(observation(), POLICY)
        with self.assertRaisesRegex(ValueError, "does not support its label scope"):
            review_candidates(
                classification,
                candidate_payload(
                    [
                        {
                            "phrase": "incomplete lighting label",
                            "label_scope": "composite-lighting",
                            "axis_requirements": {"edge_softness": ["soft"]},
                        }
                    ]
                ),
                POLICY,
            )

    def test_candidate_review_rejects_axis_conflict(self) -> None:
        classification = classify_observation(observation(), POLICY)
        reviewed = review_candidates(
            classification,
            candidate_payload(
                [
                    {
                        "phrase": "external candidate label",
                        "label_scope": "composite-lighting",
                        "axis_requirements": {
                            "displayed_key_level": ["low"],
                            "edge_softness": ["soft"],
                            "local_form_contrast": ["strong"],
                        },
                    }
                ]
            ),
            POLICY,
        )
        self.assertEqual(reviewed[0]["review_status"], "conflicting")
        self.assertEqual(reviewed[0]["conflicting_axes"], ["displayed_key_level"])

    def test_low_confidence_axis_keeps_label_inconclusive(self) -> None:
        classification = classify_observation(
            observation(local_form_contrast=("strong", "low")), POLICY
        )
        reviewed = review_candidates(
            classification,
            candidate_payload(
                [
                    {
                        "phrase": "external candidate label",
                        "label_scope": "composite-lighting",
                        "axis_requirements": {
                            "displayed_key_level": ["high"],
                            "edge_softness": ["soft"],
                            "local_form_contrast": ["strong"],
                        },
                    }
                ]
            ),
            POLICY,
        )
        self.assertEqual(reviewed[0]["review_status"], "inconclusive")
        self.assertIn("local_form_contrast", reviewed[0]["unresolved_axes"])

    def test_versioned_vocabulary_provenance_is_preserved(self) -> None:
        classification = classify_observation(observation(), POLICY)
        reviewed = review_candidates(
            classification,
            candidate_payload(
                [
                    {
                        "phrase": "held-out lighting vocabulary label",
                        "label_scope": "edge-character",
                        "axis_requirements": {"edge_softness": ["soft"]},
                    }
                ],
                kind="versioned-vocabulary",
            ),
            POLICY,
        )
        self.assertEqual(
            reviewed[0]["candidate_source"],
            {"kind": "versioned-vocabulary", "reference": "held-out test input"},
        )

    def test_classification_does_not_invent_a_friendly_label(self) -> None:
        result = classify_observation(observation(), POLICY)
        self.assertNotIn("friendly_label_review", result)

    def test_candidate_requirements_must_use_policy_terms(self) -> None:
        classification = classify_observation(observation(), POLICY)
        with self.assertRaisesRegex(ValueError, "invalid policy terms"):
            review_candidates(
                classification,
                candidate_payload(
                    [
                        {
                            "phrase": "held-out invalid candidate",
                            "label_scope": "key-character",
                            "axis_requirements": {
                                "displayed_key_level": ["not-a-policy-term"]
                            },
                        }
                    ]
                ),
                POLICY,
            )


if __name__ == "__main__":
    unittest.main()
