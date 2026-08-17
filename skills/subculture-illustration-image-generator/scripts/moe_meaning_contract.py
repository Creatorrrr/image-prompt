#!/usr/bin/env python3
"""Validated canonical/runtime meaning contracts for researched moe elements."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import unicodedata
from typing import Any, Mapping, Sequence


MEANING_SCHEMA = "subculture-illustration-moe-meaning-contracts/v1"
MEANING_FILENAME = "moe_meaning_contracts_v1.json"
DOSSIER_NAMES = {"narrative", "wardrobe", "body", "staging_social", "fantasy"}
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
SINGLE_FRAME_CAPABILITIES = {"exact", "partial", "substrate_only"}
SEQUENCE_CAPABILITIES = {"required", "recommended", "not_required"}
INTERACTION_CAPABILITIES = {"required", "not_required"}
_METADATA_TOKEN = re.compile(
    r"(?:\bSRC_[A-Z0-9_]+\b|\b[a-z]+_(?:def|claim)_\d+\b|"
    r"\bsource_supported\b|\bresearched_variant_\d+\b)"
)


class MoeMeaningContractError(ValueError):
    """Raised when canonical meaning data is incomplete or provenance drifts."""


@dataclass(frozen=True)
class MoeMeaningContracts:
    path: Path
    payload: dict[str, Any]
    contracts_by_id: dict[str, dict[str, Any]]
    sha256: str


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def contract_sha256(contract: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_json_bytes(dict(contract))).hexdigest()


def _exact_keys(value: Any, expected: set[str], *, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise MoeMeaningContractError(f"{name} must be an object")
    if set(value) != expected:
        missing = sorted(expected - set(value))
        extra = sorted(set(value) - expected)
        raise MoeMeaningContractError(
            f"{name} keys drift: missing={missing}, extra={extra}"
        )
    return value


def _nonempty_string(value: Any, *, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise MoeMeaningContractError(f"{name} must be a nonempty string")
    return value


def _string_list(
    value: Any,
    *,
    name: str,
    minimum: int = 1,
) -> list[str]:
    if not isinstance(value, list) or len(value) < minimum:
        raise MoeMeaningContractError(f"{name} needs at least {minimum} strings")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise MoeMeaningContractError(f"{name} must contain nonempty strings")
    if len(value) != len(set(value)):
        raise MoeMeaningContractError(f"{name} must remain unique")
    return value


def normalize_runtime_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    normalized = re.sub(r"[^\w]+", " ", normalized, flags=re.UNICODE)
    return " ".join(normalized.split())


def runtime_label_present(label: str, text: str) -> bool:
    normalized_label = normalize_runtime_text(label)
    normalized_text = normalize_runtime_text(text)
    if not normalized_label or not normalized_text:
        return False
    return bool(
        re.search(
            rf"(?<!\w){re.escape(normalized_label)}(?!\w)",
            normalized_text,
            flags=re.UNICODE,
        )
    )


def _validate_contract(
    raw_contract: Any,
    *,
    index: int,
    expected_element_id: str,
) -> dict[str, Any]:
    name = f"meaning contract {index}"
    contract = _exact_keys(
        raw_contract,
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
    if contract["element_id"] != expected_element_id:
        raise MoeMeaningContractError(
            f"{name} element order drift: {contract['element_id']} != {expected_element_id}"
        )
    if contract["ordinal"] != index + 1:
        raise MoeMeaningContractError(f"{name} ordinal drift")
    if contract["source_dossier"] not in DOSSIER_NAMES:
        raise MoeMeaningContractError(f"{name} source_dossier drift")
    definition = _nonempty_string(
        contract["canonical_definition_ko"],
        name=f"{name}.canonical_definition_ko",
    )
    if _METADATA_TOKEN.search(definition):
        raise MoeMeaningContractError(
            f"{name}.canonical_definition_ko contains provenance metadata"
        )
    _string_list(
        contract["essential_semantics_ko"],
        name=f"{name}.essential_semantics_ko",
        minimum=2,
    )
    _string_list(
        contract["non_equivalents_ko"],
        name=f"{name}.non_equivalents_ko",
        minimum=2,
    )
    axes = _string_list(
        contract["semantic_axes"],
        name=f"{name}.semantic_axes",
        minimum=2,
    )
    if any(not re.fullmatch(r"[a-z][a-z0-9_]+", axis) for axis in axes):
        raise MoeMeaningContractError(f"{name}.semantic_axes needs typed IDs")

    label_policy = contract["runtime_label_policy"]
    if label_policy not in LABEL_POLICIES:
        raise MoeMeaningContractError(f"{name}.runtime_label_policy drift")
    forbidden = _string_list(
        contract["runtime_forbidden_labels"],
        name=f"{name}.runtime_forbidden_labels",
        minimum=0,
    )
    if label_policy != "allow" and not forbidden:
        raise MoeMeaningContractError(
            f"{name} non-allow label policy needs runtime_forbidden_labels"
        )
    fidelity = contract["semantic_fidelity"]
    if fidelity not in SEMANTIC_FIDELITIES:
        raise MoeMeaningContractError(f"{name}.semantic_fidelity drift")

    groups = contract["component_groups"]
    if not isinstance(groups, list) or len(groups) < 2:
        raise MoeMeaningContractError(f"{name}.component_groups needs at least two")
    group_ids: set[str] = set()
    for group_index, raw_group in enumerate(groups):
        group = _exact_keys(
            raw_group,
            {"id", "minimum", "alternatives_en"},
            name=f"{name}.component_groups[{group_index}]",
        )
        group_id = group["id"]
        if not isinstance(group_id, str) or not re.fullmatch(
            r"[a-z][a-z0-9_]+", group_id
        ):
            raise MoeMeaningContractError(f"{name} has invalid component group id")
        if group_id in group_ids:
            raise MoeMeaningContractError(f"{name} has duplicate component group")
        group_ids.add(group_id)
        alternatives = _string_list(
            group["alternatives_en"],
            name=f"{name}.{group_id}.alternatives_en",
        )
        for label in forbidden:
            if any(runtime_label_present(label, item) for item in alternatives):
                raise MoeMeaningContractError(
                    f"{name}.{group_id} leaks forbidden runtime label {label!r}"
                )
        minimum = group["minimum"]
        if type(minimum) is not int or not 1 <= minimum <= len(alternatives):
            raise MoeMeaningContractError(f"{name}.{group_id}.minimum is invalid")
    _string_list(
        contract["optional_components_en"],
        name=f"{name}.optional_components_en",
        minimum=0,
    )
    _string_list(
        contract["false_substitutes_en"],
        name=f"{name}.false_substitutes_en",
    )
    _string_list(
        contract["do_not_infer_en"],
        name=f"{name}.do_not_infer_en",
    )
    if contract["adult_requirement"] not in ADULT_REQUIREMENTS:
        raise MoeMeaningContractError(f"{name}.adult_requirement drift")

    capability = _exact_keys(
        contract["capability"],
        {"single_frame", "sequence", "interaction"},
        name=f"{name}.capability",
    )
    if capability["single_frame"] not in SINGLE_FRAME_CAPABILITIES:
        raise MoeMeaningContractError(f"{name}.capability.single_frame drift")
    if capability["sequence"] not in SEQUENCE_CAPABILITIES:
        raise MoeMeaningContractError(f"{name}.capability.sequence drift")
    if capability["interaction"] not in INTERACTION_CAPABILITIES:
        raise MoeMeaningContractError(f"{name}.capability.interaction drift")
    if fidelity == "sequence_required" and capability["sequence"] != "required":
        raise MoeMeaningContractError(f"{name} sequence fidelity/capability mismatch")
    if fidelity == "interaction_required" and capability["interaction"] != "required":
        raise MoeMeaningContractError(
            f"{name} interaction fidelity/capability mismatch"
        )
    return contract


def load_meaning_contracts(
    path: str | Path,
    *,
    expected_element_ids: Sequence[str],
) -> MoeMeaningContracts:
    resolved = Path(path).expanduser().resolve()
    try:
        raw = resolved.read_bytes()
    except OSError as exc:
        raise MoeMeaningContractError(f"cannot read {resolved}: {exc}") from exc
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise MoeMeaningContractError(f"invalid JSON in {resolved}: {exc}") from exc
    top = _exact_keys(
        payload,
        {
            "schema",
            "created_at",
            "source_dossier_hashes",
            "contract_count",
            "contracts",
        },
        name="meaning contracts",
    )
    if top["schema"] != MEANING_SCHEMA:
        raise MoeMeaningContractError("meaning contract schema mismatch")
    _nonempty_string(top["created_at"], name="meaning contracts.created_at")
    source_hashes = _exact_keys(
        top["source_dossier_hashes"],
        DOSSIER_NAMES,
        name="meaning contracts.source_dossier_hashes",
    )
    dossier_root = resolved.parent / "dossiers_v2"
    for dossier_name in sorted(DOSSIER_NAMES):
        digest = source_hashes[dossier_name]
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise MoeMeaningContractError(
                f"meaning contracts {dossier_name} digest is invalid"
            )
        try:
            actual = hashlib.sha256(
                (dossier_root / f"{dossier_name}.json").read_bytes()
            ).hexdigest()
        except OSError as exc:
            raise MoeMeaningContractError(
                f"cannot read source dossier {dossier_name}: {exc}"
            ) from exc
        if actual != digest:
            raise MoeMeaningContractError(
                f"meaning contracts {dossier_name} source hash mismatch"
            )

    contracts = top["contracts"]
    if not isinstance(contracts, list):
        raise MoeMeaningContractError("meaning contracts must be an array")
    if top["contract_count"] != len(contracts) or len(contracts) != len(
        expected_element_ids
    ):
        raise MoeMeaningContractError("meaning contract count drift")
    contracts_by_id: dict[str, dict[str, Any]] = {}
    for index, (raw_contract, expected_element_id) in enumerate(
        zip(contracts, expected_element_ids, strict=True)
    ):
        contract = _validate_contract(
            raw_contract,
            index=index,
            expected_element_id=expected_element_id,
        )
        element_id = contract["element_id"]
        if element_id in contracts_by_id:
            raise MoeMeaningContractError(f"duplicate meaning contract {element_id}")
        contracts_by_id[element_id] = contract
    return MoeMeaningContracts(
        path=resolved,
        payload=top,
        contracts_by_id=contracts_by_id,
        sha256=hashlib.sha256(raw).hexdigest(),
    )


__all__ = [
    "MEANING_FILENAME",
    "MEANING_SCHEMA",
    "MoeMeaningContractError",
    "MoeMeaningContracts",
    "contract_sha256",
    "load_meaning_contracts",
    "runtime_label_present",
]
