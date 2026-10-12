"""Authored optional candidate semantics, independent of sampler ranking.

The native canonical candidate remains the only authored owner. Compiled bundles are a projection, not
another authored meaning registry; associated visual profiles never activate
merely because a bundle is discoverable or selected.
"""
from __future__ import annotations
import photo_native_pack

import copy
import hashlib
import json
import re
from typing import Any

from photo_contracts import property_effects_allowed

SURFACE_VERSION = "photo-candidate-semantic-surface/v1"
BUNDLE_VERSION = "photo-candidate-bundles/v1"
COMPILED_BUNDLE_FIELDS = (
    "id", "source_sha256", "associated_profile_ids", "components", "member_candidates",
    "confusion_boundaries", "relations", "adoption", "profile_activation",
)


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":")).encode("utf-8")).hexdigest()


def maintenance_tag(tag: str) -> bool:
    value = str(tag).strip().casefold()
    return value.endswith("_visual_semantics") or any(
        marker in value for marker in ("provenance_scope", "moe_review")
    )


def strings(value: Any) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        raise ValueError("candidate semantic string lists must contain non-empty strings")
    return [item.strip() for item in value]








def validate_relations(relations: Any, label: str) -> None:
    if not isinstance(relations, list):
        raise ValueError(f"{label}.relations must be an array")
    ids = []
    for relation in relations:
        if (not isinstance(relation, dict) or set(relation) != {"id", "type", "subject", "object"}
                or any(not isinstance(relation[key], str) or not relation[key].strip() for key in ("id", "type", "subject", "object"))):
            raise ValueError(f"{label}.relations require id, type, subject and object without unknown fields")
        ids.append(relation["id"])
    if len(ids) != len(set(ids)):
        raise ValueError(f"{label}.relations have duplicate IDs")






def concept_units(entry: dict[str, Any]) -> list[str]:
    """Preserve authored phrases intact, never infer relations from word order."""
    authored = strings(entry.get("concept_units"))
    if authored:
        return list(dict.fromkeys(authored))
    label = str(entry.get("label_en") or entry.get("en") or "").strip()
    # A short noun/relational label is usable inspiration. Longer source prose
    # needs explicitly authored units instead of a truncation that changes it.
    if label and len(label.split()) <= 24:
        return [label]
    return list(dict.fromkeys(strings(entry.get("keywords")) or strings(entry.get("concept_terms"))))[:12]


def semantic_source(entry: dict[str, Any], slot: str = "", policy: dict[str, Any] | None = None) -> dict[str, Any]:
    units = concept_units(entry)
    if not units:
        return {}
    result: dict[str, Any] = {
        "concept_units": units,
        "relations": copy.deepcopy(entry.get("relations") or []),
        "affected_dimensions": strings(entry.get("affected_dimensions")),
        "adoption": "optional",
    }
    if entry.get("canonical_candidate_ref"):
        result["canonical_candidate_ref"] = str(entry["canonical_candidate_ref"])
    if "affected_properties" in entry:
        result["affected_properties"] = copy.deepcopy(entry["affected_properties"])
    return result






def public_bundles(data: dict[str, Any], pack: dict[str, Any], joint_admissions: dict[str, Any] | None = None) -> dict[str, Any]:
    visible = {
        str(candidate.get("id") or ""): candidate
        for payload in photo_native_pack.role_cards(pack).values()
        for candidate in payload.get("candidates") or []
    }
    open_dimensions = set(((pack.get("authorial_core") or {}).get("intent_lock") or {}).get("open_dimensions") or [])
    result = []
    for bundle in data.get("candidate_bundles") or []:
        if bundle["id"] not in getattr(data,"admitted_ids",set()):continue
        member_ids = {member["id"] for member in bundle["member_candidates"]}
        dimensions = {dimension for member in bundle["member_candidates"]
                      for dimension in member.get("affected_dimensions") or []}
        joint_admission = (joint_admissions or {}).get(bundle["id"])
        lock = (pack.get("authorial_core") or {}).get("intent_lock") or {}
        if any(not property_effects_allowed(lock, member.get("affected_dimensions") or [],
                                           member.get("affected_properties", []))
               for member in bundle["member_candidates"]):
            continue
        if not joint_admission and (not member_ids.issubset(visible)
                or any(not member.get("affected_dimensions") for member in bundle["member_candidates"])
                or not dimensions.issubset(open_dimensions)
                or any((visible[member_id].get("applicability") or {}).get("status") != "eligible" for member_id in member_ids)
                or any(member_ids.intersection(visible[member_id].get("conflicts_with") or []) for member_id in member_ids)):
            continue
        row = copy.deepcopy(bundle)
        row["source_contract_sha256"] = digest(bundle)
        if joint_admission:
            row["joint_admission"] = copy.deepcopy(joint_admission)
            row["member_selection"] = "bundle_only_unless_already_eligible_standalone"
        row["id"] = row["id"]
        row["content_form"] = "unordered_inspiration_terms"
        row["semantic_surface_version"] = SURFACE_VERSION
        row["concept_units"] = [unit for component in row["components"] for unit in component["concept_units"]]
        row["concept_terms"] = list(row["concept_units"])
        row["affected_dimensions"] = sorted(dimensions)
        row["conflicts_with"] = sorted({conflict for member_id in member_ids for conflict in visible.get(member_id, {}).get("conflicts_with") or []})
        row["applicability"] = {"status": "eligible", "source": "source_recomputed_joint_adoption" if joint_admission else "all_members_eligible_and_dimensions_open"}
        row["selection_contract"] = {
            "component_evidence": "every_component_id_to_literal_final_prompt_phrase",
            "relation_evidence": "every_relation_id_to_literal_final_prompt_phrase",
            "scope": "one_coherent_realization",
            "associated_profiles_are_not_promoted": True,
        }
        result.append(row)
    seed = str((pack.get("provenance") or {}).get("seed") or "")
    result.sort(key=lambda row: digest([seed, row["id"]]))
    limit = ((data.get("candidate_semantic_policy") or {}).get("joint_adoption") or {}).get("maximum_bundles", len(result))
    result = result[:limit]
    return {"contract_version": BUNDLE_VERSION, "adoption": "optional",
            "candidate_order": "seed_shuffled_non_preferential", "candidates": result}


def bundle_source_material(bundle: dict[str, Any]) -> dict[str, Any]:
    material = {key: copy.deepcopy(bundle[key]) for key in COMPILED_BUNDLE_FIELDS if key in bundle}
    material["id"] = str(material.get("id") or "")
    return material


def apply_public_semantics(pack: dict[str, Any], sources: dict[str, dict[str, Any]]) -> None:
    def visit(value: Any) -> None:
        if isinstance(value, list):
            for item in value:
                visit(item)
        elif isinstance(value, dict):
            candidate_id = str(value.get("id") or value.get("candidate_id") or "")
            source = sources.get(candidate_id)
            if source and value.get("content_form") == "unordered_inspiration_terms":
                value.update(copy.deepcopy(source))
                value["semantic_surface_version"] = SURFACE_VERSION
                value["concept_terms"] = list(source["concept_units"])
            for item in value.values():
                visit(item)
    visit(pack)
    if isinstance(pack,photo_native_pack.WorkingPack):visit(photo_native_pack.role_cards(pack))
    pack["candidate_semantic_surface_version"] = SURFACE_VERSION
