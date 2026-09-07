#!/usr/bin/env python3
"""Audit an agent-composed photo prompt against a candidate pack."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Sequence


_SCRIPTS_IMPORT_DIR = str(Path(__file__).resolve().parent)
_SCRIPTS_IMPORT_DIR_ADDED = _SCRIPTS_IMPORT_DIR not in sys.path
if _SCRIPTS_IMPORT_DIR_ADDED:
    sys.path.insert(0, _SCRIPTS_IMPORT_DIR)
try:
    import photo_candidate_semantics
    import prompt_generator as candidate_semantics_generator
    from photo_contracts import (
        AUTHORIAL_AUTHORSHIP_POLICY_CONTRACT_VERSION,
        AUTHORIAL_CORE_BINDING_CONTRACT_VERSION,
        AUTHORIAL_CORE_CONTRACT_VERSION,
        AUTHORIAL_CORE_MODERN_CONTRACT_VERSIONS,
        AUTHORIAL_CORE_V3_CONTRACT_VERSION,
        AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS,
        AUTHORIAL_IDENTITY_PRESERVATION_NEGATIVE_TERMS,
        AUTHORIAL_INTENT_NEUTRAL_NEGATIVE_TERMS,
        AUTHORIAL_PROMPT_ABSOLUTE_MAX_WORDS,
        AUTHORIAL_PROMPT_BUDGET_CONTRACT_VERSION,
        AUTHORIAL_PROMPT_MIN_WORDS,
        AUTHORIAL_PROMPT_RECOMMENDED_MAX_WORDS,
        AUTHORIAL_PROMPT_REQUIRED_EVIDENCE_HEADROOM_WORDS,
        CHARACTER_RESPONSE_CONTRACT_VERSION,
        CHARACTER_RESPONSE_RELATION_MEMBERS,
        CHARACTER_RESPONSE_REQUIRED_AXES,
        CHARACTER_RESPONSE_REQUIRED_EVIDENCE,
        DOWNSTREAM_INTENT_PRECEDENCE_CONTRACT_VERSION,
        INTENT_LOCK_CONTRACT_VERSION,
        INTENT_LOCK_DIMENSIONS,
        INTENT_PRESERVATION_CONTRACT_VERSION,
        LEGACY_AUTHORIAL_CORE_CONTRACT_VERSION,
        NEGATIVE_INTENT_GUARD_CONTRACT_VERSION,
        RENDER_REPAIR_ALLOWED_AXES,
        RENDER_REPAIR_CONTACT_EXPECTATIONS,
        RENDER_REPAIR_CONTRACT_VERSION,
        RENDER_REPAIR_DIMENSION_AXES,
        RENDER_REPAIR_IMPORTANCE_VALUES,
        RENDER_REPAIR_INTERACTION_STATES,
        RENDER_REPAIR_RELATION_ORIGINS,
        REQUEST_BINDING_CONTRACT_VERSION,
        REQUEST_ENVELOPE_CONTRACT_VERSION,
        REQUEST_LINEAGE_V2_CONTRACT_VERSION,
        REQUIRED_INTENT_LOCK_DIMENSIONS,
        SEMANTIC_ASSERTION_OBLIGATIONS_CONTRACT_VERSION,
        canonical_json_sha256,
    )
finally:
    if _SCRIPTS_IMPORT_DIR_ADDED:
        sys.path.remove(_SCRIPTS_IMPORT_DIR)


SUPPORTED_CANDIDATE_PACK_VERSIONS = {
    "photo-candidate-pack/v2",
    "photo-candidate-pack/v3",
    "photo-candidate-pack/v4",
    "photo-candidate-pack/v5",
    "photo-candidate-pack/v6",
}
MOE_PROMPT_DEFAULT_RECOMMENDED_MIN_WORDS = 100
MOE_PROMPT_DEFAULT_RECOMMENDED_MAX_WORDS = 240
LEGACY_AUTHORIAL_PROMPT_MIN_WORDS = 24
LEGACY_AUTHORIAL_PROMPT_RECOMMENDED_MAX_WORDS = 180
LEGACY_AUTHORIAL_PROMPT_ABSOLUTE_MAX_WORDS = 320
LEGACY_AUTHORIAL_PROMPT_REQUIRED_EVIDENCE_HEADROOM_WORDS = 80
LEGACY_AUTHORIAL_PROMPT_BUDGET_CONTRACT_VERSION = "photo-authorial-prompt-budget/v1"
VISUAL_OBLIGATIONS_CONTRACT_VERSION = "photo-visual-obligations/v1"
VISUAL_INTENT_CONTRACT_VERSION = "photo-visual-intent/v1"
VISUAL_CONCEPTS_CONTRACT_VERSION = "photo-visual-concepts/v1"
MOE_RESPONSE_EVIDENCE_DIMENSIONS = {
    "actor_phrase": "subject",
    "aesthetic_baseline_phrase": "style",
    "affective_leak_phrase": "expression",
    "active_denial_phrase": "expression",
    "care_action_anchor_phrase": "relationship",
    "relationship_gaze_anchor_phrase": "relationship",
    "concealed_affection_phrase": "expression",
    "benevolent_affect_phrase": "expression",
    "baseline_phrase": "role",
    "event_phase_phrase": "event",
    "trigger_phrase": "event",
    "target_phrase": "event",
    "visible_response_phrase": "expression",
    "immediate_consequence_phrase": "event",
    "continuity_phrase": "event",
    "background_control_phrase": "setting",
    "focal_plane_phrase": "composition",
    "reference_identity_phrase": "identity",
}
MOE_RESPONSE_DEFAULT_RULE_DIMENSIONS = {
    "aesthetic_style_default": ("style",),
    "aesthetic_expression_default": ("expression",),
    "affective_balance_default": ("expression",),
    "generic_character_response_mechanism": (
        "event",
        "expression",
        "pose",
        "relationship",
    ),
    "generic_relationship_register": ("relationship", "expression"),
    "default_sensual_support": ("sexual_tone", "style", "composition"),
    "generic_expression_negative_suppression": ("expression",),
    "generic_style_negative_suppression": ("style",),
    "generic_appearance_negative_suppression": ("appearance",),
    "generic_text_negative_suppression": ("text",),
}
ADULT_APPEAL_DEFAULT_AFFECTED_DIMENSIONS = {
    "sexual_tone",
    "style",
    "composition",
    "expression",
    "pose",
    "body_geometry",
    "framing",
    "lighting",
}
MOE_WARM_AFFECT_GROUPS = (
    ("softened eye", "soft eyes", "eyes soften", "gentle eye", "warm eye"),
    (
        "lower lids soften",
        "softened lower lids",
        "lower eyelids soften",
        "softened lower eyelids",
    ),
    (
        "almost-smile",
        "almost smile",
        "near-smile",
        "near smile",
        "smile threatens",
        "smile starts",
    ),
    (
        "mouth corner lifts",
        "lifted mouth corner",
        "pleased mouth corner",
        "relieved mouth corner",
    ),
    ("mouth corner starts to lift", "mouth corner begins to lift"),
    ("fond", "fondness", "pleased", "relieved", "tender", "warmth"),
    (
        "playful embarrassment",
        "playfully embarrassed",
        "bashful delight",
        "private delight",
    ),
)
MOE_NEGATIVE_AFFECT_CUES = (
    "annoyed",
    "angry",
    "averted gaze",
    "bored",
    "cold stare",
    "frown",
    "irritated",
    "listless",
    "pout",
    "pursed",
    "sad",
    "scowl",
    "skeptical",
    "sullen",
)
MOE_WARM_EXPRESSION_DEFAULT_MARKERS = (
    "softened eye",
    "soft eyes",
    "eyes soften",
    "gentle eye",
    "warm eye",
    "lower lids soften",
    "softened lower lids",
    "lower eyelids soften",
    "softened lower eyelids",
    "almost-smile",
    "almost smile",
    "near-smile",
    "near smile",
    "smile threatens",
    "smile starts",
    "mouth corner lifts",
    "lifted mouth corner",
    "pleased mouth corner",
    "relieved mouth corner",
    "mouth corner starts to lift",
    "mouth corner begins to lift",
    "fondness",
    "playful embarrassment",
    "playfully embarrassed",
    "bashful delight",
    "private delight",
)
MOE_NEGATIVE_DEFAULT_TERMS_BY_RULE = {
    "generic_expression_negative_suppression": (
        "blank bored expression",
        "listless expression",
        "pure scowl without a warm micro-expression",
    ),
    "generic_style_negative_suppression": (
        "generic sparkle overlays",
        "decorative blush circles",
        "unrequested heart symbols",
        "heart-shaped pupils",
        "heart-shaped latte art",
        "cartoon motion lines",
        "manga reaction marks",
        "comic emphasis marks",
    ),
    "generic_appearance_negative_suppression": ("oversized anime eyes",),
    "generic_text_negative_suppression": (
        "readable background text",
        "pseudo-writing",
        "menu board lettering",
        "chalkboard writing",
        "signage behind the subject",
    ),
}
SEMANTIC_CLARIFICATION_CONTRACT_VERSION = "photo-semantic-clarification/v1"
CREATIVE_AUGMENTATION_CONTRACT_VERSION = "photo-creative-augmentation/v1"


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


def clean_prompt_spaces(text: str) -> str:
    value = re.sub(r"\s+", " ", str(text or "")).strip()
    return re.sub(r"\s+([,.!?;:])", r"\1", value)


def normalize_negative_intent_term(text: str) -> str:
    return clean_prompt_spaces(text).strip(" .;:!?\"'").casefold()


def strip_negative_directive_prefix(text: str) -> str:
    normalized = normalize_negative_intent_term(text)
    return re.sub(
        r"^(?:no|without|avoid|exclude|excluding|do\s+not|don't|never)\s+",
        "",
        normalized,
        count=1,
    ).strip()


def negative_term_matches_requester_exclusion(
    term: str,
    exclusions: Sequence[str],
) -> bool:
    term_key = strip_negative_directive_prefix(term)
    if not term_key:
        return False
    for exclusion in exclusions:
        exclusion_key = strip_negative_directive_prefix(str(exclusion))
        if exclusion_key and term_key == exclusion_key:
            return True
    return False


def authorial_negative_term_allowed(
    term: str,
    core: dict[str, Any],
    *,
    identity_preservation_enabled: bool,
) -> bool:
    key = normalize_negative_intent_term(term)
    if key in AUTHORIAL_INTENT_NEUTRAL_NEGATIVE_TERMS:
        return True
    if (
        identity_preservation_enabled
        and key in AUTHORIAL_IDENTITY_PRESERVATION_NEGATIVE_TERMS
    ):
        return True
    return negative_term_matches_requester_exclusion(
        key,
        [str(item) for item in core.get("user_exclusions") or []],
    )


def split_negative_prompt_terms(value: Any) -> list[str]:
    if value is None:
        return []
    return [
        clean_prompt_spaces(part)
        for part in str(value).split(",")
        if clean_prompt_spaces(part)
    ]


def find_blanket_negative_directives(text: str) -> list[str]:
    value = str(text or "")
    patterns = (
        re.compile(
            r"(?:^|[.;!?:—]\s+|,\s+)((?:no\b|do\s+not\b|don't\b|avoid\b|exclude\b)[^.;!?]*)",
            flags=re.IGNORECASE,
        ),
        re.compile(
            r"(?:^|[.;!?:—]\s+|,\s+)(never\s+(?:touch(?:es|ed|ing)?|inject(?:s|ed|ing)?|contact(?:s|ed|ing)?|show(?:s|ed|ing)?|depict(?:s|ed|ing)?|include(?:s|d|ing)?|use(?:s|d|ing)?|reveal(?:s|ed|ing)?|sexualiz(?:e|es|ed|ing)|crop(?:s|ped|ping)?|add(?:s|ed|ing)?)\b[^.;!?]*)",
            flags=re.IGNORECASE,
        ),
    )
    directives: list[str] = []
    seen: set[str] = set()
    for pattern in patterns:
        for match in pattern.finditer(value):
            directive = clean_prompt_spaces(match.group(1))
            key = directive.casefold()
            if directive and key not in seen:
                directives.append(directive)
                seen.add(key)
    return directives


def expected_negative_intent_guard(pack: dict[str, Any]) -> dict[str, Any] | None:
    core = pack.get("authorial_core") if isinstance(pack.get("authorial_core"), dict) else {}
    if core.get("contract_version") not in AUTHORIAL_CORE_MODERN_CONTRACT_VERSIONS:
        return None
    provenance = (
        pack.get("provenance")
        if isinstance(pack.get("provenance"), dict)
        else {}
    )
    identity_preservation_enabled = (
        str(provenance.get("reference_edit_mode") or "off") == "identity"
    )
    guard: dict[str, Any] = {
        "contract_version": NEGATIVE_INTENT_GUARD_CONTRACT_VERSION,
        "source_authorial_core_sha256": str(core.get("canonical_sha256") or ""),
        "source_intent_lock_sha256": str(
            ((core.get("intent_lock") or {}).get("canonical_sha256") or "")
        ),
        "positive_prompt_policy": "positive_description_only_no_blanket_negative_directives",
        "automatic_negative_policy": "intent_neutral_photographic_defects_only",
        "requester_exclusion_policy": "exact_active_request_scope_only",
        "platform_safety_policy": "enforce_outside_prompt_unless_requester_explicit",
        "local_boundary_policy": "positive_geometry_or_visible_state",
        "identity_preservation_enabled": identity_preservation_enabled,
        "explicit_user_exclusions": [
            str(item) for item in core.get("user_exclusions") or []
        ],
        "emitted_terms": split_negative_prompt_terms(pack.get("negative_en")),
    }
    guard["canonical_sha256"] = canonical_json_sha256(guard)
    guard["guard_id"] = str(guard["canonical_sha256"])[:16]
    return guard


def audit_negative_intent_guard(
    pack: dict[str, Any],
    prompt_en: str,
) -> list[dict[str, Any]]:
    expected = expected_negative_intent_guard(pack)
    if expected is None:
        return []
    failures: list[dict[str, Any]] = []
    actual = (
        pack.get("negative_intent_guard")
        if isinstance(pack.get("negative_intent_guard"), dict)
        else None
    )
    if actual != expected:
        failures.append(
            {
                "check": "negative_intent_guard_contract",
                "reason": (
                    "v5/v6 pack must expose the exact recomputable requester-first negative-intent boundary"
                ),
                "expected": expected,
                "actual": actual,
            }
        )

    core = pack.get("authorial_core") if isinstance(pack.get("authorial_core"), dict) else {}
    identity_enabled = bool(expected["identity_preservation_enabled"])
    terms = split_negative_prompt_terms(pack.get("negative_en"))
    disallowed_terms = [
        term
        for term in terms
        if not authorial_negative_term_allowed(
            term,
            core,
            identity_preservation_enabled=identity_enabled,
        )
    ]
    if disallowed_terms:
        failures.append(
            {
                "check": "negative_intent_guard_terms",
                "reason": (
                    "automatic negative_en contains semantic suppression that is neither a requester exclusion, an intent-neutral photographic defect, nor an enabled identity-preservation control"
                ),
                "terms": disallowed_terms,
            }
        )
    normalized_terms = [normalize_negative_intent_term(term) for term in terms]
    if len(normalized_terms) != len(set(normalized_terms)):
        failures.append(
            {
                "check": "negative_intent_guard_terms",
                "reason": "negative_en contains duplicate normalized terms",
            }
        )

    baseline_directives = find_blanket_negative_directives(
        str(core.get("baseline_prompt_en") or "")
    )
    if baseline_directives:
        failures.append(
            {
                "check": "negative_intent_guard_baseline",
                "reason": (
                    "baseline_prompt_en embeds blanket negative directives instead of positive visual realization"
                ),
                "directives": baseline_directives,
            }
        )
    prompt_directives = find_blanket_negative_directives(prompt_en)
    if prompt_directives:
        failures.append(
            {
                "check": "negative_intent_guard_prompt",
                "reason": (
                    "prompt_en embeds blanket negative directives; use positive local geometry or visible state and keep platform enforcement outside prompt prose"
                ),
                "directives": prompt_directives,
            }
        )
    return failures


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


def english_prompt_word_count(text: str) -> int:
    """Count image-prompt words consistently across the contract and audit."""
    return len(re.findall(r"[A-Za-z0-9]+(?:['’\-][A-Za-z0-9]+)*", str(text or "")))


def expected_authorial_prompt_budget_contract() -> dict[str, Any]:
    return {
        "contract_version": AUTHORIAL_PROMPT_BUDGET_CONTRACT_VERSION,
        "language": "en",
        "minimum_words": AUTHORIAL_PROMPT_MIN_WORDS,
        "recommended_maximum_words": AUTHORIAL_PROMPT_RECOMMENDED_MAX_WORDS,
        "absolute_maximum_words": AUTHORIAL_PROMPT_ABSOLUTE_MAX_WORDS,
        "required_evidence_headroom_words": AUTHORIAL_PROMPT_REQUIRED_EVIDENCE_HEADROOM_WORDS,
        "counting_rule": "ascii_words_with_internal_hyphens_or_apostrophes",
        "policy": {
            "recommended_maximum_is_warning": True,
            "absolute_bounds_are_blocking": True,
            "required_evidence_expands_advisory_ceiling": True,
            "requester_meaning_outranks_concision": True,
        },
    }


def legacy_authorial_prompt_budget_contract() -> dict[str, Any]:
    return {
        "contract_version": LEGACY_AUTHORIAL_PROMPT_BUDGET_CONTRACT_VERSION,
        "language": "en",
        "minimum_words": LEGACY_AUTHORIAL_PROMPT_MIN_WORDS,
        "recommended_maximum_words": LEGACY_AUTHORIAL_PROMPT_RECOMMENDED_MAX_WORDS,
        "absolute_maximum_words": LEGACY_AUTHORIAL_PROMPT_ABSOLUTE_MAX_WORDS,
        "required_evidence_headroom_words": LEGACY_AUTHORIAL_PROMPT_REQUIRED_EVIDENCE_HEADROOM_WORDS,
        "counting_rule": "ascii_words_with_internal_hyphens_or_apostrophes",
        "policy": {
            "recommended_maximum_is_warning": True,
            "absolute_bounds_are_blocking": True,
            "required_evidence_expands_advisory_ceiling": True,
            "requester_meaning_outranks_concision": True,
        },
    }


def nested_prompt_evidence_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        text = value.strip()
        return [text] if text else []
    if isinstance(value, dict):
        return [
            phrase
            for nested in value.values()
            for phrase in nested_prompt_evidence_strings(nested)
        ]
    if isinstance(value, list):
        return [
            phrase
            for nested in value
            for phrase in nested_prompt_evidence_strings(nested)
        ]
    return []


def authorial_required_prompt_evidence(
    pack: dict[str, Any],
    composed: dict[str, Any],
    *,
    baseline_only: bool = False,
) -> list[str]:
    """Collect literal hard-evidence phrases without treating optional ideas as duties."""

    phrases: list[str] = []
    core = pack.get("authorial_core") if isinstance(pack.get("authorial_core"), dict) else {}
    intent_lock = (
        core.get("intent_lock") if isinstance(core.get("intent_lock"), dict) else {}
    )
    phrases.extend(
        str(anchor.get("prompt_evidence") or "").strip()
        for anchor in intent_lock.get("semantic_anchors") or []
        if isinstance(anchor, dict) and str(anchor.get("prompt_evidence") or "").strip()
    )
    phrases.extend(
        str(definition.get("prompt_evidence") or "").strip()
        for definition in core.get("user_definitions") or []
        if isinstance(definition, dict)
        and str(definition.get("prompt_evidence") or "").strip()
    )
    for assertion in core.get("semantic_assertions") or []:
        if not isinstance(assertion, dict) or assertion.get("polarity") != "required":
            continue
        phrases.extend(nested_prompt_evidence_strings(assertion.get("evidence")))

    if not baseline_only:
        binding = (
            composed.get("authorial_core_binding")
            if isinstance(composed.get("authorial_core_binding"), dict)
            else {}
        )
        phrases.extend(nested_prompt_evidence_strings(binding.get("preserved_evidence")))
        for field, evidence_field in (
            ("character_response", "evidence"),
            ("semantic_assertion_evidence", "evidence"),
            ("moe_response", "prompt_evidence"),
            ("viewer_experience", "prompt_evidence"),
        ):
            payload = composed.get(field) if isinstance(composed.get(field), dict) else {}
            phrases.extend(nested_prompt_evidence_strings(payload.get(evidence_field)))
        phrases.extend(
            nested_prompt_evidence_strings(composed.get("visual_obligation_evidence"))
        )
        phrases.extend(nested_prompt_evidence_strings(composed.get("coverage_assertions")))
        manual_gate_evidence = (
            composed.get("manual_gate_evidence")
            if isinstance(composed.get("manual_gate_evidence"), dict)
            else {}
        )
        for evidence in manual_gate_evidence.values():
            if isinstance(evidence, dict):
                phrases.extend(
                    nested_prompt_evidence_strings(evidence.get("evidence_phrases"))
                )

    deduped: list[str] = []
    seen: set[str] = set()
    for phrase in phrases:
        key = phrase.casefold()
        if not phrase or key in seen:
            continue
        seen.add(key)
        deduped.append(phrase)
    return deduped


def authorial_prompt_budget_metrics(
    pack: dict[str, Any],
    composed: dict[str, Any],
    prompt_en: str,
    *,
    baseline_only: bool = False,
    budget_contract: dict[str, Any] | None = None,
) -> dict[str, int]:
    active_budget = budget_contract or expected_authorial_prompt_budget_contract()
    recommended_maximum_words = int(active_budget["recommended_maximum_words"])
    absolute_maximum_words = int(active_budget["absolute_maximum_words"])
    required_evidence_headroom_words = int(
        active_budget["required_evidence_headroom_words"]
    )
    word_matches = list(
        re.finditer(r"[A-Za-z0-9]+(?:['’\-][A-Za-z0-9]+)*", str(prompt_en or ""))
    )
    covered_word_indexes: set[int] = set()
    phrases = authorial_required_prompt_evidence(
        pack,
        composed,
        baseline_only=baseline_only,
    )
    for phrase in phrases:
        match = re.search(re.escape(phrase), prompt_en, flags=re.IGNORECASE)
        if match is None:
            continue
        covered_word_indexes.update(
            index
            for index, word in enumerate(word_matches)
            if word.start() >= match.start() and word.end() <= match.end()
        )
    actual_words = len(word_matches)
    required_evidence_words = len(covered_word_indexes)
    effective_recommended_maximum_words = min(
        absolute_maximum_words,
        max(
            recommended_maximum_words,
            required_evidence_words + required_evidence_headroom_words,
        ),
    )
    return {
        "actual_words": actual_words,
        "required_evidence_words": required_evidence_words,
        "optional_prose_words": actual_words - required_evidence_words,
        "effective_recommended_maximum_words": effective_recommended_maximum_words,
    }


AUTHORIAL_EVIDENCE_STOPWORDS = {
    "a",
    "an",
    "and",
    "as",
    "at",
    "by",
    "for",
    "from",
    "in",
    "into",
    "is",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
    "without",
}


def authorial_evidence_tokens(text: str) -> set[str]:
    return {
        token.lower()
        for token in re.findall(r"[A-Za-z0-9]+(?:[./'’\-][A-Za-z0-9]+)*", str(text or ""))
        if token.lower() not in AUTHORIAL_EVIDENCE_STOPWORDS
    }


def authorial_general_content_words(text: str) -> list[str]:
    return re.findall(
        r"[A-Za-z0-9][A-Za-z0-9_-]*|[가-힣]{2,}|[ぁ-んァ-ン一-龯]{2,}",
        str(text or ""),
    )


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
    integration = pack.get("photographic_integration")
    if isinstance(integration, dict):
        for candidate in integration.get("category_candidates") or []:
            if isinstance(candidate, dict) and candidate.get("id"):
                ids.add(str(candidate["id"]))
    craft = pack.get("photographic_craft")
    if isinstance(craft, dict):
        for candidate in craft.get("dimension_candidates") or []:
            if isinstance(candidate, dict) and candidate.get("id"):
                ids.add(str(candidate["id"]))
    for candidate in hybrid_augmentation_candidates_from_pack(pack):
        if candidate.get("id"):
            ids.add(str(candidate["id"]))
    for candidate in creative_augmentation_candidates_from_pack(pack):
        if candidate.get("id"):
            ids.add(str(candidate["id"]))
    for candidate in (pack.get("candidate_bundles") or {}).get("candidates") or []:
        if isinstance(candidate, dict) and candidate.get("id"):
            ids.add(str(candidate["id"]))
    return ids


def hybrid_augmentation_candidates_from_pack(pack: dict[str, Any]) -> list[dict[str, Any]]:
    hybrid = pack.get("hybrid_augmentation") if isinstance(pack.get("hybrid_augmentation"), dict) else {}
    adult = (
        pack.get("adult_appeal")
        if isinstance(pack.get("adult_appeal"), dict)
        else (
            hybrid.get("adult_appeal")
            if isinstance(hybrid.get("adult_appeal"), dict)
            else {}
        )
    )
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


def creative_augmentation_candidates_from_pack(
    pack: dict[str, Any],
) -> list[dict[str, Any]]:
    contract = (
        pack.get("creative_augmentation")
        if isinstance(pack.get("creative_augmentation"), dict)
        else {}
    )
    return [
        candidate
        for candidate in contract.get("candidates") or []
        if isinstance(candidate, dict)
    ]


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
    proposition = pack.get("visual_proposition")
    if isinstance(proposition, dict):
        for key in ("core_candidates", "tension_candidates"):
            for candidate in proposition.get(key) or []:
                if isinstance(candidate, dict) and candidate.get("id"):
                    candidates[str(candidate["id"])] = candidate
    integration = pack.get("photographic_integration")
    if isinstance(integration, dict):
        for candidate in integration.get("category_candidates") or []:
            if isinstance(candidate, dict) and candidate.get("id"):
                candidates[str(candidate["id"])] = candidate
    craft = pack.get("photographic_craft")
    if isinstance(craft, dict):
        for candidate in craft.get("dimension_candidates") or []:
            if isinstance(candidate, dict) and candidate.get("id"):
                candidates[str(candidate["id"])] = candidate
    for candidate in hybrid_augmentation_candidates_from_pack(pack):
        if candidate.get("id"):
            candidates[str(candidate["id"])] = candidate
    for candidate in creative_augmentation_candidates_from_pack(pack):
        if candidate.get("id"):
            candidates[str(candidate["id"])] = candidate
    for candidate in (pack.get("candidate_bundles") or {}).get("candidates") or []:
        if isinstance(candidate, dict) and candidate.get("id"):
            candidates[str(candidate["id"])] = candidate
    return candidates


def audit_v4_authorial_pack(pack: dict[str, Any]) -> list[dict[str, Any]]:
    if str(pack.get("contract_version") or "") not in {
        "photo-candidate-pack/v4",
        "photo-candidate-pack/v5",
        "photo-candidate-pack/v6",
    }:
        return []
    failures: list[dict[str, Any]] = []
    contract = (
        pack.get("authorial_composition")
        if isinstance(pack.get("authorial_composition"), dict)
        else {}
    )
    policy = contract.get("policy") if isinstance(contract.get("policy"), dict) else {}
    if (
        not contract.get("enabled")
        or contract.get("candidate_content_form") != "unordered_inspiration_terms"
        or contract.get("candidate_order") != "seed_shuffled_non_preferential"
        or policy.get("agent_is_final_author") is not True
        or policy.get("candidate_sentence_copying_forbidden") is not True
        or policy.get("all_advisory_candidates_may_be_rejected") is not True
        or policy.get("hard_identity_and_safety_constraints_remain_required") is not True
        or policy.get("chosen_candidate_interpretations_required") is not True
    ):
        failures.append(
            {
                "check": "authorial_pack_contract",
                "reason": "v4 pack is missing its fail-closed authorial composition policy",
            }
        )

    def contains_key(value: Any, key: str) -> bool:
        if isinstance(value, dict):
            return key in value or any(contains_key(item, key) for item in value.values())
        if isinstance(value, list):
            return any(contains_key(item, key) for item in value)
        return False

    if contains_key(pack, "covered_by"):
        failures.append(
            {
                "check": "authorial_coverage_answer_key",
                "reason": "v4 must not expose candidate IDs as precomputed intent-coverage answers",
            }
        )

    provenance = pack.get("provenance") if isinstance(pack.get("provenance"), dict) else {}
    private_provenance_keys = sorted(
        {
            "argv",
            "preset_id",
            "sample_prompt_id",
            "concept_gate_results",
            "concept_scene_variants",
            "character_response",
            "adult_appeal",
        }
        & set(provenance)
    )
    preset_reference = (
        pack.get("preset_reference")
        if isinstance(pack.get("preset_reference"), dict)
        else {}
    )
    motif_budget = pack.get("motif_budget") if isinstance(pack.get("motif_budget"), dict) else {}
    if (
        private_provenance_keys
        or "preset_id" in preset_reference
        or len(pack.get("presets") or []) == 1
        or "selected_motifs" in motif_budget
    ):
        failures.append(
            {
                "check": "authorial_private_routing",
                "reason": "v4 exposes a private sampled route, singleton preset, or sampled motif answer",
                "provenance_keys": private_provenance_keys,
            }
        )

    quality_profile = (
        pack.get("quality_profile")
        if isinstance(pack.get("quality_profile"), dict)
        else {}
    )
    integration = (
        pack.get("photographic_integration")
        if isinstance(pack.get("photographic_integration"), dict)
        else {}
    )
    craft = (
        pack.get("photographic_craft")
        if isinstance(pack.get("photographic_craft"), dict)
        else {}
    )
    proposition = (
        pack.get("visual_proposition")
        if isinstance(pack.get("visual_proposition"), dict)
        else {}
    )
    leaked_quality_keys = {
        "quality_profile": sorted(
            set(quality_profile) & {"source", "matched_facets", "matched_terms"}
        ),
        "photographic_integration": sorted(
            set(integration)
            & {
                "active_axes",
                "quality_profile",
                "matched_facets",
                "matched_terms",
                "principles",
                "required_categories",
                "suggested_concepts",
            }
        ),
        "photographic_craft": sorted(
            set(craft)
            & {
                "active_dimensions",
                "quality_profile",
                "matched_facets",
                "top_strategy",
                "strategy_variants",
                "prompt_dimension_ids",
            }
        ),
        "visual_proposition": sorted(
            set(proposition)
            & {
                "quality_profile",
                "subject_class",
                "subject_classes",
                "register",
                "principles",
            }
        ),
    }
    if quality_profile.get("profile_id") != "authorial" or any(leaked_quality_keys.values()):
        failures.append(
            {
                "check": "authorial_quality_routing",
                "reason": "v4 exposes a sampler-selected quality profile, axis, strategy, or proposition",
                "leaked_keys": leaked_quality_keys,
            }
        )

    scene_contract = pack.get("scene_contract") if isinstance(pack.get("scene_contract"), dict) else {}
    leaked_scene_groups = [
        str(group.get("group") or "unknown")
        for group in scene_contract.get("groups") or []
        if isinstance(group, dict)
        and (
            group.get("strategy") == "atomic_scene"
            or contains_key(group, "selected_entry_id")
            or contains_key(group, "candidate_entry_ids")
            or contains_key(group, "allowed_entry_ids")
            or (
                group.get("strategy") == "optional_inspiration_group"
                and group.get("sampler_selection_exposed") is not False
            )
        )
    ]
    if leaked_scene_groups:
        failures.append(
            {
                "check": "authorial_scene_selection",
                "reason": "v4 scene groups expose an internal selected entry or semantic answer key",
                "groups": leaked_scene_groups,
            }
        )

    candidate_surfaces = list(candidate_objects_from_pack(pack).values())
    proposition = pack.get("visual_proposition") if isinstance(pack.get("visual_proposition"), dict) else {}
    for key in ("core_candidates", "tension_candidates"):
        candidate_surfaces.extend(
            candidate
            for candidate in proposition.get(key) or []
            if isinstance(candidate, dict)
        )
    hybrid = pack.get("hybrid_augmentation") if isinstance(pack.get("hybrid_augmentation"), dict) else {}
    route_contract = hybrid.get("route_contract") if isinstance(hybrid.get("route_contract"), dict) else {}
    for route in route_contract.get("routes") or []:
        if isinstance(route, dict):
            candidate_surfaces.extend(
                detail
                for detail in route.get("details") or []
                if isinstance(detail, dict)
            )
    visual_concepts = (
        pack.get("visual_concept_candidates")
        if isinstance(pack.get("visual_concept_candidates"), dict)
        else {}
    )
    visual_candidates = [
        candidate
        for candidate in visual_concepts.get("candidates") or []
        if isinstance(candidate, dict)
    ]
    candidate_surfaces.extend(visual_candidates)
    if visual_concepts:
        candidate_ids = [str(candidate.get("id") or "") for candidate in visual_candidates]
        selection_policy = (
            visual_concepts.get("selection_policy")
            if isinstance(visual_concepts.get("selection_policy"), dict)
            else {}
        )
        concept_contract_invalid = (
            visual_concepts.get("enabled") is not True
            or visual_concepts.get("contract_version") != VISUAL_CONCEPTS_CONTRACT_VERSION
            or visual_concepts.get("candidate_order") != "seed_shuffled_non_preferential"
            or visual_concepts.get("selection_field") != "chosen_visual_concept_ids"
            or not candidate_ids
            or any(not candidate_id.startswith("visual-concept:") for candidate_id in candidate_ids)
            or len(candidate_ids) != len(set(candidate_ids))
            or any(
                selection_policy.get(key) is not True
                for key in (
                    "all_candidates_optional",
                    "selection_list_required_even_when_empty",
                    "unselected_candidates_add_no_prompt_or_review_duty",
                    "selected_candidates_promote_opt_in_contract_to_hard_obligation",
                    "matched_terms_scores_and_routing_reasons_not_exposed",
                )
            )
        )
        for candidate in visual_candidates:
            applicability = (
                candidate.get("applicability")
                if isinstance(candidate.get("applicability"), dict)
                else {}
            )
            opt_in = (
                candidate.get("opt_in_contract")
                if isinstance(candidate.get("opt_in_contract"), dict)
                else {}
            )
            obligation = (
                opt_in.get("obligation")
                if isinstance(opt_in.get("obligation"), dict)
                else {}
            )
            if (
                applicability.get("status") != "eligible"
                or opt_in.get("effect") != "promote_to_hard_visual_obligation"
                or opt_in.get("visual_obligations_contract_version")
                != VISUAL_OBLIGATIONS_CONTRACT_VERSION
                or not str(obligation.get("id") or "")
                or not obligation.get("render_gates")
            ):
                concept_contract_invalid = True
        if concept_contract_invalid:
            failures.append(
                {
                    "check": "visual_concept_candidate_contract",
                    "reason": (
                        "v4 visual concepts must be optional non-ranked candidates with a complete "
                        "pre-baked opt-in obligation"
                    ),
                }
            )
    copyable = [
        str(candidate.get("id") or candidate.get("candidate_id") or "unknown")
        for candidate in candidate_surfaces
        if any(key in candidate for key in ("label_en", "label_ko", "terms"))
        or candidate.get("content_form") != "unordered_inspiration_terms"
        or not isinstance(candidate.get("concept_terms"), list)
        or not candidate.get("concept_terms")
    ]
    if copyable:
        failures.append(
            {
                "check": "authorial_candidate_surface",
                "reason": "v4 candidate surfaces must expose only non-empty unordered concept terms",
                "candidate_ids": sorted(set(copyable)),
            }
        )

    slots = pack.get("slots") if isinstance(pack.get("slots"), dict) else {}
    ranked_slots = [
        str(slot)
        for slot, payload in slots.items()
        if isinstance(payload, dict)
        and (
            any(key in payload for key in ("selected", "weight_floor", "score_window", "selected_filter"))
            or payload.get("candidate_order") != "seed_shuffled_non_preferential"
        )
    ]
    if ranked_slots or any(
        any(key in candidate for key in ("selected_by_sampler", "probability", "weight", "score", "scores"))
        for candidate in candidate_surfaces
    ):
        failures.append(
            {
                "check": "authorial_candidate_ranking",
                "reason": "v4 must not expose sampler defaults, probabilities, weights, or ranking handles",
                "slots": sorted(ranked_slots),
            }
        )

    exploration = (
        pack.get("creative_exploration")
        if isinstance(pack.get("creative_exploration"), dict)
        else {}
    )
    leaked_replacements = [
        str(row.get("candidate_id") or "unknown")
        for row in exploration.get("contrast_candidates") or []
        if isinstance(row, dict)
        and ("replaces_candidate_id" in row or "relevance_rank" in row)
    ]
    if leaked_replacements:
        failures.append(
            {
                "check": "authorial_exploration_ranking",
                "reason": "v4 creative exploration must not expose a sampler replacement answer key",
                "candidate_ids": leaked_replacements,
            }
        )

    render_contract = pack.get("render_contract") if isinstance(pack.get("render_contract"), dict) else {}
    selected_scene = render_contract.get("selected_scene") if isinstance(render_contract.get("selected_scene"), dict) else {}
    scene_contract = pack.get("scene_contract") if isinstance(pack.get("scene_contract"), dict) else {}
    authorial_groups = [
        group
        for group in scene_contract.get("groups") or []
        if isinstance(group, dict) and group.get("strategy") == "authorial_scene"
    ]
    if authorial_groups and any(
        key in selected_scene for key in ("blueprint_id", "source_blueprint_hash", "atomic_scene")
    ):
        failures.append(
            {
                "check": "authorial_scene_privacy",
                "reason": "v4 authorial scene leaks a source handle or reusable atomic prose",
            }
        )
    if hybrid and hybrid.get("contract_version") != "photo-hybrid-augmentation/v2":
        failures.append(
            {
                "check": "authorial_hybrid_contract",
                "reason": "v4 hybrid augmentation must use the transform-only v2 contract",
            }
        )
    return failures


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
    for candidate in integration.get("category_candidates") or []:
        if not isinstance(candidate, dict) or str(candidate.get("category") or "") != category:
            continue
        terms.extend(
            str(term)
            for term in candidate.get("concept_terms") or []
            if str(term).strip()
        )
    return list(dict.fromkeys(terms))


def audit_photographic_integration(pack: dict[str, Any], search_text: str) -> dict[str, Any] | None:
    integration = pack.get("photographic_integration")
    if not isinstance(integration, dict) or not integration.get("enabled", True):
        return None

    authorial_candidates = [
        row
        for row in integration.get("category_candidates") or []
        if isinstance(row, dict) and str(row.get("category") or "").strip()
    ]
    required_categories = (
        [str(row.get("category")) for row in authorial_candidates]
        if authorial_candidates
        else [
            str(category)
            for category in integration.get("required_categories") or []
            if str(category).strip()
        ]
    )
    if not required_categories:
        required_categories = ["environment_binding", "optical_depth"]
    try:
        minimum_hits = int(
            integration.get(
                "minimum_selected_categories"
                if authorial_candidates
                else "minimum_category_hits",
                2,
            )
            or 2
        )
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
        for term in (candidate.get("concept_terms") or candidate.get("terms") or []):
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
    for candidate in craft.get("dimension_candidates") or []:
        if not isinstance(candidate, dict) or str(candidate.get("dimension") or "") != dimension_id:
            continue
        terms.extend(
            str(term)
            for term in candidate.get("concept_terms") or []
            if str(term).strip()
        )
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
        dimensions = [
            str(candidate.get("dimension"))
            for candidate in craft.get("dimension_candidates") or []
            if isinstance(candidate, dict) and str(candidate.get("dimension") or "").strip()
        ]
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


def derive_effective_visual_obligation_contract(
    pack: dict[str, Any],
    composed: dict[str, Any] | None,
) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    """Derive the only authoritative visual gate set from pack plus selection.

    Hard obligations are unconditional.  Optional visual concepts contribute
    nothing until their IDs occur in the composed selection list; a selected
    concept promotes its immutable opt-in obligation to the same hard contract.
    """

    failures: list[dict[str, Any]] = []
    hard_contract = (
        pack.get("visual_obligations")
        if isinstance(pack.get("visual_obligations"), dict)
        and pack.get("visual_obligations", {}).get("enabled") is True
        else None
    )
    candidate_contract = (
        pack.get("visual_concept_candidates")
        if isinstance(pack.get("visual_concept_candidates"), dict)
        and pack.get("visual_concept_candidates", {}).get("enabled") is True
        else None
    )
    composed_object = composed if isinstance(composed, dict) else {}
    raw_chosen = composed_object.get("chosen_visual_concept_ids")
    if candidate_contract is not None and "chosen_visual_concept_ids" not in composed_object:
        failures.append(
            {
                "check": "chosen_visual_concept_ids",
                "reason": (
                    "a pack with optional visual concepts requires an explicit selection list, "
                    "which may be empty"
                ),
            }
        )
    if raw_chosen is None:
        chosen_ids: list[str] = []
    elif not isinstance(raw_chosen, list) or any(
        not isinstance(value, str) or not value.strip() for value in raw_chosen
    ):
        failures.append(
            {
                "check": "chosen_visual_concept_ids",
                "reason": "chosen visual concept ids must be a list of non-empty strings",
            }
        )
        chosen_ids = []
    else:
        chosen_ids = [str(value).strip() for value in raw_chosen]
        if len(chosen_ids) != len(set(chosen_ids)):
            failures.append(
                {
                    "check": "chosen_visual_concept_ids",
                    "reason": "chosen visual concept ids must be distinct",
                }
            )
    if candidate_contract is None and chosen_ids:
        failures.append(
            {
                "check": "chosen_visual_concept_ids",
                "reason": "composed output selected visual concepts that the pack did not expose",
                "ids": chosen_ids,
            }
        )
    candidate_map = {
        str(candidate.get("id") or ""): candidate
        for candidate in (candidate_contract or {}).get("candidates") or []
        if isinstance(candidate, dict) and str(candidate.get("id") or "")
    }
    unknown_ids = sorted(set(chosen_ids) - set(candidate_map))
    if unknown_ids:
        failures.append(
            {
                "check": "chosen_visual_concept_ids",
                "reason": "unknown visual concept candidate id",
                "ids": unknown_ids,
            }
        )

    obligations = [
        copy.deepcopy(item)
        for item in (hard_contract or {}).get("obligations") or []
        if isinstance(item, dict) and str(item.get("id") or "")
    ]
    seen_profile_ids = {str(item.get("id") or "") for item in obligations}
    selected_candidate_ids: list[str] = []
    for candidate_id in chosen_ids:
        candidate = candidate_map.get(candidate_id)
        if not isinstance(candidate, dict):
            continue
        opt_in = (
            candidate.get("opt_in_contract")
            if isinstance(candidate.get("opt_in_contract"), dict)
            else {}
        )
        obligation = (
            opt_in.get("obligation")
            if isinstance(opt_in.get("obligation"), dict)
            else None
        )
        profile_id = str((obligation or {}).get("id") or "")
        if (
            opt_in.get("effect") != "promote_to_hard_visual_obligation"
            or opt_in.get("visual_obligations_contract_version")
            != VISUAL_OBLIGATIONS_CONTRACT_VERSION
            or not profile_id
        ):
            failures.append(
                {
                    "check": "visual_concept_opt_in_contract",
                    "reason": "selected visual concept has an invalid opt-in obligation",
                    "candidate_id": candidate_id,
                }
            )
            continue
        if profile_id in seen_profile_ids:
            failures.append(
                {
                    "check": "visual_concept_opt_in_contract",
                    "reason": "selected visual concept duplicates an already-effective profile",
                    "candidate_id": candidate_id,
                    "profile_id": profile_id,
                }
            )
            continue
        obligations.append(copy.deepcopy(obligation))
        seen_profile_ids.add(profile_id)
        selected_candidate_ids.append(candidate_id)
    if not obligations:
        return None, failures
    required_hard_gates = list(
        dict.fromkeys(
            str(gate.get("id") or "")
            for obligation in obligations
            for gate in obligation.get("render_gates") or []
            if isinstance(gate, dict) and str(gate.get("id") or "")
        )
    )
    effective: dict[str, Any] = {
        "enabled": True,
        "contract_version": VISUAL_OBLIGATIONS_CONTRACT_VERSION,
        "scope": "request_only",
        "strict_gate_set": True,
        "obligations": obligations,
        "required_hard_gates": required_hard_gates,
        "selected_visual_concept_ids": selected_candidate_ids,
    }
    if isinstance(hard_contract, dict):
        for key in ("precedence", "retry_policy", "source_visual_intent_sha256"):
            if key in hard_contract:
                effective[key] = copy.deepcopy(hard_contract[key])
    return effective, failures


def effective_visual_obligation_sha256(contract: dict[str, Any] | None) -> str | None:
    if not isinstance(contract, dict):
        return None
    canonical = json.dumps(
        contract,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def audit_visual_obligations(
    pack: dict[str, Any],
    composed: dict[str, Any],
    prompt_en: str,
) -> list[dict[str, Any]]:
    """Bind active request-scoped visual obligations to literal prompt evidence."""

    contract, selection_failures = derive_effective_visual_obligation_contract(
        pack,
        composed,
    )
    supplied_evidence = composed.get("visual_obligation_evidence")
    if not isinstance(contract, dict) or contract.get("enabled") is not True:
        if supplied_evidence not in (None, {}):
            selection_failures.append(
                {
                    "check": "visual_obligation_evidence",
                    "reason": "composed output supplies visual-obligation evidence but the pack activates no visual obligations",
                }
            )
        return selection_failures

    failures: list[dict[str, Any]] = list(selection_failures)
    if contract.get("contract_version") != VISUAL_OBLIGATIONS_CONTRACT_VERSION:
        failures.append(
            {
                "check": "visual_obligations_contract",
                "reason": "unsupported visual-obligations contract_version",
                "expected": VISUAL_OBLIGATIONS_CONTRACT_VERSION,
                "actual": contract.get("contract_version"),
            }
        )
    visual_intent = pack.get("visual_intent")
    source_visual_intent_sha256 = str(
        contract.get("source_visual_intent_sha256") or ""
    )
    if visual_intent is not None or source_visual_intent_sha256:
        if not isinstance(visual_intent, dict):
            failures.append(
                {
                    "check": "visual_intent_integrity",
                    "reason": "hash-bound visual obligations require the canonical visual_intent object",
                }
            )
        else:
            allowed_visual_intent_fields = {
                "contract_version",
                "provenance",
                "obligations",
                "canonical_sha256",
                "request_id",
            }
            unknown_visual_intent_fields = sorted(
                set(visual_intent) - allowed_visual_intent_fields
            )
            canonical_visual_intent = {
                "contract_version": visual_intent.get("contract_version"),
                "provenance": visual_intent.get("provenance"),
                "obligations": visual_intent.get("obligations"),
            }
            actual_visual_intent_sha256 = hashlib.sha256(
                json.dumps(
                    canonical_visual_intent,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode("utf-8")
            ).hexdigest()
            if (
                unknown_visual_intent_fields
                or visual_intent.get("contract_version")
                != VISUAL_INTENT_CONTRACT_VERSION
                or visual_intent.get("provenance") != "agent_prepack"
                or str(visual_intent.get("canonical_sha256") or "")
                != actual_visual_intent_sha256
                or str(visual_intent.get("request_id") or "")
                != actual_visual_intent_sha256[:16]
                or source_visual_intent_sha256 != actual_visual_intent_sha256
            ):
                failures.append(
                    {
                        "check": "visual_intent_integrity",
                        "reason": "visual_intent canonical bytes or source hash changed after pre-pack freezing",
                        "unknown_fields": unknown_visual_intent_fields,
                        "expected_sha256": actual_visual_intent_sha256,
                        "actual_sha256": visual_intent.get("canonical_sha256"),
                        "contract_sha256": source_visual_intent_sha256 or None,
                    }
                )
    obligations = [
        item
        for item in contract.get("obligations") or []
        if isinstance(item, dict) and str(item.get("id") or "").strip()
    ]
    expected_ids = {str(item["id"]) for item in obligations}
    if isinstance(visual_intent, dict):
        explicit_ids = {
            str(item.get("profile_id") or "")
            for item in visual_intent.get("obligations") or []
            if isinstance(item, dict) and str(item.get("profile_id") or "")
        }
        missing_explicit_profiles = sorted(explicit_ids - expected_ids)
        if missing_explicit_profiles:
            failures.append(
                {
                    "check": "visual_intent_binding",
                    "reason": "a pre-pack visual-intent profile is missing from active visual obligations",
                    "missing": missing_explicit_profiles,
                }
            )
    if not obligations:
        failures.append(
            {
                "check": "visual_obligations_contract",
                "reason": "enabled visual-obligations contract contains no obligations",
            }
        )
    if not isinstance(supplied_evidence, dict):
        failures.append(
            {
                "check": "visual_obligation_evidence",
                "reason": "active visual obligations require a visual_obligation_evidence object",
            }
        )
        supplied_evidence = {}
    actual_ids = {str(key) for key in supplied_evidence}
    missing_ids = sorted(expected_ids - actual_ids)
    extra_ids = sorted(actual_ids - expected_ids)
    if missing_ids or extra_ids:
        failures.append(
            {
                "check": "visual_obligation_evidence",
                "reason": "visual obligation evidence profile ids must exactly match the active pack profiles",
                "missing": missing_ids,
                "extra": extra_ids,
            }
        )

    declared_gate_ids: list[str] = []
    for obligation in obligations:
        profile_id = str(obligation["id"])
        binding = (
            obligation.get("prompt_binding")
            if isinstance(obligation.get("prompt_binding"), dict)
            else {}
        )
        required_fields = [
            str(field)
            for field in binding.get("required_evidence_fields") or []
            if str(field).strip()
        ]
        evidence_requirements = (
            obligation.get("evidence_requirements")
            if isinstance(obligation.get("evidence_requirements"), dict)
            else {}
        )
        runtime_expression = (
            obligation.get("runtime_expression")
            if isinstance(obligation.get("runtime_expression"), dict)
            else {}
        )
        expression_mode = str(runtime_expression.get("default_mode") or "")
        label_terms = nonempty_string_list(runtime_expression.get("prompt_label_terms"))
        forbidden_prompt_terms = nonempty_string_list(
            runtime_expression.get("forbidden_prompt_terms")
        )
        if expression_mode == "label_plus_definition" and not any(
            text_contains_term(prompt_en, term) for term in label_terms
        ):
            failures.append(
                {
                    "check": "visual_obligation_runtime_expression",
                    "reason": "runtime expression policy requires a safe label plus component definition",
                    "profile_id": profile_id,
                    "accepted_labels": label_terms,
                }
            )
        forbidden_runtime_hits = [
            term for term in forbidden_prompt_terms if text_contains_term(prompt_en, term)
        ]
        if forbidden_runtime_hits:
            failures.append(
                {
                    "check": "visual_obligation_runtime_expression",
                    "reason": "runtime prompt contains a label forbidden by the profile expression policy",
                    "profile_id": profile_id,
                    "terms": forbidden_runtime_hits,
                }
            )
        profile_evidence = supplied_evidence.get(profile_id)
        if not isinstance(profile_evidence, dict):
            continue
        actual_fields = {str(key) for key in profile_evidence}
        expected_fields = set(required_fields)
        missing_fields = sorted(expected_fields - actual_fields)
        extra_fields = sorted(actual_fields - expected_fields)
        if missing_fields or extra_fields:
            failures.append(
                {
                    "check": "visual_obligation_evidence",
                    "reason": "profile evidence fields must exactly match its prompt-binding contract",
                    "profile_id": profile_id,
                    "missing": missing_fields,
                    "extra": extra_fields,
                }
            )
        literal_phrases: list[str] = []
        for field in required_fields:
            phrase = profile_evidence.get(field)
            if not isinstance(phrase, str) or not phrase.strip():
                failures.append(
                    {
                        "check": "visual_obligation_evidence",
                        "reason": "required visual evidence must be a non-empty string",
                        "profile_id": profile_id,
                        "field": field,
                    }
                )
                continue
            phrase = phrase.strip()
            literal_phrases.append(phrase)
            if not text_contains_term(prompt_en, phrase):
                failures.append(
                    {
                        "check": "visual_obligation_prompt_binding",
                        "reason": "visual evidence phrase is not literal in prompt_en",
                        "profile_id": profile_id,
                        "field": field,
                        "phrase": phrase,
                    }
                )
            requirement = (
                evidence_requirements.get(field)
                if isinstance(evidence_requirements.get(field), dict)
                else {}
            )
            try:
                minimum_content_words = int(requirement.get("min_content_words", 3))
            except (TypeError, ValueError):
                minimum_content_words = 3
            content_words = authorial_evidence_tokens(phrase)
            if len(content_words) < minimum_content_words:
                failures.append(
                    {
                        "check": "visual_obligation_semantic_evidence",
                        "reason": "visual evidence phrase is too generic to prove its field",
                        "profile_id": profile_id,
                        "field": field,
                        "minimum_content_words": minimum_content_words,
                        "actual_content_words": len(content_words),
                    }
                )
            required_anchors = nonempty_string_list(requirement.get("must_mention_any"))
            if required_anchors and not any(
                text_contains_term(phrase, anchor) for anchor in required_anchors
            ):
                failures.append(
                    {
                        "check": "visual_obligation_semantic_evidence",
                        "reason": "visual evidence phrase lacks a profile-declared component anchor",
                        "profile_id": profile_id,
                        "field": field,
                        "accepted_anchors": required_anchors,
                    }
                )
            forbidden_field_hits = [
                term
                for term in nonempty_string_list(requirement.get("must_not_contain"))
                if text_contains_term(phrase, term)
            ]
            if forbidden_field_hits:
                failures.append(
                    {
                        "check": "visual_obligation_semantic_evidence",
                        "reason": "visual evidence phrase contains a profile-declared contradiction",
                        "profile_id": profile_id,
                        "field": field,
                        "terms": forbidden_field_hits,
                    }
                )
            filler_hits = [
                term
                for term in nonempty_string_list(binding.get("forbidden_filler_phrases"))
                if text_contains_term(phrase, term)
            ]
            if filler_hits:
                failures.append(
                    {
                        "check": "visual_obligation_semantic_evidence",
                        "reason": "field-name or checklist filler is not visual proof",
                        "profile_id": profile_id,
                        "field": field,
                        "terms": filler_hits,
                    }
                )
        try:
            minimum_distinct = int(
                binding.get("minimum_distinct_evidence_phrases", len(required_fields))
            )
        except (TypeError, ValueError):
            minimum_distinct = len(required_fields)
        if normalized_unique_count(literal_phrases) < minimum_distinct:
            failures.append(
                {
                    "check": "visual_obligation_distinct_evidence",
                    "reason": "different visual duties require distinct literal prompt phrases",
                    "profile_id": profile_id,
                    "minimum": minimum_distinct,
                    "actual": normalized_unique_count(literal_phrases),
                }
            )
        try:
            overlap_limit = float(
                binding.get("maximum_pairwise_content_token_overlap_ratio", 0.82)
            )
        except (TypeError, ValueError):
            overlap_limit = 0.82
        phrase_token_sets = [authorial_evidence_tokens(phrase) for phrase in literal_phrases]
        excessive_overlap_pairs: list[list[int]] = []
        for left_index, left_tokens in enumerate(phrase_token_sets):
            for right_index in range(left_index + 1, len(phrase_token_sets)):
                right_tokens = phrase_token_sets[right_index]
                union = left_tokens | right_tokens
                overlap = len(left_tokens & right_tokens) / len(union) if union else 1.0
                if overlap > overlap_limit:
                    excessive_overlap_pairs.append([left_index, right_index])
        if excessive_overlap_pairs:
            failures.append(
                {
                    "check": "visual_obligation_distinct_evidence",
                    "reason": "visual duties reuse too much of the same content-token evidence",
                    "profile_id": profile_id,
                    "maximum_overlap_ratio": overlap_limit,
                    "pairs": excessive_overlap_pairs,
                }
            )
        hard_bindings = (
            obligation.get("bindings")
            if isinstance(obligation.get("bindings"), dict)
            else {}
        )
        for field, expected_phrase in hard_bindings.items():
            actual_phrase = str(profile_evidence.get(str(field)) or "").strip()
            expected_phrase = str(expected_phrase or "").strip()
            if actual_phrase != expected_phrase:
                failures.append(
                    {
                        "check": "visual_obligation_hard_binding",
                        "reason": "request-scoped pre-pack binding changed during composition",
                        "profile_id": profile_id,
                        "field": field,
                        "expected": expected_phrase,
                        "actual": actual_phrase or None,
                    }
                )
            elif not text_contains_term(prompt_en, expected_phrase):
                failures.append(
                    {
                        "check": "visual_obligation_hard_binding",
                        "reason": "request-scoped pre-pack binding is not literal in prompt_en",
                        "profile_id": profile_id,
                        "field": field,
                        "phrase": expected_phrase,
                    }
                )
        declared_gate_ids.extend(
            str(gate.get("id") or "")
            for gate in obligation.get("render_gates") or []
            if isinstance(gate, dict) and str(gate.get("id") or "").strip()
        )

    required_gate_ids = [
        str(gate)
        for gate in contract.get("required_hard_gates") or []
        if str(gate).strip()
    ]
    if list(dict.fromkeys(declared_gate_ids)) != required_gate_ids:
        failures.append(
            {
                "check": "visual_obligations_contract",
                "reason": "required_hard_gates must exactly equal the ordered union of obligation render gates",
            }
        )
    return failures


def expected_moe_intent_precedence(
    pack: dict[str, Any],
    contract: dict[str, Any],
) -> dict[str, Any] | None:
    core = pack.get("authorial_core") if isinstance(pack.get("authorial_core"), dict) else {}
    if core.get("contract_version") != AUTHORIAL_CORE_CONTRACT_VERSION:
        return None
    intent_lock = core.get("intent_lock") if isinstance(core.get("intent_lock"), dict) else {}
    locked_dimensions = [
        str(item)
        for item in intent_lock.get("locked_dimensions") or []
        if str(item) in INTENT_LOCK_DIMENSIONS
    ]
    open_dimensions = [
        str(item)
        for item in intent_lock.get("open_dimensions") or []
        if str(item) in INTENT_LOCK_DIMENSIONS
    ]
    open_set = set(open_dimensions)
    applicability = {
        "aesthetic_style_default": True,
        "aesthetic_expression_default": True,
        "affective_balance_default": True,
        "generic_character_response_mechanism": (
            str(contract.get("primary_mechanism") or "")
            == "character_specific_reveal"
        ),
        "generic_relationship_register": (
            str(contract.get("relationship_register") or "")
            == "character_specific_reveal"
        ),
        "default_sensual_support": contract.get("defaulted_sensual_optional") is True,
        "generic_expression_negative_suppression": True,
        "generic_style_negative_suppression": True,
        "generic_appearance_negative_suppression": True,
        "generic_text_negative_suppression": True,
    }
    rules: list[dict[str, Any]] = []
    for rule_id, affected in MOE_RESPONSE_DEFAULT_RULE_DIMENSIONS.items():
        affected_dimensions = list(affected)
        if not applicability.get(rule_id, False):
            status = "not_applicable"
            blocked_dimensions: list[str] = []
        else:
            blocked_dimensions = sorted(set(affected_dimensions) - open_set)
            status = (
                "active"
                if not blocked_dimensions
                else "suppressed_requesting_user_priority"
            )
        rules.append(
            {
                "rule_id": rule_id,
                "affected_dimensions": affected_dimensions,
                "status": status,
                "blocked_dimensions": blocked_dimensions,
            }
        )
    return {
        "contract_version": DOWNSTREAM_INTENT_PRECEDENCE_CONTRACT_VERSION,
        "priority": "requesting_user",
        "source_intent_lock_sha256": str(intent_lock.get("canonical_sha256") or ""),
        "locked_dimensions": locked_dimensions,
        "open_dimensions": open_dimensions,
        "closed_dimensions": sorted(INTENT_LOCK_DIMENSIONS - open_set),
        "default_rule_policy": "active_only_when_all_affected_dimensions_are_explicitly_open",
        "non_open_evidence_policy": (
            "reuse_matching_locked_anchor_or_frozen_baseline_only"
        ),
        "evidence_field_dimensions": copy.deepcopy(
            MOE_RESPONSE_EVIDENCE_DIMENSIONS
        ),
        "rules": rules,
    }


def moe_intent_rule_status(precedence: Any, rule_id: str) -> str:
    if not isinstance(precedence, dict):
        return "legacy_unscoped"
    for row in precedence.get("rules") or []:
        if isinstance(row, dict) and row.get("rule_id") == rule_id:
            return str(row.get("status") or "")
    return "missing"


def audit_moe_intent_precedence(
    pack: dict[str, Any],
    contract: dict[str, Any],
    response: dict[str, Any],
    prompt_en: str,
) -> list[dict[str, Any]]:
    expected = expected_moe_intent_precedence(pack, contract)
    actual = contract.get("intent_precedence")
    if expected is None:
        return []
    failures: list[dict[str, Any]] = []
    if actual != expected:
        return [
            {
                "check": "moe_response_intent_precedence",
                "reason": (
                    "v2 downstream-default precedence must be an exact recomputable projection of the requesting-user intent lock"
                ),
                "expected": expected,
                "actual": actual,
            }
        ]

    composition_guidance = (
        contract.get("composition_guidance")
        if isinstance(contract.get("composition_guidance"), dict)
        else {}
    )
    binding = (
        contract.get("prompt_binding")
        if isinstance(contract.get("prompt_binding"), dict)
        else {}
    )
    required_evidence_fields = {
        str(item) for item in binding.get("required_evidence_fields") or []
    }
    affective_active = (
        moe_intent_rule_status(actual, "affective_balance_default") == "active"
    )
    aesthetic_active = (
        moe_intent_rule_status(actual, "aesthetic_style_default") == "active"
    )
    generic_mechanism_suppressed = (
        moe_intent_rule_status(actual, "generic_character_response_mechanism")
        == "suppressed_requesting_user_priority"
    )
    text_default_active = (
        moe_intent_rule_status(actual, "generic_text_negative_suppression")
        == "active"
    )
    affective_guidance = (
        composition_guidance.get("affective_balance")
        if isinstance(composition_guidance.get("affective_balance"), dict)
        else {}
    )
    aesthetic_guidance = (
        composition_guidance.get("aesthetic_entry_condition")
        if isinstance(composition_guidance.get("aesthetic_entry_condition"), dict)
        else {}
    )
    structural_mismatches: list[str] = []
    if affective_guidance.get("required") is not affective_active:
        structural_mismatches.append("affective_balance.required")
    if affective_guidance.get("status") != (
        "active" if affective_active else "suppressed_requesting_user_priority"
    ):
        structural_mismatches.append("affective_balance.status")
    if ("affective_leak_phrase" in required_evidence_fields) is not affective_active:
        structural_mismatches.append("affective_leak_phrase")
    if aesthetic_guidance.get("required") is not aesthetic_active:
        structural_mismatches.append("aesthetic_entry_condition.required")
    if aesthetic_guidance.get("status") != (
        "active" if aesthetic_active else "suppressed_requesting_user_priority"
    ):
        structural_mismatches.append("aesthetic_entry_condition.status")
    if ("aesthetic_baseline_phrase" in required_evidence_fields) is not aesthetic_active:
        structural_mismatches.append("aesthetic_baseline_phrase")
    causal_evidence_fields = {
        "baseline_phrase",
        "event_phase_phrase",
        "trigger_phrase",
        "target_phrase",
        "immediate_consequence_phrase",
        "continuity_phrase",
    }
    if generic_mechanism_suppressed and (
        causal_evidence_fields & required_evidence_fields
    ):
        structural_mismatches.append("generic_causal_evidence_fields")
    background_expected = (
        contract.get("explicit_text_requested") is not True and text_default_active
    )
    if ("background_control_phrase" in required_evidence_fields) is not background_expected:
        structural_mismatches.append("background_control_phrase")
    if structural_mismatches:
        failures.append(
            {
                "check": "moe_response_intent_precedence",
                "reason": (
                    "moe-response composition duties do not reflect the recomputed requester-first rule states"
                ),
                "fields": structural_mismatches,
            }
        )

    evidence = response.get("prompt_evidence")
    evidence = evidence if isinstance(evidence, dict) else {}
    core = pack["authorial_core"]
    baseline_prompt = str(core.get("baseline_prompt_en") or "")
    intent_lock = core.get("intent_lock") if isinstance(core.get("intent_lock"), dict) else {}
    locked_dimensions = set(intent_lock.get("locked_dimensions") or [])
    open_dimensions = set(intent_lock.get("open_dimensions") or [])
    anchors_by_dimension: dict[str, set[str]] = {}
    for anchor in intent_lock.get("semantic_anchors") or []:
        if not isinstance(anchor, dict):
            continue
        dimension = str(anchor.get("dimension") or "")
        phrase = str(anchor.get("prompt_evidence") or "")
        if dimension and phrase:
            anchors_by_dimension.setdefault(dimension, set()).add(phrase)

    for field, raw_phrase in evidence.items():
        dimension = MOE_RESPONSE_EVIDENCE_DIMENSIONS.get(str(field))
        phrase = str(raw_phrase or "").strip()
        if not dimension or not phrase or dimension in open_dimensions:
            continue
        if dimension in locked_dimensions:
            allowed = anchors_by_dimension.get(dimension, set())
            valid = phrase in allowed
            required_source = "matching_locked_semantic_anchor"
        else:
            allowed = set()
            valid = text_contains_term(baseline_prompt, phrase)
            required_source = "frozen_baseline_prompt"
        if not valid:
            failures.append(
                {
                    "check": "moe_response_intent_precedence",
                    "reason": (
                        "moe-response evidence on a non-open dimension introduced semantics outside the requester-first frozen boundary"
                    ),
                    "field": field,
                    "dimension": dimension,
                    "required_source": required_source,
                    "allowed_locked_anchor_evidence": sorted(allowed),
                    "actual": phrase,
                }
            )

    negative_en = str(pack.get("negative_en") or "").lower()
    for rule_id, terms in MOE_NEGATIVE_DEFAULT_TERMS_BY_RULE.items():
        if moe_intent_rule_status(actual, rule_id) != "suppressed_requesting_user_priority":
            continue
        leaked_terms = [term for term in terms if term.lower() in negative_en]
        if leaked_terms:
            failures.append(
                {
                    "check": "moe_response_intent_precedence",
                    "reason": (
                        "negative prompt retained a generic downstream default for a non-open semantic dimension"
                    ),
                    "rule_id": rule_id,
                    "terms": leaked_terms,
                }
            )

    if (
        moe_intent_rule_status(actual, "affective_balance_default")
        == "suppressed_requesting_user_priority"
    ):
        baseline_lower = baseline_prompt.lower()
        prompt_lower = prompt_en.lower()
        baseline_has_warm_default = any(
            cue in baseline_lower for cue in MOE_WARM_EXPRESSION_DEFAULT_MARKERS
        )
        prompt_warm_hits = sorted(
            {
                cue
                for cue in MOE_WARM_EXPRESSION_DEFAULT_MARKERS
                if cue in prompt_lower
            }
        )
        if prompt_warm_hits and not baseline_has_warm_default:
            failures.append(
                {
                    "check": "moe_response_intent_precedence",
                    "reason": (
                        "a suppressed warm-affect default leaked into a closed expression dimension without frozen requester evidence"
                    ),
                    "rule_id": "affective_balance_default",
                    "terms": prompt_warm_hits,
                }
            )

    return failures


def audit_moe_response(
    pack: dict[str, Any],
    composed: dict[str, Any],
    prompt_en: str,
    warnings: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    contract = pack.get("moe_response")
    if not isinstance(contract, dict) or not contract.get("enabled"):
        return []

    response = composed.get("moe_response")
    if not isinstance(response, dict):
        return [
            {
                "check": "moe_response",
                "reason": "enabled moe-response pack requires a moe_response object",
            }
        ]

    failures: list[dict[str, Any]] = []
    failures.extend(
        audit_moe_intent_precedence(
            pack,
            contract,
            response,
            prompt_en,
        )
    )
    composition_guidance = (
        contract.get("composition_guidance")
        if isinstance(contract.get("composition_guidance"), dict)
        else {}
    )
    prompt_budget = (
        composition_guidance.get("prompt_budget")
        if isinstance(composition_guidance.get("prompt_budget"), dict)
        else {}
    )
    if prompt_budget:
        prompt_word_count = english_prompt_word_count(prompt_en)
        advisory_budget = all(
            field in prompt_budget
            for field in (
                "recommended_minimum_words",
                "recommended_maximum_words",
                "absolute_maximum_words",
            )
        )
        if advisory_budget:
            try:
                minimum_prompt_words = int(
                    prompt_budget.get("minimum_words", AUTHORIAL_PROMPT_MIN_WORDS)
                )
                recommended_minimum_words = int(
                    prompt_budget.get(
                        "recommended_minimum_words",
                        MOE_PROMPT_DEFAULT_RECOMMENDED_MIN_WORDS,
                    )
                )
                recommended_maximum_words = int(
                    prompt_budget.get(
                        "recommended_maximum_words",
                        MOE_PROMPT_DEFAULT_RECOMMENDED_MAX_WORDS,
                    )
                )
                absolute_maximum_words = int(
                    prompt_budget.get(
                        "absolute_maximum_words",
                        AUTHORIAL_PROMPT_ABSOLUTE_MAX_WORDS,
                    )
                )
            except (TypeError, ValueError):
                minimum_prompt_words = AUTHORIAL_PROMPT_MIN_WORDS
                recommended_minimum_words = MOE_PROMPT_DEFAULT_RECOMMENDED_MIN_WORDS
                recommended_maximum_words = MOE_PROMPT_DEFAULT_RECOMMENDED_MAX_WORDS
                absolute_maximum_words = AUTHORIAL_PROMPT_ABSOLUTE_MAX_WORDS
            if not minimum_prompt_words <= prompt_word_count <= absolute_maximum_words:
                failures.append(
                    {
                        "check": "moe_response_prompt_budget",
                        "reason": "moe prompt_en exceeds the absolute compatibility bounds",
                        "minimum_words": minimum_prompt_words,
                        "absolute_maximum_words": absolute_maximum_words,
                        "actual_words": prompt_word_count,
                    }
                )
            elif warnings is not None and not (
                recommended_minimum_words
                <= prompt_word_count
                <= recommended_maximum_words
            ):
                warnings.append(
                    {
                        "check": "moe_response_prompt_budget",
                        "reason": (
                            "moe prompt_en is outside the advisory compact range; preserve required "
                            "meaning before shortening optional prose"
                        ),
                        "recommended_minimum_words": recommended_minimum_words,
                        "recommended_maximum_words": recommended_maximum_words,
                        "absolute_maximum_words": absolute_maximum_words,
                        "actual_words": prompt_word_count,
                    }
                )
        else:
            try:
                minimum_prompt_words = int(
                    prompt_budget.get(
                        "minimum_words", MOE_PROMPT_DEFAULT_RECOMMENDED_MIN_WORDS
                    )
                )
            except (TypeError, ValueError):
                minimum_prompt_words = MOE_PROMPT_DEFAULT_RECOMMENDED_MIN_WORDS
            try:
                maximum_prompt_words = int(
                    prompt_budget.get(
                        "maximum_words", MOE_PROMPT_DEFAULT_RECOMMENDED_MAX_WORDS
                    )
                )
            except (TypeError, ValueError):
                maximum_prompt_words = MOE_PROMPT_DEFAULT_RECOMMENDED_MAX_WORDS
            if not minimum_prompt_words <= prompt_word_count <= maximum_prompt_words:
                failures.append(
                    {
                        "check": "moe_response_prompt_budget",
                        "reason": (
                            "legacy moe prompt_en must stay within its recorded compact word budget"
                        ),
                        "minimum_words": minimum_prompt_words,
                        "maximum_words": maximum_prompt_words,
                        "actual_words": prompt_word_count,
                    }
                )
    required_fields = [str(item) for item in contract.get("required_fields") or [] if str(item)]
    missing_fields = [field for field in required_fields if field not in response]
    if missing_fields:
        failures.append(
            {
                "check": "moe_response",
                "reason": "moe response is missing required fields",
                "fields": missing_fields,
            }
        )

    scalar_fields = tuple(
        field
        for field in (
            "aesthetic_baseline",
            "mechanism",
            "relationship_register",
            "baseline",
            "event_phase",
            "trigger",
            "target",
            "visible_response",
            "immediate_consequence",
            "continuity",
        )
        if field in required_fields
    )
    invalid_scalars = [
        field
        for field in scalar_fields
        if not isinstance(response.get(field), str) or not str(response.get(field)).strip()
    ]
    if invalid_scalars:
        failures.append(
            {
                "check": "moe_response_causal_chain",
                "reason": "moe response requires one concrete scalar value for every causal field",
                "fields": invalid_scalars,
            }
        )

    aesthetic_baseline = str(response.get("aesthetic_baseline") or "")
    required_aesthetic = str(contract.get("aesthetic_baseline") or "")
    if aesthetic_baseline and required_aesthetic and aesthetic_baseline != required_aesthetic:
        failures.append(
            {
                "check": "moe_response_aesthetic_baseline",
                "reason": "composed response changed the routed adult character aesthetic baseline",
                "expected": required_aesthetic,
                "actual": aesthetic_baseline,
            }
        )

    mechanism = str(response.get("mechanism") or "")
    required_mechanism = str(contract.get("primary_mechanism") or "")
    if mechanism and required_mechanism and mechanism != required_mechanism:
        failures.append(
            {
                "check": "moe_response_mechanism",
                "reason": "composed response changed the routed primary mechanism",
                "expected": required_mechanism,
                "actual": mechanism,
            }
        )

    relationship_register = str(response.get("relationship_register") or "")
    required_relationship_register = str(contract.get("relationship_register") or "")
    if (
        relationship_register
        and required_relationship_register
        and relationship_register != required_relationship_register
    ):
        failures.append(
            {
                "check": "moe_response_relationship_register",
                "reason": "composed response changed the routed relationship register",
                "expected": required_relationship_register,
                "actual": relationship_register,
            }
        )

    support = response.get("support_mechanisms")
    if not isinstance(support, list) or any(not isinstance(item, str) for item in support):
        failures.append(
            {
                "check": "moe_response_support",
                "reason": "support_mechanisms must be a list of strings",
            }
        )
        support_values: list[str] = []
    else:
        support_values = [str(item) for item in support if str(item).strip()]
    allowed_support = {str(item) for item in contract.get("support_mechanisms") or []}
    unknown_support = sorted(set(support_values) - allowed_support)
    if unknown_support or len(set(support_values)) > 2 or mechanism in support_values:
        failures.append(
            {
                "check": "moe_response_support",
                "reason": "use only the routed support mechanisms, at most two, without repeating the primary",
                "unknown": unknown_support,
            }
        )

    causal_fields = (
        "baseline",
        "trigger",
        "target",
        "visible_response",
        "immediate_consequence",
    )
    causal_values = [
        str(response.get(field) or "")
        for field in causal_fields
        if field in required_fields
    ]
    if (
        len(causal_values) == len(causal_fields)
        and all(causal_values)
        and normalized_unique_count(causal_values) < len(causal_fields)
    ):
        failures.append(
            {
                "check": "moe_response_causal_chain",
                "reason": "baseline, trigger, target, visible response, and consequence must be distinct evidence",
            }
        )

    evidence = response.get("prompt_evidence")
    if not isinstance(evidence, dict):
        evidence = {}
    binding = contract.get("prompt_binding") if isinstance(contract.get("prompt_binding"), dict) else {}
    evidence_fields = [str(item) for item in binding.get("required_evidence_fields") or [] if str(item)]
    evidence_phrases: list[str] = []
    missing_evidence = []
    for field in evidence_fields:
        phrase = str(evidence.get(field) or "").strip()
        if phrase:
            evidence_phrases.append(phrase)
        else:
            missing_evidence.append(field)
    if missing_evidence:
        failures.append(
            {
                "check": "moe_response_binding",
                "reason": "moe response is missing literal prompt evidence",
                "fields": missing_evidence,
            }
        )
    missing_literal = [phrase for phrase in evidence_phrases if not text_contains_term(prompt_en, phrase)]
    if missing_literal:
        failures.append(
            {
                "check": "moe_response_binding",
                "reason": "declared moe-response evidence is not literal in prompt_en",
                "phrases": list(dict.fromkeys(missing_literal)),
            }
        )

    aesthetic_phrase = str(evidence.get("aesthetic_baseline_phrase") or "").lower()
    adult_cues = (
        "adult",
        "mid-twenties",
        "mid twenties",
        "twenty-five",
        "twenty five",
        "late twenties",
        "thirties",
    )
    pretty_cues = (
        "beautiful",
        "bishoujo",
        "bishonen",
        "handsome",
        "pretty",
    )
    cute_cues = (
        "adorable",
        "charming",
        "cute",
        "endearing",
        "kawaii",
    )
    design_detail_groups = (
        ("facial feature", "face", "features"),
        ("eyes", "eye"),
        ("mouth", "lips"),
        ("hair", "grooming"),
        ("cohesive styling", "cohesive character styling"),
    )
    expected_presentation_cues = {
        "adult_bishoujo": ("woman", "female", "feminine", "bishoujo", "she", "her"),
        "adult_bishonen": ("man", "male", "masculine", "bishonen", "he", "his"),
        "adult_beautiful_cute_character": (
            "androgynous",
            "nonbinary",
            "non-binary",
            "gender-neutral",
            "character",
        ),
    }
    if aesthetic_phrase:
        aesthetic_missing = []
        if not any(cue in aesthetic_phrase for cue in adult_cues):
            aesthetic_missing.append("explicit_adult_age")
        if not any(cue in aesthetic_phrase for cue in pretty_cues):
            aesthetic_missing.append("pretty_or_beautiful_read")
        if not any(cue in aesthetic_phrase for cue in cute_cues):
            aesthetic_missing.append("cute_or_charming_read")
        if sum(
            1 for group in design_detail_groups if any(cue in aesthetic_phrase for cue in group)
        ) < 2:
            aesthetic_missing.append("at_least_two_concrete_character_design_details")
        presentation_cues = expected_presentation_cues.get(required_aesthetic, ())
        if presentation_cues and not any(cue in aesthetic_phrase for cue in presentation_cues):
            aesthetic_missing.append("routed_presentation")
        if aesthetic_missing:
            failures.append(
                {
                    "check": "moe_response_aesthetic_evidence",
                    "reason": (
                        "moe requires a literal adult character-design entry condition that reads "
                        "as both pretty/beautiful and cute/charming before the causal event"
                    ),
                    "missing": aesthetic_missing,
                    "phrase": evidence.get("aesthetic_baseline_phrase"),
                }
            )

    identity_control = (
        contract.get("reference_identity_control")
        if isinstance(contract.get("reference_identity_control"), dict)
        else {}
    )
    if identity_control.get("enabled") is True:
        identity_phrase = str(evidence.get("reference_identity_phrase") or "").lower()
        identity_action_cues = (
            "preserve",
            "same identity",
            "sole identity reference",
            "identity unchanged",
        )
        identity_source_cues = (
            "attached portrait",
            "reference portrait",
            "source portrait",
            "uploaded portrait",
        )
        identity_detail_groups = (
            ("eye aperture", "eye shape", "eye spacing"),
            ("nose",),
            ("lip", "mouth"),
            ("face length",),
            ("lower-face", "lower face"),
            ("jaw width",),
            ("cheekbone", "facial geometry"),
            ("skin tone", "natural asymmetry"),
            ("hairline",),
        )
        anti_reshape_groups = (
            (
                "no enlarging",
                "not enlarge",
                "do not enlarge",
                "no eye enlargement",
                "preserve eye aperture",
            ),
            (
                "no rounding",
                "not round",
                "do not round",
                "no eye rounding",
                "preserve eye shape",
            ),
            (
                "no shortening",
                "not shorten",
                "do not shorten",
                "preserve face length",
            ),
            (
                "no narrowing",
                "not narrow",
                "do not narrow",
                "preserve jaw width",
                "preserve lower-face",
                "preserve lower face",
            ),
        )
        compact_no_reshape_clause = all(
            cue in identity_phrase
            for cue in ("no enlarging", "rounding", "shortening", "narrowing")
        )
        missing_identity = []
        if not any(cue in identity_phrase for cue in identity_action_cues):
            missing_identity.append("preservation_instruction")
        if not any(cue in identity_phrase for cue in identity_source_cues):
            missing_identity.append("reference_source")
        if sum(
            1
            for group in identity_detail_groups
            if any(cue in identity_phrase for cue in group)
        ) < 6:
            missing_identity.append("at_least_six_identity_anchors_including_face_proportions")
        if not compact_no_reshape_clause and any(
            not any(cue in identity_phrase for cue in group) for group in anti_reshape_groups
        ):
            missing_identity.append("explicit_anti_reshape_constraints")
        if not any(cue in identity_phrase for cue in ("adult age", "do not de-age", "no de-aging")):
            missing_identity.append("adult_age_preservation")
        if missing_identity:
            failures.append(
                {
                    "check": "moe_response_reference_identity",
                    "reason": (
                        "identity-controlled moe evaluation must hold eye aperture, face length, lower-face and jaw "
                        "proportions, and adult age constant instead of changing facial appeal and scene direction together"
                    ),
                    "missing": missing_identity,
                    "phrase": evidence.get("reference_identity_phrase"),
                }
            )

    affective_phrase = str(evidence.get("affective_leak_phrase") or "").lower()
    warm_affect_groups = MOE_WARM_AFFECT_GROUPS
    negative_affect_cues = MOE_NEGATIVE_AFFECT_CUES
    affective_missing = []
    if affective_phrase:
        if not any(any(cue in affective_phrase for cue in group) for group in warm_affect_groups):
            affective_missing.append("specific_warm_or_pleased_micro_response")
        if sum(cue in affective_phrase for cue in negative_affect_cues) > 2:
            affective_missing.append("negative_affect_exceeds_two_cues")
    if affective_missing:
        failures.append(
            {
                "check": "moe_response_affective_balance",
                "reason": (
                    "the face needs one specific warm or pleased micro-response and may use at most "
                    "two negative-affect cues so guardedness does not collapse into annoyance, sadness, or boredom"
                ),
                "missing": affective_missing,
                "phrase": evidence.get("affective_leak_phrase"),
            }
        )

    affective_prompt = prompt_en.lower()
    affective_contract = (
        contract.get("composition_guidance", {}).get("affective_balance")
        if isinstance(contract.get("composition_guidance"), dict)
        else {}
    )
    if isinstance(affective_contract, dict) and affective_contract.get("required") is True:
        whole_prompt_negative_hits = [
            cue for cue in negative_affect_cues if cue in affective_prompt
        ]
        whole_prompt_warm = any(
            any(cue in affective_prompt for cue in group) for group in warm_affect_groups
        )
        if not whole_prompt_warm or len(whole_prompt_negative_hits) > 2:
            failures.append(
                {
                    "check": "moe_response_affective_balance",
                    "reason": (
                        "the full prompt must retain a warm facial countercue and may contain at most "
                        "two negative-affect cues; splitting extra cold cues across other fields does not pass"
                    ),
                    "negative_terms": whole_prompt_negative_hits,
                    "warm_countercue_present": whole_prompt_warm,
                }
            )

    mechanism_guidance = (
        contract.get("composition_guidance", {}).get("mechanism_specific_evidence", {})
        if isinstance(contract.get("composition_guidance"), dict)
        else {}
    )
    nurturant_guidance = (
        mechanism_guidance.get("nurturant_benevolence", {})
        if isinstance(mechanism_guidance, dict)
        else {}
    )
    if (
        relationship_register == "nurturant_benevolence"
        and isinstance(nurturant_guidance, dict)
        and nurturant_guidance.get("benevolent_affect_phrase_required") is True
    ):
        benevolent_affect_phrase = str(
            evidence.get("benevolent_affect_phrase") or ""
        ).lower()
        benevolent_cue_groups = (
            ("relaxed brow", "relaxed eyebrows", "unfurrowed brow"),
            ("patient soft eyes", "patient eyes", "soft patient eyes"),
            ("reassuring mouth", "reassuring smile", "reassuring lips"),
            (
                "calm protective attention",
                "protective attention",
                "protective focus",
                "protective gaze",
            ),
        )
        benevolent_missing = [
            index
            for index, group in enumerate(benevolent_cue_groups, start=1)
            if not any(cue in benevolent_affect_phrase for cue in group)
        ]
        contradictory_cues = (
            "mid-protest",
            "pursed",
            "huff",
            "head stays aside",
            "head stays angled away",
            "irises return",
            "private liking",
            "romantic interest",
        )
        if (
            not benevolent_affect_phrase
            or not text_contains_term(
                prompt_en,
                str(evidence.get("benevolent_affect_phrase") or ""),
            )
            or benevolent_missing
            or any(cue in benevolent_affect_phrase for cue in contradictory_cues)
        ):
            failures.append(
                {
                    "check": "moe_response_benevolent_affect",
                    "reason": (
                        "nurturant_benevolence needs one literal mature expression combining a relaxed brow, "
                        "patient soft eyes, a reassuring mouth, and calm protective attention without tsundere "
                        "denial or romantic gaze leakage"
                    ),
                    "missing_groups": benevolent_missing,
                    "phrase": evidence.get("benevolent_affect_phrase"),
                }
            )
    denial_guidance = (
        mechanism_guidance.get("denial_care_leak", {})
        if isinstance(mechanism_guidance, dict)
        else {}
    )
    if (
        mechanism == "denial_care_leak"
        and isinstance(denial_guidance, dict)
        and denial_guidance.get("active_denial_phrase_required") is True
    ):
        active_denial_phrase = str(evidence.get("active_denial_phrase") or "").lower()
        active_denial_groups = (
            ("pursed lip", "pursed mouth", "mouth protest", "mid-protest", "tiny huff", "small huff"),
            ("chin lift", "lifted chin", "raised chin"),
            ("half-turned shoulder", "turned shoulder", "shoulder turns away"),
            ("brisk hand", "briskly", "dismissive hand", "offhand", "small thunk"),
        )
        active_denial_present = any(
            any(cue in active_denial_phrase for cue in group)
            for group in active_denial_groups
        )
        if (
            not active_denial_phrase
            or not text_contains_term(prompt_en, str(evidence.get("active_denial_phrase") or ""))
            or not active_denial_present
        ):
            failures.append(
                {
                    "check": "moe_response_active_denial",
                    "reason": (
                        "denial_care_leak needs a separate visible mouth, chin, shoulder, or "
                        "helping-hand protest; guardedness, a label, or averted gaze alone can "
                        "collapse into ordinary quiet kindness"
                    ),
                    "phrase": evidence.get("active_denial_phrase"),
                }
            )

        concealed_affection_phrase = str(
            evidence.get("concealed_affection_phrase") or ""
        ).lower()
        care_action_anchor_phrase = str(
            evidence.get("care_action_anchor_phrase") or ""
        ).lower()
        relationship_gaze_anchor_phrase = str(
            evidence.get("relationship_gaze_anchor_phrase") or ""
        ).lower()
        affection_cues = (
            "affection",
            "fond",
            "fondness",
            "likes",
            "liking",
            "personal liking",
            "private liking",
            "romantic interest",
            "soften",
            "softened",
            "tender",
            "warmth",
        )
        personal_liking_cues = (
            "personal liking",
            "private liking",
            "romantic interest",
            "personally fond",
            "special to her",
            "special to him",
            "special to them",
            "likes him",
            "likes her",
            "likes them",
            "attraction",
        )
        concealment_cues = (
            "almost-smile",
            "almost smile",
            "barely",
            "betray",
            "brief",
            "conceal",
            "hidden",
            "hiding",
            "nearly",
            "restrained",
            "returning",
            "stolen",
            "stops it",
            "suppressed",
        )
        recipient_cues = (
            "customer",
            "partner",
            "recipient",
            "toward her",
            "toward him",
            "toward the viewer",
            "toward their",
            "their eyes",
            "viewer",
        )
        directional_face_cues = (
            "eye",
            "eyes",
            "gaze",
            "glance",
            "lid",
            "look",
            "mouth corner",
            "peek",
            "smile",
        )
        in_frame_cues = (
            "in frame",
            "in-frame",
            "foreground",
            "frame edge",
            "near-lens",
            "near lens",
            "visible",
        )
        care_screen_position_cues = (
            "left",
            "right",
            "lower",
            "bottom",
            "foreground",
            "frame edge",
        )
        care_target_cues = (
            "hand",
            "arm",
            "sleeve",
            "wound",
            "scrape",
            "bandage",
            "knuckle",
            "pastry",
            "cup",
            "gift",
            "lunchbox",
            "note",
            "umbrella",
            "token",
            "object",
            "prop",
        )
        relationship_target_cues = (
            "face-level",
            "face level",
            "eye line",
            "eyeline",
            "outer eye",
            "one eye",
            "eyes",
            "profile",
            "face",
        )
        relationship_position_cues = (
            "above",
            "higher",
            "upper",
            "face-level",
            "face level",
            "near-lens",
            "near lens",
            "frame edge",
            "in frame",
            "in-frame",
            "visible",
        )
        partial_landmark_cues = (
            "partial",
            "sliver",
            "outer eye",
            "one eye",
        )
        partial_face_companion_cues = (
            "temple",
            "profile",
            "cheek edge",
            "brow edge",
        )
        blur_cues = (
            "blurred",
            "soft-focus",
            "soft focus",
            "out-of-focus",
            "out of focus",
        )
        relationship_frame_side_cues = (
            "upper-left",
            "upper left",
            "upper-right",
            "upper right",
            "left frame",
            "right frame",
            "left edge",
            "right edge",
        )
        full_recipient_face_cues = (
            "full recipient face",
            "recipient's full face",
            "customer's full face",
            "partner's full face",
            "second full face",
            "fully shown face",
        )
        off_frame_cues = (
            "off-frame",
            "off frame",
            "out of frame",
            "outside frame",
            "outside the frame",
        )
        care_action_anchor_present = (
            any(cue in care_action_anchor_phrase for cue in recipient_cues)
            and any(cue in care_action_anchor_phrase for cue in care_target_cues)
            and any(cue in care_action_anchor_phrase for cue in in_frame_cues)
            and any(cue in care_action_anchor_phrase for cue in care_screen_position_cues)
            and not any(cue in care_action_anchor_phrase for cue in off_frame_cues)
        )
        if (
            denial_guidance.get("care_action_anchor_phrase_required") is True
            and (
                not care_action_anchor_phrase
                or not text_contains_term(
                    prompt_en,
                    str(evidence.get("care_action_anchor_phrase") or ""),
                )
                or not care_action_anchor_present
            )
        ):
            failures.append(
                {
                    "check": "moe_response_care_action_anchor",
                    "reason": (
                        "denial_care_leak needs a visible hand, wound, or carried object at an explicit "
                        "lower screen position so the helpful action has a concrete endpoint"
                    ),
                    "phrase": evidence.get("care_action_anchor_phrase"),
                }
            )
        relationship_gaze_anchor_present = (
            any(cue in relationship_gaze_anchor_phrase for cue in recipient_cues)
            and "adult" in relationship_gaze_anchor_phrase
            and any(cue in relationship_gaze_anchor_phrase for cue in relationship_target_cues)
            and any(cue in relationship_gaze_anchor_phrase for cue in relationship_position_cues)
            and not any(cue in relationship_gaze_anchor_phrase for cue in off_frame_cues)
            and " ".join(relationship_gaze_anchor_phrase.split())
            != " ".join(care_action_anchor_phrase.split())
        )
        partial_recipient_landmark_present = (
            any(cue in relationship_gaze_anchor_phrase for cue in partial_landmark_cues)
            and any(
                cue in relationship_gaze_anchor_phrase
                for cue in partial_face_companion_cues
            )
            and any(cue in relationship_gaze_anchor_phrase for cue in blur_cues)
            and any(
                cue in relationship_gaze_anchor_phrase
                for cue in relationship_frame_side_cues
            )
            and not any(
                cue in relationship_gaze_anchor_phrase
                for cue in full_recipient_face_cues
            )
        )
        if (
            denial_guidance.get("relationship_gaze_anchor_phrase_required") is True
            and (
                not relationship_gaze_anchor_phrase
                or not text_contains_term(
                    prompt_en,
                    str(evidence.get("relationship_gaze_anchor_phrase") or ""),
                )
                or not relationship_gaze_anchor_present
            )
        ):
            failures.append(
                {
                    "check": "moe_response_relationship_gaze_anchor",
                    "reason": (
                        "denial_care_leak needs a separate face-level eye line for the same adult recipient, "
                        "spatially distinct from the lower care target; the task anchor alone reads as nurturance"
                    ),
                    "phrase": evidence.get("relationship_gaze_anchor_phrase"),
                }
            )
        if (
            denial_guidance.get("partial_recipient_landmark_required") is True
            and not partial_recipient_landmark_present
        ):
            failures.append(
                {
                    "check": "moe_response_partial_recipient_landmark",
                    "reason": (
                        "denial_care_leak needs one visible but subordinate landmark from the same adult "
                        "recipient: a blurred partial outer eye plus temple or profile sliver at a named "
                        "upper frame edge. An imagined eye line, off-frame person, or second full face "
                        "does not make the affection endpoint verifiable"
                    ),
                    "phrase": evidence.get("relationship_gaze_anchor_phrase"),
                }
            )
        head_away_cues = (
            "head stays aside",
            "head stays angled away",
            "head remains aside",
            "head remains angled away",
            "face stays aside",
            "face stays angled away",
            "face remains aside",
            "face remains angled away",
            "three-quarter head",
            "three quarter head",
            "three-quarter face",
            "three quarter face",
        )
        three_quarter_cues = (
            "three-quarter head",
            "three quarter head",
            "three-quarter face",
            "three quarter face",
            "three-quarter view",
            "three quarter view",
        )
        nose_off_lens_cues = (
            "nose axis off the lens",
            "nose points away from the lens",
            "nose stays off-axis",
            "nose remains off-axis",
            "nose points left",
            "nose points right",
        )
        iris_return_cues = (
            "iris",
            "irises",
            "pupils",
            "eyes return",
            "gaze returns",
            "glance returns",
            "returning glance",
            "stolen glance",
        )
        lower_lid_cues = (
            "lower lids soften",
            "softened lower lids",
            "lower eyelids soften",
            "softened lower eyelids",
        )
        suppressed_mouth_cues = (
            "almost-smile",
            "almost smile",
            "mouth corner nearly lifts",
            "mouth corner almost lifts",
            "mouth corner starts to lift",
            "mouth corner begins to lift",
            "one mouth corner starts",
            "one mouth corner begins",
            "suppressed smile",
            "suppresses a smile",
            "then flattens",
            "before flattening",
        )
        oblique_return_cues = (
            "small oblique return",
            "small sideways return",
            "slight oblique return",
            "brief oblique return",
            "only the irises",
            "irises alone",
            "pupils alone",
        )
        frame_side_cues = (
            "upper-left",
            "upper left",
            "upper-right",
            "upper right",
            "left of lens",
            "right of lens",
            "left frame",
            "right frame",
        )
        overt_frontal_cues = (
            "direct eye contact",
            "direct frontal",
            "directly at the camera",
            "directly into the camera",
            "faces the camera",
            "facing the camera",
            "front-facing",
            "frontal face",
            "centered face",
            "selfie gaze",
            "viewer-facing gaze",
        )
        relationship_geometry_terms = (
            "face-level",
            "face level",
            "eye line",
            "eyeline",
            "profile",
            "face",
            "eyes",
            "near-lens",
            "near lens",
        )
        care_target_gaze_cues = (
            "toward the hand",
            "to the hand",
            "at the hand",
            "toward the wound",
            "toward the scrape",
            "toward the bandage",
            "toward the knuckle",
            "toward the pastry",
            "toward the cup",
            "toward the object",
            "toward the task",
        )
        nurturant_affect_cues = (
            "benevolent",
            "maternal",
            "motherly",
            "mamang",
            "mommy",
            "nurturant",
            "nurturing",
            "protective concern",
        )
        head_left = any(
            cue in concealed_affection_phrase
            for cue in (
                "head turns left",
                "head turned left",
                "head angles left",
                "face turns left",
                "face angled left",
            )
        )
        head_right = any(
            cue in concealed_affection_phrase
            for cue in (
                "head turns right",
                "head turned right",
                "head angles right",
                "face turns right",
                "face angled right",
            )
        )
        nose_left = any(
            cue in concealed_affection_phrase
            for cue in ("nose points left", "nose axis points left")
        )
        nose_right = any(
            cue in concealed_affection_phrase
            for cue in ("nose points right", "nose axis points right")
        )
        anchor_left = any(
            cue in relationship_gaze_anchor_phrase
            for cue in ("upper-left", "upper left", "left frame", "left edge")
        )
        anchor_right = any(
            cue in relationship_gaze_anchor_phrase
            for cue in ("upper-right", "upper right", "right frame", "right edge")
        )
        iris_left = bool(
            re.search(
                r"(?:iris|irises|pupil|pupils).{0,80}(?:upper-left|upper left|left frame|left edge)",
                concealed_affection_phrase,
            )
        )
        iris_right = bool(
            re.search(
                r"(?:iris|irises|pupil|pupils).{0,80}(?:upper-right|upper right|right frame|right edge)",
                concealed_affection_phrase,
            )
        )
        opposed_head_iris_vector_present = (
            (
                head_right
                and nose_right
                and anchor_left
                and iris_left
                and not (head_left or nose_left or anchor_right or iris_right)
            )
            or (
                head_left
                and nose_left
                and anchor_right
                and iris_right
                and not (head_right or nose_right or anchor_left or iris_left)
            )
        )
        if (
            denial_guidance.get("opposed_head_iris_vector_required") is True
            and not opposed_head_iris_vector_present
        ):
            failures.append(
                {
                    "check": "moe_response_opposed_head_iris_vector",
                    "reason": (
                        "the head and nose must name one side while the partial recipient landmark and "
                        "iris return name the opposite side. Turning head and irises together creates a "
                        "generic side-look rather than concealed liking"
                    ),
                    "anchor_phrase": evidence.get("relationship_gaze_anchor_phrase"),
                    "concealed_affection_phrase": evidence.get("concealed_affection_phrase"),
                }
            )
        affection_vector_present = (
            any(cue in concealed_affection_phrase for cue in head_away_cues)
            and any(cue in concealed_affection_phrase for cue in three_quarter_cues)
            and any(cue in concealed_affection_phrase for cue in nose_off_lens_cues)
            and any(cue in concealed_affection_phrase for cue in iris_return_cues)
            and any(cue in concealed_affection_phrase for cue in oblique_return_cues)
            and any(cue in concealed_affection_phrase for cue in lower_lid_cues)
            and any(cue in concealed_affection_phrase for cue in suppressed_mouth_cues)
            and any(cue in concealed_affection_phrase for cue in frame_side_cues)
            and (
                any(
                    cue in concealed_affection_phrase and cue in relationship_gaze_anchor_phrase
                    for cue in relationship_geometry_terms
                )
                or any(
                    cue in concealed_affection_phrase and cue in relationship_gaze_anchor_phrase
                    for cue in frame_side_cues
                )
            )
            and not any(cue in concealed_affection_phrase for cue in care_target_gaze_cues)
            and not any(cue in concealed_affection_phrase for cue in overt_frontal_cues)
            and (
                denial_guidance.get("opposed_head_iris_vector_required") is not True
                or opposed_head_iris_vector_present
            )
        )
        concealed_affection_present = (
            any(cue in concealed_affection_phrase for cue in affection_cues)
            and any(cue in concealed_affection_phrase for cue in personal_liking_cues)
            and any(cue in concealed_affection_phrase for cue in concealment_cues)
            and any(cue in concealed_affection_phrase for cue in directional_face_cues)
            and not any(cue in concealed_affection_phrase for cue in nurturant_affect_cues)
            and affection_vector_present
        )
        if (
            denial_guidance.get("concealed_affection_phrase_required") is True
            and (
                not concealed_affection_phrase
                or not text_contains_term(
                    prompt_en,
                    str(evidence.get("concealed_affection_phrase") or ""),
                )
                or not concealed_affection_present
            )
        ):
            failures.append(
                {
                    "check": "moe_response_concealed_affection",
                    "reason": (
                        "denial_care_leak needs a named three-quarter head turn with the nose axis off the lens, "
                        "toward the side opposite a visible partial recipient landmark, with only the irises making a "
                        "small oblique return toward that landmark, softened lower lids, and one mouth corner beginning "
                        "to lift before suppression. Direct "
                        "frontal eye contact, care-target gaze, or maternal benevolence is not concealed peer liking"
                    ),
                    "phrase": evidence.get("concealed_affection_phrase"),
                }
            )

    response_phrase = str(evidence.get("visible_response_phrase") or "").lower()
    response_action_cues = (
        "gaze",
        "look",
        "blink",
        "mouth",
        "lip",
        "huff",
        "hand",
        "finger",
        "grip",
        "shoulder",
        "posture",
        "turn",
        "pause",
        "recoil",
        "twitch",
        "flatten",
        "tilt",
        "pupil",
        "tail",
        "composure",
    )
    if response_phrase and not any(cue in response_phrase for cue in response_action_cues):
        failures.append(
            {
                "check": "moe_response_visible_response",
                "reason": "visible response must show face, gaze, hand, posture, or involuntary reflex evidence",
                "phrase": evidence.get("visible_response_phrase"),
            }
        )

    focal_phrase = str(evidence.get("focal_plane_phrase") or "").lower()
    if focal_phrase and (
        "focal" not in focal_phrase
        or not any(term in focal_phrase for term in ("face", "gaze", "eyes", "mouth"))
        or not any(term in focal_phrase for term in ("hand", "finger", "posture", "target", "object", "prop"))
    ):
        failures.append(
            {
                "check": "moe_response_focal_plane",
                "reason": "focal-plane evidence must bind the facial response with hands/posture and the target",
                "phrase": evidence.get("focal_plane_phrase"),
            }
        )

    event_phase_phrase = str(evidence.get("event_phase_phrase") or "").lower()
    event_phase_cues = (
        "as ",
        "before",
        "caught",
        "during",
        "in the act",
        "just as",
        "mid-",
        "while",
    )
    if event_phase_phrase and not any(cue in event_phase_phrase for cue in event_phase_cues):
        failures.append(
            {
                "check": "moe_response_event_phase",
                "reason": "event-phase evidence must bind the frame to an unfinished transition, not a settled endpoint",
                "phrase": evidence.get("event_phase_phrase"),
            }
        )

    state_geometry_blob = " ".join(
        str(evidence.get(field) or "").lower()
        for field in (
            "event_phase_phrase",
            "target_phrase",
            "immediate_consequence_phrase",
        )
    )
    state_geometry_cues = (
        "above",
        "below",
        "broken",
        "crooked",
        "gap",
        "half-",
        "halfway",
        "inverted",
        "kink",
        "off-center",
        "open ",
        "outside",
        "partway",
        "slipping",
        "tilted",
        "unseated",
    )
    if state_geometry_blob and not any(cue in state_geometry_blob for cue in state_geometry_cues):
        failures.append(
            {
                "check": "moe_response_state_geometry",
                "reason": (
                    "event, target, and consequence evidence must name a visible physical separation "
                    "that distinguishes the unfinished state from its settled endpoint"
                ),
            }
        )

    if "nonhuman_reflex_leak" in {mechanism, *support_values}:
        direction_phrase = response_phrase
        body_cues = ("ear", "tail", "pupil", "posture")
        direction_cues = ("toward", "away", "aim", "left", "right", "nearer", "trigger-side")
        if not any(cue in direction_phrase for cue in body_cues) or not any(
            cue in direction_phrase for cue in direction_cues
        ):
            failures.append(
                {
                    "check": "moe_response_reflex_direction",
                    "reason": "a nonhuman reflex must name the responding body part and its direction toward a visible trigger",
                    "phrase": evidence.get("visible_response_phrase"),
                }
            )
        if "ear" in direction_phrase:
            asymmetric_cues = (
                "one ear",
                "nearer ear",
                "trigger-side ear",
                "left ear",
                "right ear",
                "other ear",
                "far ear",
                "asymmetric",
            )
            if not any(cue in direction_phrase for cue in asymmetric_cues):
                failures.append(
                    {
                        "check": "moe_response_reflex_direction",
                        "reason": "an ear reflex must be asymmetric rather than two static symmetrical ears",
                        "phrase": evidence.get("visible_response_phrase"),
                    }
                )
            compact_ear_cues = (
                "compact ear",
                "compact ears",
                "small ear",
                "small ears",
                "human-ear-scale",
                "human ear scale",
                "no taller than her human ear",
                "no taller than his human ear",
                "no taller than the visible human ear",
                "human-ear height",
            )
            angle_difference_cues = (
                "different angle",
                "different angles",
                "unequal angle",
                "unequal angles",
                "other ear keeps",
                "far ear keeps",
                "baseline angle",
            )
            reflex_missing = []
            if not any(cue in direction_phrase for cue in compact_ear_cues):
                reflex_missing.append("compact_human_ear_scale")
            if not any(cue in direction_phrase for cue in angle_difference_cues):
                reflex_missing.append("clearly_different_ear_angles")
            if reflex_missing:
                failures.append(
                    {
                        "check": "moe_response_nekomimi_scale_direction",
                        "reason": (
                            "a nekomimi ear reflex must keep each living ear compact and make the two "
                            "ear-tip angles visibly different"
                        ),
                        "missing": reflex_missing,
                        "phrase": evidence.get("visible_response_phrase"),
                    }
                )

    text_free_background = (
        contract.get("composition_guidance", {}).get("render_legibility", {}).get("text_free_background")
        if isinstance(contract.get("composition_guidance"), dict)
        else None
    )
    if text_free_background:
        background_phrase = str(evidence.get("background_control_phrase") or "").lower()
        if not background_phrase:
            failures.append(
                {
                    "check": "moe_response_background_control",
                    "reason": "moe composition requires literal unlettered-background evidence",
                    "fields": ["background_control_phrase"],
                }
            )
        else:
            background_surface_cues = (
                "plain background",
                "plain wall",
                "unlettered",
                "without text",
                "no text",
                "text-free",
                "unwritten",
                "unmarked wall",
                "soft bokeh without signs",
            )
            forbidden_background_cues = (
                "chalkboard",
                "lettering",
                "menu board",
                "pseudo-writing",
                "signage",
                "written text",
            )
            if (
                not text_contains_term(prompt_en, str(evidence.get("background_control_phrase") or ""))
                or not any(cue in background_phrase for cue in background_surface_cues)
                or any(cue in background_phrase for cue in forbidden_background_cues)
            ):
                failures.append(
                    {
                        "check": "moe_response_background_control",
                        "reason": (
                            "background evidence must literally request a plain or unlettered surface "
                            "without menus, signs, pseudo-writing, or other generated text"
                        ),
                        "phrase": evidence.get("background_control_phrase"),
                    }
                )

    weak_only_tokens = {
        "adorable",
        "anime",
        "beautiful",
        "blush",
        "blushing",
        "cat",
        "cute",
        "ears",
        "kawaii",
        "maid",
        "moe",
        "pretty",
        "shy",
        "smile",
    }
    weak_only = []
    for phrase in evidence_phrases:
        tokens = {token for token in re.findall(r"[a-z]+", phrase.lower()) if token}
        if tokens and tokens <= weak_only_tokens:
            weak_only.append(phrase)
    if weak_only:
        failures.append(
            {
                "check": "moe_response_shortcut",
                "reason": "cute labels, blush, ears, costume, or a shy smile alone are not moe-response evidence",
                "phrases": weak_only,
            }
        )

    youth_fragments = (
        "baby face",
        "baby-faced",
        "childlike",
        "child-like",
        "schoolgirl",
        "schoolboy",
        "teenage",
        "youthful proportions",
        "oversized eyes",
        "young-looking",
        "looks underage",
    )
    youth_hits = [fragment for fragment in youth_fragments if fragment in prompt_en.lower()]
    if youth_hits:
        failures.append(
            {
                "check": "moe_response_adult_guard",
                "reason": "youth morphology or minor coding cannot be used as moe evidence",
                "terms": youth_hits,
            }
        )

    if str(contract.get("sexual_tone") or "") == "nonsexual":
        sensual_fragments = (
            "cleavage",
            "chest-forward",
            "fetish",
            "lingerie",
            "pin-up",
            "seductive",
            "sultry",
            "sensual gaze",
            "sensual pose",
            "sexualized",
            "sexualised",
        )
        sensual_hits = [fragment for fragment in sensual_fragments if fragment in prompt_en.lower()]
        if sensual_hits:
            failures.append(
                {
                    "check": "moe_response_nonsexual_tone",
                    "reason": "nonsexual moe response contains sensual or body-emphasis direction",
                    "terms": sensual_hits,
                }
            )
    return failures


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
    authorial_mode = str(contract.get("contract_version") or "") == "photo-hybrid-augmentation/v2"
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

    adopted_ids: set[str] = set()
    adopted_states = {"transformed"} if authorial_mode else {"accepted", "modified"}
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
        if state in adopted_states:
            adopted_ids.add(candidate_id)
            evidence = str(decision.get("prompt_evidence") or "").strip()
            if candidate_id not in chosen:
                failures.append(
                    {
                        "check": "hybrid_augmentation_provenance",
                        "reason": (
                            "transformed augmentation candidate is missing from chosen_candidate_ids"
                            if authorial_mode
                            else "accepted or modified augmentation candidate is missing from chosen_candidate_ids"
                        ),
                        "candidate_id": candidate_id,
                    }
                )
            if not evidence or not text_contains_term(prompt_en, evidence):
                failures.append(
                    {
                        "check": "hybrid_augmentation_binding",
                        "reason": (
                            "transformed detail requires newly authored literal prompt_evidence"
                            if authorial_mode
                            else "accepted or modified detail requires literal prompt_evidence"
                        ),
                        "candidate_id": candidate_id,
                        "prompt_evidence": evidence or None,
                    }
                )
            if authorial_mode:
                interpretation = str(decision.get("artistic_interpretation") or "").strip()
                transformation = str(decision.get("transformation") or "").strip()
                dimensions = [
                    str(item)
                    for item in decision.get("transformation_dimensions") or []
                    if str(item).strip()
                ]
                allowed_dimensions = {
                    str(item)
                    for item in adoption.get("transformation_dimensions") or []
                    if str(item).strip()
                }
                if not interpretation or not transformation or not dimensions:
                    failures.append(
                        {
                            "check": "hybrid_augmentation_authorial_transform",
                            "reason": (
                                "transformed detail requires artistic_interpretation, transformation, "
                                "and at least one transformation dimension"
                            ),
                            "candidate_id": candidate_id,
                        }
                    )
                unknown_dimensions = sorted(set(dimensions) - allowed_dimensions)
                if unknown_dimensions:
                    failures.append(
                        {
                            "check": "hybrid_augmentation_authorial_transform",
                            "reason": "transformed detail uses an unknown transformation dimension",
                            "candidate_id": candidate_id,
                            "dimensions": unknown_dimensions,
                        }
                    )
                source_candidate = candidate_objects.get(candidate_id, {})
                source_terms = {
                    str(item).lower()
                    for item in source_candidate.get("concept_terms") or []
                    if str(item).strip()
                }
                evidence_terms = authorial_evidence_tokens(evidence)
                if (
                    evidence
                    and (
                        len(evidence_terms) < 3
                        or not (evidence_terms - source_terms)
                    )
                ):
                    failures.append(
                        {
                            "check": "hybrid_augmentation_authorial_transform",
                            "reason": (
                                "prompt_evidence must add authored context or causality beyond the "
                                "candidate's unordered source terms"
                            ),
                            "candidate_id": candidate_id,
                            "source_terms": sorted(source_terms),
                        }
                    )
            if not authorial_mode and state == "modified" and not str(
                decision.get("modification") or ""
            ).strip():
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
            accepted_min = int(
                adoption.get(
                    "minimum_transformed_if_selected" if authorial_mode else "minimum_accepted_if_selected",
                    1 if authorial_mode else 2,
                )
                or (1 if authorial_mode else 2)
            )
        except (TypeError, ValueError):
            accepted_min = 1 if authorial_mode else 2
        try:
            accepted_max = int(
                adoption.get("maximum_transformed" if authorial_mode else "maximum_accepted", 3 if authorial_mode else 5)
                or (3 if authorial_mode else 5)
            )
        except (TypeError, ValueError):
            accepted_max = 3 if authorial_mode else 5
        if len(adopted_ids) < accepted_min or len(adopted_ids) > accepted_max:
            failures.append(
                {
                    "check": "hybrid_augmentation_budget",
                    "reason": (
                        "transformed augmentation detail count is outside the declared budget"
                        if authorial_mode
                        else "accepted augmentation detail count is outside the declared budget"
                    ),
                    "minimum": accepted_min,
                    "maximum": accepted_max,
                    "actual": len(adopted_ids),
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
                if authorial_mode:
                    interpretation = str(actual_axis.get("artistic_interpretation") or "").strip()
                    axis_evidence = str(actual_axis.get("prompt_evidence") or "").strip()
                    if (
                        not interpretation
                        or not axis_evidence
                        or not text_contains_term(prompt_en, axis_evidence)
                    ):
                        failures.append(
                            {
                                "check": "adult_appeal_axes",
                                "reason": (
                                    "every active adult-appeal axis requires an agent-authored "
                                    "interpretation with literal prompt evidence"
                                ),
                                "axis": axis_id,
                            }
                        )
                else:
                    inventory_ids = {
                        str(candidate.get("id") or "")
                        for candidate in axis_contract.get("candidate_inventory") or []
                        if isinstance(candidate, dict) and str(candidate.get("id") or "")
                    }
                    if not (adopted_ids & inventory_ids):
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


def audit_authorial_scene(
    pack: dict[str, Any],
    composed: dict[str, Any],
    prompt_en: str,
) -> list[dict[str, Any]]:
    scene_contract = pack.get("scene_contract") if isinstance(pack.get("scene_contract"), dict) else {}
    groups = [
        group
        for group in scene_contract.get("groups") or []
        if isinstance(group, dict)
        and str(group.get("strategy") or "") == "authorial_scene"
        and str(group.get("source") or "") == "selected_render_blueprint_abstraction"
    ]
    if not groups:
        return []

    authored = composed.get("authored_scene")
    if not isinstance(authored, dict):
        return [
            {
                "check": "authorial_scene",
                "reason": "v4 abstract scene contract requires an authored_scene object",
            }
        ]

    failures: list[dict[str, Any]] = []
    if not str(authored.get("governing_premise") or "").strip() or not str(
        authored.get("artistic_rationale") or ""
    ).strip():
        failures.append(
            {
                "check": "authorial_scene_judgment",
                "reason": "authored_scene requires a governing_premise and artistic_rationale",
            }
        )

    atoms = authored.get("atoms") if isinstance(authored.get("atoms"), dict) else {}
    required_slots = list(
        dict.fromkeys(
            str(slot)
            for group in groups
            for slot in group.get("required_authored_slots") or []
            if str(slot)
        )
    )
    evidence_phrases: list[str] = []
    for slot in required_slots:
        phrase = str(atoms.get(slot) or "").strip()
        if not phrase:
            failures.append(
                {
                    "check": "authorial_scene_atoms",
                    "reason": "authored scene is missing a required newly written atom",
                    "slot": slot,
                }
            )
            continue
        evidence_phrases.append(phrase)
        if not text_contains_term(prompt_en, phrase):
            failures.append(
                {
                    "check": "authorial_scene_binding",
                    "reason": "authored scene atom is not literal in prompt_en",
                    "slot": slot,
                    "prompt_evidence": phrase,
                }
            )
        if len(authorial_evidence_tokens(phrase)) < 3:
            failures.append(
                {
                    "check": "authorial_scene_atoms",
                    "reason": "authored scene atom is too fragmentary to establish an original relation",
                    "slot": slot,
                }
            )
    if len({phrase.lower() for phrase in evidence_phrases}) != len(evidence_phrases):
        failures.append(
            {
                "check": "authorial_scene_atoms",
                "reason": "subject, action, location, and prop must be distinct authored decisions",
            }
        )
    coverage = pack.get("coverage") if isinstance(pack.get("coverage"), dict) else {}
    intent_constraints = (
        coverage.get("intent_constraints")
        if isinstance(coverage.get("intent_constraints"), dict)
        else {}
    )
    subject_atom = str(atoms.get("subject") or "")
    if intent_constraints.get("no_people") and re.search(
        r"\b(?:adult|boy|girl|human|man|men|person|people|woman|women)\b",
        subject_atom,
        flags=re.IGNORECASE,
    ):
        failures.append(
            {
                "check": "negative_presence_constraint",
                "reason": "no-people authored scene contains an explicit human subject term",
            }
        )

    choices = [row for row in authored.get("interpretive_choices") or [] if isinstance(row, dict)]
    minimum_choices = max(
        [
            int((group.get("composition_policy") or {}).get("minimum_interpretive_choices", 2) or 2)
            for group in groups
        ]
        or [2]
    )
    allowed_dimensions = {
        str(item)
        for group in groups
        for item in (group.get("composition_policy") or {}).get("interpretive_dimensions") or []
        if str(item)
    }
    choice_dimensions = [str(row.get("dimension") or "") for row in choices]
    invalid_choices = [
        row
        for row in choices
        if not str(row.get("dimension") or "").strip()
        or not str(row.get("decision") or "").strip()
        or not str(row.get("reason") or "").strip()
        or (allowed_dimensions and str(row.get("dimension") or "") not in allowed_dimensions)
    ]
    if (
        len(choices) < minimum_choices
        or len(set(choice_dimensions)) < minimum_choices
        or invalid_choices
    ):
        failures.append(
            {
                "check": "authorial_scene_judgment",
                "reason": (
                    "authored_scene requires distinct valid interpretive choices with a decision "
                    "and artistic reason"
                ),
                "minimum": minimum_choices,
                "actual_dimensions": choice_dimensions,
            }
        )
    return failures


def audit_authorial_open_slots(
    pack: dict[str, Any],
    composed: dict[str, Any],
    prompt_en: str,
) -> list[dict[str, Any]]:
    contracts = [
        row
        for row in pack.get("authorial_open_slots") or []
        if isinstance(row, dict) and str(row.get("slot") or "")
    ]
    if not contracts:
        return []
    authored_slots = composed.get("authored_slots")
    if not isinstance(authored_slots, dict):
        return [
            {
                "check": "authorial_open_slots",
                "reason": "v4 authorial openings require an authored_slots object",
                "slots": [str(row.get("slot")) for row in contracts],
            }
        ]

    failures: list[dict[str, Any]] = []
    for contract in contracts:
        slot = str(contract.get("slot") or "")
        decision = authored_slots.get(slot)
        if not isinstance(decision, dict):
            failures.append(
                {
                    "check": "authorial_open_slots",
                    "reason": "missing authored decision for an open singleton scene slot",
                    "slot": slot,
                }
            )
            continue
        evidence = str(decision.get("prompt_evidence") or "").strip()
        rationale = str(decision.get("artistic_rationale") or "").strip()
        if (
            not evidence
            or not rationale
            or not text_contains_term(prompt_en, evidence)
            or len(authorial_evidence_tokens(evidence)) < 3
        ):
            failures.append(
                {
                    "check": "authorial_open_slots",
                    "reason": (
                        "each open slot needs a newly authored literal prompt phrase and artistic rationale"
                    ),
                    "slot": slot,
                    "prompt_evidence": evidence or None,
                }
            )
        constraints = contract.get("constraints") if isinstance(contract.get("constraints"), dict) else {}
        scene_family = str(constraints.get("scene_family") or "")
        acknowledgments = {
            str(item)
            for item in decision.get("constraint_acknowledgments") or []
            if str(item).strip()
        }
        if scene_family and scene_family not in acknowledgments:
            failures.append(
                {
                    "check": "authorial_open_slot_constraints",
                    "reason": "authored location must acknowledge its required role-scene family",
                    "slot": slot,
                    "required": scene_family,
                }
            )
        forbidden_hits = [
            str(term)
            for term in constraints.get("forbidden_concepts") or []
            if text_contains_term(evidence, str(term).replace("_", " "))
        ]
        if forbidden_hits:
            failures.append(
                {
                    "check": "authorial_open_slot_constraints",
                    "reason": "authored slot uses a forbidden role-scene concept",
                    "slot": slot,
                    "concepts": forbidden_hits,
                }
            )
        if constraints.get("no_people") and re.search(
            r"\b(?:adult|boy|girl|human|man|men|person|people|woman|women)\b",
            evidence,
            flags=re.IGNORECASE,
        ):
            failures.append(
                {
                    "check": "negative_presence_constraint",
                    "reason": "no-people authorial subject contains an explicit human term",
                    "slot": slot,
                }
            )
    unexpected = sorted(set(authored_slots) - {str(row.get("slot")) for row in contracts})
    if unexpected:
        failures.append(
            {
                "check": "authorial_open_slots",
                "reason": "authored_slots contains a slot that was not opened by the pack",
                "slots": unexpected,
            }
        )
    return failures


def audit_authorial_request(
    pack: dict[str, Any],
    composed: dict[str, Any],
    prompt_en: str,
) -> list[dict[str, Any]]:
    request = (
        pack.get("authorial_request")
        if isinstance(pack.get("authorial_request"), dict)
        else None
    )
    if not isinstance(request, dict):
        return []
    failures: list[dict[str, Any]] = []
    canonical_fields = (
        "contract_version",
        "provenance",
        "subject",
        "setting",
        "event",
        "style_domain",
        "style_family",
        "style_evidence",
        "variation_key",
    )
    canonical = {key: request.get(key) for key in canonical_fields}
    expected_sha = hashlib.sha256(
        json.dumps(
            canonical,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    actual_sha = str(request.get("canonical_sha256") or "")
    if (
        request.get("contract_version") != "authorial-request/v1"
        or request.get("provenance") != "agent_prepack"
        or actual_sha != expected_sha
        or str(request.get("request_id") or "") != expected_sha[:16]
    ):
        failures.append(
            {
                "check": "authorial_request_integrity",
                "reason": "pre-pack authorial request schema, provenance or canonical hash is invalid",
            }
        )
    authored_scene = (
        composed.get("authored_scene")
        if isinstance(composed.get("authored_scene"), dict)
        else {}
    )
    if str(authored_scene.get("source_authorial_request_sha256") or "") != actual_sha:
        failures.append(
            {
                "check": "authorial_request_provenance",
                "reason": "authored_scene is not bound to the frozen pre-pack authorial request hash",
            }
        )
    atoms = authored_scene.get("atoms") if isinstance(authored_scene.get("atoms"), dict) else {}
    field_atoms = {
        "subject": "subject",
        "setting": "location",
        "event": "action",
    }
    for request_field, atom_field in field_atoms.items():
        source_tokens = authorial_evidence_tokens(str(request.get(request_field) or ""))
        atom_tokens = authorial_evidence_tokens(str(atoms.get(atom_field) or ""))
        prompt_tokens = authorial_evidence_tokens(prompt_en)
        minimum_overlap = min(3, len(source_tokens))
        if minimum_overlap < 2 or len(source_tokens & atom_tokens) < minimum_overlap:
            failures.append(
                {
                    "check": "authorial_request_binding",
                    "reason": "authored scene atom does not preserve the pre-pack request meaning",
                    "request_field": request_field,
                    "atom_field": atom_field,
                }
            )
        if minimum_overlap >= 2 and len(source_tokens & prompt_tokens) < minimum_overlap:
            failures.append(
                {
                    "check": "authorial_request_binding",
                    "reason": "prompt_en does not preserve the pre-pack request meaning",
                    "request_field": request_field,
                }
            )
    style_contract = (
        pack.get("japanese_subculture_photo")
        if isinstance(pack.get("japanese_subculture_photo"), dict)
        else {}
    )
    if (
        str(style_contract.get("source_authorial_request_sha256") or "") != actual_sha
        or str(style_contract.get("style_family_id") or "")
        != str(request.get("style_family") or "")
    ):
        failures.append(
            {
                "check": "authorial_request_style_binding",
                "reason": "typed Japanese-subculture style is not bound to the pre-pack request",
            }
        )
    return failures


def audit_japanese_subculture_photo(
    pack: dict[str, Any],
    prompt_en: str,
) -> list[dict[str, Any]]:
    contract = (
        pack.get("japanese_subculture_photo")
        if isinstance(pack.get("japanese_subculture_photo"), dict)
        else None
    )
    if not isinstance(contract, dict) or contract.get("requested") is not True:
        return []
    failures: list[dict[str, Any]] = []
    if (
        contract.get("contract_version") != "japanese-subculture-photo/v1"
        or not str(contract.get("style_family_id") or "")
        or not str(contract.get("style_family_label") or "")
    ):
        failures.append(
            {
                "check": "japanese_subculture_style_contract",
                "reason": "typed Japanese-subculture photo contract is incomplete",
            }
        )
    cues = [
        cue
        for cue in contract.get("visible_cues") or []
        if isinstance(cue, dict)
        and str(cue.get("cue_id") or "")
        and str(cue.get("prompt_phrase") or "")
    ]
    try:
        minimum = max(2, int(contract.get("minimum_visible_cues") or 2))
    except (TypeError, ValueError):
        minimum = 2
        failures.append(
            {
                "check": "japanese_subculture_style_contract",
                "reason": "minimum_visible_cues must be an integer",
            }
        )
    if len(cues) < minimum:
        failures.append(
            {
                "check": "japanese_subculture_style_contract",
                "reason": "style contract exposes fewer than two concrete visible cues",
                "visible_cue_count": len(cues),
            }
        )
    literal_cues = [
        str(cue["prompt_phrase"])
        for cue in cues
        if text_contains_term(prompt_en, str(cue["prompt_phrase"]))
    ]
    if len(literal_cues) < minimum:
        failures.append(
            {
                "check": "japanese_subculture_style_evidence",
                "reason": "style label is not backed by enough literal visible cues",
                "minimum": minimum,
                "literal_cue_count": len(literal_cues),
                "accepted_cues": [str(cue["prompt_phrase"]) for cue in cues],
            }
        )

    identity_policy = (
        contract.get("identity_policy")
        if isinstance(contract.get("identity_policy"), dict)
        else {}
    )
    if identity_policy.get("infer_ethnicity_or_nationality") is not False:
        failures.append(
            {
                "check": "japanese_subculture_style_contract",
                "reason": "style contract must forbid ethnicity or nationality inference",
            }
        )
    inference_patterns = (
        r"\bjapanese\s+(?:woman|man|person|girl|boy|ethnicity|nationality|facial\s+features?)\b",
        r"\b(?:ethnically|racially)\s+japanese\b",
        r"일본인\s*(?:여성|남성|인물|얼굴|외모|혈통)",
        r"日本人(?:の)?(?:女性|男性|人物|顔|容姿|血統)",
    )
    if any(re.search(pattern, prompt_en, flags=re.IGNORECASE) for pattern in inference_patterns):
        failures.append(
            {
                "check": "japanese_subculture_ethnicity_inference",
                "reason": "subculture style was converted into an unrequested ethnicity or nationality claim",
            }
        )

    guard = (
        contract.get("candidate_guard")
        if isinstance(contract.get("candidate_guard"), dict)
        else {}
    )
    blocked = {
        str(item)
        for item in guard.get("blocked_unrequested_entry_ids") or []
        if str(item)
    }
    preserved = {
        str(item)
        for item in guard.get("explicitly_preserved_entry_ids") or []
        if str(item)
    }
    leaked: list[dict[str, str]] = []
    for slot, payload in (pack.get("slots") or {}).items():
        if not isinstance(payload, dict):
            continue
        for candidate in payload.get("candidates") or []:
            if not isinstance(candidate, dict):
                continue
            entry_id = str(candidate.get("entry_id") or "")
            if entry_id in blocked and entry_id not in preserved:
                leaked.append({"slot": str(slot), "entry_id": entry_id})
    if leaked:
        failures.append(
            {
                "check": "japanese_subculture_candidate_relevance",
                "reason": "unrequested strong-theme candidates remain exposed",
                "candidates": leaked,
            }
        )
    return failures


def audit_candidate_semantic_contracts(
    pack: dict[str, Any], prompt_en: str, chosen: set[str],
    candidates: dict[str, dict[str, Any]], interpretations: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Bind optional semantic units to full adopted component/relationship evidence."""
    version = pack.get("candidate_semantic_surface_version")
    bundles = pack.get("candidate_bundles")
    if version is None and bundles is None:
        return []  # Immutable legacy v4/v5/v6 surfaces retain their contract.
    failures: list[dict[str, Any]] = []

    def fail(candidate_id: str, reason: str) -> None:
        failures.append({"check": "candidate_semantic_contract", "candidate_id": candidate_id, "reason": reason})

    if pack.get("contract_version") != "photo-candidate-pack/v6" or version != photo_candidate_semantics.SURFACE_VERSION:
        fail("", "semantic-unit candidates require the declared modern v6 surface version")
        return failures
    if not isinstance(bundles, dict) or bundles.get("contract_version") != photo_candidate_semantics.BUNDLE_VERSION or bundles.get("adoption") != "optional" or bundles.get("candidate_order") != "seed_shuffled_non_preferential":
        fail("", "candidate bundles require their versioned optional non-ranked contract")
        return failures
    # Load from this auditor's skill snapshot, never a path asserted by a pack.
    # Recompute admission instead of trusting its published hash or booleans.
    try:
        assets = Path(__file__).resolve().parents[1] / "assets"
        source_data = candidate_semantics_generator.load_json(assets / "photo_prompt_tags.json")
        source_data[candidate_semantics_generator.QUALITY_LAYERS_DATA_KEY] = candidate_semantics_generator.load_quality_layers(assets / "photo_prompt_quality_layers.json")
        expected_bundles = candidate_semantics_generator.candidate_pack_candidate_bundles(source_data, pack)
        if bundles != expected_bundles:
            fail("", "candidate bundle contents or joint admission differ from the same source snapshot and frozen core")
    except (OSError, TypeError, ValueError, KeyError) as exc:
        fail("", f"candidate bundle source recomputation failed: {exc}")
    open_dimensions = set(((pack.get("authorial_core") or {}).get("intent_lock") or {}).get("open_dimensions") or [])
    ordinary = {str(row.get("id") or ""): row for payload in (pack.get("slots") or {}).values()
                for row in payload.get("candidates") or [] if isinstance(row, dict)}
    bundle_rows = bundles.get("candidates") or []
    bundle_ids = [str(row.get("id") or "") for row in bundle_rows if isinstance(row, dict)]
    if len(bundle_ids) != len(bundle_rows) or len(bundle_ids) != len(set(bundle_ids)):
        fail("", "candidate bundles require unique object IDs")
    for bundle in bundle_rows:
        if not isinstance(bundle, dict):
            continue
        candidate_id = str(bundle.get("id") or "")
        if (bundle.get("source_contract_sha256") != photo_candidate_semantics.digest(photo_candidate_semantics.bundle_source_material(bundle))
                or bundle.get("adoption") != "optional"
                or bundle.get("profile_activation") != "independent_request_evidence_only"
                or (bundle.get("selection_contract") or {}).get("associated_profiles_are_not_promoted") is not True):
            fail(candidate_id, "bundle source contract changed or associated profiles acquired automatic authority")
        members = bundle.get("member_candidates") or []
        member_ids = {str(member.get("id") or "") for member in members if isinstance(member, dict)}
        dimensions = {dimension for member in members if isinstance(member, dict) for dimension in member.get("affected_dimensions") or []}
        joint_admission = bundle.get("joint_admission")
        if (len(member_ids) != len(members) or not member_ids
                or any(not member.get("affected_dimensions") for member in members)
                or dimensions != set(bundle.get("affected_dimensions") or [])
                or not dimensions.issubset(open_dimensions)
                or (not joint_admission and (not member_ids.issubset(ordinary) or any((ordinary.get(member_id, {}).get("applicability") or {}).get("status") != "eligible" for member_id in member_ids)))
                or any(member_ids.intersection(ordinary.get(member_id, {}).get("conflicts_with") or []) for member_id in member_ids)):
            fail(candidate_id, "all bundle members must remain individually eligible, conflict-free and scoped to open dimensions")
        components = bundle.get("components") or []
        component_ids = [str(component.get("id") or "") for component in components if isinstance(component, dict)]
        if (not components or len(component_ids) != len(components) or len(component_ids) != len(set(component_ids))
                or any(not component.get("concept_units") or component.get("minimum_realizations") != 1 for component in components)):
            fail(candidate_id, "bundle component groups must retain every authored alternative group")
        inherited_conflicts = {conflict for member_id in member_ids for conflict in ordinary.get(member_id, {}).get("conflicts_with") or []}
        if inherited_conflicts != set(bundle.get("conflicts_with") or []):
            fail(candidate_id, "bundle must preserve every member conflict")
        if candidate_id in chosen:
            expanded_chosen = set(chosen)
            for other in bundle_rows:
                if isinstance(other, dict) and other.get("id") in chosen:
                    expanded_chosen.update(member["id"] for member in other.get("member_candidates") or [])
            if inherited_conflicts.intersection(expanded_chosen):
                fail(candidate_id, "selected bundle conflicts with another selected candidate or bundle member")

    by_id = {str(row.get("candidate_id") or ""): row for row in interpretations}
    for candidate_id, candidate in candidates.items():
        if candidate.get("semantic_surface_version") != photo_candidate_semantics.SURFACE_VERSION:
            continue
        if not candidate.get("concept_units") or candidate.get("concept_terms") != candidate.get("concept_units") or candidate.get("adoption") != "optional":
            fail(candidate_id, "semantic-unit candidates must preserve their unordered authored units and optional adoption")
        relations = candidate.get("relations") or []
        relation_ids = [str(relation.get("id") or "") for relation in relations if isinstance(relation, dict)]
        if (len(relation_ids) != len(relations) or len(relation_ids) != len(set(relation_ids))
                or any(not all(str(relation.get(key) or "").strip() for key in ("id", "type", "subject", "object")) for relation in relations)):
            fail(candidate_id, "candidate relations require unique IDs and explicit direction, subject and object")
        if candidate_id not in chosen:
            continue
        interpretation = by_id.get(candidate_id, {})
        for field, expected_ids in (
            ("component_evidence", {str(component["id"]) for component in candidate.get("components") or []}),
            ("relation_evidence", set(relation_ids)),
        ):
            evidence = interpretation.get(field)
            if not expected_ids and evidence is None:
                continue
            if (not isinstance(evidence, dict) or set(evidence) != expected_ids
                    or any(not isinstance(value, str) or not value.strip() or not text_contains_term(prompt_en, value)
                           for value in evidence.values())):
                fail(candidate_id, f"{field} must cover the entire selected contract with literal final-prompt phrases")
    return failures


def audit_candidate_interpretations(
    pack: dict[str, Any],
    composed: dict[str, Any],
    prompt_en: str,
    chosen: set[str],
    candidate_objects: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Require authorship evidence for every ordinary v4 candidate choice."""

    contract_version = str(pack.get("contract_version") or "")
    if contract_version not in {
        "photo-candidate-pack/v4",
        "photo-candidate-pack/v5",
        "photo-candidate-pack/v6",
    }:
        return []
    brief_field = (
        "creative_augmentation_brief"
        if contract_version in {"photo-candidate-pack/v5", "photo-candidate-pack/v6"}
        else "augmentation_brief"
    )
    augmentation_brief = (
        composed.get(brief_field)
        if isinstance(composed.get(brief_field), dict)
        else {}
    )
    transformed_augmentation_ids = {
        str(row.get("candidate_id") or "")
        for row in augmentation_brief.get("decisions") or []
        if isinstance(row, dict)
        and str(row.get("decision") or "") == "transformed"
        and str(row.get("candidate_id") or "")
    }
    required_ids = chosen - transformed_augmentation_ids
    rows = [
        row
        for row in composed.get("candidate_interpretations") or []
        if isinstance(row, dict)
    ]
    row_ids = [str(row.get("candidate_id") or "") for row in rows]
    failures: list[dict[str, Any]] = []
    semantic_evidence_rows = rows + [row for row in augmentation_brief.get("decisions") or []
                                     if isinstance(row, dict) and row.get("decision") == "transformed"]
    failures.extend(audit_candidate_semantic_contracts(pack, prompt_en, chosen, candidate_objects, semantic_evidence_rows))
    if len(row_ids) != len(set(row_ids)):
        failures.append(
            {
                "check": "candidate_interpretations",
                "reason": "each chosen candidate may have only one authorial interpretation",
            }
        )
    missing = sorted(required_ids - set(row_ids))
    unexpected = sorted(set(row_ids) - required_ids)
    if missing or unexpected:
        failures.append(
            {
                "check": "candidate_interpretations",
                "reason": (
                    "candidate_interpretations must cover every non-augmentation chosen candidate "
                    "exactly once and no others"
                ),
                "missing": missing,
                "unexpected": unexpected,
            }
        )

    for row in rows:
        candidate_id = str(row.get("candidate_id") or "")
        if candidate_id not in required_ids:
            continue
        interpretation = str(row.get("artistic_interpretation") or "").strip()
        transformation = str(row.get("transformation") or "").strip()
        evidence = str(row.get("prompt_evidence") or "").strip()
        if (
            len(authorial_evidence_tokens(interpretation)) < 3
            or len(authorial_evidence_tokens(transformation)) < 3
            or not evidence
            or not text_contains_term(prompt_en, evidence)
        ):
            failures.append(
                {
                    "check": "candidate_interpretation_authorship",
                    "reason": (
                        "each chosen candidate needs substantive artistic interpretation, transformation, "
                        "and literal prompt evidence"
                    ),
                    "candidate_id": candidate_id,
                }
            )
            continue
        candidate = candidate_objects.get(candidate_id, {})
        source_terms = {
            token
            for item in candidate.get("concept_terms") or []
            for token in authorial_evidence_tokens(str(item))
        }
        evidence_terms = authorial_evidence_tokens(evidence)
        new_terms = evidence_terms - source_terms
        if len(evidence_terms) < 4 or len(new_terms) < 2:
            failures.append(
                {
                    "check": "candidate_interpretation_authorship",
                    "reason": (
                        "prompt evidence must add at least two authored content words beyond the "
                        "candidate's unordered source terms"
                    ),
                    "candidate_id": candidate_id,
                    "source_terms": sorted(source_terms),
                }
            )
    return failures


def authorial_core_active_span_texts(core: dict[str, Any]) -> list[str]:
    binding = (
        core.get("request_binding")
        if isinstance(core.get("request_binding"), dict)
        else {}
    )
    return [
        str(item.get("text") or "")
        for item in binding.get("active_spans") or []
        if isinstance(item, dict) and str(item.get("text") or "")
    ]


def authorial_core_active_scope_contains(core: dict[str, Any], text: str) -> bool:
    needle = str(text or "").strip().casefold()
    return bool(needle) and any(
        needle in source.casefold() for source in authorial_core_active_span_texts(core)
    )


def authorial_core_v2_intent_contract_valid(
    core: dict[str, Any], *, minimum_open_dimensions: int = 2
) -> bool:
    if core.get("contract_version") not in AUTHORIAL_CORE_MODERN_CONTRACT_VERSIONS:
        return True
    source_request = core.get("source_request")
    binding = core.get("request_binding")
    if not isinstance(source_request, str) or not source_request or not isinstance(binding, dict):
        return False
    if set(binding) != {
        "contract_version",
        "request_id",
        "request_sha256",
        "request_envelope_sha256",
        "active_spans",
    } or binding.get("contract_version") != REQUEST_BINDING_CONTRACT_VERSION:
        return False
    if re.fullmatch(
        r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}",
        str(binding.get("request_id") or ""),
    ) is None:
        return False
    if binding.get("request_sha256") != hashlib.sha256(
        source_request.encode("utf-8")
    ).hexdigest():
        return False
    if re.fullmatch(
        r"[0-9a-f]{64}", str(binding.get("request_envelope_sha256") or "")
    ) is None:
        return False
    spans = binding.get("active_spans")
    if not isinstance(spans, list) or not 1 <= len(spans) <= 16:
        return False
    previous_end = -1
    seen_ids: set[str] = set()
    seen_texts: set[str] = set()
    for item in spans:
        if not isinstance(item, dict) or set(item) != {"span_id", "start", "end", "text"}:
            return False
        span_id = str(item.get("span_id") or "")
        start = item.get("start")
        end = item.get("end")
        text = item.get("text")
        if (
            re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", span_id) is None
            or span_id in seen_ids
            or isinstance(start, bool)
            or isinstance(end, bool)
            or not isinstance(start, int)
            or not isinstance(end, int)
            or start < 0
            or end <= start
            or start < previous_end
            or end > len(source_request)
            or not isinstance(text, str)
            or source_request[start:end] != text
            or text.casefold() in seen_texts
        ):
            return False
        seen_ids.add(span_id)
        seen_texts.add(text.casefold())
        previous_end = end
    reconstructed_envelope = {
        "contract_version": REQUEST_ENVELOPE_CONTRACT_VERSION,
        "provenance": "requesting_user",
        "request_id": str(binding.get("request_id") or ""),
        "request_text": source_request,
        "request_sha256": str(binding.get("request_sha256") or ""),
        "active_spans": spans,
    }
    if binding.get("request_envelope_sha256") != canonical_json_sha256(
        reconstructed_envelope
    ):
        return False

    intent_lock = core.get("intent_lock")
    if not isinstance(intent_lock, dict):
        return False
    if set(intent_lock) != {
        "contract_version",
        "priority",
        "semantic_anchors",
        "locked_dimensions",
        "open_dimensions",
        "augmentation_policy",
        "material_change_policy",
        "candidate_revision_policy",
        "canonical_sha256",
        "lock_id",
    }:
        return False
    lock_material = copy.deepcopy(intent_lock)
    lock_sha = str(lock_material.pop("canonical_sha256", "") or "")
    lock_id = str(lock_material.pop("lock_id", "") or "")
    allowed_dimensions = (
        AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS
        if core.get("contract_version") == AUTHORIAL_CORE_V3_CONTRACT_VERSION
        else INTENT_LOCK_DIMENSIONS
    )
    if (
        intent_lock.get("contract_version") != INTENT_LOCK_CONTRACT_VERSION
        or intent_lock.get("priority") != "requesting_user"
        or intent_lock.get("augmentation_policy")
        != "open_dimensions_only_and_subordinate"
        or intent_lock.get("material_change_policy")
        != "rebuild_core_after_requester_input"
        or intent_lock.get("candidate_revision_policy") != "forbidden"
        or lock_sha != canonical_json_sha256(lock_material)
        or lock_id != lock_sha[:16]
    ):
        return False
    locked = intent_lock.get("locked_dimensions")
    opened = intent_lock.get("open_dimensions")
    if (
        not isinstance(locked, list)
        or not locked
        or len(locked) != len(set(str(item) for item in locked))
        or not isinstance(opened, list)
        or len(opened) < minimum_open_dimensions
        or len(opened) != len(set(str(item) for item in opened))
        or set(str(item) for item in locked) & set(str(item) for item in opened)
        or not REQUIRED_INTENT_LOCK_DIMENSIONS <= {str(item) for item in locked}
        or (set(str(item) for item in locked) | set(str(item) for item in opened))
        - allowed_dimensions
    ):
        return False
    anchors = intent_lock.get("semantic_anchors")
    if not isinstance(anchors, list) or not 1 <= len(anchors) <= 16:
        return False
    baseline = str(core.get("baseline_prompt_en") or "")
    seen_anchor_ids: set[str] = set()
    seen_anchor_evidence: set[str] = set()
    for item in anchors:
        if not isinstance(item, dict) or set(item) != {
            "anchor_id",
            "source_text",
            "dimension",
            "prompt_evidence",
        }:
            return False
        anchor_id = str(item.get("anchor_id") or "")
        source_text = str(item.get("source_text") or "")
        dimension = str(item.get("dimension") or "")
        evidence = str(item.get("prompt_evidence") or "")
        if (
            re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", anchor_id) is None
            or anchor_id in seen_anchor_ids
            or dimension not in locked
            or len(authorial_general_content_words(source_text)) < 1
            or not authorial_core_active_scope_contains(core, source_text)
            or len(authorial_evidence_tokens(evidence)) < 2
            or not text_contains_term(baseline, evidence)
            or evidence.casefold() in seen_anchor_evidence
        ):
            return False
        seen_anchor_ids.add(anchor_id)
        seen_anchor_evidence.add(evidence.casefold())
    if {str(item.get("dimension") or "") for item in anchors} != {
        str(item) for item in locked
    }:
        return False
    if any(
        not any(
            str(anchor.get("source_text") or "").casefold()
            in str(span_text).casefold()
            for anchor in anchors
        )
        for span_text in authorial_core_active_span_texts(core)
    ):
        return False
    definitions = core.get("user_definitions")
    if not isinstance(definitions, list) or len(definitions) > 8:
        return False
    seen_definition_terms: set[str] = set()
    for item in definitions:
        if not isinstance(item, dict) or set(item) != {
            "term",
            "source_text",
            "interpreted_meaning",
            "prompt_evidence",
        }:
            return False
        term = str(item.get("term") or "").strip()
        source_text = str(item.get("source_text") or "").strip()
        evidence = str(item.get("prompt_evidence") or "").strip()
        if (
            not term
            or term.casefold() in seen_definition_terms
            or source_text.casefold()
            not in {
                span.casefold() for span in authorial_core_active_span_texts(core)
            }
            or source_text.casefold() == term.casefold()
            or len(authorial_general_content_words(str(item.get("interpreted_meaning") or ""))) < 4
            or len(authorial_evidence_tokens(evidence)) < 4
            or not text_contains_term(baseline, evidence)
        ):
            return False
        seen_definition_terms.add(term.casefold())
    runtime_labels = nonempty_string_list(core.get("runtime_forbidden_labels"))
    if len(runtime_labels) > 12 or len(runtime_labels) != len(
        {item.casefold() for item in runtime_labels}
    ):
        return False
    if any(
        not authorial_core_active_scope_contains(core, label)
        or text_contains_term(baseline, label)
        for label in runtime_labels
    ):
        return False
    exclusions = nonempty_string_list(core.get("user_exclusions"))
    if any(
        not authorial_core_active_scope_contains(core, exclusion)
        for exclusion in exclusions
    ):
        return False
    if {item.casefold() for item in runtime_labels} & {
        item.casefold() for item in exclusions
    }:
        return False
    return True


def authorial_core_v3_semantic_contract_valid(core: dict[str, Any]) -> bool:
    if core.get("contract_version") != AUTHORIAL_CORE_V3_CONTRACT_VERSION:
        return True
    assertions = core.get("semantic_assertions")
    intent_lock = (
        core.get("intent_lock")
        if isinstance(core.get("intent_lock"), dict)
        else {}
    )
    binding = (
        core.get("request_binding")
        if isinstance(core.get("request_binding"), dict)
        else {}
    )
    if not isinstance(assertions, list) or len(assertions) > 16:
        return False
    span_ids = {
        str(item.get("span_id") or "")
        for item in binding.get("active_spans") or []
        if isinstance(item, dict)
    }
    locked = {str(value) for value in intent_lock.get("locked_dimensions") or []}
    opened = {str(value) for value in intent_lock.get("open_dimensions") or []}
    baseline = str(core.get("baseline_prompt_en") or "")
    seen_ids: set[str] = set()
    required_character_count = 0

    def valid_character_relation(relation: Any) -> bool:
        if not isinstance(relation, dict):
            return False
        operator = str(relation.get("operator") or "")
        identifier = r"[a-z][a-z0-9_]{0,63}"
        if operator == "same_target" and set(relation) == {
            "operator",
            "members",
        }:
            members = nonempty_string_list(relation.get("members"))
            return bool(
                2 <= len(members) <= 8
                and len(members) == len(set(members))
                and "relationship_target" in members
                and set(members) <= CHARACTER_RESPONSE_RELATION_MEMBERS
                and all(re.fullmatch(identifier, value) for value in members)
            )
        if operator == "contrasts" and set(relation) == {
            "operator",
            "left",
            "right",
        }:
            left = str(relation.get("left") or "")
            right = str(relation.get("right") or "")
            return bool(
                left != right
                and {left, right} <= CHARACTER_RESPONSE_RELATION_MEMBERS
                and re.fullmatch(identifier, left)
                and re.fullmatch(identifier, right)
            )
        if operator == "temporal_order" and set(relation) == {
            "operator",
            "first",
            "then",
        }:
            first = str(relation.get("first") or "")
            then = str(relation.get("then") or "")
            return bool(
                first != then
                and {first, then} <= CHARACTER_RESPONSE_RELATION_MEMBERS
                and re.fullmatch(identifier, first)
                and re.fullmatch(identifier, then)
            )
        return False

    def character_relation_signature(relation: dict[str, Any]) -> tuple[Any, ...]:
        operator = str(relation.get("operator") or "")
        if operator == "same_target":
            return operator, tuple(sorted(nonempty_string_list(relation.get("members"))))
        if operator == "contrasts":
            return operator, str(relation.get("left") or ""), str(
                relation.get("right") or ""
            )
        return operator, str(relation.get("first") or ""), str(
            relation.get("then") or ""
        )

    def valid_character_relations(relations: Any) -> bool:
        if not isinstance(relations, list) or not 1 <= len(relations) <= 8:
            return False
        signatures: set[tuple[Any, ...]] = set()
        for relation in relations:
            if not valid_character_relation(relation):
                return False
            signature = character_relation_signature(relation)
            if signature in signatures:
                return False
            signatures.add(signature)
        return True

    for item in assertions:
        required_fields = {
            "assertion_id",
            "dimension",
            "polarity",
            "source_span_ids",
            "axes",
            "evidence",
            "affected_dimensions",
        }
        if not isinstance(item, dict) or frozenset(item) not in {
            frozenset(required_fields),
            frozenset(required_fields | {"relations"}),
        }:
            return False
        assertion_id = str(item.get("assertion_id") or "")
        dimension = str(item.get("dimension") or "")
        polarity = str(item.get("polarity") or "")
        source_span_ids = nonempty_string_list(item.get("source_span_ids"))
        affected = nonempty_string_list(item.get("affected_dimensions"))
        axes = item.get("axes") if isinstance(item.get("axes"), dict) else {}
        evidence = (
            item.get("evidence") if isinstance(item.get("evidence"), dict) else {}
        )
        relations = item.get("relations") if "relations" in item else None
        if (
            re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", assertion_id)
            is None
            or assertion_id in seen_ids
            or dimension not in AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS
            or polarity not in {"required", "advisory", "excluded"}
            or not source_span_ids
            or len(source_span_ids) != len(set(source_span_ids))
            or not set(source_span_ids) <= span_ids
            or not affected
            or len(affected) != len(set(affected))
            or not set(affected) <= AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS
            or (polarity == "required" and not set(affected) <= locked)
            or (polarity == "advisory" and not set(affected) <= opened)
            or not 1 <= len(axes) <= 16
            or len(evidence) > 16
            or (
                relations is not None
                and (
                    dimension != "character_response"
                    or not valid_character_relations(relations)
                )
            )
        ):
            return False
        seen_ids.add(assertion_id)
        if any(
            re.fullmatch(r"[a-z][a-z0-9_]{0,63}", str(key)) is None
            or not (
                isinstance(value, str)
                and bool(value.strip())
                or isinstance(value, list)
                and 1 <= len(value) <= 8
                and all(isinstance(part, str) and part.strip() for part in value)
                and len(value) == len(set(value))
            )
            for key, value in axes.items()
        ):
            return False
        if any(
            re.fullmatch(r"[a-z][a-z0-9_]{0,63}", str(key)) is None
            or not isinstance(value, str)
            or len(authorial_evidence_tokens(value)) < 2
            or not text_contains_term(baseline, value)
            for key, value in evidence.items()
        ):
            return False
        if polarity == "required" and not evidence:
            return False
        if dimension == "character_response" and polarity == "required":
            required_character_count += 1
            channels = axes.get("affect_leak_channels")
            if (
                not CHARACTER_RESPONSE_REQUIRED_AXES <= set(axes)
                or not CHARACTER_RESPONSE_REQUIRED_EVIDENCE <= set(evidence)
                or not isinstance(channels, list)
                or len(channels) != 1
            ):
                return False
    if required_character_count > 1:
        return False

    lineage = core.get("request_lineage")
    if lineage is None:
        return True
    if not isinstance(lineage, dict):
        return False
    preserved = nonempty_string_list(lineage.get("preserved_dimensions"))
    allowed = nonempty_string_list(lineage.get("allowed_changes"))
    base_valid = bool(
        re.fullmatch(
            r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}",
            str(lineage.get("parent_request_id") or ""),
        )
        and str(lineage.get("parent_request_id") or "")
        != str(binding.get("request_id") or "")
        and re.fullmatch(
            r"[0-9a-f]{64}", str(lineage.get("parent_core_sha256") or "")
        )
        and preserved
        and allowed
        and len(preserved) == len(set(preserved))
        and len(allowed) == len(set(allowed))
        and set(preserved) <= AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS
        and set(allowed) <= AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS
        and not set(preserved) & set(allowed)
    )
    if not base_valid:
        return False
    legacy_fields = {
        "parent_request_id",
        "parent_core_sha256",
        "preserved_dimensions",
        "allowed_changes",
    }
    contract_version = str(lineage.get("contract_version") or "")
    if not contract_version:
        return set(lineage) == legacy_fields
    if contract_version != REQUEST_LINEAGE_V2_CONTRACT_VERSION or set(
        lineage
    ) != legacy_fields | {
        "contract_version",
        "repair_targets",
        "canonical_sha256",
    }:
        return False
    canonical_sha = str(lineage.get("canonical_sha256") or "")
    canonical_payload = {
        key: copy.deepcopy(value)
        for key, value in lineage.items()
        if key != "canonical_sha256"
    }
    if (
        re.fullmatch(r"[0-9a-f]{64}", canonical_sha) is None
        or canonical_json_sha256(canonical_payload) != canonical_sha
    ):
        return False
    targets = lineage.get("repair_targets")
    if not isinstance(targets, list) or not 1 <= len(targets) <= 8:
        return False
    seen_repair_ids: set[str] = set()
    expected_target_fields = {
        "repair_id",
        "source_span_ids",
        "importance",
        "relation_origin",
        "actor_phrase",
        "object_phrase",
        "interaction_state",
        "actor_object_contact",
        "protected_dimensions",
        "allowed_repair_axes",
        "interaction_phrase",
        "recognition_phrase",
    }
    required_action_assertions = [
        item
        for item in assertions
        if isinstance(item, dict)
        and item.get("polarity") == "required"
        and "action" in set(item.get("affected_dimensions") or [])
    ]
    for target in targets:
        if not isinstance(target, dict) or set(target) != expected_target_fields:
            return False
        repair_id = str(target.get("repair_id") or "")
        source_span_ids = nonempty_string_list(target.get("source_span_ids"))
        importance = str(target.get("importance") or "")
        relation_origin = str(target.get("relation_origin") or "")
        interaction_state = str(target.get("interaction_state") or "")
        actor_object_contact = str(target.get("actor_object_contact") or "")
        protected = nonempty_string_list(target.get("protected_dimensions"))
        repair_axes = nonempty_string_list(target.get("allowed_repair_axes"))
        actor_phrase = re.sub(r"\s+", " ", str(target.get("actor_phrase") or "")).strip()
        object_phrase = re.sub(r"\s+", " ", str(target.get("object_phrase") or "")).strip()
        interaction_phrase = re.sub(
            r"\s+", " ", str(target.get("interaction_phrase") or "")
        ).strip()
        recognition_phrase = re.sub(
            r"\s+", " ", str(target.get("recognition_phrase") or "")
        ).strip()
        origin_dimensions = preserved if relation_origin == "parent_preserved" else allowed
        if (
            re.fullmatch(r"[a-z][a-z0-9_]{0,63}", repair_id) is None
            or repair_id in seen_repair_ids
            or not source_span_ids
            or len(source_span_ids) != len(set(source_span_ids))
            or not set(source_span_ids) <= span_ids
            or importance not in RENDER_REPAIR_IMPORTANCE_VALUES
            or relation_origin not in RENDER_REPAIR_RELATION_ORIGINS
            or interaction_state not in RENDER_REPAIR_INTERACTION_STATES
            or actor_object_contact not in RENDER_REPAIR_CONTACT_EXPECTATIONS
            or (
                interaction_state
                in {"held", "wielded", "used", "handed_off", "carried", "worn"}
                and actor_object_contact == "absent"
            )
            or not protected
            or len(protected) != len(set(protected))
            or "action" not in protected
            or not set(protected) <= locked
            or not set(protected) <= set(origin_dimensions)
            or not repair_axes
            or len(repair_axes) != len(set(repair_axes))
            or not set(repair_axes) <= RENDER_REPAIR_ALLOWED_AXES
            or any(
                axis in repair_axes and dimension not in allowed
                for axis, dimension in RENDER_REPAIR_DIMENSION_AXES.items()
            )
            or len(authorial_evidence_tokens(actor_phrase)) < 1
            or len(authorial_evidence_tokens(object_phrase)) < 1
            or len(authorial_evidence_tokens(interaction_phrase)) < 4
            or len(authorial_evidence_tokens(recognition_phrase)) < 4
            or not text_contains_term(baseline, actor_phrase)
            or not text_contains_term(baseline, object_phrase)
            or not text_contains_term(baseline, interaction_phrase)
            or not text_contains_term(baseline, recognition_phrase)
            or interaction_phrase.casefold() == recognition_phrase.casefold()
            or not text_contains_term(interaction_phrase, actor_phrase)
            or not text_contains_term(interaction_phrase, object_phrase)
            or not text_contains_term(recognition_phrase, object_phrase)
        ):
            return False
        evidence_pair = {
            interaction_phrase.casefold(),
            recognition_phrase.casefold(),
        }
        if not any(
            evidence_pair
            <= {
                str(value).casefold()
                for value in (assertion.get("evidence") or {}).values()
                if str(value).strip()
            }
            for assertion in required_action_assertions
        ):
            return False
        seen_repair_ids.add(repair_id)
    return True


def expected_authorial_core_retrieval_provenance(
    core: dict[str, Any],
) -> dict[str, Any]:
    exclusions = [
        re.sub(r"\s+", " ", str(item)).strip()
        for item in core.get("user_exclusions") or []
        if re.sub(r"\s+", " ", str(item)).strip()
    ]
    fields: list[tuple[str, str]] = []
    redacted_fields: set[str] = set()

    def clean(value: Any) -> str:
        text = re.sub(r"\s+", " ", str(value or "")).strip()
        text = re.sub(r"\s+([,.!?;:])", r"\1", text)
        return re.sub(r"([.!?]){2,}", r"\1", text)

    def add(field: str, value: Any) -> None:
        text = clean(value)
        for exclusion in exclusions:
            if exclusion.isascii() and re.search(r"[A-Za-z0-9]", exclusion):
                pattern = (
                    r"(?<![A-Za-z0-9])"
                    + re.escape(exclusion)
                    + r"(?![A-Za-z0-9])"
                )
                updated = re.sub(pattern, " ", text, flags=re.IGNORECASE)
            else:
                updated = re.sub(
                    re.escape(exclusion),
                    " ",
                    text,
                    flags=re.IGNORECASE,
                )
            if updated != text:
                redacted_fields.add(field)
            text = updated
        text = clean(re.sub(r"(?:\s*[,;:/|]\s*){2,}", " ", text).strip(" ,;:/|"))
        if text:
            fields.append((field, text))

    if core.get("contract_version") in AUTHORIAL_CORE_MODERN_CONTRACT_VERSIONS:
        for value in authorial_core_active_span_texts(core):
            add("source_request_scope", value)
    else:
        add("source_request", core.get("source_request"))
    add("interpreted_intent", core.get("interpreted_intent"))
    add("subject", core.get("subject"))
    add("setting", core.get("setting"))
    add("event", core.get("event"))
    for value in core.get("visual_priorities") or []:
        add("visual_priority", value)
    add("baseline_prompt_en", core.get("baseline_prompt_en"))
    for definition in core.get("user_definitions") or []:
        if isinstance(definition, dict):
            add("user_definition_meaning", definition.get("interpreted_meaning"))
            add("user_definition_prompt_evidence", definition.get("prompt_evidence"))
    for interpretation in core.get("interpretation_provenance") or []:
        if isinstance(interpretation, dict):
            add("interpretation_resolution", interpretation.get("resolution"))
    style = core.get("style") if isinstance(core.get("style"), dict) else {}
    add("style_domain", style.get("domain"))
    add("style_family", style.get("family"))
    for value in style.get("evidence") or []:
        add("style_evidence", value)

    deduped: list[tuple[str, str]] = []
    seen: set[str] = set()
    for field, value in fields:
        key = value.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append((field, value))
    query = " | ".join(value for _, value in deduped)
    provenance: dict[str, Any] = {
        "contract_version": (
            "photo-retrieval-query-provenance/v2"
            if core.get("contract_version") in AUTHORIAL_CORE_MODERN_CONTRACT_VERSIONS
            else "photo-retrieval-query-provenance/v1"
        ),
        "source_authorial_core_sha256": str(core.get("canonical_sha256") or ""),
        "source_request_sha256": hashlib.sha256(
            str(core.get("source_request") or "").encode("utf-8")
        ).hexdigest(),
        "source_fields": [field for field, _ in deduped],
        "query_sha256": hashlib.sha256(query.encode("utf-8")).hexdigest(),
        "redacted_source_fields": sorted(redacted_fields),
        "excluded_term_count": len(exclusions),
        "exclusions_used_as_positive_query": False,
    }
    if core.get("contract_version") in AUTHORIAL_CORE_MODERN_CONTRACT_VERSIONS:
        binding = (
            core.get("request_binding")
            if isinstance(core.get("request_binding"), dict)
            else {}
        )
        intent_lock = (
            core.get("intent_lock")
            if isinstance(core.get("intent_lock"), dict)
            else {}
        )
        active_spans = [
            item
            for item in binding.get("active_spans") or []
            if isinstance(item, dict) and str(item.get("text") or "")
        ]
        provenance.update(
            {
                "request_envelope_sha256": str(
                    binding.get("request_envelope_sha256") or ""
                ),
                "active_scope_sha256": canonical_json_sha256(active_spans),
                "source_intent_lock_sha256": str(
                    intent_lock.get("canonical_sha256") or ""
                ),
                "runtime_forbidden_label_count": len(
                    core.get("runtime_forbidden_labels") or []
                ),
            }
        )
    return provenance


def authorial_core_interpretation_contract_valid(core: dict[str, Any]) -> bool:
    if core.get("contract_version") not in {
        LEGACY_AUTHORIAL_CORE_CONTRACT_VERSION,
        AUTHORIAL_CORE_CONTRACT_VERSION,
        AUTHORIAL_CORE_V3_CONTRACT_VERSION,
    }:
        return False
    if "interpretation_provenance" not in core or "unresolved_ambiguities" not in core:
        return False
    if core.get("unresolved_ambiguities") != []:
        return False
    interpretations = core.get("interpretation_provenance")
    if not isinstance(interpretations, list) or len(interpretations) > 8:
        return False
    user_terms = {
        str(item.get("term") or "").strip().casefold()
        for item in core.get("user_definitions") or []
        if isinstance(item, dict) and str(item.get("term") or "").strip()
    }
    source_request = str(core.get("source_request") or "").casefold()
    seen_terms: set[str] = set()
    allowed_bases = {
        "agent_general_knowledge",
        "request_context",
        "public_web_research",
    }
    for item in interpretations:
        if not isinstance(item, dict) or set(item) != {
            "term",
            "source_text",
            "basis",
            "resolution",
            "sources",
        }:
            return False
        term = str(item.get("term") or "").strip()
        source_text = str(item.get("source_text") or "").strip()
        basis = str(item.get("basis") or "").strip()
        resolution = str(item.get("resolution") or "").strip()
        sources = item.get("sources")
        key = term.casefold()
        if (
            not term
            or not source_text
            or key in seen_terms
            or key in user_terms
            or source_text.casefold() not in source_request
            or (
                core.get("contract_version") in AUTHORIAL_CORE_MODERN_CONTRACT_VERSIONS
                and not authorial_core_active_scope_contains(core, source_text)
            )
            or basis not in allowed_bases
            or len(authorial_general_content_words(resolution)) < 4
            or not isinstance(sources, list)
            or len(sources) > 4
            or len(sources) != len(set(str(value) for value in sources))
        ):
            return False
        seen_terms.add(key)
        if basis == "public_web_research":
            if not sources or any(
                re.fullmatch(r"https?://[^\s]+", str(value), flags=re.IGNORECASE)
                is None
                for value in sources
            ):
                return False
        elif sources:
            return False
    if core.get("contract_version") in AUTHORIAL_CORE_MODERN_CONTRACT_VERSIONS:
        semantic_source_texts = [
            str(item.get("source_text") or "")
            for item in [
                *(core.get("user_definitions") or []),
                *interpretations,
            ]
            if isinstance(item, dict) and str(item.get("source_text") or "")
        ]
        if any(
            not any(
                source.casefold() in span.casefold()
                for source in semantic_source_texts
            )
            for span in authorial_core_active_span_texts(core)
        ):
            return False
    return True


def audit_authorial_authorship_policy(
    pack: dict[str, Any],
) -> tuple[list[dict[str, Any]], int, int]:
    """Recompute the optional v6 policy; unmarked replay keeps the old minimum.

    The serialized minimum is never trusted. Both policy and binding blocks
    must equal independent derivations from the frozen core before 0/1 open
    dimensions or decisions are accepted.
    """

    authorial = pack.get("authorial_composition")
    authorial = authorial if isinstance(authorial, dict) else {}
    binding = authorial.get("core_binding_contract")
    binding = binding if isinstance(binding, dict) else {}
    marked = (
        "authorship_policy" in authorial
        or "contract_version" in binding
        or "source_authorship_policy_sha256" in binding
    )
    if not marked:
        return [], 2, 2

    core = pack.get("authorial_core")
    core = core if isinstance(core, dict) else {}
    intent_lock = core.get("intent_lock")
    intent_lock = intent_lock if isinstance(intent_lock, dict) else {}
    opened = intent_lock.get("open_dimensions")
    opened = opened if isinstance(opened, list) else []
    minimum_decisions = min(2, len(opened))
    expected_policy = {
        "contract_version": AUTHORIAL_AUTHORSHIP_POLICY_CONTRACT_VERSION,
        "source_authorial_core_sha256": str(core.get("canonical_sha256") or ""),
        "source_intent_lock_sha256": str(intent_lock.get("canonical_sha256") or ""),
        "allowed_dimensions": copy.deepcopy(opened),
        "minimum_authorial_decisions": minimum_decisions,
        "minimum_preserved_evidence_phrases": 3,
        "dimension_policy": "distinct_open_dimensions_only",
        "insufficient_freedom_policy": "do_not_invent_open_dimensions",
    }
    expected_policy["canonical_sha256"] = canonical_json_sha256(expected_policy)
    expected_binding = {
        "composed_field": "authorial_core_binding",
        "minimum_preserved_evidence_phrases": 3,
        "minimum_authorial_decisions": minimum_decisions,
        "evidence_must_be_literal_in_baseline_and_final_prompt": True,
        "source_intent_lock_sha256_required": True,
        "all_semantic_anchor_ids_required": True,
        "authorial_decisions_limited_to_open_dimensions": True,
        "contract_version": AUTHORIAL_CORE_BINDING_CONTRACT_VERSION,
        "source_authorship_policy_sha256": expected_policy["canonical_sha256"],
    }
    if (
        pack.get("contract_version") != "photo-candidate-pack/v6"
        or core.get("contract_version") != AUTHORIAL_CORE_V3_CONTRACT_VERSION
        or authorial.get("authorship_policy") != expected_policy
        or binding != expected_binding
    ):
        return [
            {
                "check": "authorial_authorship_policy_contract",
                "reason": "the v6 authorship policy and core binding must match the frozen open dimensions and hashes",
            }
        ], 2, 2
    return [], minimum_decisions, 0


def audit_authorial_core_v5(
    pack: dict[str, Any],
    composed: dict[str, Any],
    prompt_en: str,
    warnings: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    pack_version = str(pack.get("contract_version") or "")
    failures, minimum_decisions, minimum_open_dimensions = (
        audit_authorial_authorship_policy(pack)
    )
    if pack_version not in {"photo-candidate-pack/v5", "photo-candidate-pack/v6"}:
        return failures
    core = (
        pack.get("authorial_core")
        if isinstance(pack.get("authorial_core"), dict)
        else {}
    )
    authorial_composition = (
        pack.get("authorial_composition")
        if isinstance(pack.get("authorial_composition"), dict)
        else {}
    )
    recorded_budget = (
        authorial_composition.get("prompt_budget")
        if isinstance(authorial_composition.get("prompt_budget"), dict)
        else None
    )
    expected_budget = expected_authorial_prompt_budget_contract()
    legacy_budget = legacy_authorial_prompt_budget_contract()
    uses_current_advisory_budget = recorded_budget == expected_budget
    uses_legacy_advisory_budget = recorded_budget == legacy_budget
    uses_advisory_budget = (
        uses_current_advisory_budget or uses_legacy_advisory_budget
    )
    if recorded_budget is not None and not uses_advisory_budget:
        failures.append(
            {
                "check": "authorial_prompt_budget_contract",
                "reason": "the versioned authorial prompt-budget policy was changed after pack generation",
                "expected": expected_budget,
                "actual": recorded_budget,
            }
        )

    if uses_advisory_budget:
        active_budget = expected_budget if uses_current_advisory_budget else legacy_budget
        minimum_words = int(active_budget["minimum_words"])
        recommended_maximum_words = int(active_budget["recommended_maximum_words"])
        absolute_maximum_words = int(active_budget["absolute_maximum_words"])
        required_evidence_headroom_words = int(
            active_budget["required_evidence_headroom_words"]
        )
        prompt_metrics = authorial_prompt_budget_metrics(
            pack,
            composed,
            prompt_en,
            budget_contract=active_budget,
        )
        prompt_word_count = prompt_metrics["actual_words"]
        if not (
            minimum_words
            <= prompt_word_count
            <= absolute_maximum_words
        ):
            failures.append(
                {
                    "check": "authorial_core_prompt_budget",
                    "reason": "v5/v6 prompt_en exceeds the absolute photographic prompt bounds",
                    "minimum_words": minimum_words,
                    "recommended_maximum_words": recommended_maximum_words,
                    "absolute_maximum_words": absolute_maximum_words,
                    "actual_words": prompt_word_count,
                }
            )
        elif (
            warnings is not None
            and prompt_word_count > recommended_maximum_words
        ):
            warnings.append(
                {
                    "check": "authorial_prompt_recommended_budget",
                    "reason": (
                        "prompt_en exceeds the default concise target; this is advisory because "
                        "requester meaning and literal hard evidence take priority"
                    ),
                    "recommended_maximum_words": recommended_maximum_words,
                    "absolute_maximum_words": absolute_maximum_words,
                    **prompt_metrics,
                }
            )
            if (
                prompt_word_count
                > prompt_metrics["effective_recommended_maximum_words"]
            ):
                warnings.append(
                    {
                        "check": "authorial_prompt_optional_prose_budget",
                        "reason": (
                            "prompt_en exceeds the evidence-adjusted advisory ceiling; trim optional "
                            "candidate, styling, camera, or explanatory prose before hard evidence"
                        ),
                        "required_evidence_headroom_words": required_evidence_headroom_words,
                        "absolute_maximum_words": absolute_maximum_words,
                        **prompt_metrics,
                    }
                )

        baseline_prompt = str(core.get("baseline_prompt_en") or "")
        baseline_metrics = authorial_prompt_budget_metrics(
            pack,
            composed,
            baseline_prompt,
            baseline_only=True,
            budget_contract=active_budget,
        )
        baseline_word_count = baseline_metrics["actual_words"]
        if not (
            minimum_words
            <= baseline_word_count
            <= absolute_maximum_words
        ):
            failures.append(
                {
                    "check": "authorial_core_baseline_prompt_budget",
                    "reason": "baseline_prompt_en exceeds the absolute photographic prompt bounds",
                    "minimum_words": minimum_words,
                    "recommended_maximum_words": recommended_maximum_words,
                    "absolute_maximum_words": absolute_maximum_words,
                    "actual_words": baseline_word_count,
                }
            )
        elif (
            warnings is not None
            and baseline_word_count > recommended_maximum_words
        ):
            warnings.append(
                {
                    "check": "authorial_core_baseline_recommended_budget",
                    "reason": (
                        "baseline_prompt_en exceeds the default concise target but remains within "
                        "the absolute bound"
                    ),
                    "recommended_maximum_words": recommended_maximum_words,
                    "absolute_maximum_words": absolute_maximum_words,
                    **baseline_metrics,
                }
            )
    else:
        prompt_word_count = english_prompt_word_count(prompt_en)
        if not (
            LEGACY_AUTHORIAL_PROMPT_MIN_WORDS
            <= prompt_word_count
            <= LEGACY_AUTHORIAL_PROMPT_RECOMMENDED_MAX_WORDS
        ):
            failures.append(
                {
                    "check": "authorial_core_prompt_budget",
                    "reason": "legacy v5/v6 packs retain their recorded 24 to 180 word hard boundary",
                    "minimum_words": LEGACY_AUTHORIAL_PROMPT_MIN_WORDS,
                    "maximum_words": LEGACY_AUTHORIAL_PROMPT_RECOMMENDED_MAX_WORDS,
                    "actual_words": prompt_word_count,
                }
            )
    canonical_sha = str(core.get("canonical_sha256") or "")
    canonical_material = copy.deepcopy(core)
    canonical_material.pop("canonical_sha256", None)
    canonical_material.pop("core_id", None)
    expected_sha = hashlib.sha256(
        json.dumps(
            canonical_material,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    retrieval = (
        (pack.get("provenance") or {}).get("retrieval_query")
        if isinstance(pack.get("provenance"), dict)
        else {}
    )
    expected_retrieval = expected_authorial_core_retrieval_provenance(core)
    modern_core_fields_valid = True
    if core.get("contract_version") in AUTHORIAL_CORE_MODERN_CONTRACT_VERSIONS:
        expected_core_fields = {
            "contract_version",
            "provenance",
            "source_request",
            "interpreted_intent",
            "subject",
            "setting",
            "event",
            "visual_priorities",
            "baseline_prompt_en",
            "user_definitions",
            "interpretation_provenance",
            "unresolved_ambiguities",
            "user_exclusions",
            "runtime_forbidden_labels",
            "intent_lock",
            "request_binding",
            "style",
            "variation_key",
            "canonical_sha256",
            "core_id",
        }
        if core.get("contract_version") == AUTHORIAL_CORE_V3_CONTRACT_VERSION:
            expected_core_fields.update({"semantic_assertions", "request_lineage"})
        modern_core_fields_valid = set(core) == expected_core_fields
    allowed_core_versions = (
        {AUTHORIAL_CORE_V3_CONTRACT_VERSION}
        if pack_version == "photo-candidate-pack/v6"
        else {
            LEGACY_AUTHORIAL_CORE_CONTRACT_VERSION,
            AUTHORIAL_CORE_CONTRACT_VERSION,
        }
    )
    if (
        core.get("contract_version") not in allowed_core_versions
        or core.get("provenance") != "agent_prepack"
        or not authorial_core_interpretation_contract_valid(core)
        or not authorial_core_v2_intent_contract_valid(
            core, minimum_open_dimensions=minimum_open_dimensions
        )
        or not authorial_core_v3_semantic_contract_valid(core)
        or not modern_core_fields_valid
        or not canonical_sha
        or canonical_sha != expected_sha
        or str(core.get("core_id") or "") != canonical_sha[:16]
        or not isinstance(retrieval, dict)
        or retrieval != expected_retrieval
    ):
        failures.append(
            {
                "check": "authorial_core_integrity",
                "reason": "v5/v6 pack is not bound to one valid versioned pre-pack authorial core and retrieval query",
            }
        )

    binding = (
        composed.get("authorial_core_binding")
        if isinstance(composed.get("authorial_core_binding"), dict)
        else {}
    )
    if str(binding.get("source_authorial_core_sha256") or "") != canonical_sha:
        failures.append(
            {
                "check": "authorial_core_binding",
                "reason": "composed prompt is not bound to the governing authorial core hash",
            }
        )
    intent_lock = (
        core.get("intent_lock")
        if isinstance(core.get("intent_lock"), dict)
        else {}
    )
    intent_locked = core.get("contract_version") in AUTHORIAL_CORE_MODERN_CONTRACT_VERSIONS
    if intent_locked and str(binding.get("source_intent_lock_sha256") or "") != str(
        intent_lock.get("canonical_sha256") or ""
    ):
        failures.append(
            {
                "check": "intent_lock_binding",
                "reason": "composed prompt is not bound to the requesting-user-priority intent lock",
            }
        )
    if intent_locked:
        required_anchor_ids = {
            str(item.get("anchor_id") or "")
            for item in intent_lock.get("semantic_anchors") or []
            if isinstance(item, dict) and str(item.get("anchor_id") or "")
        }
        preserved_anchor_id_list = nonempty_string_list(
            binding.get("preserved_anchor_ids")
        )
        preserved_anchor_ids = set(preserved_anchor_id_list)
        if (
            preserved_anchor_ids != required_anchor_ids
            or len(preserved_anchor_id_list) != len(preserved_anchor_ids)
        ):
            failures.append(
                {
                    "check": "intent_lock_anchor_binding",
                    "reason": "authorial_core_binding must preserve every semantic anchor id exactly once",
                    "expected": sorted(required_anchor_ids),
                    "actual": sorted(preserved_anchor_ids),
                }
            )
        for anchor in intent_lock.get("semantic_anchors") or []:
            if not isinstance(anchor, dict):
                continue
            phrase = str(anchor.get("prompt_evidence") or "")
            if not phrase or not text_contains_term(prompt_en, phrase):
                failures.append(
                    {
                        "check": "intent_lock_prompt_evidence",
                        "reason": "every requesting-user semantic anchor must remain literal in prompt_en",
                        "anchor_id": anchor.get("anchor_id"),
                        "phrase": phrase,
                    }
                )
        preservation = (
            pack.get("intent_preservation")
            if isinstance(pack.get("intent_preservation"), dict)
            else {}
        )
        if (
            set(preservation)
            != {
                "contract_version",
                "source_authorial_core_sha256",
                "source_intent_lock_sha256",
                "priority_order",
                "required_anchor_ids",
                "locked_dimensions",
                "open_dimensions",
                "material_change_action",
                "creative_change_boundary",
            }
            or
            preservation.get("contract_version")
            != INTENT_PRESERVATION_CONTRACT_VERSION
            or preservation.get("source_authorial_core_sha256") != canonical_sha
            or preservation.get("source_intent_lock_sha256")
            != intent_lock.get("canonical_sha256")
            or preservation.get("priority_order")
            != [
                "requesting_user_definition",
                "requesting_user_semantic_anchor",
                "requesting_user_modifier_or_exclusion",
                "agent_prepack_interpretation",
                "creative_augmentation",
            ]
            or set(nonempty_string_list(preservation.get("required_anchor_ids")))
            != required_anchor_ids
            or preservation.get("locked_dimensions")
            != intent_lock.get("locked_dimensions")
            or preservation.get("open_dimensions") != intent_lock.get("open_dimensions")
            or preservation.get("material_change_action")
            != "stop_and_rebuild_core_after_requester_input"
            or preservation.get("creative_change_boundary")
            != "open_dimensions_only_and_subordinate"
        ):
            failures.append(
                {
                    "check": "intent_preservation_contract",
                    "reason": "v5/v6 pack does not preserve the canonical requester-priority intent boundary",
                }
            )
    evidence = nonempty_string_list(binding.get("preserved_evidence"))
    if len(evidence) < 3 or len({item.casefold() for item in evidence}) != len(evidence):
        failures.append(
            {
                "check": "authorial_core_evidence",
                "reason": "authorial_core_binding requires at least three distinct preserved evidence phrases",
            }
        )
    baseline = str(core.get("baseline_prompt_en") or "")
    for phrase in evidence:
        if (
            len(authorial_evidence_tokens(phrase)) < 2
            or not text_contains_term(baseline, phrase)
            or not text_contains_term(prompt_en, phrase)
        ):
            failures.append(
                {
                    "check": "authorial_core_evidence",
                    "reason": (
                        "preserved evidence must be substantive and occur literally in both "
                        "baseline_prompt_en and prompt_en"
                    ),
                    "phrase": phrase,
                }
            )
    raw_decisions = binding.get("authorial_decisions")
    decisions = (
        [row for row in raw_decisions if isinstance(row, dict)]
        if isinstance(raw_decisions, list)
        else []
    )
    dimensions = [str(row.get("dimension") or "") for row in decisions]
    if (
        len(decisions) < minimum_decisions
        or (
            minimum_open_dimensions == 0
            and (
                not isinstance(raw_decisions, list)
                or len(decisions) != len(raw_decisions)
            )
        )
        or len(dimensions) != len(set(dimensions))
        or any(
            len(authorial_evidence_tokens(str(row.get("decision") or ""))) < 2
            or len(authorial_evidence_tokens(str(row.get("rationale") or ""))) < 3
            for row in decisions
        )
    ):
        failures.append(
            {
                "check": "authorial_core_decisions",
                "reason": "composition requires the policy minimum of distinct substantive authorial decisions",
                "minimum_authorial_decisions": minimum_decisions,
            }
        )
    if intent_locked:
        open_dimensions = {
            str(item) for item in intent_lock.get("open_dimensions") or []
        }
        adult_appeal = (
            pack.get("adult_appeal")
            if isinstance(pack.get("adult_appeal"), dict)
            else {}
        )
        if (
            adult_appeal.get("enabled") is True
            and adult_appeal.get("activation_source") == "skill_default"
            and not ADULT_APPEAL_DEFAULT_AFFECTED_DIMENSIONS.issubset(
                open_dimensions
            )
        ):
            failures.append(
                {
                    "check": "intent_lock_adult_appeal_default",
                    "reason": (
                        "the skill-default adult-appeal axis may be active only when every semantic dimension it can affect is explicitly open"
                    ),
                    "required_open_dimensions": sorted(
                        ADULT_APPEAL_DEFAULT_AFFECTED_DIMENSIONS
                    ),
                    "open_dimensions": sorted(open_dimensions),
                }
            )
        invalid_dimensions = sorted(
            {
                str(row.get("dimension") or "")
                for row in decisions
                if str(row.get("dimension") or "") not in open_dimensions
            }
        )
        if invalid_dimensions:
            failures.append(
                {
                    "check": "intent_lock_authorial_dimensions",
                    "reason": "authorial decisions may change only dimensions left open by the intent lock",
                    "invalid_dimensions": invalid_dimensions,
                    "open_dimensions": sorted(open_dimensions),
                }
            )
    for exclusion in nonempty_string_list(core.get("user_exclusions")):
        if text_contains_term(prompt_en, exclusion):
            failures.append(
                {
                    "check": "authorial_core_exclusion",
                    "reason": "final prompt reintroduced an explicit authorial-core exclusion",
                    "exclusion": exclusion,
                }
            )
    for label in nonempty_string_list(core.get("runtime_forbidden_labels")):
        if text_contains_term(prompt_en, label):
            failures.append(
                {
                    "check": "intent_lock_runtime_label",
                    "reason": "a runtime-only label leaked into prompt_en without being removed from meaning resolution",
                    "label": label,
                }
            )
    return failures


def audit_semantic_clarification_v5(
    pack: dict[str, Any],
    composed: dict[str, Any],
    prompt_en: str,
) -> list[dict[str, Any]]:
    contract = (
        pack.get("semantic_clarification")
        if isinstance(pack.get("semantic_clarification"), dict)
        else {}
    )
    if not contract:
        return []
    failures: list[dict[str, Any]] = []
    if (
        contract.get("contract_version") != SEMANTIC_CLARIFICATION_CONTRACT_VERSION
        or contract.get("affected_by_creativity") is not False
        or contract.get("affected_by_seed") is not False
    ):
        failures.append(
            {
                "check": "semantic_clarification_contract",
                "reason": "semantic clarification must be deterministic and separate from creative sampling",
            }
        )
    candidates = [
        row for row in contract.get("candidates") or [] if isinstance(row, dict)
    ]
    candidate_map = {
        str(row.get("id") or ""): row
        for row in candidates
        if str(row.get("id") or "")
    }
    pack_candidate_ids = candidate_ids_from_pack(pack) | set(candidate_map)
    decisions = [
        row
        for row in composed.get("semantic_clarification_decisions") or []
        if isinstance(row, dict)
    ]
    decision_ids = [str(row.get("clarification_id") or "") for row in decisions]
    if (
        set(decision_ids) != set(candidate_map)
        or len(decision_ids) != len(set(decision_ids))
    ):
        failures.append(
            {
                "check": "semantic_clarification_decisions",
                "reason": "every clarification candidate requires exactly one typed decision",
                "expected": sorted(candidate_map),
                "actual": decision_ids,
            }
        )
    for decision in decisions:
        clarification_id = str(decision.get("clarification_id") or "")
        candidate = candidate_map.get(clarification_id)
        if candidate is None:
            continue
        state = str(decision.get("decision") or "")
        rationale = str(decision.get("rationale") or "")
        if state not in {"applied", "rejected", "superseded_by_revision"} or len(
            authorial_evidence_tokens(rationale)
        ) < 2:
            failures.append(
                {
                    "check": "semantic_clarification_decisions",
                    "reason": "each clarification needs a typed decision plus a substantive rationale",
                    "clarification_id": clarification_id,
                }
            )
            continue
        status = str((candidate.get("applicability") or {}).get("status") or "")
        revisable = candidate.get("revisable") is True
        if revisable and state == "rejected":
            failures.append(
                {
                    "check": "semantic_clarification_revision",
                    "reason": "a revisable governing hypothesis must be applied or replaced by a typed revision",
                    "clarification_id": clarification_id,
                }
            )
        if candidate.get("required_in_final_prompt") is True and state != "applied":
            failures.append(
                {
                    "check": "semantic_clarification_required",
                    "reason": "a required meaning clarification cannot be rejected",
                    "clarification_id": clarification_id,
                }
            )
        if status in {"context_mismatch", "requires_existing_adult_context"} and state != "rejected":
            failures.append(
                {
                    "check": "semantic_clarification_applicability",
                    "reason": "a context-mismatched or adult-context-gated meaning cannot be applied",
                    "clarification_id": clarification_id,
                }
            )
        if state == "superseded_by_revision":
            revised_meaning = str(decision.get("revised_meaning") or "").strip()
            evidence = str(decision.get("prompt_evidence") or "").strip()
            source_ids = nonempty_string_list(decision.get("revision_source_ids"))
            invalid_source_ids = [
                source_id
                for source_id in source_ids
                if source_id == clarification_id or source_id not in pack_candidate_ids
            ]
            original_terms = authorial_evidence_tokens(
                str(candidate.get("interpreted_meaning") or "")
            )
            evidence_terms = authorial_evidence_tokens(evidence)
            if (
                not revisable
                or str(decision.get("revision_basis") or "")
                != "candidate_pack_clarification"
                or len(authorial_general_content_words(revised_meaning)) < 4
                or not source_ids
                or len(source_ids) != len(set(source_ids))
                or invalid_source_ids
                or len(evidence_terms) < 4
                or len(evidence_terms - original_terms) < 2
                or not text_contains_term(prompt_en, evidence)
            ):
                failures.append(
                    {
                        "check": "semantic_clarification_revision",
                        "reason": (
                            "only an agent hypothesis may be superseded, and its typed revision must "
                            "cite pack candidates and bind newly authored literal evidence"
                        ),
                        "clarification_id": clarification_id,
                        "invalid_revision_source_ids": invalid_source_ids,
                    }
                )
        if state == "applied":
            evidence = str(decision.get("prompt_evidence") or "").strip()
            if not evidence or not text_contains_term(prompt_en, evidence):
                failures.append(
                    {
                        "check": "semantic_clarification_binding",
                        "reason": "applied clarification needs literal prompt evidence",
                        "clarification_id": clarification_id,
                    }
                )
            required_evidence = str(candidate.get("required_prompt_evidence") or "")
            if required_evidence and not text_contains_term(prompt_en, required_evidence):
                failures.append(
                    {
                        "check": "semantic_clarification_user_definition",
                        "reason": "requesting-user definition evidence was not preserved literally",
                        "clarification_id": clarification_id,
                    }
                )
        for label in candidate.get("forbidden_runtime_labels") or []:
            if text_contains_term(prompt_en, str(label)):
                failures.append(
                    {
                        "check": "semantic_clarification_sensitive_label",
                        "reason": "a definition-only sensitive label leaked into prompt_en",
                        "clarification_id": clarification_id,
                        "label": label,
                    }
                )
    return failures


def audit_creative_augmentation_v5(
    pack: dict[str, Any],
    composed: dict[str, Any],
    prompt_en: str,
    chosen: set[str],
) -> list[dict[str, Any]]:
    contract = (
        pack.get("creative_augmentation")
        if isinstance(pack.get("creative_augmentation"), dict)
        else {}
    )
    if not contract or not contract.get("enabled"):
        return []
    failures: list[dict[str, Any]] = []
    core = (
        pack.get("authorial_core")
        if isinstance(pack.get("authorial_core"), dict)
        else {}
    )
    intent_lock = (
        core.get("intent_lock")
        if core.get("contract_version") in AUTHORIAL_CORE_MODERN_CONTRACT_VERSIONS
        and isinstance(core.get("intent_lock"), dict)
        else {}
    )
    candidates = creative_augmentation_candidates_from_pack(pack)
    candidate_map = {
        str(row.get("id") or ""): row
        for row in candidates
        if str(row.get("id") or "")
    }
    allowed_bands = {
        str(item)
        for item in ((contract.get("distance_policy") or {}).get("allowed_bands") or [])
    }
    if (
        contract.get("contract_version") != CREATIVE_AUGMENTATION_CONTRACT_VERSION
        or not re.fullmatch(r"[0-9a-f]{64}", str(contract.get("hard_eligible_pool_sha256") or ""))
        or not re.fullmatch(r"[0-9a-f]{64}", str(contract.get("guard_invariant_sha256") or ""))
        or any(str(row.get("semantic_band") or "") not in allowed_bands for row in candidates)
    ):
        failures.append(
            {
                "check": "creative_augmentation_contract",
                "reason": "v5 creative augmentation has an invalid pool, guard, or distance-band contract",
            }
        )
    brief = (
        composed.get("creative_augmentation_brief")
        if isinstance(composed.get("creative_augmentation_brief"), dict)
        else {}
    )
    decisions = [
        row for row in brief.get("decisions") or [] if isinstance(row, dict)
    ]
    decision_ids = [str(row.get("candidate_id") or "") for row in decisions]
    if (
        set(decision_ids) != set(candidate_map)
        or len(decision_ids) != len(set(decision_ids))
    ):
        failures.append(
            {
                "check": "creative_augmentation_decisions",
                "reason": "every sampled creative candidate requires exactly one transformed or rejected decision",
                "expected": sorted(candidate_map),
                "actual": decision_ids,
            }
        )
    transformed: set[str] = set()
    for decision in decisions:
        candidate_id = str(decision.get("candidate_id") or "")
        candidate = candidate_map.get(candidate_id)
        if candidate is None:
            continue
        state = str(decision.get("decision") or "")
        rationale = str(decision.get("rationale") or "")
        if state not in {"transformed", "rejected"} or len(
            authorial_evidence_tokens(rationale)
        ) < 2:
            failures.append(
                {
                    "check": "creative_augmentation_decisions",
                    "reason": "every sampled candidate needs transformed/rejected plus rationale",
                    "candidate_id": candidate_id,
                }
            )
            continue
        if state == "rejected":
            if candidate_id in chosen:
                failures.append(
                    {
                        "check": "creative_augmentation_provenance",
                        "reason": "a rejected creative candidate must not be chosen",
                        "candidate_id": candidate_id,
                    }
                )
            continue
        transformed.add(candidate_id)
        evidence = str(decision.get("prompt_evidence") or "").strip()
        interpretation = str(decision.get("artistic_interpretation") or "")
        transformation = str(decision.get("transformation") or "")
        affected_dimensions = nonempty_string_list(
            decision.get("affected_dimensions")
        )
        if intent_lock:
            open_dimensions = {
                str(item) for item in intent_lock.get("open_dimensions") or []
            }
            invalid_dimensions = sorted(
                set(affected_dimensions) - open_dimensions
            )
            if (
                not affected_dimensions
                or len(affected_dimensions) != len(set(affected_dimensions))
                or invalid_dimensions
            ):
                failures.append(
                    {
                        "check": "intent_lock_creative_dimensions",
                        "reason": "a transformed candidate must name distinct affected dimensions and keep them within the intent lock's open dimensions",
                        "candidate_id": candidate_id,
                        "invalid_dimensions": invalid_dimensions,
                        "open_dimensions": sorted(open_dimensions),
                    }
                )
        if (
            candidate_id not in chosen
            or not evidence
            or not text_contains_term(prompt_en, evidence)
            or len(authorial_evidence_tokens(interpretation)) < 3
            or len(authorial_evidence_tokens(transformation)) < 3
        ):
            failures.append(
                {
                    "check": "creative_augmentation_transform",
                    "reason": "transformed material needs chosen provenance, interpretation, transformation, and literal evidence",
                    "candidate_id": candidate_id,
                }
            )
            continue
        source_terms = {
            token
            for item in candidate.get("concept_terms") or []
            for token in authorial_evidence_tokens(str(item))
        }
        evidence_terms = authorial_evidence_tokens(evidence)
        if len(evidence_terms) < 4 or len(evidence_terms - source_terms) < 2:
            failures.append(
                {
                    "check": "creative_augmentation_transform",
                    "reason": "creative evidence must add at least two authored content words beyond source terms",
                    "candidate_id": candidate_id,
                }
            )
    if len(transformed) > int(
        ((contract.get("selection_contract") or {}).get("maximum_transformed") or 3)
    ):
        failures.append(
            {
                "check": "creative_augmentation_budget",
                "reason": "too many creative candidates were transformed",
                "actual": len(transformed),
            }
        )
    return failures


def audit_adult_appeal_v5(
    pack: dict[str, Any],
    composed: dict[str, Any],
    prompt_en: str,
    chosen: set[str],
    candidate_objects: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    contract = (
        pack.get("adult_appeal")
        if isinstance(pack.get("adult_appeal"), dict)
        else {}
    )
    if not contract.get("enabled"):
        return [], []
    failures: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    brief = (
        composed.get("adult_appeal_brief")
        if isinstance(composed.get("adult_appeal_brief"), dict)
        else {}
    )
    adult_phrase = str(brief.get("adult_subject_phrase") or "")
    agency_phrase = str(brief.get("agency_phrase") or "")
    if (
        not re.search(r"\badult\b", adult_phrase, flags=re.IGNORECASE)
        or not text_contains_term(prompt_en, adult_phrase)
    ):
        failures.append(
            {
                "check": "adult_appeal_adult_subject",
                "reason": "adult_subject_phrase must be literal and explicitly adult",
            }
        )
    if not agency_phrase or not text_contains_term(prompt_en, agency_phrase):
        failures.append(
            {
                "check": "adult_appeal_agency",
                "reason": "agency_phrase must be literal in prompt_en",
            }
        )
    expected_axes = contract.get("axes") if isinstance(contract.get("axes"), dict) else {}
    actual_axes = brief.get("axes") if isinstance(brief.get("axes"), dict) else {}
    for axis_id, axis in expected_axes.items():
        if not isinstance(axis, dict):
            continue
        expected_intensity = int(axis.get("intensity", 0) or 0)
        actual = actual_axes.get(axis_id) if isinstance(actual_axes.get(axis_id), dict) else {}
        try:
            actual_intensity = int(actual.get("intensity", -1))
        except (TypeError, ValueError):
            actual_intensity = -1
        evidence = str(actual.get("prompt_evidence") or "")
        if actual_intensity != expected_intensity or (
            expected_intensity > 0
            and (
                len(authorial_evidence_tokens(str(actual.get("artistic_interpretation") or ""))) < 3
                or not evidence
                or not text_contains_term(prompt_en, evidence)
            )
        ):
            failures.append(
                {
                    "check": "adult_appeal_axes",
                    "reason": "active v5 adult-appeal axes must preserve intensity and authored literal evidence",
                    "axis": axis_id,
                }
            )
    expected_emphasis = str((contract.get("blend") or {}).get("emphasis") or "")
    actual_emphasis = str((brief.get("blend") or {}).get("emphasis") or "")
    if expected_emphasis != actual_emphasis:
        failures.append(
            {
                "check": "adult_appeal_blend",
                "reason": "v5 adult-appeal blend differs from the preserved contract",
            }
        )

    # v5 moves the existing adult-appeal contract out of the fixed v4 hybrid
    # block, but it must preserve the same styling/pose/camera cross-check.
    # This is compatibility enforcement, not a new policy or routing rule.
    combination = (
        contract.get("combination_policy")
        if isinstance(contract.get("combination_policy"), dict)
        else {}
    )
    risk_hits: set[str] = set()
    risk_groups = (
        combination.get("risk_groups")
        if isinstance(combination.get("risk_groups"), dict)
        else {}
    )
    chosen_entry_ids = {
        str(candidate_objects.get(candidate_id, {}).get("entry_id") or "")
        for candidate_id in chosen
    }
    for group_id, group in risk_groups.items():
        if not isinstance(group, dict):
            continue
        entry_ids = {str(item) for item in group.get("entry_ids") or []}
        prompt_terms = [str(item) for item in group.get("prompt_terms") or []]
        if chosen_entry_ids & entry_ids or any(
            text_contains_term(prompt_en, term) for term in prompt_terms
        ):
            risk_hits.add(str(group_id))
    for rule in combination.get("hard_combinations") or []:
        if not isinstance(rule, dict):
            continue
        required = {str(item) for item in rule.get("all_of") or []}
        if required and required <= risk_hits:
            failures.append(
                {
                    "check": "adult_appeal_combination_risk",
                    "reason": str(
                        rule.get("reason")
                        or "high-risk styling and camera combination"
                    ),
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
                    "reason": str(
                        rule.get("reason") or "stacked adult-fashion emphasis"
                    ),
                    "rule_id": rule.get("id"),
                    "risk_groups": sorted(required),
                }
            )
    return failures, warnings


def audit_character_response_v6(
    pack: dict[str, Any],
    composed: dict[str, Any],
    prompt_en: str,
) -> list[dict[str, Any]]:
    core = (
        pack.get("authorial_core")
        if isinstance(pack.get("authorial_core"), dict)
        else {}
    )
    required_assertions = [
        item
        for item in core.get("semantic_assertions") or []
        if isinstance(item, dict)
        and item.get("dimension") == "character_response"
        and item.get("polarity") == "required"
    ]
    contract = (
        pack.get("character_response")
        if isinstance(pack.get("character_response"), dict)
        else {}
    )
    if not contract:
        return (
            [
                {
                    "check": "character_response_contract",
                    "reason": "a required typed character-response assertion is missing its downstream contract",
                }
            ]
            if required_assertions
            else []
        )
    failures: list[dict[str, Any]] = []
    if len(required_assertions) != 1:
        return [
            {
                "check": "character_response_contract",
                "reason": "a character-response contract requires exactly one governing typed assertion",
            }
        ]
    governing_assertion = required_assertions[0]
    frozen = (
        contract.get("frozen_evidence")
        if isinstance(contract.get("frozen_evidence"), dict)
        else {}
    )
    binding = (
        contract.get("prompt_binding")
        if isinstance(contract.get("prompt_binding"), dict)
        else {}
    )
    required_fields = nonempty_string_list(binding.get("required_evidence_fields"))
    if (
        contract.get("contract_version") != CHARACTER_RESPONSE_CONTRACT_VERSION
        or contract.get("enabled") is not True
        or contract.get("source") != "authorial_core_semantic_assertion"
        or contract.get("source_authorial_core_sha256")
        != core.get("canonical_sha256")
        or contract.get("source_intent_lock_sha256")
        != (core.get("intent_lock") or {}).get("canonical_sha256")
        or contract.get("source_assertion_id")
        != governing_assertion.get("assertion_id")
        or contract.get("source_span_ids")
        != governing_assertion.get("source_span_ids")
        or contract.get("semantic_axes") != governing_assertion.get("axes")
        or frozen != governing_assertion.get("evidence")
        or set(required_fields) != CHARACTER_RESPONSE_REQUIRED_EVIDENCE
        or set(frozen) < CHARACTER_RESPONSE_REQUIRED_EVIDENCE
        or binding.get("new_hard_evidence_from_retrieval_forbidden") is not True
        or not re.fullmatch(
            r"[0-9a-f]{64}", str(contract.get("canonical_sha256") or "")
        )
    ):
        failures.append(
            {
                "check": "character_response_contract",
                "reason": "v6 character response is not bound to one typed assertion and its frozen generic evidence",
            }
        )
    contract_material = copy.deepcopy(contract)
    contract_sha = str(contract_material.pop("canonical_sha256", "") or "")
    if contract_sha != canonical_json_sha256(contract_material):
        failures.append(
            {
                "check": "character_response_integrity",
                "reason": "character-response content does not match its canonical hash",
            }
        )

    response = (
        composed.get("character_response")
        if isinstance(composed.get("character_response"), dict)
        else {}
    )
    evidence = (
        response.get("evidence")
        if isinstance(response.get("evidence"), dict)
        else {}
    )
    if str(response.get("source_contract_sha256") or "") != contract_sha:
        failures.append(
            {
                "check": "character_response_binding",
                "reason": "composed character response is not bound to the pack contract hash",
            }
        )
    if set(evidence) != set(required_fields):
        failures.append(
            {
                "check": "character_response_evidence",
                "reason": "composed evidence must cover every required generic causal field exactly once",
                "expected": required_fields,
                "actual": sorted(evidence),
            }
        )
    for field in required_fields:
        expected_phrase = str(frozen.get(field) or "")
        actual_phrase = str(evidence.get(field) or "")
        if actual_phrase != expected_phrase or not text_contains_term(
            prompt_en, actual_phrase
        ):
            failures.append(
                {
                    "check": "character_response_evidence",
                    "reason": "typed evidence must remain byte-identical to the frozen phrase and literal in prompt_en",
                    "field": field,
                }
            )

    advisory = (
        contract.get("advisory_retrieval")
        if isinstance(contract.get("advisory_retrieval"), dict)
        else {}
    )
    available_ids = {
        str(item.get("candidate_id") or "")
        for item in advisory.get("candidates") or []
        if isinstance(item, dict) and str(item.get("candidate_id") or "")
    }
    selected = nonempty_string_list(response.get("selected_advisory_candidate_ids"))
    if len(selected) != len(set(selected)) or not set(selected) <= available_ids:
        failures.append(
            {
                "check": "character_response_advisory_selection",
                "reason": "selected advisory behavior nodes must be distinct members of the retrieved optional set",
                "unexpected": sorted(set(selected) - available_ids),
            }
        )
    return failures


def expected_semantic_assertion_obligations(
    core: dict[str, Any],
) -> dict[str, Any] | None:
    if core.get("contract_version") != AUTHORIAL_CORE_V3_CONTRACT_VERSION:
        return None
    assertions = [
        item
        for item in core.get("semantic_assertions") or []
        if isinstance(item, dict)
        and item.get("polarity") == "required"
        and item.get("dimension") != "character_response"
    ]
    if not assertions:
        return None
    obligations: list[dict[str, Any]] = []
    for assertion in assertions:
        frozen = copy.deepcopy(assertion.get("evidence") or {})
        obligations.append(
            {
                "assertion_id": str(assertion.get("assertion_id") or ""),
                "dimension": str(assertion.get("dimension") or ""),
                "affected_dimensions": copy.deepcopy(
                    assertion.get("affected_dimensions") or []
                ),
                "source_span_ids": copy.deepcopy(
                    assertion.get("source_span_ids") or []
                ),
                "semantic_axes": copy.deepcopy(assertion.get("axes") or {}),
                "frozen_evidence": frozen,
                "prompt_binding": {
                    "required_evidence_fields": list(frozen),
                    "all_required_phrases_must_be_literal_in_final_prompt": True,
                    "evidence_must_remain_byte_identical": True,
                    "new_hard_evidence_from_retrieval_forbidden": True,
                },
            }
        )
    expected: dict[str, Any] = {
        "contract_version": SEMANTIC_ASSERTION_OBLIGATIONS_CONTRACT_VERSION,
        "enabled": True,
        "source": "authorial_core_semantic_assertions",
        "source_authorial_core_sha256": str(core.get("canonical_sha256") or ""),
        "source_intent_lock_sha256": str(
            ((core.get("intent_lock") or {}).get("canonical_sha256") or "")
        ),
        "composed_field": "semantic_assertion_evidence",
        "obligations": obligations,
    }
    expected["canonical_sha256"] = canonical_json_sha256(expected)
    return expected


def audit_semantic_assertion_obligations_v6(
    pack: dict[str, Any],
    composed: dict[str, Any],
    prompt_en: str,
) -> list[dict[str, Any]]:
    core = (
        pack.get("authorial_core")
        if isinstance(pack.get("authorial_core"), dict)
        else {}
    )
    expected = expected_semantic_assertion_obligations(core)
    supplied = (
        pack.get("semantic_assertion_obligations")
        if isinstance(pack.get("semantic_assertion_obligations"), dict)
        else None
    )
    composed_binding = composed.get("semantic_assertion_evidence")
    if expected is None:
        if supplied is None and composed_binding in (None, {}):
            return []
        return [
            {
                "check": "semantic_assertion_obligations_contract",
                "reason": "semantic-assertion evidence was supplied without a required non-character typed assertion",
            }
        ]
    failures: list[dict[str, Any]] = []
    if supplied != expected:
        failures.append(
            {
                "check": "semantic_assertion_obligations_contract",
                "reason": "required typed semantic assertions were changed or dropped after the authorial core was frozen",
            }
        )
    if not isinstance(composed_binding, dict) or set(composed_binding) != {
        "source_contract_sha256",
        "evidence",
    }:
        return failures + [
            {
                "check": "semantic_assertion_evidence",
                "reason": "composed output must bind the exact semantic-assertion contract and evidence map",
            }
        ]
    if composed_binding.get("source_contract_sha256") != expected.get(
        "canonical_sha256"
    ):
        failures.append(
            {
                "check": "semantic_assertion_evidence",
                "reason": "composed semantic evidence is not bound to the governing contract hash",
            }
        )
    actual_by_id = (
        composed_binding.get("evidence")
        if isinstance(composed_binding.get("evidence"), dict)
        else {}
    )
    expected_by_id = {
        str(obligation.get("assertion_id") or ""): obligation.get(
            "frozen_evidence"
        )
        for obligation in expected.get("obligations") or []
        if isinstance(obligation, dict)
    }
    if set(actual_by_id) != set(expected_by_id):
        failures.append(
            {
                "check": "semantic_assertion_evidence",
                "reason": "composed evidence must cover every required assertion exactly once",
                "expected": sorted(expected_by_id),
                "actual": sorted(actual_by_id),
            }
        )
    for assertion_id, expected_evidence in expected_by_id.items():
        actual_evidence = actual_by_id.get(assertion_id)
        if not isinstance(actual_evidence, dict) or actual_evidence != expected_evidence:
            failures.append(
                {
                    "check": "semantic_assertion_evidence",
                    "reason": "typed semantic evidence must remain byte-identical to the frozen assertion",
                    "assertion_id": assertion_id,
                }
            )
            continue
        for field, phrase in expected_evidence.items():
            if not text_contains_term(prompt_en, str(phrase or "")):
                failures.append(
                    {
                        "check": "semantic_assertion_evidence",
                        "reason": "every frozen semantic-evidence phrase must remain literal in prompt_en",
                        "assertion_id": assertion_id,
                        "field": field,
                    }
                )
    return failures


def expected_render_repair_contract(
    core: dict[str, Any],
) -> dict[str, Any] | None:
    lineage = (
        core.get("request_lineage")
        if isinstance(core.get("request_lineage"), dict)
        else {}
    )
    if lineage.get("contract_version") != REQUEST_LINEAGE_V2_CONTRACT_VERSION:
        return None
    targets: list[dict[str, Any]] = []
    required_hard_gates: list[str] = []
    for target in lineage.get("repair_targets") or []:
        if not isinstance(target, dict):
            continue
        repair_id = str(target.get("repair_id") or "")
        gates: list[dict[str, Any]] = [
            {
                "id": f"rr_{repair_id}_object_class_legible",
                "review_scale": "both",
                "criterion": (
                    "The target object is recognizable as the intended object class at thumbnail "
                    "and native scale."
                ),
            },
            {
                "id": f"rr_{repair_id}_gross_structure_coherent",
                "review_scale": "native",
                "criterion": (
                    "The target object's major parts form one coherent, non-grotesque structure; "
                    "minor ornament differences are non-blocking."
                ),
            },
            {
                "id": f"rr_{repair_id}_intended_interaction_matches",
                "review_scale": "both",
                "criterion": (
                    "The actor, object, and intended interaction state match the frozen relation; "
                    "removal, relocation, concealment, or transfer is not a repair."
                ),
            },
        ]
        if str(target.get("actor_object_contact") or "") in {
            "required",
            "transitional",
        }:
            gates.append(
                {
                    "id": f"rr_{repair_id}_contact_anatomy_coherent",
                    "review_scale": "native",
                    "criterion": (
                        "The event-critical actor-object contact and principal anatomy are coherent "
                        "without severe fusion or impossible articulation."
                    ),
                }
            )
        gate_ids = [str(gate["id"]) for gate in gates]
        required_hard_gates.extend(gate_ids)
        targets.append(
            {
                "repair_id": repair_id,
                "source_span_ids": copy.deepcopy(target.get("source_span_ids") or []),
                "importance": str(target.get("importance") or ""),
                "relation_origin": str(target.get("relation_origin") or ""),
                "actor_phrase": str(target.get("actor_phrase") or ""),
                "object_phrase": str(target.get("object_phrase") or ""),
                "interaction_state": str(target.get("interaction_state") or ""),
                "actor_object_contact": str(
                    target.get("actor_object_contact") or ""
                ),
                "protected_dimensions": copy.deepcopy(
                    target.get("protected_dimensions") or []
                ),
                "allowed_repair_axes": copy.deepcopy(
                    target.get("allowed_repair_axes") or []
                ),
                "frozen_evidence": {
                    "interaction_phrase": str(
                        target.get("interaction_phrase") or ""
                    ),
                    "recognition_phrase": str(
                        target.get("recognition_phrase") or ""
                    ),
                },
                "prompt_binding": {
                    "required_evidence_fields": [
                        "interaction_phrase",
                        "recognition_phrase",
                    ],
                    "all_required_phrases_must_be_literal_in_final_prompt": True,
                    "evidence_must_remain_byte_identical": True,
                    "semantic_substitution_forbidden": True,
                },
                "render_gates": gates,
                "required_hard_gates": gate_ids,
            }
        )
    expected: dict[str, Any] = {
        "contract_version": RENDER_REPAIR_CONTRACT_VERSION,
        "enabled": True,
        "source": "authorial_core_request_lineage",
        "source_authorial_core_sha256": str(core.get("canonical_sha256") or ""),
        "source_intent_lock_sha256": str(
            ((core.get("intent_lock") or {}).get("canonical_sha256") or "")
        ),
        "source_request_lineage_sha256": str(
            lineage.get("canonical_sha256") or ""
        ),
        "composed_field": "render_repair_evidence",
        "strict_gate_set": True,
        "major_only": True,
        "targets": targets,
        "required_hard_gates": required_hard_gates,
        "retry_policy": {
            "preserve_interaction_relation": True,
            "repair_smallest_failed_gate_set": True,
            "removal_relocation_concealment_or_transfer_is_not_repair": True,
            "minor_decorative_variation_is_non_blocking": True,
            "maximum_additional_attempts": 1,
        },
    }
    expected["canonical_sha256"] = canonical_json_sha256(expected)
    return expected


def audit_render_repair_v6(
    pack: dict[str, Any],
    composed: dict[str, Any],
    prompt_en: str,
) -> list[dict[str, Any]]:
    core = (
        pack.get("authorial_core")
        if isinstance(pack.get("authorial_core"), dict)
        else {}
    )
    expected = expected_render_repair_contract(core)
    supplied = (
        pack.get("render_repair")
        if isinstance(pack.get("render_repair"), dict)
        else None
    )
    composed_binding = composed.get("render_repair_evidence")
    if expected is None:
        if supplied is None and composed_binding in (None, {}):
            return []
        return [
            {
                "check": "render_repair_contract",
                "reason": "render-repair evidence was supplied without a v2 request-lineage repair target",
            }
        ]
    failures: list[dict[str, Any]] = []
    if supplied != expected:
        failures.append(
            {
                "check": "render_repair_contract",
                "reason": "the lineage-bound render-repair contract was changed or dropped after the core was frozen",
            }
        )
    if not isinstance(composed_binding, dict) or set(composed_binding) != {
        "source_contract_sha256",
        "evidence",
    }:
        return failures + [
            {
                "check": "render_repair_evidence",
                "reason": "composed output must bind the exact render-repair contract and evidence map",
            }
        ]
    if composed_binding.get("source_contract_sha256") != expected.get(
        "canonical_sha256"
    ):
        failures.append(
            {
                "check": "render_repair_evidence",
                "reason": "composed render-repair evidence is not bound to the governing contract hash",
            }
        )
    actual_by_id = (
        composed_binding.get("evidence")
        if isinstance(composed_binding.get("evidence"), dict)
        else {}
    )
    expected_by_id = {
        str(target.get("repair_id") or ""): target.get("frozen_evidence")
        for target in expected.get("targets") or []
        if isinstance(target, dict)
    }
    if set(actual_by_id) != set(expected_by_id):
        failures.append(
            {
                "check": "render_repair_evidence",
                "reason": "composed evidence must cover every repair target exactly once",
                "expected": sorted(expected_by_id),
                "actual": sorted(actual_by_id),
            }
        )
    for repair_id, expected_evidence in expected_by_id.items():
        actual_evidence = actual_by_id.get(repair_id)
        if not isinstance(actual_evidence, dict) or actual_evidence != expected_evidence:
            failures.append(
                {
                    "check": "render_repair_evidence",
                    "reason": "repair evidence must remain byte-identical to the frozen target",
                    "repair_id": repair_id,
                }
            )
            continue
        for field, phrase in expected_evidence.items():
            if not text_contains_term(prompt_en, str(phrase or "")):
                failures.append(
                    {
                        "check": "render_repair_evidence",
                        "reason": "every frozen repair-evidence phrase must remain literal in prompt_en",
                        "repair_id": repair_id,
                        "field": field,
                    }
                )
    return failures


def audit_composed_prompt(pack: dict[str, Any], composed: dict[str, Any]) -> dict[str, Any]:
    failures: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    prompt_en = str(composed.get("prompt_en") or "")
    search_text = composed_search_text(composed)
    negative_en = composed.get("negative_en")

    contract_version = str(pack.get("contract_version") or "")
    if contract_version not in SUPPORTED_CANDIDATE_PACK_VERSIONS:
        failures.append(
            {
                "check": "contract_version",
                "reason": "unsupported candidate-pack contract",
                "expected": sorted(SUPPORTED_CANDIDATE_PACK_VERSIONS),
                "actual": contract_version or None,
            }
        )
    failures.extend(audit_v4_authorial_pack(pack))

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
    failures.extend(audit_negative_intent_guard(pack, prompt_en))

    failures.extend(audit_creative_direction(pack, composed, prompt_en))
    failures.extend(audit_moe_response(pack, composed, prompt_en, warnings))
    failures.extend(audit_character_response_v6(pack, composed, prompt_en))
    failures.extend(
        audit_semantic_assertion_obligations_v6(pack, composed, prompt_en)
    )
    failures.extend(audit_render_repair_v6(pack, composed, prompt_en))
    failures.extend(audit_visual_obligations(pack, composed, prompt_en))
    failures.extend(audit_viewer_experience(pack, composed, prompt_en))
    failures.extend(audit_authorial_core_v5(pack, composed, prompt_en, warnings))
    failures.extend(audit_semantic_clarification_v5(pack, composed, prompt_en))

    safety = pack.get("safety") if isinstance(pack.get("safety"), dict) else {}
    if safety.get("status") != "pass" or safety.get("requires_user_approval") is True:
        failures.append({"check": "safety", "reason": "candidate pack safety contract is not pass", "safety": safety})
    failed_gates = [
        gate
        for gate in pack.get("concept_gates") or []
        if isinstance(gate, dict) and gate.get("status") not in {"pass", "manual"}
    ]
    if failed_gates:
        failures.append({"check": "concept_gates", "reason": "candidate pack contains a failed concept gate", "gates": failed_gates})
    manual_gates = [
        gate
        for gate in pack.get("concept_gates") or []
        if isinstance(gate, dict) and gate.get("status") == "manual"
    ]
    if manual_gates:
        manual_evidence = composed.get("manual_gate_evidence")
        if not isinstance(manual_evidence, dict):
            failures.append(
                {
                    "check": "concept_gates",
                    "reason": "manual concept gates require prompt-bound evidence before pixel review",
                    "gate_ids": [str(gate.get("id") or "") for gate in manual_gates],
                }
            )
        else:
            for gate in manual_gates:
                gate_id = str(gate.get("id") or "")
                evidence = manual_evidence.get(gate_id)
                if not isinstance(evidence, dict):
                    failures.append(
                        {
                            "check": "concept_gates",
                            "reason": "manual concept gate is missing an evidence object",
                            "gate_id": gate_id,
                        }
                    )
                    continue
                evidence_phrases = nonempty_string_list(evidence.get("evidence_phrases"))
                minimum = 2 if gate_id in {"contradiction_in_frame", "costume_swap_test"} else 1
                if len(evidence_phrases) < minimum:
                    failures.append(
                        {
                            "check": "concept_gates",
                            "reason": "manual concept gate has insufficient prompt evidence",
                            "gate_id": gate_id,
                            "minimum_phrases": minimum,
                        }
                    )
                    continue
                missing_phrases = [
                    phrase for phrase in evidence_phrases if not text_contains_term(prompt_en, phrase)
                ]
                if missing_phrases:
                    failures.append(
                        {
                            "check": "concept_gates",
                            "reason": "manual concept-gate evidence is not literal in prompt_en",
                            "gate_id": gate_id,
                            "phrases": missing_phrases,
                        }
                    )
                    continue
                if str(evidence.get("review_stage") or "") != "pixel_review_required":
                    failures.append(
                        {
                            "check": "concept_gates",
                            "reason": "manual gate evidence must remain pending for pixel review",
                            "gate_id": gate_id,
                        }
                    )
                    continue
                warnings.append(
                    {
                        "check": "manual_concept_gate",
                        "reason": "prompt evidence is bound; native-pixel confirmation is still required",
                        "gate_id": gate_id,
                    }
                )

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
    if not chosen and contract_version not in {
        "photo-candidate-pack/v4",
        "photo-candidate-pack/v5",
        "photo-candidate-pack/v6",
    }:
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

    adult_v5_failures, adult_v5_warnings = audit_adult_appeal_v5(
        pack,
        composed,
        prompt_en,
        chosen,
        candidate_objects,
    )
    failures.extend(adult_v5_failures)
    warnings.extend(adult_v5_warnings)

    hybrid_failures, hybrid_warnings = audit_hybrid_augmentation(
        pack,
        composed,
        prompt_en,
        chosen,
        candidate_objects,
    )
    failures.extend(hybrid_failures)
    warnings.extend(hybrid_warnings)
    failures.extend(
        audit_creative_augmentation_v5(
            pack,
            composed,
            prompt_en,
            chosen,
        )
    )
    failures.extend(
        audit_candidate_interpretations(
            pack,
            composed,
            prompt_en,
            chosen,
            candidate_objects,
        )
    )
    failures.extend(audit_authorial_scene(pack, composed, prompt_en))
    failures.extend(audit_authorial_open_slots(pack, composed, prompt_en))
    failures.extend(audit_authorial_request(pack, composed, prompt_en))
    failures.extend(audit_japanese_subculture_photo(pack, prompt_en))

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
            "cheek_makeup",
            "complexion_coverage",
            "costume_style",
            "eye_detail",
            "eye_makeup_line",
            "eyeshadow_style",
            "face_sculpting",
            "facial_hair",
            "footwear",
            "gaze_engagement",
            "hair_color",
            "hair_style",
            "hand_pose",
            "lash_style",
            "lip_color_placement",
            "lip_finish",
            "makeup_style",
            "makeup_decoration",
            "makeup_wear_state",
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
        authored_scene = composed.get("authored_scene") if isinstance(composed.get("authored_scene"), dict) else {}
        authored_atoms = authored_scene.get("atoms") if isinstance(authored_scene.get("atoms"), dict) else {}
        authored_slots = composed.get("authored_slots") if isinstance(composed.get("authored_slots"), dict) else {}
        chosen_clue_slots = sorted(
            slot
            for slot in clue_slots
            if chosen_slots.get(slot)
            or isinstance(atomic_scene.get(slot), dict)
            or bool(str(authored_atoms.get(slot) or "").strip())
            or isinstance(authored_slots.get(slot), dict)
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
        if role_scene_policy.get("selection_mode") == "agent_authored_location":
            authored_slots = composed.get("authored_slots") if isinstance(composed.get("authored_slots"), dict) else {}
            authored_location = authored_slots.get("location")
            if not isinstance(authored_location, dict):
                failures.append(
                    {
                        "check": "role_scene_policy",
                        "reason": "agent-authored role scene requires an authored location decision",
                        "scene_family": role_scene_policy.get("scene_family"),
                    }
                )
        else:
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
    effective_visual_contract, _ = derive_effective_visual_obligation_contract(
        pack,
        composed,
    )
    return {
        "status": status,
        "quality_status": quality_status,
        "pack_id": pack_id or None,
        "chosen_candidate_count": len(chosen),
        "chosen_visual_concept_ids": [
            str(value)
            for value in (effective_visual_contract or {}).get(
                "selected_visual_concept_ids"
            )
            or []
            if str(value).strip()
        ],
        "effective_visual_contract_sha256": effective_visual_obligation_sha256(
            effective_visual_contract
        ),
        "render_repair_contract_sha256": (
            str((pack.get("render_repair") or {}).get("canonical_sha256") or "")
            if isinstance(pack.get("render_repair"), dict)
            else None
        ),
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
