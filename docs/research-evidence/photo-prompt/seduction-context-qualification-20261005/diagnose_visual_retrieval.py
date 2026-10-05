"""Read-only, post-run replay; never authors a core, pack, or image."""

import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / "runtime/skills/photo-prompt-image-generator/scripts"
sys.dont_write_bytecode = True
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location("frozen_diagnostic_generator", SCRIPTS / "prompt_generator.py")
generator = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = generator
spec.loader.exec_module(generator)


def read_json(path):
    return json.loads(path.read_text())


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


targets = read_json(ROOT / "DATA-TARGET-SET.json")
profile_ids = targets["new_profile_ids"] + targets["enriched_profile_ids"]
candidate_ids = set(targets["changed_candidate_ids"])
data = generator.load_runtime_data(SCRIPTS.parent / "assets/photo_prompt_tags.json")
registry = data[generator.VISUAL_OBLIGATIONS_DATA_KEY]
profiles = {p["id"]: p for p in registry["profiles"]}
assert set(profile_ids) <= profiles.keys()
result = {
    "schema_version": "photo-postrun-retrieval-diagnostic/v1",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "scope": "Read-only post-run diagnostic on unchanged frozen inputs; not another authored test or candidate-pack generation.",
    "source_commit": targets["published_runtime_commit"],
    "dictionary_hash": generator.dictionary_hash(data),
    "compiled_visual_registry_sha256": generator.visual_profile_registry_sha256(registry),
    "profile_target_count": len(profile_ids),
    "candidate_target_count": len(candidate_ids),
    "query_embedding_api_calls": 0,
    "image_api_calls": 0,
    "new_packs_generated": 0,
    "arms": [],
}
for arm in ["arm-a", "arm-b", "arm-c2"]:
    directory = ROOT / arm
    pack = read_json(directory / "candidate_pack.json")[0]
    core = pack["authorial_core"]
    controls = read_json(directory / "creative_controls.json")
    embodiment = read_json(directory / "embodiment_review.json")
    prepared = generator.prepare_candidate_source(
        data, core, controls, embodiment, seed=pack["provenance"]["seed"]
    )
    trace = prepared["semantic_trace"]
    rows = generator.candidate_pack_visual_obligation_request_sources(prepared, trace)
    context = " ".join(row["text"] for row in rows)
    resolution = generator.candidate_pack_resolve_visual_profiles(data, prepared, trace, None)
    exposed = generator.candidate_pack_visual_concept_candidates(
        data, prepared, trace, None, pack.get("visual_obligations"), resolution
    )
    actual_ids = {c["id"] for c in pack["visual_concept_candidates"]["candidates"]}
    replayed_ids = {c["id"] for c in exposed["candidates"]}
    assert actual_ids == replayed_ids, (arm, actual_ids ^ replayed_ids)
    profile_diagnostics = []
    for profile_id in profile_ids:
        profile = profiles[profile_id]
        semantics = profile["semantics"].get("component_semantics", {})
        group_hits = {
            group["id"]: [term for term in group.get("any_terms", [])
                          if generator.intent_alias_matches(context, term)]
            for group in semantics.get("groups", [])
        }
        matched_groups = {key for key, terms in group_hits.items() if terms}
        candidate = profile.get("concept_candidate", {})
        profile_diagnostics.append({
            "profile_id": profile_id,
            "component_match": generator.candidate_pack_visual_component_match(profile, context),
            "matched_group_terms": group_hits,
            "required_groups_missing": sorted(set(semantics.get("required_group_ids", [])) - matched_groups),
            "minimum_component_groups": semantics.get("minimum_component_groups"),
            "semantic_discovery_requires_component_evidence": profile.get("activation", {}).get("semantic_discovery_requires_component_evidence") is True,
            "context_applicability": generator.visual_profile_context_applicability(
                profile, context, has_authorial_core_context=True, require_positive_context_terms=False
            ),
            "source_effects_allowed": generator.property_effects_allowed(
                core["intent_lock"], candidate.get("affected_dimensions", []), candidate.get("affected_properties")
            ),
            "resolver_hits": [hit for hit in resolution["hits"] if hit["profile_id"] == profile_id],
        })
    slot_research_ids = sorted(
        c["id"] for slot in pack["slots"].values() for c in slot["candidates"]
        if c["id"].split(":", 2)[-1] in candidate_ids
    )
    arm_result = {
        "arm_id": arm,
        "pack_id": pack["pack_id"],
        "pack_file_sha256": sha256(directory / "candidate_pack.json"),
        "source_rows": rows,
        "source_context_sha256": hashlib.sha256(context.encode()).hexdigest(),
        "original_optional_profile_ids": sorted(actual_ids),
        "replayed_optional_profile_ids": sorted(replayed_ids),
        "optional_profile_sets_equal": True,
        "ordering_policy": "Unordered public inspiration; compare stable ID sets, not array positions.",
        "research_slot_candidates_exposed": slot_research_ids,
        "research_profiles": profile_diagnostics,
    }
    if arm == "arm-a":
        entry = next(e for e in data["slots"]["hand_pose"] if e["id"] == "se_beckon_shaped_finger_static_state")
        contract, picked = generator.frozen_core_context(data, core, controls)
        arm_result["beckon_slot_probe"] = {
            "target_candidate_id": "slot:hand_pose:" + entry["id"],
            "frozen_slot_entry_eligible": generator.core_slot_entry_eligible(data, core, contract, picked, "hand_pose", entry),
            "actual_hand_pose_candidates": [c["id"] for c in pack["slots"]["hand_pose"]["candidates"]],
            "frozen_hand_focus_queries": generator.core_slot_focus_queries(data, core, "hand_pose"),
            "diagnosis_limit": "Eligibility does not establish ranking cause or sufficient prompt coverage. The absent candidate and frozen query are preserved for a scoped ranking audit.",
        }
    result["arms"].append(arm_result)
result["summary"] = {
    "all_three_replayed_profile_sets_equal": all(a["optional_profile_sets_equal"] for a in result["arms"]),
    "research_profile_component_matches": sum(p["component_match"] is not None for a in result["arms"] for p in a["research_profiles"]),
    "research_profile_component_checks": len(profile_ids) * len(result["arms"]),
    "research_profile_component_group_term_matches": sum(bool(terms) for a in result["arms"] for p in a["research_profiles"] for terms in p["matched_group_terms"].values()),
    "research_profile_resolver_hits": sum(len(p["resolver_hits"]) for a in result["arms"] for p in a["research_profiles"]),
    "interpretation_limit": "Lexical component absence is not proof of geometric absence. No prompt, aliases, pack, authored DATA, or generation criteria were changed by this diagnosis.",
}
destination = ROOT / "PARENT-RETRIEVAL-DIAGNOSTIC.json"
destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(result["summary"], ensure_ascii=False))
print(json.dumps({a["arm_id"]: len(a["research_slot_candidates_exposed"]) for a in result["arms"]}))
print(json.dumps(result["arms"][0]["beckon_slot_probe"], ensure_ascii=False))
