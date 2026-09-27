"""Bind agent-authored body-action reviews; this module is not a pose solver.

No subject taxonomy, reference image, or prompt keyword selects an anatomy model.
The reviewer owns applicability and plausibility; code checks evidence, unresolved
findings, and exact input bindings. All helpers are post-core only.
"""
from __future__ import annotations

import copy
import hashlib
import json
from typing import Any

REVIEW_VERSION = "photo-embodiment-review/v1"
POLICY_VERSION = "photo-embodiment-preflight/v1"
CHECKS = (
    "body_ownership",
    "joint_chain_and_reach",
    "support_and_balance",
    "contact_and_space",
    "visibility_and_projection",
)
GATES = tuple(f"embodiment_{check}" for check in CHECKS)


def text_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_sha256(value: Any) -> str:
    return text_sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or len(value.strip()) < 12:
        raise ValueError(f"{label} requires a concrete explanation")
    return value


def validate_review(review: Any, prompt: str, core: dict, provenance: str) -> dict:
    fields = {"contract_version", "provenance", "prompt_sha256", "scope", "summary", "checks"}
    if not isinstance(review, dict) or set(review) != fields:
        raise ValueError("embodiment review requires exactly " + ", ".join(sorted(fields)))
    if review["contract_version"] != REVIEW_VERSION or review["provenance"] != provenance:
        raise ValueError("embodiment review version or authoring phase is incorrect")
    if review["prompt_sha256"] != text_sha256(prompt):
        raise ValueError("embodiment review is stale: review the exact current prompt again")
    _text(review["summary"], "embodiment summary")
    if not isinstance(review["scope"], str) or review["scope"] not in {"body_action", "not_applicable"}:
        raise ValueError("embodiment scope must be body_action or not_applicable")
    checks = review["checks"]
    if review["scope"] == "not_applicable":
        if checks != {}:
            raise ValueError("not_applicable scope requires empty checks and an explained summary")
        return copy.deepcopy(review)
    if not isinstance(checks, dict) or set(checks) != set(CHECKS):
        raise ValueError("body-action review must decide every generic check exactly once")
    spans = (core.get("request_binding") or {}).get("active_spans") or []
    for check, row in checks.items():
        required = {"status", "reason", "prompt_evidence"}
        if not isinstance(row, dict) or not required <= set(row) or set(row) - required - {"requester_source_text"}:
            raise ValueError(f"{check}: invalid review fields")
        _text(row["reason"], check)
        status = row["status"]
        if not isinstance(status, str):
            raise ValueError(f"{check}: review status must be a string")
        if status in {"needs_revision", "unresolved"}:
            raise ValueError(f"{check}: {status}; resolve the finding before freezing or generating")
        if status not in {"supported", "not_applicable", "requester_intended"}:
            raise ValueError(f"{check}: unsupported review status")
        evidence = row["prompt_evidence"]
        if not isinstance(evidence, list) or len(evidence) > 4:
            raise ValueError(f"{check}: prompt_evidence must be a list of at most four phrases")
        if status != "not_applicable" and not evidence:
            raise ValueError(f"{check}: an applicable check requires literal positive prompt evidence")
        if status == "not_applicable" and evidence:
            raise ValueError(f"{check}: not_applicable requires empty evidence and an explanation")
        for phrase in evidence:
            if not isinstance(phrase, str) or len(phrase.split()) < 3 or phrase not in prompt:
                raise ValueError(f"{check}: evidence must be a substantive literal phrase in the reviewed prompt")
        if status == "requester_intended":
            source = row.get("requester_source_text")
            if not isinstance(source, str) or len(source.strip()) < 3 or not any(
                source in str(span.get("text") or "") for span in spans if isinstance(span, dict)
            ):
                raise ValueError(f"{check}: an intentional departure needs exact active requester source text")
        elif "requester_source_text" in row:
            raise ValueError(f"{check}: requester exception belongs only to requester_intended")
    if all(row["status"] == "not_applicable" for row in checks.values()):
        raise ValueError("body_action scope cannot mark every check not_applicable")
    return copy.deepcopy(review)


def build_policy(core: Any, baseline_review: Any) -> dict:
    if not isinstance(core, dict) or core.get("contract_version") != "photo-authorial-core/v3":
        raise ValueError("embodiment preflight requires a frozen v3 core")
    baseline = core.get("baseline_prompt_en")
    if not isinstance(baseline, str):
        raise ValueError("embodiment preflight requires the frozen baseline prompt")
    policy = {
        "contract_version": POLICY_VERSION,
        "source_authorial_core_sha256": core["canonical_sha256"],
        "source_intent_lock_sha256": core["intent_lock"]["canonical_sha256"],
        "baseline_review": validate_review(baseline_review, baseline, core, "agent_prepack"),
        "required_checks": list(CHECKS),
        "boundary": "Agent review with literal actuation and exact text binding; not a kinematic proof or pixel judgment.",
    }
    policy["canonical_sha256"] = canonical_sha256(policy)
    return policy


def policy_from_pack(pack: dict) -> dict | None:
    marker = (pack.get("provenance") or {}).get("embodiment_preflight_required")
    if "embodiment_preflight" not in pack and marker is None:
        return None  # Serialized packs made before this opt-in workflow remain replayable.
    if pack.get("contract_version") != "photo-candidate-pack/v6" or marker is not True:
        raise ValueError("embodiment preflight requires a v6 pack and its explicit provenance marker")
    policy = pack.get("embodiment_preflight")
    if not isinstance(policy, dict):
        raise ValueError("required embodiment preflight is missing")
    expected = build_policy(pack.get("authorial_core"), policy.get("baseline_review"))
    if policy != expected:
        raise ValueError("embodiment preflight differs from the frozen core and baseline review")
    return expected


def audit_composed(pack: dict, composed: dict) -> list[dict]:
    try:
        policy = policy_from_pack(pack)
        binding = composed.get("embodiment_review")
        if policy is None:
            if "embodiment_review" in composed:
                raise ValueError("embodiment review has no governing pack contract")
            return []
        if not isinstance(binding, dict) or set(binding) != {"source_contract_sha256", "review"}:
            raise ValueError("composed prompt requires an embodiment_review binding")
        if binding["source_contract_sha256"] != policy["canonical_sha256"]:
            raise ValueError("composed embodiment review is bound to a different contract")
        review = validate_review(binding["review"], str(composed.get("prompt_en") or ""),
                                 pack["authorial_core"], "agent_postcomposition")
        if policy["baseline_review"]["scope"] == "body_action" and review["scope"] != "body_action":
            raise ValueError("a frozen body-action review cannot be downgraded during composition")
        for check, baseline_row in policy["baseline_review"]["checks"].items():
            if baseline_row["status"] != "not_applicable" and review["checks"][check]["status"] == "not_applicable":
                raise ValueError(f"{check}: an applicable baseline check cannot be dropped during composition")
    except (ValueError, KeyError, TypeError) as exc:
        return [{"check": "embodiment_preflight", "reason": str(exc)}]
    return []


def audit_runtime(pack: dict, composed: dict, request: dict) -> list[dict]:
    failures = audit_composed(pack, composed)
    if failures:
        return failures
    policy = policy_from_pack(pack)
    if policy is None:
        if "source_embodiment_preflight_sha256" in request:
            return [{"check": "embodiment_runtime", "reason": "runtime embodiment binding has no governing policy"}]
        return []
    if request.get("source_embodiment_preflight_sha256") != policy["canonical_sha256"]:
        failures.append({"check": "embodiment_runtime", "reason": "runtime must bind the exact embodiment preflight"})
    prompt = composed["prompt_en"]
    allowed = [prompt]
    negative = composed.get("negative_en")
    if isinstance(negative, str):
        allowed.append(prompt + "\n\nAvoid: " + negative)
    if request.get("runtime_prompt_en") not in allowed:
        failures.append({"check": "embodiment_runtime", "reason": "new runtime prose requires a new composed review; only the exact prompt and optional preserved Avoid suffix are allowed"})
    return failures


def render_gate_ids(pack: dict, composed: dict | None) -> tuple[list[str], list[dict]]:
    failures = audit_composed(pack, composed or {})
    if failures:
        return [], failures
    policy = policy_from_pack(pack)
    if policy is None:
        return [], []
    review = composed["embodiment_review"]["review"]
    if review["scope"] == "not_applicable":
        return [], []
    return [f"embodiment_{check}" for check in CHECKS
            if review["checks"][check]["status"] != "not_applicable"], []
