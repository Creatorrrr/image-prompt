#!/usr/bin/env python3
"""Validate an image-prompt skill improvement iteration record."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = "image-prompt-skill-improvement/v1"

EVIDENCE_KINDS = {
    "source-observation",
    "user-judgment",
    "prompt-inspection",
    "prompt-evaluation",
    "package-check",
    "render-observation",
    "generation-outcome",
    "repository-history",
    "measurement",
    "external-research",
}
CLAIM_SCOPES = {
    "structural",
    "prompt-behavior",
    "render-fidelity",
    "user-aesthetic",
}
HYPOTHESIS_STAGES = {
    "observation",
    "representation",
    "prompt-priority",
    "prompt-interaction",
    "generator-response",
    "sampling",
    "external",
    "user-contract",
}
INTERVENTION_STATUSES = {"none", "proposed", "implemented"}
TARGET_LAYERS = {"entrypoint", "module", "reference", "policy", "tool", "test"}
EVALUATION_STATUSES = {"not-run", "pass", "fail", "blocked", "unscored"}
HOLDOUT_STATUSES = {"pass", "fail", "blocked", "unscored"}
DECISION_STATUSES = {
    "diagnosed",
    "proposed",
    "implemented",
    "promote",
    "revise",
    "reject",
    "blocked",
}
SCALES = {"global", "regional", "local"}

LAYER_EVIDENCE = {
    "package": "package-check",
    "prompt": "prompt-evaluation",
    "render": "render-observation",
    "user": "user-judgment",
}

PROMOTION_LAYERS = {
    "structural": ("package",),
    "prompt-behavior": ("package", "prompt"),
    "render-fidelity": ("package", "prompt", "render"),
    "user-aesthetic": ("package", "prompt", "render", "user"),
}


def _is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _require_mapping(value: Any, path: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{path} must be an object")
        return {}
    return value


def _require_list(value: Any, path: str, errors: list[str]) -> list[Any]:
    if not isinstance(value, list):
        errors.append(f"{path} must be an array")
        return []
    return value


def _require_text(
    mapping: dict[str, Any], key: str, path: str, errors: list[str]
) -> str:
    value = mapping.get(key)
    if not _is_nonempty_string(value):
        errors.append(f"{path}.{key} must be a non-empty string")
        return ""
    return value.strip()


def _check_choice(
    value: Any,
    choices: set[str],
    path: str,
    errors: list[str],
) -> str:
    if value not in choices:
        errors.append(f"{path} must be one of {sorted(choices)}")
        return ""
    return str(value)


def _check_unique_id(
    item: dict[str, Any],
    path: str,
    seen: set[str],
    errors: list[str],
) -> str:
    item_id = _require_text(item, "id", path, errors)
    if item_id:
        if item_id in seen:
            errors.append(f"{path}.id duplicates {item_id!r}")
        seen.add(item_id)
    return item_id


def _check_references(
    raw_ids: Any,
    valid_ids: set[str],
    path: str,
    errors: list[str],
    *,
    require_nonempty: bool,
) -> list[str]:
    values = _require_list(raw_ids, path, errors)
    refs: list[str] = []
    for index, value in enumerate(values):
        if not _is_nonempty_string(value):
            errors.append(f"{path}[{index}] must be a non-empty string")
            continue
        ref = value.strip()
        refs.append(ref)
        if ref not in valid_ids:
            errors.append(f"{path}[{index}] references unknown id {ref!r}")
    if require_nonempty and not refs:
        errors.append(f"{path} must contain at least one id")
    if len(refs) != len(set(refs)):
        errors.append(f"{path} must not contain duplicate ids")
    return refs


def _evidence_has_kind(
    evidence_by_id: dict[str, dict[str, Any]],
    refs: Iterable[str],
    required_kind: str,
) -> bool:
    return any(evidence_by_id.get(ref, {}).get("kind") == required_kind for ref in refs)


def validate_record(record: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(record, dict):
        return ["$ must be an object"]
    root = record

    if root.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"$.schema_version must equal {SCHEMA_VERSION!r}")

    target = _require_mapping(root.get("target"), "$.target", errors)
    _require_text(target, "skill_path", "$.target", errors)
    _require_text(target, "baseline_revision", "$.target", errors)
    candidate_revision = target.get("candidate_revision")
    if candidate_revision is not None and not _is_nonempty_string(candidate_revision):
        errors.append("$.target.candidate_revision must be null or a non-empty string")

    goal = _require_mapping(root.get("goal"), "$.goal", errors)
    goal_scope = _check_choice(
        goal.get("claim_scope"), CLAIM_SCOPES, "$.goal.claim_scope", errors
    )
    _require_text(goal, "request", "$.goal", errors)

    evidence_items = _require_list(root.get("evidence"), "$.evidence", errors)
    evidence_ids: set[str] = set()
    evidence_by_id: dict[str, dict[str, Any]] = {}
    for index, raw_item in enumerate(evidence_items):
        path = f"$.evidence[{index}]"
        item = _require_mapping(raw_item, path, errors)
        item_id = _check_unique_id(item, path, evidence_ids, errors)
        _check_choice(item.get("kind"), EVIDENCE_KINDS, f"{path}.kind", errors)
        _require_text(item, "claim", path, errors)
        _require_text(item, "artifact", path, errors)
        if item_id:
            evidence_by_id[item_id] = item
    if not evidence_items:
        errors.append("$.evidence must contain at least one item")

    contract = _require_mapping(
        root.get("perceptual_contract"), "$.perceptual_contract", errors
    )
    _require_text(
        contract, "primary_success_condition", "$.perceptual_contract", errors
    )
    user_appeal = contract.get("user_appeal")
    if user_appeal is not None and not _is_nonempty_string(user_appeal):
        errors.append(
            "$.perceptual_contract.user_appeal must be null or a non-empty string"
        )
    if _is_nonempty_string(user_appeal) and not any(
        item.get("kind") == "user-judgment" for item in evidence_by_id.values()
    ):
        errors.append(
            "$.perceptual_contract.user_appeal needs at least one user-judgment evidence item"
        )

    invariant_items = _require_list(
        contract.get("invariants"), "$.perceptual_contract.invariants", errors
    )
    invariant_ids: set[str] = set()
    for index, raw_item in enumerate(invariant_items):
        path = f"$.perceptual_contract.invariants[{index}]"
        item = _require_mapping(raw_item, path, errors)
        _check_unique_id(item, path, invariant_ids, errors)
        _require_text(item, "statement", path, errors)
        _check_references(
            item.get("evidence_ids"),
            evidence_ids,
            f"{path}.evidence_ids",
            errors,
            require_nonempty=True,
        )
        controls = _require_list(
            item.get("causal_controls"), f"{path}.causal_controls", errors
        )
        if not controls or any(not _is_nonempty_string(value) for value in controls):
            errors.append(f"{path}.causal_controls must contain non-empty strings")
    if not invariant_items:
        errors.append("$.perceptual_contract.invariants must contain at least one item")

    flexible = _require_list(
        contract.get("flexible_dimensions"),
        "$.perceptual_contract.flexible_dimensions",
        errors,
    )
    if any(not _is_nonempty_string(value) for value in flexible):
        errors.append(
            "$.perceptual_contract.flexible_dimensions must contain only non-empty strings"
        )

    mismatch_items = _require_list(root.get("mismatches"), "$.mismatches", errors)
    mismatch_ids: set[str] = set()
    for index, raw_item in enumerate(mismatch_items):
        path = f"$.mismatches[{index}]"
        item = _require_mapping(raw_item, path, errors)
        _check_unique_id(item, path, mismatch_ids, errors)
        _check_choice(item.get("scale"), SCALES, f"{path}.scale", errors)
        _require_text(item, "axis", path, errors)
        _require_text(item, "source_state", path, errors)
        _require_text(item, "render_state", path, errors)
        _check_references(
            item.get("evidence_ids"),
            evidence_ids,
            f"{path}.evidence_ids",
            errors,
            require_nonempty=True,
        )

    hypothesis_items = _require_list(root.get("hypotheses"), "$.hypotheses", errors)
    hypothesis_ids: set[str] = set()
    for index, raw_item in enumerate(hypothesis_items):
        path = f"$.hypotheses[{index}]"
        item = _require_mapping(raw_item, path, errors)
        _check_unique_id(item, path, hypothesis_ids, errors)
        stage = _check_choice(
            item.get("stage"), HYPOTHESIS_STAGES, f"{path}.stage", errors
        )
        _require_text(item, "statement", path, errors)
        refs = _check_references(
            item.get("evidence_ids"),
            evidence_ids,
            f"{path}.evidence_ids",
            errors,
            require_nonempty=True,
        )
        _require_text(item, "falsifier", path, errors)
        if stage in {"generator-response", "sampling", "external"} and not any(
            _evidence_has_kind(evidence_by_id, refs, kind)
            for kind in ("render-observation", "generation-outcome")
        ):
            errors.append(
                f"{path} stage {stage!r} needs render-observation or generation-outcome evidence"
            )

    intervention = _require_mapping(root.get("intervention"), "$.intervention", errors)
    intervention_status = _check_choice(
        intervention.get("status"),
        INTERVENTION_STATUSES,
        "$.intervention.status",
        errors,
    )
    target_layers = _require_list(
        intervention.get("target_layers"), "$.intervention.target_layers", errors
    )
    for index, value in enumerate(target_layers):
        _check_choice(
            value, TARGET_LAYERS, f"$.intervention.target_layers[{index}]", errors
        )
    if intervention_status != "none" and not target_layers:
        errors.append(
            "$.intervention.target_layers must be non-empty for a proposed or implemented intervention"
        )
    _require_text(intervention, "general_rule", "$.intervention", errors)
    _require_text(intervention, "generalization_basis", "$.intervention", errors)
    _check_references(
        intervention.get("hypothesis_ids"),
        hypothesis_ids,
        "$.intervention.hypothesis_ids",
        errors,
        require_nonempty=intervention_status != "none",
    )
    changed_paths = _require_list(
        intervention.get("changed_paths"), "$.intervention.changed_paths", errors
    )
    if any(not _is_nonempty_string(value) for value in changed_paths):
        errors.append(
            "$.intervention.changed_paths must contain only non-empty strings"
        )
    if intervention_status == "implemented" and not changed_paths:
        errors.append(
            "$.intervention.changed_paths must be non-empty for an implemented intervention"
        )
    leaked_defaults = _require_list(
        intervention.get("case_specific_runtime_defaults"),
        "$.intervention.case_specific_runtime_defaults",
        errors,
    )
    if leaked_defaults:
        errors.append("$.intervention.case_specific_runtime_defaults must remain empty")

    evaluation = _require_mapping(root.get("evaluation"), "$.evaluation", errors)
    layer_results: dict[str, tuple[str, list[str]]] = {}
    for layer, required_kind in LAYER_EVIDENCE.items():
        result = _require_mapping(
            evaluation.get(layer), f"$.evaluation.{layer}", errors
        )
        status = _check_choice(
            result.get("status"),
            EVALUATION_STATUSES,
            f"$.evaluation.{layer}.status",
            errors,
        )
        refs = _check_references(
            result.get("evidence_ids"),
            evidence_ids,
            f"$.evaluation.{layer}.evidence_ids",
            errors,
            require_nonempty=status in {"pass", "fail", "blocked"},
        )
        if status in {"pass", "fail"} and not _evidence_has_kind(
            evidence_by_id, refs, required_kind
        ):
            errors.append(
                f"$.evaluation.{layer} status {status!r} needs {required_kind!r} evidence"
            )
        layer_results[layer] = (status, refs)

    holdout_items = _require_list(
        evaluation.get("holdouts"), "$.evaluation.holdouts", errors
    )
    holdout_ids: set[str] = set()
    passing_heldout_refs: list[list[str]] = []
    for index, raw_item in enumerate(holdout_items):
        path = f"$.evaluation.holdouts[{index}]"
        item = _require_mapping(raw_item, path, errors)
        _check_unique_id(item, path, holdout_ids, errors)
        role = _check_choice(
            item.get("case_role"),
            {"motivating", "held-out"},
            f"{path}.case_role",
            errors,
        )
        status = _check_choice(
            item.get("status"), HOLDOUT_STATUSES, f"{path}.status", errors
        )
        covered_axes = _require_list(
            item.get("covered_axes"), f"{path}.covered_axes", errors
        )
        if not covered_axes or any(
            not _is_nonempty_string(value) for value in covered_axes
        ):
            errors.append(f"{path}.covered_axes must contain non-empty strings")
        refs = _check_references(
            item.get("evidence_ids"),
            evidence_ids,
            f"{path}.evidence_ids",
            errors,
            require_nonempty=status in {"pass", "fail"},
        )
        if role == "held-out" and status == "pass":
            passing_heldout_refs.append(refs)

    decision = _require_mapping(root.get("decision"), "$.decision", errors)
    decision_status = _check_choice(
        decision.get("status"), DECISION_STATUSES, "$.decision.status", errors
    )
    decision_scope = _check_choice(
        decision.get("claim_scope"), CLAIM_SCOPES, "$.decision.claim_scope", errors
    )
    if goal_scope and decision_scope and goal_scope != decision_scope:
        errors.append("$.decision.claim_scope must equal $.goal.claim_scope")
    _require_text(decision, "rationale", "$.decision", errors)
    _check_references(
        decision.get("evidence_ids"),
        evidence_ids,
        "$.decision.evidence_ids",
        errors,
        require_nonempty=True,
    )

    if (
        decision_status in {"implemented", "promote"}
        and intervention_status != "implemented"
    ):
        errors.append(
            f"$.decision.status {decision_status!r} requires $.intervention.status 'implemented'"
        )

    if decision_status == "promote" and decision_scope:
        for layer in PROMOTION_LAYERS[decision_scope]:
            if layer_results.get(layer, ("", []))[0] != "pass":
                errors.append(
                    f"promotion with claim scope {decision_scope!r} requires "
                    f"$.evaluation.{layer}.status 'pass'"
                )
        if decision_scope != "structural":
            required_holdout_kind = (
                "prompt-evaluation"
                if decision_scope == "prompt-behavior"
                else "render-observation"
            )
            if not any(
                _evidence_has_kind(evidence_by_id, refs, required_holdout_kind)
                for refs in passing_heldout_refs
            ):
                errors.append(
                    f"promotion with claim scope {decision_scope!r} requires a passing "
                    f"held-out case with {required_holdout_kind!r} evidence"
                )
        if any(status == "fail" for status, _ in layer_results.values()):
            errors.append(
                "promotion is not allowed while an evaluation layer is 'fail'"
            )

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "record", type=Path, help="Path to an iteration-record JSON file"
    )
    args = parser.parse_args(argv)

    try:
        record = json.loads(args.record.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "errors": [str(exc)]}, indent=2))
        return 2

    errors = validate_record(record)
    result = {"status": "ok" if not errors else "error", "errors": errors}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
