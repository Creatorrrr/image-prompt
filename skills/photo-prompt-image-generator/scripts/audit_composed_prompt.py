#!/usr/bin/env python3
"""Audit an agent-composed photo prompt against a candidate pack."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Sequence


def load_json_arg(raw: str) -> Any:
    raw = raw.strip()
    if raw.startswith("{") or raw.startswith("["):
        return json.loads(raw)
    return json.loads(Path(raw).read_text(encoding="utf-8"))


def first_pack(payload: Any) -> dict[str, Any]:
    if isinstance(payload, list):
        if not payload:
            raise ValueError("candidate pack list is empty")
        payload = payload[0]
    if not isinstance(payload, dict):
        raise ValueError("candidate pack must be a JSON object or a non-empty list")
    return payload


def composed_object(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("composed prompt must be a JSON object")
    return payload


def text_contains_term(text: str, term: str) -> bool:
    term = str(term or "").strip()
    if not term:
        return False
    lowered = text.lower()
    term_lower = term.lower()
    if term_lower.isascii() and re.search(r"[A-Za-z0-9]", term_lower):
        pattern = r"(?<![A-Za-z0-9])" + re.escape(term_lower) + r"(?![A-Za-z0-9])"
        return re.search(pattern, lowered) is not None
    return term_lower in lowered


def normalize_chosen_candidate_ids(raw: Any) -> set[str]:
    chosen: set[str] = set()
    if raw is None:
        return chosen
    if isinstance(raw, str):
        return {raw}
    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, str):
                chosen.add(item)
            elif isinstance(item, dict) and item.get("id"):
                chosen.add(str(item["id"]))
        return chosen
    if isinstance(raw, dict):
        for value in raw.values():
            chosen.update(normalize_chosen_candidate_ids(value))
    return chosen


def chosen_slot_entry_ids(chosen: set[str]) -> dict[str, set[str]]:
    slots: dict[str, set[str]] = {}
    for candidate_id in chosen:
        parts = candidate_id.split(":", 2)
        if len(parts) != 3 or parts[0] != "slot":
            continue
        _scope, slot, entry_id = parts
        if slot and entry_id:
            slots.setdefault(slot, set()).add(entry_id)
    return slots


def candidate_ids_from_pack(pack: dict[str, Any]) -> set[str]:
    ids = {str(candidate.get("id")) for candidate in pack.get("presets", []) if isinstance(candidate, dict)}
    slots = pack.get("slots") or {}
    if isinstance(slots, dict):
        slot_values = slots.values()
    else:
        slot_values = slots
    for slot_payload in slot_values:
        if not isinstance(slot_payload, dict):
            continue
        for candidate in slot_payload.get("candidates") or []:
            if isinstance(candidate, dict) and candidate.get("id"):
                ids.add(str(candidate["id"]))
    return ids


def assertion_terms_for_intent(intent: dict[str, Any], composed: dict[str, Any]) -> list[str]:
    text = str(intent.get("text") or "")
    terms = [text]
    for term in intent.get("audit_terms") or []:
        if isinstance(term, str):
            terms.append(term)
    assertions = composed.get("coverage_assertions") or {}
    if isinstance(assertions, dict):
        raw = assertions.get(text)
        if isinstance(raw, str):
            terms.append(raw)
        elif isinstance(raw, list):
            terms.extend(str(item) for item in raw if str(item).strip())
        elif isinstance(raw, dict):
            terms.extend(str(item) for item in raw.values() if str(item).strip())
    return list(dict.fromkeys(term for term in terms if str(term).strip()))


def audit_composed_prompt(pack: dict[str, Any], composed: dict[str, Any]) -> dict[str, Any]:
    failures: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    prompt_en = str(composed.get("prompt_en") or "")
    negative_en = composed.get("negative_en")

    if not prompt_en.strip():
        failures.append({"check": "output_contract", "reason": "missing prompt_en"})
    if "watermark" not in prompt_en.lower() or "no text" not in prompt_en.lower():
        failures.append({"check": "output_contract", "reason": "prompt_en must include no text or watermark"})

    pack_id = str(pack.get("pack_id") or "")
    composed_pack_id = str(composed.get("pack_id") or "")
    if composed_pack_id and pack_id and composed_pack_id != pack_id:
        failures.append({"check": "pack_id", "reason": "pack_id mismatch", "expected": pack_id, "actual": composed_pack_id})

    pack_negative = pack.get("negative_en")
    if pack_negative and negative_en is None:
        warnings.append({"check": "negative_en", "reason": "candidate pack has negative_en but composed prompt omitted it"})
    elif pack_negative and negative_en != pack_negative:
        failures.append({"check": "negative_en", "reason": "negative_en differs from candidate pack"})

    for intent in pack.get("mandatory_intents") or []:
        if not isinstance(intent, dict):
            continue
        terms = assertion_terms_for_intent(intent, composed)
        if not any(text_contains_term(prompt_en, term) for term in terms):
            failures.append(
                {
                    "check": "mandatory_intent",
                    "reason": "intent not represented in prompt_en",
                    "intent": intent.get("text"),
                    "accepted_terms": terms,
                }
            )
        elif intent.get("status") == "uncovered":
            warnings.append(
                {
                    "check": "uncovered_intent",
                    "reason": "uncovered candidate-pack intent was preserved by free description/assertion",
                    "intent": intent.get("text"),
                }
            )

    chosen = normalize_chosen_candidate_ids(composed.get("chosen_candidate_ids"))
    valid_ids = candidate_ids_from_pack(pack)
    if not chosen:
        warnings.append({"check": "chosen_candidate_ids", "reason": "no chosen_candidate_ids supplied"})
    invalid = sorted(candidate_id for candidate_id in chosen if candidate_id not in valid_ids)
    if invalid:
        failures.append({"check": "chosen_candidate_ids", "reason": "unknown candidate id", "ids": invalid})

    chosen_slots = chosen_slot_entry_ids(chosen)
    role_scene_policy = pack.get("role_scene_policy") if isinstance(pack.get("role_scene_policy"), dict) else {}
    if role_scene_policy.get("enabled"):
        selected_locations = chosen_slots.get("location", set())
        allowed_locations = {str(item) for item in role_scene_policy.get("allowed_locations") or []}
        forbidden_locations = {str(item) for item in role_scene_policy.get("forbidden_locations") or []}
        forbidden_locations.update(str(item) for item in role_scene_policy.get("discouraged_generic_locations") or [])
        forbidden_selected = sorted(selected_locations & forbidden_locations)
        if forbidden_selected:
            failures.append(
                {
                    "check": "role_scene_policy",
                    "reason": "role-incompatible location selected",
                    "location_ids": forbidden_selected,
                    "scene_family": role_scene_policy.get("scene_family"),
                }
            )
        outside_allowed = sorted(selected_locations - allowed_locations) if allowed_locations else []
        if outside_allowed and role_scene_policy.get("enforce"):
            failures.append(
                {
                    "check": "role_scene_policy",
                    "reason": "selected location is outside role scene pool",
                    "location_ids": outside_allowed,
                    "allowed_locations": sorted(allowed_locations),
                    "scene_family": role_scene_policy.get("scene_family"),
                }
            )
        if allowed_locations and not selected_locations:
            warnings.append(
                {
                    "check": "role_scene_policy",
                    "reason": "no location candidate id supplied for enforced role-scene audit",
                    "scene_family": role_scene_policy.get("scene_family"),
                }
            )

    species_policy = pack.get("species_family") if isinstance(pack.get("species_family"), dict) else {}
    if species_policy.get("enabled") and not species_policy.get("hybrid_allowed"):
        allowed = species_policy.get("allowed") if isinstance(species_policy.get("allowed"), dict) else {}
        for slot, allowed_ids_raw in allowed.items():
            selected_ids = chosen_slots.get(str(slot), set())
            allowed_ids = {str(item) for item in allowed_ids_raw or []}
            mismatched = sorted(selected_ids - allowed_ids)
            if mismatched:
                failures.append(
                    {
                        "check": "species_family",
                        "reason": "selected species-family detail is outside the locked family",
                        "slot": str(slot),
                        "ids": mismatched,
                        "allowed_ids": sorted(allowed_ids),
                        "family": species_policy.get("family"),
                        "variant_id": species_policy.get("variant_id"),
                    }
                )

    for conflict in pack.get("conflicts") or []:
        if not isinstance(conflict, dict) or str(conflict.get("severity") or "hard") != "hard":
            continue
        conflict_ids = {str(candidate_id) for candidate_id in conflict.get("candidates", [])}
        if conflict_ids and conflict_ids <= chosen:
            failures.append(
                {
                    "check": "hard_conflict",
                    "reason": "conflicting candidates selected together",
                    "conflict_id": conflict.get("id"),
                    "candidate_ids": sorted(conflict_ids),
                }
            )

    safety_floor = pack.get("safety_floor") if isinstance(pack.get("safety_floor"), dict) else {}
    for term in safety_floor.get("forbidden_terms") or []:
        if text_contains_term(prompt_en, str(term)):
            failures.append({"check": "safety_floor", "reason": "forbidden term appears in prompt_en", "term": term})

    status = "fail" if failures else "pass"
    return {
        "status": status,
        "pack_id": pack_id or None,
        "chosen_candidate_count": len(chosen),
        "failures": failures,
        "warnings": warnings,
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit an agent-composed prompt against a candidate pack.")
    parser.add_argument("--pack", required=True, help="Candidate pack JSON path or inline JSON.")
    parser.add_argument("--composed", required=True, help="Composed prompt JSON path or inline JSON.")
    parser.add_argument("--plain", action="store_true", help="Print only pass/fail summary.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = parse_args(argv)
        pack = first_pack(load_json_arg(args.pack))
        composed = composed_object(load_json_arg(args.composed))
        result = audit_composed_prompt(pack, composed)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    if args.plain:
        print(result["status"])
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
