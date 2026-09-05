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

    def route(
        self, *, lighting: bool = False, subjects: list[str] | None = None
    ) -> dict:
        subjects = ["human"] if subjects is None else subjects
        risks = ["face-detail"] if "human" in subjects else []
        if lighting:
            risks.append("lighting-fidelity")
        return resolve_analysis_route(
            {
                "subjects": subjects,
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

    def candidate(self, *, human: bool = True) -> dict:
        candidate = {
            "scope": "human-appearance" if human else "general",
            "phrase": "An independently supported aggregate reading.",
            "candidate_source": {
                "kind": "source-visible-approximation",
                "reference": self.source["sha256"],
            },
            "confidence": "medium",
            "viewer_priority": "P1",
            "omission_counterfactual": "material-drift",
            "decomposition_requirements": [
                "Preserve the separately owned visible form requirement."
            ],
        }
        if human:
            candidate["effect_budget"] = {
                "intended_dimensions": ["face-form"],
                "protected_dimensions": ["identity-context", "pose-occlusion"],
            }
        return candidate

    def finding_errors(
        self,
        finding: dict,
        *,
        route: dict | None = None,
        lane_id: str = "lane.subject-appearance",
    ) -> list[str]:
        route = self.route() if route is None else route
        lane = next(item for item in route["lanes"] if item["id"] == lane_id)
        report = self.report(route, lane, findings=[finding])
        return validate_compact_set(
            self.compact_set(route, replacements={lane_id: report}), self.manifest
        )

    def candidate_finding(self, representation: str = "atomic") -> dict:
        finding = self.macro_finding("lane.subject-appearance")
        finding["representation"] = representation
        if representation == "atomic":
            finding["summary_adequacy"] = None
        finding["aggregate_descriptor_candidate"] = self.candidate()
        return finding

    def test_aggregate_candidate_is_optional_for_atomic_and_macro_findings(
        self,
    ) -> None:
        for representation in ("atomic", "macro-summary"):
            with self.subTest(representation=representation):
                finding = self.candidate_finding(representation)
                del finding["aggregate_descriptor_candidate"]
                self.assertEqual(self.finding_errors(finding), [])

    def test_valid_aggregate_provenance_for_atomic_and_macro_findings(self) -> None:
        for representation in ("atomic", "macro-summary"):
            for kind, reference in (
                ("source-visible-approximation", self.source["sha256"]),
                ("user-supplied", "raw-request:appearance-reading"),
                ("versioned-vocabulary", "task-vocabulary/v1:entry-a"),
            ):
                for confidence, priority in (("high", "P0"), ("medium", "P1")):
                    with self.subTest(
                        representation=representation,
                        kind=kind,
                        confidence=confidence,
                    ):
                        finding = self.candidate_finding(representation)
                        candidate = finding["aggregate_descriptor_candidate"]
                        candidate["candidate_source"] = {
                            "kind": kind,
                            "reference": reference,
                        }
                        candidate["confidence"] = confidence
                        candidate["viewer_priority"] = priority
                        self.assertEqual(self.finding_errors(finding), [])

    def test_candidate_object_is_required_when_present(self) -> None:
        for representation in ("atomic", "macro-summary"):
            for candidate in (None, "unbounded descriptor", 4, [], True):
                with self.subTest(representation=representation, candidate=candidate):
                    finding = self.candidate_finding(representation)
                    finding["aggregate_descriptor_candidate"] = candidate
                    errors = self.finding_errors(finding)
                    self.assertTrue(
                        any(
                            "aggregate_descriptor_candidate must be an object" in e
                            for e in errors
                        ),
                        errors,
                    )

    def test_candidate_required_fields_reject_missing_and_malformed_values(
        self,
    ) -> None:
        invalid_values = {
            "phrase": (None, "", " ", []),
            "candidate_source": (None, "source", []),
            "confidence": (None, "low", "uncertain", []),
            "viewer_priority": (None, "P2", "P3", []),
            "omission_counterfactual": (None, "preserved", "uncertain", {}),
            "decomposition_requirements": (None, "form", [], [" "], [{}]),
        }
        for representation in ("atomic", "macro-summary"):
            for field, values in invalid_values.items():
                for missing, value in [(True, None)] + [
                    (False, value) for value in values
                ]:
                    with self.subTest(
                        representation=representation,
                        field=field,
                        missing=missing,
                        value=value,
                    ):
                        finding = self.candidate_finding(representation)
                        candidate = finding["aggregate_descriptor_candidate"]
                        if missing:
                            del candidate[field]
                        else:
                            candidate[field] = value
                        errors = self.finding_errors(finding)
                        self.assertTrue(
                            any(
                                f"aggregate_descriptor_candidate.{field}" in e
                                for e in errors
                            ),
                            errors,
                        )

    def test_candidate_provenance_requires_allowed_kind_and_reference(self) -> None:
        for representation in ("atomic", "macro-summary"):
            for source, expected_field in (
                ({"reference": "observation-a"}, "kind"),
                ({"kind": "preferred-label", "reference": "observation-a"}, "kind"),
                ({"kind": [], "reference": "observation-a"}, "kind"),
                ({"kind": "source-visible-approximation"}, "reference"),
                ({"kind": "user-supplied", "reference": " "}, "reference"),
                ({"kind": "versioned-vocabulary", "reference": {}}, "reference"),
            ):
                with self.subTest(representation=representation, source=source):
                    finding = self.candidate_finding(representation)
                    finding["aggregate_descriptor_candidate"][
                        "candidate_source"
                    ] = source
                    errors = self.finding_errors(finding)
                    self.assertTrue(
                        any(f"candidate_source.{expected_field}" in e for e in errors),
                        errors,
                    )

    def test_candidate_scope_rejects_unknown_and_malformed_values(self) -> None:
        for scope in (None, "human", "preferred-appearance", [], {}):
            with self.subTest(scope=scope):
                finding = self.candidate_finding()
                finding["aggregate_descriptor_candidate"]["scope"] = scope
                errors = self.finding_errors(finding)
                self.assertTrue(
                    any("aggregate_descriptor_candidate.scope" in e for e in errors)
                )

    def test_legacy_human_candidate_requires_effect_budget(self) -> None:
        for representation in ("atomic", "macro-summary"):
            with self.subTest(representation=representation):
                finding = self.candidate_finding(representation)
                candidate = finding["aggregate_descriptor_candidate"]
                del candidate["scope"]
                self.assertEqual(self.finding_errors(finding), [])
                del candidate["effect_budget"]
                errors = self.finding_errors(finding)
                self.assertTrue(
                    any("effect_budget must be an object" in e for e in errors)
                )

    def test_explicit_human_scope_requires_budget_without_human_lane_modules(
        self,
    ) -> None:
        route = self.route(subjects=["product"])
        finding = self.candidate_finding()
        self.assertEqual(self.finding_errors(finding, route=route), [])
        del finding["aggregate_descriptor_candidate"]["effect_budget"]
        errors = self.finding_errors(finding, route=route)
        self.assertTrue(any("effect_budget must be an object" in e for e in errors))

    def test_human_budget_requires_valid_intended_and_protected_dimensions(
        self,
    ) -> None:
        invalid_budgets = (
            (None, "effect_budget must be an object"),
            ("form", "effect_budget must be an object"),
            ({}, "intended_dimensions"),
            (
                {
                    "intended_dimensions": [],
                    "protected_dimensions": ["identity-context"],
                },
                "intended_dimensions",
            ),
            (
                {
                    "intended_dimensions": [" "],
                    "protected_dimensions": ["identity-context"],
                },
                "intended_dimensions",
            ),
            (
                {
                    "intended_dimensions": [{}],
                    "protected_dimensions": ["identity-context"],
                },
                "intended_dimensions",
            ),
            (
                {
                    "intended_dimensions": ["face-form"],
                    "protected_dimensions": "identity-context",
                },
                "protected_dimensions",
            ),
            (
                {"intended_dimensions": ["face-form"], "protected_dimensions": []},
                "must include identity-context",
            ),
            (
                {
                    "intended_dimensions": ["face-form"],
                    "protected_dimensions": ["pose-occlusion"],
                },
                "must include identity-context",
            ),
            (
                {
                    "intended_dimensions": ["identity-context"],
                    "protected_dimensions": ["pose-occlusion"],
                },
                "cannot control identity-context",
            ),
            (
                {
                    "intended_dimensions": ["face-form"],
                    "protected_dimensions": ["identity-context", "face-form"],
                },
                "both intend and protect",
            ),
            (
                {
                    "intended_dimensions": ["face-form", "face-form"],
                    "protected_dimensions": ["identity-context"],
                },
                "contains duplicates",
            ),
            (
                {
                    "intended_dimensions": ["face-form"],
                    "protected_dimensions": ["identity-context", "identity-context"],
                },
                "contains duplicates",
            ),
        )
        for representation in ("atomic", "macro-summary"):
            for budget, expected_error in invalid_budgets:
                with self.subTest(representation=representation, budget=budget):
                    finding = self.candidate_finding(representation)
                    finding["aggregate_descriptor_candidate"]["effect_budget"] = budget
                    errors = self.finding_errors(finding)
                    self.assertTrue(any(expected_error in e for e in errors), errors)

    def test_explicit_general_candidate_in_mixed_subject_lane_needs_no_human_budget(
        self,
    ) -> None:
        route = self.route(subjects=["human", "product"])
        for representation in ("atomic", "macro-summary"):
            with self.subTest(representation=representation):
                finding = self.candidate_finding(representation)
                finding["aggregate_descriptor_candidate"] = self.candidate(human=False)
                self.assertEqual(self.finding_errors(finding, route=route), [])
                finding["aggregate_descriptor_candidate"]["effect_budget"] = {
                    "intended_dimensions": ["object-silhouette"],
                    "protected_dimensions": ["frame-placement"],
                }
                self.assertEqual(self.finding_errors(finding, route=route), [])

    def test_legacy_nonhuman_candidate_needs_no_human_budget(self) -> None:
        route = self.route(subjects=["product"])
        finding = self.candidate_finding()
        finding["aggregate_descriptor_candidate"] = self.candidate(human=False)
        del finding["aggregate_descriptor_candidate"]["scope"]
        self.assertEqual(self.finding_errors(finding, route=route), [])

    def test_general_candidate_validates_any_supplied_budget(self) -> None:
        finding = self.candidate_finding()
        finding["aggregate_descriptor_candidate"] = self.candidate(human=False)
        for budget in (
            None,
            "budget",
            {},
            {"intended_dimensions": ["form"], "protected_dimensions": ["form"]},
        ):
            with self.subTest(budget=budget):
                finding["aggregate_descriptor_candidate"]["effect_budget"] = budget
                errors = self.finding_errors(finding)
                self.assertTrue(any("effect_budget" in e for e in errors), errors)

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
