#!/usr/bin/env python3

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
import unittest

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

from analysis_bundle import validate_bundle  # noqa: E402
from module_metadata import ROOT, load_manifest, module_map  # noqa: E402
from route_resolver import resolve_analysis_route  # noqa: E402


def valid_bundle() -> dict:
    manifest = load_manifest(ROOT)
    modules = module_map(manifest)
    route = resolve_analysis_route(
        {
            "subjects": ["generic-object"],
            "medium": ["unspecified"],
            "relationships": ["ordinary"],
        },
        manifest,
    )
    source = {"sha256": "a" * 64, "frame": "1200x900"}
    reports = []
    dispositions = []
    for lane_index, lane in enumerate(route["lanes"]):
        finding_id = f"{lane['id']}:f1"
        role = "primary" if lane_index == 0 else "supporting"
        reports.append(
            {
                "schema_version": "reverse-image-analysis-lane-report/v1",
                "route_fingerprint": route["route_fingerprint"],
                "lane_id": lane["id"],
                "source_artifact": deepcopy(source),
                "execution": {"mode": "delegated", "independent_context": True},
                "status": "complete",
                "reviewed_modules": [
                    {"id": module_id, "version": modules[module_id]["version"]}
                    for module_id in lane["module_ids"]
                ],
                "topic_dispositions": [
                    {
                        "topic": topic,
                        "disposition": "analyzed",
                        "finding_ids": [finding_id],
                        "reason": "",
                    }
                    for topic in lane["required_topics"]
                ],
                "findings": [
                    {
                        "id": finding_id,
                        "owner_key": f"owner-{lane_index}",
                        "scale": "global" if lane_index == 0 else "regional",
                        "axis": "hierarchy" if lane_index == 0 else "form",
                        "observation": "held-out source-relative observation",
                        "source_evidence": ["visible held-out cue"],
                        "confidence": "high",
                        "causal_origin": "layout" if lane_index == 0 else "intrinsic",
                        "materiality": "material",
                        "proposed_role": role,
                        "default_drift_risk": "medium",
                        "confounders": [],
                    }
                ],
                "control_requirements": [],
                "omission_checks": [],
                "handoffs": [],
                "conflicts": [],
            }
        )
        dispositions.append(
            {
                "finding_ids": [finding_id],
                "disposition": "retained",
                "final_invariant_id": f"invariant-{lane_index}",
                "final_role": role,
            }
        )
    plan_payload = {
        "render_contract": {
            "invariants": [
                {
                    "id": disposition["final_invariant_id"],
                    "role": disposition["final_role"],
                }
                for disposition in dispositions
            ]
        }
    }
    plan_sha = hashlib.sha256(
        json.dumps(
            plan_payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    return {
        "schema_version": "reverse-image-analysis-bundle/v1",
        "request": {"user_request": "reconstruct the held-out image", "intent_mode": "faithful"},
        "source_artifact": source,
        "route": route,
        "execution": {
            "mode": "delegated",
            "independence_claimed": True,
            "prompt_frozen": True,
        },
        "integrated_plan": {"sha256": plan_sha, "payload": plan_payload},
        "lane_reports": reports,
        "integration": {
            "status": "complete",
            "finding_dispositions": dispositions,
            "conflicts": [],
        },
        "adjudications": [],
        "coverage_review": {
            "reviewer_context": "independent",
            "source_sha256": source["sha256"],
            "route_fingerprint": route["route_fingerprint"],
            "integrated_plan_sha256": plan_sha,
            "reviewed_finding_ids": [
                finding_id
                for report in reports
                for finding_id in [report["findings"][0]["id"]]
            ],
            "reviewed_invariant_ids": [
                invariant["id"]
                for invariant in plan_payload["render_contract"]["invariants"]
            ],
            "status": "pass",
            "issues": [],
        },
    }


class AnalysisBundleTests(unittest.TestCase):
    def test_valid_delegated_bundle_passes(self) -> None:
        self.assertEqual(validate_bundle(valid_bundle()), [])

    def test_missing_required_lane_fails(self) -> None:
        bundle = valid_bundle()
        bundle["lane_reports"].pop()
        self.assertTrue(
            any("exactly one report" in error for error in validate_bundle(bundle))
        )

    def test_route_fingerprint_mismatch_fails(self) -> None:
        bundle = valid_bundle()
        bundle["lane_reports"][0]["route_fingerprint"] = "0" * 64
        self.assertTrue(
            any("route_fingerprint" in error for error in validate_bundle(bundle))
        )

    def test_selected_module_must_be_reviewed_at_current_version(self) -> None:
        bundle = valid_bundle()
        bundle["lane_reports"][0]["reviewed_modules"].pop()
        self.assertTrue(
            any("exactly cover assigned modules" in error for error in validate_bundle(bundle))
        )

        stale = valid_bundle()
        stale["lane_reports"][0]["reviewed_modules"][0]["version"] = -1
        self.assertTrue(any("stale version" in error for error in validate_bundle(stale)))

    def test_material_primary_finding_cannot_be_demoted(self) -> None:
        bundle = valid_bundle()
        bundle["integration"]["finding_dispositions"][0]["final_role"] = "supporting"
        self.assertTrue(
            any("cannot be demoted" in error for error in validate_bundle(bundle))
        )

    def test_final_invariant_must_exist_in_hash_bound_integrated_plan(self) -> None:
        bundle = valid_bundle()
        bundle["integration"]["finding_dispositions"][0][
            "final_invariant_id"
        ] = "does-not-exist-anywhere"
        self.assertTrue(
            any(
                "absent from the integrated plan" in error
                for error in validate_bundle(bundle)
            )
        )

    def test_critic_is_bound_to_the_integrated_plan_hash(self) -> None:
        bundle = valid_bundle()
        bundle["integrated_plan"]["payload"]["render_contract"]["invariants"][
            0
        ]["role"] = "supporting"
        self.assertTrue(
            any(
                "canonical payload" in error
                for error in validate_bundle(bundle)
            )
        )

    def test_sequential_fallback_cannot_claim_independence(self) -> None:
        bundle = valid_bundle()
        bundle["execution"]["mode"] = "sequential-fallback"
        for report in bundle["lane_reports"]:
            report["execution"] = {
                "mode": "sequential-fallback",
                "independent_context": False,
            }
        self.assertTrue(
            any("cannot claim independent" in error for error in validate_bundle(bundle))
        )

    def test_sequential_fallback_cannot_freeze_with_same_context_critic(self) -> None:
        bundle = valid_bundle()
        bundle["execution"].update(
            {"mode": "sequential-fallback", "independence_claimed": False}
        )
        for report in bundle["lane_reports"]:
            report["execution"] = {
                "mode": "sequential-fallback",
                "independent_context": False,
            }
        bundle["coverage_review"]["reviewer_context"] = "same-context"
        self.assertTrue(
            any(
                "prompt freeze requires an independent coverage reviewer" in error
                for error in validate_bundle(bundle)
            )
        )

    def test_mixed_execution_discloses_fallback_non_independence(self) -> None:
        bundle = valid_bundle()
        bundle["execution"]["mode"] = "mixed"
        bundle["lane_reports"][0]["execution"] = {
            "mode": "sequential-fallback",
            "independent_context": False,
        }
        self.assertTrue(
            any(
                "mixed execution with fallback reports cannot claim independence" in error
                for error in validate_bundle(bundle)
            )
        )

    def test_prompt_cannot_freeze_before_critic_pass(self) -> None:
        bundle = valid_bundle()
        bundle["coverage_review"] = {
            "reviewer_context": "independent",
            "source_sha256": bundle["source_artifact"]["sha256"],
            "route_fingerprint": bundle["route"]["route_fingerprint"],
            "integrated_plan_sha256": bundle["integrated_plan"]["sha256"],
            "reviewed_finding_ids": [
                finding["id"]
                for report in bundle["lane_reports"]
                for finding in report["findings"]
            ],
            "reviewed_invariant_ids": [
                invariant["id"]
                for invariant in bundle["integrated_plan"]["payload"][
                    "render_contract"
                ]["invariants"]
            ],
            "status": "revise-integration",
            "issues": [{"kind": "merge-loss", "evidence": "one primary finding disappeared"}],
        }
        self.assertTrue(
            any("prompt cannot freeze" in error for error in validate_bundle(bundle))
        )

    def test_reported_conflict_requires_integration_disposition(self) -> None:
        bundle = valid_bundle()
        bundle["lane_reports"][0]["conflicts"] = [
            {
                "id": "conflict-one",
                "owner_key": "owner-0",
                "source_evidence": ["opposed held-out evidence"],
            }
        ]
        self.assertTrue(
            any("dispose every reported conflict" in error for error in validate_bundle(bundle))
        )


if __name__ == "__main__":
    unittest.main()
