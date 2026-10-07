"""Bind agent-authored body-action reviews; this module is not a pose solver.

No subject taxonomy, reference image, or prompt keyword selects an anatomy model.
The reviewer owns applicability and plausibility; code checks evidence, unresolved
findings, and exact input bindings. Neutral record validation is shared with precore; pack/runtime helpers here remain post-core.
"""
from __future__ import annotations

import copy
import hashlib
import json
from typing import Any













def policy_from_pack(pack: dict) -> dict:
    marker = (pack.get("provenance") or {}).get("embodiment_preflight_required")
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
        if not isinstance(binding, dict) or set(binding) != {"source_contract_sha256", "review"}:
            raise ValueError("composed prompt requires an embodiment_review binding")
        if binding["source_contract_sha256"] != policy["canonical_sha256"]:
            raise ValueError("composed embodiment review is bound to a different contract")
        review = validate_review(
            binding["review"], str(composed.get("prompt_en") or ""),
            pack["authorial_core"], "agent_postcomposition",
        )
        if policy["baseline_review"]["scope"] == "body_action" and review["scope"] != "body_action":
            raise ValueError("a frozen body-action review cannot be downgraded during composition")
        for check, baseline_row in policy["baseline_review"]["checks"].items():
            if (
                baseline_row["status"] != "not_applicable"
                and review["checks"][check]["status"] == "not_applicable"
            ):
                raise ValueError(f"{check}: an applicable baseline check cannot be dropped during composition")
    except (ValueError, KeyError, TypeError) as exc:
        return [{"check": "embodiment_preflight", "reason": str(exc)}]
    return []


def audit_runtime(pack: dict, composed: dict, request: dict) -> list[dict]:
    failures = audit_composed(pack, composed)
    if failures:
        return failures
    policy = policy_from_pack(pack)
    if request.get("source_embodiment_preflight_sha256") != policy["canonical_sha256"]:
        failures.append({
            "check": "embodiment_runtime",
            "reason": "runtime must bind the exact embodiment preflight",
        })
    prompt = composed["prompt_en"]
    allowed = [prompt]
    negative = composed.get("negative_en")
    if isinstance(negative, str):
        allowed.append(prompt + "\n\nAvoid: " + negative)
    if request.get("runtime_prompt_en") not in allowed:
        failures.append({
            "check": "embodiment_runtime",
            "reason": "new runtime prose requires a new composed review; only the exact prompt and optional preserved Avoid suffix are allowed",
        })
    return failures


def render_gate_ids(pack: dict, composed: dict | None) -> tuple[list[str], list[dict]]:
    failures = audit_composed(pack, composed or {})
    if failures:
        return [], failures
    policy = policy_from_pack(pack)
    review = composed["embodiment_review"]["review"]
    if review["scope"] == "not_applicable":
        return [], []
    return [
        f"embodiment_{check}" for check in CHECKS
        if review["checks"][check]["status"] != "not_applicable"
    ], []

from photo_precore_bridge import load as _load_precore
_review = _load_precore("photo_embodiment_review")
CHECKS = _review.CHECKS
GATES = _review.GATES
POLICY_VERSION = _review.POLICY_VERSION
REVIEW_VERSION = _review.REVIEW_VERSION
_text = _review._text
build_policy = _review.build_policy
canonical_sha256 = _review.canonical_sha256
text_sha256 = _review.text_sha256
validate_review = _review.validate_review
