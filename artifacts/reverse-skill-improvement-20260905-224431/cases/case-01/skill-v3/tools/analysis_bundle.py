#!/usr/bin/env python3
"""Validate distributed reverse-image analysis routes, reports, and integration."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

from module_metadata import ROOT, load_manifest, module_map
from route_resolver import resolve_analysis_route

BUNDLE_SCHEMA = "reverse-image-analysis-bundle/v2"
REPORT_SCHEMA = "reverse-image-analysis-lane-report/v2"
VALID_INTENT_MODES = {"faithful", "semantic", "polished-fidelity", "diagnostic"}
VALID_EXECUTION_MODES = {"delegated", "sequential-fallback", "mixed"}
VALID_REPORT_MODES = {"delegated", "sequential-fallback"}
VALID_REPORT_STATUS = {"complete", "uncertain", "blocked"}
VALID_TOPIC_DISPOSITIONS = {"analyzed", "not-material", "uncertain", "blocked"}
VALID_FINDING_SCALES = {"global", "regional", "local"}
VALID_FINDING_AXES = {
    "form",
    "surface",
    "light-to-form",
    "color",
    "sharpness",
    "hierarchy",
    "topology",
    "information",
}
VALID_CONFIDENCE = {"high", "medium", "low"}
VALID_CAUSAL_ORIGINS = {
    "intrinsic",
    "pose-deformation",
    "perspective",
    "lighting-shadow",
    "material-interaction",
    "processing",
    "spatial-relation",
    "layout",
}
VALID_MATERIALITY = {"material", "uncertain", "diagnostic"}
VALID_ROLES = {"primary", "supporting"}
VALID_DRIFT_RISK = {"high", "medium", "low", "uncertain"}
VALID_ATTRIBUTION_STATUS = {"resolved", "confounded", "uncertain", "not-applicable"}
VALID_STRENGTHS = {"subtle", "moderate", "strong"}
VALID_INTEGRATION_STATUS = {"complete", "revise", "blocked"}
VALID_FINDING_DISPOSITIONS = {
    "retained",
    "merged",
    "diagnostic-only",
    "rejected",
    "uncertain",
}
VALID_OBLIGATION_DISPOSITIONS = {
    "retained",
    "merged",
    "diagnostic-only",
    "rejected",
    "uncertain",
}
VALID_CRITIC_STATUS = {"pass", "revise-route", "revise-integration", "blocked"}
VALID_CRITIC_ISSUES = {
    "route-gap",
    "topic-gap",
    "merge-loss",
    "unsupported-addition",
    "ownership-conflict",
    "role-strength-drift",
    "scope-leakage",
    "unresolved-uncertainty",
    "obligation-loss",
    "result-direction-loss",
    "coupling-loss",
    "topology-collapse",
    "net-neutralization",
    "salience-order-drift",
}
VALID_CONFLICT_RESOLUTIONS = {"automatic", "adjudicated", "uncertain"}


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: Any, *, nonempty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (bool(value) or not nonempty)
        and all(_nonempty_string(item) for item in value)
    )


def _canonical_sha256(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _validate_route(route: Any, manifest: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
    if not isinstance(route, dict):
        return ["route must be an object"], {}
    errors: list[str] = []
    facets = route.get("normalized_facets")
    if not isinstance(facets, dict):
        return ["route.normalized_facets must be an object"], route
    try:
        expected = resolve_analysis_route(
            facets, manifest, analysis_profile=route.get("analysis_profile", "prompt")
        )
    except (KeyError, TypeError, ValueError) as exc:
        return [f"route cannot be reconstructed: {exc}"], route
    if route != expected:
        errors.append("route must exactly match the deterministic analysis route")
    return errors, expected


def validate_bundle(
    bundle: dict[str, Any], manifest: dict[str, Any] | None = None
) -> list[str]:
    """Return structural errors without pretending to judge visual correctness."""

    manifest = manifest or load_manifest(ROOT)
    errors: list[str] = []
    if bundle.get("schema_version") != BUNDLE_SCHEMA:
        errors.append(f"schema_version must be {BUNDLE_SCHEMA!r}")

    request = bundle.get("request")
    if not isinstance(request, dict):
        errors.append("request must be an object")
    else:
        if not _nonempty_string(request.get("user_request")):
            errors.append("request.user_request must be non-empty")
        if request.get("intent_mode") not in VALID_INTENT_MODES:
            errors.append("request.intent_mode is invalid")

    source = bundle.get("source_artifact")
    if not isinstance(source, dict):
        errors.append("source_artifact must be an object")
        source_sha = ""
    else:
        source_sha = source.get("sha256", "")
        if not isinstance(source_sha, str) or re.fullmatch(r"[0-9a-f]{64}", source_sha) is None:
            errors.append("source_artifact.sha256 must be a lowercase SHA-256")
        if not _nonempty_string(source.get("frame")):
            errors.append("source_artifact.frame must be non-empty")

    route_errors, route = _validate_route(bundle.get("route"), manifest)
    errors.extend(route_errors)
    route_fingerprint = route.get("route_fingerprint", "")
    route_lanes = {
        lane.get("id"): lane
        for lane in route.get("lanes", [])
        if isinstance(lane, dict) and _nonempty_string(lane.get("id"))
    }

    execution = bundle.get("execution")
    if not isinstance(execution, dict):
        errors.append("execution must be an object")
        execution_mode = ""
        prompt_frozen = False
    else:
        execution_mode = execution.get("mode")
        if execution_mode not in VALID_EXECUTION_MODES:
            errors.append("execution.mode is invalid")
        prompt_frozen = execution.get("prompt_frozen")
        if not isinstance(prompt_frozen, bool):
            errors.append("execution.prompt_frozen must be boolean")
            prompt_frozen = False
        if not isinstance(execution.get("independence_claimed"), bool):
            errors.append("execution.independence_claimed must be boolean")

    integrated_plan = bundle.get("integrated_plan")
    plan_sha = ""
    plan_invariant_map: dict[str, dict[str, Any]] = {}
    if not isinstance(integrated_plan, dict):
        errors.append("integrated_plan must be an object")
    else:
        plan_payload = integrated_plan.get("payload")
        plan_sha = integrated_plan.get("sha256", "")
        if not isinstance(plan_payload, dict):
            errors.append("integrated_plan.payload must be an object")
            plan_payload = {}
        if not isinstance(plan_sha, str) or re.fullmatch(r"[0-9a-f]{64}", plan_sha) is None:
            errors.append("integrated_plan.sha256 must be a lowercase SHA-256")
        elif plan_sha != _canonical_sha256(plan_payload):
            errors.append("integrated_plan.sha256 does not match its canonical payload")
        render_contract = plan_payload.get("render_contract")
        invariants = (
            render_contract.get("invariants")
            if isinstance(render_contract, dict)
            else None
        )
        if not isinstance(invariants, list):
            errors.append(
                "integrated_plan.payload.render_contract.invariants must be a list"
            )
            invariants = []
        for index, invariant in enumerate(invariants):
            label = f"integrated_plan.payload.render_contract.invariants[{index}]"
            if not isinstance(invariant, dict) or not _nonempty_string(
                invariant.get("id")
            ):
                errors.append(f"{label}.id must be non-empty")
                continue
            invariant_id = str(invariant["id"])
            if invariant_id in plan_invariant_map:
                errors.append(f"duplicate integrated plan invariant: {invariant_id}")
            plan_invariant_map[invariant_id] = invariant
            if invariant.get("role") not in VALID_ROLES:
                errors.append(f"{label}.role is invalid")

    reports = bundle.get("lane_reports")
    if not isinstance(reports, list):
        errors.append("lane_reports must be a list")
        reports = []
    report_lane_ids: set[str] = set()
    report_modes_seen: set[str] = set()
    non_independent_report_seen = False
    finding_map: dict[str, dict[str, Any]] = {}
    obligation_map: dict[str, dict[str, Any]] = {}
    conflict_ids: set[str] = set()
    modules = module_map(manifest)

    for index, report in enumerate(reports):
        label = f"lane_reports[{index}]"
        if not isinstance(report, dict):
            errors.append(f"{label} must be an object")
            continue
        if report.get("schema_version") != REPORT_SCHEMA:
            errors.append(f"{label}.schema_version is invalid")
        lane_id = report.get("lane_id")
        if lane_id not in route_lanes:
            errors.append(f"{label}.lane_id is not required by the route")
            continue
        if lane_id in report_lane_ids:
            errors.append(f"duplicate lane report: {lane_id}")
        report_lane_ids.add(str(lane_id))
        lane = route_lanes[lane_id]
        if report.get("route_fingerprint") != route_fingerprint:
            errors.append(f"{label}.route_fingerprint does not match the route")
        report_source = report.get("source_artifact")
        if not isinstance(report_source, dict) or report_source.get("sha256") != source_sha:
            errors.append(f"{label}.source_artifact.sha256 does not match the bundle")
        elif report_source.get("frame") != source.get("frame"):
            errors.append(f"{label}.source_artifact.frame does not match the bundle")

        report_execution = report.get("execution")
        if not isinstance(report_execution, dict):
            errors.append(f"{label}.execution must be an object")
            report_mode = ""
            independent = None
        else:
            report_mode = report_execution.get("mode")
            independent = report_execution.get("independent_context")
            if report_mode not in VALID_REPORT_MODES:
                errors.append(f"{label}.execution.mode is invalid")
            else:
                report_modes_seen.add(str(report_mode))
            if not isinstance(independent, bool):
                errors.append(f"{label}.execution.independent_context must be boolean")
            elif independent is False:
                non_independent_report_seen = True
            if report_mode == "delegated" and independent is not True:
                errors.append(f"{label}: delegated reports require independent context")
            if report_mode == "sequential-fallback" and independent is not False:
                errors.append(
                    f"{label}: sequential reports must disclose non-independent context"
                )
        if execution_mode == "delegated" and (
            report_mode != "delegated" or independent is not True
        ):
            errors.append(f"{label} must be an independent delegated report")
        if execution_mode == "sequential-fallback" and (
            report_mode != "sequential-fallback" or independent is not False
        ):
            errors.append(f"{label} must disclose sequential non-independent execution")

        status = report.get("status")
        if status not in VALID_REPORT_STATUS:
            errors.append(f"{label}.status is invalid")

        reviewed = report.get("reviewed_modules")
        reviewed_versions: dict[str, Any] = {}
        if not isinstance(reviewed, list):
            errors.append(f"{label}.reviewed_modules must be a list")
            reviewed = []
        for reviewed_index, item in enumerate(reviewed):
            if not isinstance(item, dict) or not _nonempty_string(item.get("id")):
                errors.append(
                    f"{label}.reviewed_modules[{reviewed_index}] must name a module"
                )
                continue
            module_id = item["id"]
            if module_id in reviewed_versions:
                errors.append(f"{label}.reviewed_modules repeats {module_id!r}")
            reviewed_versions[module_id] = item.get("version")
        expected_modules = set(lane.get("module_ids", []))
        if set(reviewed_versions) != expected_modules:
            errors.append(f"{label}.reviewed_modules must exactly cover assigned modules")
        for module_id in expected_modules & set(reviewed_versions):
            if reviewed_versions[module_id] != modules[module_id].get("version"):
                errors.append(f"{label}.reviewed_modules has stale version for {module_id}")

        findings = report.get("findings")
        if not isinstance(findings, list):
            errors.append(f"{label}.findings must be a list")
            findings = []
        local_finding_ids: set[str] = set()
        for finding_index, finding in enumerate(findings):
            finding_label = f"{label}.findings[{finding_index}]"
            if not isinstance(finding, dict):
                errors.append(f"{finding_label} must be an object")
                continue
            finding_id = finding.get("id")
            if not _nonempty_string(finding_id) or not str(finding_id).startswith(
                f"{lane_id}:"
            ):
                errors.append(f"{finding_label}.id must use the lane namespace")
                continue
            if finding_id in finding_map:
                errors.append(f"duplicate finding id: {finding_id}")
            finding_map[str(finding_id)] = finding
            local_finding_ids.add(str(finding_id))
            if not _nonempty_string(finding.get("owner_key")):
                errors.append(f"{finding_label}.owner_key must be non-empty")
            if finding.get("scale") not in VALID_FINDING_SCALES:
                errors.append(f"{finding_label}.scale is invalid")
            if finding.get("axis") not in VALID_FINDING_AXES:
                errors.append(f"{finding_label}.axis is invalid")
            if not _nonempty_string(finding.get("observation")):
                errors.append(f"{finding_label}.observation must be non-empty")
            if not _string_list(finding.get("source_evidence"), nonempty=True):
                errors.append(f"{finding_label}.source_evidence must be non-empty")
            if finding.get("confidence") not in VALID_CONFIDENCE:
                errors.append(f"{finding_label}.confidence is invalid")
            if finding.get("causal_origin") not in VALID_CAUSAL_ORIGINS:
                errors.append(f"{finding_label}.causal_origin is invalid")
            if finding.get("materiality") not in VALID_MATERIALITY:
                errors.append(f"{finding_label}.materiality is invalid")
            if finding.get("proposed_role") not in VALID_ROLES:
                errors.append(f"{finding_label}.proposed_role is invalid")
            if finding.get("default_drift_risk") not in VALID_DRIFT_RISK:
                errors.append(f"{finding_label}.default_drift_risk is invalid")
            if not _string_list(finding.get("confounders")):
                errors.append(f"{finding_label}.confounders must be a list of strings")

            obligations = finding.get("atomic_obligations")
            if not isinstance(obligations, list):
                errors.append(f"{finding_label}.atomic_obligations must be a list")
                obligations = []
            if finding.get("materiality") == "material" and not obligations:
                errors.append(
                    f"{finding_label}: material findings require atomic obligations"
                )
            local_obligation_ids: set[str] = set()
            for obligation_index, obligation in enumerate(obligations):
                obligation_label = (
                    f"{finding_label}.atomic_obligations[{obligation_index}]"
                )
                if not isinstance(obligation, dict):
                    errors.append(f"{obligation_label} must be an object")
                    continue
                obligation_id = obligation.get("id")
                if not _nonempty_string(obligation_id) or not str(
                    obligation_id
                ).startswith(f"{finding_id}:"):
                    errors.append(
                        f"{obligation_label}.id must use the finding namespace"
                    )
                    continue
                obligation_id = str(obligation_id)
                if obligation_id in obligation_map:
                    errors.append(f"duplicate atomic obligation id: {obligation_id}")
                if obligation_id in local_obligation_ids:
                    errors.append(
                        f"{finding_label}.atomic_obligations repeats {obligation_id!r}"
                    )
                local_obligation_ids.add(obligation_id)
                obligation_map[obligation_id] = obligation
                if obligation.get("axis") not in VALID_FINDING_AXES:
                    errors.append(f"{obligation_label}.axis is invalid")
                if not _nonempty_string(obligation.get("visible_result")):
                    errors.append(
                        f"{obligation_label}.visible_result must be source-relative and non-empty"
                    )
                if not _nonempty_string(obligation.get("result_direction")):
                    errors.append(
                        f"{obligation_label}.result_direction must be source-relative and non-empty"
                    )
                if not _string_list(
                    obligation.get("subject_or_region_ids"), nonempty=True
                ):
                    errors.append(
                        f"{obligation_label}.subject_or_region_ids must be non-empty"
                    )
                if not _nonempty_string(obligation.get("relation_kind")):
                    errors.append(f"{obligation_label}.relation_kind must be non-empty")
                if not _string_list(
                    obligation.get("source_evidence"), nonempty=True
                ):
                    errors.append(
                        f"{obligation_label}.source_evidence must be non-empty"
                    )
                if obligation.get("confidence") not in VALID_CONFIDENCE:
                    errors.append(f"{obligation_label}.confidence is invalid")
                if obligation.get("causal_origin") not in VALID_CAUSAL_ORIGINS:
                    errors.append(f"{obligation_label}.causal_origin is invalid")
                if obligation.get("attribution_status") not in VALID_ATTRIBUTION_STATUS:
                    errors.append(f"{obligation_label}.attribution_status is invalid")
                if obligation.get("materiality") not in VALID_MATERIALITY:
                    errors.append(f"{obligation_label}.materiality is invalid")
                if obligation.get("proposed_role") not in VALID_ROLES:
                    errors.append(f"{obligation_label}.proposed_role is invalid")
                if obligation.get("target_strength") not in VALID_STRENGTHS:
                    errors.append(f"{obligation_label}.target_strength is invalid")
                if not _string_list(obligation.get("confounders")):
                    errors.append(
                        f"{obligation_label}.confounders must be a list of strings"
                    )

        dispositions = report.get("topic_dispositions")
        if not isinstance(dispositions, list):
            errors.append(f"{label}.topic_dispositions must be a list")
            dispositions = []
        topic_map: dict[str, dict[str, Any]] = {}
        for topic_index, item in enumerate(dispositions):
            topic_label = f"{label}.topic_dispositions[{topic_index}]"
            if not isinstance(item, dict) or not _nonempty_string(item.get("topic")):
                errors.append(f"{topic_label}.topic must be non-empty")
                continue
            topic = item["topic"]
            if topic in topic_map:
                errors.append(f"{label}.topic_dispositions repeats {topic!r}")
            topic_map[topic] = item
            if item.get("disposition") not in VALID_TOPIC_DISPOSITIONS:
                errors.append(f"{topic_label}.disposition is invalid")
            ids = item.get("finding_ids")
            if not _string_list(ids):
                errors.append(f"{topic_label}.finding_ids must be a list of strings")
                ids = []
            unknown = sorted(set(ids) - local_finding_ids)
            if unknown:
                errors.append(f"{topic_label} references unknown findings: {', '.join(unknown)}")
            if item.get("disposition") == "analyzed" and not ids:
                errors.append(f"{topic_label}: analyzed topics require findings")
            if item.get("disposition") != "analyzed" and not _nonempty_string(
                item.get("reason")
            ):
                errors.append(f"{topic_label}.reason is required for non-analyzed topics")
        if set(topic_map) != set(lane.get("required_topics", [])):
            errors.append(f"{label}.topic_dispositions must exactly cover required topics")

        for list_name in ("control_requirements", "omission_checks", "handoffs"):
            if not isinstance(report.get(list_name), list):
                errors.append(f"{label}.{list_name} must be a list")
        conflicts = report.get("conflicts")
        if not isinstance(conflicts, list):
            errors.append(f"{label}.conflicts must be a list")
            conflicts = []
        for conflict_index, conflict in enumerate(conflicts):
            conflict_label = f"{label}.conflicts[{conflict_index}]"
            if not isinstance(conflict, dict) or not _nonempty_string(conflict.get("id")):
                errors.append(f"{conflict_label}.id must be non-empty")
                continue
            conflict_id = str(conflict["id"])
            if conflict_id in conflict_ids:
                errors.append(f"duplicate conflict id: {conflict_id}")
            conflict_ids.add(conflict_id)
            if not _nonempty_string(conflict.get("owner_key")):
                errors.append(f"{conflict_label}.owner_key must be non-empty")
            if not _string_list(conflict.get("source_evidence"), nonempty=True):
                errors.append(f"{conflict_label}.source_evidence must be non-empty")

    required_lane_ids = set(route.get("required_lane_ids", []))
    if report_lane_ids != required_lane_ids:
        errors.append("lane_reports must contain exactly one report for every required lane")
    if execution_mode == "mixed" and report_modes_seen != VALID_REPORT_MODES:
        errors.append("mixed execution must contain delegated and sequential reports")

    integration = bundle.get("integration")
    if not isinstance(integration, dict):
        errors.append("integration must be an object")
        integration_status = ""
        finding_dispositions: list[Any] = []
        obligation_dispositions: list[Any] = []
        integrated_conflicts: list[Any] = []
    else:
        integration_status = integration.get("status")
        if integration_status not in VALID_INTEGRATION_STATUS:
            errors.append("integration.status is invalid")
        finding_dispositions = integration.get("finding_dispositions")
        if not isinstance(finding_dispositions, list):
            errors.append("integration.finding_dispositions must be a list")
            finding_dispositions = []
        obligation_dispositions = integration.get("obligation_dispositions")
        if not isinstance(obligation_dispositions, list):
            errors.append("integration.obligation_dispositions must be a list")
            obligation_dispositions = []
        integrated_conflicts = integration.get("conflicts")
        if not isinstance(integrated_conflicts, list):
            errors.append("integration.conflicts must be a list")
            integrated_conflicts = []

    disposed_findings: dict[str, int] = {}
    for index, disposition in enumerate(finding_dispositions):
        label = f"integration.finding_dispositions[{index}]"
        if not isinstance(disposition, dict):
            errors.append(f"{label} must be an object")
            continue
        ids = disposition.get("finding_ids")
        if not _string_list(ids, nonempty=True):
            errors.append(f"{label}.finding_ids must be non-empty")
            ids = []
        unknown = sorted(set(ids) - set(finding_map))
        if unknown:
            errors.append(f"{label} references unknown findings: {', '.join(unknown)}")
        for finding_id in ids:
            disposed_findings[finding_id] = disposed_findings.get(finding_id, 0) + 1
        status = disposition.get("disposition")
        if status not in VALID_FINDING_DISPOSITIONS:
            errors.append(f"{label}.disposition is invalid")
        if status in {"rejected", "uncertain", "diagnostic-only"} and not _nonempty_string(
            disposition.get("reason")
        ):
            errors.append(f"{label}.reason is required for {status!r}")
        material_primary = any(
            finding_map.get(finding_id, {}).get("materiality") == "material"
            and finding_map.get(finding_id, {}).get("proposed_role") == "primary"
            for finding_id in ids
        )
        if material_primary:
            if status not in {"retained", "merged"}:
                errors.append(f"{label}: a material primary finding cannot be dropped")
            if disposition.get("final_role") != "primary":
                errors.append(f"{label}: a material primary finding cannot be demoted")
            if not _nonempty_string(disposition.get("final_invariant_id")):
                errors.append(f"{label}: a material primary finding needs a final invariant")
        if status in {"retained", "merged"}:
            if disposition.get("final_role") not in VALID_ROLES:
                errors.append(f"{label}.final_role is invalid")
            final_invariant_id = disposition.get("final_invariant_id")
            if not _nonempty_string(final_invariant_id):
                errors.append(f"{label}.final_invariant_id must be non-empty")
            elif final_invariant_id not in plan_invariant_map:
                errors.append(
                    f"{label}.final_invariant_id is absent from the integrated plan"
                )
            elif plan_invariant_map[str(final_invariant_id)].get("role") != disposition.get(
                "final_role"
            ):
                errors.append(
                    f"{label}.final_role does not match the integrated plan invariant"
                )

    missing_findings = sorted(set(finding_map) - set(disposed_findings))
    repeated_findings = sorted(
        finding_id for finding_id, count in disposed_findings.items() if count != 1
    )
    if missing_findings:
        errors.append("integration omits findings: " + ", ".join(missing_findings))
    if repeated_findings:
        errors.append("integration disposes findings more than once: " + ", ".join(repeated_findings))

    disposed_obligations: dict[str, int] = {}
    for index, disposition in enumerate(obligation_dispositions):
        label = f"integration.obligation_dispositions[{index}]"
        if not isinstance(disposition, dict):
            errors.append(f"{label} must be an object")
            continue
        ids = disposition.get("obligation_ids")
        if not _string_list(ids, nonempty=True):
            errors.append(f"{label}.obligation_ids must be non-empty")
            ids = []
        unknown = sorted(set(ids) - set(obligation_map))
        if unknown:
            errors.append(
                f"{label} references unknown obligations: {', '.join(unknown)}"
            )
        for obligation_id in ids:
            disposed_obligations[obligation_id] = (
                disposed_obligations.get(obligation_id, 0) + 1
            )
        status = disposition.get("disposition")
        if status not in VALID_OBLIGATION_DISPOSITIONS:
            errors.append(f"{label}.disposition is invalid")
        if status in {"rejected", "uncertain", "diagnostic-only"} and not _nonempty_string(
            disposition.get("reason")
        ):
            errors.append(f"{label}.reason is required for {status!r}")

        material = any(
            obligation_map.get(obligation_id, {}).get("materiality") == "material"
            for obligation_id in ids
        )
        primary = any(
            obligation_map.get(obligation_id, {}).get("materiality") == "material"
            and obligation_map.get(obligation_id, {}).get("proposed_role") == "primary"
            for obligation_id in ids
        )
        if material and status not in {"retained", "merged"}:
            errors.append(f"{label}: a material atomic obligation cannot be dropped")
        if primary and disposition.get("final_role") != "primary":
            errors.append(f"{label}: a primary atomic obligation cannot be demoted")
        if status in {"retained", "merged"}:
            if disposition.get("final_role") not in VALID_ROLES:
                errors.append(f"{label}.final_role is invalid")
            final_invariant_id = disposition.get("final_invariant_id")
            if not _nonempty_string(final_invariant_id):
                errors.append(f"{label}.final_invariant_id must be non-empty")
            elif final_invariant_id not in plan_invariant_map:
                errors.append(
                    f"{label}.final_invariant_id is absent from the integrated plan"
                )
            else:
                invariant = plan_invariant_map[str(final_invariant_id)]
                if invariant.get("role") != disposition.get("final_role"):
                    errors.append(
                        f"{label}.final_role does not match the integrated plan invariant"
                    )
                bound_ids = invariant.get("source_obligation_ids")
                if not _string_list(bound_ids, nonempty=True):
                    errors.append(
                        f"integrated plan invariant {final_invariant_id!r} must bind source_obligation_ids"
                    )
                elif not set(ids).issubset(set(bound_ids)):
                    errors.append(
                        f"{label}.obligation_ids must survive in the integrated plan invariant"
                    )

    missing_obligations = sorted(set(obligation_map) - set(disposed_obligations))
    repeated_obligations = sorted(
        obligation_id
        for obligation_id, count in disposed_obligations.items()
        if count != 1
    )
    if missing_obligations:
        errors.append(
            "integration omits atomic obligations: " + ", ".join(missing_obligations)
        )
    if repeated_obligations:
        errors.append(
            "integration disposes atomic obligations more than once: "
            + ", ".join(repeated_obligations)
        )

    for invariant_id, invariant in plan_invariant_map.items():
        source_obligation_ids = invariant.get("source_obligation_ids", [])
        if not _string_list(source_obligation_ids):
            errors.append(
                f"integrated plan invariant {invariant_id!r}.source_obligation_ids must be a list"
            )
            continue
        unknown = sorted(set(source_obligation_ids) - set(obligation_map))
        if unknown:
            errors.append(
                f"integrated plan invariant {invariant_id!r} references unknown atomic obligations: "
                + ", ".join(unknown)
            )

    adjudications = bundle.get("adjudications")
    if not isinstance(adjudications, list):
        errors.append("adjudications must be a list")
        adjudications = []
    adjudication_map: dict[str, dict[str, Any]] = {}
    for index, adjudication in enumerate(adjudications):
        label = f"adjudications[{index}]"
        if not isinstance(adjudication, dict) or not _nonempty_string(adjudication.get("id")):
            errors.append(f"{label}.id must be non-empty")
            continue
        adjudication_id = str(adjudication["id"])
        if adjudication_id in adjudication_map:
            errors.append(f"duplicate adjudication id: {adjudication_id}")
        adjudication_map[adjudication_id] = adjudication
        if adjudication.get("status") not in {"resolved", "uncertain"}:
            errors.append(f"{label}.status is invalid")
        if adjudication.get("independent_context") is not True:
            errors.append(f"{label}.independent_context must be true")
        if not _string_list(adjudication.get("source_evidence"), nonempty=True):
            errors.append(f"{label}.source_evidence must be non-empty")

    integrated_conflict_ids: set[str] = set()
    for index, conflict in enumerate(integrated_conflicts):
        label = f"integration.conflicts[{index}]"
        if not isinstance(conflict, dict) or conflict.get("id") not in conflict_ids:
            errors.append(f"{label}.id must reference a reported conflict")
            continue
        conflict_id = str(conflict["id"])
        if conflict_id in integrated_conflict_ids:
            errors.append(f"integration repeats conflict {conflict_id!r}")
        integrated_conflict_ids.add(conflict_id)
        resolution = conflict.get("resolution")
        if resolution not in VALID_CONFLICT_RESOLUTIONS:
            errors.append(f"{label}.resolution is invalid")
        if resolution == "automatic" and not _nonempty_string(conflict.get("reason")):
            errors.append(f"{label}.reason is required for automatic resolution")
        if resolution in {"adjudicated", "uncertain"}:
            adjudication_id = conflict.get("adjudication_id")
            if adjudication_id not in adjudication_map:
                errors.append(f"{label}.adjudication_id is required")
            elif resolution == "adjudicated" and adjudication_map[adjudication_id].get(
                "status"
            ) != "resolved":
                errors.append(f"{label} requires a resolved adjudication")
    if integrated_conflict_ids != conflict_ids:
        errors.append("integration must dispose every reported conflict exactly once")

    review = bundle.get("coverage_review")
    if not isinstance(review, dict):
        errors.append("coverage_review must be an object")
        critic_status = ""
    else:
        reviewer_context = review.get("reviewer_context")
        if reviewer_context not in {"independent", "same-context"}:
            errors.append("coverage_review.reviewer_context is invalid")
        if execution_mode == "delegated" and reviewer_context != "independent":
            errors.append("delegated analysis requires an independent coverage reviewer")
        if prompt_frozen and reviewer_context != "independent":
            errors.append("prompt freeze requires an independent coverage reviewer")
        if review.get("source_sha256") != source_sha:
            errors.append("coverage_review.source_sha256 does not match the bundle")
        if review.get("route_fingerprint") != route_fingerprint:
            errors.append("coverage_review.route_fingerprint does not match the route")
        if review.get("integrated_plan_sha256") != plan_sha:
            errors.append(
                "coverage_review.integrated_plan_sha256 does not match the integrated plan"
            )
        reviewed_finding_ids = review.get("reviewed_finding_ids")
        if not _string_list(reviewed_finding_ids):
            errors.append("coverage_review.reviewed_finding_ids must be a list")
            reviewed_finding_ids = []
        if set(reviewed_finding_ids) != set(finding_map):
            errors.append("coverage_review must inspect every lane finding exactly once")
        elif len(reviewed_finding_ids) != len(set(reviewed_finding_ids)):
            errors.append("coverage_review.reviewed_finding_ids contains duplicates")
        reviewed_obligation_ids = review.get("reviewed_obligation_ids")
        if not _string_list(reviewed_obligation_ids):
            errors.append("coverage_review.reviewed_obligation_ids must be a list")
            reviewed_obligation_ids = []
        if set(reviewed_obligation_ids) != set(obligation_map):
            errors.append(
                "coverage_review must inspect every atomic obligation exactly once"
            )
        elif len(reviewed_obligation_ids) != len(set(reviewed_obligation_ids)):
            errors.append("coverage_review.reviewed_obligation_ids contains duplicates")
        reviewed_invariant_ids = review.get("reviewed_invariant_ids")
        if not _string_list(reviewed_invariant_ids):
            errors.append("coverage_review.reviewed_invariant_ids must be a list")
            reviewed_invariant_ids = []
        if set(reviewed_invariant_ids) != set(plan_invariant_map):
            errors.append(
                "coverage_review must inspect every integrated plan invariant exactly once"
            )
        elif len(reviewed_invariant_ids) != len(set(reviewed_invariant_ids)):
            errors.append("coverage_review.reviewed_invariant_ids contains duplicates")
        critic_status = review.get("status")
        if critic_status not in VALID_CRITIC_STATUS:
            errors.append("coverage_review.status is invalid")
        issues = review.get("issues")
        if not isinstance(issues, list):
            errors.append("coverage_review.issues must be a list")
            issues = []
        for index, issue in enumerate(issues):
            label = f"coverage_review.issues[{index}]"
            if not isinstance(issue, dict) or issue.get("kind") not in VALID_CRITIC_ISSUES:
                errors.append(f"{label}.kind is invalid")
            elif not _nonempty_string(issue.get("evidence")):
                errors.append(f"{label}.evidence must be non-empty")
        if critic_status == "pass" and issues:
            errors.append("coverage_review cannot pass with material issues")
        if critic_status in {"revise-route", "revise-integration", "blocked"} and not issues:
            errors.append("a non-pass coverage review requires at least one issue")

    if (
        execution_mode == "sequential-fallback"
        and isinstance(execution, dict)
        and execution.get("independence_claimed") is True
    ):
        errors.append("sequential fallback cannot claim independent analysis")
    if (
        execution_mode == "mixed"
        and isinstance(execution, dict)
        and execution.get("independence_claimed") is True
        and non_independent_report_seen
    ):
        errors.append("mixed execution with fallback reports cannot claim independence")
    if integration_status == "complete" and any(
        isinstance(report, dict) and report.get("status") == "blocked"
        for report in reports
    ):
        errors.append("integration cannot be complete while a required lane is blocked")
    if prompt_frozen and (
        integration_status != "complete" or critic_status != "pass" or errors
    ):
        errors.append("the prompt cannot freeze before complete integration and critic pass")
    return errors


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle", help=f"{BUNDLE_SCHEMA} JSON")
    args = parser.parse_args(argv)
    try:
        payload = json.loads(Path(args.bundle).read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise TypeError("bundle root must be an object")
        errors = validate_bundle(payload)
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        errors = [str(exc)]
    if errors:
        print(json.dumps({"status": "failed", "errors": errors}, indent=2))
        return 1
    print(json.dumps({"status": "ok"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
