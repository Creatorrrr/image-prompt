#!/usr/bin/env python3

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import sys
import unittest

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

from compact_reports import (  # noqa: E402
    REPORT_SCHEMA,
    SET_SCHEMA,
    validate_compact_set,
)
from module_metadata import ROOT, load_manifest, module_map  # noqa: E402
from route_resolver import resolve_analysis_route  # noqa: E402


class CompactReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest(ROOT)
        cls.modules = module_map(cls.manifest)
        cls.source = {"sha256": "a" * 64, "frame": "800x1000"}

    def route(self, *, lighting: bool = False) -> dict:
        risks = ["face-detail"]
        if lighting:
            risks.append("lighting-fidelity")
        return resolve_analysis_route(
            {
                "subjects": ["human"],
                "medium": ["photographic"],
                "relationships": ["ordinary"],
                "detail_risks": risks,
            },
            self.manifest,
        )

    def report(
        self,
        route: dict,
        lane: dict,
        *,
        findings: list[dict] | None = None,
        handoffs: list[dict] | None = None,
    ) -> dict:
        return {
            "schema_version": REPORT_SCHEMA,
            "route_fingerprint": route["route_fingerprint"],
            "lane_id": lane["id"],
            "source_artifact": dict(self.source),
            "execution": {"mode": "delegated", "independent_context": True},
            "status": "complete",
            "reviewed_modules": [
                {"id": module_id, "version": self.modules[module_id]["version"]}
                for module_id in lane["module_ids"]
            ],
            "primary_read": "A source-relative viewer-material result.",
            "material_findings": findings or [],
            "supporting_findings": [],
            "grouped_non_material_topics": [],
            "uncertainties": [],
            "handoffs": handoffs or [],
            "conflicts": [],
            "escalation": {"required": False, "reason": ""},
        }

    def compact_set(
        self,
        route: dict,
        *,
        replacements: dict[str, dict] | None = None,
    ) -> dict:
        replacements = replacements or {}
        reports = [
            replacements.get(lane["id"], self.report(route, lane))
            for lane in route["lanes"]
        ]
        return {
            "schema_version": SET_SCHEMA,
            "source_artifact": dict(self.source),
            "route": route,
            "lane_reports": reports,
        }

    def macro_finding(
        self,
        lane_id: str,
        *,
        verdict: str = "sufficient",
        owner_lane: str | None = None,
    ) -> dict:
        finding_id = f"{lane_id}:f1"
        residuals: list[dict] = []
        if verdict in {"lossy", "uncertain"}:
            residuals.append(
                {
                    "id": f"{finding_id}:r1",
                    "subject_or_region_ids": ["source-region-a", "source-region-b"],
                    "relation_kind": "source-relative relation",
                    "visible_result": "The two visible regions retain their source relation.",
                    "source_evidence": ["visible boundary and depth ordering"],
                    "confidence": "medium",
                    "control_requirement": "Preserve the observed relation without normalizing it.",
                    "causal_owner_lane": owner_lane or lane_id,
                    "dependencies": [],
                }
            )
        return {
            "id": finding_id,
            "owner_key": "source-relative-coupled-result",
            "viewer_priority": "P1",
            "representation": "macro-summary",
            "observation": "Several visible relations jointly create one macro result.",
            "source_evidence": ["jointly material source cues"],
            "confidence": "medium",
            "change_counterfactual": "Normalizing the relations changes the source read.",
            "default_drift_risk": "high",
            "control_requirement": "State the macro result first, then only at-risk relations.",
            "summary_adequacy": {
                "verdict": verdict,
                "at_risk_relations": residuals,
            },
        }

    def test_valid_sufficient_summary_needs_no_residuals(self) -> None:
        route = self.route()
        lane = next(item for item in route["lanes"] if item["id"] == "lane.spatial-topology")
        report = self.report(
            route,
            lane,
            findings=[self.macro_finding(lane["id"], verdict="sufficient")],
        )
        payload = self.compact_set(route, replacements={lane["id"]: report})
        self.assertEqual(validate_compact_set(payload, self.manifest), [])

    def test_lossy_summary_requires_at_risk_relations(self) -> None:
        route = self.route()
        lane = next(item for item in route["lanes"] if item["id"] == "lane.spatial-topology")
        finding = self.macro_finding(lane["id"], verdict="lossy")
        finding["summary_adequacy"]["at_risk_relations"] = []
        report = self.report(route, lane, findings=[finding])
        errors = validate_compact_set(
            self.compact_set(route, replacements={lane["id"]: report}),
            self.manifest,
        )
        self.assertTrue(any("lossy summary requires" in error for error in errors))

    def test_sufficient_summary_rejects_residual_overactuation(self) -> None:
        route = self.route()
        lane = next(item for item in route["lanes"] if item["id"] == "lane.spatial-topology")
        finding = self.macro_finding(lane["id"], verdict="lossy")
        finding["summary_adequacy"]["verdict"] = "sufficient"
        report = self.report(route, lane, findings=[finding])
        errors = validate_compact_set(
            self.compact_set(route, replacements={lane["id"]: report}),
            self.manifest,
        )
        self.assertTrue(any("must not emit residual" in error for error in errors))

    def test_atomic_finding_rejects_macro_adequacy_payload(self) -> None:
        route = self.route()
        lane = next(item for item in route["lanes"] if item["id"] == "lane.spatial-topology")
        finding = self.macro_finding(lane["id"])
        finding["representation"] = "atomic"
        report = self.report(route, lane, findings=[finding])
        errors = validate_compact_set(
            self.compact_set(route, replacements={lane["id"]: report}),
            self.manifest,
        )
        self.assertTrue(any("only for macro-summary" in error for error in errors))

    def test_cross_lane_residual_requires_closed_handoff(self) -> None:
        route = self.route(lighting=True)
        lane = next(item for item in route["lanes"] if item["id"] == "lane.medium-aesthetic-capture")
        finding = self.macro_finding(
            lane["id"],
            verdict="lossy",
            owner_lane="lane.color-light-material",
        )
        report = self.report(route, lane, findings=[finding])
        errors = validate_compact_set(
            self.compact_set(route, replacements={lane["id"]: report}),
            self.manifest,
        )
        self.assertTrue(
            any("lacks a closed P0/P1 handoff" in error for error in errors)
        )

    def test_closed_light_form_handoff_passes_when_lane_and_module_are_routed(self) -> None:
        route = self.route(lighting=True)
        lane = next(item for item in route["lanes"] if item["id"] == "lane.medium-aesthetic-capture")
        finding = self.macro_finding(
            lane["id"],
            verdict="lossy",
            owner_lane="lane.color-light-material",
        )
        residual_id = finding["summary_adequacy"]["at_risk_relations"][0]["id"]
        handoff = {
            "id": f"{lane['id']}:h1",
            "source_ids": [residual_id],
            "viewer_priority": "P1",
            "target_lane": "lane.color-light-material",
            "required_module_id": "detail.light-form-fidelity",
            "reason": "The visible regional light relation needs its causal owner.",
            "route_required": True,
        }
        report = self.report(route, lane, findings=[finding], handoffs=[handoff])
        payload = self.compact_set(route, replacements={lane["id"]: report})
        self.assertEqual(validate_compact_set(payload, self.manifest), [])

    def test_missing_light_form_lane_is_a_route_gap(self) -> None:
        route = self.route(lighting=False)
        lane = next(item for item in route["lanes"] if item["id"] == "lane.medium-aesthetic-capture")
        finding = self.macro_finding(
            lane["id"],
            verdict="lossy",
            owner_lane="lane.color-light-material",
        )
        residual_id = finding["summary_adequacy"]["at_risk_relations"][0]["id"]
        handoff = {
            "id": f"{lane['id']}:h1",
            "source_ids": [residual_id],
            "viewer_priority": "P1",
            "target_lane": "lane.color-light-material",
            "required_module_id": "detail.light-form-fidelity",
            "reason": "The source makes regional light-to-form structure material.",
            "route_required": True,
        }
        report = self.report(route, lane, findings=[finding], handoffs=[handoff])
        errors = validate_compact_set(
            self.compact_set(route, replacements={lane["id"]: report}),
            self.manifest,
        )
        self.assertTrue(any(error.startswith("route-gap:") for error in errors))

    def test_report_schema_drift_is_rejected(self) -> None:
        route = self.route()
        payload = self.compact_set(route)
        payload = deepcopy(payload)
        payload["lane_reports"][0]["schema_version"] = (
            "reverse-image-analysis-lane-report/compact-v1"
        )
        errors = validate_compact_set(payload, self.manifest)
        self.assertTrue(any("compact-v2" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
