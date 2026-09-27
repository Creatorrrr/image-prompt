#!/usr/bin/env python3
"""Deterministic, explicit-only planning for researched moe elements.

This module is deliberately additive. It does not alter the historical v1-v4
assets, base pack, safety metadata, negative prompt, retry policy, or universal
selector. A caller explicitly names one to three element IDs or reviewed
aliases. The default v5 path emits a visual-meaning-aware v7 wrapper; explicit
v4/v3/v2 replay the historical v6/v5/v4 wrappers.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import unicodedata
from typing import Any, Mapping, Sequence

from moe_meaning_contract import (
    MEANING_FILENAME,
    MEANING_SCHEMA,
    MoeMeaningContractError,
    contract_sha256,
    load_meaning_contracts,
    runtime_label_present,
)
from moe_visual_contract import (
    ACTIVATING_ALIAS_RELATIONS,
    IMAGE_EVIDENCE_FILENAME,
    IMAGE_EVIDENCE_SCHEMA,
    VISUAL_MEANING_FILENAME,
    VISUAL_MEANING_SCHEMA,
    MoeVisualContractError,
    MoeVisualMeaningContracts,
    load_visual_meaning_contracts,
    normalize_alias,
    visual_contract_sha256,
)
from moe_visual_addition import (
    ACTIVATING_ALIAS_RELATIONS_V2,
    ADDITION_FILENAME,
    GRAMMAR_SCHEMA_V5,
    MoeVisualAdditionError,
    MoeVisualAdditions,
    build_v5_manifest,
    load_moe_visual_additions,
)


ASSET_SCHEMA = "subculture-illustration-moe-elements/v1"
RESEARCH_SCHEMA = "subculture-illustration-moe-element-research/v1"
PLAN_SCHEMA = "subculture-illustration-moe-element-plan/v1"
AUDIT_SCHEMA = "subculture-illustration-moe-element-audit/v1"
GRAMMAR_SCHEMA_V2 = "subculture-illustration-moe-grammar/v2"
GRAMMAR_SCHEMA = "subculture-illustration-moe-grammar/v3"
GRAMMAR_SCHEMA_V4 = "subculture-illustration-moe-grammar/v4"
PACK_SCHEMA_V4 = "subculture-illustration-candidate-pack/v4"
PACK_SCHEMA = "subculture-illustration-candidate-pack/v5"
PACK_SCHEMA_V6 = "subculture-illustration-candidate-pack/v6"
PACK_SCHEMA_V7 = "subculture-illustration-candidate-pack/v7"
COMPOSED_SCHEMA_V2 = "subculture-illustration-moe-composed-prompt/v2"
COMPOSED_SCHEMA = "subculture-illustration-moe-composed-prompt/v3"
COMPOSED_SCHEMA_V4 = "subculture-illustration-moe-composed-prompt/v4"
COMPOSED_SCHEMA_V5 = "subculture-illustration-moe-composed-prompt/v5"
PACK_AUDIT_SCHEMA_V2 = "subculture-illustration-moe-candidate-pack-audit/v2"
PACK_AUDIT_SCHEMA = "subculture-illustration-moe-candidate-pack-audit/v3"
PACK_AUDIT_SCHEMA_V4 = "subculture-illustration-moe-candidate-pack-audit/v4"
PACK_AUDIT_SCHEMA_V5 = "subculture-illustration-moe-candidate-pack-audit/v5"
MAX_SELECTED_ELEMENTS = 3
REPRESENTATION_MODES = {
    "single_frame",
    "paired_or_sequence",
    "sequence",
    "optical_interaction",
}
OUTPUT_MODES = {
    "auto",
    "single_frame",
    "paired_frame",
    "sequence",
    "optical_interaction",
}
MECHANISM_TYPES = {
    "narrative_state",
    "relationship_viewpoint",
    "character_archetype",
    "wardrobe_construction",
    "body_pose",
    "expression_code",
    "composition_device",
    "participatory_meme",
    "fantasy_hazard",
}


class MoeElementError(ValueError):
    """Raised when the explicit moe-element contract cannot be satisfied."""


@dataclass(frozen=True)
class MoeElementAssets:
    asset_dir: Path
    payload: dict[str, Any]
    research: dict[str, Any]
    records_by_id: dict[str, dict[str, Any]]
    alias_to_id: dict[str, str]
    source_ids: frozenset[str]
    element_asset_sha256: str
    research_sha256: str


@dataclass(frozen=True)
class MoeGrammarAssets:
    """Validated research dossiers and executable candidate bundles."""

    asset_dir: Path
    payload: dict[str, Any]
    elements_by_id: dict[str, dict[str, Any]]
    candidates_by_id: dict[str, dict[str, Any]]
    grammar_sha256: str
    compatibility: dict[str, Any]
    compatibility_sha256: str
    version: str
    visual_contracts: MoeVisualMeaningContracts | None
    visual_additions: MoeVisualAdditions | None = None


def default_asset_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "assets"


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    normalized = re.sub(r"[^\w]+", " ", normalized, flags=re.UNICODE)
    return " ".join(normalized.split())


def _load_json(path: Path) -> tuple[dict[str, Any], str]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise MoeElementError(f"cannot read {path}: {exc}") from exc
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise MoeElementError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise MoeElementError(f"{path} must contain one JSON object")
    return payload, hashlib.sha256(raw).hexdigest()


def _string_list(value: Any, *, name: str, nonempty: bool = True) -> list[str]:
    if not isinstance(value, list) or (nonempty and not value):
        raise MoeElementError(
            f"{name} must be a{' nonempty' if nonempty else ''} string array"
        )
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise MoeElementError(f"{name} must contain nonempty strings")
    if len(value) != len(set(value)):
        raise MoeElementError(f"{name} must not contain duplicates")
    return list(value)


def load_moe_element_assets(asset_dir: str | Path | None = None) -> MoeElementAssets:
    root = Path(asset_dir).expanduser().resolve() if asset_dir else default_asset_dir()
    payload, element_sha = _load_json(root / "illustration_moe_elements_v1.json")
    research, research_sha = _load_json(
        root / "research_evidence_moe_elements" / "research_v1.json"
    )
    if payload.get("schema") != ASSET_SCHEMA:
        raise MoeElementError("moe-element asset schema mismatch")
    if research.get("schema") != RESEARCH_SCHEMA:
        raise MoeElementError("moe-element research schema mismatch")
    if payload.get("research_sha256") != research_sha:
        raise MoeElementError("moe-element research hash mismatch")

    sources = research.get("sources")
    if not isinstance(sources, list) or not sources:
        raise MoeElementError("research.sources must be a nonempty array")
    source_ids: set[str] = set()
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            raise MoeElementError(f"research source {index} must be an object")
        required = {"id", "kind", "title", "url", "publisher", "claim_scope"}
        if set(source) != required:
            raise MoeElementError(f"research source {index} keys drift")
        source_id = source.get("id")
        if not isinstance(source_id, str) or not source_id:
            raise MoeElementError(f"research source {index} has no id")
        if source_id in source_ids:
            raise MoeElementError(f"duplicate research source id {source_id}")
        if source.get("kind") not in {"origin_record", "independent_source"}:
            raise MoeElementError(f"research source {source_id} has invalid kind")
        if not isinstance(source.get("url"), str) or not str(source["url"]).startswith(
            "https://"
        ):
            raise MoeElementError(f"research source {source_id} must use an https URL")
        source_ids.add(source_id)

    records = payload.get("elements")
    if not isinstance(records, list) or len(records) != 29:
        raise MoeElementError("moe-element asset must contain exactly 29 elements")
    if payload.get("element_count") != 29:
        raise MoeElementError("moe-element element_count must be 29")
    records_by_id: dict[str, dict[str, Any]] = {}
    alias_to_id: dict[str, str] = {}
    ordinals: list[int] = []
    expected_keys = {
        "id",
        "ordinal",
        "category",
        "label_ko",
        "label_en",
        "aliases",
        "mechanism_type",
        "representation_mode",
        "prompt_clause_en",
        "evidence_groups_en",
        "observable_evidence",
        "incompatible_with",
        "origin_source_ids",
        "independent_source_ids",
        "limitation",
        "design_inference",
    }
    for index, record in enumerate(records):
        if not isinstance(record, dict) or set(record) != expected_keys:
            raise MoeElementError(f"moe-element record {index} keys drift")
        element_id = record.get("id")
        if not isinstance(element_id, str) or not re.fullmatch(
            r"moe_[a-z0-9_]+", element_id
        ):
            raise MoeElementError(f"moe-element record {index} has invalid id")
        if element_id in records_by_id:
            raise MoeElementError(f"duplicate moe-element id {element_id}")
        ordinal = record.get("ordinal")
        if type(ordinal) is not int:
            raise MoeElementError(
                f"moe-element {element_id} ordinal must be an integer"
            )
        ordinals.append(ordinal)
        if record.get("mechanism_type") not in MECHANISM_TYPES:
            raise MoeElementError(
                f"moe-element {element_id} has invalid mechanism_type"
            )
        if record.get("representation_mode") not in REPRESENTATION_MODES:
            raise MoeElementError(
                f"moe-element {element_id} has invalid representation_mode"
            )
        aliases = _string_list(record.get("aliases"), name=f"{element_id}.aliases")
        evidence_groups = record.get("evidence_groups_en")
        if not isinstance(evidence_groups, list) or not evidence_groups:
            raise MoeElementError(f"{element_id}.evidence_groups_en must be nonempty")
        for group_index, group in enumerate(evidence_groups):
            _string_list(group, name=f"{element_id}.evidence_groups_en[{group_index}]")
        _string_list(
            record.get("observable_evidence"), name=f"{element_id}.observable_evidence"
        )
        incompatible = _string_list(
            record.get("incompatible_with"),
            name=f"{element_id}.incompatible_with",
            nonempty=False,
        )
        origin_ids = _string_list(
            record.get("origin_source_ids"), name=f"{element_id}.origin_source_ids"
        )
        independent_ids = _string_list(
            record.get("independent_source_ids"),
            name=f"{element_id}.independent_source_ids",
        )
        for source_id in [*origin_ids, *independent_ids]:
            if source_id not in source_ids:
                raise MoeElementError(
                    f"{element_id} references unknown source {source_id}"
                )
        if (
            not isinstance(record.get("prompt_clause_en"), str)
            or not record["prompt_clause_en"].strip()
        ):
            raise MoeElementError(f"{element_id}.prompt_clause_en must be nonempty")
        for field in (
            "label_ko",
            "label_en",
            "limitation",
            "design_inference",
            "category",
        ):
            if not isinstance(record.get(field), str) or not record[field].strip():
                raise MoeElementError(f"{element_id}.{field} must be nonempty")

        records_by_id[element_id] = record
        candidates = [element_id, record["label_ko"], record["label_en"], *aliases]
        for candidate in candidates:
            normalized = normalize_text(candidate)
            if not normalized:
                raise MoeElementError(f"{element_id} exposes an empty normalized alias")
            owner = alias_to_id.get(normalized)
            if owner is not None and owner != element_id:
                raise MoeElementError(
                    f"ambiguous reviewed alias {candidate!r}: {owner} and {element_id}"
                )
            alias_to_id[normalized] = element_id

        for target in incompatible:
            if target == element_id:
                raise MoeElementError(f"{element_id} cannot conflict with itself")

    if ordinals != list(range(1, 30)):
        raise MoeElementError("moe-element ordinals must be exact 1..29 order")
    for element_id, record in records_by_id.items():
        for target in record["incompatible_with"]:
            if target not in records_by_id:
                raise MoeElementError(
                    f"{element_id} conflicts with unknown element {target}"
                )
            if element_id not in records_by_id[target]["incompatible_with"]:
                raise MoeElementError(
                    f"incompatibility must be symmetric: {element_id} / {target}"
                )

    category_counts = payload.get("category_counts")
    if not isinstance(category_counts, dict):
        raise MoeElementError("category_counts must be an object")
    actual_counts: dict[str, int] = {}
    for record in records:
        actual_counts[record["category"]] = actual_counts.get(record["category"], 0) + 1
    if category_counts != actual_counts:
        raise MoeElementError("category_counts do not match the 29 records")
    if research.get("element_ids") != list(records_by_id):
        raise MoeElementError("research element_ids must exactly match asset order")

    return MoeElementAssets(
        asset_dir=root,
        payload=payload,
        research=research,
        records_by_id=records_by_id,
        alias_to_id=alias_to_id,
        source_ids=frozenset(source_ids),
        element_asset_sha256=element_sha,
        research_sha256=research_sha,
    )


def resolve_element_tokens(
    requested_tokens: Sequence[str],
    *,
    assets: MoeElementAssets | None = None,
) -> list[dict[str, Any]]:
    """Resolve explicit IDs or complete reviewed aliases.

    This function never scans an arbitrary concept for substrings.  Passing an
    empty sequence is the explicit unselected baseline.
    """

    if isinstance(requested_tokens, (str, bytes, bytearray)) or not isinstance(
        requested_tokens, Sequence
    ):
        raise MoeElementError("requested_tokens must be an array")
    if len(requested_tokens) > MAX_SELECTED_ELEMENTS:
        raise MoeElementError(
            f"at most {MAX_SELECTED_ELEMENTS} moe elements may be selected"
        )
    runtime_assets = assets or load_moe_element_assets()
    selected_ids: list[str] = []
    for index, token in enumerate(requested_tokens):
        if not isinstance(token, str) or not token.strip():
            raise MoeElementError(f"requested token {index} must be a nonempty string")
        normalized = normalize_text(token)
        element_id = runtime_assets.alias_to_id.get(normalized)
        if element_id is None:
            raise MoeElementError(f"unknown moe element or reviewed alias: {token!r}")
        if element_id in selected_ids:
            raise MoeElementError(f"duplicate moe element selection: {element_id}")
        selected_ids.append(element_id)
    selected = [runtime_assets.records_by_id[element_id] for element_id in selected_ids]
    selected_set = set(selected_ids)
    for record in selected:
        conflicts = selected_set.intersection(record["incompatible_with"])
        if conflicts:
            raise MoeElementError(
                f"incompatible moe elements: {record['id']} / {sorted(conflicts)[0]}"
            )
    return selected


def _resolve_visual_element_bindings(
    requested_tokens: Sequence[str],
    *,
    legacy: MoeElementAssets,
    grammar: MoeGrammarAssets,
) -> list[dict[str, Any]]:
    """Resolve typed visual tokens without treating nearby terms as identity."""

    if grammar.version not in {"v4", "v5"} or grammar.visual_contracts is None:
        raise MoeElementError(
            "typed visual alias resolution requires the v5 or v4 grammar"
        )
    if isinstance(requested_tokens, (str, bytes, bytearray)) or not isinstance(
        requested_tokens, Sequence
    ):
        raise MoeElementError("requested_tokens must be an array")
    if len(requested_tokens) > MAX_SELECTED_ELEMENTS:
        raise MoeElementError(
            f"at most {MAX_SELECTED_ELEMENTS} moe elements may be selected"
        )

    canonical_ids: dict[str, str] = {}
    canonical_labels: dict[str, str] = {}
    for element_id, record in grammar.elements_by_id.items():
        canonical_ids[normalize_alias(element_id)] = element_id
        labels = [record.get("label_ko"), record.get("label_en")]
        if element_id in legacy.records_by_id:
            labels.append(legacy.records_by_id[element_id].get("label_en"))
        for token in labels:
            if not isinstance(token, str) or not token.strip():
                continue
            canonical_labels[normalize_alias(str(token))] = element_id

    bindings: list[dict[str, Any]] = []
    selected_ids: list[str] = []
    for index, token in enumerate(requested_tokens):
        if not isinstance(token, str) or not token.strip():
            raise MoeElementError(f"requested token {index} must be a nonempty string")
        normalized = normalize_alias(token)
        element_id = canonical_ids.get(normalized)
        relation = "canonical"
        variant_id = None
        if element_id is None:
            alias_binding = grammar.visual_contracts.alias_bindings.get(normalized)
            if alias_binding is not None:
                relation = str(alias_binding["relation"])
                element_id = str(alias_binding["element_id"])
                variant_id = alias_binding["variant_id"]
                activating_relations = (
                    ACTIVATING_ALIAS_RELATIONS_V2
                    if grammar.version == "v5"
                    else ACTIVATING_ALIAS_RELATIONS
                )
                if relation not in activating_relations:
                    if relation == "ambiguous":
                        contract = grammar.visual_contracts.contracts_by_id[
                            element_id
                        ]
                        choices = [
                            binding["alias"]
                            for binding in contract["alias_bindings"]
                            if binding["relation"] == "variant"
                        ]
                        raise MoeElementError(
                            f"ambiguous visual keyword {token!r}; choose a reviewed "
                            f"variant alias such as {', '.join(repr(item) for item in choices[:3])}"
                        )
                    raise MoeElementError(
                        f"related-only keyword {token!r} does not uniquely name "
                        f"{element_id}; use its canonical ID or an exact, variant, "
                        "or carrier alias"
                    )
            else:
                element_id = canonical_labels.get(normalized)
            if element_id is None:
                raise MoeElementError(
                    f"unknown moe element or reviewed alias: {token!r}"
                )
        if element_id in selected_ids:
            raise MoeElementError(f"duplicate moe element selection: {element_id}")
        selected_ids.append(element_id)
        bindings.append(
            {
                "requested_token": token,
                "element_id": element_id,
                "alias_relation": relation,
                "requested_variant_id": variant_id,
            }
        )

    return bindings


def _required_output_modes(records: Sequence[Mapping[str, Any]]) -> list[str]:
    modes = {str(record["representation_mode"]) for record in records}
    if (
        "optical_interaction" in modes
        and len(modes - {"single_frame", "optical_interaction"}) > 0
    ):
        raise MoeElementError(
            "optical interaction cannot share one plan with a sequence-only element"
        )
    if "optical_interaction" in modes:
        return ["optical_interaction"]
    if "sequence" in modes:
        return ["sequence"]
    if "paired_or_sequence" in modes:
        return ["paired_frame", "sequence"]
    return ["single_frame", "paired_frame", "sequence"]


def build_moe_element_plan(
    requested_tokens: Sequence[str],
    *,
    output_mode: str = "auto",
    assets: MoeElementAssets | None = None,
) -> dict[str, Any]:
    if output_mode not in OUTPUT_MODES:
        raise MoeElementError(f"unsupported output_mode {output_mode!r}")
    runtime_assets = assets or load_moe_element_assets()
    selected = resolve_element_tokens(requested_tokens, assets=runtime_assets)
    allowed_modes = _required_output_modes(selected)
    resolved_output_mode = allowed_modes[0] if output_mode == "auto" else output_mode
    if output_mode != "auto" and output_mode not in allowed_modes:
        raise MoeElementError(
            f"output_mode {output_mode!r} cannot prove the selected elements; "
            f"use one of {allowed_modes}"
        )

    ordered = sorted(selected, key=lambda record: int(record["ordinal"]))
    prompt_clauses = [str(record["prompt_clause_en"]) for record in ordered]
    plan: dict[str, Any] = {
        "schema": PLAN_SCHEMA,
        "plan_id": None,
        "selection_mode": "explicit_id_or_complete_reviewed_alias_only",
        "requested_tokens": list(requested_tokens),
        "selected_element_ids": [record["id"] for record in ordered],
        "required_candidate_ids": [f"moe:{record['id']}" for record in ordered],
        "frame_contract": {
            "requested_output_mode": output_mode,
            "resolved_output_mode": resolved_output_mode,
            "allowed_output_modes": allowed_modes,
            "single_frame_sufficient": resolved_output_mode == "single_frame",
            "limitations": [record["limitation"] for record in ordered],
        },
        "composition": {
            "prompt_block_en": ". ".join(prompt_clauses)
            + ("." if prompt_clauses else ""),
            "elements": [
                {
                    "element_id": record["id"],
                    "mechanism_type": record["mechanism_type"],
                    "representation_mode": record["representation_mode"],
                    "prompt_clause_en": record["prompt_clause_en"],
                    "evidence_groups_en": record["evidence_groups_en"],
                    "observable_evidence": record["observable_evidence"],
                    "design_inference": record["design_inference"],
                }
                for record in ordered
            ],
        },
        "source_trace": [
            {
                "element_id": record["id"],
                "origin_source_ids": record["origin_source_ids"],
                "independent_source_ids": record["independent_source_ids"],
            }
            for record in ordered
        ],
        "asset_hashes": {
            "moe_elements_sha256": runtime_assets.element_asset_sha256,
            "moe_research_sha256": runtime_assets.research_sha256,
        },
        "nonclaims": list(runtime_assets.payload["nonclaims"]),
    }
    plan["plan_id"] = hashlib.sha256(canonical_json_bytes(plan)).hexdigest()
    return plan


def _normalized_phrase_contains(haystack: str, needle: str) -> bool:
    haystack_norm = f" {normalize_text(haystack)} "
    needle_norm = normalize_text(needle)
    return bool(needle_norm) and f" {needle_norm} " in haystack_norm


def audit_moe_element_prompt(
    plan: Mapping[str, Any],
    prompt_en: str,
    *,
    assets: MoeElementAssets | None = None,
) -> dict[str, Any]:
    runtime_assets = assets or load_moe_element_assets()
    failures: list[dict[str, Any]] = []
    if plan.get("schema") != PLAN_SCHEMA:
        failures.append({"check": "schema", "message": "plan schema mismatch"})
    if not isinstance(prompt_en, str) or not prompt_en.strip():
        failures.append({"check": "prompt", "message": "prompt_en must be nonempty"})
        prompt_en = ""
    supplied_plan_id = plan.get("plan_id")
    replay_input = dict(plan)
    replay_input["plan_id"] = None
    expected_plan_id = hashlib.sha256(canonical_json_bytes(replay_input)).hexdigest()
    if supplied_plan_id != expected_plan_id:
        failures.append(
            {"check": "plan_id", "message": "plan_id does not match canonical bytes"}
        )
    hashes = plan.get("asset_hashes")
    if hashes != {
        "moe_elements_sha256": runtime_assets.element_asset_sha256,
        "moe_research_sha256": runtime_assets.research_sha256,
    }:
        failures.append({"check": "asset_hashes", "message": "plan asset hashes drift"})

    requested = plan.get("requested_tokens")
    frame = plan.get("frame_contract")
    try:
        replayed = build_moe_element_plan(
            requested if isinstance(requested, list) else [],
            output_mode=(
                str(frame.get("requested_output_mode"))
                if isinstance(frame, Mapping)
                else "auto"
            ),
            assets=runtime_assets,
        )
        if canonical_json_bytes(replayed) != canonical_json_bytes(dict(plan)):
            failures.append(
                {"check": "replay", "message": "plan differs from deterministic replay"}
            )
    except MoeElementError as exc:
        failures.append({"check": "replay", "message": str(exc)})

    composition = plan.get("composition")
    elements = composition.get("elements") if isinstance(composition, Mapping) else None
    evidence: list[dict[str, Any]] = []
    if not isinstance(elements, list):
        failures.append(
            {"check": "composition", "message": "composition.elements must be an array"}
        )
        elements = []
    for element in elements:
        if not isinstance(element, Mapping):
            failures.append(
                {
                    "check": "composition",
                    "message": "element evidence must be an object",
                }
            )
            continue
        element_id = str(element.get("element_id") or "")
        groups = element.get("evidence_groups_en")
        missing_groups: list[int] = []
        if not isinstance(groups, list):
            missing_groups.append(0)
        else:
            for group_index, alternatives in enumerate(groups):
                if not isinstance(alternatives, list) or not any(
                    isinstance(alternative, str)
                    and _normalized_phrase_contains(prompt_en, alternative)
                    for alternative in alternatives
                ):
                    missing_groups.append(group_index)
        if missing_groups:
            failures.append(
                {
                    "check": "literal_evidence",
                    "element_id": element_id,
                    "missing_group_indexes": missing_groups,
                }
            )
        evidence.append(
            {
                "element_id": element_id,
                "evidence_groups_pass": not missing_groups,
            }
        )
    return {
        "schema": AUDIT_SCHEMA,
        "status": "pass" if not failures else "fail",
        "plan_id": supplied_plan_id,
        "selected_element_count": len(elements),
        "evidence": evidence,
        "failures": failures,
    }


def list_moe_elements(assets: MoeElementAssets | None = None) -> list[dict[str, Any]]:
    runtime_assets = assets or load_moe_element_assets()
    return [
        {
            "ordinal": record["ordinal"],
            "id": record["id"],
            "category": record["category"],
            "label_ko": record["label_ko"],
            "label_en": record["label_en"],
            "representation_mode": record["representation_mode"],
        }
        for record in runtime_assets.payload["elements"]
    ]


def _exact_keys(value: Any, expected: set[str], *, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise MoeElementError(f"{name} must be an object")
    if set(value) != expected:
        missing = sorted(expected - set(value))
        extra = sorted(set(value) - expected)
        raise MoeElementError(f"{name} keys drift: missing={missing}, extra={extra}")
    return value


def _validated_atom(value: Any, *, name: str, atom_ids: set[str]) -> dict[str, Any]:
    atom = _exact_keys(
        value,
        {"id", "prompt_fragment_en", "observable_evidence"},
        name=name,
    )
    atom_id = atom["id"]
    if not isinstance(atom_id, str) or not re.fullmatch(
        r"moe_atom_[a-z0-9_]+", atom_id
    ):
        raise MoeElementError(f"{name}.id must be a typed moe_atom ID")
    if atom_id in atom_ids:
        raise MoeElementError(f"duplicate moe atom id {atom_id}")
    atom_ids.add(atom_id)
    if (
        not isinstance(atom["prompt_fragment_en"], str)
        or not atom["prompt_fragment_en"].strip()
    ):
        raise MoeElementError(f"{name}.prompt_fragment_en must be nonempty")
    _string_list(atom["observable_evidence"], name=f"{name}.observable_evidence")
    return atom


def load_moe_grammar_assets(
    asset_dir: str | Path | None = None,
    *,
    legacy_assets: MoeElementAssets | None = None,
    grammar_version: str = "v5",
) -> MoeGrammarAssets:
    """Load current v5 additions or explicit historical v4/v3/v2 replay.

    The v1 inventory stays byte-stable and remains the authority for explicit
    element IDs. V4 types aliases and visual variants, v3 adds canonical/runtime
    meaning contracts, and v2 remains available only through explicit replay.
    """

    root = Path(asset_dir).expanduser().resolve() if asset_dir else default_asset_dir()
    legacy = legacy_assets or load_moe_element_assets(root)
    if grammar_version == "v5":
        return _load_moe_grammar_v5_assets(root, legacy)
    if grammar_version not in {"v2", "v3", "v4"}:
        raise MoeElementError("grammar_version must be v5, v4, v3, or v2")
    grammar_schema = {
        "v2": GRAMMAR_SCHEMA_V2,
        "v3": GRAMMAR_SCHEMA,
        "v4": GRAMMAR_SCHEMA_V4,
    }[grammar_version]
    payload, grammar_sha = _load_json(
        root / f"illustration_moe_grammar_{grammar_version}.json"
    )
    compatibility, compatibility_sha = _load_json(
        root / "illustration_moe_compatibility_v2.json"
    )
    grammar_keys = {
        "schema",
        "created_at",
        "legacy_element_asset_sha256",
        "legacy_research_sha256",
        "research_dossier_hashes",
        "intent_corpus_sha256",
        "compatibility_sha256",
        "element_count",
        "candidate_count",
        "source_count",
        "sources",
        "selection_contract",
        "compatibility_rules",
        "elements",
    }
    if grammar_version in {"v3", "v4"}:
        grammar_keys.update({"meaning_contract_schema", "meaning_contracts_sha256"})
    if grammar_version == "v4":
        grammar_keys.update(
            {
                "base_grammar_v3_sha256",
                "visual_meaning_contract_schema",
                "visual_meaning_contracts_sha256",
                "image_search_evidence_schema",
                "image_search_evidence_sha256",
            }
        )
    top = _exact_keys(
        payload,
        grammar_keys,
        name="moe grammar",
    )
    if top["schema"] != grammar_schema:
        raise MoeElementError("moe grammar schema mismatch")
    if grammar_version == "v4":
        base_v3, base_v3_sha = _load_json(root / "illustration_moe_grammar_v3.json")
        if base_v3.get("schema") != GRAMMAR_SCHEMA:
            raise MoeElementError("v4 base grammar schema mismatch")
        if top["base_grammar_v3_sha256"] != base_v3_sha:
            raise MoeElementError("v4 base grammar hash mismatch")
        base_projection = copy.deepcopy(payload)
        for field in (
            "base_grammar_v3_sha256",
            "visual_meaning_contract_schema",
            "visual_meaning_contracts_sha256",
            "image_search_evidence_schema",
            "image_search_evidence_sha256",
        ):
            base_projection.pop(field)
        base_projection["schema"] = GRAMMAR_SCHEMA
        base_projection["created_at"] = base_v3.get("created_at")
        for element in base_projection.get("elements", []):
            if isinstance(element, dict):
                element.pop("visual_meaning_contract", None)
                element.pop("visual_meaning_contract_sha256", None)
        if canonical_json_bytes(base_projection) != canonical_json_bytes(base_v3):
            raise MoeElementError("v4 base grammar projection drift")
    meaning_assets = None
    visual_assets = None
    if grammar_version in {"v3", "v4"}:
        expected_ids = [
            row["id"]
            for row in sorted(
                legacy.records_by_id.values(), key=lambda row: int(row["ordinal"])
            )
        ]
        try:
            meaning_assets = load_meaning_contracts(
                root / "research_evidence_moe_elements" / MEANING_FILENAME,
                expected_element_ids=expected_ids,
            )
        except MoeMeaningContractError as exc:
            raise MoeElementError(str(exc)) from exc
        if top["meaning_contract_schema"] != MEANING_SCHEMA:
            raise MoeElementError("moe grammar meaning contract schema mismatch")
        if top["meaning_contracts_sha256"] != meaning_assets.sha256:
            raise MoeElementError("moe grammar meaning contract hash mismatch")
    if grammar_version == "v4":
        if meaning_assets is None:
            raise MoeElementError("v4 base meaning contracts were not loaded")
        try:
            visual_assets = load_visual_meaning_contracts(
                root
                / "research_evidence_moe_elements"
                / VISUAL_MEANING_FILENAME,
                evidence_path=(
                    root
                    / "research_evidence_moe_elements"
                    / IMAGE_EVIDENCE_FILENAME
                ),
                base_meanings=meaning_assets,
                expected_element_ids=expected_ids,
                expected_aliases={
                    element_id: legacy.records_by_id[element_id]["aliases"]
                    for element_id in expected_ids
                },
                expected_candidate_subtypes={
                    str(element["id"]): {
                        str(candidate["subtype_id"])
                        for candidate in element["candidates"]
                    }
                    for element in top["elements"]
                },
            )
        except MoeVisualContractError as exc:
            raise MoeElementError(str(exc)) from exc
        if top["visual_meaning_contract_schema"] != VISUAL_MEANING_SCHEMA:
            raise MoeElementError("moe grammar visual meaning schema mismatch")
        if top["visual_meaning_contracts_sha256"] != visual_assets.sha256:
            raise MoeElementError("moe grammar visual meaning hash mismatch")
        if top["image_search_evidence_schema"] != IMAGE_EVIDENCE_SCHEMA:
            raise MoeElementError("moe grammar image evidence schema mismatch")
        if top["image_search_evidence_sha256"] != visual_assets.evidence_sha256:
            raise MoeElementError("moe grammar image evidence hash mismatch")
    if top["legacy_element_asset_sha256"] != legacy.element_asset_sha256:
        raise MoeElementError("moe grammar legacy element hash mismatch")
    if top["legacy_research_sha256"] != legacy.research_sha256:
        raise MoeElementError("moe grammar legacy research hash mismatch")
    dossier_hashes = top["research_dossier_hashes"]
    expected_dossier_names = {
        "narrative",
        "wardrobe",
        "body",
        "staging_social",
        "fantasy",
    }
    if (
        not isinstance(dossier_hashes, dict)
        or set(dossier_hashes) != expected_dossier_names
    ):
        raise MoeElementError("moe grammar research dossier hash inventory drift")
    dossier_root = root / "research_evidence_moe_elements" / "dossiers_v2"
    for dossier_name in sorted(expected_dossier_names):
        dossier_path = dossier_root / f"{dossier_name}.json"
        try:
            actual_digest = hashlib.sha256(dossier_path.read_bytes()).hexdigest()
        except OSError as exc:
            raise MoeElementError(
                f"cannot read research dossier {dossier_path}: {exc}"
            ) from exc
        if dossier_hashes[dossier_name] != actual_digest:
            raise MoeElementError(f"moe grammar {dossier_name} dossier hash mismatch")
    intent_corpus_path = (
        root / "research_evidence_moe_elements" / "intent_corpus_v2.json"
    )
    try:
        intent_corpus_sha = hashlib.sha256(intent_corpus_path.read_bytes()).hexdigest()
    except OSError as exc:
        raise MoeElementError(f"cannot read intent corpus: {exc}") from exc
    if top["intent_corpus_sha256"] != intent_corpus_sha:
        raise MoeElementError("moe grammar intent corpus hash mismatch")
    if top["compatibility_sha256"] != compatibility_sha:
        raise MoeElementError("moe grammar compatibility hash mismatch")
    if top["element_count"] != 29:
        raise MoeElementError("moe grammar element_count must be 29")

    sources = top["sources"]
    if not isinstance(sources, list) or not sources:
        raise MoeElementError("moe grammar sources must be a nonempty array")
    source_ids: set[str] = set()
    for index, raw_source in enumerate(sources):
        source = _exact_keys(
            raw_source,
            {"id", "kind", "title", "url", "publisher", "claim_scope"},
            name=f"moe grammar source {index}",
        )
        source_id = source["id"]
        if not isinstance(source_id, str) or not re.fullmatch(
            r"(?:blog|ext|v2)_[a-z0-9_]+", source_id
        ):
            raise MoeElementError(f"moe grammar source {index} has invalid id")
        if source_id in source_ids:
            raise MoeElementError(f"duplicate moe grammar source id {source_id}")
        source_ids.add(source_id)
        if source["kind"] not in {
            "origin_record",
            "independent_source",
            "supplemental_source",
        }:
            raise MoeElementError(f"moe grammar source {source_id} has invalid kind")
        if not isinstance(source["url"], str) or not source["url"].startswith(
            "https://"
        ):
            raise MoeElementError(f"moe grammar source {source_id} must use https")
        for field in ("title", "publisher", "claim_scope"):
            if not isinstance(source[field], str) or not source[field].strip():
                raise MoeElementError(
                    f"moe grammar source {source_id}.{field} is empty"
                )
    if top["source_count"] != len(sources):
        raise MoeElementError("moe grammar source_count drift")

    _exact_keys(
        top["selection_contract"],
        {
            "activation",
            "max_selected_elements",
            "default_creativity",
            "creative_cue_preserves_numeric_value",
            "candidate_precedence",
            "max_support_atoms",
        },
        name="moe grammar selection_contract",
    )
    selection_contract = top["selection_contract"]
    if selection_contract != {
        "activation": "explicit_id_or_complete_reviewed_alias_only",
        "max_selected_elements": 3,
        "default_creativity": 0.5,
        "creative_cue_preserves_numeric_value": True,
        "candidate_precedence": [
            "explicit_preference_cue",
            "creative_development_contract",
            "numeric_creativity_band",
            "stable_seed_tiebreak",
        ],
        "max_support_atoms": 2,
    }:
        raise MoeElementError("moe grammar selection_contract drift")

    rules = _exact_keys(
        top["compatibility_rules"],
        {"hard_conflicts", "synergies", "generic_integration_clause_en"},
        name="moe grammar compatibility_rules",
    )
    if (
        not isinstance(rules["generic_integration_clause_en"], str)
        or not rules["generic_integration_clause_en"].strip()
    ):
        raise MoeElementError("generic integration clause must be nonempty")

    elements = top["elements"]
    if not isinstance(elements, list) or len(elements) != 29:
        raise MoeElementError("moe grammar must contain exactly 29 elements")
    element_keys = {
        "id",
        "ordinal",
        "category",
        "label_ko",
        "aliases",
        "research_questions",
        "definition_and_history",
        "semantic_subtypes",
        "appeal_mechanisms",
        "observable_or_narrative_evidence",
        "preference_axes",
        "candidates",
        "compatibility_and_conflicts",
        "format_implications",
        "source_supported_claims",
        "cross_source_synthesis",
        "design_inference",
        "limitations",
    }
    if grammar_version in {"v3", "v4"}:
        element_keys.update({"meaning_contract", "meaning_contract_sha256"})
    if grammar_version == "v4":
        element_keys.update(
            {"visual_meaning_contract", "visual_meaning_contract_sha256"}
        )
    candidate_keys = {
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
    elements_by_id: dict[str, dict[str, Any]] = {}
    candidates_by_id: dict[str, dict[str, Any]] = {}
    atom_ids: set[str] = set()
    claim_ids: set[str] = set()
    candidate_count = 0
    for index, raw_element in enumerate(elements):
        element = _exact_keys(raw_element, element_keys, name=f"moe dossier {index}")
        element_id = element["id"]
        if element_id not in legacy.records_by_id:
            raise MoeElementError(f"moe dossier {index} has unknown element id")
        if element_id in elements_by_id:
            raise MoeElementError(f"duplicate moe dossier {element_id}")
        if (
            element["ordinal"] != index + 1
            or legacy.records_by_id[element_id]["ordinal"] != index + 1
        ):
            raise MoeElementError(f"moe dossier {element_id} ordinal drift")
        if element["category"] != legacy.records_by_id[element_id]["category"]:
            raise MoeElementError(f"moe dossier {element_id} category drift")
        if element["label_ko"] != legacy.records_by_id[element_id]["label_ko"]:
            raise MoeElementError(f"moe dossier {element_id} label drift")
        if element["aliases"] != legacy.records_by_id[element_id]["aliases"]:
            raise MoeElementError(f"moe dossier {element_id} aliases drift")
        questions = _string_list(
            element["research_questions"], name=f"{element_id}.research_questions"
        )
        if len(questions) < 3:
            raise MoeElementError(
                f"{element_id} needs at least three research questions"
            )
        if (
            not isinstance(element["definition_and_history"], str)
            or not element["definition_and_history"].strip()
        ):
            raise MoeElementError(f"{element_id}.definition_and_history is empty")
        meaning_contract = None
        if grammar_version in {"v3", "v4"}:
            if meaning_assets is None:
                raise MoeElementError("meaning contracts were not loaded")
            expected_contract = meaning_assets.contracts_by_id[element_id]
            meaning_contract = element["meaning_contract"]
            if canonical_json_bytes(meaning_contract) != canonical_json_bytes(
                expected_contract
            ):
                raise MoeElementError(f"{element_id}.meaning_contract drift")
            if element["meaning_contract_sha256"] != contract_sha256(expected_contract):
                raise MoeElementError(f"{element_id}.meaning contract hash drift")
            if (
                element["definition_and_history"]
                != expected_contract["canonical_definition_ko"]
            ):
                raise MoeElementError(f"{element_id}.canonical definition drift")
        if grammar_version == "v4":
            if visual_assets is None:
                raise MoeElementError("v4 visual meaning contracts were not loaded")
            expected_visual_contract = visual_assets.contracts_by_id[element_id]
            if canonical_json_bytes(
                element["visual_meaning_contract"]
            ) != canonical_json_bytes(expected_visual_contract):
                raise MoeElementError(f"{element_id}.visual_meaning_contract drift")
            if element["visual_meaning_contract_sha256"] != visual_contract_sha256(
                expected_visual_contract
            ):
                raise MoeElementError(f"{element_id}.visual meaning contract hash drift")
        _string_list(
            element["observable_or_narrative_evidence"],
            name=f"{element_id}.observable_or_narrative_evidence",
        )
        _string_list(
            element["compatibility_and_conflicts"],
            name=f"{element_id}.compatibility_and_conflicts",
        )
        _string_list(
            element["format_implications"], name=f"{element_id}.format_implications"
        )
        _string_list(element["design_inference"], name=f"{element_id}.design_inference")
        _string_list(element["limitations"], name=f"{element_id}.limitations")
        if (
            not isinstance(element["cross_source_synthesis"], str)
            or not element["cross_source_synthesis"].strip()
        ):
            raise MoeElementError(f"{element_id}.cross_source_synthesis is empty")

        subtypes = element["semantic_subtypes"]
        if not isinstance(subtypes, list) or len(subtypes) < 2:
            raise MoeElementError(f"{element_id} needs at least two semantic subtypes")
        subtype_ids: set[str] = set()
        for subtype_index, raw_subtype in enumerate(subtypes):
            subtype = _exact_keys(
                raw_subtype,
                {"id", "label", "distinction"},
                name=f"{element_id}.semantic_subtypes[{subtype_index}]",
            )
            subtype_id = subtype["id"]
            if not isinstance(subtype_id, str) or not subtype_id:
                raise MoeElementError(f"{element_id} has invalid subtype id")
            if subtype_id in subtype_ids:
                raise MoeElementError(
                    f"{element_id} has duplicate subtype {subtype_id}"
                )
            subtype_ids.add(subtype_id)
            if grammar_version in {"v3", "v4"} and subtype_id.startswith(
                "researched_variant_"
            ):
                raise MoeElementError(f"{element_id} retains a placeholder subtype")
            for field in ("label", "distinction"):
                if not isinstance(subtype[field], str) or not subtype[field].strip():
                    raise MoeElementError(f"{element_id}.{subtype_id}.{field} is empty")

        mechanisms = element["appeal_mechanisms"]
        if not isinstance(mechanisms, list) or len(mechanisms) < 2:
            raise MoeElementError(f"{element_id} needs at least two appeal mechanisms")
        for mechanism_index, raw_mechanism in enumerate(mechanisms):
            mechanism = _exact_keys(
                raw_mechanism,
                {"id", "description", "basis", "source_ids"},
                name=f"{element_id}.appeal_mechanisms[{mechanism_index}]",
            )
            if mechanism["basis"] not in {"source_supported", "design_inference"}:
                raise MoeElementError(f"{element_id} appeal mechanism basis drift")
            mechanism_sources = _string_list(
                mechanism["source_ids"],
                name=f"{element_id}.appeal_mechanisms[{mechanism_index}].source_ids",
                nonempty=mechanism["basis"] == "source_supported",
            )
            if not set(mechanism_sources).issubset(source_ids):
                raise MoeElementError(f"{element_id} appeal mechanism source drift")

        axes = element["preference_axes"]
        if not isinstance(axes, list) or len(axes) < 2:
            raise MoeElementError(f"{element_id} needs at least two preference axes")
        for axis_index, raw_axis in enumerate(axes):
            axis = _exact_keys(
                raw_axis,
                {"id", "description", "values"},
                name=f"{element_id}.preference_axes[{axis_index}]",
            )
            values = axis["values"]
            if not isinstance(values, list) or len(values) < 2:
                raise MoeElementError(f"{element_id} preference axis needs two values")
            for value_index, raw_value in enumerate(values):
                value = _exact_keys(
                    raw_value,
                    {"id", "label", "request_cues"},
                    name=f"{element_id}.preference_axes[{axis_index}].values[{value_index}]",
                )
                _string_list(
                    value["request_cues"],
                    name=f"{element_id}.preference_axes[{axis_index}].values[{value_index}].request_cues",
                )

        claims = element["source_supported_claims"]
        if not isinstance(claims, list) or not claims:
            raise MoeElementError(f"{element_id} needs source-supported claims")
        local_claim_ids: set[str] = set()
        for claim_index, raw_claim in enumerate(claims):
            claim = _exact_keys(
                raw_claim,
                {"id", "claim", "source_ids", "confidence"},
                name=f"{element_id}.source_supported_claims[{claim_index}]",
            )
            claim_id = claim["id"]
            if not isinstance(claim_id, str) or not re.fullmatch(
                r"moe_claim_[a-z0-9_]+", claim_id
            ):
                raise MoeElementError(f"{element_id} has invalid claim id")
            if claim_id in claim_ids:
                raise MoeElementError(f"duplicate moe claim id {claim_id}")
            claim_ids.add(claim_id)
            local_claim_ids.add(claim_id)
            referenced_sources = _string_list(
                claim["source_ids"], name=f"{element_id}.{claim_id}.source_ids"
            )
            if not set(referenced_sources).issubset(source_ids):
                raise MoeElementError(f"{element_id}.{claim_id} source drift")
            if claim["confidence"] not in {"high", "medium", "medium-low", "low"}:
                raise MoeElementError(f"{element_id}.{claim_id} confidence drift")

        candidates = element["candidates"]
        if not isinstance(candidates, list) or len(candidates) < 3:
            raise MoeElementError(f"{element_id} needs at least three candidates")
        novelty_levels: set[int] = set()
        canonical_default_count = 0
        for candidate_index, raw_candidate in enumerate(candidates):
            candidate = _exact_keys(
                raw_candidate,
                candidate_keys,
                name=f"{element_id}.candidates[{candidate_index}]",
            )
            candidate_id = candidate["id"]
            if not isinstance(candidate_id, str) or not re.fullmatch(
                r"moe_candidate_[a-z0-9_]+", candidate_id
            ):
                raise MoeElementError(f"{element_id} has invalid candidate id")
            if candidate_id in candidates_by_id:
                raise MoeElementError(f"duplicate moe candidate id {candidate_id}")
            if candidate["subtype_id"] not in subtype_ids:
                raise MoeElementError(f"{candidate_id} references unknown subtype")
            novelty = candidate["novelty_level"]
            if type(novelty) is not int or novelty not in {0, 1, 2}:
                raise MoeElementError(
                    f"{candidate_id} novelty_level must be 0, 1, or 2"
                )
            novelty_levels.add(novelty)
            if type(candidate["canonical_default"]) is not bool:
                raise MoeElementError(
                    f"{candidate_id}.canonical_default must be boolean"
                )
            if candidate["canonical_default"]:
                canonical_default_count += 1
                if novelty != 1:
                    raise MoeElementError(
                        f"{candidate_id} canonical default must use novelty level 1"
                    )
            _string_list(candidate["intent_keys"], name=f"{candidate_id}.intent_keys")
            if candidate["representation_mode"] not in REPRESENTATION_MODES:
                raise MoeElementError(f"{candidate_id} representation_mode drift")
            if candidate["integration_role"] not in {
                "character_state",
                "relationship_event",
                "wardrobe",
                "pose",
                "expression",
                "composition",
                "participatory_action",
                "environment_hazard",
            }:
                raise MoeElementError(f"{candidate_id} integration_role drift")
            _string_list(
                candidate["selection_cues"], name=f"{candidate_id}.selection_cues"
            )
            if (
                not isinstance(candidate["preference_profile"], dict)
                or not candidate["preference_profile"]
            ):
                raise MoeElementError(
                    f"{candidate_id}.preference_profile must be nonempty"
                )
            if any(
                not isinstance(key, str)
                or not key
                or not isinstance(value, str)
                or not value
                for key, value in candidate["preference_profile"].items()
            ):
                raise MoeElementError(
                    f"{candidate_id}.preference_profile must be string map"
                )
            _validated_atom(
                candidate["primary_atom"],
                name=f"{candidate_id}.primary_atom",
                atom_ids=atom_ids,
            )
            support_atoms = candidate["support_atoms"]
            if not isinstance(support_atoms, list) or not 2 <= len(support_atoms) <= 3:
                raise MoeElementError(
                    f"{candidate_id} needs two or three support atoms"
                )
            for support_index, support in enumerate(support_atoms):
                _validated_atom(
                    support,
                    name=f"{candidate_id}.support_atoms[{support_index}]",
                    atom_ids=atom_ids,
                )
            if grammar_version in {"v3", "v4"} and meaning_contract is not None:
                runtime_fragments = [
                    candidate["primary_atom"]["prompt_fragment_en"],
                    *[support["prompt_fragment_en"] for support in support_atoms],
                ]
                for label in meaning_contract["runtime_forbidden_labels"]:
                    if any(
                        runtime_label_present(label, fragment)
                        for fragment in runtime_fragments
                    ):
                        raise MoeElementError(
                            f"{candidate_id} leaks runtime-forbidden label {label!r}"
                        )
            for field in ("resource_claims", "compatibility_tags"):
                _string_list(candidate[field], name=f"{candidate_id}.{field}")
            candidate_claim_ids = _string_list(
                candidate["source_claim_ids"], name=f"{candidate_id}.source_claim_ids"
            )
            if not set(candidate_claim_ids).issubset(local_claim_ids):
                raise MoeElementError(f"{candidate_id} source_claim_ids drift")
            for field in ("label_en", "limitation"):
                if (
                    not isinstance(candidate[field], str)
                    or not candidate[field].strip()
                ):
                    raise MoeElementError(f"{candidate_id}.{field} is empty")
            stored = copy.deepcopy(candidate)
            stored["element_id"] = element_id
            candidates_by_id[candidate_id] = stored
            candidate_count += 1
        if novelty_levels != {0, 1, 2}:
            raise MoeElementError(
                f"{element_id} must expose novelty levels 0, 1, and 2"
            )
        if canonical_default_count != 1:
            raise MoeElementError(
                f"{element_id} must expose exactly one canonical default"
            )
        elements_by_id[element_id] = element

    if list(elements_by_id) != list(legacy.records_by_id):
        raise MoeElementError("moe grammar element order must match the v1 inventory")
    if top["candidate_count"] != candidate_count:
        raise MoeElementError("moe grammar candidate_count drift")

    if compatibility.get("schema") != "subculture-illustration-moe-compatibility/v2":
        raise MoeElementError("moe compatibility schema mismatch")
    compatibility_source_hashes = compatibility.get("source_hashes")
    if (
        not isinstance(compatibility_source_hashes, dict)
        or compatibility_source_hashes.get("illustration_moe_elements_v1_sha256")
        != legacy.element_asset_sha256
    ):
        raise MoeElementError("moe compatibility legacy element hash mismatch")
    compatibility_profiles = compatibility.get("element_profiles")
    if not isinstance(compatibility_profiles, list) or [
        profile.get("element_id") if isinstance(profile, dict) else None
        for profile in compatibility_profiles
    ] != list(elements_by_id):
        raise MoeElementError("moe compatibility element profile order drift")
    compatibility_counts = compatibility.get("counts")
    if (
        not isinstance(compatibility_counts, dict)
        or compatibility_counts.get("element_profiles") != 29
    ):
        raise MoeElementError("moe compatibility counts drift")

    hard_conflicts = rules["hard_conflicts"]
    if not isinstance(hard_conflicts, list):
        raise MoeElementError("hard_conflicts must be an array")
    seen_pairs: set[tuple[str, str]] = set()
    for index, pair in enumerate(hard_conflicts):
        if (
            not isinstance(pair, list)
            or len(pair) != 2
            or any(not isinstance(item, str) for item in pair)
        ):
            raise MoeElementError(f"hard_conflicts[{index}] must be a two-ID array")
        canonical_pair = tuple(sorted(pair))
        if pair != list(canonical_pair) or canonical_pair in seen_pairs:
            raise MoeElementError("hard conflict pairs must be unique and sorted")
        if not set(pair).issubset(elements_by_id):
            raise MoeElementError("hard conflict references an unknown element")
        seen_pairs.add(canonical_pair)
    synergies = rules["synergies"]
    if not isinstance(synergies, list):
        raise MoeElementError("synergies must be an array")
    for index, raw_synergy in enumerate(synergies):
        synergy = _exact_keys(
            raw_synergy,
            {"element_ids", "bridge_clause_en"},
            name=f"synergies[{index}]",
        )
        pair = synergy["element_ids"]
        if (
            not isinstance(pair, list)
            or len(pair) != 2
            or pair != sorted(pair)
            or not set(pair).issubset(elements_by_id)
        ):
            raise MoeElementError(f"synergies[{index}].element_ids drift")
        if (
            not isinstance(synergy["bridge_clause_en"], str)
            or not synergy["bridge_clause_en"].strip()
        ):
            raise MoeElementError(f"synergies[{index}].bridge_clause_en is empty")

    return MoeGrammarAssets(
        asset_dir=root,
        payload=payload,
        elements_by_id=elements_by_id,
        candidates_by_id=candidates_by_id,
        grammar_sha256=grammar_sha,
        compatibility=compatibility,
        compatibility_sha256=compatibility_sha,
        version=grammar_version,
        visual_contracts=visual_assets,
    )


def _load_moe_grammar_v5_assets(
    root: Path,
    legacy: MoeElementAssets,
) -> MoeGrammarAssets:
    """Build the authenticated effective v5 view over byte-stable grammar v4."""

    base = load_moe_grammar_assets(
        root,
        legacy_assets=legacy,
        grammar_version="v4",
    )
    if base.visual_contracts is None:
        raise MoeElementError("v5 requires validated v4 visual contracts")
    try:
        additions = load_moe_visual_additions(
            root / "research_evidence_moe_elements" / ADDITION_FILENAME,
            base_grammar_sha256=base.grammar_sha256,
            base_elements_by_id=base.elements_by_id,
            base_alias_bindings=base.visual_contracts.alias_bindings,
        )
    except MoeVisualAdditionError as exc:
        raise MoeElementError(str(exc)) from exc

    manifest, manifest_sha = _load_json(root / "illustration_moe_grammar_v5.json")
    expected_manifest = build_v5_manifest(
        base_grammar_sha256=base.grammar_sha256,
        base_elements_by_id=base.elements_by_id,
        base_visual_contracts=base.visual_contracts.contracts_by_id,
        base_image_evidence=base.visual_contracts.image_evidence_by_id,
        base_candidate_count=int(base.payload["candidate_count"]),
        base_compatibility_sha256=base.compatibility_sha256,
        additions=additions,
    )
    if canonical_json_bytes(manifest) != canonical_json_bytes(expected_manifest):
        raise MoeElementError("compiled v5 grammar manifest is stale")

    elements_by_id = copy.deepcopy(base.elements_by_id)
    candidates_by_id = copy.deepcopy(base.candidates_by_id)
    for element_id, refinement in additions.refinements_by_id.items():
        element = elements_by_id[element_id]
        visual_contract = copy.deepcopy(refinement["visual_meaning_contract"])
        element["visual_meaning_contract"] = visual_contract
        element["visual_meaning_contract_sha256"] = refinement[
            "visual_meaning_contract_sha256"
        ]
    for element_id, profile in additions.new_profiles_by_id.items():
        element = {
            "id": element_id,
            "ordinal": profile["ordinal"],
            "category": profile["category"],
            "label_ko": profile["label_ko"],
            "label_en": profile["label_en"],
            "aliases": [alias["alias"] for alias in profile["aliases"]],
            "preference_axes": copy.deepcopy(profile["preference_axes"]),
            "candidates": copy.deepcopy(profile["candidates"]),
            "meaning_contract": copy.deepcopy(profile["meaning_contract"]),
            "meaning_contract_sha256": profile["meaning_contract_sha256"],
            "visual_meaning_contract": copy.deepcopy(
                profile["visual_meaning_contract"]
            ),
            "visual_meaning_contract_sha256": profile[
                "visual_meaning_contract_sha256"
            ],
        }
        elements_by_id[element_id] = element
        for candidate in element["candidates"]:
            stored = copy.deepcopy(candidate)
            stored["element_id"] = element_id
            candidates_by_id[str(candidate["id"])] = stored

    merged_contracts = copy.deepcopy(base.visual_contracts.contracts_by_id)
    merged_evidence = copy.deepcopy(base.visual_contracts.image_evidence_by_id)
    merged_aliases = copy.deepcopy(base.visual_contracts.alias_bindings)
    for profile in additions.profiles_by_id.values():
        merged_contracts[str(profile["element_id"])] = copy.deepcopy(
            profile["visual_meaning_contract"]
        )
        merged_evidence[str(profile["research_evidence"]["id"])] = copy.deepcopy(
            profile["research_evidence"]
        )
    merged_aliases.update(copy.deepcopy(additions.alias_bindings))
    visual_contracts = MoeVisualMeaningContracts(
        path=additions.path,
        evidence_path=additions.path,
        payload=copy.deepcopy(manifest),
        contracts_by_id=merged_contracts,
        alias_bindings=merged_aliases,
        image_evidence_by_id=merged_evidence,
        sha256=str(manifest["effective_visual_meaning_contracts_sha256"]),
        evidence_sha256=str(manifest["effective_image_search_evidence_sha256"]),
    )

    compatibility = copy.deepcopy(base.compatibility)
    compatibility["schema"] = "subculture-illustration-moe-compatibility/v3"
    compatibility.setdefault("source_hashes", {})[
        "moe_visual_additions_v1_sha256"
    ] = additions.sha256
    compatibility["element_profiles"].extend(
        copy.deepcopy(profile["compatibility_profile"])
        for profile in additions.new_profiles_by_id.values()
    )
    compatibility["counts"]["element_profiles"] = len(elements_by_id)

    payload = copy.deepcopy(base.payload)
    payload.update(
        {
            "schema": GRAMMAR_SCHEMA_V5,
            "created_at": manifest["created_at"],
            "base_grammar_v4_sha256": manifest["base_grammar_v4_sha256"],
            "visual_additions_schema": manifest["visual_additions_schema"],
            "visual_additions_sha256": manifest["visual_additions_sha256"],
            "meaning_contract_schema": (
                "subculture-illustration-moe-meaning-contracts/v2-effective"
            ),
            "meaning_contracts_sha256": manifest[
                "effective_meaning_contracts_sha256"
            ],
            "visual_meaning_contract_schema": (
                "subculture-illustration-moe-meaning-contracts/v3-effective"
            ),
            "visual_meaning_contracts_sha256": manifest[
                "effective_visual_meaning_contracts_sha256"
            ],
            "image_search_evidence_schema": (
                "subculture-illustration-moe-image-search-evidence/v2-effective"
            ),
            "image_search_evidence_sha256": manifest[
                "effective_image_search_evidence_sha256"
            ],
            "element_count": manifest["selectable_element_count"],
            "candidate_count": manifest["candidate_count"],
            "elements": list(elements_by_id.values()),
        }
    )
    rules = copy.deepcopy(base.payload["compatibility_rules"])
    rules["hard_conflicts"] = sorted(
        [
            *rules["hard_conflicts"],
            *additions.payload["compatibility_rules"]["hard_conflicts"],
        ]
    )
    rules["synergies"].extend(
        copy.deepcopy(additions.payload["compatibility_rules"]["synergies"])
    )
    payload["compatibility_rules"] = rules
    payload["sources"] = [
        *copy.deepcopy(base.payload["sources"]),
        *copy.deepcopy(additions.payload["sources"]),
    ]
    payload["source_count"] = len(payload["sources"])

    return MoeGrammarAssets(
        asset_dir=root,
        payload=payload,
        elements_by_id=elements_by_id,
        candidates_by_id=candidates_by_id,
        grammar_sha256=manifest_sha,
        compatibility=compatibility,
        compatibility_sha256=str(manifest["effective_compatibility_sha256"]),
        version="v5",
        visual_contracts=visual_contracts,
        visual_additions=additions,
    )


def _preference_cue_match(text: str, cue: str) -> bool:
    normalized_text = normalize_text(text)
    normalized_cue = normalize_text(cue)
    if not normalized_cue:
        return False
    if re.search(r"[가-힣ぁ-んァ-ン一-龯]", normalized_cue):
        return normalized_cue in normalized_text
    return f" {normalized_cue} " in f" {normalized_text} "


def _stable_rank(seed: int, *parts: str) -> str:
    return hashlib.sha256(canonical_json_bytes([seed, *parts])).hexdigest()


def _select_v2_candidate(
    element: Mapping[str, Any],
    *,
    preference_text: str,
    creativity: float,
    creative_development_required: bool,
    seed: int,
    allowed_subtype_ids: set[str] | None = None,
) -> tuple[dict[str, Any], list[str], str, int]:
    candidates = [
        candidate
        for candidate in element["candidates"]
        if allowed_subtype_ids is None
        or str(candidate["subtype_id"]) in allowed_subtype_ids
    ]
    if not candidates:
        raise MoeElementError(
            f"{element['id']} has no candidate for the requested visual variant"
        )
    matched_axis_values: dict[str, set[str]] = {}
    matched_axis_cues: dict[tuple[str, str], list[str]] = {}
    for axis in element["preference_axes"]:
        for value in axis["values"]:
            matches = [
                cue
                for cue in value["request_cues"]
                if _preference_cue_match(preference_text, cue)
            ]
            if matches:
                matched_axis_values.setdefault(axis["id"], set()).add(value["id"])
                matched_axis_cues[(axis["id"], value["id"])] = matches
    matched_by_candidate: dict[str, list[str]] = {
        candidate["id"]: [
            cue
            for cue in candidate["selection_cues"]
            if _preference_cue_match(preference_text, cue)
        ]
        for candidate in candidates
    }
    match_vectors = {
        candidate["id"]: (
            len(matched_by_candidate[candidate["id"]])
            + sum(
                1
                for axis_id, value_id in candidate["preference_profile"].items()
                if value_id in matched_axis_values.get(axis_id, set())
            ),
            len(matched_by_candidate[candidate["id"]]),
            sum(
                1
                for axis_id, value_id in candidate["preference_profile"].items()
                if value_id in matched_axis_values.get(axis_id, set())
            ),
        )
        for candidate in candidates
    }
    maximum_match = max(match_vectors.values())
    if maximum_match[1] >= 2 or maximum_match[2] >= 2:
        pool = [
            candidate
            for candidate in candidates
            if match_vectors[candidate["id"]] == maximum_match
        ]
        reason = "explicit_preference_cue"
        target_novelty = 2 if creative_development_required else round(creativity * 2)
    else:
        target_novelty = 2 if creative_development_required else round(creativity * 2)
        pool = [
            candidate
            for candidate in candidates
            if int(candidate["novelty_level"]) == target_novelty
        ]
        if not pool:
            distance = min(
                abs(int(candidate["novelty_level"]) - target_novelty)
                for candidate in candidates
            )
            pool = [
                candidate
                for candidate in candidates
                if abs(int(candidate["novelty_level"]) - target_novelty) == distance
            ]
        canonical_pool = [
            candidate for candidate in pool if candidate["canonical_default"] is True
        ]
        if canonical_pool:
            pool = canonical_pool
        reason = (
            "creative_development_contract"
            if creative_development_required
            else "numeric_creativity_band"
        )
    selected = min(
        pool,
        key=lambda candidate: _stable_rank(seed, str(element["id"]), candidate["id"]),
    )
    selected_axis_cues = [
        cue
        for axis_id, value_id in selected["preference_profile"].items()
        for cue in matched_axis_cues.get((axis_id, value_id), [])
    ]
    return (
        selected,
        list(
            dict.fromkeys([*selected_axis_cues, *matched_by_candidate[selected["id"]]])
        ),
        reason,
        target_novelty,
    )


def _v2_allowed_output_modes(candidates: Sequence[Mapping[str, Any]]) -> list[str]:
    modes = {str(candidate["representation_mode"]) for candidate in candidates}
    if "optical_interaction" in modes and len(modes) > 1:
        raise MoeElementError(
            "optical interaction cannot share one moe pack with a non-interactive frame contract"
        )
    if "optical_interaction" in modes:
        return ["optical_interaction"]
    if "sequence" in modes:
        return ["sequence"]
    if "paired_or_sequence" in modes:
        return ["paired_frame", "sequence"]
    return ["single_frame", "paired_frame", "sequence"]


def _bind_required_meaning_components(
    prompt_fragment: str,
    meaning_contract: Mapping[str, Any],
) -> str:
    """Make every required semantic group explicit without emitting its label."""

    additions: list[str] = []
    working = prompt_fragment
    for group in meaning_contract["component_groups"]:
        matched = [
            alternative
            for alternative in group["alternatives_en"]
            if _normalized_phrase_contains(working, alternative)
        ]
        missing_count = int(group["minimum"]) - len(matched)
        if missing_count <= 0:
            continue
        unused = [
            alternative
            for alternative in group["alternatives_en"]
            if alternative not in matched
        ]
        additions.extend(unused[:missing_count])
        working = f"{working} {' '.join(unused[:missing_count])}"
    if not additions:
        return prompt_fragment
    return (
        f"{prompt_fragment.rstrip()} Make these visible facts explicit: "
        f"{'; '.join(additions)}."
    )


def _visual_variants_by_id(
    contract: Mapping[str, Any],
) -> dict[str, Mapping[str, Any]]:
    return {str(variant["id"]): variant for variant in contract["visual_variants"]}


def _select_visual_variant(
    contract: Mapping[str, Any],
    *,
    candidate_subtype_id: str,
    requested_variant_id: str | None,
) -> Mapping[str, Any]:
    variants = _visual_variants_by_id(contract)
    if requested_variant_id is not None:
        variant = variants.get(requested_variant_id)
        if variant is None:
            raise MoeElementError(
                f"{contract['element_id']} references unknown visual variant "
                f"{requested_variant_id!r}"
            )
        if candidate_subtype_id not in variant["candidate_subtype_ids"]:
            raise MoeElementError(
                f"{contract['element_id']} candidate subtype {candidate_subtype_id!r} "
                f"does not belong to visual variant {requested_variant_id!r}"
            )
        return variant
    owners = [
        variant
        for variant in variants.values()
        if candidate_subtype_id in variant["candidate_subtype_ids"]
    ]
    if len(owners) != 1:
        raise MoeElementError(
            f"{contract['element_id']} candidate subtype {candidate_subtype_id!r} "
            "must resolve to exactly one visual variant"
        )
    return owners[0]


def _bind_visual_variant_constraints(
    prompt_fragment: str,
    variant: Mapping[str, Any],
) -> str:
    """Bind the selected visual signature as literal, auditable prompt facts."""

    required_phrases = [
        *variant["all_of_en"],
        *variant["any_of"]["alternatives_en"][: variant["any_of"]["minimum"]],
        *variant["topology_edges_en"],
        *variant["camera_requirements_en"],
        *variant["temporal_states_en"],
        *variant["interaction_requirements_en"],
    ]
    additions = [
        phrase
        for phrase in required_phrases
        if not _normalized_phrase_contains(prompt_fragment, phrase)
    ]
    if not additions:
        return prompt_fragment
    return (
        f"{prompt_fragment.rstrip()} Visual proof requirements: "
        f"{'; '.join(additions)}."
    )


def _visual_allowed_output_modes(
    base_modes: Sequence[str],
    variants: Sequence[Mapping[str, Any]],
) -> list[str]:
    allowed = list(base_modes)
    for variant in variants:
        supported = set(variant["supported_output_modes"])
        allowed = [mode for mode in allowed if mode in supported]
    if not allowed:
        selected = [str(variant["id"]) for variant in variants]
        raise MoeElementError(
            "selected visual variants have no shared output mode: "
            + ", ".join(selected)
        )
    return allowed


def _visual_evidence_projection(
    *,
    element_id: str,
    contract_sha256_value: str,
    variant: Mapping[str, Any],
    image_evidence_id: str,
) -> dict[str, Any]:
    return {
        "element_id": element_id,
        "contract_sha256": contract_sha256_value,
        "selected_variant_id": variant["id"],
        "required_component_group_ids": list(
            variant["required_component_group_ids"]
        ),
        "all_of_en": list(variant["all_of_en"]),
        "any_of": copy.deepcopy(variant["any_of"]),
        "topology_edges_en": list(variant["topology_edges_en"]),
        "camera_requirements_en": list(variant["camera_requirements_en"]),
        "temporal_states_en": list(variant["temporal_states_en"]),
        "interaction_requirements_en": list(
            variant["interaction_requirements_en"]
        ),
        "negative_visual_confounds_en": list(
            variant["negative_visual_confounds_en"]
        ),
        "supported_output_modes": list(variant["supported_output_modes"]),
        "image_evidence_id": image_evidence_id,
    }


def build_moe_candidate_pack(
    base_candidate_pack: Mapping[str, Any],
    requested_tokens: Sequence[str],
    *,
    preference_text: str | None = None,
    output_mode: str = "auto",
    legacy_assets: MoeElementAssets | None = None,
    grammar_assets: MoeGrammarAssets | None = None,
) -> dict[str, Any]:
    """Wrap an unchanged base pack with v7 visual meaning or historical replay."""

    if not isinstance(base_candidate_pack, Mapping):
        raise MoeElementError("base_candidate_pack must be an object")
    base_pack = copy.deepcopy(dict(base_candidate_pack))
    if base_pack.get("contract_version") not in {
        "subculture-illustration-candidate-pack/v1",
        "subculture-illustration-candidate-pack/v2",
        "subculture-illustration-candidate-pack/v3",
    }:
        raise MoeElementError("base_candidate_pack must be a v1, v2, or v3 pack")
    if not isinstance(base_pack.get("pack_id"), str):
        raise MoeElementError("base_candidate_pack must expose pack_id")
    request = base_pack.get("request_contract")
    provenance = base_pack.get("provenance")
    authorial = base_pack.get("authorial_contract")
    composition = base_pack.get("composition_contract")
    if not all(
        isinstance(value, Mapping)
        for value in (request, provenance, authorial, composition)
    ):
        raise MoeElementError("base_candidate_pack is missing required contracts")
    request_text = request.get("request_text")
    creativity = request.get("creativity")
    seed = provenance.get("seed")
    if not isinstance(request_text, str) or not request_text.strip():
        raise MoeElementError("base request_text must be nonempty")
    if isinstance(creativity, bool) or not isinstance(creativity, (int, float)):
        raise MoeElementError("base creativity must be numeric")
    creativity_value = float(creativity)
    if not 0 <= creativity_value <= 1:
        raise MoeElementError("base creativity must be from 0 through 1")
    if type(seed) is not int:
        raise MoeElementError("base provenance.seed must be an integer")
    if output_mode not in OUTPUT_MODES:
        raise MoeElementError(f"unsupported output_mode {output_mode!r}")
    exact_preference_text = request_text if preference_text is None else preference_text
    if not isinstance(exact_preference_text, str):
        raise MoeElementError("preference_text must be a string")

    legacy = legacy_assets or load_moe_element_assets()
    grammar = grammar_assets or load_moe_grammar_assets(
        legacy_assets=legacy, asset_dir=legacy.asset_dir
    )
    meaning_aware = grammar.version in {"v3", "v4", "v5"}
    visual_aware = grammar.version in {"v4", "v5"}
    pack_schema = {
        "v2": PACK_SCHEMA_V4,
        "v3": PACK_SCHEMA,
        "v4": PACK_SCHEMA_V6,
        "v5": PACK_SCHEMA_V7,
    }[grammar.version]
    composed_schema = {
        "v2": COMPOSED_SCHEMA_V2,
        "v3": COMPOSED_SCHEMA,
        "v4": COMPOSED_SCHEMA_V4,
        "v5": COMPOSED_SCHEMA_V5,
    }[grammar.version]
    if visual_aware:
        token_bindings = _resolve_visual_element_bindings(
            requested_tokens,
            legacy=legacy,
            grammar=grammar,
        )
        selected_ids = [str(binding["element_id"]) for binding in token_bindings]
    else:
        selected_legacy = resolve_element_tokens(requested_tokens, assets=legacy)
        selected_ids = [record["id"] for record in selected_legacy]
        token_bindings = [
            {
                "requested_token": token,
                "element_id": element_id,
                "alias_relation": "historical_untyped",
                "requested_variant_id": None,
            }
            for token, element_id in zip(requested_tokens, selected_ids, strict=True)
        ]
    selected_set = set(selected_ids)
    hard_conflicts = {
        tuple(pair) for pair in grammar.payload["compatibility_rules"]["hard_conflicts"]
    }
    for left_index, left in enumerate(selected_ids):
        for right in selected_ids[left_index + 1 :]:
            if tuple(sorted((left, right))) in hard_conflicts:
                raise MoeElementError(f"incompatible moe elements: {left} / {right}")
    representative_decisions = [
        copy.deepcopy(row)
        for row in grammar.compatibility.get("representative_combinations", [])
        if isinstance(row, dict)
        and set(row.get("element_ids", []))
        and set(row.get("element_ids", [])).issubset(selected_set)
    ]
    for row in representative_decisions:
        if row.get("decision") == "block":
            raise MoeElementError(
                f"incompatible moe combination: {row.get('id')} ({row.get('reason')})"
            )

    creative_development_required = (
        authorial.get("creative_development_required") is True
    )
    selected_candidates: list[dict[str, Any]] = []
    intent_rows: list[dict[str, Any]] = []
    selected_nodes: list[dict[str, Any]] = []
    selected_meaning_bindings: list[dict[str, Any]] = []
    selected_visual_bindings: list[dict[str, Any]] = []
    selected_visual_variants: list[Mapping[str, Any]] = []
    required_moe_ids: list[str] = []
    for element_index, token_binding in enumerate(token_bindings):
        token = str(token_binding["requested_token"])
        element_id = str(token_binding["element_id"])
        element = grammar.elements_by_id[element_id]
        visual_contract = (
            element["visual_meaning_contract"] if visual_aware else None
        )
        requested_variant_id = token_binding["requested_variant_id"]
        allowed_subtype_ids = None
        if isinstance(visual_contract, Mapping) and requested_variant_id is not None:
            requested_variant = _visual_variants_by_id(visual_contract).get(
                str(requested_variant_id)
            )
            if requested_variant is None:
                raise MoeElementError(
                    f"{element_id} has no requested visual variant "
                    f"{requested_variant_id!r}"
                )
            allowed_subtype_ids = set(requested_variant["candidate_subtype_ids"])
        candidate, matched_cues, reason, target_novelty = _select_v2_candidate(
            element,
            preference_text=exact_preference_text,
            creativity=creativity_value,
            creative_development_required=creative_development_required,
            seed=seed,
            allowed_subtype_ids=allowed_subtype_ids,
        )
        visual_variant = None
        if isinstance(visual_contract, Mapping):
            visual_variant = _select_visual_variant(
                visual_contract,
                candidate_subtype_id=str(candidate["subtype_id"]),
                requested_variant_id=(
                    str(requested_variant_id)
                    if requested_variant_id is not None
                    else None
                ),
            )
            selected_visual_variants.append(visual_variant)
        ranked_supports = sorted(
            candidate["support_atoms"],
            key=lambda atom: _stable_rank(
                seed, element_id, candidate["id"], atom["id"]
            ),
        )
        # The compatibility contract is global, not per element: one governing
        # primary plus no more than two visible supports across the whole pack.
        if len(selected_ids) == 1:
            support_atoms = ranked_supports[:2]
        elif len(selected_ids) == 2 and element_index == 0:
            support_atoms = ranked_supports[:1]
        else:
            support_atoms = []
        primary = candidate["primary_atom"]
        meaning_contract = element.get("meaning_contract") if meaning_aware else None
        primary_prompt_fragment = primary["prompt_fragment_en"]
        if isinstance(meaning_contract, Mapping):
            primary_prompt_fragment = _bind_required_meaning_components(
                primary_prompt_fragment,
                meaning_contract,
            )
        if isinstance(visual_variant, Mapping):
            primary_prompt_fragment = _bind_visual_variant_constraints(
                primary_prompt_fragment,
                visual_variant,
            )
        exposed_ids = [
            f"moe:{candidate['id']}",
            f"moe:{primary['id']}",
            *[f"moe:{atom['id']}" for atom in support_atoms],
        ]
        required_moe_ids.extend(exposed_ids)
        selected_nodes.append(
            {
                "id": primary["id"],
                "candidate_id": candidate["id"],
                "element_id": element_id,
                "selected_role": "primary" if element_index == 0 else "support",
                "prompt_fragment_en": primary_prompt_fragment,
                "observable_evidence": primary["observable_evidence"],
            }
        )
        selected_nodes.extend(
            {
                "id": atom["id"],
                "candidate_id": candidate["id"],
                "element_id": element_id,
                "selected_role": "support",
                "prompt_fragment_en": atom["prompt_fragment_en"],
                "observable_evidence": atom["observable_evidence"],
            }
            for atom in support_atoms
        )
        selected_candidate = {
            "element_id": element_id,
            "candidate_id": candidate["id"],
            "label_en": candidate["label_en"],
            "subtype_id": candidate["subtype_id"],
            "novelty_level": candidate["novelty_level"],
            "canonical_default": candidate["canonical_default"],
            "intent_keys": list(candidate["intent_keys"]),
            "representation_mode": candidate["representation_mode"],
            "integration_role": candidate["integration_role"],
            "preference_profile": copy.deepcopy(candidate["preference_profile"]),
            "resource_claims": list(candidate["resource_claims"]),
            "compatibility_tags": list(candidate["compatibility_tags"]),
            "source_claim_ids": list(candidate["source_claim_ids"]),
            "selected_primary_atom_id": primary["id"],
            "selected_support_atom_ids": [atom["id"] for atom in support_atoms],
        }
        if meaning_aware:
            meaning_contract = element["meaning_contract"]
            selected_candidate["semantic_fidelity"] = meaning_contract[
                "semantic_fidelity"
            ]
            selected_candidate["meaning_contract_sha256"] = element[
                "meaning_contract_sha256"
            ]
            selected_meaning_bindings.append(
                {
                    "element_id": element_id,
                    "source": "canonical_research_contract",
                    "contract_sha256": element["meaning_contract_sha256"],
                    "contract": copy.deepcopy(meaning_contract),
                }
            )
        if visual_aware and isinstance(visual_contract, Mapping) and isinstance(
            visual_variant, Mapping
        ):
            selected_candidate["visual_variant_id"] = visual_variant["id"]
            selected_candidate["visual_meaning_contract_sha256"] = element[
                "visual_meaning_contract_sha256"
            ]
            selected_visual_bindings.append(
                {
                    "element_id": element_id,
                    "source": "typed_visual_meaning_contract",
                    "contract_sha256": element[
                        "visual_meaning_contract_sha256"
                    ],
                    "contract": copy.deepcopy(visual_contract),
                    "selected_variant_id": visual_variant["id"],
                    "selected_variant": copy.deepcopy(visual_variant),
                    "image_evidence_id": visual_contract["image_evidence_id"],
                }
            )
        selected_candidates.append(selected_candidate)
        intent_row = {
            "requested_token": token,
            "element_id": element_id,
            "matched_preference_cues": matched_cues,
            "selected_candidate_id": candidate["id"],
            "selection_reason": reason,
            "target_novelty_level": target_novelty,
        }
        if visual_aware:
            intent_row["alias_relation"] = token_binding["alias_relation"]
            intent_row["selected_visual_variant_id"] = (
                visual_variant["id"]
                if isinstance(visual_variant, Mapping)
                else None
            )
        intent_rows.append(intent_row)

    allowed_modes = _v2_allowed_output_modes(selected_candidates)
    if visual_aware:
        allowed_modes = _visual_allowed_output_modes(
            allowed_modes,
            selected_visual_variants,
        )
    resolved_output_mode = allowed_modes[0] if output_mode == "auto" else output_mode
    if output_mode != "auto" and output_mode not in allowed_modes:
        raise MoeElementError(
            f"output_mode {output_mode!r} cannot carry the selected moe candidates; "
            f"use one of {allowed_modes}"
        )

    synergy_clauses = [
        row["bridge_clause_en"]
        for row in grammar.payload["compatibility_rules"]["synergies"]
        if set(row["element_ids"]).issubset(selected_set)
    ]
    integration_clauses = synergy_clauses or [
        grammar.payload["compatibility_rules"]["generic_integration_clause_en"]
    ]
    compatibility_profiles = {
        row["element_id"]: row
        for row in grammar.compatibility.get("element_profiles", [])
        if isinstance(row, dict) and isinstance(row.get("element_id"), str)
    }
    base_required = composition.get("required_chosen_candidate_ids")
    if not isinstance(base_required, list) or any(
        not isinstance(item, str) or not item for item in base_required
    ):
        raise MoeElementError("base composition candidate IDs must be strings")
    combined_required_ids = [*base_required, *required_moe_ids]
    if len(combined_required_ids) != len(set(combined_required_ids)):
        raise MoeElementError("moe required candidate IDs must remain unique")

    grammar_hash_key = {
        "v2": "moe_grammar_v2_sha256",
        "v3": "moe_grammar_v3_sha256",
        "v4": "moe_grammar_v4_sha256",
        "v5": "moe_grammar_v5_sha256",
    }[grammar.version]
    compatibility_hash_key = (
        "moe_compatibility_v3_sha256"
        if grammar.version == "v5"
        else "moe_compatibility_v2_sha256"
    )
    pack: dict[str, Any] = {
        "contract_version": pack_schema,
        "pack_id": None,
        "base_candidate_pack": base_pack,
        "request_contract": {
            "request_text": request_text,
            "requested_element_tokens": list(requested_tokens),
            "preference_text": exact_preference_text,
            "selected_element_ids": selected_ids,
            "output_mode": output_mode,
            "creativity": creativity_value,
            "creative_development_required": creative_development_required,
        },
        "moe_intent": intent_rows,
        "moe_grammar": {
            "schema": grammar.payload["schema"],
            "frame_contract": {
                "requested_output_mode": output_mode,
                "resolved_output_mode": resolved_output_mode,
                "allowed_output_modes": allowed_modes,
            },
            "selected_candidates": selected_candidates,
            "selected_nodes": selected_nodes,
            "sparse_bundle": {
                "governing_primary_element_id": selected_ids[0]
                if selected_ids
                else None,
                "governing_primary_count": 1 if selected_ids else 0,
                "support_count": max(0, len(selected_nodes) - 1),
                "maximum_support_count": 2,
            },
            "integration_clauses_en": integration_clauses,
            "compatibility_trace": {
                "schema": grammar.compatibility["schema"],
                "selected_element_profiles": [
                    copy.deepcopy(compatibility_profiles[element_id])
                    for element_id in selected_ids
                ],
                "representative_decisions": representative_decisions,
                "resolution_order": list(
                    grammar.compatibility["design_contract"]["resolution_order"]
                ),
            },
        },
        "composition_contract": {
            "composer": "agent",
            "base_pack_id": base_pack["pack_id"],
            "required_chosen_candidate_ids": combined_required_ids,
            "selected_moe_candidate_ids": [
                row["candidate_id"] for row in selected_candidates
            ],
            "composition_mode": "recompose_into_one_shared_event_not_suffix_append",
            "composed_schema": composed_schema,
        },
        "safety": copy.deepcopy(base_pack.get("safety")),
        "negative_en": base_pack.get("negative_en"),
        "asset_hashes": {
            "legacy_moe_elements_sha256": legacy.element_asset_sha256,
            "legacy_moe_research_sha256": legacy.research_sha256,
            grammar_hash_key: grammar.grammar_sha256,
            compatibility_hash_key: grammar.compatibility_sha256,
        },
        "provenance": {
            "generator_version": {
                "v2": "subculture-illustration-moe-generator/v2",
                "v3": "subculture-illustration-moe-generator/v3",
                "v4": "subculture-illustration-moe-generator/v4",
                "v5": "subculture-illustration-moe-generator/v5",
            }[grammar.version],
            "selection_mode": {
                "v2": "research_preference_sparse_bundle_v2",
                "v3": "canonical_meaning_preference_sparse_bundle_v3",
                "v4": "typed_visual_meaning_sparse_bundle_v4",
                "v5": "typed_visual_additions_sparse_bundle_v5",
            }[grammar.version],
            "base_pack_id": base_pack["pack_id"],
            "seed": seed,
        },
    }
    if meaning_aware:
        pack["moe_grammar"]["meaning_bindings"] = selected_meaning_bindings
        semantic_contract = {
            "schema": "subculture-illustration-moe-semantic-binding/v1",
            "original_request_sha256": hashlib.sha256(
                request_text.encode("utf-8")
            ).hexdigest(),
            "meaning_contracts_sha256": grammar.payload["meaning_contracts_sha256"],
            "safety_evaluation_source": "original_request_plus_canonical_meaning",
            "silent_semantic_substitution": "forbidden",
        }
        if visual_aware:
            pack["moe_grammar"]["visual_bindings"] = selected_visual_bindings
            semantic_contract.update(
                {
                    "schema": (
                        "subculture-illustration-moe-semantic-binding/v3"
                        if grammar.version == "v5"
                        else "subculture-illustration-moe-semantic-binding/v2"
                    ),
                    "visual_meaning_contracts_sha256": grammar.payload[
                        "visual_meaning_contracts_sha256"
                    ],
                    "image_search_evidence_sha256": grammar.payload[
                        "image_search_evidence_sha256"
                    ],
                    "alias_resolution_policy": (
                        "typed_exact_variant_carrier_related_ambiguous_v2"
                        if grammar.version == "v5"
                        else "typed_exact_variant_carrier_related_v1"
                    ),
                }
            )
            if grammar.version == "v5":
                semantic_contract["visual_additions_sha256"] = grammar.payload[
                    "visual_additions_sha256"
                ]
                pack["asset_hashes"].update(
                    {
                        "moe_visual_additions_v1_sha256": grammar.payload[
                            "visual_additions_sha256"
                        ],
                        "moe_visual_meaning_effective_v3_sha256": grammar.payload[
                            "visual_meaning_contracts_sha256"
                        ],
                        "moe_image_search_evidence_effective_v2_sha256": grammar.payload[
                            "image_search_evidence_sha256"
                        ],
                    }
                )
            else:
                pack["asset_hashes"].update(
                    {
                        "moe_visual_meaning_contracts_v2_sha256": grammar.payload[
                            "visual_meaning_contracts_sha256"
                        ],
                        "moe_image_search_evidence_v1_sha256": grammar.payload[
                            "image_search_evidence_sha256"
                        ],
                    }
                )
        pack["semantic_contract"] = semantic_contract
    pack["pack_id"] = hashlib.sha256(canonical_json_bytes(pack)).hexdigest()[:16]
    return pack


def compose_moe_prompt_draft(
    pack: Mapping[str, Any],
    base_prompt_en: str,
) -> dict[str, Any]:
    """Create one hierarchy-aware shared-event draft, not a label suffix block."""

    pack_schema = pack.get("contract_version")
    if pack_schema not in {
        PACK_SCHEMA_V4,
        PACK_SCHEMA,
        PACK_SCHEMA_V6,
        PACK_SCHEMA_V7,
    }:
        raise MoeElementError(
            "compose_moe_prompt_draft requires a v4, v5, v6, or v7 pack"
        )
    meaning_aware = pack_schema in {PACK_SCHEMA, PACK_SCHEMA_V6, PACK_SCHEMA_V7}
    visual_aware = pack_schema in {PACK_SCHEMA_V6, PACK_SCHEMA_V7}
    if not isinstance(base_prompt_en, str) or not base_prompt_en.strip():
        raise MoeElementError("base_prompt_en must be nonempty")
    grammar = pack.get("moe_grammar")
    composition = pack.get("composition_contract")
    if not isinstance(grammar, Mapping) or not isinstance(composition, Mapping):
        raise MoeElementError("moe pack lacks grammar or composition contract")
    nodes = grammar.get("selected_nodes")
    integration = grammar.get("integration_clauses_en")
    if not isinstance(nodes, list) or not isinstance(integration, list):
        raise MoeElementError("moe selected nodes or integration clauses are invalid")
    primary_nodes = [node for node in nodes if node.get("selected_role") == "primary"]
    support_nodes = [node for node in nodes if node.get("selected_role") == "support"]
    if nodes and len(primary_nodes) != 1:
        raise MoeElementError("moe composition requires exactly one governing primary")
    base_scene = base_prompt_en.strip().rstrip(".")
    if not nodes:
        prompt = base_scene + "."
    else:
        primary_phrase = str(primary_nodes[0]["prompt_fragment_en"]).strip()
        support_phrases = [
            str(node["prompt_fragment_en"]).strip() for node in support_nodes
        ]
        bridge = " ".join(str(clause).strip() for clause in integration)
        support_clause = (
            " The same action must also carry these subordinate, visible details: "
            + " ".join(support_phrases)
            if support_phrases
            else ""
        )
        prompt = (
            f"{base_scene}. One continuous shared event governs the image: "
            f"{primary_phrase}{support_clause} Shared-event constraint: {bridge}"
        ).strip()
        if not prompt.endswith("."):
            prompt += "."
    evidence: list[dict[str, Any]] = []
    for candidate in grammar.get("selected_candidates", []):
        element_nodes = [
            node for node in nodes if node.get("element_id") == candidate["element_id"]
        ]
        evidence.append(
            {
                "element_id": candidate["element_id"],
                "candidate_id": candidate["candidate_id"],
                "primary_phrase": next(
                    node["prompt_fragment_en"]
                    for node in element_nodes
                    if node["id"] == candidate["selected_primary_atom_id"]
                ),
                "support_phrases": [
                    node["prompt_fragment_en"]
                    for node in element_nodes
                    if node["id"] in candidate["selected_support_atom_ids"]
                ],
            }
        )
    result = {
        "schema": {
            PACK_SCHEMA_V4: COMPOSED_SCHEMA_V2,
            PACK_SCHEMA: COMPOSED_SCHEMA,
            PACK_SCHEMA_V6: COMPOSED_SCHEMA_V4,
            PACK_SCHEMA_V7: COMPOSED_SCHEMA_V5,
        }[pack_schema],
        "pack_id": pack["pack_id"],
        "base_pack_id": composition["base_pack_id"],
        "prompt_en": prompt,
        "negative_en": pack["negative_en"],
        "chosen_candidate_ids": list(composition["required_chosen_candidate_ids"]),
        "composition_blueprint": {
            "governing_primary_node_id": (
                primary_nodes[0]["id"] if primary_nodes else None
            ),
            "support_node_ids": [node["id"] for node in support_nodes],
            "integration_clauses_en": list(integration),
        },
        "moe_evidence": evidence,
    }
    if meaning_aware:
        bindings = grammar.get("meaning_bindings")
        if not isinstance(bindings, list):
            raise MoeElementError("meaning-aware pack lacks meaning bindings")
        result["meaning_evidence"] = [
            {
                "element_id": binding["element_id"],
                "contract_sha256": binding["contract_sha256"],
                "semantic_fidelity": binding["contract"]["semantic_fidelity"],
                "component_groups": copy.deepcopy(
                    binding["contract"]["component_groups"]
                ),
                "runtime_forbidden_labels": list(
                    binding["contract"]["runtime_forbidden_labels"]
                ),
            }
            for binding in bindings
        ]
        runtime_surfaces = [result["prompt_en"], str(result.get("negative_en") or "")]
        for binding in bindings:
            for label in binding["contract"]["runtime_forbidden_labels"]:
                if any(runtime_label_present(label, text) for text in runtime_surfaces):
                    raise MoeElementError(
                        f"runtime prompt leaks forbidden meaning label {label!r}"
                    )
    if visual_aware:
        visual_bindings = grammar.get("visual_bindings")
        if not isinstance(visual_bindings, list):
            raise MoeElementError("v6 pack lacks visual meaning bindings")
        result["visual_evidence"] = [
            _visual_evidence_projection(
                element_id=str(binding["element_id"]),
                contract_sha256_value=str(binding["contract_sha256"]),
                variant=binding["selected_variant"],
                image_evidence_id=str(binding["image_evidence_id"]),
            )
            for binding in visual_bindings
        ]
    return result


def audit_moe_candidate_pack(
    pack: Mapping[str, Any],
    composed: Mapping[str, Any],
    *,
    legacy_assets: MoeElementAssets | None = None,
    grammar_assets: MoeGrammarAssets | None = None,
) -> dict[str, Any]:
    """Replay selection and audit v7 visual meaning or historical v6/v5/v4."""

    failures: list[dict[str, Any]] = []
    resolved_grammar_for_audit = grammar_assets
    pack_schema = pack.get("contract_version")
    meaning_aware = pack_schema in {PACK_SCHEMA, PACK_SCHEMA_V6, PACK_SCHEMA_V7}
    visual_aware = pack_schema in {PACK_SCHEMA_V6, PACK_SCHEMA_V7}
    expected_composed_schema = {
        PACK_SCHEMA_V4: COMPOSED_SCHEMA_V2,
        PACK_SCHEMA: COMPOSED_SCHEMA,
        PACK_SCHEMA_V6: COMPOSED_SCHEMA_V4,
        PACK_SCHEMA_V7: COMPOSED_SCHEMA_V5,
    }.get(pack_schema, COMPOSED_SCHEMA_V5)
    expected_audit_schema = {
        PACK_SCHEMA_V4: PACK_AUDIT_SCHEMA_V2,
        PACK_SCHEMA: PACK_AUDIT_SCHEMA,
        PACK_SCHEMA_V6: PACK_AUDIT_SCHEMA_V4,
        PACK_SCHEMA_V7: PACK_AUDIT_SCHEMA_V5,
    }.get(pack_schema, PACK_AUDIT_SCHEMA_V5)
    supplied_pack_id = pack.get("pack_id")
    replay_id_input = copy.deepcopy(dict(pack))
    replay_id_input["pack_id"] = None
    expected_pack_id = hashlib.sha256(
        canonical_json_bytes(replay_id_input)
    ).hexdigest()[:16]
    if pack_schema not in {
        PACK_SCHEMA_V4,
        PACK_SCHEMA,
        PACK_SCHEMA_V6,
        PACK_SCHEMA_V7,
    }:
        failures.append(
            {"check": "schema", "message": "v4/v5/v6/v7 pack schema mismatch"}
        )
    if supplied_pack_id != expected_pack_id:
        failures.append({"check": "pack_id", "message": "v4/v5/v6/v7 pack_id drift"})
    base_pack = pack.get("base_candidate_pack")
    request = pack.get("request_contract")
    if not isinstance(base_pack, Mapping) or not isinstance(request, Mapping):
        failures.append(
            {"check": "pack", "message": "moe base or request contract missing"}
        )
    else:
        try:
            resolved_legacy = legacy_assets or load_moe_element_assets()
            resolved_grammar = grammar_assets
            if resolved_grammar is None:
                embedded_grammar = pack.get("moe_grammar")
                embedded_schema = (
                    embedded_grammar.get("schema")
                    if isinstance(embedded_grammar, Mapping)
                    else None
                )
                replay_version = {
                    GRAMMAR_SCHEMA_V2: "v2",
                    GRAMMAR_SCHEMA: "v3",
                    GRAMMAR_SCHEMA_V4: "v4",
                    GRAMMAR_SCHEMA_V5: "v5",
                }.get(embedded_schema)
                if replay_version is None:
                    raise MoeElementError("embedded moe grammar schema mismatch")
                resolved_grammar = load_moe_grammar_assets(
                    resolved_legacy.asset_dir,
                    legacy_assets=resolved_legacy,
                    grammar_version=replay_version,
                )
            resolved_grammar_for_audit = resolved_grammar
            replayed = build_moe_candidate_pack(
                base_pack,
                request.get("requested_element_tokens", []),
                preference_text=request.get("preference_text"),
                output_mode=str(request.get("output_mode") or "auto"),
                legacy_assets=resolved_legacy,
                grammar_assets=resolved_grammar,
            )
            if canonical_json_bytes(replayed) != canonical_json_bytes(dict(pack)):
                failures.append(
                    {"check": "replay", "message": "v4/v5/v6/v7 selection replay drift"}
                )
        except (MoeElementError, TypeError, ValueError) as exc:
            failures.append({"check": "replay", "message": str(exc)})
        try:
            from illustration_audit import validate_pack_integrity

            for error in validate_pack_integrity(dict(base_pack)):
                failures.append(
                    {
                        "check": "base_pack_integrity",
                        "message": error.get("message", "base pack integrity failure"),
                    }
                )
        except (ImportError, TypeError, ValueError) as exc:
            failures.append({"check": "base_pack_integrity", "message": str(exc)})

    if composed.get("schema") != expected_composed_schema:
        failures.append(
            {"check": "composed_schema", "message": "composed schema mismatch"}
        )
    if composed.get("pack_id") != supplied_pack_id:
        failures.append(
            {"check": "composed_pack_id", "message": "composed pack_id drift"}
        )
    if composed.get("negative_en") != pack.get("negative_en"):
        failures.append({"check": "negative_en", "message": "negative prompt changed"})
    composition = pack.get("composition_contract")
    expected_ids = (
        composition.get("required_chosen_candidate_ids")
        if isinstance(composition, Mapping)
        else None
    )
    if composed.get("chosen_candidate_ids") != expected_ids:
        failures.append(
            {"check": "chosen_candidate_ids", "message": "chosen candidate IDs drift"}
        )
    if not isinstance(composed.get("composition_blueprint"), Mapping):
        failures.append(
            {
                "check": "composition_blueprint",
                "message": "composition blueprint missing",
            }
        )
    prompt_en = composed.get("prompt_en")
    if not isinstance(prompt_en, str) or not prompt_en.strip():
        failures.append({"check": "prompt", "message": "prompt_en must be nonempty"})
        prompt_en = ""
    grammar = pack.get("moe_grammar")
    nodes = grammar.get("selected_nodes") if isinstance(grammar, Mapping) else None
    if not isinstance(nodes, list):
        failures.append({"check": "moe_grammar", "message": "selected_nodes missing"})
        nodes = []
    primary_nodes = [
        node
        for node in nodes
        if isinstance(node, Mapping) and node.get("selected_role") == "primary"
    ]
    if nodes and len(primary_nodes) != 1:
        failures.append(
            {"check": "sparse_bundle", "message": "exactly one primary is required"}
        )
    if len(nodes) > 3:
        failures.append(
            {"check": "sparse_bundle", "message": "at most two supports are allowed"}
        )
    for node in nodes:
        phrase = node.get("prompt_fragment_en") if isinstance(node, Mapping) else None
        if not isinstance(phrase, str) or phrase not in prompt_en:
            failures.append(
                {
                    "check": "literal_evidence",
                    "message": "selected moe atom phrase is absent from prompt",
                    "node_id": node.get("id") if isinstance(node, Mapping) else None,
                }
            )
    evidence = composed.get("moe_evidence")
    expected_evidence: list[dict[str, Any]] = []
    if isinstance(grammar, Mapping):
        for candidate in grammar.get("selected_candidates", []):
            element_nodes = [
                node
                for node in nodes
                if isinstance(node, Mapping)
                and node.get("element_id") == candidate.get("element_id")
            ]
            expected_evidence.append(
                {
                    "element_id": candidate.get("element_id"),
                    "candidate_id": candidate.get("candidate_id"),
                    "primary_phrase": next(
                        (
                            node.get("prompt_fragment_en")
                            for node in element_nodes
                            if node.get("id")
                            == candidate.get("selected_primary_atom_id")
                        ),
                        None,
                    ),
                    "support_phrases": [
                        node.get("prompt_fragment_en")
                        for node in element_nodes
                        if node.get("id")
                        in candidate.get("selected_support_atom_ids", [])
                    ],
                }
            )
    if evidence != expected_evidence:
        failures.append(
            {"check": "moe_evidence", "message": "moe evidence projection drift"}
        )
    if meaning_aware:
        semantic_contract = pack.get("semantic_contract")
        expected_semantic_keys = {
            "schema",
            "original_request_sha256",
            "meaning_contracts_sha256",
            "safety_evaluation_source",
            "silent_semantic_substitution",
        }
        if visual_aware:
            expected_semantic_keys.update(
                {
                    "visual_meaning_contracts_sha256",
                    "image_search_evidence_sha256",
                    "alias_resolution_policy",
                }
            )
        if pack_schema == PACK_SCHEMA_V7:
            expected_semantic_keys.add("visual_additions_sha256")
        if (
            not isinstance(semantic_contract, Mapping)
            or set(semantic_contract) != expected_semantic_keys
        ):
            failures.append(
                {
                    "check": "semantic_contract",
                    "message": "meaning semantic contract is missing or structurally changed",
                }
            )
            semantic_contract = {}
        request_text = (
            request.get("request_text") if isinstance(request, Mapping) else None
        )
        expected_request_sha = (
            hashlib.sha256(request_text.encode("utf-8")).hexdigest()
            if isinstance(request_text, str)
            else None
        )
        expected_semantic_schema = {
            PACK_SCHEMA_V7: "subculture-illustration-moe-semantic-binding/v3",
            PACK_SCHEMA_V6: "subculture-illustration-moe-semantic-binding/v2",
            PACK_SCHEMA: "subculture-illustration-moe-semantic-binding/v1",
        }.get(pack_schema, "subculture-illustration-moe-semantic-binding/v1")
        if semantic_contract.get("schema") != expected_semantic_schema:
            failures.append(
                {"check": "semantic_contract", "message": "semantic schema drift"}
            )
        if semantic_contract.get("original_request_sha256") != expected_request_sha:
            failures.append(
                {
                    "check": "semantic_contract",
                    "message": "original request meaning hash drift",
                }
            )
        if semantic_contract.get("safety_evaluation_source") != (
            "original_request_plus_canonical_meaning"
        ):
            failures.append(
                {
                    "check": "semantic_contract",
                    "message": "safety must evaluate both original text and canonical meaning",
                }
            )
        if semantic_contract.get("silent_semantic_substitution") != "forbidden":
            failures.append(
                {
                    "check": "semantic_contract",
                    "message": "silent semantic substitution must remain forbidden",
                }
            )

        bindings = (
            grammar.get("meaning_bindings") if isinstance(grammar, Mapping) else None
        )
        selected_candidates = (
            grammar.get("selected_candidates", [])
            if isinstance(grammar, Mapping)
            else []
        )
        if not isinstance(selected_candidates, list):
            failures.append(
                {
                    "check": "meaning_bindings",
                    "message": "selected candidates must be an array",
                }
            )
            selected_candidates = []
        selected_ids = [
            candidate.get("element_id")
            for candidate in selected_candidates
            if isinstance(candidate, Mapping)
        ]
        if (
            not isinstance(bindings, list)
            or len(bindings) != len(selected_ids)
            or any(not isinstance(binding, Mapping) for binding in bindings)
            or [
                binding.get("element_id")
                for binding in bindings
                if isinstance(binding, Mapping)
            ]
            != selected_ids
        ):
            failures.append(
                {
                    "check": "meaning_bindings",
                    "message": "meaning bindings do not match selected element order",
                }
            )
            bindings = []

        canonical_contract_rows: list[dict[str, Any]] = []
        expected_grammar_version = {
            PACK_SCHEMA_V7: "v5",
            PACK_SCHEMA_V6: "v4",
            PACK_SCHEMA: "v3",
        }.get(pack_schema, "v3")
        if (
            resolved_grammar_for_audit is None
            or resolved_grammar_for_audit.version != expected_grammar_version
        ):
            failures.append(
                {
                    "check": "meaning_bindings",
                    "message": (
                        f"audit requires the validated {expected_grammar_version} "
                        "meaning grammar"
                    ),
                }
            )
        else:
            expected_meaning_sha = resolved_grammar_for_audit.payload.get(
                "meaning_contracts_sha256"
            )
            if (
                semantic_contract.get("meaning_contracts_sha256")
                != expected_meaning_sha
            ):
                failures.append(
                    {
                        "check": "meaning_bindings",
                        "message": "meaning-contract asset hash drift",
                    }
                )
            if visual_aware:
                expected_visual_sha = resolved_grammar_for_audit.payload.get(
                    "visual_meaning_contracts_sha256"
                )
                expected_image_evidence_sha = resolved_grammar_for_audit.payload.get(
                    "image_search_evidence_sha256"
                )
                if (
                    semantic_contract.get("visual_meaning_contracts_sha256")
                    != expected_visual_sha
                ):
                    failures.append(
                        {
                            "check": "visual_meaning_bindings",
                            "message": "visual-meaning contract asset hash drift",
                        }
                    )
                if (
                    semantic_contract.get("image_search_evidence_sha256")
                    != expected_image_evidence_sha
                ):
                    failures.append(
                        {
                            "check": "visual_meaning_bindings",
                            "message": "image-search evidence asset hash drift",
                        }
                    )
                expected_alias_policy = (
                    "typed_exact_variant_carrier_related_ambiguous_v2"
                    if pack_schema == PACK_SCHEMA_V7
                    else "typed_exact_variant_carrier_related_v1"
                )
                if semantic_contract.get("alias_resolution_policy") != expected_alias_policy:
                    failures.append(
                        {
                            "check": "visual_alias_policy",
                            "message": "typed visual alias policy drift",
                        }
                    )
                if pack_schema == PACK_SCHEMA_V7 and semantic_contract.get(
                    "visual_additions_sha256"
                ) != resolved_grammar_for_audit.payload.get(
                    "visual_additions_sha256"
                ):
                    failures.append(
                        {
                            "check": "visual_additions",
                            "message": "visual additions asset hash drift",
                        }
                    )
            for candidate in selected_candidates:
                if not isinstance(candidate, Mapping):
                    failures.append(
                        {
                            "check": "meaning_bindings",
                            "message": "selected candidate entries must be objects",
                        }
                    )
                    continue
                element_id = candidate.get("element_id")
                expected_element = resolved_grammar_for_audit.elements_by_id.get(
                    str(element_id)
                )
                if expected_element is None:
                    failures.append(
                        {
                            "check": "meaning_bindings",
                            "message": f"unknown meaning-bound element {element_id}",
                        }
                    )
                    continue
                expected_contract = expected_element["meaning_contract"]
                expected_contract_hash = expected_element["meaning_contract_sha256"]
                canonical_contract_rows.append(
                    {
                        "element_id": element_id,
                        "contract_sha256": expected_contract_hash,
                        "contract": expected_contract,
                    }
                )
                if len(canonical_contract_rows) > len(bindings):
                    continue
                binding = bindings[len(canonical_contract_rows) - 1]
                if set(binding) != {
                    "element_id",
                    "source",
                    "contract_sha256",
                    "contract",
                }:
                    failures.append(
                        {
                            "check": "meaning_bindings",
                            "message": f"{element_id} meaning binding structure drift",
                        }
                    )
                if binding.get("source") != "canonical_research_contract":
                    failures.append(
                        {
                            "check": "meaning_bindings",
                            "message": f"{element_id} meaning binding source drift",
                        }
                    )
                if binding.get(
                    "contract_sha256"
                ) != expected_contract_hash or canonical_json_bytes(
                    binding.get("contract")
                ) != canonical_json_bytes(expected_contract):
                    failures.append(
                        {
                            "check": "meaning_bindings",
                            "message": f"{element_id} canonical meaning contract drift",
                        }
                    )
                if (
                    candidate.get("meaning_contract_sha256") != expected_contract_hash
                    or candidate.get("semantic_fidelity")
                    != expected_contract["semantic_fidelity"]
                ):
                    failures.append(
                        {
                            "check": "semantic_fidelity",
                            "message": f"{element_id} fidelity declaration drift",
                        }
                    )

        expected_meaning_evidence = [
            {
                "element_id": row["element_id"],
                "contract_sha256": row["contract_sha256"],
                "semantic_fidelity": row["contract"]["semantic_fidelity"],
                "component_groups": copy.deepcopy(row["contract"]["component_groups"]),
                "runtime_forbidden_labels": list(
                    row["contract"]["runtime_forbidden_labels"]
                ),
            }
            for row in canonical_contract_rows
        ]
        if composed.get("meaning_evidence") != expected_meaning_evidence:
            failures.append(
                {
                    "check": "meaning_evidence",
                    "message": "composed meaning evidence projection drift",
                }
            )

        runtime_surfaces = [prompt_en, str(composed.get("negative_en") or "")]
        resolved_mode = (
            grammar.get("frame_contract", {}).get("resolved_output_mode")
            if isinstance(grammar, Mapping)
            and isinstance(grammar.get("frame_contract"), Mapping)
            else None
        )
        for row in canonical_contract_rows:
            element_id = row["element_id"]
            contract = row["contract"]
            for label in contract.get("runtime_forbidden_labels", []):
                if any(runtime_label_present(label, text) for text in runtime_surfaces):
                    failures.append(
                        {
                            "check": "runtime_label_policy",
                            "message": f"{element_id} leaks forbidden runtime label {label!r}",
                        }
                    )
            for group in contract.get("component_groups", []):
                alternatives = group.get("alternatives_en", [])
                matches = [
                    alternative
                    for alternative in alternatives
                    if _normalized_phrase_contains(prompt_en, alternative)
                ]
                if len(matches) < group.get("minimum", 1):
                    failures.append(
                        {
                            "check": "meaning_component_group",
                            "element_id": element_id,
                            "group_id": group.get("id"),
                            "message": "required component group is not visibly bound in prompt",
                        }
                    )
            capability = contract.get("capability", {})
            if capability.get("sequence") == "required" and resolved_mode not in {
                "paired_frame",
                "sequence",
            }:
                failures.append(
                    {
                        "check": "meaning_capability",
                        "message": f"{element_id} requires paired or sequential evidence",
                    }
                )
            if (
                capability.get("interaction") == "required"
                and resolved_mode != "optical_interaction"
            ):
                failures.append(
                    {
                        "check": "meaning_capability",
                        "message": f"{element_id} requires an interaction-capable output",
                    }
                )
            if contract.get("adult_requirement") in {
                "explicit_adult_for_body_focus",
                "explicit_adult_if_suggestive",
                "explicit_adult_always",
            } and not _normalized_phrase_contains(prompt_en, "adult"):
                failures.append(
                    {
                        "check": "adult_subject",
                        "message": f"{element_id} requires an explicitly adult subject",
                    }
                )
        if visual_aware:
            visual_bindings = (
                grammar.get("visual_bindings")
                if isinstance(grammar, Mapping)
                else None
            )
            if (
                not isinstance(visual_bindings, list)
                or len(visual_bindings) != len(selected_ids)
                or any(not isinstance(binding, Mapping) for binding in visual_bindings)
                or [
                    binding.get("element_id")
                    for binding in visual_bindings
                    if isinstance(binding, Mapping)
                ]
                != selected_ids
            ):
                failures.append(
                    {
                        "check": "visual_meaning_bindings",
                        "message": (
                            "visual meaning bindings do not match selected element order"
                        ),
                    }
                )
                visual_bindings = []

            expected_visual_evidence: list[dict[str, Any]] = []
            if (
                resolved_grammar_for_audit is not None
                and resolved_grammar_for_audit.version in {"v4", "v5"}
            ):
                if resolved_grammar_for_audit.version == "v5":
                    expected_asset_hashes = {
                        "moe_visual_additions_v1_sha256": (
                            resolved_grammar_for_audit.payload.get(
                                "visual_additions_sha256"
                            )
                        ),
                        "moe_visual_meaning_effective_v3_sha256": (
                            resolved_grammar_for_audit.payload.get(
                                "visual_meaning_contracts_sha256"
                            )
                        ),
                        "moe_image_search_evidence_effective_v2_sha256": (
                            resolved_grammar_for_audit.payload.get(
                                "image_search_evidence_sha256"
                            )
                        ),
                    }
                else:
                    expected_asset_hashes = {
                        "moe_visual_meaning_contracts_v2_sha256": (
                            resolved_grammar_for_audit.payload.get(
                                "visual_meaning_contracts_sha256"
                            )
                        ),
                        "moe_image_search_evidence_v1_sha256": (
                            resolved_grammar_for_audit.payload.get(
                                "image_search_evidence_sha256"
                            )
                        ),
                    }
                asset_hashes = pack.get("asset_hashes")
                for key, expected_hash in expected_asset_hashes.items():
                    if (
                        not isinstance(asset_hashes, Mapping)
                        or asset_hashes.get(key) != expected_hash
                    ):
                        failures.append(
                            {
                                "check": "visual_asset_hashes",
                                "message": f"{key} drift",
                            }
                        )

                for index, candidate in enumerate(selected_candidates):
                    if not isinstance(candidate, Mapping):
                        continue
                    element_id = str(candidate.get("element_id"))
                    expected_element = resolved_grammar_for_audit.elements_by_id.get(
                        element_id
                    )
                    if expected_element is None:
                        continue
                    contract = expected_element["visual_meaning_contract"]
                    contract_hash = expected_element[
                        "visual_meaning_contract_sha256"
                    ]
                    variant_id = candidate.get("visual_variant_id")
                    variant = _visual_variants_by_id(contract).get(str(variant_id))
                    if variant is None:
                        failures.append(
                            {
                                "check": "visual_variant",
                                "element_id": element_id,
                                "message": "selected visual variant is unknown",
                            }
                        )
                        continue
                    if candidate.get("subtype_id") not in variant[
                        "candidate_subtype_ids"
                    ]:
                        failures.append(
                            {
                                "check": "visual_variant",
                                "element_id": element_id,
                                "message": (
                                    "candidate subtype belongs to a different visual "
                                    "variant"
                                ),
                            }
                        )
                    if (
                        candidate.get("visual_meaning_contract_sha256")
                        != contract_hash
                    ):
                        failures.append(
                            {
                                "check": "visual_meaning_bindings",
                                "element_id": element_id,
                                "message": "selected candidate visual contract hash drift",
                            }
                        )

                    expected_binding = {
                        "element_id": element_id,
                        "source": "typed_visual_meaning_contract",
                        "contract_sha256": contract_hash,
                        "contract": contract,
                        "selected_variant_id": variant["id"],
                        "selected_variant": variant,
                        "image_evidence_id": contract["image_evidence_id"],
                    }
                    if index >= len(visual_bindings) or canonical_json_bytes(
                        visual_bindings[index]
                    ) != canonical_json_bytes(expected_binding):
                        failures.append(
                            {
                                "check": "visual_meaning_bindings",
                                "element_id": element_id,
                                "message": "visual meaning binding drift",
                            }
                        )

                    expected_visual_evidence.append(
                        _visual_evidence_projection(
                            element_id=element_id,
                            contract_sha256_value=str(contract_hash),
                            variant=variant,
                            image_evidence_id=str(contract["image_evidence_id"]),
                        )
                    )

                    required_fields = (
                        "all_of_en",
                        "topology_edges_en",
                        "camera_requirements_en",
                        "temporal_states_en",
                        "interaction_requirements_en",
                    )
                    for field in required_fields:
                        for phrase in variant[field]:
                            if not _normalized_phrase_contains(prompt_en, phrase):
                                failures.append(
                                    {
                                        "check": "visual_requirement",
                                        "element_id": element_id,
                                        "variant_id": variant["id"],
                                        "field": field,
                                        "message": (
                                            "required visual phrase is absent from prompt"
                                        ),
                                    }
                                )
                    any_of = variant["any_of"]
                    any_matches = [
                        phrase
                        for phrase in any_of["alternatives_en"]
                        if _normalized_phrase_contains(prompt_en, phrase)
                    ]
                    if len(any_matches) < any_of["minimum"]:
                        failures.append(
                            {
                                "check": "visual_any_of",
                                "element_id": element_id,
                                "variant_id": variant["id"],
                                "message": "visual alternative minimum is not met",
                            }
                        )
                    if resolved_mode not in variant["supported_output_modes"]:
                        failures.append(
                            {
                                "check": "visual_output_mode",
                                "element_id": element_id,
                                "variant_id": variant["id"],
                                "message": (
                                    "resolved output mode cannot prove this visual variant"
                                ),
                            }
                        )

            if composed.get("visual_evidence") != expected_visual_evidence:
                failures.append(
                    {
                        "check": "visual_evidence",
                        "message": "composed visual evidence projection drift",
                    }
                )
            intent_rows = pack.get("moe_intent")
            if not isinstance(intent_rows, list) or any(
                not isinstance(row, Mapping)
                or row.get("alias_relation")
                not in {"canonical", *ACTIVATING_ALIAS_RELATIONS}
                for row in intent_rows
            ):
                failures.append(
                    {
                        "check": "visual_alias_policy",
                        "message": "non-activating or untyped visual alias reached v6",
                    }
                )
    if isinstance(base_pack, Mapping):
        if pack.get("safety") != base_pack.get("safety"):
            failures.append(
                {"check": "safety", "message": "base safety contract changed"}
            )
        if pack.get("negative_en") != base_pack.get("negative_en"):
            failures.append(
                {"check": "negative_en", "message": "base negative prompt changed"}
            )
    return {
        "schema": expected_audit_schema,
        "status": "pass" if not failures else "fail",
        "pack_id": supplied_pack_id,
        "selected_element_count": len(
            grammar.get("selected_candidates", [])
            if isinstance(grammar, Mapping)
            and isinstance(grammar.get("selected_candidates"), list)
            else []
        ),
        "failures": failures,
        "limits": [
            "This audit proves research-backed candidate selection and literal prompt binding, not rendered pixels or universal reader preference.",
            "The unchanged base pack still requires its ordinary composed-prompt audit before rendering.",
        ],
    }


__all__ = [
    "ASSET_SCHEMA",
    "AUDIT_SCHEMA",
    "COMPOSED_SCHEMA",
    "COMPOSED_SCHEMA_V2",
    "COMPOSED_SCHEMA_V4",
    "COMPOSED_SCHEMA_V5",
    "GRAMMAR_SCHEMA",
    "GRAMMAR_SCHEMA_V2",
    "GRAMMAR_SCHEMA_V4",
    "GRAMMAR_SCHEMA_V5",
    "MAX_SELECTED_ELEMENTS",
    "MoeGrammarAssets",
    "MoeElementAssets",
    "MoeElementError",
    "PLAN_SCHEMA",
    "PACK_AUDIT_SCHEMA",
    "PACK_AUDIT_SCHEMA_V2",
    "PACK_AUDIT_SCHEMA_V4",
    "PACK_AUDIT_SCHEMA_V5",
    "PACK_SCHEMA",
    "PACK_SCHEMA_V4",
    "PACK_SCHEMA_V6",
    "PACK_SCHEMA_V7",
    "RESEARCH_SCHEMA",
    "audit_moe_element_prompt",
    "audit_moe_candidate_pack",
    "build_moe_candidate_pack",
    "build_moe_element_plan",
    "canonical_json_bytes",
    "compose_moe_prompt_draft",
    "default_asset_dir",
    "list_moe_elements",
    "load_moe_element_assets",
    "load_moe_grammar_assets",
    "normalize_text",
    "resolve_element_tokens",
]
