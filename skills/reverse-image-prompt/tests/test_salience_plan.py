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
