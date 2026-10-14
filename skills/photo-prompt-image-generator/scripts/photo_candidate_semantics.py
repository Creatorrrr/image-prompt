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
BUNDLE_VERSION = "photo-candidate-bundles/v2"
COMPILED_BUNDLE_FIELDS = (
    "id", "source_sha256", "associated_profile_ids", "components", "member_candidates",
    "confusion_boundaries", "relations", "adoption", "profile_activation",
    "realization_id", "source_record_sha256", "native_bundle_contract",
    "native_dependency_choices", "native_dependency_selections", "native_effect_closure",
    "affected_dimensions", "affected_properties", "realization_choices",
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






NATIVE_BUNDLE_CONTRACT = 'photo-native-selected-members/v1'


def native_bundle_view(data, bundle, pack, realization_id, dependency_selections=None,owner_selections=None):
    """Expose root obligations separately from explicitly adopted child choices."""
    import photo_candidate_corpus as c
    import photo_candidate_realizations as realizations
    import photo_semantic_evidence as native
    import photo_shared_views as views
    import prompt_generator as g
    cid=bundle['id'];core=pack['authorial_core'];selections=copy.deepcopy(dependency_selections or {})
    if not isinstance(selections,dict) or any(not isinstance(key,str) or not isinstance(value,str) for key,value in selections.items()):
        raise ValueError('explicit native dependency selections must map CID strings to actual RID strings')
    entry=c.entry(data,cid,realization_id=realization_id,dependency_selections=selections,owner_selections=owner_selections)
    proof=native.proof_of(entry);choices=native.dependency_choices(proof,realization_id)
    if not set(selections)<=set(choices):raise ValueError('unknown native member selection')
    row={**copy.deepcopy(bundle),**entry}
    row.update(realization_id=realization_id,native_bundle_contract=NATIVE_BUNDLE_CONTRACT,
        native_dependency_choices=choices,native_dependency_selections=selections,
        source_record_sha256=c.digest(data['candidates'][cid]),adoption='optional')
    row.setdefault('relations',[])
    row['member_candidates']=[];closure=[]
    try:
        closure=native.effect_closure(cid,proof,realization_id,selections)
        dimensions,properties,_=native.permission_scope(entry,core)
        constraints,picked=g.frozen_core_context(data,core,pack['creative_controls'])
        allowed=g.core_entry_eligible(data,core,constraints,picked,'',entry)
        pointers={pointer['candidate_id']:pointer for pointer in data['candidates'][cid]['content'].get('member_candidates',[])}
        for dependency,_ in native.selected_dependencies(proof,realization_id,selections):
            child_id=dependency['candidate_id']
            rid=next(item['realization_id'] for item in closure if item['candidate_id']==child_id)
            child_guard=native.compact(data['candidates'][child_id],data)
            child_choices=native.dependency_choices(child_guard,rid)
            member=views.materialize_member(data,pointers[child_id],realization_id=rid,
                dependency_selections={key:value for key,value in selections.items() if key in child_choices},owner_selections=owner_selections,guard_root=entry)
            if not g.core_entry_eligible(data,core,constraints,picked,member['slot'],member):
                allowed=False
            row['member_candidates'].append(member)
        status='eligible' if allowed else 'ineligible'
    except ValueError as error:
        # A required conditional member needs an actual choice. Publish its
        # bounded source-addressed choice inventory, never a union of siblings.
        dimensions=list(entry['affected_dimensions']);properties=copy.deepcopy(entry['affected_properties'])
        status='review_required';row['native_selection_reason']=str(error)
        if native._has_target_guards(entry) and not native.admission(entry,core,allow_unselected=True)['allowed']:
            # A supplied mapping that fails a source guard is not a pending choice.
            status='ineligible'
    row.update(native_effect_closure=closure,affected_dimensions=dimensions,affected_properties=properties,
        content_form='unordered_inspiration_terms',semantic_surface_version=SURFACE_VERSION,
        concept_units=[unit for component in row.get('components',[]) for unit in component['concept_units']],
        applicability={'status':status,'source':'native_whole_selected_dependencies'},conflicts_with=[])
    row['concept_terms']=list(row['concept_units'])
    row['selection_contract']={'scope':'root_components_plus_explicit_selected_members',
        'dependency_selections':'candidate_id_to_actual_child_realization',
        'component_evidence':'every_parent_component_id_to_literal_final_prompt_phrase',
        'relation_evidence':'every_parent_relation_id_to_literal_final_prompt_phrase',
        'associated_profiles_are_not_promoted':True}
    row['source_contract_sha256']=digest(bundle_source_material(row))
    return row


def bundle_variants(data, bundle, pack):
    import photo_candidate_corpus as c
    import photo_candidate_realizations as realizations
    import prompt_generator as g
    cid=bundle['id'];record=data['candidates'][cid]
    import photo_semantic_evidence as native
    if native.native_status(record)=='qualified':
        return [native_bundle_view(data,bundle,pack,rid) for rid in realizations.ids(record)]
    if not record['effects'].get('realizations'):
        return [bundle]
    core=pack['authorial_core']
    contract,picked=g.frozen_core_context(data,core,pack['creative_controls'])
    result=[]
    for rid in realizations.eligible_ids(data,cid,core,contract,picked):
        row={**copy.deepcopy(bundle),**c.entry(data,cid,realization_id=rid)}
        wanted=realizations.member_ids(record,rid)
        row['member_candidates']=[copy.deepcopy(member) for member in bundle['member_candidates'] if member['id'] in wanted]
        row['realization_id']=rid;row['source_record_sha256']=c.digest(record)
        result.append(row)
    return result


def public_bundles(data: dict[str, Any], pack: dict[str, Any], joint_admissions: dict[str, Any] | None = None) -> dict[str, Any]:
    visible = {
        str(candidate.get("id") or ""): candidate
        for payload in photo_native_pack.role_cards(pack).values()
        for candidate in payload.get("candidates") or []
    }
    open_dimensions = set(((pack.get("authorial_core") or {}).get("intent_lock") or {}).get("open_dimensions") or [])
    result = []
    originals={row['id']:row for row in data.get('candidate_bundles') or []}
    variants=[row for bundle in originals.values() for row in bundle_variants(data,bundle,pack)]
    for bundle in variants:
        if bundle["id"] not in getattr(data,"admitted_ids",set()):continue
        if bundle.get('native_bundle_contract') == NATIVE_BUNDLE_CONTRACT:
            # Candidate-native scope already includes root/joint effects and
            # only explicitly selected members; legacy member unions do not apply.
            result.append(copy.deepcopy(bundle));continue
        member_ids = {member["id"] for member in bundle["member_candidates"]}
        dimensions = {dimension for member in bundle["member_candidates"]
                      for dimension in member.get("affected_dimensions") or []}
        key=(bundle['id'],bundle.get('realization_id','base'))
        joint_admission = (joint_admissions or {}).get(key)
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
        row['source_record_sha256']=digest(data['candidates'][bundle['id']])
        row["source_contract_sha256"] = digest(bundle_source_material(row))
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
    grouped={}
    for row in result:grouped.setdefault(row['id'],[]).append(row)
    result=[]
    for cid,choices in grouped.items():
        if 'realization_id' not in choices[0] or not data['candidates'][cid]['effects'].get('realizations'):
            result.extend(choices);continue
        if choices[0].get('native_bundle_contract') == NATIVE_BUNDLE_CONTRACT:
            master=copy.deepcopy(originals[cid])
            master.update(native_bundle_contract=NATIVE_BUNDLE_CONTRACT,
                realization_choices=sorted(choices,key=lambda row:row['realization_id']),
                affected_dimensions=[],affected_properties=[],member_candidates=[],
                source_record_sha256=digest(data['candidates'][cid]),
                applicability={'status':'review_required','source':'explicit_actual_root_realization_required'},
                selection_contract={'realization_id':'one_presented_realization_required',
                    'dependency_selections':'candidate_id_to_actual_child_realization',
                    'associated_profiles_are_not_promoted':True})
            master['source_contract_sha256']=digest(bundle_source_material(master))
            result.append(master);continue
        master=copy.deepcopy(originals[cid])
        master.update(content_form='unordered_inspiration_terms',semantic_surface_version=SURFACE_VERSION,
                      source_record_sha256=digest(data['candidates'][cid]),
                      realization_choices=sorted(choices,key=lambda row:row['realization_id']),
                      applicability={'status':'eligible','source':'one_source_recomputed_realization_required'},
                      conflicts_with=[],concept_units=[unit for component in master['components'] for unit in component['concept_units']])
        master['concept_terms']=list(master['concept_units'])
        master['source_contract_sha256']=digest(bundle_source_material(master))
        master['selection_contract']={'realization_id':'one_presented_realization_required',
            'component_evidence':'selected_realization_components_only',
            'relation_evidence':'selected_realization_relations_only',
            'scope':'one_coherent_realization','associated_profiles_are_not_promoted':True}
        result.append(master)
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
            # Native bundles already carry their exact selected closure and
            # resolved owner effects. A role's local surface is not that view.
            if (source and value.get("content_form") == "unordered_inspiration_terms"
                    and value.get('native_bundle_contract') != NATIVE_BUNDLE_CONTRACT):
                value.update(copy.deepcopy(source))
                value["semantic_surface_version"] = SURFACE_VERSION
                value["concept_terms"] = list(source["concept_units"])
            for item in value.values():
                visit(item)
    visit(pack)
    if isinstance(pack,photo_native_pack.WorkingPack):visit(photo_native_pack.role_cards(pack))
    pack["candidate_semantic_surface_version"] = SURFACE_VERSION


def bundle_audit_material(bundle):
    if bundle.get('native_bundle_contract') != NATIVE_BUNDLE_CONTRACT:
        return bundle
    # A native pool may merge other role presentations for the same CID. Those
    # extra display fields are not the bundle's immutable semantic contract.
    fields=(*COMPILED_BUNDLE_FIELDS,'source_contract_sha256','selection_contract',
        'native_selection_reason','applicability','content_form','semantic_surface_version',
        'concept_units','concept_terms','conflicts_with')
    return {key:copy.deepcopy(bundle[key]) for key in fields if key in bundle}
