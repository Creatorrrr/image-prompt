#!/usr/bin/env python3
"""Fail-closed audit for an agent-composed subculture illustration prompt.

The candidate pack is the complete trust boundary for this command.  The
auditor never imports the photographic runtime or reloads a mutable graph.
It verifies the pack's compact graph/format proof, then verifies that every
visible evidence phrase claimed by the composed object is literally present
in ``prompt_en``.

Exit status:
    0: pack integrity and composed-prompt audit pass
    1: pack is sound, but the composed prompt fails one or more checks
    2: CLI/JSON error or candidate-pack integrity failure
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping, Sequence


CONTRACT_VERSION = "subculture-illustration-candidate-pack/v1"
CONTRACT_VERSION_V2 = "subculture-illustration-candidate-pack/v2"
SUPPORTED_CONTRACT_VERSIONS = (CONTRACT_VERSION, CONTRACT_VERSION_V2)

COMPOSED_PROMPT_SCHEMA_V2 = "subculture-illustration-composed-prompt/v2"
SECOND_LOOK_PLAN_SCHEMA = "illustration-second-look-plan/v1"
SECOND_LOOK_PLAN_CONTRACT_KEYS = {
    "schema",
    "required",
    "required_roles",
    "carrier_kinds",
    "risk_flags",
    "forbidden_as_sole",
    "allowed_review_scale_ids",
    "fallback_must_reference_selected_consequence",
}
SECOND_LOOK_PLAN_KEYS = {
    "schema",
    "selected_proposal_id",
    "reveal_phrase",
    "review_scale_ids",
    "primary_carrier",
    "fallback_carrier",
}
SECOND_LOOK_CARRIER_KEYS = {
    "carrier_kind",
    "carrier_phrase",
    "protected_locus_phrase",
    "consequence_phrase",
    "risk_flags",
}
SECOND_LOOK_ROLES = ("primary_carrier", "fallback_carrier")
SECOND_LOOK_CARRIER_KINDS = (
    "surface_state",
    "material_boundary",
    "isolated_contour",
    "object_relation",
    "environmental_trace",
    "projected_form",
    "dedicated_panel",
)
SECOND_LOOK_RISK_FLAGS = (
    "compound_anatomy",
    "subscale_symbol_decode",
    "overlapping_multi_limb_projection",
)

# These patterns are intentionally scoped to the phrases explicitly linked to
# one second-look carrier.  They are a narrow under-declaration backstop, not a
# general semantic classifier over the full prompt.
SECOND_LOOK_LINKED_RISK_PATTERNS: dict[str, tuple[str, ...]] = {
    "compound_anatomy": (
        r"\b(?:clasped|clasping|interlocked|interlocking|interlaced|intertwined|entangled|overlapping|merged|clustered)\s+(?:human\s+)?(?:hands?|fingers?|arms?|limbs?)\b",
        r"\b(?:two|three|four|both|multiple|several|\d+)\s+(?:human\s+)?(?:hands?|fingers?|arms?|limbs?)\b[^.!?;]{0,64}\b(?:clasp(?:ed|ing|s)?|interlock(?:ed|ing|s)?|interlac(?:ed|ing)|intertwin(?:ed|ing)|entangl(?:ed|ing)|overlap(?:ped|ping|s)?|merg(?:ed|ing)|cluster(?:ed|ing|s)?)\b",
    ),
    "subscale_symbol_decode": (
        r"\b(?:tiny|minute|microscopic|micro[- ]?scale|sub[- ]?scale|hairline|pinhead[- ]sized|coin[- ]sized|fingernail[- ]sized)\b[^.!?;]{0,64}\b(?:text|letters?|lettering|words?|glyphs?|runes?|symbols?|inscriptions?|writing|characters?|marks?)\b",
        r"\b(?:text|letters?|lettering|words?|glyphs?|runes?|symbols?|inscriptions?|writing|characters?|marks?)\b[^.!?;]{0,64}\b(?:tiny|minute|microscopic|micro[- ]?scale|sub[- ]?scale|hairline|pinhead[- ]sized|coin[- ]sized|fingernail[- ]sized)\b",
    ),
    "overlapping_multi_limb_projection": (
        r"\b(?:overlapping|merged|intersecting|crossing|entangled|clustered)\s+multi[- ]limb(?:ed)?\s+(?:shadow|silhouette|projection|reflection)s?\b",
        r"\bmulti[- ]limb(?:ed)?\s+(?:shadow|silhouette|projection|reflection)s?\b",
        r"\b(?:two|three|four|multiple|several|\d+)\s+(?:overlapping|merged|intersecting|crossing|entangled|clustered)?\s*(?:arms?|hands?|limbs?)\s+(?:shadows?|silhouettes?|projections?|reflections?)\b",
        r"\b(?:shadows?|silhouettes?|projections?|reflections?)\b[^.!?;]{0,80}\b(?:two|three|four|multiple|several|\d+)\s+(?:arms?|hands?|limbs?)\b[^.!?;]{0,48}\b(?:overlap|merge|intersect|cross|entangle|cluster)(?:ed|ing|s)?\b",
        r"\b(?:overlapping|merged|intersecting|crossing|entangled|clustered)\b[^.!?;]{0,48}\b(?:shadows?|silhouettes?|projections?|reflections?)\s+(?:of|from)\s+(?:two|three|four|multiple|several|\d+)\s+(?:arms?|hands?|limbs?)\b",
        r"\b(?:overlapping|merged|intersecting|crossing|entangled|clustered)\b[^.!?;]{0,48}\b(?:two|three|four|multiple|several|\d+)\s+(?:arms?|hands?|limbs?)\b[^.!?;]{0,48}\b(?:shadows?|silhouettes?|projections?|reflections?)\b",
    ),
}

VARIANT_FAMILY: dict[str, str] = {
    "single_illustration": "single_frame",
    "key_art": "key_art",
    "ensemble_key_art": "key_art",
    "responsive_key_art": "key_art",
    "light_novel_cover": "cover",
    "collectible_card": "card",
    "vertical_scroll_sequence": "vertical_sequence",
    "character_design_board": "adaptation_board",
    "merch_adaptation_board": "adaptation_board",
    "campaign_art_board": "adaptation_board",
}

# These are prompt-evidence keys, not aspect-ratio aliases.  A pack may add
# stricter fields, but cannot remove these canonical variant requirements.
FORMAT_REQUIRED_FIELDS: dict[str, tuple[str, ...]] = {
    "single_illustration": (
        "decisive_instant_phrase",
        "visual_rest_or_omission_phrase",
    ),
    "key_art": (
        "project_pillar_phrase",
        "cast_world_stake_hierarchy_phrase",
        "repeatable_signature_phrase",
    ),
    "ensemble_key_art": (
        "project_pillar_phrase",
        "cast_world_stake_hierarchy_phrase",
        "repeatable_signature_phrase",
        "silhouette_separation_phrase",
        "directed_relations_phrase",
    ),
    "responsive_key_art": (
        "project_pillar_phrase",
        "cast_world_stake_hierarchy_phrase",
        "repeatable_signature_phrase",
        "square_safe_zone_phrase",
        "wide_safe_zone_phrase",
        "vertical_safe_zone_phrase",
        "core_action_preservation_phrase",
        "secondary_clue_preservation_phrase",
    ),
    "light_novel_cover": (
        "story_promise_phrase",
        "relation_or_conflict_hook_phrase",
        "title_safe_area_phrase",
        "trim_safe_core_phrase",
    ),
    "collectible_card": (
        "frame_safe_silhouette_phrase",
        "hand_action_target_phrase",
        "effect_causality_phrase",
        "rarity_as_scene_consequence_phrase",
    ),
    "vertical_scroll_sequence": (
        "beat_one_phrase",
        "beat_two_phrase",
        "gutter_duration_phrase",
        "delayed_reveal_phrase",
        "identity_invariant_phrase",
    ),
    "character_design_board": (
        "representation_one_phrase",
        "representation_two_phrase",
        "identity_invariant_phrase",
        "format_specific_simplification_phrase",
        "state_or_view_change_phrase",
    ),
    "merch_adaptation_board": (
        "representation_one_phrase",
        "representation_two_phrase",
        "identity_invariant_phrase",
        "format_specific_simplification_phrase",
        "functional_anchor_phrase",
        "small_scale_simplification_phrase",
    ),
    "campaign_art_board": (
        "representation_one_phrase",
        "representation_two_phrase",
        "identity_invariant_phrase",
        "format_specific_simplification_phrase",
        "shared_signature_phrase",
        "distinct_application_phrase",
    ),
}

AUTHORIAL_REQUIRED_FIELDS = (
    "focal_hierarchy_phrase",
    "controlled_omission_phrase",
    "edge_or_mark_rule_phrase",
    "repeated_material_or_motif_rule_phrase",
)

VIEWER_REQUIRED_FIELDS = (
    "first_glance_hook_phrase",
    "second_look_reveal_phrase",
    "affect_actor_phrase",
    "affect_action_phrase",
    "affect_target_phrase",
    "affect_consequence_phrase",
)

FORMAT_CONTRACT_KEY_GROUPS = (
    ("hierarchy_contract",),
    ("crop_contract",),
    ("sequence_contract", "sequential_contract"),
    ("scale_contract", "scale_preservation_contract"),
    ("text_space_contract", "text_safe_contract"),
)

ASPECT_ONLY_KEYS = {
    "aspect_ratio",
    "aspect_ratio_phrase",
    "ratio",
    "ratio_phrase",
    "dimensions",
    "dimensions_phrase",
}

OUTCOME_CLAIM_PATTERNS = (
    r"\bthe viewer (?:feels?|will feel|experiences?|will experience)\b",
    r"\b(?:evokes?|creates?|guarantees?) (?:empathy|attachment|engagement|immersion|virality)\b",
    r"\b(?:memorable|viral|irresistible) image\b",
    r"\bmakes? the viewer (?:feel|care|buy|share|return)\b",
)

POST_RENDER_CLAIM_PATTERNS = (
    r"\brendered pixels? (?:pass|passed|prove|proved|show|showed|verify|verified|survive|survived)\b",
    r"\b(?:the )?(?:final|generated|rendered) image (?:passes|passed|proves|proved|verifies|verified)\b",
    r"\b(?:passes|passed|verified by|approved by) (?:the )?(?:pixel|render|thumbnail|native[- ]scale) review\b",
    r"\b(?:pixel|rendered[- ]image) review\s*:\s*(?:pass|approved|verified)\b",
)

POST_RENDER_EVIDENCE_KEY_PATTERN = re.compile(
    r"(?:^|_)(?:rendered_pixel_review|post_render|pixel_review|render_review|"
    r"thumbnail_review|native_review|image_review|qualification_status)(?:_|$)",
    flags=re.IGNORECASE,
)

NON_COMPOSITION_EVIDENCE_KEYS = {
    "prompt_contract",
    "rendered_pixel_review",
}

NAMED_STYLE_PATTERNS = (
    r"\bin (?:the )?style of\b",
    r"\b(?:style|art|design) of (?-i:[A-Z][A-Za-z.'-]+(?:\s+[A-Z][A-Za-z.'-]+){0,3})\b",
    r"\bby (?:artist|illustrator|mangaka|character designer)\b",
    r"\b(?:copy|copies|replicate|replicates|imitate|imitates) (?:the )?(?:art|look|style|visual language) of\b",
    r"\b(?:Studio Ghibli|Pixar|Disney|MAPPA|ufotable|Kyoto Animation|Trigger|Madhouse|Gainax|Sunrise|Bones)(?:'s)? style\b",
)

# This is deliberately a narrow, high-confidence backstop.  The authoritative
# declaration remains reference_boundary; a local regex cannot enumerate all
# artists, studios, franchises, or protected designs.
PROTECTED_IP_PATTERNS = (
    r"\b(?:Pok[eé]mon|Pikachu|Naruto|One Piece|Genshin Impact|Honkai|Demon Slayer)\b",
    r"\b(?:Dragon Ball|Gundam|Evangelion|Hello Kitty|Sanrio|Totoro)\b",
    r"\b(?:Marvel|DC Comics|Disney|Mickey Mouse|Star Wars|Harry Potter)\b",
    r"\b(?:Super Mario|The Legend of Zelda|Sonic the Hedgehog|League of Legends|Overwatch)\b",
    r"[©™®]",
)

UNIVERSAL_INFERENCE_PATTERNS = (
    r"\b(?:universally|inherently|intrinsically|naturally|always)\b[^.!?]{0,70}\b(?:means?|symboli[sz]es?|represents?|denotes?|proves?)\b",
    r"\b(?:color|colour|red|blue|white|black|circle|square|triangle|shape)s?\b[^.!?]{0,45}\b(?:always|inherently|universally)\b",
    r"\ball (?:Korean|Japanese|Chinese|Asian|East Asian) (?:people|viewers|audiences|characters)\b",
    r"\b(?:Korean|Japanese|Chinese|Asian|East Asian) (?:people|viewers|audiences|characters) (?:are|always|naturally|inherently)\b",
    r"\b(?:national|racial|cultural) personality\b",
)

DECORATIVE_SOUP_PATTERNS = (
    r"\b(?:decorative|ornamental|random) (?:motif|motifs|symbol|symbols|icons?)\b",
    r"\b(?:motif|symbol|icon) (?:collage|soup|pile|stack)\b",
    r"\b(?:scatter|sprinkle|fill)\b[^.!?]{0,35}\b(?:motifs?|symbols?|icons?)\b",
)

FORMAT_FORBIDDEN_PATTERNS: dict[str, tuple[tuple[str, str], ...]] = {
    "light_novel_cover": (
        (r"\b(?:readable|legible|spelled[- ]out|generated) title(?: text| lettering)?\b", "generated readable title text"),
        (r"\b(?:write|render|print) the (?:exact )?title\b", "generated readable title text"),
    ),
    "collectible_card": (
        (r"\b(?:paid rarity|rarity badge|rarity stars?|gem frame|gacha UI|monetization cue|SSR badge|UR badge|five[- ]star badge)\b", "paid-rarity UI or monetization cue"),
    ),
    "vertical_scroll_sequence": (
        (r"\b(?:single|one) (?:poster|image) stretched (?:to|into) (?:9:16|vertical)\b", "stretched-poster substitution"),
    ),
    "character_design_board": (
        (r"\bidentical (?:asset|image|pose) (?:reused|repeated|copied)\b", "identical asset reuse"),
    ),
    "merch_adaptation_board": (
        (r"\bidentical (?:asset|image|pose) (?:reused|repeated|copied)\b", "identical asset reuse"),
    ),
    "campaign_art_board": (
        (r"\bidentical (?:asset|image|pose) (?:reused|repeated|copied)\b", "identical asset reuse"),
    ),
}


class AuditInputError(ValueError):
    """Raised for CLI transport or JSON shape errors."""


def issue(check: str, reason: str, **details: Any) -> dict[str, Any]:
    result: dict[str, Any] = {"check": check, "reason": reason}
    result.update(details)
    return result


def load_json_arg(raw: str) -> Any:
    """Load an inline JSON value or a UTF-8 JSON file."""

    value = str(raw or "").strip()
    if not value:
        raise AuditInputError("JSON argument must not be empty")
    if value.startswith("{") or value.startswith("["):
        return json.loads(value)
    return json.loads(Path(value).read_text(encoding="utf-8"))


def first_pack(payload: Any) -> dict[str, Any]:
    """Accept exactly one candidate pack, optionally wrapped in a list."""

    if isinstance(payload, list):
        if len(payload) != 1:
            raise AuditInputError("candidate pack list must contain exactly one pack")
        payload = payload[0]
    if not isinstance(payload, dict):
        raise AuditInputError("candidate pack must be a JSON object or a one-item list")
    return payload


def composed_object(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise AuditInputError("composed prompt must be a JSON object")
    return payload


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def computed_pack_id(pack: Mapping[str, Any]) -> str:
    """Return the canonical 16-hex pack ID with pack_id nulled."""

    hashable = dict(pack)
    hashable["pack_id"] = None
    return hashlib.sha256(canonical_json(hashable).encode("utf-8")).hexdigest()[:16]


def _is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: Any) -> list[str] | None:
    if not isinstance(value, list):
        return None
    if any(not _is_nonempty_string(item) for item in value):
        return None
    return [str(item) for item in value]


def _mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _normalized_contract_phrase(value: Any) -> str:
    """Normalize only for equality checks; literal prompt coverage stays exact."""

    if not isinstance(value, str):
        return ""
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def _exact_object_keys(
    value: Any,
    expected_keys: Iterable[str],
    *,
    check: str,
    object_name: str,
) -> list[dict[str, Any]]:
    if not isinstance(value, dict):
        return [issue(check, f"{object_name} must be an object")]
    expected = set(expected_keys)
    actual = set(value)
    if actual == expected:
        return []
    return [
        issue(
            check,
            f"{object_name} must have the exact v2 field set",
            missing=sorted(expected - actual),
            unexpected=sorted(actual - expected),
        )
    ]


def _match_is_negated(text: str, start: int) -> bool:
    """Recognize a nearby plain-language exclusion, not full English scope."""

    prefix = text[max(0, start - 64) : start]
    local_clause = re.split(r"[.!?;,:]", prefix)[-1]
    return re.search(
        r"\b(?:no|not|without|avoid|exclude|never|forbid(?:den)?)\b",
        local_clause,
        flags=re.IGNORECASE,
    ) is not None


def _nonnegated_matches(pattern: str, text: str) -> list[re.Match[str]]:
    return [
        match
        for match in re.finditer(pattern, text, flags=re.IGNORECASE)
        if not _match_is_negated(text, match.start())
    ]


def text_contains_term(text: str, term: str) -> bool:
    """Case-insensitive term coverage with ASCII token boundaries."""

    needle = str(term or "").strip()
    if not needle:
        return False
    if needle.isascii() and re.search(r"[A-Za-z0-9]", needle):
        pattern = r"(?<![A-Za-z0-9])" + re.escape(needle) + r"(?![A-Za-z0-9])"
        return re.search(pattern, text, flags=re.IGNORECASE) is not None
    return needle.casefold() in text.casefold()


def selected_runtime_nodes(pack: Mapping[str, Any]) -> list[dict[str, Any]]:
    grammar = _mapping(pack.get("visual_grammar"))
    return [node for node in grammar.get("runtime_nodes") or [] if isinstance(node, dict)]


def expected_chosen_candidate_ids(pack: Mapping[str, Any]) -> list[str]:
    """Compute the exact trace IDs exposed by a valid compact pack."""

    request = _mapping(pack.get("request_contract"))
    profile = _mapping(pack.get("format_profile"))
    route_id = str(request.get("route_id") or "")
    variant_id = str(profile.get("variant_id") or "")
    ids = [f"route:{route_id}", f"format:{variant_id}"]
    ids.extend(f"visual:{node.get('id')}" for node in selected_runtime_nodes(pack) if node.get("id"))
    return ids


def _profile_required_evidence_fields(profile: Mapping[str, Any]) -> list[str]:
    # Format assets also declare lifecycle evidence types such as
    # ``rendered_pixel_review``.  Those are qualification requirements, not
    # phrases that a pre-render prompt may truthfully claim.  Only the typed
    # composition-field list crosses into composed-prompt auditing.
    return _string_list(profile.get("required_format_evidence_fields")) or []


def _second_look_pack_contract_failures(
    pack: Mapping[str, Any],
    profile: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Validate the exact v2 pre-render second-look planning contract."""

    if pack.get("contract_version") != CONTRACT_VERSION_V2:
        return []

    errors: list[dict[str, Any]] = []
    composition = pack.get("composition_contract")
    if not isinstance(composition, dict):
        errors.append(issue("composition_contract", "composition_contract must be an object"))
    elif composition.get("composed_schema") != COMPOSED_PROMPT_SCHEMA_V2:
        errors.append(
            issue(
                "second_look_pack_contract",
                "composition_contract.composed_schema must select the v2 composed-prompt schema",
                expected=COMPOSED_PROMPT_SCHEMA_V2,
                actual=composition.get("composed_schema"),
            )
        )

    viewer = pack.get("viewer_contract")
    if not isinstance(viewer, dict):
        errors.append(issue("viewer_contract", "viewer_contract must be an object"))
        return errors
    plan_contract = viewer.get("second_look_plan_contract")
    errors.extend(
        _exact_object_keys(
            plan_contract,
            SECOND_LOOK_PLAN_CONTRACT_KEYS,
            check="second_look_pack_contract",
            object_name="viewer_contract.second_look_plan_contract",
        )
    )
    if not isinstance(plan_contract, dict):
        return errors

    expected_values: tuple[tuple[str, Any], ...] = (
        ("schema", SECOND_LOOK_PLAN_SCHEMA),
        ("required", True),
        ("required_roles", list(SECOND_LOOK_ROLES)),
        ("carrier_kinds", list(SECOND_LOOK_CARRIER_KINDS)),
        ("risk_flags", list(SECOND_LOOK_RISK_FLAGS)),
        ("forbidden_as_sole", list(SECOND_LOOK_RISK_FLAGS)),
        ("fallback_must_reference_selected_consequence", True),
    )
    for field, expected in expected_values:
        actual = plan_contract.get(field)
        # Identity is intentional for the boolean fields: integers must not
        # masquerade as JSON booleans.
        matches = actual is expected if isinstance(expected, bool) else actual == expected
        if not matches:
            errors.append(
                issue(
                    "second_look_pack_contract",
                    "second-look contract field does not match the closed v2 contract",
                    field=field,
                    expected=expected,
                    actual=actual,
                )
            )

    scale_contract = profile.get("scale_contract")
    expected_scales = (
        _string_list(scale_contract.get("inspection_scales"))
        if isinstance(scale_contract, dict)
        else None
    )
    if not expected_scales or len(expected_scales) != len(set(expected_scales)):
        errors.append(
            issue(
                "second_look_pack_contract",
                "format_profile.scale_contract.inspection_scales must be a nonempty unique string list",
                actual=scale_contract.get("inspection_scales") if isinstance(scale_contract, dict) else None,
            )
        )
    if plan_contract.get("allowed_review_scale_ids") != expected_scales:
        errors.append(
            issue(
                "second_look_pack_contract",
                "allowed_review_scale_ids must exactly copy the selected format inspection scales",
                expected=expected_scales,
                actual=plan_contract.get("allowed_review_scale_ids"),
            )
        )
    return errors


def validate_pack_integrity(pack: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Validate the complete compact graph and format proof embedded in a pack."""

    errors: list[dict[str, Any]] = []
    pack_id = pack.get("pack_id")
    expected_id = computed_pack_id(pack)
    if not isinstance(pack_id, str) or not re.fullmatch(r"[0-9a-f]{16}", pack_id):
        errors.append(issue("pack_integrity", "pack_id must be 16 lowercase hexadecimal characters", actual=pack_id))
    if pack_id != expected_id:
        errors.append(issue("pack_integrity", "candidate pack content does not match canonical pack_id", expected=expected_id, actual=pack_id))

    if pack.get("contract_version") not in SUPPORTED_CONTRACT_VERSIONS:
        errors.append(
            issue(
                "pack_contract",
                "unsupported or missing candidate-pack contract_version",
                expected=list(SUPPORTED_CONTRACT_VERSIONS),
                actual=pack.get("contract_version"),
            )
        )

    request = pack.get("request_contract")
    if not isinstance(request, dict):
        errors.append(issue("request_contract", "request_contract must be an object"))
        request = {}
    route_id = request.get("route_id")
    if not _is_nonempty_string(route_id):
        errors.append(issue("request_contract", "route_id must be a nonempty string"))

    if not _is_nonempty_string(pack.get("negative_en")):
        errors.append(issue("pack_contract", "negative_en must be a nonempty string"))

    profile = pack.get("format_profile")
    if not isinstance(profile, dict):
        errors.append(issue("format_contract", "format_profile must be an object"))
        profile = {}
    variant_id = profile.get("variant_id")
    family_id = profile.get("family_id")
    if variant_id not in VARIANT_FAMILY:
        errors.append(issue("format_contract", "unknown format variant", actual=variant_id, known=sorted(VARIANT_FAMILY)))
    elif family_id != VARIANT_FAMILY[variant_id]:
        errors.append(issue("format_contract", "format family does not match variant", variant_id=variant_id, expected=VARIANT_FAMILY[variant_id], actual=family_id))
    for aliases in FORMAT_CONTRACT_KEY_GROUPS:
        present = [key for key in aliases if isinstance(profile.get(key), dict)]
        if not present:
            errors.append(issue("format_contract", "compact format contract group must embed an object", accepted_fields=list(aliases)))
    embedded_format_fields = _profile_required_evidence_fields(profile)
    lifecycle_evidence_types = _string_list(profile.get("required_evidence_types"))
    if lifecycle_evidence_types is None:
        errors.append(issue("format_contract", "required_evidence_types must be a string list of lifecycle qualification types"))
        lifecycle_evidence_types = []
    if not embedded_format_fields:
        errors.append(issue("format_contract", "format profile must embed required non-ratio evidence fields"))
    elif all(field in ASPECT_ONLY_KEYS for field in embedded_format_fields):
        errors.append(issue("format_contract", "format profile substitutes aspect ratio for typed format behavior", fields=embedded_format_fields))
    elif variant_id in FORMAT_REQUIRED_FIELDS:
        missing_canonical = sorted(set(FORMAT_REQUIRED_FIELDS[variant_id]) - set(embedded_format_fields))
        if missing_canonical:
            errors.append(issue("format_contract", "embedded format requirements omit canonical typed evidence", missing=missing_canonical))
    leaked_lifecycle_fields = sorted(
        field
        for field in embedded_format_fields
        if field in set(lifecycle_evidence_types)
        or field in NON_COMPOSITION_EVIDENCE_KEYS
        or POST_RENDER_EVIDENCE_KEY_PATTERN.search(field)
    )
    if leaked_lifecycle_fields:
        errors.append(
            issue(
                "format_contract",
                "post-render or lifecycle qualification types cannot be required composed-prompt fields",
                fields=leaked_lifecycle_fields,
            )
        )

    grammar = pack.get("visual_grammar")
    if not isinstance(grammar, dict):
        errors.append(issue("visual_grammar", "visual_grammar must be an object"))
        grammar = {}
    if not _is_nonempty_string(grammar.get("topic_id")):
        errors.append(issue("visual_grammar", "visual_grammar.topic_id must be a nonempty string"))
    elif route_id and grammar.get("topic_id") != route_id:
        errors.append(issue("visual_grammar", "visual_grammar topic must match request route", route_id=route_id, topic_id=grammar.get("topic_id")))
    if not _is_nonempty_string(grammar.get("family_id")):
        errors.append(issue("visual_grammar", "visual_grammar.family_id must be a nonempty string"))
    raw_nodes = grammar.get("runtime_nodes")
    if not isinstance(raw_nodes, list) or any(not isinstance(node, dict) for node in raw_nodes):
        errors.append(issue("visual_grammar", "runtime_nodes must be a list of objects"))
        raw_nodes = []
    nodes = [node for node in raw_nodes if isinstance(node, dict)]
    if not 1 <= len(nodes) <= 3:
        errors.append(issue("visual_grammar", "runtime bundle must contain one to three nodes", count=len(nodes)))

    node_ids = [str(node.get("id") or "") for node in nodes]
    if any(not node_id for node_id in node_ids):
        errors.append(issue("visual_grammar", "every runtime node must have a nonempty id"))
    if len(node_ids) != len(set(node_ids)):
        errors.append(issue("visual_grammar", "runtime node ids must be unique", ids=node_ids))

    primary_ids: list[str] = []
    support_ids: list[str] = []
    available_evidence: set[str] = set()
    for node in nodes:
        node_id = str(node.get("id") or "")
        node_type = node.get("node_type")
        role = node.get("selected_role")
        if node_type != "visual_atom":
            errors.append(issue("typed_candidate_boundary", "selected runtime node is not a visual_atom", node_id=node_id, node_type=node_type))
        if role == "primary":
            primary_ids.append(node_id)
        elif role == "support":
            support_ids.append(node_id)
        else:
            errors.append(issue("visual_grammar", "runtime node selected_role must be primary or support", node_id=node_id, selected_role=role))
        if not _is_nonempty_string(node.get("definition")):
            errors.append(issue("visual_grammar", "runtime node must embed a nonempty definition", node_id=node_id))
        evidence_types = _string_list(node.get("observable_evidence_types"))
        if not evidence_types:
            errors.append(issue("visual_grammar", "runtime node must embed observable evidence types", node_id=node_id))
        else:
            available_evidence.update(evidence_types)
            phase_invalid = sorted(
                evidence_type
                for evidence_type in evidence_types
                if evidence_type in NON_COMPOSITION_EVIDENCE_KEYS
                or POST_RENDER_EVIDENCE_KEY_PATTERN.search(evidence_type)
            )
            if phase_invalid:
                errors.append(issue("visual_grammar", "visual atoms cannot expose post-render qualification evidence", node_id=node_id, evidence_types=phase_invalid))
        format_families = _string_list(node.get("format_family_ids"))
        if not format_families:
            errors.append(issue("visual_grammar", "runtime node must embed applicable format families", node_id=node_id))
        elif family_id not in format_families:
            errors.append(issue("visual_grammar", "runtime node is not applicable to the selected format family", node_id=node_id, family_id=family_id, allowed=format_families))

    if len(primary_ids) != 1:
        errors.append(issue("sparse_visual_bundle", "runtime bundle must have exactly one primary visual atom", primary_ids=primary_ids))
    if len(support_ids) > 2:
        errors.append(issue("sparse_visual_bundle", "runtime bundle may expose at most two support visual atoms", support_ids=support_ids))
    if grammar.get("primary_runtime_id") != (primary_ids[0] if len(primary_ids) == 1 else None):
        errors.append(issue("sparse_visual_bundle", "primary_runtime_id does not match the primary runtime node", declared=grammar.get("primary_runtime_id"), actual=primary_ids))
    declared_supports = _string_list(grammar.get("support_runtime_ids"))
    if declared_supports is None or set(declared_supports) != set(support_ids) or len(declared_supports) != len(support_ids):
        errors.append(issue("sparse_visual_bundle", "support_runtime_ids do not exactly match support runtime nodes", declared=grammar.get("support_runtime_ids"), actual=support_ids))
    max_support = grammar.get("max_support_cues")
    if isinstance(max_support, bool) or not isinstance(max_support, int) or not 0 <= max_support <= 2:
        errors.append(issue("sparse_visual_bundle", "max_support_cues must be an integer from zero to two", actual=max_support))
    elif len(support_ids) > max_support:
        errors.append(issue("sparse_visual_bundle", "selected support count exceeds max_support_cues", support_count=len(support_ids), max_support_cues=max_support))

    required_visual_evidence = _string_list(grammar.get("required_evidence_types"))
    if not required_visual_evidence:
        errors.append(issue("visual_grammar", "visual_grammar must embed required evidence types"))
    else:
        phase_invalid = sorted(
            evidence_type
            for evidence_type in required_visual_evidence
            if evidence_type in NON_COMPOSITION_EVIDENCE_KEYS
            or POST_RENDER_EVIDENCE_KEY_PATTERN.search(evidence_type)
        )
        if phase_invalid:
            errors.append(issue("visual_grammar", "post-render qualification cannot be required as pre-render visual evidence", evidence_types=phase_invalid))
        unavailable = sorted(set(required_visual_evidence) - available_evidence)
        if unavailable:
            errors.append(issue("visual_grammar", "required evidence is not supplied by the selected runtime nodes", unavailable=unavailable, available=sorted(available_evidence)))

    compatible_ids = _string_list(grammar.get("compatible_edge_ids"))
    if compatible_ids is None:
        errors.append(issue("compatibility_edge", "compatible_edge_ids must be a string list"))
        compatible_ids = []
    if len(nodes) > 1 and not compatible_ids:
        errors.append(issue("compatibility_edge", "multi-node bundle requires a declared compatibility edge"))

    edge = grammar.get("selected_edge")
    if not isinstance(edge, dict):
        errors.append(issue("compatibility_edge", "visual_grammar must embed selected_edge"))
    else:
        edge_id = edge.get("id")
        if not _is_nonempty_string(edge_id) or edge_id not in compatible_ids:
            errors.append(issue("compatibility_edge", "selected edge id is absent from compatible_edge_ids", edge_id=edge_id, compatible_edge_ids=compatible_ids))
        if edge.get("route_id") != route_id:
            errors.append(issue("compatibility_edge", "selected edge route does not match request route", expected=route_id, actual=edge.get("route_id")))
        edge_families = _string_list(edge.get("format_family_ids"))
        if not edge_families or family_id not in edge_families:
            errors.append(issue("compatibility_edge", "selected edge is not applicable to the format family", family_id=family_id, allowed=edge.get("format_family_ids")))
        if edge.get("primary_node_id") != grammar.get("primary_runtime_id"):
            errors.append(issue("compatibility_edge", "selected edge primary does not match visual_grammar", edge_primary=edge.get("primary_node_id"), grammar_primary=grammar.get("primary_runtime_id")))
        edge_supports = _string_list(edge.get("support_node_ids"))
        if edge_supports is None or set(edge_supports) != set(support_ids) or len(edge_supports) != len(support_ids):
            errors.append(issue("compatibility_edge", "selected edge supports do not exactly match runtime supports", edge_supports=edge.get("support_node_ids"), runtime_supports=support_ids))
        minimum = edge.get("minimum_supports")
        maximum = edge.get("maximum_supports")
        if isinstance(minimum, bool) or not isinstance(minimum, int) or isinstance(maximum, bool) or not isinstance(maximum, int) or not (0 <= minimum <= maximum <= 2):
            errors.append(issue("compatibility_edge", "selected edge support bounds must satisfy 0 <= minimum <= maximum <= 2", minimum=minimum, maximum=maximum))
        elif not minimum <= len(support_ids) <= maximum:
            errors.append(issue("compatibility_edge", "selected support count is outside selected edge bounds", support_count=len(support_ids), minimum=minimum, maximum=maximum))
        edge_evidence = _string_list(edge.get("required_evidence_types"))
        if not edge_evidence:
            errors.append(issue("compatibility_edge", "selected edge must embed required evidence types"))
        elif required_visual_evidence and not set(edge_evidence).issubset(set(required_visual_evidence)):
            errors.append(issue("compatibility_edge", "selected edge evidence is absent from visual_grammar requirements", edge_required=edge_evidence, grammar_required=required_visual_evidence))

    expected_ids = expected_chosen_candidate_ids(pack)
    composition_contract = pack.get("composition_contract")
    if not isinstance(composition_contract, dict):
        errors.append(issue("composition_contract", "composition_contract must be an object"))
    else:
        declared_ids = _string_list(composition_contract.get("required_chosen_candidate_ids"))
        if declared_ids is None or set(declared_ids) != set(expected_ids) or len(declared_ids) != len(expected_ids):
            errors.append(issue("composition_contract", "required_chosen_candidate_ids do not exactly match the compact pack selection", declared=composition_contract.get("required_chosen_candidate_ids"), expected=expected_ids))

    authorial_contract = pack.get("authorial_contract")
    if not isinstance(authorial_contract, dict):
        errors.append(issue("authorial_contract", "authorial_contract must be an object"))
    else:
        authorial_required = _string_list(authorial_contract.get("required_fields"))
        if authorial_required is None or not set(AUTHORIAL_REQUIRED_FIELDS).issubset(authorial_required):
            errors.append(issue("authorial_contract", "authorial_contract must embed all canonical authorial evidence fields", required=list(AUTHORIAL_REQUIRED_FIELDS), actual=authorial_contract.get("required_fields")))
        if not isinstance(authorial_contract.get("creative_development_required"), bool):
            errors.append(issue("authorial_contract", "creative_development_required must be boolean"))

    viewer_contract = pack.get("viewer_contract")
    if not isinstance(viewer_contract, dict):
        errors.append(issue("viewer_contract", "viewer_contract must be an object"))
    else:
        viewer_required = _string_list(viewer_contract.get("required_fields"))
        if viewer_required is None or not set(VIEWER_REQUIRED_FIELDS).issubset(viewer_required):
            errors.append(issue("viewer_contract", "viewer_contract must embed all canonical causal viewer fields", required=list(VIEWER_REQUIRED_FIELDS), actual=viewer_contract.get("required_fields")))

    safety = pack.get("safety")
    if not isinstance(safety, dict) or safety.get("status") != "pass" or safety.get("requires_user_approval") is True:
        errors.append(issue("safety_contract", "candidate pack safety must already be pass with no approval wait", safety=safety))

    guard = pack.get("guard_contract")
    if not isinstance(guard, dict):
        errors.append(issue("guard_contract", "guard_contract must be an object"))
    else:
        if _string_list(guard.get("guard_node_ids")) is None:
            errors.append(issue("guard_contract", "guard_node_ids must be a string list"))
        if _string_list(guard.get("router_node_ids")) is None:
            errors.append(issue("guard_contract", "router_node_ids must be a string list"))

    errors.extend(_second_look_pack_contract_failures(pack, profile))

    return errors


def _evidence_leaf_values(value: Any, path: str = "") -> Iterator[tuple[str, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            yield from _evidence_leaf_values(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _evidence_leaf_values(child, f"{path}[{index}]")
    else:
        yield path, value


def _phrase_is_literal(prompt_en: str, value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and value in prompt_en


def audit_literal_evidence(
    prompt_en: str,
    section_name: str,
    section: Any,
    *,
    skipped_roots: Iterable[str] = (),
) -> list[dict[str, Any]]:
    """Require every visible-evidence scalar to be an exact prompt substring."""

    failures: list[dict[str, Any]] = []
    if not isinstance(section, dict):
        return [issue("evidence_shape", "evidence section must be an object", section=section_name)]
    skipped = set(skipped_roots)
    visible_section = {key: value for key, value in section.items() if key not in skipped}
    for path, value in _evidence_leaf_values(visible_section):
        full_path = f"{section_name}.{path}" if path else section_name
        if not isinstance(value, str):
            failures.append(issue("literal_evidence", "visible evidence leaf must be a string", field=full_path, actual_type=type(value).__name__))
        elif not value.strip():
            failures.append(issue("literal_evidence", "visible evidence phrase must be nonempty", field=full_path))
        elif value not in prompt_en:
            failures.append(issue("literal_evidence", "evidence phrase is not an exact literal substring of prompt_en", field=full_path, phrase=value))
    return failures


def _required_phrase_failures(
    section_name: str,
    section: Mapping[str, Any],
    required_fields: Iterable[str],
    prompt_en: str,
) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    for field in dict.fromkeys(required_fields):
        value = section.get(field)
        if not _is_nonempty_string(value):
            failures.append(issue("required_evidence", "required evidence phrase is missing", section=section_name, field=field))
        elif value not in prompt_en:
            failures.append(issue("literal_evidence", "required evidence phrase is not an exact literal substring of prompt_en", section=section_name, field=field, phrase=value))
    return failures


def _authorial_concreteness_failures(authorial: Mapping[str, Any]) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    generic_only = {
        "beautiful",
        "cinematic",
        "detailed",
        "high quality",
        "masterpiece",
        "anime style",
        "stylized",
        "atmospheric",
    }
    for field in AUTHORIAL_REQUIRED_FIELDS:
        value = authorial.get(field)
        if not _is_nonempty_string(value):
            continue
        normalized = " ".join(re.findall(r"[A-Za-z0-9]+", str(value).casefold()))
        word_count = len(normalized.split())
        if normalized in generic_only or word_count < 3:
            failures.append(issue("authorial_grammar", "authorial evidence must state a concrete decision, not a style adjective", field=field, phrase=value))
    return failures


def _strict_chosen_ids(raw: Any) -> tuple[list[str], list[dict[str, Any]]]:
    failures: list[dict[str, Any]] = []
    if not isinstance(raw, list):
        return [], [issue("chosen_candidate_ids", "chosen_candidate_ids must be a list of strings")]
    ids: list[str] = []
    for index, value in enumerate(raw):
        if not _is_nonempty_string(value):
            failures.append(issue("chosen_candidate_ids", "candidate id must be a nonempty string", index=index, actual=value))
        else:
            ids.append(str(value))
    if len(ids) != len(set(ids)):
        failures.append(issue("chosen_candidate_ids", "chosen_candidate_ids must not contain duplicates", ids=ids))
    return ids, failures


def _mandatory_intent_failures(pack: Mapping[str, Any], composed: Mapping[str, Any], prompt_en: str) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    request = _mapping(pack.get("request_contract"))
    intents = request.get("mandatory_intents") or []
    if not isinstance(intents, list):
        return [issue("mandatory_intent", "request_contract.mandatory_intents must be a list")]
    assertions = composed.get("coverage_assertions", {})
    if not isinstance(assertions, dict):
        return [issue("coverage_assertions", "coverage_assertions must be an object when supplied")]
    known_keys: set[str] = set()
    visual_evidence = _mapping(composed.get("visual_evidence"))
    for intent in intents:
        evidence_key = ""
        if isinstance(intent, str):
            text = intent
            terms = [intent]
        elif isinstance(intent, dict):
            text = str(intent.get("text") or intent.get("id") or "")
            evidence_key = str(intent.get("evidence_key") or "")
            raw_terms = _string_list(intent.get("audit_terms"))
            terms = raw_terms or ([text] if text else [])
        else:
            failures.append(issue("mandatory_intent", "mandatory intent must be a string or object", actual=intent))
            continue
        if not text:
            failures.append(issue("mandatory_intent", "mandatory intent must have a nonempty identity"))
            continue
        known_keys.add(text)
        asserted = assertions.get(text)
        assertion_phrases = [asserted] if isinstance(asserted, str) else (_string_list(asserted) or [])
        for phrase in assertion_phrases:
            if phrase not in prompt_en:
                failures.append(issue("coverage_assertions", "asserted mandatory-intent phrase is not literal in prompt_en", intent=text, phrase=phrase))
        bound_evidence = visual_evidence.get(evidence_key) if evidence_key else None
        evidence_covers = _phrase_is_literal(prompt_en, bound_evidence)
        if evidence_key and not evidence_covers:
            failures.append(issue("mandatory_intent", "mandatory-intent evidence_key has no literal visual_evidence phrase", intent=text, evidence_key=evidence_key))
        accepted = [term for term in terms if isinstance(term, str) and text_contains_term(prompt_en, term)]
        if not accepted and not assertion_phrases and not evidence_covers:
            failures.append(issue("mandatory_intent", "mandatory visible intent is absent from prompt_en", intent=text, accepted_terms=terms))
    for key in assertions:
        if str(key) not in known_keys:
            failures.append(issue("coverage_assertions", "assertion key is not a mandatory intent", intent=key))
    return failures


def _reference_boundary_failures(composed: Mapping[str, Any], prompt_en: str, pack: Mapping[str, Any]) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    boundary = composed.get("reference_boundary")
    if not isinstance(boundary, dict):
        return [issue("reference_boundary", "reference_boundary must be an object")]
    if boundary.get("original_design") is not True:
        failures.append(issue("reference_boundary", "original_design must be true"))
    for key in ("named_style_references", "protected_ip_references"):
        value = boundary.get(key)
        if not isinstance(value, list):
            failures.append(issue("reference_boundary", f"{key} must be a list"))
        elif value:
            failures.append(issue("reference_boundary", f"{key} must be empty", references=value))

    for pattern in NAMED_STYLE_PATTERNS:
        match = re.search(pattern, prompt_en, flags=re.IGNORECASE)
        if match:
            failures.append(issue("named_style_reference", "prompt uses a named-artist/studio style proof", excerpt=match.group(0)))
    for pattern in PROTECTED_IP_PATTERNS:
        match = re.search(pattern, prompt_en, flags=re.IGNORECASE)
        if match:
            failures.append(issue("protected_ip_reference", "prompt contains a protected-IP or logo reference", excerpt=match.group(0)))

    guard = _mapping(pack.get("guard_contract"))
    for key in ("forbidden_prompt_terms", "named_style_terms", "protected_ip_terms"):
        terms = _string_list(guard.get(key)) or []
        for term in terms:
            if term.casefold() in prompt_en.casefold():
                failures.append(issue("guard_contract", "prompt contains a pack-declared forbidden reference", category=key, term=term))
    return failures


def _policy_language_failures(prompt_en: str) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    for pattern in UNIVERSAL_INFERENCE_PATTERNS:
        matches = _nonnegated_matches(pattern, prompt_en)
        if matches:
            match = matches[0]
            failures.append(issue("universal_inference", "prompt makes a universal color, shape, or cultural inference", excerpt=match.group(0)))
    for pattern in OUTCOME_CLAIM_PATTERNS:
        matches = _nonnegated_matches(pattern, prompt_en)
        if matches:
            match = matches[0]
            failures.append(issue("viewer_outcome_claim", "viewer response claim is not visible evidence", excerpt=match.group(0)))
    return failures


def _phase_boundary_failures(
    pack: Mapping[str, Any],
    composed: Mapping[str, Any],
    prompt_en: str,
) -> list[dict[str, Any]]:
    """Reject post-render qualification claims in a pre-render composition."""

    failures: list[dict[str, Any]] = []
    profile = _mapping(pack.get("format_profile"))
    lifecycle_types = set(_string_list(profile.get("required_evidence_types")) or [])
    composition_fields = set(_profile_required_evidence_fields(profile))
    lifecycle_only = lifecycle_types - composition_fields

    for section_name in (
        "visual_evidence",
        "authorial_grammar",
        "viewer_evidence",
        "format_evidence",
    ):
        section = composed.get(section_name)
        if not isinstance(section, dict):
            continue
        for path, _value in _evidence_leaf_values(section):
            segments = [segment for segment in re.split(r"[.\[\]]+", path) if segment]
            for segment in segments:
                if segment in lifecycle_only or POST_RENDER_EVIDENCE_KEY_PATTERN.search(segment):
                    failures.append(
                        issue(
                            "phase_boundary",
                            "post-render or lifecycle qualification field cannot be claimed by a pre-render composed prompt",
                            section=section_name,
                            field=path,
                            lifecycle_field=segment,
                        )
                    )
                    break

    for pattern in POST_RENDER_CLAIM_PATTERNS:
        matches = _nonnegated_matches(pattern, prompt_en)
        if matches:
            failures.append(
                issue(
                    "phase_boundary",
                    "prompt claims a completed pixel or render review before image generation",
                    excerpt=matches[0].group(0),
                )
            )
    return failures


def _photo_dominance_failures(pack: Mapping[str, Any], prompt_en: str) -> list[dict[str, Any]]:
    request = _mapping(pack.get("request_contract"))
    request_text = str(request.get("request_text") or "")
    hybrid_requested = request.get("hybrid_medium_requested") is True or bool(
        re.search(r"\b(?:hybrid medium|photo[- ]illustration|photographic illustration|mixed photo and illustration)\b", request_text, flags=re.IGNORECASE)
    )
    if hybrid_requested:
        return []

    categories: dict[str, list[str]] = {}
    patterns: dict[str, str] = {
        "photo_medium": r"\b(?:photorealistic|photo-realistic|photographic|photograph|photo shoot|photo portrait)\b",
        "camera_body": r"\b(?:DSLR camera|mirrorless camera|shot on|captured (?:on|with)|(?:Leica|Canon|Nikon|Hasselblad)(?:\s+camera)?)\b",
        "lens_formula": r"\b(?:bokeh|depth of field|focal length|\d{2,3}\s*mm(?:\s+lens)?|telephoto lens|wide[- ]angle lens|macro lens)\b",
        "exposure_formula": r"\b(?:ISO\s*\d+|f\s*/\s*\d|shutter speed|aperture)\b",
    }
    for category, pattern in patterns.items():
        hits = [match.group(0) for match in re.finditer(pattern, prompt_en, flags=re.IGNORECASE)]
        if hits:
            categories[category] = hits
    begins_as_photo = re.search(r"^\s*(?:a |an )?(?:photorealistic |photographic )?(?:photo|photograph)\b", prompt_en, flags=re.IGNORECASE)
    equipment_formula = "exposure_formula" in categories or (
        "camera_body" in categories and "lens_formula" in categories
    )
    illustration_present = bool(re.search(r"\b(?:illustration|drawn|painted|inked|linework|cel[- ]shaded|artwork)\b", prompt_en, flags=re.IGNORECASE))
    if begins_as_photo or equipment_formula or (len(categories) >= 2 and not illustration_present):
        return [issue("photographic_dominance", "camera, lens, or photoreal capture formula dominates an illustration prompt without an explicit hybrid-medium request", categories=categories)]
    return []


def _motif_failures(pack: Mapping[str, Any], composed: Mapping[str, Any], prompt_en: str) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    authorial = _mapping(composed.get("authorial_grammar"))
    visual = _mapping(composed.get("visual_evidence"))
    motif_values: list[str] = []
    state_values: list[str] = []
    for section in (authorial, visual):
        for key, value in section.items():
            lowered = str(key).lower()
            values = [value] if isinstance(value, str) else (_string_list(value) or [])
            if "motif_family" in lowered:
                motif_values.extend(values)
            if "motif" in lowered and ("state" in lowered or "placement" in lowered):
                state_values.extend(values)
    unique_motifs = list(dict.fromkeys(motif_values))
    if len(unique_motifs) > 1:
        failures.append(issue("motif_budget", "at most one motif family may be claimed", motif_families=unique_motifs))
    for pattern in DECORATIVE_SOUP_PATTERNS:
        matches = _nonnegated_matches(pattern, prompt_en)
        if matches:
            match = matches[0]
            failures.append(issue("decorative_motif_soup", "decorative motif accumulation is not a causal visual metaphor", excerpt=match.group(0)))

    # A declared list of three or more comma-separated symbols is also a
    # high-confidence soup signal, regardless of whether it uses the word art.
    for match in re.finditer(r"\b(?:motifs?|symbols?|icons?)\s+(?:of|:)\s+([^.!?]{1,140})", prompt_en, flags=re.IGNORECASE):
        items = [part.strip() for part in re.split(r",|\band\b|&", match.group(1), flags=re.IGNORECASE) if part.strip()]
        if len(items) >= 3:
            failures.append(issue("decorative_motif_soup", "prompt stacks three or more motif subjects without a single-family state rule", excerpt=match.group(0), item_count=len(items)))

    route_id = str(_mapping(pack.get("request_contract")).get("route_id") or "")
    if route_id == "recurring_motif_visual_metaphor":
        if len(unique_motifs) != 1:
            failures.append(issue("motif_budget", "recurring-motif route requires exactly one literal motif-family phrase", motif_families=unique_motifs))
        if len(set(state_values)) < 2:
            failures.append(issue("motif_state_change", "recurring-motif route requires two distinct literal states or placements tied to the event", states=state_values))
    return failures


def _format_failures(pack: Mapping[str, Any], composed: Mapping[str, Any], prompt_en: str) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    profile = _mapping(pack.get("format_profile"))
    variant = str(profile.get("variant_id") or "")
    evidence = composed.get("format_evidence")
    if not isinstance(evidence, dict):
        return [issue("format_evidence", "format_evidence must be an object")]
    required = list(FORMAT_REQUIRED_FIELDS.get(variant, ()))
    required.extend(_profile_required_evidence_fields(profile))
    failures.extend(_required_phrase_failures("format_evidence", evidence, required, prompt_en))
    non_ratio_keys = [key for key, value in evidence.items() if key not in ASPECT_ONLY_KEYS and _is_nonempty_string(value)]
    if not non_ratio_keys:
        failures.append(issue("aspect_only_format", "format evidence contains only an aspect ratio or no typed behavior", keys=sorted(evidence)))
    for pattern, label in FORMAT_FORBIDDEN_PATTERNS.get(variant, ()):
        matches = _nonnegated_matches(pattern, prompt_en)
        if matches:
            match = matches[0]
            failures.append(issue("format_substitution", f"{variant} contains forbidden {label}", excerpt=match.group(0)))
    return failures


def _creative_development_failures(pack: Mapping[str, Any], composed: Mapping[str, Any], prompt_en: str) -> list[dict[str, Any]]:
    contract = _mapping(pack.get("authorial_contract"))
    if contract.get("creative_development_required") is not True:
        return []
    failures: list[dict[str, Any]] = []
    authorial = _mapping(composed.get("authorial_grammar"))
    development = authorial.get("creative_development")
    if not isinstance(development, dict):
        return [issue("creative_development", "high-creativity pack requires authorial_grammar.creative_development")]
    rejected = _string_list(development.get("rejected_ordinary_answers"))
    if not rejected or len(set(rejected)) < 3:
        failures.append(issue("creative_development", "at least three distinct ordinary first answers must be rejected", answers=development.get("rejected_ordinary_answers")))
    proposals = development.get("proposals")
    if not isinstance(proposals, list) or len(proposals) < 4 or any(not isinstance(item, dict) for item in proposals):
        failures.append(issue("creative_development", "at least four structured proposals are required"))
        proposals = []
    proposal_ids: list[str] = []
    operator_ids: list[str] = []
    selected_flags: list[str] = []
    by_id: dict[str, dict[str, Any]] = {}
    for proposal in proposals:
        proposal_id = str(proposal.get("id") or "")
        operator_id = str(proposal.get("operator_id") or "")
        if not proposal_id or proposal_id in by_id:
            failures.append(issue("creative_development", "proposal ids must be nonempty and unique", proposal_id=proposal_id))
        else:
            by_id[proposal_id] = proposal
        proposal_ids.append(proposal_id)
        operator_ids.append(operator_id)
        if proposal.get("selected") is True:
            selected_flags.append(proposal_id)
        for field in ("familiar_anchor_phrase", "changed_rule_phrase", "aboutness", "signature_phrase"):
            if not _is_nonempty_string(proposal.get(field)):
                failures.append(issue("creative_development", "proposal field must be a nonempty scalar", proposal_id=proposal_id, field=field))
        consequences = _string_list(proposal.get("visible_consequence_phrases"))
        if not consequences or len(set(consequences)) < 2:
            failures.append(issue("creative_development", "proposal needs at least two distinct visible consequences", proposal_id=proposal_id))
    if len(set(operator_ids)) < min(4, len(proposals)):
        failures.append(issue("creative_development", "the first four proposals must use distinct operator IDs", operator_ids=operator_ids))
    selected_id = development.get("selected_proposal_id")
    if selected_flags and (len(selected_flags) != 1 or selected_id != selected_flags[0]):
        failures.append(issue("creative_development", "exactly one selected proposal must agree with selected_proposal_id", selected_flags=selected_flags, selected_proposal_id=selected_id))
    if not _is_nonempty_string(selected_id) or selected_id not in by_id:
        failures.append(issue("creative_development", "selected_proposal_id must name exactly one proposal", selected_proposal_id=selected_id))
        return failures
    selected = by_id[str(selected_id)]
    reveal_phrase = selected.get("first_second_reveal_phrase") or selected.get("reveal_phrase")
    if not _is_nonempty_string(reveal_phrase):
        failures.append(issue("creative_development", "selected proposal needs one first-to-second-look reveal phrase", selected_proposal_id=selected_id))
    selected_phrases = [
        selected.get("familiar_anchor_phrase"),
        selected.get("changed_rule_phrase"),
        reveal_phrase,
        selected.get("signature_phrase"),
        *(_string_list(selected.get("visible_consequence_phrases")) or []),
    ]
    for phrase in selected_phrases:
        if _is_nonempty_string(phrase) and phrase not in prompt_en:
            failures.append(issue("creative_development", "selected proposal evidence is not literal in prompt_en", selected_proposal_id=selected_id, phrase=phrase))
    for proposal_id, proposal in by_id.items():
        if proposal_id == selected_id:
            continue
        signature = proposal.get("signature_phrase")
        if _is_nonempty_string(signature) and signature in prompt_en:
            failures.append(issue("creative_development", "unselected proposal signature leaked into prompt_en", proposal_id=proposal_id, signature=signature))
    return failures


def _carrier_risk_failures(
    role: str,
    carrier: Mapping[str, Any],
) -> tuple[list[str], list[dict[str, Any]]]:
    failures: list[dict[str, Any]] = []
    raw_flags = carrier.get("risk_flags")
    flags = _string_list(raw_flags)
    if flags is None:
        failures.append(
            issue(
                "second_look_risk_flags",
                "carrier risk_flags must be a list of nonempty strings",
                role=role,
                actual=raw_flags,
            )
        )
        flags = []
    if len(flags) != len(set(flags)):
        failures.append(
            issue(
                "second_look_risk_flags",
                "carrier risk_flags must be unique",
                role=role,
                actual=flags,
            )
        )
    unknown = sorted(set(flags) - set(SECOND_LOOK_RISK_FLAGS))
    if unknown:
        failures.append(
            issue(
                "second_look_risk_flags",
                "carrier declares a risk flag outside the closed v2 enum",
                role=role,
                unknown=unknown,
                allowed=list(SECOND_LOOK_RISK_FLAGS),
            )
        )

    linked_text = ". ".join(
        str(carrier.get(field) or "")
        for field in ("carrier_phrase", "protected_locus_phrase", "consequence_phrase")
    )
    for risk_flag, patterns in SECOND_LOOK_LINKED_RISK_PATTERNS.items():
        if risk_flag in flags:
            continue
        match = next(
            (
                found
                for pattern in patterns
                if (found := re.search(pattern, linked_text, flags=re.IGNORECASE)) is not None
            ),
            None,
        )
        if match is not None:
            failures.append(
                issue(
                    "second_look_risk_backstop",
                    "linked carrier phrases contain a narrowly recognized risk that was not declared",
                    role=role,
                    risk_flag=risk_flag,
                    excerpt=match.group(0),
                )
            )
    return flags, failures


def _second_look_plan_failures(
    pack: Mapping[str, Any],
    composed: Mapping[str, Any],
    prompt_en: str,
) -> list[dict[str, Any]]:
    """Audit the v2 plan as pre-render evidence, never as pixel proof."""

    if pack.get("contract_version") != CONTRACT_VERSION_V2:
        return []

    failures: list[dict[str, Any]] = []
    if composed.get("schema") != COMPOSED_PROMPT_SCHEMA_V2:
        failures.append(
            issue(
                "second_look_plan",
                "v2 candidate pack requires the v2 composed-prompt schema",
                expected=COMPOSED_PROMPT_SCHEMA_V2,
                actual=composed.get("schema"),
            )
        )

    plan = composed.get("second_look_plan")
    failures.extend(
        _exact_object_keys(
            plan,
            SECOND_LOOK_PLAN_KEYS,
            check="second_look_plan",
            object_name="second_look_plan",
        )
    )
    if not isinstance(plan, dict):
        return failures
    if plan.get("schema") != SECOND_LOOK_PLAN_SCHEMA:
        failures.append(
            issue(
                "second_look_plan",
                "second_look_plan schema does not match the pack contract",
                expected=SECOND_LOOK_PLAN_SCHEMA,
                actual=plan.get("schema"),
            )
        )

    reveal_phrase = plan.get("reveal_phrase")
    if not _is_nonempty_string(reveal_phrase):
        failures.append(issue("second_look_plan", "reveal_phrase must be a nonempty string"))
    elif reveal_phrase not in prompt_en:
        failures.append(
            issue(
                "literal_evidence",
                "second-look reveal is not an exact literal substring of prompt_en",
                field="second_look_plan.reveal_phrase",
                phrase=reveal_phrase,
            )
        )
    viewer_reveal = _mapping(composed.get("viewer_evidence")).get("second_look_reveal_phrase")
    if reveal_phrase != viewer_reveal:
        failures.append(
            issue(
                "second_look_plan",
                "second-look plan reveal must exactly match viewer_evidence.second_look_reveal_phrase",
                expected=viewer_reveal,
                actual=reveal_phrase,
            )
        )

    review_scales = _string_list(plan.get("review_scale_ids"))
    if not review_scales:
        failures.append(
            issue(
                "second_look_review_scales",
                "review_scale_ids must be a nonempty string list",
                actual=plan.get("review_scale_ids"),
            )
        )
        review_scales = []
    elif len(review_scales) != len(set(review_scales)):
        failures.append(
            issue(
                "second_look_review_scales",
                "review_scale_ids must not contain duplicates",
                actual=review_scales,
            )
        )
    plan_contract = _mapping(_mapping(pack.get("viewer_contract")).get("second_look_plan_contract"))
    allowed_scales = _string_list(plan_contract.get("allowed_review_scale_ids")) or []
    unknown_scales = sorted(set(review_scales) - set(allowed_scales))
    if unknown_scales:
        failures.append(
            issue(
                "second_look_review_scales",
                "review_scale_ids must be a subset of the pack-declared inspection scales",
                unknown=unknown_scales,
                allowed=allowed_scales,
            )
        )

    carriers: dict[str, dict[str, Any]] = {}
    declared_risks: dict[str, list[str]] = {}
    for role in SECOND_LOOK_ROLES:
        carrier = plan.get(role)
        failures.extend(
            _exact_object_keys(
                carrier,
                SECOND_LOOK_CARRIER_KEYS,
                check="second_look_carrier",
                object_name=f"second_look_plan.{role}",
            )
        )
        if not isinstance(carrier, dict):
            continue
        carriers[role] = carrier
        carrier_kind = carrier.get("carrier_kind")
        if carrier_kind not in SECOND_LOOK_CARRIER_KINDS:
            failures.append(
                issue(
                    "second_look_carrier",
                    "carrier_kind is outside the closed v2 enum",
                    role=role,
                    actual=carrier_kind,
                    allowed=list(SECOND_LOOK_CARRIER_KINDS),
                )
            )
        for field in ("carrier_phrase", "protected_locus_phrase", "consequence_phrase"):
            phrase = carrier.get(field)
            if not _is_nonempty_string(phrase):
                failures.append(
                    issue(
                        "second_look_carrier",
                        "carrier phrase field must be a nonempty string",
                        role=role,
                        field=field,
                    )
                )
            elif phrase not in prompt_en:
                failures.append(
                    issue(
                        "literal_evidence",
                        "second-look carrier phrase is not an exact literal substring of prompt_en",
                        field=f"second_look_plan.{role}.{field}",
                        phrase=phrase,
                    )
                )
        flags, risk_failures = _carrier_risk_failures(role, carrier)
        declared_risks[role] = flags
        failures.extend(risk_failures)

    primary = carriers.get("primary_carrier")
    fallback = carriers.get("fallback_carrier")
    if primary is not None and fallback is not None:
        for field in ("carrier_phrase", "protected_locus_phrase", "consequence_phrase"):
            primary_value = _normalized_contract_phrase(primary.get(field))
            fallback_value = _normalized_contract_phrase(fallback.get(field))
            if primary_value and primary_value == fallback_value:
                failures.append(
                    issue(
                        "second_look_distinctness",
                        "primary and fallback carrier evidence must remain distinct after normalization",
                        field=field,
                        primary=primary.get(field),
                        fallback=fallback.get(field),
                    )
                )
        fallback_risks = declared_risks.get("fallback_carrier", [])
        if fallback_risks:
            failures.append(
                issue(
                    "second_look_fallback",
                    "fallback_carrier.risk_flags must be empty",
                    actual=fallback_risks,
                )
            )
        primary_risks = declared_risks.get("primary_carrier", [])
        if primary_risks and primary.get("carrier_kind") == fallback.get("carrier_kind"):
            failures.append(
                issue(
                    "second_look_fallback",
                    "a risky primary carrier requires a safe fallback of a different carrier kind",
                    primary_kind=primary.get("carrier_kind"),
                    fallback_kind=fallback.get("carrier_kind"),
                    primary_risk_flags=primary_risks,
                )
            )

    authorial_contract = _mapping(pack.get("authorial_contract"))
    creative_required = authorial_contract.get("creative_development_required") is True
    selected_id = plan.get("selected_proposal_id")
    primary_consequence = primary.get("consequence_phrase") if primary is not None else None
    fallback_consequence = fallback.get("consequence_phrase") if fallback is not None else None
    if (
        _is_nonempty_string(primary_consequence)
        and _is_nonempty_string(fallback_consequence)
        and _normalized_contract_phrase(primary_consequence)
        == _normalized_contract_phrase(fallback_consequence)
    ):
        # Keep this explicit proposal-level failure in addition to the carrier
        # pair failure: the two planned realizations must implement two actual
        # consequences, not two labels for one consequence.
        failures.append(
            issue(
                "second_look_proposal_binding",
                "primary and fallback must reference two distinct visible consequences",
                primary=primary_consequence,
                fallback=fallback_consequence,
            )
        )

    if not creative_required:
        if selected_id is not None:
            failures.append(
                issue(
                    "second_look_proposal_binding",
                    "selected_proposal_id must be null when creative development is not required",
                    actual=selected_id,
                )
            )
        return failures

    development = _mapping(_mapping(composed.get("authorial_grammar")).get("creative_development"))
    expected_selected_id = development.get("selected_proposal_id")
    if not _is_nonempty_string(selected_id) or selected_id != expected_selected_id:
        failures.append(
            issue(
                "second_look_proposal_binding",
                "second-look plan must name the creative-development selected proposal exactly",
                expected=expected_selected_id,
                actual=selected_id,
            )
        )
    proposals = development.get("proposals")
    selected_proposal = (
        next(
            (
                proposal
                for proposal in proposals
                if isinstance(proposal, dict) and proposal.get("id") == expected_selected_id
            ),
            None,
        )
        if isinstance(proposals, list)
        else None
    )
    if not isinstance(selected_proposal, dict):
        failures.append(
            issue(
                "second_look_proposal_binding",
                "selected proposal is unavailable for exact second-look binding",
                selected_proposal_id=expected_selected_id,
            )
        )
        return failures

    expected_reveal = selected_proposal.get("first_second_reveal_phrase") or selected_proposal.get("reveal_phrase")
    if reveal_phrase != expected_reveal:
        failures.append(
            issue(
                "second_look_proposal_binding",
                "second-look reveal must exactly match the selected proposal reveal",
                expected=expected_reveal,
                actual=reveal_phrase,
            )
        )
    proposal_consequences = _string_list(selected_proposal.get("visible_consequence_phrases")) or []
    for role, consequence in (
        ("primary_carrier", primary_consequence),
        ("fallback_carrier", fallback_consequence),
    ):
        if consequence not in proposal_consequences:
            failures.append(
                issue(
                    "second_look_proposal_binding",
                    "carrier consequence must exactly match a selected-proposal visible consequence",
                    role=role,
                    consequence=consequence,
                    selected_proposal_id=expected_selected_id,
                    allowed=proposal_consequences,
                )
            )
    return failures


def _prompt_word_warning(pack: Mapping[str, Any], prompt_en: str) -> list[dict[str, Any]]:
    profile = _mapping(pack.get("format_profile"))
    raw_range = profile.get("prompt_word_range")
    minimum: int | None = None
    maximum: int | None = None
    if isinstance(raw_range, list) and len(raw_range) == 2 and all(isinstance(item, int) and not isinstance(item, bool) for item in raw_range):
        minimum, maximum = raw_range
    elif isinstance(raw_range, dict):
        raw_min, raw_max = raw_range.get("minimum"), raw_range.get("maximum")
        if isinstance(raw_min, int) and not isinstance(raw_min, bool) and isinstance(raw_max, int) and not isinstance(raw_max, bool):
            minimum, maximum = raw_min, raw_max
    if minimum is None or maximum is None or minimum > maximum:
        return []
    count = len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", prompt_en))
    if not minimum <= count <= maximum:
        return [issue("prompt_word_range", "prompt word count is outside the format recommendation; this is advisory", word_count=count, minimum=minimum, maximum=maximum)]
    return []


def audit_composed_prompt(pack: dict[str, Any], composed: dict[str, Any]) -> dict[str, Any]:
    """Return a deterministic JSON-serializable audit result."""

    integrity_errors = validate_pack_integrity(pack)
    failures: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []

    required_fields = (
        "pack_id",
        "prompt_en",
        "negative_en",
        "chosen_candidate_ids",
        "composer",
        "visual_evidence",
        "authorial_grammar",
        "viewer_evidence",
        "format_evidence",
        "reference_boundary",
    )
    missing = [field for field in required_fields if field not in composed]
    if missing:
        failures.append(issue("output_contract", "composed object is missing required fields", fields=missing))

    prompt_en = composed.get("prompt_en")
    if not _is_nonempty_string(prompt_en):
        failures.append(issue("output_contract", "prompt_en must be a nonempty string"))
        prompt_en = ""
    else:
        prompt_en = str(prompt_en)
    if composed.get("composer") != "agent":
        failures.append(issue("output_contract", "composer must equal agent", actual=composed.get("composer")))
    if composed.get("pack_id") != pack.get("pack_id"):
        failures.append(issue("pack_id", "composed pack_id does not exactly match candidate pack", expected=pack.get("pack_id"), actual=composed.get("pack_id")))
    if composed.get("negative_en") != pack.get("negative_en"):
        failures.append(issue("negative_en", "negative_en is not byte-for-byte identical to candidate pack"))

    chosen_ids, chosen_failures = _strict_chosen_ids(composed.get("chosen_candidate_ids"))
    failures.extend(chosen_failures)
    expected_ids = expected_chosen_candidate_ids(pack)
    if set(chosen_ids) != set(expected_ids) or len(chosen_ids) != len(expected_ids):
        failures.append(issue("chosen_candidate_ids", "chosen_candidate_ids must be the exact route, format, and exposed visual-node set", expected=expected_ids, actual=chosen_ids, missing=sorted(set(expected_ids) - set(chosen_ids)), extra=sorted(set(chosen_ids) - set(expected_ids))))
    allowed_visual_ids = {candidate_id for candidate_id in expected_ids if candidate_id.startswith("visual:")}
    nonvisual_candidates = sorted(candidate_id for candidate_id in chosen_ids if candidate_id.startswith("visual:") and candidate_id not in allowed_visual_ids)
    if nonvisual_candidates:
        failures.append(issue("typed_candidate_boundary", "unexposed, router, guard, or other nonvisual candidate selected as visual proof", ids=nonvisual_candidates))

    visual_evidence = _mapping(composed.get("visual_evidence"))
    authorial = _mapping(composed.get("authorial_grammar"))
    viewer = _mapping(composed.get("viewer_evidence"))
    format_evidence = _mapping(composed.get("format_evidence"))
    failures.extend(audit_literal_evidence(prompt_en, "visual_evidence", composed.get("visual_evidence")))
    failures.extend(audit_literal_evidence(prompt_en, "authorial_grammar", composed.get("authorial_grammar"), skipped_roots=("creative_development",)))
    failures.extend(audit_literal_evidence(prompt_en, "viewer_evidence", composed.get("viewer_evidence")))
    failures.extend(audit_literal_evidence(prompt_en, "format_evidence", composed.get("format_evidence")))

    grammar = _mapping(pack.get("visual_grammar"))
    required_visual = _string_list(grammar.get("required_evidence_types")) or []
    failures.extend(_required_phrase_failures("visual_evidence", visual_evidence, required_visual, prompt_en))

    authorial_contract = _mapping(pack.get("authorial_contract"))
    authorial_fields = list(AUTHORIAL_REQUIRED_FIELDS)
    authorial_fields.extend(_string_list(authorial_contract.get("required_fields")) or [])
    failures.extend(_required_phrase_failures("authorial_grammar", authorial, authorial_fields, prompt_en))
    failures.extend(_authorial_concreteness_failures(authorial))

    viewer_contract = _mapping(pack.get("viewer_contract"))
    viewer_fields = list(VIEWER_REQUIRED_FIELDS)
    viewer_fields.extend(_string_list(viewer_contract.get("required_fields")) or [])
    if viewer_contract.get("reinspection_reward_required") is True:
        viewer_fields.append("reinspection_reward_phrase")
    failures.extend(_required_phrase_failures("viewer_evidence", viewer, viewer_fields, prompt_en))

    first = viewer.get("first_glance_hook_phrase")
    second = viewer.get("second_look_reveal_phrase")
    if _is_nonempty_string(first) and _is_nonempty_string(second):
        if first == second:
            failures.append(issue("first_second_look", "first-glance hook and second-look reveal must be different phrases"))
        elif prompt_en.find(str(first)) >= prompt_en.find(str(second)):
            failures.append(issue("first_second_look", "first-glance phrase must precede second-look phrase in prompt_en", first=first, second=second))
    causal_fields = ["affect_actor_phrase", "affect_action_phrase", "affect_target_phrase", "affect_consequence_phrase"]
    causal_values = [viewer.get(field) for field in causal_fields if _is_nonempty_string(viewer.get(field))]
    if len(causal_values) == len(causal_fields) and len(set(causal_values)) != len(causal_values):
        failures.append(issue("causal_viewer_evidence", "actor, directed action, target, and consequence must be distinct visible phrases", phrases=causal_values))

    failures.extend(_mandatory_intent_failures(pack, composed, prompt_en))
    failures.extend(_format_failures(pack, composed, prompt_en))
    failures.extend(_reference_boundary_failures(composed, prompt_en, pack))
    failures.extend(_policy_language_failures(prompt_en))
    failures.extend(_phase_boundary_failures(pack, composed, prompt_en))
    failures.extend(_photo_dominance_failures(pack, prompt_en))
    failures.extend(_motif_failures(pack, composed, prompt_en))
    failures.extend(_creative_development_failures(pack, composed, prompt_en))
    failures.extend(_second_look_plan_failures(pack, composed, prompt_en))
    warnings.extend(_prompt_word_warning(pack, prompt_en))

    status = "error" if integrity_errors else ("fail" if failures else "pass")
    return {
        "status": status,
        "quality_status": "warn" if warnings else "pass",
        "pack_id": pack.get("pack_id"),
        "chosen_candidate_count": len(chosen_ids),
        "integrity_errors": integrity_errors,
        "failures": failures,
        "warnings": warnings,
        "limits": [
            "A prompt audit cannot prove rendered pixel salience, historical originality, audience response, sales, or legal clearance.",
            "Named-style and protected-IP text detection is a narrow backstop; reference_boundary and platform policy remain authoritative.",
        ],
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit one agent-composed illustration prompt against one compact candidate pack.")
    parser.add_argument("--pack", required=True, help="Candidate-pack JSON path or inline JSON.")
    parser.add_argument("--composed", required=True, help="Composed-prompt JSON path or inline JSON.")
    parser.add_argument("--output-file", help="Optional UTF-8 path for the same JSON result printed to stdout.")
    return parser.parse_args(argv)


def _transport_error_result(exc: Exception) -> dict[str, Any]:
    return {
        "status": "error",
        "quality_status": "not_run",
        "pack_id": None,
        "chosen_candidate_count": 0,
        "integrity_errors": [issue("input", str(exc))],
        "failures": [],
        "warnings": [],
        "limits": [],
    }


def main(argv: Sequence[str] | None = None) -> int:
    output_path: Path | None = None
    try:
        args = parse_args(argv)
        output_path = Path(args.output_file) if args.output_file else None
        pack = first_pack(load_json_arg(args.pack))
        composed = composed_object(load_json_arg(args.composed))
        result = audit_composed_prompt(pack, composed)
    except (AuditInputError, OSError, UnicodeError, json.JSONDecodeError, TypeError, ValueError) as exc:
        result = _transport_error_result(exc)
        payload = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        if output_path is not None:
            try:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(payload, encoding="utf-8")
            except OSError:
                pass
        sys.stdout.write(payload)
        return 2

    payload = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if output_path is not None:
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(payload, encoding="utf-8")
        except OSError as exc:
            error_result = _transport_error_result(exc)
            sys.stdout.write(json.dumps(error_result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
            return 2
    sys.stdout.write(payload)
    if result["integrity_errors"]:
        return 2
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
