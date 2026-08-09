#!/usr/bin/env python3
"""Deterministic runtime for the subculture illustration candidate pack.

This module deliberately owns no prompt-composition or image-generation logic.  It
loads the sibling skill's three typed assets, resolves one topic and one output
variant with scoped literal rules, selects one declared sparse visual bundle, and
returns a compact, canonical candidate pack for an agent composer.

The implementation is standard-library only and does not import the photographic
prompt runtime, a semantic index, an embedding client, or a network client.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Iterable, Mapping, Sequence
import unicodedata


LEGACY_CONTRACT_VERSION = "subculture-illustration-candidate-pack/v1"
LEGACY_GENERATOR_VERSION = "subculture-illustration-generator/v1"
CONTRACT_VERSION = "subculture-illustration-candidate-pack/v2"
GENERATOR_VERSION = "subculture-illustration-generator/v2"
SELECTION_MODE = "deterministic_rule_v1"
DEFAULT_CREATIVITY = 0.85

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

ASSET_FILENAMES = {
    "topic_crosswalk": "illustration_topic_crosswalk_v1.json",
    "format_profiles": "illustration_format_profiles_v1.json",
    "mechanism_graph": "illustration_mechanism_graph_v1.json",
    "research_manifest": "research_evidence_illustration/manifest.json",
}

EXPECTED_SCHEMAS = {
    "topic_crosswalk": "subculture-illustration-topic-crosswalk/v1",
    "format_profiles": "subculture-illustration-format-profiles/v1",
    "mechanism_graph": "subculture-illustration-mechanism-graph/v1",
    "research_manifest": "subculture_illustration_research_manifest_v1",
}

FORMAT_FAMILY_IDS = {
    "single_frame",
    "key_art",
    "cover",
    "card",
    "vertical_sequence",
    "adaptation_board",
}

FORMAT_VARIANT_IDS = {
    "single_illustration",
    "key_art",
    "ensemble_key_art",
    "responsive_key_art",
    "light_novel_cover",
    "collectible_card",
    "vertical_scroll_sequence",
    "character_design_board",
    "merch_adaptation_board",
    "campaign_art_board",
}

NODE_ROLES = {"visual_atom", "router", "guard"}
LOCALES = ("ko", "en", "ja", "zh")
MAX_SUPPORT_CUES = 2

BASE_NEGATIVE_TERMS = (
    "named artist or studio imitation",
    "protected character or franchise copy",
    "franchise logo",
    "readable generated title text",
    "random symbol stack",
    "universal color or shape stereotype",
    "aspect-ratio-only composition",
    "unclear actor-action-target relation",
    "equal-detail clutter",
)

FORMAT_NEGATIVE_TERMS = {
    "single_illustration": (
        "static character lineup",
        "lore exposition text",
    ),
    "key_art": (
        "asset collage",
        "logo-dependent identity",
    ),
    "ensemble_key_art": (
        "matching-pose lineup",
        "merged cast silhouettes",
    ),
    "responsive_key_art": (
        "critical edge crop",
        "ratio suffix without safe-zone design",
    ),
    "light_novel_cover": (
        "generic centered beauty portrait",
        "trope icon stack",
    ),
    "collectible_card": (
        "paid-rarity interface",
        "effect cloud hiding the action",
    ),
    "vertical_scroll_sequence": (
        "single poster stretched vertically",
        "dense equal panels",
    ),
    "character_design_board": (
        "copy-paste pose",
        "identity from face alone",
    ),
    "merch_adaptation_board": (
        "detail shrink only",
        "identity-losing simplification",
    ),
    "campaign_art_board": (
        "identical asset reuse",
        "unrelated palette variants",
    ),
}

FORMAT_EVIDENCE_FIELDS = {
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

CREATIVE_CUES = (
    "creative",
    "original",
    "ingenious",
    "inventive",
    "surprising",
    "authorial",
    "창의적",
    "독창적",
    "기발한",
    "참신한",
    "작가적",
    "작가의 터치",
    "創意",
    "独創",
    "独创",
)


class IllustrationRuntimeError(Exception):
    """Base runtime failure with a stable CLI exit category."""

    exit_code = 1


class InputContractError(IllustrationRuntimeError):
    """Invalid caller input."""

    exit_code = 2


class AssetValidationError(IllustrationRuntimeError):
    """Missing, malformed, or internally inconsistent runtime assets."""

    exit_code = 3


class ResolutionError(IllustrationRuntimeError):
    """Unknown, ambiguous, or incompatible route/format resolution."""

    exit_code = 4


@dataclass(frozen=True)
class RuntimeAssets:
    asset_dir: Path
    crosswalk: Mapping[str, Any]
    profiles: Mapping[str, Any]
    graph: Mapping[str, Any]
    research_manifest: Mapping[str, Any]
    hashes: Mapping[str, str]
    routes_by_id: Mapping[str, Mapping[str, Any]]
    families_by_id: Mapping[str, Mapping[str, Any]]
    variants_by_id: Mapping[str, Mapping[str, Any]]
    nodes_by_id: Mapping[str, Mapping[str, Any]]
    bundles_by_id: Mapping[str, Mapping[str, Any]]


@dataclass(frozen=True)
class ResolvedRequest:
    route: Mapping[str, Any]
    variant: Mapping[str, Any]
    family: Mapping[str, Any]
    route_source: str
    format_source: str
    matched_rule_ids: tuple[str, ...]
    matched_format_alias: str | None


def default_asset_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "assets"


def normalize_text(value: str) -> str:
    """Apply the runtime's complete matching normalization contract."""

    if not isinstance(value, str):
        raise InputContractError("text values must be strings")
    normalized = unicodedata.normalize("NFKC", value).casefold()
    return " ".join(normalized.split())


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def canonical_pack_id(pack: Mapping[str, Any]) -> str:
    payload = dict(pack)
    payload["pack_id"] = None
    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()[:16]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssetValidationError(message)


def _require_mapping(value: Any, label: str) -> Mapping[str, Any]:
    _require(isinstance(value, dict), f"{label} must be an object")
    return value


def _require_list(value: Any, label: str, *, nonempty: bool = False) -> list[Any]:
    _require(isinstance(value, list), f"{label} must be an array")
    if nonempty:
        _require(bool(value), f"{label} must not be empty")
    return value


def _require_string(value: Any, label: str) -> str:
    _require(isinstance(value, str) and bool(value.strip()), f"{label} must be a nonempty string")
    return value


def _string_list(
    value: Any,
    label: str,
    *,
    nonempty: bool = False,
    unique: bool = True,
) -> list[str]:
    items = _require_list(value, label, nonempty=nonempty)
    for index, item in enumerate(items):
        _require_string(item, f"{label}[{index}]")
    if unique:
        _require(len(items) == len(set(items)), f"{label} contains duplicates")
    return items


def _unique_map(items: Sequence[Mapping[str, Any]], key: str, label: str) -> dict[str, Mapping[str, Any]]:
    result: dict[str, Mapping[str, Any]] = {}
    for index, item in enumerate(items):
        _require_mapping(item, f"{label}[{index}]")
        identifier = _require_string(item.get(key), f"{label}[{index}].{key}")
        _require(identifier not in result, f"duplicate {label} {key}: {identifier}")
        result[identifier] = item
    return result


def _load_json(path: Path, label: str) -> tuple[Mapping[str, Any], str]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise AssetValidationError(f"cannot read {label} asset {path}: {exc}") from exc
    try:
        parsed = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AssetValidationError(f"invalid UTF-8 JSON in {label} asset {path}: {exc}") from exc
    return _require_mapping(parsed, label), hashlib.sha256(raw).hexdigest()


def _validate_aliases(value: Any, label: str) -> dict[str, list[str]]:
    aliases = _require_mapping(value, label)
    _require(set(aliases) == set(LOCALES), f"{label} must contain exactly {', '.join(LOCALES)}")
    result: dict[str, list[str]] = {}
    for locale in LOCALES:
        phrases = _string_list(aliases[locale], f"{label}.{locale}")
        normalized: list[str] = []
        normalized_seen: set[str] = set()
        for phrase in phrases:
            norm = normalize_text(phrase)
            _require(bool(norm), f"{label}.{locale} contains an empty normalized alias")
            _require(norm not in normalized_seen, f"{label} repeats normalized alias {phrase!r}")
            normalized_seen.add(norm)
            normalized.append(phrase)
        result[locale] = normalized
    return result


def _count_matches(counts: Any, expected: Mapping[str, int], label: str) -> None:
    if counts is None:
        return
    obj = _require_mapping(counts, f"{label}.counts")
    aliases = {
        "routes": ("route_count", "routes"),
        "topics": ("topic_count", "topics"),
        "families": ("family_count", "families"),
        "variants": ("variant_count", "variants"),
        "nodes": ("node_count", "runtime_node_count", "nodes", "runtime_nodes"),
        "bundles": ("bundle_count", "bundles"),
    }
    for logical, expected_value in expected.items():
        present = [key for key in aliases[logical] if key in obj]
        if not present:
            continue
        for key in present:
            _require(obj[key] == expected_value, f"{label}.counts.{key} does not match asset contents")


def load_runtime_assets(asset_dir: str | Path | None = None) -> RuntimeAssets:
    """Load and strictly cross-validate all runtime-facing assets."""

    root = Path(asset_dir).expanduser().resolve() if asset_dir else default_asset_dir()
    loaded: dict[str, Mapping[str, Any]] = {}
    hashes: dict[str, str] = {}
    for label, filename in ASSET_FILENAMES.items():
        loaded[label], hashes[label] = _load_json(root / filename, label)
        _require(
            loaded[label].get("schema") == EXPECTED_SCHEMAS[label],
            f"{label}.schema must be {EXPECTED_SCHEMAS[label]!r}",
        )

    crosswalk = loaded["topic_crosswalk"]
    profiles = loaded["format_profiles"]
    graph = loaded["mechanism_graph"]
    manifest = loaded["research_manifest"]

    normalization = _require_mapping(crosswalk.get("normalization"), "topic_crosswalk.normalization")
    _require(normalization.get("form") == "NFKC", "crosswalk normalization.form must be NFKC")
    _require(normalization.get("casefold") is True, "crosswalk normalization.casefold must be true")
    _require(normalization.get("whitespace") == "collapse", "crosswalk whitespace normalization must collapse")
    _require(normalization.get("ascii_boundary") is True, "crosswalk ascii_boundary must be true")

    families = _require_list(profiles.get("families"), "format_profiles.families", nonempty=True)
    variants = _require_list(profiles.get("variants"), "format_profiles.variants", nonempty=True)
    families_by_id = _unique_map(families, "id", "format_profiles.families")
    variants_by_id = _unique_map(variants, "id", "format_profiles.variants")
    _require(set(families_by_id) == FORMAT_FAMILY_IDS, "format profile family IDs must equal the six frozen families")
    _require(set(variants_by_id) == FORMAT_VARIANT_IDS, "format variant IDs must equal the ten frozen variants")

    contract_keys = (
        "hierarchy_contract",
        "crop_contract",
        "text_safe_contract",
        "sequential_contract",
        "scale_preservation_contract",
    )
    for family_id, family in families_by_id.items():
        variant_ids = _string_list(family.get("variant_ids"), f"family {family_id}.variant_ids", nonempty=True)
        _require(set(variant_ids) <= set(variants_by_id), f"family {family_id} references unknown variants")
        default_variant = _require_string(family.get("default_variant_id"), f"family {family_id}.default_variant_id")
        _require(default_variant in variant_ids, f"family {family_id} default variant is not a family member")
        max_support = family.get("max_support_cues")
        _require(type(max_support) is int and 0 <= max_support <= MAX_SUPPORT_CUES, f"family {family_id} max_support_cues must be 0..2")
        for key in contract_keys:
            _require_mapping(family.get(key), f"family {family_id}.{key}")
        _string_list(family.get("required_evidence_types"), f"family {family_id}.required_evidence_types", nonempty=True)
        _string_list(family.get("forbidden_substitutions"), f"family {family_id}.forbidden_substitutions", nonempty=True)

    seen_variant_membership: set[str] = set()
    for variant_id, variant in variants_by_id.items():
        family_id = _require_string(variant.get("family_id"), f"variant {variant_id}.family_id")
        _require(family_id in families_by_id, f"variant {variant_id} references unknown family {family_id}")
        _require(variant_id in families_by_id[family_id]["variant_ids"], f"variant {variant_id} missing from family {family_id}")
        seen_variant_membership.add(variant_id)
        _validate_aliases(variant.get("aliases"), f"variant {variant_id}.aliases")
        overrides = _require_mapping(variant.get("contract_overrides"), f"variant {variant_id}.contract_overrides")
        _require(set(overrides) <= set(contract_keys), f"variant {variant_id} has unknown contract override keys")
        for key, value in overrides.items():
            _require_mapping(value, f"variant {variant_id}.contract_overrides.{key}")
        _string_list(variant.get("required_evidence_types"), f"variant {variant_id}.required_evidence_types")
        _string_list(variant.get("forbidden_substitutions"), f"variant {variant_id}.forbidden_substitutions")
    _require(seen_variant_membership == set(variants_by_id), "each variant must belong to exactly one known family")
    _count_matches(profiles.get("counts"), {"families": 6, "variants": 10}, "format_profiles")

    routes = _require_list(crosswalk.get("routes"), "topic_crosswalk.routes", nonempty=True)
    routes_by_id = _unique_map(routes, "route_id", "topic_crosswalk.routes")
    _require(len(routes_by_id) == 24, "topic crosswalk must contain exactly 24 routes")
    topic_ids: set[str] = set()
    for route_id, route in routes_by_id.items():
        topic_id = _require_string(route.get("topic_id"), f"route {route_id}.topic_id")
        _require(topic_id not in topic_ids, f"duplicate topic_id {topic_id}")
        topic_ids.add(topic_id)
        _require(topic_id == route_id, f"v1 route_id and topic_id must match for {route_id}")
        _require(type(route.get("ordinal")) is int and route["ordinal"] > 0, f"route {route_id}.ordinal must be positive")
        _require_string(route.get("family_id"), f"route {route_id}.family_id")
        _require_string(route.get("matrix_id"), f"route {route_id}.matrix_id")
        _string_list(route.get("source_record_ids"), f"route {route_id}.source_record_ids", nonempty=True)
        allowed = _string_list(route.get("allowed_variant_ids"), f"route {route_id}.allowed_variant_ids", nonempty=True)
        _require(set(allowed) <= set(variants_by_id), f"route {route_id} references unknown variants")
        default_variant = _require_string(route.get("default_variant_id"), f"route {route_id}.default_variant_id")
        _require(default_variant in allowed, f"route {route_id} default variant is not allowed")
        _validate_aliases(route.get("aliases"), f"route {route_id}.aliases")
        rules = _require_list(route.get("routing_rules"), f"route {route_id}.routing_rules", nonempty=True)
        rule_ids: set[str] = set()
        for index, rule_raw in enumerate(rules):
            rule = _require_mapping(rule_raw, f"route {route_id}.routing_rules[{index}]")
            rule_id = _require_string(rule.get("id"), f"route {route_id}.routing_rules[{index}].id")
            _require(rule_id not in rule_ids, f"route {route_id} repeats routing rule {rule_id}")
            rule_ids.add(rule_id)
            _require(rule.get("locale") in LOCALES, f"routing rule {rule_id} has invalid locale")
            _require(rule.get("match") == "exact_phrase", f"routing rule {rule_id} must use exact_phrase")
            _require(type(rule.get("priority")) is int and rule["priority"] >= 3000, f"routing rule {rule_id} priority must be >=3000")
            phrases = _string_list(rule.get("phrases"), f"routing rule {rule_id}.phrases", nonempty=True)
            declared_aliases = {normalize_text(item) for item in route["aliases"][rule["locale"]]}
            _require(
                {normalize_text(item) for item in phrases} <= declared_aliases,
                f"routing rule {rule_id} phrases must be declared route aliases",
            )
        _string_list(route.get("visual_candidate_ids"), f"route {route_id}.visual_candidate_ids", nonempty=True)
        _string_list(route.get("bundle_ids"), f"route {route_id}.bundle_ids", nonempty=True)
        # Research-derived router and guard roles are topic-local evidence, not
        # universal boilerplate.  A topic with no such candidate must retain an
        # explicit empty list rather than receiving an invented shared node.
        _string_list(route.get("router_candidate_ids"), f"route {route_id}.router_candidate_ids")
        _string_list(route.get("guard_candidate_ids"), f"route {route_id}.guard_candidate_ids")
    _require(sorted(route["ordinal"] for route in routes) == list(range(1, 25)), "route ordinals must be exactly 1..24")
    _count_matches(crosswalk.get("counts"), {"routes": 24, "topics": 24}, "topic_crosswalk")

    family_defaults = _require_mapping(crosswalk.get("format_family_defaults"), "topic_crosswalk.format_family_defaults")
    _require(set(family_defaults) == FORMAT_FAMILY_IDS, "format_family_defaults must cover exactly six format families")

    _require(graph.get("domain") == "subculture_illustration", "mechanism_graph.domain must be subculture_illustration")
    _require(graph.get("max_support_cues") == MAX_SUPPORT_CUES, "mechanism_graph.max_support_cues must be 2")
    nodes = _require_list(graph.get("runtime_nodes"), "mechanism_graph.runtime_nodes", nonempty=True)
    bundles = _require_list(graph.get("bundles"), "mechanism_graph.bundles", nonempty=True)
    nodes_by_id = _unique_map(nodes, "id", "mechanism_graph.runtime_nodes")
    bundles_by_id = _unique_map(bundles, "id", "mechanism_graph.bundles")

    for node_id, node in nodes_by_id.items():
        role = node.get("role")
        _require(role in NODE_ROLES, f"node {node_id} has invalid role {role!r}")
        topic_id = _require_string(node.get("topic_id"), f"node {node_id}.topic_id")
        _require(topic_id in topic_ids, f"node {node_id} references unknown topic {topic_id}")
        _require_string(node.get("family_id"), f"node {node_id}.family_id")
        _require_string(node.get("definition"), f"node {node_id}.definition")
        _require(type(node.get("primary_eligible")) is bool, f"node {node_id}.primary_eligible must be boolean")
        _require(type(node.get("support_eligible")) is bool, f"node {node_id}.support_eligible must be boolean")
        format_ids = _string_list(node.get("format_family_ids"), f"node {node_id}.format_family_ids", nonempty=True)
        _require(set(format_ids) <= FORMAT_FAMILY_IDS, f"node {node_id} references unknown format families")
        provenance = _require_mapping(node.get("provenance"), f"node {node_id}.provenance")
        _require_string(provenance.get("matrix_id"), f"node {node_id}.provenance.matrix_id")
        _string_list(provenance.get("evidence_record_ids"), f"node {node_id}.provenance.evidence_record_ids", nonempty=True)
        kinds = _string_list(provenance.get("provenance_kinds"), f"node {node_id}.provenance.provenance_kinds", nonempty=True)
        _require(set(kinds) <= {"source_supported", "cross_source_synthesis", "design_inference"}, f"node {node_id} has invalid provenance kinds")
        _require(provenance.get("definition_source") == "candidate_definitions", f"node {node_id} definition source must be candidate_definitions")
        if role != "visual_atom":
            _require(not node["primary_eligible"] and not node["support_eligible"], f"nonvisual node {node_id} cannot be selectable")

    for route_id, route in routes_by_id.items():
        role_fields = (
            ("visual_candidate_ids", "visual_atom"),
            ("router_candidate_ids", "router"),
            ("guard_candidate_ids", "guard"),
        )
        for field, expected_role in role_fields:
            for node_id in route[field]:
                _require(node_id in nodes_by_id, f"route {route_id} references unknown node {node_id}")
                node = nodes_by_id[node_id]
                _require(node["role"] == expected_role, f"route {route_id} {field} contains non-{expected_role} node {node_id}")
                _require(node["topic_id"] == route["topic_id"], f"route {route_id} contains node from another topic: {node_id}")

    for bundle_id, bundle in bundles_by_id.items():
        route_id = _require_string(bundle.get("route_id"), f"bundle {bundle_id}.route_id")
        _require(route_id in routes_by_id, f"bundle {bundle_id} references unknown route {route_id}")
        format_ids = _string_list(bundle.get("format_family_ids"), f"bundle {bundle_id}.format_family_ids", nonempty=True)
        _require(set(format_ids) <= FORMAT_FAMILY_IDS, f"bundle {bundle_id} references unknown format families")
        primary_id = _require_string(bundle.get("primary_node_id"), f"bundle {bundle_id}.primary_node_id")
        support_ids = _string_list(bundle.get("support_node_ids"), f"bundle {bundle_id}.support_node_ids")
        _require(len(support_ids) <= MAX_SUPPORT_CUES, f"bundle {bundle_id} has more than two supports")
        _require(primary_id not in support_ids, f"bundle {bundle_id} repeats primary as support")
        _string_list(bundle.get("required_evidence_types"), f"bundle {bundle_id}.required_evidence_types", nonempty=True)
        _string_list(bundle.get("compatibility_basis"), f"bundle {bundle_id}.compatibility_basis", nonempty=True)
        _string_list(bundle.get("conflict_checks"), f"bundle {bundle_id}.conflict_checks", nonempty=True)
        _string_list(bundle.get("boundary_checks"), f"bundle {bundle_id}.boundary_checks", nonempty=True)
        route = routes_by_id[route_id]
        for node_id, eligibility in [(primary_id, "primary_eligible"), *[(item, "support_eligible") for item in support_ids]]:
            _require(node_id in nodes_by_id, f"bundle {bundle_id} references unknown node {node_id}")
            node = nodes_by_id[node_id]
            _require(node["role"] == "visual_atom", f"bundle {bundle_id} selects nonvisual node {node_id}")
            _require(node[eligibility] is True, f"bundle {bundle_id} selects ineligible node {node_id}")
            _require(node["topic_id"] == route["topic_id"], f"bundle {bundle_id} selects a node from another route")
            _require(bool(set(node["format_family_ids"]) & set(format_ids)), f"bundle {bundle_id} node {node_id} is format-inapplicable")

    for route_id, route in routes_by_id.items():
        for bundle_id in route["bundle_ids"]:
            _require(bundle_id in bundles_by_id, f"route {route_id} references unknown bundle {bundle_id}")
            _require(bundles_by_id[bundle_id]["route_id"] == route_id, f"route {route_id} references another route's bundle")
        _require(
            any(nodes_by_id[node_id]["primary_eligible"] for node_id in route["visual_candidate_ids"]),
            f"route {route_id} has no primary-eligible visual atom",
        )

    _count_matches(graph.get("counts"), {"nodes": len(nodes_by_id), "bundles": len(bundles_by_id)}, "mechanism_graph")

    # The manifest remains research provenance, not prompt content.  Validate only
    # the frozen aggregate identity needed by runtime provenance.
    _require(manifest.get("topic_count") == 24, "research manifest topic_count must be 24")
    _require(manifest.get("record_count") == 72, "research manifest record_count must be 72")

    return RuntimeAssets(
        asset_dir=root,
        crosswalk=crosswalk,
        profiles=profiles,
        graph=graph,
        research_manifest=manifest,
        hashes=hashes,
        routes_by_id=routes_by_id,
        families_by_id=families_by_id,
        variants_by_id=variants_by_id,
        nodes_by_id=nodes_by_id,
        bundles_by_id=bundles_by_id,
    )


def validate_assets(asset_dir: str | Path | None = None) -> dict[str, Any]:
    assets = load_runtime_assets(asset_dir)
    role_counts = {
        role: sum(node["role"] == role for node in assets.nodes_by_id.values())
        for role in sorted(NODE_ROLES)
    }
    return {
        "status": "pass",
        "asset_dir": str(assets.asset_dir),
        "route_count": len(assets.routes_by_id),
        "format_family_count": len(assets.families_by_id),
        "format_variant_count": len(assets.variants_by_id),
        "runtime_node_count": len(assets.nodes_by_id),
        "bundle_count": len(assets.bundles_by_id),
        "role_counts": role_counts,
        "asset_hashes": dict(sorted(assets.hashes.items())),
    }


def _literal_phrase_match(normalized_haystack: str, phrase: str) -> bool:
    needle = normalize_text(phrase)
    if not needle:
        return False
    if needle.isascii():
        return re.search(r"(?<![0-9a-z_])" + re.escape(needle) + r"(?![0-9a-z_])", normalized_haystack) is not None
    return needle in normalized_haystack


def _flatten_aliases(alias_map: Mapping[str, Any]) -> Iterable[str]:
    for locale in LOCALES:
        for phrase in alias_map[locale]:
            yield phrase


def _explicit_route(topic: str, assets: RuntimeAssets) -> Mapping[str, Any]:
    if topic in assets.routes_by_id:
        return assets.routes_by_id[topic]
    matches = [route for route in assets.routes_by_id.values() if route["topic_id"] == topic]
    if len(matches) == 1:
        return matches[0]
    raise ResolutionError(
        f"unknown topic/route {topic!r}; use --list-topics for the 24 exact IDs"
    )


def _explicit_variant(format_id: str, assets: RuntimeAssets) -> Mapping[str, Any]:
    if format_id not in assets.variants_by_id:
        raise ResolutionError(
            f"unknown format variant {format_id!r}; use --list-formats for exact IDs"
        )
    return assets.variants_by_id[format_id]


def _resolve_format_alias(concept_norm: str, assets: RuntimeAssets) -> tuple[Mapping[str, Any] | None, str | None]:
    hits: list[tuple[int, str, str]] = []
    for variant_id, variant in assets.variants_by_id.items():
        for phrase in _flatten_aliases(variant["aliases"]):
            if _literal_phrase_match(concept_norm, phrase):
                hits.append((len(normalize_text(phrase)), variant_id, phrase))
    if not hits:
        return None, None
    best_length = max(item[0] for item in hits)
    best = [item for item in hits if item[0] == best_length]
    variant_ids = sorted({item[1] for item in best})
    if len(variant_ids) != 1:
        raise ResolutionError(
            "ambiguous format phrases resolve equally to: " + ", ".join(variant_ids)
        )
    selected = variant_ids[0]
    phrase = sorted(item[2] for item in best if item[1] == selected)[0]
    return assets.variants_by_id[selected], phrase


def _format_default_route(family_id: str, variant_id: str, assets: RuntimeAssets) -> Mapping[str, Any]:
    raw = assets.crosswalk["format_family_defaults"].get(family_id)
    route_id: str | None = None
    if isinstance(raw, str):
        route_id = raw
    elif isinstance(raw, dict):
        for key in (variant_id, "default_route_id", "route_id", "default"):
            value = raw.get(key)
            if isinstance(value, str) and value:
                route_id = value
                break
    if route_id not in assets.routes_by_id:
        raise AssetValidationError(
            f"format default for {family_id}/{variant_id} does not resolve to a known route"
        )
    return assets.routes_by_id[route_id]


def _resolve_route_rules(
    concept_norm: str,
    assets: RuntimeAssets,
) -> tuple[Mapping[str, Any] | None, tuple[str, ...]]:
    route_hits: dict[str, tuple[int, set[str]]] = {}
    for route_id, route in assets.routes_by_id.items():
        for rule in route["routing_rules"]:
            matching = [phrase for phrase in rule["phrases"] if _literal_phrase_match(concept_norm, phrase)]
            if not matching:
                continue
            score = int(rule["priority"]) + max(len(normalize_text(item)) for item in matching)
            previous = route_hits.get(route_id)
            if previous is None or score > previous[0]:
                route_hits[route_id] = (score, {rule["id"]})
            elif score == previous[0]:
                previous[1].add(rule["id"])
    if not route_hits:
        return None, ()
    best_score = max(value[0] for value in route_hits.values())
    best_routes = sorted(route_id for route_id, value in route_hits.items() if value[0] == best_score)
    if len(best_routes) != 1:
        raise ResolutionError(
            "ambiguous topic rules resolve equally to: "
            + ", ".join(best_routes)
            + "; pass --topic explicitly"
        )
    route_id = best_routes[0]
    return assets.routes_by_id[route_id], tuple(sorted(route_hits[route_id][1]))


def resolve_request(
    concept: str,
    *,
    topic: str = "auto",
    format_id: str = "auto",
    assets: RuntimeAssets | None = None,
) -> ResolvedRequest:
    """Resolve a request without embeddings or silent lexical tie-breaking."""

    runtime_assets = assets or load_runtime_assets()
    if not isinstance(concept, str) or not concept.strip():
        raise InputContractError("--concept must be a nonempty string")
    concept_norm = normalize_text(concept)

    if format_id != "auto":
        variant = _explicit_variant(format_id, runtime_assets)
        format_source = "explicit"
        matched_format_alias = None
    else:
        variant, matched_format_alias = _resolve_format_alias(concept_norm, runtime_assets)
        format_source = "rule_exact_phrase" if variant is not None else "unresolved"

    if topic != "auto":
        route = _explicit_route(topic, runtime_assets)
        route_source = "explicit"
        matched_rule_ids: tuple[str, ...] = ()
    else:
        route, matched_rule_ids = _resolve_route_rules(concept_norm, runtime_assets)
        if route is not None:
            route_source = "rule_exact_phrase"
        else:
            if variant is None:
                variant = runtime_assets.variants_by_id["single_illustration"]
                format_source = "fallback"
            family_id = variant["family_id"]
            route = _format_default_route(family_id, variant["id"], runtime_assets)
            route_source = "format_default"

    if variant is None:
        variant = runtime_assets.variants_by_id[route["default_variant_id"]]
        format_source = "route_default"

    variant_id = variant["id"]
    if variant_id not in route["allowed_variant_ids"]:
        allowed = ", ".join(route["allowed_variant_ids"])
        raise ResolutionError(
            f"topic {route['route_id']!r} is incompatible with format {variant_id!r}; "
            f"allowed variants: {allowed}"
        )
    family = runtime_assets.families_by_id[variant["family_id"]]
    return ResolvedRequest(
        route=route,
        variant=variant,
        family=family,
        route_source=route_source,
        format_source=format_source,
        matched_rule_ids=matched_rule_ids,
        matched_format_alias=matched_format_alias,
    )


def _merge_profile_contracts(family: Mapping[str, Any], variant: Mapping[str, Any]) -> dict[str, Any]:
    overrides = variant["contract_overrides"]
    source_to_pack = {
        "hierarchy_contract": "hierarchy_contract",
        "crop_contract": "crop_contract",
        "sequential_contract": "sequence_contract",
        "scale_preservation_contract": "scale_contract",
        "text_safe_contract": "text_space_contract",
    }
    result: dict[str, Any] = {}
    for source_key, pack_key in source_to_pack.items():
        merged = dict(family[source_key])
        merged.update(overrides.get(source_key, {}))
        result[pack_key] = merged
    result["required_evidence_types"] = sorted(
        set(family["required_evidence_types"]) | set(variant["required_evidence_types"])
    )
    result["forbidden_substitutions"] = list(
        dict.fromkeys([*family["forbidden_substitutions"], *variant["forbidden_substitutions"]])
    )
    return result


def _selection_digest(
    assets: RuntimeAssets,
    concept_norm: str,
    route_id: str,
    variant_id: str,
    seed: int,
    candidate_id: str,
) -> int:
    material = "\x1f".join(
        (
            assets.hashes["mechanism_graph"],
            concept_norm,
            route_id,
            variant_id,
            str(seed),
            candidate_id,
        )
    ).encode("utf-8")
    return int.from_bytes(hashlib.sha256(material).digest(), "big")


def _select_bundle(
    resolved: ResolvedRequest,
    concept_norm: str,
    seed: int,
    assets: RuntimeAssets,
) -> tuple[Mapping[str, Any], list[str]]:
    route = resolved.route
    family_id = resolved.family["id"]
    eligible: list[Mapping[str, Any]] = []
    for bundle_id in route["bundle_ids"]:
        bundle = assets.bundles_by_id[bundle_id]
        if family_id not in bundle["format_family_ids"]:
            continue
        node_ids = [bundle["primary_node_id"], *bundle["support_node_ids"]]
        if all(family_id in assets.nodes_by_id[node_id]["format_family_ids"] for node_id in node_ids):
            eligible.append(bundle)
    if not eligible:
        raise ResolutionError(
            f"topic {route['route_id']!r} has no declared visual bundle for format family {family_id!r}"
        )
    bundle = min(
        eligible,
        key=lambda item: (
            _selection_digest(
                assets,
                concept_norm,
                route["route_id"],
                resolved.variant["id"],
                seed,
                item["id"],
            ),
            item["id"],
        ),
    )
    support_budget = min(
        MAX_SUPPORT_CUES,
        int(assets.graph["max_support_cues"]),
        int(resolved.family["max_support_cues"]),
    )
    ranked_supports = sorted(
        bundle["support_node_ids"],
        key=lambda node_id: (
            _selection_digest(
                assets,
                concept_norm,
                route["route_id"],
                resolved.variant["id"],
                seed,
                f"{bundle['id']}:{node_id}",
            ),
            node_id,
        ),
    )
    return bundle, ranked_supports[:support_budget]


def _creative_requested(concept_norm: str, creativity: float) -> bool:
    return creativity >= 0.75 or any(_literal_phrase_match(concept_norm, cue) for cue in CREATIVE_CUES)


def _negative_prompt(variant_id: str) -> str:
    terms = [*BASE_NEGATIVE_TERMS, *FORMAT_NEGATIVE_TERMS[variant_id]]
    return ", ".join(dict.fromkeys(terms))


def build_candidate_pack(
    concept: str,
    *,
    topic: str = "auto",
    format_id: str = "auto",
    seed: int = 0,
    creativity: float = DEFAULT_CREATIVITY,
    safety_evaluation: bool = False,
    contract_version: str = CONTRACT_VERSION,
    assets: RuntimeAssets | None = None,
) -> dict[str, Any]:
    """Build one deterministic, sparse, composition-ready candidate pack."""

    if type(seed) is not int:
        raise InputContractError("seed must be an integer")
    if isinstance(creativity, bool) or not isinstance(creativity, (int, float)):
        raise InputContractError("creativity must be a number from 0 through 1")
    creativity_value = float(creativity)
    if not 0.0 <= creativity_value <= 1.0:
        raise InputContractError("creativity must be from 0 through 1")
    if contract_version not in {LEGACY_CONTRACT_VERSION, CONTRACT_VERSION}:
        raise InputContractError(
            f"unsupported contract_version {contract_version!r}; expected "
            f"{LEGACY_CONTRACT_VERSION!r} or {CONTRACT_VERSION!r}"
        )

    runtime_assets = assets or load_runtime_assets()
    resolved = resolve_request(
        concept,
        topic=topic,
        format_id=format_id,
        assets=runtime_assets,
    )
    concept_norm = normalize_text(concept)
    bundle, support_ids = _select_bundle(resolved, concept_norm, seed, runtime_assets)
    primary_id = bundle["primary_node_id"]
    selected_ids = [primary_id, *support_ids]
    selected_nodes: list[dict[str, Any]] = []
    for node_id in selected_ids:
        node = runtime_assets.nodes_by_id[node_id]
        selected_nodes.append(
            {
                "id": node_id,
                "node_type": "visual_atom",
                "selected_role": "primary" if node_id == primary_id else "support",
                "definition": node["definition"],
                "observable_evidence_types": [node_id],
                "format_family_ids": list(node["format_family_ids"]),
            }
        )

    merged_profile = _merge_profile_contracts(resolved.family, resolved.variant)
    required_evidence_types = list(bundle["required_evidence_types"])
    required_ids = [
        f"route:{resolved.route['route_id']}",
        f"format:{resolved.variant['id']}",
        *[f"visual:{node_id}" for node_id in selected_ids],
    ]
    support_budget = min(MAX_SUPPORT_CUES, int(resolved.family["max_support_cues"]))
    high_creativity = _creative_requested(concept_norm, creativity_value)

    format_profile = {
        "family_id": resolved.family["id"],
        "variant_id": resolved.variant["id"],
        "max_support_cues": support_budget,
        **merged_profile,
        "required_format_evidence_fields": list(FORMAT_EVIDENCE_FIELDS[resolved.variant["id"]]),
    }

    selected_edge = {
        "id": bundle["id"],
        "route_id": resolved.route["route_id"],
        "format_family_ids": list(bundle["format_family_ids"]),
        "primary_node_id": primary_id,
        "support_node_ids": support_ids,
        "minimum_supports": min(1, len(support_ids)),
        "maximum_supports": min(support_budget, len(bundle["support_node_ids"])),
        "required_evidence_types": required_evidence_types,
    }

    safety: dict[str, Any]
    if safety_evaluation:
        safety = {
            "mode": "explicit_evaluation",
            "evaluation_requested": True,
            "status": "pass",
            "requires_user_approval": False,
            "items": [
                {"id": "original_design_boundary", "status": "pass_by_contract"},
                {"id": "adult_non_inference_boundary", "status": "pass_by_contract"},
                {"id": "platform_safety_still_applies", "status": "acknowledged"},
            ],
        }
    else:
        safety = {
            "mode": "automatic",
            "evaluation_requested": False,
            "status": "pass",
            "requires_user_approval": False,
            "items": [],
        }

    viewer_contract: dict[str, Any] = {
        "schema": "illustration-viewer-evidence/v1",
        "required_fields": [
            "first_glance_hook_phrase",
            "second_look_reveal_phrase",
            "affect_actor_phrase",
            "affect_action_phrase",
            "affect_target_phrase",
            "affect_consequence_phrase",
        ],
        "audience_literacy_required": True,
        "response_is_hypothesis": True,
    }
    composition_contract: dict[str, Any] = {
        "composer": "agent",
        "required_chosen_candidate_ids": required_ids,
        "negative_must_match_exactly": True,
        "evidence_values_must_be_literal_prompt_substrings": True,
        "final_prompt_composition_deferred": True,
    }
    if contract_version == CONTRACT_VERSION:
        viewer_contract["second_look_plan_contract"] = {
            "schema": "illustration-second-look-plan/v1",
            "required": True,
            "required_roles": ["primary_carrier", "fallback_carrier"],
            "carrier_kinds": list(SECOND_LOOK_CARRIER_KINDS),
            "risk_flags": list(SECOND_LOOK_RISK_FLAGS),
            "forbidden_as_sole": list(SECOND_LOOK_RISK_FLAGS),
            "allowed_review_scale_ids": list(merged_profile["scale_contract"]["inspection_scales"]),
            "fallback_must_reference_selected_consequence": True,
        }
        composition_contract["composed_schema"] = "subculture-illustration-composed-prompt/v2"

    pack: dict[str, Any] = {
        "contract_version": contract_version,
        "pack_id": None,
        "request_contract": {
            "request_text": concept,
            "mandatory_intents": [
                {"id": evidence_type, "evidence_key": evidence_type}
                for evidence_type in required_evidence_types
            ],
            "route_id": resolved.route["route_id"],
            "topic_id": resolved.route["topic_id"],
            "route_source": resolved.route_source,
            "format_source": resolved.format_source,
            "matched_rule_ids": list(resolved.matched_rule_ids),
            "matched_format_alias": resolved.matched_format_alias,
            "creativity": creativity_value,
        },
        "format_profile": format_profile,
        "visual_grammar": {
            "topic_id": resolved.route["topic_id"],
            "family_id": resolved.route["family_id"],
            "primary_runtime_id": primary_id,
            "support_runtime_ids": support_ids,
            "max_support_cues": support_budget,
            "runtime_nodes": selected_nodes,
            "compatible_edge_ids": [bundle["id"]],
            "selected_edge": selected_edge,
            "required_evidence_types": required_evidence_types,
        },
        "authorial_contract": {
            "schema": "illustration-authorial-grammar/v1",
            "required_fields": [
                "focal_hierarchy_phrase",
                "controlled_omission_phrase",
                "edge_or_mark_rule_phrase",
                "repeated_material_or_motif_rule_phrase",
            ],
            "creative_development_required": high_creativity,
            "familiar_anchor_required": high_creativity,
            "one_changed_rule_required": high_creativity,
            "first_second_look_required": True,
            "proposal_count_required": 4 if high_creativity else 0,
        },
        "viewer_contract": viewer_contract,
        "guard_contract": {
            "router_node_ids": list(resolved.route["router_candidate_ids"]),
            "guard_node_ids": list(resolved.route["guard_candidate_ids"]),
            "active_guards": [
                {
                    "id": node_id,
                    "policy": runtime_assets.nodes_by_id[node_id]["definition"],
                }
                for node_id in resolved.route["guard_candidate_ids"]
            ],
            "forbidden_prompt_proofs": [
                "artist_or_studio_name",
                "protected_design_or_logo",
                "market_term_as_visual_evidence",
                "universal_color_shape_or_culture_inference",
                "viewer_outcome_claim",
            ],
        },
        "composition_contract": composition_contract,
        "safety": safety,
        "negative_en": _negative_prompt(resolved.variant["id"]),
        "asset_hashes": {
            "topic_crosswalk_sha256": runtime_assets.hashes["topic_crosswalk"],
            "format_profiles_sha256": runtime_assets.hashes["format_profiles"],
            "mechanism_graph_sha256": runtime_assets.hashes["mechanism_graph"],
            "research_manifest_sha256": runtime_assets.hashes["research_manifest"],
        },
        "provenance": {
            "generator_version": (
                GENERATOR_VERSION
                if contract_version == CONTRACT_VERSION
                else LEGACY_GENERATOR_VERSION
            ),
            "selection_mode": SELECTION_MODE,
            "seed": seed,
            "normalization": "NFKC+casefold+whitespace-collapse",
        },
    }
    pack["pack_id"] = canonical_pack_id(pack)
    return pack


def list_topics(assets: RuntimeAssets | None = None) -> list[dict[str, Any]]:
    runtime_assets = assets or load_runtime_assets()
    return [
        {
            "ordinal": route["ordinal"],
            "topic_id": route["topic_id"],
            "family_id": route["family_id"],
            "default_variant_id": route["default_variant_id"],
            "allowed_variant_ids": list(route["allowed_variant_ids"]),
        }
        for route in sorted(runtime_assets.routes_by_id.values(), key=lambda item: item["ordinal"])
    ]


def list_formats(assets: RuntimeAssets | None = None) -> list[dict[str, Any]]:
    runtime_assets = assets or load_runtime_assets()
    return [
        {
            "variant_id": variant_id,
            "family_id": variant["family_id"],
            "aliases": {locale: list(variant["aliases"][locale]) for locale in LOCALES},
        }
        for variant_id, variant in sorted(runtime_assets.variants_by_id.items())
    ]


__all__ = [
    "AssetValidationError",
    "IllustrationRuntimeError",
    "InputContractError",
    "CONTRACT_VERSION",
    "DEFAULT_CREATIVITY",
    "GENERATOR_VERSION",
    "LEGACY_CONTRACT_VERSION",
    "LEGACY_GENERATOR_VERSION",
    "SECOND_LOOK_CARRIER_KINDS",
    "SECOND_LOOK_RISK_FLAGS",
    "ResolutionError",
    "RuntimeAssets",
    "ResolvedRequest",
    "build_candidate_pack",
    "canonical_json_bytes",
    "canonical_pack_id",
    "default_asset_dir",
    "list_formats",
    "list_topics",
    "load_runtime_assets",
    "normalize_text",
    "resolve_request",
    "validate_assets",
]
