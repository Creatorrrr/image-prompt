#!/usr/bin/env python3
"""Validated alias, visual-variant, and image-search evidence contracts."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import unicodedata
from typing import Any, Mapping, Sequence

from moe_meaning_contract import (
    MEANING_SCHEMA,
    MoeMeaningContracts,
    canonical_json_bytes,
    contract_sha256,
    runtime_label_present,
)


VISUAL_MEANING_SCHEMA = "subculture-illustration-moe-meaning-contracts/v2"
VISUAL_MEANING_FILENAME = "moe_meaning_contracts_v2.json"
IMAGE_EVIDENCE_SCHEMA = "subculture-illustration-moe-image-search-evidence/v1"
IMAGE_EVIDENCE_FILENAME = "image_search_evidence_v1.json"
ALIAS_RELATIONS = {"exact", "variant", "carrier", "related"}
ACTIVATING_ALIAS_RELATIONS = {"exact", "variant", "carrier"}
SEARCH_CONFIDENCE = {"high", "medium", "low"}
OUTPUT_MODES = {
    "single_frame",
    "paired_frame",
    "sequence",
    "optical_interaction",
}


class MoeVisualContractError(ValueError):
    """Raised when visual meaning or image-search evidence drifts."""


@dataclass(frozen=True)
class MoeVisualMeaningContracts:
    path: Path
    evidence_path: Path
    payload: dict[str, Any]
    contracts_by_id: dict[str, dict[str, Any]]
    alias_bindings: dict[str, dict[str, Any]]
    image_evidence_by_id: dict[str, dict[str, Any]]
    sha256: str
    evidence_sha256: str


def normalize_alias(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    normalized = re.sub(r"[^\w]+", " ", normalized, flags=re.UNICODE)
    return " ".join(normalized.split())


def visual_contract_sha256(contract: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_json_bytes(dict(contract))).hexdigest()


def _load_object(path: Path) -> tuple[dict[str, Any], str]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise MoeVisualContractError(f"cannot read {path}: {exc}") from exc
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise MoeVisualContractError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise MoeVisualContractError(f"{path} must contain one JSON object")
    return payload, hashlib.sha256(raw).hexdigest()


def _exact_keys(value: Any, expected: set[str], *, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise MoeVisualContractError(f"{name} must be an object")
    if set(value) != expected:
        missing = sorted(expected - set(value))
        extra = sorted(set(value) - expected)
        raise MoeVisualContractError(
            f"{name} keys drift: missing={missing}, extra={extra}"
        )
    return value


def _string(value: Any, *, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise MoeVisualContractError(f"{name} must be a nonempty string")
    return value


def _string_list(
    value: Any,
    *,
    name: str,
    minimum: int = 1,
) -> list[str]:
    if not isinstance(value, list) or len(value) < minimum:
        raise MoeVisualContractError(f"{name} needs at least {minimum} strings")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise MoeVisualContractError(f"{name} must contain nonempty strings")
    if len(value) != len(set(value)):
        raise MoeVisualContractError(f"{name} must remain unique")
    return value


def _validate_image_evidence(
    payload: Any,
    *,
    expected_element_ids: Sequence[str],
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    top = _exact_keys(
        payload,
        {"schema", "created_at", "methodology", "record_count", "records"},
        name="image-search evidence",
    )
    if top["schema"] != IMAGE_EVIDENCE_SCHEMA:
        raise MoeVisualContractError("image-search evidence schema mismatch")
    _string(top["created_at"], name="image-search evidence.created_at")
    methodology = _exact_keys(
        top["methodology"],
        {"search_scope", "content_filter", "interpretation_limit"},
        name="image-search evidence.methodology",
    )
    for key, value in methodology.items():
        _string(value, name=f"image-search evidence.methodology.{key}")
    records = top["records"]
    if not isinstance(records, list) or len(records) != len(expected_element_ids):
        raise MoeVisualContractError("image-search evidence record count drift")
    if top["record_count"] != len(records):
        raise MoeVisualContractError("image-search evidence record_count drift")
    by_id: dict[str, dict[str, Any]] = {}
    seen_elements: list[str] = []
    for index, raw_record in enumerate(records):
        record = _exact_keys(
            raw_record,
            {
                "id",
                "element_id",
                "queries",
                "search_confidence",
                "recurring_features_en",
                "observed_confounds_en",
                "representative_source_urls",
                "limitations_en",
            },
            name=f"image-search evidence record {index}",
        )
        evidence_id = _string(record["id"], name=f"image evidence {index}.id")
        if not re.fullmatch(r"moe_image_evidence_[0-9]{2}", evidence_id):
            raise MoeVisualContractError(f"invalid image evidence id {evidence_id}")
        if evidence_id in by_id:
            raise MoeVisualContractError(f"duplicate image evidence id {evidence_id}")
        element_id = _string(
            record["element_id"], name=f"image evidence {evidence_id}.element_id"
        )
        seen_elements.append(element_id)
        _string_list(record["queries"], name=f"image evidence {evidence_id}.queries")
        if record["search_confidence"] not in SEARCH_CONFIDENCE:
            raise MoeVisualContractError(
                f"image evidence {evidence_id} search confidence drift"
            )
        _string_list(
            record["recurring_features_en"],
            name=f"image evidence {evidence_id}.recurring_features_en",
            minimum=2,
        )
        _string_list(
            record["observed_confounds_en"],
            name=f"image evidence {evidence_id}.observed_confounds_en",
        )
        urls = _string_list(
            record["representative_source_urls"],
            name=f"image evidence {evidence_id}.representative_source_urls",
            minimum=0,
        )
        if any(not url.startswith("https://") for url in urls):
            raise MoeVisualContractError(
                f"image evidence {evidence_id} source URLs must use https"
            )
        _string_list(
            record["limitations_en"],
            name=f"image evidence {evidence_id}.limitations_en",
        )
        by_id[evidence_id] = record
    if seen_elements != list(expected_element_ids):
        raise MoeVisualContractError("image-search evidence element order drift")
    return top, by_id


def load_visual_meaning_contracts(
    path: str | Path,
    *,
    evidence_path: str | Path,
    base_meanings: MoeMeaningContracts,
    expected_element_ids: Sequence[str],
    expected_aliases: Mapping[str, Sequence[str]],
    expected_candidate_subtypes: Mapping[str, set[str]],
) -> MoeVisualMeaningContracts:
    contract_path = Path(path).expanduser().resolve()
    image_path = Path(evidence_path).expanduser().resolve()
    payload, payload_sha = _load_object(contract_path)
    image_payload, image_sha = _load_object(image_path)
    _, evidence_by_id = _validate_image_evidence(
        image_payload, expected_element_ids=expected_element_ids
    )
    top = _exact_keys(
        payload,
        {
            "schema",
            "created_at",
            "base_contract_schema",
            "base_contracts_sha256",
            "image_evidence_schema",
            "image_evidence_sha256",
            "contract_count",
            "contracts",
        },
        name="visual meaning contracts",
    )
    if top["schema"] != VISUAL_MEANING_SCHEMA:
        raise MoeVisualContractError("visual meaning contract schema mismatch")
    if top["base_contract_schema"] != MEANING_SCHEMA:
        raise MoeVisualContractError("visual meaning base schema mismatch")
    if top["base_contracts_sha256"] != base_meanings.sha256:
        raise MoeVisualContractError("visual meaning base contract hash mismatch")
    if top["image_evidence_schema"] != IMAGE_EVIDENCE_SCHEMA:
        raise MoeVisualContractError("visual meaning image evidence schema mismatch")
    if top["image_evidence_sha256"] != image_sha:
        raise MoeVisualContractError("visual meaning image evidence hash mismatch")
    contracts = top["contracts"]
    if not isinstance(contracts, list) or len(contracts) != len(expected_element_ids):
        raise MoeVisualContractError("visual meaning contract count drift")
    if top["contract_count"] != len(contracts):
        raise MoeVisualContractError("visual meaning contract_count drift")

    contracts_by_id: dict[str, dict[str, Any]] = {}
    alias_bindings: dict[str, dict[str, Any]] = {}
    used_evidence_ids: set[str] = set()
    for index, raw_contract in enumerate(contracts):
        name = f"visual meaning contract {index}"
        contract = _exact_keys(
            raw_contract,
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
        element_id = contract["element_id"]
        if element_id != expected_element_ids[index]:
            raise MoeVisualContractError(f"{name} element order drift")
        if contract["ordinal"] != index + 1:
            raise MoeVisualContractError(f"{name} ordinal drift")
        base_contract = base_meanings.contracts_by_id[element_id]
        if contract["base_contract_sha256"] != contract_sha256(base_contract):
            raise MoeVisualContractError(f"{name} base contract hash drift")

        variants = contract["visual_variants"]
        if not isinstance(variants, list) or not variants:
            raise MoeVisualContractError(f"{name}.visual_variants must be nonempty")
        variants_by_id: dict[str, dict[str, Any]] = {}
        subtype_owners: dict[str, str] = {}
        component_group_ids = {
            group["id"] for group in base_contract["component_groups"]
        }
        forbidden_labels = base_contract["runtime_forbidden_labels"]
        for variant_index, raw_variant in enumerate(variants):
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
                name=f"{name}.visual_variants[{variant_index}]",
            )
            variant_id = _string(
                variant["id"], name=f"{name}.visual_variants[{variant_index}].id"
            )
            if not re.fullmatch(r"[a-z][a-z0-9_]+", variant_id):
                raise MoeVisualContractError(f"{name} invalid variant id")
            if variant_id in variants_by_id:
                raise MoeVisualContractError(f"{name} duplicate variant {variant_id}")
            subtype_ids = _string_list(
                variant["candidate_subtype_ids"],
                name=f"{name}.{variant_id}.candidate_subtype_ids",
            )
            for subtype_id in subtype_ids:
                if subtype_id in subtype_owners:
                    raise MoeVisualContractError(
                        f"{name} subtype {subtype_id} belongs to multiple variants"
                    )
                subtype_owners[subtype_id] = variant_id
            required_groups = _string_list(
                variant["required_component_group_ids"],
                name=f"{name}.{variant_id}.required_component_group_ids",
            )
            if set(required_groups) != component_group_ids:
                raise MoeVisualContractError(
                    f"{name}.{variant_id} must bind every base component group"
                )
            phrase_fields = (
                "all_of_en",
                "topology_edges_en",
                "camera_requirements_en",
                "temporal_states_en",
                "interaction_requirements_en",
                "negative_visual_confounds_en",
            )
            for field in phrase_fields:
                minimum = 0 if field in {"temporal_states_en", "interaction_requirements_en"} else 1
                phrases = _string_list(
                    variant[field], name=f"{name}.{variant_id}.{field}", minimum=minimum
                )
                if field != "negative_visual_confounds_en":
                    for label in forbidden_labels:
                        if any(runtime_label_present(label, phrase) for phrase in phrases):
                            raise MoeVisualContractError(
                                f"{name}.{variant_id}.{field} leaks forbidden label {label!r}"
                            )
            any_of = _exact_keys(
                variant["any_of"],
                {"minimum", "alternatives_en"},
                name=f"{name}.{variant_id}.any_of",
            )
            alternatives = _string_list(
                any_of["alternatives_en"],
                name=f"{name}.{variant_id}.any_of.alternatives_en",
                minimum=0,
            )
            minimum = any_of["minimum"]
            if type(minimum) is not int or not 0 <= minimum <= len(alternatives):
                raise MoeVisualContractError(f"{name}.{variant_id}.any_of minimum drift")
            for label in forbidden_labels:
                if any(runtime_label_present(label, phrase) for phrase in alternatives):
                    raise MoeVisualContractError(
                        f"{name}.{variant_id}.any_of leaks forbidden label {label!r}"
                    )
            modes = _string_list(
                variant["supported_output_modes"],
                name=f"{name}.{variant_id}.supported_output_modes",
            )
            if not set(modes).issubset(OUTPUT_MODES):
                raise MoeVisualContractError(f"{name}.{variant_id} output mode drift")
            variants_by_id[variant_id] = variant
        if set(subtype_owners) != expected_candidate_subtypes[element_id]:
            missing = sorted(expected_candidate_subtypes[element_id] - set(subtype_owners))
            extra = sorted(set(subtype_owners) - expected_candidate_subtypes[element_id])
            raise MoeVisualContractError(
                f"{name} candidate subtype coverage drift: missing={missing}, extra={extra}"
            )
        if contract["default_variant_id"] not in variants_by_id:
            raise MoeVisualContractError(f"{name} default variant is unknown")

        raw_aliases = contract["alias_bindings"]
        if not isinstance(raw_aliases, list):
            raise MoeVisualContractError(f"{name}.alias_bindings must be an array")
        alias_phrases: list[str] = []
        for alias_index, raw_alias in enumerate(raw_aliases):
            alias = _exact_keys(
                raw_alias,
                {"alias", "relation", "variant_id"},
                name=f"{name}.alias_bindings[{alias_index}]",
            )
            phrase = _string(alias["alias"], name=f"{name}.alias[{alias_index}]")
            alias_phrases.append(phrase)
            relation = alias["relation"]
            if relation not in ALIAS_RELATIONS:
                raise MoeVisualContractError(f"{name} alias relation drift")
            variant_id = alias["variant_id"]
            if relation == "variant":
                if variant_id not in variants_by_id:
                    raise MoeVisualContractError(
                        f"{name} variant alias {phrase!r} has unknown variant"
                    )
            elif variant_id is not None:
                raise MoeVisualContractError(
                    f"{name} non-variant alias {phrase!r} cannot force a variant"
                )
            normalized = normalize_alias(phrase)
            owner = alias_bindings.get(normalized)
            if owner is not None and owner["element_id"] != element_id:
                raise MoeVisualContractError(
                    f"ambiguous visual alias {phrase!r}: {owner['element_id']} / {element_id}"
                )
            alias_bindings[normalized] = {
                "element_id": element_id,
                "alias": phrase,
                "relation": relation,
                "variant_id": variant_id,
            }
        if alias_phrases != list(expected_aliases[element_id]):
            raise MoeVisualContractError(f"{name} alias inventory or order drift")

        evidence_id = contract["image_evidence_id"]
        evidence = evidence_by_id.get(evidence_id)
        if evidence is None or evidence["element_id"] != element_id:
            raise MoeVisualContractError(f"{name} image evidence binding drift")
        if evidence_id in used_evidence_ids:
            raise MoeVisualContractError(f"duplicate image evidence binding {evidence_id}")
        used_evidence_ids.add(evidence_id)
        contracts_by_id[element_id] = contract

    if set(used_evidence_ids) != set(evidence_by_id):
        raise MoeVisualContractError("orphan image-search evidence records")
    return MoeVisualMeaningContracts(
        path=contract_path,
        evidence_path=image_path,
        payload=top,
        contracts_by_id=contracts_by_id,
        alias_bindings=alias_bindings,
        image_evidence_by_id=evidence_by_id,
        sha256=payload_sha,
        evidence_sha256=image_sha,
    )


__all__ = [
    "ACTIVATING_ALIAS_RELATIONS",
    "ALIAS_RELATIONS",
    "IMAGE_EVIDENCE_FILENAME",
    "IMAGE_EVIDENCE_SCHEMA",
    "MoeVisualContractError",
    "MoeVisualMeaningContracts",
    "VISUAL_MEANING_FILENAME",
    "VISUAL_MEANING_SCHEMA",
    "load_visual_meaning_contracts",
    "normalize_alias",
    "visual_contract_sha256",
]
