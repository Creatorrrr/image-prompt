"""Neutral agent-authored body review binding; no pose solver or taxonomy."""
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
