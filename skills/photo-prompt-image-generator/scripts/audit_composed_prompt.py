#!/usr/bin/env python3
"""Audit an agent-composed photo prompt against a candidate pack."""

from __future__ import annotations

import argparse
import hashlib
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
        if len(payload) != 1:
            raise ValueError("candidate pack list must contain exactly one pack")
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
    return str(composed.get("prompt_en") or "")


def computed_pack_id(pack: dict[str, Any]) -> str:
    hashable = dict(pack)
    hashable["pack_id"] = None
    payload = json.dumps(hashable, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def assertion_values(raw: Any) -> list[str]:
    if isinstance(raw, str):
        return [raw] if raw.strip() else []
    if isinstance(raw, list):
        return [str(item) for item in raw if str(item).strip()]
    if isinstance(raw, dict):
        return [str(item) for item in raw.values() if str(item).strip()]
    return []


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
    for candidate in hybrid_augmentation_candidates_from_pack(pack):
        if candidate.get("id"):
            ids.add(str(candidate["id"]))
    return ids


def hybrid_augmentation_candidates_from_pack(pack: dict[str, Any]) -> list[dict[str, Any]]:
    hybrid = pack.get("hybrid_augmentation") if isinstance(pack.get("hybrid_augmentation"), dict) else {}
    adult = hybrid.get("adult_appeal") if isinstance(hybrid.get("adult_appeal"), dict) else {}
    axes = adult.get("axes") if isinstance(adult.get("axes"), dict) else {}
    candidates: list[dict[str, Any]] = []
    for axis in axes.values():
        if not isinstance(axis, dict):
            continue
        candidates.extend(
            candidate
            for candidate in axis.get("candidate_inventory") or []
            if isinstance(candidate, dict)
        )
    return candidates


def candidate_objects_from_pack(pack: dict[str, Any]) -> dict[str, dict[str, Any]]:
    candidates: dict[str, dict[str, Any]] = {}
    for candidate in pack.get("presets") or []:
        if isinstance(candidate, dict) and candidate.get("id"):
            candidates[str(candidate["id"])] = candidate
    slots = pack.get("slots") or {}
    slot_values = slots.values() if isinstance(slots, dict) else slots
    for slot_payload in slot_values:
        if not isinstance(slot_payload, dict):
            continue
        for candidate in slot_payload.get("candidates") or []:
            if isinstance(candidate, dict) and candidate.get("id"):
                candidates[str(candidate["id"])] = candidate
    for candidate in hybrid_augmentation_candidates_from_pack(pack):
        if candidate.get("id"):
            candidates[str(candidate["id"])] = candidate
    return candidates


def assertion_terms_for_intent(intent: dict[str, Any], composed: dict[str, Any]) -> list[str]:
    text = str(intent.get("text") or "")
    terms = [str(item) for item in intent.get("audit_terms") or [] if str(item).strip()]
    if not terms:
        terms = [text]
    assertions = composed.get("coverage_assertions") or {}
    if isinstance(assertions, dict):
        terms.extend(assertion_values(assertions.get(text)))
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
    if final_sentence and final_sentence.lower() in prompt_en.lower():
        return None
    audit_terms = [str(term) for term in touch.get("audit_terms") or [] if str(term).strip()]
    matched_terms = [term for term in audit_terms if text_contains_term(prompt_en, term)]
    if len(matched_terms) >= min(2, len(audit_terms)):
        return None
    return {
        "check": "artistic_final_touch",
        "reason": "composed prompt does not represent the profile-specific photographic touch",
        "expected_final_sentence": final_sentence or None,
        "matched_terms": matched_terms[:5],
    }


def nonempty_string_list(raw: Any) -> list[str]:
    if not isinstance(raw, list):
        return []
    return [str(item).strip() for item in raw if isinstance(item, str) and str(item).strip()]


def normalized_unique_count(values: Sequence[str]) -> int:
    return len({str(value).strip().lower() for value in values if str(value).strip()})


def audit_viewer_experience(
    pack: dict[str, Any],
    composed: dict[str, Any],
    prompt_en: str,
) -> list[dict[str, Any]]:
    contract = pack.get("viewer_experience")
    if not isinstance(contract, dict) or not contract.get("enabled"):
        return []

    failures: list[dict[str, Any]] = []
    experience = composed.get("viewer_experience")
    if not isinstance(experience, dict):
        return [
            {
                "check": "viewer_experience",
                "reason": "enabled viewer-experience pack requires a viewer_experience object",
            }
        ]

    required_fields = [str(item) for item in contract.get("required_fields") or [] if str(item)]
    missing_fields = [field for field in required_fields if field not in experience]
    if missing_fields:
        failures.append(
            {
                "check": "viewer_experience",
                "reason": "viewer experience is missing required fields",
                "fields": missing_fields,
            }
        )

    scalar_fields = (
        "viewing_context",
        "primary_viewer_need",
        "intended_experience",
        "viewer_promise",
        "first_glance_hook",
        "interpretive_question",
        "attachment_channel",
        "commercial_objective",
    )
    invalid_scalars = [
        field
        for field in scalar_fields
        if not isinstance(experience.get(field), str) or not str(experience.get(field)).strip()
    ]
    if invalid_scalars:
        failures.append(
            {
                "check": "viewer_experience_primary",
                "reason": "viewer experience must select one scalar value for each primary field",
                "fields": invalid_scalars,
            }
        )
    if "primary_viewer_needs" in experience or "intended_experiences" in experience:
        failures.append(
            {
                "check": "viewer_experience_affect_stacking",
                "reason": "use one primary_viewer_need and one scalar intended_experience, not stacked plural fields",
            }
        )

    allowed = contract.get("allowed_values") if isinstance(contract.get("allowed_values"), dict) else {}
    for field, enum_key in (
        ("viewing_context", "viewing_context"),
        ("primary_viewer_need", "primary_viewer_need"),
        ("attachment_channel", "attachment_channel"),
        ("commercial_objective", "commercial_objective"),
    ):
        value = str(experience.get(field) or "")
        values = {str(item) for item in allowed.get(enum_key) or []}
        if value and values and value not in values:
            failures.append(
                {
                    "check": "viewer_experience_enum",
                    "reason": "viewer experience uses a value outside the candidate-pack contract",
                    "field": field,
                    "value": value,
                }
            )

    audience = experience.get("target_audience")
    if not isinstance(audience, dict):
        audience = {}
    audience_fields = [str(item) for item in contract.get("target_audience_fields") or [] if str(item)]
    missing_audience = [
        field
        for field in audience_fields
        if not isinstance(audience.get(field), str) or not str(audience.get(field)).strip()
    ]
    if missing_audience:
        failures.append(
            {
                "check": "viewer_experience_audience",
                "reason": "target audience must declare literacy and prior-knowledge scope",
                "fields": missing_audience,
            }
        )
    literacy = str(audience.get("literacy") or "")
    allowed_literacy = {str(item) for item in allowed.get("audience_literacy") or []}
    if literacy and allowed_literacy and literacy not in allowed_literacy:
        failures.append(
            {
                "check": "viewer_experience_audience",
                "reason": "audience literacy is outside the candidate-pack contract",
                "value": literacy,
            }
        )

    affect = experience.get("affect_evidence")
    if not isinstance(affect, dict):
        affect = {}
    affect_fields = [str(item) for item in contract.get("affect_evidence_fields") or [] if str(item)]
    missing_affect = [
        field
        for field in affect_fields
        if not isinstance(affect.get(field), str) or not str(affect.get(field)).strip()
    ]
    if missing_affect:
        failures.append(
            {
                "check": "viewer_experience_affect_cause",
                "reason": "affect requires a visible actor, action, target, and consequence",
                "fields": missing_affect,
            }
        )

    reinspection = experience.get("reinspection_reward")
    if not isinstance(reinspection, dict):
        reinspection = {}
    reinspection_mode = str(reinspection.get("mode") or "")
    reinspection_description = str(reinspection.get("description") or "").strip()
    allowed_reinspection = {str(item) for item in allowed.get("reinspection_mode") or []}
    if reinspection_mode not in allowed_reinspection:
        failures.append(
            {
                "check": "viewer_experience_reinspection",
                "reason": "reinspection reward requires one allowed mode",
                "value": reinspection_mode or None,
            }
        )
    elif reinspection_mode == "causal_second_reading" and not reinspection_description:
        failures.append(
            {
                "check": "viewer_experience_reinspection",
                "reason": "causal second reading requires a concrete description",
            }
        )

    conditional = contract.get("conditional_rules") if isinstance(contract.get("conditional_rules"), dict) else {}
    primary_need = str(experience.get("primary_viewer_need") or "")
    attachment_channel = str(experience.get("attachment_channel") or "")
    attachment_needs = {str(item) for item in conditional.get("attachment_required_for_needs") or []}
    if primary_need in attachment_needs and attachment_channel == "none":
        failures.append(
            {
                "check": "viewer_experience_attachment",
                "reason": "the selected viewer need requires a visible attachment channel",
                "primary_viewer_need": primary_need,
            }
        )

    commercial_objective = str(experience.get("commercial_objective") or "")
    creative_direction = pack.get("creative_direction")
    creative_enabled = isinstance(creative_direction, dict) and creative_direction.get("enabled") is True
    if (
        creative_enabled
        and commercial_objective == "none"
        and conditional.get("creative_noncommercial_reinspection_required") is True
        and reinspection_mode != "causal_second_reading"
    ):
        failures.append(
            {
                "check": "viewer_experience_reinspection",
                "reason": "a noncommercial creative-direction run requires one causal second-reading reward",
            }
        )
    if creative_enabled and commercial_objective == "none" and str(experience.get("interpretive_question") or "").strip().lower() == "none":
        failures.append(
            {
                "check": "viewer_experience_question",
                "reason": "a noncommercial creative-direction run requires a resolvable interpretive question",
            }
        )

    evidence = experience.get("prompt_evidence")
    if not isinstance(evidence, dict):
        evidence = {}
    binding = contract.get("prompt_binding") if isinstance(contract.get("prompt_binding"), dict) else {}
    required_evidence_fields = [str(item) for item in binding.get("required_evidence_fields") or [] if str(item)]
    evidence_phrases: list[str] = []
    missing_evidence = []
    for field in required_evidence_fields:
        phrase = str(evidence.get(field) or "").strip()
        if phrase:
            evidence_phrases.append(phrase)
        else:
            missing_evidence.append(field)
    if missing_evidence:
        failures.append(
            {
                "check": "viewer_experience_binding",
                "reason": "viewer experience is missing required visible prompt evidence",
                "fields": missing_evidence,
            }
        )

    conditional_evidence = binding.get("conditional_evidence_fields") if isinstance(binding.get("conditional_evidence_fields"), dict) else {}
    conditional_required: list[str] = []
    if attachment_channel and attachment_channel != "none":
        conditional_required.append(str(conditional_evidence.get("attachment_channel_not_none") or "attachment_phrase"))
    if reinspection_mode == "causal_second_reading":
        conditional_required.append(
            str(conditional_evidence.get("reinspection_mode_causal_second_reading") or "reinspection_reward_phrase")
        )
    commercial_legibility_objectives = {
        str(item) for item in conditional.get("commercial_legibility_required_for_objectives") or []
    }
    if commercial_objective in commercial_legibility_objectives:
        conditional_required.append(
            str(conditional_evidence.get("commercial_objective_comprehend_remember_act") or "commercial_legibility_phrase")
        )
    missing_conditional = []
    for field in conditional_required:
        phrase = str(evidence.get(field) or "").strip()
        if phrase:
            evidence_phrases.append(phrase)
        else:
            missing_conditional.append(field)
    if missing_conditional:
        failures.append(
            {
                "check": "viewer_experience_binding",
                "reason": "viewer experience is missing conditional visible evidence",
                "fields": missing_conditional,
            }
        )

    missing_literal = [phrase for phrase in evidence_phrases if not text_contains_term(prompt_en, phrase)]
    if missing_literal:
        failures.append(
            {
                "check": "viewer_experience_binding",
                "reason": "declared viewer-experience evidence is not literal in prompt_en",
                "phrases": list(dict.fromkeys(missing_literal)),
            }
        )

    outcome_claim_fragments = (
        "viewer feels",
        "audience feels",
        "makes the viewer feel",
        "evokes empathy",
        "creates attachment",
        "emotionally moving",
        "immersive experience",
        "memorable image",
        "trustworthy product",
    )
    weak_evidence_tokens = {
        "anime",
        "beautiful",
        "cinematic",
        "cute",
        "dramatic",
        "emotional",
        "kawaii",
        "moe",
        "photorealistic",
        "subculture",
    }
    invalid_claims = []
    weak_only = []
    youth_morphology = []
    for phrase in evidence_phrases:
        lower = phrase.lower()
        if any(fragment in lower for fragment in outcome_claim_fragments):
            invalid_claims.append(phrase)
        tokens = {token for token in re.findall(r"[a-z]+", lower) if token}
        if tokens and tokens <= weak_evidence_tokens:
            weak_only.append(phrase)
        if attachment_channel != "none" and any(
            fragment in lower
            for fragment in ("baby face", "childlike", "child-like", "youthful proportions", "oversized eyes")
        ):
            youth_morphology.append(phrase)
    if invalid_claims:
        failures.append(
            {
                "check": "viewer_experience_outcome_claim",
                "reason": "prompt evidence must show a visible cause rather than assert a viewer outcome",
                "phrases": invalid_claims,
            }
        )
    if weak_only:
        failures.append(
            {
                "check": "viewer_experience_weak_evidence",
                "reason": "genre labels and style or affect adjectives alone are not viewer-experience evidence",
                "phrases": weak_only,
            }
        )
    if youth_morphology:
        failures.append(
            {
                "check": "viewer_experience_attachment",
                "reason": "face or youth morphology cannot serve as attachment evidence",
                "phrases": youth_morphology,
            }
        )
    return failures


def audit_creative_direction(
    pack: dict[str, Any],
    composed: dict[str, Any],
    prompt_en: str,
) -> list[dict[str, Any]]:
    contract = pack.get("creative_direction")
    if not isinstance(contract, dict) or not contract.get("enabled"):
        return []

    failures: list[dict[str, Any]] = []
    brief = composed.get("creative_brief")
    if not isinstance(brief, dict):
        return [
            {
                "check": "creative_direction",
                "reason": "enabled creative-direction pack requires a creative_brief object",
            }
        ]

    baseline_contract = contract.get("ordinary_baseline") if isinstance(contract.get("ordinary_baseline"), dict) else {}
    minimum_cliches = int(baseline_contract.get("minimum_cliches", 3) or 3)
    ordinary_baseline = nonempty_string_list(brief.get("ordinary_baseline"))
    rejected_cliches = nonempty_string_list(brief.get("rejected_cliches"))
    if len(ordinary_baseline) < minimum_cliches or normalized_unique_count(ordinary_baseline) < minimum_cliches:
        failures.append(
            {
                "check": "creative_direction_baseline",
                "reason": "creative brief must name distinct ordinary first-answer cliches before ideation",
                "minimum": minimum_cliches,
                "actual": len(ordinary_baseline),
            }
        )
    if len(rejected_cliches) < minimum_cliches or normalized_unique_count(rejected_cliches) < minimum_cliches:
        failures.append(
            {
                "check": "creative_direction_cliche_rejection",
                "reason": "creative brief must explicitly reject distinct cliches",
                "minimum": minimum_cliches,
                "actual": len(rejected_cliches),
            }
        )

    proposal_contract = contract.get("proposal_contract") if isinstance(contract.get("proposal_contract"), dict) else {}
    minimum_proposals = int(proposal_contract.get("minimum_proposals", 4) or 4)
    required_proposal_fields = [str(item) for item in proposal_contract.get("required_fields") or [] if str(item)]
    allowed_operator_ids = {
        str(item.get("id"))
        for item in proposal_contract.get("operators") or []
        if isinstance(item, dict) and str(item.get("id") or "")
    }
    proposals = brief.get("proposals")
    if not isinstance(proposals, list):
        proposals = []
    if len(proposals) < minimum_proposals:
        failures.append(
            {
                "check": "creative_direction_proposals",
                "reason": "creative brief has too few concept proposals",
                "minimum": minimum_proposals,
                "actual": len(proposals),
            }
        )

    proposal_by_id: dict[str, dict[str, Any]] = {}
    operator_ids: list[str] = []
    signature_phrases: dict[str, str] = {}
    for index, proposal in enumerate(proposals):
        if not isinstance(proposal, dict):
            failures.append(
                {
                    "check": "creative_direction_proposals",
                    "reason": "every concept proposal must be an object",
                    "index": index,
                }
            )
            continue
        missing = []
        for field in required_proposal_fields:
            value = proposal.get(field)
            if field == "visible_consequences":
                if len(nonempty_string_list(value)) < 2:
                    missing.append(field)
            elif not isinstance(value, str) or not value.strip():
                missing.append(field)
        if missing:
            failures.append(
                {
                    "check": "creative_direction_proposals",
                    "reason": "concept proposal is missing required developed fields",
                    "index": index,
                    "fields": missing,
                }
            )
        proposal_id = str(proposal.get("id") or "").strip()
        operator_id = str(proposal.get("operator_id") or "").strip()
        if proposal_id:
            if proposal_id in proposal_by_id:
                failures.append(
                    {
                        "check": "creative_direction_proposals",
                        "reason": "concept proposal ids must be unique",
                        "id": proposal_id,
                    }
                )
            proposal_by_id[proposal_id] = proposal
            signature_phrases[proposal_id] = str(proposal.get("signature_phrase") or "").strip()
        if operator_id:
            operator_ids.append(operator_id)
            if allowed_operator_ids and operator_id not in allowed_operator_ids:
                failures.append(
                    {
                        "check": "creative_direction_proposals",
                        "reason": "concept proposal uses an operator outside the pack contract",
                        "id": proposal_id or None,
                        "operator_id": operator_id,
                    }
                )
        if "rule_breaks" in proposal or isinstance(proposal.get("rule_break"), (list, dict)):
            failures.append(
                {
                    "check": "creative_direction_rule_break",
                    "reason": "each concept proposal must contain one scalar rule_break, not a stack",
                    "id": proposal_id or None,
                }
            )

    if proposal_contract.get("distinct_operator_ids") and normalized_unique_count(operator_ids) < min(
        minimum_proposals, len(proposals)
    ):
        failures.append(
            {
                "check": "creative_direction_operators",
                "reason": "concept proposals must use distinct concept-move operators",
                "minimum_unique": min(minimum_proposals, len(proposals)),
                "actual_unique": normalized_unique_count(operator_ids),
            }
        )
    nonempty_signatures = [phrase for phrase in signature_phrases.values() if phrase]
    if normalized_unique_count(nonempty_signatures) != len(nonempty_signatures):
        failures.append(
            {
                "check": "creative_direction_proposals",
                "reason": "concept proposal signature phrases must be unique",
            }
        )

    selected_proposal_id = str(brief.get("selected_proposal_id") or "").strip()
    selected_proposal = proposal_by_id.get(selected_proposal_id)
    if not selected_proposal:
        failures.append(
            {
                "check": "creative_direction_selection",
                "reason": "selected_proposal_id must identify exactly one developed proposal",
                "selected_proposal_id": selected_proposal_id or None,
            }
        )
    selected_flags = [
        str(proposal.get("id") or "")
        for proposal in proposals
        if isinstance(proposal, dict) and proposal.get("selected") is True
    ]
    if selected_flags and selected_flags != [selected_proposal_id]:
        failures.append(
            {
                "check": "creative_direction_selection",
                "reason": "proposal selected flags conflict with selected_proposal_id",
                "selected_flags": selected_flags,
                "selected_proposal_id": selected_proposal_id or None,
            }
        )

    selected_signature = signature_phrases.get(selected_proposal_id, "")
    if selected_signature and not text_contains_term(prompt_en, selected_signature):
        failures.append(
            {
                "check": "creative_direction_binding",
                "reason": "selected proposal signature phrase is not literal in prompt_en",
                "phrase": selected_signature,
            }
        )
    mixed_signatures = [
        phrase
        for proposal_id, phrase in signature_phrases.items()
        if proposal_id != selected_proposal_id and phrase and text_contains_term(prompt_en, phrase)
    ]
    if mixed_signatures:
        failures.append(
            {
                "check": "creative_direction_selection",
                "reason": "prompt_en mixes signature phrases from unselected proposals",
                "phrases": mixed_signatures,
            }
        )

    selected_contract = (
        contract.get("selected_concept_contract")
        if isinstance(contract.get("selected_concept_contract"), dict)
        else {}
    )
    selected_concept = brief.get("selected_concept")
    if not isinstance(selected_concept, dict):
        failures.append(
            {
                "check": "creative_direction_selection",
                "reason": "creative brief requires a selected_concept object",
            }
        )
        return failures
    required_selected_fields = [str(item) for item in selected_contract.get("required_fields") or [] if str(item)]
    missing_selected_fields = [field for field in required_selected_fields if field not in selected_concept]
    if missing_selected_fields:
        failures.append(
            {
                "check": "creative_direction_selection",
                "reason": "selected concept is missing required fields",
                "fields": missing_selected_fields,
            }
        )
    if str(selected_concept.get("proposal_id") or "") != selected_proposal_id:
        failures.append(
            {
                "check": "creative_direction_selection",
                "reason": "selected concept proposal_id does not match selected_proposal_id",
            }
        )
    if "rule_breaks" in selected_concept or not isinstance(selected_concept.get("rule_break"), str):
        failures.append(
            {
                "check": "creative_direction_rule_break",
                "reason": "selected concept must contain exactly one scalar rule_break",
            }
        )
    if selected_proposal:
        for field in ("familiar_anchor", "rule_break", "aboutness"):
            if str(selected_concept.get(field) or "").strip() != str(selected_proposal.get(field) or "").strip():
                failures.append(
                    {
                        "check": "creative_direction_selection",
                        "reason": "selected concept diverges from the chosen proposal",
                        "field": field,
                    }
                )
        if nonempty_string_list(selected_concept.get("visible_consequences")) != nonempty_string_list(
            selected_proposal.get("visible_consequences")
        ):
            failures.append(
                {
                    "check": "creative_direction_selection",
                    "reason": "selected concept consequence chain diverges from the chosen proposal",
                    "field": "visible_consequences",
                }
            )

    minimum_consequences = int(selected_contract.get("minimum_visible_consequences", 2) or 2)
    consequences = nonempty_string_list(selected_concept.get("visible_consequences"))
    if len(consequences) < minimum_consequences or normalized_unique_count(consequences) < minimum_consequences:
        failures.append(
            {
                "check": "creative_direction_consequences",
                "reason": "selected rule break needs distinct visible consequences",
                "minimum": minimum_consequences,
                "actual": len(consequences),
            }
        )
    minimum_reveal_steps = int(selected_contract.get("minimum_reveal_steps", 3) or 3)
    reveal_path = nonempty_string_list(selected_concept.get("reveal_path"))
    if len(reveal_path) < minimum_reveal_steps or normalized_unique_count(reveal_path) < minimum_reveal_steps:
        failures.append(
            {
                "check": "creative_direction_reveal",
                "reason": "selected concept needs a staged viewer discovery path",
                "minimum": minimum_reveal_steps,
                "actual": len(reveal_path),
            }
        )

    grammar_fields = [str(item) for item in selected_contract.get("authorial_grammar_fields") or [] if str(item)]
    authorial_grammar = selected_concept.get("authorial_grammar")
    if not isinstance(authorial_grammar, dict):
        authorial_grammar = {}
    missing_grammar = [
        field
        for field in grammar_fields
        if not isinstance(authorial_grammar.get(field), str) or not str(authorial_grammar.get(field)).strip()
    ]
    if missing_grammar:
        failures.append(
            {
                "check": "creative_direction_authorial_grammar",
                "reason": "authorial voice must be expressed as concrete frame, time, omission, and material decisions",
                "fields": missing_grammar,
            }
        )

    evidence = selected_concept.get("prompt_evidence")
    if not isinstance(evidence, dict):
        failures.append(
            {
                "check": "creative_direction_binding",
                "reason": "selected concept requires literal prompt_evidence",
            }
        )
        return failures

    scalar_evidence_fields = ("familiar_anchor_phrase", "rule_break_phrase")
    evidence_phrases: list[str] = []
    for field in scalar_evidence_fields:
        phrase = str(evidence.get(field) or "").strip()
        if not phrase:
            failures.append(
                {
                    "check": "creative_direction_binding",
                    "reason": "prompt evidence field is missing",
                    "field": field,
                }
            )
        else:
            evidence_phrases.append(phrase)
    for field, minimum in (("visible_consequence_phrases", minimum_consequences), ("reveal_path_phrases", minimum_reveal_steps)):
        phrases = nonempty_string_list(evidence.get(field))
        if len(phrases) < minimum:
            failures.append(
                {
                    "check": "creative_direction_binding",
                    "reason": "prompt evidence list is too short",
                    "field": field,
                    "minimum": minimum,
                    "actual": len(phrases),
                }
            )
        evidence_phrases.extend(phrases)

    grammar_evidence = evidence.get("authorial_grammar_phrases")
    if not isinstance(grammar_evidence, dict):
        grammar_evidence = {}
    missing_grammar_evidence = [
        field
        for field in grammar_fields
        if not isinstance(grammar_evidence.get(field), str) or not str(grammar_evidence.get(field)).strip()
    ]
    if missing_grammar_evidence:
        failures.append(
            {
                "check": "creative_direction_binding",
                "reason": "each authorial grammar decision requires literal prompt evidence",
                "fields": missing_grammar_evidence,
            }
        )
    evidence_phrases.extend(
        str(grammar_evidence.get(field) or "").strip()
        for field in grammar_fields
        if str(grammar_evidence.get(field) or "").strip()
    )

    missing_literal_phrases = [phrase for phrase in evidence_phrases if not text_contains_term(prompt_en, phrase)]
    if missing_literal_phrases:
        failures.append(
            {
                "check": "creative_direction_binding",
                "reason": "declared creative evidence is not literal in prompt_en",
                "phrases": list(dict.fromkeys(missing_literal_phrases)),
            }
        )
    if normalized_unique_count(evidence_phrases) != len(evidence_phrases):
        failures.append(
            {
                "check": "creative_direction_binding",
                "reason": "creative evidence fields must point to distinct visible decisions",
            }
        )

    touch = pack.get("artistic_final_touch") if isinstance(pack.get("artistic_final_touch"), dict) else {}
    final_touch = str(touch.get("final_sentence_en") or "").strip().lower()
    borrowed_touch_phrases = [
        phrase
        for phrase in grammar_evidence.values()
        if isinstance(phrase, str)
        and phrase.strip()
        and final_touch
        and (phrase.strip().lower() in final_touch or final_touch in phrase.strip().lower())
    ]
    if borrowed_touch_phrases:
        failures.append(
            {
                "check": "creative_direction_authorial_grammar",
                "reason": "fixed artistic_final_touch wording is surface craft, not evidence of authorial voice",
                "phrases": borrowed_touch_phrases,
            }
        )
    return failures


def audit_hybrid_augmentation(
    pack: dict[str, Any],
    composed: dict[str, Any],
    prompt_en: str,
    chosen: set[str],
    candidate_objects: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    contract = pack.get("hybrid_augmentation")
    if not isinstance(contract, dict) or not contract.get("enabled"):
        return [], []

    failures: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    brief = composed.get("augmentation_brief")
    if not isinstance(brief, dict):
        return [
            {
                "check": "hybrid_augmentation",
                "reason": "enabled hybrid candidate pack requires augmentation_brief",
            }
        ], []

    if not str(brief.get("concept_core") or "").strip():
        failures.append(
            {
                "check": "hybrid_augmentation_core",
                "reason": "augmentation_brief requires an agent-authored concept_core",
            }
        )

    route_contract = contract.get("route_contract") if isinstance(contract.get("route_contract"), dict) else {}
    routes = [route for route in route_contract.get("routes") or [] if isinstance(route, dict)]
    route_map = {str(route.get("id") or ""): route for route in routes if str(route.get("id") or "")}
    expected_route_ids = set(route_map)
    considered = [row for row in brief.get("routes_considered") or [] if isinstance(row, dict)]
    considered_ids = [str(row.get("route_id") or "") for row in considered]
    if set(considered_ids) != expected_route_ids or len(considered_ids) != len(set(considered_ids)):
        failures.append(
            {
                "check": "hybrid_augmentation_routes",
                "reason": "routes_considered must cover every exposed route exactly once",
                "expected": sorted(expected_route_ids),
                "actual": considered_ids,
            }
        )
    selected_route_id = str(brief.get("selected_route_id") or "")
    selected_rows = [row for row in considered if str(row.get("decision") or "") == "selected"]
    invalid_route_decisions = [
        row
        for row in considered
        if str(row.get("decision") or "") not in {"selected", "rejected"}
        or not str(row.get("reason") or "").strip()
    ]
    if invalid_route_decisions:
        failures.append(
            {
                "check": "hybrid_augmentation_routes",
                "reason": "every route requires selected/rejected plus a non-empty reason",
            }
        )
    if selected_route_id == "none":
        if selected_rows or not str(brief.get("all_rejected_reason") or "").strip():
            failures.append(
                {
                    "check": "hybrid_augmentation_selection",
                    "reason": "selecting none requires every route rejected and all_rejected_reason",
                }
            )
    elif selected_route_id not in route_map or len(selected_rows) != 1 or str(selected_rows[0].get("route_id") or "") != selected_route_id:
        failures.append(
            {
                "check": "hybrid_augmentation_selection",
                "reason": "select exactly one exposed route, or use selected_route_id none",
                "selected_route_id": selected_route_id or None,
            }
        )

    adoption = contract.get("adoption_contract") if isinstance(contract.get("adoption_contract"), dict) else {}
    allowed_states = {str(item) for item in adoption.get("decision_states") or []}
    allowed_functions = {str(item) for item in adoption.get("detail_functions") or []}
    decisions = [row for row in brief.get("decisions") or [] if isinstance(row, dict)]
    decision_ids = [str(row.get("candidate_id") or "") for row in decisions]
    if len(decision_ids) != len(set(decision_ids)):
        failures.append(
            {
                "check": "hybrid_augmentation_decisions",
                "reason": "each route candidate may have only one decision",
            }
        )
    selected_candidate_ids = (
        {str(item) for item in (route_map.get(selected_route_id) or {}).get("candidate_ids") or []}
        if selected_route_id in route_map
        else set()
    )
    if selected_route_id in route_map and set(decision_ids) != selected_candidate_ids:
        failures.append(
            {
                "check": "hybrid_augmentation_decisions",
                "reason": "every selected-route candidate requires an explicit decision",
                "expected": sorted(selected_candidate_ids),
                "actual": sorted(set(decision_ids)),
            }
        )
    if selected_route_id == "none" and decisions:
        failures.append(
            {
                "check": "hybrid_augmentation_decisions",
                "reason": "no candidate decisions are allowed when all routes are rejected",
            }
        )

    accepted_ids: set[str] = set()
    for decision in decisions:
        candidate_id = str(decision.get("candidate_id") or "")
        state = str(decision.get("decision") or "")
        function = str(decision.get("function") or "")
        if candidate_id not in selected_candidate_ids:
            failures.append(
                {
                    "check": "hybrid_augmentation_decisions",
                    "reason": "decision references a candidate outside the selected route",
                    "candidate_id": candidate_id,
                }
            )
            continue
        if state not in allowed_states:
            failures.append(
                {
                    "check": "hybrid_augmentation_decisions",
                    "reason": "unknown augmentation decision state",
                    "candidate_id": candidate_id,
                    "decision": state,
                }
            )
        if function not in allowed_functions:
            failures.append(
                {
                    "check": "hybrid_augmentation_decisions",
                    "reason": "unknown augmentation detail function",
                    "candidate_id": candidate_id,
                    "function": function,
                }
            )
        if not str(decision.get("rationale") or "").strip() or not str(
            decision.get("marginal_contribution") or ""
        ).strip():
            failures.append(
                {
                    "check": "hybrid_augmentation_marginal_value",
                    "reason": "every decision requires rationale and marginal_contribution",
                    "candidate_id": candidate_id,
                }
            )
        if state in {"accepted", "modified"}:
            accepted_ids.add(candidate_id)
            evidence = str(decision.get("prompt_evidence") or "").strip()
            if candidate_id not in chosen:
                failures.append(
                    {
                        "check": "hybrid_augmentation_provenance",
                        "reason": "accepted or modified augmentation candidate is missing from chosen_candidate_ids",
                        "candidate_id": candidate_id,
                    }
                )
            if not evidence or not text_contains_term(prompt_en, evidence):
                failures.append(
                    {
                        "check": "hybrid_augmentation_binding",
                        "reason": "accepted or modified detail requires literal prompt_evidence",
                        "candidate_id": candidate_id,
                        "prompt_evidence": evidence or None,
                    }
                )
            if state == "modified" and not str(decision.get("modification") or "").strip():
                failures.append(
                    {
                        "check": "hybrid_augmentation_decisions",
                        "reason": "modified detail requires a modification description",
                        "candidate_id": candidate_id,
                    }
                )
        elif state == "rejected" and candidate_id in chosen:
            failures.append(
                {
                    "check": "hybrid_augmentation_provenance",
                    "reason": "rejected augmentation candidate must not be chosen",
                    "candidate_id": candidate_id,
                }
            )

    if selected_route_id in route_map:
        try:
            accepted_min = int(adoption.get("minimum_accepted_if_selected", 2) or 2)
        except (TypeError, ValueError):
            accepted_min = 2
        try:
            accepted_max = int(adoption.get("maximum_accepted", 5) or 5)
        except (TypeError, ValueError):
            accepted_max = 5
        if len(accepted_ids) < accepted_min or len(accepted_ids) > accepted_max:
            failures.append(
                {
                    "check": "hybrid_augmentation_budget",
                    "reason": "accepted augmentation detail count is outside the declared budget",
                    "minimum": accepted_min,
                    "maximum": accepted_max,
                    "actual": len(accepted_ids),
                }
            )

    adult_contract = contract.get("adult_appeal") if isinstance(contract.get("adult_appeal"), dict) else {}
    if adult_contract.get("enabled"):
        adult_brief = brief.get("adult_appeal")
        if not isinstance(adult_brief, dict):
            failures.append(
                {
                    "check": "adult_appeal",
                    "reason": "active adult-appeal axes require augmentation_brief.adult_appeal",
                }
            )
            return failures, warnings
        adult_subject_phrase = str(adult_brief.get("adult_subject_phrase") or "").strip()
        agency_phrase = str(adult_brief.get("agency_phrase") or "").strip()
        if (
            not adult_subject_phrase
            or not text_contains_term(prompt_en, adult_subject_phrase)
            or not re.search(r"\badult\b", adult_subject_phrase, flags=re.IGNORECASE)
        ):
            failures.append(
                {
                    "check": "adult_appeal_adult_subject",
                    "reason": "adult_subject_phrase must be literal in prompt_en and explicitly say adult",
                }
            )
        if not agency_phrase or not text_contains_term(prompt_en, agency_phrase):
            failures.append(
                {
                    "check": "adult_appeal_agency",
                    "reason": "agency_phrase must be literal in prompt_en",
                }
            )
        expected_axes = adult_contract.get("axes") if isinstance(adult_contract.get("axes"), dict) else {}
        actual_axes = adult_brief.get("axes") if isinstance(adult_brief.get("axes"), dict) else {}
        for axis_id, axis_contract in expected_axes.items():
            if not isinstance(axis_contract, dict):
                continue
            expected_intensity = int(axis_contract.get("intensity", 0) or 0)
            actual_axis = actual_axes.get(axis_id) if isinstance(actual_axes.get(axis_id), dict) else {}
            try:
                actual_intensity = int(actual_axis.get("intensity", -1))
            except (TypeError, ValueError):
                actual_intensity = -1
            if actual_intensity != expected_intensity:
                failures.append(
                    {
                        "check": "adult_appeal_axes",
                        "reason": "composed adult-appeal intensity differs from the explicit candidate-pack axis",
                        "axis": axis_id,
                        "expected": expected_intensity,
                        "actual": actual_intensity,
                    }
                )
            if expected_intensity > 0:
                inventory_ids = {
                    str(candidate.get("id") or "")
                    for candidate in axis_contract.get("candidate_inventory") or []
                    if isinstance(candidate, dict) and str(candidate.get("id") or "")
                }
                if not (accepted_ids & inventory_ids):
                    failures.append(
                        {
                            "check": "adult_appeal_axes",
                            "reason": "every active adult-appeal axis requires one accepted or modified candidate",
                            "axis": axis_id,
                        }
                    )
        expected_emphasis = str((adult_contract.get("blend") or {}).get("emphasis") or "")
        actual_emphasis = str((adult_brief.get("blend") or {}).get("emphasis") or "") if isinstance(adult_brief.get("blend"), dict) else ""
        if actual_emphasis != expected_emphasis:
            failures.append(
                {
                    "check": "adult_appeal_blend",
                    "reason": "composed blend emphasis differs from the candidate pack",
                    "expected": expected_emphasis,
                    "actual": actual_emphasis or None,
                }
            )

        combination = adult_contract.get("combination_policy") if isinstance(adult_contract.get("combination_policy"), dict) else {}
        risk_hits: set[str] = set()
        risk_groups = combination.get("risk_groups") if isinstance(combination.get("risk_groups"), dict) else {}
        chosen_entry_ids = {
            str(candidate_objects.get(candidate_id, {}).get("entry_id") or "")
            for candidate_id in chosen
        }
        for group_id, group in risk_groups.items():
            if not isinstance(group, dict):
                continue
            entry_ids = {str(item) for item in group.get("entry_ids") or []}
            prompt_terms = [str(item) for item in group.get("prompt_terms") or []]
            if chosen_entry_ids & entry_ids or any(text_contains_term(prompt_en, term) for term in prompt_terms):
                risk_hits.add(str(group_id))
        for rule in combination.get("hard_combinations") or []:
            if not isinstance(rule, dict):
                continue
            required = {str(item) for item in rule.get("all_of") or []}
            if required and required <= risk_hits:
                failures.append(
                    {
                        "check": "adult_appeal_combination_risk",
                        "reason": str(rule.get("reason") or "high-risk styling and camera combination"),
                        "rule_id": rule.get("id"),
                        "risk_groups": sorted(required),
                    }
                )
        for rule in combination.get("warning_combinations") or []:
            if not isinstance(rule, dict):
                continue
            required = {str(item) for item in rule.get("all_of") or []}
            if required and required <= risk_hits:
                warnings.append(
                    {
                        "check": "adult_appeal_combination_risk",
                        "reason": str(rule.get("reason") or "stacked adult-fashion emphasis"),
                        "rule_id": rule.get("id"),
                        "risk_groups": sorted(required),
                    }
                )

    return failures, warnings


def audit_composed_prompt(pack: dict[str, Any], composed: dict[str, Any]) -> dict[str, Any]:
    failures: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    prompt_en = str(composed.get("prompt_en") or "")
    search_text = composed_search_text(composed)
    negative_en = composed.get("negative_en")

    required_fields = ("pack_id", "prompt_en", "negative_en", "chosen_candidate_ids", "composer")
    missing_fields = [field for field in required_fields if field not in composed]
    if missing_fields:
        failures.append({"check": "output_contract", "reason": "missing required fields", "fields": missing_fields})
    if not prompt_en.strip():
        failures.append({"check": "output_contract", "reason": "missing prompt_en"})
    if composed.get("composer") != "agent":
        failures.append({"check": "output_contract", "reason": "composer must equal agent"})

    pack_id = str(pack.get("pack_id") or "")
    composed_pack_id = str(composed.get("pack_id") or "")
    expected_pack_id = computed_pack_id(pack)
    if not pack_id or pack_id != expected_pack_id:
        failures.append(
            {
                "check": "pack_integrity",
                "reason": "candidate pack content does not match pack_id",
                "expected": expected_pack_id,
                "actual": pack_id or None,
            }
        )
    if composed_pack_id != pack_id:
        failures.append({"check": "pack_id", "reason": "pack_id mismatch", "expected": pack_id, "actual": composed_pack_id})

    pack_negative = pack.get("negative_en")
    if negative_en != pack_negative:
        failures.append({"check": "negative_en", "reason": "negative_en differs from candidate pack"})

    failures.extend(audit_creative_direction(pack, composed, prompt_en))
    failures.extend(audit_viewer_experience(pack, composed, prompt_en))

    safety = pack.get("safety") if isinstance(pack.get("safety"), dict) else {}
    if safety.get("status") != "pass" or safety.get("requires_user_approval") is True:
        failures.append({"check": "safety", "reason": "candidate pack safety contract is not pass", "safety": safety})
    failed_gates = [
        gate
        for gate in pack.get("concept_gates") or []
        if isinstance(gate, dict) and gate.get("status") != "pass"
    ]
    if failed_gates:
        failures.append({"check": "concept_gates", "reason": "candidate pack contains a failed concept gate", "gates": failed_gates})

    mandatory_texts = {
        str(intent.get("text") or "")
        for intent in pack.get("mandatory_intents") or []
        if isinstance(intent, dict) and str(intent.get("text") or "")
    }
    assertions = composed.get("coverage_assertions")
    if assertions is not None and not isinstance(assertions, dict):
        failures.append({"check": "coverage_assertions", "reason": "coverage_assertions must be an object"})
    elif isinstance(assertions, dict):
        for key, raw in assertions.items():
            if str(key) not in mandatory_texts:
                failures.append({"check": "coverage_assertions", "reason": "assertion key is not a mandatory intent", "intent": key})
            for phrase in assertion_values(raw):
                if not text_contains_term(prompt_en, phrase):
                    failures.append(
                        {
                            "check": "coverage_assertions",
                            "reason": "asserted phrase is not literal in prompt_en",
                            "intent": key,
                            "phrase": phrase,
                        }
                    )

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
        failures.append({"check": "chosen_candidate_ids", "reason": "no chosen_candidate_ids supplied"})
    invalid = sorted(candidate_id for candidate_id in chosen if candidate_id not in valid_ids)
    if invalid:
        failures.append({"check": "chosen_candidate_ids", "reason": "unknown candidate id", "ids": invalid})

    candidate_objects = candidate_objects_from_pack(pack)
    ineligible = []
    for candidate_id in sorted(chosen):
        candidate = candidate_objects.get(candidate_id)
        if not isinstance(candidate, dict):
            continue
        applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
        if applicability and applicability.get("status") != "eligible":
            ineligible.append(
                {
                    "id": candidate_id,
                    "status": applicability.get("status"),
                    "reason": applicability.get("reason"),
                }
            )
    if ineligible:
        failures.append(
            {
                "check": "candidate_applicability",
                "reason": "chosen candidate is not eligible for this request",
                "candidates": ineligible,
            }
        )

    hybrid_failures, hybrid_warnings = audit_hybrid_augmentation(
        pack,
        composed,
        prompt_en,
        chosen,
        candidate_objects,
    )
    failures.extend(hybrid_failures)
    warnings.extend(hybrid_warnings)

    coverage = pack.get("coverage") if isinstance(pack.get("coverage"), dict) else {}
    intent_constraints = coverage.get("intent_constraints") if isinstance(coverage.get("intent_constraints"), dict) else {}
    no_people = bool(intent_constraints.get("no_people")) or any(
        isinstance(intent, dict) and "no_people" in (intent.get("constraints") or [])
        for intent in pack.get("intent_contract") or []
    )
    if no_people:
        person_only_slots = {
            "appearance_type",
            "body_framing",
            "body_orientation",
            "body_pose",
            "brow_style",
            "costume_style",
            "eye_detail",
            "eye_makeup_line",
            "facial_hair",
            "footwear",
            "gaze_engagement",
            "hair_color",
            "hair_style",
            "hand_pose",
            "lip_finish",
            "makeup_style",
            "person_origin",
            "silhouette_proportion",
            "skin_finish",
            "wardrobe_style",
        }
        violations: list[dict[str, Any]] = []
        for candidate_id in sorted(chosen):
            candidate = candidate_objects.get(candidate_id)
            if not isinstance(candidate, dict) or not str(candidate.get("slot") or ""):
                continue
            slot = str(candidate.get("slot") or "")
            tokens = {
                str(item).lower()
                for item in [*(candidate.get("kind") or []), *(candidate.get("tags") or [])]
            }
            if slot in person_only_slots or "human" in tokens:
                violations.append({"id": candidate_id, "slot": slot, "tokens": sorted(tokens)[:12]})
        if violations:
            failures.append(
                {
                    "check": "negative_presence_constraint",
                    "reason": "no-people request contains person-only chosen candidates",
                    "candidates": violations,
                }
            )

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
        open_slot_name = str(open_slot.get("slot") or "")
        chosen_hit = bool(open_slot_name) and any(
            candidate_id.startswith(f"slot:{open_slot_name}:") for candidate_id in chosen
        )
        text_hits = [term for term in terms if text_contains_term(search_text, term)]
        if chosen_hit or text_hits:
            masked_echo_count += 1
            failures.append(
                {
                    "check": "masked_bucket_echo",
                    "reason": "masked/open preset section was copied back into the composed prompt",
                    "slot": open_slot.get("slot"),
                    "bucket": open_slot.get("bucket"),
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
    scene_contract = pack.get("scene_contract") if isinstance(pack.get("scene_contract"), dict) else {}
    for group in scene_contract.get("groups") or []:
        if not isinstance(group, dict) or str(group.get("strategy") or "") != "atomic_scene":
            continue
        if str(group.get("source") or "") == "selected_render_blueprint":
            for slot in group.get("required_slots") or []:
                slot_contract = (group.get("slots") or {}).get(str(slot))
                if not isinstance(slot_contract, dict):
                    failures.append(
                        {
                            "check": "atomic_scene_contract",
                            "reason": "resolved render scene is missing a required atomic slot",
                            "group": group.get("group"),
                            "slot": str(slot),
                        }
                    )
                    continue
                terms = [
                    str(term)
                    for term in slot_contract.get("audit_terms") or []
                    if str(term).strip()
                ]
                if not terms or not any(text_contains_term(prompt_en, term) for term in terms):
                    failures.append(
                        {
                            "check": "atomic_scene_contract",
                            "reason": "mandatory resolved render atom is absent from prompt_en",
                            "group": group.get("group"),
                            "slot": str(slot),
                            "accepted_terms": terms,
                        }
                    )
            controlled_slots = {
                str(slot)
                for slot in group.get("controlled_candidate_slots") or []
                if str(slot)
            }
            mixed_slots = sorted(slot for slot in controlled_slots if chosen_slots.get(slot))
            if mixed_slots:
                failures.append(
                    {
                        "check": "atomic_scene_contract",
                        "reason": "ordinary sampler candidates cannot override resolved render atoms",
                        "group": group.get("group"),
                        "slots": mixed_slots,
                    }
                )
            continue
        for slot in group.get("required_slots") or []:
            if not chosen_slots.get(str(slot)):
                failures.append(
                    {
                        "check": "atomic_scene_contract",
                        "reason": "required atomic-scene slot was not chosen",
                        "group": group.get("group"),
                        "slot": str(slot),
                    }
                )
        for slot, slot_contract in (group.get("slots") or {}).items():
            if not isinstance(slot_contract, dict):
                continue
            allowed_ids = {str(item) for item in slot_contract.get("allowed_entry_ids") or []}
            selected_ids = chosen_slots.get(str(slot), set())
            outside = sorted(selected_ids - allowed_ids) if allowed_ids else sorted(selected_ids)
            if outside:
                failures.append(
                    {
                        "check": "atomic_scene_contract",
                        "reason": "chosen candidate crosses the selected scene variant boundary",
                        "group": group.get("group"),
                        "slot": str(slot),
                        "ids": outside,
                        "allowed_ids": sorted(allowed_ids),
                    }
                )
    evidence_budget = pack.get("evidence_budget") if isinstance(pack.get("evidence_budget"), dict) else {}
    if evidence_budget.get("enabled"):
        clue_slots = {str(item) for item in evidence_budget.get("world_clue_slots") or [] if str(item)}
        render_contract = pack.get("render_contract") if isinstance(pack.get("render_contract"), dict) else {}
        selected_scene = render_contract.get("selected_scene") if isinstance(render_contract.get("selected_scene"), dict) else {}
        atomic_scene = selected_scene.get("atomic_scene") if isinstance(selected_scene.get("atomic_scene"), dict) else {}
        chosen_clue_slots = sorted(
            slot
            for slot in clue_slots
            if chosen_slots.get(slot) or isinstance(atomic_scene.get(slot), dict)
        )
        try:
            minimum_chosen = int(evidence_budget.get("minimum_chosen", 0))
            maximum_chosen = int(evidence_budget.get("maximum_chosen", len(clue_slots)))
        except (TypeError, ValueError):
            minimum_chosen, maximum_chosen = 0, len(clue_slots)
        if len(chosen_clue_slots) < minimum_chosen or len(chosen_clue_slots) > maximum_chosen:
            failures.append(
                {
                    "check": "evidence_budget",
                    "reason": "chosen world-clue slots fall outside the sparse evidence budget",
                    "chosen_slots": chosen_clue_slots,
                    "minimum_chosen": minimum_chosen,
                    "maximum_chosen": maximum_chosen,
                }
            )
    render_contract = pack.get("render_contract") if isinstance(pack.get("render_contract"), dict) else {}
    selected_scene = render_contract.get("selected_scene") if isinstance(render_contract.get("selected_scene"), dict) else {}
    visual_provenance = [
        str(item)
        for item in selected_scene.get("diegetic_visual_provenance") or []
        if str(item).strip()
    ]
    if render_contract.get("enabled") and len(set(visual_provenance)) > 1:
        failures.append(
            {
                "check": "diegetic_visual_provenance",
                "reason": "selected atomic scene carries multiple visual provenance values",
                "values": sorted(set(visual_provenance)),
            }
        )
    character_grammar = (
        pack.get("character_grammar")
        if isinstance(pack.get("character_grammar"), dict)
        else {}
    )
    if character_grammar.get("enabled"):
        runtime_nodes = [
            item
            for item in character_grammar.get("runtime_nodes") or []
            if isinstance(item, dict)
        ]
        max_support_cues = int(character_grammar.get("max_support_cues", 2) or 2)
        primary_nodes = [item for item in runtime_nodes if item.get("role") == "primary"]
        support_nodes = [item for item in runtime_nodes if item.get("role") == "support"]
        runtime_ids = {str(item.get("id") or "") for item in runtime_nodes}
        primary_runtime_id = (
            str(primary_nodes[0].get("id") or "")
            if len(primary_nodes) == 1
            else ""
        )
        if (
            character_grammar.get("valid") is not True
            or len(primary_nodes) != 1
            or not primary_runtime_id
            or len(support_nodes) > max_support_cues
            or len(runtime_nodes) != len(runtime_ids)
        ):
            failures.append(
                {
                    "check": "character_grammar_contract",
                    "reason": "character runtime bundle violates the one-primary sparse support contract",
                    "primary_runtime_id": primary_runtime_id,
                    "runtime_ids": sorted(runtime_ids),
                    "support_count": len(support_nodes),
                    "max_support_cues": max_support_cues,
                }
            )
        if len(runtime_nodes) > 1 and character_grammar.get("compatible_bundle") is not True:
            failures.append(
                {
                    "check": "character_grammar_contract",
                    "reason": "multi-node character runtime bundle is not declared compatible",
                }
            )
        scene_evidence = {
            str(item)
            for item in selected_scene.get("visual_evidence_types") or []
            if str(item)
        }
        grammar_evidence = {
            str(item)
            for item in character_grammar.get("visual_evidence_types") or []
            if str(item)
        }
        required_evidence = {
            str(item)
            for item in character_grammar.get("required_visual_evidence_types") or []
            if str(item)
        }
        if (
            not scene_evidence
            or scene_evidence != grammar_evidence
            or not required_evidence.issubset(scene_evidence)
        ):
            failures.append(
                {
                    "check": "character_grammar_contract",
                    "reason": "selected scene and character grammar visual evidence types are missing or inconsistent",
                    "scene_evidence": sorted(scene_evidence),
                    "grammar_evidence": sorted(grammar_evidence),
                    "required_evidence": sorted(required_evidence),
                }
            )
        constraints = (
            character_grammar.get("composition_constraints")
            if isinstance(character_grammar.get("composition_constraints"), dict)
            else {}
        )
        if (
            constraints.get("explicit_adult_original_subject") != "required"
            or constraints.get("observable_evidence") != "required"
            or constraints.get("appearance_inference_from_route") != "forbidden"
            or constraints.get("protected_identity_replication") != "forbidden"
        ):
            failures.append(
                {
                    "check": "character_grammar_contract",
                    "reason": "character route is missing generic composition constraints",
                }
            )
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
        if allowed_locations and not selected_locations and role_scene_policy.get("enforce"):
            failures.append(
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
            if allowed_ids and not selected_ids:
                failures.append(
                    {
                        "check": "species_family",
                        "reason": "required species-family slot candidate id is missing",
                        "slot": str(slot),
                        "allowed_ids": sorted(allowed_ids),
                        "family": species_policy.get("family"),
                        "variant_id": species_policy.get("variant_id"),
                    }
                )
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
    quality_status = "warn" if warnings else "pass"
    return {
        "status": status,
        "quality_status": quality_status,
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
