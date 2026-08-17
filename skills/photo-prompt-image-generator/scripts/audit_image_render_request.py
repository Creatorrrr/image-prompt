#!/usr/bin/env python3
"""Audit exact runtime inputs before a native or API image-generation call.

The composed-prompt audit proves the candidate composition only.  This auditor
separately verifies that a concrete render request embeds that audited prompt,
preserves negative_en byte-for-byte, and binds real reference files without
silently inheriting the composed preflight result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import audit_composed_prompt


SCHEMA_VERSION = "photo-image-render-request/v2"


def load_json_arg(raw: str) -> Any:
    raw = raw.strip()
    if raw.startswith("{") or raw.startswith("["):
        return json.loads(raw)
    return json.loads(Path(raw).read_text(encoding="utf-8"))


def one_object(payload: Any, label: str) -> dict[str, Any]:
    if isinstance(payload, list):
        if len(payload) != 1:
            raise ValueError(f"{label} list must contain exactly one object")
        payload = payload[0]
    if not isinstance(payload, dict):
        raise ValueError(f"{label} must be a JSON object or one-item list")
    return payload


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_path(raw: str, request_path: Path | None) -> Path:
    path = Path(raw).expanduser()
    if not path.is_absolute() and request_path is not None:
        path = request_path.parent / path
    return path.resolve()


def audit_image_render_request(
    pack: dict[str, Any],
    composed: dict[str, Any],
    request: dict[str, Any],
    *,
    request_path: Path | None = None,
) -> dict[str, Any]:
    failures: list[dict[str, Any]] = []

    if request.get("schema_version") != SCHEMA_VERSION:
        failures.append(
            {
                "check": "schema_version",
                "reason": f"render request must use {SCHEMA_VERSION}",
            }
        )

    pack_id = str(pack.get("pack_id") or "")
    composed_pack_id = str(composed.get("pack_id") or "")
    request_pack_id = str(request.get("pack_id") or "")
    if not pack_id or composed_pack_id != pack_id or request_pack_id != pack_id:
        failures.append(
            {
                "check": "pack_id",
                "reason": "pack, composed prompt, and render request must share one exact pack_id",
                "pack": pack_id,
                "composed": composed_pack_id,
                "request": request_pack_id,
            }
        )

    authorial_core = (
        pack.get("authorial_core")
        if isinstance(pack.get("authorial_core"), dict)
        else {}
    )
    intent_lock = (
        authorial_core.get("intent_lock")
        if authorial_core.get("contract_version")
        in {"photo-authorial-core/v2", "photo-authorial-core/v3"}
        and isinstance(authorial_core.get("intent_lock"), dict)
        else {}
    )
    expected_intent_lock_sha256 = str(intent_lock.get("canonical_sha256") or "")
    if intent_lock and request.get("source_intent_lock_sha256") != expected_intent_lock_sha256:
        failures.append(
            {
                "check": "source_intent_lock_sha256",
                "reason": "an intent-locked v5/v6 render request must bind the exact requesting-user-priority intent lock",
                "expected": expected_intent_lock_sha256,
                "actual": request.get("source_intent_lock_sha256"),
            }
        )

    runtime_prompt = request.get("runtime_prompt_en")
    if not isinstance(runtime_prompt, str) or not runtime_prompt.strip():
        failures.append(
            {
                "check": "runtime_prompt_en",
                "reason": "render request requires the exact runtime prompt string",
            }
        )
        runtime_prompt = ""
    composed_prompt = str(composed.get("prompt_en") or "")
    if not composed_prompt or composed_prompt not in runtime_prompt:
        failures.append(
            {
                "check": "composed_prompt_binding",
                "reason": "exact audited prompt_en must occur contiguously in runtime_prompt_en",
            }
        )

    pack_negative = pack.get("negative_en")
    composed_negative = composed.get("negative_en")
    runtime_negative = request.get("runtime_negative_en")
    if composed_negative != pack_negative:
        failures.append(
            {
                "check": "composed_negative_en",
                "reason": "composed negative_en differs from candidate pack",
            }
        )
    if runtime_negative != pack_negative:
        failures.append(
            {
                "check": "runtime_negative_en",
                "reason": "runtime negative_en must equal candidate-pack negative_en byte-for-byte",
                "expected_sha256": (
                    hashlib.sha256(str(pack_negative).encode("utf-8")).hexdigest()
                    if pack_negative is not None
                    else None
                ),
                "actual_sha256": (
                    hashlib.sha256(str(runtime_negative).encode("utf-8")).hexdigest()
                    if runtime_negative is not None
                    else None
                ),
            }
        )
    if pack_negative is not None and f"Avoid: {pack_negative}" not in runtime_prompt:
        failures.append(
            {
                "check": "runtime_negative_binding",
                "reason": "runtime_prompt_en must contain the exact candidate-pack negative after an Avoid: prefix",
            }
        )

    effective_visual_contract, visual_selection_failures = (
        audit_composed_prompt.derive_effective_visual_obligation_contract(
            pack,
            composed,
        )
    )
    failures.extend(
        {
            "check": f"effective_visual_contract.{failure.get('check')}",
            "reason": failure.get("reason"),
            **{
                key: value
                for key, value in failure.items()
                if key not in {"check", "reason"}
            },
        }
        for failure in visual_selection_failures
    )
    effective_visual_sha256 = (
        audit_composed_prompt.effective_visual_obligation_sha256(
            effective_visual_contract
        )
    )
    selected_visual_concepts = [
        str(value)
        for value in (effective_visual_contract or {}).get(
            "selected_visual_concept_ids"
        )
        or []
        if str(value).strip()
    ]
    if selected_visual_concepts and request.get(
        "effective_visual_contract_sha256"
    ) != effective_visual_sha256:
        failures.append(
            {
                "check": "effective_visual_contract_sha256",
                "reason": (
                    "a selected visual concept requires the runtime request to bind the "
                    "pack-plus-composed effective visual contract"
                ),
                "expected": effective_visual_sha256,
                "actual": request.get("effective_visual_contract_sha256"),
            }
        )

    runtime_label_rules: list[dict[str, str]] = [
        {"label": str(label), "source": "authorial_core"}
        for label in authorial_core.get("runtime_forbidden_labels") or []
        if str(label).strip()
    ]
    for obligation in (effective_visual_contract or {}).get("obligations") or []:
        if not isinstance(obligation, dict):
            continue
        expression = (
            obligation.get("runtime_expression")
            if isinstance(obligation.get("runtime_expression"), dict)
            else {}
        )
        runtime_label_rules.extend(
            {
                "label": str(label),
                "source": f"visual_profile:{obligation.get('id') or ''}",
            }
            for label in expression.get("runtime_forbidden_labels") or []
            if str(label).strip()
        )
    deduped_runtime_rules: list[dict[str, str]] = []
    seen_runtime_labels: set[str] = set()
    for rule in runtime_label_rules:
        key = rule["label"].casefold()
        if key in seen_runtime_labels:
            continue
        seen_runtime_labels.add(key)
        deduped_runtime_rules.append(rule)
    runtime_surfaces = {
        "runtime_prompt_en": runtime_prompt,
        "runtime_negative_en": (
            str(runtime_negative) if runtime_negative is not None else ""
        ),
    }
    runtime_label_hits = [
        {
            **rule,
            "surfaces": [
                surface
                for surface, text in runtime_surfaces.items()
                if audit_composed_prompt.text_contains_term(text, rule["label"])
            ],
        }
        for rule in deduped_runtime_rules
        if any(
            audit_composed_prompt.text_contains_term(text, rule["label"])
            for text in runtime_surfaces.values()
        )
    ]
    if runtime_label_hits:
        failures.append(
            {
                "check": "runtime_forbidden_label",
                "reason": "a meaning-resolution label leaked into a concrete runtime prompt surface",
                "hits": runtime_label_hits,
            }
        )

    boundary = request.get("audit_boundary")
    if not isinstance(boundary, dict):
        failures.append(
            {
                "check": "audit_boundary",
                "reason": "render request requires an explicit audit_boundary object",
            }
        )
        boundary = {}
    if boundary.get("composed_prompt_audit_status") not in {"pass", "warn"}:
        failures.append(
            {
                "check": "composed_prompt_audit_status",
                "reason": "render request requires a passing or warning composed preflight",
            }
        )
    if boundary.get("runtime_prompt_audit_status") != "not_run":
        failures.append(
            {
                "check": "runtime_prompt_audit_status",
                "reason": "runtime string must remain not_run until this exact-input audit succeeds",
            }
        )
    if boundary.get("inherits_composed_prompt_pass") is not False:
        failures.append(
            {
                "check": "audit_inheritance",
                "reason": "runtime request must explicitly refuse inheritance of composed preflight PASS",
            }
        )

    reference_control = (
        pack.get("moe_response", {}).get("reference_identity_control")
        if isinstance(pack.get("moe_response"), dict)
        else None
    )
    references = request.get("references")
    if not isinstance(references, list):
        failures.append(
            {"check": "references", "reason": "render request references must be a list"}
        )
        references = []
    if isinstance(reference_control, dict) and reference_control.get("enabled") is True:
        identity_rows = [
            row
            for row in references
            if isinstance(row, dict) and row.get("role") == "sole_identity_and_adult_age_reference"
        ]
        if len(identity_rows) != 1:
            failures.append(
                {
                    "check": "identity_reference_role",
                    "reason": "identity-controlled render requires exactly one sole identity and adult-age reference",
                    "actual": len(identity_rows),
                }
            )
    for index, row in enumerate(references):
        if not isinstance(row, dict):
            failures.append(
                {"check": f"references[{index}]", "reason": "reference row must be an object"}
            )
            continue
        raw_path = str(row.get("path") or "").strip()
        expected_sha = str(row.get("sha256") or "").strip().lower()
        if not raw_path:
            failures.append(
                {"check": f"references[{index}].path", "reason": "reference path is required"}
            )
            continue
        resolved = resolve_path(raw_path, request_path)
        if not resolved.is_file():
            failures.append(
                {
                    "check": f"references[{index}].path",
                    "reason": "reference file does not exist",
                    "path": str(resolved),
                }
            )
            continue
        actual_sha = sha256_path(resolved)
        if expected_sha != actual_sha:
            failures.append(
                {
                    "check": f"references[{index}].sha256",
                    "reason": "reference bytes differ from the recorded digest",
                    "expected": expected_sha,
                    "actual": actual_sha,
                }
            )

    return {
        "schema_version": "photo-image-render-request-audit/v1",
        "pack_id": pack_id,
        "status": "pass" if not failures else "fail",
        "runtime_prompt_id": hashlib.sha256(runtime_prompt.encode("utf-8")).hexdigest()[:16],
        "source_intent_lock_sha256": expected_intent_lock_sha256 or None,
        "negative_matches_pack": runtime_negative == pack_negative,
        "effective_visual_contract_sha256": effective_visual_sha256,
        "selected_visual_concept_ids": selected_visual_concepts,
        "reference_count": len(references),
        "failures": failures,
        "boundary": (
            "This audit verifies exact text and reference bytes before generation. It does not inspect "
            "rendered pixels or establish user-perceived quality."
        ),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pack", required=True)
    parser.add_argument("--composed", required=True)
    parser.add_argument("--request", required=True)
    parser.add_argument("--output")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        pack = one_object(load_json_arg(args.pack), "candidate pack")
        composed = one_object(load_json_arg(args.composed), "composed prompt")
        request = one_object(load_json_arg(args.request), "render request")
        request_path = None
        raw_request_path = Path(args.request).expanduser()
        if not args.request.strip().startswith(("{", "[")) and raw_request_path.is_file():
            request_path = raw_request_path.resolve()
        result = audit_image_render_request(
            pack, composed, request, request_path=request_path
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "reason": str(exc)}, ensure_ascii=False, indent=2))
        return 2

    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
