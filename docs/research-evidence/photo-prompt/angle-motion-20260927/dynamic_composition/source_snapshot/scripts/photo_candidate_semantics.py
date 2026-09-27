"""Authored optional candidate semantics, independent of sampler ranking.

The extension source remains the owner. Compiled bundles are a projection, not
another authored meaning registry; associated visual profiles never activate
merely because a bundle is discoverable or selected.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from typing import Any

SURFACE_VERSION = "photo-candidate-semantic-surface/v1"
BUNDLE_VERSION = "photo-candidate-bundles/v1"
COMPILED_BUNDLE_FIELDS = (
    "id", "source_sha256", "associated_profile_ids", "components", "member_candidates",
    "confusion_boundaries", "relations", "adoption", "profile_activation",
)
MAINTENANCE_VERSION = "photo-extension-maintenance-ref/v1"
RUNTIME_EXTENSION_KEYS = frozenset({
    "schema_version", "auto_optional_policy", "facet_vocab", "preset_families",
    "preset_filter_defaults", "preset_render_contract_defaults", "presets",
    "existing_preset_metadata_overrides", "existing_preset_render_contract_extensions",
    "existing_preset_filter_extensions", "existing_preset_filter_overrides",
    "slots", "coherence_rules", "character_mechanism_graph", "slot_applicability",
    "visual_semantics", "maintenance_ref",
})
# These legacy declarations are explicitly documentation, never runtime policy.
LEGACY_MAINTENANCE_KEYS = frozenset({"contract_version", "description"})
BUNDLE_SOURCE_KEYS = frozenset({
    "id", "primary_visual_proposition", "hard_profile_id", "hard_profile_ids",
    "component_groups", "candidate_ids", "confusion_boundaries", "source_keywords",
    "activation_mode", "establishment", "runtime_preset_id", "terms", "relations", "candidate_only", "candidate_slots",
})


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


def validate_extension_keys(extension: dict[str, Any]) -> None:
    unknown = set(extension) - RUNTIME_EXTENSION_KEYS - LEGACY_MAINTENANCE_KEYS
    if unknown:
        raise ValueError(f"research extension has unsupported runtime keys: {sorted(unknown)}")
    reference = extension.get("maintenance_ref")
    if reference is not None and (
        not isinstance(reference, dict)
        or set(reference) != {"contract_version", "record_id", "sha256"}
        or reference.get("contract_version") != MAINTENANCE_VERSION
        or not str(reference.get("record_id") or "").strip()
        or not re.fullmatch(r"[0-9a-f]{64}", str(reference.get("sha256") or ""))
    ):
        raise ValueError("extension maintenance_ref requires its declared schema, record id and SHA-256")


def validate_semantic_policy(policy: dict[str, Any], allowed_dimensions: set[str]) -> None:
    if not policy:
        return  # Older dictionaries remain readable without opting into v1.
    if (not isinstance(policy, dict)
            or set(policy) != {"contract_version", "unknown_scope", "slot_dimensions", "required_extensions", "joint_adoption"}
            or policy.get("contract_version") != "photo-candidate-semantic-policy/v1"
            or policy.get("unknown_scope") != "not_eligible_for_bundle_adoption"
            or not isinstance(policy.get("slot_dimensions"), dict)):
        raise ValueError("candidate_semantic_policy requires its explicit dimension ownership schema")
    for slot, dimensions in policy["slot_dimensions"].items():
        if (not isinstance(dimensions, list) or len(strings(dimensions)) != len(dimensions)
                or not set(dimensions).issubset(allowed_dimensions)):
            raise ValueError(f"candidate semantic scope {slot} contains unknown dimensions")
    extensions = policy.get("required_extensions")
    if (not isinstance(extensions, list) or not extensions
            or any(not isinstance(name, str) or "/" in name or "\\" in name or not name.endswith(".json") for name in extensions)):
        raise ValueError("required candidate extensions must be JSON basenames")
    joint = policy.get("joint_adoption")
    if (not isinstance(joint, dict) or set(joint) != {"maximum_bundles", "maximum_members_per_bundle", "minimum_shared_content_words", "context_policy"}
            or joint.get("context_policy") != "self_contained_bundle_guards_only"
            or any(type(joint.get(key)) is not int or joint[key] < 1 for key in ("maximum_bundles", "maximum_members_per_bundle", "minimum_shared_content_words"))):
        raise ValueError("joint candidate adoption needs bounded positive integer limits and its declared context policy")


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


def validate_candidate_entries(data: dict[str, Any], allowed_dimensions: set[str]) -> None:
    for slot, entries in (data.get("slots") or {}).items():
        by_id = {entry["id"]: entry for entry in entries}
        for entry in entries:
            if "concept_units" in entry and not strings(entry["concept_units"]):
                raise ValueError(f"{slot}.{entry['id']} concept_units must be non-empty")
            if "relations" in entry:
                validate_relations(entry["relations"], f"{slot}.{entry['id']}")
            if "affected_dimensions" in entry and not set(strings(entry["affected_dimensions"])).issubset(allowed_dimensions):
                raise ValueError(f"{slot}.{entry['id']} has unknown affected dimensions")
            seen = {entry["id"]}
            target = entry.get("canonical_concept_id")
            while target:
                if target not in by_id or target in seen:
                    raise ValueError(f"{slot}.{entry['id']} has a missing or cyclic canonical concept reference")
                seen.add(target)
                target = by_id[target].get("canonical_concept_id")


def slot_dimensions(slot: str, policy: dict[str, Any] | None = None) -> list[str]:
    """Use the authored slot ownership table; unknown scopes stay unadoptable."""
    return strings(((policy or {}).get("slot_dimensions") or {}).get(slot))


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
        "affected_dimensions": strings(entry.get("affected_dimensions")) or slot_dimensions(slot, policy),
        "adoption": "optional",
    }
    if entry.get("canonical_concept_id"):
        result["canonical_concept_id"] = str(entry["canonical_concept_id"])
    return result


def compile_extension_bundles(data: dict[str, Any], extension: dict[str, Any]) -> None:
    rows = extension.get("visual_semantics")
    if rows is None:
        return
    if not isinstance(rows, list):
        raise ValueError("visual_semantics must be an array of authored optional bundles")
    entries: dict[str, list[tuple[str, dict[str, Any]]]] = {}
    for slot, values in (data.get("slots") or {}).items():
        for entry in values:
            entries.setdefault(str(entry.get("id") or ""), []).append((slot, entry))
    target = data.setdefault("candidate_bundles", [])
    existing = {row["id"] for row in target}
    for row in rows:
        if not isinstance(row, dict) or not row.get("id"):
            raise ValueError("visual_semantics entries require an id")
        unknown = set(row) - BUNDLE_SOURCE_KEYS
        if unknown:
            raise ValueError(f"visual_semantics.{row['id']} has unsupported keys: {sorted(unknown)}")
        validate_relations(row.get("relations", []), f"visual_semantics.{row['id']}")
        if row["id"] in existing:
            raise ValueError(f"duplicate candidate bundle id: {row['id']}")
        components = []
        for index, component in enumerate(row.get("component_groups") or []):
            if isinstance(component, str) and component.strip():
                components.append({"id": f"component_{index + 1}", "concept_units": [component.strip()], "minimum_realizations": 1})
            elif isinstance(component, dict) and component.get("id") and strings(component.get("visible_evidence")):
                if set(component) - {"id", "visible_evidence"}:
                    raise ValueError(f"candidate bundle {row['id']} has unsupported component fields")
                components.append({"id": str(component["id"]), "concept_units": strings(component["visible_evidence"]), "minimum_realizations": 1})
            else:
                raise ValueError(f"candidate bundle {row['id']} has an invalid component")
        members = strings(row.get("candidate_ids"))
        if not components or not members or len(members) != len(set(members)):
            raise ValueError(f"candidate bundle {row['id']} requires components and unique member IDs")
        scopes = row.get("candidate_slots") or {}
        if not isinstance(scopes, dict) or set(scopes) - set(members):
            raise ValueError(f"candidate bundle {row['id']} has invalid candidate slot scopes")
        resolved = {
            member: [pair for pair in entries.get(member, [])
                     if member not in scopes or pair[0] == scopes[member]]
            for member in members
        }
        missing = [member for member in members if len(resolved[member]) != 1]
        if missing:
            raise ValueError(f"candidate bundle {row['id']} has missing or ambiguous candidate references: {missing}")
        associated = strings(row.get("hard_profile_ids"))
        if row.get("hard_profile_id"):
            associated.append(str(row["hard_profile_id"]))
        compiled = {
            "id": str(row["id"]),
            "source_sha256": digest(row),
            "associated_profile_ids": list(dict.fromkeys(associated)),
            "components": components,
            "member_candidates": [
                {"id": f"slot:{resolved[member][0][0]}:{member}", "slot": resolved[member][0][0],
                 "entry_id": member, **semantic_source(resolved[member][0][1], resolved[member][0][0], data.get("candidate_semantic_policy"))}
                for member in members
            ],
            "confusion_boundaries": strings(row.get("confusion_boundaries")),
            "relations": copy.deepcopy(row.get("relations") or []),
            "adoption": "optional",
            "profile_activation": "independent_request_evidence_only",
        }
        target.append(compiled)
        existing.add(row["id"])


def validate_bundle_references(data: dict[str, Any], profiles: list[dict[str, Any]]) -> None:
    known = {str(row.get("id") or "") for row in profiles}
    for bundle in data.get("candidate_bundles") or []:
        unknown = set(bundle["associated_profile_ids"]) - known
        if unknown:
            raise ValueError(f"candidate bundle {bundle['id']} references unknown visual profiles: {sorted(unknown)}")


def public_bundles(data: dict[str, Any], pack: dict[str, Any], joint_admissions: dict[str, Any] | None = None) -> dict[str, Any]:
    visible = {
        str(candidate.get("id") or ""): candidate
        for payload in (pack.get("slots") or {}).values()
        for candidate in payload.get("candidates") or []
    }
    open_dimensions = set(((pack.get("authorial_core") or {}).get("intent_lock") or {}).get("open_dimensions") or [])
    result = []
    for bundle in data.get("candidate_bundles") or []:
        member_ids = {member["id"] for member in bundle["member_candidates"]}
        dimensions = {dimension for member in bundle["member_candidates"]
                      for dimension in member.get("affected_dimensions") or []}
        joint_admission = (joint_admissions or {}).get(bundle["id"])
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
        row["id"] = "bundle:" + row["id"]
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
    material["id"] = str(material.get("id") or "").removeprefix("bundle:")
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
    pack["candidate_semantic_surface_version"] = SURFACE_VERSION
