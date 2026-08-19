#!/usr/bin/env python3
"""Validated additive visual-semantics profiles layered over moe grammar v4.

The historical 29-element assets remain byte-for-byte replay inputs.  This
module validates a small successor registry that can refine one existing visual
contract and add independently selectable concepts without pretending that the
old inventory already contained them.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Mapping, Sequence

from moe_meaning_contract import (
    canonical_json_bytes,
    contract_sha256,
    runtime_label_present,
)
from moe_visual_contract import normalize_alias, visual_contract_sha256


ADDITION_SCHEMA = "subculture-illustration-moe-visual-additions/v1"
ADDITION_FILENAME = "moe_visual_additions_v1.json"
GRAMMAR_SCHEMA_V5 = "subculture-illustration-moe-grammar/v5"
ALIAS_RELATIONS_V2 = {"exact", "variant", "carrier", "related", "ambiguous"}
ACTIVATING_ALIAS_RELATIONS_V2 = {"exact", "variant", "carrier"}
EXPECTED_PROFILE_IDS = (
    "moe_ntr_relationship_displacement",
    "moe_female_leopard_pose",
    "moe_cat_pose_family",
    "moe_brief_underwear_glimpse",
    "moe_blond_tanned_delinq_archetype",
    "moe_glasses_woman_archetype",
    "moe_literary_woman_archetype",
    "moe_gumiho",
    "moe_dragon",
    "moe_dokkaebi",
    "moe_ghost",
    "moe_robot",
    "moe_assassin",
    "moe_soldier",
    "moe_pilot",
    "moe_tights",
    "moe_bandage",
)
NEW_PROFILE_IDS = EXPECTED_PROFILE_IDS[1:]
REFINED_PROFILE_IDS = EXPECTED_PROFILE_IDS[:1]
OUTPUT_MODES = {
    "single_frame",
    "paired_frame",
    "sequence",
    "optical_interaction",
}
REPRESENTATION_MODES = {
    "single_frame",
    "paired_or_sequence",
    "sequence",
    "optical_interaction",
}
INTEGRATION_ROLES = {
    "character_state",
    "relationship_event",
    "wardrobe",
    "pose",
    "expression",
    "composition",
    "participatory_action",
    "environment_hazard",
}
LABEL_POLICIES = {"allow", "omit", "brand_neutral"}
SEMANTIC_FIDELITIES = {
    "exact_componentized",
    "safe_analogue",
    "partial_evidence",
    "sequence_required",
    "interaction_required",
}
ADULT_REQUIREMENTS = {
    "none",
    "explicit_adult_for_body_focus",
    "explicit_adult_if_suggestive",
    "explicit_adult_always",
    "nonsexual_school_context",
}


class MoeVisualAdditionError(ValueError):
    """Raised when the additive registry or its v5 manifest drifts."""


@dataclass(frozen=True)
class MoeVisualAdditions:
    path: Path
    payload: dict[str, Any]
    profiles_by_id: dict[str, dict[str, Any]]
    new_profiles_by_id: dict[str, dict[str, Any]]
    refinements_by_id: dict[str, dict[str, Any]]
    alias_bindings: dict[str, dict[str, Any]]
    sources_by_id: dict[str, dict[str, Any]]
    sha256: str


def _exact_keys(value: Any, expected: set[str], *, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise MoeVisualAdditionError(f"{name} must be an object")
    if set(value) != expected:
        raise MoeVisualAdditionError(
            f"{name} keys drift: missing={sorted(expected - set(value))}, "
            f"extra={sorted(set(value) - expected)}"
        )
    return value


def _string(value: Any, *, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise MoeVisualAdditionError(f"{name} must be a nonempty string")
    return value


def _strings(value: Any, *, name: str, minimum: int = 1) -> list[str]:
    if not isinstance(value, list) or len(value) < minimum:
        raise MoeVisualAdditionError(f"{name} needs at least {minimum} strings")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise MoeVisualAdditionError(f"{name} must contain nonempty strings")
    if len(value) != len(set(value)):
        raise MoeVisualAdditionError(f"{name} must remain unique")
    return list(value)


def _load_object(path: Path) -> tuple[dict[str, Any], str]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise MoeVisualAdditionError(f"cannot read {path}: {exc}") from exc
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise MoeVisualAdditionError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise MoeVisualAdditionError(f"{path} must contain one JSON object")
    return payload, hashlib.sha256(raw).hexdigest()


def _validate_meaning_contract(
    value: Any,
    *,
    element_id: str,
    ordinal: int,
) -> dict[str, Any]:
    name = f"{element_id}.meaning_contract"
    contract = _exact_keys(
        value,
        {
            "element_id",
            "ordinal",
            "source_dossier",
            "canonical_definition_ko",
            "essential_semantics_ko",
            "non_equivalents_ko",
            "semantic_axes",
            "runtime_label_policy",
            "runtime_forbidden_labels",
            "semantic_fidelity",
            "component_groups",
            "optional_components_en",
            "false_substitutes_en",
            "do_not_infer_en",
            "adult_requirement",
            "capability",
        },
        name=name,
    )
    if contract["element_id"] != element_id or contract["ordinal"] != ordinal:
        raise MoeVisualAdditionError(f"{name} identity or ordinal drift")
    if contract["source_dossier"] != "visual_additions":
        raise MoeVisualAdditionError(f"{name}.source_dossier drift")
    _string(contract["canonical_definition_ko"], name=f"{name}.definition")
    _strings(contract["essential_semantics_ko"], name=f"{name}.essential", minimum=2)
    _strings(contract["non_equivalents_ko"], name=f"{name}.non_equivalents", minimum=2)
    axes = _strings(contract["semantic_axes"], name=f"{name}.semantic_axes", minimum=2)
    if any(not re.fullmatch(r"[a-z][a-z0-9_]+", axis) for axis in axes):
        raise MoeVisualAdditionError(f"{name}.semantic_axes needs typed IDs")
    if contract["runtime_label_policy"] not in LABEL_POLICIES:
        raise MoeVisualAdditionError(f"{name}.runtime_label_policy drift")
    forbidden = _strings(
        contract["runtime_forbidden_labels"],
        name=f"{name}.runtime_forbidden_labels",
        minimum=0,
    )
    if contract["runtime_label_policy"] != "allow" and not forbidden:
        raise MoeVisualAdditionError(f"{name} needs forbidden runtime labels")
    if contract["semantic_fidelity"] not in SEMANTIC_FIDELITIES:
        raise MoeVisualAdditionError(f"{name}.semantic_fidelity drift")
    groups = contract["component_groups"]
    if not isinstance(groups, list) or len(groups) < 2:
        raise MoeVisualAdditionError(f"{name}.component_groups needs at least two")
    group_ids: set[str] = set()
    for index, raw_group in enumerate(groups):
        group = _exact_keys(
            raw_group,
            {"id", "minimum", "alternatives_en"},
            name=f"{name}.component_groups[{index}]",
        )
        group_id = _string(group["id"], name=f"{name}.group[{index}].id")
        if not re.fullmatch(r"[a-z][a-z0-9_]+", group_id) or group_id in group_ids:
            raise MoeVisualAdditionError(f"{name} component group ID drift")
        group_ids.add(group_id)
        alternatives = _strings(
            group["alternatives_en"], name=f"{name}.{group_id}.alternatives_en"
        )
        minimum = group["minimum"]
        if type(minimum) is not int or not 1 <= minimum <= len(alternatives):
            raise MoeVisualAdditionError(f"{name}.{group_id}.minimum drift")
        for label in forbidden:
            if any(runtime_label_present(label, phrase) for phrase in alternatives):
                raise MoeVisualAdditionError(
                    f"{name}.{group_id} leaks forbidden label {label!r}"
                )
    _strings(contract["optional_components_en"], name=f"{name}.optional", minimum=0)
    _strings(contract["false_substitutes_en"], name=f"{name}.false_substitutes")
    _strings(contract["do_not_infer_en"], name=f"{name}.do_not_infer")
    if contract["adult_requirement"] not in ADULT_REQUIREMENTS:
        raise MoeVisualAdditionError(f"{name}.adult_requirement drift")
    capability = _exact_keys(
        contract["capability"],
        {"single_frame", "sequence", "interaction"},
        name=f"{name}.capability",
    )
    if capability["single_frame"] not in {"exact", "partial", "substrate_only"}:
        raise MoeVisualAdditionError(f"{name}.single_frame capability drift")
    if capability["sequence"] not in {"required", "recommended", "not_required"}:
        raise MoeVisualAdditionError(f"{name}.sequence capability drift")
    if capability["interaction"] not in {"required", "not_required"}:
        raise MoeVisualAdditionError(f"{name}.interaction capability drift")
    return contract


def _validate_axes(value: Any, *, element_id: str, allow_empty: bool) -> None:
    if not isinstance(value, list) or (not allow_empty and len(value) < 2):
        raise MoeVisualAdditionError(f"{element_id}.preference_axes drift")
    for axis_index, raw_axis in enumerate(value):
        axis = _exact_keys(
            raw_axis,
            {"id", "description", "values"},
            name=f"{element_id}.preference_axes[{axis_index}]",
        )
        _string(axis["id"], name=f"{element_id}.axis.id")
        _string(axis["description"], name=f"{element_id}.axis.description")
        values = axis["values"]
        if not isinstance(values, list) or len(values) < 2:
            raise MoeVisualAdditionError(f"{element_id} axis needs two values")
        for value_index, raw_choice in enumerate(values):
            choice = _exact_keys(
                raw_choice,
                {"id", "label", "request_cues"},
                name=f"{element_id}.axis.values[{value_index}]",
            )
            _string(choice["id"], name=f"{element_id}.axis.value.id")
            _string(choice["label"], name=f"{element_id}.axis.value.label")
            _strings(choice["request_cues"], name=f"{element_id}.axis.value.cues")


def _validate_atom(value: Any, *, name: str, atom_ids: set[str]) -> dict[str, Any]:
    atom = _exact_keys(
        value,
        {"id", "prompt_fragment_en", "observable_evidence"},
        name=name,
    )
    atom_id = _string(atom["id"], name=f"{name}.id")
    if not re.fullmatch(r"moe_atom_[a-z0-9_]+", atom_id) or atom_id in atom_ids:
        raise MoeVisualAdditionError(f"{name}.id drift")
    atom_ids.add(atom_id)
    _string(atom["prompt_fragment_en"], name=f"{name}.prompt_fragment_en")
    _strings(atom["observable_evidence"], name=f"{name}.observable_evidence")
    return atom


def _validate_candidates(
    value: Any,
    *,
    element_id: str,
    claim_ids: set[str],
    forbidden_labels: Sequence[str],
    adult_required: bool,
) -> set[str]:
    if not isinstance(value, list) or len(value) < 3:
        raise MoeVisualAdditionError(f"{element_id}.candidates needs at least three")
    candidate_ids: set[str] = set()
    atom_ids: set[str] = set()
    subtype_ids: set[str] = set()
    novelty_levels: set[int] = set()
    default_count = 0
    expected_keys = {
        "id",
        "label_en",
        "subtype_id",
        "novelty_level",
        "canonical_default",
        "intent_keys",
        "representation_mode",
        "integration_role",
        "selection_cues",
        "preference_profile",
        "primary_atom",
        "support_atoms",
        "resource_claims",
        "compatibility_tags",
        "source_claim_ids",
        "limitation",
    }
    for index, raw_candidate in enumerate(value):
        candidate = _exact_keys(
            raw_candidate, expected_keys, name=f"{element_id}.candidates[{index}]"
        )
        candidate_id = _string(candidate["id"], name=f"{element_id}.candidate.id")
        if (
            not re.fullmatch(r"moe_candidate_[a-z0-9_]+", candidate_id)
            or candidate_id in candidate_ids
        ):
            raise MoeVisualAdditionError(f"{element_id} candidate ID drift")
        candidate_ids.add(candidate_id)
        subtype_id = _string(
            candidate["subtype_id"], name=f"{candidate_id}.subtype_id"
        )
        subtype_ids.add(subtype_id)
        novelty = candidate["novelty_level"]
        if type(novelty) is not int or novelty not in {0, 1, 2}:
            raise MoeVisualAdditionError(f"{candidate_id}.novelty_level drift")
        novelty_levels.add(novelty)
        if type(candidate["canonical_default"]) is not bool:
            raise MoeVisualAdditionError(f"{candidate_id}.canonical_default drift")
        if candidate["canonical_default"]:
            default_count += 1
            if novelty != 1:
                raise MoeVisualAdditionError(f"{candidate_id} default must be novelty 1")
        if candidate["representation_mode"] not in REPRESENTATION_MODES:
            raise MoeVisualAdditionError(f"{candidate_id}.representation_mode drift")
        if candidate["integration_role"] not in INTEGRATION_ROLES:
            raise MoeVisualAdditionError(f"{candidate_id}.integration_role drift")
        for field in (
            "label_en",
            "limitation",
        ):
            _string(candidate[field], name=f"{candidate_id}.{field}")
        for field in (
            "intent_keys",
            "selection_cues",
            "resource_claims",
            "compatibility_tags",
            "source_claim_ids",
        ):
            _strings(candidate[field], name=f"{candidate_id}.{field}")
        if not set(candidate["source_claim_ids"]).issubset(claim_ids):
            raise MoeVisualAdditionError(f"{candidate_id}.source_claim_ids drift")
        profile = candidate["preference_profile"]
        if not isinstance(profile, dict) or not profile or any(
            not isinstance(key, str)
            or not key
            or not isinstance(item, str)
            or not item
            for key, item in profile.items()
        ):
            raise MoeVisualAdditionError(f"{candidate_id}.preference_profile drift")
        primary = _validate_atom(
            candidate["primary_atom"], name=f"{candidate_id}.primary_atom", atom_ids=atom_ids
        )
        supports = candidate["support_atoms"]
        if not isinstance(supports, list) or not 2 <= len(supports) <= 3:
            raise MoeVisualAdditionError(f"{candidate_id}.support_atoms drift")
        validated_supports = [
            _validate_atom(
                support,
                name=f"{candidate_id}.support_atoms[{support_index}]",
                atom_ids=atom_ids,
            )
            for support_index, support in enumerate(supports)
        ]
        runtime_fragments = [
            primary["prompt_fragment_en"],
            *[support["prompt_fragment_en"] for support in validated_supports],
        ]
        for label in forbidden_labels:
            if any(runtime_label_present(label, fragment) for fragment in runtime_fragments):
                raise MoeVisualAdditionError(
                    f"{candidate_id} leaks forbidden runtime label {label!r}"
                )
        if adult_required and not runtime_label_present(
            "adult", primary["prompt_fragment_en"]
        ):
            raise MoeVisualAdditionError(f"{candidate_id} must explicitly bind adult")
    if novelty_levels != {0, 1, 2} or default_count != 1:
        raise MoeVisualAdditionError(
            f"{element_id} needs novelty 0/1/2 and one canonical default"
        )
    return subtype_ids


def _validate_visual_contract(
    value: Any,
    *,
    element_id: str,
    ordinal: int,
    meaning_contract: Mapping[str, Any],
    candidate_subtypes: set[str],
    aliases: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    name = f"{element_id}.visual_meaning_contract"
    contract = _exact_keys(
        value,
        {
            "element_id",
            "ordinal",
            "base_contract_sha256",
            "default_variant_id",
            "alias_bindings",
            "visual_variants",
            "image_evidence_id",
        },
        name=name,
    )
    if contract["element_id"] != element_id or contract["ordinal"] != ordinal:
        raise MoeVisualAdditionError(f"{name} identity or ordinal drift")
    if contract["base_contract_sha256"] != contract_sha256(meaning_contract):
        raise MoeVisualAdditionError(f"{name} base meaning hash drift")
    if canonical_json_bytes(contract["alias_bindings"]) != canonical_json_bytes(list(aliases)):
        raise MoeVisualAdditionError(f"{name} alias binding drift")
    forbidden = list(meaning_contract["runtime_forbidden_labels"])
    required_group_ids = {
        str(group["id"]) for group in meaning_contract["component_groups"]
    }
    variants = contract["visual_variants"]
    if not isinstance(variants, list) or not variants:
        raise MoeVisualAdditionError(f"{name}.visual_variants must be nonempty")
    variant_ids: set[str] = set()
    subtype_owners: dict[str, str] = {}
    for index, raw_variant in enumerate(variants):
        variant = _exact_keys(
            raw_variant,
            {
                "id",
                "candidate_subtype_ids",
                "required_component_group_ids",
                "all_of_en",
                "any_of",
                "topology_edges_en",
                "camera_requirements_en",
                "temporal_states_en",
                "interaction_requirements_en",
                "negative_visual_confounds_en",
                "supported_output_modes",
            },
            name=f"{name}.visual_variants[{index}]",
        )
        variant_id = _string(variant["id"], name=f"{name}.variant.id")
        if variant_id in variant_ids:
            raise MoeVisualAdditionError(f"{name} duplicate variant {variant_id}")
        variant_ids.add(variant_id)
        subtype_ids = _strings(
            variant["candidate_subtype_ids"], name=f"{name}.{variant_id}.subtypes"
        )
        for subtype_id in subtype_ids:
            if subtype_id in subtype_owners:
                raise MoeVisualAdditionError(
                    f"{name} subtype {subtype_id} belongs to multiple variants"
                )
            subtype_owners[subtype_id] = variant_id
        groups = _strings(
            variant["required_component_group_ids"],
            name=f"{name}.{variant_id}.groups",
        )
        if set(groups) != required_group_ids:
            raise MoeVisualAdditionError(f"{name}.{variant_id} group coverage drift")
        for field in (
            "all_of_en",
            "topology_edges_en",
            "camera_requirements_en",
            "temporal_states_en",
            "interaction_requirements_en",
            "negative_visual_confounds_en",
        ):
            minimum = 0 if field in {"temporal_states_en", "interaction_requirements_en"} else 1
            phrases = _strings(
                variant[field], name=f"{name}.{variant_id}.{field}", minimum=minimum
            )
            if field != "negative_visual_confounds_en":
                for label in forbidden:
                    if any(runtime_label_present(label, phrase) for phrase in phrases):
                        raise MoeVisualAdditionError(
                            f"{name}.{variant_id}.{field} leaks {label!r}"
                        )
        any_of = _exact_keys(
            variant["any_of"],
            {"minimum", "alternatives_en"},
            name=f"{name}.{variant_id}.any_of",
        )
        alternatives = _strings(
            any_of["alternatives_en"],
            name=f"{name}.{variant_id}.any_of.alternatives",
            minimum=0,
        )
        minimum = any_of["minimum"]
        if type(minimum) is not int or not 0 <= minimum <= len(alternatives):
            raise MoeVisualAdditionError(f"{name}.{variant_id}.any_of minimum drift")
        modes = _strings(
            variant["supported_output_modes"], name=f"{name}.{variant_id}.modes"
        )
        if not set(modes).issubset(OUTPUT_MODES):
            raise MoeVisualAdditionError(f"{name}.{variant_id}.modes drift")
    if set(subtype_owners) != candidate_subtypes:
        raise MoeVisualAdditionError(
            f"{name} subtype coverage drift: "
            f"missing={sorted(candidate_subtypes - set(subtype_owners))}, "
            f"extra={sorted(set(subtype_owners) - candidate_subtypes)}"
        )
    if contract["default_variant_id"] not in variant_ids:
        raise MoeVisualAdditionError(f"{name}.default_variant_id drift")
    for alias in aliases:
        relation = alias["relation"]
        variant_id = alias["variant_id"]
        if relation == "variant" and variant_id not in variant_ids:
            raise MoeVisualAdditionError(f"{name} variant alias target drift")
        if relation != "variant" and variant_id is not None:
            raise MoeVisualAdditionError(f"{name} non-variant alias has a target")
    _string(contract["image_evidence_id"], name=f"{name}.image_evidence_id")
    return contract


def load_moe_visual_additions(
    path: str | Path,
    *,
    base_grammar_sha256: str,
    base_elements_by_id: Mapping[str, Mapping[str, Any]],
    base_alias_bindings: Mapping[str, Mapping[str, Any]],
) -> MoeVisualAdditions:
    resolved = Path(path).expanduser().resolve()
    payload, payload_sha = _load_object(resolved)
    top = _exact_keys(
        payload,
        {
            "schema",
            "created_at",
            "base_grammar_schema",
            "base_grammar_v4_sha256",
            "methodology",
            "source_count",
            "sources",
            "profile_count",
            "compatibility_rules",
            "profiles",
        },
        name="visual additions",
    )
    if top["schema"] != ADDITION_SCHEMA:
        raise MoeVisualAdditionError("visual additions schema mismatch")
    if top["base_grammar_schema"] != "subculture-illustration-moe-grammar/v4":
        raise MoeVisualAdditionError("visual additions base schema mismatch")
    if top["base_grammar_v4_sha256"] != base_grammar_sha256:
        raise MoeVisualAdditionError("visual additions base grammar hash mismatch")
    _string(top["created_at"], name="visual additions.created_at")
    methodology = _exact_keys(
        top["methodology"],
        {"research_scope", "content_filter", "interpretation_limit"},
        name="visual additions.methodology",
    )
    for key, value in methodology.items():
        _string(value, name=f"visual additions.methodology.{key}")

    sources = top["sources"]
    if not isinstance(sources, list) or not sources:
        raise MoeVisualAdditionError("visual additions.sources must be nonempty")
    sources_by_id: dict[str, dict[str, Any]] = {}
    source_urls: set[str] = set()
    for index, raw_source in enumerate(sources):
        source = _exact_keys(
            raw_source,
            {"id", "kind", "title", "url", "publisher", "claim_scope"},
            name=f"visual additions.sources[{index}]",
        )
        source_id = _string(source["id"], name=f"visual source {index}.id")
        if not re.fullmatch(r"add_src_[a-z0-9_]+", source_id) or source_id in sources_by_id:
            raise MoeVisualAdditionError(f"visual source {index} ID drift")
        if source["kind"] not in {
            "dictionary",
            "academic",
            "editorial",
            "community_reference",
            "instructional",
        }:
            raise MoeVisualAdditionError(f"visual source {source_id}.kind drift")
        for field in ("title", "publisher", "claim_scope"):
            _string(source[field], name=f"visual source {source_id}.{field}")
        url = _string(source["url"], name=f"visual source {source_id}.url")
        if not url.startswith("https://"):
            raise MoeVisualAdditionError(f"visual source {source_id} must use https")
        source_urls.add(url)
        sources_by_id[source_id] = source
    if top["source_count"] != len(sources):
        raise MoeVisualAdditionError("visual additions source_count drift")

    rules = _exact_keys(
        top["compatibility_rules"],
        {"hard_conflicts", "synergies"},
        name="visual additions.compatibility_rules",
    )
    if not isinstance(rules["hard_conflicts"], list) or not isinstance(
        rules["synergies"], list
    ):
        raise MoeVisualAdditionError("visual additions compatibility rules drift")

    profiles = top["profiles"]
    if not isinstance(profiles, list) or [
        row.get("element_id") if isinstance(row, dict) else None for row in profiles
    ] != list(EXPECTED_PROFILE_IDS):
        raise MoeVisualAdditionError("visual additions profile inventory drift")
    if top["profile_count"] != len(profiles):
        raise MoeVisualAdditionError("visual additions profile_count drift")

    profiles_by_id: dict[str, dict[str, Any]] = {}
    new_profiles: dict[str, dict[str, Any]] = {}
    refinements: dict[str, dict[str, Any]] = {}
    alias_bindings: dict[str, dict[str, Any]] = {}
    evidence_ids: set[str] = set()
    profile_keys = {
        "element_id",
        "ordinal",
        "mode",
        "category",
        "label_ko",
        "label_en",
        "aliases",
        "research_summary_ko",
        "claims",
        "research_evidence",
        "meaning_contract",
        "meaning_contract_sha256",
        "preference_axes",
        "candidates",
        "visual_meaning_contract",
        "visual_meaning_contract_sha256",
        "compatibility_profile",
    }
    for index, raw_profile in enumerate(profiles):
        profile = _exact_keys(raw_profile, profile_keys, name=f"visual profile {index}")
        element_id = str(profile["element_id"])
        ordinal = profile["ordinal"]
        if type(ordinal) is not int or ordinal < 1:
            raise MoeVisualAdditionError(f"{element_id}.ordinal drift")
        mode = profile["mode"]
        if mode not in {"existing_refinement", "new_element"}:
            raise MoeVisualAdditionError(f"{element_id}.mode drift")
        for field in ("category", "label_ko", "label_en", "research_summary_ko"):
            _string(profile[field], name=f"{element_id}.{field}")

        claims = profile["claims"]
        if not isinstance(claims, list) or not claims:
            raise MoeVisualAdditionError(f"{element_id}.claims must be nonempty")
        claim_ids: set[str] = set()
        for claim_index, raw_claim in enumerate(claims):
            claim = _exact_keys(
                raw_claim,
                {"id", "claim_ko", "source_ids", "confidence"},
                name=f"{element_id}.claims[{claim_index}]",
            )
            claim_id = _string(claim["id"], name=f"{element_id}.claim.id")
            if not re.fullmatch(r"moe_add_claim_[a-z0-9_]+", claim_id) or claim_id in claim_ids:
                raise MoeVisualAdditionError(f"{element_id} claim ID drift")
            claim_ids.add(claim_id)
            _string(claim["claim_ko"], name=f"{claim_id}.claim_ko")
            referenced = _strings(claim["source_ids"], name=f"{claim_id}.source_ids")
            if not set(referenced).issubset(sources_by_id):
                raise MoeVisualAdditionError(f"{claim_id}.source_ids drift")
            if claim["confidence"] not in {"high", "medium", "medium-low", "low"}:
                raise MoeVisualAdditionError(f"{claim_id}.confidence drift")

        evidence = _exact_keys(
            profile["research_evidence"],
            {
                "id",
                "queries",
                "search_confidence",
                "recurring_features_en",
                "observed_confounds_en",
                "representative_source_urls",
                "limitations_en",
            },
            name=f"{element_id}.research_evidence",
        )
        evidence_id = _string(evidence["id"], name=f"{element_id}.evidence.id")
        if evidence_id in evidence_ids:
            raise MoeVisualAdditionError(f"duplicate evidence ID {evidence_id}")
        evidence_ids.add(evidence_id)
        _strings(evidence["queries"], name=f"{element_id}.evidence.queries")
        if evidence["search_confidence"] not in {"high", "medium", "low"}:
            raise MoeVisualAdditionError(f"{element_id}.search_confidence drift")
        _strings(
            evidence["recurring_features_en"],
            name=f"{element_id}.evidence.recurring_features",
            minimum=2,
        )
        _strings(
            evidence["observed_confounds_en"],
            name=f"{element_id}.evidence.confounds",
        )
        urls = _strings(
            evidence["representative_source_urls"],
            name=f"{element_id}.evidence.urls",
            minimum=0,
        )
        if not set(urls).issubset(source_urls):
            raise MoeVisualAdditionError(f"{element_id}.evidence URLs drift")
        _strings(evidence["limitations_en"], name=f"{element_id}.evidence.limitations")

        aliases = profile["aliases"]
        if not isinstance(aliases, list) or not aliases:
            raise MoeVisualAdditionError(f"{element_id}.aliases must be nonempty")
        validated_aliases: list[dict[str, Any]] = []
        for alias_index, raw_alias in enumerate(aliases):
            alias = _exact_keys(
                raw_alias,
                {"alias", "relation", "variant_id"},
                name=f"{element_id}.aliases[{alias_index}]",
            )
            phrase = _string(alias["alias"], name=f"{element_id}.alias")
            relation = alias["relation"]
            if relation not in ALIAS_RELATIONS_V2:
                raise MoeVisualAdditionError(f"{element_id} alias relation drift")
            normalized = normalize_alias(phrase)
            existing = alias_bindings.get(normalized) or base_alias_bindings.get(normalized)
            if existing is not None and str(existing["element_id"]) != element_id:
                raise MoeVisualAdditionError(
                    f"ambiguous alias {phrase!r}: {existing['element_id']} / {element_id}"
                )
            binding = {
                "element_id": element_id,
                "alias": phrase,
                "relation": relation,
                "variant_id": alias["variant_id"],
            }
            alias_bindings[normalized] = binding
            validated_aliases.append(dict(alias))

        if mode == "existing_refinement":
            base_element = base_elements_by_id.get(element_id)
            if base_element is None or ordinal != int(base_element["ordinal"]):
                raise MoeVisualAdditionError(f"{element_id} refinement target drift")
            if profile["meaning_contract"] is not None:
                raise MoeVisualAdditionError(f"{element_id} refinement cannot replace meaning")
            meaning = base_element["meaning_contract"]
            if profile["meaning_contract_sha256"] != base_element["meaning_contract_sha256"]:
                raise MoeVisualAdditionError(f"{element_id} base meaning hash drift")
            if profile["preference_axes"] or profile["candidates"]:
                raise MoeVisualAdditionError(f"{element_id} refinement cannot replace candidates")
            _validate_axes(profile["preference_axes"], element_id=element_id, allow_empty=True)
            candidate_subtypes = {
                str(candidate["subtype_id"]) for candidate in base_element["candidates"]
            }
            if profile["compatibility_profile"] is not None:
                raise MoeVisualAdditionError(f"{element_id} refinement cannot replace compatibility")
            refinements[element_id] = profile
        else:
            if element_id in base_elements_by_id or element_id not in NEW_PROFILE_IDS:
                raise MoeVisualAdditionError(f"{element_id} new element identity drift")
            meaning = _validate_meaning_contract(
                profile["meaning_contract"], element_id=element_id, ordinal=ordinal
            )
            if profile["meaning_contract_sha256"] != contract_sha256(meaning):
                raise MoeVisualAdditionError(f"{element_id} meaning hash drift")
            _validate_axes(profile["preference_axes"], element_id=element_id, allow_empty=False)
            candidate_subtypes = _validate_candidates(
                profile["candidates"],
                element_id=element_id,
                claim_ids=claim_ids,
                forbidden_labels=meaning["runtime_forbidden_labels"],
                adult_required=meaning["adult_requirement"]
                in {
                    "explicit_adult_for_body_focus",
                    "explicit_adult_if_suggestive",
                    "explicit_adult_always",
                },
            )
            if not isinstance(profile["compatibility_profile"], dict):
                raise MoeVisualAdditionError(f"{element_id}.compatibility_profile missing")
            new_profiles[element_id] = profile

        visual = _validate_visual_contract(
            profile["visual_meaning_contract"],
            element_id=element_id,
            ordinal=ordinal,
            meaning_contract=meaning,
            candidate_subtypes=candidate_subtypes,
            aliases=validated_aliases,
        )
        if profile["visual_meaning_contract_sha256"] != visual_contract_sha256(visual):
            raise MoeVisualAdditionError(f"{element_id} visual contract hash drift")
        if visual["image_evidence_id"] != evidence_id:
            raise MoeVisualAdditionError(f"{element_id} evidence binding drift")
        profiles_by_id[element_id] = profile

    known_ids = set(base_elements_by_id).union(NEW_PROFILE_IDS)
    for pair in rules["hard_conflicts"]:
        if (
            not isinstance(pair, list)
            or len(pair) != 2
            or pair != sorted(pair)
            or not set(pair).issubset(known_ids)
        ):
            raise MoeVisualAdditionError("visual additions hard conflict drift")
    for index, raw_synergy in enumerate(rules["synergies"]):
        synergy = _exact_keys(
            raw_synergy,
            {"element_ids", "bridge_clause_en"},
            name=f"visual additions.synergies[{index}]",
        )
        pair = synergy["element_ids"]
        if (
            not isinstance(pair, list)
            or len(pair) != 2
            or pair != sorted(pair)
            or not set(pair).issubset(known_ids)
        ):
            raise MoeVisualAdditionError("visual additions synergy pair drift")
        _string(synergy["bridge_clause_en"], name="visual additions synergy clause")

    return MoeVisualAdditions(
        path=resolved,
        payload=top,
        profiles_by_id=profiles_by_id,
        new_profiles_by_id=new_profiles,
        refinements_by_id=refinements,
        alias_bindings=alias_bindings,
        sources_by_id=sources_by_id,
        sha256=payload_sha,
    )


def build_v5_manifest(
    *,
    base_grammar_sha256: str,
    base_elements_by_id: Mapping[str, Mapping[str, Any]],
    base_visual_contracts: Mapping[str, Mapping[str, Any]],
    base_image_evidence: Mapping[str, Mapping[str, Any]],
    base_candidate_count: int,
    base_compatibility_sha256: str,
    additions: MoeVisualAdditions,
) -> dict[str, Any]:
    """Build the small deterministic manifest that authenticates the v5 view."""

    effective_meanings: list[Mapping[str, Any]] = []
    effective_visuals: list[Mapping[str, Any]] = []
    effective_evidence: list[Mapping[str, Any]] = []
    for element_id, element in base_elements_by_id.items():
        effective_meanings.append(element["meaning_contract"])
        refinement = additions.refinements_by_id.get(element_id)
        effective_visuals.append(
            refinement["visual_meaning_contract"]
            if refinement is not None
            else base_visual_contracts[element_id]
        )
        if refinement is not None:
            effective_evidence.append(refinement["research_evidence"])
        else:
            evidence_id = base_visual_contracts[element_id]["image_evidence_id"]
            effective_evidence.append(base_image_evidence[evidence_id])
    for profile in additions.new_profiles_by_id.values():
        effective_meanings.append(profile["meaning_contract"])
        effective_visuals.append(profile["visual_meaning_contract"])
        effective_evidence.append(profile["research_evidence"])

    extension_candidate_count = sum(
        len(profile["candidates"])
        for profile in additions.new_profiles_by_id.values()
    )
    compatibility_projection = {
        "base_compatibility_sha256": base_compatibility_sha256,
        "rules": additions.payload["compatibility_rules"],
        "profiles": [
            profile["compatibility_profile"]
            for profile in additions.new_profiles_by_id.values()
        ],
    }
    return {
        "schema": GRAMMAR_SCHEMA_V5,
        "created_at": additions.payload["created_at"],
        "base_grammar_v4_sha256": base_grammar_sha256,
        "visual_additions_schema": additions.payload["schema"],
        "visual_additions_sha256": additions.sha256,
        "base_element_count": len(base_elements_by_id),
        "new_element_count": len(additions.new_profiles_by_id),
        "refined_element_count": len(additions.refinements_by_id),
        "selectable_element_count": len(base_elements_by_id)
        + len(additions.new_profiles_by_id),
        "candidate_count": base_candidate_count + extension_candidate_count,
        "new_element_ids": list(additions.new_profiles_by_id),
        "refined_element_ids": list(additions.refinements_by_id),
        "effective_meaning_contracts_sha256": hashlib.sha256(
            canonical_json_bytes(effective_meanings)
        ).hexdigest(),
        "effective_visual_meaning_contracts_sha256": hashlib.sha256(
            canonical_json_bytes(effective_visuals)
        ).hexdigest(),
        "effective_image_search_evidence_sha256": hashlib.sha256(
            canonical_json_bytes(effective_evidence)
        ).hexdigest(),
        "effective_compatibility_sha256": hashlib.sha256(
            canonical_json_bytes(compatibility_projection)
        ).hexdigest(),
    }


__all__ = [
    "ACTIVATING_ALIAS_RELATIONS_V2",
    "ADDITION_FILENAME",
    "ADDITION_SCHEMA",
    "ALIAS_RELATIONS_V2",
    "EXPECTED_PROFILE_IDS",
    "GRAMMAR_SCHEMA_V5",
    "MoeVisualAdditionError",
    "MoeVisualAdditions",
    "NEW_PROFILE_IDS",
    "REFINED_PROFILE_IDS",
    "build_v5_manifest",
    "load_moe_visual_additions",
]
