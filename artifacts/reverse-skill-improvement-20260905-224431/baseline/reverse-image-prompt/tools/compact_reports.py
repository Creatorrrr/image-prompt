#!/usr/bin/env python3
"""Validate compact lane reports and close material cross-lane handoffs.

This checker proves structural coverage only. It cannot decide whether a source
image was interpreted correctly or whether a downstream render is faithful.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from module_metadata import ROOT, load_manifest, module_map
from route_resolver import resolve_analysis_route


SET_SCHEMA = "reverse-image-analysis-compact-set/v2"
REPORT_SCHEMA = "reverse-image-analysis-lane-report/compact-v2"
VALID_REPORT_STATUS = {"complete", "uncertain", "blocked"}
VALID_REPORT_MODES = {"delegated", "sequential-fallback"}
VALID_PRIORITIES = {"P0", "P1"}
VALID_CONFIDENCE = {"high", "medium", "low"}
VALID_DRIFT_RISK = {"high", "medium", "low", "uncertain"}
VALID_REPRESENTATIONS = {"atomic", "macro-summary"}
VALID_ADEQUACY = {"sufficient", "lossy", "uncertain"}


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: Any, *, nonempty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (bool(value) or not nonempty)
        and all(_nonempty_string(item) for item in value)
    )


def _validate_route(
    route: Any, manifest: dict[str, Any]
) -> tuple[list[str], dict[str, Any]]:
    if not isinstance(route, dict):
        return ["route must be an object"], {}
    facets = route.get("normalized_facets")
    if not isinstance(facets, dict):
        return ["route.normalized_facets must be an object"], route
    try:
        expected = resolve_analysis_route(
            facets,
            manifest,
            analysis_profile="prompt",
        )
    except (KeyError, TypeError, ValueError) as exc:
        return [f"route cannot be reconstructed: {exc}"], route
    errors: list[str] = []
    if route != expected:
        errors.append("route must exactly match the deterministic prompt route")
    return errors, expected


def validate_compact_set(
    compact_set: Any, manifest: dict[str, Any] | None = None
) -> list[str]:
    """Return structural errors for a compact report set."""

    manifest = manifest or load_manifest(ROOT)
    if not isinstance(compact_set, dict):
        return ["$ must be an object"]

    errors: list[str] = []
    if compact_set.get("schema_version") != SET_SCHEMA:
        errors.append(f"schema_version must be {SET_SCHEMA!r}")

    source = compact_set.get("source_artifact")
    if not isinstance(source, dict):
        errors.append("source_artifact must be an object")
        source_sha = ""
        source_frame = ""
    else:
        source_sha = source.get("sha256", "")
        source_frame = source.get("frame", "")
        if not isinstance(source_sha, str) or re.fullmatch(
            r"[0-9a-f]{64}", source_sha
        ) is None:
            errors.append("source_artifact.sha256 must be a lowercase SHA-256")
        if not _nonempty_string(source_frame):
            errors.append("source_artifact.frame must be non-empty")

    route_errors, route = _validate_route(compact_set.get("route"), manifest)
    errors.extend(route_errors)
    if route.get("analysis_profile") != "prompt":
        errors.append("route.analysis_profile must be 'prompt'")
    route_fingerprint = route.get("route_fingerprint", "")
    route_lanes = {
        lane.get("id"): lane
        for lane in route.get("lanes", [])
        if isinstance(lane, dict) and _nonempty_string(lane.get("id"))
    }
    modules = module_map(manifest)

    reports = compact_set.get("lane_reports")
    if not isinstance(reports, list):
        errors.append("lane_reports must be a list")
        reports = []

    report_lane_ids: set[str] = set()
    for report_index, report in enumerate(reports):
        label = f"lane_reports[{report_index}]"
        if not isinstance(report, dict):
            errors.append(f"{label} must be an object")
            continue
        if report.get("schema_version") != REPORT_SCHEMA:
            errors.append(f"{label}.schema_version must be {REPORT_SCHEMA!r}")

        lane_id = report.get("lane_id")
        if lane_id not in route_lanes:
            errors.append(f"{label}.lane_id is not required by the route")
            continue
        lane_id = str(lane_id)
        if lane_id in report_lane_ids:
            errors.append(f"duplicate lane report: {lane_id}")
        report_lane_ids.add(lane_id)
        lane = route_lanes[lane_id]

        if report.get("route_fingerprint") != route_fingerprint:
            errors.append(f"{label}.route_fingerprint does not match the route")
        report_source = report.get("source_artifact")
        if not isinstance(report_source, dict):
            errors.append(f"{label}.source_artifact must be an object")
        else:
            if report_source.get("sha256") != source_sha:
                errors.append(f"{label}.source_artifact.sha256 does not match the set")
            if report_source.get("frame") != source_frame:
                errors.append(f"{label}.source_artifact.frame does not match the set")

        execution = report.get("execution")
        if not isinstance(execution, dict):
            errors.append(f"{label}.execution must be an object")
        else:
            mode = execution.get("mode")
            independent = execution.get("independent_context")
            if mode not in VALID_REPORT_MODES:
                errors.append(f"{label}.execution.mode is invalid")
            if not isinstance(independent, bool):
                errors.append(f"{label}.execution.independent_context must be boolean")
            if mode == "delegated" and independent is not True:
                errors.append(f"{label}: delegated reports require independent context")
            if mode == "sequential-fallback" and independent is not False:
                errors.append(f"{label}: sequential fallback must disclose dependence")

        if report.get("status") not in VALID_REPORT_STATUS:
            errors.append(f"{label}.status is invalid")
        if not _nonempty_string(report.get("primary_read")):
            errors.append(f"{label}.primary_read must be non-empty")

        reviewed = report.get("reviewed_modules")
        reviewed_versions: dict[str, Any] = {}
        if not isinstance(reviewed, list):
            errors.append(f"{label}.reviewed_modules must be a list")
            reviewed = []
        for item_index, item in enumerate(reviewed):
            item_label = f"{label}.reviewed_modules[{item_index}]"
            if not isinstance(item, dict) or not _nonempty_string(item.get("id")):
                errors.append(f"{item_label} must name a module")
                continue
            module_id = str(item["id"])
            if module_id in reviewed_versions:
                errors.append(f"{label}.reviewed_modules repeats {module_id!r}")
            reviewed_versions[module_id] = item.get("version")
        expected_modules = set(lane.get("module_ids", []))
        if set(reviewed_versions) != expected_modules:
            errors.append(f"{label}.reviewed_modules must exactly cover assigned modules")
        for module_id in expected_modules & set(reviewed_versions):
            if reviewed_versions[module_id] != modules[module_id].get("version"):
                errors.append(f"{label}.reviewed_modules has stale version for {module_id}")

        findings = report.get("material_findings")
        if not isinstance(findings, list):
            errors.append(f"{label}.material_findings must be a list")
            findings = []
        local_source_ids: set[str] = set()
        cross_lane_residuals: list[tuple[str, str]] = []
        for finding_index, finding in enumerate(findings):
            finding_label = f"{label}.material_findings[{finding_index}]"
            if not isinstance(finding, dict):
                errors.append(f"{finding_label} must be an object")
                continue
            finding_id = finding.get("id")
            if not _nonempty_string(finding_id) or not str(finding_id).startswith(
                f"{lane_id}:"
            ):
                errors.append(f"{finding_label}.id must use the lane namespace")
                continue
            finding_id = str(finding_id)
            if finding_id in local_source_ids:
                errors.append(f"duplicate compact source id: {finding_id}")
            local_source_ids.add(finding_id)

            if not _nonempty_string(finding.get("owner_key")):
                errors.append(f"{finding_label}.owner_key must be non-empty")
            if finding.get("viewer_priority") not in VALID_PRIORITIES:
                errors.append(f"{finding_label}.viewer_priority must be P0 or P1")
            representation = finding.get("representation")
            if representation not in VALID_REPRESENTATIONS:
                errors.append(f"{finding_label}.representation is invalid")
            if not _nonempty_string(finding.get("observation")):
                errors.append(f"{finding_label}.observation must be non-empty")
            if not _string_list(finding.get("source_evidence"), nonempty=True):
                errors.append(f"{finding_label}.source_evidence must be non-empty")
            if finding.get("confidence") not in VALID_CONFIDENCE:
                errors.append(f"{finding_label}.confidence is invalid")
            if not _nonempty_string(finding.get("change_counterfactual")):
                errors.append(f"{finding_label}.change_counterfactual must be non-empty")
            if finding.get("default_drift_risk") not in VALID_DRIFT_RISK:
                errors.append(f"{finding_label}.default_drift_risk is invalid")
            if not _nonempty_string(finding.get("control_requirement")):
                errors.append(f"{finding_label}.control_requirement must be non-empty")

            adequacy = finding.get("summary_adequacy")
            if representation == "atomic":
                if adequacy is not None:
                    errors.append(
                        f"{finding_label}.summary_adequacy is only for macro-summary findings"
                    )
                continue
            if representation != "macro-summary":
                continue
            if not isinstance(adequacy, dict):
                errors.append(
                    f"{finding_label}.summary_adequacy is required for macro-summary findings"
                )
                continue
            verdict = adequacy.get("verdict")
            if verdict not in VALID_ADEQUACY:
                errors.append(f"{finding_label}.summary_adequacy.verdict is invalid")
            residuals = adequacy.get("at_risk_relations")
            if not isinstance(residuals, list):
                errors.append(
                    f"{finding_label}.summary_adequacy.at_risk_relations must be a list"
                )
                residuals = []
            if verdict == "sufficient" and residuals:
                errors.append(
                    f"{finding_label}: a sufficient summary must not emit residual relations"
                )
            if verdict in {"lossy", "uncertain"} and not residuals:
                errors.append(
                    f"{finding_label}: a {verdict} summary requires at-risk relations"
                )
            for residual_index, residual in enumerate(residuals):
                residual_label = (
                    f"{finding_label}.summary_adequacy.at_risk_relations[{residual_index}]"
                )
                if not isinstance(residual, dict):
                    errors.append(f"{residual_label} must be an object")
                    continue
                residual_id = residual.get("id")
                if not _nonempty_string(residual_id) or not str(residual_id).startswith(
                    f"{finding_id}:"
                ):
                    errors.append(f"{residual_label}.id must use the finding namespace")
                    continue
                residual_id = str(residual_id)
                if residual_id in local_source_ids:
                    errors.append(f"duplicate compact source id: {residual_id}")
                local_source_ids.add(residual_id)
                if not _string_list(
                    residual.get("subject_or_region_ids"), nonempty=True
                ):
                    errors.append(
                        f"{residual_label}.subject_or_region_ids must be non-empty"
                    )
                if not _nonempty_string(residual.get("relation_kind")):
                    errors.append(f"{residual_label}.relation_kind must be non-empty")
                if not _nonempty_string(residual.get("visible_result")):
                    errors.append(f"{residual_label}.visible_result must be non-empty")
                if not _string_list(residual.get("source_evidence"), nonempty=True):
                    errors.append(f"{residual_label}.source_evidence must be non-empty")
                if residual.get("confidence") not in VALID_CONFIDENCE:
                    errors.append(f"{residual_label}.confidence is invalid")
                if not _nonempty_string(residual.get("control_requirement")):
                    errors.append(f"{residual_label}.control_requirement must be non-empty")
                owner_lane = residual.get("causal_owner_lane")
                if not _nonempty_string(owner_lane):
                    errors.append(f"{residual_label}.causal_owner_lane must be non-empty")
                elif owner_lane not in route_lanes:
                    errors.append(
                        f"route-gap: {residual_label} requires absent lane {owner_lane!r}"
                    )
                elif owner_lane != lane_id:
                    cross_lane_residuals.append((residual_id, str(owner_lane)))
                if not _string_list(residual.get("dependencies", [])):
                    errors.append(f"{residual_label}.dependencies must be a list of strings")

        handoffs = report.get("handoffs")
        if not isinstance(handoffs, list):
            errors.append(f"{label}.handoffs must be a list")
            handoffs = []
        local_handoff_ids: set[str] = set()
        route_required_handoffs: list[dict[str, Any]] = []
        for handoff_index, handoff in enumerate(handoffs):
            handoff_label = f"{label}.handoffs[{handoff_index}]"
            if not isinstance(handoff, dict):
                errors.append(f"{handoff_label} must be an object")
                continue
            handoff_id = handoff.get("id")
            if not _nonempty_string(handoff_id) or not str(handoff_id).startswith(
                f"{lane_id}:"
            ):
                errors.append(f"{handoff_label}.id must use the lane namespace")
            elif handoff_id in local_handoff_ids:
                errors.append(f"duplicate handoff id: {handoff_id}")
            else:
                local_handoff_ids.add(str(handoff_id))
            source_ids = handoff.get("source_ids")
            if not _string_list(source_ids, nonempty=True):
                errors.append(f"{handoff_label}.source_ids must be non-empty")
                source_ids = []
            unknown = sorted(set(source_ids) - local_source_ids)
            if unknown:
                errors.append(
                    f"{handoff_label}.source_ids reference unknown ids: {', '.join(unknown)}"
                )
            if handoff.get("viewer_priority") not in VALID_PRIORITIES:
                errors.append(f"{handoff_label}.viewer_priority must be P0 or P1")
            if not _nonempty_string(handoff.get("target_lane")):
                errors.append(f"{handoff_label}.target_lane must be non-empty")
            if not _nonempty_string(handoff.get("reason")):
                errors.append(f"{handoff_label}.reason must be non-empty")
            route_required = handoff.get("route_required")
            if not isinstance(route_required, bool):
                errors.append(f"{handoff_label}.route_required must be boolean")
            if route_required is True:
                route_required_handoffs.append(handoff)
                target_lane = handoff.get("target_lane")
                required_module_id = handoff.get("required_module_id")
                if target_lane not in route_lanes:
                    errors.append(
                        f"route-gap: {handoff_label} targets absent lane {target_lane!r}"
                    )
                if not _nonempty_string(required_module_id):
                    errors.append(
                        f"{handoff_label}.required_module_id is required for a route handoff"
                    )
                elif target_lane in route_lanes and required_module_id not in set(
                    route_lanes[target_lane].get("module_ids", [])
                ):
                    errors.append(
                        f"route-gap: {handoff_label} requires module {required_module_id!r} "
                        f"outside target lane {target_lane!r}"
                    )

        for residual_id, owner_lane in cross_lane_residuals:
            if not any(
                residual_id in handoff.get("source_ids", [])
                and handoff.get("target_lane") == owner_lane
                and handoff.get("route_required") is True
                for handoff in route_required_handoffs
            ):
                errors.append(
                    f"route-gap: cross-lane residual {residual_id!r} lacks a closed "
                    f"P0/P1 handoff to {owner_lane!r}"
                )

        for list_name in (
            "supporting_findings",
            "grouped_non_material_topics",
            "uncertainties",
            "conflicts",
        ):
            if not isinstance(report.get(list_name), list):
                errors.append(f"{label}.{list_name} must be a list")
        escalation = report.get("escalation")
        if not isinstance(escalation, dict):
            errors.append(f"{label}.escalation must be an object")
        else:
            required = escalation.get("required")
            if not isinstance(required, bool):
                errors.append(f"{label}.escalation.required must be boolean")
            if required is True and not _nonempty_string(escalation.get("reason")):
                errors.append(f"{label}.escalation.reason is required when escalating")

    required_lane_ids = set(route.get("required_lane_ids", []))
    if report_lane_ids != required_lane_ids:
        errors.append("lane_reports must contain exactly one report for every required lane")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("compact_set", type=Path)
    args = parser.parse_args(argv)
    try:
        payload = json.loads(args.compact_set.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "errors": [str(exc)]}, indent=2))
        return 2
    errors = validate_compact_set(payload)
    print(
        json.dumps(
            {"status": "ok" if not errors else "error", "errors": errors},
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
