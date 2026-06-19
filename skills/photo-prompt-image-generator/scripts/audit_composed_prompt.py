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


def composed_search_text(composed: dict[str, Any]) -> str:
    values = [str(composed.get("prompt_en") or "")]
    assertions = composed.get("coverage_assertions") or {}
    if isinstance(assertions, dict):
        for value in assertions.values():
            if isinstance(value, str):
                values.append(value)
            elif isinstance(value, list):
                values.extend(str(item) for item in value if str(item).strip())
            elif isinstance(value, dict):
                values.extend(str(item) for item in value.values() if str(item).strip())
    return " ".join(values)


def candidate_id_matches_term(candidate_id: str, term: str) -> bool:
    term = str(term or "").strip().lower()
    if not term:
        return False
    return term in str(candidate_id or "").lower()


def chosen_matches_terms(chosen: set[str], terms: Sequence[str]) -> bool:
    return any(candidate_id_matches_term(candidate_id, term) for candidate_id in chosen for term in terms)


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
    proposition = pack.get("visual_proposition")
    if isinstance(proposition, dict):
        for key in ("core_candidates", "tension_candidates"):
            for candidate in proposition.get(key) or []:
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


def terms_for_identity_axis(axis: dict[str, Any]) -> list[str]:
    terms = [str(axis.get("id") or "")]
    for term in axis.get("terms") or []:
        if isinstance(term, str):
            terms.append(term)
    description = str(axis.get("description") or "").strip()
    if description:
        terms.append(description)
    return [term for term in dict.fromkeys(terms) if term.strip()]


def open_slot_terms(open_slot: dict[str, Any]) -> list[str]:
    terms: list[str] = []
    for key in ("masked_entry_id", "candidate_id"):
        value = str(open_slot.get(key) or "").strip()
        if value:
            terms.append(value)
    for term in open_slot.get("terms") or []:
        if isinstance(term, str) and term.strip():
            terms.append(term)
    return list(dict.fromkeys(terms))


def motif_taxonomy_terms(pack: dict[str, Any], motif: str) -> list[str]:
    budget = pack.get("motif_budget") if isinstance(pack.get("motif_budget"), dict) else {}
    taxonomy = budget.get("motif_taxonomy") if isinstance(budget.get("motif_taxonomy"), dict) else {}
    return [str(term) for term in taxonomy.get(motif, []) if str(term).strip()]


def photographic_integration_category_terms(integration: dict[str, Any], category: str) -> list[str]:
    terms: list[str] = []
    category_terms = integration.get("category_terms") if isinstance(integration.get("category_terms"), dict) else {}
    for term in category_terms.get(category) or []:
        if isinstance(term, str) and term.strip():
            terms.append(term)
    suggested = integration.get("suggested_phrases") if isinstance(integration.get("suggested_phrases"), dict) else {}
    for phrase in suggested.get(category) or []:
        if isinstance(phrase, str) and phrase.strip():
            terms.append(phrase)
    return list(dict.fromkeys(terms))


def audit_photographic_integration(pack: dict[str, Any], search_text: str) -> dict[str, Any] | None:
    integration = pack.get("photographic_integration")
    if not isinstance(integration, dict) or not integration.get("enabled", True):
        return None

    required_categories = [
        str(category)
        for category in integration.get("required_categories") or []
        if str(category).strip()
    ]
    if not required_categories:
        required_categories = ["environment_binding", "optical_depth"]
    try:
        minimum_hits = int(integration.get("minimum_category_hits", 2) or 2)
    except (TypeError, ValueError):
        minimum_hits = 2
    minimum_hits = max(1, min(minimum_hits, len(required_categories)))

    hits: dict[str, list[str]] = {}
    missing: list[str] = []
    for category in required_categories:
        terms = photographic_integration_category_terms(integration, category)
        matched = [term for term in terms if text_contains_term(search_text, term)]
        if matched:
            hits[category] = matched[:5]
        else:
            missing.append(category)

    if len(hits) >= minimum_hits:
        return None
    return {
        "check": "photographic_integration",
        "reason": "composed prompt underuses the candidate pack's photographic integration layer",
        "profile_id": integration.get("profile_id"),
        "minimum_category_hits": minimum_hits,
        "hit_categories": sorted(hits),
        "missing_categories": missing,
        "principles": integration.get("principles", [])[:3] if isinstance(integration.get("principles"), list) else [],
    }


def visual_proposition_category_terms(proposition: dict[str, Any], category: str) -> list[str]:
    terms: list[str] = []
    category_terms = proposition.get("category_terms") if isinstance(proposition.get("category_terms"), dict) else {}
    for term in category_terms.get(category) or []:
        if isinstance(term, str) and term.strip():
            terms.append(term)
    candidate_keys = {
        "narrative_core": "core_candidates",
        "concept_tension": "tension_candidates",
    }
    for candidate in proposition.get(candidate_keys.get(category, ""), []) or []:
        if not isinstance(candidate, dict):
            continue
        for term in candidate.get("terms") or []:
            if isinstance(term, str) and term.strip():
                terms.append(term)
    return list(dict.fromkeys(terms))


def photographic_craft_dimension_terms(craft: dict[str, Any], dimension_id: str) -> list[str]:
    terms: list[str] = []
    for dimension in craft.get("active_dimensions") or []:
        if not isinstance(dimension, dict) or str(dimension.get("id") or "") != dimension_id:
            continue
        for key in ("selected_guidance_en", "selected_guidance_ko", "guidance_en", "guidance_ko", "selected_principle"):
            value = str(dimension.get(key) or "").strip()
            if value:
                terms.append(value)
        for term in dimension.get("audit_terms") or []:
            if isinstance(term, str) and term.strip():
                terms.append(term)
        for refinement in dimension.get("active_refinements") or []:
            if not isinstance(refinement, dict):
                continue
            for key in ("guidance_en", "guidance_ko", "principle"):
                value = str(refinement.get(key) or "").strip()
                if value:
                    terms.append(value)
            for term in refinement.get("audit_terms") or []:
                if isinstance(term, str) and term.strip():
                    terms.append(term)
    return list(dict.fromkeys(terms))


def audit_photographic_craft(pack: dict[str, Any], search_text: str) -> dict[str, Any] | None:
    craft = pack.get("photographic_craft")
    if not isinstance(craft, dict) or not craft.get("enabled", True):
        return None
    strategy = craft.get("top_strategy") if isinstance(craft.get("top_strategy"), dict) else {}
    dimensions = [
        str(dimension_id)
        for dimension_id in strategy.get("emphasize") or craft.get("prompt_dimension_ids") or []
        if str(dimension_id).strip()
    ]
    if not dimensions:
        dimensions = [
            str(dimension.get("id"))
            for dimension in craft.get("active_dimensions") or []
            if isinstance(dimension, dict) and str(dimension.get("id") or "").strip()
        ][:2]
    if not dimensions:
        return None

    hits: dict[str, list[str]] = {}
    missing: list[str] = []
    for dimension_id in dimensions:
        terms = photographic_craft_dimension_terms(craft, dimension_id)
        matched = [term for term in terms if text_contains_term(search_text, term)]
        if matched:
            hits[dimension_id] = matched[:5]
        else:
            missing.append(dimension_id)

    if hits:
        return None
    return {
        "check": "photographic_craft",
        "reason": "composed prompt does not visibly use the candidate pack's photographer craft decision layer",
        "top_strategy": strategy.get("id"),
        "expected_dimensions": dimensions,
        "missing_dimensions": missing,
        "principles": [
            str(dimension.get("selected_principle") or dimension.get("baseline_principle") or "")
            for dimension in craft.get("active_dimensions") or []
            if isinstance(dimension, dict) and str(dimension.get("id") or "") in set(dimensions)
        ][:3],
    }


def audit_visual_proposition(pack: dict[str, Any], search_text: str) -> dict[str, Any] | None:
    proposition = pack.get("visual_proposition")
    if not isinstance(proposition, dict) or not proposition.get("enabled", True):
        return None
    try:
        minimum_hits = int(proposition.get("minimum_hits", 1) or 0)
    except (TypeError, ValueError):
        minimum_hits = 1
    if minimum_hits <= 0:
        return None

    categories = [
        str(category)
        for category in proposition.get("audit_categories") or ["narrative_core", "concept_tension", "evidence"]
        if str(category).strip()
    ]
    if not categories:
        categories = ["narrative_core", "concept_tension", "evidence"]
    hits: dict[str, list[str]] = {}
    missing: list[str] = []
    for category in categories:
        terms = visual_proposition_category_terms(proposition, category)
        matched = [term for term in terms if text_contains_term(search_text, term)]
        if matched:
            hits[category] = matched[:5]
        else:
            missing.append(category)

    if len(hits) >= min(minimum_hits, len(categories)):
        return None
    return {
        "check": "visual_proposition",
        "reason": "composed prompt does not visibly use the candidate pack's emotional proposition or visual tension layer",
        "register": proposition.get("register"),
        "subject_class": proposition.get("subject_class"),
        "subject_classes": proposition.get("subject_classes", []),
        "minimum_hits": minimum_hits,
        "hit_categories": sorted(hits),
        "missing_categories": missing,
        "principles": proposition.get("principles", [])[:3] if isinstance(proposition.get("principles"), list) else [],
    }


def audit_artistic_final_touch(pack: dict[str, Any], prompt_en: str) -> dict[str, Any] | None:
    touch = pack.get("artistic_final_touch")
    if not isinstance(touch, dict) or not touch.get("enabled", True):
        return None
    final_sentence = str(touch.get("final_sentence_en") or "").strip()
    prompt_clean = prompt_en.strip()
    if final_sentence and prompt_clean.lower().endswith(final_sentence.lower()):
        return None
    audit_terms = [str(term) for term in touch.get("audit_terms") or [] if str(term).strip()]
    matched_terms = [term for term in audit_terms if text_contains_term(prompt_en, term)]
    return {
        "check": "artistic_final_touch",
        "reason": "composed prompt does not end with the candidate pack's final photographic touch",
        "expected_final_sentence": final_sentence or None,
        "matched_terms": matched_terms[:5],
    }


def audit_composed_prompt(pack: dict[str, Any], composed: dict[str, Any]) -> dict[str, Any]:
    failures: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    prompt_en = str(composed.get("prompt_en") or "")
    search_text = composed_search_text(composed)
    negative_en = composed.get("negative_en")

    if not prompt_en.strip():
        failures.append({"check": "output_contract", "reason": "missing prompt_en"})

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

    concept_axes = pack.get("concept_axes") if isinstance(pack.get("concept_axes"), dict) else {}
    for axis in concept_axes.get("required") or []:
        if not isinstance(axis, dict):
            continue
        terms = terms_for_identity_axis(axis)
        if terms and not any(text_contains_term(search_text, term) or chosen_matches_terms(chosen, [term]) for term in terms):
            failures.append(
                {
                    "check": "identity_axis",
                    "reason": "required identity axis not represented",
                    "axis": axis.get("id"),
                    "accepted_terms": terms,
                }
            )

    masked_echo_count = 0
    for open_slot in pack.get("open_slots") or []:
        if not isinstance(open_slot, dict):
            continue
        terms = open_slot_terms(open_slot)
        chosen_hit = chosen_matches_terms(chosen, [str(open_slot.get("candidate_id") or ""), str(open_slot.get("masked_entry_id") or "")])
        text_hits = [term for term in terms if text_contains_term(search_text, term)]
        if chosen_hit or text_hits:
            masked_echo_count += 1
            failures.append(
                {
                    "check": "masked_bucket_echo",
                    "reason": "masked/open preset section was copied back into the composed prompt",
                    "slot": open_slot.get("slot"),
                    "bucket": open_slot.get("bucket"),
                    "candidate_id": open_slot.get("candidate_id"),
                    "text_hits": text_hits[:8],
                    "chosen_hit": chosen_hit,
                }
            )

    motif_budget = pack.get("motif_budget") if isinstance(pack.get("motif_budget"), dict) else {}
    for motif in motif_budget.get("discouraged_now") or []:
        motif_id = str(motif or "")
        terms = motif_taxonomy_terms(pack, motif_id)
        if not terms:
            terms = [motif_id]
        text_hits = [term for term in terms if text_contains_term(search_text, term)]
        chosen_hit = chosen_matches_terms(chosen, terms)
        if text_hits or chosen_hit:
            failures.append(
                {
                    "check": "motif_quota",
                    "reason": "discouraged motif selected despite quota pressure",
                    "motif": motif_id,
                    "text_hits": text_hits[:8],
                    "chosen_hit": chosen_hit,
                }
            )

    taxonomy = motif_budget.get("motif_taxonomy") if isinstance(motif_budget.get("motif_taxonomy"), dict) else {}
    quota_motifs = set((motif_budget.get("quotas") or {}).keys()) if isinstance(motif_budget.get("quotas"), dict) else set()
    hit_motifs: set[str] = set()
    for motif, terms_raw in taxonomy.items():
        terms = [str(term) for term in terms_raw or [] if str(term).strip()]
        if terms and (chosen_matches_terms(chosen, terms) or any(text_contains_term(search_text, term) for term in terms)):
            hit_motifs.add(str(motif))
    if quota_motifs and hit_motifs and hit_motifs <= quota_motifs:
        warnings.append(
            {
                "check": "cliche_only_concept_coverage",
                "reason": "concept coverage relies only on capped/cliche motif groups",
                "motifs": sorted(hit_motifs),
            }
        )

    echo_risk = pack.get("template_echo_risk") if isinstance(pack.get("template_echo_risk"), dict) else {}
    if pack.get("open_slots"):
        try:
            max_allowed = float(echo_risk.get("max_allowed_score", 0.2))
        except (TypeError, ValueError):
            max_allowed = 0.2
        masked_total = max(1, len([slot for slot in pack.get("open_slots") or [] if isinstance(slot, dict)]))
        score = masked_echo_count / masked_total
        if score > max_allowed:
            failures.append(
                {
                    "check": "template_echo_risk",
                    "reason": "excessive overlap with masked source preset/bundle",
                    "score": round(score, 4),
                    "max_allowed_score": max_allowed,
                    "masked_echo_count": masked_echo_count,
                    "masked_slot_count": masked_total,
                }
            )

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

    photographic_warning = audit_photographic_integration(pack, search_text)
    if photographic_warning:
        warnings.append(photographic_warning)
    proposition_warning = audit_visual_proposition(pack, search_text)
    if proposition_warning:
        warnings.append(proposition_warning)
    craft_warning = audit_photographic_craft(pack, search_text)
    if craft_warning:
        warnings.append(craft_warning)
    final_touch_warning = audit_artistic_final_touch(pack, prompt_en)
    if final_touch_warning:
        warnings.append(final_touch_warning)

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
